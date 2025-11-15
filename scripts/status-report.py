#!/usr/bin/env python3
"""
Generate status report across all CODITECT sub-projects.
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

def get_submodule_status(submodule_path):
    """Get git status for a submodule."""
    try:
        os.chdir(submodule_path)

        # Get current branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()

        # Get latest commit
        commit = subprocess.check_output(
            ["git", "log", "-1", "--format=%h - %s"],
            text=True
        ).strip()

        # Get uncommitted changes
        status = subprocess.check_output(
            ["git", "status", "--short"],
            text=True
        ).strip()

        uncommitted = len(status.split("\n")) if status else 0

        return {
            "branch": branch,
            "commit": commit,
            "uncommitted": uncommitted,
            "status": "✓" if uncommitted == 0 else "⚠"
        }
    except Exception as e:
        return {
            "branch": "ERROR",
            "commit": str(e),
            "uncommitted": 0,
            "status": "✗"
        }

def main():
    master_root = Path(__file__).parent.parent
    submodules_dir = master_root / "submodules"

    print(f"\n{'='*80}")
    print(f"  CODITECT Platform - Status Report")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    if not submodules_dir.exists():
        print("❌ No submodules directory found")
        return

    submodules = [d for d in submodules_dir.iterdir() if d.is_dir() and (d / ".git").exists()]

    print(f"Total Sub-Projects: {len(submodules)}\n")
    print(f"{'Project':<35} {'Branch':<15} {'Status':<8} {'Uncommitted'}")
    print(f"{'-'*80}")

    for submodule in sorted(submodules):
        status = get_submodule_status(submodule)
        uncommitted_str = f"{status['uncommitted']} files" if status['uncommitted'] > 0 else "Clean"
        print(f"{submodule.name:<35} {status['branch']:<15} {status['status']:<8} {uncommitted_str}")

    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
