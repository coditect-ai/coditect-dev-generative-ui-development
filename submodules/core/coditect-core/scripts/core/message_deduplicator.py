#!/usr/bin/env python3
"""
Global Message-Level Deduplicator

Simple deduplication system that only cares about unique message content.
No session tracking - just one global pool of all unique messages ever seen.

Key principle: If we've seen this exact message content before, it's a duplicate.
Period. No complex session detection needed.

Usage:
    dedup = MessageDeduplicator(storage_dir='dedup_state')

    # Process any export - no session ID needed!
    new_messages, stats = dedup.process_export(export_data)

    # Optional: Link to checkpoint for organization
    new_messages, stats = dedup.process_export(
        export_data,
        checkpoint_id="week1-day2"  # For your reference only
    )

Author: Claude + AZ1.AI
License: MIT
"""

import hashlib
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Setup dual logging (stdout + file)
log_dir = Path(__file__).parent.parent.parent / "MEMORY-CONTEXT" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "message_deduplicator.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# Custom Exception Hierarchy
# ============================================================================

class DeduplicationError(Exception):
    """Base exception for deduplication errors."""
    pass


class StorageError(DeduplicationError):
    """Raised when storage operations fail."""
    pass


class ParseError(DeduplicationError):
    """Raised when export parsing fails."""
    pass


class MessageDeduplicator:
    """
    Global message-level deduplication.

    Maintains ONE global pool of all unique message hashes.
    Any duplicate content from ANY export is caught and filtered.

    Storage:
        global_hashes.json - Set of all unique message content hashes
        unique_messages.jsonl - Append-only log of unique messages
        checkpoint_index.json - Optional mapping of checkpoints to message hashes
    """

    def __init__(self, storage_dir: str):
        """
        Initialize deduplicator with persistent storage directory.

        Args:
            storage_dir: Path to directory for state files

        Raises:
            StorageError: If storage directory cannot be created or accessed
        """
        try:
            self.storage_dir = Path(storage_dir)
            self.storage_dir.mkdir(parents=True, exist_ok=True)

            # Global state files
            self.hashes_file = self.storage_dir / "global_hashes.json"
            self.messages_file = self.storage_dir / "unique_messages.jsonl"
            self.checkpoint_index_file = self.storage_dir / "checkpoint_index.json"

            # Load global hash pool
            hashes_data = self._load_json(self.hashes_file, default=[])
            self.global_hashes = set(hashes_data)

            # Load checkpoint index (optional organizational metadata)
            self.checkpoint_index = self._load_json(self.checkpoint_index_file, default={})

            logger.info(f"MessageDeduplicator initialized with storage at {self.storage_dir}")
            logger.info(f"Loaded {len(self.global_hashes)} unique message hashes")
            logger.info(f"Tracking {len(self.checkpoint_index)} checkpoints")

        except OSError as e:
            logger.error(f"Failed to create storage directory: {e}")
            raise StorageError(f"Could not create storage directory: {e}") from e
        except Exception as e:
            logger.error(f"Failed to initialize deduplicator: {e}")
            raise

    def process_export(
        self,
        export_data: Dict[str, Any],
        checkpoint_id: Optional[str] = None,
        dry_run: bool = False
    ) -> Tuple[List[Dict], Dict[str, Any]]:
        """
        Process export and return only new unique messages.

        Args:
            export_data: Export dict with 'messages' array
            checkpoint_id: Optional checkpoint/commit to link messages to
            dry_run: If True, don't save state (for testing)

        Returns:
            Tuple of (new_messages, statistics)

        Raises:
            ParseError: If export data is invalid
        """
        try:
            # Validate export data
            if not export_data or 'messages' not in export_data:
                raise ParseError("Export data must contain 'messages' array")

            messages = export_data.get("messages", [])
            new_messages = []
            duplicates = 0
            checkpoint_hashes = []

            logger.info(f"Processing export")
            logger.info(f"  Messages in export: {len(messages)}")
            logger.info(f"  Global unique hashes: {len(self.global_hashes)}")
            if checkpoint_id:
                logger.info(f"  Checkpoint ID: {checkpoint_id}")

            for msg in messages:
                # Hash message content
                content_hash = self._hash_message(msg)

                # Check global pool
                if content_hash in self.global_hashes:
                    duplicates += 1
                    continue  # Already seen this exact message

                # New unique message!
                new_messages.append(msg)
                self.global_hashes.add(content_hash)
                checkpoint_hashes.append(content_hash)

                # Append to log (if not dry run)
                if not dry_run:
                    self._append_message(msg, content_hash, checkpoint_id)

            # Update state (if not dry run)
            if not dry_run and new_messages:
                self._save_hashes()

                # Update checkpoint index if checkpoint_id provided
                if checkpoint_id and checkpoint_hashes:
                    if checkpoint_id not in self.checkpoint_index:
                        self.checkpoint_index[checkpoint_id] = {
                            'created': datetime.now(timezone.utc).isoformat(),
                            'message_hashes': []
                        }
                    self.checkpoint_index[checkpoint_id]['message_hashes'].extend(checkpoint_hashes)
                    self._save_checkpoint_index()

            # Generate statistics
            stats = {
                'total_messages': len(messages),
                'new_unique': len(new_messages),
                'duplicates_filtered': duplicates,
                'dedup_rate': (duplicates / len(messages) * 100) if len(messages) > 0 else 0,
                'global_unique_count': len(self.global_hashes)
            }

            logger.info("Processing complete:")
            logger.info(f"  New unique messages: {stats['new_unique']}")
            logger.info(f"  Duplicates filtered: {stats['duplicates_filtered']}")
            logger.info(f"  Deduplication rate: {stats['dedup_rate']:.1f}%")
            logger.info(f"  Total unique messages globally: {stats['global_unique_count']}")

            return new_messages, stats

        except ParseError:
            raise
        except Exception as e:
            logger.error(f"Failed to process export: {e}")
            raise ParseError(f"Export processing failed: {e}") from e

    def _hash_message(self, message: Dict[str, Any]) -> str:
        """
        Create SHA-256 hash of message content.

        Normalizes message to focus on content, ignoring metadata like timestamps.
        """
        try:
            # Normalize message (only hash the actual content)
            normalized = {
                'role': message.get('role') or message.get('type', 'unknown'),
                'content': message.get('content') or message.get('message', '')
            }

            content_str = json.dumps(normalized, sort_keys=True)
            return hashlib.sha256(content_str.encode()).hexdigest()

        except Exception as e:
            logger.error(f"Failed to hash message: {e}")
            # Return a fallback hash based on string representation
            return hashlib.sha256(str(message).encode()).hexdigest()

    def _append_message(
        self,
        message: Dict[str, Any],
        content_hash: str,
        checkpoint_id: Optional[str] = None
    ) -> None:
        """
        Append unique message to append-only log.

        Args:
            message: Message dict
            content_hash: Pre-computed content hash
            checkpoint_id: Optional checkpoint this message belongs to

        Raises:
            StorageError: If append fails
        """
        entry = {
            'hash': content_hash,
            'message': message,
            'first_seen': datetime.now(timezone.utc).isoformat(),
            'checkpoint': checkpoint_id
        }

        try:
            with open(self.messages_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except IOError as e:
            logger.error(f"Failed to append message to log: {e}")
            raise StorageError(f"Could not append to log: {e}") from e

    def _save_hashes(self) -> None:
        """
        Save global hash pool to disk.

        Raises:
            StorageError: If save fails
        """
        try:
            with open(self.hashes_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.global_hashes), f)
        except IOError as e:
            logger.error(f"Failed to save hashes: {e}")
            raise StorageError(f"Could not save hashes: {e}") from e

    def _save_checkpoint_index(self) -> None:
        """
        Save checkpoint index to disk.

        Raises:
            StorageError: If save fails
        """
        try:
            with open(self.checkpoint_index_file, 'w', encoding='utf-8') as f:
                json.dump(self.checkpoint_index, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save checkpoint index: {e}")
            raise StorageError(f"Could not save checkpoint index: {e}") from e

    def _load_json(self, filepath: Path, default=None):
        """
        Load JSON file with error handling.

        Args:
            filepath: Path to JSON file
            default: Default value if file doesn't exist or is invalid

        Returns:
            Loaded JSON data or default
        """
        if not filepath.exists():
            return default if default is not None else {}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse {filepath}: {e}. Using default.")
            return default if default is not None else {}
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}. Using default.")
            return default if default is not None else {}

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get global deduplication statistics.

        Returns:
            Dict with global stats
        """
        return {
            'total_unique_messages': len(self.global_hashes),
            'checkpoints_tracked': len(self.checkpoint_index),
            'storage_dir': str(self.storage_dir)
        }

    def get_checkpoint_messages(self, checkpoint_id: str) -> List[str]:
        """
        Get message hashes for a specific checkpoint.

        Args:
            checkpoint_id: Checkpoint identifier

        Returns:
            List of message hashes for this checkpoint
        """
        if checkpoint_id not in self.checkpoint_index:
            return []

        return self.checkpoint_index[checkpoint_id].get('message_hashes', [])

    def get_all_checkpoints(self) -> List[str]:
        """Get list of all tracked checkpoint IDs"""
        return list(self.checkpoint_index.keys())


# Backward compatibility: Import the old parser functions
def parse_claude_export_file(filepath: Path) -> Dict[str, Any]:
    """
    Parse Claude Code conversation export file.

    Claude exports are text-based with special markers:
    - ⏺ = User message/action
    - ⎿ = Assistant response/tool result

    Args:
        filepath: Path to export file

    Returns:
        Dict with 'messages' array containing parsed conversation

    Raises:
        ParseError: If file cannot be parsed
    """
    try:
        logger.info(f"Parsing Claude export: {filepath}")

        if not filepath.exists():
            raise ParseError(f"Export file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        messages = []
        current_message = None
        current_content = []
        index = 0

        for line in lines:
            # User message/action marker
            if line.startswith("⏺"):
                # Save previous message if exists
                if current_message is not None:
                    current_message["content"] = "".join(current_content).strip()
                    messages.append(current_message)
                    index += 1

                # Start new user message
                current_message = {"index": index, "role": "user", "type": "user"}
                current_content = [line[2:]]  # Remove marker

            # Assistant response marker
            elif line.strip().startswith("⎿"):
                # Save previous message if exists
                if current_message is not None:
                    current_message["content"] = "".join(current_content).strip()
                    messages.append(current_message)
                    index += 1

                # Start new assistant message
                current_message = {"index": index, "role": "assistant", "type": "assistant"}
                current_content = [line.strip()[2:]]  # Remove marker and whitespace

            # Continuation of current message
            else:
                if current_message is not None:
                    current_content.append(line)

        # Save final message
        if current_message is not None:
            current_message["content"] = "".join(current_content).strip()
            messages.append(current_message)

        logger.info(f"Parsed {len(messages)} messages from export")

        return {"messages": messages}

    except IOError as e:
        logger.error(f"Failed to read export file: {e}")
        raise ParseError(f"Could not read export file: {e}") from e
    except Exception as e:
        logger.error(f"Failed to parse export file: {e}")
        raise ParseError(f"Export parsing failed: {e}") from e


if __name__ == "__main__":
    # Simple CLI for testing
    import argparse

    parser = argparse.ArgumentParser(description="Message Deduplicator")
    parser.add_argument("--file", "-f", required=True, help="Export file to process")
    parser.add_argument("--storage-dir", "-d", default="dedup_state", help="Storage directory")
    parser.add_argument("--checkpoint", "-c", help="Optional checkpoint ID")
    parser.add_argument("--dry-run", action="store_true", help="Don't save state")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    try:
        # Initialize
        dedup = MessageDeduplicator(args.storage_dir)

        # Parse export
        export_data = parse_claude_export_file(Path(args.file))

        # Process
        new_messages, stats = dedup.process_export(
            export_data,
            checkpoint_id=args.checkpoint,
            dry_run=args.dry_run
        )

        # Print results
        print(f"\nResults:")
        print(f"  Total messages: {stats['total_messages']}")
        print(f"  New unique: {stats['new_unique']}")
        print(f"  Duplicates: {stats['duplicates_filtered']}")
        print(f"  Dedup rate: {stats['dedup_rate']:.1f}%")
        print(f"  Global unique: {stats['global_unique_count']}")

        logger.info("Deduplication completed successfully")
        sys.exit(0)

    except ParseError as e:
        print(f"\n❌ Parse Error: {e}")
        logger.error(f"Parse error: {e}")
        sys.exit(1)

    except StorageError as e:
        print(f"\n❌ Storage Error: {e}")
        logger.error(f"Storage error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        logger.warning("Interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\nLog file: {log_file}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        logger.exception("Unexpected error during deduplication")
        sys.exit(1)
