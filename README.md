# CODITECT ROLLOUT MASTER

**Master Orchestration Repository for AZ1.AI CODITECT Platform Rollout**

---

## Overview

This repository orchestrates the complete AZ1.AI CODITECT platform rollout from beta through pilot to full Go-to-Market (GTM), coordinating **46 git submodules** across **8 category folders**.

**Current Phase:** Beta Testing (Active - Nov 12 to Dec 10, 2025)
**Target Launch:** March 11, 2026 (109 days remaining)
**Status:** Production-ready master repository with distributed intelligence architecture

### Key Capabilities

- **Distributed Intelligence:** `.coditect` symlink chain enables autonomous operation at every submodule level
- **Centralized Orchestration:** Single source of truth for all CODITECT platform components
- **Automated Coordination:** Git submodules for seamless multi-repo development
- **AI-First Development:** Designed for autonomous AI agents with human strategic guidance
- **Zero Catastrophic Forgetting:** MEMORY-CONTEXT system preserves session continuity

---

## 📖 Essential Reading

**START HERE (in order):**

1. **[WHAT-IS-CODITECT.md](WHAT-IS-CODITECT.md)** - Distributed intelligence architecture (CRITICAL)
2. **[NAVIGATING DOCUMENTATION](#-navigating-documentation)** - How to find the right documentation
3. **[docs/project-management/PROJECT-PLAN.md](docs/project-management/PROJECT-PLAN.md)** - Complete rollout strategy
4. **[docs/project-management/TASKLIST.md](docs/project-management/TASKLIST.md)** - Checkbox-based progress tracking (530+ tasks)
5. **[CLAUDE.md](CLAUDE.md)** - AI agent coordination and development workflow

**Quick Links:**
- 📊 [Visual Architecture](diagrams/README.md) - 24 C4 diagrams documenting 7-phase evolution
- 🧠 [MEMORY-CONTEXT Architecture](https://github.com/coditect-ai/coditect-labs-learning/blob/main/docs/02-architecture/MEMORY-CONTEXT-ARCHITECTURE.md) - Session continuity system
- 🎓 [Training System](https://github.com/coditect-ai/coditect-core/blob/main/user-training/README.md) - CODITECT Operator certification (55K+ words)

---

## 🗺️ Navigating Documentation

**This repository uses a hierarchical documentation structure** - each major directory has its own `README.md` (for humans) and `CLAUDE.md` (for AI agents) providing directory-specific context.

### Documentation Hierarchy

```
coditect-rollout-master/
├── README.md ⭐ YOU ARE HERE - Master overview and navigation guide
├── CLAUDE.md - AI agent orchestration and workflows
│
├── docs/
│   ├── project-management/
│   │   ├── README.md 📋 - Project planning navigation (8.4KB)
│   │   ├── CLAUDE.md - AI context for planning tasks
│   │   ├── PROJECT-PLAN.md - Complete rollout strategy (72KB)
│   │   └── TASKLIST.md - 530+ tasks with checkboxes (23KB)
│   │
│   ├── adrs/
│   │   ├── README.md 🏛️ - Architecture decisions index (12KB)
│   │   ├── CLAUDE.md - AI context for ADR work
│   │   └── project-intelligence/ - 8 ADRs for Project Intelligence Platform
│   │
│   └── security/
│       ├── README.md 🔒 - Security documentation guide (9.5KB)
│       ├── CLAUDE.md - AI context for security operations
│       └── coditect-google-security-advisories/ - GCP security notifications
│
├── scripts/
│   ├── README.md 🔧 - Automation scripts catalog (13KB)
│   ├── CLAUDE.md - AI context for script execution
│   └── (19 Python + 6 shell scripts)
│
├── diagrams/ - 24 C4 architecture diagrams
├── submodules/ - 46 repositories across 8 categories
└── MEMORY-CONTEXT/ - Session exports and context preservation
```

### Finding the Right Documentation

**For Project Planning & Status:**
→ Start with [docs/project-management/README.md](docs/project-management/README.md)

**For Architecture Decisions:**
→ Start with [docs/adrs/README.md](docs/adrs/README.md)

**For Security Information:**
→ Start with [docs/security/README.md](docs/security/README.md)

**For Automation Scripts:**
→ Start with [scripts/README.md](scripts/README.md)

**For AI Agents:**
→ Read this README.md first, then navigate to relevant subdirectory `CLAUDE.md` for task-specific context

---

## Quick Start

### Clone with All Submodules

```bash
# Clone repository with all 46 submodules
git clone --recurse-submodules https://github.com/coditect-ai/coditect-rollout-master.git

# Or initialize submodules after clone
git submodule update --init --recursive
```

### Directory Structure

```
coditect-rollout-master/
├── .coditect -> submodules/core/coditect-core    # CODITECT brain (distributed intelligence)
├── .claude -> .coditect                          # Claude Code compatibility symlink
├── WHAT-IS-CODITECT.md -> ...                    # Architecture documentation (symlink)
│
├── docs/                                         # Master orchestration documentation
│   ├── project-management/                       # 📋 PROJECT-PLAN.md (72KB), TASKLIST.md (23KB)
│   │   ├── README.md (8.4KB) ⭐                  # Navigation guide for planning docs
│   │   └── CLAUDE.md (5.5KB)                     # AI context for planning tasks
│   │
│   ├── adrs/                                     # 🏛️ Architecture Decision Records
│   │   ├── README.md (12KB) ⭐                   # ADR index and navigation
│   │   ├── CLAUDE.md (5.1KB)                     # AI context for ADR work
│   │   └── project-intelligence/ - 10 ADRs
│   │
│   └── security/                                 # 🔒 GCP security advisories
│       ├── README.md (9.5KB) ⭐                  # Security docs guide
│       ├── CLAUDE.md (5.5KB)                     # AI context for security ops
│       └── coditect-google-security-advisories/
│
├── diagrams/                                     # 24 C4 architecture diagrams
│   ├── phase-1-claude-framework/
│   ├── phase-2-ide-cloud/
│   ├── phase-3-workflow-analyzer/
│   ├── phase-4-license-management/
│   ├── phase-5-marketplace-analytics/
│   ├── phase-6-orchestration/
│   └── phase-7-enterprise-scale/
│
├── scripts/                                      # 🔧 Orchestration automation
│   ├── README.md (13KB) ⭐                       # Scripts catalog and usage
│   ├── CLAUDE.md (6.5KB)                         # AI context for script execution
│   └── (19 Python + 6 shell scripts)
│
├── submodules/                                   # 46 submodules in 8 categories
│   ├── core/       # 3 repos  - Core CODITECT framework
│   ├── cloud/      # 4 repos  - Cloud platform (optional SaaS)
│   ├── dev/        # 10 repos - Developer tools and CLI
│   ├── market/     # 2 repos  - Agent marketplace
│   ├── docs/       # 5 repos  - Documentation sites
│   ├── ops/        # 4 repos  - Operations and distribution
│   ├── gtm/        # 6 repos  - Go-to-market materials
│   └── labs/       # 12 repos - Research and next-generation
│
└── MEMORY-CONTEXT/                               # Session exports and context preservation
    ├── sessions/                                 # Session exports
    ├── checkpoints/                              # Sprint checkpoints
    ├── dedup_state/                              # Message deduplication (7,507+ unique messages)
    └── exports-archive/                          # Archived exports
```

---

## Repository Categories (8 Folders, 46 Submodules)

### core/ - Core Framework (3 repos)

| Repository | Description | Status |
|------------|-------------|--------|
| [coditect-core](submodules/core/coditect-core) | ⭐ Primary product: 49 agents, 81 commands, 26 skills | Active |
| [coditect-core-framework](submodules/core/coditect-core-framework) | Framework utilities and shared code | Active |
| [coditect-core-architecture](submodules/core/coditect-core-architecture) | Architecture docs and ADRs | Active |

### cloud/ - Cloud Platform (4 repos)

| Repository | Description | Status |
|------------|-------------|--------|
| [coditect-cloud-backend](submodules/cloud/coditect-cloud-backend) | FastAPI/Rust backend services | P0 |
| [coditect-cloud-frontend](submodules/cloud/coditect-cloud-frontend) | React TypeScript UI | P0 |
| [coditect-cloud-ide](submodules/cloud/coditect-cloud-ide) | Eclipse Theia cloud IDE | P0 |
| [coditect-cloud-infra](submodules/cloud/coditect-cloud-infra) | Terraform GCP infrastructure | P0 |

### dev/ - Developer Tools (10 repos)

| Repository | Description | Status |
|------------|-------------|--------|
| [coditect-cli](submodules/dev/coditect-cli) | Command-line interface | P0 |
| [coditect-analytics](submodules/dev/coditect-analytics) | Usage analytics and insights | P1 |
| [coditect-automation](submodules/dev/coditect-automation) | AI orchestration engine | P1 |
| [coditect-dev-context](submodules/dev/coditect-dev-context) | Context management system | Active |
| [coditect-dev-intelligence](submodules/dev/coditect-dev-intelligence) | Development intelligence | Active |
| [coditect-dev-pdf](submodules/dev/coditect-dev-pdf) | PDF generation utilities | Active |
| [coditect-dev-audio2text](submodules/dev/coditect-dev-audio2text) | Audio transcription | Active |
| [coditect-dev-qrcode](submodules/dev/coditect-dev-qrcode) | QR code generation | Active |
| [coditect-dev-research](submodules/dev/coditect-dev-research) | Research tools | Active |
| [coditect-dev-validation](submodules/dev/coditect-dev-validation) | Validation utilities | Active |

### market/ - Marketplace (2 repos)

| Repository | Description | Status |
|------------|-------------|--------|
| [coditect-market-agents](submodules/market/coditect-market-agents) | Agent marketplace platform | P1 |
| [coditect-market-activity](submodules/market/coditect-market-activity) | Community activity feed | Active |

### docs/ - Documentation (5 repos)

| Repository | Description | Status |
|------------|-------------|--------|
| [coditect-docs-main](submodules/docs/coditect-docs-main) | Docusaurus documentation site | P0 |
| [coditect-docs-blog](submodules/docs/coditect-docs-blog) | Blog and thought leadership | Active |
| [coditect-docs-training](submodules/docs/coditect-docs-training) | Training course materials | Active |
| [coditect-docs-setup](submodules/docs/coditect-docs-setup) | Setup and installation guides | Active |
| [coditect-legal](submodules/docs/coditect-legal) | Legal documents | P0 |

### ops/ - Operations (4 repos)

| Repository | Description | Status |
|------------|-------------|--------|
| [coditect-ops-distribution](submodules/ops/coditect-ops-distribution) | Cross-platform installer/updater | Active |
| [coditect-ops-license](submodules/ops/coditect-ops-license) | License validation system | Active |
| [coditect-ops-projects](submodules/ops/coditect-ops-projects) | Project orchestration tools | Active |
| [coditect-ops-compliance](submodules/ops/coditect-ops-compliance) | Compliance automation | Active |

### gtm/ - Go-to-Market (6 repos)

| Repository | Description | Status |
|------------|-------------|--------|
| [coditect-gtm-strategy](submodules/gtm/coditect-gtm-strategy) | GTM strategy and planning | Active |
| [coditect-gtm-legitimacy](submodules/gtm/coditect-gtm-legitimacy) | Social proof and credibility | Active |
| [coditect-gtm-comms](submodules/gtm/coditect-gtm-comms) | Marketing communications | Active |
| [coditect-gtm-crm](submodules/gtm/coditect-gtm-crm) | HubSpot CRM integration | Active |
| [coditect-gtm-personas](submodules/gtm/coditect-gtm-personas) | User persona research | Active |
| [coditect-gtm-customer-clipora](submodules/gtm/coditect-gtm-customer-clipora) | Customer success platform | Active |

### labs/ - Research & Next-Generation (12 repos)

| Repository | Description | Status |
|------------|-------------|--------|
| [coditect-labs-agent-standards](submodules/labs/coditect-labs-agent-standards) | Agent development standards | Active |
| [coditect-labs-agents-research](submodules/labs/coditect-labs-agents-research) | Multi-agent system research | Active |
| [coditect-labs-claude-research](submodules/labs/coditect-labs-claude-research) | Claude integration experiments | Active |
| [coditect-labs-workflow](submodules/labs/coditect-labs-workflow) | Workflow analysis and patterns | Active |
| [coditect-labs-screenshot](submodules/labs/coditect-labs-screenshot) | Screenshot automation | Active |
| [coditect-labs-v4-archive](submodules/labs/coditect-labs-v4-archive) | V4 codebase archive | Archive |
| [coditect-labs-multi-agent-rag](submodules/labs/coditect-labs-multi-agent-rag) | RAG system research | Active |
| [coditect-labs-cli-web-arch](submodules/labs/coditect-labs-cli-web-arch) | CLI/Web architecture | Active |
| [coditect-labs-first-principles](submodules/labs/coditect-labs-first-principles) | First principles analysis | Active |
| [coditect-labs-learning](submodules/labs/coditect-labs-learning) | Learning experiments | Active |
| [coditect-labs-mcp-auth](submodules/labs/coditect-labs-mcp-auth) | MCP authentication | Active |
| [coditect-next-generation](submodules/labs/coditect-next-generation) | ⭐ Autonomous Platform (Next-Gen) | Active |

---

## Documentation Structure

### Master Planning & Orchestration

**📋 [docs/project-management/](docs/project-management/)** - Master planning and task tracking
- **[README.md](docs/project-management/README.md)** (8.4KB) - Navigation guide for planning documentation
- **[CLAUDE.md](docs/project-management/CLAUDE.md)** (5.5KB) - AI agent context for planning tasks
- **[PROJECT-PLAN.md](docs/project-management/PROJECT-PLAN.md)** (72KB) - Complete rollout strategy (Beta → Pilot → GTM)
- **[TASKLIST.md](docs/project-management/TASKLIST.md)** (23KB) - 530+ tasks with checkbox tracking
- **Organization Reports:** Comprehensive audits, cleanup summaries, reorganization status
- **Timeline Visualizations:** JSON data + interactive HTML Gantt charts

**📖 Quick Guide:**
- Current status: Read PROJECT-PLAN.md Executive Summary
- Active tasks: Check TASKLIST.md for ⚡ ACTIVE phase
- Timeline: Open PROJECT-TIMELINE-INTERACTIVE.html in browser
- Details: Review README.md for complete documentation inventory

---

### Architecture Decision Records

**🏛️ [docs/adrs/](docs/adrs/)** - Architecture decisions documentation
- **[README.md](docs/adrs/README.md)** (12KB) - ADR index and navigation guide
- **[CLAUDE.md](docs/adrs/CLAUDE.md)** (5.1KB) - AI agent context for ADR-related work
- **project-intelligence/** - 10 ADRs documenting Project Intelligence Platform
  - ADR-001 through ADR-008: Technology choices (Git, PostgreSQL, ChromaDB, FastAPI, React, GCP)
  - ADR-COMPLIANCE-REPORT.md: Cross-ADR validation and consistency check

**📖 Quick Guide:**
- Technology stack: Review ADRs 002, 003, 005, 006, 007
- Multi-tenancy: ADR-004 (schema-based approach)
- Access control: ADR-008 (RBAC)
- Data source: ADR-001 (Git as source of truth)

---

### Security Documentation

**🔒 [docs/security/](docs/security/)** - Security advisories and compliance
- **[README.md](docs/security/README.md)** (9.5KB) - Security documentation guide
- **[CLAUDE.md](docs/security/CLAUDE.md)** (5.5KB) - AI agent context for security operations
- **coditect-google-security-advisories/** - GCP security notifications
  - container-contract.html (300KB): GCP Cloud Run security requirements
  - Security advisory exports from GCP Security Command Center

**📖 Quick Guide:**
- Container security: Review container-contract.html
- Recent advisories: Check coditect-google-security-advisories/
- Best practices: See README.md security checklist
- Incident response: Follow security incident workflow in README.md

---

### Automation Scripts

**🔧 [scripts/](scripts/)** - Orchestration automation and utilities
- **[README.md](scripts/README.md)** (13KB) - Complete scripts catalog and usage guide
- **[CLAUDE.md](scripts/CLAUDE.md)** (6.5KB) - AI agent context for script execution
- **19 Python scripts + 6 shell scripts** organized by category:
  - Project initialization and setup
  - Git and submodule operations
  - Timeline and documentation generation
  - MEMORY-CONTEXT management
  - Reporting and status

**📖 Quick Guide:**
- Submodule sync: Use `sync-all-submodules.sh` (never raw git commands)
- Timeline generation: Run `generate-enhanced-timeline.py` after PROJECT-PLAN updates
- New projects: Execute `coditect-project-init.sh` with interactive prompts
- Script safety: Review CLAUDE.md for critical constraints

---

### Visual Architecture

**📊 [diagrams/](diagrams/)** - 24 C4 Model architecture diagrams

**Complete C4 Model architecture** documenting evolution from Phase 1 (local framework) through Phase 7 (enterprise scale).

**[📂 View All Diagrams](diagrams/README.md)** | **[📈 Master Timeline](diagrams/mermaid-source/master-gantt-timeline.mmd)**

#### Quick Access by Phase

| Phase | Status | Focus | Diagrams |
|-------|--------|-------|----------|
| **[Phase 1](diagrams/phase-1-claude-framework/)** | ✅ Active | .claude Framework (Local) | [C1](diagrams/phase-1-claude-framework/phase1-c1-system-context.md) · [C2](diagrams/phase-1-claude-framework/phase1-c2-container.md) · [C3](diagrams/phase-1-claude-framework/phase1-c3-agent-execution.md) |
| **[Phase 2](diagrams/phase-2-ide-cloud/)** | ✅ Deployed | IDE in Cloud (coditect.ai) | [C1](diagrams/phase-2-ide-cloud/phase2-c1-system-context.md) · [C2](diagrams/phase-2-ide-cloud/phase2-c2-container.md) · [C3](diagrams/phase-2-ide-cloud/phase2-c3-theia-ide.md) |
| **[Phase 3](diagrams/phase-3-workflow-analyzer/)** | ✅ Deployed | Workflow Analyzer | [C1](diagrams/phase-3-workflow-analyzer/phase3-c1-system-context.md) · [C2](diagrams/phase-3-workflow-analyzer/phase3-c2-container.md) · [C3](diagrams/phase-3-workflow-analyzer/phase3-c3-orchestration.md) |
| **[Phase 4](diagrams/phase-4-license-management/)** | 🔨 In Dev | License/User/Session Mgmt | [C1](diagrams/phase-4-license-management/phase4-c1-system-context.md) · [C2](diagrams/phase-4-license-management/phase4-c2-container.md) · [C3×3](diagrams/phase-4-license-management/) |
| **[Phase 5](diagrams/phase-5-marketplace-analytics/)** | 📋 Planned | Marketplace & Analytics | [C1](diagrams/phase-5-marketplace-analytics/phase5-c1-system-context.md) · [C2×2](diagrams/phase-5-marketplace-analytics/) |
| **[Phase 6](diagrams/phase-6-orchestration/)** | 📋 Planned | Multi-Agent Orchestration | [C1](diagrams/phase-6-orchestration/phase6-c1-system-context.md) · [C2](diagrams/phase-6-orchestration/phase6-c2-infrastructure.md) · [C3](diagrams/phase-6-orchestration/phase6-c3-inter-agent-communication.md) |
| **[Phase 7](diagrams/phase-7-enterprise-scale/)** | 📋 Planned | Enterprise Scale & Self-Service | [C1](diagrams/phase-7-enterprise-scale/phase7-c1-system-context.md) · [C2](diagrams/phase-7-enterprise-scale/phase7-c2-self-service.md) · [C3×2](diagrams/phase-7-enterprise-scale/) |

**Total:** 24 comprehensive diagram docs | **Methodology:** C4 Model (Context → Container → Component)

---

### Submodule Documentation

**Each of the 46 submodules contains:**
- **PROJECT-PLAN.md** - Submodule-specific implementation plan
- **TASKLIST.md** - Submodule-specific progress tracking
- **README.md** - User-facing overview
- **CLAUDE.md** - AI agent guidelines (in most submodules)

---

## Rollout Phases

### Phase 0: Foundation & Architecture ✅ COMPLETE

**Duration:** Aug 27 - Nov 16, 2025 (completed 2 weeks ahead of schedule)

**Deliverables:**
- ✅ WHAT-IS-CODITECT.md (Distributed intelligence architecture)
- ✅ 24 C4 architecture diagrams (7 phases documented)
- ✅ MEMORY-CONTEXT architecture (zero catastrophic forgetting)
- ✅ Training system (55K+ words, 13 modules)
- ✅ All repository documentation updated
- ✅ Scientific foundation (NESTED LEARNING integration)

### Phase 1: Beta Testing ⚡ ACTIVE

**Duration:** Nov 12 - Dec 10, 2025 (4 weeks)
**Current Status:** Week 2 of 4
**Target:** 50-100 beta users

**Development Status:**
- ✅ Backend (12w) - Complete
- ✅ Frontend (10w) - Complete
- ✅ CLI Tools (8w) - Complete
- ✅ Documentation (6w) - Complete
- ✅ Infrastructure (8w) - Complete
- ✅ Legal (4w) - Complete
- 🔨 Marketplace (10w) - In progress (Week 5)
- 🔨 Analytics (6w) - In progress (Week 3)

**Beta Activities:**
- ✅ Beta Prep (1w) - Complete
- ⚡ Beta Testing (4w) - **ACTIVE NOW** (Week 2)
- 📅 Beta Analysis (1w) - Scheduled Dec 10

### Phase 2: Pilot Program 📅 SCHEDULED

**Duration:** Dec 17, 2025 - Feb 18, 2026 (9 weeks)
**Target:** 100-500 pilot users

**Timeline:**
- Pilot Onboarding (1w) - Dec 17, 2025
- Pilot Phase 1 (4w) - Dec 24, 2025 - Jan 21, 2026 (100-200 users)
- Pilot Phase 2 (4w) - Jan 21 - Feb 18, 2026 (200-500 users)
- Pilot Analysis (1w) - Feb 18, 2026

**Success Criteria:**
- 300+ active pilot users by Phase 2 end
- 80%+ user satisfaction maintained
- Enterprise use cases validated
- Pricing model confirmed

### Phase 3: GTM & Public Launch 🎯 TARGET

**Duration:** Feb 25 - Apr 8, 2026 (6 weeks)
**Target Launch:** March 11, 2026 (109 days remaining)

**Activities:**
- GTM Preparation (2w) - Feb 25, 2026
- **Public Launch** - March 11, 2026
- Post-Launch Support (4w) - March 12, 2026
- Marketing campaigns and sales enablement
- Customer onboarding and support scaling

---

## Current Status

**Phase:** Beta Testing (Active - Week 2 of 4)
**Next Milestone:** Beta Analysis - December 10, 2025
**Submodules:** 46 repositories across 8 categories
**Documentation:** 456K+ words comprehensive
**Root Organization:** Production-ready (100/100 standards)
**Budget:** $2.566M total investment (through Month 12)

### Recent Checkpoints

- **[2025-11-22]** [Documentation Rewrite Complete](CHECKPOINTS/) - CLAUDE.md + README.md follow Anthropic best practices
- **[2025-11-16]** [TASKLISTs Updated and Checkpoint System Complete](CHECKPOINTS/2025-11-16T09-26-41Z-TASKLISTs-Updated-and-Checkpoint-Automation-System-Complete.md)
- **[2025-11-16]** [Phase 0 Architecture Documentation Complete](CHECKPOINTS/2025-11-16T08-34-53Z-DISTRIBUTED-INTELLIGENCE-ARCHITECTURE-COMPLETE.md)

**Create new checkpoint:**
```bash
python3 .coditect/scripts/create-checkpoint.py "Your sprint description" --auto-commit
```

---

## Development Workflow

### Work on Submodule

```bash
# Navigate to submodule
cd submodules/cloud/coditect-cloud-backend

# Make changes, commit, push
git checkout main
git pull
git add .
git commit -m "feat: Add authentication"
git push

# Return to master and update pointer
cd ../../..
git add submodules/cloud/coditect-cloud-backend
git commit -m "Update cloud backend: Add authentication"
git push
```

### Sync All Submodules

```bash
# Update all submodules to latest
git submodule update --remote --merge

# Commit pointer updates
git add submodules/
git commit -m "Sync all submodules to latest"
git push
```

### Create Checkpoint

```bash
# After completing significant work
python3 .coditect/scripts/create-checkpoint.py "Sprint description" --auto-commit
```

---

## Technology Stack

**Backend:** FastAPI (Python), Rust (Actix-web), PostgreSQL, Redis, FoundationDB
**Frontend:** React, TypeScript, Next.js, Docusaurus
**Infrastructure:** Google Cloud Platform, Terraform, Docker, Kubernetes (GKE), Cloud Run
**AI/ML:** Anthropic Claude, LangChain, ClickHouse (analytics)
**CI/CD:** GitHub Actions

---

## Distributed Intelligence Architecture

This repository demonstrates CODITECT's core capability: **distributed intelligence via symlink chains**.

### How It Works

```
coditect-rollout-master/
├── .coditect -> submodules/core/coditect-core    # Master brain
│   ├── agents/      # 49 AI agents
│   ├── commands/    # 81 slash commands
│   └── skills/      # 26 production skills
├── .claude -> .coditect                          # Claude Code compatibility
│
├── submodules/
│   └── cloud/
│       └── coditect-cloud-backend/
│           ├── .coditect -> ../../../.coditect   # Intelligent node
│           └── .claude -> .coditect              # Claude Code access
```

**Every submodule becomes intelligent** - capable of autonomous operation with full access to the CODITECT framework.

**📖 Learn More:** [WHAT-IS-CODITECT.md](WHAT-IS-CODITECT.md) - Complete architecture guide

---

## Contributing

See [CLAUDE.md](CLAUDE.md) for AI agent coordination guidelines and development workflow.

For humans:
1. Read master planning documents in [docs/project-management/](docs/project-management/)
2. Follow git submodule workflow in [CLAUDE.md](CLAUDE.md)
3. Update [TASKLIST.md](docs/project-management/TASKLIST.md) with progress
4. Create checkpoint after completing work

---

## License

Copyright © 2025 AZ1.AI INC. All Rights Reserved.

**PROPRIETARY AND CONFIDENTIAL** - This repository contains AZ1.AI INC. trade secrets and confidential information. Unauthorized copying, transfer, or use is strictly prohibited.

---

**Last Updated:** 2025-11-22
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
**Owner:** AZ1.AI INC
**Lead:** Hal Casteel, Founder/CEO/CTO

*Built with Excellence by AZ1.AI CODITECT*
*Systematic Development. Continuous Context. Exceptional Results.*
