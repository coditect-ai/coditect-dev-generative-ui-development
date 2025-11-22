#!/usr/bin/env python3
"""
FSM Validator

Validates finite state machine definitions and transitions.
"""

from enum import Enum
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TransitionRule:
    """Transition rule with optional guard and action"""
    from_state: str
    to_state: str
    trigger: str
    guard: Optional[str] = None  # Condition expression
    action: Optional[str] = None  # Side effect to execute


class FSMValidator:
    """Validate FSM structure and behavior"""

    def __init__(self):
        self.states: Set[str] = set()
        self.triggers: Set[str] = set()
        self.transitions: List[TransitionRule] = []
        self.initial_state: Optional[str] = None
        self.terminal_states: Set[str] = set()

    def add_state(self, state: str, is_initial: bool = False, is_terminal: bool = False):
        """Add a state to the FSM"""
        self.states.add(state)
        if is_initial:
            self.initial_state = state
        if is_terminal:
            self.terminal_states.add(state)

    def add_transition(
        self,
        from_state: str,
        to_state: str,
        trigger: str,
        guard: Optional[str] = None,
        action: Optional[str] = None
    ):
        """Add a transition rule"""
        if from_state not in self.states:
            raise ValueError(f"Unknown state: {from_state}")
        if to_state not in self.states:
            raise ValueError(f"Unknown state: {to_state}")

        self.triggers.add(trigger)
        self.transitions.append(
            TransitionRule(from_state, to_state, trigger, guard, action)
        )

    def validate_structure(self) -> Tuple[bool, List[str]]:
        """
        Validate FSM structure.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Check 1: Must have at least one state
        if len(self.states) == 0:
            errors.append("FSM has no states defined")

        # Check 2: Must have an initial state
        if self.initial_state is None:
            errors.append("FSM has no initial state")
        elif self.initial_state not in self.states:
            errors.append(f"Initial state '{self.initial_state}' not in state list")

        # Check 3: Terminal states should have no outgoing transitions
        for trans in self.transitions:
            if trans.from_state in self.terminal_states:
                errors.append(
                    f"Terminal state '{trans.from_state}' has outgoing transition to '{trans.to_state}'"
                )

        # Check 4: All states should be reachable from initial state
        reachable = self._find_reachable_states()
        unreachable = self.states - reachable
        if unreachable:
            errors.append(f"Unreachable states: {', '.join(unreachable)}")

        # Check 5: Should have at least one terminal state (or cycle)
        if len(self.terminal_states) == 0:
            has_cycle = self._has_cycle()
            if not has_cycle:
                errors.append("FSM has no terminal states and no cycles (dead end)")

        # Check 6: Duplicate transitions
        seen = set()
        for trans in self.transitions:
            key = (trans.from_state, trans.trigger)
            if key in seen:
                errors.append(
                    f"Duplicate transition from '{trans.from_state}' on trigger '{trans.trigger}'"
                )
            seen.add(key)

        return (len(errors) == 0, errors)

    def _find_reachable_states(self) -> Set[str]:
        """Find all states reachable from initial state"""
        if self.initial_state is None:
            return set()

        reachable = {self.initial_state}
        queue = [self.initial_state]

        while queue:
            current = queue.pop(0)
            for trans in self.transitions:
                if trans.from_state == current and trans.to_state not in reachable:
                    reachable.add(trans.to_state)
                    queue.append(trans.to_state)

        return reachable

    def _has_cycle(self) -> bool:
        """Check if FSM has any cycles"""
        visited = set()
        rec_stack = set()

        def visit(state: str) -> bool:
            visited.add(state)
            rec_stack.add(state)

            # Visit all neighbors
            for trans in self.transitions:
                if trans.from_state == state:
                    neighbor = trans.to_state
                    if neighbor not in visited:
                        if visit(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True  # Cycle detected

            rec_stack.remove(state)
            return False

        # Check from initial state
        if self.initial_state:
            return visit(self.initial_state)
        return False

    def validate_transition(
        self,
        current_state: str,
        trigger: str
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate a specific transition.

        Returns:
            (is_valid, next_state_if_valid, error_message_if_invalid)
        """
        if current_state not in self.states:
            return (False, None, f"Unknown state: {current_state}")

        # Find matching transition
        matching = [
            t for t in self.transitions
            if t.from_state == current_state and t.trigger == trigger
        ]

        if len(matching) == 0:
            return (
                False,
                None,
                f"No transition from '{current_state}' on trigger '{trigger}'"
            )

        # Return first match (guards would be evaluated at runtime)
        trans = matching[0]
        return (True, trans.to_state, None)

    def get_valid_triggers(self, current_state: str) -> List[str]:
        """Get all valid triggers from current state"""
        return [
            t.trigger for t in self.transitions
            if t.from_state == current_state
        ]

    def get_state_info(self, state: str) -> dict:
        """Get information about a state"""
        if state not in self.states:
            return {"error": "Unknown state"}

        outgoing = [t for t in self.transitions if t.from_state == state]
        incoming = [t for t in self.transitions if t.to_state == state]

        return {
            "state": state,
            "is_initial": state == self.initial_state,
            "is_terminal": state in self.terminal_states,
            "outgoing_transitions": len(outgoing),
            "incoming_transitions": len(incoming),
            "valid_triggers": self.get_valid_triggers(state),
        }

    def generate_diagram(self) -> str:
        """Generate Mermaid state diagram"""
        lines = ["```mermaid", "stateDiagram-v2"]

        # Define initial state
        if self.initial_state:
            lines.append(f"    [*] --> {self.initial_state}")

        # Define transitions
        for trans in self.transitions:
            guard_str = f" [{trans.guard}]" if trans.guard else ""
            action_str = f" / {trans.action}" if trans.action else ""
            lines.append(
                f"    {trans.from_state} --> {trans.to_state}: {trans.trigger}{guard_str}{action_str}"
            )

        # Define terminal states
        for terminal in self.terminal_states:
            lines.append(f"    {terminal} --> [*]")

        lines.append("```")
        return "\n".join(lines)


def create_t2_recursive_workflow_fsm() -> FSMValidator:
    """Create T2 recursive workflow FSM"""
    fsm = FSMValidator()

    # Add states
    states = [
        "INITIATE", "IDENTIFY", "DOCUMENT", "SOLVE", "CODE",
        "DEPLOY", "TEST", "VALIDATE", "COMPLETE",
        "CHECKPOINT", "SUSPENDED", "ESCALATED"
    ]

    for state in states:
        is_initial = (state == "INITIATE")
        is_terminal = (state in ["COMPLETE", "SUSPENDED", "ESCALATED"])
        fsm.add_state(state, is_initial=is_initial, is_terminal=is_terminal)

    # Add forward transitions
    fsm.add_transition("INITIATE", "IDENTIFY", "start")
    fsm.add_transition("IDENTIFY", "DOCUMENT", "issue_identified")
    fsm.add_transition("DOCUMENT", "SOLVE", "context_captured")
    fsm.add_transition("SOLVE", "CODE", "solution_designed")
    fsm.add_transition("CODE", "DEPLOY", "code_implemented")
    fsm.add_transition("DEPLOY", "TEST", "changes_deployed")
    fsm.add_transition("TEST", "VALIDATE", "tests_passed")
    fsm.add_transition("VALIDATE", "COMPLETE", "validation_successful")

    # Add traceback transitions
    fsm.add_transition("TEST", "IDENTIFY", "traceback_misidentified")
    fsm.add_transition("TEST", "SOLVE", "traceback_wrong_approach")
    fsm.add_transition("TEST", "CODE", "traceback_implementation_error")
    fsm.add_transition("SOLVE", "IDENTIFY", "traceback_misidentified")
    fsm.add_transition("CODE", "SOLVE", "traceback_wrong_approach")
    fsm.add_transition("DEPLOY", "CODE", "traceback_deployment_error")
    fsm.add_transition("VALIDATE", "IDENTIFY", "traceback_misidentified")

    # Add checkpoint transitions
    for state in ["INITIATE", "IDENTIFY", "DOCUMENT", "SOLVE", "CODE", "DEPLOY", "TEST", "VALIDATE"]:
        fsm.add_transition(state, "CHECKPOINT", "checkpoint",
                          guard="token_usage >= 85%",
                          action="save_state()")

    fsm.add_transition("CHECKPOINT", "SUSPENDED", "suspend")

    # Add escalation transitions
    fsm.add_transition("IDENTIFY", "ESCALATED", "escalate",
                      guard="iteration_count >= 10")

    return fsm


def main():
    """Example usage"""
    print("=== FSM Validator ===\n")

    # Create T2 recursive workflow FSM
    fsm = create_t2_recursive_workflow_fsm()

    # Validate structure
    print("1. STRUCTURE VALIDATION")
    print("-" * 60)
    is_valid, errors = fsm.validate_structure()
    if is_valid:
        print("✓ FSM structure is valid")
    else:
        print("✗ FSM structure has errors:")
        for error in errors:
            print(f"  - {error}")
    print()

    # Test specific transitions
    print("2. TRANSITION VALIDATION")
    print("-" * 60)

    test_cases = [
        ("INITIATE", "start"),
        ("TEST", "tests_passed"),
        ("TEST", "traceback_implementation_error"),
        ("COMPLETE", "any_trigger"),  # Should fail (terminal state)
        ("UNKNOWN", "start"),  # Should fail (unknown state)
    ]

    for state, trigger in test_cases:
        is_valid, next_state, error = fsm.validate_transition(state, trigger)
        if is_valid:
            print(f"✓ {state} --[{trigger}]--> {next_state}")
        else:
            print(f"✗ {state} --[{trigger}]--> ERROR: {error}")
    print()

    # State information
    print("3. STATE INFORMATION")
    print("-" * 60)
    for state in ["INITIATE", "TEST", "COMPLETE"]:
        info = fsm.get_state_info(state)
        print(f"{state}:")
        print(f"  Initial: {info['is_initial']}")
        print(f"  Terminal: {info['is_terminal']}")
        print(f"  Outgoing: {info['outgoing_transitions']}")
        print(f"  Incoming: {info['incoming_transitions']}")
        print(f"  Valid triggers: {', '.join(info['valid_triggers'])}")
        print()

    # Generate diagram
    print("4. STATE DIAGRAM")
    print("-" * 60)
    print(fsm.generate_diagram())


if __name__ == "__main__":
    main()
