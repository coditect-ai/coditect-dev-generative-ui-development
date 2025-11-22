#!/usr/bin/env python3
"""
CODITECT Session Export Engine

Automatically captures session context for MEMORY-CONTEXT system.

Features:
- Conversation extraction from checkpoints and sessions
- Metadata generation (timestamp, participants, objectives)
- File change tracking via git
- Decision logging and rationale capture
- Privacy-aware export

Usage:
    python session_export.py --checkpoint MEMORY-CONTEXT/checkpoints/2025-11-16-session.md
    python session_export.py --auto  # Auto-detect latest checkpoint
    python session_export.py --session-dir MEMORY-CONTEXT/sessions/

Author: AZ1.AI CODITECT Team
Sprint: Sprint +1 - MEMORY-CONTEXT Implementation
Date: 2025-11-16
"""

import os
import sys
import json
import re
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import subprocess

# Import core utilities
from utils import find_git_root

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SessionExporter:
    """
    Exports session context to MEMORY-CONTEXT system.

    Extracts conversation history, metadata, file changes, and decisions
    from checkpoint files and current git state.
    """

    def __init__(self, repo_root: Optional[Path] = None):
        """
        Initialize SessionExporter.

        Args:
            repo_root: Root directory of repository. Auto-detected if not provided.
        """
        if repo_root is None:
            # Auto-detect repo root using utility
            repo_root = find_git_root()
        else:
            repo_root = Path(repo_root)
            # Validate that provided path is a git repository
            if not ((repo_root / '.git').exists() or (repo_root / '.git').is_file()):
                raise ValueError(f"Provided path is not a git repository: {repo_root}")

        self.repo_root = Path(repo_root)
        self.memory_context_dir = self.repo_root / "MEMORY-CONTEXT"
        self.sessions_dir = self.memory_context_dir / "sessions"
        self.exports_dir = self.memory_context_dir / "exports"
        self.checkpoints_dir = self.memory_context_dir / "checkpoints"

        # Ensure directories exist
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"SessionExporter initialized for repo: {self.repo_root}")

    def export_session(
        self,
        checkpoint_path: Optional[Path] = None,
        session_name: Optional[str] = None
    ) -> Path:
        """
        Export session context from checkpoint.

        Args:
            checkpoint_path: Path to checkpoint file. Auto-detect latest if None.
            session_name: Custom session name. Auto-generated if None.

        Returns:
            Path to exported session file
        """
        # Auto-detect latest checkpoint if not provided
        if checkpoint_path is None:
            checkpoint_path = self._find_latest_checkpoint()
            if checkpoint_path is None:
                raise ValueError("No checkpoints found. Create a checkpoint first.")

        checkpoint_path = Path(checkpoint_path)
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

        logger.info(f"Exporting session from checkpoint: {checkpoint_path.name}")

        # Extract session data
        conversation = self._extract_conversation(checkpoint_path)
        metadata = self._generate_metadata(checkpoint_path)
        file_changes = self._track_file_changes()
        decisions = self._extract_decisions(checkpoint_path)

        # Generate session export
        session_content = self._build_session_export(
            conversation=conversation,
            metadata=metadata,
            file_changes=file_changes,
            decisions=decisions
        )

        # Generate session filename with ISO-DATETIME prefix
        if session_name is None:
            # Extract from checkpoint filename or use metadata
            session_name = self._generate_session_name(checkpoint_path, metadata)

        # Use current datetime as ISO-DATETIME prefix to prevent collisions
        # Format: YYYY-MM-DDTHH-MM-SSZ-session-name.md
        iso_datetime = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        session_filename = f"{iso_datetime}-{session_name}.md"
        session_path = self.sessions_dir / session_filename

        # Write session file
        session_path.write_text(session_content)
        logger.info(f"Session exported to: {session_path}")

        # Also create JSON export for programmatic access
        json_path = self.exports_dir / session_filename.replace('.md', '.json')
        self._export_json(
            json_path,
            conversation=conversation,
            metadata=metadata,
            file_changes=file_changes,
            decisions=decisions
        )
        logger.info(f"JSON export created: {json_path}")

        return session_path

    def _find_latest_checkpoint(self) -> Optional[Path]:
        """Find the most recent checkpoint file."""
        if not self.checkpoints_dir.exists():
            return None

        checkpoints = list(self.checkpoints_dir.glob("*.md"))
        if not checkpoints:
            return None

        # Sort by modification time (most recent first)
        checkpoints.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return checkpoints[0]

    def _extract_conversation(self, checkpoint_path: Path) -> List[Dict[str, str]]:
        """
        Extract conversation history from checkpoint.

        Returns:
            List of conversation turns with role and content
        """
        content = checkpoint_path.read_text()
        conversation = []

        # Look for conversation patterns in checkpoint
        # Checkpoints typically have sections like "## Work Completed" or conversation logs

        # Extract user messages (lines starting with User:, Human:, etc.)
        user_pattern = r'^(?:User|Human):\s*(.+)$'
        ai_pattern = r'^(?:Assistant|AI|Claude):\s*(.+)$'

        lines = content.split('\n')
        for line in lines:
            user_match = re.match(user_pattern, line, re.IGNORECASE)
            if user_match:
                conversation.append({
                    'role': 'user',
                    'content': user_match.group(1).strip(),
                    'timestamp': None  # Could extract from surrounding context
                })
                continue

            ai_match = re.match(ai_pattern, line, re.IGNORECASE)
            if ai_match:
                conversation.append({
                    'role': 'assistant',
                    'content': ai_match.group(1).strip(),
                    'timestamp': None
                })

        # If no explicit conversation found, extract key sections as summary
        if not conversation:
            # Extract sections as high-level conversation summary
            sections = self._extract_sections(content)
            if sections:
                conversation.append({
                    'role': 'system',
                    'content': 'Session summary extracted from checkpoint',
                    'sections': sections
                })

        logger.info(f"Extracted {len(conversation)} conversation turns")
        return conversation

    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract markdown sections from checkpoint."""
        sections = {}
        current_section = None
        current_content = []

        for line in content.split('\n'):
            # Detect section headers (## Header)
            header_match = re.match(r'^##\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                # Start new section
                current_section = header_match.group(1).strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        # Save final section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _generate_metadata(self, checkpoint_path: Path) -> Dict[str, Any]:
        """
        Generate metadata for session export.

        Returns:
            Metadata dict with timestamp, participants, objectives, etc.
        """
        # Extract timestamp from checkpoint filename or file modification time
        filename = checkpoint_path.stem

        # Try to parse ISO timestamp from filename (e.g., 2025-11-16T10-39-43Z-...)
        timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z)', filename)
        if timestamp_match:
            # Keep ISO format: YYYY-MM-DDTHH:MM:SSZ
            timestamp_str = timestamp_match.group(1)
            # Convert hyphens to colons in time portion only
            parts = timestamp_str.split('T')
            if len(parts) == 2:
                date_part = parts[0]
                time_part = parts[1].replace('-', ':').replace('Z', '')
                timestamp = f"{date_part}T{time_part}Z"
            else:
                timestamp = timestamp_str
        else:
            # Fall back to file modification time in ISO format
            mtime = checkpoint_path.stat().st_mtime
            timestamp = datetime.fromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Extract session objectives from checkpoint filename
        # Filename format: YYYY-MM-DDTHH-MM-SSZ-Description-Here.md
        objective_parts = filename.split('-')[4:] if len(filename.split('-')) > 4 else []
        objectives = ' '.join(objective_parts).replace('-', ' ') if objective_parts else "Session work"

        # Extract tags from content
        content = checkpoint_path.read_text()
        tags = self._extract_tags(content)

        metadata = {
            'timestamp': timestamp,
            'checkpoint_file': checkpoint_path.name,
            'participants': ['user', 'claude-code'],  # Default participants
            'objectives': objectives,
            'tags': tags,
            'repository': str(self.repo_root),
            'export_time': datetime.now().isoformat()
        }

        logger.info(f"Generated metadata: {metadata['objectives']}")
        return metadata

    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from checkpoint content."""
        tags = set()

        # Common tag patterns
        tag_patterns = [
            r'#([\w-]+)',  # Hashtags (including hyphens)
            r'\*\*Tags:\*\*\s*(.+)$',  # Explicit tags line
            r'\*\*Sprint:\*\*\s*(.+)$',  # Sprint name
            r'\*\*Phase:\*\*\s*(.+)$',  # Phase
        ]

        for pattern in tag_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                tag_text = match.group(1).strip()
                # For hashtags, add directly
                if pattern.startswith(r'#'):
                    if tag_text and len(tag_text) > 1:
                        tags.add(tag_text.lower())
                else:
                    # Split on common separators
                    for tag in re.split(r'[,;|\s]+', tag_text):
                        if tag and len(tag) > 1:
                            tags.add(tag.lower().replace(' ', '-'))

        return sorted(list(tags))

    def _track_file_changes(self) -> Dict[str, List[str]]:
        """
        Track file changes using git.

        Returns:
            Dict with 'modified', 'added', 'deleted' file lists
        """
        try:
            # Get git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )

            file_changes = {
                'modified': [],
                'added': [],
                'deleted': [],
                'untracked': []
            }

            # Parse git status output
            for line in result.stdout.split('\n'):
                if not line.strip():
                    continue

                status = line[:2]
                filepath = line[3:].strip()

                if status == ' M' or status == 'M ':
                    file_changes['modified'].append(filepath)
                elif status == 'A ' or status == 'AM':
                    file_changes['added'].append(filepath)
                elif status == ' D' or status == 'D ':
                    file_changes['deleted'].append(filepath)
                elif status == '??':
                    file_changes['untracked'].append(filepath)

            # Also get recent commits
            commits_result = subprocess.run(
                ['git', 'log', '--oneline', '-10'],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            file_changes['recent_commits'] = commits_result.stdout.strip().split('\n')

            logger.info(f"Tracked {sum(len(v) for v in file_changes.values() if isinstance(v, list))} file changes")
            return file_changes

        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e}")
            return {'modified': [], 'added': [], 'deleted': [], 'untracked': []}

    def _extract_decisions(self, checkpoint_path: Path) -> List[Dict[str, str]]:
        """
        Extract decision points and rationale from checkpoint.

        Returns:
            List of decisions with context and rationale
        """
        content = checkpoint_path.read_text()
        decisions = []

        # Look for decision indicators
        decision_patterns = [
            r'(?:decided|decision|chose|selected|opted)\s+to\s+(.+?)(?:\.|$)',
            r'(?:rationale|reason|because):\s*(.+?)(?:\n|$)',
            r'\*\*Decision:\*\*\s*(.+?)(?:\n|$)',
        ]

        for pattern in decision_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                decision_text = match.group(1).strip()

                # Extract context (surrounding lines)
                start_pos = max(0, match.start() - 200)
                end_pos = min(len(content), match.end() + 200)
                context = content[start_pos:end_pos]

                decisions.append({
                    'decision': decision_text,
                    'context': context,
                    'timestamp': None  # Could extract from surrounding text
                })

        # Also look for sections explicitly labeled as decisions
        sections = self._extract_sections(content)
        for section_name, section_content in sections.items():
            if 'decision' in section_name.lower() or 'rationale' in section_name.lower():
                decisions.append({
                    'decision': section_name,
                    'context': section_content,
                    'timestamp': None
                })

        logger.info(f"Extracted {len(decisions)} decisions")
        return decisions

    def _build_session_export(
        self,
        conversation: List[Dict],
        metadata: Dict,
        file_changes: Dict,
        decisions: List[Dict]
    ) -> str:
        """Build markdown session export document."""

        lines = [
            f"# Session Export: {metadata['objectives']}",
            "",
            f"**Timestamp:** {metadata['timestamp']}",
            f"**Checkpoint:** {metadata['checkpoint_file']}",
            f"**Repository:** {metadata['repository']}",
            f"**Participants:** {', '.join(metadata['participants'])}",
            "",
            "---",
            "",
            "## Session Metadata",
            "",
            f"- **Objectives:** {metadata['objectives']}",
            f"- **Tags:** {', '.join(metadata['tags']) if metadata['tags'] else 'None'}",
            f"- **Export Time:** {metadata['export_time']}",
            "",
            "---",
            "",
            "## Conversation Summary",
            ""
        ]

        # Add conversation
        if conversation:
            for i, turn in enumerate(conversation, 1):
                role = turn.get('role', 'unknown').capitalize()
                content = turn.get('content', '')

                # Handle sections if present
                if 'sections' in turn:
                    lines.append(f"### Checkpoint Sections")
                    lines.append("")
                    for section_name, section_content in turn['sections'].items():
                        lines.append(f"#### {section_name}")
                        lines.append("")
                        lines.append(section_content[:500] + "..." if len(section_content) > 500 else section_content)
                        lines.append("")
                else:
                    lines.append(f"### Turn {i}: {role}")
                    lines.append("")
                    lines.append(content)
                    lines.append("")
        else:
            lines.append("*No conversation history extracted*")
            lines.append("")

        # Add file changes
        lines.extend([
            "---",
            "",
            "## File Changes",
            ""
        ])

        if any(file_changes.values()):
            for change_type, files in file_changes.items():
                if change_type == 'recent_commits':
                    continue
                if files:
                    lines.append(f"### {change_type.capitalize()}")
                    lines.append("")
                    for file in files[:20]:  # Limit to 20 files per category
                        lines.append(f"- `{file}`")
                    if len(files) > 20:
                        lines.append(f"- *... and {len(files) - 20} more*")
                    lines.append("")

            # Add recent commits
            if 'recent_commits' in file_changes and file_changes['recent_commits']:
                lines.append("### Recent Commits")
                lines.append("")
                for commit in file_changes['recent_commits'][:10]:
                    lines.append(f"- {commit}")
                lines.append("")
        else:
            lines.append("*No file changes detected*")
            lines.append("")

        # Add decisions
        lines.extend([
            "---",
            "",
            "## Decisions & Rationale",
            ""
        ])

        if decisions:
            for i, decision in enumerate(decisions, 1):
                lines.append(f"### Decision {i}")
                lines.append("")
                lines.append(f"**Decision:** {decision['decision']}")
                lines.append("")
                if decision.get('context'):
                    lines.append("**Context:**")
                    lines.append(decision['context'][:300] + "..." if len(decision['context']) > 300 else decision['context'])
                lines.append("")
        else:
            lines.append("*No explicit decisions extracted*")
            lines.append("")

        # Footer
        lines.extend([
            "---",
            "",
            "## Next Session",
            "",
            "**Recommended Context Loading:**",
            "```bash",
            f"python3 scripts/core/context_loader.py --session '{metadata['checkpoint_file']}' --relevance 0.7",
            "```",
            "",
            "**Related Sessions:**",
            "- *To be populated by context loader*",
            "",
            "---",
            "",
            f"*Exported by CODITECT Session Export Engine - {metadata['export_time']}*"
        ])

        return '\n'.join(lines)

    def _export_json(
        self,
        json_path: Path,
        conversation: List[Dict],
        metadata: Dict,
        file_changes: Dict,
        decisions: List[Dict]
    ):
        """Export session data as JSON for programmatic access."""
        data = {
            'metadata': metadata,
            'conversation': conversation,
            'file_changes': file_changes,
            'decisions': decisions
        }

        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _generate_session_name(self, checkpoint_path: Path, metadata: Dict) -> str:
        """Generate session name from checkpoint or metadata."""
        # Extract from checkpoint filename
        filename = checkpoint_path.stem

        # Remove timestamp prefix
        name_parts = filename.split('-')[4:] if len(filename.split('-')) > 4 else [filename]
        name = '-'.join(name_parts)

        # Clean up
        name = name.replace('_', '-')

        # Limit length
        if len(name) > 100:
            name = name[:100]

        return name if name else 'session'


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='CODITECT Session Export Engine - Export session context for MEMORY-CONTEXT system'
    )

    parser.add_argument(
        '--checkpoint',
        type=str,
        help='Path to checkpoint file to export. Auto-detects latest if not provided.'
    )

    parser.add_argument(
        '--auto',
        action='store_true',
        help='Automatically export latest checkpoint'
    )

    parser.add_argument(
        '--session-name',
        type=str,
        help='Custom session name for export'
    )

    parser.add_argument(
        '--repo-root',
        type=str,
        help='Repository root directory. Auto-detected if not provided.'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Initialize exporter
        repo_root = Path(args.repo_root) if args.repo_root else None
        exporter = SessionExporter(repo_root=repo_root)

        # Export session
        checkpoint_path = Path(args.checkpoint) if args.checkpoint else None
        session_path = exporter.export_session(
            checkpoint_path=checkpoint_path,
            session_name=args.session_name
        )

        print(f"\n✅ Session exported successfully!")
        print(f"📄 Markdown: {session_path}")
        print(f"📊 JSON: {session_path.parent.parent / 'exports' / session_path.name.replace('.md', '.json')}")
        print(f"\n💡 Load this context in your next session:")
        print(f"   python3 scripts/core/context_loader.py --session '{session_path.name}'")

        return 0

    except Exception as e:
        logger.error(f"Session export failed: {e}", exc_info=args.verbose)
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
