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

