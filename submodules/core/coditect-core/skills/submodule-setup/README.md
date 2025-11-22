# Submodule Setup Skill

**Purpose:** Automated initialization of CODITECT submodules with directory structure, symlink chains, and template generation.

## Quick Start

### For Claude Code Users

When setting up a new submodule, simply invoke:

```
Use the submodule-setup skill to create a new submodule at submodules/cloud/coditect-cloud-newservice
```

Claude will autonomously:
1. Verify parent directory structure
2. Create submodule directory
3. Establish symlink chains
4. Generate project templates
5. Initialize git repository

### For Manual Setup

```bash
# 1. Navigate to rollout-master root
cd /path/to/coditect-rollout-master

# 2. Create submodule directory
mkdir -p submodules/cloud/coditect-cloud-newservice

# 3. Create symlinks
cd submodules/cloud/coditect-cloud-newservice
ln -s ../../../.coditect .coditect
ln -s .coditect .claude

# 4. Verify symlinks
ls .coditect/agents/  # Should show 50+ agents

# 5. Generate templates (use templates/ directory)
# Copy and customize PROJECT-PLAN, TASKLIST, README

# 6. Initialize git
git init
git remote add origin https://github.com/coditect-ai/coditect-cloud-newservice.git

# 7. Add to parent repository
cd ../../..
git submodule add https://github.com/coditect-ai/coditect-cloud-newservice.git submodules/cloud/coditect-cloud-newservice
```

## What Gets Created

After setup, your submodule will have:

```
submodules/cloud/coditect-cloud-newservice/
├── .coditect -> ../../../.coditect    [SYMLINK - Critical!]
├── .claude -> .coditect               [SYMLINK - Claude compatibility]
├── PROJECT-PLAN.md                    [Phased implementation plan]
├── TASKLIST.md                        [Checkbox task tracking]
├── README.md                          [Submodule documentation]
├── .gitignore                         [Standard exclusions]
└── src/                               [Source code directory]
```

## Verification

After setup, verify with:

```bash
# Check symlinks
ls -la .coditect
ls .coditect/agents/  # Should list agents

# Check templates exist
ls PROJECT-PLAN.md TASKLIST.md README.md

# Check git configuration
git remote -v
git status
```

Or use the `submodule-validation` skill for comprehensive checks.

## Examples

See `examples/` directory:
- `basic-setup.sh` - Simple single submodule
- `batch-setup.py` - Multiple submodules at once
- `verification-checklist.md` - What to verify

## Templates

See `templates/` directory:
- `PROJECT-PLAN.template.md` - Standard structure
- `TASKLIST.template.md` - Task list format
- `README.template.md` - README format
- `.gitignore.template` - Exclusions

## Troubleshooting

**Symlink broken:**
```bash
# Remove and recreate
rm .coditect
ln -s ../../../.coditect .coditect
```

**Category directory doesn't exist:**
```bash
# Create it first
mkdir -p submodules/cloud/
```

**Git submodule not registered:**
```bash
# Add from rollout-master root
git submodule add <url> submodules/cloud/repo-name
```

## Next Steps

After setup:
1. Run `submodule-validation` skill to verify
2. Customize PROJECT-PLAN.md for your project
3. Add initial tasks to TASKLIST.md
4. Push to GitHub remote
5. Start development!

## Related Skills

- **submodule-validation** - Verify setup correctness
- **github-integration** - Create GitHub repo
- **submodule-configuration** - Manage config
- **submodule-health** - Monitor status

## Related Agents

- **submodule-orchestrator** - Coordinates all operations
