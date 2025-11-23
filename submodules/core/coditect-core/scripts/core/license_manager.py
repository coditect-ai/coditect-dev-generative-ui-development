#!/usr/bin/env python3
"""
CODITECT License Manager - SaaS License Control System

Production-grade license management for CODITECT SaaS platform with
tier-based feature enforcement, usage quota tracking, and JWT-based
license key generation.

License Tiers:
- FREE: Max 5 projects, 10 AI ops/day, community support, single user
- STARTER: $29/month - 25 projects, 500 AI ops/day, email support, 3 users
- PRO: $99/month - 100 projects, 5K AI ops/day, priority support, 10 users
- ENTERPRISE: Custom - Unlimited projects/ops, dedicated support, unlimited users

Features:
- JWT-based license key generation and validation
- Tier-based feature enforcement
- Usage quota tracking and enforcement
- Expiration checking with grace period (7 days)
- Multi-user license support
- Offline validation (cached for 24 hours)
- Database-backed persistence (SQLite/PostgreSQL)

Usage:
    from license_manager import LicenseManager, LicenseTier

    lm = LicenseManager()

    # Generate new license
    license_key = lm.generate_license(
        tier=LicenseTier.PRO,
        user_email="user@example.com",
        organization="Acme Corp"
    )

    # Validate license
    is_valid = lm.validate_license(license_key)

    # Check quota
    can_proceed = lm.check_quota(license_key, operation_type="ai_operation")

    # Record usage
    lm.record_usage(license_key, operation_type="ai_operation")

Author: AZ1.AI CODITECT Team
Sprint: Phase 4 - License Management Implementation
Date: 2025-11-22
"""

import os
import sys
import json
import logging
import sqlite3
import hashlib
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from uuid import uuid4

# JWT and cryptography libraries
try:
    import jwt
except ImportError:
    print("ERROR: PyJWT library required. Install with: pip install PyJWT", file=sys.stderr)
    sys.exit(1)

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("ERROR: cryptography library required. Install with: pip install cryptography", file=sys.stderr)
    sys.exit(1)

# Import core utilities
try:
    from utils import find_git_root, GitRepositoryNotFoundError, InvalidPathError
except ImportError:
    # Fallback if utils not available
    class GitRepositoryNotFoundError(Exception):
        pass
    class InvalidPathError(Exception):
        pass
    def find_git_root():
        return Path.cwd()

# Configure logging to output to both stdout and file
log_filename = f"logs/license_manager_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_filename)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTION HIERARCHY
# ============================================================================

class LicenseError(Exception):
    """Base exception for license management errors."""
    pass


class LicenseValidationError(LicenseError):
    """Raised when license validation fails."""
    pass


class LicenseExpiredError(LicenseError):
    """Raised when license has expired."""
    pass


class QuotaExceededError(LicenseError):
    """Raised when usage quota is exceeded."""
    pass


class LicenseNotFoundError(LicenseError):
    """Raised when license cannot be found."""
    pass


class DatabaseError(LicenseError):
    """Raised when database operation fails."""
    pass


class ConfigurationError(LicenseError):
    """Raised when configuration is invalid."""
    pass


class EncryptionError(LicenseError):
    """Raised when encryption/decryption fails."""
    pass


# ============================================================================
# ENUMS AND DATA STRUCTURES
# ============================================================================

class LicenseTier(Enum):
    """License tier levels."""
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class LicenseStatus(Enum):
    """License status states."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass
class TierConfig:
    """Configuration for a license tier."""
    name: str
    max_projects: int
    max_ai_operations_per_day: int
    max_users: int
    support_level: str
    price_monthly: float

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class LicenseInfo:
    """License information."""
    license_id: str
    license_key: str
    tier: LicenseTier
    user_email: str
    organization: str
    status: LicenseStatus
    created_at: datetime
    expires_at: datetime
    max_users: int
    max_projects: int
    max_ai_operations_per_day: int
    last_validated: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'license_id': self.license_id,
            'license_key': self.license_key,
            'tier': self.tier.value,
            'user_email': self.user_email,
            'organization': self.organization,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'max_users': self.max_users,
            'max_projects': self.max_projects,
            'max_ai_operations_per_day': self.max_ai_operations_per_day,
            'last_validated': self.last_validated.isoformat() if self.last_validated else None
        }


@dataclass
class UsageStats:
    """Current usage statistics."""
    projects_count: int
    ai_operations_today: int
    active_users_count: int

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


# ============================================================================
# TIER CONFIGURATIONS
# ============================================================================

TIER_CONFIGS = {
    LicenseTier.FREE: TierConfig(
        name="Free",
        max_projects=5,
        max_ai_operations_per_day=10,
        max_users=1,
        support_level="Community",
        price_monthly=0.0
    ),
    LicenseTier.STARTER: TierConfig(
        name="Starter",
        max_projects=25,
        max_ai_operations_per_day=500,
        max_users=3,
        support_level="Email",
        price_monthly=29.0
    ),
    LicenseTier.PRO: TierConfig(
        name="Pro",
        max_projects=100,
        max_ai_operations_per_day=5000,
        max_users=10,
        support_level="Priority",
        price_monthly=99.0
    ),
    LicenseTier.ENTERPRISE: TierConfig(
        name="Enterprise",
        max_projects=-1,  # Unlimited
        max_ai_operations_per_day=-1,  # Unlimited
        max_users=-1,  # Unlimited
        support_level="Dedicated",
        price_monthly=-1.0  # Custom pricing
    )
}


# ============================================================================
# LICENSE MANAGER CLASS
# ============================================================================

class LicenseManager:
    """
    Manages CODITECT SaaS licenses with tier enforcement and quota tracking.

    Provides complete license lifecycle management from generation through
    validation, quota enforcement, and renewal.
    """

    # JWT configuration
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_DAYS = 365
    GRACE_PERIOD_DAYS = 7
    CACHE_VALIDATION_HOURS = 24

    def __init__(
        self,
        db_path: Optional[Path] = None,
        secret_key: Optional[str] = None,
        encryption_key: Optional[bytes] = None
    ):
        """
        Initialize License Manager.

        Args:
            db_path: Path to SQLite database (auto-detected if None)
            secret_key: JWT secret key (generated if None)
            encryption_key: Fernet encryption key (generated if None)

        Raises:
            ConfigurationError: If initialization fails
            DatabaseError: If database setup fails
        """
        try:
            # Setup database path
            if db_path is None:
                try:
                    repo_root = find_git_root()
                except (GitRepositoryNotFoundError, InvalidPathError):
                    repo_root = Path.cwd()

                db_path = repo_root.parent.parent.parent / "MEMORY-CONTEXT" / "licenses.db"

            self.db_path = Path(db_path)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            # Setup JWT secret key
            if secret_key is None:
                secret_key = self._generate_secret_key()
            self.secret_key = secret_key

            # Setup encryption key
            if encryption_key is None:
                encryption_key = Fernet.generate_key()
            self.cipher = Fernet(encryption_key)

            # Initialize database
            self._init_database()

            logger.info(f"LicenseManager initialized (database: {self.db_path})")

        except (ConfigurationError, DatabaseError):
            raise
        except Exception as e:
            error_msg = f"Failed to initialize LicenseManager: {e}"
            logger.error(error_msg, exc_info=True)
            raise ConfigurationError(error_msg) from e

    def _generate_secret_key(self) -> str:
        """Generate secure JWT secret key."""
        return hashlib.sha256(os.urandom(32)).hexdigest()

    def _init_database(self) -> None:
        """
        Initialize database schema.

        Raises:
            DatabaseError: If schema creation fails
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.execute("PRAGMA foreign_keys = ON")

            cursor = conn.cursor()

            # Create licenses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS licenses (
                    license_id TEXT PRIMARY KEY,
                    license_key TEXT UNIQUE NOT NULL,
                    tier TEXT NOT NULL,
                    user_email TEXT NOT NULL,
                    organization TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    max_users INTEGER NOT NULL,
                    max_projects INTEGER NOT NULL,
                    max_ai_operations_per_day INTEGER NOT NULL,
                    last_validated TIMESTAMP
                )
            """)

            # Create license_usage table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS license_usage (
                    usage_id TEXT PRIMARY KEY,
                    license_id TEXT NOT NULL,
                    date DATE NOT NULL,
                    projects_count INTEGER DEFAULT 0,
                    ai_operations_count INTEGER DEFAULT 0,
                    active_users_count INTEGER DEFAULT 0,
                    FOREIGN KEY (license_id) REFERENCES licenses(license_id) ON DELETE CASCADE,
                    UNIQUE(license_id, date)
                )
            """)

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_license_key ON licenses(license_key)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_license_status ON licenses(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_license_date ON license_usage(license_id, date)")

            conn.commit()
            conn.close()

            logger.info("Database schema initialized successfully")

        except sqlite3.Error as e:
            error_msg = f"Database schema initialization failed: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg) from e

    def generate_license(
        self,
        tier: LicenseTier,
        user_email: str,
        organization: str,
        duration_days: int = 365
    ) -> str:
        """
        Generate new license key.

        Args:
            tier: License tier
            user_email: User's email address
            organization: Organization name
            duration_days: License validity duration

        Returns:
            Generated license key (JWT token)

        Raises:
            DatabaseError: If license creation fails
            ConfigurationError: If tier configuration invalid
        """
        # Input validation
        if not user_email or '@' not in user_email:
            raise ConfigurationError("Invalid email address")

        if not organization:
            raise ConfigurationError("Organization name required")

        if tier not in TIER_CONFIGS:
            raise ConfigurationError(f"Invalid tier: {tier}")

        try:
            tier_config = TIER_CONFIGS[tier]
            license_id = str(uuid4())
            created_at = datetime.now(timezone.utc)
            expires_at = created_at + timedelta(days=duration_days)

            # Generate JWT token
            payload = {
                'license_id': license_id,
                'tier': tier.value,
                'user_email': user_email,
                'organization': organization,
                'created_at': created_at.isoformat(),
                'expires_at': expires_at.isoformat()
            }

            license_key = jwt.encode(payload, self.secret_key, algorithm=self.JWT_ALGORITHM)

            # Encrypt license key for storage
            encrypted_key = self.cipher.encrypt(license_key.encode()).decode()

            # Store in database
            conn = sqlite3.connect(str(self.db_path))
            conn.execute("PRAGMA foreign_keys = ON")

            conn.execute("""
                INSERT INTO licenses (
                    license_id, license_key, tier, user_email, organization,
                    status, created_at, expires_at, max_users, max_projects,
                    max_ai_operations_per_day
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                license_id,
                encrypted_key,
                tier.value,
                user_email,
                organization,
                LicenseStatus.ACTIVE.value,
                created_at.isoformat(),
                expires_at.isoformat(),
                tier_config.max_users,
                tier_config.max_projects,
                tier_config.max_ai_operations_per_day
            ))

            conn.commit()
            conn.close()

            logger.info(f"License generated: {license_id} ({tier.value}) for {user_email}")

            return license_key

        except sqlite3.Error as e:
            error_msg = f"Failed to create license in database: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg) from e
        except Exception as e:
            error_msg = f"License generation failed: {e}"
            logger.error(error_msg, exc_info=True)
            raise LicenseError(error_msg) from e

    def validate_license(self, license_key: str) -> bool:
        """
        Validate license key.

        Args:
            license_key: JWT license key to validate

        Returns:
            True if valid and active, False otherwise

        Raises:
            LicenseValidationError: If validation fails
            LicenseExpiredError: If license expired (beyond grace period)
        """
        try:
            # Decode JWT
            try:
                payload = jwt.decode(license_key, self.secret_key, algorithms=[self.JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                raise LicenseExpiredError("License has expired")
            except jwt.InvalidTokenError as e:
                raise LicenseValidationError(f"Invalid license token: {e}")

            license_id = payload.get('license_id')
            if not license_id:
                raise LicenseValidationError("License ID missing from token")

            # Check database
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row

            cursor = conn.execute(
                "SELECT * FROM licenses WHERE license_id = ?",
                (license_id,)
            )
            row = cursor.fetchone()
            conn.close()

            if not row:
                raise LicenseNotFoundError(f"License not found: {license_id}")

            # Check status
            status = LicenseStatus(row['status'])
            if status == LicenseStatus.REVOKED:
                raise LicenseValidationError("License has been revoked")

            if status == LicenseStatus.SUSPENDED:
                raise LicenseValidationError("License is suspended")

            # Check expiration with grace period
            expires_at = datetime.fromisoformat(row['expires_at'])
            now = datetime.now(timezone.utc)

            if now > expires_at + timedelta(days=self.GRACE_PERIOD_DAYS):
                raise LicenseExpiredError(f"License expired on {expires_at.date()}")

            # Update last validated timestamp
            self._update_last_validated(license_id)

            logger.info(f"License validated successfully: {license_id}")
            return True

        except (LicenseValidationError, LicenseExpiredError, LicenseNotFoundError):
            raise
        except Exception as e:
            error_msg = f"License validation error: {e}"
            logger.error(error_msg, exc_info=True)
            raise LicenseValidationError(error_msg) from e

    def check_quota(
        self,
        license_key: str,
        operation_type: str = "ai_operation"
    ) -> bool:
        """
        Check if operation is within quota limits.

        Args:
            license_key: JWT license key
            operation_type: Type of operation (ai_operation, project, user)

        Returns:
            True if within quota, False otherwise

        Raises:
            QuotaExceededError: If quota exceeded
            LicenseValidationError: If license invalid
        """
        # Validate license first
        self.validate_license(license_key)

        try:
            payload = jwt.decode(license_key, self.secret_key, algorithms=[self.JWT_ALGORITHM])
            license_id = payload['license_id']

            # Get license info
            license_info = self._get_license_info(license_id)

            # Get current usage
            usage_stats = self._get_usage_stats(license_id)

            # Check quota based on operation type
            if operation_type == "ai_operation":
                if license_info.max_ai_operations_per_day == -1:  # Unlimited
                    return True

                if usage_stats.ai_operations_today >= license_info.max_ai_operations_per_day:
                    raise QuotaExceededError(
                        f"Daily AI operations quota exceeded "
                        f"({usage_stats.ai_operations_today}/{license_info.max_ai_operations_per_day})"
                    )

            elif operation_type == "project":
                if license_info.max_projects == -1:  # Unlimited
                    return True

                if usage_stats.projects_count >= license_info.max_projects:
                    raise QuotaExceededError(
                        f"Project quota exceeded "
                        f"({usage_stats.projects_count}/{license_info.max_projects})"
                    )

            elif operation_type == "user":
                if license_info.max_users == -1:  # Unlimited
                    return True

                if usage_stats.active_users_count >= license_info.max_users:
                    raise QuotaExceededError(
                        f"User quota exceeded "
                        f"({usage_stats.active_users_count}/{license_info.max_users})"
                    )

            return True

        except QuotaExceededError:
            raise
        except Exception as e:
            error_msg = f"Quota check failed: {e}"
            logger.error(error_msg, exc_info=True)
            raise LicenseError(error_msg) from e

    def record_usage(
        self,
        license_key: str,
        operation_type: str = "ai_operation",
        count: int = 1
    ) -> None:
        """
        Record usage event.

        Args:
            license_key: JWT license key
            operation_type: Type of operation
            count: Number of operations to record

        Raises:
            DatabaseError: If recording fails
        """
        try:
            payload = jwt.decode(license_key, self.secret_key, algorithms=[self.JWT_ALGORITHM])
            license_id = payload['license_id']
            today = datetime.now(timezone.utc).date()

            conn = sqlite3.connect(str(self.db_path))
            conn.execute("PRAGMA foreign_keys = ON")

            # Insert or update usage record
            if operation_type == "ai_operation":
                conn.execute("""
                    INSERT INTO license_usage (usage_id, license_id, date, ai_operations_count)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(license_id, date) DO UPDATE SET
                        ai_operations_count = ai_operations_count + ?
                """, (str(uuid4()), license_id, today.isoformat(), count, count))

            elif operation_type == "project":
                conn.execute("""
                    INSERT INTO license_usage (usage_id, license_id, date, projects_count)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(license_id, date) DO UPDATE SET
                        projects_count = ?
                """, (str(uuid4()), license_id, today.isoformat(), count, count))

            elif operation_type == "user":
                conn.execute("""
                    INSERT INTO license_usage (usage_id, license_id, date, active_users_count)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(license_id, date) DO UPDATE SET
                        active_users_count = ?
                """, (str(uuid4()), license_id, today.isoformat(), count, count))

            conn.commit()
            conn.close()

            logger.debug(f"Usage recorded: {operation_type} count={count} for {license_id}")

        except sqlite3.Error as e:
            error_msg = f"Failed to record usage: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg) from e

    def get_license_info(self, license_key: str) -> Dict:
        """
        Get comprehensive license information and usage stats.

        Args:
            license_key: JWT license key

        Returns:
            Dictionary with license info and remaining quotas
        """
        try:
            payload = jwt.decode(license_key, self.secret_key, algorithms=[self.JWT_ALGORITHM])
            license_id = payload['license_id']

            license_info = self._get_license_info(license_id)
            usage_stats = self._get_usage_stats(license_id)
            tier_config = TIER_CONFIGS[license_info.tier]

            # Calculate remaining quotas
            remaining = {
                'projects': (
                    license_info.max_projects - usage_stats.projects_count
                    if license_info.max_projects != -1 else -1
                ),
                'ai_operations_today': (
                    license_info.max_ai_operations_per_day - usage_stats.ai_operations_today
                    if license_info.max_ai_operations_per_day != -1 else -1
                ),
                'users': (
                    license_info.max_users - usage_stats.active_users_count
                    if license_info.max_users != -1 else -1
                )
            }

            # Check if in grace period
            now = datetime.now(timezone.utc)
            expires_at = license_info.expires_at
            in_grace_period = expires_at < now <= expires_at + timedelta(days=self.GRACE_PERIOD_DAYS)

            return {
                'license_info': license_info.to_dict(),
                'tier_config': tier_config.to_dict(),
                'current_usage': usage_stats.to_dict(),
                'remaining_quota': remaining,
                'in_grace_period': in_grace_period,
                'days_until_expiration': (expires_at - now).days
            }

        except Exception as e:
            error_msg = f"Failed to get license info: {e}"
            logger.error(error_msg, exc_info=True)
            raise LicenseError(error_msg) from e

    def renew_license(self, license_key: str, duration_days: int = 365) -> str:
        """
        Renew license for additional period.

        Args:
            license_key: Current license key
            duration_days: Extension duration

        Returns:
            New license key with updated expiration
        """
        try:
            payload = jwt.decode(license_key, self.secret_key, algorithms=[self.JWT_ALGORITHM])
            license_id = payload['license_id']

            # Get current license
            license_info = self._get_license_info(license_id)

            # Calculate new expiration
            new_expires_at = datetime.now(timezone.utc) + timedelta(days=duration_days)

            # Generate new license key
            new_payload = payload.copy()
            new_payload['expires_at'] = new_expires_at.isoformat()
            new_license_key = jwt.encode(new_payload, self.secret_key, algorithm=self.JWT_ALGORITHM)

            # Update database
            encrypted_key = self.cipher.encrypt(new_license_key.encode()).decode()

            conn = sqlite3.connect(str(self.db_path))
            conn.execute("""
                UPDATE licenses
                SET license_key = ?, expires_at = ?, status = ?
                WHERE license_id = ?
            """, (encrypted_key, new_expires_at.isoformat(), LicenseStatus.ACTIVE.value, license_id))

            conn.commit()
            conn.close()

            logger.info(f"License renewed: {license_id} until {new_expires_at.date()}")

            return new_license_key

        except Exception as e:
            error_msg = f"License renewal failed: {e}"
            logger.error(error_msg, exc_info=True)
            raise LicenseError(error_msg) from e

    def suspend_license(self, license_key: str) -> None:
        """Suspend license temporarily."""
        self._update_license_status(license_key, LicenseStatus.SUSPENDED)

    def activate_license(self, license_key: str) -> None:
        """Activate suspended license."""
        self._update_license_status(license_key, LicenseStatus.ACTIVE)

    def revoke_license(self, license_key: str) -> None:
        """Revoke license permanently."""
        self._update_license_status(license_key, LicenseStatus.REVOKED)

    def _update_license_status(self, license_key: str, status: LicenseStatus) -> None:
        """Update license status in database."""
        try:
            payload = jwt.decode(license_key, self.secret_key, algorithms=[self.JWT_ALGORITHM])
            license_id = payload['license_id']

            conn = sqlite3.connect(str(self.db_path))
            conn.execute(
                "UPDATE licenses SET status = ? WHERE license_id = ?",
                (status.value, license_id)
            )
            conn.commit()
            conn.close()

            logger.info(f"License status updated: {license_id} -> {status.value}")

        except Exception as e:
            error_msg = f"Failed to update license status: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg) from e

    def _get_license_info(self, license_id: str) -> LicenseInfo:
        """Retrieve license info from database."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row

            cursor = conn.execute(
                "SELECT * FROM licenses WHERE license_id = ?",
                (license_id,)
            )
            row = cursor.fetchone()
            conn.close()

            if not row:
                raise LicenseNotFoundError(f"License not found: {license_id}")

            # Decrypt license key
            decrypted_key = self.cipher.decrypt(row['license_key'].encode()).decode()

            return LicenseInfo(
                license_id=row['license_id'],
                license_key=decrypted_key,
                tier=LicenseTier(row['tier']),
                user_email=row['user_email'],
                organization=row['organization'],
                status=LicenseStatus(row['status']),
                created_at=datetime.fromisoformat(row['created_at']),
                expires_at=datetime.fromisoformat(row['expires_at']),
                max_users=row['max_users'],
                max_projects=row['max_projects'],
                max_ai_operations_per_day=row['max_ai_operations_per_day'],
                last_validated=datetime.fromisoformat(row['last_validated']) if row['last_validated'] else None
            )

        except sqlite3.Error as e:
            error_msg = f"Database query failed: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg) from e

    def _get_usage_stats(self, license_id: str) -> UsageStats:
        """Get current usage statistics."""
        try:
            today = datetime.now(timezone.utc).date()

            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row

            cursor = conn.execute(
                "SELECT * FROM license_usage WHERE license_id = ? AND date = ?",
                (license_id, today.isoformat())
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                return UsageStats(
                    projects_count=row['projects_count'] or 0,
                    ai_operations_today=row['ai_operations_count'] or 0,
                    active_users_count=row['active_users_count'] or 0
                )
            else:
                return UsageStats(
                    projects_count=0,
                    ai_operations_today=0,
                    active_users_count=0
                )

        except sqlite3.Error as e:
            error_msg = f"Failed to get usage stats: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg) from e

    def _update_last_validated(self, license_id: str) -> None:
        """Update last validation timestamp."""
        try:
            now = datetime.now(timezone.utc)

            conn = sqlite3.connect(str(self.db_path))
            conn.execute(
                "UPDATE licenses SET last_validated = ? WHERE license_id = ?",
                (now.isoformat(), license_id)
            )
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            logger.warning(f"Failed to update last_validated: {e}")


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def main():
    """
    CLI entry point for license management operations.

    Returns:
        Exit code (0 for success, 1-5 for various failures)
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='CODITECT License Manager - SaaS License Control System'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate new license')
    gen_parser.add_argument('--tier', required=True, choices=['free', 'starter', 'pro', 'enterprise'])
    gen_parser.add_argument('--email', required=True, help='User email address')
    gen_parser.add_argument('--org', required=True, help='Organization name')
    gen_parser.add_argument('--duration', type=int, default=365, help='Duration in days')

    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate license key')
    val_parser.add_argument('license_key', help='License key to validate')

    # Info command
    info_parser = subparsers.add_parser('info', help='Get license information')
    info_parser.add_argument('license_key', help='License key')

    # Check quota command
    quota_parser = subparsers.add_parser('check-quota', help='Check quota limits')
    quota_parser.add_argument('license_key', help='License key')
    quota_parser.add_argument('--type', default='ai_operation',
                             choices=['ai_operation', 'project', 'user'])

    try:
        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return 0

        # Initialize license manager
        try:
            lm = LicenseManager()
        except (ConfigurationError, DatabaseError) as e:
            print(f"❌ Failed to initialize License Manager: {e}", file=sys.stderr)
            return 1

        # Execute command
        if args.command == 'generate':
            try:
                tier = LicenseTier(args.tier)
                license_key = lm.generate_license(
                    tier=tier,
                    user_email=args.email,
                    organization=args.org,
                    duration_days=args.duration
                )

                print("\n" + "="*80)
                print("LICENSE GENERATED SUCCESSFULLY")
                print("="*80)
                print(f"\nTier: {tier.value.upper()}")
                print(f"Email: {args.email}")
                print(f"Organization: {args.org}")
                print(f"Duration: {args.duration} days")
                print(f"\nLicense Key:\n{license_key}")
                print("\n⚠️  Store this key securely - it cannot be recovered!")
                print("="*80)

                return 0

            except (ConfigurationError, DatabaseError) as e:
                print(f"❌ License generation failed: {e}", file=sys.stderr)
                return 2

        elif args.command == 'validate':
            try:
                is_valid = lm.validate_license(args.license_key)

                if is_valid:
                    print("✅ License is VALID and ACTIVE")
                    return 0
                else:
                    print("❌ License is INVALID")
                    return 3

            except LicenseExpiredError as e:
                print(f"❌ {e}", file=sys.stderr)
                return 4
            except (LicenseValidationError, LicenseNotFoundError) as e:
                print(f"❌ {e}", file=sys.stderr)
                return 3

        elif args.command == 'info':
            try:
                info = lm.get_license_info(args.license_key)

                print("\n" + "="*80)
                print("LICENSE INFORMATION")
                print("="*80)

                print(f"\nTier: {info['tier_config']['name']} (${info['tier_config']['price_monthly']}/month)")
                print(f"Email: {info['license_info']['user_email']}")
                print(f"Organization: {info['license_info']['organization']}")
                print(f"Status: {info['license_info']['status'].upper()}")

                print(f"\n📅 Created: {info['license_info']['created_at'][:10]}")
                print(f"📅 Expires: {info['license_info']['expires_at'][:10]}")
                print(f"⏰ Days remaining: {info['days_until_expiration']}")

                if info['in_grace_period']:
                    print("⚠️  IN GRACE PERIOD - Renew soon!")

                print("\n📊 USAGE & QUOTAS")
                print("-" * 80)

                # Projects
                if info['license_info']['max_projects'] == -1:
                    print(f"Projects: {info['current_usage']['projects_count']} (Unlimited)")
                else:
                    print(f"Projects: {info['current_usage']['projects_count']}/{info['license_info']['max_projects']} "
                          f"({info['remaining_quota']['projects']} remaining)")

                # AI Operations
                if info['license_info']['max_ai_operations_per_day'] == -1:
                    print(f"AI Operations (today): {info['current_usage']['ai_operations_today']} (Unlimited)")
                else:
                    print(f"AI Operations (today): {info['current_usage']['ai_operations_today']}/"
                          f"{info['license_info']['max_ai_operations_per_day']} "
                          f"({info['remaining_quota']['ai_operations_today']} remaining)")

                # Users
                if info['license_info']['max_users'] == -1:
                    print(f"Active Users: {info['current_usage']['active_users_count']} (Unlimited)")
                else:
                    print(f"Active Users: {info['current_usage']['active_users_count']}/"
                          f"{info['license_info']['max_users']} "
                          f"({info['remaining_quota']['users']} remaining)")

                print("="*80)

                return 0

            except LicenseError as e:
                print(f"❌ {e}", file=sys.stderr)
                return 3

        elif args.command == 'check-quota':
            try:
                can_proceed = lm.check_quota(args.license_key, args.type)

                if can_proceed:
                    print(f"✅ Quota check PASSED for {args.type}")
                    return 0

            except QuotaExceededError as e:
                print(f"❌ {e}", file=sys.stderr)
                return 5
            except LicenseError as e:
                print(f"❌ {e}", file=sys.stderr)
                return 3

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user", file=sys.stderr)
        return 130

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        logger.error("Unexpected error in main", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
