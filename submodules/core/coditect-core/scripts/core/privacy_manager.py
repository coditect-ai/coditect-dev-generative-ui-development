#!/usr/bin/env python3
"""
CODITECT Privacy Control Manager

Implements privacy-aware data handling with PII detection, redaction,
and 4-level privacy model for MEMORY-CONTEXT system.

Privacy Levels:
- PUBLIC: Can be shared publicly, no PII
- TEAM: Internal team sharing, some PII allowed
- PRIVATE: Restricted access, full PII allowed
- EPHEMERAL: Never stored, session-only

Features:
- Automatic PII detection (emails, phones, SSN, credit cards, IP addresses, etc.)
- Configurable redaction strategies
- Privacy-aware export filtering
- GDPR compliance support
- Audit trail for privacy operations

Usage:
    from privacy_manager import PrivacyManager, PrivacyLevel

    pm = PrivacyManager()

    # Detect PII
    pii_found = pm.detect_pii(text)

    # Redact based on privacy level
    safe_text = pm.redact(text, level=PrivacyLevel.PUBLIC)

    # Check if content is safe for level
    is_safe = pm.is_safe_for_level(text, PrivacyLevel.TEAM)

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation
Date: 2025-11-16
"""

import os
import re
import json
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

# Import core utilities
from utils import find_git_root

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PrivacyLevel(Enum):
    """Privacy levels for data handling."""
    PUBLIC = "public"           # Can be shared publicly, no PII
    TEAM = "team"               # Internal team sharing, minimal PII
    PRIVATE = "private"         # Restricted access, full PII allowed
    EPHEMERAL = "ephemeral"     # Never stored, session-only


class PIIType(Enum):
    """Types of Personally Identifiable Information."""
    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    IP_ADDRESS = "ip_address"
    API_KEY = "api_key"
    PASSWORD = "password"
    AWS_KEY = "aws_key"
    GITHUB_TOKEN = "github_token"  # All GitHub token types
    GITHUB_PAT = "github_pat"       # Fine-grained PAT
    GITHUB_OAUTH = "github_oauth"   # OAuth tokens
    NAME = "name"               # Requires ML model for accuracy
    ADDRESS = "address"         # Requires ML model for accuracy
    DATE_OF_BIRTH = "date_of_birth"


@dataclass
class PIIDetection:
    """Represents a detected PII instance."""
    pii_type: PIIType
    value: str
    start: int
    end: int
    confidence: float           # 0.0 to 1.0
    context: str                # Surrounding text for verification


@dataclass
class PrivacyConfig:
    """Privacy configuration settings."""
    default_level: PrivacyLevel
    auto_redact: bool
    pii_types_to_detect: List[PIIType]
    redaction_char: str
    preserve_format: bool       # e.g., xxx-xxx-1234 instead of [REDACTED]
    audit_enabled: bool
    gdpr_mode: bool

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'default_level': self.default_level.value,
            'auto_redact': self.auto_redact,
            'pii_types_to_detect': [t.value for t in self.pii_types_to_detect],
            'redaction_char': self.redaction_char,
            'preserve_format': self.preserve_format,
            'audit_enabled': self.audit_enabled,
            'gdpr_mode': self.gdpr_mode
        }


class PrivacyManager:
    """
    Manages privacy controls for MEMORY-CONTEXT system.

    Provides PII detection, redaction, and privacy-level filtering.
    """

    # PII Detection Patterns (regex-based, high confidence)
    PII_PATTERNS = {
        PIIType.EMAIL: r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        PIIType.PHONE: r'\b(?:(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?)?([0-9]{3})[-.]?([0-9]{4})\b',  # Matches 7 or 10 digit phone numbers
        PIIType.SSN: r'\b\d{3}-\d{2}-\d{4}\b',
        PIIType.CREDIT_CARD: r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        PIIType.IP_ADDRESS: r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        PIIType.API_KEY: r'\b[A-Za-z0-9]{32,}\b',  # Generic long alphanumeric
        PIIType.AWS_KEY: r'AKIA[0-9A-Z]{16}',
        # GitHub tokens - ALL types with flexible length (minimum 20 chars for security)
        PIIType.GITHUB_TOKEN: r'ghp_[A-Za-z0-9]{20,}',  # Personal access token (classic)
        PIIType.GITHUB_PAT: r'github_pat_[A-Za-z0-9_]{20,}',  # Fine-grained PAT
        PIIType.GITHUB_OAUTH: r'gh[ospru]_[A-Za-z0-9]{20,}',  # OAuth/User/System/Refresh tokens
        PIIType.PASSWORD: r'(?i)(password|passwd|pwd)[\s:=]+[^\s]{6,}',
    }

    # Context-aware patterns (lower confidence, need verification)
    CONTEXT_PATTERNS = {
        PIIType.DATE_OF_BIRTH: r'\b(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d\b',
    }

    def __init__(
        self,
        repo_root: Optional[Path] = None,
        config: Optional[PrivacyConfig] = None
    ):
        """
        Initialize PrivacyManager.

        Args:
            repo_root: Repository root directory
            config: Privacy configuration (uses defaults if not provided)
        """
        if repo_root is None:
            # Auto-detect repo root using utility
            try:
                repo_root = find_git_root()
            except ValueError:
                # Fallback to current directory if not in git repo
                repo_root = Path.cwd()

        self.repo_root = Path(repo_root)
        self.memory_context_dir = self.repo_root / "MEMORY-CONTEXT"
        self.config_path = self.memory_context_dir / "privacy.config.json"

        # Load or create configuration
        if config is None:
            self.config = self._load_or_create_config()
        else:
            self.config = config

        # Audit log
        self.audit_log_path = self.memory_context_dir / "archive" / "privacy_audit.log"

        logger.info(f"PrivacyManager initialized (level: {self.config.default_level.value})")

    def _load_or_create_config(self) -> PrivacyConfig:
        """Load existing config or create default."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                data = json.load(f)

            return PrivacyConfig(
                default_level=PrivacyLevel(data['default_level']),
                auto_redact=data['auto_redact'],
                pii_types_to_detect=[PIIType(t) for t in data['pii_types_to_detect']],
                redaction_char=data['redaction_char'],
                preserve_format=data['preserve_format'],
                audit_enabled=data['audit_enabled'],
                gdpr_mode=data['gdpr_mode']
            )
        else:
            # Create default config
            config = PrivacyConfig(
                default_level=PrivacyLevel.TEAM,
                auto_redact=True,
                pii_types_to_detect=[
                    PIIType.EMAIL,
                    PIIType.PHONE,
                    PIIType.SSN,
                    PIIType.CREDIT_CARD,
                    PIIType.IP_ADDRESS,
                    PIIType.API_KEY,
                    PIIType.AWS_KEY,
                    PIIType.GITHUB_TOKEN,
                    PIIType.GITHUB_PAT,
                    PIIType.GITHUB_OAUTH,
                    PIIType.PASSWORD
                ],
                redaction_char='*',
                preserve_format=True,
                audit_enabled=True,
                gdpr_mode=True
            )

            # Save default config
            self._save_config(config)
            return config

    def _save_config(self, config: PrivacyConfig) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)

        logger.info(f"Privacy config saved to {self.config_path}")

    def _log_audit(self, operation: str, details: Dict) -> None:
        """Log privacy operation to audit trail."""
        if not self.config.audit_enabled:
            return

        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc).isoformat()
        audit_entry = {
            'timestamp': timestamp,
            'operation': operation,
            'details': details
        }

        with open(self.audit_log_path, 'a') as f:
            f.write(json.dumps(audit_entry) + '\n')

    def detect_pii(
        self,
        text: str,
        pii_types: Optional[List[PIIType]] = None
    ) -> List[PIIDetection]:
        """
        Detect PII in text.

        Args:
            text: Text to scan for PII
            pii_types: Specific PII types to detect (all if None)

        Returns:
            List of detected PII instances
        """
        if pii_types is None:
            pii_types = self.config.pii_types_to_detect

        detections = []

        for pii_type in pii_types:
            # Use high-confidence patterns
            if pii_type in self.PII_PATTERNS:
                pattern = self.PII_PATTERNS[pii_type]
                for match in re.finditer(pattern, text):
                    # Extract context (50 chars before/after)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]

                    detections.append(PIIDetection(
                        pii_type=pii_type,
                        value=match.group(0),
                        start=match.start(),
                        end=match.end(),
                        confidence=0.95,  # High confidence for regex matches
                        context=context
                    ))

            # Use context-aware patterns (lower confidence)
            elif pii_type in self.CONTEXT_PATTERNS:
                pattern = self.CONTEXT_PATTERNS[pii_type]
                for match in re.finditer(pattern, text):
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]

                    detections.append(PIIDetection(
                        pii_type=pii_type,
                        value=match.group(0),
                        start=match.start(),
                        end=match.end(),
                        confidence=0.7,  # Lower confidence, may need verification
                        context=context
                    ))

        # Log audit trail
        if detections:
            self._log_audit('pii_detected', {
                'count': len(detections),
                'types': list(set(d.pii_type.value for d in detections)),
                'text_length': len(text)
            })

        logger.info(f"Detected {len(detections)} PII instances")
        return detections

    def redact(
        self,
        text: str,
        level: PrivacyLevel,
        detections: Optional[List[PIIDetection]] = None
    ) -> str:
        """
        Redact PII based on privacy level.

        Args:
            text: Text to redact
            level: Target privacy level
            detections: Pre-detected PII (will auto-detect if None)

        Returns:
            Redacted text
        """
        # Detect PII if not provided
        if detections is None:
            detections = self.detect_pii(text)

        # Determine which PII types to redact based on level
        redact_types = self._get_redact_types_for_level(level)

        # Sort detections by position (reverse order for string replacement)
        sorted_detections = sorted(detections, key=lambda d: d.start, reverse=True)

        redacted_text = text
        redaction_count = 0

        for detection in sorted_detections:
            if detection.pii_type in redact_types:
                # Redact this PII
                if self.config.preserve_format:
                    # Preserve format (e.g., xxx-xxx-1234)
                    redacted_value = self._preserve_format_redaction(detection.value)
                else:
                    # Simple placeholder
                    redacted_value = f"[{detection.pii_type.value.upper()}_REDACTED]"

                redacted_text = (
                    redacted_text[:detection.start] +
                    redacted_value +
                    redacted_text[detection.end:]
                )
                redaction_count += 1

        # Log audit trail
        if redaction_count > 0:
            self._log_audit('pii_redacted', {
                'level': level.value,
                'redaction_count': redaction_count,
                'text_length_before': len(text),
                'text_length_after': len(redacted_text)
            })

        logger.info(f"Redacted {redaction_count} PII instances for level {level.value}")
        return redacted_text

    def _get_redact_types_for_level(self, level: PrivacyLevel) -> Set[PIIType]:
        """Get PII types to redact for given privacy level."""
        if level == PrivacyLevel.PUBLIC:
            # Redact everything except generic info
            return {
                PIIType.EMAIL,
                PIIType.PHONE,
                PIIType.SSN,
                PIIType.CREDIT_CARD,
                PIIType.IP_ADDRESS,
                PIIType.API_KEY,
                PIIType.AWS_KEY,
                PIIType.GITHUB_TOKEN,
                PIIType.GITHUB_PAT,
                PIIType.GITHUB_OAUTH,
                PIIType.PASSWORD,
                PIIType.NAME,
                PIIType.ADDRESS,
                PIIType.DATE_OF_BIRTH
            }
        elif level == PrivacyLevel.TEAM:
            # Redact sensitive data only
            return {
                PIIType.SSN,
                PIIType.CREDIT_CARD,
                PIIType.PASSWORD,
                PIIType.API_KEY,
                PIIType.AWS_KEY,
                PIIType.GITHUB_TOKEN,
                PIIType.GITHUB_PAT,
                PIIType.GITHUB_OAUTH
            }
        else:
            # PRIVATE and EPHEMERAL - only redact credentials (CRITICAL FIX)
            # Always redact passwords and API keys regardless of privacy level
            return {
                PIIType.PASSWORD,
                PIIType.API_KEY,
                PIIType.AWS_KEY,
                PIIType.GITHUB_TOKEN,
                PIIType.GITHUB_PAT,
                PIIType.GITHUB_OAUTH,
                PIIType.CREDIT_CARD  # Always redact credit cards too
            }

    def _preserve_format_redaction(self, value: str) -> str:
        """
        Redact while preserving format.

        Examples:
            555-123-4567 → ***-***-4567
            john@example.com → j***@example.com
            4532-1234-5678-9012 → ****-****-****-9012
        """
        # Email: preserve domain, redact local part
        if '@' in value:
            local, domain = value.split('@', 1)
            if len(local) > 1:
                return local[0] + ('*' * (len(local) - 1)) + '@' + domain
            else:
                return '*@' + domain

        # Phone/SSN/Credit Card: preserve last 4 digits
        digits = re.findall(r'\d', value)
        if len(digits) >= 4:
            # Preserve structure but redact most digits
            redacted = value
            digit_count = 0
            for i, char in enumerate(value):
                if char.isdigit():
                    digit_count += 1
                    # Redact all but last 4 digits
                    if digit_count <= len(digits) - 4:
                        redacted = redacted[:i] + '*' + redacted[i+1:]
            return redacted

        # Default: full redaction
        return '*' * len(value)

    def is_safe_for_level(
        self,
        text: str,
        level: PrivacyLevel,
        threshold: float = 0.8
    ) -> bool:
        """
        Check if text is safe for given privacy level.

        Args:
            text: Text to check
            level: Target privacy level
            threshold: Confidence threshold for PII detection

        Returns:
            True if safe, False if contains PII for this level
        """
        detections = self.detect_pii(text)
        redact_types = self._get_redact_types_for_level(level)

        # Check if any high-confidence PII needs redaction
        for detection in detections:
            if detection.pii_type in redact_types and detection.confidence >= threshold:
                return False

        return True

    def get_privacy_summary(self, text: str) -> Dict:
        """
        Get privacy analysis summary for text.

        Returns:
            Dictionary with privacy metrics
        """
        detections = self.detect_pii(text)

        pii_by_type = {}
        for detection in detections:
            pii_type = detection.pii_type.value
            if pii_type not in pii_by_type:
                pii_by_type[pii_type] = 0
            pii_by_type[pii_type] += 1

        # Determine safest privacy level
        if not detections:
            safest_level = PrivacyLevel.PUBLIC
        elif all(d.pii_type not in self._get_redact_types_for_level(PrivacyLevel.TEAM) for d in detections):
            safest_level = PrivacyLevel.TEAM
        else:
            safest_level = PrivacyLevel.PRIVATE

        return {
            'total_pii_found': len(detections),
            'pii_by_type': pii_by_type,
            'safest_level': safest_level.value,
            'safe_for_public': safest_level == PrivacyLevel.PUBLIC,
            'safe_for_team': safest_level in [PrivacyLevel.PUBLIC, PrivacyLevel.TEAM],
            'text_length': len(text)
        }


def main():
    """CLI entry point for testing."""
    import argparse

    parser = argparse.ArgumentParser(
        description='CODITECT Privacy Control Manager - PII detection and redaction'
    )

    parser.add_argument(
        '--text',
        type=str,
        help='Text to analyze'
    )

    parser.add_argument(
        '--file',
        type=str,
        help='File to analyze'
    )

    parser.add_argument(
        '--level',
        type=str,
        choices=['public', 'team', 'private', 'ephemeral'],
        default='team',
        help='Privacy level for redaction'
    )

    parser.add_argument(
        '--detect-only',
        action='store_true',
        help='Only detect PII, do not redact'
    )

    args = parser.parse_args()

    # Get text to analyze
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Error: Provide --text or --file")
        return 1

    # Initialize privacy manager
    pm = PrivacyManager()

    # Detect PII
    print("\n" + "="*80)
    print("PRIVACY ANALYSIS")
    print("="*80)

    summary = pm.get_privacy_summary(text)
    print(f"\nTotal PII found: {summary['total_pii_found']}")
    print(f"Safest privacy level: {summary['safest_level'].upper()}")
    print(f"\nPII by type:")
    for pii_type, count in summary['pii_by_type'].items():
        print(f"  - {pii_type}: {count}")

    if not args.detect_only:
        # Redact
        level = PrivacyLevel(args.level)
        redacted_text = pm.redact(text, level)

        print("\n" + "="*80)
        print(f"REDACTED TEXT (Level: {level.value.upper()})")
        print("="*80)
        print(redacted_text)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
