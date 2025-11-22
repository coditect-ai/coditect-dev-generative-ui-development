"""
Agent Registry - LLM Abstraction Layer
======================================

Universal AI agent registry supporting multiple LLMs (Claude, GPT, Gemini, Llama, custom).

Features:
- ✅ LLM-Agnostic (works with any AI agent)
- ✅ Pluggable Backends (Claude, GPT, Gemini, custom)
- ✅ Agent Capabilities (track what each agent can do)
- ✅ Interface Abstraction (Task tool, API, CLI)
- ✅ Configuration Management (API keys, models, endpoints)

Example:
    >>> from claude.orchestration import AgentRegistry, AgentType, AgentInterface
    >>>
    >>> registry = AgentRegistry()
    >>>
    >>> # Register Claude agent
    >>> registry.register_agent(
    ...     name="claude-code",
    ...     agent_type=AgentType.ANTHROPIC_CLAUDE,
    ...     interface=AgentInterface.TASK_TOOL,
    ...     capabilities=["code", "research", "design"]
    ... )
    >>>
    >>> # Register GPT-4 agent
    >>> registry.register_agent(
    ...     name="gpt-4",
    ...     agent_type=AgentType.OPENAI_GPT,
    ...     interface=AgentInterface.API,
    ...     api_key=os.getenv("OPENAI_API_KEY"),
    ...     model="gpt-4"
    ... )
    >>>
    >>> # Get agent
    >>> agent = registry.get_agent("claude-code")
    >>> print(agent.capabilities)

Copyright © 2025 AZ1.AI INC. All rights reserved.
Developer: Hal Casteel, CEO/CTO
Email: 1@az1.ai
"""

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class AgentType(str, Enum):
    """Types of AI agents supported."""

    ANTHROPIC_CLAUDE = "anthropic-claude"  # Claude (Sonnet, Opus, Haiku)
    OPENAI_GPT = "openai-gpt"              # GPT-4, GPT-3.5, etc.
    GOOGLE_GEMINI = "google-gemini"        # Gemini Pro, Ultra
    META_LLAMA = "meta-llama"              # Llama 2, 3, etc.
    CUSTOM = "custom"                      # Custom LLM endpoint


class AgentInterface(str, Enum):
    """How to interact with the agent."""

    TASK_TOOL = "task-tool"      # Claude Code Task tool (interactive)
    API = "api"                  # Direct API calls (REST/gRPC)
    CLI = "cli"                  # Command-line interface
    HYBRID = "hybrid"            # Multiple interfaces


class AgentCapability(str, Enum):
    """What the agent can do."""

    CODE = "code"                # Code generation, editing
    RESEARCH = "research"        # Web search, document analysis
    DESIGN = "design"            # Architecture, system design
    TESTING = "testing"          # Test generation, QA
    DEPLOYMENT = "deployment"    # CI/CD, infrastructure
    DOCUMENTATION = "documentation"  # Docs, diagrams
    ANALYSIS = "analysis"        # Data analysis, metrics
    PLANNING = "planning"        # Project planning, roadmaps


@dataclass
class AgentConfig:
    """
    Configuration for an AI agent.

    Attributes:
        name: Agent identifier (e.g., "claude-code", "gpt-4")
        agent_type: Type of LLM
        interface: How to interact with agent
        capabilities: What agent can do
        model: Specific model name (e.g., "claude-sonnet-4")
        api_key: API key for authentication (optional)
        api_endpoint: Custom API endpoint (optional)
        max_tokens: Maximum tokens per request
        temperature: Sampling temperature (0-1)
        metadata: Additional configuration
        enabled: Whether agent is currently enabled
    """

    name: str
    agent_type: AgentType
    interface: AgentInterface
    capabilities: List[AgentCapability] = field(default_factory=list)
    model: str = ""
    api_key: Optional[str] = None
    api_endpoint: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.7
    metadata: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True

    def __post_init__(self):
        """Validate configuration."""
        if not self.name:
            raise ValueError("Agent name is required")

        # Auto-detect API key from environment if not provided
        if self.api_key is None and self.interface == AgentInterface.API:
            env_var_map = {
                AgentType.ANTHROPIC_CLAUDE: "ANTHROPIC_API_KEY",
                AgentType.OPENAI_GPT: "OPENAI_API_KEY",
                AgentType.GOOGLE_GEMINI: "GOOGLE_API_KEY",
            }
            env_var = env_var_map.get(self.agent_type)
            if env_var:
                self.api_key = os.getenv(env_var)

    def supports_capability(self, capability: AgentCapability) -> bool:
        """Check if agent supports a specific capability."""
        return capability in self.capabilities

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "agent_type": self.agent_type.value,
            "interface": self.interface.value,
            "capabilities": [c.value for c in self.capabilities],
            "model": self.model,
            "api_endpoint": self.api_endpoint,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "metadata": self.metadata,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AgentConfig":
        """Deserialize from dictionary."""
        # Convert enums
        if "agent_type" in data and isinstance(data["agent_type"], str):
            data["agent_type"] = AgentType(data["agent_type"])

        if "interface" in data and isinstance(data["interface"], str):
            data["interface"] = AgentInterface(data["interface"])

        if "capabilities" in data:
            data["capabilities"] = [
                AgentCapability(c) if isinstance(c, str) else c
                for c in data["capabilities"]
            ]

        return cls(**data)


class AgentRegistry:
    """
    Universal AI agent registry.

    Manages multiple LLM agents with different capabilities and interfaces.
    Provides agent discovery, selection, and configuration.

    Example:
        >>> registry = AgentRegistry()
        >>>
        >>> # Register agents
        >>> registry.register_agent(
        ...     name="claude-code",
        ...     agent_type=AgentType.ANTHROPIC_CLAUDE,
        ...     interface=AgentInterface.TASK_TOOL
        ... )
        >>>
        >>> # Find agents by capability
        >>> code_agents = registry.find_agents_by_capability(AgentCapability.CODE)
        >>>
        >>> # Get recommended agent for task
        >>> agent = registry.get_recommended_agent(
        ...     required_capabilities=[AgentCapability.CODE, AgentCapability.TESTING]
        ... )
    """

    def __init__(self):
        """Initialize empty agent registry."""
        self.agents: Dict[str, AgentConfig] = {}

    def register_agent(
        self,
        name: str,
        agent_type: AgentType,
        interface: AgentInterface,
        capabilities: Optional[List[AgentCapability]] = None,
        **kwargs
    ) -> AgentConfig:
        """
        Register a new agent.

        Args:
            name: Agent identifier
            agent_type: Type of LLM
            interface: How to interact with agent
            capabilities: What agent can do
            **kwargs: Additional configuration (model, api_key, etc.)

        Returns:
            AgentConfig instance

        Raises:
            ValueError: If agent already registered
        """
        if name in self.agents:
            raise ValueError(f"Agent '{name}' already registered")

        config = AgentConfig(
            name=name,
            agent_type=agent_type,
            interface=interface,
            capabilities=capabilities or [],
            **kwargs
        )

        self.agents[name] = config
        return config

    def get_agent(self, name: str) -> Optional[AgentConfig]:
        """
        Get agent by name.

        Args:
            name: Agent identifier

        Returns:
            AgentConfig if found, None otherwise
        """
        return self.agents.get(name)

    def list_agents(self, enabled_only: bool = True) -> List[AgentConfig]:
        """
        List all registered agents.

        Args:
            enabled_only: Only return enabled agents

        Returns:
            List of AgentConfig instances
        """
        agents = list(self.agents.values())

        if enabled_only:
            agents = [a for a in agents if a.enabled]

        return agents

    def find_agents_by_capability(
        self,
        capability: AgentCapability,
        enabled_only: bool = True
    ) -> List[AgentConfig]:
        """
        Find agents that support a specific capability.

        Args:
            capability: Required capability
            enabled_only: Only return enabled agents

        Returns:
            List of matching agents
        """
        agents = self.list_agents(enabled_only=enabled_only)
        return [a for a in agents if a.supports_capability(capability)]

    def find_agents_by_type(
        self,
        agent_type: AgentType,
        enabled_only: bool = True
    ) -> List[AgentConfig]:
        """
        Find agents of a specific type.

        Args:
            agent_type: Type of LLM
            enabled_only: Only return enabled agents

        Returns:
            List of matching agents
        """
        agents = self.list_agents(enabled_only=enabled_only)
        return [a for a in agents if a.agent_type == agent_type]

    def get_recommended_agent(
        self,
        required_capabilities: List[AgentCapability],
        preferred_types: Optional[List[AgentType]] = None,
        fallback: str = "claude-code"
    ) -> Optional[AgentConfig]:
        """
        Get recommended agent for a task based on requirements.

        Selection criteria:
        1. Must support all required capabilities
        2. Prefer agents of specified types
        3. Prefer agents with more capabilities (more versatile)
        4. Fall back to specified default agent

        Args:
            required_capabilities: Required capabilities
            preferred_types: Preferred agent types (optional)
            fallback: Fallback agent name if no match

        Returns:
            Recommended AgentConfig, or None if no suitable agent
        """
        # Find agents with all required capabilities
        candidates = []
        for agent in self.list_agents(enabled_only=True):
            if all(agent.supports_capability(cap) for cap in required_capabilities):
                candidates.append(agent)

        if not candidates:
            # No agent supports all capabilities, try fallback
            return self.get_agent(fallback)

        # Filter by preferred types if specified
        if preferred_types:
            preferred = [a for a in candidates if a.agent_type in preferred_types]
            if preferred:
                candidates = preferred

        # Sort by number of capabilities (more versatile = better)
        candidates.sort(key=lambda a: len(a.capabilities), reverse=True)

        return candidates[0]

    def enable_agent(self, name: str) -> bool:
        """Enable an agent."""
        agent = self.get_agent(name)
        if agent:
            agent.enabled = True
            return True
        return False

    def disable_agent(self, name: str) -> bool:
        """Disable an agent."""
        agent = self.get_agent(name)
        if agent:
            agent.enabled = False
            return True
        return False

    def unregister_agent(self, name: str) -> bool:
        """
        Remove an agent from registry.

        Args:
            name: Agent identifier

        Returns:
            True if removed, False if not found
        """
        if name in self.agents:
            del self.agents[name]
            return True
        return False


# Pre-configured agent templates

def create_claude_code_agent(name: str = "claude-code") -> AgentConfig:
    """Create Claude Code agent configuration."""
    return AgentConfig(
        name=name,
        agent_type=AgentType.ANTHROPIC_CLAUDE,
        interface=AgentInterface.TASK_TOOL,
        model="claude-sonnet-4",
        capabilities=[
            AgentCapability.CODE,
            AgentCapability.RESEARCH,
            AgentCapability.DESIGN,
            AgentCapability.TESTING,
            AgentCapability.DOCUMENTATION,
            AgentCapability.ANALYSIS,
            AgentCapability.PLANNING,
        ],
        max_tokens=8000,
        temperature=0.7,
    )


def create_gpt4_agent(
    name: str = "gpt-4",
    api_key: Optional[str] = None
) -> AgentConfig:
    """Create GPT-4 agent configuration."""
    return AgentConfig(
        name=name,
        agent_type=AgentType.OPENAI_GPT,
        interface=AgentInterface.API,
        model="gpt-4",
        api_key=api_key,
        api_endpoint="https://api.openai.com/v1/chat/completions",
        capabilities=[
            AgentCapability.CODE,
            AgentCapability.RESEARCH,
            AgentCapability.DESIGN,
            AgentCapability.DOCUMENTATION,
            AgentCapability.ANALYSIS,
        ],
        max_tokens=4000,
        temperature=0.7,
    )


def create_gemini_agent(
    name: str = "gemini-pro",
    api_key: Optional[str] = None
) -> AgentConfig:
    """Create Gemini Pro agent configuration."""
    return AgentConfig(
        name=name,
        agent_type=AgentType.GOOGLE_GEMINI,
        interface=AgentInterface.API,
        model="gemini-pro",
        api_key=api_key,
        api_endpoint="https://generativelanguage.googleapis.com/v1/models",
        capabilities=[
            AgentCapability.CODE,
            AgentCapability.RESEARCH,
            AgentCapability.ANALYSIS,
        ],
        max_tokens=4000,
        temperature=0.7,
    )
