# 🚀 CODITECT 1-2-3 Slash Command Quick Start

**Learn the CODITECT slash command system in 3 simple steps.**

---

## 📖 Table of Contents

1. [The 3-Step System](#the-3-step-system)
2. [🤖 AI Router - The Easiest Way](#-ai-router---the-easiest-way-start-here)
3. [Step 1: Quick Lookup](#step-1-quick-lookup)
4. [Step 2: Get Guidance](#step-2-get-guidance)
5. [Step 3: Execute with Confidence](#step-3-execute-with-confidence)
6. [Common Scenarios](#common-scenarios)
7. [Quick Reference Card](#quick-reference-card)

---

## The 3-Step System

CODITECT provides **72 slash commands** and **49 specialized agents**. Here's how to always know which one to use:

```
┌─────────────────────────────────────────────────┐
│  🤖 AI ROUTER (EASIEST - START HERE!)         │
│  Just describe what you want in plain English  │
│  └─ coditect-router "your request"            │
└─────────────────────────────────────────────────┘
              ↓ (Or use manual lookup)
┌─────────────────────────────────────────────────┐
│  STEP 1: QUICK LOOKUP                          │
│  Know what you need? → Reference guide         │
│  └─ docs/SLASH-COMMANDS-REFERENCE.md          │
└─────────────────────────────────────────────────┘
              ↓ (If unsure)
┌─────────────────────────────────────────────────┐
│  STEP 2: GET GUIDANCE                          │
│  Need help choosing? → Ask the system          │
│  └─ /COMMAND-GUIDE, /suggest-agent             │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  STEP 3: EXECUTE WITH CONFIDENCE               │
│  Run the recommended command/agent             │
│  └─ Follow the provided syntax                 │
└─────────────────────────────────────────────────┘
```

---

## 🤖 AI Router - The Easiest Way (Start Here!)

### What It Is
**AI-powered command selection** that analyzes your plain English request and tells you exactly which slash command to use.

### When to Use
- ✅ **Recommended for beginners** - No need to memorize 72 commands
- ✅ **When you're unsure** which command is right
- ✅ **To avoid mistakes** and use the optimal command every time
- ✅ **For complex requests** that might need multiple commands

### How to Use

**Basic Usage:**
```bash
# From anywhere in your project
coditect-router "I need to add user authentication"

# Interactive mode (recommended)
coditect-router -i
```

**Example Output:**
```
🤖 CODITECT AI Command Router
======================================================================

📍 RECOMMENDED COMMAND: /implement
   Description: Production-ready implementation mode
   Purpose: Build production code with error handling

💭 REASONING:
   Your request involves implementing a new feature (authentication)
   which requires production-quality code with security best practices.

🔄 ALTERNATIVES:
   • /prototype: If you just need a quick proof-of-concept first
   • /feature_development: For full end-to-end feature workflow

📋 NEXT STEPS:
   1. Use /implement to build authentication system
   2. Include error handling and security hardening
   3. Follow up with /test_generate for comprehensive tests

💻 USAGE:
   Type in Claude Code: /implement
```

### Two Modes

**1. Heuristic Mode** (Default - No Setup Required)
- Works immediately without any API key
- Uses intelligent keyword pattern matching
- Fast and reliable for common scenarios

**2. AI-Powered Mode** (Recommended for Best Results)
- Set environment variable: `export ANTHROPIC_API_KEY="your-key"`
- Uses Claude AI to deeply understand your request
- Handles complex, nuanced scenarios
- Provides detailed reasoning

### Quick Setup in Claude Code

Add to your shell (bash/zsh):
```bash
# Add to ~/.bashrc or ~/.zshrc
alias cr='coditect-router'
alias cri='coditect-router -i'

# Now you can just type:
cr "fix bug in payment system"
cri  # Interactive mode
```

---

## Step 1: Quick Lookup

### When to Use
- ✅ You know what category of work you're doing
- ✅ You want to see all available commands
- ✅ You need a quick reference

### Where to Look
**File:** `docs/SLASH-COMMANDS-REFERENCE.md`

### What You'll Find
**72 commands organized by category:**

| Category | Example Commands |
|----------|------------------|
| **Planning & Strategy** | `/deliberation`, `/strategy`, `/create_plan` |
| **Implementation** | `/implement`, `/action`, `/prototype` |
| **Code Review** | `/analyze`, `/ai_review`, `/full_review` |
| **Testing & Quality** | `/test_generate`, `/tdd_cycle`, `/security_sast` |
| **Documentation** | `/document`, `/doc_generate` |
| **Research** | `/research`, `/research_codebase`, `/multi-agent-research` |
| **Database** | `/db_migrations`, `/db-performance-analyzer` |
| **DevOps** | `/monitor_setup`, `/slo_implement` |
| **Git/Version Control** | `/commit`, `/describe_pr`, `/pr_enhance` |
| **Session Management** | `/context_save`, `/create_handoff`, `/resume_handoff` |

### Example Usage
```bash
# 1. Open the reference
cat .coditect/docs/SLASH-COMMANDS-REFERENCE.md

# 2. Find your category (e.g., "Implementation")
# 3. Pick the right command
/implement user-authentication-feature
```

---

## Step 2: Get Guidance

### When to Use
- ❓ Unsure which command fits your task
- ❓ Complex multi-step workflow
- ❓ Need agent invocation syntax

### Option A: Command Decision Tree
**Command:** `/COMMAND-GUIDE`

**Shows you:**
```
What do you want to do?
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
│  └─ Execute existing plan → /implement_plan
│
├─ Review/Analyze something?
│  ├─ Code quality review → /analyze
│  └─ Debug issues → /debug
```

**Plus workflow patterns:**
- Full Feature Development (8 steps)
- Quick Feature (3 steps)
- Bug Fix (3 steps)
- Performance Work (3 steps)

### Option B: Agent Selection Helper
**Command:** `/suggest-agent [what you want to do]`

**Example:**
```bash
# Input
/suggest-agent "optimize database queries"

# Output
"Use the foundationdb-expert subagent to analyze and optimize
database performance including query patterns and schema efficiency"

# Then copy-paste and execute the suggestion
```

### Option C: Intelligent Dispatcher
**Command:** `/agent-dispatcher [detailed request]`

**Example:**
```bash
/agent-dispatcher "implement user authentication with tests and documentation"

# Returns:
- Primary recommendation with full syntax
- Alternative approaches
- Multi-agent coordination if needed
- Reasoning for selection
```

---

## Step 3: Execute with Confidence

### After Getting Guidance

#### For Slash Commands
```bash
# Direct execution
/implement feature-name

# Or with arguments
/research verify-api-availability
```

#### For Agent Invocations
```bash
# Copy the exact syntax from /suggest-agent or /agent-dispatcher
"Use the rust-expert-developer subagent to implement JWT authentication with refresh tokens"

# Agent executes with specialized knowledge
```

#### For Multi-Step Workflows
```bash
# Follow the pattern from /COMMAND-GUIDE

# Example: Full Feature Development
1. /deliberation "analyze user profile editing requirements"
2. /research "verify React state management patterns"
3. /implement "user profile editing feature"
4. /analyze "review profile editing implementation"
5. /document "create API documentation for profile endpoints"
6. /commit "add user profile editing feature"
```

---

## Common Scenarios

### Scenario 1: "I Need to Implement a New Feature"

**❓ Unsure where to start?**
```bash
# Step 1: Get guidance
/COMMAND-GUIDE

# Step 2: Follow "Pattern 1: Full Feature Development"
1. /deliberation
2. /research
3. /implement
4. /analyze
5. /document
6. /commit
```

**✅ Know the pattern?**
```bash
# Jump straight to implementation
/implement user-profile-editing
```

---

### Scenario 2: "I Need to Fix a Bug"

**❓ Complex bug requiring investigation?**
```bash
# Step 1: Understand the issue
/debug authentication-token-expiration

# Step 2: Implement fix
/implement fix-jwt-expiration-bug

# Step 3: Commit
/commit
```

**✅ Simple fix?**
```bash
# Direct fix
/implement fix-typo-in-validation
/commit
```

---

### Scenario 3: "I Need to Research Competitors"

**❓ Need the right agent?**
```bash
# Step 1: Get agent syntax
/suggest-agent "research AI IDE pricing strategies"

# Step 2: Use the suggested invocation
"Use the competitive-market-analyst subagent to research AI IDE
pricing strategies and compare with our positioning"
```

**✅ Know the agent?**
```bash
# Direct invocation
"Use the competitive-market-analyst subagent to analyze competitor
feature sets and pricing models"
```

---

### Scenario 4: "I Need to Optimize Performance"

**❓ Not sure which area?**
```bash
# Step 1: Analyze first
/analyze identify-performance-bottlenecks

# Step 2: Optimize specific area
/optimize database-query-performance

# Step 3: Commit
/commit
```

**✅ Know the bottleneck?**
```bash
# Direct optimization
/optimize database-indexes
/commit
```

---

### Scenario 5: "I Need to Review Code"

**Quick lookup:**
```bash
# Check reference guide for review commands
# Options: /analyze, /ai_review, /full_review, /local_review

# Production code review
/analyze comprehensive-quality-review

# Multi-dimensional review
/full_review orchestrate-all-review-agents
```

---

### Scenario 6: "I'm Starting a New Project"

```bash
# Step 1: Business discovery
"Use the competitive-market-analyst subagent to research market
opportunity and competitive landscape"

# Step 2: Technical planning
/strategy "design system architecture with C4 diagrams"

# Step 3: Create implementation plan
/create_plan "development roadmap with milestones"

# Step 4: Begin development
/implement "core features based on plan"
```

---

## Quick Reference Card

### 🎯 Decision Tree (1-Minute)

```
I need to...
│
├─ Know all commands? → docs/SLASH-COMMANDS-REFERENCE.md
├─ Choose a command? → /COMMAND-GUIDE
├─ Get agent syntax? → /suggest-agent [task]
└─ Complex workflow? → /agent-dispatcher [request]
```

---

### 📚 Most Common Commands

**Planning:**
- `/deliberation` - Pure planning, no code
- `/strategy` - Architecture and system design
- `/create_plan` - Implementation planning

**Development:**
- `/implement` - Production-ready code
- `/prototype` - Quick proof-of-concept
- `/action` - Autonomous implementation mode

**Quality:**
- `/analyze` - Code review with rubrics
- `/test_generate` - Generate tests
- `/debug` - Debug issues

**Documentation:**
- `/document` - Generate docs
- `/describe_pr` - PR descriptions

**Git:**
- `/commit` - Create commits
- `/create_worktree` - Git worktree management

**Session:**
- `/create_handoff` - End session handoff
- `/resume_handoff` - Resume from handoff

---

### 🤖 Most Common Agents

**Research:**
- `competitive-market-analyst` - Market research
- `web-search-researcher` - External information
- `codebase-analyzer` - Understand code

**Development:**
- `rust-expert-developer` - Rust backend
- `frontend-react-typescript-expert` - React frontend
- `orchestrator` - Multi-step coordination

**Infrastructure:**
- `foundationdb-expert` - Database design
- `cloud-architect` - Deployment and CI/CD

**Quality:**
- `testing-specialist` - Test coverage
- `security-specialist` - Security audits
- `qa-reviewer` - Documentation review

---

### 💡 Pro Tips

1. **Start Simple**
   - Use reference guide for quick lookups
   - Learn patterns gradually

2. **When Unsure**
   - `/COMMAND-GUIDE` for workflows
   - `/suggest-agent` for agent syntax

3. **Complex Tasks**
   - Use `/agent-dispatcher` for orchestration
   - Follow workflow patterns from guide

4. **Build Muscle Memory**
   - Common pattern: `/deliberation` → `/research` → `/implement`
   - Review pattern: `/analyze` → fix → `/commit`

5. **Save Time**
   - Bookmark `SLASH-COMMANDS-REFERENCE.md`
   - Keep `/COMMAND-GUIDE` handy
   - Use `/suggest-agent` liberally

---

## 🎓 Learning Path

### Day 1: Quick Start (30 minutes)
1. ✅ Read this guide
2. ✅ Browse `SLASH-COMMANDS-REFERENCE.md`
3. ✅ Try `/COMMAND-GUIDE`
4. ✅ Execute one simple command: `/implement hello-world`

### Week 1: Build Confidence (2-3 hours)
1. ✅ Use `/suggest-agent` for 3 different tasks
2. ✅ Complete one full feature workflow
3. ✅ Practice `/deliberation` → `/implement` → `/commit`
4. ✅ Try agent invocation with "Use the [agent] subagent..."

### Month 1: Master the System (ongoing)
1. ✅ Learn all workflow patterns from `/COMMAND-GUIDE`
2. ✅ Use `/agent-dispatcher` for complex tasks
3. ✅ Memorize your top 10 most-used commands
4. ✅ Explore specialized agents for your domain

---

## 📖 Additional Resources

**Core Documentation:**
- `docs/SLASH-COMMANDS-REFERENCE.md` - All 72 commands with descriptions
- `commands/COMMAND-GUIDE.md` - Detailed decision trees and workflows
- `commands/agent-dispatcher.md` - Agent selection logic
- `commands/suggest-agent.md` - Agent syntax generator
- `AGENT-INDEX.md` - Complete agent catalog (49 agents)

**Training Materials:**
- `user-training/README.md` - Comprehensive training program
- `user-training/CLAUDE.md` - Training context for AI assistants
- `AZ1.AI-CODITECT-1-2-3-QUICKSTART.md` - Framework initialization guide

**Architecture:**
- `WHAT-IS-CODITECT.md` - Distributed intelligence architecture
- `C4-ARCHITECTURE-METHODOLOGY.md` - C4 diagram methodology

---

## 🆘 Need Help?

### If you're stuck:

1. **Check the reference guide**
   ```bash
   cat .coditect/docs/SLASH-COMMANDS-REFERENCE.md
   ```

2. **Ask for guidance**
   ```bash
   /COMMAND-GUIDE
   /suggest-agent "describe your task"
   /agent-dispatcher "detailed request"
   ```

3. **Search the documentation**
   ```bash
   grep -r "your-topic" .coditect/docs/
   grep -r "your-topic" .coditect/commands/
   ```

4. **Start simple and iterate**
   - Begin with basic commands
   - Add complexity as needed
   - Learn from the output

---

## 🎯 The Golden Rule

> **"When in doubt, ask the system!"**

```bash
# Any of these will guide you:
/COMMAND-GUIDE
/suggest-agent [what you want]
/agent-dispatcher [detailed request]

# The CODITECT framework is self-documenting
# You're never more than one command away from the answer
```

---

## 🚀 Ready to Start?

**Your first command:**
```bash
# Try this right now:
/suggest-agent "create a simple REST API endpoint"

# Then execute what it suggests
# That's it - you're using CODITECT! 🎉
```

---

**Last Updated:** 2025-11-16
**Version:** 1.0
**Part of:** CODITECT Framework Core
**Repository:** https://github.com/coditect-ai/coditect-core
