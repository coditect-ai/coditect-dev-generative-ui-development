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
# Conversation Export Deduplication - Database Design

**Project:** Claude Conversation Export Deduplication System
**Database:** PostgreSQL 14+
**Version:** 1.0
**Date:** 2025-11-17
**Status:** Schema Design Complete - Ready for Implementation

**Related Documents:**
- Implementation Plan: `docs/CONVERSATION-DEDUPLICATION-IMPLEMENTATION-PLAN.md`
- Architecture: `docs/CONVERSATION-DEDUPLICATION-ARCHITECTURE.md`
- Research: `MEMORY-CONTEXT/RESEARCH-CLAUDE-CONVERSATION-EXPORT-DEDUPLICATION.md`

---

## Executive Summary

This document provides the complete PostgreSQL database schema for the Conversation Export Deduplication System (Phase 2 production backend). The schema supports:

- **Scalability:** Millions of messages across thousands of conversations
- **Performance:** Optimized indexes for fast deduplication lookups
- **Integrity:** Foreign keys and constraints ensure data consistency
- **Auditability:** Complete audit trail of all deduplication operations
- **Queryability:** Rich SQL access for analytics and reporting

**Migration Path:** JSON files (Phase 1) → PostgreSQL (Phase 2) with zero data loss.

---

## Table of Contents

1. [Schema Overview](#schema-overview)
2. [Table Definitions](#table-definitions)
3. [Indexes & Constraints](#indexes--constraints)
4. [Complete DDL](#complete-ddl)
5. [Migration Scripts](#migration-scripts)
6. [Query Patterns](#query-patterns)
7. [Performance Tuning](#performance-tuning)
8. [Backup & Recovery](#backup--recovery)
9. [Security](#security)
10. [Partitioning Strategy](#partitioning-strategy)

---

## Schema Overview

### Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────┐
│                      Database Schema                             │
│                                                                  │
│  ┌──────────────────┐                                            │
│  │  conversations   │                                            │
│  ├──────────────────┤                                            │
│  │ PK conversation_id (VARCHAR 255)                             │
│  │    created_at (TIMESTAMP)                                    │
│  │    last_updated (TIMESTAMP)                                  │
│  │    total_messages (INTEGER)                                  │
│  │    metadata (JSONB)                                          │
│  └────────┬─────────┘                                            │
│           │                                                      │
│           │ 1:N                                                  │
│           │                                                      │
│  ┌────────▼─────────────────┐                                   │
│  │       messages           │                                   │
│  ├──────────────────────────┤                                   │
│  │ PK message_id (BIGSERIAL)                                    │
│  │ FK conversation_id (VARCHAR 255)  ◄────┐                     │
│  │    message_index (INTEGER)             │                     │
│  │    content_hash (VARCHAR 64)           │                     │
│  │    role (VARCHAR 50)                   │ Foreign Key         │
│  │    content (TEXT)                      │                     │
│  │    created_at (TIMESTAMP)              │                     │
│  │    metadata (JSONB)                    │                     │
│  │ UK (conversation_id, message_index)    │                     │
│  └──────────────────────────┘             │                     │
│           │                                │                     │
│           │ 1:1                            │                     │
│           │                                │                     │
│  ┌────────▼────────────────┐              │                     │
│  │      watermarks         │              │                     │
│  ├─────────────────────────┤              │                     │
│  │ PK conversation_id (VARCHAR 255)  ◄────┘                     │
│  │    highest_index (INTEGER)                                   │
│  │    last_updated (TIMESTAMP)                                  │
│  └─────────────────────────┘                                    │
│           │                                                      │
│           │ 1:1                                                  │
│           │                                                      │
│  ┌────────▼──────────────────┐                                  │
│  │   deduplication_log       │                                  │
│  ├───────────────────────────┤                                  │
│  │ PK log_id (BIGSERIAL)                                        │
│  │ FK conversation_id (VARCHAR 255)                             │
│  │    operation (VARCHAR 50)                                    │
│  │    messages_processed (INTEGER)                              │
│  │    duplicates_filtered (INTEGER)                             │
│  │    storage_savings_pct (DECIMAL)                             │
│  │    processing_time_ms (INTEGER)                              │
│  │    created_at (TIMESTAMP)                                    │
│  │    metadata (JSONB)                                          │
│  └───────────────────────────┘                                  │
│                                                                  │
│  ┌────────────────────────────┐                                 │
│  │  content_hashes (Optional) │                                 │
│  ├────────────────────────────┤                                 │
│  │ PK hash_id (BIGSERIAL)                                       │
│  │ FK conversation_id (VARCHAR 255)                             │
│  │    content_hash (VARCHAR 64)                                 │
│  │ UK (conversation_id, content_hash)                           │
│  └────────────────────────────┘                                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

Legend:
  PK = Primary Key
  FK = Foreign Key
  UK = Unique Key
  1:N = One-to-Many relationship
  1:1 = One-to-One relationship
```

### Table Summary

| Table | Purpose | Rows (Expected) | Growth Rate |
|-------|---------|-----------------|-------------|
| **conversations** | Conversation metadata | 100-1,000 | Low (new projects) |
| **messages** | Append-only message log | 10,000-1,000,000 | High (daily) |
| **watermarks** | Highest processed index | 100-1,000 | Low (matches conversations) |
| **deduplication_log** | Audit trail | 1,000-10,000 | Medium (per export) |
| **content_hashes** | Fast duplicate lookup (optional) | 10,000-1,000,000 | High (matches messages) |

---

## Table Definitions

### 1. conversations

**Purpose:** Store metadata for each conversation (project/session).

**Schema:**
```sql
CREATE TABLE conversations (
    conversation_id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total_messages INTEGER DEFAULT 0 NOT NULL,
    metadata JSONB,

    CONSTRAINT chk_total_messages_positive CHECK (total_messages >= 0)
);

COMMENT ON TABLE conversations IS 'Metadata for each conversation/project';
COMMENT ON COLUMN conversations.conversation_id IS 'Unique identifier for conversation (e.g., rollout-master)';
COMMENT ON COLUMN conversations.created_at IS 'Timestamp when conversation first seen';
COMMENT ON COLUMN conversations.last_updated IS 'Timestamp of last export processing';
COMMENT ON COLUMN conversations.total_messages IS 'Cached count of total unique messages';
COMMENT ON COLUMN conversations.metadata IS 'Additional metadata (project name, tags, etc.)';
```

**Example Row:**
```sql
INSERT INTO conversations (conversation_id, total_messages, metadata) VALUES (
    'rollout-master',
    26,
    '{"project": "CODITECT Rollout Master", "tags": ["coditect", "master"]}'::JSONB
);
```

**Indexes:**
```sql
CREATE INDEX idx_conversations_last_updated ON conversations(last_updated DESC);
CREATE INDEX idx_conversations_metadata ON conversations USING GIN(metadata);
```

---

### 2. messages

**Purpose:** Append-only log of all unique messages across all conversations.

**Schema:**
```sql
CREATE TABLE messages (
    message_id BIGSERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    message_index INTEGER NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    role VARCHAR(50),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    metadata JSONB,

    CONSTRAINT uk_conversation_message_index UNIQUE (conversation_id, message_index),
    CONSTRAINT chk_message_index_positive CHECK (message_index >= 0)
);

COMMENT ON TABLE messages IS 'Append-only log of all unique messages';
COMMENT ON COLUMN messages.message_id IS 'Auto-incrementing unique message ID';
COMMENT ON COLUMN messages.conversation_id IS 'Foreign key to conversations table';
COMMENT ON COLUMN messages.message_index IS 'Sequential index within conversation (from export)';
COMMENT ON COLUMN messages.content_hash IS 'SHA-256 hash of normalized message content';
COMMENT ON COLUMN messages.role IS 'Message role: user, assistant, system';
COMMENT ON COLUMN messages.content IS 'Full message content (text/JSON)';
COMMENT ON COLUMN messages.created_at IS 'Timestamp when message added to database';
COMMENT ON COLUMN messages.metadata IS 'Additional metadata (timestamps, tool calls, etc.)';
```

**Example Row:**
```sql
INSERT INTO messages (conversation_id, message_index, content_hash, role, content, metadata) VALUES (
    'rollout-master',
    0,
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'user',
    'Hello, Claude',
    '{"timestamp": "2025-11-17T10:00:00Z", "tools_used": []}'::JSONB
);
```

**Indexes:**
```sql
-- Primary lookup: Find message by conversation and index (fast watermark check)
CREATE INDEX idx_messages_conversation_index ON messages(conversation_id, message_index);

-- Duplicate detection: Find messages by content hash
CREATE INDEX idx_messages_content_hash ON messages(conversation_id, content_hash);

-- Time-based queries: Latest messages
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);

-- Full-text search (optional, for advanced queries)
CREATE INDEX idx_messages_content_fts ON messages USING GIN(to_tsvector('english', content));
```

---

### 3. watermarks

**Purpose:** Track highest processed message index per conversation (fast deduplication).

**Schema:**
```sql
CREATE TABLE watermarks (
    conversation_id VARCHAR(255) PRIMARY KEY REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    highest_index INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT chk_highest_index_positive CHECK (highest_index >= -1)
);

COMMENT ON TABLE watermarks IS 'Highest processed message index per conversation';
COMMENT ON COLUMN watermarks.conversation_id IS 'Foreign key to conversations table';
COMMENT ON COLUMN watermarks.highest_index IS 'Highest message index processed (-1 = none yet)';
COMMENT ON COLUMN watermarks.last_updated IS 'Timestamp of last watermark update';
```

**Example Row:**
```sql
INSERT INTO watermarks (conversation_id, highest_index) VALUES (
    'rollout-master',
    25
);
```

**Indexes:**
```sql
-- Primary key already provides index on conversation_id
-- No additional indexes needed (table is small and frequently updated)
```

---

### 4. deduplication_log

**Purpose:** Audit trail of all deduplication operations (statistics, performance).

**Schema:**
```sql
CREATE TABLE deduplication_log (
    log_id BIGSERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    operation VARCHAR(50) NOT NULL,
    messages_processed INTEGER NOT NULL,
    duplicates_filtered INTEGER NOT NULL,
    storage_savings_pct DECIMAL(5,2),
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    metadata JSONB,

    CONSTRAINT chk_messages_processed_positive CHECK (messages_processed >= 0),
    CONSTRAINT chk_duplicates_filtered_positive CHECK (duplicates_filtered >= 0),
    CONSTRAINT chk_processing_time_positive CHECK (processing_time_ms >= 0)
);

COMMENT ON TABLE deduplication_log IS 'Audit trail of deduplication operations';
COMMENT ON COLUMN deduplication_log.log_id IS 'Auto-incrementing log entry ID';
COMMENT ON COLUMN deduplication_log.conversation_id IS 'Conversation being processed';
COMMENT ON COLUMN deduplication_log.operation IS 'Operation type: process_export, migrate, rebuild';
COMMENT ON COLUMN deduplication_log.messages_processed IS 'Total messages in export';
COMMENT ON COLUMN deduplication_log.duplicates_filtered IS 'Number of duplicates filtered';
COMMENT ON COLUMN deduplication_log.storage_savings_pct IS 'Percentage of storage saved';
COMMENT ON COLUMN deduplication_log.processing_time_ms IS 'Processing time in milliseconds';
COMMENT ON COLUMN deduplication_log.created_at IS 'Timestamp of operation';
COMMENT ON COLUMN deduplication_log.metadata IS 'Additional operation metadata';
```

**Example Row:**
```sql
INSERT INTO deduplication_log (conversation_id, operation, messages_processed, duplicates_filtered, storage_savings_pct, processing_time_ms, metadata) VALUES (
    'rollout-master',
    'process_export',
    26,
    11,
    73.08,
    150,
    '{"export_file": "2025-11-17-EXPORT-ROLLOUT-MASTER.txt", "export_size_kb": 51}'::JSONB
);
```

**Indexes:**
```sql
CREATE INDEX idx_deduplication_log_conversation ON deduplication_log(conversation_id, created_at DESC);
CREATE INDEX idx_deduplication_log_created_at ON deduplication_log(created_at DESC);
CREATE INDEX idx_deduplication_log_operation ON deduplication_log(operation);
```

---

### 5. content_hashes (Optional)

**Purpose:** Fast content hash lookups (alternative to storing hashes in messages table).

**Note:** This table is optional - you can store content_hash directly in `messages` table. Use this if you want a separate normalized table for hashes.

**Schema:**
```sql
CREATE TABLE content_hashes (
    hash_id BIGSERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    content_hash VARCHAR(64) NOT NULL,

    CONSTRAINT uk_conversation_content_hash UNIQUE (conversation_id, content_hash)
);

COMMENT ON TABLE content_hashes IS 'Normalized table for content hashes (optional)';
COMMENT ON COLUMN content_hashes.hash_id IS 'Auto-incrementing hash ID';
COMMENT ON COLUMN content_hashes.conversation_id IS 'Conversation this hash belongs to';
COMMENT ON COLUMN content_hashes.content_hash IS 'SHA-256 content hash';
```

**Indexes:**
```sql
CREATE INDEX idx_content_hashes_conversation ON content_hashes(conversation_id);
-- Unique constraint already provides index on (conversation_id, content_hash)
```

**Design Note:** We recommend storing `content_hash` directly in the `messages` table for simplicity. This separate table is only needed if you want to normalize hashes or track hash metadata separately.

---

## Indexes & Constraints

### Index Strategy

**Primary Indexes (Automatically Created):**
- `conversations.conversation_id` (PRIMARY KEY)
- `messages.message_id` (PRIMARY KEY)
- `watermarks.conversation_id` (PRIMARY KEY)
- `deduplication_log.log_id` (PRIMARY KEY)

**Performance Indexes:**
```sql
-- Deduplication hot path (most frequent queries)
CREATE INDEX idx_messages_conversation_index ON messages(conversation_id, message_index);
CREATE INDEX idx_messages_content_hash ON messages(conversation_id, content_hash);

-- Analytics and reporting
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_deduplication_log_created_at ON deduplication_log(created_at DESC);

-- Metadata queries (JSONB)
CREATE INDEX idx_conversations_metadata ON conversations USING GIN(metadata);
CREATE INDEX idx_messages_metadata ON messages USING GIN(metadata);

-- Full-text search (optional)
CREATE INDEX idx_messages_content_fts ON messages USING GIN(to_tsvector('english', content));
```

### Unique Constraints

```sql
-- Prevent duplicate message indices within same conversation
ALTER TABLE messages ADD CONSTRAINT uk_conversation_message_index
    UNIQUE (conversation_id, message_index);

-- Prevent duplicate content hashes within same conversation (optional table)
ALTER TABLE content_hashes ADD CONSTRAINT uk_conversation_content_hash
    UNIQUE (conversation_id, content_hash);
```

### Check Constraints

```sql
-- Ensure non-negative values
ALTER TABLE conversations ADD CONSTRAINT chk_total_messages_positive
    CHECK (total_messages >= 0);

ALTER TABLE messages ADD CONSTRAINT chk_message_index_positive
    CHECK (message_index >= 0);

ALTER TABLE watermarks ADD CONSTRAINT chk_highest_index_positive
    CHECK (highest_index >= -1);  -- -1 means no messages processed yet

ALTER TABLE deduplication_log ADD CONSTRAINT chk_messages_processed_positive
    CHECK (messages_processed >= 0);

ALTER TABLE deduplication_log ADD CONSTRAINT chk_duplicates_filtered_positive
    CHECK (duplicates_filtered >= 0);

ALTER TABLE deduplication_log ADD CONSTRAINT chk_processing_time_positive
    CHECK (processing_time_ms >= 0);
```

### Foreign Key Constraints

```sql
-- messages.conversation_id → conversations.conversation_id (CASCADE DELETE)
ALTER TABLE messages ADD CONSTRAINT fk_messages_conversation
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE;

-- watermarks.conversation_id → conversations.conversation_id (CASCADE DELETE)
ALTER TABLE watermarks ADD CONSTRAINT fk_watermarks_conversation
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE;

-- deduplication_log.conversation_id → conversations.conversation_id (CASCADE DELETE)
ALTER TABLE deduplication_log ADD CONSTRAINT fk_deduplication_log_conversation
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE;

-- content_hashes.conversation_id → conversations.conversation_id (CASCADE DELETE)
ALTER TABLE content_hashes ADD CONSTRAINT fk_content_hashes_conversation
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE;
```

---

## Complete DDL

### Full Schema Creation Script

**File:** `scripts/database/create_schema.sql`

```sql
-- ============================================================================
-- Conversation Export Deduplication - PostgreSQL Schema
-- Version: 1.0
-- Date: 2025-11-17
-- ============================================================================

-- Drop existing schema (WARNING: This will delete all data!)
-- Uncomment only if you want to recreate from scratch
-- DROP TABLE IF EXISTS content_hashes CASCADE;
-- DROP TABLE IF EXISTS deduplication_log CASCADE;
-- DROP TABLE IF EXISTS watermarks CASCADE;
-- DROP TABLE IF EXISTS messages CASCADE;
-- DROP TABLE IF EXISTS conversations CASCADE;

-- ============================================================================
-- Table: conversations
-- Purpose: Store metadata for each conversation/project
-- ============================================================================

CREATE TABLE conversations (
    conversation_id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total_messages INTEGER DEFAULT 0 NOT NULL,
    metadata JSONB,

    CONSTRAINT chk_total_messages_positive CHECK (total_messages >= 0)
);

CREATE INDEX idx_conversations_last_updated ON conversations(last_updated DESC);
CREATE INDEX idx_conversations_metadata ON conversations USING GIN(metadata);

COMMENT ON TABLE conversations IS 'Metadata for each conversation/project';
COMMENT ON COLUMN conversations.conversation_id IS 'Unique identifier for conversation (e.g., rollout-master)';
COMMENT ON COLUMN conversations.created_at IS 'Timestamp when conversation first seen';
COMMENT ON COLUMN conversations.last_updated IS 'Timestamp of last export processing';
COMMENT ON COLUMN conversations.total_messages IS 'Cached count of total unique messages';
COMMENT ON COLUMN conversations.metadata IS 'Additional metadata (project name, tags, etc.)';

-- ============================================================================
-- Table: messages
-- Purpose: Append-only log of all unique messages
-- ============================================================================

CREATE TABLE messages (
    message_id BIGSERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    message_index INTEGER NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    role VARCHAR(50),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    metadata JSONB,

    CONSTRAINT uk_conversation_message_index UNIQUE (conversation_id, message_index),
    CONSTRAINT chk_message_index_positive CHECK (message_index >= 0)
);

CREATE INDEX idx_messages_conversation_index ON messages(conversation_id, message_index);
CREATE INDEX idx_messages_content_hash ON messages(conversation_id, content_hash);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_messages_metadata ON messages USING GIN(metadata);

-- Optional: Full-text search index (uncomment if needed)
-- CREATE INDEX idx_messages_content_fts ON messages USING GIN(to_tsvector('english', content));

COMMENT ON TABLE messages IS 'Append-only log of all unique messages';
COMMENT ON COLUMN messages.message_id IS 'Auto-incrementing unique message ID';
COMMENT ON COLUMN messages.conversation_id IS 'Foreign key to conversations table';
COMMENT ON COLUMN messages.message_index IS 'Sequential index within conversation (from export)';
COMMENT ON COLUMN messages.content_hash IS 'SHA-256 hash of normalized message content';
COMMENT ON COLUMN messages.role IS 'Message role: user, assistant, system';
COMMENT ON COLUMN messages.content IS 'Full message content (text/JSON)';
COMMENT ON COLUMN messages.created_at IS 'Timestamp when message added to database';
COMMENT ON COLUMN messages.metadata IS 'Additional metadata (timestamps, tool calls, etc.)';

-- ============================================================================
-- Table: watermarks
-- Purpose: Track highest processed message index per conversation
-- ============================================================================

CREATE TABLE watermarks (
    conversation_id VARCHAR(255) PRIMARY KEY REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    highest_index INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT chk_highest_index_positive CHECK (highest_index >= -1)
);

COMMENT ON TABLE watermarks IS 'Highest processed message index per conversation';
COMMENT ON COLUMN watermarks.conversation_id IS 'Foreign key to conversations table';
COMMENT ON COLUMN watermarks.highest_index IS 'Highest message index processed (-1 = none yet)';
COMMENT ON COLUMN watermarks.last_updated IS 'Timestamp of last watermark update';

-- ============================================================================
-- Table: deduplication_log
-- Purpose: Audit trail of deduplication operations
-- ============================================================================

CREATE TABLE deduplication_log (
    log_id BIGSERIAL PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    operation VARCHAR(50) NOT NULL,
    messages_processed INTEGER NOT NULL,
    duplicates_filtered INTEGER NOT NULL,
    storage_savings_pct DECIMAL(5,2),
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    metadata JSONB,

    CONSTRAINT chk_messages_processed_positive CHECK (messages_processed >= 0),
    CONSTRAINT chk_duplicates_filtered_positive CHECK (duplicates_filtered >= 0),
    CONSTRAINT chk_processing_time_positive CHECK (processing_time_ms >= 0)
);

CREATE INDEX idx_deduplication_log_conversation ON deduplication_log(conversation_id, created_at DESC);
CREATE INDEX idx_deduplication_log_created_at ON deduplication_log(created_at DESC);
CREATE INDEX idx_deduplication_log_operation ON deduplication_log(operation);
CREATE INDEX idx_deduplication_log_metadata ON deduplication_log USING GIN(metadata);

COMMENT ON TABLE deduplication_log IS 'Audit trail of deduplication operations';
COMMENT ON COLUMN deduplication_log.log_id IS 'Auto-incrementing log entry ID';
COMMENT ON COLUMN deduplication_log.conversation_id IS 'Conversation being processed';
COMMENT ON COLUMN deduplication_log.operation IS 'Operation type: process_export, migrate, rebuild';
COMMENT ON COLUMN deduplication_log.messages_processed IS 'Total messages in export';
COMMENT ON COLUMN deduplication_log.duplicates_filtered IS 'Number of duplicates filtered';
COMMENT ON COLUMN deduplication_log.storage_savings_pct IS 'Percentage of storage saved';
COMMENT ON COLUMN deduplication_log.processing_time_ms IS 'Processing time in milliseconds';
COMMENT ON COLUMN deduplication_log.created_at IS 'Timestamp of operation';
COMMENT ON COLUMN deduplication_log.metadata IS 'Additional operation metadata';

-- ============================================================================
-- Table: content_hashes (Optional)
-- Purpose: Normalized content hash lookup (alternative to storing in messages)
-- ============================================================================

-- OPTIONAL: Uncomment if you want separate hash table
-- CREATE TABLE content_hashes (
--     hash_id BIGSERIAL PRIMARY KEY,
--     conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
--     content_hash VARCHAR(64) NOT NULL,
--
--     CONSTRAINT uk_conversation_content_hash UNIQUE (conversation_id, content_hash)
-- );
--
-- CREATE INDEX idx_content_hashes_conversation ON content_hashes(conversation_id);
--
-- COMMENT ON TABLE content_hashes IS 'Normalized table for content hashes (optional)';
-- COMMENT ON COLUMN content_hashes.hash_id IS 'Auto-incrementing hash ID';
-- COMMENT ON COLUMN content_hashes.conversation_id IS 'Conversation this hash belongs to';
-- COMMENT ON COLUMN content_hashes.content_hash IS 'SHA-256 content hash';

-- ============================================================================
-- Triggers: Update timestamps automatically
-- ============================================================================

-- Update conversations.last_updated when messages added
CREATE OR REPLACE FUNCTION update_conversation_last_updated()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET last_updated = CURRENT_TIMESTAMP
    WHERE conversation_id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_messages_update_conversation
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION update_conversation_last_updated();

-- Update watermarks.last_updated automatically
CREATE OR REPLACE FUNCTION update_watermark_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_watermarks_update_timestamp
BEFORE UPDATE ON watermarks
FOR EACH ROW
EXECUTE FUNCTION update_watermark_timestamp();

-- ============================================================================
-- Grant Permissions (adjust as needed for your environment)
-- ============================================================================

-- Example: Grant all privileges to application role
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dedup_app_role;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO dedup_app_role;

-- ============================================================================
-- Schema Creation Complete
-- ============================================================================

-- Verify schema
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('conversations', 'messages', 'watermarks', 'deduplication_log')
ORDER BY table_name, ordinal_position;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Conversation Deduplication schema created successfully!';
    RAISE NOTICE 'Tables created: conversations, messages, watermarks, deduplication_log';
    RAISE NOTICE 'Ready for data import.';
END $$;
```

---

## Migration Scripts

### JSON to PostgreSQL Migration

**File:** `scripts/database/migrate_json_to_postgresql.py`

```python
#!/usr/bin/env python3
"""
Migrate conversation deduplication data from JSON files to PostgreSQL.

Usage:
    python migrate_json_to_postgresql.py \
        --json-dir ./MEMORY-CONTEXT/dedup_state \
        --db-url postgresql://user:pass@localhost/dedup_db
"""

import json
import psycopg2
from pathlib import Path
import argparse
from datetime import datetime

class JSONToPostgreSQLMigrator:
    """Migrate JSON deduplication state to PostgreSQL."""

    def __init__(self, json_dir: str, db_url: str):
        self.json_dir = Path(json_dir)
        self.db_url = db_url
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to PostgreSQL database."""
        self.conn = psycopg2.connect(self.db_url)
        self.cursor = self.conn.cursor()
        print(f"✅ Connected to PostgreSQL database")

    def migrate_watermarks(self):
        """Migrate watermarks from JSON to PostgreSQL."""
        watermarks_file = self.json_dir / 'watermarks.json'

        if not watermarks_file.exists():
            print(f"⚠️  Watermarks file not found: {watermarks_file}")
            return

        with open(watermarks_file, 'r') as f:
            watermarks = json.load(f)

        print(f"\n📊 Migrating {len(watermarks)} watermarks...")

        for conversation_id, highest_index in watermarks.items():
            # Insert conversation if not exists
            self.cursor.execute("""
                INSERT INTO conversations (conversation_id, total_messages)
                VALUES (%s, %s)
                ON CONFLICT (conversation_id) DO NOTHING
            """, (conversation_id, highest_index + 1))

            # Insert watermark
            self.cursor.execute("""
                INSERT INTO watermarks (conversation_id, highest_index)
                VALUES (%s, %s)
                ON CONFLICT (conversation_id) DO UPDATE
                SET highest_index = EXCLUDED.highest_index,
                    last_updated = CURRENT_TIMESTAMP
            """, (conversation_id, highest_index))

            print(f"  ✅ {conversation_id}: watermark={highest_index}")

        self.conn.commit()
        print(f"✅ Migrated {len(watermarks)} watermarks")

    def migrate_content_hashes(self):
        """Migrate content hashes from JSON to PostgreSQL (metadata only)."""
        hashes_file = self.json_dir / 'content_hashes.json'

        if not hashes_file.exists():
            print(f"⚠️  Content hashes file not found: {hashes_file}")
            return

        with open(hashes_file, 'r') as f:
            hashes_data = json.load(f)

        print(f"\n📊 Content hashes for {len(hashes_data)} conversations")

        for conversation_id, hashes in hashes_data.items():
            print(f"  ✅ {conversation_id}: {len(hashes)} unique hashes")
            # Note: Hashes are already stored in messages table during log migration
            # This is just for verification

        print(f"✅ Content hashes verified (stored in messages table)")

    def migrate_conversation_log(self):
        """Migrate conversation log (JSONL) to PostgreSQL messages table."""
        log_file = self.json_dir / 'conversation_log.jsonl'

        if not log_file.exists():
            print(f"⚠️  Conversation log not found: {log_file}")
            return

        print(f"\n📊 Migrating conversation log...")

        messages_count = 0
        with open(log_file, 'r') as f:
            for line in f:
                event = json.loads(line)

                conversation_id = event['conversation_id']
                message = event['message']
                content_hash = event['content_hash']
                timestamp = event.get('timestamp', datetime.utcnow().isoformat())

                # Extract message fields
                message_index = message.get('index', 0)
                role = message.get('type', message.get('role', 'unknown'))
                content = json.dumps(message.get('message', message.get('content', '')))

                # Insert message
                self.cursor.execute("""
                    INSERT INTO messages (
                        conversation_id, message_index, content_hash,
                        role, content, created_at, metadata
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (conversation_id, message_index) DO NOTHING
                """, (
                    conversation_id, message_index, content_hash,
                    role, content, timestamp, json.dumps(message)
                ))

                messages_count += 1

                if messages_count % 100 == 0:
                    print(f"  ✅ Migrated {messages_count} messages...")
                    self.conn.commit()

        self.conn.commit()
        print(f"✅ Migrated {messages_count} messages from conversation log")

    def update_conversation_totals(self):
        """Update total_messages count for each conversation."""
        print(f"\n📊 Updating conversation totals...")

        self.cursor.execute("""
            UPDATE conversations c
            SET total_messages = (
                SELECT COUNT(*) FROM messages m
                WHERE m.conversation_id = c.conversation_id
            )
        """)

        self.conn.commit()
        print(f"✅ Updated conversation totals")

    def verify_migration(self):
        """Verify migration integrity."""
        print(f"\n🔍 Verifying migration integrity...")

        # Check conversations count
        self.cursor.execute("SELECT COUNT(*) FROM conversations")
        conv_count = self.cursor.fetchone()[0]
        print(f"  ✅ Conversations: {conv_count}")

        # Check messages count
        self.cursor.execute("SELECT COUNT(*) FROM messages")
        msg_count = self.cursor.fetchone()[0]
        print(f"  ✅ Messages: {msg_count}")

        # Check watermarks count
        self.cursor.execute("SELECT COUNT(*) FROM watermarks")
        watermark_count = self.cursor.fetchone()[0]
        print(f"  ✅ Watermarks: {watermark_count}")

        # Verify total_messages matches actual count
        self.cursor.execute("""
            SELECT c.conversation_id, c.total_messages, COUNT(m.message_id) as actual_count
            FROM conversations c
            LEFT JOIN messages m ON c.conversation_id = m.conversation_id
            GROUP BY c.conversation_id, c.total_messages
            HAVING c.total_messages != COUNT(m.message_id)
        """)

        mismatches = self.cursor.fetchall()
        if mismatches:
            print(f"  ⚠️  Total message count mismatches:")
            for row in mismatches:
                print(f"    {row[0]}: expected={row[1]}, actual={row[2]}")
        else:
            print(f"  ✅ All message counts match")

        print(f"\n✅ Migration verification complete!")

    def migrate(self):
        """Run complete migration."""
        try:
            self.connect()
            self.migrate_watermarks()
            self.migrate_content_hashes()
            self.migrate_conversation_log()
            self.update_conversation_totals()
            self.verify_migration()

            print(f"\n{'='*60}")
            print(f"✅ MIGRATION COMPLETE")
            print(f"{'='*60}")

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            if self.conn:
                self.conn.rollback()
            raise
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

def main():
    parser = argparse.ArgumentParser(description='Migrate JSON to PostgreSQL')
    parser.add_argument('--json-dir', required=True, help='Path to JSON state directory')
    parser.add_argument('--db-url', required=True, help='PostgreSQL connection URL')

    args = parser.parse_args()

    migrator = JSONToPostgreSQLMigrator(args.json_dir, args.db_url)
    migrator.migrate()

if __name__ == '__main__':
    main()
```

---

## Query Patterns

### Common Queries

**1. Get watermark for conversation:**
```sql
SELECT highest_index
FROM watermarks
WHERE conversation_id = 'rollout-master';
```

**2. Get all messages for conversation:**
```sql
SELECT message_index, role, content, created_at
FROM messages
WHERE conversation_id = 'rollout-master'
ORDER BY message_index ASC;
```

**3. Check if message already exists (by index):**
```sql
SELECT EXISTS (
    SELECT 1 FROM messages
    WHERE conversation_id = 'rollout-master'
      AND message_index = 25
);
```

**4. Check if content hash already exists:**
```sql
SELECT EXISTS (
    SELECT 1 FROM messages
    WHERE conversation_id = 'rollout-master'
      AND content_hash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
);
```

**5. Get deduplication statistics:**
```sql
SELECT
    conversation_id,
    SUM(messages_processed) as total_processed,
    SUM(duplicates_filtered) as total_duplicates,
    AVG(storage_savings_pct) as avg_savings_pct,
    AVG(processing_time_ms) as avg_processing_time_ms
FROM deduplication_log
GROUP BY conversation_id;
```

**6. Get latest N messages:**
```sql
SELECT message_index, role, content, created_at
FROM messages
WHERE conversation_id = 'rollout-master'
ORDER BY message_index DESC
LIMIT 10;
```

**7. Search messages by content (full-text):**
```sql
SELECT message_index, role, content
FROM messages
WHERE conversation_id = 'rollout-master'
  AND to_tsvector('english', content) @@ to_tsquery('english', 'deduplication & storage');
```

**8. Get conversation summary:**
```sql
SELECT
    c.conversation_id,
    c.total_messages,
    c.created_at,
    c.last_updated,
    w.highest_index,
    (SELECT COUNT(*) FROM deduplication_log WHERE conversation_id = c.conversation_id) as export_count
FROM conversations c
LEFT JOIN watermarks w ON c.conversation_id = w.conversation_id
WHERE c.conversation_id = 'rollout-master';
```

---

## Performance Tuning

### Query Performance Tips

1. **Use prepared statements** to avoid SQL injection and improve query planning:
```python
cursor.execute(
    "SELECT highest_index FROM watermarks WHERE conversation_id = %s",
    (conversation_id,)
)
```

2. **Batch inserts** for better performance:
```python
# Instead of inserting one message at a time
for message in messages:
    cursor.execute("INSERT INTO messages (...) VALUES (...)", (message,))

# Batch insert
execute_values(cursor,
    "INSERT INTO messages (conversation_id, message_index, ...) VALUES %s",
    [(msg['conv_id'], msg['index'], ...) for msg in messages]
)
```

3. **Use connection pooling:**
```python
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn='postgresql://user:pass@localhost/dedup_db'
)
```

4. **Analyze query plans:**
```sql
EXPLAIN ANALYZE
SELECT * FROM messages
WHERE conversation_id = 'rollout-master'
  AND message_index > 100
ORDER BY message_index;
```

5. **Vacuum regularly:**
```sql
-- Analyze tables to update statistics
ANALYZE conversations;
ANALYZE messages;
ANALYZE watermarks;

-- Vacuum to reclaim space
VACUUM FULL messages;
```

---

## Backup & Recovery

### Backup Strategy

**Daily Full Backup:**
```bash
# Backup entire database
pg_dump -h localhost -U dedup_user -F c -b -v -f dedup_db_backup_$(date +%Y%m%d).dump dedup_db

# Compress backup
gzip dedup_db_backup_$(date +%Y%m%d).dump

# Upload to S3 (optional)
aws s3 cp dedup_db_backup_$(date +%Y%m%d).dump.gz s3://backups/dedup/
```

**Continuous WAL Archiving:**
```sql
-- Enable WAL archiving in postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/wal_archive/%f'
```

**Restore from Backup:**
```bash
# Restore full backup
pg_restore -h localhost -U dedup_user -d dedup_db -v dedup_db_backup_20251117.dump

# Point-in-time recovery (PITR)
pg_restore -h localhost -U dedup_user -d dedup_db -v dedup_db_backup_20251117.dump --recovery-target-time='2025-11-17 12:00:00'
```

---

## Security

### Access Control

```sql
-- Create application role with limited privileges
CREATE ROLE dedup_app_role LOGIN PASSWORD 'secure_password';

-- Grant SELECT, INSERT, UPDATE on tables (no DELETE)
GRANT SELECT, INSERT, UPDATE ON conversations, messages, watermarks, deduplication_log TO dedup_app_role;

-- Grant sequence usage
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO dedup_app_role;

-- Deny DELETE privilege (append-only guarantee)
REVOKE DELETE ON messages FROM dedup_app_role;
```

### SSL/TLS Connections

```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='dedup_db',
    user='dedup_app_role',
    password='secure_password',
    sslmode='require',  # Require SSL connection
    sslcert='/path/to/client-cert.pem',
    sslkey='/path/to/client-key.pem',
    sslrootcert='/path/to/root-cert.pem'
)
```

---

## Partitioning Strategy

### Table Partitioning (For Large Scale)

For deployments with 1M+ messages, consider partitioning the `messages` table:

```sql
-- Partition by conversation_id (hash partitioning)
CREATE TABLE messages_partitioned (
    message_id BIGSERIAL,
    conversation_id VARCHAR(255) NOT NULL,
    message_index INTEGER NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    role VARCHAR(50),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    metadata JSONB,
    PRIMARY KEY (conversation_id, message_id),
    UNIQUE (conversation_id, message_index)
) PARTITION BY HASH (conversation_id);

-- Create 8 partitions
CREATE TABLE messages_p0 PARTITION OF messages_partitioned FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE messages_p1 PARTITION OF messages_partitioned FOR VALUES WITH (MODULUS 8, REMAINDER 1);
CREATE TABLE messages_p2 PARTITION OF messages_partitioned FOR VALUES WITH (MODULUS 8, REMAINDER 2);
CREATE TABLE messages_p3 PARTITION OF messages_partitioned FOR VALUES WITH (MODULUS 8, REMAINDER 3);
CREATE TABLE messages_p4 PARTITION OF messages_partitioned FOR VALUES WITH (MODULUS 8, REMAINDER 4);
CREATE TABLE messages_p5 PARTITION OF messages_partitioned FOR VALUES WITH (MODULUS 8, REMAINDER 5);
CREATE TABLE messages_p6 PARTITION OF messages_partitioned FOR VALUES WITH (MODULUS 8, REMAINDER 6);
CREATE TABLE messages_p7 PARTITION OF messages_partitioned FOR VALUES WITH (MODULUS 8, REMAINDER 7);
```

**Benefits:**
- Faster queries (smaller partitions to scan)
- Parallel query execution across partitions
- Easier maintenance (vacuum/analyze per partition)

---

## Appendix A: Sample Data

### Insert Sample Conversation

```sql
-- Insert conversation
INSERT INTO conversations (conversation_id, metadata) VALUES (
    'rollout-master',
    '{"project": "CODITECT Rollout Master", "tags": ["coditect", "master"]}'::JSONB
);

-- Insert watermark
INSERT INTO watermarks (conversation_id, highest_index) VALUES (
    'rollout-master',
    25
);

-- Insert sample messages
INSERT INTO messages (conversation_id, message_index, content_hash, role, content, metadata) VALUES
('rollout-master', 0, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'user', 'Hello, Claude', '{}'),
('rollout-master', 1, 'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a', 'assistant', 'Hello! How can I help you today?', '{}'),
('rollout-master', 2, '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca7', 'user', 'Create a new checkpoint', '{}');

-- Insert deduplication log entry
INSERT INTO deduplication_log (conversation_id, operation, messages_processed, duplicates_filtered, storage_savings_pct, processing_time_ms, metadata) VALUES (
    'rollout-master',
    'process_export',
    26,
    11,
    73.08,
    150,
    '{"export_file": "2025-11-17-EXPORT-ROLLOUT-MASTER.txt", "export_size_kb": 51}'::JSONB
);
```

---

## Appendix B: Database Configuration

### Recommended postgresql.conf Settings

```ini
# Connection Settings
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
work_mem = 4MB

# WAL Settings (for backups)
wal_level = replica
max_wal_size = 1GB
min_wal_size = 80MB
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/wal_archive/%f'

# Query Tuning
random_page_cost = 1.1  # For SSD storage
effective_io_concurrency = 200  # For SSD storage

# Logging
log_statement = 'mod'  # Log all data modifications
log_duration = on
log_min_duration_statement = 1000  # Log queries > 1s
```

---

**Document Status:** ✅ Database Design Complete
**Last Updated:** 2025-11-17
**Next Steps:** Create database schema, run migration
**Owner:** AZ1.AI CODITECT Team
# Conversation Export Deduplication - Implementation Plan

**Project:** Claude Conversation Export Deduplication System (Option B - Full Architecture)
**Timeline:** 2-3 weeks (320-480 engineering hours, 2 engineers)
**Status:** Ready for Implementation
**Date:** 2025-11-17

**Research Source:** `MEMORY-CONTEXT/RESEARCH-CLAUDE-CONVERSATION-EXPORT-DEDUPLICATION.md` (1,429 lines, 49KB)
**Review Guide:** `docs/DEDUPLICATION-RESEARCH-REVIEW-GUIDE.md`

---

## Executive Summary

### Problem Statement

Multi-day Claude sessions produce exponentially growing export files due to complete conversation history being included in each export:

**Observed Growth (Real Data):**
```
Export 1:  13KB (361 lines)        - Baseline
Export 2:  51KB (3.9x growth)      - Includes ALL of Export 1 + new content
Export 3: 439KB (33.7x growth!)    - Includes ALL previous + new content
```

**Result:** 95% data duplication, massive storage waste, difficulty extracting new content.

### Solution Overview

**Hybrid Deduplication Architecture** combining:
- **Sequence Watermarks** (Primary) - Track highest processed message index per conversation
- **Content Hashing** (Secondary) - SHA-256 deduplication for exact duplicates
- **Append-Only Log** (Persistence) - Zero catastrophic forgetting guarantee
- **PostgreSQL Backend** (Scalability) - Production-ready queryable storage

**Expected Outcomes:**
- ✅ **95% storage reduction** for multi-day sessions
- ✅ **Zero catastrophic forgetting** (all unique data preserved)
- ✅ **O(n) processing time**, O(k) space complexity
- ✅ **Production-ready** with monitoring and alerting

### Implementation Scope

**Phase 1: Core Implementation** (Week 1, 96-120 hours)
- ClaudeConversationDeduplicator class (Python)
- CLI tool for manual deduplication
- Comprehensive unit tests
- Integration with existing exports

**Phase 2: CODITECT Integration & PostgreSQL** (Week 2, 128-160 hours)
- Checkpoint automation integration
- SessionExportManager for MEMORY-CONTEXT
- PostgreSQL schema and migration
- Historical data processing

**Phase 3: Production Hardening** (Week 3, 96-120 hours)
- Gap detection and alerting
- Performance optimization
- Complete documentation
- Deployment automation

**Total Effort:** 320-400 engineering hours (2-3 weeks, 2 engineers)

---

## Decision Matrix (User Selections)

### 1. Storage Backend: **Option C - Hybrid** ✅ RECOMMENDED

**Rationale:**
- Start with JSON files (watermarks, hashes) for speed and simplicity
- Use PostgreSQL for append-only log (queryable, scalable)
- Migrate fully to PostgreSQL in Phase 2 after validation

**Benefits:**
- Fast MVP implementation (JSON files work immediately)
- Production scalability (PostgreSQL handles millions of messages)
- Smooth migration path (incremental adoption)

### 2. Session ID Strategy: **Option B - Auto-detect from Filename** ✅ RECOMMENDED

**Rationale:**
- Existing exports follow pattern: `YYYY-MM-DD-EXPORT-{project}.txt`
- Extract project name automatically: `2025-11-17-EXPORT-ROLLOUT-MASTER.txt` → `rollout-master`
- Manual override available via `--session-id` flag

**Implementation:**
```python
def detect_session_id(filename: str) -> str:
    """Auto-detect session ID from export filename."""
    # Pattern: YYYY-MM-DD-EXPORT-{project}.txt
    match = re.search(r'\d{4}-\d{2}-\d{2}-EXPORT-(.+)\.txt', filename)
    if match:
        return match.group(1).lower()
    # Fallback: Use filename stem
    return Path(filename).stem
```

### 3. Delta Encoding: **Option A - No Delta Encoding** ✅ RECOMMENDED

**Rationale:**
- Message-level deduplication already achieves 95% savings
- Delta encoding adds complexity for marginal 2-5% improvement
- Can be added later if needed (non-blocking enhancement)

### 4. Integration Points: **Option C - Both** ✅ RECOMMENDED

**Automated (Primary):**
- Integrate with `.coditect/scripts/create-checkpoint.py`
- Automatically deduplicate during checkpoint creation
- Transparent to user workflow

**Manual (Secondary):**
- CLI tool for ad-hoc deduplication
- Historical data migration
- Debugging and troubleshooting

### 5. Historical Data: **Option A - Process All** ✅ RECOMMENDED

**Rationale:**
- Only 4 existing export files (503KB total)
- Processing takes ~1-2 hours one-time effort
- Complete conversation history from day 1
- Validates deduplication effectiveness

**Files to Process:**
```
MEMORY-CONTEXT/
├── 2025-11-16-EXPORT-CHECKPOINT.txt (13KB)
├── 2025-11-16T1523-RESTORE-CONTEXT.txt (439KB)
├── 2025-11-17-EXPORT-MEMORY-CONTEXT-DOT-CODITECT.txt (51KB)
└── exports/2025-11-17-EXPORT-ROLLOUT-MASTER.txt (13KB)
```

---

## Phase 1: Core Implementation (Week 1)

**Duration:** 96-120 hours (2 engineers, 6-8 days)
**Goal:** Working deduplication system with CLI tool and tests
**Deliverables:** Python package, CLI, unit tests, integration tests

### 1.1 ClaudeConversationDeduplicator Class

**Owner:** Senior Python Developer
**Time:** 24-32 hours
**Priority:** P0

**Tasks:**

- [ ] **Setup project structure** (2 hours)
  - Create `scripts/deduplication/` directory
  - Initialize Python package (`__init__.py`, `setup.py`)
  - Configure logging and error handling
  - Setup virtual environment and dependencies

- [ ] **Implement core deduplicator class** (12-16 hours)
  - Adapt research code (Section 4.1) to production standards
  - Implement sequence watermark tracking
  - Implement content hash deduplication (SHA-256)
  - Create append-only log writer (JSONL format)
  - Add atomic file operations (write-to-temp, rename)
  - **Acceptance:** Deduplicate 2 exports, verify only new messages returned

- [ ] **Add state management** (4 hours)
  - Implement watermarks persistence (JSON)
  - Implement content hashes persistence (JSON)
  - Add state loading and saving with error recovery
  - Implement state validation and corruption detection
  - **Acceptance:** State survives process restart, corrupted state detected

- [ ] **Implement conversation reconstruction** (4 hours)
  - Add `get_full_conversation(conversation_id)` method
  - Read and parse append-only log
  - Sort messages by sequence number
  - **Acceptance:** Reconstruct full conversation from logs

- [ ] **Add statistics and reporting** (4 hours)
  - Implement `get_statistics(conversation_id)` method
  - Add deduplication metrics (watermark, unique messages, total)
  - Create storage efficiency calculator
  - **Acceptance:** Display meaningful stats for processed conversations

**Dependencies:** None
**Risk:** Low - Research code is production-ready, minimal adaptation needed

### 1.2 CLI Tool Development

**Owner:** Senior Python Developer
**Time:** 16-20 hours
**Priority:** P0

**Tasks:**

- [ ] **Create main CLI script** (4 hours)
  - Build `deduplicate_export.py` with argparse
  - Add command-line arguments (export file, session ID, output, stats)
  - Implement help text and usage examples
  - **Acceptance:** CLI runs with `--help` flag showing all options

- [ ] **Implement single file deduplication** (4 hours)
  - Load export file (JSON or TXT parsing)
  - Auto-detect or use provided session ID
  - Run deduplication via ClaudeConversationDeduplicator
  - Output new messages only (JSON or markdown)
  - **Acceptance:** Process 13KB export, output only new messages

- [ ] **Add batch processing mode** (4 hours)
  - Scan directory for multiple export files
  - Process all exports sequentially
  - Aggregate statistics across all files
  - **Acceptance:** Process all 4 historical exports in one command

- [ ] **Implement progress reporting** (4 hours)
  - Add progress bars for large exports (using `tqdm`)
  - Display real-time deduplication stats
  - Log warnings for anomalies (gaps, duplicate content)
  - **Acceptance:** Progress visible during processing, warnings logged

**Dependencies:** 1.1 (ClaudeConversationDeduplicator)
**Risk:** Low - Straightforward CLI wrapper around core class

### 1.3 Comprehensive Unit Tests

**Owner:** QA Engineer / Developer
**Time:** 20-24 hours
**Priority:** P0

**Tasks:**

- [ ] **Setup test framework** (4 hours)
  - Configure pytest with coverage reporting
  - Create test fixtures (sample exports, mock data)
  - Setup test data directory (`tests/fixtures/`)
  - **Acceptance:** Tests run with `pytest`, coverage report generated

- [ ] **Test deduplication logic** (8 hours)
  - Test with exact duplicates (100% overlap)
  - Test with partial duplicates (50% overlap)
  - Test with no duplicates (0% overlap)
  - Test with out-of-order messages
  - Test with gaps in sequence numbers
  - **Acceptance:** 90%+ code coverage, all edge cases handled

- [ ] **Test state persistence** (4 hours)
  - Test watermark save/load
  - Test content hash save/load
  - Test append-only log integrity
  - Test corruption recovery
  - **Acceptance:** State survives crashes, corrupted state detected

- [ ] **Test error handling** (4 hours)
  - Test with malformed export files
  - Test with missing fields (index, content, role)
  - Test with invalid session IDs
  - Test file system errors (permissions, disk full)
  - **Acceptance:** Graceful error messages, no crashes

**Dependencies:** 1.1, 1.2
**Risk:** Low - Standard testing practices

### 1.4 Integration Testing with Real Data

**Owner:** Developer + User
**Time:** 8-12 hours
**Priority:** P0

**Tasks:**

- [ ] **Test with 13KB export** (2 hours)
  - Run deduplication on `2025-11-16-EXPORT-CHECKPOINT.txt`
  - Verify all messages extracted as new (first run)
  - Verify 0 new messages on second run (idempotency)
  - **Acceptance:** 100% of messages marked as new, then 0% on re-run

- [ ] **Test with 51KB export** (2 hours)
  - Run on `2025-11-17-EXPORT-MEMORY-CONTEXT-DOT-CODITECT.txt`
  - Verify only new messages extracted (excludes 13KB duplicates)
  - Calculate deduplication percentage
  - **Acceptance:** ~25% new messages, 75% duplicates filtered

- [ ] **Test with 439KB export** (2 hours)
  - Run on `2025-11-16T1523-RESTORE-CONTEXT.txt`
  - Verify only new messages extracted (excludes all previous)
  - Calculate storage savings
  - **Acceptance:** ~95% storage reduction achieved

- [ ] **Test full conversation reconstruction** (2 hours)
  - Reconstruct complete conversation from logs
  - Verify message ordering (sequence numbers)
  - Verify no data loss (all unique messages present)
  - **Acceptance:** Full conversation matches original exports combined

**Dependencies:** 1.1, 1.2, 1.3
**Risk:** Medium - Depends on real export file format matching expectations

### 1.5 Documentation (Phase 1)

**Owner:** Technical Writer / Developer
**Time:** 12-16 hours
**Priority:** P1

**Tasks:**

- [ ] **Create README for deduplication module** (4 hours)
  - Overview and architecture
  - Installation instructions
  - Quick start guide
  - CLI usage examples
  - **Acceptance:** New users can install and run deduplication

- [ ] **Write API documentation** (4 hours)
  - Docstrings for all classes and methods
  - Generate HTML docs with Sphinx
  - Add code examples to docs
  - **Acceptance:** Complete API reference available

- [ ] **Create troubleshooting guide** (4 hours)
  - Common errors and solutions
  - Performance tuning tips
  - FAQ section
  - **Acceptance:** Users can self-serve common issues

**Dependencies:** 1.1, 1.2
**Risk:** Low

**Phase 1 Completion Criteria:**
- ✅ ClaudeConversationDeduplicator class fully implemented
- ✅ CLI tool works for single and batch processing
- ✅ 90%+ test coverage with all edge cases
- ✅ Successfully processes all 4 historical exports
- ✅ Documentation complete and published

**Phase 1 Checkpoint:** Run full deduplication on historical data, verify 95% storage reduction achieved.

---

## Phase 2: CODITECT Integration & PostgreSQL Migration (Week 2)

**Duration:** 128-160 hours (2 engineers, 8-10 days)
**Goal:** Production-ready integration with CODITECT, PostgreSQL backend
**Deliverables:** SessionExportManager, PostgreSQL schema, migration scripts, automated workflow

### 2.1 Checkpoint Automation Integration

**Owner:** CODITECT Framework Developer
**Time:** 16-20 hours
**Priority:** P0

**Tasks:**

- [ ] **Integrate with create-checkpoint.py** (8 hours)
  - Add deduplication step to checkpoint workflow
  - Call deduplication before creating checkpoint
  - Store deduplicated results in MEMORY-CONTEXT/sessions/
  - Update checkpoint document with deduplication stats
  - **Acceptance:** Checkpoints automatically deduplicate exports

- [ ] **Add export preparation integration** (4 hours)
  - Modify checkpoint script to prepare export location
  - Auto-detect session ID from checkpoint description
  - Link export to checkpoint document
  - **Acceptance:** Export location ready when checkpoint created

- [ ] **Test end-to-end checkpoint workflow** (4 hours)
  - Create checkpoint with deduplication enabled
  - Verify deduplicated data in MEMORY-CONTEXT/sessions/
  - Verify README.md updated with checkpoint
  - **Acceptance:** Full workflow works without manual intervention

**Dependencies:** Phase 1 complete
**Risk:** Low - Checkpoint script already modular

### 2.2 SessionExportManager Implementation

**Owner:** Senior Python Developer
**Time:** 24-32 hours
**Priority:** P0

**Tasks:**

- [ ] **Create SessionExportManager class** (12 hours)
  - Implement `import_export(export_file, session_id)` method
  - Auto-detect session ID from filename
  - Call ClaudeConversationDeduplicator
  - Save new messages to session markdown file
  - Return deduplication statistics
  - **Acceptance:** Import export, save only new messages to session file

- [ ] **Add session file formatting** (4 hours)
  - Format messages as markdown (user/assistant sections)
  - Add metadata headers (session ID, timestamp, stats)
  - Preserve code blocks and formatting
  - **Acceptance:** Session files are human-readable markdown

- [ ] **Implement session merging** (8 hours)
  - Merge multiple exports into single session file
  - Handle overlapping message sequences
  - Preserve chronological order
  - **Acceptance:** Multiple exports merge correctly into one session

- [ ] **Add session export API** (8 hours)
  - Export session to JSON (for programmatic access)
  - Export session to HTML (for web viewing)
  - Export statistics summary
  - **Acceptance:** Sessions exportable in multiple formats

**Dependencies:** Phase 1 complete
**Risk:** Low - Builds on proven deduplication logic

### 2.3 PostgreSQL Schema Design & Implementation

**Owner:** Database Architect + Backend Developer
**Time:** 32-40 hours
**Priority:** P0

**Tasks:**

- [ ] **Design PostgreSQL schema** (8 hours)
  - Design `conversations` table (conversation_id, metadata)
  - Design `messages` table (message_id, conversation_id, index, content_hash, content, timestamp)
  - Design `watermarks` table (conversation_id, highest_index, last_updated)
  - Design `deduplication_log` table (audit trail)
  - Add indexes for performance (conversation_id, index, content_hash)
  - **Acceptance:** Complete schema DDL ready (see DATABASE-DESIGN.md)

- [ ] **Implement PostgreSQL backend** (12 hours)
  - Create `PostgreSQLDeduplicator` class (inherits from base)
  - Implement watermark tracking in PostgreSQL
  - Implement content hash storage in PostgreSQL
  - Implement append-only log in `messages` table
  - Add connection pooling (psycopg2-pool)
  - **Acceptance:** Deduplication works with PostgreSQL backend

- [ ] **Create migration scripts** (8 hours)
  - Write JSON → PostgreSQL migration script
  - Migrate watermarks from JSON files
  - Migrate content hashes from JSON files
  - Migrate append-only log from JSONL to PostgreSQL
  - Verify data integrity post-migration
  - **Acceptance:** Historical data migrated to PostgreSQL successfully

- [ ] **Add PostgreSQL configuration** (4 hours)
  - Create database connection config (environment variables)
  - Add database initialization scripts (schema creation)
  - Configure connection pooling and timeouts
  - **Acceptance:** Database connects and initializes automatically

**Dependencies:** Phase 1 complete
**Risk:** Medium - Requires PostgreSQL setup and configuration

### 2.4 Historical Data Processing

**Owner:** Data Engineer / Developer
**Time:** 12-16 hours
**Priority:** P1

**Tasks:**

- [ ] **Process 4 existing exports** (4 hours)
  - Run batch deduplication on all historical files
  - Import deduplicated data into PostgreSQL
  - Generate deduplication statistics report
  - **Acceptance:** All historical data processed, stats verified

- [ ] **Validate data integrity** (4 hours)
  - Reconstruct full conversations from database
  - Compare with original exports
  - Verify no data loss or corruption
  - **Acceptance:** 100% data integrity verified

- [ ] **Generate migration report** (4 hours)
  - Document storage savings (before/after)
  - Document deduplication percentages per export
  - Document processing time and performance
  - **Acceptance:** Migration report published

**Dependencies:** 2.3 (PostgreSQL setup)
**Risk:** Low - Well-defined data processing task

### 2.5 Monitoring & Statistics

**Owner:** DevOps Engineer
**Time:** 16-20 hours
**Priority:** P1

**Tasks:**

- [ ] **Add deduplication metrics** (8 hours)
  - Track total messages processed
  - Track duplicates filtered
  - Track storage savings (bytes)
  - Track processing time per export
  - **Acceptance:** Metrics logged and queryable

- [ ] **Create statistics dashboard** (8 hours)
  - Build web dashboard (Flask/Dash) for stats visualization
  - Display deduplication trends over time
  - Show storage savings graphs
  - Show conversation growth charts
  - **Acceptance:** Dashboard accessible and displays real-time stats

**Dependencies:** 2.3 (PostgreSQL)
**Risk:** Low - Standard monitoring implementation

**Phase 2 Completion Criteria:**
- ✅ SessionExportManager integrated with CODITECT
- ✅ PostgreSQL backend fully operational
- ✅ All historical data migrated to PostgreSQL
- ✅ Checkpoint automation includes deduplication
- ✅ Monitoring and statistics operational

**Phase 2 Checkpoint:** Create checkpoint with automated deduplication, verify seamless integration.

---

## Phase 3: Production Hardening (Week 3)

**Duration:** 96-120 hours (2 engineers, 6-8 days)
**Goal:** Production-ready system with monitoring, alerting, optimization
**Deliverables:** Gap detection, performance tuning, complete docs, deployment automation

### 3.1 Gap Detection & Alerting

**Owner:** Backend Developer
**Time:** 16-20 hours
**Priority:** P0

**Tasks:**

- [ ] **Implement gap detection** (8 hours)
  - Detect missing message sequences
  - Identify time gaps between exports
  - Flag conversations with data loss risk
  - **Acceptance:** Gaps detected and logged

- [ ] **Add alerting system** (8 hours)
  - Email alerts for detected gaps
  - Slack notifications for critical issues
  - Alert dashboard (integrate with monitoring)
  - **Acceptance:** Alerts delivered within 5 minutes of detection

**Dependencies:** Phase 2 complete
**Risk:** Low

### 3.2 Semantic Deduplication (Optional Enhancement)

**Owner:** ML Engineer / Developer
**Time:** 20-24 hours
**Priority:** P2 (Optional)

**Tasks:**

- [ ] **Research embedding models** (4 hours)
  - Evaluate sentence-transformers (SBERT)
  - Test OpenAI embeddings API
  - Benchmark similarity detection accuracy
  - **Acceptance:** Model selected with 90%+ accuracy on test data

- [ ] **Implement semantic similarity** (12 hours)
  - Integrate embedding model
  - Calculate cosine similarity between messages
  - Add fuzzy matching threshold (configurable)
  - **Acceptance:** Near-duplicate messages detected and filtered

- [ ] **Add semantic deduplication mode** (4 hours)
  - CLI flag `--semantic` to enable
  - Configure similarity threshold
  - Report semantic duplicates separately
  - **Acceptance:** Semantic mode reduces storage by additional 2-5%

**Dependencies:** Phase 2 complete
**Risk:** Medium - ML model integration complexity
**Note:** This is an optional enhancement, can be deferred to Phase 4

### 3.3 Performance Optimization

**Owner:** Performance Engineer / Senior Developer
**Time:** 20-24 hours
**Priority:** P1

**Tasks:**

- [ ] **Benchmark current performance** (4 hours)
  - Measure processing time for various export sizes
  - Profile CPU and memory usage
  - Identify bottlenecks (I/O, hashing, database)
  - **Acceptance:** Performance baseline established

- [ ] **Optimize database queries** (8 hours)
  - Add database indexes (conversation_id, index, content_hash)
  - Implement batch inserts for append-only log
  - Use connection pooling
  - **Acceptance:** 50% reduction in database query time

- [ ] **Implement streaming processing** (8 hours)
  - Process large exports line-by-line (avoid loading entire file)
  - Yield results incrementally
  - Add progress reporting for long-running operations
  - **Acceptance:** Process 10MB+ exports without memory issues

**Dependencies:** Phase 2 complete
**Risk:** Low - Standard optimization techniques

### 3.4 Complete Documentation

**Owner:** Technical Writer
**Time:** 24-32 hours
**Priority:** P0

**Tasks:**

- [ ] **Write architecture documentation** (8 hours)
  - Complete `CONVERSATION-DEDUPLICATION-ARCHITECTURE.md`
  - Add C4 diagrams (context, container, component)
  - Document data flow and integration points
  - **Acceptance:** Architecture fully documented with diagrams

- [ ] **Write database documentation** (8 hours)
  - Complete `CONVERSATION-DEDUPLICATION-DATABASE-DESIGN.md`
  - Document schema with ERD diagrams
  - Add migration guides
  - Document backup and recovery procedures
  - **Acceptance:** Database design fully documented

- [ ] **Write user guide** (8 hours)
  - Installation and setup instructions
  - Usage examples for all CLI commands
  - Integration guide for CODITECT
  - Troubleshooting section
  - **Acceptance:** Users can self-onboard without support

**Dependencies:** All previous tasks
**Risk:** Low

### 3.5 Deployment Automation

**Owner:** DevOps Engineer
**Time:** 16-20 hours
**Priority:** P1

**Tasks:**

- [ ] **Create Docker container** (8 hours)
  - Write Dockerfile for deduplication service
  - Include PostgreSQL client libraries
  - Add entrypoint script for initialization
  - **Acceptance:** Service runs in Docker container

- [ ] **Setup CI/CD pipeline** (8 hours)
  - Configure GitHub Actions for automated testing
  - Add deployment to staging/production
  - Automated database migrations on deploy
  - **Acceptance:** Code pushes trigger automated tests and deployment

**Dependencies:** Phase 2 complete
**Risk:** Low - Standard DevOps practices

**Phase 3 Completion Criteria:**
- ✅ Gap detection and alerting operational
- ✅ Performance optimized (50%+ speedup)
- ✅ Complete documentation published
- ✅ Deployment automation configured
- ✅ (Optional) Semantic deduplication implemented

**Phase 3 Checkpoint:** Full production deployment, monitoring all green.

---

## Testing Strategy

### Unit Tests
- **Coverage Target:** 90%+
- **Framework:** pytest
- **Focus:** Deduplication logic, state management, error handling

### Integration Tests
- **Coverage:** End-to-end workflows
- **Focus:** CLI tool, SessionExportManager, checkpoint integration
- **Data:** Real historical exports

### Performance Tests
- **Benchmarks:** Processing time, memory usage, database query performance
- **Load Testing:** 1,000+ messages, 10MB+ exports

### Regression Tests
- **Automated:** Run on every commit via CI/CD
- **Dataset:** Historical exports as test fixtures

---

## Risk Management

### Risk 1: Export Format Changes
**Probability:** Low
**Impact:** High
**Mitigation:**
- Support multiple export formats (JSON, TXT, API responses)
- Add format detection and validation
- Fail gracefully with clear error messages

### Risk 2: PostgreSQL Setup Complexity
**Probability:** Medium
**Impact:** Medium
**Mitigation:**
- Provide Docker Compose for local development
- Document database setup step-by-step
- Support JSON files as fallback (Phase 1)

### Risk 3: Data Loss During Migration
**Probability:** Low
**Impact:** Critical
**Mitigation:**
- Backup all JSON files before migration
- Validate data integrity post-migration
- Keep JSON files for 30 days post-migration

### Risk 4: Performance Degradation at Scale
**Probability:** Medium
**Impact:** Medium
**Mitigation:**
- Benchmark with large datasets (1,000+ messages)
- Implement database indexing and query optimization
- Add streaming processing for large exports

---

## Success Metrics

### Quantitative Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Storage Reduction** | 95% | Compare raw exports vs deduplicated storage |
| **Processing Speed** | <5s per 100KB | Time to process exports |
| **Test Coverage** | 90%+ | pytest coverage report |
| **Zero Data Loss** | 100% integrity | Reconstruction validation |
| **Deduplication Accuracy** | 99%+ | Manual verification sample |

### Qualitative Metrics

- ✅ User can run deduplication without manual intervention
- ✅ Checkpoints automatically include deduplicated exports
- ✅ Developers can query conversation history via PostgreSQL
- ✅ System recovers gracefully from errors
- ✅ Documentation is complete and accessible

---

## Timeline & Milestones

### Week 1: Core Implementation
- **Days 1-2:** ClaudeConversationDeduplicator class
- **Days 3-4:** CLI tool and tests
- **Days 5-6:** Integration testing with real data
- **Milestone:** Working deduplication system

### Week 2: CODITECT Integration & PostgreSQL
- **Days 7-8:** Checkpoint integration, SessionExportManager
- **Days 9-11:** PostgreSQL schema, migration, testing
- **Days 12-13:** Historical data processing, monitoring
- **Milestone:** Production-ready PostgreSQL backend

### Week 3: Production Hardening
- **Days 14-15:** Gap detection, alerting
- **Days 16-17:** Performance optimization
- **Days 18-19:** Documentation completion
- **Days 20-21:** Deployment automation, final testing
- **Milestone:** Production deployment

---

## Resource Requirements

### Personnel
- **2 Senior Python Developers** (full-time, 3 weeks)
- **1 Database Architect** (part-time, Week 2)
- **1 DevOps Engineer** (part-time, Week 3)
- **1 Technical Writer** (part-time, Weeks 1-3)

### Infrastructure
- **Development:**
  - PostgreSQL 14+ (local Docker)
  - Python 3.9+ virtual environments
  - Git repository access

- **Production:**
  - PostgreSQL 14+ (managed service recommended)
  - 2 CPU, 4GB RAM minimum
  - 50GB storage (grows with conversations)

### Budget Estimate
- **Engineering:** $30,000 - $40,000 (320-400 hours @ $100/hr)
- **Infrastructure:** $50 - $100/month (PostgreSQL managed service)
- **Tools/Licenses:** $0 (all open-source)

**Total:** $30,000 - $40,000 one-time + $50-100/month ongoing

---

## Next Steps

### Immediate (This Week)
1. ✅ Review and approve this implementation plan
2. ⏸️ Allocate 2 senior developers for 3-week sprint
3. ⏸️ Setup development environment (PostgreSQL, Python)
4. ⏸️ Create GitHub project with milestones

### Week 1 Kickoff
1. ⏸️ Begin Phase 1 implementation
2. ⏸️ Daily standups for progress tracking
3. ⏸️ First checkpoint: Deduplicator class working

### Week 2-3
1. ⏸️ Follow phase-by-phase execution
2. ⏸️ Weekly demo to stakeholders
3. ⏸️ Final checkpoint: Production deployment

---

## Appendix A: Related Documents

- **Research:** `MEMORY-CONTEXT/RESEARCH-CLAUDE-CONVERSATION-EXPORT-DEDUPLICATION.md`
- **Review Guide:** `docs/DEDUPLICATION-RESEARCH-REVIEW-GUIDE.md`
- **Architecture:** `docs/CONVERSATION-DEDUPLICATION-ARCHITECTURE.md` (to be created)
- **Database Design:** `docs/CONVERSATION-DEDUPLICATION-DATABASE-DESIGN.md` (to be created)
- **Task List:** `MEMORY-CONTEXT/TASKLIST-CONVERSATION-DEDUPLICATION.md` (to be created)

---

## Appendix B: Stakeholder Communication

### Weekly Status Report Template

**Week X Status Report: Conversation Deduplication Implementation**

**Progress This Week:**
- [List completed tasks]
- [Show metrics: lines of code, tests written, coverage %]

**Blockers:**
- [List any blockers requiring stakeholder intervention]

**Next Week:**
- [Preview upcoming tasks]

**Risks/Changes:**
- [Any new risks or scope changes]

**Demo:** [Link to working demo/screenshots]

---

**Document Status:** ✅ Ready for Implementation
**Last Updated:** 2025-11-17
**Next Review:** Start of Phase 1 (Week 1 kickoff)
**Owner:** AZ1.AI CODITECT Team
# Conversation Export Deduplication - Research Review Guide

**Purpose:** Guide stakeholder review of deduplication research and facilitate decision-making for full architecture implementation.

**Research Document:** `MEMORY-CONTEXT/RESEARCH-CLAUDE-CONVERSATION-EXPORT-DEDUPLICATION.md` (1,429 lines, 49KB)

**Review Time:** 30-45 minutes for executive summary + key sections, 2-3 hours for complete deep dive

---

## 📊 Executive Overview

### The Problem (Confirmed in Your Data)

**Your MEMORY-CONTEXT exports show exponential growth:**
```
   13KB - 2025-11-17-EXPORT-ROLLOUT-MASTER.txt (361 lines)
   51KB - 2025-11-17-EXPORT-MEMORY-CONTEXT-DOT-CODITECT.txt (3.9x larger)
  439KB - 2025-11-16T1523-RESTORE-CONTEXT.txt (33.7x larger!)
```

**Root Cause:** Multi-day Claude sessions where `/export` creates files containing:
- ALL previous conversation turns from session start
- PLUS new conversation turns since last export
- Result: Massive overlap between consecutive exports

### The Solution (Research-Backed)

**Hybrid Deduplication Strategy** combining:
1. **Sequence Number Watermarks** (Primary) - Track highest processed message index
2. **Content Hashing** (Secondary) - SHA-256 deduplication for exact duplicates
3. **Append-Only Log** (Persistence) - Zero catastrophic forgetting guarantee
4. **Idempotent Processing** (Safety) - Safe to reprocess same export multiple times

**Expected Results:**
- ✅ **~95% storage reduction** for repeated exports
- ✅ **Zero catastrophic forgetting** (all unique data preserved)
- ✅ **O(n) processing time**, O(k) space (k = unique messages)
- ✅ **Production-ready** with complete working implementation

---

## 📖 Document Structure (1,429 Lines)

### Section 1: Anthropic Claude Conversation Export Format (Lines 20-165)

**What You'll Learn:**
- Official Claude export capabilities (limited documentation)
- Claude API message structure (stateless, requires full history)
- Third-party export formats (reverse-engineered)
- Claude Code session storage patterns

**Key Finding:**
```json
// Third-party export format (most common)
{
  "exported_at": "2025-11-17T10:30:00Z",
  "title": "Conversation Title",
  "messages": [
    {
      "index": 0,                    // Sequential position (0-based)
      "type": "prompt",              // "prompt" (user) or "response" (assistant)
      "message": [...]               // Array of content blocks
    }
  ]
}
```

**Critical Limitation:** No unique message IDs, no timestamps - must use `index` for sequencing.

**Review Focus:**
- [ ] Understand export format structure (pages 1-4)
- [ ] Note lack of unique identifiers (implications for deduplication)
- [ ] Review Claude Code's existing incremental update pattern (BashOutput position tracking)

---

### Section 2: Conversation Data Deduplication Strategies (Lines 166-533)

**What You'll Learn:**
- Content-Addressable Storage (Git model)
- Sequence Number Tracking (Kafka watermarks)
- Event Sourcing Patterns
- Idempotent Processing
- Temporal Deduplication Windows

**Key Strategies Compared:**

| Strategy | Pros | Cons | Our Use |
|----------|------|------|---------|
| **Content Hashing** | Exact duplicate detection, proven (Git) | Misses near-duplicates | ✅ Secondary |
| **Sequence Numbers** | O(1) space, fast, simple | Requires sequential indices | ✅ Primary |
| **Event Sourcing** | Complete audit trail, reconstruction | Storage overhead | ✅ Append-only log |
| **Fuzzy Matching** | Near-duplicate detection | CPU intensive, false positives | ⚠️ Optional |
| **Temporal Windows** | Time-based dedup | Requires timestamps (we don't have) | ❌ Not applicable |

**Code Examples Provided:**
- Git-style content hashing (lines 186-220)
- Kafka-style watermark tracking (lines 222-280)
- Event sourcing append-only log (lines 282-345)
- Idempotent message processing (lines 347-410)

**Review Focus:**
- [ ] Compare strategy trade-offs (table above)
- [ ] Understand why sequence numbers are primary (we have indices)
- [ ] Review content hashing for safety net (catch duplicates)
- [ ] Examine event sourcing for zero forgetting guarantee

---

### Section 3: Incremental Storage and Delta Encoding (Lines 534-736)

**What You'll Learn:**
- Delta compression for similar content
- Snapshot + delta strategies
- Block-level deduplication
- JSON-delta algorithms

**Key Techniques:**

**Delta Encoding (bsdiff algorithm):**
```python
# Store only differences between versions
delta = bsdiff.diff(old_export_bytes, new_export_bytes)
# Reconstruction: new_export = bspatch.patch(old_export, delta)
```

**Snapshot + Delta Pattern:**
```
Export 1 (13KB):   [Full snapshot]
Export 2 (51KB):   [Delta from Export 1] = ~5KB stored
Export 3 (439KB):  [Delta from Export 2] = ~10KB stored

Total storage: 13KB + 5KB + 10KB = 28KB (vs 503KB raw)
Storage savings: 94.4%
```

**JSON-Delta (RFC 6902):**
```json
// Instead of storing full exports, store patches
[
  {"op": "add", "path": "/messages/10", "value": {...}},
  {"op": "add", "path": "/messages/11", "value": {...}}
]
```

**Review Focus:**
- [ ] Understand delta encoding potential (94%+ savings)
- [ ] Evaluate complexity vs benefit trade-off
- [ ] Consider snapshot frequency (e.g., daily full + hourly deltas)
- [ ] Review JSON-delta for structured data efficiency

**Decision Point:** Do we need delta encoding, or is message-level deduplication sufficient?

---

### Section 4: Recommended Implementation (Lines 737-1001) ⭐ MOST IMPORTANT

**What You'll Get:**
- Complete working Python implementation (~200 lines)
- Usage examples with real data
- Key features and guarantees
- Advanced features (gap detection, semantic deduplication)

**The ClaudeConversationDeduplicator Class:**

```python
class ClaudeConversationDeduplicator:
    """
    Hybrid deduplication for Claude conversation exports.

    Storage:
        - watermarks.json: {conversation_id: highest_index}
        - content_hashes.json: {conversation_id: [hash1, hash2, ...]}
        - conversation_log.jsonl: Append-only log of all messages

    Methods:
        - process_export(conversation_id, export_data) → new_messages
        - get_full_conversation(conversation_id) → all_messages
        - get_statistics(conversation_id) → {watermark, unique_messages, total}
    """
```

**Usage Example (Lines 894-934):**
```python
# Process first export
export_1 = {'messages': [{'index': 0, ...}, {'index': 1, ...}]}
new_msgs_1 = dedup.process_export('session-abc', export_1)
# Result: 2 new messages

# Process second export (with duplicates)
export_2 = {'messages': [
    {'index': 0, ...},  # Duplicate
    {'index': 1, ...},  # Duplicate
    {'index': 2, ...},  # NEW
    {'index': 3, ...}   # NEW
]}
new_msgs_2 = dedup.process_export('session-abc', export_2)
# Result: 2 new messages (duplicates filtered)

# Reconstruct full conversation
full = dedup.get_full_conversation('session-abc')
# Result: 4 unique messages
```

**Guarantees:**
- ✅ **Zero Catastrophic Forgetting:** Append-only log preserves all unique messages
- ✅ **Efficiency:** O(n) time, O(k) space (k = unique messages per conversation)
- ✅ **Robustness:** Idempotent processing, crash recovery, gap detection
- ✅ **Works Without IDs:** Handles missing message IDs/timestamps gracefully

**Review Focus:**
- [ ] Study the implementation (lines 743-892) - THIS IS READY TO USE
- [ ] Run through usage example mentally with your data
- [ ] Understand guarantees and trade-offs
- [ ] Review gap detection (lines 956-976) for missing messages
- [ ] Consider semantic deduplication (lines 978-998) for near-duplicates

---

### Section 5: Implementation Recommendations (Lines 1002-1181) ⭐ ARCHITECTURE

**What You'll Learn:**
- Production architecture diagram
- CODITECT framework integration
- CLI tool design
- Automated processing workflows

**Production Architecture:**
```
┌─────────────────────────────────────────────────┐
│ Claude Export Deduplication System              │
├─────────────────────────────────────────────────┤
│  Export Files (JSON) ──▶ Deduplication Processor│
│                          ├─ Sequence tracking   │
│                          ├─ Content hashing     │
│                          └─ Idempotent processing│
│                                    │             │
│                         ┌──────────▼──────────┐ │
│                         │ Persistent Storage   │ │
│                         │  - Watermarks (JSON) │ │
│                         │  - Hashes (JSON)     │ │
│                         │  - Append-only log   │ │
│                         └──────────────────────┘ │
│                                                   │
│  Outputs: New messages, Full reconstruction,     │
│           Statistics, Gap detection              │
└─────────────────────────────────────────────────┘
```

**CODITECT Integration (Lines 1036-1089):**
```python
class SessionExportManager:
    """Manage Claude session exports with deduplication"""

    def __init__(self, project_root):
        self.memory_context_dir = project_root / 'MEMORY-CONTEXT'
        self.dedup = ClaudeConversationDeduplicator(
            storage_dir=self.memory_context_dir / 'dedup_state'
        )

    def import_export(self, export_file, session_id=None):
        """Import Claude export, deduplicating automatically"""
        # Auto-detect session ID
        # Deduplicate
        # Save new messages to session file
        return {
            'total_messages': X,
            'new_messages': Y,
            'duplicates_filtered': X - Y
        }
```

**CLI Tool (Lines 1091-1150):**
```bash
# Manual deduplication
python deduplicate_export.py export.json --session-id abc123 --stats

# Batch processing
python batch_deduplicate.py MEMORY-CONTEXT/exports/ --output-dir sessions/

# Statistics
python dedup_stats.py --session-id abc123
```

**Review Focus:**
- [ ] Evaluate architecture diagram for completeness
- [ ] Review CODITECT integration approach
- [ ] Assess CLI tool requirements
- [ ] Consider automation opportunities

---

### Section 6: Best Practices Summary (Lines 1182-1264)

**Quick Reference Checklist:**

**Design Principles:**
- [ ] Use content hashing for exact deduplication
- [ ] Track sequence numbers/watermarks for efficiency
- [ ] Implement append-only logs for auditability
- [ ] Design for idempotent processing
- [ ] Add comprehensive error handling

**Storage Optimization:**
- [ ] Normalize message content before hashing
- [ ] Use atomic file operations (write to temp, rename)
- [ ] Implement periodic compaction of append-only logs
- [ ] Consider tiered storage (hot/warm/cold)

**Operational Excellence:**
- [ ] Monitor deduplication ratios (should be 90%+ for multi-day sessions)
- [ ] Alert on anomalies (gaps, duplicate content at new indices)
- [ ] Regular backups of watermarks and hashes
- [ ] Test disaster recovery procedures

**Review Focus:**
- [ ] Use as implementation checklist
- [ ] Identify gaps in current plan
- [ ] Note monitoring requirements

---

### Section 7: Gaps and Future Research (Lines 1265-1304)

**Known Limitations:**

1. **No Semantic Search Yet**
   - Current: Exact match deduplication only
   - Future: Semantic similarity for near-duplicates
   - Requires: Embedding model integration

2. **Manual Session ID Assignment**
   - Current: User must provide session ID
   - Future: Auto-detect from conversation content or file patterns
   - Requires: Heuristics or ML-based classification

3. **No Cross-Conversation Analysis**
   - Current: Each conversation isolated
   - Future: Detect reused content across conversations
   - Requires: Global content hash index

4. **Limited Format Support**
   - Current: Assumes third-party JSON format
   - Future: Support official Claude exports, API responses, etc.
   - Requires: Format detection and normalization layer

**Review Focus:**
- [ ] Understand current limitations
- [ ] Prioritize future enhancements
- [ ] Note dependencies for roadmap

---

### Section 8: Conclusion (Lines 1305-1370)

**Key Takeaways:**

1. **Problem is Solvable:** Proven patterns from distributed systems apply directly
2. **Implementation Ready:** Complete working code provided
3. **Zero Forgetting Achievable:** Append-only log + idempotent processing = guarantee
4. **High ROI:** 95% storage reduction, minimal complexity

**Recommended Next Steps:**
1. ✅ Implement core deduplicator (Section 4.1 code)
2. ✅ Test with your 13KB, 51KB, 439KB exports
3. ✅ Integrate with checkpoint automation
4. ✅ Extend to PostgreSQL for scalability
5. ✅ Add monitoring and alerting

---

### Section 9: References (Lines 1371-1414)

**40+ Authoritative Sources:**
- Anthropic Claude documentation
- Git internals and content-addressable storage
- Apache Kafka (sequence numbers, watermarks)
- Event sourcing patterns (Martin Fowler)
- Distributed systems deduplication (Google, AWS)
- Delta encoding algorithms (bsdiff, xdelta, JSON-delta)

**Review Focus:**
- [ ] Validate research quality (authoritative sources)
- [ ] Note relevant deep dives for specific topics

---

### Appendix A: Complete Working Implementation (Lines 1415-1429)

**Full code ready to copy-paste:**
- ClaudeConversationDeduplicator class
- SessionExportManager integration
- CLI tool wrapper
- Unit test examples

---

## 🎯 Key Decision Points for Review

Before proceeding to Option B (Full Architecture), decide on:

### 1. Storage Backend

**Option A: JSON Files (Recommended for MVP)**
- ✅ Simple, no dependencies
- ✅ Works immediately
- ❌ Limited scalability (hundreds of conversations OK, thousands not)
- **Use for:** Quick implementation, proof of concept

**Option B: PostgreSQL (Recommended for Production)**
- ✅ Scalable to millions of messages
- ✅ ACID guarantees
- ✅ Rich querying capabilities
- ❌ Requires database setup
- **Use for:** Long-term solution, multiple users

**Option C: Hybrid (Recommended Overall)**
- Start with JSON files for watermarks/hashes (fast reads)
- Use PostgreSQL for append-only log (queryable history)
- Migrate to full PostgreSQL later if needed

**❓ Decision:** Which storage backend do you prefer for Phase 1?

---

### 2. Session ID Strategy

**Option A: Manual (Simplest)**
- User provides session ID when running deduplication
- Example: `deduplicate_export.py export.json --session-id 2025-11-17-project-X`

**Option B: Auto-detect from Filename**
- Parse session ID from export filename
- Example: `2025-11-17-EXPORT-ROLLOUT-MASTER.txt` → `rollout-master`

**Option C: Auto-detect from Content**
- Extract conversation title or project name from export content
- Requires parsing export file first

**❓ Decision:** How should session IDs be determined?

---

### 3. Delta Encoding

**Option A: No Delta Encoding (Recommended)**
- Message-level deduplication is sufficient
- Simpler implementation
- Still achieves 95% savings

**Option B: Add Delta Encoding**
- Additional 2-5% savings (marginal improvement)
- Significant complexity increase
- Worth it only for very large exports (multi-MB)

**❓ Decision:** Is delta encoding needed for your use case?

---

### 4. Integration Points

**Where should deduplication run?**

**Option A: Manual CLI Tool**
- Run manually: `python deduplicate_export.py export.txt`
- User controls when/what to deduplicate
- Good for testing and ad-hoc processing

**Option B: Checkpoint Automation**
- Automatically deduplicate during checkpoint creation
- Transparent to user
- Integrates with existing workflow

**Option C: Both**
- Automated for routine checkpoints
- Manual tool for historical data migration

**❓ Decision:** Which integration approach?

---

### 5. Historical Data Migration

**You have existing exports with duplicates:**
```
MEMORY-CONTEXT/
├── 2025-11-16-EXPORT-CHECKPOINT.txt (13KB)
├── 2025-11-16T1523-RESTORE-CONTEXT.txt (439KB)
├── 2025-11-17-EXPORT-MEMORY-CONTEXT-DOT-CODITECT.txt (51KB)
└── exports/2025-11-17-EXPORT-ROLLOUT-MASTER.txt (13KB)
```

**Option A: Process All Historical Exports**
- Run deduplication on all existing files
- Build complete conversation history from day 1
- Time investment: 1-2 hours

**Option B: Start Fresh**
- Only deduplicate new exports going forward
- Keep historical exports as-is
- Faster to implement

**❓ Decision:** Process historical data or start fresh?

---

## ✅ Review Checklist

Before proceeding to Option B implementation, confirm:

- [ ] **Section 4 reviewed:** Understand the core implementation
- [ ] **Section 5 reviewed:** Understand integration architecture
- [ ] **Decision 1 made:** Storage backend (JSON/PostgreSQL/Hybrid)
- [ ] **Decision 2 made:** Session ID strategy (Manual/Auto-filename/Auto-content)
- [ ] **Decision 3 made:** Delta encoding needed? (Yes/No)
- [ ] **Decision 4 made:** Integration points (Manual/Automated/Both)
- [ ] **Decision 5 made:** Historical data migration (Yes/No)

**Once checklist complete:** Ready for Option B detailed implementation plan

---

## 📋 Next: Option B Implementation Plan Preview

**Phase 1: Core Implementation** (Week 1, 16-20 hours)
- Implement ClaudeConversationDeduplicator
- Create CLI tool
- Write unit tests
- Test with your existing exports

**Phase 2: CODITECT Integration** (Week 2, 16-20 hours)
- Integrate with checkpoint automation
- Add SessionExportManager
- Migrate to PostgreSQL (if chosen)
- Process historical data (if chosen)

**Phase 3: Production Hardening** (Week 3, 12-16 hours)
- Add monitoring and alerting
- Implement gap detection
- Create documentation
- Performance optimization

**Total Effort:** 44-56 engineering hours (2-3 weeks for 1 engineer, 1-1.5 weeks for 2 engineers)

---

**Ready to proceed with Option B detailed plan?** Let me know your decisions on the 5 decision points above, and I'll create the comprehensive implementation plan with tasks, code, and deliverables.
# Export-Dedup Prominent Metrics Display

**Date:** November 22, 2025
**Status:** ✅ Complete and Tested
**Enhancement:** Prominently display new unique messages count

## Overview

The `/export-dedup` command now **always displays the exact count of new unique messages** that were added and backed up, using prominent visual formatting to ensure you never miss this critical metric.

## What You See

After running `/export-dedup`, you'll see this prominent section:

```
🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐
📊 BACKUP & DEDUPLICATION RESULTS
🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐

🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: 143
🔄 Duplicate Messages Filtered: 63
📨 Total Messages Processed: 206
💾 Total Unique Messages in Storage: 7931
🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐
```

## Key Metrics Displayed

| Metric | Meaning | Example |
|--------|---------|---------|
| **🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP** | Messages newly added to your global storage | 143 |
| **🔄 Duplicate Messages Filtered** | Messages already backed up (not duplicated) | 63 |
| **📨 Total Messages Processed** | All messages in this export | 206 |
| **💾 Total Unique Messages in Storage** | Cumulative backup count across all sessions | 7,931 |

## Why This Matters

### Data Assurance
- **Always know** exactly how many new messages were captured
- **Never worry** about data loss - see the exact backup count
- **Verify success** - clear metrics confirm deduplication worked

### Tracking Progress
- See your global message storage growth over time
- Monitor deduplication efficiency (how many duplicates are being filtered)
- Understand your conversation history scale

### Example Scenarios

**Scenario 1: High New Messages (Good for new work)**
```
🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: 347
🔄 Duplicate Messages Filtered: 12
📨 Total Messages Processed: 359
💾 Total Unique Messages in Storage: 8,421
```
→ Lots of new content captured ✅

**Scenario 2: High Duplicates (Good for context reuse)**
```
🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: 23
🔄 Duplicate Messages Filtered: 377
📨 Total Messages Processed: 400
💾 Total Unique Messages in Storage: 7,954
```
→ Mostly reused context (94% dedup rate) ✅

**Scenario 3: Zero New (Re-running same export)**
```
🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: 0
🔄 Duplicate Messages Filtered: 206
📨 Total Messages Processed: 206
💾 Total Unique Messages in Storage: 7,931
```
→ All messages already captured (safe to skip) ✅

## Implementation Details

### Enhanced Wrapper Script

**File:** `.coditect/scripts/export-dedup-with-status.py`

The wrapper now:
1. Executes the core deduplication script
2. **Parses output** to extract numeric metrics
3. **Displays prominently** with emoji and separators
4. **Logs to file** for persistent record

### Metric Extraction

Uses regex pattern matching to extract numbers from output like:
- `"New unique: 143"` → 143
- `"Total messages: 206"` → 206
- `"Global unique count: 7931"` → 7931

### Visual Hierarchy

```
Step-by-step execution details
     ↓
[All output from core script]
     ↓
╔════════════════════════════════════════╗
║   BACKUP & DEDUPLICATION RESULTS       ║  ← PROMINENT SECTION
║   🆕 NEW UNIQUE MESSAGES: X            ║     (Always visible)
║   🔄 Duplicates Filtered: Y            ║
║   📨 Total Processed: Z                ║
║   💾 Total in Storage: W               ║
╚════════════════════════════════════════╝
     ↓
Execution summary (status, exit code, duration)
     ↓
Log file location
```

## Usage

No special setup needed - it happens automatically:

```bash
/export          # Capture conversation
/export-dedup    # See prominent metrics display
               # Including: NEW UNIQUE MESSAGES ADDED & BACKED UP
/compact         # Safe to free context
```

## Persistent Logging

All metrics are logged to: `MEMORY-CONTEXT/export-dedup-status.txt`

This allows you to:
- Review historical metrics
- Track how many messages you've accumulated
- See trends in deduplication rates
- Verify backup continuity

Example log entry:
```
================================================================================
EXPORT-DEDUP EXECUTION REPORT
================================================================================

[Full execution details...]

🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐
📊 BACKUP & DEDUPLICATION RESULTS
🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐

🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: 143
🔄 Duplicate Messages Filtered: 63
📨 Total Messages Processed: 206
💾 Total Unique Messages in Storage: 7,931
```

## Benefits

### For Users
✅ **Clear visibility** - Never miss how many messages were backed up
✅ **Data confidence** - See exact counts, not just "success/fail"
✅ **Progress tracking** - Monitor your cumulative message storage
✅ **Audit trail** - Historical log of all backup operations
✅ **Peace of mind** - Know exactly what's been preserved

### For Automation
✅ **Parseable metrics** - Extract numbers from output
✅ **Consistent format** - Same metrics every time
✅ **Logged to file** - Can review metrics later
✅ **Exit codes** - Still return proper status for scripting

## Technical Details

### Metric Extraction Function

```python
def extract_metric(text, pattern):
    """Extract numeric metric from output text"""
    match = re.search(rf"{re.escape(pattern)}\s*(\d+)", text)
    if match:
        return int(match.group(1))
    return None
```

Handles various output formats:
- `"New unique: 143"`
- `"New unique messages: 143"`
- `"Total messages: 206"`

### Display Format

```python
metrics_display = f"""
{'🔐'*40}
📊 BACKUP & DEDUPLICATION RESULTS
{'🔐'*40}

🆕 NEW UNIQUE MESSAGES ADDED & BACKED UP: {new_unique_count}
🔄 Duplicate Messages Filtered: {duplicates_count}
📨 Total Messages Processed: {total_messages}
💾 Total Unique Messages in Storage: {global_unique_count}
{'🔐'*40}
"""
```

## Future Enhancements

Potential additions (not implemented):
- [ ] Summary statistics (average messages per session)
- [ ] Growth trends (messages added today vs week ago)
- [ ] Automated alerts (warn if dedup rate too high)
- [ ] CSV export for analytics
- [ ] Dashboard integration

## Summary

✅ **NEW UNIQUE MESSAGES ADDED & BACKED UP** is now **always prominently displayed**
✅ **Visual formatting** ensures you can't miss this metric
✅ **Persistent logging** creates audit trail of all backups
✅ **No configuration** needed - happens automatically
✅ **100% backward compatible** - no breaking changes

**Result: Complete transparency and confidence in your message backup process.**

---

**Document Version:** 1.0
**Last Updated:** November 22, 2025
**Status:** Complete and Tested ✅
# Export-Dedup Status Reports - Implementation Guide

**Date:** November 22, 2025
**Status:** ✅ Complete and Tested
**Version:** 2.1

## Overview

The `/export-dedup` command now **always displays a comprehensive status report** showing exactly what happened during export deduplication, archival, and checkpoint creation.

## The Problem (SOLVED)

Previously, `/export-dedup` would run in the background with **no visible output** to the user. This created uncertainty:
- Did it actually run?
- How many messages were deduplicated?
- Were files archived correctly?
- Did the checkpoint get created?

**Status:** 🎯 SOLVED with guaranteed status reports

## The Solution

### New Wrapper Script: `export-dedup-with-status.py`

Located at: `.coditect/scripts/export-dedup-with-status.py`

This wrapper:
1. **Executes the core deduplication script** (`export-dedup.py`)
2. **Captures all output** (stdout + stderr)
3. **Displays complete execution report** to your terminal immediately
4. **Logs full report** to persistent file: `MEMORY-CONTEXT/export-dedup-status.txt`
5. **Shows clear status summary** with exit code and duration

### Updated Slash Command

The `/export-dedup` command now uses the new wrapper:

```python
import subprocess
import sys

# Use the new wrapper that guarantees output display
result = subprocess.run([
    "python3", ".coditect/scripts/export-dedup-with-status.py"
], cwd=".", capture_output=False, text=True)

sys.exit(result.returncode)
```

**Key difference:** `capture_output=False` ensures all output flows directly to your terminal.

## What You See Now

### Real Example Output

```
================================================================================
EXPORT-DEDUP EXECUTION REPORT
================================================================================
Started: 2025-11-22T00:05:05.843578
Repository: coditect-rollout-master
Status Log: MEMORY-CONTEXT/export-dedup-status.txt
================================================================================

📦 RUNNING DEDUPLICATION PROCESS...

============================================================
CODITECT Export & Deduplicate Workflow
============================================================

Step 1: Looking for export files...
✓ Found 1 export file(s)
  → [6.3m] 2025-11-21-EXPORT-CODITECT-PROJECT-STATUS...txt
     Location: repo root

Step 2: Deduplicating 1 export file(s)...
  Total messages: 206
  New unique: 143
  Duplicates filtered: 63
  Dedup rate: 30.6%

Step 3: Archiving export files...
  ✓ Archived: ... → MEMORY-CONTEXT/exports-archive/

Step 4: Creating checkpoint...
✓ Checkpoint created successfully

============================================================
✅ Export and deduplication complete!
============================================================

📊 Deduplication Summary:
   - New unique messages: 143
   - Total unique messages: 7,931
   - Storage: MEMORY-CONTEXT/dedup_state

📁 Export(s) archived:
   - Location: MEMORY-CONTEXT/exports-archive
   - Files: 1 export(s) moved

📝 Checkpoint created: Automated export and deduplication

================================================================================
EXECUTION SUMMARY
================================================================================
Status: ✅ SUCCESS
Exit Code: 0
Completed: 2025-11-22T00:05:07.497788
Duration: 1.65 seconds
================================================================================

📝 Full report saved to: MEMORY-CONTEXT/export-dedup-status.txt
```

### Information Displayed

Each execution shows:

1. **Execution Header**
   - Start timestamp
   - Repository name
   - Status log file location

2. **Deduplication Process** (5 steps)
   - Export file search results
   - Message processing stats (total, new, duplicates, dedup rate)
   - Archive confirmation with file locations
   - Checkpoint creation status
   - Final summary with statistics

3. **Execution Summary**
   - Status (✅ SUCCESS or ❌ FAILED)
   - Exit code
   - Completion timestamp
   - Duration in seconds

4. **Log Location**
   - Path to persistent status log

## Persistent Status Log

### Location

```
MEMORY-CONTEXT/export-dedup-status.txt
```

### Purpose

Accumulates all `/export-dedup` executions for:
- **Audit trail** - See when exports were processed
- **Historical analysis** - Track deduplication trends
- **Troubleshooting** - Review past failures and successes
- **Progress tracking** - Monitor unique message count over time

### Format

Plain text file with execution reports separated by blank lines:

```
================================================================================
EXPORT-DEDUP EXECUTION REPORT
================================================================================
Started: 2025-11-22T00:05:05.843578
...

[Full output of that execution]

================================================================================
EXECUTION SUMMARY
================================================================================
Status: ✅ SUCCESS
...

[Next execution report starts here...]
```

## Usage

### Normal Usage

```bash
/export-dedup
```

**Result:** Immediate status report displayed to terminal + logged to file

### Check Status Log

View all past executions:

```bash
cat MEMORY-CONTEXT/export-dedup-status.txt
```

See last 10 executions:

```bash
tail -100 MEMORY-CONTEXT/export-dedup-status.txt
```

Find successful runs:

```bash
grep -n "Status: ✅ SUCCESS" MEMORY-CONTEXT/export-dedup-status.txt
```

Find failures:

```bash
grep -n "Status: ❌ FAILED" MEMORY-CONTEXT/export-dedup-status.txt
```

## Key Metrics Shown

Each execution report includes:

| Metric | Meaning |
|--------|---------|
| **Messages in export** | Total messages parsed from export file |
| **New unique** | Number of messages not seen before |
| **Duplicates filtered** | Number of messages already in global store |
| **Dedup rate %** | Percentage of messages that were duplicates |
| **Global unique count** | Total unique messages across all sessions |
| **Files archived** | Number of export files moved to archive |
| **Duration** | Time taken for complete operation |
| **Exit code** | 0 = success, non-zero = failure |

## Integration with Other Commands

### Complete Workflow

```bash
# Step 1: Capture conversation
/export

# Step 2: Process exports + dedup + checkpoint
/export-dedup
# ← See full status report

# Step 3: Free up context
/compact
```

### Automated Workflow

```bash
# All three in sequence with full visibility
/export && /export-dedup && /compact
```

## Error Handling

If `/export-dedup` fails, you'll see:

```
================================================================================
EXPORT-DEDUP EXECUTION REPORT
...

❌ ERROR: [error message]

================================================================================
EXECUTION SUMMARY
================================================================================
Status: ❌ FAILED
Exit Code: 1
...
```

**Troubleshooting steps are shown in the report.**

## Technical Details

### Wrapper Script Location

```
.coditect/scripts/export-dedup-with-status.py
```

### Core Script (unchanged)

```
.coditect/scripts/export-dedup.py
```

The wrapper is a lightweight pass-through that:
1. Calls the core script
2. Captures output
3. Displays it immediately
4. Logs to persistent file
5. Returns same exit code

### Files Modified

- **commands/export-dedup.md** - Updated slash command definition
- **scripts/export-dedup-with-status.py** - New wrapper script (350 lines)

### Backward Compatibility

✅ **100% backward compatible** - Core deduplication logic unchanged
✅ **No breaking changes** - All existing scripts continue to work
✅ **Opt-in visibility** - Wrapper provides additional output without affecting core functionality

## Benefits

### For Users

✅ **Transparency** - Always know what happened
✅ **Peace of mind** - See exact dedup stats
✅ **Audit trail** - Historical log of all executions
✅ **Troubleshooting** - Easy to verify success/failure
✅ **Confidence** - Know when it's safe to /compact

### For Automation

✅ **Predictable output** - Can parse status log for metrics
✅ **Exit codes** - Can detect failures in scripts
✅ **No side effects** - Output-only, doesn't change behavior
✅ **Portable** - Works in any environment (local, CI/CD)

## Examples

### Example 1: Successful Deduplication

```
Status: ✅ SUCCESS
New unique messages: 143
Total unique messages: 7,931
Duration: 1.65 seconds
```

Means:
- 143 new messages were added to the global store
- You now have 7,931 total unique messages preserved
- Process completed quickly

### Example 2: High Deduplication Rate

```
Messages in export: 206
New unique: 52
Duplicates filtered: 154
Dedup rate: 74.8%
```

Means:
- Only 52 out of 206 messages were new
- 154 messages had already been captured before
- Good sign of context reuse

### Example 3: Checking Status Log

```bash
$ grep "Overall dedup rate" MEMORY-CONTEXT/export-dedup-status.txt
Overall dedup rate: 30.6%
Overall dedup rate: 42.3%
Overall dedup rate: 18.9%
Overall dedup rate: 55.1%
```

Shows trend of deduplication rates across sessions.

## Next Steps

### Immediate

1. ✅ Use `/export-dedup` normally
2. ✅ Observe the comprehensive status report
3. ✅ Check `MEMORY-CONTEXT/export-dedup-status.txt` for historical logs

### Future Enhancements

Potential additions (not implemented yet):

- [ ] Configurable output levels (verbose/quiet)
- [ ] JSON export of metrics for parsing
- [ ] Automated alerts for high dedup rates
- [ ] Integration with monitoring dashboard
- [ ] Email notifications for long-running operations

## FAQ

**Q: Can I disable the status report?**
A: No, reporting is always on. This ensures visibility is guaranteed.

**Q: Will this affect performance?**
A: Minimal overhead (~50ms for file I/O to log file). Core deduplication unchanged.

**Q: What if the status log file gets too large?**
A: You can archive it manually:
```bash
mv MEMORY-CONTEXT/export-dedup-status.txt MEMORY-CONTEXT/export-dedup-status-archive-2025-11-22.txt
```

**Q: Can I parse the status log programmatically?**
A: Yes, it's plain text. Use grep/awk to extract metrics. Future JSON format possible.

**Q: Does this work with /compact safely?**
A: Yes. The full execution report is logged to disk before /compact frees context.

## Summary

- ✅ `/export-dedup` now **always displays visible status reports**
- ✅ **Persistent logging** to `MEMORY-CONTEXT/export-dedup-status.txt`
- ✅ **Clear metrics** on messages, duplicates, and archive operations
- ✅ **No silent failures** - always know what happened
- ✅ **100% backward compatible** - existing workflows unaffected

**Result: Complete visibility into your export deduplication workflow.**

---

**Document Version:** 2.1
**Last Updated:** November 22, 2025
**Status:** Complete and Tested ✅
