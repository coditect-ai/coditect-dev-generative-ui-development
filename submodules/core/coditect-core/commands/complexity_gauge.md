# Complexity Gauge: Token Budget and Workflow Complexity Monitor

## Role and Purpose

An intelligent complexity monitoring specialist focused on tracking token usage, dependency complexity, and context window management across multi-agent orchestration workflows. This command helps prevent context collapse by providing early warnings and triggering appropriate context management strategies.

## Overview

The Complexity Gauge command is designed to:
- Monitor token consumption across orchestrated workflows
- Track complexity metrics (dependency depth, module breadth, agent invocations)
- Predict context window overflow before it occurs
- Recommend context management strategies (summarization, chunking, archiving)
- Generate actionable complexity reports for orchestrators
- Enable intelligent workflow throttling and batching

## When to Use This Command

**✅ Use `/complexity_gauge` when:**
- Starting multi-phase workflows (estimate complexity upfront)
- Mid-workflow to check remaining token budget
- Before spawning multiple parallel subagents
- When workflows involve recursive or cascading dependencies
- After completing a major phase (assess cumulative usage)
- When context feels "heavy" or approaching limits

**❌ Don't use for:**
- Simple single-agent tasks
- Workflows with < 3 phases
- Quick file lookups or searches
- Already-complete workflows

## Input Parameters

When invoked, provide context about the current workflow:

- **Current Phase**: Which phase of the workflow you're in
- **Completed Phases**: List of already-executed phases with token estimates
- **Remaining Phases**: Upcoming phases with estimated complexity
- **Subagents Used**: Count and types of subagents already invoked
- **Dependency Graph**: Number of modules/components involved

## Complexity Metrics

### 1. Token Usage Tracking

**Current Token Usage Formula:**
```
Total Tokens =
  Σ(Context Read) +
  Σ(Subagent Prompts) +
  Σ(Subagent Responses) +
  Σ(Tool Results) +
  Current Context Size
```

**Budget Calculation:**
```
Available Budget = 160,000 tokens (Claude Sonnet 4.5 limit)
Safety Threshold = 70% (112,000 tokens)
Warning Threshold = 85% (136,000 tokens)
Critical Threshold = 95% (152,000 tokens)
```

### 2. Workflow Complexity Scoring

Assign complexity points based on:

| Factor | Points | Examples |
|--------|--------|----------|
| **Module Count** | 5 per module | Frontend, Backend, Database, Infrastructure |
| **Dependency Depth** | 10 per level | Direct, transitive, deep cascades |
| **Subagent Invocations** | 3 per agent | codebase-analyzer, codebase-locator, etc. |
| **File Operations** | 1 per file | Read, Edit, Write operations |
| **Context Switches** | 15 per switch | Handoffs between agents or phases |
| **Recursive Calls** | 20 per recursion | Retry loops, traceback iterations |

**Complexity Score Ranges:**
- **Simple**: 0-50 points (< 30K tokens)
- **Moderate**: 51-150 points (30K-60K tokens)
- **Complex**: 151-300 points (60K-100K tokens)
- **Very Complex**: 301+ points (100K-160K tokens)

### 3. Dependency Graph Analysis

**Breadth**: Number of distinct modules involved
**Depth**: Longest dependency chain (A → B → C → D = depth 4)
**Cascading Risk**: Modules where changes trigger multiple downstream impacts

**Risk Score:**
```
Risk = (Breadth × Depth × Cascading Factor)

Cascading Factor:
- Isolated change: 1.0
- 2-3 downstream impacts: 1.5
- 4-6 downstream impacts: 2.0
- 7+ downstream impacts: 3.0
```

## Analysis Process

### Step 1: Gather Workflow Context

Collect information about the current workflow state:

1. **What phase are we in?** (e.g., Phase 3 of 7)
2. **What's been done so far?** (List completed phases with token estimates)
3. **What remains?** (List pending phases with estimates)
4. **How many subagents have been invoked?** (Count and types)
5. **What modules are involved?** (Frontend, Backend, DB, etc.)
6. **Are there recursive elements?** (Retry loops, cascading fixes)

### Step 2: Calculate Current Token Usage

Estimate token consumption:

```
Phase 1 (Research):
  - codebase-locator: ~8K tokens
  - codebase-analyzer: ~12K tokens
  - File reads (5 files): ~10K tokens
  - Total: ~30K tokens

Phase 2 (Design):
  - Orchestrator planning: ~5K tokens
  - Design validation: ~8K tokens
  - Total: ~13K tokens

Cumulative so far: 43K tokens
Remaining budget: 117K tokens (73% available)
```

### Step 3: Project Remaining Token Needs

Estimate tokens for pending phases:

```
Phase 3 (Backend Implementation): ~25K tokens
Phase 4 (Frontend Implementation): ~20K tokens
Phase 5 (Testing): ~15K tokens
Phase 6 (Integration): ~18K tokens
Phase 7 (Documentation): ~8K tokens

Total projected: ~86K tokens
Grand total estimate: 43K + 86K = 129K / 160K (81% usage)
```

### Step 4: Identify Risk Factors

Flag potential issues:

- **❌ Over-budget risk**: Projected usage > 140K tokens
- **⚠️ Warning zone**: Projected usage 112K-140K tokens
- **✅ Safe zone**: Projected usage < 112K tokens

**Risk factors:**
- Recursive workflows (unpredictable token growth)
- Large file reads (> 2000 lines per file)
- Many parallel subagents (> 5 concurrent)
- Deep dependency chains (> 4 levels)
- Poorly scoped phases (vague success criteria)

### Step 5: Recommend Mitigation Strategies

Based on risk level, suggest actions:

#### If **Safe Zone** (< 70% budget used):
✅ **Continue as planned** - No action needed
✅ **Consider expansion** - Add optional enhancements if desired

#### If **Warning Zone** (70-85% budget used):
⚠️ **Implement summarization** - Use `/context_save` to archive completed phases
⚠️ **Defer non-critical tasks** - Move optional work to follow-up sessions
⚠️ **Batch file operations** - Read multiple files in parallel, not sequentially
⚠️ **Limit subagent responses** - Request focused, concise outputs

#### If **Critical Zone** (85-95% budget used):
🔴 **Mandatory summarization** - Archive all non-essential context immediately
🔴 **Split workflow** - Pause and create handoff document for next session
🔴 **Cancel optional phases** - Focus only on core requirements
🔴 **Aggressive chunking** - Use incremental approaches, avoid large operations

#### If **Over-budget** (> 95% budget used):
🚨 **STOP** - Do not proceed with current workflow
🚨 **Emergency context save** - Create comprehensive checkpoint with `/context_save`
🚨 **Handoff document** - Write detailed continuation plan for next session
🚨 **Session restart** - Begin new session with restored context

## Output Format

### Complexity Report Structure

```markdown
## 🎯 COMPLEXITY GAUGE REPORT

**Workflow**: [Workflow name]
**Current Phase**: [X of Y]
**Timestamp**: [ISO 8601 timestamp]

---

### 📊 Token Budget Analysis

**Current Usage**: [X]K / 160K ([Y]%)
**Projected Total**: [Z]K / 160K ([W]%)
**Status**: [Safe Zone | Warning Zone | Critical Zone | Over-budget]

**Budget Breakdown:**
- Phase 1: [X]K tokens
- Phase 2: [Y]K tokens
- Phase 3 (projected): [Z]K tokens
- ...

**Remaining Budget**: [X]K tokens ([Y]% available)

---

### 🔬 Complexity Scoring

**Complexity Score**: [X] points ([Simple | Moderate | Complex | Very Complex])

**Factors:**
- Modules involved: [N] × 5 = [X] points
- Dependency depth: [N] levels × 10 = [X] points
- Subagent invocations: [N] × 3 = [X] points
- File operations: [N] × 1 = [X] points
- Context switches: [N] × 15 = [X] points
- Recursive calls: [N] × 20 = [X] points

**Total**: [X] points

---

### 🌐 Dependency Graph

**Breadth**: [N] modules
**Depth**: [N] levels (longest chain: [A → B → C])
**Cascading Risk**: [Low | Medium | High | Critical]

**Modules:**
- Backend (Rust/Actix-web)
- Frontend (React/TypeScript)
- Database (FoundationDB)
- Infrastructure (K8s/GCP)

**Key Dependencies:**
- [Module A] → [Module B]: [Impact description]
- [Module B] → [Module C]: [Impact description]

---

### ⚠️ Risk Assessment

**Overall Risk Level**: [Low | Medium | High | Critical]

**Identified Risks:**
- [Risk 1]: [Description + Likelihood]
- [Risk 2]: [Description + Likelihood]
- [Risk 3]: [Description + Likelihood]

---

### 💡 Recommended Actions

**Immediate (This phase):**
1. [Action 1]
2. [Action 2]

**Short-term (Next 1-2 phases):**
1. [Action 1]
2. [Action 2]

**Long-term (Remaining workflow):**
1. [Action 1]
2. [Action 2]

---

### 🎬 Decision Point

**Should we continue?**
- ✅ Yes, proceed as planned (Safe zone)
- ⚠️ Yes, with modifications (Warning zone - apply recommended actions)
- 🔴 Pause and optimize (Critical zone - mandatory context management)
- 🚨 Stop and handoff (Over-budget - session restart required)
```

## Integration with Other Commands

### Use With Orchestrator

The orchestrator should invoke `/complexity_gauge` at strategic points:

```markdown
## Phase 3: Backend Implementation

**Before starting:**
Run complexity check to ensure sufficient token budget:

/complexity_gauge

If status is Warning or Critical, apply recommended mitigations before proceeding.
```

### Use With Context Management

Trigger context management based on gauge results:

```bash
# If complexity_gauge returns "Warning Zone":
/context_save project_root=/home/hal/v4/PROJECTS/t2 context_type=standard

# Continue with reduced context footprint
```

### Use With Recursive Workflows

Monitor complexity during recursive iterations:

```markdown
# In recursive_workflow command:
- Execute phase
- Run /complexity_gauge
- If budget allows, continue recursion
- If budget critical, checkpoint and defer
```

## Advanced Features

### 1. Predictive Token Estimation

Estimate tokens for upcoming operations:

**File Read Estimation:**
- Small file (< 500 lines): ~2K tokens
- Medium file (500-2000 lines): ~5K tokens
- Large file (> 2000 lines): ~10K+ tokens

**Subagent Invocation Estimation:**
- codebase-locator: ~8K tokens (prompt + response)
- codebase-analyzer: ~12K tokens
- codebase-pattern-finder: ~10K tokens
- thoughts-analyzer: ~8K tokens
- web-search-researcher: ~15K tokens (with web results)

**Phase Type Estimation:**
- Research phase: 20K-40K tokens
- Design phase: 10K-20K tokens
- Implementation phase: 25K-50K tokens
- Testing phase: 15K-25K tokens
- Documentation phase: 8K-15K tokens

### 2. Context Compression Strategies

When context is heavy, recommend compression:

**Level 1 (Light compression - 10-20% reduction):**
- Summarize completed phases into 3-5 bullet points
- Remove verbose subagent outputs, keep only key findings
- Archive file contents, keep only file:line references

**Level 2 (Moderate compression - 30-40% reduction):**
- Aggressive phase summarization (1-2 sentences per phase)
- Remove all file contents, keep metadata only
- Consolidate duplicate information
- Store detailed context in FoundationDB, keep references only

**Level 3 (Heavy compression - 50-70% reduction):**
- Minimal phase tracking (state machine only)
- External storage for all details (FDB + file system)
- Keep only: current state, next actions, critical blockers
- Use `/context_save` to archive everything else

### 3. Real-time Monitoring

Provide ongoing complexity tracking:

```
Phase 1 complete: 30K tokens used (19% budget)
Phase 2 complete: 43K tokens used (27% budget) ✅ Safe
Phase 3 in progress: ~68K tokens projected (43% budget) ✅ Safe
```

## Best Practices

### When to Check Complexity

**Always check before:**
- Starting multi-phase workflows
- Spawning > 3 parallel subagents
- Reading > 5 files
- Recursive operations
- Complex refactoring tasks

**Check during:**
- Long-running workflows (every 2-3 phases)
- When context feels heavy
- After major file operations
- Before critical decision points

**Check after:**
- Completing major milestones
- Encountering unexpected complexity
- Workflow deviations from plan

### Token Budget Allocation

**Conservative allocation (safe approach):**
- Research: 25% (40K tokens)
- Implementation: 40% (64K tokens)
- Testing/Validation: 20% (32K tokens)
- Documentation: 10% (16K tokens)
- Buffer: 5% (8K tokens)

**Aggressive allocation (experienced teams):**
- Research: 15% (24K tokens)
- Implementation: 50% (80K tokens)
- Testing/Validation: 25% (40K tokens)
- Documentation: 5% (8K tokens)
- Buffer: 5% (8K tokens)

## Troubleshooting

### Common Issues

**"Complexity score seems too high"**
- Review scoring factors for accuracy
- Check if recursive elements are being double-counted
- Verify module counts are correct

**"Token projections inaccurate"**
- Use actual measurements from completed phases
- Adjust estimates based on project patterns
- Add 20% buffer for uncertainty

**"Risk level escalates unexpectedly"**
- Identify which metric triggered escalation
- Review dependency graph for hidden complexity
- Consider splitting workflow into smaller chunks

## References

- **Research source**: `thoughts/shared/research/2025-10-18-multi-agent-orchestration-research.md`
- **Context patterns**: Temporal.io, Kafka, MegaAgent, AgentOrchestra research
- **Related commands**: `/context_save`, `/context_restore`, orchestrator workflows
- **Architecture docs**: `docs/DEFINITIVE-V5-ARCHITECTURE.md`

---

**Last Updated**: 2025-10-18
**Project**: Coditect AI IDE (T2)
**Status**: Production-ready context management tool
