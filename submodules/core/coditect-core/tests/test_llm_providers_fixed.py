"""
Test LLM Providers - Individual Provider Tests (Fixed)
======================================================

Tests for individual LLM provider implementations with proper mocking.

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock


class TestAnthropicLlm:
    """Test Anthropic Claude provider."""

    @patch('anthropic.AsyncAnthropic')
    def test_anthropic_initialization(self, mock_anthropic_class):
        """Test AnthropicLlm initialization."""
        from llm_abstractions import AnthropicLlm

        llm = AnthropicLlm(
            model="claude-3-5-sonnet-20241022",
            api_key="test-key",
            max_tokens=8192,
            temperature=0.7
        )

        assert llm.model == "claude-3-5-sonnet-20241022"
        assert llm.api_key == "test-key"
        assert llm.max_tokens == 8192
        assert llm.temperature == 0.7
        mock_anthropic_class.assert_called_once_with(api_key="test-key")

    @patch.dict('os.environ', {}, clear=True)
    def test_anthropic_missing_api_key_raises_error(self):
        """Test AnthropicLlm raises error when API key missing."""
        from llm_abstractions import AnthropicLlm

        with pytest.raises(ValueError, match="API key required"):
            AnthropicLlm(model="claude-3-5-sonnet-20241022")

    @pytest.mark.asyncio
    @patch('anthropic.AsyncAnthropic')
    async def test_anthropic_generate_content(self, mock_anthropic_class):
        """Test AnthropicLlm content generation."""
        from llm_abstractions import AnthropicLlm

        # Mock API response
        mock_content = Mock()
        mock_content.text = "Hello from Claude!"
        mock_response = Mock()
        mock_response.content = [mock_content]

        mock_client = Mock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)
        mock_anthropic_class.return_value = mock_client

        llm = AnthropicLlm(api_key="test-key")
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from Claude!"
        mock_client.messages.create.assert_called_once()

    @pytest.mark.asyncio
    @patch('anthropic.AsyncAnthropic')
    async def test_anthropic_empty_messages_raises_error(self, mock_anthropic_class):
        """Test AnthropicLlm raises error for empty messages."""
        from llm_abstractions import AnthropicLlm

        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client

        llm = AnthropicLlm(api_key="test-key")

        with pytest.raises(ValueError, match="Messages list cannot be empty"):
            await llm.generate_content_async([])


class TestOpenAILlm:
    """Test OpenAI GPT provider."""

    @patch('openai.AsyncOpenAI')
    def test_openai_initialization(self, mock_openai_class):
        """Test OpenAILlm initialization."""
        from llm_abstractions import OpenAILlm

        llm = OpenAILlm(
            model="gpt-4o",
            api_key="test-key",
            max_tokens=4000,
            temperature=0.7
        )

        assert llm.model == "gpt-4o"
        assert llm.api_key == "test-key"
        assert llm.max_tokens == 4000
        assert llm.temperature == 0.7
        mock_openai_class.assert_called_once_with(api_key="test-key")

    @pytest.mark.asyncio
    @patch('openai.AsyncOpenAI')
    async def test_openai_generate_content(self, mock_openai_class):
        """Test OpenAILlm content generation."""
        from llm_abstractions import OpenAILlm

        # Mock API response
        mock_message = Mock()
        mock_message.content = "Hello from GPT!"
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response = Mock()
        mock_response.choices = [mock_choice]

        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai_class.return_value = mock_client

        llm = OpenAILlm(api_key="test-key")
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from GPT!"

    @pytest.mark.asyncio
    @patch('openai.AsyncOpenAI')
    async def test_openai_invalid_role_raises_error(self, mock_openai_class):
        """Test OpenAILlm raises error for invalid role."""
        from llm_abstractions import OpenAILlm

        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        llm = OpenAILlm(api_key="test-key")

        messages = [{"role": "invalid", "content": "test"}]
        with pytest.raises(ValueError, match="Invalid role"):
            await llm.generate_content_async(messages)


class TestGemini:
    """Test Google Gemini provider."""

    @patch('google.generativeai')
    def test_gemini_initialization(self, mock_genai):
        """Test Gemini initialization."""
        from llm_abstractions import Gemini

        llm = Gemini(
            model="gemini-2.0-flash",
            api_key="test-key",
            max_tokens=8192,
            temperature=0.7
        )

        assert llm.model == "gemini-2.0-flash"
        assert llm.api_key == "test-key"
        assert llm.max_tokens == 8192
        assert llm.temperature == 0.7
        mock_genai.configure.assert_called_once_with(api_key="test-key")

    @pytest.mark.asyncio
    @patch('asyncio.to_thread')
    @patch('google.generativeai')
    async def test_gemini_generate_content(self, mock_genai, mock_to_thread):
        """Test Gemini content generation."""
        from llm_abstractions import Gemini

        # Mock API response
        mock_response = Mock()
        mock_response.text = "Hello from Gemini!"
        mock_to_thread.return_value = mock_response

        llm = Gemini(api_key="test-key")
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from Gemini!"
        mock_to_thread.assert_called_once()


class TestHuggingFaceLlm:
    """Test Hugging Face provider."""

    @patch('huggingface_hub.AsyncInferenceClient')
    def test_huggingface_initialization(self, mock_client_class):
        """Test HuggingFaceLlm initialization."""
        from llm_abstractions import HuggingFaceLlm

        llm = HuggingFaceLlm(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            api_key="test-key"
        )

        assert llm.model == "meta-llama/Meta-Llama-3-8B-Instruct"
        assert llm.api_key == "test-key"
        mock_client_class.assert_called_once()

    @pytest.mark.asyncio
    @patch('huggingface_hub.AsyncInferenceClient')
    async def test_huggingface_generate_content(self, mock_client_class):
        """Test HuggingFaceLlm content generation."""
        from llm_abstractions import HuggingFaceLlm

        # Mock API response
        mock_message = Mock()
        mock_message.content = "Hello from Llama!"
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response = Mock()
        mock_response.choices = [mock_choice]

        mock_client = Mock()
        mock_client.chat_completion = AsyncMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        llm = HuggingFaceLlm(api_key="test-key")
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from Llama!"


class TestOllamaLlm:
    """Test Ollama local inference provider."""

    def test_ollama_initialization(self):
        """Test OllamaLlm initialization."""
        from llm_abstractions import OllamaLlm

        llm = OllamaLlm(
            model="llama3.2",
            base_url="http://localhost:11434"
        )

        assert llm.model == "llama3.2"
        assert llm.base_url == "http://localhost:11434"

    @pytest.mark.asyncio
    async def test_ollama_connection_error(self):
        """Test OllamaLlm handles connection errors gracefully."""
        from llm_abstractions import OllamaLlm

        llm = OllamaLlm(base_url="http://localhost:9999")  # Invalid port

        messages = [{"role": "user", "content": "test"}]
        with pytest.raises(RuntimeError, match="Failed to connect to Ollama"):
            await llm.generate_content_async(messages)


class TestLMStudioLlm:
    """Test LM Studio local inference provider."""

    def test_lmstudio_initialization(self):
        """Test LMStudioLlm initialization."""
        from llm_abstractions import LMStudioLlm

        llm = LMStudioLlm(
            model="llama-3.2-3b-instruct",
            base_url="http://localhost:1234/v1"
        )

        assert llm.model == "llama-3.2-3b-instruct"
        assert llm.base_url == "http://localhost:1234/v1"

    @pytest.mark.asyncio
    @patch('openai.AsyncOpenAI')
    async def test_lmstudio_generate_content(self, mock_openai_class):
        """Test LMStudioLlm content generation."""
        from llm_abstractions import LMStudioLlm

        # Mock API response
        mock_message = Mock()
        mock_message.content = "Hello from LM Studio!"
        mock_choice = Mock()
        mock_choice.message = mock_message
        mock_response = Mock()
        mock_response.choices = [mock_choice]

        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai_class.return_value = mock_client

        llm = LMStudioLlm()
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from LM Studio!"


class TestSearchAugmentedLlm:
    """Test Search-Augmented LLM wrapper."""

    @patch('duckduckgo_search.DDGS')
    @patch('anthropic.AsyncAnthropic')
    def test_search_augmented_initialization(self, mock_anthropic_class, mock_ddgs_class):
        """Test SearchAugmentedLlm initialization."""
        from llm_abstractions import SearchAugmentedLlm, AnthropicLlm

        base_llm = AnthropicLlm(api_key="test-key")
        search_llm = SearchAugmentedLlm(
            llm=base_llm,
            search_provider="duckduckgo",
            auto_search=True,
            max_results=5
        )

        assert search_llm.llm == base_llm
        assert search_llm.search_provider == "duckduckgo"
        assert search_llm.auto_search is True
        assert search_llm.max_results == 5

    def test_search_augmented_should_search_detection(self):
        """Test _should_search keyword detection."""
        from llm_abstractions import SearchAugmentedLlm

        base_llm = Mock()
        search_llm = SearchAugmentedLlm(llm=base_llm, auto_search=True, search_provider="duckduckgo")

        # Should trigger search
        assert search_llm._should_search([{"role": "user", "content": "latest news"}])
        assert search_llm._should_search([{"role": "user", "content": "what's current"}])
        assert search_llm._should_search([{"role": "user", "content": "today's update"}])
        assert search_llm._should_search([{"role": "user", "content": "recent 2025"}])

        # Should not trigger search
        assert not search_llm._should_search([{"role": "user", "content": "explain this"}])
        assert not search_llm._should_search([{"role": "user", "content": "how does it work"}])
