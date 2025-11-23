"""
Google Gemini LLM - Official SDK Integration
============================================

Google Gemini LLM integration using official google-generativeai SDK.

Supported Models:
- gemini-2.0-flash (Gemini 2.0 Flash - latest, recommended)
- gemini-1.5-pro (Gemini 1.5 Pro - most capable)
- gemini-1.5-flash (Gemini 1.5 Flash - fast)

Example:
    >>> from llm_abstractions import Gemini
    >>>
    >>> llm = Gemini(
    ...     model="gemini-2.0-flash",
    ...     api_key="..."
    ... )
    >>>
    >>> messages = [{"role": "user", "content": "Hello!"}]
    >>> response = await llm.generate_content_async(messages)
    >>> print(response)

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

import asyncio
import os
from typing import Any, Dict, List, Optional

from .base_llm import BaseLlm


class Gemini(BaseLlm):
    """
    Google Gemini LLM integration.

    Uses official google-generativeai SDK for async content generation.

    Attributes:
        model: Gemini model name
        api_key: Google API key
        client: Gemini client instance
        max_tokens: Maximum tokens in response (default: 8192)
        temperature: Sampling temperature (default: 0.7)

    Example:
        >>> llm = Gemini(model="gemini-2.0-flash")
        >>> response = await llm.generate_content_async(messages)
    """

    # Supported Gemini models
    SUPPORTED_MODELS = [
        "gemini-2.0-flash",    # Gemini 2.0 Flash (latest, recommended)
        "gemini-1.5-pro",      # Gemini 1.5 Pro (most capable)
        "gemini-1.5-flash",    # Gemini 1.5 Flash (fast)
    ]

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        max_tokens: int = 8192,
        temperature: float = 0.7,
        **kwargs: Any
    ):
        """
        Initialize Gemini LLM.

        Args:
            model: Gemini model name (default: gemini-2.0-flash)
            api_key: Google API key (uses GOOGLE_API_KEY env var if not provided)
            max_tokens: Maximum tokens in response (default: 8192)
            temperature: Sampling temperature 0.0-2.0 (default: 0.7)
            **kwargs: Additional SDK configuration

        Raises:
            ValueError: If API key not provided and not in environment
            ImportError: If google-generativeai SDK not installed
        """
        self.model = model or "gemini-2.0-flash"
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs

        if not self.api_key:
            raise ValueError(
                "Google API key required. Set GOOGLE_API_KEY environment "
                "variable or pass api_key parameter."
            )

        # Lazy import to allow module loading without SDK installed
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        except ImportError as e:
            raise ImportError(
                "Google Generative AI SDK not installed. Install with:\n"
                "  pip install google-generativeai\n"
                f"Original error: {e}"
            ) from e

    async def generate_content_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> str:
        """
        Generate content using Gemini.

        Args:
            messages: List of messages in format:
                      [{"role": "user"|"model", "content": "..."}]
            **kwargs: Additional parameters (overrides defaults):
                      - max_tokens: int
                      - temperature: float
                      - top_p: float
                      - top_k: int

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

        # Convert messages to Gemini format
        # Gemini uses simple prompt for now (can be enhanced with chat history)
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if not content:
                raise ValueError(f"Invalid message format: {msg}")

            # Build conversational prompt
            if role in ("user", "human"):
                prompt += f"User: {content}\n\n"
            elif role in ("assistant", "model", "ai"):
                prompt += f"Assistant: {content}\n\n"
            else:
                prompt += f"{content}\n\n"

        # Merge kwargs with defaults
        generation_config = {
            "max_output_tokens": kwargs.pop("max_tokens", self.max_tokens),
            "temperature": kwargs.pop("temperature", self.temperature),
            **kwargs
        }

        try:
            # Call Gemini API (run in thread pool for async compatibility)
            response = await asyncio.to_thread(
                self.client.generate_content,
                prompt,
                generation_config=generation_config
            )

            # Extract text from response
            if response.text:
                return response.text

            return ""

        except Exception as e:
            raise RuntimeError(
                f"Gemini API call failed for model {self.model}: {e}"
            ) from e

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Gemini(model={self.model!r}, "
            f"max_tokens={self.max_tokens}, "
            f"temperature={self.temperature})"
        )

