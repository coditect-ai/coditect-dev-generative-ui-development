# ADR-002 Diagram 2: Deployment Options Comparison

**Related ADR:** [ADR-002: Hybrid Deployment Architecture](../../adrs/ADR-002-hybrid-deployment-architecture.md)

---

## Subscription Tiers & Deployment Models

```mermaid
graph TB
    subgraph "Free Tier - Local Only"
        F1[Desktop Installation]
        F2[10 commands/day]
        F3[Basic agents 10/52]
        F4[No cloud sync]
        F5[Community support]

        F1 --> F2
        F2 --> F3
        F3 --> F4
        F4 --> F5
    end

    subgraph "Pro Tier - Local + Cloud Sync"
        P1[Desktop Installation]
        P2[Unlimited commands]
        P3[All 52 agents]
        P4[Cloud sync enabled]
        P5[Priority support]
        P6[Multi-device]

        P1 --> P2
        P2 --> P3
        P3 --> P4
        P4 --> P5
        P5 --> P6
    end

    subgraph "Team Tier - Collaboration"
        T1[Desktop per user]
        T2[Shared contexts]
        T3[Team analytics]
        T4[Organization mgmt]
        T5[RBAC]

        T1 --> T2
        T2 --> T3
        T3 --> T4
        T4 --> T5
    end

    subgraph "Enterprise - On-Premise"
        E1[Internal Cloud Deploy]
        E2[SSO Integration]
        E3[Air-gapped option]
        E4[Unlimited users]
        E5[SLA 99.9%]

        E1 --> E2
        E2 --> E3
        E3 --> E4
        E4 --> E5
    end

    F1 -.Upgrade.-> P1
    P1 -.Upgrade.-> T1
    T1 -.Upgrade.-> E1

    style F1 fill:#e1f5ff
    style P1 fill:#b3e5ff
    style T1 fill:#66c2ff
    style E1 fill:#0099ff
```

---

## Installation Flows by Tier

### Free Tier - No Registration Required

```mermaid
sequenceDiagram
    actor User as Developer
    participant CLI as Local CLI
    participant Brew as Package Manager

    User->>Brew: brew install coditect
    Brew->>CLI: Download & install
    CLI-->>User: Installed

    User->>CLI: coditect init
    Note over CLI: Free tier enabled<br/>No registration needed
    CLI-->>User: ✅ Ready (10 commands/day)

    Note over User,CLI: Optional: Register for Pro trial
    User->>CLI: coditect register
    CLI->>CLI: Opens browser to https://coditect.ai/signup
```

### Pro Tier - Cloud Registration + Local

```mermaid
sequenceDiagram
    actor User as Developer
    participant Browser as Web Browser
    participant Cloud as CODITECT Cloud
    participant CLI as Local CLI

    User->>Browser: Visit coditect.ai/signup
    Browser->>Cloud: Register (email + password)
    Cloud->>Cloud: Create user account
    Cloud->>Cloud: Generate license key
    Cloud-->>Browser: Display license key

    User->>User: Copy license key

    User->>CLI: brew install coditect
    CLI-->>User: Installed

    User->>CLI: coditect login
    CLI->>Cloud: Authenticate (email/password)
    Cloud-->>CLI: Access token + license key
    CLI->>CLI: Save to ~/.coditect/auth.json

    CLI-->>User: ✅ PRO tier activated
```

### Enterprise Tier - On-Premise Deployment

```mermaid
sequenceDiagram
    actor Admin as Enterprise Admin
    participant K8s as Kubernetes Cluster
    participant Helm as Helm Charts
    participant Cloud as CODITECT Cloud (Internal)
    participant User as Employee
    participant CLI as Employee's CLI

    Admin->>Helm: helm install coditect-enterprise
    Note over Helm: Values:<br/>- License key: ENT-ACME-100<br/>- SSO: enabled<br/>- Air-gap: true

    Helm->>K8s: Deploy services
    K8s->>Cloud: Start Auth, License, Sync services
    Cloud->>Cloud: Validate enterprise license

    Admin->>Cloud: Configure SSO (Okta)
    Admin->>Cloud: Add employees

    User->>CLI: brew install coditect
    User->>CLI: coditect config set cloud-url https://coditect.acme.com
    User->>CLI: coditect login --sso

    CLI->>Cloud: Redirect to SSO
    Cloud->>Cloud: SAML authentication
    Cloud-->>CLI: Auth token + org license

    CLI-->>User: ✅ Logged in (ACME org)
```

---

## Architecture Comparison Matrix

| Feature | Free | Pro | Team | Enterprise |
|---------|------|-----|------|------------|
| **Deployment** | Local only | Local + Cloud | Local + Cloud | On-Premise |
| **Installation** | `brew install` | `brew install` + signup | `brew install` + org invite | Helm chart |
| **Authentication** | None | Email/OAuth | Email/OAuth | SSO (SAML/OIDC) |
| **License Storage** | Local only | Cloud validated | Cloud validated | Internal server |
| **Data Residency** | 100% local | 100% local | 100% local (+ optional sync) | Customer infrastructure |
| **Internet Required** | No | Yes (daily check) | Yes (daily check) | No (air-gapped option) |
| **Collaboration** | ❌ | ❌ | ✅ Team sync | ✅ Organization sync |
| **Support** | Community | Email | Chat | Dedicated engineer |

---

## License Validation Flows

### Standard (Free/Pro/Team) - Cloud Validation

```mermaid
sequenceDiagram
    participant CLI as Local Engine
    participant Cache as Local Cache
    participant API as License API
    participant DB as License DB

    CLI->>Cache: Load cached validation

    alt Cache valid (< 24 hours)
        Cache-->>CLI: Use cached license
    else Cache expired or missing
        CLI->>API: POST /api/v1/licenses/validate<br/>{license_key, machine_id}
        API->>DB: Lookup license

        alt License valid
            DB-->>API: License details (tier, features, quotas)
            API-->>CLI: Validation response
            CLI->>Cache: Cache for 24 hours
        else License invalid/expired
            DB-->>API: License not found/expired
            API-->>CLI: Error: Invalid license
            CLI->>CLI: Downgrade to free tier
        end
    end

    Note over CLI: Enable features based on tier
```

### Enterprise - On-Premise Validation

```mermaid
sequenceDiagram
    participant CLI as Employee CLI
    participant Internal as Internal License Server
    participant License as Enterprise License Key

    CLI->>Internal: POST /internal/licenses/validate<br/>{user_email}

    Internal->>License: Verify enterprise license
    Note over License: License format:<br/>ENT-ACME-100-20261231-SIG

    License->>License: Check signature (RSA)
    License->>License: Check expiration
    License->>License: Check user count

    alt License valid
        License-->>Internal: Valid (100 seats, expires 2026-12-31)
        Internal->>Internal: Check user in organization
        Internal-->>CLI: Access granted (org features)
    else License invalid
        License-->>Internal: Invalid signature/expired
        Internal-->>CLI: Error: Contact admin
    end
```

---

## Network Communication Patterns

### Standard Deployment (Cloud Connected)

```mermaid
graph LR
    subgraph "Developer Machine"
        CLI[Local Engine]
    end

    subgraph "CODITECT Cloud GCP"
        Auth[Auth Service]
        License[License Service]
        Sync[Sync Service]
    end

    subgraph "External Services"
        Claude[Claude API]
        GPT[OpenAI API]
    end

    CLI -->|License check 1x/day| License
    CLI -->|Optional sync| Sync
    CLI -->|Command execution| Claude
    CLI -->|Command execution| GPT

    Auth -.Manages.-> License

    style CLI fill:#b3e5ff
    style Auth fill:#66c2ff
    style License fill:#66c2ff
    style Sync fill:#66c2ff
    style Claude fill:#ffe6cc
    style GPT fill:#ffe6cc
```

**Communication Frequency:**
- License validation: 1x per 24 hours (cached)
- Cloud sync: On-demand or periodic (if enabled)
- LLM API calls: Per command execution

### Enterprise Deployment (Air-Gapped)

```mermaid
graph LR
    subgraph "Corporate Network (Air-Gapped)"
        subgraph "Employee Machines"
            CLI1[Employee 1 CLI]
            CLI2[Employee 2 CLI]
            CLI3[Employee N CLI]
        end

        subgraph "Internal Cloud (K8s)"
            Auth[Auth Service]
            License[License Service]
            Sync[Sync Service]
        end

        CLI1 -->|Internal HTTPS| Auth
        CLI2 -->|Internal HTTPS| Auth
        CLI3 -->|Internal HTTPS| Auth

        Auth --> License
        Auth --> Sync
    end

    subgraph "External (Optional)"
        LLM[LLM Provider]
    end

    CLI1 -.Optional.-> LLM
    CLI2 -.Optional.-> LLM
    CLI3 -.Optional.-> LLM

    style Auth fill:#66c2ff
    style License fill:#66c2ff
    style Sync fill:#66c2ff
    style LLM fill:#ffe6cc,stroke-dasharray: 5 5
```

**Communication Patterns:**
- All auth/license traffic stays inside corporate network
- No external internet required for CODITECT features
- Optional: LLM API access (if org policy allows)
- Optional: Self-hosted LLM (Ollama, LM Studio)

---

## Migration Paths

### User Growth Journey

```mermaid
stateDiagram-v2
    [*] --> Free: Install CODITECT

    Free --> ProTrial: Click "Upgrade" in CLI
    ProTrial --> Pro: Subscribe ($49/mo)
    ProTrial --> Free: Trial expires (30 days)

    Pro --> Team: Invite colleagues
    Team --> Enterprise: Request on-premise

    Free --> Team: Join organization
    Pro --> Team: Join organization

    note right of Free
        10 commands/day
        Local only
        No registration
    end note

    note right of Pro
        Unlimited commands
        Cloud sync
        $49/month
    end note

    note right of Team
        5+ users
        Collaboration
        $99/mo base
    end note

    note right of Enterprise
        On-premise option
        SSO integration
        Custom pricing
    end note
```

---

## Technical Stack by Deployment

### Local Engine (All Tiers)

```
Programming Language: Python 3.10+
CLI Framework: Click/Typer
Database: SQLite (local MEMORY-CONTEXT)
Encryption: Fernet (license keys, API keys)
Package Management: pip/poetry
Distribution: Homebrew (macOS), Chocolatey (Windows), apt/snap (Linux)
```

### Cloud Services (Pro/Team)

```
Hosting: Google Cloud Platform (GCP)
Regions: us-central1 (primary), europe-west1 (EU), asia-northeast1 (Asia)
API Framework: FastAPI (Python)
Database: Cloud SQL PostgreSQL (multi-tenant)
Cache: Memorystore Redis
Storage: Cloud Storage (GCS)
CDN: Cloud CDN
Monitoring: Cloud Monitoring + Prometheus
Logging: Cloud Logging + Loki
```

### Enterprise On-Premise

```
Container Orchestration: Kubernetes 1.28+
Package Manager: Helm 3.x
Database: PostgreSQL 15+ (self-hosted or Cloud SQL)
Cache: Redis 7+ (self-hosted or Memorystore)
Storage: GCS or S3-compatible (MinIO)
Ingress: Nginx or Istio
Service Mesh: Istio (optional)
Monitoring: Prometheus + Grafana
```

---

**Related Documents:**
- [ADR-002: Hybrid Deployment Architecture](../../adrs/ADR-002-hybrid-deployment-architecture.md)
- [Diagram 1: Hybrid Architecture Overview](./01-hybrid-architecture-overview.md)
- [Diagram 3: Cloud Services Architecture](./03-cloud-services.md)
