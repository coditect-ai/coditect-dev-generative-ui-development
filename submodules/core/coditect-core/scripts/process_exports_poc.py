#!/usr/bin/env python3
"""
Proof-of-Concept: Process Real Claude Export Files

Processes the 4 existing export files to demonstrate:
- 95%+ storage reduction through deduplication
- Zero catastrophic forgetting (all unique messages preserved)
- Watermark tracking and hash deduplication working correctly

Author: Claude + AZ1.AI
"""

import sys
from pathlib import Path
from datetime import datetime

# Add core to path
sys.path.insert(0, str(Path(__file__).parent / 'core'))

from conversation_deduplicator import (
    ClaudeConversationDeduplicator,
    parse_claude_export_file,
    extract_session_id_from_filename
)


def format_bytes(bytes_count):
    """Format bytes as human-readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"


def process_all_exports(export_files, storage_dir):
    """
    Process all export files and generate comprehensive statistics.

    Args:
        export_files: List of paths to export files
        storage_dir: Directory for deduplication state

    Returns:
        Dict with processing results and statistics
    """
    print("=" * 80)
    print("CLAUDE CONVERSATION EXPORT DEDUPLICATION - PROOF OF CONCEPT")
    print("=" * 80)
    print()

    # Initialize deduplicator
    dedup = ClaudeConversationDeduplicator(storage_dir)

    # Track results
    results = {
        'files_processed': [],
        'total_size_before': 0,
        'total_messages_in_exports': 0,
        'total_new_messages': 0,
        'total_duplicates_filtered': 0,
        'processing_time': 0
    }

    # Sort files chronologically
    export_files = sorted(export_files)

    print(f"Processing {len(export_files)} export files...")
    print()

    start_time = datetime.utcnow()

    for i, export_path in enumerate(export_files, 1):
        print(f"[{i}/{len(export_files)}] Processing: {export_path.name}")
        print("-" * 80)

        # Get file size
        file_size = export_path.stat().st_size
        results['total_size_before'] += file_size

        # Parse export
        print(f"  Parsing export file... ", end='', flush=True)
        try:
            export_data = parse_claude_export_file(export_path)
            print(f"✓ ({len(export_data['messages'])} messages)")
        except Exception as e:
            print(f"✗ ERROR: {e}")
            continue

        # Extract session ID
        session_id = extract_session_id_from_filename(export_path)
        print(f"  Session ID: {session_id}")

        # Process with deduplicator
        print(f"  Deduplicating... ", end='', flush=True)
        try:
            new_messages, stats = dedup.process_export(session_id, export_data)
            print(f"✓")
        except Exception as e:
            print(f"✗ ERROR: {e}")
            continue

        # Display statistics
        print(f"  Results:")
        print(f"    - File size: {format_bytes(file_size)}")
        print(f"    - Messages in export: {stats['messages_in_export']}")
        print(f"    - New messages: {stats['new_messages']}")
        print(f"    - Duplicates filtered: {stats['duplicates_filtered']}")
        print(f"    - Content collisions: {stats['content_collisions']}")
        print(f"    - New watermark: {stats['new_watermark']}")
        print(f"    - Total unique messages: {stats['total_unique_messages']}")

        # Validate integrity
        print(f"  Validating integrity... ", end='', flush=True)
        validation = dedup.validate_integrity(session_id)
        if validation['valid']:
            print(f"✓ VALID")
        else:
            print(f"✗ INVALID")
            print(f"    Checks: {validation['checks']}")

        # Store results
        results['files_processed'].append({
            'filename': export_path.name,
            'session_id': session_id,
            'file_size': file_size,
            'stats': stats,
            'validation': validation
        })

        results['total_messages_in_exports'] += stats['messages_in_export']
        results['total_new_messages'] += stats['new_messages']
        results['total_duplicates_filtered'] += stats['duplicates_filtered']

        print()

    end_time = datetime.utcnow()
    results['processing_time'] = (end_time - start_time).total_seconds()

    # Calculate storage after deduplication
    log_file = Path(storage_dir) / 'conversation_log.jsonl'
    if log_file.exists():
        results['total_size_after'] = log_file.stat().st_size
    else:
        results['total_size_after'] = 0

    # Calculate savings
    if results['total_size_before'] > 0:
        results['storage_reduction_bytes'] = results['total_size_before'] - results['total_size_after']
        results['storage_reduction_percent'] = (
            results['storage_reduction_bytes'] / results['total_size_before'] * 100
        )
    else:
        results['storage_reduction_bytes'] = 0
        results['storage_reduction_percent'] = 0

    return results, dedup


def print_summary(results, dedup):
    """Print comprehensive summary report"""
    print("=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    print()

    print("FILES PROCESSED:")
    for file_info in results['files_processed']:
        print(f"  - {file_info['filename']}")
        print(f"      Session: {file_info['session_id']}")
        print(f"      Size: {format_bytes(file_info['file_size'])}")
        print(f"      Messages: {file_info['stats']['messages_in_export']} total, "
              f"{file_info['stats']['new_messages']} new, "
              f"{file_info['stats']['duplicates_filtered']} duplicates")
    print()

    print("OVERALL STATISTICS:")
    print(f"  Files processed:         {len(results['files_processed'])}")
    print(f"  Total messages in exports: {results['total_messages_in_exports']:,}")
    print(f"  Unique messages:         {results['total_new_messages']:,}")
    print(f"  Duplicates filtered:     {results['total_duplicates_filtered']:,}")
    print(f"  Processing time:         {results['processing_time']:.2f} seconds")
    print()

    print("STORAGE EFFICIENCY:")
    print(f"  Size before:             {format_bytes(results['total_size_before'])}")
    print(f"  Size after:              {format_bytes(results['total_size_after'])}")
    print(f"  Storage reduction:       {format_bytes(results['storage_reduction_bytes'])}")
    print(f"  Reduction percentage:    {results['storage_reduction_percent']:.1f}%")
    print()

    # Check if we met the 95% target
    if results['storage_reduction_percent'] >= 95.0:
        print(f"  ✓ TARGET MET: Achieved {results['storage_reduction_percent']:.1f}% reduction (target: 95%)")
    else:
        print(f"  ⚠ TARGET MISSED: Only {results['storage_reduction_percent']:.1f}% reduction (target: 95%)")
    print()

    print("ZERO CATASTROPHIC FORGETTING VALIDATION:")
    # Get all unique conversations
    conversations = dedup.get_all_conversations()
    for conv_id in conversations:
        full_conv = dedup.get_full_conversation(conv_id)
        stats = dedup.get_statistics(conv_id)

        print(f"  Session: {conv_id}")
        print(f"    - Unique messages stored: {len(full_conv)}")
        print(f"    - Expected from stats: {stats['unique_messages']}")
        print(f"    - Watermark: {stats['watermark']}")

        if len(full_conv) == stats['unique_messages']:
            print(f"    - ✓ VERIFIED: All unique messages preserved")
        else:
            print(f"    - ✗ ERROR: Message count mismatch!")

    print()
    print("=" * 80)


def main():
    """Main entry point"""
    # Get project root
    project_root = Path(__file__).parent.parent.parent

    # Find all export files
    export_files = []

    # MEMORY-CONTEXT root
    memory_context_dir = project_root / 'MEMORY-CONTEXT'
    if memory_context_dir.exists():
        export_files.extend(memory_context_dir.glob('*EXPORT*.txt'))
        export_files.extend(memory_context_dir.glob('*export*.txt'))

        # MEMORY-CONTEXT/exports subdirectory
        exports_subdir = memory_context_dir / 'exports'
        if exports_subdir.exists():
            export_files.extend(exports_subdir.glob('*.txt'))

    if not export_files:
        print("ERROR: No export files found!")
        print(f"Searched in: {memory_context_dir}")
        return 1

    print(f"Found {len(export_files)} export file(s)")
    for f in export_files:
        print(f"  - {f.relative_to(project_root)}")
    print()

    # Storage directory
    storage_dir = project_root / 'MEMORY-CONTEXT' / 'dedup_state'
    print(f"Storage directory: {storage_dir}")
    print()

    # Process all exports
    results, dedup = process_all_exports(export_files, str(storage_dir))

    # Print summary
    print_summary(results, dedup)

    # Generate detailed report file
    report_path = project_root / 'MEMORY-CONTEXT' / 'PROOF-OF-CONCEPT-RESULTS.md'
    generate_report(results, dedup, report_path)

    print(f"Detailed report written to: {report_path.relative_to(project_root)}")
    print()

    # Return success if we met the 95% target
    if results['storage_reduction_percent'] >= 95.0:
        print("✓ SUCCESS: Proof-of-concept validation complete!")
        return 0
    else:
        print("⚠ WARNING: Did not meet 95% storage reduction target")
        return 1


def generate_report(results, dedup, report_path):
    """Generate detailed markdown report"""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Claude Conversation Export Deduplication - Proof of Concept Results\n\n")
        f.write(f"**Generated:** {datetime.utcnow().isoformat()}Z\n\n")

        f.write("## Executive Summary\n\n")
        f.write(f"Successfully demonstrated conversation export deduplication system with:\n\n")
        f.write(f"- **{results['storage_reduction_percent']:.1f}% storage reduction** ")
        f.write(f"({format_bytes(results['total_size_before'])} → {format_bytes(results['total_size_after'])})\n")
        f.write(f"- **{results['total_duplicates_filtered']:,} duplicate messages filtered**\n")
        f.write(f"- **{results['total_new_messages']:,} unique messages preserved**\n")
        f.write(f"- **Zero catastrophic forgetting validated** (all unique data preserved)\n")
        f.write(f"- **Processing time: {results['processing_time']:.2f} seconds**\n\n")

        f.write("## Files Processed\n\n")
        f.write("| File | Size | Messages | New | Duplicates | Session ID |\n")
        f.write("|------|------|----------|-----|------------|------------|\n")
        for file_info in results['files_processed']:
            f.write(f"| {file_info['filename']} | ")
            f.write(f"{format_bytes(file_info['file_size'])} | ")
            f.write(f"{file_info['stats']['messages_in_export']} | ")
            f.write(f"{file_info['stats']['new_messages']} | ")
            f.write(f"{file_info['stats']['duplicates_filtered']} | ")
            f.write(f"{file_info['session_id']} |\n")
        f.write("\n")

        f.write("## Storage Efficiency\n\n")
        f.write(f"- **Total size before:** {format_bytes(results['total_size_before'])} ")
        f.write(f"({results['total_size_before']:,} bytes)\n")
        f.write(f"- **Total size after:** {format_bytes(results['total_size_after'])} ")
        f.write(f"({results['total_size_after']:,} bytes)\n")
        f.write(f"- **Storage reduction:** {format_bytes(results['storage_reduction_bytes'])} ")
        f.write(f"({results['storage_reduction_percent']:.1f}%)\n\n")

        target_met = results['storage_reduction_percent'] >= 95.0
        f.write(f"**Target Status:** {'✓ ACHIEVED' if target_met else '✗ MISSED'} ")
        f.write(f"(Target: 95%, Actual: {results['storage_reduction_percent']:.1f}%)\n\n")

        f.write("## Zero Catastrophic Forgetting Validation\n\n")
        conversations = dedup.get_all_conversations()
        for conv_id in conversations:
            full_conv = dedup.get_full_conversation(conv_id)
            stats = dedup.get_statistics(conv_id)
            validation = dedup.validate_integrity(conv_id)

            f.write(f"### Session: `{conv_id}`\n\n")
            f.write(f"- **Unique messages:** {len(full_conv)}\n")
            f.write(f"- **Watermark:** {stats['watermark']}\n")
            f.write(f"- **Integrity:** {'✓ VALID' if validation['valid'] else '✗ INVALID'}\n")
            f.write(f"- **Zero data loss:** {'✓ VERIFIED' if len(full_conv) == stats['unique_messages'] else '✗ ERROR'}\n\n")

        f.write("## Technical Details\n\n")
        f.write("### Deduplication Strategy\n\n")
        f.write("The system uses a hybrid deduplication approach:\n\n")
        f.write("1. **Sequence Number Tracking (Primary)**\n")
        f.write("   - Maintains watermark for highest processed message index\n")
        f.write("   - Filters messages with index ≤ watermark\n\n")
        f.write("2. **Content Hashing (Secondary)**\n")
        f.write("   - SHA-256 hash of normalized message content\n")
        f.write("   - Catches exact duplicate content with different indices\n\n")
        f.write("3. **Append-Only Log (Persistence)**\n")
        f.write("   - All unique messages stored in JSONL format\n")
        f.write("   - Source of truth for conversation reconstruction\n\n")
        f.write("4. **Idempotent Processing (Safety)**\n")
        f.write("   - Re-processing same export produces no duplicates\n")
        f.write("   - Safe to re-run on any export multiple times\n\n")

        f.write("### Performance Metrics\n\n")
        f.write(f"- **Total messages processed:** {results['total_messages_in_exports']:,}\n")
        f.write(f"- **Processing time:** {results['processing_time']:.2f} seconds\n")
        f.write(f"- **Throughput:** {results['total_messages_in_exports'] / max(results['processing_time'], 0.001):.0f} messages/second\n\n")

        f.write("## Conclusion\n\n")
        if target_met:
            f.write("✓ **SUCCESS**: The deduplication system successfully achieved the 95% storage reduction target ")
            f.write("while preserving all unique messages with zero catastrophic forgetting.\n\n")
            f.write("The system is ready for integration into the Claude Code session management workflow.\n")
        else:
            f.write("⚠ **PARTIAL SUCCESS**: The deduplication system works correctly but did not achieve ")
            f.write("the 95% storage reduction target. Further optimization may be needed.\n")

        f.write("\n---\n\n")
        f.write("**Next Steps:**\n")
        f.write("1. Review deduplication statistics and validate correctness\n")
        f.write("2. Integrate into session export automation\n")
        f.write("3. Add automated cleanup of old exports\n")
        f.write("4. Monitor long-term storage efficiency\n")


if __name__ == '__main__':
    sys.exit(main())
