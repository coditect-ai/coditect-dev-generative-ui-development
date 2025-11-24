# Server-Side Alignment Checklist

**Document:** SERVER-ALIGNMENT-CHECKLIST.md
**Version:** 1.0.0
**Purpose:** Ensure coditect-cloud-infra aligns with ADR-002 and ADR-003
**Date Created:** 2025-11-23
**Status:** ACTION REQUIRED

---

## Executive Summary

**Question:** Do we need to make any further refinements to ensure server-side alignment?

**Answer:** ✅ **YES - 1 Critical Refinement + 5 Important Updates Required**

### Overall Alignment: 90% ✅

The cloud infrastructure is **highly aligned** with the architecture specifications, but we need to make **ONE CRITICAL refinement** and **FIVE important updates** to achieve 100% alignment.

---

## CRITICAL REFINEMENT (Must Do)

### 1. Reconcile License Validation Strategy ⚠️ BLOCKING

**Problem:** ADR-002 specifies "daily validation with 7-day offline grace period," but cloud-infra implements "5-minute heartbeat with NO offline support."

**Impact:**
- ❌ Users cannot work offline (blocks travel, airplane mode, network issues)
- ❌ Architecture documents don't match implementation
- ❌ Poor user experience vs competitors

**Solution:** Implement **Hybrid Strategy** (both online heartbeat + offline grace period)

**Created:** [ADR-002-ADDENDUM-LICENSE-VALIDATION-STRATEGY.md](ADR-002-ADDENDUM-LICENSE-VALIDATION-STRATEGY.md)

**Implementation Required:**
```python
# Backend: coditect-cloud-infra/api/licenses.py
@router.post("/api/v1/licenses/acquire")
async def acquire_license(...):
    if tenant.plan == 'FREE':
        return {'mode': 'offline', 'grace_period_days': 0}
    else:
        return {
            'mode': 'online',
            'session_id': session_id,
            'heartbeat_interval': 300,
            'grace_period_days': 7  # NEW: Support offline mode
        }

# NEW: Reconnection endpoint
@router.post("/api/v1/licenses/reconnect")
async def reconnect_license(...):
    # Handle offline-to-online transition
    pass
```

```python
# Client: coditect-core/api/license_client.py
class HybridLicenseValidator:
    async def heartbeat_loop(self):
        # After 3 heartbeat failures, switch to offline mode
        if consecutive_failures >= 3:
            await self.enter_offline_mode()

    async def offline_monitor(self):
        # Monitor 7-day grace period
        # Attempt reconnection every hour
        pass
```

**Effort:** 3-4 days
**Priority:** P0 (CRITICAL)
**Owner:** Backend Team + CLI Team

---

## IMPORTANT UPDATES (Should Do)

### 2. Add Custom JWT Claims 🔑 P0

**Problem:** Firebase JWT tokens don't include tier, license_key, scopes (ADR-003 requirement).

**Impact:**
- ❌ Local CLI cannot read user tier from token
- ❌ Must make extra API call to get license info
- ❌ Cannot check permissions locally

**Solution:**
```python
# Backend: coditect-cloud-infra/api/auth/register.py
from firebase_admin import auth

# After creating user in PostgreSQL
auth.set_custom_user_claims(firebase_uid, {
    'tenant_id': str(tenant.id),
    'tier': tenant.plan,  # NEW
    'license_key': license.key_string,  # NEW
    'role': user.role,  # NEW
    'scopes': ['commands:execute', 'sync:read', 'sync:write']  # NEW
})
```

**Effort:** 1 day
**Priority:** P0
**Owner:** Backend Team

---

### 3. Implement Session Revocation 🔐 P0

**Problem:** No way to revoke sessions/tokens remotely (ADR-003 specifies this feature).

**Impact:**
- ❌ Stolen tokens remain valid until expiry
- ❌ Cannot implement "Log out all devices" feature
- ❌ Security risk

**Solution:**
```python
# Backend: coditect-cloud-infra/api/auth/sessions.py (NEW FILE)
@router.delete("/api/v1/auth/sessions/{session_id}")
async def revoke_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis)
):
    await redis.delete(f"session:{session_id}")
    # Log audit event
    return {"status": "revoked"}

@router.get("/api/v1/auth/sessions")
async def list_sessions(current_user: User = Depends(get_current_user)):
    # Return list of active sessions for user
    pass
```

**Effort:** 2 days
**Priority:** P0
**Owner:** Backend Team

---

### 4. Add Email Verification 📧 P0

**Problem:** Users can register with fake emails (no verification flow).

**Impact:**
- ❌ Spam registrations possible
- ❌ Security bypass (fake accounts)
- ❌ Cannot send important emails (password reset, etc.)

**Solution:**
```python
# Backend: coditect-cloud-infra/api/auth/register.py
@router.post("/api/v1/auth/register")
async def register_user(...):
    # Create user with email_verified=False
    user = User(email=email, email_verified=False)

    # Send verification email
    token = generate_verification_token(user.id)
    await send_email(
        to=email,
        subject="Verify your CODITECT account",
        template="email_verification",
        link=f"https://auth.coditect.ai/verify?token={token}"
    )

    return {"message": "Check your email to verify account"}

@router.get("/api/v1/auth/verify")
async def verify_email(token: str):
    user_id = decode_verification_token(token)
    await db.execute(
        update(User).where(User.id == user_id).values(email_verified=True)
    )
    return {"message": "Email verified successfully"}
```

**Effort:** 2 days
**Priority:** P0
**Owner:** Backend Team

---

### 5. Implement MFA (TOTP) 🔐 P1

**Problem:** Multi-factor authentication not implemented (ADR-003 specifies TOTP).

**Impact:**
- ❌ Cannot sell to security-conscious enterprises
- ❌ Security requirement for enterprise tier
- ❌ Compliance risk (SOC 2, ISO 27001)

**Solution:**
```python
# Backend: coditect-cloud-infra/api/auth/mfa.py (NEW FILE)
import pyotp

@router.post("/api/v1/auth/mfa/enroll")
async def enroll_mfa(current_user: User = Depends(get_current_user)):
    secret = pyotp.random_base32()

    # Generate QR code
    totp = pyotp.TOTP(secret)
    qr_uri = totp.provisioning_uri(
        name=current_user.email,
        issuer_name="CODITECT"
    )

    # Generate backup codes
    backup_codes = [secrets.token_urlsafe(8) for _ in range(10)]

    return {
        'secret': secret,
        'qr_code_url': generate_qr_code(qr_uri),
        'backup_codes': backup_codes
    }

@router.post("/api/v1/auth/mfa/verify")
async def verify_mfa(code: str, current_user: User = Depends(get_current_user)):
    totp = pyotp.TOTP(current_user.mfa_secret)

    if totp.verify(code):
        # Enable MFA for user
        current_user.mfa_enabled = True
        await db.commit()
        return {"status": "MFA enabled"}
    else:
        raise HTTPException(400, "Invalid code")

@router.post("/api/v1/auth/mfa/challenge")
async def mfa_challenge(code: str, session: dict):
    # Validate TOTP code during login
    pass
```

**Effort:** 3 days
**Priority:** P1 (blocks enterprise sales)
**Owner:** Backend Team

---

### 6. Add Command Quota Enforcement 📊 P1

**Problem:** Free tier has unlimited commands (ADR-002 specifies 10 commands/day limit).

**Impact:**
- ❌ Free tier abuse possible
- ❌ Revenue loss (users stay on free tier)
- ❌ Infrastructure costs (unlimited usage)

**Solution:**
```python
# Backend: coditect-cloud-infra/api/middleware/quota.py (NEW FILE)
from datetime import datetime

async def check_quota(user: User, db: AsyncSession, redis: Redis):
    if user.tier == 'PRO' or user.tier == 'ENTERPRISE':
        return True  # Unlimited

    # Free tier: 10 commands/day
    today = datetime.now().date()
    key = f"quota:{user.id}:{today}"

    current_count = await redis.incr(key)

    if current_count == 1:
        # Set expiry at midnight
        await redis.expireat(key, datetime.combine(today + timedelta(days=1), time.min))

    if current_count > 10:
        raise HTTPException(
            status_code=429,
            detail="Daily quota exceeded (10 commands/day). Upgrade to Pro for unlimited commands."
        )

# Usage in API endpoint:
@app.post("/api/v1/commands/execute")
async def execute_command(
    request: CommandRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    await check_quota(user, db, redis)  # NEW
    # Execute command...
```

**Effort:** 2 days
**Priority:** P1
**Owner:** Backend Team

---

## SUMMARY CHECKLIST

### Week 1 (Critical Path)

- [ ] **Implement Hybrid License Validation** (3-4 days, P0)
  - [ ] Backend: Add `mode` and `grace_period_days` to `/acquire` response
  - [ ] Backend: Create `/reconnect` endpoint
  - [ ] Client: Implement `HybridLicenseValidator` class
  - [ ] Client: Add offline monitor and reconnection logic
  - [ ] Tests: Mode transition tests, grace period tests

- [ ] **Add Custom JWT Claims** (1 day, P0)
  - [ ] Backend: Call `auth.set_custom_user_claims()` in registration
  - [ ] Backend: Include tier, license_key, scopes in JWT
  - [ ] Client: Read claims from JWT token
  - [ ] Tests: Verify custom claims are set

### Week 2 (Security & Core Features)

- [ ] **Implement Session Revocation** (2 days, P0)
  - [ ] Backend: Create `/auth/sessions` endpoints (list, revoke)
  - [ ] Frontend: Add "Active Sessions" page to admin UI
  - [ ] Tests: Revocation tests

- [ ] **Add Email Verification** (2 days, P0)
  - [ ] Backend: Generate verification tokens
  - [ ] Backend: Send verification emails
  - [ ] Backend: Create `/verify` endpoint
  - [ ] Frontend: Verification page in admin UI
  - [ ] Tests: Email verification flow tests

### Week 3 (Enterprise & Revenue)

- [ ] **Implement MFA (TOTP)** (3 days, P1)
  - [ ] Backend: Create `/mfa/enroll`, `/mfa/verify`, `/mfa/challenge` endpoints
  - [ ] Backend: Store encrypted MFA secrets
  - [ ] Frontend: MFA enrollment page with QR code
  - [ ] Frontend: MFA challenge during login
  - [ ] Tests: MFA enrollment and challenge tests

- [ ] **Add Command Quota Enforcement** (2 days, P1)
  - [ ] Backend: Create quota middleware
  - [ ] Backend: Track commands in Redis
  - [ ] Frontend: Show quota usage in admin UI
  - [ ] Tests: Quota enforcement tests

---

## SUCCESS CRITERIA

**Before Production Launch:**

✅ All P0 items completed
- [x] ADRs and diagrams created
- [ ] Hybrid license validation implemented
- [ ] Custom JWT claims added
- [ ] Session revocation implemented
- [ ] Email verification added

✅ All P1 items completed
- [ ] MFA implemented
- [ ] Command quota enforcement added

✅ Integration tests passing
- [ ] End-to-end authentication flow
- [ ] License acquisition and validation
- [ ] Offline mode and reconnection
- [ ] Quota enforcement

✅ Documentation updated
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Integration guide for local CLI
- [ ] Admin UI user guide

---

## TIMELINE

**Total Time to 100% Alignment:** 2-3 weeks

| Week | Focus | Deliverables |
|------|-------|--------------|
| **Week 1** | Critical Path | Hybrid validation, custom JWT claims |
| **Week 2** | Security | Session revocation, email verification |
| **Week 3** | Enterprise | MFA, quota enforcement |

---

## RECOMMENDATION

**YES, refinements are needed**, but they are **well-defined and scoped**:

1. ✅ **Technology stack is perfect** (no changes needed)
2. ✅ **Architecture is sound** (ADR-002, ADR-003 are excellent)
3. ⚠️ **Implementation gaps** (6 items, total 2-3 weeks)

**Next Steps:**
1. Review this checklist with the team
2. Assign owners for each task
3. Begin Week 1 critical path items
4. Track progress in TASKLIST.md

**Confidence:** 95% that these refinements will achieve 100% alignment

---

**Last Updated:** 2025-11-23
**Status:** Awaiting team review
**Owner:** Architecture Team
