# CODITECT Architecture Diagrams

Visual documentation of architectural decisions and system design using Mermaid diagrams and narrative documentation.

---

## 📚 Architecture Decision Records (ADRs)

### [ADR-002: Hybrid Deployment Architecture](adr-002-deployment/)

**Decision:** Local-first execution + cloud services model

**Diagrams:**
1. [Hybrid Architecture Overview](adr-002-deployment/01-hybrid-architecture-overview.md) - System context (C4 Level 1)
2. [Deployment Options Comparison](adr-002-deployment/02-deployment-options.md) - Free, Pro, Team, Enterprise tiers
3. [Cloud Services Architecture](adr-002-deployment/03-cloud-services.md) - Microservices architecture (C4 Level 2)

**Key Topics:**
- Local engine + cloud services architecture
- Subscription tiers and deployment models
- License validation flows
- Offline mode and grace periods
- Enterprise on-premise deployment
- Cloud infrastructure (GCP)

---

### [ADR-003: User Registration and Authentication](adr-003-authentication/)

**Decision:** Multi-layered authentication with Firebase Auth, JWT tokens, and enterprise SSO

**Diagrams:**
1. [Authentication Flows](adr-003-authentication/01-authentication-flows.md) - Registration, login, SSO, MFA flows

**Key Topics:**
- User registration (email/password, OAuth, SSO)
- Authentication flows (JWT, refresh tokens)
- Enterprise SSO (SAML, OIDC)
- Multi-factor authentication (TOTP)
- Session management and revocation
- Password security and reset flows

---

## 🎨 Diagram Types

### Sequence Diagrams
Interactive flows showing step-by-step processes:
- User registration and email verification
- Login with email/password
- Token refresh flows
- SAML 2.0 SSO authentication
- OAuth 2.0 / OIDC flows
- MFA enrollment and challenge

### Container Diagrams (C4 Level 2)
Service-level architecture:
- CODITECT Cloud Services
- API Gateway and microservices
- Database, cache, storage layers

### Context Diagrams (C4 Level 1)
System-level overview:
- Hybrid architecture (local + cloud)
- External integrations (Stripe, SSO, LLM providers)

### State Diagrams
Lifecycle and state transitions:
- Offline mode and grace periods
- Session lifecycle
- Subscription tier progression

### Deployment Diagrams
Infrastructure and deployment:
- GCP Cloud Run auto-scaling
- Kubernetes enterprise deployment
- Network topology

---

## 📖 How to Use These Diagrams

### For Developers
1. Start with ADR-002 for deployment architecture understanding
2. Read ADR-003 for authentication implementation
3. Use sequence diagrams as implementation guides
4. Reference container diagrams for service boundaries

### For Product/Business
1. Review deployment options comparison (ADR-002 Diagram 2)
2. Understand subscription tiers and features
3. Enterprise deployment capabilities

### For Architecture Reviews
1. Use C4 diagrams for high-level discussions
2. Drill down to sequence diagrams for detailed flows
3. Reference ADRs for decision rationale

---

## 🔗 Related Documentation

**Architecture Decision Records:**
- [ADR-001: Async Task Executor Refactoring](../adrs/ADR-001-async-task-executor-refactoring.md)
- [ADR-002: Hybrid Deployment Architecture](../adrs/ADR-002-hybrid-deployment-architecture.md)
- [ADR-003: User Registration and Authentication](../adrs/ADR-003-user-registration-authentication.md)

**Technical Specifications:**
- [Database Architecture](../database/DATABASE-ARCHITECTURE-PROJECT-INTELLIGENCE.md)
- [C4 Diagrams](../c4-diagrams/C4-DIAGRAMS-PROJECT-INTELLIGENCE.md)
- [Software Design Document](../software-design/SOFTWARE-DESIGN-DOCUMENT-PROJECT-INTELLIGENCE.md)

**Project Planning:**
- [PROJECT-PLAN.md](../../03-project-planning/PROJECT-PLAN.md)
- [TASKLIST-WITH-CHECKBOXES.md](../../03-project-planning/TASKLIST-WITH-CHECKBOXES.md)

---

## ✨ Diagram Standards

### Mermaid Syntax
All diagrams use [Mermaid](https://mermaid.js.org/) for version-controllable, text-based diagrams.

### C4 Model
System architecture follows the [C4 Model](https://c4model.com/):
- **Level 1 (Context)**: System and external dependencies
- **Level 2 (Container)**: Services and databases
- **Level 3 (Component)**: Internal structure
- **Level 4 (Code)**: Implementation details

### Naming Conventions
- `01-{topic}.md` - Primary diagram
- `02-{topic}.md` - Secondary diagram
- `03-{topic}.md` - Tertiary diagram

### File Structure
```
docs/02-architecture/diagrams/
├── README.md (this file)
├── adr-002-deployment/
│   ├── 01-hybrid-architecture-overview.md
│   ├── 02-deployment-options.md
│   └── 03-cloud-services.md
└── adr-003-authentication/
    └── 01-authentication-flows.md
```

---

## 🚀 Future Diagrams (Roadmap)

### ADR-004: Licensing and Entitlement System
- License key generation and validation
- Quota enforcement mechanisms
- Feature flag architecture

### ADR-005: Multi-Tenancy Strategy
- Tenant isolation patterns
- Database partitioning strategies
- Cross-tenant security boundaries

### ADR-006: Payment and Subscription Management
- Stripe integration architecture
- Subscription lifecycle workflows
- Billing and invoicing flows

---

**Last Updated:** 2025-11-23
**Maintained By:** Engineering Team
**Review Frequency:** Quarterly or with major architectural changes
