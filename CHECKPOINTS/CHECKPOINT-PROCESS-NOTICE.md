# ⚠️ IMPORTANT: Standardized Checkpoint Process

**Effective Date:** November 22, 2025
**Status:** ✅ OPERATIONAL

---

## The Standard (Required)

When you have completed work, use this process:

```bash
cd /Users/halcasteel/PROJECTS/coditect-rollout-master

python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Your sprint description"
```

## What It Does

Automatically:
1. ✅ Detects all 45 configured submodules
2. ✅ Commits changes in each modified submodule
3. ✅ Pushes each submodule to remote
4. ✅ Updates parent repository with submodule pointers
5. ✅ Commits and pushes parent repository
6. ✅ Creates comprehensive audit trail

## Why This Matters

**DO NOT use:** `git push`

**ALWAYS use:** `python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py`

**Reason:** Without the standardized process, you'll have:
- ❌ Parent repo updated but submodules left uncommitted
- ❌ Next session starting with broken context
- ❌ Lost audit trail of what was changed and why
- ❌ Inconsistent state across distributed repositories

## Example

```bash
python3 submodules/core/coditect-core/scripts/checkpoint-with-submodules.py \
  "Completed export dedup and automatic re-organization"
```

**Output:**
```
================================================================================
CODITECT Enhanced Checkpoint System with Multi-Submodule Management
================================================================================

📋 Sprint: Completed export dedup and automatic re-organization
🕐 Timestamp: 2025-11-22T07-04-21Z
🚀 Mode: Commit + Push (all submodules and parent)

📍 Step 1: Detecting modified submodules...
================================================================================
Found 45 submodules configured
✅ submodules/core/coditect-core: HAS MODIFICATIONS
✅ submodules/cloud/coditect-cloud-backend: HAS MODIFICATIONS
... (40 more submodules)
📊 Summary: 42 submodule(s) with modifications

[continues with commit and push operations...]

================================================================================
✅ CHECKPOINT COMPLETE
================================================================================
```

## Documentation

- **Quick Start:** Read `CHECKPOINT-QUICK-START.md` in master repo
- **Full Standard:** Read `docs/CHECKPOINT-PROCESS-STANDARD.md` in coditect-core
- **Implementation:** Read `CHECKPOINT-PROCESS-IMPLEMENTATION.md` in master repo

## Key Rules

### ✅ DO
- Use the standardized checkpoint process for all work
- Create descriptive sprint descriptions
- Check audit trail after checkpoint completes
- Allow time between checkpoints (30+ minutes)

### ❌ DON'T
- Use plain `git push` (leaves submodules uncommitted)
- Push only parent repo (breaks distributed intelligence)
- Skip the checkpoint process (loses audit trail)
- Create checkpoints for trivial changes (group related work)

## Verification

After running checkpoint, verify it worked:

```bash
# Check latest commits
git log --oneline -3

# Should show:
#  109b8f2 Document standardized checkpoint process
#  44729e0 Update coditect-core: Add checkpoint-with-submodules...
#  6cae947 Add standardized checkpoint process

# Check audit trail
cat MEMORY-CONTEXT/audit-logs/2025-11-22T*.json | jq '.operation_summary'

# Should show:
# {
#   "total_operations": 46,
#   "by_status": {
#     "success": 44,
#     "warning": 0,
#     "error": 0,
#     "info": 2
#   }
# }
```

## Questions?

Refer to:
1. **"How do I use checkpoint?"** → `CHECKPOINT-QUICK-START.md`
2. **"What if something goes wrong?"** → See troubleshooting in `CHECKPOINT-PROCESS-STANDARD.md`
3. **"Why was this implemented?"** → Read `CHECKPOINT-PROCESS-IMPLEMENTATION.md`
4. **"Show me the code"** → `submodules/core/coditect-core/scripts/checkpoint-with-submodules.py`

---

**Remember:** Every session should end with a checkpoint to ensure work is saved and all repos are in consistent state.

**Status:** ✅ OPERATIONAL AND REQUIRED
**Copyright:** © 2025 AZ1.AI INC. All rights reserved.
