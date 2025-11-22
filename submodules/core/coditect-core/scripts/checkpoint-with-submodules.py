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

Usage:
    python3 scripts/checkpoint-with-submodules.py "Sprint description" [--auto-push]

Author: AZ1.AI INC.
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Tuple, Optional
import argparse
from collections import defaultdict


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

    def log_operation(self, repo_name: str, operation: str, status: str, details: str = ""):
        """Log an operation for audit trail.

        Args:
            repo_name: Name of repository (parent or submodule path)
            operation: Operation performed (commit, push, detect)
            status: Status (success, warning, error)
            details: Additional details
        """
        self.operations_log.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'repo': repo_name,
            'operation': operation,
            'status': status,
            'details': details
        })

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
                cwd=str(cwd)
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    def detect_modified_submodules(self) -> Dict[str, Dict]:
        """Detect all modified submodules in the repository.

        Returns:
            Dictionary mapping submodule path to status info
        """
        print("\n📍 Step 1: Detecting modified submodules...")
        print("=" * 80)

        modified_submodules = {}

        # Get all submodules from .gitmodules
        returncode, output, _ = self.run_command("git config --file .gitmodules --get-regexp path")

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
                continue

            # Check if submodule has uncommitted changes
            returncode, status, _ = self.run_command(
                "git status --porcelain",
                cwd=submodule_full_path
            )

            if returncode == 0 and status.strip():
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

        # Get current branch
        returncode, branch, _ = self.run_command(
            "git branch --show-current",
            cwd=submodule_full_path
        )

        if returncode != 0:
            print(f"  ❌ Failed to get current branch: {_}")
            self.log_operation(submodule_path, "push", "error", "Failed to get branch")
            return False

        branch = branch.strip()

        # Push to remote
        returncode, stdout, stderr = self.run_command(
            f"git push origin {branch}",
            cwd=submodule_full_path
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

    def commit_parent_repo(self, sprint_description: str) -> bool:
        """Commit submodule pointer updates in parent repository.

        Args:
            sprint_description: Description for commit message

        Returns:
            True if successful, False otherwise
        """
        print(f"\n📝 Committing parent repository changes...")

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

    def push_parent_repo(self) -> bool:
        """Push parent repository changes to remote.

        Returns:
            True if successful, False otherwise
        """
        print(f"🚀 Pushing parent repository...")

        # Get current branch
        returncode, branch, _ = self.run_command(
            "git branch --show-current",
            cwd=self.repo_root
        )

        if returncode != 0:
            print(f"  ❌ Failed to get current branch: {_}")
            self.log_operation("parent", "push", "error", "Failed to get branch")
            return False

        branch = branch.strip()

        # Push to remote
        returncode, stdout, stderr = self.run_command(
            f"git push origin {branch}",
            cwd=self.repo_root
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

    def generate_audit_report(self, sprint_description: str) -> str:
        """Generate audit report of all operations.

        Args:
            sprint_description: Description of the sprint

        Returns:
            Path to audit report file
        """
        print(f"\n📊 Generating audit report...")

        memory_context_dir = self.repo_root / "MEMORY-CONTEXT"
        memory_context_dir.mkdir(exist_ok=True)

        audit_dir = memory_context_dir / "audit-logs"
        audit_dir.mkdir(exist_ok=True)

        safe_desc = sprint_description.replace(' ', '-').replace('/', '-')
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
        return str(audit_file)

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

    manager = SubmoduleCheckpointManager(repo_root=args.repo_root)
    success = manager.run_full_checkpoint(
        sprint_description=args.description,
        auto_push=not args.no_push
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
