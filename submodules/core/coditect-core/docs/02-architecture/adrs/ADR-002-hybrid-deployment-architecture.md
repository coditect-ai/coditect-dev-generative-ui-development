# ADR-002: Hybrid Deployment Architecture (Local-First + Cloud Services)

**Status:** Accepted
**Date:** 2025-11-23
**Decision Makers:** Hal Casteel (Founder/CEO/CTO)
**Stakeholders:** Engineering, Product, Sales, Customer Success

---

## Context

CODITECT is AZ1.AI INC's flagship product - a comprehensive project management and AI-powered development platform. We need to define the deployment architecture that balances:

1. **Customer preferences**: Developers prefer local-first tools (privacy, performance, offline work)
2. **Revenue model**: SaaS subscriptions require cloud infrastructure and validation
3. **Enterprise needs**: On-premise deployments with air-gapped environments
4. **Competitive positioning**: Differentiate from pure cloud SaaS (Cursor, GitHub Copilot) and pure local tools

**Key Requirements:**
- Local-first execution (no latency, works offline)
- Cloud registration and license validation
- Multi-user collaboration (teams, organizations)
- Enterprise on-premise option
- Support for free, pro, and enterprise tiers

---

## Decision

**CODITECT will use a HYBRID DEPLOYMENT MODEL** similar to Docker Desktop, Figma Desktop, and Postman:

### Architecture: Local Agent + Cloud Services

```
┌─────────────────────────────────────────────────────────────┐
│                    CUSTOMER ENVIRONMENT                      │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         CODITECT Local Engine (Desktop App)        │    │
│  │                                                      │    │
│  │  • CLI Interface (slash commands)                   │    │
│  │  • 52 AI Agents (local execution)                   │    │
│  │  • Task Orchestration                               │    │
│  │  • LLM Provider Integration (Claude, GPT, etc)      │    │
│  │  • Local Project Files                              │    │
│  │  • MEMORY-CONTEXT Storage (local SQLite)            │    │
│  │  • License Key Storage (encrypted)                  │    │
│  │                                                      │    │
│  └─────────────────┬────────────────────────────────────┘    │
│                    │ HTTPS (License Validation,              │
│                    │         Cloud Sync - Optional)          │
└────────────────────┼────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    CODITECT CLOUD (GCP)                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              User Management Service                  │  │
│  │  • User Registration & Authentication                │  │
│  │  • Organization/Team Management                      │  │
│  │  • SSO Integration (Enterprise)                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Licensing & Entitlement Service            │  │
│  │  • License Key Generation & Validation               │  │
│  │  • Subscription Tier Enforcement (Free/Pro/Ent)      │  │
│  │  • Usage Tracking & Quotas                           │  │
│  │  • License Revocation & Updates                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Payment & Billing Service                   │  │
│  │  • Stripe Integration (SaaS subscriptions)           │  │
│  │  • Invoice Generation (Enterprise)                   │  │
│  │  • Subscription Lifecycle Management                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        Cloud Sync Service (Optional)                  │  │
│  │  • Project Backup & Restore                          │  │
│  │  • MEMORY-CONTEXT Sync                               │  │
│  │  • Team Collaboration (shared contexts)              │  │
│  │  • Cross-Device Sync                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Analytics & Telemetry                    │  │
│  │  • Usage Metrics (commands executed, agents used)    │  │
│  │  • Error Tracking & Diagnostics                      │  │
│  │  • Feature Adoption Analysis                         │  │
│  │  • Performance Monitoring                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Database: PostgreSQL (multi-tenant)                        │
│  Cache: Redis (sessions, license cache)                     │
│  Storage: GCS (backups, templates, artifacts)               │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Options

### 1. **Standard Cloud SaaS** (Free & Pro Tiers)

**Installation:**
```bash
# Download local CLI/desktop app
brew install coditect              # macOS
choco install coditect             # Windows
snap install coditect              # Linux

# First-time setup
coditect login                     # Opens browser, cloud auth
coditect init                      # Initialize project
```

**Architecture:**
- Local engine runs all commands
- Cloud validates license on startup
- Optional: Cloud sync enabled (Pro tier)
- LLM API keys stored locally (encrypted)

**License Validation:**
- On startup: Validate license key → cache for 24 hours
- Every 24 hours: Re-validate with cloud
- Offline mode: Use cached validation (7 day grace period)
- If validation fails: Downgrade to free tier limits

---

### 2. **Enterprise On-Premise** (Enterprise Tier)

**Installation:**
```bash
# Deploy CODITECT Cloud on customer infrastructure
helm install coditect coditect/enterprise \
  --set enterprise.airgap=true \
  --set license.type=enterprise \
  --set license.key=$ENTERPRISE_LICENSE_KEY

# Employees install local engine
coditect config set cloud-url https://coditect.company.com
coditect login --sso
```

**Architecture:**
- Customer hosts CODITECT Cloud (Kubernetes)
- All data stays on-premise (air-gapped option)
- Enterprise SSO integration (Okta, Azure AD)
- Internal license server (no external validation)
- Multi-tenant within organization

**License Validation:**
- Enterprise license key (perpetual or annual)
- Internal validation server
- User count enforcement
- Department/team isolation

---

### 3. **Developer Trial** (Free Tier)

**Installation:**
```bash
# No registration required initially
brew install coditect
coditect init                      # Works with free tier limits

# Register for more features
coditect register                  # Optional, unlocks Pro trial
```

**Free Tier Limits:**
- 10 commands per day
- Single user (no collaboration)
- No cloud sync
- Community support only
- Basic agents (10 of 52)

**License Validation:**
- Anonymous usage tracking (opt-in telemetry)
- Local storage only
- No cloud validation required
- Can upgrade to Pro anytime

---

## Subscription Tiers

### Free Tier ($0/month)
- ✅ 10 commands/day
- ✅ Basic agents (10/52)
- ✅ Local execution only
- ✅ Single user
- ❌ No cloud sync
- ❌ No collaboration
- ❌ Community support

### Pro Tier ($49/month per user)
- ✅ Unlimited commands
- ✅ All 52 agents + 81 commands
- ✅ Cloud sync & backup
- ✅ MEMORY-CONTEXT sync
- ✅ Multi-device support
- ✅ Priority email support
- ✅ Advanced features (hooks, multi-agent workflows)

### Team Tier ($99/month for 5 users, +$19/user)
- ✅ Everything in Pro
- ✅ Team collaboration (shared contexts)
- ✅ Organization management
- ✅ Role-based access control
- ✅ Team analytics dashboard
- ✅ Slack/Teams integration
- ✅ Priority chat support

### Enterprise Tier (Custom pricing)
- ✅ Everything in Team
- ✅ On-premise deployment option
- ✅ Air-gapped deployment
- ✅ SSO integration (SAML, OAuth)
- ✅ Unlimited users
- ✅ Dedicated support engineer
- ✅ SLA guarantee (99.9% uptime)
- ✅ Custom integrations
- ✅ Annual or perpetual licenses

---

## Technical Implementation

### Local Engine (Desktop App)

**Technology Stack:**
- **Core:** Python 3.10+ (orchestration, agents)
- **CLI:** Click/Typer (command-line interface)
- **GUI (Optional):** Electron or Tauri (desktop wrapper)
- **Database:** SQLite (local MEMORY-CONTEXT, settings)
- **Encryption:** Fernet (license keys, API keys)
- **Auto-Update:** Sparkle (macOS), Squirrel (Windows)

**Key Components:**
1. **License Manager** - Validates license on startup, caches locally
2. **Command Executor** - Runs slash commands, enforces quotas
3. **Agent Orchestrator** - Manages 52 AI agents
4. **Sync Client** - Optional cloud sync (Pro+)
5. **Telemetry Client** - Anonymous usage stats (opt-in)

### Cloud Services (GCP)

**Technology Stack:**
- **API:** FastAPI (Python) on Cloud Run
- **Database:** Cloud SQL PostgreSQL (multi-tenant)
- **Cache:** Memorystore Redis (sessions, license cache)
- **Storage:** Cloud Storage (backups, artifacts)
- **Auth:** Firebase Auth + Custom JWT
- **Payments:** Stripe (subscriptions, invoicing)
- **CDN:** Cloud CDN (downloads, static assets)

**Key Services:**
1. **Auth Service** - User registration, login, SSO
2. **License Service** - Key generation, validation, quotas
3. **Billing Service** - Stripe integration, subscription lifecycle
4. **Sync Service** - MEMORY-CONTEXT sync, backups
5. **Analytics Service** - Usage tracking, dashboards
6. **Admin Portal** - User management, license management

---

## License Key Format

### Standard License Key (Pro/Team)
```
Format: CODITECT-{TYPE}-{HASH}-{CHECKSUM}

Example: CODITECT-PRO-A7F3E9D2C4B1-8F2A

Components:
- Prefix: CODITECT
- Type: FREE | PRO | TEAM | ENT
- Hash: 12-char random (encodes user_id, tier, expiration)
- Checksum: 4-char validation
```

**Validation Flow:**
```
1. Local Engine Startup
   ├─ Load license key from ~/.coditect/license.key
   ├─ Check local cache (~/.coditect/license.cache)
   │  └─ If cached and valid (<24h old) → Use cached validation
   └─ Else: Call cloud API
      POST /api/v1/licenses/validate
      {
        "license_key": "CODITECT-PRO-...",
        "machine_id": "sha256(hardware_id)",
        "version": "1.0.0"
      }

2. Cloud License Service
   ├─ Verify license key format and checksum
   ├─ Lookup license in database
   ├─ Check subscription status (active, expired, canceled)
   ├─ Check device count (Team tier: max 5 devices)
   ├─ Check usage quotas
   └─ Return validation result:
      {
        "valid": true,
        "tier": "PRO",
        "expires_at": "2026-11-23T00:00:00Z",
        "features": ["unlimited_commands", "cloud_sync", "all_agents"],
        "quotas": {"commands_per_day": -1}
      }

3. Local Engine
   ├─ Cache validation result (24 hour TTL)
   ├─ Enable features based on tier
   └─ Enforce quotas
```

### Enterprise License Key (On-Premise)
```
Format: CODITECT-ENT-{COMPANY}-{SEATS}-{EXPIRY}-{SIG}

Example: CODITECT-ENT-ACME-100-20261231-A7F3E9D2C4B1F8E2

Components:
- Type: ENT (Enterprise)
- Company: Short code (ACME, GOOG, etc)
- Seats: Licensed user count
- Expiry: YYYYMMDD (perpetual = 99991231)
- Signature: RSA signature (validates against AZ1.AI public key)
```

**Validation Flow (On-Premise):**
```
1. Customer's CODITECT Cloud
   ├─ License key embedded in Helm chart
   ├─ Validated on startup using AZ1.AI public key
   └─ Serves as internal license server

2. Employee's Local Engine
   ├─ Validates against internal license server
   ├─ No external internet required
   └─ Company controls user provisioning
```

---

## Data Residency & Compliance

### Data Storage Locations

**Local (User's Machine):**
- Project files (customer code, documents)
- MEMORY-CONTEXT messages (conversation history)
- LLM API keys (encrypted)
- License cache
- User preferences

**Cloud (CODITECT Servers):**
- User account information (email, name)
- License keys and subscription status
- Billing information (via Stripe)
- Sync'd MEMORY-CONTEXT (optional, Pro+)
- Usage telemetry (anonymous, opt-in)

**NOT Stored in Cloud:**
- Customer source code
- Customer project data
- LLM API keys
- Command outputs
- Chat conversations (unless sync enabled)

### Compliance

**GDPR (EU Users):**
- Data processing agreement available
- Right to access/delete user data
- Opt-in telemetry and analytics
- EU data residency option (GCP europe-west1)

**SOC 2 Type II (Enterprise):**
- Annual audit (target: 2026 Q3)
- Security controls documented
- Incident response procedures
- Access logging and monitoring

**ISO 27001 (Enterprise):**
- Information security management
- Risk assessment and treatment
- Security policy enforcement
- Target: 2027 Q1

---

## Offline Mode

### Graceful Degradation

**When Cloud is Unavailable:**
1. Use cached license validation (7 day grace period)
2. Disable cloud sync (data stays local)
3. Continue local execution (full functionality)
4. Queue telemetry for later upload (optional)

**Grace Period Logic:**
```python
def validate_license_offline(cached_validation):
    """
    Allow offline usage with cached license for 7 days.
    After 7 days, downgrade to free tier limits.
    """
    if cached_validation is None:
        return FreeTierLimits()

    cached_at = cached_validation['cached_at']
    age_days = (datetime.now() - cached_at).days

    if age_days <= 7:
        # Grace period: Use cached validation
        return cached_validation['features']
    else:
        # Grace period expired: Downgrade to free tier
        return FreeTierLimits()
```

**User Experience:**
```
$ coditect analyze
⚠️  Cloud validation unavailable. Using cached license (valid for 5 more days).
✅ Running analysis with PRO tier features...
```

---

## Migration Path

### From Current State → Hybrid Architecture

**Phase 1: User Management (2 weeks)**
- [ ] Design user database schema
- [ ] Implement registration/login API
- [ ] Build user management portal
- [ ] Integrate Firebase Auth

**Phase 2: Licensing System (2 weeks)**
- [ ] Design license key generation
- [ ] Implement license validation API
- [ ] Build license caching in local engine
- [ ] Add quota enforcement

**Phase 3: Payment Integration (1 week)**
- [ ] Integrate Stripe (subscriptions)
- [ ] Implement subscription lifecycle webhooks
- [ ] Build billing portal

**Phase 4: Local Engine Updates (2 weeks)**
- [ ] Add license manager to CLI
- [ ] Implement cloud validation on startup
- [ ] Add offline mode with grace period
- [ ] Build auto-update mechanism

**Phase 5: Cloud Sync (Optional - 2 weeks)**
- [ ] Design sync protocol
- [ ] Implement backup API
- [ ] Build conflict resolution
- [ ] Add multi-device support

**Total Timeline:** 8-10 weeks for full hybrid architecture

---

## Alternatives Considered

### Alternative 1: Pure Cloud SaaS (Rejected)

**Architecture:** Web-based IDE like Cursor Cloud, Replit
- Users work in browser or thin client
- All execution happens in cloud
- All data stored in cloud

**Rejected Because:**
- ❌ High latency for command execution
- ❌ Requires constant internet
- ❌ Privacy concerns (code in cloud)
- ❌ Higher infrastructure costs
- ❌ Doesn't differentiate from competitors

---

### Alternative 2: Pure Local (Rejected)

**Architecture:** Standalone desktop app like VS Code
- 100% local execution
- No cloud services
- License files distributed manually

**Rejected Because:**
- ❌ No SaaS revenue model
- ❌ Difficult license enforcement
- ❌ No collaboration features
- ❌ No telemetry or usage insights
- ❌ Complex license distribution (piracy risk)

---

### Alternative 3: Electron App + Cloud API (Rejected)

**Architecture:** Desktop app with heavy cloud reliance
- UI in Electron
- All processing in cloud
- Essentially web app wrapped in Electron

**Rejected Because:**
- ❌ Not truly "local-first"
- ❌ Requires internet for all features
- ❌ Higher cloud costs per user
- ❌ Worse performance than local execution

---

## Consequences

### Positive

✅ **Best of Both Worlds**
- Fast local execution (no latency)
- Cloud-based licensing and collaboration
- Works offline (with grace period)

✅ **Developer-Friendly**
- Privacy (code stays local)
- Performance (no cloud roundtrips)
- Familiar CLI/desktop experience

✅ **Business-Friendly**
- SaaS revenue model (recurring subscriptions)
- License enforcement (cloud validation)
- Usage analytics (product improvement)
- Upsell path (free → pro → team → enterprise)

✅ **Enterprise-Ready**
- On-premise deployment option
- Air-gapped support
- SSO integration
- Custom licensing

✅ **Competitive Positioning**
- Differentiated from pure cloud (Cursor, Copilot)
- Better privacy than cloud-first solutions
- More features than pure local tools

### Negative

❌ **Complexity**
- Two codebases to maintain (local engine + cloud services)
- More complex deployment and testing
- Sync conflicts and offline mode edge cases

❌ **Infrastructure Costs**
- Cloud infrastructure required (Auth, License, Sync)
- CDN for downloads
- Support for multiple platforms (Mac, Windows, Linux)

❌ **Development Time**
- 8-10 weeks additional development
- License validation system
- Cloud sync implementation
- Multi-platform builds and testing

### Risks & Mitigations

**Risk 1: Cloud Dependency Creates Friction**
- Mitigation: 7-day offline grace period
- Mitigation: Free tier with no cloud requirement
- Mitigation: Clear communication about cloud benefits

**Risk 2: License Validation Overhead**
- Mitigation: 24-hour cache (only 1 API call per day)
- Mitigation: Fast validation API (<100ms)
- Mitigation: Offline mode fallback

**Risk 3: Piracy / License Sharing**
- Mitigation: Device fingerprinting
- Mitigation: License seat limits (Team tier)
- Mitigation: Usage anomaly detection
- Mitigation: Focus on value, not DRM (honest customers pay)

**Risk 4: Multi-Platform Support Burden**
- Mitigation: Use cross-platform tools (Python, Electron/Tauri)
- Mitigation: Automated build pipelines (GitHub Actions)
- Mitigation: Community testing (beta programs)

---

## Success Metrics

### Technical Metrics
- License validation latency: <100ms (p95)
- Offline grace period: 7 days minimum
- Auto-update success rate: >95%
- Multi-platform support: Mac, Windows, Linux (all within 30 days of release)

### Business Metrics
- Free → Pro conversion: >5% (industry standard: 2-3%)
- Pro → Team conversion: >10%
- License compliance rate: >95% (minimal piracy)
- Customer satisfaction (NPS): >50

### Product Metrics
- Commands executed per user per day: >20 (Pro tier)
- Cloud sync adoption: >40% (Pro tier users)
- Feature utilization: >60% of paid features used monthly

---

## References

**Similar Hybrid Models:**
- Docker Desktop (local runtime + cloud hub)
- Figma Desktop (local performance + cloud collaboration)
- Postman (local collections + cloud sync)
- GitHub Desktop (local git + cloud remote)

**Industry Standards:**
- Stripe subscription management
- Firebase Auth for identity
- JWT for API authentication
- License key format: Keygen.sh patterns

**Related ADRs:**
- ADR-003: User Registration and Authentication
- ADR-004: Licensing and Entitlement System
- ADR-005: Multi-Tenancy Strategy
- ADR-006: Payment and Subscription Management

---

**Author:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC
**Reviewers:** Engineering Team
**Approved By:** Hal Casteel
**Date:** 2025-11-23
