# CODITECT Memory Management System Design

**Date:** November 22, 2025
**Status:** Architecture Design Phase
**Objective:** Production-grade memory system for 1-2M+ session messages
**Scope:** Storage, search, reporting, backup, and analytics

---

## Executive Summary

As we extract 1-2M+ session messages with full provenance, we need a **production-grade memory management system** that provides:

1. **Persistent Storage** - Scalable database for millions of messages
2. **Fast Search** - Full-text search, filtering, temporal queries
3. **Rich Reporting** - Analytics, project tracking, timeline reconstruction
4. **Intelligent Backup** - Multi-tier redundancy with disaster recovery
5. **Data Integrity** - Provenance preservation, audit trails, verification

**Architecture:** PostgreSQL (primary) + Redis (cache) + Meilisearch (search) + S3 (backup)

**Estimated Capacity:** 2M messages, ~5-10GB storage, sub-second queries

---

## Current State Assessment

### What We Have Now

**JSONL Files (Temporary):**
- Phase 1: 1.2 MB (1,494 messages)
- Phase 2: 92 MB (271,694 messages)
- **Total:** ~93 MB raw text
- **Format:** One JSON per line (parseable but not queryable)
- **Location:** MEMORY-CONTEXT/session-memory-extraction/

**Limitations of Current Approach:**
- ❌ Not queryable (must load entire file to search)
- ❌ Not indexed (linear scan for any search)
- ❌ No backup strategy beyond git
- ❌ Not scalable (JSONL becomes unwieldy at 1-2GB)
- ❌ No analytics capability
- ❌ No temporal queries
- ❌ No project-level aggregation

---

## System Architecture

### High-Level Overview

```
Data Pipeline:
   Extract (Phase 1-7)
        ↓
   Transform & Enrich
        ↓
   PostgreSQL (Primary Store)
        ↓
   ├─ Meilisearch (Full-text index)
   ├─ Redis (Query cache)
   └─ TimescaleDB (Temporal analytics)
        ↓
   Reporting & Analytics
        ↓
   Backup (S3 + Local)
```

### 4-Tier Storage Strategy

#### Tier 1: PostgreSQL (Primary Database)

**Purpose:** Authoritative storage for all messages

**Schema (Simplified):**
```sql
CREATE TABLE session_messages (
  id BIGSERIAL PRIMARY KEY,
  message_id UUID NOT NULL UNIQUE,        -- SHA-256 derived
  hash VARCHAR(64) NOT NULL UNIQUE,       -- For dedup
  content TEXT NOT NULL,
  project_id UUID,                        -- Project association
  session_id UUID,                        -- Session tracking
  phase INTEGER,                          -- Which extraction phase
  source_file VARCHAR(500),               -- Original file location
  source_line INTEGER,                    -- Line in source file
  component VARCHAR(100),                 -- LSP, Hooks, Skills, etc
  log_level VARCHAR(20),                  -- DEBUG, ERROR, INFO
  timestamp TIMESTAMP WITH TIME ZONE,     -- When it happened
  extracted_at TIMESTAMP DEFAULT NOW(),   -- When we extracted it
  metadata JSONB,                         -- Flexible metadata
  searchable_text TSVECTOR,               -- For text search
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_project(project_id),
  INDEX idx_session(session_id),
  INDEX idx_timestamp(timestamp),
  INDEX idx_component(component),
  INDEX idx_hash(hash),
  FULLTEXT INDEX idx_search(searchable_text)
);

CREATE TABLE projects (
  id UUID PRIMARY KEY,
  path VARCHAR(1000) NOT NULL UNIQUE,
  name VARCHAR(500),
  description TEXT,
  first_message_at TIMESTAMP,
  last_message_at TIMESTAMP,
  message_count INTEGER DEFAULT 0,
  active BOOLEAN DEFAULT true,
  metadata JSONB
);

CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  duration_seconds INTEGER,
  message_count INTEGER,
  components_used TEXT[],
  errors_count INTEGER,
  metadata JSONB
);

CREATE TABLE extraction_runs (
  id SERIAL PRIMARY KEY,
  phase INTEGER NOT NULL,
  source_file VARCHAR(500),
  file_size_bytes BIGINT,
  messages_extracted INTEGER,
  new_unique_messages INTEGER,
  duplicate_messages INTEGER,
  errors_count INTEGER,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  source_checksum VARCHAR(64),
  status VARCHAR(50)
);
```

**Capacity:**
- 2M messages: ~500 MB (metadata only)
- Full text index: ~2-3 GB
- Indexes: ~1-2 GB
- **Total:** ~5-7 GB

**Performance:**
- Insert: O(1) with batch loading
- Query by ID: O(1)
- Full-text search: O(log n) with index
- Project aggregation: O(1) with materialized view

#### Tier 2: Meilisearch (Full-Text Search)

**Purpose:** Fast full-text search across all messages

**Index Structure:**
```json
{
  "messages": {
    "fields": {
      "content": { "searchable": true, "analyzer": "en" },
      "component": { "filterable": true },
      "project": { "filterable": true },
      "session_id": { "filterable": true },
      "timestamp": { "sortable": true },
      "log_level": { "filterable": true }
    },
    "ranking_rules": [
      "words",
      "typo",
      "proximity",
      "attribute",
      "sort",
      "exactness"
    ]
  }
}
```

**Query Examples:**
```
# Find all Hooks-related messages in coditect-rollout-master
GET /indexes/messages/search?q=hooks&filter=project:coditect-rollout-master

# Find recent errors
GET /indexes/messages/search?q=&filter=log_level:ERROR&sort=timestamp:desc&limit=50

# Search with autocomplete
GET /indexes/messages/search?q=lsp manager&limit=10
```

**Capacity:**
- 2M messages: ~3-4 GB index
- Query latency: <100ms for most searches
- Result limit: 10,000 documents per request

#### Tier 3: Redis (Query Cache)

**Purpose:** Cache frequent queries for sub-second response

**Key Patterns:**
```python
# Cache keys by query type
sessions:{session_id}                  # Session summary
project:{project_id}:stats             # Project statistics
search:{query_hash}                    # Search results
timeline:{date}                        # Daily activity
top_components                         # Global component stats

# TTL: 1 hour (auto-refresh)
```

**Typical Cache:**
- 100-200 MB for hot queries
- Hit rate: 70-80% on repeat queries

#### Tier 4: S3 Backup + Local Archives

**Purpose:** Disaster recovery and long-term archival

**Backup Strategy:**

```
Daily Incremental Backup:
  PostgreSQL dump → Compress → S3 + Local NAS

Weekly Full Backup:
  - Full database dump
  - All JSONL files
  - Meilisearch snapshot
  - Verification checksums

Monthly Archive:
  - Copy to glacier for 7-year retention
  - Encrypt with KMS key
  - Store manifests
```

**Restore Procedures:**
- Recovery time objective (RTO): <1 hour
- Recovery point objective (RPO): <1 day
- Verification: Checksum validation

---

## Phase 2: Implementation Roadmap

### Week 1: Database Setup

**Tasks:**
1. Create PostgreSQL schema
2. Design index strategy
3. Set up replication/failover
4. Create initial migrations
5. Test with Phase 1-2 data

**Deliverable:** Empty production database ready for data load

### Week 2: Data Loading & Indexing

**Tasks:**
1. Build JSONL → PostgreSQL loader
2. Enrich with cross-references (Phase 1 ↔ Phase 2)
3. Generate full-text indexes
4. Validate data integrity
5. Performance tune queries

**Deliverable:** All 273K Phase 1-2 messages loaded with 100% verification

### Week 3: Search Implementation

**Tasks:**
1. Deploy Meilisearch
2. Create search indexes
3. Build query API wrapper
4. Add filtering/sorting
5. Test search latency

**Deliverable:** Full-text search operational with <100ms queries

### Week 4: Reporting & Analytics

**Tasks:**
1. Create reporting views
2. Build timeline functionality
3. Project-level analytics
4. Session reconstruction
5. Dashboard prototypes

**Deliverable:** Basic reporting operational

### Weeks 5-6: Backup & Operations

**Tasks:**
1. Set up S3 backups
2. Create restore procedures
3. Build monitoring/alerting
4. Document operations
5. Disaster recovery drills

**Deliverable:** Production-ready backup strategy

---

## Database Schema Details

### Core Tables

#### session_messages (Primary)

```sql
-- 2M rows, optimized for queries
CREATE TABLE session_messages (
  id BIGSERIAL PRIMARY KEY,

  -- Message identity
  message_id UUID NOT NULL UNIQUE,
  hash VARCHAR(64) NOT NULL UNIQUE,

  -- Content
  content TEXT NOT NULL,

  -- Context (Foreign keys)
  project_id UUID NOT NULL,
  session_id UUID NOT NULL,

  -- Extraction info
  phase INTEGER NOT NULL,                -- 1-7
  source_file VARCHAR(500),              -- debug/abc123.txt:line-42
  source_line INTEGER,

  -- Structured data
  component VARCHAR(100),                -- LSP, Hooks, Permissions
  log_level VARCHAR(20),                 -- DEBUG, ERROR
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL,

  -- System fields
  searchable_text TSVECTOR,              -- For full-text search
  metadata JSONB,                        -- Flexible fields
  extracted_at TIMESTAMP DEFAULT NOW(),

  -- Indexes
  CONSTRAINT fk_project FOREIGN KEY (project_id) REFERENCES projects(id),
  CONSTRAINT fk_session FOREIGN KEY (session_id) REFERENCES sessions(id),
  INDEX idx_project(project_id),
  INDEX idx_session(session_id),
  INDEX idx_timestamp(timestamp DESC),
  INDEX idx_component(component),
  INDEX idx_log_level(log_level),
  INDEX idx_hash(hash),
  FULLTEXT INDEX idx_search(searchable_text)
);
```

#### projects

```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  path VARCHAR(1000) NOT NULL UNIQUE,
  name VARCHAR(500) NOT NULL,
  description TEXT,

  -- Activity window
  first_message_at TIMESTAMP,
  last_message_at TIMESTAMP,

  -- Aggregates (materialized)
  message_count INTEGER DEFAULT 0,
  session_count INTEGER DEFAULT 0,
  error_count INTEGER DEFAULT 0,

  -- State
  active BOOLEAN DEFAULT true,
  metadata JSONB,

  created_at TIMESTAMP DEFAULT NOW(),

  INDEX idx_path(path),
  INDEX idx_active(active)
);
```

#### sessions

```sql
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  project_id UUID NOT NULL REFERENCES projects(id),

  -- Timing
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  duration_seconds INTEGER GENERATED ALWAYS AS (
    EXTRACT(EPOCH FROM (ended_at - started_at))::integer
  ) STORED,

  -- Aggregates
  message_count INTEGER DEFAULT 0,
  error_count INTEGER DEFAULT 0,
  components_used TEXT[],

  -- Metadata
  metadata JSONB,

  created_at TIMESTAMP DEFAULT NOW(),

  INDEX idx_project(project_id),
  INDEX idx_started(started_at DESC),
  INDEX idx_duration(duration_seconds)
);
```

#### extraction_runs (Audit trail)

```sql
CREATE TABLE extraction_runs (
  id SERIAL PRIMARY KEY,

  phase INTEGER NOT NULL,                -- 1-7
  source_file VARCHAR(500),
  file_size_bytes BIGINT,

  -- Results
  messages_extracted INTEGER,
  new_unique_messages INTEGER,
  duplicate_messages INTEGER,
  errors_count INTEGER,

  -- Timing
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  duration_seconds INTEGER GENERATED ALWAYS AS (
    EXTRACT(EPOCH FROM (completed_at - started_at))::integer
  ) STORED,

  -- Verification
  source_checksum VARCHAR(64),
  destination_checksum VARCHAR(64),
  status VARCHAR(50),

  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Full-Text Search Configuration

### Meilisearch Setup

```json
{
  "indexes": {
    "messages": {
      "primaryKey": "message_id",
      "searchableAttributes": [
        "content",
        "component",
        "project",
        "source_file"
      ],
      "filterableAttributes": [
        "project_id",
        "session_id",
        "component",
        "log_level",
        "phase",
        "timestamp"
      ],
      "sortableAttributes": [
        "timestamp",
        "extracted_at"
      ],
      "ranking_rules": [
        "words",
        "typo",
        "proximity",
        "attribute",
        "sort",
        "exactness"
      ],
      "stop_words": ["the", "a", "an"],
      "synonyms": {
        "LSP": ["language server", "lsp server"],
        "Hooks": ["hook", "event"],
        "error": ["fail", "exception"]
      }
    }
  }
}
```

### Example Queries

```python
# Search everything
POST /indexes/messages/search
{
  "q": "authentication error",
  "limit": 50
}

# Filter by project and time range
POST /indexes/messages/search
{
  "q": "hooks",
  "filter": [
    ["project_id = 'uuid...'"],
    ["timestamp >= 2025-11-15"],
    ["timestamp <= 2025-11-22"]
  ],
  "sort": ["timestamp:desc"]
}

# Aggregation: count by component
POST /indexes/messages/search
{
  "facets": ["component"]
}
```

---

## Reporting Engine

### Pre-Built Reports

#### 1. Project Activity Report

```sql
SELECT
  p.name,
  COUNT(DISTINCT sm.session_id) as sessions,
  COUNT(sm.id) as messages,
  COUNT(CASE WHEN sm.log_level = 'ERROR' THEN 1 END) as errors,
  MIN(sm.timestamp) as started,
  MAX(sm.timestamp) as last_activity,
  EXTRACT(DAY FROM MAX(sm.timestamp) - MIN(sm.timestamp)) as days_active
FROM session_messages sm
JOIN projects p ON sm.project_id = p.id
GROUP BY p.id, p.name
ORDER BY messages DESC;
```

**Output:** Which projects are most active, error rates, timeline

#### 2. Timeline Report

```sql
SELECT
  DATE(sm.timestamp) as date,
  p.name as project,
  COUNT(sm.id) as messages,
  COUNT(DISTINCT sm.session_id) as sessions,
  COUNT(CASE WHEN sm.log_level = 'ERROR' THEN 1 END) as errors,
  ARRAY_AGG(DISTINCT sm.component) as components
FROM session_messages sm
JOIN projects p ON sm.project_id = p.id
WHERE sm.timestamp >= NOW() - INTERVAL '30 days'
GROUP BY DATE(sm.timestamp), p.name
ORDER BY date DESC, messages DESC;
```

**Output:** Daily activity breakdown by project

#### 3. Component Usage Report

```sql
SELECT
  component,
  COUNT(sm.id) as occurrences,
  COUNT(DISTINCT sm.session_id) as sessions,
  COUNT(DISTINCT DATE(sm.timestamp)) as active_days,
  COUNT(CASE WHEN sm.log_level = 'ERROR' THEN 1 END) as errors,
  ROUND(100.0 * COUNT(CASE WHEN sm.log_level = 'ERROR' THEN 1 END)
        / COUNT(sm.id), 2) as error_rate_pct
FROM session_messages
WHERE component IS NOT NULL
GROUP BY component
ORDER BY occurrences DESC;
```

**Output:** Which Claude Code features most used, reliability metrics

#### 4. Session Reconstruction Report

```sql
SELECT
  sm.session_id,
  p.name as project,
  s.started_at,
  s.ended_at,
  s.duration_seconds,
  COUNT(sm.id) as messages,
  ARRAY_AGG(DISTINCT sm.component ORDER BY sm.component) as components,
  COUNT(CASE WHEN sm.log_level = 'ERROR' THEN 1 END) as errors
FROM session_messages sm
JOIN projects p ON sm.project_id = p.id
JOIN sessions s ON sm.session_id = s.id
WHERE sm.session_id = $1
GROUP BY sm.session_id, p.name, s.started_at, s.ended_at, s.duration_seconds
ORDER BY sm.timestamp;
```

**Output:** Complete reconstruction of specific session

#### 5. Error Analysis Report

```sql
SELECT
  sm.component,
  p.name as project,
  COUNT(sm.id) as error_count,
  COUNT(DISTINCT sm.session_id) as affected_sessions,
  COUNT(DISTINCT DATE(sm.timestamp)) as days_with_errors,
  ARRAY_AGG(DISTINCT SUBSTRING(sm.content, 1, 100)) as error_samples
FROM session_messages sm
JOIN projects p ON sm.project_id = p.id
WHERE sm.log_level = 'ERROR'
GROUP BY sm.component, p.name
ORDER BY error_count DESC;
```

**Output:** Error patterns and affected systems

---

## Backup & Disaster Recovery

### Backup Strategy

#### Daily Incremental Backup
```bash
# Day 1: Full backup
pg_dump coditect_memory --compress --file backup-2025-11-22.sql.gz
aws s3 cp backup-2025-11-22.sql.gz s3://coditect-backups/daily/
cp backup-2025-11-22.sql.gz /mnt/nas/backups/

# Days 2-7: Incremental
pg_basebackup --wal-method=stream --format=tar | gzip > incremental.tar.gz
aws s3 cp incremental.tar.gz s3://coditect-backups/incremental/$(date +%s).tar.gz
```

#### Weekly Full Backup
```bash
# Full database
pg_dump coditect_memory --verbose --file full-backup-$(date +%Y-%m-%d).sql
gzip full-backup-*.sql

# Export all data for long-term archive
aws s3 cp full-backup-*.sql.gz s3://coditect-backups/weekly/
aws s3 cp full-backup-*.sql.gz s3://coditect-backups-archive/$(date +%Y)/

# Create manifest
echo "{
  'date': '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
  'size_bytes': $(du -b backup-*.sql.gz),
  'hash': '$(sha256sum full-backup-*.sql.gz)',
  'compression': 'gzip'
}" > manifest.json
```

#### Monthly Archive to Glacier
```bash
aws s3 cp s3://coditect-backups-archive/2025-11/ \
  s3://coditect-glacier-archive/ \
  --storage-class GLACIER_IR \
  --sse aws:kms \
  --sse-kms-key-id arn:aws:kms:us-east-1:ACCOUNT:key/ID
```

### Restore Procedures

#### Point-in-Time Recovery
```bash
# Get latest backup
aws s3 cp s3://coditect-backups/daily/backup-latest.sql.gz .
gunzip backup-latest.sql.gz

# Restore to test database
createdb coditect_memory_restore
psql coditect_memory_restore < backup-latest.sql

# Verify integrity
SELECT COUNT(*) FROM session_messages;  -- Should be 273,188+
SELECT COUNT(*) FROM projects;           -- Should be 16+
```

#### Emergency Full Recovery
```bash
# 1. Create new database
createdb coditect_memory_recovered

# 2. Restore from most recent backup
psql coditect_memory_recovered < backup-2025-11-22.sql.gz

# 3. Verify checksum
SELECT md5(string_agg(hash, '' ORDER BY hash))
FROM session_messages;
-- Compare with stored manifest checksum

# 4. Validate all constraints
ALTER TABLE session_messages ENABLE CONSTRAINT ALL;
SELECT COUNT(*) FROM session_messages WHERE project_id IS NULL;  -- Should be 0

# 5. Reindex
REINDEX DATABASE coditect_memory_recovered;

# 6. Switch over
ALTER DATABASE coditect_memory RENAME TO coditect_memory_old;
ALTER DATABASE coditect_memory_recovered RENAME TO coditect_memory;
```

---

## Implementation Timeline

### Phase 1: Infrastructure (Week 1-2)

**Deliverables:**
- PostgreSQL 15+ configured with replication
- Redis cache layer deployed
- Monitoring and alerting setup
- Initial schema created
- Data loading pipeline built

**Effort:** 40 hours

### Phase 2: Data Migration (Week 2-3)

**Deliverables:**
- All Phase 1-2 messages loaded
- Cross-reference enrichment complete
- Full-text indexes built
- Meilisearch deployed and indexed
- Data validation complete

**Effort:** 30 hours

### Phase 3: Search & Analytics (Week 3-4)

**Deliverables:**
- Search API operational
- Pre-built reports available
- Dashboard prototypes
- Query performance optimized
- Documentation complete

**Effort:** 35 hours

### Phase 4: Backup & Operations (Week 4-5)

**Deliverables:**
- Backup automation running
- Disaster recovery tested
- Monitoring dashboards
- Runbooks and playbooks
- Team training

**Effort:** 25 hours

**Total Effort:** 130 hours (~3.25 weeks full-time)

---

## Cost Estimation

### Infrastructure (Monthly)

| Component | Capacity | Cost |
|-----------|----------|------|
| PostgreSQL (RDS) | 500 GB | $150-300 |
| Redis (ElastiCache) | 2 GB | $20-40 |
| Meilisearch (self-hosted) | 10 GB | ~$0 (EC2) |
| S3 Storage | 50 GB | $1.15 |
| S3 Backups | 100 GB | $2.30 |
| Glacier Archive | 1 TB | $4 |
| **Total** | | **$177-350/month** |

### Development Cost

| Phase | Hours | Cost (@$100/hr) |
|-------|-------|-----------------|
| Infrastructure | 40 | $4,000 |
| Data Migration | 30 | $3,000 |
| Search/Analytics | 35 | $3,500 |
| Backup/Ops | 25 | $2,500 |
| **Total** | **130** | **$13,000** |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Search Latency** | <100ms | 95th percentile |
| **Query Accuracy** | 100% | Verified results |
| **Data Integrity** | 100% | Checksums match |
| **Backup Success** | 99.9% | Monthly test pass |
| **Recovery Time** | <1 hour | Drill results |
| **Uptime** | 99.95% | Monitoring data |
| **Scalability** | 10M messages | Tested capacity |

---

## Next Steps

1. **Immediate:** Review architecture and get approval
2. **Week 1:** Provision PostgreSQL and set up schema
3. **Week 2:** Load Phase 1-2 data and enrich
4. **Week 3:** Deploy search and build reports
5. **Week 4:** Setup backup automation and test recovery
6. **Ongoing:** Continue phases 3-7 extraction with new pipeline

---

## Conclusion

This production-grade memory management system will:

✅ Store 1-2M messages safely and reliably
✅ Enable fast search across all data
✅ Provide rich reporting and analytics
✅ Protect against data loss
✅ Support long-term archival
✅ Enable session reconstruction
✅ Scale to future growth

Estimated total investment: **$13,000 development + $2,100/year operations**

---

**Architecture Version:** 1.0
**Design Date:** November 22, 2025
**Status:** Ready for Implementation Review

