# CODITECT Rollout Master - Claude Code Configuration

## Project Overview

**CODITECT Rollout Master** is the master orchestration repository for the complete AZ1.AI CODITECT platform rollout, coordinating 10 sub-projects through git submodules for autonomous AI-first development.

### Purpose
- Centralized orchestration for all CODITECT platform components
- Automated coordination of multi-repo development
- AI-first autonomous development with human-in-the-loop guidance
- Beta → Pilot → Full GTM rollout management

---

## Architecture

### Master Repository Structure

```
coditect-rollout-master/
├── docs/                           # Master planning documents
│   ├── CODITECT-MASTER-ORCHESTRATION-PLAN.md
│   ├── CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md
│   ├── CODITECT-REUSABLE-TOOLS-ARCHITECTURE.md
│   ├── CODITECT-INTEGRATED-ECOSYSTEM-VISION.md
│   └── CODITECT-ROLLOUT-MASTER-PLAN.md
├── submodules/                     # 10 sub-projects as git submodules
│   ├── coditect-cloud-backend/     # FastAPI backend (P0, 12 weeks)
│   ├── coditect-cloud-frontend/    # React frontend (P0, 10 weeks)
│   ├── coditect-cli/               # Python CLI tools (P0, 8 weeks)
│   ├── coditect-docs/              # Docusaurus docs (P0, 6 weeks)
│   ├── coditect-agent-marketplace/ # Next.js marketplace (P1, 10 weeks)
│   ├── coditect-analytics/         # ClickHouse analytics (P1, 6 weeks)
│   ├── coditect-infrastructure/    # Terraform IaC (P0, 8 weeks)
│   ├── coditect-legal/             # Legal documents (P0, 4 weeks)
│   ├── coditect-framework/         # Core framework (P0, Ongoing)
│   └── coditect-automation/        # AI orchestration (P1, 8 weeks)
├── scripts/                        # Automation scripts
├── templates/                      # Project templates
├── workflows/                      # GitHub Actions workflows
├── MEMORY-CONTEXT/                 # Persistent context for AI agents
├── .gitmodules                     # Submodule configuration
├── README.md                       # User-facing documentation
└── CLAUDE.md                       # This file - AI agent configuration
```

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

---

**Last Updated:** November 15, 2025
**Current Phase:** Pre-Beta (Planning Complete)
**Next Milestone:** Phase 1 Beta Development Kickoff
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
**Owner:** AZ1.AI INC
**Lead:** Hal Casteel, Founder/CEO/CTO
