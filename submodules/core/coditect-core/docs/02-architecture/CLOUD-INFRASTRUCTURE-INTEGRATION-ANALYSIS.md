# Cloud Infrastructure Integration Analysis

**Document:** CLOUD-INFRASTRUCTURE-INTEGRATION-ANALYSIS.md
**Version:** 1.0.0
**Purpose:** Integration analysis between CODITECT Core (ADR-002/ADR-003) and Cloud Infrastructure
**Audience:** Architecture Team, Backend Engineers
**Date Created:** 2025-11-23
**Status:** ANALYSIS COMPLETE

---

## Executive Summary

This document analyzes the integration between the **CODITECT Core local client** (defined in ADR-002 and ADR-003) and the **coditect-cloud-infra** server-side infrastructure. It identifies alignment, gaps, and provides integration recommendations.

### Key Findings

✅ **EXCELLENT ALIGNMENT** - The cloud infrastructure is highly aligned with ADR-002 and ADR-003 architectural decisions.

**Technology Stack Match:**
- ✅ FastAPI for License API (matches ADR-003)
- ✅ Firebase Identity Platform (matches ADR-003)
- ✅ PostgreSQL Cloud SQL (matches ADR-003)
- ✅ Redis for caching (matches ADR-002)
- ✅ JWT tokens with 1-hour expiry (matches ADR-003)
- ✅ Google OAuth, GitHub OAuth (matches ADR-003)

**Deployment Model Match:**
- ✅ Hybrid model: Local CLI + Cloud Services (matches ADR-002)
- ✅ License validation with local caching (matches ADR-002)
- ✅ Multi-tier subscription model (matches ADR-002)

**Gaps Identified:**
- ⚠️ Email/password authentication implementation (partially complete)
- ⚠️ Enterprise SSO (SAML 2.0, OIDC) not yet implemented
- ⚠️ Multi-factor authentication (TOTP) not yet implemented
- ⚠️ Session management and revocation (partial implementation)
- ⚠️ Payment processing (Stripe integration planned but not implemented)

---

## Table of Contents

1. [Technology Stack Comparison](#1-technology-stack-comparison)
2. [Architecture Alignment](#2-architecture-alignment)
3. [Authentication System Comparison](#3-authentication-system-comparison)
4. [License Management Comparison](#4-license-management-comparison)
5. [Integration Points](#5-integration-points)
6. [Gap Analysis](#6-gap-analysis)
7. [Implementation Recommendations](#7-implementation-recommendations)
8. [Migration Path](#8-migration-path)

---

## 1. Technology Stack Comparison

### Backend Framework

| Component | ADR-003 Spec | Cloud-Infra Implementation | Status |
|-----------|--------------|---------------------------|--------|
| **API Framework** | FastAPI | FastAPI 0.104+ | ✅ MATCH |
| **Server** | Uvicorn | Uvicorn | ✅ MATCH |
| **Python Version** | 3.10+ | 3.11 | ✅ MATCH |
| **API Design** | REST + WebSockets | REST (WebSocket planned) | ⚠️ PARTIAL |

### Authentication & Authorization

| Component | ADR-003 Spec | Cloud-Infra Implementation | Status |
|-----------|--------------|---------------------------|--------|
| **Primary Auth** | Firebase Auth | Firebase Identity Platform | ✅ MATCH |
| **JWT Tokens** | RS256, 1hr access + 30 day refresh | RS256, 1hr access + 30 day refresh | ✅ MATCH |
| **OAuth Providers** | Google, GitHub, Microsoft | Google, GitHub | ⚠️ PARTIAL |
| **SSO** | SAML 2.0, OIDC | Planned (Ory Hydra) | ⏸️ PLANNED |
| **MFA** | TOTP | Not implemented | ❌ GAP |

### Database & Storage

| Component | ADR-002/ADR-003 Spec | Cloud-Infra Implementation | Status |
|-----------|---------------------|---------------------------|--------|
| **Primary Database** | PostgreSQL (Cloud SQL) | PostgreSQL 16 (Cloud SQL) | ✅ MATCH |
| **Multi-tenancy** | Tenant isolation | Shared-table with tenant_id | ✅ MATCH |
| **Cache** | Redis (Memorystore) | Redis 6GB (Memorystore) | ✅ MATCH |
| **Encryption** | At rest + in transit | Cloud SQL encrypted | ✅ MATCH |
| **Future Scale** | Not specified | Citus (distributed PostgreSQL) | ℹ️ ENHANCEMENT |

### Infrastructure

| Component | ADR-002 Spec | Cloud-Infra Implementation | Status |
|-----------|--------------|---------------------------|--------|
| **Cloud Provider** | GCP | GCP | ✅ MATCH |
| **Orchestration** | GKE (Kubernetes) | GKE 1.28+ | ✅ MATCH |
| **Load Balancer** | GCP Cloud Load Balancer | NGINX Ingress + Cloud LB | ✅ MATCH |
| **API Gateway** | Not specified | Kong (planned) | ℹ️ ENHANCEMENT |
| **SSL/TLS** | Required | Let's Encrypt + managed certs | ✅ MATCH |

### Observability

| Component | ADR-002 Spec | Cloud-Infra Implementation | Status |
|-----------|--------------|---------------------------|--------|
| **Metrics** | Prometheus | Prometheus | ✅ MATCH |
| **Dashboards** | Grafana | Grafana | ✅ MATCH |
| **Tracing** | Not specified | Jaeger | ℹ️ ENHANCEMENT |
| **Logging** | Cloud Logging | GCP Cloud Logging | ✅ MATCH |

---

## 2. Architecture Alignment

### Deployment Model

**ADR-002: Hybrid Deployment Architecture**
```
Local Engine + Cloud Services
- Local-first execution (all AI agents run locally)
- Cloud license validation (daily check, 24-hour cache)
- 7-day offline grace period
```

**Cloud-Infra Implementation:**
```
CODITECT CLI (Local) + License API (Cloud)
- License Client SDK in local CLI
- License validation via HTTPS REST API
- Session heartbeat every 5 minutes
- Redis TTL for session expiry (6 minutes)
```

**Alignment:** ✅ EXCELLENT MATCH

**Key Difference:** Cloud-infra uses 5-minute heartbeat (stricter) vs ADR-002's 24-hour cache (more lenient). Both approaches are valid:
- **Cloud-infra approach:** Better real-time seat management, requires internet
- **ADR-002 approach:** Better offline support, less precise seat tracking

**Recommendation:** Implement BOTH patterns:
- Default: 5-minute heartbeat for active internet users
- Fallback: 24-hour cache with 7-day grace period for offline users

### Subscription Tiers

**ADR-002 Spec:**
- Free Tier: 10 commands/day, basic agents, local only
- Pro Tier ($49/mo): Unlimited commands, all agents, cloud sync
- Team Tier ($99/mo): Collaboration, shared contexts, RBAC
- Enterprise Tier (custom): On-premise, SSO, unlimited users

**Cloud-Infra Implementation:**
```sql
CREATE TABLE tenants (
    plan VARCHAR(50) DEFAULT 'FREE',  -- FREE, PRO, ENTERPRISE
    max_seats INTEGER NOT NULL DEFAULT 1
);
```

**Alignment:** ✅ GOOD MATCH

**Gaps:**
- ⚠️ "Team Tier" not explicitly defined (use PRO with max_seats > 1)
- ⚠️ Quota enforcement (commands/day) not implemented
- ⚠️ Feature flags (agent access, cloud sync) not in database schema

---

## 3. Authentication System Comparison

### User Registration

**ADR-003 Flow:**
1. User visits /signup
2. Choose email/password OR OAuth (Google/GitHub/Microsoft)
3. Email/password: Requires email verification
4. OAuth: Email pre-verified
5. Backend creates user account + generates license key
6. Send welcome email with license key

**Cloud-Infra Flow:**
1. User visits https://auth.coditect.ai/signup
2. Click "Sign Up with Google" or "Sign Up with GitHub"
3. Identity Platform handles OAuth
4. Frontend receives JWT token
5. POST /api/v1/auth/register with JWT + organization name
6. Backend creates tenant + user + license in transaction
7. Send welcome email with license key

**Alignment:** ✅ EXCELLENT MATCH

**Implementation Status:**
- ✅ OAuth registration flow (complete)
- ⚠️ Email/password registration (partial - Identity Platform supports it, but flow not documented)
- ❌ Email verification (not implemented)

### Authentication Methods

| Method | ADR-003 Spec | Cloud-Infra Status | Implementation |
|--------|--------------|-------------------|----------------|
| **Email/Password** | ✅ Required | ⚠️ Partial | Identity Platform enabled, flow not documented |
| **Google OAuth** | ✅ Required | ✅ Complete | Implemented + documented |
| **GitHub OAuth** | ✅ Required | ✅ Complete | Implemented + documented |
| **Microsoft OAuth** | ✅ Required | ❌ Missing | Identity Platform supports, not configured |
| **SAML 2.0 (SSO)** | ✅ Enterprise | ⏸️ Planned | Ory Hydra planned, not implemented |
| **OIDC (SSO)** | ✅ Enterprise | ⏸️ Planned | Ory Hydra planned, not implemented |
| **MFA (TOTP)** | ✅ Required | ❌ Missing | Not implemented |

### JWT Token Structure

**ADR-003 Spec:**
```json
{
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
}
```

**Cloud-Infra Implementation:**
```json
{
  "iss": "https://securetoken.google.com/coditect-citus-prod",
  "aud": "coditect-citus-prod",
  "user_id": "abc123...",
  "email": "user@example.com",
  "email_verified": true,
  "firebase": {
    "identities": {
      "google.com": ["123456789"]
    },
    "sign_in_provider": "google.com"
  }
}
```

**Gap:** Cloud-infra uses Firebase's default token structure. Custom claims (tier, license_key, scopes, org_id) are NOT included.

**Recommendation:** Use Firebase Custom Claims API:
```python
from firebase_admin import auth

auth.set_custom_user_claims(uid, {
    'tenant_id': str(tenant.id),
    'tier': tenant.plan,
    'license_key': license.key_string,
    'role': user.role,
    'scopes': get_user_scopes(user.role, tenant.plan)
})
```

### Session Management

**ADR-003 Spec:**
- 1-hour access tokens
- 30-day refresh tokens
- Session revocation via user action
- Device tracking (browser, location)
- Sliding window expiry

**Cloud-Infra Implementation:**
- 1-hour access tokens ✅
- 30-day refresh tokens ✅
- Session tracking via Redis (session:{session_id}) ✅
- 6-minute TTL with heartbeat refresh ✅
- Session revocation: NOT IMPLEMENTED ❌
- Device tracking: NOT IMPLEMENTED ❌

---

## 4. License Management Comparison

### License Key Format

**ADR-002 Spec:**
```
Format: CODITECT-{TYPE}-{HASH}-{CHECKSUM}
Example: CODITECT-PRO-A7F3E9D2C4B1-8F2A
```

**Cloud-Infra Implementation:**
```
Format: CODITECT-{RANDOM}
Example: CODITECT-AB12CD34EF56
```

**Gap:** Cloud-infra does not include TYPE in license key. Recommendation: Update to include tier.

### License Validation Flow

**ADR-002 Spec:**
```
Local CLI → Cloud API (daily validation)
  ↓
Cache for 24 hours
  ↓
After 7 days offline → Downgrade to free tier
```

**Cloud-Infra Implementation:**
```
Local CLI → POST /api/v1/licenses/acquire (on startup)
  ↓
Heartbeat every 5 minutes → PUT /api/v1/licenses/heartbeat
  ↓
Redis session expires after 6 minutes without heartbeat
  ↓
Lua script decrements seat count automatically
```

**Alignment:** Both valid approaches, but different tradeoffs

**Key Differences:**

| Aspect | ADR-002 | Cloud-Infra | Better For |
|--------|---------|-------------|-----------|
| **Validation Frequency** | Daily | 5-minute heartbeat | Cloud-infra (real-time) |
| **Offline Support** | 7-day grace period | None | ADR-002 (offline users) |
| **Seat Management** | Not specified | Atomic seat counting | Cloud-infra (concurrency) |
| **Network Dependency** | Low (daily check) | High (5-min heartbeat) | ADR-002 (reliability) |

**Recommendation:** Hybrid approach:
1. Daily validation for license status (as ADR-002)
2. Optional heartbeat for real-time seat management (as cloud-infra)
3. 7-day grace period for offline mode (as ADR-002)
4. Configurable per tenant (free tier: no heartbeat, enterprise: strict heartbeat)

### Quota Enforcement

**ADR-002 Spec:**
- Free Tier: 10 commands/day
- Pro Tier: Unlimited
- Team Tier: Unlimited
- Enterprise Tier: Unlimited

**Cloud-Infra Implementation:**
- Seat limits: YES (atomic seat counting via Redis Lua scripts)
- Command quotas: NO (not implemented)
- Feature flags: NO (not implemented)

**Gap:** Command quota enforcement not implemented

**Recommendation:** Add quota tracking:
```sql
ALTER TABLE licenses ADD COLUMN quotas JSONB DEFAULT '{"commands_per_day": null}';

-- Track usage in Redis
-- quota:{license_key}:{date} = command_count (TTL: 24 hours)
```

---

## 5. Integration Points

### Local CLI → Cloud API Integration

**Endpoints Required by Local CLI:**

| Endpoint | ADR-002/ADR-003 | Cloud-Infra | Status |
|----------|-----------------|-------------|--------|
| `POST /api/v1/auth/register` | User registration | ✅ Implemented | READY |
| `POST /api/v1/auth/login` | Email/password login | ⚠️ Partial | Use Firebase SDK directly |
| `POST /api/v1/auth/refresh` | Token refresh | ⚠️ Partial | Use Firebase SDK directly |
| `POST /api/v1/licenses/validate` | License validation | ⚠️ Alternative | Use /licenses/acquire |
| `POST /api/v1/licenses/acquire` | Acquire license seat | ✅ Implemented | READY |
| `PUT /api/v1/licenses/heartbeat` | Session heartbeat | ✅ Implemented | READY |
| `DELETE /api/v1/licenses/release` | Release license seat | ✅ Implemented | READY |

**Integration Flow:**

```python
# Local CLI on startup
class LicenseClient:
    def __init__(self, license_key: str):
        self.license_key = license_key
        self.session_id = None
        self.base_url = "https://auth.coditect.ai"

    async def startup(self):
        """Called when CODITECT CLI starts."""
        # 1. Authenticate user (if not cached)
        if not self.has_valid_token():
            await self.login()

        # 2. Acquire license seat
        response = await self.acquire_license()
        self.session_id = response['session_id']

        # 3. Start heartbeat task
        asyncio.create_task(self.heartbeat_loop())

    async def acquire_license(self):
        """Acquire a license seat."""
        hardware_id = get_hardware_fingerprint()
        token = self.get_cached_token()

        response = await requests.post(
            f"{self.base_url}/api/v1/licenses/acquire",
            json={"hardware_id": hardware_id},
            headers={"Authorization": f"Bearer {token}"}
        )

        return response.json()

    async def heartbeat_loop(self):
        """Send heartbeat every 5 minutes."""
        while True:
            await asyncio.sleep(300)  # 5 minutes

            try:
                await requests.put(
                    f"{self.base_url}/api/v1/licenses/heartbeat",
                    json={"session_id": self.session_id}
                )
            except Exception as e:
                logger.warning(f"Heartbeat failed: {e}")
                # Continue anyway - graceful degradation

    async def shutdown(self):
        """Called when CODITECT CLI exits."""
        if self.session_id:
            await requests.delete(
                f"{self.base_url}/api/v1/licenses/release",
                json={"session_id": self.session_id}
            )
```

### Authentication Integration

**Local CLI Authentication Flow:**

1. **Initial Setup:**
   ```bash
   $ coditect login
   Opening browser to https://auth.coditect.ai/login...
   ✅ Logged in as user@example.com
   ```

2. **Browser OAuth Flow:**
   - CLI starts local server on localhost:8787
   - Opens browser to Admin UI
   - User authenticates via Firebase (Google/GitHub/Email)
   - Admin UI redirects to localhost:8787/callback with token
   - CLI saves token to ~/.coditect/auth.json

3. **Token Storage:**
   ```json
   {
     "access_token": "eyJhbGciOiJSUzI1NiIs...",
     "refresh_token": "AMf-vBxT...",
     "expires_at": 1700003600,
     "user": {
       "email": "user@example.com",
       "tenant_id": "550e8400-...",
       "plan": "PRO"
     }
   }
   ```

4. **Automatic Token Refresh:**
   ```python
   async def ensure_valid_token(self):
       if self.token_expired():
           new_token = await self.refresh_token()
           self.save_token(new_token)
   ```

---

## 6. Gap Analysis

### Critical Gaps (Must Fix)

| Gap | Impact | Priority | Effort |
|-----|--------|----------|--------|
| **MFA (TOTP) not implemented** | Security risk for enterprise customers | P0 | 3 days |
| **Email/password flow not documented** | Blocks users without Google/GitHub | P0 | 1 day |
| **Email verification missing** | Security risk (fake emails) | P0 | 2 days |
| **Session revocation not implemented** | Security risk (can't logout remotely) | P0 | 2 days |
| **Custom JWT claims not set** | CLI can't read tier/license from token | P0 | 1 day |

### Important Gaps (Should Fix)

| Gap | Impact | Priority | Effort |
|-----|--------|----------|--------|
| **Command quota enforcement** | Free tier abuse possible | P1 | 3 days |
| **Feature flags in database** | Can't disable features per tier | P1 | 2 days |
| **Microsoft OAuth missing** | Blocks enterprise Microsoft customers | P1 | 1 day |
| **Device tracking missing** | Can't show "active devices" in UI | P1 | 2 days |
| **Stripe integration incomplete** | Can't charge customers | P1 | 5 days |

### Nice-to-Have Gaps (Future)

| Gap | Impact | Priority | Effort |
|-----|--------|----------|--------|
| **SAML 2.0 SSO** | Blocks large enterprise customers | P2 | 10 days |
| **OAuth 2.0/OIDC SSO** | Blocks mid-size enterprise customers | P2 | 8 days |
| **License key tier prefix** | Harder to identify tier from key | P2 | 1 day |
| **WebSocket streaming** | Better real-time updates | P2 | 5 days |

---

## 7. Implementation Recommendations

### Immediate Actions (This Week)

1. **Add Custom JWT Claims**
   ```python
   # In POST /api/v1/auth/register endpoint
   from firebase_admin import auth

   # After creating user in PostgreSQL
   auth.set_custom_user_claims(firebase_uid, {
       'tenant_id': str(tenant.id),
       'tier': tenant.plan,
       'license_key': license.key_string,
       'role': user.role,
       'max_seats': tenant.max_seats
   })
   ```

2. **Implement Session Revocation**
   ```python
   @router.delete("/api/v1/auth/sessions/{session_id}")
   async def revoke_session(
       session_id: str,
       current_user: User = Depends(get_current_user),
       redis: Redis = Depends(get_redis)
   ):
       # Delete from Redis
       await redis.delete(f"session:{session_id}")

       # Update PostgreSQL audit log
       await log_audit_event(
           tenant_id=current_user.tenant_id,
           user_id=current_user.id,
           action="SESSION_REVOKED",
           metadata={"session_id": session_id}
       )

       return {"status": "revoked"}
   ```

3. **Document Email/Password Registration**
   - Create flow diagram
   - Add API endpoint documentation
   - Implement email verification

### Short-Term (Next 2 Weeks)

1. **Implement MFA (TOTP)**
   - Enrollment endpoint
   - Challenge endpoint
   - Backup codes
   - QR code generation

2. **Add Command Quota Enforcement**
   - Redis-based quota tracking
   - Middleware to check quota on each command
   - Reset daily at midnight UTC

3. **Implement Stripe Integration**
   - Webhook handler for subscription events
   - Update tenant plan on payment
   - Handle failed payments

### Long-Term (Next 2 Months)

1. **Enterprise SSO (SAML 2.0)**
   - Ory Hydra configuration
   - JIT provisioning
   - Group-to-role mapping

2. **Offline Mode Improvements**
   - Implement 7-day grace period
   - Local license cache
   - Graceful degradation

3. **Citus Migration for Hyperscale**
   - Test with 100K+ tenants
   - Shard distribution strategy
   - Migration scripts

---

## 8. Migration Path

### Phase 1: Align with ADRs (Week 1-2)

**Tasks:**
- ✅ Verify FastAPI alignment (already done)
- ✅ Verify Firebase Auth alignment (already done)
- [ ] Add custom JWT claims
- [ ] Implement session revocation
- [ ] Document email/password flow
- [ ] Add email verification

**Deliverable:** Cloud infrastructure 100% aligned with ADR-003

### Phase 2: Fill Critical Gaps (Week 3-4)

**Tasks:**
- [ ] Implement MFA (TOTP)
- [ ] Add command quota enforcement
- [ ] Implement device tracking
- [ ] Add feature flags to database
- [ ] Complete Stripe integration

**Deliverable:** Production-ready authentication and licensing system

### Phase 3: Enterprise Features (Week 5-8)

**Tasks:**
- [ ] SAML 2.0 SSO implementation
- [ ] OAuth 2.0/OIDC SSO
- [ ] Enhanced audit logging
- [ ] Advanced rate limiting
- [ ] Multi-region deployment

**Deliverable:** Enterprise-ready platform

### Phase 4: Hyperscale (Ongoing)

**Tasks:**
- [ ] Migrate to Citus when >50K tenants
- [ ] Implement sharding strategy
- [ ] Multi-region failover
- [ ] Advanced caching layers

**Deliverable:** 1M+ tenant support

---

## Conclusion

**Overall Assessment:** ✅ EXCELLENT FOUNDATION

The **coditect-cloud-infra** repository is **highly aligned** with the architectural decisions made in ADR-002 and ADR-003. The technology stack, deployment model, and core authentication flows match the specifications.

**Key Strengths:**
- FastAPI + Firebase Auth + PostgreSQL (exactly as specified)
- Hybrid deployment model (local + cloud)
- Atomic seat counting with Redis
- Comprehensive infrastructure as code (OpenTofu)
- Production-ready observability (Prometheus, Grafana, Jaeger)

**Critical Next Steps:**
1. Add custom JWT claims (1 day)
2. Implement session revocation (2 days)
3. Implement MFA (TOTP) (3 days)
4. Complete email/password flow (2 days)
5. Add command quota enforcement (3 days)

**Timeline to Production:**
- **Phase 1** (ADR alignment): 2 weeks
- **Phase 2** (Critical gaps): 2 weeks
- **Phase 3** (Enterprise features): 4 weeks
- **Total**: 8 weeks to enterprise-ready platform

---

**Last Updated:** 2025-11-23
**Status:** Integration analysis complete
**Next Step:** Review with architecture team
**Owner:** CODITECT Architecture Team
