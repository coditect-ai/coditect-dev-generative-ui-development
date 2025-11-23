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
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup dual logging (stdout + file)
log_dir = PROJECT_ROOT / "MEMORY-CONTEXT" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "db_migrate.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# Custom Exception Hierarchy
# ============================================================================

class DatabaseMigrationError(Exception):
    """Base exception for database migration errors."""
    pass


class AlembicNotInstalledError(DatabaseMigrationError):
    """Raised when Alembic is not installed."""
    pass


class MigrationConfigError(DatabaseMigrationError):
    """Raised when migration configuration is invalid."""
    pass


class MigrationExecutionError(DatabaseMigrationError):
    """Raised when migration execution fails."""
    pass


class MigrationRollbackError(DatabaseMigrationError):
    """Raised when rollback fails."""
    pass


class DatabaseConnectionError(DatabaseMigrationError):
    """Raised when database connection fails."""
    pass


class DatabaseMigrator:
    """Manage database migrations."""

    def __init__(self, db_path: Path):
        """
        Initialize database migrator.

        Args:
            db_path: Path to SQLite database file

        Raises:
            AlembicNotInstalledError: If Alembic is not installed
            MigrationConfigError: If configuration is invalid
        """
        try:
            # Validate db_path
            if not db_path:
                raise MigrationConfigError("Database path cannot be empty")

            self.db_path = Path(db_path)
            self.migrations_dir = PROJECT_ROOT / "MEMORY-CONTEXT" / "migrations"
            self.alembic_ini = PROJECT_ROOT / "alembic.ini"

            # Import Alembic (late import to provide clear error if not installed)
            try:
                from alembic.config import Config
                from alembic import command
                self.Config = Config
                self.command = command
            except ImportError as e:
                logger.error("Alembic not installed")
                raise AlembicNotInstalledError(
                    "Alembic not installed. Install with:\n"
                    "  pip install alembic"
                ) from e

            logger.info(f"DatabaseMigrator initialized for: {self.db_path}")

        except Exception as e:
            logger.error(f"Failed to initialize DatabaseMigrator: {e}")
            raise

    def get_config(self) -> 'Config':
        """
        Get Alembic configuration.

        Returns:
            Alembic Config object

        Raises:
            MigrationConfigError: If configuration is invalid
        """
        try:
            # Create alembic.ini if it doesn't exist
            if not self.alembic_ini.exists():
                self._create_alembic_ini()

            # Validate alembic.ini exists
            if not self.alembic_ini.exists():
                raise MigrationConfigError(f"Failed to create alembic.ini at {self.alembic_ini}")

            config = self.Config(str(self.alembic_ini))
            config.set_main_option("script_location", str(self.migrations_dir))
            config.set_main_option(
                "sqlalchemy.url",
                f"sqlite:///{self.db_path}"
            )

            logger.debug(f"Alembic config loaded from: {self.alembic_ini}")
            return config

        except Exception as e:
            logger.error(f"Failed to get Alembic config: {e}")
            raise MigrationConfigError(f"Configuration error: {e}") from e

    def _create_alembic_ini(self):
        """
        Create alembic.ini configuration file.

        Raises:
            MigrationConfigError: If file creation fails
        """
        try:
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

            # Ensure parent directory exists
            self.alembic_ini.parent.mkdir(parents=True, exist_ok=True)

            with open(self.alembic_ini, 'w') as f:
                f.write(alembic_ini_content)

            logger.info(f"Created alembic.ini: {self.alembic_ini}")

        except IOError as e:
            logger.error(f"Failed to create alembic.ini: {e}")
            raise MigrationConfigError(f"Could not create alembic.ini: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error creating alembic.ini: {e}")
            raise MigrationConfigError(f"Configuration file creation failed: {e}") from e

    def init(self):
        """
        Initialize Alembic migrations directory.

        Raises:
            MigrationExecutionError: If initialization fails
        """
        try:
            # Validate migrations directory doesn't already exist
            if self.migrations_dir.exists():
                logger.warning(f"Migrations directory already exists: {self.migrations_dir}")

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
            raise MigrationExecutionError(f"Failed to initialize migrations: {e}") from e

    def upgrade(self, revision: str = "head"):
        """
        Upgrade database to a later version.

        Args:
            revision: Revision to upgrade to (default: head)

        Raises:
            MigrationExecutionError: If upgrade fails
        """
        try:
            # Validate revision format
            if not revision:
                raise MigrationExecutionError("Revision cannot be empty")

            logger.info(f"Starting database upgrade to: {revision}")
            config = self.get_config()
            self.command.upgrade(config, revision)
            logger.info(f"✅ Upgraded database to: {revision}")

        except Exception as e:
            logger.error(f"❌ Database upgrade failed: {e}")
            raise MigrationExecutionError(f"Upgrade to {revision} failed: {e}") from e

    def downgrade(self, revision: str = "-1"):
        """
        Downgrade database to a previous version.

        Args:
            revision: Revision to downgrade to (default: -1 = previous)

        Raises:
            MigrationRollbackError: If downgrade fails
        """
        try:
            # Validate revision format
            if not revision:
                raise MigrationRollbackError("Revision cannot be empty")

            logger.warning(f"Starting database downgrade to: {revision}")
            config = self.get_config()
            self.command.downgrade(config, revision)
            logger.info(f"✅ Downgraded database to: {revision}")

        except Exception as e:
            logger.error(f"❌ Database downgrade failed: {e}")
            raise MigrationRollbackError(f"Downgrade to {revision} failed: {e}") from e

    def current(self):
        """
        Show current database version.

        Raises:
            MigrationExecutionError: If operation fails
        """
        try:
            config = self.get_config()
            self.command.current(config)

        except Exception as e:
            logger.error(f"❌ Failed to get current version: {e}")
            raise MigrationExecutionError(f"Failed to get current version: {e}") from e

    def history(self):
        """
        Show migration history.

        Raises:
            MigrationExecutionError: If operation fails
        """
        try:
            config = self.get_config()
            self.command.history(config)

        except Exception as e:
            logger.error(f"❌ Failed to get history: {e}")
            raise MigrationExecutionError(f"Failed to get migration history: {e}") from e


def main():
    """
    Main entry point.

    Returns:
        Exit code (0 = success, 1 = failure)
    """
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
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    try:
        # Validate database path
        if args.db_path:
            db_path = Path(args.db_path)
            if not db_path.is_absolute():
                logger.error("Database path must be absolute")
                print("\n❌ Error: Database path must be absolute")
                return 1
        else:
            db_path = PROJECT_ROOT / "MEMORY-CONTEXT" / "memory-context.db"

        logger.info(f"Using database: {db_path}")

        # Create migrator
        migrator = DatabaseMigrator(db_path=db_path)

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
        logger.info("Migration command completed successfully")
        return 0

    except AlembicNotInstalledError as e:
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
        logger.error(f"Alembic not installed: {e}")
        return 1

    except MigrationConfigError as e:
        print()
        print("=" * 70)
        print("MIGRATION CONFIGURATION ERROR")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("Check your database path and alembic.ini configuration.")
        print()
        logger.error(f"Configuration error: {e}")
        return 1

    except (MigrationExecutionError, MigrationRollbackError) as e:
        print()
        print("=" * 70)
        print("MIGRATION COMMAND FAILED")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("Check the logs for more details.")
        print(f"Log file: {log_file}")
        print()
        logger.error(f"Migration failed: {e}")
        return 1

    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("MIGRATION INTERRUPTED")
        print("=" * 70)
        print()
        print("Migration was interrupted by user.")
        print("Database may be in inconsistent state.")
        print("Run 'current' command to check status.")
        print()
        logger.warning("Migration interrupted by user")
        return 1

    except Exception as e:
        print()
        print("=" * 70)
        print("UNEXPECTED ERROR")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print(f"Log file: {log_file}")
        print()
        logger.exception("Unexpected error during migration")
        return 1


if __name__ == "__main__":
    sys.exit(main())
