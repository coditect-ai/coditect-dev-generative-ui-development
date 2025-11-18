#!/usr/bin/env python3
"""
Generate Interactive Timeline from Deduplicated Messages

Creates a complete, drillable timeline linking:
- 1,601 unique messages
- Project plans and tasklists
- Checkpoint events
- Temporal progression

Output formats:
1. Markdown with mermaid diagrams
2. Interactive HTML (optional)
3. JSON data structure (for API integration)
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import defaultdict

# Paths
project_root = Path(__file__).parent.parent
DEDUP_STATE_DIR = project_root / "MEMORY-CONTEXT" / "dedup_state"
CHECKPOINTS_DIR = project_root / "CHECKPOINTS"
UNIQUE_MESSAGES_FILE = DEDUP_STATE_DIR / "unique_messages.jsonl"
CHECKPOINT_INDEX_FILE = DEDUP_STATE_DIR / "checkpoint_index.json"

# Output
OUTPUT_DIR = project_root / "docs"
TIMELINE_MD = OUTPUT_DIR / "PROJECT-TIMELINE.md"
TIMELINE_JSON = OUTPUT_DIR / "PROJECT-TIMELINE.json"


def load_messages() -> List[Dict]:
    """Load all unique messages."""
    messages = []
    with open(UNIQUE_MESSAGES_FILE, 'r') as f:
        for line in f:
            messages.append(json.loads(line))
    return messages


def load_checkpoint_index() -> Dict:
    """Load checkpoint index."""
    with open(CHECKPOINT_INDEX_FILE, 'r') as f:
        return json.load(f)


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse various timestamp formats."""
    if not timestamp_str:
        return None

    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue

    return None


def extract_phase_info(checkpoint_name: str, source_file: str) -> Dict:
    """Extract phase/sprint information from checkpoint names."""
    info = {
        'phase': 'Unknown',
        'sprint': None,
        'day': None,
        'type': 'session',
        'focus': 'General'
    }

    # Phase patterns
    if 'Week 1' in checkpoint_name or 'Week 1' in source_file:
        info['phase'] = 'Week 1'
    elif 'Sprint +1' in checkpoint_name or 'Sprint +1' in source_file:
        info['phase'] = 'Sprint +1'
    elif 'Sprint 2' in checkpoint_name or 'Sprint 2' in source_file:
        info['phase'] = 'Sprint 2'
    elif 'Sprint 3' in checkpoint_name or 'Sprint 3' in source_file:
        info['phase'] = 'Sprint 3'

    # Day patterns
    day_match = re.search(r'Day (\d+)', checkpoint_name)
    if day_match:
        info['day'] = int(day_match.group(1))

    # Type detection
    if 'CHECKPOINT' in source_file or 'checkpoint' in checkpoint_name.lower():
        info['type'] = 'checkpoint'
    elif 'EXPORT' in source_file or 'export' in checkpoint_name.lower():
        info['type'] = 'export'

    # Focus area detection
    focus_keywords = {
        'Backend': ['backend', 'api', 'rust', 'actix'],
        'Frontend': ['frontend', 'react', 'ui'],
        'Cloud': ['cloud', 'gke', 'gcp', 'deploy'],
        'Database': ['database', 'postgres', 'sql', 'foundationdb'],
        'Architecture': ['architecture', 'adr', 'design'],
        'Documentation': ['document', 'doc', 'guide'],
        'Testing': ['test', 'qa', 'quality'],
        'Infrastructure': ['infrastructure', 'docker', 'k8s'],
        'Memory Context': ['memory-context', 'dedup', 'consolidation'],
    }

    checkpoint_lower = checkpoint_name.lower() + ' ' + source_file.lower()

    for focus, keywords in focus_keywords.items():
        if any(keyword in checkpoint_lower for keyword in keywords):
            info['focus'] = focus
            break

    return info


def group_messages_by_phase(messages: List[Dict], checkpoint_index: Dict) -> Dict:
    """Group messages by phase/sprint."""
    phases = defaultdict(lambda: {
        'checkpoints': [],
        'message_count': 0,
        'focus_areas': defaultdict(int),
        'days': defaultdict(list)
    })

    for checkpoint_name, checkpoint_data in checkpoint_index.items():
        # Get checkpoint metadata
        source_file = checkpoint_data.get('source_file', '')
        file_timestamp = checkpoint_data.get('file_timestamp', '')
        message_hashes = checkpoint_data.get('message_hashes', [])

        # Extract phase info
        phase_info = extract_phase_info(checkpoint_name, source_file)
        phase = phase_info['phase']

        # Organize checkpoint
        checkpoint_entry = {
            'name': checkpoint_name,
            'timestamp': file_timestamp,
            'source_file': source_file,
            'message_count': len(message_hashes),
            'type': phase_info['type'],
            'focus': phase_info['focus'],
            'day': phase_info['day']
        }

        phases[phase]['checkpoints'].append(checkpoint_entry)
        phases[phase]['message_count'] += len(message_hashes)
        phases[phase]['focus_areas'][phase_info['focus']] += len(message_hashes)

        if phase_info['day']:
            phases[phase]['days'][phase_info['day']].append(checkpoint_entry)

    return dict(phases)


def generate_mermaid_timeline(phases: Dict) -> str:
    """Generate Mermaid Gantt chart for timeline."""
    lines = [
        "```mermaid",
        "gantt",
        "    title CODITECT Development Timeline",
        "    dateFormat YYYY-MM-DD",
        "    section Week 1"
    ]

    # Add phases
    for phase_name in sorted(phases.keys()):
        phase = phases[phase_name]
        checkpoints = sorted(phase['checkpoints'], key=lambda x: x['timestamp'] or '')

        if checkpoints:
            first_date = checkpoints[0]['timestamp'][:10] if checkpoints[0]['timestamp'] else '2025-11-16'
            last_date = checkpoints[-1]['timestamp'][:10] if checkpoints[-1]['timestamp'] else '2025-11-17'

            lines.append(f"    {phase_name}: {first_date}, {last_date}")

    lines.append("```")
    return '\n'.join(lines)


def generate_markdown_timeline(phases: Dict, checkpoint_index: Dict, total_messages: int) -> str:
    """Generate comprehensive markdown timeline."""
    lines = [
        "# CODITECT Development Timeline",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        f"**Total Unique Messages**: {total_messages:,}",
        f"**Total Checkpoints**: {len(checkpoint_index)}",
        f"**Phases**: {len(phases)}",
        "",
        "---",
        "",
        "## Timeline Visualization",
        "",
    ]

    # Add Mermaid diagram
    lines.append(generate_mermaid_timeline(phases))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Add detailed phase breakdown
    lines.append("## Detailed Timeline")
    lines.append("")

    for phase_name in sorted(phases.keys()):
        phase = phases[phase_name]
        checkpoints = sorted(phase['checkpoints'], key=lambda x: x['timestamp'] or '')

        lines.append(f"### {phase_name}")
        lines.append("")
        lines.append(f"**Messages**: {phase['message_count']:,}")
        lines.append(f"**Checkpoints**: {len(checkpoints)}")
        lines.append("")

        # Focus areas
        lines.append("**Focus Areas**:")
        for focus, count in sorted(phase['focus_areas'].items(), key=lambda x: -x[1]):
            percentage = (count / phase['message_count'] * 100) if phase['message_count'] > 0 else 0
            lines.append(f"- {focus}: {count} messages ({percentage:.1f}%)")
        lines.append("")

        # Checkpoints by day
        if phase['days']:
            lines.append("**By Day**:")
            for day in sorted(phase['days'].keys()):
                day_checkpoints = phase['days'][day]
                lines.append(f"\n#### Day {day}")
                for ckpt in day_checkpoints:
                    lines.append(f"- **{ckpt['name']}**")
                    lines.append(f"  - Focus: {ckpt['focus']}")
                    lines.append(f"  - Messages: {ckpt['message_count']}")
                    lines.append(f"  - Source: `{ckpt['source_file']}`")
        else:
            lines.append("**Checkpoints**:")
            for ckpt in checkpoints:
                lines.append(f"\n- **{ckpt['name']}**")
                lines.append(f"  - Focus: {ckpt['focus']}")
                lines.append(f"  - Messages: {ckpt['message_count']}")
                lines.append(f"  - Timestamp: {ckpt['timestamp']}")
                lines.append(f"  - Source: `{ckpt['source_file']}`")

        lines.append("")
        lines.append("---")
        lines.append("")

    # Add integration section
    lines.extend([
        "## Integration with Project Plans",
        "",
        "### Linked Resources",
        "",
        "**Project Plans:**",
        "- [CODITECT Master Orchestration Plan](CODITECT-MASTER-ORCHESTRATION-PLAN.md)",
        "- [Cloud Platform Project Plan](CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md)",
        "- [Rollout Master Plan](CODITECT-ROLLOUT-MASTER-PLAN.md)",
        "",
        "**Tasklists:**",
        "- Check individual submodule `TASKLIST.md` files for checkbox progress",
        "- See `CHECKPOINTS/` directory for completed phase summaries",
        "",
        "**Export Files:**",
        "- All processed exports in `MEMORY-CONTEXT/dedup_state/unique_messages.jsonl`",
        "- Original exports in submodule `docs/09-sessions/` directories",
        "",
        "---",
        "",
        "## Usage",
        "",
        "**Drill Down:**",
        "1. Identify phase of interest (e.g., Week 1, Sprint +1)",
        "2. Review focus areas to understand work distribution",
        "3. Navigate to specific checkpoint files for detailed context",
        "4. Check linked project plans and tasklists for task status",
        "",
        "**API Integration:**",
        "- JSON export available: `PROJECT-TIMELINE.json`",
        "- Use for activity feed integration",
        "- Powers 360° project intelligence dashboard",
        "",
        "---",
        "",
        f"**Last Updated**: {datetime.now().isoformat()}",
    ])

    return '\n'.join(lines)


def generate_json_timeline(phases: Dict, checkpoint_index: Dict, total_messages: int) -> Dict:
    """Generate JSON timeline for API integration."""
    return {
        'generated': datetime.now().isoformat(),
        'total_messages': total_messages,
        'total_checkpoints': len(checkpoint_index),
        'phases': phases,
        'checkpoint_index': checkpoint_index,
        'metadata': {
            'dedup_state_dir': str(DEDUP_STATE_DIR),
            'unique_messages_file': str(UNIQUE_MESSAGES_FILE),
            'checkpoint_index_file': str(CHECKPOINT_INDEX_FILE)
        }
    }


def main():
    """Generate complete timeline."""
    print("=" * 80)
    print("TIMELINE GENERATOR")
    print("=" * 80)
    print()

    # Load data
    print("📂 Loading deduplicated messages...")
    messages = load_messages()
    print(f"   Loaded {len(messages):,} unique messages")

    print("📂 Loading checkpoint index...")
    checkpoint_index = load_checkpoint_index()
    print(f"   Loaded {len(checkpoint_index)} checkpoints")
    print()

    # Group by phase
    print("🔄 Grouping messages by phase...")
    phases = group_messages_by_phase(messages, checkpoint_index)
    print(f"   Identified {len(phases)} phases")
    print()

    # Generate outputs
    print("📝 Generating markdown timeline...")
    markdown = generate_markdown_timeline(phases, checkpoint_index, len(messages))
    TIMELINE_MD.write_text(markdown)
    print(f"   ✅ Written to: {TIMELINE_MD}")

    print("📝 Generating JSON timeline...")
    json_data = generate_json_timeline(phases, checkpoint_index, len(messages))
    with open(TIMELINE_JSON, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"   ✅ Written to: {TIMELINE_JSON}")
    print()

    # Summary
    print("=" * 80)
    print("TIMELINE SUMMARY")
    print("=" * 80)
    for phase_name in sorted(phases.keys()):
        phase = phases[phase_name]
        print(f"\n{phase_name}:")
        print(f"  Messages: {phase['message_count']:,}")
        print(f"  Checkpoints: {len(phase['checkpoints'])}")
        print(f"  Focus Areas: {', '.join(phase['focus_areas'].keys())}")

    print()
    print("=" * 80)
    print("✅ TIMELINE GENERATION COMPLETE")
    print("=" * 80)
    print()
    print("📖 View timeline: docs/PROJECT-TIMELINE.md")
    print("🔗 API integration: docs/PROJECT-TIMELINE.json")
    print()


if __name__ == "__main__":
    main()
