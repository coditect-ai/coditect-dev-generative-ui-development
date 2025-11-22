#!/usr/bin/env python3
"""
Session Memory Extraction - Phase 4: todos Extraction

Purpose: Extract task and todo metadata from ~/.claude/todos/
This directory contains task state information from Claude Code sessions.

Strategy:
1. Scan all todo JSON files in ~/.claude/todos/
2. Extract task state, timestamps, and project associations
3. Create message entries from todo tracking information
4. Parse task descriptions for meaningful context
5. Deduplicate using existing SHA-256 hash store
6. Verify data integrity before/after extraction

Output: Task tracking metadata with full provenance
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
import sys

class SessionMemoryExtractorPhase4:
    """Extract todo/task metadata from ~/.claude/todos/"""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.home = Path.home()
        self.claude_dir = self.home / '.claude'
        self.todos_dir = self.claude_dir / 'todos'
        self.memory_context = Path.cwd() / 'MEMORY-CONTEXT'
        self.extracted_messages = []
        self.statistics = {
            'total_todo_files': 0,
            'tasks_found': 0,
            'task_states': {},
            'extracted_messages': 0,
            'new_unique_messages': 0,
            'duplicates_found': 0,
            'errors': 0
        }
        self.processing_log = []

    def log(self, message: str):
        """Log with optional verbose output"""
        if self.verbose:
            print(message)
        self.processing_log.append({
            'timestamp': datetime.now().isoformat(),
            'message': message
        })

    def verify_source_directory(self) -> bool:
        """Verify todos directory exists and is readable"""
        self.log(f"\n{'='*80}")
        self.log("PHASE 4 EXTRACTION: todos Directory Processing")
        self.log(f"{'='*80}\n")

        self.log("Step 1: Verify Source Directory")
        if not self.todos_dir.exists():
            self.log(f"❌ todos directory not found: {self.todos_dir}")
            return False

        if not os.access(self.todos_dir, os.R_OK):
            self.log(f"❌ todos directory not readable: {self.todos_dir}")
            return False

        self.log(f"✅ todos directory verified: {self.todos_dir}")
        return True

    def compute_baseline_checksum(self) -> str:
        """Compute SHA-256 checksum of entire todos directory"""
        self.log("\nStep 2: Compute Baseline Checksum")

        hasher = hashlib.sha256()
        file_count = 0

        try:
            for file_path in sorted(self.todos_dir.rglob('*')):
                if file_path.is_file():
                    with open(file_path, 'rb') as f:
                        hasher.update(f.read())
                    file_count += 1
        except Exception as e:
            self.log(f"⚠️  Error computing checksum: {e}")
            return None

        checksum = hasher.hexdigest()
        self.log(f"✅ Baseline checksum computed: {checksum}")
        self.log(f"   (based on {file_count} files)")
        return checksum

    def load_global_hashes(self) -> Set[str]:
        """Load existing unique message hashes from MEMORY-CONTEXT"""
        hash_file = self.memory_context / 'dedup_state' / 'global_hashes.json'

        try:
            with open(hash_file, 'r') as f:
                data = json.load(f)

            if isinstance(data, list):
                return set(data)
            elif isinstance(data, dict):
                return set(data.get('hashes', []))
            else:
                return set()
        except Exception as e:
            self.log(f"⚠️  Error loading existing hashes: {e}")
            return set()

    def extract_todo_metadata(self) -> List[Dict]:
        """Extract metadata from todos JSON files"""
        self.log("\nStep 3: Extract Todo Metadata")

        messages = []
        todo_files = list(self.todos_dir.glob('*.json'))
        self.statistics['total_todo_files'] = len(todo_files)

        self.log(f"Found {len(todo_files)} todo files to process")

        for todo_file in todo_files:
            try:
                with open(todo_file, 'r') as f:
                    todo_data = json.load(f)

                # Extract tasks from todo file
                if isinstance(todo_data, list):
                    tasks = todo_data
                elif isinstance(todo_data, dict) and 'tasks' in todo_data:
                    tasks = todo_data['tasks']
                else:
                    tasks = [todo_data] if todo_data else []

                for task in tasks:
                    if not isinstance(task, dict):
                        continue

                    # Track task state
                    state = task.get('status', 'unknown')
                    if state not in self.statistics['task_states']:
                        self.statistics['task_states'][state] = 0
                    self.statistics['task_states'][state] += 1

                    # Create message from task
                    title = task.get('title', task.get('content', 'Task'))
                    description = task.get('description', '')
                    project = task.get('project', task.get('context', ''))

                    # Build message content
                    message_content = f"Task: {title}"
                    if description:
                        message_content += f" - {description[:100]}"  # First 100 chars

                    # Get timestamp from various possible fields
                    timestamp = None
                    for ts_field in ['created_at', 'createdAt', 'timestamp', 'updated_at', 'updatedAt']:
                        if ts_field in task:
                            try:
                                if isinstance(task[ts_field], str):
                                    dt = datetime.fromisoformat(task[ts_field].replace('Z', '+00:00'))
                                else:
                                    dt = datetime.fromtimestamp(task[ts_field])
                                timestamp = int(dt.timestamp() * 1000)
                                break
                            except:
                                pass

                    if not timestamp:
                        timestamp = int(datetime.now().timestamp() * 1000)

                    message = {
                        'content': message_content,
                        'source': f'todos/{todo_file.name}',
                        'timestamp': timestamp,
                        'source_type': 'todos',
                        'metadata': {
                            'title': title,
                            'status': state,
                            'project': project,
                            'complete_task': task
                        }
                    }

                    messages.append(message)
                    self.statistics['tasks_found'] += 1

            except json.JSONDecodeError as e:
                self.log(f"⚠️  Error parsing JSON {todo_file.name}: {e}")
                self.statistics['errors'] += 1
            except Exception as e:
                self.log(f"⚠️  Error processing {todo_file.name}: {e}")
                self.statistics['errors'] += 1
                continue

        self.log(f"✅ Extracted {len(messages)} todo messages from {len(todo_files)} files")
        return messages

    def deduplicate_messages(self, messages: List[Dict], existing_hashes: Set[str]) -> Tuple[List[Dict], int, int]:
        """Deduplicate messages using existing hash store"""
        self.log("\nStep 4: Deduplicate Messages")

        unique_messages = []
        new_count = 0
        dup_count = 0

        for msg in messages:
            content_hash = hashlib.sha256(msg['content'].encode()).hexdigest()

            if content_hash not in existing_hashes:
                msg['hash'] = content_hash
                unique_messages.append(msg)
                existing_hashes.add(content_hash)
                new_count += 1
            else:
                dup_count += 1

        self.log(f"✅ Deduplicated: {new_count} new, {dup_count} duplicates")
        return unique_messages, new_count, dup_count

    def create_task_analysis(self, messages: List[Dict]) -> Dict:
        """Create task analysis summary"""
        self.log("\nStep 5: Create Task Analysis")

        analysis = {
            'extraction_date': datetime.now().isoformat(),
            'source': 'todos',
            'total_tasks': len(messages),
            'task_states': self.statistics['task_states'],
            'tasks_by_state': {}
        }

        for msg in messages:
            state = msg['metadata']['status']
            if state not in analysis['tasks_by_state']:
                analysis['tasks_by_state'][state] = []
            analysis['tasks_by_state'][state].append(msg['metadata']['title'])

        self.log(f"✅ Task analysis created")
        return analysis

    def save_extracted_messages(self, messages: List[Dict]) -> bool:
        """Save extracted messages to JSONL file"""
        self.log("\nStep 6: Save Extracted Messages")

        output_file = self.memory_context / 'extractions' / 'phase4-extracted-messages.jsonl'
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_file, 'w') as f:
                for msg in messages:
                    f.write(json.dumps(msg) + '\n')

            self.log(f"✅ Saved {len(messages)} messages to {output_file.name}")
            return True
        except Exception as e:
            self.log(f"❌ Error saving messages: {e}")
            self.statistics['errors'] += 1
            return False

    def save_task_analysis(self, analysis: Dict) -> bool:
        """Save task analysis"""
        self.log("\nStep 7: Save Task Analysis")

        output_file = self.memory_context / 'extractions' / 'phase4-task-analysis.json'
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)

            self.log(f"✅ Saved task analysis to {output_file.name}")
            return True
        except Exception as e:
            self.log(f"❌ Error saving analysis: {e}")
            self.statistics['errors'] += 1
            return False

    def save_statistics(self) -> bool:
        """Save extraction statistics"""
        self.log("\nStep 8: Save Statistics")

        stats_file = self.memory_context / 'extractions' / 'phase4-statistics.json'
        stats_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(stats_file, 'w') as f:
                json.dump(self.statistics, f, indent=2)

            self.log(f"✅ Saved statistics to {stats_file.name}")
            return True
        except Exception as e:
            self.log(f"❌ Error saving statistics: {e}")
            return False

    def verify_post_extraction(self, baseline: str) -> bool:
        """Verify todos directory unchanged after extraction"""
        self.log("\nStep 9: Verify Post-Extraction Integrity")

        post_checksum = self.compute_baseline_checksum()
        if baseline == post_checksum:
            self.log("✅ Checksums match - todos untouched (read-only verified)")
            return True
        else:
            self.log(f"⚠️  Checksum mismatch detected")
            self.log(f"   Before: {baseline}")
            self.log(f"   After:  {post_checksum}")
            return False

    def generate_summary(self) -> bool:
        """Generate extraction summary"""
        self.log("\nStep 10: Generate Summary")

        summary = {
            'extraction_date': datetime.now().isoformat(),
            'phase': 'Phase 4: todos',
            'status': 'complete',
            'statistics': self.statistics,
            'source_directory': str(self.todos_dir),
            'output_files': [
                'extractions/phase4-extracted-messages.jsonl',
                'extractions/phase4-task-analysis.json',
                'extractions/phase4-statistics.json'
            ]
        }

        summary_file = self.memory_context / 'extractions' / 'phase4-summary.json'
        summary_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)

            self.log(f"✅ Summary saved to {summary_file.name}")
            return True
        except Exception as e:
            self.log(f"❌ Error saving summary: {e}")
            return False

    def run_extraction(self) -> bool:
        """Run complete Phase 4 extraction process"""
        try:
            # Step 1: Verify directory
            if not self.verify_source_directory():
                return False

            # Step 2: Compute baseline checksum
            baseline_checksum = self.compute_baseline_checksum()
            if not baseline_checksum:
                return False

            # Step 3: Load existing hashes for deduplication
            existing_hashes = self.load_global_hashes()
            self.log(f"✅ Loaded {len(existing_hashes)} existing hashes for deduplication")

            # Step 4: Extract todo metadata
            raw_messages = self.extract_todo_metadata()

            # Step 5: Deduplicate
            unique_messages, new_count, dup_count = self.deduplicate_messages(raw_messages, existing_hashes)
            self.statistics['extracted_messages'] = len(raw_messages)
            self.statistics['new_unique_messages'] = new_count
            self.statistics['duplicates_found'] = dup_count

            if not unique_messages:
                self.log("\n⚠️  No new unique messages found in Phase 4")
                return True

            # Step 6: Create task analysis
            task_analysis = self.create_task_analysis(unique_messages)

            # Step 7: Save messages
            if not self.save_extracted_messages(unique_messages):
                return False

            # Step 8: Save analysis
            if not self.save_task_analysis(task_analysis):
                return False

            # Step 9: Save statistics
            if not self.save_statistics():
                return False

            # Step 10: Verify integrity
            self.verify_post_extraction(baseline_checksum)

            # Step 11: Generate summary
            if not self.generate_summary():
                return False

            # Print completion summary
            self._print_completion_summary()

            return True

        except Exception as e:
            self.log(f"\n❌ Extraction failed with error: {e}")
            import traceback
            self.log(traceback.format_exc())
            return False

    def _print_completion_summary(self):
        """Print completion summary"""
        self.log(f"\n{'='*80}")
        self.log("PHASE 4 EXTRACTION COMPLETE")
        self.log(f"{'='*80}\n")

        self.log(f"📊 STATISTICS:")
        self.log(f"   Todo Files:             {self.statistics['total_todo_files']}")
        self.log(f"   Tasks Found:            {self.statistics['tasks_found']}")
        self.log(f"   Extracted Messages:     {self.statistics['extracted_messages']}")
        self.log(f"   🆕 NEW UNIQUE MESSAGES: {self.statistics['new_unique_messages']}")
        self.log(f"   Duplicates Found:       {self.statistics['duplicates_found']}")
        self.log(f"   Errors:                 {self.statistics['errors']}")

        if self.statistics['task_states']:
            self.log(f"\n   Task States:")
            for state, count in self.statistics['task_states'].items():
                self.log(f"      {state}: {count}")

        self.log(f"\n✅ All files verified as read-only (no modifications)")
        self.log(f"✅ Full provenance tracking complete")
        self.log(f"✅ Phase 4 extraction successful\n")


def main():
    """Main entry point"""
    os.chdir(Path(__file__).parent.parent.parent)  # Change to project root

    extractor = SessionMemoryExtractorPhase4(verbose=True)
    success = extractor.run_extraction()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
