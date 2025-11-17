# CODITECT Shared Data Model Architecture

**Date:** 2025-11-16
**Purpose:** Define shared data models across all CODITECT platform components
**Status:** Design Specification
**Version:** 1.0

---

## Executive Summary

This document defines the **shared data model architecture** for the CODITECT platform, enabling consistent data structures across all 23 submodules while allowing component-specific extensions where appropriate.

**Key Principles:**
- ✅ **Shared Core Models** - User, Organization, License, Session, Project entities shared across all components
- ✅ **Component Independence** - Each component can extend shared models with specific fields
- ✅ **Event-Driven Sync** - Changes propagate through event bus for eventual consistency
- ✅ **API-First Design** - All data access through well-defined APIs, not direct database access
- ✅ **Multi-Tenancy** - All models support organization/tenant isolation

---

## Architecture Overview

### Distributed Data Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CODITECT Platform Layer                      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Shared Data Model (Core Entities)              │  │
│  │  - User, Organization, License, Session, Project          │  │
│  │  - Event, Agent, Workflow, Asset, Metric                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Data Access Layer                      │  │
│  │  - REST APIs (FastAPI)                                    │  │
│  │  - GraphQL (optional)                                     │  │
│  │  - Event Bus (RabbitMQ/NATS)                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Backend    │      │   Frontend   │      │  License     │
│  (FastAPI)   │      │   (React)    │      │  Manager     │
│              │      │              │      │              │
│  Extends:    │      │  Reads:      │      │  Extends:    │
│  - Session   │      │  - User      │      │  - License   │
│  - Workflow  │      │  - Project   │      │  - Hardware  │
└──────────────┘      └──────────────┘      └──────────────┘

        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   ERP-CRM    │      │  Installer   │      │   Analytics  │
│   (Odoo)     │      │  (Python)    │      │ (ClickHouse) │
│              │      │              │      │              │
│  Extends:    │      │  Reads:      │      │  Aggregates: │
│  - Customer  │      │  - User      │      │  - Event     │
│  - Invoice   │      │  - License   │      │  - Metric    │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

## Core Shared Entities

### 1. User

**Purpose:** Represents a human user of the CODITECT platform
**Shared Across:** All components
**Storage:** PostgreSQL (primary), cached in Redis

**Schema:**

```python
class User:
    # Identity
    id: UUID                          # Primary key
    email: str                        # Unique, indexed
    username: str                     # Unique, indexed, optional
    full_name: str
    avatar_url: Optional[str]

    # Authentication
    hashed_password: str              # bcrypt hash
    is_active: bool = True
    is_verified: bool = False
    email_verified_at: Optional[datetime]

    # Multi-tenancy
    organization_id: UUID             # FK to Organization
    role: UserRole                    # OWNER, ADMIN, MEMBER, GUEST

    # Licensing
    license_id: Optional[UUID]        # FK to License
    license_status: LicenseStatus     # ACTIVE, TRIAL, EXPIRED, NONE

    # Metadata
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    metadata: JSONB = {}              # Component-specific extensions

    # Soft delete
    deleted_at: Optional[datetime]
```

**API Endpoints:**
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/{id}` - Get user by ID
- `PATCH /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Soft delete user

**Component Extensions:**
- **Backend:** `sessions: List[Session]`, `workflows: List[Workflow]`
- **ERP-CRM:** `customer_id: Optional[UUID]`, `accounting_ref: Optional[str]`
- **Analytics:** Aggregated events, usage metrics

---

### 2. Organization

**Purpose:** Multi-tenant organization/company entity
**Shared Across:** All components
**Storage:** PostgreSQL (primary), cached in Redis

**Schema:**

```python
class Organization:
    # Identity
    id: UUID
    name: str                         # Company name
    slug: str                         # Unique URL-safe identifier
    domain: Optional[str]             # Email domain for SSO

    # Branding
    logo_url: Optional[str]
    primary_color: Optional[str]      # Hex color

    # Subscription
    plan: SubscriptionPlan            # FREE, PRO, ENTERPRISE
    subscription_status: str          # ACTIVE, TRIAL, SUSPENDED, CANCELED
    trial_ends_at: Optional[datetime]
    subscription_ends_at: Optional[datetime]

    # Limits
    max_users: int = 5
    max_projects: int = 10
    max_storage_gb: int = 10

    # Billing
    billing_email: Optional[str]
    tax_id: Optional[str]

    # Metadata
    created_at: datetime
    updated_at: datetime
    metadata: JSONB = {}

    # Relations
    owner_id: UUID                    # FK to User
    users: List[User]
    licenses: List[License]
```

**API Endpoints:**
- `GET /api/v1/organizations` - List user's organizations
- `POST /api/v1/organizations` - Create organization
- `GET /api/v1/organizations/{id}` - Get organization details
- `PATCH /api/v1/organizations/{id}` - Update organization
- `DELETE /api/v1/organizations/{id}` - Delete organization

---

### 3. License

**Purpose:** Software license and entitlements
**Shared Across:** license-manager, license-server, backend, installer
**Storage:** PostgreSQL (primary), Redis (cache)

**Schema:**

```python
class License:
    # Identity
    id: UUID
    license_key: str                  # Unique, indexed
    license_type: LicenseType         # TRIAL, PRO, ENTERPRISE, PILOT

    # Ownership
    organization_id: UUID             # FK to Organization
    user_id: UUID                     # FK to User (assignee)

    # Status
    status: LicenseStatus             # ACTIVE, SUSPENDED, EXPIRED, REVOKED
    activated_at: Optional[datetime]
    expires_at: Optional[datetime]
    last_validated_at: Optional[datetime]

    # Entitlements
    max_activations: int = 3
    current_activations: int = 0
    features: List[str] = []          # Feature flags

    # Hardware Binding
    hardware_fingerprints: List[str] = []

    # Metadata
    created_at: datetime
    updated_at: datetime
    metadata: JSONB = {}

    # Telemetry (opt-in)
    telemetry_enabled: bool = False
    last_heartbeat_at: Optional[datetime]
```

**API Endpoints:**
- `POST /api/v1/licenses/validate` - Validate license key
- `POST /api/v1/licenses/activate` - Activate license on hardware
- `POST /api/v1/licenses/deactivate` - Deactivate license
- `GET /api/v1/licenses/{id}` - Get license details
- `PATCH /api/v1/licenses/{id}` - Update license

---

### 4. Session

**Purpose:** User session and state persistence
**Shared Across:** Backend, frontend, CLI
**Storage:** FoundationDB (multi-tenant), Redis (cache)

**Schema:**

```python
class Session:
    # Identity
    id: UUID
    session_token: str                # Unique, indexed

    # User Context
    user_id: UUID                     # FK to User
    organization_id: UUID             # FK to Organization

    # Session Data
    project_id: Optional[UUID]        # Current project
    workspace_state: JSONB = {}       # UI state, open files, etc.
    agent_state: JSONB = {}           # Agent memory, context

    # Session Management
    created_at: datetime
    expires_at: datetime
    last_activity_at: datetime
    is_active: bool = True

    # Device Info
    device_fingerprint: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
```

**API Endpoints:**
- `POST /api/v1/sessions` - Create session
- `GET /api/v1/sessions/{id}` - Get session
- `PATCH /api/v1/sessions/{id}` - Update session state
- `DELETE /api/v1/sessions/{id}` - End session
- `POST /api/v1/sessions/{id}/heartbeat` - Keep-alive

---

### 5. Project

**Purpose:** Development project / workspace
**Shared Across:** Backend, frontend, CLI, docs
**Storage:** PostgreSQL (metadata), FoundationDB (state)

**Schema:**

```python
class Project:
    # Identity
    id: UUID
    name: str
    slug: str                         # URL-safe identifier
    description: Optional[str]

    # Ownership
    organization_id: UUID             # FK to Organization
    owner_id: UUID                    # FK to User

    # Project Type
    project_type: ProjectType         # WEB_APP, API, CLI, MOBILE, ML, OTHER
    framework: Optional[str]          # Next.js, FastAPI, etc.
    language: Optional[str]           # Python, TypeScript, etc.

    # Repository
    git_url: Optional[str]
    git_branch: Optional[str]

    # Status
    status: ProjectStatus             # ACTIVE, ARCHIVED, DELETED

    # Metadata
    created_at: datetime
    updated_at: datetime
    last_accessed_at: Optional[datetime]
    metadata: JSONB = {}

    # Relations
    members: List[User]               # Team members
    workflows: List[Workflow]
```

**API Endpoints:**
- `GET /api/v1/projects` - List projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/{id}` - Get project
- `PATCH /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Archive/delete project

---

### 6. Event

**Purpose:** System events and audit trail
**Shared Across:** All components (event sourcing)
**Storage:** ClickHouse (time-series), PostgreSQL (critical events)

**Schema:**

```python
class Event:
    # Identity
    id: UUID
    event_type: str                   # user.login, license.activated, etc.
    event_version: str = "1.0"

    # Context
    user_id: Optional[UUID]
    organization_id: Optional[UUID]
    session_id: Optional[UUID]

    # Event Data
    payload: JSONB                    # Event-specific data
    metadata: JSONB = {}              # Request ID, IP, user agent, etc.

    # Timestamp
    occurred_at: datetime             # When event happened
    recorded_at: datetime             # When event was recorded

    # Processing
    processed: bool = False
    processed_at: Optional[datetime]
```

**API Endpoints:**
- `POST /api/v1/events` - Publish event
- `GET /api/v1/events` - Query events (admin only)
- `GET /api/v1/events/audit-log` - Get audit log

---

### 7. Agent

**Purpose:** AI agent instance and state
**Shared Across:** Framework, backend, CLI
**Storage:** FoundationDB (state), PostgreSQL (metadata)

**Schema:**

```python
class Agent:
    # Identity
    id: UUID
    agent_type: str                   # orchestrator, codebase-analyzer, etc.
    agent_version: str

    # Context
    user_id: UUID
    organization_id: UUID
    project_id: Optional[UUID]
    session_id: Optional[UUID]

    # State
    state: AgentState                 # IDLE, RUNNING, PAUSED, COMPLETED, FAILED
    memory: JSONB = {}                # Agent memory/context
    checkpoint: Optional[str]         # State checkpoint reference

    # Execution
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error: Optional[str]

    # Metrics
    tasks_completed: int = 0
    tokens_used: int = 0
    cost_usd: Decimal = Decimal("0.00")
```

---

### 8. Workflow

**Purpose:** Multi-step automation workflow
**Shared Across:** Backend, automation, framework
**Storage:** PostgreSQL (definition), FoundationDB (execution state)

**Schema:**

```python
class Workflow:
    # Identity
    id: UUID
    name: str
    description: Optional[str]

    # Ownership
    organization_id: UUID
    created_by: UUID                  # FK to User
    project_id: Optional[UUID]

    # Definition
    steps: List[WorkflowStep]         # Ordered steps
    triggers: List[WorkflowTrigger]   # What starts this workflow

    # State
    status: WorkflowStatus            # DRAFT, ACTIVE, PAUSED, COMPLETED

    # Execution Stats
    executions: int = 0
    last_execution_at: Optional[datetime]
    average_duration_seconds: Optional[float]

    # Metadata
    created_at: datetime
    updated_at: datetime
```

---

## Data Consistency Patterns

### Event-Driven Architecture

All data changes publish events to the event bus for cross-component synchronization:

```python
# Example: User updates their profile
@app.patch("/users/{user_id}")
async def update_user(user_id: UUID, data: UserUpdate):
    # 1. Update database
    user = await db.users.update(user_id, data)

    # 2. Publish event
    await event_bus.publish(Event(
        event_type="user.updated",
        user_id=user_id,
        organization_id=user.organization_id,
        payload={"changes": data.dict(exclude_unset=True)},
        metadata={"request_id": request_id}
    ))

    # 3. Invalidate cache
    await cache.delete(f"user:{user_id}")

    return user

# Other components subscribe to user.updated
@event_bus.subscribe("user.updated")
async def sync_user_to_erp(event: Event):
    """ERP-CRM component syncs user to Odoo"""
    user_id = event.user_id
    changes = event.payload["changes"]
    await odoo_client.update_user(user_id, changes)
```

---

## Database Strategy

### Primary Storage (PostgreSQL)

**Used for:**
- Structured relational data (User, Organization, License, Project)
- Strong consistency requirements
- Complex queries and joins
- Transactional integrity

**Schema Organization:**

```sql
-- Shared schema for core models
CREATE SCHEMA coditect_shared;

-- Component-specific schemas
CREATE SCHEMA coditect_backend;
CREATE SCHEMA coditect_erp;
CREATE SCHEMA coditect_analytics;

-- Core shared tables
CREATE TABLE coditect_shared.users (...);
CREATE TABLE coditect_shared.organizations (...);
CREATE TABLE coditect_shared.licenses (...);
CREATE TABLE coditect_shared.projects (...);

-- Component-specific extensions
CREATE TABLE coditect_backend.sessions (...);
CREATE TABLE coditect_erp.customers (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES coditect_shared.users(id),
    ...
);
```

### Multi-Tenant Storage (FoundationDB)

**Used for:**
- Session state and agent memory
- High-throughput writes
- Multi-tenant key-value data
- Strong consistency with low latency

**Key Design:**

```python
# Tenant isolation built into key structure
/org/{org_id}/sessions/{session_id} → session_data
/org/{org_id}/agents/{agent_id}/state → agent_state
/org/{org_id}/projects/{project_id}/files → file_metadata
```

### Time-Series Storage (ClickHouse)

**Used for:**
- Events and audit logs
- Usage metrics
- Analytics aggregations
- High-volume writes

**Schema:**

```sql
CREATE TABLE events (
    id UUID,
    event_type String,
    user_id Nullable(UUID),
    organization_id Nullable(UUID),
    occurred_at DateTime,
    payload String  -- JSON
) ENGINE = MergeTree()
ORDER BY (organization_id, occurred_at);
```

### Cache Layer (Redis)

**Used for:**
- Session tokens
- User/organization cache
- License validation cache
- Rate limiting

**Key Patterns:**

```
user:{user_id} → {user_json}  [TTL: 15 min]
org:{org_id} → {org_json}     [TTL: 15 min]
license:{key} → {license_json} [TTL: 1 hour]
session:{token} → {session_id} [TTL: expires_at]
```

---

## API Design Principles

### RESTful API Conventions

All components expose REST APIs following these patterns:

```
GET    /api/v1/{resource}              # List (paginated)
POST   /api/v1/{resource}              # Create
GET    /api/v1/{resource}/{id}         # Read
PATCH  /api/v1/{resource}/{id}         # Update (partial)
PUT    /api/v1/{resource}/{id}         # Replace (full)
DELETE /api/v1/{resource}/{id}         # Delete (soft or hard)

# Relationships
GET    /api/v1/{resource}/{id}/{sub}   # Get related items
POST   /api/v1/{resource}/{id}/{sub}   # Add relationship
DELETE /api/v1/{resource}/{id}/{sub}/{sub_id}  # Remove relationship
```

### Authentication

All API requests require authentication:

```
Authorization: Bearer {jwt_token}
X-Organization-ID: {org_id}  # Optional, for multi-org users
```

### Response Format

```json
{
  "data": {...},
  "meta": {
    "request_id": "req_123",
    "timestamp": "2025-11-16T12:00:00Z"
  }
}
```

### Error Format

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found",
    "details": {
      "user_id": "uuid-here"
    },
    "request_id": "req_123"
  }
}
```

---

## Component-Specific Extensions

### Backend (coditect-cloud-backend)

**Extends:**
- `User.metadata` → `{"backend_settings": {...}}`
- `Session` → Full implementation with agent state
- `Workflow` → Execution engine

### ERP-CRM (az1.ai-CODITECT-ERP-CRM)

**Extends:**
- `Organization` → Customer in Odoo
- `User` → Contact in Odoo
- `User.metadata` → `{"odoo_partner_id": 123}`

**Mapping:**

```python
# CODITECT Organization → Odoo Company
class OdooOrganization(Organization):
    odoo_company_id: int
    accounting_ref: str
    tax_id: str

# CODITECT User → Odoo Partner (Contact)
class OdooUser(User):
    odoo_partner_id: int
    customer_ref: str
```

### Analytics (coditect-analytics)

**Aggregates:**
- Events → Usage metrics
- Sessions → Active users, session duration
- Workflows → Success rate, average duration

**Materialized Views:**

```sql
-- Daily active users by organization
CREATE MATERIALIZED VIEW daily_active_users AS
SELECT
    organization_id,
    DATE(occurred_at) as date,
    COUNT(DISTINCT user_id) as dau
FROM events
WHERE event_type IN ('user.login', 'session.created')
GROUP BY organization_id, DATE(occurred_at);
```

### License Components

**license-manager extends License:**

```python
class ClientLicense(License):
    """Client-side license with offline validation"""
    offline_token: str  # Signed JWT for offline validation
    grace_period_days: int = 3
    last_online_check: datetime
```

**license-server manages License:**
- Activation tracking
- Telemetry collection
- Admin operations

---

## Migration Strategy

### Phase 1: Core Shared Models (Week 1-2)

1. Create `coditect_shared` schema in PostgreSQL
2. Deploy User, Organization, License tables
3. Migrate existing users/orgs to shared schema
4. Update backend to use shared models

### Phase 2: Component Integration (Week 3-4)

1. Update all components to reference shared models
2. Implement event bus for data sync
3. Deploy FoundationDB for session state
4. Migrate sessions to FoundationDB

### Phase 3: Analytics & Observability (Week 5-6)

1. Deploy ClickHouse for events
2. Migrate event logging to ClickHouse
3. Create materialized views for analytics
4. Deploy Grafana dashboards

---

## Data Access Patterns

### Read-Heavy Operations

Use caching aggressively:

```python
@cache(ttl=900)  # 15 minutes
async def get_user(user_id: UUID) -> User:
    return await db.query(User).filter_by(id=user_id).first()
```

### Write Operations

Invalidate cache on write:

```python
async def update_user(user_id: UUID, data: dict):
    user = await db.users.update(user_id, data)
    await cache.delete(f"user:{user_id}")
    await event_bus.publish(Event(...))
    return user
```

### Cross-Component Queries

Use GraphQL federation for cross-component queries:

```graphql
query GetUserWithProjects($userId: UUID!) {
  user(id: $userId) {        # From backend
    id
    email
    organization {           # From backend
      id
      name
    }
    projects {              # From backend
      id
      name
      status
    }
    erpCustomer {           # From ERP-CRM
      customerId
      accountingRef
      invoices {
        id
        total
      }
    }
  }
}
```

---

## Security & Privacy

### Data Isolation

- Every query includes `organization_id` filter (Row-Level Security)
- FoundationDB keys include org prefix
- Cache keys include org prefix
- Cross-org data access blocked at API level

### Encryption

- At rest: PostgreSQL TLS, FDB encryption
- In transit: HTTPS/TLS for all APIs
- Secrets: Google Cloud Secret Manager

### Audit Trail

All data modifications logged as events:

```python
Event(
    event_type="user.updated",
    user_id=current_user.id,
    organization_id=org_id,
    payload={
        "target_user_id": target_user.id,
        "changes": {"email": "new@example.com"},
        "previous_values": {"email": "old@example.com"}
    },
    metadata={"ip": request.client.host, "user_agent": ...}
)
```

---

## Future Enhancements

### GraphQL Federation

Unified API across all components:

```
┌─────────────────┐
│  GraphQL Gateway│
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
┌───▼───┐ ┌──▼──┐ ┌───▼───┐ ┌──▼──┐
│Backend│ │ ERP │ │License│ │ CLI │
└───────┘ └─────┘ └───────┘ └─────┘
```

### Real-Time Subscriptions

WebSocket subscriptions for live updates:

```graphql
subscription OnProjectUpdate($projectId: UUID!) {
  projectUpdated(projectId: $projectId) {
    id
    status
    updatedBy {
      id
      email
    }
  }
}
```

### Data Warehouse

Long-term analytics and reporting:

```
ClickHouse (events) → BigQuery (data warehouse) → Looker (BI)
```

---

## Implementation Checklist

### Shared Schema Setup

- [ ] Create `coditect_shared` PostgreSQL schema
- [ ] Deploy User, Organization, License, Project tables
- [ ] Create indexes for common queries
- [ ] Setup Row-Level Security policies

### API Layer

- [ ] Define OpenAPI specs for shared models
- [ ] Implement REST API endpoints
- [ ] Add authentication middleware
- [ ] Add multi-tenancy filters
- [ ] Add input validation (Pydantic)

### Event Bus

- [ ] Setup RabbitMQ/NATS cluster
- [ ] Define event schemas
- [ ] Implement event publishers
- [ ] Implement event subscribers
- [ ] Add dead letter queue for failed events

### Caching

- [ ] Setup Redis cluster
- [ ] Implement cache decorators
- [ ] Define cache invalidation strategies
- [ ] Monitor cache hit rates

### Documentation

- [ ] API documentation (Swagger/Redoc)
- [ ] Data model diagrams (ERD)
- [ ] Integration guides per component
- [ ] Migration runbooks

---

## Conclusion

This shared data model architecture enables:

✅ **Consistency** - Same User/Org/License model across all components
✅ **Flexibility** - Components can extend shared models with metadata
✅ **Scalability** - Event-driven sync, caching, time-series storage
✅ **Multi-Tenancy** - Built-in organization isolation
✅ **Auditability** - Complete event trail for compliance

**Next Steps:**
1. Review this architecture with engineering team
2. Prioritize Phase 1 implementation (Weeks 1-2)
3. Create database migration scripts
4. Update component APIs to use shared models
5. Deploy event bus infrastructure

---

**Author:** Claude Code
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
**Related Documents:**
- `CODITECT-MASTER-ORCHESTRATION-PLAN.md`
- `CODITECT-ROLLOUT-MASTER-PLAN.md`
- `SUBMODULE-MIGRATION-PLAN-UPDATED.md`
