# MEMORY-CONTEXT - Session Preservation System

## Overview

The MEMORY-CONTEXT system provides comprehensive conversation preservation, deduplication, and knowledge base management for CODITECT projects. It maintains a deduplicated store of 10,472+ unique messages across 127+ conversation sessions, enabling context continuity and knowledge reuse.

## Directory Structure

```
MEMORY-CONTEXT/
├── README.md                           # This file
├── checkpoints/                        # Session checkpoint markdown files (94 files)
├── dashboard/                          # Interactive web dashboard
│   ├── index.html                      # Dashboard entry point
│   ├── css/                            # Styling (AZ1.AI design system)
│   ├── js/                             # Application logic
│   ├── data/                           # Generated JSON data
│   └── assets/                         # Images, fonts, logos
├── dedup_state/                        # Deduplication state (source of truth)
│   ├── unique_messages.jsonl           # 7.8MB, 10,472 unique messages
│   ├── global_hashes.json              # 695KB, hash index
│   ├── checkpoint_index.json           # 776KB, checkpoint mappings
│   ├── conversation_log.jsonl          # 943KB, session log
│   ├── watermarks.json                 # 315B, progress tracking
│   └── content_hashes.json             # 106KB, collision detection
├── exports/                            # Conversation export files
├── exports-archive/                    # Archived exports
├── logs/                               # Operation logs
├── scripts/                            # Dashboard generation scripts
├── sessions/                           # Session export markdown files
└── [Automation Scripts - documented below]
```

## Quick Start

### Run Deduplication and Auto-Sync

The easiest way to maintain your MEMORY-CONTEXT:

```bash
cd MEMORY-CONTEXT
./dedup-and-sync.sh
```

**This single command:**
1. ✅ Reindexes deduplication state
2. ✅ Checks all 46 submodules for changes
3. ✅ Auto-commits changes in each submodule
4. ✅ Auto-pushes submodule changes
5. ✅ Updates master repo submodule pointers
6. ✅ Auto-commits and pushes master repo
7. ✅ Shows detailed summary

### View Knowledge Base Dashboard

```bash
cd dashboard
python3 -m http.server 8000
open http://localhost:8000
```

**Dashboard Features:**
- Interactive timeline with 124 sessions
- 10,206 messages searchable
- Git commit visualization
- Topic taxonomy and file references
- Checkpoint detail panels
- Real-time filtering

---

## Core Features

### 1. Message Deduplication

**Purpose:** Eliminate duplicate message content across all exports and sessions.

**Storage:**
- `unique_messages.jsonl` - Append-only source of truth (7.8MB)
- `global_hashes.json` - SHA-256 hash index (695KB, 10,472 hashes)
- `checkpoint_index.json` - Checkpoint-to-message mappings (776KB, 127 checkpoints)

**Deduplication Rate:** ~40-60% typical (varies by session overlap)

**Benefits:**
- Reduces storage by 40-60%
- Enables efficient search across all sessions
- Maintains single source of truth
- Prevents context drift

### 2. Session Checkpoints

**Purpose:** Preserve complete conversation state for context continuity.

**Location:** `checkpoints/` directory (94 markdown files)

**Checkpoint Format:**
```
2025-11-22T08-28-09Z-Submodule-configuration-cross-check.md
```

**Contents:**
- Session metadata (date, participants, objectives)
- Complete conversation history
- Tool usage and results
- Decisions made and rationale
- Next steps and blockers

**Usage:**
- Reference previous conversations
- Continue work across sessions
- Share context with team
- Track project evolution

### 3. Interactive Dashboard

**Purpose:** Visual exploration of conversation history and knowledge base.

**URL:** http://localhost:8000 (after starting server)

**Features:**

**Timeline View:**
- Chronological session bubbles (circles)
- Git commits (squares at top)
- Hover for details
- Click for GitHub links (commits)
- Click for checkpoint details (sessions)

**Search:**
- 10,206 messages indexed
- Real-time filtering
- Topic and file search
- Command history

**Analytics:**
- Message counts per session
- Topic distribution
- File modification tracking
- Command usage patterns

**Technology:**
- D3.js for timeline visualization
- AZ1.AI design system
- Responsive layout
- Dark/light theme toggle

### 4. Export Management

**Purpose:** Process Claude Code conversation exports into deduplicated storage.

**Workflow:**
1. Run `/export` in Claude Code
2. Export file saved to `exports/`
3. Run `./dedup-and-sync.sh`
4. Messages deduplicated and indexed
5. Changes committed and pushed

**Export Format:**
- Text-based with markers (⏺ user, ⎿ assistant)
- Timestamp and metadata
- Complete conversation history

**Processing:**
- Parses markers into structured messages
- Extracts roles and content
- Computes content hashes (SHA-256)
- Filters duplicates
- Appends unique messages to store

---

## Automation Scripts

### Primary Scripts

#### `dedup-and-sync.sh`
**Complete automation workflow - Use this for most tasks**

```bash
./dedup-and-sync.sh              # With backup (recommended)
./dedup-and-sync.sh --no-backup  # Without backup (faster)
```

**What it does:**
1. Runs deduplication reindex
2. Processes all submodules (git status → commit → push)
3. Updates master repo (submodule pointers + dedup state)
4. Shows detailed summary

**When to use:**
- After running `/export-dedup` in Claude Code
- Daily maintenance
- Before starting new session
- After major changes

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Automated Dedup and Git Sync Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Running deduplication...
✅ Reindex completed successfully!
  Messages processed: 10472
  Unique hashes: 10472
  Checkpoints found: 127

Step 2: Processing submodules...
▶ Checking submodule: submodules/core/coditect-core
  ✓ Changes committed and pushed

Step 3: Processing master repository...
✓ Master repo changes committed and pushed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Submodules with changes: 1
Submodules committed:    1
Submodules pushed:       1

✅ Workflow completed successfully!
```

---

#### `reindex-dedup.sh`
**Rebuild indices from source data**

```bash
./reindex-dedup.sh              # With backup
./reindex-dedup.sh --no-backup  # Without backup
```

**What it does:**
- Reads `unique_messages.jsonl` (source of truth)
- Rebuilds `global_hashes.json`
- Rebuilds `checkpoint_index.json`
- Creates timestamped backups

**When to use:**
- Index corruption
- After manual edits to `unique_messages.jsonl`
- Integrity verification
- Performance optimization

**Performance:**
- 10,472 messages in <1 second
- Backup creation: ~100ms
- Total: <2 seconds

---

### Dashboard Scripts

Located in `scripts/` directory:

#### `generate-dashboard.py`
**Generate dashboard data files (JSON only)**

```bash
python3 scripts/generate-dashboard.py
```

**What it generates:**
- `dashboard/data/messages.json` - Message index
- `dashboard/data/messages-page-*.json` - Paginated messages (500 per page)
- `dashboard/data/topics.json` - Topic taxonomy
- `dashboard/data/files.json` - File references
- `dashboard/data/checkpoints.json` - Session data (124 database + 94 markdown = 218 total)
- `dashboard/data/commands.json` - Command history
- `dashboard/data/git-commits.json` - Git commit history

**Important:** This script NEVER modifies HTML/CSS/JS files. Those are source code and must be edited directly.

**When to run:**
- After new dedup operations
- After adding checkpoints
- Weekly dashboard refresh
- Before demoing knowledge base

**Performance:**
- Processes 10,472 messages
- Scans 94 checkpoint files
- Generates 25+ JSON files
- Total time: ~30 seconds

#### `extract_git_commits.py`
**Extract git commit history for dashboard**

```bash
python3 scripts/extract_git_commits.py
```

**What it does:**
- Scans git history (last 365 days)
- Extracts commit metadata
- Categorizes by type (feat, fix, docs, etc.)
- Generates `git-commits.json`

**When to run:**
- Weekly with dashboard regeneration
- After major commit activity
- Before presentations

---

## Common Workflows

### Workflow 1: Daily Export Processing

**After running `/export-dedup` in Claude Code:**

```bash
cd MEMORY-CONTEXT
./dedup-and-sync.sh
```

**Result:**
- Export processed and deduplicated
- Changes committed to all repos
- Everything pushed to GitHub
- Ready for next session

**Time:** ~20 seconds (with changes), ~5 seconds (clean)

---

### Workflow 2: Dashboard Refresh

**Weekly or before demos:**

```bash
cd MEMORY-CONTEXT

# Generate fresh dashboard data
python3 scripts/generate-dashboard.py

# Start dashboard server
cd dashboard
python3 -m http.server 8000

# Open in browser
open http://localhost:8000
```

**Time:** ~30 seconds generation, instant server start

---

### Workflow 3: Manual Checkpoint Creation

**After completing significant work:**

```bash
cd ..  # Navigate to project root
python3 .coditect/scripts/create-checkpoint.py "Sprint 3 Week 2 Complete" --auto-commit
```

**Result:**
- Checkpoint markdown file created in `MEMORY-CONTEXT/checkpoints/`
- Automatically committed with descriptive message
- Available in dashboard after next regeneration

---

### Workflow 4: Search Across All Sessions

**Using dashboard:**

1. Start dashboard: `cd dashboard && python3 -m http.server 8000`
2. Open: http://localhost:8000
3. Use global search bar (top)
4. Filter by topics, files, or commands
5. Click results to see context

**Using command line:**

```bash
# Search unique messages
grep -i "search term" dedup_state/unique_messages.jsonl

# Search checkpoints
grep -r "search term" checkpoints/
```

---

### Workflow 5: Recovery from Corruption

**If dedup state becomes corrupted:**

```bash
cd MEMORY-CONTEXT

# Check available backups
ls -lt dedup_state/*.backup-* | head -10

# Restore from backup (choose most recent)
cp dedup_state/global_hashes.json.backup-YYYYMMDD-HHMMSS dedup_state/global_hashes.json
cp dedup_state/checkpoint_index.json.backup-YYYYMMDD-HHMMSS dedup_state/checkpoint_index.json

# Verify and reindex
./reindex-dedup.sh

# Sync changes
./dedup-and-sync.sh
```

---

## Performance Metrics

### Deduplication Performance

| Metric | Value | Notes |
|--------|-------|-------|
| **Unique Messages** | 10,472 | Source of truth |
| **Total Checkpoints** | 127 | From conversation log |
| **Reindex Time** | <1 second | 10,472 messages |
| **Dedup Rate** | 40-60% | Typical session overlap |
| **Storage Savings** | 40-60% | vs. raw exports |

### Dashboard Performance

| Metric | Value | Notes |
|--------|-------|-------|
| **Total Messages Indexed** | 10,206 | Searchable messages |
| **Total Sessions** | 124 | Timeline visualization |
| **Total Checkpoints** | 218 | 124 database + 94 markdown |
| **Generation Time** | ~30 seconds | Full regeneration |
| **Load Time** | <2 seconds | Initial page load |
| **Search Time** | <100ms | Client-side filtering |

### Git Operations

| Metric | Value | Notes |
|--------|-------|-------|
| **Submodules Checked** | 46 | All project repos |
| **Commit Time** | 1-2 seconds | Per repo with changes |
| **Push Time** | 2-3 seconds | Per repo with changes |
| **Total Workflow** | 5-20 seconds | Depends on changes |

---

## Troubleshooting

### Problem: "Deduplication failed"

**Symptoms:**
```
✗ Deduplication failed
```

**Causes:**
- Corrupted `unique_messages.jsonl`
- Missing dedup state files
- Disk space issues

**Solution:**
```bash
# Check if source file exists
ls -lh dedup_state/unique_messages.jsonl

# Check disk space
df -h .

# Restore from backup if corrupted
cp dedup_state/unique_messages.jsonl.backup-* dedup_state/unique_messages.jsonl

# Retry
./reindex-dedup.sh
```

---

### Problem: "Failed to push changes"

**Symptoms:**
```
✗ Failed to push changes
```

**Causes:**
- Network connectivity
- GitHub authentication
- Branch protection

**Solution:**
```bash
# Check GitHub authentication
gh auth status

# Login if needed
gh auth login

# Check network
ping github.com

# Manual push if needed
cd submodules/path/to/submodule
git push origin main
```

---

### Problem: Submodule in detached HEAD

**Symptoms:**
```
HEAD detached at abc1234
```

**Causes:**
- Raw `git submodule update` used
- Interrupted git operations

**Solution:**
```bash
cd submodules/path/to/submodule
git checkout main
git pull
cd ../../..

# Use sync script in future
cd ../scripts
./sync-all-submodules.sh
```

---

### Problem: Dashboard not updating

**Symptoms:**
- New checkpoints not appearing
- Message counts outdated

**Causes:**
- Dashboard not regenerated
- Browser cache

**Solution:**
```bash
# Regenerate dashboard data
python3 scripts/generate-dashboard.py

# Hard refresh browser (Cmd+Shift+R on Mac)
# Or clear cache
```

---

### Problem: Checkpoint detail panels show "not found"

**Symptoms:**
- Clicking checkpoint shows error
- Console shows 404 errors

**Causes:**
- Missing checkpoint markdown files
- Symlink not created
- HTTP server not serving checkpoints directory

**Solution:**
```bash
# Check symlink exists
ls -la dashboard/checkpoints

# Create symlink if missing
cd dashboard
ln -sfn ../checkpoints checkpoints
cd ..

# Restart HTTP server
cd dashboard
python3 -m http.server 8000
```

---

## Best Practices

### 1. Regular Dedup Maintenance

**Recommendation:** Run dedup-and-sync after every conversation export

```bash
# After /export-dedup in Claude Code
cd MEMORY-CONTEXT
./dedup-and-sync.sh
```

**Benefits:**
- Keeps dedup state current
- Prevents git drift
- Maintains clean history
- Enables context continuity

---

### 2. Backup Management

**Recommendation:** Keep 7 days of backups, delete older

```bash
# Check backup count
ls -1 dedup_state/*.backup-* | wc -l

# Clean backups older than 7 days
find dedup_state -name "*.backup-*" -mtime +7 -delete
```

**Benefits:**
- Prevents disk bloat
- Maintains recovery capability
- Organizes backup directory

---

### 3. Dashboard Refresh Schedule

**Recommendation:** Regenerate dashboard weekly or before demos

```bash
# Weekly refresh
python3 scripts/generate-dashboard.py
```

**Benefits:**
- Fresh data for presentations
- Accurate statistics
- All sessions visible

---

### 4. Checkpoint Organization

**Recommendation:** Use descriptive checkpoint names

```bash
# Good checkpoint naming
python3 .coditect/scripts/create-checkpoint.py "Sprint 3 Week 2 - Auth Implementation Complete"

# Bad checkpoint naming
python3 .coditect/scripts/create-checkpoint.py "work"
```

**Benefits:**
- Easy to find sessions later
- Clear project timeline
- Better dashboard visualization

---

### 5. Git Workflow Discipline

**Recommendation:** Always use automation scripts, not raw git commands

```bash
# ✅ GOOD - Use automation
./dedup-and-sync.sh

# ❌ BAD - Manual submodule updates
git submodule update
```

**Benefits:**
- Consistent commit messages
- Proper error handling
- Complete workflow coverage
- No missed steps

---

## Integration

### With Claude Code

**After conversation exports:**

```bash
# 1. In Claude Code
/export-dedup

# 2. In terminal
cd MEMORY-CONTEXT
./dedup-and-sync.sh
```

---

### With Cron (Scheduled Automation)

```bash
# Edit crontab
crontab -e

# Add entry (runs every 6 hours)
0 */6 * * * cd /path/to/MEMORY-CONTEXT && ./dedup-and-sync.sh --no-backup
```

---

### With GitHub Actions

```yaml
name: Automated Dedup Sync
on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  dedup-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive
          token: ${{ secrets.GH_TOKEN }}

      - name: Run dedup sync
        run: |
          cd MEMORY-CONTEXT
          ./dedup-and-sync.sh --no-backup
```

---

## Security Considerations

### Sensitive Data

**Warning:** Conversation exports may contain sensitive information:
- API keys or credentials
- Private project details
- Personal information

**Recommendations:**
1. Review exports before committing
2. Use `.gitignore` for sensitive exports
3. Scrub sensitive data from checkpoints
4. Restrict repository access appropriately

### Access Control

**Repository Access:**
- Limit access to trusted team members
- Use GitHub branch protection
- Require PR reviews for changes
- Enable 2FA for all contributors

---

## Architecture

### Deduplication Strategy

**Approach:** Content-based SHA-256 hashing

```python
# Message normalization
normalized = {
    'role': message.get('role'),
    'content': message.get('content')
}

# Hash computation
content_hash = hashlib.sha256(
    json.dumps(normalized, sort_keys=True).encode()
).hexdigest()
```

**Benefits:**
- Deterministic (same content = same hash)
- Collision-resistant (SHA-256)
- Fast lookups (O(1) with hash index)
- Storage efficient (hash vs. full content)

### Storage Format

**Source of Truth:** `unique_messages.jsonl`

```jsonl
{"hash": "abc123...", "message": {...}, "first_seen": "2025-11-24T12:00:00Z", "checkpoint": "session-id"}
{"hash": "def456...", "message": {...}, "first_seen": "2025-11-24T12:05:00Z", "checkpoint": "session-id"}
```

**Indices:**
- `global_hashes.json` - Array of all unique hashes
- `checkpoint_index.json` - Mapping `{checkpoint_id: {created, message_hashes}}`

**Benefits:**
- Append-only source (no overwrites)
- Fast index rebuilds (from source)
- Recovery-friendly (source is reliable)

---

## Related Documentation

### Core Documentation
- [REINDEX-DEDUP.md](REINDEX-DEDUP.md) - Reindex technical details
- [DEDUP-WORKFLOW-GUIDE.md](DEDUP-WORKFLOW-GUIDE.md) - Workflow examples
- [dashboard/REGENERATION-WARNING.md](dashboard/REGENERATION-WARNING.md) - Dashboard safety

### Project Documentation
- [../README.md](../README.md) - Master project overview
- [../WHAT-IS-CODITECT.md](../WHAT-IS-CODITECT.md) - CODITECT architecture
- [../docs/project-management/PROJECT-PLAN.md](../docs/project-management/PROJECT-PLAN.md) - Project plan

### Script Documentation
- [../scripts/README.md](../scripts/README.md) - All automation scripts
- [../scripts/CLAUDE.md](../scripts/CLAUDE.md) - Script usage guide

---

## Statistics

**As of 2025-11-24:**

| Metric | Count | Size |
|--------|-------|------|
| **Unique Messages** | 10,472 | 7.8MB |
| **Global Hashes** | 10,472 | 695KB |
| **Checkpoints (DB)** | 124 | - |
| **Checkpoints (Files)** | 94 | ~50MB |
| **Total Checkpoints** | 218 | 776KB index |
| **Conversations** | 127 | 943KB log |
| **Exports Processed** | 300+ | - |
| **Sessions Tracked** | 124 | - |

**Storage Efficiency:**
- Raw exports: ~18MB
- Deduplicated: ~7.8MB
- Savings: 57% reduction

---

## Support

**Questions or Issues:**
1. Check this README
2. Review related documentation
3. Check troubleshooting section
4. Review script output for errors
5. Contact: Hal Casteel, Founder/CEO/CTO

**Contributing:**
- Follow conventional commit format
- Test scripts before committing
- Update documentation
- Maintain backward compatibility

---

**Last Updated:** 2025-11-24
**Version:** 1.0
**Author:** AZ1.AI CODITECT
**License:** MIT
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
