#!/usr/bin/env python3
"""
Component Validation Hook for CODITECT

Validates new agents, skills, and commands against STANDARDS.md before creation.
Ensures all components meet quality standards and architectural requirements.

Event: PreToolUse
Matcher: tool_name: "Write"
Trigger: When creating .coditect/agents/*.md, .coditect/skills/*/SKILL.md, or .coditect/commands/*.md
"""

import json
import sys
import re
from pathlib import Path
from typing import Tuple


def validate_agent(content: str) -> Tuple[bool, str]:
    """Validate agent against STANDARDS.md"""

    # Check YAML frontmatter
    if not content.startswith('---'):
        return False, "Missing YAML frontmatter (must start with ---)"

    # Extract YAML section
    parts = content.split('---')
    if len(parts) < 3:
        return False, "Invalid YAML frontmatter structure (need opening and closing ---)"

    yaml_content = parts[1].strip()
    markdown_content = '---'.join(parts[2:]).strip()

    # Validate required fields in YAML
    required_fields = {
        'name': 'Agent name (kebab-case)',
        'description': 'Agent description (1-2 sentences)',
        'purpose': 'Agent purpose and capabilities',
        'tools': 'List of tools the agent has access to',
        'model': 'Claude model used (e.g., claude-opus, claude-sonnet)'
    }

    yaml_lines = yaml_content.split('\n')
    found_fields = {}

    for line in yaml_lines:
        if ':' in line:
            key = line.split(':')[0].strip()
            value = line.split(':', 1)[1].strip()
            found_fields[key] = value

    # Check all required fields exist
    missing_fields = []
    for field in required_fields.keys():
        if field not in found_fields:
            missing_fields.append(field)

    if missing_fields:
        return False, f"Missing required YAML fields: {', '.join(missing_fields)}"

    # Validate name format (kebab-case)
    name = found_fields.get('name', '')
    if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', name):
        return False, f"Agent name '{name}' must be kebab-case (lowercase with hyphens only)"

    # Validate description is not empty
    description = found_fields.get('description', '')
    if not description or description == '""':
        return False, "Description must be a non-empty string"

    # Validate description length (20-200 chars)
    desc_len = len(description.strip('"'))
    if desc_len < 20:
        return False, f"Description too short ({desc_len} chars, need at least 20)"
    if desc_len > 200:
        return False, f"Description too long ({desc_len} chars, keep to ~200)"

    # Validate content length (minimum 300 words)
    word_count = len(markdown_content.split())
    if word_count < 300:
        return False, f"Content too short ({word_count} words, need at least 300)"

    # Check for key sections
    required_sections = ['## Purpose', '## Capabilities', '## Usage']
    content_lower = markdown_content.lower()
    for section in required_sections:
        if section.lower() not in content_lower:
            return False, f"Missing required section: '{section}'"

    return True, "Agent validated successfully"


def validate_skill(content: str) -> Tuple[bool, str]:
    """Validate skill against STANDARDS.md"""

    # Check YAML frontmatter
    if not content.startswith('---'):
        return False, "Missing YAML frontmatter (must start with ---)"

    # Extract YAML section
    parts = content.split('---')
    if len(parts) < 3:
        return False, "Invalid YAML frontmatter structure"

    yaml_content = parts[1].strip()
    markdown_content = '---'.join(parts[2:]).strip()

    # Validate required fields
    required_fields = {
        'name': 'Skill name',
        'description': 'Skill description',
        'category': 'Skill category (e.g., development, analysis)',
        'reusability': 'Reusability score (1-10)'
    }

    yaml_lines = yaml_content.split('\n')
    found_fields = {}

    for line in yaml_lines:
        if ':' in line and not line.strip().startswith('-'):
            key = line.split(':')[0].strip()
            value = line.split(':', 1)[1].strip()
            found_fields[key] = value

    # Check all required fields
    missing_fields = [f for f in required_fields.keys() if f not in found_fields]
    if missing_fields:
        return False, f"Missing required YAML fields: {', '.join(missing_fields)}"

    # Validate name format
    name = found_fields.get('name', '')
    if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', name):
        return False, f"Skill name '{name}' must be kebab-case"

    # Validate reusability is numeric (1-10)
    reusability = found_fields.get('reusability', '')
    try:
        reusability_score = int(reusability)
        if not (1 <= reusability_score <= 10):
            return False, f"Reusability must be 1-10, got {reusability_score}"
    except (ValueError, TypeError):
        return False, f"Reusability must be a number 1-10, got '{reusability}'"

    # Validate content length
    word_count = len(markdown_content.split())
    if word_count < 200:
        return False, f"Content too short ({word_count} words, need at least 200)"

    return True, "Skill validated successfully"


def validate_command(content: str) -> Tuple[bool, str]:
    """Validate slash command against STANDARDS.md"""

    # Check YAML frontmatter
    if not content.startswith('---'):
        return False, "Missing YAML frontmatter (must start with ---)"

    # Extract YAML section
    parts = content.split('---')
    if len(parts) < 3:
        return False, "Invalid YAML frontmatter structure"

    yaml_content = parts[1].strip()
    markdown_content = '---'.join(parts[2:]).strip()

    # Validate required fields
    required_fields = {
        'name': 'Command name',
        'description': 'Command description',
        'agents': 'Agents this command uses'
    }

    yaml_lines = yaml_content.split('\n')
    found_fields = {}

    for line in yaml_lines:
        if ':' in line and not line.strip().startswith('-'):
            key = line.split(':')[0].strip()
            value = line.split(':', 1)[1].strip()
            found_fields[key] = value

    # Check required fields
    missing_fields = [f for f in required_fields.keys() if f not in found_fields]
    if missing_fields:
        return False, f"Missing required YAML fields: {', '.join(missing_fields)}"

    # Validate name starts with slash
    name = found_fields.get('name', '')
    if not name.startswith('/'):
        return False, f"Command name must start with / (got '{name}')"

    # Validate content exists
    if not markdown_content or len(markdown_content) < 100:
        return False, "Command documentation must have substantial content (100+ chars)"

    return True, "Command validated successfully"


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract file path and content from hook input
        file_path = hook_input.get('tool_input', {}).get('file_path', '')
        new_content = hook_input.get('tool_input', {}).get('new_string', '')

        if not file_path:
            # Can't validate without file path, allow
            print(json.dumps({"continue": True}))
            sys.exit(0)

        # Determine component type and validate
        is_valid = False
        message = ""

        if '/agents/' in file_path and file_path.endswith('.md'):
            is_valid, message = validate_agent(new_content)
        elif '/skills/' in file_path and file_path.endswith(('SKILL.md', '.md')):
            is_valid, message = validate_skill(new_content)
        elif '/commands/' in file_path and file_path.endswith('.md'):
            is_valid, message = validate_command(new_content)
        else:
            # Not a component file, allow
            print(json.dumps({"continue": True}))
            sys.exit(0)

        # Return validation result
        if is_valid:
            print(json.dumps({
                "continue": True,
                "suppressOutput": False
            }))
            sys.exit(0)
        else:
            print(json.dumps({
                "continue": False,
                "stopReason": f"Component validation failed: {message}"
            }))
            sys.exit(1)

    except json.JSONDecodeError as e:
        print(json.dumps({
            "continue": False,
            "stopReason": f"Hook error: Failed to parse JSON input: {e}"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "continue": False,
            "stopReason": f"Hook error: {type(e).__name__}: {e}"
        }))
        sys.exit(1)


if __name__ == '__main__':
    main()
