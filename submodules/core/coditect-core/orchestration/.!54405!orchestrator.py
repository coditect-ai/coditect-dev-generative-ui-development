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

