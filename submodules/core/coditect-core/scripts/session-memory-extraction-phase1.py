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
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re


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
        self.extraction_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Initialize state
        self.log_file = self.logs_dir / f"phase1-{datetime.now().isoformat()}.log"
        self.extracted_messages = []
        self.new_unique_count = 0
        self.duplicate_count = 0
        self.total_processed = 0
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

    def verify_source_file(self) -> Tuple[bool, str]:
        """Verify source file exists and is readable."""
        self.log("=" * 80)
        self.log("PHASE 1: history.jsonl EXTRACTION")
        self.log("=" * 80)
        self.log("")

        self.log("Step 1/10: Verify source file...")

        if not self.source_file.exists():
            msg = f"Source file not found: {self.source_file}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg

        if not os.access(self.source_file, os.R_OK):
            msg = f"Source file not readable: {self.source_file}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg

        # Get file size
        file_size = self.source_file.stat().st_size
        self.log(f"✓ Source file exists and is readable")
        self.log(f"  Location: {self.source_file}")
        self.log(f"  Size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")

        return True, "Source file verified"

    def compute_baseline_checksum(self) -> Tuple[bool, str, str]:
        """Compute baseline checksum before processing."""
        self.log("")
        self.log("Step 2/10: Compute baseline checksum...")

        try:
            checksum = self._compute_file_sha256(self.source_file)
            self.log(f"✓ Baseline checksum computed")
            self.log(f"  SHA-256: {checksum}")
            return True, "Checksum computed", checksum
        except Exception as e:
            msg = f"Failed to compute checksum: {e}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg, ""

    def stream_extract_messages(self) -> Tuple[bool, str, int]:
        """Stream extract messages line-by-line from history.jsonl."""
        self.log("")
        self.log("Step 3/10: Stream extract messages from history.jsonl...")

        try:
            line_count = 0
            error_lines = []

            with open(self.source_file, "r") as f:
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
                        self.log(f"  Warning: Malformed JSON at line {line_num}: {e}")

            self.log(f"✓ Extracted {line_count} messages from history.jsonl")

            if error_lines:
                self.log(f"  Note: {len(error_lines)} malformed lines skipped")

            return True, f"Extracted {line_count} messages", line_count

        except Exception as e:
            msg = f"Failed to extract messages: {e}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg, 0

    def deduplicate_messages(self) -> Tuple[bool, str, int, int]:
        """Deduplicate extracted messages against global store."""
        self.log("")
        self.log("Step 4/10: Deduplicate messages against MEMORY-CONTEXT...")

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

    def create_session_index(self) -> Tuple[bool, str]:
        """Create index mapping messages back to original file."""
        self.log("")
        self.log("Step 5/10: Create session index with full provenance...")

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
        self.log("Step 6/10: Save extracted new unique messages...")

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

    def verify_post_extraction_checksum(self, baseline: str) -> Tuple[bool, str]:
        """Verify source file unchanged after extraction."""
        self.log("")
        self.log("Step 7/10: Verify source file unchanged after extraction...")

        try:
            post_checksum = self._compute_file_sha256(self.source_file)

            if post_checksum == baseline:
                self.log(f"✓ Source file integrity verified")
                self.log(f"  Pre-extraction:  {baseline}")
                self.log(f"  Post-extraction: {post_checksum}")
                self.log(f"  Status: UNCHANGED ✓")
                return True, "Checksum verification passed"
            else:
                msg = f"Source file was modified during extraction!"
                self.log(f"ERROR: {msg}")
                self.log(f"  Pre-extraction:  {baseline}")
                self.log(f"  Post-extraction: {post_checksum}")
                self.errors.append(msg)
                return False, msg

        except Exception as e:
            msg = f"Failed to verify checksum: {e}"
            self.log(f"ERROR: {msg}")
            self.errors.append(msg)
            return False, msg

    def save_statistics(self):
        """Save extraction statistics."""
        self.log("")
        self.log("Step 8/10: Save extraction statistics...")

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
        self.log("Step 9/10: Generate summary report...")

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

        self.log(summary)
        return summary

    def run(self) -> bool:
        """Execute complete Phase 1 extraction."""
        try:
            # Step 1: Verify source file
            success, msg = self.verify_source_file()
            if not success:
                return False

            # Step 2: Compute baseline checksum
            success, msg, baseline = self.compute_baseline_checksum()
            if not success:
                return False

            # Step 3: Stream extract messages
            success, msg, count = self.stream_extract_messages()
            if not success or count == 0:
                self.log("ERROR: No messages extracted from source file")
                return False

            # Step 4: Deduplicate
            success, msg, new_count, dup_count = self.deduplicate_messages()
            if not success:
                return False

            # Step 5: Create session index
            success, msg = self.create_session_index()
            if not success:
                return False

            # Step 6: Save messages
            success, msg = self.save_extracted_messages()
            if not success:
                return False

            # Step 7: Verify post-extraction checksum
            success, msg = self.verify_post_extraction_checksum(baseline)
            if not success:
                return False

            # Step 8: Save statistics
            self.save_statistics()

            # Step 9: Generate summary
            summary = self.generate_summary()

            # Step 10: Final status
            self.log("")
            self.log("Step 10/10: Phase 1 extraction complete")

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
    """Run Phase 1 extraction."""
    print("CODITECT Session Memory Extraction - Phase 1: history.jsonl")
    print("")

    extractor = SessionMemoryExtractor(verbose=True)
    success = extractor.run()

    print("")
    if success:
        print("✅ Phase 1 extraction SUCCESSFUL")
        sys.exit(0)
    else:
        print("❌ Phase 1 extraction FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
