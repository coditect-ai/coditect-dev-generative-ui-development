# Architecture Decision Records (ADRs)

**Last Updated:** 2025-11-22
**Total ADRs:** 10 (8 project-specific + 1 compliance report + 1 index)
**Primary Project:** Project Intelligence Platform (Multi-tenant SaaS)
**Status:** Architecture Approved ✅, Implementation Planning Phase

---

## Overview

This directory contains **Architecture Decision Records (ADRs)** documenting key architectural decisions for CODITECT platform projects. Currently, it houses comprehensive ADRs for the **Project Intelligence Platform** - a multi-tenant SaaS application for visualizing project history and insights.

**ADR Purpose:**
- Document significant architectural decisions
- Provide rationale and context for technology choices
- Enable future developers to understand "why" not just "what"
- Track alternatives considered and trade-offs made
- Serve as reference for implementation teams

---

## 📁 Project Intelligence Platform ADRs

Located in `project-intelligence/` subdirectory.

### Core Architecture Decisions

| ADR | Title | Decision | Status |
|-----|-------|----------|--------|
| **001** | Git as Source of Truth | Use Git repository history as primary data source | ✅ Approved |
| **002** | PostgreSQL as Primary Database | Use PostgreSQL for relational data storage | ✅ Approved |
| **003** | ChromaDB for Semantic Search | Use ChromaDB for vector embeddings and semantic search | ✅ Approved |
| **004** | Multi-Tenant Strategy | Use schema-based multi-tenancy in PostgreSQL | ✅ Approved |
| **005** | FastAPI over Flask/Django | Use FastAPI for backend API framework | ✅ Approved |
| **006** | React + Next.js Frontend | Use React with Next.js for frontend | ✅ Approved |
| **007** | GCP Cloud Run Deployment | Deploy on Google Cloud Platform using Cloud Run | ✅ Approved |
| **008** | Role-Based Access Control | Implement RBAC with org/project/user scopes | ✅ Approved |

### Supporting Documentation

| Document | Purpose | Lines |
|----------|---------|-------|
| **README.md** | Index and overview of all ADRs | 400+ |
| **ADR-COMPLIANCE-REPORT.md** | Cross-ADR validation and consistency check | 500+ |

---

## 🎯 Project Intelligence Platform Overview

**Vision:** Multi-tenant SaaS platform that ingests Git repository history and provides intelligent insights, visualization, and AI-powered analysis of project evolution.

**Key Features:**
- Git repository ingestion and analysis
- Timeline visualization of project milestones
- Semantic search across commits, issues, PRs
- AI-powered insight generation
- Multi-tenant with org/project/user isolation
- Role-based access control (Owner, Admin, Member, Viewer)

**Tech Stack (per ADRs):**
- **Backend:** FastAPI + PostgreSQL + ChromaDB
- **Frontend:** React + Next.js + TypeScript
- **Cloud:** GCP Cloud Run + Cloud SQL + Cloud Storage
- **Auth:** OAuth 2.0 + JWT tokens
- **Search:** ChromaDB vector embeddings + PostgreSQL FTS

---

## 📋 ADR Index (Detailed)

### ADR-001: Git as Source of Truth

**Decision:** Use Git repository history as the primary source of truth for project data.

**Context:**
- Need reliable, versioned source of project history
- Developers already maintain Git repositories
- Avoid duplicate data entry

**Alternatives Considered:**
- Manual data entry system
- Database-first approach with Git sync
- Issue tracker APIs (GitHub, GitLab)

**Consequences:**
- ✅ Authoritative source (Git commits don't lie)
- ✅ Zero additional data entry overhead
- ⚠️ Complex parsing required for insights
- ⚠️ Depends on commit message quality

**File:** project-intelligence/ADR-001-git-as-source-of-truth.md (21KB)

---

### ADR-002: PostgreSQL as Primary Database

**Decision:** Use PostgreSQL for relational data storage.

**Context:**
- Need ACID transactions for multi-tenancy
- Complex relationships (users, orgs, projects, repos)
- Schema-based multi-tenancy support

**Alternatives Considered:**
- MySQL
- MongoDB (NoSQL)
- DynamoDB

**Consequences:**
- ✅ ACID compliance and data integrity
- ✅ Native schema-based multi-tenancy
- ✅ Rich query capabilities (JOINs, CTEs)
- ✅ Full-text search built-in
- ⚠️ Requires vertical scaling strategy

**File:** project-intelligence/ADR-002-postgresql-as-primary-database.md (19KB)

---

### ADR-003: ChromaDB for Semantic Search

**Decision:** Use ChromaDB for vector embeddings and semantic search.

**Context:**
- Need semantic search across commits, code, docs
- Want AI-powered insight generation
- Require embedding storage and similarity search

**Alternatives Considered:**
- Pinecone (SaaS vector DB)
- Weaviate
- Elasticsearch with vector plugin

**Consequences:**
- ✅ Open-source and self-hostable
- ✅ Python-native integration
- ✅ Fast similarity search
- ⚠️ Requires embedding generation pipeline
- ⚠️ Additional infrastructure to manage

**File:** project-intelligence/ADR-003-chromadb-for-semantic-search.md (20KB)

---

### ADR-004: Multi-Tenant Strategy

**Decision:** Use schema-based multi-tenancy in PostgreSQL.

**Context:**
- Multiple organizations using single platform
- Need strong data isolation
- Want cost efficiency vs. DB-per-tenant

**Alternatives Considered:**
- Row-level tenancy (tenant_id column)
- Database per tenant
- Separate infrastructure per tenant

**Consequences:**
- ✅ Strong data isolation via PostgreSQL schemas
- ✅ Cost-efficient (shared infrastructure)
- ✅ Easier backups and migrations
- ⚠️ Requires connection pooling strategy
- ⚠️ Schema management complexity

**File:** project-intelligence/ADR-004-multi-tenant-strategy.md (15KB)

---

### ADR-005: FastAPI over Flask/Django

**Decision:** Use FastAPI for backend API framework.

**Context:**
- Need high-performance async API
- Want automatic OpenAPI documentation
- Require type safety and validation

**Alternatives Considered:**
- Flask (traditional Python framework)
- Django + DRF (full-featured framework)
- Express.js (Node.js alternative)

**Consequences:**
- ✅ Async/await for high concurrency
- ✅ Auto-generated OpenAPI docs
- ✅ Pydantic validation
- ✅ Modern Python type hints
- ⚠️ Smaller ecosystem vs. Django

**File:** project-intelligence/ADR-005-fastapi-over-flask-django.md (6.5KB)

---

### ADR-006: React + Next.js Frontend

**Decision:** Use React with Next.js for frontend.

**Context:**
- Need server-side rendering for SEO
- Want component-based architecture
- Require modern developer experience

**Alternatives Considered:**
- Vue.js + Nuxt.js
- Svelte + SvelteKit
- Angular

**Consequences:**
- ✅ SSR and static generation
- ✅ Large React ecosystem
- ✅ Excellent TypeScript support
- ✅ Built-in routing and API routes
- ⚠️ More complex than SPA frameworks

**File:** project-intelligence/ADR-006-react-nextjs-frontend.md (6.7KB)

---

### ADR-007: GCP Cloud Run Deployment

**Decision:** Deploy on Google Cloud Platform using Cloud Run.

**Context:**
- Need serverless container deployment
- Want automatic scaling
- Require cost efficiency (pay-per-use)

**Alternatives Considered:**
- AWS ECS Fargate
- Azure Container Instances
- Kubernetes (GKE)

**Consequences:**
- ✅ Serverless (no server management)
- ✅ Auto-scaling (0 to N)
- ✅ Pay only for requests
- ✅ Integrates with GCP services
- ⚠️ Vendor lock-in to GCP
- ⚠️ Cold start latency

**File:** project-intelligence/ADR-007-gcp-cloud-run-deployment.md (6KB)

---

### ADR-008: Role-Based Access Control

**Decision:** Implement RBAC with org/project/user scopes.

**Context:**
- Need granular permissions
- Want hierarchical access (org → project → repo)
- Require audit trail

**Alternatives Considered:**
- Simple admin/user roles
- Attribute-based access control (ABAC)
- Custom permission system

**Consequences:**
- ✅ Industry-standard RBAC pattern
- ✅ Clear permission hierarchy
- ✅ Scalable to enterprise needs
- ⚠️ Complex permission evaluation
- ⚠️ Requires permission caching

**File:** project-intelligence/ADR-008-role-based-access-control.md (10KB)

---

### ADR Compliance Report

**Document:** ADR-COMPLIANCE-REPORT.md (16KB)

**Purpose:** Cross-ADR validation ensuring architectural consistency.

**Validation Areas:**
- Technology stack compatibility
- Multi-tenancy consistency across layers
- Security considerations alignment
- Deployment strategy coherence
- Data flow integrity

**Status:** ✅ All ADRs compliant and internally consistent

---

## 🚀 Quick Start Guide

### For Architects

1. **Reviewing Architecture:**
   ```bash
   # Read ADR index
   cat project-intelligence/README.md

   # Review compliance
   cat project-intelligence/ADR-COMPLIANCE-REPORT.md
   ```

2. **Understanding Decisions:**
   - Read ADRs in numerical order (001 → 008)
   - Note alternatives considered
   - Understand trade-offs made

3. **Proposing Changes:**
   - Create new ADR following template
   - Reference existing ADRs
   - Update compliance report

### For Developers

1. **Technology Choices:**
   - ADR-005: Backend framework (FastAPI)
   - ADR-006: Frontend framework (React + Next.js)
   - ADR-002: Database (PostgreSQL)
   - ADR-003: Search (ChromaDB)

2. **Implementation Patterns:**
   - ADR-004: Multi-tenancy (schema-based)
   - ADR-008: Access control (RBAC)
   - ADR-001: Data source (Git)

3. **Deployment:**
   - ADR-007: Cloud platform (GCP Cloud Run)

### For AI Agents

1. **Architecture Context:**
   ```
   Read project-intelligence/README.md → Overview
   Read ADR-001 through ADR-008 → Core decisions
   Read ADR-COMPLIANCE-REPORT.md → Validation
   ```

2. **Implementation Guidance:**
   - Reference ADRs for technology constraints
   - Use "Consequences" sections for patterns
   - Check compliance report for cross-cutting concerns

---

## 📝 ADR Template

```markdown
# ADR-XXX: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Date:** YYYY-MM-DD
**Deciders:** [List of people]
**Technical Story:** [Link to issue/story]

## Context and Problem Statement

[Describe the context and problem statement]

## Decision Drivers

- [Driver 1]
- [Driver 2]
- ...

## Considered Options

- [Option 1]
- [Option 2]
- ...

## Decision Outcome

Chosen option: "[Option X]", because [justification].

### Positive Consequences

- [e.g., improvement of quality attribute satisfaction]
- ...

### Negative Consequences

- [e.g., compromising quality attribute]
- ...

## Pros and Cons of the Options

### [Option 1]

- ✅ Pro 1
- ✅ Pro 2
- ⚠️ Con 1
- ⚠️ Con 2

### [Option 2]

...

## Links

- [Link type] [Link description]
- ...
```

---

## 🔗 Related Documentation

### Within This Repository

- **[../project-management/](../project-management/)** - PROJECT-PLAN.md and TASKLIST.md
- **[../security/](../security/)** - Security advisories and policies
- **[../../diagrams/](../../diagrams/)** - C4 architecture diagrams
- **[../../README.md](../../README.md)** - Repository overview

### External References

- **ADR Template:** https://github.com/joelparkerhenderson/architecture-decision-record
- **C4 Model:** https://c4model.com/
- **Project Intelligence Platform Repo:** (To be created in submodules/cloud/)

---

## 📊 ADR Statistics

| Metric | Value |
|--------|-------|
| Total ADRs | 8 |
| Status: Approved | 8 (100%) |
| Status: Proposed | 0 |
| Status: Deprecated | 0 |
| Total Word Count | ~100K words |
| Average ADR Length | ~12.5K words |
| Documentation Coverage | 100% (all decisions documented) |

---

## 🆘 Common Questions

**Q: Why are all ADRs in project-intelligence/ subdirectory?**
**A:** This ADR directory is organized by project. Future projects will have their own subdirectories (e.g., cloud-platform/, marketplace/, etc.).

**Q: Can ADRs be changed after approval?**
**A:** ADRs are immutable. If a decision changes, create a new ADR that supersedes the old one, marking the old ADR as "Superseded by ADR-XXX".

**Q: How detailed should ADRs be?**
**A:** Include enough detail for future developers to understand the "why". Document alternatives considered and trade-offs explicitly.

**Q: When should I create an ADR?**
**A:** Create an ADR for any decision that:
- Affects system architecture significantly
- Is difficult/expensive to change later
- Involves trade-offs between quality attributes
- Is likely to be questioned in the future

---

**Document Status:** ✅ Production Ready
**Last Validated:** 2025-11-22
**Next Review:** When new ADRs added
