# CODITECT Checkpoint Quick Start Guide

**tl;dr:** Use `checkpoint-with-submodules.py` instead of `git push`

---

## One-Command Checkpoint

```bash
cd /Users/halcasteel/PROJECTS/coditect-rollout-master

python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Your sprint description here"
```

**What it does:**
- ✅ Detects all 42 modified submodules
- ✅ Commits each submodule
- ✅ Pushes each submodule to remote
- ✅ Updates parent repo with submodule pointers
- ✅ Commits and pushes parent repo
- ✅ Creates audit trail

**Time:** ~2-3 minutes

---

## Examples

### Daily Checkpoint
```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Daily work: Feature X implementation complete"
```

### After Sprint
```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Sprint +1 complete: All modules updated and tested"
```

### After Export Dedup
```bash
# 1. Process export
cd submodules/core/coditect-core
python3 scripts/export-dedup.py --yes --auto-compact

# 2. Checkpoint everything
cd ../../../
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Export dedup and organization complete"
```

### Dry Run (Commit Only)
```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Work in progress" \
  --no-push
```

---

## Status Output

```
================================================================================
CODITECT Enhanced Checkpoint System with Multi-Submodule Management
================================================================================

📋 Sprint: Export dedup automatic re-organization complete
🕐 Timestamp: 2025-11-22T07-04-21Z
🚀 Mode: Commit + Push (all submodules and parent)

📍 Step 1: Detecting modified submodules...
================================================================================
Found 45 submodules configured
✅ submodules/core/coditect-core: HAS MODIFICATIONS
✅ submodules/cloud/coditect-cloud-backend: HAS MODIFICATIONS
... (40 more)
📊 Summary: 42 submodule(s) with modifications

================================================================================
Step 2: Committing and pushing modified submodules
================================================================================
✅ submodules/core/coditect-core: Committed and pushed
✅ submodules/cloud/coditect-cloud-backend: Committed and pushed
... (40 more)

================================================================================
Step 3: Updating parent repository
================================================================================
✅ Parent repository committed and pushed

================================================================================
Step 4: Generating audit report
================================================================================
✅ Audit report saved: 2025-11-22T07-04-21Z-checkpoint-audit-*.json

================================================================================
✅ CHECKPOINT COMPLETE
================================================================================
```

---

## Key Rules

### ✅ DO

1. **Use checkpoint for all major work**
   ```bash
   python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py "Description"
   ```

2. **Use descriptive sprint descriptions**
   ```bash
   "Feature X: Database schema migration complete"
   "Bug fix: Memory leak in agent framework"
   "Documentation: Updated API reference"
   ```

3. **Check audit trail for verification**
   ```bash
   cat MEMORY-CONTEXT/audit-logs/latest.json
   ```

### ❌ DON'T

1. **Don't use plain `git push`**
   ```bash
   # WRONG ❌
   git push
   ```

2. **Don't push only parent repo**
   ```bash
   # WRONG ❌
   cd master-repo && git push
   ```

3. **Don't forget descriptive messages**
   ```bash
   # WRONG ❌
   python3 scripts/checkpoint-with-submodules.py "update"

   # RIGHT ✅
   python3 scripts/checkpoint-with-submodules.py "Feature complete: Multi-agent routing"
   ```

---

## When to Checkpoint

| Trigger | Example | Action |
|---------|---------|--------|
| **Feature complete** | Added new API endpoint | `checkpoint-with-submodules.py "API endpoint: /agents/list"` |
| **Bug fixed** | Fixed memory leak | `checkpoint-with-submodules.py "Fix: Memory leak in agent pool"` |
| **Sprint finished** | Weekly checkpoint | `checkpoint-with-submodules.py "Sprint +1 complete"` |
| **Export processed** | After /export + dedup | `checkpoint-with-submodules.py "Export dedup complete"` |
| **Session ending** | End of work day | `checkpoint-with-submodules.py "End of session checkpoint"` |

---

## Troubleshooting

### "Submodule path does not exist"
```bash
git submodule update --init --recursive
```

### "Everything up-to-date" for a submodule
This is normal - that submodule has no changes to push. The script will skip it.

### One submodule push fails
The script will continue with others. Check the audit log:
```bash
cat MEMORY-CONTEXT/audit-logs/latest.json | jq '.operations[] | select(.status == "error")'
```

### Need to retry after fixing an issue
Just run checkpoint again - it will detect and push only the modified submodules.

---

## Audit Trail

Every checkpoint creates a detailed log:

```bash
# View latest audit log
cat MEMORY-CONTEXT/audit-logs/2025-11-22T07-04-21Z-checkpoint-audit-*.json | jq .

# View just the summary
cat MEMORY-CONTEXT/audit-logs/latest.json | jq '.operation_summary'

# Output:
# {
#   "total_operations": 46,
#   "by_status": {
#     "success": 44,
#     "warning": 1,
#     "error": 0,
#     "info": 1
#   }
# }
```

---

## Integration with Export Dedup

**Complete workflow:**

```bash
# Step 1: Export conversation (in Claude Code)
/export

# Step 2: Deduplicate and organize
cd submodules/core/coditect-core
python3 scripts/export-dedup.py --yes --auto-compact

# Step 3: Checkpoint everything
cd ../../../
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Export dedup and organization complete"
```

**Result:**
- ✅ Conversation deduplicated (95%+ reduction)
- ✅ Messages organized into checkpoints
- ✅ All changes committed and pushed
- ✅ Audit trail created
- ✅ Ready for next session

---

## Command Reference

### Full Checkpoint (Commit + Push)
```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Sprint description"
```

### Dry Run (Commit Only)
```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Sprint description" \
  --no-push
```

### Custom Repo Root
```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Sprint description" \
  --repo-root /custom/path
```

### Get Help
```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py --help
```

---

## Key Principle

**All modified submodules must be committed and pushed alongside the parent repo.**

A checkpoint is complete when:
- ✅ All modified submodules committed
- ✅ All modified submodules pushed
- ✅ Parent repo updated with submodule pointers
- ✅ Parent repo committed
- ✅ Parent repo pushed
- ✅ Audit trail created

---

## More Information

- **Full Documentation:** `CHECKPOINT-PROCESS-STANDARD.md` (in coditect-core)
- **Implementation Details:** `CHECKPOINT-PROCESS-IMPLEMENTATION.md` (in master repo)
- **Script Source:** `submodules/core/coditect-core/scripts/checkpoint-with-submodules.py`

---

**Last Updated:** November 22, 2025
**Status:** ✅ Ready to Use
**Copyright:** © 2025 AZ1.AI INC. All rights reserved.
