#!/usr/bin/env python3
"""
Comprehensive Git Staging Manager

Ensures ALL modified files are staged for commit, including:
- Checkpoint files and indexes
- MANIFEST.json files (dashboard dependencies)
- Dedup state (global_hashes.json, checkpoint_index.json, unique_messages.jsonl)
- Session files and exports
- README and documentation
- Any other modified tracked files

Provides detailed logging for every file staged (or skipped) with success/error tracking.

Author: AZ1.AI INC (Hal Casteel)
Framework: CODITECT
License: MIT
"""

import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class GitStagingResult:
    """Result of git staging operation."""
    success: bool
    files_staged: List[str] = field(default_factory=list)
    files_skipped: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    total_files: int = 0


class GitStagingManager:
    """
    Manages comprehensive git staging with detailed logging.

    Ensures no files are missed during commit preparation.
    """

    # Critical files that MUST be staged if modified
    CRITICAL_PATHS = [
        # Checkpoint system
        "MEMORY-CONTEXT/checkpoints/",
        "MEMORY-CONTEXT/dedup_state/checkpoint_index.json",

        # Dashboard indexes (CRITICAL - don't miss!)
        "MEMORY-CONTEXT/messages/MANIFEST.json",
        "MEMORY-CONTEXT/messages/by-checkpoint/MANIFEST.json",

        # Dedup state
        "MEMORY-CONTEXT/dedup_state/global_hashes.json",
        "MEMORY-CONTEXT/dedup_state/unique_messages.jsonl",

        # Session and message storage
        "MEMORY-CONTEXT/messages/",
        "MEMORY-CONTEXT/sessions/",
        "MEMORY-CONTEXT/backups/",

        # Documentation
        "README.md",
        "CLAUDE.md",
        ".coditect/",
    ]

    def __init__(self, repo_root: Path, logger: logging.Logger):
        """
        Initialize git staging manager.

        Args:
            repo_root: Repository root directory
            logger: Logger instance
        """
        self.repo_root = Path(repo_root)
        self.logger = logger

    def get_modified_files(self) -> Tuple[Set[str], Set[str], Set[str]]:
        """
        Get all modified, untracked, and deleted files.

        Returns:
            Tuple of (modified_files, untracked_files, deleted_files)
        """
        self.logger.debug("Detecting modified files with git status")

        try:
            # Use porcelain format for reliable parsing
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=10
            )

            if result.returncode != 0:
                self.logger.error(f"Git status failed: {result.stderr}")
                return set(), set(), set()

            modified_files = set()
            untracked_files = set()
            deleted_files = set()

            for line in result.stdout.splitlines():
                if not line.strip():
                    continue

                # Parse git status format: "XY filename"
                status = line[:2]
                filename = line[3:].strip()

                # Remove quotes if present
                if filename.startswith('"') and filename.endswith('"'):
                    filename = filename[1:-1]

                # Classify by status
                if status[0] == '?' or status[1] == '?':
                    untracked_files.add(filename)
                elif status[0] == 'D' or status[1] == 'D':
                    deleted_files.add(filename)
                else:
                    modified_files.add(filename)

            self.logger.info(f"✓ Detected {len(modified_files)} modified, {len(untracked_files)} untracked, {len(deleted_files)} deleted files")
            self.logger.debug(f"  Modified: {', '.join(sorted(modified_files)[:5])}..." if modified_files else "  Modified: none")
            self.logger.debug(f"  Untracked: {', '.join(sorted(untracked_files)[:5])}..." if untracked_files else "  Untracked: none")
            self.logger.debug(f"  Deleted: {', '.join(sorted(deleted_files)[:5])}..." if deleted_files else "  Deleted: none")

            return modified_files, untracked_files, deleted_files

        except subprocess.TimeoutExpired:
            self.logger.error("Git status command timed out")
            return set(), set(), set()
        except Exception as e:
            self.logger.error(f"Failed to detect modified files: {e}")
            return set(), set(), set()

    def verify_critical_files_staged(self, staged_files: Set[str]) -> List[str]:
        """
        Verify all critical paths are staged if they were modified.

        Args:
            staged_files: Set of files that were staged

        Returns:
            List of critical files that are missing from staging
        """
        self.logger.debug("Verifying critical files are staged")

        missing_critical = []

        for critical_path in self.CRITICAL_PATHS:
            # Check if any staged file matches this critical path
            matches = [f for f in staged_files if f.startswith(critical_path)]

            if not matches:
                # Check if this critical path was actually modified
                try:
                    result = subprocess.run(
                        ["git", "status", "--porcelain", critical_path],
                        capture_output=True,
                        text=True,
                        cwd=self.repo_root,
                        timeout=5
                    )

                    if result.stdout.strip():
                        # Critical file was modified but not staged!
                        missing_critical.append(critical_path)
                        self.logger.warning(f"⚠️  Critical file modified but not staged: {critical_path}")
                except Exception as e:
                    self.logger.debug(f"Could not check {critical_path}: {e}")

        if missing_critical:
            self.logger.error(f"❌ {len(missing_critical)} critical files not staged:")
            for path in missing_critical:
                self.logger.error(f"   - {path}")
        else:
            self.logger.info("✓ All critical files verified staged")

        return missing_critical

    def stage_all_changes(self, include_untracked: bool = True) -> GitStagingResult:
        """
        Stage all changes comprehensively with detailed logging.

        Args:
            include_untracked: Whether to stage untracked files

        Returns:
            GitStagingResult with detailed success/failure information
        """
        result = GitStagingResult(success=False)

        self.logger.info("=" * 60)
        self.logger.info("Starting comprehensive git staging")
        self.logger.info("=" * 60)

        # Step 1: Detect all modified files
        modified, untracked, deleted = self.get_modified_files()
        result.total_files = len(modified) + len(untracked) + len(deleted)

        if result.total_files == 0:
            self.logger.info("✓ No files to stage (repository is clean)")
            result.success = True
            return result

        self.logger.info(f"\n📋 Files to stage: {result.total_files} total")
        self.logger.info(f"   • Modified/Added: {len(modified)}")
        self.logger.info(f"   • Untracked: {len(untracked)}")
        self.logger.info(f"   • Deleted: {len(deleted)}")

        # Step 2: Stage modified and deleted files (tracked files)
        if modified or deleted:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("Staging modified and deleted files")
            self.logger.info("=" * 60)

            try:
                # Use git add -u to stage all tracked file changes
                self.logger.debug("Running: git add -u")
                cmd_result = subprocess.run(
                    ["git", "add", "-u"],
                    capture_output=True,
                    text=True,
                    cwd=self.repo_root,
                    timeout=30
                )

                if cmd_result.returncode == 0:
                    result.files_staged.extend(modified)
                    result.files_staged.extend(deleted)
                    self.logger.info(f"✓ Staged {len(modified) + len(deleted)} tracked file changes")

                    # Log each file for audit trail
                    for filename in sorted(modified):
                        self.logger.debug(f"  ✓ Staged (modified): {filename}")
                    for filename in sorted(deleted):
                        self.logger.debug(f"  ✓ Staged (deleted): {filename}")
                else:
                    error_msg = f"git add -u failed: {cmd_result.stderr}"
                    self.logger.error(f"❌ {error_msg}")
                    result.errors.append(error_msg)
                    return result

            except subprocess.TimeoutExpired:
                error_msg = "git add -u timed out (>30s)"
                self.logger.error(f"❌ {error_msg}")
                result.errors.append(error_msg)
                return result
            except Exception as e:
                error_msg = f"Failed to stage tracked files: {e}"
                self.logger.error(f"❌ {error_msg}")
                result.errors.append(error_msg)
                return result

        # Step 3: Stage untracked files (if requested)
        if include_untracked and untracked:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("Staging untracked files")
            self.logger.info("=" * 60)

            for filename in sorted(untracked):
                try:
                    self.logger.debug(f"Staging: {filename}")
                    cmd_result = subprocess.run(
                        ["git", "add", filename],
                        capture_output=True,
                        text=True,
                        cwd=self.repo_root,
                        timeout=5
                    )

                    if cmd_result.returncode == 0:
                        result.files_staged.append(filename)
                        self.logger.debug(f"  ✓ Staged (untracked): {filename}")
                    else:
                        result.files_skipped.append(filename)
                        self.logger.warning(f"  ⚠️  Skipped: {filename} ({cmd_result.stderr.strip()})")

                except Exception as e:
                    result.files_skipped.append(filename)
                    self.logger.warning(f"  ⚠️  Failed to stage {filename}: {e}")

            self.logger.info(f"✓ Staged {len([f for f in result.files_staged if f in untracked])} untracked files")

        # Step 4: Verify critical files
        self.logger.info("\n" + "=" * 60)
        self.logger.info("Verifying critical files are staged")
        self.logger.info("=" * 60)

        staged_set = set(result.files_staged)
        missing_critical = self.verify_critical_files_staged(staged_set)

        if missing_critical:
            # Try to stage missing critical files explicitly
            self.logger.warning(f"⚠️  Attempting to stage {len(missing_critical)} missing critical files")

            for critical_path in missing_critical:
                try:
                    cmd_result = subprocess.run(
                        ["git", "add", critical_path],
                        capture_output=True,
                        text=True,
                        cwd=self.repo_root,
                        timeout=5
                    )

                    if cmd_result.returncode == 0:
                        result.files_staged.append(critical_path)
                        self.logger.info(f"  ✓ Recovered and staged: {critical_path}")
                    else:
                        error_msg = f"Failed to stage critical file {critical_path}: {cmd_result.stderr}"
                        result.errors.append(error_msg)
                        self.logger.error(f"  ❌ {error_msg}")
                except Exception as e:
                    error_msg = f"Exception staging critical file {critical_path}: {e}"
                    result.errors.append(error_msg)
                    self.logger.error(f"  ❌ {error_msg}")

        # Step 5: Final verification with git status
        self.logger.info("\n" + "=" * 60)
        self.logger.info("Final staging verification")
        self.logger.info("=" * 60)

        try:
            verify_result = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=10
            )

            if verify_result.returncode == 0:
                actually_staged = set(verify_result.stdout.splitlines())
                self.logger.info(f"✓ Git reports {len(actually_staged)} files staged")

                # Check for discrepancies
                expected_staged = set(result.files_staged)
                if actually_staged != expected_staged:
                    extra = actually_staged - expected_staged
                    missing = expected_staged - actually_staged

                    if extra:
                        self.logger.warning(f"⚠️  {len(extra)} extra files staged: {', '.join(list(extra)[:5])}")
                    if missing:
                        self.logger.warning(f"⚠️  {len(missing)} expected files not staged: {', '.join(list(missing)[:5])}")

            else:
                self.logger.warning(f"⚠️  Could not verify staging: {verify_result.stderr}")

        except Exception as e:
            self.logger.warning(f"⚠️  Verification failed: {e}")

        # Determine overall success
        result.success = (len(result.errors) == 0)

        # Final summary
        self.logger.info("\n" + "=" * 60)
        self.logger.info("Git Staging Summary")
        self.logger.info("=" * 60)
        self.logger.info(f"Status: {'✅ SUCCESS' if result.success else '❌ FAILED'}")
        self.logger.info(f"Files staged: {len(result.files_staged)}")
        self.logger.info(f"Files skipped: {len(result.files_skipped)}")
        self.logger.info(f"Errors: {len(result.errors)}")

        if result.errors:
            self.logger.error("\nErrors encountered:")
            for error in result.errors:
                self.logger.error(f"  • {error}")

        return result


if __name__ == "__main__":
    """Test git staging manager"""
    import sys

    # Setup basic logging for testing
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Get repo root (assume we're in scripts/core/)
    repo_root = Path(__file__).resolve().parents[4]
    logger.info(f"Testing in repository: {repo_root}")

    # Create staging manager
    manager = GitStagingManager(repo_root, logger)

    # Test staging
    result = manager.stage_all_changes(include_untracked=False)

    # Exit with appropriate code
    sys.exit(0 if result.success else 1)
