# CODITECT Rollout Master - Claude Code Configuration

## Project Overview

**CODITECT Rollout Master** is the master orchestration repository for the complete AZ1.AI CODITECT platform rollout, coordinating 19 sub-projects through git submodules using distributed intelligence architecture.

### Purpose
- **Distributed Intelligence:** `.coditect` symlink chain enables autonomous operation at every submodule level
- **Centralized Orchestration:** Single source of truth for all CODITECT platform components
- **Automated Coordination:** Multi-repo development with intelligent agents at every node
- **AI-First Development:** Autonomous agent orchestration with human-in-the-loop guidance
- **Phased Rollout:** Beta → Pilot → Full GTM with training and certification

### Essential Reading
Before working on this project, understand the architecture:
- 📖 **[WHAT-IS-CODITECT.md](https://github.com/coditect-ai/coditect-project-dot-claude/blob/main/WHAT-IS-CODITECT.md)** - Distributed intelligence architecture
- 🎓 **[Training System](https://github.com/coditect-ai/coditect-project-dot-claude/blob/main/user-training/README.md)** - CODITECT Operator training
- 📘 **[AZ1.AI-CODITECT-VISION-AND-STRATEGY.md](AZ1.AI-CODITECT-VISION-AND-STRATEGY.md)** - Complete vision
- 🚀 **[1-2-3-SLASH-COMMAND-QUICK-START.md](.coditect/1-2-3-SLASH-COMMAND-QUICK-START.md)** (NEW!) - Master all 72 commands in 3 steps

---

## Architecture

### Master Repository Structure (Distributed Intelligence)

```
coditect-rollout-master/
├── .coditect/                      # CODITECT brain (git submodule)
│   ├── agents/                     # 50 specialized AI agents
│   ├── skills/                     # 189 reusable skills
│   ├── commands/                   # 72 slash commands
│   ├── user-training/              # Training materials (240K+ words)
│   ├── WHAT-IS-CODITECT.md        # Architecture documentation
│   ├── README.md                   # Framework documentation
│   └── CLAUDE.md                   # Framework context
│
├── .claude -> .coditect            # Claude Code compatibility symlink
│
├── docs/                           # Master planning documents
│   ├── CODITECT-MASTER-ORCHESTRATION-PLAN.md
│   ├── CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md
│   ├── CODITECT-REUSABLE-TOOLS-ARCHITECTURE.md
│   ├── CODITECT-INTEGRATED-ECOSYSTEM-VISION.md
│   └── CODITECT-ROLLOUT-MASTER-PLAN.md
│
├── submodules/                     # 19 sub-projects (intelligent nodes)
│   ├── coditect-cloud-backend/     # FastAPI backend (P0, 12 weeks)
│   │   ├── .coditect -> ../../.coditect   # Intelligent node
│   │   ├── .claude -> .coditect           # Claude Code access
│   │   └── src/
│   ├── coditect-cloud-frontend/    # React frontend (P0, 10 weeks)
│   │   ├── .coditect -> ../../.coditect
│   │   ├── .claude -> .coditect
│   │   └── src/
│   ├── coditect-cli/               # Python CLI tools (P0, 8 weeks)
│   │   ├── .coditect -> ../../.coditect
│   │   └── .claude -> .coditect
│   └── ... (all submodules follow same pattern)
│
├── scripts/                        # Automation scripts
├── templates/                      # Project templates
├── workflows/                      # GitHub Actions workflows
├── MEMORY-CONTEXT/                 # Persistent context for AI agents
├── .gitmodules                     # Submodule configuration
├── README.md                       # User-facing documentation
└── CLAUDE.md                       # This file - AI agent configuration
```

**Key Pattern:** Every submodule has `.coditect -> ../../.coditect` symlink enabling intelligent autonomous operation at every level. See [WHAT-IS-CODITECT.md](https://github.com/coditect-ai/coditect-project-dot-claude/blob/main/WHAT-IS-CODITECT.md) for complete architecture details.

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

### Phase 1: Beta (Weeks 1-16)
**Goal:** Functional CODITECT platform for internal testing

**P0 Projects:**
- ✅ coditect-framework (Ongoing - already operational)
- ⏸️ coditect-cloud-backend (12 weeks)
- ⏸️ coditect-cloud-frontend (10 weeks)
- ⏸️ coditect-cli (8 weeks)
- ⏸️ coditect-docs (6 weeks)
- ⏸️ coditect-infrastructure (8 weeks)
- ⏸️ coditect-legal (4 weeks)

### Phase 2: Pilot (Weeks 17-28)
**Goal:** Limited external user testing (50-100 users)

**P1 Projects:**
- ⏸️ coditect-agent-marketplace (10 weeks)
- ⏸️ coditect-analytics (6 weeks)
- ⏸️ coditect-automation (8 weeks)

### Phase 3: Full GTM (Week 29+)
**Goal:** Public launch with marketing, sales, support

**Activities:**
- Marketing campaigns
- Sales enablement
- Customer onboarding
- Support infrastructure
- Continuous improvement

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

**Master Repository:**
- ✅ Initial structure created
- ✅ 10 submodules configured
- ✅ Master planning documents
- ⏸️ Awaiting Phase 1 kickoff

**Submodules:**
- ✅ coditect-framework - Operational
- ⏸️ All others - Ready for development

**Next Milestone:** Phase 1 Beta Development Start

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

**Last Updated:** November 16, 2025
**Current Phase:** Pre-Beta (Planning Complete)
**Next Milestone:** Phase 1 Beta Development Kickoff
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
**Owner:** AZ1.AI INC
**Lead:** Hal Casteel, Founder/CEO/CTO
