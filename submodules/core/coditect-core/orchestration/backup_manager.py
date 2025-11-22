"""
Backup Manager - Permanent Backup Archive & Rollback
====================================================

Provides permanent backup archival and point-in-time rollback functionality
for project orchestration state.

Features:
- ✅ Permanent Archive (backups NEVER auto-deleted)
- ✅ Timestamped Backups (every state change)
- ✅ Easy Rollback (restore to any point in time)
- ✅ Organized Storage (dedicated backups/ directory)
- ✅ Metadata Tracking (backup size, task count, completion %)

Example:
    >>> from claude.orchestration import BackupManager
    >>>
    >>> manager = BackupManager(state_file="project_state.json")
    >>>
    >>> # Create backup
    >>> metadata = manager.create_backup()
    >>> print(f"Backup created: {metadata.timestamp}")
    >>>
    >>> # List backups
    >>> backups = manager.list_backups()
    >>> for backup in backups:
    ...     print(f"{backup.timestamp}: {backup.total_tasks} tasks")
    >>>
    >>> # Rollback to specific backup
    >>> success = manager.rollback_to_backup("20251112-013045")

Storage Strategy:
    - Backups stored in {state_file_dir}/backups/
    - Filename format: project_state.backup.{timestamp}.json
    - NEVER auto-deleted (permanent archive)
    - User controls manual compression/archival
    - ~50KB per backup, 1-5MB for 100 backups

Copyright © 2025 AZ1.AI INC. All rights reserved.
Developer: Hal Casteel, CEO/CTO
Email: 1@az1.ai
"""

import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class BackupMetadata:
    """Metadata for a backup file."""

    timestamp: str
    file_path: Path
    file_size_bytes: int
    total_tasks: int
    completed_tasks: int
    completion_percentage: float
    format_version: int
    project_id: str

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"{self.timestamp} | "
            f"{self.total_tasks} tasks "
            f"({self.completion_percentage:.1f}% complete) | "
            f"{self._format_size(self.file_size_bytes)}"
        )

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size in human-readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"


class BackupManager:
    """
    Permanent backup archive with rollback support.

    Manages timestamped backups of project state with:
    - Permanent storage (never auto-deleted)
    - Easy rollback to any point in time
    - Metadata tracking and reporting
    - Organized directory structure

    Attributes:
        state_file: Path to primary state file
        backups_dir: Path to backups directory

    Example:
        >>> manager = BackupManager(state_file="project_state.json")
        >>> manager.create_backup()
        >>> backups = manager.list_backups()
        >>> manager.rollback_to_backup(backups[-1].timestamp)
    """

    def __init__(self, state_file: Path | str):
        """
        Initialize backup manager.

        Args:
            state_file: Path to primary state file
        """
        self.state_file = Path(state_file)
        self.backups_dir = self.state_file.parent / "backups"

        # Ensure backups directory exists
        self.backups_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self) -> Optional[BackupMetadata]:
        """
        Create timestamped backup of current state.

        Backups are PERMANENTLY archived and never auto-deleted.
        User controls manual compression/cleanup.

        Returns:
            BackupMetadata if backup created, None if state file doesn't exist

        Raises:
            IOError: If backup creation fails
        """
        if not self.state_file.exists():
            return None

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Create backup filename
        backup_file = self.backups_dir / f"project_state.backup.{timestamp}.json"

        try:
            # Copy state file to backup
            shutil.copy2(self.state_file, backup_file)

            # Extract metadata from backup
            metadata = self._extract_metadata(backup_file, timestamp)

            return metadata

        except Exception as e:
            raise IOError(f"Failed to create backup: {e}") from e

    def list_backups(self, limit: Optional[int] = None) -> List[BackupMetadata]:
        """
        List all backups in chronological order (newest first).

        Args:
            limit: Maximum number of backups to return (None = all)

        Returns:
            List of BackupMetadata sorted by timestamp (newest first)
        """
        backups = []

        # Find all backup files
        for backup_file in self.backups_dir.glob("project_state.backup.*.json"):
            # Extract timestamp from filename
            # Format: project_state.backup.20251112-013045.json
            try:
                timestamp = backup_file.stem.split(".")[-1]
                metadata = self._extract_metadata(backup_file, timestamp)
                backups.append(metadata)
            except Exception:
                # Skip corrupted/invalid backups
                continue

        # Sort by timestamp (newest first)
        backups.sort(key=lambda b: b.timestamp, reverse=True)

        # Apply limit if specified
        if limit is not None:
            backups = backups[:limit]

        return backups

    def rollback_to_backup(
        self,
        timestamp: str,
        create_pre_rollback_backup: bool = True,
        confirm: bool = True,
    ) -> bool:
        """
        Rollback state to a specific backup.

        Optionally creates a backup of current state before rollback
        (fully reversible operation).

        Args:
            timestamp: Backup timestamp to restore (e.g., "20251112-013045")
            create_pre_rollback_backup: Create backup before rollback
            confirm: Require user confirmation (default: True)

        Returns:
            True if rollback successful, False otherwise

        Raises:
            FileNotFoundError: If backup doesn't exist
            IOError: If rollback fails
        """
        # Find backup file
        backup_file = self.backups_dir / f"project_state.backup.{timestamp}.json"

        if not backup_file.exists():
            raise FileNotFoundError(f"Backup not found: {timestamp}")

        # User confirmation (if enabled)
        if confirm:
            print(f"\n⚠️  WARNING: ROLLBACK TO PREVIOUS STATE")
            print(f"   Current state will be replaced with backup: {timestamp}\n")

            # Load backup metadata
            try:
                metadata = self._extract_metadata(backup_file, timestamp)
                print(f"   Backup details:")
                print(f"   - Timestamp: {metadata.timestamp}")
                print(f"   - Total tasks: {metadata.total_tasks}")
                print(f"   - Completed: {metadata.completed_tasks} ({metadata.completion_percentage:.1f}%)")
                print(f"   - Project ID: {metadata.project_id}")
                print()
            except Exception:
                pass

            response = input(f"Continue with rollback? [y/N]: ")
            if response.lower() != 'y':
                print("Rollback cancelled.")
                return False

        # Create pre-rollback backup (optional, but recommended)
        if create_pre_rollback_backup and self.state_file.exists():
            try:
                pre_rollback_metadata = self.create_backup()
                if pre_rollback_metadata:
                    print(f"\n✅ Current state backed up: {pre_rollback_metadata.timestamp}")
            except Exception as e:
                print(f"\n⚠️  Warning: Failed to create pre-rollback backup: {e}")
                response = input("Continue with rollback anyway? [y/N]: ")
                if response.lower() != 'y':
                    print("Rollback cancelled.")
                    return False

        try:
            # Perform rollback (copy backup to state file)
            shutil.copy2(backup_file, self.state_file)
            print(f"✅ State rolled back to: {timestamp}")
            return True

        except Exception as e:
            raise IOError(f"Rollback failed: {e}") from e

    def delete_backup(self, timestamp: str) -> bool:
        """
        Delete a specific backup.

        WARNING: This is a destructive operation. Deleted backups cannot be recovered.

        Args:
            timestamp: Backup timestamp to delete

        Returns:
            True if deleted, False if backup doesn't exist
        """
        backup_file = self.backups_dir / f"project_state.backup.{timestamp}.json"

        if not backup_file.exists():
            return False

        backup_file.unlink()
        return True

    def compress_old_backups(
        self,
        older_than_days: int = 30,
        keep_every_nth: int = 10,
    ) -> dict:
        """
        Compress old backups to save disk space.

        Strategy:
        - Keep all backups from last N days
        - For older backups, keep every Nth backup
        - Compress deleted backups into tar.gz

        Args:
            older_than_days: Only compress backups older than N days
            keep_every_nth: Keep every Nth backup (delete rest)

        Returns:
            Dictionary with compression stats

        Raises:
            NotImplementedError: Feature not yet implemented
        """
        raise NotImplementedError("Backup compression not yet implemented")

    def _extract_metadata(
        self,
        backup_file: Path,
        timestamp: str,
    ) -> BackupMetadata:
        """
        Extract metadata from backup file.

        Args:
            backup_file: Path to backup file
            timestamp: Backup timestamp

        Returns:
            BackupMetadata instance

        Raises:
            json.JSONDecodeError: If backup file is corrupted
        """
        # Load backup file
        with open(backup_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Get file size
        file_size = backup_file.stat().st_size

        # Extract metrics
        metrics = data.get("metrics", {})
        total_tasks = metrics.get("total_tasks", 0)
        completed_tasks = metrics.get("completed_tasks", 0)
        completion_percentage = metrics.get("completion_percentage", 0.0)

        # Extract metadata
        format_version = data.get("format_version", 1)
        project_id = data.get("project_id", "")

        return BackupMetadata(
            timestamp=timestamp,
            file_path=backup_file,
            file_size_bytes=file_size,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            completion_percentage=completion_percentage,
            format_version=format_version,
            project_id=project_id,
        )
