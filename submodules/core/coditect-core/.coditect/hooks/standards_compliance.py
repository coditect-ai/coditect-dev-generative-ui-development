#!/usr/bin/env python3
"""
Standards Compliance Validation Hook for CODITECT

Enforces STANDARDS.md compliance for all code changes.
Prevents modifications that violate architectural decisions and naming conventions.

Event: PreToolUse
Matcher: tool_name = "Edit"
Trigger: When editing any .py, .sh, .md files
"""

import json
import sys
import re
from pathlib import Path
from typing import Tuple, List, Optional


class ComplianceChecker:
    """Checks code compliance against STANDARDS.md"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.standards_path = self.repo_root / 'STANDARDS.md'
        self.standards = self.load_standards()

    def load_standards(self) -> dict:
        """Load STANDARDS.md"""
        if not self.standards_path.exists():
            return {}

        try:
            with open(self.standards_path, 'r') as f:
                return {'content': f.read()}
        except Exception:
            return {}

    def check_file_naming(self, file_path: str) -> List[str]:
        """Check file naming conventions"""
        violations = []

        path = Path(file_path)
        filename = path.name

        # Check agents naming (kebab-case.md)
        if '/.coditect/agents/' in file_path:
            if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*\.md$', filename):
                violations.append(f"Agent file must be kebab-case: {filename}")

        # Check skills naming
        elif '/.coditect/skills/' in file_path:
            if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*\.md$|^SKILL\.md$', filename):
                violations.append(f"Skill file must be kebab-case or SKILL.md: {filename}")

        # Check commands naming
        elif '/.coditect/commands/' in file_path:
            if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*\.md$', filename):
                violations.append(f"Command file must be kebab-case: {filename}")

        # Check Python files (snake_case.py)
        elif file_path.endswith('.py'):
            if not re.match(r'^[a-z0-9_]+\.py$', filename) and not filename.startswith('test_'):
                violations.append(f"Python file should be snake_case: {filename}")

        # Check Bash files (kebab-case.sh)
        elif file_path.endswith('.sh'):
            if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*\.sh$', filename):
                violations.append(f"Bash file should be kebab-case: {filename}")

        return violations

    def check_content_standards(self, file_path: str, content: str) -> List[str]:
        """Check content against standards"""
        violations = []

        # Skip empty or very short content
        if not content or len(content) < 50:
            return violations

        # Check for disallowed patterns
        if any(bad in content for bad in ['TODO', 'FIXME', 'HACK', 'XXX']):
            # These might be allowed in some contexts, just warn
            pass

        # Check for required headers in component files
        if any(pattern in file_path for pattern in ['agents/', 'skills/', 'commands/']):
            if not content.startswith('---'):
                violations.append("Component files must start with YAML frontmatter (---)")

        # Check for proper markdown headers
        if file_path.endswith('.md'):
            lines = content.split('\n')

            # Check header hierarchy (no H1 at top except in special files)
            if not any(x in file_path for x in ['README', 'STANDARDS', 'CLAUDE']):
                h1_count = sum(1 for line in lines if line.startswith('# '))
                if h1_count > 1:
                    violations.append("Markdown files should have at most one H1 header")

        # Check Python style basics
        if file_path.endswith('.py'):
            lines = content.split('\n')

            # Check for docstrings in functions
            in_function = False
            for i, line in enumerate(lines):
                if re.match(r'^\s*def \w+', line):
                    in_function = True
                    # Check if next non-empty line is a docstring
                    for next_line in lines[i+1:i+5]:
                        if next_line.strip() and not any(x in next_line for x in ['"""', "'''", '# ', 'return']):
                            if not in_function:
                                violations.append(f"Function missing docstring near line {i}")
                            in_function = False
                            break
                        if '"""' in next_line or "'''" in next_line:
                            in_function = False
                            break

        return violations

    def check_security(self, file_path: str, content: str) -> List[str]:
        """Check for security issues"""
        violations = []

        # Check for hardcoded secrets/credentials
        secret_patterns = [
            r'api[_-]?key\s*[=:]\s*["\'][\w-]+["\']',
            r'password\s*[=:]\s*["\'][\w-]+["\']',
            r'secret\s*[=:]\s*["\'][\w-]+["\']',
            r'token\s*[=:]\s*["\'][\w-]+["\']',
            r'aws[_-]?key\s*[=:]\s*["\'][\w-]+["\']',
        ]

        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append("Potential hardcoded secret/credential detected - should use environment variables")

        # Check for dangerous shell commands in .sh files
        if file_path.endswith('.sh'):
            dangerous_patterns = [
                r'rm\s+-rf\s+/',
                r'chmod\s+777',
                r'eval\s+',
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, content):
                    violations.append(f"Dangerous shell pattern detected: {pattern}")

        return violations

    def check_all(self, file_path: str, content: str) -> Tuple[bool, List[str]]:
        """Run all compliance checks"""
        violations = []

        violations.extend(self.check_file_naming(file_path))
        violations.extend(self.check_content_standards(file_path, content))
        violations.extend(self.check_security(file_path, content))

        return len(violations) == 0, violations


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract file information
        file_path = hook_input.get('tool_input', {}).get('file_path', '')
        new_content = hook_input.get('tool_input', {}).get('new_string', '')

        if not file_path:
            # Can't check without file path, allow
            print(json.dumps({"continue": True}))
            sys.exit(0)

        # Skip certain paths that are auto-generated or external
        if any(x in file_path for x in [
            'node_modules/', 'venv/', '.git/', 'dist/', 'build/',
            '__pycache__', '.pytest_cache', '.egg-info'
        ]):
            print(json.dumps({"continue": True}))
            sys.exit(0)

        # Get repo root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Check compliance
        checker = ComplianceChecker(repo_root)
        is_compliant, violations = checker.check_all(file_path, new_content)

        if is_compliant:
            print(json.dumps({"continue": True}))
            sys.exit(0)
        else:
            # Format error message
            error_msg = "Standards compliance violations:\n"
            for violation in violations:
                error_msg += f"  - {violation}\n"

            print(json.dumps({
                "continue": False,
                "stopReason": error_msg.rstrip()
            }))
            sys.exit(1)

    except json.JSONDecodeError as e:
        print(json.dumps({"continue": False, "stopReason": f"Hook error: {e}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"continue": False, "stopReason": f"Hook error: {e}"}))
        sys.exit(1)


if __name__ == '__main__':
    main()
