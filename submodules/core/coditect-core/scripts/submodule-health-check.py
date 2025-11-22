#!/usr/bin/env python3
"""
Submodule Health Check - Status Monitoring and Reporting

Comprehensive health monitoring for CODITECT submodules including git status,
symlink integrity, update tracking, and ecosystem-wide dashboard generation.

Usage:
    python3 submodule-health-check.py --all
    python3 submodule-health-check.py --category cloud
    python3 submodule-health-check.py --path submodules/cloud/coditect-cloud-backend

Examples:
    python3 submodule-health-check.py --all
    python3 submodule-health-check.py --category dev
    python3 submodule-health-check.py --path submodules/cloud/backend --verbose

Requirements:
    - Python 3.9+
    - Git configured
    - Access to all submodules

Exit Codes:
    0: Success - Health check completed
    1: Error - Health check failed
    2: Usage error - Invalid arguments
"""

import sys
import os
import argparse
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class HealthStatus:
    """Health status for a submodule."""
    name: str
    path: str
    category: str
    score: int
    git_status: Dict[str, any]
    symlink_status: Dict[str, bool]
    issues: List[str]
    warnings: List[str]


def run_git_command(cmd: List[str], cwd: Path) -> str:
    """Run git command and return stdout."""
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def check_git_status(submodule_path: Path) -> Dict[str, any]:
    """Check git status for submodule."""
    status = {
        'uncommitted': 0,
        'unpushed': 0,
        'branch': '',
        'behind': 0,
        'ahead': 0,
        'detached': False,
        'last_commit': ''
    }

    try:
        # Check uncommitted changes
        porcelain = run_git_command(['git', 'status', '--porcelain'], submodule_path)
        status['uncommitted'] = len([l for l in porcelain.split('\n') if l])

        # Check branch
        branch = run_git_command(['git', 'branch', '--show-current'], submodule_path)
        status['branch'] = branch or 'detached'
        status['detached'] = not bool(branch)

        # Check unpushed commits
        if not status['detached']:
            unpushed = run_git_command(['git', 'log', '@{u}..', '--oneline'], submodule_path)
            status['unpushed'] = len([l for l in unpushed.split('\n') if l])

            # Check behind/ahead
            run_git_command(['git', 'fetch', 'origin', '--quiet'], submodule_path)
            behind = run_git_command(['git', 'log', '..@{u}', '--oneline'], submodule_path)
            status['behind'] = len([l for l in behind.split('\n') if l])
            status['ahead'] = status['unpushed']

        # Last commit
        last_commit = run_git_command(['git', 'log', '-1', '--format=%cr'], submodule_path)
        status['last_commit'] = last_commit

    except Exception as e:
        logger.debug(f"Git status check error: {e}")

    return status


def check_symlinks(submodule_path: Path) -> Dict[str, bool]:
    """Check symlink integrity."""
    status = {
        'coditect_exists': False,
        'coditect_accessible': False,
        'claude_exists': False,
        'framework_accessible': False
    }

    try:
        coditect_link = submodule_path / '.coditect'
        status['coditect_exists'] = coditect_link.is_symlink()
        status['coditect_accessible'] = coditect_link.exists() and coditect_link.is_dir()

        claude_link = submodule_path / '.claude'
        status['claude_exists'] = claude_link.is_symlink()

        agents_dir = coditect_link / 'agents'
        status['framework_accessible'] = agents_dir.is_dir() if coditect_link.exists() else False

    except Exception as e:
        logger.debug(f"Symlink check error: {e}")

    return status


def calculate_health_score(git_status: Dict, symlink_status: Dict) -> Tuple[int, List[str], List[str]]:
    """Calculate health score and identify issues/warnings."""
    score = 100
    issues = []
    warnings = []

    # Git status scoring
    if git_status['uncommitted'] > 0:
        deduction = min(git_status['uncommitted'] * 5, 20)
        score -= deduction
        if git_status['uncommitted'] > 5:
            issues.append(f"{git_status['uncommitted']} uncommitted changes")
        else:
            warnings.append(f"{git_status['uncommitted']} uncommitted changes")

    if git_status['unpushed'] > 0:
        deduction = min(git_status['unpushed'] * 5, 20)
        score -= deduction
        warnings.append(f"{git_status['unpushed']} unpushed commits")

    if git_status['behind'] > 0:
        score -= 10
        warnings.append(f"Behind remote by {git_status['behind']} commits")

    if git_status['detached']:
        score -= 15
        issues.append("Detached HEAD state")

    if git_status['branch'] != 'main':
        score -= 5
        warnings.append(f"On branch '{git_status['branch']}' (not main)")

    # Symlink status scoring
    if not symlink_status['coditect_exists']:
        score -= 20
        issues.append(".coditect symlink missing")

    if not symlink_status['coditect_accessible']:
        score -= 20
        issues.append(".coditect symlink broken or inaccessible")

    if not symlink_status['framework_accessible']:
        score -= 10
        issues.append("CODITECT framework not accessible")

    return max(score, 0), issues, warnings


def check_submodule_health(submodule_path: Path) -> HealthStatus:
    """Perform complete health check on submodule."""
    name = submodule_path.name
    category = submodule_path.parent.name

    git_status = check_git_status(submodule_path)
    symlink_status = check_symlinks(submodule_path)
    score, issues, warnings = calculate_health_score(git_status, symlink_status)

    return HealthStatus(
        name=name,
        path=str(submodule_path),
        category=category,
        score=score,
        git_status=git_status,
        symlink_status=symlink_status,
        issues=issues,
        warnings=warnings
    )


def generate_dashboard(health_statuses: List[HealthStatus]) -> str:
    """Generate comprehensive health dashboard."""
    total = len(health_statuses)
    avg_score = sum(s.score for s in health_statuses) / total if total > 0 else 0

    excellent = sum(1 for s in health_statuses if s.score >= 90)
    good = sum(1 for s in health_statuses if 70 <= s.score < 90)
    fair = sum(1 for s in health_statuses if 50 <= s.score < 70)
    poor = sum(1 for s in health_statuses if s.score < 50)

    dashboard = f"""# CODITECT Submodule Health Dashboard
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
Total Submodules: {total}
Average Health Score: {avg_score:.1f}/100

Health Distribution:
- Excellent (90-100): {excellent} ({excellent/total*100:.1f}%)
- Good (70-89): {good} ({good/total*100:.1f}%)
- Fair (50-69): {fair} ({fair/total*100:.1f}%)
- Poor (0-49): {poor} ({poor/total*100:.1f}%)

"""

    # Critical issues
    critical = [s for s in health_statuses if s.score < 50]
    if critical:
        dashboard += "\n## Critical Issues\n"
        for status in critical:
            dashboard += f"\n### {status.name} ({status.score}/100) ❌\n"
            dashboard += f"**Path:** {status.path}\n"
            dashboard += f"**Issues:**\n"
            for issue in status.issues:
                dashboard += f"  - {issue}\n"

    # Warnings
    warning_submodules = [s for s in health_statuses if 50 <= s.score < 70]
    if warning_submodules:
        dashboard += "\n## Warnings\n"
        for status in warning_submodules:
            dashboard += f"- {status.name} ({status.score}/100): {', '.join(status.warnings)}\n"

    return dashboard


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description='CODITECT submodule health check')
    parser.add_argument('--all', action='store_true', help='Check all submodules')
    parser.add_argument('--category', help='Check all submodules in category')
    parser.add_argument('--path', help='Check specific submodule path')
    parser.add_argument('--output', help='Output file for report (default: stdout)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Determine which submodules to check
        submodule_paths = []

        if args.all:
            submodules_dir = Path('submodules')
            for category_dir in submodules_dir.iterdir():
                if category_dir.is_dir():
                    for submodule_dir in category_dir.iterdir():
                        if submodule_dir.is_dir() and (submodule_dir / '.git').exists():
                            submodule_paths.append(submodule_dir)

        elif args.category:
            category_dir = Path('submodules') / args.category
            for submodule_dir in category_dir.iterdir():
                if submodule_dir.is_dir() and (submodule_dir / '.git').exists():
                    submodule_paths.append(submodule_dir)

        elif args.path:
            submodule_paths.append(Path(args.path))

        else:
            parser.error("Must specify --all, --category, or --path")

        # Perform health checks
        print(f"Checking {len(submodule_paths)} submodules...")
        health_statuses = []

        for path in submodule_paths:
            try:
                status = check_submodule_health(path)
                health_statuses.append(status)
                emoji = "✅" if status.score >= 70 else ("⚠️" if status.score >= 50 else "❌")
                print(f"{emoji} {status.name}: {status.score}/100")
            except Exception as e:
                logger.error(f"Failed to check {path}: {e}")

        # Generate dashboard
        dashboard = generate_dashboard(health_statuses)

        # Output
        if args.output:
            Path(args.output).write_text(dashboard)
            print(f"\nReport saved to: {args.output}")
        else:
            print("\n" + dashboard)

        return 0

    except Exception as e:
        logger.exception("Health check failed")
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
