# CODITECT Checkpoint Process Standard

**Framework:** CODITECT
**Version:** 1.0
**Status:** ✅ OPERATIONAL
**Author:** AZ1.AI INC.
**Effective Date:** November 22, 2025

---

## Executive Summary

This document establishes the **standardized checkpoint process** for the CODITECT platform that ensures **all modified submodules are consistently committed and pushed** alongside the parent repository.

**Key Principle:** A checkpoint is incomplete unless ALL modified submodules have been committed and pushed to their remote repositories.

---

## The Problem: Inconsistent Submodule State

### Previous Behavior (Anti-Pattern)
```
User runs: git push (from master repo)
        ↓
Master repo changes pushed ✅
        ↓
Submodule changes left uncommitted ❌
        ↓
Result: Inconsistent state across repos
```

**Consequences:**
- Distributed intelligence broken (submodules out of sync)
- Next session missing critical context
- Difficult debugging across multiple repos
- Loss of audit trail for work done

### Desired Behavior (Standardized)
```
Checkpoint Process:
1. Detect ALL modified submodules
2. Commit changes in each submodule → Push to remote
3. Commit parent repo with updated submodule pointers
4. Push parent repo to remote
5. Generate audit trail
        ↓
Result: All repos in consistent, traceable state ✅
```

---

## Checkpoint Process Workflow

### Phase 1: Submodule Detection & Commit

**Script:** `scripts/checkpoint-with-submodules.py`

```bash
cd /path/to/coditect-rollout-master

# Detect all 45 configured submodules
# For each submodule with modifications:
#   1. Stage all changes (git add -A)
#   2. Commit with descriptive message
#   3. Push to remote
```

**Output:**
```
📍 Step 1: Detecting modified submodules...
✅ submodules/core/coditect-core: HAS MODIFICATIONS
✅ submodules/cloud/coditect-cloud-backend: HAS MODIFICATIONS
... (40 more submodules)
📊 Summary: 42 submodule(s) with modifications
```

### Phase 2: Parent Repository Update

**What Happens:**
1. Parent repo detects all submodule pointer changes
2. Stages `.gitmodules` and all submodule references
3. Creates comprehensive commit message with all updated submodules
4. Pushes parent repo to remote

**Result:**
- Parent repo now points to latest submodule commits
- Next clone will get correct versions of all submodules
- Complete audit trail of what changed

### Phase 3: Audit Trail Generation

**What's Created:**
```
MEMORY-CONTEXT/audit-logs/
├── 2025-11-22T07-04-21Z-checkpoint-audit-Sprint-Description.json
```

**Contains:**
- Timestamp of checkpoint
- Sprint description
- List of all modified submodules
- Operation-by-operation audit trail
- Success/error status for each operation

---

## Usage: Complete Checkpoint with All Submodules

### Option 1: Full Checkpoint (Commit + Push Everything)

```bash
cd /Users/halcasteel/PROJECTS/coditect-rollout-master

python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Export dedup automatic re-organization complete"
```

**What happens:**
1. ✅ Commits & pushes all 42 modified submodules
2. ✅ Commits & pushes parent repo with updated pointers
3. ✅ Generates audit report
4. ✅ Result: All repos in consistent state on remote

### Option 2: Dry-Run (Commit Only, No Push)

```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Work in progress" \
  --no-push
```

**What happens:**
1. ✅ Commits all modified submodules (locally)
2. ✅ Commits parent repo (locally)
3. ❌ Does NOT push to remote
4. ✅ Generates audit report

**Use Case:** Testing checkpoint before pushing, or saving state locally mid-work

---

## Checkpoint Locations in Repository

### In coditect-core (Core Framework)

**Main Scripts:**
- `scripts/checkpoint-with-submodules.py` - Enhanced checkpoint with submodule management
- `scripts/create-checkpoint.py` - Legacy checkpoint (for single repos)
- `scripts/export-dedup.py` - Automatic conversation export deduplication

**Documentation:**
- `docs/CHECKPOINT-PROCESS-STANDARD.md` - This file
- `docs/CHECKPOINT-WORKFLOW.md` - Detailed workflow diagrams

### In Master Repo

**Audit Trails:**
```
MEMORY-CONTEXT/audit-logs/
├── 2025-11-22T07-04-21Z-checkpoint-audit-*.json
├── 2025-11-22T07-15-43Z-checkpoint-audit-*.json
└── ... (historical audit logs)
```

**Session History:**
```
MEMORY-CONTEXT/sessions/
├── 2025-11-22-Sprint-Description.md
└── ... (session summaries)
```

**Checkpoints:**
```
MEMORY-CONTEXT/checkpoints/
├── 2025-11-22T07-04-21Z-Sprint-Description.md
└── ... (state snapshots)
```

---

## Key Design Principles

### 1. **No Partial Checkpoints**

A checkpoint is either:
- **Complete:** All modified submodules + parent repo committed and pushed
- **Incomplete:** Should not be used

**Never:**
```bash
# ❌ BAD: Push only parent repo
git push
```

**Always:**
```bash
# ✅ GOOD: Checkpoint handles all submodules + parent
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py "Description"
```

### 2. **Consistent Audit Trail**

Every checkpoint operation is logged:
- When it started/ended
- Which submodules were modified
- Success/failure of each operation
- Detailed error messages for debugging

**Access Audit Trail:**
```bash
cat MEMORY-CONTEXT/audit-logs/2025-11-22T07-04-21Z-*.json | jq .
```

### 3. **Atomic Operations (Per Submodule)**

Each submodule's commit/push cycle is atomic:
- All changes staged together
- Committed with single message
- Pushed as unit
- If push fails, clear error message (can retry)

### 4. **Graceful Error Handling**

If one submodule fails:
- Other submodules continue processing
- Clear error message shown
- Audit trail captures which failed
- Can fix and re-run checkpoint

**Example:**
```
❌ submodules/cloud/coditect-cloud-backend: Push failed
   (network timeout - can retry)

✅ submodules/core/coditect-core: Success
✅ 40 other submodules: Success

⚠️  Summary: 41 success, 1 failure
    Run checkpoint again after fixing issue
```

---

## When to Run Checkpoints

### Recommended Checkpoint Triggers

1. **After Major Work Completion** (Daily)
   ```bash
   python3 scripts/checkpoint-with-submodules.py "Daily checkpoint: Feature X complete"
   ```

2. **After Sprint Completion** (Weekly)
   ```bash
   python3 scripts/checkpoint-with-submodules.py "Sprint +1 complete: All modules updated"
   ```

3. **Before Context Transition** (Session End)
   ```bash
   python3 scripts/checkpoint-with-submodules.py "Session context saved for continuity"
   ```

4. **After Architecture Changes** (Critical)
   ```bash
   python3 scripts/checkpoint-with-submodules.py "Architecture update: Multi-agent messaging"
   ```

### When NOT to Checkpoint

- ❌ Mid-feature (work incomplete)
- ❌ After just a single file change
- ❌ Before running tests (checkpoint after passing tests)

---

## Integration with Other Systems

### Export Deduplication

After running `/export` in Claude Code:

```bash
# Step 1: Run export-dedup to process conversation
cd /Users/halcasteel/PROJECTS/coditect-rollout-master/submodules/core/coditect-core
python3 scripts/export-dedup.py --yes --auto-compact

# Step 2: Checkpoint to commit all changes
cd /Users/halcasteel/PROJECTS/coditect-rollout-master
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Export dedup and organization complete"
```

**Result:**
- ✅ Conversation deduplicated
- ✅ Messages organized into checkpoints
- ✅ All changes committed and pushed
- ✅ Audit trail created
- ✅ Ready for next session

---

## Troubleshooting

### Issue: "Submodule path does not exist"

**Cause:** Submodule initialized but not cloned

**Fix:**
```bash
git submodule update --init --recursive
```

### Issue: "Everything up-to-date" for submodule

**Cause:** Submodule already pushed (or no changes)

**Fix:** This is normal - checkpoint will skip push for clean submodules

**Log Entry:**
```json
{
  "repo": "submodules/cloud/coditect-cloud-frontend",
  "operation": "push",
  "status": "info",
  "details": "Everything up-to-date"
}
```

### Issue: One submodule push fails, others succeed

**Cause:** Network issue or permission problem with one repo

**Fix:**
```bash
# 1. Check git status of failed submodule
cd submodules/cloud/failed-submodule
git status

# 2. Fix issue (permissions, credentials, etc)

# 3. Re-run checkpoint
cd ../../../..
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py "Retry after fix"
```

---

## Audit Trail Analysis

### View Latest Checkpoint Audit

```bash
# List all audit logs (most recent first)
ls -t MEMORY-CONTEXT/audit-logs/ | head -5

# View latest checkpoint audit
cat MEMORY-CONTEXT/audit-logs/2025-11-22T07-04-21Z-checkpoint-audit-*.json | jq .
```

### Extract Submodule Summary

```bash
# Show which submodules were modified
cat MEMORY-CONTEXT/audit-logs/latest-audit.json | \
  jq '.operations[] | select(.operation == "detect") | .repo'
```

### Check Push Status

```bash
# Show which pushes succeeded/failed
cat MEMORY-CONTEXT/audit-logs/latest-audit.json | \
  jq '.operations[] | select(.operation == "push") | {repo: .repo, status: .status}'
```

---

## Best Practices

### ✅ DO:

1. **Run checkpoint after major work completion**
   ```bash
   python3 scripts/checkpoint-with-submodules.py "Feature completed"
   ```

2. **Use descriptive sprint descriptions**
   ```bash
   # Good ✅
   "Export dedup with automatic re-organization and submodule integration"

   # Bad ❌
   "update"
   ```

3. **Check audit trail for verification**
   ```bash
   cat MEMORY-CONTEXT/audit-logs/latest.json
   ```

4. **Allow time between checkpoints** (at least 30 minutes)
   - Prevents excessive git activity
   - Allows meaningful work to accumulate

### ❌ DON'T:

1. **Manually git push** (use checkpoint instead)
   ```bash
   # Don't do this ❌
   git push

   # Do this instead ✅
   python3 scripts/checkpoint-with-submodules.py "Description"
   ```

2. **Push only parent repo** (always include submodules)
   ```bash
   # Don't do this ❌
   cd master-repo && git push

   # Do this instead ✅
   python3 scripts/checkpoint-with-submodules.py "Description"
   ```

3. **Skip audit trail verification**
   ```bash
   # Always verify
   cat MEMORY-CONTEXT/audit-logs/latest.json
   ```

---

## Future Enhancements

### Planned (Phase 2)

- [ ] Automatic checkpoint triggers (e.g., after 2 hours of activity)
- [ ] Smart batch detection (group related submodule commits)
- [ ] Parallel submodule pushing (faster for many repos)
- [ ] Slack/Discord notifications on checkpoint completion
- [ ] Automatic rollback on critical failures
- [ ] Integration with CI/CD validation gates

### Proposed (Phase 3)

- [ ] Checkpoint scheduling (daily at specific time)
- [ ] Smart checkpointing (only if significant work done)
- [ ] Cross-repo dependency tracking
- [ ] Automated testing on checkpoint
- [ ] WebUI for checkpoint visualization

---

## References

- **Main Script:** `scripts/checkpoint-with-submodules.py`
- **Legacy Script:** `scripts/create-checkpoint.py`
- **Export Dedup:** `scripts/export-dedup.py`
- **Framework:** CODITECT v1.0
- **Repository:** https://github.com/coditect-ai/coditect-rollout-master

---

**Last Updated:** November 22, 2025
**Status:** ✅ Approved for Production Use
**Copyright:** © 2025 AZ1.AI INC. All rights reserved.
