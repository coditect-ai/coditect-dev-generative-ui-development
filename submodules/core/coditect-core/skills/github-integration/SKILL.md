---
name: github-integration
description: Automated GitHub repository creation, remote configuration, and organization management for CODITECT submodules using GitHub CLI (gh).
license: MIT
allowed-tools: Bash, Read, Write
metadata:
  token-multiplier: "12x"
  supported-languages: "Bash, GitHub CLI"
  reusability: "High - All 41+ submodules need GitHub repos"
---

## When to Use This Skill

✅ Use when:
- Creating new GitHub repository for CODITECT submodule
- Configuring git remote tracking for existing repository
- Setting up repository settings (description, topics, visibility)
- Adding repository to coditect-ai organization
- Configuring branch protection and collaboration settings

❌ Don't use when:
- Repository already exists on GitHub (use verification instead)
- Only need local git operations (use git commands directly)
- Working with non-GitHub version control (GitLab, Bitbucket)
- Need to modify existing repository settings (use GitHub web UI)

## Core Capabilities

### 1. Repository Creation via GitHub CLI
Automates GitHub repository creation using `gh` CLI:
- Creates repository in `coditect-ai` organization
- Sets description, visibility (public/private)
- Configures topics/tags for discoverability
- Initializes with README if requested
- Sets default branch (main)

### 2. Remote Configuration
Configures git remote tracking for submodule:
- Adds GitHub remote as `origin`
- Sets up tracking for main branch
- Configures push/pull defaults
- Verifies remote connectivity
- Handles SSH vs HTTPS authentication

### 3. Repository Settings Management
Configures repository settings for CODITECT standards:
- Enable/disable features (Issues, Wiki, Projects, Discussions)
- Set repository visibility
- Configure default branch
- Add topics for organization
- Set repository description

### 4. Collaboration Setup
Configures team access and collaboration:
- Add repository to organization
- Configure team permissions
- Set up branch protection rules
- Configure required reviews
- Enable status checks

## Usage Pattern

### Step 1: Verify GitHub CLI Installation
Ensure GitHub CLI is installed and authenticated:
```bash
# Check gh CLI installed
gh --version

# Check authentication
gh auth status

# If not authenticated
gh auth login
```

### Step 2: Create Repository on GitHub
Use GitHub CLI to create repository in organization:
```bash
# Create public repository
gh repo create coditect-ai/coditect-cloud-newservice \
  --public \
  --description "CODITECT cloud service for XYZ" \
  --homepage "https://coditect.ai"

# Create private repository
gh repo create coditect-ai/coditect-labs-experiment \
  --private \
  --description "Research experiment for XYZ"
```

### Step 3: Configure Local Git Remote
Add GitHub repository as remote in local submodule:
```bash
cd submodules/cloud/coditect-cloud-newservice

# Add remote
git remote add origin https://github.com/coditect-ai/coditect-cloud-newservice.git

# Verify remote
git remote -v

# Set upstream tracking
git push -u origin main
```

### Step 4: Configure Repository Settings
Set repository metadata and features:
```bash
# Add topics
gh repo edit coditect-ai/coditect-cloud-newservice \
  --add-topic coditect \
  --add-topic cloud \
  --add-topic microservices

# Update description
gh repo edit coditect-ai/coditect-cloud-newservice \
  --description "Updated description"

# Enable/disable features
gh repo edit coditect-ai/coditect-cloud-newservice \
  --enable-issues \
  --disable-wiki
```

### Step 5: Setup Branch Protection
Configure branch protection for main branch:
```bash
# Basic protection
gh api repos/coditect-ai/coditect-cloud-newservice/branches/main/protection \
  -X PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci/tests"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

## Examples

See `examples/` directory for:
- `create-repo.sh` - Create repository with standard settings
- `batch-create-repos.sh` - Create multiple repositories
- `configure-settings.sh` - Apply standard repository settings

## Templates

See `templates/` directory for:
- `.github-settings.yml` - Standard repository settings
- `.github-topics.txt` - Standard topics by category
- `branch-protection.json` - Branch protection configuration

## Integration Points

**Works with:**
- `submodule-setup` skill - Complete submodule initialization
- `submodule-validation` skill - Verify GitHub configuration
- GitHub CLI (`gh`) - Primary automation tool

**Prerequisites:**
- GitHub CLI installed (`brew install gh` or equivalent)
- Authenticated to GitHub (`gh auth login`)
- Member of `coditect-ai` organization with repo creation permissions

## Success Criteria

GitHub integration complete when:
- [ ] Repository created on GitHub in `coditect-ai` organization
- [ ] Local git remote configured to GitHub repository
- [ ] Initial commit pushed to GitHub
- [ ] Repository settings configured (description, topics, visibility)
- [ ] Branch protection enabled on main branch
- [ ] Repository visible in organization dashboard

## Common Issues

**GitHub CLI not installed:**
```bash
# macOS
brew install gh

# Linux
sudo apt install gh  # or equivalent for your distro

# Windows
winget install GitHub.cli
```

**Authentication failed:**
```bash
# Re-authenticate
gh auth logout
gh auth login

# Check status
gh auth status
```

**Organization permission denied:**
- Ensure you're member of `coditect-ai` organization
- Check with organization owner to grant repository creation permissions
- Verify organization membership: `gh api user/memberships/orgs`

**Repository already exists:**
```bash
# Check if repository exists
gh repo view coditect-ai/repo-name

# If exists, use existing repo
git remote add origin https://github.com/coditect-ai/repo-name.git
```

## Security Considerations

**Repository Visibility:**
- **Public:** Open source, documentation, examples
- **Private:** Proprietary code, internal tools, research

**Access Control:**
- Use organization teams for access management
- Apply least-privilege principle
- Require 2FA for organization members
- Enable branch protection on main branches

**Secrets Management:**
- Never commit secrets to repository
- Use GitHub Secrets for CI/CD
- Rotate tokens regularly
- Audit access logs

## Advanced Usage

### Batch Repository Creation
Create multiple repositories from configuration file:
```bash
# Read from repos.txt
while IFS=',' read -r name description topics; do
  gh repo create "coditect-ai/$name" \
    --public \
    --description "$description"

  # Add topics
  for topic in $(echo "$topics" | tr '|' ' '); do
    gh repo edit "coditect-ai/$name" --add-topic "$topic"
  done
done < repos.txt
```

### Repository Templates
Create new repositories from template:
```bash
# Use existing repo as template
gh repo create coditect-ai/new-service \
  --template coditect-ai/service-template \
  --public
```

### Automated Settings Sync
Keep repository settings synchronized:
```bash
# Export settings from template repo
gh api repos/coditect-ai/template/topics > template-topics.json

# Apply to new repos
gh api repos/coditect-ai/new-repo/topics \
  -X PUT \
  --input template-topics.json
```

## Related Skills

- **submodule-setup** - Initialize submodule directory structure
- **submodule-validation** - Verify GitHub integration
- **submodule-configuration** - Manage repository configuration

## Related Agents

- **submodule-orchestrator** - Coordinates all submodule operations

## GitHub CLI Reference

**Common Commands:**
```bash
# Repository operations
gh repo create <owner>/<repo>      # Create repository
gh repo view <owner>/<repo>        # View repository
gh repo edit <owner>/<repo>        # Edit settings
gh repo delete <owner>/<repo>      # Delete repository

# Remote operations
gh repo clone <owner>/<repo>       # Clone repository
gh repo fork <owner>/<repo>        # Fork repository

# Settings
gh repo edit --add-topic <topic>   # Add topic
gh repo edit --description <desc>  # Update description
gh repo edit --visibility <vis>    # Change visibility
```

**API Access:**
```bash
# Raw API calls
gh api repos/<owner>/<repo>        # Get repository info
gh api repos/<owner>/<repo>/topics # Get topics
gh api -X PUT ...                  # Update settings
```
