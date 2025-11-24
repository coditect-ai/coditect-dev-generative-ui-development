"""
Slash Command Router

Routes slash commands to appropriate agents via LLM bindings.
Enables programmatic command execution with structured results.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

from .task import AgentTask, TaskStatus
from .executor import TaskExecutor
from .agent_registry import AgentRegistry
from .command_result import (
    CommandResult,
    CommandStatus,
    CommandSpec,
    COMMAND_REGISTRY,
)


class CommandParser:
    """Parses slash commands into structured format."""

    @staticmethod
    def parse(command_str: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parse command string into command name and arguments.

        Examples:
            "/analyze" → ("/analyze", {})
            "/analyze target=src/main.rs" → ("/analyze", {"target": "src/main.rs"})
            "/implement description='Add auth'" → ("/implement", {"description": "Add auth"})

        Args:
            command_str: Raw command string

        Returns:
            (command_name, arguments_dict)
        """
        # Split command and args
        parts = command_str.strip().split(maxsplit=1)
        command = parts[0]

        if len(parts) == 1:
            return command, {}

        # Parse arguments
        args_str = parts[1]
        args = {}

        # Match key=value or key='value' or key="value"
        pattern = r'(\w+)=(["\']?)([^"\']*?)\2(?:\s|$)'
        matches = re.findall(pattern, args_str)

        for key, _, value in matches:
            args[key] = value

        # If no key=value pairs found, treat entire string as description
        if not args:
            args = {"description": args_str}

        return command, args


class SlashCommandRouter:
    """
    Routes slash commands to agents via LLM bindings.

    Provides programmatic command execution with structured results,
    enabling API access, automation, and external system integration.

    Example:
        >>> router = SlashCommandRouter()
        >>> result = await router.execute("/analyze target=src/main.rs")
        >>> print(result.status)  # CommandStatus.SUCCESS
        >>> print(result.agent_used)  # "code-reviewer"
    """

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        executor: Optional[TaskExecutor] = None,
    ):
        """
        Initialize command router.

        Args:
            registry: Optional AgentRegistry instance
            executor: Optional TaskExecutor instance
        """
        self.registry = registry or AgentRegistry()
        self.executor = executor or TaskExecutor(registry=self.registry)
        self.parser = CommandParser()

        # Command registry
        self.commands = COMMAND_REGISTRY

    def list_commands(self, category: Optional[str] = None) -> List[CommandSpec]:
        """
        List all available commands.

        Args:
            category: Optional filter by category

        Returns:
            List of command specifications
        """
        commands = list(self.commands.values())

        if category:
            commands = [cmd for cmd in commands if cmd.category == category]

        return commands

    def get_command_spec(self, command: str) -> Optional[CommandSpec]:
        """
        Get specification for a command.

        Args:
            command: Command name (e.g., "/analyze")

        Returns:
            CommandSpec if found, None otherwise
        """
        return self.commands.get(command)

    def get_command_help(self, command: str) -> str:
        """
        Get help text for a command.

        Args:
            command: Command name

        Returns:
            Formatted help text
        """
        spec = self.get_command_spec(command)

        if not spec:
            return f"Unknown command: {command}"

        help_text = f"""
**{spec.name}** - {spec.description}

**Agent:** {spec.agent_id}
**Category:** {spec.category or 'general'}

**Required Arguments:**
{chr(10).join(f'  - {arg}' for arg in spec.required_args) if spec.required_args else '  (none)'}

**Optional Arguments:**
{chr(10).join(f'  - {arg}' for arg in spec.optional_args) if spec.optional_args else '  (none)'}

**Examples:**
{chr(10).join(f'  {ex}' for ex in spec.examples)}
"""
        return help_text.strip()

    async def execute(
        self,
        command_str: str,
        args: Optional[Dict[str, Any]] = None,
    ) -> CommandResult:
        """
        Execute a slash command.

        Args:
            command_str: Command string (e.g., "/analyze target=src/main.rs")
            args: Optional arguments dict (overrides parsed args)

        Returns:
            CommandResult with structured execution data

        Example:
            >>> result = await router.execute("/analyze target=main.rs")
            >>> print(result.status)  # CommandStatus.SUCCESS
            >>> print(result.output)  # Analysis output
            >>> print(result.agent_used)  # "code-reviewer"
        """
        started_at = datetime.now()

        # Parse command
        command, parsed_args = self.parser.parse(command_str)

        # Merge args (explicit args override parsed)
        final_args = {**parsed_args, **(args or {})}

        # Get command specification
        spec = self.get_command_spec(command)

        if not spec:
            return CommandResult(
                command=command,
                status=CommandStatus.FAILED,
                output="",
                error_message=f"Unknown command: {command}",
                error_type="UnknownCommand",
                started_at=started_at,
                completed_at=datetime.now(),
            )

        # Validate arguments
        is_valid, error_msg = spec.validate_args(final_args)

        if not is_valid:
            return CommandResult(
                command=command,
                status=CommandStatus.FAILED,
                output="",
                error_message=error_msg,
                error_type="InvalidArguments",
                started_at=started_at,
                completed_at=datetime.now(),
            )

        # Build task description
        task_description = self._build_task_description(spec, final_args)

        # Create task
        task = AgentTask(
            task_id=f"CMD-{command.lstrip('/')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            title=f"Execute {command}",
            description=task_description,
            agent=spec.agent_id,
            status=TaskStatus.PENDING,
            metadata={
                "command": command,
                "args": final_args,
                "task_type": spec.task_type,
                "streaming_enabled": spec.streaming_enabled,
            },
        )

        # Register task
        self.registry.register_task(task)

        try:
            # Execute via TaskExecutor
            exec_result = await self.executor.execute_async(task.task_id)

            # Calculate execution time
            completed_at = datetime.now()
            execution_time = (completed_at - started_at).total_seconds()

            # Extract LLM metadata
            llm_provider = exec_result.metadata.get("provider")
            llm_model = exec_result.metadata.get("model")
            tokens_used = exec_result.metadata.get("tokens_used")
            estimated_cost = exec_result.metadata.get("estimated_cost")

            # Map execution status to command status
            if exec_result.status.value == "success":
                cmd_status = CommandStatus.SUCCESS
            elif exec_result.status.value == "failed":
                cmd_status = CommandStatus.FAILED
            else:
                cmd_status = CommandStatus.PARTIAL

            # Build command result
            result = CommandResult(
                command=command,
                status=cmd_status,
                output=exec_result.output or "",
                agent_used=spec.agent_id,
                llm_provider=llm_provider,
                llm_model=llm_model,
                started_at=started_at,
                completed_at=completed_at,
                execution_time_seconds=execution_time,
                tokens_used=tokens_used,
                estimated_cost=estimated_cost,
                structured_data=self._extract_structured_data(command, exec_result),
                metadata={
                    "task_id": task.task_id,
                    "exec_metadata": exec_result.metadata,
                },
            )

            return result

        except Exception as e:
            # Handle execution errors
            completed_at = datetime.now()
            execution_time = (completed_at - started_at).total_seconds()

            return CommandResult(
                command=command,
                status=CommandStatus.FAILED,
                output="",
                agent_used=spec.agent_id,
                started_at=started_at,
                completed_at=completed_at,
                execution_time_seconds=execution_time,
                error_message=str(e),
                error_type=type(e).__name__,
                metadata={"task_id": task.task_id},
            )

    def _build_task_description(
        self, spec: CommandSpec, args: Dict[str, Any]
    ) -> str:
        """
        Build task description from command spec and arguments.

        Args:
            spec: Command specification
            args: Command arguments

        Returns:
            Task description string
        """
        # Base description
        description = f"Execute {spec.name} command\n\n"

        # Add arguments
        if args:
            description += "**Arguments:**\n"
            for key, value in args.items():
                description += f"- {key}: {value}\n"

        return description.strip()

    def _extract_structured_data(
        self, command: str, exec_result: Any
    ) -> Dict[str, Any]:
        """
        Extract structured data from execution result.

        Command-specific parsing to extract structured information
        from LLM output.

        Args:
            command: Command name
            exec_result: Execution result from TaskExecutor

        Returns:
            Structured data dictionary
        """
        structured = {}

        # Command-specific extraction logic
        if command == "/analyze":
            # Try to extract quality score, issues, etc.
            # This is a placeholder - real implementation would parse LLM output
            structured["quality_score"] = None
            structured["issues_found"] = None

        elif command == "/implement":
            # Extract code blocks, file paths, etc.
            structured["files_created"] = []
            structured["code_blocks"] = []

        # Add execution metadata
        structured["execution_method"] = exec_result.metadata.get("execution_method")

        return structured


# Singleton instance
_router_instance: Optional[SlashCommandRouter] = None


def get_command_router() -> SlashCommandRouter:
    """Get singleton SlashCommandRouter instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = SlashCommandRouter()
    return _router_instance
