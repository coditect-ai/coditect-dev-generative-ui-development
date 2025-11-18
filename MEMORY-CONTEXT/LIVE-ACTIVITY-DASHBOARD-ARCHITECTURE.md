# CODITECT Live Activity Dashboard - Architecture Design

**Created:** 2025-11-17 20:15:04
**Status:** Conceptual Architecture

---

## Executive Summary

Transform the static deduplication database into a **real-time development
intelligence dashboard** that answers:

- **WHO** is doing the work? (Human user? Which AI agent?)
- **WHAT** are they working on? (Feature, component, bug fix)
- **WHY** are they doing it? (Which PROJECT-PLAN goal, TASKLIST item)
- **HOW** is it progressing? (Real-time updates, completion %)
- **WHEN** did activity occur? (Live feed, historical timeline)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   LIVE ACTIVITY DASHBOARD                    │
│  (Web UI - Real-time updates via WebSocket)                 │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ WebSocket / SSE
                            │
┌─────────────────────────────────────────────────────────────┐
│              ACTIVITY STREAM PROCESSOR                       │
│  • Parse new messages                                        │
│  • Extract entities (user, agent, project, task)           │
│  • Link to PROJECT-PLAN & TASKLIST                          │
│  • Calculate metrics & progress                             │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ File System Events
                            │
┌─────────────────────────────────────────────────────────────┐
│              FILE SYSTEM WATCHER                             │
│  • Watch: unique_messages.jsonl (new messages)              │
│  • Watch: TASKLIST.md (checkbox updates)                    │
│  • Watch: .git/refs/heads/* (commits)                       │
│  • Watch: MEMORY-CONTEXT/checkpoints/ (milestones)          │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ Append Events
                            │
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
│  • unique_messages.jsonl (conversation stream)              │
│  • PROJECT-PLAN.md (strategic goals)                        │
│  • TASKLIST.md (tactical execution)                         │
│  • .git/log (commits, authors)                              │
│  • checkpoint_index.json (message→checkpoint mapping)       │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Identity Detection (WHO)

**User Identification:**
```python
# From git commits
git_author = subprocess.check_output(['git', 'log', '-1', '--format=%an <%ae>'])

# From message patterns
if message.role == 'user':
    identity = {
        'type': 'human',
        'name': git_author,
        'session': current_session_id
    }
```

**Agent Identification:**
```python
# Detect which AI agent from content patterns
agent_patterns = {
    'rust-expert-developer': r'Rust.*async.*tokio',
    'database-architect': r'PostgreSQL|MySQL|schema.*design',
    'frontend-react-typescript': r'React.*TypeScript.*component',
    'orchestrator': r'coordinating.*agents|multi-agent',
}

for agent, pattern in agent_patterns.items():
    if re.search(pattern, message.content):
        identity = {'type': 'ai_agent', 'agent': agent}
```

### 2. Work Context Detection (WHAT)

**Extract Work Topics:**
```python
# Multi-level context extraction
context = {
    'project': None,      # coditect-cloud-backend
    'feature': None,      # user authentication
    'component': None,    # OAuth2 middleware
    'activity': None,     # implementing, testing, debugging
    'files': []           # affected files
}

# From message content
if 'implementing' in message.lower():
    context['activity'] = 'implementation'
elif 'testing' in message.lower():
    context['activity'] = 'testing'
elif 'debugging' in message.lower():
    context['activity'] = 'debugging'

# From file references in tool calls
if 'Read(' in message or 'Write(' in message:
    files = extract_file_paths(message)
    context['files'] = files
    context['component'] = infer_component_from_paths(files)
```

### 3. Intent Linking (WHY)

**Link to PROJECT-PLAN.md:**
```python
# Parse PROJECT-PLAN.md structure
project_plan = parse_project_plan('PROJECT-PLAN.md')
# {
#   'Phase 1: Foundation': [
#     'Setup authentication system',
#     'Database schema design'
#   ],
#   'Phase 2: Core Features': [...]
# }

# Match current work to plan sections
def find_plan_goal(work_context):
    for phase, goals in project_plan.items():
        for goal in goals:
            if fuzzy_match(work_context, goal):
                return {'phase': phase, 'goal': goal}
    return None
```

**Link to TASKLIST.md:**
```python
# Parse TASKLIST with checkbox states
tasklist = parse_tasklist('TASKLIST.md')
# [
#   {'id': 1, 'text': 'Setup OAuth2 middleware', 'done': False},
#   {'id': 2, 'text': 'Add user session management', 'done': True}
# ]

# Auto-detect which task is being worked on
def infer_current_task(message_content, tasklist):
    for task in tasklist:
        if not task['done']:  # Only check pending tasks
            if fuzzy_match(message_content, task['text']):
                return task
    return None

# Auto-update checkboxes when work is detected as complete
def auto_check_completion(message_content):
    if re.search(r'✅|completed|finished|done|success', message_content):
        task = infer_current_task(previous_messages, tasklist)
        if task:
            update_checkbox(task['id'], done=True)
```

### 4. Progress Tracking (HOW)

**Real-time Metrics:**
```python
class ProgressTracker:
    def calculate_metrics(self):
        return {
            # TASKLIST progress
            'tasks_total': len(tasklist),
            'tasks_completed': sum(1 for t in tasklist if t['done']),
            'tasks_in_progress': self.detect_active_tasks(),
            'completion_percentage': (completed / total) * 100,
            
            # Activity metrics
            'messages_today': count_messages_since(today),
            'active_sessions': len(active_sessions),
            'current_velocity': messages_per_hour,
            
            # Productivity indicators
            'files_modified': len(git_diff_files),
            'commits_today': count_commits_since(today),
            'tests_passing': parse_test_results(),
        }
```

### 5. Live Feed (WHEN)

**File System Watcher:**
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MessageStreamHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('unique_messages.jsonl'):
            # Read new messages (tail -n since last read)
            new_messages = read_new_messages(last_position)
            
            for msg in new_messages:
                # Extract entities
                activity = parse_activity(msg)
                
                # Broadcast to dashboard
                websocket.broadcast({
                    'type': 'new_activity',
                    'timestamp': msg['first_seen'],
                    'actor': activity['who'],
                    'action': activity['what'],
                    'context': activity['why'],
                    'progress': calculate_progress()
                })

# Start watching
observer = Observer()
observer.schedule(handler, 'MEMORY-CONTEXT/dedup_state', recursive=False)
observer.start()
```

---

## Dashboard UI Components

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  CODITECT Live Activity Dashboard                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────────────────┐    │
│  │ Current Activity │  │   Project Progress           │    │
│  │                  │  │                              │    │
│  │ 👤 User: Hal     │  │  Phase 1: Foundation         │    │
│  │ 🤖 Agent: None   │  │  ████████░░░░░░░ 60%         │    │
│  │                  │  │                              │    │
│  │ Working on:      │  │  Phase 2: Core Features      │    │
│  │ OAuth2 Middleware│  │  ███░░░░░░░░░░░░ 20%         │    │
│  │                  │  │                              │    │
│  │ Task: [3/12]     │  │  Overall: 45% complete       │    │
│  │ ✅ Setup auth    │  │  Est. completion: 3 days     │    │
│  │ 🔄 Add sessions  │  └──────────────────────────────┘    │
│  │ ⏸️  JWT tokens   │                                      │
│  └──────────────────┘  ┌──────────────────────────────┐    │
│                         │   Activity Stream            │    │
│  ┌────────────────────────────────────────────────┐   │    │
│  │ Live Message Feed (Last 10)                    │   │    │
│  │────────────────────────────────────────────────│   │    │
│  │ 19:45 👤 Hal: Testing OAuth2 flow              │   │    │
│  │ 19:44 🤖 Assistant: Implementing token refresh  │   │    │
│  │ 19:42 👤 Hal: Fixed session expiry bug         │   │    │
│  │ 19:40 🤖 rust-expert: Added async handlers     │   │    │
│  │ 19:38 ✅ Checkpoint: Auth system v1 complete   │   │    │
│  └────────────────────────────────────────────────┘   │    │
│                                                        │    │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │    │
│  │ Messages/hr  │  │ Commits/day  │  │ Tests      │  │    │
│  │    42        │  │     8        │  │  ✅ 45/45  │  │    │
│  └──────────────┘  └──────────────┘  └────────────┘  │    │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Example

### Scenario: User implements OAuth2 middleware

**1. New message arrives:**
```json
{
  "hash": "abc123...",
  "message": {
    "role": "user",
    "content": "I'll implement the OAuth2 middleware for token validation"
  },
  "first_seen": "2025-11-17T20:30:00Z",
  "checkpoint": "phase-1-auth-system"
}
```

**2. Activity processor extracts:**
```python
{
  'who': {
    'type': 'human',
    'name': 'Hal Casteel',
    'email': 'hal@az1.ai'
  },
  'what': {
    'activity': 'implementing',
    'feature': 'OAuth2 middleware',
    'component': 'authentication',
    'files': ['src/middleware/oauth2.rs']
  },
  'why': {
    'project_plan': {
      'phase': 'Phase 1: Foundation',
      'goal': 'Setup authentication system'
    },
    'tasklist': {
      'id': 3,
      'text': '[ ] Implement OAuth2 middleware',
      'status': 'in_progress'
    }
  },
  'when': '2025-11-17T20:30:00Z'
}
```

**3. Dashboard updates:**
- Current Activity: "Hal is implementing OAuth2 middleware"
- TASKLIST: Mark task #3 as "in progress" (yellow indicator)
- Progress: Calculate % complete for Phase 1
- Stream: Add message to live feed
- Velocity: Update messages/hour metric

**4. When complete (detected from success patterns):**
```python
# Detect completion from message like:
# "✅ OAuth2 middleware complete - all tests passing"

# Auto-update TASKLIST
update_checkbox(task_id=3, done=True)

# Broadcast completion event
websocket.broadcast({
  'type': 'task_complete',
  'task': 'OAuth2 middleware',
  'celebration': '🎉'
})
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Goal:** Basic live feed working

- [ ] File system watcher for unique_messages.jsonl
- [ ] WebSocket server for real-time updates
- [ ] Basic message parser (who, what, when)
- [ ] Simple web UI with live message stream

**Deliverable:** See new messages appear in dashboard as they're added

### Phase 2: Context Intelligence (Week 3-4)

**Goal:** Understand WHAT work is being done

- [ ] Work context extraction (feature, component, activity)
- [ ] File reference parsing from tool calls
- [ ] Agent detection from content patterns
- [ ] Current activity panel in UI

**Deliverable:** Dashboard shows "Working on: OAuth2 middleware"

### Phase 3: Plan Integration (Week 5-6)

**Goal:** Link work to strategic goals

- [ ] PROJECT-PLAN.md parser
- [ ] TASKLIST.md parser with checkbox state
- [ ] Fuzzy matching algorithm (work → plan goals)
- [ ] Progress calculation and visualization

**Deliverable:** Dashboard shows which plan goal is being addressed

### Phase 4: Auto-Completion (Week 7-8)

**Goal:** Auto-update TASKLISTs from conversation

- [ ] Success pattern detection (✅, completed, done)
- [ ] Auto-checkbox updates in TASKLIST.md
- [ ] Git commit integration
- [ ] Celebration animations for completions

**Deliverable:** Checkboxes auto-update when work completes

### Phase 5: Analytics & Insights (Week 9-10)

**Goal:** Productivity metrics and trends

- [ ] Velocity tracking (messages/hour, tasks/day)
- [ ] Progress predictions (ETA for completion)
- [ ] Agent effectiveness metrics
- [ ] Historical analytics dashboard

**Deliverable:** Full analytics dashboard with insights

---

## Technology Stack

### Backend
- **Python 3.11+** - Core processing
- **FastAPI** - WebSocket server
- **watchdog** - File system monitoring
- **spaCy/transformers** - NLP for context extraction
- **Redis** - Real-time event queue

### Frontend
- **React + TypeScript** - UI framework
- **TanStack Query** - Real-time data sync
- **Recharts** - Progress visualizations
- **Tailwind CSS** - Styling
- **WebSocket** - Live updates

### Data Storage
- **unique_messages.jsonl** - Message stream (existing)
- **SQLite** - Indexed queries for dashboard
- **Redis** - Session state and caching

---

## Key Features

### 1. Multi-User Support
- Track different users working on same project
- Show who's active right now
- User-specific progress tracking

### 2. Agent Intelligence
- Detect which AI agents are being used
- Track agent effectiveness (success rate)
- Suggest best agent for current task

### 3. Smart Suggestions
```python
# Based on current work context, suggest:
if working_on('authentication') and tasklist_has('add JWT tokens'):
    suggest_task('JWT tokens - next logical step')
    suggest_agent('rust-expert-developer - best for async Rust')
```

### 4. Productivity Insights
- Peak productivity hours
- Average task completion time
- Context switching frequency
- Collaboration patterns

---

## Security & Privacy

- **Local-first:** Dashboard runs locally, no cloud required
- **Read-only access:** Never modifies git history or code
- **Opt-in sharing:** Can expose dashboard to team if desired
- **Sensitive data filtering:** Redact API keys, credentials

---

## Success Metrics

**After implementation:**
- ✅ 100% visibility into current work
- ✅ Auto-updating TASKLIST checkboxes (90%+ accuracy)
- ✅ Real-time progress tracking (<5s latency)
- ✅ Work-to-plan linkage (80%+ match rate)
- ✅ Zero manual status updates required

---

## Next Steps

1. **Review this architecture** - Validate approach
2. **Build POC** - Phase 1 implementation (2 weeks)
3. **User testing** - Get feedback from Hal
4. **Iterate** - Refine based on real usage
5. **Scale** - Add team features, analytics
