# CODITECT Memory Management Submodule Plan

**Date:** November 22, 2025
**Status:** Planning Phase
**Objective:** Create production-grade memory management system as dedicated submodule
**Category:** Core infrastructure (goes in submodules/core/)

---

## Submodule Structure

### Proposed Location
```
submodules/core/coditect-memory-management/
```

### Rationale for Core Category
- **Why Core?** Memory management is fundamental infrastructure like coditect-core
- **Not Dev:** Too critical to be developer tool
- **Not Cloud:** Not cloud-specific, local-first
- **Not Market/GTM:** Backend infrastructure, not customer-facing
- **Perfect Fit:** Core framework component

### Directory Structure

```
submodules/core/coditect-memory-management/
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py         # PostgreSQL connection pooling
│   │   ├── schema.py              # SQL schema definitions
│   │   ├── migrations.py          # Alembic migration manager
│   │   └── models.py              # SQLAlchemy ORM models
│   ├── search/
│   │   ├── __init__.py
│   │   ├── meilisearch_client.py  # Meilisearch integration
│   │   ├── indexing.py            # Index management
│   │   └── query.py               # Search query interface
│   ├── cache/
│   │   ├── __init__.py
│   │   ├── redis_client.py        # Redis connection
│   │   ├── cache_keys.py          # Key naming scheme
│   │   └── strategies.py          # Cache strategies
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── jsonl_loader.py        # JSONL file loading
│   │   ├── enrichment.py          # Cross-reference enrichment
│   │   ├── validation.py          # Data validation
│   │   └── deduplication.py       # Checksum-based dedup
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── reporters.py           # Report generators
│   │   ├── queries.py             # Pre-built SQL reports
│   │   └── templates.py           # Report formatting
│   ├── backup/
│   │   ├── __init__.py
│   │   ├── backup_manager.py      # Backup orchestration
│   │   ├── s3_backend.py          # S3 storage
│   │   ├── local_backend.py       # Local NAS storage
│   │   ├── restore.py             # Recovery procedures
│   │   └── verification.py        # Integrity checking
│   ├── api/
│   │   ├── __init__.py
│   │   ├── server.py              # FastAPI app
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── search.py          # /api/search/*
│   │   │   ├── messages.py        # /api/messages/*
│   │   │   ├── projects.py        # /api/projects/*
│   │   │   ├── sessions.py        # /api/sessions/*
│   │   │   ├── reports.py         # /api/reports/*
│   │   │   └── health.py          # /api/health
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py            # API authentication
│   │       ├── logging.py         # Request logging
│   │       └── ratelimit.py       # Rate limiting
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── commands.py            # CLI entry points
│   │   ├── ingest.py              # `memory ingest` command
│   │   ├── backup.py              # `memory backup` command
│   │   ├── restore.py             # `memory restore` command
│   │   ├── verify.py              # `memory verify` command
│   │   └── search.py              # `memory search` command
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── metrics.py             # Prometheus metrics
│   │   ├── logging.py             # Structured logging
│   │   └── alerts.py              # Alert conditions
│   └── utils/
│       ├── __init__.py
│       ├── checksum.py            # SHA-256 utilities
│       ├── datetime.py            # Temporal utilities
│       └── config.py              # Configuration management
├── migrations/
│   ├── __init__.py
│   ├── env.py                     # Alembic config
│   └── versions/
│       ├── 001_initial_schema.py
│       ├── 002_add_indexes.py
│       └── ...
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── unit/
│   │   ├── test_database.py
│   │   ├── test_search.py
│   │   ├── test_cache.py
│   │   ├── test_ingestion.py
│   │   └── test_backup.py
│   ├── integration/
│   │   ├── test_api.py
│   │   ├── test_end_to_end.py
│   │   └── test_recovery.py
│   └── fixtures/
│       ├── sample_messages.json
│       └── test_data.sql
├── docs/
│   ├── README.md                  # Project overview
│   ├── ARCHITECTURE.md            # System architecture
│   ├── API.md                     # API documentation
│   ├── OPERATIONS.md              # Operational guide
│   ├── CLI.md                     # Command-line guide
│   ├── DATABASE.md                # Database schema docs
│   ├── BACKUP.md                  # Backup/recovery guide
│   └── DEPLOYMENT.md              # Deployment instructions
├── docker/
│   ├── Dockerfile                 # Application image
│   ├── docker-compose.yml         # Local dev environment
│   └── .dockerignore
├── scripts/
│   ├── init_db.sh                 # Initialize database
│   ├── load_data.sh               # Load JSONL data
│   ├── backup.sh                  # Backup automation
│   ├── restore.sh                 # Restore from backup
│   └── health_check.sh            # Health monitoring
├── config/
│   ├── default.yaml               # Default configuration
│   ├── development.yaml           # Dev environment
│   ├── production.yaml            # Prod environment
│   └── testing.yaml               # Test environment
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Modern Python packaging
├── setup.py                       # Installation script
├── Makefile                       # Common tasks
├── .coditect -> ../../.coditect   # Distributed intelligence
├── .claude -> .coditect           # Claude Code access
├── .gitignore
├── LICENSE
├── README.md                      # User-facing documentation
├── CLAUDE.md                      # Claude Code integration
├── PROJECT-PLAN.md               # Project plan & timeline
├── TASKLIST.md                    # Task tracking
└── CHANGELOG.md                   # Version history
```

---

## Key Components by Module

### 1. Database Module (`src/database/`)

**Purpose:** PostgreSQL connection, schema, and ORM

**Key Classes:**
```python
class DatabaseConnection:
    """Connection pooling and lifecycle management"""
    def __init__(self, connection_string):
        self.pool = create_engine(connection_string, poolclass=QueuePool)

    def execute_query(self, query):
        """Execute raw SQL"""

    def get_session(self):
        """Get SQLAlchemy session"""

class SessionMessage(Base):
    """ORM model for session_messages table"""
    __tablename__ = 'session_messages'
    id: int
    message_id: UUID
    hash: str
    content: str
    project_id: UUID
    session_id: UUID
    ...

class SchemaManager:
    """Create/migrate schema"""
    def create_tables(self):
        """Create all tables"""

    def migrate(self, revision):
        """Run Alembic migration"""
```

**Features:**
- Connection pooling (20-50 concurrent connections)
- SQLAlchemy ORM for type safety
- Alembic migrations for schema versioning
- Read replicas for analytics queries
- Prepared statements for security

### 2. Search Module (`src/search/`)

**Purpose:** Meilisearch integration for full-text search

**Key Classes:**
```python
class MeilisearchClient:
    """Meilisearch interaction"""
    def __init__(self, base_url, api_key):
        self.client = Client(base_url, api_key)

    def search(self, query, filters=None, limit=50):
        """Execute search with optional filters"""

    def faceted_search(self, query, facets):
        """Search with facet aggregation"""

class IndexManager:
    """Index lifecycle management"""
    def create_index(self, name):
        """Create new index"""

    def reindex(self):
        """Rebuild all indexes from database"""

    def add_document(self, message):
        """Add single message to index"""

    def bulk_add(self, messages):
        """Add many messages efficiently"""
```

**Features:**
- Full-text search with synonym support
- Field filtering (project, component, log level)
- Faceted aggregation (count by component)
- Autocomplete suggestions
- Typo tolerance
- Ranking customization

### 3. Cache Module (`src/cache/`)

**Purpose:** Redis caching for hot queries

**Key Classes:**
```python
class CacheStrategy:
    """Cache management strategy"""
    def __init__(self, redis_client, ttl_seconds=3600):
        self.redis = redis_client
        self.ttl = ttl_seconds

    def get(self, key):
        """Retrieve from cache"""

    def set(self, key, value, ttl=None):
        """Store in cache"""

    def invalidate(self, pattern):
        """Invalidate cache entries matching pattern"""

class QueryCache:
    """Cache query results"""
    def cache_search_results(self, query_hash, results):
        """Cache search results"""

    def cache_project_stats(self, project_id, stats):
        """Cache project statistics"""
```

**Features:**
- Key namespacing (sessions:*, projects:*, searches:*)
- Automatic expiration (TTL)
- Cache invalidation patterns
- Hit/miss statistics
- Memory optimization

### 4. Ingestion Module (`src/ingestion/`)

**Purpose:** Load JSONL files and enrich data

**Key Classes:**
```python
class JSONLLoader:
    """Load JSONL files into database"""
    def __init__(self, db_connection):
        self.db = db_connection

    def load_file(self, filepath, phase):
        """Load JSONL file with progress tracking"""

    def load_batch(self, messages, batch_size=1000):
        """Insert batch of messages"""

class Enrichment:
    """Enrich messages with cross-references"""
    def enrich_phase2_with_projects(self, messages):
        """Cross-ref Phase 2 debug logs with Phase 1 projects"""

    def compute_session_stats(self):
        """Calculate session duration, component list, etc"""

class Deduplication:
    """Checksum-based deduplication"""
    def compute_hash(self, message_content):
        """SHA-256 hash of content"""

    def find_duplicates(self, messages):
        """Identify messages already in database"""
```

**Features:**
- Streaming JSONL loader (memory efficient)
- Progress tracking and resume capability
- Batch insert optimization
- Automatic enrichment
- Duplicate detection via checksums

### 5. Reporting Module (`src/reporting/`)

**Purpose:** Generate reports and analytics

**Key Classes:**
```python
class ReportGenerator:
    """Generate various reports"""
    def project_activity_report(self, start_date, end_date):
        """Project activity summary"""

    def timeline_report(self, days=30):
        """Daily activity breakdown"""

    def component_usage_report(self):
        """Feature usage statistics"""

    def error_analysis_report(self):
        """Error patterns and trends"""

    def session_report(self, session_id):
        """Complete session reconstruction"""

class ReportRenderer:
    """Render reports in various formats"""
    def as_table(self, report):
        """ASCII table output"""

    def as_json(self, report):
        """JSON output"""

    def as_html(self, report):
        """HTML report"""

    def as_csv(self, report):
        """CSV export"""
```

**Features:**
- Pre-built SQL reports
- Custom query interface
- Multiple output formats
- Scheduled report generation
- Email delivery

### 6. Backup Module (`src/backup/`)

**Purpose:** Database backup and disaster recovery

**Key Classes:**
```python
class BackupManager:
    """Orchestrate backups"""
    def full_backup(self):
        """Create full backup"""

    def incremental_backup(self):
        """Create incremental backup"""

    def schedule_backups(self, schedule):
        """Set up backup schedule"""

class S3Backend:
    """Store backups in S3"""
    def upload_backup(self, filepath):
        """Upload to S3 with encryption"""

    def list_backups(self):
        """List available backups"""

    def download_backup(self, backup_id):
        """Download specific backup"""

class RestoreManager:
    """Restore from backup"""
    def restore_full(self, backup_id):
        """Restore entire database"""

    def restore_point_in_time(self, timestamp):
        """Restore to specific time"""

    def verify_restore(self):
        """Verify restored data integrity"""
```

**Features:**
- Full and incremental backups
- Multi-destination (S3 + local NAS)
- Encryption with KMS
- Automatic scheduling
- Point-in-time recovery
- Verification checksums
- Disaster recovery testing

### 7. API Module (`src/api/`)

**Purpose:** FastAPI REST interface

**Endpoints:**
```
GET  /api/health                      # System health check
GET  /api/search?q=...                # Search messages
GET  /api/messages/{id}               # Get specific message
GET  /api/projects                    # List all projects
GET  /api/projects/{id}/stats         # Project statistics
GET  /api/sessions/{id}               # Session details
GET  /api/sessions/{id}/timeline      # Session reconstruction
GET  /api/reports/projects            # Project activity report
GET  /api/reports/timeline            # Daily activity
GET  /api/reports/components          # Feature usage
GET  /api/reports/errors              # Error analysis
```

**Features:**
- OpenAPI documentation
- Authentication (API key)
- Rate limiting
- Request logging
- Error handling
- Response caching

### 8. CLI Module (`src/cli/`)

**Purpose:** Command-line interface

**Commands:**
```bash
# Ingest JSONL files
memory ingest /path/to/extracted-messages.jsonl --phase 3

# Backup database
memory backup --full --destination s3://bucket/

# Restore from backup
memory restore --backup-id latest --verify

# Verify data integrity
memory verify --check-hashes

# Search from command line
memory search "hooks" --project coditect-rollout-master --limit 50

# Generate reports
memory report --type project-activity --format csv --output report.csv

# Health check
memory health
```

**Features:**
- Click CLI framework
- Command grouping
- Progress bars
- Error handling
- Colored output

---

## Technology Stack

### Backend
- **Python 3.11+** - Type-safe, performant
- **FastAPI** - Modern async API framework
- **SQLAlchemy** - ORM with migrations
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Meilisearch** - Full-text search
- **Redis** - Caching
- **Boto3** - AWS S3 integration
- **Click** - CLI framework
- **Prometheus** - Metrics
- **Structlog** - Structured logging

### Database
- **PostgreSQL 15+** - Primary storage
- **Replication** - Failover capability
- **TimescaleDB** - Temporal analytics (optional)

### Observability
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **OpenTelemetry** - Distributed tracing
- **Loki** - Log aggregation (optional)

### Testing
- **Pytest** - Test framework
- **Pytest-asyncio** - Async testing
- **Testcontainers** - Database containers
- **Faker** - Test data generation

---

## Development Timeline

### Phase 1: Core Infrastructure (Week 1)
- [ ] Create submodule repository
- [ ] Set up database connection pooling
- [ ] Implement ORM models
- [ ] Create Alembic migrations
- [ ] Write unit tests for database layer
- **Deliverable:** Database ready for data loading

### Phase 2: Data Loading (Week 2)
- [ ] Build JSONL loader
- [ ] Implement enrichment pipeline
- [ ] Load Phase 1-2 data (273K messages)
- [ ] Create deduplication
- [ ] Verify data integrity
- **Deliverable:** All data in database with full validation

### Phase 3: Search & Cache (Week 2-3)
- [ ] Integrate Meilisearch
- [ ] Build search API
- [ ] Implement Redis caching
- [ ] Create filter/sort capabilities
- [ ] Write search tests
- **Deliverable:** Fast search operational

### Phase 4: Reporting (Week 3)
- [ ] Build report generators
- [ ] Create pre-built reports
- [ ] Implement report rendering (JSON, CSV, HTML)
- [ ] Add scheduled reporting
- [ ] Create dashboard prototype
- **Deliverable:** Rich reporting capability

### Phase 5: Backup & Ops (Week 4)
- [ ] Implement backup manager
- [ ] Build S3 integration
- [ ] Create restore procedures
- [ ] Add monitoring/alerting
- [ ] Test disaster recovery
- **Deliverable:** Production-ready backup system

### Phase 6: API & CLI (Week 4-5)
- [ ] Build FastAPI server
- [ ] Create REST endpoints
- [ ] Implement Click CLI
- [ ] Add authentication
- [ ] Write integration tests
- **Deliverable:** Complete API and CLI interface

### Phase 7: Documentation & Deployment (Week 5)
- [ ] Write comprehensive documentation
- [ ] Create deployment guide
- [ ] Build Docker images
- [ ] Set up CI/CD pipeline
- [ ] Perform load testing
- **Deliverable:** Production-ready system

---

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| **Search latency** | <100ms | 95th percentile |
| **Data accuracy** | 100% | Checksum verification |
| **Backup success** | 99.9% | Monthly dry-run tests |
| **Recovery time** | <1 hour | Timed drills |
| **Uptime** | 99.95% | Monitoring |
| **Scalability** | 10M messages | Load testing |
| **Test coverage** | >90% | Pytest coverage |

---

## Resource Requirements

### Development Team
- 1 Backend Engineer (Python/PostgreSQL) - 5 weeks
- 1 DevOps Engineer (Backup/Ops/Deployment) - 2 weeks
- 1 QA Engineer (Testing/Verification) - 3 weeks

### Infrastructure
- PostgreSQL 15+ server
- Redis instance
- Meilisearch deployment
- S3 bucket for backups
- Local NAS for incremental backups
- Monitoring infrastructure

---

## Next Steps

1. **Immediate:** Create GitHub repository for coditect-memory-management
2. **This week:** Initialize Python project structure
3. **Next week:** Begin Phase 1 database implementation
4. **Timeline:** 5 weeks to production-ready system
5. **Parallel:** Continue extracting Phases 3-7 while building system

---

## Conclusion

Creating `coditect-memory-management` as a dedicated submodule provides:

✅ **Isolation:** Memory system independent and versioned
✅ **Reusability:** Can be used across all CODITECT projects
✅ **Scalability:** Production-grade architecture from day one
✅ **Maintainability:** Clear separation of concerns
✅ **Professionalism:** Enterprise-grade data management

**Expected investment:** ~130 engineering hours
**Expected ROI:** Invaluable for session recovery, analytics, audit trail

---

**Plan Version:** 1.0
**Date:** November 22, 2025
**Status:** Ready for Implementation Approval

