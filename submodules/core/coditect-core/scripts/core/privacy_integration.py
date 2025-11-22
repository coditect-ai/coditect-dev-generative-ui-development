#!/usr/bin/env python3
"""
CODITECT Privacy Integration Layer

Integrates privacy_manager.py with checkpoint and export workflows.
Provides seamless privacy-aware content processing.

Usage:
    from privacy_integration import process_checkpoint_with_privacy, process_export_with_privacy

    # Process checkpoint
    safe_content = process_checkpoint_with_privacy(checkpoint_content, privacy_level="private")

    # Process export
    safe_content = process_export_with_privacy(export_content, privacy_level="team")

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation
Date: 2025-11-16
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime, timezone

# Add parent directory to path to import privacy_manager
sys.path.insert(0, str(Path(__file__).parent))

try:
    from privacy_manager import PrivacyManager, PrivacyLevel, PIIDetection
except ImportError:
    print("ERROR: Cannot import privacy_manager.py")
    print("Make sure privacy_manager.py is in the same directory")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PrivacyIntegration:
    """Integrates privacy controls with CODITECT workflows."""

    def __init__(self, repo_root: Optional[Path] = None):
        """
        Initialize privacy integration.

        Args:
            repo_root: Repository root directory
        """
        if repo_root is None:
            # Try to find repo root
            current = Path.cwd()
            while current != current.parent:
                if (current / ".git").exists():
                    repo_root = current
                    break
                current = current.parent

            if repo_root is None:
                repo_root = Path.cwd()

        self.repo_root = Path(repo_root)
        self.memory_context_dir = self.repo_root / "MEMORY-CONTEXT"
        self.audit_dir = self.memory_context_dir / "audit"
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        # Initialize privacy manager
        self.privacy_manager = PrivacyManager(repo_root=self.repo_root)

        logger.info(f"Privacy integration initialized for: {self.repo_root}")

    def process_content(
        self,
        content: str,
        content_type: str,
        privacy_level: str = "private",
        detect_only: bool = False
    ) -> Tuple[str, Dict]:
        """
        Process content with privacy controls.

        Args:
            content: Content to process
            content_type: Type of content (checkpoint, export, session)
            privacy_level: Privacy level to apply
            detect_only: Only detect PII, don't redact

        Returns:
            Tuple of (processed_content, privacy_report)
        """
        # Convert string privacy level to enum
        try:
            level = PrivacyLevel(privacy_level.lower())
        except ValueError:
            logger.warning(f"Invalid privacy level '{privacy_level}', using PRIVATE")
            level = PrivacyLevel.PRIVATE

        # Detect PII
        detections = self.privacy_manager.detect_pii(content)

        # Build privacy report
        report = {
            'content_type': content_type,
            'privacy_level': level.value,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'pii_detections': len(detections),
            'detection_types': {},
            'redacted': not detect_only
        }

        # Count detection types
        for detection in detections:
            pii_type = detection.pii_type.value
            report['detection_types'][pii_type] = report['detection_types'].get(pii_type, 0) + 1

        # Log detections
        if detections:
            logger.info(f"Found {len(detections)} PII instances in {content_type}")
            for pii_type, count in report['detection_types'].items():
                logger.info(f"  - {pii_type}: {count}")

        # Redact if not detect-only mode
        if not detect_only:
            processed_content = self.privacy_manager.redact(content, level=level)

            # Check if safe for level
            is_safe = self.privacy_manager.is_safe_for_level(processed_content, level)
            report['safe_for_level'] = is_safe

            if not is_safe:
                logger.warning(f"Content may not be safe for {level.value} level after redaction!")
        else:
            processed_content = content
            report['safe_for_level'] = None

        # Write audit log
        self._write_audit_log(report)

        return processed_content, report

    def _write_audit_log(self, report: Dict):
        """Write privacy audit log."""
        audit_file = self.audit_dir / "privacy-audit.log"

        log_entry = {
            'timestamp': report['timestamp'],
            'content_type': report['content_type'],
            'privacy_level': report['privacy_level'],
            'pii_detections': report['pii_detections'],
            'detection_types': report['detection_types'],
            'redacted': report['redacted'],
            'safe_for_level': report.get('safe_for_level')
        }

        try:
            with open(audit_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")


# Convenience functions for common workflows

def process_checkpoint_with_privacy(
    checkpoint_content: str,
    privacy_level: str = "private",
    detect_only: bool = False,
    repo_root: Optional[Path] = None
) -> Tuple[str, Dict]:
    """
    Process checkpoint content with privacy controls.

    Args:
        checkpoint_content: Checkpoint markdown content
        privacy_level: Privacy level (public, team, private, ephemeral)
        detect_only: Only detect PII, don't redact
        repo_root: Repository root directory

    Returns:
        Tuple of (processed_content, privacy_report)
    """
    integration = PrivacyIntegration(repo_root=repo_root)
    return integration.process_content(
        checkpoint_content,
        content_type="checkpoint",
        privacy_level=privacy_level,
        detect_only=detect_only
    )


def process_export_with_privacy(
    export_content: str,
    privacy_level: str = "private",
    detect_only: bool = False,
    repo_root: Optional[Path] = None
) -> Tuple[str, Dict]:
    """
    Process export content with privacy controls.

    Args:
        export_content: Export text content
        privacy_level: Privacy level (public, team, private, ephemeral)
        detect_only: Only detect PII, don't redact
        repo_root: Repository root directory

    Returns:
        Tuple of (processed_content, privacy_report)
    """
    integration = PrivacyIntegration(repo_root=repo_root)
    return integration.process_content(
        export_content,
        content_type="export",
        privacy_level=privacy_level,
        detect_only=detect_only
    )


def process_session_with_privacy(
    session_content: str,
    privacy_level: str = "private",
    detect_only: bool = False,
    repo_root: Optional[Path] = None
) -> Tuple[str, Dict]:
    """
    Process session content with privacy controls.

    Args:
        session_content: Session markdown/JSON content
        privacy_level: Privacy level (public, team, private, ephemeral)
        detect_only: Only detect PII, don't redact
        repo_root: Repository root directory

    Returns:
        Tuple of (processed_content, privacy_report)
    """
    integration = PrivacyIntegration(repo_root=repo_root)
    return integration.process_content(
        session_content,
        content_type="session",
        privacy_level=privacy_level,
        detect_only=detect_only
    )


def main():
    """CLI interface for privacy integration."""
    import argparse

    parser = argparse.ArgumentParser(
        description="CODITECT Privacy Integration - Process content with privacy controls"
    )
    parser.add_argument('--file', type=str, help='File to process')
    parser.add_argument('--text', type=str, help='Text to process')
    parser.add_argument('--type', type=str, choices=['checkpoint', 'export', 'session'],
                        default='checkpoint', help='Content type')
    parser.add_argument('--level', type=str,
                        choices=['public', 'team', 'private', 'ephemeral'],
                        default='private', help='Privacy level')
    parser.add_argument('--detect-only', action='store_true',
                        help='Only detect PII, do not redact')
    parser.add_argument('--output', type=str, help='Output file (default: stdout)')

    args = parser.parse_args()

    # Get content
    if args.file:
        with open(args.file, 'r') as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        print("ERROR: Must provide --file or --text")
        sys.exit(1)

    # Process content
    integration = PrivacyIntegration()
    processed_content, report = integration.process_content(
        content,
        content_type=args.type,
        privacy_level=args.level,
        detect_only=args.detect_only
    )

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(processed_content)
        print(f"✅ Processed content written to: {args.output}")
    else:
        print(processed_content)

    # Print report
    print("\n" + "="*80)
    print("PRIVACY REPORT")
    print("="*80)
    print(f"Content Type: {report['content_type']}")
    print(f"Privacy Level: {report['privacy_level']}")
    print(f"PII Detections: {report['pii_detections']}")
    if report['detection_types']:
        print("\nDetection Breakdown:")
        for pii_type, count in report['detection_types'].items():
            print(f"  - {pii_type}: {count}")
    print(f"Redacted: {'Yes' if report['redacted'] else 'No (detect-only mode)'}")
    if report.get('safe_for_level') is not None:
        safe_status = "✅ SAFE" if report['safe_for_level'] else "⚠️ MAY NOT BE SAFE"
        print(f"Safe for {report['privacy_level']}: {safe_status}")
    print("="*80)


if __name__ == '__main__':
    main()
