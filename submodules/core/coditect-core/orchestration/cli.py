#!/usr/bin/env python3
"""
CLI - Command-Line Interface for Orchestrator
============================================

Provides command-line interface for project orchestration operations.

Usage:
    python -m claude.orchestration.cli [command] [options]

Commands:
    --list                    List all tasks
    --next                    Show next recommended task
    --execute TASK_ID         Execute specific task
    --complete TASK_ID        Mark task as completed
    --fail TASK_ID            Mark task as failed
    --cancel TASK_ID          Cancel task
    --report                  Generate status report
    --list-backups            List all backups
    --rollback TIMESTAMP      Rollback to specific backup
    --help                    Show this help message

Examples:
    # Show next task
    python -m claude.orchestration.cli --next

    # Execute task
    python -m claude.orchestration.cli --execute TASK-001

    # Mark complete
    python -m claude.orchestration.cli --complete TASK-001

    # Generate report
    python -m claude.orchestration.cli --report

    # List backups
    python -m claude.orchestration.cli --list-backups

    # Rollback
    python -m claude.orchestration.cli --rollback 20251112-013045

Copyright � 2025 AZ1.AI INC. All rights reserved.
Developer: Hal Casteel, CEO/CTO
Email: 1@az1.ai
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Optional

from .orchestrator import ProjectOrchestrator
from .task import TaskStatus, TaskPriority, ProjectPhase


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for CLI.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Project Orchestration CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                      # List all tasks
  %(prog)s --next                      # Show next task
  %(prog)s --execute TASK-001          # Execute task
  %(prog)s --complete TASK-001         # Mark complete
  %(prog)s --report                    # Status report
  %(prog)s --list-backups              # List backups
  %(prog)s --rollback 20251112-013045  # Rollback

Copyright � 2025 AZ1.AI INC. All rights reserved.
        """
    )

    # Project options
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)"
    )

    parser.add_argument(
        "--state-file",
        type=Path,
        help="Path to state file (default: {project-root}/scripts/project_state.json)"
    )

    # Commands
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all tasks"
    )

    parser.add_argument(
        "--next",
        action="store_true",
        help="Show next recommended task"
    )

    parser.add_argument(
        "--execute",
        metavar="TASK_ID",
        help="Execute specific task"
    )

    parser.add_argument(
        "--complete",
        metavar="TASK_ID",
        help="Mark task as completed"
    )

    parser.add_argument(
        "--fail",
        metavar="TASK_ID",
        help="Mark task as failed"
    )

    parser.add_argument(
        "--cancel",
        metavar="TASK_ID",
        help="Cancel task"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate status report"
    )

    parser.add_argument(
        "--list-backups",
        action="store_true",
        help="List all backups"
    )

    parser.add_argument(
        "--rollback",
        metavar="TIMESTAMP",
        help="Rollback to specific backup (e.g., 20251112-013045)"
    )

    # Filters
    parser.add_argument(
        "--priority",
        choices=["critical", "high", "medium", "low"],
        help="Filter by priority"
    )

    parser.add_argument(
        "--phase",
        choices=["planning", "design", "development", "testing", "deployment", "maintenance"],
        help="Filter by phase"
    )

    parser.add_argument(
        "--status",
        choices=["pending", "in_progress", "blocked", "completed", "failed", "cancelled"],
        help="Filter by status"
    )

    return parser


def cmd_list_tasks(orchestrator: ProjectOrchestrator, args: argparse.Namespace) -> None:
    """List all tasks."""
    tasks = list(orchestrator.tasks.values())

    # Apply filters
    if args.priority:
        priority = TaskPriority(args.priority)
        tasks = [t for t in tasks if t.priority == priority]

    if args.phase:
        phase = ProjectPhase(args.phase)
        tasks = [t for t in tasks if t.phase == phase]

    if args.status:
        status = TaskStatus(args.status)
        tasks = [t for t in tasks if t.status == status]

    if not tasks:
        print("\nNo tasks found.\n")
        return

    print("\n" + "=" * 70)
    print("TASK LIST")
    print("=" * 70 + "\n")

    for task in tasks:
        status_emoji = {
            TaskStatus.PENDING: "� ",
            TaskStatus.IN_PROGRESS: "=",
            TaskStatus.BLOCKED: "=�",
            TaskStatus.COMPLETED: "",
            TaskStatus.FAILED: "L",
            TaskStatus.CANCELLED: "=�",
        }.get(task.status, "  ")

        print(f"{status_emoji} {task.task_id}: {task.title}")
        print(f"   Status: {task.status.value} | Priority: {task.priority.value} | Phase: {task.phase.value}")
        print(f"   Estimated: {task.estimated_hours}h | Agent: {task.agent}")

        if task.dependencies:
            print(f"   Dependencies: {', '.join(task.dependencies)}")

        print()

    print("=" * 70 + "\n")


def cmd_next_task(orchestrator: ProjectOrchestrator, args: argparse.Namespace) -> None:
    """Show next recommended task."""
    priority = TaskPriority(args.priority) if args.priority else None
    phase = ProjectPhase(args.phase) if args.phase else None

    next_task = orchestrator.get_next_task(priority=priority, phase=phase)

    if not next_task:
        print("\n No tasks ready to execute. All tasks either completed or blocked.\n")
        return

    print("\n" + "=" * 70)
    print("<� NEXT RECOMMENDED TASK")
    print("=" * 70 + "\n")

    print(f"Task ID: {next_task.task_id}")
    print(f"Title: {next_task.title}")
    print(f"Priority: {next_task.priority.value}")
    print(f"Phase: {next_task.phase.value}")
    print(f"Estimated: {next_task.estimated_hours}h")
    print(f"Agent: {next_task.agent}")

    if next_task.dependencies:
        print(f"Dependencies: {', '.join(next_task.dependencies)}")

    print(f"\nDescription:")
    print(next_task.description)

    if next_task.deliverables:
        print(f"\nDeliverables:")
        for deliverable in next_task.deliverables:
            print(f"  - {deliverable}")

    if next_task.success_criteria:
        print(f"\nSuccess Criteria:")
        for criteria in next_task.success_criteria:
            print(f"  - {criteria}")

    print("\n" + "=" * 70 + "\n")
    print(f"To execute: python -m claude.orchestration.cli --execute {next_task.task_id}\n")


def cmd_execute_task(orchestrator: ProjectOrchestrator, task_id: str) -> None:
    """Execute specific task."""
    task = orchestrator.get_task(task_id)
    if not task:
        print(f"\nL Task '{task_id}' not found.\n")
        sys.exit(1)

    print(f"\n=� Executing task: {task_id}\n")

    try:
        # Call async execute_task() using asyncio.run()
        result = asyncio.run(orchestrator.execute_task(task_id))

        if result.status == "success":
            print(f" Task executed successfully")
        elif result.status == "pending":
            print(f"�  Task execution pending (interactive mode)")
        else:
            print(f"L Task execution failed: {result.error}")

        if result.output:
            print(f"\nOutput:\n{result.output}")

    except Exception as e:
        print(f"\nL Execution failed: {e}\n")
        sys.exit(1)


def cmd_complete_task(orchestrator: ProjectOrchestrator, task_id: str) -> None:
    """Mark task as completed."""
    task = orchestrator.get_task(task_id)
    if not task:
        print(f"\nL Task '{task_id}' not found.\n")
        sys.exit(1)

    success = orchestrator.complete_task(task_id)

    if success:
        print(f"\n Task '{task_id}' marked as completed.\n")
    else:
        print(f"\nL Failed to mark task '{task_id}' as completed.\n")
        sys.exit(1)


def cmd_fail_task(orchestrator: ProjectOrchestrator, task_id: str) -> None:
    """Mark task as failed."""
    task = orchestrator.get_task(task_id)
    if not task:
        print(f"\nL Task '{task_id}' not found.\n")
        sys.exit(1)

    error = input("Error message (optional): ")

    success = orchestrator.fail_task(task_id, error=error)

    if success:
        print(f"\nL Task '{task_id}' marked as failed.\n")
    else:
        print(f"\nL Failed to mark task '{task_id}' as failed.\n")
        sys.exit(1)


def cmd_cancel_task(orchestrator: ProjectOrchestrator, task_id: str) -> None:
    """Cancel task."""
    task = orchestrator.get_task(task_id)
    if not task:
        print(f"\nL Task '{task_id}' not found.\n")
        sys.exit(1)

    success = orchestrator.cancel_task(task_id)

    if success:
        print(f"\n=� Task '{task_id}' cancelled.\n")
    else:
        print(f"\nL Failed to cancel task '{task_id}'.\n")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Create orchestrator
    try:
        orchestrator = ProjectOrchestrator(
            project_root=args.project_root,
            state_file=args.state_file
        )
    except Exception as e:
        print(f"\nL Failed to initialize orchestrator: {e}\n")
        sys.exit(1)

    # Execute commands
    try:
        if args.list:
            cmd_list_tasks(orchestrator, args)

        elif args.next:
            cmd_next_task(orchestrator, args)

        elif args.execute:
            cmd_execute_task(orchestrator, args.execute)

        elif args.complete:
            cmd_complete_task(orchestrator, args.complete)

        elif args.fail:
            cmd_fail_task(orchestrator, args.fail)

        elif args.cancel:
            cmd_cancel_task(orchestrator, args.cancel)

        elif args.report:
            orchestrator.print_report()

        elif args.list_backups:
            orchestrator.list_backups()

        elif args.rollback:
            orchestrator.rollback_to_backup(args.rollback)

        else:
            parser.print_help()

    except Exception as e:
        print(f"\nL Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
