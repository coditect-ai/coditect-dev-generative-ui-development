#!/usr/bin/env python3
"""
CODITECT MEMORY-CONTEXT Database Initialization

Creates SQLite database with schema for sessions, patterns, and checkpoints.
Supports privacy controls, NESTED LEARNING, and context retrieval.

Usage:
    python3 scripts/core/db_init.py [--reset] [--verbose]

Options:
    --reset     Drop existing tables before creating
    --verbose   Show detailed SQL execution

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 3
Date: 2025-11-16
"""

import os
import sys
import sqlite3
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('db_init.log')
    ]
)
logger = logging.getLogger(__name__)

# Custom exceptions
class DatabaseInitError(Exception):
    """Base exception for database initialization errors"""
    pass

class SchemaError(DatabaseInitError):
    """Schema loading or validation error"""
    pass

class ConnectionError(DatabaseInitError):
    """Database connection error"""
    pass


class DatabaseInitializer:
    """Initialize CODITECT MEMORY-CONTEXT database."""

    def __init__(self, db_path: Path, verbose: bool = False):
        """
        Initialize database initializer.

        Args:
            db_path: Path to SQLite database file
            verbose: Enable verbose logging
        """
        self.db_path = Path(db_path)
        self.schema_path = PROJECT_ROOT.parent.parent.parent / "MEMORY-CONTEXT" / "database-schema.sql"
        self.verbose = verbose

        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        if self.verbose:
            logger.setLevel(logging.DEBUG)

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
            conn.row_factory = sqlite3.Row  # Access columns by name
            conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
            logger.info("Database connection established")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise ConnectionError(f"Could not connect to database: {e}")
        except Exception as e:
            logger.error(f"Unexpected error connecting to database: {e}")
            raise DatabaseInitError(f"Database connection error: {e}")

    def load_schema(self) -> str:
        """
        Load SQL schema from file.

        Returns:
            SQL schema as string

        Raises:
            SchemaError: If schema file not found or cannot be read
        """
        try:
            if not self.schema_path.exists():
                logger.error(f"Schema file not found: {self.schema_path}")
                raise SchemaError(
                    f"Schema file not found: {self.schema_path}\n"
                    f"Expected: MEMORY-CONTEXT/database-schema.sql"
                )

            logger.debug(f"Loading schema from: {self.schema_path}")
            with open(self.schema_path, 'r') as f:
                schema_sql = f.read()

            if not schema_sql.strip():
                raise SchemaError("Schema file is empty")

            logger.info(f"Loaded schema from: {self.schema_path}")
            return schema_sql

        except SchemaError:
            raise
        except Exception as e:
            logger.error(f"Failed to load schema: {e}")
            raise SchemaError(f"Could not load schema file: {e}")

    def execute_schema(self, conn: sqlite3.Connection, schema_sql: str) -> None:
        """
        Execute schema SQL statements.

        Args:
            conn: SQLite connection
            schema_sql: SQL schema to execute
        """
        # Split into individual statements (ignore comments)
        statements = []
        current_statement = []

        for line in schema_sql.split('\n'):
            # Skip comment-only lines
            if line.strip().startswith('--'):
                continue

            current_statement.append(line)

            # End of statement (semicolon)
            if line.strip().endswith(';'):
                statement = '\n'.join(current_statement).strip()
                if statement and not statement.startswith('--'):
                    statements.append(statement)
                current_statement = []

        # Execute each statement
        cursor = conn.cursor()
        for i, statement in enumerate(statements, 1):
            try:
                if self.verbose:
                    logger.debug(f"Executing statement {i}/{len(statements)}")
                    logger.debug(f"SQL: {statement[:100]}...")

                cursor.execute(statement)

            except sqlite3.Error as e:
                logger.error(f"Error executing statement {i}")
                logger.error(f"Statement: {statement[:200]}...")
                logger.error(f"Error: {e}")
                raise

        conn.commit()
        logger.info(f"Executed {len(statements)} SQL statements")

    def verify_schema(self, conn: sqlite3.Connection) -> None:
        """
        Verify database schema was created correctly.

        Args:
            conn: SQLite connection

        Raises:
            AssertionError: If schema verification fails
        """
        cursor = conn.cursor()

        # Expected tables
        expected_tables = [
            'sessions',
            'patterns',
            'tags',
            'session_tags',
            'pattern_tags',
            'checkpoints',
            'context_loads',
            'privacy_audit',
            'db_metadata',
        ]

        # Expected views
        expected_views = [
            'v_active_sessions',
            'v_patterns_by_usage',
            'v_recent_checkpoints',
            'v_privacy_audit_summary',
        ]

        # Get existing tables
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        existing_tables = [row[0] for row in cursor.fetchall()]

        # Get existing views
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name"
        )
        existing_views = [row[0] for row in cursor.fetchall()]

        # Verify tables
        missing_tables = set(expected_tables) - set(existing_tables)
        if missing_tables:
            raise AssertionError(
                f"Missing tables: {', '.join(missing_tables)}"
            )

        # Verify views
        missing_views = set(expected_views) - set(existing_views)
        if missing_views:
            raise AssertionError(
                f"Missing views: {', '.join(missing_views)}"
            )

        logger.info(f"✅ Verified {len(expected_tables)} tables")
        logger.info(f"✅ Verified {len(expected_views)} views")

        # Get metadata
        cursor.execute("SELECT key, value FROM db_metadata")
        metadata = {row[0]: row[1] for row in cursor.fetchall()}

        logger.info(f"Database metadata:")
        for key, value in metadata.items():
            logger.info(f"  {key}: {value}")

    def reset_database(self, conn: sqlite3.Connection) -> None:
        """
        Drop all tables and views (for reset).

        Args:
            conn: SQLite connection
        """
        cursor = conn.cursor()

        # Get all tables and views
        cursor.execute(
            "SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view')"
        )
        objects = cursor.fetchall()

        # Drop views first (they depend on tables)
        for name, obj_type in objects:
            if obj_type == 'view':
                cursor.execute(f"DROP VIEW IF EXISTS {name}")
                logger.info(f"Dropped view: {name}")

        # Drop tables
        for name, obj_type in objects:
            if obj_type == 'table':
                cursor.execute(f"DROP TABLE IF EXISTS {name}")
                logger.info(f"Dropped table: {name}")

        conn.commit()
        logger.info("Database reset complete")

    def initialize(self, reset: bool = False) -> None:
        """
        Initialize database with schema.

        Args:
            reset: Drop existing tables before creating

        Raises:
            DatabaseInitError: If initialization fails
        """
        conn = None
        try:
            logger.info("Starting database initialization...")

            # Check if database exists
            db_exists = self.db_path.exists()
            logger.debug(f"Database exists: {db_exists}")

            # Connect to database
            conn = self.connect()
            logger.info(f"Connected to database: {self.db_path}")

            # Reset if requested
            if reset and db_exists:
                logger.warning("RESET FLAG DETECTED - Dropping all tables")
                self.reset_database(conn)

            # Load schema
            schema_sql = self.load_schema()

            # Execute schema
            logger.info("Creating database schema...")
            self.execute_schema(conn, schema_sql)

            # Verify schema
            self.verify_schema(conn)

            # Success
            if reset:
                logger.info("✅ Database reset and initialized successfully")
            else:
                logger.info("✅ Database initialized successfully")

            # Show database info
            db_size_kb = self.db_path.stat().st_size / 1024
            logger.info(f"Database size: {db_size_kb:.2f} KB")
            logger.info(f"Database location: {self.db_path}")

        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise
        except SchemaError as e:
            logger.error(f"Schema error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during initialization: {e}", exc_info=True)
            raise DatabaseInitError(f"Database initialization failed: {e}")
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
            description='Initialize CODITECT MEMORY-CONTEXT database'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Drop existing tables before creating (WARNING: data loss)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed SQL execution'
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
            db_path = PROJECT_ROOT.parent.parent.parent / "MEMORY-CONTEXT" / "memory-context.db"

        # Confirm reset if requested
        if args.reset:
            print()
            print("⚠️  WARNING: --reset flag detected")
            print("⚠️  This will DELETE ALL DATA in the database")
            print(f"⚠️  Database: {db_path}")
            print()
            confirm = input("Type 'yes' to confirm reset: ")
            if confirm.lower() != 'yes':
                print("Cancelled.")
                logger.info("Reset cancelled by user")
                return 0

        # Initialize database
        logger.info(f"Initializing database at: {db_path}")
        initializer = DatabaseInitializer(
            db_path=db_path,
            verbose=args.verbose
        )

        initializer.initialize(reset=args.reset)

        print()
        print("=" * 70)
        print("DATABASE INITIALIZATION COMPLETE")
        print("=" * 70)
        print()
        print(f"Database: {db_path}")
        print(f"Schema: {initializer.schema_path}")
        print()
        print("Next steps:")
        print("  1. Run db_seed.py to add sample data (optional)")
        print("  2. Test with: python3 scripts/core/session_export.py")
        print("  3. Setup ChromaDB with: python3 scripts/core/chromadb_setup.py")
        print()
        return 0

    except ConnectionError as e:
        logger.error(f"Database connection error: {e}")
        print()
        print("=" * 70)
        print("DATABASE INITIALIZATION FAILED - CONNECTION ERROR")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_init.log for details")
        print()
        return 1
    except SchemaError as e:
        logger.error(f"Schema error: {e}")
        print()
        print("=" * 70)
        print("DATABASE INITIALIZATION FAILED - SCHEMA ERROR")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_init.log for details")
        print()
        return 1
    except DatabaseInitError as e:
        logger.error(f"Database initialization error: {e}")
        print()
        print("=" * 70)
        print("DATABASE INITIALIZATION FAILED")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_init.log for details")
        print()
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print()
        print("=" * 70)
        print("DATABASE INITIALIZATION FAILED - UNEXPECTED ERROR")
        print("=" * 70)
        print()
        print(f"❌ Unexpected error: {e}")
        print(f"See db_init.log for details")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
