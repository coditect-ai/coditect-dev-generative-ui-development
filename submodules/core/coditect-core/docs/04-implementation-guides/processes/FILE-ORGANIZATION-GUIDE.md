# CODITECT Rollout Master - File Organization Guide

**Quick Reference:** Where does this file belong?

---

## Root Directory Files (ESSENTIAL ONLY)

Only these files should exist in the project root:

```
/Users/halcasteel/PROJECTS/coditect-rollout-master/
├── README.md                    # User-facing documentation
├── CLAUDE.md                    # AI agent configuration
├── PROJECT-PLAN.md              # Master project plan
├── TASKLIST.md                  # Task tracking
├── .gitignore                   # Git ignore rules
├── .gitmodules                  # Submodule configuration
├── .claude -> .coditect         # Symlink (framework access)
├── .coditect -> submodules/...  # Symlink (core framework)
└── WHAT-IS-CODITECT.md -> ...   # Symlink (architecture docs)
```

---

## File Type Location Guide

### Session Exports (.txt files)
**Location:** `MEMORY-CONTEXT/exports-archive/`

**Pattern:** `YYYY-MM-DD-EXPORT-*.txt`

**Examples:**
- 2025-11-22-EXPORT-SESSION-CONTEXT.txt
- 2025-11-17-MEMORY-CONTEXT-REFACTOR.txt
- EXPORT-CURRENT-BUILD.txt

**Why:** Session exports are persistent AI context, not project documentation.

---

### Checkpoint Documents
**Location:** `CHECKPOINTS/`

**Pattern:** `CHECKPOINT-*.md`, `YYYY-MM-DDTHH-MM-SSZ-*.md`

**Examples:**
- CHECKPOINT-CLOUD-SQL-DEPLOYMENT-READY.md
- CHECKPOINT-PROCESS-IMPLEMENTATION.md
- 2025-11-22T10-30-00Z-Sprint-Complete.md

**Why:** Checkpoints have dedicated directory for historical tracking.

---

### Workflow Documentation
**Location:** `docs/`

**Pattern:** `*-WORKFLOW.md`, `AUTOMATED-*.md`

**Examples:**
- AUTOMATED-CHECKPOINT-WORKFLOW.md
- README-AUTOMATED-WORKFLOW.md
- GIT-WORKFLOW.md

**Why:** All documentation belongs in docs/ directory.

---

### Customer-Facing Guides
**Location:** `docs/`

**Pattern:** `QUICKSTART-*.md`, `*-GUIDE.md`

**Examples:**
- QUICKSTART-GUIDE-FOR-NEW-CUSTOMERS.md
- INSTALLATION-GUIDE.md
- DEVELOPER-GUIDE.md

**Why:** User documentation should be easily discoverable in docs/.

---

### Submodule Documentation
**Location:** `docs/`

**Pattern:** `SUBMODULE-*.md`

**Examples:**
- SUBMODULE-CREATION-QUICK-REFERENCE.md
- SUBMODULE-CREATION-VERIFICATION-SUMMARY.md
- SUBMODULE-MIGRATION-PLAN.md

**Why:** Technical reference documentation belongs in docs/.

---

### Security Advisories
**Location:** `docs/security/`

**Pattern:** `*-security-*`, `*-advisories/`

**Examples:**
- coditect-google-security-advisories/
- security-audit-2025.md
- vulnerability-reports/

**Why:** Security files should be segregated for access control.

---

### Architecture Diagrams
**Location:** `diagrams/`

**Pattern:** `*.mmd`, `*.md`, `phase-*/`

**Examples:**
- master-gantt-timeline.mmd
- phase-1-claude-framework/
- mermaid-source/

**Why:** Visual architecture should be separate from text documentation.

---

### Automation Scripts
**Location:** `scripts/`

**Pattern:** `*.py`, `*.sh`, `coditect-*.py`

**Examples:**
- coditect-project-init.sh
- generate-diagram-docs.py
- update-phase-readmes.py

**Why:** Executable scripts have dedicated directory.

---

### Infrastructure Code
**Location:** `infrastructure/`

**Pattern:** `docker-compose*.yml`, `*.tf`, `setup.sh`

**Examples:**
- docker-compose.yml
- postgres/
- deployment/

**Why:** Infrastructure as code should be isolated.

---

### Project Templates
**Location:** `templates/`

**Pattern:** `template-*`, `*.template.md`

**Examples:**
- template-project-plan.md
- template-tasklist.md
- api-template/

**Why:** Reusable templates should be centralized.

---

## .gitignore Protection

The following patterns are blocked from being committed to root:

```gitignore
# Export files
/*.txt
/EXPORT-*.txt
/*-EXPORT-*.txt
/2025-*-EXPORT-*.txt

# Checkpoint files
/CHECKPOINT-*.md

# Workflow docs
/AUTOMATED-*.md
/*-WORKFLOW.md
/*-GUIDE*.md
/QUICKSTART-*.md

# Submodule docs
/SUBMODULE-*.md

# Security advisories
/coditect-google-security-advisories/
/*-security-*/
```

**If you try to commit a file to root and it's blocked:** Check this guide for the correct location!

---

## Common Mistakes and Fixes

### Mistake: Export file in root
```bash
# WRONG
/Users/.../coditect-rollout-master/2025-11-22-EXPORT-SESSION.txt

# RIGHT
/Users/.../coditect-rollout-master/MEMORY-CONTEXT/exports-archive/2025-11-22-EXPORT-SESSION.txt

# FIX
mv 2025-11-22-EXPORT-SESSION.txt MEMORY-CONTEXT/exports-archive/
```

---

### Mistake: Checkpoint in root
```bash
# WRONG
/Users/.../coditect-rollout-master/CHECKPOINT-FEATURE-COMPLETE.md

# RIGHT
/Users/.../coditect-rollout-master/CHECKPOINTS/CHECKPOINT-FEATURE-COMPLETE.md

# FIX
git mv CHECKPOINT-FEATURE-COMPLETE.md CHECKPOINTS/
```

---

### Mistake: Documentation in root
```bash
# WRONG
/Users/.../coditect-rollout-master/QUICKSTART-GUIDE.md

# RIGHT
/Users/.../coditect-rollout-master/docs/QUICKSTART-GUIDE.md

# FIX
mv QUICKSTART-GUIDE.md docs/
```

---

## Decision Tree: Where Does This File Go?

```
Is it a session export (.txt)?
├─ YES → MEMORY-CONTEXT/exports-archive/
└─ NO ↓

Is it a checkpoint document?
├─ YES → CHECKPOINTS/
└─ NO ↓

Is it a security advisory?
├─ YES → docs/security/
└─ NO ↓

Is it documentation (.md)?
├─ YES → docs/
└─ NO ↓

Is it an architecture diagram?
├─ YES → diagrams/
└─ NO ↓

Is it a script (.py, .sh)?
├─ YES → scripts/
└─ NO ↓

Is it infrastructure code?
├─ YES → infrastructure/
└─ NO ↓

Is it a template?
├─ YES → templates/
└─ NO ↓

Is it essential project config?
├─ YES → ROOT (e.g., README.md, CLAUDE.md, PROJECT-PLAN.md)
└─ NO → Ask before creating in root!
```

---

## Automated Enforcement

The `.gitignore` file automatically prevents misplaced files from being committed. If you try to add a file to root and git blocks it, that's a sign the file belongs in a subdirectory!

**Example:**
```bash
$ git add CHECKPOINT-NEW-FEATURE.md
The following paths are ignored by one of your .gitignore files:
CHECKPOINT-NEW-FEATURE.md

# This is correct! Move it to CHECKPOINTS/ instead:
$ git mv CHECKPOINT-NEW-FEATURE.md CHECKPOINTS/
$ git add CHECKPOINTS/CHECKPOINT-NEW-FEATURE.md
```

---

## Verification Command

Check if root is clean:

```bash
# List all files in root (should see only 10 essential files)
ls -la | grep "^-" | wc -l

# If you see more than 10, investigate:
ls -la | grep "^-"

# Check which files are misplaced:
ls -1 *.txt *.md 2>/dev/null | grep -v -E "^(README|CLAUDE|PROJECT-PLAN|TASKLIST|WHAT-IS-CODITECT)\.md$"
```

---

## Questions?

**Q: Can I create a new markdown file in root?**
A: Only if it's essential project documentation (README.md, CLAUDE.md, PROJECT-PLAN.md, TASKLIST.md). Everything else goes in `docs/`.

**Q: What if I need to create a new category?**
A: Create a new subdirectory with a clear name and update this guide. Don't scatter files in root!

**Q: What about temporary files?**
A: Use `tmp/` directory (create if needed) or your local system's temp directory. Never commit temp files!

**Q: How do I preserve git history when moving files?**
A: Use `git mv` instead of regular `mv`:
```bash
git mv SOURCE DESTINATION
git commit -m "chore: Move file to proper location"
```

---

## Maintenance

This guide should be updated whenever:
- New file categories are created
- Directory structure changes
- .gitignore rules are added
- Production standards evolve

**Last Updated:** November 22, 2025
**Maintained by:** CODITECT Project Organizer Agent
**Framework:** AZ1.AI CODITECT v1.0

---

**Remember:** A clean root directory is a sign of a professional, production-ready project!
