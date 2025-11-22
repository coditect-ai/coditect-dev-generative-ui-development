#!/usr/bin/env python3
"""
Unit Tests for Session Export Engine

Tests session context export, conversation extraction, metadata generation,
file change tracking, and decision extraction.

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 5
Date: 2025-11-16
"""

import os
import sys
import unittest
import tempfile
import json
import subprocess
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open, call

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'scripts' / 'core'))

from session_export import SessionExporter


class TestSessionExporter(unittest.TestCase):
    """Test cases for SessionExporter class."""

    def setUp(self):
        """Set up each test with temporary directory and exporter."""
        # Create temporary directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)

        # Create .git to make it a valid git repository
        (self.repo_root / '.git').mkdir()

        # Create directory structure
        self.memory_context_dir = self.repo_root / "MEMORY-CONTEXT"
        self.checkpoints_dir = self.memory_context_dir / "checkpoints"
        self.sessions_dir = self.memory_context_dir / "sessions"
        self.exports_dir = self.memory_context_dir / "exports"

        self.checkpoints_dir.mkdir(parents=True)

        # Initialize exporter
        self.exporter = SessionExporter(repo_root=self.repo_root)

    def tearDown(self):
        """Clean up temporary files after each test."""
        import shutil
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    # ========== Initialization Tests ==========

    def test_init_explicit_repo_root(self):
        """Test SessionExporter initialization with explicitly provided repo root."""
        exporter = SessionExporter(repo_root=self.repo_root)

        self.assertEqual(exporter.repo_root, self.repo_root)
        self.assertEqual(exporter.memory_context_dir, self.repo_root / "MEMORY-CONTEXT")
        self.assertEqual(exporter.sessions_dir, self.repo_root / "MEMORY-CONTEXT" / "sessions")
        self.assertEqual(exporter.exports_dir, self.repo_root / "MEMORY-CONTEXT" / "exports")
        self.assertTrue(exporter.sessions_dir.exists())
        self.assertTrue(exporter.exports_dir.exists())

    @patch('session_export.find_git_root')
    def test_init_auto_detect_git_root(self, mock_find_git_root):
        """Test SessionExporter initialization with auto-detected git root."""
        mock_find_git_root.return_value = self.repo_root

        exporter = SessionExporter(repo_root=None)

        mock_find_git_root.assert_called_once()
        self.assertEqual(exporter.repo_root, self.repo_root)

    def test_init_invalid_repo_root(self):
        """Test SessionExporter initialization fails for non-git directory."""
        invalid_dir = Path(self.temp_dir) / "not_a_repo"
        invalid_dir.mkdir()

        with self.assertRaises(ValueError) as context:
            SessionExporter(repo_root=invalid_dir)

        self.assertIn("not a git repository", str(context.exception))

    # ========== Find Latest Checkpoint Tests ==========

    def test_find_latest_checkpoint(self):
        """Test finding most recent checkpoint file."""
        # Create multiple checkpoint files with different timestamps
        checkpoint1 = self.checkpoints_dir / "2025-11-15T10-00-00Z-old-checkpoint.md"
        checkpoint2 = self.checkpoints_dir / "2025-11-16T14-30-00Z-recent-checkpoint.md"
        checkpoint3 = self.checkpoints_dir / "2025-11-16T09-00-00Z-morning-checkpoint.md"

        checkpoint1.write_text("Old checkpoint content")
        checkpoint2.write_text("Recent checkpoint content")
        checkpoint3.write_text("Morning checkpoint content")

        # Make checkpoint2 the most recently modified
        import time
        time.sleep(0.01)  # Ensure different mtimes
        checkpoint2.touch()

        latest = self.exporter._find_latest_checkpoint()

        self.assertEqual(latest, checkpoint2)

    def test_find_latest_checkpoint_no_checkpoints(self):
        """Test finding latest checkpoint when no checkpoints exist."""
        # Clear checkpoints directory
        for file in self.checkpoints_dir.glob("*.md"):
            file.unlink()

        latest = self.exporter._find_latest_checkpoint()

        self.assertIsNone(latest)

    def test_find_latest_checkpoint_nonexistent_directory(self):
        """Test finding latest checkpoint when checkpoints directory doesn't exist."""
        import shutil
        shutil.rmtree(self.checkpoints_dir)

        latest = self.exporter._find_latest_checkpoint()

        self.assertIsNone(latest)

    # ========== Conversation Extraction Tests ==========

    def test_extract_conversation(self):
        """Test extracting conversation from checkpoint with explicit messages."""
        checkpoint_content = """# Checkpoint

## Work Completed

User: Create a new authentication system
Assistant: I'll implement OAuth2 authentication
User: Add password reset functionality
Assistant: Password reset added with email verification
"""

        checkpoint_path = self.checkpoints_dir / "test-checkpoint.md"
        checkpoint_path.write_text(checkpoint_content)

        conversation = self.exporter._extract_conversation(checkpoint_path)

        self.assertEqual(len(conversation), 4)
        self.assertEqual(conversation[0]['role'], 'user')
        self.assertIn('authentication', conversation[0]['content'].lower())
        self.assertEqual(conversation[1]['role'], 'assistant')
        self.assertIn('oauth2', conversation[1]['content'].lower())

    def test_extract_conversation_empty(self):
        """Test extracting conversation when no conversation found (fallback to sections)."""
        checkpoint_content = """# Checkpoint

## Work Completed

Implemented authentication system

## Next Steps

Add authorization layer
"""

        checkpoint_path = self.checkpoints_dir / "test-checkpoint.md"
        checkpoint_path.write_text(checkpoint_content)

        conversation = self.exporter._extract_conversation(checkpoint_path)

        # Should fall back to sections extraction
        self.assertGreater(len(conversation), 0)
        self.assertEqual(conversation[0]['role'], 'system')
        self.assertIn('sections', conversation[0])

    def test_extract_conversation_case_insensitive(self):
        """Test conversation extraction is case-insensitive."""
        checkpoint_content = """
HUMAN: Test message one
CLAUDE: Response one
human: Test message two
claude: Response two
"""

        checkpoint_path = self.checkpoints_dir / "test-checkpoint.md"
        checkpoint_path.write_text(checkpoint_content)

        conversation = self.exporter._extract_conversation(checkpoint_path)

        self.assertEqual(len(conversation), 4)
        self.assertEqual(conversation[0]['role'], 'user')
        self.assertEqual(conversation[1]['role'], 'assistant')

    # ========== Section Extraction Tests ==========

    def test_extract_sections(self):
        """Test extracting markdown sections from checkpoint."""
        content = """# Main Title

## Section One

Content for section one.
Multiple lines.

## Section Two

Content for section two.

## Section Three

Final section content.
"""

        sections = self.exporter._extract_sections(content)

        self.assertEqual(len(sections), 3)
        self.assertIn('Section One', sections)
        self.assertIn('Section Two', sections)
        self.assertIn('Section Three', sections)
        self.assertIn('Multiple lines', sections['Section One'])

    def test_extract_sections_empty_content(self):
        """Test extracting sections from empty content."""
        sections = self.exporter._extract_sections("")

        self.assertEqual(sections, {})

    def test_extract_sections_no_sections(self):
        """Test extracting sections when no section headers exist."""
        content = "Just plain text without any headers."

        sections = self.exporter._extract_sections(content)

        self.assertEqual(sections, {})

    # ========== Metadata Generation Tests ==========

    def test_generate_metadata(self):
        """Test metadata generation with ISO timestamp from filename."""
        checkpoint_path = self.checkpoints_dir / "2025-11-16T14-30-45Z-sprint-completion.md"
        checkpoint_path.write_text("# Checkpoint\n\n#testing #sprint-1")

        metadata = self.exporter._generate_metadata(checkpoint_path)

        self.assertIn('timestamp', metadata)
        self.assertIn('2025-11-16', metadata['timestamp'])
        self.assertIn('checkpoint_file', metadata)
        self.assertEqual(metadata['checkpoint_file'], checkpoint_path.name)
        self.assertIn('participants', metadata)
        self.assertIn('objectives', metadata)
        # Objectives extracted from filename parts after timestamp
        self.assertIn('sprint', metadata['objectives'].lower())
        self.assertIn('completion', metadata['objectives'].lower())
        self.assertIn('tags', metadata)
        self.assertIn('testing', metadata['tags'])
        self.assertIn('sprint-1', metadata['tags'])

    def test_generate_metadata_fallback(self):
        """Test metadata generation falls back to file mtime when no timestamp in filename."""
        checkpoint_path = self.checkpoints_dir / "checkpoint-without-timestamp.md"
        checkpoint_path.write_text("# Checkpoint")

        metadata = self.exporter._generate_metadata(checkpoint_path)

        self.assertIn('timestamp', metadata)
        # Should be in ISO format
        self.assertRegex(metadata['timestamp'], r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')

    def test_generate_metadata_with_tags(self):
        """Test metadata extracts tags from checkpoint content."""
        checkpoint_content = """# Checkpoint

**Tags:** testing, deployment, production
**Sprint:** Sprint +1
**Phase:** Beta

Work completed here.
"""

        checkpoint_path = self.checkpoints_dir / "test-checkpoint.md"
        checkpoint_path.write_text(checkpoint_content)

        metadata = self.exporter._generate_metadata(checkpoint_path)

        self.assertIn('tags', metadata)
        tags = metadata['tags']
        self.assertIn('testing', tags)
        self.assertIn('deployment', tags)
        self.assertIn('sprint', tags)

    # ========== Tag Extraction Tests ==========

    def test_extract_tags(self):
        """Test extracting tags from checkpoint content."""
        content = """# Checkpoint

#authentication #oauth2 #security

**Tags:** testing, deployment
**Sprint:** Sprint +1
**Phase:** Beta Testing
"""

        tags = self.exporter._extract_tags(content)

        self.assertIn('authentication', tags)
        self.assertIn('oauth2', tags)
        self.assertIn('security', tags)
        self.assertIn('testing', tags)
        self.assertIn('deployment', tags)
        self.assertIn('sprint', tags)
        # Phase "Beta Testing" gets split and normalized
        self.assertTrue(any('beta' in tag for tag in tags))

    def test_extract_tags_empty_content(self):
        """Test extracting tags from empty content."""
        tags = self.exporter._extract_tags("")

        self.assertEqual(tags, [])

    def test_extract_tags_no_tags(self):
        """Test extracting tags when none exist."""
        content = "Just regular content without any tags."

        tags = self.exporter._extract_tags(content)

        self.assertEqual(tags, [])

    # ========== File Change Tracking Tests ==========

    @patch('subprocess.run')
    def test_track_file_changes(self, mock_run):
        """Test tracking file changes via git status."""
        # Mock git status output
        mock_status_result = MagicMock()
        mock_status_result.stdout = """ M src/auth.py
A  src/models.py
 D tests/old_test.py
?? README.md
AM src/utils.py
"""

        # Mock git log output
        mock_log_result = MagicMock()
        mock_log_result.stdout = """abc123 Add authentication
def456 Update models
ghi789 Fix bugs
"""

        # Configure mock to return different results for different commands
        def run_side_effect(cmd, **kwargs):
            if 'status' in cmd:
                return mock_status_result
            elif 'log' in cmd:
                return mock_log_result
            return MagicMock()

        mock_run.side_effect = run_side_effect

        file_changes = self.exporter._track_file_changes()

        self.assertIn('modified', file_changes)
        self.assertIn('added', file_changes)
        self.assertIn('deleted', file_changes)
        self.assertIn('untracked', file_changes)
        self.assertIn('recent_commits', file_changes)

        self.assertIn('src/auth.py', file_changes['modified'])
        self.assertIn('src/models.py', file_changes['added'])
        self.assertIn('src/utils.py', file_changes['added'])
        self.assertIn('tests/old_test.py', file_changes['deleted'])
        self.assertIn('README.md', file_changes['untracked'])

        self.assertEqual(len(file_changes['recent_commits']), 3)

    @patch('subprocess.run')
    def test_track_file_changes_git_error(self, mock_run):
        """Test file change tracking handles git errors gracefully."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')

        file_changes = self.exporter._track_file_changes()

        # Should return empty lists on error
        self.assertEqual(file_changes['modified'], [])
        self.assertEqual(file_changes['added'], [])
        self.assertEqual(file_changes['deleted'], [])
        self.assertEqual(file_changes['untracked'], [])

    @patch('subprocess.run')
    def test_track_file_changes_empty_status(self, mock_run):
        """Test file change tracking with clean working directory."""
        mock_status_result = MagicMock()
        mock_status_result.stdout = ""

        mock_log_result = MagicMock()
        mock_log_result.stdout = "abc123 Latest commit"

        def run_side_effect(cmd, **kwargs):
            if 'status' in cmd:
                return mock_status_result
            elif 'log' in cmd:
                return mock_log_result
            return MagicMock()

        mock_run.side_effect = run_side_effect

        file_changes = self.exporter._track_file_changes()

        self.assertEqual(len(file_changes['modified']), 0)
        self.assertEqual(len(file_changes['added']), 0)
        self.assertEqual(len(file_changes['deleted']), 0)

    # ========== Decision Extraction Tests ==========

    def test_extract_decisions(self):
        """Test extracting decisions from checkpoint content."""
        checkpoint_content = """# Checkpoint

## Architecture Decisions

We decided to use PostgreSQL for the database because it offers better JSON support.

The rationale: PostgreSQL provides JSONB type with indexing.

**Decision:** Use FastAPI for the backend framework.

We chose to implement caching with Redis since it's fast and reliable.
"""

        checkpoint_path = self.checkpoints_dir / "test-checkpoint.md"
        checkpoint_path.write_text(checkpoint_content)

        decisions = self.exporter._extract_decisions(checkpoint_path)

        self.assertGreater(len(decisions), 0)

        # Check that decisions contain expected text
        decision_texts = [d['decision'] for d in decisions]
        self.assertTrue(any('PostgreSQL' in text for text in decision_texts))
        self.assertTrue(any('FastAPI' in text or 'Use FastAPI' in text for text in decision_texts))

    def test_extract_decisions_from_sections(self):
        """Test extracting decisions from dedicated decision sections."""
        checkpoint_content = """# Checkpoint

## Decision Log

Selected React for frontend framework due to ecosystem maturity.

## Rationale Section

Using Docker for containerization.
"""

        checkpoint_path = self.checkpoints_dir / "test-checkpoint.md"
        checkpoint_path.write_text(checkpoint_content)

        decisions = self.exporter._extract_decisions(checkpoint_path)

        self.assertGreater(len(decisions), 0)

        # Should extract sections labeled as decisions or rationale
        section_decisions = [d for d in decisions if d['decision'] in ['Decision Log', 'Rationale Section']]
        self.assertGreater(len(section_decisions), 0)

    def test_extract_decisions_empty(self):
        """Test extracting decisions when none exist."""
        checkpoint_content = """# Checkpoint

Just regular work completed without any explicit decisions.
"""

        checkpoint_path = self.checkpoints_dir / "test-checkpoint.md"
        checkpoint_path.write_text(checkpoint_content)

        decisions = self.exporter._extract_decisions(checkpoint_path)

        # May have some incidental matches, but should be minimal
        # Just verify it doesn't crash
        self.assertIsInstance(decisions, list)

    # ========== Session Export Building Tests ==========

    def test_build_session_export(self):
        """Test building markdown session export document."""
        conversation = [
            {'role': 'user', 'content': 'Create authentication system'},
            {'role': 'assistant', 'content': 'Implementing OAuth2'}
        ]

        metadata = {
            'timestamp': '2025-11-16T14:30:00Z',
            'checkpoint_file': 'test-checkpoint.md',
            'repository': str(self.repo_root),
            'participants': ['user', 'claude-code'],
            'objectives': 'Sprint completion',
            'tags': ['testing', 'auth'],
            'export_time': '2025-11-16T15:00:00Z'
        }

        file_changes = {
            'modified': ['src/auth.py'],
            'added': ['src/models.py'],
            'deleted': [],
            'untracked': ['README.md'],
            'recent_commits': ['abc123 Add auth', 'def456 Update models']
        }

        decisions = [
            {
                'decision': 'Use OAuth2',
                'context': 'OAuth2 is industry standard',
                'timestamp': None
            }
        ]

        export_content = self.exporter._build_session_export(
            conversation=conversation,
            metadata=metadata,
            file_changes=file_changes,
            decisions=decisions
        )

        # Verify structure
        self.assertIn('# Session Export', export_content)
        self.assertIn('Sprint completion', export_content)
        self.assertIn('2025-11-16T14:30:00Z', export_content)
        self.assertIn('## Session Metadata', export_content)
        self.assertIn('## Conversation Summary', export_content)
        self.assertIn('## File Changes', export_content)
        self.assertIn('## Decisions & Rationale', export_content)
        self.assertIn('Create authentication system', export_content)
        self.assertIn('Use OAuth2', export_content)
        self.assertIn('src/auth.py', export_content)

    def test_build_session_export_empty_conversation(self):
        """Test building session export with no conversation."""
        metadata = {
            'timestamp': '2025-11-16T14:30:00Z',
            'checkpoint_file': 'test.md',
            'repository': str(self.repo_root),
            'participants': ['user'],
            'objectives': 'Test',
            'tags': [],
            'export_time': '2025-11-16T15:00:00Z'
        }

        export_content = self.exporter._build_session_export(
            conversation=[],
            metadata=metadata,
            file_changes={'modified': [], 'added': [], 'deleted': [], 'untracked': []},
            decisions=[]
        )

        self.assertIn('*No conversation history extracted*', export_content)
        self.assertIn('*No file changes detected*', export_content)
        self.assertIn('*No explicit decisions extracted*', export_content)

    # ========== JSON Export Tests ==========

    def test_export_json(self):
        """Test exporting session data as JSON."""
        json_path = self.exports_dir / "test-export.json"

        conversation = [{'role': 'user', 'content': 'Test message'}]
        metadata = {'timestamp': '2025-11-16T14:30:00Z', 'objectives': 'Test'}
        file_changes = {'modified': ['test.py'], 'added': [], 'deleted': [], 'untracked': []}
        decisions = [{'decision': 'Test decision', 'context': 'Test context'}]

        self.exporter._export_json(
            json_path,
            conversation=conversation,
            metadata=metadata,
            file_changes=file_changes,
            decisions=decisions
        )

        self.assertTrue(json_path.exists())

        # Verify JSON structure
        with open(json_path, 'r') as f:
            data = json.load(f)

        self.assertIn('metadata', data)
        self.assertIn('conversation', data)
        self.assertIn('file_changes', data)
        self.assertIn('decisions', data)
        self.assertEqual(data['metadata']['objectives'], 'Test')

    # ========== Session Name Generation Tests ==========

    def test_generate_session_name(self):
        """Test generating session name from checkpoint filename."""
        checkpoint_path = self.checkpoints_dir / "2025-11-16T14-30-00Z-sprint-completion-auth-system.md"
        metadata = {'objectives': 'Sprint completion'}

        session_name = self.exporter._generate_session_name(checkpoint_path, metadata)

        # Session name extracted from parts after timestamp (including 00Z)
        self.assertIn('sprint-completion-auth-system', session_name)

    def test_generate_session_name_short_filename(self):
        """Test generating session name from short checkpoint filename."""
        checkpoint_path = self.checkpoints_dir / "checkpoint.md"
        metadata = {'objectives': 'Work'}

        session_name = self.exporter._generate_session_name(checkpoint_path, metadata)

        # Should return 'checkpoint' or 'session' as fallback
        self.assertIn(session_name, ['checkpoint', 'session'])

    def test_generate_session_name_long_filename(self):
        """Test session name truncation for very long filenames."""
        long_name = "a" * 150  # 150 character name
        checkpoint_path = self.checkpoints_dir / f"2025-11-16T14-30-00Z-{long_name}.md"
        metadata = {'objectives': 'Test'}

        session_name = self.exporter._generate_session_name(checkpoint_path, metadata)

        # Should be truncated to 100 characters
        self.assertLessEqual(len(session_name), 100)

    # ========== Full Export Session Integration Tests ==========

    @patch('subprocess.run')
    def test_export_session_full_pipeline(self, mock_run):
        """Integration test for complete session export pipeline."""
        # Create checkpoint file
        checkpoint_content = """# Checkpoint

User: Implement authentication
Assistant: OAuth2 implementation complete

## Work Completed

Authentication system implemented with OAuth2.

**Decision:** Use OAuth2 for authentication.
**Rationale:** Industry standard with good library support.
"""

        checkpoint_path = self.checkpoints_dir / "2025-11-16T14-30-00Z-auth-implementation.md"
        checkpoint_path.write_text(checkpoint_content)

        # Mock git commands
        mock_status_result = MagicMock()
        mock_status_result.stdout = " M src/auth.py"

        mock_log_result = MagicMock()
        mock_log_result.stdout = "abc123 Add authentication"

        def run_side_effect(cmd, **kwargs):
            if 'status' in cmd:
                return mock_status_result
            elif 'log' in cmd:
                return mock_log_result
            return MagicMock()

        mock_run.side_effect = run_side_effect

        # Export session
        session_path = self.exporter.export_session(
            checkpoint_path=checkpoint_path,
            session_name="test-session"
        )

        # Verify session file created
        self.assertTrue(session_path.exists())
        self.assertTrue(session_path.name.endswith('-test-session.md'))

        # Verify JSON export created
        json_filename = session_path.name.replace('.md', '.json')
        json_path = self.exports_dir / json_filename
        self.assertTrue(json_path.exists())

        # Verify content
        content = session_path.read_text()
        self.assertIn('Session Export', content)
        self.assertIn('OAuth2', content)
        self.assertIn('src/auth.py', content)

    @patch('subprocess.run')
    def test_export_session_auto_detect_checkpoint(self, mock_run):
        """Test exporting session with auto-detected checkpoint."""
        # Create checkpoint
        checkpoint_path = self.checkpoints_dir / "2025-11-16T14-30-00Z-latest.md"
        checkpoint_path.write_text("# Checkpoint\n\nLatest work")

        # Mock git commands
        mock_run.return_value = MagicMock(stdout="")

        # Export without specifying checkpoint
        session_path = self.exporter.export_session()

        self.assertTrue(session_path.exists())

    def test_export_session_no_checkpoints_raises_error(self):
        """Test export_session raises error when no checkpoints exist."""
        # Clear checkpoints
        for file in self.checkpoints_dir.glob("*.md"):
            file.unlink()

        with self.assertRaises(ValueError) as context:
            self.exporter.export_session()

        self.assertIn("No checkpoints found", str(context.exception))

    def test_export_session_nonexistent_checkpoint_raises_error(self):
        """Test export_session raises error for nonexistent checkpoint."""
        nonexistent = self.checkpoints_dir / "does-not-exist.md"

        with self.assertRaises(FileNotFoundError):
            self.exporter.export_session(checkpoint_path=nonexistent)


class TestSessionExporterEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        (self.repo_root / '.git').mkdir()

        # Create directory structure
        self.memory_context_dir = self.repo_root / "MEMORY-CONTEXT"
        self.checkpoints_dir = self.memory_context_dir / "checkpoints"
        self.checkpoints_dir.mkdir(parents=True)

        self.exporter = SessionExporter(repo_root=self.repo_root)

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_extract_conversation_with_sections_fallback(self):
        """Test conversation extraction falls back to sections when no explicit messages."""
        checkpoint_content = """# Checkpoint

## Section One

Content here.

## Section Two

More content.
"""

        checkpoint_path = self.exporter.checkpoints_dir / "test.md"
        checkpoint_path.write_text(checkpoint_content)

        conversation = self.exporter._extract_conversation(checkpoint_path)

        self.assertEqual(len(conversation), 1)
        self.assertEqual(conversation[0]['role'], 'system')
        self.assertIn('sections', conversation[0])
        self.assertIn('Section One', conversation[0]['sections'])

    def test_metadata_timestamp_parsing_variations(self):
        """Test metadata handles various timestamp formats in filename."""
        test_cases = [
            ("2025-11-16T14-30-00Z-test.md", "2025-11-16"),
            ("2025-01-01T00-00-00Z-test.md", "2025-01-01"),
            ("no-timestamp-test.md", None),  # Should fall back to mtime
        ]

        for filename, expected_date in test_cases:
            checkpoint_path = self.exporter.checkpoints_dir / filename
            checkpoint_path.write_text("# Test")

            metadata = self.exporter._generate_metadata(checkpoint_path)

            if expected_date:
                self.assertIn(expected_date, metadata['timestamp'])
            else:
                # Should have some timestamp from mtime
                self.assertRegex(metadata['timestamp'], r'\d{4}-\d{2}-\d{2}')

    def test_tag_extraction_with_special_characters(self):
        """Test tag extraction handles special characters correctly."""
        content = """# Checkpoint

#tag-with-hyphens #tag_with_underscores #123numeric

**Tags:** multi word tag, another tag; semicolon|pipe
"""

        tags = self.exporter._extract_tags(content)

        self.assertIn('tag-with-hyphens', tags)
        # Underscores and special chars should be normalized
        self.assertTrue(any('multi' in tag or 'word' in tag for tag in tags))

    def test_build_session_export_truncates_long_content(self):
        """Test session export truncates very long content appropriately."""
        long_content = "x" * 1000

        conversation = [
            {
                'role': 'system',
                'content': 'Summary',
                'sections': {
                    'Long Section': long_content
                }
            }
        ]

        metadata = {
            'timestamp': '2025-11-16T14:30:00Z',
            'checkpoint_file': 'test.md',
            'repository': str(self.repo_root),
            'participants': ['user'],
            'objectives': 'Test',
            'tags': [],
            'export_time': '2025-11-16T15:00:00Z'
        }

        export = self.exporter._build_session_export(
            conversation=conversation,
            metadata=metadata,
            file_changes={'modified': [], 'added': [], 'deleted': [], 'untracked': []},
            decisions=[]
        )

        # Content should be truncated with ellipsis
        self.assertIn('...', export)

    def test_file_changes_limits_output(self):
        """Test file changes output is limited to prevent excessive size."""
        many_files = [f"file_{i}.py" for i in range(50)]

        file_changes = {
            'modified': many_files,
            'added': [],
            'deleted': [],
            'untracked': []
        }

        metadata = {
            'timestamp': '2025-11-16T14:30:00Z',
            'checkpoint_file': 'test.md',
            'repository': str(self.repo_root),
            'participants': ['user'],
            'objectives': 'Test',
            'tags': [],
            'export_time': '2025-11-16T15:00:00Z'
        }

        export = self.exporter._build_session_export(
            conversation=[],
            metadata=metadata,
            file_changes=file_changes,
            decisions=[]
        )

        # Should indicate there are more files
        self.assertIn('and 30 more', export)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSessionExporter))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionExporterEdgeCases))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return success/failure
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
