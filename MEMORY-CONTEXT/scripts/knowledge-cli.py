#!/usr/bin/env python3
"""
CODITECT Knowledge CLI - Search and Navigate Indexed Messages

Usage:
    python knowledge-cli.py search "git submodule"
    python knowledge-cli.py topics
    python knowledge-cli.py files
    python knowledge-cli.py checkpoint 2025-11-22-HOOKS
    python knowledge-cli.py stats
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any
import argparse
from datetime import datetime


BASE_DIR = Path(__file__).parent.parent
DB_FILE = BASE_DIR / "knowledge.db"


class KnowledgeCLI:
    """Command-line interface for knowledge search"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Connect to database"""
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found: {self.db_path}\n"
                f"Run: python index-messages.py first"
            )
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

    def search(self, query: str, limit: int = 10, topic: str = None):
        """Full-text search messages"""
        cursor = self.conn.cursor()

        print(f"\n🔍 Searching for: '{query}'")
        if topic:
            print(f"   Filtered by topic: {topic}")

        # Build FTS query
        sql = '''
            SELECT
                m.hash,
                m.role,
                m.content,
                m.checkpoint_id,
                m.first_seen,
                messages_fts.rank
            FROM messages_fts
            JOIN messages m ON messages_fts.hash = m.hash
        '''

        params = [query]

        # Add topic filter if specified
        if topic:
            sql += '''
                JOIN message_tags mt ON m.hash = mt.message_hash
                JOIN tags t ON mt.tag_id = t.id
            '''

        sql += ' WHERE messages_fts MATCH ?'

        if topic:
            sql += ' AND t.name = ?'
            params.append(f'topic:{topic}')

        sql += ' ORDER BY rank LIMIT ?'
        params.append(limit)

        cursor.execute(sql, params)
        results = cursor.fetchall()

        if not results:
            print("  ❌ No results found")
            return

        print(f"  ✅ Found {len(results)} results\n")
        print("=" * 80)

        for idx, row in enumerate(results, 1):
            self._print_message(row, idx)
            print()

    def list_topics(self):
        """List all topics with message counts"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT t.name, COUNT(mt.message_hash) as count
            FROM tags t
            JOIN message_tags mt ON t.id = mt.tag_id
            WHERE t.category = 'topic'
            GROUP BY t.name
            ORDER BY count DESC
        ''')

        results = cursor.fetchall()

        print("\n📚 Available Topics:\n")
        print("=" * 80)

        for row in results:
            topic_name = row['name'].replace('topic:', '')
            count = row['count']
            bar = "█" * min(50, count // 20)
            print(f"  {topic_name:20} {count:>5} msgs  {bar}")

        print("=" * 80)
        print(f"\nUsage: python knowledge-cli.py search 'query' --topic <topic>")

    def list_files(self, limit: int = 50):
        """List most referenced files"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT filepath, COUNT(*) as count
            FROM file_references
            GROUP BY filepath
            ORDER BY count DESC
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()

        print(f"\n📁 Top {limit} Referenced Files:\n")
        print("=" * 80)

        for row in results:
            filepath = row['filepath']
            count = row['count']
            print(f"  {filepath:60} ({count} refs)")

        print("=" * 80)
        print(f"\nUsage: python knowledge-cli.py file <filepath>")

    def show_file_history(self, filepath: str):
        """Show all messages referencing a specific file"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT
                m.hash,
                m.role,
                m.content,
                m.checkpoint_id,
                m.first_seen,
                fr.operation
            FROM file_references fr
            JOIN messages m ON fr.message_hash = m.hash
            WHERE fr.filepath = ?
            ORDER BY m.first_seen DESC
        ''', (filepath,))

        results = cursor.fetchall()

        if not results:
            print(f"  ❌ No messages found for file: {filepath}")
            return

        print(f"\n📄 File History: {filepath}")
        print(f"   {len(results)} messages\n")
        print("=" * 80)

        for idx, row in enumerate(results, 1):
            self._print_message(row, idx)
            print()

    def show_checkpoint(self, checkpoint_id: str):
        """Show all messages in a checkpoint/session"""
        cursor = self.conn.cursor()

        # Get checkpoint info
        cursor.execute('''
            SELECT * FROM checkpoints WHERE id LIKE ?
        ''', (f'%{checkpoint_id}%',))

        checkpoint = cursor.fetchone()

        if not checkpoint:
            print(f"  ❌ Checkpoint not found: {checkpoint_id}")
            return

        full_id = checkpoint['id']

        print(f"\n📅 Checkpoint: {full_id}")
        print(f"   Date: {checkpoint['date']}")
        print(f"   Messages: {checkpoint['message_count']}\n")
        print("=" * 80)

        # Get messages
        cursor.execute('''
            SELECT * FROM messages
            WHERE checkpoint_id = ?
            ORDER BY message_index
        ''', (full_id,))

        for idx, row in enumerate(cursor.fetchall(), 1):
            self._print_message(row, idx)
            print()

    def list_checkpoints(self, limit: int = 30):
        """List recent checkpoints"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT id, date, message_count
            FROM checkpoints
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()

        print(f"\n📅 Recent Checkpoints (Top {limit}):\n")
        print("=" * 80)

        for row in results:
            checkpoint_id = row['id']
            date = row['date']
            count = row['message_count']
            print(f"  {date:15} {checkpoint_id:50} ({count} msgs)")

        print("=" * 80)
        print(f"\nUsage: python knowledge-cli.py checkpoint <checkpoint-id>")

    def list_commands(self, cmd_type: str = None, limit: int = 20):
        """List commands executed"""
        cursor = self.conn.cursor()

        if cmd_type:
            cursor.execute('''
                SELECT c.command_text, c.command_type, m.checkpoint_id
                FROM commands c
                JOIN messages m ON c.message_hash = m.hash
                WHERE c.command_type = ?
                ORDER BY m.first_seen DESC
                LIMIT ?
            ''', (cmd_type, limit))

            print(f"\n⚡ Recent {cmd_type.upper()} Commands:\n")
        else:
            cursor.execute('''
                SELECT command_type, COUNT(*) as count
                FROM commands
                GROUP BY command_type
                ORDER BY count DESC
            ''')

            results = cursor.fetchall()
            print(f"\n⚡ Command Types:\n")
            print("=" * 80)

            for row in results:
                print(f"  {row['command_type']:15} {row['count']:>6} commands")

            print("=" * 80)
            print(f"\nUsage: python knowledge-cli.py commands --type git")
            return

        print("=" * 80)

        for row in cursor.fetchall():
            cmd = row['command_text']
            if len(cmd) > 70:
                cmd = cmd[:67] + "..."
            print(f"  {cmd}")

        print("=" * 80)

    def show_stats(self):
        """Show knowledge base statistics"""
        cursor = self.conn.cursor()

        print("\n" + "=" * 80)
        print("CODITECT KNOWLEDGE BASE STATISTICS")
        print("=" * 80)

        # Messages
        cursor.execute('SELECT COUNT(*) FROM messages')
        total = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM messages WHERE role = "user"')
        user = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM messages WHERE role = "assistant"')
        assistant = cursor.fetchone()[0]

        print(f"\n📊 Messages:")
        print(f"  Total:     {total:>6}")
        print(f"  User:      {user:>6} ({user/total*100:.1f}%)")
        print(f"  Assistant: {assistant:>6} ({assistant/total*100:.1f}%)")

        # Checkpoints
        cursor.execute('SELECT COUNT(*) FROM checkpoints')
        checkpoints = cursor.fetchone()[0]
        print(f"\n📅 Checkpoints: {checkpoints}")

        # Date range
        cursor.execute('''
            SELECT MIN(date), MAX(date) FROM checkpoints WHERE date != ""
        ''')
        row = cursor.fetchone()
        print(f"  Date Range: {row[0]} to {row[1]}")

        # Top topics
        cursor.execute('''
            SELECT t.name, COUNT(mt.message_hash) as count
            FROM tags t
            JOIN message_tags mt ON t.id = mt.tag_id
            WHERE t.category = 'topic'
            GROUP BY t.name
            ORDER BY count DESC
            LIMIT 5
        ''')

        print(f"\n🏷️  Top Topics:")
        for row in cursor.fetchall():
            topic = row['name'].replace('topic:', '')
            count = row['count']
            print(f"  {topic:20} {count:>6} mentions")

        # File operations
        cursor.execute('SELECT COUNT(DISTINCT filepath) FROM file_references')
        files = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM file_references WHERE operation = "write"')
        writes = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM file_references WHERE operation = "read"')
        reads = cursor.fetchone()[0]

        print(f"\n📁 Files:")
        print(f"  Unique:    {files:>6}")
        print(f"  Writes:    {writes:>6}")
        print(f"  Reads:     {reads:>6}")

        # Commands
        cursor.execute('SELECT COUNT(*) FROM commands')
        total_cmds = cursor.fetchone()[0]
        print(f"\n⚡ Commands: {total_cmds}")

        print("\n" + "=" * 80)

    def _print_message(self, row: sqlite3.Row, index: int = None):
        """Pretty print a message"""
        role = row['role']
        content = row['content']
        checkpoint = row['checkpoint_id']
        msg_hash = row['hash'][:8]

        # Truncate long content
        if len(content) > 200:
            content = content[:197] + "..."

        role_emoji = "👤" if role == "user" else "🤖"

        if index:
            print(f"[{index}] {role_emoji} {role.upper()} ({msg_hash})")
        else:
            print(f"{role_emoji} {role.upper()} ({msg_hash})")

        print(f"    Checkpoint: {checkpoint}")
        print(f"    {content}")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='CODITECT Knowledge CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python knowledge-cli.py search "git submodule"
  python knowledge-cli.py search "deployment" --topic deployment --limit 20
  python knowledge-cli.py topics
  python knowledge-cli.py files
  python knowledge-cli.py file PROJECT-PLAN.md
  python knowledge-cli.py checkpoints
  python knowledge-cli.py checkpoint 2025-11-22
  python knowledge-cli.py commands
  python knowledge-cli.py commands --type git
  python knowledge-cli.py stats
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search messages')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Max results')
    search_parser.add_argument('--topic', help='Filter by topic')

    # Topics command
    subparsers.add_parser('topics', help='List all topics')

    # Files command
    files_parser = subparsers.add_parser('files', help='List referenced files')
    files_parser.add_argument('--limit', type=int, default=50, help='Max files')

    # File command
    file_parser = subparsers.add_parser('file', help='Show file history')
    file_parser.add_argument('filepath', help='File path')

    # Checkpoints command
    checkpoints_parser = subparsers.add_parser('checkpoints', help='List checkpoints')
    checkpoints_parser.add_argument('--limit', type=int, default=30, help='Max checkpoints')

    # Checkpoint command
    checkpoint_parser = subparsers.add_parser('checkpoint', help='Show checkpoint messages')
    checkpoint_parser.add_argument('checkpoint_id', help='Checkpoint ID (partial match)')

    # Commands command
    commands_parser = subparsers.add_parser('commands', help='List commands')
    commands_parser.add_argument('--type', help='Command type (git, docker, gcloud, etc.)')
    commands_parser.add_argument('--limit', type=int, default=20, help='Max commands')

    # Stats command
    subparsers.add_parser('stats', help='Show statistics')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Create CLI
    cli = KnowledgeCLI(DB_FILE)

    try:
        cli.connect()

        if args.command == 'search':
            cli.search(args.query, args.limit, args.topic)

        elif args.command == 'topics':
            cli.list_topics()

        elif args.command == 'files':
            cli.list_files(args.limit)

        elif args.command == 'file':
            cli.show_file_history(args.filepath)

        elif args.command == 'checkpoints':
            cli.list_checkpoints(args.limit)

        elif args.command == 'checkpoint':
            cli.show_checkpoint(args.checkpoint_id)

        elif args.command == 'commands':
            cli.list_commands(args.type, args.limit)

        elif args.command == 'stats':
            cli.show_stats()

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        cli.close()

    return 0


if __name__ == '__main__':
    exit(main())
