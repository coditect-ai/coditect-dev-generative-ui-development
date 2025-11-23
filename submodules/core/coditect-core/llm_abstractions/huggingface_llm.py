"""
Hugging Face LLM - Inference API Integration
============================================

Hugging Face LLM integration using Inference API for hosted models.

Supported Models:
- meta-llama/Meta-Llama-3-70B-Instruct (Llama 3 70B - recommended)
- meta-llama/Meta-Llama-3-8B-Instruct (Llama 3 8B)
- mistralai/Mistral-7B-Instruct-v0.2 (Mistral 7B)
- mistralai/Mixtral-8x7B-Instruct-v0.1 (Mixtral 8x7B)
- HuggingFaceH4/zephyr-7b-beta (Zephyr 7B)
- microsoft/Phi-3-mini-4k-instruct (Phi-3)
- google/gemma-7b-it (Gemma 7B)

Example:
    >>> from llm_abstractions import HuggingFaceLlm
    >>>
    >>> llm = HuggingFaceLlm(
    ...     model="meta-llama/Meta-Llama-3-8B-Instruct",
    ...     api_key="hf_..."
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


class HuggingFaceLlm(BaseLlm):
    """
    Hugging Face LLM integration via Inference API.

    Uses official huggingface_hub SDK for async content generation.

    Attributes:
        model: Hugging Face model ID (e.g., meta-llama/Meta-Llama-3-8B-Instruct)
        api_key: Hugging Face API token
        client: InferenceClient instance
        max_tokens: Maximum tokens in response (default: 2048)
        temperature: Sampling temperature (default: 0.7)

    Example:
        >>> llm = HuggingFaceLlm(model="meta-llama/Meta-Llama-3-8B-Instruct")
        >>> response = await llm.generate_content_async(messages)
    """

    # Supported Hugging Face models (popular chat/instruct models)
    SUPPORTED_MODELS = [
        "meta-llama/Meta-Llama-3-70B-Instruct",     # Llama 3 70B (recommended)
        "meta-llama/Meta-Llama-3-8B-Instruct",      # Llama 3 8B
        "mistralai/Mistral-7B-Instruct-v0.2",       # Mistral 7B
        "mistralai/Mixtral-8x7B-Instruct-v0.1",     # Mixtral 8x7B
        "HuggingFaceH4/zephyr-7b-beta",             # Zephyr 7B
        "microsoft/Phi-3-mini-4k-instruct",         # Phi-3
        "google/gemma-7b-it",                       # Gemma 7B
    ]

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs: Any
    ):
        """
        Initialize Hugging Face LLM.

        Args:
            model: HF model ID (default: meta-llama/Meta-Llama-3-8B-Instruct)
            api_key: HF API token (uses HF_TOKEN or HUGGINGFACE_API_KEY env var if not provided)
            max_tokens: Maximum tokens in response (default: 2048)
            temperature: Sampling temperature 0.0-2.0 (default: 0.7)
            **kwargs: Additional SDK configuration

        Raises:
            ValueError: If API key not provided and not in environment
            ImportError: If huggingface_hub SDK not installed
        """
        self.model = model or "meta-llama/Meta-Llama-3-8B-Instruct"
        self.api_key = (api_key or
                        os.getenv("HF_TOKEN") or
                        os.getenv("HUGGINGFACE_API_KEY"))
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs

        if not self.api_key:
            raise ValueError(
                "Hugging Face API token required. Set HF_TOKEN or "
                "HUGGINGFACE_API_KEY environment variable or pass api_key parameter."
            )

        # Lazy import to allow module loading without SDK installed
        try:
            from huggingface_hub import AsyncInferenceClient
            self.client = AsyncInferenceClient(
                model=self.model,
                token=self.api_key,
                **kwargs
            )
        except ImportError as e:
            raise ImportError(
                "Hugging Face Hub SDK not installed. Install with:\n"
                "  pip install huggingface_hub\n"
                f"Original error: {e}"
            ) from e

    async def generate_content_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> str:
        """
        Generate content using Hugging Face Inference API.

        Args:
            messages: List of messages in format:
                      [{"role": "system"|"user"|"assistant", "content": "..."}]
            **kwargs: Additional parameters (overrides defaults):
                      - max_tokens: int
                      - temperature: float
                      - top_p: float
                      - repetition_penalty: float

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
            "top_p": kwargs.pop("top_p", 0.95),
            "repetition_penalty": kwargs.pop("repetition_penalty", 1.0),
            **kwargs  # Include any additional parameters
        }

        try:
            # Call Hugging Face Inference API
            response = await self.client.chat_completion(
                messages=messages,
                **params
            )

            # Extract text from response
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content or ""

            return ""

        except Exception as e:
            raise RuntimeError(
                f"Hugging Face API call failed for model {self.model}: {e}"
            ) from e

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"HuggingFaceLlm(model={self.model!r}, "
            f"max_tokens={self.max_tokens}, "
            f"temperature={self.temperature})"
        )
