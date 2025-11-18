#!/usr/bin/env python3
"""
Enhanced Timeline Generator with ALL Features

Generates:
1. Calendar Timeline - Organized by actual dates (September → October → November)
2. Task Linking - Extracts and links completed tasks from CHECKPOINT files
3. Weekly Breakdown - Week 1, Week 2, etc. with daily drill-down
4. Interactive HTML - Click-through timeline with search/filter

Output:
- docs/PROJECT-TIMELINE-ENHANCED.md (markdown with calendar organization)
- docs/PROJECT-TIMELINE-INTERACTIVE.html (interactive visualization)
- docs/PROJECT-TIMELINE-DATA.json (API-ready data)
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import calendar

# Paths
project_root = Path(__file__).parent.parent
DEDUP_STATE_DIR = project_root / "MEMORY-CONTEXT" / "dedup_state"
CHECKPOINTS_DIR = project_root / "CHECKPOINTS"
TEST_CHECKPOINTS_DIR = project_root / "MEMORY-CONTEXT" / "test-dataset" / "checkpoints"
UNIQUE_MESSAGES_FILE = DEDUP_STATE_DIR / "unique_messages.jsonl"
CHECKPOINT_INDEX_FILE = DEDUP_STATE_DIR / "checkpoint_index.json"

# Output
OUTPUT_DIR = project_root / "docs"
TIMELINE_MD = OUTPUT_DIR / "PROJECT-TIMELINE-ENHANCED.md"
TIMELINE_HTML = OUTPUT_DIR / "PROJECT-TIMELINE-INTERACTIVE.html"
TIMELINE_JSON = OUTPUT_DIR / "PROJECT-TIMELINE-DATA.json"


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


def extract_date_from_filename(filename: str) -> Optional[datetime]:
    """Extract date from various filename patterns."""
    # Pattern 1: YYYY-MM-DD
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        try:
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            pass

    # Pattern 2: YYYYMMDDTHHMMSS
    match = re.search(r'(\d{4})(\d{2})(\d{2})T', filename)
    if match:
        try:
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            pass

    return None


def extract_date_from_checkpoint(checkpoint_name: str, checkpoint_data: Dict) -> Optional[datetime]:
    """Extract date from checkpoint name or data."""
    # Try filename first
    source_file = checkpoint_data.get('source_file', '')
    date = extract_date_from_filename(source_file)
    if date:
        return date

    # Try checkpoint name
    date = extract_date_from_filename(checkpoint_name)
    if date:
        return date

    # Try file_timestamp
    file_timestamp = checkpoint_data.get('file_timestamp', '')
    if file_timestamp:
        try:
            return datetime.fromisoformat(file_timestamp.replace('Z', '+00:00'))
        except:
            pass

    return None


def get_week_number(date: datetime) -> Tuple[int, int]:
    """Get (year, week_number) for a date."""
    return date.isocalendar()[0], date.isocalendar()[1]


def parse_checkpoint_file_for_tasks(checkpoint_file: Path) -> List[Dict]:
    """Parse checkpoint markdown file and extract completed tasks."""
    if not checkpoint_file.exists():
        return []

    tasks = []
    try:
        content = checkpoint_file.read_text(encoding='utf-8')

        # Find completed tasks (checkboxes with [x])
        completed_pattern = r'[-*]\s+\[x\]\s+(.+?)(?:\n|$)'
        matches = re.finditer(completed_pattern, content, re.IGNORECASE | re.MULTILINE)

        for match in matches:
            task_text = match.group(1).strip()
            tasks.append({
                'text': task_text,
                'status': 'completed',
                'type': 'checkbox'
            })

        # Find tasks from "## Completed" sections
        completed_section = re.search(r'##\s+Completed\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if completed_section:
            section_text = completed_section.group(1)
            # Extract list items
            for line in section_text.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('*'):
                    task_text = re.sub(r'^[-*]\s+', '', line).strip()
                    if task_text and not any(t['text'] == task_text for t in tasks):
                        tasks.append({
                            'text': task_text,
                            'status': 'completed',
                            'type': 'section'
                        })

    except Exception as e:
        print(f"⚠️  Error parsing {checkpoint_file.name}: {e}")

    return tasks


def load_all_checkpoint_tasks() -> Dict[str, List[Dict]]:
    """Load completed tasks from all checkpoint files."""
    checkpoint_tasks = {}

    # Check both CHECKPOINTS directories
    for checkpoints_dir in [CHECKPOINTS_DIR, TEST_CHECKPOINTS_DIR]:
        if not checkpoints_dir.exists():
            continue

        for checkpoint_file in checkpoints_dir.glob("*.md"):
            checkpoint_name = checkpoint_file.stem
            tasks = parse_checkpoint_file_for_tasks(checkpoint_file)
            if tasks:
                checkpoint_tasks[checkpoint_name] = tasks

    return checkpoint_tasks


def extract_phase_info(checkpoint_name: str, source_file: str, date: Optional[datetime]) -> Dict:
    """Extract phase/sprint information from checkpoint names."""
    info = {
        'phase': 'Unknown',
        'sprint': None,
        'day': None,
        'week': None,
        'type': 'session',
        'focus': 'General',
        'month': None,
        'year': None
    }

    # Date-based info
    if date:
        info['month'] = date.strftime('%B')  # e.g., "November"
        info['year'] = date.year
        year, week = get_week_number(date)
        info['week'] = week

    # Phase patterns
    if 'Week 1' in checkpoint_name or 'Week 1' in source_file:
        info['phase'] = 'Week 1'
    elif 'Week 2' in checkpoint_name or 'Week 2' in source_file:
        info['phase'] = 'Week 2'
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
        'Backend': ['backend', 'api', 'rust', 'actix', 'fastapi'],
        'Frontend': ['frontend', 'react', 'ui', 'theia'],
        'Cloud': ['cloud', 'gke', 'gcp', 'deploy', 'infrastructure'],
        'Database': ['database', 'postgres', 'sql', 'foundationdb', 'sqlite'],
        'Architecture': ['architecture', 'adr', 'design', 'distributed'],
        'Documentation': ['document', 'doc', 'guide', 'training'],
        'Testing': ['test', 'qa', 'quality', 'pytest'],
        'Infrastructure': ['infrastructure', 'docker', 'k8s', 'kubernetes'],
        'Memory Context': ['memory-context', 'dedup', 'consolidation', 'export'],
        'Automation': ['automation', 'workflow', 'ci', 'cd'],
        'AI/ML': ['ai', 'ml', 'agent', 'llm', 'curriculum'],
    }

    checkpoint_lower = checkpoint_name.lower() + ' ' + source_file.lower()

    for focus, keywords in focus_keywords.items():
        if any(keyword in checkpoint_lower for keyword in keywords):
            info['focus'] = focus
            break

    return info


def organize_by_calendar(checkpoint_index: Dict, checkpoint_tasks: Dict) -> Dict:
    """Organize checkpoints by calendar (year → month → week → day)."""
    calendar_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    for checkpoint_name, checkpoint_data in checkpoint_index.items():
        # Extract date
        date = extract_date_from_checkpoint(checkpoint_name, checkpoint_data)

        # Get phase info
        source_file = checkpoint_data.get('source_file', '')
        phase_info = extract_phase_info(checkpoint_name, source_file, date)

        # Get tasks for this checkpoint
        tasks = checkpoint_tasks.get(checkpoint_name, [])

        # Build checkpoint entry
        checkpoint_entry = {
            'name': checkpoint_name,
            'date': date.isoformat() if date else None,
            'date_obj': date,
            'source_file': source_file,
            'message_count': len(checkpoint_data.get('message_hashes', [])),
            'type': phase_info['type'],
            'focus': phase_info['focus'],
            'phase': phase_info['phase'],
            'day': phase_info['day'],
            'tasks': tasks,
            'task_count': len(tasks)
        }

        # Organize by calendar
        if date:
            year = date.year
            month = date.strftime('%B')
            year_week, week = get_week_number(date)
            day = date.day

            calendar_data[year][month][week][day].append(checkpoint_entry)
        else:
            # Unknown dates go to a special section
            calendar_data[0]['Unknown'][0][0].append(checkpoint_entry)

    return dict(calendar_data)


def generate_mermaid_gantt(calendar_data: Dict) -> str:
    """Generate Mermaid Gantt chart with calendar organization."""
    lines = [
        "```mermaid",
        "gantt",
        "    title CODITECT Development Timeline (Calendar View)",
        "    dateFormat YYYY-MM-DD",
        "    axisFormat %b %d",
        ""
    ]

    # Process each year
    for year in sorted(calendar_data.keys(), reverse=True):
        if year == 0:
            continue  # Skip unknown dates

        year_data = calendar_data[year]

        for month in sorted(year_data.keys(), key=lambda m: datetime.strptime(m, '%B').month if m != 'Unknown' else 0):
            if month == 'Unknown':
                continue

            lines.append(f"    section {month} {year}")

            month_data = year_data[month]

            # Get all checkpoints for this month
            all_checkpoints = []
            for week in month_data.values():
                for day in week.values():
                    all_checkpoints.extend(day)

            # Group by focus area
            by_focus = defaultdict(list)
            for ckpt in all_checkpoints:
                if ckpt['date_obj']:
                    by_focus[ckpt['focus']].append(ckpt)

            # Add timeline entries
            for focus in sorted(by_focus.keys()):
                checkpoints = sorted(by_focus[focus], key=lambda x: x['date_obj'])
                if checkpoints:
                    start_date = checkpoints[0]['date_obj'].strftime('%Y-%m-%d')
                    end_date = checkpoints[-1]['date_obj'].strftime('%Y-%m-%d')
                    count = len(checkpoints)
                    lines.append(f"    {focus} ({count}): {start_date}, {end_date}")

    lines.append("```")
    return '\n'.join(lines)


def generate_markdown_timeline(calendar_data: Dict, checkpoint_index: Dict, total_messages: int, total_tasks: int) -> str:
    """Generate enhanced markdown timeline with calendar organization and tasks."""
    lines = [
        "# CODITECT Development Timeline (Enhanced)",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        f"**Total Unique Messages**: {total_messages:,}",
        f"**Total Checkpoints**: {len(checkpoint_index)}",
        f"**Completed Tasks Tracked**: {total_tasks:,}",
        "",
        "---",
        "",
        "## 📊 Overview",
        "",
        "This timeline organizes all development activity by:",
        "- **Calendar dates** (Year → Month → Week → Day)",
        "- **Focus areas** (Backend, Frontend, Cloud, etc.)",
        "- **Completed tasks** extracted from checkpoint files",
        "- **Message counts** from deduplicated conversation history",
        "",
        "---",
        "",
        "## 📅 Timeline Visualization",
        "",
    ]

    # Add Mermaid Gantt
    lines.append(generate_mermaid_gantt(calendar_data))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Calendar breakdown
    lines.append("## 📆 Calendar Timeline")
    lines.append("")

    for year in sorted(calendar_data.keys(), reverse=True):
        if year == 0:
            year_label = "Unknown Dates"
        else:
            year_label = str(year)

        year_data = calendar_data[year]

        lines.append(f"### {year_label}")
        lines.append("")

        for month in sorted(year_data.keys(), key=lambda m: datetime.strptime(m, '%B').month if m != 'Unknown' else 0):
            month_data = year_data[month]

            # Calculate month totals
            month_messages = 0
            month_checkpoints = 0
            month_tasks = 0

            for week in month_data.values():
                for day in week.values():
                    for ckpt in day:
                        month_messages += ckpt['message_count']
                        month_checkpoints += 1
                        month_tasks += ckpt['task_count']

            lines.append(f"#### {month} {year if year != 0 else ''}")
            lines.append("")
            lines.append(f"**Summary**: {month_checkpoints} checkpoints, {month_messages:,} messages, {month_tasks} tasks completed")
            lines.append("")

            # Weekly breakdown
            for week in sorted(month_data.keys()):
                week_data = month_data[week]

                if not week_data or (len(week_data) == 1 and 0 in week_data):
                    continue  # Skip empty weeks

                lines.append(f"##### Week {week}")
                lines.append("")

                # Daily breakdown
                for day in sorted(week_data.keys()):
                    day_checkpoints = week_data[day]

                    if not day_checkpoints:
                        continue

                    # Format day header
                    if day_checkpoints[0]['date_obj']:
                        day_label = day_checkpoints[0]['date_obj'].strftime('%A, %B %d, %Y')
                    else:
                        day_label = f"Day {day}" if day != 0 else "Date Unknown"

                    lines.append(f"###### {day_label}")
                    lines.append("")

                    # List checkpoints for this day
                    for ckpt in sorted(day_checkpoints, key=lambda x: x['date_obj'] if x['date_obj'] else datetime.min):
                        lines.append(f"**{ckpt['name']}**")
                        lines.append(f"- **Focus**: {ckpt['focus']}")
                        lines.append(f"- **Phase**: {ckpt['phase']}")
                        lines.append(f"- **Messages**: {ckpt['message_count']:,}")
                        lines.append(f"- **Source**: `{ckpt['source_file']}`")

                        if ckpt['tasks']:
                            lines.append(f"- **Tasks Completed**: {len(ckpt['tasks'])}")
                            lines.append("  <details>")
                            lines.append("  <summary>View tasks</summary>")
                            lines.append("")
                            for task in ckpt['tasks'][:20]:  # Limit to first 20
                                lines.append(f"  - [x] {task['text']}")
                            if len(ckpt['tasks']) > 20:
                                lines.append(f"  - ... and {len(ckpt['tasks']) - 20} more tasks")
                            lines.append("  </details>")

                        lines.append("")

        lines.append("---")
        lines.append("")

    # Add statistics section
    lines.extend([
        "## 📈 Statistics",
        "",
        "### By Focus Area",
        ""
    ])

    # Calculate focus area stats
    focus_stats = defaultdict(lambda: {'checkpoints': 0, 'messages': 0, 'tasks': 0})
    for year_data in calendar_data.values():
        for month_data in year_data.values():
            for week_data in month_data.values():
                for day_data in week_data.values():
                    for ckpt in day_data:
                        focus_stats[ckpt['focus']]['checkpoints'] += 1
                        focus_stats[ckpt['focus']]['messages'] += ckpt['message_count']
                        focus_stats[ckpt['focus']]['tasks'] += ckpt['task_count']

    lines.append("| Focus Area | Checkpoints | Messages | Tasks |")
    lines.append("|------------|-------------|----------|-------|")
    for focus in sorted(focus_stats.keys(), key=lambda f: focus_stats[f]['messages'], reverse=True):
        stats = focus_stats[focus]
        lines.append(f"| {focus} | {stats['checkpoints']} | {stats['messages']:,} | {stats['tasks']} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Add integration section
    lines.extend([
        "## 🔗 Integration",
        "",
        "### Linked Resources",
        "",
        "**Project Plans:**",
        "- [Master Orchestration Plan](CODITECT-MASTER-ORCHESTRATION-PLAN.md)",
        "- [Cloud Platform Project Plan](CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md)",
        "- [Rollout Master Plan](CODITECT-ROLLOUT-MASTER-PLAN.md)",
        "",
        "**Tasklists:**",
        "- Individual submodule `TASKLIST.md` files",
        "- `CHECKPOINTS/` directory for phase summaries",
        "",
        "**Raw Data:**",
        "- [Interactive HTML Timeline](PROJECT-TIMELINE-INTERACTIVE.html)",
        "- [JSON Data Export](PROJECT-TIMELINE-DATA.json)",
        "- [Deduplication Database](../MEMORY-CONTEXT/dedup_state/)",
        "",
        "---",
        "",
        f"**Last Updated**: {datetime.now().isoformat()}",
    ])

    return '\n'.join(lines)


def generate_interactive_html(calendar_data: Dict, checkpoint_index: Dict, total_messages: int, total_tasks: int) -> str:
    """Generate interactive HTML timeline with search and filter."""

    # Convert calendar data to JSON for JavaScript
    calendar_json = json.dumps(calendar_data, default=str, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CODITECT Development Timeline - Interactive</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
        }}

        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}

        .controls {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}

        .search-box {{
            flex: 1;
            min-width: 300px;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            font-size: 1em;
            border: 2px solid #dee2e6;
            border-radius: 10px;
            transition: all 0.3s;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .filter-group {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            padding: 8px 16px;
            background: white;
            border: 2px solid #dee2e6;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9em;
        }}

        .filter-btn:hover {{
            background: #f8f9fa;
        }}

        .filter-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}

        .timeline {{
            padding: 40px;
        }}

        .year-section {{
            margin-bottom: 60px;
        }}

        .year-header {{
            font-size: 2em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .month-section {{
            margin-bottom: 40px;
            margin-left: 20px;
        }}

        .month-header {{
            font-size: 1.5em;
            color: #764ba2;
            margin-bottom: 15px;
        }}

        .week-section {{
            margin-left: 20px;
            margin-bottom: 30px;
        }}

        .week-header {{
            font-size: 1.2em;
            color: #666;
            margin-bottom: 10px;
        }}

        .day-section {{
            margin-left: 20px;
            margin-bottom: 20px;
        }}

        .day-header {{
            font-size: 1.1em;
            color: #888;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .checkpoint-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            margin-left: 20px;
            transition: all 0.3s;
            cursor: pointer;
        }}

        .checkpoint-card:hover {{
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transform: translateY(-2px);
            border-color: #667eea;
        }}

        .checkpoint-card.hidden {{
            display: none;
        }}

        .checkpoint-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }}

        .checkpoint-name {{
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
            flex: 1;
        }}

        .checkpoint-badges {{
            display: flex;
            gap: 8px;
        }}

        .badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
        }}

        .badge-focus {{
            background: #e7f5ff;
            color: #1864ab;
        }}

        .badge-messages {{
            background: #f3f0ff;
            color: #5f3dc4;
        }}

        .badge-tasks {{
            background: #d3f9d8;
            color: #2b8a3e;
        }}

        .checkpoint-meta {{
            display: flex;
            gap: 20px;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}

        .checkpoint-source {{
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            color: #999;
            padding: 8px 12px;
            background: #f8f9fa;
            border-radius: 6px;
            margin-bottom: 10px;
        }}

        .tasks-section {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e9ecef;
        }}

        .tasks-header {{
            font-weight: 600;
            margin-bottom: 10px;
            color: #495057;
        }}

        .task-list {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }}

        .task-list.expanded {{
            max-height: 500px;
            overflow-y: auto;
        }}

        .task-item {{
            padding: 6px 0;
            color: #666;
            font-size: 0.9em;
        }}

        .task-item::before {{
            content: "✓ ";
            color: #2b8a3e;
            font-weight: bold;
            margin-right: 5px;
        }}

        .toggle-tasks {{
            background: none;
            border: none;
            color: #667eea;
            cursor: pointer;
            font-size: 0.9em;
            padding: 5px 0;
            text-decoration: underline;
        }}

        .no-results {{
            text-align: center;
            padding: 60px;
            color: #999;
            font-size: 1.2em;
        }}

        .empty {{
            display: none;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}

            .stats {{
                flex-direction: column;
                gap: 20px;
            }}

            .controls {{
                flex-direction: column;
            }}

            .timeline {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 CODITECT Development Timeline</h1>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{total_messages:,}</div>
                    <div class="stat-label">Unique Messages</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{len(checkpoint_index)}</div>
                    <div class="stat-label">Checkpoints</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{total_tasks:,}</div>
                    <div class="stat-label">Tasks Completed</div>
                </div>
            </div>
        </div>

        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search checkpoints, tasks, or focus areas...">
            </div>
            <div class="filter-group" id="filterButtons">
                <!-- Dynamically populated -->
            </div>
        </div>

        <div class="timeline" id="timeline">
            <!-- Dynamically populated -->
        </div>

        <div class="no-results empty" id="noResults">
            No results found. Try adjusting your search or filters.
        </div>
    </div>

    <script>
        const calendarData = {calendar_json};

        // Extract unique focus areas
        const focusAreas = new Set();
        Object.values(calendarData).forEach(yearData => {{
            Object.values(yearData).forEach(monthData => {{
                Object.values(monthData).forEach(weekData => {{
                    Object.values(weekData).forEach(dayData => {{
                        dayData.forEach(ckpt => focusAreas.add(ckpt.focus));
                    }});
                }});
            }});
        }});

        // Create filter buttons
        const filterContainer = document.getElementById('filterButtons');
        const allFocusAreas = ['All', ...Array.from(focusAreas).sort()];
        let activeFilter = 'All';

        allFocusAreas.forEach(focus => {{
            const btn = document.createElement('button');
            btn.className = 'filter-btn' + (focus === 'All' ? ' active' : '');
            btn.textContent = focus;
            btn.onclick = () => {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeFilter = focus;
                filterCheckpoints();
            }};
            filterContainer.appendChild(btn);
        }});

        // Render timeline
        function renderTimeline() {{
            const timeline = document.getElementById('timeline');
            timeline.innerHTML = '';

            Object.entries(calendarData).sort((a, b) => b[0] - a[0]).forEach(([year, yearData]) => {{
                const yearSection = document.createElement('div');
                yearSection.className = 'year-section';

                const yearHeader = document.createElement('div');
                yearHeader.className = 'year-header';
                yearHeader.textContent = year == 0 ? 'Unknown Dates' : year;
                yearSection.appendChild(yearHeader);

                Object.entries(yearData).forEach(([month, monthData]) => {{
                    const monthSection = document.createElement('div');
                    monthSection.className = 'month-section';

                    const monthHeader = document.createElement('div');
                    monthHeader.className = 'month-header';
                    monthHeader.textContent = month;
                    monthSection.appendChild(monthHeader);

                    Object.entries(monthData).sort((a, b) => a[0] - b[0]).forEach(([week, weekData]) => {{
                        const weekSection = document.createElement('div');
                        weekSection.className = 'week-section';

                        const weekHeader = document.createElement('div');
                        weekHeader.className = 'week-header';
                        weekHeader.textContent = `Week ${{week}}`;
                        weekSection.appendChild(weekHeader);

                        Object.entries(weekData).sort((a, b) => a[0] - b[0]).forEach(([day, dayCheckpoints]) => {{
                            const daySection = document.createElement('div');
                            daySection.className = 'day-section';

                            if (dayCheckpoints.length > 0 && dayCheckpoints[0].date_obj) {{
                                const dayHeader = document.createElement('div');
                                dayHeader.className = 'day-header';
                                const date = new Date(dayCheckpoints[0].date_obj);
                                dayHeader.textContent = date.toLocaleDateString('en-US', {{
                                    weekday: 'long',
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                }});
                                daySection.appendChild(dayHeader);
                            }}

                            dayCheckpoints.forEach(ckpt => {{
                                const card = createCheckpointCard(ckpt);
                                daySection.appendChild(card);
                            }});

                            weekSection.appendChild(daySection);
                        }});

                        monthSection.appendChild(weekSection);
                    }});

                    yearSection.appendChild(monthSection);
                }});

                timeline.appendChild(yearSection);
            }});
        }}

        function createCheckpointCard(ckpt) {{
            const card = document.createElement('div');
            card.className = 'checkpoint-card';
            card.dataset.focus = ckpt.focus;
            card.dataset.name = ckpt.name.toLowerCase();
            card.dataset.phase = ckpt.phase.toLowerCase();
            card.dataset.source = ckpt.source_file.toLowerCase();

            const header = document.createElement('div');
            header.className = 'checkpoint-header';

            const name = document.createElement('div');
            name.className = 'checkpoint-name';
            name.textContent = ckpt.name;
            header.appendChild(name);

            const badges = document.createElement('div');
            badges.className = 'checkpoint-badges';

            const focusBadge = document.createElement('span');
            focusBadge.className = 'badge badge-focus';
            focusBadge.textContent = ckpt.focus;
            badges.appendChild(focusBadge);

            const messagesBadge = document.createElement('span');
            messagesBadge.className = 'badge badge-messages';
            messagesBadge.textContent = `${{ckpt.message_count.toLocaleString()}} msgs`;
            badges.appendChild(messagesBadge);

            if (ckpt.task_count > 0) {{
                const tasksBadge = document.createElement('span');
                tasksBadge.className = 'badge badge-tasks';
                tasksBadge.textContent = `${{ckpt.task_count}} tasks`;
                badges.appendChild(tasksBadge);
            }}

            header.appendChild(badges);
            card.appendChild(header);

            const meta = document.createElement('div');
            meta.className = 'checkpoint-meta';
            meta.innerHTML = `
                <span><strong>Phase:</strong> ${{ckpt.phase}}</span>
                <span><strong>Type:</strong> ${{ckpt.type}}</span>
            `;
            card.appendChild(meta);

            const source = document.createElement('div');
            source.className = 'checkpoint-source';
            source.textContent = ckpt.source_file;
            card.appendChild(source);

            if (ckpt.tasks && ckpt.tasks.length > 0) {{
                const tasksSection = document.createElement('div');
                tasksSection.className = 'tasks-section';

                const tasksHeader = document.createElement('div');
                tasksHeader.className = 'tasks-header';
                tasksHeader.textContent = `✓ ${{ckpt.tasks.length}} Tasks Completed`;
                tasksSection.appendChild(tasksHeader);

                const toggleBtn = document.createElement('button');
                toggleBtn.className = 'toggle-tasks';
                toggleBtn.textContent = 'Show tasks';
                toggleBtn.onclick = (e) => {{
                    e.stopPropagation();
                    taskList.classList.toggle('expanded');
                    toggleBtn.textContent = taskList.classList.contains('expanded') ? 'Hide tasks' : 'Show tasks';
                }};
                tasksSection.appendChild(toggleBtn);

                const taskList = document.createElement('div');
                taskList.className = 'task-list';
                ckpt.tasks.slice(0, 20).forEach(task => {{
                    const taskItem = document.createElement('div');
                    taskItem.className = 'task-item';
                    taskItem.textContent = task.text;
                    taskList.appendChild(taskItem);
                }});
                if (ckpt.tasks.length > 20) {{
                    const more = document.createElement('div');
                    more.className = 'task-item';
                    more.textContent = `... and ${{ckpt.tasks.length - 20}} more tasks`;
                    taskList.appendChild(more);
                }}
                tasksSection.appendChild(taskList);

                card.appendChild(tasksSection);

                // Store tasks text for search
                card.dataset.tasks = ckpt.tasks.map(t => t.text).join(' ').toLowerCase();
            }} else {{
                card.dataset.tasks = '';
            }}

            return card;
        }}

        function filterCheckpoints() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.checkpoint-card');
            let visibleCount = 0;

            cards.forEach(card => {{
                const matchesFilter = activeFilter === 'All' || card.dataset.focus === activeFilter;
                const matchesSearch = searchTerm === '' ||
                    card.dataset.name.includes(searchTerm) ||
                    card.dataset.focus.toLowerCase().includes(searchTerm) ||
                    card.dataset.phase.includes(searchTerm) ||
                    card.dataset.source.includes(searchTerm) ||
                    card.dataset.tasks.includes(searchTerm);

                if (matchesFilter && matchesSearch) {{
                    card.classList.remove('hidden');
                    visibleCount++;
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            // Show/hide no results message
            document.getElementById('noResults').classList.toggle('empty', visibleCount > 0);
        }}

        // Search input handler
        document.getElementById('searchInput').addEventListener('input', filterCheckpoints);

        // Initial render
        renderTimeline();
    </script>
</body>
</html>
"""
    return html


def main():
    """Generate all enhanced timeline outputs."""
    print("=" * 80)
    print("ENHANCED TIMELINE GENERATOR")
    print("=" * 80)
    print()

    # Load data
    print("📂 Loading deduplicated messages...")
    messages = load_messages()
    print(f"   ✅ Loaded {len(messages):,} unique messages")

    print("📂 Loading checkpoint index...")
    checkpoint_index = load_checkpoint_index()
    print(f"   ✅ Loaded {len(checkpoint_index)} checkpoints")

    print("📂 Loading completed tasks from checkpoint files...")
    checkpoint_tasks = load_all_checkpoint_tasks()
    total_tasks = sum(len(tasks) for tasks in checkpoint_tasks.values())
    print(f"   ✅ Extracted {total_tasks:,} completed tasks from {len(checkpoint_tasks)} checkpoints")
    print()

    # Organize by calendar
    print("🗓️  Organizing by calendar...")
    calendar_data = organize_by_calendar(checkpoint_index, checkpoint_tasks)
    print(f"   ✅ Organized into calendar structure")
    print()

    # Generate outputs
    print("📝 Generating enhanced markdown timeline...")
    markdown = generate_markdown_timeline(calendar_data, checkpoint_index, len(messages), total_tasks)
    TIMELINE_MD.write_text(markdown)
    print(f"   ✅ Written to: {TIMELINE_MD}")

    print("📝 Generating interactive HTML timeline...")
    html = generate_interactive_html(calendar_data, checkpoint_index, len(messages), total_tasks)
    TIMELINE_HTML.write_text(html)
    print(f"   ✅ Written to: {TIMELINE_HTML}")

    print("📝 Generating JSON data export...")
    json_data = {
        'generated': datetime.now().isoformat(),
        'total_messages': len(messages),
        'total_checkpoints': len(checkpoint_index),
        'total_tasks': total_tasks,
        'calendar': calendar_data,
        'checkpoint_index': checkpoint_index
    }
    with open(TIMELINE_JSON, 'w') as f:
        json.dump(json_data, f, default=str, indent=2)
    print(f"   ✅ Written to: {TIMELINE_JSON}")
    print()

    # Summary
    print("=" * 80)
    print("ENHANCEMENT SUMMARY")
    print("=" * 80)
    print()
    print("✅ Calendar Timeline - Organized by Year → Month → Week → Day")
    print("✅ Task Linking - Extracted completed tasks from checkpoint files")
    print("✅ Weekly Breakdown - Full calendar with weekly/daily drill-down")
    print("✅ Interactive HTML - Searchable, filterable timeline visualization")
    print()
    print("📊 Statistics:")
    print(f"   • Years covered: {len([y for y in calendar_data.keys() if y != 0])}")
    print(f"   • Months covered: {sum(len(year_data) for year_data in calendar_data.values())}")
    print(f"   • Total messages: {len(messages):,}")
    print(f"   • Total checkpoints: {len(checkpoint_index)}")
    print(f"   • Tasks completed: {total_tasks:,}")
    print()
    print("=" * 80)
    print("✅ ALL ENHANCEMENTS COMPLETE")
    print("=" * 80)
    print()
    print("📖 View enhanced timeline: docs/PROJECT-TIMELINE-ENHANCED.md")
    print("🌐 Open interactive timeline: docs/PROJECT-TIMELINE-INTERACTIVE.html")
    print("🔗 API data: docs/PROJECT-TIMELINE-DATA.json")
    print()


if __name__ == "__main__":
    main()
