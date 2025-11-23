"""
Test TaskExecutor LLM Integration - Phase 1C
============================================

Tests for TaskExecutor integration with LlmFactory.

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from orchestration.executor import TaskExecutor, ExecutionStatus, ExecutionResult
from orchestration.agent_registry import (
    AgentRegistry,
    AgentConfig,
    AgentType,
    AgentInterface,
    AgentCapability
)
from orchestration.task import AgentTask, TaskStatus


@pytest.fixture
def agent_registry():
    """Create agent registry for testing."""
    registry = AgentRegistry()

    # Register Claude agent
    registry.register_agent(
        name="claude-test",
        agent_type=AgentType.ANTHROPIC_CLAUDE,
        interface=AgentInterface.API,
        model="claude-3-5-sonnet-20241022",
        api_key="test-key",
        metadata={
            "max_tokens": 4096,
            "temperature": 0.7,
            "system_prompt": "You are a helpful assistant."
        }
    )

    # Register GPT agent
    registry.register_agent(
        name="gpt-test",
        agent_type=AgentType.OPENAI_GPT,
        interface=AgentInterface.API,
        model="gpt-4o",
        api_key="test-key",
        metadata={
            "max_tokens": 4000,
            "temperature": 0.7
        }
    )

    # Register Ollama agent (no API key)
    registry.register_agent(
        name="ollama-test",
        agent_type="ollama",  # Using string for custom type
        interface=AgentInterface.API,
        model="llama3.2",
        metadata={
            "base_url": "http://localhost:11434"
        }
    )

    return registry


@pytest.fixture
def sample_task():
    """Create sample task for testing."""
    return AgentTask(
        task_id="TEST-001",
        title="Explain async/await in Python",
        description="Explain async/await in Python",
        agent="claude-test",
        status=TaskStatus.PENDING,
        metadata={"context": "User is new to async programming"}
    )


class TestTaskExecutorLlmIntegration:
    """Test TaskExecutor integration with LLM Factory."""

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_uses_llm_factory(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor uses LlmFactory for API execution."""
        # Mock LLM provider
        mock_llm = AsyncMock()
        mock_llm.generate_content_async = AsyncMock(
            return_value="Async/await explanation from LLM"
        )
        mock_factory.get_provider.return_value = mock_llm

        # Create executor
        executor = TaskExecutor(registry=agent_registry)

        # Execute task
        result = await executor.execute(sample_task, agent="claude-test")

        # Verify LlmFactory was used
        mock_factory.get_provider.assert_called_once()
        mock_llm.generate_content_async.assert_called_once()

        # Verify result
        assert result.status == ExecutionStatus.SUCCESS
        assert result.output == "Async/await explanation from LLM"
        assert result.metadata["execution_method"] == "llm_factory"
        assert result.metadata["provider"] == "anthropic-claude"

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_prepares_messages_correctly(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor prepares messages with system prompt and context."""
        # Mock LLM provider
        mock_llm = AsyncMock()
        mock_llm.generate_content_async = AsyncMock(return_value="Response")
        mock_factory.get_provider.return_value = mock_llm

        executor = TaskExecutor(registry=agent_registry)
        await executor.execute(sample_task, agent="claude-test")

        # Verify messages structure
        call_args = mock_llm.generate_content_async.call_args
        messages = call_args[0][0]

        # Should have system prompt, task description, and context
        assert len(messages) == 3
        assert messages[0]["role"] == "system"
        assert "helpful assistant" in messages[0]["content"]
        assert messages[1]["role"] == "user"
        assert "Explain async/await" in messages[1]["content"]
        assert messages[2]["role"] == "user"
        assert "Context:" in messages[2]["content"]
        assert "new to async" in messages[2]["content"]

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_passes_provider_config(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor passes correct config to LlmFactory."""
        mock_llm = AsyncMock()
        mock_llm.generate_content_async = AsyncMock(return_value="Response")
        mock_factory.get_provider.return_value = mock_llm

        executor = TaskExecutor(registry=agent_registry)
        await executor.execute(sample_task, agent="claude-test")

        # Verify factory was called with correct parameters
        mock_factory.get_provider.assert_called_once_with(
            agent_type="anthropic-claude",
            model="claude-3-5-sonnet-20241022",
            api_key="test-key",
            max_tokens=4096,
            temperature=0.7
        )

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_handles_llm_factory_error(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor falls back when LlmFactory fails."""
        # Mock factory to raise error
        mock_factory.get_provider.side_effect = ValueError("Provider not available")

        executor = TaskExecutor(registry=agent_registry)
        result = await executor.execute(sample_task, agent="claude-test")

        # Should fall back to script-based execution
        assert result.metadata.get("llm_factory_error") is not None

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', False)
    async def test_executor_falls_back_when_abstractions_unavailable(
        self,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor falls back when llm_abstractions not available."""
        executor = TaskExecutor(registry=agent_registry)
        result = await executor.execute(sample_task, agent="claude-test")

        # Should fall back to script-based execution
        assert result.metadata.get("execution_method") != "llm_factory"

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_parallel_execution_with_llm_factory(
        self,
        mock_factory,
        agent_registry
    ):
        """Test TaskExecutor parallel execution with multiple LLM providers."""
        # Mock different LLM providers
        mock_claude = AsyncMock()
        mock_claude.generate_content_async = AsyncMock(return_value="Claude response")

        mock_gpt = AsyncMock()
        mock_gpt.generate_content_async = AsyncMock(return_value="GPT response")

        # Return different mocks based on agent type
        def get_provider_side_effect(**kwargs):
            if kwargs["agent_type"] == "anthropic-claude":
                return mock_claude
            elif kwargs["agent_type"] == "openai-gpt":
                return mock_gpt
            return AsyncMock()

        mock_factory.get_provider.side_effect = get_provider_side_effect

        # Create tasks
        task1 = AgentTask(
            task_id="TASK-001",
            title="Task 1",
            description="Task 1",
            agent="claude-test",
            status=TaskStatus.PENDING
        )

        task2 = AgentTask(
            task_id="TASK-002",
            title="Task 2",
            description="Task 2",
            agent="gpt-test",
            status=TaskStatus.PENDING
        )

        # Execute in parallel
        executor = TaskExecutor(registry=agent_registry)
        results = await executor.execute_parallel([
            (task1, "claude-test"),
            (task2, "gpt-test")
        ])

        # Verify both executed successfully
        assert len(results) == 2
        assert results[0].status == ExecutionStatus.SUCCESS
        assert results[0].output == "Claude response"
        assert results[1].status == ExecutionStatus.SUCCESS
        assert results[1].output == "GPT response"

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_tracks_execution_metadata(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor tracks execution metadata."""
        mock_llm = AsyncMock()
        mock_llm.generate_content_async = AsyncMock(return_value="Response")
        mock_factory.get_provider.return_value = mock_llm

        executor = TaskExecutor(registry=agent_registry)
        result = await executor.execute(sample_task, agent="claude-test")

        # Verify metadata
        assert result.metadata["execution_method"] == "llm_factory"
        assert result.metadata["provider"] == "anthropic-claude"
        assert result.metadata["model"] == "claude-3-5-sonnet-20241022"
        assert result.task_id == "TEST-001"
        assert result.agent == "claude-test"
        assert result.started_at is not None

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_handles_api_exceptions(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor handles API exceptions gracefully."""
        mock_llm = AsyncMock()
        mock_llm.generate_content_async = AsyncMock(
            side_effect=RuntimeError("API call failed")
        )
        mock_factory.get_provider.return_value = mock_llm

        executor = TaskExecutor(registry=agent_registry)
        result = await executor.execute(sample_task, agent="claude-test")

        # Should record error in metadata
        assert "llm_factory_error" in result.metadata
        assert "API call failed" in result.metadata["llm_factory_error"]

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_supports_local_inference(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor works with local inference providers (Ollama)."""
        mock_llm = AsyncMock()
        mock_llm.generate_content_async = AsyncMock(
            return_value="Response from local Ollama"
        )
        mock_factory.get_provider.return_value = mock_llm

        executor = TaskExecutor(registry=agent_registry)
        result = await executor.execute(sample_task, agent="ollama-test")

        # Verify execution
        assert result.status == ExecutionStatus.SUCCESS
        assert result.output == "Response from local Ollama"
        mock_factory.get_provider.assert_called_once()

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_duration_tracking(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test TaskExecutor tracks execution duration."""
        mock_llm = AsyncMock()
        mock_llm.generate_content_async = AsyncMock(return_value="Response")
        mock_factory.get_provider.return_value = mock_llm

        executor = TaskExecutor(registry=agent_registry)
        result = await executor.execute(sample_task, agent="claude-test")

        # Verify duration tracking
        assert result.started_at is not None
        assert result.completed_at is not None
        assert result.duration_seconds is not None
        assert result.duration_seconds >= 0


class TestExecutorBackwardCompatibility:
    """Test backward compatibility with script-based execution."""

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_falls_back_to_script_on_provider_error(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test executor falls back to script when provider fails."""
        # Mock factory to raise ValueError (provider not available)
        mock_factory.get_provider.side_effect = ValueError("Provider not registered")

        executor = TaskExecutor(registry=agent_registry)
        result = await executor.execute(sample_task, agent="claude-test")

        # Should attempt fallback
        assert "llm_factory_error" in result.metadata
        assert "Provider not registered" in result.metadata["llm_factory_error"]

    @pytest.mark.asyncio
    @patch('orchestration.executor.LLM_ABSTRACTIONS_AVAILABLE', True)
    @patch('orchestration.executor.LlmFactory')
    async def test_executor_falls_back_to_script_on_runtime_error(
        self,
        mock_factory,
        agent_registry,
        sample_task
    ):
        """Test executor falls back to script when LLM call fails."""
        mock_llm = AsyncMock()
        mock_llm.generate_content_async = AsyncMock(
            side_effect=Exception("Network error")
        )
        mock_factory.get_provider.return_value = mock_llm

        executor = TaskExecutor(registry=agent_registry)
        result = await executor.execute(sample_task, agent="claude-test")

        # Should record error and attempt fallback
        assert "llm_factory_error" in result.metadata
