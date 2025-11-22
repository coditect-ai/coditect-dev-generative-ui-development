---
name: submodule-configuration
description: Configuration management for submodules including template updates, settings synchronization, and environment-specific configurations across CODITECT ecosystem.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Grep
metadata:
  token-multiplier: "8x"
  supported-languages: "Bash, Python, YAML"
  reusability: "Medium - Used when updating configurations"
---

## When to Use This Skill

✅ Use when:
- Updating project templates (PROJECT-PLAN.md, TASKLIST.md)
- Synchronizing configuration changes across multiple submodules
- Applying new CODITECT standards to existing submodules
- Managing environment-specific configurations (dev, staging, prod)
- Updating repository settings or metadata

❌ Don't use when:
- Initial submodule setup (use `submodule-setup`)
- Verifying configuration (use `submodule-validation`)
- Monitoring health (use `submodule-health`)
- Making code changes (use development workflow)

## Core Capabilities

### 1. Template Update Management
Updates project templates while preserving customizations:
- Update PROJECT-PLAN.md structure while keeping content
- Refresh TASKLIST.md format while preserving task status
- Update README.md sections while keeping custom content
- Merge template changes with existing files
- Track template versions and changes

### 2. Configuration Synchronization
Keeps configuration consistent across submodules:
- Apply standard .gitignore updates to all submodules
- Synchronize CI/CD configurations (.github/workflows)
- Update common scripts and tools
- Propagate security updates
- Maintain version consistency

### 3. Environment Configuration
Manages environment-specific settings:
- Development environment configurations
- Staging environment settings
- Production configurations
- Environment variable templates
- Secret management integration

### 4. Metadata Management
Updates repository and project metadata:
- Repository descriptions and topics
- License files and copyright notices
- Contributing guidelines
- Code of conduct
- Issue and PR templates

## Usage Pattern

### Step 1: Identify Configuration Change Needed
Determine what configuration needs updating:
- Template format changes
- New CODITECT standards
- Security updates
- Environment changes
- Metadata updates

### Step 2: Test Configuration Change
Test the change on a single submodule first:
```bash
# Navigate to test submodule
cd submodules/labs/test-project

# Apply configuration change
# (specific commands depend on what's being updated)

# Verify change works
git diff
git status
```

### Step 3: Apply to Multiple Submodules
Once tested, apply to all relevant submodules:
```bash
# Use batch script
.coditect/scripts/update-submodule-config.py \
  --config-type gitignore \
  --categories cloud,dev,gtm
```

### Step 4: Verify Changes
Verify configuration applied correctly:
```bash
# Check each submodule
for dir in submodules/cloud/*; do
  echo "Checking $dir..."
  cd "$dir"
  git diff .gitignore
  cd ../../..
done
```

### Step 5: Commit and Push
Commit configuration changes:
```bash
# From each submodule
git add .gitignore
git commit -m "Update .gitignore with CODITECT standards"
git push

# Update parent repository references
cd ../../..
git add submodules/
git commit -m "Update submodule references: configuration sync"
git push
```

## Configuration Types

### Template Configurations
- `PROJECT-PLAN.md` - Project plan structure
- `TASKLIST.md` - Task list format
- `README.md` - Documentation structure
- `.gitignore` - Exclusion patterns

### CI/CD Configurations
- `.github/workflows/*.yml` - GitHub Actions
- `.github/dependabot.yml` - Dependency updates
- `.github/CODEOWNERS` - Code ownership

### Development Configurations
- `.vscode/settings.json` - VSCode settings
- `.editorconfig` - Editor configurations
- `pyrightconfig.json` - Python type checking
- `tsconfig.json` - TypeScript configuration

### Environment Configurations
- `.env.template` - Environment variable template
- `config/development.yml` - Dev environment
- `config/staging.yml` - Staging environment
- `config/production.yml` - Prod environment

## Examples

See `examples/` directory for:
- `update-gitignore.sh` - Update .gitignore across submodules
- `sync-ci-config.py` - Synchronize CI/CD configurations
- `update-templates.sh` - Refresh project templates

## Templates

See `templates/` directory for:
- Standard configuration files for each type
- Migration guides for version updates
- Rollback procedures

## Integration Points

**Works with:**
- `submodule-validation` skill - Verify configuration changes
- `batch-setup.py` script - Apply to multiple submodules
- Version control - Track configuration history

**Used by:**
- `submodule-orchestrator` agent - Coordinate updates
- DevOps automation - Configuration management

## Success Criteria

Configuration update complete when:
- [ ] Change tested on single submodule
- [ ] Applied to all relevant submodules
- [ ] Validation checks pass
- [ ] Changes committed and pushed
- [ ] Parent repository updated
- [ ] Documentation updated

## Best Practices

**Before Making Changes:**
- Test on single submodule first
- Back up existing configurations
- Document what's changing and why
- Plan rollback procedure

**During Changes:**
- Apply incrementally (one category at a time)
- Verify each batch before proceeding
- Monitor for errors or issues
- Keep change log

**After Changes:**
- Run validation checks
- Update documentation
- Notify team of changes
- Monitor for issues

## Common Scenarios

### Update .gitignore
```bash
# Copy new .gitignore template
cp .coditect/templates/submodule/.gitignore.template .gitignore

# Merge with existing exclusions
# Review and commit
```

### Sync CI/CD Workflows
```bash
# Copy workflow from template
cp .coditect/templates/github-workflows/ci.yml .github/workflows/

# Customize for submodule
# Test workflow
# Commit and push
```

### Update Environment Config
```bash
# Update environment template
cp config/development.template.yml config/development.yml

# Fill in environment-specific values
# Validate configuration
# Deploy to environment
```

## Related Skills

- **submodule-setup** - Initial setup
- **submodule-validation** - Verify changes
- **submodule-health** - Monitor after changes

## Related Agents

- **submodule-orchestrator** - Coordinate configuration updates
