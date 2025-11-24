#!/usr/bin/env python3
"""
CODITECT Knowledge Indexing System
Creates searchable SQLite database from unique_messages.jsonl

Usage:
    python index-messages.py
    python index-messages.py --rebuild
"""

import json
import sqlite3
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any
import argparse

# Paths
BASE_DIR = Path(__file__).parent.parent
MESSAGES_FILE = BASE_DIR / "dedup_state" / "unique_messages.jsonl"
DB_FILE = BASE_DIR / "knowledge.db"
CHECKPOINT_INDEX = BASE_DIR / "dedup_state" / "checkpoint_index.json"


class MessageIndexer:
    """Index messages into searchable SQLite database"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None
        self.stats = defaultdict(int)

    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

    def create_schema(self):
        """Create database schema with FTS5 search"""
        print("Creating database schema...")

        cursor = self.conn.cursor()

        # Core messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                hash TEXT PRIMARY KEY,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                checkpoint_id TEXT NOT NULL,
                message_index INTEGER
            )
        ''')

        # Full-text search virtual table
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
                hash UNINDEXED,
                content,
                checkpoint_id UNINDEXED,
                tokenize='porter'
            )
        ''')

        # Checkpoints table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkpoints (
                id TEXT PRIMARY KEY,
                title TEXT,
                date TEXT,
                message_count INTEGER DEFAULT 0
            )
        ''')

        # Tags table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT
            )
        ''')

        # Message-tag junction table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_tags (
                message_hash TEXT,
                tag_id INTEGER,
                confidence REAL DEFAULT 1.0,
                PRIMARY KEY (message_hash, tag_id),
                FOREIGN KEY (message_hash) REFERENCES messages(hash),
                FOREIGN KEY (tag_id) REFERENCES tags(id)
            )
        ''')

        # File references table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_references (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_hash TEXT NOT NULL,
                filepath TEXT NOT NULL,
                operation TEXT,
                FOREIGN KEY (message_hash) REFERENCES messages(hash)
            )
        ''')

        # Commands table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_hash TEXT NOT NULL,
                command_type TEXT,
                command_text TEXT NOT NULL,
                FOREIGN KEY (message_hash) REFERENCES messages(hash)
            )
        ''')

        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_checkpoint ON messages(checkpoint_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_references_filepath ON file_references(filepath)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_commands_type ON commands(command_type)')

        self.conn.commit()
        print("✓ Schema created")

    def classify_message(self, content: str) -> List[str]:
        """Classify message into topics/categories"""
        tags = []
        content_lower = content.lower()

        # Topic detection
        if any(kw in content_lower for kw in ['agent', 'orchestrat', 'subagent']):
            tags.append('topic:agents')
        if 'submodule' in content_lower:
            tags.append('topic:submodules')
        if any(kw in content_lower for kw in ['deploy', 'docker', 'gcp', 'kubernetes', 'cloud build']):
            tags.append('topic:deployment')
        if any(kw in content_lower for kw in ['document', 'readme', 'claude.md']):
            tags.append('topic:documentation')
        if 'test' in content_lower and not 'attest' in content_lower:
            tags.append('topic:testing')
        if 'security' in content_lower:
            tags.append('topic:security')

        # Action detection
        if content.startswith('Read('):
            tags.append('action:read-file')
        if content.startswith('Write('):
            tags.append('action:write-file')
        if content.startswith('Edit('):
            tags.append('action:edit-file')
        if content.startswith('Bash('):
            tags.append('action:shell-command')
        if content.startswith('Task('):
            tags.append('action:task-invocation')

        # Artifact detection
        if '.md' in content and any(a in content for a in ['Write', 'Edit']):
            tags.append('artifact:documentation')
        if '.py' in content:
            tags.append('artifact:python-code')
        if '.sh' in content:
            tags.append('artifact:shell-script')
        if any(ext in content for ext in ['.json', '.yaml', '.yml']):
            tags.append('artifact:config-file')

        return tags

    def extract_files(self, content: str) -> List[Dict[str, str]]:
        """Extract file references from message content"""
        files = []

        # Pattern for file paths
        file_pattern = r'([a-zA-Z0-9_/-]+\.[a-zA-Z0-9]+)'
        matches = re.findall(file_pattern, content)

        # Determine operation
        operation = None
        if content.startswith('Read('):
            operation = 'read'
        elif content.startswith('Write('):
            operation = 'write'
        elif content.startswith('Edit('):
            operation = 'edit'
        else:
            operation = 'mention'

        for filepath in matches[:5]:  # Top 5 files per message
            # Filter out false positives
            if not any(skip in filepath for skip in ['http://', 'https://', '127.0.0.1', 'localhost']):
                files.append({'filepath': filepath, 'operation': operation})

        return files

    def extract_command(self, content: str) -> Dict[str, str]:
        """Extract command from Bash() tool call"""
        if not content.startswith('Bash('):
            return None

        # Extract command text
        match = re.match(r'Bash\(([^)]+)\)', content)
        if not match:
            return None

        cmd_text = match.group(1).strip()

        # Determine command type
        cmd_type = 'bash'
        if cmd_text.startswith('git '):
            cmd_type = 'git'
        elif cmd_text.startswith('docker '):
            cmd_type = 'docker'
        elif cmd_text.startswith('gcloud '):
            cmd_type = 'gcloud'
        elif cmd_text.startswith('python'):
            cmd_type = 'python'

        return {'command_type': cmd_type, 'command_text': cmd_text}

    def get_or_create_tag(self, tag_name: str) -> int:
        """Get existing tag ID or create new tag"""
        cursor = self.conn.cursor()

        # Parse tag category
        category = tag_name.split(':')[0] if ':' in tag_name else 'other'

        # Try to find existing tag
        cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
        row = cursor.fetchone()

        if row:
            return row[0]

        # Create new tag
        cursor.execute('INSERT INTO tags (name, category) VALUES (?, ?)', (tag_name, category))
        self.conn.commit()
        return cursor.lastrowid

    def index_message(self, msg_data: Dict[str, Any]):
        """Index a single message"""
        try:
            msg_hash = msg_data.get('hash')
            message = msg_data.get('message', {})
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            first_seen = msg_data.get('first_seen', '')
            checkpoint = msg_data.get('checkpoint', '')
            msg_index = message.get('index', 0)

            cursor = self.conn.cursor()

            # Insert message
            cursor.execute('''
                INSERT OR REPLACE INTO messages (hash, role, content, first_seen, checkpoint_id, message_index)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (msg_hash, role, content, first_seen, checkpoint, msg_index))

            # Insert into FTS
            cursor.execute('''
                INSERT OR REPLACE INTO messages_fts (hash, content, checkpoint_id)
                VALUES (?, ?, ?)
            ''', (msg_hash, content, checkpoint))

            # Classify and tag
            tags = self.classify_message(content)
            for tag_name in tags:
                tag_id = self.get_or_create_tag(tag_name)
                cursor.execute('''
                    INSERT OR IGNORE INTO message_tags (message_hash, tag_id)
                    VALUES (?, ?)
                ''', (msg_hash, tag_id))

            # Extract file references
            files = self.extract_files(content)
            for file_info in files:
                cursor.execute('''
                    INSERT INTO file_references (message_hash, filepath, operation)
                    VALUES (?, ?, ?)
                ''', (msg_hash, file_info['filepath'], file_info['operation']))

            # Extract commands
            cmd_info = self.extract_command(content)
            if cmd_info:
                cursor.execute('''
                    INSERT INTO commands (message_hash, command_type, command_text)
                    VALUES (?, ?, ?)
                ''', (msg_hash, cmd_info['command_type'], cmd_info['command_text']))

            # Update checkpoint
            cursor.execute('''
                INSERT OR IGNORE INTO checkpoints (id, title, date)
                VALUES (?, ?, ?)
            ''', (checkpoint, checkpoint, checkpoint.split('-')[0] if '-' in checkpoint else ''))

            cursor.execute('''
                UPDATE checkpoints SET message_count = message_count + 1
                WHERE id = ?
            ''', (checkpoint,))

            self.stats['indexed'] += 1
            self.stats[f'role_{role}'] += 1

        except Exception as e:
            print(f"Error indexing message {msg_hash}: {e}")
            self.stats['errors'] += 1

    def index_all_messages(self, messages_file: Path):
        """Index all messages from JSONL file"""
        print(f"Indexing messages from {messages_file}...")

        with open(messages_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    msg_data = json.loads(line)
                    self.index_message(msg_data)

                    if line_num % 1000 == 0:
                        self.conn.commit()
                        print(f"  Processed {line_num} messages...")

                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON at line {line_num}")
                    self.stats['errors'] += 1

        self.conn.commit()
        print(f"✓ Indexed {self.stats['indexed']} messages")

    def print_stats(self):
        """Print indexing statistics"""
        print("\n" + "=" * 80)
        print("INDEXING STATISTICS")
        print("=" * 80)

        cursor = self.conn.cursor()

        # Message counts
        cursor.execute('SELECT COUNT(*) FROM messages')
        total_messages = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM messages WHERE role = "user"')
        user_messages = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM messages WHERE role = "assistant"')
        assistant_messages = cursor.fetchone()[0]

        print(f"\n📊 Messages:")
        print(f"  Total:     {total_messages:>6}")
        print(f"  User:      {user_messages:>6}")
        print(f"  Assistant: {assistant_messages:>6}")

        # Checkpoints
        cursor.execute('SELECT COUNT(*) FROM checkpoints')
        total_checkpoints = cursor.fetchone()[0]
        print(f"\n📅 Checkpoints: {total_checkpoints}")

        # Tags
        cursor.execute('''
            SELECT t.name, COUNT(mt.message_hash) as count
            FROM tags t
            JOIN message_tags mt ON t.id = mt.tag_id
            GROUP BY t.name
            ORDER BY count DESC
            LIMIT 10
        ''')
        print(f"\n🏷️  Top Tags:")
        for row in cursor.fetchall():
            print(f"  {row[0]:30} {row[1]:>6}")

        # Files
        cursor.execute('SELECT COUNT(DISTINCT filepath) FROM file_references')
        unique_files = cursor.fetchone()[0]
        print(f"\n📁 Unique Files: {unique_files}")

        # Commands
        cursor.execute('''
            SELECT command_type, COUNT(*) as count
            FROM commands
            GROUP BY command_type
            ORDER BY count DESC
        ''')
        print(f"\n⚡ Commands:")
        for row in cursor.fetchall():
            print(f"  {row[0]:15} {row[1]:>6}")

        print("\n" + "=" * 80)
        print(f"✅ Database created: {self.db_path}")
        print("=" * 80)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='Index CODITECT conversation messages')
    parser.add_argument('--rebuild', action='store_true', help='Rebuild database from scratch')
    args = parser.parse_args()

    # Remove existing database if rebuilding
    if args.rebuild and DB_FILE.exists():
        print(f"Removing existing database: {DB_FILE}")
        DB_FILE.unlink()

    # Check input file exists
    if not MESSAGES_FILE.exists():
        print(f"Error: Messages file not found: {MESSAGES_FILE}")
        return 1

    # Create indexer
    indexer = MessageIndexer(DB_FILE)

    try:
        indexer.connect()
        indexer.create_schema()
        indexer.index_all_messages(MESSAGES_FILE)
        indexer.print_stats()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        indexer.close()

    print(f"\n✅ Indexing complete!")
    print(f"\nNext steps:")
    print(f"  1. Search: python knowledge-cli.py search 'your query'")
    print(f"  2. Browse: python knowledge-cli.py topics")
    print(f"  3. Files: python knowledge-cli.py files")

    return 0


if __name__ == '__main__':
    exit(main())
