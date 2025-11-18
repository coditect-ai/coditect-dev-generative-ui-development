# CODITECT 360° Project Intelligence System

**Created:** 2025-11-17 20:19:35
**Vision:** Complete project visibility by combining 4 data streams

---

## The 360° View: Four Data Streams

```
┌─────────────────────────────────────────────────────────────┐
│               360° PROJECT INTELLIGENCE                      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   INTENT     │  │  EXECUTION   │  │    OUTCOME   │     │
│  │ (What/Why)   │  │   (How)      │  │   (Results)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                 │                  │             │
│         ▼                 ▼                  ▼             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │PROJECT-PLAN  │  │Conversations │  │  Git History │     │
│  │  TASKLIST    │  │  (messages)  │  │   (commits)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│                          ▼                                  │
│                ┌──────────────────┐                         │
│                │  CORRELATION     │                         │
│                │     ENGINE       │                         │
│                └──────────────────┘                         │
│                          │                                  │
│          ┌───────────────┼───────────────┐                 │
│          ▼               ▼               ▼                 │
│   ┌──────────┐  ┌──────────────┐  ┌──────────┐            │
│   │Timeline  │  │ Impact Graph │  │Analytics │            │
│   │ View     │  │   (files→    │  │Dashboard │            │
│   │          │  │    tasks)    │  │          │            │
│   └──────────┘  └──────────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Stream #1: Strategic Intent

### PROJECT-PLAN.md

**What it tells us:** WHAT we're building and WHY

```markdown
# Project Plan: CODITECT Cloud Backend

## Phase 1: Foundation (Weeks 1-4)
- [ ] Setup authentication system
- [ ] Database schema design
- [ ] API endpoint structure

## Phase 2: Core Features (Weeks 5-8)
- [ ] User management
- [ ] OAuth2 integration
```

**Extract:**
```python
{
  'phases': [
    {
      'name': 'Phase 1: Foundation',
      'duration': 'Weeks 1-4',
      'goals': ['Setup authentication system', ...]
    }
  ]
}
```

### TASKLIST.md

**What it tells us:** Tactical execution items

```markdown
# TASKLIST

## Week 1
- [x] Setup project structure
- [x] Configure database connection
- [ ] Implement OAuth2 middleware
- [ ] Add JWT token validation
```

**Track:**
```python
{
  'task_id': 3,
  'text': 'Implement OAuth2 middleware',
  'status': 'pending',
  'linked_to_plan': 'Phase 1: Setup authentication system'
}
```

---

## Data Stream #2: Execution Activity

### Conversation Messages

**What it tells us:** HOW work is being done, WHO is doing it

From `unique_messages.jsonl`:
```json
{
  "timestamp": "2025-11-17T15:30:00Z",
  "role": "user",
  "content": "Implementing OAuth2 middleware for token validation"
}
```

**Extract:**
- Activity type: implementing
- Component: OAuth2 middleware
- Person: User (Hal)
- Time: 3:30 PM

---

## Data Stream #3: Code Changes (Git)

### Git Commits

**What it tells us:** Actual code changes, when, by whom

```bash
git log --name-status --pretty=format:'%H|%an|%ae|%at|%s' -n 100
```

**Example output:**
```
abc123|Hal Casteel|hal@az1.ai|1700237400|Add OAuth2 middleware
M       src/middleware/oauth2.rs
A       src/middleware/auth.rs
M       Cargo.toml
```

**Extract:**
```python
{
  'commit_hash': 'abc123',
  'author': 'Hal Casteel',
  'timestamp': '2025-11-17T15:45:00Z',
  'message': 'Add OAuth2 middleware',
  'files_changed': [
    {'path': 'src/middleware/oauth2.rs', 'status': 'modified'},
    {'path': 'src/middleware/auth.rs', 'status': 'added'}
  ],
  'stats': {
    'insertions': 150,
    'deletions': 20,
    'files_changed': 3
  }
}
```

### File Change History

**Track which files changed over time:**
```bash
git log --all --pretty=format: --name-only | sort | uniq -c | sort -rg
```

**Build file activity map:**
```python
{
  'src/middleware/oauth2.rs': {
    'total_commits': 12,
    'first_changed': '2025-11-15T10:00:00Z',
    'last_changed': '2025-11-17T15:45:00Z',
    'primary_author': 'Hal Casteel',
    'linked_tasks': ['OAuth2 middleware', 'Token validation']
  }
}
```

---

## Data Stream #4: Outcomes & Results

### Checkpoint Documents

**What it tells us:** Milestones achieved, state at point in time

From `MEMORY-CONTEXT/checkpoints/*.md`:
```markdown
# Checkpoint: Phase 1 Complete

## Completed
- ✅ OAuth2 middleware implemented
- ✅ All tests passing (45/45)

## Files Changed
- src/middleware/oauth2.rs
- src/middleware/auth.rs
```

---

## The Correlation Engine

### How to Link Everything Together

```python
class CorrelationEngine:
    """
    Links data streams to create 360° project view
    """
    
    def correlate_activity(self, timestamp_window='1 hour'):
        """
        For a given time window, correlate:
        - Conversation messages
        - Git commits
        - TASKLIST changes
        - File modifications
        """
        
        # 1. Get all activities in time window
        messages = self.get_messages(timestamp_window)
        commits = self.get_commits(timestamp_window)
        
        # 2. Extract intent from messages
        intent = self.extract_intent(messages)
        # e.g., {'feature': 'OAuth2', 'activity': 'implementing'}
        
        # 3. Match commits to intent
        for commit in commits:
            # Check if commit message mentions OAuth2
            if self.fuzzy_match(commit['message'], intent['feature']):
                
                # 4. Link commit files to TASKLIST
                for file in commit['files_changed']:
                    task = self.find_task_for_file(file)
                    if task:
                        self.link(commit, task)
                        
                        # 5. Update TASKLIST checkbox if work complete
                        if self.is_complete(commit, messages):
                            self.check_task(task['id'])
        
        # 6. Link to PROJECT-PLAN goal
        plan_goal = self.match_to_plan(intent)
        
        return {
            'intent': intent,
            'commits': commits,
            'tasks_affected': tasks,
            'plan_goal': plan_goal,
            'files_changed': files
        }

    def find_task_for_file(self, file_path):
        """
        Map files to TASKLIST items
        
        Strategy:
        1. Check if file path mentions task keywords
        2. Check git commit messages that touched this file
        3. Check conversation messages that mention this file
        """
        
        # Load TASKLIST
        tasklist = self.load_tasklist()
        
        # Extract keywords from file path
        # e.g., 'src/middleware/oauth2.rs' -> ['oauth2', 'middleware']
        file_keywords = self.extract_keywords(file_path)
        
        # Find tasks with matching keywords
        for task in tasklist:
            task_keywords = self.extract_keywords(task['text'])
            
            if self.keyword_overlap(file_keywords, task_keywords) > 0.5:
                return task
        
        return None
```

---

## Timeline View: The Story Over Time

### Integrated Timeline

Combine all events into single timeline:

```
Timeline: OAuth2 Implementation (Nov 17, 2025)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

14:00  📋 PLAN  │ Added to TASKLIST: 'Implement OAuth2 middleware'
       ├─ Phase: Phase 1 - Foundation
       └─ Priority: P0

15:00  💬 START │ User: 'Starting OAuth2 implementation'
       ├─ Actor: Hal Casteel
       └─ Intent: implementing OAuth2

15:15  💻 CODE  │ Git: Modified src/middleware/oauth2.rs
       ├─ +150 lines, -20 lines
       ├─ Files: oauth2.rs, auth.rs, Cargo.toml
       └─ Linked to: Task #3 'OAuth2 middleware'

15:30  🤖 HELP  │ Agent: rust-expert-developer
       ├─ Assisted with: async token validation
       └─ Code review: suggested improvements

15:45  💻 CODE  │ Git: Commit 'Add OAuth2 middleware'
       ├─ Author: Hal Casteel
       ├─ Hash: abc123
       └─ Linked to: Task #3

16:00  ✅ TEST  │ User: 'All tests passing (45/45)'
       ├─ Success pattern detected
       └─ Auto-checked: Task #3 ✅

16:15  📸 CHECKPOINT │ Created: 'Phase 1 Auth Complete'
       ├─ Tasks completed: 3/12
       ├─ Files modified: 15
       └─ Phase progress: 25%
```

---

## Impact Graph: Files → Tasks → Plans

### Visual Relationship Map

```
PROJECT-PLAN: Phase 1 - Foundation
        │
        ├─ Goal: Setup authentication system
        │   │
        │   ├─ TASK #1: [x] Setup project structure
        │   │   └─ FILES: Cargo.toml, src/main.rs
        │   │       └─ COMMITS: 5 commits, 3 authors
        │   │
        │   ├─ TASK #2: [x] Configure database
        │   │   └─ FILES: src/db/mod.rs, migrations/
        │   │       └─ COMMITS: 8 commits, 2 authors
        │   │
        │   └─ TASK #3: [x] OAuth2 middleware
        │       └─ FILES: src/middleware/oauth2.rs
        │           ├─ COMMITS: 12 commits, 1 author
        │           ├─ CONVERSATIONS: 45 messages
        │           └─ AGENTS USED: rust-expert-developer
        │
        └─ Goal: Database schema design
            └─ TASK #4: [ ] Design user schema
                └─ STATUS: In progress
                    ├─ FILES: None yet
                    └─ CONVERSATIONS: 12 messages (planning)
```

### File Impact Analysis

**Which files contribute to which goals?**

```python
file_impact = {
    'src/middleware/oauth2.rs': {
        'tasks': ['OAuth2 middleware', 'Token validation'],
        'plan_goals': ['Setup authentication system'],
        'phases': ['Phase 1: Foundation'],
        'contributors': ['Hal Casteel'],
        'effort_hours': 4.5,
        'importance_score': 9.2  # Based on centrality in dependency graph
    }
}
```

---

## Analytics Dashboard

### Key Metrics

**Project Health:**
```python
{
    # Velocity
    'tasks_per_week': 4.2,
    'commits_per_day': 8,
    'messages_per_hour': 15,
    
    # Progress
    'phase_1_completion': 75.0,  # %
    'overall_completion': 35.0,  # %
    'on_track': True,
    'eta_completion': '2025-12-15',
    
    # Quality
    'test_coverage': 92.0,  # %
    'bugs_per_commit': 0.3,
    'code_review_score': 8.5,  # /10
    
    # Collaboration
    'ai_agent_usage': {
        'rust-expert-developer': 45,  # messages
        'database-architect': 23,
        'testing-specialist': 12
    },
    'human_hours': 32.5,
    'ai_assist_hours': 8.2
}
```

### Predictive Insights

```python
# Based on historical velocity and remaining tasks
predictions = {
    'phase_1_eta': '2025-11-22',  # 5 days from now
    'confidence': 0.85,
    
    'risks': [
        {
            'type': 'scope_creep',
            'probability': 0.3,
            'impact': 'Could delay by 1 week',
            'mitigation': 'Lock scope, defer new features to Phase 2'
        },
        {
            'type': 'technical_debt',
            'probability': 0.15,
            'impact': 'Test coverage below 80%',
            'mitigation': 'Allocate 20% time to testing'
        }
    ],
    
    'recommendations': [
        'Focus on Task #4 next (critical path)',
        'Consider using database-architect agent for schema design',
        'Schedule code review before Phase 1 checkpoint'
    ]
}
```

---

## Implementation: Data Collection

### 1. Git Data Collector

```python
class GitDataCollector:
    """Collect and index git history"""
    
    def collect_commits(self, since_date=None):
        """
        Collect all commits with file changes
        """
        cmd = [
            'git', 'log',
            '--all',
            '--pretty=format:%H|%an|%ae|%at|%s',
            '--name-status'
        ]
        
        if since_date:
            cmd.append(f'--since={since_date}')
        
        output = subprocess.check_output(cmd).decode('utf-8')
        return self.parse_git_log(output)
    
    def get_file_history(self, file_path):
        """
        Get all commits that touched a specific file
        """
        cmd = ['git', 'log', '--follow', '--pretty=format:%H|%at|%s', file_path]
        output = subprocess.check_output(cmd).decode('utf-8')
        return self.parse_file_history(output)
    
    def get_file_diff_stats(self, commit_hash, file_path):
        """
        Get insertion/deletion stats for a file in a commit
        """
        cmd = ['git', 'show', '--numstat', commit_hash, '--', file_path]
        output = subprocess.check_output(cmd).decode('utf-8')
        return self.parse_numstat(output)
```

### 2. TASKLIST Parser

```python
class TasklistParser:
    """Parse TASKLIST.md with checkbox tracking"""
    
    def parse(self, tasklist_path):
        """
        Extract tasks with checkbox state
        """
        with open(tasklist_path, 'r') as f:
            content = f.read()
        
        tasks = []
        task_pattern = r'- \[([ x])\] (.+)'
        
        for i, match in enumerate(re.finditer(task_pattern, content), 1):
            done = match.group(1) == 'x'
            text = match.group(2)
            
            tasks.append({
                'id': i,
                'text': text,
                'done': done,
                'keywords': self.extract_keywords(text)
            })
        
        return tasks
    
    def watch_for_changes(self, tasklist_path, callback):
        """
        Watch TASKLIST.md for checkbox changes
        """
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class TasklistHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if event.src_path == str(tasklist_path):
                    new_tasks = self.parse(tasklist_path)
                    callback(new_tasks)
        
        observer = Observer()
        observer.schedule(handler, str(tasklist_path.parent))
        observer.start()
```

### 3. PROJECT-PLAN Parser

```python
class ProjectPlanParser:
    """Parse PROJECT-PLAN.md structure"""
    
    def parse(self, plan_path):
        """
        Extract phases, goals, checkboxes
        """
        with open(plan_path, 'r') as f:
            content = f.read()
        
        # Parse markdown structure
        phases = []
        current_phase = None
        
        for line in content.split('\n'):
            # Phase header (## Phase 1: ...)
            if line.startswith('## '):
                current_phase = {
                    'name': line[3:],
                    'goals': []
                }
                phases.append(current_phase)
            
            # Goal item (- [ ] ...)
            elif line.strip().startswith('- ['):
                if current_phase:
                    done = 'x' in line[:10]
                    text = re.sub(r'- \[.\] ', '', line).strip()
                    current_phase['goals'].append({
                        'text': text,
                        'done': done
                    })
        
        return phases
```

---

## Implementation: Correlation Logic

### File → Task Mapping

```python
def link_files_to_tasks(git_commits, tasklist):
    """
    For each git commit, determine which TASKLIST item it addresses
    """
    
    links = []
    
    for commit in git_commits:
        # Extract keywords from commit message
        commit_keywords = extract_keywords(commit['message'])
        
        # Extract keywords from changed files
        file_keywords = []
        for file in commit['files_changed']:
            file_keywords.extend(extract_keywords(file['path']))
        
        # Find best matching task
        best_match = None
        best_score = 0
        
        for task in tasklist:
            task_keywords = task['keywords']
            
            # Calculate overlap score
            score = keyword_overlap(
                commit_keywords + file_keywords,
                task_keywords
            )
            
            if score > best_score:
                best_score = score
                best_match = task
        
        if best_score > 0.4:  # Threshold
            links.append({
                'commit': commit['hash'],
                'task': best_match['id'],
                'confidence': best_score
            })
    
    return links
```

### Task → Plan Goal Mapping

```python
def link_tasks_to_plan(tasklist, project_plan):
    """
    Link TASKLIST items to PROJECT-PLAN goals
    """
    
    links = []
    
    for task in tasklist:
        task_keywords = task['keywords']
        
        best_match = None
        best_score = 0
        
        for phase in project_plan:
            for goal in phase['goals']:
                goal_keywords = extract_keywords(goal['text'])
                
                score = keyword_overlap(task_keywords, goal_keywords)
                
                if score > best_score:
                    best_score = score
                    best_match = {'phase': phase['name'], 'goal': goal}
        
        if best_score > 0.3:
            links.append({
                'task': task['id'],
                'phase': best_match['phase'],
                'goal': best_match['goal']['text'],
                'confidence': best_score
            })
    
    return links
```

---

## Dashboard UI: 360° View

```
┌─────────────────────────────────────────────────────────────┐
│  CODITECT 360° Project Dashboard                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📊 PROJECT OVERVIEW                                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Project: CODITECT Cloud Backend                      │   │
│  │ Phase: 1 of 3 (Foundation) - 75% complete            │   │
│  │ Timeline: On track | ETA: Nov 22, 2025               │   │
│  │ Health: 🟢 Excellent (92% test coverage)             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  🎯 CURRENT FOCUS                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Plan Goal: Setup authentication system               │   │
│  │ ├─ Task #3: OAuth2 middleware ✅                     │   │
│  │ ├─ Task #4: JWT validation 🔄 (In progress)          │   │
│  │ └─ Task #5: Session management ⏸️  (Pending)         │   │
│  │                                                       │   │
│  │ Working on: JWT token validation                     │   │
│  │ Files: src/middleware/jwt.rs (+89 -12)               │   │
│  │ Last commit: 5 min ago by Hal Casteel               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  📈 TIMELINE (Last 24 hours)                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 08:00 ──●── Started OAuth2 implementation            │   │
│  │ 10:30 ──●── First commit (oauth2.rs)                 │   │
│  │ 12:00 ──●── Agent assist (rust-expert)               │   │
│  │ 14:00 ──●── Tests passing ✅                         │   │
│  │ 15:00 ──●── Task #3 complete                         │   │
│  │ 16:00 ──●── Started JWT validation                   │   │
│  │ NOW   ──●── Implementing token refresh               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  🗺️  IMPACT MAP                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Phase 1: Foundation                                  │   │
│  │  └─ Auth System (75% done)                           │   │
│  │      ├─ oauth2.rs ████████░░ 12 commits             │   │
│  │      ├─ auth.rs   ████████░░ 8 commits              │   │
│  │      └─ jwt.rs    ████░░░░░░ 3 commits (active)     │   │
│  │                                                       │   │
│  │ Most active files:                                   │   │
│  │  1. src/middleware/oauth2.rs (15 commits, 3 authors) │   │
│  │  2. src/db/mod.rs (12 commits, 2 authors)            │   │
│  │  3. Cargo.toml (8 commits, 1 author)                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  📊 METRICS                                                 │
│  ┌──────────────┬──────────────┬──────────────────────┐    │
│  │ Velocity     │ Quality      │ Collaboration        │    │
│  ├──────────────┼──────────────┼──────────────────────┤    │
│  │ 4.2 task/wk  │ 92% coverage │ 8 AI agent assists   │    │
│  │ 8 commit/day │ 0.3 bug/comm │ 32h human + 8h AI    │    │
│  │ 15 msg/hr    │ 8.5/10 review│ 3 agents used        │    │
│  └──────────────┴──────────────┴──────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Benefits of 360° View

### 1. Complete Traceability
- From strategic goal → tactical task → conversation → code → outcome
- Answer "why did we build this?" years later
- Audit trail for compliance

### 2. Predictive Intelligence
- Detect blockers before they become critical
- Predict completion dates with high accuracy
- Identify technical debt accumulation

### 3. Team Coordination
- See what everyone is working on
- Identify bottlenecks and dependencies
- Optimize resource allocation

### 4. Knowledge Preservation
- Capture decision rationale (conversation)
- Link decisions to outcomes (git commits)
- Build institutional memory

### 5. Continuous Improvement
- Measure what works (velocity, quality metrics)
- Learn from patterns (successful vs failed approaches)
- Optimize processes based on data

---

## Implementation Phases

### Phase 1: Data Collection (Week 1-2)
- [ ] Git data collector
- [ ] TASKLIST parser
- [ ] PROJECT-PLAN parser
- [ ] Message stream reader
- [ ] SQLite database for indexed queries

### Phase 2: Correlation Engine (Week 3-4)
- [ ] File → Task mapper
- [ ] Task → Plan Goal mapper
- [ ] Conversation → Activity detector
- [ ] Timeline builder

### Phase 3: Dashboard UI (Week 5-6)
- [ ] Project overview panel
- [ ] Current focus panel
- [ ] Timeline visualization
- [ ] Impact map graph
- [ ] Metrics dashboard

### Phase 4: Intelligence Layer (Week 7-8)
- [ ] Predictive analytics
- [ ] Risk detection
- [ ] Smart recommendations
- [ ] Auto-checkbox updates

### Phase 5: Real-time (Week 9-10)
- [ ] File watchers for all data sources
- [ ] WebSocket live updates
- [ ] Push notifications
- [ ] Multi-project support

---

## Success Criteria

**After full implementation:**

✅ **Complete Visibility**
- See what's being worked on right now
- Understand why (linked to plan goals)
- Track how (git commits + conversations)

✅ **Zero Manual Updates**
- TASKLIST auto-updates from git commits
- Progress calculations automatic
- Timeline self-generates

✅ **High Accuracy**
- 85%+ file→task matching accuracy
- 90%+ task→goal matching accuracy
- 95%+ completion detection accuracy

✅ **Actionable Insights**
- Predict completion within ±3 days
- Detect risks 1 week in advance
- Recommend next best action

✅ **Performance**
- Dashboard loads in <2s
- Real-time updates <5s latency
- Handles projects with 10,000+ commits
