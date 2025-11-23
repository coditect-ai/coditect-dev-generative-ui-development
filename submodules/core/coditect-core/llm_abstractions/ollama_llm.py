"""
Ollama LLM - Local Inference Integration
=========================================

Ollama LLM integration for local model inference via HTTP API.

Supported Models:
- llama3.2 (Llama 3.2 - latest, recommended)
- llama3.1 (Llama 3.1)
- llama2 (Llama 2)
- codellama (Code Llama - specialized for coding)
- mistral (Mistral 7B)
- mixtral (Mixtral 8x7B)
- phi3 (Phi-3)
- gemma2 (Gemma 2)
- qwen2.5 (Qwen 2.5)

Example:
    >>> from llm_abstractions import OllamaLlm
    >>>
    >>> llm = OllamaLlm(
    ...     model="llama3.2",
    ...     base_url="http://localhost:11434"
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

import aiohttp

from .base_llm import BaseLlm


class OllamaLlm(BaseLlm):
    """
    Ollama LLM integration for local inference.

    Uses Ollama HTTP API for async content generation with local models.

    Attributes:
        model: Ollama model name
        base_url: Ollama API base URL (default: http://localhost:11434)
        max_tokens: Maximum tokens in response (default: 2048)
        temperature: Sampling temperature (default: 0.7)

    Example:
        >>> llm = OllamaLlm(model="llama3.2")
        >>> response = await llm.generate_content_async(messages)
    """

    # Supported Ollama models (popular ones)
    SUPPORTED_MODELS = [
        "llama3.2",      # Llama 3.2 (latest, recommended)
        "llama3.1",      # Llama 3.1
        "llama2",        # Llama 2
        "codellama",     # Code Llama (specialized for coding)
        "mistral",       # Mistral 7B
        "mixtral",       # Mixtral 8x7B
        "phi3",          # Phi-3
        "gemma2",        # Gemma 2
        "qwen2.5",       # Qwen 2.5
    ]

    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs: Any
    ):
        """
        Initialize Ollama LLM.

        Args:
            model: Ollama model name (default: llama3.2)
            base_url: Ollama API URL (default: http://localhost:11434)
            max_tokens: Maximum tokens in response (default: 2048)
            temperature: Sampling temperature 0.0-2.0 (default: 0.7)
            **kwargs: Additional configuration

        Note:
            Requires Ollama server running locally or accessible via base_url.
            Install Ollama from https://ollama.ai
        """
        self.model = model or "llama3.2"
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL") or
                         "http://localhost:11434")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.kwargs = kwargs

    async def generate_content_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> str:
        """
        Generate content using Ollama.

        Args:
            messages: List of messages in format:
                      [{"role": "system"|"user"|"assistant", "content": "..."}]
            **kwargs: Additional parameters (overrides defaults):
                      - max_tokens: int
                      - temperature: float
                      - top_p: float
                      - top_k: int
                      - stream: bool (default: False)

        Returns:
            Generated text response

        Raises:
            ValueError: If messages format is invalid
            RuntimeError: If API call fails or Ollama server unreachable

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

        # Prepare request payload
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": kwargs.pop("stream", False),
            "options": {
                "num_predict": kwargs.pop("max_tokens", self.max_tokens),
                "temperature": kwargs.pop("temperature", self.temperature),
                "top_p": kwargs.pop("top_p", 0.9),
                "top_k": kwargs.pop("top_k", 40),
            }
        }

        try:
            # Call Ollama API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=600)  # 10 min timeout
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(
                            f"Ollama API returned status {response.status}: {error_text}"
                        )

                    result = await response.json()

                    # Extract text from response
                    if "message" in result and "content" in result["message"]:
                        return result["message"]["content"]

                    return ""

        except aiohttp.ClientError as e:
            raise RuntimeError(
                f"Failed to connect to Ollama server at {self.base_url}. "
                f"Ensure Ollama is running.\nError: {e}"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Ollama API call failed for model {self.model}: {e}"
            ) from e

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"OllamaLlm(model={self.model!r}, "
            f"base_url={self.base_url!r}, "
            f"max_tokens={self.max_tokens}, "
            f"temperature={self.temperature})"
        )
