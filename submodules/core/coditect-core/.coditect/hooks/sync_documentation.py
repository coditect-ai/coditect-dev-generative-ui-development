#!/usr/bin/env python3
"""
Documentation Sync Hook for CODITECT

Automatically updates component inventories and documentation when new files are created.
Keeps AGENT-INDEX.md, skills catalog, and COMPLETE-INVENTORY.md in sync with actual components.

Event: PostToolUse
Matcher: tool_name = "Write"
Trigger: When new .coditect/agents/*.md, .coditect/skills/*/SKILL.md, or .coditect/commands/*.md files are created
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime


class DocumentationSyncer:
    """Syncs documentation when new components are created"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.coditect_dir = self.repo_root / '.coditect'

    def extract_component_info(self, file_path: str, content: str) -> Optional[Dict]:
        """Extract metadata from component file"""

        if not content or content.startswith('---') is False:
            return None

        # Parse YAML frontmatter
        parts = content.split('---')
        if len(parts) < 3:
            return None

        yaml_content = parts[1]

        # Extract fields
        info = {
            'file_path': file_path,
            'created': datetime.now().isoformat()
        }

        for line in yaml_content.split('\n'):
            if ':' not in line or line.strip().startswith('-'):
                continue

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')

            info[key] = value

        return info

    def should_update_inventory(self, file_path: str) -> bool:
        """Check if file should trigger inventory update"""
        return any(pattern in file_path for pattern in [
            '/.coditect/agents/',
            '/.coditect/skills/',
            '/.coditect/commands/'
        ])

    def get_component_type(self, file_path: str) -> Optional[str]:
        """Determine component type from file path"""
        if '/.coditect/agents/' in file_path:
            return 'agent'
        elif '/.coditect/skills/' in file_path:
            return 'skill'
        elif '/.coditect/commands/' in file_path:
            return 'command'
        return None

    def update_agent_index(self, agent_info: Dict) -> bool:
        """Update AGENT-INDEX.md with new agent"""
        agent_index_path = self.coditect_dir / 'AGENT-INDEX.md'

        if not agent_index_path.exists():
            # Create new AGENT-INDEX.md
            content = f"""# CODITECT Agent Index

Complete catalog of all {len([1])} agents in the CODITECT framework.

## Agents by Category

### General Purpose
- **{agent_info.get('name', 'unknown')}** - {agent_info.get('description', 'No description')}
  - File: {agent_info.get('file_path', 'unknown')}
  - Model: {agent_info.get('model', 'unknown')}
  - Created: {agent_info.get('created', 'unknown')}

---

*Last Updated: {datetime.now().isoformat()}*
"""
            try:
                with open(agent_index_path, 'w') as f:
                    f.write(content)
                return True
            except Exception as e:
                sys.stderr.write(f"Failed to create AGENT-INDEX.md: {e}\n")
                return False
        else:
            # Append to existing index
            try:
                with open(agent_index_path, 'r') as f:
                    content = f.read()

                # Check if agent already in index
                if f"**{agent_info.get('name')}**" in content:
                    return True  # Already indexed

                # Add agent to appropriate section
                entry = f"\n- **{agent_info.get('name')}** - {agent_info.get('description', 'No description')}\n"
                entry += f"  - File: {agent_info.get('file_path', 'unknown')}\n"
                entry += f"  - Model: {agent_info.get('model', 'unknown')}\n"

                # Insert before the last --- line
                parts = content.rsplit('\n---', 1)
                updated = parts[0] + entry + '\n\n---' + (parts[1] if len(parts) > 1 else '')

                # Update timestamp
                updated = re.sub(
                    r'\*Last Updated:.*\*',
                    f'*Last Updated: {datetime.now().isoformat()}*',
                    updated
                )

                with open(agent_index_path, 'w') as f:
                    f.write(updated)

                return True

            except Exception as e:
                sys.stderr.write(f"Failed to update AGENT-INDEX.md: {e}\n")
                return False

    def update_complete_inventory(self, component_type: str, component_info: Dict) -> bool:
        """Update COMPLETE-INVENTORY.md with new component"""
        inventory_path = self.coditect_dir / 'COMPLETE-INVENTORY.md'

        if not inventory_path.exists():
            # Create new COMPLETE-INVENTORY.md
            header = f"""# CODITECT Complete Component Inventory

## Summary

- **Agents:** 1
- **Skills:** 0
- **Commands:** 0
- **Scripts:** 0
- **Total Components:** 1

## Components by Type

### Agents (1)
- {component_info.get('name', 'unknown')} - {component_info.get('description', 'No description')}

---

*Last Updated: {datetime.now().isoformat()}*
"""
            try:
                with open(inventory_path, 'w') as f:
                    f.write(header)
                return True
            except Exception as e:
                sys.stderr.write(f"Failed to create COMPLETE-INVENTORY.md: {e}\n")
                return False
        else:
            # Update existing inventory
            try:
                with open(inventory_path, 'r') as f:
                    content = f.read()

                # Check if already in inventory
                if component_info.get('name') in content:
                    return True  # Already documented

                # Update last modified time
                content = re.sub(
                    r'\*Last Updated:.*\*',
                    f'*Last Updated: {datetime.now().isoformat()}*',
                    content
                )

                with open(inventory_path, 'w') as f:
                    f.write(content)

                return True

            except Exception as e:
                sys.stderr.write(f"Failed to update COMPLETE-INVENTORY.md: {e}\n")
                return False

    def sync(self, file_path: str, content: str) -> bool:
        """Perform documentation sync"""

        # Check if this file should trigger sync
        if not self.should_update_inventory(file_path):
            return True

        # Extract component info
        component_info = self.extract_component_info(file_path, content)
        if not component_info:
            return True  # Can't extract info, skip silently

        # Get component type
        component_type = self.get_component_type(file_path)
        if not component_type:
            return True

        # Update appropriate index
        if component_type == 'agent':
            return self.update_agent_index(component_info)
        elif component_type == 'skill':
            return self.update_complete_inventory('skill', component_info)
        elif component_type == 'command':
            return self.update_complete_inventory('command', component_info)

        return True


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract file information
        file_path = hook_input.get('tool_input', {}).get('file_path', '')
        new_content = hook_input.get('tool_input', {}).get('new_string', '')

        if not file_path or not new_content:
            # Missing information, skip
            print(json.dumps({"continue": True, "suppressOutput": True}))
            sys.exit(0)

        # Get repository root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Perform synchronization
        syncer = DocumentationSyncer(repo_root)
        success = syncer.sync(file_path, new_content)

        # Always return success (non-blocking hook)
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)

    except json.JSONDecodeError:
        # Can't parse input, continue silently
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)
    except Exception as e:
        # Log error but continue (non-blocking)
        sys.stderr.write(f"Documentation sync hook error: {e}\n")
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
