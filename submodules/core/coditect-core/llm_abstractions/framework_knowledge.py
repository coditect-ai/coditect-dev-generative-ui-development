"""
Framework Knowledge Loader

Loads framework component metadata and system prompt templates for LLM framework awareness.

Phase 2C: Framework Knowledge Registration System

This module provides the FrameworkKnowledgeLoader class which loads:
- Component registry (agents, skills, commands, scripts)
- Individual component metadata
- System prompt templates

The loader uses a singleton pattern for efficient knowledge loading across the framework.

Author: AZ1.AI INC.
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import json
from dataclasses import dataclass, field


@dataclass
class ComponentMetadata:
    """Metadata for a single framework component."""

    id: str
    name: str
    category: str
    description: str
    capabilities: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FrameworkRegistry:
    """Complete framework component registry."""

    framework_version: str
    last_updated: str
    agents: Dict[str, ComponentMetadata]
    skills: Dict[str, ComponentMetadata]
    commands: Dict[str, ComponentMetadata]
    scripts: Dict[str, ComponentMetadata]


class FrameworkKnowledgeLoader:
    """
    Loads framework component metadata and system prompt templates.

    Singleton pattern for efficient knowledge loading.

    Usage:
        knowledge = FrameworkKnowledgeLoader.get_instance()
        agent = knowledge.get_agent_metadata("ai-specialist")
        prompt = knowledge.get_system_prompt("framework-core")
        recommendations = knowledge.recommend_agent("analyze code architecture")
    """

    _instance: Optional['FrameworkKnowledgeLoader'] = None

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize knowledge loader.

        Args:
            config_dir: Optional path to .coditect/config directory
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = self._find_config_dir()

        self.registry: Optional[FrameworkRegistry] = None
        self.system_prompts: Dict[str, str] = {}

        # Load on initialization
        self._load_registry()
        self._load_system_prompts()

    @classmethod
    def get_instance(cls, config_dir: Optional[Path] = None) -> 'FrameworkKnowledgeLoader':
        """
        Get singleton instance.

        Args:
            config_dir: Optional path to config directory

        Returns:
            Singleton instance of FrameworkKnowledgeLoader
        """
        if cls._instance is None:
            cls._instance = cls(config_dir)
        return cls._instance

    def _find_config_dir(self) -> Path:
        """
        Find .coditect/config directory.

        Searches in multiple locations:
        1. .coditect/config (current directory)
        2. .claude/config (symlink)
        3. ../coditect-core/.coditect/config (parent submodule)

        Returns:
            Path to config directory
        """
        candidates = [
            Path(".coditect/config"),
            Path(".claude/config"),
            Path("../coditect-core/.coditect/config"),
            Path(__file__).parent.parent / ".coditect" / "config",
        ]

        for candidate in candidates:
            if candidate.exists() and (candidate / "framework-registry.json").exists():
                return candidate.resolve()

        # Default fallback
        return Path(".coditect/config")

    def _load_registry(self):
        """Load framework component registry from JSON."""
        registry_file = self.config_dir / "framework-registry.json"

        if not registry_file.exists():
            print(f"⚠️  Framework registry not found: {registry_file}")
            return

        try:
            with open(registry_file, 'r') as f:
                data = json.load(f)

            # Parse agents
            agents = {}
            for category, agent_list in data["components"]["agents"]["categories"].items():
                for agent in agent_list:
                    agents[agent["id"]] = ComponentMetadata(
                        id=agent["id"],
                        name=agent["name"],
                        category=agent.get("category", category),
                        description=agent["description"],
                        capabilities=agent.get("capabilities", []),
                        use_cases=agent.get("use_cases", []),
                        tags=agent.get("tags", []),
                        metadata=agent.get("metadata", {})
                    )

            # Parse skills
            skills = {}
            for skill in data["components"]["skills"]["list"]:
                skills[skill["id"]] = ComponentMetadata(
                    id=skill["id"],
                    name=skill["name"],
                    category="skill",
                    description=skill["description"],
                    capabilities=skill.get("provides", []),
                    use_cases=skill.get("use_cases", []),
                    tags=skill.get("tags", []),
                    metadata=skill.get("metadata", {})
                )

            # Parse commands
            commands = {}
            for category, command_list in data["components"]["commands"]["categories"].items():
                for command in command_list:
                    commands[command["id"]] = ComponentMetadata(
                        id=command["id"],
                        name=command["name"],
                        category=category,
                        description=command["description"],
                        capabilities=command.get("workflow", []),
                        use_cases=[command.get("example", "")],
                        tags=command.get("tags", []),
                        metadata={
                            "syntax": command.get("syntax", ""),
                            "agents_invoked": command.get("agents_invoked", []),
                            "typical_duration": command.get("typical_duration", "")
                        }
                    )

            # Parse scripts
            scripts = {}
            for script in data["components"]["scripts"]["list"]:
                scripts[script["id"]] = ComponentMetadata(
                    id=script["id"],
                    name=script["name"],
                    category="script",
                    description=script["description"],
                    capabilities=[],
                    use_cases=[script.get("usage", "")],
                    tags=script.get("tags", []),
                    metadata={
                        "path": script.get("path", ""),
                        "arguments": script.get("arguments", [])
                    }
                )

            self.registry = FrameworkRegistry(
                framework_version=data["framework_version"],
                last_updated=data["last_updated"],
                agents=agents,
                skills=skills,
                commands=commands,
                scripts=scripts
            )

            print(f"✅ Framework registry loaded: {len(agents)} agents, {len(skills)} skills, {len(commands)} commands, {len(scripts)} scripts")

        except Exception as e:
            print(f"⚠️  Error loading framework registry: {e}")
            import traceback
            traceback.print_exc()

    def _load_system_prompts(self):
        """Load system prompt templates."""
        prompt_dir = self.config_dir / "system-prompts"

        if not prompt_dir.exists():
            # No prompts yet, will be created in Phase 4
            return

        try:
            for prompt_file in prompt_dir.glob("*.txt"):
                prompt_name = prompt_file.stem
                with open(prompt_file, 'r') as f:
                    self.system_prompts[prompt_name] = f.read()

            if self.system_prompts:
                print(f"✅ Loaded {len(self.system_prompts)} system prompt templates")

        except Exception as e:
            print(f"⚠️  Error loading system prompts: {e}")

    def get_agent_metadata(self, agent_id: str) -> Optional[ComponentMetadata]:
        """
        Get metadata for specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Component metadata or None if not found
        """
        if not self.registry:
            return None
        return self.registry.agents.get(agent_id)

    def get_skill_metadata(self, skill_id: str) -> Optional[ComponentMetadata]:
        """
        Get metadata for specific skill.

        Args:
            skill_id: Skill identifier

        Returns:
            Component metadata or None if not found
        """
        if not self.registry:
            return None
        return self.registry.skills.get(skill_id)

    def get_command_metadata(self, command_id: str) -> Optional[ComponentMetadata]:
        """
        Get metadata for specific command.

        Args:
            command_id: Command identifier

        Returns:
            Component metadata or None if not found
        """
        if not self.registry:
            return None
        return self.registry.commands.get(command_id)

    def get_system_prompt(self, prompt_type: str = "framework-core") -> str:
        """
        Get system prompt template.

        Args:
            prompt_type: Type of prompt template

        Returns:
            System prompt string or empty string if not found
        """
        return self.system_prompts.get(prompt_type, "")

    def get_component_summary(self, component_type: str = "all") -> str:
        """
        Get summary of framework components for injection into LLM context.

        Args:
            component_type: "agents", "skills", "commands", "scripts", or "all"

        Returns:
            Formatted summary string
        """
        if not self.registry:
            return ""

        summary_parts = []

        if component_type in ["agents", "all"]:
            agent_count = len(self.registry.agents)
            summary_parts.append(f"**{agent_count} Specialized Agents** available")

        if component_type in ["skills", "all"]:
            skill_count = len(self.registry.skills)
            summary_parts.append(f"**{skill_count} Production Skills** available")

        if component_type in ["commands", "all"]:
            command_count = len(self.registry.commands)
            summary_parts.append(f"**{command_count} Slash Commands** available")

        if component_type in ["scripts", "all"]:
            script_count = len(self.registry.scripts)
            summary_parts.append(f"**{script_count} Automation Scripts** available")

        return ", ".join(summary_parts)

    def recommend_agent(self, task_description: str, category: Optional[str] = None, limit: int = 5) -> List[str]:
        """
        Recommend agents for a given task.

        Simple keyword matching (Phase 2C).
        Future: Use embeddings for semantic search (Phase 3).

        Args:
            task_description: Description of the task
            category: Optional category filter
            limit: Maximum number of recommendations

        Returns:
            List of recommended agent IDs (sorted by relevance)
        """
        if not self.registry:
            return []

        keywords = task_description.lower().split()
        recommendations = []

        for agent_id, agent in self.registry.agents.items():
            # Filter by category if specified
            if category and agent.category != category:
                continue

            # Keyword matching in description, capabilities, use_cases
            text_parts = [agent.description]
            text_parts.extend(agent.capabilities)
            text_parts.extend(agent.use_cases)
            text_parts.extend(agent.tags)

            text = " ".join(text_parts).lower()

            score = sum(1 for keyword in keywords if keyword in text)

            if score > 0:
                recommendations.append((agent_id, score))

        # Sort by score descending
        recommendations.sort(key=lambda x: x[1], reverse=True)

        return [agent_id for agent_id, _ in recommendations[:limit]]

    def get_all_agents(self) -> List[ComponentMetadata]:
        """Get list of all agents."""
        if not self.registry:
            return []
        return list(self.registry.agents.values())

    def get_all_skills(self) -> List[ComponentMetadata]:
        """Get list of all skills."""
        if not self.registry:
            return []
        return list(self.registry.skills.values())

    def get_all_commands(self) -> List[ComponentMetadata]:
        """Get list of all commands."""
        if not self.registry:
            return []
        return list(self.registry.commands.values())

    def get_agents_by_category(self, category: str) -> List[ComponentMetadata]:
        """Get agents filtered by category."""
        if not self.registry:
            return []
        return [agent for agent in self.registry.agents.values() if agent.category == category]


# Convenience function
def get_framework_knowledge() -> FrameworkKnowledgeLoader:
    """
    Get framework knowledge loader instance.

    Returns:
        Singleton instance of FrameworkKnowledgeLoader
    """
    return FrameworkKnowledgeLoader.get_instance()
