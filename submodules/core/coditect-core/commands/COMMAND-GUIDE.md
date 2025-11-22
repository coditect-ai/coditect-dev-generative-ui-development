# Command Selection Guide

**How to know which command to use when.**

## Quick Decision Tree

```
START: What do you want to do?
│
├─ Plan/Design something?
│  ├─ Architecture/system design → /strategy
│  ├─ Task breakdown → /deliberation
│  ├─ Create implementation plan → /create_plan
│  └─ Validate existing plan → /validate_plan
│
├─ Research/Verify something?
│  ├─ Verify assumptions/APIs → /research
│  ├─ Search codebase → /research_codebase
│  └─ Web research → Use web-search-researcher agent
│
├─ Implement something?
│  ├─ Production code → /implement
│  ├─ Quick prototype → /prototype
│  ├─ One-shot feature → /oneshot
│  └─ Execute existing plan → /implement_plan
│
├─ Review/Analyze something?
│  ├─ Code quality review → /analyze
│  ├─ Local code review → /local_review
│  └─ Debug issues → /debug
│
├─ Optimize something?
│  ├─ Performance optimization → /optimize
│  └─ (covered by /optimize command)
│
├─ Document something?
│  ├─ API docs, architecture → /document
│  └─ Describe PR → /describe_pr or /ci_describe_pr
│
├─ Git workflow?
│  ├─ Create commit → /commit or /ci_commit
│  ├─ Create PR description → /describe_pr
│  └─ Create worktree → /create_worktree
│
└─ Session handoff?
   ├─ End session → /create_handoff
   └─ Resume session → /resume_handoff
```

## Command Categories

### Planning Commands (Start Here)

| Command | When to Use | Output |
|---------|-------------|--------|
| **/deliberation** | Pure planning, NO code - analyze requirements, decompose tasks | Task breakdown, dependency graph, alternatives |
| **/strategy** | Architectural planning, system design | C4 diagrams, ADR, migration path |
| **/create_plan** | Create implementation plan for feature | Step-by-step execution plan |
| **/validate_plan** | Validate existing plan before execution | Plan review, risk assessment |

**Decision**: Start with `/deliberation` for complex tasks, `/strategy` for architecture.

---

### Research/Verification Commands

| Command | When to Use | Output |
|---------|-------------|--------|
| **/research** | Verify assumptions, check APIs/packages exist (5-20 tool calls) | Verification report, blockers, recommendations |
| **/research_codebase** | Search codebase for patterns, examples | File locations, code examples |

**Decision**: Use `/research` after `/deliberation` to verify feasibility.

---

### Implementation Commands (Do the Work)

| Command | When to Use | Output |
|---------|-------------|--------|
| **/action** | Implementation mode - ONE artifact per response | Working code, tests, docs |
| **/implement** | Production-ready implementation with all quality gates | Full implementation with circuit breakers, tests, observability |
| **/prototype** | Rapid prototyping - skip some production requirements | Quick working code with TODO markers |
| **/oneshot** | Single-shot implementation without plan | Complete feature in one go |
| **/implement_plan** | Execute existing plan step-by-step | Implementation following plan |

**Decision**: Use `/implement` for production, `/prototype` for experiments, `/action` for autonomous mode.

---

### Review/Quality Commands

| Command | When to Use | Output |
|---------|-------------|--------|
| **/analyze** | Code review using evaluation-framework rubrics | Scores (1-5), justifications, improvements |
| **/local_review** | Local code review workflow | Review report |
| **/debug** | Debugging assistance | Debug analysis, fixes |

**Decision**: Use `/analyze` after implementation to verify quality.

---

### Optimization Commands

| Command | When to Use | Output |
|---------|-------------|--------|
| **/optimize** | Performance optimization with benchmarks | Before/after code, benchmark results |

---

### Documentation Commands

| Command | When to Use | Output |
|---------|-------------|--------|
| **/document** | Generate API docs, architecture, runbooks | OpenAPI specs, C4 diagrams, user guides |
| **/describe_pr** | Create PR description | PR title, summary, test plan |

---

### Git Workflow Commands

| Command | When to Use | Output |
|---------|-------------|--------|
| **/commit** | Create git commit | Commit with conventional format |
| **/ci_commit** | CI commit workflow | Commit for CI/CD |
| **/describe_pr** | PR description | PR summary |
| **/create_worktree** | Git worktree management | New worktree |

---

### Session Management Commands

| Command | When to Use | Output |
|---------|-------------|--------|
| **/create_handoff** | End session, create handoff doc | Handoff markdown |
| **/resume_handoff** | Resume from handoff | Restored context |

---

## Workflow Patterns

### Pattern 1: Full Feature Development (Comprehensive)
```
1. /deliberation - Analyze requirements, decompose tasks
2. /research - Verify assumptions, check APIs
3. /strategy - Design architecture (if needed)
4. /implement - Production implementation
5. /analyze - Code review
6. /document - Generate docs
7. /commit - Create commit
8. /describe_pr - Create PR
```

### Pattern 2: Quick Feature (Fast)
```
1. /prototype - Rapid implementation
2. /local_review - Quick review
3. /commit - Create commit
```

### Pattern 3: Bug Fix
```
1. /debug - Analyze issue
2. /implement - Fix with tests
3. /commit - Create commit
```

### Pattern 4: Performance Work
```
1. /analyze - Identify bottlenecks
2. /optimize - Improve performance
3. /commit - Create commit
```

### Pattern 5: Autonomous Development
```
1. "Use autonomous mode with DELIBERATION" - Plan
2. "Continue with RESEARCH" - Verify
3. "Continue with ACTION" - Implement (use /action internally)
```

---

## When Orchestrator Should Auto-Invoke

The **orchestrator agent** should automatically invoke commands for:

### Auto-Invoke Scenarios

| User Request | Orchestrator Should Invoke |
|--------------|----------------------------|
| "Implement user profile editing" | `/deliberation` → `/research` → `/implement` |
| "Fix JWT expiration bug" | `/debug` → `/implement` |
| "Review authentication code" | `/analyze` |
| "Optimize database queries" | `/analyze` → `/optimize` |
| "Document the API" | `/document` |
| "Create PR for feature X" | `/describe_pr` |

### Orchestrator Decision Logic

**Orchestrator uses commands when**:
- User request matches workflow pattern
- Multi-step process requires coordination
- Quality gates must be enforced

**Orchestrator does NOT use commands when**:
- Simple single-step tasks
- User explicitly requests specific agent
- Clarifying questions

---

## How to Use This Guide

### For Users

**Starting a task:**
1. Read the Quick Decision Tree
2. Find matching command
3. Invoke: `/command-name [arguments]`

**Not sure?**
- Ask: "Which command should I use for [task]?"
- Orchestrator will recommend based on this guide

### For Orchestrator

**When user requests feature development:**
1. Identify workflow pattern (Full Feature, Quick Feature, etc.)
2. Invoke commands in sequence
3. Report progress after each command

**Decision criteria:**
- Complexity → Full Feature workflow
- Urgency → Quick Feature workflow
- Bug → Bug Fix workflow
- Performance → Performance workflow

---

## Command Cheat Sheet

**Planning**: `/deliberation`, `/strategy`, `/create_plan`
**Research**: `/research`, `/research_codebase`
**Implementation**: `/implement`, `/action`, `/prototype`
**Review**: `/analyze`, `/local_review`
**Optimization**: `/optimize`
**Documentation**: `/document`
**Git**: `/commit`, `/describe_pr`
**Session**: `/create_handoff`, `/resume_handoff`

---

## Next Steps

1. **Bookmark this guide** - Reference when choosing commands
2. **Update orchestrator** - Configure auto-invoke logic
3. **Test workflows** - Try Pattern 1 (Full Feature Development)
4. **Provide feedback** - Refine command selection over time
