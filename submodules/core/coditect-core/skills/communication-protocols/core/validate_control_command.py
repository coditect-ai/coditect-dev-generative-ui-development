#!/usr/bin/env python3
"""
Control Command Validator

Validates CONTROL command syntax and semantics for multi-agent workflows.
"""

import re
from enum import Enum
from typing import Optional, Tuple
from dataclasses import dataclass


class ControlCommand(Enum):
    """Valid control commands"""
    PAUSE = "PAUSE"
    CHECKPOINT = "CHECKPOINT"
    ESCALATE = "ESCALATE"
    RESUME = "RESUME"
    DELEGATE = "DELEGATE"


@dataclass
class ParsedCommand:
    """Parsed control command structure"""
    command: ControlCommand
    argument: Optional[str] = None
    reason: Optional[str] = None


class ControlCommandValidator:
    """Validate control command syntax and semantics"""

    # Regex patterns
    COMMAND_PATTERN = r"^CONTROL:\s+(\w+)(?:\s+(.+?))?(?:\s+REASON:\s+(.+))?$"

    # Valid agents for DELEGATE command
    VALID_AGENTS = {
        "orchestrator",
        "codebase-analyzer",
        "codebase-locator",
        "codebase-pattern-finder",
        "thoughts-analyzer",
        "thoughts-locator",
        "web-search-researcher",
        "project-organizer",
    }

    def validate(self, command_str: str) -> Tuple[bool, Optional[str], Optional[ParsedCommand]]:
        """
        Validate a control command string.

        Returns:
            (is_valid, error_message, parsed_command)
        """
        # Check basic format
        match = re.match(self.COMMAND_PATTERN, command_str.strip())
        if not match:
            return False, "Invalid CONTROL command format. Expected: CONTROL: <COMMAND> [arg] [REASON: <reason>]", None

        command_name, argument, reason = match.groups()

        # Validate command exists
        try:
            command = ControlCommand[command_name.upper()]
        except KeyError:
            valid_commands = ", ".join([c.value for c in ControlCommand])
            return False, f"Unknown command '{command_name}'. Valid: {valid_commands}", None

        # Command-specific validation
        if command == ControlCommand.DELEGATE:
            if not argument:
                return False, "DELEGATE command requires agent name argument", None
            if argument not in self.VALID_AGENTS:
                valid = ", ".join(sorted(self.VALID_AGENTS))
                return False, f"Unknown agent '{argument}'. Valid agents: {valid}", None

        if command == ControlCommand.RESUME:
            if argument:
                # Validate checkpoint ID format (optional)
                if not re.match(r"^ckpt_[\w\-]+$", argument):
                    return False, f"Invalid checkpoint ID format: '{argument}'. Expected: ckpt_<name>", None

        if command == ControlCommand.CHECKPOINT:
            if not reason:
                return False, "CHECKPOINT command should include REASON (e.g., token usage, phase completion)", None

        if command == ControlCommand.ESCALATE:
            if not reason:
                return False, "ESCALATE command must include REASON explaining why human intervention needed", None

        # Build parsed result
        parsed = ParsedCommand(
            command=command,
            argument=argument,
            reason=reason
        )

        return True, None, parsed

    def validate_batch(self, commands: list[str]) -> dict:
        """
        Validate multiple commands and return summary.

        Returns:
            {
                "total": int,
                "valid": int,
                "invalid": int,
                "errors": [(command, error_msg), ...]
            }
        """
        results = {
            "total": len(commands),
            "valid": 0,
            "invalid": 0,
            "errors": []
        }

        for cmd in commands:
            is_valid, error, _ = self.validate(cmd)
            if is_valid:
                results["valid"] += 1
            else:
                results["invalid"] += 1
                results["errors"].append((cmd, error))

        return results

    def suggest_fix(self, command_str: str) -> Optional[str]:
        """
        Suggest a fix for common control command errors.

        Returns:
            Suggested corrected command string, or None if no suggestion
        """
        # Common mistake: missing "CONTROL:" prefix
        if not command_str.strip().startswith("CONTROL:"):
            for cmd in ControlCommand:
                if command_str.strip().upper().startswith(cmd.value):
                    return f"CONTROL: {command_str.strip()}"

        # Common mistake: missing colon after CONTROL
        if command_str.strip().startswith("CONTROL ") and ":" not in command_str[:10]:
            return command_str.replace("CONTROL ", "CONTROL: ", 1)

        # Common mistake: DELEGATE without agent
        if "DELEGATE" in command_str.upper() and not any(agent in command_str for agent in self.VALID_AGENTS):
            return f"{command_str.strip()} codebase-analyzer  # Specify target agent"

        return None


def main():
    """Example usage"""
    validator = ControlCommandValidator()

    # Test cases
    test_commands = [
        # Valid commands
        "CONTROL: PAUSE",
        "CONTROL: CHECKPOINT REASON: Token usage at 85%",
        "CONTROL: DELEGATE codebase-analyzer",
        "CONTROL: ESCALATE REASON: Max iterations exceeded",
        "CONTROL: RESUME ckpt_auth_phase2",

        # Invalid commands
        "PAUSE",  # Missing CONTROL: prefix
        "CONTROL CHECKPOINT",  # Missing colon
        "CONTROL: MAGIC",  # Invalid command
        "CONTROL: DELEGATE",  # Missing agent
        "CONTROL: DELEGATE unknown-agent",  # Unknown agent
        "CONTROL: ESCALATE",  # Missing reason
    ]

    print("=== Control Command Validation ===\n")

    for cmd in test_commands:
        is_valid, error, parsed = validator.validate(cmd)

        if is_valid:
            print(f"✓ VALID: {cmd}")
            print(f"  Command: {parsed.command.value}")
            if parsed.argument:
                print(f"  Argument: {parsed.argument}")
            if parsed.reason:
                print(f"  Reason: {parsed.reason}")
        else:
            print(f"✗ INVALID: {cmd}")
            print(f"  Error: {error}")

            # Try to suggest fix
            suggestion = validator.suggest_fix(cmd)
            if suggestion:
                print(f"  Suggestion: {suggestion}")

        print()

    # Batch validation
    print("\n=== Batch Validation Summary ===")
    summary = validator.validate_batch(test_commands)
    print(f"Total: {summary['total']}")
    print(f"Valid: {summary['valid']}")
    print(f"Invalid: {summary['invalid']}")

    if summary['errors']:
        print("\nErrors:")
        for cmd, error in summary['errors']:
            print(f"  - {cmd[:50]}... → {error}")


if __name__ == "__main__":
    main()
