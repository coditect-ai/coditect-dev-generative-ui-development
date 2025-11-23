#!/usr/bin/env python3
"""
CODITECT MEMORY-CONTEXT Database Seeding

Adds sample data to database for testing and demonstration.
Creates sample sessions, patterns, tags, and checkpoints.

Usage:
    python3 scripts/core/db_seed.py [--reset] [--verbose]

Options:
    --reset     Clear existing data before seeding
    --verbose   Show detailed progress

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 3
Date: 2025-11-16
"""

import os
import sys
import sqlite3
import argparse
import logging
import uuid
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('db_seed.log')
    ]
)
logger = logging.getLogger(__name__)

# Custom exceptions
class DatabaseSeedError(Exception):
    """Base exception for database seeding errors"""
    pass

class ValidationError(DatabaseSeedError):
    """Data validation error"""
    pass

class ConnectionError(DatabaseSeedError):
    """Database connection error"""
    pass


class DatabaseSeeder:
    """Seed CODITECT MEMORY-CONTEXT database with sample data."""

    def __init__(self, db_path: Path, verbose: bool = False):
        """
        Initialize database seeder.

        Args:
            db_path: Path to SQLite database file
            verbose: Enable verbose logging

        Raises:
            ValidationError: If database file doesn't exist
        """
        self.db_path = Path(db_path)
        self.verbose = verbose

        if self.verbose:
            logger.setLevel(logging.DEBUG)

        logger.debug(f"Initializing seeder with database: {self.db_path}")

        if not self.db_path.exists():
            logger.error(f"Database not found: {self.db_path}")
            raise ValidationError(
                f"Database not found: {self.db_path}\n"
                f"Run db_init.py first to create database"
            )

        logger.info("Database seeder initialized")

    def connect(self) -> sqlite3.Connection:
        """
        Create database connection.

        Returns:
            SQLite connection object

        Raises:
            ConnectionError: If database connection fails
        """
        try:
            logger.debug(f"Connecting to database: {self.db_path}")
            conn = sqlite3.Connection(str(self.db_path))
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            logger.info("Database connection established")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise ConnectionError(f"Could not connect to database: {e}")
        except Exception as e:
            logger.error(f"Unexpected error connecting to database: {e}")
            raise DatabaseSeedError(f"Database connection error: {e}")

    def clear_data(self, conn: sqlite3.Connection) -> None:
        """
        Clear all existing data (keep schema).

        Args:
            conn: SQLite connection
        """
        cursor = conn.cursor()

        # Order matters due to foreign keys
        tables = [
            'privacy_audit',
            'context_loads',
            'session_tags',
            'pattern_tags',
            'tags',
            'sessions',
            'patterns',
            'checkpoints',
        ]

        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            logger.info(f"Cleared table: {table}")

        conn.commit()
        logger.info("All data cleared")

    def seed_tags(self, conn: sqlite3.Connection) -> dict:
        """
        Seed tags table with sample tags.

        Args:
            conn: SQLite connection

        Returns:
            Dictionary mapping tag names to tag IDs
        """
        cursor = conn.cursor()

        sample_tags = [
            # Technology tags
            ('python', 'technology', 'Python programming language'),
            ('javascript', 'technology', 'JavaScript programming language'),
            ('typescript', 'technology', 'TypeScript programming language'),
            ('react', 'technology', 'React frontend framework'),
            ('fastapi', 'technology', 'FastAPI backend framework'),
            ('sqlite', 'technology', 'SQLite database'),
            ('chromadb', 'technology', 'ChromaDB vector database'),

            # Project tags
            ('memory-context', 'project', 'MEMORY-CONTEXT implementation'),
            ('privacy-manager', 'project', 'Privacy control system'),
            ('nested-learning', 'project', 'Pattern extraction system'),
            ('coditect-framework', 'project', 'Core CODITECT framework'),

            # Domain tags
            ('backend', 'domain', 'Backend development'),
            ('frontend', 'domain', 'Frontend development'),
            ('database', 'domain', 'Database design and management'),
            ('security', 'domain', 'Security and privacy'),
            ('ai-ml', 'domain', 'AI and machine learning'),

            # Workflow tags
            ('bug-fix', 'workflow', 'Bug fix workflow'),
            ('feature-dev', 'workflow', 'Feature development'),
            ('refactoring', 'workflow', 'Code refactoring'),
            ('testing', 'workflow', 'Testing and QA'),
            ('deployment', 'workflow', 'Deployment and operations'),
        ]

        tag_ids = {}
        now = datetime.now(timezone.utc).isoformat()

        for tag_name, tag_category, description in sample_tags:
            cursor.execute(
                """
                INSERT INTO tags (tag_name, tag_category, description, usage_count, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (tag_name, tag_category, description, 0, now)
            )
            tag_ids[tag_name] = cursor.lastrowid

        conn.commit()
        logger.info(f"Seeded {len(sample_tags)} tags")

        return tag_ids

    def seed_checkpoints(self, conn: sqlite3.Connection) -> list:
        """
        Seed checkpoints table with sample checkpoints.

        Args:
            conn: SQLite connection

        Returns:
            List of checkpoint IDs
        """
        cursor = conn.cursor()
        now = datetime.now(timezone.utc)

        sample_checkpoints = [
            {
                'timestamp': (now - timedelta(days=7)).isoformat(),
                'description': 'Sprint +1 Day 1 Complete: Session Export Engine',
                'git_commit_hash': '0a72883',
                'git_branch': 'main',
                'files_changed': 12,
                'tasks_completed': 6,
            },
            {
                'timestamp': (now - timedelta(days=6)).isoformat(),
                'description': 'Sprint +1 Day 2 Complete: Privacy Manager Production Ready',
                'git_commit_hash': 'afcc2cf',
                'git_branch': 'main',
                'files_changed': 8,
                'tasks_completed': 7,
            },
        ]

        checkpoint_ids = []

        for checkpoint in sample_checkpoints:
            checkpoint_id = str(uuid.uuid4())
            checkpoint_file = f"MEMORY-CONTEXT/checkpoints/{checkpoint['timestamp'][:10]}-{checkpoint['description'].replace(' ', '-')}.md"

            cursor.execute(
                """
                INSERT INTO checkpoints (
                    checkpoint_id, timestamp, description,
                    checkpoint_file_path, session_export_path,
                    git_commit_hash, git_branch, git_status,
                    submodules_updated, files_changed, tasks_completed,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    checkpoint_id,
                    checkpoint['timestamp'],
                    checkpoint['description'],
                    checkpoint_file,
                    f"MEMORY-CONTEXT/sessions/{checkpoint['timestamp'][:10]}-session.md",
                    checkpoint['git_commit_hash'],
                    checkpoint['git_branch'],
                    'Clean working directory',
                    1,
                    checkpoint['files_changed'],
                    checkpoint['tasks_completed'],
                    checkpoint['timestamp'],
                )
            )

            checkpoint_ids.append(checkpoint_id)

        conn.commit()
        logger.info(f"Seeded {len(sample_checkpoints)} checkpoints")

        return checkpoint_ids

    def seed_sessions(self, conn: sqlite3.Connection, checkpoint_ids: list, tag_ids: dict) -> list:
        """
        Seed sessions table with sample sessions.

        Args:
            conn: SQLite connection
            checkpoint_ids: List of checkpoint IDs to link to
            tag_ids: Dictionary mapping tag names to IDs

        Returns:
            List of session IDs
        """
        cursor = conn.cursor()
        now = datetime.now(timezone.utc)

        sample_sessions = [
            {
                'title': 'Privacy Manager Implementation',
                'description': 'Implement 4-level privacy model with PII detection and redaction',
                'privacy_level': 'TEAM',
                'timestamp': (now - timedelta(days=6)).isoformat(),
                'duration_minutes': 240,
                'messages_count': 45,
                'files_changed_count': 8,
                'token_count': 12000,
                'checkpoint_id': checkpoint_ids[1] if len(checkpoint_ids) > 1 else None,
                'tags': ['privacy-manager', 'python', 'security', 'feature-dev'],
            },
            {
                'title': 'Database Schema Design',
                'description': 'Design SQLite schema for MEMORY-CONTEXT system',
                'privacy_level': 'PUBLIC',
                'timestamp': now.isoformat(),
                'duration_minutes': 120,
                'messages_count': 22,
                'files_changed_count': 4,
                'token_count': 8000,
                'checkpoint_id': None,
                'tags': ['memory-context', 'database', 'sqlite', 'feature-dev'],
            },
            {
                'title': 'Session Export Engine Bug Fix',
                'description': 'Fix conversation extraction edge case handling',
                'privacy_level': 'TEAM',
                'timestamp': (now - timedelta(days=7)).isoformat(),
                'duration_minutes': 60,
                'messages_count': 15,
                'files_changed_count': 3,
                'token_count': 4000,
                'checkpoint_id': checkpoint_ids[0] if len(checkpoint_ids) > 0 else None,
                'tags': ['memory-context', 'python', 'bug-fix', 'testing'],
            },
        ]

        session_ids = []

        for session in sample_sessions:
            session_id = str(uuid.uuid4())

            # Create sample metadata
            metadata = {
                'participants': ['user', 'claude'],
                'objectives': [session['title']],
                'tools_used': ['Read', 'Write', 'Edit', 'Bash'],
                'agents_invoked': [],
            }

            # Create sample conversation
            conversation = [
                {'role': 'user', 'content': f'Help me with {session["title"]}', 'timestamp': session['timestamp']},
                {'role': 'assistant', 'content': f'I\'ll help you {session["description"]}', 'timestamp': session['timestamp']},
            ]

            # Create sample decisions
            decisions = [
                {'decision': f'Use regex-based PII detection for v1.0', 'rationale': 'Simpler than ML, good enough for MVP', 'alternatives': ['spaCy NER', 'LLM-based'], 'outcome': 'Implemented successfully'},
            ]

            # Create sample file changes
            file_changes = [
                {'file': 'scripts/core/privacy_manager.py', 'action': 'created', 'lines_added': 250},
                {'file': 'tests/core/test_privacy.py', 'action': 'created', 'lines_added': 180},
            ]

            cursor.execute(
                """
                INSERT INTO sessions (
                    session_id, timestamp, privacy_level, title, description,
                    conversation_json, metadata_json, decisions_json, file_changes_json,
                    context_summary, embedding_id,
                    duration_minutes, messages_count, files_changed_count, token_count,
                    pii_detected, pii_redacted, gdpr_compliant,
                    access_count, last_accessed,
                    status, checkpoint_id, parent_session_id,
                    created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    session['timestamp'],
                    session['privacy_level'],
                    session['title'],
                    session['description'],
                    json.dumps(conversation),
                    json.dumps(metadata),
                    json.dumps(decisions),
                    json.dumps(file_changes),
                    session['description'],  # context_summary
                    f'emb_{session_id[:8]}',  # embedding_id
                    session['duration_minutes'],
                    session['messages_count'],
                    session['files_changed_count'],
                    session['token_count'],
                    False,  # pii_detected
                    False,  # pii_redacted
                    True,   # gdpr_compliant
                    0,      # access_count
                    None,   # last_accessed
                    'active',
                    session['checkpoint_id'],
                    None,   # parent_session_id
                    session['timestamp'],
                    session['timestamp'],
                )
            )

            session_ids.append(session_id)

            # Add tags
            for tag_name in session['tags']:
                if tag_name in tag_ids:
                    cursor.execute(
                        "INSERT INTO session_tags (session_id, tag_id, created_at) VALUES (?, ?, ?)",
                        (session_id, tag_ids[tag_name], session['timestamp'])
                    )

        conn.commit()
        logger.info(f"Seeded {len(sample_sessions)} sessions")

        return session_ids

    def seed_patterns(self, conn: sqlite3.Connection, session_ids: list, tag_ids: dict) -> list:
        """
        Seed patterns table with sample patterns.

        Args:
            conn: SQLite connection
            session_ids: List of session IDs to link to
            tag_ids: Dictionary mapping tag names to IDs

        Returns:
            List of pattern IDs
        """
        cursor = conn.cursor()
        now = datetime.now(timezone.utc)

        sample_patterns = [
            {
                'type': 'workflow',
                'name': 'Create Python Class with Tests',
                'description': 'Standard workflow for creating new Python class with unit tests',
                'template': 'Create class → Write tests → Implement functionality → Run tests',
                'category': 'python-development',
                'confidence': 0.9,
                'quality_score': 0.85,
                'frequency': 15,
                'reuse_count': 8,
                'success_rate': 0.95,
                'tags': ['python', 'testing', 'feature-dev'],
            },
            {
                'type': 'decision',
                'name': 'Choose PII Detection Method',
                'description': 'Decision pattern for selecting PII detection approach',
                'template': 'Evaluate options (regex vs ML vs LLM) → Choose based on accuracy/complexity tradeoff',
                'category': 'security',
                'confidence': 0.8,
                'quality_score': 0.75,
                'frequency': 3,
                'reuse_count': 1,
                'success_rate': 1.0,
                'tags': ['security', 'privacy-manager'],
            },
            {
                'type': 'code',
                'name': 'Enum-based Configuration',
                'description': 'Use Python Enum for type-safe configuration options',
                'template': 'class ConfigOption(Enum): ...',
                'category': 'python-patterns',
                'confidence': 0.95,
                'quality_score': 0.9,
                'frequency': 20,
                'reuse_count': 12,
                'success_rate': 1.0,
                'tags': ['python'],
            },
        ]

        pattern_ids = []

        for pattern in sample_patterns:
            pattern_id = str(uuid.uuid4())

            # Create pattern JSON
            pattern_json = {
                'name': pattern['name'],
                'type': pattern['type'],
                'template': pattern['template'],
                'examples': [],
                'variations': [],
            }

            cursor.execute(
                """
                INSERT INTO patterns (
                    pattern_id, pattern_type, name, description,
                    pattern_json, template, example,
                    category, tags_csv, confidence, quality_score,
                    frequency, reuse_count, success_rate, last_used,
                    embedding_id, source_session_id, related_patterns_json,
                    version, parent_pattern_id, deprecated,
                    created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pattern_id,
                    pattern['type'],
                    pattern['name'],
                    pattern['description'],
                    json.dumps(pattern_json),
                    pattern['template'],
                    '',  # example
                    pattern['category'],
                    ','.join(pattern['tags']),
                    pattern['confidence'],
                    pattern['quality_score'],
                    pattern['frequency'],
                    pattern['reuse_count'],
                    pattern['success_rate'],
                    now.isoformat(),
                    f'emb_pattern_{pattern_id[:8]}',
                    session_ids[0] if session_ids else None,
                    '[]',  # related_patterns_json
                    1,     # version
                    None,  # parent_pattern_id
                    False, # deprecated
                    now.isoformat(),
                    now.isoformat(),
                )
            )

            pattern_ids.append(pattern_id)

            # Add tags
            for tag_name in pattern['tags']:
                if tag_name in tag_ids:
                    cursor.execute(
                        "INSERT INTO pattern_tags (pattern_id, tag_id, created_at) VALUES (?, ?, ?)",
                        (pattern_id, tag_ids[tag_name], now.isoformat())
                    )

        conn.commit()
        logger.info(f"Seeded {len(sample_patterns)} patterns")

        return pattern_ids

    def seed(self, reset: bool = False) -> None:
        """
        Seed database with sample data.

        Args:
            reset: Clear existing data before seeding

        Raises:
            DatabaseSeedError: If seeding operation fails
        """
        conn = None
        try:
            logger.info("Starting database seeding...")
            conn = self.connect()
            logger.info(f"Connected to database: {self.db_path}")

            # Clear data if requested
            if reset:
                logger.warning("RESET FLAG DETECTED - Clearing all data")
                self.clear_data(conn)

            # Seed in order (respecting foreign keys)
            logger.info("Seeding database with sample data...")

            tag_ids = self.seed_tags(conn)
            checkpoint_ids = self.seed_checkpoints(conn)
            session_ids = self.seed_sessions(conn, checkpoint_ids, tag_ids)
            pattern_ids = self.seed_patterns(conn, session_ids, tag_ids)

            # Success
            logger.info("✅ Database seeded successfully")
            logger.info(f"  - {len(tag_ids)} tags")
            logger.info(f"  - {len(checkpoint_ids)} checkpoints")
            logger.info(f"  - {len(session_ids)} sessions")
            logger.info(f"  - {len(pattern_ids)} patterns")

        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise
        except sqlite3.Error as e:
            logger.error(f"Database error during seeding: {e}")
            raise DatabaseSeedError(f"Database error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during seeding: {e}", exc_info=True)
            raise DatabaseSeedError(f"Database seeding failed: {e}")
        finally:
            # Always close connection
            if conn:
                try:
                    conn.close()
                    logger.debug("Database connection closed")
                except Exception as e:
                    logger.warning(f"Error closing connection: {e}")


def main():
    """Main entry point."""
    try:
        parser = argparse.ArgumentParser(
            description='Seed CODITECT MEMORY-CONTEXT database with sample data'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Clear existing data before seeding'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed progress'
        )
        parser.add_argument(
            '--db-path',
            type=str,
            default=None,
            help='Custom database path (default: MEMORY-CONTEXT/memory-context.db)'
        )

        args = parser.parse_args()

        # Determine database path
        if args.db_path:
            db_path = Path(args.db_path)
        else:
            db_path = PROJECT_ROOT / "MEMORY-CONTEXT" / "memory-context.db"

        logger.info(f"Starting seeding operation for: {db_path}")

        # Seed database
        seeder = DatabaseSeeder(
            db_path=db_path,
            verbose=args.verbose
        )

        seeder.seed(reset=args.reset)

        print()
        print("=" * 70)
        print("DATABASE SEEDING COMPLETE")
        print("=" * 70)
        print()
        print(f"Database: {db_path}")
        print()
        print("Sample data added:")
        print("  - Tags (21): python, javascript, react, etc.")
        print("  - Checkpoints (2): Sprint +1 Day 1-2 completions")
        print("  - Sessions (3): Privacy Manager, Database Design, Bug Fix")
        print("  - Patterns (3): Workflow, Decision, Code patterns")
        print()
        print("Next steps:")
        print("  1. Query data: sqlite3 MEMORY-CONTEXT/memory-context.db")
        print("  2. Test views: SELECT * FROM v_active_sessions;")
        print("  3. Setup ChromaDB: python3 scripts/core/chromadb_setup.py")
        print()
        return 0

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        print()
        print("=" * 70)
        print("DATABASE SEEDING FAILED - VALIDATION ERROR")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_seed.log for details")
        print()
        return 1
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        print()
        print("=" * 70)
        print("DATABASE SEEDING FAILED - CONNECTION ERROR")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_seed.log for details")
        print()
        return 1
    except DatabaseSeedError as e:
        logger.error(f"Seeding error: {e}")
        print()
        print("=" * 70)
        print("DATABASE SEEDING FAILED")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_seed.log for details")
        print()
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print()
        print("=" * 70)
        print("DATABASE SEEDING FAILED - UNEXPECTED ERROR")
        print("=" * 70)
        print()
        print(f"❌ Unexpected error: {e}")
        print(f"See db_seed.log for details")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
