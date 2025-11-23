# CODITECT License Manager - Usage Guide

Complete guide for implementing and using the CODITECT License Manager for SaaS license control.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [License Tiers](#license-tiers)
- [Core Functionality](#core-functionality)
- [CLI Usage](#cli-usage)
- [Programmatic API](#programmatic-api)
- [Integration Examples](#integration-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Production Deployment](#production-deployment)

---

## Overview

The CODITECT License Manager provides production-grade SaaS license control with:

- **JWT-based license keys** - Secure, self-contained tokens
- **4 license tiers** - FREE, STARTER, PRO, ENTERPRISE
- **Quota enforcement** - Automatic limit checking for projects, AI operations, users
- **Usage tracking** - Daily metrics and analytics
- **Grace period** - 7-day grace period after expiration
- **Offline validation** - Cached validation for 24 hours
- **Database-backed** - SQLite (development) or PostgreSQL (production)

---

## Installation

### Prerequisites

```bash
# Required Python packages
pip install PyJWT>=2.8.0
pip install cryptography>=41.0.0

# Optional for testing
pip install pytest>=7.4.0
```

### Setup

```bash
# Initialize database
cd scripts/core
python license_manager.py --help

# The database will be auto-created at:
# MEMORY-CONTEXT/licenses.db
```

---

## Quick Start

### Generate a License

```bash
# Generate PRO tier license
python license_manager.py generate \
  --tier pro \
  --email user@company.com \
  --org "Acme Corp" \
  --duration 365
```

**Output:**
```
================================================================================
LICENSE GENERATED SUCCESSFULLY
================================================================================

Tier: PRO
Email: user@company.com
Organization: Acme Corp
Duration: 365 days

License Key:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsaWNlbnNlX2lkIjoiYWJjZDEyMzQtNTY3OC...

⚠️  Store this key securely - it cannot be recovered!
================================================================================
```

### Validate a License

```bash
python license_manager.py validate "your_license_key_here"
```

**Output:**
```
✅ License is VALID and ACTIVE
```

### Check License Information

```bash
python license_manager.py info "your_license_key_here"
```

**Output:**
```
================================================================================
LICENSE INFORMATION
================================================================================

Tier: Pro ($99/month)
Email: user@company.com
Organization: Acme Corp
Status: ACTIVE

📅 Created: 2025-11-22
📅 Expires: 2026-11-22
⏰ Days remaining: 365

📊 USAGE & QUOTAS
--------------------------------------------------------------------------------
Projects: 15/100 (85 remaining)
AI Operations (today): 234/5000 (4766 remaining)
Active Users: 7/10 (3 remaining)
================================================================================
```

---

## License Tiers

### FREE Tier ($0/month)

```python
- Max Projects: 5
- AI Operations/Day: 10
- Max Users: 1
- Support: Community
```

**Ideal for:**
- Individual developers
- Proof of concept projects
- Learning CODITECT framework

---

### STARTER Tier ($29/month)

```python
- Max Projects: 25
- AI Operations/Day: 500
- Max Users: 3
- Support: Email
```

**Ideal for:**
- Small teams (2-3 developers)
- Startups and side projects
- Light production workloads

---

### PRO Tier ($99/month)

```python
- Max Projects: 100
- AI Operations/Day: 5,000
- Max Users: 10
- Support: Priority
```

**Ideal for:**
- Growing teams (5-10 developers)
- Multiple production applications
- High AI operation workloads

---

### ENTERPRISE Tier (Custom Pricing)

```python
- Max Projects: Unlimited
- AI Operations/Day: Unlimited
- Max Users: Unlimited
- Support: Dedicated
- SLA Guarantees
- Custom deployment options
```

**Ideal for:**
- Large organizations (10+ developers)
- Mission-critical applications
- Custom compliance requirements
- On-premise deployment needs

---

## Core Functionality

### 1. License Generation

Create new licenses programmatically:

```python
from license_manager import LicenseManager, LicenseTier

lm = LicenseManager()

license_key = lm.generate_license(
    tier=LicenseTier.PRO,
    user_email="team@company.com",
    organization="Acme Corp",
    duration_days=365  # 1 year
)

print(f"Generated license: {license_key}")
```

---

### 2. License Validation

Validate license before allowing operations:

```python
try:
    is_valid = lm.validate_license(license_key)
    print("✅ License is valid")
except LicenseExpiredError:
    print("❌ License has expired")
except LicenseValidationError as e:
    print(f"❌ Validation failed: {e}")
```

---

### 3. Quota Checking

Check if operation is within quota limits:

```python
from license_manager import QuotaExceededError

try:
    # Check before AI operation
    lm.check_quota(license_key, operation_type="ai_operation")

    # Perform operation
    result = perform_ai_operation()

    # Record usage
    lm.record_usage(license_key, operation_type="ai_operation")

except QuotaExceededError as e:
    print(f"❌ Quota exceeded: {e}")
    # Prompt user to upgrade tier
```

---

### 4. Usage Recording

Track usage for analytics and quota enforcement:

```python
# Record single AI operation
lm.record_usage(license_key, operation_type="ai_operation", count=1)

# Update project count
lm.record_usage(license_key, operation_type="project", count=25)

# Update active user count
lm.record_usage(license_key, operation_type="user", count=7)
```

---

### 5. License Information

Get comprehensive license details:

```python
info = lm.get_license_info(license_key)

print(f"Tier: {info['tier_config']['name']}")
print(f"Status: {info['license_info']['status']}")
print(f"Projects: {info['current_usage']['projects_count']}/{info['license_info']['max_projects']}")
print(f"AI Ops Today: {info['current_usage']['ai_operations_today']}")
print(f"Remaining: {info['remaining_quota']['ai_operations_today']} operations")

if info['in_grace_period']:
    print("⚠️  License in grace period - please renew!")
```

---

### 6. License Renewal

Extend license expiration:

```python
# Renew for another year
new_license_key = lm.renew_license(license_key, duration_days=365)

print(f"License renewed: {new_license_key}")
```

---

### 7. License Suspension/Activation

Temporarily disable or re-enable licenses:

```python
# Suspend (e.g., for payment failure)
lm.suspend_license(license_key)

# Activate (after payment received)
lm.activate_license(license_key)

# Revoke permanently (fraud, violation)
lm.revoke_license(license_key)
```

---

## CLI Usage

### Complete CLI Reference

```bash
# Generate license
python license_manager.py generate --tier {free|starter|pro|enterprise} \
  --email EMAIL --org ORGANIZATION [--duration DAYS]

# Validate license
python license_manager.py validate LICENSE_KEY

# Get license info
python license_manager.py info LICENSE_KEY

# Check quota
python license_manager.py check-quota LICENSE_KEY \
  [--type {ai_operation|project|user}]
```

### Exit Codes

```
0   - Success
1   - General error
2   - License generation failed
3   - License invalid/not found
4   - License expired
5   - Quota exceeded
130 - User cancelled (Ctrl+C)
```

---

## Programmatic API

### Initialize License Manager

```python
from license_manager import LicenseManager
from pathlib import Path

# Auto-detect database location
lm = LicenseManager()

# Custom database path
lm = LicenseManager(
    db_path=Path("/custom/path/licenses.db"),
    secret_key="your_secret_key_here",
    encryption_key=b"your_32_byte_encryption_key_here"
)
```

---

### Example: Web Application Integration

```python
from flask import Flask, request, jsonify
from license_manager import (
    LicenseManager,
    LicenseValidationError,
    QuotaExceededError
)

app = Flask(__name__)
lm = LicenseManager()

@app.before_request
def check_license():
    """Validate license on every request."""
    license_key = request.headers.get('X-License-Key')

    if not license_key:
        return jsonify({"error": "License key required"}), 401

    try:
        lm.validate_license(license_key)
    except LicenseValidationError as e:
        return jsonify({"error": str(e)}), 403

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """AI analysis endpoint with quota enforcement."""
    license_key = request.headers.get('X-License-Key')

    try:
        # Check quota before operation
        lm.check_quota(license_key, operation_type="ai_operation")

        # Perform AI analysis
        result = perform_analysis(request.json)

        # Record usage
        lm.record_usage(license_key, operation_type="ai_operation")

        return jsonify({"result": result}), 200

    except QuotaExceededError as e:
        return jsonify({
            "error": str(e),
            "upgrade_url": "https://example.com/upgrade"
        }), 429
```

---

### Example: CLI Tool Integration

```python
#!/usr/bin/env python3
"""CODITECT CLI with license enforcement."""

import click
from license_manager import LicenseManager, QuotaExceededError

lm = LicenseManager()

@click.command()
@click.option('--license', required=True, help='License key')
@click.option('--project', required=True, help='Project name')
def analyze_project(license, project):
    """Analyze project with license enforcement."""

    try:
        # Validate license
        lm.validate_license(license)

        # Check quota
        lm.check_quota(license, operation_type="ai_operation")

        # Perform analysis
        click.echo(f"Analyzing project: {project}")
        result = run_analysis(project)

        # Record usage
        lm.record_usage(license, operation_type="ai_operation")

        click.echo(f"✅ Analysis complete: {result}")

    except QuotaExceededError as e:
        click.echo(f"❌ {e}", err=True)
        click.echo("💡 Upgrade your license for more operations", err=True)
        raise click.Abort()

if __name__ == '__main__':
    analyze_project()
```

---

## Error Handling

### Exception Hierarchy

```python
LicenseError                    # Base exception
├── LicenseValidationError      # Invalid token/signature
├── LicenseExpiredError         # Expired (beyond grace period)
├── QuotaExceededError          # Usage quota exceeded
├── LicenseNotFoundError        # License not in database
├── DatabaseError               # Database operation failed
├── ConfigurationError          # Invalid configuration
└── EncryptionError             # Encryption/decryption failed
```

### Comprehensive Error Handling

```python
from license_manager import (
    LicenseManager,
    LicenseValidationError,
    LicenseExpiredError,
    QuotaExceededError,
    LicenseNotFoundError
)

lm = LicenseManager()

def perform_licensed_operation(license_key: str):
    """Perform operation with comprehensive error handling."""

    try:
        # Validate license
        lm.validate_license(license_key)

        # Check quota
        lm.check_quota(license_key, operation_type="ai_operation")

        # Perform operation
        result = expensive_ai_operation()

        # Record usage
        lm.record_usage(license_key, operation_type="ai_operation")

        return {"success": True, "result": result}

    except LicenseExpiredError as e:
        return {
            "success": False,
            "error": "license_expired",
            "message": str(e),
            "action": "renew_license"
        }

    except QuotaExceededError as e:
        return {
            "success": False,
            "error": "quota_exceeded",
            "message": str(e),
            "action": "upgrade_tier"
        }

    except LicenseValidationError as e:
        return {
            "success": False,
            "error": "invalid_license",
            "message": str(e),
            "action": "contact_support"
        }

    except LicenseNotFoundError as e:
        return {
            "success": False,
            "error": "license_not_found",
            "message": str(e),
            "action": "purchase_license"
        }
```

---

## Best Practices

### 1. Secure Key Storage

```python
# ✅ GOOD: Store in environment variables
import os
license_key = os.environ.get('CODITECT_LICENSE_KEY')

# ❌ BAD: Hardcode in source code
license_key = "eyJhbGc..."  # NEVER DO THIS
```

---

### 2. Cached Validation

```python
import time
from datetime import datetime, timedelta

class LicenseCache:
    """Cache license validation for 24 hours."""

    def __init__(self, lm: LicenseManager):
        self.lm = lm
        self.cache = {}

    def validate_cached(self, license_key: str) -> bool:
        """Validate with 24-hour cache."""
        cache_entry = self.cache.get(license_key)

        if cache_entry:
            validated_at, is_valid = cache_entry
            age = datetime.now() - validated_at

            if age < timedelta(hours=24):
                return is_valid

        # Cache miss or expired - validate
        is_valid = self.lm.validate_license(license_key)
        self.cache[license_key] = (datetime.now(), is_valid)

        return is_valid
```

---

### 3. Quota Pre-checks

```python
def batch_ai_operations(license_key: str, tasks: list):
    """Perform batch operations with upfront quota check."""

    # Get current quota remaining
    info = lm.get_license_info(license_key)
    remaining = info['remaining_quota']['ai_operations_today']

    if len(tasks) > remaining:
        raise QuotaExceededError(
            f"Batch requires {len(tasks)} operations, "
            f"but only {remaining} remaining today"
        )

    # Proceed with batch
    results = []
    for task in tasks:
        result = perform_task(task)
        lm.record_usage(license_key, "ai_operation")
        results.append(result)

    return results
```

---

### 4. Graceful Degradation

```python
def perform_operation(license_key: str):
    """Degrade gracefully if license issues."""

    try:
        lm.validate_license(license_key)
        lm.check_quota(license_key, "ai_operation")

        # Full AI-powered operation
        return ai_powered_operation()

    except QuotaExceededError:
        # Fallback to basic operation
        logger.warning("Quota exceeded, using basic mode")
        return basic_operation()

    except LicenseValidationError:
        # Read-only mode
        logger.error("Invalid license, read-only mode")
        return readonly_operation()
```

---

## Production Deployment

### 1. PostgreSQL Migration

```python
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update LicenseManager for PostgreSQL
import psycopg2
from psycopg2 import pool

class ProductionLicenseManager(LicenseManager):
    """PostgreSQL-backed license manager."""

    def __init__(self, connection_pool):
        self.pool = connection_pool
        # Override SQLite connection methods
```

### PostgreSQL Schema

```sql
-- See license_schema.sql for complete schema
-- Key differences from SQLite:

CREATE TABLE licenses (
    license_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_key TEXT UNIQUE NOT NULL,
    tier VARCHAR(20) NOT NULL CHECK(tier IN ('free', 'starter', 'pro', 'enterprise')),
    ...
);

-- Add partitioning for large datasets
CREATE TABLE license_usage (
    ...
) PARTITION BY RANGE (date);

CREATE TABLE license_usage_2025 PARTITION OF license_usage
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

---

### 2. Environment Configuration

```bash
# .env file
CODITECT_DB_TYPE=postgresql
CODITECT_DB_HOST=localhost
CODITECT_DB_PORT=5432
CODITECT_DB_NAME=coditect_licenses
CODITECT_DB_USER=coditect_user
CODITECT_DB_PASSWORD=secure_password_here
CODITECT_JWT_SECRET=your_secret_key_here
CODITECT_ENCRYPTION_KEY=your_32_byte_key_here
```

---

### 3. Monitoring & Alerts

```python
# Example: Prometheus metrics integration
from prometheus_client import Counter, Gauge

license_validations = Counter(
    'coditect_license_validations_total',
    'Total license validations',
    ['status']
)

quota_usage = Gauge(
    'coditect_quota_usage',
    'Current quota usage',
    ['tier', 'operation_type']
)

def validate_with_metrics(license_key: str):
    """Validate with Prometheus metrics."""
    try:
        result = lm.validate_license(license_key)
        license_validations.labels(status='success').inc()
        return result
    except LicenseValidationError:
        license_validations.labels(status='failed').inc()
        raise
```

---

### 4. Automated Cleanup

```python
#!/usr/bin/env python3
"""Daily maintenance script."""

from license_manager import LicenseManager
from datetime import datetime, timedelta

lm = LicenseManager()

def daily_maintenance():
    """Run daily maintenance tasks."""

    # Mark expired licenses (beyond grace period)
    # DELETE FROM licenses WHERE status = 'active' AND expires_at < NOW() - INTERVAL '7 days'

    # Clean up old usage records (keep 90 days)
    # DELETE FROM license_usage WHERE date < NOW() - INTERVAL '90 days'

    # Send renewal reminders (30 days before expiration)
    # SELECT * FROM licenses WHERE expires_at BETWEEN NOW() AND NOW() + INTERVAL '30 days'
```

---

## Support

For issues, questions, or feature requests:

- **Documentation:** `/docs/LICENSE-MANAGER-USAGE.md`
- **Source Code:** `/scripts/core/license_manager.py`
- **Tests:** `/tests/core/test_license_manager.py`
- **Schema:** `/scripts/core/license_schema.sql`

---

**Version:** 1.0.0
**Last Updated:** 2025-11-22
**Author:** AZ1.AI CODITECT Team
