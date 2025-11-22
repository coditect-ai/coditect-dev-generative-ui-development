#!/usr/bin/env python3
"""
CODITECT Checkpoint Archival System

Automatically archives old checkpoints according to checkpoint.config.json settings.
Implements never-delete policy with audit trail.

Features:
- Automatic archival based on age thresholds
- Year-based organization for historical data
- Audit logging for all operations
- Optional compression for very old files
- Config-driven retention policies

Usage:
    python3 scripts/core/archive-checkpoints.py [--dry-run] [--force-compress]
    python3 scripts/core/archive-checkpoints.py --check  # Preview what would be archived

Author: AZ1.AI CODITECT Team
Framework: MEMORY-CONTEXT
Date: 2025-11-16
"""

import os
import sys
import json
import shutil
import gzip
import argparse
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CheckpointArchiver:
    """
    Automatically archives checkpoints according to retention policies.

    Implements never-delete policy - all files are preserved in archive.
    """

    def __init__(self, repo_root: Optional[Path] = None):
        """
        Initialize CheckpointArchiver.

        Args:
            repo_root: Root directory of repository. Auto-detected if not provided.
        """
        if repo_root is None:
            # Auto-detect repo root
            current = Path.cwd()
            while current != current.parent:
                if (current / '.git').exists() or (current / '.git').is_file():
                    repo_root = current
                    break
                current = current.parent
            else:
                raise ValueError("Could not find git repository root")

        self.repo_root = Path(repo_root)
        self.memory_context_dir = self.repo_root / "MEMORY-CONTEXT"
        self.checkpoints_dir = self.memory_context_dir / "checkpoints"
        self.archive_dir = self.memory_context_dir / "archive"
        self.config_path = self.memory_context_dir / "checkpoint.config.json"

        # Load configuration
        self.config = self._load_config()

        # Setup archive directories
        self.checkpoints_archive_dir = Path(self.config['archive']['checkpoints_dir'])
        self.sessions_archive_dir = Path(self.config['archive']['sessions_dir'])
        self.exports_archive_dir = Path(self.config['archive']['exports_dir'])

        # Audit log
        self.audit_log_path = Path(self.config['audit']['log_file'])

        logger.info(f"CheckpointArchiver initialized for repo: {self.repo_root}")

    def _load_config(self) -> Dict:
        """Load checkpoint configuration."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            config = json.load(f)

        logger.info(f"Loaded config from {self.config_path}")
        return config

    def _log_audit(self, operation: str, details: Dict) -> None:
        """
        Log operation to audit trail.

        Args:
            operation: Operation type (e.g., 'file_archived', 'file_compressed')
            details: Operation details dictionary
        """
        if not self.config['audit']['enabled']:
            return

        # Ensure audit log directory exists
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create audit entry
        timestamp = datetime.now(timezone.utc).isoformat()
        audit_entry = {
            'timestamp': timestamp,
            'operation': operation,
            'details': details
        }

        # Append to audit log
        with open(self.audit_log_path, 'a') as f:
            f.write(json.dumps(audit_entry) + '\n')

        logger.debug(f"Audit logged: {operation}")

    def find_files_to_archive(
        self,
        directory: Path,
        archive_after_days: int
    ) -> List[Tuple[Path, datetime]]:
        """
        Find files older than threshold.

        Args:
            directory: Directory to scan
            archive_after_days: Age threshold in days

        Returns:
            List of (file_path, modification_time) tuples
        """
        if not directory.exists():
            return []

        threshold = datetime.now(timezone.utc) - timedelta(days=archive_after_days)
        old_files = []

        for file_path in directory.glob("*.md"):
            # Get file modification time
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)

            if mtime < threshold:
                old_files.append((file_path, mtime))

        logger.info(f"Found {len(old_files)} files to archive from {directory}")
        return old_files

    def archive_file(
        self,
        file_path: Path,
        archive_base_dir: Path,
        organize_by_year: bool = True,
        dry_run: bool = False
    ) -> Optional[Path]:
        """
        Archive a single file.

        Args:
            file_path: File to archive
            archive_base_dir: Base archive directory
            organize_by_year: Whether to organize by year subdirectories
            dry_run: If True, only simulate archival

        Returns:
            Path where file was archived (or would be archived if dry_run)
        """
        # Determine archive destination
        if organize_by_year:
            # Extract year from filename (ISO-DATETIME format: YYYY-MM-DD...)
            filename = file_path.name
            year = filename[:4] if filename[:4].isdigit() else "unknown"
            dest_dir = archive_base_dir / year
        else:
            dest_dir = archive_base_dir

        dest_path = dest_dir / file_path.name

        if dry_run:
            logger.info(f"[DRY RUN] Would archive: {file_path} → {dest_path}")
            return dest_path

        # Create destination directory
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Move file to archive (preserves modification time)
        shutil.move(str(file_path), str(dest_path))

        # Log audit trail
        self._log_audit('file_archived', {
            'original_path': str(file_path),
            'archive_path': str(dest_path),
            'file_size': dest_path.stat().st_size,
            'modification_time': datetime.fromtimestamp(dest_path.stat().st_mtime).isoformat()
        })

        logger.info(f"Archived: {file_path.name} → {dest_path}")
        return dest_path

    def compress_file(
        self,
        file_path: Path,
        dry_run: bool = False
    ) -> Optional[Path]:
        """
        Compress a file using gzip.

        Args:
            file_path: File to compress
            dry_run: If True, only simulate compression

        Returns:
            Path to compressed file (or would-be path if dry_run)
        """
        compressed_path = file_path.with_suffix(file_path.suffix + '.gz')

        if dry_run:
            logger.info(f"[DRY RUN] Would compress: {file_path} → {compressed_path}")
            return compressed_path

        # Compress file
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove original
        original_size = file_path.stat().st_size
        compressed_size = compressed_path.stat().st_size
        file_path.unlink()

        # Log audit trail
        self._log_audit('file_compressed', {
            'original_path': str(file_path),
            'compressed_path': str(compressed_path),
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': f"{(1 - compressed_size/original_size) * 100:.1f}%"
        })

        logger.info(f"Compressed: {file_path.name} ({original_size} → {compressed_size} bytes)")
        return compressed_path

    def find_files_to_compress(
        self,
        archive_dir: Path,
        compress_after_days: int
    ) -> List[Path]:
        """
        Find archived files old enough to compress.

        Args:
            archive_dir: Archive directory to scan
            compress_after_days: Age threshold in days

        Returns:
            List of file paths to compress
        """
        if not archive_dir.exists():
            return []

        threshold = datetime.now(timezone.utc) - timedelta(days=compress_after_days)
        old_files = []

        # Recursively find .md files (not already compressed)
        for file_path in archive_dir.rglob("*.md"):
            # Skip if already has .gz companion
            if file_path.with_suffix(file_path.suffix + '.gz').exists():
                continue

            # Check file age
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
            if mtime < threshold:
                old_files.append(file_path)

        logger.info(f"Found {len(old_files)} files to compress in {archive_dir}")
        return old_files

    def archive_checkpoints(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Archive old checkpoints according to config.

        Args:
            dry_run: If True, only simulate archival

        Returns:
            Dictionary with archival statistics
        """
        stats = {
            'checkpoints_archived': 0,
            'sessions_archived': 0,
            'exports_archived': 0,
            'files_compressed': 0
        }

        # Archive checkpoints
        checkpoint_config = self.config['checkpoints']
        if checkpoint_config['auto_archive']:
            files_to_archive = self.find_files_to_archive(
                self.checkpoints_dir,
                checkpoint_config['archive_after_days']
            )

            for file_path, _ in files_to_archive:
                self.archive_file(
                    file_path,
                    self.checkpoints_archive_dir,
                    organize_by_year=self.config['archive']['organize_by_year'],
                    dry_run=dry_run
                )
                stats['checkpoints_archived'] += 1

        # Archive sessions
        sessions_config = self.config['sessions']
        sessions_dir = self.memory_context_dir / "sessions"
        if sessions_config['auto_archive']:
            files_to_archive = self.find_files_to_archive(
                sessions_dir,
                sessions_config['archive_after_days']
            )

            for file_path, _ in files_to_archive:
                self.archive_file(
                    file_path,
                    self.sessions_archive_dir,
                    organize_by_year=self.config['archive']['organize_by_year'],
                    dry_run=dry_run
                )
                stats['sessions_archived'] += 1

        # Archive exports
        exports_config = self.config['exports']
        exports_dir = self.memory_context_dir / "exports"
        if exports_config['auto_archive']:
            files_to_archive = self.find_files_to_archive(
                exports_dir,
                exports_config['archive_after_days']
            )

            for file_path, _ in files_to_archive:
                self.archive_file(
                    file_path,
                    self.exports_archive_dir,
                    organize_by_year=self.config['archive']['organize_by_year'],
                    dry_run=dry_run
                )
                stats['exports_archived'] += 1

        return stats

    def compress_old_archives(
        self,
        dry_run: bool = False,
        force: bool = False
    ) -> int:
        """
        Compress very old archived files.

        Args:
            dry_run: If True, only simulate compression
            force: If True, compress regardless of compress_after_days setting

        Returns:
            Number of files compressed
        """
        compress_after_days = self.config['archive'].get('compress_after_days', 180)
        if force:
            compress_after_days = 0  # Compress everything

        files_compressed = 0

        # Compress in all archive directories
        for archive_dir in [
            self.checkpoints_archive_dir,
            self.sessions_archive_dir,
            self.exports_archive_dir
        ]:
            files_to_compress = self.find_files_to_compress(archive_dir, compress_after_days)

            for file_path in files_to_compress:
                self.compress_file(file_path, dry_run=dry_run)
                files_compressed += 1

        return files_compressed

    def run(
        self,
        dry_run: bool = False,
        compress: bool = False,
        force_compress: bool = False
    ) -> Dict[str, int]:
        """
        Run complete archival workflow.

        Args:
            dry_run: If True, only simulate operations
            compress: If True, also compress old archives
            force_compress: If True, compress regardless of age

        Returns:
            Statistics dictionary
        """
        logger.info("=" * 80)
        logger.info("CODITECT Checkpoint Archival System")
        logger.info("=" * 80)

        if dry_run:
            logger.info("DRY RUN MODE - No files will be modified")

        # Archive old files
        logger.info("\nArchiving old files...")
        stats = self.archive_checkpoints(dry_run=dry_run)

        # Compress very old files
        if compress or force_compress:
            logger.info("\nCompressing old archives...")
            stats['files_compressed'] = self.compress_old_archives(
                dry_run=dry_run,
                force=force_compress
            )

        # Summary
        logger.info("\n" + "=" * 80)
        logger.info("ARCHIVAL SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Checkpoints archived: {stats['checkpoints_archived']}")
        logger.info(f"Sessions archived: {stats['sessions_archived']}")
        logger.info(f"Exports archived: {stats['exports_archived']}")
        logger.info(f"Files compressed: {stats['files_compressed']}")
        logger.info("=" * 80)

        if not dry_run and stats['checkpoints_archived'] + stats['sessions_archived'] + stats['exports_archived'] > 0:
            logger.info(f"\nAudit log: {self.audit_log_path}")

        return stats


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='CODITECT Checkpoint Archival System - Archive old files according to retention policy'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate archival without modifying files'
    )

    parser.add_argument(
        '--compress',
        action='store_true',
        help='Also compress old archived files'
    )

    parser.add_argument(
        '--force-compress',
        action='store_true',
        help='Force compression of all archives regardless of age'
    )

    parser.add_argument(
        '--check',
        action='store_true',
        help='Preview what would be archived (alias for --dry-run)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # --check is alias for --dry-run
    if args.check:
        args.dry_run = True

    try:
        archiver = CheckpointArchiver()
        stats = archiver.run(
            dry_run=args.dry_run,
            compress=args.compress,
            force_compress=args.force_compress
        )

        return 0

    except Exception as e:
        logger.error(f"Archival failed: {e}", exc_info=args.verbose)
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
