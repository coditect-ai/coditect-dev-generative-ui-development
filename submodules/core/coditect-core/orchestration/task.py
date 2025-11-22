"""
Task Model - Zero-Ambiguity Task Specification
==============================================

Defines the AgentTask class and related enums for specifying AI agent tasks
with complete clarity and no ambiguity.

Example:
    >>> task = AgentTask(
    ...     task_id="API-001",
    ...     title="Design Authentication API",
    ...     description='''
    ...     Create REST API for user authentication.
    ...
    ...     INPUTS:
    ...     - docs/API-SPEC.md (template)
    ...     - docs/AUTH-REQUIREMENTS.md
    ...
    ...     REQUIREMENTS:
    ...     1. POST /auth/register endpoint
    ...     2. POST /auth/login endpoint
    ...     3. JWT token generation
    ...
    ...     OUTPUT: src/api/auth.ts
    ...
    ...     SUCCESS CRITERIA:
    ...     - All endpoints implemented
    ...     - Unit tests passing
    ...     ''',
    ...     agent="claude-code",
    ...     priority=TaskPriority.CRITICAL,
    ...     phase=ProjectPhase.DEVELOPMENT,
    ...     estimated_hours=4
    ... )
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class TaskPriority(str, Enum):
    """Task priority levels for execution ordering."""

    CRITICAL = "critical"  # Must be done immediately, blocks everything
    HIGH = "high"          # Important, should be done soon
    MEDIUM = "medium"      # Normal priority
    LOW = "low"            # Nice to have, can be deferred


class TaskStatus(str, Enum):
    """Task execution status."""

    PENDING = "pending"        # Not started yet
    IN_PROGRESS = "in_progress"  # Currently being worked on
    BLOCKED = "blocked"        # Waiting on dependencies or resources
    COMPLETED = "completed"    # Successfully finished
    FAILED = "failed"          # Execution failed
    CANCELLED = "cancelled"    # Task cancelled/deprecated


class ProjectPhase(str, Enum):
    """Project lifecycle phase for task organization."""

    PLANNING = "planning"          # Requirements, specifications
    DESIGN = "design"              # Architecture, technical design
    DEVELOPMENT = "development"    # Implementation, coding
    TESTING = "testing"            # QA, integration testing
    DEPLOYMENT = "deployment"      # Release, production deployment
    MAINTENANCE = "maintenance"    # Bug fixes, optimizations


@dataclass
class AgentTask:
    """
    Zero-ambiguity task specification for AI agents.

    A task contains everything an agent needs to autonomously execute work:
    - Clear title and description
    - Specific inputs, requirements, outputs
    - Success criteria for validation
    - Agent assignment (LLM-agnostic)
    - Dependencies and priority

    Attributes:
        task_id: Unique identifier (e.g., "ADR-001", "API-042")
        title: Human-readable title (concise, < 60 chars)
        description: Complete task specification (zero ambiguity)
        agent: AI agent name (e.g., "claude-code", "gpt-4", "gemini-pro")
        priority: Task priority level
        phase: Project lifecycle phase
        dependencies: List of prerequisite task IDs
        estimated_hours: Time estimate for completion
        deliverables: List of output files to be created
        success_criteria: Measurable success indicators
        commands: Agent execution commands (optional)
        tags: Categorization tags (optional)
        status: Current execution status
        started_at: Timestamp when started
        completed_at: Timestamp when completed
        output_files: Actual files created (populated after completion)
        notes: Additional notes or context
        metadata: Custom key-value pairs

    Example:
        >>> task = AgentTask(
        ...     task_id="DB-001",
        ...     title="Design Database Schema",
        ...     description='''
        ...     Create Prisma schema for multi-tenant booking system.
        ...
        ...     INPUTS:
        ...     - docs/SOFTWARE-DESIGN-DOCUMENT.md (section 5)
        ...     - architecture/diagrams/entity-relationship.md
        ...
        ...     REQUIREMENTS:
        ...     1. Multi-tenant isolation (tenant_id in all tables)
        ...     2. Soft deletes (deleted_at timestamp)
        ...     3. Audit fields (created_at, updated_at, created_by, updated_by)
        ...     4. UUID primary keys
        ...     5. Indexes for frequently queried fields
        ...
        ...     OUTPUT: prisma/schema.prisma
        ...
        ...     SUCCESS CRITERIA:
        ...     - Schema compiles with `npx prisma validate`
        ...     - All entities from ERD represented
        ...     - Relationships correctly defined (1:1, 1:N, N:M)
        ...     - Indexes on foreign keys
        ...     ''',
        ...     agent="claude-code",
        ...     priority=TaskPriority.CRITICAL,
        ...     phase=ProjectPhase.DESIGN,
        ...     dependencies=[],
        ...     estimated_hours=6,
        ...     deliverables=["prisma/schema.prisma"],
        ...     success_criteria=[
        ...         "Schema validates successfully",
        ...         "All entities represented",
        ...         "Relationships correct",
        ...         "Indexes added"
        ...     ]
        ... )
    """

    # Required fields
    task_id: str
    title: str
    description: str
    agent: str

    # Priority and organization
    priority: TaskPriority = TaskPriority.MEDIUM
    phase: ProjectPhase = ProjectPhase.DEVELOPMENT
    dependencies: List[str] = field(default_factory=list)

    # Estimation and outputs
    estimated_hours: float = 1.0
    deliverables: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)

    # Optional execution details
    commands: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    # Status tracking (set by orchestrator)
    status: TaskStatus = TaskStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Outputs (populated after completion)
    output_files: List[str] = field(default_factory=list)
    notes: str = ""

    # Extensibility
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Validate task specification on creation."""
        if not self.task_id:
            raise ValueError("task_id is required")

        if not self.title:
            raise ValueError("title is required")

        if not self.description:
            raise ValueError("description is required")

        if not self.agent:
            raise ValueError("agent is required")

        if self.estimated_hours <= 0:
            raise ValueError("estimated_hours must be positive")

    def is_ready(self, completed_tasks: set) -> bool:
        """
        Check if task is ready to execute (all dependencies completed).

        Args:
            completed_tasks: Set of completed task IDs

        Returns:
            True if all dependencies are satisfied
        """
        return all(dep in completed_tasks for dep in self.dependencies)

    def is_blocked(self, completed_tasks: set) -> bool:
        """
        Check if task is blocked by incomplete dependencies.

        Args:
            completed_tasks: Set of completed task IDs

        Returns:
            True if any dependencies are not completed
        """
        return not self.is_ready(completed_tasks)

    def to_dict(self) -> dict:
        """
        Serialize task to dictionary (for JSON persistence).

        Returns:
            Dictionary representation of task
        """
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "agent": self.agent,
            "priority": self.priority.value,
            "phase": self.phase.value,
            "dependencies": self.dependencies,
            "estimated_hours": self.estimated_hours,
            "deliverables": self.deliverables,
            "success_criteria": self.success_criteria,
            "commands": self.commands,
            "tags": self.tags,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "output_files": self.output_files,
            "notes": self.notes,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AgentTask":
        """
        Deserialize task from dictionary (from JSON persistence).

        Args:
            data: Dictionary representation of task

        Returns:
            AgentTask instance
        """
        # Convert enum strings back to enums
        if "priority" in data and isinstance(data["priority"], str):
            data["priority"] = TaskPriority(data["priority"])

        if "phase" in data and isinstance(data["phase"], str):
            data["phase"] = ProjectPhase(data["phase"])

        if "status" in data and isinstance(data["status"], str):
            data["status"] = TaskStatus(data["status"])

        # Convert ISO timestamp strings back to datetime
        if data.get("started_at"):
            data["started_at"] = datetime.fromisoformat(data["started_at"])

        if data.get("completed_at"):
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])

        return cls(**data)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"AgentTask(task_id='{self.task_id}', "
            f"title='{self.title}', "
            f"status={self.status.value}, "
            f"agent='{self.agent}', "
            f"priority={self.priority.value})"
        )


# Task creation helpers

def create_design_task(
    task_id: str,
    title: str,
    description: str,
    agent: str = "claude-code",
    **kwargs
) -> AgentTask:
    """Helper to create a design phase task."""
    return AgentTask(
        task_id=task_id,
        title=title,
        description=description,
        agent=agent,
        phase=ProjectPhase.DESIGN,
        **kwargs
    )


def create_development_task(
    task_id: str,
    title: str,
    description: str,
    agent: str = "claude-code",
    **kwargs
) -> AgentTask:
    """Helper to create a development phase task."""
    return AgentTask(
        task_id=task_id,
        title=title,
        description=description,
        agent=agent,
        phase=ProjectPhase.DEVELOPMENT,
        **kwargs
    )


def create_critical_task(
    task_id: str,
    title: str,
    description: str,
    agent: str = "claude-code",
    **kwargs
) -> AgentTask:
    """Helper to create a critical priority task."""
    return AgentTask(
        task_id=task_id,
        title=title,
        description=description,
        agent=agent,
        priority=TaskPriority.CRITICAL,
        **kwargs
    )
