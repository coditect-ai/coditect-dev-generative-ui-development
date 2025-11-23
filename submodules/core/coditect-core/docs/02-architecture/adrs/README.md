# Architecture Decision Records - CODITECT Core Framework

## Overview

Architecture Decision Records (ADRs) documenting key architectural decisions for the CODITECT Core Framework orchestration system.

**Purpose:** Document significant architectural decisions with context, alternatives considered, and rationale to enable future developers to understand "why" decisions were made, not just "what" was decided.

**Status:** Active (1 ADR documented as of 2025-11-23)

---

## ADR Index

### ADR-001: Async TaskExecutor Refactoring ✅ ACCEPTED

**File:** [ADR-001-async-task-executor-refactoring.md](ADR-001-async-task-executor-refactoring.md)

**Date:** 2025-11-23

**Status:** ✅ ACCEPTED

**Decision:** Make `TaskExecutor.execute()` an async method, converting all 7 execution-related methods to async/await pattern to enable end-to-end async flow and eliminate async/sync boundaries.

**Context:** User explicitly requested async alignment with `ProjectOrchestrator.execute_task()`. Current architecture uses `asyncio.run()` wrapper which creates new event loop per task (~10-20ms overhead) and prevents parallel task execution.

**Impact:**
- ✅ End-to-end async flow (no event loop overhead)
- ✅ Parallel task execution (3x speedup: 2s vs 6s for 3 tasks)
- ✅ Phase 1 Message Bus foundation (autonomous agents)
- ⚠️ Breaking change (all callers use `await`)
- ⚠️ Budget +$750, Timeline +3 days

**Related Documents:**
- [PROJECT-PLAN-EXECUTOR-REFACTORING.md](../../../PROJECT-PLAN-EXECUTOR-REFACTORING.md)
- [ASYNC-EXECUTOR-STRATEGIC-PLAN.md](../../ASYNC-EXECUTOR-STRATEGIC-PLAN.md)
- [docs/03-project-planning/PROJECT-PLAN.md](../../03-project-planning/PROJECT-PLAN.md)

---

## ADR Process

### When to Create an ADR

Create an ADR when making decisions about:

**Architecture & Design:**
- Core framework patterns (async/sync, message passing, state management)
- Technology choices (frameworks, libraries, protocols)
- API design patterns (REST, GraphQL, WebSockets)
- Data models and storage strategies

**Non-Functional Requirements:**
- Performance optimization strategies
- Security architecture
- Scalability approaches
- Deployment patterns

**Integration Points:**
- External service integrations
- Inter-service communication
- Multi-tenant isolation strategies

**Do NOT create ADRs for:**
- Implementation details (code-level decisions)
- Temporary workarounds
- Bug fixes (unless they reveal architectural issues)
- Configuration choices

### ADR Template

```markdown
# ADR-XXX: [Title]

```yaml
Document: ADR-XXX-short-name
Version: 1.0.0
Purpose: [One-line summary]
Audience: [Target readers]
Date Created: YYYY-MM-DD
Status: [PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED]
Related ADRs: [List related ADRs]
Related Documents: [List related docs]
```

## Context and Problem Statement
[Describe the issue being addressed]

## Decision Drivers
### Mandatory Requirements (Must-Have)
### Important Goals (Should-Have)
### Nice-to-Have

## Considered Options
### Option 1: [Name] (SELECTED/REJECTED)
**Pros:** ...
**Cons:** ...

## Decision Outcome
[Chosen option with rationale]

## Consequences
### Positive Consequences
### Negative Consequences
### Risk Mitigation

## Implementation Details
[How to implement the decision]

## Validation and Compliance
[How to verify the decision is followed]

## Links
[Related documents, external references]
```

### ADR Lifecycle

**1. PROPOSED** - Initial draft, under review
**2. ACCEPTED** - Approved and implemented
**3. DEPRECATED** - No longer recommended but not superseded
**4. SUPERSEDED** - Replaced by newer ADR (mark with "Superseded by ADR-XXX")

**Important:** ADRs are **immutable once accepted**. To change a decision, create a new ADR and mark the old one as superseded.

---

## Statistics

- **Total ADRs:** 1
- **Status Breakdown:**
  - ✅ ACCEPTED: 1 (100%)
  - 📋 PROPOSED: 0
  - 🚫 DEPRECATED: 0
  - ⏭️ SUPERSEDED: 0
- **Total Documentation:** ~30K words
- **Last Updated:** 2025-11-23

---

## Cross-References

### Implementation Planning
- [PROJECT-PLAN-EXECUTOR-REFACTORING.md](../../../PROJECT-PLAN-EXECUTOR-REFACTORING.md) - Executor refactoring project plan
- [docs/03-project-planning/PROJECT-PLAN.md](../../03-project-planning/PROJECT-PLAN.md) - Master CODITECT roadmap
- [docs/03-project-planning/TASKLIST-WITH-CHECKBOXES.md](../../03-project-planning/TASKLIST-WITH-CHECKBOXES.md) - Implementation tasks

### Architecture Documentation
- [docs/02-architecture/orchestration/](../orchestration/) - Orchestration architecture
- [docs/MULTI-AGENT-ARCHITECTURE-BEST-PRACTICES.md](../../MULTI-AGENT-ARCHITECTURE-BEST-PRACTICES.md) - Async patterns research
- [ASYNC-EXECUTOR-STRATEGIC-PLAN.md](../../ASYNC-EXECUTOR-STRATEGIC-PLAN.md) - Comprehensive async analysis

### Code Locations
- `orchestration/executor.py` - TaskExecutor implementation
- `orchestration/orchestrator.py` - ProjectOrchestrator implementation
- `llm_abstractions/` - LLM provider implementations

---

## Quality Gates

**Before Creating ADR:**
- [ ] Decision is architectural (not implementation detail)
- [ ] Multiple alternatives have been considered
- [ ] Impact is significant (affects multiple components)
- [ ] Decision needs to be communicated to team

**Before Accepting ADR:**
- [ ] All alternatives documented with pros/cons
- [ ] Consequences (positive and negative) clearly stated
- [ ] Implementation plan provided
- [ ] Validation criteria defined
- [ ] Stakeholders reviewed and approved

**After Accepting ADR:**
- [ ] Update this README index
- [ ] Cross-reference from related documents
- [ ] Mark old ADRs as superseded if applicable
- [ ] Communicate to team

---

**Maintained by:** Architecture Team, AZ1.AI INC.
**Last Updated:** 2025-11-23
**Review Frequency:** When new ADRs added or decisions revisited
