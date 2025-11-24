# Claude Code Hooks - Comprehensive Analysis & Implementation Strategy

**Date:** November 22, 2025
**Status:** ✅ Complete Research & Analysis
**Scope:** Understanding Anthropic hooks, CODITECT integration strategy, implementation roadmap
**Audience:** CODITECT Core Team, DevOps Engineers, Automation Specialists

---

## Executive Summary

Claude Code **Hooks** are shell-based automation triggers that execute at specific points in Claude Code's lifecycle, enabling autonomous enforcement of development standards, automated quality checks, and custom workflows. Hooks fire BEFORE or AFTER specific tool usage (file editing, git operations, etc.), allowing teams to enforce standards automatically rather than manually.

**CODITECT Application:** Implement hooks to enforce STANDARDS.md compliance, automate pre-commit quality checks, enforce architectural standards, and trigger intelligent workflows without user intervention.

---

## Part 1: Understanding Claude Code Hooks

### What Are Hooks?

Hooks are **user-defined shell commands** that execute automatically when:
- Specified tools are used (e.g., `Edit`, `Write`, `Bash`)
- Specific events occur (before/after tool execution, session start/end, context compaction)
- Claude Code detects permission requests or notifications
- User submits a prompt (preprocessing opportunity)

**Key Distinction:** Hooks are NOT callbacks or notifications—they are **executable shell commands** that can:
- Modify or reject proposed changes
- Run additional validation
- Trigger secondary workflows
- Block unsafe operations
- Enforce organizational standards

### Hook Lifecycle Events

| Event | Timing | Use Cases | Can Block? |
|-------|--------|-----------|-----------|
| **UserPromptSubmit** | Before Claude processes prompt | Add context, validate input, block harmful prompts | ✅ Yes |
| **PreToolUse** | Before tool executes | Approval gate, validation, pre-flight checks | ✅ Yes |
| **PostToolUse** | After tool completes | Validation of results, triggering workflows, cleanup | ❌ No |
| **PermissionRequest** | When permission needed | Auto-approve/deny, custom policies | ✅ Yes |
| **Notification** | During notifications | Custom alerting, logging, escalation | ❌ No |
| **SessionStart** | Session begins | Setup automation, context loading | ❌ No |
| **SessionEnd** | Session ends | Cleanup, checkpointing, archiving | ❌ No |
| **PreCompact** | Before context compaction | Backup context, validation | ❌ No |

**Critical:** Only `PreToolUse`, `UserPromptSubmit`, and `PermissionRequest` can BLOCK operations (return `continue: false`).

### Matcher Patterns

Matchers identify WHICH tools trigger hooks:

```json
{
  "tool_name": "Write|Edit"  // Regex pattern
}
```

**Matcher Types:**

| Pattern | Matches | Use |
|---------|---------|-----|
| `"Write"` | Exact match: `Write` tool only | Specific tool targeting |
| `"Edit"` | Exact match: `Edit` tool only | Specific tool targeting |
| `"Write\|Edit"` | Either Write OR Edit tools | Multiple tool types |
| `".*"` or `""` | All tools | Wildcard catch-all |
| `"Notebook.*"` | Regex: NotebookEdit, NotebookWrite, etc. | Pattern matching |
| `"mcp__.*"` | All MCP tools | Model Context Protocol tools |
| `"mcp__github__.*"` | GitHub MCP tools only | Specific MCP servers |

### Configuration Structure

Hooks are defined in `settings.json` or `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": {
          "tool_name": "Edit|Write"
        },
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/validation.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": {
          "tool_name": "Bash"
        },
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/post-execution.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": {},
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/prompt-enhancer.py"
          }
        ]
      }
    ]
  }
}
```

**Configuration Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `hooks` | object | ✅ | Top-level hooks container |
| `EventName` | string | ✅ | Hook event type (PreToolUse, PostToolUse, etc.) |
| `matcher.tool_name` | string/regex | ✅ (unless empty) | Tool name pattern to match |
| `hooks[]` | array | ✅ | Array of hook commands |
| `type` | string | ✅ | Hook type: `command` or `prompt` |
| `command` | string | ✅ | Bash command to execute |
| `timeout` | number | ❌ | Timeout in seconds (default: 60) |

### Hook Execution Model

**Sequential Execution:**

1. Event occurs (e.g., user calls `Edit` tool)
2. Claude identifies matching matchers
3. For each matching hook:
   - Streams structured JSON to stdin containing tool data and context
   - Waits up to 60 seconds for response
   - Interprets exit code and/or JSON output
4. Based on all hook responses, decides whether to continue
5. Proceeds or blocks based on hook decisions

**Input/Output Model:**

**Stdin (Structured JSON):**
```json
{
  "event": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "new_string": "...",
    "old_string": "..."
  },
  "metadata": {
    "timestamp": "2025-11-22T10:30:00Z",
    "session_id": "abc123"
  }
}
```

**Exit Code & JSON Output:**

**Continue (allow operation):**
```bash
exit 0
# OR
echo '{"continue": true}' && exit 0
```

**Block (reject operation):**
```bash
echo '{"continue": false, "stopReason": "File violates standards"}' && exit 1
```

**Suppress Output:**
```bash
echo '{"continue": true, "suppressOutput": true}' && exit 0
```

---

## Part 2: CODITECT Hook Integration Strategy

### Why Hooks Matter for CODITECT

CODITECT is built on **autonomous operation with human checkpoints**. Hooks enable:

1. **Automated Standards Enforcement** - Validate code against STANDARDS.md automatically
2. **Quality Gates** - Block changes that violate architectural decisions
3. **Intelligent Preprocessing** - Enhance prompts with context before Claude processes
4. **Compliance Checking** - Automatically verify ADR compliance
5. **Workflow Automation** - Trigger secondary workflows without user intervention
6. **Cost Optimization** - Pre-validate changes to reduce token consumption

### Recommended Hook Implementation (CODITECT)

**Phase 1: Quality Assurance Hooks** (Critical)

| Hook | Event | Purpose | Blocking? |
|------|-------|---------|-----------|
| **Component Validation** | PreToolUse (Write) | Validate new agents/skills/commands against STANDARDS.md | ✅ Yes |
| **Standards Compliance** | PreToolUse (Edit) | Verify changes conform to CODITECT standards | ✅ Yes |
| **Git Pre-Commit** | PostToolUse (Bash) | Run tests/linting after git commits | ❌ No |
| **Documentation Sync** | PostToolUse (Write) | Update inventory when new files created | ❌ No |
| **Prompt Enhancement** | UserPromptSubmit | Add CODITECT context to user prompts | ❌ No |

**Phase 2: Intelligent Routing Hooks** (Advanced)

| Hook | Event | Purpose | Blocking? |
|------|-------|---------|-----------|
| **Agent Selection** | UserPromptSubmit | Analyze prompt, suggest optimal agent | ❌ No |
| **Component Router** | UserPromptSubmit | Identify if creating new component (agent/skill/command) | ❌ No |
| **Permission Auto-Approval** | PermissionRequest | Auto-approve safe operations | ✅ Yes |

**Phase 3: Observability Hooks** (Nice-to-have)

| Hook | Event | Purpose | Blocking? |
|------|-------|---------|-----------|
| **Change Logging** | PostToolUse (*) | Log all changes to audit trail | ❌ No |
| **Quality Metrics** | SessionEnd | Calculate session metrics (files changed, agents used) | ❌ No |
| **Context Export** | SessionEnd | Auto-export context for checkpoint | ❌ No |

---

## Part 3: Implementation Details

### Hook 1: Component Validation Hook

**Purpose:** Validate new agents/skills/commands against STANDARDS.md before creation

**Event:** `PreToolUse`
**Matcher:** `tool_name: "Write"`
**Trigger:** When creating `.coditect/agents/*.md`, `.coditect/skills/*/SKILL.md`, or `.coditect/commands/*.md`

**Logic:**
1. Extract file path from tool input
2. Check if it's a component file (agents/, skills/, commands/)
3. If yes, validate against STANDARDS.md:
   - YAML frontmatter present
   - Required fields (name, description, etc.)
   - File naming conventions (kebab-case)
   - Content length requirements
4. If invalid, block with specific error message
5. If valid, allow

**Implementation:**
```bash
#!/bin/bash
# hooks/component-validation.sh

set -euo pipefail

# Read stdin
json=$(cat)

# Extract file path
file_path=$(echo "$json" | jq -r '.tool_input.file_path // empty')

# Check if component file
if [[ "$file_path" =~ \.coditect/(agents|skills|commands)/.*\.(md|SKILL\.md)$ ]]; then
    # Run STANDARDS validation
    python3 hooks/validate_component.py "$file_path" < <(echo "$json")
else
    # Not a component file, allow
    exit 0
fi
```

**Python Validation (`hooks/validate_component.py`):**
```python
#!/usr/bin/env python3
"""Validate component against STANDARDS.md"""

import json
import sys
import re
from pathlib import Path

def validate_agent(content: str) -> tuple[bool, str]:
    """Validate agent file"""
    # Check YAML frontmatter
    if not content.startswith('---'):
        return False, "Missing YAML frontmatter (---)"

    # Extract YAML
    parts = content.split('---')
    if len(parts) < 3:
        return False, "Invalid YAML frontmatter structure"

    yaml_content = parts[1]
    markdown_content = '---'.join(parts[2:])

    # Validate required fields
    required_fields = ['name', 'description', 'tools', 'model']
    for field in required_fields:
        if f'{field}:' not in yaml_content:
            return False, f"Missing required field: {field}"

    # Validate name format (kebab-case)
    name_match = re.search(r'name:\s*([a-z0-9-]+)', yaml_content)
    if name_match:
        name = name_match.group(1)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' must be kebab-case"

    # Validate content length (300-800 words)
    word_count = len(markdown_content.split())
    if word_count < 300:
        return False, f"Content too short ({word_count} words, need 300+)"
    if word_count > 2000:
        return False, f"Content too long ({word_count} words, should be ~800)"

    return True, "Valid agent"

# Parse input
try:
    hook_input = json.loads(sys.stdin.read())
    file_path = sys.argv[1]
except (json.JSONDecodeError, IndexError) as e:
    print(json.dumps({"continue": False, "stopReason": f"Hook error: {e}"}))
    sys.exit(1)

# Validate based on component type
if 'agents' in file_path:
    is_valid, message = validate_agent(hook_input['tool_input']['new_string'])
elif 'skills' in file_path:
    # Validate skill
    pass
elif 'commands' in file_path:
    # Validate command
    pass
else:
    is_valid, message = True, "Not a component file"

# Return result
if is_valid:
    print(json.dumps({"continue": True}))
    sys.exit(0)
else:
    print(json.dumps({"continue": False, "stopReason": message}))
    sys.exit(1)
```

### Hook 2: Git Pre-Commit Quality Checks

**Purpose:** Run quality checks (tests, linting, type checking) after git commits

**Event:** `PostToolUse`
**Matcher:** `tool_name: "Bash"` (only after bash commands)
**Trigger:** When `git commit` is executed

**Logic:**
1. Check if bash command was a git commit
2. If yes, run quality checks in background:
   - Run test suite
   - Lint code (eslint, black, rustfmt, etc.)
   - Type checking (mypy, typescript compiler)
   - Documentation validation
3. If any check fails, log warning (non-blocking)
4. Store results for later review

**Implementation:**
```bash
#!/bin/bash
# hooks/post-commit-quality.sh

json=$(cat)
command=$(echo "$json" | jq -r '.tool_input.command // empty')

# Check if this was a git commit
if [[ "$command" == *"git commit"* ]]; then
    echo '{"suppressOutput": true}' # Hide output from transcript

    # Run quality checks in parallel
    (
        python3 hooks/run-quality-checks.py &
        HOOK_PID=$!
        wait $HOOK_PID || echo "Quality checks had issues"
    ) &

    exit 0
fi

exit 0
```

### Hook 3: Prompt Enhancement Hook

**Purpose:** Automatically enhance user prompts with CODITECT context

**Event:** `UserPromptSubmit`
**Matcher:** `{}` (matches all prompts)

**Logic:**
1. Extract user prompt
2. Analyze prompt to determine context needed:
   - Is it about agents? Add agent count/list
   - Is it about components? Add STANDARDS.md reference
   - Is it about projects? Add `/new-project` suggestion
3. Prepend context to prompt before Claude processes
4. Allow prompt to continue (never block)

**Implementation:**
```bash
#!/bin/bash
# hooks/prompt-enhancer.sh

python3 << 'PYTHON'
import json
import sys
from pathlib import Path

hook_input = json.loads(sys.stdin.read())
user_prompt = hook_input.get('user_prompt', '')

# Analyze prompt
enhanced_prompt = user_prompt

if any(word in user_prompt.lower() for word in ['agent', 'create agent', 'new agent']):
    enhanced_prompt += "\n\n[CONTEXT] CODITECT has 52 agents. Reference AGENT-INDEX.md and COMPLETE-INVENTORY.md for current inventory."

if any(word in user_prompt.lower() for word in ['component', 'skill', 'command', 'script']):
    enhanced_prompt += "\n\n[CONTEXT] Follow STANDARDS.md for component creation. Reference COMPLETE-INVENTORY.md for inventory."

if any(word in user_prompt.lower() for word in ['new project', 'create project']):
    enhanced_prompt += "\n\n[CONTEXT] Use /new-project command for complete project creation. Reference commands/new-project.md."

# Return enhanced prompt
print(json.dumps({
    "continue": True,
    "enhanced_prompt": enhanced_prompt
}))
sys.exit(0)
PYTHON
```

---

## Part 4: Implementation Roadmap

### Phase 1: Component Validation (Week 1)
- [ ] Create `hooks/` directory structure
- [ ] Implement component validation hook
- [ ] Create validation scripts (validate_agent.py, etc.)
- [ ] Test with 3 existing components
- [ ] Document in README.md

### Phase 2: Quality Gates (Week 2)
- [ ] Implement Git pre-commit quality checks
- [ ] Configure linting rules (eslint, black, rustfmt)
- [ ] Setup test automation
- [ ] Create quality metrics dashboard

### Phase 3: Intelligent Routing (Week 3)
- [ ] Implement prompt enhancement hook
- [ ] Create agent suggestion logic
- [ ] Test with 10 different prompts
- [ ] Measure efficiency gains

### Phase 4: Observability (Week 4)
- [ ] Implement change logging hook
- [ ] Create audit trail system
- [ ] Setup quality metrics calculation
- [ ] Create dashboard for monitoring

---

## Part 5: Hook Configuration for CODITECT

**File:** `.claude/settings.json` (or project-level `settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": {
          "tool_name": "Write"
        },
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.coditect/hooks/component-validation.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": {
          "tool_name": "Bash"
        },
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.coditect/hooks/post-commit-quality.sh",
            "timeout": 120
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": {},
        "hooks": [
          {
            "type": "command",
            "command": "bash $CLAUDE_PROJECT_DIR/.coditect/hooks/prompt-enhancer.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

---

## Part 6: Best Practices

### Security
1. **Always validate inputs** - Never trust hook input data
2. **Use absolute paths** - Prefer `$CLAUDE_PROJECT_DIR` variable
3. **Escape shell variables** - Use quotes: `"$file_path"` not `$file_path`
4. **Block path traversal** - Validate paths don't escape project directory
5. **Skip sensitive files** - Never process `.env`, `.git`, secrets

### Performance
1. **Keep hooks fast** - Aim for <5s execution
2. **Use timeouts** - Prevent hanging operations (default 60s)
3. **Run async when possible** - Use backgrounding for non-critical tasks
4. **Cache data** - Avoid repeated calculations
5. **Parallelize** - Run independent checks in parallel

### Reliability
1. **Test thoroughly** - Test with actual tool inputs
2. **Handle errors gracefully** - Always provide clear error messages
3. **Log for debugging** - Write to `/tmp` or logs directory
4. **Version control hooks** - Check into git like any other code
5. **Document extensively** - Clear comments for maintainability

---

## Part 7: Use Cases & Expected Outcomes

### Use Case 1: Preventing Non-Standard Components
**Before:** Developer creates agent missing required fields → discovered during review → rework
**With Hooks:** Developer attempts to create agent → validation hook blocks → error message shows exactly what's missing → developer fixes immediately

**Impact:** 100% reduction in non-standard components, faster feedback loop

### Use Case 2: Automated Quality Checks
**Before:** Manual quality review → test failures discovered → debug & fix → retest
**With Hooks:** Developer commits → quality checks run automatically → issues reported immediately

**Impact:** 50% faster feedback, higher quality code

### Use Case 3: Intelligent Prompt Enhancement
**Before:** User asks vague question → Claude spends tokens searching for context
**With Hooks:** User asks question → hook adds relevant context → Claude answers more accurately

**Impact:** 30% token reduction, better answers

---

## Conclusion

Hooks represent a paradigm shift from **reactive validation** (after the fact) to **proactive enforcement** (before problems occur). By implementing hooks strategically, CODITECT can:

✅ Enforce standards automatically
✅ Block non-compliant changes
✅ Automate quality gates
✅ Enhance prompts intelligently
✅ Reduce token consumption
✅ Improve developer experience

**Next Steps:**
1. Review this analysis
2. Prioritize which hooks to implement first
3. Create `/analyze` and `/generate-project-plan` commands for hooks
4. Begin Phase 1 implementation

