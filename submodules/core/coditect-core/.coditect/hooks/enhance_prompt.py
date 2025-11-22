#!/usr/bin/env python3
"""
Prompt Enhancement Hook for CODITECT

Automatically enhances user prompts with relevant CODITECT context before Claude processes them.
Adds framework context, project CLAUDE.md sections, and MEMORY-CONTEXT references to provide
intelligent context without duplicating information.

Event: UserPromptSubmit
Matcher: {} (matches all prompts)
"""

import json
import sys
import os
from pathlib import Path
from typing import Optional, Dict, List


class PromptEnhancer:
    """Enhances prompts with CODITECT context"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.coditect_dir = self.repo_root / '.coditect'
        self.cache = {}

    def load_file(self, path: Path) -> Optional[str]:
        """Load file with caching"""
        if path in self.cache:
            return self.cache[path]

        if not path.exists():
            return None

        try:
            with open(path, 'r') as f:
                content = f.read()
            self.cache[path] = content
            return content
        except Exception:
            return None

    def extract_relevant_sections(self, prompt: str) -> List[str]:
        """Extract relevant sections from framework docs based on prompt keywords"""
        sections = []

        # Check CLAUDE.md for relevant sections
        claude_md = self.repo_root / 'CLAUDE.md'
        claude_content = self.load_file(claude_md)

        if not claude_content:
            return sections

        # Keywords to look for in prompt
        keywords_to_sections = {
            'agent': [
                '## 🎯 Agent Framework',
                '## 📋 CODITECT Framework Components',
                'Agent Invocation Method'
            ],
            'command': [
                '## 🚀 Slash Command Quick Start',
                'commands/README.md'
            ],
            'hook': [
                '## 🎣 Claude Code Hooks Implementation Workflow',
                'hooks framework'
            ],
            'project': [
                '## 📋 Project Planning',
                'PROJECT-PLAN.md',
                'TASKLIST'
            ],
            'phase': [
                '## Implementation Roadmap',
                'Phase'
            ],
            'test': [
                '## Quality Gates & Testing'
            ],
            'architecture': [
                'Architecture Overview',
                'Distributed Intelligence'
            ],
            'training': [
                '## 🎓 User Training System',
                'user-training'
            ]
        }

        # Find relevant sections based on keywords in prompt
        prompt_lower = prompt.lower()
        found_sections = set()

        for keyword, section_list in keywords_to_sections.items():
            if keyword in prompt_lower:
                found_sections.update(section_list)

        return list(found_sections)

    def get_context_hint(self, prompt: str) -> Optional[str]:
        """Generate a context hint to add to the prompt"""

        prompt_lower = prompt.lower()

        # Determine context level based on prompt content
        hints = []

        # Check if creating new component
        if any(kw in prompt_lower for kw in ['new agent', 'create agent', 'new skill', 'new command', 'new hook']):
            hints.append(
                "\n[CODITECT: This appears to be a component creation task. "
                "Use STANDARDS.md and the component validation hook as reference.]"
            )

        # Check if related to hooks
        if 'hook' in prompt_lower or 'automation' in prompt_lower:
            hints.append(
                "\n[CODITECT: Hooks framework available. See HOOKS-COMPREHENSIVE-ANALYSIS.md "
                "for implementation patterns and Phase 1A quick wins.]"
            )

        # Check if related to project planning
        if any(kw in prompt_lower for kw in ['project plan', 'tasklist', 'roadmap', 'phase']):
            hints.append(
                "\n[CODITECT: Refer to PROJECT-PLAN.md and TASKLIST-WITH-CHECKBOXES.md "
                "for current phase and task tracking.]"
            )

        # Check if asking about architecture
        if any(kw in prompt_lower for kw in ['architecture', 'design', 'structure', 'how does']):
            hints.append(
                "\n[CODITECT: See WHAT-IS-CODITECT.md and Architecture Overview section "
                "for distributed intelligence architecture details.]"
            )

        # Check if asking about agents/commands
        if any(kw in prompt_lower for kw in ['agent', 'command', 'skill', 'slash']):
            hints.append(
                "\n[CODITECT: Use AGENT-INDEX.md, commands/README.md, and COMPLETE-INVENTORY.md "
                "to find existing components before creating new ones.]"
            )

        return ''.join(hints) if hints else None

    def enhance(self, prompt: str) -> str:
        """Enhance prompt with CODITECT context"""

        if not prompt or len(prompt) < 10:
            # Too short to enhance meaningfully
            return prompt

        # Add context hint
        context_hint = self.get_context_hint(prompt)

        if context_hint:
            # Add context hint to end of prompt
            enhanced = prompt + context_hint
            return enhanced

        return prompt


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract user prompt
        user_prompt = hook_input.get('prompt', '')

        if not user_prompt:
            # No prompt to enhance
            print(json.dumps({"continue": True}))
            sys.exit(0)

        # Get repository root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Enhance prompt
        enhancer = PromptEnhancer(repo_root)
        enhanced_prompt = enhancer.enhance(user_prompt)

        # Return enhanced prompt
        if enhanced_prompt != user_prompt:
            print(json.dumps({
                "continue": True,
                "modifiedPrompt": enhanced_prompt,
                "suppressOutput": False
            }))
        else:
            print(json.dumps({"continue": True}))

        sys.exit(0)

    except json.JSONDecodeError as e:
        # Can't parse input, just continue
        print(json.dumps({"continue": True}))
        sys.exit(0)
    except Exception as e:
        # Log error but allow operation to continue
        sys.stderr.write(f"Prompt enhancement hook error: {e}\n")
        print(json.dumps({"continue": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
