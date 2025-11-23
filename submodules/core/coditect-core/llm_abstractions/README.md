# LLM Abstractions - Multi-Provider LLM Integration

Unified interface for multiple LLM providers with async support, local inference, and search augmentation.

## Overview

The `llm_abstractions` package provides:

- **Unified API**: Single interface (`BaseLlm`) for all providers
- **Async Support**: Full async/await for concurrent operations
- **Provider Flexibility**: 6 providers + search augmentation
- **Local & Cloud**: Support for both cloud APIs and local inference
- **Dynamic Loading**: Factory pattern with lazy loading
- **Search Augmentation**: RAG with web search for grounded responses

## Supported Providers

### Cloud/API Providers

1. **AnthropicLlm** - Anthropic Claude (claude-3-5-sonnet-20241022, etc.)
2. **OpenAILlm** - OpenAI GPT (gpt-4o, gpt-5.1-codex-max, etc.)
3. **Gemini** - Google Gemini (gemini-2.0-flash, gemini-1.5-pro, etc.)
4. **HuggingFaceLlm** - Hugging Face Inference API (Llama 3, Mistral, etc.)

### Local Inference Providers

5. **OllamaLlm** - Ollama local inference (llama3.2, codellama, etc.)
6. **LMStudioLlm** - LM Studio local inference (any GGUF model)

### Search Augmentation

7. **SearchAugmentedLlm** - Wrapper adding web search to any provider

## Quick Start

### Installation

```bash
# Install core dependencies
pip install -r requirements.txt

# Or install specific providers
pip install anthropic openai google-generativeai
pip install huggingface-hub aiohttp duckduckgo-search
```

### Basic Usage

```python
from llm_abstractions import LlmFactory

# Get provider via factory
llm = LlmFactory.get_provider(
    agent_type="anthropic-claude",
    model="claude-3-5-sonnet-20241022"
)

# Generate content
messages = [{"role": "user", "content": "Hello!"}]
response = await llm.generate_content_async(messages)
print(response)
```

### Factory Pattern

```python
from llm_abstractions import LlmFactory

# List available providers
providers = LlmFactory.list_providers()
print(providers)
# Output: {
#   'anthropic-claude': AnthropicLlm,
#   'openai-gpt': OpenAILlm,
#   'google-gemini': Gemini,
#   'huggingface': HuggingFaceLlm,
#   'ollama': OllamaLlm,
#   'lmstudio': LMStudioLlm
# }

# Check if provider available
if LlmFactory.is_provider_available("ollama"):
    llm = LlmFactory.get_provider("ollama", model="llama3.2")
```

### Local Inference

```python
# Ollama (requires Ollama server running)
from llm_abstractions import OllamaLlm

llm = OllamaLlm(
    model="llama3.2",
    base_url="http://localhost:11434"
)

messages = [{"role": "user", "content": "What is 2+2?"}]
response = await llm.generate_content_async(messages)

# LM Studio (requires LM Studio running with model loaded)
from llm_abstractions import LMStudioLlm

llm = LMStudioLlm(
    model="llama-3.2-3b-instruct",
    base_url="http://localhost:1234/v1"
)

response = await llm.generate_content_async(messages)
```

### Search-Augmented Generation

```python
from llm_abstractions import SearchAugmentedLlm, AnthropicLlm

# Wrap any LLM with search capabilities
base_llm = AnthropicLlm(model="claude-3-5-sonnet-20241022")
search_llm = SearchAugmentedLlm(
    llm=base_llm,
    search_provider="duckduckgo",
    auto_search=True  # Auto-detect queries needing search
)

# Query with automatic search augmentation
messages = [{"role": "user", "content": "What's the latest on GPT-5?"}]
response = await search_llm.generate_content_async(messages)
# Response grounded in recent web search results

# Force search with custom query
response = await search_llm.generate_content_async(
    messages,
    force_search=True,
    search_query="GPT-5 news 2025"
)
```

## Provider Details

### 1. AnthropicLlm

**Models:**
- `claude-3-5-sonnet-20241022` (latest, recommended)
- `claude-3-5-haiku-20241022` (fast)
- `claude-3-opus-20240229` (most capable)
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`

**API Key:** `ANTHROPIC_API_KEY` environment variable or `api_key` parameter

**Example:**
```python
from llm_abstractions import AnthropicLlm

llm = AnthropicLlm(
    model="claude-3-5-sonnet-20241022",
    api_key="sk-ant-...",
    max_tokens=4096,
    temperature=0.7
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain async/await in Python"}
]

response = await llm.generate_content_async(messages)
```

### 2. OpenAILlm

**Models:**
- `gpt-4o` (latest, recommended)
- `gpt-5.1-codex-max` (specialized coding, Nov 2025)
- `gpt-4-turbo` (fast)
- `gpt-4` (most capable)
- `gpt-3.5-turbo` (economical)

**API Key:** `OPENAI_API_KEY` environment variable or `api_key` parameter

**Example:**
```python
from llm_abstractions import OpenAILlm

llm = OpenAILlm(
    model="gpt-4o",
    api_key="sk-...",
    max_tokens=4000,
    temperature=0.7
)

# JSON mode example
messages = [{"role": "user", "content": "List 3 colors in JSON"}]
response = await llm.generate_content_async(
    messages,
    response_format={"type": "json_object"}
)
```

### 3. Gemini

**Models:**
- `gemini-2.0-flash` (latest, recommended)
- `gemini-1.5-pro` (most capable)
- `gemini-1.5-flash` (fast)

**API Key:** `GOOGLE_API_KEY` environment variable or `api_key` parameter

**Example:**
```python
from llm_abstractions import Gemini

llm = Gemini(
    model="gemini-2.0-flash",
    api_key="...",
    max_tokens=8192,
    temperature=0.7
)

messages = [{"role": "user", "content": "What is quantum computing?"}]
response = await llm.generate_content_async(messages)
```

### 4. HuggingFaceLlm

**Models:**
- `meta-llama/Meta-Llama-3-70B-Instruct` (recommended)
- `meta-llama/Meta-Llama-3-8B-Instruct`
- `mistralai/Mistral-7B-Instruct-v0.2`
- `mistralai/Mixtral-8x7B-Instruct-v0.1`
- `HuggingFaceH4/zephyr-7b-beta`
- `microsoft/Phi-3-mini-4k-instruct`
- `google/gemma-7b-it`

**API Key:** `HF_TOKEN` or `HUGGINGFACE_API_KEY` environment variable or `api_key` parameter

**Example:**
```python
from llm_abstractions import HuggingFaceLlm

llm = HuggingFaceLlm(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    api_key="hf_...",
    max_tokens=2048,
    temperature=0.7
)

messages = [{"role": "user", "content": "Explain transformers"}]
response = await llm.generate_content_async(messages)
```

### 5. OllamaLlm

**Models:**
- `llama3.2` (latest, recommended)
- `llama3.1`, `llama2`
- `codellama` (specialized for coding)
- `mistral`, `mixtral`
- `phi3`, `gemma2`, `qwen2.5`

**Requirements:**
- Ollama server running locally or accessible via `base_url`
- Install from: https://ollama.ai
- Default URL: `http://localhost:11434`

**Example:**
```python
from llm_abstractions import OllamaLlm

llm = OllamaLlm(
    model="llama3.2",
    base_url="http://localhost:11434"
)

messages = [{"role": "user", "content": "Write a Python function to sort a list"}]
response = await llm.generate_content_async(messages)
```

### 6. LMStudioLlm

**Models:**
- Any GGUF model loaded in LM Studio
- Popular: llama-3.2-3b-instruct, mistral-7b-instruct, codellama-7b-instruct

**Requirements:**
- LM Studio running with model loaded
- Download from: https://lmstudio.ai
- Default URL: `http://localhost:1234/v1`
- No API key required (local inference)

**Example:**
```python
from llm_abstractions import LMStudioLlm

llm = LMStudioLlm(
    model="llama-3.2-3b-instruct",
    base_url="http://localhost:1234/v1"
)

messages = [{"role": "user", "content": "Explain recursion"}]
response = await llm.generate_content_async(messages)
```

### 7. SearchAugmentedLlm

**Search Providers:**
- `duckduckgo` - DuckDuckGo search (no API key required)
- `google` - Google Custom Search (requires `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`)

**Features:**
- Auto-detection of queries needing current information
- Configurable search result injection
- Graceful degradation if search fails
- Support for any underlying LLM provider

**Example:**
```python
from llm_abstractions import SearchAugmentedLlm, OpenAILlm

# Wrap GPT-4 with search capabilities
base_llm = OpenAILlm(model="gpt-4o")
search_llm = SearchAugmentedLlm(
    llm=base_llm,
    search_provider="duckduckgo",
    auto_search=True,
    max_results=5
)

# Auto search (triggered by "latest")
messages = [{"role": "user", "content": "What's the latest on AI regulation?"}]
response = await search_llm.generate_content_async(messages)

# Manual search
response = await search_llm.generate_content_async(
    [{"role": "user", "content": "Explain AI regulation"}],
    force_search=True,
    search_query="AI regulation 2025"
)
```

## Advanced Usage

### Custom Provider Registration

```python
from llm_abstractions import LlmFactory, BaseLlm

class MyCustomLlm(BaseLlm):
    async def generate_content_async(self, messages, **kwargs):
        # Custom implementation
        return "Custom response"

# Register custom provider
LlmFactory.register_provider("my-custom-llm", MyCustomLlm)

# Use custom provider
llm = LlmFactory.get_provider("my-custom-llm")
response = await llm.generate_content_async(messages)
```

### Error Handling

```python
from llm_abstractions import LlmFactory

try:
    llm = LlmFactory.get_provider("anthropic-claude")
    response = await llm.generate_content_async(messages)
except ValueError as e:
    # Provider not registered or invalid configuration
    print(f"Configuration error: {e}")
except RuntimeError as e:
    # API call failed
    print(f"API error: {e}")
except ImportError as e:
    # SDK not installed
    print(f"Missing dependency: {e}")
```

### Parallel Execution

```python
import asyncio
from llm_abstractions import LlmFactory

# Create multiple provider instances
claude = LlmFactory.get_provider("anthropic-claude")
gpt = LlmFactory.get_provider("openai-gpt")
gemini = LlmFactory.get_provider("google-gemini")

messages = [{"role": "user", "content": "What is AI?"}]

# Execute in parallel
responses = await asyncio.gather(
    claude.generate_content_async(messages),
    gpt.generate_content_async(messages),
    gemini.generate_content_async(messages)
)

print("Claude:", responses[0])
print("GPT:", responses[1])
print("Gemini:", responses[2])
```

## Environment Variables

```bash
# Cloud/API providers
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="..."
export HF_TOKEN="hf_..."

# Local inference
export OLLAMA_BASE_URL="http://localhost:11434"
export LMSTUDIO_BASE_URL="http://localhost:1234/v1"

# Search augmentation
export GOOGLE_CSE_ID="..."  # For Google Custom Search
```

## Architecture

```
llm_abstractions/
├── base_llm.py              # BaseLlm interface
├── llm_factory.py           # Factory pattern for provider loading
├── anthropic_llm.py         # Anthropic Claude provider
├── openai_llm.py            # OpenAI GPT provider
├── gemini.py                # Google Gemini provider
├── huggingface_llm.py       # Hugging Face provider
├── ollama_llm.py            # Ollama local inference
├── lmstudio_llm.py          # LM Studio local inference
├── search_augmented_llm.py  # Search augmentation wrapper
├── __init__.py              # Package initialization
└── README.md                # This file
```

## Testing

See `tests/test_llm_abstractions.py` for comprehensive tests.

```bash
# Run tests
pytest tests/test_llm_abstractions.py -v

# Run with coverage
pytest tests/test_llm_abstractions.py --cov=llm_abstractions --cov-report=html
```

## Performance Notes

- **Async by Default**: All providers use async/await for maximum concurrency
- **Lazy Loading**: SDKs only imported when provider is used
- **Connection Pooling**: Automatic connection reuse for repeated calls
- **Timeout Handling**: Configurable timeouts for long-running requests
- **Local Inference**: Ollama and LM Studio offer 0 API cost and data privacy

## Security

- **API Keys**: Never commit API keys to version control
- **Environment Variables**: Use `.env` files (gitignored) for credentials
- **Local Inference**: Ollama and LM Studio run entirely locally (no data sent to cloud)
- **Search Privacy**: DuckDuckGo doesn't track searches (unlike Google)

## Troubleshooting

### Provider not available

**Error:** `ValueError: No LLM provider registered for agent type: xxx`

**Fix:**
```bash
# Install required SDK
pip install anthropic  # For Anthropic
pip install openai     # For OpenAI, LM Studio
pip install google-generativeai  # For Gemini
pip install huggingface-hub      # For Hugging Face
pip install aiohttp              # For Ollama
```

### Ollama connection refused

**Error:** `Failed to connect to Ollama server`

**Fix:**
1. Install Ollama from https://ollama.ai
2. Start Ollama server: `ollama serve`
3. Load a model: `ollama pull llama3.2`
4. Verify: `curl http://localhost:11434/api/tags`

### LM Studio connection refused

**Error:** `LM Studio API call failed`

**Fix:**
1. Install LM Studio from https://lmstudio.ai
2. Load a model in LM Studio UI
3. Enable "Local Server" in LM Studio
4. Verify: `curl http://localhost:1234/v1/models`

### Search augmentation not working

**Error:** `Search failed` or `DuckDuckGo search not installed`

**Fix:**
```bash
pip install duckduckgo-search

# For Google Custom Search
pip install google-api-python-client
export GOOGLE_API_KEY="..."
export GOOGLE_CSE_ID="..."
```

## Roadmap

- [ ] Add Azure OpenAI provider
- [ ] Add AWS Bedrock provider
- [ ] Add Cohere provider
- [ ] Add Together AI provider
- [ ] Add Groq provider (ultra-fast inference)
- [ ] Add vLLM local inference support
- [ ] Add streaming responses
- [ ] Add token usage tracking
- [ ] Add cost estimation
- [ ] Add retry logic with exponential backoff
- [ ] Add provider fallback chain

## Contributing

See main CODITECT contributing guidelines.

## License

Copyright © 2025 AZ1.AI INC. All rights reserved.

---

**Last Updated:** 2025-11-23
**Phase:** Phase 1C - LLM Provider Implementation
**Status:** ✅ 7 providers + search augmentation complete
