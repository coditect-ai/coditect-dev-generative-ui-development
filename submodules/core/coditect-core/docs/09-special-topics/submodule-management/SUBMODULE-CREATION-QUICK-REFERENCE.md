# Submodule Creation Quick Reference

**TL;DR:** The CODITECT submodule creation process is fully automated with 4 entry points.

---

## Quick Start: Create Your First Submodule

### Option 1: Interactive Mode (Easiest for New Users)

```bash
python3 submodules/core/coditect-core/scripts/setup-new-submodule.py --interactive
```

**You'll be prompted for:**
- Category (cloud/dev/gtm/labs/docs/ops/market/core)
- Repository name (must start with `coditect-{category}-`)
- Purpose (one sentence)
- Visibility (public/private)

**What it does automatically:**
✅ Creates directory structure
✅ Sets up symlinks (.coditect, .claude)
✅ Generates 4 template files
✅ Initializes git repository
✅ Creates GitHub repository
✅ Pushes to remote
✅ Registers with parent
✅ Runs 23-point verification

**Time:** 2-3 minutes

### Option 2: Command-Line Mode (For Scripting)

```bash
python3 submodules/core/coditect-core/scripts/setup-new-submodule.py \
  --category cloud \
  --name coditect-cloud-service \
  --purpose "API gateway service" \
  --visibility public
```

### Option 3: Configuration File Mode (For Batch Operations)

**Create `submodules.yml`:**
```yaml
submodules:
  - category: cloud
    name: coditect-cloud-gateway
    purpose: API gateway for cloud services
    visibility: public
  - category: dev
    name: coditect-dev-logger
    purpose: Centralized logging utility
    visibility: private
```

**Run batch setup:**
```bash
python3 submodules/core/coditect-core/scripts/batch-setup.py --config submodules.yml
```

### Option 4: High-Level Workflow (Integrated Discovery + Creation)

```bash
/new-project "Build an API for managing team projects"
```

**This orchestrates:**
1. Project discovery (interactive interview)
2. Submodule creation (automated git setup)
3. Project planning (generates specifications)
4. Structure optimization (production-ready layout)
5. Quality assurance (verification checks)

---

## What Gets Created

When you create a submodule, you automatically get:

✅ **Git Repository:**
- Initialized with `main` branch
- Configured remote (origin → GitHub coditect-ai organization)
- Initial commit pushed

✅ **Symlink Chains:**
- `.coditect` → `../../../.coditect` (points to master repo's framework)
- `.claude` → `.coditect` (Claude Code compatibility)
- Both verified functional (access to 50+ agents, 20+ skills, 70+ commands)

✅ **Template Files:**
- `README.md` - Getting started guide
- `PROJECT-PLAN.md` - Implementation roadmap
- `TASKLIST.md` - Checkbox-based task tracking
- `.gitignore` - Standard exclusions

✅ **GitHub Integration:**
- Public/private repository configured
- Topics added (coditect + category)
- Proper description and homepage

✅ **Parent Integration:**
- Registered in `.gitmodules`
- Submodule pointer added to master repo
- Ready for collaborative development

---

## Verify Your Submodule

After creation, verify everything is correct:

```bash
# Option 1: Full verification with detailed checks
./submodules/core/coditect-core/scripts/verify-submodules.sh \
  submodules/{category}/{repo-name}

# Option 2: Health check and scoring
python3 submodules/core/coditect-core/scripts/submodule-health-check.py \
  --path submodules/{category}/{repo-name}

# Option 3: Quick spot checks
cd submodules/{category}/{repo-name}
ls -la .coditect/agents/ | head -5  # Should show 50+ agents
ls PROJECT-PLAN.md TASKLIST.md README.md  # All should exist
git remote -v  # Should show GitHub remote
git log --oneline -1  # Should show initial commit
```

---

## Next Steps After Creation

1. **Customize PROJECT-PLAN.md**
   - Add your specific project phases
   - Define success criteria
   - Outline resources needed

2. **Add tasks to TASKLIST.md**
   - Break down work into manageable pieces
   - Use checkbox format for tracking

3. **Start development**
   - Push code to your repo
   - Commit regularly
   - Use checkpoint process for major milestones

4. **Update parent repository**
   - When submodule progresses, the master repo's submodule pointer updates
   - Use automated checkpoint process to sync:
     ```bash
     python3 scripts/export-dedup.py --yes --auto-compact
     ```

---

## Common Patterns

### Create a Cloud Service

```bash
python3 submodules/core/coditect-core/scripts/setup-new-submodule.py \
  --category cloud \
  --name coditect-cloud-myservice \
  --purpose "Service for managing X in the cloud" \
  --visibility public
```

### Create a Private Development Tool

```bash
python3 submodules/core/coditect-core/scripts/setup-new-submodule.py \
  --category dev \
  --name coditect-dev-mytool \
  --purpose "Internal development tool for Y" \
  --visibility private
```

### Create Multiple Submodules

```bash
# Create config file
cat > my-services.yml << EOF
submodules:
  - category: cloud
    name: coditect-cloud-api
    purpose: REST API gateway
    visibility: public
  - category: cloud
    name: coditect-cloud-worker
    purpose: Background job processor
    visibility: public
  - category: dev
    name: coditect-dev-cli
    purpose: Command-line tools
    visibility: private
EOF

# Run batch setup
python3 submodules/core/coditect-core/scripts/batch-setup.py --config my-services.yml
```

### Dry-run to preview changes

```bash
python3 submodules/core/coditect-core/scripts/batch-setup.py \
  --config submodules.yml \
  --dry-run
```

---

## Troubleshooting

### "Must run from coditect-rollout-master root directory"

Make sure you're in the master repo:
```bash
cd /path/to/coditect-rollout-master
ls .coditect  # Should exist
```

### "Git is not installed or not in PATH"

Install Git:
```bash
# macOS
brew install git

# Linux (Ubuntu)
sudo apt-get install git

# Verify
git --version
```

### "GitHub CLI is not installed"

Install GitHub CLI:
```bash
# macOS
brew install gh

# Linux (Ubuntu)
sudo apt-get install gh

# Verify
gh --version
```

### "GitHub CLI is not authenticated"

Authenticate with GitHub:
```bash
gh auth login
# Follow the prompts to authenticate
```

### "Repository name validation failed"

Make sure your repo name follows the pattern:
```
coditect-{category}-{name}

Valid examples:
✅ coditect-cloud-gateway
✅ coditect-dev-logger
✅ coditect-ops-monitoring

Invalid examples:
❌ cloud-gateway (missing prefix)
❌ coditect_cloud_gateway (underscores instead of hyphens)
❌ Coditect-Cloud-Gateway (uppercase letters)
```

### "Symlink verification failed: agents directory not accessible"

This usually means the parent repo's `.coditect` is not accessible. Verify:
```bash
cd /path/to/coditect-rollout-master
ls -la .coditect
ls -la .coditect/agents/ | wc -l  # Should show 50+
```

---

## Automation Details

The creation process is **fully automated** and runs **8 steps:**

1. ✅ **Directory Creation** - Creates category/submodule dirs
2. ✅ **Symlink Setup** - Creates .coditect and .claude symlinks
3. ✅ **Template Generation** - Generates 4 template files
4. ✅ **Git Initialization** - Initializes git repo with initial commit
5. ✅ **GitHub Repository** - Creates repo via `gh` CLI
6. ✅ **Remote Configuration** - Sets up origin remote and pushes
7. ✅ **Parent Registration** - Registers submodule in .gitmodules
8. ✅ **Verification** - Runs 23-point validation suite

**Total time:** 2-3 minutes with zero manual git commands needed

---

## Integration with Workflows

### Export-Dedup Workflow

When you run the export-dedup process, **Step 8 automatically commits and pushes** all modified submodules:

```bash
# In Claude Code
/export

# In terminal
python3 submodules/core/coditect-core/scripts/export-dedup.py --yes --auto-compact
# This runs 8 steps including Step 8: automatic multi-submodule checkpoint
```

### Project Checkpoint

Create a major checkpoint with one command:

```bash
python3 submodules/core/coditect-core/scripts/create-checkpoint.py \
  "Sprint description" \
  --auto-commit
```

---

## Key Resources

- **Full Audit Report:** [SUBMODULE-CREATION-AUTOMATION-AUDIT.md](submodules/core/coditect-core/SUBMODULE-CREATION-AUTOMATION-AUDIT.md)
- **Setup Command Guide:** [setup-submodule.md](submodules/core/coditect-core/commands/setup-submodule.md)
- **Batch Setup Guide:** [batch-setup-submodules.md](submodules/core/coditect-core/commands/batch-setup-submodules.md)
- **New Project Workflow:** [new-project.md](submodules/core/coditect-core/commands/new-project.md)
- **Verification Guide:** [verify-submodule.md](submodules/core/coditect-core/commands/verify-submodule.md)

---

## Status

✅ **Submodule creation automation is fully operational and production-ready.**

- 4 entry points (interactive, CLI, config file, high-level)
- 6 automation scripts
- 4 slash commands
- 100% automation coverage
- 23+ validation checks per submodule
- Comprehensive documentation

**No manual git commands required. Everything is automated.**

---

**Last Updated:** November 22, 2025
**Framework:** CODITECT v1.0
**Status:** ✅ Production Ready
**Copyright:** © 2025 AZ1.AI INC. All rights reserved.
