# CODITECT STANDARDS - SPECIFICATION

**Version:** 1.0 - Final
**Status:** ✅ Authoritative specification for agentic automation
**Scope:** Complete specification for all component creation
**Use:** Agents use this to create new components autonomously

---

## AGENTS

**Location:** `.coditect/agents/`
**File:** `agent-name-kebab-case.md`
**Count:** 50+ existing
**Compliance:** 100%

### YAML Frontmatter (Required)

```yaml
---
name: agent-name-kebab-case
description: [1-3 sentence description of agent's specialty]
tools: Tool1, Tool2, Tool3
model: sonnet
color: [optional: yellow, blue, green, red, cyan, magenta, white]
context_awareness: [optional: auto-detection patterns]
---
```

**Field Specifications:**

| Field | Type | Rules | Example |
|-------|------|-------|---------|
| `name` | string | kebab-case, matches filename, 1-50 chars | `codebase-analyzer` |
| `description` | string | Start with role, specific purpose, max 200 chars | `Technical analysis specialist...` |
| `tools` | list | Comma-separated, must be available tools | `Read, Write, Edit, Bash` |
| `model` | string | Always `sonnet` | `sonnet` |
| `color` | string | Optional, for CLI output | `yellow` |
| `context_awareness` | object | Optional, for auto-detection | See section 2.4 |

### Markdown Sections (Required)

```markdown
You are a [Role]. [One sentence purpose].

## Core Responsibilities

1. **[Title]**
   - [Capability/task]
   - [Capability/task]

2. **[Title]**
   - [Capability/task]

## Important Guidelines

- [Rule 1]
- [Rule 2]
- [Rule 3]
```

**Minimum requirements:**
- Opening: "You are a..." + purpose statement
- Core Responsibilities: 2-5 numbered items, 2-4 bullets each
- Important Guidelines: 3-7 clear rules
- Total length: 300-800 words

---

## SKILLS

**Location:** `.coditect/skills/[skill-name]/`
**Entry Point:** `SKILL.md` (Required)
**Count:** 24+ existing
**Compliance:** 100%

### Directory Structure

```
skill-name/
├── SKILL.md              [Required]
├── README.md             [Optional - user guide]
├── core/                 [Optional - Python code if applicable]
│   ├── main.py
│   └── requirements.txt
├── examples/             [Optional - usage examples]
└── templates/            [Optional - reusable templates]
```

**Rules:**
- Directory name: `kebab-case`, matches `name` field
- SKILL.md: Always required
- Other files: Create only if content exists
- No empty directories

### SKILL.md Format

```yaml
---
name: skill-name-kebab-case
description: [What Claude can do with this skill]
license: MIT
allowed-tools: [Tool1, Tool2]
metadata:
  token-multiplier: "10x"
  supported-languages: "Python, TypeScript"
---

## When to Use This Skill

✅ Use when:
- Case 1
- Case 2

❌ Don't use when:
- Anti-pattern 1
- Anti-pattern 2

## Core Capabilities

### 1. [Capability]
[Description]

### 2. [Capability]
[Description]

## Usage Pattern

### Step 1: [Title]
[Instructions]

### Step 2: [Title]
[Instructions]

### Step 3: [Title]
[Instructions]
```

**Minimum requirements:**
- YAML with name, description, license, allowed-tools
- "When to Use" with ✅ and ❌
- "Core Capabilities" with 2-4 items
- "Usage Pattern" with 2-4 steps
- Total length: 500-1200 words

### Python in core/ (If Applicable)

```python
#!/usr/bin/env python3
"""
[Module title]

[Detailed description of what this module does]

Usage:
    from module_name import MainClass
    result = MainClass().execute(data)
"""

from typing import Dict, Any

class MainClass:
    """Main implementation class."""

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute operation."""
        return {}
```

**Requirements:**
- Shebang: `#!/usr/bin/env python3`
- Module docstring with usage
- Type hints on all functions
- Class-based structure recommended
- requirements.txt for dependencies

---

## COMMANDS

**Location:** `.coditect/commands/`
**File:** `command-name.md` (no YAML unless needed)
**Count:** 74+ existing
**Compliance:** 85% (legacy naming variation; new commands use hyphens)

### File Format

```markdown
# [Command Title]

[One paragraph: what command does and when to use it]

## Steps to follow:

### Step 1: [Title]
[Instructions for what Claude should do]

### Step 2: [Title]
[Instructions for what Claude should do]

### Step 3: [Title]
[Instructions for what Claude should do]

## Important notes:

- [Constraint or guideline 1]
- [Constraint or guideline 2]
- [Constraint or guideline 3]
```

**Naming:**
- **NEW commands:** Use hyphens (`/command-name`)
- **Legacy commands:** May use underscores (compatibility)
- Pattern: `[verb]-[noun]` (e.g., `/setup-project`, `/verify-compliance`)

**Requirements:**
- Clear title
- Purpose paragraph
- "Steps to follow" section
- "Important notes" section
- Total length: 300-600 words

**Optional YAML (rarely used):**

```yaml
---
name: command-name
description: One-sentence description
---
```

---

## SCRIPTS

**Location:** `.coditect/scripts/`
**Naming:** `script-name.py` or `script-name.sh`
**Count:** 55+ existing
**Compliance:** 95% (Python) / 80% (Bash)

### Python Script

```python
#!/usr/bin/env python3
"""
[Script Title]

[Detailed description of what this script does]

Usage:
    python3 script-name.py [args]

Examples:
    python3 script-name.py --option value

Requirements:
    - Python 3.9+
    - Package >= 1.0

Exit Codes:
    0: Success
    1: General error
    2: Usage error
"""

import sys
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def main() -> int:
    """Main entry point."""
    try:
        # Implementation
        return 0
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Requirements:**
- Shebang: `#!/usr/bin/env python3`
- Complete module docstring with usage, examples, requirements, exit codes
- Type hints on ALL functions (args and returns)
- Logging (not print)
- Error handling with try/except
- Proper exit codes (0/1/2/3...)
- `if __name__ == "__main__"` guard
- Executable: `chmod +x script-name.py`

### Bash Script

```bash
#!/bin/bash
#
# [Script Title]
#
# [Detailed description]
#
# Usage:
#   ./script-name.sh [options]
#
# Examples:
#   ./script-name.sh --option value
#
# Exit Codes:
#   0: Success
#   1: Error

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

function main() {
    echo -e "${GREEN}✓${NC} Done"
}

main "$@"
```

**Requirements:**
- Shebang: `#!/bin/bash`
- Header comments with description, usage, examples, exit codes
- `set -euo pipefail` (MANDATORY)
- Color definitions
- Function-based structure
- Logging functions (optional)
- Error trap (optional)
- `main()` as entry point
- Executable: `chmod +x script-name.sh`

---

## NAMING CONVENTIONS

| Type | Pattern | Case | Separator | Example | Compliance |
|------|---------|------|-----------|---------|-----------|
| **Agent** | [domain]-[spec] | lowercase | hyphen | `codebase-analyzer` | 100% |
| **Skill** | [domain]-[capability] | lowercase | hyphen | `code-editor` | 100% |
| **Command** | [verb]-[noun] | lowercase | hyphen | `/setup-project` | 85% (legacy variation) |
| **Script** | [purpose]-[action] | lowercase | hyphen | `create-checkpoint.py` | 100% |

**Rules:**
- ALL components: lowercase only
- ALL components: hyphens (not underscores)
- NO abbreviations
- NO version numbers
- Descriptive names (not `tool1`, `utility2`)

---

## FILE ORGANIZATION

```
.coditect/
├── agents/                    [Agent files]
│   └── agent-name.md
├── skills/                    [Skill directories]
│   └── skill-name/
│       ├── SKILL.md
│       ├── core/
│       └── examples/
├── commands/                  [Command files]
│   └── command-name.md
├── scripts/                   [Script files]
│   ├── script-name.py
│   └── script-name.sh
├── hooks/                     [Git hooks]
│   └── pre-commit
├── STANDARDS.md              [THIS FILE]
└── CODITECT-ARCHITECTURE-STANDARDS.md [Detailed reference]
```

---

## VERIFICATION CHECKLIST

### Before Creating Any Component

**Agent:**
- [ ] YAML has: name, description, tools, model
- [ ] Name is kebab-case
- [ ] Markdown has: Opening, Core Responsibilities, Guidelines
- [ ] Tools list is accurate
- [ ] File: `.coditect/agents/agent-name.md`

**Skill:**
- [ ] SKILL.md exists with YAML frontmatter
- [ ] Directory name is kebab-case
- [ ] Name matches directory
- [ ] Has: When to Use, Core Capabilities, Usage Pattern
- [ ] File: `.coditect/skills/skill-name/SKILL.md`

**Command:**
- [ ] Filename is kebab-case (use hyphens for new commands)
- [ ] Has: Title, Purpose, Steps, Notes
- [ ] File: `.coditect/commands/command-name.md`

**Python Script:**
- [ ] Shebang: `#!/usr/bin/env python3`
- [ ] Module docstring complete
- [ ] Type hints on all functions
- [ ] Exit codes defined
- [ ] Executable: `chmod +x`
- [ ] File: `.coditect/scripts/script-name.py`

**Bash Script:**
- [ ] Shebang: `#!/bin/bash`
- [ ] `set -euo pipefail` present
- [ ] Header comments complete
- [ ] Executable: `chmod +x`
- [ ] File: `.coditect/scripts/script-name.sh`

---

## GIT WORKFLOW

### Add Component to Version Control

```bash
# Step 1: Check status
git status

# Step 2: Add component(s)
git add .coditect/agents/new-agent.md
# OR
git add .coditect/skills/new-skill/
# OR
git add .coditect/commands/new-command.md
# OR
git add .coditect/scripts/new-script.py

# Step 3: Verify what will be committed
git diff --cached

# Step 4: Commit with message
git commit -m "Add [component-type]: [description]"

# Step 5: Push to remote
git push origin main
```

---

## COMPLIANCE MATRIX (Current State)

| Type | Count | Compliance | Status |
|------|-------|-----------|--------|
| Agents | 50 | 100% | ✅ Perfect |
| Skills | 24 | 100% | ✅ Perfect |
| Commands | 74 | 85% | ⚠️ Legacy names |
| Scripts | 55 | 95% | ✅ High |
| **Total** | **203** | **95%** | ✅ Production |

---

**This specification enables autonomous agent creation with minimal human prompting.**

**For detailed guidance, reference: `.coditect/CODITECT-ARCHITECTURE-STANDARDS.md`**
