# CODITECT Rollout Master - Claude Code Configuration

## Project Overview

Master orchestration repository coordinating **46 git submodules** across **8 category folders** for complete AZ1.AI CODITECT platform rollout (Beta → Pilot → GTM).

**Current Phase:** Beta Testing (Active - Week 2 of 4)
**Public Launch:** March 11, 2026 (109 days remaining)
**Architecture:** Distributed intelligence via .coditect symlink chains

---

## Essential Reading

**READ FIRST (in order):**

1. **[WHAT-IS-CODITECT.md](WHAT-IS-CODITECT.md)** - Distributed intelligence architecture (CRITICAL)
2. **[README.md](README.md)** - Repository overview and navigation guide
3. **[docs/project-management/PROJECT-PLAN.md](docs/project-management/PROJECT-PLAN.md)** - Complete rollout strategy
4. **[docs/project-management/TASKLIST.md](docs/project-management/TASKLIST.md)** - 530+ tasks with checkbox tracking

---

## 📂 Hierarchical Documentation

**This repository uses hierarchical CLAUDE.md files** - navigate to subdirectory CLAUDE.md for task-specific AI agent context.

### Documentation Structure

```
ROOT (you are here)
├── CLAUDE.md ⭐ - Master orchestration and submodule coordination
│
├── docs/project-management/CLAUDE.md - Project planning and task management
│   → Read this for: PROJECT-PLAN/TASKLIST updates, sprint planning, milestone tracking
│
├── docs/adrs/CLAUDE.md - Architecture decision documentation
│   → Read this for: ADR creation/review, technology choices, architectural constraints
│
├── docs/security/CLAUDE.md - Security operations and compliance
│   → Read this for: Security advisories, incident response, container compliance
│
└── scripts/CLAUDE.md - Automation script execution
    → Read this for: Running scripts, submodule sync, timeline generation
```

### When to Read Subdirectory CLAUDE.md

**Project Planning Tasks** → docs/project-management/CLAUDE.md
- Updating PROJECT-PLAN.md or TASKLIST.md
- Sprint planning and milestone tracking
- Progress reporting and status updates
- Timeline visualization regeneration

**Architecture Tasks** → docs/adrs/CLAUDE.md
- Creating or reviewing ADRs
- Understanding technology stack choices
- Implementing features per architectural constraints
- Validating cross-ADR consistency

**Security Tasks** → docs/security/CLAUDE.md
- Reviewing GCP security advisories
- Container security compliance
- Incident response workflows
- Security best practices for deployments

**Script Execution** → scripts/CLAUDE.md
- Running submodule sync scripts
- Generating documentation/timelines
- Project initialization workflows
- MEMORY-CONTEXT management

---

## Repository Structure

```
coditect-rollout-master/
├── .coditect -> submodules/core/coditect-core    # CODITECT brain
├── .claude -> .coditect                          # Claude Code compatibility
├── docs/                                         # Master documentation
│   ├── project-management/ - PROJECT-PLAN.md (72KB) + TASKLIST.md (23KB)
│   ├── adrs/ - 10 ADRs for Project Intelligence Platform
│   └── security/ - GCP security advisories
├── diagrams/ - 24 C4 architecture diagrams (7 phases)
├── scripts/ - 19 Python + 6 shell automation scripts
├── submodules/ - 46 repositories across 8 categories
└── MEMORY-CONTEXT/ - Session exports and context preservation
```

---

## Prerequisites

**Required Tools:**
- Git 2.25+ (submodule support)
- Python 3.10+
- Claude Code (Anthropic CLI)

**Initial Setup:**
```bash
git clone --recurse-submodules https://github.com/coditect-ai/coditect-rollout-master.git
# OR if already cloned:
git submodule update --init --recursive
```

---

## Git Submodule Workflow

### CRITICAL: Always Follow This Pattern

**Working in a Submodule:**

```bash
# 1. Navigate to submodule
cd submodules/cloud/coditect-cloud-backend

# 2. Ensure on main branch
git checkout main
git pull

# 3. Make changes, commit, push IN THE SUBMODULE
git add .
git commit -m "feat: Add user authentication"
git push

# 4. Return to master and update pointer
cd ../../..
git add submodules/cloud/coditect-cloud-backend
git commit -m "Update cloud backend: Add user authentication"
git push
```

**CRITICAL:** Commit and push in submodule FIRST, then update pointer in master repo.

**Syncing All Submodules:**

```bash
# Use the sync script (NEVER use raw git submodule update)
./scripts/sync-all-submodules.sh

# Review changes
git status

# Commit pointer updates
git add submodules/
git commit -m "Sync all submodules to latest"
git push
```

**Safety:** Always use `scripts/sync-all-submodules.sh` instead of raw git commands - it handles detached HEAD states automatically.

---

## Branch Naming & Commits

**Branch Convention:**
- `main` - Production-ready (protected)
- `feature/short-description` - New features
- `fix/short-description` - Bug fixes
- `docs/short-description` - Documentation
- `refactor/short-description` - Code refactoring

**Commit Format:**

```
<type>(<scope>): <subject>

<body>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`

---

## Development Workflow

### 1. EXPLORE - Understand Current State

```bash
# Read master planning
cat docs/project-management/PROJECT-PLAN.md | head -100
cat docs/project-management/TASKLIST.md | grep '\[ \]' | head -20

# Check submodule status
git submodule status
```

### 2. PLAN - Create Implementation Plan

- Identify which submodules need changes
- Check cross-submodule dependencies
- Review relevant ADRs in docs/adrs/
- Update TASKLIST.md with new tasks

### 3. CODE - Implement Changes

- Work in one submodule at a time
- Follow submodule's CLAUDE.md guidelines
- Update submodule documentation

### 4. COMMIT - Checkpoint Work

```bash
python3 .coditect/scripts/create-checkpoint.py "Sprint description" --auto-commit
```

---

## Common Tasks

### Sync Submodules to Latest

```bash
./scripts/sync-all-submodules.sh
git add submodules/
git commit -m "Sync all submodules to latest"
git push
```

### Create Project Checkpoint

```bash
python3 .coditect/scripts/create-checkpoint.py "Description of work completed" --auto-commit
```

### Regenerate Timeline After PROJECT-PLAN Updates

```bash
cd scripts/
python generate-enhanced-timeline.py
# Verify: open ../docs/project-management/PROJECT-TIMELINE-INTERACTIVE.html
```

### Verify Distributed Intelligence

```bash
./scripts/verify-distributed-intelligence.sh
```

---

## AI Agent Coordination

### Master Planning Documents

**AI agents MUST read before making changes:**

1. docs/project-management/PROJECT-PLAN.md - Overall rollout strategy
2. docs/project-management/TASKLIST.md - Current progress
3. Subdirectory CLAUDE.md - Task-specific context

### Human Approval Required For

**YOU MUST request human approval for:**

- Architecture changes affecting multiple submodules
- New dependencies or technology additions
- Budget changes (>$5K)
- Timeline adjustments
- Security-related changes

Provide clear recommendations with pros/cons for human decision.

---

## Security & Secrets

**NEVER commit:**
- API keys, tokens, credentials
- `.env` files with secrets
- SSL certificates or private keys

**ALWAYS use:**
- Google Cloud Secret Manager (production)
- `.gitignore` for local secrets
- Environment variables for configuration

---

## Unexpected Behaviors

### Submodule Detached HEAD

**Problem:** After `git submodule update`, submodule in detached HEAD state.

**Solution:**
```bash
cd submodules/problematic-submodule
git checkout main
git pull
cd ../..
git add submodules/problematic-submodule
git commit -m "Fix detached HEAD in submodule"
```

### Merge Conflicts in Submodules

**Problem:** Submodule has conflicts after `git submodule update --remote`.

**Solution:**
```bash
cd submodules/conflicted-submodule
git pull origin main
# Resolve conflicts manually
git add .
git commit
git push
cd ../..
git add submodules/conflicted-submodule
git commit -m "Resolve merge conflicts in submodule"
```

---

## MEMORY-CONTEXT Architecture

**Session Preservation System:**

- `/MEMORY-CONTEXT/sessions/` - Session exports (read at session start)
- `/MEMORY-CONTEXT/checkpoints/` - Sprint checkpoints
- `/MEMORY-CONTEXT/dedup_state/` - Deduplicated messages (7,507+ unique)

**Always create checkpoints after completing work** to enable context continuity.

---

## Support & Troubleshooting

**Documentation:**
- Submodule issues: [Git Submodules Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- CODITECT framework: `.coditect/README.md`
- Project questions: docs/project-management/

**Contact:** Hal Casteel, Founder/CEO/CTO

---

## Current Status

**Phase:** Beta Testing (Active - Week 2 of 4)
**Next Milestone:** Beta Analysis - December 10, 2025
**Submodules:** 46 repositories across 8 categories
**Documentation:** 456K+ words comprehensive
**Root Organization:** Production-ready (100/100 standards)

---

**Last Updated:** 2025-11-22
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
**Owner:** AZ1.AI INC
**Lead:** Hal Casteel, Founder/CEO/CTO
