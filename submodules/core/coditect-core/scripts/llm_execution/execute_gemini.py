#!/usr/bin/env python3
"""
Execute Gemini - Standardized Google Gemini Execution Script
===========================================================

Executes tasks using Google Gemini via API.

Usage:
    echo '{"task_id": "TASK-001", ...}' | python execute_gemini.py

Input (stdin): JSON task specification
Output (stdout): JSON execution result
Exit Codes:
    0 - Success
    1 - Execution error
    2 - Configuration error (missing API key)
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


def execute_gemini_api(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute task using Google Gemini API.

    Args:
        task: Task data dictionary

    Returns:
        Execution result dictionary
    """
    start_time = time.time()
    task_id = task["task_id"]

    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {
            "status": "failed",
            "error": "GOOGLE_API_KEY environment variable not set",
            "task_id": task_id,
            "exit_code": 2,
            "timestamp": datetime.now().isoformat(),
        }

    try:
        # Import Gemini library (NEW google-genai SDK, GA Nov 5, 2025)
        try:
            from google import genai
        except ImportError:
            return {
                "status": "failed",
                "error": "google-genai library not installed. Install with: pip install google-genai",
                "task_id": task_id,
                "exit_code": 2,
                "timestamp": datetime.now().isoformat(),
            }

        # Initialize Gemini client (2025 SDK)
        client = genai.Client(api_key=api_key)

        # Get model from task or use default (gemini-2.5-flash is latest free tier)
        model_name = task.get("model", "gemini-3.0-ultra")

        # Build prompt with complete task specification
        prompt = f"""You are an AI agent executing a specific task for project orchestration.

Task ID: {task_id}
Title: {task['title']}

Task Description:
{task['description']}

"""

        if task.get("deliverables"):
            prompt += "\nExpected Deliverables:\n"
            for deliverable in task["deliverables"]:
                prompt += f"- {deliverable}\n"

        if task.get("success_criteria"):
            prompt += "\nSuccess Criteria:\n"
            for criteria in task["success_criteria"]:
                prompt += f"- {criteria}\n"

        prompt += "\nPlease complete this task according to the specifications provided."

        # Display execution info
        print(f"\n> Executing with Gemini", file=sys.stderr)
        print(f"   Task ID: {task_id}", file=sys.stderr)
        print(f"   Model: {model_name}", file=sys.stderr)
        print(f"   Calling Google Gemini API...\n", file=sys.stderr)

        # Generate content (2025 SDK format)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={
                'temperature': task.get("temperature", 0.7),
                'max_output_tokens': task.get("max_tokens", 4000),
            }
        )

        # Extract response
        output = response.text

        # Calculate execution time
        execution_time = time.time() - start_time

        # Get token counts if available
        tokens_used = None
        prompt_tokens = None
        completion_tokens = None

        if hasattr(response, 'usage_metadata'):
            prompt_tokens = getattr(response.usage_metadata, 'prompt_token_count', None)
            completion_tokens = getattr(response.usage_metadata, 'candidates_token_count', None)
            if prompt_tokens and completion_tokens:
                tokens_used = prompt_tokens + completion_tokens

        print(f"\n Gemini completed task", file=sys.stderr)
        if tokens_used:
            print(f"   Tokens used: {tokens_used} (prompt: {prompt_tokens}, completion: {completion_tokens})", file=sys.stderr)
        print(f"   Execution time: {execution_time:.2f}s\n", file=sys.stderr)

        result = {
            "status": "success",
            "output": output,
            "error": None,
            "task_id": task_id,
            "agent": task.get("agent", "gemini-pro"),
            "model": model_name,
            "execution_time_seconds": execution_time,
            "timestamp": datetime.now().isoformat(),
            "exit_code": 0,
        }

        if tokens_used:
            result["tokens_used"] = tokens_used
            result["prompt_tokens"] = prompt_tokens
            result["completion_tokens"] = completion_tokens

        return result

    except Exception as e:
        error_message = str(e)

        # Check for specific error types
        if "API key" in error_message or "authentication" in error_message.lower():
            exit_code = 2
            error_message = f"Invalid Google API key: {error_message}"
        elif "quota" in error_message.lower() or "rate limit" in error_message.lower():
            exit_code = 1
            error_message = f"Gemini API rate limit exceeded: {error_message}"
        else:
            exit_code = 1
            error_message = f"Gemini API error: {error_message}"

        return {
            "status": "failed",
            "error": error_message,
            "task_id": task_id,
            "exit_code": exit_code,
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

        # Execute with Gemini API
        result = execute_gemini_api(task)

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
