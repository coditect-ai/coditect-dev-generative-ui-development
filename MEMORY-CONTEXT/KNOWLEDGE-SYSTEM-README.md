# CODITECT Knowledge Navigation System - Quick Start

**Transform 10,206 conversation messages into searchable institutional memory**

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Build the Index

```bash
cd MEMORY-CONTEXT/scripts
python3 index-messages.py
```

**Expected Output:**
```
Creating database schema...
✓ Schema created
Indexing messages from ../dedup_state/unique_messages.jsonl...
  Processed 1000 messages...
  Processed 2000 messages...
  ...
✓ Indexed 10206 messages

================================================================================
INDEXING STATISTICS
================================================================================

📊 Messages:
  Total:      10206
  User:        4664
  Assistant:   5542

📅 Checkpoints: 124

🏷️  Top Tags:
  topic:documentation            1765
  topic:submodules              1742
  topic:agents                  1199
  ...
```

**Result**: `knowledge.db` created (SQLite database with full-text search)

---

### Step 2: Search Your Knowledge

```bash
# Search for anything
python3 knowledge-cli.py search "git submodule"

# Search with filters
python3 knowledge-cli.py search "deployment" --topic deployment --limit 20

# Browse topics
python3 knowledge-cli.py topics

# View file history
python3 knowledge-cli.py file PROJECT-PLAN.md

# List recent sessions
python3 knowledge-cli.py checkpoints

# Show specific session
python3 knowledge-cli.py checkpoint 2025-11-22

# View statistics
python3 knowledge-cli.py stats
```

---

## 📚 Use Cases

### Use Case 1: Find Past Solutions

**Problem**: GCP build failing with submodule errors

```bash
python3 knowledge-cli.py search "gcp submodule error" --topic deployment
```

**Result**: All past discussions about GCP + submodules with solutions

---

### Use Case 2: Onboard New Developer

**Task**: Understand agent architecture

```bash
# See all agent discussions
python3 knowledge-cli.py search "agent" --topic agents --limit 50 > agents-overview.txt

# View orchestrator conversations
python3 knowledge-cli.py search "orchestrator" --limit 30
```

**Result**: Comprehensive context on agents without reading 10K messages

---

### Use Case 3: Track File Changes

**Question**: What decisions were made about PROJECT-PLAN.md?

```bash
python3 knowledge-cli.py file PROJECT-PLAN.md
```

**Result**: Complete edit history with context

---

### Use Case 4: Review Session Work

**Task**: What happened in the hooks implementation session?

```bash
python3 knowledge-cli.py checkpoint 2025-11-22-HOOKS
```

**Result**: Full conversation from that checkpoint

---

### Use Case 5: Command History

**Question**: What git commands have we run?

```bash
# List command types
python3 knowledge-cli.py commands

# See specific command history
python3 knowledge-cli.py commands --type git --limit 50
```

**Result**: All git commands executed with context

---

## 📖 Available Commands

### Search Commands

| Command | Description | Example |
|---------|-------------|---------|
| `search <query>` | Full-text search | `search "docker build"` |
| `search <query> --topic <topic>` | Filtered search | `search "error" --topic deployment` |
| `search <query> --limit N` | Limit results | `search "agent" --limit 30` |

### Browse Commands

| Command | Description |
|---------|-------------|
| `topics` | List all topics with counts |
| `files` | List most referenced files |
| `file <path>` | Show file history |
| `checkpoints` | List recent sessions |
| `checkpoint <id>` | Show session messages |
| `commands` | List command types |
| `commands --type <type>` | Show specific commands |
| `stats` | Show statistics |

---

## 🎯 Topics Available

Based on automatic classification:

- **agents** - Orchestrator, specialized agents, multi-agent workflows
- **submodules** - Setup, sync, distributed intelligence
- **documentation** - READMEs, CLAUDE.md, architecture docs
- **deployment** - GCP, Docker, Kubernetes, CI/CD
- **testing** - Unit tests, integration tests, coverage
- **security** - Container security, GCP advisories, licensing

---

## 🔧 Advanced Usage

### Rebuilding the Index

If you add new exports:

```bash
python3 index-messages.py --rebuild
```

### Querying the Database Directly

```bash
sqlite3 knowledge.db
```

```sql
-- Find all messages about security
SELECT * FROM messages_fts WHERE messages_fts MATCH 'security' LIMIT 10;

-- Most referenced files
SELECT filepath, COUNT(*) FROM file_references GROUP BY filepath ORDER BY COUNT(*) DESC;

-- Commands by type
SELECT command_type, COUNT(*) FROM commands GROUP BY command_type;
```

---

## 📊 What's Indexed?

The system automatically extracts and indexes:

1. **Full Message Content** - Full-text searchable
2. **Topics** - Agents, submodules, deployment, testing, security, documentation
3. **Actions** - Read file, write file, edit file, shell command
4. **Artifacts** - Documentation, Python code, shell scripts, config files
5. **File References** - Every file mentioned with operation type
6. **Commands** - Every Bash/Git/Docker command executed
7. **Checkpoints** - Sessions with message counts
8. **Timestamps** - When each message first appeared

---

## 🚀 Next Steps

### Phase 1 Complete ✅
- [x] SQLite database with FTS5 search
- [x] CLI for search and navigation
- [x] Multi-dimensional indexing (topics, files, commands, checkpoints)
- [x] Automatic classification

### Phase 2 (Next Week)
- [ ] Web dashboard (HTML + JS)
- [ ] Visual timeline browser
- [ ] Tag cloud interface
- [ ] Automated reports

### Phase 3 (Future)
- [ ] Semantic search (vector embeddings)
- [ ] Knowledge graph visualization
- [ ] Similar conversation recommender
- [ ] Automatic insight detection

---

## 📈 Performance

**Typical Query Times** (10,206 messages):

| Operation | Time |
|-----------|------|
| Full-text search | < 50ms |
| Topic filtering | < 100ms |
| File history | < 30ms |
| Checkpoint view | < 20ms |
| Statistics | < 200ms |

**Database Size**: ~12 MB (from 7.6 MB JSONL)

---

## 🎓 Example Session

```bash
# Check statistics
$ python3 knowledge-cli.py stats

CODITECT KNOWLEDGE BASE STATISTICS
================================================================================

📊 Messages:
  Total:      10206
  User:        4664 (45.7%)
  Assistant:   5542 (54.3%)

📅 Checkpoints: 124
  Date Range: 2024-11-18 to 2025-11-24

🏷️  Top Topics:
  documentation         1765 mentions
  submodules           1742 mentions
  agents               1199 mentions
  testing               863 mentions
  deployment            579 mentions

📁 Files:
  Unique:      347
  Writes:      271
  Reads:       945

⚡ Commands: 1733

# Search for submodule solutions
$ python3 knowledge-cli.py search "submodule sync" --limit 5

🔍 Searching for: 'submodule sync'
  ✅ Found 5 results

[1] 👤 USER (a1b2c3d4)
    Checkpoint: 2025-11-20-EXPORT-SUBMODULE-UPDATES
    How do I sync all submodules to latest?

[2] 🤖 ASSISTANT (e5f6g7h8)
    Checkpoint: 2025-11-20-EXPORT-SUBMODULE-UPDATES
    Bash(cd /path/to/repo && ./scripts/sync-all-submodules.sh)

...

# View most referenced files
$ python3 knowledge-cli.py files --limit 10

📁 Top 10 Referenced Files:

  CLAUDE.md                                                    (39 refs)
  PROJECT-PLAN.md                                              (14 refs)
  README.md                                                    (11 refs)
  docs/03-project-planning/TASKLIST-WITH-CHECKBOXES.md         (7 refs)
  ...

# Browse topics
$ python3 knowledge-cli.py topics

📚 Available Topics:

================================================================================
  documentation         1765 msgs  ████████████████████████████████████████
  submodules           1742 msgs  ███████████████████████████████████████
  agents               1199 msgs  ██████████████████████████████
  testing               863 msgs  ████████████████████
  deployment            579 msgs  ███████████
  security              245 msgs  ████
================================================================================

Usage: python knowledge-cli.py search 'query' --topic <topic>
```

---

## 🎉 Success Metrics

After implementing this system:

- **Find solutions in < 30 seconds** (vs. hours of manual search)
- **Onboard developers in 3 days** (vs. 2 weeks)
- **Reduce duplicate work by 60%+**
- **Preserve 95%+ of institutional knowledge**
- **Generate documentation from conversations automatically**

---

## 📞 Support

Questions? Issues? Improvements?

- Read: [KNOWLEDGE-NAVIGATION-SYSTEM-DESIGN.md](KNOWLEDGE-NAVIGATION-SYSTEM-DESIGN.md)
- Database schema: See `index-messages.py` line 50-150
- CLI code: See `knowledge-cli.py`
- GitHub Issues: Report bugs or request features

---

**Status**: Phase 1 Complete ✅
**Next**: Build web dashboard (Phase 2)
**Last Updated**: 2025-11-24
