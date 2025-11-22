# 1-2-3 CODITECT Onboarding: Quick Guide
## Become a CODITECT-Enabled AI Operator in 30 Minutes

**Last Updated**: 2025-11-15 | **Version**: 1.0 | **Framework**: CODITECT v1.0 (78% Complete)

---

## 🎯 What You'll Master

By the end of this guide (30 minutes), you will:
- ✅ Initialize CODITECT projects with one command
- ✅ Invoke 50 specialized AI agents correctly
- ✅ Coordinate multi-agent workflows
- ✅ Manage context across sessions
- ✅ Begin building production-ready software immediately

---

## 📋 Prerequisites (5 minutes)

**Required:**
- Git installed
- Terminal access
- Basic command line knowledge

**Recommended:**
- Claude Code CLI ([install](https://code.claude.com/docs/en/installation))
- Anthropic API key ([get one](https://console.anthropic.com/))
- GitHub account

**Verify Setup:**
```bash
git --version          # Should show version
claude --version       # Optional but recommended
echo $ANTHROPIC_API_KEY  # Should show your key
```

---

## 🎯 STEP 0: Shell Setup for AI Router (2 minutes) - **DO THIS FIRST!**

### Why This Matters
Instead of memorizing 72 slash commands, you'll type plain English like:
- `cr "add user authentication"` ← AI suggests the right command
- `cri` ← Interactive mode for multiple questions

### Quick Setup (ZSH - macOS default)

```bash
# Add CODITECT AI Router aliases to your shell
cat >> ~/.zshrc << 'EOF'

# =============================================================================
# CODITECT AI Command Router
# =============================================================================
# Never memorize 72 slash commands - just describe what you want!
# Usage: cr "I need to add user authentication"
#        cri  (interactive mode)

# Auto-detect CODITECT location
if [[ -d "$HOME/PROJECTS/coditect-rollout-master/.coditect" ]]; then
    export CODITECT_ROUTER="$HOME/PROJECTS/coditect-rollout-master/.coditect/scripts/coditect-router"
elif [[ -d "$HOME/.coditect" ]]; then
    export CODITECT_ROUTER="$HOME/.coditect/scripts/coditect-router"
elif [[ -d "$(pwd)/.coditect" ]]; then
    export CODITECT_ROUTER="$(pwd)/.coditect/scripts/coditect-router"
fi

# Create aliases
if [[ -n "$CODITECT_ROUTER" && -x "$CODITECT_ROUTER" ]]; then
    alias cr='$CODITECT_ROUTER'
    alias cri='$CODITECT_ROUTER -i'
    alias coditect-router='$CODITECT_ROUTER'
fi
# =============================================================================
EOF

# Reload shell configuration
source ~/.zshrc
```

**Verify it works:**
```bash
cr "test"
# Should show command suggestions!
```

**✅ Done!** You can now use `cr` from anywhere. Skip the manual command memorization!

**📖 Full Setup Guide:** [SHELL-SETUP-GUIDE.md](../SHELL-SETUP-GUIDE.md) (includes Bash, troubleshooting, AI mode)

---

## 🚀 STEP 1: Initialize Your First Project (5 minutes)

### 1.1 Run the Initialization Script

```bash
# Download and run initialization script
curl -fsSL https://raw.githubusercontent.com/coditect-ai/coditect-rollout-master/main/scripts/coditect-project-init.sh -o coditect-init.sh
chmod +x coditect-init.sh

# Initialize your project
./coditect-init.sh my-awesome-project your-github-username
```

**What This Does:**
1. Creates `~/PROJECTS/` directory
2. Installs CODITECT framework as `.coditect/` submodule
3. Creates `.claude` symlink for Claude Code
4. Sets up `MEMORY-CONTEXT/` for session persistence
5. Creates your project with complete structure
6. Generates README, CLAUDE.md, PROJECT-PLAN, TASKLIST
7. Initializes git repository

**Result:**
```
~/PROJECTS/
├── .coditect/              ← 49 agents, 189 skills, 72 commands
├── .claude -> .coditect    ← Symlink for Claude Code
├── MEMORY-CONTEXT/         ← Session history
└── my-awesome-project/     ← Your new project
    ├── README.md
    ├── CLAUDE.md
    ├── PROJECT-PLAN.md
    ├── TASKLIST.md
    └── docs/
```

### 1.2 Create GitHub Repository

```bash
# Go to https://github.com/new
# Repository name: my-awesome-project
# Owner: your-github-username
# Privacy: Private (recommended)
# Click "Create repository"

# Push your initial commit
cd ~/PROJECTS/my-awesome-project
git push -u origin main
```

**✅ Checkpoint**: You now have a CODITECT-enabled project!

---

## 🤖 STEP 2: Master Agent Invocation (10 minutes)

### 2.1 Understanding the Framework

**50 Specialized Agents Across 8 Domains:**

| Domain | Key Agents | Use For |
|--------|------------|---------|
| **Research** | competitive-market-analyst, web-search-researcher | Market analysis, pricing research |
| **Code Analysis** | codebase-analyzer, codebase-locator, codebase-pattern-finder | Understanding existing code |
| **Orchestration** | orchestrator, orchestrator-code-review | Multi-agent coordination |
| **Development** | rust-expert-developer, frontend-react-typescript-expert | Implementation |
| **Infrastructure** | cloud-architect, devops-engineer, k8s-statefulset-specialist | Deployment |
| **Testing** | testing-specialist, security-specialist | Quality assurance |
| **Architecture** | senior-architect, software-design-architect | System design |
| **Business** | business-intelligence-analyst, venture-capital-analyst | Strategy |

**View Full Catalog:**
```bash
open ~/PROJECTS/.coditect/AGENT-INDEX.md
```

### 2.2 The ONLY Working Invocation Pattern

**⚠️ CRITICAL: Task Tool Proxy Pattern**

This is the **ONLY verified method** that actually invokes specialized agents:

```python
Task(
    subagent_type="general-purpose",
    prompt="Use [agent-name] subagent to [detailed task description]"
)
```

**❌ WRONG (doesn't work):**
```
"Use competitive-market-analyst to research pricing"
# This just prompts base Claude to pretend to be that agent
```

**✅ CORRECT (actually invokes agent):**
```python
Task(
    subagent_type="general-purpose",
    prompt="Use competitive-market-analyst subagent to research AI IDE pricing strategies including freemium, subscription, and enterprise tiers with competitor analysis"
)
```

### 2.3 Real-World Examples

**Market Research:**
```python
Task(
    subagent_type="general-purpose",
    prompt="Use competitive-market-analyst subagent to analyze the AI coding assistant market, focusing on: (1) competitor pricing models, (2) feature differentiation, (3) target customer segments, (4) positioning strategies"
)
```

**Code Analysis:**
```python
Task(
    subagent_type="general-purpose",
    prompt="Use codebase-analyzer subagent to understand how authentication is implemented in backend/src/auth/, including JWT handling, session management, and middleware integration"
)
```

**Full-Stack Feature:**
```python
Task(
    subagent_type="general-purpose",
    prompt="Use orchestrator subagent to implement user profile editing feature:

    Phase 1: Backend API (rust-expert-developer)
    Phase 2: Frontend UI (frontend-react-typescript-expert)
    Phase 3: Testing (testing-specialist)
    Phase 4: Documentation (qa-reviewer)

    Token budget: 60K, Checkpoints after each phase"
)
```

**✅ Checkpoint**: You can now invoke agents correctly!

---

## 📊 STEP 3: Business Discovery Process (5 minutes)

### 3.1 The 8 Essential Business Documents

Every CODITECT project follows this discovery framework:

```
docs/
├── research/
│   ├── 01-market-research.md          ← TAM/SAM/SOM, industry trends
│   └── 03-customer-discovery.md       ← Interview findings, pain points
├── product/
│   └── 02-product-scope.md            ← MVP definition, features
├── strategy/
│   ├── 04-competitive-analysis.md     ← Competitors, differentiation
│   ├── 05-value-proposition.md        ← Positioning statement
│   ├── 06-product-market-fit-plan.md  ← 7-Fit validation
│   ├── 07-pricing-strategy.md         ← Pricing model, rationale
│   └── 08-go-to-market-strategy.md    ← GTM motion, acquisition
└── executive-summary.md               ← One-page overview
```

### 3.2 Quick Discovery Workflow

**Start with Your Idea:**
```
My Idea: "A SaaS platform for team project management with
real-time collaboration, task tracking, and analytics"
```

**Use Orchestrator to Generate Documents:**
```python
Task(
    subagent_type="general-purpose",
    prompt="Use orchestrator subagent to conduct business discovery for my project idea:

    'A SaaS platform for team project management with real-time collaboration'

    Phase 1: Market research (TAM/SAM/SOM)
    Phase 2: Customer discovery (ICP, pain points)
    Phase 3: Competitive analysis
    Phase 4: Value proposition and pricing
    Phase 5: GTM strategy

    Generate all 8 business documents in docs/ directory"
)
```

**Review Templates:**
```bash
# All templates are in your project already
ls -la ~/PROJECTS/my-awesome-project/docs/
```

**✅ Checkpoint**: You understand the business discovery process!

---

## 🧠 STEP 4: Context Management (5 minutes)

### 4.1 The Catastrophic Forgetting Problem

**Problem:** AI assistants forget everything between sessions.

**Solution:** MEMORY-CONTEXT system

### 4.2 Session Workflow

**At Session Start:**
```bash
cd ~/PROJECTS/my-awesome-project

# Review last session
cat ~/PROJECTS/MEMORY-CONTEXT/sessions/2025-11-XX-SESSION-01.md

# Tell Claude what to remember
"I'm continuing work on [PROJECT]. Review the last session summary
to understand where we left off. Today's focus: [SPECIFIC GOALS]"
```

**During Session:**
- Work on tasks with agents
- Make progress

**At Session End:**
```bash
# Export conversation (in Claude Code)
/export 2025-11-15-EXPORT-CONTEXT-MY-PROJECT.txt
mv 2025-11-15-EXPORT-CONTEXT-MY-PROJECT.txt ~/PROJECTS/MEMORY-CONTEXT/sessions/

# Create summary
cat > ~/PROJECTS/MEMORY-CONTEXT/sessions/2025-11-15-SESSION-02.md << 'EOF'
# Session Summary - 2025-11-15

**Duration**: 2 hours
**Phase**: Business Discovery

## Accomplished
- Completed market research (TAM: $13.5B)
- Conducted 5 customer interviews
- Defined ICP: Mid-market SaaS companies

## Key Decisions
- Pricing: Freemium + $49/mo Pro tier
- GTM: Product-led growth (PLG)

## Next Session
- Design architecture (C4 diagrams)
- Technology stack selection
EOF
```

### 4.3 MEMORY-CONTEXT Directory Structure

```
~/PROJECTS/MEMORY-CONTEXT/
├── sessions/
│   ├── 2025-11-15-SESSION-01.md       ← Session summaries
│   ├── 2025-11-15-SESSION-02.md
│   └── 2025-11-15-EXPORT-CONTEXT-*.txt ← Full exports
├── decisions/
│   └── ADR-001-technology-stack.md    ← Architecture decisions
├── business/
│   └── customer-interview-notes.md    ← Business research
└── technical/
    └── architecture-evolution.md      ← Technical context
```

**Best Practices:**
- ✅ Export after every significant session
- ✅ Write brief summaries (5-10 bullet points)
- ✅ Document key decisions immediately
- ✅ Review before starting new session
- ❌ Don't commit to git (it's gitignored)

**✅ Checkpoint**: You can maintain context across sessions!

---

## 📍 STEP 4.5: Creating Project Checkpoints (3 minutes) - **NEW!**

### What Are Checkpoints?

Checkpoints are automated progress snapshots that capture:
- ✅ Git status and recent commits
- ✅ Submodule states (if using)
- ✅ Completed tasks from TASKLISTs
- ✅ Changed files summary
- ✅ Session context export

**Why Use Checkpoints:**
- Track progress across work sessions
- Never lose work (automatically backed up to GitHub)
- Resume work seamlessly
- Share progress with team/stakeholders

### Creating a Checkpoint (One Command)

```bash
# Automated checkpoint with automatic push to remote
python3 .coditect/scripts/create-checkpoint.py "Sprint description" --auto-push
```

**What This Does:**
1. Generates checkpoint document in `MEMORY-CONTEXT/checkpoints/`
2. Updates README.md with checkpoint reference
3. Creates session export for context continuity
4. Commits all changes locally
5. **Pushes to GitHub remote** (both submodule and master repo)
6. Updates parent repository submodule pointer

**Example:**
```bash
# After completing business discovery phase
cd ~/PROJECTS/my-awesome-project

python3 .coditect/scripts/create-checkpoint.py "Business Discovery Complete: Market Research, Value Prop, and GTM Strategy" --auto-push

# Output:
# ✅ Created checkpoint: MEMORY-CONTEXT/checkpoints/2025-11-16T14-30-00Z-Business-Discovery-Complete.md
# ✅ Updated README.md with checkpoint reference
# ✅ Created MEMORY-CONTEXT session export
# ✅ Committed checkpoint to git
# ✅ Pushed changes to remote (current repository)
# ✅ Pushed submodule update to parent repository
#
# 🎉 CHECKPOINT COMPLETE - All work backed up to GitHub!
```

### Checkpoint Flags

**`--auto-commit` (local only):**
```bash
# Commits changes locally but doesn't push to remote
python3 .coditect/scripts/create-checkpoint.py "Sprint description" --auto-commit
```

**`--auto-push` (recommended):**
```bash
# Commits AND pushes to remote - ensures work is backed up
python3 .coditect/scripts/create-checkpoint.py "Sprint description" --auto-push
```

**Manual (no flags):**
```bash
# Just creates checkpoint files, you commit/push manually
python3 .coditect/scripts/create-checkpoint.py "Sprint description"

# Then manually:
git add MEMORY-CONTEXT/ README.md
git commit -m "Create checkpoint: Sprint description"
git push
```

### When to Create Checkpoints

**Recommended Checkpoint Schedule:**
- ✅ After completing each major phase (business discovery, architecture design, etc.)
- ✅ End of each work session (before closing Claude Code)
- ✅ After significant milestones (first API endpoint, database schema complete)
- ✅ Before making major changes (architecture refactor, framework upgrade)
- ✅ When switching focus areas (backend → frontend, coding → documentation)

**Pro Tip:** Use `--auto-push` so your work is always backed up to GitHub!

### Viewing Checkpoints

**List all checkpoints:**
```bash
ls -lt MEMORY-CONTEXT/checkpoints/
# Shows checkpoints sorted by newest first
```

**Read a checkpoint:**
```bash
cat MEMORY-CONTEXT/checkpoints/2025-11-16T14-30-00Z-Business-Discovery-Complete.md
# Full details: git status, completed tasks, file changes, next steps
```

**Checkpoints in README.md:**
```bash
# Your README.md now has a "Recent Checkpoints" section
cat README.md | grep -A 10 "Recent Checkpoints"
```

### Checkpoint Example Output

When you run the checkpoint script with `--auto-push`, you'll see:

```
================================================================================
CODITECT Checkpoint Creation System
================================================================================

📋 Sprint: Business Discovery Complete
🕐 Timestamp: 2025-11-16T14-30-00Z
🚀 Auto-Push: Enabled (will commit and push)

Step 1: Generating checkpoint document...
✅ Created checkpoint: MEMORY-CONTEXT/checkpoints/2025-11-16T14-30-00Z-Business-Discovery-Complete.md

Step 2: Updating README.md...
✅ Updated README.md with checkpoint reference

Step 3: Creating MEMORY-CONTEXT session export...
✅ Created MEMORY-CONTEXT session export: MEMORY-CONTEXT/sessions/2025-11-16-Business-Discovery-Complete.md

Step 4: Committing changes to git...
✅ Committed checkpoint to git

Step 5: Pushing changes to remote...
Pushing changes to remote...
✅ Pushed changes to remote (current repository)

Detected submodule - updating parent repository...
✅ Pushed submodule update to parent repository

================================================================================
✅ CHECKPOINT CREATION COMPLETE
================================================================================

Checkpoint: MEMORY-CONTEXT/checkpoints/2025-11-16T14-30-00Z-Business-Discovery-Complete.md
Reference: README.md (Recent Checkpoints section)
Context Export: MEMORY-CONTEXT/sessions/

Next session can load this checkpoint for context continuity.

================================================================================
```

**✅ Checkpoint**: You can create automated progress snapshots that backup to GitHub!

---

## 🎓 STEP 5: Common Workflows (Quick Reference)

### Market Research
```python
Task(subagent_type="general-purpose",
     prompt="Use competitive-market-analyst subagent to [research task]")
```

### Code Understanding
```python
# Find files
Task(subagent_type="general-purpose",
     prompt="Use codebase-locator subagent to find all [feature] files")

# Understand implementation
Task(subagent_type="general-purpose",
     prompt="Use codebase-analyzer subagent to analyze [component]")

# Find patterns
Task(subagent_type="general-purpose",
     prompt="Use codebase-pattern-finder subagent to extract [usage examples]")
```

### Multi-Agent Coordination
```python
Task(subagent_type="general-purpose",
     prompt="Use orchestrator subagent to coordinate [complex multi-phase task]")
```

### Commands (Shortcuts)
```bash
/create_plan "Implement user authentication"   # Generate project plan
/research_codebase "authentication system"     # Systematic code research
/security_audit                                # Security vulnerability scan
/ci_commit                                     # Create conventional commit
```

---

## 🚀 You're Ready! Start Building

### Your 30-Minute Onboarding Checklist

- [x] Initialized CODITECT project
- [x] Understand 50 specialized agents
- [x] Master Task tool invocation pattern
- [x] Know the 8 business discovery documents
- [x] Set up MEMORY-CONTEXT for session continuity
- [x] Have quick reference for common workflows

### Next Steps

**Day 1: Business Discovery**
```bash
cd ~/PROJECTS/my-awesome-project

# Start Claude Code
claude

# Begin business discovery
Task(subagent_type="general-purpose",
     prompt="Use orchestrator subagent to conduct complete business discovery for my project: [DESCRIBE YOUR IDEA]")
```

**Day 2-3: Architecture Design**
```python
Task(subagent_type="general-purpose",
     prompt="Use senior-architect subagent to design system architecture with C4 diagrams based on business requirements in docs/")
```

**Day 4+: Implementation**
```python
Task(subagent_type="general-purpose",
     prompt="Use orchestrator subagent to implement MVP with backend, frontend, testing, and deployment")
```

---

## 📚 Additional Resources

### Essential Documentation
- **Agent Catalog**: `~/PROJECTS/.coditect/AGENT-INDEX.md`
- **Business Frameworks**: `~/PROJECTS/.coditect/AZ1.AI-CODITECT-1-2-3-QUICKSTART.md`
- **Architecture Guide**: `~/PROJECTS/.coditect/C4-ARCHITECTURE-METHODOLOGY.md`
- **Platform Roadmap**: `~/PROJECTS/.coditect/PLATFORM-EVOLUTION-ROADMAP.md`

### Quick Reference Cards

**Agent Selection:**
- Market research → `competitive-market-analyst`
- Find code → `codebase-locator`
- Understand code → `codebase-analyzer`
- Complex multi-step → `orchestrator`
- Backend dev → `rust-expert-developer`
- Frontend dev → `frontend-react-typescript-expert`
- Testing → `testing-specialist`
- Security → `security-specialist`

**File Locations:**
```
~/PROJECTS/
├── .coditect/                  ← Framework (49 agents, 189 skills, 72 commands)
├── .claude -> .coditect        ← Symlink
├── MEMORY-CONTEXT/             ← Session history
└── [your-project]/
    ├── README.md               ← Project overview
    ├── CLAUDE.md               ← AI agent config
    ├── PROJECT-PLAN.md         ← Project plan
    ├── TASKLIST.md             ← Task tracking
    └── docs/                   ← Business & technical docs
```

**Common Commands:**
```bash
# View agents
open ~/PROJECTS/.coditect/AGENT-INDEX.md

# Check for reusable work
python ~/PROJECTS/.coditect/scripts/core/smart_task_executor.py

# Session export (in Claude Code)
/export [filename].txt

# Create plan
/create_plan "[task description]"

# Research codebase
/research_codebase "[component name]"
```

---

## ⚠️ Common Mistakes to Avoid

**❌ Don't use direct natural language for agents:**
```
"Use competitive-market-analyst to research pricing"  # Doesn't work!
```

**✅ Always use Task tool:**
```python
Task(subagent_type="general-purpose",
     prompt="Use competitive-market-analyst subagent to research pricing")
```

**❌ Don't skip session exports:**
You'll lose context and have to start over.

**✅ Export at end of every session:**
```bash
/export 2025-XX-XX-SESSION-NAME.txt
# Create summary in MEMORY-CONTEXT/sessions/
```

**❌ Don't use single agent for everything:**
```python
# Wrong - one agent can't do multi-domain work well
Task(subagent_type="general-purpose",
     prompt="Use codebase-analyzer subagent to research market, design architecture, and implement backend")
```

**✅ Use orchestrator for multi-domain:**
```python
Task(subagent_type="general-purpose",
     prompt="Use orchestrator subagent to coordinate market research, architecture design, and implementation")
```

---

## 🎯 Success Criteria

**You're a CODITECT-Enabled AI Operator when you can:**

- ✅ Initialize new projects in <5 minutes
- ✅ Invoke any of the 49 agents correctly
- ✅ Coordinate multi-agent workflows for complex tasks
- ✅ Maintain context across multi-day projects
- ✅ Generate all business discovery documents
- ✅ Design architecture with C4 diagrams
- ✅ Implement features with specialized developers
- ✅ Deploy production-ready software

**Skill Levels:**

**Level 1: Beginner (Days 1-7)**
- Single agent invocation
- Basic commands
- Simple session management

**Level 2: Intermediate (Weeks 2-4)**
- Multi-agent coordination
- Complex workflows
- Work reuse optimization

**Level 3: Advanced (Months 2-3)**
- Custom workflow design
- Framework extension
- Team training

**Level 4: Expert (Months 4+)**
- Enterprise orchestration
- Framework contribution
- Autonomous system implementation

---

## 🚀 Start Your First Project Now!

```bash
# 1. Initialize project
./coditect-init.sh my-saas-platform your-github-username

# 2. Create GitHub repo
# Go to https://github.com/new

# 3. Push initial commit
cd ~/PROJECTS/my-saas-platform
git push -u origin main

# 4. Start Claude Code
claude

# 5. Begin business discovery
Task(subagent_type="general-purpose",
     prompt="Use orchestrator subagent to conduct complete business discovery for my SaaS platform idea: [DESCRIBE YOUR IDEA IN DETAIL]")

# 6. Export at end of session
/export 2025-XX-XX-MY-FIRST-SESSION.txt
```

**You're ready to build production software with AI! 🎉**

---

## 📞 Support & Community

**Documentation:** https://github.com/coditect-ai/coditect-core
**Issues:** https://github.com/coditect-ai/coditect-core/issues
**Framework Version:** CODITECT v1.0 (78% Complete)

**Roadmap to 100% Autonomy:** 8-week plan documented in `.coditect/ORCHESTRATOR-PROJECT-PLAN.md`

---

**Built with CODITECT**
*Master AI-Powered Development in 30 Minutes*

**Last Updated**: 2025-11-15
**Next Review**: Weekly updates as framework evolves

---

## Appendix: Business Discovery Frameworks (Quick Reference)

### 7-Fit Product-Market Fit

1. **Problem-Solution Fit**: Does solution solve the problem?
2. **Solution-Market Fit**: Is there a market for this?
3. **Product-Channel Fit**: Can you reach customers efficiently?
4. **Channel-Model Fit**: Does distribution support business model?
5. **Model-Market Fit**: Can you acquire customers profitably?
6. **Product-Market Fit**: Do customers love and retain product?
7. **Business-Market Fit**: Can you scale sustainably?

### Market Sizing (TAM/SAM/SOM)

- **TAM**: Total Addressable Market (100% market share)
- **SAM**: Serviceable Addressable Market (your product's reach)
- **SOM**: Serviceable Obtainable Market (realistic Year 1-3)

### Value Proposition Template

```
For [TARGET CUSTOMER]
Who [NEED/OPPORTUNITY]
Our [PRODUCT]
Is a [CATEGORY]
That [KEY BENEFIT]
Unlike [COMPETITOR]
Our product [DIFFERENTIATION]
```

### Ideal Customer Profile (ICP)

**Demographics**: Industry, company size, job titles, geography
**Psychographics**: Pain points, goals, buying triggers
**Behavioral**: Current tools, budget, technical sophistication

### Pricing Models

1. Per-User (Seat-Based)
2. Usage-Based (Consumption)
3. Flat-Rate (Unlimited)
4. Freemium + Paid Tiers
5. Feature-Based Tiers
6. Hybrid (Usage + Seats)

### GTM Strategies

- **PLG** (Product-Led Growth): Self-serve, freemium, viral
- **SLG** (Sales-Led Growth): Outbound, enterprise, custom
- **MLG** (Marketing-Led Growth): Inbound, content, SEO
- **Partner-Led**: Marketplaces, resellers, integrations

**All templates included in your project's `docs/` directory!**
