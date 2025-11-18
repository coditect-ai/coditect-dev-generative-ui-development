#!/usr/bin/env python3
"""
Comprehensive Export and Checkpoint Consolidation

Processes:
1. All remaining EXPORT files (across all locations)
2. All CHECKPOINT markdown files
3. Deduplicates everything into single database

Usage:
    python3 scripts/comprehensive-consolidation.py
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


def find_all_content_files() -> Dict[str, List[Tuple[Path, datetime]]]:
    """Find all export and checkpoint files."""
    files = {
        'exports': [],
        'checkpoints': []
    }

    # Find all export files
    for export_file in project_root.glob("**/*EXPORT*.txt"):
        if export_file.is_file() and '.git' not in str(export_file):
            mtime = datetime.fromtimestamp(export_file.stat().st_mtime)
            files['exports'].append((export_file, mtime))

    # Find all checkpoint files
    checkpoints_dir = project_root / "CHECKPOINTS"
    if checkpoints_dir.exists():
        for ckpt_file in checkpoints_dir.glob("*.md"):
            if ckpt_file.is_file():
                mtime = datetime.fromtimestamp(ckpt_file.stat().st_mtime)
                files['checkpoints'].append((ckpt_file, mtime))

    # Sort by modification time
    files['exports'].sort(key=lambda x: x[1])
    files['checkpoints'].sort(key=lambda x: x[1])

    return files


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
                if line.strip().startswith('## Message') or line.strip().startswith('---'):
                    if current_message and in_message:
                        content = ''.join(current_message).strip()
                        if content:
                            messages.append({
                                'role': 'unknown',
                                'content': content,
                                'timestamp': None,
                                'source_type': 'export'
                            })
                        current_message = []
                    in_message = True
                    continue

                if in_message:
                    current_message.append(line)

            # Last message
            if current_message:
                content = ''.join(current_message).strip()
                if content:
                    messages.append({
                        'role': 'unknown',
                        'content': content,
                        'timestamp': None,
                        'source_type': 'export'
                    })

    except Exception as e:
        print(f"⚠️  Error parsing {file_path.name}: {e}")
        return []

    return messages


def parse_checkpoint_file(file_path: Path) -> List[Dict]:
    """Parse checkpoint markdown file and extract sections as messages."""
    messages = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract major sections
        sections = re.split(r'\n#{1,2}\s+', content)

        for section in sections:
            section = section.strip()
            if len(section) > 100:  # Only include substantial sections
                messages.append({
                    'role': 'checkpoint',
                    'content': section,
                    'timestamp': None,
                    'source_type': 'checkpoint'
                })

    except Exception as e:
        print(f"⚠️  Error parsing {file_path.name}: {e}")
        return []

    return messages


def compute_hash(message: Dict) -> str:
    """Compute SHA-256 hash of message content."""
    content = message.get('content', '')
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def deduplicate_by_location(files: List[Tuple[Path, datetime]]) -> List[Tuple[Path, datetime]]:
    """
    Deduplicate files by preferring original locations over copies.

    Priority:
    1. Coditect-v5-multiple-LLM-IDE/docs/09-sessions/ (originals)
    2. coditect-project-dot-claude/MEMORY-CONTEXT/ (framework)
    3. Master MEMORY-CONTEXT/ (current project)
    4. test-dataset/ (copies)
    5. archives/ (backups)
    """
    seen_names = {}

    for file_path, mtime in files:
        filename = file_path.name

        if filename not in seen_names:
            seen_names[filename] = (file_path, mtime)
        else:
            # Prefer originals over copies
            existing_path, existing_mtime = seen_names[filename]

            # Priority scoring (lower is better)
            def priority_score(p: Path) -> int:
                path_str = str(p)
                if '/09-sessions/' in path_str:
                    return 1
                elif '/coditect-project-dot-claude/MEMORY-CONTEXT/' in path_str:
                    return 2
                elif '/MEMORY-CONTEXT/' in path_str and 'test-dataset' not in path_str:
                    return 3
                elif '/test-dataset/' in path_str:
                    return 4
                elif '/archive/' in path_str or '/99-archive/' in path_str:
                    return 5
                return 6

            if priority_score(file_path) < priority_score(existing_path):
                seen_names[filename] = (file_path, mtime)

    return list(seen_names.values())


def process_file(
    file_path: Path,
    file_mtime: datetime,
    file_type: str,
    global_hashes: Set[str],
    checkpoint_index: Dict
) -> Tuple[int, int, List[Dict]]:
    """Process single file (export or checkpoint)."""
    checkpoint_name = f"{file_type}-{file_path.stem}"

    # Check if already processed
    if checkpoint_name in checkpoint_index:
        print(f"⏭️  Skipping {file_path.name} (already processed)")
        return (0, 0, [])

    # Parse based on type
    if file_type == 'export':
        messages = parse_export_file(file_path)
    else:  # checkpoint
        messages = parse_checkpoint_file(file_path)

    if not messages:
        print(f"⚠️  No content found in {file_path.name}")
        return (0, 0, [])

    # Deduplicate
    new_unique_messages = []
    new_hashes = []

    for msg in messages:
        msg_hash = compute_hash(msg)
        if msg_hash not in global_hashes:
            global_hashes.add(msg_hash)
            new_hashes.append(msg_hash)
            new_unique_messages.append({
                'hash': msg_hash,
                'message': msg,
                'first_seen': file_mtime.isoformat(),
                'checkpoint': checkpoint_name,
                'source_file': str(file_path.relative_to(project_root))
            })

    total = len(messages)
    new = len(new_unique_messages)
    dups = total - new

    print(f"✅ {file_path.name}: {total} sections ({new} new, {dups} duplicates)")

    return (total, new, new_unique_messages)


def save_dedup_state(
    global_hashes: Set[str],
    new_unique_messages: List[Dict],
    checkpoint_index: Dict
):
    """Save updated deduplication state."""
    DEDUP_STATE_DIR.mkdir(parents=True, exist_ok=True)

    # Save global hashes
    with open(GLOBAL_HASHES_FILE, 'w') as f:
        json.dump(sorted(list(global_hashes)), f)

    # Append unique messages
    with open(UNIQUE_MESSAGES_FILE, 'a') as f:
        for msg_obj in new_unique_messages:
            f.write(json.dumps(msg_obj) + '\n')

    # Save checkpoint index
    with open(CHECKPOINT_INDEX_FILE, 'w') as f:
        json.dump(checkpoint_index, f, indent=2)


def main():
    """Main comprehensive consolidation workflow."""
    print("=" * 80)
    print("COMPREHENSIVE CONSOLIDATION: EXPORTS + CHECKPOINTS")
    print("=" * 80)
    print()

    # Find all files
    print("📂 Scanning for all content files...")
    all_files = find_all_content_files()

    print(f"   Found {len(all_files['exports'])} export files")
    print(f"   Found {len(all_files['checkpoints'])} checkpoint files")
    print()

    # Deduplicate by location
    print("🔍 Deduplicating by location (preferring originals)...")
    unique_exports = deduplicate_by_location(all_files['exports'])
    print(f"   Unique export files: {len(unique_exports)} (removed {len(all_files['exports']) - len(unique_exports)} copies)")
    print()

    # Load existing state
    print("📊 Loading existing deduplication state...")
    checkpoint_index = load_checkpoint_index()
    global_hashes = load_global_hashes()
    print(f"   Existing checkpoints: {len(checkpoint_index)}")
    print(f"   Existing unique messages: {len(global_hashes)}")
    print()

    # Process exports
    print("🔄 Processing export files...")
    print()

    total_messages = 0
    total_new = 0
    all_new_unique = []
    processed_count = 0

    for file_path, file_mtime in unique_exports:
        total, new, unique_msgs = process_file(
            file_path, file_mtime, 'export', global_hashes, checkpoint_index
        )

        if total > 0:
            total_messages += total
            total_new += new
            all_new_unique.extend(unique_msgs)

            checkpoint_name = f"export-{file_path.stem}"
            checkpoint_index[checkpoint_name] = {
                "created": datetime.utcnow().isoformat() + "Z",
                "message_hashes": [msg['hash'] for msg in unique_msgs],
                "source_file": str(file_path.relative_to(project_root)),
                "file_timestamp": file_mtime.isoformat(),
                "type": "export"
            }
            processed_count += 1

    print()
    print("🔄 Processing checkpoint files...")
    print()

    for file_path, file_mtime in all_files['checkpoints']:
        total, new, unique_msgs = process_file(
            file_path, file_mtime, 'checkpoint', global_hashes, checkpoint_index
        )

        if total > 0:
            total_messages += total
            total_new += new
            all_new_unique.extend(unique_msgs)

            checkpoint_name = f"checkpoint-{file_path.stem}"
            checkpoint_index[checkpoint_name] = {
                "created": datetime.utcnow().isoformat() + "Z",
                "message_hashes": [msg['hash'] for msg in unique_msgs],
                "source_file": str(file_path.relative_to(project_root)),
                "file_timestamp": file_mtime.isoformat(),
                "type": "checkpoint"
            }
            processed_count += 1

    print()
    print("=" * 80)
    print("COMPREHENSIVE SUMMARY")
    print("=" * 80)
    print(f"Files processed: {processed_count}")
    print(f"Total sections scanned: {total_messages}")
    print(f"New unique sections: {total_new}")
    print(f"Duplicates filtered: {total_messages - total_new}")
    print(f"Total unique messages in database: {len(global_hashes)}")
    print()

    if processed_count == 0:
        print("✅ All content already processed!")
        return

    # Save state
    print("💾 Saving deduplication state...")
    save_dedup_state(global_hashes, all_new_unique, checkpoint_index)
    print("   ✅ State saved")
    print()

    print("📝 Commit to git with:")
    print()
    print(f"   git add {DEDUP_STATE_DIR.relative_to(project_root)}")
    print(f"   git commit -m \"Comprehensive consolidation: {processed_count} files, {total_new} new unique messages\"")
    print()


if __name__ == "__main__":
    main()
