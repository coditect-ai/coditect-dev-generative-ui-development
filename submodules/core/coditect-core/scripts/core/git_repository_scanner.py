#!/usr/bin/env python3
"""
Git Repository Scanner

Discovers and tracks ALL git repositories under PROJECTS/ directory tree.

Handles:
- Master repository
- All submodules (registered and unregistered)
- Standalone git repositories
- Nested git repositories

Provides comprehensive logging of all repositories and their status.

Author: AZ1.AI INC (Hal Casteel)
Framework: CODITECT
License: MIT
"""

import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Set, Optional
from dataclasses import dataclass, field


@dataclass
class GitRepository:
    """Represents a discovered git repository."""
    path: Path
    name: str
    is_submodule: bool
    is_dirty: bool
    branch: str
    has_uncommitted: bool
    modified_files: List[str] = field(default_factory=list)
    untracked_files: List[str] = field(default_factory=list)


class GitRepositoryScanner:
    """
    Scans directory tree for all git repositories and tracks their status.
    """

    def __init__(self, root_path: Path, logger: logging.Logger):
        """
        Initialize repository scanner.

        Args:
            root_path: Root directory to scan from (usually PROJECTS/)
            logger: Logger instance
        """
        self.root_path = Path(root_path)
        self.logger = logger
        self.repositories: List[GitRepository] = []

    def find_all_repositories(self) -> List[GitRepository]:
        """
        Recursively find ALL .git directories under root_path.

        Returns:
            List of discovered GitRepository objects
        """
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Scanning for git repositories under: {self.root_path}")
        self.logger.info(f"{'='*60}")

        repositories = []
        seen_repos = set()

        try:
            # Find all .git directories
            for git_dir in self.root_path.rglob('.git'):
                # Skip if this is a file (submodule pointer)
                if git_dir.is_file():
                    self.logger.debug(f"Skipping git file (submodule pointer): {git_dir}")
                    continue

                # Get repository path (parent of .git)
                repo_path = git_dir.parent

                # Skip if we've already seen this repo
                repo_key = str(repo_path.resolve())
                if repo_key in seen_repos:
                    continue

                seen_repos.add(repo_key)

                # Analyze repository
                try:
                    repo_info = self._analyze_repository(repo_path)
                    if repo_info:
                        repositories.append(repo_info)
                        self.logger.debug(f"Found repo: {repo_info.name} at {repo_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to analyze repository at {repo_path}: {e}")

        except Exception as e:
            self.logger.error(f"Error scanning for repositories: {e}")

        # Sort by path for consistent ordering
        repositories.sort(key=lambda r: str(r.path))

        self.repositories = repositories

        self.logger.info(f"\n✓ Found {len(repositories)} git repositories")
        self._log_repository_summary()

        return repositories

    def _analyze_repository(self, repo_path: Path) -> Optional[GitRepository]:
        """
        Analyze a single git repository.

        Args:
            repo_path: Path to repository

        Returns:
            GitRepository object or None if analysis fails
        """
        try:
            # Get repository name
            repo_name = repo_path.name

            # Check if this is a submodule
            is_submodule = self._is_submodule(repo_path)

            # Get current branch
            branch = self._get_branch(repo_path)

            # Get repository status
            is_dirty, modified, untracked = self._get_status(repo_path)

            return GitRepository(
                path=repo_path,
                name=repo_name,
                is_submodule=is_submodule,
                is_dirty=is_dirty,
                branch=branch,
                has_uncommitted=(len(modified) > 0 or len(untracked) > 0),
                modified_files=modified,
                untracked_files=untracked
            )

        except Exception as e:
            self.logger.debug(f"Failed to analyze {repo_path}: {e}")
            return None

    def _is_submodule(self, repo_path: Path) -> bool:
        """Check if repository is a git submodule."""
        try:
            # Check if .git is a file (submodule pointer)
            git_path = repo_path / ".git"
            if git_path.is_file():
                return True

            # Check if parent has .gitmodules mentioning this path
            parent = repo_path.parent
            gitmodules = parent / ".gitmodules"

            if gitmodules.exists():
                with open(gitmodules, 'r') as f:
                    content = f.read()
                    if repo_path.name in content:
                        return True

            return False

        except Exception:
            return False

    def _get_branch(self, repo_path: Path) -> str:
        """Get current branch name."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                cwd=repo_path,
                timeout=5
            )

            if result.returncode == 0:
                return result.stdout.strip()

            return "unknown"

        except Exception:
            return "unknown"

    def _get_status(self, repo_path: Path) -> tuple[bool, List[str], List[str]]:
        """
        Get repository status.

        Returns:
            Tuple of (is_dirty, modified_files, untracked_files)
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=repo_path,
                timeout=10
            )

            if result.returncode != 0:
                return False, [], []

            modified = []
            untracked = []

            for line in result.stdout.splitlines():
                if not line.strip():
                    continue

                status = line[:2]
                filename = line[3:].strip()

                if status[0] == '?' or status[1] == '?':
                    untracked.append(filename)
                else:
                    modified.append(filename)

            is_dirty = (len(modified) > 0 or len(untracked) > 0)

            return is_dirty, modified, untracked

        except Exception as e:
            self.logger.debug(f"Failed to get status for {repo_path}: {e}")
            return False, [], []

    def _log_repository_summary(self):
        """Log summary of discovered repositories."""
        if not self.repositories:
            return

        self.logger.info(f"\n{'='*60}")
        self.logger.info("Repository Summary")
        self.logger.info(f"{'='*60}")

        master_repos = [r for r in self.repositories if not r.is_submodule]
        submodules = [r for r in self.repositories if r.is_submodule]
        dirty_repos = [r for r in self.repositories if r.is_dirty]

        self.logger.info(f"Master repositories: {len(master_repos)}")
        self.logger.info(f"Submodules: {len(submodules)}")
        self.logger.info(f"Repositories with changes: {len(dirty_repos)}")

        if dirty_repos:
            self.logger.info(f"\n{'='*60}")
            self.logger.info("Repositories with Uncommitted Changes")
            self.logger.info(f"{'='*60}")

            for repo in dirty_repos:
                self.logger.info(f"\n📦 {repo.name}")
                self.logger.info(f"   Path: {repo.path}")
                self.logger.info(f"   Branch: {repo.branch}")
                self.logger.info(f"   Type: {'Submodule' if repo.is_submodule else 'Master'}")

                if repo.modified_files:
                    self.logger.info(f"   Modified files: {len(repo.modified_files)}")
                    for f in repo.modified_files[:5]:  # Show first 5
                        self.logger.debug(f"     • {f}")
                    if len(repo.modified_files) > 5:
                        self.logger.debug(f"     ... and {len(repo.modified_files) - 5} more")

                if repo.untracked_files:
                    self.logger.info(f"   Untracked files: {len(repo.untracked_files)}")
                    for f in repo.untracked_files[:5]:  # Show first 5
                        self.logger.debug(f"     • {f}")
                    if len(repo.untracked_files) > 5:
                        self.logger.debug(f"     ... and {len(repo.untracked_files) - 5} more")

    def get_repositories_with_changes(self) -> List[GitRepository]:
        """
        Get list of repositories that have uncommitted changes.

        Returns:
            List of GitRepository objects with changes
        """
        return [r for r in self.repositories if r.has_uncommitted]

    def log_all_repositories(self):
        """Log detailed information about ALL repositories."""
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"All {len(self.repositories)} Git Repositories")
        self.logger.info(f"{'='*60}")

        for i, repo in enumerate(self.repositories, 1):
            status_icon = "🔴" if repo.is_dirty else "🟢"
            type_label = "submodule" if repo.is_submodule else "master"

            self.logger.info(f"\n{i}. {status_icon} {repo.name} ({type_label})")
            self.logger.info(f"   Path: {repo.path}")
            self.logger.info(f"   Branch: {repo.branch}")

            if repo.is_dirty:
                self.logger.info(f"   Status: DIRTY ({len(repo.modified_files)} modified, {len(repo.untracked_files)} untracked)")
            else:
                self.logger.info(f"   Status: CLEAN")


if __name__ == "__main__":
    """Test repository scanner"""
    import sys

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Find PROJECTS directory
    # Assume we're in: PROJECTS/coditect-rollout-master/submodules/core/coditect-core/scripts/core/
    projects_dir = Path(__file__).resolve().parents[6]

    if not projects_dir.exists():
        logger.error(f"PROJECTS directory not found: {projects_dir}")
        sys.exit(1)

    logger.info(f"Scanning PROJECTS directory: {projects_dir}")

    # Create scanner
    scanner = GitRepositoryScanner(projects_dir, logger)

    # Find all repositories
    repos = scanner.find_all_repositories()

    # Log detailed information
    scanner.log_all_repositories()

    logger.info(f"\n{'='*60}")
    logger.info(f"Total repositories: {len(repos)}")
    logger.info(f"Repositories with changes: {len(scanner.get_repositories_with_changes())}")
    logger.info(f"{'='*60}")

    sys.exit(0)
