"""
Command Result Data Structures

Defines structured result types for slash command execution.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class CommandStatus(Enum):
    """Status of command execution."""

    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    PENDING = "pending"


@dataclass
class CommandResult:
    """
    Structured result from slash command execution.

    Provides programmatic access to command execution results
    with metadata for tracking, analytics, and downstream integration.
    """

    # Core fields
    command: str  # Original command (e.g., "/analyze")
    status: CommandStatus
    output: str  # Primary output text

    # Execution metadata
    agent_used: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None

    # Timing
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time_seconds: Optional[float] = None

    # Resource usage
    tokens_used: Optional[int] = None
    estimated_cost: Optional[float] = None

    # Structured results (command-specific)
    structured_data: Dict[str, Any] = field(default_factory=dict)

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Error information (if status == FAILED)
    error_message: Optional[str] = None
    error_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "command": self.command,
            "status": self.status.value,
            "output": self.output,
            "agent_used": self.agent_used,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "execution_time_seconds": self.execution_time_seconds,
            "tokens_used": self.tokens_used,
            "estimated_cost": self.estimated_cost,
            "structured_data": self.structured_data,
            "metadata": self.metadata,
            "error_message": self.error_message,
            "error_type": self.error_type,
        }

    @property
    def success(self) -> bool:
        """Check if command succeeded."""
        return self.status == CommandStatus.SUCCESS

    @property
    def cost_formatted(self) -> str:
        """Get formatted cost string."""
        if self.estimated_cost is None:
            return "N/A"
        return f"${self.estimated_cost:.4f}"


@dataclass
class CommandSpec:
    """
    Specification for a slash command.

    Defines how a command should be parsed and executed.
    """

    name: str  # Command name (e.g., "/analyze")
    agent_id: str  # Agent to execute the command
    description: str  # Human-readable description

    # Argument specification
    required_args: List[str] = field(default_factory=list)
    optional_args: List[str] = field(default_factory=list)

    # Execution configuration
    task_type: str = "general"  # For system prompt selection
    streaming_enabled: bool = False

    # Examples
    examples: List[str] = field(default_factory=list)

    # Metadata
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def validate_args(self, args: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate command arguments.

        Returns:
            (is_valid, error_message)
        """
        # Check required args
        for req_arg in self.required_args:
            if req_arg not in args:
                return False, f"Missing required argument: {req_arg}"

        return True, None


# Command registry - maps command names to specifications
COMMAND_REGISTRY: Dict[str, CommandSpec] = {
    "/analyze": CommandSpec(
        name="/analyze",
        agent_id="code-reviewer",
        description="Analyze code quality, security, and performance",
        optional_args=["target", "focus", "depth"],
        task_type="code-generation",
        examples=[
            "/analyze",
            "/analyze target=src/main.rs",
            "/analyze focus=security",
        ],
        category="development",
        tags=["code", "quality", "review"],
    ),

    "/implement": CommandSpec(
        name="/implement",
        agent_id="rust-expert-developer",
        description="Implement production-ready code with full error handling",
        required_args=["description"],
        optional_args=["language", "framework"],
        task_type="code-generation",
        examples=[
            "/implement description='Add JWT authentication middleware'",
            "/implement description='WebSocket server' framework=actix-web",
        ],
        category="development",
        tags=["code", "implementation", "production"],
    ),

    "/research": CommandSpec(
        name="/research",
        agent_id="web-search-researcher",
        description="Research external information with multi-source validation",
        required_args=["topic"],
        optional_args=["depth", "sources"],
        task_type="research",
        examples=[
            "/research topic='GraphQL vs REST performance 2025'",
            "/research topic='Rust async patterns' depth=comprehensive",
        ],
        category="research",
        tags=["research", "external", "validation"],
    ),

    "/strategy": CommandSpec(
        name="/strategy",
        agent_id="software-design-architect",
        description="Architectural planning with C4 diagrams and ADRs",
        required_args=["goal"],
        optional_args=["constraints", "style"],
        task_type="architecture",
        examples=[
            "/strategy goal='Design multi-tenant SaaS architecture'",
            "/strategy goal='API design' style=REST",
        ],
        category="architecture",
        tags=["architecture", "planning", "c4"],
    ),

    "/optimize": CommandSpec(
        name="/optimize",
        agent_id="senior-architect",
        description="Performance optimization and scalability analysis",
        required_args=["target"],
        optional_args=["metric", "threshold"],
        task_type="code-generation",
        examples=[
            "/optimize target=database_queries",
            "/optimize target=api_endpoints metric=latency",
        ],
        category="performance",
        tags=["performance", "optimization", "scalability"],
    ),

    "/document": CommandSpec(
        name="/document",
        agent_id="codi-documentation-writer",
        description="Generate comprehensive documentation",
        required_args=["type"],
        optional_args=["target", "format"],
        task_type="documentation",
        examples=[
            "/document type=api",
            "/document type=architecture target=auth_system",
        ],
        category="documentation",
        tags=["documentation", "api", "architecture"],
    ),

    "/new-project": CommandSpec(
        name="/new-project",
        agent_id="orchestrator",
        description="Complete project creation from discovery to structure",
        required_args=["description"],
        optional_args=["type", "stack"],
        task_type="general",
        streaming_enabled=True,
        examples=[
            "/new-project description='Build SaaS API for project management'",
            "/new-project description='E-commerce platform' stack=rust",
        ],
        category="project",
        tags=["project", "creation", "workflow"],
    ),
}
