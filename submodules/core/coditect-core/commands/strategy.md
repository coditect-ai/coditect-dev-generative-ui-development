---
name: strategy
description: Architectural planning and system design mode - provides C4 diagrams, multi-agent coordination analysis, and architectural decision records
---

# Strategy Mode

Focus on architectural patterns and system design for: $ARGUMENTS

## Execution Guidelines

### Analysis Framework
- Provide C4 diagrams (Context, Container, Component levels)
- Consider multi-agent coordination patterns
- Analyze token costs (15x multiplier for multi-agent systems)
- Identify failure modes and cascade risks
- Propose 3 alternative approaches with tradeoffs
- Include scalability analysis

### Output Format
- **Architecture Decision Record (ADR) format**
  - Context: Problem statement and constraints
  - Decision: Chosen approach with rationale
  - Consequences: Pros/cons, risks, tradeoffs
- **C4 Diagrams**: Context → Container → Component
- **Migration Path**: From current state to target
- **Risk Analysis**: Failure modes, mitigation strategies

### Integration
- Auto-load: `framework-patterns` skill (C4 diagrams, FSM patterns)
- Auto-load: `multi-agent-workflow` skill (token economics)
- Use: `/complexity_gauge` if needed for token estimation

### Quality Gates
| Aspect | Threshold | Action |
|--------|-----------|--------|
| Alternatives | < 3 | Reject - provide more options |
| C4 Coverage | < 2 levels | Reject - need deeper detail |
| Scalability | Not addressed | Reject - must consider scale |

## Best Practices

✅ **DO**:
- Start with system context (C4 Level 1)
- Consider event-driven patterns first
- Include observability from the start
- Design for failure scenarios
- Provide concrete migration steps

❌ **DON'T**:
- Skip architecture diagrams
- Ignore multi-agent token costs
- Propose single solution without alternatives
- Forget error handling and circuit breakers
- Recommend synchronous coordination patterns
