"""
LM Studio LLM - Local Inference Integration
===========================================

LM Studio LLM integration for local model inference via OpenAI-compatible API.

Supported Models:
- Any GGUF model loaded in LM Studio
- Llama 3.2, Llama 3.1, Llama 2
- Mistral, Mixtral
- Phi-3, Gemma 2
- Code Llama, DeepSeek Coder
- Qwen 2.5

Example:
    >>> from llm_abstractions import LMStudioLlm
    >>>
    >>> llm = LMStudioLlm(
    ...     model="llama-3.2-3b-instruct",
    ...     base_url="http://localhost:1234/v1"
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


class LMStudioLlm(BaseLlm):
    """
    LM Studio LLM integration for local inference.

    Uses OpenAI-compatible API provided by LM Studio for async content generation
    with locally loaded GGUF models.

    Attributes:
        model: Model identifier (must match loaded model in LM Studio)
        base_url: LM Studio API base URL (default: http://localhost:1234/v1)
        client: AsyncOpenAI client instance
        max_tokens: Maximum tokens in response (default: 2048)
        temperature: Sampling temperature (default: 0.7)

    Example:
        >>> llm = LMStudioLlm(model="llama-3.2-3b-instruct")
        >>> response = await llm.generate_content_async(messages)
    """

    # Popular GGUF models for LM Studio (examples)
    SUPPORTED_MODELS = [
        "llama-3.2-3b-instruct",
        "llama-3.1-8b-instruct",
        "mistral-7b-instruct",
        "phi-3-mini-4k-instruct",
        "gemma-2-9b-it",
        "codellama-7b-instruct",
        "deepseek-coder-6.7b-instruct",
        "qwen2.5-7b-instruct",
    ]

    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,  # Accepted but ignored
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs: Any
    ):
        """
        Initialize LM Studio LLM.

        Args:
            model: Model name (must match loaded model in LM Studio)
                   Use "local-model" or actual model name from LM Studio
            base_url: LM Studio API URL (default: http://localhost:1234/v1)
            api_key: API key (accepted but ignored for local inference)
            max_tokens: Maximum tokens in response (default: 2048)
            temperature: Sampling temperature 0.0-2.0 (default: 0.7)
            **kwargs: Additional OpenAI SDK configuration

        Note:
            Requires LM Studio running with a model loaded.
            Download from https://lmstudio.ai
            API key is not required for local inference.
        """
        self.model = model or "local-model"  # LM Studio default
        self.base_url = (base_url or
                         os.getenv("LMSTUDIO_BASE_URL") or
                         "http://localhost:1234/v1")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs
        # Ignore api_key for local inference

        # Lazy import to allow module loading without SDK installed
        try:
            from openai import AsyncOpenAI
            # LM Studio doesn't require API key
            self.client = AsyncOpenAI(
                base_url=self.base_url,
                api_key="lm-studio",  # Dummy key (not used)
                **kwargs
            )
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
        Generate content using LM Studio.

        Args:
            messages: List of messages in format:
                      [{"role": "system"|"user"|"assistant", "content": "..."}]
            **kwargs: Additional parameters (overrides defaults):
                      - max_tokens: int
                      - temperature: float
                      - top_p: float
                      - frequency_penalty: float
                      - presence_penalty: float
                      - stream: bool (default: False)

        Returns:
            Generated text response

        Raises:
            ValueError: If messages format is invalid
            RuntimeError: If API call fails or LM Studio server unreachable

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
            "top_p": kwargs.pop("top_p", 0.95),
            "stream": kwargs.pop("stream", False),
            **kwargs  # Include any additional parameters
        }

        try:
            # Call LM Studio API (OpenAI-compatible)
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
                f"LM Studio API call failed for model {self.model}. "
                f"Ensure LM Studio is running with a model loaded at {self.base_url}.\n"
                f"Error: {e}"
            ) from e

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"LMStudioLlm(model={self.model!r}, "
            f"base_url={self.base_url!r}, "
            f"max_tokens={self.max_tokens}, "
            f"temperature={self.temperature})"
        )
