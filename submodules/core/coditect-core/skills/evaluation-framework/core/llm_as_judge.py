#!/usr/bin/env python3
"""
LLM-as-Judge Implementation

Implements LLM-based evaluation with structured rubrics and scoring.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import json
import re


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
    weight: float  # 0.0 - 1.0
    scoring_guide: Dict[ScoreLevel, str]


@dataclass
class EvaluationResult:
    """Result of evaluating one criterion"""
    criterion: str
    score: ScoreLevel
    justification: str
    examples: List[str]
    improvement_suggestions: List[str]


@dataclass
class OverallEvaluation:
    """Complete evaluation result"""
    individual_scores: List[EvaluationResult]
    weighted_average: float
    overall_assessment: str
    strengths: List[str]
    weaknesses: List[str]
    actionable_feedback: List[str]


class LLMAsJudge:
    """LLM-based evaluation system"""

    def generate_evaluation_prompt(
        self,
        output: str,
        criteria: List[EvaluationCriterion],
        context: Optional[str] = None
    ) -> str:
        """
        Generate evaluation prompt for LLM.

        Args:
            output: The text/code to evaluate
            criteria: List of evaluation criteria
            context: Optional context about the task

        Returns:
            Formatted prompt for LLM evaluation
        """
        prompt = "# Evaluation Task\n\n"

        if context:
            prompt += f"## Context\n{context}\n\n"

        prompt += f"""## Output to Evaluate
```
{output}
```

## Evaluation Criteria

"""
        for criterion in criteria:
            prompt += f"\n### {criterion.name} (Weight: {criterion.weight * 100:.0f}%)\n"
            prompt += f"{criterion.description}\n\n"
            prompt += "**Scoring Guide:**\n"
            for level in sorted(criterion.scoring_guide.keys(), key=lambda x: x.value, reverse=True):
                prompt += f"- **{level.name.title()} ({level.value})**: {criterion.scoring_guide[level]}\n"

        prompt += """
## Required Response Format

For EACH criterion above, provide:

```json
{
  "criterion": "<criterion name>",
  "score": <1-5>,
  "justification": "<detailed explanation>",
  "examples": ["<quote 1>", "<quote 2>"],
  "improvement_suggestions": ["<suggestion 1>", "<suggestion 2>"]
}
```

## Final Summary

After all individual criterion evaluations, provide:

```json
{
  "overall_assessment": "<holistic evaluation>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
  "actionable_feedback": ["<action 1>", "<action 2>", "<action 3>"]
}
```

## Important Guidelines
- Be objective and evidence-based
- Quote specific examples from the output
- Provide actionable, specific feedback
- Consider the context and constraints
- Be consistent in your evaluation standards
"""
        return prompt

    def parse_evaluation_response(
        self,
        response: str,
        criteria: List[EvaluationCriterion]
    ) -> OverallEvaluation:
        """
        Parse LLM evaluation response.

        Args:
            response: Raw LLM response
            criteria: List of criteria used for evaluation

        Returns:
            Structured OverallEvaluation
        """
        # Extract JSON blocks from response
        json_pattern = r'```json\s*(\{.*?\})\s*```'
        json_blocks = re.findall(json_pattern, response, re.DOTALL)

        if len(json_blocks) < len(criteria) + 1:
            raise ValueError(f"Expected {len(criteria) + 1} JSON blocks, got {len(json_blocks)}")

        # Parse individual criterion results
        individual_scores = []
        for i, json_str in enumerate(json_blocks[:len(criteria)]):
            data = json.loads(json_str)
            result = EvaluationResult(
                criterion=data["criterion"],
                score=ScoreLevel(data["score"]),
                justification=data["justification"],
                examples=data.get("examples", []),
                improvement_suggestions=data.get("improvement_suggestions", [])
            )
            individual_scores.append(result)

        # Parse summary
        summary = json.loads(json_blocks[-1])

        # Calculate weighted average
        weighted_sum = sum(
            result.score.value * criteria[i].weight
            for i, result in enumerate(individual_scores)
        )
        total_weight = sum(c.weight for c in criteria)
        weighted_average = weighted_sum / total_weight if total_weight > 0 else 0

        return OverallEvaluation(
            individual_scores=individual_scores,
            weighted_average=weighted_average,
            overall_assessment=summary["overall_assessment"],
            strengths=summary["strengths"],
            weaknesses=summary["weaknesses"],
            actionable_feedback=summary["actionable_feedback"]
        )

    def generate_report(self, evaluation: OverallEvaluation) -> str:
        """
        Generate human-readable evaluation report.

        Args:
            evaluation: OverallEvaluation object

        Returns:
            Markdown-formatted report
        """
        report = f"""# Evaluation Report

**Overall Score**: {evaluation.weighted_average:.2f}/5.0

## Summary

{evaluation.overall_assessment}

## Strengths

{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(evaluation.strengths))}

## Weaknesses

{chr(10).join(f"{i+1}. {w}" for i, w in enumerate(evaluation.weaknesses))}

## Actionable Feedback

{chr(10).join(f"{i+1}. {a}" for i, a in enumerate(evaluation.actionable_feedback))}

## Detailed Criterion Scores

"""
        for result in evaluation.individual_scores:
            report += f"""
### {result.criterion}

**Score**: {result.score.value}/5 ({result.score.name})

**Justification**:
{result.justification}

**Evidence**:
{chr(10).join(f"- `{ex}`" for ex in result.examples)}

**Improvement Suggestions**:
{chr(10).join(f"- {imp}" for imp in result.improvement_suggestions)}

---
"""
        return report

    def calculate_score_distribution(
        self,
        evaluations: List[OverallEvaluation]
    ) -> Dict[ScoreLevel, int]:
        """
        Calculate distribution of scores across multiple evaluations.

        Args:
            evaluations: List of evaluations

        Returns:
            Count of each score level
        """
        distribution = {level: 0 for level in ScoreLevel}

        for eval in evaluations:
            for result in eval.individual_scores:
                distribution[result.score] += 1

        return distribution


def main():
    """Example usage"""
    judge = LLMAsJudge()

    # Define criteria
    criteria = [
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
                ScoreLevel.EXCELLENT: "Comprehensive error handling with recovery",
                ScoreLevel.GOOD: "Good error handling, clear messages",
                ScoreLevel.ADEQUATE: "Basic error handling present",
                ScoreLevel.POOR: "Minimal error handling",
                ScoreLevel.FAILING: "No error handling",
            }
        ),
    ]

    # Example output to evaluate
    code_output = """
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def process_data(data):
    results = []
    for item in data:
        try:
            result = divide(item['numerator'], item['denominator'])
            results.append(result)
        except (ValueError, KeyError) as e:
            print(f"Error processing item: {e}")
            results.append(None)
    return results
"""

    # Generate evaluation prompt
    prompt = judge.generate_evaluation_prompt(
        output=code_output,
        criteria=criteria,
        context="Evaluating a Python function for data processing with error handling"
    )

    print("=== LLM-as-Judge Evaluation Prompt ===\n")
    print(prompt)
    print("\n" + "="*60 + "\n")

    # Example: Parse a mock response (in real usage, this comes from LLM)
    mock_response = """
```json
{
  "criterion": "Correctness",
  "score": 4,
  "justification": "The code correctly handles the main case of division and the zero division edge case. However, it doesn't validate input types.",
  "examples": ["if b == 0: raise ValueError", "except (ValueError, KeyError)"],
  "improvement_suggestions": ["Add type validation for inputs", "Consider handling float('inf') case"]
}
```

```json
{
  "criterion": "Code Structure",
  "score": 4,
  "justification": "Code is well-organized with clear separation between division logic and data processing. Good use of try-except blocks.",
  "examples": ["def divide(a, b):", "for item in data:"],
  "improvement_suggestions": ["Consider extracting error logging to separate function"]
}
```

```json
{
  "criterion": "Error Handling",
  "score": 4,
  "justification": "Good error handling with specific exceptions caught. Returns None for failed items rather than crashing.",
  "examples": ["except (ValueError, KeyError) as e:", "results.append(None)"],
  "improvement_suggestions": ["Log errors to a logger instead of print", "Consider collecting errors for reporting"]
}
```

```json
{
  "overall_assessment": "This is a well-written function with good error handling practices. It correctly handles the main use case and includes error recovery. Minor improvements could make it more robust and production-ready.",
  "strengths": ["Explicit zero division check", "Graceful error recovery with None values", "Catches specific exceptions"],
  "weaknesses": ["Uses print for error logging", "No input type validation", "No detailed error reporting"],
  "actionable_feedback": ["Replace print with proper logging", "Add type hints and validation", "Return errors alongside results for better debugging"]
}
```
"""

    evaluation = judge.parse_evaluation_response(mock_response, criteria)
    report = judge.generate_report(evaluation)

    print("=== Evaluation Report ===\n")
    print(report)


if __name__ == "__main__":
    main()
