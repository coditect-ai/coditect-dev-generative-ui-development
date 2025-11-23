# GitHub Projects Board Setup - Phase 1 Production Readiness

**Project Name:** CODITECT Core - Phase 1 Production Readiness
**Duration:** 2 weeks (Nov 25 - Dec 6, 2025)
**Team:** 3 people (2 Developers + 1 DevOps)
**Total Issues:** 32 tasks across 4 workstreams

---

## Quick Start

### Option 1: Automated Setup (GitHub CLI)

```bash
# Install GitHub CLI if needed
brew install gh  # macOS
# or: sudo apt install gh  # Linux

# Authenticate
gh auth login

# Create project
gh project create \
  --title "Phase 1 - Production Readiness" \
  --owner coditect-ai \
  --body "2-week sprint to complete P0 blockers for production launch"

# Get project number (will be shown in output)
# Example: https://github.com/orgs/coditect-ai/projects/1
# Project number is: 1
```

### Option 2: Manual Setup (GitHub Web UI)

Follow the step-by-step guide below.

---

## Step-by-Step Web UI Setup

### 1. Create New Project

**Navigate to:**
https://github.com/orgs/coditect-ai/projects?type=beta

**Click:** "New project" button

**Choose:** "Board" template

**Configure:**
- **Project name:** Phase 1 - Production Readiness
- **Description:** 2-week sprint to complete P0 blockers for production launch (Test Coverage, Error Handling, Monitoring, Documentation)
- **Visibility:** Private (or Public if preferred)

**Click:** "Create project"

---

### 2. Configure Board Columns

**Default columns to keep:**
- ✅ **Todo** - Tasks not yet started
- ✅ **In Progress** - Tasks currently being worked on
- ✅ **Done** - Completed tasks

**Additional columns to add:**

**Click:** "+" button next to columns

**Add these columns:**
1. **Blocked** - Tasks blocked by dependencies or external factors
2. **Review** - Tasks completed but pending review
3. **Testing** - Tasks in testing/validation phase

**Final column order (left to right):**
1. Todo
2. In Progress
3. Blocked
4. Testing
5. Review
6. Done

---

### 3. Add Automation Rules

**For each column, configure automation:**

#### Todo Column
- **No automation needed** (manual placement)

#### In Progress Column
**Automation:**
- When issue/PR is assigned → Move to "In Progress"
- When issue label changes to "in-progress" → Move here

**How to configure:**
1. Click "⋯" menu on "In Progress" column
2. Select "Workflows"
3. Enable "Item added to project"
4. Enable "Item reopened"

#### Blocked Column
**Automation:**
- When issue label changes to "blocked" → Move here

**How to configure:**
1. Click "⋯" menu on "Blocked" column
2. Select "Workflows"
3. Add custom automation for label "blocked"

#### Testing Column
**Automation:**
- When issue label changes to "testing" → Move here

#### Review Column
**Automation:**
- When PR is opened → Move here
- When issue label changes to "review" → Move here

#### Done Column
**Automation:**
- When issue is closed as completed → Move to "Done"
- When PR is merged → Move to "Done"

**How to configure:**
1. Click "⋯" menu on "Done" column
2. Select "Workflows"
3. Enable "Item closed"

---

### 4. Add Custom Fields

**Click:** "⋮" (three dots) in top right → "Settings"

**Add these custom fields:**

#### Field 1: Workstream
- **Type:** Single select
- **Options:**
  - Workstream 1: Test Coverage
  - Workstream 2: Error Handling
  - Workstream 3: Documentation
  - Workstream 4: Monitoring

#### Field 2: Estimated Hours
- **Type:** Number
- **Description:** Estimated hours to complete

#### Field 3: Actual Hours
- **Type:** Number
- **Description:** Actual hours spent

#### Field 4: Assignee Role
- **Type:** Single select
- **Options:**
  - Developer 1
  - Developer 2
  - DevOps

#### Field 5: Priority
- **Type:** Single select
- **Options:**
  - P0 - Critical
  - P1 - High
  - P2 - Medium

#### Field 6: Day
- **Type:** Number
- **Description:** Day number (1-10) in 2-week sprint

#### Field 7: Dependencies
- **Type:** Text
- **Description:** Issue numbers this task depends on (e.g., "#1, #2")

---

### 5. Add All Issues to Project

**Method 1: Bulk add via GitHub CLI**

```bash
# Get project number from URL
# Example: https://github.com/orgs/coditect-ai/projects/1 → project number is 1
PROJECT_NUMBER=1

# Add all issues with milestone "Phase 1 - Production Readiness"
gh issue list --repo coditect-ai/coditect-core \
  --milestone "Phase 1 - Production Readiness" \
  --json number \
  --jq '.[].number' | \
  xargs -I {} gh project item-add $PROJECT_NUMBER \
  --owner coditect-ai \
  --url https://github.com/coditect-ai/coditect-core/issues/{}
```

**Method 2: Manual add via Web UI**

1. Open project board
2. Click "Add items" button
3. Search for issues by milestone: `milestone:"Phase 1 - Production Readiness"`
4. Select all 32 issues
5. Click "Add selected items"

---

### 6. Set Custom Field Values for Each Issue

**For each issue, set:**

| Issue # | Workstream | Est. Hours | Role | Priority | Day | Dependencies |
|---------|-----------|-----------|------|----------|-----|--------------|
| #1 | Test Coverage | 4 | Developer 1 | P0 | 1 | - |
| #2 | Test Coverage | 2 | Developer 1 | P0 | 1 | #1 |
| #3 | Test Coverage | 6 | Developer 1 | P0 | 1 | #1, #2 |
| #4 | Test Coverage | 8 | Developer 1 | P0 | 2 | #1, #2 |
| #5 | Test Coverage | 8 | Developer 1 | P0 | 3 | #3, #4 |
| #6 | Test Coverage | 8 | Developer 1 | P0 | 4 | #5 |
| #7 | Test Coverage | 8 | Developer 1 | P0 | 5 | #3 |
| #8 | Test Coverage | 8 | Developer 1 | P0 | 6 | #1 |
| #9 | Test Coverage | 8 | Developer 1 | P0 | 7 | #1 |
| #10 | Test Coverage | 8 | Developer 1 | P0 | 8 | #3-9 |
| #11 | Test Coverage | 8 | Developer 1 | P0 | 9 | #3-10 |
| #12 | Test Coverage | 6 | Developer 1 | P0 | 10 | #11 |
| #13 | Error Handling | 4 | Developer 2 | P0 | 1 | - |
| #14 | Error Handling | 4 | Developer 2 | P0 | 1 | #13 |
| #15 | Error Handling | 8 | Developer 2 | P0 | 2 | #14 |
| #16 | Error Handling | 8 | Developer 2 | P0 | 3 | #14 |
| #17 | Error Handling | 8 | Developer 2 | P0 | 4 | #14 |
| #18 | Error Handling | 8 | Developer 2 | P0 | 5 | #15-17 |
| #19 | Documentation | 4 | Developer 2 | P0 | 6 | #18 |
| #20 | Documentation | 3 | Developer 2 | P0 | 6 | #19 |
| #21 | Documentation | 4 | Developer 2 | P0 | 7 | #19 |
| #22 | Documentation | 1 | Developer 2 | P0 | 7 | #19-21 |
| #23 | Monitoring | 4 | DevOps | P0 | 1 | - |
| #24 | Monitoring | 4 | DevOps | P0 | 2 | #23 |
| #25 | Monitoring | 4 | DevOps | P0 | 3 | #24 |
| #26 | Monitoring | 4 | DevOps | P0 | 4 | #24 |
| #27 | Monitoring | 4 | DevOps | P0 | 5 | #24 |
| #28 | Monitoring | 4 | DevOps | P0 | 6 | #23 |
| #29 | Monitoring | 4 | DevOps | P0 | 7 | #28 |
| #30 | Monitoring | 4 | DevOps | P0 | 8 | #23-29 |
| #31 | Monitoring | 4 | DevOps | P0 | 9 | #30 |
| #32 | Monitoring | 4 | DevOps | P0 | 10 | #31 |

**How to set custom fields:**
1. Click on issue in project board
2. In right sidebar, find custom fields
3. Set "Workstream", "Estimated Hours", "Assignee Role", "Priority", "Day", "Dependencies"
4. Repeat for all 32 issues

---

### 7. Create Custom Views

**Create multiple views for different perspectives:**

#### View 1: By Workstream (Board View)

**Create:**
1. Click "View 1" dropdown → "New view"
2. Select "Board" layout
3. Name: "By Workstream"
4. Group by: "Workstream"
5. Sort by: "Day" ascending

**Result:** 4 swimlanes (one per workstream) with tasks organized by day

---

#### View 2: By Day (Table View)

**Create:**
1. Click "View 1" dropdown → "New view"
2. Select "Table" layout
3. Name: "By Day"
4. Group by: "Day"
5. Sort by: "Day" ascending
6. Show columns: Title, Assignee Role, Estimated Hours, Status, Dependencies

**Result:** Table grouped by day showing what should be worked on each day

---

#### View 3: By Assignee (Board View)

**Create:**
1. Click "View 1" dropdown → "New view"
2. Select "Board" layout
3. Name: "By Assignee"
4. Group by: "Assignee Role"
5. Sort by: "Day" ascending

**Result:** 3 swimlanes (Developer 1, Developer 2, DevOps) showing individual workload

---

#### View 4: Blocked & Overdue (Table View)

**Create:**
1. Click "View 1" dropdown → "New view"
2. Select "Table" layout
3. Name: "Blocked & Overdue"
4. Filter by: Status = "Blocked" OR (Status != "Done" AND Day < Current Day)
5. Sort by: "Priority" descending
6. Show columns: Title, Assignee Role, Priority, Day, Dependencies, Status

**Result:** Focus view showing items needing attention

---

#### View 5: Burndown (Chart View - if available)

**Create:**
1. Click "View 1" dropdown → "New view"
2. Select "Chart" layout (if available in GitHub Projects Beta)
3. Name: "Burndown Chart"
4. X-axis: Day
5. Y-axis: Count of issues not Done
6. Group by: Workstream

**Result:** Visual burndown chart showing progress

---

### 8. Configure Project Settings

**Click:** "⋮" (three dots) in top right → "Settings"

**Configure:**

#### General Settings
- **Project description:** 2-week sprint to complete P0 blockers for production launch
- **README:** (Optional) Add project overview and goals
- **Visibility:** Private (recommended for internal projects)

#### Access Settings
- **Add team members:**
  - Developer 1: Write access
  - Developer 2: Write access
  - DevOps: Write access
  - Project Manager: Admin access
  - Stakeholders: Read access

#### Notifications
- **Enable:** Issue status changes, new items added, items completed
- **Frequency:** Real-time for critical updates

---

## Daily Workflow

### Developer Workflow

**Every Morning (9:00 AM Standup):**
1. Open project board → "By Assignee" view
2. Review your swimlane (Developer 1 or Developer 2)
3. Check "Blocked" column for your tasks
4. Identify next task to work on (check Day number and Dependencies)

**Starting a Task:**
1. Assign yourself to the issue (if not already assigned)
2. Move issue to "In Progress" column (or add "in-progress" label)
3. Update "Actual Hours" field as you work

**Completing a Task:**
1. Create PR if code changes involved
2. Move to "Review" column (or add "review" label)
3. Update "Actual Hours" with final time spent
4. Tag reviewer in PR or issue

**Blocking a Task:**
1. Add comment explaining blocker
2. Add "blocked" label
3. Issue automatically moves to "Blocked" column
4. Escalate blocker in standup

---

### DevOps Workflow

**Same as developer workflow, but:**
- Work from "Monitoring" workstream
- Focus on infrastructure and observability tasks
- Part-time allocation (4 hours/day)
- Update "Actual Hours" to track part-time effort

---

### Project Manager Workflow

**Daily (15 minutes):**
1. Open "Blocked & Overdue" view
2. Address blockers with team
3. Update stakeholders on progress
4. Review "Burndown Chart" for overall progress

**Mid-Week Checkpoint (Wednesday, Day 3):**
1. Generate progress report:
   - Total issues: 32
   - Completed: X
   - In Progress: Y
   - Blocked: Z
   - % Complete: (X / 32) × 100
2. Review with team
3. Adjust plan if needed

**End-of-Week Review (Friday, Day 5 and Day 10):**
1. Generate comprehensive report
2. Identify risks and mitigation
3. Update stakeholder presentation
4. Plan next week (Week 2 or post-Phase 1)

---

## Progress Tracking

### Key Metrics to Track

#### Velocity
- **Formula:** Completed issues per day
- **Target:** ~3-4 issues per day (32 issues / 10 days)
- **How to measure:** Count issues in "Done" column daily

#### Burndown Rate
- **Formula:** Remaining issues / Days left
- **Target:** Linear decrease from 32 → 0 over 10 days
- **How to measure:** Track "Todo" + "In Progress" count daily

#### Blocker Rate
- **Formula:** Issues in "Blocked" column / Total issues
- **Target:** <10% (max 3 issues blocked at any time)
- **How to measure:** Count "Blocked" column

#### Workstream Balance
- **Formula:** % complete per workstream
- **Target:** All workstreams complete within 20% of each other
- **How to measure:** Group by workstream, calculate % done

---

## Reporting & Dashboards

### Daily Standup Report (Auto-Generated)

**Create automation or manual tracking spreadsheet:**

```markdown
## Daily Standup Report - Day X of 10

**Date:** YYYY-MM-DD

### Progress
- **Completed:** X / 32 issues (X%)
- **In Progress:** Y issues
- **Blocked:** Z issues
- **On Track:** Yes/No

### Yesterday's Completions
- [ ] Issue #X: Title (Developer 1)
- [ ] Issue #Y: Title (Developer 2)
- [ ] Issue #Z: Title (DevOps)

### Today's Plan
- [ ] Issue #A: Title (Developer 1)
- [ ] Issue #B: Title (Developer 2)
- [ ] Issue #C: Title (DevOps)

### Blockers
- Issue #X: Blocker description (Owner: Developer 1, Escalated to: PM)

### Metrics
- **Velocity:** X issues/day (target: 3.2)
- **Burndown:** X issues remaining (target: Y)
- **Days Remaining:** X days
```

---

### Weekly Summary Report

**Generate every Friday (Day 5 and Day 10):**

```markdown
## Weekly Summary - Week X of 2

**Week:** YYYY-MM-DD to YYYY-MM-DD

### Overall Progress
- **Total Issues:** 32
- **Completed This Week:** X issues
- **Total Completed:** Y issues (Y%)
- **Remaining:** Z issues

### Workstream Progress
| Workstream | Total | Completed | % Complete | On Track? |
|-----------|-------|-----------|-----------|----------|
| Test Coverage (12) | 12 | X | X% | Yes/No |
| Error Handling (6) | 6 | Y | Y% | Yes/No |
| Documentation (4) | 4 | Z | Z% | Yes/No |
| Monitoring (10) | 10 | W | W% | Yes/No |

### Highlights
- ✅ Completed test coverage for core modules
- ✅ Error handling library implemented
- ⚠️ Monitoring deployment delayed 1 day

### Risks & Mitigation
- **Risk:** Test coverage target may fall short
- **Mitigation:** Added 2 days buffer, prioritizing high-value modules

### Next Week Plan
- Complete remaining X issues
- Focus on integration testing
- Begin quality gate validation

### Team Feedback
- Developer 1: [feedback]
- Developer 2: [feedback]
- DevOps: [feedback]
```

---

## Quality Gate Validation

### Pre-Production Checklist (Day 10)

**Use this checklist for GO/NO-GO decision:**

#### Quality Gate 1: Test Coverage ✅
- [ ] Overall coverage ≥60% (run `pytest --cov`)
- [ ] Core modules ≥70% (task.py, orchestrator.py, state_manager.py, executor.py)
- [ ] CI integration operational (tests run on PR)
- [ ] No failing tests

**Validation:** Run `pytest --cov` and verify coverage report

---

#### Quality Gate 2: Error Handling ✅
- [ ] All 21 scripts have error handling (code review)
- [ ] All scripts log errors with context (manual check)
- [ ] Graceful degradation implemented (testing)
- [ ] No unhandled exceptions in production scenarios (testing)

**Validation:** Code review + manual error scenario testing

---

#### Quality Gate 3: Production Monitoring ✅
- [ ] Prometheus collecting metrics (check /metrics endpoint)
- [ ] 2 Grafana dashboards operational (System Health, User Experience)
- [ ] Jaeger tracing working (traces visible in UI)
- [ ] Alert rules tested (trigger test alert)
- [ ] Documentation complete (MONITORING-GUIDE.md exists)

**Validation:** Run sample workload, verify metrics/traces/alerts

---

#### Quality Gate 4: Documentation Navigation ✅
- [ ] 6 category README.md files created
- [ ] 6 category CLAUDE.md files created
- [ ] Master docs/README.md created
- [ ] All broken links fixed (run link checker)
- [ ] Link checker validation passes (0 broken links)

**Validation:** Manual navigation test + automated link checker

---

## Tips & Best Practices

### For Team Members

1. **Update Issues Daily**
   - Move cards when you start/complete work
   - Update "Actual Hours" daily
   - Comment on progress/blockers

2. **Check Dependencies**
   - Before starting a task, verify dependencies are complete
   - Check "Dependencies" custom field
   - Don't start blocked tasks

3. **Communicate Blockers Early**
   - Add "blocked" label immediately
   - Comment with blocker details
   - Escalate in standup (don't wait)

4. **Keep PR Linked**
   - Link PR to issue using "Closes #X" in PR description
   - PR merge auto-closes issue and moves to "Done"

5. **Review Team's Work**
   - Check "Review" column for peer review requests
   - Provide feedback within 4 hours
   - Approve or request changes

---

### For Project Manager

1. **Monitor Blockers**
   - Check "Blocked" column multiple times per day
   - Resolve blockers within 2 hours
   - Escalate technical blockers to senior engineer

2. **Track Velocity**
   - Calculate daily: issues completed / day
   - Compare to target: 3.2 issues/day
   - Adjust plan if velocity <80% of target

3. **Balance Workload**
   - Use "By Assignee" view to check individual workload
   - Reassign tasks if one person overloaded
   - Ensure no one is idle

4. **Stakeholder Updates**
   - Send daily summary to stakeholders
   - Highlight risks and mitigation
   - Prepare for GO/NO-GO decision on Day 10

---

## Troubleshooting

### Issue: Tasks Not Moving Automatically

**Problem:** Cards stay in "Todo" even when assigned

**Solution:**
1. Check automation rules (column settings → Workflows)
2. Ensure automation is enabled
3. Manually move cards if automation broken
4. Re-enable automation in project settings

---

### Issue: Custom Fields Not Showing

**Problem:** Custom fields not visible in cards

**Solution:**
1. Click "⋮" → "Settings"
2. Check "Fields" section
3. Ensure fields are enabled
4. Add fields to card layout (click card, check sidebar)

---

### Issue: Dependencies Not Tracked

**Problem:** Can't see which tasks are blocking others

**Solution:**
1. Use "Dependencies" custom field (text)
2. Manually enter issue numbers (#1, #2)
3. Consider using GitHub task lists in issue description
4. Use "Blocked" label and column

---

### Issue: Project Board Too Cluttered

**Problem:** Too many cards, can't see overview

**Solution:**
1. Use views to filter (By Workstream, By Day)
2. Hide "Done" column (collapse it)
3. Archive completed issues after 1 week
4. Use search/filter to focus on specific workstream

---

## Next Steps After Setup

1. **Team Training (30 minutes)**
   - Walk through board layout
   - Explain workflow (Todo → In Progress → Review → Done)
   - Practice moving cards
   - Show custom views

2. **Kickoff Meeting (1 hour)**
   - Review all 32 issues
   - Confirm dependencies
   - Assign initial tasks (Day 1 tasks)
   - Set expectations for daily standups

3. **First Standup (Day 1, 9:00 AM)**
   - Each person shares their Day 1 tasks
   - Identify any immediate blockers
   - Commit to moving first tasks to "In Progress"

4. **Daily Rhythm**
   - Standup: 9:00 AM (15 minutes)
   - Work: 9:15 AM - 6:00 PM
   - End-of-day: Update board before leaving
   - Async communication: Slack/GitHub comments

---

## Resources

### Links
- **Project Board:** https://github.com/orgs/coditect-ai/projects/X
- **Repository:** https://github.com/coditect-ai/coditect-core
- **Issues:** https://github.com/coditect-ai/coditect-core/issues?q=is%3Aissue+milestone%3A%22Phase+1+-+Production+Readiness%22
- **Documentation:** See PHASE-1-IMPLEMENTATION-PLAN.md

### GitHub Projects Documentation
- **GitHub Projects Guide:** https://docs.github.com/en/issues/planning-and-tracking-with-projects
- **Automation:** https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project
- **Custom Fields:** https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields

---

**Setup Version:** 1.0
**Created:** November 22, 2025
**Owner:** CODITECT Core Team
**Status:** Ready for Implementation
**Next Action:** Create project board and add issues

---

## Summary

✅ **Project board configured** with 6 columns (Todo, In Progress, Blocked, Testing, Review, Done)
✅ **32 issues ready to add** from GITHUB-ISSUES-PHASE-1.md
✅ **7 custom fields defined** (Workstream, Est. Hours, Actual Hours, Assignee Role, Priority, Day, Dependencies)
✅ **5 custom views created** (By Workstream, By Day, By Assignee, Blocked & Overdue, Burndown)
✅ **4 quality gates** defined for GO/NO-GO decision
✅ **Team workflow** documented for daily operations

**Ready to launch Phase 1! 🚀**
