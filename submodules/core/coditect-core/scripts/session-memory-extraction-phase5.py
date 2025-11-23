#!/usr/bin/env python3
"""
CODITECT Session Memory Extraction - Phase 5: shell-snapshots Extraction

Purpose:
--------
Extract shell environment snapshots from ~/.claude/shell-snapshots/ with:
- Read-only access (original files never modified)
- Complete streaming processing (JSON parsing, memory safe)
- Deduplication against MEMORY-CONTEXT system
- Full provenance tracking (know origin of each message)
- Verification at every step (checksums, counts, integrity)

Safety Guarantees:
------------------
1. Original files checked with SHA-256 before processing
2. Processing is purely read-only (no modifications)
3. Original files checksummed again after processing
4. If checksums differ, abort with clear error
5. All extracted content backed up with full provenance

Output Structure:
-----------------
MEMORY-CONTEXT/session-memory-extraction/
├── phase-5-shell-snapshots/
│   ├── extracted-messages.jsonl (new unique messages)
│   ├── processing-log.txt (detailed execution log)
│   ├── shell-analysis.json (shell environment breakdown)
│   └── statistics.json (counts, dedup rates, etc)
└── logs/
    └── phase5-execution.log (full execution transcript)
"""

import json
import hashlib
import os
import sys
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set


# ============================================================================
# CUSTOM EXCEPTION HIERARCHY
# ============================================================================

class Phase5ExtractionError(Exception):
    """Base exception for Phase 5 extraction errors"""
    pass


class SourceFileError(Phase5ExtractionError):
    """Source file access or validation errors"""
    pass


class ChecksumError(Phase5ExtractionError):
    """Checksum verification errors"""
    pass


class ExtractionError(Phase5ExtractionError):
    """Message extraction errors"""
    pass


class DeduplicationError(Phase5ExtractionError):
    """Deduplication processing errors"""
    pass


class OutputError(Phase5ExtractionError):
    """Output file writing errors"""
    pass


class DataIntegrityError(Phase5ExtractionError):
    """Data integrity validation errors"""
    pass


# ============================================================================
# DUAL LOGGING SETUP
# ============================================================================

def setup_logging(log_dir: Path, verbose: bool = True) -> Tuple[logging.Logger, Path]:
    """Setup dual logging: stdout + file"""
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"phase5_{timestamp}.log"

    logger = logging.getLogger("Phase5Extractor")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    if verbose:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger, log_file


# ============================================================================
# MAIN EXTRACTOR CLASS
# ============================================================================

class SessionMemoryExtractor:
    """Extract shell snapshot metadata with safety guarantees."""

    def __init__(self, verbose: bool = True):
        """Initialize extractor with paths and state."""
        self.home = Path.home()
        self.source_dir = self.home / ".claude" / "shell-snapshots"
        self.memory_context = Path.cwd() / "MEMORY-CONTEXT"
        self.extraction_dir = self.memory_context / "session-memory-extraction" / "phase-5-shell-snapshots"
        self.logs_dir = self.memory_context / "session-memory-extraction" / "logs"
        self.verbose = verbose

        try:
            self.extraction_dir.mkdir(parents=True, exist_ok=True)
            self.logs_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OutputError(f"Failed to create directories: {e}") from e

        self.logger, self.log_file = setup_logging(self.logs_dir, verbose)

        self.extracted_messages = []
        self.new_unique_count = 0
        self.duplicate_count = 0
        self.total_processed = 0
        self.baseline_checksum = None
        self.errors = []
        self.statistics = {
            'total_snapshot_files': 0,
            'snapshots_parsed': 0,
            'env_vars_tracked': 0
        }

        try:
            self.global_hashes = self._load_global_hashes()
            self.logger.info(f"Loaded {len(self.global_hashes)} existing unique message hashes")
        except Exception as e:
            self.logger.warning(f"Failed to load global hashes, starting fresh: {e}")
            self.global_hashes = set()

    def _load_global_hashes(self) -> Set[str]:
        """Load existing unique message hashes from MEMORY-CONTEXT."""
        hash_file = self.memory_context / "dedup_state" / "global_hashes.json"

        if not hash_file.exists():
            self.logger.debug(f"Hash file not found at {hash_file}, starting fresh")
            return set()

        try:
            with open(hash_file, "r", encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, list):
                return set(data)
            elif isinstance(data, dict):
                return set(data.get("hashes", []))
            else:
                self.logger.warning(f"Unexpected hash file format, starting fresh")
                return set()

        except json.JSONDecodeError as e:
            raise DeduplicationError(f"Invalid JSON in hash file: {e}") from e
        except IOError as e:
            raise DeduplicationError(f"Failed to read hash file: {e}") from e

    def _compute_sha256(self, data: str) -> str:
        """Compute SHA-256 hash of data."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _compute_directory_checksum(self, directory: Path) -> str:
        """Compute SHA-256 checksum of entire directory (streaming)."""
        sha256_hash = hashlib.sha256()
        file_count = 0

        try:
            for file_path in sorted(directory.rglob('*')):
                if file_path.is_file():
                    with open(file_path, 'rb') as f:
                        for byte_block in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(byte_block)
                    file_count += 1
        except IOError as e:
            raise ChecksumError(f"Failed to read files for checksum: {e}") from e

        self.logger.debug(f"Computed checksum from {file_count} files")
        return sha256_hash.hexdigest()

    def verify_source_directory(self) -> Tuple[bool, str]:
        """Verify source directory exists and is readable."""
        self.logger.info("=" * 80)
        self.logger.info("PHASE 5: shell-snapshots EXTRACTION")
        self.logger.info("=" * 80)
        self.logger.info("")
        self.logger.info("Step 1/10: Verify source directory...")

        if not self.source_dir.exists():
            raise SourceFileError(f"Source directory not found: {self.source_dir}")

        if not os.access(self.source_dir, os.R_OK):
            raise SourceFileError(f"Source directory not readable: {self.source_dir}")

        self.logger.info(f"✓ Source directory verified")
        self.logger.info(f"  Location: {self.source_dir}")

        return True, "Directory verified"

    def compute_baseline_checksum(self) -> Tuple[bool, str, str]:
        """Compute baseline checksum before processing."""
        self.logger.info("")
        self.logger.info("Step 2/10: Compute baseline checksum...")

        try:
            checksum = self._compute_directory_checksum(self.source_dir)
            self.baseline_checksum = checksum
            self.logger.info(f"✓ Baseline checksum computed")
            self.logger.info(f"  SHA-256: {checksum}")
            return True, "Checksum computed", checksum
        except Exception as e:
            raise ChecksumError(f"Failed to compute baseline checksum: {e}") from e

    def extract_snapshot_metadata(self) -> Tuple[bool, str, int]:
        """Extract metadata from shell snapshot files."""
        self.logger.info("")
        self.logger.info("Step 3/10: Extract shell snapshot metadata...")

        messages = []

        try:
            snapshot_files = list(self.source_dir.glob('*.json')) + list(self.source_dir.glob('*/*.json'))
            self.statistics['total_snapshot_files'] = len(snapshot_files)

            self.logger.info(f"Found {len(snapshot_files)} snapshot files to process")

            for snapshot_file in snapshot_files:
                try:
                    with open(snapshot_file, 'r', encoding='utf-8') as f:
                        snapshot_data = json.load(f)

                    self.statistics['snapshots_parsed'] += 1

                    # Extract snapshot metadata
                    shell_type = snapshot_data.get('shell', 'unknown')
                    cwd = snapshot_data.get('cwd', '')
                    pwd_depth = len(cwd.split('/')) if cwd else 0

                    # Extract environment variables
                    env_vars = snapshot_data.get('env', {})
                    key_vars = ['PATH', 'SHELL', 'HOME', 'USER', 'PWD', 'PYTHONPATH', 'NODE_PATH']
                    important_env = {k: v for k, v in env_vars.items() if k in key_vars}
                    self.statistics['env_vars_tracked'] += len(important_env)

                    # Extract aliases if present
                    aliases = snapshot_data.get('aliases', {})
                    alias_count = len(aliases)

                    # Extract shell functions if present
                    functions = snapshot_data.get('functions', {})
                    func_count = len(functions)

                    # Build message content
                    message_content = f"Shell snapshot: {shell_type} in {cwd}"
                    if alias_count > 0:
                        message_content += f" ({alias_count} aliases)"
                    if func_count > 0:
                        message_content += f" ({func_count} functions)"

                    # Get timestamp
                    timestamp = snapshot_data.get('timestamp', int(datetime.now().timestamp() * 1000))
                    if isinstance(timestamp, str):
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            timestamp = int(dt.timestamp() * 1000)
                        except (ValueError, OSError):
                            timestamp = int(datetime.now().timestamp() * 1000)

                    message = {
                        'content': message_content,
                        'source': f'shell-snapshots/{snapshot_file.name}',
                        'timestamp': timestamp,
                        'source_type': 'shell-snapshots',
                        'metadata': {
                            'shell': shell_type,
                            'cwd': cwd,
                            'pwd_depth': pwd_depth,
                            'env_vars_count': len(important_env),
                            'aliases_count': alias_count,
                            'functions_count': func_count,
                            'has_history': 'history' in snapshot_data
                        }
                    }

                    messages.append(message)

                except json.JSONDecodeError as e:
                    self.logger.debug(f"  Error parsing JSON {snapshot_file.name}: {e}")
                except Exception as e:
                    self.logger.debug(f"  Error processing {snapshot_file.name}: {e}")
                    continue

            self.extracted_messages = messages
            self.logger.info(f"✓ Extracted {len(messages)} shell snapshot messages")
            return True, f"Extracted {len(messages)} messages", len(messages)

        except Exception as e:
            raise ExtractionError(f"Failed to extract metadata: {e}") from e

    def deduplicate_messages(self) -> Tuple[bool, str, int, int]:
        """Deduplicate extracted messages against global store."""
        self.logger.info("")
        self.logger.info("Step 4/10: Deduplicate messages against MEMORY-CONTEXT...")

        new_messages = []
        duplicates = 0

        try:
            for msg in self.extracted_messages:
                content_hash = self._compute_sha256(msg["content"])

                if content_hash not in self.global_hashes:
                    new_messages.append({
                        **msg,
                        "hash": content_hash
                    })
                    self.new_unique_count += 1
                else:
                    duplicates += 1

            self.duplicate_count = duplicates
            self.total_processed = len(self.extracted_messages)

            dedup_rate = (duplicates / self.total_processed * 100) if self.total_processed > 0 else 0

            self.logger.info(f"✓ Deduplication complete")
            self.logger.info(f"  New unique messages: {self.new_unique_count}")
            self.logger.info(f"  Duplicate messages: {duplicates}")
            self.logger.info(f"  Total processed: {self.total_processed}")
            self.logger.info(f"  Deduplication rate: {dedup_rate:.1f}%")

            self.extracted_messages = new_messages

            return True, "Deduplication complete", self.new_unique_count, duplicates

        except Exception as e:
            raise DeduplicationError(f"Deduplication failed: {e}") from e

    def create_shell_analysis(self) -> Tuple[bool, str]:
        """Create shell environment analysis."""
        self.logger.info("")
        self.logger.info("Step 5/10: Create shell analysis...")

        try:
            shell_types = {}
            for msg in self.extracted_messages:
                shell = msg['metadata']['shell']
                if shell not in shell_types:
                    shell_types[shell] = 0
                shell_types[shell] += 1

            analysis = {
                "extraction_timestamp": datetime.now().isoformat(),
                "source": "shell-snapshots",
                "total_snapshots": len(self.extracted_messages),
                "shell_types": shell_types,
                "total_env_vars": sum(m['metadata']['env_vars_count'] for m in self.extracted_messages),
                "total_aliases": sum(m['metadata']['aliases_count'] for m in self.extracted_messages),
                "total_functions": sum(m['metadata']['functions_count'] for m in self.extracted_messages)
            }

            # Atomic write
            analysis_file = self.extraction_dir / "shell-analysis.json"
            temp_file = analysis_file.with_suffix('.json.tmp')

            try:
                with open(temp_file, "w", encoding='utf-8') as f:
                    json.dump(analysis, f, indent=2, default=str, ensure_ascii=False)
                temp_file.replace(analysis_file)
            except Exception as e:
                if temp_file.exists():
                    temp_file.unlink()
                raise

            self.logger.info(f"✓ Shell analysis created")
            self.logger.info(f"  Location: {analysis_file}")

            return True, "Shell analysis created"

        except Exception as e:
            raise OutputError(f"Failed to create shell analysis: {e}") from e

    def save_extracted_messages(self) -> Tuple[bool, str]:
        """Save new unique messages in JSONL format."""
        self.logger.info("")
        self.logger.info("Step 6/10: Save extracted new unique messages...")

        try:
            output_file = self.extraction_dir / "extracted-messages.jsonl"
            temp_file = output_file.with_suffix('.jsonl.tmp')

            try:
                with open(temp_file, "w", encoding='utf-8') as f:
                    for msg in self.extracted_messages:
                        f.write(json.dumps(msg, default=str, ensure_ascii=False) + "\n")
                temp_file.replace(output_file)
            except Exception as e:
                if temp_file.exists():
                    temp_file.unlink()
                raise

            self.logger.info(f"✓ Extracted messages saved")
            self.logger.info(f"  Location: {output_file}")
            self.logger.info(f"  Messages: {len(self.extracted_messages)}")
            self.logger.info(f"  Size: {output_file.stat().st_size:,} bytes")

            return True, "Messages saved"

        except Exception as e:
            raise OutputError(f"Failed to save messages: {e}") from e

    def verify_post_extraction_checksum(self, baseline: str) -> Tuple[bool, str]:
        """Verify source directory unchanged after extraction."""
        self.logger.info("")
        self.logger.info("Step 7/10: Verify source directory unchanged after extraction...")

        try:
            post_checksum = self._compute_directory_checksum(self.source_dir)

            if post_checksum == baseline:
                self.logger.info(f"✓ Source directory integrity verified")
                self.logger.info(f"  Pre-extraction:  {baseline}")
                self.logger.info(f"  Post-extraction: {post_checksum}")
                self.logger.info(f"  Status: UNCHANGED ✓")
                return True, "Checksum verification passed"
            else:
                raise DataIntegrityError(
                    f"Source directory was modified during extraction!\n"
                    f"  Pre-extraction:  {baseline}\n"
                    f"  Post-extraction: {post_checksum}"
                )

        except DataIntegrityError:
            raise
        except Exception as e:
            raise ChecksumError(f"Failed to verify post-extraction checksum: {e}") from e

    def save_statistics(self):
        """Save extraction statistics."""
        self.logger.info("")
        self.logger.info("Step 8/10: Save extraction statistics...")

        try:
            stats = {
                "extraction_timestamp": datetime.now().isoformat(),
                "phase": "phase-5-shell-snapshots",
                "source_directory": str(self.source_dir),
                "total_snapshot_files": self.statistics['total_snapshot_files'],
                "snapshots_parsed": self.statistics['snapshots_parsed'],
                "env_vars_tracked": self.statistics['env_vars_tracked'],
                "total_messages_processed": self.total_processed,
                "new_unique_messages": self.new_unique_count,
                "duplicate_messages": self.duplicate_count,
                "deduplication_rate": (self.duplicate_count / self.total_processed * 100) if self.total_processed > 0 else 0,
                "extraction_success": len(self.errors) == 0,
                "errors": self.errors
            }

            stats_file = self.extraction_dir / "statistics.json"
            temp_file = stats_file.with_suffix('.json.tmp')

            try:
                with open(temp_file, "w", encoding='utf-8') as f:
                    json.dump(stats, f, indent=2, ensure_ascii=False)
                temp_file.replace(stats_file)
            except Exception as e:
                if temp_file.exists():
                    temp_file.unlink()
                raise

            self.logger.info(f"✓ Statistics saved to {stats_file}")

            return True

        except Exception as e:
            raise OutputError(f"Failed to save statistics: {e}") from e

    def generate_summary(self) -> str:
        """Generate summary report."""
        self.logger.info("")
        self.logger.info("Step 9/10: Generate summary report...")

        summary = f"""
{'='*80}
PHASE 5 EXTRACTION SUMMARY - shell-snapshots
{'='*80}

EXECUTION DETAILS:
  Timestamp: {datetime.now().isoformat()}
  Source Directory: {self.source_dir}
  Extraction Directory: {self.extraction_dir}

RESULTS:
  Snapshot Files: {self.statistics['total_snapshot_files']}
  Snapshots Parsed: {self.statistics['snapshots_parsed']}
  Environment Vars: {self.statistics['env_vars_tracked']}
  Total Messages Processed: {self.total_processed}
  New Unique Messages: {self.new_unique_count}
  Duplicate Messages: {self.duplicate_count}
  Deduplication Rate: {(self.duplicate_count / self.total_processed * 100) if self.total_processed > 0 else 0:.1f}%

VERIFICATION:
  Source Directory Integrity: {'✓ VERIFIED' if len(self.errors) == 0 else '✗ FAILED'}
  Extraction Success: {'✓ YES' if len(self.errors) == 0 else '✗ NO'}
  Total Errors: {len(self.errors)}

OUTPUT FILES:
  Shell Analysis: {self.extraction_dir / 'shell-analysis.json'}
  Extracted Messages: {self.extraction_dir / 'extracted-messages.jsonl'}
  Statistics: {self.extraction_dir / 'statistics.json'}
  Execution Log: {self.log_file}

{'='*80}
"""

        self.logger.info(summary)
        return summary

    def run(self) -> bool:
        """Execute complete Phase 5 extraction."""
        try:
            self.verify_source_directory()
            success, msg, baseline = self.compute_baseline_checksum()
            success, msg, count = self.extract_snapshot_metadata()
            if count == 0:
                self.logger.warning("No shell snapshot metadata extracted")
                return True
            self.deduplicate_messages()
            self.create_shell_analysis()
            self.save_extracted_messages()
            self.verify_post_extraction_checksum(baseline)
            self.save_statistics()
            self.generate_summary()
            self.logger.info("")
            self.logger.info("Step 10/10: Phase 5 extraction complete")
            self.logger.info("✓ ALL STEPS COMPLETED SUCCESSFULLY")
            return True

        except Phase5ExtractionError as e:
            self.logger.error(f"Extraction failed: {e}")
            self.errors.append(str(e))
            return False

        except Exception as e:
            self.logger.error(f"CRITICAL ERROR: {e}")
            self.logger.debug(traceback.format_exc())
            self.errors.append(f"Critical error: {e}")
            return False


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def main():
    """Run Phase 5 extraction."""
    import argparse

    parser = argparse.ArgumentParser(description="Phase 5: Extract messages from shell-snapshots")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    args = parser.parse_args()

    print("CODITECT Session Memory Extraction - Phase 5: shell-snapshots")
    print("")

    try:
        extractor = SessionMemoryExtractor(verbose=not args.quiet)
        success = extractor.run()

        print("")
        if success:
            print("✅ Phase 5 extraction SUCCESSFUL")
            sys.exit(0)
        else:
            print("❌ Phase 5 extraction FAILED")
            print(f"Check log file: {extractor.log_file}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Extraction cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
