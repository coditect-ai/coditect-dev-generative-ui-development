#!/usr/bin/env python3
"""
CODITECT Knowledge Navigation System - Dashboard Data Generator
Generates JSON data files from SQLite database for dashboard consumption

Usage:
    python3 generate-dashboard.py

Output:
    dashboard/data/ directory with JSON data files

NOTE: This script ONLY generates data files. It does NOT touch HTML, CSS, or JS
      files - those are source code and should be managed via git.
"""

import sqlite3
import json
import os
import shutil
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict
import re

class DashboardGenerator:
    """Static site generator for knowledge navigation dashboard"""

    def __init__(self, db_path: str, output_dir: str):
        self.db_path = Path(db_path)
        self.output_dir = Path(output_dir)
        self.conn = None
        self.stats = {
            'messages_exported': 0,
            'pages_generated': 0,
            'topics_exported': 0,
            'files_exported': 0,
            'checkpoints_exported': 0,
            'commands_exported': 0,
            'git_commits_exported': 0
        }
        # Cache for export metadata
        self.export_metadata_cache = {}

    def connect(self):
        """Connect to SQLite database"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        print(f"✓ Connected to {self.db_path}")

    def load_export_metadata(self, checkpoint_id: str) -> Dict[str, Any]:
        """Load rich metadata from export JSON file if available"""
        if checkpoint_id in self.export_metadata_cache:
            return self.export_metadata_cache[checkpoint_id]

        # Try to find corresponding export JSON file
        exports_dir = self.db_path.parent / 'exports'
        if not exports_dir.exists():
            return {}

        matched = False
        # Match checkpoint ID to export file (they might have different naming)
        for export_file in exports_dir.glob('*.json'):
            try:
                with open(export_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    metadata = data.get('metadata', {})

                    # Check if this export matches our checkpoint
                    # Remove .md extension for comparison
                    checkpoint_file = metadata.get('checkpoint_file', '').replace('.md', '')

                    # Try multiple matching strategies
                    # 1. Exact match
                    # 2. Checkpoint ID contains the filename
                    # 3. Filename is at the end of checkpoint ID
                    if (checkpoint_file and (
                        checkpoint_id == checkpoint_file or
                        checkpoint_file in checkpoint_id or
                        checkpoint_id.endswith(checkpoint_file))):
                        # Extract rich metadata
                        result = {
                            'repository': metadata.get('repository', ''),
                            'project_name': self._extract_project_name(metadata.get('repository', '')),
                            'participants': metadata.get('participants', []),
                            'objectives': metadata.get('objectives', ''),
                            'tags': metadata.get('tags', []),
                            'export_time': metadata.get('export_time', '')
                        }
                        self.export_metadata_cache[checkpoint_id] = result
                        return result
            except Exception as e:
                continue

        return {}

    def _extract_project_name(self, repository_path: str) -> str:
        """Extract project name from repository path"""
        if not repository_path:
            return ''

        # Get the last directory name from the path
        # e.g., /Users/.../coditect-rollout-master/submodules/coditect-project-dot-claude
        # -> coditect-project-dot-claude
        path = Path(repository_path)
        project_name = path.name

        # If it's the master repo, try to get a better name
        if 'coditect-rollout-master' in repository_path and '/submodules/' not in repository_path:
            return 'coditect-rollout-master'

        return project_name

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_directories(self):
        """Create output directory structure"""
        dirs = [
            self.output_dir,
            self.output_dir / 'data',
            self.output_dir / 'css',
            self.output_dir / 'js',
            self.output_dir / 'templates',
            self.output_dir / 'assets'
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created {dir_path}")

    def export_messages(self, page_size: int = 100) -> Dict[str, Any]:
        """
        Export all messages with pagination

        Returns:
            Message index with metadata
        """
        print("\n📊 Exporting messages...")

        cursor = self.conn.cursor()

        # Get all messages with tags
        cursor.execute('''
            SELECT
                m.hash,
                m.role,
                m.content,
                m.first_seen,
                m.checkpoint_id,
                m.message_index,
                c.title as checkpoint_title,
                GROUP_CONCAT(DISTINCT t.name) as tags
            FROM messages m
            LEFT JOIN checkpoints c ON m.checkpoint_id = c.id
            LEFT JOIN message_tags mt ON m.hash = mt.message_hash
            LEFT JOIN tags t ON mt.tag_id = t.id
            GROUP BY m.hash
            ORDER BY m.first_seen, m.message_index
        ''')

        all_messages = []
        for row in cursor.fetchall():
            # Create content preview (first 200 chars)
            content = row['content'] or ''
            content_preview = content[:200] + ('...' if len(content) > 200 else '')

            # Parse tags
            tags = row['tags'].split(',') if row['tags'] else []

            # Get file references for this message
            cursor.execute('''
                SELECT filepath, operation FROM file_references
                WHERE message_hash = ?
            ''', (row['hash'],))
            file_refs = [{'filepath': r['filepath'], 'operation': r['operation']}
                        for r in cursor.fetchall()]

            # Get commands for this message
            cursor.execute('''
                SELECT command_type, command_text FROM commands
                WHERE message_hash = ?
            ''', (row['hash'],))
            commands = [{'type': r['command_type'], 'text': r['command_text']}
                       for r in cursor.fetchall()]

            message = {
                'hash': row['hash'],
                'role': row['role'],
                'content': content,
                'content_preview': content_preview,
                'checkpoint_id': row['checkpoint_id'] or '',
                'checkpoint_title': row['checkpoint_title'] or '',
                'first_seen': row['first_seen'] or '',
                'tags': tags,
                'file_references': file_refs,
                'commands': commands,
                'word_count': len(content.split()),
                'has_code': '```' in content or 'def ' in content or 'function ' in content
            }
            all_messages.append(message)

        self.stats['messages_exported'] = len(all_messages)
        print(f"  Found {len(all_messages)} messages")

        # Paginate messages
        total_pages = (len(all_messages) + page_size - 1) // page_size
        print(f"  Creating {total_pages} pages ({page_size} messages/page)...")

        for page_num in range(total_pages):
            start_idx = page_num * page_size
            end_idx = min(start_idx + page_size, len(all_messages))
            page_messages = all_messages[start_idx:end_idx]

            page_file = self.output_dir / 'data' / f'messages-page-{page_num+1:03d}.json'
            with open(page_file, 'w') as f:
                json.dump({
                    'page': page_num + 1,
                    'total_pages': total_pages,
                    'messages': page_messages
                }, f, indent=2)

        self.stats['pages_generated'] = total_pages

        # Create message index (metadata only, no full content)
        message_index = {
            'version': '1.0',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'total_messages': len(all_messages),
            'pagination': {
                'page_size': page_size,
                'total_pages': total_pages
            },
            'messages': [
                {
                    'hash': msg['hash'],
                    'role': msg['role'],
                    'content_preview': msg['content_preview'],
                    'checkpoint_id': msg['checkpoint_id'],
                    'first_seen': msg['first_seen'],
                    'tags': msg['tags'],
                    'word_count': msg['word_count'],
                    'has_code': msg['has_code']
                }
                for msg in all_messages
            ]
        }

        # Write index file
        index_file = self.output_dir / 'data' / 'messages.json'
        with open(index_file, 'w') as f:
            json.dump(message_index, f, indent=2)

        print(f"✓ Exported {len(all_messages)} messages ({total_pages} pages)")
        return message_index

    def export_topics(self) -> Dict[str, Any]:
        """Export topic metadata with statistics"""
        print("\n🏷️  Exporting topics...")

        cursor = self.conn.cursor()

        # Get all tags with message counts
        cursor.execute('''
            SELECT
                t.name,
                t.category,
                COUNT(DISTINCT mt.message_hash) as message_count
            FROM tags t
            LEFT JOIN message_tags mt ON t.id = mt.tag_id
            GROUP BY t.name, t.category
            ORDER BY message_count DESC
        ''')

        topics = []
        topic_colors = {
            'topic:documentation': '#3498db',
            'topic:submodules': '#2ecc71',
            'topic:agents': '#9b59b6',
            'topic:testing': '#e74c3c',
            'topic:deployment': '#f39c12',
            'topic:security': '#e67e22',
        }

        total_messages = self.stats['messages_exported']

        for row in cursor.fetchall():
            name = row['name']
            display_name = name.split(':')[-1].title()
            message_count = row['message_count']

            # Get top files for this topic
            cursor.execute('''
                SELECT fr.filepath, COUNT(*) as count
                FROM file_references fr
                JOIN message_tags mt ON fr.message_hash = mt.message_hash
                JOIN tags t ON mt.tag_id = t.id
                WHERE t.name = ?
                GROUP BY fr.filepath
                ORDER BY count DESC
                LIMIT 5
            ''', (name,))
            top_files = [{'file': r['filepath'], 'count': r['count']}
                        for r in cursor.fetchall()]

            topic = {
                'name': name,
                'display_name': display_name,
                'category': row['category'],
                'message_count': message_count,
                'percentage': round((message_count / total_messages * 100), 1) if total_messages > 0 else 0,
                'color': topic_colors.get(name, '#95a5a6'),
                'top_files': top_files
            }
            topics.append(topic)

        self.stats['topics_exported'] = len(topics)

        # Create topic taxonomy
        topic_data = {
            'version': '1.0',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'topics': topics,
            'topic_hierarchy': {
                'topics': ['documentation', 'submodules', 'agents', 'testing', 'deployment', 'security'],
                'actions': ['read-file', 'write-file', 'edit-file', 'shell-command', 'task-invocation'],
                'artifacts': ['documentation', 'python-code', 'shell-script', 'config-file']
            }
        }

        # Write topics file
        topics_file = self.output_dir / 'data' / 'topics.json'
        with open(topics_file, 'w') as f:
            json.dump(topic_data, f, indent=2)

        print(f"✓ Exported {len(topics)} topics")
        return topic_data

    def export_files(self) -> Dict[str, Any]:
        """Export file references and build file tree"""
        print("\n📁 Exporting file references...")

        cursor = self.conn.cursor()

        # Get all file references with stats
        cursor.execute('''
            SELECT
                filepath,
                COUNT(*) as reference_count,
                SUM(CASE WHEN operation = 'read' THEN 1 ELSE 0 END) as read_count,
                SUM(CASE WHEN operation = 'write' THEN 1 ELSE 0 END) as write_count,
                SUM(CASE WHEN operation = 'edit' THEN 1 ELSE 0 END) as edit_count,
                MIN(m.first_seen) as first_reference,
                MAX(m.first_seen) as last_reference
            FROM file_references fr
            JOIN messages m ON fr.message_hash = m.hash
            GROUP BY filepath
            ORDER BY reference_count DESC
        ''')

        files = []
        file_tree = {}

        for row in cursor.fetchall():
            filepath = row['filepath']

            # Determine file type
            ext = Path(filepath).suffix.lower()
            file_type_map = {
                '.md': 'markdown',
                '.py': 'python',
                '.js': 'javascript',
                '.ts': 'typescript',
                '.json': 'json',
                '.yaml': 'yaml',
                '.yml': 'yaml',
                '.sh': 'shell',
                '.bash': 'shell'
            }
            file_type = file_type_map.get(ext, 'text')

            # Get related topics
            cursor.execute('''
                SELECT DISTINCT t.name
                FROM message_tags mt
                JOIN tags t ON mt.tag_id = t.id
                WHERE mt.message_hash IN (
                    SELECT message_hash FROM file_references WHERE filepath = ?
                )
                LIMIT 5
            ''', (filepath,))
            related_topics = [r['name'] for r in cursor.fetchall()]

            file_data = {
                'filepath': filepath,
                'reference_count': row['reference_count'],
                'operations': {
                    'read': row['read_count'],
                    'write': row['write_count'],
                    'edit': row['edit_count']
                },
                'first_reference': row['first_reference'] or '',
                'last_reference': row['last_reference'] or '',
                'file_type': file_type,
                'related_topics': related_topics
            }
            files.append(file_data)

            # Build file tree
            parts = filepath.split('/')
            current = file_tree
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # Leaf node (file)
                    current[part] = {
                        'type': 'file',
                        'count': row['reference_count']
                    }
                else:
                    # Directory node
                    if part not in current:
                        current[part] = {'type': 'directory'}
                    current = current[part]

        self.stats['files_exported'] = len(files)

        file_data = {
            'version': '1.0',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'files': files,
            'file_tree': file_tree
        }

        # Write files file
        files_file = self.output_dir / 'data' / 'files.json'
        with open(files_file, 'w') as f:
            json.dump(file_data, f, indent=2)

        print(f"✓ Exported {len(files)} file references")
        return file_data

    def scan_checkpoint_markdown_files(self) -> List[Dict[str, Any]]:
        """Scan checkpoints/ and sessions/ directories for actual markdown files"""
        checkpoint_files = []

        # Scan both checkpoints/ and sessions/ directories
        scan_dirs = [
            self.db_path.parent / 'checkpoints',
            self.db_path.parent / 'sessions'
        ]

        for checkpoints_dir in scan_dirs:
            if not checkpoints_dir.exists():
                print(f"  Warning: {checkpoints_dir.name}/ directory not found")
                continue

            for md_file in sorted(checkpoints_dir.glob('*.md'), reverse=True):
                # Use filename without extension as ID
                checkpoint_id = md_file.stem

                # Extract date from filename
                checkpoint_date = 'Unknown'
                # Try ISO format first (2025-11-16T09-26-41Z)
                iso_match = re.match(r'(\d{4}-\d{2}-\d{2}T[\d-]+Z)', checkpoint_id)
                if iso_match:
                    # Convert to proper ISO format
                    date_str = iso_match.group(1).replace('T', 'T').replace('-', ':', 2).replace('-', ':', 2)
                    checkpoint_date = date_str
                else:
                    # Try simple date format (2025-11-16)
                    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', checkpoint_id)
                    if date_match:
                        checkpoint_date = date_match.group(1) + 'T12:00:00Z'

                # Read first few lines for title/summary
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:20]
                        title = checkpoint_id  # Default to filename
                        summary = ''

                        # Look for markdown title
                        for line in lines:
                            if line.startswith('# '):
                                title = line[2:].strip()
                                break

                        # Look for summary or first paragraph
                        in_para = False
                        for line in lines:
                            if line.strip() and not line.startswith('#'):
                                summary += line.strip() + ' '
                                in_para = True
                                if len(summary) > 200:
                                    break
                            elif in_para and not line.strip():
                                break

                        summary = summary[:200].strip()
                except Exception as e:
                    print(f"  Warning: Could not read {md_file.name}: {e}")
                    title = checkpoint_id
                    summary = ''

                checkpoint_files.append({
                    'id': checkpoint_id,
                    'title': title,
                    'date': checkpoint_date,
                    'message_count': 0,  # Not tracked for checkpoint files
                    'user_messages': 0,
                    'assistant_messages': 0,
                    'top_topics': [],
                    'files_modified': [],
                    'commands_executed': 0,
                    'summary': summary if summary else 'Checkpoint session',
                    'project_name': '',
                    'repository': '',
                    'participants': [],
                    'objectives': '',
                    'export_tags': ['checkpoint'],
                    'export_time': '',
                    'source': 'markdown'  # Mark as coming from markdown file
                })

        return checkpoint_files

    def export_checkpoints(self) -> Dict[str, Any]:
        """Export checkpoint metadata and timeline"""
        print("\n💬 Exporting checkpoints...")

        cursor = self.conn.cursor()

        # Get all checkpoints with stats
        cursor.execute('''
            SELECT
                id,
                title,
                date,
                message_count
            FROM checkpoints
            ORDER BY date DESC
        ''')

        checkpoints = []
        timeline_data = defaultdict(lambda: {'message_count': 0, 'checkpoints': []})

        for row in cursor.fetchall():
            checkpoint_id = row['id']

            # Get message role breakdown
            cursor.execute('''
                SELECT
                    role,
                    COUNT(*) as count
                FROM messages
                WHERE checkpoint_id = ?
                GROUP BY role
            ''', (checkpoint_id,))
            role_counts = dict(cursor.fetchall())

            # Get top topics
            cursor.execute('''
                SELECT t.name, COUNT(*) as count
                FROM message_tags mt
                JOIN tags t ON mt.tag_id = t.id
                WHERE mt.message_hash IN (
                    SELECT hash FROM messages WHERE checkpoint_id = ?
                )
                GROUP BY t.name
                ORDER BY count DESC
                LIMIT 5
            ''', (checkpoint_id,))
            top_topics = [r['name'] for r in cursor.fetchall()]

            # Get files modified
            cursor.execute('''
                SELECT DISTINCT filepath
                FROM file_references
                WHERE message_hash IN (
                    SELECT hash FROM messages WHERE checkpoint_id = ?
                )
                AND operation IN ('write', 'edit')
                LIMIT 10
            ''', (checkpoint_id,))
            files_modified = [r['filepath'] for r in cursor.fetchall()]

            # Get command count
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM commands
                WHERE message_hash IN (
                    SELECT hash FROM messages WHERE checkpoint_id = ?
                )
            ''', (checkpoint_id,))
            commands_executed = cursor.fetchone()['count']

            checkpoint_date = row['date'] or ''

            # Load rich metadata from export JSON if available
            export_meta = self.load_export_metadata(checkpoint_id)

            checkpoint = {
                'id': checkpoint_id,
                'title': row['title'] or '',
                'date': checkpoint_date,
                'message_count': row['message_count'],
                'user_messages': role_counts.get('user', 0),
                'assistant_messages': role_counts.get('assistant', 0),
                'top_topics': top_topics,
                'files_modified': files_modified,
                'commands_executed': commands_executed,
                'summary': f"{role_counts.get('user', 0)} user messages, {role_counts.get('assistant', 0)} assistant responses",
                # Rich metadata from export JSON
                'project_name': export_meta.get('project_name', ''),
                'repository': export_meta.get('repository', ''),
                'participants': export_meta.get('participants', []),
                'objectives': export_meta.get('objectives', ''),
                'export_tags': export_meta.get('tags', []),
                'export_time': export_meta.get('export_time', '')
            }
            checkpoints.append(checkpoint)

            # Add to timeline
            if checkpoint_date:
                date_key = checkpoint_date[:10]  # YYYY-MM-DD
                timeline_data[date_key]['message_count'] += row['message_count']
                timeline_data[date_key]['checkpoints'].append(checkpoint_id)

        # Scan for actual checkpoint markdown files
        print("  Scanning checkpoints/ and sessions/ directories for markdown files...")
        markdown_checkpoints = self.scan_checkpoint_markdown_files()
        print(f"  Found {len(markdown_checkpoints)} checkpoint markdown files")

        # Merge database checkpoints with markdown file checkpoints
        # Database checkpoints come first (they have full stats)
        all_checkpoints = checkpoints + markdown_checkpoints

        self.stats['checkpoints_exported'] = len(all_checkpoints)
        self.stats['checkpoint_markdown_files'] = len(markdown_checkpoints)

        # Convert timeline to sorted list
        timeline = [
            {
                'date': date,
                'message_count': data['message_count'],
                'checkpoints': data['checkpoints']
            }
            for date, data in sorted(timeline_data.items())
        ]

        checkpoint_data = {
            'version': '1.0',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'checkpoints': all_checkpoints,
            'timeline': timeline,
            'stats': {
                'total': len(all_checkpoints),
                'from_database': len(checkpoints),
                'from_markdown': len(markdown_checkpoints)
            }
        }

        # Write checkpoints file
        checkpoints_file = self.output_dir / 'data' / 'checkpoints.json'
        with open(checkpoints_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)

        print(f"✓ Exported {len(all_checkpoints)} total checkpoints ({len(checkpoints)} from database, {len(markdown_checkpoints)} from markdown)")
        return checkpoint_data

    def export_commands(self) -> Dict[str, Any]:
        """Export command history"""
        print("\n⚡ Exporting commands...")

        cursor = self.conn.cursor()

        # Get all commands with context
        cursor.execute('''
            SELECT
                c.command_type,
                c.command_text,
                c.message_hash,
                m.checkpoint_id,
                m.first_seen
            FROM commands c
            JOIN messages m ON c.message_hash = m.hash
            ORDER BY m.first_seen DESC
        ''')

        commands = []
        command_stats = defaultdict(int)

        for idx, row in enumerate(cursor.fetchall(), 1):
            command = {
                'id': idx,
                'command_type': row['command_type'],
                'command_text': row['command_text'],
                'message_hash': row['message_hash'],
                'checkpoint_id': row['checkpoint_id'] or '',
                'timestamp': row['first_seen'] or ''
            }
            commands.append(command)
            command_stats[row['command_type']] += 1

        self.stats['commands_exported'] = len(commands)

        command_data = {
            'version': '1.0',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'commands': commands,
            'command_stats': dict(command_stats)
        }

        # Write commands file
        commands_file = self.output_dir / 'data' / 'commands.json'
        with open(commands_file, 'w') as f:
            json.dump(command_data, f, indent=2)

        print(f"✓ Exported {len(commands)} commands")
        return command_data

    def get_github_repo_url(self) -> Optional[str]:
        """Extract GitHub repository URL from git remote"""
        try:
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                cwd=self.db_path.parent.parent,  # Go to repo root
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                remote_url = result.stdout.strip()
                # Convert SSH to HTTPS URL
                if remote_url.startswith('git@github.com:'):
                    remote_url = remote_url.replace('git@github.com:', 'https://github.com/')
                if remote_url.endswith('.git'):
                    remote_url = remote_url[:-4]
                return remote_url
        except Exception as e:
            print(f"  Warning: Could not extract GitHub URL: {e}")
        return None

    def export_git_commits(self, limit: int = 500) -> Dict[str, Any]:
        """Export git commit history with GitHub links"""
        print("\n🔧 Exporting git commits...")

        commits = []
        github_url = self.get_github_repo_url()

        if not github_url:
            print("  Warning: GitHub URL not found, commit links will be unavailable")

        try:
            # Get git log with separator to avoid JSON parsing issues
            git_format = '%H%n%h%n%an%n%ae%n%aI%n%s%n%b%n===COMMIT_END==='

            result = subprocess.run(
                ['git', 'log', f'--pretty=format:{git_format}', f'-{limit}'],
                cwd=self.db_path.parent.parent,  # Go to repo root
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # Parse git log output by splitting on separator
                commit_blocks = result.stdout.split('===COMMIT_END===')
                commits_raw = []

                for block in commit_blocks:
                    lines = block.strip().split('\n')
                    if len(lines) >= 6:  # Must have at least hash, short_hash, author, email, date, subject
                        # Body is everything after subject (index 5 onwards)
                        body_lines = lines[6:] if len(lines) > 6 else []
                        commits_raw.append({
                            'hash': lines[0],
                            'short_hash': lines[1],
                            'author': lines[2],
                            'email': lines[3],
                            'date': lines[4],
                            'subject': lines[5],
                            'body': '\n'.join(body_lines)
                        })

                for commit_raw in commits_raw:
                    # Parse commit date
                    commit_date = datetime.fromisoformat(commit_raw['date'].replace('Z', '+00:00'))

                    # Extract commit type from subject (feat:, fix:, docs:, etc.)
                    subject = commit_raw['subject']
                    commit_type = 'other'
                    if ':' in subject or '(' in subject:
                        # Handle both "feat:" and "feat(scope):" formats
                        type_part = subject.split(':')[0].strip().lower()
                        if '(' in type_part:
                            type_part = type_part.split('(')[0].strip()
                        if type_part in ['feat', 'fix', 'docs', 'refactor', 'test', 'chore', 'ci', 'style', 'perf']:
                            commit_type = type_part

                    commit = {
                        'hash': commit_raw['hash'],
                        'short_hash': commit_raw['short_hash'],
                        'author': commit_raw['author'],
                        'email': commit_raw['email'],
                        'date': commit_date.isoformat(),
                        'timestamp': int(commit_date.timestamp() * 1000),  # JavaScript timestamp
                        'subject': subject,
                        'body': commit_raw['body'].strip(),
                        'type': commit_type,
                        'github_url': f"{github_url}/commit/{commit_raw['hash']}" if github_url else None
                    }
                    commits.append(commit)

                print(f"  Found {len(commits)} commits")
            else:
                print(f"  Warning: git log failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            print("  Warning: git log timed out")
        except Exception as e:
            print(f"  Warning: Could not extract git commits: {e}")

        commit_data = {
            'version': '1.0',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'github_url': github_url,
            'commits': commits,
            'commit_types': {
                'feat': 'New features',
                'fix': 'Bug fixes',
                'docs': 'Documentation',
                'refactor': 'Code refactoring',
                'test': 'Tests',
                'chore': 'Maintenance',
                'ci': 'CI/CD',
                'style': 'Code style',
                'perf': 'Performance',
                'other': 'Other changes'
            }
        }

        # Write git commits file
        commits_file = self.output_dir / 'data' / 'git-commits.json'
        with open(commits_file, 'w') as f:
            json.dump(commit_data, f, indent=2)

        self.stats['git_commits_exported'] = len(commits)
        print(f"✓ Exported {len(commits)} git commits")
        return commit_data

    def copy_static_assets(self):
        """Copy CSS, JS, and asset files"""
        print("\n📦 Copying static assets...")

        # Create placeholder CSS files
        css_files = {
            'main.css': self._get_main_css(),
            'layout.css': self._get_layout_css(),
            'components.css': self._get_components_css(),
            'print.css': self._get_print_css()
        }

        for filename, content in css_files.items():
            css_file = self.output_dir / 'css' / filename
            with open(css_file, 'w') as f:
                f.write(content)
            print(f"✓ Created {filename}")

        # Create placeholder JS files (stubs for now, full implementation in next task)
        js_files = {
            'navigation.js': self._get_navigation_js(),
            'data-loader.js': self._get_data_loader_js()
        }

        for filename, content in js_files.items():
            js_file = self.output_dir / 'js' / filename
            with open(js_file, 'w') as f:
                f.write(content)
            print(f"✓ Created {filename}")

    def generate_html(self, message_index: Dict, topics: Dict, files: Dict,
                     checkpoints: Dict, commands: Dict):
        """Generate HTML dashboard"""
        print("\n📄 Generating HTML...")

        # Generate index.html
        html_content = self._get_index_html(
            message_index, topics, files, checkpoints, commands
        )

        index_file = self.output_dir / 'index.html'
        with open(index_file, 'w') as f:
            f.write(html_content)

        print(f"✓ Generated index.html")

    def _get_main_css(self) -> str:
        """Generate main.css with CSS variables and global styles"""
        return """/* CODITECT Knowledge Navigation Dashboard - Main Styles */

:root {
    /* Color Palette */
    --color-primary: #3498db;
    --color-secondary: #2ecc71;
    --color-accent: #9b59b6;
    --color-warning: #f39c12;
    --color-danger: #e74c3c;
    --color-dark: #2c3e50;
    --color-light: #ecf0f1;
    --color-white: #ffffff;

    /* Typography */
    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif;
    --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", monospace;
    --font-size-base: 16px;
    --font-size-small: 14px;
    --font-size-large: 18px;
    --line-height: 1.6;

    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;

    /* Borders */
    --border-radius: 8px;
    --border-color: #ddd;

    /* Shadows */
    --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 8px rgba(0,0,0,0.15);
    --shadow-lg: 0 8px 16px rgba(0,0,0,0.2);
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    line-height: var(--line-height);
    color: var(--color-dark);
    background-color: var(--color-light);
}

h1, h2, h3, h4, h5, h6 {
    margin-bottom: var(--spacing-md);
    font-weight: 600;
}

a {
    color: var(--color-primary);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

code, pre {
    font-family: var(--font-mono);
    background-color: rgba(0,0,0,0.05);
    padding: 2px 6px;
    border-radius: 4px;
}

pre {
    padding: var(--spacing-md);
    overflow-x: auto;
}

.stat-card {
    background: var(--color-white);
    padding: var(--spacing-lg);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-sm);
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-primary);
}

.message-card {
    background: var(--color-white);
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s;
}

.message-card:hover {
    box-shadow: var(--shadow-md);
}

.tag {
    display: inline-block;
    padding: var(--spacing-xs) var(--spacing-sm);
    margin: var(--spacing-xs);
    background-color: var(--color-primary);
    color: var(--color-white);
    border-radius: 4px;
    font-size: var(--font-size-small);
}

button {
    padding: var(--spacing-sm) var(--spacing-lg);
    background-color: var(--color-primary);
    color: var(--color-white);
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: var(--font-size-base);
    transition: background-color 0.2s;
}

button:hover {
    background-color: #2980b9;
}

input[type="search"],
input[type="text"] {
    padding: var(--spacing-sm);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: var(--font-size-base);
    width: 100%;
}
"""

    def _get_layout_css(self) -> str:
        """Generate layout.css with grid layout"""
        return """/* CODITECT Dashboard - Layout Styles */

.app-container {
    display: grid;
    grid-template-areas:
        "header header header"
        "sidebar main main"
        "footer footer footer";
    grid-template-columns: 250px 1fr;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
    gap: 0;
}

.app-header {
    grid-area: header;
    background-color: var(--color-dark);
    color: var(--color-white);
    padding: var(--spacing-md) var(--spacing-lg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: var(--shadow-md);
}

.logo {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.logo h1 {
    margin: 0;
    font-size: 1.5rem;
}

.global-search {
    flex-grow: 1;
    max-width: 500px;
    margin: 0 var(--spacing-xl);
}

.sidebar {
    grid-area: sidebar;
    background-color: var(--color-white);
    padding: var(--spacing-lg);
    border-right: 1px solid var(--border-color);
    overflow-y: auto;
}

.sidebar nav ul {
    list-style: none;
}

.sidebar nav li {
    margin-bottom: var(--spacing-sm);
}

.sidebar nav a {
    display: block;
    padding: var(--spacing-sm);
    border-radius: var(--border-radius);
    transition: background-color 0.2s;
}

.sidebar nav a:hover {
    background-color: var(--color-light);
    text-decoration: none;
}

.main-content {
    grid-area: main;
    padding: var(--spacing-lg);
    overflow-y: auto;
}

.app-footer {
    grid-area: footer;
    background-color: var(--color-dark);
    color: var(--color-white);
    padding: var(--spacing-md);
    text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
    .app-container {
        grid-template-areas:
            "header"
            "main"
            "footer";
        grid-template-columns: 1fr;
    }

    .sidebar {
        display: none;
    }

    .global-search {
        max-width: 100%;
        margin: var(--spacing-sm) 0;
    }
}

/* Dashboard Grid */
.dashboard-overview {
    display: grid;
    gap: var(--spacing-lg);
}

.quick-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--spacing-md);
}
"""

    def _get_components_css(self) -> str:
        """Generate components.css"""
        return """/* CODITECT Dashboard - Component Styles */

/* Message Cards */
.message-list {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.message-card {
    position: relative;
}

.message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-sm);
    font-size: var(--font-size-small);
    color: #666;
}

.message-role {
    font-weight: 600;
    text-transform: uppercase;
}

.message-role.user {
    color: var(--color-primary);
}

.message-role.assistant {
    color: var(--color-secondary);
}

.message-content {
    line-height: 1.8;
}

.message-footer {
    margin-top: var(--spacing-sm);
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
}

/* Tabs */
.tab-bar {
    display: flex;
    gap: var(--spacing-sm);
    border-bottom: 2px solid var(--border-color);
    margin-bottom: var(--spacing-lg);
}

.tab-button {
    padding: var(--spacing-sm) var(--spacing-lg);
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    font-size: var(--font-size-base);
    color: var(--color-dark);
    transition: all 0.2s;
}

.tab-button:hover {
    background-color: var(--color-light);
}

.tab-button.active {
    border-bottom-color: var(--color-primary);
    color: var(--color-primary);
    font-weight: 600;
}

/* Pagination */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-lg);
}

.pagination button {
    padding: var(--spacing-sm);
    min-width: 40px;
}

.pagination button.active {
    background-color: var(--color-primary);
}
"""

    def _get_print_css(self) -> str:
        """Generate print.css for PDF exports"""
        return """/* CODITECT Dashboard - Print Styles */

@media print {
    .sidebar,
    .app-footer,
    .global-search,
    button,
    .pagination {
        display: none;
    }

    .app-container {
        display: block;
    }

    .main-content {
        padding: 0;
    }

    .message-card {
        page-break-inside: avoid;
        box-shadow: none;
        border: 1px solid var(--border-color);
    }

    @page {
        margin: 2cm;
    }
}
"""

    def _get_navigation_js(self) -> str:
        """Generate navigation.js stub"""
        return """// CODITECT Dashboard - Navigation System
console.log('✓ Navigation loaded');

// TODO: Implement tab switching
// TODO: Implement URL hash routing
// TODO: Implement sidebar navigation
"""

    def _get_data_loader_js(self) -> str:
        """Generate data-loader.js stub"""
        return """// CODITECT Dashboard - Data Loader
console.log('✓ Data Loader loaded');

// TODO: Implement JSON loading
// TODO: Implement caching
// TODO: Implement pagination
"""

    def _get_index_html(self, message_index, topics, files, checkpoints, commands) -> str:
        """Generate index.html"""
        total_messages = message_index['total_messages']
        checkpoint_count = len(checkpoints['checkpoints'])
        file_count = len(files['files'])
        command_count = len(commands['commands'])
        generated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CODITECT Knowledge Base Dashboard</title>
    <meta http-equiv="Content-Security-Policy" content="
        default-src 'self';
        script-src 'self' https://cdn.jsdelivr.net https://unpkg.com 'unsafe-inline';
        style-src 'self' 'unsafe-inline';
        img-src 'self' data:;
        connect-src 'none';
    ">
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/layout.css">
    <link rel="stylesheet" href="css/components.css">
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="app-header">
            <div class="logo">
                <h1>🧠 CODITECT Knowledge Base</h1>
            </div>
            <div class="global-search">
                <input type="search" id="global-search" placeholder="Search {total_messages:,} messages...">
            </div>
        </header>

        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <nav>
                <ul>
                    <li><a href="#overview">📊 Overview</a></li>
                    <li><a href="#timeline">📅 Timeline</a></li>
                    <li><a href="#topics">🏷️ Topics</a></li>
                    <li><a href="#files">📁 Files</a></li>
                    <li><a href="#checkpoints">💬 Sessions</a></li>
                    <li><a href="#commands">⚡ Commands</a></li>
                </ul>
            </nav>
        </aside>

        <!-- Main Content Area -->
        <main class="main-content">
            <div class="dashboard-overview">
                <!-- Quick Stats Panel -->
                <section class="quick-stats">
                    <div class="stat-card">
                        <h3>Total Messages</h3>
                        <p class="stat-value">{total_messages:,}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Checkpoints</h3>
                        <p class="stat-value">{checkpoint_count}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Files Referenced</h3>
                        <p class="stat-value">{file_count}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Commands Executed</h3>
                        <p class="stat-value">{command_count}</p>
                    </div>
                </section>

                <!-- Welcome Message -->
                <section style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2>Welcome to CODITECT Knowledge Base</h2>
                    <p style="margin: 1rem 0;">
                        This dashboard provides interactive access to <strong>{total_messages:,} conversation messages</strong>
                        from <strong>{checkpoint_count} sessions</strong>.
                    </p>
                    <p style="margin: 1rem 0;">
                        Navigate using the sidebar or use the search bar above to find specific conversations.
                    </p>
                    <p style="margin: 1rem 0;">
                        <strong>Phase 2 Status:</strong> Static site generator complete ✅ |
                        Full JavaScript interactivity coming in Task 1.3-1.5
                    </p>
                </section>

                <!-- Top Topics Preview -->
                <section style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h2>Top Topics</h2>
                    <ul style="list-style: none; padding: 0;">
                        {"".join([
                            f'<li style="padding: 0.5rem; margin: 0.25rem 0; background: #f5f5f5; border-radius: 4px;">'
                            f'<strong>{topic["display_name"]}</strong>: {topic["message_count"]:,} messages ({topic["percentage"]}%)</li>'
                            for topic in topics['topics'][:6]
                        ])}
                    </ul>
                </section>
            </div>
        </main>

        <!-- Footer -->
        <footer class="app-footer">
            <p>CODITECT Knowledge Base • Generated {generated_at} • {total_messages:,} messages</p>
        </footer>
    </div>

    <script src="js/navigation.js"></script>
    <script src="js/data-loader.js"></script>
</body>
</html>
"""

    def print_summary(self):
        """Print generation summary"""
        print("\n" + "="*80)
        print("DATA GENERATION COMPLETE")
        print("="*80)
        print(f"Messages exported:    {self.stats['messages_exported']:,}")
        print(f"Pages generated:      {self.stats['pages_generated']}")
        print(f"Topics exported:      {self.stats['topics_exported']}")
        print(f"Files exported:       {self.stats['files_exported']}")
        print(f"Checkpoints exported: {self.stats['checkpoints_exported']}")
        print(f"Commands exported:    {self.stats['commands_exported']:,}")
        print(f"Git commits exported: {self.stats['git_commits_exported']}")
        print("="*80)
        print(f"\n✓ Data files generated at: {self.output_dir}/data/")
        print(f"\n📊 To view dashboard: Open file://{self.output_dir.absolute()}/index.html in browser")
        print("\n💡 Note: HTML/CSS/JS files are source code (not generated)")
        print("   They are version-controlled via git and edited directly")


def main():
    """Main execution"""
    import sys

    # Paths
    script_dir = Path(__file__).parent
    db_path = script_dir.parent / 'knowledge.db'
    output_dir = script_dir.parent / 'dashboard'

    print("="*80)
    print("CODITECT DASHBOARD DATA GENERATOR")
    print("="*80)
    print(f"Database: {db_path}")
    print(f"Output:   {output_dir}/data/")
    print("="*80)
    print("\n⚡ Generating JSON data files only (HTML/CSS/JS are source code)")
    print("   Dashboard application files are managed via git, not generated\n")

    # Generate dashboard
    generator = DashboardGenerator(str(db_path), str(output_dir))

    try:
        generator.connect()
        generator.create_directories()

        # Export all data files
        message_index = generator.export_messages(page_size=100)
        topics = generator.export_topics()
        files = generator.export_files()
        checkpoints = generator.export_checkpoints()
        commands = generator.export_commands()
        git_commits = generator.export_git_commits(limit=500)

        print("\n✅ Data generation complete!")
        print("   HTML/CSS/JS files unchanged (managed via git)")

        generator.print_summary()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        generator.close()


if __name__ == '__main__':
    main()
