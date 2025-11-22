# Verify Submodule

Run comprehensive verification checks on a CODITECT submodule to ensure it's correctly configured with symlinks, templates, git integration, and framework accessibility. This command validates post-setup correctness or troubleshoots existing submodules.

## Steps to follow:

### Step 1: Identify Submodule to Verify

Ask the user which submodule to verify:
- **Path to submodule:** Either relative path from rollout-master root (e.g., `submodules/cloud/coditect-cloud-backend`) or absolute path
- **Verification type:** Quick check or comprehensive validation

If no path provided, ask if they want to verify all submodules or a specific category.

### Step 2: Navigate to Submodule

Change to the submodule directory:

```bash
cd {submodule-path}
```

Verify the directory exists and contains expected structure. If directory doesn't exist, report error and exit.

### Step 3: Verify Symlink Integrity

Check that symlink chains are correctly established:

```bash
# Check .coditect symlink exists
ls -la .coditect

# Verify it points to correct target
readlink .coditect  # Should show: ../../../.coditect

# Check .claude symlink exists
ls -la .claude

# Verify it points to .coditect
readlink .claude  # Should show: .coditect

# Test symlinks are accessible
ls .coditect/agents/ | wc -l  # Should show 50+
ls .coditect/skills/ | wc -l  # Should show 24+
ls .coditect/commands/ | wc -l  # Should show 74+
```

Report status:
- ✅ If all checks pass: "Symlinks verified - distributed intelligence accessible"
- ❌ If any check fails: "Symlink issue detected" with specific error
- Provide fix command if broken (e.g., `ln -sf ../../../.coditect .coditect`)

### Step 4: Verify Template Files

Check that required project templates exist and have content:

```bash
# Check files exist
ls PROJECT-PLAN.md TASKLIST.md README.md .gitignore

# Check files have content (not empty)
wc -l PROJECT-PLAN.md  # Should have > 10 lines
wc -l TASKLIST.md      # Should have > 5 lines
wc -l README.md        # Should have > 10 lines
wc -l .gitignore       # Should have > 5 lines
```

For each file, report:
- ✅ If exists and has content: "Template verified"
- ⚠️  If exists but seems empty: "Template exists but may need content"
- ❌ If missing: "Template missing" with creation instructions

Use Read tool to check file structure:
- PROJECT-PLAN.md should have "## Phases" or similar structure
- TASKLIST.md should have checkbox format `- [ ]` or `- [x]`
- README.md should mention the submodule name
- .gitignore should have standard exclusions

### Step 5: Verify Git Configuration

Check git repository setup and remote configuration:

```bash
# Check .git directory exists
ls -la .git

# Check git remote configured
git remote -v

# Verify remote is GitHub coditect-ai repository
git remote get-url origin  # Should contain github.com/coditect-ai/

# Check current branch
git branch --show-current

# Check git status
git status

# Check if there are uncommitted changes
git diff --stat
git diff --cached --stat

# Check if there are unpushed commits
git log @{u}.. --oneline 2>/dev/null || echo "No upstream configured"
```

Report findings:
- ✅ Git repository initialized
- ✅ Remote 'origin' configured to GitHub
- ✅ On main branch
- ⚠️  Uncommitted changes detected (list files)
- ⚠️  Unpushed commits detected (show count)
- ❌ No remote configured (provide setup command)

### Step 6: Verify Parent Repository Integration

Return to parent repository and check submodule registration:

```bash
cd ../../..  # Return to rollout-master root

# Check .gitmodules contains this submodule
grep "{repo-name}" .gitmodules

# Check git recognizes the submodule
git submodule status | grep "{repo-name}"

# Check submodule is at correct commit
cd {submodule-path}
git log -1 --oneline
cd ../../..
```

Report integration status:
- ✅ Submodule registered in .gitmodules
- ✅ Git submodule status shows correct commit
- ⚠️  Parent repository has uncommitted submodule reference changes
- ❌ Submodule not in .gitmodules (provide registration command)

### Step 7: Run Framework Accessibility Tests

Verify CODITECT framework is fully accessible through symlinks:

```bash
cd {submodule-path}

# Count agents
agent_count=$(ls .coditect/agents/*.md 2>/dev/null | wc -l)
echo "Agents accessible: $agent_count"

# Count skills
skill_count=$(ls -d .coditect/skills/*/ 2>/dev/null | wc -l)
echo "Skills accessible: $skill_count"

# Count commands
command_count=$(ls .coditect/commands/*.md 2>/dev/null | wc -l)
echo "Commands accessible: $command_count"

# Check STANDARDS.md accessible
ls .coditect/STANDARDS.md
```

Expected counts:
- Agents: 50+ files
- Skills: 24+ directories
- Commands: 74+ files

Report:
- ✅ All framework components accessible
- ❌ Framework not accessible (symlink issue)

### Step 8: Generate Verification Report

Create a comprehensive verification report:

```markdown
# Submodule Verification Report
**Submodule:** {repo-name}
**Path:** {submodule-path}
**Date:** {current-date}
**Verification Type:** {quick/comprehensive}

## Results Summary
**Overall Status:** {✅ Passed / ⚠️ Warnings / ❌ Failed}
**Total Checks:** {count}
**Passed:** {count}
**Warnings:** {count}
**Failed:** {count}

## Symlink Checks
- [ ] .coditect symlink exists
- [ ] .coditect points to ../../../.coditect
- [ ] .coditect is accessible
- [ ] .claude symlink exists
- [ ] .claude points to .coditect
- [ ] Agents accessible (50+ files)
- [ ] Skills accessible (24+ directories)
- [ ] Commands accessible (74+ files)

## Template Checks
- [ ] PROJECT-PLAN.md exists and has content
- [ ] TASKLIST.md exists with checkbox format
- [ ] README.md exists with description
- [ ] .gitignore exists with exclusions

## Git Configuration Checks
- [ ] Git repository initialized
- [ ] Remote 'origin' configured
- [ ] Remote URL is GitHub coditect-ai
- [ ] On main branch
- [ ] No uncommitted changes (or list them)
- [ ] No unpushed commits (or list them)

## Parent Integration Checks
- [ ] Entry in parent .gitmodules
- [ ] Git submodule status shows correct commit
- [ ] Parent repository aware of submodule

## Issues Found
{list any issues with severity: Critical, Warning, Info}

## Recommendations
{list recommended actions to fix issues}

## Next Steps
{suggested next steps based on findings}
```

Display this report to the user.

### Step 9: Provide Remediation Guidance

For each issue found, provide specific remediation commands:

**Broken symlink:**
```bash
cd {submodule-path}
rm .coditect
ln -s ../../../.coditect .coditect
```

**Missing template:**
```bash
cp .coditect/skills/submodule-setup/templates/{template-name} {submodule-path}/
```

**No git remote:**
```bash
git remote add origin https://github.com/coditect-ai/{repo-name}.git
```

**Uncommitted changes:**
```bash
git add .
git commit -m "Your commit message"
```

**Not in .gitmodules:**
```bash
# From rollout-master root
git submodule add https://github.com/coditect-ai/{repo-name}.git {submodule-path}
```

### Step 10: Suggest Next Actions

Based on verification results, suggest appropriate next actions:

**If all checks passed:**
- ✅ Submodule is correctly configured
- Continue development work
- Run periodic health checks with `/submodule-status` command

**If warnings found:**
- ⚠️ Address warnings when convenient
- Review uncommitted/unpushed changes
- Update documentation if outdated

**If critical issues found:**
- ❌ Fix critical issues immediately
- Re-run verification after fixes
- Consider using `submodule-configuration` skill for systematic fixes

## Important notes:

- **Run verification after setup** - Always verify new submodule setup completed correctly
- **Use for troubleshooting** - When submodule behavior is unexpected, verify configuration
- **Regular health checks** - Periodic verification catches issues early
- **Fix issues promptly** - Don't let configuration drift accumulate
- **Document findings** - Add verification reports to submodule documentation
- **Automate verification** - Consider adding to CI/CD pipeline
- **Check before major operations** - Verify before making significant changes
- **Parent-child relationship** - Ensure parent repository recognizes submodule
- **Symlink integrity critical** - Broken symlinks break distributed intelligence
- **Batch verification** - Use `/batch-verify-submodules` for multiple submodules

## Success criteria:

- [ ] All symlink checks passed
- [ ] All template checks passed
- [ ] All git configuration checks passed
- [ ] All parent integration checks passed
- [ ] Framework fully accessible
- [ ] Verification report generated
- [ ] User understands any issues found
- [ ] Remediation guidance provided for failures
