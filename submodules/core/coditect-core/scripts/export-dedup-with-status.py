#!/usr/bin/env python3
"""
Export Deduplication with Guaranteed Status Report

This wrapper ensures that /export-dedup ALWAYS displays a visible status report
by writing output to:
  1. stdout (for immediate display)
  2. MEMORY-CONTEXT/export-dedup-status.txt (persistent log)
  3. Prints final summary with clear visual markers

PRODUCTION-GRADE ERROR HANDLING:
- Custom exception hierarchy
- Dual logging (file + stdout)
- Atomic file operations
- Data integrity verification
- Graceful error recovery
- User-friendly error messages

Author: Claude + AZ1.AI
License: MIT
"""

import sys
import subprocess
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import os
import re
import signal
import tempfile
import shutil


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class ExportDedupStatusError(Exception):
    """Base exception for export-dedup-with-status operations"""
    pass


class SourceFileError(ExportDedupStatusError):
    """Export-dedup script not found"""
    pass


class ExecutionError(ExportDedupStatusError):
    """Script execution failure"""
    pass


class OutputError(ExportDedupStatusError):
    """Status report write failure"""
    pass


class DataIntegrityError(ExportDedupStatusError):
    """Output parsing or integrity verification failure"""
    pass


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging(log_dir: Path) -> logging.Logger:
    """
    Configure dual logging (file + stdout).

    Args:
        log_dir: Directory for log files

    Returns:
        Configured logger instance
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"export-dedup-status-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    logger = logging.getLogger("export_dedup_status")
    logger.setLevel(logging.DEBUG)

    # File handler - detailed logs
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler - user-friendly output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


# ============================================================================
# SIGNAL HANDLING
# ============================================================================

class GracefulExit:
    """Handle graceful shutdown on SIGINT/SIGTERM"""

    def __init__(self):
        self.exit_requested = False
        signal.signal(signal.SIGINT, self.request_exit)
        signal.signal(signal.SIGTERM, self.request_exit)

    def request_exit(self, signum, frame):
        """Set exit flag on signal"""
        self.exit_requested = True
        print("\n\n⚠️  Interrupt received. Writing status report...")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_metric(text: str, pattern: str, fallback_pattern: Optional[str] = None) -> Optional[int]:
    """
    Extract numeric metric from output text.

    Examples:
        extract_metric(output, "New unique:", "new_unique")
        → Looks for "New unique: 143" and returns 143

    Args:
        text: Text to search
        pattern: Primary search pattern
        fallback_pattern: Alternative pattern if primary fails

    Returns:
        Extracted integer value or None if not found
    """
    if not text:
        return None

    # Try to find pattern followed by a number
    # Handles formats like:
    # - "New unique: 143"
    # - "New unique messages: 143"
    # - "Total messages: 206"
    match = re.search(rf"{re.escape(pattern)}\s*(\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try fallback pattern if provided
    if fallback_pattern:
        match = re.search(rf"{re.escape(fallback_pattern)}\s*(\d+)", text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def atomic_write(filepath: Path, content: str, logger: logging.Logger) -> None:
    """
    Atomically write content to file using temp + rename.

    Args:
        filepath: Target file path
        content: Content to write
        logger: Logger instance

    Raises:
        OutputError: If write fails
    """
    temp_file = None
    try:
        # Create temp file in same directory for atomic rename
        temp_fd, temp_path = tempfile.mkstemp(
            dir=filepath.parent,
            prefix=f".{filepath.name}.tmp-",
            text=True
        )
        temp_file = Path(temp_path)

        # Write to temp file
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            f.write(content)

        # Atomic rename
        temp_file.rename(filepath)
        logger.debug(f"Atomically wrote: {filepath}")

    except Exception as e:
        # Clean up temp file on failure
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except:
                pass
        raise OutputError(f"Failed to write {filepath}: {e}") from e


def create_backup(filepath: Path, logger: logging.Logger) -> Path:
    """
    Create timestamped backup of file.

    Args:
        filepath: File to backup
        logger: Logger instance

    Returns:
        Path to backup file

    Raises:
        OutputError: If backup creation fails
    """
    try:
        if not filepath.exists():
            logger.debug(f"No existing file to backup: {filepath}")
            return None

        backup_path = filepath.parent / f"{filepath.name}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(filepath, backup_path)
        logger.debug(f"Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        raise OutputError(f"Failed to create backup of {filepath}: {e}") from e


def find_master_repo(start_path: Path) -> Path:
    """
    Intelligently find the master repository root.

    Walks up the directory tree from start_path looking for a directory that:
    1. Contains a .git directory (is a git repo)
    2. Contains a submodules/ directory (is the master repo with submodules)

    This allows the script to work from anywhere:
    - Run from PROJECTS folder
    - Run from master repo
    - Run from any submodule
    - Run from any subdirectory

    Args:
        start_path: Starting point for search (usually script location)

    Returns:
        Path to master repo root, or None if not found
    """
    current = start_path if start_path.is_dir() else start_path.parent

    # Walk up directory tree (max 10 levels to prevent infinite loop)
    for _ in range(10):
        # Check if this directory is the master repo
        has_git = (current / ".git").exists()
        has_submodules = (current / "submodules").exists() and (current / "submodules").is_dir()

        if has_git and has_submodules:
            return current

        # Move up one level
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent

    return None


def verify_script_exists(script_path: Path) -> None:
    """
    Verify export-dedup.py script exists.

    Args:
        script_path: Path to script

    Raises:
        SourceFileError: If script not found
    """
    if not script_path.exists():
        raise SourceFileError(
            f"export-dedup.py not found at {script_path}\n\n"
            "This script is required for deduplication to work.\n"
            "Make sure submodules are initialized: git submodule update --init --recursive"
        )


def parse_execution_output(
    stdout: str,
    stderr: str,
    returncode: int,
    logger: logging.Logger
) -> Dict[str, Any]:
    """
    Parse execution output and extract metrics.

    Args:
        stdout: Standard output
        stderr: Standard error
        returncode: Exit code
        logger: Logger instance

    Returns:
        Dictionary with parsed metrics

    Raises:
        DataIntegrityError: If critical metrics can't be extracted
    """
    try:
        # Extract key metrics from output
        metrics = {
            'new_unique': extract_metric(stdout, "New unique:"),
            'duplicates': extract_metric(stdout, "Duplicates filtered:"),
            'global_unique': extract_metric(stdout, "Global unique count:"),
            'total_messages': extract_metric(stdout, "Total messages:"),
            'files_processed': extract_metric(stdout, "Files processed:"),
        }

        # Calculate overall dedup rate if possible
        if metrics['total_messages'] and metrics['duplicates']:
            metrics['dedup_rate'] = (
                metrics['duplicates'] / metrics['total_messages'] * 100
            )
        else:
            metrics['dedup_rate'] = None

        # Verify critical metrics present (if success)
        if returncode == 0:
            if metrics['new_unique'] is None and metrics['total_messages'] is None:
                logger.warning("Could not extract metrics from output - may indicate parsing issue")
                # Not fatal, just log warning

        return metrics

    except Exception as e:
        raise DataIntegrityError(f"Failed to parse execution output: {e}") from e


def format_status_report(
    start_time: datetime,
    end_time: datetime,
    returncode: int,
    metrics: Dict[str, Any],
    stdout: str,
    stderr: str,
    logger: logging.Logger
) -> str:
    """
    Format comprehensive status report.

    Args:
        start_time: Execution start time
        end_time: Execution end time
        returncode: Exit code
        metrics: Parsed metrics
        stdout: Standard output
        stderr: Standard error
        logger: Logger instance

    Returns:
        Formatted status report string
    """
    duration = (end_time - start_time).total_seconds()
    status = "✅ SUCCESS" if returncode == 0 else "❌ FAILED"

    # Build header
    header = f"""
{'='*80}
EXPORT-DEDUP EXECUTION REPORT
{'='*80}
Started: {start_time.isoformat()}
Completed: {end_time.isoformat()}
Duration: {duration:.2f} seconds
Status: {status}
Exit Code: {returncode}
{'='*80}
"""

    # Build metrics display
    metrics_display = f"""
{'🔐'*40}
📊 BACKUP & DEDUPLICATION RESULTS
{'🔐'*40}
"""
    if metrics.get('new_unique') is not None:
        metrics_display += f"\n🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: {metrics['new_unique']}\n"
    if metrics.get('duplicates') is not None:
        metrics_display += f"🔄 Duplicate Messages Filtered: {metrics['duplicates']}\n"
    if metrics.get('total_messages') is not None:
        metrics_display += f"📨 Total Messages Processed: {metrics['total_messages']}\n"
    if metrics.get('global_unique') is not None:
        metrics_display += f"💾 Total Unique Messages in Storage: {metrics['global_unique']}\n"
    if metrics.get('files_processed') is not None:
        metrics_display += f"📁 Files Processed: {metrics['files_processed']}\n"
    if metrics.get('dedup_rate') is not None:
        metrics_display += f"📈 Deduplication Rate: {metrics['dedup_rate']:.1f}%\n"
    metrics_display += f"{'🔐'*40}\n"

    # Build full output section
    output_section = "\n"
    if stdout:
        output_section += "STANDARD OUTPUT:\n"
        output_section += "=" * 80 + "\n"
        output_section += stdout + "\n"
        output_section += "=" * 80 + "\n\n"

    if stderr:
        output_section += "STANDARD ERROR:\n"
        output_section += "=" * 80 + "\n"
        output_section += stderr + "\n"
        output_section += "=" * 80 + "\n\n"

    # Combine all sections
    return header + "\n" + metrics_display + "\n" + output_section


def main() -> int:
    """
    Execute export-dedup.py and ALWAYS display status report.

    Returns:
        Exit code (0=success, 1=error, 130=interrupted)
    """

    # Initialize graceful exit handler
    graceful_exit = GracefulExit()

    # Paths - Smart repo detection
    repo_root = find_master_repo(Path(__file__).resolve())
    if not repo_root:
        logger.error("❌ Could not find master repository root")
        logger.error("   Looking for directory with .git and submodules/")
        return 1

    script_path = repo_root / "submodules" / "core" / "coditect-core" / "scripts" / "export-dedup.py"
    memory_context = repo_root / "MEMORY-CONTEXT"
    status_log = memory_context / "export-dedup-status.txt"
    log_dir = memory_context / "logs"

    # Setup logging
    logger = setup_logging(log_dir)

    # Log repo detection for debugging
    logger.info(f"✅ Master repo detected: {repo_root}")
    logger.debug(f"   Script location: {Path(__file__).resolve()}")
    logger.debug(f"   MEMORY-CONTEXT: {memory_context}")

    # Ensure MEMORY-CONTEXT exists
    try:
        memory_context.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create MEMORY-CONTEXT directory: {e}")
        return 1

    # Timestamp for this execution
    start_time = datetime.now()

    try:
        # Verify script exists
        verify_script_exists(script_path)

        # Build status report header
        logger.info(f"\n{'='*80}")
        logger.info("EXPORT-DEDUP EXECUTION REPORT")
        logger.info(f"{'='*80}")
        logger.info(f"Started: {start_time.isoformat()}")
        logger.info(f"Repository: {repo_root.name}")
        logger.info(f"Status Log: {status_log.relative_to(repo_root)}")
        logger.info(f"{'='*80}\n")

        # Check for early interrupt
        if graceful_exit.exit_requested:
            return 130

        # Execute the actual export-dedup script
        logger.info("📦 RUNNING DEDUPLICATION PROCESS...\n")

        result = subprocess.run(
            [sys.executable, str(script_path), "--yes", "--auto-compact"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            timeout=600  # 10 minute timeout
        )

        # Check for interrupt during execution
        if graceful_exit.exit_requested:
            logger.warning("Execution interrupted by user")
            return 130

        # Capture all output
        stdout = result.stdout if result.stdout else ""
        stderr = result.stderr if result.stderr else ""

        # Parse output for metrics
        metrics = parse_execution_output(stdout, stderr, result.returncode, logger)

        # Print script output immediately to stdout
        if stdout:
            print(stdout, flush=True)
        if stderr:
            print(stderr, file=sys.stderr, flush=True)

        # Generate final status
        end_time = datetime.now()

        # Format comprehensive report
        complete_report = format_status_report(
            start_time,
            end_time,
            result.returncode,
            metrics,
            stdout,
            stderr,
            logger
        )

        # Print metrics prominently to stdout
        if metrics:
            logger.info(f"\n{'🔐'*40}")
            logger.info("📊 BACKUP & DEDUPLICATION RESULTS")
            logger.info(f"{'🔐'*40}")
            if metrics.get('new_unique') is not None:
                logger.info(f"🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: {metrics['new_unique']}")
            if metrics.get('duplicates') is not None:
                logger.info(f"🔄 Duplicate Messages Filtered: {metrics['duplicates']}")
            if metrics.get('total_messages') is not None:
                logger.info(f"📨 Total Messages Processed: {metrics['total_messages']}")
            if metrics.get('global_unique') is not None:
                logger.info(f"💾 Total Unique Messages in Storage: {metrics['global_unique']}")
            logger.info(f"{'🔐'*40}\n")

        # Print execution summary
        duration = (end_time - start_time).total_seconds()
        status = "✅ SUCCESS" if result.returncode == 0 else "❌ FAILED"

        logger.info(f"{'='*80}")
        logger.info("EXECUTION SUMMARY")
        logger.info(f"{'='*80}")
        logger.info(f"Status: {status}")
        logger.info(f"Exit Code: {result.returncode}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"{'='*80}\n")

        # Create backup of existing status log
        if status_log.exists():
            create_backup(status_log, logger)

        # Write to status log file atomically
        atomic_write(status_log, complete_report, logger)

        # Print log location to user
        logger.info(f"📝 Full report saved to: {status_log.relative_to(repo_root)}\n")

        # ================================================================
        # AUTO-SYNC: Automatically sync git repositories after success
        # ================================================================
        if result.returncode == 0:
            logger.info(f"{'='*80}")
            logger.info("STEP 5: AUTO-SYNCING GIT REPOSITORIES")
            logger.info(f"{'='*80}\n")

            # Find dedup-and-sync.sh script in master repo
            # repo_root is already the master repo (calculated at line 390)
            memory_context_dir = repo_root / "MEMORY-CONTEXT"
            sync_script = memory_context_dir / "dedup-and-sync.sh"

            if sync_script.exists() and sync_script.is_file():
                logger.info("🔄 Running dedup-and-sync.sh...")
                logger.info(f"   Script: {sync_script.relative_to(repo_root)}\n")

                try:
                    # Run sync script (pass through output in real-time)
                    sync_result = subprocess.run(
                        [str(sync_script)],
                        cwd=str(memory_context_dir),
                        capture_output=False,  # Show output in real-time
                        text=True,
                        timeout=300  # 5 minutes max for git operations
                    )

                    if sync_result.returncode == 0:
                        logger.info("\n✅ Git sync completed successfully!")
                        logger.info("   All changes committed and pushed to remote\n")
                    else:
                        logger.warning(f"\n⚠️  Git sync exited with code {sync_result.returncode}")
                        logger.warning("   Check output above for details")
                        logger.warning("   You may need to run manually:\n")
                        logger.warning(f"     cd MEMORY-CONTEXT && ./dedup-and-sync.sh\n")

                except subprocess.TimeoutExpired:
                    logger.error("\n❌ Git sync timed out (>5 minutes)")
                    logger.error("   Network issues or too many changes")
                    logger.error("   Run manually: cd MEMORY-CONTEXT && ./dedup-and-sync.sh\n")

                except Exception as e:
                    logger.error(f"\n❌ Git sync failed: {e}")
                    logger.error("   Run manually: cd MEMORY-CONTEXT && ./dedup-and-sync.sh\n")

            else:
                logger.warning("\n⚠️  dedup-and-sync.sh not found")
                logger.warning(f"   Expected location: {sync_script}")
                logger.warning("   Skipping git sync - run manually if needed:\n")
                logger.warning(f"     cd MEMORY-CONTEXT && ./dedup-and-sync.sh\n")

        else:
            # Export-dedup failed, don't try to sync
            logger.info("\n⚠️  Skipping git sync (export-dedup had errors)\n")

        # ================================================================
        # End of auto-sync integration
        # ================================================================

        # Exit with same code as script
        return result.returncode

    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  Operation interrupted by user")
        return 130

    except subprocess.TimeoutExpired:
        error_msg = "\n❌ TIMEOUT ERROR: export-dedup.py exceeded 10 minute timeout\n\n"
        error_msg += "Suggestion: Check for stuck processes or very large exports"
        logger.error(error_msg)

        # Log to file
        try:
            end_time = datetime.now()
            report = format_status_report(
                start_time, end_time, 1, {}, "", error_msg, logger
            )
            atomic_write(status_log, report, logger)
        except:
            pass

        return 1

    except SourceFileError as e:
        logger.error(f"\n❌ SOURCE FILE ERROR: {e}\n")

        # Log to file
        try:
            end_time = datetime.now()
            report = format_status_report(
                start_time, end_time, 1, {}, "", str(e), logger
            )
            atomic_write(status_log, report, logger)
        except:
            pass

        return 1

    except ExecutionError as e:
        logger.error(f"\n❌ EXECUTION ERROR: {e}\n")
        logger.info("Suggestion: Check export-dedup.py for errors")

        # Log to file
        try:
            end_time = datetime.now()
            report = format_status_report(
                start_time, end_time, 1, {}, "", str(e), logger
            )
            atomic_write(status_log, report, logger)
        except:
            pass

        return 1

    except OutputError as e:
        logger.error(f"\n❌ OUTPUT ERROR: {e}\n")
        logger.info("Suggestion: Check write permissions and disk space")
        return 1

    except DataIntegrityError as e:
        logger.error(f"\n❌ DATA INTEGRITY ERROR: {e}\n")
        logger.info("Suggestion: Check output format from export-dedup.py")
        return 1

    except Exception as e:
        logger.error(f"\n❌ UNEXPECTED ERROR: {e}\n")
        logger.debug("Full traceback:", exc_info=True)
        logger.info("Suggestion: Check logs for details")

        # Log to file
        try:
            import traceback
            end_time = datetime.now()
            error_trace = traceback.format_exc()
            report = format_status_report(
                start_time, end_time, 1, {}, "", f"{e}\n\n{error_trace}", logger
            )
            atomic_write(status_log, report, logger)
        except:
            pass

        return 1

    finally:
        logger.debug("Cleanup complete")


if __name__ == "__main__":
    import traceback
    sys.exit(main())
