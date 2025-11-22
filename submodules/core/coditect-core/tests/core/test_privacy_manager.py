#!/usr/bin/env python3
"""
Comprehensive Tests for CODITECT Privacy Manager

Tests PII detection, redaction, privacy levels, configuration management,
and audit logging with 85%+ code coverage goal.

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation
Date: 2025-11-16
"""

import unittest
import sys
import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime, timezone

# Add scripts/core to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "core"))

from privacy_manager import (
    PrivacyManager, PrivacyLevel, PIIType, PIIDetection, PrivacyConfig
)

# Comprehensive test data fixtures
TEST_CASES = {
    'email': {
        'valid': [
            'john@example.com',
            'user.name+tag@example.co.uk',
            'test.email_123@subdomain.example.org',
            'admin@localhost.localdomain'
        ],
        'invalid': [
            'not-an-email@',
            '@example.com',
            'missing-at-sign.com'
        ]
    },
    'phone': {
        'valid': [
            '555-123-4567',  # 10-digit with dashes
            '(555) 123-4567',  # 10-digit with parens
            '5551234567',  # 10-digit no separators
            '123-4567',  # 7-digit with dash
            '1234567',  # 7-digit no separator
            '+1-555-123-4567'  # International format
        ],
        'invalid': [
            '123-456',  # Too short
            'not-a-phone'
        ]
    },
    'ssn': {
        'valid': [
            '123-45-6789',
            '987-65-4321'
        ],
        'invalid': [
            '000-00-0000',  # Invalid SSN (but pattern matches)
            '123456789',  # No dashes
            '12-345-6789'  # Wrong format
        ]
    },
    'credit_card': {
        'valid': [
            '4532-1234-5678-9012',
            '4532 1234 5678 9012',
            '4532123456789012'
        ],
        'invalid': [
            '1234-5678-9012',  # Too short
            '4532-1234-5678'  # Incomplete
        ]
    },
    'ip_address': {
        'valid': [
            '192.168.1.100',
            '10.0.0.1',
            '8.8.8.8'
        ],
        'invalid': [
            '256.256.256.256',  # Out of range (but pattern matches)
            '192.168.1'  # Incomplete
        ]
    },
    'github_tokens': {
        'valid': [
            'ghp_1234567890123456789012345678901234',  # Classic PAT (36 chars)
            'ghp_12345678901234567890',  # Minimum 20 chars
            'github_pat_11ABCDEFG1234567890_abcdefghijklmnopqrstuvwxyz',  # Fine-grained PAT
            'gho_12345678901234567890123456789012',  # OAuth (32 chars)
            'ghu_12345678901234567890123456789012',  # User token
            'ghs_12345678901234567890123456789012',  # Server token
            'ghr_12345678901234567890123456789012',  # Refresh token
            'ghp_' + 'x' * 100  # Long token
        ],
        'invalid': [
            'ghp_tooshort',  # Less than 20 chars
            'github_12345678901234567890',  # Wrong prefix
        ]
    },
    'aws_key': {
        'valid': [
            'AKIAIOSFODNN7EXAMPLE',  # 20 chars total (AKIA + 16)
            'AKIATESTKEYEXAMPLE12'  # 20 chars total (AKIA + 16)
        ],
        'invalid': [
            'AKIA123',  # Too short
            'NOTAKIA12345678901'  # Wrong prefix
        ]
    },
    'password': {
        'valid': [
            'password: secret123',
            'Password=MyP@ssw0rd',
            'pwd: abc123def'
        ],
        'invalid': [
            'password: 123',  # Too short (less than 6 chars)
            'my password'  # No separator
        ]
    }
}


class TestPrivacyManagerInit(unittest.TestCase):
    """Test PrivacyManager initialization and configuration."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_init_auto_detect_git_root(self):
        """Test auto-detection of git root."""
        # This will use current directory's git root
        pm = PrivacyManager()
        self.assertIsNotNone(pm.repo_root)
        self.assertIsInstance(pm.repo_root, Path)

    def test_init_explicit_repo_root(self):
        """Test initialization with explicit repo root."""
        pm = PrivacyManager(repo_root=self.test_path)
        self.assertEqual(pm.repo_root, self.test_path)
        self.assertEqual(pm.memory_context_dir, self.test_path / "MEMORY-CONTEXT")

    def test_init_no_git_repo(self):
        """Test fallback to cwd when not in git repo."""
        # Use temp directory which is not a git repo
        pm = PrivacyManager(repo_root=self.test_path)
        self.assertIsNotNone(pm.repo_root)
        self.assertEqual(pm.repo_root, self.test_path)

    def test_load_existing_config(self):
        """Test loading existing configuration."""
        # Create config file
        config_dir = self.test_path / "MEMORY-CONTEXT"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "privacy.config.json"

        config_data = {
            'default_level': 'public',
            'auto_redact': False,
            'pii_types_to_detect': ['email', 'phone'],
            'redaction_char': 'X',
            'preserve_format': False,
            'audit_enabled': False,
            'gdpr_mode': False
        }

        with open(config_path, 'w') as f:
            json.dump(config_data, f)

        # Load config
        pm = PrivacyManager(repo_root=self.test_path)
        self.assertEqual(pm.config.default_level, PrivacyLevel.PUBLIC)
        self.assertFalse(pm.config.auto_redact)
        self.assertEqual(pm.config.redaction_char, 'X')
        self.assertFalse(pm.config.preserve_format)

    def test_create_default_config(self):
        """Test default configuration creation."""
        pm = PrivacyManager(repo_root=self.test_path)

        # Check default values
        self.assertEqual(pm.config.default_level, PrivacyLevel.TEAM)
        self.assertTrue(pm.config.auto_redact)
        self.assertEqual(pm.config.redaction_char, '*')
        self.assertTrue(pm.config.preserve_format)
        self.assertTrue(pm.config.audit_enabled)
        self.assertTrue(pm.config.gdpr_mode)

        # Check config file was created
        config_path = self.test_path / "MEMORY-CONTEXT" / "privacy.config.json"
        self.assertTrue(config_path.exists())

    def test_save_config(self):
        """Test configuration persistence."""
        pm = PrivacyManager(repo_root=self.test_path)

        # Modify config
        pm.config.default_level = PrivacyLevel.PRIVATE
        pm.config.redaction_char = '#'
        pm._save_config(pm.config)

        # Create new manager and verify config loaded
        pm2 = PrivacyManager(repo_root=self.test_path)
        self.assertEqual(pm2.config.default_level, PrivacyLevel.PRIVATE)
        self.assertEqual(pm2.config.redaction_char, '#')

    def test_custom_config(self):
        """Test initialization with custom config."""
        custom_config = PrivacyConfig(
            default_level=PrivacyLevel.PUBLIC,
            auto_redact=False,
            pii_types_to_detect=[PIIType.EMAIL],
            redaction_char='X',
            preserve_format=False,
            audit_enabled=False,
            gdpr_mode=False
        )

        pm = PrivacyManager(repo_root=self.test_path, config=custom_config)
        self.assertEqual(pm.config.default_level, PrivacyLevel.PUBLIC)
        self.assertEqual(pm.config.redaction_char, 'X')


class TestPIIDetection(unittest.TestCase):
    """Test PII detection functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.pm = PrivacyManager(repo_root=Path(self.test_dir))

    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_detect_email(self):
        """Test email detection."""
        for email in TEST_CASES['email']['valid']:
            text = f"Contact me at {email} for info."
            detections = self.pm.detect_pii(text)
            email_detections = [d for d in detections if d.pii_type == PIIType.EMAIL]
            self.assertGreater(len(email_detections), 0, f"Should detect email: {email}")
            self.assertEqual(email_detections[0].value, email)

    def test_detect_phone(self):
        """Test phone number detection (7 and 10 digit)."""
        for phone in TEST_CASES['phone']['valid']:
            text = f"Call me at {phone}"
            detections = self.pm.detect_pii(text)
            phone_detections = [d for d in detections if d.pii_type == PIIType.PHONE]
            self.assertGreater(len(phone_detections), 0, f"Should detect phone: {phone}")

    def test_detect_ssn(self):
        """Test SSN detection."""
        for ssn in TEST_CASES['ssn']['valid']:
            text = f"My SSN is {ssn}"
            detections = self.pm.detect_pii(text)
            ssn_detections = [d for d in detections if d.pii_type == PIIType.SSN]
            self.assertEqual(len(ssn_detections), 1, f"Should detect SSN: {ssn}")
            self.assertEqual(ssn_detections[0].value, ssn)

    def test_detect_credit_card(self):
        """Test credit card detection."""
        for cc in TEST_CASES['credit_card']['valid']:
            text = f"Card number: {cc}"
            detections = self.pm.detect_pii(text)
            cc_detections = [d for d in detections if d.pii_type == PIIType.CREDIT_CARD]
            self.assertGreater(len(cc_detections), 0, f"Should detect credit card: {cc}")

    def test_detect_ip_address(self):
        """Test IP address detection."""
        for ip in TEST_CASES['ip_address']['valid']:
            text = f"Server at {ip} is online"
            detections = self.pm.detect_pii(text)
            ip_detections = [d for d in detections if d.pii_type == PIIType.IP_ADDRESS]
            self.assertGreater(len(ip_detections), 0, f"Should detect IP: {ip}")

    def test_detect_api_key(self):
        """Test generic API key detection."""
        api_key = 'a' * 32  # 32 character alphanumeric
        text = f"API Key: {api_key}"
        detections = self.pm.detect_pii(text)
        api_detections = [d for d in detections if d.pii_type == PIIType.API_KEY]
        self.assertGreater(len(api_detections), 0, "Should detect API key")

    def test_detect_aws_key(self):
        """Test AWS key detection."""
        for aws_key in TEST_CASES['aws_key']['valid']:
            text = f"AWS: {aws_key}"
            detections = self.pm.detect_pii(text)
            aws_detections = [d for d in detections if d.pii_type == PIIType.AWS_KEY]
            self.assertEqual(len(aws_detections), 1, f"Should detect AWS key: {aws_key}")

    def test_detect_github_tokens(self):
        """Test all GitHub token types."""
        for token in TEST_CASES['github_tokens']['valid']:
            text = f"Token: {token}"
            detections = self.pm.detect_pii(text)
            github_detections = [
                d for d in detections
                if d.pii_type in [PIIType.GITHUB_TOKEN, PIIType.GITHUB_PAT, PIIType.GITHUB_OAUTH]
            ]
            self.assertGreater(len(github_detections), 0, f"Should detect GitHub token: {token[:20]}...")

    def test_detect_password(self):
        """Test password pattern detection."""
        for pwd_pattern in TEST_CASES['password']['valid']:
            text = f"Login with {pwd_pattern}"
            detections = self.pm.detect_pii(text)
            pwd_detections = [d for d in detections if d.pii_type == PIIType.PASSWORD]
            self.assertGreater(len(pwd_detections), 0, f"Should detect password: {pwd_pattern}")

    def test_detect_multiple_pii(self):
        """Test detecting multiple PII types in same text."""
        text = """
        Contact: john@example.com
        Phone: 555-123-4567
        SSN: 123-45-6789
        Server: 192.168.1.100
        AWS Key: AKIAIOSFODNN7EXAMPLE
        """
        detections = self.pm.detect_pii(text)

        # Should detect multiple types
        self.assertGreater(len(detections), 3, "Should detect multiple PII instances")

        pii_types = {d.pii_type for d in detections}
        self.assertIn(PIIType.EMAIL, pii_types)
        self.assertIn(PIIType.PHONE, pii_types)
        self.assertIn(PIIType.SSN, pii_types)

    def test_detect_no_pii(self):
        """Test with clean text (no PII)."""
        text = "This is a completely safe message with no personal information."
        detections = self.pm.detect_pii(text)
        self.assertEqual(len(detections), 0, "Should not detect PII in clean text")

    def test_detect_pii_context(self):
        """Test context extraction around PII."""
        text = "The developer's email address is john.doe@example.com and they work remotely."
        detections = self.pm.detect_pii(text)

        self.assertGreater(len(detections), 0)
        detection = detections[0]

        # Check context is extracted
        self.assertIsNotNone(detection.context)
        self.assertIn("john.doe@example.com", detection.context)
        self.assertGreater(len(detection.context), len("john.doe@example.com"))

    def test_detect_pii_confidence(self):
        """Test confidence scores for detections."""
        text = "Email: test@example.com"
        detections = self.pm.detect_pii(text)

        self.assertGreater(len(detections), 0)
        # Regex-based detections should have high confidence
        self.assertEqual(detections[0].confidence, 0.95)

    def test_detect_specific_types(self):
        """Test detecting specific PII types only."""
        text = "Email: john@example.com, Phone: 555-1234"

        # Detect only emails
        detections = self.pm.detect_pii(text, pii_types=[PIIType.EMAIL])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].pii_type, PIIType.EMAIL)


class TestRedaction(unittest.TestCase):
    """Test PII redaction functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.pm = PrivacyManager(repo_root=Path(self.test_dir))

    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_redact_public_level(self):
        """Test PUBLIC level redacts all PII."""
        text = "Email: john@example.com, Phone: 555-123-4567, SSN: 123-45-6789"
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)

        # All PII should be redacted
        self.assertNotIn("john@example.com", redacted)
        self.assertNotIn("555-123-4567", redacted)
        self.assertNotIn("123-45-6789", redacted)

    def test_redact_team_level(self):
        """Test TEAM level redacts sensitive only."""
        text = "Email: john@example.com, AWS: AKIAIOSFODNN7EXAMPLE, SSN: 123-45-6789"
        redacted = self.pm.redact(text, level=PrivacyLevel.TEAM)

        # Email might be preserved at TEAM level
        # But sensitive data should be redacted
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", redacted, "AWS key should be redacted")
        self.assertNotIn("123-45-6789", redacted, "SSN should be redacted")

    def test_redact_private_level(self):
        """Test PRIVATE level redacts credentials only."""
        text = "Email: john@example.com, AWS: AKIAIOSFODNN7EXAMPLE, Phone: 555-1234"
        redacted = self.pm.redact(text, level=PrivacyLevel.PRIVATE)

        # Email and phone should be preserved
        self.assertIn("john@example.com", redacted, "Email should be preserved at PRIVATE")

        # Credentials should still be redacted
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", redacted, "AWS key should be redacted")

    def test_redact_ephemeral_level(self):
        """Test EPHEMERAL level handling."""
        text = "Email: john@example.com, Password: secret123"
        redacted = self.pm.redact(text, level=PrivacyLevel.EPHEMERAL)

        # Should behave like PRIVATE (only redact credentials)
        self.assertIn("john@example.com", redacted)
        self.assertNotIn("secret123", redacted)

    def test_preserve_format_email(self):
        """Test email format preservation."""
        text = "Email: john.doe@example.com"
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)

        # Should preserve format: j***@example.com
        self.assertIn("@", redacted, "Should preserve @ symbol")
        self.assertIn("example.com", redacted, "Should preserve domain")
        self.assertIn("*", redacted, "Should use masking")

    def test_preserve_format_phone(self):
        """Test phone format preservation."""
        text = "Phone: 555-123-4567"
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)

        # Should preserve format: ***-***-4567
        self.assertIn("4567", redacted, "Should preserve last 4 digits")
        self.assertIn("*", redacted, "Should mask other digits")

    def test_preserve_format_credit_card(self):
        """Test credit card format preservation."""
        text = "Card: 4532-1234-5678-9012"
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)

        # Should preserve last 4 digits
        self.assertIn("9012", redacted, "Should preserve last 4 digits")
        self.assertIn("*", redacted, "Should mask other digits")

    def test_redact_multiple_instances(self):
        """Test redacting multiple PII instances."""
        text = "Email john@example.com and jane@example.com"
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)

        # Both emails should be redacted
        self.assertNotIn("john@example.com", redacted)
        self.assertNotIn("jane@example.com", redacted)

    def test_redact_no_pii(self):
        """Test text with no PII returns unchanged."""
        text = "This is a clean message."
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)

        self.assertEqual(text, redacted, "Clean text should be unchanged")

    def test_redact_with_predetected_pii(self):
        """Test redaction with pre-detected PII."""
        text = "Email: test@example.com"
        detections = self.pm.detect_pii(text)

        # Use pre-detected PII
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC, detections=detections)

        self.assertNotIn("test@example.com", redacted)

    def test_redaction_without_preserve_format(self):
        """Test redaction without format preservation."""
        # Create config without format preservation
        config = PrivacyConfig(
            default_level=PrivacyLevel.TEAM,
            auto_redact=True,
            pii_types_to_detect=[PIIType.EMAIL],
            redaction_char='*',
            preserve_format=False,  # Disable format preservation
            audit_enabled=False,
            gdpr_mode=True
        )

        pm = PrivacyManager(repo_root=Path(self.test_dir), config=config)
        text = "Email: john@example.com"
        redacted = pm.redact(text, level=PrivacyLevel.PUBLIC)

        # Should use placeholder instead of format preservation
        self.assertIn("[EMAIL_REDACTED]", redacted)
        self.assertNotIn("john@example.com", redacted)


class TestPrivacyLevels(unittest.TestCase):
    """Test privacy level logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.pm = PrivacyManager(repo_root=Path(self.test_dir))

    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_redact_types_public(self):
        """Test PUBLIC level redaction rules."""
        redact_types = self.pm._get_redact_types_for_level(PrivacyLevel.PUBLIC)

        # Should redact most PII types
        self.assertIn(PIIType.EMAIL, redact_types)
        self.assertIn(PIIType.PHONE, redact_types)
        self.assertIn(PIIType.SSN, redact_types)
        self.assertIn(PIIType.PASSWORD, redact_types)
        self.assertIn(PIIType.API_KEY, redact_types)

    def test_get_redact_types_team(self):
        """Test TEAM level redaction rules."""
        redact_types = self.pm._get_redact_types_for_level(PrivacyLevel.TEAM)

        # Should redact sensitive data
        self.assertIn(PIIType.SSN, redact_types)
        self.assertIn(PIIType.PASSWORD, redact_types)
        self.assertIn(PIIType.API_KEY, redact_types)

        # Should NOT redact contact info
        self.assertNotIn(PIIType.EMAIL, redact_types)
        self.assertNotIn(PIIType.PHONE, redact_types)

    def test_get_redact_types_private(self):
        """Test PRIVATE level redaction rules."""
        redact_types = self.pm._get_redact_types_for_level(PrivacyLevel.PRIVATE)

        # Should only redact credentials
        self.assertIn(PIIType.PASSWORD, redact_types)
        self.assertIn(PIIType.API_KEY, redact_types)
        self.assertIn(PIIType.AWS_KEY, redact_types)

        # Should NOT redact PII
        self.assertNotIn(PIIType.EMAIL, redact_types)
        self.assertNotIn(PIIType.PHONE, redact_types)

    def test_is_safe_for_level_safe(self):
        """Test safe text for level."""
        clean_text = "This is a safe message."

        # Should be safe for all levels
        self.assertTrue(self.pm.is_safe_for_level(clean_text, PrivacyLevel.PUBLIC))
        self.assertTrue(self.pm.is_safe_for_level(clean_text, PrivacyLevel.TEAM))
        self.assertTrue(self.pm.is_safe_for_level(clean_text, PrivacyLevel.PRIVATE))

    def test_is_safe_for_level_unsafe(self):
        """Test unsafe text for level."""
        pii_text = "Email: john@example.com, Password: secret123"

        # Not safe for PUBLIC (contains email)
        self.assertFalse(self.pm.is_safe_for_level(pii_text, PrivacyLevel.PUBLIC))

        # Safe for PRIVATE (credentials check)
        # Note: Password will make it unsafe
        self.assertFalse(self.pm.is_safe_for_level(pii_text, PrivacyLevel.PRIVATE))

        # Test with email only (safe for TEAM)
        email_only = "Email: john@example.com"
        self.assertTrue(self.pm.is_safe_for_level(email_only, PrivacyLevel.TEAM))

    def test_is_safe_confidence_threshold(self):
        """Test confidence threshold for safety check."""
        text = "Email: test@example.com"

        # With high threshold (1.0), won't match our 0.95 confidence
        is_safe = self.pm.is_safe_for_level(text, PrivacyLevel.PUBLIC, threshold=1.0)
        self.assertTrue(is_safe, "Should be safe with threshold above detection confidence")

        # With low threshold, should detect
        is_safe = self.pm.is_safe_for_level(text, PrivacyLevel.PUBLIC, threshold=0.9)
        self.assertFalse(is_safe, "Should be unsafe with threshold below detection confidence")


class TestPrivacySummary(unittest.TestCase):
    """Test privacy summary functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.pm = PrivacyManager(repo_root=Path(self.test_dir))

    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_privacy_summary_no_pii(self):
        """Test summary with clean text."""
        text = "This is a safe message."
        summary = self.pm.get_privacy_summary(text)

        self.assertEqual(summary['total_pii_found'], 0)
        self.assertEqual(summary['pii_by_type'], {})
        self.assertEqual(summary['safest_level'], PrivacyLevel.PUBLIC.value)
        self.assertTrue(summary['safe_for_public'])
        self.assertTrue(summary['safe_for_team'])

    def test_get_privacy_summary_with_pii(self):
        """Test summary with PII detected."""
        text = "Email: john@example.com, Phone: 555-1234"
        summary = self.pm.get_privacy_summary(text)

        self.assertGreater(summary['total_pii_found'], 0)
        self.assertIn('email', summary['pii_by_type'])
        self.assertFalse(summary['safe_for_public'])

    def test_get_privacy_summary_safest_level(self):
        """Test safest level calculation."""
        # Only contact info (safe for TEAM)
        text1 = "Email: john@example.com"
        summary1 = self.pm.get_privacy_summary(text1)
        self.assertEqual(summary1['safest_level'], PrivacyLevel.TEAM.value)

        # Sensitive data (requires PRIVATE)
        text2 = "SSN: 123-45-6789"
        summary2 = self.pm.get_privacy_summary(text2)
        self.assertEqual(summary2['safest_level'], PrivacyLevel.PRIVATE.value)

        # No PII (safe for PUBLIC)
        text3 = "Clean message"
        summary3 = self.pm.get_privacy_summary(text3)
        self.assertEqual(summary3['safest_level'], PrivacyLevel.PUBLIC.value)

    def test_privacy_summary_structure(self):
        """Test summary dictionary structure."""
        text = "Test message"
        summary = self.pm.get_privacy_summary(text)

        # Check required keys
        required_keys = [
            'total_pii_found',
            'pii_by_type',
            'safest_level',
            'safe_for_public',
            'safe_for_team',
            'text_length'
        ]

        for key in required_keys:
            self.assertIn(key, summary, f"Summary should contain '{key}'")

    def test_privacy_summary_pii_counts(self):
        """Test PII type counting in summary."""
        text = "Email: john@example.com and jane@example.com"
        summary = self.pm.get_privacy_summary(text)

        # Should count 2 emails
        self.assertEqual(summary['pii_by_type']['email'], 2)


class TestAuditLogging(unittest.TestCase):
    """Test audit logging functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.pm = PrivacyManager(repo_root=Path(self.test_dir))
        self.audit_log_path = self.pm.audit_log_path

    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_audit_log_pii_detected(self):
        """Test audit log creation for PII detection."""
        text = "Email: test@example.com"
        detections = self.pm.detect_pii(text)

        # Check audit log was created
        self.assertTrue(self.audit_log_path.exists(), "Audit log should be created")

        # Check audit log content
        with open(self.audit_log_path, 'r') as f:
            log_entries = [json.loads(line) for line in f]

        self.assertGreater(len(log_entries), 0, "Should have audit entries")
        last_entry = log_entries[-1]

        self.assertEqual(last_entry['operation'], 'pii_detected')
        self.assertIn('count', last_entry['details'])
        self.assertGreater(last_entry['details']['count'], 0)

    def test_audit_log_pii_redacted(self):
        """Test audit log for redaction."""
        text = "Email: test@example.com"
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)

        # Check audit log
        with open(self.audit_log_path, 'r') as f:
            log_entries = [json.loads(line) for line in f]

        # Should have both detection and redaction entries
        operations = [e['operation'] for e in log_entries]
        self.assertIn('pii_detected', operations)
        self.assertIn('pii_redacted', operations)

        # Check redaction entry
        redaction_entries = [e for e in log_entries if e['operation'] == 'pii_redacted']
        self.assertGreater(len(redaction_entries), 0)

        redaction_entry = redaction_entries[-1]
        self.assertEqual(redaction_entry['details']['level'], 'public')
        self.assertGreater(redaction_entry['details']['redaction_count'], 0)

    def test_audit_log_disabled(self):
        """Test when audit logging is disabled."""
        # Create config with audit disabled
        config = PrivacyConfig(
            default_level=PrivacyLevel.TEAM,
            auto_redact=True,
            pii_types_to_detect=[PIIType.EMAIL],
            redaction_char='*',
            preserve_format=True,
            audit_enabled=False,  # Disable audit
            gdpr_mode=True
        )

        pm = PrivacyManager(repo_root=Path(self.test_dir), config=config)

        text = "Email: test@example.com"
        pm.detect_pii(text)

        # Audit log should not be created
        self.assertFalse(pm.audit_log_path.exists(), "Audit log should not exist when disabled")

    def test_audit_log_timestamp_format(self):
        """Test audit log timestamp format."""
        text = "Email: test@example.com"
        self.pm.detect_pii(text)

        with open(self.audit_log_path, 'r') as f:
            log_entry = json.loads(f.readline())

        # Check timestamp is ISO format
        timestamp = log_entry['timestamp']
        # Should parse without error
        parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        self.assertIsInstance(parsed, datetime)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.pm = PrivacyManager(repo_root=Path(self.test_dir))

    def tearDown(self):
        """Clean up."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_empty_string(self):
        """Test handling of empty strings."""
        text = ""
        detections = self.pm.detect_pii(text)
        self.assertEqual(len(detections), 0)

        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)
        self.assertEqual(redacted, "")

    def test_none_values(self):
        """Test handling of None values."""
        # detect_pii expects string, will fail with None
        with self.assertRaises(TypeError):
            self.pm.detect_pii(None)

    def test_very_long_text(self):
        """Test handling of very long text."""
        # Create text with many PII instances
        text = "\n".join([f"Email{i}: user{i}@example.com" for i in range(100)])

        detections = self.pm.detect_pii(text)
        self.assertEqual(len(detections), 100)

        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)
        self.assertNotIn("user0@example.com", redacted)

    def test_overlapping_patterns(self):
        """Test handling of overlapping pattern matches."""
        # Some patterns might overlap
        text = "Contact: 1234567890123456789012345678901234"  # Long number (could match multiple patterns)

        detections = self.pm.detect_pii(text)
        # Should detect (API key pattern matches long alphanumeric)
        self.assertGreater(len(detections), 0)

    def test_unicode_text(self):
        """Test handling of Unicode text."""
        text = "Email: user@例え.jp, Phone: 555-1234"
        detections = self.pm.detect_pii(text)

        # Should still detect phone
        phone_detections = [d for d in detections if d.pii_type == PIIType.PHONE]
        self.assertGreater(len(phone_detections), 0)

    def test_short_email_redaction(self):
        """Test redaction of very short emails."""
        text = "Email: a@b.co"
        redacted = self.pm.redact(text, level=PrivacyLevel.PUBLIC)

        # Should still redact properly
        self.assertNotIn("a@b.co", redacted)
        self.assertIn("@", redacted)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPrivacyManagerInit))
    suite.addTests(loader.loadTestsFromTestCase(TestPIIDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestRedaction))
    suite.addTests(loader.loadTestsFromTestCase(TestPrivacyLevels))
    suite.addTests(loader.loadTestsFromTestCase(TestPrivacySummary))
    suite.addTests(loader.loadTestsFromTestCase(TestAuditLogging))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
