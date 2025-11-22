---
name: submodule-validation
description: Comprehensive verification of submodule setup including symlink integrity, template generation, git configuration, and CODITECT framework accessibility.
license: MIT
allowed-tools: Bash, Read, Grep, Glob
metadata:
  token-multiplier: "10x"
  supported-languages: "Bash, Python"
  reusability: "High - Run after every submodule setup"
---

## When to Use This Skill

✅ Use when:
- Verifying new submodule setup completed correctly
- Troubleshooting submodule configuration issues
- Running health checks after updates
- Validating batch submodule operations
- Auditing submodule compliance with CODITECT standards

❌ Don't use when:
- Initial setup hasn't been completed (use `submodule-setup` first)
- Creating new submodule (validation comes after setup)
- Modifying configuration (use `submodule-configuration`)
- Monitoring ongoing operations (use `submodule-health`)

## Core Capabilities

### 1. Symlink Integrity Verification
Validates that symlink chains are correctly established and functional:
- `.coditect` symlink exists and points to `../../../.coditect`
- `.claude` symlink exists and points to `.coditect`
- Symlink targets are accessible (not broken)
- CODITECT framework is accessible through symlinks (agents/, skills/, commands/)
- Relative paths are correct for submodule location

### 2. Template Verification
Confirms required project templates exist and have content:
- PROJECT-PLAN.md exists with valid structure
- TASKLIST.md exists with checkbox format
- README.md exists with submodule description
- .gitignore exists with standard exclusions
- Templates follow CODITECT standards

### 3. Git Configuration Validation
Verifies git repository and remote configuration:
- Git repository initialized (.git directory exists)
- Remote 'origin' configured with GitHub URL
- Branch tracking configured (main branch)
- .gitmodules entry exists in parent repository
- Submodule can push/pull from remote

### 4. Framework Accessibility Testing
Tests that CODITECT framework is fully accessible:
- Can read agents from `.coditect/agents/`
- Can read skills from `.coditect/skills/`
- Can read commands from `.coditect/commands/`
- Can execute scripts from `.coditect/scripts/`
- STANDARDS.md and other core files accessible

## Usage Pattern

### Step 1: Navigate to Submodule
Change to submodule directory to validate:
```bash
cd submodules/cloud/coditect-cloud-service
```

### Step 2: Run Validation Checks
Execute validation script or manual checks:
```bash
# Check symlinks
ls -la .coditect
ls -la .claude

# Verify CODITECT access
ls .coditect/agents/ | wc -l  # Should show 50+
ls .coditect/skills/ | wc -l  # Should show 24+
ls .coditect/commands/ | wc -l # Should show 74+

# Check templates
ls PROJECT-PLAN.md TASKLIST.md README.md .gitignore

# Check git
git remote -v
git status
```

### Step 3: Verify Parent Integration
Check that parent repository recognizes submodule:
```bash
cd ../../..  # Return to rollout-master root

# Check .gitmodules
grep "coditect-cloud-service" .gitmodules

# Check submodule status
git submodule status | grep coditect-cloud-service
```

### Step 4: Run Automated Validation
Use validation script for comprehensive check:
```bash
# From rollout-master root
.coditect/scripts/verify-submodules.sh submodules/cloud/coditect-cloud-service
```

### Step 5: Review Validation Report
Review output and fix any issues found:
- ✅ All checks passed - submodule ready
- ❌ Failed checks - review errors and fix
- ⚠️  Warnings - optional items to address

## Validation Checklist

**Symlinks:**
- [ ] `.coditect` symlink exists
- [ ] `.coditect` points to `../../../.coditect`
- [ ] `.coditect` is accessible (not broken)
- [ ] `.claude` symlink exists
- [ ] `.claude` points to `.coditect`
- [ ] Can list `.coditect/agents/` (50+ files)
- [ ] Can list `.coditect/skills/` (24+ directories)
- [ ] Can list `.coditect/commands/` (74+ files)

**Templates:**
- [ ] PROJECT-PLAN.md exists
- [ ] PROJECT-PLAN.md has phases section
- [ ] TASKLIST.md exists
- [ ] TASKLIST.md has checkbox format
- [ ] README.md exists
- [ ] README.md has submodule description
- [ ] .gitignore exists

**Git Configuration:**
- [ ] .git directory exists
- [ ] Git remote 'origin' configured
- [ ] Remote URL is GitHub coditect-ai repository
- [ ] Main branch exists
- [ ] Can push to remote (authentication works)

**Parent Integration:**
- [ ] Entry in parent .gitmodules
- [ ] Submodule registered with git
- [ ] Submodule path matches directory

## Examples

See `examples/` directory for:
- `quick-validation.sh` - Fast validation check
- `comprehensive-validation.py` - Detailed validation report
- `batch-validation.sh` - Validate multiple submodules

## Templates

See `templates/` directory for:
- `validation-report.md` - Standard validation report format
- `validation-checklist.txt` - Printable checklist

## Common Issues and Fixes

**Broken symlink:**
```bash
# Remove and recreate
rm .coditect
ln -s ../../../.coditect .coditect
```

**Missing template:**
```bash
# Copy from template
cp ../../../.coditect/templates/submodule/PROJECT-PLAN.template.md PROJECT-PLAN.md
```

**Git remote not configured:**
```bash
git remote add origin https://github.com/coditect-ai/repo-name.git
```

**Not in .gitmodules:**
```bash
# From rollout-master root
git submodule add https://github.com/coditect-ai/repo-name.git submodules/category/repo-name
```

## Integration Points

**Works with:**
- `submodule-setup` skill - Run validation after setup
- `submodule-health` skill - Ongoing monitoring
- `verify-submodules.sh` script - Automated validation

**Used by:**
- `submodule-orchestrator` agent - Verify setup steps

## Success Criteria

Validation passes when:
- [ ] All symlink checks pass
- [ ] All template checks pass
- [ ] All git checks pass
- [ ] All parent integration checks pass
- [ ] No errors in validation report
- [ ] All warnings (if any) acknowledged

## Related Skills

- **submodule-setup** - Initial setup
- **submodule-health** - Ongoing monitoring
- **submodule-configuration** - Configuration management

## Related Agents

- **submodule-orchestrator** - Coordinates validation
