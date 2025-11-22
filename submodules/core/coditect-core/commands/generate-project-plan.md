---
name: generate-project-plan
description: Autonomous project specification and multi-agent orchestration plan generator for submodules
version: 1.0
category: project-management
tags: [specification, planning, orchestration, automation, multi-agent]
keywords: [project plan, submodule, specification, orchestration, tasklist, multi-agent, autonomous, implementation plan]
purpose: Generate complete project specifications and multi-agent orchestration plans for submodule implementation
trigger_phrases:
  - "create project plan for"
  - "generate implementation plan"
  - "need project specifications"
  - "set up multi-agent orchestration"
  - "create tasklist for submodule"
  - "autonomous project planning"
  - "specification and management"
automation_level: fully_automated
estimated_time: 10-30 minutes
output_files:
  - PROJECT-PLAN.md (25-30 KB)
  - TASKLIST-WITH-CHECKBOXES.md (40-50 KB)
  - docs/ (if missing)
agents_used:
  - orchestrator (coordination)
  - software-design-document-specialist (documentation)
  - agent-dispatcher (agent selection)
requires_human: false
---

# Generate Project Plan & Orchestration Artifacts

**Autonomous submodule specification and multi-agent implementation planning system.**

## Purpose

Automatically generate complete project specifications, implementation plans, and multi-agent orchestration artifacts for any CODITECT submodule. This command:

1. **Detects** current submodule context
2. **Analyzes** existing documentation (or creates if missing)
3. **Generates** comprehensive specifications
4. **Creates** PROJECT-PLAN.md with multi-agent orchestration strategy
5. **Creates** TASKLIST-WITH-CHECKBOXES.md with detailed task breakdown
6. **Provides** agent invocation syntax for autonomous execution

## 🤖 CR Command Router Help

The `cr` (coditect-router) command can automatically recommend this command when you describe your need in plain English.

### How CR Works

The AI-powered router analyzes your request and suggests the best command:

```bash
# Ask cr what to do
cr "I need to create a complete implementation plan for my new backend submodule"

# CR will recommend:
# 📍 RECOMMENDED COMMAND: /generate-project-plan
# 💭 REASONING: Detected submodule planning request requiring multi-agent orchestration
# 📋 NEXT STEPS:
#    1. Navigate to submodule directory
#    2. Run: /generate-project-plan
#    3. Review generated PROJECT-PLAN.md and TASKLIST-WITH-CHECKBOXES.md
```

### Trigger Phrases for CR

The router will recommend this command when you use phrases like:
- "create project plan for [submodule]"
- "generate implementation plan"
- "need project specifications"
- "set up multi-agent orchestration"
- "create tasklist for submodule"
- "autonomous project planning"
- "specification and management"

### CR Interactive Mode

```bash
# Start interactive mode
cr -i

# Then describe your need:
📝 What do you want to do? > I'm starting a new project and need a complete plan with agent coordination

# CR analyzes and recommends this command
```

### User Feedback Loop

After using this command, you can provide feedback to improve recommendations:

```bash
# Tell CR what worked
cr feedback "generate-project-plan worked perfectly for my backend submodule"

# Or report issues
cr feedback "generate-project-plan needs better documentation detection"
```

## When to Use

- Starting a new submodule project
- Need complete implementation plan with agent orchestration
- Want checkbox-based tasklist for progress tracking
- Require specification documentation for existing submodule
- Setting up multi-agent autonomous development workflow
- Coordinating multiple specialized agents for complex projects

## Usage

### Basic Usage (Current Directory)
```bash
/generate-project-plan
```
Analyzes current submodule, generates all artifacts.

### Specify Target Submodule
```bash
/generate-project-plan submodules/coditect-cloud-backend
```
Analyzes specified submodule path.

### Custom Options
```bash
/generate-project-plan --phases 3 --weeks 12 --budget 100000
```
Customize planning parameters.

## What Gets Created

### 1. Documentation Analysis & Generation

**If docs/ exists:**
- Reads all existing documentation
- Analyzes architecture, design decisions, specifications
- Identifies gaps and missing documentation

**If docs/ missing:**
- Generates Software Design Document (SDD)
- Creates C4 architecture diagrams
- Writes Architecture Decision Records (ADRs)
- Documents database schema, APIs, deployment strategy

### 2. PROJECT-PLAN.md

Complete implementation plan including:
- **Phase breakdown** (Infrastructure, Backend, Frontend, etc.)
- **Weekly milestones** with deliverables
- **Multi-agent orchestration strategy**
- **Agent assignment matrix** (which agent for which tasks)
- **Budget breakdown** (engineering, infrastructure, contingency)
- **Risk management** (risks, mitigation strategies)
- **Success metrics** (technical, adoption, business)
- **Quality gates** (phase completion criteria)
- **Agent invocation examples** (code snippets for ORCHESTRATOR)

### 3. TASKLIST-WITH-CHECKBOXES.md

Detailed task breakdown with:
- **185+ checkbox tasks** across all phases
- **Agent assignments** (which specialized agent executes each task)
- **Time estimates** (hours per task)
- **Dependencies** (sequential vs parallel execution)
- **Acceptance criteria** (how to verify task completion)
- **Progress tracking** (weekly milestone summaries)
- **Orchestration guidance** (sequential chains, parallel execution patterns)

### 4. docs/ Structure (if created)

```
docs/
├── EXECUTIVE-SUMMARY-{project}.md
├── SOFTWARE-DESIGN-DOCUMENT-{project}.md
├── C4-DIAGRAMS-{project}.md
├── DATABASE-ARCHITECTURE-{project}.md
└── adrs/
    ├── README.md
    ├── ADR-001-{decision}.md
    ├── ADR-002-{decision}.md
    └── ...
```

## Execution Workflow

### Step 1: Context Detection

```python
# Detect current working directory
cwd = os.getcwd()

# Check if inside submodule
if "submodules/" in cwd:
    submodule_name = extract_submodule_name(cwd)
    submodule_path = find_submodule_root(cwd)
else:
    # Prompt user for submodule path
    submodule_path = prompt_for_submodule()
```

### Step 2: Documentation Analysis

```python
# Check for existing documentation
docs_dir = os.path.join(submodule_path, "docs")

if os.path.exists(docs_dir):
    # Analyze existing docs
    existing_docs = analyze_documentation(docs_dir)
    documentation_status = "COMPLETE" if all_required_present(existing_docs) else "PARTIAL"
else:
    # Generate missing documentation
    Task(
        subagent_type="software-design-document-specialist",
        prompt=f"Generate complete software design documentation for {submodule_name}.
        Analyze existing README.md and code structure.
        Create: SDD (67K+ words), C4 diagrams (9+ diagrams),
        Database architecture, 8+ ADRs with 40/40 quality scores.
        Output to: {docs_dir}/"
    )
```

### Step 3: Project Plan Generation

```python
# Generate implementation plan with multi-agent orchestration
Task(
    subagent_type="orchestrator",
    prompt=f"""Create comprehensive PROJECT-PLAN.md for {submodule_name}.

Documentation available:
{documentation_summary}

Requirements:
1. Analyze existing docs to understand architecture, tech stack, requirements
2. Break implementation into 3-4 phases (e.g., Infrastructure, Backend, Frontend, Launch)
3. Create weekly milestones (8-12 weeks total)
4. Assign specialized agents to each task area:
   - devops-engineer for infrastructure
   - rust-expert-developer for backend (adapts to language)
   - frontend-react-typescript-expert for frontend
   - database-architect for database work
   - security-specialist for auth/security
   - multi-tenant-architect for multi-tenancy
   - monitoring-specialist for observability
   - etc.

5. Include budget breakdown (engineering hours + infrastructure costs)
6. Add risk management section (risks + mitigation)
7. Define success metrics (technical, adoption, business)
8. Provide agent invocation syntax examples

Output format: Follow coditect-project-intelligence/PROJECT-PLAN.md as template.
Target: 25-30 KB comprehensive plan ready for ORCHESTRATOR execution.
"""
)
```

### Step 4: Tasklist Generation

```python
# Generate checkbox-based tasklist
Task(
    subagent_type="orchestrator",
    prompt=f"""Create comprehensive TASKLIST-WITH-CHECKBOXES.md for {submodule_name}.

Based on PROJECT-PLAN.md phases:
{phases_summary}

Requirements:
1. Break each phase into detailed tasks (15-30 tasks per phase)
2. Each task must include:
   - [ ] Checkbox format
   - Agent assignment (which specialized agent)
   - Time estimate (hours)
   - Dependencies (task IDs that must complete first)
   - Acceptance criteria (verification method)

3. Add progress tracking:
   - Weekly milestone summaries
   - Phase completion criteria
   - Overall project progress percentage

4. Include orchestration guidance:
   - Sequential execution requirements (dependencies)
   - Parallel execution opportunities (independent tasks)
   - Multi-agent coordination patterns (when to use orchestrator)

5. Provide agent invocation examples for each phase

Output format: Follow coditect-project-intelligence/TASKLIST-WITH-CHECKBOXES.md as template.
Target: 180+ tasks across all phases, checkbox-based for progress tracking.
"""
)
```

### Step 5: Commit & Summary

```python
# Commit all generated artifacts
subprocess.run([
    "git", "add",
    "PROJECT-PLAN.md",
    "TASKLIST-WITH-CHECKBOXES.md",
    "docs/"
])

subprocess.run([
    "git", "commit", "-m",
    f"""Generate project plan and orchestration artifacts for {submodule_name}

- PROJECT-PLAN.md: Complete implementation plan with multi-agent orchestration
- TASKLIST-WITH-CHECKBOXES.md: {task_count} tasks across {week_count} weeks
- docs/: {doc_count} specification documents

Generated by: /generate-project-plan command
Ready for: ORCHESTRATOR-driven autonomous implementation

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
"""
])

# Display summary
print(f"""
✅ Project plan generation complete!

📁 Files created:
   - PROJECT-PLAN.md ({plan_size} KB)
   - TASKLIST-WITH-CHECKBOXES.md ({tasklist_size} KB)
   - docs/ ({doc_count} files, {docs_size} KB)

📊 Statistics:
   - Total phases: {phase_count}
   - Total weeks: {week_count}
   - Total tasks: {task_count}
   - Agent types: {agent_count}

🤖 Next steps:
   1. Review PROJECT-PLAN.md for overall strategy
   2. Check TASKLIST-WITH-CHECKBOXES.md for task breakdown
   3. Use ORCHESTRATOR agent to begin autonomous execution:

      Task(
          subagent_type="orchestrator",
          prompt="Execute Week 1 tasks from {submodule_name}/TASKLIST-WITH-CHECKBOXES.md"
      )
""")
```

## Multi-Agent Orchestration Patterns

### Pattern 1: Direct Agent Invocation (Simple Tasks)

```python
# Single agent completes entire task
Task(
    subagent_type="codi-devops-engineer",
    prompt="Deploy GCP infrastructure following infrastructure/DEPLOYMENT-PLAN.md"
)
```

### Pattern 2: Sequential Agent Chain (Dependent Tasks)

```python
# Agent A → Agent B → Agent C
# Week 1: Infrastructure setup
Task(subagent_type="codi-devops-engineer",
     prompt="Step 1: Provision GCP project and services")

# Wait for completion, then:
Task(subagent_type="database-architect",
     prompt="Step 2: Deploy PostgreSQL schema with RLS policies")

# Wait for completion, then:
Task(subagent_type="security-specialist",
     prompt="Step 3: Configure IAM and security policies")
```

### Pattern 3: Parallel Execution (Independent Tasks)

```python
# Week 5: Multiple parsers can run in parallel
# All these tasks are independent and can run simultaneously:

Task(subagent_type="rust-expert-developer",
     prompt="Create JSONL parser for unique_messages.jsonl")

Task(subagent_type="rust-expert-developer",
     prompt="Create JSON parser for checkpoint_index.json")

Task(subagent_type="rust-expert-developer",
     prompt="Create Markdown parser for CHECKPOINTS/*.md")
```

### Pattern 4: Orchestrated Coordination (Complex Workflows)

```python
# Orchestrator coordinates multiple agents
Task(
    subagent_type="orchestrator",
    prompt="""Coordinate git ingestion pipeline implementation.

Coordinate these agents:
1. senior-architect for service design
2. rust-expert-developer for parser implementation
3. database-architect for sync logic
4. codi-test-engineer for integration tests

Deliverables:
- Git clone/pull automation
- Three parsers (JSONL, JSON, Markdown)
- SHA-256 deduplication
- Idempotent sync
- 15+ integration tests

Target: Process 1,601 messages in <60 seconds
"""
)
```

## Command Options

### --phases N
Number of implementation phases (default: auto-detect)

```bash
/generate-project-plan --phases 3
```

### --weeks N
Total implementation weeks (default: auto-detect)

```bash
/generate-project-plan --weeks 12
```

### --budget N
Budget in USD (default: auto-calculate)

```bash
/generate-project-plan --budget 100000
```

### --agents "agent1,agent2,..."
Preferred agent list (default: auto-select)

```bash
/generate-project-plan --agents "devops-engineer,rust-expert-developer,frontend-expert"
```

### --template PATH
Use custom template for plan generation

```bash
/generate-project-plan --template ../coditect-project-intelligence/PROJECT-PLAN.md
```

### --skip-docs
Skip documentation generation (use existing only)

```bash
/generate-project-plan --skip-docs
```

### --update
Update existing plan (don't regenerate from scratch)

```bash
/generate-project-plan --update
```

## Output Format

### PROJECT-PLAN.md Structure

```markdown
# {Submodule Name} - Project Plan

## Project Overview
- Purpose
- Strategic Value
- Architecture Highlights

## Implementation Phases
### Phase 1: {Name} (Weeks X-Y)
- Goal
- Duration
- Team
- Budget
- Weekly breakdown
- Agent orchestration examples
- Acceptance criteria

### Phase 2: {Name} (Weeks X-Y)
...

## Multi-Agent Orchestration Strategy
- Agent roles & responsibilities
- Orchestration patterns (direct, sequential, parallel, coordinated)
- Example invocations

## Quality Gates
- Phase completion criteria

## Risk Management
- High-priority risks
- Mitigation strategies

## Success Metrics
- Technical metrics
- Adoption metrics
- Business metrics

## Budget Breakdown
- Engineering costs
- Infrastructure costs
- Total with contingency
```

### TASKLIST-WITH-CHECKBOXES.md Structure

```markdown
# {Submodule Name} - Implementation Tasklist

## Progress Summary
| Phase | Tasks | Completed | In Progress | Pending | % Complete |
|-------|-------|-----------|-------------|---------|------------|
| Phase 0 | 5 | 5 | 0 | 0 | 100% ✅ |
| Phase 1 | 75 | 0 | 0 | 75 | 0% ⏸️ |
...

## Phase 1: {Name} (Weeks X-Y)

### Week X: {Milestone}

#### X.1 {Task Group}
**Agent**: `agent-name`
**Duration**: N hours
**Dependencies**: X.Y, X.Z

- [ ] Specific task 1
- [ ] Specific task 2
- [ ] Specific task 3

**Acceptance**: Verification criteria

---

#### X.2 {Task Group}
...
```

## Integration with Other Commands

### After Plan Generation

```bash
# Start implementation
/implement

# Or use orchestrator directly
Task(subagent_type="orchestrator",
     prompt="Execute Week 1 tasks from PROJECT-PLAN.md")
```

### Update Existing Plan

```bash
# Regenerate with updates
/generate-project-plan --update

# Add new tasks
/generate-project-plan --append-tasks "Add Stripe integration, Add email notifications"
```

### Export Plan

```bash
# Export to different formats
/generate-project-plan --export pdf
/generate-project-plan --export html
```

## Examples

### Example 1: New Backend Submodule

```bash
cd submodules/coditect-api-gateway
/generate-project-plan
```

**Output:**
- Creates docs/SOFTWARE-DESIGN-DOCUMENT-api-gateway.md
- Creates docs/C4-DIAGRAMS-api-gateway.md
- Creates PROJECT-PLAN.md (4 phases, 10 weeks)
- Creates TASKLIST-WITH-CHECKBOXES.md (120 tasks)

### Example 2: Existing Submodule with Docs

```bash
cd submodules/coditect-cloud-frontend
/generate-project-plan
```

**Output:**
- Analyzes existing docs/
- Creates PROJECT-PLAN.md based on existing specs
- Creates TASKLIST-WITH-CHECKBOXES.md (95 tasks)

### Example 3: Custom Configuration

```bash
cd submodules/coditect-mobile-app
/generate-project-plan --phases 4 --weeks 16 --budget 150000 --agents "frontend-react-typescript-expert,mobile-app-specialist"
```

**Output:**
- Custom 4-phase, 16-week plan
- Budget allocated to $150K
- Prioritizes specified agents
- Creates PROJECT-PLAN.md + TASKLIST-WITH-CHECKBOXES.md

## Best Practices

1. **Run from submodule root**
   - Ensures correct context detection
   - Proper relative paths in generated files

2. **Review generated docs before committing**
   - Verify phase breakdown makes sense
   - Check agent assignments are appropriate
   - Validate budget and timeline estimates

3. **Use --update for iterative refinement**
   - Don't regenerate from scratch if plan already exists
   - Append new tasks instead of recreating

4. **Commit incrementally**
   - Commit docs/ separately from plans
   - Easier to review changes

5. **Start with ORCHESTRATOR**
   - Use orchestrator for phase-level execution
   - It will coordinate individual agents

## Troubleshooting

### "Cannot detect submodule context"
- Ensure you're inside a submodule directory
- Or provide explicit path: `/generate-project-plan submodules/name`

### "Insufficient documentation for plan generation"
- Use `--force-doc-generation` to create missing docs
- Or manually create docs/ with minimum requirements

### "Agent assignment unclear"
- Use `--agents` to specify preferred agents
- Review generated plan and manually adjust agent assignments

### "Budget/timeline unrealistic"
- Use `--budget N --weeks N` to override defaults
- Adjust after generation if needed

## Related Commands

- `/implement` - Execute implementation based on generated plan
- `/strategy` - Architectural planning (used internally by this command)
- `/document` - Documentation generation (used internally)
- `/agent-dispatcher` - Agent selection (used internally)
- `/suggest-agent` - Get agent recommendations for tasks

---

**Version**: 1.0
**Category**: Project Management
**Automation Level**: Fully Automated
**Dependencies**: orchestrator, software-design-document-specialist, agent-dispatcher
**Estimated Time**: 10-30 minutes (depending on submodule complexity)
**Output Size**: 50-100 KB (docs + plans)

🤖 **Ready for ORCHESTRATOR-driven autonomous implementation!**
