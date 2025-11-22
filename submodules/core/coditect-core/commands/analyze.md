---
name: analyze
description: Code review and analysis mode - evaluates code quality, security, performance, and provides actionable feedback
---

# Analysis Mode

Analyze code for: $ARGUMENTS

## Analysis Framework

### Evaluation Criteria
Use the evaluation-framework skill with comprehensive rubrics:

**Code Quality** (if analyzing implementation):
- Correctness (30%)
- Code Structure (20%)
- Error Handling (15%)
- Documentation (10%)
- Type Safety (10%)
- Performance (10%)
- Security (5%)

**Architecture** (if analyzing design):
- Scalability (25%)
- Maintainability (20%)
- Observability (15%)
- Fault Tolerance (15%)
- Security (15%)
- Documentation (10%)

**Multi-Agent Systems** (if analyzing agents):
- Coordination Efficiency (25%)
- Error Cascade Prevention (20%)
- Token Economics (15%)
- Observability (15%)
- Delegation Clarity (15%)
- Checkpoint/Resume (10%)

### Output Format
```markdown
# Analysis Report

**Overall Score**: X.X/5.0

## Summary
[Brief assessment of strengths and weaknesses]

## Detailed Scores

### Criterion 1
**Score**: X/5 (Level)
**Justification**: [Evidence-based explanation]
**Examples**: [Quote specific code]
**Improvements**: [Actionable suggestions]

[... repeat for all criteria ...]

## Priority Improvements
1. [Most impactful change]
2. [Second priority]
3. [Third priority]

## Security Issues
[If any CRITICAL/HIGH security concerns found]
```

### Integration
- Auto-load: `evaluation-framework` skill (LLM-as-judge, rubrics)
- Auto-load: `production-patterns` skill (identify missing patterns)
- Auto-load: `framework-patterns` skill (architecture analysis)

### Quality Gates
| Aspect | Threshold | Action |
|--------|-----------|--------|
| Missing criteria | Any | Reject - analyze all aspects |
| No examples | Any criterion | Reject - quote specific code |
| Vague feedback | Any | Reject - be specific and actionable |

## Best Practices

✅ **DO**:
- Quote specific code examples
- Provide actionable, specific feedback
- Rank issues by priority/severity
- Consider context and constraints
- Include positive feedback (strengths)
- Reference production patterns

❌ **DON'T**:
- Be vague ("could be better")
- Only provide scores without justification
- Skip security analysis
- Ignore performance implications
- Forget to suggest concrete improvements
