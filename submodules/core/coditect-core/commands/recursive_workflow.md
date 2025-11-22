# Recursive Workflow Manager: FSM-Based Multi-Phase Resolution

## Role and Purpose

An elite workflow orchestration specialist focused on managing complex, iterative, multi-module problem resolution using Finite State Machine (FSM) patterns. This command enables robust, stateful, recursive workflows that can recover from failures, maintain context across iterations, and resolve cascading dependencies across multiple modules.

## Overview

The Recursive Workflow Manager is designed to:
- Execute multi-step resolution workflows using FSM state machines
- Handle cascading dependencies across modules (frontend, backend, database, infrastructure)
- Persist workflow state to FoundationDB for recovery and resumption
- Manage context handoff between phases and iterations
- Support traceback and retry logic on failures
- Enable recursive problem-solving with intelligent iteration limits
- Coordinate with complexity gauge for token budget management

## When to Use This Command

**✅ Use `/recursive_workflow` when:**
- Issues span multiple modules with cascading dependencies
- Solution requires iterative refinement (identify → fix → test → retry)
- Failures in one module trigger fixes in others
- Need to maintain state across context collapses
- Recursive debugging or resolution required
- Long-running multi-phase fixes

**❌ Don't use for:**
- Simple single-module fixes
- One-shot implementations
- Non-iterative tasks
- Issues with clear, direct solutions

## Workflow States (FSM)

The recursive workflow operates as a finite state machine with these states:

```
┌─────────────┐
│  INITIATE   │  Entry point
└──────┬──────┘
       │
       v
┌─────────────┐
│   IDENTIFY  │  Analyze issue, map dependencies
└──────┬──────┘
       │
       v
┌─────────────┐
│  DOCUMENT   │  Capture current state, context
└──────┬──────┘
       │
       v
┌─────────────┐
│   SOLVE     │  Design solution strategy
└──────┬──────┘
       │
       v
┌─────────────┐
│    CODE     │  Implement fix
└──────┬──────┘
       │
       v
┌─────────────┐
│   DEPLOY    │  Apply changes
└──────┬──────┘
       │
       v
┌─────────────┐
│    TEST     │  Validate fix
└──────┬──────┘
       │
       ├─ PASS ──────────────┐
       │                      v
       │              ┌─────────────┐
       │              │  VALIDATE   │  Confirm complete resolution
       │              └──────┬──────┘
       │                     │
       │                     v
       │              ┌─────────────┐
       │              │  COMPLETE   │  Terminal state (success)
       │              └─────────────┘
       │
       └─ FAIL ───> [TRACEBACK]
                          │
                          v
                    Determine cause:
                    - Incomplete fix? → SOLVE
                    - New issue found? → IDENTIFY
                    - Implementation error? → CODE
                    - Deployment problem? → DEPLOY
```

## State Definitions

### 1. INITIATE
**Purpose**: Initialize workflow, load context, establish baseline

**Actions**:
- Read issue description
- Identify affected modules
- Establish session ID for state persistence
- Create workflow record in FoundationDB
- Set iteration counter = 0
- Run `/complexity_gauge` to baseline token usage

**Outputs**:
- Workflow ID (UUID)
- Session ID
- Module list
- Initial complexity score

**Transition**: Always → IDENTIFY

---

### 2. IDENTIFY
**Purpose**: Analyze issue, map dependencies, locate affected code

**Actions**:
- Use `codebase-locator` to find relevant files
- Use `codebase-analyzer` to understand current implementation
- Build dependency graph (which modules impact which)
- Identify cascading effects
- Estimate complexity score
- Document known unknowns

**Outputs**:
- File list with locations
- Dependency graph (Module A → B → C)
- Affected components
- Root cause hypothesis

**Transitions**:
- Normal → DOCUMENT
- Context overflow → CHECKPOINT (save state, restart session)
- Cannot identify root cause → ESCALATE (human intervention)

---

### 3. DOCUMENT
**Purpose**: Capture complete current state before making changes

**Actions**:
- Save workflow state to FoundationDB:
  ```sql
  workflow_states(
    workflow_id,
    session_id,
    current_state,
    context_snapshot,
    dependency_graph,
    iteration_count,
    token_usage,
    created_at
  )
  ```
- Create context snapshot (current state of affected modules)
- Document assumptions and constraints
- Log all findings from IDENTIFY phase
- Run `/complexity_gauge` to track token budget

**Outputs**:
- State checkpoint in FDB
- Context snapshot file
- Assumptions list

**Transitions**:
- Normal → SOLVE
- Token budget critical → COMPRESS_CONTEXT (use `/context_save`)

---

### 4. SOLVE
**Purpose**: Design solution strategy

**Actions**:
- Analyze root cause from IDENTIFY findings
- Design fix strategy
- Identify which modules need changes
- Determine change order (dependencies first)
- Estimate risk and complexity
- Create mini-plan for implementation

**Outputs**:
- Solution design document
- Change order list (Module A, then B, then C)
- Risk assessment
- Success criteria

**Transitions**:
- Normal → CODE
- Solution unclear → IDENTIFY (gather more info)
- Multiple solutions → HUMAN_DECISION (ask user to choose)

---

### 5. CODE
**Purpose**: Implement the fix

**Actions**:
- Make code changes in dependency order
- Use `Read` to load files
- Use `Edit` to modify code
- Follow architectural patterns from codebase
- Add comments explaining changes
- Preserve existing tests (don't break them)

**Outputs**:
- Modified files list
- Change summary
- Files changed count

**Transitions**:
- Normal → DEPLOY
- Compilation errors → SOLVE (revise strategy)
- Context overflow → CHECKPOINT

---

### 6. DEPLOY
**Purpose**: Apply changes to the environment

**Actions**:
- Compile/build changes
- Run type checks
- Deploy to appropriate environment
  - Backend: `cargo build` (Rust)
  - Frontend: `npm run build` (TypeScript/React)
  - Database: migrations if needed
- Verify deployment success

**Outputs**:
- Build/compile results
- Deployment status
- Error logs (if any)

**Transitions**:
- Build success → TEST
- Build failure → CODE (fix implementation)
- Deployment failure → SOLVE (wrong approach)

---

### 7. TEST
**Purpose**: Validate the fix works

**Actions**:
- Run automated tests:
  - Backend: `cargo test`
  - Frontend: `npm run test`
  - Integration: `./scripts/test-runner.sh`
- Manual validation of success criteria
- Check for regressions
- Verify cascading modules work

**Outputs**:
- Test results
- Pass/fail status
- Regression report

**Transitions**:
- All tests pass → VALIDATE
- Tests fail, expected → CODE (fix implementation)
- Tests fail, unexpected → IDENTIFY (new issue found)
- Tests pass, but manual validation fails → SOLVE (missed requirement)

---

### 8. VALIDATE
**Purpose**: Confirm complete resolution, check cascading effects

**Actions**:
- Verify original issue resolved
- Check all affected modules
- Confirm no new issues introduced
- Review success criteria from SOLVE phase
- Run final `/complexity_gauge` for metrics

**Outputs**:
- Validation report
- Module health check results
- Final state snapshot

**Transitions**:
- Fully resolved → COMPLETE
- Partially resolved → IDENTIFY (address remaining issues)
- New issues discovered → IDENTIFY (start new iteration)

---

### 9. COMPLETE
**Purpose**: Terminal success state

**Actions**:
- Save final state to FoundationDB
- Generate completion report
- Archive workflow context with `/context_save`
- Update metrics (total iterations, token usage, time)
- Clean up temporary state

**Outputs**:
- Completion report
- Metrics summary
- Archived context reference

**Transition**: None (terminal state)

---

### Special States

#### CHECKPOINT
**Purpose**: Save state and prepare for context collapse

**Actions**:
- Run `/complexity_gauge` to confirm critical status
- Execute `/context_save` with comprehensive mode
- Save FSM state to FoundationDB:
  ```json
  {
    "workflow_id": "uuid",
    "current_state": "CODE",
    "iteration": 2,
    "context_ref": "fdb://contexts/uuid",
    "resume_instructions": "Continue from CODE state, files X Y Z modified",
    "next_action": "Complete edit of backend/src/handlers/auth.rs:167"
  }
  ```
- Create handoff document for next session
- Mark workflow as SUSPENDED

**Resume Process**:
1. New session starts
2. Read workflow state from FDB
3. Execute `/context_restore` with context_ref
4. Resume from saved state
5. Continue FSM from current_state

#### TRACEBACK
**Purpose**: Handle failures by returning to appropriate earlier state

**Traceback Logic**:
```python
def traceback(failure_type, current_state):
    if failure_type == "implementation_error":
        return "CODE"  # Fix the code
    elif failure_type == "wrong_approach":
        return "SOLVE"  # Redesign solution
    elif failure_type == "misidentified_issue":
        return "IDENTIFY"  # Re-analyze problem
    elif failure_type == "missing_context":
        return "DOCUMENT"  # Capture more state
    else:
        return "ESCALATE"  # Human help needed
```

**Actions**:
- Analyze failure reason
- Determine appropriate state to return to
- Preserve failure context (don't lose information)
- Increment iteration counter
- Check iteration limit (max 10)

**Transitions**:
- iteration_count < 10 → [Determined state]
- iteration_count >= 10 → ESCALATE (too many retries)

#### ESCALATE
**Purpose**: Request human intervention

**Actions**:
- Generate escalation report:
  - What we tried
  - What failed
  - Why we're stuck
  - What information is missing
- Persist all context
- Pause workflow (SUSPENDED state)

**Output**: Escalation report for human review

## State Persistence Schema (FoundationDB)

### Workflow State Record

```typescript
interface WorkflowState {
  // Identity
  workflow_id: string;        // UUID
  session_id: string;         // Current session
  tenant_id: string;          // Multi-tenant isolation

  // FSM State
  current_state: FSMState;    // One of: INITIATE, IDENTIFY, DOCUMENT, etc.
  previous_state: FSMState | null;
  iteration_count: number;

  // Context
  issue_description: string;
  affected_modules: string[]; // ["backend", "frontend", "database"]
  dependency_graph: DependencyGraph;
  context_snapshot_ref: string;  // Reference to saved context

  // Metrics
  token_usage: number;
  complexity_score: number;
  start_time: timestamp;
  last_updated: timestamp;

  // State-specific data
  state_data: {
    // IDENTIFY
    files_located?: string[];
    root_cause_hypothesis?: string;

    // SOLVE
    solution_design?: string;
    change_order?: string[];

    // CODE
    modified_files?: string[];

    // TEST
    test_results?: TestResult[];

    // VALIDATE
    validation_report?: string;
  };

  // Failure tracking
  failures: {
    state: string;
    reason: string;
    timestamp: timestamp;
  }[];

  // Resume data (for CHECKPOINT)
  resume_instructions?: string;
  next_action?: string;
}

type FSMState =
  | "INITIATE"
  | "IDENTIFY"
  | "DOCUMENT"
  | "SOLVE"
  | "CODE"
  | "DEPLOY"
  | "TEST"
  | "VALIDATE"
  | "COMPLETE"
  | "CHECKPOINT"
  | "SUSPENDED"
  | "ESCALATED";

interface DependencyGraph {
  nodes: string[];  // Module names
  edges: {
    from: string;
    to: string;
    impact: "high" | "medium" | "low";
  }[];
}
```

### FoundationDB Key Structure

```
/workflows/{tenant_id}/{workflow_id}/state          → WorkflowState
/workflows/{tenant_id}/{workflow_id}/context        → ContextSnapshot
/workflows/{tenant_id}/{workflow_id}/history/{n}    → StateTransition
/workflows/{tenant_id}/{workflow_id}/checkpoints/{n} → Checkpoint
```

## Context Handoff Strategy

### Between States (Same Session)

**Minimal handoff** - FSM manages state transitions:
- Current state stored in memory
- Key data passed via state_data object
- No serialization needed

### Between Iterations (Traceback)

**Moderate handoff** - Preserve failure context:
- Save failure reason
- Preserve all findings from current iteration
- Carry forward to next iteration
- Add to failures array

### Between Sessions (Checkpoint/Resume)

**Full handoff** - Complete state serialization:

**Save process**:
1. Run `/complexity_gauge` to confirm need
2. Execute `/context_save project_root=$PROJECT_ROOT context_type=comprehensive`
3. Save FSM state to FDB
4. Create resume instructions
5. Generate handoff document

**Resume process**:
1. Query FDB for workflow state
2. Execute `/context_restore` with context reference
3. Load FSM state
4. Display resume instructions to user
5. Continue from saved state

### Context Compression During Long Workflows

**After each state transition**:
- Archive completed state data
- Keep only essential context for current state
- Use references instead of full data
- Example:
  ```
  IDENTIFY → DOCUMENT:
    Archive: Full file contents from codebase-analyzer
    Keep: File paths, key findings (3-5 bullets)
  ```

## Execution Process

### Invocation

```bash
# Start new recursive workflow
/recursive_workflow

# Resume suspended workflow
/recursive_workflow resume workflow_id=abc-123-def
```

### Workflow Parameters

When starting a new workflow, provide:

```markdown
**Issue Description**: [Clear description of the problem]

**Affected Modules**: [Which modules are involved]
- [ ] Backend (Rust/Actix-web)
- [ ] Frontend (React/TypeScript)
- [ ] Database (FoundationDB)
- [ ] Infrastructure (K8s/GCP)

**Known Constraints**: [Any limitations or requirements]

**Success Criteria**: [How to know when resolved]
```

### Execution Loop

```python
def execute_workflow(workflow_id):
    state = load_state(workflow_id)

    while state.current_state != "COMPLETE":
        # Check token budget
        gauge_result = run_complexity_gauge()
        if gauge_result.status == "CRITICAL":
            transition_to("CHECKPOINT")
            break

        # Execute current state
        result = execute_state(state.current_state, state.state_data)

        # Determine next state
        if result.success:
            next_state = get_next_state(state.current_state)
        else:
            next_state = traceback(result.failure_type, state.current_state)

        # Transition
        state = transition(state, next_state, result.data)
        save_state(workflow_id, state)

        # Increment iteration if traceback
        if next_state in ["IDENTIFY", "SOLVE", "CODE"]:
            state.iteration_count += 1
            if state.iteration_count >= 10:
                transition_to("ESCALATE")
                break

    return generate_completion_report(state)
```

### State Transition Logging

Every transition logged to FDB:

```json
{
  "workflow_id": "uuid",
  "transition_id": "uuid",
  "from_state": "CODE",
  "to_state": "DEPLOY",
  "timestamp": "2025-10-18T12:34:56Z",
  "reason": "Code changes complete, ready to deploy",
  "token_usage_at_transition": 45000,
  "state_data": { /* relevant data */ }
}
```

## Integration with Other Commands

### With Complexity Gauge

**Check before each major state**:
```markdown
Before transitioning to CODE state:

/complexity_gauge

If status is Warning or Critical:
- Consider CHECKPOINT
- Compress context
- Defer non-critical work
```

### With Context Management

**Save context at checkpoints**:
```bash
# When entering CHECKPOINT state:
/context_save project_root=/home/hal/v4/PROJECTS/t2 context_type=comprehensive

# When resuming:
/context_restore project:t2 mode=full
```

### With Orchestrator

**Orchestrator can invoke recursive workflow for complex issues**:

```markdown
## Phase 4: Fix Cascading Bug

This issue spans backend, frontend, and database. Use recursive workflow:

/recursive_workflow

Issue: Session invalidation not propagating to frontend
Modules: Backend (auth.rs), Frontend (authStore.ts), Database (session table)
Success: User logged out in UI when session invalidated server-side
```

## Output Format

### Workflow Progress Report

```markdown
## 🔄 RECURSIVE WORKFLOW PROGRESS

**Workflow ID**: abc-123-def-456
**Session**: 2 of 2
**Status**: IN_PROGRESS
**Current State**: TEST (6 of 9)
**Iteration**: 2

---

### 📊 State Transitions

1. ✅ INITIATE → IDENTIFY (Iteration 1)
2. ✅ IDENTIFY → DOCUMENT (Iteration 1)
3. ✅ DOCUMENT → SOLVE (Iteration 1)
4. ✅ SOLVE → CODE (Iteration 1)
5. ✅ CODE → DEPLOY (Iteration 1)
6. ⚠️ DEPLOY → TEST → ❌ FAIL (Iteration 1)
7. 🔄 TRACEBACK → SOLVE (Iteration 2, reason: Tests failed)
8. ✅ SOLVE → CODE (Iteration 2)
9. ✅ CODE → DEPLOY (Iteration 2)
10. 🔵 **CURRENT** → TEST (Iteration 2)

---

### 🎯 Current State: TEST

**Actions in progress:**
- Running backend tests: `cargo test`
- Running frontend tests: `npm run test`
- Validating integration

**Token Usage**: 67K / 160K (42%)
**Complexity Score**: 145 points (Moderate)

---

### 📦 Affected Modules

- ✅ **Backend** (Rust): auth.rs modified (line 167, 302, 337)
- 🔵 **Frontend** (TypeScript): authStore.ts in progress
- ⏳ **Database** (FDB): No changes yet

**Dependency Chain**: Backend → Frontend → (validate end-to-end)

---

### 🔍 Issues Resolved This Iteration

**Iteration 1** (Failed):
- ❌ Backend tests failed: JWT signature mismatch
- Root cause: Missing algorithm parameter

**Iteration 2** (Current):
- ✅ Fixed JWT algorithm configuration
- ✅ Backend tests now pass
- 🔵 Testing frontend integration...

---

### 📈 Metrics

**Time Elapsed**: 18 minutes
**States Executed**: 10
**Iterations**: 2 of 10 max
**Token Usage**: 67K (42% of budget)
**Files Modified**: 3

---

### ⏭️ Next Actions

If TEST passes:
- Transition to VALIDATE
- Check success criteria
- Confirm no regressions

If TEST fails:
- Analyze failure
- Traceback to appropriate state (likely CODE or SOLVE)
- Iteration 3
```

## Advanced Features

### 1. Parallel Path Execution

For independent modules, execute states in parallel:

```
IDENTIFY (finds 3 independent bugs)
   ├─ Path A: Bug 1 (Backend only)
   ├─ Path B: Bug 2 (Frontend only)
   └─ Path C: Bug 3 (Database only)

Each path runs DOCUMENT → SOLVE → CODE → DEPLOY → TEST independently

Final VALIDATE merges all paths
```

### 2. Nested Workflows

Complex issues may spawn sub-workflows:

```
Main Workflow: Authentication System Overhaul
  ├─ Sub-workflow 1: JWT Token Refresh
  ├─ Sub-workflow 2: Session Storage Migration
  └─ Sub-workflow 3: Frontend Auth State Sync
```

Each sub-workflow has its own FSM state machine.

### 3. Conditional Branching

States can have conditional transitions:

```
TEST result:
  ├─ All pass → VALIDATE
  ├─ Frontend only fail → CODE (frontend fix)
  ├─ Backend only fail → CODE (backend fix)
  └─ Both fail → SOLVE (wrong approach)
```

## Best Practices

### Iteration Limits

- **Max iterations**: 10 (hard limit)
- **Warning at**: 5 iterations (consider ESCALATE)
- **Checkpoint recommended**: Every 3 iterations

### Token Budget Management

- **Run `/complexity_gauge`**: Before each major state
- **Checkpoint trigger**: > 85% token usage
- **Context compression**: > 70% token usage

### State Persistence Frequency

- **Every transition**: Save to FDB
- **After failures**: Immediate save
- **Before CHECKPOINT**: Full save + context archive

### Error Handling

- **Retry limit**: 3 attempts per state
- **Escalation**: After 10 iterations or 3 retry failures
- **Logging**: All failures recorded with context

## Troubleshooting

### "Workflow stuck in loop (IDENTIFY → SOLVE → CODE → TEST → IDENTIFY)"

**Cause**: Test failures not providing enough info for fix

**Solution**:
- Add explicit failure analysis in TEST state
- Improve error messages
- Use `codebase-pattern-finder` for similar fixes
- Consider ESCALATE if iteration > 5

### "Context collapse during long workflow"

**Cause**: Too many iterations without CHECKPOINT

**Solution**:
- Trigger CHECKPOINT at 70% token budget (not 85%)
- Use aggressive context compression
- Archive completed states immediately

### "Workflow state lost after session restart"

**Cause**: FDB state not persisted or query failed

**Solution**:
- Verify FDB connection
- Check workflow_id is correct
- Use `/context_restore` with correct project ID
- Review FDB key structure

## References

- **Research source**: `thoughts/shared/research/2025-10-18-multi-agent-orchestration-research.md`
- **FSM patterns**: MetaAgent (OpenReview), Temporal.io workflows
- **Context management**: AgentOrchestra, MegaAgent hierarchical coordination
- **Related commands**: `/complexity_gauge`, `/context_save`, `/context_restore`
- **Architecture**: `docs/DEFINITIVE-V5-ARCHITECTURE.md`
- **FDB schema**: `docs/reference/FDB-MODELS-IMPLEMENTATION-CHECKLIST.md`

---

**Last Updated**: 2025-10-18
**Project**: Coditect AI IDE (T2)
**Status**: Production-ready recursive workflow orchestration
