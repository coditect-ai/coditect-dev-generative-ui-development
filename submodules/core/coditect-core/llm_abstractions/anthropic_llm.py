"""
Anthropic LLM - Official SDK Integration
========================================

Anthropic Claude LLM integration using official AsyncAnthropic SDK.

Supported Models:
- claude-3-5-sonnet-20241022 (Sonnet 3.5 - latest, recommended)
- claude-3-5-haiku-20241022 (Haiku 3.5 - fast)
- claude-3-opus-20240229 (Opus 3 - most capable)
- claude-3-sonnet-20240229 (Sonnet 3)
- claude-3-haiku-20240307 (Haiku 3)

Example:
    >>> from llm_abstractions import AnthropicLlm
    >>>
    >>> llm = AnthropicLlm(
    ...     model="claude-3-5-sonnet-20241022",
    ...     api_key="sk-ant-..."
    ... )
    >>>
    >>> messages = [{"role": "user", "content": "Hello!"}]
    >>> response = await llm.generate_content_async(messages)
    >>> print(response)

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

import os
from typing import Any, Dict, List, Optional

from .base_llm import BaseLlm


class AnthropicLlm(BaseLlm):
    """
    Anthropic Claude LLM integration.

    Uses official AsyncAnthropic SDK for async content generation.

    Attributes:
        model: Claude model name
        api_key: Anthropic API key
        client: AsyncAnthropic client instance
        max_tokens: Maximum tokens in response (default: 4096)
        temperature: Sampling temperature (default: 0.7)

    Example:
        >>> llm = AnthropicLlm(model="claude-3-5-sonnet-20241022")
        >>> response = await llm.generate_content_async(messages)
    """

    # Supported Claude models
    SUPPORTED_MODELS = [
        "claude-3-5-sonnet-20241022",  # Sonnet 3.5 (latest, recommended)
        "claude-3-5-haiku-20241022",   # Haiku 3.5 (fast)
        "claude-3-opus-20240229",      # Opus 3 (most capable)
        "claude-3-sonnet-20240229",    # Sonnet 3
        "claude-3-haiku-20240307",     # Haiku 3
    ]

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any
    ):
        """
        Initialize Anthropic LLM.

        Args:
            model: Claude model name (default: claude-3-5-sonnet-20241022)
            api_key: Anthropic API key (uses ANTHROPIC_API_KEY env var if not provided)
            max_tokens: Maximum tokens in response (default: 4096)
            temperature: Sampling temperature 0.0-1.0 (default: 0.7)
            **kwargs: Additional SDK configuration

        Raises:
            ValueError: If API key not provided and not in environment
            ImportError: If anthropic SDK not installed
        """
        self.model = model or "claude-3-5-sonnet-20241022"
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs

        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment "
                "variable or pass api_key parameter."
            )

        # Lazy import to allow module loading without SDK installed
        try:
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=self.api_key, **kwargs)
        except ImportError as e:
            raise ImportError(
                "Anthropic SDK not installed. Install with:\n"
                "  pip install anthropic\n"
                f"Original error: {e}"
            ) from e

    async def generate_content_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> str:
        """
        Generate content using Claude.

        Args:
            messages: List of messages in format:
                      [{"role": "user"|"assistant", "content": "..."}]
            **kwargs: Additional parameters (overrides defaults):
                      - max_tokens: int
                      - temperature: float
                      - top_p: float
                      - top_k: int
                      - system: str (system prompt)

        Returns:
            Generated text response

        Raises:
            ValueError: If messages format is invalid
            RuntimeError: If API call fails

        Example:
            >>> messages = [
            ...     {"role": "user", "content": "What is 2+2?"}
            ... ]
            >>> response = await llm.generate_content_async(messages)
        """
        # Validate messages
        if not messages:
            raise ValueError("Messages list cannot be empty")

        # Extract system prompt if present
        system_prompt = kwargs.pop("system", None)
        filtered_messages = []

        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")

            if not role or not content:
                raise ValueError(f"Invalid message format: {msg}")

            # Handle system messages
            if role == "system":
                system_prompt = content
            else:
                filtered_messages.append({"role": role, "content": content})

        # Merge kwargs with defaults
        params = {
            "max_tokens": kwargs.pop("max_tokens", self.max_tokens),
            "temperature": kwargs.pop("temperature", self.temperature),
            **kwargs  # Include any additional parameters
        }

        # Add system prompt if present
        if system_prompt:
            params["system"] = system_prompt

        try:
            # Call Anthropic API
            response = await self.client.messages.create(
                model=self.model,
                messages=filtered_messages,
                **params
            )

            # Extract text from response
            if response.content and len(response.content) > 0:
                return response.content[0].text

            return ""

        except Exception as e:
            raise RuntimeError(
                f"Anthropic API call failed for model {self.model}: {e}"
            ) from e

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"AnthropicLlm(model={self.model!r}, "
            f"max_tokens={self.max_tokens}, "
            f"temperature={self.temperature})"
        )
