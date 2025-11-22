#!/usr/bin/env python3
"""
Error Recovery & Resilience Hook for CODITECT

Implements automatic error recovery, circuit breaker patterns, and resilience strategies.
Enables graceful degradation and automatic retries for transient failures.

Event: PostToolUse (all tools)
Matcher: tool_name = "*" (all tools)
Trigger: After tool execution to detect and handle failures
"""

import json
import sys
import os
import time
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class ErrorRecoveryManager:
    """Manages error recovery and resilience"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.circuit_breaker_file = self.repo_root / '.coditect' / 'hooks' / '.circuit-breaker.json'
        self.retry_policy_file = self.repo_root / '.coditect' / 'hooks' / '.retry-policy.json'
        self.error_log_file = self.repo_root / '.coditect' / 'hooks' / '.error-recovery.log'
        self.circuit_breakers = self.load_circuit_breakers()
        self.default_retry_policy = {
            'max_retries': 3,
            'initial_delay': 1,
            'max_delay': 30,
            'backoff_multiplier': 2,
            'jitter': True
        }

    def load_circuit_breakers(self) -> Dict:
        """Load circuit breaker states"""
        if self.circuit_breaker_file.exists():
            try:
                with open(self.circuit_breaker_file, 'r') as f:
                    import json as json_module
                    return json_module.load(f)
            except Exception:
                return {}
        return {}

    def save_circuit_breakers(self):
        """Save circuit breaker states"""
        try:
            with open(self.circuit_breaker_file, 'w') as f:
                import json as json_module
                json_module.dump(self.circuit_breakers, f, indent=2)
        except Exception:
            pass

    def check_circuit_breaker(self, component: str) -> Dict:
        """Check circuit breaker status for component"""

        if component not in self.circuit_breakers:
            self.circuit_breakers[component] = {
                'state': 'closed',
                'failure_count': 0,
                'last_failure': None,
                'timeout': 60
            }

        breaker = self.circuit_breakers[component]

        # Check if breaker should be reset (timeout elapsed)
        if breaker['state'] == 'open':
            last_failure = datetime.fromisoformat(breaker['last_failure'])
            timeout = timedelta(seconds=breaker['timeout'])

            if datetime.now() - last_failure > timeout:
                # Reset to half-open for retry
                breaker['state'] = 'half-open'
                breaker['failure_count'] = 0

        return breaker

    def record_failure(self, component: str, error: str):
        """Record failure for circuit breaker"""

        if component not in self.circuit_breakers:
            self.circuit_breakers[component] = {
                'state': 'closed',
                'failure_count': 0,
                'last_failure': None,
                'timeout': 60
            }

        breaker = self.circuit_breakers[component]
        breaker['failure_count'] += 1
        breaker['last_failure'] = datetime.now().isoformat()

        # Open circuit breaker after 5 failures
        if breaker['failure_count'] >= 5:
            breaker['state'] = 'open'
            breaker['timeout'] = min(breaker['timeout'] * 2, 300)  # Exponential backoff, max 5 min

        self.save_circuit_breakers()

    def record_success(self, component: str):
        """Record success, close circuit breaker"""

        if component in self.circuit_breakers:
            breaker = self.circuit_breakers[component]
            breaker['state'] = 'closed'
            breaker['failure_count'] = 0
            breaker['last_failure'] = None
            breaker['timeout'] = 60
            self.save_circuit_breakers()

    def get_retry_policy(self, error_type: str) -> Dict:
        """Get retry policy for error type"""

        policies = {
            'transient': {  # Connection errors, timeouts, rate limiting
                'max_retries': 3,
                'initial_delay': 0.5,
                'max_delay': 30,
                'backoff_multiplier': 2
            },
            'permanent': {  # Invalid input, authorization errors
                'max_retries': 0,
                'skip_retry': True
            },
            'unknown': {  # Unknown errors
                'max_retries': 1,
                'initial_delay': 1,
                'max_delay': 10,
                'backoff_multiplier': 2
            }
        }

        return policies.get(error_type, policies['unknown'])

    def classify_error(self, error: str, exit_code: int) -> str:
        """Classify error for recovery strategy"""

        error_lower = error.lower()

        # Transient errors
        transient_patterns = [
            'connection', 'timeout', 'temporarily', 'rate limit',
            'busy', 'unavailable', 'try again', 'econnrefused',
            'network', 'remote', 'refused', 'broken pipe'
        ]

        for pattern in transient_patterns:
            if pattern in error_lower:
                return 'transient'

        # Permanent errors
        permanent_patterns = [
            'invalid', 'permission', 'denied', 'forbidden', 'unauthorized',
            'not found', 'syntax', 'parse', 'auth', 'forbidden', 'not found'
        ]

        for pattern in permanent_patterns:
            if pattern in error_lower:
                return 'permanent'

        # Exit code indicators
        if exit_code == 0:
            return 'success'
        elif exit_code in [401, 403, 404, 422]:
            return 'permanent'
        elif exit_code in [429, 500, 502, 503]:
            return 'transient'

        return 'unknown'

    def calculate_backoff_delay(self, attempt: int, policy: Dict) -> float:
        """Calculate backoff delay for retry"""

        initial = policy['initial_delay']
        multiplier = policy['backoff_multiplier']
        max_delay = policy['max_delay']

        # Exponential backoff: initial * multiplier^(attempt-1)
        delay = initial * (multiplier ** (attempt - 1))

        # Cap at max_delay
        delay = min(delay, max_delay)

        # Add jitter (random variation)
        if policy.get('jitter'):
            import random
            jitter = random.uniform(0, delay * 0.1)
            delay += jitter

        return delay

    def log_error_recovery(self, component: str, error: str, recovery_action: str):
        """Log error recovery attempt"""

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'component': component,
            'error': error,
            'recovery_action': recovery_action
        }

        try:
            with open(self.error_log_file, 'a') as f:
                import json as json_module
                f.write(json_module.dumps(log_entry) + '\n')
        except Exception:
            pass

    def get_recovery_suggestions(self, error_type: str, component: str) -> List[str]:
        """Get recovery suggestions for error"""

        suggestions = {
            'transient': [
                'Retry with exponential backoff',
                'Check network connectivity',
                'Wait for service recovery',
                'Use circuit breaker pattern'
            ],
            'permanent': [
                'Review error message and fix root cause',
                'Check permissions and authentication',
                'Verify input parameters',
                'Check component configuration'
            ],
            'unknown': [
                'Check logs for details',
                'Verify system resources (disk, memory)',
                'Check recent changes',
                'Enable debug logging'
            ]
        }

        return suggestions.get(error_type, [])


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract information
        exit_code = hook_input.get('exit_code', 0)
        error_message = hook_input.get('error_message', '')
        tool_name = hook_input.get('tool_name', 'Unknown')
        event = hook_input.get('event', 'PostToolUse')

        # Get repo root
        script_dir = Path(__file__).parent.parent.parent
        repo_root = str(script_dir)

        # Initialize error recovery
        recovery = ErrorRecoveryManager(repo_root)

        # No error, record success
        if exit_code == 0:
            recovery.record_success(tool_name)
            print(json.dumps({"continue": True, "suppressOutput": True}))
            sys.exit(0)

        # Error occurred
        error_type = recovery.classify_error(error_message, exit_code)
        retry_policy = recovery.get_retry_policy(error_type)

        # Check circuit breaker
        breaker = recovery.check_circuit_breaker(tool_name)

        result = {
            "continue": True,
            "suppressOutput": True,
            "error_recovery": {
                "error_type": error_type,
                "circuit_breaker_state": breaker['state'],
                "can_retry": breaker['state'] != 'open'
            }
        }

        # Add recovery suggestions
        if error_type == 'transient':
            suggestions = recovery.get_recovery_suggestions(error_type, tool_name)
            recovery.log_error_recovery(tool_name, error_message, f"Transient error - retry recommended")
            result['suggestions'] = suggestions

        elif error_type == 'permanent':
            suggestions = recovery.get_recovery_suggestions(error_type, tool_name)
            recovery.log_error_recovery(tool_name, error_message, f"Permanent error - review and fix")
            result['suggestions'] = suggestions

        # Record failure
        recovery.record_failure(tool_name, error_message)

        # If circuit breaker is open, warn user
        if breaker['state'] == 'open':
            result['warning'] = f"Circuit breaker open for {tool_name}. Wait {breaker['timeout']}s before retry."

        print(json.dumps(result))
        sys.exit(0)

    except json.JSONDecodeError:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"continue": True, "suppressOutput": True}))
        sys.exit(0)


if __name__ == '__main__':
    main()
