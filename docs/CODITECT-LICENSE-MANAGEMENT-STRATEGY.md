# CODITECT Multi-Product License Management Strategy

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Author:** Hal Casteel, Founder/CEO/CTO
**Date:** 2025-11-17
**Status:** DRAFT - Architecture Decision Required

---

## Executive Summary

This document defines the complete license management and user provisioning strategy for the AZ1.AI CODITECT multi-product ecosystem, covering:
- Local CODITECT CLI/Framework (runs on user's machine)
- Cloud IDE (https://coditect.ai)
- Workflow App (https://workflow.coditect.ai)
- Future products (agent marketplace, analytics, etc.)

**Key Decision:** Use centralized license server with feature-flag based entitlements to support 1-to-N product access from a single license.

---

## Product Ecosystem Overview

### Current Products (3)

```
┌─────────────────────────────────────────────────────────────┐
│              AZ1.AI CODITECT PRODUCT FAMILY                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. LOCAL CODITECT (CLI/Framework)                         │
│     ├─ Installed: User's local machine (Mac/Linux/Windows) │
│     ├─ Runtime: Local Python/Git                           │
│     ├─ Data: ~/.coditect/ (local files)                    │
│     └─ Use Case: Offline development, local automation     │
│                                                             │
│  2. CLOUD IDE (https://coditect.ai)                        │
│     ├─ Deployed: GCP (serene-voltage-464305-n2)            │
│     ├─ Runtime: React + Theia + Rust backend               │
│     ├─ Data: FoundationDB (sessions, projects, state)      │
│     └─ Use Case: Browser-based IDE, collaboration          │
│                                                             │
│  3. WORKFLOW APP (https://workflow.coditect.ai)            │
│     ├─ Deployed: GCP (TBD - likely Cloud Run)              │
│     ├─ Runtime: React + FastAPI backend                    │
│     ├─ Data: PostgreSQL + FoundationDB                     │
│     └─ Use Case: Workflow automation, process management   │
│                                                             │
│  FUTURE: Agent Marketplace, Analytics, Custom Deployments  │
└─────────────────────────────────────────────────────────────┘
```

---

## Centralized License Server Architecture

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│         CENTRALIZED LICENSE & AUTH SERVER                    │
│              (api.coditect.ai)                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  PostgreSQL Cloud SQL (coditect-week1-pilot)                │
│  ├─ organizations (customer companies)                      │
│  ├─ users (individual users per org)                        │
│  ├─ licenses (one license per organization)                 │
│  │   └─ features (JSONB):                                   │
│  │       {                                                   │
│  │         "products": {                                     │
│  │           "local_cli": true,                             │
│  │           "cloud_ide": true,                             │
│  │           "workflow_app": false,                         │
│  │           "agent_marketplace": false                     │
│  │         },                                                │
│  │         "quotas": {                                       │
│  │           "max_users": 10,                               │
│  │           "max_projects": 100,                           │
│  │           "max_storage_gb": 50                           │
│  │         }                                                 │
│  │       }                                                   │
│  ├─ projects (shared across all products)                   │
│  └─ activations (track active sessions per product)         │
│                                                              │
│  FastAPI License Validation API                             │
│  ├─ POST /api/v1/auth/signup                                │
│  ├─ POST /api/v1/auth/login                                 │
│  ├─ POST /api/v1/licenses/validate                          │
│  ├─ POST /api/v1/licenses/activate                          │
│  ├─ GET  /api/v1/licenses/features                          │
│  └─ GET  /api/v1/users/me                                   │
└──────────────────────────────────────────────────────────────┘
         │                    │                    │
         │ HTTPS              │ HTTPS              │ HTTPS
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  LOCAL CLI      │  │  CLOUD IDE      │  │  WORKFLOW APP   │
│  (User's Mac)   │  │  (coditect.ai)  │  │  (workflow.     │
│                 │  │                 │  │   coditect.ai)  │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ • Auth via      │  │ • Auth via      │  │ • Auth via      │
│   device flow   │  │   email/password│  │   SSO           │
│ • Validates     │  │ • Validates     │  │ • Validates     │
│   license on    │  │   license on    │  │   license on    │
│   startup       │  │   login         │  │   login         │
│ • Stores token  │  │ • Stores JWT    │  │ • Stores JWT    │
│   locally       │  │   in browser    │  │   in browser    │
│ • Periodic      │  │ • Periodic      │  │ • Periodic      │
│   revalidation  │  │   revalidation  │  │   revalidation  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Complete User Provisioning Flows

### Flow 1: New Customer Signup (Self-Service)

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: USER VISITS SIGNUP PAGE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User navigates to: https://coditect.ai/signup            │
│                                                             │
│  Signup Form:                                              │
│  ├─ Email: user@company.com                               │
│  ├─ Password: ********                                     │
│  ├─ Company Name: Acme Corp                               │
│  └─ Plan Selection:                                        │
│      ☐ FREE (Local CLI only)                              │
│      ☐ PRO ($49/user/month - All products)                │
│      ☐ ENTERPRISE (Custom - Contact sales)                │
│                                                             │
│  User selects: ☑ PRO                                       │
│  User clicks: [Create Account]                             │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: BACKEND CREATES ACCOUNT                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FastAPI Backend (api.coditect.ai):                        │
│                                                             │
│  1. Create Organization:                                   │
│     INSERT INTO organizations (name, slug, plan)           │
│     VALUES ('Acme Corp', 'acme-corp', 'PRO')               │
│     → org_id: 550e8400-e29b-41d4-a716-446655440000         │
│                                                             │
│  2. Create User (OWNER role):                              │
│     INSERT INTO users (email, password_hash, org_id, role) │
│     VALUES ('user@company.com', '$2b$12$...', org_id, 'OWNER')│
│     → user_id: 6ba7b810-9dad-11d1-80b4-00c04fd430c8        │
│                                                             │
│  3. Generate License:                                      │
│     Key Format: CODITECT-{PLAN}-{YEAR}-{RANDOM}           │
│     Example: CODITECT-PRO-2024-X7Y8Z9A1                   │
│                                                             │
│     INSERT INTO licenses (key, type, org_id, features)     │
│     VALUES (                                               │
│       'CODITECT-PRO-2024-X7Y8Z9A1',                       │
│       'PRO',                                               │
│       org_id,                                              │
│       {                                                     │
│         "products": {                                       │
│           "local_cli": true,      ← PRO includes all      │
│           "cloud_ide": true,                              │
│           "workflow_app": true                            │
│         },                                                 │
│         "quotas": {                                        │
│           "max_users": 10,        ← PRO tier limits       │
│           "max_projects": 100,                            │
│           "max_storage_gb": 50                            │
│         },                                                 │
│         "expires_at": "2025-11-17T00:00:00Z"  ← 1 year    │
│       }                                                     │
│     )                                                      │
│                                                             │
│  4. Send Welcome Email:                                    │
│     To: user@company.com                                   │
│     Subject: "Welcome to CODITECT PRO"                     │
│     Body:                                                  │
│       - Account created                                    │
│       - License key: CODITECT-PRO-2024-X7Y8Z9A1           │
│       - Getting started links:                             │
│         • Local CLI: coditect.ai/docs/cli-setup           │
│         • Cloud IDE: coditect.ai (click to launch)        │
│         • Workflow: workflow.coditect.ai                  │
│                                                             │
│  5. Return Success Response:                               │
│     {                                                      │
│       "message": "Account created successfully",          │
│       "user_id": "6ba7b810-...",                          │
│       "organization_id": "550e8400-...",                  │
│       "license_key": "CODITECT-PRO-2024-X7Y8Z9A1",       │
│       "enabled_products": ["local_cli", "cloud_ide", "workflow_app"]│
│     }                                                      │
└─────────────────────────────────────────────────────────────┘
```

---

### Flow 2A: User Uses LOCAL CODITECT CLI

```
┌─────────────────────────────────────────────────────────────┐
│ INSTALLATION                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User's Machine:                                           │
│  $ pip install coditect-cli                                │
│  $ coditect --version                                      │
│  → CODITECT CLI v1.0.0                                     │
│                                                             │
│  $ coditect init my-project                                │
│  → Error: Authentication required                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ AUTHENTICATION (Device Flow)                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  $ coditect login                                          │
│                                                             │
│  CLI Output:                                               │
│  ┌───────────────────────────────────────────┐            │
│  │ Opening browser for authentication...     │            │
│  │                                            │            │
│  │ If browser doesn't open, visit:           │            │
│  │ https://coditect.ai/auth/device           │            │
│  │                                            │            │
│  │ Enter code: A1B2-C3D4                     │            │
│  │                                            │            │
│  │ Waiting for authentication...             │            │
│  └───────────────────────────────────────────┘            │
│                                                             │
│  Browser Opens → https://coditect.ai/auth/device          │
│  User sees:                                                │
│  ┌───────────────────────────────────────────┐            │
│  │ Authorize CODITECT CLI                    │            │
│  │                                            │            │
│  │ Device Code: A1B2-C3D4                    │            │
│  │                                            │            │
│  │ Email: user@company.com                   │            │
│  │ Password: ********                         │            │
│  │                                            │            │
│  │ [Authorize CLI] [Cancel]                  │            │
│  └───────────────────────────────────────────┘            │
│                                                             │
│  User clicks [Authorize CLI]                               │
│                                                             │
│  Backend (api.coditect.ai):                                │
│  1. Validates email/password                               │
│  2. Checks license:                                        │
│     SELECT features->'products'->>'local_cli'             │
│     FROM licenses WHERE organization_id = user.org_id      │
│     → Result: true ✅                                      │
│                                                             │
│  3. Generates API Token (long-lived):                     │
│     {                                                      │
│       "user_id": "6ba7b810-...",                          │
│       "organization_id": "550e8400-...",                  │
│       "license_id": "abc123...",                          │
│       "scopes": ["local_cli"],                            │
│       "expires_at": "2026-11-17T00:00:00Z"  ← 1 year     │
│     }                                                      │
│     Token (JWT): eyJhbGciOiJIUzI1NiIs...                  │
│                                                             │
│  4. Returns token to CLI                                   │
│                                                             │
│  CLI receives token:                                       │
│  ┌───────────────────────────────────────────┐            │
│  │ ✅ Authentication successful!              │            │
│  │                                            │            │
│  │ Logged in as: user@company.com            │            │
│  │ Organization: Acme Corp                   │            │
│  │ Plan: PRO                                  │            │
│  │ Enabled products:                          │            │
│  │   • Local CLI ✅                           │            │
│  │   • Cloud IDE ✅                           │            │
│  │   • Workflow App ✅                        │            │
│  │                                            │            │
│  │ Token stored: ~/.coditect/credentials     │            │
│  └───────────────────────────────────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ USAGE (CLI operates locally)                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  $ coditect init my-project                                │
│                                                             │
│  CLI:                                                      │
│  1. Reads token from ~/.coditect/credentials               │
│  2. Validates token with License Server:                   │
│     POST api.coditect.ai/api/v1/licenses/validate         │
│     Headers: Authorization: Bearer eyJhbGci...             │
│                                                             │
│     Response:                                              │
│     {                                                      │
│       "valid": true,                                       │
│       "organization": "Acme Corp",                         │
│       "plan": "PRO",                                       │
│       "features": {                                        │
│         "local_cli": true,                                │
│         "cloud_ide": true,                                │
│         "workflow_app": true                              │
│       },                                                   │
│       "expires_at": "2025-11-17T00:00:00Z"                │
│     }                                                      │
│                                                             │
│  3. If valid → Proceed with local operations              │
│     Creates: my-project/.coditect/                        │
│              my-project/PROJECT-PLAN.md                   │
│              my-project/TASKLIST.md                       │
│                                                             │
│  4. All work happens LOCALLY (no cloud dependency)        │
│     - Uses local .coditect framework                      │
│     - Stores files locally                                │
│     - Runs AI agents locally                              │
│                                                             │
│  Note: CLI revalidates license:                           │
│  - On startup (coditect command)                          │
│  - Every 24 hours (background check)                      │
│  - Cached for offline use (7-day grace period)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Flow 2B: User Uses CLOUD IDE (https://coditect.ai)

```
┌─────────────────────────────────────────────────────────────┐
│ ACCESS                                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User navigates to: https://coditect.ai                    │
│                                                             │
│  Login Page:                                               │
│  ┌───────────────────────────────────────────┐            │
│  │ CODITECT Cloud IDE                        │            │
│  │                                            │            │
│  │ Email: user@company.com                   │            │
│  │ Password: ********                         │            │
│  │                                            │            │
│  │ [Sign In] [Sign Up] [Forgot Password?]   │            │
│  └───────────────────────────────────────────┘            │
│                                                             │
│  User clicks [Sign In]                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ AUTHENTICATION & LICENSE VALIDATION                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  POST api.coditect.ai/api/v1/auth/login                    │
│  {                                                          │
│    "email": "user@company.com",                            │
│    "password": "********"                                  │
│  }                                                          │
│                                                             │
│  Backend (FastAPI):                                        │
│  1. Validate credentials:                                  │
│     SELECT * FROM users WHERE email = 'user@company.com'   │
│     → Verify bcrypt password hash                          │
│                                                             │
│  2. Check license features:                                │
│     SELECT l.features->'products'->>'cloud_ide' AS allowed │
│     FROM licenses l                                        │
│     JOIN users u ON u.organization_id = l.organization_id  │
│     WHERE u.id = '6ba7b810-...'                            │
│     → Result: true ✅                                      │
│                                                             │
│  3. Check license validity:                                │
│     - Is license ACTIVE? ✅                                │
│     - Is license not expired? ✅                           │
│     - Are we under max_users quota? (3/10 used) ✅         │
│                                                             │
│  4. Generate JWT tokens:                                   │
│     Access Token (short-lived, 1 hour):                    │
│     {                                                      │
│       "user_id": "6ba7b810-...",                          │
│       "organization_id": "550e8400-...",                  │
│       "email": "user@company.com",                        │
│       "role": "OWNER",                                     │
│       "features": {                                        │
│         "cloud_ide": true,                                │
│         "local_cli": true,                                │
│         "workflow_app": true                              │
│       },                                                   │
│       "exp": 1700000000  ← 1 hour from now                │
│     }                                                      │
│                                                             │
│     Refresh Token (long-lived, 7 days)                    │
│                                                             │
│  5. Create activation record:                              │
│     INSERT INTO activations (user_id, product, device)     │
│     VALUES ('6ba7b810-...', 'cloud_ide', 'Chrome/Mac')    │
│                                                             │
│  6. Return tokens:                                         │
│     {                                                      │
│       "access_token": "eyJhbGci...",                      │
│       "refresh_token": "eyJhbGci...",                     │
│       "token_type": "bearer",                             │
│       "expires_in": 3600,                                 │
│       "user": {                                            │
│         "id": "6ba7b810-...",                             │
│         "email": "user@company.com",                      │
│         "organization": "Acme Corp",                      │
│         "plan": "PRO"                                      │
│       }                                                    │
│     }                                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ LOAD IDE                                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend (React):                                         │
│  1. Stores JWT in memory + secure httpOnly cookie          │
│  2. Loads IDE UI (Theia-based editor)                     │
│  3. Connects to backend WebSocket for real-time features   │
│                                                             │
│  Backend (Rust + FoundationDB):                            │
│  1. Validates JWT on every WebSocket message               │
│  2. Loads user session from FoundationDB:                  │
│     - Open projects                                        │
│     - Recent files                                         │
│     - IDE preferences                                      │
│  3. Enforces RLS (organization_id from JWT)                │
│  4. User works in browser IDE                              │
│                                                             │
│  Periodic License Revalidation:                            │
│  - Every 1 hour: Check license still valid                 │
│  - If expired → Show upgrade prompt, disable editing       │
│  - If revoked → Force logout                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Flow 2C: User Uses WORKFLOW APP (https://workflow.coditect.ai)

```
┌─────────────────────────────────────────────────────────────┐
│ ACCESS (SSO from main auth)                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Scenario 1: User already logged in to coditect.ai        │
│  --------------------------------------------------------  │
│                                                             │
│  User visits: https://workflow.coditect.ai                 │
│                                                             │
│  Workflow App (Frontend):                                  │
│  1. Checks for existing session cookie from *.coditect.ai  │
│  2. Finds JWT token (shared cookie domain)                 │
│  3. Validates token with License Server:                   │
│     GET api.coditect.ai/api/v1/users/me                    │
│     Headers: Authorization: Bearer eyJhbGci...             │
│                                                             │
│  4. Backend checks license.features.workflow_app:          │
│     → true ✅ (PRO plan includes workflow app)             │
│                                                             │
│  5. Loads Workflow App UI (no login required)              │
│                                                             │
│  --------------------------------------------------------  │
│  Scenario 2: User NOT logged in                           │
│  --------------------------------------------------------  │
│                                                             │
│  User visits: https://workflow.coditect.ai                 │
│                                                             │
│  Workflow App:                                             │
│  1. No session found                                       │
│  2. Redirects to: https://coditect.ai/login?              │
│                   redirect=workflow.coditect.ai            │
│  3. User logs in at coditect.ai                            │
│  4. After login → Redirected back to workflow.coditect.ai  │
│  5. Workflow app validates token (same as Scenario 1)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## License Tier Definitions

### Proposed License Tiers

```yaml
FREE_TIER:
  price: $0/month
  max_users: 1
  products:
    local_cli: true
    cloud_ide: false         # ❌ Not included
    workflow_app: false      # ❌ Not included
  quotas:
    max_projects: 3
    max_storage_gb: 1
    max_ai_requests_per_month: 100
  support: community
  features:
    - Local CLI access only
    - Limited AI agent usage
    - Community support
    - Public project templates

PRO_TIER:
  price: $49/user/month
  max_users: unlimited (pay per user)
  products:
    local_cli: true
    cloud_ide: true          # ✅ Included
    workflow_app: true       # ✅ Included
  quotas:
    max_projects: 100
    max_storage_gb: 50
    max_ai_requests_per_month: 10000
  support: email (24h response)
  features:
    - All products enabled
    - Priority AI processing
    - Email support
    - Private project templates
    - Team collaboration
    - Advanced analytics

ENTERPRISE_TIER:
  price: Custom (contact sales)
  max_users: unlimited
  products:
    local_cli: true
    cloud_ide: true
    workflow_app: true
    agent_marketplace: true   # ✅ Custom agents
    advanced_analytics: true  # ✅ Analytics dashboard
    on_premise_option: true   # ✅ Self-hosted
  quotas:
    max_projects: -1          # Unlimited
    max_storage_gb: -1        # Unlimited
    max_ai_requests_per_month: -1  # Unlimited
  support: priority (4h response, dedicated account manager)
  features:
    - All PRO features
    - Custom AI agent development
    - On-premise deployment option
    - SSO (SAML, OAuth)
    - Advanced security (audit logs, compliance)
    - Custom integrations
    - Dedicated infrastructure
    - SLA guarantees (99.9% uptime)
```

---

## License Provisioning Processes

### Process 1: Self-Service (Automated)

```
USER ACTION → SYSTEM RESPONSE

1. User signs up at https://coditect.ai/signup
   ├─ Selects plan: FREE, PRO
   └─ Enters payment (if PRO)

2. Backend auto-provisions:
   ├─ Creates organization
   ├─ Creates first user (OWNER)
   ├─ Generates license key
   ├─ Sets features based on plan
   ├─ If PRO: Creates Stripe subscription
   └─ Sends welcome email with license key

3. User immediately has access to entitled products
   ├─ FREE: Can install CLI immediately
   └─ PRO: Can access CLI + Cloud IDE + Workflow

TIME TO ACTIVATION: <60 seconds
```

### Process 2: Sales-Led (Manual)

```
SALES PROCESS → ADMIN ACTION

1. Sales team qualifies enterprise customer
   ├─ Custom requirements gathered
   ├─ Pricing negotiated
   └─ Contract signed

2. Admin creates custom license via Admin Dashboard:
   ├─ Organization: customer.company.com
   ├─ Plan: ENTERPRISE
   ├─ Custom features:
   │   ├─ All products: true
   │   ├─ max_users: 100 (or unlimited)
   │   ├─ max_storage_gb: 500
   │   ├─ custom_features: ["sso", "audit_logs", "on_premise"]
   │   └─ expires_at: 2026-12-31 (annual)
   └─ Generate license: CODITECT-ENT-2024-CUSTOM123

3. Sales sends license key + onboarding materials

4. Customer IT team:
   ├─ Receives license key
   ├─ Configures SSO (if applicable)
   ├─ Invites users to organization
   └─ All users activate with same license

TIME TO ACTIVATION: 1-5 business days
```

### Process 3: Trial (Temporary Access)

```
TRIAL REQUEST → AUTO-PROVISION

1. User requests PRO trial at https://coditect.ai/trial
   ├─ No payment required
   └─ Email verification only

2. Backend creates 14-day trial license:
   ├─ Plan: PRO_TRIAL
   ├─ Features: Same as PRO
   ├─ expires_at: NOW() + 14 days
   ├─ auto_downgrade: true (→ FREE after expiration)
   └─ License key: CODITECT-TRIAL-2024-XYZ

3. User has full PRO access for 14 days

4. On day 14:
   ├─ If user upgraded → No change
   └─ If no upgrade → Auto-downgrade to FREE
       ├─ Cloud IDE access disabled
       ├─ Workflow app access disabled
       └─ Local CLI still works

TIME TO ACTIVATION: <60 seconds
CONVERSION WINDOW: 14 days
```

---

## Multi-Product Access Matrix

### Access Control Table

| Plan | Local CLI | Cloud IDE | Workflow | Marketplace | Analytics | On-Premise |
|------|-----------|-----------|----------|-------------|-----------|------------|
| **FREE** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **PRO** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **ENTERPRISE** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

### Implementation (PostgreSQL Schema)

```sql
-- licenses table features JSONB column
{
  "products": {
    "local_cli": true,
    "cloud_ide": false,
    "workflow_app": false,
    "agent_marketplace": false,
    "advanced_analytics": false,
    "on_premise": false
  },
  "quotas": {
    "max_users": 1,
    "max_projects": 3,
    "max_storage_gb": 1
  },
  "custom_features": []
}

-- Each product checks its own flag:
SELECT features->'products'->>'cloud_ide' AS allowed
FROM licenses
WHERE organization_id = ?
-- Returns: "true" or "false"
```

---

## Future Product Extensibility

### Adding New Product (Example: Agent Marketplace)

```
STEP 1: Update License Schema
├─ Add new feature flag: features.products.agent_marketplace
├─ Define which tiers include it (ENTERPRISE only)
└─ No database migration needed (JSONB is flexible)

STEP 2: Deploy New Product
├─ Deploy: https://marketplace.coditect.ai
├─ Implement license check on login:
│   GET api.coditect.ai/api/v1/licenses/features
│   → Check: features.products.agent_marketplace
└─ If false → Show "Upgrade to Enterprise" page

STEP 3: Update Documentation
├─ Add to pricing page
├─ Update license tier definitions
└─ Inform existing customers

STEP 4: Upsell to Existing Customers
├─ Enterprise customers: Auto-enabled (already paying)
├─ PRO customers: Email campaign → "New feature available"
└─ FREE customers: Upgrade prompt in dashboard

TIME TO ADD NEW PRODUCT: <1 week (no license system changes)
```

---

## Technical Implementation Details

### License Validation Flow (Backend)

```python
# FastAPI endpoint (in services/license_service.py)

async def validate_product_access(
    user_id: UUID,
    product: str  # "local_cli", "cloud_ide", "workflow_app", etc.
) -> bool:
    """
    Validate if user has access to specific product.

    Args:
        user_id: User UUID
        product: Product identifier

    Returns:
        True if user has access, False otherwise
    """
    # Get user's organization
    user = await db.get(User, user_id)

    # Get organization's license
    license = await db.query(License).filter(
        License.organization_id == user.organization_id
    ).first()

    # Check license validity
    if not license:
        return False

    if license.status != "ACTIVE":
        return False

    if license.expires_at and license.expires_at < datetime.utcnow():
        return False

    # Check product-specific access
    product_enabled = license.features.get("products", {}).get(product, False)

    return product_enabled


# Usage in API endpoints:

@app.get("/api/v1/cloud-ide/dashboard")
async def cloud_ide_dashboard(current_user: User = Depends(get_current_user)):
    # Validate access to cloud IDE
    has_access = await validate_product_access(
        current_user.id,
        "cloud_ide"
    )

    if not has_access:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "product_access_denied",
                "message": "Your plan does not include Cloud IDE access",
                "upgrade_url": "https://coditect.ai/pricing"
            }
        )

    # Continue with dashboard logic...
    return {"dashboard": "data"}
```

### JWT Token Structure

```json
{
  "user_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "organization_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@company.com",
  "role": "OWNER",
  "plan": "PRO",
  "features": {
    "products": {
      "local_cli": true,
      "cloud_ide": true,
      "workflow_app": true
    }
  },
  "license_id": "abc123-def456-ghi789",
  "exp": 1700000000,
  "iat": 1699996400,
  "iss": "api.coditect.ai",
  "sub": "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
}
```

Each product can decode the JWT and check `features.products.{product_name}` to determine access.

---

## Security Considerations

### Preventing License Abuse

1. **Activation Limits**
```sql
-- Track active sessions per product
CREATE TABLE activations (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    product TEXT NOT NULL,  -- "local_cli", "cloud_ide", etc.
    device_id TEXT,
    device_name TEXT,
    ip_address INET,
    created_at TIMESTAMP DEFAULT NOW(),
    last_seen_at TIMESTAMP DEFAULT NOW()
);

-- Enforce max_activations from license.quotas.max_users
-- If exceeded → Deny new activation, show "Too many devices" error
```

2. **License Sharing Prevention**
- Track IP addresses and device fingerprints
- Alert on suspicious patterns (e.g., 10 IPs in 1 hour)
- Require re-authentication if device changes

3. **Token Expiration**
- Access tokens: 1 hour (must refresh)
- Refresh tokens: 7 days (must re-login)
- API tokens (CLI): 1 year (can revoke anytime)

4. **License Revocation**
- Admin can instantly revoke license
- All products check license on next request
- Real-time revocation (WebSocket notification)

---

## Billing Integration (Stripe)

### Subscription Lifecycle

```
USER UPGRADES TO PRO
├─ Frontend: Stripe Checkout session
├─ User pays $49/month
├─ Stripe webhook: subscription.created
├─ Backend updates license:
│   ├─ SET plan = 'PRO'
│   ├─ SET features.products.cloud_ide = true
│   ├─ SET features.products.workflow_app = true
│   └─ SET stripe_subscription_id = 'sub_...'
└─ User immediately gains access (no delay)

MONTHLY RENEWAL
├─ Stripe auto-charges on renewal date
├─ Stripe webhook: invoice.paid
├─ Backend extends license:
│   └─ SET expires_at = NOW() + INTERVAL '1 month'

PAYMENT FAILURE
├─ Stripe webhook: invoice.payment_failed
├─ Backend:
│   ├─ Email user: "Payment failed, please update card"
│   ├─ Grace period: 7 days
│   └─ If still failed after 7 days:
│       ├─ SET license.status = 'SUSPENDED'
│       ├─ User loses access to Cloud IDE + Workflow
│       └─ Local CLI downgrades to FREE features

USER CANCELS SUBSCRIPTION
├─ Stripe webhook: subscription.canceled
├─ Backend:
│   ├─ SET license.status = 'CANCELED'
│   ├─ Allow access until end of billing period
│   └─ After period ends → Auto-downgrade to FREE
```

---

## Open Questions / Decisions Needed

### 1. License Key Format
**Options:**
- A) `CODITECT-{PLAN}-{YEAR}-{RANDOM8}` (e.g., `CODITECT-PRO-2024-X7Y8Z9A1`)
- B) UUID-based (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- C) Hybrid (e.g., `CODITECT-550e8400-e29b-41d4`)

**Recommendation:** Option A (human-readable, marketing-friendly)

### 2. License Server URL
**Options:**
- A) `api.coditect.ai` (centralized API for all services)
- B) `licenses.coditect.ai` (dedicated license server)
- C) `auth.coditect.ai` (authentication + licensing)

**Recommendation:** Option A (simpler architecture, fewer domains)

### 3. Pricing Model
**Options:**
- A) Per-user/month (e.g., $49/user/month for PRO)
- B) Per-organization/month (e.g., $99/month for up to 10 users)
- C) Usage-based (e.g., $0.01 per AI request)

**Recommendation:** Option A for PRO, Option B for ENTERPRISE

### 4. Trial Duration
**Options:**
- A) 14 days (industry standard)
- B) 30 days (generous, higher conversion)
- C) 7 days (shorter sales cycle)

**Recommendation:** Option A (14 days)

### 5. Downgrade Policy
**When user cancels PRO, should they:**
- A) Immediately lose access to Cloud IDE/Workflow?
- B) Keep access until end of billing period?
- C) Keep access for 30 days (grace period)?

**Recommendation:** Option B (keep until billing period ends)

---

## Implementation Checklist

### Phase 1: Core License Management (Week 1 - Current)
- [x] PostgreSQL schema (organizations, users, licenses)
- [x] FastAPI authentication (signup, login)
- [ ] License validation API endpoints
- [ ] Feature flag checking logic
- [ ] JWT token generation with product features

### Phase 2: Product Integration (Week 2-3)
- [ ] Cloud IDE license check on login
- [ ] Workflow app license check on login
- [ ] Local CLI device authentication flow
- [ ] Local CLI license validation

### Phase 3: Billing Integration (Week 4)
- [ ] Stripe subscription creation
- [ ] Stripe webhook handlers
- [ ] Payment failure handling
- [ ] Subscription cancellation flow

### Phase 4: Admin Dashboard (Week 5)
- [ ] Admin UI for license management
- [ ] User invite system
- [ ] Usage analytics dashboard
- [ ] License key regeneration

### Phase 5: Advanced Features (Week 6+)
- [ ] SSO integration (SAML, OAuth)
- [ ] Audit logging
- [ ] License usage analytics
- [ ] Custom enterprise features

---

## Conclusion

This license management strategy provides:

✅ **Unified Authentication** - Single login across all products
✅ **Flexible Licensing** - Support for 1-to-N product access
✅ **Scalable Architecture** - Easy to add new products
✅ **Multiple Tiers** - FREE, PRO, ENTERPRISE
✅ **Self-Service** - Automated provisioning
✅ **Enterprise-Ready** - Custom features, SSO, audit logs

**Next Steps:**
1. Review and approve this strategy
2. Confirm license tier pricing
3. Continue FastAPI implementation (license validation endpoints)
4. Test complete user provisioning flows

**Status:** DRAFT - Awaiting approval to proceed with implementation

---

**Author:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
**Date:** 2025-11-17
**Version:** 1.0
