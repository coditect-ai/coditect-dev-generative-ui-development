"""
AZ1.AI Agentic Project Orchestration Framework
===============================================

Universal LLM-agnostic orchestration framework for AI-driven project management.

Supports: Claude, GPT-4, Gemini, Llama, and custom LLMs.

Quick Start:
    >>> from claude.orchestration import ProjectOrchestrator, AgentTask, TaskPriority
    >>>
    >>> orchestrator = ProjectOrchestrator(project_root="/path/to/project")
    >>>
    >>> task = AgentTask(
    ...     task_id="TASK-001",
    ...     title="Create API Documentation",
    ...     description="Generate comprehensive API docs...",
    ...     agent="claude-code",  # or "gpt-4", "gemini-pro", etc.
    ...     priority=TaskPriority.HIGH
    ... )
    >>>
    >>> orchestrator.add_task(task)
    >>> next_task = orchestrator.get_next_task()
    >>> orchestrator.execute_task(next_task.task_id)
    >>> orchestrator.complete_task(next_task.task_id)

Components:
    - ProjectOrchestrator: Core orchestration engine
    - AgentTask: Zero-ambiguity task specification
    - StateManager: Enterprise-grade state persistence
    - BackupManager: Backup and rollback functionality
    - AgentRegistry: LLM abstraction layer
    - TaskExecutor: Universal task executor

Features:
    ✅ LLM-Agnostic (Claude, GPT, Gemini, Llama, custom)
    ✅ Enterprise-Grade State Persistence (atomic writes, checksums)
    ✅ Dependency Management (automatic task ordering)
    ✅ Parallel Execution (3-4x speedup)
    ✅ Complete Audit Trail (permanent backups)
    ✅ Rollback Support (restore to any point in time)

License: Proprietary - Closed Source
Copyright: © 2025 AZ1.AI INC. All rights reserved.
Developer: Hal Casteel, CEO/CTO
Email: 1@az1.ai
"""

__version__ = "2.0.0"
__author__ = "Hal Casteel, CEO/CTO, AZ1.AI INC."
__email__ = "1@az1.ai"
__license__ = "Proprietary"

from .task import (
    AgentTask,
    TaskPriority,
    TaskStatus,
    ProjectPhase,
)

from .state_manager import (
    StateManager,
    StateFormatVersion,
)

from .backup_manager import (
    BackupManager,
    BackupMetadata,
)

from .orchestrator import (
    ProjectOrchestrator,
    DependencyError,
)

from .agent_registry import (
    AgentRegistry,
    AgentType,
    AgentInterface,
)

from .executor import (
    TaskExecutor,
    ExecutionResult,
    ParallelExecutor,
)

__all__ = [
    # Core classes
    "ProjectOrchestrator",
    "AgentTask",
    "StateManager",
    "BackupManager",
    "AgentRegistry",
    "TaskExecutor",
    "ParallelExecutor",

    # Enums
    "TaskPriority",
    "TaskStatus",
    "ProjectPhase",
    "StateFormatVersion",
    "AgentType",
    "AgentInterface",

    # Data classes
    "BackupMetadata",
    "ExecutionResult",

    # Exceptions
    "DependencyError",

    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
