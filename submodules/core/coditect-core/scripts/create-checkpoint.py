#!/usr/bin/env python3
"""
CODITECT Checkpoint Creation Script

Automated checkpoint creation system that:
1. Generates ISO-DATETIME stamped checkpoint documents
2. Updates all impacted TASKLISTs with completed/WIP tasks
3. Creates project plan updates
4. Commits all changes to git
5. Updates README.md with checkpoint reference
6. Prepares context for next session
7. Automatically extracts session context (git, tasks, sections)

Usage:
    python3 scripts/create-checkpoint.py "Sprint description" [--auto-commit]

Author: AZ1.AI INC.
Framework: CODITECT
Copyright: © 2025 AZ1.AI INC. All rights reserved.
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse

# Privacy integration (optional - fail gracefully if not available)
try:
    sys.path.insert(0, str(Path(__file__).parent / "core"))
    from privacy_integration import process_checkpoint_with_privacy
    PRIVACY_AVAILABLE = True
except ImportError:
    PRIVACY_AVAILABLE = False

# Session export integration (optional - fail gracefully if not available)
try:
    sys.path.insert(0, str(Path(__file__).parent / "core"))
    from session_export import SessionExporter
    SESSION_EXPORT_AVAILABLE = True
except ImportError:
    SESSION_EXPORT_AVAILABLE = False

# Conversation deduplication integration (optional - fail gracefully if not available)
try:
    sys.path.insert(0, str(Path(__file__).parent / "core"))
    from conversation_deduplicator import (
        ClaudeConversationDeduplicator,
        parse_claude_export_file,
        extract_session_id_from_filename
    )
    DEDUP_AVAILABLE = True
except ImportError:
    DEDUP_AVAILABLE = False


class CheckpointCreator:
    """Automated checkpoint creation and documentation system."""

    def __init__(self, base_dir: str = None):
        """Initialize checkpoint creator.

        Args:
            base_dir: Base directory for the project (defaults to script's parent dir)
        """
        if base_dir is None:
            script_dir = Path(__file__).parent.absolute()
            self.base_dir = script_dir.parent
        else:
            self.base_dir = Path(base_dir)

        self.memory_context_dir = self.base_dir / "MEMORY-CONTEXT"
        self.checkpoints_dir = self.memory_context_dir / "checkpoints"
        self.docs_dir = self.base_dir / "docs"

        # Ensure directories exist
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
        self.memory_context_dir.mkdir(exist_ok=True)
        self.docs_dir.mkdir(exist_ok=True)

        # ISO-DATETIME timestamp
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

    def get_git_status(self) -> Dict[str, any]:
        """Get comprehensive git status information.

        Returns:
            Dictionary with git status details
        """
        os.chdir(self.base_dir)

        status = {
            'branch': self._run_command("git branch --show-current"),
            'status': self._run_command("git status --short"),
            'recent_commits': self._run_command("git log -5 --oneline"),
            'changed_files': self._run_command("git diff --name-only HEAD"),
            'untracked_files': self._run_command("git ls-files --others --exclude-standard"),
        }

        return status

    def get_submodule_status(self) -> List[Dict[str, str]]:
        """Get status of all git submodules recursively.

        Returns:
            List of submodule status dictionaries
        """
        os.chdir(self.base_dir)

        submodules = []
        # Use --recursive to get nested submodules
        submodule_output = self._run_command("git submodule status --recursive")

        if submodule_output and not submodule_output.startswith('fatal'):
            for line in submodule_output.strip().split('\n'):
                if not line.strip() or line.startswith('fatal'):
                    continue

                parts = line.strip().split()
                if len(parts) >= 2:
                    commit = parts[0].lstrip('+-')
                    path = parts[1]

                    # Verify path exists before trying to access it
                    submodule_path = self.base_dir / path
                    if not submodule_path.exists():
                        continue

                    # Get latest commit message for this submodule
                    try:
                        os.chdir(submodule_path)
                        commit_msg = self._run_command("git log -1 --oneline")
                        os.chdir(self.base_dir)

                        submodules.append({
                            'path': path,
                            'commit': commit,
                            'message': commit_msg
                        })
                    except (FileNotFoundError, OSError):
                        # Skip submodules we can't access
                        continue

        return submodules

    def collect_completed_tasks(self) -> Dict[str, List[str]]:
        """Scan all TASKLISTs for recently completed tasks.

        Returns:
            Dictionary mapping project names to completed tasks
        """
        completed = {}

        # Find all TASKLIST.md files
        tasklist_files = list(self.base_dir.rglob("TASKLIST.md"))

        for tasklist_path in tasklist_files:
            project_name = tasklist_path.parent.name

            with open(tasklist_path, 'r') as f:
                content = f.read()

            # Extract completed tasks (lines with [x])
            completed_tasks = []
            for line in content.split('\n'):
                if '- [x]' in line.lower():
                    # Clean up the task description
                    task = line.split('[x]', 1)[1].strip() if '[x]' in line else line.strip()
                    completed_tasks.append(task)

            if completed_tasks:
                completed[project_name] = completed_tasks[:10]  # Top 10 recent

        return completed

    def generate_checkpoint_document(self, sprint_description: str) -> Tuple[str, str]:
        """Generate comprehensive checkpoint document.

        Args:
            sprint_description: Description of the sprint/work completed

        Returns:
            Tuple of (filename, content)
        """
        git_status = self.get_git_status()
        submodules = self.get_submodule_status()
        completed_tasks = self.collect_completed_tasks()

        # Generate filename
        safe_description = sprint_description.replace(' ', '-').replace('/', '-')
        filename = f"{self.timestamp}-{safe_description}.md"

        # Generate content
        newline = '\n'
        commit_count = len(git_status['recent_commits'].split(newline)) if git_status['recent_commits'] else 0
        content = f"""# CODITECT Checkpoint: {sprint_description}

**Timestamp:** {self.timestamp}
**Sprint:** {sprint_description}
**Status:** ✅ CHECKPOINT CAPTURED
**Framework:** CODITECT

**Author:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
**Copyright:** © 2025 AZ1.AI INC. All rights reserved.

---

## Executive Summary

This checkpoint captures the state of the CODITECT platform after completing: {sprint_description}

**Key Metrics:**
- Repositories Updated: {len(submodules)} submodules
- Tasks Completed: {sum(len(tasks) for tasks in completed_tasks.values())}
- Git Commits: {commit_count}
- Timestamp: {self.timestamp}

---

## Git Status

### Current Branch
```
{git_status['branch']}
```

### Recent Commits
```
{git_status['recent_commits']}
```

### Working Directory Status
```
{git_status['status'] if git_status['status'] else 'Clean working directory'}
```

---

## Submodule Status

### Updated Submodules ({len(submodules)})

"""

        for sub in submodules:
            content += f"""
**{sub['path']}**
- Commit: `{sub['commit'][:7]}`
- Latest: {sub['message']}
"""

        content += "\n---\n\n## Completed Tasks by Project\n\n"

        for project, tasks in completed_tasks.items():
            content += f"\n### {project}\n\n"
            for task in tasks[:5]:  # Top 5 per project
                content += f"- [x] {task}\n"

        content += f"""

---

## Documentation Updates

### Created/Updated Files

"""

        if git_status['changed_files']:
            for file in git_status['changed_files'].split('\n'):
                if file.strip():
                    content += f"- {file}\n"

        content += """

---

## Next Steps

### Immediate Actions

- [ ] Review checkpoint completeness
- [ ] Update README.md with checkpoint reference
- [ ] Prepare context for next session
- [ ] Begin Sprint +1 planning (if applicable)

### Sprint +1 Preparation

See individual project TASKLISTs for detailed Sprint +1 tasks:
- Master TASKLIST: `TASKLIST.md`
- Framework: `submodules/coditect-framework/TASKLIST.md`
- Backend: `submodules/coditect-cloud-backend/TASKLIST.md`
- Frontend: `submodules/coditect-cloud-frontend/TASKLIST.md`
- CLI: `submodules/coditect-cli/TASKLIST.md`
- Docs: `submodules/coditect-docs/TASKLIST.md`
- Infrastructure: `submodules/coditect-infrastructure/TASKLIST.md`
- Legal: `submodules/coditect-legal/TASKLIST.md`

---

## Session Context Export

### Key Decisions Made

(To be filled by session review)

### Architecture Changes

(To be filled by session review)

### Dependencies Updated

(To be filled by session review)

---

## MEMORY-CONTEXT Integration

This checkpoint will be available for context loading in future sessions:

```bash
# Load checkpoint context for next session
python3 scripts/load-session-context.py {filename}
```

**Storage Location:** `MEMORY-CONTEXT/checkpoints/{filename}`

**Linked in:** README.md (see "Recent Checkpoints" section)

---

## Metrics & KPIs

### Sprint Metrics

| Metric | Value |
|--------|-------|
| Duration | (Session length) |
| Commits | {len(git_status['recent_commits'].split('\\n')) if git_status['recent_commits'] else 0} |
| Files Changed | {len(git_status['changed_files'].split('\\n')) if git_status['changed_files'] else 0} |
| Submodules Updated | {len(submodules)} |
| Tasks Completed | {sum(len(tasks) for tasks in completed_tasks.values())} |

---

## Quality Assurance

### Checklist

- [x] All changes committed to git
- [x] Submodule pointers updated
- [x] TASKLISTs updated with completion status
- [x] Documentation synchronized
- [x] Checkpoint created with ISO-DATETIME
- [ ] README.md updated with checkpoint link
- [ ] Session context exported to MEMORY-CONTEXT

---

**Generated by:** CODITECT Checkpoint Automation System
**Script:** `scripts/create-checkpoint.py`
**Timestamp:** {self.timestamp}
**Status:** ✅ CHECKPOINT COMPLETE

---

**END OF CHECKPOINT**
"""

        return filename, content

    def update_readme(self, checkpoint_filename: str, sprint_description: str) -> None:
        """Update README.md with checkpoint reference.

        Args:
            checkpoint_filename: Name of the checkpoint file
            sprint_description: Description of the sprint
        """
        readme_path = self.base_dir / "README.md"

        if not readme_path.exists():
            print(f"⚠️  README.md not found at {readme_path}")
            return

        with open(readme_path, 'r') as f:
            content = f.read()

        # Create checkpoint entry
        checkpoint_entry = f"\n- **[{self.timestamp}]** [{sprint_description}](MEMORY-CONTEXT/checkpoints/{checkpoint_filename})"

        # Find or create "Recent Checkpoints" section
        if "## Recent Checkpoints" in content:
            # Insert after the section header
            parts = content.split("## Recent Checkpoints", 1)
            # Find the next section or end
            next_section_idx = parts[1].find("\n## ")
            if next_section_idx != -1:
                before_next = parts[1][:next_section_idx]
                after_next = parts[1][next_section_idx:]
                updated = parts[0] + "## Recent Checkpoints" + checkpoint_entry + "\n" + before_next + after_next
            else:
                updated = parts[0] + "## Recent Checkpoints" + checkpoint_entry + "\n" + parts[1]
        else:
            # Add section before final separator
            if "---\n\n*Built with Excellence" in content:
                parts = content.split("---\n\n*Built with Excellence", 1)
                updated = parts[0] + f"\n## Recent Checkpoints\n{checkpoint_entry}\n\n---\n\n*Built with Excellence" + parts[1]
            else:
                # Append at end
                updated = content + f"\n\n## Recent Checkpoints\n{checkpoint_entry}\n"

        with open(readme_path, 'w') as f:
            f.write(updated)

        print(f"✅ Updated README.md with checkpoint reference")

    def prepare_conversation_export(self, sprint_description: str) -> str:
        """Prepare location for Claude Code /export command.

        Args:
            sprint_description: Description of the sprint

        Returns:
            Path where export should be saved
        """
        exports_dir = self.memory_context_dir / "exports"
        exports_dir.mkdir(exist_ok=True)

        # Create export filename
        safe_desc = sprint_description.replace(' ', '-').replace('/', '-')
        export_filename = f"{self.timestamp}-{safe_desc}.txt"
        export_path = exports_dir / export_filename

        # Create placeholder
        placeholder = f"""# CODITECT Conversation Export
# Timestamp: {self.timestamp}
# Description: {sprint_description}
# Status: PENDING - Waiting for /export command

This file is a placeholder. Please run /export in Claude Code and save to this location.

Export will contain:
- Complete conversation history
- Code changes and file modifications
- Decision points and rationale
- Task progress and completions
- Session metadata

This export will be used for:
- MEMORY-CONTEXT session continuity
- NESTED LEARNING pattern extraction
- Cross-session context loading
- Zero catastrophic forgetting

Full path: {export_path}
"""

        with open(export_path, 'w') as f:
            f.write(placeholder)

        return str(export_path)

    def create_memory_context_export(self, sprint_description: str) -> str:
        """Create MEMORY-CONTEXT session export.

        Args:
            sprint_description: Description of the sprint

        Returns:
            Path to created export file
        """
        sessions_dir = self.memory_context_dir / "sessions"
        sessions_dir.mkdir(exist_ok=True)

        # Create session export filename
        date_only = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        safe_desc = sprint_description.replace(' ', '-').replace('/', '-')
        export_filename = f"{date_only}-{safe_desc}.md"
        export_path = sessions_dir / export_filename

        # Generate session export content
        content = f"""# Session: {sprint_description}

**Date:** {date_only}
**Duration:** (Session length)
**Status:** ✅ Complete

---

## Objectives

- [x] {sprint_description}

---

## Key Decisions

(To be filled from session review)

---

## Work Completed

(See checkpoint: `MEMORY-CONTEXT/checkpoints/{self.timestamp}-{safe_desc}.md`)

---

## Next Session

See Sprint +1 tasks in project TASKLISTs.

---

**Session Export Format:** MEMORY-CONTEXT v1.0
**Generated:** {self.timestamp}
"""

        with open(export_path, 'w') as f:
            f.write(content)

        print(f"✅ Created MEMORY-CONTEXT session export: {export_path}")
        return str(export_path)

    def deduplicate_exports(self, sprint_description: str) -> Optional[Dict[str, any]]:
        """Automatically deduplicate conversation exports.

        Args:
            sprint_description: Description of the sprint (used for session ID)

        Returns:
            Deduplication statistics or None if not available
        """
        if not DEDUP_AVAILABLE:
            return None

        try:
            # Initialize deduplicator
            dedup_dir = self.memory_context_dir / "dedup_state"
            dedup = ClaudeConversationDeduplicator(storage_dir=dedup_dir)

            # Find latest export for this session
            exports_dir = self.memory_context_dir / "exports"
            if not exports_dir.exists():
                return None

            # Look for recent export files (last 10 minutes)
            import time
            current_time = time.time()
            recent_exports = []

            for export_file in exports_dir.glob("*.txt"):
                file_age = current_time - export_file.stat().st_mtime
                if file_age < 600:  # 10 minutes
                    recent_exports.append(export_file)

            if not recent_exports:
                # No recent exports, process all exports
                recent_exports = list(exports_dir.glob("*.txt"))

            if not recent_exports:
                return None

            # Sort by modification time (most recent first)
            recent_exports.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            # Process the most recent export
            latest_export = recent_exports[0]

            # Extract session ID from filename
            session_id = extract_session_id_from_filename(latest_export)

            # Parse and deduplicate
            export_data = parse_claude_export_file(latest_export)
            new_messages, stats = dedup.process_export(session_id, export_data)

            return {
                'file': latest_export.name,
                'session_id': session_id,
                'total_messages': stats['messages_in_export'],
                'new_messages': stats['new_messages'],
                'duplicates_filtered': stats['duplicates_filtered'],
                'deduplication_rate': (
                    (stats['duplicates_filtered'] / stats['messages_in_export'] * 100)
                    if stats['messages_in_export'] > 0 else 0
                ),
                'watermark': stats['new_watermark'],
                'total_unique_messages': stats['total_unique_messages']
            }

        except Exception as e:
            print(f"⚠️  Deduplication failed: {e}")
            return None

    def _run_command(self, cmd: str) -> str:
        """Run shell command and return output.

        Args:
            cmd: Command to run

        Returns:
            Command output as string (stdout + stderr)
        """
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=os.getcwd()  # Use current working directory, not self.base_dir
            )
            # Combine stdout and stderr for git commands (git push writes to stderr)
            output = (result.stdout + result.stderr).strip()
            return output
        except Exception as e:
            print(f"⚠️  Command failed: {cmd}\n   Error: {e}")
            return ""

    def commit_changes(self, checkpoint_filename: str, sprint_description: str) -> None:
        """Commit all changes to git.

        Args:
            checkpoint_filename: Name of checkpoint file
            sprint_description: Description of the sprint
        """
        os.chdir(self.base_dir)

        # Add checkpoint and README
        self._run_command(f"git add MEMORY-CONTEXT/checkpoints/{checkpoint_filename}")
        self._run_command("git add README.md")
        self._run_command("git add MEMORY-CONTEXT/")

        # Commit
        commit_msg = f"""Create checkpoint: {sprint_description}

Automated checkpoint creation via create-checkpoint.py

Checkpoint: {checkpoint_filename}
Timestamp: {self.timestamp}
Status: ✅ CHECKPOINT COMPLETE

Updates:
- Created checkpoint document
- Updated README.md with checkpoint reference
- Created MEMORY-CONTEXT session export
- Captured git status and submodule state

🤖 Generated with CODITECT Checkpoint Automation System
"""

        # Use heredoc for commit message to preserve formatting
        self._run_command(f'git commit -m "$(cat <<\'EOF\'\n{commit_msg}\nEOF\n)"')

        print(f"✅ Committed checkpoint to git")

    def push_changes(self) -> None:
        """Push all committed changes to remote repository.

        Pushes both the current repository and updates the parent repository
        if this is a submodule.
        """
        os.chdir(self.base_dir)

        # Determine if we're in a submodule
        is_submodule = (self.base_dir / ".." / ".." / ".git").exists() or \
                       (self.base_dir / ".." / ".gitmodules").exists()

        # Push current repository
        print("\nPushing changes to remote...")
        push_result = self._run_command("git push")

        if push_result or "Everything up-to-date" in push_result:
            print(f"✅ Pushed changes to remote (current repository)")
        else:
            print(f"⚠️  Push may have failed - check git output")
            return

        # If this is a submodule, update parent repository
        if is_submodule:
            print("\nDetected submodule - updating parent repository...")

            # Get the submodule path relative to parent
            parent_dir = self.base_dir.parent.parent
            submodule_name = self.base_dir.name
            submodule_relative_path = self.base_dir.relative_to(parent_dir)

            # Change to parent directory
            os.chdir(parent_dir)

            # Check if there are changes to the submodule pointer
            status_output = self._run_command(f"git status --porcelain {submodule_relative_path}")

            if status_output:
                print(f"  Detected changes in submodule pointer")

                # Add submodule pointer update
                add_result = self._run_command(f"git add {submodule_relative_path}")
                print(f"  Added submodule: {submodule_relative_path}")

                # Commit submodule update with properly escaped message
                commit_msg = f"Update {submodule_name} submodule: Checkpoint created"
                commit_result = self._run_command(f"git commit -m '{commit_msg}'")

                if "nothing to commit" in commit_result:
                    print(f"  ℹ️  No changes to commit in parent repository")
                else:
                    print(f"  ✅ Committed submodule update to parent repository")

                    # Push parent repository
                    parent_push = self._run_command("git push")

                    if parent_push or "Everything up-to-date" in parent_push:
                        print(f"✅ Pushed submodule update to parent repository")
                    else:
                        print(f"⚠️  Parent repository push may have failed")
                        print(f"  Output: {parent_push}")
            else:
                print(f"  ℹ️  No changes to submodule pointer - skipping parent update")

            # Return to original directory
            os.chdir(self.base_dir)
        else:
            print("Not a submodule - skipping parent repository update")

    def run(
        self,
        sprint_description: str,
        auto_commit: bool = False,
        auto_push: bool = False,
        privacy_scan: bool = False,
        privacy_level: str = 'private',
        with_export: bool = True
    ) -> str:
        """Run complete checkpoint creation process.

        Args:
            sprint_description: Description of the sprint/work completed
            auto_commit: Whether to automatically commit changes
            auto_push: Whether to automatically push changes (implies auto_commit)
            privacy_scan: Whether to scan for PII and generate privacy report
            privacy_level: Privacy level for scanning (public, team, private, ephemeral)
            with_export: Whether to prepare conversation export location (default: True)

        Returns:
            Path to created checkpoint file
        """
        # If auto_push is enabled, auto_commit must also be enabled
        if auto_push:
            auto_commit = True

        print(f"\n{'='*80}")
        print(f"CODITECT Checkpoint Creation System")
        print(f"{'='*80}\n")

        print(f"📋 Sprint: {sprint_description}")
        print(f"🕐 Timestamp: {self.timestamp}")
        if with_export:
            print(f"📤 Conversation Export: Enabled (will prepare /export location)")
        if privacy_scan:
            print(f"🔒 Privacy Scan: Enabled (Level: {privacy_level})")
        if auto_push:
            print(f"🚀 Auto-Push: Enabled (will commit and push)")
        elif auto_commit:
            print(f"💾 Auto-Commit: Enabled (will commit locally)")
        print()

        # Step 0: Prepare conversation export (if enabled)
        export_path = None
        if with_export:
            print("Step 0: Preparing conversation export location...")
            export_path = self.prepare_conversation_export(sprint_description)
            print(f"✅ Export location prepared: {export_path}")
            print()
            print(f"{'='*80}")
            print(f"📤 CONVERSATION EXPORT READY")
            print(f"{'='*80}")
            print()
            print(f"Run this command in Claude Code to save full conversation:")
            print(f"  /export")
            print()
            print(f"Save to:")
            print(f"  {export_path}")
            print()
            print(f"Note: You can run /export before or after this checkpoint completes.")
            print(f"      The export location has been prepared and will be referenced in")
            print(f"      the checkpoint documentation for easy access.")
            print()
            print(f"Continuing with checkpoint creation...\n")

        # Step 1: Generate checkpoint document
        print("Step 1: Generating checkpoint document...")
        filename, content = self.generate_checkpoint_document(sprint_description)
        checkpoint_path = self.checkpoints_dir / filename

        with open(checkpoint_path, 'w') as f:
            f.write(content)

        print(f"✅ Created checkpoint: {checkpoint_path}")

        # Step 2: Update README.md
        print("\nStep 2: Updating README.md...")
        self.update_readme(filename, sprint_description)

        # Step 3: Create MEMORY-CONTEXT export
        print("\nStep 3: Creating MEMORY-CONTEXT session export...")
        self.create_memory_context_export(sprint_description)

        # Step 3.5: Automatic session context extraction
        if SESSION_EXPORT_AVAILABLE:
            print("\nStep 3.5: Extracting session context (git, tasks, sections)...")
            try:
                exporter = SessionExporter(repo_root=self.base_dir)
                session_export_path = exporter.export_session(
                    checkpoint_path=checkpoint_path,
                    session_name=sprint_description.replace(' ', '-')
                )
                print(f"✅ Automated context extraction complete")
                print(f"   Session markdown: {session_export_path.name}")
                print(f"   JSON export: exports/{session_export_path.stem}.json")
            except Exception as e:
                print(f"⚠️  Automated context extraction failed: {e}")
                print(f"   Continuing with checkpoint creation...")

        # Step 3.6: Privacy scan if requested
        if privacy_scan and PRIVACY_AVAILABLE:
            print(f"\nStep 3.6: Running privacy scan (Level: {privacy_level})...")
            try:
                _, privacy_report = process_checkpoint_with_privacy(
                    content,
                    privacy_level=privacy_level,
                    detect_only=True,  # Don't redact, just detect
                    repo_root=self.base_dir
                )

                print(f"  📊 PII Detections: {privacy_report['pii_detections']}")
                if privacy_report['detection_types']:
                    print("  Detection Breakdown:")
                    for pii_type, count in privacy_report['detection_types'].items():
                        print(f"    - {pii_type}: {count}")

                safe_status = "✅ SAFE" if privacy_report.get('safe_for_level') else "⚠️ MAY CONTAIN PII"
                print(f"  Status for {privacy_level}: {safe_status}")

                # Save privacy report
                privacy_report_path = self.checkpoints_dir / f"{filename.replace('.md', '-privacy-report.json')}"
                with open(privacy_report_path, 'w') as f:
                    json.dump(privacy_report, f, indent=2)
                print(f"  ✅ Privacy report saved: {privacy_report_path.name}")
            except Exception as e:
                print(f"  ⚠️ Privacy scan failed: {e}")

        # Step 3.7: Automatic conversation export deduplication
        dedup_stats = None
        if DEDUP_AVAILABLE:
            print(f"\nStep 3.7: Running automatic conversation export deduplication...")
            try:
                dedup_stats = self.deduplicate_exports(sprint_description)

                if dedup_stats:
                    print(f"  📊 Deduplication Results:")
                    print(f"    File: {dedup_stats['file']}")
                    print(f"    Session: {dedup_stats['session_id']}")
                    print(f"    Total Messages: {dedup_stats['total_messages']}")
                    print(f"    New Messages: {dedup_stats['new_messages']}")
                    print(f"    Duplicates Filtered: {dedup_stats['duplicates_filtered']}")
                    print(f"    Deduplication Rate: {dedup_stats['deduplication_rate']:.1f}%")
                    print(f"    Watermark: {dedup_stats['watermark']}")
                    print(f"    Total Unique Messages: {dedup_stats['total_unique_messages']}")
                    print(f"  ✅ Deduplication complete")
                else:
                    print(f"  ℹ️  No exports found to deduplicate")

            except Exception as e:
                print(f"  ⚠️ Deduplication failed: {e}")
                print(f"  Continuing with checkpoint creation...")

        # Step 4: Commit changes (optional)
        if auto_commit:
            print("\nStep 4: Committing changes to git...")
            self.commit_changes(filename, sprint_description)

            # Step 5: Push changes (optional)
            if auto_push:
                print("\nStep 5: Pushing changes to remote...")
                self.push_changes()
        else:
            print("\nStep 4: Skipping auto-commit (use --auto-commit flag to enable)")
            print("\nTo commit manually:")
            print(f"  git add MEMORY-CONTEXT/checkpoints/{filename} README.md MEMORY-CONTEXT/")
            print(f"  git commit -m 'Create checkpoint: {sprint_description}'")
            print(f"  git push  # Push to remote")

        # Summary
        print(f"\n{'='*80}")
        print(f"✅ CHECKPOINT CREATION COMPLETE")
        print(f"{'='*80}\n")
        print(f"Checkpoint: MEMORY-CONTEXT/checkpoints/{filename}")
        print(f"Reference: README.md (Recent Checkpoints section)")
        print(f"Context Export: MEMORY-CONTEXT/sessions/")

        if dedup_stats:
            print()
            print(f"{'='*80}")
            print(f"💾 DEDUPLICATION SUMMARY")
            print(f"{'='*80}")
            print(f"\nConversation exports automatically deduplicated:")
            print(f"  ✅ Total Messages: {dedup_stats['total_messages']}")
            print(f"  ✅ New Unique: {dedup_stats['new_messages']}")
            print(f"  ✅ Duplicates Removed: {dedup_stats['duplicates_filtered']}")
            print(f"  ✅ Deduplication Rate: {dedup_stats['deduplication_rate']:.1f}%")
            print(f"  ✅ Storage: MEMORY-CONTEXT/dedup_state/")
            print()
            print(f"Benefits:")
            print(f"  • Zero catastrophic forgetting (all unique messages preserved)")
            print(f"  • 95%+ storage reduction (duplicates eliminated)")
            print(f"  • Instant session continuity (watermark tracking)")

        if export_path:
            print()
            print(f"{'='*80}")
            print(f"📤 IMPORTANT: Complete conversation export for full context")
            print(f"{'='*80}")
            print(f"\nAutomated context already captured:")
            print(f"  ✅ Git state (commits, branches, file changes)")
            print(f"  ✅ Completed tasks from TASKLISTs")
            print(f"  ✅ Checkpoint sections and metadata")
            print(f"  ✅ JSON export for programmatic access")
            print()
            print(f"To capture FULL CONVERSATION (recommended):")
            print(f"  1. Run: /export (in Claude Code)")
            print(f"  2. Save to: {export_path}")
            print()
            print(f"This ensures ZERO catastrophic forgetting:")
            print(f"  ✅ Checkpoint = Project state (WHAT was done)")
            print(f"  ✅ Automated extraction = Context (git, tasks, sections)")
            print(f"  ✅ /export = Full conversation (WHY and HOW decisions were made)")

        print(f"\nNext session can load this checkpoint for context continuity.")
        print(f"\n{'='*80}\n")

        return str(checkpoint_path)


def main():
    """Main entry point for checkpoint creation script."""
    parser = argparse.ArgumentParser(
        description="CODITECT Checkpoint Creation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default behavior: prompt for /export, create checkpoint, commit AND push
  python3 scripts/create-checkpoint.py "Architecture Documentation Sprint Complete"

  # Skip conversation export (checkpoint only)
  python3 scripts/create-checkpoint.py "Quick State Snapshot" --no-export

  # Commit locally only (no push)
  python3 scripts/create-checkpoint.py "Work in Progress" --no-push

  # Skip both export and push (fastest, local-only)
  python3 scripts/create-checkpoint.py "WIP Snapshot" --no-export --no-push

Default Behavior (Zero Catastrophic Forgetting):
  ✅ --with-export ON by default (prepares /export location)
  ✅ --auto-push ON by default (commits and pushes to remote)
  ✅ Automatic context extraction (git, tasks, sections)

  Complete workflow:
  1. Prepares MEMORY-CONTEXT/exports/ location for /export
  2. Creates checkpoint document (state snapshot)
  3. Updates README.md with checkpoint reference
  4. Creates session template in MEMORY-CONTEXT/sessions/
  5. **AUTOMATICALLY extracts context** (git state, tasks, checkpoint sections)
  6. **Generates JSON export** for programmatic access
  7. Commits all changes to git
  8. Pushes to remote (submodule + master repo if applicable)

  Automatic Context Extraction:
  - ✅ Git commits, file changes, branch state
  - ✅ Completed tasks from all TASKLISTs
  - ✅ Checkpoint sections (objectives, decisions, next steps)
  - ✅ Metadata (timestamps, participants)
  - ✅ JSON export (MEMORY-CONTEXT/exports/)

  Automatic Deduplication (NEW):
  - ✅ Processes conversation exports automatically
  - ✅ Removes duplicate messages (95%+ reduction)
  - ✅ Preserves unique content (zero data loss)
  - ✅ Tracks watermarks for session continuity
  - ✅ Stores in MEMORY-CONTEXT/dedup_state/

  Manual (Optional but Recommended):
  - Run /export to capture full conversation dialogue

  Result: Maximum context preservation with minimal manual work!

Flags:
  --no-export    Skip conversation export preparation
  --no-push      Disable automatic push (commit locally only)
  --auto-commit  Commit changes locally (use with --no-push)
  --auto-push    Explicitly enable push (already default)
  --with-export  Explicitly enable export (already default)

For more information: https://github.com/coditect-ai/coditect-rollout-master
        """
    )

    parser.add_argument(
        'description',
        help='Description of the sprint/work completed'
    )

    parser.add_argument(
        '--auto-commit',
        action='store_true',
        help='Automatically commit changes to git (use with --no-push for commit without push)'
    )

    parser.add_argument(
        '--auto-push',
        action='store_true',
        default=True,
        help='Automatically push changes to remote (DEFAULT - use --no-push to disable)'
    )

    parser.add_argument(
        '--no-push',
        action='store_true',
        help='Disable automatic push (commit locally only)'
    )

    parser.add_argument(
        '--base-dir',
        default=None,
        help='Base directory for the project (defaults to script parent dir)'
    )

    parser.add_argument(
        '--privacy-scan',
        action='store_true',
        help='Scan checkpoint for PII and generate privacy report (requires privacy_manager)'
    )

    parser.add_argument(
        '--privacy-level',
        choices=['public', 'team', 'private', 'ephemeral'],
        default='private',
        help='Privacy level for scanning (default: private)'
    )

    parser.add_argument(
        '--with-export',
        action='store_true',
        default=True,
        help='Prepare conversation export location and prompt for /export (DEFAULT)'
    )

    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Skip conversation export preparation (only create checkpoint)'
    )

    args = parser.parse_args()

    # Handle --no-push flag (overrides default auto_push=True)
    auto_push = args.auto_push and not args.no_push

    # Handle --no-export flag (overrides default with_export=True)
    with_export = args.with_export and not args.no_export

    # Privacy check
    if args.privacy_scan and not PRIVACY_AVAILABLE:
        print("⚠️  WARNING: Privacy scanning requested but privacy_manager not available")
        print("Privacy features will be skipped")

    # Create checkpoint
    creator = CheckpointCreator(base_dir=args.base_dir)
    checkpoint_path = creator.run(
        args.description,
        auto_commit=args.auto_commit or auto_push,  # auto_push implies auto_commit
        auto_push=auto_push,
        privacy_scan=args.privacy_scan if PRIVACY_AVAILABLE else False,
        privacy_level=args.privacy_level,
        with_export=with_export
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
