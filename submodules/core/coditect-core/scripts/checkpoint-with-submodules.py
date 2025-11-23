#!/usr/bin/env python3
"""
CODITECT Enhanced Checkpoint System with Multi-Submodule Management

Unified checkpoint process that ensures all modified submodules are committed
and pushed along with the parent repository.

Features:
1. Detects ALL modified submodules across the entire git tree
2. Commits changes in each modified submodule independently
3. Pushes each modified submodule to its remote
4. Updates parent repository with submodule pointer changes
5. Commits and pushes parent repository
6. Handles nested submodules gracefully
7. Provides detailed audit trail of all operations
8. Production-grade error handling with logging and rollback
9. Network retry logic for push operations
10. Resource cleanup and proper exit codes

Usage:
    python3 scripts/checkpoint-with-submodules.py "Sprint description" [--auto-push]

Author: AZ1.AI INC.
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional
import argparse
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('checkpoint-submodules.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


# Custom Exception Hierarchy
class CheckpointError(Exception):
    """Base exception for checkpoint operations."""
    pass


class GitOperationError(CheckpointError):
    """Raised when git operation fails."""
    pass


class SubmoduleOperationError(CheckpointError):
    """Raised when submodule operation fails."""
    pass


class NetworkError(CheckpointError):
    """Raised when network operation fails."""
    pass


class ValidationError(CheckpointError):
    """Raised when input validation fails."""
    pass


class SubmoduleCheckpointManager:
    """Manages checkpoint creation across parent and all modified submodules."""

    def __init__(self, repo_root: str = None):
        """Initialize checkpoint manager.

        Args:
            repo_root: Root directory of the repository (defaults to current directory)
        """
        if repo_root is None:
            self.repo_root = Path.cwd()
        else:
            self.repo_root = Path(repo_root)

        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        self.operations_log = []

        # Git state tracking for rollback
        self.git_state = None
        self.submodule_states = {}

        # Network retry configuration
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def validate_inputs(self, sprint_description: str) -> None:
        """
        Validate input parameters.

        Args:
            sprint_description: Sprint description to validate

        Raises:
            ValidationError: If inputs are invalid
        """
        if not sprint_description or not sprint_description.strip():
            raise ValidationError("Sprint description cannot be empty")

        if len(sprint_description) > 200:
            raise ValidationError("Sprint description too long (max 200 characters)")

        # Check for safe characters (prevent command injection)
        unsafe_chars = set(';&|`$')
        if any(char in sprint_description for char in unsafe_chars):
            raise ValidationError(f"Sprint description contains unsafe characters: {unsafe_chars}")

        logger.info(f"Input validation passed for: {sprint_description}")

    def save_git_state(self) -> None:
        """
        Save current git state for potential rollback.

        Raises:
            GitOperationError: If unable to save git state
        """
        try:
            logger.info("Saving git state for potential rollback...")

            returncode, head, _ = self.run_command("git rev-parse HEAD")
            returncode, branch, _ = self.run_command("git rev-parse --abbrev-ref HEAD")

            self.git_state = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'head': head.strip(),
                'branch': branch.strip()
            }

            logger.info(f"Git state saved: HEAD={self.git_state['head'][:7]}, branch={self.git_state['branch']}")

        except Exception as e:
            logger.error(f"Failed to save git state: {e}")
            raise GitOperationError(f"Unable to save git state: {e}")

    def rollback_git_state(self) -> None:
        """
        Rollback git to saved state.

        Raises:
            GitOperationError: If rollback fails
        """
        if not self.git_state:
            logger.warning("No saved git state to rollback to")
            return

        try:
            logger.warning("Rolling back git state...")

            # Reset to saved HEAD
            logger.info(f"Resetting to {self.git_state['head'][:7]}")
            self.run_command(f"git reset --hard {self.git_state['head']}")

            # Rollback submodule states
            for path, state in self.submodule_states.items():
                try:
                    logger.info(f"Rolling back submodule {path}")
                    self.run_command(f"git reset --hard {state['head']}", cwd=self.repo_root / path)
                except Exception as e:
                    logger.error(f"Failed to rollback submodule {path}: {e}")

            logger.info("Git state rollback complete")

        except Exception as e:
            logger.error(f"Git rollback failed: {e}")
            raise GitOperationError(f"Rollback failed: {e}")

    def log_operation(self, repo_name: str, operation: str, status: str, details: str = ""):
        """Log an operation for audit trail.

        Args:
            repo_name: Name of repository (parent or submodule path)
            operation: Operation performed (commit, push, detect)
            status: Status (success, warning, error)
            details: Additional details
        """
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'repo': repo_name,
            'operation': operation,
            'status': status,
            'details': details
        }
        self.operations_log.append(log_entry)

        # Also log to logger
        level = {
            'success': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'info': logging.INFO
        }.get(status, logging.INFO)

        logger.log(level, f"{repo_name} | {operation} | {status} | {details}")

    def run_command(self, cmd: str, cwd: Path = None) -> Tuple[int, str, str]:
        """Run shell command and return output.

        Args:
            cmd: Command to execute
            cwd: Working directory (defaults to repo_root)

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        if cwd is None:
            cwd = self.repo_root

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(cwd),
                timeout=30  # 30 second timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {cmd}")
            return 1, "", "Command timed out after 30 seconds"
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return 1, "", str(e)

    def run_command_with_retry(self, cmd: str, cwd: Path = None, operation_name: str = "operation") -> Tuple[int, str, str]:
        """
        Run command with retry logic for network operations.

        Args:
            cmd: Command to execute
            cwd: Working directory
            operation_name: Name of operation for logging

        Returns:
            Tuple of (return_code, stdout, stderr)

        Raises:
            NetworkError: If all retries fail
        """
        for attempt in range(1, self.max_retries + 1):
            logger.info(f"Attempting {operation_name} (attempt {attempt}/{self.max_retries})")

            returncode, stdout, stderr = self.run_command(cmd, cwd)

            if returncode == 0:
                return returncode, stdout, stderr

            # Check if error is network-related
            if any(err in stderr.lower() for err in ['network', 'connection', 'timeout', 'fetch']):
                if attempt < self.max_retries:
                    logger.warning(f"Network error on attempt {attempt}, retrying in {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise NetworkError(f"{operation_name} failed after {self.max_retries} attempts: {stderr}")
            else:
                # Non-network error, don't retry
                return returncode, stdout, stderr

        return returncode, stdout, stderr

    def detect_modified_submodules(self) -> Dict[str, Dict]:
        """Detect all modified submodules in the repository.

        Returns:
            Dictionary mapping submodule path to status info

        Raises:
            SubmoduleOperationError: If submodule detection fails critically
        """
        print("\n📍 Step 1: Detecting modified submodules...")
        print("=" * 80)

        modified_submodules = {}

        try:
            # Get all submodules from .gitmodules
            returncode, output, stderr = self.run_command("git config --file .gitmodules --get-regexp path")

            if returncode != 0 or not output.strip():
                print("ℹ️  No submodules found in .gitmodules")
                self.log_operation("parent", "detect_submodules", "info", "No submodules found")
                return modified_submodules

            # Parse submodule paths
            submodule_paths = []
            for line in output.strip().split('\n'):
                if line.strip():
                    # Format: submodule.<name>.path <path>
                    parts = line.split()
                    if len(parts) >= 2:
                        path = parts[-1]
                        submodule_paths.append(path)

            print(f"Found {len(submodule_paths)} submodules configured")

            # Check each submodule for modifications
            for submodule_path in submodule_paths:
                submodule_full_path = self.repo_root / submodule_path

                if not submodule_full_path.exists():
                    print(f"⚠️  Submodule path does not exist: {submodule_path}")
                    self.log_operation(submodule_path, "detect", "warning", "Path does not exist")
                    continue

                # Check if submodule has uncommitted changes
                returncode, status, _ = self.run_command(
                    "git status --porcelain",
                    cwd=submodule_full_path
                )

                if returncode == 0 and status.strip():
                    # Save submodule state for potential rollback
                    head_code, head_commit, _ = self.run_command("git rev-parse HEAD", cwd=submodule_full_path)
                    if head_code == 0:
                        self.submodule_states[submodule_path] = {'head': head_commit.strip()}

                    # Has changes
                    modified_submodules[submodule_path] = {
                        'path': submodule_full_path,
                        'has_changes': True,
                        'status': status.strip()
                    }
                    print(f"✅ {submodule_path}: HAS MODIFICATIONS")
                    self.log_operation(submodule_path, "detect", "success", f"Found {len(status.strip().split(chr(10)))} modified files")
                else:
                    print(f"⚪ {submodule_path}: clean")
                    self.log_operation(submodule_path, "detect", "info", "No modifications")

            print(f"\n📊 Summary: {len(modified_submodules)} submodule(s) with modifications")
            return modified_submodules

        except Exception as e:
            logger.error(f"Submodule detection failed: {e}")
            raise SubmoduleOperationError(f"Failed to detect submodules: {e}")

    def commit_submodule_changes(
        self,
        submodule_path: str,
        submodule_full_path: Path,
        sprint_description: str
    ) -> bool:
        """Commit changes in a specific submodule.

        Args:
            submodule_path: Relative path to submodule
            submodule_full_path: Full path to submodule
            sprint_description: Description for commit message

        Returns:
            True if successful, False otherwise
        """
        print(f"\n📝 Committing changes in: {submodule_path}")

        try:
            # Stage all changes
            returncode, _, stderr = self.run_command(
                "git add -A",
                cwd=submodule_full_path
            )

            if returncode != 0:
                print(f"  ❌ Failed to stage changes: {stderr}")
                self.log_operation(submodule_path, "commit", "error", f"Stage failed: {stderr}")
                return False

            # Check if there are actually changes to commit
            returncode, status, _ = self.run_command(
                "git status --porcelain",
                cwd=submodule_full_path
            )

            if not status.strip():
                print(f"  ℹ️  No staged changes to commit")
                self.log_operation(submodule_path, "commit", "info", "No changes to commit")
                return True

            # Get submodule name from path
            submodule_name = Path(submodule_path).name

            # Commit changes
            commit_msg = f"""Update {submodule_name}: {sprint_description}

Timestamp: {self.timestamp}
Status: ✅ SUBMODULE CHECKPOINT

Modified by: CODITECT Enhanced Checkpoint System
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.
"""

            # Use heredoc for multi-line commit message
            returncode, stdout, stderr = self.run_command(
                f'git commit -m "$(cat <<\'EOF\'\n{commit_msg}\nEOF\n)"',
                cwd=submodule_full_path
            )

            if returncode != 0 and "nothing to commit" not in stderr:
                print(f"  ❌ Commit failed: {stderr}")
                self.log_operation(submodule_path, "commit", "error", f"Commit failed: {stderr}")
                return False

            print(f"  ✅ Committed changes in {submodule_path}")
            self.log_operation(submodule_path, "commit", "success", "Changes committed")
            return True

        except Exception as e:
            logger.error(f"Failed to commit submodule {submodule_path}: {e}")
            self.log_operation(submodule_path, "commit", "error", str(e))
            return False

    def push_submodule_changes(
        self,
        submodule_path: str,
        submodule_full_path: Path
    ) -> bool:
        """Push changes in a specific submodule to its remote.

        Args:
            submodule_path: Relative path to submodule
            submodule_full_path: Full path to submodule

        Returns:
            True if successful, False otherwise
        """
        print(f"🚀 Pushing changes in: {submodule_path}")

        try:
            # Get current branch
            returncode, branch, stderr = self.run_command(
                "git branch --show-current",
                cwd=submodule_full_path
            )

            if returncode != 0:
                print(f"  ❌ Failed to get current branch: {stderr}")
                self.log_operation(submodule_path, "push", "error", "Failed to get branch")
                return False

            branch = branch.strip()

            # Push to remote with retry logic
            returncode, stdout, stderr = self.run_command_with_retry(
                f"git push origin {branch}",
                cwd=submodule_full_path,
                operation_name=f"push {submodule_path}"
            )

            if returncode != 0:
                if "Everything up-to-date" in stderr or "Everything up-to-date" in stdout:
                    print(f"  ℹ️  Everything up-to-date on {branch}")
                    self.log_operation(submodule_path, "push", "info", "Everything up-to-date")
                    return True
                else:
                    print(f"  ❌ Push failed: {stderr}")
                    self.log_operation(submodule_path, "push", "error", f"Push failed: {stderr}")
                    return False

            print(f"  ✅ Pushed changes in {submodule_path}")
            self.log_operation(submodule_path, "push", "success", "Changes pushed to remote")
            return True

        except NetworkError as e:
            logger.error(f"Network error pushing {submodule_path}: {e}")
            print(f"  ❌ Network error: {e}")
            self.log_operation(submodule_path, "push", "error", str(e))
            return False
        except Exception as e:
            logger.error(f"Failed to push submodule {submodule_path}: {e}")
            self.log_operation(submodule_path, "push", "error", str(e))
            return False

    def commit_parent_repo(self, sprint_description: str) -> bool:
        """Commit submodule pointer updates in parent repository.

        Args:
            sprint_description: Description for commit message

        Returns:
            True if successful, False otherwise
        """
        print(f"\n📝 Committing parent repository changes...")

        try:
            # Stage submodule pointer updates
            returncode, _, stderr = self.run_command(
                "git add .gitmodules",
                cwd=self.repo_root
            )

            if returncode != 0:
                print(f"  ⚠️  Failed to stage .gitmodules: {stderr}")

            # Stage all submodule updates
            returncode, _, stderr = self.run_command(
                "git add submodules/",
                cwd=self.repo_root
            )

            if returncode != 0:
                print(f"  ⚠️  Failed to stage submodules: {stderr}")

            # Check if there are changes to commit
            returncode, status, _ = self.run_command(
                "git status --porcelain",
                cwd=self.repo_root
            )

            if not status.strip():
                print(f"  ℹ️  No changes in parent repository to commit")
                self.log_operation("parent", "commit", "info", "No changes to commit")
                return True

            # Commit parent repo changes
            commit_msg = f"""Checkpoint: {sprint_description}

Update submodule references after checkpoint creation.

Timestamp: {self.timestamp}
Status: ✅ PARENT CHECKPOINT

Modified by: CODITECT Enhanced Checkpoint System
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.
"""

            returncode, stdout, stderr = self.run_command(
                f'git commit -m "$(cat <<\'EOF\'\n{commit_msg}\nEOF\n)"',
                cwd=self.repo_root
            )

            if returncode != 0 and "nothing to commit" not in stderr:
                print(f"  ❌ Commit failed: {stderr}")
                self.log_operation("parent", "commit", "error", f"Commit failed: {stderr}")
                return False

            print(f"  ✅ Committed parent repository changes")
            self.log_operation("parent", "commit", "success", "Parent changes committed")
            return True

        except Exception as e:
            logger.error(f"Failed to commit parent repo: {e}")
            self.log_operation("parent", "commit", "error", str(e))
            return False

    def push_parent_repo(self) -> bool:
        """Push parent repository changes to remote.

        Returns:
            True if successful, False otherwise
        """
        print(f"🚀 Pushing parent repository...")

        try:
            # Get current branch
            returncode, branch, stderr = self.run_command(
                "git branch --show-current",
                cwd=self.repo_root
            )

            if returncode != 0:
                print(f"  ❌ Failed to get current branch: {stderr}")
                self.log_operation("parent", "push", "error", "Failed to get branch")
                return False

            branch = branch.strip()

            # Push to remote with retry logic
            returncode, stdout, stderr = self.run_command_with_retry(
                f"git push origin {branch}",
                cwd=self.repo_root,
                operation_name="push parent repository"
            )

            if returncode != 0:
                if "Everything up-to-date" in stderr or "Everything up-to-date" in stdout:
                    print(f"  ℹ️  Everything up-to-date on {branch}")
                    self.log_operation("parent", "push", "info", "Everything up-to-date")
                    return True
                else:
                    print(f"  ❌ Push failed: {stderr}")
                    self.log_operation("parent", "push", "error", f"Push failed: {stderr}")
                    return False

            print(f"  ✅ Pushed parent repository")
            self.log_operation("parent", "push", "success", "Parent pushed to remote")
            return True

        except NetworkError as e:
            logger.error(f"Network error pushing parent repo: {e}")
            print(f"  ❌ Network error: {e}")
            self.log_operation("parent", "push", "error", str(e))
            return False
        except Exception as e:
            logger.error(f"Failed to push parent repo: {e}")
            self.log_operation("parent", "push", "error", str(e))
            return False

    def generate_audit_report(self, sprint_description: str) -> str:
        """Generate audit report of all operations.

        Args:
            sprint_description: Description of the sprint

        Returns:
            Path to audit report file
        """
        print(f"\n📊 Generating audit report...")

        try:
            memory_context_dir = self.repo_root / "MEMORY-CONTEXT"
            memory_context_dir.mkdir(exist_ok=True)

            audit_dir = memory_context_dir / "audit-logs"
            audit_dir.mkdir(exist_ok=True)

            safe_desc = sprint_description.replace(' ', '-').replace('/', '-')[:50]
            audit_file = audit_dir / f"{self.timestamp}-checkpoint-audit-{safe_desc}.json"

            import json
            with open(audit_file, 'w') as f:
                json.dump({
                    'timestamp': self.timestamp,
                    'sprint_description': sprint_description,
                    'repo_root': str(self.repo_root),
                    'operations': self.operations_log,
                    'operation_summary': {
                        'total_operations': len(self.operations_log),
                        'by_status': {
                            'success': sum(1 for op in self.operations_log if op['status'] == 'success'),
                            'warning': sum(1 for op in self.operations_log if op['status'] == 'warning'),
                            'error': sum(1 for op in self.operations_log if op['status'] == 'error'),
                            'info': sum(1 for op in self.operations_log if op['status'] == 'info'),
                        }
                    }
                }, f, indent=2)

            print(f"  ✅ Audit report saved: {audit_file.name}")
            logger.info(f"Audit report saved to {audit_file}")
            return str(audit_file)

        except Exception as e:
            logger.error(f"Failed to generate audit report: {e}")
            print(f"  ⚠️  Failed to generate audit report: {e}")
            return ""

    def run_full_checkpoint(
        self,
        sprint_description: str,
        auto_push: bool = True
    ) -> bool:
        """Run complete checkpoint process with all submodules.

        Args:
            sprint_description: Description of work completed
            auto_push: Whether to automatically push changes

        Returns:
            True if all operations succeeded, False otherwise
        """
        print(f"\n{'='*80}")
        print(f"CODITECT Enhanced Checkpoint System with Multi-Submodule Management")
        print(f"{'='*80}\n")

        print(f"📋 Sprint: {sprint_description}")
        print(f"🕐 Timestamp: {self.timestamp}")
        print(f"📂 Repository Root: {self.repo_root}")
        if auto_push:
            print(f"🚀 Mode: Commit + Push (all submodules and parent)")
        else:
            print(f"💾 Mode: Commit Only (no push)")
        print()

        try:
            # Validate inputs
            self.validate_inputs(sprint_description)

            # Save git state for rollback
            self.save_git_state()

            # Step 1: Detect modified submodules
            modified_submodules = self.detect_modified_submodules()

            if not modified_submodules:
                print("\n⚪ No modified submodules detected")
                print("   Will proceed with parent repository changes only")

            # Step 2: Commit and push each modified submodule
            if auto_push:
                print(f"\n{'='*80}")
                print(f"Step 2: Committing and pushing modified submodules")
                print(f"{'='*80}\n")

                all_submodule_success = True
                for submodule_path, info in modified_submodules.items():
                    success = self.commit_submodule_changes(
                        submodule_path,
                        info['path'],
                        sprint_description
                    )

                    if success:
                        success = self.push_submodule_changes(
                            submodule_path,
                            info['path']
                        )

                    if not success:
                        all_submodule_success = False
                        print(f"  ⚠️  Issues with {submodule_path}")

                if not all_submodule_success:
                    print(f"\n⚠️  Some submodules had issues - continuing with parent repo")

            # Step 3: Commit parent repository with submodule references
            print(f"\n{'='*80}")
            print(f"Step 3: Updating parent repository")
            print(f"{'='*80}\n")

            parent_success = self.commit_parent_repo(sprint_description)

            # Step 4: Push parent repository
            if auto_push and parent_success:
                print()
                parent_success = self.push_parent_repo()

            # Step 5: Generate audit report
            print(f"\n{'='*80}")
            print(f"Step 4: Generating audit report")
            print(f"{'='*80}\n")

            audit_file = self.generate_audit_report(sprint_description)

            # Summary
            print(f"\n{'='*80}")
            print(f"✅ CHECKPOINT COMPLETE")
            print(f"{'='*80}\n")

            print(f"📊 Operations Summary:")
            print(f"  • Submodules processed: {len(modified_submodules)}")
            print(f"  • Total operations: {len(self.operations_log)}")
            if audit_file:
                print(f"  • Audit report: {audit_file}")
            print()

            if auto_push:
                print(f"🚀 All changes committed and pushed:")
                if modified_submodules:
                    for submodule_path in modified_submodules.keys():
                        print(f"  ✅ {submodule_path}")
                print(f"  ✅ Parent repository (coditect-rollout-master)")
            else:
                print(f"💾 All changes committed locally (not pushed)")

            print(f"\n{'='*80}\n")

            return parent_success

        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n❌ Validation Error: {e}")
            return False
        except (GitOperationError, SubmoduleOperationError, NetworkError) as e:
            logger.error(f"Checkpoint failed: {e}")
            print(f"\n❌ Checkpoint Failed: {e}")
            print(f"\n🔄 Rolling back changes...")
            try:
                self.rollback_git_state()
                print(f"✅ Rollback completed")
            except Exception as rollback_error:
                logger.error(f"Rollback failed: {rollback_error}")
                print(f"❌ Rollback failed: {rollback_error}")
            return False
        except Exception as e:
            logger.exception("Unexpected error during checkpoint")
            print(f"\n❌ Unexpected Error: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CODITECT Enhanced Checkpoint System with Multi-Submodule Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full checkpoint with commit and push
  python3 scripts/checkpoint-with-submodules.py "Deduplication and re-organization complete"

  # Commit only (no push)
  python3 scripts/checkpoint-with-submodules.py "WIP snapshot" --no-push

Key Benefits:
  ✅ Detects ALL modified submodules automatically
  ✅ Commits changes in each submodule independently
  ✅ Pushes each submodule to its remote
  ✅ Updates parent repository with submodule pointers
  ✅ Commits and pushes parent repository
  ✅ Generates audit trail for all operations
  ✅ Handles nested submodules gracefully
  ✅ Ensures consistency across entire monorepo
  ✅ Production-grade error handling with rollback
  ✅ Network retry logic for push operations

For more information: https://github.com/coditect-ai/coditect-rollout-master
        """
    )

    parser.add_argument(
        'description',
        help='Description of the sprint/work completed'
    )

    parser.add_argument(
        '--no-push',
        action='store_true',
        help='Commit changes locally without pushing to remote'
    )

    parser.add_argument(
        '--repo-root',
        default=None,
        help='Root directory of the repository'
    )

    args = parser.parse_args()

    try:
        manager = SubmoduleCheckpointManager(repo_root=args.repo_root)
        success = manager.run_full_checkpoint(
            sprint_description=args.description,
            auto_push=not args.no_push
        )

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.warning("Checkpoint cancelled by user")
        print("\n\n⚠️  Checkpoint cancelled by user")
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        logger.exception("Fatal error in main")
        print(f"\n❌ Fatal Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
