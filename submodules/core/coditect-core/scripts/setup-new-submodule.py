#!/usr/bin/env python3
"""
Setup New Submodule - Main Orchestration Script

Automates the complete setup of a new CODITECT submodule including directory structure,
symlinks, templates, git initialization, GitHub repository creation, and parent integration.

This script serves as the automated implementation of the `/setup-submodule` command,
enabling both interactive and non-interactive usage.

Usage:
    python3 setup-new-submodule.py --category cloud --name coditect-cloud-service --purpose "API gateway"
    python3 setup-new-submodule.py --interactive
    python3 setup-new-submodule.py --config submodules.yml

Examples:
    # Interactive mode
    python3 setup-new-submodule.py -i

    # Command-line arguments
    python3 setup-new-submodule.py \\
        --category dev \\
        --name coditect-dev-logger \\
        --purpose "Centralized logging utility" \\
        --visibility private

    # From configuration file
    python3 setup-new-submodule.py --config my-submodules.yml

Requirements:
    - Python 3.9+
    - Git installed and configured
    - GitHub CLI (gh) installed and authenticated
    - Write access to coditect-ai organization
    - Current directory must be rollout-master root

Exit Codes:
    0: Success - Submodule created successfully
    1: General error - Setup failed
    2: Usage error - Invalid arguments
    3: Prerequisites not met - Missing requirements
    4: Git operation failed - Git command error
    5: GitHub operation failed - GitHub API/CLI error
"""

import sys
import os
import argparse
import logging
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

# Handle yaml import with auto-installation
try:
    import yaml
except ImportError:
    print("Installing required dependency: pyyaml...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyyaml"], check=True)
    import yaml

# ANSI color codes for output
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

# Global logger (configured later)
logger = None


def setup_logging() -> logging.Logger:
    """
    Setup dual logging to both file and stdout.

    Returns:
        Configured logger instance
    """
    # Create logs directory
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    # Create log file with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = logs_dir / f'setup-new-submodule_{timestamp}.log'

    # Configure logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # File handler - detailed logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler - user-friendly logging
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logging initialized: {log_file}")

    return logger


class SubmoduleSetupError(Exception):
    """Base exception for submodule setup errors."""
    pass


class PrerequisiteError(SubmoduleSetupError):
    """Raised when prerequisites are not met."""
    pass


class GitOperationError(SubmoduleSetupError):
    """Raised when git operation fails."""
    pass


class GitHubOperationError(SubmoduleSetupError):
    """Raised when GitHub operation fails."""
    pass


class RollbackError(SubmoduleSetupError):
    """Raised when rollback operation fails."""
    pass


def retry_operation(max_retries: int = 3, delay: float = 2.0, backoff: float = 2.0):
    """
    Decorator for retrying operations with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay in seconds
        backoff: Backoff multiplier for each retry

    Returns:
        Decorated function with retry logic
    """
    import time
    import functools

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (GitHubOperationError, subprocess.CalledProcessError, OSError) as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        raise

                    print_warning(
                        f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                        f"Retrying in {current_delay:.1f}s..."
                    )
                    if logger:
                        logger.warning(
                            f"Retry attempt {attempt + 1}/{max_retries} failed: {e}"
                        )

                    time.sleep(current_delay)
                    current_delay *= backoff

            # Should not reach here, but raise last exception if it does
            if last_exception:
                raise last_exception

        return wrapper
    return decorator


def print_success(message: str) -> None:
    """Print success message in green."""
    print(f"{GREEN}✓{NC} {message}")


def print_warning(message: str) -> None:
    """Print warning message in yellow."""
    print(f"{YELLOW}⚠{NC} {message}")


def print_error(message: str) -> None:
    """Print error message in red."""
    print(f"{RED}✗{NC} {message}")


def print_info(message: str) -> None:
    """Print info message in blue."""
    print(f"{BLUE}ℹ{NC} {message}")


def run_command(cmd: List[str], cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    """
    Run shell command and return result.

    Args:
        cmd: Command and arguments as list
        cwd: Working directory (default: current)
        check: Raise exception on non-zero exit (default: True)

    Returns:
        CompletedProcess instance with stdout, stderr, returncode

    Raises:
        subprocess.CalledProcessError: If check=True and command fails
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {' '.join(cmd)}")
        logger.error(f"Exit code: {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        raise


def validate_category(category: str) -> bool:
    """
    Validate that category is one of the allowed CODITECT categories.

    Args:
        category: Category name to validate

    Returns:
        True if valid, False otherwise
    """
    valid_categories = ['cloud', 'dev', 'gtm', 'labs', 'docs', 'ops', 'market', 'core']
    return category in valid_categories


def validate_repo_name(name: str, category: str) -> bool:
    """
    Validate repository name follows CODITECT naming convention.

    Args:
        name: Repository name to validate
        category: Category the repository belongs to

    Returns:
        True if valid, False otherwise
    """
    # Must start with coditect-{category}-
    expected_prefix = f"coditect-{category}-"
    if not name.startswith(expected_prefix):
        print_error(f"Repository name validation failed!")
        print_info(f"Expected format: {expected_prefix}<name>")
        print_info(f"Example: {expected_prefix}compliance (produces coditect-{category}-compliance)")
        print_info(f"Full name received: {name}")
        if not name.startswith("coditect-"):
            print_warning(f"Did you forget the 'coditect-{category}-' prefix?")
        return False

    # Must be kebab-case (lowercase with hyphens)
    if not name.islower() or ' ' in name or '_' in name:
        print_error("Repository name must be lowercase with hyphens (kebab-case)")
        print_info(f"Invalid characters found in: {name}")
        return False

    return True


def check_prerequisites() -> None:
    """
    Verify all prerequisites are met before starting setup.

    Checks:
    - Current directory is rollout-master root
    - .coditect directory exists
    - Git is installed and configured
    - GitHub CLI is installed and authenticated

    Raises:
        PrerequisiteError: If any prerequisite is not met
    """
    # Check current directory is rollout-master root
    if not Path('.coditect').is_dir():
        raise PrerequisiteError(
            "Must run from coditect-rollout-master root directory. "
            ".coditect directory not found."
        )

    # Check .coditect has agents
    if not Path('.coditect/agents').is_dir():
        raise PrerequisiteError(".coditect/agents directory not found")

    # Check git is installed
    try:
        run_command(['git', '--version'])
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise PrerequisiteError("Git is not installed or not in PATH")

    # Check git is configured
    try:
        run_command(['git', 'config', 'user.name'])
        run_command(['git', 'config', 'user.email'])
    except subprocess.CalledProcessError:
        raise PrerequisiteError(
            "Git user.name and user.email not configured. "
            "Run: git config --global user.name 'Your Name' && "
            "git config --global user.email 'you@example.com'"
        )

    # Check GitHub CLI is installed
    try:
        run_command(['gh', '--version'])
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise PrerequisiteError(
            "GitHub CLI (gh) is not installed. "
            "Install: brew install gh (macOS) or see https://cli.github.com/"
        )

    # Check GitHub CLI is authenticated
    try:
        result = run_command(['gh', 'auth', 'status'], check=False)
        if result.returncode != 0:
            raise PrerequisiteError(
                "GitHub CLI is not authenticated. "
                "Run: gh auth login"
            )
    except subprocess.CalledProcessError:
        raise PrerequisiteError("Failed to check GitHub CLI authentication")

    print_success("All prerequisites verified")


def create_directory_structure(category: str, repo_name: str) -> Path:
    """
    Create submodule directory structure.

    Args:
        category: Category directory name
        repo_name: Repository name

    Returns:
        Path to created submodule directory

    Raises:
        SubmoduleSetupError: If directory creation fails
    """
    try:
        # Create category directory if doesn't exist
        category_dir = Path('submodules') / category
        category_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Category directory: {category_dir}")

        # Create submodule directory
        submodule_dir = category_dir / repo_name
        if submodule_dir.exists():
            raise SubmoduleSetupError(
                f"Submodule directory already exists: {submodule_dir}"
            )

        submodule_dir.mkdir(parents=True)
        print_success(f"Created directory: {submodule_dir}")

        return submodule_dir

    except Exception as e:
        raise SubmoduleSetupError(f"Failed to create directory structure: {e}")


def create_symlinks(submodule_dir: Path) -> None:
    """
    Create .coditect and .claude symlinks.

    Args:
        submodule_dir: Path to submodule directory

    Raises:
        SubmoduleSetupError: If symlink creation fails
    """
    try:
        # Create .coditect symlink pointing to ../../../.coditect
        coditect_symlink = submodule_dir / '.coditect'
        coditect_symlink.symlink_to('../../../.coditect')
        print_success("Created symlink: .coditect -> ../../../.coditect")

        # Create .claude symlink pointing to .coditect
        claude_symlink = submodule_dir / '.claude'
        claude_symlink.symlink_to('.coditect')
        print_success("Created symlink: .claude -> .coditect")

        # Verify symlinks are accessible
        agents_dir = coditect_symlink / 'agents'
        if not agents_dir.is_dir():
            raise SubmoduleSetupError("Symlink verification failed: agents directory not accessible")

        print_success("Symlink verification passed")

    except Exception as e:
        raise SubmoduleSetupError(f"Failed to create symlinks: {e}")


def generate_templates(submodule_dir: Path, repo_name: str, category: str, purpose: str) -> None:
    """
    Generate project templates (README, PROJECT-PLAN, TASKLIST, .gitignore).

    Args:
        submodule_dir: Path to submodule directory
        repo_name: Repository name
        category: Category name
        purpose: One-sentence purpose description

    Raises:
        SubmoduleSetupError: If template generation fails
    """
    try:
        # Generate README.md
        readme_content = f"""# {repo_name}

**Category:** {category}

## Purpose

{purpose}

## Getting Started

This submodule is part of the CODITECT ecosystem and has access to 50+ agents, 74 commands, and 24 skills via the `.coditect` symlink.

### Prerequisites

- CODITECT rollout-master repository
- Git submodule access

### Quick Start

```bash
# From rollout-master root
cd submodules/{category}/{repo_name}

# Verify CODITECT access
ls .coditect/agents/

# Start development
```

## Documentation

- [PROJECT-PLAN.md](PROJECT-PLAN.md) - Implementation plan
- [TASKLIST.md](TASKLIST.md) - Task tracking

## License

MIT
"""
        (submodule_dir / 'README.md').write_text(readme_content)
        print_success("Created README.md")

        # Generate .gitignore
        gitignore_content = """# Dependencies
node_modules/
venv/
__pycache__/

# Build outputs
dist/
build/
*.pyc

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# CODITECT
# Note: .coditect and .claude are symlinks, not tracked
"""
        (submodule_dir / '.gitignore').write_text(gitignore_content)
        print_success("Created .gitignore")

        # Generate PROJECT-PLAN.md (basic structure)
        project_plan_content = f"""# {repo_name} - Project Plan

**Version:** 1.0
**Status:** 🟡 Planning
**Category:** {category}
**Created:** {datetime.now().strftime('%Y-%m-%d')}

## Overview

**Purpose:** {purpose}

## Phases

### Phase 1: Foundation
- [ ] Setup repository structure
- [ ] Configure development environment
- [ ] Create initial documentation

### Phase 2: Implementation
- [ ] Core functionality
- [ ] Testing
- [ ] Documentation

### Phase 3: Integration
- [ ] Integration with CODITECT ecosystem
- [ ] End-to-end testing
- [ ] Deployment preparation

## Success Criteria

- [ ] All tests passing
- [ ] Documentation complete
- [ ] Integration verified
"""
        (submodule_dir / 'PROJECT-PLAN.md').write_text(project_plan_content)
        print_success("Created PROJECT-PLAN.md")

        # Generate TASKLIST.md
        tasklist_content = f"""# {repo_name} - Task List

## Current Sprint

### Setup (Week 1)
- [x] Create submodule directory
- [x] Establish symlinks
- [x] Generate initial templates
- [ ] Customize PROJECT-PLAN.md
- [ ] Add development tasks

### Development (Week 2+)
- [ ] Define requirements
- [ ] Implement core features
- [ ] Write tests
- [ ] Document APIs

## Backlog

- [ ] Additional features
- [ ] Performance optimization
- [ ] Advanced testing

## Completed

- [x] Submodule setup via CODITECT automation
"""
        (submodule_dir / 'TASKLIST.md').write_text(tasklist_content)
        print_success("Created TASKLIST.md")

    except Exception as e:
        raise SubmoduleSetupError(f"Failed to generate templates: {e}")


def initialize_git_repository(submodule_dir: Path, repo_name: str) -> None:
    """
    Initialize git repository and make initial commit.

    Args:
        submodule_dir: Path to submodule directory
        repo_name: Repository name

    Raises:
        GitOperationError: If git initialization fails
    """
    try:
        # Initialize git repository
        run_command(['git', 'init'], cwd=submodule_dir)

        # Checkout main branch
        run_command(['git', 'checkout', '-b', 'main'], cwd=submodule_dir)

        # Add all files
        run_command(['git', 'add', '.'], cwd=submodule_dir)

        # Make initial commit
        commit_message = f"""Initial commit: CODITECT submodule setup

- Established .coditect and .claude symlinks for distributed intelligence
- Created PROJECT-PLAN.md with phased implementation
- Created TASKLIST.md with checkbox progress tracking
- Created README.md with getting started guide
- Added .gitignore with standard exclusions

Generated with CODITECT framework
"""
        run_command(['git', 'commit', '-m', commit_message], cwd=submodule_dir)

        print_success("Git repository initialized and initial commit made")

    except subprocess.CalledProcessError as e:
        raise GitOperationError(f"Git initialization failed: {e}")


@retry_operation(max_retries=3, delay=2.0)
def create_github_repository(repo_name: str, purpose: str, visibility: str, category: str) -> None:
    """
    Create GitHub repository using GitHub CLI with retry logic.

    Args:
        repo_name: Repository name
        purpose: Repository description
        visibility: 'public' or 'private'
        category: Category for topics

    Raises:
        GitHubOperationError: If GitHub repository creation fails
    """
    try:
        logger.info(f"Creating GitHub repository: coditect-ai/{repo_name}")

        # Create repository
        visibility_flag = f"--{visibility}"
        run_command([
            'gh', 'repo', 'create', f'coditect-ai/{repo_name}',
            visibility_flag,
            '--description', purpose,
            '--homepage', 'https://coditect.ai'
        ])
        print_success(f"Created GitHub repository: coditect-ai/{repo_name}")
        logger.info("GitHub repository created successfully")

        # Add topics
        logger.debug("Adding topics...")
        run_command([
            'gh', 'repo', 'edit', f'coditect-ai/{repo_name}',
            '--add-topic', 'coditect',
            '--add-topic', category
        ])
        print_success(f"Added topics: coditect, {category}")
        logger.info(f"Topics added: coditect, {category}")

    except subprocess.CalledProcessError as e:
        error_msg = f"GitHub repository creation failed: {e.stderr if hasattr(e, 'stderr') else str(e)}"
        logger.error(error_msg)
        raise GitHubOperationError(error_msg)


@retry_operation(max_retries=3, delay=2.0)
def configure_remote_and_push(submodule_dir: Path, repo_name: str) -> None:
    """
    Configure git remote and push to GitHub with retry logic.

    Args:
        submodule_dir: Path to submodule directory
        repo_name: Repository name

    Raises:
        GitOperationError: If git remote configuration or push fails
    """
    try:
        logger.info("Configuring git remote...")

        # Add remote
        remote_url = f"https://github.com/coditect-ai/{repo_name}.git"
        run_command(['git', 'remote', 'add', 'origin', remote_url], cwd=submodule_dir)
        print_success(f"Added remote: {remote_url}")
        logger.info(f"Remote added: {remote_url}")

        # Push to GitHub
        logger.info("Pushing to GitHub...")
        run_command(['git', 'push', '-u', 'origin', 'main'], cwd=submodule_dir)
        print_success("Pushed to GitHub")
        logger.info("Successfully pushed to GitHub")

    except subprocess.CalledProcessError as e:
        error_msg = f"Git remote configuration or push failed: {e.stderr if hasattr(e, 'stderr') else str(e)}"
        logger.error(error_msg)
        raise GitOperationError(error_msg)


def rollback_submodule_setup(category: str, repo_name: str, created_items: List[str]) -> None:
    """
    Rollback submodule setup on failure.

    Args:
        category: Category directory name
        repo_name: Repository name
        created_items: List of items created (for tracking what to clean up)

    Raises:
        RollbackError: If rollback operation fails
    """
    logger.warning("Rolling back submodule setup...")
    print_warning("Rolling back submodule setup...")

    rollback_errors = []

    try:
        # Remove local submodule directory
        submodule_dir = Path('submodules') / category / repo_name
        if submodule_dir.exists() and 'submodule_dir' in created_items:
            logger.info(f"Removing directory: {submodule_dir}")
            import shutil
            shutil.rmtree(submodule_dir)
            print_success(f"Removed directory: {submodule_dir}")

        # Remove GitHub repository if created
        if 'github_repo' in created_items:
            try:
                logger.info(f"Deleting GitHub repository: coditect-ai/{repo_name}")
                run_command([
                    'gh', 'repo', 'delete', f'coditect-ai/{repo_name}',
                    '--yes'
                ], check=False)
                print_success(f"Deleted GitHub repository: coditect-ai/{repo_name}")
            except Exception as e:
                error_msg = f"Failed to delete GitHub repository: {e}"
                logger.error(error_msg)
                rollback_errors.append(error_msg)
                print_warning(error_msg)

        # Remove submodule registration from parent
        if 'parent_registration' in created_items:
            try:
                logger.info("Removing submodule registration from parent...")
                submodule_path = f"submodules/{category}/{repo_name}"
                run_command(['git', 'rm', '-f', submodule_path], check=False)
                print_success("Removed submodule registration from parent")
            except Exception as e:
                error_msg = f"Failed to remove submodule registration: {e}"
                logger.error(error_msg)
                rollback_errors.append(error_msg)
                print_warning(error_msg)

        if rollback_errors:
            raise RollbackError(f"Rollback completed with errors: {'; '.join(rollback_errors)}")
        else:
            print_success("Rollback completed successfully")
            logger.info("Rollback completed successfully")

    except Exception as e:
        error_msg = f"Critical rollback failure: {e}"
        logger.error(error_msg)
        raise RollbackError(error_msg)


def register_submodule_with_parent(category: str, repo_name: str) -> None:
    """
    Register submodule with parent rollout-master repository.

    Args:
        category: Category directory name
        repo_name: Repository name

    Raises:
        GitOperationError: If submodule registration fails
    """
    try:
        submodule_path = f"submodules/{category}/{repo_name}"
        submodule_url = f"https://github.com/coditect-ai/{repo_name}.git"

        # Add submodule to parent
        run_command([
            'git', 'submodule', 'add',
            submodule_url,
            submodule_path
        ])
        print_success(f"Registered submodule in parent repository")

    except subprocess.CalledProcessError as e:
        raise GitOperationError(f"Submodule registration failed: {e}")


def main() -> int:
    """
    Main entry point for submodule setup script.

    Returns:
        Exit code (0 for success, non-zero for error)

    Exit Codes:
        0: Success
        1: General error
        2: Usage error
        3: Prerequisites not met
        4: Git operation failed
        5: GitHub operation failed
        6: Rollback failed (after setup error)
        130: User cancelled (Ctrl+C)
    """
    global logger

    parser = argparse.ArgumentParser(
        description='Setup new CODITECT submodule with complete automation',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--category', '-c',
                        help='Submodule category (cloud, dev, gtm, labs, docs, ops, market, core)')
    parser.add_argument('--name', '-n',
                        help='Full repository name with prefix (e.g., coditect-ops-compliance, coditect-cloud-gateway)')
    parser.add_argument('--purpose', '-p', help='One-sentence purpose description')
    parser.add_argument('--visibility', '-v', choices=['public', 'private'], default='public',
                        help='GitHub repository visibility (default: public)')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Interactive mode - prompt for all inputs')
    parser.add_argument('--config', help='Path to YAML configuration file')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Initialize logging
    logger = setup_logging()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Track created items for rollback
    created_items = []
    category = None
    repo_name = None

    try:
        print_info("CODITECT Submodule Setup")
        print()

        # Check prerequisites
        print_info("Checking prerequisites...")
        check_prerequisites()
        print()

        # Get configuration (interactive, args, or config file)
        if args.interactive:
            # Interactive mode - prompt user
            print_info("Interactive mode - enter submodule details:")
            print()

            category = input("Category (cloud/dev/gtm/labs/docs/ops/market/core): ").strip()

            print_info(f"For category '{category}', the full repository name must start with: coditect-{category}-")
            print_info("Examples: coditect-ops-compliance, coditect-cloud-gateway, coditect-dev-logger")
            repo_name = input(f"Full repository name (coditect-{category}-<name>): ").strip()

            purpose = input("Purpose (one sentence): ").strip()
            visibility = input("Visibility (public/private) [public]: ").strip() or 'public'
            print()
        elif args.config:
            # Load from config file
            with open(args.config) as f:
                config = yaml.safe_load(f)
            # This script handles single submodule; batch script uses this for each
            category = config['category']
            repo_name = config['name']
            purpose = config['purpose']
            visibility = config.get('visibility', 'public')
        else:
            # Use command-line arguments
            if not all([args.category, args.name, args.purpose]):
                parser.error("--category, --name, and --purpose are required (or use --interactive)")
            category = args.category
            repo_name = args.name
            purpose = args.purpose
            visibility = args.visibility

        # Validate inputs
        print_info("Validating inputs...")
        if not validate_category(category):
            print_error(f"Invalid category: {category}")
            print_info("Valid categories: cloud, dev, gtm, labs, docs, ops, market, core")
            return 2

        if not validate_repo_name(repo_name, category):
            return 2

        print_success("Input validation passed")
        print()

        # Show configuration and confirm
        print_info(f"Configuration:")
        print(f"  Category: {category}")
        print(f"  Repository: {repo_name}")
        print(f"  Purpose: {purpose}")
        print(f"  Visibility: {visibility}")
        print()

        if args.interactive:
            confirm = input("Proceed with setup? (y/N): ").strip().lower()
            if confirm != 'y':
                print_warning("Setup cancelled")
                return 0

        # Execute setup steps with rollback tracking
        try:
            print_info("Step 1: Creating directory structure...")
            submodule_dir = create_directory_structure(category, repo_name)
            created_items.append('submodule_dir')
            logger.info(f"Created directory: {submodule_dir}")
            print()

            print_info("Step 2: Creating symlinks...")
            create_symlinks(submodule_dir)
            print()

            print_info("Step 3: Generating templates...")
            generate_templates(submodule_dir, repo_name, category, purpose)
            print()

            print_info("Step 4: Initializing git repository...")
            initialize_git_repository(submodule_dir, repo_name)
            print()

            print_info("Step 5: Creating GitHub repository...")
            create_github_repository(repo_name, purpose, visibility, category)
            created_items.append('github_repo')
            logger.info("GitHub repository created")
            print()

            print_info("Step 6: Configuring remote and pushing...")
            configure_remote_and_push(submodule_dir, repo_name)
            print()

            print_info("Step 7: Registering submodule with parent...")
            register_submodule_with_parent(category, repo_name)
            created_items.append('parent_registration')
            logger.info("Submodule registered with parent")
            print()

            print_success("✓ Submodule setup complete!")
            logger.info("Submodule setup completed successfully")
            print()
            print_info("Next steps:")
            print(f"  1. cd submodules/{category}/{repo_name}")
            print("  2. Customize PROJECT-PLAN.md")
            print("  3. Add tasks to TASKLIST.md")
            print("  4. Start development!")

            return 0

        except (GitOperationError, GitHubOperationError, SubmoduleSetupError) as e:
            # Attempt rollback on setup failure
            logger.error(f"Setup failed, attempting rollback: {e}")
            print_error(f"Setup failed: {e}")
            print()

            try:
                rollback_submodule_setup(category, repo_name, created_items)
                logger.info("Rollback completed successfully")
                print()
                print_info("Rollback completed. You can retry the setup.")
                return 1
            except RollbackError as rb_error:
                logger.error(f"Rollback failed: {rb_error}")
                print_error(f"Rollback failed: {rb_error}")
                print_warning("Manual cleanup may be required:")
                print(f"  - Remove directory: submodules/{category}/{repo_name}")
                print(f"  - Delete GitHub repo: gh repo delete coditect-ai/{repo_name}")
                return 6

    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        print()
        print_warning("Operation cancelled by user")

        # Attempt cleanup
        if created_items:
            print_warning("Attempting to clean up partial setup...")
            try:
                rollback_submodule_setup(category, repo_name, created_items)
            except:
                pass

        return 130

    except PrerequisiteError as e:
        logger.error(f"Prerequisites not met: {e}")
        print_error(f"Prerequisites not met: {e}")
        return 3

    except Exception as e:
        logger.exception("Unexpected error occurred")
        print_error(f"Unexpected error: {e}")

        # Attempt cleanup on unexpected errors
        if created_items and category and repo_name:
            print_warning("Attempting rollback due to unexpected error...")
            try:
                rollback_submodule_setup(category, repo_name, created_items)
            except:
                logger.error("Rollback failed after unexpected error")

        return 1

    finally:
        # Resource cleanup
        logger.info("Script execution completed")
        # Close logging handlers
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)


if __name__ == "__main__":
    sys.exit(main())
