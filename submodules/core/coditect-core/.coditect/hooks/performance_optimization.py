#!/usr/bin/env python3
"""
Performance Optimization Detection Hook for CODITECT

Identifies performance anti-patterns, inefficient code, and optimization opportunities.
Suggests optimizations without blocking operations.

Event: PostToolUse
Matcher: tool_name = "Write|Edit|Bash"
Trigger: After code changes, test execution, or git commits
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class PerformanceAnalyzer:
    """Analyzes code for performance issues and optimization opportunities"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.issues = []
        self.optimizations = []

    def analyze_python_performance(self, content: str, file_path: str) -> List[str]:
        """Detect Python performance anti-patterns"""
        suggestions = []

        lines = content.split('\n')

        # Check for nested loops without optimization
        nested_loops = 0
        for i, line in enumerate(lines):
            if re.match(r'\s*for\s+\w+\s+in', line):
                nested_loops += 1
                if nested_loops > 2:
                    suggestions.append(f"Line {i+1}: Deeply nested loops (3+). Consider list comprehensions or vectorization")
                    nested_loops = 0
            elif not line.strip().startswith('for'):
                nested_loops = 0

        # Check for list concatenation in loops (inefficient)
        if re.search(r'for\s+\w+\s+in.*:\s*\n.*\+\s*=|list\s*\+\s*=', content):
            suggestions.append("List concatenation in loops detected. Use list.extend() or list comprehension instead")

        # Check for string concatenation in loops
        if re.search(r'for\s+\w+\s+in.*:\s*.*str.*\+=', content):
            suggestions.append("String concatenation in loops detected. Use list + join() instead")

        # Check for repeated function calls with same args
        if re.search(r'for\s+\w+\s+in.*:\s*.*\.find\(|\.index\(|\.count\(', content):
            suggestions.append("Multiple .find()/.index()/.count() calls detected. Cache results outside loop")

        # Check for file operations in loops
        if re.search(r'for\s+\w+\s+in.*:\s*.*open\(|\.read\(|\.write\(', content):
            suggestions.append("File operations in loops detected. Batch operations for better performance")

        # Check for dictionary access patterns
        if re.search(r'if\s+\w+\s+in\s+dict.*:\s*dict\[', content):
            suggestions.append("Dictionary existence check + access pattern. Use dict.get() instead")

        # Check for lambda in high-frequency operations
        if re.search(r'(map|filter|sorted).*lambda', content) and 'test' not in file_path:
            suggestions.append("Lambda functions in map/filter/sorted. Define function once for reuse and clarity")

        # Check for list() conversion of generators
        if re.search(r'list\(.*for.*in', content):
            suggestions.append("Converting generator to list. Avoid if possible; use generators for memory efficiency")

        # Check for N+1 query patterns (database)
        if re.search(r'for\s+\w+\s+in.*query.*:\s*.*query', content):
            suggestions.append("Potential N+1 query pattern. Use joins or batch queries instead")

        return suggestions

    def analyze_bash_performance(self, content: str) -> List[str]:
        """Detect Bash performance anti-patterns"""
        suggestions = []

        # Check for excessive piping
        pipe_count = content.count('|')
        if pipe_count > 5:
            suggestions.append(f"High pipe count ({pipe_count}). Consider combining commands or using awk/sed")

        # Check for subshells in loops
        if re.search(r'for.*\$\(.*\)', content):
            suggestions.append("Subshells in loops detected. Consider using xargs or parallel processing")

        # Check for grep/sed chains
        if re.search(r'grep.*\|.*grep|sed.*\|.*sed', content):
            suggestions.append("Chained grep/sed detected. Combine into single command for efficiency")

        # Check for unnecessary cat
        if re.search(r'cat\s+\w+\s*\|', content):
            suggestions.append("Unnecessary cat detected. Redirect file directly to command")

        # Check for external command in loop
        if re.search(r'while.*read|for.*in.*\$\(', content):
            suggestions.append("External commands in loop. Use built-in bash features when possible")

        # Check for repeated curl/wget calls
        if content.count('curl') > 2 or content.count('wget') > 2:
            suggestions.append("Multiple curl/wget calls. Consider parallel execution or session reuse")

        return suggestions

    def analyze_file_size(self, content: str, file_path: str) -> List[str]:
        """Detect when files are getting too large"""
        suggestions = []

        lines = len(content.split('\n'))
        file_size = len(content)

        # Files getting too large
        if lines > 1000:
            suggestions.append(f"Large file ({lines} lines). Consider splitting into smaller modules")

        if file_size > 100000:
            suggestions.append(f"Large file ({file_size} bytes). Split for better maintainability and load time")

        # Deep nesting
        max_indent = 0
        for line in content.split('\n'):
            indent = len(line) - len(line.lstrip())
            max_indent = max(max_indent, indent)

        if max_indent > 32:  # 8 levels of 4-space indentation
            suggestions.append(f"Deep nesting detected ({max_indent} spaces). Refactor for clarity and performance")

        return suggestions

    def analyze_git_operations(self, command: str) -> List[str]:
        """Detect performance issues in git operations"""
        suggestions = []

        # Check for large commits
        if 'git commit' in command:
            suggestions.append("Commit detected. If large commit: Use git add -p to stage changes incrementally")

        # Check for force push (risky)
        if 'git push --force' in command or 'git push -f' in command:
            suggestions.append("Force push detected. Use with caution. Prefer --force-with-lease to prevent data loss")

        # Check for operations on large repositories
        if 'git clone' in command:
            suggestions.append("Clone detected. Use --depth for large repos: git clone --depth 1 <url>")

        # Check for expensive operations
        if 'git log' in command and '--all' in command:
            suggestions.append("git log --all on large repo. Use git log <branch> for specific branch history")

        return suggestions

    def generate_report(self) -> Optional[str]:
        """Generate optimization report"""
        if not self.optimizations:
            return None

        report_lines = ["Performance Optimization Opportunities:"]

        for optimization in self.optimizations:
            report_lines.append(f"  • {optimization}")

        return "\n".join(report_lines)

    def analyze(self, file_path: str, content: str, event: str) -> Optional[Dict]:
        """Analyze file/operation for performance issues"""

        # Skip certain files
        if any(x in file_path for x in ['node_modules', '__pycache__', '.git', 'venv', '.egg-info']):
            return None

        # Analyze based on file type
        if file_path.endswith('.py'):
            self.optimizations.extend(self.analyze_python_performance(content, file_path))

        if file_path.endswith('.sh'):
            self.optimizations.extend(self.analyze_bash_performance(content))

        # Always check file size
        self.optimizations.extend(self.analyze_file_size(content, file_path))

        # Analyze git operations if bash tool
        if event == 'PostToolUse' and '.sh' in file_path or file_path.endswith(('.sh', '.bash')):
            if 'git' in content:
                self.optimizations.extend(self.analyze_git_operations(content))

        if self.optimizations:
            return {
                'has_optimizations': True,
                'count': len(self.optimizations),
                'suggestions': self.optimizations,
                'report': self.generate_report()
            }

        return None


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract information
        file_path = hook_input.get('tool_input', {}).get('file_path', '') or \
                   hook_input.get('tool_input', {}).get('command', '')
        content = hook_input.get('tool_input', {}).get('new_string', '')
        event = hook_input.get('event', 'PostToolUse')

        if not file_path or not content:
            print(json.dumps({"continue": True, "suppressOutput": True}))
            sys.exit(0)

        # Get repo root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Analyze performance
        analyzer = PerformanceAnalyzer(repo_root)
        result = analyzer.analyze(file_path, content, event)

        if result:
            # Log optimization suggestions
            report_file = repo_root + '/.performance-analysis.txt'
            try:
                with open(report_file, 'a') as f:
                    f.write(f"\n\n--- {Path(file_path).name} ({Path(__file__).stem}) ---\n")
                    f.write(result.get('report', 'No optimizations found'))
            except Exception:
                pass

            print(json.dumps({
                "continue": True,
                "suppressOutput": True
            }))
        else:
            print(json.dumps({"continue": True, "suppressOutput": True}))

        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Performance analysis error: {e}\n")
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
