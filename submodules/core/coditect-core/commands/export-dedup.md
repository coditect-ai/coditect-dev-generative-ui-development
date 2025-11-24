---
name: export-dedup
description: Automated export deduplication and checkpoint creation
version: 2.0
category: workflow
tags: [export, deduplication, checkpoint, automation]
automation_level: fully_automated
---

# Export Deduplication & Checkpoint Workflow

**INSTRUCTIONS FOR CLAUDE: Automatically execute the export deduplication script below.**

This command will:
1. Find all export files (root + MEMORY-CONTEXT)
2. Deduplicate messages using SHA-256 hashing
3. Archive processed exports
4. Create checkpoint with git commit
5. Prompt you to run /compact

## Automatic Execution with Guaranteed Status Report

**Execute this wrapper script immediately - GUARANTEES visible status output:**

```python
import subprocess
import sys

# Use the new wrapper that guarantees output display
result = subprocess.run([
    "python3", "scripts/export-dedup-with-status.py"
], cwd=".", capture_output=False, text=True)

# Exit with same code
sys.exit(result.returncode)
```

**This wrapper ensures:**
- ✅ All output is displayed immediately to your terminal
- ✅ Complete execution report is printed to console
- ✅ Full report is ALSO logged to `MEMORY-CONTEXT/export-dedup-status.txt`
- ✅ Easy to verify what happened (no silent failures)
- ✅ Status log accumulates all runs for audit trail

---

**✨ Fully automated with auto-archive!**

## Quick Start (Fully Automated)

```bash
# After running /export, use automated mode:
python3 scripts/export-dedup.py --yes --description "Your description" --auto-compact

# Or let it auto-generate description:
python3 scripts/export-dedup.py -y --auto-compact
```

## How export-dedup Works (Step-by-Step)

When you run `python3 scripts/export-dedup.py`, here's exactly what happens:

### Step 1: Intelligent Export File Search

The script searches **multiple locations recursively** to find ALL export files:

**Locations searched:**
1. **Repo root** (shallow) - e.g., `/path/to/project/*.txt`
2. **MEMORY-CONTEXT/** (shallow) - e.g., `MEMORY-CONTEXT/*EXPORT*.txt`
3. **Current working directory** (recursive) - wherever you ran the command
4. **Submodules/** (recursive) - all submodule directories
5. **Temp locations** (last 24h only):
   - `~/Downloads/*EXPORT*.txt`
   - `/tmp/*EXPORT*.txt`
   - `~/Desktop/*EXPORT*.txt`

**Smart filtering:**
- **Excludes**: `.git/`, `node_modules/`, `venv/`, `exports-archive/` (already processed)
- **Deduplicates by inode**: Handles symlinks/hardlinks correctly
- **Permission handling**: Skips files it can't read (no errors)
- **Sorts by age**: Newest export first

**Result**: List of ALL export files found, sorted by modification time (newest → oldest)

### Step 2: Message Deduplication (The Core Magic)

For **each** export file found, the script:

1. **Parses the export file** using `parse_claude_export_file()`
   - Reads the raw text export from `/export` command
   - Extracts individual messages (user, assistant, tool calls, results)
   - Preserves full context including code, decisions, errors

2. **Generates unique message IDs** using SHA-256 content hashing
   - Each message → SHA-256 hash of: `role + content + timestamp`
   - Hash is deterministic (same message = same hash)
   - Even 1 character change = completely different hash

3. **Checks against global unique message store**
   - Loads existing hashes from `MEMORY-CONTEXT/dedup_state/global_hashes.json`
   - Contains ALL unique messages from ALL previous sessions
   - Currently stores 3,771+ unique messages

4. **Filters duplicates**
   - If hash exists in global store → **SKIP** (already seen)
   - If hash is new → **ADD** to global store
   - Updates `unique_messages.jsonl` with new messages

5. **Updates session watermark**
   - Tracks highest message index processed for this session
   - Stored in `watermarks.json`
   - Enables incremental processing (only new messages next time)

6. **Stores conversation log**
   - Records which messages belong to which session
   - Enables perfect session reconstruction later
   - Stored in `conversation_log.jsonl`

**Result**:
- **New unique messages** stored globally
- **Duplicate messages** filtered out
- **Statistics** tracked (total, new, duplicates, dedup rate)

### Step 3: Archive Export Files

**What happens:**
- Moves ALL processed export files to `MEMORY-CONTEXT/exports-archive/`
- Keeps workspace root clean
- Prevents re-processing same exports
- Preserves exports (doesn't delete them)

**If file exists in archive:**
- Adds timestamp: `filename-20251118-153045.txt`
- Never overwrites existing archives

**Can be disabled:** Use `--no-archive` to keep exports in place

### Step 4: Create Checkpoint

**What happens:**
1. Runs `scripts/create-checkpoint.py`
2. Generates checkpoint document with:
   - Git status
   - Submodule states
   - Recent commits
   - Changed files
   - Deduplication statistics
3. Creates git commit with standardized message
4. Updates README.md with checkpoint reference

**Checkpoint description:**
- Uses `--description` if provided
- Prompts interactively if not provided
- Auto-generates "Automated export and deduplication" if `--yes` flag used

### Step 5: Summary & /compact Prompt

**Displays:**
- 📊 Deduplication summary (new messages, global total, storage location)
- 📁 Archive summary (location, number of files moved)
- 📝 Checkpoint description
- ⚠️ **Prompt to run /compact** (if `--auto-compact` flag used)

**Why /compact is safe now:**
- All messages stored in `dedup_state/unique_messages.jsonl`
- Export files archived to `exports-archive/`
- Checkpoint committed to git
- Running `/compact` frees context WITHOUT data loss

## Why This Prevents Data Loss

1. **Before /compact runs:**
   - You run `/export` → captures FULL conversation
   - Script processes export → extracts unique messages
   - Stores globally in `MEMORY-CONTEXT/dedup_state/`

2. **Global unique message store:**
   - 3,771+ messages stored (and growing)
   - SHA-256 hashing ensures perfect deduplication
   - Messages stored ONCE even if they appear in 10 different exports

3. **Perfect reconstruction:**
   - `conversation_log.jsonl` tracks message→session mapping
   - Any session can be reconstructed 100% from unique messages
   - Watermarks enable resuming from last processed message

4. **After /compact:**
   - Context is freed in Claude Code
   - BUT messages are in git (`unique_messages.jsonl`)
   - Next session can load relevant context from deduplicated store
   - Zero catastrophic forgetting!

## New Features

### ✅ Automated Mode (`--yes` / `-y`)
- No interactive prompts (perfect for scripts/automation)
- Auto-accepts old exports (still processes them)
- Auto-generates checkpoint description if not provided

### ✅ Auto-Archive
- Moves processed exports to `MEMORY-CONTEXT/exports-archive/`
- Keeps workspace root clean
- Prevents re-processing same exports
- Can disable with `--no-archive`

### ✅ Multi-Location Search
- Searches repo root for `*EXPORT*.txt`
- Searches `MEMORY-CONTEXT/` for `*EXPORT*.txt`
- Processes all found exports (not just latest)
- Removes duplicates automatically

### ✅ Better Error Handling
- Catches `EOFError` in non-interactive environments
- Shows full traceback on failures
- Continues on archive failures (doesn't abort)

## Arguments

All arguments are optional:

- `--description "Your description"` - Checkpoint description (auto-generated if not provided)
- `--checkpoint-only` - Skip deduplication, just create checkpoint
- `--auto-compact` - Show compact reminder after completion
- `-y` / `--yes` - Skip all interactive prompts (automation mode)
- `--no-archive` - Don't move exports to archive (keep in place)

## Usage Examples

### Interactive Mode (Original Behavior)
```python
import subprocess
subprocess.run(["python3", "scripts/export-dedup.py", "--auto-compact"])
# Will prompt for confirmation if export is old
# Will prompt for checkpoint description
```

### Automated Mode (New)
```python
import subprocess
subprocess.run([
    "python3", "scripts/export-dedup.py",
    "--yes",  # Skip all prompts
    "--description", "Project Intelligence Platform submodule created",
    "--auto-compact"
])
# Fully automated, no prompts, archives exports
```

### Minimal Automation
```python
import subprocess
subprocess.run([
    "python3", "scripts/export-dedup.py",
    "-y"  # Just auto-accept, use default description
])
# Auto-description: "Automated export and deduplication"
```

### Skip Archive (Keep Exports)
```python
import subprocess
subprocess.run([
    "python3", "scripts/export-dedup.py",
    "--yes",
    "--no-archive"  # Don't move exports
])
# Processes exports but leaves them in place
```

## Output Example

```
============================================================
CODITECT Export & Deduplicate Workflow
============================================================

Step 1: Looking for export files...
✓ Found 2 export file(s)
  Latest: 2025-11-18-EXPORT-PROJECTS-coditect-rollout-master-coditect-project-intelligenc.txt
✓ Recent export (< 5 min old)

Step 2: Deduplicating messages...

  Deduplication Results:
    Total messages: 54
    New unique: 54
    Duplicates filtered: 0
    Dedup rate: 0.0%
    Global unique count: 1655

Step 3: Archiving export files...
  ✓ Archived: 2025-11-18-EXPORT-PROJECTS-coditect-rollout-master-coditect-project-intelligenc.txt → MEMORY-CONTEXT/exports-archive/...
  ✓ Archived: 2025-11-17-EXPORT-PROJECTS-coditect-rollout-master-2117ET.txt → MEMORY-CONTEXT/exports-archive/...

  Total archived: 2 file(s)

Step 4: Creating checkpoint...
✓ Checkpoint created successfully

============================================================
✅ Export and deduplication complete!
============================================================

📊 Deduplication Summary:
   - New unique messages: 54
   - Total unique messages: 1655
   - Storage: MEMORY-CONTEXT/dedup_state

📁 Export(s) archived:
   - Location: MEMORY-CONTEXT/exports-archive
   - Files: 2 export(s) moved

📝 Checkpoint created: Project Intelligence Platform submodule created

⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

💡 Safe to compact now!

   Run: /compact

   This will free up context space while
   preserving all data in the checkpoint.

⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
```

## Deduplication State Files (The Magic Behind the Scenes)

The script maintains several files in `MEMORY-CONTEXT/dedup_state/`:

### 1. `unique_messages.jsonl` (3,771+ messages, 3.8 MB)

**What it stores:** Every unique message ever seen across ALL sessions

**Format:** JSON Lines (one message per line)
```json
{"role": "user", "content": "...", "timestamp": "2025-11-18T...", "hash": "abc123..."}
{"role": "assistant", "content": "...", "timestamp": "2025-11-18T...", "hash": "def456..."}
```

**Why important:**
- Global deduplication store
- Messages stored ONCE even if they appear in 10 exports
- Perfect reconstruction possible (all data preserved)

### 2. `global_hashes.json` (106 KB)

**What it stores:** SHA-256 hash → message index mapping

**Format:** JSON object
```json
{
  "abc123...": 0,
  "def456...": 1,
  "ghi789...": 2
}
```

**Why important:**
- Fast duplicate detection (O(1) lookup)
- No need to read all messages to check if one exists
- Enables efficient incremental processing

### 3. `watermarks.json` (315 bytes)

**What it stores:** Highest message index processed per session

**Format:** JSON object
```json
{
  "2025-11-18-coditect-cloud-backend": 73,
  "2025-11-18-project-plan-created": 93
}
```

**Why important:**
- Tracks progress per session
- Enables resuming from last processed message
- Prevents re-processing same messages

### 4. `conversation_log.jsonl` (965 KB)

**What it stores:** Session → message mapping (which messages belong to which session)

**Format:** JSON Lines
```json
{"session_id": "2025-11-18-...", "message_index": 0, "timestamp": "..."}
{"session_id": "2025-11-18-...", "message_index": 1, "timestamp": "..."}
```

**Why important:**
- Enables perfect session reconstruction
- Can rebuild any session from unique messages
- Supports session-specific queries

### 5. `content_hashes.json` (109 KB)

**What it stores:** Content hash → full SHA-256 mapping

**Format:** JSON object
```json
{
  "content_hash_abc": "full_sha256_hash_abc123..."
}
```

**Why important:**
- Collision detection
- Content-based deduplication
- Ensures message integrity

### 6. `checkpoint_index.json` (298 KB)

**What it stores:** Checkpoint metadata and references

**Format:** JSON object mapping checkpoint IDs to metadata

**Why important:**
- Links checkpoints to deduplicated messages
- Enables checkpoint-based session restoration
- Supports time-based queries

## Archive Directory Structure

After running:
```
MEMORY-CONTEXT/
├── exports-archive/          # Processed exports (moved here)
│   ├── 2025-11-18-EXPORT-coditect-cloud-backend.txt
│   ├── 2025-11-18-EXPORT-project-plan-created.txt
│   └── ... (all processed exports preserved)
│
├── dedup_state/              # Deduplication engine state
│   ├── unique_messages.jsonl       # 3,771+ unique messages (3.8 MB)
│   ├── global_hashes.json          # Hash → index mapping (106 KB)
│   ├── watermarks.json             # Session progress tracking (315 B)
│   ├── conversation_log.jsonl      # Session → message mapping (965 KB)
│   ├── content_hashes.json         # Content hashing (109 KB)
│   └── checkpoint_index.json       # Checkpoint metadata (298 KB)
│
└── sessions/                 # Session-specific exports (if used)
```

**Total dedup state size:** ~5.3 MB for 3,771 messages across 6 sessions
**Efficiency:** Each message stored ONCE, referenced by multiple sessions

## Best Practices

1. **Always run `/export` first** - Captures current conversation state
2. **Use `--yes` for automation** - No interactive prompts needed
3. **Add `--description`** - Makes checkpoints easier to find later
4. **Use `--auto-compact`** - Reminds you to free up context
5. **Check archive periodically** - Old exports can be deleted manually

## Integration with Other Commands

```bash
# Complete workflow (automated):
/export
python3 scripts/export-dedup.py -y --description "Feature X complete" --auto-compact
/compact

# Or use the slash command wrapper:
/export
/export-dedup  # Calls script automatically
/compact
```

## Troubleshooting

**"No export files found!"**
- Run `/export` first to create an export file

**"Deduplication failed"**
- Check that `MEMORY-CONTEXT/dedup_state/` exists
- Check for corrupt JSON files in dedup_state/
- Script shows full traceback for debugging

**"Archive failed"**
- Check write permissions on `MEMORY-CONTEXT/`
- Script continues even if archive fails (non-fatal)

**Export is old but script continues**
- Using `--yes` flag auto-accepts old exports
- Remove `--yes` to get prompted for confirmation
