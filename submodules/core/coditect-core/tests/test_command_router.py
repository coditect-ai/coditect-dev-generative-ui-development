"""
Tests for Slash Command Router (Phase 2B)

Tests command parsing, routing, execution, and structured results.
"""

import pytest
from datetime import datetime
from orchestration import (
    SlashCommandRouter,
    CommandParser,
    CommandResult,
    CommandStatus,
    CommandSpec,
    COMMAND_REGISTRY,
    get_command_router,
    AgentRegistry,
)


class TestCommandParser:
    """Test command parsing."""

    def test_parse_simple_command(self):
        """Test parsing simple command without arguments."""
        parser = CommandParser()
        command, args = parser.parse("/analyze")

        assert command == "/analyze"
        assert args == {}

    def test_parse_command_with_single_arg(self):
        """Test parsing command with single argument."""
        parser = CommandParser()
        command, args = parser.parse("/analyze target=src/main.rs")

        assert command == "/analyze"
        assert args == {"target": "src/main.rs"}

    def test_parse_command_with_multiple_args(self):
        """Test parsing command with multiple arguments."""
        parser = CommandParser()
        command, args = parser.parse("/analyze target=src/main.rs focus=security")

        assert command == "/analyze"
        assert args == {"target": "src/main.rs", "focus": "security"}

    def test_parse_command_with_quoted_value(self):
        """Test parsing command with quoted argument value."""
        parser = CommandParser()
        command, args = parser.parse("/implement description='Add JWT authentication'")

        assert command == "/implement"
        assert args == {"description": "Add JWT authentication"}

    def test_parse_command_with_double_quoted_value(self):
        """Test parsing command with double-quoted argument value."""
        parser = CommandParser()
        command, args = parser.parse('/research topic="GraphQL vs REST"')

        assert command == "/research"
        assert args == {"topic": "GraphQL vs REST"}

    def test_parse_command_with_text_no_key(self):
        """Test parsing command with text but no key=value format."""
        parser = CommandParser()
        command, args = parser.parse("/implement Add authentication system")

        assert command == "/implement"
        assert args == {"description": "Add authentication system"}


class TestCommandRegistry:
    """Test command registry."""

    def test_registry_has_commands(self):
        """Test that command registry has expected commands."""
        assert "/analyze" in COMMAND_REGISTRY
        assert "/implement" in COMMAND_REGISTRY
        assert "/research" in COMMAND_REGISTRY
        assert "/strategy" in COMMAND_REGISTRY
        assert "/optimize" in COMMAND_REGISTRY
        assert "/document" in COMMAND_REGISTRY
        assert "/new-project" in COMMAND_REGISTRY

    def test_analyze_command_spec(self):
        """Test /analyze command specification."""
        spec = COMMAND_REGISTRY["/analyze"]

        assert spec.name == "/analyze"
        assert spec.agent_id == "code-reviewer"
        assert spec.task_type == "code-generation"
        assert len(spec.examples) > 0

    def test_implement_command_spec(self):
        """Test /implement command specification."""
        spec = COMMAND_REGISTRY["/implement"]

        assert spec.name == "/implement"
        assert spec.agent_id == "rust-expert-developer"
        assert "description" in spec.required_args
        assert spec.task_type == "code-generation"

    def test_research_command_spec(self):
        """Test /research command specification."""
        spec = COMMAND_REGISTRY["/research"]

        assert spec.name == "/research"
        assert spec.agent_id == "web-search-researcher"
        assert "topic" in spec.required_args
        assert spec.task_type == "research"


class TestCommandSpec:
    """Test CommandSpec validation."""

    def test_validate_args_success(self):
        """Test successful argument validation."""
        spec = CommandSpec(
            name="/test",
            agent_id="test-agent",
            description="Test command",
            required_args=["arg1", "arg2"],
            optional_args=["arg3"],
        )

        is_valid, error = spec.validate_args({"arg1": "value1", "arg2": "value2"})

        assert is_valid is True
        assert error is None

    def test_validate_args_with_optional(self):
        """Test validation with optional arguments."""
        spec = CommandSpec(
            name="/test",
            agent_id="test-agent",
            description="Test command",
            required_args=["arg1"],
            optional_args=["arg2"],
        )

        is_valid, error = spec.validate_args({"arg1": "value1", "arg2": "value2"})

        assert is_valid is True
        assert error is None

    def test_validate_args_missing_required(self):
        """Test validation failure for missing required argument."""
        spec = CommandSpec(
            name="/test",
            agent_id="test-agent",
            description="Test command",
            required_args=["arg1", "arg2"],
        )

        is_valid, error = spec.validate_args({"arg1": "value1"})

        assert is_valid is False
        assert "arg2" in error


class TestSlashCommandRouter:
    """Test SlashCommandRouter."""

    def test_router_initialization(self):
        """Test router initializes correctly."""
        router = SlashCommandRouter()

        assert router.registry is not None
        assert router.executor is not None
        assert router.parser is not None
        assert len(router.commands) > 0

    def test_list_commands(self):
        """Test listing all commands."""
        router = SlashCommandRouter()
        commands = router.list_commands()

        assert len(commands) > 0
        assert all(isinstance(cmd, CommandSpec) for cmd in commands)

    def test_list_commands_by_category(self):
        """Test filtering commands by category."""
        router = SlashCommandRouter()
        dev_commands = router.list_commands(category="development")

        assert len(dev_commands) > 0
        assert all(cmd.category == "development" for cmd in dev_commands)

    def test_get_command_spec(self):
        """Test getting command specification."""
        router = SlashCommandRouter()
        spec = router.get_command_spec("/analyze")

        assert spec is not None
        assert spec.name == "/analyze"
        assert spec.agent_id == "code-reviewer"

    def test_get_command_spec_unknown(self):
        """Test getting unknown command returns None."""
        router = SlashCommandRouter()
        spec = router.get_command_spec("/unknown")

        assert spec is None

    def test_get_command_help(self):
        """Test getting command help text."""
        router = SlashCommandRouter()
        help_text = router.get_command_help("/analyze")

        assert "/analyze" in help_text
        assert "code-reviewer" in help_text
        assert "Examples" in help_text

    def test_get_command_help_unknown(self):
        """Test help for unknown command."""
        router = SlashCommandRouter()
        help_text = router.get_command_help("/unknown")

        assert "Unknown command" in help_text

    @pytest.mark.asyncio
    async def test_execute_unknown_command(self):
        """Test executing unknown command returns error."""
        router = SlashCommandRouter()
        result = await router.execute("/unknown")

        assert result.command == "/unknown"
        assert result.status == CommandStatus.FAILED
        assert result.error_type == "UnknownCommand"
        assert "Unknown command" in result.error_message

    @pytest.mark.asyncio
    async def test_execute_command_missing_required_args(self):
        """Test executing command with missing required args."""
        router = SlashCommandRouter()
        result = await router.execute("/implement")  # Missing required 'description'

        assert result.command == "/implement"
        assert result.status == CommandStatus.FAILED
        assert result.error_type == "InvalidArguments"
        assert "description" in result.error_message

    def test_build_task_description(self):
        """Test building task description from command spec."""
        router = SlashCommandRouter()
        spec = COMMAND_REGISTRY["/analyze"]
        args = {"target": "src/main.rs", "focus": "security"}

        description = router._build_task_description(spec, args)

        assert "/analyze" in description
        assert "target" in description
        assert "src/main.rs" in description
        assert "focus" in description
        assert "security" in description


class TestCommandResult:
    """Test CommandResult data structure."""

    def test_command_result_creation(self):
        """Test creating CommandResult."""
        result = CommandResult(
            command="/analyze",
            status=CommandStatus.SUCCESS,
            output="Analysis complete",
            agent_used="code-reviewer",
            llm_provider="anthropic-claude",
            llm_model="claude-3-5-haiku-20241022",
        )

        assert result.command == "/analyze"
        assert result.status == CommandStatus.SUCCESS
        assert result.output == "Analysis complete"
        assert result.agent_used == "code-reviewer"

    def test_command_result_to_dict(self):
        """Test converting CommandResult to dictionary."""
        result = CommandResult(
            command="/analyze",
            status=CommandStatus.SUCCESS,
            output="Analysis complete",
            agent_used="code-reviewer",
        )

        data = result.to_dict()

        assert isinstance(data, dict)
        assert data["command"] == "/analyze"
        assert data["status"] == "success"
        assert data["agent_used"] == "code-reviewer"

    def test_command_result_success_property(self):
        """Test success property."""
        success_result = CommandResult(
            command="/test",
            status=CommandStatus.SUCCESS,
            output="Done",
        )

        failed_result = CommandResult(
            command="/test",
            status=CommandStatus.FAILED,
            output="",
        )

        assert success_result.success is True
        assert failed_result.success is False

    def test_command_result_cost_formatted(self):
        """Test formatted cost string."""
        result = CommandResult(
            command="/test",
            status=CommandStatus.SUCCESS,
            output="Done",
            estimated_cost=0.0032,
        )

        assert result.cost_formatted == "$0.0032"

    def test_command_result_cost_formatted_none(self):
        """Test formatted cost when None."""
        result = CommandResult(
            command="/test",
            status=CommandStatus.SUCCESS,
            output="Done",
        )

        assert result.cost_formatted == "N/A"


class TestGetCommandRouter:
    """Test singleton get_command_router function."""

    def test_get_singleton_instance(self):
        """Test getting singleton router instance."""
        router1 = get_command_router()
        router2 = get_command_router()

        assert router1 is router2  # Same instance


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
