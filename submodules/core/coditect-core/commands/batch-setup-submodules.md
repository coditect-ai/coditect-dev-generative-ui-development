# Batch Setup Submodules

Set up multiple CODITECT submodules at once from a configuration file or list. This command automates the creation of multiple repositories simultaneously, maintaining consistency and saving time.

## Steps to follow:

### Step 1: Gather Batch Configuration

Ask the user how they want to provide the submodule list:
- **Configuration file:** Path to YAML/JSON file with submodule definitions
- **Interactive list:** Enter submodules one by one
- **Category batch:** Create all submodules for a specific category from plan

**Configuration file format (YAML):**
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

If using configuration file, read and parse it. If interactive, collect information for each submodule.

### Step 2: Validate Batch Configuration

Before starting batch setup, validate all submodule definitions:
- All categories are valid (cloud, dev, gtm, labs, docs, ops, market, core)
- All repository names follow `coditect-{category}-{name}` convention
- All names use kebab-case
- No duplicate names
- Visibility is either 'public' or 'private'

Report validation results and ask user to confirm before proceeding.

### Step 3: Verify Prerequisites

Check that all prerequisites are met for batch operation:

```bash
# Check in rollout-master root
test -d .coditect

# Check GitHub CLI
gh auth status

# Check git configuration
git config user.name
git config user.email

# Check disk space (estimate needed space)
df -h .
```

If any prerequisite fails, stop and provide instructions to fix.

### Step 4: Create Execution Plan

Show the user what will be created:

```
Batch Setup Plan
================
Total submodules: {count}

Submodules to create:
1. cloud/coditect-cloud-gateway (public)
   Purpose: API gateway for cloud services

2. dev/coditect-dev-logger (private)
   Purpose: Centralized logging utility

3. ...

Estimated time: {estimate} minutes
Estimated disk space: {estimate} MB

Continue with batch setup? (y/N)
```

Wait for user confirmation before proceeding.

### Step 5: Execute Batch Setup

For each submodule in the list, execute setup using the `setup-submodule` command logic:

Use TodoWrite to track progress:
```json
[
  {"content": "Setup cloud/coditect-cloud-gateway", "status": "in_progress", "activeForm": "Setting up cloud/coditect-cloud-gateway"},
  {"content": "Setup dev/coditect-dev-logger", "status": "pending", "activeForm": "Setting up dev/coditect-dev-logger"},
  ...
]
```

For each submodule:
1. Create directory structure and symlinks
2. Generate templates (README, PROJECT-PLAN, TASKLIST, .gitignore)
3. Initialize git repository
4. Create GitHub repository
5. Configure remote and push
6. Register with parent repository

If any step fails for a submodule:
- Log the error
- Mark that submodule as failed
- Continue with remaining submodules
- Collect failed submodules for retry later

Update TodoWrite after each submodule completes.

### Step 6: Create GitHub Repositories in Batch

Use GitHub CLI batch operations where possible:

```bash
# Create repositories (can be done in parallel)
for submodule in "${submodules[@]}"; do
  gh repo create "coditect-ai/${submodule[name]}" \
    --${submodule[visibility]} \
    --description "${submodule[purpose]}" \
    --homepage "https://coditect.ai" &
done

# Wait for all repository creations to complete
wait

# Add topics to each repository
for submodule in "${submodules[@]}"; do
  gh repo edit "coditect-ai/${submodule[name]}" \
    --add-topic coditect \
    --add-topic ${submodule[category]}
done
```

### Step 7: Update Parent Repository

After all submodules are created, update parent repository:

```bash
# Add all new submodules to parent
for submodule in "${completed_submodules[@]}"; do
  git submodule add "https://github.com/coditect-ai/${submodule[name]}.git" \
    "submodules/${submodule[category]}/${submodule[name]}"
done

# Commit all submodule additions
git add .gitmodules submodules/
git commit -m "Batch add submodules: $(date +%Y-%m-%d)

Added ${count} new submodules:
${list_of_submodules}

Generated with CODITECT batch-setup-submodules command
"

git push
```

### Step 8: Run Verification

After batch setup completes, run verification on all newly created submodules:

```bash
for submodule in "${completed_submodules[@]}"; do
  echo "Verifying ${submodule[name]}..."
  # Use verify-submodule logic for each
done
```

Collect verification results and report any issues.

### Step 9: Generate Batch Setup Report

Create comprehensive report of batch operation:

```markdown
# Batch Submodule Setup Report
**Date:** {date}
**Total Requested:** {count}
**Successful:** {success_count}
**Failed:** {failed_count}
**Duration:** {duration}

## Successfully Created
{list with checkboxes}

## Failed Submodules
{list with error reasons}

## Verification Results
{summary of verification for successful submodules}

## Next Steps
1. Review any failed submodules and retry manually
2. Customize PROJECT-PLAN.md for each new submodule
3. Add initial tasks to TASKLIST.md
4. Begin development work
```

Save this report to `BATCH-SETUP-REPORT-{date}.md` in rollout-master root.

### Step 10: Provide Retry Instructions

For any failed submodules, provide instructions for retry:

**If failed during directory creation:**
- Check permissions and disk space
- Ensure category directory exists
- Retry with `/setup-submodule` for individual submodule

**If failed during GitHub creation:**
- Check GitHub authentication: `gh auth status`
- Verify organization permissions
- Check if repository name already exists
- Retry GitHub creation manually: `gh repo create ...`

**If failed during git operations:**
- Check git configuration
- Verify network connectivity
- Check SSH keys or HTTPS credentials
- Retry git operations manually

Allow user to retry failed submodules or continue with successful ones.

## Important notes:

- **Use TodoWrite to track progress** - Critical for batch operations to show real-time status
- **Handle failures gracefully** - One failure shouldn't stop entire batch
- **Collect all errors** - Report all failures at the end for batch remediation
- **Verify prerequisites first** - Don't start batch if prerequisites aren't met
- **Estimate time accurately** - Each submodule takes ~2-3 minutes
- **Respect rate limits** - GitHub API has rate limits; add delays if needed
- **Atomic operations per submodule** - Each submodule is independent unit
- **Rollback on total failure** - If everything fails, consider cleanup
- **Save batch configuration** - Keep configuration file for reproducibility
- **Parallel where safe** - GitHub repository creation can be parallel
- **Serial where needed** - Git commits must be serial
- **Validate before execution** - Catch errors in planning phase
- **Report progress continuously** - User should see what's happening
- **Preserve logs** - Keep detailed logs for troubleshooting

## Success criteria:

- [ ] All submodule definitions validated
- [ ] Prerequisites verified before starting
- [ ] Execution plan shown and confirmed
- [ ] Progress tracked with TodoWrite
- [ ] Each successful submodule has:
  - [ ] Directory structure created
  - [ ] Symlinks functional
  - [ ] Templates generated
  - [ ] Git repository initialized
  - [ ] GitHub repository created
  - [ ] Remote configured and pushed
  - [ ] Registered in parent .gitmodules
- [ ] Failed submodules logged with errors
- [ ] Verification run on successful submodules
- [ ] Batch report generated
- [ ] Retry instructions provided for failures
- [ ] Parent repository committed and pushed
