#!/usr/bin/env python3
"""
Dependency Management Hook for CODITECT

Tracks, validates, and manages dependencies across agents, skills, and commands.
Detects circular dependencies, missing dependencies, and unused imports.
Maintains dependency graph for system resilience.

Event: PostToolUse (after Write/Edit)
Matcher: tool_name = "Write|Edit"
Trigger: When component files are created/modified
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


class DependencyManager:
    """Manages and validates dependencies"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.dependency_graph = {}
        self.circular_deps = []
        self.missing_deps = []
        self.unused_imports = []
        self.load_dependency_graph()

    def load_dependency_graph(self):
        """Load existing dependency graph"""
        graph_file = self.repo_root / '.coditect' / 'hooks' / '.dependency-graph.json'

        if graph_file.exists():
            try:
                with open(graph_file, 'r') as f:
                    import json as json_module
                    self.dependency_graph = json_module.load(f)
            except Exception:
                self.dependency_graph = {}

    def save_dependency_graph(self):
        """Save dependency graph to file"""
        graph_file = self.repo_root / '.coditect' / 'hooks' / '.dependency-graph.json'

        try:
            with open(graph_file, 'w') as f:
                import json as json_module
                json_module.dump(self.dependency_graph, f, indent=2)
        except Exception:
            pass

    def extract_dependencies(self, file_path: str, content: str) -> Dict[str, List[str]]:
        """Extract dependencies from file"""

        dependencies = {
            'agents': [],
            'skills': [],
            'commands': [],
            'imports': [],
            'external': []
        }

        # Extract agent/skill/command references
        # Pattern: /analyze-hooks, agent-name, skill-name
        agent_pattern = r'(?:Use |invoke |call |execute )(?:agent[_-])?([a-z0-9-]+)'
        for match in re.finditer(agent_pattern, content, re.IGNORECASE):
            dependencies['agents'].append(match.group(1))

        # Pattern: skill: skill-name or skill skill-name
        skill_pattern = r'(?:skill[_:\s]+)([a-z0-9-]+)'
        for match in re.finditer(skill_pattern, content, re.IGNORECASE):
            dependencies['skills'].append(match.group(1))

        # Pattern: /command-name or command-name
        command_pattern = r'/([a-z0-9-]+)(?:[\s\n]|$)'
        for match in re.finditer(command_pattern, content):
            dependencies['commands'].append(match.group(1))

        # Extract Python imports
        if file_path.endswith('.py'):
            import_pattern = r'^(?:from|import)\s+([a-zA-Z0-9_.]+)'
            for match in re.finditer(import_pattern, content, re.MULTILINE):
                module = match.group(1).split('.')[0]
                dependencies['imports'].append(module)

        # Extract external tool dependencies
        external_tools = ['curl', 'wget', 'docker', 'kubectl', 'git', 'python3', 'bash']
        for tool in external_tools:
            if re.search(rf'\b{tool}\b', content):
                dependencies['external'].append(tool)

        # Remove duplicates
        for key in dependencies:
            dependencies[key] = list(set(dependencies[key]))

        return dependencies

    def check_circular_dependencies(self, component: str, deps: List[str], visited: Optional[Set] = None) -> List[str]:
        """Check for circular dependencies"""
        if visited is None:
            visited = set()

        circular = []

        if component in visited:
            circular.append(f"Circular dependency detected: {component}")
            return circular

        visited.add(component)

        for dep in deps:
            if dep in self.dependency_graph:
                sub_deps = self.dependency_graph[dep].get('deps', [])
                if component in sub_deps:
                    circular.append(f"Circular dependency: {component} ↔ {dep}")
                else:
                    circular.extend(self.check_circular_dependencies(dep, sub_deps, visited.copy()))

        return circular

    def check_missing_dependencies(self, deps: Dict[str, List[str]]) -> List[str]:
        """Check for missing dependencies"""
        missing = []

        # Check if referenced agents/skills exist
        agents_dir = self.repo_root / '.coditect' / 'agents'
        skills_dir = self.repo_root / '.coditect' / 'skills'
        commands_dir = self.repo_root / '.coditect' / 'commands'

        for agent in deps['agents']:
            agent_file = agents_dir / f"{agent}.md"
            if not agent_file.exists():
                missing.append(f"Agent not found: {agent}")

        for skill in deps['skills']:
            skill_file = skills_dir / f"{skill}" / "SKILL.md"
            if not skill_file.exists():
                missing.append(f"Skill not found: {skill}")

        for command in deps['commands']:
            command_file = commands_dir / f"{command}.md"
            if not command_file.exists():
                # Don't warn if it's an external command
                if not any(x in command for x in ['git', 'curl', 'docker', 'python']):
                    missing.append(f"Command not found: {command}")

        return missing

    def check_unused_imports(self, file_path: str, content: str, imports: List[str]) -> List[str]:
        """Check for unused imports"""
        unused = []

        if not file_path.endswith('.py'):
            return unused

        # Skip test files
        if 'test' in file_path:
            return unused

        lines = content.split('\n')

        for imp in imports:
            # Check if import is used in code
            usage_count = 0

            for line in lines:
                # Skip import lines
                if line.strip().startswith('import') or line.strip().startswith('from'):
                    continue

                # Count usage
                if re.search(rf'\b{imp}\b', line):
                    usage_count += 1

            if usage_count == 0:
                unused.append(f"Unused import: {imp}")

        return unused

    def validate_dependencies(self, file_path: str, content: str) -> Dict:
        """Validate all dependencies for a file"""

        result = {
            'file': file_path,
            'dependencies': {},
            'issues': [],
            'warnings': []
        }

        # Extract dependencies
        deps = self.extract_dependencies(file_path, content)
        result['dependencies'] = deps

        # Check circular dependencies
        if deps['agents']:
            circular = self.check_circular_dependencies(
                Path(file_path).stem,
                deps['agents']
            )
            result['issues'].extend(circular)

        # Check missing dependencies
        missing = self.check_missing_dependencies(deps)
        result['issues'].extend(missing)

        # Check unused imports
        unused = self.check_unused_imports(file_path, content, deps['imports'])
        result['warnings'].extend(unused)

        # Check for external tool dependencies
        for tool in deps['external']:
            result['dependencies']['external_tools'] = deps['external']

        return result

    def update_dependency_graph(self, component: str, deps: Dict[str, List[str]]):
        """Update dependency graph with new component"""
        all_deps = deps['agents'] + deps['skills'] + deps['commands'] + deps['imports']

        self.dependency_graph[component] = {
            'deps': all_deps,
            'import_deps': deps['imports'],
            'external_deps': deps['external'],
            'last_updated': str(Path(__file__).stat().st_mtime)
        }

        self.save_dependency_graph()


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract information
        file_path = hook_input.get('tool_input', {}).get('file_path', '')
        content = hook_input.get('tool_input', {}).get('new_string', '')

        if not file_path or not content:
            print(json.dumps({"continue": True, "suppressOutput": True}))
            sys.exit(0)

        # Skip certain files
        if any(x in file_path for x in ['.git', 'node_modules', '__pycache__', '.egg-info']):
            print(json.dumps({"continue": True, "suppressOutput": True}))
            sys.exit(0)

        # Get repo root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Validate dependencies
        manager = DependencyManager(repo_root)
        validation = manager.validate_dependencies(file_path, content)

        # Update dependency graph
        component_name = Path(file_path).stem.replace('-', '_')
        manager.update_dependency_graph(component_name, validation['dependencies'])

        # Log report if there are issues
        if validation['issues'] or validation['warnings']:
            report_file = repo_root + '/.dependency-report.txt'
            try:
                with open(report_file, 'a') as f:
                    f.write(f"\n\n--- {Path(file_path).name} ({Path(__file__).stem}) ---\n")
                    if validation['issues']:
                        f.write("Issues:\n")
                        for issue in validation['issues']:
                            f.write(f"  ❌ {issue}\n")
                    if validation['warnings']:
                        f.write("Warnings:\n")
                        for warning in validation['warnings']:
                            f.write(f"  ⚠️ {warning}\n")
            except Exception:
                pass

        # Always allow operation (non-blocking hook)
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Dependency management error: {e}\n")
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
