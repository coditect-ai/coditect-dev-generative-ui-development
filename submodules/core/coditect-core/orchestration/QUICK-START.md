# Quick Start Guide - Orchestration Framework

**Get started in 5 minutes!**

Copyright © 2025 AZ1.AI INC. | Developer: Hal Casteel, CEO/CTO | Email: 1@az1.ai

---

## Step 1: Import the Framework

```python
from claude.orchestration import (
    ProjectOrchestrator,
    AgentTask,
    TaskPriority,
    ProjectPhase
)
```

## Step 2: Create an Orchestrator

```python
# Initialize orchestrator for your project
orchestrator = ProjectOrchestrator(project_root=".")
```

## Step 3: Define Your First Task

```python
task = AgentTask(
    task_id="TASK-001",
    title="Create Project README",
    description="""
    Create a comprehensive README.md file for the project.

    REQUIREMENTS:
    1. Project overview
    2. Installation instructions
    3. Usage examples
    4. License information

    OUTPUT: README.md

    SUCCESS CRITERIA:
    - Complete project documentation
    - Clear installation steps
    - Working code examples
    """,
    agent="claude-code",
    priority=TaskPriority.HIGH,
    phase=ProjectPhase.DOCUMENTATION,
    estimated_hours=2,
    deliverables=["README.md"]
)
```

## Step 4: Add Task to Orchestrator

```python
orchestrator.add_task(task)
```

## Step 5: Execute the Task

```python
# Get next task to work on
next_task = orchestrator.get_next_task()
print(f"Next task: {next_task.title}")

# Execute the task
result = orchestrator.execute_task(next_task.task_id)

# After agent completes the work, mark as complete
orchestrator.complete_task(next_task.task_id)
```

## Step 6: Check Progress

```python
# Generate status report
orchestrator.print_report()
```

---

## Using the CLI

Prefer command-line? Use the CLI interface:

```bash
# Show next task
python -m claude.orchestration.cli --next

# Execute task
python -m claude.orchestration.cli --execute TASK-001

# Mark complete
python -m claude.orchestration.cli --complete TASK-001

# View report
python -m claude.orchestration.cli --report
```

---

## Complete Example: Multi-Task Project

```python
from claude.orchestration import (
    ProjectOrchestrator,
    AgentTask,
    TaskPriority,
    ProjectPhase
)

# Initialize
orchestrator = ProjectOrchestrator(project_root=".")

# Define tasks
tasks = [
    AgentTask(
        task_id="DESIGN-001",
        title="Create System Architecture",
        description="Design system architecture...",
        agent="claude-code",
        priority=TaskPriority.CRITICAL,
        phase=ProjectPhase.DESIGN,
        estimated_hours=4,
        dependencies=[]
    ),
    AgentTask(
        task_id="DEV-001",
        title="Implement Core Module",
        description="Implement core functionality...",
        agent="claude-code",
        priority=TaskPriority.HIGH,
        phase=ProjectPhase.DEVELOPMENT,
        estimated_hours=6,
        dependencies=["DESIGN-001"]  # Wait for design
    ),
    AgentTask(
        task_id="TEST-001",
        title="Write Unit Tests",
        description="Create comprehensive tests...",
        agent="claude-code",
        priority=TaskPriority.MEDIUM,
        phase=ProjectPhase.TESTING,
        estimated_hours=3,
        dependencies=["DEV-001"]  # Wait for implementation
    )
]

# Add all tasks
for task in tasks:
    orchestrator.add_task(task)

# Execute workflow
while next_task := orchestrator.get_next_task():
    print(f"\n<¯ Working on: {next_task.title}")

    # Execute
    result = orchestrator.execute_task(next_task.task_id)

    # Wait for agent to complete...
    input("Press Enter when agent completes...")

    # Mark complete
    orchestrator.complete_task(next_task.task_id)

    # Show progress
    orchestrator.print_report()

print("\n All tasks completed!")
```

---

## Using Different LLMs

```python
# Use Claude
orchestrator.execute_task("TASK-001", agent="claude-code")

# Use GPT-4 (when execute_gpt.py is implemented)
orchestrator.execute_task("TASK-002", agent="gpt-4")

# Use Gemini (when execute_gemini.py is implemented)
orchestrator.execute_task("TASK-003", agent="gemini-pro")
```

---

## Backup & Rollback

```bash
# List all backups
python -m claude.orchestration.cli --list-backups

# Rollback to previous state
python -m claude.orchestration.cli --rollback 20251112-013045
```

---

## Next Steps

1. **Read the full documentation:** `.claude/orchestration/README.md`
2. **Check examples:** See complete usage examples
3. **Explore the API:** All modules have comprehensive docstrings
4. **Customize:** Extend with your own agents and workflows

---

## Need Help?

- **Documentation:** `.claude/orchestration/README.md`
- **Completion Summary:** `.claude/orchestration/COMPLETION-SUMMARY.md`
- **Contact:** 1@az1.ai

---

**Framework Version:** 2.0.0
**Status:** Production Ready
**License:** Proprietary - AZ1.AI INC.
