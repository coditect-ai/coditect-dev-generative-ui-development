#!/usr/bin/env python3
"""
Execute Custom - Template for Custom LLM Endpoints
==================================================

Executes tasks using custom LLM endpoints (OpenAI-compatible or REST API).

Usage:
    echo '{"task_id": "TASK-001", ...}' | python execute_custom.py

Input (stdin): JSON task specification
Output (stdout): JSON execution result
Exit Codes:
    0 - Success
    1 - Execution error
    2 - Configuration error
    3 - Task specification error

Environment Variables:
    CUSTOM_LLM_API_KEY - API key for authentication
    CUSTOM_LLM_ENDPOINT - Full API endpoint URL
    CUSTOM_LLM_MODEL - Model name (optional)

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


def execute_custom_llm(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute task using custom LLM endpoint.

    Supports:
    - OpenAI-compatible endpoints
    - Generic REST APIs
    - Local LLMs (Ollama, LM Studio, etc.)

    Args:
        task: Task data dictionary

    Returns:
        Execution result dictionary
    """
    start_time = time.time()
    task_id = task["task_id"]

    # Get configuration from environment or task
    api_key = task.get("api_key") or os.getenv("CUSTOM_LLM_API_KEY")
    endpoint = task.get("endpoint") or os.getenv("CUSTOM_LLM_ENDPOINT")
    model = task.get("model") or os.getenv("CUSTOM_LLM_MODEL", "default")

    # Validate configuration
    if not endpoint:
        return {
            "status": "failed",
            "error": "CUSTOM_LLM_ENDPOINT not set. Set environment variable or pass in task.",
            "task_id": task_id,
            "exit_code": 2,
            "timestamp": datetime.now().isoformat(),
        }

    try:
        import requests
    except ImportError:
        return {
            "status": "failed",
            "error": "requests library not installed. Install with: pip install requests",
            "task_id": task_id,
            "exit_code": 2,
            "timestamp": datetime.now().isoformat(),
        }

    # Build prompt
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
    print(f"\n> Executing with Custom LLM", file=sys.stderr)
    print(f"   Task ID: {task_id}", file=sys.stderr)
    print(f"   Endpoint: {endpoint}", file=sys.stderr)
    print(f"   Model: {model}", file=sys.stderr)
    print(f"   Calling API...\n", file=sys.stderr)

    try:
        # Try OpenAI-compatible format first
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": task.get("temperature", 0.7),
            "max_tokens": task.get("max_tokens", 4000),
        }

        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=300  # 5 minute timeout
        )

        response.raise_for_status()

        # Parse response
        result = response.json()

        # Try to extract text from OpenAI-compatible format
        if "choices" in result and len(result["choices"]) > 0:
            output = result["choices"][0].get("message", {}).get("content", "")
            tokens_used = result.get("usage", {}).get("total_tokens")
        # Try generic text response
        elif "text" in result:
            output = result["text"]
            tokens_used = None
        # Try generic content response
        elif "content" in result:
            output = result["content"]
            tokens_used = None
        else:
            output = str(result)
            tokens_used = None

        execution_time = time.time() - start_time

        print(f"\n Custom LLM completed task", file=sys.stderr)
        if tokens_used:
            print(f"   Tokens used: {tokens_used}", file=sys.stderr)
        print(f"   Execution time: {execution_time:.2f}s\n", file=sys.stderr)

        response_data = {
            "status": "success",
            "output": output,
            "error": None,
            "task_id": task_id,
            "agent": task.get("agent", "custom"),
            "model": model,
            "endpoint": endpoint,
            "execution_time_seconds": execution_time,
            "timestamp": datetime.now().isoformat(),
            "exit_code": 0,
        }

        if tokens_used:
            response_data["tokens_used"] = tokens_used

        return response_data

    except requests.exceptions.Timeout:
        return {
            "status": "failed",
            "error": "Request timeout (5 minutes exceeded)",
            "task_id": task_id,
            "exit_code": 1,
            "timestamp": datetime.now().isoformat(),
        }

    except requests.exceptions.HTTPError as e:
        return {
            "status": "failed",
            "error": f"HTTP error: {e.response.status_code} - {e.response.text}",
            "task_id": task_id,
            "exit_code": 1,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": f"Custom LLM API error: {str(e)}",
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

        # Execute with custom LLM
        result = execute_custom_llm(task)

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
