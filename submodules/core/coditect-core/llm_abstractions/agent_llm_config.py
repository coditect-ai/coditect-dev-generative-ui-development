"""
Agent-to-LLM Configuration Loader

Loads and manages agent-llm-bindings.yaml configuration file that maps
CODITECT agents to specific LLM providers and models.

Usage:
    from llm_abstractions import AgentLlmConfig

    config = AgentLlmConfig.get_instance()
    agent_config = config.get_agent_config("ai-specialist")

    llm = LlmFactory.get_provider(
        agent_type=agent_config.provider,
        model=agent_config.model,
        api_key=agent_config.api_key,
        max_tokens=agent_config.max_tokens,
        temperature=agent_config.temperature
    )
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:
    raise ImportError(
        "PyYAML is required for agent configuration. "
        "Install it with: pip install pyyaml"
    )


@dataclass
class LlmConfig:
    """Configuration for an LLM provider."""

    provider: str
    model: str
    api_key: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Resolve environment variables in API key."""
        if self.api_key and self.api_key.startswith("${") and self.api_key.endswith("}"):
            env_var = self.api_key[2:-1]  # Remove ${ and }
            self.api_key = os.getenv(env_var)

    def to_factory_kwargs(self) -> Dict[str, Any]:
        """Convert to kwargs for LlmFactory.get_provider()."""
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        if self.api_key:
            kwargs["api_key"] = self.api_key

        # Add provider-specific metadata
        for key, value in self.metadata.items():
            if key not in kwargs:
                kwargs[key] = value

        return kwargs


class AgentLlmConfig:
    """
    Singleton configuration loader for agent-to-LLM bindings.

    Loads agent-llm-bindings.yaml and provides agent configuration lookup.
    """

    _instance: Optional['AgentLlmConfig'] = None
    _config_path: Optional[Path] = None

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration loader.

        Args:
            config_path: Path to agent-llm-bindings.yaml file.
                        If None, searches in default locations.
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self._find_config_file()

        self.agents: Dict[str, LlmConfig] = {}
        self.defaults: Optional[LlmConfig] = None

        if self.config_path.exists():
            self._load_config()
        else:
            raise FileNotFoundError(
                f"Agent-LLM bindings config not found at {self.config_path}. "
                f"Create .coditect/config/agent-llm-bindings.yaml to configure agent bindings."
            )

    @classmethod
    def get_instance(cls, config_path: Optional[Path] = None) -> 'AgentLlmConfig':
        """
        Get singleton instance of AgentLlmConfig.

        Args:
            config_path: Optional path to config file (used on first initialization)

        Returns:
            Singleton instance
        """
        if cls._instance is None or (config_path and config_path != cls._config_path):
            cls._instance = cls(config_path)
            cls._config_path = config_path
        return cls._instance

    @classmethod
    def reload(cls) -> 'AgentLlmConfig':
        """Force reload of configuration from disk."""
        cls._instance = None
        cls._config_path = None
        return cls.get_instance()

    def _find_config_file(self) -> Path:
        """
        Find agent-llm-bindings.yaml in default locations.

        Search order:
        1. .coditect/config/agent-llm-bindings.yaml
        2. .claude/config/agent-llm-bindings.yaml
        3. ../coditect-core/.coditect/config/agent-llm-bindings.yaml (for submodules)

        Returns:
            Path to config file
        """
        # Try current directory
        candidates = [
            Path(".coditect/config/agent-llm-bindings.yaml"),
            Path(".claude/config/agent-llm-bindings.yaml"),
        ]

        # Try parent directory (for submodules)
        parent_candidates = [
            Path("../coditect-core/.coditect/config/agent-llm-bindings.yaml"),
            Path("../../coditect-core/.coditect/config/agent-llm-bindings.yaml"),
        ]
        candidates.extend(parent_candidates)

        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()

        # Default to .coditect/config/agent-llm-bindings.yaml
        return Path(".coditect/config/agent-llm-bindings.yaml")

    def _load_config(self):
        """Load and parse agent-llm-bindings.yaml."""
        with open(self.config_path, 'r') as f:
            data = yaml.safe_load(f)

        if not data:
            raise ValueError(f"Empty configuration file: {self.config_path}")

        # Load defaults
        if 'defaults' in data:
            defaults_data = data['defaults']
            self.defaults = LlmConfig(
                provider=defaults_data.get('provider', 'anthropic-claude'),
                model=defaults_data.get('model', 'claude-3-5-sonnet-20241022'),
                api_key=defaults_data.get('api_key'),
                max_tokens=defaults_data.get('max_tokens', 4096),
                temperature=defaults_data.get('temperature', 0.7),
                metadata=defaults_data.get('metadata', {})
            )
        else:
            # Fallback defaults
            self.defaults = LlmConfig(
                provider='anthropic-claude',
                model='claude-3-5-sonnet-20241022',
                max_tokens=4096,
                temperature=0.7
            )

        # Load agent-specific configs
        if 'agents' in data:
            for agent_id, agent_data in data['agents'].items():
                self.agents[agent_id] = LlmConfig(
                    provider=agent_data.get('provider', self.defaults.provider),
                    model=agent_data.get('model', self.defaults.model),
                    api_key=agent_data.get('api_key', self.defaults.api_key),
                    max_tokens=agent_data.get('max_tokens', self.defaults.max_tokens),
                    temperature=agent_data.get('temperature', self.defaults.temperature),
                    metadata=agent_data.get('metadata', {})
                )

    def get_agent_config(self, agent_id: str) -> LlmConfig:
        """
        Get LLM configuration for a specific agent.

        Args:
            agent_id: Agent identifier (e.g., "ai-specialist", "rust-expert-developer")

        Returns:
            LlmConfig for the agent (falls back to defaults if not found)
        """
        if agent_id in self.agents:
            return self.agents[agent_id]

        # Fallback to defaults
        if self.defaults:
            return self.defaults

        # Ultimate fallback (should never reach here)
        return LlmConfig(
            provider='anthropic-claude',
            model='claude-3-5-sonnet-20241022',
            max_tokens=4096,
            temperature=0.7
        )

    def has_agent_config(self, agent_id: str) -> bool:
        """Check if agent has explicit configuration (not using defaults)."""
        return agent_id in self.agents

    def list_configured_agents(self) -> list[str]:
        """Get list of all explicitly configured agent IDs."""
        return list(self.agents.keys())

    def get_all_configs(self) -> Dict[str, LlmConfig]:
        """Get all agent configurations."""
        return self.agents.copy()

    def __repr__(self) -> str:
        return (
            f"AgentLlmConfig(config_path={self.config_path}, "
            f"agents={len(self.agents)}, defaults={self.defaults is not None})"
        )


# Convenience function for getting agent config
def get_agent_config(agent_id: str) -> LlmConfig:
    """
    Convenience function to get agent configuration.

    Args:
        agent_id: Agent identifier

    Returns:
        LlmConfig for the agent

    Example:
        config = get_agent_config("ai-specialist")
        llm = LlmFactory.get_provider(
            agent_type=config.provider,
            **config.to_factory_kwargs()
        )
    """
    return AgentLlmConfig.get_instance().get_agent_config(agent_id)
