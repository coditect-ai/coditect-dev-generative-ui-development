"""
LLM Factory - Dynamic Provider Loading
======================================

Factory for creating LLM provider instances based on agent type.

Features:
- Dynamic provider registration
- AgentType-based provider lookup
- Configuration injection
- Custom provider support

Example:
    >>> from llm_abstractions import LlmFactory
    >>> from orchestration.agent_registry import AgentType
    >>>
    >>> # Get provider instance
    >>> llm = LlmFactory.get_provider(
    ...     agent_type=AgentType.ANTHROPIC_CLAUDE,
    ...     model="claude-3-5-sonnet-20241022",
    ...     api_key="sk-..."
    ... )
    >>>
    >>> # Generate content
    >>> messages = [{"role": "user", "content": "Hello!"}]
    >>> response = await llm.generate_content_async(messages)

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

import os
from typing import Dict, Type, Any, Optional

from .base_llm import BaseLlm


class LlmFactory:
    """
    Factory for creating LLM provider instances.

    Provides dynamic provider registration and instantiation based on
    agent type with configuration injection.

    Attributes:
        _providers: Dict mapping AgentType to BaseLlm implementation class

    Example:
        >>> llm = LlmFactory.get_provider(AgentType.ANTHROPIC_CLAUDE)
        >>> response = await llm.generate_content_async(messages)
    """

    _providers: Dict[str, Type[BaseLlm]] = {}

    @classmethod
    def register_provider(
        cls,
        agent_type: str,
        provider_class: Type[BaseLlm]
    ) -> None:
        """
        Register custom LLM provider.

        Args:
            agent_type: Agent type identifier (e.g., "anthropic-claude")
            provider_class: BaseLlm implementation class

        Raises:
            TypeError: If provider_class is not a BaseLlm subclass

        Example:
            >>> class MyCustomLlm(BaseLlm):
            ...     async def generate_content_async(self, messages, **kwargs):
            ...         return "Custom response"
            >>>
            >>> LlmFactory.register_provider("custom-llm", MyCustomLlm)
        """
        if not issubclass(provider_class, BaseLlm):
            raise TypeError(f"{provider_class} must be a subclass of BaseLlm")

        cls._providers[agent_type] = provider_class
        print(f"✅ Registered LLM provider: {agent_type} → {provider_class.__name__}")

    @classmethod
    def get_provider(
        cls,
        agent_type: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs: Any
    ) -> BaseLlm:
        """
        Get LLM provider instance for agent type.

        Args:
            agent_type: Agent type identifier (e.g., "anthropic-claude")
            model: Model name (provider-specific)
            api_key: API key (uses environment variable if not provided)
            **kwargs: Additional configuration for LLM provider

        Returns:
            Configured BaseLlm instance

        Raises:
            ValueError: If agent type not supported
            RuntimeError: If provider not registered yet

        Example:
            >>> llm = LlmFactory.get_provider(
            ...     agent_type="anthropic-claude",
            ...     model="claude-3-5-sonnet-20241022",
            ...     temperature=0.7
            ... )
        """
        # Lazy load providers on first use
        if not cls._providers:
            cls._register_default_providers()

        # Get provider class
        provider_class = cls._providers.get(agent_type)
        if not provider_class:
            available = ", ".join(cls._providers.keys())
            raise ValueError(
                f"No LLM provider registered for agent type: {agent_type}\n"
                f"Available providers: {available}\n"
                f"Use LlmFactory.register_provider() to add custom providers"
            )

        # Instantiate provider with configuration
        try:
            return provider_class(model=model, api_key=api_key, **kwargs)
        except Exception as e:
            raise RuntimeError(
                f"Failed to instantiate {provider_class.__name__}: {e}"
            ) from e

    @classmethod
    def _register_default_providers(cls) -> None:
        """
        Register default LLM providers.

        Called automatically on first get_provider() call.
        Registers: Anthropic, OpenAI, Gemini, Ollama, HuggingFace, LMStudio.
        """
        # Import here to avoid circular dependencies

        # Cloud/API providers
        try:
            from .anthropic_llm import AnthropicLlm
            cls._providers["anthropic-claude"] = AnthropicLlm
        except ImportError:
            print("⚠️  AnthropicLlm not available (install anthropic SDK)")

        try:
            from .openai_llm import OpenAILlm
            cls._providers["openai-gpt"] = OpenAILlm
        except ImportError:
            print("⚠️  OpenAILlm not available (install openai SDK)")

        try:
            from .gemini import Gemini
            cls._providers["google-gemini"] = Gemini
        except ImportError:
            print("⚠️  Gemini not available (install google-generativeai SDK)")

        try:
            from .huggingface_llm import HuggingFaceLlm
            cls._providers["huggingface"] = HuggingFaceLlm
        except ImportError:
            print("⚠️  HuggingFaceLlm not available (install huggingface_hub SDK)")

        # Local inference providers
        try:
            from .ollama_llm import OllamaLlm
            cls._providers["ollama"] = OllamaLlm
        except ImportError:
            print("⚠️  OllamaLlm not available (install aiohttp SDK)")

        try:
            from .lmstudio_llm import LMStudioLlm
            cls._providers["lmstudio"] = LMStudioLlm
        except ImportError:
            print("⚠️  LMStudioLlm not available (install openai SDK)")

    @classmethod
    def list_providers(cls) -> Dict[str, Type[BaseLlm]]:
        """
        List all registered providers.

        Returns:
            Dict mapping agent_type to provider class

        Example:
            >>> providers = LlmFactory.list_providers()
            >>> for agent_type, provider_class in providers.items():
            ...     print(f"{agent_type}: {provider_class.__name__}")
        """
        if not cls._providers:
            cls._register_default_providers()

        return cls._providers.copy()

    @classmethod
    def is_provider_available(cls, agent_type: str) -> bool:
        """
        Check if provider is available for agent type.

        Args:
            agent_type: Agent type identifier

        Returns:
            True if provider is registered

        Example:
            >>> if LlmFactory.is_provider_available("anthropic-claude"):
            ...     llm = LlmFactory.get_provider("anthropic-claude")
        """
        if not cls._providers:
            cls._register_default_providers()

        return agent_type in cls._providers
