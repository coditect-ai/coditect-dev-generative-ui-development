"""
System Prompt Builder

Builds context-aware system prompts with framework knowledge for LLMs.

Phase 2C: Framework Knowledge Registration System

This module provides the SystemPromptBuilder class which:
- Builds framework-aware system prompts
- Injects component knowledge (agents, skills, commands, scripts)
- Creates task-specific prompts with custom context
- Generates agent invocation prompts with examples

Author: AZ1.AI INC.
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.
"""

from typing import Dict, List, Optional
from .framework_knowledge import FrameworkKnowledgeLoader, ComponentMetadata


class SystemPromptBuilder:
    """
    Builds context-aware system prompts with framework knowledge.

    Usage:
        builder = SystemPromptBuilder()
        prompt = builder.build_prompt(
            task_type="code-generation",
            include_agents=True,
            include_skills=True
        )

        # Or build agent-specific prompt
        agent_prompt = builder.build_agent_invocation_prompt("ai-specialist")
    """

    def __init__(self, knowledge_loader: Optional[FrameworkKnowledgeLoader] = None):
        """
        Initialize prompt builder.

        Args:
            knowledge_loader: Optional knowledge loader instance (uses singleton if not provided)
        """
        self.knowledge = knowledge_loader or FrameworkKnowledgeLoader.get_instance()

    def build_prompt(
        self,
        task_type: str = "general",
        include_agents: bool = True,
        include_skills: bool = True,
        include_commands: bool = True,
        include_scripts: bool = False,
        custom_context: Optional[str] = None,
        agent_recommendations: Optional[List[str]] = None
    ) -> str:
        """
        Build system prompt with framework knowledge.

        Args:
            task_type: Type of task (general, code-generation, research, architecture, etc.)
            include_agents: Include agent catalog
            include_skills: Include skill library
            include_commands: Include command reference
            include_scripts: Include script inventory
            custom_context: Additional custom context
            agent_recommendations: Optional list of recommended agent IDs to highlight

        Returns:
            Complete system prompt string
        """
        prompt_parts = []

        # Core framework prompt (if available)
        core_prompt = self.knowledge.get_system_prompt("framework-core")
        if core_prompt:
            prompt_parts.append(core_prompt)
        else:
            # Fallback: Generate basic framework prompt
            prompt_parts.append(self._build_basic_framework_prompt())

        # Task-specific prompt (if available)
        task_prompt = self.knowledge.get_system_prompt(f"task-{task_type}")
        if task_prompt:
            prompt_parts.append(task_prompt)

        # Component summaries
        if include_agents or include_skills or include_commands or include_scripts:
            summary = self.knowledge.get_component_summary("all")
            if summary:
                prompt_parts.append(f"\n## Framework Components Available\n\n{summary}")

        # Agent recommendations (if provided)
        if agent_recommendations:
            rec_section = self._build_recommendations_section(agent_recommendations)
            prompt_parts.append(rec_section)

        # Custom context
        if custom_context:
            prompt_parts.append(f"\n## Additional Context\n\n{custom_context}")

        return "\n\n".join(prompt_parts)

    def _build_basic_framework_prompt(self) -> str:
        """Build basic framework prompt when no template exists."""
        agents = self.knowledge.get_all_agents()
        skills = self.knowledge.get_all_skills()
        commands = self.knowledge.get_all_commands()

        prompt = """You are working within the AZ1.AI CODITECT framework - a comprehensive project management and development platform with specialized components.

## Available Resources

"""

        # Add agent summary
        if agents:
            prompt += f"**{len(agents)} Specialized Agents** for:\n"
            agent_categories = {}
            for agent in agents:
                cat = agent.category
                if cat not in agent_categories:
                    agent_categories[cat] = []
                agent_categories[cat].append(agent.name)

            for category, agent_names in sorted(agent_categories.items())[:5]:
                prompt += f"- {category}: {', '.join(agent_names[:3])}\n"

        # Add skill summary
        if skills:
            prompt += f"\n**{len(skills)} Production Skills** including:\n"
            for skill in skills[:5]:
                prompt += f"- {skill.name}\n"

        # Add command summary
        if commands:
            prompt += f"\n**{len(commands)} Slash Commands** for various workflows\n"

        prompt += """
## Agent Invocation Pattern

**CRITICAL**: Use the Task tool to invoke specialized agents:

```python
# Correct invocation
Task(subagent_type="general-purpose", prompt="Use <agent-name> subagent to <task>")
```

## Framework Context

Current directory has CODITECT framework accessible via:
- `.coditect/` - Master framework directory
- `.claude/` - Symlink to .coditect for Claude Code compatibility

Use this framework knowledge to provide optimal recommendations and workflows.
"""

        return prompt

    def _build_recommendations_section(self, agent_ids: List[str]) -> str:
        """Build section with recommended agents for current task."""
        section = "\n## Recommended Agents for This Task\n\n"

        for agent_id in agent_ids:
            agent = self.knowledge.get_agent_metadata(agent_id)
            if agent:
                section += f"**{agent.name}** (`{agent_id}`):\n"
                section += f"  {agent.description}\n\n"

        return section

    def build_agent_invocation_prompt(self, agent_id: str) -> str:
        """
        Build prompt for invoking a specific agent.

        Includes agent metadata (capabilities, use cases, typical invocation).

        Args:
            agent_id: Agent identifier

        Returns:
            Agent invocation prompt or error message if agent not found
        """
        agent_metadata = self.knowledge.get_agent_metadata(agent_id)

        if not agent_metadata:
            return f"Agent '{agent_id}' not found in framework registry."

        # Build capabilities section
        capabilities_text = ""
        if agent_metadata.capabilities:
            capabilities_text = "\n**Capabilities:**\n"
            for cap in agent_metadata.capabilities[:5]:
                capabilities_text += f"- {cap}\n"

        # Build use cases section
        use_cases_text = ""
        if agent_metadata.use_cases:
            use_cases_text = "\n**Typical Use Cases:**\n"
            for uc in agent_metadata.use_cases[:3]:
                use_cases_text += f"- {uc}\n"

        # Build invocation example
        typical_invocation = agent_metadata.metadata.get('typical_invocation',
            f'Task(subagent_type="general-purpose", prompt="Use {agent_id} subagent to <task>")')

        prompt = f"""## Agent: {agent_metadata.name}

**Description:** {agent_metadata.description}
{capabilities_text}{use_cases_text}
**Invocation Pattern:**
```python
{typical_invocation}
```
"""
        return prompt

    def build_task_prompt_with_recommendations(self, task_description: str, limit: int = 3) -> str:
        """
        Build prompt for a task with automatic agent recommendations.

        Args:
            task_description: Description of the task
            limit: Maximum number of recommendations

        Returns:
            Complete prompt with task description and recommendations
        """
        # Get agent recommendations
        recommendations = self.knowledge.recommend_agent(task_description, limit=limit)

        # Build prompt with recommendations
        prompt = self.build_prompt(
            task_type="general",
            include_agents=True,
            include_skills=True,
            include_commands=True,
            custom_context=f"**Current Task:** {task_description}",
            agent_recommendations=recommendations
        )

        return prompt

    def build_skill_activation_prompt(self, skill_id: str) -> str:
        """
        Build prompt for activating a specific skill.

        Args:
            skill_id: Skill identifier

        Returns:
            Skill activation prompt or error message if skill not found
        """
        skill_metadata = self.knowledge.get_skill_metadata(skill_id)

        if not skill_metadata:
            return f"Skill '{skill_id}' not found in framework registry."

        # Build capabilities section
        capabilities_text = ""
        if skill_metadata.capabilities:
            capabilities_text = "\n**Provides:**\n"
            for cap in skill_metadata.capabilities[:5]:
                capabilities_text += f"- {cap}\n"

        # Build use cases section
        use_cases_text = ""
        if skill_metadata.use_cases:
            use_cases_text = "\n**Use Cases:**\n"
            for uc in skill_metadata.use_cases[:3]:
                use_cases_text += f"- {uc}\n"

        # Get activation syntax
        activation = f'Skill(skill="{skill_id}")'

        prompt = f"""## Skill: {skill_metadata.name}

**Description:** {skill_metadata.description}
{capabilities_text}{use_cases_text}
**Activation:**
```python
{activation}
```
"""
        return prompt

    def build_command_help_prompt(self, command_id: str) -> str:
        """
        Build help prompt for a specific command.

        Args:
            command_id: Command identifier

        Returns:
            Command help prompt or error message if command not found
        """
        command_metadata = self.knowledge.get_command_metadata(command_id)

        if not command_metadata:
            return f"Command '{command_id}' not found in framework registry."

        # Build workflow section
        workflow_text = ""
        if command_metadata.capabilities:  # Capabilities holds workflow steps
            workflow_text = "\n**Workflow:**\n"
            for i, step in enumerate(command_metadata.capabilities[:5], 1):
                workflow_text += f"{i}. {step}\n"

        # Build agents section
        agents_text = ""
        agents_invoked = command_metadata.metadata.get('agents_invoked', [])
        if agents_invoked:
            agents_text = f"\n**Agents Invoked:** {', '.join(agents_invoked)}\n"

        # Get syntax
        syntax = command_metadata.metadata.get('syntax', f'/{command_id}')

        # Get example
        example = command_metadata.use_cases[0] if command_metadata.use_cases else syntax

        prompt = f"""## Command: {command_metadata.name}

**Description:** {command_metadata.description}
{workflow_text}{agents_text}
**Syntax:**
```
{syntax}
```

**Example:**
```
{example}
```
"""
        return prompt
