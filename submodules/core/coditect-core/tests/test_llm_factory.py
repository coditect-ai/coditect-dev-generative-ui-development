"""
Test LLM Factory - Provider Registration and Instantiation
==========================================================

Tests for LlmFactory dynamic provider loading and registration.

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

import pytest
from unittest.mock import Mock, patch
from llm_abstractions import LlmFactory, BaseLlm
from llm_abstractions.llm_factory import LlmFactory as Factory


class TestLlmFactory:
    """Test LlmFactory provider registration and instantiation."""

    def test_factory_registers_default_providers(self):
        """Test that factory registers all default providers on first use."""
        # Get providers (triggers lazy loading)
        providers = LlmFactory.list_providers()

        # Should have all 6 providers
        assert len(providers) >= 6
        assert "anthropic-claude" in providers
        assert "openai-gpt" in providers
        assert "google-gemini" in providers
        assert "huggingface" in providers
        assert "ollama" in providers
        assert "lmstudio" in providers

    def test_factory_list_providers_returns_dict(self):
        """Test list_providers returns dictionary of providers."""
        providers = LlmFactory.list_providers()

        assert isinstance(providers, dict)
        for key, value in providers.items():
            assert isinstance(key, str)
            assert issubclass(value, BaseLlm)

    def test_factory_is_provider_available(self):
        """Test is_provider_available checks registration."""
        # Should be available
        assert LlmFactory.is_provider_available("anthropic-claude")
        assert LlmFactory.is_provider_available("openai-gpt")
        assert LlmFactory.is_provider_available("google-gemini")

        # Should not be available
        assert not LlmFactory.is_provider_available("non-existent-provider")

    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    def test_factory_get_provider_anthropic(self):
        """Test get_provider returns AnthropicLlm instance."""
        llm = LlmFactory.get_provider(
            agent_type="anthropic-claude",
            model="claude-3-5-sonnet-20241022",
            api_key="test-key"
        )

        assert llm is not None
        assert llm.model == "claude-3-5-sonnet-20241022"
        assert llm.api_key == "test-key"

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_factory_get_provider_openai(self):
        """Test get_provider returns OpenAILlm instance."""
        llm = LlmFactory.get_provider(
            agent_type="openai-gpt",
            model="gpt-4o",
            api_key="test-key"
        )

        assert llm is not None
        assert llm.model == "gpt-4o"
        assert llm.api_key == "test-key"

    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'})
    def test_factory_get_provider_gemini(self):
        """Test get_provider returns Gemini instance."""
        llm = LlmFactory.get_provider(
            agent_type="google-gemini",
            model="gemini-2.0-flash",
            api_key="test-key"
        )

        assert llm is not None
        assert llm.model == "gemini-2.0-flash"
        assert llm.api_key == "test-key"

    def test_factory_get_provider_ollama_no_api_key(self):
        """Test get_provider returns OllamaLlm without API key."""
        llm = LlmFactory.get_provider(
            agent_type="ollama",
            model="llama3.2"
        )

        assert llm is not None
        assert llm.model == "llama3.2"
        assert llm.base_url == "http://localhost:11434"

    def test_factory_get_provider_lmstudio_no_api_key(self):
        """Test get_provider returns LMStudioLlm without API key."""
        llm = LlmFactory.get_provider(
            agent_type="lmstudio",
            model="llama-3.2-3b-instruct"
        )

        assert llm is not None
        assert llm.model == "llama-3.2-3b-instruct"
        assert llm.base_url == "http://localhost:1234/v1"

    def test_factory_get_provider_invalid_raises_error(self):
        """Test get_provider raises ValueError for invalid provider."""
        with pytest.raises(ValueError, match="No LLM provider registered"):
            LlmFactory.get_provider(
                agent_type="invalid-provider",
                model="test-model"
            )

    def test_factory_register_custom_provider(self):
        """Test custom provider registration."""
        # Create custom provider
        class CustomLlm(BaseLlm):
            def __init__(self, model=None, api_key=None, **kwargs):
                self.model = model
                self.api_key = api_key

            async def generate_content_async(self, messages, **kwargs):
                return "custom response"

        # Register custom provider
        LlmFactory.register_provider("custom-llm", CustomLlm)

        # Verify registration
        assert LlmFactory.is_provider_available("custom-llm")

        # Get custom provider
        llm = LlmFactory.get_provider(agent_type="custom-llm")
        assert llm is not None
        assert isinstance(llm, CustomLlm)

    def test_factory_register_provider_validates_base_class(self):
        """Test register_provider validates BaseLlm subclass."""
        # Create invalid provider (not BaseLlm subclass)
        class InvalidProvider:
            pass

        # Should raise TypeError
        with pytest.raises(TypeError, match="must be a subclass of BaseLlm"):
            LlmFactory.register_provider("invalid", InvalidProvider)

    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    def test_factory_get_provider_with_kwargs(self):
        """Test get_provider passes kwargs to provider."""
        llm = LlmFactory.get_provider(
            agent_type="anthropic-claude",
            model="claude-3-5-sonnet-20241022",
            api_key="test-key",
            max_tokens=8192,
            temperature=0.5
        )

        assert llm.max_tokens == 8192
        assert llm.temperature == 0.5

    def test_factory_lazy_loading(self):
        """Test factory lazy loads providers on first use."""
        # Clear internal provider registry
        Factory._providers = {}

        # Verify empty
        assert len(Factory._providers) == 0

        # Get providers (should trigger lazy loading)
        providers = LlmFactory.list_providers()

        # Should have providers now
        assert len(providers) >= 6

    @patch.dict('os.environ', {}, clear=True)
    @patch('anthropic.AsyncAnthropic')
    def test_factory_get_provider_missing_api_key_raises_error(self, mock_anthropic):
        """Test get_provider raises error when API key missing."""
        # Factory wraps ValueError in RuntimeError
        with pytest.raises(RuntimeError, match="Failed to instantiate"):
            LlmFactory.get_provider(
                agent_type="anthropic-claude",
                model="claude-3-5-sonnet-20241022"
            )

    def test_factory_provider_repr(self):
        """Test provider __repr__ methods."""
        llm = LlmFactory.get_provider(
            agent_type="ollama",
            model="llama3.2"
        )

        repr_str = repr(llm)
        assert "OllamaLlm" in repr_str
        assert "llama3.2" in repr_str
