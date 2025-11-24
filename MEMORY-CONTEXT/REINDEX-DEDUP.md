# Deduplication Reindexing Guide

## Overview

The deduplication system maintains several index files for fast lookups:

- `global_hashes.json` - Set of all unique message content hashes (695KB, 10,472 hashes)
- `checkpoint_index.json` - Mapping of checkpoints to message hashes (776KB, 127 checkpoints)
- `unique_messages.jsonl` - Source of truth, append-only log (7.8MB, 10,472 messages)

Sometimes you may need to **rebuild the indices** from the source data.

## When to Reindex

Use reindexing when:

1. **Index corruption** - If `global_hashes.json` or `checkpoint_index.json` become corrupted
2. **Manual changes** - After manually editing `unique_messages.jsonl`
3. **Integrity verification** - To verify indices match the source data
4. **Performance optimization** - To rebuild indices with improved structure
5. **Recovery** - After restoring from backup

## Quick Start

### Simple Method (Recommended)

```bash
cd MEMORY-CONTEXT
./reindex-dedup.sh
```

This will:
- ✅ Automatically backup existing indices
- ✅ Rebuild from `unique_messages.jsonl`
- ✅ Show progress every 1,000 messages
- ✅ Display statistics when complete

### Without Backup (Faster)

```bash
cd MEMORY-CONTEXT
./reindex-dedup.sh --no-backup
```

Skips backup creation for faster execution (useful if you already have backups).

## Advanced Usage

### Direct Python Script

```bash
cd MEMORY-CONTEXT

# With backup (default)
python3 ../submodules/core/coditect-core/scripts/core/message_deduplicator.py \
  --reindex \
  --storage-dir dedup_state

# Without backup
python3 ../submodules/core/coditect-core/scripts/core/message_deduplicator.py \
  --reindex \
  --storage-dir dedup_state \
  --no-backup

# With verbose logging
python3 ../submodules/core/coditect-core/scripts/core/message_deduplicator.py \
  --reindex \
  --storage-dir dedup_state \
  --verbose
```

## What Happens During Reindex

1. **Backup Creation** (if enabled)
   - Creates timestamped backups:
     - `global_hashes.json.backup-YYYYMMDD-HHMMSS`
     - `checkpoint_index.json.backup-YYYYMMDD-HHMMSS`

2. **Index Reset**
   - Clears all in-memory indices
   - Prepares for rebuild

3. **Source Scan**
   - Reads through `unique_messages.jsonl` line by line
   - Extracts message hashes and checkpoint IDs
   - Progress logged every 1,000 messages

4. **Index Rebuild**
   - Rebuilds `global_hashes.json` with all unique hashes
   - Rebuilds `checkpoint_index.json` with checkpoint mappings
   - Saves both indices to disk

5. **Statistics**
   - Reports:
     - Messages processed (e.g., 10,472)
     - Unique hashes (e.g., 10,472)
     - Checkpoints found (e.g., 127)

## Performance

**Current Dataset:**
- **Messages:** 10,472
- **Checkpoints:** 127
- **Time:** <1 second
- **Backup Size:** 1.5MB (both indices combined)

**Scalability:**
- Processes ~10,000 messages/second
- Memory efficient (streaming read)
- Suitable for datasets with millions of messages

## Verification

After reindexing, verify the indices:

```bash
# Check global hashes count
cat dedup_state/global_hashes.json | python3 -c "import sys, json; print(len(json.load(sys.stdin)))"

# Check checkpoint index
cat dedup_state/checkpoint_index.json | python3 -c "import sys, json; print(len(json.load(sys.stdin)))"

# Check unique messages
wc -l dedup_state/unique_messages.jsonl
```

All three should report consistent counts.

## Backup Management

Backups are created with timestamps and are **not automatically deleted**. To clean up old backups:

```bash
# List all backups
ls -lh dedup_state/*.backup-*

# Remove backups older than 7 days
find dedup_state -name "*.backup-*" -mtime +7 -delete
```

## Troubleshooting

### "No messages file found"

**Problem:** `unique_messages.jsonl` doesn't exist

**Solution:** No deduplication data to reindex. This is the source of truth - if it's missing, you need to restore from backup or re-run deduplication from scratch.

### "Invalid JSON, skipping"

**Problem:** Corrupted line in `unique_messages.jsonl`

**Solution:** The reindex process will skip corrupted lines and continue. Check the logs for specific line numbers, then manually inspect/repair those lines.

### Mismatched counts

**Problem:** Message count doesn't match unique hash count

**Solution:** This indicates duplicate hashes in the source file, which shouldn't happen. Investigate and potentially run integrity checks.

## Related Scripts

- `export-dedup-with-status.py` - Export and deduplicate conversations
- `message_deduplicator.py` - Core deduplication logic
- `conversation_deduplicator.py` - Conversation-level deduplication

## Documentation

For more information:
- [DEDUP-STORAGE-FORMAT.md](../submodules/core/coditect-core/docs/DEDUP-STORAGE-FORMAT.md) - Storage format specification
- [message_deduplicator.py](../submodules/core/coditect-core/scripts/core/message_deduplicator.py) - Source code

---

**Last Updated:** 2025-11-24
**Author:** AZ1.AI CODITECT
**License:** MIT
