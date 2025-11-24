# Deduplication Workflow Guide

## Quick Reference

This guide shows the complete deduplication workflow from export to git sync.

## The Problem

After conversation exports, you have:
- New messages in export files
- Dedup state that needs updating
- Git changes in multiple places:
  - `MEMORY-CONTEXT/dedup_state/` (master repo)
  - Potentially changes in submodules
- Manual git workflow is tedious and error-prone

## The Solution

**One command to rule them all:**

```bash
cd MEMORY-CONTEXT
./dedup-and-sync.sh
```

## What It Does

### Step 1: Deduplication
- Runs reindex on dedup state
- Rebuilds indices from `unique_messages.jsonl`
- Creates backups automatically
- Shows progress every 1,000 messages

**Current Dataset:**
- 10,472 unique messages
- 127 checkpoints
- ~1 second execution time

### Step 2: Submodule Sync
- Checks all 46 submodules for changes
- Auto-commits changes in each submodule
- Auto-pushes to origin
- Uses conventional commit format

**Example commit message:**
```
chore: Auto-sync after deduplication

Automated commit from dedup-and-sync.sh
Timestamp: 2025-11-24 19:30:00 UTC

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Step 3: Master Repo Sync
- Checks for submodule pointer updates
- Checks for other changes in master repo
- Auto-commits all changes
- Auto-pushes to origin

**Example commit message (with submodule updates):**
```
chore: Update submodule pointers after dedup sync

Submodules updated:
- submodules/core/coditect-core
- submodules/cloud/coditect-cloud-backend

Automated commit from dedup-and-sync.sh
Timestamp: 2025-11-24 19:30:05 UTC

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Step 4: Summary
Shows:
- Number of submodules with changes
- Number of submodules committed
- Number of submodules pushed
- Master repo status

## Usage

### Standard Workflow (Recommended)

```bash
cd MEMORY-CONTEXT
./dedup-and-sync.sh
```

**What happens:**
1. ✅ Dedup with automatic backup
2. ✅ Check all submodules
3. ✅ Commit and push submodule changes
4. ✅ Update master repo
5. ✅ Commit and push master changes
6. ✅ Show summary

### Fast Workflow (No Backup)

```bash
cd MEMORY-CONTEXT
./dedup-and-sync.sh --no-backup
```

Use when:
- You already have recent backups
- You want faster execution
- You're confident in the data

**Time Savings:** ~100ms (backup creation skipped)

## Individual Components

If you need to run steps individually:

### 1. Reindex Only

```bash
cd MEMORY-CONTEXT
./reindex-dedup.sh
```

### 2. Git Status Check

```bash
# Check master repo
git status

# Check all submodules
git submodule foreach 'echo "=== $name ===" && git status'
```

### 3. Manual Submodule Commit

```bash
cd submodules/path/to/submodule
git add -A
git commit -m "chore: Manual sync"
git push
cd ../../..
```

### 4. Manual Master Commit

```bash
git add -A
git commit -m "chore: Update after submodule sync"
git push
```

## Common Scenarios

### Scenario 1: After /export-dedup Command

You just ran `/export-dedup` in Claude Code and have new export files.

**Solution:**
```bash
cd MEMORY-CONTEXT
./dedup-and-sync.sh
```

**Result:**
- Dedup state updated
- All changes committed and pushed
- Ready for next session

### Scenario 2: Multiple Export Files to Process

You have 5+ export files waiting to be processed.

**Solution:**
```bash
cd MEMORY-CONTEXT

# Process each export manually first
python3 ../submodules/core/coditect-core/scripts/export-dedup-with-status.py \
  --file exports/file1.txt

python3 ../submodules/core/coditect-core/scripts/export-dedup-with-status.py \
  --file exports/file2.txt

# Then sync everything
./dedup-and-sync.sh
```

**Alternative:**
```bash
# Use batch processing
cd ../submodules/core/coditect-core/scripts
python3 deduplicate_export.py --batch /path/to/exports/

cd ../../../../MEMORY-CONTEXT
./dedup-and-sync.sh
```

### Scenario 3: Reindex After Manual Edits

You manually edited `unique_messages.jsonl` and need to rebuild indices.

**Solution:**
```bash
cd MEMORY-CONTEXT
./reindex-dedup.sh  # Just reindex, no git sync
```

If you want git sync too:
```bash
./dedup-and-sync.sh  # Reindex + git sync
```

### Scenario 4: Check What Changed Before Committing

You want to see what changed before auto-committing.

**Solution:**
```bash
cd MEMORY-CONTEXT

# Check dedup state changes
git status dedup_state/

# Check all submodules
git submodule foreach 'git status'

# Then decide:
./dedup-and-sync.sh  # If you want to proceed
```

## Output Examples

### Successful Run

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Automated Dedup and Git Sync Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Running deduplication...
🔄 Reindexing deduplication state...
Storage: /path/to/dedup_state

✅ Reindex completed successfully!

Results:
  Messages processed: 10472
  Unique hashes: 10472
  Checkpoints found: 127
  Status: success

✓ Deduplication completed successfully

Step 2: Processing submodules...
Found 46 submodules

▶ Checking submodule: submodules/core/coditect-core
  Changes detected
  M  scripts/core/message_deduplicator.py
  ✓ Changes committed
  ✓ Changes pushed to origin/main

▶ Checking submodule: submodules/cloud/coditect-cloud-backend
  ✓ No changes

[... more submodules ...]

Step 3: Processing master repository...
Changes detected in master repository
 M MEMORY-CONTEXT/dedup_state/global_hashes.json
 M MEMORY-CONTEXT/dedup_state/checkpoint_index.json
 M submodules/core/coditect-core
✓ Master repository changes committed
✓ Master repository changes pushed to origin/main

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Submodules with changes: 1
Submodules committed:    1
Submodules pushed:       1

✅ Workflow completed successfully!
```

### No Changes

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Automated Dedup and Git Sync Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Running deduplication...
✅ Reindex completed successfully!

Step 2: Processing submodules...
Found 46 submodules

▶ Checking submodule: submodules/core/coditect-core
  ✓ No changes

[... all submodules clean ...]

Step 3: Processing master repository...
✓ No changes in master repository

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Submodules with changes: 0
Submodules committed:    0
Submodules pushed:       0

✅ Workflow completed successfully!
```

## Troubleshooting

### "Failed to push changes"

**Problem:** Network issue or authentication failure

**Solution:**
```bash
# Check GitHub authentication
gh auth status

# Or push manually
cd submodules/path/to/failing/submodule
git push origin main
```

### "Deduplication failed"

**Problem:** Corrupted dedup state or missing source file

**Solution:**
```bash
cd MEMORY-CONTEXT

# Check if unique_messages.jsonl exists
ls -lh dedup_state/unique_messages.jsonl

# If missing, restore from backup
cp dedup_state/unique_messages.jsonl.backup-* dedup_state/unique_messages.jsonl

# Retry
./dedup-and-sync.sh
```

### Submodule in detached HEAD state

**Problem:** Submodule not on a branch

**Solution:**
```bash
cd submodules/path/to/submodule
git checkout main
git pull
cd ../../..

# Retry workflow
cd MEMORY-CONTEXT
./dedup-and-sync.sh
```

### "Your branch is ahead of 'origin/main'"

This is expected! The script has committed changes but hasn't pushed yet if you see this message.

**Solution:** The script handles this automatically. If push failed, check network/auth.

## Best Practices

1. **Run after every export session**
   - Keeps dedup state current
   - Prevents git drift
   - Maintains clean history

2. **Use standard workflow (with backup)**
   - Backups are cheap (1.5MB)
   - Recovery is expensive
   - Peace of mind

3. **Check summary output**
   - Verify expected submodules committed
   - Look for push failures
   - Note which repos changed

4. **Monitor backup accumulation**
   ```bash
   # Check backup count
   ls -1 dedup_state/*.backup-* | wc -l

   # Clean old backups (>7 days)
   find dedup_state -name "*.backup-*" -mtime +7 -delete
   ```

5. **Validate after workflow**
   ```bash
   # Ensure working tree clean
   git status

   # Ensure submodules clean
   git submodule foreach 'git status'

   # Should show: "nothing to commit, working tree clean"
   ```

## Performance

**Typical Execution Time:**
- Dedup reindex: <1 second
- Git operations: 2-5 seconds per repo with changes
- Total for clean run: ~5 seconds
- Total with 3 submodule changes: ~20 seconds

**Scalability:**
- Tested with 46 submodules
- Handles 10,472 messages efficiently
- Network is the bottleneck (push operations)

## Integration

### With /export-dedup Command

Add to your workflow:
```bash
1. /export-dedup         # In Claude Code
2. cd MEMORY-CONTEXT
3. ./dedup-and-sync.sh   # Automate the rest
```

### With Cron Job

```bash
# Add to crontab for automatic sync
# Every 6 hours
0 */6 * * * cd /path/to/MEMORY-CONTEXT && ./dedup-and-sync.sh --no-backup
```

### With GitHub Actions

```yaml
name: Automated Dedup Sync
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  dedup-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive
      - name: Run dedup sync
        run: |
          cd MEMORY-CONTEXT
          ./dedup-and-sync.sh --no-backup
```

## Related Documentation

- [REINDEX-DEDUP.md](REINDEX-DEDUP.md) - Reindex details
- [export-dedup-status.txt](export-dedup-status.txt) - Dedup status tracking
- [../scripts/CLAUDE.md](../scripts/CLAUDE.md) - Script automation guide

---

**Last Updated:** 2025-11-24
**Author:** AZ1.AI CODITECT
**License:** MIT
