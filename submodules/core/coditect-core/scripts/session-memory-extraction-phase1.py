#!/usr/bin/env python3
"""
CODITECT Session Memory Extraction - Phase 1: history.jsonl Processing

Purpose:
--------
Systematically extract unique messages from ~/.claude/history.jsonl with:
- Read-only access (original file never modified)
- Complete streaming processing (line-by-line, memory safe)
- Deduplication against MEMORY-CONTEXT system
- Full provenance tracking (know origin of each message)
- Verification at every step (checksums, counts, integrity)

Safety Guarantees:
------------------
1. Original file checked with SHA-256 before processing
2. Processing is purely read-only (no modifications)
3. Original file checksummed again after processing
4. If checksums differ, abort with clear error
5. All extracted content backed up with full provenance

Output Structure:
-----------------
MEMORY-CONTEXT/session-memory-extraction/
├── phase-1-history/
│   ├── extracted-messages.jsonl (new unique messages)
│   ├── processing-log.txt (detailed execution log)
│   ├── session-index.json (mapping of messages to original file)
│   └── statistics.json (counts, dedup rates, etc)
└── logs/
    └── phase1-execution.log (full execution transcript)
"""

import json
import hashlib
import os
import sys
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re


# ============================================================================
# CUSTOM EXCEPTION HIERARCHY
# ============================================================================

class Phase1ExtractionError(Exception):
    """Base exception for Phase 1 extraction errors"""
    pass


class SourceFileError(Phase1ExtractionError):
    """Source file access or validation errors"""
    pass


class ChecksumError(Phase1ExtractionError):
    """Checksum verification errors"""
    pass


class ExtractionError(Phase1ExtractionError):
    """Message extraction errors"""
    pass


class DeduplicationError(Phase1ExtractionError):
    """Deduplication processing errors"""
    pass


class OutputError(Phase1ExtractionError):
    """Output file writing errors"""
    pass


class DataIntegrityError(Phase1ExtractionError):
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
    log_file = log_dir / f"phase1_{timestamp}.log"

    # Create logger
    logger = logging.getLogger("Phase1Extractor")
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
    """Extract and deduplicate session memory with safety guarantees."""

    def __init__(self, verbose: bool = True):
        """Initialize extractor with paths and state."""
        self.home = Path.home()
        self.source_file = self.home / ".claude" / "history.jsonl"
        self.memory_context = Path.cwd() / "MEMORY-CONTEXT"
        self.extraction_dir = self.memory_context / "session-memory-extraction" / "phase-1-history"
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

    def verify_source_file(self) -> Tuple[bool, str]:
        """
        Verify source file exists and is readable.

        Returns:
            Tuple of (success, message)

        Raises:
            SourceFileError: If source file is invalid
        """
        self.logger.info("=" * 80)
        self.logger.info("PHASE 1: history.jsonl EXTRACTION")
        self.logger.info("=" * 80)
        self.logger.info("")
        self.logger.info("Step 1/10: Verify source file...")

        if not self.source_file.exists():
            raise SourceFileError(f"Source file not found: {self.source_file}")

        if not os.access(self.source_file, os.R_OK):
            raise SourceFileError(f"Source file not readable: {self.source_file}")

        # Get file size
        try:
            file_size = self.source_file.stat().st_size
        except OSError as e:
            raise SourceFileError(f"Cannot access file metadata: {e}") from e

        self.logger.info(f"✓ Source file exists and is readable")
        self.logger.info(f"  Location: {self.source_file}")
        self.logger.info(f"  Size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")

        return True, "Source file verified"

    def compute_baseline_checksum(self) -> Tuple[bool, str, str]:
        """
        Compute baseline checksum before processing.

        Returns:
            Tuple of (success, message, checksum)

        Raises:
            ChecksumError: If checksum computation fails
        """
        self.logger.info("")
        self.logger.info("Step 2/10: Compute baseline checksum...")

        try:
            checksum = self._compute_file_sha256(self.source_file)
            self.logger.info(f"✓ Baseline checksum computed")
            self.logger.info(f"  SHA-256: {checksum}")
            return True, "Checksum computed", checksum
        except Exception as e:
            raise ChecksumError(f"Failed to compute baseline checksum: {e}") from e

    def stream_extract_messages(self) -> Tuple[bool, str, int]:
        """
        Stream extract messages line-by-line from history.jsonl.

        Returns:
            Tuple of (success, message, count)

        Raises:
            ExtractionError: If extraction fails
        """
        self.logger.info("")
        self.logger.info("Step 3/10: Stream extract messages from history.jsonl...")

        try:
            line_count = 0
            error_lines = []

            with open(self.source_file, "r", encoding='utf-8', errors='replace') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        entry = json.loads(line)

                        # Extract message content
                        display = entry.get("display", "")
                        timestamp = entry.get("timestamp", "")
                        session_id = entry.get("sessionId", "")
                        project = entry.get("project", "")

                        if display:
                            self.extracted_messages.append({
                                "content": display,
                                "source": f"history.jsonl:line-{line_num}",
                                "timestamp": timestamp,
                                "session_id": session_id,
                                "project": project,
                                "source_type": "history"
                            })
                            line_count += 1

                    except json.JSONDecodeError as e:
                        error_lines.append((line_num, str(e)))
                        self.logger.debug(f"  Malformed JSON at line {line_num}: {e}")

            self.logger.info(f"✓ Extracted {line_count} messages from history.jsonl")

            if error_lines:
                self.logger.warning(f"  Note: {len(error_lines)} malformed lines skipped")

            return True, f"Extracted {line_count} messages", line_count

        except IOError as e:
            raise ExtractionError(f"Failed to read source file: {e}") from e
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

    def create_session_index(self) -> Tuple[bool, str]:
        """
        Create index mapping messages back to original file.

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
                "source_file": str(self.source_file),
                "source_type": "history.jsonl",
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

    def verify_post_extraction_checksum(self, baseline: str) -> Tuple[bool, str]:
        """
        Verify source file unchanged after extraction.

        Args:
            baseline: Baseline checksum to compare against

        Returns:
            Tuple of (success, message)

        Raises:
            DataIntegrityError: If file was modified
        """
        self.logger.info("")
        self.logger.info("Step 7/10: Verify source file unchanged after extraction...")

        try:
            post_checksum = self._compute_file_sha256(self.source_file)

            if post_checksum == baseline:
                self.logger.info(f"✓ Source file integrity verified")
                self.logger.info(f"  Pre-extraction:  {baseline}")
                self.logger.info(f"  Post-extraction: {post_checksum}")
                self.logger.info(f"  Status: UNCHANGED ✓")
                return True, "Checksum verification passed"
            else:
                raise DataIntegrityError(
                    f"Source file was modified during extraction!\n"
                    f"  Pre-extraction:  {baseline}\n"
                    f"  Post-extraction: {post_checksum}"
                )

        except DataIntegrityError:
            raise
        except Exception as e:
            raise ChecksumError(f"Failed to verify post-extraction checksum: {e}") from e

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
                "phase": "phase-1-history",
                "source_file": str(self.source_file),
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
PHASE 1 EXTRACTION SUMMARY - history.jsonl
{'='*80}

EXECUTION DETAILS:
  Timestamp: {datetime.now().isoformat()}
  Source File: {self.source_file}
  Extraction Directory: {self.extraction_dir}

RESULTS:
  Total Messages Processed: {self.total_processed}
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
        Execute complete Phase 1 extraction.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Step 1: Verify source file
            self.verify_source_file()

            # Step 2: Compute baseline checksum
            success, msg, baseline = self.compute_baseline_checksum()

            # Step 3: Stream extract messages
            success, msg, count = self.stream_extract_messages()
            if count == 0:
                self.logger.warning("No messages extracted from source file")
                return True  # Not an error, just empty

            # Step 4: Deduplicate
            self.deduplicate_messages()

            # Step 5: Create session index
            self.create_session_index()

            # Step 6: Save messages
            self.save_extracted_messages()

            # Step 7: Verify post-extraction checksum
            self.verify_post_extraction_checksum(baseline)

            # Step 8: Save statistics
            self.save_statistics()

            # Step 9: Generate summary
            self.generate_summary()

            # Step 10: Final status
            self.logger.info("")
            self.logger.info("Step 10/10: Phase 1 extraction complete")
            self.logger.info("✓ ALL STEPS COMPLETED SUCCESSFULLY")

            return True

        except Phase1ExtractionError as e:
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
    """Run Phase 1 extraction."""
    import argparse

    parser = argparse.ArgumentParser(description="Phase 1: Extract messages from history.jsonl")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output")
    args = parser.parse_args()

    print("CODITECT Session Memory Extraction - Phase 1: history.jsonl")
    print("")

    try:
        extractor = SessionMemoryExtractor(verbose=not args.quiet)
        success = extractor.run()

        print("")
        if success:
            print("✅ Phase 1 extraction SUCCESSFUL")
            sys.exit(0)
        else:
            print("❌ Phase 1 extraction FAILED")
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
