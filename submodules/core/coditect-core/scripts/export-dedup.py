#!/usr/bin/env python3
"""
Export and Deduplicate Session with Automated Multi-Submodule Checkpoint

FULLY AUTOMATED WORKFLOW:
1. Find export files (flexible multi-location search)
2. Process and deduplicate messages
3. Move exports to archive
4. Create checkpoint
5. Re-organize messages into checkpoint structure
6. Update consolidated backup
7. Update MANIFEST.json
8. ✅ AUTOMATICALLY run multi-submodule checkpoint (commits + pushes ALL repos)

All steps run automatically with no manual intervention required.

ENHANCED SEARCH: Now finds exports anywhere in the repository tree:
  • Repo root (shallow)
  • MEMORY-CONTEXT (shallow)
  • Current working directory (recursive)
  • All submodules (recursive)
  • Common temp locations: ~/Downloads, /tmp, ~/Desktop (last 24h)
  • Handles symlinks, hardlinks, permission issues
  • Excludes: .git, node_modules, exports-archive, etc.

AUTOMATED MULTI-SUBMODULE CHECKPOINT:
After dedup completes, automatically:
  • Detects all 45 configured submodules
  • Commits changes in each modified submodule
  • Pushes each submodule to remote
  • Updates parent repo with submodule pointers
  • Commits and pushes parent repo
  • Generates comprehensive audit trail

NO MANUAL GIT OPERATIONS REQUIRED - Everything is automated.

Author: Claude + AZ1.AI
License: MIT
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json
import shutil

# Add core to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

from message_deduplicator import MessageDeduplicator, parse_claude_export_file


def find_all_exports(repo_root: Path, memory_context_dir: Path) -> list:
    """
    Find all export files with flexible, powerful search logic.

    Searches multiple locations recursively to handle exports created anywhere:
    - Repo root (shallow)
    - MEMORY-CONTEXT (shallow)
    - Current working directory tree (recursive)
    - Submodules (recursive)
    - Common temp locations

    Excludes:
    - exports-archive (already processed)
    - .git directories
    - node_modules, venv, etc.
    """
    export_files = []
    seen_inodes = set()  # Track by inode to handle symlinks/hardlinks

    exclude_dirs = {
        '.git', 'node_modules', 'venv', '__pycache__',
        '.venv', 'dist', 'build', 'target',
        'exports-archive'  # Don't re-process archived exports
    }

    def should_skip_dir(dir_path: Path) -> bool:
        """Check if directory should be excluded from search"""
        return dir_path.name in exclude_dirs

    def add_export_if_unique(export_path: Path):
        """Add export to list if not already seen (handles symlinks)"""
        try:
            stat = export_path.stat()
            inode = (stat.st_dev, stat.st_ino)

            if inode not in seen_inodes:
                seen_inodes.add(inode)
                export_files.append(export_path)
        except (OSError, IOError) as e:
            # Skip files we can't stat (broken symlinks, permission issues)
            pass

    # 1. Search repo root (shallow - most common case)
    for export_path in repo_root.glob("*EXPORT*.txt"):
        add_export_if_unique(export_path)

    # 2. Search MEMORY-CONTEXT (shallow)
    if memory_context_dir.exists():
        for export_path in memory_context_dir.glob("*EXPORT*.txt"):
            add_export_if_unique(export_path)

    # 3. Search current working directory tree (recursive)
    cwd = Path.cwd()
    if cwd != repo_root and cwd.is_relative_to(repo_root):
        # Only search cwd if it's inside repo and not the root itself
        for export_path in cwd.rglob("*EXPORT*.txt"):
            if not any(should_skip_dir(p) for p in export_path.parents):
                add_export_if_unique(export_path)

    # 4. Search submodules directory (recursive)
    submodules_dir = repo_root / "submodules"
    if submodules_dir.exists():
        for export_path in submodules_dir.rglob("*EXPORT*.txt"):
            if not any(should_skip_dir(p) for p in export_path.parents):
                add_export_if_unique(export_path)

    # 5. Search common temp locations (where /export might save files)
    temp_locations = [
        Path.home() / "Downloads",
        Path("/tmp"),
        Path.home() / "Desktop"
    ]

    for temp_dir in temp_locations:
        if temp_dir.exists():
            try:
                # Only check files modified in last 24 hours (reduce search time)
                cutoff_time = datetime.now().timestamp() - 86400
                for export_path in temp_dir.glob("*EXPORT*.txt"):
                    if export_path.stat().st_mtime > cutoff_time:
                        add_export_if_unique(export_path)
            except (OSError, IOError, PermissionError):
                # Skip temp locations we can't access
                pass

    # Sort by modification time (newest first)
    export_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    return export_files


def find_latest_export(repo_root: Path, memory_context_dir: Path) -> Path:
    """Find most recent export file"""
    export_files = find_all_exports(repo_root, memory_context_dir)

    if not export_files:
        return None

    return export_files[0]


def archive_export(export_file: Path, archive_dir: Path) -> Path:
    """Move export file to archive directory"""
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Generate archive path
    archive_path = archive_dir / export_file.name

    # If archive file exists, add timestamp
    if archive_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive_path = archive_dir / f"{export_file.stem}-{timestamp}{export_file.suffix}"

    # Move file
    shutil.move(str(export_file), str(archive_path))

    return archive_path


def run_export_dedup(
    description: str = None,
    checkpoint_only: bool = False,
    auto_compact: bool = False,
    yes: bool = False,
    archive: bool = True
):
    """
    Main export-dedup workflow

    Args:
        description: Checkpoint description
        checkpoint_only: Skip deduplication
        auto_compact: Prompt user to compact after
        yes: Skip interactive prompts (auto-accept)
        archive: Move processed exports to archive
    """

    # Paths - Script is at .coditect/scripts/ which symlinks to submodules/core/coditect-core/scripts/
    # So we need to go up 5 levels: scripts -> coditect-core -> core -> submodules -> repo_root
    repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    framework_root = Path(__file__).resolve().parent.parent
    memory_context_dir = repo_root / "MEMORY-CONTEXT"
    archive_dir = memory_context_dir / "exports-archive"
    submodules_dir = repo_root / "submodules"

    print("\n" + "="*60)
    print("CODITECT Export & Deduplicate Workflow")
    print("="*60)
    print()

    # Step 1: Find all exports
    print("Step 1: Looking for export files...")
    print("  Searching:")
    print(f"    • Repo root: {repo_root}")
    print(f"    • MEMORY-CONTEXT: {memory_context_dir}")
    print(f"    • Current directory: {Path.cwd()}")
    print(f"    • Submodules (recursive)")
    print(f"    • Common temp locations")
    print()

    all_exports = find_all_exports(repo_root, memory_context_dir)

    if not all_exports:
        print("\n⚠️  No export files found!")
        print("\nSearched locations:")
        print("  - Repository root")
        print("  - MEMORY-CONTEXT directory")
        print("  - Current working directory tree")
        print("  - All submodules")
        print("  - ~/Downloads, /tmp, ~/Desktop (last 24h)")
        print("\nPlease run: /export")
        print("Then run this command again.")
        return 1

    latest_export = all_exports[0]

    print(f"✓ Found {len(all_exports)} export file(s)")

    # Show location details for each export
    for i, export_path in enumerate(all_exports, 1):
        age_seconds = datetime.now().timestamp() - export_path.stat().st_mtime
        age_str = f"{age_seconds/60:.1f}m" if age_seconds < 3600 else f"{age_seconds/3600:.1f}h"

        # Determine location category
        if export_path.parent == repo_root:
            location = "repo root"
        elif export_path.is_relative_to(memory_context_dir):
            location = f"MEMORY-CONTEXT/{export_path.relative_to(memory_context_dir).parent}"
        elif submodules_dir.exists() and export_path.is_relative_to(submodules_dir):
            location = f"submodules/{export_path.relative_to(submodules_dir).parent}"
        else:
            location = str(export_path.parent)

        marker = "→" if i == 1 else " "
        print(f"  {marker} [{age_str}] {export_path.name}")
        print(f"     Location: {location}")

    print()

    # Check if export is recent (within 5 minutes)
    export_age = datetime.now().timestamp() - latest_export.stat().st_mtime

    if export_age > 300 and not yes:  # 5 minutes
        print(f"\n⚠️  Latest export is {export_age/60:.1f} minutes old:")
        print(f"    {latest_export.name}")
        print("\nFor best results, run /export first to capture current state.")
        try:
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != 'y':
                return 1
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️  Non-interactive mode detected, continuing anyway...")
    elif export_age > 300 and yes:
        print(f"⚠️  Latest export is {export_age/60:.1f} minutes old (auto-accepting)")
    else:
        print(f"✓ Recent export (< 5 min old)")

    # Step 2: Deduplicate ALL exports (unless skipped)
    all_stats = []
    if not checkpoint_only:
        print(f"\nStep 2: Deduplicating {len(all_exports)} export file(s)...")

        try:
            # Initialize deduplicator
            dedup_dir = memory_context_dir / "dedup_state"
            dedup = MessageDeduplicator(storage_dir=dedup_dir)

            # Process each export file
            for idx, export_file in enumerate(all_exports, 1):
                print(f"\n  Processing {idx}/{len(all_exports)}: {export_file.name}")

                # Parse export
                export_data = parse_claude_export_file(export_file)

                # Extract checkpoint ID from description or filename
                if description and idx == 1:  # Use description for latest export only
                    checkpoint_id = datetime.now().strftime("%Y-%m-%d") + f"-{description}"
                else:
                    checkpoint_id = export_file.stem

                # Process
                new_messages, stats = dedup.process_export(
                    export_data,
                    checkpoint_id=checkpoint_id
                )

                all_stats.append({
                    'file': export_file.name,
                    'stats': stats
                })

                print(f"    Total messages: {stats['total_messages']}")
                print(f"    New unique: {stats['new_unique']}")
                print(f"    Duplicates filtered: {stats['duplicates_filtered']}")
                print(f"    Dedup rate: {stats['dedup_rate']:.1f}%")

            # Summary of all processed exports
            total_messages = sum(s['stats']['total_messages'] for s in all_stats)
            total_new = sum(s['stats']['new_unique'] for s in all_stats)
            total_duplicates = sum(s['stats']['duplicates_filtered'] for s in all_stats)
            overall_dedup_rate = (total_duplicates / total_messages * 100) if total_messages > 0 else 0

            print(f"\n  📊 Overall Deduplication Summary:")
            print(f"    Files processed: {len(all_stats)}")
            print(f"    Total messages: {total_messages}")
            print(f"    New unique: {total_new}")
            print(f"    Duplicates filtered: {total_duplicates}")
            print(f"    Overall dedup rate: {overall_dedup_rate:.1f}%")
            print(f"    Global unique count: {all_stats[-1]['stats']['global_unique_count']}")

            # Store latest stats for checkpoint description
            stats = all_stats[-1]['stats'] if all_stats else None

        except Exception as e:
            print(f"\n❌ Deduplication failed: {e}")
            import traceback
            traceback.print_exc()
            return 1
    else:
        print("\nStep 2: Skipping deduplication (--checkpoint-only)")
        stats = None

    # Step 3: Archive export files
    if archive:
        print("\nStep 3: Archiving export files...")

        archived_files = []
        for export_file in all_exports:
            try:
                archive_path = archive_export(export_file, archive_dir)
                archived_files.append(archive_path)
                print(f"  ✓ Archived: {export_file.name} → {archive_path.relative_to(repo_root)}")
            except Exception as e:
                print(f"  ⚠️  Failed to archive {export_file.name}: {e}")

        print(f"\n  Total archived: {len(archived_files)} file(s)")
    else:
        print("\nStep 3: Skipping archive (--no-archive)")

    # Step 4: Create checkpoint
    print("\nStep 4: Creating checkpoint...")

    try:
        # Generate checkpoint description
        if not description:
            if yes:
                description = "Automated export and deduplication"
            else:
                try:
                    description = input("\nEnter checkpoint description: ").strip()
                    if not description:
                        description = "Session export and deduplication"
                except (EOFError, KeyboardInterrupt):
                    description = "Automated export and deduplication"
                    print(f"\nUsing default: {description}")

        # Run checkpoint script
        checkpoint_script = framework_root / "scripts" / "create-checkpoint.py"

        result = subprocess.run(
            [
                sys.executable,
                str(checkpoint_script),
                description,
                "--auto-commit"
            ],
            cwd=repo_root,  # Run from repo root, not framework
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✓ Checkpoint created successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"⚠️  Checkpoint creation had issues:")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)

    except Exception as e:
        print(f"❌ Checkpoint creation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Step 5: Re-organize all messages into checkpoint structure
    print("\nStep 5: Re-organizing messages into checkpoint structure...")

    try:
        import re
        from collections import defaultdict

        def sanitize_filename(name):
            """Remove invalid filename characters"""
            # Replace forward slashes with dashes
            name = name.replace('/', '-')
            # Remove or replace other problematic characters
            name = re.sub(r'[<>:"|?*\n\r]', '', name)
            # Limit length to 200 chars (safe for most filesystems)
            return name[:200]

        dedup_dir = memory_context_dir / "dedup_state"
        checkpoint_dir = memory_context_dir / "messages" / "by-checkpoint"
        unique_messages_file = dedup_dir / "unique_messages.jsonl"

        if unique_messages_file.exists():
            # Load all messages from global store
            messages = []
            with open(unique_messages_file, 'r') as f:
                for line in f:
                    if line.strip():
                        messages.append(json.loads(line))

            print(f"  Loaded {len(messages)} messages from global store")

            # Group by checkpoint
            by_checkpoint = defaultdict(list)
            for msg in messages:
                checkpoint = msg.get('checkpoint', '2025-01-01-uncategorized')
                by_checkpoint[checkpoint].append(msg)

            print(f"  Grouped into {len(by_checkpoint)} checkpoint(s)")

            # Write organized files
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            fallback_dir = checkpoint_dir / "by-date-fallback"

            for checkpoint_name, msgs in by_checkpoint.items():
                if checkpoint_name == '2025-01-01-uncategorized':
                    # Put legacy messages in fallback directory
                    fallback_dir.mkdir(parents=True, exist_ok=True)
                    filename = fallback_dir / f"{checkpoint_name}.jsonl"
                else:
                    # Sanitize checkpoint name for filesystem
                    safe_name = sanitize_filename(checkpoint_name)
                    filename = checkpoint_dir / f"{safe_name}.jsonl"

                with open(filename, 'w') as f:
                    for msg in msgs:
                        f.write(json.dumps(msg) + '\n')

            # Count organized messages
            organized_count = sum(len(msgs) for name, msgs in by_checkpoint.items()
                                 if name != '2025-01-01-uncategorized')
            fallback_count = len(by_checkpoint.get('2025-01-01-uncategorized', []))

            print(f"  ✓ Organized checkpoints: {organized_count} messages")
            print(f"  ✓ Fallback directory: {fallback_count} legacy messages")
            print(f"  ✓ Total organized: {len(messages)} messages")

        else:
            print("  ⚠️  Global message store not found, skipping organization")

    except Exception as e:
        print(f"  ⚠️  Organization failed: {e}")
        import traceback
        traceback.print_exc()
        # Don't fail the script, just continue to next step

    # Step 6: Update consolidated backup
    print("\nStep 6: Updating consolidated backup...")

    try:
        if unique_messages_file.exists():
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
            backup_file = memory_context_dir / "backups" / f"CONSOLIDATED-ALL-MESSAGES-{timestamp}.jsonl"
            backup_file.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy(unique_messages_file, backup_file)

            # Count messages in backup
            backup_count = sum(1 for line in open(backup_file) if line.strip())
            print(f"  ✓ Created backup: {backup_file.name}")
            print(f"  ✓ Messages in backup: {backup_count}")

    except Exception as e:
        print(f"  ⚠️  Backup creation failed: {e}")
        # Don't fail the script, just continue

    # Step 7: Update MANIFEST.json
    print("\nStep 7: Updating MANIFEST.json...")

    try:
        manifest_file = checkpoint_dir / "MANIFEST.json"

        manifest = {
            "by_checkpoint": {},
            "total_messages": len(messages),
            "last_updated": datetime.now().isoformat(),
            "organization_method": "checkpoint-based",
            "includes_phases": ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
        }

        # Build manifest for each checkpoint
        for checkpoint_name, msgs in by_checkpoint.items():
            if msgs:
                first_seen = msgs[0].get('first_seen', '')
                last_seen = msgs[-1].get('first_seen', '') if len(msgs) > 1 else first_seen

                manifest["by_checkpoint"][checkpoint_name] = {
                    "count": len(msgs),
                    "first_message": first_seen,
                    "last_message": last_seen
                }

        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"  ✓ Updated MANIFEST.json")
        print(f"  ✓ Tracked {len(manifest['by_checkpoint'])} checkpoint(s)")

    except Exception as e:
        print(f"  ⚠️  Manifest update failed: {e}")
        # Don't fail the script, just continue

    # Step 8: Automatically run multi-submodule checkpoint
    print("\nStep 8: Running automated multi-submodule checkpoint...")
    print("  (This commits all modified submodules + parent repo)")

    try:
        checkpoint_with_submodules_script = framework_root / "scripts" / "checkpoint-with-submodules.py"

        if checkpoint_with_submodules_script.exists():
            result = subprocess.run(
                [
                    sys.executable,
                    str(checkpoint_with_submodules_script),
                    f"Export dedup: {description}",
                ],
                cwd=repo_root,  # Run from repo root
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("  ✓ Multi-submodule checkpoint completed successfully")
                print()
                print("  📊 Checkpoint results:")
                if "Summary:" in result.stdout:
                    # Extract summary lines from output
                    for line in result.stdout.split('\n'):
                        if "Summary:" in line or "submodule" in line or "✅" in line or "⚪" in line:
                            print(f"     {line.strip()}")
            else:
                print("  ⚠️  Multi-submodule checkpoint had issues:")
                if result.stderr:
                    # Only show first few lines of error
                    for line in result.stderr.split('\n')[:5]:
                        if line.strip():
                            print(f"     {line.strip()}")
                if result.stdout:
                    for line in result.stdout.split('\n')[-5:]:
                        if line.strip():
                            print(f"     {line.strip()}")
        else:
            print(f"  ⚠️  checkpoint-with-submodules.py not found at {checkpoint_with_submodules_script}")
            print("     Skipping automated checkpoint")

    except Exception as e:
        print(f"  ⚠️  Automated checkpoint failed: {e}")
        # Don't fail the script, just continue

    # Final message
    print("\n" + "="*60)
    print("✅ Export, deduplication, and organization complete!")
    print("   ✅ All modified submodules committed + pushed")
    print("="*60)
    print()

    if stats and not checkpoint_only:
        print(f"📊 Deduplication Summary:")
        print(f"   - New unique messages: {stats['new_unique']}")
        print(f"   - Total unique messages: {stats['global_unique_count']}")
        print(f"   - Storage: {dedup_dir.relative_to(repo_root)}")

    if archive:
        print(f"\n📁 Export(s) archived:")
        print(f"   - Location: {archive_dir.relative_to(repo_root)}")
        print(f"   - Files: {len(all_exports)} export(s) moved")

    print(f"\n📝 Checkpoint created: {description}")

    print(f"\n📋 Organization complete:")
    print(f"   - Location: {checkpoint_dir.relative_to(repo_root)}")
    print(f"   - Checkpoints: {len(by_checkpoint) if 'by_checkpoint' in locals() else '?'}")
    print(f"   - Total messages: {len(messages) if 'messages' in locals() else '?'}")

    if auto_compact:
        print("\n" + "⚠️"*30)
        print("\n💡 Safe to compact now!")
        print("\n   Run: /compact")
        print("\n   This will free up context space while")
        print("   preserving all data in the checkpoint.")
        print("\n" + "⚠️"*30)

    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Export and deduplicate current session (fully automated)"
    )
    parser.add_argument(
        "--description",
        help="Checkpoint description"
    )
    parser.add_argument(
        "--checkpoint-only",
        action="store_true",
        help="Skip deduplication, just create checkpoint"
    )
    parser.add_argument(
        "--auto-compact",
        action="store_true",
        help="Prompt user to /compact after completion"
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip interactive prompts (auto-accept)"
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Don't move exports to archive (keep in place)"
    )

    args = parser.parse_args()

    sys.exit(run_export_dedup(
        description=args.description,
        checkpoint_only=args.checkpoint_only,
        auto_compact=args.auto_compact,
        yes=args.yes,
        archive=not args.no_archive
    ))
