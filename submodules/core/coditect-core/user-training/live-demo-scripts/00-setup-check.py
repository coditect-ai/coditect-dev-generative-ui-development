#!/usr/bin/env python3
"""
CODITECT Setup Check Script

Verifies environment is ready for live demo scripts.
Checks Claude Code, git, Python, and directory structure.

Author: Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.

Usage:
    python3 00-setup-check.py
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(msg):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_success(msg):
    print(f"{Colors.OKGREEN}✅ {msg}{Colors.ENDC}")


def print_error(msg):
    print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")


def print_warning(msg):
    print(f"{Colors.WARNING}⚠️  {msg}{Colors.ENDC}")


def print_info(msg):
    print(f"{Colors.OKCYAN}ℹ️  {msg}{Colors.ENDC}")


def check_python():
    """Check Python version."""
    print_info("Checking Python version...")

    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} installed")
        return True
    else:
        print_error(f"Python 3.7+ required (found {version.major}.{version.minor})")
        print_info("Install from: https://python.org")
        return False


def check_claude_code():
    """Check if Claude Code is installed."""
    print_info("Checking for Claude Code...")

    result = subprocess.run(
        ["which", "claude"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        # Get version
        version_result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True
        )
        print_success(f"Claude Code installed: {version_result.stdout.strip()}")
        return True
    else:
        print_error("Claude Code not found")
        print_info("Install from: https://claude.com/code")
        print_info("After installation, run this script again")
        return False


def check_git():
    """Check if git is installed and configured."""
    print_info("Checking git installation...")

    # Check if git exists
    if not shutil.which("git"):
        print_error("Git not installed")
        print_info("Install from: https://git-scm.com")
        return False

    print_success("Git installed")

    # Check git configuration
    result = subprocess.run(
        ["git", "config", "user.name"],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        print_warning("Git user not configured")
        print_info("Run: git config --global user.name \"Your Name\"")
        print_info("Run: git config --global user.email \"your@email.com\"")
        return False

    print_success("Git configured")
    return True


def check_directory_structure():
    """Verify we're in the right directory."""
    print_info("Checking directory structure...")

    current_dir = Path.cwd()

    # Should be in live-demo-scripts directory
    if current_dir.name != "live-demo-scripts":
        print_warning("Not in live-demo-scripts directory")
        print_info(f"Current: {current_dir}")
        print_info("Navigate to: .coditect/user-training/live-demo-scripts/")
        return False

    # Check parent directories exist
    if not (current_dir.parent.name == "user-training"):
        print_error("Unexpected directory structure")
        return False

    print_success("In correct directory")

    # Check for sample-project-templates
    templates_dir = current_dir.parent / "sample-project-templates"
    if not templates_dir.exists():
        print_info("Creating sample-project-templates directory...")
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "business").mkdir(exist_ok=True)
        (templates_dir / "technical").mkdir(exist_ok=True)
        (templates_dir / "project-management").mkdir(exist_ok=True)
        print_success("Created sample-project-templates structure")

    return True


def create_workspace():
    """Create workspace for demo outputs."""
    print_info("Setting up workspace...")

    workspace = Path.cwd().parent / "sample-project-templates"

    subdirs = [
        "business",
        "technical",
        "project-management"
    ]

    for subdir in subdirs:
        path = workspace / subdir
        path.mkdir(parents=True, exist_ok=True)

    print_success("Workspace ready")
    return True


def print_next_steps():
    """Print next steps for user."""
    print_header("Setup Check Complete!")

    print(f"{Colors.OKGREEN}{Colors.BOLD}✅ Your environment is ready!{Colors.ENDC}\n")

    print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}\n")

    print(f"{Colors.OKCYAN}Run the master orchestrator:{Colors.ENDC}")
    print(f"   python3 01-master-orchestrator.py\n")

    print(f"{Colors.OKCYAN}Or run individual phases:{Colors.ENDC}")
    print(f"   python3 02-phase1-business-discovery.py")
    print(f"   python3 03-phase2-technical-spec.py")
    print(f"   python3 04-phase3-project-management.py\n")

    print(f"{Colors.BOLD}What will happen:{Colors.ENDC}")
    print(f"   • Scripts will invoke real CODITECT agents")
    print(f"   • Generate production-quality templates")
    print(f"   • Show step-by-step explanations")
    print(f"   • Create complete PixelFlow sample project\n")

    print(f"{Colors.BOLD}Expected time:{Colors.ENDC}")
    print(f"   • Full demo: 30-45 minutes")
    print(f"   • Single phase: 5-20 minutes\n")

    print(f"{Colors.OKGREEN}Happy learning! 🚀{Colors.ENDC}\n")


def main():
    """Main setup check workflow."""
    print_header("CODITECT Setup Check")

    print(f"{Colors.BOLD}Verifying your environment for live demo scripts...{Colors.ENDC}\n")

    all_checks_passed = True

    # Run all checks
    if not check_python():
        all_checks_passed = False

    if not check_claude_code():
        all_checks_passed = False

    if not check_git():
        all_checks_passed = False

    if not check_directory_structure():
        all_checks_passed = False

    if all_checks_passed:
        create_workspace()
        print_next_steps()
        return 0
    else:
        print_header("Setup Issues Found")
        print_error("Please fix the issues above and run this script again\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
