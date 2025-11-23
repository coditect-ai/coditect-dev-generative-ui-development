#!/usr/bin/env python3
"""
CODITECT MEMORY-CONTEXT Database Backup & Restore

Backs up SQLite database and ChromaDB vector storage.
Supports automated daily backups and restore functionality.

Usage:
    python3 scripts/core/db_backup.py backup           # Create backup
    python3 scripts/core/db_backup.py restore BACKUP   # Restore from backup
    python3 scripts/core/db_backup.py list             # List backups
    python3 scripts/core/db_backup.py cleanup --days 30 # Delete old backups

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 3
Date: 2025-11-16
"""

import os
import sys
import shutil
import argparse
import logging
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('db_backup.log')
    ]
)
logger = logging.getLogger(__name__)

# Custom exceptions
class DatabaseBackupError(Exception):
    """Base exception for database backup errors"""
    pass

class BackupNotFoundError(DatabaseBackupError):
    """Backup file or directory not found"""
    pass

class RestoreError(DatabaseBackupError):
    """Error during restore operation"""
    pass


class DatabaseBackup:
    """Backup and restore CODITECT MEMORY-CONTEXT database."""

    def __init__(self, db_path: Path, chroma_dir: Path, backup_dir: Path):
        """
        Initialize database backup.

        Args:
            db_path: Path to SQLite database
            chroma_dir: Path to ChromaDB directory
            backup_dir: Path to backup storage directory
        """
        self.db_path = Path(db_path)
        self.chroma_dir = Path(chroma_dir)
        self.backup_dir = Path(backup_dir)

        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def get_backup_name(self, timestamp: Optional[datetime] = None) -> str:
        """
        Generate backup name with timestamp.

        Args:
            timestamp: Optional timestamp (default: now)

        Returns:
            Backup name (e.g., "backup_2025-11-16T12-30-45Z")
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        return f"backup_{timestamp.strftime('%Y-%m-%dT%H-%M-%SZ')}"

    def backup_sqlite(self, backup_path: Path) -> None:
        """
        Backup SQLite database using online backup API.

        Args:
            backup_path: Path to backup database file
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")

        # Use SQLite online backup API for consistent backup
        source_conn = sqlite3.connect(str(self.db_path))
        backup_conn = sqlite3.connect(str(backup_path))

        with backup_conn:
            source_conn.backup(backup_conn)

        source_conn.close()
        backup_conn.close()

        logger.info(f"SQLite backup complete: {backup_path.name}")

        # Get backup size
        backup_size_kb = backup_path.stat().st_size / 1024
        logger.info(f"  Backup size: {backup_size_kb:.2f} KB")

    def backup_chromadb(self, backup_path: Path) -> None:
        """
        Backup ChromaDB directory.

        Args:
            backup_path: Path to backup directory
        """
        if not self.chroma_dir.exists():
            logger.warning(f"ChromaDB directory not found: {self.chroma_dir}")
            logger.warning("Skipping ChromaDB backup")
            return

        # Copy entire ChromaDB directory
        shutil.copytree(self.chroma_dir, backup_path, dirs_exist_ok=True)

        logger.info(f"ChromaDB backup complete: {backup_path.name}")

        # Get backup size
        total_size = sum(
            f.stat().st_size
            for f in backup_path.rglob('*')
            if f.is_file()
        )
        backup_size_mb = total_size / (1024 * 1024)
        logger.info(f"  Backup size: {backup_size_mb:.2f} MB")

    def create_backup(self) -> Path:
        """
        Create full backup (SQLite + ChromaDB).

        Returns:
            Path to backup directory

        Raises:
            DatabaseBackupError: If backup creation fails
        """
        backup_path = None
        try:
            logger.info("Starting backup creation...")

            # Generate backup name
            backup_name = self.get_backup_name()
            backup_path = self.backup_dir / backup_name

            # Create backup directory
            logger.debug(f"Creating backup directory: {backup_path}")
            backup_path.mkdir(parents=True, exist_ok=True)

            logger.info(f"Creating backup: {backup_name}")

            # Backup SQLite
            sqlite_backup = backup_path / "memory-context.db"
            self.backup_sqlite(sqlite_backup)

            # Backup ChromaDB
            chromadb_backup = backup_path / "chromadb"
            self.backup_chromadb(chromadb_backup)

            # Create backup metadata
            metadata = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'db_path': str(self.db_path),
                'chroma_dir': str(self.chroma_dir),
                'backup_name': backup_name,
            }

            metadata_file = backup_path / "backup_metadata.txt"
            with open(metadata_file, 'w') as f:
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")

            logger.info(f"✅ Backup created successfully: {backup_path}")

            return backup_path

        except FileNotFoundError as e:
            logger.error(f"File not found during backup: {e}")
            # Clean up partial backup
            if backup_path and backup_path.exists():
                shutil.rmtree(backup_path)
                logger.debug(f"Cleaned up partial backup: {backup_path}")
            raise DatabaseBackupError(f"Backup failed - file not found: {e}")
        except PermissionError as e:
            logger.error(f"Permission denied during backup: {e}")
            raise DatabaseBackupError(f"Backup failed - permission denied: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during backup: {e}", exc_info=True)
            # Clean up partial backup
            if backup_path and backup_path.exists():
                try:
                    shutil.rmtree(backup_path)
                    logger.debug(f"Cleaned up partial backup: {backup_path}")
                except Exception as cleanup_error:
                    logger.warning(f"Could not clean up partial backup: {cleanup_error}")
            raise DatabaseBackupError(f"Backup failed: {e}")

    def restore_sqlite(self, backup_path: Path) -> None:
        """
        Restore SQLite database from backup.

        Args:
            backup_path: Path to backup database file
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")

        # Create backup of current database before restoring
        if self.db_path.exists():
            current_backup = self.db_path.with_suffix('.db.before_restore')
            shutil.copy2(self.db_path, current_backup)
            logger.info(f"Created safety backup: {current_backup.name}")

        # Restore from backup
        shutil.copy2(backup_path, self.db_path)

        logger.info(f"SQLite restore complete: {self.db_path.name}")

    def restore_chromadb(self, backup_path: Path) -> None:
        """
        Restore ChromaDB from backup.

        Args:
            backup_path: Path to backup ChromaDB directory
        """
        if not backup_path.exists():
            logger.warning(f"ChromaDB backup not found: {backup_path}")
            logger.warning("Skipping ChromaDB restore")
            return

        # Create backup of current ChromaDB before restoring
        if self.chroma_dir.exists():
            current_backup = self.chroma_dir.parent / f"{self.chroma_dir.name}.before_restore"
            if current_backup.exists():
                shutil.rmtree(current_backup)
            shutil.copytree(self.chroma_dir, current_backup)
            logger.info(f"Created safety backup: {current_backup.name}")

            # Remove current ChromaDB
            shutil.rmtree(self.chroma_dir)

        # Restore from backup
        shutil.copytree(backup_path, self.chroma_dir)

        logger.info(f"ChromaDB restore complete: {self.chroma_dir.name}")

    def restore_backup(self, backup_name: str) -> None:
        """
        Restore from backup.

        Args:
            backup_name: Name of backup to restore

        Raises:
            BackupNotFoundError: If backup not found
            RestoreError: If restore operation fails
        """
        try:
            logger.info(f"Starting restore from backup: {backup_name}")
            backup_path = self.backup_dir / backup_name

            if not backup_path.exists():
                logger.error(f"Backup not found: {backup_name}")
                raise BackupNotFoundError(f"Backup not found: {backup_name}")

            if not backup_path.is_dir():
                logger.error(f"Backup path is not a directory: {backup_path}")
                raise BackupNotFoundError(f"Invalid backup path: {backup_name}")

            logger.info(f"Restoring from backup: {backup_name}")

            # Restore SQLite
            sqlite_backup = backup_path / "memory-context.db"
            self.restore_sqlite(sqlite_backup)

            # Restore ChromaDB
            chromadb_backup = backup_path / "chromadb"
            self.restore_chromadb(chromadb_backup)

            logger.info(f"✅ Restore completed successfully")

        except BackupNotFoundError:
            raise
        except FileNotFoundError as e:
            logger.error(f"File not found during restore: {e}")
            raise RestoreError(f"Restore failed - file not found: {e}")
        except PermissionError as e:
            logger.error(f"Permission denied during restore: {e}")
            raise RestoreError(f"Restore failed - permission denied: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during restore: {e}", exc_info=True)
            raise RestoreError(f"Restore failed: {e}")

    def list_backups(self) -> List[dict]:
        """
        List all available backups.

        Returns:
            List of backup metadata dictionaries
        """
        backups = []

        for backup_path in sorted(self.backup_dir.glob("backup_*")):
            if backup_path.is_dir():
                # Read metadata
                metadata_file = backup_path / "backup_metadata.txt"
                metadata = {'name': backup_path.name, 'path': str(backup_path)}

                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        for line in f:
                            if ':' in line:
                                key, value = line.strip().split(':', 1)
                                metadata[key.strip()] = value.strip()

                # Get size
                total_size = sum(
                    f.stat().st_size
                    for f in backup_path.rglob('*')
                    if f.is_file()
                )
                metadata['size_mb'] = total_size / (1024 * 1024)

                backups.append(metadata)

        return backups

    def cleanup_old_backups(self, days: int = 30) -> int:
        """
        Delete backups older than specified days.

        Args:
            days: Delete backups older than this many days

        Returns:
            Number of backups deleted
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        deleted_count = 0

        for backup in self.list_backups():
            backup_timestamp = datetime.fromisoformat(backup.get('timestamp', ''))

            if backup_timestamp < cutoff_date:
                backup_path = Path(backup['path'])
                shutil.rmtree(backup_path)
                logger.info(f"Deleted old backup: {backup['name']}")
                deleted_count += 1

        if deleted_count > 0:
            logger.info(f"✅ Cleaned up {deleted_count} old backups")
        else:
            logger.info("No old backups to clean up")

        return deleted_count


def main():
    """Main entry point."""
    try:
        parser = argparse.ArgumentParser(
            description='Backup and restore CODITECT MEMORY-CONTEXT database'
        )
        parser.add_argument(
            'command',
            choices=['backup', 'restore', 'list', 'cleanup'],
            help='Command to execute'
        )
        parser.add_argument(
            'backup_name',
            nargs='?',
            help='Backup name (required for restore)'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete backups older than N days (cleanup command)'
        )
        parser.add_argument(
            '--db-path',
            type=str,
            default=None,
            help='Custom database path'
        )
        parser.add_argument(
            '--chroma-dir',
            type=str,
            default=None,
            help='Custom ChromaDB directory'
        )
        parser.add_argument(
            '--backup-dir',
            type=str,
            default=None,
            help='Custom backup directory'
        )

        args = parser.parse_args()

        # Determine paths
        db_path = Path(args.db_path) if args.db_path else PROJECT_ROOT / "MEMORY-CONTEXT" / "memory-context.db"
        chroma_dir = Path(args.chroma_dir) if args.chroma_dir else PROJECT_ROOT / "MEMORY-CONTEXT" / "chromadb"
        backup_dir = Path(args.backup_dir) if args.backup_dir else PROJECT_ROOT / "MEMORY-CONTEXT" / "backups"

        logger.info(f"Starting {args.command} operation")

        # Create backup handler
        backup = DatabaseBackup(
            db_path=db_path,
            chroma_dir=chroma_dir,
            backup_dir=backup_dir
        )

        # Execute command
        if args.command == 'backup':
            backup_path = backup.create_backup()
            print()
            print("=" * 70)
            print("BACKUP CREATED")
            print("=" * 70)
            print()
            print(f"Backup location: {backup_path}")
            print()
            return 0

        elif args.command == 'restore':
            if not args.backup_name:
                logger.error("Backup name required for restore")
                print("❌ Error: backup_name required for restore", file=sys.stderr)
                print("Usage: db_backup.py restore <backup_name>", file=sys.stderr)
                print("Run 'db_backup.py list' to see available backups", file=sys.stderr)
                return 1

            backup.restore_backup(args.backup_name)
            print()
            print("=" * 70)
            print("RESTORE COMPLETE")
            print("=" * 70)
            print()
            return 0

        elif args.command == 'list':
            backups = backup.list_backups()

            print()
            print("=" * 70)
            print("AVAILABLE BACKUPS")
            print("=" * 70)
            print()

            if not backups:
                print("No backups found.")
            else:
                for b in backups:
                    print(f"Backup: {b['name']}")
                    print(f"  Created: {b.get('timestamp', 'Unknown')}")
                    print(f"  Size: {b.get('size_mb', 0):.2f} MB")
                    print()
            return 0

        elif args.command == 'cleanup':
            deleted = backup.cleanup_old_backups(days=args.days)
            print()
            print("=" * 70)
            print("CLEANUP COMPLETE")
            print("=" * 70)
            print()
            print(f"Deleted {deleted} backups older than {args.days} days")
            print()
            return 0

    except BackupNotFoundError as e:
        logger.error(f"Backup not found: {e}")
        print()
        print("=" * 70)
        print("BACKUP NOT FOUND")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_backup.log for details")
        print()
        return 1
    except RestoreError as e:
        logger.error(f"Restore error: {e}")
        print()
        print("=" * 70)
        print("RESTORE FAILED")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_backup.log for details")
        print()
        return 1
    except DatabaseBackupError as e:
        logger.error(f"Backup/restore error: {e}")
        print()
        print("=" * 70)
        print("OPERATION FAILED")
        print("=" * 70)
        print()
        print(f"❌ Error: {e}")
        print(f"See db_backup.log for details")
        print()
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print()
        print("=" * 70)
        print("COMMAND FAILED - UNEXPECTED ERROR")
        print("=" * 70)
        print()
        print(f"❌ Unexpected error: {e}")
        print(f"See db_backup.log for details")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
