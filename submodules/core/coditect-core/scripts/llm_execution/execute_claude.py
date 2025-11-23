#!/usr/bin/env python3
"""
Execute Claude - Standardized Claude Agent Execution Script
===========================================================

Executes tasks using Anthropic Claude (via Claude Code Task tool).

Usage:
    echo '{"task_id": "TASK-001", ...}' | python execute_claude.py

Input (stdin): JSON task specification
Output (stdout): JSON execution result
Exit Codes:
    0 - Success
    1 - Execution error
    2 - Configuration error
    3 - Task specification error

Copyright (c) 2025 AZ1.AI INC. All rights reserved.
Developer: Hal Casteel, CEO/CTO
Email: 1@az1.ai
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, Any, Optional


def read_task_from_stdin() -> Dict[str, Any]:
    """
    Read task specification from stdin.

    Returns:
        Task data dictionary

    Raises:
        ValueError: If input is not valid JSON
    """
    try:
        task_data = json.load(sys.stdin)
        return task_data
    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "failed",
            "error": f"Invalid JSON input: {e}",
            "exit_code": 3
        }), file=sys.stderr)
        sys.exit(3)


def validate_task_spec(task: Dict[str, Any]) -> Optional[str]:
    """
    Validate task specification has required fields.

    Args:
        task: Task data dictionary

    Returns:
        Error message if invalid, None if valid
    """
    required_fields = ["task_id", "title", "description", "agent"]

    for field in required_fields:
        if field not in task or not task[field]:
            return f"Missing required field: {field}"

    return None


def generate_task_tool_command(task: Dict[str, Any]) -> str:
    """
    Generate Task tool command for Claude Code.

    Args:
        task: Task data dictionary

    Returns:
        Command string for Task tool
    """
    # Format: Use {agent} subagent to {task_title}
    agent_name = task.get("agent", "claude").replace("-code", "")
    title = task["title"]

    command = f"Use {agent_name} subagent to {title}"

    return command


def execute_claude_interactive(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute task using Claude Code (interactive mode).

    Displays command for user to copy/paste into Claude Code.
    This is the primary execution mode for Claude.

    Args:
        task: Task data dictionary

    Returns:
        Execution result dictionary
    """
    start_time = time.time()
    task_id = task["task_id"]

    # Generate Task tool command
    command = generate_task_tool_command(task)

    # Display instructions
    print("\n" + "=" * 70, file=sys.stderr)
    print("=� CLAUDE CODE TASK EXECUTION", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(f"\nTask ID: {task_id}", file=sys.stderr)
    print(f"Title: {task['title']}", file=sys.stderr)
    print(f"Agent: {task.get('agent', 'claude-code')}", file=sys.stderr)
    print(f"\nCOPY THIS COMMAND TO CLAUDE CODE:", file=sys.stderr)
    print(f"\n   {command}\n", file=sys.stderr)

    if task.get("deliverables"):
        print(f"Expected deliverables:", file=sys.stderr)
        for deliverable in task["deliverables"]:
            print(f"   - {deliverable}", file=sys.stderr)
        print(file=sys.stderr)

    print("After agent completes, mark task as done in orchestrator.", file=sys.stderr)
    print("=" * 70 + "\n", file=sys.stderr)

    # Calculate execution time
    execution_time = time.time() - start_time

    # Return result (pending user action)
    return {
        "status": "pending",
        "output": command,
        "error": None,
        "task_id": task_id,
        "agent": task.get("agent", "claude-code"),
        "execution_mode": "interactive",
        "command": command,
        "execution_time_seconds": execution_time,
        "timestamp": datetime.now().isoformat(),
    }


def execute_claude_api(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute task using Claude API (direct API mode).

    NOTE: API execution requires Anthropic API key and is for
    automated execution without user interaction.

    Args:
        task: Task data dictionary

    Returns:
        Execution result dictionary

    Raises:
        NotImplementedError: API mode not yet implemented
    """
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "status": "failed",
            "error": "ANTHROPIC_API_KEY environment variable not set",
            "exit_code": 2
        }

    # TODO: Implement Claude API execution
    # This would use anthropic Python SDK to call Claude API directly
    raise NotImplementedError("Claude API execution not yet implemented")


def main():
    """Main execution entry point."""
    try:
        # Read task from stdin
        task = read_task_from_stdin()

        # Validate task specification
        error = validate_task_spec(task)
        if error:
            result = {
                "status": "failed",
                "error": error,
                "exit_code": 3
            }
            print(json.dumps(result), file=sys.stderr)
            sys.exit(3)

        # Determine execution mode
        execution_mode = task.get("execution_mode", "interactive")

        if execution_mode == "api":
            result = execute_claude_api(task)
        else:
            result = execute_claude_interactive(task)

        # Output result to stdout
        print(json.dumps(result, indent=2))

        # Exit with appropriate code
        exit_code = result.get("exit_code", 0)
        sys.exit(exit_code)

    except Exception as e:
        result = {
            "status": "failed",
            "error": str(e),
            "exit_code": 1
        }
        print(json.dumps(result), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
