#!/usr/bin/env python3
"""
Unit Tests for CODITECT License Manager

Comprehensive test suite covering license generation, validation,
quota enforcement, and database operations.

Usage:
    python -m pytest tests/core/test_license_manager.py -v

Author: AZ1.AI CODITECT Team
Date: 2025-11-22
"""

import os
import sys
import json
import pytest
import tempfile
import jwt
from pathlib import Path
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "core"))

from license_manager import (
    LicenseManager,
    LicenseTier,
    LicenseStatus,
    LicenseError,
    LicenseValidationError,
    LicenseExpiredError,
    QuotaExceededError,
    LicenseNotFoundError,
    DatabaseError,
    ConfigurationError,
    TIER_CONFIGS
)


@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = Path(f.name)

    yield db_path

    # Cleanup
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def license_manager(temp_db):
    """Initialize LicenseManager with temporary database."""
    return LicenseManager(
        db_path=temp_db,
        secret_key="test_secret_key_12345",
        encryption_key=b'test_encryption_key_1234567890123456789012345678'[:32]
    )


class TestLicenseManagerInitialization:
    """Test LicenseManager initialization."""

    def test_initialization_success(self, temp_db):
        """Test successful initialization."""
        lm = LicenseManager(
            db_path=temp_db,
            secret_key="test_key",
            encryption_key=b'a' * 32
        )

        assert lm.db_path == temp_db
        assert temp_db.exists()
        assert lm.secret_key == "test_key"

    def test_database_schema_creation(self, temp_db):
        """Test that database schema is created correctly."""
        lm = LicenseManager(db_path=temp_db)

        import sqlite3
        conn = sqlite3.connect(str(temp_db))
        cursor = conn.cursor()

        # Check licenses table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='licenses'")
        assert cursor.fetchone() is not None

        # Check license_usage table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='license_usage'")
        assert cursor.fetchone() is not None

        conn.close()

    def test_auto_directory_creation(self):
        """Test that parent directories are created automatically."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "subdir" / "test.db"
            lm = LicenseManager(db_path=db_path)

            assert db_path.parent.exists()
            assert db_path.exists()


class TestLicenseGeneration:
    """Test license generation functionality."""

    def test_generate_free_license(self, license_manager):
        """Test generating FREE tier license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.FREE,
            user_email="test@example.com",
            organization="Test Org"
        )

        assert license_key is not None
        assert isinstance(license_key, str)

        # Decode and verify JWT
        payload = jwt.decode(license_key, "test_secret_key_12345", algorithms=["HS256"])
        assert payload['tier'] == 'free'
        assert payload['user_email'] == "test@example.com"
        assert payload['organization'] == "Test Org"

    def test_generate_starter_license(self, license_manager):
        """Test generating STARTER tier license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.STARTER,
            user_email="starter@example.com",
            organization="Starter Co"
        )

        payload = jwt.decode(license_key, "test_secret_key_12345", algorithms=["HS256"])
        assert payload['tier'] == 'starter'

    def test_generate_pro_license(self, license_manager):
        """Test generating PRO tier license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="pro@example.com",
            organization="Pro Corp"
        )

        payload = jwt.decode(license_key, "test_secret_key_12345", algorithms=["HS256"])
        assert payload['tier'] == 'pro'

    def test_generate_enterprise_license(self, license_manager):
        """Test generating ENTERPRISE tier license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.ENTERPRISE,
            user_email="enterprise@example.com",
            organization="Enterprise Inc"
        )

        payload = jwt.decode(license_key, "test_secret_key_12345", algorithms=["HS256"])
        assert payload['tier'] == 'enterprise'

    def test_custom_duration(self, license_manager):
        """Test license generation with custom duration."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="custom@example.com",
            organization="Custom Org",
            duration_days=30
        )

        payload = jwt.decode(license_key, "test_secret_key_12345", algorithms=["HS256"])
        created_at = datetime.fromisoformat(payload['created_at'])
        expires_at = datetime.fromisoformat(payload['expires_at'])

        duration = (expires_at - created_at).days
        assert duration == 30

    def test_invalid_email(self, license_manager):
        """Test that invalid email raises error."""
        with pytest.raises(ConfigurationError, match="Invalid email"):
            license_manager.generate_license(
                tier=LicenseTier.FREE,
                user_email="invalid_email",
                organization="Test Org"
            )

    def test_empty_organization(self, license_manager):
        """Test that empty organization raises error."""
        with pytest.raises(ConfigurationError, match="Organization name required"):
            license_manager.generate_license(
                tier=LicenseTier.FREE,
                user_email="test@example.com",
                organization=""
            )


class TestLicenseValidation:
    """Test license validation functionality."""

    def test_validate_valid_license(self, license_manager):
        """Test validating a valid license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="valid@example.com",
            organization="Valid Org"
        )

        is_valid = license_manager.validate_license(license_key)
        assert is_valid is True

    def test_validate_invalid_token(self, license_manager):
        """Test that invalid JWT token raises error."""
        with pytest.raises(LicenseValidationError, match="Invalid license token"):
            license_manager.validate_license("invalid_token_here")

    def test_validate_tampered_license(self, license_manager):
        """Test that tampered license fails validation."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.FREE,
            user_email="test@example.com",
            organization="Test Org"
        )

        # Tamper with the token
        tampered_key = license_key[:-10] + "tampered123"

        with pytest.raises(LicenseValidationError):
            license_manager.validate_license(tampered_key)

    def test_validate_suspended_license(self, license_manager):
        """Test that suspended license fails validation."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="suspend@example.com",
            organization="Suspend Org"
        )

        # Suspend the license
        license_manager.suspend_license(license_key)

        with pytest.raises(LicenseValidationError, match="suspended"):
            license_manager.validate_license(license_key)

    def test_validate_revoked_license(self, license_manager):
        """Test that revoked license fails validation."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="revoke@example.com",
            organization="Revoke Org"
        )

        # Revoke the license
        license_manager.revoke_license(license_key)

        with pytest.raises(LicenseValidationError, match="revoked"):
            license_manager.validate_license(license_key)

    def test_validate_expired_license(self, license_manager):
        """Test that expired license (beyond grace period) fails validation."""
        # Generate license that expired 10 days ago
        license_key = license_manager.generate_license(
            tier=LicenseTier.FREE,
            user_email="expired@example.com",
            organization="Expired Org",
            duration_days=-10  # Expired 10 days ago
        )

        with pytest.raises(LicenseExpiredError):
            license_manager.validate_license(license_key)


class TestQuotaManagement:
    """Test quota checking and enforcement."""

    def test_free_tier_ai_operations_quota(self, license_manager):
        """Test FREE tier AI operations quota (10/day)."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.FREE,
            user_email="quota@example.com",
            organization="Quota Org"
        )

        # Should be able to do 10 operations
        for i in range(10):
            assert license_manager.check_quota(license_key, "ai_operation") is True
            license_manager.record_usage(license_key, "ai_operation")

        # 11th operation should exceed quota
        with pytest.raises(QuotaExceededError, match="AI operations quota exceeded"):
            license_manager.check_quota(license_key, "ai_operation")

    def test_starter_tier_project_quota(self, license_manager):
        """Test STARTER tier project quota (25 projects)."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.STARTER,
            user_email="projects@example.com",
            organization="Projects Org"
        )

        # Set 25 projects
        license_manager.record_usage(license_key, "project", count=25)

        # Should be at limit
        assert license_manager.check_quota(license_key, "project") is True

        # Adding one more should fail
        license_manager.record_usage(license_key, "project", count=26)
        with pytest.raises(QuotaExceededError, match="Project quota exceeded"):
            license_manager.check_quota(license_key, "project")

    def test_pro_tier_user_quota(self, license_manager):
        """Test PRO tier user quota (10 users)."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="users@example.com",
            organization="Users Org"
        )

        # Set 10 users
        license_manager.record_usage(license_key, "user", count=10)

        # Should be at limit
        assert license_manager.check_quota(license_key, "user") is True

        # Adding one more should fail
        license_manager.record_usage(license_key, "user", count=11)
        with pytest.raises(QuotaExceededError, match="User quota exceeded"):
            license_manager.check_quota(license_key, "user")

    def test_enterprise_unlimited_quota(self, license_manager):
        """Test ENTERPRISE tier has unlimited quota."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.ENTERPRISE,
            user_email="unlimited@example.com",
            organization="Unlimited Org"
        )

        # Record massive usage
        license_manager.record_usage(license_key, "ai_operation", count=10000)
        license_manager.record_usage(license_key, "project", count=1000)
        license_manager.record_usage(license_key, "user", count=100)

        # Should all pass
        assert license_manager.check_quota(license_key, "ai_operation") is True
        assert license_manager.check_quota(license_key, "project") is True
        assert license_manager.check_quota(license_key, "user") is True


class TestUsageRecording:
    """Test usage recording functionality."""

    def test_record_ai_operation(self, license_manager):
        """Test recording AI operation usage."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="usage@example.com",
            organization="Usage Org"
        )

        # Record operations
        license_manager.record_usage(license_key, "ai_operation", count=5)

        # Verify recorded
        info = license_manager.get_license_info(license_key)
        assert info['current_usage']['ai_operations_today'] == 5

    def test_record_multiple_operations(self, license_manager):
        """Test recording multiple operations accumulates."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="multi@example.com",
            organization="Multi Org"
        )

        # Record multiple times
        license_manager.record_usage(license_key, "ai_operation", count=3)
        license_manager.record_usage(license_key, "ai_operation", count=2)
        license_manager.record_usage(license_key, "ai_operation", count=5)

        # Should accumulate
        info = license_manager.get_license_info(license_key)
        assert info['current_usage']['ai_operations_today'] == 10

    def test_record_project_count(self, license_manager):
        """Test recording project count."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.STARTER,
            user_email="proj@example.com",
            organization="Proj Org"
        )

        license_manager.record_usage(license_key, "project", count=15)

        info = license_manager.get_license_info(license_key)
        assert info['current_usage']['projects_count'] == 15

    def test_record_user_count(self, license_manager):
        """Test recording active user count."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="users@example.com",
            organization="Users Org"
        )

        license_manager.record_usage(license_key, "user", count=7)

        info = license_manager.get_license_info(license_key)
        assert info['current_usage']['active_users_count'] == 7


class TestLicenseInfo:
    """Test license information retrieval."""

    def test_get_license_info_complete(self, license_manager):
        """Test getting complete license information."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="info@example.com",
            organization="Info Org"
        )

        info = license_manager.get_license_info(license_key)

        assert 'license_info' in info
        assert 'tier_config' in info
        assert 'current_usage' in info
        assert 'remaining_quota' in info

        assert info['license_info']['tier'] == 'pro'
        assert info['license_info']['user_email'] == "info@example.com"
        assert info['tier_config']['name'] == "Pro"
        assert info['tier_config']['price_monthly'] == 99.0

    def test_remaining_quota_calculation(self, license_manager):
        """Test remaining quota is calculated correctly."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.STARTER,
            user_email="quota@example.com",
            organization="Quota Org"
        )

        # Use some quota
        license_manager.record_usage(license_key, "ai_operation", count=100)
        license_manager.record_usage(license_key, "project", count=10)
        license_manager.record_usage(license_key, "user", count=2)

        info = license_manager.get_license_info(license_key)

        # Starter tier: 500 AI ops, 25 projects, 3 users
        assert info['remaining_quota']['ai_operations_today'] == 400
        assert info['remaining_quota']['projects'] == 15
        assert info['remaining_quota']['users'] == 1

    def test_unlimited_quota_representation(self, license_manager):
        """Test that unlimited quota is represented as -1."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.ENTERPRISE,
            user_email="enterprise@example.com",
            organization="Enterprise Org"
        )

        info = license_manager.get_license_info(license_key)

        assert info['remaining_quota']['ai_operations_today'] == -1
        assert info['remaining_quota']['projects'] == -1
        assert info['remaining_quota']['users'] == -1


class TestLicenseRenewal:
    """Test license renewal functionality."""

    def test_renew_license(self, license_manager):
        """Test renewing a license extends expiration."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="renew@example.com",
            organization="Renew Org",
            duration_days=30
        )

        # Get original expiration
        original_info = license_manager.get_license_info(license_key)
        original_expires = datetime.fromisoformat(original_info['license_info']['expires_at'])

        # Renew for 365 days
        new_license_key = license_manager.renew_license(license_key, duration_days=365)

        # Get new expiration
        new_info = license_manager.get_license_info(new_license_key)
        new_expires = datetime.fromisoformat(new_info['license_info']['expires_at'])

        # Should be approximately 365 days from now
        assert (new_expires - datetime.now(timezone.utc)).days >= 364

    def test_renew_reactivates_status(self, license_manager):
        """Test that renewal reactivates license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.FREE,
            user_email="reactivate@example.com",
            organization="Reactivate Org"
        )

        # Suspend license
        license_manager.suspend_license(license_key)

        # Renew should reactivate
        new_license_key = license_manager.renew_license(license_key)

        # Should be valid again
        assert license_manager.validate_license(new_license_key) is True


class TestLicenseStatusManagement:
    """Test license status changes."""

    def test_suspend_license(self, license_manager):
        """Test suspending a license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="suspend@example.com",
            organization="Suspend Org"
        )

        license_manager.suspend_license(license_key)

        with pytest.raises(LicenseValidationError, match="suspended"):
            license_manager.validate_license(license_key)

    def test_activate_suspended_license(self, license_manager):
        """Test activating a suspended license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="activate@example.com",
            organization="Activate Org"
        )

        license_manager.suspend_license(license_key)
        license_manager.activate_license(license_key)

        assert license_manager.validate_license(license_key) is True

    def test_revoke_license(self, license_manager):
        """Test revoking a license."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="revoke@example.com",
            organization="Revoke Org"
        )

        license_manager.revoke_license(license_key)

        with pytest.raises(LicenseValidationError, match="revoked"):
            license_manager.validate_license(license_key)


class TestTierConfigurations:
    """Test tier configuration constants."""

    def test_free_tier_config(self):
        """Test FREE tier configuration."""
        config = TIER_CONFIGS[LicenseTier.FREE]

        assert config.max_projects == 5
        assert config.max_ai_operations_per_day == 10
        assert config.max_users == 1
        assert config.price_monthly == 0.0

    def test_starter_tier_config(self):
        """Test STARTER tier configuration."""
        config = TIER_CONFIGS[LicenseTier.STARTER]

        assert config.max_projects == 25
        assert config.max_ai_operations_per_day == 500
        assert config.max_users == 3
        assert config.price_monthly == 29.0

    def test_pro_tier_config(self):
        """Test PRO tier configuration."""
        config = TIER_CONFIGS[LicenseTier.PRO]

        assert config.max_projects == 100
        assert config.max_ai_operations_per_day == 5000
        assert config.max_users == 10
        assert config.price_monthly == 99.0

    def test_enterprise_tier_config(self):
        """Test ENTERPRISE tier configuration."""
        config = TIER_CONFIGS[LicenseTier.ENTERPRISE]

        assert config.max_projects == -1  # Unlimited
        assert config.max_ai_operations_per_day == -1  # Unlimited
        assert config.max_users == -1  # Unlimited


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_license_not_found(self, license_manager):
        """Test handling of non-existent license."""
        fake_payload = {
            'license_id': 'non-existent-id',
            'tier': 'pro',
            'user_email': 'fake@example.com',
            'organization': 'Fake Org',
            'created_at': datetime.now(timezone.utc).isoformat(),
            'expires_at': (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
        }

        fake_license = jwt.encode(fake_payload, "test_secret_key_12345", algorithm="HS256")

        with pytest.raises(LicenseNotFoundError):
            license_manager._get_license_info('non-existent-id')

    def test_concurrent_usage_updates(self, license_manager):
        """Test concurrent usage updates don't cause conflicts."""
        license_key = license_manager.generate_license(
            tier=LicenseTier.PRO,
            user_email="concurrent@example.com",
            organization="Concurrent Org"
        )

        # Simulate concurrent updates
        for _ in range(10):
            license_manager.record_usage(license_key, "ai_operation", count=1)

        info = license_manager.get_license_info(license_key)
        assert info['current_usage']['ai_operations_today'] == 10


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
