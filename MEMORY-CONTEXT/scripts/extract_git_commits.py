#!/usr/bin/env python3
"""
Extract git commit data from checkpoint markdown files
Creates git-commits.json dataset for dashboard
"""

import json
import re
from pathlib import Path
from datetime import datetime

def parse_checkpoint_markdown(filepath):
    """Parse checkpoint markdown to extract git data"""
    try:
        content = filepath.read_text()
        
        data = {
            'checkpoint_id': filepath.stem,
            'commits': [],
            'branch': '',
            'working_dir_status': '',
            'submodules': []
        }
        
        # Extract timestamp from content
        timestamp_match = re.search(r'\*\*Timestamp:\*\* (\d{4}-\d{2}-\d{2}T[\d:-]+Z)', content)
        if timestamp_match:
            data['timestamp'] = timestamp_match.group(1)
        
        # Extract branch
        branch_match = re.search(r'### Current Branch\s*```\s*([^\s]+)\s*```', content)
        if branch_match:
            data['branch'] = branch_match.group(1)
        
        # Extract recent commits
        commits_match = re.search(r'### Recent Commits\s*```\s*([\s\S]*?)```', content)
        if commits_match:
            commit_lines = commits_match.group(1).strip().split('\n')
            for line in commit_lines:
                commit_match = re.match(r'^([a-f0-9]+)\s+(.+)$', line)
                if commit_match:
                    data['commits'].append({
                        'hash': commit_match.group(1),
                        'message': commit_match.group(2)
                    })
        
        # Extract working directory status
        status_match = re.search(r'### Working Directory Status\s*```\s*([\s\S]*?)```', content)
        if status_match:
            data['working_dir_status'] = status_match.group(1).strip()
        
        # Extract submodules
        submodule_match = re.search(r'### Updated Submodules.*?\n\n([\s\S]*?)(?=\n---|\n##|$)', content)
        if submodule_match:
            submodule_text = submodule_match.group(1)
            # Split by double newline + **
            blocks = re.split(r'\n\n\*\*', submodule_text)
            
            for block in blocks:
                name_match = re.match(r'([^\*\n]+)', block)
                commit_match = re.search(r'- Commit: `([^`]+)`', block)
                latest_match = re.search(r'- Latest: ([a-f0-9]+)\s+(.+)', block)
                
                if name_match:
                    submodule_data = {
                        'name': name_match.group(1).replace('**', '').strip(),
                        'commit': commit_match.group(1) if commit_match else '',
                        'latest_hash': latest_match.group(1) if latest_match else '',
                        'latest_message': latest_match.group(2) if latest_match else ''
                    }
                    if submodule_data['name']:  # Only add if has name
                        data['submodules'].append(submodule_data)
        
        return data if (data['commits'] or data['submodules']) else None
        
    except Exception as e:
        print(f"Error parsing {filepath.name}: {e}")
        return None

def main():
    checkpoints_dir = Path('/Users/halcasteel/PROJECTS/coditect-rollout-master/MEMORY-CONTEXT/checkpoints')
    output_file = Path('/Users/halcasteel/PROJECTS/coditect-rollout-master/MEMORY-CONTEXT/dashboard/data/git-commits.json')
    
    print(f"📂 Scanning checkpoints in: {checkpoints_dir}")
    
    all_commits_data = []
    checkpoint_files = list(checkpoints_dir.glob('*.md'))
    
    print(f"📄 Found {len(checkpoint_files)} checkpoint files")
    
    for checkpoint_file in checkpoint_files:
        data = parse_checkpoint_markdown(checkpoint_file)
        if data:
            # Add file system modification time
            file_stat = checkpoint_file.stat()
            data['file_modified_time'] = datetime.fromtimestamp(file_stat.st_mtime).isoformat() + 'Z'
            data['file_created_time'] = datetime.fromtimestamp(file_stat.st_ctime).isoformat() + 'Z'

            all_commits_data.append(data)
            print(f"✓ Extracted data from {checkpoint_file.name}: {len(data['commits'])} commits, {len(data['submodules'])} submodules")
    
    # Sort by timestamp (newest first)
    all_commits_data.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    output_data = {
        'version': '1.0',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'total_sessions': len(all_commits_data),
        'total_commits': sum(len(d['commits']) for d in all_commits_data),
        'sessions': all_commits_data
    }
    
    output_file.write_text(json.dumps(output_data, indent=2))
    
    print(f"\n✅ Created {output_file}")
    print(f"   Sessions with git data: {len(all_commits_data)}")
    print(f"   Total commits tracked: {output_data['total_commits']}")
    
if __name__ == '__main__':
    main()
