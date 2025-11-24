# ADR-002 Addendum: License Validation Strategy

**Document:** ADR-002-ADDENDUM-LICENSE-VALIDATION-STRATEGY
**Version:** 1.0.0
**Purpose:** Reconcile license validation differences between ADR-002 spec and cloud-infra implementation
**Audience:** Backend Engineers, Architecture Team
**Date Created:** 2025-11-23
**Status:** ✅ ACCEPTED
**Parent ADR:** [ADR-002: Hybrid Deployment Architecture](ADR-002-hybrid-deployment-architecture.md)

---

## Context and Problem Statement

**Issue:** ADR-002 specifies "daily license validation with 24-hour cache and 7-day offline grace period," but the existing `coditect-cloud-infra` implementation uses a **5-minute heartbeat with 6-minute session TTL** and no offline support.

**Discovery:** During cloud infrastructure integration analysis (2025-11-23), we found:

| Aspect | ADR-002 Spec | Cloud-Infra Implementation |
|--------|--------------|---------------------------|
| **Validation Frequency** | Daily (24-hour cache) | 5-minute heartbeat |
| **Offline Support** | 7-day grace period | None (requires internet) |
| **Seat Management** | Not specified | Atomic seat counting (Redis Lua) |
| **Network Dependency** | Low (daily check) | High (5-min heartbeat) |

**Why This Matters:**
- **User Experience:** Users expect to work offline for at least a few days
- **Seat Management:** Enterprise customers need accurate, real-time seat usage
- **Revenue Protection:** Must prevent license abuse while supporting offline work
- **Technical Feasibility:** Both approaches are valid but serve different needs

**Question:** Which strategy should we implement, or should we support both?

---

## Decision Drivers

### Mandatory Requirements (Must-Have)
1. **Prevent license abuse** - Users cannot share licenses across unlimited devices
2. **Offline work support** - Users can work offline for reasonable periods (travel, network issues)
3. **Accurate seat counting** - Enterprise knows exactly how many seats are in use
4. **Graceful degradation** - System works even when cloud services are temporarily unavailable
5. **User experience** - No disruptive "license expired" errors during normal usage

### Important Goals (Should-Have)
1. **Real-time seat visibility** - Admin dashboard shows active sessions
2. **Fast license acquisition** - <1 second to acquire license on CLI startup
3. **Low network overhead** - Minimize API calls to reduce costs
4. **Enterprise compliance** - Audit trail of license usage

### Nice-to-Have
1. **Zombie session cleanup** - Automatic cleanup of crashed/killed processes
2. **Configurable grace periods** - Different policies for Free vs Enterprise tiers
3. **License transfer** - Easy to move license between devices

---

## Considered Options

### Option 1: Daily Validation Only (ADR-002 Original)

**How it works:**
```python
class LicenseValidator:
    async def validate(self):
        # Check cache first
        cached = self.load_cache()
        if cached and cached['expires_at'] > now():
            return cached['features']

        # Call cloud API (once per day)
        try:
            response = await self.api.validate_license(self.license_key)
            self.save_cache(response, ttl=24*3600)
            return response['features']
        except NetworkError:
            # Offline mode: 7-day grace period
            if cached and (now() - cached['cached_at']).days < 7:
                return cached['features']
            else:
                return FreeTierLimits()
```

**Pros:**
- ✅ Excellent offline support (7-day grace period)
- ✅ Low network overhead (1 API call per day)
- ✅ Simple implementation
- ✅ Good user experience (works during network issues)

**Cons:**
- ❌ Inaccurate seat counting (users can share license by working offline)
- ❌ No real-time visibility (can't see active sessions)
- ❌ Zombie session problem (crashed CLI doesn't release seat)
- ❌ 7-day grace period is exploitable (users can stay offline indefinitely)

---

### Option 2: Heartbeat Only (Cloud-Infra Current)

**How it works:**
```python
class LicenseValidator:
    async def startup(self):
        # Acquire seat on startup
        response = await self.api.acquire_license(hardware_id)
        self.session_id = response['session_id']

        # Start heartbeat loop
        asyncio.create_task(self.heartbeat_loop())

    async def heartbeat_loop(self):
        while True:
            await asyncio.sleep(300)  # 5 minutes
            try:
                await self.api.heartbeat(self.session_id)
            except NetworkError:
                logger.warning("Heartbeat failed - may lose seat")
```

**Pros:**
- ✅ Accurate seat counting (Redis atomic operations)
- ✅ Real-time visibility (admin sees active sessions)
- ✅ Automatic zombie cleanup (6-minute TTL)
- ✅ Enterprise-friendly (audit trail, precise usage)

**Cons:**
- ❌ NO offline support (requires internet every 5 minutes)
- ❌ Higher network overhead (288 API calls per day)
- ❌ Poor user experience (frequent "network error" warnings)
- ❌ Airplane/travel scenario fails completely

---

### Option 3: Hybrid Strategy (RECOMMENDED) ✅

**How it works:**
```python
class HybridLicenseValidator:
    def __init__(self):
        self.mode = 'online'  # or 'offline'
        self.heartbeat_interval = 300  # 5 minutes
        self.offline_grace_days = 7

    async def startup(self):
        try:
            # Attempt to acquire seat
            response = await self.api.acquire_license(hardware_id)
            self.session_id = response['session_id']
            self.mode = 'online'

            # Start online heartbeat
            asyncio.create_task(self.online_heartbeat_loop())
        except NetworkError:
            # Fallback to offline mode
            self.enter_offline_mode()

    async def online_heartbeat_loop(self):
        """Send heartbeat every 5 minutes while online."""
        failures = 0

        while self.mode == 'online':
            await asyncio.sleep(self.heartbeat_interval)

            try:
                await self.api.heartbeat(self.session_id)
                failures = 0  # Reset failure count
            except NetworkError:
                failures += 1

                # After 3 consecutive failures (~15 min), switch to offline mode
                if failures >= 3:
                    self.enter_offline_mode()

    def enter_offline_mode(self):
        """Switch to offline mode with grace period."""
        self.mode = 'offline'
        self.offline_start = datetime.now()

        logger.info("Entered offline mode - 7-day grace period active")

        # Check grace period on each command
        asyncio.create_task(self.offline_grace_period_monitor())

    async def offline_grace_period_monitor(self):
        """Monitor offline grace period."""
        while self.mode == 'offline':
            await asyncio.sleep(3600)  # Check every hour

            days_offline = (datetime.now() - self.offline_start).days

            if days_offline >= self.offline_grace_days:
                logger.warning(
                    f"Offline grace period expired ({self.offline_grace_days} days). "
                    "Limited to free tier until reconnected."
                )
                self.downgrade_to_free_tier()

            # Try to reconnect
            try:
                await self.attempt_reconnect()
            except NetworkError:
                pass  # Stay offline

    async def attempt_reconnect(self):
        """Attempt to reconnect and resume online mode."""
        response = await self.api.acquire_license(hardware_id)
        self.session_id = response['session_id']
        self.mode = 'online'

        logger.info("Reconnected to cloud - resuming online mode")
        asyncio.create_task(self.online_heartbeat_loop())
```

**Pros:**
- ✅ **Best of both worlds**
- ✅ Real-time seat management when online (enterprise needs)
- ✅ Offline support with grace period (user experience)
- ✅ Automatic mode switching (no user intervention)
- ✅ Configurable per tier (Free: no heartbeat, Enterprise: strict heartbeat)

**Cons:**
- ⚠️ More complex implementation (~300 lines vs ~50 lines)
- ⚠️ Need to handle mode transitions carefully
- ⚠️ Edge cases (network flapping, partial connectivity)

**Complexity Mitigation:**
- Use state machine pattern for mode transitions
- Comprehensive testing of edge cases
- Clear logging and monitoring of mode switches

---

## Decision Outcome

**SELECTED: Option 3 - Hybrid Strategy**

We will implement **both** validation strategies with automatic mode switching:

1. **Online Mode (Default):**
   - 5-minute heartbeat for seat management
   - Atomic seat counting via Redis Lua scripts
   - Real-time admin dashboard visibility
   - Automatic zombie session cleanup

2. **Offline Mode (Fallback):**
   - Triggered after 3 consecutive heartbeat failures (~15 minutes)
   - 7-day grace period using cached license
   - Hourly reconnection attempts
   - Downgrade to free tier after grace period expires

3. **Tier-Specific Policies:**
   - **Free Tier:** No heartbeat (offline-only), 24-hour cache
   - **Pro Tier:** Hybrid mode (5-min heartbeat + 7-day grace)
   - **Team Tier:** Hybrid mode with 3-day grace period (stricter)
   - **Enterprise Tier:** Configurable (strict online-only OR hybrid)

### Rationale

This decision balances competing concerns:

**For Users:**
- ✅ Works offline (travel, network issues, airplane mode)
- ✅ No disruptive "license expired" errors during normal usage
- ✅ Automatic reconnection (no manual intervention)

**For Enterprise Customers:**
- ✅ Accurate seat counting (know exactly how many licenses are in use)
- ✅ Real-time visibility (admin dashboard shows active sessions)
- ✅ Audit trail (who used license when)
- ✅ Configurable policies (can enforce strict online-only mode)

**For Business:**
- ✅ Prevents abuse (7-day grace period limits sharing)
- ✅ Revenue protection (licenses expire after grace period)
- ✅ Competitive advantage (better offline support than competitors)

---

## Consequences

### Positive Consequences

1. **Better User Experience:**
   - Users can work offline for a week without interruption
   - No "license check failed" errors every 5 minutes
   - Automatic reconnection when network returns

2. **Better Enterprise Support:**
   - Real-time seat visibility in admin dashboard
   - Accurate billing (know exactly how many seats are in use)
   - Audit trail for compliance

3. **Competitive Advantage:**
   - Most competitors don't support offline work
   - Hybrid approach is unique (local-first + cloud benefits)

4. **Flexible Policies:**
   - Free tier: No heartbeat overhead
   - Pro tier: Balanced hybrid mode
   - Enterprise tier: Configurable per customer needs

### Negative Consequences

1. **Increased Complexity:**
   - State machine for mode transitions
   - Edge case handling (network flapping)
   - More testing required

2. **Network Overhead:**
   - 288 heartbeat calls per day (vs 1 daily validation)
   - Mitigation: Free tier doesn't use heartbeat

3. **Grace Period Abuse:**
   - Users could exploit 7-day grace period by going offline repeatedly
   - Mitigation: Track offline periods, warn after 3+ cycles

### Risk Mitigation

**Risk 1: State Machine Bugs**
- Mitigation: Comprehensive state transition tests
- Fallback: If state machine fails, default to offline mode (safe)

**Risk 2: Network Flapping**
- Scenario: Network drops for 1 minute, comes back, drops again
- Mitigation: Exponential backoff for reconnection attempts
- Don't switch to offline mode on first failure (wait for 3 consecutive failures)

**Risk 3: Grace Period Abuse**
```python
# Detect abuse pattern
async def check_offline_abuse(self):
    """Detect users exploiting offline mode."""
    history = await db.get_offline_history(license_key, days=30)

    offline_cycles = len([h for h in history if h['went_offline']])
    total_offline_days = sum(h['days_offline'] for h in history)

    if offline_cycles > 5 and total_offline_days > 20:
        # User has been offline 20+ days in last 30 days
        logger.warning(f"Possible offline abuse: {license_key}")
        await notify_admin(license_key, "offline_abuse_pattern")
```

**Risk 4: Complexity**
- Mitigation: Extract mode logic into separate class
- Clear documentation and decision flowcharts
- Monitoring and alerting for mode switches

---

## Implementation Details

### Phase 1: Cloud-Infra Changes (Backend)

**File:** `coditect-cloud-infra/api/licenses.py`

1. **Add offline mode support to `/acquire` endpoint:**
```python
@router.post("/api/v1/licenses/acquire")
async def acquire_license(
    req: LicenseAcquireRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    # Check user's tier
    tenant = await db.get(Tenant, user.tenant_id)

    if tenant.plan == 'FREE':
        # Free tier: No seat management, return offline-only license
        return {
            'mode': 'offline',
            'license': sign_license_offline(tenant, expires_in=24*3600),
            'grace_period_days': 0  # No grace period for free tier
        }

    # Pro/Team/Enterprise: Try to acquire seat
    try:
        session_id = await acquire_seat_atomic(redis, tenant.id, user.id, req.hardware_id)

        return {
            'mode': 'online',
            'session_id': session_id,
            'heartbeat_interval': 300,  # 5 minutes
            'grace_period_days': get_grace_period(tenant.plan),  # 7 days for Pro
            'license': sign_license_online(tenant, session_id)
        }
    except NoSeatsAvailable:
        raise HTTPException(403, "All seats in use")
```

2. **Add reconnection endpoint:**
```python
@router.post("/api/v1/licenses/reconnect")
async def reconnect_license(
    req: ReconnectRequest,
    user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis)
):
    """Reconnect after offline period."""
    # Release old session if exists
    if req.old_session_id:
        await release_seat(redis, req.old_session_id)

    # Acquire new session
    session_id = await acquire_seat_atomic(redis, user.tenant_id, user.id, req.hardware_id)

    return {
        'session_id': session_id,
        'mode': 'online',
        'message': 'Reconnected successfully'
    }
```

### Phase 2: Local CLI Changes (Client)

**File:** `api/license_client.py` (new)

```python
from enum import Enum
from datetime import datetime, timedelta

class LicenseMode(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"  # Free tier limits

class HybridLicenseValidator:
    def __init__(self, license_key: str, config: dict):
        self.license_key = license_key
        self.mode = LicenseMode.ONLINE
        self.session_id = None
        self.heartbeat_interval = config.get('heartbeat_interval', 300)
        self.grace_period_days = config.get('grace_period_days', 7)
        self.offline_start = None
        self.heartbeat_task = None

    async def startup(self):
        """Initialize license on CLI startup."""
        try:
            # Try online mode first
            await self.acquire_online()
        except NetworkError as e:
            logger.warning(f"Network error on startup: {e}")
            await self.enter_offline_mode()
        except Exception as e:
            logger.error(f"License acquisition failed: {e}")
            raise

    async def acquire_online(self):
        """Acquire license in online mode."""
        response = await self.api.acquire_license(
            hardware_id=get_hardware_fingerprint()
        )

        if response['mode'] == 'offline':
            # Free tier or server-requested offline mode
            await self.enter_offline_mode()
            return

        self.session_id = response['session_id']
        self.heartbeat_interval = response['heartbeat_interval']
        self.grace_period_days = response['grace_period_days']
        self.mode = LicenseMode.ONLINE

        # Save license to cache
        self.save_license_cache(response['license'])

        # Start heartbeat
        self.heartbeat_task = asyncio.create_task(self.heartbeat_loop())

        logger.info(f"✅ License acquired (online mode, seat: {self.session_id})")

    async def heartbeat_loop(self):
        """Send heartbeat every N minutes."""
        consecutive_failures = 0

        while self.mode == LicenseMode.ONLINE:
            await asyncio.sleep(self.heartbeat_interval)

            try:
                await self.api.heartbeat(self.session_id)
                consecutive_failures = 0
                logger.debug("Heartbeat sent successfully")
            except NetworkError as e:
                consecutive_failures += 1
                logger.warning(
                    f"Heartbeat failed (attempt {consecutive_failures}/3): {e}"
                )

                # After 3 failures (~15 minutes), switch to offline mode
                if consecutive_failures >= 3:
                    logger.warning("Multiple heartbeat failures - entering offline mode")
                    await self.enter_offline_mode()

    async def enter_offline_mode(self):
        """Switch to offline mode with grace period."""
        self.mode = LicenseMode.OFFLINE
        self.offline_start = datetime.now()

        # Stop heartbeat task
        if self.heartbeat_task:
            self.heartbeat_task.cancel()

        # Load cached license
        cached_license = self.load_license_cache()
        if not cached_license:
            logger.error("No cached license - degrading to free tier")
            self.mode = LicenseMode.DEGRADED
            return

        days_remaining = self.grace_period_days
        logger.info(
            f"📴 Offline mode active - grace period: {days_remaining} days remaining"
        )

        # Start grace period monitor
        asyncio.create_task(self.offline_monitor())

    async def offline_monitor(self):
        """Monitor offline grace period and attempt reconnection."""
        while self.mode == LicenseMode.OFFLINE:
            await asyncio.sleep(3600)  # Check hourly

            # Check grace period
            days_offline = (datetime.now() - self.offline_start).days
            days_remaining = self.grace_period_days - days_offline

            if days_remaining <= 0:
                logger.error(
                    "⚠️  Offline grace period expired - limited to free tier features"
                )
                self.mode = LicenseMode.DEGRADED
                return

            if days_remaining <= 2:
                logger.warning(
                    f"⚠️  Offline grace period expires in {days_remaining} days - "
                    "please reconnect to internet"
                )

            # Try to reconnect
            try:
                await self.attempt_reconnect()
            except NetworkError:
                logger.debug("Reconnection attempt failed - staying offline")

    async def attempt_reconnect(self):
        """Attempt to reconnect and resume online mode."""
        logger.info("Attempting to reconnect...")

        response = await self.api.reconnect_license(
            old_session_id=self.session_id,
            hardware_id=get_hardware_fingerprint()
        )

        self.session_id = response['session_id']
        self.mode = LicenseMode.ONLINE
        self.offline_start = None

        logger.info("✅ Reconnected to cloud - resuming online mode")

        # Restart heartbeat
        self.heartbeat_task = asyncio.create_task(self.heartbeat_loop())

    async def shutdown(self):
        """Release license on CLI shutdown."""
        if self.heartbeat_task:
            self.heartbeat_task.cancel()

        if self.session_id and self.mode == LicenseMode.ONLINE:
            try:
                await self.api.release_license(self.session_id)
                logger.info("License released")
            except Exception as e:
                logger.warning(f"Failed to release license: {e}")
```

### Phase 3: Testing Strategy

**Test Scenarios:**

1. **Happy Path - Online Mode:**
   ```python
   async def test_online_mode_happy_path():
       validator = HybridLicenseValidator(license_key, config)
       await validator.startup()

       assert validator.mode == LicenseMode.ONLINE
       assert validator.session_id is not None

       # Simulate 10 successful heartbeats
       for _ in range(10):
           await asyncio.sleep(validator.heartbeat_interval)

       assert validator.mode == LicenseMode.ONLINE  # Still online
   ```

2. **Network Failure - Offline Transition:**
   ```python
   async def test_offline_transition():
       validator = HybridLicenseValidator(license_key, config)
       await validator.startup()

       # Simulate network failure
       mock_api.heartbeat.side_effect = NetworkError("Connection failed")

       # Wait for 3 heartbeat failures (~15 minutes)
       await asyncio.sleep(validator.heartbeat_interval * 3 + 10)

       assert validator.mode == LicenseMode.OFFLINE
       assert validator.offline_start is not None
   ```

3. **Offline Grace Period Expiry:**
   ```python
   async def test_grace_period_expiry():
       validator = HybridLicenseValidator(license_key, config)
       validator.mode = LicenseMode.OFFLINE
       validator.offline_start = datetime.now() - timedelta(days=8)

       await validator.offline_monitor()

       assert validator.mode == LicenseMode.DEGRADED
   ```

4. **Successful Reconnection:**
   ```python
   async def test_successful_reconnection():
       validator = HybridLicenseValidator(license_key, config)
       validator.mode = LicenseMode.OFFLINE
       validator.offline_start = datetime.now() - timedelta(days=2)

       # Network comes back
       mock_api.reconnect_license.return_value = {'session_id': 'new123'}

       await validator.attempt_reconnect()

       assert validator.mode == LicenseMode.ONLINE
       assert validator.offline_start is None
   ```

---

## Validation and Compliance

### How to Verify This Decision is Followed

**Backend Checklist:**
- [ ] `/api/v1/licenses/acquire` returns `mode` field ('online' or 'offline')
- [ ] Free tier always returns `mode: 'offline'`
- [ ] Pro/Team/Enterprise tiers return `grace_period_days` in response
- [ ] `/api/v1/licenses/reconnect` endpoint exists
- [ ] Redis tracks offline sessions separately from online sessions

**Frontend (CLI) Checklist:**
- [ ] `HybridLicenseValidator` class implements state machine
- [ ] Automatic mode switching after 3 heartbeat failures
- [ ] Grace period monitor runs in background
- [ ] Hourly reconnection attempts in offline mode
- [ ] Clear user notifications for mode switches
- [ ] Cached license is saved and loaded correctly

**Testing Checklist:**
- [ ] Unit tests for all mode transitions
- [ ] Integration tests for heartbeat loop
- [ ] Network failure simulation tests
- [ ] Grace period expiry tests
- [ ] Reconnection success/failure tests

**Monitoring Checklist:**
- [ ] Grafana dashboard shows online vs offline session counts
- [ ] Alert when >20% of sessions are in offline mode
- [ ] Track average offline duration per user
- [ ] Alert on suspected offline abuse patterns

---

## Links

**Related Documents:**
- [ADR-002: Hybrid Deployment Architecture](ADR-002-hybrid-deployment-architecture.md) - Parent ADR
- [CLOUD-INFRASTRUCTURE-INTEGRATION-ANALYSIS.md](CLOUD-INFRASTRUCTURE-INTEGRATION-ANALYSIS.md) - Integration analysis that identified this gap
- [coditect-cloud-infra: C2-CONTAINER-DIAGRAM.md](../../../../../submodules/cloud/coditect-cloud-infra/docs/architecture/C2-CONTAINER-DIAGRAM.md) - Current cloud architecture

**Implementation Files:**
- Backend: `coditect-cloud-infra/api/licenses.py`
- Client: `coditect-core/api/license_client.py`
- Tests: `coditect-core/tests/test_license_validation.py`

---

**Last Updated:** 2025-11-23
**Status:** ✅ ACCEPTED
**Implementation Timeline:** Week 3-4 of Phase 1
**Owner:** Backend Team + CLI Team
