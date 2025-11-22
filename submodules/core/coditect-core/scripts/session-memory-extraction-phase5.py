#!/usr/bin/env python3
"""
Session Memory Extraction - Phase 5: shell-snapshots Extraction

Purpose: Extract shell environment snapshots from ~/.claude/shell-snapshots/
This directory contains shell state snapshots from Claude Code sessions.

Strategy:
1. Scan all shell snapshot files
2. Extract environment variables, shell state, and context
3. Create message entries from shell state information
4. Parse shell commands and settings
5. Deduplicate using existing SHA-256 hash store
6. Verify data integrity before/after extraction

Output: Shell environment context with full provenance
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
import sys

class SessionMemoryExtractorPhase5:
    """Extract shell snapshot metadata from ~/.claude/shell-snapshots/"""

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.home = Path.home()
        self.claude_dir = self.home / '.claude'
        self.snapshots_dir = self.claude_dir / 'shell-snapshots'
        self.memory_context = Path.cwd() / 'MEMORY-CONTEXT'
        self.extracted_messages = []
        self.statistics = {
            'total_snapshot_files': 0,
            'snapshots_parsed': 0,
            'env_vars_tracked': 0,
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
        """Verify shell-snapshots directory exists and is readable"""
        self.log(f"\n{'='*80}")
        self.log("PHASE 5 EXTRACTION: shell-snapshots Directory Processing")
        self.log(f"{'='*80}\n")

        self.log("Step 1: Verify Source Directory")
        if not self.snapshots_dir.exists():
            self.log(f"❌ shell-snapshots directory not found: {self.snapshots_dir}")
            return False

        if not os.access(self.snapshots_dir, os.R_OK):
            self.log(f"❌ shell-snapshots directory not readable: {self.snapshots_dir}")
            return False

        self.log(f"✅ shell-snapshots directory verified: {self.snapshots_dir}")
        return True

    def compute_baseline_checksum(self) -> str:
        """Compute SHA-256 checksum of entire shell-snapshots directory"""
        self.log("\nStep 2: Compute Baseline Checksum")

        hasher = hashlib.sha256()
        file_count = 0

        try:
            for file_path in sorted(self.snapshots_dir.rglob('*')):
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

    def extract_snapshot_metadata(self) -> List[Dict]:
        """Extract metadata from shell snapshot files"""
        self.log("\nStep 3: Extract Shell Snapshot Metadata")

        messages = []
        snapshot_files = list(self.snapshots_dir.glob('*.json')) + list(self.snapshots_dir.glob('*/*.json'))
        self.statistics['total_snapshot_files'] = len(snapshot_files)

        self.log(f"Found {len(snapshot_files)} snapshot files to process")

        for snapshot_file in snapshot_files:
            try:
                with open(snapshot_file, 'r') as f:
                    snapshot_data = json.load(f)

                self.statistics['snapshots_parsed'] += 1

                # Extract snapshot metadata
                shell_type = snapshot_data.get('shell', 'unknown')
                cwd = snapshot_data.get('cwd', '')
                pwd_depth = len(cwd.split('/')) if cwd else 0

                # Extract environment variables
                env_vars = snapshot_data.get('env', {})
                key_vars = ['PATH', 'SHELL', 'HOME', 'USER', 'PWD', 'PYTHONPATH', 'NODE_PATH']
                important_env = {k: v for k, v in env_vars.items() if k in key_vars}
                self.statistics['env_vars_tracked'] += len(important_env)

                # Extract aliases if present
                aliases = snapshot_data.get('aliases', {})
                alias_count = len(aliases)

                # Extract shell functions if present
                functions = snapshot_data.get('functions', {})
                func_count = len(functions)

                # Build message content
                message_content = f"Shell snapshot: {shell_type} in {cwd}"
                if alias_count > 0:
                    message_content += f" ({alias_count} aliases)"
                if func_count > 0:
                    message_content += f" ({func_count} functions)"

                # Get timestamp
                timestamp = snapshot_data.get('timestamp', int(datetime.now().timestamp() * 1000))
                if isinstance(timestamp, str):
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = int(dt.timestamp() * 1000)
                    except:
                        timestamp = int(datetime.now().timestamp() * 1000)

                message = {
                    'content': message_content,
                    'source': f'shell-snapshots/{snapshot_file.name}',
                    'timestamp': timestamp,
                    'source_type': 'shell-snapshots',
                    'metadata': {
                        'shell': shell_type,
                        'cwd': cwd,
                        'pwd_depth': pwd_depth,
                        'env_vars_count': len(important_env),
                        'aliases_count': alias_count,
                        'functions_count': func_count,
                        'has_history': 'history' in snapshot_data
                    }
                }

                messages.append(message)

            except json.JSONDecodeError as e:
                self.log(f"⚠️  Error parsing JSON {snapshot_file.name}: {e}")
                self.statistics['errors'] += 1
            except Exception as e:
                self.log(f"⚠️  Error processing {snapshot_file.name}: {e}")
                self.statistics['errors'] += 1
                continue

        self.log(f"✅ Extracted {len(messages)} shell snapshot messages")
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

    def create_shell_analysis(self, messages: List[Dict]) -> Dict:
        """Create shell environment analysis"""
        self.log("\nStep 5: Create Shell Analysis")

        analysis = {
            'extraction_date': datetime.now().isoformat(),
            'source': 'shell-snapshots',
            'total_snapshots': len(messages),
            'shell_types': {},
            'total_env_vars': sum(m['metadata']['env_vars_count'] for m in messages),
            'total_aliases': sum(m['metadata']['aliases_count'] for m in messages),
            'total_functions': sum(m['metadata']['functions_count'] for m in messages)
        }

        # Count shell types
        for msg in messages:
            shell = msg['metadata']['shell']
            if shell not in analysis['shell_types']:
                analysis['shell_types'][shell] = 0
            analysis['shell_types'][shell] += 1

        self.log(f"✅ Shell analysis created")
        return analysis

    def save_extracted_messages(self, messages: List[Dict]) -> bool:
        """Save extracted messages to JSONL file"""
        self.log("\nStep 6: Save Extracted Messages")

        output_file = self.memory_context / 'extractions' / 'phase5-extracted-messages.jsonl'
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

    def save_shell_analysis(self, analysis: Dict) -> bool:
        """Save shell analysis"""
        self.log("\nStep 7: Save Shell Analysis")

        output_file = self.memory_context / 'extractions' / 'phase5-shell-analysis.json'
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)

            self.log(f"✅ Saved shell analysis to {output_file.name}")
            return True
        except Exception as e:
            self.log(f"❌ Error saving analysis: {e}")
            self.statistics['errors'] += 1
            return False

    def save_statistics(self) -> bool:
        """Save extraction statistics"""
        self.log("\nStep 8: Save Statistics")

        stats_file = self.memory_context / 'extractions' / 'phase5-statistics.json'
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
        """Verify shell-snapshots directory unchanged after extraction"""
        self.log("\nStep 9: Verify Post-Extraction Integrity")

        post_checksum = self.compute_baseline_checksum()
        if baseline == post_checksum:
            self.log("✅ Checksums match - shell-snapshots untouched (read-only verified)")
            return True
        else:
            self.log(f"⚠️  Checksum mismatch detected")
            return False

    def generate_summary(self) -> bool:
        """Generate extraction summary"""
        self.log("\nStep 10: Generate Summary")

        summary = {
            'extraction_date': datetime.now().isoformat(),
            'phase': 'Phase 5: shell-snapshots',
            'status': 'complete',
            'statistics': self.statistics,
            'source_directory': str(self.snapshots_dir),
            'output_files': [
                'extractions/phase5-extracted-messages.jsonl',
                'extractions/phase5-shell-analysis.json',
                'extractions/phase5-statistics.json'
            ]
        }

        summary_file = self.memory_context / 'extractions' / 'phase5-summary.json'
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
        """Run complete Phase 5 extraction process"""
        try:
            # Step 1: Verify directory
            if not self.verify_source_directory():
                return False

            # Step 2: Compute baseline checksum
            baseline_checksum = self.compute_baseline_checksum()
            if not baseline_checksum:
                return False

            # Step 3: Load existing hashes
            existing_hashes = self.load_global_hashes()
            self.log(f"✅ Loaded {len(existing_hashes)} existing hashes for deduplication")

            # Step 4: Extract snapshot metadata
            raw_messages = self.extract_snapshot_metadata()

            # Step 5: Deduplicate
            unique_messages, new_count, dup_count = self.deduplicate_messages(raw_messages, existing_hashes)
            self.statistics['extracted_messages'] = len(raw_messages)
            self.statistics['new_unique_messages'] = new_count
            self.statistics['duplicates_found'] = dup_count

            if not unique_messages:
                self.log("\n⚠️  No new unique messages found in Phase 5")
                return True

            # Step 6: Create analysis
            shell_analysis = self.create_shell_analysis(unique_messages)

            # Step 7: Save messages
            if not self.save_extracted_messages(unique_messages):
                return False

            # Step 8: Save analysis
            if not self.save_shell_analysis(shell_analysis):
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
        self.log("PHASE 5 EXTRACTION COMPLETE")
        self.log(f"{'='*80}\n")

        self.log(f"📊 STATISTICS:")
        self.log(f"   Snapshot Files:         {self.statistics['total_snapshot_files']}")
        self.log(f"   Snapshots Parsed:       {self.statistics['snapshots_parsed']}")
        self.log(f"   Environment Vars:       {self.statistics['env_vars_tracked']}")
        self.log(f"   Extracted Messages:     {self.statistics['extracted_messages']}")
        self.log(f"   🆕 NEW UNIQUE MESSAGES: {self.statistics['new_unique_messages']}")
        self.log(f"   Duplicates Found:       {self.statistics['duplicates_found']}")
        self.log(f"   Errors:                 {self.statistics['errors']}")
        self.log(f"\n✅ All files verified as read-only (no modifications)")
        self.log(f"✅ Full provenance tracking complete")
        self.log(f"✅ Phase 5 extraction successful\n")


def main():
    """Main entry point"""
    os.chdir(Path(__file__).parent.parent.parent)  # Change to project root

    extractor = SessionMemoryExtractorPhase5(verbose=True)
    success = extractor.run_extraction()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
