# CODITECT Component Creation Standards & Guide

**Last Updated:** 2025-11-21
**Status:** Production Ready
**Scope:** Agents, Skills, Commands, Scripts

---

## Executive Summary

This document is the **authoritative standard** for creating new CODITECT components. It covers the exact formats, structures, and conventions used throughout the CODITECT framework.

**Key Point:** Standards are **already established and in use** - this guide documents existing patterns from 50+ agents, 24+ skills, and 74+ commands.

---

## 1. AGENT CREATION STANDARD

### 1.1 File Location & Naming

```
.coditect/agents/
├── agent-name-1.md          # Snake-case with hyphens
├── agent-name-2.md
└── agent-name-3.md
```

**Rules:**
- Filename: `lower-case-with-hyphens.md`
- One agent per file
- Location: `.coditect/agents/` directory

### 1.2 Agent File Format

**Structure:** YAML Frontmatter + Markdown Content

```markdown
---
name: agent-name-here
description: One-sentence description of what this agent does. Concise and clear.
tools: Read, Write, Edit, Glob, LS, Grep, Bash, TodoWrite
model: sonnet
---

# Agent Name (Human Readable)

## Core Responsibilities

1. **First Responsibility**
   - Detailed explanation
   - With examples if helpful

2. **Second Responsibility**
   - Detailed explanation

## How This Agent Works

[Detailed explanation of capabilities and approach]

## When to Use This Agent

✅ **Use this agent for:**
- Clear use case 1
- Clear use case 2

❌ **Don't use this agent for:**
- Anti-pattern 1
- Anti-pattern 2

## Context Awareness (Optional)

If agent has special auto-detection capabilities:

```yaml
context_awareness:
  auto_scope_keywords: ["keyword1", "keyword2"]
  patterns:
    pattern_type: ["indicator1", "indicator2"]
```

## Example Usage

```
Task(
    subagent_type="general-purpose",
    prompt="Use the [agent-name] subagent to [specific task]"
)
```
```

### 1.3 YAML Frontmatter Reference

| Field | Required | Type | Example |
|-------|----------|------|---------|
| `name` | ✅ Yes | String | `agent-name` |
| `description` | ✅ Yes | String | "One-sentence description" |
| `tools` | ✅ Yes | List | `Read, Write, Edit, Bash` |
| `model` | ✅ Yes | String | `sonnet` or `haiku` |
| `context_awareness` | ❌ No | YAML | Auto-detection patterns |

**Valid Tools:** Read, Write, Edit, Bash, Glob, Grep, LS, TodoWrite, WebSearch, WebFetch, Glob

### 1.4 Agent Naming Convention

```
coditect-category-specialist     # For domain specialists
orchestrator                      # For coordinators
analyzer                          # For research/analysis
developer                         # For implementation
architect                         # For design
manager                           # For process management
specialist                        # For specific domain expertise
```

**Examples:**
- `rust-expert-developer` - Rust development specialist
- `frontend-react-typescript-expert` - React/TS specialist
- `orchestrator` - Multi-agent coordinator
- `competitive-market-analyst` - Market research specialist

### 1.5 Real Agent Examples

**Example 1: project-organizer**
```yaml
---
name: project-organizer
description: Maintains production-ready directory structure...
tools: Read, Write, Edit, Glob, LS, Grep, Bash, TodoWrite
model: sonnet
---
```

**Example 2: codebase-analyzer**
```yaml
---
name: codebase-analyzer
description: Technical codebase analysis specialist for understanding...
tools: Read, Write, Edit, Grep, Glob, LS, TodoWrite
model: sonnet
---
```

---

## 2. SKILL CREATION STANDARD

### 2.1 Skill Directory Structure

```
.coditect/skills/
└── skill-name/                          # Kebab-case directory
    ├── SKILL.md                         # Main documentation (REQUIRED)
    ├── README.md                        # Quick start guide
    ├── config.md                        # Configuration details
    ├── implementation.py                # Implementation code (if applicable)
    └── quickstart.md                    # Quick examples
```

**Rules:**
- Directory name: `lower-case-with-hyphens`
- SKILL.md: **REQUIRED** - Main entry point
- One skill per directory
- Implementation files optional (if skill includes code)

### 2.2 SKILL.md Format

**Structure:** YAML Frontmatter + Markdown Content

```markdown
---
name: skill-name
description: One-sentence description of the skill capability
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
metadata:
  token-multiplier: "15x"
  max-context-per-file: "5000"
  checkpoint-storage: ".coditect/checkpoints/"
  supported-languages: "Python, TypeScript, JavaScript"
---

# Skill Name (Human Readable)

Production-ready [description of what this skill does].

## When to Use This Skill

✅ **Use skill-name when:**
- Use case 1
- Use case 2

❌ **Don't use skill-name when:**
- Anti-pattern 1
- Anti-pattern 2

## Core Capabilities

### 1. First Capability
Description and examples

### 2. Second Capability
Description and examples

## Usage Pattern

### Step 1: Initialization
```
Code example
```

### Step 2: Execution
```
Code example
```

## Token Budgets

| Scenario | Files | Budget | Savings |
|----------|-------|--------|---------|
| Small Task | 3-5 | 15K | 20% |
| Medium Task | 5-10 | 30K | 37% |

## Integration

How this skill integrates with the rest of CODITECT.
```

### 2.3 Skill Metadata Reference

| Field | Required | Purpose | Example |
|-------|----------|---------|---------|
| `name` | ✅ Yes | Skill identifier | `code-editor` |
| `description` | ✅ Yes | One-line description | "Autonomous code modification system" |
| `license` | ✅ Yes | License type | `MIT` |
| `allowed-tools` | ✅ Yes | Tools available | `[Read, Write, Edit, Bash]` |
| `metadata.token-multiplier` | ❌ No | Estimated token savings | `"15x"` |
| `metadata.max-context-per-file` | ❌ No | Max context size | `"5000"` |
| `metadata.checkpoint-storage` | ❌ No | Checkpoint location | `".coditect/checkpoints/"` |
| `metadata.supported-languages` | ❌ No | Languages supported | `"Python, TypeScript, Rust"` |

### 2.4 Required Markdown Sections

Every SKILL.md must include:

1. **When to Use This Skill** (✅/❌ format)
2. **Core Capabilities** (numbered list with details)
3. **Usage Pattern** (step-by-step instructions)
4. **Token Budgets** (if applicable, table format)
5. **Integration** (how it fits into CODITECT)

### 2.5 Real Skill Examples

**Example: code-editor**
- Location: `.coditect/skills/code-editor/`
- Files: SKILL.md (13KB), README.md, config.md, implementation.py (906 lines)
- Purpose: Multi-file code modifications with checkpoint/rollback
- Token Multiplier: 15x (30-40% savings on multi-file features)

**Example: build-deploy-workflow**
- Location: `.coditect/skills/build-deploy-workflow/`
- Purpose: Automated build, deploy, and documentation workflow
- Integration: GCP Cloud Build + GKE deployment

---

## 3. COMMAND CREATION STANDARD

### 3.1 File Location & Naming

```
.coditect/commands/
├── command-name.md                      # Kebab-case, matches command
└── another-command.md
```

**Rules:**
- Filename: `lower-case-with-hyphens.md`
- Filename MUST match command name (without leading `/`)
- One command per file
- Location: `.coditect/commands/` directory

### 3.2 Command File Format

**Structure:** YAML Frontmatter + Markdown Content

```markdown
---
name: command-name
description: One-sentence description of what this command does
---

# Command Name (Human Readable)

One paragraph introduction explaining the purpose and when to use this command.

## Usage

```bash
/command-name [arguments]
```

## Examples

### Example 1: Basic Usage
```bash
/command-name basic-argument
```
Result or explanation

### Example 2: Advanced Usage
```bash
/command-name --option value
```
Result or explanation

## Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--option` | string | No | What this option does |

## Output Format

[Description of what the command returns]

## When to Use

✅ **Use this command when:**
- Use case 1
- Use case 2

❌ **Don't use this command when:**
- Anti-pattern 1

## Related Commands

- `/related-command-1` - For related task
- `/related-command-2` - For similar task
```

### 3.3 YAML Frontmatter Reference

| Field | Required | Type | Example |
|-------|----------|------|---------|
| `name` | ✅ Yes | String | `command-name` |
| `description` | ✅ Yes | String | "One-sentence description" |

### 3.4 Command Naming Convention

```
/action-noun-specifics    # General format
/setup-submodule          # Specific example
/verify-compliance        # Specific example
/batch-deploy-services    # Specific example
```

### 3.5 Real Command Examples

**Example 1: /action**
```yaml
---
name: action
description: Implementation mode - emits working code in persistent artifacts
---
```

**Example 2: /agent-dispatcher**
```yaml
---
name: agent-dispatcher
description: Intelligent agent selection and invocation syntax generator
---
```

---

## 4. SCRIPT CREATION STANDARD

### 4.1 File Location & Naming

```
.coditect/scripts/
├── python-scripts/
│   ├── script-name.py
│   ├── another-script.py
│   └── requirements.txt
├── bash-scripts/
│   ├── script-name.sh
│   └── another-script.sh
└── core/
    └── utility-scripts/
```

**Rules:**
- Python scripts: `script-name.py` in `python-scripts/`
- Bash scripts: `script-name.sh` in `bash-scripts/`
- Executable bit: `chmod +x script-name.py` or `chmod +x script-name.sh`
- Documentation: Inline comments + optional `README.md`

### 4.2 Python Script Format

**Structure:** Shebang + Docstring + Code

```python
#!/usr/bin/env python3
"""
Script Name - One-line description

Detailed description of what this script does and when to use it.

Usage:
    python3 script-name.py [arguments]
    ./script-name.py [arguments]

Examples:
    # Example 1
    python3 script-name.py --option value

    # Example 2
    ./script-name.py input-file.txt

Requirements:
    - Python 3.9+
    - gitpython >= 3.1.0
    - other dependencies

Exit Codes:
    0: Success
    1: General error
    2: Configuration error
"""

import sys
import argparse
from pathlib import Path

# ... implementation ...

if __name__ == "__main__":
    # Entry point
    pass
```

**Key Components:**
- Shebang: `#!/usr/bin/env python3`
- Docstring: Detailed description, usage, examples
- Type hints: Function signatures with types
- Error handling: Try/except with meaningful messages
- Logging: Use Python logging module
- Exit codes: Clear return codes

### 4.3 Bash Script Format

**Structure:** Shebang + Comments + Code

```bash
#!/bin/bash

# Script Name
# One-line description
#
# Detailed description of what this script does
#
# Usage:
#     ./script-name.sh [arguments]
#
# Examples:
#     ./script-name.sh --option value
#
# Requirements:
#     - bash 4.0+
#     - git
#     - other tools
#
# Exit Codes:
#     0: Success
#     1: General error
#     2: Configuration error

set -euo pipefail  # Exit on error, undefined variables, pipe failures

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# Error handler
error() {
    echo -e "${RED}ERROR: $*${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✓ $*${NC}"
}

# ... implementation ...

main() {
    # Main script logic
    :
}

main "$@"
```

**Key Components:**
- Shebang: `#!/bin/bash`
- `set -euo pipefail`: Error handling
- Color output: For CLI readability
- Functions: `main()`, `error()`, `success()`
- Error codes: Clear exit codes

### 4.4 Real Script Examples

**Example 1: coditect-router** (Bash)
- Purpose: AI command selection tool
- Location: `.coditect/scripts/coditect-router`

**Example 2: create-checkpoint.py** (Python)
- Purpose: Automated checkpoint creation
- Location: `.coditect/scripts/create-checkpoint.py`
- Lines: ~900

**Example 3: coditect-setup.py** (Python)
- Purpose: Interactive project setup
- Location: `.coditect/scripts/coditect-setup.py`
- Lines: ~850

---

## 5. INTEGRATION CHECKLIST

### 5.1 After Creating an Agent

- [ ] File in `.coditect/agents/agent-name.md`
- [ ] YAML frontmatter with all required fields
- [ ] `name` matches filename (without `.md`)
- [ ] `tools` list is accurate and up-to-date
- [ ] `model` is either `sonnet` or `haiku`
- [ ] Markdown content includes:
  - [ ] Core Responsibilities section
  - [ ] How This Agent Works section
  - [ ] When to Use section (with ✅ and ❌)
  - [ ] Example Usage section
- [ ] Tested invocation via Task tool
- [ ] Added to AGENT-INDEX.md with description

### 5.2 After Creating a Skill

- [ ] Directory created: `.coditect/skills/skill-name/`
- [ ] SKILL.md created with YAML frontmatter
- [ ] All required metadata fields present
- [ ] README.md created with quick start
- [ ] Implementation files (if applicable) present
- [ ] When to Use section includes ✅ and ❌
- [ ] Core Capabilities documented with examples
- [ ] Token budgets documented (if applicable)
- [ ] Integration section describes CODITECT fit
- [ ] Tested from agent or command
- [ ] Added to skills registry (if applicable)

### 5.3 After Creating a Command

- [ ] File in `.coditect/commands/command-name.md`
- [ ] YAML frontmatter with `name` and `description`
- [ ] `name` matches filename (without `.md`)
- [ ] Usage section shows correct syntax
- [ ] Examples section with 2+ working examples
- [ ] When to Use section with ✅ and ❌
- [ ] Related Commands section links similar commands
- [ ] Tested via slash command invocation
- [ ] Added to command documentation/index

### 5.4 After Creating a Script

- [ ] File in `.coditect/scripts/script-name.py` or `.sh`
- [ ] Executable bit set: `chmod +x script-name`
- [ ] Shebang correct for language
- [ ] Docstring/comments complete
- [ ] Usage examples provided
- [ ] Error handling implemented
- [ ] Exit codes documented
- [ ] Tested locally
- [ ] Added to documentation/index

---

## 6. BEST PRACTICES

### 6.1 Naming Conventions

| Component | Convention | Example |
|-----------|-----------|---------|
| Agents | `lower-case-with-hyphens` | `rust-expert-developer` |
| Skills | `lower-case-with-hyphens` | `code-editor` |
| Commands | `/lower-case-with-hyphens` | `/setup-submodule` |
| Scripts | `script-name.py` or `.sh` | `coditect-setup.py` |

### 6.2 Description Guidelines

**Agent Description (one sentence):**
```
"Technical codebase analysis specialist for understanding implementation details,
architectural patterns, and code structure."
```

**Skill Description (one sentence):**
```
"Autonomous code modification system with multi-file orchestration, dependency
management, and checkpoint rollback."
```

**Command Description (one sentence):**
```
"Intelligent agent selection and invocation syntax generator for finding the
right agent for any task."
```

### 6.3 Documentation Quality

**Minimum Documentation:**
- One-sentence purpose statement
- Clear when to use (✅ and ❌ sections)
- Working examples
- Integration guidance

**Excellent Documentation:**
- Detailed capability descriptions
- Multiple usage scenarios
- Token budget estimates
- Integration patterns
- Troubleshooting guidance

### 6.4 Code Quality Standards

**Python Scripts:**
- Type hints on all functions
- Docstrings for all public functions
- Error handling with meaningful messages
- Logging for debugging
- Requirements.txt for dependencies

**Bash Scripts:**
- `set -euo pipefail` for safety
- Functions for reusability
- Color output for readability
- Clear error messages
- Comments for complex logic

---

## 7. COMMON PATTERNS & TEMPLATES

### 7.1 Agent File Template

```markdown
---
name: agent-name
description: One-sentence description of what this agent does
tools: Read, Write, Edit, Glob, LS, Grep, Bash, TodoWrite
model: sonnet
---

# Agent Name

[Brief introduction - 2-3 sentences]

## Core Responsibilities

1. **First Responsibility**
   - Detail 1
   - Detail 2

2. **Second Responsibility**
   - Detail 1
   - Detail 2

## How This Agent Works

[2-3 paragraphs explaining approach and methodology]

## When to Use This Agent

✅ **Use this agent for:**
- Use case 1
- Use case 2

❌ **Don't use this agent for:**
- Anti-pattern 1
- Anti-pattern 2

## Example Usage

```
Task(
    subagent_type="general-purpose",
    prompt="Use the agent-name subagent to [specific task]"
)
```
```

### 7.2 Skill SKILL.md Template

```markdown
---
name: skill-name
description: One-sentence description
license: MIT
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  token-multiplier: "10x"
  supported-languages: "Python, TypeScript"
---

# Skill Name

[Description and introduction]

## When to Use This Skill

✅ **Use skill-name when:**
- Use case 1
- Use case 2

❌ **Don't use skill-name when:**
- Anti-pattern 1

## Core Capabilities

### 1. First Capability
[Description and example]

### 2. Second Capability
[Description and example]

## Usage Pattern

### Step 1: Initialize
[Instructions and code]

### Step 2: Execute
[Instructions and code]

## Token Budgets

| Scenario | Budget | Savings |
|----------|--------|---------|
| Small | 10K | 20% |
| Large | 50K | 40% |
```

### 7.3 Command File Template

```markdown
---
name: command-name
description: One-sentence description
---

# Command Name

[Introduction paragraph]

## Usage

```bash
/command-name [arguments]
```

## Examples

### Example 1: Basic Usage
```bash
/command-name basic-arg
```

### Example 2: Advanced Usage
```bash
/command-name --option value
```

## When to Use

✅ **Use this command when:**
- Use case 1

❌ **Don't use when:**
- Anti-pattern 1
```

---

## 8. TROUBLESHOOTING

### Issue: Agent not recognized

**Symptoms:** Task tool doesn't find the agent

**Causes:**
1. Filename doesn't match `name` field (check for typos)
2. Missing YAML frontmatter or incorrect format
3. Agent not in `.coditect/agents/` directory

**Solution:**
1. Verify filename matches: `agent-name.md`
2. Verify YAML frontmatter is valid (test with YAML parser)
3. Verify location: `.coditect/agents/agent-name.md`

### Issue: Skill not loading

**Symptoms:** Skill invoke fails or not found

**Causes:**
1. SKILL.md missing in skill directory
2. Directory structure incorrect
3. Metadata parsing error

**Solution:**
1. Ensure directory structure: `.coditect/skills/skill-name/SKILL.md`
2. Validate SKILL.md YAML frontmatter
3. Check metadata field formats

### Issue: Command not executing

**Symptoms:** `/command-name` not recognized

**Causes:**
1. Filename doesn't match command name
2. Command file in wrong location
3. YAML frontmatter missing or malformed

**Solution:**
1. Verify filename: `command-name.md` (matches `/command-name`)
2. Verify location: `.coditect/commands/command-name.md`
3. Validate YAML frontmatter

---

## 9. VALIDATION CHECKLIST

Before publishing any component:

### Agent Validation
- [ ] File named correctly (kebab-case)
- [ ] YAML frontmatter valid
- [ ] All required fields present
- [ ] Tools list accurate
- [ ] When to Use section complete
- [ ] Examples provided
- [ ] Tested with Task tool

### Skill Validation
- [ ] Directory structure correct
- [ ] SKILL.md present with frontmatter
- [ ] README.md with quick start
- [ ] When to Use section complete
- [ ] Core Capabilities detailed
- [ ] Usage examples included
- [ ] Token budgets documented (if applicable)
- [ ] Integration described

### Command Validation
- [ ] File named correctly (matches command)
- [ ] YAML frontmatter valid
- [ ] Usage syntax correct
- [ ] Examples working
- [ ] When to Use complete
- [ ] Related Commands listed
- [ ] Tested with slash command

### Script Validation
- [ ] Correct location
- [ ] Executable bit set
- [ ] Shebang correct
- [ ] Docstring complete
- [ ] Error handling implemented
- [ ] Exit codes documented
- [ ] Tested locally

---

## 10. RESOURCES & REFERENCES

### Official CODITECT Documentation
- `.coditect/CLAUDE.md` - CODITECT configuration
- `.coditect/AGENT-INDEX.md` - Agent catalog
- `.coditect/docs/` - Detailed documentation
- `submodules/core/coditect-core/README.md` - Framework overview

### Real Examples
- **Agent:** `.coditect/agents/project-organizer.md`
- **Skill:** `.coditect/skills/code-editor/SKILL.md`
- **Command:** `.coditect/commands/action.md`
- **Script:** `.coditect/scripts/coditect-router`

### Related Standards
- **Repository Naming:** `submodules/core/coditect-core/docs/REPO-NAMING-CONVENTION.md`
- **Git Workflows:** `.coditect/scripts/coditect-git-helper.py`
- **Project Planning:** `submodules/core/coditect-core/PROJECT-PLAN.md`

---

## 11. NEXT STEPS

To create your first component:

1. **Choose Component Type**
   - Agent: Use Section 1
   - Skill: Use Section 2
   - Command: Use Section 3
   - Script: Use Section 4

2. **Use Template**
   - Copy appropriate template from Section 7
   - Customize for your use case
   - Follow naming conventions from Section 6.1

3. **Follow Checklist**
   - Use appropriate checklist from Section 5
   - Verify all items checked off
   - Test thoroughly

4. **Validate**
   - Use validation checklist from Section 9
   - Test with actual framework tools
   - Document any special behavior

5. **Integrate**
   - Add to appropriate index/registry
   - Update CLAUDE.md if necessary
   - Create checkpoint with changes

---

**This standard is production-proven and actively used across 50+ agents, 24+ skills, and 74+ commands in CODITECT.**
