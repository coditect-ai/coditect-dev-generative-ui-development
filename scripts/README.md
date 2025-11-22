# Automation Scripts - CODITECT Rollout Master

**Last Updated:** 2025-11-22
**Directory Purpose:** Orchestration automation scripts for managing 46 submodules and master repository
**Total Scripts:** 19 Python scripts + 6 shell scripts
**Categories:** Project initialization, Git operations, timeline generation, maintenance

---

## Overview

This directory contains **automation scripts** that power the CODITECT Rollout Master repository orchestration. These scripts handle complex operations across 46 git submodules, generate project artifacts (timelines, diagrams), manage MEMORY-CONTEXT exports, and maintain repository health.

**Script Philosophy:**
- **Automation over manual processes** - Reduce human error in complex operations
- **Git submodule safety** - Scripts enforce correct submodule workflows
- **Reproducibility** - Same inputs always produce same outputs
- **Documentation generation** - Auto-generate timelines, diagrams, reports
- **Context preservation** - Integrate with MEMORY-CONTEXT system

---

## 📋 Script Categories

### 1. Project Initialization & Setup

| Script | Language | Purpose | Usage |
|--------|----------|---------|-------|
| **coditect-setup.py** | Python | Initialize new CODITECT project structure | `python coditect-setup.py` |
| **coditect-bootstrap-projects.py** | Python | Bootstrap multiple projects from templates | `python coditect-bootstrap-projects.py` |
| **coditect-project-init.sh** | Bash | Complete project initialization workflow | `./coditect-project-init.sh` |
| **coditect-project-spec-builder.sh** | Bash | Interactive project specification builder | `./coditect-project-spec-builder.sh` |

**When to Use:**
- Starting new CODITECT-based projects
- Creating submodules with standard structure
- Generating initial PROJECT-PLAN.md and TASKLIST.md
- Setting up .coditect symlink chains

---

### 2. Git & Submodule Operations

| Script | Language | Purpose | Usage |
|--------|----------|---------|-------|
| **sync-all-submodules.sh** | Bash | Sync all 46 submodules to latest | `./sync-all-submodules.sh` |
| **update-all-submodules.sh** | Bash | Update submodule references in master | `./update-all-submodules.sh` |
| **coditect-git-helper.py** | Python | Git operations helper with safety checks | `python coditect-git-helper.py` |
| **verify-distributed-intelligence.sh** | Bash | Validate .coditect symlink chain integrity | `./verify-distributed-intelligence.sh` |
| **rollback-reorg.sh** | Bash | Rollback repository reorganization | `./rollback-reorg.sh` |
| **maintenance/COMMIT-REORGANIZATION.sh** | Bash | Commit reorganization changes safely | `./maintenance/COMMIT-REORGANIZATION.sh` |

**When to Use:**
- Daily/weekly submodule synchronization
- After making changes in submodules
- Validating distributed intelligence architecture
- Emergency rollbacks

**CRITICAL:** Always use these scripts for submodule operations to avoid detached HEAD states and reference issues.

---

### 3. Timeline & Documentation Generation

| Script | Language | Purpose | Usage |
|--------|----------|---------|-------|
| **generate-timeline.py** | Python | Generate PROJECT-TIMELINE.json from PROJECT-PLAN.md | `python generate-timeline.py` |
| **generate-enhanced-timeline.py** | Python | Generate interactive HTML timeline visualization | `python generate-enhanced-timeline.py` |
| **generate-diagram-docs.py** | Python | Generate documentation from Mermaid diagrams | `python generate-diagram-docs.py` |
| **update-phase-readmes.py** | Python | Update README files in diagram phase directories | `python update-phase-readmes.py` |

**When to Use:**
- After updating PROJECT-PLAN.md milestones
- Generating stakeholder reports
- Creating presentation materials
- Updating architecture documentation

**Output Locations:**
- Timelines: `docs/project-management/PROJECT-TIMELINE-*.{json,html}`
- Diagrams: `diagrams/phase-*/README.md`

---

### 4. MEMORY-CONTEXT Management

| Script | Language | Purpose | Usage |
|--------|----------|---------|-------|
| **comprehensive-consolidation.py** | Python | Consolidate Claude Code session exports | `python comprehensive-consolidation.py` |
| **bulk-consolidate-exports.py** | Python | Bulk process multiple session exports | `python bulk-consolidate-exports.py` |
| **prototype_checkpoint_toon.py** | Python | TOON format checkpoint prototype | `python prototype_checkpoint_toon.py` |

**When to Use:**
- Weekly MEMORY-CONTEXT maintenance
- After completing major work sessions
- Preparing for session continuity
- TOON format experimentation

**Output Locations:**
- Consolidated exports: `MEMORY-CONTEXT/exports-archive/`
- Checkpoints: `MEMORY-CONTEXT/checkpoints/`

---

### 5. Reporting & Status

| Script | Language | Purpose | Usage |
|--------|----------|---------|-------|
| **status-report.py** | Python | Generate current project status report | `python status-report.py` |

**When to Use:**
- Daily standup preparation
- Weekly stakeholder updates
- Milestone completion verification

---

## 🚀 Quick Start Guide

### Daily Operations

```bash
# 1. Sync all submodules to latest
./sync-all-submodules.sh

# 2. Verify distributed intelligence
./verify-distributed-intelligence.sh

# 3. Generate status report
python status-report.py
```

### After Updating PROJECT-PLAN.md

```bash
# 1. Regenerate timeline JSON
python generate-timeline.py

# 2. Create interactive visualization
python generate-enhanced-timeline.py

# 3. Verify output
open ../docs/project-management/PROJECT-TIMELINE-INTERACTIVE.html
```

### After Working in Submodules

```bash
# 1. Update master repo pointers
./update-all-submodules.sh

# 2. Commit the updates
git add submodules/
git commit -m "chore: Update submodule references"
git push
```

### Weekly MEMORY-CONTEXT Maintenance

```bash
# 1. Consolidate exports
python comprehensive-consolidation.py

# 2. Archive old exports
mv MEMORY-CONTEXT/exports/*.txt MEMORY-CONTEXT/exports-archive/

# 3. Verify checkpoint integrity
ls -lh MEMORY-CONTEXT/checkpoints/
```

---

## 📝 Script Details

### coditect-project-init.sh (56KB)

**Complete project initialization workflow.**

**Features:**
- Interactive project specification
- Git repository creation
- .coditect symlink chain setup
- Initial PROJECT-PLAN.md generation
- TASKLIST.md with starter tasks
- Standard directory structure

**Usage:**
```bash
./coditect-project-init.sh
# Follow interactive prompts
```

**Output:**
- New project directory with CODITECT structure
- Git repository initialized
- Symlinks: .coditect → .claude → core
- Documentation: README.md, CLAUDE.md, PROJECT-PLAN.md

---

### sync-all-submodules.sh

**Safely synchronize all 46 submodules.**

**What it does:**
1. Fetch latest from all submodule remotes
2. Checkout main branch in each submodule
3. Pull latest changes
4. Handle detached HEAD states
5. Report any conflicts

**Usage:**
```bash
./sync-all-submodules.sh
```

**Safety Features:**
- Detects and warns about uncommitted changes
- Handles detached HEAD automatically
- Reports conflicts for manual resolution

---

### update-all-submodules.sh (11KB)

**Update submodule references in master repository.**

**What it does:**
1. Update all submodule pointers to current HEAD
2. Generate summary of changes
3. Prepare commit message
4. Validate no uncommitted changes in submodules

**Usage:**
```bash
./update-all-submodules.sh
```

**Output:**
- Updated .gitmodules references
- Commit message with change summary
- Ready for `git push`

---

### generate-enhanced-timeline.py (40KB)

**Generate interactive HTML Gantt chart from PROJECT-PLAN.md.**

**Features:**
- Parse PROJECT-PLAN.md for milestones
- Calculate dependencies and critical path
- Generate interactive D3.js visualization
- Export to HTML with zoom/pan controls

**Usage:**
```bash
python generate-enhanced-timeline.py

# Output: docs/project-management/PROJECT-TIMELINE-INTERACTIVE.html
```

**Dependencies:**
- Requires PROJECT-PLAN.md with milestone tables
- Python 3.10+
- No external Python packages needed (uses standard library)

---

### verify-distributed-intelligence.sh (5KB)

**Validate .coditect symlink chain integrity.**

**What it checks:**
- .coditect symlink exists and points correctly
- .claude symlink exists and points to .coditect
- Core submodule is initialized
- Symlink chain resolves correctly

**Usage:**
```bash
./verify-distributed-intelligence.sh

# Output: ✅ All symlinks valid OR ❌ Issues found with fix instructions
```

**Fixes:**
- Automatically repairs broken symlinks
- Re-initializes missing submodules
- Reports unresolvable issues

---

### coditect-router (symlink)

**AI-powered command router for slash commands.**

**Purpose:** Help users find the right slash command for their task.

**Target:** `../.coditect/scripts/coditect-router`

**Usage:**
```bash
./coditect-router "I need to add authentication"

# Interactive mode
./coditect-router -i
```

**Features:**
- Plain English command selection
- Explains why command is recommended
- Shows alternatives
- Works with or without API key

---

## ⚙️ Script Configuration

### Environment Variables

Most scripts use these environment variables:

```bash
# Project root (auto-detected)
export CODITECT_ROOT=/Users/halcasteel/PROJECTS/coditect-rollout-master

# Git user (for commits)
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your.email@example.com"

# MEMORY-CONTEXT location
export MEMORY_CONTEXT_DIR="$CODITECT_ROOT/MEMORY-CONTEXT"
```

### Python Dependencies

```bash
# Most scripts use standard library only
# Some require:
pip install jinja2  # For template rendering
pip install pygit2  # For advanced Git operations
```

### Shell Requirements

- **Bash 4.0+** (macOS: `brew install bash`)
- **Git 2.25+** (with submodule support)
- **Python 3.10+**

---

## 🔧 Maintenance

### Adding New Scripts

1. **Create script in appropriate category:**
   - Project init → root scripts/
   - Git operations → root scripts/
   - Maintenance → scripts/maintenance/
   - MEMORY-CONTEXT → root scripts/

2. **Follow naming convention:**
   - Python: `lowercase-with-hyphens.py`
   - Shell: `lowercase-with-hyphens.sh`
   - Executable: `chmod +x script.sh`

3. **Include header:**
   ```bash
   #!/usr/bin/env python3
   """
   Script Name - Brief description

   Usage: python script.py [args]
   """
   ```

4. **Update this README:**
   - Add to appropriate table
   - Document usage and purpose
   - Note any dependencies

5. **Test thoroughly:**
   - Test in clean repository
   - Test with submodules
   - Test error conditions
   - Document edge cases

---

## 🔗 Related Documentation

### Within This Repository

- **[../docs/project-management/](../docs/project-management/)** - PROJECT-PLAN.md and TASKLIST.md (scripts generate artifacts here)
- **[../WHAT-IS-CODITECT.md](../WHAT-IS-CODITECT.md)** - Understanding distributed intelligence (context for verification scripts)
- **[../.coditect/](../.coditect/)** - CODITECT core framework (target of setup scripts)
- **[../MEMORY-CONTEXT/](../MEMORY-CONTEXT/)** - Session exports (managed by consolidation scripts)

### Script Documentation

- **Timeline Generation:** See `generate-enhanced-timeline.py` docstrings
- **Git Operations:** See `coditect-git-helper.py` help
- **Project Init:** Run `./coditect-project-init.sh --help`

---

## 🆘 Troubleshooting

### Common Issues

**Q: sync-all-submodules.sh reports "detached HEAD" errors**
**A:** Expected behavior. Script automatically fixes by checking out main branch. If persists:
```bash
cd submodules/problematic-submodule
git checkout main
git pull
cd ../..
```

**Q: generate-enhanced-timeline.py fails with "No module named 'jinja2'"**
**A:** Install dependency:
```bash
pip install jinja2
```

**Q: verify-distributed-intelligence.sh reports broken symlinks**
**A:** Run script with fix mode:
```bash
./verify-distributed-intelligence.sh --fix
```

**Q: update-all-submodules.sh reports uncommitted changes**
**A:** Commit changes in submodules first:
```bash
cd submodules/affected-submodule
git add .
git commit -m "Your changes"
git push
cd ../..
./update-all-submodules.sh
```

---

## 📊 Script Statistics

| Metric | Value |
|--------|-------|
| Total Scripts | 25 |
| Python Scripts | 19 |
| Shell Scripts | 6 |
| Total Lines of Code | ~150K |
| Largest Script | coditect-project-init.sh (56KB) |
| Most Complex | generate-enhanced-timeline.py (40KB) |
| Submodule Operations | 6 scripts |
| Documentation Generators | 4 scripts |

---

## 📧 Support

**For script issues:**
1. Check this README for usage instructions
2. Run script with `--help` flag (if supported)
3. Check script docstrings and comments
4. Review related documentation
5. Contact: Hal Casteel, CTO

**For feature requests:**
- Document in `docs/project-management/TASKLIST.md`
- Create ADR if architectural decision required
- Implement following script conventions above

---

**Document Status:** ✅ Production Ready
**Last Validated:** 2025-11-22
**Next Review:** When new scripts added or major updates made
