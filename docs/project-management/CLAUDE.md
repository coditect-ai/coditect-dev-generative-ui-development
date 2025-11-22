# Project Management - Claude Code Configuration

## Directory Purpose

Master planning and task tracking for CODITECT platform rollout (46 submodules, 8 categories, $884K budget).

## Essential Reading

**READ FIRST (in order):**
1. PROJECT-PLAN.md - Complete rollout strategy (72KB)
2. TASKLIST.md - Checkbox-based task tracking (23KB)
3. Organization reports (for infrastructure context)

## Tech Stack

**Planning Tools:**
- Markdown-based PROJECT-PLAN.md and TASKLIST.md
- JSON timeline data with interactive HTML visualization
- Git-tracked progress with conventional commits

**Project Metrics:**
- Phase: Beta Testing (Active - Week 2 of 4)
- Timeline: Aug 27, 2025 → Mar 11, 2026 (197 days)
- Status: Phase 0 Complete ✅, Phase 1 Active ⚡
- Submodules: 46 repositories across 8 categories

## Key Documents

### PROJECT-PLAN.md (72KB)
- Executive summary with status dashboard
- 6-phase rollout timeline
- Budget breakdown ($884K)
- Milestone tracking
- Risk management
- Success metrics

### TASKLIST.md (23KB)
- 530+ tasks across all phases
- Checkbox format: [x] complete, [ ] pending
- Phase 0: ✅ Complete (350+ tasks)
- Phase 1: ⚡ Active (50% complete)
- Phase 2+: ⏸️ Scheduled

### Organization Reports
- Root cleanup validation (Nov 22)
- Comprehensive audits
- Reorganization summaries
- Submodule verification

## Common Operations

### Check Current Status
```bash
# Phase and milestone
grep "Current Phase" PROJECT-PLAN.md

# Active tasks
grep '\[ \]' TASKLIST.md | head -10

# Budget status
grep "Budget" PROJECT-PLAN.md | head -5
```

### Update Progress
```bash
# Mark task complete in TASKLIST.md
# Change [ ] to [x]

# Update PROJECT-PLAN.md status table
# Modify percentage or status emoji
```

### Generate Reports
```bash
# Timeline visualization
open PROJECT-TIMELINE-INTERACTIVE.html

# Task completion percentage
grep -c '\[x\]' TASKLIST.md
grep -c '\[ \]' TASKLIST.md
```

## Project-Specific Instructions

### When Reviewing Project Status
1. Read PROJECT-PLAN.md Executive Summary (lines 1-50)
2. Check current phase objectives (Section 3)
3. Review milestone dates (Section 4)
4. Validate budget status (Section 5)

### When Working on Tasks
1. Find task in TASKLIST.md under active phase
2. Check dependencies and blockers
3. Review related ADRs in ../adrs/
4. Update checkbox [x] when complete
5. Create MEMORY-CONTEXT checkpoint if significant

### When Planning Sprints
1. Review PROJECT-PLAN.md phase breakdown
2. Identify next 2-week priorities in TASKLIST.md
3. Check PROJECT-TIMELINE-INTERACTIVE.html for dependencies
4. Coordinate with submodule PROJECT-PLANs

### When Reporting Progress
1. Extract metrics from PROJECT-PLAN.md
2. Calculate completion from TASKLIST.md checkboxes
3. Reference organization reports for infrastructure
4. Update stakeholder dashboard

## Cross-References

**Architecture:**
- ../adrs/project-intelligence/ - 8 ADRs for platform architecture
- ../../diagrams/ - C4 diagrams (24 complete)

**Implementation:**
- ../../submodules/core/coditect-core/ - Core framework
- ../../submodules/cloud/ - Cloud platform (4 repos)
- ../../submodules/dev/ - Developer tools (10 repos)

**Context:**
- ../../WHAT-IS-CODITECT.md - Distributed intelligence overview
- ../../README.md - Repository overview
- ../../MEMORY-CONTEXT/ - Session continuity

## Important Constraints

### Document Updates
- PROJECT-PLAN.md: Update weekly during active phases
- TASKLIST.md: Update same-day when tasks complete
- Timeline JSON: Update weekly with milestone changes
- Organization reports: Generate after infrastructure changes

### Git Workflow
- Use conventional commits
- Reference PROJECT-PLAN.md section in commit messages
- Create checkpoints after milestone completion
- Tag major phase transitions

### Task Management
- Mark tasks [x] only when fully complete
- Add new tasks to appropriate phase section
- Note blockers with ⚠️ emoji
- Cross-reference related tasks

## Quality Gates

**Before Marking Phase Complete:**
- [ ] All phase tasks checked [x] in TASKLIST.md
- [ ] PROJECT-PLAN.md status updated
- [ ] Milestone documented in timeline JSON
- [ ] Checkpoint created in MEMORY-CONTEXT
- [ ] Organization report generated (if structure changed)

**Before Major Updates:**
- [ ] Read current PROJECT-PLAN.md status
- [ ] Check TASKLIST.md for active phase
- [ ] Review recent organization reports
- [ ] Validate no conflicting updates in progress

## Automation Hooks

### Task Completion
When marking task complete:
1. Update TASKLIST.md checkbox
2. Check if milestone reached
3. Update PROJECT-PLAN.md if needed
4. Create checkpoint if significant

### Phase Transition
When phase completes:
1. Verify all tasks [x] in TASKLIST.md
2. Update PROJECT-PLAN.md phase status
3. Generate phase completion report
4. Create MEMORY-CONTEXT checkpoint
5. Tag git commit

### Timeline Updates
When milestones change:
1. Update PROJECT-PLAN.md dates
2. Regenerate timeline JSON
3. Rebuild interactive HTML
4. Validate dependencies still valid

## Troubleshooting

**Completion percentages don't match:**
- TASKLIST.md is source of truth (task-level)
- PROJECT-PLAN.md shows phase-level rollup

**Timeline visualization not loading:**
- Open PROJECT-TIMELINE-INTERACTIVE.html in modern browser
- Check JSON files are valid (run through jq)

**Organization reports outdated:**
- Generate new report after directory changes
- Reference timestamp in filename

**Unclear next priorities:**
- Check TASKLIST.md active phase (⚡ emoji)
- Focus on unchecked [ ] tasks in that section

---

**Status:** ✅ Production Ready
**Last Updated:** 2025-11-22
**Review Frequency:** Weekly during active phases
