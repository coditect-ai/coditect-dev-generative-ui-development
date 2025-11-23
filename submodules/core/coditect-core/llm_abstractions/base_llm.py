from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseLlm(ABC):
    """
    Abstract base class for all LLM implementations.
    """

    @abstractmethod
    async def generate_content_async(
        self, messages: List[Dict[str, str]], **kwargs: Any
    ) -> str:
        """
        Generate content using the LLM.

        Args:
            messages: A list of messages in the conversation history.
            **kwargs: Additional keyword arguments for the LLM.

        Returns:
            The generated content as a string.
        """
        pass
