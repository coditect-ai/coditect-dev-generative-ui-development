#!/usr/bin/env python3
"""
Bulk Export Consolidation Script

Processes all export files through deduplication system while preserving timestamps.
Ensures all unique messages are consolidated into single database and backed up to git.

Usage:
    python3 scripts/bulk-consolidate-exports.py [--dry-run]
"""

import os
import sys
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

MEMORY_CONTEXT_DIR = project_root / "MEMORY-CONTEXT"
DEDUP_STATE_DIR = MEMORY_CONTEXT_DIR / "dedup_state"
GLOBAL_HASHES_FILE = DEDUP_STATE_DIR / "global_hashes.json"
UNIQUE_MESSAGES_FILE = DEDUP_STATE_DIR / "unique_messages.jsonl"
CHECKPOINT_INDEX_FILE = DEDUP_STATE_DIR / "checkpoint_index.json"


def find_all_export_files() -> List[Tuple[Path, datetime]]:
    """Find all export files with their filesystem timestamps."""
    export_files = []

    # Search patterns
    patterns = [
        MEMORY_CONTEXT_DIR / "*EXPORT*.txt",
        MEMORY_CONTEXT_DIR / "exports" / "*EXPORT*.txt",
        MEMORY_CONTEXT_DIR / "test-dataset" / "exports" / "*EXPORT*.txt",
    ]

    for pattern in patterns:
        parent = pattern.parent
        if parent.exists():
            for file_path in parent.glob(pattern.name):
                if file_path.is_file():
                    # Get file modification time (preserves original timestamp)
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    export_files.append((file_path, mtime))

    # Sort by modification time (oldest first)
    export_files.sort(key=lambda x: x[1])
    return export_files


def load_checkpoint_index() -> Dict:
    """Load existing checkpoint index."""
    if CHECKPOINT_INDEX_FILE.exists():
        with open(CHECKPOINT_INDEX_FILE, 'r') as f:
            return json.load(f)
    return {}


def load_global_hashes() -> Set[str]:
    """Load existing global hashes."""
    if GLOBAL_HASHES_FILE.exists():
        with open(GLOBAL_HASHES_FILE, 'r') as f:
            data = json.load(f)
            # Handle both array and object formats
            if isinstance(data, list):
                return set(data)
            elif isinstance(data, dict):
                return set(data.get("hashes", []))
    return set()


def parse_export_file(file_path: Path) -> List[Dict]:
    """Parse export file and extract messages."""
    messages = []
    current_message = []
    in_message = False

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Check for message boundaries
                if line.strip().startswith('## Message') or line.strip().startswith('---'):
                    if current_message and in_message:
                        # Save previous message
                        content = ''.join(current_message).strip()
                        if content:
                            messages.append({
                                'role': 'unknown',
                                'content': content,
                                'timestamp': None
                            })
                        current_message = []
                    in_message = True
                    continue

                if in_message:
                    current_message.append(line)

            # Don't forget the last message
            if current_message:
                content = ''.join(current_message).strip()
                if content:
                    messages.append({
                        'role': 'unknown',
                        'content': content,
                        'timestamp': None
                    })

    except Exception as e:
        print(f"⚠️  Error parsing {file_path.name}: {e}")
        return []

    return messages


def compute_hash(message: Dict) -> str:
    """Compute SHA-256 hash of message content."""
    content = message.get('content', '')
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def process_export_file(
    file_path: Path,
    file_mtime: datetime,
    global_hashes: Set[str],
    checkpoint_index: Dict
) -> Tuple[int, int, List[Dict]]:
    """
    Process single export file.

    Returns:
        (total_messages, new_messages, unique_message_objects)
    """
    checkpoint_name = f"export-{file_path.stem}"

    # Check if already processed
    if checkpoint_name in checkpoint_index:
        print(f"⏭️  Skipping {file_path.name} (already processed)")
        return (0, 0, [])

    # Parse messages
    messages = parse_export_file(file_path)
    if not messages:
        print(f"⚠️  No messages found in {file_path.name}")
        return (0, 0, [])

    # Deduplicate
    new_unique_messages = []
    new_hashes = []

    for msg in messages:
        msg_hash = compute_hash(msg)
        if msg_hash not in global_hashes:
            # New unique message
            global_hashes.add(msg_hash)
            new_hashes.append(msg_hash)
            new_unique_messages.append({
                'hash': msg_hash,
                'message': msg,
                'first_seen': file_mtime.isoformat(),
                'checkpoint': checkpoint_name
            })

    total = len(messages)
    new = len(new_unique_messages)
    dups = total - new

    print(f"✅ {file_path.name}: {total} messages ({new} new, {dups} duplicates)")

    return (total, new, new_unique_messages)


def save_dedup_state(
    global_hashes: Set[str],
    new_unique_messages: List[Dict],
    checkpoint_index: Dict
):
    """Save updated deduplication state."""
    # Ensure dedup_state directory exists
    DEDUP_STATE_DIR.mkdir(parents=True, exist_ok=True)

    # Save global hashes (maintain simple array format for compatibility)
    with open(GLOBAL_HASHES_FILE, 'w') as f:
        json.dump(sorted(list(global_hashes)), f)

    # Append unique messages
    with open(UNIQUE_MESSAGES_FILE, 'a') as f:
        for msg_obj in new_unique_messages:
            f.write(json.dumps(msg_obj) + '\n')

    # Save checkpoint index
    with open(CHECKPOINT_INDEX_FILE, 'w') as f:
        json.dump(checkpoint_index, f, indent=2)


def main(dry_run: bool = False):
    """Main consolidation workflow."""
    print("=" * 80)
    print("BULK EXPORT CONSOLIDATION")
    print("=" * 80)
    print()

    # Find all export files
    print("📂 Scanning for export files...")
    export_files = find_all_export_files()
    print(f"   Found {len(export_files)} export files")
    print()

    # Load existing state
    print("📊 Loading existing deduplication state...")
    checkpoint_index = load_checkpoint_index()
    global_hashes = load_global_hashes()
    print(f"   Existing checkpoints: {len(checkpoint_index)}")
    print(f"   Existing unique messages: {len(global_hashes)}")
    print()

    # Process files
    print("🔄 Processing export files...")
    print()

    total_messages_all = 0
    total_new_all = 0
    all_new_unique_messages = []
    processed_count = 0

    for file_path, file_mtime in export_files:
        total, new, unique_msgs = process_export_file(
            file_path, file_mtime, global_hashes, checkpoint_index
        )

        if total > 0:
            total_messages_all += total
            total_new_all += new
            all_new_unique_messages.extend(unique_msgs)

            # Add to checkpoint index
            checkpoint_name = f"export-{file_path.stem}"
            checkpoint_index[checkpoint_name] = {
                "created": datetime.utcnow().isoformat() + "Z",
                "message_hashes": [msg['hash'] for msg in unique_msgs],
                "source_file": str(file_path.relative_to(project_root)),
                "file_timestamp": file_mtime.isoformat()
            }
            processed_count += 1

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files processed: {processed_count}")
    print(f"Total messages scanned: {total_messages_all}")
    print(f"New unique messages: {total_new_all}")
    print(f"Duplicates filtered: {total_messages_all - total_new_all}")
    print(f"Total unique messages in database: {len(global_hashes)}")
    print()

    if dry_run:
        print("🔍 DRY RUN - No changes written")
        return

    if processed_count == 0:
        print("✅ All export files already processed!")
        return

    # Save state
    print("💾 Saving deduplication state...")
    save_dedup_state(global_hashes, all_new_unique_messages, checkpoint_index)
    print("   ✅ State saved")
    print()

    # Git tracking
    print("📝 Recommendation: Commit to git with:")
    print()
    print(f"   git add {DEDUP_STATE_DIR.relative_to(project_root)}")
    print(f"   git commit -m \"Bulk consolidation: {processed_count} files, {total_new_all} new unique messages\"")
    print()


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)
