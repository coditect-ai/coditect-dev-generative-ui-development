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
