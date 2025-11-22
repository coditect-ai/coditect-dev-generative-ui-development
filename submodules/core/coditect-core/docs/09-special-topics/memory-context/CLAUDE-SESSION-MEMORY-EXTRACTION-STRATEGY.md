# Claude Code Session Memory Extraction Strategy

**Date:** November 22, 2025
**Status:** 🎯 SYSTEMATIC EXTRACTION PLAN
**Safety Level:** ⭐⭐⭐⭐⭐ (Highest - Read-only, fully reversible)

## Executive Summary

This document provides a **systematic, non-destructive strategy** for extracting unique messages from `~/.claude` session memory without risking session restoration or data integrity.

**Core Principles:**
1. ✅ **Read-Only Access** - Original files NEVER modified
2. ✅ **Complete Coverage** - Systematic processing of ALL 1,790+ items
3. ✅ **Zero Data Loss** - Everything preserved in multiple locations
4. ✅ **Verifiable** - Track exactly what was processed
5. ✅ **Reversible** - Can reprocess anytime, original files unchanged
6. ✅ **Safe Restoration** - Claude Code can still restore any session

---

## Part 1: Assessment & Inventory

### Step 1.1: Complete File Inventory

**Objective:** Create comprehensive manifest of ALL files to process

**Action:** Create inventory script that documents everything WITHOUT modifying anything

```bash
# Create inventory directory
mkdir -p MEMORY-CONTEXT/session-memory-extraction/inventory

# Generate complete manifest
python3 << 'EOF'
import json
from pathlib import Path
import os
from datetime import datetime

session_memory_root = Path.home() / ".claude"
inventory_file = Path("/Users/halcasteel/PROJECTS/coditect-rollout-master/MEMORY-CONTEXT/session-memory-extraction/inventory/complete-manifest.json")

inventory = {
    "extraction_date": datetime.now().isoformat(),
    "root_path": str(session_memory_root),
    "data_sources": {}
}

# 1. history.jsonl
history_file = session_memory_root / "history.jsonl"
if history_file.exists():
    lines = len(history_file.read_text().strip().split('\n'))
    inventory["data_sources"]["history.jsonl"] = {
        "path": str(history_file),
        "type": "jsonl",
        "line_count": lines,
        "size_bytes": os.path.getsize(history_file),
        "status": "NOT_PROCESSED",
        "checksum": None
    }

# 2. debug/ directory
debug_dir = session_memory_root / "debug"
if debug_dir.exists():
    debug_files = list(debug_dir.glob("*.txt"))
    inventory["data_sources"]["debug"] = {
        "path": str(debug_dir),
        "type": "directory",
        "file_count": len(debug_files),
        "files": [str(f) for f in debug_files],
        "status": "NOT_PROCESSED",
        "total_size_bytes": sum(os.path.getsize(f) for f in debug_files)
    }

# 3. file-history/ directory
fh_dir = session_memory_root / "file-history"
if fh_dir.exists():
    fh_items = list(fh_dir.iterdir())
    total_files = 0
    for item in fh_items:
        if item.is_dir():
            total_files += len(list(item.iterdir()))
    inventory["data_sources"]["file-history"] = {
        "path": str(fh_dir),
        "type": "directory",
        "subdirs": len(fh_items),
        "total_files": total_files,
        "status": "NOT_PROCESSED"
    }

# 4. todos/ directory
todos_dir = session_memory_root / "todos"
if todos_dir.exists():
    todos_files = list(todos_dir.glob("*.json"))
    inventory["data_sources"]["todos"] = {
        "path": str(todos_dir),
        "type": "directory",
        "file_count": len(todos_files),
        "status": "NOT_PROCESSED",
        "total_size_bytes": sum(os.path.getsize(f) for f in todos_files)
    }

# 5. shell-snapshots/ directory
shells_dir = session_memory_root / "shell-snapshots"
if shells_dir.exists():
    shell_files = list(shells_dir.glob("*.sh"))
    inventory["data_sources"]["shell-snapshots"] = {
        "path": str(shells_dir),
        "type": "directory",
        "file_count": len(shell_files),
        "status": "NOT_PROCESSED",
        "total_size_bytes": sum(os.path.getsize(f) for f in shell_files)
    }

# 6. session-env/ directory
sesenv_dir = session_memory_root / "session-env"
if sesenv_dir.exists():
    sesenv_items = list(sesenv_dir.iterdir())
    inventory["data_sources"]["session-env"] = {
        "path": str(sesenv_dir),
        "type": "directory",
        "item_count": len(sesenv_items),
        "status": "NOT_PROCESSED"
    }

# 7. projects/ directory
proj_dir = session_memory_root / "projects"
if proj_dir.exists():
    proj_items = list(proj_dir.iterdir())
    inventory["data_sources"]["projects"] = {
        "path": str(proj_dir),
        "type": "directory",
        "item_count": len(proj_items),
        "status": "NOT_PROCESSED"
    }

# Write inventory
inventory_file.parent.mkdir(parents=True, exist_ok=True)
with open(inventory_file, 'w') as f:
    json.dump(inventory, f, indent=2)

print(f"✅ Inventory created: {inventory_file}")
print(json.dumps(inventory, indent=2))

EOF
```

**Output:** Complete manifest in `MEMORY-CONTEXT/session-memory-extraction/inventory/complete-manifest.json`

### Step 1.2: Verify No Changes During Inventory

**Objective:** Baseline checksums to verify files don't change unexpectedly

```bash
# Create checksum file for verification
find ~/.claude -type f \( -name "*.jsonl" -o -name "*.json" -o -name "*.txt" -o -name "*.sh" \) \
  -exec sha256sum {} \; > MEMORY-CONTEXT/session-memory-extraction/inventory/baseline-checksums.txt

# Count total files
echo "Total files in ~/.claude to process:" $(find ~/.claude -type f | wc -l)
```

**Purpose:** Can verify at any time that original files haven't changed

---

## Part 2: Processing Strategy

### Step 2.1: Processing Order (Systematic)

**Process in this order (highest value → lowest risk):**

| Phase | Source | Item Count | Complexity | Priority | Estimated Messages |
|-------|--------|-----------|-----------|----------|-------------------|
| 1 | history.jsonl | 1,484 | 🟢 Easy | P0 | 600-800 |
| 2 | debug/ | 54 | 🟢 Easy | P0 | 300-400 |
| 3 | file-history/ | 91 | 🟡 Medium | P1 | 200-300 |
| 4 | todos/ | 120 | 🟡 Medium | P1 | 150-200 |
| 5 | shell-snapshots/ | 41 | 🟡 Medium | P2 | 41 snapshots |
| 6 | session-env/ | 38 | 🟡 Medium | P2 | Varies |
| 7 | projects/ | 16 | 🟡 Medium | P2 | Varies |

**Why this order:**
- Start with easiest, highest-value sources first
- Build confidence before moving to complex ones
- Low-risk phases prove the process works
- Can stop at any phase and still have captured valuable data

### Step 2.2: Per-Phase Processing Pattern

**For each phase:**

```
Phase X: {DataSource}
├─ Step X.1: Verify all files readable (no permission errors)
├─ Step X.2: Load reference checksums (verify unmodified)
├─ Step X.3: Extract messages/content (READ-ONLY)
├─ Step X.4: Deduplicate against existing MEMORY-CONTEXT
├─ Step X.5: Add new unique messages to store
├─ Step X.6: Create session index (provenance tracking)
├─ Step X.7: Log extraction details (processing record)
├─ Step X.8: Verify checksums (confirm no changes)
├─ Step X.9: Mark phase complete in manifest
└─ Step X.10: Commit to git with full documentation
```

---

## Part 3: Detailed Phase 1 Plan (history.jsonl)

### Phase 1: history.jsonl Processing

**File:** `~/.claude/history.jsonl`
**Format:** JSON Lines (1 JSON object per line)
**Size:** 1.0 MB
**Line Count:** 1,484
**Objective:** Extract 600-800 unique messages

#### Step 1.1: Pre-Flight Verification

```python
# Verify file is readable and unmodified
import hashlib
from pathlib import Path

history_file = Path.home() / ".claude" / "history.jsonl"

# 1. Check file exists and is readable
assert history_file.exists(), "history.jsonl not found"
assert history_file.stat().st_mode & 0o400, "history.jsonl not readable"

# 2. Get baseline checksum
with open(history_file, 'rb') as f:
    file_hash = hashlib.sha256(f.read()).hexdigest()

print(f"✅ File verified")
print(f"   Path: {history_file}")
print(f"   Size: {history_file.stat().st_size} bytes")
print(f"   SHA256: {file_hash}")

# 3. Verify against baseline
baseline_hash = "..."  # Load from baseline-checksums.txt
assert file_hash == baseline_hash, "File modified since baseline!"

print("✅ File unchanged since baseline - safe to process")
```

#### Step 1.2: Streaming Extraction (Memory-Safe)

```python
# Process line-by-line to avoid loading entire file in memory
import json
from datetime import datetime

history_file = Path.home() / ".claude" / "history.jsonl"
extraction_log = Path("/Users/halcasteel/PROJECTS/coditect-rollout-master/MEMORY-CONTEXT/session-memory-extraction/logs/phase1-extraction.jsonl")

extracted_count = 0
skipped_count = 0

with open(history_file, 'r') as f:
    for line_num, line in enumerate(f, 1):
        try:
            entry = json.loads(line)

            # Extract message components
            message = {
                "source_file": "history.jsonl",
                "source_line": line_num,
                "timestamp": entry.get("timestamp"),
                "project": entry.get("project"),
                "session_id": entry.get("sessionId"),
                "content": entry.get("display", ""),
                "type": "history_entry",
                "extraction_date": datetime.now().isoformat()
            }

            # Write to extraction log (for deduplication later)
            # ... (will add to dedup system)

            extracted_count += 1

        except json.JSONDecodeError as e:
            print(f"❌ Error on line {line_num}: {e}")
            skipped_count += 1
        except Exception as e:
            print(f"⚠️  Unexpected error on line {line_num}: {e}")
            skipped_count += 1

print(f"✅ Extraction complete:")
print(f"   Total lines: {line_num}")
print(f"   Extracted: {extracted_count}")
print(f"   Skipped: {skipped_count}")
print(f"   Success rate: {100*extracted_count/line_num:.1f}%")
```

#### Step 1.3: Deduplication Against MEMORY-CONTEXT

```python
# Use existing deduplication system
from pathlib import Path
import sys

# Load existing dedup system
sys.path.insert(0, str(Path("/Users/halcasteel/PROJECTS/coditect-rollout-master/submodules/core/coditect-core/scripts/core")))
from message_deduplicator import MessageDeduplicator

# Initialize dedup system
dedup_dir = Path("/Users/halcasteel/PROJECTS/coditect-rollout-master/MEMORY-CONTEXT/dedup_state")
dedup = MessageDeduplicator(storage_dir=dedup_dir)

# Process each extracted message
new_unique = 0
duplicates = 0

for message in extracted_messages:  # From step 1.2
    hash_value = sha256(message["content"].encode()).hexdigest()

    if hash_value not in dedup.global_hashes:
        # New unique message
        dedup.add_message(message)
        new_unique += 1
    else:
        # Duplicate
        duplicates += 1

print(f"✅ Deduplication complete:")
print(f"   New unique: {new_unique}")
print(f"   Duplicates: {duplicates}")
print(f"   Dedup rate: {100*duplicates/(new_unique+duplicates):.1f}%")
```

#### Step 1.4: Session Index Creation

```python
# Create mapping of message_id → original_file_location
session_index = {
    "phase": 1,
    "source": "history.jsonl",
    "processed_date": datetime.now().isoformat(),
    "total_messages_extracted": extracted_count,
    "total_messages_new_unique": new_unique,
    "total_messages_duplicates": duplicates,
    "message_locations": [
        {
            "message_id": sha256(msg["content"].encode()).hexdigest(),
            "source_file": "history.jsonl",
            "source_line": msg["source_line"],
            "timestamp": msg["timestamp"],
            "project": msg["project"],
            "session_id": msg["session_id"]
        }
        for msg in extracted_messages
    ]
}

# Save index
index_file = Path("/Users/halcasteel/PROJECTS/coditect-rollout-master/MEMORY-CONTEXT/session-memory-extraction/indexes/phase1-history-index.json")
with open(index_file, 'w') as f:
    json.dump(session_index, f, indent=2)

print(f"✅ Session index created: {index_file}")
```

#### Step 1.5: Verification

```bash
# Verify original file unchanged
sha256sum ~/.claude/history.jsonl
# Compare against baseline-checksums.txt

# Verify extraction logged
wc -l MEMORY-CONTEXT/session-memory-extraction/logs/phase1-extraction.jsonl

# Verify dedup added messages
grep -c "history_entry" MEMORY-CONTEXT/dedup_state/unique_messages.jsonl

# Verify index created
ls -lh MEMORY-CONTEXT/session-memory-extraction/indexes/phase1-history-index.json
```

#### Step 1.6: Git Commit

```bash
git add MEMORY-CONTEXT/session-memory-extraction/
git commit -m "Phase 1: Extract history.jsonl session memory

- Extracted 1,484 entries from ~/.claude/history.jsonl
- Identified 600-800 new unique messages
- Added to MEMORY-CONTEXT/dedup_state
- Created session index with full provenance
- Original file verified unchanged
- All files read-only, fully reversible

Extraction log: MEMORY-CONTEXT/session-memory-extraction/logs/phase1-extraction.jsonl
Session index: MEMORY-CONTEXT/session-memory-extraction/indexes/phase1-history-index.json"
```

---

## Part 4: Directory Structure

### Session Memory Extraction Organization

```
MEMORY-CONTEXT/
└── session-memory-extraction/           # NEW: Session memory extraction system
    ├── inventory/
    │   ├── complete-manifest.json       # All files to process
    │   └── baseline-checksums.txt       # Verify no changes
    │
    ├── logs/
    │   ├── phase1-extraction.jsonl      # Extracted messages from history.jsonl
    │   ├── phase2-extraction.jsonl      # Extracted messages from debug/
    │   ├── phase3-extraction.jsonl      # Extracted messages from file-history/
    │   ├── phase4-extraction.jsonl      # Extracted messages from todos/
    │   ├── phase5-extraction.jsonl      # Extracted from shell-snapshots/
    │   ├── processing-summary.txt       # Overall stats
    │   └── verification-report.txt      # Checksum verification results
    │
    ├── indexes/
    │   ├── phase1-history-index.json    # Message location mapping for phase 1
    │   ├── phase2-debug-index.json      # Message location mapping for phase 2
    │   ├── phase3-filehistory-index.json # ... phase 3
    │   ├── phase4-todos-index.json      # ... phase 4
    │   ├── phase5-shells-index.json     # ... phase 5
    │   └── complete-session-index.json  # Combined index all phases
    │
    ├── extraction-strategy.md           # This document
    └── extraction-progress.json         # Track which phases completed
```

---

## Part 5: Safety Guardrails

### Guardrail 1: File Integrity Checking

**Before each extraction:**
```bash
# Verify original files unchanged
sha256sum ~/.claude/history.jsonl > /tmp/check.txt
diff /tmp/check.txt MEMORY-CONTEXT/session-memory-extraction/inventory/baseline-checksums.txt
```

**After each extraction:**
```bash
# Re-verify files unchanged
sha256sum ~/.claude/history.jsonl >> MEMORY-CONTEXT/session-memory-extraction/inventory/verification-checksums.txt
```

### Guardrail 2: Extraction Verification

**For each phase:**
1. Count lines/entries in source
2. Count extracted messages
3. Verify no data loss: `extracted >= expected - 5%`

### Guardrail 3: Deduplication Verification

**Verify dedup system:**
1. All new unique messages added to `unique_messages.jsonl`
2. All hashes added to `global_hashes.json`
3. Watermarks updated for this extraction

### Guardrail 4: Reversibility Verification

**At any time, can:**
1. Re-read original files (never modified)
2. Re-run extraction (idempotent)
3. Restore to previous dedup state (git history)

### Guardrail 5: Session Restoration Verification

**Verify Claude Code can still restore sessions:**
1. Test loading a session from `~/.claude/todos/`
2. Verify file permissions unchanged
3. Verify no symlinks broken

---

## Part 6: Execution Checklist

### Pre-Extraction (Day 0)

- [ ] Read this entire strategy document
- [ ] Create inventory: `python3 step1-inventory.py`
- [ ] Create baseline checksums: `step1-checksums.sh`
- [ ] Review manifest: `cat MEMORY-CONTEXT/session-memory-extraction/inventory/complete-manifest.json`
- [ ] Commit inventory: `git add MEMORY-CONTEXT/session-memory-extraction/inventory && git commit -m "..."`

### Phase 1: history.jsonl (Day 1)

- [ ] Pre-flight check: verify file readable
- [ ] Verify baseline checksum
- [ ] Extract messages: `python3 phase1-extract-history.py`
- [ ] Review extraction log
- [ ] Deduplicate: run dedup system
- [ ] Create session index
- [ ] Post-flight check: verify file unchanged
- [ ] Review stats: X new unique, Y duplicates
- [ ] Commit to git with detailed message

### Phase 2: debug/ (Day 2)

- [ ] (Repeat pattern from Phase 1)

### Phase 3: file-history/ (Day 3)

- [ ] (Repeat pattern from Phase 1)

### Phase 4: todos/ (Day 4)

- [ ] (Repeat pattern from Phase 1)

### Phase 5+: shell-snapshots, session-env, projects (Day 5+)

- [ ] (Repeat pattern from Phase 1)

### Post-Extraction (Day 6+)

- [ ] Review complete-session-index.json
- [ ] Create restoration test plan
- [ ] Verify Claude Code sessions still restore
- [ ] Final verification report
- [ ] Update documentation

---

## Part 7: Recovery Plan

### If Something Goes Wrong

**Scenario 1: File accidentally modified**
- Restore from git: `git checkout ~/.claude/...` (NO - original files not in git!)
- Use Time Machine / system backups
- Files are read-only anyway (should prevent accidental modification)

**Scenario 2: Extraction incomplete**
- Check logs for errors
- Retry the phase (idempotent operation)
- No data loss - original files untouched

**Scenario 3: Dedup system corrupted**
- Restore from git: `git checkout MEMORY-CONTEXT/dedup_state/`
- Re-run deduplication
- All original data still in `~/.claude`

**Scenario 4: Session can't be restored**
- Original files in `~/.claude` untouched
- Claude Code can restore from backups
- Extraction process doesn't affect session restoration

---

## Part 8: Success Metrics

### Objective Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| **Files processed** | 1,790+ items | Count in inventory |
| **Messages extracted** | 1,250-1,700 | Count in extraction logs |
| **New unique** | 600-800 (phase 1 alone) | Count added to dedup system |
| **File integrity** | 100% unchanged | Checksum verification |
| **Zero data loss** | 100% | Compare original vs extracted counts |
| **Session restoration** | 100% working | Test restore from ~/.claude |
| **Reversibility** | 100% | Can reprocess anytime |

### Subjective Metrics

- ✅ All files documented in manifest
- ✅ Complete provenance tracking (know origin of each message)
- ✅ Safe to expand to other projects' ~/.claude folders
- ✅ Process can be automated for future sessions
- ✅ Zero risk to any part of system

---

## Part 9: Future Automation

### After successful Phase 1-5:

```bash
# Weekly automated processing
0 2 * * 0 /usr/local/bin/extract-session-memory.sh

# Monthly verification
0 3 1 * * /usr/local/bin/verify-session-memory.sh

# Quarterly restoration test
0 4 1 */3 * /usr/local/bin/test-session-restoration.sh
```

---

## Summary

This strategy ensures:

✅ **Systematic** - All 1,790+ items processed in order
✅ **Non-Destructive** - Original files never modified
✅ **Verifiable** - Every step logged and checksummed
✅ **Reversible** - Can reprocess anytime
✅ **Safe** - Multiple guardrails prevent data loss
✅ **Complete** - Full provenance tracking
✅ **Scalable** - Can automate weekly

**Result:** 1,250-1,700 new unique messages safely extracted and backed up, while keeping `~/.claude` in perfect condition for Claude Code to restore sessions anytime.

---

**Document Version:** 1.0
**Created:** November 22, 2025
**Status:** Ready for Phase 1 execution
**Next Step:** Run pre-extraction checklist
