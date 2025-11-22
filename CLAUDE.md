# CODITECT Rollout Master - Claude Code Configuration

## Project Overview

**CODITECT Rollout Master** is the master orchestration repository coordinating the complete AZ1.AI CODITECT platform rollout through **46 git submodules** organized across **8 category folders**. This repository demonstrates CODITECT's distributed intelligence architecture in action.

**Current Phase:** Beta Testing (Active - Nov 12 to Dec 10, 2025)
**Public Launch Target:** March 11, 2026 (109 days remaining)

## Essential Reading

**YOU MUST read these documents before working in this repository:**

1. **[WHAT-IS-CODITECT.md](WHAT-IS-CODITECT.md)** - Understanding the distributed intelligence architecture (CRITICAL)
2. **[docs/project-management/PROJECT-PLAN.md](docs/project-management/PROJECT-PLAN.md)** - Complete rollout strategy and current status
3. **[docs/project-management/TASKLIST.md](docs/project-management/TASKLIST.md)** - Checkbox-based progress tracking
4. **[README.md](README.md)** - Repository overview and architecture

## Repository Structure

```
coditect-rollout-master/
├── .coditect -> submodules/core/coditect-core    # The CODITECT brain (distributed intelligence)
├── .claude -> .coditect                          # Claude Code compatibility symlink
├── docs/                                         # Master orchestration documentation
│   ├── project-management/                       # PROJECT-PLAN.md and TASKLIST.md
│   ├── adrs/                                     # Architecture Decision Records
│   └── security/                                 # Security documentation
├── submodules/                                   # 46 submodules in 8 categories
│   ├── core/       # 3 repos  - Core CODITECT framework
│   ├── cloud/      # 4 repos  - Cloud platform (optional SaaS)
│   ├── dev/        # 10 repos - Developer tools and CLI
│   ├── market/     # 2 repos  - Agent marketplace
│   ├── docs/       # 5 repos  - Documentation sites
│   ├── ops/        # 4 repos  - Operations and distribution
│   ├── gtm/        # 6 repos  - Go-to-market materials
│   └── labs/       # 12 repos - Research and next-generation
├── MEMORY-CONTEXT/                               # Session exports and context preservation
└── scripts/                                      # Orchestration automation scripts
```

## Developer Environment Setup

### Prerequisites

IMPORTANT: Install these tools before working in this repository:

- **Git** (with submodule support): `git --version` should show 2.25+
- **Python 3.10+**: For CODITECT automation scripts
- **Claude Code**: Anthropic's official CLI (recommended)

### Initial Setup

```bash
# Clone with all 46 submodules
git clone --recurse-submodules https://github.com/coditect-ai/coditect-rollout-master.git

# Or if already cloned, initialize submodules
git submodule update --init --recursive
```

## Repository Etiquette

### IMPORTANT: Git Submodule Workflow

**YOU MUST follow this workflow when working with submodules:**

#### Working in a Submodule

```bash
# 1. Navigate to the submodule
cd submodules/cloud/coditect-cloud-backend

# 2. Ensure you're on the correct branch
git checkout main
git pull

# 3. Make changes, commit, and push IN THE SUBMODULE
git add .
git commit -m "feat: Add user authentication"
git push

# 4. Return to master repo and update the submodule reference
cd ../../..
git add submodules/cloud/coditect-cloud-backend
git commit -m "Update cloud backend: Add user authentication"
git push
```

**CRITICAL:** Always commit and push in the submodule FIRST, then update the pointer in the master repo.

#### Updating All Submodules

```bash
# Pull latest changes from all submodules
git submodule update --remote --merge

# Review changes
git status

# Commit pointer updates
git add submodules/
git commit -m "Update all submodule pointers to latest"
git push
```

### Branch Naming Convention

- `main` - Production-ready code (protected)
- `feature/short-description` - New features
- `fix/short-description` - Bug fixes
- `docs/short-description` - Documentation updates
- `refactor/short-description` - Code refactoring

### Commit Message Format

Follow Conventional Commits:

```
<type>(<scope>): <subject>

<body>

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`

## Development Workflow

### Explore → Plan → Code → Commit

**1. EXPLORE** - Understand the current state
```bash
# Read master planning documents
cat docs/project-management/PROJECT-PLAN.md | head -100
cat docs/project-management/TASKLIST.md | grep '\[ \]' | head -20

# Check submodule status
git submodule status
```

**2. PLAN** - Create implementation plan
- Identify which submodules need changes
- Check for cross-submodule dependencies
- Review relevant ADRs in docs/adrs/
- Update TASKLIST.md with new tasks

**3. CODE** - Implement changes
- Work in one submodule at a time
- Follow submodule's CLAUDE.md guidelines
- Update submodule documentation as you go

**4. COMMIT** - Checkpoint your work
```bash
# Create automated checkpoint (after significant work)
python3 .coditect/scripts/create-checkpoint.py "Sprint description" --auto-commit
```

## Unexpected Behaviors & Important Notes

### Submodule Detached HEAD

**Problem:** After `git submodule update`, submodules may be in detached HEAD state.

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

**Problem:** Submodule has merge conflicts after `git submodule update --remote`.

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

### MEMORY-CONTEXT Architecture

**IMPORTANT:** This repository uses MEMORY-CONTEXT for session preservation:

- `/MEMORY-CONTEXT/sessions/` - Session exports (read at session start)
- `/MEMORY-CONTEXT/checkpoints/` - Sprint checkpoints
- `/MEMORY-CONTEXT/dedup_state/` - Deduplicated message store (7,507+ unique messages)

**Always create checkpoints after completing work** to enable context continuity across sessions.

## AI Agent Coordination

### Master Planning Documents

AI agents MUST read these before making changes:

1. **docs/project-management/PROJECT-PLAN.md** - Overall rollout strategy
2. **docs/project-management/TASKLIST.md** - Current progress tracking
3. **Per-submodule PROJECT-PLAN.md** - Submodule-specific plans

### Human Checkpoints Required

**YOU MUST request human approval for:**

- Architecture changes affecting multiple submodules
- New dependencies or technology additions
- Budget changes (>$5K)
- Timeline adjustments
- Security-related changes

Provide clear recommendations with pros/cons for human decision-making.

## Security & Secrets

**NEVER commit:**
- API keys, tokens, credentials
- `.env` files with secrets
- SSL certificates or private keys

**ALWAYS use:**
- Google Cloud Secret Manager (production)
- `.gitignore` for local secrets
- Environment variables for configuration

## Common Tasks

### Create Checkpoint (After Completing Work)

```bash
python3 .coditect/scripts/create-checkpoint.py "Description of work completed" --auto-commit
```

This creates:
- Checkpoint document in CHECKPOINTS/
- MEMORY-CONTEXT session export
- Updates README.md with checkpoint link
- Commits all changes to git

### Sync All Submodules

```bash
# Update all to latest
git submodule update --remote --merge

# Commit updates
git add submodules/
git commit -m "Sync all submodules to latest"
git push
```

### Add New Submodule

```bash
git submodule add https://github.com/coditect-ai/new-repo.git submodules/category/new-repo
git commit -m "Add new-repo submodule to category"
git push
```

## Support & Troubleshooting

- **Submodule Issues:** See [Git Submodules Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- **CODITECT Framework:** See `.coditect/README.md` or [coditect-core repository](https://github.com/coditect-ai/coditect-core)
- **Project Questions:** Review docs/project-management/ directory

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
