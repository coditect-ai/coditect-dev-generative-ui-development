#!/usr/bin/env python3
"""
Multi-Tool Orchestration Hook for CODITECT

Coordinates execution across multiple tools and manages dependencies.
Detects when multiple tools work together and ensures proper sequencing.
Enables complex workflows like "Create agent → Update inventory → Commit to git → Run tests".

Event: PreToolUse and PostToolUse
Matcher: tool_name = "*" (all tools)
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import hashlib


class ToolOrchestrator:
    """Orchestrates multi-tool workflows"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.session_state_file = self.repo_root / '.coditect' / 'hooks' / '.tool-session-state.json'
        self.session_state = self.load_session_state()
        self.tool_sequence = []
        self.dependencies = {}

    def load_session_state(self) -> Dict:
        """Load session state for multi-tool tracking"""
        if self.session_state_file.exists():
            try:
                with open(self.session_state_file, 'r') as f:
                    import json as json_module
                    return json_module.load(f)
            except Exception:
                return self.init_session_state()
        return self.init_session_state()

    def init_session_state(self) -> Dict:
        """Initialize new session state"""
        return {
            'session_id': hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
            'tools_used': [],
            'tool_outputs': {},
            'dependencies': {},
            'start_time': datetime.now().isoformat(),
            'last_update': datetime.now().isoformat()
        }

    def save_session_state(self):
        """Save session state to file"""
        try:
            self.session_state['last_update'] = datetime.now().isoformat()
            with open(self.session_state_file, 'w') as f:
                import json as json_module
                json_module.dump(self.session_state, f, indent=2)
        except Exception:
            pass

    def detect_workflow_pattern(self, tool_name: str, tool_input: Dict) -> Optional[str]:
        """Detect which workflow pattern this tool is part of"""

        patterns = {
            'component_creation': {
                'tools': ['Write', 'Edit'],
                'triggers': ['.coditect/agents/', '.coditect/skills/', '.coditect/commands/'],
                'next_tools': ['Bash']  # Usually followed by git commit
            },
            'code_generation': {
                'tools': ['Write', 'Edit'],
                'triggers': ['src/', 'lib/', 'backend/'],
                'next_tools': ['Bash']  # Usually followed by tests
            },
            'documentation_update': {
                'tools': ['Write', 'Edit'],
                'triggers': ['.md', 'README', 'docs/'],
                'next_tools': ['Bash']  # Usually followed by git commit
            },
            'testing_cycle': {
                'tools': ['Bash'],
                'triggers': ['test', 'pytest', 'cargo test', 'npm test'],
                'next_tools': ['Edit']  # May need code fixes
            },
            'deployment': {
                'tools': ['Bash'],
                'triggers': ['git push', 'deploy', 'kubectl', 'docker'],
                'next_tools': ['Bash']  # May need monitoring checks
            }
        }

        file_path = tool_input.get('file_path', '') or tool_input.get('command', '')

        for pattern_name, pattern in patterns.items():
            if tool_name in pattern['tools']:
                for trigger in pattern['triggers']:
                    if trigger in file_path:
                        return pattern_name

        return None

    def get_workflow_guidance(self, pattern: str, tool_name: str) -> Optional[str]:
        """Get guidance for next steps in workflow"""

        guidance = {
            'component_creation': {
                'Write': 'Component created. Next: Verify in AGENT-INDEX.md, then commit with `git commit`',
                'Edit': 'Component updated. Next: Run tests with `bash run-tests.sh`, then commit',
                'Bash': 'Component committed. Next: Verify tests pass, then push with `git push`'
            },
            'code_generation': {
                'Write': 'Code written. Next: Run tests to validate with `npm test` or `cargo test`',
                'Edit': 'Code edited. Next: Run tests with `npm test` or similar',
                'Bash': 'Tests executed. Next: Commit changes with `git commit`'
            },
            'documentation_update': {
                'Write': 'Documentation written. Next: Verify links are valid, then commit',
                'Edit': 'Documentation edited. Next: Commit changes with `git commit`',
                'Bash': 'Documentation committed. Next: Push with `git push`'
            },
            'testing_cycle': {
                'Bash': 'Tests executed. If failures: Edit code to fix, then re-run tests'
            },
            'deployment': {
                'Bash': 'Deployment executed. Next: Monitor with observability tools, check logs'
            }
        }

        if pattern in guidance and tool_name in guidance[pattern]:
            return guidance[pattern][tool_name]
        return None

    def track_tool_execution(self, tool_name: str, tool_input: Dict, event: str):
        """Track tool execution for workflow analysis"""

        # Add to tools used
        if tool_name not in self.session_state['tools_used']:
            self.session_state['tools_used'].append(tool_name)

        # Detect workflow pattern
        pattern = self.detect_workflow_pattern(tool_name, tool_input)
        if pattern:
            self.session_state['current_pattern'] = pattern

        # Store tool output info (for dependency tracking)
        file_path = tool_input.get('file_path', '') or tool_input.get('command', '')
        if file_path:
            self.session_state['tool_outputs'][tool_name] = {
                'target': file_path,
                'event': event,
                'timestamp': datetime.now().isoformat()
            }

        # Get workflow guidance
        guidance = self.get_workflow_guidance(pattern, tool_name) if pattern else None

        return pattern, guidance

    def validate_tool_prerequisites(self, tool_name: str, previous_tools: List[str]) -> Tuple[bool, Optional[str]]:
        """Validate that prerequisite tools have been run"""

        # Component creation should have at least Write before Bash
        if tool_name == 'Bash' and 'Write' not in previous_tools and 'Edit' not in previous_tools:
            # Check if it's a git commit
            # In that case, Write might not be needed
            pass

        # Testing should come after code generation
        if 'test' in tool_name.lower():
            if 'Write' not in previous_tools and 'Edit' not in previous_tools:
                return False, "Should run tests after writing/editing code"

        return True, None

    def analyze_tool_sequence(self) -> Dict:
        """Analyze the sequence of tools used in session"""

        analysis = {
            'tool_sequence': self.session_state['tools_used'],
            'total_tools': len(self.session_state['tools_used']),
            'patterns_detected': [],
            'recommendations': []
        }

        # Detect patterns from sequence
        tools = self.session_state['tools_used']

        if 'Write' in tools or 'Edit' in tools:
            if 'Bash' in tools:
                analysis['patterns_detected'].append('code_generation_workflow')

            if '.coditect' in str(self.session_state.get('tool_outputs', {})):
                analysis['patterns_detected'].append('component_creation_workflow')

        # Generate recommendations
        if len(tools) == 0:
            analysis['recommendations'].append('Start with Write or Edit to create/modify files')
        elif len(tools) == 1 and tools[0] in ['Write', 'Edit']:
            analysis['recommendations'].append('Next: Test changes with Bash (tests) or Bash (git commit)')
        elif 'Write' in tools and 'Bash' not in tools:
            analysis['recommendations'].append('Next: Commit changes with Bash or run tests')

        return analysis


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract information
        event = hook_input.get('event', '')
        tool_name = hook_input.get('tool_name', '')
        tool_input = hook_input.get('tool_input', {})

        if not tool_name:
            print(json.dumps({"continue": True}))
            sys.exit(0)

        # Get repo root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Track tool execution
        orchestrator = ToolOrchestrator(repo_root)
        pattern, guidance = orchestrator.track_tool_execution(tool_name, tool_input, event)

        # Validate prerequisites
        previous_tools = orchestrator.session_state['tools_used']
        is_valid, error = orchestrator.validate_tool_prerequisites(tool_name, previous_tools)

        # Save session state
        orchestrator.save_session_state()

        # Return result
        result = {"continue": True}

        if guidance:
            result['guidance'] = guidance

        if pattern:
            result['workflow_hint'] = f"Detected workflow pattern: {pattern}"

        print(json.dumps(result))
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"continue": True}))
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Multi-tool orchestration error: {e}\n")
        print(json.dumps({"continue": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
