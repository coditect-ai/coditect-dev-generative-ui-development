# CODITECT Rollout Master - Claude Code Configuration

## Project Overview

**CODITECT Rollout Master** is the master orchestration repository for the complete AZ1.AI CODITECT platform rollout, coordinating 42 submodules across 8 categories through git submodules using distributed intelligence architecture.

### Purpose
- **Distributed Intelligence:** `.coditect` symlink chain enables autonomous operation at every submodule level
- **Centralized Orchestration:** Single source of truth for all CODITECT platform components
- **Automated Coordination:** Multi-repo development with intelligent agents at every node
- **AI-First Development:** Autonomous agent orchestration with human-in-the-loop guidance
- **Phased Rollout:** Beta → Pilot → Full GTM with training and certification

### Essential Reading
Before working on this project, understand the architecture:
- 📖 **[WHAT-IS-CODITECT.md](https://github.com/coditect-ai/coditect-core/blob/main/WHAT-IS-CODITECT.md)** - Distributed intelligence architecture
- 🎓 **[Training System](https://github.com/coditect-ai/coditect-core/blob/main/user-training/README.md)** - CODITECT Operator training
- 📘 **[AZ1.AI-CODITECT-VISION-AND-STRATEGY.md](AZ1.AI-CODITECT-VISION-AND-STRATEGY.md)** - Complete vision
- 📂 **[REPO-NAMING-CONVENTION.md](docs/REPO-NAMING-CONVENTION.md)** - Repository naming rules for 8 categories
- 🚀 **[1-2-3-SLASH-COMMAND-QUICK-START.md](.coditect/1-2-3-SLASH-COMMAND-QUICK-START.md)** - Master all 72 commands in 3 steps
- 🤖 **AI Command Router** (`coditect-router`) - Never memorize commands, just describe what you want in plain English!

---

## Architecture

### Master Repository Structure (Distributed Intelligence)

```
coditect-rollout-master/
├── .coditect -> submodules/core/coditect-core    # CODITECT brain
│   ├── agents/                     # 49 specialized AI agents
│   ├── skills/                     # 18 production skills
│   ├── commands/                   # 72 slash commands
│   ├── user-training/              # Training materials (55K+ words)
│   └── WHAT-IS-CODITECT.md         # Architecture documentation
│
├── .claude -> .coditect            # Claude Code compatibility symlink
│
├── docs/                           # Master planning documents
│   ├── REPO-NAMING-CONVENTION.md   # Repository naming rules
│   ├── CODITECT-MASTER-ORCHESTRATION-PLAN.md
│   ├── CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md
│   └── ... (60+ planning documents)
│
├── submodules/                     # 42 sub-projects in 8 category folders
│   ├── core/                       # 3 repos - Core framework
│   │   ├── coditect-core/
│   │   ├── coditect-core-framework/
│   │   └── coditect-core-architecture/
│   ├── cloud/                      # 4 repos - Cloud platform
│   │   ├── coditect-cloud-backend/
│   │   │   ├── .coditect -> ../../../.coditect   # Intelligent node
│   │   │   └── .claude -> .coditect              # Claude Code access
│   │   ├── coditect-cloud-frontend/
│   │   ├── coditect-cloud-ide/
│   │   └── coditect-cloud-infra/
│   ├── dev/                        # 9 repos - Developer tools
│   ├── market/                     # 2 repos - Marketplace
│   ├── docs/                       # 5 repos - Documentation
│   ├── ops/                        # 3 repos - Operations
│   ├── gtm/                        # 6 repos - Go-to-market
│   └── labs/                       # 12 repos - Research & Next-Gen
│       ├── coditect-labs-agent-standards/
│       ├── coditect-labs-agents-research/
│       ├── ... (9 more labs repos)
│       └── coditect-next-generation/  # ⭐ Autonomous Platform (NEW Nov 22)
│           ├── .coditect -> ../../../.coditect  # Distributed intelligence
│           └── .claude -> .coditect             # Claude Code access
│
├── scripts/                        # Automation scripts
├── templates/                      # Project templates
├── MEMORY-CONTEXT/                 # Persistent context for AI agents
├── .gitmodules                     # Submodule configuration
├── README.md                       # User-facing documentation
└── CLAUDE.md                       # This file - AI agent configuration
```

**Key Pattern:** Every submodule has `.coditect -> ../../../.coditect` symlink enabling intelligent autonomous operation at every level. See [WHAT-IS-CODITECT.md](https://github.com/coditect-ai/coditect-core/blob/main/WHAT-IS-CODITECT.md) for complete architecture details.

**Repository Naming:** All repos follow `coditect-{category}-{name}` convention. See [docs/REPO-NAMING-CONVENTION.md](docs/REPO-NAMING-CONVENTION.md) for rules.

---

## Submodule Management

### Git Submodule Workflow

**Initial Setup:**
```bash
# Clone with all submodules
git clone --recurse-submodules https://github.com/coditect-ai/coditect-rollout-master.git

# Or initialize submodules after clone
git submodule update --init --recursive
```

**Working with Submodules:**
```bash
# Update all submodules to latest
git submodule update --remote --merge

# Update specific submodule
git submodule update --remote --merge submodules/coditect-cloud-backend

# Commit submodule reference changes
git add submodules/coditect-cloud-backend
git commit -m "Update cloud backend to latest"
git push
```

**Submodule Development:**
```bash
# Work inside a submodule
cd submodules/coditect-cloud-backend
git checkout main
# Make changes, commit, push
git add .
git commit -m "Add feature X"
git push

# Return to master repo and update reference
cd ../..
git add submodules/coditect-cloud-backend
git commit -m "Update cloud backend submodule reference"
git push
```

---

## Development Workflow

### AI-First Autonomous Development

This repository is designed for **AI agents to autonomously coordinate** multi-project development:

1. **Master Planning** - AI reads docs/ to understand overall vision
2. **Project Coordination** - AI coordinates work across submodules
3. **Context Management** - MEMORY-CONTEXT/ stores persistent AI context
4. **Human Checkpoints** - Strategic approvals at phase gates

### Claude Code Integration

When working in this repository, Claude should:

1. **Read Master Plans First**
   ```bash
   # Start with these documents
   docs/CODITECT-MASTER-ORCHESTRATION-PLAN.md
   docs/CODITECT-ROLLOUT-MASTER-PLAN.md
   ```

2. **Understand Submodule Dependencies**
   - Check .gitmodules for current submodule states
   - Review each submodule's PROJECT-PLAN.md
   - Check TASKLIST.md for current progress

3. **Work Systematically**
   - Work in priority order (P0 first, then P1)
   - Complete one submodule phase before starting next
   - Update master documentation as work progresses

4. **Maintain Context**
   - Store decisions in MEMORY-CONTEXT/
   - Update master plans with learnings
   - Document blockers and resolutions

---

## Key Documents

### Master Planning
- **CODITECT-MASTER-ORCHESTRATION-PLAN.md** - Overall rollout strategy
- **CODITECT-ROLLOUT-MASTER-PLAN.md** - Detailed implementation plan
- **CODITECT-INTEGRATED-ECOSYSTEM-VISION.md** - Long-term vision

### Architecture
- **CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md** - Cloud platform architecture
- **CODITECT-REUSABLE-TOOLS-ARCHITECTURE.md** - Reusable component design

### Per-Submodule
Each submodule contains:
- **PROJECT-PLAN.md** - Detailed project plan
- **TASKLIST.md** - Checkbox-based progress tracking
- **README.md** - User-facing documentation

---

## Rollout Phases

### Phase 0: Foundation & Architecture (Aug-Nov 2025) ✅ COMPLETE
**Goal:** Establish distributed intelligence architecture and documentation

**Deliverables:**
- ✅ WHAT-IS-CODITECT.md (Distributed intelligence architecture)
- ✅ Visual Architecture Diagrams (5 comprehensive Mermaid diagrams)
- ✅ MEMORY-CONTEXT Architecture Documentation
- ✅ Training System (55K+ words, 13 modules)
- ✅ All repository documentation updated
- ✅ Scientific foundation (NESTED LEARNING integration)

**Status:** Completed November 16, 2025 (2 weeks ahead of schedule)

### Phase 1: Beta Testing (Nov 12 - Dec 10, 2025) ⚡ ACTIVE
**Goal:** Internal and limited external user testing (50-100 users)

**Current Status:** Week 2 of 4 (Nov 20, 2025)

**Active Development:**
- ✅ Backend (12w) - Complete
- ✅ Frontend (10w) - Complete
- ✅ CLI Tools (8w) - Complete
- ✅ Documentation (6w) - Complete
- ✅ Infrastructure (8w) - Complete
- ✅ Legal (4w) - Complete
- 🔨 Marketplace (10w) - In progress
- 🔨 Analytics (6w) - In progress

**Beta Testing Activities:**
- ✅ Beta Prep (1w) - Complete
- ⚡ Beta Testing (4w) - ACTIVE NOW (Week 2)
- ⏸️ Beta Analysis (1w) - Scheduled Dec 10

### Phase 2: Pilot Program (Dec 2025 - Feb 2026)
**Goal:** Expanded testing with 100-500 pilot users

**Timeline:**
- ⏸️ Pilot Onboarding (1w) - Dec 17, 2025
- ⏸️ Pilot Phase 1 (4w) - Dec 24, 2025 - Jan 21, 2026 (100-200 users)
- ⏸️ Pilot Phase 2 (4w) - Jan 21 - Feb 18, 2026 (200-500 users)
- ⏸️ Pilot Analysis (1w) - Feb 18, 2026

**Success Criteria:**
- 300+ active pilot users by Phase 2 end
- 80%+ user satisfaction maintained
- Enterprise use cases validated
- Pricing model confirmed

### Phase 3: GTM & Public Launch (Feb-Mar 2026) 🎯
**Goal:** Public launch with marketing, sales, support

**Timeline:**
- ⏸️ GTM Preparation (2w) - Feb 25, 2026
- 🎯 Public Launch - March 11, 2026
- ⏸️ Post-Launch Support (4w) - March 12, 2026

**Activities:**
- Marketing campaigns and sales enablement
- Customer onboarding and support scaling
- 24/7 monitoring and rapid issue resolution
- Continuous improvement based on user feedback

---

## Technology Stack

### Backend
- **FastAPI** - Python web framework
- **PostgreSQL** - Relational database
- **Redis** - Caching and sessions
- **FoundationDB** - Multi-tenant state storage
- **Google Cloud Platform** - Cloud infrastructure

### Frontend
- **React** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Next.js** - React framework (marketplace)
- **Docusaurus** - Documentation site

### Infrastructure
- **Terraform** - Infrastructure as Code
- **Docker** - Containerization
- **Kubernetes** - Container orchestration (GKE)
- **Cloud Run** - Serverless compute
- **GitHub Actions** - CI/CD

### AI/ML
- **Anthropic Claude** - AI agents and orchestration
- **LangChain** - AI framework integration
- **ClickHouse** - Analytics and usage tracking

---

## Code Patterns

### Submodule Commit Pattern

When committing changes across submodules:

```bash
# 1. Work in submodule first
cd submodules/coditect-cloud-backend
git add .
git commit -m "Add feature X"
git push

# 2. Return to master and update reference
cd ../..
git add submodules/coditect-cloud-backend
git commit -m "Update cloud backend: Add feature X"
git push
```

### Multi-Submodule Updates

When updating multiple submodules:

```bash
# Update all submodules to latest
git submodule update --remote --merge

# Review changes
git status

# Commit all submodule reference updates
git add .gitmodules submodules/
git commit -m "Update all submodules to latest

- coditect-cloud-backend: Feature X
- coditect-cloud-frontend: UI update Y
- coditect-docs: Documentation Z
"
git push
```

---

## AI Agent Guidelines

### When Working in This Repository

1. **Always Read Master Plans First**
   - Understand overall vision before making changes
   - Check current rollout phase
   - Verify dependencies between submodules

2. **Work on One Submodule at a Time**
   - Complete logical units of work
   - Don't switch contexts mid-feature
   - Update master docs after major completions

3. **Maintain Context Across Sessions**
   - Use MEMORY-CONTEXT/ for persistent state
   - Document decisions and rationale
   - Track blockers and open questions

4. **Coordinate Across Submodules**
   - Check for breaking changes
   - Update integration points
   - Test cross-submodule functionality

5. **Human Checkpoint Rules**
   - Request approval for:
     - Architecture changes
     - New dependencies
     - Budget increases
     - Timeline extensions
   - Provide clear recommendations with pros/cons

---

## Common Tasks

### Add New Submodule
```bash
git submodule add https://github.com/coditect-ai/new-project.git submodules/new-project
git commit -m "Add new-project submodule"
git push
```

### Remove Submodule
```bash
git submodule deinit -f submodules/old-project
git rm -f submodules/old-project
rm -rf .git/modules/submodules/old-project
git commit -m "Remove old-project submodule"
git push
```

### Update Submodule URL
```bash
# Edit .gitmodules
vim .gitmodules

# Sync changes
git submodule sync
git submodule update --init --recursive

# Commit
git commit -am "Update submodule URLs"
git push
```

---

## Testing Approach

### Integration Testing

Since this coordinates multiple projects, integration testing is critical:

1. **Local Integration Tests**
   - Run all submodule test suites
   - Test cross-submodule APIs
   - Verify deployment scripts

2. **Staging Environment**
   - Deploy all submodules to staging
   - End-to-end user flow testing
   - Performance testing

3. **Production Deployment**
   - Blue-green deployments
   - Gradual rollout (10% → 50% → 100%)
   - Monitor metrics and rollback if needed

---

## Monitoring & Observability

### Metrics to Track

**Development Metrics:**
- Submodule completion percentage
- Open vs closed tasks
- Blockers and resolution time
- Code quality scores

**Platform Metrics:**
- User growth (beta → pilot → GTM)
- API latency and errors
- System uptime
- Cost per user

**Business Metrics:**
- Trial → paid conversion
- Monthly recurring revenue (MRR)
- Customer acquisition cost (CAC)
- Net promoter score (NPS)

---

## Security Considerations

### Secrets Management

**NEVER commit:**
- API keys
- Database credentials
- OAuth secrets
- SSL certificates

**ALWAYS use:**
- Google Cloud Secret Manager
- Environment variables
- Encrypted configuration files
- .gitignore for local secrets

### Access Control

- Each submodule has its own GitHub repo with access control
- Master repo has restricted write access
- CI/CD uses service accounts with minimal permissions
- Production secrets stored in GCP Secret Manager

---

## Current Status

**Project Status:** Beta Testing (Active) - Week 2 of 4 (Nov 20, 2025)

**Master Repository:**
- ✅ 41 submodules configured across 8 categories
- ✅ Distributed intelligence architecture operational
- ✅ Master planning documents complete
- ✅ Phase 0: Foundation complete (Nov 16, 2025)
- ⚡ Phase 1: Beta Testing active (Nov 12 - Dec 10, 2025)

**Development Status:**
- ✅ Backend (12w) - Complete
- ✅ Frontend (10w) - Complete
- ✅ CLI Tools (8w) - Complete
- ✅ Documentation (6w) - Complete
- ✅ Infrastructure (8w) - Complete
- ✅ Legal (4w) - Complete
- 🔨 Marketplace (10w) - In progress (Week 5)
- 🔨 Analytics (6w) - In progress (Week 3)

**Budget:** $2.566M total investment (through Month 12)

**Timeline:** 111 days to public launch (March 11, 2026)

**Next Milestone:** Beta Analysis - December 10, 2025

---

## Future Enhancements

### Short-term (Next 3 months)
- [ ] Automated submodule update notifications
- [ ] Cross-submodule dependency tracking
- [ ] Integrated testing dashboard
- [ ] AI agent coordination improvements

### Medium-term (3-6 months)
- [ ] Automated rollback procedures
- [ ] Multi-environment management (dev/staging/prod)
- [ ] Performance benchmarking suite
- [ ] Customer feedback integration

### Long-term (6-12 months)
- [ ] Multi-region deployment
- [ ] Advanced analytics and ML insights
- [ ] White-label customization
- [ ] Enterprise features (SSO, audit logs)

---

## Support & Troubleshooting

### Common Issues

**Submodule not updating:**
```bash
git submodule update --remote --force
```

**Detached HEAD in submodule:**
```bash
cd submodules/problematic-submodule
git checkout main
git pull
cd ../..
git add submodules/problematic-submodule
git commit -m "Fix detached HEAD"
```

**Merge conflicts in submodule:**
```bash
cd submodules/conflicted-submodule
git pull origin main
# Resolve conflicts
git add .
git commit
git push
cd ../..
git add submodules/conflicted-submodule
git commit -m "Resolve submodule conflicts"
```

---

## Contributing

When contributing to this master repository:

1. Read all master planning documents
2. Understand the current rollout phase
3. Work on assigned submodules
4. Update master docs with progress
5. Request reviews at phase gates
6. Maintain context in MEMORY-CONTEXT/
7. **Create checkpoint after completing work** (see below)

---

## Checkpoint Automation System

### Overview

CODITECT includes an automated checkpoint creation system that:
- ✅ Standardizes checkpoint format (ISO-DATETIME stamped)
- ✅ Captures git status, submodule states, completed tasks
- ✅ Updates README.md with checkpoint reference
- ✅ Creates MEMORY-CONTEXT session export
- ✅ Enables zero catastrophic forgetting between sessions
- ✅ Saves tokens through reusable checkpoint template

### When to Create Checkpoints

Create checkpoints after:
- Completing a sprint (Phase 0, Sprint +1, Sprint +2, etc.)
- Major architectural changes
- Completing multiple submodule updates
- Finishing documentation sprints
- Phase gate completions
- End of development session (for context continuity)

### How to Create Checkpoints

**Single Command:**
```bash
python3 .coditect/scripts/create-checkpoint.py "Sprint description" --auto-commit
```

**Examples:**
```bash
# After architecture sprint
python3 .coditect/scripts/create-checkpoint.py "Architecture Documentation Sprint Complete" --auto-commit

# After MEMORY-CONTEXT implementation
python3 .coditect/scripts/create-checkpoint.py "Sprint +1 MEMORY-CONTEXT Implementation Complete" --auto-commit

# After updating TASKLISTs
python3 .coditect/scripts/create-checkpoint.py "TASKLISTs Updated Across All Submodules" --auto-commit

# Manual commit (without --auto-commit)
python3 .coditect/scripts/create-checkpoint.py "Sprint description"
# Then manually review and commit
```

### What the Script Does

1. **Generates Checkpoint Document** (`CHECKPOINTS/YYYY-MM-DDTHH-MM-SSZ-description.md`)
   - Git status and recent commits
   - Submodule status and latest commits
   - Completed tasks from all TASKLISTs
   - Changed files summary
   - Next steps and Sprint +1 preparation

2. **Updates README.md**
   - Adds checkpoint to "Recent Checkpoints" section
   - Links to checkpoint document
   - Maintains chronological order

3. **Creates MEMORY-CONTEXT Export** (`MEMORY-CONTEXT/sessions/YYYY-MM-DD-description.md`)
   - Session summary
   - Objectives completed
   - Key decisions
   - Work completed reference
   - Next session preparation

4. **Commits Changes** (if --auto-commit flag used)
   - Commits checkpoint, README.md, and MEMORY-CONTEXT export
   - Standardized commit message with metadata

### Benefits for AI Agents

**Context Continuity:**
- Next session starts with complete checkpoint context
- Zero catastrophic forgetting via MEMORY-CONTEXT export
- Clear understanding of what was completed

**Token Efficiency:**
- Reusable checkpoint template (don't recreate format each time)
- Standardized structure saves tokens
- Links to detailed TASKLISTs instead of duplicating

**Informed Decision Making:**
- Historical checkpoints show progression
- Pattern recognition across sprints
- Dependencies and blockers tracked

### Claude Code Integration

When working in this repository:

1. **Start of Session:** Read most recent checkpoint
   ```bash
   # Find most recent checkpoint
   ls -t CHECKPOINTS/ | head -1
   ```

2. **During Work:** Track progress in TASKLISTs
   - Mark completed tasks with `[x]`
   - Add new tasks as discovered
   - Update WIP status

3. **End of Session:** Create checkpoint
   ```bash
   python3 .coditect/scripts/create-checkpoint.py "Session description" --auto-commit
   ```

4. **Next Session:** Load checkpoint context
   - Read most recent checkpoint document
   - Review MEMORY-CONTEXT session export
   - Continue from where previous session ended

### Script Location and Documentation

- **Script:** `.coditect/scripts/create-checkpoint.py` (part of core CODITECT framework)
- **Documentation:** See script header for detailed usage
- **Help:** `python3 .coditect/scripts/create-checkpoint.py --help`
- **Framework Repo:** https://github.com/coditect-ai/coditect-project-dot-claude

---

**Last Updated:** November 20, 2025
**Current Phase:** Beta Testing (Active - Week 2 of 4)
**Next Milestone:** Beta Analysis - December 10, 2025
**Target Launch:** March 11, 2026 (111 days remaining)
**Budget:** $2.566M total investment
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
**Owner:** AZ1.AI INC
**Lead:** Hal Casteel, Founder/CEO/CTO
