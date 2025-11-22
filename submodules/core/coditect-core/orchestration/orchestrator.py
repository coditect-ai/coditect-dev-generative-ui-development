"""
Project Orchestrator - Core Orchestration Engine
================================================

Central orchestrator for managing multi-week AI agent projects with
dependency resolution, parallel execution, and complete audit trail.

Features:
-  Task Management (add, update, complete, cancel)
-  Dependency Resolution (automatic task ordering)
-  State Persistence (crash-safe atomic writes)
-  Backup & Rollback (permanent archive)
-  Progress Tracking (metrics, reporting)
-  Parallel Execution Planning (3-4x speedup)
-  LLM-Agnostic (works with any agent)

Example:
    >>> from claude.orchestration import ProjectOrchestrator, AgentTask
    >>>
    >>> orchestrator = ProjectOrchestrator(project_root=".")
    >>>
    >>> task = AgentTask(...)
    >>> orchestrator.add_task(task)
    >>>
    >>> next_task = orchestrator.get_next_task()
    >>> orchestrator.execute_task(next_task.task_id)
    >>> orchestrator.complete_task(next_task.task_id)
    >>>
    >>> orchestrator.generate_report()

Copyright © 2025 AZ1.AI INC. All rights reserved.
Developer: Hal Casteel, CEO/CTO
Email: 1@az1.ai
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from .agent_registry import AgentRegistry
from .backup_manager import BackupManager
from .executor import TaskExecutor, ParallelExecutor, ExecutionResult
from .state_manager import StateManager, StateMetadata
from .task import AgentTask, TaskStatus, TaskPriority, ProjectPhase


class DependencyError(Exception):
    """Raised when there are dependency-related issues."""
    pass


class ProjectOrchestrator:
    """
    Core project orchestration engine.

    Manages complete project lifecycle with task management, dependency
    resolution, state persistence, and progress tracking.

    Attributes:
        project_root: Path to project root directory
        project_id: Unique project identifier
        tasks: Dictionary of task_id ’ AgentTask
        state_manager: State persistence manager
        backup_manager: Backup and rollback manager
        executor: Task executor (optional)
        registry: Agent registry (optional)

    Example:
        >>> orchestrator = ProjectOrchestrator(
        ...     project_root=".",
        ...     project_id="calendar-platform"
        ... )
        >>>
        >>> # Add tasks
        >>> orchestrator.add_task(task1)
        >>> orchestrator.add_task(task2)
        >>>
        >>> # Execute workflow
        >>> next_task = orchestrator.get_next_task()
        >>> orchestrator.execute_task(next_task.task_id)
        >>> orchestrator.complete_task(next_task.task_id)
        >>>
        >>> # Generate report
        >>> orchestrator.generate_report()
    """

    def __init__(
        self,
        project_root: Path | str,
        project_id: str = "",
        state_file: Optional[Path | str] = None,
        executor: Optional[TaskExecutor] = None,
        registry: Optional[AgentRegistry] = None,
    ):
        """
        Initialize project orchestrator.

        Args:
            project_root: Path to project root directory
            project_id: Unique project identifier (uses dir name if not provided)
            state_file: Path to state file (default: {project_root}/scripts/project_state.json)
            executor: Task executor (optional, created if not provided)
            registry: Agent registry (optional, created if not provided)
        """
        self.project_root = Path(project_root)
        self.project_id = project_id or self.project_root.name

        # State file location
        if state_file is None:
            self.state_file = self.project_root / "scripts" / "project_state.json"
        else:
            self.state_file = Path(state_file)

        # Initialize managers
        self.state_manager = StateManager(state_file=self.state_file)
        self.backup_manager = BackupManager(state_file=self.state_file)

        # Initialize registry and executor
        self.registry = registry or AgentRegistry()
        self.executor = executor or TaskExecutor(registry=self.registry)

        # Task storage
        self.tasks: Dict[str, AgentTask] = {}

        # Load existing state
        self._load_state()

    def add_task(self, task: AgentTask) -> None:
        """
        Add a task to the project.

        Args:
            task: AgentTask to add

        Raises:
            ValueError: If task_id already exists
            DependencyError: If dependencies are invalid
        """
        if task.task_id in self.tasks:
            raise ValueError(f"Task '{task.task_id}' already exists")

        # Validate dependencies exist
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                raise DependencyError(
                    f"Task '{task.task_id}' depends on non-existent task '{dep_id}'"
                )

        # Add task
        self.tasks[task.task_id] = task

        # Save state
        self._save_state()

    def add_tasks(self, tasks: List[AgentTask]) -> None:
        """
        Add multiple tasks to the project.

        Args:
            tasks: List of AgentTask instances

        Raises:
            ValueError: If any task_id already exists
            DependencyError: If any dependencies are invalid
        """
        for task in tasks:
            self.add_task(task)

    def get_task(self, task_id: str) -> Optional[AgentTask]:
        """
        Get a task by ID.

        Args:
            task_id: Task identifier

        Returns:
            AgentTask if found, None otherwise
        """
        return self.tasks.get(task_id)

    def update_task(self, task: AgentTask) -> None:
        """
        Update an existing task.

        Args:
            task: Updated AgentTask

        Raises:
            ValueError: If task doesn't exist
        """
        if task.task_id not in self.tasks:
            raise ValueError(f"Task '{task.task_id}' not found")

        self.tasks[task.task_id] = task
        self._save_state()

    def remove_task(self, task_id: str) -> bool:
        """
        Remove a task from the project.

        Args:
            task_id: Task identifier

        Returns:
            True if removed, False if not found

        Raises:
            DependencyError: If other tasks depend on this task
        """
        if task_id not in self.tasks:
            return False

        # Check for dependent tasks
        dependents = self._find_dependent_tasks(task_id)
        if dependents:
            raise DependencyError(
                f"Cannot remove task '{task_id}': "
                f"other tasks depend on it: {', '.join(dependents)}"
            )

        # Remove task
        del self.tasks[task_id]
        self._save_state()
        return True

    def start_task(self, task_id: str) -> bool:
        """
        Mark a task as in progress.

        Args:
            task_id: Task identifier

        Returns:
            True if started, False if not found or not ready

        Raises:
            DependencyError: If dependencies not satisfied
        """
        task = self.get_task(task_id)
        if not task:
            return False

        # Check dependencies
        if not task.is_ready(self._get_completed_task_ids()):
            raise DependencyError(
                f"Task '{task_id}' has unsatisfied dependencies: "
                f"{', '.join(task.dependencies)}"
            )

        # Mark as in progress
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()

        self._save_state()
        return True

    def complete_task(
        self,
        task_id: str,
        output_files: Optional[List[str]] = None,
        notes: str = ""
    ) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id: Task identifier
            output_files: List of created files (optional)
            notes: Additional notes (optional)

        Returns:
            True if completed, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        # Mark as completed
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()

        if output_files:
            task.output_files = output_files

        if notes:
            task.notes = notes

        self._save_state()
        return True

    def fail_task(self, task_id: str, error: str = "") -> bool:
        """
        Mark a task as failed.

        Args:
            task_id: Task identifier
            error: Error message

        Returns:
            True if marked failed, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        task.status = TaskStatus.FAILED
        task.notes = error

        self._save_state()
        return True

    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a task.

        Args:
            task_id: Task identifier

        Returns:
            True if cancelled, False if not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        task.status = TaskStatus.CANCELLED
        self._save_state()
        return True

    def get_next_task(
        self,
        priority: Optional[TaskPriority] = None,
        phase: Optional[ProjectPhase] = None
    ) -> Optional[AgentTask]:
        """
        Get the next task to work on based on priority and dependencies.

        Selection criteria:
        1. Status must be PENDING
        2. All dependencies must be completed
        3. Filter by priority/phase if specified
        4. Sort by priority (CRITICAL > HIGH > MEDIUM > LOW)

        Args:
            priority: Filter by priority (optional)
            phase: Filter by phase (optional)

        Returns:
            Next AgentTask to work on, or None if no tasks ready
        """
        completed = self._get_completed_task_ids()

        # Find ready tasks
        ready_tasks = []
        for task in self.tasks.values():
            # Must be pending
            if task.status != TaskStatus.PENDING:
                continue

            # Must have dependencies satisfied
            if not task.is_ready(completed):
                continue

            # Apply filters
            if priority and task.priority != priority:
                continue

            if phase and task.phase != phase:
                continue

            ready_tasks.append(task)

        if not ready_tasks:
            return None

        # Sort by priority (CRITICAL first)
        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3,
        }

        ready_tasks.sort(key=lambda t: priority_order.get(t.priority, 99))

        return ready_tasks[0]

    def get_ready_tasks(
        self,
        max_count: Optional[int] = None
    ) -> List[AgentTask]:
        """
        Get all tasks ready to execute (for parallel execution).

        Args:
            max_count: Maximum number of tasks to return

        Returns:
            List of ready AgentTask instances
        """
        completed = self._get_completed_task_ids()
        ready_tasks = []

        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING and task.is_ready(completed):
                ready_tasks.append(task)

        # Sort by priority
        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3,
        }
        ready_tasks.sort(key=lambda t: priority_order.get(t.priority, 99))

        if max_count:
            ready_tasks = ready_tasks[:max_count]

        return ready_tasks

    def execute_task(
        self,
        task_id: str,
        agent: Optional[str] = None
    ) -> ExecutionResult:
        """
        Execute a task using specified agent.

        Args:
            task_id: Task identifier
            agent: Agent name (uses task.agent if not specified)

        Returns:
            ExecutionResult

        Raises:
            ValueError: If task not found
            DependencyError: If dependencies not satisfied
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task '{task_id}' not found")

        # Start task (validates dependencies)
        self.start_task(task_id)

        # Execute using executor
        result = self.executor.execute(task, agent=agent)

        return result

    def generate_report(self) -> dict:
        """
        Generate project status report.

        Returns:
            Dictionary with project metrics and status
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        in_progress = sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS)
        pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
        blocked = sum(1 for t in self.tasks.values() if t.status == TaskStatus.BLOCKED)
        failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)

        # Calculate hours
        estimated_total_hours = sum(t.estimated_hours for t in self.tasks.values())
        estimated_remaining_hours = sum(
            t.estimated_hours for t in self.tasks.values()
            if t.status in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED)
        )

        # Calculate completion percentage
        completion_pct = (completed / total * 100) if total > 0 else 0.0

        # Find next task
        next_task = self.get_next_task()

        return {
            "project_id": self.project_id,
            "total_tasks": total,
            "completed_tasks": completed,
            "in_progress_tasks": in_progress,
            "pending_tasks": pending,
            "blocked_tasks": blocked,
            "failed_tasks": failed,
            "completion_percentage": round(completion_pct, 2),
            "estimated_total_hours": estimated_total_hours,
            "estimated_remaining_hours": estimated_remaining_hours,
            "next_task": next_task.task_id if next_task else None,
            "timestamp": datetime.now().isoformat(),
        }

    def print_report(self) -> None:
        """Print formatted project status report."""
        report = self.generate_report()

        print("\n" + "=" * 70)
        print(f"PROJECT STATUS REPORT: {report['project_id']}")
        print("=" * 70)

        print(f"\n=Ê PROGRESS:")
        print(f"   Total Tasks: {report['total_tasks']}")
        print(f"    Completed: {report['completed_tasks']}")
        print(f"   = In Progress: {report['in_progress_tasks']}")
        print(f"   ø  Pending: {report['pending_tasks']}")
        print(f"   =« Blocked: {report['blocked_tasks']}")
        print(f"   L Failed: {report['failed_tasks']}")
        print(f"   =È Completion: {report['completion_percentage']:.1f}%")

        print(f"\nñ  TIME ESTIMATES:")
        print(f"   Total: {report['estimated_total_hours']:.1f} hours")
        print(f"   Remaining: {report['estimated_remaining_hours']:.1f} hours")

        if report['next_task']:
            next_task = self.get_task(report['next_task'])
            print(f"\n<¯ NEXT TASK:")
            print(f"   {next_task.task_id}: {next_task.title}")
            print(f"   Priority: {next_task.priority.value}")
            print(f"   Estimated: {next_task.estimated_hours}h")

        print("\n" + "=" * 70 + "\n")

    def list_backups(self, limit: int = 10) -> None:
        """
        List recent backups.

        Args:
            limit: Maximum number of backups to show
        """
        backups = self.backup_manager.list_backups(limit=limit)

        if not backups:
            print("\n=æ No backups found.\n")
            return

        print("\n" + "=" * 70)
        print("BACKUP ARCHIVE")
        print("=" * 70 + "\n")

        for i, backup in enumerate(backups, start=1):
            print(f"{i}. {backup}")

        print("\n" + "=" * 70 + "\n")

    def rollback_to_backup(
        self,
        timestamp: str,
        confirm: bool = True
    ) -> bool:
        """
        Rollback state to a specific backup.

        Args:
            timestamp: Backup timestamp (e.g., "20251112-013045")
            confirm: Require user confirmation

        Returns:
            True if rollback successful, False otherwise
        """
        success = self.backup_manager.rollback_to_backup(
            timestamp=timestamp,
            create_pre_rollback_backup=True,
            confirm=confirm
        )

        if success:
            # Reload state from file
            self._load_state()

        return success

    def _save_state(self) -> None:
        """Save current state to file with backup."""
        # Create backup first
        self.backup_manager.create_backup()

        # Serialize tasks
        tasks_dict = {
            task_id: task.to_dict()
            for task_id, task in self.tasks.items()
        }

        # Save state
        self.state_manager.save_state(
            tasks=tasks_dict,
            project_id=self.project_id
        )

    def _load_state(self) -> None:
        """Load state from file."""
        try:
            state = self.state_manager.load_state()

            # Restore tasks
            self.tasks = {}
            for task_id, task_data in state.get("tasks", {}).items():
                task = AgentTask.from_dict(task_data)
                self.tasks[task_id] = task

        except FileNotFoundError:
            # No state file yet, start fresh
            self.tasks = {}

    def _get_completed_task_ids(self) -> Set[str]:
        """Get set of completed task IDs."""
        return {
            task_id for task_id, task in self.tasks.items()
            if task.status == TaskStatus.COMPLETED
        }

    def _find_dependent_tasks(self, task_id: str) -> List[str]:
        """Find tasks that depend on specified task."""
        dependents = []
        for tid, task in self.tasks.items():
            if task_id in task.dependencies:
                dependents.append(tid)
        return dependents
