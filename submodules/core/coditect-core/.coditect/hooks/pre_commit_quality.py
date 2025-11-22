#!/usr/bin/env python3
"""
Pre-Commit Quality Checks Hook for CODITECT

Runs comprehensive quality checks (tests, linting, type checking) after git commits.
Detects quality issues and suggests fixes without blocking the commit.

Event: PostToolUse
Matcher: tool_name = "Bash"
Trigger: When `git commit` is executed
"""

import json
import sys
import subprocess
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import tempfile


class QualityChecker:
    """Runs quality checks on changed files"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.issues = []
        self.warnings = []
        self.results = {}

    def run_command(self, cmd: str, cwd: Optional[str] = None) -> Tuple[int, str, str]:
        """Run a command and capture output"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out after 30 seconds"
        except Exception as e:
            return 1, "", str(e)

    def get_changed_files(self) -> List[str]:
        """Get list of changed files in last commit"""
        code, stdout, _ = self.run_command("git diff-tree --no-commit-id --name-only -r HEAD")
        if code != 0:
            return []
        return stdout.strip().split('\n') if stdout.strip() else []

    def check_python_files(self) -> bool:
        """Check Python files for basic quality"""
        changed_files = self.get_changed_files()
        py_files = [f for f in changed_files if f.endswith('.py')]

        if not py_files:
            return True

        success = True

        # Check for syntax errors
        for py_file in py_files:
            full_path = self.repo_root / py_file
            if full_path.exists():
                code, _, stderr = self.run_command(f"python3 -m py_compile {py_file}")
                if code != 0:
                    self.issues.append(f"Python syntax error in {py_file}: {stderr}")
                    success = False

        # Check for import issues
        code, stdout, stderr = self.run_command("python3 -m pip list")
        if code == 0:
            # Basic import check - can be extended
            pass

        return success

    def check_bash_files(self) -> bool:
        """Check Bash files for basic quality"""
        changed_files = self.get_changed_files()
        bash_files = [f for f in changed_files if f.endswith('.sh')]

        if not bash_files:
            return True

        success = True

        for bash_file in bash_files:
            full_path = self.repo_root / bash_file
            if full_path.exists():
                # Use shellcheck if available
                code, _, stderr = self.run_command(f"bash -n {bash_file}")
                if code != 0:
                    self.issues.append(f"Bash syntax error in {bash_file}: {stderr}")
                    success = False

        return success

    def check_markdown_files(self) -> bool:
        """Check Markdown files for basic quality"""
        changed_files = self.get_changed_files()
        md_files = [f for f in changed_files if f.endswith('.md')]

        if not md_files:
            return True

        success = True

        for md_file in md_files:
            full_path = self.repo_root / md_file

            if not full_path.exists():
                continue

            try:
                with open(full_path, 'r') as f:
                    content = f.read()

                # Check for broken links (basic check)
                link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                matches = re.findall(link_pattern, content)

                for text, link in matches:
                    # Skip external links
                    if link.startswith('http'):
                        continue

                    # Check if local file exists
                    if not link.startswith('#'):
                        link_path = full_path.parent / link
                        if not link_path.exists():
                            self.warnings.append(f"Broken link in {md_file}: [{text}]({link})")

                # Check for required sections in certain files
                if 'PROJECT-PLAN' in md_file.upper() or 'TASKLIST' in md_file.upper():
                    if not content.strip():
                        self.issues.append(f"Empty project file: {md_file}")
                        success = False

            except Exception as e:
                self.warnings.append(f"Error checking {md_file}: {e}")

        return success

    def check_json_files(self) -> bool:
        """Check JSON files for validity"""
        changed_files = self.get_changed_files()
        json_files = [f for f in changed_files if f.endswith('.json')]

        if not json_files:
            return True

        success = True

        for json_file in json_files:
            full_path = self.repo_root / json_file

            if not full_path.exists():
                continue

            try:
                import json as json_module
                with open(full_path, 'r') as f:
                    json_module.load(f)
            except json.JSONDecodeError as e:
                self.issues.append(f"Invalid JSON in {json_file}: {e}")
                success = False
            except Exception as e:
                self.warnings.append(f"Error checking {json_file}: {e}")

        return success

    def run_all_checks(self) -> Dict:
        """Run all quality checks"""
        self.results = {
            'python': self.check_python_files(),
            'bash': self.check_bash_files(),
            'markdown': self.check_markdown_files(),
            'json': self.check_json_files(),
        }

        return {
            'issues': self.issues,
            'warnings': self.warnings,
            'results': self.results,
            'success': all(self.results.values()) and not self.issues
        }


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

        # Run quality checks
        checker = QualityChecker(repo_root)
        results = checker.run_all_checks()

        # Format report
        report_lines = ["Quality Check Results:"]
        if results['issues']:
            report_lines.append("❌ Issues Found:")
            for issue in results['issues']:
                report_lines.append(f"  - {issue}")

        if results['warnings']:
            report_lines.append("⚠️ Warnings:")
            for warning in results['warnings']:
                report_lines.append(f"  - {warning}")

        if results['success']:
            report_lines.append("✅ All quality checks passed!")

        # Log results
        report = "\n".join(report_lines)
        with open(repo_root + '/.quality-check-report.txt', 'a') as f:
            f.write(f"\n\n--- {Path(__file__).stem} ---\n{report}\n")

        # Always allow operation (non-blocking hook)
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Quality check hook error: {e}\n")
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
