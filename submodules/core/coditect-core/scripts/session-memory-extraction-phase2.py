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
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class Phase2DebugExtractor:
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
        self.extraction_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Initialize state
        self.log_file = self.logs_dir / f"phase2-{datetime.now().isoformat()}.log"
        self.extracted_messages = []
        self.new_unique_count = 0
        self.duplicate_count = 0
        self.total_processed = 0
        self.file_checksums = {}
        self.errors = []

        # Load existing dedup state
        self.global_hashes = self._load_global_hashes()
        self.log(f"Loaded {len(self.global_hashes)} existing unique message hashes")

    def log(self, message: str):
        """Log message to both console and file."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"

        if self.verbose:
            print(log_entry)

        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")

    def _load_global_hashes(self) -> set:
        """Load existing unique message hashes from MEMORY-CONTEXT."""
        hash_file = self.memory_context / "dedup_state" / "global_hashes.json"
        if not hash_file.exists():
            self.log(f"Warning: Hash file not found at {hash_file}")
            return set()

        try:
            with open(hash_file, "r") as f:
                data = json.load(f)

            # Handle both array format and dictionary format
            if isinstance(data, list):
                return set(data)
            elif isinstance(data, dict):
                return set(data.get("hashes", []))
            else:
                return set()
        except Exception as e:
            self.log(f"Error loading hashes: {e}")
            return set()

    def _compute_sha256(self, data: str) -> str:
        """Compute SHA-256 hash of data."""
        return hashlib.sha256(data.encode()).hexdigest()

    def _compute_file_sha256(self, filepath: Path) -> str:
        """Compute SHA-256 hash of entire file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def verify_source_directory(self) -> Tuple[bool, str, List[Path]]:
        """Verify source directory exists and list all files."""
        self.log("=" * 80)
        self.log("PHASE 2: debug/ LOGS EXTRACTION")
        self.log("=" * 80)
        self.log("")

        self.log("Step 1/12: Verify source directory...")

        if not self.source_dir.exists():
            msg = f"Source directory not found: {self.source_dir}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg, []

        if not os.access(self.source_dir, os.R_OK):
            msg = f"Source directory not readable: {self.source_dir}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg, []

        # Get all .txt files
        debug_files = sorted(list(self.source_dir.glob("*.txt")))

        if not debug_files:
            msg = f"No debug log files found in {self.source_dir}"
            self.log(f"WARNING: {msg}")
            return True, "No files to process", []

        total_size = sum(f.stat().st_size for f in debug_files)
        self.log(f"✓ Source directory verified")
        self.log(f"  Location: {self.source_dir}")
        self.log(f"  Files found: {len(debug_files)}")
        self.log(f"  Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.2f} MB)")

        return True, "Directory verified", debug_files

    def compute_baseline_checksums(self, files: List[Path]) -> Tuple[bool, str]:
        """Compute baseline checksums for all files."""
        self.log("")
        self.log("Step 2/12: Compute baseline checksums for all files...")

        try:
            for filepath in files:
                checksum = self._compute_file_sha256(filepath)
                self.file_checksums[str(filepath)] = checksum

            self.log(f"✓ Baseline checksums computed for {len(files)} files")
            return True, "Checksums computed"
        except Exception as e:
            msg = f"Failed to compute checksums: {e}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg

    def stream_extract_log_messages(self, files: List[Path]) -> Tuple[bool, str, int]:
        """Stream extract meaningful messages from debug logs."""
        self.log("")
        self.log("Step 3/12: Stream extract meaningful messages from debug logs...")

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

        key_regex = re.compile("|".join(key_patterns), re.IGNORECASE)

        line_count = 0
        file_count = 0

        for filepath in files:
            try:
                with open(filepath, "r", errors="ignore") as f:
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
                                "source_type": "debug"
                            })
                            line_count += 1

                file_count += 1

            except Exception as e:
                self.log(f"  Warning: Error reading {filepath.name}: {e}")
                self.errors.append(f"Error reading {filepath.name}: {e}")

        self.log(f"✓ Extracted {line_count} meaningful messages from {file_count} files")
        return True, f"Extracted {line_count} messages", line_count

    def deduplicate_messages(self) -> Tuple[bool, str, int, int]:
        """Deduplicate extracted messages against global store."""
        self.log("")
        self.log("Step 4/12: Deduplicate messages against MEMORY-CONTEXT...")

        new_messages = []
        duplicates = 0

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

        self.log(f"✓ Deduplication complete")
        self.log(f"  New unique messages: {self.new_unique_count}")
        self.log(f"  Duplicate messages: {duplicates}")
        self.log(f"  Total processed: {self.total_processed}")
        self.log(f"  Deduplication rate: {dedup_rate:.1f}%")

        # Keep only new messages for further processing
        self.extracted_messages = new_messages

        return True, "Deduplication complete", self.new_unique_count, duplicates

    def create_session_index(self, files: List[Path]) -> Tuple[bool, str]:
        """Create index mapping messages back to original files."""
        self.log("")
        self.log("Step 5/12: Create session index with full provenance...")

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

            index_file = self.extraction_dir / "session-index.json"
            with open(index_file, "w") as f:
                json.dump(index, f, indent=2, default=str)

            self.log(f"✓ Session index created")
            self.log(f"  Location: {index_file}")
            self.log(f"  Size: {index_file.stat().st_size:,} bytes")

            return True, "Session index created"

        except Exception as e:
            msg = f"Failed to create index: {e}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg

    def save_extracted_messages(self) -> Tuple[bool, str]:
        """Save new unique messages in JSONL format."""
        self.log("")
        self.log("Step 6/12: Save extracted new unique messages...")

        try:
            output_file = self.extraction_dir / "extracted-messages.jsonl"

            with open(output_file, "w") as f:
                for msg in self.extracted_messages:
                    f.write(json.dumps(msg, default=str) + "\n")

            self.log(f"✓ Extracted messages saved")
            self.log(f"  Location: {output_file}")
            self.log(f"  Messages: {len(self.extracted_messages)}")
            self.log(f"  Size: {output_file.stat().st_size:,} bytes")

            return True, "Messages saved"

        except Exception as e:
            msg = f"Failed to save messages: {e}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg

    def verify_post_extraction_checksums(self, files: List[Path]) -> Tuple[bool, str]:
        """Verify all source files unchanged after extraction."""
        self.log("")
        self.log("Step 7/12: Verify all source files unchanged after extraction...")

        try:
            all_match = True

            for filepath in files:
                post_checksum = self._compute_file_sha256(filepath)
                baseline = self.file_checksums[str(filepath)]

                if post_checksum != baseline:
                    self.log(f"✗ {filepath.name}: CHECKSUM MISMATCH!")
                    self.log(f"  Pre:  {baseline}")
                    self.log(f"  Post: {post_checksum}")
                    all_match = False
                else:
                    self.log(f"✓ {filepath.name}: unchanged")

            if all_match:
                self.log(f"✓ All {len(files)} files verified unchanged")
                return True, "All files verified"
            else:
                msg = f"Some files were modified during extraction!"
                self.errors.append(msg)
                return False, msg

        except Exception as e:
            msg = f"Failed to verify checksums: {e}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg

    def save_statistics(self):
        """Save extraction statistics."""
        self.log("")
        self.log("Step 8/12: Save extraction statistics...")

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
            with open(stats_file, "w") as f:
                json.dump(stats, f, indent=2)

            self.log(f"✓ Statistics saved to {stats_file}")

            return True

        except Exception as e:
            self.log(f"ERROR: Failed to save statistics: {e}")
            return False

    def generate_summary(self) -> str:
        """Generate summary report."""
        self.log("")
        self.log("Step 9/12: Generate summary report...")

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

        self.log(summary)
        return summary

    def run(self) -> bool:
        """Execute complete Phase 2 extraction."""
        try:
            # Step 1: Verify source directory
            success, msg, files = self.verify_source_directory()
            if not success:
                return False

            if not files:
                self.log("No debug files found. Skipping Phase 2.")
                return True

            # Step 2: Compute baseline checksums
            success, msg = self.compute_baseline_checksums(files)
            if not success:
                return False

            # Step 3: Stream extract messages
            success, msg, count = self.stream_extract_log_messages(files)
            if not success or count == 0:
                self.log("WARNING: No meaningful messages extracted from debug logs")
                # Don't fail - this is acceptable

            # Step 4: Deduplicate
            success, msg, new_count, dup_count = self.deduplicate_messages()
            if not success:
                return False

            # Step 5: Create session index
            success, msg = self.create_session_index(files)
            if not success:
                return False

            # Step 6: Save messages
            success, msg = self.save_extracted_messages()
            if not success:
                return False

            # Step 7: Verify post-extraction checksums
            success, msg = self.verify_post_extraction_checksums(files)
            if not success:
                return False

            # Step 8: Save statistics
            self.save_statistics()

            # Step 9: Generate summary
            summary = self.generate_summary()

            # Step 10: Final status
            self.log("")
            self.log("Step 10/12: Phase 2 extraction complete")

            if len(self.errors) == 0:
                self.log("✓ ALL STEPS COMPLETED SUCCESSFULLY")
                return True
            else:
                self.log(f"✗ COMPLETED WITH {len(self.errors)} ERRORS")
                for error in self.errors:
                    self.log(f"  - {error}")
                return False

        except Exception as e:
            self.log(f"CRITICAL ERROR: {e}")
            self.errors.append(str(e))
            return False


def main():
    """Run Phase 2 extraction."""
    print("CODITECT Session Memory Extraction - Phase 2: debug/ Logs")
    print("")

    extractor = Phase2DebugExtractor(verbose=True)
    success = extractor.run()

    print("")
    if success:
        print("✅ Phase 2 extraction SUCCESSFUL")
        sys.exit(0)
    else:
        print("❌ Phase 2 extraction FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
