#!/usr/bin/env python3
"""
CODITECT Core Utilities

Shared utility functions for MEMORY-CONTEXT system.

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation Day 5
Date: 2025-11-16
"""

import sys
from pathlib import Path
from typing import Optional
import logging

# Configure logging to output to both stdout and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('coditect-utils.log')
    ]
)
logger = logging.getLogger(__name__)


# Custom exception hierarchy for better error handling
class UtilsError(Exception):
    """Base exception for utility errors."""
    pass


class GitRepositoryNotFoundError(UtilsError):
    """Raised when git repository cannot be found."""
    pass


class InvalidPathError(UtilsError):
    """Raised when path is invalid or inaccessible."""
    pass


def find_git_root(start_path: Optional[Path] = None) -> Path:
    """
    Find git repository root directory.

    Searches upward from start_path (or current directory) for .git directory.

    Args:
        start_path: Starting directory for search. Uses current directory if None.

    Returns:
        Path to git repository root

    Raises:
        GitRepositoryNotFoundError: If no git repository found
        InvalidPathError: If start_path is invalid or inaccessible

    Examples:
        >>> root = find_git_root()
        >>> print(root)
        /Users/user/project

        >>> root = find_git_root(Path("/Users/user/project/src/subdir"))
        >>> print(root)
        /Users/user/project
    """
    try:
        # Input validation
        if start_path is None:
            start_path = Path.cwd()
        else:
            start_path = Path(start_path)

        # Validate path exists
        if not start_path.exists():
            error_msg = f"Start path does not exist: {start_path}"
            logger.error(error_msg)
            raise InvalidPathError(error_msg)

        # Validate path is accessible
        try:
            current = start_path.resolve()
        except (OSError, RuntimeError) as e:
            error_msg = f"Cannot resolve path '{start_path}': {e}"
            logger.error(error_msg)
            raise InvalidPathError(error_msg) from e

        # Walk up directory tree looking for .git
        max_depth = 50  # Safety limit to prevent infinite loops
        depth = 0

        while current != current.parent and depth < max_depth:
            git_dir = current / '.git'

            # Check for .git directory or file (submodules use .git file)
            try:
                if git_dir.exists() or git_dir.is_file():
                    logger.debug(f"Found git root: {current}")
                    return current
            except (OSError, PermissionError) as e:
                logger.warning(f"Cannot access '{git_dir}': {e}")
                # Continue searching parent directories

            current = current.parent
            depth += 1

        # No .git found
        error_msg = (
            f"Could not find git repository root starting from: {start_path}\n"
            f"Searched up to root directory without finding .git"
        )
        logger.error(error_msg)
        raise GitRepositoryNotFoundError(error_msg)

    except (GitRepositoryNotFoundError, InvalidPathError):
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        # Catch unexpected errors
        error_msg = f"Unexpected error while finding git root: {e}"
        logger.error(error_msg, exc_info=True)
        raise UtilsError(error_msg) from e


def validate_git_repository(path: Path) -> bool:
    """
    Validate that path is a git repository.

    Args:
        path: Path to check

    Returns:
        True if path is a git repository, False otherwise

    Raises:
        InvalidPathError: If path does not exist or is inaccessible

    Examples:
        >>> is_repo = validate_git_repository(Path("/Users/user/project"))
        >>> print(is_repo)
        True
    """
    try:
        # Input validation
        if path is None:
            logger.error("Path cannot be None")
            raise InvalidPathError("Path cannot be None")

        path = Path(path)

        # Validate path exists
        if not path.exists():
            logger.debug(f"Path does not exist: {path}")
            return False

        # Check for .git
        git_dir = path / '.git'

        try:
            result = git_dir.exists() or git_dir.is_file()
            if result:
                logger.debug(f"Valid git repository: {path}")
            else:
                logger.debug(f"Not a git repository: {path}")
            return result

        except (OSError, PermissionError) as e:
            logger.warning(f"Cannot access .git in '{path}': {e}")
            return False

    except InvalidPathError:
        raise
    except Exception as e:
        error_msg = f"Unexpected error validating git repository: {e}"
        logger.error(error_msg, exc_info=True)
        raise UtilsError(error_msg) from e


def main():
    """CLI entry point for testing utility functions."""
    import sys

    try:
        # Test find_git_root
        print("Testing find_git_root()...")
        root = find_git_root()
        print(f"✅ Git root found: {root}")

        # Test validate_git_repository
        print(f"\nTesting validate_git_repository({root})...")
        is_valid = validate_git_repository(root)
        print(f"✅ Valid repository: {is_valid}")

        return 0

    except GitRepositoryNotFoundError as e:
        print(f"❌ Git repository not found: {e}", file=sys.stderr)
        return 1
    except InvalidPathError as e:
        print(f"❌ Invalid path: {e}", file=sys.stderr)
        return 1
    except UtilsError as e:
        print(f"❌ Utility error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        logger.error("Unexpected error in main", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
