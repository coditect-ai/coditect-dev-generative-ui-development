# Phase 1: .coditect/.claude Framework

**Status:** ✅ Active Pilot (<5 users)
**Timeline:** Current state
**User Scale:** <5 users
**Deployment:** Local development only

## Overview

Phase 1 is the **CODITECT Core Framework** - a local development framework that provides 50 specialized AI agents, 75 slash commands, and 18+ production skills through a git submodule pattern.

## Key Characteristics

- ✅ **No central server** - purely local framework
- ✅ **Manual setup** - user adds git submodule + symlink
- ✅ **No authentication** - user's own Anthropic API key
- ✅ **No tracking** - no usage analytics or session management
- ❌ **Human-in-the-loop** - agents cannot communicate with each other

## Diagrams

### C1 - System Context Diagram
**File:** `phase1-c1-system-context.mmd`
**Purpose:** Shows how developers interact with the CODITECT framework and external systems

**Key Elements:**
- Developer on local machine
- CODITECT Framework (.coditect/.claude)
- Anthropic Claude API
- GitHub Repository

### C2 - Container Diagram
**File:** `phase1-c2-container.mmd`
**Purpose:** Shows the internal structure of the .coditect directory

**Key Containers:**
1. **agents/** - 50 specialized AI agents
   - Business analysts (competitive-market-analyst, business-intelligence)
   - Code specialists (codebase-analyzer, rust-expert, frontend-react)
   - Cloud/DevOps (cloud-architect, devops-engineer)
   - Quality (testing-specialist, qa-reviewer, security)
2. **skills/** - 18+ automation skills
   - ai-curriculum-development
   - build-deploy-workflow
   - code-editor
   - foundationdb-queries
   - google-cloud-build
   - multi-agent-workflow
   - rust-backend-patterns
3. **commands/** - 75 slash commands
   - /implement, /analyze, /document
   - /strategy, /deliberation, /research
   - /commit, /create_handoff
4. **templates/** - Project initialization templates
5. **user-training/** - 13 comprehensive training documents (55K+ words)
6. **.claude symlink** - Compatibility layer for Claude Code

### C3 - Component Diagram (Agent Execution)
**File:** `phase1-c3-agent-execution.mmd`
**Purpose:** Shows how agents are discovered, dispatched, and executed

**Component Responsibilities:**
- **Task Tool Proxy**: Claude Code integration point
- **Agent Dispatcher**: Routes requests to appropriate specialized agent
- **Prompt Builder**: Constructs agent-specific prompts with context
- **Response Parser**: Extracts structured data from LLM responses

**Agent Categories (50 Total):**
- Orchestrator (1) - Multi-agent coordination
- Analysis Specialists (12) - Code analysis, architecture review
- Locators (4) - File discovery, pattern finding
- Development (8) - Rust, React, full-stack specialists
- Research (6) - Web search, competitive analysis, market research
- Business (3) - Business intelligence, VC analysis, curriculum development
- Cloud/DevOps (6) - Cloud architecture, Kubernetes, GCP, DevOps
- Quality (10) - Testing, QA, security, documentation

## Phase 1 Limitations

❌ **No inter-agent communication** - human must copy/paste between agents
❌ **No central authentication** - each user manages own API keys
❌ **No usage tracking** - no metrics or analytics
❌ **No session persistence** - context lost between sessions (mitigated by MEMORY-CONTEXT system)
❌ **No multi-user coordination** - agents unaware of other users' work
❌ **No automated workflows** - everything requires manual triggering

## Phase 1 Statistics

| Metric | Count |
|--------|-------|
| **AI Agents** | 50 |
| **Slash Commands** | 75 |
| **Production Skills** | 18+ |
| **Automation Scripts** | 21 |
| **Training Documents** | 13 |
| **Training Words** | 55,000+ |
| **Orchestration Modules** | 8 (Python) |
| **Memory Context Messages** | 6,400+ |

## Directory Structure

```
.coditect/
├── agents/                      # 50 specialized AI agents
├── commands/                    # 75 slash commands
├── skills/                      # 18+ production skills
├── orchestration/               # 8 Python orchestration modules
├── scripts/                     # 21 automation scripts
├── user-training/               # 13 training documents (55K+ words)
│   ├── 1-2-3-CODITECT-ONBOARDING-GUIDE.md
│   ├── CODITECT-OPERATOR-TRAINING-SYSTEM.md
│   ├── CODITECT-OPERATOR-ASSESSMENTS.md
│   ├── live-demo-scripts/
│   └── sample-project-templates/
├── MEMORY-CONTEXT/              # Persistent AI context (6,400+ messages)
├── templates/                   # Project templates
├── docs/                        # Architecture and research
├── AGENT-INDEX.md              # Complete agent catalog
├── CLAUDE.md                   # AI agent configuration
└── README.md                   # Project documentation
```

## Symlink Architecture

Every CODITECT project has this symlink pattern:

```
project-root/
├── .coditect/  → submodules/core/coditect-core/
└── .claude/    → .coditect/
```

This enables:
- **Distributed Intelligence** - Full agent access in every submodule
- **Claude Code Compatibility** - Works with official Claude Code tool
- **Autonomous Operation** - Agents can operate at any node in the tree

## Usage Example

```bash
# Clone project with submodules
git clone --recurse-submodules https://github.com/user/my-project.git

# Navigate to project
cd my-project

# Use CODITECT agents via Claude Code
# "Use the rust-expert-developer subagent to implement JWT authentication"

# Use slash commands
/implement user-authentication-feature
/analyze code-quality-review
/document api-documentation
```

## Next Phase

**Phase 2: Full IDE in the Cloud** adds:
- Browser-based access (no local installation)
- Cloud hosting on GKE
- Eclipse Theia IDE with Monaco editor
- Extension marketplace
- Persistent workspace storage

---

**Last Updated:** 2025-11-20
**Maintained By:** AZ1.AI CODITECT Team
