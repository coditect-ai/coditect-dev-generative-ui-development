# Setup Submodule

Interactive command to set up a new CODITECT submodule with complete directory structure, symlinks, templates, and GitHub integration. This command guides you through the entire submodule initialization process step-by-step.

## Steps to follow:

### Step 1: Gather Submodule Information

Ask the user for the following information:
- **Category:** Which category does this submodule belong to? (cloud, dev, gtm, labs, docs, ops, market, core)
- **Repository Name:** What is the repository name? (Must follow `coditect-{category}-{name}` convention)
- **Purpose:** Brief one-sentence description of the submodule's purpose
- **Visibility:** Should the GitHub repository be public or private?

Validate that:
- Category is valid (one of the 8 categories)
- Repository name follows naming convention (`coditect-{category}-{name}`)
- Repository name uses kebab-case (lowercase with hyphens)

### Step 2: Verify Parent Directory and Prerequisites

Before creating the submodule, verify:
- Current working directory is the rollout-master root (check for `.coditect` directory)
- Category directory exists at `submodules/{category}/` (create if missing)
- GitHub CLI (`gh`) is installed and authenticated (run `gh auth status`)
- Git is configured with user name and email

Use Bash tool to check these prerequisites. If any are missing, provide clear instructions to the user.

### Step 3: Create Submodule Directory Structure

Create the submodule directory and establish symlink chains:

```bash
# Create category directory if doesn't exist
mkdir -p submodules/{category}

# Create submodule directory
mkdir -p submodules/{category}/{repo-name}

# Navigate to submodule
cd submodules/{category}/{repo-name}

# Create symlink chains
ln -s ../../../.coditect .coditect
ln -s .coditect .claude

# Verify symlinks work
ls .coditect/agents/ | wc -l  # Should show 50+
```

Verify the symlinks are functional before proceeding.

### Step 4: Generate Project Templates

Create the initial project files from templates:

**README.md:**
- Use `.coditect/skills/submodule-setup/templates/README.template.md` if it exists
- Otherwise create a basic README with:
  - Submodule name and purpose
  - Getting started instructions
  - Link to PROJECT-PLAN.md and TASKLIST.md
  - CODITECT distributed intelligence explanation

**PROJECT-PLAN.md:**
- Use `.coditect/skills/submodule-setup/templates/PROJECT-PLAN.template.md` if it exists
- Replace template variables with actual values
- Include standard phases: Foundation, Implementation, Integration, Launch
- Customize for submodule-specific goals

**TASKLIST.md:**
- Create with checkbox format
- Include initial setup tasks (most already completed)
- Add placeholder tasks for next development phases

**.gitignore:**
- Copy from template or create standard exclusions:
  - Dependencies (node_modules/, venv/, __pycache__/)
  - Build outputs (dist/, build/, *.pyc)
  - IDE (.vscode/, .idea/)
  - OS (.DS_Store, Thumbs.db)
  - Environment (.env, .env.local)

### Step 5: Initialize Git Repository

Set up git repository in the submodule:

```bash
git init
git checkout -b main
git add .
git commit -m "Initial commit: CODITECT submodule setup

- Established .coditect and .claude symlinks for distributed intelligence
- Created PROJECT-PLAN.md with phased implementation
- Created TASKLIST.md with checkbox progress tracking
- Created README.md with getting started guide
- Added .gitignore with standard exclusions

Generated with CODITECT framework
"
```

### Step 6: Create GitHub Repository

Use GitHub CLI to create the repository:

```bash
# Create repository in coditect-ai organization
gh repo create coditect-ai/{repo-name} \
  --{visibility} \
  --description "{purpose}" \
  --homepage "https://coditect.ai"

# Add topics for discoverability
gh repo edit coditect-ai/{repo-name} \
  --add-topic coditect \
  --add-topic {category}
```

### Step 7: Configure Git Remote and Push

Link local repository to GitHub and push:

```bash
git remote add origin https://github.com/coditect-ai/{repo-name}.git
git push -u origin main
```

Verify the push was successful.

### Step 8: Register Submodule with Parent Repository

Return to rollout-master root and register the submodule:

```bash
cd ../../..

# Add submodule to parent repository
git submodule add https://github.com/coditect-ai/{repo-name}.git submodules/{category}/{repo-name}

# Verify submodule registered
git status
grep {repo-name} .gitmodules

# Commit submodule addition
git add .gitmodules submodules/{category}/{repo-name}
git commit -m "Add {category}/{repo-name} submodule

{purpose}

Generated with CODITECT framework
"
```

### Step 9: Run Verification Checks

Verify the submodule setup is complete and correct:

```bash
# Navigate to submodule
cd submodules/{category}/{repo-name}

# Run validation checks
ls -la .coditect  # Should show symlink
ls .coditect/agents/ | wc -l  # Should show 50+
ls PROJECT-PLAN.md TASKLIST.md README.md  # Should all exist
git remote -v  # Should show GitHub remote
git status  # Should be clean

# Return to parent
cd ../../..

# Check parent integration
git submodule status | grep {repo-name}
```

Use the `submodule-validation` skill for comprehensive verification.

### Step 10: Provide Next Steps

Inform the user that setup is complete and provide next steps:

1. **Customize PROJECT-PLAN.md** - Update with specific project phases and tasks
2. **Add tasks to TASKLIST.md** - Break down work into actionable tasks
3. **Start development** - Begin implementing the submodule
4. **Push changes** - Regularly commit and push to GitHub
5. **Update parent** - When submodule progresses, update parent repository reference

Provide the path to the new submodule: `submodules/{category}/{repo-name}`

## Important notes:

- **Symlinks are critical** - Verify they work before proceeding with other steps
- **Follow naming conventions** - All repository names must follow `coditect-{category}-{name}` pattern
- **Test each step** - Don't skip verification steps; catch errors early
- **Clean up on failure** - If setup fails partway, remove partial state before retrying
- **Use TodoWrite** - For complex operations, track progress with checkboxes
- **Commit atomically** - Each git commit should be a logical unit of work
- **Document decisions** - Note any deviations from standard setup in PROJECT-PLAN.md
- **Verify GitHub permissions** - Ensure you have write access to coditect-ai organization
- **Handle errors gracefully** - Provide clear error messages and recovery instructions
- **Preserve context** - Use MEMORY-CONTEXT exports for session continuity if needed

## Success criteria:

- [ ] Submodule directory created at correct location
- [ ] Symlinks `.coditect` and `.claude` functional
- [ ] All template files generated (README, PROJECT-PLAN, TASKLIST, .gitignore)
- [ ] Git repository initialized and committed
- [ ] GitHub repository created with correct visibility and topics
- [ ] Remote configured and initial push successful
- [ ] Submodule registered in parent .gitmodules
- [ ] All verification checks pass
- [ ] User knows next steps to take
