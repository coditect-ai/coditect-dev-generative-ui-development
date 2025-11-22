#!/usr/bin/env python3
"""
CODITECT Core Utilities

Shared utility functions for MEMORY-CONTEXT system.

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 5
Date: 2025-11-16
"""

from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def find_git_root(start_path: Optional[Path] = None) -> Path:
    """
    Find git repository root directory.

    Searches upward from start_path (or current directory) for .git directory.

    Args:
        start_path: Starting directory for search. Uses current directory if None.

    Returns:
        Path to git repository root

    Raises:
        ValueError: If no git repository found

    Examples:
        >>> root = find_git_root()
        >>> print(root)
        /Users/user/project

        >>> root = find_git_root(Path("/Users/user/project/src/subdir"))
        >>> print(root)
        /Users/user/project
    """
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path)

    current = start_path.resolve()

    # Walk up directory tree looking for .git
    while current != current.parent:
        git_dir = current / '.git'

        # Check for .git directory or file (submodules use .git file)
        if git_dir.exists() or git_dir.is_file():
            logger.debug(f"Found git root: {current}")
            return current

        current = current.parent

    # No .git found
    raise ValueError(
        f"Could not find git repository root starting from: {start_path}\n"
        f"Searched up to root directory without finding .git"
    )


def validate_git_repository(path: Path) -> bool:
    """
    Validate that path is a git repository.

    Args:
        path: Path to check

    Returns:
        True if path is a git repository, False otherwise

    Examples:
        >>> is_repo = validate_git_repository(Path("/Users/user/project"))
        >>> print(is_repo)
        True
    """
    git_dir = Path(path) / '.git'
    return git_dir.exists() or git_dir.is_file()
