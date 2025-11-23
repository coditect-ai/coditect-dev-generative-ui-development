#!/usr/bin/env python3
"""
CODITECT Session Memory Extraction - Phase 2: debug/ Logs Processing

Purpose:
--------
Systematically extract meaningful messages from ~/.claude/debug/ logs with:
- Read-only access (original files never modified)
- Complete streaming processing (log parsing, memory safe)
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
├── phase-2-debug/
│   ├── extracted-messages.jsonl (new unique messages)
│   ├── processing-log.txt (detailed execution log)
│   ├── session-index.json (mapping of messages to original files)
│   └── statistics.json (counts, dedup rates, etc)
└── logs/
    └── phase2-execution.log (full execution transcript)
"""

import json
import hashlib
import os
import sys
import logging
import traceback
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


# ============================================================================
# CUSTOM EXCEPTION HIERARCHY
# ============================================================================

class Phase2ExtractionError(Exception):
    """Base exception for Phase 2 extraction errors"""
    pass


class SourceFileError(Phase2ExtractionError):
    """Source file access or validation errors"""
    pass


class ChecksumError(Phase2ExtractionError):
    """Checksum verification errors"""
    pass


class ExtractionError(Phase2ExtractionError):
    """Message extraction errors"""
    pass


class DeduplicationError(Phase2ExtractionError):
    """Deduplication processing errors"""
    pass


class OutputError(Phase2ExtractionError):
    """Output file writing errors"""
    pass


class DataIntegrityError(Phase2ExtractionError):
    """Data integrity validation errors"""
    pass


# ============================================================================
# DUAL LOGGING SETUP
# ============================================================================

def setup_logging(log_dir: Path, verbose: bool = True) -> Tuple[logging.Logger, Path]:
    """
    Setup dual logging: stdout + file

    Args:
        log_dir: Directory for log files
        verbose: Enable console output

    Returns:
        Tuple of (logger, log_file_path)
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"phase2_{timestamp}.log"

    # Create logger
    logger = logging.getLogger("Phase2Extractor")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # File handler (always enabled, detailed)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler (optional, less detailed)
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
    """Extract and deduplicate debug log messages with safety guarantees."""

    def __init__(self, verbose: bool = True):
        """Initialize extractor with paths and state."""
        self.home = Path.home()
        self.source_dir = self.home / ".claude" / "debug"
        self.memory_context = Path.cwd() / "MEMORY-CONTEXT"
        self.extraction_dir = self.memory_context / "session-memory-extraction" / "phase-2-debug"
        self.logs_dir = self.memory_context / "session-memory-extraction" / "logs"
        self.verbose = verbose

        # Create directories
        try:
            self.extraction_dir.mkdir(parents=True, exist_ok=True)
            self.logs_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OutputError(f"Failed to create directories: {e}") from e

        # Setup dual logging
        self.logger, self.log_file = setup_logging(self.logs_dir, verbose)

        # Initialize state
        self.extracted_messages = []
        self.new_unique_count = 0
        self.duplicate_count = 0
        self.total_processed = 0
        self.file_checksums = {}
        self.errors = []

        # Load existing dedup state
        try:
            self.global_hashes = self._load_global_hashes()
            self.logger.info(f"Loaded {len(self.global_hashes)} existing unique message hashes")
        except Exception as e:
            self.logger.warning(f"Failed to load global hashes, starting fresh: {e}")
            self.global_hashes = set()

    def _load_global_hashes(self) -> set:
        """
        Load existing unique message hashes from MEMORY-CONTEXT.

        Returns:
            Set of existing message hashes

        Raises:
            IOError: If hash file cannot be read
        """
        hash_file = self.memory_context / "dedup_state" / "global_hashes.json"

        if not hash_file.exists():
            self.logger.debug(f"Hash file not found at {hash_file}, starting fresh")
            return set()

        try:
            with open(hash_file, "r", encoding='utf-8') as f:
                data = json.load(f)

            # Handle both array format and dictionary format
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
        """
        Compute SHA-256 hash of data.

        Args:
            data: String data to hash

        Returns:
            Hex digest of hash
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _compute_file_sha256(self, filepath: Path) -> str:
        """
        Compute SHA-256 hash of entire file (streaming).

        Args:
            filepath: Path to file

        Returns:
            Hex digest of hash

        Raises:
            IOError: If file cannot be read
        """
        sha256_hash = hashlib.sha256()

        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
        except IOError as e:
            raise ChecksumError(f"Failed to read file for checksum: {e}") from e

        return sha256_hash.hexdigest()

    def verify_source_directory(self) -> Tuple[bool, str, List[Path]]:
        """
        Verify source directory exists and list all files.

        Returns:
            Tuple of (success, message, file_list)

        Raises:
            SourceFileError: If source directory is invalid
        """
        self.logger.info("=" * 80)
        self.logger.info("PHASE 2: debug/ LOGS EXTRACTION")
        self.logger.info("=" * 80)
        self.logger.info("")
        self.logger.info("Step 1/10: Verify source directory...")

        if not self.source_dir.exists():
            raise SourceFileError(f"Source directory not found: {self.source_dir}")

        if not os.access(self.source_dir, os.R_OK):
            raise SourceFileError(f"Source directory not readable: {self.source_dir}")

        # Get all .txt files
        try:
            debug_files = sorted(list(self.source_dir.glob("*.txt")))
        except OSError as e:
            raise SourceFileError(f"Failed to list directory contents: {e}") from e

        if not debug_files:
            self.logger.warning(f"No debug log files found in {self.source_dir}")
            return True, "No files to process", []

        try:
            total_size = sum(f.stat().st_size for f in debug_files)
        except OSError as e:
            raise SourceFileError(f"Cannot access file metadata: {e}") from e

        self.logger.info(f"✓ Source directory verified")
        self.logger.info(f"  Location: {self.source_dir}")
        self.logger.info(f"  Files found: {len(debug_files)}")
        self.logger.info(f"  Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")

        return True, "Directory verified", debug_files

    def compute_baseline_checksums(self, files: List[Path]) -> Tuple[bool, str]:
        """
        Compute baseline checksums for all files.

        Args:
            files: List of files to checksum

        Returns:
            Tuple of (success, message)

        Raises:
            ChecksumError: If checksum computation fails
        """
        self.logger.info("")
        self.logger.info("Step 2/10: Compute baseline checksums for all files...")

        try:
            for filepath in files:
                checksum = self._compute_file_sha256(filepath)
                self.file_checksums[str(filepath)] = checksum

            self.logger.info(f"✓ Baseline checksums computed for {len(files)} files")
            return True, "Checksums computed"

        except Exception as e:
            raise ChecksumError(f"Failed to compute checksums: {e}") from e

    def stream_extract_log_messages(self, files: List[Path]) -> Tuple[bool, str, int]:
        """
        Stream extract meaningful messages from debug logs.

        Args:
            files: List of log files to process

        Returns:
            Tuple of (success, message, count)

        Raises:
            ExtractionError: If extraction fails
        """
        self.logger.info("")
        self.logger.info("Step 3/10: Stream extract meaningful messages from debug logs...")

        # Pattern to identify key log lines (not noise)
        key_patterns = [
            r"\[DEBUG\]",
            r"\[INFO\]",
            r"\[WARN\]",
            r"\[ERROR\]",
            r"Loading",
            r"Applying",
            r"Metrics",
            r"Stream",
            r"Permission",
            r"LSP",
        ]

        try:
            key_regex = re.compile("|".join(key_patterns), re.IGNORECASE)
        except re.error as e:
            raise ExtractionError(f"Invalid regex pattern: {e}") from e

        line_count = 0
        file_count = 0
        error_files = []

        try:
            for filepath in files:
                try:
                    with open(filepath, "r", encoding='utf-8', errors='replace') as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()
                            if not line:
                                continue

                            # Check if line contains meaningful information
                            if key_regex.search(line):
                                self.extracted_messages.append({
                                    "content": line,
                                    "source": f"debug/{filepath.name}:line-{line_num}",
                                    "file": filepath.name,
                                    "timestamp": int(datetime.now().timestamp() * 1000),
                                    "source_type": "debug"
                                })
                                line_count += 1

                    file_count += 1

                except IOError as e:
                    error_files.append((filepath.name, str(e)))
                    self.logger.debug(f"  Error reading {filepath.name}: {e}")

            self.logger.info(f"✓ Extracted {line_count} meaningful messages from {file_count} files")

            if error_files:
                self.logger.warning(f"  Note: {len(error_files)} files had read errors")

            return True, f"Extracted {line_count} messages", line_count

        except Exception as e:
            raise ExtractionError(f"Unexpected error during extraction: {e}") from e

    def deduplicate_messages(self) -> Tuple[bool, str, int, int]:
        """
        Deduplicate extracted messages against global store.

        Returns:
            Tuple of (success, message, new_count, duplicate_count)
        """
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

            # Keep only new messages for further processing
            self.extracted_messages = new_messages

            return True, "Deduplication complete", self.new_unique_count, duplicates

        except Exception as e:
            raise DeduplicationError(f"Deduplication failed: {e}") from e

    def create_session_index(self, files: List[Path]) -> Tuple[bool, str]:
        """
        Create index mapping messages back to original files.

        Args:
            files: List of source files

        Returns:
            Tuple of (success, message)

        Raises:
            OutputError: If index creation fails
        """
        self.logger.info("")
        self.logger.info("Step 5/10: Create session index with full provenance...")

        try:
            index = {
                "extraction_timestamp": datetime.now().isoformat(),
                "source_directory": str(self.source_dir),
                "source_type": "debug",
                "source_files": [str(f) for f in files],
                "total_files": len(files),
                "total_messages": self.total_processed,
                "new_unique_count": self.new_unique_count,
                "duplicate_count": self.duplicate_count,
                "messages": self.extracted_messages
            }

            # Atomic write with backup
            index_file = self.extraction_dir / "session-index.json"
            temp_file = index_file.with_suffix('.json.tmp')

            try:
                with open(temp_file, "w", encoding='utf-8') as f:
                    json.dump(index, f, indent=2, default=str, ensure_ascii=False)

                # Atomic rename
                temp_file.replace(index_file)

            except Exception as e:
                # Cleanup temp file on error
                if temp_file.exists():
                    temp_file.unlink()
                raise

            self.logger.info(f"✓ Session index created")
            self.logger.info(f"  Location: {index_file}")
            self.logger.info(f"  Size: {index_file.stat().st_size:,} bytes")

            return True, "Session index created"

        except Exception as e:
            raise OutputError(f"Failed to create session index: {e}") from e

    def save_extracted_messages(self) -> Tuple[bool, str]:
        """
        Save new unique messages in JSONL format.

        Returns:
            Tuple of (success, message)

        Raises:
            OutputError: If save fails
        """
        self.logger.info("")
        self.logger.info("Step 6/10: Save extracted new unique messages...")

        try:
            output_file = self.extraction_dir / "extracted-messages.jsonl"
            temp_file = output_file.with_suffix('.jsonl.tmp')

            try:
                with open(temp_file, "w", encoding='utf-8') as f:
                    for msg in self.extracted_messages:
                        f.write(json.dumps(msg, default=str, ensure_ascii=False) + "\n")

                # Atomic rename
                temp_file.replace(output_file)

            except Exception as e:
                # Cleanup temp file on error
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

    def verify_post_extraction_checksums(self, files: List[Path]) -> Tuple[bool, str]:
        """
        Verify all source files unchanged after extraction.

        Args:
            files: List of files to verify

        Returns:
            Tuple of (success, message)

        Raises:
            DataIntegrityError: If files were modified
        """
        self.logger.info("")
        self.logger.info("Step 7/10: Verify all source files unchanged after extraction...")

        try:
            all_match = True
            mismatches = []

            for filepath in files:
                post_checksum = self._compute_file_sha256(filepath)
                baseline = self.file_checksums[str(filepath)]

                if post_checksum != baseline:
                    self.logger.error(f"✗ {filepath.name}: CHECKSUM MISMATCH!")
                    self.logger.error(f"  Pre:  {baseline}")
                    self.logger.error(f"  Post: {post_checksum}")
                    mismatches.append(filepath.name)
                    all_match = False
                else:
                    self.logger.debug(f"✓ {filepath.name}: unchanged")

            if all_match:
                self.logger.info(f"✓ All {len(files)} files verified unchanged")
                self.logger.info(f"  Status: UNCHANGED ✓")
                return True, "All files verified"
            else:
                raise DataIntegrityError(
                    f"Some files were modified during extraction!\n"
                    f"  Modified files: {', '.join(mismatches)}"
                )

        except DataIntegrityError:
            raise
        except Exception as e:
            raise ChecksumError(f"Failed to verify checksums: {e}") from e

    def save_statistics(self):
        """
        Save extraction statistics.

        Raises:
            OutputError: If statistics save fails
        """
        self.logger.info("")
        self.logger.info("Step 8/10: Save extraction statistics...")

        try:
            stats = {
                "extraction_timestamp": datetime.now().isoformat(),
                "phase": "phase-2-debug",
                "source_directory": str(self.source_dir),
                "total_files_processed": len(self.file_checksums),
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

                # Atomic rename
                temp_file.replace(stats_file)

            except Exception as e:
                # Cleanup temp file on error
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
PHASE 2 EXTRACTION SUMMARY - debug/ Logs
{'='*80}

EXECUTION DETAILS:
  Timestamp: {datetime.now().isoformat()}
  Source Directory: {self.source_dir}
  Extraction Directory: {self.extraction_dir}

RESULTS:
  Files Processed: {len(self.file_checksums)}
  Total Messages Extracted: {self.total_processed}
  New Unique Messages: {self.new_unique_count}
  Duplicate Messages: {self.duplicate_count}
  Deduplication Rate: {(self.duplicate_count / self.total_processed * 100) if self.total_processed > 0 else 0:.1f}%

VERIFICATION:
  Source File Integrity: {'✓ VERIFIED' if len(self.errors) == 0 else '✗ FAILED'}
  Extraction Success: {'✓ YES' if len(self.errors) == 0 else '✗ NO'}
  Total Errors: {len(self.errors)}

OUTPUT FILES:
  Session Index: {self.extraction_dir / 'session-index.json'}
  Extracted Messages: {self.extraction_dir / 'extracted-messages.jsonl'}
  Statistics: {self.extraction_dir / 'statistics.json'}
  Execution Log: {self.log_file}

{'='*80}
"""

        self.logger.info(summary)
        return summary

    def run(self) -> bool:
        """
        Execute complete Phase 2 extraction.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Step 1: Verify source directory
            success, msg, files = self.verify_source_directory()
            if not files:
                self.logger.info("No debug files found. Skipping Phase 2.")
                return True

            # Step 2: Compute baseline checksums
            self.compute_baseline_checksums(files)

            # Step 3: Stream extract messages
            success, msg, count = self.stream_extract_log_messages(files)
            if count == 0:
                self.logger.warning("No meaningful messages extracted from debug logs")
                return True  # Not an error, just empty

            # Step 4: Deduplicate
            self.deduplicate_messages()

            # Step 5: Create session index
            self.create_session_index(files)

            # Step 6: Save messages
            self.save_extracted_messages()

            # Step 7: Verify post-extraction checksums
            self.verify_post_extraction_checksums(files)

            # Step 8: Save statistics
            self.save_statistics()

            # Step 9: Generate summary
            self.generate_summary()

            # Step 10: Final status
            self.logger.info("")
            self.logger.info("Step 10/10: Phase 2 extraction complete")
            self.logger.info("✓ ALL STEPS COMPLETED SUCCESSFULLY")

            return True

        except Phase2ExtractionError as e:
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
    """Run Phase 2 extraction."""
    import argparse

    parser = argparse.ArgumentParser(description="Phase 2: Extract messages from debug/ logs")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    args = parser.parse_args()

    print("CODITECT Session Memory Extraction - Phase 2: debug/ Logs")
    print("")

    try:
        extractor = SessionMemoryExtractor(verbose=not args.quiet)
        success = extractor.run()

        print("")
        if success:
            print("✅ Phase 2 extraction SUCCESSFUL")
            sys.exit(0)
        else:
            print("❌ Phase 2 extraction FAILED")
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
