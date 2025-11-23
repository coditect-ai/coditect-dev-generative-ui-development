"""
Search-Augmented LLM - Web Search Integration
=============================================

Web search augmentation wrapper for any LLM provider.

Implements search-augmented generation (RAG with web search) by:
1. Analyzing user query to determine if search is needed
2. Performing web search using DuckDuckGo or Google
3. Injecting search results into LLM context
4. Generating response with grounded, up-to-date information

Example:
    >>> from llm_abstractions import SearchAugmentedLlm, AnthropicLlm
    >>>
    >>> base_llm = AnthropicLlm(model="claude-3-5-sonnet-20241022")
    >>> search_llm = SearchAugmentedLlm(
    ...     llm=base_llm,
    ...     search_provider="duckduckgo"
    ... )
    >>>
    >>> messages = [{"role": "user", "content": "What's the latest on GPT-5?"}]
    >>> response = await search_llm.generate_content_async(messages)
    >>> print(response)  # Response grounded in recent search results

Copyright © 2025 AZ1.AI INC. All rights reserved.
Phase: Phase 1C - LLM Provider Implementation
"""

import re
from typing import Any, Dict, List, Optional

from .base_llm import BaseLlm


class SearchAugmentedLlm(BaseLlm):
    """
    Search-augmented LLM wrapper.

    Adds web search capabilities to any LLM provider for grounded,
    up-to-date responses.

    Attributes:
        llm: Underlying LLM provider
        search_provider: Search provider ("duckduckgo" or "google")
        auto_search: Automatically search for queries needing current info
        max_results: Maximum search results to include (default: 5)

    Example:
        >>> base_llm = OpenAILlm(model="gpt-4")
        >>> search_llm = SearchAugmentedLlm(llm=base_llm)
        >>> response = await search_llm.generate_content_async(messages)
    """

    # Keywords indicating need for current information
    SEARCH_TRIGGERS = [
        "latest", "recent", "current", "today", "news", "update",
        "what's new", "what is new", "right now", "this week",
        "this month", "this year", "2024", "2025", "2026"
    ]

    def __init__(
        self,
        llm: BaseLlm,
        search_provider: str = "duckduckgo",
        auto_search: bool = True,
        max_results: int = 5,
        **kwargs: Any
    ):
        """
        Initialize search-augmented LLM.

        Args:
            llm: Base LLM provider to augment with search
            search_provider: Search provider ("duckduckgo" or "google")
            auto_search: Auto-detect queries needing search (default: True)
            max_results: Max search results to include (default: 5)
            **kwargs: Additional configuration

        Raises:
            ImportError: If search dependencies not installed
        """
        self.llm = llm
        self.search_provider = search_provider
        self.auto_search = auto_search
        self.max_results = max_results
        self.kwargs = kwargs

        # Lazy import search dependencies
        if search_provider == "duckduckgo":
            try:
                from duckduckgo_search import DDGS
                self.search_client = DDGS()
            except ImportError as e:
                raise ImportError(
                    "DuckDuckGo search not installed. Install with:\n"
                    "  pip install duckduckgo-search\n"
                    f"Original error: {e}"
                ) from e
        elif search_provider == "google":
            try:
                import googleapiclient.discovery
                # Google Custom Search requires API key and Search Engine ID
                # Set via GOOGLE_API_KEY and GOOGLE_CSE_ID env vars
                self.search_client = None  # Initialized on first search
            except ImportError as e:
                raise ImportError(
                    "Google API client not installed. Install with:\n"
                    "  pip install google-api-python-client\n"
                    f"Original error: {e}"
                ) from e
        else:
            raise ValueError(
                f"Unsupported search provider: {search_provider}. "
                "Use 'duckduckgo' or 'google'"
            )

    def _should_search(self, messages: List[Dict[str, str]]) -> bool:
        """
        Determine if search should be performed for this query.

        Args:
            messages: User messages

        Returns:
            True if search is likely helpful
        """
        if not self.auto_search:
            return False

        # Check last user message for search triggers
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "").lower()

                # Check for search trigger keywords
                for trigger in self.SEARCH_TRIGGERS:
                    if trigger in content:
                        return True

                # Check for question words with time context
                if re.search(r'\b(what|when|who|where|how)\b.*\b(now|today|recent)', content):
                    return True

                break

        return False

    async def _perform_search(self, query: str) -> List[Dict[str, str]]:
        """
        Perform web search.

        Args:
            query: Search query

        Returns:
            List of search results with title, url, snippet
        """
        results = []

        try:
            if self.search_provider == "duckduckgo":
                # DuckDuckGo search
                search_results = self.search_client.text(
                    query,
                    max_results=self.max_results
                )

                for result in search_results:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", "")
                    })

            elif self.search_provider == "google":
                # Google Custom Search (requires setup)
                import os
                import googleapiclient.discovery

                api_key = os.getenv("GOOGLE_API_KEY")
                cse_id = os.getenv("GOOGLE_CSE_ID")

                if not api_key or not cse_id:
                    raise ValueError(
                        "Google search requires GOOGLE_API_KEY and GOOGLE_CSE_ID "
                        "environment variables"
                    )

                service = googleapiclient.discovery.build(
                    "customsearch", "v1", developerKey=api_key
                )

                search_results = service.cse().list(
                    q=query,
                    cx=cse_id,
                    num=self.max_results
                ).execute()

                for item in search_results.get("items", []):
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })

        except Exception as e:
            # If search fails, return empty results (graceful degradation)
            print(f"⚠️  Search failed: {e}")
            return []

        return results

    def _inject_search_context(
        self,
        messages: List[Dict[str, str]],
        search_results: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Inject search results into message context.

        Args:
            messages: Original messages
            search_results: Search results to inject

        Returns:
            Updated messages with search context
        """
        # Format search results
        context = "\n\n**Web Search Results:**\n\n"
        for i, result in enumerate(search_results, 1):
            context += f"{i}. **{result['title']}**\n"
            context += f"   {result['snippet']}\n"
            context += f"   Source: {result['url']}\n\n"

        # Find system message or create one
        augmented_messages = []
        system_added = False

        for msg in messages:
            if msg.get("role") == "system" and not system_added:
                # Append to existing system message
                augmented_messages.append({
                    "role": "system",
                    "content": msg.get("content", "") + "\n\n" + context
                })
                system_added = True
            elif msg.get("role") == "user" and not system_added:
                # Insert system message before first user message
                augmented_messages.append({
                    "role": "system",
                    "content": context
                })
                system_added = True
                augmented_messages.append(msg)
            else:
                augmented_messages.append(msg)

        # If no user message yet, prepend system message
        if not system_added:
            augmented_messages.insert(0, {
                "role": "system",
                "content": context
            })

        return augmented_messages

    async def generate_content_async(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any
    ) -> str:
        """
        Generate content with optional search augmentation.

        Args:
            messages: List of messages
            **kwargs: Additional parameters:
                      - force_search: bool (override auto_search)
                      - search_query: str (custom search query)
                      - All base LLM parameters

        Returns:
            Generated text response

        Example:
            >>> # Auto search
            >>> messages = [{"role": "user", "content": "What's the latest on AI?"}]
            >>> response = await search_llm.generate_content_async(messages)
            >>>
            >>> # Force search with custom query
            >>> response = await search_llm.generate_content_async(
            ...     messages,
            ...     force_search=True,
            ...     search_query="AI news 2025"
            ... )
        """
        force_search = kwargs.pop("force_search", False)
        search_query = kwargs.pop("search_query", None)

        # Determine if search should be performed
        should_search = force_search or self._should_search(messages)

        if should_search:
            # Extract or construct search query
            if not search_query:
                # Use last user message as query
                for msg in reversed(messages):
                    if msg.get("role") == "user":
                        search_query = msg.get("content", "")
                        break

            if search_query:
                # Perform search
                search_results = await self._perform_search(search_query)

                if search_results:
                    # Inject search context into messages
                    messages = self._inject_search_context(messages, search_results)

        # Call underlying LLM with (possibly augmented) messages
        return await self.llm.generate_content_async(messages, **kwargs)

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"SearchAugmentedLlm(llm={self.llm!r}, "
            f"search_provider={self.search_provider!r}, "
            f"auto_search={self.auto_search})"
        )
