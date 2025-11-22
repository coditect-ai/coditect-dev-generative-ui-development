# MEMORY-CONTEXT Week 1 Implementation Guide

**Project:** CODITECT Rollout Master - MEMORY-CONTEXT Consolidation
**Timeline:** Week 1 (Days 1-5)
**Status:** In Progress - Day 1
**Date:** 2025-11-17

---

## Executive Summary

Week 1 focuses on establishing the core infrastructure for the Hybrid Centralized + Distributed MEMORY-CONTEXT architecture. This includes provisioning PostgreSQL as the central database, ChromaDB for semantic search, and implementing the Context API service.

### Week 1 Objectives

- **Day 1:** Infrastructure provisioning (PostgreSQL + ChromaDB)
- **Day 2-3:** Context API development (FastAPI)
- **Day 4:** Schema migration and data validation
- **Day 5:** Service deployment and integration testing

### Success Criteria

- [ ] PostgreSQL database operational with migrated schema
- [ ] ChromaDB instance running with embedding service
- [ ] Context API deployed with core CRUD endpoints
- [ ] All existing MEMORY-CONTEXT data migrated successfully
- [ ] Integration tests passing (>95% success rate)
- [ ] API response times <500ms (p95)

---

## Day 1: Infrastructure Provisioning

### Objectives

1. Provision PostgreSQL 14+ database
2. Set up ChromaDB instance with embedding service
3. Configure initial database schema
4. Validate connectivity and basic operations

### Team Assignments

**Database Architect:**
- PostgreSQL provisioning and configuration
- Schema migration from SQLite design
- Index optimization and query planning

**DevOps Engineer:**
- ChromaDB Docker setup
- Infrastructure automation scripts
- Monitoring and logging configuration

### Deliverables

**1. PostgreSQL Database Setup**
- Database instance (local or Cloud SQL)
- Extensions: pg_trgm, uuid-ossp
- Initial schema created
- Connection credentials secured

**2. ChromaDB Instance**
- Docker container running ChromaDB
- Embedding model configured
- Collections created
- API endpoint accessible

**3. Infrastructure Automation**
- Docker Compose configuration
- Setup scripts for reproducible deployment
- Health check endpoints
- Backup configuration

---

## PostgreSQL Setup Details

### Installation Options

**Option A: Local PostgreSQL (Development)**
```bash
# macOS (Homebrew)
brew install postgresql@14
brew services start postgresql@14

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql-14 postgresql-contrib-14
sudo systemctl start postgresql
```

**Option B: Docker PostgreSQL (Recommended)**
```bash
# See docker-compose.yml in infrastructure/ directory
docker-compose up -d postgres
```

**Option C: Google Cloud SQL (Production)**
```bash
# See infrastructure/terraform/cloudsql.tf
terraform init
terraform plan
terraform apply
```

### Database Configuration

**Database Name:** `coditect_memory_context`
**User:** `coditect_admin` (with password from secrets)
**Extensions Required:**
- `pg_trgm` - Full-text search
- `uuid-ossp` - UUID generation
- `pgcrypto` - Encryption functions

**Performance Settings:**
```sql
-- Recommended postgresql.conf settings
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
```

### Schema Migration from SQLite

**Source:** `.coditect/MEMORY-CONTEXT/database-schema.sql`
**Target:** PostgreSQL with modifications

**Key Changes:**
- `INTEGER PRIMARY KEY AUTOINCREMENT` → `SERIAL PRIMARY KEY`
- `TEXT` columns → `VARCHAR` or `TEXT` (explicit lengths where appropriate)
- `BOOLEAN DEFAULT 0` → `BOOLEAN DEFAULT FALSE`
- Add explicit `TIMESTAMP WITH TIME ZONE` for all timestamp columns
- Replace `datetime('now')` with `NOW()`

**Migration Script:** `infrastructure/postgres/schema-migration.sql`

---

## ChromaDB Setup Details

### Installation and Configuration

**Deployment:** Docker container with persistent volume

**Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
- Lightweight (80MB)
- Fast inference (<50ms per document)
- 384-dimensional embeddings
- Good balance of speed and quality

**Collections:**
1. `sessions_embeddings` - Session context summaries
2. `checkpoints_embeddings` - Checkpoint descriptions
3. `patterns_embeddings` - Extracted patterns

### ChromaDB Docker Setup

**Image:** `chromadb/chroma:latest`
**Persistence:** Local volume mount
**API Port:** 8000
**Health Check:** HTTP GET to `/api/v1/heartbeat`

**Configuration:** See `infrastructure/chromadb/config.yml`

---

## Context API Specification (Preview)

**Framework:** FastAPI (Python 3.11+)
**Database Driver:** asyncpg (async PostgreSQL)
**ChromaDB Client:** chromadb Python SDK

### Core Endpoints (Day 2-3 Implementation)

**Sessions:**
- `GET /api/v1/sessions` - List sessions with filters
- `GET /api/v1/sessions/{session_id}` - Get session details
- `POST /api/v1/sessions` - Create new session
- `PATCH /api/v1/sessions/{session_id}` - Update session
- `DELETE /api/v1/sessions/{session_id}` - Soft delete session

**Checkpoints:**
- `GET /api/v1/checkpoints` - List checkpoints
- `GET /api/v1/checkpoints/{checkpoint_id}` - Get checkpoint
- `POST /api/v1/checkpoints` - Create checkpoint

**Search:**
- `GET /api/v1/search` - Semantic search (uses ChromaDB)
- `GET /api/v1/search/sessions` - Search sessions only
- `GET /api/v1/search/patterns` - Search patterns only

**Patterns:**
- `GET /api/v1/patterns` - List patterns
- `GET /api/v1/patterns/{pattern_id}` - Get pattern
- `POST /api/v1/patterns` - Create pattern

---

## Day 1 Implementation Artifacts

### 1. Docker Compose Configuration

**File:** `infrastructure/docker-compose.yml`

Includes:
- PostgreSQL 14 container
- ChromaDB container
- Redis container (for future caching)
- Network configuration
- Volume mounts
- Health checks

### 2. PostgreSQL Schema Migration

**File:** `infrastructure/postgres/schema-migration.sql`

Complete PostgreSQL schema based on SQLite design:
- All 9 tables migrated
- Indexes optimized for PostgreSQL
- Views recreated
- Foreign key constraints
- Initial metadata

### 3. ChromaDB Setup Script

**File:** `infrastructure/chromadb/setup-collections.py`

Python script to:
- Initialize ChromaDB client
- Create collections
- Configure embedding model
- Test embedding generation
- Health check

### 4. Infrastructure Automation

**File:** `infrastructure/setup.sh`

Bash script to:
- Check prerequisites (Docker, Python 3.11+)
- Start Docker Compose services
- Wait for PostgreSQL ready
- Run schema migration
- Initialize ChromaDB collections
- Validate all services healthy
- Display connection info

### 5. Testing and Validation

**File:** `infrastructure/tests/test-day1.py`

Integration tests:
- PostgreSQL connectivity
- Schema validation (all tables exist)
- ChromaDB API accessibility
- Embedding generation test
- Basic CRUD operations

---

## Execution Timeline - Day 1

### Morning (0900-1200)

**Database Architect:**
- [ ] Review SQLite schema
- [ ] Design PostgreSQL schema modifications
- [ ] Create schema-migration.sql
- [ ] Test migration on local PostgreSQL

**DevOps Engineer:**
- [ ] Create docker-compose.yml
- [ ] Configure PostgreSQL container
- [ ] Configure ChromaDB container
- [ ] Test container orchestration

### Afternoon (1300-1700)

**Database Architect:**
- [ ] Optimize indexes for PostgreSQL
- [ ] Create database initialization script
- [ ] Document schema changes and rationale
- [ ] Performance testing (simple queries)

**DevOps Engineer:**
- [ ] Create setup-collections.py for ChromaDB
- [ ] Write infrastructure automation (setup.sh)
- [ ] Create health check endpoints
- [ ] Write Day 1 integration tests

### End of Day Checkpoint

- [ ] All Docker containers running
- [ ] PostgreSQL accessible with schema created
- [ ] ChromaDB collections initialized
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Commit infrastructure code to git

---

## Day 2-3: Context API Development

### Objectives

1. Implement FastAPI application structure
2. Create database models and ORM layer
3. Implement core CRUD endpoints
4. Add ChromaDB integration for search
5. Comprehensive API testing

### Team Assignments

**Backend Developer:**
- FastAPI application setup
- Database models (SQLAlchemy)
- CRUD operations implementation
- API endpoint development
- Unit and integration tests

**Database Architect (Support):**
- Query optimization
- Index tuning
- Performance monitoring
- Database access patterns

---

## Day 4: Schema Migration and Data Validation

### Objectives

1. Migrate existing data from SQLite to PostgreSQL
2. Migrate existing sessions/checkpoints to new structure
3. Generate embeddings for all existing content
4. Validate data integrity

### Data Migration Plan

**Source Databases:**
- Framework: `.coditect/MEMORY-CONTEXT/memory-context.db` (212KB)
- Master: No existing database (file-based only)

**Migration Steps:**
1. Export all data from SQLite to JSON
2. Transform data to match PostgreSQL schema
3. Import data into PostgreSQL tables
4. Generate embeddings for all sessions/checkpoints
5. Store embeddings in ChromaDB
6. Validate row counts and data integrity
7. Create backup of original SQLite database

**Migration Script:** `infrastructure/migration/migrate-data.py`

---

## Day 5: Service Deployment and Testing

### Objectives

1. Deploy Context API as systemd service (or Docker)
2. Configure API authentication
3. Run comprehensive integration tests
4. Performance testing and optimization
5. Documentation and handoff

### Deployment Options

**Option A: Systemd Service (Linux)**
- FastAPI with Uvicorn
- Systemd unit file
- Auto-restart on failure
- Logging to journald

**Option B: Docker Container**
- Dockerfile for Context API
- Docker Compose integration
- Container orchestration
- Health checks

**Option C: Google Cloud Run (Production)**
- Containerized deployment
- Auto-scaling
- HTTPS endpoint
- Cloud SQL connection

### Testing Strategy

**Unit Tests:**
- Individual endpoint tests
- Database model tests
- ChromaDB integration tests

**Integration Tests:**
- End-to-end API workflows
- Database transactions
- Search functionality
- Error handling

**Performance Tests:**
- Load testing (100+ concurrent requests)
- Response time validation (<500ms p95)
- Database query performance
- ChromaDB search latency

**Success Criteria:**
- [ ] All integration tests pass (>95%)
- [ ] API uptime >99%
- [ ] Response times <500ms (p95)
- [ ] No data loss during migration
- [ ] Search results accurate and relevant

---

## Risk Mitigation

### Top Risks - Week 1

**1. PostgreSQL Performance Issues**
- **Risk:** Slow queries, connection pooling problems
- **Mitigation:** Index optimization, connection pool tuning, query profiling
- **Contingency:** Use read replicas if needed

**2. ChromaDB Embedding Generation Delays**
- **Risk:** Embedding 100+ documents takes too long
- **Mitigation:** Batch processing, async embedding generation
- **Contingency:** Queue embeddings for background processing

**3. Data Migration Failures**
- **Risk:** Data loss or corruption during migration
- **Mitigation:** Comprehensive backups, dry-run migrations, validation scripts
- **Contingency:** Rollback plan to SQLite

**4. API Development Delays**
- **Risk:** FastAPI implementation takes longer than expected
- **Mitigation:** Start with minimal viable API, incremental feature additions
- **Contingency:** Reduce scope to core CRUD operations only

---

## Next Steps After Week 1

### Week 2: Data Migration and Rollout

- Consolidate framework MEMORY-CONTEXT data
- Consolidate master MEMORY-CONTEXT data
- Deploy sync agents to framework + master
- Pilot with 5 submodules

### Week 3: Full Rollout

- Deploy to all 23 submodules
- Monitor performance and errors
- Optimize based on usage patterns
- Create operator documentation

---

## Appendix: File Structure

```
coditect-rollout-master/
├── infrastructure/
│   ├── docker-compose.yml
│   ├── setup.sh
│   ├── postgres/
│   │   ├── schema-migration.sql
│   │   └── init.sh
│   ├── chromadb/
│   │   ├── config.yml
│   │   └── setup-collections.py
│   ├── migration/
│   │   ├── migrate-data.py
│   │   └── validate-migration.py
│   ├── tests/
│   │   ├── test-day1.py
│   │   ├── test-day2-3.py
│   │   ├── test-day4.py
│   │   └── test-day5.py
│   └── deployment/
│       ├── context-api.service (systemd)
│       ├── Dockerfile (Context API)
│       └── cloudbuild.yaml (GCP)
├── context-api/
│   ├── main.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py (SQLAlchemy)
│   │   ├── schemas.py (Pydantic)
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── chromadb_client.py
│   │   └── routers/
│   │       ├── sessions.py
│   │       ├── checkpoints.py
│   │       ├── patterns.py
│   │       └── search.py
│   └── tests/
│       ├── test_sessions.py
│       ├── test_checkpoints.py
│       └── test_search.py
└── docs/
    ├── MEMORY-CONTEXT-ARCHITECTURE-ANALYSIS.md (complete SDD)
    ├── MEMORY-CONTEXT-RECOMMENDATION-SUMMARY.md (executive summary)
    ├── MEMORY-CONTEXT-WEEK1-IMPLEMENTATION.md (this file)
    └── MEMORY-CONTEXT-API-REFERENCE.md (API documentation)
```

---

**Last Updated:** 2025-11-17
**Status:** Ready for Day 1 Implementation
**Next Milestone:** PostgreSQL and ChromaDB provisioned by end of Day 1
