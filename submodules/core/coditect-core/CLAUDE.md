# CLAUDE.md - CODITECT Agentic System Integration

## 🔗 Symlink Architecture

**IMPORTANT:** `.claude` IS `.coditect` via symlinks!
- `.coditect/.claude -> .coditect` (self-reference)  
- `.coditect/.coditect -> ../../.coditect` (parent reference)

All CODITECT components are **directly accessible** in this `.claude` directory.

## 📋 CODITECT Framework Components

This directory structure provides comprehensive agentic development framework with:
- **52 Specialized Agents** (⭐ 2 new project creation agents Nov 22)
  - Project discovery, structure optimization, and lifecycle management
  - Research, analysis, and competitive intelligence
  - Full-stack development and infrastructure specialists
  - Quality assurance, security, and compliance
- **81 Slash Commands** (⭐ 4 new commands Nov 22)
  - `/new-project` - Complete project creation workflow
  - `/analyze-hooks` - Assess hooks implementation readiness
  - `/web-search-hooks` - Research hooks best practices and patterns
  - `/generate-project-plan-hooks` - Create hooks implementation roadmap
  - Project creation, management, and planning
  - Development, testing, and deployment workflows
  - Analysis, research, and architecture commands
- **26 Production Skills** (254+ reusable assets)
  - Project and submodule management (5 new Nov 21)
  - Framework patterns, production patterns, backend patterns
  - Documentation, workflow, and CI/CD automation
- **21 Python Scripts** for automation (4 new submodule scripts Nov 21)
- **Memory & Context System** for session preservation (7,507+ unique messages)

## Project Overview

**CODITECT** is a comprehensive project management and development framework designed to transform ideas into production-ready products systematically. This repository contains:

1. **AZ1.AI CODITECT Framework v1.0** - Project initialization and management system
2. **Universal Agent Framework v2.0** - Cross-platform agent framework (in development)
3. **Educational Curriculum Framework** - AI-powered educational content development (legacy)
4. **CODITECT Operator Training System** - Comprehensive training program for users

## 🎓 User Training System (NEW!)

**Complete training program located in `user-training/` directory.**

For detailed training context, see: [user-training/CLAUDE.md](user-training/CLAUDE.md)

**Quick Overview:**
- **30-minute Quick Start** - Immediate productivity for experienced developers
- **4-6 hour Comprehensive Training** - Full certification path
- **13 Core Documents** - 55,000+ words of training materials
- **Live Demo Scripts** - Step-by-step orchestrated demonstrations
- **Sample Templates** - Real-world examples and quality benchmarks
- **Assessments & Certification** - Verify capability, not just knowledge

**Training covers:**
- Environment setup and framework initialization
- Task Tool Pattern mastery (critical for agent invocation)
- Business discovery (market research, value proposition, PMF, GTM, pricing)
- Technical specification (C4 architecture, database design, API specs, ADRs)
- Project management (PROJECT-PLAN, TASKLIST, checkpoints)
- Advanced operations (session management, multi-session continuity)

**For users new to CODITECT:** Start with `user-training/README.md`

## 🚀 Slash Command Quick Start (NEW!)

**Essential guide for mastering CODITECT's 78 slash commands and 52 agents.**

See: **[1-2-3-SLASH-COMMAND-QUICK-START.md](1-2-3-SLASH-COMMAND-QUICK-START.md)**

### 🆕 New Project Creation Workflow

**Create complete, production-ready projects in one command:**

```bash
# Unified project creation command
/new-project "Build an API for managing team projects"

# Automatically executes:
# 1. Project Discovery - Interactive interview with requirement gathering
# 2. Submodule Creation - Git infrastructure setup
# 3. Project Planning - Generate PROJECT-PLAN.md and TASKLIST.md
# 4. Structure Optimization - Production-ready directory structure
# 5. Quality Assurance - Verification and team onboarding
```

**Output:** Complete production-ready project with:
- Git repository with CODITECT naming conventions
- Symlink chains for distributed intelligence (.coditect, .claude)
- PROJECT-PLAN.md with complete specification
- TASKLIST.md with checkbox-based tracking
- Production-ready directory structure by project type
- Starter code and templates
- CI/CD workflows (GitHub Actions)
- Docker configuration for local development
- Comprehensive documentation (README, API, deployment guides)
- Test structure with examples

See: **[commands/new-project.md](commands/new-project.md)** for detailed workflow

### 🎣 Claude Code Hooks Implementation Workflow (⭐ NEW Nov 22)

**Complete hooks automation strategy from analysis to production:**

```bash
# Step 1: Analyze CODITECT readiness for hooks
/analyze-hooks

# Step 2: Research industry standards and best practices
/web-search-hooks

# Step 3: Create comprehensive implementation roadmap
/generate-project-plan-hooks
```

**Deliverables:**
- Phase 1: Quick wins (component validation, prompt enhancement)
- Phase 2: Quality automation (git checks, standards validation)
- Phase 3: Advanced features (multi-tool orchestration, optimization)
- Phase 4: Production hardening (monitoring, observability)

**Key Commands:**
- `/analyze-hooks` - Assess CODITECT readiness, identify automatable processes
- `/web-search-hooks` - Research community patterns, security best practices, production strategies
- `/generate-project-plan-hooks` - Create 4-phase implementation roadmap with tasks, resources, risks

**Integration:**
- Hooks automate validation, quality checks, and documentation synchronization
- Reduces manual reviews by 40-60%
- Enables pre-deployment compliance and error prevention
- Seamlessly integrates with existing workflows

See: **[commands/analyze-hooks.md](commands/analyze-hooks.md)**, **[commands/web-search-hooks.md](commands/web-search-hooks.md)**, **[commands/generate-project-plan-hooks.md](commands/generate-project-plan-hooks.md)**, **[docs/HOOKS-COMPREHENSIVE-ANALYSIS.md](docs/HOOKS-COMPREHENSIVE-ANALYSIS.md)** for detailed workflows

### 🤖 AI Command Router (Easiest Way!)

**Never memorize commands again** - just describe what you want:

```bash
# Simple command selection
coditect-router "I need to add user authentication"

# Interactive mode
coditect-router -i

# Quick aliases (add to shell)
alias cr='coditect-router'
alias cri='coditect-router -i'
```

**How it works:**
- Analyzes your plain English request
- Suggests the optimal slash command
- Explains why it's the right choice
- Shows alternatives and next steps
- Works with or without API key (heuristic mode included)

### 3-Step System (Manual Method)

1. **Quick Lookup** - Browse all commands in `docs/SLASH-COMMANDS-REFERENCE.md`
2. **Get Guidance** - Use `/COMMAND-GUIDE`, `/suggest-agent`, or `/agent-dispatcher`
3. **Execute with Confidence** - Follow recommended syntax

**Perfect for:**
- Learning which command to use when
- Getting agent invocation syntax
- Understanding workflow patterns
- Building command muscle memory

**See also:**
- `docs/SLASH-COMMANDS-REFERENCE.md` - Complete command catalog
- `commands/COMMAND-GUIDE.md` - Decision trees and workflows
- `commands/suggest-agent.md` - Agent selection helper
- `commands/agent-dispatcher.md` - Intelligent orchestration
- `scripts/coditect-router` - AI command selection tool

---

## 📋 Project Planning (NEW!)

**Complete project lifecycle documentation:**

- **[PROJECT-PLAN.md](docs/03-project-planning/PROJECT-PLAN.md)** - Comprehensive 62KB project plan
  - Current operational status (78% → 100% roadmap)
  - Implementation roadmap (Phases 1-5, 20 weeks)
  - Multi-agent orchestration strategy
  - Budget & resource requirements ($111K implementation)
  - Success metrics and quality gates

- **[TASKLIST-WITH-CHECKBOXES.md](docs/03-project-planning/TASKLIST-WITH-CHECKBOXES.md)** - 38KB task tracking
  - Phase 0: 350+ completed tasks (✅ 100% operational)
  - Phase 1-5: 180+ pending tasks (⏸️ roadmap)
  - Total: 530+ tasks with checkbox format
  - Progress tracking across all phases

---

# Educational Curriculum Development Framework (Legacy)

## Overview
Comprehensive AI education curriculum development framework with autonomous content generation, multi-level assessment creation, and intelligent work reuse optimization using specialized educational AI agents.

## 🎯 Agent Framework - 52 Specialists (Core Framework)

### Core Educational Agents
- **ai-curriculum-specialist** - Master curriculum development and educational architecture
- **educational-content-generator** - Multi-level content creation with pedagogical frameworks
- **assessment-creation-agent** - Adaptive assessment design with bias detection
- **orchestrator** - Multi-agent coordination for complex educational workflows

### Educational Skills Framework
- **ai-curriculum-development** - Complete educational development automation
- **notebooklm-content-optimization** - AI content formatting and enhancement

### Work Reuse & Token Optimization
- **Work Reuse Optimizer** - Intelligent analysis of 254+ reusable assets
- **Smart Task Executor** - Automated reuse checking with ROI calculation
- **Asset Library Management** - Token savings tracking and adaptation guidance

## ⚡ Agent Invocation Method

### 🛠️ Task Tool Proxy Pattern (VERIFIED WORKING)
**This is the ONLY confirmed working method to invoke specialized agents:**

```python
# Educational content generation
Task(subagent_type="general-purpose", prompt="Use ai-curriculum-specialist subagent to generate Module 1 foundations content across all skill levels")

# Assessment creation
Task(subagent_type="general-purpose", prompt="Use assessment-creation-agent subagent to create adaptive quizzes for neural networks module")

# Complex curriculum workflows with reuse optimization
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate multi-module curriculum development with intelligent work reuse")
```

**Why Use Task Tool:**
- ✅ **Verified Agent Invocation**: Actually calls specialized agents (not just base Claude)
- ✅ **Proper Agent Identification**: Agents respond with their specialized knowledge
- ✅ **Enhanced Capabilities**: Access to agent-specific automation features
- ✅ **Quality Differentiation**: Higher quality, specialized responses vs. general Claude

**⚠️ Direct Natural Language Does NOT Work:**
Simply typing "Use [agent] subagent to [task]" will NOT invoke specialized agents - it just prompts base Claude to respond as if it were that agent.
```

## 📂 Directory Structure
```
.claude/
├── agents/                      # 52 specialized AI agents
├── commands/                    # 81 slash commands
├── skills/                      # 26 production skills (254+ assets)
├── docs/                        # Documentation and research
│   ├── HOOKS-COMPREHENSIVE-ANALYSIS.md
│   └── ... (60+ documentation files)
├── AGENT-INDEX.md              # Complete agent catalog
├── COMPLETE-INVENTORY.md       # All 177 components inventory
├── CLAUDE.md                   # This configuration file
└── README.md                   # Project documentation
```

## 🚀 Quick Start Examples

### Educational Content Development
```python
Task(subagent_type="general-purpose", prompt="Use ai-curriculum-specialist subagent to create beginner-friendly neural networks content with visual analogies")
```

### Assessment Creation
```python
Task(subagent_type="general-purpose", prompt="Use assessment-creation-agent subagent to design adaptive quiz for machine learning fundamentals")
```

### Work Reuse Optimization
```python
# Always check for reusable work first
python scripts/core/smart_task_executor.py
```

### Comprehensive Curriculum Development
```python
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate complete Module 2 development with reuse optimization and quality gates")
```

## 🎯 Intelligent Automation Features

### Smart Context Awareness
- Educational agents auto-detect skill levels and learning objectives
- Intelligent progress reporting with curriculum checkpoints
- Context-aware content adaptation and difficulty scaling
- Seamless integration with existing educational frameworks

### Work Reuse Intelligence
- Automatic scanning of 254+ reusable assets
- ROI-driven reuse recommendations (13.8-27.6x returns)
- Token optimization with up to 100% efficiency gains
- Quality-maintained adaptation strategies

### Enhanced Educational Capabilities
Selected educational agents include advanced automation with:
- Multi-level content generation (beginner through expert)
- Assessment-integrated learning design
- NotebookLM optimization for AI-powered book generation
- Cross-module consistency and progression validation

## 📋 Available Commands
- See [commands/README.md](commands/README.md) for complete command inventory
- `/generate-curriculum-content` - Automated curriculum content generation
- `/optimize-work-reuse` - Intelligent work reuse and token optimization
- `/agent-dispatcher` - Smart agent selection and coordination

## 🔧 Settings & Configuration
- `settings.agents-research.json` - Agent research configuration
- `settings.local.json` - Local environment settings  
- `.claude/settings.local.json` - Additional local configuration

---

## 💡 Best Practices

### For Educational Content Tasks
1. **Always run work reuse check first** using smart_task_executor
2. Use ai-curriculum-specialist for comprehensive curriculum development
3. Use assessment-creation-agent for adaptive evaluations
4. Leverage orchestrator for complex multi-module coordination

### For Content Optimization
1. Apply notebooklm-content-optimization skill for AI-ready formatting
2. Use work_reuse_optimizer to identify adaptation opportunities
3. Implement quality gates for consistency and standards compliance

### For Project Management
1. Use curriculum_project_manager for autonomous project lifecycle
2. Use orchestrator for multi-agent workflow coordination
3. Track progress with persistent state management and checkboxes

---

## 📊 **Project Checkpoint: 2025-11-12**

### **🎯 Major Milestone: Comprehensive Automation Analysis Complete**

**Status Update:** Framework analyzed from automation perspective with complete roadmap to 100% autonomous operation created.

#### **Analysis Deliverables (150K+ words)**

**Implementation Planning:**
- ✅ **ORCHESTRATOR-PROJECT-PLAN.md** - 135+ actionable tasks with checkboxes, time estimates, and acceptance criteria
- ✅ **PROJECT-TIMELINE.md** - Week-by-week Gantt charts showing parallel work streams
- ✅ **EXECUTION-CHECKLIST.md** - Printable checklist for daily progress tracking
- ✅ **PROJECT-PLAN-SUMMARY.md** - Quick reference overview of 8-week implementation

**Architecture & Design:**
- ✅ **AUTONOMOUS-AGENT-SYSTEM-DESIGN.md** - Complete system architecture with working code examples
  - Agent Discovery Service (Redis) - 250 lines of code
  - Message Bus (RabbitMQ) - 300 lines of code
  - Task Queue Manager (Redis + RQ) - 400 lines of code
  - Circuit Breaker Service (PyBreaker) - 150 lines of code
  - Distributed State Manager (S3 + Redis locks) - 300 lines of code
  - Monitoring & Observability (Prometheus/Jaeger/Grafana) - 250 lines of code

**Research & Best Practices:**
- ✅ **docs/MULTI-AGENT-ARCHITECTURE-BEST-PRACTICES.md** - 70K+ word research document
  - LangGraph, CrewAI, AutoGen multi-agent patterns analyzed
  - Temporal, Airflow, Celery orchestration patterns documented
  - Circuit breaker, retry logic, and resilience patterns
  - Distributed state management strategies (Redis locks, CRDT, event sourcing)
  - OpenTelemetry observability patterns with code examples
  - 30+ complete Python code examples ready to use

**Gap Analysis:**
- ✅ **CLAUDE-AUTOMATION-GAP-ANALYSIS.md** (in parent repo) - 32K word comprehensive analysis
  - 10 critical gap domains identified
  - Cost-benefit analysis: $100K investment → 29% ROI Year 1, 858% Year 2
  - Risk assessment with mitigation strategies
  - Break-even analysis: Month 9

#### **Key Findings**

**Current Framework Status:**
- **Completion:** 78% (7/9 core orchestration modules operational, 2,864 lines production code)
- **Agent Count:** 49 specialized agents across 8 domains
- **Skills:** 18 production skills catalogued
- **Commands:** 72 slash commands available
- **Scripts:** 21 Python automation scripts

**Critical Gap (#1 Blocker):**
**No inter-agent communication** - Agents cannot send tasks to each other, making system fundamentally human-in-the-loop.

**Current Reality:**
```
User → Orchestrator → "Use agent-X subagent" → Human copies/pastes → Agent X executes
                                ↑
                    Human intervention required!
```

**Target State:**
```
User → Orchestrator → Agent A → Agent B → Agent C → Result (all automatic)
```

**The 3 Must-Haves to Achieve Autonomy:**
1. **Message Bus (RabbitMQ)** - Inter-agent task passing with priority queues
2. **Agent Discovery Service (Redis)** - Capability-based agent discovery and load balancing
3. **Task Queue Manager (Redis + RQ)** - Persistent queue with dependency resolution and automatic unblocking

#### **8-Week Implementation Roadmap**

**Phase 1: Foundation (Weeks 1-2) - P0**
- Goal: Core infrastructure for autonomous operation
- Tasks: 45 tasks, 96 hours
- Deliverables: Message Bus, Agent Discovery, Task Queue, Unit Tests
- Success: First autonomous agent-to-agent task delegation works

**Phase 2: Resilience (Weeks 3-4) - P0**
- Goal: Error handling and recovery
- Tasks: 38 tasks, 80 hours
- Deliverables: Circuit Breaker, Retry Engine, Distributed State, Integration Tests
- Success: System recovers automatically from failures

**Phase 3: Observability (Weeks 5-6) - P1**
- Goal: Complete visibility into system behavior
- Tasks: 32 tasks, 80 hours
- Deliverables: Prometheus metrics, Jaeger tracing, Loki logs, Grafana dashboards
- Success: Full observability stack operational

**Phase 4: Polish (Weeks 7-8) - P1/P2**
- Goal: Production readiness
- Tasks: 20 tasks, 64 hours
- Deliverables: CLI integration, API docs, Docker/K8s deployment, Load testing
- Success: System handles 100+ concurrent tasks

**Total:** 135+ tasks, 320 engineering hours over 8 weeks

#### **Success Metrics (Target State)**

| Metric | Current | Target | Impact |
|--------|---------|--------|--------|
| **Autonomy** | 0% | 95% | Eliminate human-in-the-loop |
| **Latency** | N/A | <5s | Task dispatch speed |
| **Throughput** | 1/min | 100/min | 100x improvement |
| **Reliability** | N/A | 99.9% | Production-grade uptime |
| **Recovery Time** | N/A | <60s | Automatic failure recovery |
| **Test Coverage** | 0% | 80%+ | Confidence in changes |
| **Agent Utilization** | N/A | 70% | Efficient resource use |

#### **Business Case**

**Investment Required:**
- Engineering: $100,800 (2 full-stack engineers, 1 DevOps part-time)
- Infrastructure: $1,400 (8 weeks) + $3,600/year (production)
- Total Year 1: $105,800

**Expected Benefits (Annual):**
- Operational efficiency gains: $78,000/year (reduced manual orchestration)
- Faster task completion (60% faster): $50,000/year
- LLM cost reduction (40% via work reuse): $2,400/year
- Total quantified benefits: $130,400+/year

**ROI Analysis:**
- Year 1: 29% ROI (break-even Month 9)
- Year 2: 858% ROI
- 3-Year NPV (10% discount): $257,000

**Recommendation:** **STRONG INVEST** - 95% confidence in achieving full autonomy

#### **Next Steps**

**Immediate Actions (This Week):**
1. ✅ Review ORCHESTRATOR-PROJECT-PLAN.md for detailed task breakdown
2. ⏸️ Present findings to stakeholders for go/no-go decision
3. ⏸️ Allocate 2 full-stack engineers + 1 DevOps engineer (part-time)
4. ⏸️ Provision infrastructure: RabbitMQ, Redis, PostgreSQL, Prometheus, Grafana, Jaeger

**Week 1 (Phase 1 Start):**
1. ⏸️ Setup development environment and GitHub project with milestones
2. ⏸️ Begin Agent Discovery Service implementation (3 days)
3. ⏸️ Daily standups and progress tracking via EXECUTION-CHECKLIST.md
4. ⏸️ First checkpoint: Agent registry working by Day 3

**Week 2-8:**
1. ⏸️ Follow ORCHESTRATOR-PROJECT-PLAN.md week-by-week
2. ⏸️ Check off tasks as completed
3. ⏸️ Weekly sync meetings to review progress
4. ⏸️ Final checkpoint (Week 8): Fully autonomous system operational

#### **Documentation Locations**

**In This Repository (.claude/):**
- `ORCHESTRATOR-PROJECT-PLAN.md` - Complete implementation plan
- `AUTONOMOUS-AGENT-SYSTEM-DESIGN.md` - System architecture
- `PROJECT-TIMELINE.md` - Week-by-week schedule
- `EXECUTION-CHECKLIST.md` - Daily task checklist
- `docs/MULTI-AGENT-ARCHITECTURE-BEST-PRACTICES.md` - Research findings

**In Parent Repository:**
- `CLAUDE-AUTOMATION-GAP-ANALYSIS.md` - Comprehensive gap analysis
- `COMPLETE-AUTOMATION-ANALYSIS-SUMMARY.md` - Master summary document

---

**Status**: Production Ready (78% Complete) → Roadmap to 100% Autonomy Created ✅
**Agent Framework**: 50 agents + 74 commands + 24 skills (254+ assets) operational
**Critical Path Identified**: Message Bus + Agent Discovery + Task Queue = Autonomy
**Implementation Ready**: 135+ tasks with code examples ready for execution
**Project Planning**: PROJECT-PLAN.md (62KB) + TASKLIST-WITH-CHECKBOXES.md (38KB) ✅
**Last Updated**: November 20, 2025
**Next Milestone**: Phase 1 kickoff - Agent Discovery Service implementation
