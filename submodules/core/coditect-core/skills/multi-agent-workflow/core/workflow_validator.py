#!/usr/bin/env python3
"""
Workflow Validator for FSM-based Recursive Workflows

Validates state transitions, checks iteration limits, and enforces workflow rules.
"""

from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass


class FSMState(Enum):
    """Valid FSM states for recursive workflows"""
    INITIATE = "INITIATE"
    IDENTIFY = "IDENTIFY"
    DOCUMENT = "DOCUMENT"
    SOLVE = "SOLVE"
    CODE = "CODE"
    DEPLOY = "DEPLOY"
    TEST = "TEST"
    VALIDATE = "VALIDATE"
    COMPLETE = "COMPLETE"
    CHECKPOINT = "CHECKPOINT"
    SUSPENDED = "SUSPENDED"
    ESCALATED = "ESCALATED"


@dataclass
class StateTransition:
    """Represents a state transition"""
    from_state: FSMState
    to_state: FSMState
    reason: str


class WorkflowValidator:
    """Validate FSM state transitions and workflow constraints"""

    # Maximum iteration limit
    MAX_ITERATIONS = 10

    # Valid state transitions (from_state -> [to_states])
    VALID_TRANSITIONS = {
        FSMState.INITIATE: [FSMState.IDENTIFY, FSMState.CHECKPOINT],
        FSMState.IDENTIFY: [FSMState.DOCUMENT, FSMState.CHECKPOINT, FSMState.ESCALATED],
        FSMState.DOCUMENT: [FSMState.SOLVE, FSMState.CHECKPOINT],
        FSMState.SOLVE: [FSMState.CODE, FSMState.IDENTIFY, FSMState.CHECKPOINT],
        FSMState.CODE: [FSMState.DEPLOY, FSMState.SOLVE, FSMState.CHECKPOINT],
        FSMState.DEPLOY: [FSMState.TEST, FSMState.CODE, FSMState.CHECKPOINT],
        FSMState.TEST: [FSMState.VALIDATE, FSMState.IDENTIFY, FSMState.SOLVE,
                        FSMState.CODE, FSMState.CHECKPOINT],
        FSMState.VALIDATE: [FSMState.COMPLETE, FSMState.IDENTIFY, FSMState.CHECKPOINT],
        FSMState.COMPLETE: [],  # Terminal state
        FSMState.CHECKPOINT: [FSMState.SUSPENDED],
        FSMState.SUSPENDED: [],  # Can resume to any saved state
        FSMState.ESCALATED: [],  # Terminal state (human intervention)
    }

    # Traceback logic (failure_type -> target_state)
    TRACEBACK_TARGETS = {
        "implementation_error": FSMState.CODE,
        "wrong_approach": FSMState.SOLVE,
        "misidentified_issue": FSMState.IDENTIFY,
        "missing_context": FSMState.DOCUMENT,
        "deployment_failure": FSMState.DEPLOY,
    }

    def __init__(self):
        self.iteration_count = 0
        self.transition_history = []

    def validate_transition(
        self, from_state: FSMState, to_state: FSMState
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate a state transition.

        Returns:
            (is_valid, error_message)
        """
        # Check if transition is allowed
        valid_targets = self.VALID_TRANSITIONS.get(from_state, [])

        if to_state not in valid_targets:
            return False, f"Invalid transition: {from_state.value} → {to_state.value}"

        # Special check: Can't transition from terminal states
        if from_state in [FSMState.COMPLETE, FSMState.ESCALATED]:
            return False, f"Cannot transition from terminal state: {from_state.value}"

        return True, None

    def traceback(
        self, failure_type: str, current_state: FSMState
    ) -> Tuple[FSMState, str]:
        """
        Determine target state for traceback based on failure type.

        Returns:
            (target_state, reason)
        """
        target = self.TRACEBACK_TARGETS.get(failure_type)

        if target is None:
            # Unknown failure type - escalate
            return FSMState.ESCALATED, f"Unknown failure type: {failure_type}"

        # Increment iteration count
        self.iteration_count += 1

        # Check iteration limit
        if self.iteration_count >= self.MAX_ITERATIONS:
            return FSMState.ESCALATED, f"Iteration limit exceeded ({self.MAX_ITERATIONS})"

        reason = f"Traceback due to {failure_type} (iteration {self.iteration_count})"
        return target, reason

    def record_transition(
        self, from_state: FSMState, to_state: FSMState, reason: str
    ):
        """Record a state transition"""
        transition = StateTransition(from_state, to_state, reason)
        self.transition_history.append(transition)

    def is_iteration_limit_exceeded(self) -> bool:
        """Check if iteration limit has been exceeded"""
        return self.iteration_count >= self.MAX_ITERATIONS

    def get_transition_count(self) -> int:
        """Get total number of transitions"""
        return len(self.transition_history)

    def get_iteration_count(self) -> int:
        """Get current iteration count"""
        return self.iteration_count

    def validate_workflow_state(
        self,
        current_state: FSMState,
        iteration_count: int,
        affected_modules: List[str],
    ) -> Tuple[bool, List[str]]:
        """
        Validate overall workflow state.

        Returns:
            (is_valid, warnings)
        """
        warnings = []
        is_valid = True

        # Check iteration count
        if iteration_count > 5:
            warnings.append(f"High iteration count ({iteration_count}). Consider ESCALATE.")

        if iteration_count >= self.MAX_ITERATIONS:
            warnings.append(f"MAX iteration limit reached ({self.MAX_ITERATIONS}). MUST escalate.")
            is_valid = False

        # Check module complexity
        if len(affected_modules) > 5:
            warnings.append(
                f"High module count ({len(affected_modules)}). Risk of cascading complexity."
            )

        # Check if stuck in loop
        if len(self.transition_history) > 3:
            recent = self.transition_history[-3:]
            states = [t.to_state for t in recent]
            if len(set(states)) < 3:
                warnings.append(
                    f"Possible loop detected: {' → '.join(s.value for s in states)}"
                )

        return is_valid, warnings

    def get_next_state_suggestions(
        self, current_state: FSMState
    ) -> List[Tuple[FSMState, str]]:
        """Get suggested next states with explanations"""
        valid_targets = self.VALID_TRANSITIONS.get(current_state, [])
        suggestions = []

        for target in valid_targets:
            if target == FSMState.CHECKPOINT:
                reason = "Save state before context collapse"
            elif target == FSMState.ESCALATED:
                reason = "Request human intervention"
            elif target == FSMState.COMPLETE:
                reason = "Workflow successfully completed"
            else:
                reason = f"Normal forward progress to {target.value}"

            suggestions.append((target, reason))

        return suggestions


def main():
    """Example usage"""
    validator = WorkflowValidator()

    # Example workflow
    transitions = [
        (FSMState.INITIATE, FSMState.IDENTIFY, "Start workflow"),
        (FSMState.IDENTIFY, FSMState.DOCUMENT, "Issue identified"),
        (FSMState.DOCUMENT, FSMState.SOLVE, "State captured"),
        (FSMState.SOLVE, FSMState.CODE, "Solution designed"),
        (FSMState.CODE, FSMState.DEPLOY, "Code implemented"),
        (FSMState.DEPLOY, FSMState.TEST, "Changes deployed"),
    ]

    print("=== Workflow Validation ===")
    for from_state, to_state, reason in transitions:
        is_valid, error = validator.validate_transition(from_state, to_state)
        if is_valid:
            validator.record_transition(from_state, to_state, reason)
            print(f"✓ {from_state.value} → {to_state.value}: {reason}")
        else:
            print(f"✗ {from_state.value} → {to_state.value}: {error}")

    # Simulate a test failure requiring traceback
    print("\n=== Traceback Example ===")
    target, reason = validator.traceback("implementation_error", FSMState.TEST)
    print(f"Traceback: TEST → {target.value}")
    print(f"Reason: {reason}")
    print(f"Iteration count: {validator.get_iteration_count()}")


if __name__ == "__main__":
    main()
