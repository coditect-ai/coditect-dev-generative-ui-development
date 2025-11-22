---
name: deliberation
description: Pure planning mode - NO code execution, only analysis, task decomposition, and requirement clarification
---

# DELIBERATION MODE

Analyze requirements and decompose tasks for: $ARGUMENTS

## Mode Rules

### ❌ STRICTLY FORBIDDEN
- **NO code execution** - Analysis only
- **NO tool calls** (except Read for context gathering)
- **NO implementation** - Planning phase only
- **NO premature solutions** - Explore problem space first

### ✅ REQUIRED ACTIVITIES
- **Pure analysis** - Understand requirements deeply
- **Task decomposition** - Break into logical phases
- **Gap identification** - Find missing information
- **Dependency mapping** - Understand relationships
- **Question formulation** - Clarify ambiguities

## Deliberation Framework

### Phase 1: Requirement Analysis
```markdown
## Requirements Understanding

### Explicit Requirements
1. [Requirement as stated]
2. [Requirement as stated]

### Implied Requirements
1. [Inferred from context]
2. [Inferred from context]

### Ambiguities / Questions
1. [Unclear aspect] - Need clarification on X
2. [Missing detail] - Should we assume Y or Z?

### Constraints
- Technical: [Framework, language, platform]
- Business: [Timeline, resources]
- Dependencies: [External systems]
```

### Phase 2: Task Decomposition
```markdown
## Task Breakdown

### Phase 1: [Phase Name]
**Duration**: [Estimated time]
**Complexity**: [Low/Medium/High]
**Dependencies**: [What must be done first]

Tasks:
1. [Specific task] - [Why needed]
2. [Specific task] - [Why needed]

### Phase 2: [Phase Name]
[... repeat structure ...]

## Dependency Graph
```
Phase 1 (Foundation)
  ├─> Phase 2 (Core)
  │     └─> Phase 4 (Integration)
  └─> Phase 3 (Auxiliary)
        └─> Phase 4 (Integration)
```
```

### Phase 3: Complexity Assessment
```markdown
## Complexity Analysis

### Token Budget Estimate
- Phase 1: 15K tokens (research + design)
- Phase 2: 25K tokens (implementation)
- Phase 3: 10K tokens (testing)
- **Total**: 50K tokens

### Risk Zones
- **High Risk**: [Aspect with high complexity]
- **Medium Risk**: [Aspect with moderate complexity]
- **Low Risk**: [Well-understood aspects]

### Recommended Strategy
Based on complexity: [Use /complexity_gauge, /recursive_workflow, orchestrator, etc.]
```

### Phase 4: Alternative Approaches
```markdown
## Approaches Considered

### Approach 1: [Name]
**Pros**: [Benefits]
**Cons**: [Drawbacks]
**Complexity**: [Assessment]
**Recommendation**: [Yes/No/Maybe]

### Approach 2: [Name]
[... repeat structure ...]

### Recommended Approach
[Chosen approach with rationale]
```

## Output Structure

```markdown
# Deliberation: [Feature/Task Name]

## Executive Summary
[2-3 sentences: What we're building, why, high-level approach]

## Requirement Analysis
[See Phase 1 above]

## Task Decomposition
[See Phase 2 above]

## Complexity Assessment
[See Phase 3 above]

## Alternative Approaches
[See Phase 4 above]

## Questions for User
1. [Clarifying question 1]
2. [Clarifying question 2]

## Next Steps
**If approved, transition to**: RESEARCH mode (verify assumptions) or ACTION mode (implementation)

**Ready to proceed?**
```

## Integration
- Auto-load: `multi-agent-workflow` skill (token estimation)
- Auto-load: `framework-patterns` skill (architecture options)
- Use: `/complexity_gauge` for token budget analysis

## Transition Protocol

After deliberation complete:

```
**Deliberation complete. Ready to transition:**

Option 1: RESEARCH mode
- Verify technical assumptions
- Check if packages/APIs exist
- Validate approach feasibility
- Estimated: 5-10 tool calls

Option 2: ACTION mode (if confident)
- Skip verification
- Proceed directly to implementation
- Use deliberation plan as blueprint

Which mode should we use next?
```

## Best Practices

✅ **DO**:
- Ask clarifying questions
- Consider multiple approaches
- Identify dependencies explicitly
- Estimate complexity honestly
- Note assumptions clearly

❌ **DON'T**:
- Jump to implementation
- Make unjustified assumptions
- Skip dependency analysis
- Ignore edge cases
- Provide only one approach
