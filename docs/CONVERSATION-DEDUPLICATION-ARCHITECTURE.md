# Conversation Export Deduplication - System Architecture

**Project:** Claude Conversation Export Deduplication System
**Version:** 1.0
**Date:** 2025-11-17
**Status:** Design Complete - Ready for Implementation

**Related Documents:**
- Implementation Plan: `docs/CONVERSATION-DEDUPLICATION-IMPLEMENTATION-PLAN.md`
- Database Design: `docs/CONVERSATION-DEDUPLICATION-DATABASE-DESIGN.md`
- Research: `MEMORY-CONTEXT/RESEARCH-CLAUDE-CONVERSATION-EXPORT-DEDUPLICATION.md`

---

## Executive Summary

This document describes the complete system architecture for the Claude Conversation Export Deduplication System, which solves the problem of exponentially growing export files in multi-day Claude sessions by implementing a hybrid deduplication strategy combining sequence watermarks, content hashing, and append-only logs.

**Key Architecture Principles:**
- **Zero Catastrophic Forgetting:** All unique data preserved in append-only log
- **Hybrid Storage:** JSON for speed (Phase 1), PostgreSQL for scale (Phase 2)
- **Idempotent Processing:** Safe to reprocess same export multiple times
- **Integration-First:** Seamless integration with CODITECT checkpoint automation

---

## C4 Architecture Model

### Level 1: System Context Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    System Context                               │
│                                                                 │
│                                                                 │
│  ┌─────────────┐                                               │
│  │   Claude    │──┐                                            │
│  │ Conversation│  │ /export command                            │
│  │  Sessions   │  │ (13KB → 51KB → 439KB)                      │
│  └─────────────┘  │                                            │
│                   │                                            │
│                   ▼                                            │
│         ┌─────────────────────────┐                            │
│         │  Conversation Export    │                            │
│         │ Deduplication System    │                            │
│         │                         │                            │
│         │ - Extracts NEW messages │                            │
│         │ - 95% storage reduction │                            │
│         │ - Zero data loss        │                            │
│         └───────┬─────────────────┘                            │
│                 │                                              │
│                 │ Deduplicated messages                        │
│                 │ Statistics & metrics                         │
│                 │                                              │
│                 ▼                                              │
│    ┌────────────────────────────┐                              │
│    │   CODITECT Framework       │                              │
│    │                            │                              │
│    │ - Checkpoint automation    │                              │
│    │ - MEMORY-CONTEXT storage   │                              │
│    │ - Session continuity       │                              │
│    └────────────────────────────┘                              │
│                                                                 │
│                                                                 │
│  ┌──────────────┐          ┌─────────────┐                     │
│  │ PostgreSQL   │          │  Monitoring │                     │
│  │   Database   │          │  Dashboard  │                     │
│  │              │          │             │                     │
│  │ - Messages   │          │ - Stats     │                     │
│  │ - Watermarks │          │ - Alerts    │                     │
│  │ - Hashes     │          │ - Trends    │                     │
│  └──────────────┘          └─────────────┘                     │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

External Systems:
- Claude Conversation Sessions (User interaction)
- CODITECT Framework (Integration point)
- PostgreSQL Database (Persistence)
- Monitoring Dashboard (Observability)
```

**Key External Relationships:**

1. **Claude Sessions → Deduplication System**
   - Input: Export files (JSON/TXT format)
   - Size: 13KB to 439KB (exponential growth)
   - Frequency: Multiple times per day for multi-day sessions

2. **Deduplication System → CODITECT Framework**
   - Output: Deduplicated messages (JSON/Markdown)
   - Integration: Checkpoint automation
   - Storage: MEMORY-CONTEXT/sessions/

3. **Deduplication System → PostgreSQL**
   - Persistence: Messages, watermarks, content hashes
   - Scalability: Millions of messages
   - Queryability: SQL access to conversation history

4. **Deduplication System → Monitoring**
   - Metrics: Storage savings, processing time, deduplication rate
   - Alerts: Gaps, anomalies, errors

---

### Level 2: Container Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  Conversation Deduplication System                        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                     CLI & Integration Layer                      │     │
│  │                                                                  │     │
│  │  ┌──────────────┐    ┌──────────────────┐   ┌───────────────┐  │     │
│  │  │ CLI Tool     │    │ SessionExport    │   │ Checkpoint    │  │     │
│  │  │              │    │ Manager          │   │ Integration   │  │     │
│  │  │ - Manual     │    │                  │   │               │  │     │
│  │  │ - Batch      │    │ - Auto-detect ID │   │ - Automated   │  │     │
│  │  │ - Stats      │    │ - Format output  │   │ - Transparent │  │     │
│  │  └──────┬───────┘    └────────┬─────────┘   └───────┬───────┘  │     │
│  │         │                     │                     │          │     │
│  │         └─────────────────────┼─────────────────────┘          │     │
│  └───────────────────────────────┼──────────────────────────────────┘   │
│                                  │                                      │
│                                  ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │               Core Deduplication Engine                          │   │
│  │                                                                  │   │
│  │  ┌───────────────────────────────────────────────────────────┐  │   │
│  │  │  ClaudeConversationDeduplicator                           │  │   │
│  │  │                                                            │  │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │   │
│  │  │  │  Sequence    │  │   Content    │  │  Append-Only │    │  │   │
│  │  │  │  Watermark   │  │   Hashing    │  │     Log      │    │  │   │
│  │  │  │  Tracker     │  │   (SHA-256)  │  │   Writer     │    │  │   │
│  │  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │  │   │
│  │  │         │                 │                 │            │  │   │
│  │  │         └─────────────────┴─────────────────┘            │  │   │
│  │  │                           │                               │  │   │
│  │  │                           ▼                               │  │   │
│  │  │                  ┌─────────────────┐                      │  │   │
│  │  │                  │  State Manager  │                      │  │   │
│  │  │                  │                 │                      │  │   │
│  │  │                  │  - Load/Save    │                      │  │   │
│  │  │                  │  - Validation   │                      │  │   │
│  │  │                  │  - Recovery     │                      │  │   │
│  │  │                  └────────┬────────┘                      │  │   │
│  │  │                           │                               │  │   │
│  │  └───────────────────────────┼───────────────────────────────┘  │   │
│  │                              │                                  │   │
│  └──────────────────────────────┼──────────────────────────────────┘   │
│                                 │                                      │
│                                 ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                  Storage Layer (Pluggable)                       │   │
│  │                                                                  │   │
│  │  ┌────────────────────┐         ┌──────────────────────┐        │   │
│  │  │  JSON File         │         │  PostgreSQL          │        │   │
│  │  │  Backend           │         │  Backend             │        │   │
│  │  │  (Phase 1)         │         │  (Phase 2)           │        │   │
│  │  │                    │         │                      │        │   │
│  │  │ - watermarks.json  │         │ - conversations tbl  │        │   │
│  │  │ - hashes.json      │         │ - messages tbl       │        │   │
│  │  │ - log.jsonl        │         │ - watermarks tbl     │        │   │
│  │  └────────────────────┘         └──────────────────────┘        │   │
│  │                                                                  │   │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

External Dependencies:
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│ Export Files    │    │ MEMORY-      │    │ PostgreSQL DB   │
│ (Input)         │    │ CONTEXT      │    │ (Persistence)   │
│                 │    │ (Output)     │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

**Container Descriptions:**

1. **CLI & Integration Layer**
   - Technology: Python Click/argparse
   - Purpose: User interface and automation integration
   - Components:
     - CLI Tool (manual/batch processing)
     - SessionExportManager (CODITECT integration)
     - Checkpoint Integration (automated workflow)

2. **Core Deduplication Engine**
   - Technology: Python 3.9+
   - Purpose: Deduplication logic and state management
   - Components:
     - ClaudeConversationDeduplicator (main class)
     - Sequence Watermark Tracker (primary deduplication)
     - Content Hashing (SHA-256, secondary deduplication)
     - Append-Only Log Writer (persistence)
     - State Manager (load/save/validation)

3. **Storage Layer (Pluggable)**
   - Technology: JSON files (Phase 1), PostgreSQL (Phase 2)
   - Purpose: Persistent storage with migration path
   - Implementations:
     - JSON File Backend (simple, fast, MVP)
     - PostgreSQL Backend (scalable, queryable, production)

---

### Level 3: Component Diagram (Core Deduplication Engine)

```
┌────────────────────────────────────────────────────────────────────────┐
│            ClaudeConversationDeduplicator Component                     │
│                                                                         │
│  Entry Point: process_export(conversation_id, export_data)             │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 1. Export Parser                                                 │  │
│  │    ┌──────────────────────────────────────────────┐              │  │
│  │    │ parse_export(export_data) → messages[]       │              │  │
│  │    │                                               │              │  │
│  │    │ - Detect format (JSON/TXT/API)                │              │  │
│  │    │ - Extract messages array                      │              │  │
│  │    │ - Normalize message structure                 │              │  │
│  │    │ - Validate required fields (index, content)   │              │  │
│  │    └──────────────────┬────────────────────────────┘              │  │
│  │                       │                                           │  │
│  └───────────────────────┼───────────────────────────────────────────┘  │
│                          │                                              │
│                          ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 2. State Loader                                                  │  │
│  │    ┌──────────────────────────────────────────────┐              │  │
│  │    │ load_state(conversation_id) → state          │              │  │
│  │    │                                               │              │  │
│  │    │ Returns:                                      │              │  │
│  │    │   - watermark: int (highest index processed) │              │  │
│  │    │   - content_hashes: Set[str]                 │              │  │
│  │    │                                               │              │  │
│  │    │ Storage: JSON or PostgreSQL                  │              │  │
│  │    └──────────────────┬────────────────────────────┘              │  │
│  │                       │                                           │  │
│  └───────────────────────┼───────────────────────────────────────────┘  │
│                          │                                              │
│                          ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 3. Deduplication Logic (Main Loop)                               │  │
│  │                                                                   │  │
│  │    FOR each message in sorted(messages, key=index):              │  │
│  │                                                                   │  │
│  │    ┌─────────────────────────────────────────────────┐           │  │
│  │    │ Check 1: Sequence Watermark (Primary)          │           │  │
│  │    │                                                 │           │  │
│  │    │   if message.index <= watermark:               │           │  │
│  │    │       continue  # Already processed            │           │  │
│  │    └─────────────────┬───────────────────────────────┘           │  │
│  │                      │                                           │  │
│  │                      ▼                                           │  │
│  │    ┌─────────────────────────────────────────────────┐           │  │
│  │    │ Check 2: Content Hash (Secondary)              │           │  │
│  │    │                                                 │           │  │
│  │    │   content_hash = sha256(normalize(message))    │           │  │
│  │    │                                                 │           │  │
│  │    │   if content_hash in seen_hashes:              │           │  │
│  │    │       log_warning("Duplicate at new index")    │           │  │
│  │    │       continue  # Same content                 │           │  │
│  │    └─────────────────┬───────────────────────────────┘           │  │
│  │                      │                                           │  │
│  │                      ▼                                           │  │
│  │    ┌─────────────────────────────────────────────────┐           │  │
│  │    │ New Unique Message Found                        │           │  │
│  │    │                                                 │           │  │
│  │    │   new_messages.append(message)                 │           │  │
│  │    │   seen_hashes.add(content_hash)                │           │  │
│  │    │   watermark = max(watermark, message.index)    │           │  │
│  │    │                                                 │           │  │
│  │    │   append_to_log(conversation_id, message)      │           │  │
│  │    └─────────────────┬───────────────────────────────┘           │  │
│  │                      │                                           │  │
│  │    END FOR           │                                           │  │
│  │                      │                                           │  │
│  └──────────────────────┼───────────────────────────────────────────┘  │
│                         │                                              │
│                         ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 4. State Saver                                                   │  │
│  │    ┌──────────────────────────────────────────────┐              │  │
│  │    │ save_state(conversation_id, state)           │              │  │
│  │    │                                               │              │  │
│  │    │   state = {                                   │              │  │
│  │    │     watermark: int,                           │              │  │
│  │    │     content_hashes: Set[str]                  │              │  │
│  │    │   }                                           │              │  │
│  │    │                                               │              │  │
│  │    │ Atomic write:                                 │              │  │
│  │    │   1. Write to temp file                       │              │  │
│  │    │   2. Atomic rename                            │              │  │
│  │    └──────────────────┬────────────────────────────┘              │  │
│  │                       │                                           │  │
│  └───────────────────────┼───────────────────────────────────────────┘  │
│                          │                                              │
│                          ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 5. Output                                                         │  │
│  │    ┌──────────────────────────────────────────────┐              │  │
│  │    │ Return new_messages[]                        │              │  │
│  │    │                                               │              │  │
│  │    │ Statistics:                                   │              │  │
│  │    │   - Total messages in export                 │              │  │
│  │    │   - New unique messages                      │              │  │
│  │    │   - Duplicates filtered                      │              │  │
│  │    │   - Storage savings (%)                      │              │  │
│  │    └───────────────────────────────────────────────┘              │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  Supporting Methods:                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ - create_message_hash(message) → str                             │  │
│  │ - normalize_message(message) → dict                              │  │
│  │ - append_to_log(conversation_id, message) → void                 │  │
│  │ - get_full_conversation(conversation_id) → messages[]            │  │
│  │ - get_statistics(conversation_id) → stats                        │  │
│  │ - detect_gaps(conversation_id, messages) → gaps[]                │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Component Interactions:**

1. **Export Parser** → State Loader
   - Parse export file, extract messages
   - Pass conversation_id to load previous state

2. **State Loader** → Deduplication Logic
   - Load watermark and content hashes
   - Provide to main loop for comparison

3. **Deduplication Logic** → Append-Only Log
   - For each new message, append to log
   - Log format: JSONL (one JSON object per line)

4. **Deduplication Logic** → State Saver
   - After processing, save updated state
   - Atomic write ensures consistency

5. **State Saver** → Output
   - Return new messages and statistics
   - Client receives deduplicated results

---

## Data Flow Diagrams

### Data Flow 1: First Export Processing

```
┌─────────────┐
│ User runs   │
│ /export in  │
│ Claude      │
│             │
│ Output:     │
│ export.txt  │
│ (13KB)      │
└──────┬──────┘
       │
       │ 1. User runs CLI tool
       │    deduplicate_export.py export.txt --session-id rollout-master
       │
       ▼
┌──────────────────────────────────────────┐
│ ClaudeConversationDeduplicator           │
│                                          │
│ process_export("rollout-master",        │
│                 export_data)             │
│                                          │
│ State Check:                             │
│   watermark = -1 (no previous state)    │
│   content_hashes = {} (empty)           │
│                                          │
│ Processing:                              │
│   FOR message in messages (index 0-10): │
│     index > watermark? YES (0 > -1)     │
│     hash in seen? NO (first time)       │
│     → ADD to new_messages               │
│     → APPEND to log                     │
│     → UPDATE watermark = 10             │
│                                          │
│ Save State:                              │
│   watermarks.json:                       │
│     {"rollout-master": 10}               │
│   content_hashes.json:                   │
│     {"rollout-master": [hash0...hash10]} │
│   conversation_log.jsonl:                │
│     {conv_id, timestamp, hash, msg0}     │
│     {conv_id, timestamp, hash, msg1}     │
│     ...                                  │
└──────┬───────────────────────────────────┘
       │
       │ 2. Return Results
       │
       ▼
┌──────────────────────────────────────────┐
│ Output:                                  │
│                                          │
│ new_messages: 11 messages (index 0-10)  │
│ duplicates_filtered: 0                   │
│ storage_savings: 0% (first run)          │
│                                          │
│ Files Created:                           │
│   MEMORY-CONTEXT/dedup_state/            │
│   ├── watermarks.json                    │
│   ├── content_hashes.json                │
│   └── conversation_log.jsonl             │
└──────────────────────────────────────────┘
```

### Data Flow 2: Second Export Processing (With Duplicates)

```
┌─────────────┐
│ User runs   │
│ /export in  │
│ Claude      │
│ (next day)  │
│             │
│ Output:     │
│ export2.txt │
│ (51KB)      │
│             │
│ Contains:   │
│ - Msgs 0-10 │ ← DUPLICATES from Export 1
│ - Msgs 11-25│ ← NEW messages
└──────┬──────┘
       │
       │ 1. User runs CLI tool
       │    deduplicate_export.py export2.txt --session-id rollout-master
       │
       ▼
┌──────────────────────────────────────────┐
│ ClaudeConversationDeduplicator           │
│                                          │
│ process_export("rollout-master",        │
│                 export_data)             │
│                                          │
│ State Check:                             │
│   watermark = 10 (from previous run)    │
│   content_hashes = {hash0...hash10}     │
│                                          │
│ Processing:                              │
│   FOR message in messages (index 0-25): │
│                                          │
│     Message 0 (index 0):                │
│       index > watermark? NO (0 <= 10)   │
│       → SKIP (already processed)        │
│                                          │
│     Message 1-10 (index 1-10):          │
│       index > watermark? NO             │
│       → SKIP (already processed)        │
│                                          │
│     Message 11 (index 11):              │
│       index > watermark? YES (11 > 10)  │
│       hash in seen? NO (new content)    │
│       → ADD to new_messages             │
│       → APPEND to log                   │
│       → UPDATE watermark = 11           │
│                                          │
│     Message 12-25 (index 12-25):        │
│       index > watermark? YES            │
│       hash in seen? NO                  │
│       → ADD to new_messages             │
│       → APPEND to log                   │
│       → UPDATE watermark = 25           │
│                                          │
│ Save State:                              │
│   watermarks.json:                       │
│     {"rollout-master": 25} ← UPDATED    │
│   content_hashes.json:                   │
│     {"rollout-master": [hash0...hash25]} │
│   conversation_log.jsonl: (appended)     │
│     {conv_id, timestamp, hash, msg11}    │
│     {conv_id, timestamp, hash, msg12}    │
│     ...                                  │
└──────┬───────────────────────────────────┘
       │
       │ 2. Return Results
       │
       ▼
┌──────────────────────────────────────────┐
│ Output:                                  │
│                                          │
│ new_messages: 15 messages (index 11-25) │
│ duplicates_filtered: 11 (msgs 0-10)      │
│ storage_savings: 73% (11/26 filtered)    │
│                                          │
│ Total conversation size: 26 messages     │
│ Raw export size: 51KB                    │
│ Deduplicated storage: ~14KB (27% of raw) │
└──────────────────────────────────────────┘
```

### Data Flow 3: CODITECT Checkpoint Integration

```
┌───────────────────────────────────────────┐
│ User runs:                                │
│ python3 .coditect/scripts/                │
│         create-checkpoint.py              │
│         "Sprint Complete"                 │
└─────────────┬─────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│ Checkpoint Script (create-checkpoint.py)        │
│                                                 │
│ Step 1: Prepare export location                │
│   ├─ Create export filename with timestamp     │
│   └─ Prompt user to run /export                │
│                                                 │
│ Step 2: Generate checkpoint document           │
│   ├─ Collect git status                        │
│   ├─ Collect completed tasks                   │
│   └─ Create checkpoint.md                      │
│                                                 │
│ Step 3: Deduplicate conversation export ← NEW! │
│   ├─ Call SessionExportManager              │
│   │   └─ Calls ClaudeConversationDeduplicator│
│   ├─ Extract only NEW messages                 │
│   └─ Save to MEMORY-CONTEXT/sessions/          │
│                                                 │
│ Step 4: Update README.md                       │
│   └─ Add checkpoint reference                  │
│                                                 │
│ Step 5: Commit to git                          │
│   └─ Commit checkpoint + deduplicated session  │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│ Output Files Created:                           │
│                                                 │
│ MEMORY-CONTEXT/                                 │
│ ├── checkpoints/                                │
│ │   └── 2025-11-17T12-00-00Z-Sprint-Complete.md│
│ │                                               │
│ ├── sessions/                                   │
│ │   └── 2025-11-17-Sprint-Complete.md          │
│ │       (Contains ONLY new messages)            │
│ │                                               │
│ ├── exports/                                    │
│ │   └── 2025-11-17T12-00-00Z-Sprint-Complete.txt│
│ │       (Raw export from /export)              │
│ │                                               │
│ └── dedup_state/                                │
│     ├── watermarks.json (updated)               │
│     ├── content_hashes.json (updated)           │
│     └── conversation_log.jsonl (appended)       │
│                                                 │
│ README.md (updated with checkpoint reference)   │
└─────────────────────────────────────────────────┘
```

---

## Storage Architecture

### Phase 1: JSON File Backend (MVP)

```
MEMORY-CONTEXT/
└── dedup_state/
    ├── watermarks.json
    │   {
    │     "conversation_id": highest_index_processed,
    │     "rollout-master": 25,
    │     "framework-development": 150,
    │     ...
    │   }
    │
    ├── content_hashes.json
    │   {
    │     "conversation_id": ["hash1", "hash2", ...],
    │     "rollout-master": [
    │       "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    │       "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a",
    │       ...
    │     ],
    │     ...
    │   }
    │
    └── conversation_log.jsonl
        {"conversation_id": "rollout-master", "timestamp": "2025-11-17T10:00:00Z", "content_hash": "e3b0c44...", "message": {...}}
        {"conversation_id": "rollout-master", "timestamp": "2025-11-17T10:01:00Z", "content_hash": "a7ffc6f...", "message": {...}}
        ...
```

**Characteristics:**
- Fast read/write (no database connection)
- Simple implementation (standard library only)
- Limited scalability (~1,000 conversations, ~10,000 messages total)
- Perfect for MVP and testing

### Phase 2: PostgreSQL Backend (Production)

**Schema (see DATABASE-DESIGN.md for complete DDL):**

```sql
-- Conversations table (metadata)
CREATE TABLE conversations (
    conversation_id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_messages INTEGER DEFAULT 0,
    metadata JSONB
);

-- Messages table (append-only log)
CREATE TABLE messages (
    message_id BIGSERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) REFERENCES conversations(conversation_id),
    message_index INTEGER NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    role VARCHAR(50),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    UNIQUE(conversation_id, message_index)
);

-- Watermarks table (fast lookups)
CREATE TABLE watermarks (
    conversation_id VARCHAR(255) PRIMARY KEY REFERENCES conversations(conversation_id),
    highest_index INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Content hashes index (fast duplicate detection)
CREATE INDEX idx_messages_content_hash ON messages(conversation_id, content_hash);
CREATE INDEX idx_messages_index ON messages(conversation_id, message_index);
```

**Characteristics:**
- Scalable to millions of messages
- ACID guarantees (transactional consistency)
- SQL queryability (analytics, search)
- Perfect for production deployment

**Migration Path (JSON → PostgreSQL):**
```python
def migrate_to_postgresql():
    """Migrate from JSON files to PostgreSQL"""
    # 1. Load JSON state
    watermarks = load_json('watermarks.json')
    content_hashes = load_json('content_hashes.json')

    # 2. Insert into PostgreSQL
    for conv_id, watermark in watermarks.items():
        # Insert conversation
        db.execute("INSERT INTO conversations (conversation_id) VALUES (%s)", (conv_id,))

        # Insert watermark
        db.execute("INSERT INTO watermarks (conversation_id, highest_index) VALUES (%s, %s)",
                   (conv_id, watermark))

    # 3. Parse JSONL log and insert messages
    with open('conversation_log.jsonl', 'r') as f:
        for line in f:
            event = json.loads(line)
            db.execute("""
                INSERT INTO messages (conversation_id, message_index, content_hash, content)
                VALUES (%s, %s, %s, %s)
            """, (event['conversation_id'], event['message']['index'],
                  event['content_hash'], event['message']['content']))

    # 4. Verify integrity
    verify_migration()
```

---

## API Specifications

### Python API (Core Library)

```python
from deduplication import ClaudeConversationDeduplicator

# Initialize (JSON backend)
dedup = ClaudeConversationDeduplicator(
    storage_dir='./MEMORY-CONTEXT/dedup_state'
)

# Initialize (PostgreSQL backend)
dedup = ClaudeConversationDeduplicator(
    backend='postgresql',
    connection_string='postgresql://user:pass@localhost/dedup_db'
)

# Process single export
new_messages = dedup.process_export(
    conversation_id='rollout-master',
    export_data={'messages': [...]}
)

# Get statistics
stats = dedup.get_statistics('rollout-master')
# Returns: {
#   'watermark': 25,
#   'unique_messages': 26,
#   'total_messages': 26,
#   'storage_savings_pct': 73.0
# }

# Reconstruct full conversation
full_conversation = dedup.get_full_conversation('rollout-master')
# Returns: List of all unique messages, sorted by index

# Detect gaps
gaps = dedup.detect_gaps('rollout-master', messages)
# Returns: [(5, 7), (10, 12)] # Gap from index 5-7, 10-12
```

### CLI API

```bash
# Single file deduplication
python deduplicate_export.py export.txt \
    --session-id rollout-master \
    --output new_messages.json \
    --stats

# Batch processing
python deduplicate_export.py MEMORY-CONTEXT/exports/ \
    --batch \
    --output-dir MEMORY-CONTEXT/sessions/

# Statistics only
python deduplicate_export.py export.txt \
    --session-id rollout-master \
    --stats-only

# PostgreSQL backend
python deduplicate_export.py export.txt \
    --session-id rollout-master \
    --backend postgresql \
    --db-url postgresql://localhost/dedup_db
```

### Integration API (CODITECT)

```python
from deduplication.integration import SessionExportManager

# Initialize
manager = SessionExportManager(
    project_root='/Users/halcasteel/PROJECTS/coditect-rollout-master'
)

# Import export (auto-detects session ID from filename)
result = manager.import_export(
    export_file='MEMORY-CONTEXT/exports/2025-11-17-EXPORT-ROLLOUT-MASTER.txt'
)

# Returns:
# {
#   'session_id': 'rollout-master',
#   'total_messages': 26,
#   'new_messages': 15,
#   'duplicates_filtered': 11,
#   'storage_savings_pct': 73.0,
#   'session_file': 'MEMORY-CONTEXT/sessions/rollout-master.md'
# }

# Manual session ID override
result = manager.import_export(
    export_file='export.txt',
    session_id='custom-session-id'
)
```

---

## Integration Points

### 1. CODITECT Checkpoint Automation

**File:** `.coditect/scripts/create-checkpoint.py`

**Integration Point:** Add deduplication step before checkpoint creation

```python
# In create-checkpoint.py (modified)

from deduplication.integration import SessionExportManager

class CheckpointCreator:
    def __init__(self, base_dir):
        # ... existing code ...
        self.session_manager = SessionExportManager(base_dir)

    def run(self, sprint_description, auto_commit=False):
        # ... existing steps ...

        # NEW: Step 3.5 - Deduplicate conversation export
        if export_path.exists():
            print("Step 3.5: Deduplicating conversation export...")
            result = self.session_manager.import_export(export_path)
            print(f"  New messages: {result['new_messages']}")
            print(f"  Duplicates filtered: {result['duplicates_filtered']}")
            print(f"  Storage savings: {result['storage_savings_pct']:.1f}%")

        # ... continue with existing steps ...
```

### 2. MEMORY-CONTEXT Storage Structure

**Before Deduplication:**
```
MEMORY-CONTEXT/
├── 2025-11-16-EXPORT-CHECKPOINT.txt (13KB)
├── 2025-11-17-EXPORT-MEMORY-CONTEXT-DOT-CODITECT.txt (51KB)
└── 2025-11-16T1523-RESTORE-CONTEXT.txt (439KB)
Total: 503KB (95% duplicates)
```

**After Deduplication:**
```
MEMORY-CONTEXT/
├── exports/                          # Raw exports (archived)
│   ├── 2025-11-16-EXPORT-CHECKPOINT.txt (13KB)
│   ├── 2025-11-17-EXPORT-MEMORY-CONTEXT-DOT-CODITECT.txt (51KB)
│   └── 2025-11-16T1523-RESTORE-CONTEXT.txt (439KB)
│
├── sessions/                         # Deduplicated sessions
│   ├── rollout-master.md (25KB)     # Only unique messages
│   └── framework-development.md (15KB)
│
└── dedup_state/                      # Deduplication state
    ├── watermarks.json (1KB)
    ├── content_hashes.json (5KB)
    └── conversation_log.jsonl (30KB)

Total: 503KB (raw) + 61KB (deduplicated) = 564KB
Effective storage: 61KB (89% savings)
```

### 3. Session Continuity Workflow

**Scenario:** Multi-day project spanning 5 sessions

```
Session 1 (Day 1):
  /export → 13KB
  Deduplicate → 13KB new (100% unique)
  Session file: session-1.md (13KB)

Session 2 (Day 2):
  /export → 51KB (includes all of Session 1 + new)
  Deduplicate → 38KB new (25% unique)
  Session file: session-2.md (38KB)

Session 3 (Day 3):
  /export → 439KB (includes all previous + new)
  Deduplicate → 388KB new (12% unique)
  Session file: session-3.md (388KB)

Session 4 (Day 4):
  /export → 850KB (includes all previous + new)
  Deduplicate → 411KB new (52% unique)
  Session file: session-4.md (411KB)

Session 5 (Day 5):
  /export → 1.2MB (includes all previous + new)
  Deduplicate → 350KB new (29% unique)
  Session file: session-5.md (350KB)

Total Raw Exports: 2.55MB
Total Unique Content: 1.2MB
Storage Savings: 53% (and growing with more sessions)
```

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| **Process Export** | O(n) | n = messages in export |
| **Sequence Check** | O(1) | Direct watermark comparison |
| **Content Hash Check** | O(1) | Hash set lookup |
| **Append to Log** | O(1) | Append-only write |
| **State Save** | O(k) | k = unique messages seen |
| **Full Reconstruction** | O(m) | m = total unique messages |

### Space Complexity

| Component | Complexity | Notes |
|-----------|------------|-------|
| **Watermarks** | O(c) | c = number of conversations |
| **Content Hashes** | O(k) | k = unique messages per conversation |
| **Append-Only Log** | O(m) | m = total unique messages (unbounded) |
| **Total** | O(c + k + m) | Linear growth |

### Performance Benchmarks (Estimated)

| Export Size | Messages | Processing Time | Memory Usage |
|-------------|----------|-----------------|--------------|
| 13KB | 10 | <100ms | <5MB |
| 51KB | 50 | <200ms | <10MB |
| 439KB | 500 | <1s | <50MB |
| 1MB | 1,000 | <2s | <100MB |
| 10MB | 10,000 | <10s | <500MB |

**Note:** Actual performance will be validated during Phase 3 optimization.

---

## Security & Privacy Considerations

### Data Protection

1. **Content Hashing (SHA-256)**
   - One-way hash function (irreversible)
   - Collisions statistically impossible (2^256 space)
   - Safe for deduplication without exposing content

2. **State File Protection**
   - Store in `MEMORY-CONTEXT/` (gitignored by default)
   - File permissions: 600 (owner read/write only)
   - No sensitive data in watermarks (just indices)

3. **PostgreSQL Security**
   - Connection strings in environment variables (not code)
   - Use SSL/TLS for database connections
   - Role-based access control (RBAC)
   - Encrypted backups

### Privacy Compliance

**Data Retention:**
- Append-only log retains all unique messages indefinitely
- Implement data purge API for GDPR compliance
- Allow conversation deletion by conversation_id

**PII Handling:**
- Deduplication system is content-agnostic
- Integrates with existing CODITECT privacy manager
- Can run privacy scan before deduplication (optional)

**Audit Trail:**
- All deduplication operations logged
- Deduplication log table tracks when messages processed
- Full reconstruction possible for compliance audits

---

## Monitoring & Observability

### Metrics to Track

**Deduplication Metrics:**
- Total exports processed
- Total messages processed
- Duplicates filtered (count, percentage)
- Storage savings (bytes, percentage)
- Processing time per export

**System Health Metrics:**
- Database connection pool status
- Query performance (average, p95, p99)
- Disk usage (append-only log growth)
- Error rates (parse errors, database errors)

**Business Metrics:**
- Active conversations count
- Average messages per conversation
- Deduplication efficiency trend over time

### Alerting Rules

**Critical Alerts:**
- Database connection failure
- Data corruption detected (hash mismatch)
- Disk space < 10% free

**Warning Alerts:**
- Gaps detected in message sequences
- Processing time > 10s for single export
- Deduplication rate < 50% (unexpected)

**Info Alerts:**
- Large export processed (>10MB)
- New conversation created
- Daily statistics summary

### Monitoring Dashboard

**Components:**
- **Overview Panel:** Total conversations, messages, storage savings
- **Trends Chart:** Deduplication rate over time
- **Performance Chart:** Processing time distribution
- **Alerts Panel:** Recent alerts and their status
- **Conversation List:** Top conversations by message count

**Technology:** Grafana + Prometheus (or simple Flask dashboard for MVP)

---

## Disaster Recovery

### Backup Strategy

**JSON Files (Phase 1):**
- Daily backup of entire `MEMORY-CONTEXT/dedup_state/` directory
- Retention: 30 days
- Storage: Git LFS or cloud storage (S3)

**PostgreSQL (Phase 2):**
- Continuous WAL archiving
- Daily full backups
- Point-in-time recovery capability
- Retention: 90 days

### Recovery Procedures

**Scenario 1: State File Corruption**
```python
# Detect corruption
if not validate_state(watermarks_file):
    # Restore from backup
    restore_from_backup(watermarks_file, date='yesterday')

    # Re-index from append-only log
    rebuild_state_from_log()
```

**Scenario 2: Database Failure**
```bash
# Restore from latest backup
pg_restore -d dedup_db latest_backup.dump

# Verify integrity
python verify_database_integrity.py

# Resume operations
```

**Scenario 3: Complete Data Loss**
```python
# Rebuild from raw exports (nuclear option)
for export_file in glob('MEMORY-CONTEXT/exports/*.txt'):
    # Reprocess all exports from scratch
    dedup.process_export(
        conversation_id=extract_session_id(export_file),
        export_data=load_export(export_file)
    )

# Result: State fully reconstructed from raw data
```

---

## Appendix A: Technology Stack

### Core Technologies
- **Python 3.9+** - Implementation language
- **PostgreSQL 14+** - Production database
- **Click/argparse** - CLI framework
- **pytest** - Testing framework

### Dependencies
```
# requirements.txt
psycopg2-binary>=2.9.0  # PostgreSQL adapter
click>=8.0.0             # CLI framework
tqdm>=4.60.0             # Progress bars
pytest>=7.0.0            # Testing
pytest-cov>=3.0.0        # Coverage reporting
```

### Development Tools
- **Black** - Code formatting
- **Flake8** - Linting
- **mypy** - Type checking
- **Sphinx** - Documentation generation

---

## Appendix B: Future Enhancements

### Phase 4 Roadmap (Post-MVP)

1. **Semantic Deduplication** (ML-based)
   - Detect near-duplicates using embeddings
   - Configurable similarity threshold
   - Expected additional 2-5% savings

2. **Delta Encoding** (Optional)
   - Compress similar messages using bsdiff
   - For very large exports (>10MB)
   - Marginal improvement over message-level dedup

3. **Real-Time Streaming**
   - WebSocket API for real-time deduplication
   - Integrate with Claude API directly
   - No manual /export needed

4. **Multi-User Support**
   - User authentication and authorization
   - Per-user conversation isolation
   - Team-level analytics

5. **Advanced Analytics**
   - Conversation topic clustering
   - Message sentiment analysis
   - Participant activity heatmaps

6. **Export Format Support**
   - Support official Claude exports (when available)
   - Support API response format
   - Auto-detect and normalize formats

---

**Document Status:** ✅ Architecture Design Complete
**Last Updated:** 2025-11-17
**Next Steps:** Begin Phase 1 Implementation
**Owner:** AZ1.AI CODITECT Team
