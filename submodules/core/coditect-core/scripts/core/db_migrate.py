#!/usr/bin/env python3
"""
CODITECT MEMORY-CONTEXT Database Migrations

Manages database schema migrations using Alembic.
Supports forward and backward migrations for schema versioning.

Usage:
    python3 scripts/core/db_migrate.py init          # Initialize migrations
    python3 scripts/core/db_migrate.py upgrade        # Upgrade to latest
    python3 scripts/core/db_migrate.py downgrade      # Downgrade one version
    python3 scripts/core/db_migrate.py current        # Show current version
    python3 scripts/core/db_migrate.py history        # Show migration history

Dependencies:
    pip install alembic

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 3
Date: 2025-11-16
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseMigrator:
    """Manage database migrations."""

    def __init__(self, db_path: Path):
        """
        Initialize database migrator.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.migrations_dir = PROJECT_ROOT / "MEMORY-CONTEXT" / "migrations"
        self.alembic_ini = PROJECT_ROOT / "alembic.ini"

        # Import Alembic (late import to provide clear error if not installed)
        try:
            from alembic.config import Config
            from alembic import command
            self.Config = Config
            self.command = command
        except ImportError:
            raise ImportError(
                "Alembic not installed. Install with:\n"
                "  pip install alembic"
            )

    def get_config(self) -> 'Config':
        """
        Get Alembic configuration.

        Returns:
            Alembic Config object
        """
        # Create alembic.ini if it doesn't exist
        if not self.alembic_ini.exists():
            self._create_alembic_ini()

        config = self.Config(str(self.alembic_ini))
        config.set_main_option("script_location", str(self.migrations_dir))
        config.set_main_option(
            "sqlalchemy.url",
            f"sqlite:///{self.db_path}"
        )

        return config

    def _create_alembic_ini(self):
        """Create alembic.ini configuration file."""
        alembic_ini_content = f"""# Alembic configuration for CODITECT MEMORY-CONTEXT

[alembic]
script_location = {self.migrations_dir}
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = sqlite:///{self.db_path}

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %%(levelname)-5.5s [%%(name)s] %%(message)s
datefmt = %%H:%%M:%%S
"""

        with open(self.alembic_ini, 'w') as f:
            f.write(alembic_ini_content)

        logger.info(f"Created alembic.ini: {self.alembic_ini}")

    def init(self):
        """Initialize Alembic migrations directory."""
        try:
            config = self.get_config()
            self.command.init(config, str(self.migrations_dir))
            logger.info(f"✅ Initialized migrations directory: {self.migrations_dir}")

            # Create initial migration
            logger.info("Creating initial migration...")
            self.command.revision(
                config,
                message="Initial schema",
                autogenerate=False
            )

            logger.info("✅ Migration initialization complete")

        except Exception as e:
            logger.error(f"❌ Migration initialization failed: {e}")
            raise

    def upgrade(self, revision: str = "head"):
        """
        Upgrade database to a later version.

        Args:
            revision: Revision to upgrade to (default: head)
        """
        try:
            config = self.get_config()
            self.command.upgrade(config, revision)
            logger.info(f"✅ Upgraded database to: {revision}")

        except Exception as e:
            logger.error(f"❌ Database upgrade failed: {e}")
            raise

    def downgrade(self, revision: str = "-1"):
        """
        Downgrade database to a previous version.

        Args:
            revision: Revision to downgrade to (default: -1 = previous)
        """
        try:
            config = self.get_config()
            self.command.downgrade(config, revision)
            logger.info(f"✅ Downgraded database to: {revision}")

        except Exception as e:
            logger.error(f"❌ Database downgrade failed: {e}")
            raise

    def current(self):
        """Show current database version."""
        try:
            config = self.get_config()
            self.command.current(config)

        except Exception as e:
            logger.error(f"❌ Failed to get current version: {e}")
            raise

    def history(self):
        """Show migration history."""
        try:
            config = self.get_config()
            self.command.history(config)

        except Exception as e:
            logger.error(f"❌ Failed to get history: {e}")
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Manage CODITECT MEMORY-CONTEXT database migrations'
    )
    parser.add_argument(
        'command',
        choices=['init', 'upgrade', 'downgrade', 'current', 'history'],
        help='Migration command to execute'
    )
    parser.add_argument(
        '--revision',
        type=str,
        default=None,
        help='Target revision (upgrade/downgrade)'
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

    # Create migrator
    migrator = DatabaseMigrator(db_path=db_path)

    try:
        # Execute command
        if args.command == 'init':
            migrator.init()

        elif args.command == 'upgrade':
            revision = args.revision or "head"
            migrator.upgrade(revision)

        elif args.command == 'downgrade':
            revision = args.revision or "-1"
            migrator.downgrade(revision)

        elif args.command == 'current':
            migrator.current()

        elif args.command == 'history':
            migrator.history()

        print()
        print("=" * 70)
        print("MIGRATION COMMAND COMPLETE")
        print("=" * 70)
        print()

    except ImportError as e:
        print()
        print("=" * 70)
        print("ALEMBIC NOT INSTALLED")
        print("=" * 70)
        print()
        print("Database migrations require Alembic.")
        print()
        print("Install with:")
        print("  pip install alembic")
        print()
        sys.exit(1)

    except Exception as e:
        print()
        print("=" * 70)
        print("MIGRATION COMMAND FAILED")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
