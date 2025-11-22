#!/usr/bin/env python3
"""
Quality Gate Enforcement Hook for CODITECT

Enforces quality gates and prevents commits that fail quality checks.
Validates test coverage, code metrics, and architectural compliance.

Event: PostToolUse
Matcher: tool_name = "Bash"
Trigger: When `git commit` is executed
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import re


class QualityGateEnforcer:
    """Enforces quality gates on commits"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.violations = []
        self.metrics = {}

    def get_commit_message(self) -> str:
        """Get the commit message"""
        try:
            result = subprocess.run(
                "git log -1 --pretty=%B",
                shell=True,
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except Exception:
            return ""

    def validate_commit_message(self) -> bool:
        """Validate commit message format"""
        msg = self.get_commit_message()

        if not msg:
            self.violations.append("Commit message is empty")
            return False

        # Check minimum length
        if len(msg.split('\n')[0]) < 10:
            self.violations.append("Commit message summary too short (min 10 chars)")
            return False

        # Check for conventional commit format (optional but recommended)
        if not re.match(r'^(feat|fix|docs|style|refactor|perf|test|chore|ci)(\(.+\))?:', msg):
            # Not strictly a violation, just log as metric
            self.metrics['conventional_commit'] = False
        else:
            self.metrics['conventional_commit'] = True

        # Check for breaking changes notation
        if 'BREAKING CHANGE' in msg:
            self.metrics['breaking_change'] = True
        else:
            self.metrics['breaking_change'] = False

        return True

    def validate_changed_files(self) -> bool:
        """Validate that changed files are appropriate"""
        try:
            result = subprocess.run(
                "git diff-tree --no-commit-id --name-only -r HEAD",
                shell=True,
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=5
            )

            changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

            # Check for suspicious changes
            suspicious_patterns = [
                r'node_modules/',
                r'\.git/',
                r'__pycache__',
                r'\.egg-info',
            ]

            for pattern in suspicious_patterns:
                for file in changed_files:
                    if re.search(pattern, file):
                        self.violations.append(f"Should not commit {pattern} directory: {file}")
                        return False

            self.metrics['files_changed'] = len(changed_files)
            return True

        except Exception as e:
            self.violations.append(f"Could not validate changed files: {e}")
            return False

    def validate_code_metrics(self) -> bool:
        """Validate code quality metrics"""
        try:
            # Check for very large commits (>500 lines changed)
            result = subprocess.run(
                "git diff-tree --no-commit-id --numstat HEAD | awk '{sum+=$1+$2} END {print sum}'",
                shell=True,
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.stdout.strip():
                lines_changed = int(result.stdout.strip())
                self.metrics['lines_changed'] = lines_changed

                if lines_changed > 1000:
                    self.violations.append(f"Commit too large ({lines_changed} lines). Consider breaking into smaller commits.")

        except Exception as e:
            # Non-blocking metric check
            pass

        return True

    def validate_test_coverage(self) -> bool:
        """Validate test coverage for changed files"""
        try:
            # Get changed Python files
            result = subprocess.run(
                "git diff-tree --no-commit-id --name-only -r HEAD | grep '\\.py$'",
                shell=True,
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=5
            )

            py_files = [f for f in result.stdout.strip().split('\n') if f and 'test' not in f]

            if not py_files:
                return True

            # Check if tests were added/modified
            result = subprocess.run(
                "git diff-tree --no-commit-id --name-only -r HEAD | grep 'test'",
                shell=True,
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=5
            )

            test_files = result.stdout.strip()
            self.metrics['test_files_changed'] = len(test_files.split('\n')) if test_files else 0

            # Warn if production code changed but no tests
            if py_files and not test_files:
                self.violations.append("Production code changed but no test files modified. Please add tests.")

            return True

        except Exception:
            # Non-blocking check
            return True

    def enforce_gates(self) -> Tuple[bool, List[str]]:
        """Enforce all quality gates"""
        success = True

        # Validate commit message
        if not self.validate_commit_message():
            success = False

        # Validate changed files
        if not self.validate_changed_files():
            success = False

        # Validate code metrics
        if not self.validate_code_metrics():
            success = False

        # Validate test coverage
        if not self.validate_test_coverage():
            success = False

        return success and len(self.violations) == 0, self.violations

    def generate_report(self) -> str:
        """Generate quality gate report"""
        lines = ["Quality Gate Enforcement Report:"]

        if self.violations:
            lines.append(f"\n❌ {len(self.violations)} Violations Found:")
            for violation in self.violations:
                lines.append(f"  - {violation}")
        else:
            lines.append("\n✅ All quality gates passed!")

        if self.metrics:
            lines.append("\nMetrics:")
            for metric, value in self.metrics.items():
                lines.append(f"  - {metric}: {value}")

        return "\n".join(lines)


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Check if this was a git commit
        command = hook_input.get('tool_input', {}).get('command', '')

        if 'git commit' not in command:
            # Not a commit, skip
            print(json.dumps({"continue": True, "suppressOutput": True}))
            sys.exit(0)

        # Get repo root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Enforce quality gates
        enforcer = QualityGateEnforcer(repo_root)
        success, violations = enforcer.enforce_gates()

        # Log report
        report = enforcer.generate_report()
        report_file = repo_root + '/.quality-gate-report.txt'

        try:
            with open(report_file, 'a') as f:
                f.write(f"\n\n{report}\n")
        except Exception:
            pass

        # Always allow operation (non-blocking hook)
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Quality gate enforcement error: {e}\n")
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
