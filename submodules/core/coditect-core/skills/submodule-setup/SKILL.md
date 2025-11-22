---
name: submodule-setup
description: Automated submodule initialization with directory structure creation, symlink chains, and template generation for distributed CODITECT intelligence.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata:
  token-multiplier: "15x"
  supported-languages: "Bash, Python"
  reusability: "High - Used for all 41+ submodules"
---

## When to Use This Skill

✅ Use when:
- Creating a new CODITECT submodule from scratch
- Setting up distributed intelligence (.coditect symlinks) in existing repository
- Initializing project templates (PROJECT-PLAN.md, TASKLIST.md, README.md)
- Establishing git submodule integration with parent repository
- Automating batch setup of multiple submodules

❌ Don't use when:
- Submodule already has .coditect symlinks (use `submodule-validation` instead)
- Only need to verify existing setup (use `submodule-validation`)
- Making changes to existing submodule configuration (use `submodule-configuration`)
- Running health checks on operational submodule (use `submodule-health`)

## Core Capabilities

### 1. Directory Structure Creation
Creates complete CODITECT-compliant directory structure for new submodule including:
- Root directory at correct location (`submodules/{category}/{repo-name}/`)
- Standard subdirectories (src/, docs/, tests/, scripts/, etc.)
- Configuration directories (.github/, .vscode/ if applicable)
- Proper permissions and ownership

### 2. Symlink Chain Establishment
Creates the critical symlink architecture that enables distributed intelligence:
- `.coditect -> ../../../.coditect` (links to parent rollout-master/.coditect/)
- `.claude -> .coditect` (Claude Code compatibility layer)
- Verifies symlink integrity and accessibility
- Handles relative path calculation for nested submodules

### 3. Template Generation
Generates project templates from CODITECT standards:
- PROJECT-PLAN.md with phased implementation structure
- TASKLIST.md with checkbox-based progress tracking
- README.md with submodule purpose and getting started
- .gitignore with CODITECT-specific exclusions
- Environment-specific configurations

### 4. Git Submodule Integration
Configures git submodule relationship with parent repository:
- Adds submodule to parent .gitmodules file
- Initializes submodule git repository
- Sets up remote tracking to GitHub
- Configures branch tracking (main/master)
- Commits submodule reference to parent repository

## Usage Pattern

### Step 1: Verify Parent Directory Structure
Before creating submodule, verify the category directory exists and is correct location:
```bash
# Check that category directory exists
ls submodules/cloud/  # or dev/, gtm/, labs/, etc.

# Verify parent .coditect is accessible
ls .coditect/agents/  # Should show 50+ agent files
```

### Step 2: Create Submodule Directory and Symlinks
Create the submodule directory structure and establish symlink chains:
```bash
# Create submodule directory
mkdir -p submodules/cloud/coditect-cloud-new-service

# Create symlink chains
cd submodules/cloud/coditect-cloud-new-service
ln -s ../../../.coditect .coditect
ln -s .coditect .claude

# Verify symlinks work
ls .coditect/agents/  # Should show agents from parent
```

### Step 3: Generate Project Templates
Use templates to create initial project files:
- Read template files from `.coditect/templates/submodule/`
- Customize PROJECT-PLAN.md with submodule-specific phases
- Customize TASKLIST.md with initial tasks
- Customize README.md with submodule purpose
- Generate .gitignore from template

### Step 4: Initialize Git Repository
Set up git repository and link to remote:
```bash
git init
git remote add origin https://github.com/coditect-ai/repo-name.git
git checkout -b main
git add .
git commit -m "Initial commit: CODITECT submodule setup"
```

### Step 5: Add to Parent Repository
Register submodule with parent rollout-master:
```bash
cd ../../..  # Return to rollout-master root
git submodule add https://github.com/coditect-ai/repo-name.git submodules/cloud/repo-name
git commit -m "Add cloud/repo-name submodule"
```

## Examples

See `examples/` directory for:
- `basic-setup.sh` - Simple single submodule setup
- `batch-setup.py` - Batch setup for multiple submodules
- `verification-checklist.md` - Post-setup verification steps

## Templates

See `templates/` directory for:
- `PROJECT-PLAN.template.md` - Standard project plan structure
- `TASKLIST.template.md` - Checkbox task list template
- `README.template.md` - Submodule README template
- `.gitignore.template` - Standard exclusions

## Integration Points

**Works with:**
- `submodule-validation` skill - Verify setup completed correctly
- `github-integration` skill - Create GitHub repository and configure
- `submodule-orchestrator` agent - Coordinate complete lifecycle

**Calls:**
- Bash tool for directory creation and symlink operations
- Write tool for template file generation
- Read tool to access template files from `.coditect/templates/`

## Success Criteria

Setup is complete when:
- [ ] Directory structure exists at `submodules/{category}/{repo-name}/`
- [ ] Symlinks `.coditect` and `.claude` are functional
- [ ] PROJECT-PLAN.md, TASKLIST.md, README.md exist with content
- [ ] Git repository initialized with remote configured
- [ ] Submodule added to parent .gitmodules
- [ ] All verification checks pass (see `submodule-validation` skill)

## Common Issues

**Symlink not working:**
```bash
# Check symlink target
ls -la .coditect
# Should show: .coditect -> ../../../.coditect

# Verify target exists
ls ../../../.coditect/agents/  # Should list agents
```

**Parent directory doesn't exist:**
```bash
# Create category directory first
mkdir -p submodules/cloud/
# Then create submodule
```

**Git submodule path mismatch:**
- Ensure path in `git submodule add` exactly matches directory structure
- Use relative paths from rollout-master root: `submodules/{category}/{repo-name}`
