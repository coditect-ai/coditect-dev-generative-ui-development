#!/usr/bin/env python3
"""
Execute GPT - Standardized OpenAI GPT-4 Execution Script
========================================================

Executes tasks using OpenAI GPT-4 via API.

Usage:
    echo '{"task_id": "TASK-001", ...}' | python execute_gpt.py

Input (stdin): JSON task specification
Output (stdout): JSON execution result
Exit Codes:
    0 - Success
    1 - Execution error
    2 - Configuration error (missing API key)
    3 - Task specification error

Copyright � 2025 AZ1.AI INC. All rights reserved.
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
    """Read task specification from stdin."""
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
    """Validate task specification has required fields."""
    required_fields = ["task_id", "title", "description", "agent"]

    for field in required_fields:
        if field not in task or not task[field]:
            return f"Missing required field: {field}"

    return None


def execute_gpt_api(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute task using OpenAI GPT-4 API.

    Args:
        task: Task data dictionary

    Returns:
        Execution result dictionary
    """
    start_time = time.time()
    task_id = task["task_id"]

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "status": "failed",
            "error": "OPENAI_API_KEY environment variable not set",
            "task_id": task_id,
            "exit_code": 2,
            "timestamp": datetime.now().isoformat(),
        }

    try:
        # Import OpenAI library (v1.99.9+ / 2025 SDK)
        try:
            from openai import OpenAI
        except ImportError:
            return {
                "status": "failed",
                "error": "openai library not installed. Install with: pip install openai",
                "task_id": task_id,
                "exit_code": 2,
                "timestamp": datetime.now().isoformat(),
            }

        # Initialize OpenAI client (2025 SDK)
        client = OpenAI(api_key=api_key)

        # Get model from task or use default (gpt-4o is latest as of 2025)
        model = task.get("model", "gpt-4o")

        # Build system prompt
        system_prompt = f"""You are an AI agent executing a specific task for project orchestration.

Task ID: {task_id}
Title: {task['title']}

Your goal is to complete this task according to the specifications provided.
"""

        # Build user prompt with complete task specification
        user_prompt = f"""Please complete the following task:

{task['description']}

"""

        if task.get("deliverables"):
            user_prompt += "\nExpected Deliverables:\n"
            for deliverable in task["deliverables"]:
                user_prompt += f"- {deliverable}\n"

        if task.get("success_criteria"):
            user_prompt += "\nSuccess Criteria:\n"
            for criteria in task["success_criteria"]:
                user_prompt += f"- {criteria}\n"

        # Display execution info
        print(f"\n> Executing with GPT-4", file=sys.stderr)
        print(f"   Task ID: {task_id}", file=sys.stderr)
        print(f"   Model: {model}", file=sys.stderr)
        print(f"   Calling OpenAI API...\n", file=sys.stderr)

        # Call GPT-4 API (2025 SDK format)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=task.get("temperature", 0.7),
            max_tokens=task.get("max_tokens", 4000),
        )

        # Extract response
        output = response.choices[0].message.content

        # Calculate execution time
        execution_time = time.time() - start_time

        # Calculate tokens used
        tokens_used = response.usage.total_tokens
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        print(f"\n GPT-4 completed task", file=sys.stderr)
        print(f"   Tokens used: {tokens_used} (prompt: {prompt_tokens}, completion: {completion_tokens})", file=sys.stderr)
        print(f"   Execution time: {execution_time:.2f}s\n", file=sys.stderr)

        return {
            "status": "success",
            "output": output,
            "error": None,
            "task_id": task_id,
            "agent": task.get("agent", "gpt-4"),
            "model": model,
            "execution_time_seconds": execution_time,
            "tokens_used": tokens_used,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "timestamp": datetime.now().isoformat(),
            "exit_code": 0,
        }

    except Exception as e:
        from openai import AuthenticationError, RateLimitError, APIError

        # Handle specific OpenAI exceptions (2025 SDK format)
        if isinstance(e, AuthenticationError):
            return {
                "status": "failed",
                "error": "Invalid OpenAI API key",
                "task_id": task_id,
                "exit_code": 2,
                "timestamp": datetime.now().isoformat(),
            }

        elif isinstance(e, RateLimitError):
            return {
                "status": "failed",
                "error": "OpenAI API rate limit exceeded. Please try again later.",
                "task_id": task_id,
                "exit_code": 1,
                "timestamp": datetime.now().isoformat(),
            }

        elif isinstance(e, APIError):
            return {
                "status": "failed",
                "error": f"OpenAI API error: {str(e)}",
                "task_id": task_id,
                "exit_code": 1,
                "timestamp": datetime.now().isoformat(),
            }

    except Exception as e:
        return {
            "status": "failed",
            "error": f"Unexpected error: {str(e)}",
            "task_id": task_id,
            "exit_code": 1,
            "timestamp": datetime.now().isoformat(),
        }


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

        # Execute with GPT-4 API
        result = execute_gpt_api(task)

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
