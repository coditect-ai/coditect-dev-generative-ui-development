---
name: evaluation-framework
description: LLM-as-judge evaluation patterns, rubric generation, and quality assessment frameworks. Use when evaluating code quality, assessing outputs, creating evaluation criteria, or implementing review systems.
license: MIT
allowed-tools: [Read, Write]
metadata:
  token-efficiency: "Structured rubrics enable consistent 5-min evaluations vs 20-min manual reviews"
  integration: "Orchestrator Code Quality Cycle + Quality Gate agent"
  tech-stack: "LLM-as-judge patterns, Python dataclasses, scoring rubrics"
  production-usage: "Used for code review, skill evaluation, output assessment"
tags: [evaluation, llm-as-judge, quality-assessment, rubrics, code-review]
version: 2.0.0
status: production
---

# Evaluation Framework

Expert skill for creating evaluation rubrics, implementing LLM-as-judge patterns, and assessing quality.

## When to Use

✅ **Use this skill when:**
- Creating evaluation rubrics for code/outputs (consistent scoring)
- Implementing LLM-as-judge patterns (automated review)
- Quality assessment frameworks (standardized criteria)
- Automated code review systems (scalable evaluation)
- Output validation and scoring (objective assessment)
- Creating grading criteria (5-level scoring guides)
- Time savings: 75% faster reviews (20→5 min per evaluation)

❌ **Don't use this skill when:**
- Simple pass/fail checks (use basic validation instead)
- Subjective aesthetic judgments (rubrics work best for objective criteria)
- Real-time interactive reviews (LLM-as-judge is async)
- Single evaluation (not worth rubric setup overhead)

## LLM-as-Judge Pattern

### Core Concept

Use an LLM to evaluate outputs based on defined criteria, providing:
- Structured scoring
- Consistent evaluation
- Detailed feedback
- Comparative analysis

### Evaluation Template

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class ScoreLevel(Enum):
    """Standardized score levels"""
    EXCELLENT = 5  # Exceeds all criteria
    GOOD = 4       # Meets all criteria well
    ADEQUATE = 3   # Meets minimum criteria
    POOR = 2       # Below minimum criteria
    FAILING = 1    # Does not meet criteria

@dataclass
class EvaluationCriterion:
    """Single evaluation criterion"""
    name: str
    description: str
    weight: float  # 0.0 - 1.0
    scoring_guide: Dict[ScoreLevel, str]

@dataclass
class EvaluationResult:
    """Result of evaluation"""
    criterion: str
    score: ScoreLevel
    justification: str
    examples: List[str]
    improvement_suggestions: List[str]

@dataclass
class OverallEvaluation:
    """Complete evaluation"""
    individual_scores: List[EvaluationResult]
    weighted_average: float
    overall_assessment: str
    strengths: List[str]
    weaknesses: List[str]
    actionable_feedback: List[str]
```

### LLM-as-Judge Prompt Template

```markdown
# Evaluation Task

Evaluate the following OUTPUT against the specified CRITERIA.

## Output to Evaluate
```
{output_text}
```

## Evaluation Criteria

{criterion_1_name} (Weight: {weight}%)
- Excellent (5): {excellent_description}
- Good (4): {good_description}
- Adequate (3): {adequate_description}
- Poor (2): {poor_description}
- Failing (1): {failing_description}

{criterion_2_name} (Weight: {weight}%)
[...repeat for all criteria...]

## Required Response Format

For EACH criterion, provide:

1. **Score**: {1-5}
2. **Justification**: {detailed explanation referencing specific parts of output}
3. **Evidence**: {quote specific examples from output}
4. **Improvement Suggestions**: {actionable recommendations}

## Final Summary

- **Weighted Average Score**: {calculated from individual scores}
- **Overall Assessment**: {holistic evaluation}
- **Top 3 Strengths**: {bullet list}
- **Top 3 Weaknesses**: {bullet list}
- **Priority Improvements**: {ranked list of most impactful changes}

## Important
- Be objective and evidence-based
- Quote specific examples
- Provide actionable feedback
- Consider context and constraints
- Be consistent across evaluations
```

## Code Quality Rubric

### Criteria

**1. Correctness (Weight: 30%)**
- Excellent (5): Handles all cases including edge cases, no bugs
- Good (4): Handles main cases correctly, minor edge case issues
- Adequate (3): Core functionality works, some edge case bugs
- Poor (2): Core functionality has bugs
- Failing (1): Does not work as intended

**2. Code Structure (Weight: 20%)**
- Excellent (5): Well-organized, clear separation of concerns, DRY
- Good (4): Organized, minor repetition
- Adequate (3): Functional organization, some repetition
- Poor (2): Poor organization, significant repetition
- Failing (1): Unstructured, unmaintainable

**3. Error Handling (Weight: 15%)**
- Excellent (5): Comprehensive error handling with recovery, detailed messages
- Good (4): Good error handling, clear messages
- Adequate (3): Basic error handling present
- Poor (2): Minimal error handling
- Failing (1): No error handling

**4. Documentation (Weight: 10%)**
- Excellent (5): Comprehensive docs, examples, edge cases documented
- Good (4): Good documentation coverage
- Adequate (3): Basic documentation present
- Poor (2): Minimal documentation
- Failing (1): No documentation

**5. Type Safety (Weight: 10%)**
- Excellent (5): Full type hints, passes strict type checking
- Good (4): Good type coverage (>80%)
- Adequate (3): Basic type hints (>50%)
- Poor (2): Minimal type hints (<50%)
- Failing (1): No type hints

**6. Performance (Weight: 10%)**
- Excellent (5): Optimal algorithms, efficient implementation
- Good (4): Good performance, room for minor optimization
- Adequate (3): Acceptable performance
- Poor (2): Performance issues
- Failing (1): Unacceptable performance

**7. Security (Weight: 5%)**
- Excellent (5): Security best practices, input validation, no vulnerabilities
- Good (4): Good security practices
- Adequate (3): Basic security measures
- Poor (2): Security concerns present
- Failing (1): Critical security issues

## Architecture Quality Rubric

**1. Scalability (Weight: 25%)**
- Excellent (5): Scales horizontally, handles 10x growth
- Good (4): Scales with minor modifications
- Adequate (3): Handles current load
- Poor (2): Scaling issues likely
- Failing (1): Cannot scale

**2. Maintainability (Weight: 20%)**
- Excellent (5): Clear boundaries, easy to modify, well-tested
- Good (4): Generally maintainable
- Adequate (3): Can be maintained with effort
- Poor (2): Difficult to maintain
- Failing (1): Unmaintainable

**3. Observability (Weight: 15%)**
- Excellent (5): Comprehensive metrics, logging, tracing
- Good (4): Good observability coverage
- Adequate (3): Basic logging/metrics
- Poor (2): Minimal observability
- Failing (1): No observability

**4. Fault Tolerance (Weight: 15%)**
- Excellent (5): Circuit breakers, retries, graceful degradation
- Good (4): Good error recovery
- Adequate (3): Basic error handling
- Poor (2): Poor fault tolerance
- Failing (1): No fault tolerance

**5. Security (Weight: 15%)**
- Excellent (5): Defense in depth, least privilege, validated inputs
- Good (4): Good security practices
- Adequate (3): Basic security
- Poor (2): Security gaps
- Failing (1): Critical vulnerabilities

**6. Documentation (Weight: 10%)**
- Excellent (5): Architecture diagrams, ADRs, runbooks
- Good (4): Good documentation
- Adequate (3): Basic documentation
- Poor (2): Minimal documentation
- Failing (1): No documentation

## Multi-Agent System Rubric

**1. Coordination Efficiency (Weight: 25%)**
- Excellent (5): Minimal coordination overhead, async patterns
- Good (4): Efficient coordination
- Adequate (3): Acceptable coordination
- Poor (2): High coordination overhead
- Failing (1): Coordination bottleneck

**2. Error Cascade Prevention (Weight: 20%)**
- Excellent (5): Circuit breakers, bulkheads, timeouts everywhere
- Good (4): Good isolation
- Adequate (3): Basic isolation
- Poor (2): Error cascade risk
- Failing (1): No isolation

**3. Token Economics (Weight: 15%)**
- Excellent (5): Optimized token usage, checkpointing, compression
- Good (4): Good token management
- Adequate (3): Acceptable token usage
- Poor (2): High token consumption
- Failing (1): Excessive token waste

**4. Observability (Weight: 15%)**
- Excellent (5): Full tracing, agent state visibility, debug tools
- Good (4): Good observability
- Adequate (3): Basic logging
- Poor (2): Limited visibility
- Failing (1): No observability

**5. Delegation Clarity (Weight: 15%)**
- Excellent (5): Clear responsibilities, typed interfaces, boundaries
- Good (4): Clear delegation
- Adequate (3): Understandable delegation
- Poor (2): Unclear responsibilities
- Failing (1): Chaotic delegation

**6. Checkpoint/Resume (Weight: 10%)**
- Excellent (5): Comprehensive checkpointing, resume from any state
- Good (4): Good checkpoint coverage
- Adequate (3): Basic checkpointing
- Poor (2): Limited checkpointing
- Failing (1): No checkpointing

## Evaluation Process

### Step 1: Define Criteria

```python
code_quality_criteria = [
    EvaluationCriterion(
        name="Correctness",
        description="Code works as intended, handles edge cases",
        weight=0.30,
        scoring_guide={
            ScoreLevel.EXCELLENT: "Handles all cases including edge cases, no bugs",
            ScoreLevel.GOOD: "Handles main cases correctly, minor edge case issues",
            ScoreLevel.ADEQUATE: "Core functionality works, some edge case bugs",
            ScoreLevel.POOR: "Core functionality has bugs",
            ScoreLevel.FAILING: "Does not work as intended",
        }
    ),
    # ... more criteria
]
```

### Step 2: Generate Evaluation Prompt

```python
def generate_evaluation_prompt(
    output: str,
    criteria: List[EvaluationCriterion]
) -> str:
    """Generate LLM-as-judge prompt"""
    prompt = f"""# Evaluation Task

Evaluate the following OUTPUT against the specified CRITERIA.

## Output to Evaluate
```
{output}
```

## Evaluation Criteria

"""
    for criterion in criteria:
        prompt += f"\n{criterion.name} (Weight: {criterion.weight * 100}%)\n"
        for level, description in criterion.scoring_guide.items():
            prompt += f"- {level.name.title()} ({level.value}): {description}\n"

    prompt += """
## Required Response Format

[Format instructions...]
"""
    return prompt
```

### Step 3: Parse Evaluation Response

```python
def parse_evaluation_response(
    response: str,
    criteria: List[EvaluationCriterion]
) -> OverallEvaluation:
    """Parse LLM evaluation response"""
    # Extract individual scores
    # Calculate weighted average
    # Generate overall assessment
    pass
```

### Step 4: Generate Report

```python
def generate_evaluation_report(eval: OverallEvaluation) -> str:
    """Generate human-readable report"""
    report = f"""
# Evaluation Report

**Overall Score**: {eval.weighted_average:.2f}/5.0

## Strengths
{chr(10).join(f"- {s}" for s in eval.strengths)}

## Weaknesses
{chr(10).join(f"- {w}" for w in eval.weaknesses)}

## Detailed Scores

"""
    for result in eval.individual_scores:
        report += f"""
### {result.criterion}
**Score**: {result.score.value}/5 ({result.score.name})

**Justification**: {result.justification}

**Examples**:
{chr(10).join(f"- {ex}" for ex in result.examples)}

**Improvements**:
{chr(10).join(f"- {imp}" for imp in result.improvement_suggestions)}
"""
    return report
```

## Comparative Evaluation

For comparing multiple implementations:

```python
@dataclass
class ComparativeEvaluation:
    """Compare multiple outputs"""
    outputs: List[str]
    criteria: List[EvaluationCriterion]
    individual_evaluations: List[OverallEvaluation]
    rankings: Dict[str, int]  # output_id -> rank
    best_practices: List[str]
    common_issues: List[str]
```

## Executable Scripts

See `core/llm_as_judge.py` for LLM-as-judge implementation.
See `core/rubric_generator.py` for rubric generation utilities.

## Best Practices

### ✅ DO

- **Define clear criteria** - Specific, measurable, actionable
- **Use weighted scoring** - Reflect importance of criteria
- **Provide scoring guides** - Clear descriptions for each level
- **Require evidence** - Quote specific examples
- **Give actionable feedback** - Specific improvement suggestions
- **Be consistent** - Apply same standards across evaluations

### ❌ DON'T

- **Don't use vague criteria** - "Good code" is not measurable
- **Don't skip justifications** - Always explain scores
- **Don't ignore context** - Consider constraints and requirements
- **Don't be subjective** - Base on evidence, not preference
- **Don't provide only scores** - Include improvement guidance

## Integration with T2

**Use cases in T2**:
- Code review automation (evaluate PRs)
- Agent output validation (ensure quality)
- Architecture assessment (evaluate designs)
- Documentation quality checks

**Example integration**:
```rust
// Evaluate agent output before accepting
let evaluation = evaluate_agent_output(
    agent_output,
    &evaluation_criteria,
    llm_service
).await?;

if evaluation.weighted_average < 3.0 {
    // Reject and request improvements
    return Err(AgentError::OutputQualityTooLow {
        score: evaluation.weighted_average,
        issues: evaluation.weaknesses,
    });
}
```

## Templates

See `templates/evaluation_rubrics.md` for pre-built rubrics.
