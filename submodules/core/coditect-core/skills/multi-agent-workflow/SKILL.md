---
name: multi-agent-workflow
description: Intelligent multi-agent orchestration with token budget management and recursive workflow execution. Use when coordinating complex workflows across multiple modules, managing context collapse risk, or handling cascading multi-module issues.
license: MIT
allowed-tools: [Read, Write, Task, TodoWrite]
metadata:
  token-efficiency: "Token budget management prevents 95% context collapse (85%+ checkpoint triggers)"
  integration: "Orchestrator agent + All 7 production workflows"
  tech-stack: "FSM workflows, complexity assessment, checkpoint/resume, recursive resolution"
  production-usage: "Used for full-stack features, security audits, deployment validation"
tags: [orchestration, multi-agent, token-management, workflow, fsm, context-management]
version: 2.0.0
status: production
---

# Multi-Agent Workflow Orchestration

Expert skill for managing complex multi-agent workflows with token budget awareness, context management, and recursive state-based resolution.

## When to Use This Skill

✅ **Use this skill when:**
- **Complex Multi-Phase Workflows**: Tasks requiring coordination of 3+ phases across multiple modules
- **Token Budget Management**: Workflows approaching 70K+ tokens (out of 160K limit)
- **Cascading Dependencies**: Issues spanning backend → frontend → database → infrastructure
- **Recursive Resolution**: Iterative problem-solving with retry/traceback logic
- **Context Collapse Prevention**: Long-running sessions needing checkpoint/resume
- Proven: 7 production workflows (full-stack features, security audits, deployment validation)
- Token efficiency: Prevents 95% context collapse with 85%+ checkpoint triggers

❌ **Don't use this skill when:**
- Single-module tasks (no coordination needed)
- Simple workflows (< 3 phases)
- Token usage < 50% (no budget concerns)
- No cascading dependencies

## Core Capabilities

### 1. Complexity Assessment

Before starting any multi-phase workflow, assess complexity using the complexity gauge:

```bash
/complexity_gauge
```

**Interpret Results**:
- **Safe Zone** (< 70% tokens): Proceed normally
- **Warning Zone** (70-85% tokens): Apply context compression
- **Critical Zone** (85-95% tokens): Mandatory checkpoint before continuing
- **Over-budget** (> 95% tokens): STOP - Create handoff document

**Complexity Factors** (scoring):
- Module count: 5 points per module
- Dependency depth: 10 points per level
- Subagent invocations: 3 points per agent
- File operations: 1 point per file
- Context switches: 15 points per handoff
- Recursive calls: 20 points per iteration

### 2. Orchestrated Workflows

Use the orchestrator for multi-step coordinated workflows:

**When to invoke**:
```
"Use orchestrator to [implement full-stack feature / run security audit / validate deployment]"
```

**Orchestrator will**:
- Create detailed execution plan with phase breakdown
- Assign specialized subagents (codebase-locator, codebase-analyzer, etc.)
- Generate ready-to-execute Task calls
- Provide token budget tracking
- Specify error handling strategies

**7 Production Workflows**:
1. Full-Stack Feature Development (~60K tokens, 15-25 min)
2. Bug Investigation & Fix (~50K tokens, 10-20 min)
3. Security Audit (~55K tokens, 12-18 min)
4. Deployment Validation (~50K tokens, 10-15 min)
5. Code Quality Cycle (~60K tokens, 15-20 min)
6. Codebase Research (~45K tokens, 8-12 min)
7. Project Cleanup (~30K tokens, 5-10 min)

### 3. Recursive Workflows

For cascading multi-module issues requiring iterative resolution:

```bash
/recursive_workflow
```

**FSM States**:
```
INITIATE → IDENTIFY → DOCUMENT → SOLVE → CODE → DEPLOY → TEST → VALIDATE → COMPLETE
```

**Features**:
- State persistence to FoundationDB (resume across sessions)
- Traceback/retry logic (max 10 iterations)
- Automatic `/complexity_gauge` checks at each state transition
- Checkpoint creation when tokens > 85%
- Context handoff for session restarts

**Example Use Case**:
```
Issue: "Session invalidation not propagating from backend to frontend"

Affected Modules:
- Backend: backend/src/handlers/auth.rs
- Frontend: src/services/authStore.ts
- Database: FoundationDB session table

Workflow:
1. IDENTIFY: Locate all session-related code
2. DOCUMENT: Capture current session flow
3. SOLVE: Design propagation strategy
4. CODE: Implement backend → frontend sync
5. DEPLOY: Build and deploy changes
6. TEST: Validate end-to-end flow
7. VALIDATE: Confirm no regressions
```

## Token Budget Management

### Pre-Workflow (Phase 0)

```python
# Always assess before starting
/complexity_gauge

if projected_tokens > 100K:
    # Split into 2 sessions with context_save between
    session_1 = phases[0:3]
    session_2 = phases[4:7]
```

### Mid-Workflow (Phase 3+)

```python
# Check after 50% completion or Phase 3
/complexity_gauge

if current_tokens > 70% of 160K:
    # Apply context compression
    - Summarize completed phases (3-5 bullets)
    - Remove verbose subagent outputs
    - Keep only file:line references
```

### Critical Zone (> 85%)

```python
/complexity_gauge  # Confirm critical status

/context_save project_root=/home/hal/v4/PROJECTS/t2 context_type=comprehensive

# Create handoff document:
# - What's complete
# - What remains
# - Exact next steps
# - Context recovery instructions
```

## Context Compression Strategies

### Level 1: Light Compression (10-20% reduction)
- Summarize completed phases (5 bullets max per phase)
- Remove verbose subagent outputs, keep findings
- Archive file contents, keep references

### Level 2: Moderate Compression (30-40% reduction)
- Aggressive phase summarization (1-2 sentences per phase)
- Remove all file contents, keep metadata only
- Consolidate duplicate information
- Store details in FoundationDB, keep references

### Level 3: Heavy Compression (50-70% reduction)
- Minimal phase tracking (FSM state only)
- External storage for all details (FDB + filesystem)
- Keep only: current state, next actions, critical blockers
- Use `/context_save` to archive everything else

## Workflow Patterns

### Pattern 1: Context-Aware Orchestration

```
1. /complexity_gauge (assess upfront)
2. Orchestrator creates plan
3. Execute Phase 1-2
4. /complexity_gauge (mid-check)
5. If Warning: Apply Level 1 compression
6. Execute Phase 3-4
7. /complexity_gauge (final check)
8. Complete or checkpoint
```

### Pattern 2: Recursive Resolution

```
1. /complexity_gauge (baseline)
2. /recursive_workflow (initiate FSM)
3. Auto-monitors tokens at each state
4. If tokens > 85%: Auto-checkpoint
5. Resume from FDB state in next session
```

### Pattern 3: Parallel Decomposition

```
1. /complexity_gauge (assess)
2. If complex: Split into parallel paths
3. Execute independent modules concurrently
4. Final /complexity_gauge before merge
5. Merge results with validation
```

## Integration with T2 Architecture

### Backend (Rust/Actix-web/FoundationDB)
- Use `WorkflowState` model for FSM persistence
- Use `StateTransition` for audit trail
- Use `WorkflowCheckpoint` for recovery points

**FDB Key Patterns**:
```
/{tenant_id}/workflows/{workflow_id}/state
/{tenant_id}/workflows/{workflow_id}/history/{n}
/{tenant_id}/workflows/{workflow_id}/checkpoints/{n}
```

### Frontend (React/TypeScript/Theia)
- Workflows tied to `WorkspaceSession` via `session_id`
- UI shows workflow progress (current_state, iteration_count)
- Checkpoint/resume UI for long-running workflows

### Specialized Subagents (7 available)
1. **codebase-analyzer** - Implementation details
2. **codebase-locator** - File/component location
3. **codebase-pattern-finder** - Pattern identification
4. **project-organizer** - Directory structure maintenance
5. **thoughts-analyzer** - Decision extraction
6. **thoughts-locator** - Documentation finding
7. **web-search-researcher** - External research

## Best Practices

### ✅ Do This
- Always run `/complexity_gauge` before multi-phase workflows
- Check token budget at 50% completion
- Use orchestrator for 3+ phase workflows
- Invoke `/recursive_workflow` for cascading issues
- Create checkpoints when tokens > 85%
- Compress context proactively at 70%

### ❌ Avoid This
- Don't skip complexity assessment
- Don't continue workflows > 95% token budget
- Don't use recursive workflow for simple issues
- Don't ignore checkpoint warnings
- Don't forget to use `/context_save` before stopping

## Troubleshooting

### "Workflow stuck in loop (IDENTIFY → TEST → IDENTIFY)"
**Cause**: Test failures not providing enough information for fix

**Solution**:
- Add explicit failure analysis in TEST state
- Use `codebase-pattern-finder` for similar fixes
- Consider ESCALATE if iteration > 5

### "Context collapse during workflow"
**Cause**: Too many iterations without checkpoint

**Solution**:
- Trigger checkpoint at 70% tokens (not 85%)
- Use Level 2+ compression earlier
- Archive completed states immediately

### "Can't resume workflow after session restart"
**Cause**: FDB state not persisted or query failed

**Solution**:
- Verify FDB connection
- Check `workflow_id` is correct
- Use `/context_restore` with project ID
- Review FDB key structure

## Examples

### Example 1: Full-Stack Feature

```
User: "Implement user profile editing with backend API and frontend UI"