"""
Tests for Agent-to-LLM Bindings (Phase 2A)

Tests the agent-llm-bindings.yaml configuration system and integration with TaskExecutor.
"""

import pytest
import tempfile
from pathlib import Path
from llm_abstractions import AgentLlmConfig, LlmConfig


class TestAgentLlmConfig:
    """Test AgentLlmConfig loader."""

    def test_load_valid_config(self):
        """Test loading a valid agent-llm-bindings.yaml file."""
        # Use the actual config file
        config = AgentLlmConfig.get_instance()

        assert config is not None
        assert len(config.list_configured_agents()) > 0

    def test_get_agent_config_existing(self):
        """Test getting configuration for an existing agent."""
        config = AgentLlmConfig.get_instance()

        # Test with ai-specialist (should exist)
        llm_config = config.get_agent_config("ai-specialist")

        assert llm_config is not None
        assert llm_config.provider == "anthropic-claude"
        assert llm_config.model == "claude-3-5-sonnet-20241022"
        assert llm_config.max_tokens == 4096
        assert llm_config.temperature == 0.7

    def test_get_agent_config_nonexistent_uses_defaults(self):
        """Test getting configuration for non-existent agent falls back to defaults."""
        config = AgentLlmConfig.get_instance()

        # Test with non-existent agent
        llm_config = config.get_agent_config("non-existent-agent")

        # Should return defaults
        assert llm_config is not None
        assert llm_config.provider == "anthropic-claude"  # Default
        assert llm_config.model == "claude-3-5-sonnet-20241022"  # Default

    def test_has_agent_config(self):
        """Test checking if agent has explicit configuration."""
        config = AgentLlmConfig.get_instance()

        # ai-specialist should exist
        assert config.has_agent_config("ai-specialist") is True

        # non-existent agent should not
        assert config.has_agent_config("non-existent-agent") is False

    def test_list_configured_agents(self):
        """Test listing all configured agents."""
        config = AgentLlmConfig.get_instance()

        agents = config.list_configured_agents()

        # Should have ai-specialist (from our bindings file)
        assert "ai-specialist" in agents
        assert "orchestrator" in agents
        assert "rust-expert-developer" in agents

    def test_llm_config_to_factory_kwargs(self):
        """Test converting LlmConfig to factory kwargs."""
        llm_config = LlmConfig(
            provider="anthropic-claude",
            model="claude-3-5-sonnet-20241022",
            api_key="test-key",
            max_tokens=2048,
            temperature=0.5,
            metadata={"custom_field": "value"}
        )

        kwargs = llm_config.to_factory_kwargs()

        assert kwargs["model"] == "claude-3-5-sonnet-20241022"
        assert kwargs["api_key"] == "test-key"
        assert kwargs["max_tokens"] == 2048
        assert kwargs["temperature"] == 0.5
        assert kwargs["custom_field"] == "value"  # Metadata included

    def test_config_with_custom_path(self):
        """Test loading config from custom path."""
        # Create temporary config file
        config_content = """
defaults:
  provider: openai-gpt
  model: gpt-4o
  max_tokens: 4096
  temperature: 0.7

agents:
  test-agent:
    provider: anthropic-claude
    model: claude-3-5-haiku-20241022
    max_tokens: 2048
    temperature: 0.5
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_content)
            temp_path = Path(f.name)

        try:
            # Load config from temp file
            config = AgentLlmConfig(config_path=temp_path)

            # Test defaults
            assert config.defaults.provider == "openai-gpt"
            assert config.defaults.model == "gpt-4o"

            # Test agent config
            llm_config = config.get_agent_config("test-agent")
            assert llm_config.provider == "anthropic-claude"
            assert llm_config.model == "claude-3-5-haiku-20241022"
            assert llm_config.max_tokens == 2048
            assert llm_config.temperature == 0.5

        finally:
            # Cleanup
            temp_path.unlink()


class TestAgentSpecificBindings:
    """Test specific agent bindings from agent-llm-bindings.yaml."""

    def test_ai_specialist_binding(self):
        """Test ai-specialist uses premium Claude Sonnet."""
        config = AgentLlmConfig.get_instance()
        llm_config = config.get_agent_config("ai-specialist")

        assert llm_config.provider == "anthropic-claude"
        assert llm_config.model == "claude-3-5-sonnet-20241022"
        assert llm_config.max_tokens == 4096
        assert llm_config.temperature == 0.7

    def test_rust_expert_binding(self):
        """Test rust-expert-developer uses GPT-4o."""
        config = AgentLlmConfig.get_instance()
        llm_config = config.get_agent_config("rust-expert-developer")

        assert llm_config.provider == "openai-gpt"
        assert llm_config.model == "gpt-4o"
        assert llm_config.temperature == 0.4  # Lower for code generation

    def test_codebase_locator_binding(self):
        """Test codebase-locator uses local Ollama (fast, free)."""
        config = AgentLlmConfig.get_instance()
        llm_config = config.get_agent_config("codebase-locator")

        assert llm_config.provider == "ollama"
        assert llm_config.model == "llama3.2"
        assert llm_config.temperature == 0.5

    def test_qa_reviewer_binding(self):
        """Test qa-reviewer uses fast/cheap Claude Haiku."""
        config = AgentLlmConfig.get_instance()
        llm_config = config.get_agent_config("qa-reviewer")

        assert llm_config.provider == "anthropic-claude"
        assert llm_config.model == "claude-3-5-haiku-20241022"  # Fast and cheap
        assert llm_config.temperature == 0.5  # Consistent QA

    def test_research_agent_binding(self):
        """Test research-agent uses free Gemini."""
        config = AgentLlmConfig.get_instance()
        llm_config = config.get_agent_config("research-agent")

        assert llm_config.provider == "google-gemini"
        assert llm_config.model == "gemini-pro"
        assert llm_config.temperature == 0.8  # Higher for creative research


class TestTaskExecutorIntegration:
    """Test TaskExecutor integration with agent-LLM bindings."""

    def test_bindings_integration_imports(self):
        """Test that TaskExecutor can import agent-LLM bindings."""
        # Import check
        from orchestration.executor import AGENT_LLM_CONFIG_AVAILABLE

        # Should be available since we have the config file
        assert AGENT_LLM_CONFIG_AVAILABLE is True

    def test_agent_config_loaded_by_executor(self):
        """Test that agent configuration can be loaded for executor use."""
        from llm_abstractions import AgentLlmConfig

        # Load config
        config = AgentLlmConfig.get_instance()

        # Simulate what executor does: get config for specific agent
        llm_config = config.get_agent_config("ai-specialist")

        # Verify it would select the right provider
        assert llm_config.provider == "anthropic-claude"
        assert llm_config.model == "claude-3-5-sonnet-20241022"

        # Verify factory kwargs can be created
        factory_kwargs = llm_config.to_factory_kwargs()
        assert "model" in factory_kwargs
        assert "max_tokens" in factory_kwargs
        assert "temperature" in factory_kwargs

    def test_multiple_agent_configs(self):
        """Test loading configs for multiple different agents."""
        from llm_abstractions import AgentLlmConfig

        config = AgentLlmConfig.get_instance()

        # Test different agent types use different providers
        ai_specialist = config.get_agent_config("ai-specialist")
        rust_expert = config.get_agent_config("rust-expert-developer")
        codebase_locator = config.get_agent_config("codebase-locator")

        # Different providers for different use cases
        assert ai_specialist.provider == "anthropic-claude"  # Premium reasoning
        assert rust_expert.provider == "openai-gpt"  # Code generation
        assert codebase_locator.provider == "ollama"  # Local, fast, free


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
