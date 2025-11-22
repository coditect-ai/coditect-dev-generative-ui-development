# Agentic Project Orchestration Framework

**Version:** 2.0
**Status:** Production-Ready
**License:** Proprietary - Closed Source
**Copyright:** © 2025 AZ1.AI INC. All rights reserved.
**Developer:** Hal Casteel, CEO/CTO
**Email:** 1@az1.ai
**LLM Support:** Claude, GPT-4, Gemini, Llama, Universal

---

## Overview

The **Agentic Project Orchestration Framework** is a universal project management system for AI-driven development. It orchestrates complex multi-week projects by breaking them into zero-ambiguity tasks and dispatching them to specialized AI agents (Claude, GPT, Gemini, etc.) for autonomous execution.

### Key Features

✅ **LLM-Agnostic** - Works with Claude, GPT, Gemini, Llama, any AI agent
✅ **Enterprise-Grade State Persistence** - Atomic writes, crash recovery, backups
✅ **Dependency Management** - Automatic task ordering and unblocking
✅ **Parallel Execution** - 3-4x speedup with concurrent task execution
✅ **Complete Audit Trail** - Every state change archived permanently
✅ **Rollback Support** - Restore to any point in time
✅ **Zero-Ambiguity Tasks** - Tasks have exact inputs, requirements, outputs
✅ **Progress Tracking** - Real-time metrics and reporting

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT LAYER                             │
│  (Your project defines tasks specific to your domain)       │
│                                                              │
│  from claude.orchestration import ProjectOrchestrator       │
│  orchestrator = ProjectOrchestrator(project_root)           │
│  orchestrator.add_task(...)                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATION FRAMEWORK LAYER                   │
│               (.claude/orchestration/)                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Orchestrator │  │     Task     │  │    State     │     │
│  │   (Core)     │  │    Model     │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Backup     │  │    Agent     │  │   Executor   │     │
│  │   Manager    │  │   Registry   │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                  AI AGENT LAYER                              │
│  (Claude, GPT-4, Gemini, Llama, Custom Agents)             │
│                                                              │
│  Execute tasks via:                                          │
│  - Claude Code (Task tool)                                   │
│  - OpenAI API                                                │
│  - Gemini API                                                │
│  - Custom LLM endpoints                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. `orchestrator.py` - Core Engine

The central orchestrator that manages project execution.

**Key Methods:**
- `add_task()` - Define a new task
- `execute_task()` - Execute a specific task
- `complete_task()` - Mark task as complete
- `get_next_task()` - Get next recommended task
- `generate_report()` - Project status report

**Features:**
- Dependency resolution
- Task priority management
- Parallel execution planning
- Automatic task unblocking

### 2. `task.py` - Task Model

Zero-ambiguity task specification.

**Task Fields:**
- `task_id` - Unique identifier
- `title` - Human-readable title
- `description` - Complete specification
- `agent` - AI agent name (LLM-agnostic)
- `priority` - CRITICAL, HIGH, MEDIUM, LOW
- `phase` - planning, design, development, testing, deployment
- `dependencies` - List of prerequisite task IDs
- `estimated_hours` - Time estimate
- `deliverables` - Output files
- `success_criteria` - Measurable outcomes
- `commands` - Agent execution commands

### 3. `state_manager.py` - State Persistence

Enterprise-grade state management with atomic writes.

**Features:**
- **Atomic Writes** - POSIX temp + rename pattern
- **Crash Recovery** - Survives power failures
- **Checksums** - SHA256 integrity verification
- **Format Versioning** - Support migrations
- **Rich Metadata** - Metrics, timestamps, change history

**Performance:**
- Read: 2ms (warm cache)
- Write: 138ms (with fsync + backup)
- Checksum: 3ms

### 4. `backup_manager.py` - Backup & Rollback

Permanent backup archive with rollback support.

**Features:**
- **Permanent Archive** - Never auto-delete backups
- **Timestamped Backups** - Every state change archived
- **Easy Rollback** - Restore to any point in time
- **Organized Storage** - Dedicated backups directory
- **Manual Compression** - User-controlled archival

**Commands:**
```bash
# List backups
python -m claude.orchestration.cli --list-backups

# Rollback to specific backup
python -m claude.orchestration.cli --rollback 20251112-013045
```

### 5. `agent_registry.py` - LLM Support

Universal AI agent registry supporting multiple LLMs.

**Supported LLMs:**
- **Anthropic Claude** - Claude Code, API
- **OpenAI GPT** - GPT-4, GPT-3.5
- **Google Gemini** - Gemini Pro, Ultra
- **Meta Llama** - Llama 2, 3
- **Custom Agents** - Any LLM with API

**Agent Configuration:**
```python
# Register Claude agent
registry.register_agent(
    name="claude-code",
    type="anthropic-claude",
    interface="task-tool",
    capabilities=["code", "research", "design"]
)

# Register GPT-4 agent
registry.register_agent(
    name="gpt-4",
    type="openai-gpt",
    interface="api",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### 6. `executor.py` - Task Execution

Universal task executor for any LLM.

**Execution Modes:**
- **Interactive** - Copy/paste command to Claude Code
- **API** - Direct API calls (GPT, Gemini)
- **Hybrid** - Combine multiple LLMs

**Example:**
```python
# Execute with Claude
executor.execute(task_id="ADR-001", agent="claude-code")

# Execute with GPT-4
executor.execute(task_id="ADR-002", agent="gpt-4")

# Parallel execution (multiple LLMs)
executor.execute_parallel([
    ("ADR-003", "claude-code"),
    ("ADR-004", "gpt-4"),
    ("ADR-005", "gemini-pro")
])
```

---

## Installation

### Option 1: As a Git Submodule (Recommended)

```bash
# Add .claude as submodule to your project
git submodule add https://github.com/your-org/claude-framework.git .claude

# Initialize orchestration
python .claude/orchestration/init.py
```

### Option 2: Direct Clone

```bash
# Clone into your project
git clone https://github.com/your-org/claude-framework.git .claude

# Add to .gitignore if desired
echo ".claude/" >> .gitignore
```

### Option 3: Python Package

```bash
# Install as Python package (future)
pip install claude-orchestration
```

---

## Quick Start

### 1. Create Project Orchestrator

```python
# project_orchestrator.py
from pathlib import Path
from claude.orchestration import (
    ProjectOrchestrator,
    AgentTask,
    TaskPriority,
    ProjectPhase
)

# Initialize orchestrator
project_root = Path(__file__).parent
orchestrator = ProjectOrchestrator(project_root)

# Define tasks
orchestrator.add_task(AgentTask(
    task_id="TASK-001",
    title="Create System Design Document",
    description="""
    Create comprehensive system design document.

    INPUTS:
    - requirements/REQUIREMENTS.md
    - architecture/ARCHITECTURE.md

    REQUIREMENTS:
    1. Document system architecture
    2. Create component diagrams
    3. Specify API contracts

    SUCCESS CRITERIA:
    - 50+ pages comprehensive spec
    - Diagrams for all components
    - API fully documented
    """,
    agent="claude-code",  # or "gpt-4", "gemini-pro"
    priority=TaskPriority.CRITICAL,
    phase=ProjectPhase.DESIGN,
    dependencies=[],
    estimated_hours=8,
    deliverables=["docs/SYSTEM-DESIGN.md"],
    success_criteria=[
        "Complete architecture documentation",
        "All components diagrammed",
        "API contracts specified"
    ]
))

# Get next task
next_task = orchestrator.get_next_task()
print(f"Next: {next_task.task_id}")

# Execute
orchestrator.execute_task(next_task.task_id)

# Mark complete
orchestrator.complete_task(next_task.task_id)

# Generate report
orchestrator.generate_report()
```

### 2. Run Orchestrator

```bash
# List all tasks
python project_orchestrator.py --list

# Get next task
python project_orchestrator.py --next

# Execute specific task
python project_orchestrator.py --execute TASK-001

# Mark complete
python project_orchestrator.py --complete TASK-001

# Generate report
python project_orchestrator.py --report

# List backups
python project_orchestrator.py --list-backups

# Rollback
python project_orchestrator.py --rollback 20251112-013045
```

---

## LLM Integration Examples

### Claude Code (Interactive)

```python
task = orchestrator.get_next_task()
print(f"📝 Copy this command to Claude Code:")
print(f"   Use {task.agent} subagent to {task.title}")
```

### GPT-4 (API)

```python
import openai

def execute_with_gpt4(task: AgentTask):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a specialized agent."},
            {"role": "user", "content": task.description}
        ]
    )
    return response.choices[0].message.content
```

### Gemini (API)

```python
import google.generativeai as genai

def execute_with_gemini(task: AgentTask):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(task.description)
    return response.text
```

### Custom LLM (API)

```python
import requests

def execute_with_custom_llm(task: AgentTask):
    response = requests.post(
        "https://your-llm-api.com/generate",
        json={
            "prompt": task.description,
            "max_tokens": 4000
        }
    )
    return response.json()["text"]
```

---

## State File Format

### `project_state.json`

```json
{
  "version": "1.0",
  "format_version": 2,
  "project_id": "your-project-name",
  "last_updated": "2025-11-12T01:30:45.123456",
  "checksum": "a3f5c2b8e1d9f7a4",
  "tasks": {
    "TASK-001": {
      "task_id": "TASK-001",
      "status": "completed",
      "started_at": "2025-11-11T14:09:55",
      "completed_at": "2025-11-11T15:12:30",
      "agent": "claude-code",
      "actual_hours": 1.5
    }
  },
  "metrics": {
    "total_tasks": 10,
    "completed_tasks": 3,
    "completion_percentage": 30.0
  }
}
```

---

## Best Practices

### 1. Task Granularity

**Good:**
```python
# Small, focused task (2-8 hours)
task = AgentTask(
    task_id="API-001",
    title="Design Authentication API",
    estimated_hours=4
)
```

**Bad:**
```python
# Too large (40+ hours)
task = AgentTask(
    task_id="BUILD-EVERYTHING",
    title="Build entire backend",
    estimated_hours=200  # ❌ Too big!
)
```

### 2. Zero-Ambiguity Specifications

**Good:**
```python
description="""
Create REST API for user authentication.

INPUTS:
- docs/API-SPEC.md (template)
- docs/AUTH-REQUIREMENTS.md

REQUIREMENTS:
1. POST /auth/register endpoint
2. POST /auth/login endpoint
3. JWT token generation
4. Password hashing (bcrypt)

OUTPUT: src/api/auth.ts

SUCCESS CRITERIA:
- All endpoints implemented
- Unit tests passing
- JWT validation working
"""
```

**Bad:**
```python
description="Build auth stuff"  # ❌ Ambiguous!
```

### 3. Dependency Management

```python
# Define dependencies explicitly
tasks = [
    AgentTask(task_id="DESIGN-001", dependencies=[]),
    AgentTask(task_id="IMPLEMENT-001", dependencies=["DESIGN-001"]),
    AgentTask(task_id="TEST-001", dependencies=["IMPLEMENT-001"])
]
```

---

## Advanced Features

### Parallel Execution

```python
from claude.orchestration import ParallelExecutor

executor = ParallelExecutor(orchestrator)

# Execute 3 tasks in parallel
results = executor.execute_parallel([
    "TASK-001",  # Claude Code
    "TASK-002",  # GPT-4
    "TASK-003",  # Gemini Pro
])

# 3x speedup!
```

### Custom Agents

```python
from claude.orchestration import AgentRegistry, CustomAgent

# Register custom agent
class MyCustomAgent(CustomAgent):
    def execute(self, task: AgentTask) -> str:
        # Your custom execution logic
        return result

registry = AgentRegistry()
registry.register(MyCustomAgent(name="my-agent"))
```

### Webhooks & Notifications

```python
from claude.orchestration import WebhookManager

# Register webhook
webhooks = WebhookManager()
webhooks.register(
    event="task_completed",
    url="https://your-server.com/webhook",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
```

---

## Configuration

### `orchestration.config.json`

```json
{
  "state_file": "scripts/project_state.json",
  "backups_dir": "scripts/backups",
  "backup_retention": "permanent",
  "fsync_enabled": true,
  "checksum_enabled": true,
  "parallel_max": 4,
  "default_agent": "claude-code",
  "llm_providers": {
    "anthropic": {
      "api_key": "${ANTHROPIC_API_KEY}",
      "models": ["claude-sonnet-4", "claude-opus-4"]
    },
    "openai": {
      "api_key": "${OPENAI_API_KEY}",
      "models": ["gpt-4", "gpt-3.5-turbo"]
    },
    "google": {
      "api_key": "${GOOGLE_API_KEY}",
      "models": ["gemini-pro", "gemini-ultra"]
    }
  }
}
```

---

## Documentation

### Framework Documentation

- `ARCHITECTURE.md` - System architecture
- `API-REFERENCE.md` - Component API docs
- `BEST-PRACTICES.md` - Patterns and guidelines
- `STATE-PERSISTENCE.md` - State management details
- `LLM-INTEGRATION.md` - Multi-LLM support guide

### Example Projects

- `examples/simple-project/` - Basic usage
- `examples/multi-llm/` - Using multiple LLMs
- `examples/parallel-execution/` - Concurrent tasks
- `examples/custom-agent/` - Custom agent integration

---

## Testing

```bash
# Run unit tests
python -m pytest .claude/orchestration/tests/

# Test state persistence
python .claude/orchestration/tests/test_state_manager.py

# Test crash recovery
python .claude/orchestration/tests/test_crash_recovery.py

# Test LLM integrations
python .claude/orchestration/tests/test_llm_agents.py
```

---

## Contributing

We welcome contributions! This framework is designed to be:

✅ **LLM-agnostic** - Support any AI agent
✅ **Extensible** - Easy to add new features
✅ **Well-documented** - Comprehensive docs
✅ **Well-tested** - High test coverage

See `CONTRIBUTING.md` for guidelines.

---

## License

**Proprietary - Closed Source**

Copyright © 2025 AZ1.AI INC. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, or use of this software, via any medium, is strictly prohibited.

**Developer:** Hal Casteel, CEO/CTO
**Email:** 1@az1.ai
**Company:** AZ1.AI INC.

---

## Support

- **Documentation:** `.claude/orchestration/docs/`
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** support@az1.ai

---

## Roadmap

### v2.1 (Q1 2026)
- [ ] Cloud state sync (S3, GCS)
- [ ] Web dashboard UI
- [ ] Real-time collaboration

### v2.2 (Q2 2026)
- [ ] GraphQL API
- [ ] Mobile app
- [ ] Advanced analytics

### v3.0 (Q3 2026)
- [ ] Multi-project orchestration
- [ ] AI agent marketplace
- [ ] Enterprise features

---

**Version:** 2.0
**Status:** ✅ Production-Ready
**Last Updated:** 2025-11-12

**Copyright © 2025 AZ1.AI INC. All rights reserved.**
