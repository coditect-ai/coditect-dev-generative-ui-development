#!/usr/bin/env python3
"""
Delegation Template Generator

Generates YAML delegation templates for multi-agent coordination.
"""

import yaml
from typing import List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class DelegationType(Enum):
    """Types of delegation patterns"""
    STANDARD = "standard"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"


class Priority(Enum):
    """Task priority levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class DelegationTask:
    """Single delegation task"""
    agent: str
    task: str
    timeout: Optional[str] = None
    output_to: Optional[str] = None


@dataclass
class StandardDelegation:
    """Standard single-agent delegation"""
    from_agent: str
    to_agent: str
    task_description: str
    scope: List[str]
    deliverable: str
    context_phase: str
    token_budget: int
    priority: Priority


@dataclass
class ParallelDelegation:
    """Parallel multi-agent delegation"""
    coordinator: str
    agents: List[DelegationTask]
    aggregation_strategy: str


@dataclass
class SequentialDelegation:
    """Sequential delegation chain"""
    workflow: str
    steps: List[dict]


class DelegationTemplateGenerator:
    """Generate delegation templates for multi-agent coordination"""

    # Valid agents
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

    def generate_standard(
        self,
        from_agent: str,
        to_agent: str,
        task_description: str,
        scope: List[str],
        deliverable: str,
        context_phase: str,
        token_budget: int = 10000,
        priority: Priority = Priority.MEDIUM
    ) -> str:
        """
        Generate standard delegation template.

        Args:
            from_agent: Agent delegating the task
            to_agent: Agent receiving the task
            task_description: What needs to be done
            scope: Files/directories to analyze
            deliverable: Expected output format
            context_phase: Current workflow phase
            token_budget: Maximum tokens for this task
            priority: Task priority level

        Returns:
            YAML string for delegation
        """
        if to_agent not in self.VALID_AGENTS:
            raise ValueError(f"Unknown agent: {to_agent}. Valid: {sorted(self.VALID_AGENTS)}")

        delegation = {
            "delegation": {
                "from_agent": from_agent,
                "to_agent": to_agent,
                "task": {
                    "description": task_description,
                    "scope": scope,
                    "deliverable": deliverable
                },
                "context": {
                    "current_phase": context_phase,
                    "token_budget": token_budget,
                    "priority": priority.value
                }
            }
        }

        return yaml.dump(delegation, default_flow_style=False, sort_keys=False)

    def generate_parallel(
        self,
        coordinator: str,
        tasks: List[DelegationTask],
        aggregation_strategy: str = "Wait for all, merge results by priority"
    ) -> str:
        """
        Generate parallel delegation template.

        Args:
            coordinator: Orchestrating agent (usually "orchestrator")
            tasks: List of DelegationTask objects
            aggregation_strategy: How to combine results

        Returns:
            YAML string for parallel delegation
        """
        for task in tasks:
            if task.agent not in self.VALID_AGENTS:
                raise ValueError(f"Unknown agent: {task.agent}")

        delegation = {
            "parallel_delegation": {
                "coordinator": coordinator,
                "agents": [
                    {
                        "agent": t.agent,
                        "task": t.task,
                        **({"timeout": t.timeout} if t.timeout else {})
                    }
                    for t in tasks
                ],
                "aggregation_strategy": aggregation_strategy
            }
        }

        return yaml.dump(delegation, default_flow_style=False, sort_keys=False)

    def generate_sequential(
        self,
        workflow: str,
        steps: List[DelegationTask]
    ) -> str:
        """
        Generate sequential delegation chain template.

        Args:
            workflow: Name of the workflow
            steps: List of DelegationTask objects in execution order

        Returns:
            YAML string for sequential delegation
        """
        for step in steps:
            if step.agent not in self.VALID_AGENTS:
                raise ValueError(f"Unknown agent: {step.agent}")

        delegation = {
            "sequential_delegation": {
                "workflow": workflow,
                "steps": [
                    {
                        "step": i + 1,
                        "agent": step.agent,
                        "task": step.task,
                        **({"output_to": step.output_to} if step.output_to else {})
                    }
                    for i, step in enumerate(steps)
                ]
            }
        }

        return yaml.dump(delegation, default_flow_style=False, sort_keys=False)

    def generate_common_patterns(self) -> dict:
        """
        Generate common delegation patterns.

        Returns:
            Dictionary of pattern_name -> yaml_template
        """
        patterns = {}

        # Pattern 1: Code Analysis
        patterns["code_analysis"] = self.generate_standard(
            from_agent="orchestrator",
            to_agent="codebase-analyzer",
            task_description="Analyze authentication implementation for security vulnerabilities",
            scope=[
                "backend/src/handlers/auth.rs",
                "backend/src/middleware/auth.rs"
            ],
            deliverable="Security vulnerability report with file:line references",
            context_phase="Security Audit",
            token_budget=12000,
            priority=Priority.HIGH
        )

        # Pattern 2: File Location
        patterns["file_location"] = self.generate_parallel(
            coordinator="orchestrator",
            tasks=[
                DelegationTask(
                    agent="codebase-locator",
                    task="Find all JWT-related files",
                    timeout="5min"
                ),
                DelegationTask(
                    agent="thoughts-locator",
                    task="Find authentication design decisions",
                    timeout="3min"
                )
            ]
        )

        # Pattern 3: Bug Fix Pipeline
        patterns["bug_fix_pipeline"] = self.generate_sequential(
            workflow="Bug Fix Pipeline",
            steps=[
                DelegationTask(
                    agent="codebase-locator",
                    task="Locate files related to bug #1234",
                    output_to="step_2_input"
                ),
                DelegationTask(
                    agent="codebase-analyzer",
                    task="Analyze root cause in {step_2_input}",
                    output_to="step_3_input"
                ),
                DelegationTask(
                    agent="orchestrator",
                    task="Implement fix based on {step_3_input}"
                )
            ]
        )

        # Pattern 4: Research Phase
        patterns["research_phase"] = self.generate_parallel(
            coordinator="orchestrator",
            tasks=[
                DelegationTask(
                    agent="codebase-locator",
                    task="Find all session management files",
                    timeout="5min"
                ),
                DelegationTask(
                    agent="codebase-pattern-finder",
                    task="Extract session creation patterns",
                    timeout="10min"
                ),
                DelegationTask(
                    agent="thoughts-locator",
                    task="Find session management requirements",
                    timeout="3min"
                )
            ],
            aggregation_strategy="Wait for all, create comprehensive research report"
        )

        return patterns


def main():
    """Example usage"""
    generator = DelegationTemplateGenerator()

    print("=== Delegation Template Generator ===\n")

    # Example 1: Standard delegation
    print("1. STANDARD DELEGATION (Security Audit)")
    print("-" * 60)
    standard = generator.generate_standard(
        from_agent="orchestrator",
        to_agent="codebase-analyzer",
        task_description="Analyze authentication flow for security vulnerabilities",
        scope=[
            "backend/src/handlers/auth.rs",
            "backend/src/middleware/auth.rs"
        ],
        deliverable="Vulnerability report with severity levels and file:line references",
        context_phase="Security Audit - Phase 1",
        token_budget=15000,
        priority=Priority.HIGH
    )
    print(standard)

    # Example 2: Parallel delegation
    print("\n2. PARALLEL DELEGATION (Research Phase)")
    print("-" * 60)
    parallel = generator.generate_parallel(
        coordinator="orchestrator",
        tasks=[
            DelegationTask(
                agent="codebase-locator",
                task="Find all authentication-related files",
                timeout="5min"
            ),
            DelegationTask(
                agent="codebase-analyzer",
                task="Analyze JWT implementation",
                timeout="10min"
            ),
            DelegationTask(
                agent="thoughts-locator",
                task="Find auth design decisions",
                timeout="3min"
            )
        ],
        aggregation_strategy="Wait for all, create comprehensive auth analysis report"
    )
    print(parallel)

    # Example 3: Sequential delegation
    print("\n3. SEQUENTIAL DELEGATION (Bug Fix Pipeline)")
    print("-" * 60)
    sequential = generator.generate_sequential(
        workflow="Bug Fix Pipeline - Issue #1234",
        steps=[
            DelegationTask(
                agent="codebase-locator",
                task="Locate files related to session timeout bug",
                output_to="step_2_input"
            ),
            DelegationTask(
                agent="codebase-analyzer",
                task="Analyze root cause in {step_2_input}",
                output_to="step_3_input"
            ),
            DelegationTask(
                agent="orchestrator",
                task="Implement fix based on analysis: {step_3_input}"
            )
        ]
    )
    print(sequential)

    # Example 4: Common patterns
    print("\n4. COMMON PATTERNS")
    print("-" * 60)
    patterns = generator.generate_common_patterns()
    print(f"Generated {len(patterns)} common patterns:")
    for pattern_name in patterns.keys():
        print(f"  - {pattern_name}")


if __name__ == "__main__":
    main()
