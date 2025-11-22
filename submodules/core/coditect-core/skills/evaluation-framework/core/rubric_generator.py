#!/usr/bin/env python3
"""
Rubric Generator

Utilities for generating evaluation rubrics for different domains.
"""

from typing import List, Dict
from dataclasses import dataclass
from enum import Enum


class ScoreLevel(Enum):
    """Standardized score levels"""
    EXCELLENT = 5
    GOOD = 4
    ADEQUATE = 3
    POOR = 2
    FAILING = 1


@dataclass
class EvaluationCriterion:
    """Single evaluation criterion"""
    name: str
    description: str
    weight: float
    scoring_guide: Dict[ScoreLevel, str]


class RubricGenerator:
    """Generate evaluation rubrics for different domains"""

    def generate_code_quality_rubric(self) -> List[EvaluationCriterion]:
        """Generate rubric for code quality evaluation"""
        return [
            EvaluationCriterion(
                name="Correctness",
                description="Code works as intended and handles edge cases",
                weight=0.30,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Handles all cases including edge cases, no bugs",
                    ScoreLevel.GOOD: "Handles main cases correctly, minor edge case issues",
                    ScoreLevel.ADEQUATE: "Core functionality works, some edge case bugs",
                    ScoreLevel.POOR: "Core functionality has bugs",
                    ScoreLevel.FAILING: "Does not work as intended",
                }
            ),
            EvaluationCriterion(
                name="Code Structure",
                description="Organization and clarity of code",
                weight=0.20,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Well-organized, clear separation of concerns, DRY",
                    ScoreLevel.GOOD: "Organized, minor repetition",
                    ScoreLevel.ADEQUATE: "Functional organization, some repetition",
                    ScoreLevel.POOR: "Poor organization, significant repetition",
                    ScoreLevel.FAILING: "Unstructured, unmaintainable",
                }
            ),
            EvaluationCriterion(
                name="Error Handling",
                description="Handling of errors and edge cases",
                weight=0.15,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Comprehensive error handling with recovery, detailed messages",
                    ScoreLevel.GOOD: "Good error handling, clear messages",
                    ScoreLevel.ADEQUATE: "Basic error handling present",
                    ScoreLevel.POOR: "Minimal error handling",
                    ScoreLevel.FAILING: "No error handling",
                }
            ),
            EvaluationCriterion(
                name="Documentation",
                description="Code documentation and comments",
                weight=0.10,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Comprehensive docs, examples, edge cases documented",
                    ScoreLevel.GOOD: "Good documentation coverage",
                    ScoreLevel.ADEQUATE: "Basic documentation present",
                    ScoreLevel.POOR: "Minimal documentation",
                    ScoreLevel.FAILING: "No documentation",
                }
            ),
            EvaluationCriterion(
                name="Type Safety",
                description="Use of type hints and type checking",
                weight=0.10,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Full type hints, passes strict type checking",
                    ScoreLevel.GOOD: "Good type coverage (>80%)",
                    ScoreLevel.ADEQUATE: "Basic type hints (>50%)",
                    ScoreLevel.POOR: "Minimal type hints (<50%)",
                    ScoreLevel.FAILING: "No type hints",
                }
            ),
            EvaluationCriterion(
                name="Performance",
                description="Algorithm efficiency and resource usage",
                weight=0.10,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Optimal algorithms, efficient implementation",
                    ScoreLevel.GOOD: "Good performance, room for minor optimization",
                    ScoreLevel.ADEQUATE: "Acceptable performance",
                    ScoreLevel.POOR: "Performance issues",
                    ScoreLevel.FAILING: "Unacceptable performance",
                }
            ),
            EvaluationCriterion(
                name="Security",
                description="Security best practices",
                weight=0.05,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Security best practices, input validation, no vulnerabilities",
                    ScoreLevel.GOOD: "Good security practices",
                    ScoreLevel.ADEQUATE: "Basic security measures",
                    ScoreLevel.POOR: "Security concerns present",
                    ScoreLevel.FAILING: "Critical security issues",
                }
            ),
        ]

    def generate_architecture_rubric(self) -> List[EvaluationCriterion]:
        """Generate rubric for architecture evaluation"""
        return [
            EvaluationCriterion(
                name="Scalability",
                description="Ability to scale with load",
                weight=0.25,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Scales horizontally, handles 10x growth",
                    ScoreLevel.GOOD: "Scales with minor modifications",
                    ScoreLevel.ADEQUATE: "Handles current load",
                    ScoreLevel.POOR: "Scaling issues likely",
                    ScoreLevel.FAILING: "Cannot scale",
                }
            ),
            EvaluationCriterion(
                name="Maintainability",
                description="Ease of maintaining and modifying the system",
                weight=0.20,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Clear boundaries, easy to modify, well-tested",
                    ScoreLevel.GOOD: "Generally maintainable",
                    ScoreLevel.ADEQUATE: "Can be maintained with effort",
                    ScoreLevel.POOR: "Difficult to maintain",
                    ScoreLevel.FAILING: "Unmaintainable",
                }
            ),
            EvaluationCriterion(
                name="Observability",
                description="Metrics, logging, tracing capabilities",
                weight=0.15,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Comprehensive metrics, logging, tracing",
                    ScoreLevel.GOOD: "Good observability coverage",
                    ScoreLevel.ADEQUATE: "Basic logging/metrics",
                    ScoreLevel.POOR: "Minimal observability",
                    ScoreLevel.FAILING: "No observability",
                }
            ),
            EvaluationCriterion(
                name="Fault Tolerance",
                description="Error recovery and resilience",
                weight=0.15,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Circuit breakers, retries, graceful degradation",
                    ScoreLevel.GOOD: "Good error recovery",
                    ScoreLevel.ADEQUATE: "Basic error handling",
                    ScoreLevel.POOR: "Poor fault tolerance",
                    ScoreLevel.FAILING: "No fault tolerance",
                }
            ),
            EvaluationCriterion(
                name="Security",
                description="Security architecture and practices",
                weight=0.15,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Defense in depth, least privilege, validated inputs",
                    ScoreLevel.GOOD: "Good security practices",
                    ScoreLevel.ADEQUATE: "Basic security",
                    ScoreLevel.POOR: "Security gaps",
                    ScoreLevel.FAILING: "Critical vulnerabilities",
                }
            ),
            EvaluationCriterion(
                name="Documentation",
                description="Architecture documentation quality",
                weight=0.10,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Architecture diagrams, ADRs, runbooks",
                    ScoreLevel.GOOD: "Good documentation",
                    ScoreLevel.ADEQUATE: "Basic documentation",
                    ScoreLevel.POOR: "Minimal documentation",
                    ScoreLevel.FAILING: "No documentation",
                }
            ),
        ]

    def generate_multiagent_rubric(self) -> List[EvaluationCriterion]:
        """Generate rubric for multi-agent system evaluation"""
        return [
            EvaluationCriterion(
                name="Coordination Efficiency",
                description="Efficiency of agent coordination",
                weight=0.25,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Minimal coordination overhead, async patterns",
                    ScoreLevel.GOOD: "Efficient coordination",
                    ScoreLevel.ADEQUATE: "Acceptable coordination",
                    ScoreLevel.POOR: "High coordination overhead",
                    ScoreLevel.FAILING: "Coordination bottleneck",
                }
            ),
            EvaluationCriterion(
                name="Error Cascade Prevention",
                description="Isolation to prevent cascading failures",
                weight=0.20,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Circuit breakers, bulkheads, timeouts everywhere",
                    ScoreLevel.GOOD: "Good isolation",
                    ScoreLevel.ADEQUATE: "Basic isolation",
                    ScoreLevel.POOR: "Error cascade risk",
                    ScoreLevel.FAILING: "No isolation",
                }
            ),
            EvaluationCriterion(
                name="Token Economics",
                description="Efficient token usage across agents",
                weight=0.15,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Optimized token usage, checkpointing, compression",
                    ScoreLevel.GOOD: "Good token management",
                    ScoreLevel.ADEQUATE: "Acceptable token usage",
                    ScoreLevel.POOR: "High token consumption",
                    ScoreLevel.FAILING: "Excessive token waste",
                }
            ),
            EvaluationCriterion(
                name="Observability",
                description="Visibility into agent states and interactions",
                weight=0.15,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Full tracing, agent state visibility, debug tools",
                    ScoreLevel.GOOD: "Good observability",
                    ScoreLevel.ADEQUATE: "Basic logging",
                    ScoreLevel.POOR: "Limited visibility",
                    ScoreLevel.FAILING: "No observability",
                }
            ),
            EvaluationCriterion(
                name="Delegation Clarity",
                description="Clear agent responsibilities and boundaries",
                weight=0.15,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Clear responsibilities, typed interfaces, boundaries",
                    ScoreLevel.GOOD: "Clear delegation",
                    ScoreLevel.ADEQUATE: "Understandable delegation",
                    ScoreLevel.POOR: "Unclear responsibilities",
                    ScoreLevel.FAILING: "Chaotic delegation",
                }
            ),
            EvaluationCriterion(
                name="Checkpoint/Resume",
                description="State persistence and recovery",
                weight=0.10,
                scoring_guide={
                    ScoreLevel.EXCELLENT: "Comprehensive checkpointing, resume from any state",
                    ScoreLevel.GOOD: "Good checkpoint coverage",
                    ScoreLevel.ADEQUATE: "Basic checkpointing",
                    ScoreLevel.POOR: "Limited checkpointing",
                    ScoreLevel.FAILING: "No checkpointing",
                }
            ),
        ]

    def generate_custom_rubric(
        self,
        criteria_specs: List[Dict]
    ) -> List[EvaluationCriterion]:
        """
        Generate custom rubric from specifications.

        Args:
            criteria_specs: List of criterion specifications
                [
                    {
                        "name": "Criterion Name",
                        "description": "What this measures",
                        "weight": 0.3,
                        "levels": {
                            5: "Excellent description",
                            4: "Good description",
                            3: "Adequate description",
                            2: "Poor description",
                            1: "Failing description"
                        }
                    },
                    ...
                ]

        Returns:
            List of EvaluationCriterion objects
        """
        criteria = []

        for spec in criteria_specs:
            scoring_guide = {}
            for score, description in spec["levels"].items():
                scoring_guide[ScoreLevel(score)] = description

            criterion = EvaluationCriterion(
                name=spec["name"],
                description=spec["description"],
                weight=spec["weight"],
                scoring_guide=scoring_guide
            )
            criteria.append(criterion)

        # Validate weights sum to 1.0
        total_weight = sum(c.weight for c in criteria)
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total_weight}")

        return criteria

    def export_rubric_markdown(
        self,
        criteria: List[EvaluationCriterion],
        title: str
    ) -> str:
        """
        Export rubric as markdown table.

        Args:
            criteria: List of evaluation criteria
            title: Rubric title

        Returns:
            Markdown-formatted rubric
        """
        md = f"# {title}\n\n"

        for criterion in criteria:
            md += f"## {criterion.name} (Weight: {criterion.weight * 100:.0f}%)\n\n"
            md += f"{criterion.description}\n\n"
            md += "| Score | Level | Description |\n"
            md += "|-------|-------|-------------|\n"

            for level in sorted(criterion.scoring_guide.keys(), key=lambda x: x.value, reverse=True):
                md += f"| {level.value} | {level.name.title()} | {criterion.scoring_guide[level]} |\n"

            md += "\n"

        return md


def main():
    """Example usage"""
    generator = RubricGenerator()

    print("=== Rubric Generator ===\n")

    # Generate code quality rubric
    print("1. CODE QUALITY RUBRIC")
    print("-" * 60)
    code_rubric = generator.generate_code_quality_rubric()
    md = generator.export_rubric_markdown(code_rubric, "Code Quality Evaluation Rubric")
    print(md)

    # Generate architecture rubric
    print("\n2. ARCHITECTURE RUBRIC")
    print("-" * 60)
    arch_rubric = generator.generate_architecture_rubric()
    md = generator.export_rubric_markdown(arch_rubric, "Architecture Quality Rubric")
    print(md)

    # Generate multi-agent rubric
    print("\n3. MULTI-AGENT SYSTEM RUBRIC")
    print("-" * 60)
    multiagent_rubric = generator.generate_multiagent_rubric()
    md = generator.export_rubric_markdown(multiagent_rubric, "Multi-Agent System Evaluation Rubric")
    print(md)

    # Custom rubric example
    print("\n4. CUSTOM RUBRIC EXAMPLE")
    print("-" * 60)
    custom_spec = [
        {
            "name": "API Design",
            "description": "Quality of API interface design",
            "weight": 0.4,
            "levels": {
                5: "RESTful, consistent, well-documented with examples",
                4: "Good API design with minor inconsistencies",
                3: "Functional API with some design issues",
                2: "Poor API design, difficult to use",
                1: "Broken or unusable API"
            }
        },
        {
            "name": "Response Time",
            "description": "API response time performance",
            "weight": 0.3,
            "levels": {
                5: "< 100ms for all endpoints",
                4: "< 200ms for most endpoints",
                3: "< 500ms acceptable",
                2: "> 500ms for many endpoints",
                1: "> 1000ms unacceptable"
            }
        },
        {
            "name": "Error Messages",
            "description": "Quality of error responses",
            "weight": 0.3,
            "levels": {
                5: "Clear, actionable error messages with codes and docs links",
                4: "Good error messages",
                3: "Basic error messages",
                2: "Generic error messages",
                1: "No error messages or stack traces exposed"
            }
        }
    ]

    custom_rubric = generator.generate_custom_rubric(custom_spec)
    md = generator.export_rubric_markdown(custom_rubric, "API Quality Evaluation Rubric")
    print(md)


if __name__ == "__main__":
    main()
