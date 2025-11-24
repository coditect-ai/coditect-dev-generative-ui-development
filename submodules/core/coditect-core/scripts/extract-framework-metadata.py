#!/usr/bin/env python3
"""
Framework Metadata Extraction Script

Extracts metadata from all CODITECT components (agents, skills, commands, scripts)
and generates the framework-registry.json file for LLM framework awareness.

Phase 2C: Framework Knowledge Registration System

Usage:
    python3 scripts/extract-framework-metadata.py

Output:
    - .coditect/config/framework-registry.json
    - .coditect/config/agents/ (individual agent metadata files)
    - .coditect/config/skills/ (individual skill metadata files)
    - .coditect/config/commands/ (individual command metadata files)
    - .coditect/config/scripts/ (individual script metadata files)

Author: AZ1.AI INC.
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


def parse_simple_yaml(yaml_str: str) -> Dict[str, Any]:
    """Simple YAML parser for basic key-value pairs and lists."""
    result = {}
    current_key = None
    current_list = []

    for line in yaml_str.split('\n'):
        line = line.rstrip()

        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue

        # List item
        if line.strip().startswith('-') and current_key:
            item = line.strip()[1:].strip()
            current_list.append(item)
            continue

        # Key-value pair
        if ':' in line and not line.startswith(' '):
            # Save previous list if exists
            if current_key and current_list:
                result[current_key] = current_list
                current_list = []

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Check if this is a list key
            if not value:
                current_key = key
                continue

            # Handle different value types
            if value.lower() in ('true', 'false'):
                result[key] = value.lower() == 'true'
            elif value.startswith('[') and value.endswith(']'):
                # Simple list parsing
                result[key] = [v.strip().strip('"').strip("'") for v in value[1:-1].split(',') if v.strip()]
            else:
                # String value
                result[key] = value.strip('"').strip("'")
        elif current_key and line.startswith('  '):
            # Nested item (treat as part of current context)
            continue

    # Save final list if exists
    if current_key and current_list:
        result[current_key] = current_list

    return result


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    try:
        metadata = parse_simple_yaml(parts[1])
        body = parts[2].strip()
        return metadata or {}, body
    except Exception as e:
        print(f"⚠️  YAML parsing error: {e}")
        return {}, content


def extract_agent_metadata(agent_file: Path) -> Dict[str, Any]:
    """
    Extract metadata from an agent markdown file.

    Agent files have YAML frontmatter with:
    - name: Agent ID
    - description: One-line description
    - tools: List of available tools
    - model: LLM model to use
    """
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            file_content = f.read()

        metadata, content = parse_frontmatter(file_content)

        # Extract capabilities from content (first section after frontmatter)
        capabilities = []
        use_cases = []

        # Find "Core Responsibilities" or similar section
        responsibilities_match = re.search(
            r'## Core Responsibilities\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )
        if responsibilities_match:
            resp_text = responsibilities_match.group(1)
            # Extract numbered or bulleted items
            capabilities = re.findall(r'(?:###|\*|-)\s*\*\*(.+?)\*\*', resp_text)

        # Find usage examples
        examples_match = re.search(
            r'## Usage Examples?\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )
        if examples_match:
            examples_text = examples_match.group(1)
            # Extract usage patterns
            use_cases = re.findall(r'```[^\n]*\n(.+?)\n```', examples_text, re.DOTALL)
            use_cases = [uc.strip() for uc in use_cases if 'Use' in uc or 'Task(' in uc]

        # Determine category from context awareness DNA
        category = "general"
        if 'context_awareness' in metadata:
            keywords = metadata['context_awareness'].get('auto_scope_keywords', {})
            if keywords:
                # Use first category as primary
                category = list(keywords.keys())[0] if keywords else "general"

        # Extract typical invocation
        typical_invocation = f'Task(subagent_type="general-purpose", prompt="Use {metadata.get("name", "")} subagent to <task>")'
        if use_cases:
            # Use first use case as example
            typical_invocation = use_cases[0][:200] if len(use_cases[0]) < 200 else use_cases[0][:197] + "..."

        # Extract tags
        tags = []
        if 'context_awareness' in metadata:
            confidence_boosters = metadata['context_awareness'].get('confidence_boosters', [])
            for booster in confidence_boosters:
                if isinstance(booster, str):
                    # Extract words from confidence boosters
                    words = re.findall(r'\w+', booster.lower())
                    tags.extend(words[:3])  # Take first 3 words

        tags = list(set(tags))[:5]  # Deduplicate and limit to 5 tags

        return {
            "id": metadata.get("name", agent_file.stem),
            "name": metadata.get("name", agent_file.stem).replace('-', ' ').title(),
            "category": category,
            "description": metadata.get("description", ""),
            "capabilities": capabilities[:5],  # Limit to top 5
            "use_cases": use_cases[:3],  # Limit to top 3
            "typical_invocation": typical_invocation,
            "llm_binding": {
                "provider": "anthropic-claude",
                "model": metadata.get("model", "sonnet"),
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "tools": metadata.get("tools", []),
            "tags": tags,
            "metadata": {
                "automation_features": metadata.get("automation_features", {}),
                "progress_checkpoints": metadata.get("progress_checkpoints", {}),
            }
        }
    except Exception as e:
        print(f"⚠️  Error extracting agent metadata from {agent_file}: {e}")
        return None


def extract_skill_metadata(skill_dir: Path) -> Dict[str, Any]:
    """
    Extract metadata from a skill directory.

    Skill directories contain:
    - SKILL.md: Main skill documentation with frontmatter
    - core/: Implementation files
    - templates/: Reusable templates
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None

    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            file_content = f.read()

        metadata, content = parse_frontmatter(file_content)

        # Extract what the skill provides
        provides = []
        when_to_use_match = re.search(
            r'## When to Use\s*\n.*?✅.*?when:.*?\n(.*?)(?=\n##|❌)',
            content,
            re.DOTALL
        )
        if when_to_use_match:
            provides_text = when_to_use_match.group(1)
            provides = re.findall(r'(?:-|\*)\s*(.+?)(?:\n|$)', provides_text)
            provides = [p.strip() for p in provides if p.strip()][:5]

        # Extract use cases
        use_cases = []
        if provides:
            use_cases = provides[:3]  # Use top 3 as use cases

        # Extract tags from metadata
        tags = []
        if 'metadata' in metadata:
            tech_stack = metadata['metadata'].get('tech-stack', '')
            if tech_stack:
                tags = [t.strip() for t in tech_stack.split(',')][:5]

        return {
            "id": metadata.get("name", skill_dir.name),
            "name": metadata.get("name", skill_dir.name).replace('-', ' ').title(),
            "description": metadata.get("description", ""),
            "provides": provides,
            "use_cases": use_cases,
            "activation": f'Skill(skill="{metadata.get("name", skill_dir.name)}")',
            "tags": tags,
            "metadata": {
                "license": metadata.get("license", "MIT"),
                "allowed_tools": metadata.get("allowed-tools", []),
                "token_efficiency": metadata.get("metadata", {}).get("token-efficiency", ""),
                "integration": metadata.get("metadata", {}).get("integration", ""),
            }
        }
    except Exception as e:
        print(f"⚠️  Error extracting skill metadata from {skill_dir}: {e}")
        return None


def extract_command_metadata(command_file: Path) -> Dict[str, Any]:
    """
    Extract metadata from a command markdown file.

    Command files describe slash commands with:
    - Title/description
    - Steps to follow
    - Success criteria
    - Usage examples
    """
    try:
        with open(command_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title/description (first heading)
        title_match = re.search(r'^# (.+?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else command_file.stem

        # Extract description (first paragraph after title)
        desc_match = re.search(
            r'^# .+?\n\n(.+?)(?:\n\n|\n##)',
            content,
            re.DOTALL | re.MULTILINE
        )
        description = desc_match.group(1).strip() if desc_match else ""
        description = description.replace('\n', ' ')[:200]

        # Extract workflow steps
        workflow = []
        steps_matches = re.findall(r'### Step \d+: (.+?)$', content, re.MULTILINE)
        workflow = steps_matches[:5]  # Limit to 5 steps

        # Extract agents invoked
        agents_invoked = []
        task_matches = re.findall(r'Use (\w+-?\w+-?\w*) subagent', content)
        agents_invoked = list(set(task_matches))[:5]

        # Generate syntax
        command_name = f"/{command_file.stem}"
        syntax = f'{command_name} "<description>"'

        # Extract example
        example_match = re.search(r'```(?:bash)?\n(/\w+.+?)$', content, re.MULTILINE)
        example = example_match.group(1) if example_match else syntax

        # Extract tags from filename and content
        tags = []
        if 'project' in command_file.stem or 'new' in command_file.stem:
            tags.append('project-creation')
        if 'deploy' in command_file.stem or 'build' in command_file.stem:
            tags.append('deployment')
        if 'analyze' in command_file.stem or 'research' in command_file.stem:
            tags.append('analysis')
        if 'hook' in command_file.stem:
            tags.append('automation')

        tags.append('workflow')

        return {
            "id": command_file.stem,
            "name": command_name,
            "description": description,
            "syntax": syntax,
            "workflow": workflow,
            "example": example,
            "typical_duration": "5-10 minutes",  # Default
            "agents_invoked": agents_invoked,
            "tags": tags[:5]
        }
    except Exception as e:
        print(f"⚠️  Error extracting command metadata from {command_file}: {e}")
        return None


def extract_script_metadata(script_file: Path) -> Dict[str, Any]:
    """
    Extract metadata from a Python script file.

    Scripts have docstrings with:
    - Description
    - Usage
    - Author/copyright
    """
    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract module docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        docstring = docstring_match.group(1).strip() if docstring_match else ""

        # Extract description (first paragraph)
        desc_lines = []
        for line in docstring.split('\n'):
            line = line.strip()
            if not line or line.startswith('Usage:') or line.startswith('Author:'):
                break
            desc_lines.append(line)

        description = ' '.join(desc_lines)[:200]

        # Extract usage
        usage_match = re.search(r'Usage:\s*\n\s*(.+?)$', docstring, re.MULTILINE)
        usage = usage_match.group(1).strip() if usage_match else f"python3 scripts/{script_file.name}"

        # Extract arguments from usage
        arguments = []
        arg_matches = re.findall(r'(?:"<(.+?)>"|--(\w+))', usage)
        for arg_match in arg_matches:
            if arg_match[0]:  # Positional argument
                arguments.append({
                    "name": arg_match[0],
                    "required": True,
                    "type": "string"
                })
            elif arg_match[1]:  # Flag argument
                arguments.append({
                    "name": f"--{arg_match[1]}",
                    "required": False,
                    "type": "flag"
                })

        # Extract tags from script purpose
        tags = []
        if 'checkpoint' in script_file.stem or 'memory' in description.lower():
            tags.append('memory')
        if 'git' in script_file.stem or 'commit' in description.lower():
            tags.append('git')
        if 'submodule' in script_file.stem:
            tags.append('submodule')
        if 'setup' in script_file.stem or 'bootstrap' in script_file.stem:
            tags.append('setup')

        tags.append('automation')

        return {
            "id": script_file.stem,
            "name": script_file.name,
            "path": f"scripts/{script_file.name}",
            "description": description,
            "usage": usage,
            "arguments": arguments,
            "output": "See script documentation",
            "tags": tags[:5]
        }
    except Exception as e:
        print(f"⚠️  Error extracting script metadata from {script_file}: {e}")
        return None


def main():
    """Main extraction workflow."""
    print("🔍 Framework Metadata Extraction - Phase 2C")
    print("=" * 60)

    # Find project root
    project_root = Path(__file__).parent.parent

    # Create output directories
    config_dir = project_root / ".coditect" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    (config_dir / "agents").mkdir(exist_ok=True)
    (config_dir / "skills").mkdir(exist_ok=True)
    (config_dir / "commands").mkdir(exist_ok=True)
    (config_dir / "scripts").mkdir(exist_ok=True)

    # Extract agent metadata
    print("\n📋 Extracting agent metadata...")
    agents_dir = project_root / "agents"
    agent_files = list(agents_dir.glob("*.md"))

    agents_by_category = {}
    for agent_file in agent_files:
        agent_metadata = extract_agent_metadata(agent_file)
        if agent_metadata:
            category = agent_metadata.get("category", "general")
            if category not in agents_by_category:
                agents_by_category[category] = []
            agents_by_category[category].append(agent_metadata)

            # Write individual agent metadata file
            agent_json_file = config_dir / "agents" / f"{agent_metadata['id']}.json"
            with open(agent_json_file, 'w') as f:
                json.dump(agent_metadata, f, indent=2)

    print(f"   ✅ Extracted {len(agent_files)} agents across {len(agents_by_category)} categories")

    # Extract skill metadata
    print("\n📋 Extracting skill metadata...")
    skills_dir = project_root / "skills"
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]

    skills = []
    for skill_dir in skill_dirs:
        skill_metadata = extract_skill_metadata(skill_dir)
        if skill_metadata:
            skills.append(skill_metadata)

            # Write individual skill metadata file
            skill_json_file = config_dir / "skills" / f"{skill_metadata['id']}.json"
            with open(skill_json_file, 'w') as f:
                json.dump(skill_metadata, f, indent=2)

    print(f"   ✅ Extracted {len(skills)} skills")

    # Extract command metadata
    print("\n📋 Extracting command metadata...")
    commands_dir = project_root / "commands"
    command_files = list(commands_dir.glob("*.md"))

    commands_by_category = {
        "project_creation": [],
        "development": [],
        "analysis": [],
        "deployment": [],
        "other": []
    }

    for command_file in command_files:
        command_metadata = extract_command_metadata(command_file)
        if command_metadata:
            # Categorize command
            tags = command_metadata.get("tags", [])
            if "project-creation" in tags:
                category = "project_creation"
            elif "deployment" in tags:
                category = "deployment"
            elif "analysis" in tags:
                category = "analysis"
            elif any(tag in tags for tag in ["development", "implement", "code"]):
                category = "development"
            else:
                category = "other"

            commands_by_category[category].append(command_metadata)

            # Write individual command metadata file
            command_json_file = config_dir / "commands" / f"{command_metadata['id']}.json"
            with open(command_json_file, 'w') as f:
                json.dump(command_metadata, f, indent=2)

    print(f"   ✅ Extracted {len(command_files)} commands across {len(commands_by_category)} categories")

    # Extract script metadata
    print("\n📋 Extracting script metadata...")
    scripts_dir = project_root / "scripts"
    script_files = list(scripts_dir.glob("*.py"))

    scripts = []
    for script_file in script_files:
        script_metadata = extract_script_metadata(script_file)
        if script_metadata:
            scripts.append(script_metadata)

            # Write individual script metadata file
            script_json_file = config_dir / "scripts" / f"{script_metadata['id']}.json"
            with open(script_json_file, 'w') as f:
                json.dump(script_metadata, f, indent=2)

    print(f"   ✅ Extracted {len(scripts)} scripts")

    # Create framework registry
    print("\n📦 Creating framework registry...")

    registry = {
        "framework_version": "1.0.0",
        "last_updated": datetime.now().isoformat(),
        "components": {
            "agents": {
                "total": len(agent_files),
                "categories": agents_by_category
            },
            "skills": {
                "total": len(skills),
                "list": skills
            },
            "commands": {
                "total": len(command_files),
                "categories": commands_by_category
            },
            "scripts": {
                "total": len(scripts),
                "list": scripts
            }
        }
    }

    registry_file = config_dir / "framework-registry.json"
    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)

    print(f"   ✅ Framework registry created: {registry_file}")

    # Summary
    print("\n" + "=" * 60)
    print("✅ Metadata Extraction Complete!")
    print(f"   📊 Total components: {len(agent_files) + len(skills) + len(command_files) + len(scripts)}")
    print(f"   👤 Agents: {len(agent_files)}")
    print(f"   🎯 Skills: {len(skills)}")
    print(f"   ⚡ Commands: {len(command_files)}")
    print(f"   🔧 Scripts: {len(scripts)}")
    print(f"\n   📁 Output: {config_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
