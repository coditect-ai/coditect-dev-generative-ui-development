"""
LLM Abstractions - Multi-Provider LLM Integration
=================================================

Unified interface for multiple LLM providers with async support.

Providers:
- AnthropicLlm: Claude 3.5 Sonnet, Opus, Haiku
- OpenAILlm: GPT-4, GPT-4 Turbo, GPT-3.5, Codex-Max
- Gemini: Gemini 2.0 Flash, 1.5 Pro, 1.5 Flash

Example:
    >>> from llm_abstractions import LlmFactory
    >>>
    >>> # Get provider via factory
    >>> llm = LlmFactory.get_provider("anthropic-claude", model="claude-3-5-sonnet-20241022")
    >>>
    >>> # Generate content
    >>> messages = [{"role": "user", "content": "Hello!"}]
    >>> response = await llm.generate_content_async(messages)

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

from .base_llm import BaseLlm
from .llm_factory import LlmFactory

# Agent-to-LLM configuration (Phase 2A)
try:
    from .agent_llm_config import AgentLlmConfig, LlmConfig, get_agent_config
except ImportError:
    AgentLlmConfig = None
    LlmConfig = None
    get_agent_config = None

# Import providers (lazy loaded by factory)

# Cloud/API providers
try:
    from .anthropic_llm import AnthropicLlm
except ImportError:
    AnthropicLlm = None

try:
    from .openai_llm import OpenAILlm
except ImportError:
    OpenAILlm = None

try:
    from .gemini import Gemini
except ImportError:
    Gemini = None

try:
    from .huggingface_llm import HuggingFaceLlm
except ImportError:
    HuggingFaceLlm = None

# Local inference providers
try:
    from .ollama_llm import OllamaLlm
except ImportError:
    OllamaLlm = None

try:
    from .lmstudio_llm import LMStudioLlm
except ImportError:
    LMStudioLlm = None

# Search augmentation wrapper
try:
    from .search_augmented_llm import SearchAugmentedLlm
except ImportError:
    SearchAugmentedLlm = None

__all__ = [
    "BaseLlm",
    "LlmFactory",
    # Agent-to-LLM configuration (Phase 2A)
    "AgentLlmConfig",
    "LlmConfig",
    "get_agent_config",
    # Cloud/API providers
    "AnthropicLlm",
    "OpenAILlm",
    "Gemini",
    "HuggingFaceLlm",
    # Local inference providers
    "OllamaLlm",
    "LMStudioLlm",
    # Search augmentation
    "SearchAugmentedLlm",
]
