"""
Test LLM Providers - Individual Provider Tests
==============================================

Tests for individual LLM provider implementations with mocking.

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from llm_abstractions import (
    AnthropicLlm,
    OpenAILlm,
    Gemini,
    HuggingFaceLlm,
    OllamaLlm,
    LMStudioLlm,
    SearchAugmentedLlm
)


class TestAnthropicLlm:
    """Test Anthropic Claude provider."""

    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('llm_abstractions.anthropic_llm.AsyncAnthropic')
    def test_anthropic_initialization(self, mock_anthropic):
        """Test AnthropicLlm initialization."""
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

    @patch.dict('os.environ', {})
    def test_anthropic_missing_api_key_raises_error(self):
        """Test AnthropicLlm raises error when API key missing."""
        with pytest.raises(ValueError, match="API key required"):
            AnthropicLlm(model="claude-3-5-sonnet-20241022")

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('llm_abstractions.anthropic_llm.AsyncAnthropic')
    async def test_anthropic_generate_content(self, mock_anthropic):
        """Test AnthropicLlm content generation."""
        # Mock API response
        mock_response = Mock()
        mock_response.content = [Mock(text="Hello from Claude!")]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)
        mock_anthropic.return_value = mock_client

        llm = AnthropicLlm(api_key="test-key")
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from Claude!"
        mock_client.messages.create.assert_called_once()


class TestOpenAILlm:
    """Test OpenAI GPT provider."""

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('llm_abstractions.openai_llm.AsyncOpenAI')
    def test_openai_initialization(self, mock_openai):
        """Test OpenAILlm initialization."""
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

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('llm_abstractions.openai_llm.AsyncOpenAI')
    async def test_openai_generate_content(self, mock_openai):
        """Test OpenAILlm content generation."""
        # Mock API response
        mock_response = Mock()
        mock_choice = Mock()
        mock_choice.message.content = "Hello from GPT!"
        mock_response.choices = [mock_choice]

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client

        llm = OpenAILlm(api_key="test-key")
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from GPT!"


class TestGemini:
    """Test Google Gemini provider."""

    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'})
    @patch('llm_abstractions.gemini.genai')
    def test_gemini_initialization(self, mock_genai):
        """Test Gemini initialization."""
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

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'})
    @patch('llm_abstractions.gemini.genai')
    @patch('llm_abstractions.gemini.asyncio.to_thread')
    async def test_gemini_generate_content(self, mock_to_thread, mock_genai):
        """Test Gemini content generation."""
        # Mock API response
        mock_response = Mock()
        mock_response.text = "Hello from Gemini!"
        mock_to_thread.return_value = mock_response

        llm = Gemini(api_key="test-key")
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from Gemini!"


class TestHuggingFaceLlm:
    """Test Hugging Face provider."""

    @patch.dict('os.environ', {'HF_TOKEN': 'test-key'})
    @patch('llm_abstractions.huggingface_llm.AsyncInferenceClient')
    def test_huggingface_initialization(self, mock_client):
        """Test HuggingFaceLlm initialization."""
        llm = HuggingFaceLlm(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            api_key="test-key"
        )

        assert llm.model == "meta-llama/Meta-Llama-3-8B-Instruct"
        assert llm.api_key == "test-key"

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'HF_TOKEN': 'test-key'})
    @patch('llm_abstractions.huggingface_llm.AsyncInferenceClient')
    async def test_huggingface_generate_content(self, mock_client_class):
        """Test HuggingFaceLlm content generation."""
        # Mock API response
        mock_response = Mock()
        mock_choice = Mock()
        mock_choice.message.content = "Hello from Llama!"
        mock_response.choices = [mock_choice]

        mock_client = AsyncMock()
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
        llm = OllamaLlm(
            model="llama3.2",
            base_url="http://localhost:11434"
        )

        assert llm.model == "llama3.2"
        assert llm.base_url == "http://localhost:11434"

    @pytest.mark.asyncio
    @patch('llm_abstractions.ollama_llm.aiohttp.ClientSession')
    async def test_ollama_generate_content(self, mock_session_class):
        """Test OllamaLlm content generation."""
        # Mock API response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "message": {"content": "Hello from Ollama!"}
        })

        mock_session = AsyncMock()
        mock_session.post = AsyncMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock()

        mock_session_class.return_value = mock_session

        llm = OllamaLlm(model="llama3.2")
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from Ollama!"


class TestLMStudioLlm:
    """Test LM Studio local inference provider."""

    def test_lmstudio_initialization(self):
        """Test LMStudioLlm initialization."""
        llm = LMStudioLlm(
            model="llama-3.2-3b-instruct",
            base_url="http://localhost:1234/v1"
        )

        assert llm.model == "llama-3.2-3b-instruct"
        assert llm.base_url == "http://localhost:1234/v1"

    @pytest.mark.asyncio
    @patch('llm_abstractions.lmstudio_llm.AsyncOpenAI')
    async def test_lmstudio_generate_content(self, mock_openai):
        """Test LMStudioLlm content generation."""
        # Mock API response
        mock_response = Mock()
        mock_choice = Mock()
        mock_choice.message.content = "Hello from LM Studio!"
        mock_response.choices = [mock_choice]

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client

        llm = LMStudioLlm()
        messages = [{"role": "user", "content": "Hello"}]

        response = await llm.generate_content_async(messages)

        assert response == "Hello from LM Studio!"


class TestSearchAugmentedLlm:
    """Test Search-Augmented LLM wrapper."""

    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('llm_abstractions.anthropic_llm.AsyncAnthropic')
    @patch('llm_abstractions.search_augmented_llm.DDGS')
    def test_search_augmented_initialization(self, mock_ddgs, mock_anthropic):
        """Test SearchAugmentedLlm initialization."""
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

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('llm_abstractions.anthropic_llm.AsyncAnthropic')
    @patch('llm_abstractions.search_augmented_llm.DDGS')
    async def test_search_augmented_auto_search(self, mock_ddgs, mock_anthropic):
        """Test SearchAugmentedLlm auto-detection of search queries."""
        # Setup base LLM mock
        mock_response = Mock()
        mock_response.content = [Mock(text="Response with search results")]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)
        mock_anthropic.return_value = mock_client

        # Setup search mock
        mock_search_instance = Mock()
        mock_search_instance.text.return_value = [
            {"title": "Result 1", "href": "http://example.com/1", "body": "Snippet 1"},
            {"title": "Result 2", "href": "http://example.com/2", "body": "Snippet 2"}
        ]
        mock_ddgs.return_value = mock_search_instance

        base_llm = AnthropicLlm(api_key="test-key")
        search_llm = SearchAugmentedLlm(llm=base_llm, auto_search=True)

        # Query with "latest" should trigger search
        messages = [{"role": "user", "content": "What's the latest on AI?"}]
        response = await search_llm.generate_content_async(messages)

        assert response == "Response with search results"
        # Verify search was called
        mock_search_instance.text.assert_called_once()

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('llm_abstractions.anthropic_llm.AsyncAnthropic')
    async def test_search_augmented_no_search_needed(self, mock_anthropic):
        """Test SearchAugmentedLlm skips search when not needed."""
        # Setup base LLM mock
        mock_response = Mock()
        mock_response.content = [Mock(text="Normal response")]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)
        mock_anthropic.return_value = mock_client

        base_llm = AnthropicLlm(api_key="test-key")
        search_llm = SearchAugmentedLlm(llm=base_llm, auto_search=True)

        # Query without trigger keywords
        messages = [{"role": "user", "content": "Explain Python"}]
        response = await search_llm.generate_content_async(messages)

        assert response == "Normal response"

    def test_search_augmented_should_search_detection(self):
        """Test _should_search keyword detection."""
        base_llm = Mock()
        search_llm = SearchAugmentedLlm(llm=base_llm, auto_search=True)

        # Should trigger search
        assert search_llm._should_search([{"role": "user", "content": "latest news"}])
        assert search_llm._should_search([{"role": "user", "content": "what's current"}])
        assert search_llm._should_search([{"role": "user", "content": "today's update"}])
        assert search_llm._should_search([{"role": "user", "content": "recent 2025"}])

        # Should not trigger search
        assert not search_llm._should_search([{"role": "user", "content": "explain this"}])
        assert not search_llm._should_search([{"role": "user", "content": "how does it work"}])


class TestProviderErrorHandling:
    """Test error handling across all providers."""

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('llm_abstractions.anthropic_llm.AsyncAnthropic')
    async def test_anthropic_empty_messages_raises_error(self, mock_anthropic):
        """Test AnthropicLlm raises error for empty messages."""
        llm = AnthropicLlm(api_key="test-key")

        with pytest.raises(ValueError, match="Messages list cannot be empty"):
            await llm.generate_content_async([])

    @pytest.mark.asyncio
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('llm_abstractions.openai_llm.AsyncOpenAI')
    async def test_openai_invalid_role_raises_error(self, mock_openai):
        """Test OpenAILlm raises error for invalid role."""
        llm = OpenAILlm(api_key="test-key")

        messages = [{"role": "invalid", "content": "test"}]
        with pytest.raises(ValueError, match="Invalid role"):
            await llm.generate_content_async(messages)

    @pytest.mark.asyncio
    async def test_ollama_connection_error(self):
        """Test OllamaLlm handles connection errors gracefully."""
        llm = OllamaLlm(base_url="http://localhost:9999")  # Invalid port

        messages = [{"role": "user", "content": "test"}]
        with pytest.raises(RuntimeError, match="Failed to connect to Ollama"):
            await llm.generate_content_async(messages)
