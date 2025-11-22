# Submodule Status

Generate comprehensive health status report for CODITECT submodules including git status, symlink integrity, update tracking, and ecosystem-wide dashboard. This command provides ongoing monitoring and health checks for operational submodules.

## Steps to follow:

### Step 1: Determine Scope

Ask the user what scope they want to check:
- **All submodules:** Generate ecosystem-wide status report for all 41+ submodules
- **Specific category:** Check all submodules in one category (cloud, dev, gtm, etc.)
- **Single submodule:** Detailed status for one specific submodule
- **Recent changes:** Only submodules with recent activity or changes

Based on their choice, set the scope for status checking.

### Step 2: Collect Git Status Information

For each submodule in scope, collect git status:

```bash
cd {submodule-path}

# Check for uncommitted changes
uncommitted=$(git status --porcelain | wc -l)

# Check for unpushed commits
unpushed=$(git log @{u}.. --oneline 2>/dev/null | wc -l)

# Check branch
branch=$(git branch --show-current)

# Check if behind remote
git fetch origin --quiet
behind=$(git log ..@{u} --oneline 2>/dev/null | wc -l)

# Check if ahead of remote
ahead=$(git log @{u}.. --oneline 2>/dev/null | wc -l)

# Check last commit date
last_commit=$(git log -1 --format=%cd --date=relative)

# Check detached HEAD
detached=$(git symbolic-ref -q HEAD || echo "detached")
```

Store this information for each submodule.

### Step 3: Check Symlink Health

Verify symlink integrity for each submodule:

```bash
cd {submodule-path}

# Check .coditect symlink
if [ -L .coditect ]; then
  if [ -e .coditect ]; then
    symlink_status="✅ OK"
  else
    symlink_status="❌ Broken"
  fi
else
  symlink_status="❌ Missing"
fi

# Verify framework accessibility
if [ -d .coditect/agents ]; then
  agent_count=$(ls .coditect/agents/*.md 2>/dev/null | wc -l)
  framework_access="✅ OK ($agent_count agents)"
else
  framework_access="❌ Not accessible"
fi
```

### Step 4: Calculate Health Score

For each submodule, calculate a health score (0-100):

**Scoring factors:**
- Git status clean (no uncommitted changes): +20 points
- No unpushed commits: +20 points
- Branch synchronized with remote: +15 points
- On main branch: +10 points
- Symlinks functional: +15 points
- Framework accessible: +10 points
- Recent activity (commit in last week): +10 points

**Deductions:**
- Uncommitted changes: -5 per file (max -20)
- Unpushed commits: -5 per commit (max -20)
- Behind remote: -10
- Detached HEAD: -15
- Broken symlink: -20
- Framework not accessible: -20

Calculate final score and categorize:
- 90-100: Excellent ✅
- 70-89: Good ✅
- 50-69: Fair ⚠️
- 0-49: Poor ❌

### Step 5: Generate Status Dashboard

Create a comprehensive status dashboard:

```markdown
# CODITECT Submodule Status Dashboard
**Generated:** {timestamp}
**Scope:** {all/category/single}

## Overview
Total Submodules: {count}
Average Health Score: {avg_score}/100

Health Distribution:
- Excellent (90-100): {count} ({percentage}%)
- Good (70-89): {count} ({percentage}%)
- Fair (50-69): {count} ({percentage}%)
- Poor (0-49): {count} ({percentage}%)

## Category Summary
{for each category}
### {category} ({count} submodules)
Average Score: {score}/100
Status: {emoji}

{table of submodules in category}

## Critical Issues
{list submodules with score < 50}

## Warnings
{list submodules with score 50-69}

## Recent Activity
{list submodules with commits in last 7 days}

## Stale Submodules
{list submodules with no commits in last 30 days}
```

### Step 6: Create Detailed Submodule Reports

For each submodule (or single if scope is specific), create detailed status card:

```markdown
### {submodule-name}
**Score:** {score}/100 {emoji}
**Category:** {category}
**Last Activity:** {relative-time}

**Git Status:**
- Branch: {branch}
- Uncommitted: {count} files
- Unpushed: {count} commits
- Behind Remote: {count} commits
- Ahead of Remote: {count} commits

**Symlink Health:**
- .coditect: {status}
- .claude: {status}
- Framework Access: {status}

**Issues:**
{list any issues found}

**Recommendations:**
{list recommended actions}
```

### Step 7: Identify Actionable Items

Extract actionable items across all checked submodules:

**High Priority (do today):**
- Broken symlinks (blocks distributed intelligence)
- Detached HEAD (risky state)
- Significant uncommitted changes (risk of loss)

**Medium Priority (do this week):**
- Unpushed commits (not backed up to GitHub)
- Behind remote (missing updates)
- Fair health scores (needs attention)

**Low Priority (do when convenient):**
- Stale submodules (no recent activity)
- Minor uncommitted changes
- Documentation updates needed

Present prioritized action list to user.

### Step 8: Generate Trend Analysis

If previous status reports exist, compare to show trends:

```markdown
## Trend Analysis
Compared to last status check ({date}):

**Improvements:**
- {submodule}: Score improved from {old} to {new}
- {count} submodules with reduced uncommitted changes
- {count} submodules pushed pending commits

**Regressions:**
- {submodule}: Score decreased from {old} to {new}
- {count} new broken symlinks
- {count} submodules now behind remote

**New Issues:**
- {list new issues since last check}

**Resolved Issues:**
- {list issues that were fixed}
```

### Step 9: Save Status Report

Save the complete status report to file:

```bash
# Create reports directory if doesn't exist
mkdir -p .coditect/reports/submodule-status

# Save with timestamp
report_file=".coditect/reports/submodule-status/status-$(date +%Y-%m-%d-%H%M%S).md"
echo "{status_report}" > "$report_file"

echo "Status report saved to: $report_file"
```

Optionally commit the report to git for historical tracking.

### Step 10: Provide Next Steps

Based on the status findings, suggest next steps:

**If all excellent:**
- ✅ Ecosystem is healthy
- Continue regular development
- Schedule next status check in 1 week

**If critical issues found:**
- ❌ Fix critical issues immediately
- Run `/verify-submodule` on affected submodules
- Re-run status check after fixes

**If warnings found:**
- ⚠️ Address warnings during maintenance window
- Commit and push pending changes
- Update submodules behind remote

**If stale submodules:**
- 📊 Review if submodules are still active
- Archive or remove abandoned submodules
- Update documentation for inactive projects

Provide specific commands for common fixes (commit, push, update, fix symlink).

## Important notes:

- **Run regularly** - Schedule weekly status checks to catch issues early
- **Track trends** - Compare reports over time to identify patterns
- **Fix critical issues first** - Broken symlinks and detached HEADs need immediate attention
- **Automate monitoring** - Consider adding to CI/CD for continuous monitoring
- **Share reports** - Keep team informed of ecosystem health
- **Use for planning** - Status reports inform maintenance priorities
- **Check before major operations** - Always check status before batch operations
- **Preserve history** - Keep historical reports to track improvements
- **Context awareness** - Health scores consider multiple factors, not just git status
- **Customizable thresholds** - Adjust health score criteria for your needs
- **Integration ready** - Can feed into dashboards and monitoring systems
- **Actionable output** - Reports should lead to clear next steps

## Success criteria:

- [ ] Status collected for all submodules in scope
- [ ] Git status checked for each submodule
- [ ] Symlink health verified for each submodule
- [ ] Health scores calculated correctly
- [ ] Dashboard generated with overview
- [ ] Detailed reports created for each submodule
- [ ] Actionable items identified and prioritized
- [ ] Trend analysis included (if historical data available)
- [ ] Report saved to file
- [ ] User provided with clear next steps
- [ ] Critical issues highlighted prominently
