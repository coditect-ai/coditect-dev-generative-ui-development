#!/usr/bin/env python3
"""
CODITECT Conversation Export Deduplicator - CLI Tool

User-friendly command-line interface for conversation export deduplication.
Supports single file, batch directory processing, statistics, and integrity checks.

Usage:
    deduplicate-export --file export.json --session-id my-session
    deduplicate-export --batch MEMORY-CONTEXT/exports/
    deduplicate-export --stats --session-id my-session
    deduplicate-export --integrity --storage-dir MEMORY-CONTEXT/dedup_state

Author: Claude + AZ1.AI
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

# Add core scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from core.conversation_deduplicator import (
    ClaudeConversationDeduplicator,
    parse_claude_export_file,
    extract_session_id_from_filename as extract_session_id_core
)


class Colors:
    """ANSI color codes for terminal output"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    def disable():
        """Disable colors for non-terminal output"""
        Colors.HEADER = ""
        Colors.OKBLUE = ""
        Colors.OKCYAN = ""
        Colors.OKGREEN = ""
        Colors.WARNING = ""
        Colors.FAIL = ""
        Colors.ENDC = ""
        Colors.BOLD = ""
        Colors.UNDERLINE = ""


def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * len(text)}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def extract_session_id_from_filename(filepath: Path) -> str:
    """
    Extract session ID from export filename.

    Wrapper around core function for consistency.
    """
    return extract_session_id_core(filepath)


def parse_export_file(filepath: Path) -> Dict[str, Any]:
    """
    Parse export file and convert to standard format.

    Supports:
    - JSON format (if already structured)
    - Plain text format (Claude Code /export output)
    """
    try:
        with open(filepath, "r") as f:
            content = f.read()

        # Try parsing as JSON first
        try:
            data = json.loads(content)
            if "messages" in data:
                return data
        except json.JSONDecodeError:
            pass

        # Plain text format - use proper Claude export parser
        return parse_claude_export_file(filepath)

    except Exception as e:
        raise ValueError(f"Failed to parse export file {filepath}: {e}")


def process_single_file(
    filepath: Path,
    session_id: Optional[str],
    dedup: ClaudeConversationDeduplicator,
    dry_run: bool = False,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Process a single export file"""

    if verbose:
        print_info(f"Processing: {filepath}")

    # Auto-detect session ID if not provided
    if not session_id:
        session_id = extract_session_id_from_filename(filepath)
        if verbose:
            print_info(f"Auto-detected session ID: {session_id}")

    # Parse export file
    try:
        export_data = parse_export_file(filepath)
    except Exception as e:
        print_error(f"Failed to parse {filepath.name}: {e}")
        return {"success": False, "error": str(e)}

    # Process with deduplicator
    try:
        if dry_run:
            new_messages, stats = dedup.process_export(session_id, export_data, dry_run=True)
        else:
            new_messages, stats = dedup.process_export(session_id, export_data)

        result = {
            "success": True,
            "session_id": session_id,
            "file": str(filepath),
            "total_messages": stats["messages_in_export"],
            "new_messages": stats["new_messages"],
            "duplicates_filtered": stats["duplicates_filtered"],
            "content_collisions": stats["content_collisions"],
            "deduplication_rate": (
                (stats["duplicates_filtered"] / stats["messages_in_export"] * 100)
                if stats["messages_in_export"] > 0
                else 0
            ),
        }

        if verbose or not dry_run:
            print_success(f"Processed {filepath.name}")
            print(f"   Session: {session_id}")
            print(
                f"   Total: {stats['messages_in_export']} | "
                f"New: {stats['new_messages']} | "
                f"Duplicates: {stats['duplicates_filtered']}"
            )
            if stats["messages_in_export"] > 0:
                print(f"   Deduplication: {result['deduplication_rate']:.1f}%")

        return result

    except Exception as e:
        print_error(f"Processing failed: {e}")
        return {"success": False, "error": str(e)}


def process_batch(
    directory: Path,
    dedup: ClaudeConversationDeduplicator,
    dry_run: bool = False,
    verbose: bool = False,
) -> List[Dict[str, Any]]:
    """Process all export files in a directory"""

    print_header(f"Batch Processing: {directory}")

    # Find all export files
    patterns = ["*.txt", "*.json", "*.md"]
    export_files = []

    for pattern in patterns:
        export_files.extend(directory.glob(pattern))

    if not export_files:
        print_warning(f"No export files found in {directory}")
        return []

    print_info(f"Found {len(export_files)} files to process")

    results = []
    for filepath in sorted(export_files):
        result = process_single_file(filepath, None, dedup, dry_run, verbose)
        results.append(result)

    # Summary
    print_header("Batch Processing Summary")

    successful = sum(1 for r in results if r.get("success"))
    failed = len(results) - successful

    print(f"Total files: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if successful > 0:
        total_msgs = sum(r.get("total_messages", 0) for r in results if r.get("success"))
        total_new = sum(r.get("new_messages", 0) for r in results if r.get("success"))
        total_dup = total_msgs - total_new

        print(f"\nTotal messages: {total_msgs}")
        print(f"New messages: {total_new}")
        print(f"Duplicates filtered: {total_dup}")

        if total_msgs > 0:
            print(f"Overall deduplication rate: {total_dup / total_msgs * 100:.1f}%")

    return results


def show_statistics(
    session_id: str, dedup: ClaudeConversationDeduplicator
) -> None:
    """Display statistics for a session"""

    print_header(f"Statistics: {session_id}")

    try:
        stats = dedup.get_statistics(session_id)

        print(f"Session ID: {session_id}")
        print(f"Watermark: {stats.get('watermark', 'N/A')}")
        print(f"Unique messages: {stats.get('unique_messages', 'N/A')}")
        print(f"Total messages: {stats.get('total_messages', 'N/A')}")

        # Get full conversation for additional stats
        try:
            messages = dedup.get_full_conversation(session_id)
            print(f"Reconstructable messages: {len(messages)}")
        except Exception as e:
            print_warning(f"Could not reconstruct conversation: {e}")

        print_success("Statistics retrieved successfully")

    except Exception as e:
        print_error(f"Failed to get statistics: {e}")


def run_integrity_check(
    dedup: ClaudeConversationDeduplicator, verbose: bool = False
) -> None:
    """Run integrity check on all conversations"""

    print_header("Integrity Check")

    try:
        # Get all conversation IDs from watermarks
        watermarks = dedup.watermarks

        if not watermarks:
            print_warning("No conversations found")
            return

        print_info(f"Checking {len(watermarks)} conversations...")

        all_valid = True
        for conv_id in watermarks:
            try:
                is_valid, issues = dedup.validate_integrity(conv_id)

                if is_valid:
                    if verbose:
                        print_success(f"{conv_id}: Valid")
                else:
                    print_warning(f"{conv_id}: Issues found")
                    for issue in issues:
                        print(f"   - {issue}")
                    all_valid = False

            except Exception as e:
                print_error(f"{conv_id}: Check failed - {e}")
                all_valid = False

        if all_valid:
            print_success(f"All {len(watermarks)} conversations passed integrity check")
        else:
            print_warning("Some conversations have integrity issues (see above)")

    except Exception as e:
        print_error(f"Integrity check failed: {e}")


def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description="CODITECT Conversation Export Deduplicator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single file
  %(prog)s --file export.json --session-id my-session

  # Auto-detect session ID from filename
  %(prog)s --file 2025-11-17-EXPORT-ROLLOUT-MASTER.txt

  # Batch process directory
  %(prog)s --batch MEMORY-CONTEXT/exports/

  # Show statistics
  %(prog)s --stats --session-id my-session

  # Run integrity check
  %(prog)s --integrity

  # Dry run (preview without changes)
  %(prog)s --file export.json --dry-run

For more information, see: DEVELOPMENT-SETUP.md
        """,
    )

    # Mode selection (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--file", "-f", type=Path, help="Process single export file"
    )
    mode_group.add_argument(
        "--batch", "-b", type=Path, help="Process all files in directory"
    )
    mode_group.add_argument(
        "--stats", action="store_true", help="Show statistics for a session"
    )
    mode_group.add_argument(
        "--integrity", action="store_true", help="Run integrity check on all conversations"
    )

    # Common options
    parser.add_argument(
        "--session-id",
        "-s",
        help="Session identifier (auto-detected if not provided)",
    )
    parser.add_argument(
        "--storage-dir",
        "-d",
        type=Path,
        default=Path("../../MEMORY-CONTEXT/dedup_state"),
        help="Storage directory for deduplication state (default: ../../MEMORY-CONTEXT/dedup_state)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying storage",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Minimal output (errors only)"
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Write results to JSON file",
    )

    args = parser.parse_args()

    # Configure colors
    if args.no_color or not sys.stdout.isatty():
        Colors.disable()

    # Initialize deduplicator
    try:
        dedup = ClaudeConversationDeduplicator(storage_dir=args.storage_dir)
        if args.verbose:
            print_success(f"Deduplicator initialized: {args.storage_dir}")
    except Exception as e:
        print_error(f"Failed to initialize deduplicator: {e}")
        return 1

    # Execute requested mode
    result = None

    try:
        if args.file:
            # Single file mode
            if not args.file.exists():
                print_error(f"File not found: {args.file}")
                return 1

            print_header("Single File Processing")
            result = process_single_file(
                args.file, args.session_id, dedup, args.dry_run, args.verbose
            )

            if args.output:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                print_success(f"Results written to {args.output}")

        elif args.batch:
            # Batch directory mode
            if not args.batch.is_dir():
                print_error(f"Directory not found: {args.batch}")
                return 1

            results = process_batch(args.batch, dedup, args.dry_run, args.verbose)

            if args.output:
                with open(args.output, "w") as f:
                    json.dump(results, f, indent=2)
                print_success(f"Results written to {args.output}")

        elif args.stats:
            # Statistics mode
            if not args.session_id:
                print_error("--session-id required for --stats mode")
                return 1

            show_statistics(args.session_id, dedup)

        elif args.integrity:
            # Integrity check mode
            run_integrity_check(dedup, args.verbose)

    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
        return 130

    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
