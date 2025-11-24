# ADR-002 Diagram 1: Hybrid Architecture Overview

**Related ADR:** [ADR-002: Hybrid Deployment Architecture](../../adrs/ADR-002-hybrid-deployment-architecture.md)

---

## System Context Diagram (C4 Level 1)

This diagram shows the high-level hybrid architecture: local engine + cloud services.

```mermaid
C4Context
    title CODITECT Hybrid Architecture - System Context

    Person(developer, "Developer", "Software developer using CODITECT")
    Person(admin, "Enterprise Admin", "Manages organization licenses")

    System_Boundary(local, "Local Environment") {
        System(engine, "CODITECT Local Engine", "Desktop app: CLI + 52 agents + orchestration")
    }

    System_Boundary(cloud, "CODITECT Cloud (GCP)") {
        System(auth, "Auth Service", "User registration, login, SSO")
        System(license, "License Service", "License validation, quotas")
        System(billing, "Billing Service", "Stripe integration, subscriptions")
        System(sync, "Sync Service", "Cloud backup, collaboration")
    }

    System_Ext(llm, "LLM Providers", "Claude, GPT-4, Gemini")
    System_Ext(stripe, "Stripe", "Payment processing")
    System_Ext(sso, "Enterprise SSO", "Okta, Azure AD")

    Rel(developer, engine, "Uses", "CLI commands")
    Rel(engine, auth, "Validates license", "HTTPS/REST")
    Rel(engine, sync, "Syncs data", "HTTPS/REST (optional)")
    Rel(engine, llm, "Executes with", "API calls")

    Rel(admin, auth, "Manages users", "Web portal")
    Rel(auth, license, "Checks entitlements")
    Rel(auth, sso, "Authenticates", "SAML/OAuth")
    Rel(billing, stripe, "Processes payments")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="2")
```

---

## Key Architectural Decisions

### 1. **Local-First Execution**
- All AI agents run locally on developer's machine
- No latency for command execution
- Works offline (with 7-day grace period)
- Customer code never leaves local environment

### 2. **Cloud-Based Management**
- User registration and authentication in cloud
- License validation via cloud API (cached locally)
- Optional cloud sync for collaboration
- Telemetry and analytics (opt-in)

### 3. **Hybrid Benefits**
- ✅ Performance: Local execution speed
- ✅ Privacy: Code stays local
- ✅ Collaboration: Cloud sync for teams
- ✅ Licensing: Cloud-based enforcement
- ✅ Offline: 7-day grace period

---

## Data Flow

### Typical User Session

```mermaid
sequenceDiagram
    actor Dev as Developer
    participant CLI as Local Engine
    participant Auth as Auth Service
    participant License as License Service
    participant LLM as Claude API

    Dev->>CLI: coditect analyze

    Note over CLI: Check cached license<br/>(24hr TTL)

    alt License cached and valid
        CLI->>CLI: Use cached validation
    else License cache expired
        CLI->>Auth: Validate license
        Auth->>License: Check entitlements
        License-->>Auth: Valid (PRO tier)
        Auth-->>CLI: Features enabled
        CLI->>CLI: Cache validation
    end

    CLI->>LLM: Execute analysis
    LLM-->>CLI: Analysis results
    CLI-->>Dev: Display results

    Note over CLI,Dev: All execution happens locally<br/>License validated once per day
```

---

## Deployment Models

### Standard SaaS (Free/Pro/Team)
```
Developer's Machine          CODITECT Cloud (GCP)
┌─────────────────┐         ┌─────────────────────┐
│  Local Engine   │────────▶│  Auth Service       │
│  • CLI          │  HTTPS  │  • Registration     │
│  • 52 Agents    │◀────────│  • License Check    │
│  • SQLite       │         │  • Cloud Sync       │
└─────────────────┘         └─────────────────────┘
```

### Enterprise On-Premise
```
Customer Network
┌──────────────────────────────────────────┐
│  Employee Machines     Internal Cloud    │
│  ┌───────────┐         ┌──────────────┐ │
│  │  Local    │────────▶│  Auth Service│ │
│  │  Engine   │  HTTPS  │  (Kubernetes)│ │
│  └───────────┘◀────────│  • SSO       │ │
│                        │  • License   │ │
│  ┌───────────┐         │  • Sync      │ │
│  │  Local    │────────▶│              │ │
│  │  Engine   │         └──────────────┘ │
│  └───────────┘                          │
│                                         │
│  ← Air-gapped option: no external     │
│     internet required                   │
└──────────────────────────────────────────┘
```

---

## Security Boundaries

```mermaid
graph TB
    subgraph "Customer Environment (Private)"
        A[Source Code]
        B[Project Files]
        C[LLM API Keys]
        D[Local MEMORY-CONTEXT]
    end

    subgraph "Local Engine (Encrypted Storage)"
        E[License Key Cache]
        F[Auth Tokens]
        G[User Preferences]
    end

    subgraph "CODITECT Cloud (Multi-Tenant)"
        H[User Accounts]
        I[License Records]
        J[Subscription Status]
        K[Usage Metrics]
    end

    A -.Never sent to cloud.- K
    B -.Never sent to cloud.- K
    C -.Never sent to cloud.- K
    D -.Optional sync only.- K

    E -->|Daily validation| I
    F -->|Session management| H

    style A fill:#f9f,stroke:#333
    style B fill:#f9f,stroke:#333
    style C fill:#f9f,stroke:#333
    style D fill:#f9f,stroke:#333
```

**Privacy Guarantees:**
- 🔒 Customer code NEVER sent to CODITECT cloud
- 🔒 LLM API keys stored locally (encrypted)
- 🔒 Project files stay on local machine
- 🔒 MEMORY-CONTEXT synced only if user enables (Pro+)

---

## Offline Mode

### Grace Period Logic

```mermaid
stateDiagram-v2
    [*] --> Online: App startup

    Online --> LicenseCheck: Validate license

    LicenseCheck --> ValidCached: Cache < 24h old
    LicenseCheck --> CloudValidate: Cache expired

    CloudValidate --> CacheUpdate: Success
    CloudValidate --> OfflineMode: Network error

    CacheUpdate --> FullFeatures
    ValidCached --> FullFeatures

    OfflineMode --> GracePeriod: Check cache age

    GracePeriod --> GracePeriodActive: < 7 days old
    GracePeriod --> FreeTierOnly: > 7 days old

    GracePeriodActive --> FullFeatures: Use cached license
    FreeTierOnly --> LimitedFeatures: Downgrade to free

    FullFeatures --> [*]: App running
    LimitedFeatures --> [*]: App running

    note right of OfflineMode
        User sees warning:
        "Offline mode - using cached license
        Valid for X more days"
    end note

    note right of FreeTierOnly
        User sees message:
        "License validation required
        Downgraded to free tier"
    end note
```

---

**Related Documents:**
- [ADR-002: Hybrid Deployment Architecture](../../adrs/ADR-002-hybrid-deployment-architecture.md)
- [ADR-003: User Registration and Authentication](../../adrs/ADR-003-user-registration-authentication.md)
- [Diagram 2: Deployment Options Comparison](./02-deployment-options.md)
- [Diagram 3: Cloud Services Architecture](./03-cloud-services.md)
