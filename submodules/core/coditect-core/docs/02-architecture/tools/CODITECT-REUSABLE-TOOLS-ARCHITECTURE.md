# AZ1.AI CODITECT Reusable Tools Architecture

**Strategic Framework for Building Tools Once, Using Everywhere**

**Document Version:** 1.0
**Last Updated:** 2025-11-15
**Document Owner:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
**Status:** FOUNDATIONAL ARCHITECTURE

---

## Executive Summary

This document establishes the architectural principles and patterns for creating **reusable, multi-stakeholder tools** within the AZ1.AI CODITECT ecosystem. Every tool we build should serve not just immediate internal needs, but be designed from the ground up for reuse across:

- **Internal Users** (AZ1.AI team members)
- **Customers** (CODITECT platform subscribers)
- **Vendors** (Technology and service partners)
- **Consultants** (Implementation and advisory partners)
- **Affiliates** (Strategic partners and resellers)
- **Advisors** (Board members, technical advisors)
- **Auditors** (Security, compliance, financial auditors)
- **Future User Groups** (yet to be defined)

**Core Principle:** **Build Once, Use Everywhere, Scale Infinitely**

---

## Table of Contents

1. [Strategic Rationale](#strategic-rationale)
2. [Stakeholder Groups & Use Cases](#stakeholder-groups--use-cases)
3. [Tool Design Principles](#tool-design-principles)
4. [Reusable Tools Catalog](#reusable-tools-catalog)
5. [Tool Abstraction Patterns](#tool-abstraction-patterns)
6. [Multi-Tenancy Architecture](#multi-tenancy-architecture)
7. [Permission & Access Control](#permission--access-control)
8. [Tool Distribution & Packaging](#tool-distribution--packaging)
9. [Documentation Standards](#documentation-standards)
10. [Versioning & Backward Compatibility](#versioning--backward-compatibility)
11. [Tool Evolution Roadmap](#tool-evolution-roadmap)

---

## Strategic Rationale

### Why Build Reusable Tools?

**Economic Benefits:**
- **10x ROI** - Build once, amortize cost across all user groups
- **Reduced Maintenance** - Single codebase for all stakeholders
- **Faster Time-to-Market** - Internal tools become products immediately

**Competitive Advantages:**
- **Network Effects** - More users = better tools = more users
- **Ecosystem Lock-In** - Tools integrate with CODITECT platform
- **Market Differentiation** - Tooling as a competitive moat

**Operational Efficiency:**
- **Consistent UX** - Same tools everywhere reduce training costs
- **Unified Support** - Single support model for all users
- **Centralized Updates** - Fix once, deploy everywhere

### Current State: One-Off Tools (Anti-Pattern)

**Problems with one-off tools:**
```
Internal Tool (v1) → Customer needs it → Rebuild from scratch (v2)
                  → Consultant needs it → Rebuild again (v3)
                  → Auditor needs it → Rebuild again (v4)

Result: 4 tools, 4 codebases, 4x maintenance cost, inconsistent UX
```

### Desired State: Reusable Tools (CODITECT Pattern)

**Reusable tool lifecycle:**
```
Reusable Tool (v1.0) → Internal use (validates tool)
                    → Abstract & generalize (v1.1)
                    → Customer release (v2.0)
                    → Multi-stakeholder use (v2.1+)

Result: 1 tool, 1 codebase, all stakeholders, consistent UX
```

---

## Stakeholder Groups & Use Cases

### 1. Internal Users (AZ1.AI Team)

**Who:** Engineers, product managers, designers, executives

**Use Cases:**
- Master project orchestration (what we built today)
- Git automation for non-Git experts
- Session management and context tracking
- Cross-project status reporting
- Automated onboarding for new team members

**Access Level:** Full access, all features, internal-only features enabled

---

### 2. Customers (CODITECT Platform Subscribers)

**Who:** Individual developers, teams, businesses using CODITECT

**User Tiers:**
- **Individual** - Solo developers, freelancers
- **Team** - 2-10 person teams
- **Business** - 10-50 person companies
- **Enterprise** - 50+ person organizations

**Use Cases:**
- Master project orchestration for their own multi-repo projects
- Git automation integrated with CODITECT workflows
- Session management for AI-assisted development
- Project status reporting and analytics
- Team collaboration and coordination

**Access Level:** Tiered access based on subscription level

**Customization Needs:**
- White-labeling options (Enterprise tier)
- Custom branding (Business tier and above)
- Integration with their own tools (APIs, webhooks)

---

### 3. Vendors (Technology & Service Partners)

**Who:** Cloud providers, tool vendors, service integrators

**Use Cases:**
- Integration testing with CODITECT platform
- Monitoring their service status within CODITECT
- Analytics on usage of their services
- Support ticket integration
- SLA compliance tracking

**Access Level:** Limited to vendor-specific data, no customer data access

**Examples:**
- GCP monitoring their infrastructure performance
- GitHub monitoring git operations
- Stripe monitoring payment processing
- Auth0 monitoring authentication flows

---

### 4. Consultants (Implementation & Advisory Partners)

**Who:** Implementation partners, fractional CTOs, technical advisors

**Use Cases:**
- Multi-client project management (one consultant, many clients)
- Onboarding clients to CODITECT
- Auditing client codebases
- Generating reports for clients
- Training and enablement

**Access Level:** Scoped access to specific client projects (with client permission)

**Billing Model:**
- Consultants pay for CODITECT Pro license
- Clients grant consultants temporary access
- Usage tracked for billing and compliance

---

### 5. Affiliates (Strategic Partners & Resellers)

**Who:** Resellers, system integrators, agency partners

**Use Cases:**
- White-labeled CODITECT offerings
- Multi-client portfolio management
- Reseller analytics and reporting
- Lead generation and tracking
- Commission tracking

**Access Level:** Partner portal with aggregated analytics

**Revenue Share Model:**
- Affiliates earn commission on referred customers
- Tools track attribution and payouts
- Analytics show pipeline and conversion metrics

---

### 6. Advisors (Board Members, Technical Advisors)

**Who:** Board members, advisors, investors, mentors

**Use Cases:**
- Executive dashboards (high-level metrics)
- Strategic insights (growth, retention, usage)
- Compliance and governance reports
- Competitive analysis
- Risk assessment

**Access Level:** Read-only access to aggregated data (no PII, no customer data)

**Confidentiality:**
- All data anonymized
- NDA-protected dashboards
- Audit logs for all advisor access

---

### 7. Auditors (Security, Compliance, Financial)

**Who:** Security auditors, compliance auditors, financial auditors

**Use Cases:**
- **Security Auditors** - Code analysis, vulnerability scanning, penetration testing
- **Compliance Auditors** - SOC 2, ISO 27001, GDPR, CCPA compliance verification
- **Financial Auditors** - Revenue recognition, billing accuracy, ARR validation

**Access Level:** Time-limited, scoped access with full audit logging

**Audit Trail:**
- Every auditor action logged
- Immutable audit logs
- Regular attestation reports

---

### 8. Future User Groups

**Potential Future Groups:**
- **Educators** - Using CODITECT for teaching software development
- **Students** - Learning AI-first development
- **Open Source Projects** - Free tier for OSS contributors
- **Non-Profits** - Discounted/free access for social impact
- **Government** - Public sector implementations (with compliance requirements)
- **Research Institutions** - Academic research on AI-assisted development

**Design Implication:** Architecture must be flexible enough to support future personas

---

## Tool Design Principles

### 1. Multi-Tenancy by Default

**Every tool must support multiple tenants from day one.**

```python
# BAD: Single-tenant design
def get_projects():
    return db.query("SELECT * FROM projects")

# GOOD: Multi-tenant design
def get_projects(tenant_id: str):
    return db.query("SELECT * FROM projects WHERE tenant_id = ?", tenant_id)
```

**Implementation:**
- Tenant ID in every database table
- Row-level security in PostgreSQL
- API requests always include tenant context
- No cross-tenant data leakage

---

### 2. Permission-Based Access Control

**Role-Based Access Control (RBAC) + Attribute-Based Access Control (ABAC)**

```python
# Permission model
class Permission:
    resource: str        # e.g., "project", "user", "billing"
    action: str          # e.g., "read", "write", "delete", "admin"
    scope: str           # e.g., "own", "team", "organization", "global"
    conditions: dict     # e.g., {"ip_whitelist": [...], "time_range": [...]}

# Permission check
@require_permission(resource="project", action="write", scope="team")
def update_project(tenant_id: str, project_id: str, data: dict):
    # Only executes if user has team-level write permission
    pass
```

**Standard Roles:**
- **Viewer** - Read-only access
- **Editor** - Read + write access
- **Admin** - Full access within scope
- **Owner** - Full access + billing + user management
- **Support** - AZ1.AI support team (time-limited access)
- **Auditor** - Read-only with full audit trail

---

### 3. Configurable vs. Hardcoded

**Use configuration files, not hardcoded values.**

```yaml
# config/stakeholder-tiers.yaml
stakeholder_tiers:
  internal:
    name: "AZ1.AI Internal"
    features:
      - all
    rate_limits:
      api_calls_per_minute: unlimited
      projects: unlimited

  customer_individual:
    name: "Individual Developer"
    features:
      - master_project_orchestration
      - git_automation
      - session_management
    rate_limits:
      api_calls_per_minute: 100
      projects: 10

  customer_enterprise:
    name: "Enterprise Customer"
    features:
      - all_customer_features
      - white_labeling
      - sso
      - dedicated_support
    rate_limits:
      api_calls_per_minute: 10000
      projects: unlimited

  consultant:
    name: "Consultant"
    features:
      - multi_client_management
      - client_reporting
      - time_tracking
    rate_limits:
      api_calls_per_minute: 500
      projects: 50  # across all clients
```

**Benefits:**
- Change tier limits without code changes
- A/B test feature access
- Quickly create new tiers for new stakeholder groups

---

### 4. API-First Design

**Every tool must have a REST API + optional CLI/GUI.**

```
Tool Architecture:
  Core Logic (Python library)
      ↓
  REST API (FastAPI)
      ↓
  ┌─────────┬──────────┬──────────┐
  │   CLI   │   Web    │  Mobile  │
  │ (Click) │ (React)  │  (Swift) │
  └─────────┴──────────┴──────────┘
```

**Why API-First:**
- CLI can be built on API
- Web UI can be built on API
- Mobile app can be built on API
- Customers can build their own integrations
- Third-party tools can integrate

**API Requirements:**
- OpenAPI/Swagger documentation
- Versioned endpoints (/v1/, /v2/, etc.)
- Rate limiting
- Authentication (OAuth 2.0 + API keys)
- Webhooks for events

---

### 5. Self-Service & Automation

**Minimize human involvement in common workflows.**

```python
# Example: Self-service onboarding
@app.post("/api/v1/onboarding/start")
async def start_onboarding(user_id: str):
    """
    Automated onboarding flow:
    1. Create tenant
    2. Setup default project
    3. Send welcome email with credentials
    4. Schedule onboarding call (optional)
    5. Provision resources
    6. Grant initial access
    """
    tenant = create_tenant(user_id)
    project = create_default_project(tenant.id)
    send_welcome_email(user_id, tenant, project)

    # No human intervention required!

    return {"tenant_id": tenant.id, "project_id": project.id}
```

**Self-Service Capabilities:**
- User registration
- Payment/billing
- Tier upgrades/downgrades
- Team member invitations
- Access grants for consultants/auditors
- Offboarding and data export

---

### 6. Observable & Debuggable

**Every tool must have comprehensive logging, metrics, and tracing.**

```python
from opentelemetry import trace, metrics

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

project_creation_counter = meter.create_counter(
    "coditect.projects.created",
    description="Number of projects created"
)

@tracer.start_as_current_span("create_project")
def create_project(tenant_id: str, name: str):
    span = trace.get_current_span()
    span.set_attribute("tenant_id", tenant_id)
    span.set_attribute("project_name", name)

    logger.info(f"Creating project", extra={
        "tenant_id": tenant_id,
        "project_name": name,
        "stakeholder_type": get_stakeholder_type(tenant_id)
    })

    # ... create project ...

    project_creation_counter.add(1, {"stakeholder_type": get_stakeholder_type(tenant_id)})

    return project
```

**Observability Stack:**
- **Logs** - Structured JSON logs (Loki/CloudWatch)
- **Metrics** - Prometheus + Grafana
- **Traces** - Jaeger/Zipkin (OpenTelemetry)
- **Dashboards** - Per stakeholder group

---

### 7. Secure by Default

**Security is not optional.**

```python
# Security checklist for every tool:
✅ Authentication required (no anonymous access)
✅ Authorization checks on every operation
✅ Input validation and sanitization
✅ SQL injection prevention (parameterized queries)
✅ XSS prevention (output escaping)
✅ CSRF protection
✅ Rate limiting to prevent abuse
✅ Audit logging for sensitive operations
✅ Data encryption at rest and in transit
✅ Secrets management (never hardcoded)
✅ Dependency scanning for vulnerabilities
✅ Regular security audits
```

**Compliance:**
- SOC 2 Type II
- GDPR compliance (data privacy)
- CCPA compliance (California residents)
- HIPAA compliance (if healthcare customers)
- ISO 27001 certification

---

### 8. Documentation as Code

**Documentation lives with the code, not in a separate wiki.**

```python
# Example: API endpoint with comprehensive documentation
@app.post("/api/v1/projects",
    summary="Create a new project",
    description="""
    Creates a new project within the specified tenant.

    **Permissions Required:** `project:write:team`

    **Rate Limit:** 100 projects per hour per tenant

    **Stakeholder Access:**
    - Internal: Unlimited projects
    - Customer (Individual): Max 10 projects
    - Customer (Enterprise): Unlimited projects
    - Consultant: Max 50 projects across all clients

    **Audit:** Project creation is logged for compliance
    """,
    responses={
        201: {"description": "Project created successfully"},
        400: {"description": "Invalid request (e.g., project limit reached)"},
        403: {"description": "Insufficient permissions"},
        429: {"description": "Rate limit exceeded"}
    }
)
async def create_project(request: CreateProjectRequest):
    pass
```

**Documentation Types:**
- **API Docs** - Auto-generated from OpenAPI spec
- **CLI Docs** - Auto-generated from Click/Typer
- **User Guides** - Markdown in `/docs` directory
- **Architecture Docs** - C4 diagrams, ADRs
- **Runbooks** - For operations and support

---

## Reusable Tools Catalog

### Tools We've Built (Ready for Multi-Stakeholder Use)

#### 1. Master Project Orchestration

**Current State:** Built for internal AZ1.AI rollout
**Reusable For:** All stakeholder groups

**Abstraction Path:**
```
v1.0 (Today)     → Internal use only (coditect-rollout-master)
v1.1 (Week 2)    → Abstract tenant-specific logic
v2.0 (Month 2)   → Customer beta (invite-only)
v2.5 (Month 4)   → Consultant/advisor access
v3.0 (Month 6)   → General availability for all customers
```

**Required Changes for Reusability:**
- [x] Git submodule support ✅ (already implemented)
- [ ] Multi-tenancy (tenant_id in all operations)
- [ ] Permission-based access control
- [ ] White-labeling for enterprise customers
- [ ] Usage tracking and billing integration
- [ ] Self-service project creation UI
- [ ] Template marketplace (pre-built project templates)

**Stakeholder-Specific Features:**
- **Internal** - Unlimited projects, advanced debugging
- **Customers** - Project limits by tier, standard support
- **Consultants** - Multi-client view, client reporting
- **Advisors** - Portfolio-level analytics (read-only)

---

#### 2. Git Automation (coditect-git-helper.py)

**Current State:** CLI tool for session-based Git workflows
**Reusable For:** Customers, consultants, internal

**Abstraction Path:**
```
v1.0 (Today)     → CLI tool, single user
v1.1 (Week 1)    → Add tenant context, multi-user support
v2.0 (Month 1)   → Web UI for non-CLI users
v2.5 (Month 3)   → GitHub App for seamless integration
v3.0 (Month 5)   → Support GitLab, Bitbucket, Azure DevOps
```

**Required Changes:**
- [ ] Multi-tenant support (track sessions per tenant)
- [ ] Web UI (for non-technical users)
- [ ] OAuth integration with GitHub/GitLab
- [ ] Team collaboration (shared sessions)
- [ ] Session analytics (time spent, commits per session)

**Stakeholder-Specific Features:**
- **Internal** - Unlimited sessions, advanced branching strategies
- **Customers** - Session history, team collaboration
- **Consultants** - Client session summaries, billable hours tracking

---

#### 3. Session Management & MEMORY-CONTEXT

**Current State:** Directory-based session export system
**Reusable For:** All stakeholder groups

**Abstraction Path:**
```
v1.0 (Today)     → File-based session exports
v1.1 (Week 1)    → Cloud-backed session storage (S3/GCS)
v2.0 (Month 2)   → Session search and retrieval API
v2.5 (Month 4)   → AI-powered session insights
v3.0 (Month 6)   → Cross-project session analytics
```

**Required Changes:**
- [ ] Cloud storage backend (S3/GCS)
- [ ] Session metadata database (PostgreSQL)
- [ ] Full-text search (Elasticsearch/Typesense)
- [ ] Session sharing (export to PDF, share link)
- [ ] Session templates (reusable session structures)

**Stakeholder-Specific Features:**
- **Internal** - Unlimited storage, AI insights
- **Customers** - Storage limits by tier, basic search
- **Consultants** - Client session reports
- **Auditors** - Read-only access to audit trail sessions

---

#### 4. Project Status Reporting (status-report.py)

**Current State:** CLI script for cross-project status
**Reusable For:** All stakeholder groups

**Abstraction Path:**
```
v1.0 (Today)     → CLI script, single project
v1.1 (Week 1)    → Multi-project, multi-tenant support
v2.0 (Month 1)   → Web dashboard with visualizations
v2.5 (Month 3)   → Real-time status updates (WebSockets)
v3.0 (Month 5)   → Customizable dashboards per stakeholder
```

**Required Changes:**
- [ ] Multi-tenant data isolation
- [ ] Real-time metrics collection
- [ ] Web dashboard (React + GraphQL)
- [ ] Customizable widgets
- [ ] Export to PDF/Excel
- [ ] Scheduled reports (email, Slack)

**Stakeholder-Specific Dashboards:**
- **Internal** - All metrics, debugging info
- **Customers** - Project health, velocity, blockers
- **Consultants** - Multi-client portfolio view
- **Advisors** - High-level KPIs (growth, retention)
- **Auditors** - Compliance metrics, audit readiness

---

#### 5. Automated Onboarding (coditect-setup.py)

**Current State:** Script for initial CODITECT setup
**Reusable For:** Customers, consultants, vendors

**Abstraction Path:**
```
v1.0 (Today)     → Manual execution, single user
v1.1 (Week 2)    → Self-service web-based onboarding
v2.0 (Month 1)   → Automated provisioning (API-driven)
v2.5 (Month 3)   → Interactive tutorials (in-app guidance)
v3.0 (Month 6)   → AI-assisted onboarding (chatbot)
```

**Required Changes:**
- [ ] Web-based onboarding flow
- [ ] Tenant provisioning automation
- [ ] Payment integration (Stripe)
- [ ] License acceptance tracking
- [ ] Onboarding analytics (drop-off points)

**Stakeholder-Specific Onboarding:**
- **Customers** - Self-service, guided tutorials
- **Consultants** - Bulk client onboarding
- **Vendors** - Integration-specific setup
- **Enterprise** - Custom onboarding with CSM

---

### Tools to Build (Prioritized for Reusability)

#### 6. Multi-Tenant Admin Panel

**Priority:** P0 (Required for customer rollout)

**Capabilities:**
- User management (invite, remove, role changes)
- Billing management (upgrade, downgrade, cancel)
- Usage analytics (API calls, storage, compute)
- Audit logs (who did what, when)
- Support ticket integration
- Feature flag management

**Stakeholder Access:**
- **Internal (AZ1.AI Admin)** - Manage all tenants
- **Customer (Owner)** - Manage their own tenant
- **Consultant** - View client tenants (read-only)

---

#### 7. Agent Marketplace Integration

**Priority:** P1 (Competitive differentiator)

**Capabilities:**
- Browse and install AI agents
- Agent ratings and reviews
- Agent usage analytics
- Custom agent development
- Agent sharing within organization

**Stakeholder Access:**
- **Internal** - All agents, alpha/beta agents
- **Customers** - Public agents + org-private agents
- **Consultants** - Client-specific agent recommendations

---

#### 8. Workflow Analyzer Integration

**Priority:** P1 (Leverage existing R&D)

**Capabilities:**
- Analyze development workflows
- Identify bottlenecks
- Suggest optimizations
- Benchmark against industry standards

**Stakeholder Access:**
- **Internal** - Full analysis, all tenants (aggregated)
- **Customers** - Their own workflow analysis
- **Consultants** - Client workflow reports
- **Advisors** - Industry benchmark reports

---

#### 9. Multi-LLM IDE Integration

**Priority:** P0 (Core platform capability)

**Capabilities:**
- Cloud-based IDE with multiple LLM backends
- Real-time collaboration
- Integrated with master project orchestration
- Session management built-in

**Stakeholder Access:**
- **All stakeholders** - Access via web browser
- **Customers** - LLM access based on tier
- **Enterprise** - Dedicated LLM instances

---

#### 10. Compliance & Audit Tools

**Priority:** P1 (Required for enterprise sales)

**Capabilities:**
- Automated compliance checks (SOC 2, ISO 27001)
- Audit trail export
- Vulnerability scanning
- License compliance
- GDPR/CCPA data export

**Stakeholder Access:**
- **Auditors** - Full access during audit window
- **Customers** - Self-service compliance reports
- **Internal** - Compliance dashboard

---

## Tool Abstraction Patterns

### Pattern 1: Configuration-Driven Behavior

**Example: Rate limiting by stakeholder type**

```python
# config/rate_limits.yaml
rate_limits:
  api_calls:
    internal: -1  # Unlimited
    customer_individual: 100  # per minute
    customer_business: 1000
    customer_enterprise: 10000
    consultant: 500
    vendor: 200
    auditor: 50  # Read-only, low limit

# Implementation
from functools import wraps
import yaml

config = yaml.safe_load(open("config/rate_limits.yaml"))

def rate_limit(resource: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(tenant_id: str, *args, **kwargs):
            stakeholder_type = get_stakeholder_type(tenant_id)
            limit = config["rate_limits"][resource][stakeholder_type]

            if limit == -1:  # Unlimited
                return await func(tenant_id, *args, **kwargs)

            current_usage = await get_usage(tenant_id, resource)
            if current_usage >= limit:
                raise RateLimitExceeded(f"Rate limit exceeded: {limit} {resource} per minute")

            return await func(tenant_id, *args, **kwargs)
        return wrapper
    return decorator

@rate_limit("api_calls")
async def create_project(tenant_id: str, name: str):
    # Rate limit enforced automatically
    pass
```

---

### Pattern 2: Feature Flags

**Example: Gradual rollout of new features**

```python
# Feature flag service (LaunchDarkly, Unleash, or custom)
class FeatureFlags:
    @staticmethod
    def is_enabled(feature: str, tenant_id: str) -> bool:
        stakeholder_type = get_stakeholder_type(tenant_id)

        # Internal always gets all features
        if stakeholder_type == "internal":
            return True

        # Check feature flag service
        return feature_flag_service.is_enabled(
            feature_key=feature,
            context={"tenant_id": tenant_id, "type": stakeholder_type}
        )

# Usage
@app.post("/api/v1/projects")
async def create_project(tenant_id: str, request: CreateProjectRequest):
    # New feature: AI-generated project templates
    if FeatureFlags.is_enabled("ai_project_templates", tenant_id):
        template = generate_ai_template(request.description)
        request.template = template

    return await _create_project(tenant_id, request)
```

**Rollout Strategy:**
```
Week 1: Internal only (100% internal, 0% customers)
Week 2: Beta customers (100% internal, 10% enterprise customers)
Week 3: Expand (100% internal, 50% enterprise, 10% business)
Week 4: General availability (all stakeholders)
```

---

### Pattern 3: Plugin Architecture

**Example: Extensible tool with plugins**

```python
# Core tool provides plugin interface
class CoditectPlugin:
    def on_project_created(self, tenant_id: str, project_id: str):
        pass

    def on_session_started(self, tenant_id: str, session_id: str):
        pass

# Plugin registry
class PluginRegistry:
    plugins: List[CoditectPlugin] = []

    @classmethod
    def register(cls, plugin: CoditectPlugin):
        cls.plugins.append(plugin)

    @classmethod
    def trigger(cls, event: str, **kwargs):
        for plugin in cls.plugins:
            method = getattr(plugin, f"on_{event}", None)
            if method:
                method(**kwargs)

# Example plugin: Slack notifications
class SlackNotificationPlugin(CoditectPlugin):
    def on_project_created(self, tenant_id: str, project_id: str):
        send_slack_message(
            channel=get_tenant_slack_channel(tenant_id),
            message=f"New project created: {project_id}"
        )

# Register plugin
PluginRegistry.register(SlackNotificationPlugin())

# Trigger event
@app.post("/api/v1/projects")
async def create_project(tenant_id: str, request: CreateProjectRequest):
    project = await _create_project(tenant_id, request)

    # Plugins get notified automatically
    PluginRegistry.trigger("project_created", tenant_id=tenant_id, project_id=project.id)

    return project
```

**Stakeholder-Specific Plugins:**
- **Internal** - Slack, Jira, Linear integrations
- **Customers** - Zapier, Slack, Microsoft Teams
- **Consultants** - Time tracking, billing integrations

---

## Multi-Tenancy Architecture

### Database Design

```sql
-- Every table has tenant_id
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    stakeholder_type VARCHAR(50) NOT NULL,  -- 'internal', 'customer', 'consultant', etc.
    tier VARCHAR(50) NOT NULL,  -- 'individual', 'business', 'enterprise'
    status VARCHAR(50) DEFAULT 'active',  -- 'active', 'suspended', 'offboarded'
    created_at TIMESTAMP DEFAULT NOW(),
    offboarded_at TIMESTAMP
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    -- Enforce tenant isolation with index
    CONSTRAINT unique_project_name_per_tenant UNIQUE (tenant_id, name)
);

-- Row-level security (PostgreSQL)
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON projects
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

**Query Pattern:**
```python
# Set tenant context at request start
@app.middleware("http")
async def set_tenant_context(request: Request, call_next):
    tenant_id = get_tenant_from_auth_token(request)

    async with db.transaction():
        await db.execute(f"SET LOCAL app.current_tenant_id = '{tenant_id}'")
        response = await call_next(request)

    return response

# All queries automatically filtered by tenant_id
projects = await db.fetch_all("SELECT * FROM projects")
# Returns only projects for current tenant (row-level security enforced)
```

---

## Permission & Access Control

### Permission Matrix

| Resource | Internal | Customer (Owner) | Customer (Editor) | Customer (Viewer) | Consultant | Vendor | Auditor |
|----------|----------|------------------|-------------------|-------------------|------------|--------|---------|
| **Projects** |
| Create | ✅ | ✅ | ✅ | ❌ | ✅ (client) | ❌ | ❌ |
| Read | ✅ | ✅ | ✅ | ✅ | ✅ (client) | ❌ | ✅ |
| Update | ✅ | ✅ | ✅ | ❌ | ✅ (client) | ❌ | ❌ |
| Delete | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Users** |
| Invite | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Remove | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Billing** |
| View | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Update | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Audit Logs** |
| View | ✅ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ✅ |
| Export | ✅ | ✅ (own) | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Tool Distribution & Packaging

### Distribution Channels

**1. Cloud SaaS (Primary)**
- Web application (https://app.coditect.ai)
- No installation required
- Automatic updates
- Multi-device access

**2. CLI Tools (PyPI)**
```bash
# Install via pip
pip install coditect-cli

# Authenticate
coditect auth login

# Use tools
coditect projects create "My Project"
coditect git start-session "New feature"
```

**3. Docker Containers**
```bash
# Run master project orchestrator
docker run -it coditect/orchestrator:latest

# Run in Kubernetes
kubectl apply -f coditect-deployment.yaml
```

**4. GitHub App**
```
# Install from GitHub Marketplace
https://github.com/marketplace/coditect-ai
```

**5. VS Code Extension**
```
# Install from VS Code Marketplace
ext install coditect.coditect-vscode
```

---

## Documentation Standards

### Documentation Types by Stakeholder

**Internal Documentation:**
- Architecture Decision Records (ADRs)
- Database schema docs
- API internal implementation docs
- Runbooks for operations

**Customer Documentation:**
- Getting started guides
- Tutorials
- API reference (OpenAPI)
- FAQs
- Video tutorials

**Consultant Documentation:**
- Multi-client management guide
- Best practices
- Client onboarding checklists
- Reporting templates

**Vendor Documentation:**
- Integration guides
- API specifications
- SLA requirements
- Support escalation

**Auditor Documentation:**
- Compliance reports
- Security architecture
- Data flow diagrams
- Audit trail export guide

---

## Versioning & Backward Compatibility

### Semantic Versioning

```
v<MAJOR>.<MINOR>.<PATCH>

MAJOR: Breaking changes (require customer code changes)
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
```

**Deprecation Policy:**
```
v2.0 (New version)  → Announce deprecation of v1.0
  ↓
v2.1               → v1.0 still supported (warning logs)
  ↓
v2.2               → v1.0 still supported (warning logs)
  ↓
v3.0 (6 months)    → v1.0 removed, v2.x becomes baseline
```

**API Versioning:**
```
/api/v1/projects   → Supported
/api/v2/projects   → Current
/api/v3/projects   → Beta (opt-in)
```

---

## Tool Evolution Roadmap

### Phase 1: Internal Validation (Months 1-2)

**Goal:** Validate tools with AZ1.AI team

**Activities:**
- Use tools for CODITECT rollout
- Identify pain points and bugs
- Gather feedback from team
- Iterate rapidly

**Success Criteria:**
- 100% of AZ1.AI team using tools daily
- <5 P1 bugs per tool
- NPS >70 from internal users

---

### Phase 2: Abstraction & Generalization (Months 2-4)

**Goal:** Make tools reusable for external stakeholders

**Activities:**
- Add multi-tenancy to all tools
- Implement RBAC
- Build web UIs for CLI tools
- Write customer-facing documentation
- Add usage tracking and billing hooks

**Success Criteria:**
- All tools support multi-tenancy
- Permission system tested with 5+ personas
- Documentation complete for customers

---

### Phase 3: Customer Beta (Months 4-6)

**Goal:** Validate tools with 50-100 beta customers

**Activities:**
- Invite beta customers (enterprise tier)
- Provide white-glove onboarding
- Collect feedback and iterate
- Build case studies

**Success Criteria:**
- 50+ beta customers using tools
- NPS >60 from beta customers
- 3-5 case studies completed
- <10 P1/P2 bugs

---

### Phase 4: General Availability (Month 6+)

**Goal:** Open tools to all customer tiers

**Activities:**
- Public launch announcement
- Self-service onboarding
- Consultant and vendor access
- Marketplace integrations

**Success Criteria:**
- 1000+ active tenants using tools
- <5% churn rate
- 95%+ uptime SLA
- Revenue from tools covers development cost

---

## Summary: Build Once, Use Everywhere

### Key Takeaways

✅ **Every tool we build must be designed for reusability from day one**

✅ **Multi-tenancy, RBAC, and API-first are non-negotiable**

✅ **Think beyond current use case → all stakeholder groups**

✅ **Configuration over code → easy to adapt for new stakeholders**

✅ **Security, observability, and documentation are first-class concerns**

✅ **Internal validation → Abstraction → Customer beta → General availability**

### Economic Impact

**Without Reusability (Current Anti-Pattern):**
- 1 tool × 8 stakeholder groups = 8 tools to build
- 8 tools × $50K each = $400K total cost
- 8 tools × 20 hours/month maintenance = 160 hours/month

**With Reusability (CODITECT Pattern):**
- 1 tool × 1 build = $75K (50% more upfront for abstraction)
- 1 tool × 20 hours/month maintenance = 20 hours/month
- **Savings: $325K + 140 hours/month**

### Competitive Moat

By building reusable tools, we create:
1. **Network effects** - More users = better tools = more users
2. **Ecosystem lock-in** - Tools integrate deeply with CODITECT platform
3. **Faster innovation** - New features benefit all stakeholders
4. **Market differentiation** - Competitors can't match our tooling velocity

---

**This is the AZ1.AI CODITECT way: Build once, use everywhere, scale infinitely.**

---

*Built with Excellence by AZ1.AI CODITECT*
*Systematic Development. Continuous Context. Exceptional Results.*
