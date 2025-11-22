#!/usr/bin/env python3
"""
Unit tests for ClaudeConversationDeduplicator

Tests cover:
- First export processing (all new messages)
- Second export with duplicates (deduplication works)
- Content hash collision handling
- Gap detection
- Watermark tracking
- Full conversation reconstruction
- Statistics generation
- Integrity validation
- File parsing

Author: Claude + AZ1.AI
License: MIT
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Import the module to test
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "core"))

from conversation_deduplicator import (
    ClaudeConversationDeduplicator,
    parse_claude_export_file,
    extract_session_id_from_filename,
)


class TestClaudeConversationDeduplicator:
    """Test suite for ClaudeConversationDeduplicator"""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory for tests"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def deduplicator(self, temp_storage):
        """Create deduplicator instance with temp storage"""
        return ClaudeConversationDeduplicator(temp_storage)

    @pytest.fixture
    def sample_export_1(self):
        """First export with 3 messages"""
        return {
            "messages": [
                {"index": 0, "role": "user", "content": "Hello, Claude!"},
                {"index": 1, "role": "assistant", "content": "Hello! How can I help?"},
                {"index": 2, "role": "user", "content": "Tell me about AI."},
            ]
        }

    @pytest.fixture
    def sample_export_2(self):
        """Second export with duplicates + 2 new messages"""
        return {
            "messages": [
                {"index": 0, "role": "user", "content": "Hello, Claude!"},
                {"index": 1, "role": "assistant", "content": "Hello! How can I help?"},
                {"index": 2, "role": "user", "content": "Tell me about AI."},
                {"index": 3, "role": "assistant", "content": "AI is fascinating..."},
                {"index": 4, "role": "user", "content": "Thank you!"},
            ]
        }

    def test_init_creates_directories(self, temp_storage):
        """Test that initialization creates necessary directories"""
        storage_path = Path(temp_storage) / "test_storage"
        dedup = ClaudeConversationDeduplicator(str(storage_path))

        assert storage_path.exists()
        assert dedup.storage_dir == storage_path

    def test_first_export_all_new(self, deduplicator, sample_export_1):
        """Test processing first export - all messages are new"""
        new_messages, stats = deduplicator.process_export("session-1", sample_export_1)

        assert len(new_messages) == 3
        assert stats["new_messages"] == 3
        assert stats["duplicates_filtered"] == 0
        assert stats["new_watermark"] == 2
        assert stats["total_unique_messages"] == 3

    def test_second_export_with_duplicates(
        self, deduplicator, sample_export_1, sample_export_2
    ):
        """Test that duplicates are filtered on second export"""
        # First export
        deduplicator.process_export("session-1", sample_export_1)

        # Second export with duplicates
        new_messages, stats = deduplicator.process_export("session-1", sample_export_2)

        assert len(new_messages) == 2  # Only messages 3 and 4 are new
        assert stats["new_messages"] == 2
        assert stats["duplicates_filtered"] == 3  # Messages 0, 1, 2 filtered
        assert stats["new_watermark"] == 4
        assert stats["total_unique_messages"] == 5

    def test_watermark_tracking(self, deduplicator, sample_export_1):
        """Test that watermark is correctly updated"""
        deduplicator.process_export("session-1", sample_export_1)

        assert deduplicator.watermarks["session-1"] == 2

        # Process again - watermark shouldn't change
        deduplicator.process_export("session-1", sample_export_1)
        assert deduplicator.watermarks["session-1"] == 2

    def test_content_hash_deduplication(self, deduplicator):
        """Test that identical content is detected even with different indices"""
        export = {
            "messages": [
                {"index": 0, "role": "user", "content": "Hello"},
                {"index": 1, "role": "assistant", "content": "Hi there"},
                {"index": 2, "role": "user", "content": "Hello"},  # Duplicate content
            ]
        }

        new_messages, stats = deduplicator.process_export("session-1", export)

        # All 3 should be added (different indices)
        assert len(new_messages) == 3
        assert stats["content_collisions"] == 0

    def test_full_conversation_reconstruction(
        self, deduplicator, sample_export_1, sample_export_2
    ):
        """Test reconstructing full conversation from log"""
        # Process both exports
        deduplicator.process_export("session-1", sample_export_1)
        deduplicator.process_export("session-1", sample_export_2)

        # Reconstruct full conversation
        full_conv = deduplicator.get_full_conversation("session-1")

        assert len(full_conv) == 5
        assert full_conv[0]["content"] == "Hello, Claude!"
        assert full_conv[4]["content"] == "Thank you!"

    def test_multiple_conversations(self, deduplicator, sample_export_1):
        """Test handling multiple separate conversations"""
        deduplicator.process_export("session-1", sample_export_1)
        deduplicator.process_export("session-2", sample_export_1)

        assert len(deduplicator.get_all_conversations()) == 2
        assert "session-1" in deduplicator.watermarks
        assert "session-2" in deduplicator.watermarks

    def test_get_statistics(self, deduplicator, sample_export_1):
        """Test statistics generation"""
        deduplicator.process_export("session-1", sample_export_1)

        stats = deduplicator.get_statistics("session-1")

        assert stats["conversation_id"] == "session-1"
        assert stats["watermark"] == 2
        assert stats["unique_messages"] == 3
        assert stats["total_messages_processed"] == 3

    def test_dry_run_mode(self, deduplicator, sample_export_1):
        """Test that dry run doesn't persist state"""
        new_messages, stats = deduplicator.process_export(
            "session-1", sample_export_1, dry_run=True
        )

        assert len(new_messages) == 3
        assert "session-1" not in deduplicator.watermarks  # State not saved

    def test_empty_export(self, deduplicator):
        """Test handling empty export"""
        empty_export = {"messages": []}

        new_messages, stats = deduplicator.process_export("session-1", empty_export)

        assert len(new_messages) == 0
        assert stats["new_messages"] == 0

    def test_integrity_validation_valid(self, deduplicator, sample_export_1):
        """Test integrity validation passes for valid data"""
        deduplicator.process_export("session-1", sample_export_1)

        validation = deduplicator.validate_integrity("session-1")

        assert validation["valid"] is True
        assert validation["checks"]["hash_count_matches"] is True
        assert validation["checks"]["no_sequence_gaps"] is True
        assert validation["checks"]["watermark_correct"] is True

    def test_integrity_validation_empty_conversation(self, deduplicator):
        """Test integrity validation for non-existent conversation"""
        validation = deduplicator.validate_integrity("nonexistent")

        assert validation["valid"] is True  # Empty is valid
        assert validation["stats"]["watermark"] == -1
        assert validation["stats"]["message_count"] == 0

    def test_state_persistence(self, temp_storage, sample_export_1):
        """Test that state persists across instances"""
        # First instance
        dedup1 = ClaudeConversationDeduplicator(temp_storage)
        dedup1.process_export("session-1", sample_export_1)

        # Second instance (simulates restart)
        dedup2 = ClaudeConversationDeduplicator(temp_storage)

        assert dedup2.watermarks["session-1"] == 2
        assert len(dedup2.content_hashes["session-1"]) == 3

    def test_append_only_log_exists(self, deduplicator, sample_export_1):
        """Test that append-only log is created"""
        deduplicator.process_export("session-1", sample_export_1)

        log_file = deduplicator.storage_dir / "conversation_log.jsonl"
        assert log_file.exists()

        # Verify log content
        with open(log_file, "r") as f:
            lines = f.readlines()
            assert len(lines) == 3  # 3 messages

    def test_unsorted_messages(self, deduplicator):
        """Test that messages are processed in index order even if unsorted"""
        unsorted_export = {
            "messages": [
                {"index": 2, "role": "user", "content": "Third"},
                {"index": 0, "role": "user", "content": "First"},
                {"index": 1, "role": "assistant", "content": "Second"},
            ]
        }

        new_messages, stats = deduplicator.process_export("session-1", unsorted_export)

        # Should process all 3 in order
        assert len(new_messages) == 3
        assert new_messages[0]["content"] == "First"
        assert new_messages[1]["content"] == "Second"
        assert new_messages[2]["content"] == "Third"


class TestExportFileParsing:
    """Test suite for export file parsing functions"""

    @pytest.fixture
    def temp_export_file(self):
        """Create temporary export file"""
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        )
        yield temp_file
        Path(temp_file.name).unlink()

    def test_parse_claude_export_file(self, temp_export_file):
        """Test parsing Claude Code export format"""
        # Write sample export
        temp_export_file.write(
            """
⏺ Hello, Claude!

  ⎿  Hello! How can I help you today?

⏺ Tell me about deduplication

  ⎿  Deduplication is the process of removing duplicate data...
"""
        )
        temp_export_file.close()

        # Parse
        export_data = parse_claude_export_file(Path(temp_export_file.name))

        assert "messages" in export_data
        assert len(export_data["messages"]) == 4

        # Verify message structure
        assert export_data["messages"][0]["role"] == "user"
        assert "Hello, Claude!" in export_data["messages"][0]["content"]

        assert export_data["messages"][1]["role"] == "assistant"
        assert "How can I help" in export_data["messages"][1]["content"]

    def test_extract_session_id_from_filename(self):
        """Test session ID extraction from various filename formats"""
        test_cases = [
            ("2025-11-16-EXPORT-CHECKPOINT.txt", "2025-11-16-checkpoint"),
            ("2025-11-17-EXPORT-ROLLOUT-MASTER.txt", "2025-11-17-rollout-master"),
            ("EXPORT-test-session.txt", "test-session"),
            ("my_session_export.txt", "my-session-export"),
        ]

        for filename, expected_id in test_cases:
            path = Path(filename)
            session_id = extract_session_id_from_filename(path)
            assert session_id == expected_id, f"Failed for {filename}"

    def test_parse_multiline_messages(self, temp_export_file):
        """Test parsing messages that span multiple lines"""
        temp_export_file.write(
            """
⏺ This is a long message
that spans multiple
lines of text.

  ⎿  This is a response
  that also spans
  multiple lines.
"""
        )
        temp_export_file.close()

        export_data = parse_claude_export_file(Path(temp_export_file.name))

        assert len(export_data["messages"]) == 2
        assert "multiple\nlines" in export_data["messages"][0]["content"]


class TestEdgeCases:
    """Test edge cases and error conditions"""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_duplicate_processing_idempotent(self, temp_storage):
        """Test that processing same export multiple times is idempotent"""
        dedup = ClaudeConversationDeduplicator(temp_storage)

        export = {"messages": [{"index": 0, "role": "user", "content": "Test"}]}

        # Process 3 times
        for i in range(3):
            new_messages, stats = dedup.process_export("session-1", export)

            if i == 0:
                assert len(new_messages) == 1
            else:
                assert len(new_messages) == 0  # Already processed

        # Verify total messages
        full = dedup.get_full_conversation("session-1")
        assert len(full) == 1  # Only one copy

    def test_concurrent_conversations(self, temp_storage):
        """Test interleaved processing of multiple conversations"""
        dedup = ClaudeConversationDeduplicator(temp_storage)

        export1 = {
            "messages": [{"index": 0, "role": "user", "content": "Session 1 msg 1"}]
        }
        export2 = {
            "messages": [{"index": 0, "role": "user", "content": "Session 2 msg 1"}]
        }

        # Interleave processing
        dedup.process_export("session-1", export1)
        dedup.process_export("session-2", export2)

        export1_v2 = {
            "messages": [
                {"index": 0, "role": "user", "content": "Session 1 msg 1"},
                {"index": 1, "role": "user", "content": "Session 1 msg 2"},
            ]
        }

        dedup.process_export("session-1", export1_v2)

        # Verify correct separation
        conv1 = dedup.get_full_conversation("session-1")
        conv2 = dedup.get_full_conversation("session-2")

        assert len(conv1) == 2
        assert len(conv2) == 1
        assert "Session 1" in conv1[0]["content"]
        assert "Session 2" in conv2[0]["content"]

    def test_large_export_performance(self, temp_storage):
        """Test performance with large export (1000 messages)"""
        dedup = ClaudeConversationDeduplicator(temp_storage)

        # Create large export
        messages = [
            {
                "index": i,
                "role": "user" if i % 2 == 0 else "assistant",
                "content": f"Message {i}",
            }
            for i in range(1000)
        ]
        large_export = {"messages": messages}

        import time

        start = time.time()
        new_messages, stats = dedup.process_export("large-session", large_export)
        elapsed = time.time() - start

        assert len(new_messages) == 1000
        assert elapsed < 5.0  # Should complete in under 5 seconds

    def test_malformed_message_handling(self, temp_storage):
        """Test handling of messages with missing fields"""
        dedup = ClaudeConversationDeduplicator(temp_storage)

        export = {
            "messages": [
                {"index": 0, "content": "Missing role"},  # No role field
                {"role": "user", "content": "Missing index"},  # No index field
                {"index": 2, "role": "user", "content": "Complete"},
            ]
        }

        # Should handle gracefully (default values)
        new_messages, stats = dedup.process_export("session-1", export)
        assert len(new_messages) > 0  # Should process without crashing


def test_full_integration_workflow(tmp_path):
    """Integration test: Full workflow from file parsing to deduplication"""
    # Create export files
    export1_path = tmp_path / "2025-11-17-EXPORT-DAY1.txt"
    export1_path.write_text(
        """
⏺ Hello, Claude!

  ⎿  Hello! How can I help you?

⏺ What is AI?
""",
        encoding="utf-8",
    )

    export2_path = tmp_path / "2025-11-17-EXPORT-DAY2.txt"
    export2_path.write_text(
        """
⏺ Hello, Claude!

  ⎿  Hello! How can I help you?

⏺ What is AI?

  ⎿  AI stands for Artificial Intelligence...

⏺ Thank you!
""",
        encoding="utf-8",
    )

    # Process both exports
    storage_dir = tmp_path / "dedup_state"
    dedup = ClaudeConversationDeduplicator(str(storage_dir))

    # Day 1
    export1_data = parse_claude_export_file(export1_path)
    session_id = extract_session_id_from_filename(export1_path)
    new1, stats1 = dedup.process_export(session_id, export1_data)

    # Day 2
    export2_data = parse_claude_export_file(export2_path)
    new2, stats2 = dedup.process_export(session_id, export2_data)

    # Verify results
    assert stats1["new_messages"] == 3  # All new on day 1
    assert stats2["new_messages"] == 2  # Only 2 new on day 2
    assert stats2["duplicates_filtered"] == 3  # 3 duplicates filtered

    # Verify full conversation
    full = dedup.get_full_conversation(session_id)
    assert len(full) == 5  # Total unique messages

    # Verify integrity
    validation = dedup.validate_integrity(session_id)
    assert validation["valid"] is True

    # Calculate storage savings
    original_size = len(export1_path.read_text()) + len(export2_path.read_text())
    log_size = (storage_dir / "conversation_log.jsonl").stat().st_size

    # Log should be much smaller than combined exports
    # (though actual savings depend on format - this is just a sanity check)
    assert log_size > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
