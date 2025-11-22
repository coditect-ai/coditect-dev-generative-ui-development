---
name: submodule-health
description: Ongoing health monitoring and status reporting for CODITECT submodules including git status, symlink integrity, update tracking, and ecosystem-wide dashboards.
license: MIT
allowed-tools: Bash, Read, Grep, Glob
metadata:
  token-multiplier: "12x"
  supported-languages: "Bash, Python"
  reusability: "High - Run regularly for monitoring"
---

## When to Use This Skill

✅ Use when:
- Monitoring health of operational submodules
- Generating status reports for all 41+ submodules
- Tracking git synchronization across ecosystem
- Identifying outdated or broken submodules
- Creating health dashboards and metrics

❌ Don't use when:
- Initial submodule setup (use `submodule-setup`)
- Post-setup verification (use `submodule-validation`)
- Making configuration changes (use `submodule-configuration`)
- Debugging specific issues (use targeted troubleshooting)

## Core Capabilities

### 1. Git Status Monitoring
Tracks git status across all submodules:
- Uncommitted changes detection
- Unpushed commits identification
- Branch synchronization with remote
- Detached HEAD warnings
- Merge conflict detection
- Stale branches identification

### 2. Symlink Health Checks
Verifies symlink integrity across ecosystem:
- Broken symlink detection
- Symlink accessibility validation
- Framework connectivity verification
- Performance impact assessment
- Automatic repair suggestions

### 3. Update Tracking
Monitors submodule update status:
- Parent repository submodule references
- Local vs remote version comparison
- Pending updates identification
- Update history tracking
- Dependency version tracking

### 4. Dashboard Generation
Creates comprehensive health dashboards:
- Ecosystem-wide status overview
- Per-category health summaries
- Individual submodule health cards
- Trend analysis and metrics
- Alert and warning aggregation

## Usage Pattern

### Step 1: Run Health Check
Execute health check across all or specific submodules:
```bash
# All submodules
.coditect/scripts/submodule-health-check.py --all

# Specific category
.coditect/scripts/submodule-health-check.py --category cloud

# Single submodule
.coditect/scripts/submodule-health-check.py --path submodules/cloud/coditect-cloud-backend
```

### Step 2: Review Health Report
Analyze the generated health report:
- ✅ Healthy - No issues detected
- ⚠️  Warning - Minor issues or recommendations
- ❌ Critical - Major issues requiring attention
- 📊 Metrics - Health scores and trends

### Step 3: Investigate Issues
For any warnings or critical issues, investigate:
```bash
# Check specific submodule
cd submodules/cloud/problematic-service

# Check git status
git status
git log -5

# Check symlinks
ls -la .coditect
ls .coditect/agents/ | wc -l

# Check remote sync
git fetch
git status
```

### Step 4: Fix Issues
Apply fixes for detected issues:
- Commit uncommitted changes
- Push unpushed commits
- Fix broken symlinks
- Update submodule references
- Resolve conflicts

### Step 5: Verify Fixes
Re-run health check to confirm fixes:
```bash
.coditect/scripts/submodule-health-check.py --path submodules/cloud/fixed-service
```

## Health Check Categories

### Git Health
- **Uncommitted Changes:** Files modified but not committed
- **Unpushed Commits:** Commits not pushed to remote
- **Branch Sync:** Local branch behind/ahead of remote
- **Detached HEAD:** Not on a branch
- **Conflicts:** Merge conflicts present

### Symlink Health
- **Broken Links:** Symlinks pointing to non-existent targets
- **Inaccessible:** Symlinks exist but target not readable
- **Missing Links:** Required symlinks not present
- **Performance:** Symlink resolution time

### Update Health
- **Outdated:** Submodule reference older than remote
- **Diverged:** Local and remote have diverged
- **Stale:** No updates in extended period
- **Version Mismatch:** Dependency versions inconsistent

### Operational Health
- **Build Status:** CI/CD build passing/failing
- **Test Coverage:** Test coverage percentage
- **Documentation:** Documentation up to date
- **Activity:** Recent commit activity

## Health Scoring

**100-90: Excellent**
- All checks passing
- No warnings
- Recent activity
- Up to date

**89-70: Good**
- Minor warnings
- Generally healthy
- Some maintenance needed
- Acceptable state

**69-50: Fair**
- Multiple warnings
- Attention recommended
- Maintenance overdue
- Requires action soon

**49-0: Poor**
- Critical issues
- Immediate action required
- Multiple failures
- Broken state

## Dashboard Format

```
CODITECT Submodule Health Dashboard
Generated: 2025-11-21 10:30:00

=== Overview ===
Total Submodules: 41
Healthy: 35 (85%)
Warnings: 4 (10%)
Critical: 2 (5%)
Average Health Score: 87/100

=== Category Summary ===
cloud (4 submodules): 92/100 ✅
dev (9 submodules): 88/100 ✅
gtm (6 submodules): 75/100 ⚠️
labs (11 submodules): 82/100 ✅
docs (5 submodules): 90/100 ✅
ops (3 submodules): 85/100 ✅
market (2 submodules): 65/100 ⚠️
core (3 submodules): 95/100 ✅

=== Critical Issues ===
1. submodules/market/coditect-market-agents
   - ❌ 15 uncommitted changes
   - ❌ Broken .coditect symlink
   - Score: 45/100

2. submodules/gtm/coditect-gtm-crm
   - ❌ 3 unpushed commits
   - ⚠️  5 days behind remote
   - Score: 48/100

=== Recommendations ===
1. Fix broken symlinks in 2 submodules
2. Commit and push pending changes in 4 submodules
3. Update 3 submodules to latest remote
4. Review stale branches in 2 submodules
```

## Examples

See `examples/` directory for:
- `quick-health-check.sh` - Fast health check
- `detailed-health-report.py` - Comprehensive report
- `health-dashboard.sh` - Generate dashboard
- `fix-common-issues.sh` - Auto-fix common problems

## Templates

See `templates/` directory for:
- `health-report.md` - Standard report format
- `dashboard.html` - HTML dashboard template
- `alerts.json` - Alert configuration

## Monitoring Schedule

**Daily:**
- Quick health check across all submodules
- Email summary of critical issues

**Weekly:**
- Comprehensive health report
- Trend analysis
- Dashboard update

**Monthly:**
- Full ecosystem audit
- Performance metrics
- Optimization recommendations

## Integration Points

**Works with:**
- `submodule-validation` skill - Validation checks
- CI/CD systems - Build and test status
- Monitoring tools - Metrics and alerts

**Used by:**
- `submodule-orchestrator` agent - Health monitoring
- DevOps dashboards - Status visualization

## Automation

### Scheduled Health Checks
```bash
# Add to crontab for daily checks
0 9 * * * cd /path/to/rollout-master && .coditect/scripts/submodule-health-check.py --all --email
```

### CI/CD Integration
```yaml
# GitHub Actions workflow
name: Submodule Health Check
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: .coditect/scripts/submodule-health-check.py --all --ci
```

## Related Skills

- **submodule-validation** - Post-setup verification
- **submodule-configuration** - Configuration management
- **submodule-setup** - Initial setup

## Related Agents

- **submodule-orchestrator** - Coordinates health monitoring
