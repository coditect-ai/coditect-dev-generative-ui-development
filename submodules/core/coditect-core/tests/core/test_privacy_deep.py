#!/usr/bin/env python3
"""
Deep Privacy Testing Suite

Comprehensive security testing for privacy manager.
Tests edge cases, bypass attempts, and real-world scenarios.

Author: AZ1.AI CODITECT Team
Date: 2025-11-16
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "core"))

from privacy_manager import PrivacyManager, PrivacyLevel, PIIType


def test_email_edge_cases():
    """Test email detection with various formats and edge cases."""
    pm = PrivacyManager()

    test_cases = [
        # Standard emails
        ("john@example.com", True, "Standard email"),
        ("john.doe@example.com", True, "Email with dot"),
        ("john+tag@example.com", True, "Email with plus tag"),
        ("john_doe@example.com", True, "Email with underscore"),

        # Edge cases
        ("john@subdomain.example.com", True, "Subdomain email"),
        ("john@example.co.uk", True, "Country code TLD"),
        ("a@b.co", True, "Minimal email"),

        # Should NOT match
        ("@example.com", False, "Missing local part"),
        ("john@", False, "Missing domain"),
        ("john@@example.com", False, "Double @"),
        ("not-an-email", False, "No @ symbol"),
    ]

    results = []
    for text, should_detect, description in test_cases:
        detections = pm.detect_pii(text)
        email_found = any(d.pii_type == PIIType.EMAIL for d in detections)

        status = "✅" if email_found == should_detect else "❌"
        results.append({
            'test': description,
            'input': text,
            'expected': should_detect,
            'actual': email_found,
            'status': status
        })

    return results


def test_credential_edge_cases():
    """Test credential detection with obfuscation attempts."""
    pm = PrivacyManager()

    test_cases = [
        # AWS Keys
        ("AKIAIOSFODNN7EXAMPLE", PIIType.AWS_KEY, True, "Standard AWS key"),
        ("AKIA1234567890ABCDEF", PIIType.AWS_KEY, True, "Valid AWS key format"),
        ("akia1234567890abcdef", PIIType.AWS_KEY, False, "Lowercase AWS key (invalid)"),
        ("AKIA123", PIIType.AWS_KEY, False, "Too short AWS key"),

        # GitHub Tokens
        ("ghp_1234567890abcdefghijklmnopqrstuvwxy", PIIType.GITHUB_TOKEN, True, "Valid GitHub token"),
        ("ghp_" + "a" * 35, PIIType.GITHUB_TOKEN, True, "Minimum length GitHub token"),
        ("ghp_" + "a" * 50, PIIType.GITHUB_TOKEN, True, "Longer GitHub token"),
        ("GHP_1234567890abcdefghijklmnopqrstuvwxy", PIIType.GITHUB_TOKEN, False, "Uppercase prefix"),
        ("ghp_123", PIIType.GITHUB_TOKEN, False, "Too short GitHub token"),

        # Generic API Keys (long alphanumeric)
        ("a" * 32, PIIType.API_KEY, True, "32 char API key"),
        ("a" * 64, PIIType.API_KEY, True, "64 char API key"),
        ("abc123def456ghi789jkl012mno345pq", PIIType.API_KEY, True, "Mixed alphanumeric API key"),
    ]

    results = []
    for text, expected_type, should_detect, description in test_cases:
        detections = pm.detect_pii(text)
        found = any(d.pii_type == expected_type for d in detections)

        status = "✅" if found == should_detect else "❌"
        results.append({
            'test': description,
            'input': text[:50] + "..." if len(text) > 50 else text,
            'expected_type': expected_type.value,
            'expected': should_detect,
            'actual': found,
            'status': status
        })

    return results


def test_phone_edge_cases():
    """Test phone number detection variations."""
    pm = PrivacyManager()

    test_cases = [
        # Valid formats
        ("555-1234", True, "7-digit phone"),
        ("555-123-4567", True, "10-digit with dashes"),
        ("(555) 123-4567", True, "10-digit with parens"),
        ("5551234567", True, "10-digit no formatting"),
        ("+1-555-123-4567", True, "International format"),
        ("1-555-123-4567", True, "With country code"),

        # Edge cases
        ("555.123.4567", True, "Dots as separator"),
        ("(555)123-4567", True, "No space after parens"),

        # Should NOT match
        ("123-45-6789", False, "SSN format, not phone"),
        ("555-12345", False, "Wrong digit count"),
        ("55-1234", False, "Too few digits"),
    ]

    results = []
    for text, should_detect, description in test_cases:
        detections = pm.detect_pii(text)
        phone_found = any(d.pii_type == PIIType.PHONE for d in detections)

        status = "✅" if phone_found == should_detect else "❌"
        results.append({
            'test': description,
            'input': text,
            'expected': should_detect,
            'actual': phone_found,
            'status': status
        })

    return results


def test_credential_redaction_at_all_levels():
    """CRITICAL: Verify credentials are ALWAYS redacted at ALL privacy levels."""
    pm = PrivacyManager()

    # Realistic scenario with multiple PII types
    sensitive_text = """
    Development Environment Setup:
    - Email: developer@company.com
    - Phone: 555-123-4567
    - Server: 192.168.1.100
    - AWS Access Key: AKIAIOSFODNN7EXAMPLE
    - GitHub Token: ghp_1234567890abcdefghijklmnopqrstuvwxy
    - Database Password: MySecretPass123!
    - Credit Card (test): 4532-1234-5678-9012
    """

    levels = [
        (PrivacyLevel.PUBLIC, "PUBLIC"),
        (PrivacyLevel.TEAM, "TEAM"),
        (PrivacyLevel.PRIVATE, "PRIVATE"),
        (PrivacyLevel.EPHEMERAL, "EPHEMERAL"),
    ]

    results = []

    # Critical credentials that should NEVER appear in ANY redacted output
    critical_credentials = [
        "AKIAIOSFODNN7EXAMPLE",
        "ghp_1234567890abcdefghijklmnopqrstuvwxy",
        "MySecretPass123!",
        "4532-1234-5678-9012"
    ]

    for level, level_name in levels:
        redacted = pm.redact(sensitive_text, level=level)

        for credential in critical_credentials:
            leaked = credential in redacted

            status = "❌ CRITICAL LEAK!" if leaked else "✅ SECURE"
            results.append({
                'level': level_name,
                'credential_type': 'AWS Key' if 'AKIA' in credential else
                                  'GitHub Token' if 'ghp_' in credential else
                                  'Password' if 'Pass' in credential else
                                  'Credit Card',
                'leaked': leaked,
                'status': status
            })

    return results


def test_redaction_bypass_attempts():
    """Test various attempts to bypass redaction."""
    pm = PrivacyManager()

    test_cases = [
        # Spacing tricks
        ("my email is john @ example.com", "Spaced email"),
        ("AWS key: AKIA IOSFODNN7EXAMPLE", "Spaced AWS key"),

        # Character substitution
        ("john[at]example[dot]com", "Substituted email"),
        ("john(at)example.com", "Parentheses substitution"),

        # Zero-width characters (Unicode trickery)
        ("john@exam\u200Bple.com", "Zero-width space in email"),

        # Partial obfuscation
        ("john@ex*mple.com", "Asterisk in domain"),
        ("j*hn@example.com", "Asterisk in local part"),

        # Case variations
        ("JOHN@EXAMPLE.COM", "Uppercase email"),
        ("JoHn@ExAmPlE.cOm", "Mixed case email"),
    ]

    results = []
    for text, description in test_cases:
        detections = pm.detect_pii(text)
        detected = len(detections) > 0

        # For bypass attempts, we want to know if we detected it or if it bypassed
        status = "✅ DETECTED" if detected else "⚠️ BYPASSED"
        results.append({
            'test': description,
            'input': text,
            'detected': detected,
            'status': status
        })

    return results


def test_realistic_checkpoint_scenario():
    """Test with realistic checkpoint content."""
    pm = PrivacyManager()

    checkpoint_content = """
# Sprint Checkpoint 2025-11-16

## Team
- Lead: Alice Johnson (alice@company.com, 555-123-4567)
- Developer: Bob Smith (bob.smith@company.com)
- DevOps: Carol White (carol@company.com, ext. 555-7890)

## Infrastructure
- Production Server: 10.0.1.50
- Staging Server: 10.0.1.51
- Database: db.internal.company.com

## Credentials Updated
- AWS Access Key: AKIAIOSFODNN7EXAMPLE (rotated)
- GitHub Deploy Token: ghp_abcdefghijklmnopqrstuvwxyz12345
- API Key: sk-proj-abc123def456ghi789jkl012mno345pq678rst

## Completed
- Fixed bug in payment processing
- Test credit card: 4532-1234-5678-9012
- Deployed to production
    """

    # Test at each privacy level
    results = {}

    for level in [PrivacyLevel.PUBLIC, PrivacyLevel.TEAM, PrivacyLevel.PRIVATE]:
        redacted = pm.redact(checkpoint_content, level=level)

        # Check for leaks
        leaks = {
            'emails': sum(1 for email in ['alice@company.com', 'bob.smith@company.com', 'carol@company.com']
                         if email in redacted),
            'aws_key': 'AKIAIOSFODNN7EXAMPLE' in redacted,
            'github_token': 'ghp_abcdefghijklmnopqrstuvwxyz12345' in redacted,
            'credit_card': '4532-1234-5678-9012' in redacted,
            'api_key': 'sk-proj-abc123def456ghi789jkl012mno345pq678rst' in redacted,
        }

        results[level.value] = {
            'redacted_length': len(redacted),
            'original_length': len(checkpoint_content),
            'leaks': leaks,
            'has_critical_leak': leaks['aws_key'] or leaks['github_token'] or leaks['credit_card']
        }

    return results


def run_deep_tests():
    """Run all deep privacy tests."""
    print("="*80)
    print("COMPREHENSIVE PRIVACY SECURITY TESTING")
    print("="*80)
    print()

    # Test 1: Email edge cases
    print("TEST 1: Email Detection Edge Cases")
    print("-" * 80)
    email_results = test_email_edge_cases()
    for r in email_results:
        print(f"{r['status']} {r['test']:40s} | Input: {r['input']:30s} | Expected: {r['expected']}, Got: {r['actual']}")

    email_pass = sum(1 for r in email_results if r['status'] == '✅')
    email_total = len(email_results)
    print(f"\nEmail Tests: {email_pass}/{email_total} passing")
    print()

    # Test 2: Credential edge cases
    print("TEST 2: Credential Detection Edge Cases")
    print("-" * 80)
    cred_results = test_credential_edge_cases()
    for r in cred_results:
        print(f"{r['status']} {r['test']:40s} | Type: {r['expected_type']:15s} | Expected: {r['expected']}, Got: {r['actual']}")

    cred_pass = sum(1 for r in cred_results if r['status'] == '✅')
    cred_total = len(cred_results)
    print(f"\nCredential Tests: {cred_pass}/{cred_total} passing")
    print()

    # Test 3: Phone edge cases
    print("TEST 3: Phone Number Detection Edge Cases")
    print("-" * 80)
    phone_results = test_phone_edge_cases()
    for r in phone_results:
        print(f"{r['status']} {r['test']:40s} | Input: {r['input']:20s} | Expected: {r['expected']}, Got: {r['actual']}")

    phone_pass = sum(1 for r in phone_results if r['status'] == '✅')
    phone_total = len(phone_results)
    print(f"\nPhone Tests: {phone_pass}/{phone_total} passing")
    print()

    # Test 4: CRITICAL - Credential redaction at all levels
    print("TEST 4: CRITICAL - Credential Redaction at ALL Privacy Levels")
    print("-" * 80)
    redaction_results = test_credential_redaction_at_all_levels()

    critical_leaks = 0
    for r in redaction_results:
        print(f"{r['status']} {r['level']:12s} | {r['credential_type']:15s} | Leaked: {r['leaked']}")
        if r['leaked']:
            critical_leaks += 1

    print(f"\nCritical Leaks Found: {critical_leaks}")
    if critical_leaks > 0:
        print("❌ SECURITY VULNERABILITY DETECTED!")
    else:
        print("✅ All credentials properly redacted at all levels")
    print()

    # Test 5: Bypass attempts
    print("TEST 5: Redaction Bypass Attempts")
    print("-" * 80)
    bypass_results = test_redaction_bypass_attempts()
    for r in bypass_results:
        print(f"{r['status']} {r['test']:40s} | Detected: {r['detected']}")

    bypasses = sum(1 for r in bypass_results if r['status'] == '⚠️ BYPASSED')
    print(f"\nBypass Attempts: {bypasses} succeeded (lower is better)")
    print()

    # Test 6: Realistic scenario
    print("TEST 6: Realistic Checkpoint Content")
    print("-" * 80)
    scenario_results = test_realistic_checkpoint_scenario()

    for level, data in scenario_results.items():
        print(f"\nLevel: {level.upper()}")
        print(f"  Reduction: {data['original_length']} → {data['redacted_length']} bytes")
        print(f"  Leaks detected:")
        for leak_type, leaked in data['leaks'].items():
            status = "❌" if leaked else "✅"
            print(f"    {status} {leak_type}: {leaked}")

        if data['has_critical_leak']:
            print(f"  ❌ CRITICAL LEAK DETECTED!")
        else:
            print(f"  ✅ No critical leaks")

    # Summary
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)

    total_tests = email_total + cred_total + phone_total
    total_pass = email_pass + cred_pass + phone_pass

    print(f"Detection Tests: {total_pass}/{total_tests} passing ({100*total_pass//total_tests}%)")
    print(f"Critical Leaks: {critical_leaks} (MUST be 0)")
    print(f"Bypass Attempts: {bypasses} succeeded (known limitations)")

    if critical_leaks == 0 and total_pass == total_tests:
        print("\n✅ PRIVACY MANAGER: PRODUCTION READY")
        return True
    else:
        print("\n❌ PRIVACY MANAGER: HAS ISSUES - NOT PRODUCTION READY")
        return False


if __name__ == '__main__':
    success = run_deep_tests()
    sys.exit(0 if success else 1)
