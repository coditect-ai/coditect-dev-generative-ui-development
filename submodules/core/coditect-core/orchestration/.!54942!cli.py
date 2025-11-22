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

