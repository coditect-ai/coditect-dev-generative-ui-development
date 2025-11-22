# Automation Scripts - Claude Code Configuration

## Directory Purpose

Orchestration automation scripts for managing 46 submodules, generating artifacts, and maintaining repository health.

## Essential Reading

**READ FIRST:**
1. This CLAUDE.md - Script usage and safety
2. README.md - Complete script catalog
3. Individual script docstrings - Detailed usage

## Tech Stack

**Languages:**
- Python 3.10+ (19 scripts)
- Bash 4.0+ (6 scripts)

**Key Libraries:**
- Python standard library (most scripts)
- jinja2 (template rendering)
- pygit2 (advanced Git operations)

**Requirements:**
- Git 2.25+ (submodule support)
- bash, python3 in PATH

## Critical Scripts

### Submodule Operations (USE THESE, NOT RAW GIT)

**sync-all-submodules.sh**
- Sync all 46 submodules to latest
- Handles detached HEAD automatically
- Safe for daily use

**update-all-submodules.sh**
- Update master repo submodule pointers
- Run after changes in submodules
- Generates commit message

**verify-distributed-intelligence.sh**
- Validate .coditect symlink chain
- Auto-repair broken symlinks
- Run weekly for health check

### Documentation Generators

**generate-enhanced-timeline.py**
- Creates interactive HTML Gantt chart
- Input: PROJECT-PLAN.md
- Output: PROJECT-TIMELINE-INTERACTIVE.html

**generate-diagram-docs.py**
- Generate docs from Mermaid diagrams
- Updates diagram README files
- Run after diagram changes

### Project Initialization

**coditect-project-init.sh**
- Complete project setup workflow
- Interactive specification builder
- Creates CODITECT structure

## Common Operations

### Daily Maintenance
```bash
# Sync submodules
./sync-all-submodules.sh

# Verify symlinks
./verify-distributed-intelligence.sh

# Status report
python status-report.py
```

### After Submodule Changes
```bash
# Update pointers
./update-all-submodules.sh

# Commit
git add submodules/
git commit -m "chore: Update submodule references"
git push
```

### After PROJECT-PLAN Updates
```bash
# Regenerate timeline
python generate-timeline.py
python generate-enhanced-timeline.py

# Verify
open ../docs/project-management/PROJECT-TIMELINE-INTERACTIVE.html
```

### Weekly MEMORY-CONTEXT Cleanup
```bash
# Consolidate exports
python comprehensive-consolidation.py

# Archive
mv MEMORY-CONTEXT/exports/*.txt MEMORY-CONTEXT/exports-archive/
```

## Project-Specific Instructions

### When Working with Submodules
1. ALWAYS use sync-all-submodules.sh (never git submodule update manually)
2. After changes, run update-all-submodules.sh
3. Commit submodule pointer updates to master repo
4. Verify with verify-distributed-intelligence.sh

### When Generating Documentation
1. Update source (PROJECT-PLAN.md, diagrams)
2. Run appropriate generator script
3. Verify output in target directory
4. Commit generated files

### When Creating New Projects
1. Run coditect-project-init.sh
2. Follow interactive prompts
3. Verify .coditect symlink chain
4. Initialize git and push to remote

### Script Safety Rules
1. Scripts auto-detect CODITECT_ROOT
2. Always run from scripts/ directory
3. Check exit codes (0 = success)
4. Review script output for errors
5. Scripts won't modify submodules with uncommitted changes

## Cross-References

**Generated Artifacts:**
- docs/project-management/PROJECT-TIMELINE-*.json
- docs/project-management/PROJECT-TIMELINE-INTERACTIVE.html
- diagrams/phase-*/README.md

**Input Sources:**
- docs/project-management/PROJECT-PLAN.md
- diagrams/mermaid-source/*.mmd
- MEMORY-CONTEXT/exports/

**Maintenance Targets:**
- submodules/ (all 46 repos)
- .coditect symlink chain
- MEMORY-CONTEXT/

## Important Constraints

### Submodule Safety
- Never use raw `git submodule update`
- Always use sync-all-submodules.sh
- Check for uncommitted changes first
- Handle detached HEAD via scripts

### Script Execution
- Run from scripts/ directory
- Check current directory first
- Use absolute paths in scripts
- Validate environment variables

### Git Operations
- Conventional commit messages
- Always push submodule changes before updating pointers
- Create checkpoints after major operations

## Quality Gates

**Before Running Scripts:**
- [ ] Current directory is scripts/
- [ ] No uncommitted changes in submodules
- [ ] Git credentials configured
- [ ] Required dependencies installed

**After Submodule Operations:**
- [ ] All submodules on main branch
- [ ] No detached HEAD states
- [ ] Master repo pointers updated
- [ ] Changes committed and pushed

**After Documentation Generation:**
- [ ] Output files created successfully
- [ ] No broken links or references
- [ ] Visual artifacts display correctly
- [ ] Files committed to git

## Automation Hooks

### Submodule Sync (Daily)
```bash
# Add to cron or GitHub Actions
./sync-all-submodules.sh
./verify-distributed-intelligence.sh
```

### Timeline Regeneration (Weekly)
```bash
# After PROJECT-PLAN updates
python generate-timeline.py
python generate-enhanced-timeline.py
git add ../docs/project-management/PROJECT-TIMELINE-*
git commit -m "docs: Update project timeline"
```

### MEMORY-CONTEXT Cleanup (Weekly)
```bash
python comprehensive-consolidation.py
# Archive old exports
# Update checkpoint index
```

## Script Cheat Sheet

| Task | Script | Args |
|------|--------|------|
| Sync submodules | sync-all-submodules.sh | none |
| Update pointers | update-all-submodules.sh | none |
| Verify symlinks | verify-distributed-intelligence.sh | none |
| Timeline JSON | generate-timeline.py | none |
| Timeline HTML | generate-enhanced-timeline.py | none |
| Diagram docs | generate-diagram-docs.py | none |
| Status report | status-report.py | none |
| New project | coditect-project-init.sh | interactive |
| Consolidate exports | comprehensive-consolidation.py | none |

## Troubleshooting

**Detached HEAD in submodule:**
```bash
cd submodules/problematic-submodule
git checkout main
git pull
cd ../..
```

**Broken symlinks:**
```bash
./verify-distributed-intelligence.sh --fix
```

**Script can't find CODITECT_ROOT:**
```bash
export CODITECT_ROOT=/Users/halcasteel/PROJECTS/coditect-rollout-master
```

**Timeline generation fails:**
```bash
# Check PROJECT-PLAN.md has valid milestone tables
# Ensure Python 3.10+
python --version
```

## Environment Variables

```bash
# Auto-detected by scripts (optional override)
export CODITECT_ROOT=/path/to/coditect-rollout-master
export MEMORY_CONTEXT_DIR="$CODITECT_ROOT/MEMORY-CONTEXT"

# Git config (for commits)
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your.email@example.com"
```

---

**Status:** ✅ Production Ready
**Last Updated:** 2025-11-22
**Review Frequency:** When scripts added or updated
