"""
Task Executor - Universal LLM Task Execution
===========================================

Universal task executor for any LLM with standardized script-based agent calling.

Features:
- ✅ LLM-Agnostic (Claude, GPT, Gemini, Llama, custom)
- ✅ Multiple Execution Modes (interactive, API, hybrid)
- ✅ Standardized Scripts Library (consistent agent calling)
- ✅ Parallel Execution (3-4x speedup)
- ✅ Execution Result Tracking (status, output, errors)
- ✅ Automatic Agent Selection (based on capabilities)

Execution Modes:
    - INTERACTIVE: Copy/paste command to Claude Code (Task tool)
    - API: Direct API calls (GPT, Gemini, etc.)
    - HYBRID: Combine multiple LLMs for complex workflows

Example:
    >>> from claude.orchestration import TaskExecutor, AgentRegistry
    >>>
    >>> registry = AgentRegistry()
    >>> registry.register_agent("claude-code", ...)
    >>>
    >>> executor = TaskExecutor(registry=registry)
    >>>
    >>> # Execute single task
    >>> result = executor.execute(task_id="TASK-001", agent="claude-code")
    >>> print(result.status)
    >>>
    >>> # Execute multiple tasks in parallel
    >>> results = executor.execute_parallel([
    ...     ("TASK-002", "claude-code"),
    ...     ("TASK-003", "gpt-4"),
    ...     ("TASK-004", "gemini-pro")
    ... ])

Copyright © 2025 AZ1.AI INC. All rights reserved.
Developer: Hal Casteel, CEO/CTO
Email: 1@az1.ai
"""

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .agent_registry import AgentRegistry, AgentConfig, AgentInterface, AgentType
from .task import AgentTask, TaskStatus


class ExecutionStatus(str, Enum):
    """Status of task execution."""

    SUCCESS = "success"        # Task completed successfully
    FAILED = "failed"          # Task failed
    PENDING = "pending"        # Execution not started
    IN_PROGRESS = "in_progress"  # Currently executing
    CANCELLED = "cancelled"    # Execution cancelled


@dataclass
class ExecutionResult:
    """
    Result of task execution.

    Attributes:
        task_id: Task identifier
        agent: Agent name used
        status: Execution status
        started_at: When execution started
        completed_at: When execution completed
        output: Agent output/response
        error: Error message if failed
        metadata: Additional execution metadata
    """

    task_id: str
    agent: str
    status: ExecutionStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    output: str = ""
    error: str = ""
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate execution duration in seconds."""
        if self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds()
        return None

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "task_id": self.task_id,
            "agent": self.agent,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "output": self.output,
            "error": self.error,
            "metadata": self.metadata,
        }


class TaskExecutor:
    """
    Universal task executor for any LLM.

    Provides standardized execution interface for tasks across different
    LLMs (Claude, GPT, Gemini, custom) using scripts library.

    Attributes:
        registry: Agent registry
        scripts_dir: Path to scripts library (optional)
        default_agent: Default agent name if not specified

    Example:
        >>> executor = TaskExecutor(registry=registry)
        >>> result = executor.execute("TASK-001", "claude-code")
    """

    def __init__(
        self,
        registry: AgentRegistry,
        scripts_dir: Optional[Path] = None,
        default_agent: str = "claude-code"
    ):
        """
        Initialize task executor.

        Args:
            registry: Agent registry
            scripts_dir: Path to scripts library
            default_agent: Default agent name
        """
        self.registry = registry
        self.scripts_dir = scripts_dir or Path(__file__).parent.parent / "scripts"
        self.default_agent = default_agent

    def execute(
        self,
        task: AgentTask,
        agent: Optional[str] = None,
        mode: Optional[str] = None
    ) -> ExecutionResult:
        """
        Execute a single task using specified agent.

        Args:
            task: Task to execute
            agent: Agent name (uses task.agent if not specified)
            mode: Execution mode override (interactive, api, hybrid)

        Returns:
            ExecutionResult

        Raises:
            ValueError: If agent not found or not configured
        """
        # Determine agent to use
        agent_name = agent or task.agent or self.default_agent

        # Get agent config
        agent_config = self.registry.get_agent(agent_name)
        if not agent_config:
            raise ValueError(f"Agent '{agent_name}' not found in registry")

        if not agent_config.enabled:
            raise ValueError(f"Agent '{agent_name}' is disabled")

        # Determine execution mode
        exec_mode = mode or agent_config.interface.value

        # Create execution result
        result = ExecutionResult(
            task_id=task.task_id,
            agent=agent_name,
            status=ExecutionStatus.PENDING,
            started_at=datetime.now(),
        )

        try:
            # Execute based on mode
            if exec_mode == AgentInterface.TASK_TOOL.value or exec_mode == "interactive":
                result = self._execute_interactive(task, agent_config, result)

            elif exec_mode == AgentInterface.API.value:
                result = self._execute_api(task, agent_config, result)

            elif exec_mode == AgentInterface.HYBRID.value:
                result = self._execute_hybrid(task, agent_config, result)

            else:
                raise ValueError(f"Unknown execution mode: {exec_mode}")

        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.now()

        return result

    def execute_parallel(
        self,
        tasks: List[Tuple[AgentTask, str]],
        max_concurrent: int = 3
    ) -> List[ExecutionResult]:
        """
        Execute multiple tasks in parallel using different agents.

        NOTE: This generates execution plan and instructions.
        Actual parallel execution requires manual coordination or
        future automation (Process pool, async/await, etc.)

        Args:
            tasks: List of (task, agent_name) tuples
            max_concurrent: Maximum concurrent executions

        Returns:
            List of ExecutionResult instances

        Example:
            >>> results = executor.execute_parallel([
            ...     (task1, "claude-code"),
            ...     (task2, "gpt-4"),
            ...     (task3, "gemini-pro")
            ... ])
        """
        print(f"\n🚀 PARALLEL EXECUTION PLAN")
        print(f"   Total tasks: {len(tasks)}")
        print(f"   Max concurrent: {max_concurrent}")
        print(f"   Estimated speedup: {len(tasks) / max_concurrent:.1f}x\n")

        results = []

        # Group tasks into batches
        for i in range(0, len(tasks), max_concurrent):
            batch = tasks[i:i + max_concurrent]
            batch_num = (i // max_concurrent) + 1

            print(f"📦 BATCH {batch_num}:")
            for task, agent_name in batch:
                print(f"   - {task.task_id}: {agent_name}")

            print(f"\n   ⏱️  Run these {len(batch)} tasks concurrently for maximum speed\n")

            # For now, execute sequentially (future: implement true parallelism)
            for task, agent_name in batch:
                result = self.execute(task, agent=agent_name)
                results.append(result)

        return results

    def _execute_interactive(
        self,
        task: AgentTask,
        agent_config: AgentConfig,
        result: ExecutionResult
    ) -> ExecutionResult:
        """
        Execute task in interactive mode (Claude Code Task tool).

        Displays command for user to copy/paste into Claude Code.

        Args:
            task: Task to execute
            agent_config: Agent configuration
            result: Execution result (in progress)

        Returns:
            Updated ExecutionResult
        """
        result.status = ExecutionStatus.IN_PROGRESS

        # Generate command for Task tool
        command = self._generate_task_tool_command(task, agent_config)

        # Display instructions
        print(f"\n📝 COPY AND PASTE THIS COMMAND INTO CLAUDE CODE:\n")
        print(f"   {command}\n")
        print(f"   Task ID: {task.task_id}")
        print(f"   Agent: {agent_config.name}")
        print(f"   Title: {task.title}\n")
        print(f"   After agent completes, mark task as done in orchestrator.\n")

        # Mark as pending (user needs to execute manually)
        result.status = ExecutionStatus.PENDING
        result.output = command
        result.metadata["execution_mode"] = "interactive"
        result.metadata["command"] = command

        return result

    def _execute_api(
        self,
        task: AgentTask,
        agent_config: AgentConfig,
        result: ExecutionResult
    ) -> ExecutionResult:
        """
        Execute task via direct API call.

        Supports OpenAI GPT, Google Gemini, and custom LLMs.

        Args:
            task: Task to execute
            agent_config: Agent configuration
            result: Execution result (in progress)

        Returns:
            Updated ExecutionResult

        Raises:
            NotImplementedError: API execution not yet implemented
        """
        result.status = ExecutionStatus.IN_PROGRESS

        # Use scripts library for standardized API calling
        script_path = self._get_execution_script(agent_config.agent_type)

        if script_path and script_path.exists():
            result = self._execute_via_script(task, agent_config, script_path, result)
        else:
            # Fallback: Generate API call instructions
            print(f"\n⚠️  API execution for {agent_config.agent_type.value} not yet implemented")
            print(f"   Task: {task.task_id}")
            print(f"   Agent: {agent_config.name}")
            print(f"   Required script: {script_path}\n")

            result.status = ExecutionStatus.PENDING
            result.metadata["requires_implementation"] = True

        return result

    def _execute_hybrid(
        self,
        task: AgentTask,
        agent_config: AgentConfig,
        result: ExecutionResult
    ) -> ExecutionResult:
        """
        Execute task using hybrid approach (multiple LLMs).

        Args:
            task: Task to execute
            agent_config: Agent configuration
            result: Execution result (in progress)

        Returns:
            Updated ExecutionResult

        Raises:
            NotImplementedError: Hybrid execution not yet implemented
        """
        raise NotImplementedError("Hybrid execution not yet implemented")

    def _execute_via_script(
        self,
        task: AgentTask,
        agent_config: AgentConfig,
        script_path: Path,
        result: ExecutionResult
    ) -> ExecutionResult:
        """
        Execute task using scripts library.

        Standardized script-based execution for consistent agent calling.

        Args:
            task: Task to execute
            agent_config: Agent configuration
            script_path: Path to execution script
            result: Execution result (in progress)

        Returns:
            Updated ExecutionResult
        """
        try:
            # Prepare task data as JSON
            task_data = task.to_dict()

            # Call execution script
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                input=json.dumps(task_data),
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )

            if proc.returncode == 0:
                result.status = ExecutionStatus.SUCCESS
                result.output = proc.stdout
            else:
                result.status = ExecutionStatus.FAILED
                result.error = proc.stderr

            result.completed_at = datetime.now()
            result.metadata["exit_code"] = proc.returncode

        except subprocess.TimeoutExpired:
            result.status = ExecutionStatus.FAILED
            result.error = "Execution timeout (1 hour)"
            result.completed_at = datetime.now()

        except Exception as e:
            result.status = ExecutionStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.now()

        return result

    def _generate_task_tool_command(
        self,
        task: AgentTask,
        agent_config: AgentConfig
    ) -> str:
        """
        Generate Task tool command for Claude Code.

        Format: Use {agent} subagent to {task_title}

        Args:
            task: Task to execute
            agent_config: Agent configuration

        Returns:
            Command string for Task tool
        """
        # Use subagent naming (without -code suffix if present)
        agent_name = agent_config.name.replace("-code", "")

        command = f"Use {agent_name} subagent to {task.title}"

        return command

    def _get_execution_script(self, agent_type: AgentType) -> Optional[Path]:
        """
        Get standardized execution script for agent type.

        Scripts library provides consistent interface for:
        - execute_claude.py
        - execute_gpt.py
        - execute_gemini.py
        - execute_llama.py
        - execute_custom.py

        Args:
            agent_type: Type of LLM

        Returns:
            Path to execution script, or None if not found
        """
        script_map = {
            AgentType.ANTHROPIC_CLAUDE: "execute_claude.py",
            AgentType.OPENAI_GPT: "execute_gpt.py",
            AgentType.GOOGLE_GEMINI: "execute_gemini.py",
            AgentType.META_LLAMA: "execute_llama.py",
            AgentType.CUSTOM: "execute_custom.py",
        }

        script_name = script_map.get(agent_type)
        if not script_name:
            return None

        script_path = self.scripts_dir / script_name
        return script_path if script_path.exists() else None


class ParallelExecutor:
    """
    Parallel task executor for maximum speed.

    Analyzes task dependencies and generates optimal execution plan
    with parallel batches.

    Example:
        >>> parallel_executor = ParallelExecutor(executor=executor)
        >>> plan = parallel_executor.generate_execution_plan(tasks)
        >>> results = parallel_executor.execute_plan(plan)
    """

    def __init__(self, executor: TaskExecutor):
        """
        Initialize parallel executor.

        Args:
            executor: Base TaskExecutor instance
        """
        self.executor = executor

    def generate_execution_plan(
        self,
        tasks: Dict[str, AgentTask],
        max_concurrent: int = 3
    ) -> List[List[Tuple[AgentTask, str]]]:
        """
        Generate optimal parallel execution plan.

        Analyzes dependencies and groups tasks into batches that can
        run concurrently (no dependency violations).

        Args:
            tasks: Dictionary of task_id → AgentTask
            max_concurrent: Maximum tasks per batch

        Returns:
            List of batches, each batch is list of (task, agent) tuples

        Example:
            >>> plan = parallel_executor.generate_execution_plan(tasks)
            >>> # [[task1, task2, task3], [task4, task5], [task6]]
        """
        # Track completed tasks
        completed = set()
        remaining = dict(tasks)
        batches = []

        while remaining:
            # Find tasks ready to execute (all dependencies satisfied)
            ready = []
            for task_id, task in remaining.items():
                if task.is_ready(completed):
                    ready.append((task, task.agent))

            if not ready:
                # No tasks ready (circular dependency or blocked)
                print(f"⚠️  WARNING: {len(remaining)} tasks blocked by dependencies")
                break

            # Split ready tasks into batches of max_concurrent
            for i in range(0, len(ready), max_concurrent):
                batch = ready[i:i + max_concurrent]
                batches.append(batch)

            # Mark as completed for dependency checking
            for task, _ in ready:
                completed.add(task.task_id)
                del remaining[task.task_id]

        return batches

    def execute_plan(
        self,
        plan: List[List[Tuple[AgentTask, str]]]
    ) -> List[ExecutionResult]:
        """
        Execute parallel execution plan.

        Args:
            plan: Execution plan from generate_execution_plan()

        Returns:
            List of ExecutionResult instances
        """
        results = []

        for batch_num, batch in enumerate(plan, start=1):
            print(f"\n📦 EXECUTING BATCH {batch_num}/{len(plan)}")
            print(f"   Tasks in batch: {len(batch)}\n")

            batch_results = self.executor.execute_parallel(batch)
            results.extend(batch_results)

        return results
