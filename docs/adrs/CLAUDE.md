# Architecture Decision Records - Claude Code Configuration

## Directory Purpose

Architecture Decision Records (ADRs) documenting key architectural decisions for CODITECT platform projects.

## Essential Reading

**READ FIRST:**
1. project-intelligence/README.md - Index of 8 ADRs
2. project-intelligence/ADR-COMPLIANCE-REPORT.md - Cross-ADR validation
3. Individual ADRs as needed for implementation context

## Tech Stack (from ADRs)

### Project Intelligence Platform

**Backend:**
- FastAPI (ADR-005)
- PostgreSQL (ADR-002)
- ChromaDB (ADR-003)

**Frontend:**
- React + Next.js (ADR-006)
- TypeScript
- Server-side rendering

**Cloud:**
- GCP Cloud Run (ADR-007)
- Cloud SQL
- Cloud Storage

**Architecture:**
- Schema-based multi-tenancy (ADR-004)
- RBAC permissions (ADR-008)
- Git as source of truth (ADR-001)

## Key ADRs

### ADR-001: Git as Source of Truth
- Use Git repository history as primary data source
- Zero additional data entry
- Complex parsing required

### ADR-002: PostgreSQL Database
- ACID transactions
- Schema-based multi-tenancy
- Full-text search built-in

### ADR-003: ChromaDB Semantic Search
- Vector embeddings
- Similarity search
- AI-powered insights

### ADR-004: Multi-Tenant Strategy
- PostgreSQL schemas per tenant
- Strong data isolation
- Cost-efficient shared infrastructure

### ADR-005: FastAPI Backend
- Async/await performance
- Auto-generated OpenAPI docs
- Type-safe with Pydantic

### ADR-006: React + Next.js Frontend
- Server-side rendering
- Component-based architecture
- TypeScript support

### ADR-007: GCP Cloud Run Deployment
- Serverless containers
- Auto-scaling 0 to N
- Pay-per-use pricing

### ADR-008: RBAC Permissions
- Org/Project/User scopes
- Hierarchical access
- Audit trail

## Common Operations

### Review Architecture
```bash
# ADR index
cat project-intelligence/README.md

# All decisions summary
cat project-intelligence/ADR-COMPLIANCE-REPORT.md

# Specific decision
cat project-intelligence/ADR-005-fastapi-over-flask-django.md
```

### Validate Consistency
```bash
# Check cross-ADR alignment
cat project-intelligence/ADR-COMPLIANCE-REPORT.md

# Search for conflicts
grep -r "CONFLICT" project-intelligence/
```

### Implementation Guidance
```bash
# Technology choices
grep "Decision:" project-intelligence/ADR-*.md

# Trade-offs
grep "Consequences:" project-intelligence/ADR-*.md
```

## Project-Specific Instructions

### When Implementing Features
1. Check relevant ADRs for constraints
2. Follow technology choices (FastAPI, PostgreSQL, etc.)
3. Maintain multi-tenancy via schemas (ADR-004)
4. Implement RBAC per ADR-008 patterns

### When Reviewing Code
1. Validate against ADR decisions
2. Check multi-tenancy isolation
3. Ensure RBAC enforcement
4. Verify Git parsing follows ADR-001

### When Proposing Changes
1. Review existing ADRs first
2. Document why change needed
3. Create new ADR (don't modify existing)
4. Mark superseded ADRs if applicable
5. Update compliance report

### When Adding Technology
1. Check if addressed by existing ADR
2. If not, create new ADR with:
   - Context and problem statement
   - Alternatives considered
   - Decision outcome with rationale
   - Trade-offs (pros/cons)
3. Update ADR-COMPLIANCE-REPORT.md

## Cross-References

**Implementation:**
- Project Intelligence backend: (To be created in submodules/cloud/)
- Related diagrams: ../../diagrams/phase-*-*/

**Planning:**
- ../project-management/PROJECT-PLAN.md - Overall timeline
- ../project-management/TASKLIST.md - Implementation tasks

**Security:**
- ../security/ - GCP security advisories
- ADR-008 for RBAC requirements

## Important Constraints

### ADR Immutability
- ADRs are immutable once approved
- Create new ADR to supersede old decisions
- Mark old ADR as "Superseded by ADR-XXX"

### Multi-Tenancy (ADR-004)
- All queries MUST filter by tenant schema
- Never cross-tenant data access
- Schema-per-tenant isolation enforced

### Access Control (ADR-008)
- Check permissions at API layer
- Org → Project → User hierarchy
- Roles: Owner, Admin, Member, Viewer

### Data Source (ADR-001)
- Git is authoritative source
- Never modify Git data
- Parse commits for insights

## Quality Gates

**Before Implementation:**
- [ ] Read relevant ADRs
- [ ] Understand technology constraints
- [ ] Review trade-offs documented
- [ ] Check compliance report alignment

**Before Architecture Changes:**
- [ ] Create new ADR if significant
- [ ] Document alternatives considered
- [ ] Explain rationale and trade-offs
- [ ] Update compliance report

**Before Deployment:**
- [ ] Validate ADR-007 (GCP Cloud Run)
- [ ] Check multi-tenancy (ADR-004)
- [ ] Verify RBAC (ADR-008)
- [ ] Test Git ingestion (ADR-001)

## ADR Template Structure

```
# ADR-XXX: [Title]

Status: [Proposed | Accepted | Deprecated | Superseded]
Date: YYYY-MM-DD

## Context and Problem Statement
## Decision Drivers
## Considered Options
## Decision Outcome
## Pros and Cons of Options
## Links
```

## Statistics

- Total ADRs: 8
- Status Approved: 100%
- Total Documentation: ~100K words
- Projects Covered: 1 (Project Intelligence Platform)

---

**Status:** ✅ Production Ready
**Last Updated:** 2025-11-22
**Review Frequency:** When new ADRs added
