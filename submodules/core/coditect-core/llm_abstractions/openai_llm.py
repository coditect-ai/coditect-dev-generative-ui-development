"""
OpenAI LLM - Official AsyncOpenAI SDK Integration
=================================================

OpenAI GPT LLM integration using official AsyncOpenAI SDK.

Supported Models:
- gpt-4o (GPT-4 Optimized - latest, recommended)
- gpt-4-turbo (GPT-4 Turbo - fast)
- gpt-4 (GPT-4 - most capable)
- gpt-3.5-turbo (GPT-3.5 - economical)
- gpt-5.1-codex-max (Specialized coding - Nov 2025)

Example:
    >>> from llm_abstractions import OpenAILlm
    >>>
    >>> llm = OpenAILlm(
    ...     model="gpt-4o",
    ...     api_key="sk-..."
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


class OpenAILlm(BaseLlm):
    """
    OpenAI GPT LLM integration.

    Uses official AsyncOpenAI SDK for async content generation.

    Attributes:
        model: GPT model name
        api_key: OpenAI API key
        client: AsyncOpenAI client instance
        max_tokens: Maximum tokens in response (default: 4000)
        temperature: Sampling temperature (default: 0.7)

    Example:
        >>> llm = OpenAILlm(model="gpt-4o")
        >>> response = await llm.generate_content_async(messages)
    """

    # Supported GPT models
    SUPPORTED_MODELS = [
        "gpt-4o",              # GPT-4 Optimized (latest, recommended)
        "gpt-4-turbo",         # GPT-4 Turbo (fast)
        "gpt-4",               # GPT-4 (most capable)
        "gpt-3.5-turbo",       # GPT-3.5 (economical)
        "gpt-5.1-codex-max",   # Specialized coding (Nov 2025)
    ]

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        **kwargs: Any
    ):
        """
        Initialize OpenAI LLM.

        Args:
            model: GPT model name (default: gpt-4o)
                   - "gpt-4o" (default): General-purpose latest
                   - "gpt-5.1-codex-max": Specialized for coding tasks,
                     multi-hour agent loops, project-scale refactors
                   - "gpt-4", "gpt-4-turbo": Alternative models
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            max_tokens: Maximum tokens in response (default: 4000)
            temperature: Sampling temperature 0.0-2.0 (default: 0.7)
            **kwargs: Additional SDK configuration

        Raises:
            ValueError: If API key not provided and not in environment
            ImportError: If openai SDK not installed
        """
        self.model = model or "gpt-4o"
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs

        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment "
                "variable or pass api_key parameter."
            )

        # Lazy import to allow module loading without SDK installed
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=self.api_key, **kwargs)
        except ImportError as e:
            raise ImportError(
                "OpenAI SDK not installed. Install with:\n"
                "  pip install openai\n"
                f"Original error: {e}"
            ) from e

    async def generate_content_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> str:
        """
        Generate content using GPT.

        Args:
            messages: List of messages in format:
                      [{"role": "system"|"user"|"assistant", "content": "..."}]
            **kwargs: Additional parameters (overrides defaults):
                      - max_tokens: int
                      - temperature: float
                      - top_p: float
                      - frequency_penalty: float
                      - presence_penalty: float
                      - response_format: dict (for JSON mode)

        Returns:
            Generated text response

        Raises:
            ValueError: If messages format is invalid
            RuntimeError: If API call fails

        Example:
            >>> messages = [
            ...     {"role": "system", "content": "You are a helpful assistant."},
            ...     {"role": "user", "content": "What is 2+2?"}
            ... ]
            >>> response = await llm.generate_content_async(messages)
        """
        # Validate messages
        if not messages:
            raise ValueError("Messages list cannot be empty")

        # Validate message format
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")

            if not role or not content:
                raise ValueError(f"Invalid message format: {msg}")

            if role not in ("system", "user", "assistant"):
                raise ValueError(f"Invalid role: {role}")

        # Merge kwargs with defaults
        params = {
            "max_tokens": kwargs.pop("max_tokens", self.max_tokens),
            "temperature": kwargs.pop("temperature", self.temperature),
            **kwargs  # Include any additional parameters
        }

        try:
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **params
            )

            # Extract text from response
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content or ""

            return ""

        except Exception as e:
            raise RuntimeError(
                f"OpenAI API call failed for model {self.model}: {e}"
            ) from e

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"OpenAILlm(model={self.model!r}, "
            f"max_tokens={self.max_tokens}, "
            f"temperature={self.temperature})"
        )
