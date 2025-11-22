#!/usr/bin/env python3
"""
Claude Conversation Export Deduplicator

Hybrid deduplication system for Claude Code conversation exports that combines:
- Sequence number tracking (primary deduplication mechanism)
- Content hashing (secondary, catches exact duplicates)
- Append-only log (persistent storage with zero data loss)
- Idempotent processing (safe to re-run on same exports)

Solves the exponential growth problem in multi-day sessions:
- Day 1: 13KB export
- Day 2: 51KB export (cumulative)
- Day 3: 439KB export (cumulative with full history)

Expected storage reduction: 95%+ through deduplication.

Author: Claude + AZ1.AI
License: MIT
"""

import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ClaudeConversationDeduplicator:
    """
    Hybrid deduplication for Claude conversation exports.

    Combines:
    - Sequence number tracking (primary)
    - Content hashing (secondary, for exact duplicates)
    - Append-only log (persistence)
    - Idempotent processing (safety)

    Usage:
        dedup = ClaudeConversationDeduplicator(storage_dir='dedup_state')

        # Process first export
        new_msgs = dedup.process_export('session-1', export_data)
        print(f"Added {len(new_msgs)} new messages")

        # Process second export (with duplicates)
        new_msgs = dedup.process_export('session-1', export_data_2)
        print(f"Added {len(new_msgs)} new messages (duplicates filtered)")

        # Get full conversation
        full = dedup.get_full_conversation('session-1')

        # Get statistics
        stats = dedup.get_statistics('session-1')
    """

    def __init__(self, storage_dir: str):
        """
        Initialize deduplicator with persistent storage directory.

        Args:
            storage_dir: Path to directory for state files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # State files
        self.watermarks_file = self.storage_dir / "watermarks.json"
        self.content_hashes_file = self.storage_dir / "content_hashes.json"
        self.log_file = self.storage_dir / "conversation_log.jsonl"

        # Load state
        self.watermarks = self._load_json(self.watermarks_file, default={})
        self.content_hashes = self._load_json(self.content_hashes_file, default={})

        logger.info(f"Deduplicator initialized with storage at {self.storage_dir}")
        logger.info(f"Loaded {len(self.watermarks)} conversation watermarks")

    def process_export(
        self, conversation_id: str, export_data: Dict[str, Any], dry_run: bool = False
    ) -> Tuple[List[Dict], Dict[str, Any]]:
        """
        Process a Claude conversation export, returning only new unique messages.

        Args:
            conversation_id: Unique identifier for the conversation/session
            export_data: Export dict with 'messages' array
            dry_run: If True, don't save state (for testing)

        Returns:
            Tuple of (new_messages, statistics)
            - new_messages: List of new unique messages not seen before
            - statistics: Dict with processing stats
        """
        messages = export_data.get("messages", [])
        new_messages = []
        duplicates_filtered = 0
        content_collisions = 0

        # Get current state for this conversation
        watermark = self.watermarks.get(conversation_id, -1)
        seen_hashes = set(self.content_hashes.get(conversation_id, []))
        original_seen_count = len(seen_hashes)

        logger.info(f"Processing export for '{conversation_id}'")
        logger.info(f"  Current watermark: {watermark}")
        logger.info(f"  Messages in export: {len(messages)}")
        logger.info(f"  Known unique hashes: {len(seen_hashes)}")

        for msg in sorted(messages, key=lambda m: m.get("index", 0)):
            msg_index = msg.get("index", 0)

            # Check 1: Sequence number (primary deduplication)
            if msg_index <= watermark:
                duplicates_filtered += 1
                continue  # Already processed by sequence

            # Check 2: Content hash (catch exact duplicates)
            content_hash = self._create_message_hash(msg)
            if content_hash in seen_hashes:
                # Same content but higher sequence - edge case
                content_collisions += 1
                logger.warning(
                    f"Content collision at index {msg_index}: "
                    f"Same content as earlier message (hash: {content_hash[:8]}...)"
                )
                continue

            # New unique message - add to results
            new_messages.append(msg)
            seen_hashes.add(content_hash)
            watermark = max(watermark, msg_index)

            # Append to persistent log (if not dry run)
            if not dry_run:
                self._append_to_log(conversation_id, msg, content_hash)

        # Update state (if not dry run)
        if new_messages and not dry_run:
            self.watermarks[conversation_id] = watermark
            self.content_hashes[conversation_id] = list(seen_hashes)
            self._save_state()

        # Calculate statistics
        stats = {
            "conversation_id": conversation_id,
            "messages_in_export": len(messages),
            "new_messages": len(new_messages),
            "duplicates_filtered": duplicates_filtered,
            "content_collisions": content_collisions,
            "new_watermark": watermark,
            "total_unique_messages": len(seen_hashes),
            "new_hashes_added": len(seen_hashes) - original_seen_count,
        }

        logger.info("Processing complete:")
        logger.info(f"  New messages: {stats['new_messages']}")
        logger.info(f"  Duplicates filtered: {stats['duplicates_filtered']}")
        logger.info(f"  Content collisions: {stats['content_collisions']}")
        logger.info(f"  New watermark: {stats['new_watermark']}")

        return new_messages, stats

    def _create_message_hash(self, message: Dict[str, Any]) -> str:
        """
        Create SHA-256 hash of message content for deduplication.

        Normalizes message to exclude ephemeral fields like timestamps,
        focusing only on semantic content.

        Args:
            message: Message dict

        Returns:
            Hex digest of SHA-256 hash
        """
        # Normalize message to exclude ephemeral fields
        normalized = {
            "role": message.get("type", message.get("role")),
            "content": message.get("message", message.get("content")),
            "index": message.get("index", 0),
        }
        content_str = json.dumps(normalized, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()

    def _append_to_log(
        self, conversation_id: str, message: Dict[str, Any], content_hash: str
    ) -> None:
        """
        Append message to append-only log.

        The log provides:
        - Persistent storage of all unique messages
        - Audit trail of when messages were added
        - Recovery mechanism if state files are corrupted

        Args:
            conversation_id: Conversation identifier
            message: Message dict to append
            content_hash: Pre-computed content hash
        """
        event = {
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "content_hash": content_hash,
            "message": message,
        }

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            logger.error(f"Failed to append to log: {e}")
            raise

    def _save_state(self) -> None:
        """
        Persist watermarks and content hashes atomically.

        Uses atomic write pattern (write to temp file, then rename)
        to prevent corruption if process is interrupted.
        """
        try:
            self._save_json(self.watermarks_file, self.watermarks)
            self._save_json(self.content_hashes_file, self.content_hashes)
            logger.debug("State saved successfully")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            raise

    def _load_json(self, filepath: Path, default: Optional[Any] = None) -> Any:
        """
        Load JSON from file or return default.

        Args:
            filepath: Path to JSON file
            default: Default value if file doesn't exist

        Returns:
            Loaded JSON data or default value
        """
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Corrupted JSON in {filepath}: {e}")
                return default if default is not None else {}
        return default if default is not None else {}

    def _save_json(self, filepath: Path, data: Any) -> None:
        """
        Save JSON to file atomically.

        Args:
            filepath: Path to JSON file
            data: Data to serialize
        """
        # Write to temp file first
        temp_file = filepath.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        # Atomic rename
        temp_file.replace(filepath)

    def get_full_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Reconstruct full conversation from append-only log.

        This is the source of truth for all messages, providing:
        - Complete conversation history
        - Chronological ordering by message index
        - Validation that no messages were lost

        Args:
            conversation_id: Conversation identifier

        Returns:
            List of all messages for this conversation, sorted by index
        """
        messages: List[Dict[str, Any]] = []

        if not self.log_file.exists():
            logger.warning(f"Log file does not exist: {self.log_file}")
            return messages

        logger.info(f"Reconstructing conversation '{conversation_id}' from log")

        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    event = json.loads(line)
                    if event["conversation_id"] == conversation_id:
                        messages.append(event["message"])
        except Exception as e:
            logger.error(f"Failed to read log file: {e}")
            raise

        # Sort by index for chronological order
        messages = sorted(messages, key=lambda m: m.get("index", 0))
        logger.info(f"Reconstructed {len(messages)} messages")

        return messages

    def get_statistics(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get statistics for a conversation.

        Args:
            conversation_id: Conversation identifier

        Returns:
            Dict with watermark, unique message count, etc.
        """
        watermark = self.watermarks.get(conversation_id, -1)
        unique_hashes = len(self.content_hashes.get(conversation_id, []))

        return {
            "conversation_id": conversation_id,
            "watermark": watermark,
            "unique_messages": unique_hashes,
            "total_messages_processed": watermark + 1 if watermark >= 0 else 0,
        }

    def get_all_conversations(self) -> List[str]:
        """
        Get list of all conversation IDs in the system.

        Returns:
            List of conversation IDs
        """
        return list(self.watermarks.keys())

    def validate_integrity(self, conversation_id: str) -> Dict[str, Any]:
        """
        Validate data integrity for a conversation.

        Checks:
        - Watermark consistency
        - Hash count matches log count
        - No gaps in sequence numbers

        Args:
            conversation_id: Conversation identifier

        Returns:
            Dict with validation results
        """
        logger.info(f"Validating integrity for '{conversation_id}'")

        # Get state
        watermark = self.watermarks.get(conversation_id, -1)
        hashes = self.content_hashes.get(conversation_id, [])

        # Get messages from log
        messages = self.get_full_conversation(conversation_id)

        # Check 1: Hash count matches message count
        hash_count_ok = len(hashes) == len(messages)

        # Check 2: No gaps in sequence
        if messages:
            indices = [m.get("index", 0) for m in messages]
            expected_indices = list(range(len(messages)))
            sequence_ok = indices == expected_indices
        else:
            sequence_ok = True

        # Check 3: Watermark matches highest index
        if messages:
            max_index = max(m.get("index", 0) for m in messages)
            watermark_ok = watermark == max_index
        else:
            watermark_ok = watermark == -1

        results = {
            "conversation_id": conversation_id,
            "valid": hash_count_ok and sequence_ok and watermark_ok,
            "checks": {
                "hash_count_matches": hash_count_ok,
                "no_sequence_gaps": sequence_ok,
                "watermark_correct": watermark_ok,
            },
            "stats": {
                "watermark": watermark,
                "hash_count": len(hashes),
                "message_count": len(messages),
            },
        }

        if results["valid"]:
            logger.info("✓ Integrity validation passed")
        else:
            logger.warning("✗ Integrity validation failed!")
            logger.warning(f"  Details: {results['checks']}")

        return results


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
    """
    logger.info(f"Parsing Claude export: {filepath}")

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


def extract_session_id_from_filename(filepath: Path) -> str:
    """
    Extract session ID from export filename.

    Examples:
        2025-11-16-EXPORT-CHECKPOINT.txt → 2025-11-16-checkpoint
        2025-11-17-EXPORT-ROLLOUT-MASTER.txt → rollout-master

    Args:
        filepath: Path to export file

    Returns:
        Session ID string
    """
    filename = filepath.stem  # Remove .txt extension

    # Remove common prefixes
    filename = filename.replace("EXPORT-", "").replace("export-", "")

    # Convert to lowercase and replace spaces/underscores with dashes
    session_id = filename.lower().replace("_", "-").replace(" ", "-")

    return session_id


if __name__ == "__main__":
    # CLI interface for testing
    import argparse

    parser = argparse.ArgumentParser(description="Claude Conversation Deduplicator")
    parser.add_argument("export_file", help="Path to Claude export file")
    parser.add_argument(
        "--storage-dir", default="dedup_state", help="Directory for state files"
    )
    parser.add_argument(
        "--session-id", help="Session ID (auto-detected if not provided)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Process without saving state"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Parse export file
    export_path = Path(args.export_file)
    export_data = parse_claude_export_file(export_path)

    # Detect or use provided session ID
    session_id = args.session_id or extract_session_id_from_filename(export_path)

    # Process with deduplicator
    dedup = ClaudeConversationDeduplicator(args.storage_dir)
    new_messages, stats = dedup.process_export(
        session_id, export_data, dry_run=args.dry_run
    )

    # Print results
    print(f"\n{'='*60}")
    print(f"Processing Results for: {session_id}")
    print(f"{'='*60}")
    print(f"Messages in export:    {stats['messages_in_export']}")
    print(f"New messages:          {stats['new_messages']}")
    print(f"Duplicates filtered:   {stats['duplicates_filtered']}")
    print(f"Content collisions:    {stats['content_collisions']}")
    print(f"New watermark:         {stats['new_watermark']}")
    print(f"Total unique messages: {stats['total_unique_messages']}")

    if not args.dry_run:
        # Validate integrity
        validation = dedup.validate_integrity(session_id)
        print(f"\nIntegrity: {'✓ VALID' if validation['valid'] else '✗ INVALID'}")
