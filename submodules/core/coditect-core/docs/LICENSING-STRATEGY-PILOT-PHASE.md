# CODITECT Licensing Strategy - Pilot Phase Control

## Executive Summary

**Challenge:** Maintain control over CODITECT deployment during pilot phase when distributing Python source code (not compiled binary).

**Solution:** Multi-layered licensing system with online validation, hardware fingerprinting, and graceful degradation.

**Goal:** Bridge pilot phase to enterprise Multi-Agent Platform as a Service (MAPaaS) with full SaaS licensing.

---

## 1. Strategic Requirements

### 1.1 Pilot Phase Control (Immediate Need)

| Requirement | Priority | Rationale |
|------------|----------|-----------|
| License key required to run | P0 | Prevent unauthorized use |
| Online validation | P0 | Central control and revocation |
| Usage tracking | P0 | Understand pilot user behavior |
| Time-limited licenses | P0 | Pilot phase expiration |
| User identity binding | P1 | Know who is using the system |
| Hardware fingerprinting | P1 | Prevent key sharing |
| Feature gating | P1 | Control which features available |
| Offline grace period | P2 | Allow offline work (48-72 hours) |

### 1.2 Transition to Enterprise SaaS

**Pilot Phase (Now):**
- Self-hosted Python source code
- License key validation
- Limited pilot users (50-100)

**Production Phase (3-6 months):**
- Cloud-hosted SaaS platform
- Multi-tenant architecture
- Subscription-based pricing
- OAuth/SSO integration

**Enterprise Phase (6-12 months):**
- On-premise deployment option
- Floating licenses
- Enterprise SSO
- Audit trails and compliance

---

## 2. Licensing Architecture

### 2.1 License Key Format

**Structure:**
```
CODITECT-{VERSION}-{USER_TYPE}-{RANDOM}-{CHECKSUM}

Example:
CODITECT-PILOT-TEAM-A7F2-E9D1B3C4
```

**Components:**
- `CODITECT`: Product identifier
- `PILOT/PROD/ENTERPRISE`: License tier
- `TEAM/INDIVIDUAL/CONSULTANT/AUDITOR`: User type
- `A7F2`: Random component (16-bit)
- `E9D1B3C4`: Checksum (CRC32)

### 2.2 License Server Architecture

```
┌──────────────────────────────────────────────────────┐
│                   CODITECT Client                     │
│  ┌────────────────────────────────────────────────┐  │
│  │  1. Startup: Check license.json                │  │
│  │  2. Validate locally (offline check)           │  │
│  │  3. If expired or missing, call license server │  │
│  │  4. Hardware fingerprint validation            │  │
│  │  5. Usage telemetry (opt-in)                   │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────┬───────────────────────────────────┘
                   │
                   │ HTTPS POST
                   │ {license_key, hardware_id, version}
                   ▼
┌──────────────────────────────────────────────────────┐
│            CODITECT License Server (GCP)              │
│  ┌────────────────────────────────────────────────┐  │
│  │  Cloud Run Service (FastAPI)                   │  │
│  │  ├─ /validate    - Validate license key        │  │
│  │  ├─ /activate    - Activate license            │  │
│  │  ├─ /deactivate  - Deactivate license          │  │
│  │  ├─ /refresh     - Refresh validation          │  │
│  │  └─ /telemetry   - Usage analytics (opt-in)    │  │
│  └────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────┐  │
│  │  PostgreSQL (Cloud SQL)                        │  │
│  │  ├─ licenses table                             │  │
│  │  ├─ activations table                          │  │
│  │  ├─ usage_logs table                           │  │
│  │  └─ feature_gates table                        │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### 2.3 Database Schema

#### licenses table
```sql
CREATE TABLE licenses (
    license_key VARCHAR(50) PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    user_name VARCHAR(255),
    organization VARCHAR(255),
    user_type VARCHAR(50),  -- team, individual, consultant, auditor
    license_tier VARCHAR(50), -- pilot, prod, enterprise
    issued_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    max_activations INT DEFAULT 1,
    features_enabled TEXT[],  -- Array of enabled features
    status VARCHAR(50),  -- active, revoked, expired
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### activations table
```sql
CREATE TABLE activations (
    id SERIAL PRIMARY KEY,
    license_key VARCHAR(50) REFERENCES licenses(license_key),
    hardware_id VARCHAR(64) NOT NULL,  -- SHA-256 of hardware fingerprint
    machine_name VARCHAR(255),
    ip_address INET,
    coditect_version VARCHAR(50),
    activated_at TIMESTAMP DEFAULT NOW(),
    last_validated_at TIMESTAMP DEFAULT NOW(),
    validation_count INT DEFAULT 0,
    status VARCHAR(50),  -- active, deactivated
    UNIQUE(license_key, hardware_id)
);
```

#### usage_logs table
```sql
CREATE TABLE usage_logs (
    id SERIAL PRIMARY KEY,
    license_key VARCHAR(50) REFERENCES licenses(license_key),
    event_type VARCHAR(100),  -- startup, agent_invoked, session_exported
    event_data JSONB,
    timestamp TIMESTAMP DEFAULT NOW(),
    coditect_version VARCHAR(50)
);
```

---

## 3. Implementation Strategy

### 3.1 Client-Side License Validation

**File:** `scripts/core/license_manager.py`

```python
#!/usr/bin/env python3
"""
CODITECT License Manager

Validates license keys, manages activation, and enforces licensing constraints.
Includes offline grace period and hardware fingerprinting.
"""

import os
import sys
import json
import hashlib
import platform
import socket
import uuid
from pathlib import Path
from datetime import datetime, timedelta
import urllib.request
import urllib.error

class LicenseManager:
    """Manage CODITECT licensing and validation"""

    def __init__(self, license_server_url="https://license.coditect.ai"):
        self.license_server_url = license_server_url
        self.license_file = Path.home() / ".coditect" / "license.json"
        self.license_file.parent.mkdir(exist_ok=True)

        # Grace period for offline operation
        self.offline_grace_period = timedelta(days=3)

    def get_hardware_id(self) -> str:
        """Generate unique hardware fingerprint"""
        # Combine multiple hardware identifiers
        mac = uuid.getnode()  # MAC address
        hostname = socket.gethostname()
        system = platform.system()
        machine = platform.machine()

        fingerprint = f"{mac}:{hostname}:{system}:{machine}"
        return hashlib.sha256(fingerprint.encode()).hexdigest()

    def load_license(self) -> dict:
        """Load license from local file"""
        if not self.license_file.exists():
            return None

        try:
            with open(self.license_file, 'r') as f:
                return json.load(f)
        except Exception:
            return None

    def save_license(self, license_data: dict):
        """Save license to local file"""
        with open(self.license_file, 'w') as f:
            json.dump(license_data, f, indent=2)

    def validate_offline(self, license_data: dict) -> bool:
        """Validate license without server (grace period)"""
        if not license_data:
            return False

        # Check expiration
        expires_at = datetime.fromisoformat(license_data.get('expires_at', ''))
        if datetime.now() > expires_at:
            return False

        # Check last validation (grace period)
        last_validated = datetime.fromisoformat(license_data.get('last_validated', ''))
        if datetime.now() - last_validated > self.offline_grace_period:
            return False  # Need online validation

        # Check hardware ID
        if license_data.get('hardware_id') != self.get_hardware_id():
            return False  # License tied to different machine

        return True

    def validate_online(self, license_key: str) -> tuple:
        """Validate license with server"""
        try:
            # Prepare request
            url = f"{self.license_server_url}/validate"
            data = json.dumps({
                'license_key': license_key,
                'hardware_id': self.get_hardware_id(),
                'coditect_version': self.get_coditect_version(),
                'machine_name': socket.gethostname()
            }).encode()

            req = urllib.request.Request(url, data=data, method='POST')
            req.add_header('Content-Type', 'application/json')

            # Make request
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())

                if result.get('valid'):
                    # Save license locally
                    license_data = {
                        'license_key': license_key,
                        'hardware_id': self.get_hardware_id(),
                        'expires_at': result['expires_at'],
                        'features_enabled': result.get('features_enabled', []),
                        'last_validated': datetime.now().isoformat(),
                        'user_name': result.get('user_name'),
                        'organization': result.get('organization')
                    }
                    self.save_license(license_data)

                    return True, result.get('message', 'License valid')
                else:
                    return False, result.get('message', 'License invalid')

        except urllib.error.HTTPError as e:
            if e.code == 403:
                return False, "License revoked or invalid"
            elif e.code == 404:
                return False, "License key not found"
            else:
                return False, f"Server error: {e.code}"

        except Exception as e:
            # Network error - try offline validation
            license_data = self.load_license()
            if license_data and self.validate_offline(license_data):
                return True, "License valid (offline mode)"
            else:
                return False, f"License validation failed: {e}"

    def validate(self) -> tuple:
        """Main validation entry point"""
        # Check for license file first
        license_data = self.load_license()

        # Try offline validation first (faster)
        if license_data and self.validate_offline(license_data):
            return True, "License valid"

        # Need online validation
        if not license_data:
            license_key = self.prompt_for_license_key()
            if not license_key:
                return False, "No license key provided"
        else:
            license_key = license_data.get('license_key')

        # Validate online
        return self.validate_online(license_key)

    def prompt_for_license_key(self) -> str:
        """Prompt user for license key"""
        print("\n" + "="*70)
        print("CODITECT LICENSE ACTIVATION")
        print("="*70)
        print("\nNo valid license found. Please enter your license key.")
        print("To obtain a license key, visit: https://coditect.ai/pilot")
        print()
        license_key = input("License Key: ").strip()
        return license_key

    def get_coditect_version(self) -> str:
        """Get current CODITECT version"""
        # Read from VERSION file or package metadata
        version_file = Path(__file__).parent.parent / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "1.0.0"

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled for this license"""
        license_data = self.load_license()
        if not license_data:
            return False

        features = license_data.get('features_enabled', [])
        return feature in features

    def log_usage(self, event_type: str, event_data: dict = None):
        """Log usage event (opt-in telemetry)"""
        license_data = self.load_license()
        if not license_data:
            return

        # Only log if telemetry enabled
        if not license_data.get('telemetry_enabled', False):
            return

        try:
            url = f"{self.license_server_url}/telemetry"
            data = json.dumps({
                'license_key': license_data.get('license_key'),
                'event_type': event_type,
                'event_data': event_data or {},
                'timestamp': datetime.now().isoformat(),
                'coditect_version': self.get_coditect_version()
            }).encode()

            req = urllib.request.Request(url, data=data, method='POST')
            req.add_header('Content-Type', 'application/json')

            # Fire and forget (non-blocking)
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass  # Silent failure for telemetry


def require_license(func):
    """Decorator to enforce licensing on functions"""
    def wrapper(*args, **kwargs):
        license_manager = LicenseManager()
        valid, message = license_manager.validate()

        if not valid:
            print(f"\n❌ {message}")
            print("\nCODITECT requires a valid license to operate.")
            print("Please visit https://coditect.ai/pilot to obtain a license key.")
            sys.exit(1)

        return func(*args, **kwargs)

    return wrapper
```

### 3.2 Integration with CODITECT Core

**Update:** `scripts/coditect-setup.py`

```python
# Add at top of file
from core.license_manager import LicenseManager, require_license

class CoditectSetup:
    def __init__(self):
        # ... existing code ...

        # Add license manager
        self.license_manager = LicenseManager()

    @require_license
    def run(self) -> int:
        """Main setup flow - now requires valid license"""
        # Existing setup code continues...
```

**Update:** Main agent invocation

```python
# scripts/coditect-router (AI command router)
from core.license_manager import LicenseManager

def main():
    # Validate license at startup
    license_manager = LicenseManager()
    valid, message = license_manager.validate()

    if not valid:
        print(f"❌ {message}")
        print("CODITECT requires a valid license.")
        sys.exit(1)

    # License valid, log usage
    license_manager.log_usage('coditect_router_invoked')

    # Continue with normal operation...
```

### 3.3 License Server Implementation

**File:** `license-server/main.py` (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import secrets

app = FastAPI()

class LicenseValidationRequest(BaseModel):
    license_key: str
    hardware_id: str
    coditect_version: str
    machine_name: str

class LicenseValidationResponse(BaseModel):
    valid: bool
    message: str
    expires_at: str = None
    features_enabled: list = []
    user_name: str = None
    organization: str = None

@app.post("/validate", response_model=LicenseValidationResponse)
async def validate_license(req: LicenseValidationRequest):
    """Validate license key and hardware binding"""

    # Query database
    license = await db.fetch_one(
        "SELECT * FROM licenses WHERE license_key = $1",
        req.license_key
    )

    if not license:
        raise HTTPException(status_code=404, detail="License not found")

    # Check status
    if license['status'] != 'active':
        raise HTTPException(status_code=403, detail="License revoked")

    # Check expiration
    if datetime.now() > license['expires_at']:
        raise HTTPException(status_code=403, detail="License expired")

    # Check or create activation
    activation = await db.fetch_one(
        """SELECT * FROM activations
           WHERE license_key = $1 AND hardware_id = $2""",
        req.license_key, req.hardware_id
    )

    if not activation:
        # Check activation limit
        activation_count = await db.fetch_val(
            "SELECT COUNT(*) FROM activations WHERE license_key = $1 AND status = 'active'",
            req.license_key
        )

        if activation_count >= license['max_activations']:
            raise HTTPException(
                status_code=403,
                detail=f"Maximum activations ({license['max_activations']}) reached"
            )

        # Create new activation
        await db.execute(
            """INSERT INTO activations
               (license_key, hardware_id, machine_name, coditect_version, ip_address)
               VALUES ($1, $2, $3, $4, $5)""",
            req.license_key, req.hardware_id, req.machine_name,
            req.coditect_version, request.client.host
        )

    else:
        # Update last validated
        await db.execute(
            """UPDATE activations
               SET last_validated_at = NOW(), validation_count = validation_count + 1
               WHERE license_key = $1 AND hardware_id = $2""",
            req.license_key, req.hardware_id
        )

    # Return validation response
    return LicenseValidationResponse(
        valid=True,
        message="License valid",
        expires_at=license['expires_at'].isoformat(),
        features_enabled=license['features_enabled'] or [],
        user_name=license['user_name'],
        organization=license['organization']
    )

@app.post("/telemetry")
async def log_telemetry(event: dict):
    """Log usage telemetry (opt-in only)"""
    await db.execute(
        """INSERT INTO usage_logs (license_key, event_type, event_data, coditect_version)
           VALUES ($1, $2, $3, $4)""",
        event['license_key'], event['event_type'],
        json.dumps(event.get('event_data', {})), event['coditect_version']
    )
    return {"status": "logged"}
```

---

## 4. Python Source Code Protection

### 4.1 Challenge: Source Code is Readable

**Problem:** Python source code can be read and license checks removed.

**Mitigation Strategies:**

#### Strategy 1: Code Obfuscation (PyArmor)

```bash
# Install PyArmor
pip install pyarmor

# Obfuscate critical files
pyarmor obfuscate scripts/core/license_manager.py
pyarmor obfuscate scripts/coditect-setup.py

# Users get .pyc bytecode files instead of .py source
```

**Pros:**
- Makes tampering difficult
- Protects license validation logic

**Cons:**
- Not foolproof (bytecode can be decompiled)
- Adds complexity to deployment

#### Strategy 2: Server-Side Feature Gating

```python
# Critical features require server-side execution
def invoke_premium_agent(agent_name, task):
    # Call CODITECT Cloud API instead of local execution
    response = requests.post(
        "https://api.coditect.ai/agents/invoke",
        headers={"Authorization": f"Bearer {license_key}"},
        json={"agent": agent_name, "task": task}
    )
    return response.json()
```

**Pros:**
- Cannot be bypassed (runs on server)
- Full control over features

**Cons:**
- Requires internet connection
- Latency for remote execution

#### Strategy 3: License as Runtime Dependency

```python
# Import fails without valid license
# scripts/core/__init__.py
from .license_manager import LicenseManager

_license_manager = LicenseManager()
_valid, _message = _license_manager.validate()

if not _valid:
    raise ImportError(f"CODITECT license validation failed: {_message}")

# Now any import of coditect modules checks license
```

**Pros:**
- Cannot use CODITECT without license
- Simple to implement

**Cons:**
- Can be bypassed with code modification

### 4.2 Recommended Hybrid Approach

**Pilot Phase:**
1. **License validation on startup** (moderate protection)
2. **Offline grace period** (3 days) for user convenience
3. **Usage telemetry** (opt-in) to understand behavior
4. **Legal agreements** (pilot terms and conditions)

**Production Phase:**
5. **Code obfuscation** for core licensing modules
6. **Server-side premium features** (AI agent marketplace)
7. **Subscription-based SaaS** with OAuth

**Enterprise Phase:**
8. **On-premise with floating licenses**
9. **Hardware security modules** for enterprise deployments

---

## 5. Pilot Deployment Workflow

### 5.1 Pilot User Onboarding

```
1. User fills out pilot application:
   https://coditect.ai/pilot-apply

2. AZ1.AI reviews application:
   - Validates use case
   - Checks company/individual credentials
   - Decides on acceptance

3. User accepted → License key generated:
   License Server Admin UI:
   - Enter: Email, Name, Organization
   - Select: User Type (team, individual, consultant, auditor)
   - Select: Features Enabled
   - Set: Expiration Date (e.g., 90 days)
   - Click: Generate License Key

   Generated: CODITECT-PILOT-TEAM-A7F2-E9D1B3C4

4. License key emailed to user:
   "Welcome to CODITECT Pilot!
    Your license key: CODITECT-PILOT-TEAM-A7F2-E9D1B3C4
    Expires: 2025-02-15

    Get started:
    1. Install CODITECT: python3 scripts/installer/install.py
    2. Run setup: python3 scripts/coditect-setup.py
    3. Enter license key when prompted

    Docs: https://docs.coditect.ai
    Support: pilot@coditect.ai"

5. User installs and activates:
   $ python3 scripts/coditect-setup.py

   CODITECT LICENSE ACTIVATION
   ======================================
   No valid license found. Please enter your license key.
   License Key: CODITECT-PILOT-TEAM-A7F2-E9D1B3C4

   ✓ License validated successfully
   ✓ Welcome, John Doe (Acme Corp)
   ✓ License expires: 2025-02-15
   ✓ Features: [core, agents, marketplace]

6. AZ1.AI monitors usage:
   - License Server Dashboard shows:
     - Active licenses: 47
     - Total activations: 52
     - Usage events (last 24h): 1,234
     - Top features: agents (45%), marketplace (30%), core (25%)
```

### 5.2 License Administration UI

**Dashboard:** `https://license.coditect.ai/admin`

**Features:**
- Generate license keys
- View all licenses (filterable by status, tier, user type)
- View activations per license
- Revoke licenses
- Extend expiration dates
- View usage analytics
- Export reports (CSV, PDF)

**Sample License Detail View:**
```
License Key: CODITECT-PILOT-TEAM-A7F2-E9D1B3C4
─────────────────────────────────────────────────
User: John Doe
Email: john@acme.com
Organization: Acme Corp
User Type: Team
Tier: Pilot
Status: ✅ Active

Issued: 2024-11-16
Expires: 2025-02-15 (89 days remaining)
Max Activations: 3

Activations (2/3):
├─ Machine 1: MacBook Pro (john-mbp.local)
│  Hardware ID: a7f2e9d1...
│  Last Validated: 2024-11-16 14:23 (2 hours ago)
│  Validations: 147
│
└─ Machine 2: Linux Workstation (acme-dev-01)
   Hardware ID: b8c3f0e2...
   Last Validated: 2024-11-16 10:15 (6 hours ago)
   Validations: 89

Features Enabled:
✓ core (base framework)
✓ agents (AI agent system)
✓ marketplace (agent marketplace - pilot access)
✗ enterprise-sso (not available in pilot)
✗ audit-logs (not available in pilot)

Usage (Last 7 Days):
├─ Startup events: 42
├─ Agents invoked: 187
├─ Sessions exported: 34
└─ Checkpoints created: 28

Actions:
[Extend License] [Revoke License] [Add Activation] [View Full Logs]
```

---

## 6. Feature Gating Strategy

### 6.1 Pilot vs Production vs Enterprise

| Feature | Pilot | Production | Enterprise |
|---------|-------|------------|------------|
| Core Framework | ✅ | ✅ | ✅ |
| 50 AI Agents | ✅ | ✅ | ✅ |
| Local Development | ✅ | ✅ | ✅ |
| Agent Marketplace | ✅ (read-only) | ✅ (publish) | ✅ (private) |
| Cloud Sync | ❌ | ✅ | ✅ |
| Team Collaboration | ❌ | ✅ | ✅ |
| Enterprise SSO | ❌ | ❌ | ✅ |
| Audit Logs | ❌ | ❌ | ✅ |
| SLA Guarantees | ❌ | ❌ | ✅ (99.9%) |
| Dedicated Support | ❌ | ❌ | ✅ |
| On-Premise Option | ❌ | ❌ | ✅ |

### 6.2 Feature Check Implementation

```python
# scripts/core/feature_gate.py
from .license_manager import LicenseManager

class FeatureGate:
    """Control feature availability based on license"""

    def __init__(self):
        self.license_manager = LicenseManager()

    def require_feature(self, feature: str):
        """Decorator to gate features"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.license_manager.is_feature_enabled(feature):
                    print(f"\n❌ Feature '{feature}' not available in your license tier.")
                    print("Upgrade to unlock this feature: https://coditect.ai/upgrade")
                    return None
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Usage example
feature_gate = FeatureGate()

@feature_gate.require_feature('agent_marketplace_publish')
def publish_agent_to_marketplace(agent_definition):
    """Publish custom agent (production tier only)"""
    # Implementation...

@feature_gate.require_feature('enterprise_sso')
def enable_sso_integration(provider):
    """Enable SSO (enterprise tier only)"""
    # Implementation...
```

---

## 7. Transition Plan to Enterprise SaaS

### 7.1 Phase 1: Pilot (Now - 3 months)

**Licensing:**
- Time-limited keys (90 days)
- Hardware-bound activations
- Basic feature gating
- Manual key generation

**Infrastructure:**
- License Server on Cloud Run
- PostgreSQL on Cloud SQL
- Simple admin UI

**Control:**
- Can revoke licenses remotely
- Track usage patterns
- Collect pilot feedback

### 7.2 Phase 2: Production SaaS (3-6 months)

**Licensing:**
- Subscription-based (monthly/annual)
- OAuth/SSO integration
- Self-service signup
- Automated provisioning

**Infrastructure:**
- Full SaaS platform
- Multi-tenant architecture
- Stripe payment integration
- Customer portal

**Features:**
- Cloud-hosted agents
- Team collaboration
- Agent marketplace with publishing
- Usage-based pricing tiers

### 7.3 Phase 3: Enterprise (6-12 months)

**Licensing:**
- Floating licenses
- On-premise deployment
- Air-gapped installations
- Enterprise contracts

**Infrastructure:**
- Hybrid cloud/on-premise
- Kubernetes helm charts
- License server clustering
- Advanced monitoring

**Features:**
- Enterprise SSO (Okta, Azure AD)
- Audit trails and compliance
- Dedicated support
- SLA guarantees (99.9%)

---

## 8. Security Considerations

### 8.1 License Key Security

**Generation:**
- Cryptographically secure random component
- CRC32 checksum for validation
- Stored hashed in database (SHA-256)

**Transmission:**
- HTTPS only
- No license keys in URLs (POST body only)
- Rate limiting on validation endpoints

**Storage:**
- Encrypted at rest in database
- Encrypted in transit (TLS 1.3)
- Access logs for all license operations

### 8.2 Preventing Abuse

**Key Sharing Prevention:**
- Hardware fingerprinting
- Max activations limit
- Detect activation from multiple IPs
- Revoke on suspicious activity

**Bypass Prevention:**
- Code obfuscation (PyArmor)
- License validation in multiple places
- Server-side feature execution
- Legal agreements (pilot terms)

**Grace Periods:**
- 72-hour offline grace period
- Allows legitimate offline work
- Balances security vs usability

---

## 9. Cost Analysis

### 9.1 Infrastructure Costs (Pilot Phase)

| Component | Service | Cost (Monthly) |
|-----------|---------|----------------|
| License Server | Cloud Run (always-on) | $5-10 |
| Database | Cloud SQL (PostgreSQL - db-f1-micro) | $7-15 |
| Storage | License data (< 1GB) | $0.02 |
| Networking | Egress (minimal) | $1-5 |
| **Total** | | **$13-30/month** |

**50 pilot users:** ~$0.26-0.60 per user/month

### 9.2 Development Effort

| Task | Effort | Priority |
|------|--------|----------|
| License Manager (client) | 2 days | P0 |
| License Server (FastAPI) | 3 days | P0 |
| Database schema + migrations | 1 day | P0 |
| Admin UI (basic) | 3 days | P1 |
| Integration with CODITECT | 2 days | P0 |
| Testing + deployment | 2 days | P0 |
| Documentation | 1 day | P1 |
| **Total** | **~14 days** | |

**Timeline:** 2-3 weeks for complete implementation

---

## 10. Pilot Success Metrics

### 10.1 Licensing KPIs

| Metric | Target | How to Measure |
|--------|--------|----------------|
| License activation rate | 90%+ | licenses activated / licenses issued |
| Daily active licenses | 70%+ | users validating in last 24h |
| License violations | < 5% | revocations / total licenses |
| Average activations per license | 1.5 | total activations / licenses |
| Time to first activation | < 1 hour | activation_time - issue_time |

### 10.2 Usage Analytics

**Track (opt-in telemetry):**
- Agents most frequently invoked
- Features most used
- Session export frequency
- Checkpoint creation patterns
- Error rates by feature

**Insights:**
- Which agents provide most value?
- Which features to prioritize?
- Where do users get stuck?
- What drives conversions (pilot → paid)?

---

## 11. Legal Framework

### 11.1 Pilot License Agreement

**Key Terms:**
1. **Limited License:** Pilot users receive time-limited, non-transferable, non-commercial license
2. **No Warranty:** Pilot software provided "as is"
3. **Feedback Rights:** AZ1.AI can use pilot feedback to improve product
4. **Confidentiality:** Pilot users agree not to disclose sensitive info
5. **Termination:** AZ1.AI can revoke licenses at any time
6. **No Resale:** Cannot sublicense or redistribute

**Sample Clause:**
```
PILOT LICENSE TERMS

This pilot license ("License") grants you a limited, non-exclusive,
non-transferable, revocable right to use CODITECT software solely for
evaluation and testing purposes during the pilot period.

RESTRICTIONS:
- No commercial use
- No redistribution
- No reverse engineering
- No removal of license checks

TERM: This License expires on [EXPIRATION_DATE] or upon revocation
by AZ1.AI INC, whichever occurs first.

DATA COLLECTION: You consent to collection of usage analytics to
improve the product.
```

### 11.2 Transition to Paid Licensing

**Pilot Exit Paths:**
1. **Convert to paid subscription** - Seamless upgrade, keep data
2. **Decline to continue** - Export data, license expires
3. **Enterprise negotiation** - Custom contract, on-premise option

---

## 12. Implementation Checklist

### 12.1 Phase 1: Core Licensing (Week 1-2)

- [ ] Create `scripts/core/license_manager.py` with validation logic
- [ ] Implement hardware fingerprinting
- [ ] Create offline grace period (72 hours)
- [ ] Add license prompt to `coditect-setup.py`
- [ ] Test on Windows, macOS, Linux

### 12.2 Phase 2: License Server (Week 2-3)

- [ ] Deploy FastAPI license server to Cloud Run
- [ ] Create PostgreSQL database on Cloud SQL
- [ ] Implement `/validate` endpoint
- [ ] Implement `/activate` and `/deactivate` endpoints
- [ ] Add rate limiting and security headers
- [ ] Create database migrations

### 12.3 Phase 3: Admin Tools (Week 3-4)

- [ ] Build license generation script
- [ ] Create simple admin web UI (Streamlit or React)
- [ ] Implement license revocation
- [ ] Add usage analytics dashboard
- [ ] Create pilot user onboarding flow

### 12.4 Phase 4: Integration & Testing (Week 4)

- [ ] Integrate license checks into all CODITECT entry points
- [ ] Test activation on fresh machines
- [ ] Test offline grace period
- [ ] Test license revocation
- [ ] Load test license server (1000 validations/minute)
- [ ] Security audit of license validation

### 12.5 Phase 5: Documentation (Week 4)

- [ ] User guide: How to activate license
- [ ] Admin guide: How to generate/revoke licenses
- [ ] Troubleshooting guide
- [ ] Legal: Pilot license agreement
- [ ] FAQ: Common licensing questions

---

## 13. Risk Mitigation

### 13.1 Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| License checks bypassed | Medium | High | Code obfuscation + server-side features |
| Server downtime blocks users | Low | High | 72-hour offline grace period |
| Key sharing between users | Medium | Medium | Hardware fingerprinting + activation limits |
| User frustration with licensing | Low | Medium | Clear messaging + easy activation |
| Pilot licenses leaked publicly | Low | High | Revocation capability + monitoring |
| Legal compliance issues | Low | High | Review by legal counsel |

### 13.2 Contingency Plans

**If license server goes down:**
- 72-hour grace period allows continued operation
- Monitor with Uptime Robot (99.9% SLA)
- Auto-recovery with Cloud Run (stateless)

**If keys leaked publicly:**
- Immediate revocation via admin UI
- Issue new keys to legitimate users
- Implement IP-based rate limiting

**If bypass discovered:**
- Legal action against violators
- Accelerate transition to SaaS model
- Add additional obfuscation layers

---

## 14. Conclusion

### 14.1 Recommendation

**Implement licensing system NOW for pilot phase:**

**Week 1-2:** Core client-side licensing
**Week 3:** License server deployment
**Week 4:** Admin UI and testing
**Total:** 4 weeks to production-ready licensing

**Investment:** ~$15-30/month infrastructure + 2-3 weeks dev time
**ROI:** Complete control over pilot deployment + smooth transition to SaaS

### 14.2 Success Criteria

✅ **Pilot Control:** Only authorized users can run CODITECT
✅ **Usage Tracking:** Understand how pilot users engage
✅ **Feature Gating:** Control which features are available
✅ **Revocation:** Can remotely disable licenses
✅ **Scalability:** System scales to 100+ users easily
✅ **Transition Ready:** Clear path to enterprise SaaS model

---

**Status:** Design Complete - Ready for Implementation
**Priority:** P0 (Critical for Pilot Launch)
**Owner:** AZ1.AI INC
**Last Updated:** November 16, 2025
**Next Steps:** Review with stakeholders → Approve → Implement
