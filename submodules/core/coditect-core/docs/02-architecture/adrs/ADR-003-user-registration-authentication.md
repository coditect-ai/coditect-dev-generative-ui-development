# ADR-003: User Registration and Authentication

**Status:** Accepted
**Date:** 2025-11-23
**Decision Makers:** Hal Casteel (Founder/CEO/CTO)
**Stakeholders:** Engineering, Security, Product
**Supersedes:** None
**Related:** ADR-002 (Hybrid Deployment Architecture)

---

## Context

CODITECT requires a robust user identity and authentication system to support:

1. **Cloud-based registration** - Users sign up via web portal or CLI
2. **Local engine authentication** - Secure access to cloud services
3. **Multi-tier access** - Free, Pro, Team, Enterprise with different auth flows
4. **Enterprise SSO** - SAML, OAuth, Azure AD, Okta integration
5. **API security** - JWT tokens for REST API access
6. **Account management** - Password reset, email verification, MFA

**Key Requirements:**
- Industry-standard security (OWASP Top 10 compliance)
- Scalable authentication (100K+ users)
- Fast validation (<100ms for token verification)
- Multi-device support
- Offline mode support (cached authentication)
- Enterprise SSO integration
- GDPR/SOC2 compliance

---

## Decision

**CODITECT will use a MULTI-LAYERED AUTHENTICATION SYSTEM** with Firebase Auth as the primary identity provider, supplemented by custom JWT tokens and enterprise SSO.

### Authentication Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION LAYERS                     │
└─────────────────────────────────────────────────────────────┘

Layer 1: Primary Authentication (Firebase Auth)
├─ Email/Password
├─ Social OAuth (Google, GitHub, Microsoft)
├─ Magic Links (passwordless)
└─ Phone/SMS (optional MFA)

Layer 2: License Validation (Custom)
├─ License key verification
├─ Subscription tier check
├─ Quota enforcement
└─ Feature flags

Layer 3: API Access (JWT Tokens)
├─ Short-lived access tokens (1 hour)
├─ Refresh tokens (30 days)
├─ Scope-based permissions
└─ Rate limiting by user/tier

Layer 4: Enterprise SSO (Custom Integration)
├─ SAML 2.0 (Okta, OneLogin)
├─ OAuth 2.0 / OIDC (Azure AD, Google Workspace)
├─ LDAP/Active Directory (on-premise)
└─ Just-In-Time (JIT) provisioning
```

---

## User Registration Flows

### 1. Standard Registration (Free/Pro/Team Tiers)

**Web Portal Flow:**
```
User Journey:
1. User visits https://coditect.ai/signup
2. Enters email + password (or social OAuth)
3. Email verification sent
4. User clicks verification link
5. Account activated → Free tier
6. Optional: Subscribe to Pro/Team
7. License key generated and displayed
8. User copies license key

Technical Flow:
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "Jane Developer"
}

Response:
{
  "user_id": "usr_7f3e9d2c4b1",
  "email": "user@example.com",
  "email_verified": false,
  "tier": "FREE",
  "verification_email_sent": true
}

Email Verification:
GET /api/v1/auth/verify-email?token=eyJhbGci...

Post-Verification:
{
  "user_id": "usr_7f3e9d2c4b1",
  "email_verified": true,
  "license_key": "CODITECT-FREE-A7F3E9D2C4B1-8F2A",
  "tier": "FREE"
}
```

**CLI Registration Flow:**
```bash
$ coditect register

📧 Email: user@example.com
🔒 Password: ********
👤 Name: Jane Developer

✅ Registration successful!
📬 Verification email sent to user@example.com

⏳ Waiting for email verification... (Click link in email)

✅ Email verified!
🎉 Welcome to CODITECT!

Your license key: CODITECT-FREE-A7F3E9D2C4B1-8F2A
(Saved to ~/.coditect/license.key)

🚀 Run 'coditect init' to start your first project!
```

---

### 2. Social OAuth Registration (Faster Onboarding)

**Supported Providers:**
- Google (recommended for developers)
- GitHub (developer-friendly)
- Microsoft (enterprise users)

**OAuth Flow:**
```
1. User clicks "Sign up with Google"
   ├─ Redirect to https://accounts.google.com/oauth
   └─ Scopes: email, profile

2. User authorizes
   └─ Redirect back to https://coditect.ai/auth/callback?code=...

3. Backend exchanges code for tokens
   POST https://oauth2.googleapis.com/token
   └─ Receives: access_token, id_token (JWT with email)

4. Create CODITECT user
   ├─ Extract email from id_token
   ├─ Auto-verify email (trusted OAuth provider)
   ├─ Generate license key
   └─ Create user record

5. User logged in
   └─ No email verification needed (OAuth provider verified)
```

**Benefits:**
- ✅ Faster registration (no password needed)
- ✅ Auto-verified email
- ✅ Familiar user experience
- ✅ No password to manage

---

### 3. Enterprise SSO Registration (Team/Enterprise Tiers)

**SAML 2.0 Flow:**
```
1. Admin configures SSO in CODITECT Admin Portal
   ├─ Company: Acme Corp
   ├─ Identity Provider: Okta
   ├─ SAML Metadata URL: https://acme.okta.com/metadata
   ├─ Domain: @acme.com
   └─ JIT Provisioning: Enabled

2. Employee visits https://coditect.ai/login
   ├─ Enters email: alice@acme.com
   └─ CODITECT detects @acme.com → SSO required

3. Redirect to Okta
   GET https://acme.okta.com/saml/login?SAMLRequest=...

4. Employee authenticates with Okta
   └─ Okta redirects back with SAML assertion

5. CODITECT validates SAML assertion
   ├─ Verify signature (Okta's public key)
   ├─ Extract user attributes (email, name, groups)
   └─ JIT provision user if not exists:
      ├─ Create user record
      ├─ Assign to organization (Acme Corp)
      ├─ Assign role based on SAML groups
      └─ Generate license key (enterprise)

6. User logged in
   └─ Access granted based on organization license
```

**SAML Attributes Mapping:**
```xml
<saml:Attribute Name="email">
  <saml:AttributeValue>alice@acme.com</saml:AttributeValue>
</saml:Attribute>
<saml:Attribute Name="firstName">
  <saml:AttributeValue>Alice</saml:AttributeValue>
</saml:Attribute>
<saml:Attribute Name="lastName">
  <saml:AttributeValue>Smith</saml:AttributeValue>
</saml:Attribute>
<saml:Attribute Name="groups">
  <saml:AttributeValue>Engineering</saml:AttributeValue>
  <saml:AttributeValue>Admins</saml:AttributeValue>
</saml:Attribute>
```

**Role Mapping:**
```yaml
saml_role_mapping:
  Admins: organization_admin
  Engineering: developer
  Managers: team_lead
  default: member
```

---

## Authentication Flows

### 1. Email/Password Authentication

**Login Flow:**
```
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Backend Process:
1. Look up user by email
2. Verify password (bcrypt hash comparison)
3. Check email verification status
4. Check account status (active, suspended, deleted)
5. Generate JWT access token (1 hour expiry)
6. Generate refresh token (30 days expiry)
7. Log login event (IP, device, timestamp)

Response:
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "rt_a7f3e9d2c4b1f8e2...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "user_id": "usr_7f3e9d2c4b1",
    "email": "user@example.com",
    "name": "Jane Developer",
    "tier": "PRO",
    "license_key": "CODITECT-PRO-A7F3E9D2C4B1-8F2A"
  }
}
```

**JWT Token Structure (Access Token):**
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "coditect_key_1"
  },
  "payload": {
    "iss": "https://auth.coditect.ai",
    "sub": "usr_7f3e9d2c4b1",
    "aud": "https://api.coditect.ai",
    "exp": 1700000000,
    "iat": 1699996400,
    "email": "user@example.com",
    "tier": "PRO",
    "license_key": "CODITECT-PRO-A7F3E9D2C4B1-8F2A",
    "scopes": ["commands:execute", "sync:read", "sync:write"],
    "org_id": null
  },
  "signature": "..."
}
```

**CLI Login Flow:**
```bash
$ coditect login

Choose login method:
  1. Email/Password
  2. Google
  3. GitHub
  4. SSO (Enterprise)

Selection: 1

📧 Email: user@example.com
🔒 Password: ********

✅ Login successful!
👤 Logged in as: Jane Developer (PRO tier)
🔑 License: CODITECT-PRO-A7F3E9D2C4B1-8F2A

Tokens saved to ~/.coditect/auth.json
```

---

### 2. Token Refresh Flow

**When Access Token Expires:**
```
POST /api/v1/auth/refresh
{
  "refresh_token": "rt_a7f3e9d2c4b1f8e2..."
}

Backend Process:
1. Validate refresh token
   ├─ Check signature
   ├─ Check expiration (30 days)
   └─ Check revocation list

2. Look up user and verify account status

3. Generate new access token (1 hour)

4. Optionally rotate refresh token
   └─ Generate new refresh token
   └─ Invalidate old refresh token

Response:
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "rt_b8g4f0e3d5c2g9f3...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Automatic Refresh (Local Engine):**
```python
class AuthManager:
    def get_valid_token(self):
        """
        Get valid access token, refreshing if expired.
        """
        token = self.load_access_token()

        if self.is_token_expired(token):
            # Refresh token
            refresh_token = self.load_refresh_token()
            new_tokens = self.refresh_tokens(refresh_token)
            self.save_tokens(new_tokens)
            return new_tokens['access_token']

        return token
```

---

### 3. Local Engine Authentication

**First-Time Setup:**
```bash
$ coditect login

🌐 Opening browser for authentication...
(Opens: https://coditect.ai/cli-login?device=macos&version=1.0.0)

Browser Flow:
1. User logs in (email/password or OAuth)
2. User authorizes CLI access
3. Browser shows: "✅ Authentication successful! Return to CLI."
4. Browser sends auth code to CLI via localhost redirect
   http://localhost:8787/callback?code=auth_abc123

CLI receives code:
POST /api/v1/auth/device-token
{
  "auth_code": "auth_abc123",
  "device_id": "mac_a7f3e9d2c4b1",
  "device_name": "Jane's MacBook Pro"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "rt_...",
  "license_key": "CODITECT-PRO-A7F3E9D2C4B1-8F2A"
}

Saved to ~/.coditect/auth.json:
{
  "user_id": "usr_7f3e9d2c4b1",
  "email": "user@example.com",
  "access_token": "eyJ...",
  "refresh_token": "rt_...",
  "license_key": "CODITECT-PRO-A7F3E9D2C4B1-8F2A",
  "cached_at": "2025-11-23T10:00:00Z"
}
```

**Subsequent Startups:**
```python
# On every CLI startup
def startup():
    auth = load_auth_from_disk()  # ~/.coditect/auth.json

    if auth is None:
        print("❌ Not logged in. Run 'coditect login'")
        exit(1)

    # Validate cached auth (24 hour cache)
    if is_recent(auth['cached_at'], hours=24):
        # Use cached validation
        return enable_features(auth['tier'])

    # Re-validate with cloud (once per day)
    try:
        validation = validate_license(auth['license_key'])
        update_cache(validation)
        return enable_features(validation['tier'])
    except NetworkError:
        # Offline mode: Use cached auth (7 day grace period)
        if is_recent(auth['cached_at'], days=7):
            print("⚠️  Offline mode: Using cached license")
            return enable_features(auth['tier'])
        else:
            print("❌ License validation required (grace period expired)")
            exit(1)
```

---

## Password Security

### Password Requirements

**Minimum Standards:**
- Length: 12+ characters
- Complexity: 1 uppercase, 1 lowercase, 1 digit, 1 special char
- Not in common password lists (10M most common)
- Not same as email prefix
- Not reused from previous 5 passwords

**Password Hashing:**
```python
# bcrypt with 12 rounds
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

**Password Reset Flow:**
```
1. User requests password reset
   POST /api/v1/auth/request-password-reset
   { "email": "user@example.com" }

2. Backend generates reset token
   ├─ Create secure random token (32 bytes)
   ├─ Hash token (SHA-256)
   ├─ Store hash in database with 1-hour expiry
   └─ Send email with reset link

3. Email sent:
   Subject: Reset your CODITECT password
   Link: https://coditect.ai/reset-password?token=abc123

4. User clicks link, enters new password
   POST /api/v1/auth/reset-password
   {
     "token": "abc123",
     "new_password": "NewSecurePass456!"
   }

5. Backend validates token and updates password
   ├─ Hash submitted token → lookup in database
   ├─ Check expiry (< 1 hour old)
   ├─ Validate new password meets requirements
   ├─ Hash new password (bcrypt)
   ├─ Update user password
   ├─ Invalidate reset token
   └─ Invalidate all existing sessions (force re-login)

6. Confirmation email sent
   "Your CODITECT password was changed"
```

---

## Multi-Factor Authentication (MFA)

### TOTP (Time-Based One-Time Password)

**Enrollment Flow:**
```
1. User enables MFA in account settings
   POST /api/v1/auth/mfa/enroll

2. Backend generates TOTP secret
   import pyotp
   secret = pyotp.random_base32()

3. Response includes QR code
   {
     "secret": "JBSWY3DPEHPK3PXP",
     "qr_code": "data:image/png;base64,iVBORw0KGgo...",
     "backup_codes": [
       "a7f3-e9d2-c4b1",
       "8f2a-3d5c-7e1b",
       ...
     ]
   }

4. User scans QR code with authenticator app
   (Google Authenticator, Authy, 1Password)

5. User enters verification code
   POST /api/v1/auth/mfa/verify
   {
     "code": "123456"
   }

6. Backend validates code
   totp = pyotp.TOTP(secret)
   is_valid = totp.verify(code, valid_window=1)

7. MFA enabled
   ├─ Store encrypted secret in database
   ├─ Store backup codes (hashed)
   └─ User receives confirmation
```

**Login with MFA:**
```
1. User enters email/password
   POST /api/v1/auth/login
   { "email": "...", "password": "..." }

2. Backend detects MFA enabled
   {
     "mfa_required": true,
     "mfa_token": "temp_mfa_7f3e9d2c4b1"
   }

3. User enters TOTP code or backup code
   POST /api/v1/auth/mfa/challenge
   {
     "mfa_token": "temp_mfa_7f3e9d2c4b1",
     "code": "123456"
   }

4. Backend validates code
   └─ If valid: Issue access/refresh tokens
   └─ If invalid: Reject (rate limit after 5 failures)

5. User logged in
```

---

## Session Management

### Session Storage

**Database Schema:**
```sql
CREATE TABLE user_sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    refresh_token_hash VARCHAR(256) NOT NULL,
    device_id VARCHAR(256),
    device_name VARCHAR(256),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP,
    revoked_reason VARCHAR(256),
    INDEX idx_user_sessions (user_id, revoked),
    INDEX idx_expires_at (expires_at)
);
```

### Session Lifecycle

**Creation:**
- On login: Create session with 30-day expiry
- Store refresh token (hashed)
- Track device info (for "Active Sessions" list)

**Usage:**
- On token refresh: Update last_used_at
- Extend expiry (sliding window)

**Revocation:**
- On logout: Mark session as revoked
- On password change: Revoke all sessions
- On security event: Revoke compromised sessions
- Admin action: Revoke user's sessions

**Cleanup:**
- Cron job: Delete expired sessions (>30 days old)
- Retention: Keep revoked sessions for 90 days (audit trail)

---

## API Authentication

### REST API Endpoints

**Protected Endpoint Example:**
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Dependency to validate JWT and extract user.
    """
    token = credentials.credentials

    # Validate JWT
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience="https://api.coditect.ai"
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    # Extract user info
    user_id = payload['sub']
    tier = payload['tier']
    scopes = payload['scopes']

    return {
        'user_id': user_id,
        'tier': tier,
        'scopes': scopes
    }

@app.post("/api/v1/commands/execute")
async def execute_command(
    request: CommandRequest,
    user: dict = Depends(get_current_user)
):
    """
    Execute command (requires authentication).
    """
    # Check scope
    if "commands:execute" not in user['scopes']:
        raise HTTPException(403, "Insufficient permissions")

    # Check quota (based on tier)
    quota = get_quota(user['tier'])
    if not check_quota(user['user_id'], quota):
        raise HTTPException(429, "Quota exceeded")

    # Execute command
    result = await execute_slash_command(request.command, request.args)
    return result
```

**Authorization Header:**
```http
POST /api/v1/commands/execute HTTP/1.1
Host: api.coditect.ai
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "command": "/analyze",
  "args": {"target": "src/main.rs"}
}
```

---

## Security Best Practices

### OWASP Top 10 Compliance

**A01: Broken Access Control**
- ✅ JWT validation on every API request
- ✅ Scope-based permissions
- ✅ Multi-tenant isolation (organization_id checks)

**A02: Cryptographic Failures**
- ✅ HTTPS only (TLS 1.3)
- ✅ bcrypt password hashing (12 rounds)
- ✅ JWT signed with RS256 (RSA keys)
- ✅ Secrets encrypted at rest (GCP KMS)

**A03: Injection**
- ✅ Parameterized SQL queries
- ✅ Input validation (Pydantic)
- ✅ Output encoding

**A04: Insecure Design**
- ✅ Rate limiting (per user, per IP)
- ✅ Account lockout (5 failed logins)
- ✅ Session fixation protection
- ✅ CSRF tokens for web forms

**A05: Security Misconfiguration**
- ✅ Secure defaults
- ✅ Minimal error details in production
- ✅ Security headers (HSTS, CSP, X-Frame-Options)

**A06: Vulnerable Components**
- ✅ Dependency scanning (Dependabot)
- ✅ Regular updates
- ✅ SCA (Software Composition Analysis)

**A07: Authentication Failures**
- ✅ Strong password policy
- ✅ MFA support
- ✅ Rate limiting on auth endpoints
- ✅ No default credentials

**A08: Data Integrity Failures**
- ✅ JWT signature validation
- ✅ HTTPS (TLS)
- ✅ Subresource Integrity (SRI)

**A09: Logging Failures**
- ✅ Audit logging (auth events)
- ✅ Failed login attempts logged
- ✅ Sensitive data redacted from logs

**A10: SSRF**
- ✅ URL validation
- ✅ Allowlist for external requests
- ✅ No user-controlled URLs

---

## Implementation Checklist

### Phase 1: Core Authentication (Week 1)
- [ ] Firebase Auth setup
- [ ] User registration API
- [ ] Email verification flow
- [ ] Login API (email/password)
- [ ] JWT generation and validation
- [ ] Refresh token flow
- [ ] Password reset flow

### Phase 2: OAuth & Social Login (Week 2)
- [ ] Google OAuth integration
- [ ] GitHub OAuth integration
- [ ] Microsoft OAuth integration
- [ ] Social account linking

### Phase 3: Local Engine Integration (Week 3)
- [ ] CLI login flow (browser-based)
- [ ] Token storage (~/.coditect/auth.json)
- [ ] Automatic token refresh
- [ ] Offline mode with grace period

### Phase 4: Enterprise SSO (Week 4)
- [ ] SAML 2.0 integration
- [ ] OAuth 2.0/OIDC integration
- [ ] JIT provisioning
- [ ] Role mapping
- [ ] Admin portal for SSO configuration

### Phase 5: Security Hardening (Week 5)
- [ ] MFA (TOTP) enrollment
- [ ] MFA login flow
- [ ] Session management
- [ ] Rate limiting
- [ ] Account lockout
- [ ] Security audit logging

---

## Success Metrics

### Security Metrics
- Password breach rate: <0.01% (strong password requirements)
- Account takeover rate: <0.001% (MFA, rate limiting)
- Invalid login attempts blocked: >99%
- Token validation latency: <10ms (p95)

### User Experience Metrics
- Registration completion rate: >80%
- Email verification rate: >90% (within 24 hours)
- Social OAuth adoption: >60% (faster registration)
- MFA adoption (Pro+ users): >30%

### Technical Metrics
- Auth API availability: 99.9%
- Auth API latency: <100ms (p95)
- Token refresh success rate: >99.9%
- Offline mode reliability: 100% (7-day grace period)

---

## References

**Standards:**
- OAuth 2.0: RFC 6749
- JWT: RFC 7519
- SAML 2.0: OASIS Standard
- TOTP: RFC 6238

**Libraries:**
- Firebase Auth (identity provider)
- PyJWT (JWT handling)
- bcrypt (password hashing)
- python-saml (SAML integration)
- pyotp (TOTP generation)

**Related ADRs:**
- ADR-002: Hybrid Deployment Architecture
- ADR-004: Licensing and Entitlement System
- ADR-005: Multi-Tenancy Strategy

---

**Author:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC
**Approved By:** Hal Casteel
**Date:** 2025-11-23
