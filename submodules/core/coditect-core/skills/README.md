# Claude Skills for T2 Project

**Last Updated**: 2025-10-18
**Anthropic Skills**: October 2025 Release

## Overview

This directory contains **Claude Skills** - folders with instructions, executable scripts, and resources that Claude loads dynamically when relevant to a task.

### What Are Skills?

Skills are more powerful than commands because they:
- **Composable**: Can stack together
- **Portable**: Same format across Claude Code, API, and Claude.ai
- **Efficient**: Only load when relevant (progressive disclosure)
- **Powerful**: Can include executable Python code (requires Code Execution Tool beta)

### Skills vs Commands vs Agents

| Feature | Commands | Agents | Skills |
|---------|----------|--------|--------|
| Format | Markdown | YAML + Markdown | Folder with SKILL.md + scripts |
| Invocation | `/command-name` | Manual/auto via Task | Auto-loaded when relevant |
| Execution | Claude follows instructions | Specialized AI assistant | Can execute included code |
| Tools | No tools | Specific tools (Read, Grep, etc.) | Executable Python/scripts |
| Scope | Single workflow | Focused specialization | Complete capability |

## Directory Structure

```
.claude/
├── skills/                           # CUSTOM T2 SKILLS (active)
│   ├── multi-agent-workflow/         # ⭐ Token management + orchestration
│   │   ├── SKILL.md                  # Main skill instructions
│   │   ├── core/
│   │   │   ├── token_calculator.py   # Calculate token usage
│   │   │   └── workflow_validator.py # Validate FSM transitions
│   │   └── examples/
│   ├── foundationdb-queries/         # ⭐ FDB patterns + tenant isolation
│   │   └── SKILL.md
│   ├── rust-backend-patterns/        # ⭐ Actix-web + error handling
│   │   └── SKILL.md
│   ├── communication-protocols/      # ⭐ CONTROL commands + delegation (NEW)
│   │   ├── SKILL.md
│   │   ├── core/
│   │   │   ├── validate_control_command.py
│   │   │   └── delegation_template_generator.py
│   │   └── examples/
│   ├── search-strategies/            # ⭐ Grep/Glob optimization + tool selection (NEW)
│   │   ├── SKILL.md
│   │   ├── core/
│   │   │   └── optimize_search.py
│   │   └── examples/
│   └── framework-patterns/           # ⭐ Event-driven + FSM + C4 diagrams (NEW)
│       ├── SKILL.md
│       ├── core/
│       │   ├── generate_c4_diagram.py
│       │   └── fsm_validator.py
│       └── templates/
│
└── skills-reference/                  # REFERENCE SKILLS (submodule)
    └── (anthropics/skills repo)
        ├── algorithmic-art/
        ├── brand-guidelines/
        ├── canvas-design/
        ├── document-skills/          # docx, pdf, pptx, xlsx
        ├── mcp-builder/
        ├── skill-creator/            # Template for new skills
        ├── template-skill/           # Minimal template
        ├── webapp-testing/
        └── ... (12 total reference skills)
```

## Custom T2 Skills

### 1. multi-agent-workflow

**When Claude Uses It**:
- Multi-phase workflows with 3+ phases
- Token usage > 70K (out of 160K limit)
- Cascading multi-module issues
- Need for checkpoint/resume

**Capabilities**:
- Token budget calculation and monitoring
- FSM state validation for recursive workflows
- Complexity assessment with risk zones
- Integration with `/complexity_gauge` and `/recursive_workflow` commands

**Executable Scripts**:
- `core/token_calculator.py` - Calculate token usage estimates
- `core/workflow_validator.py` - Validate FSM state transitions

**Example Usage**:
```python
from core.token_calculator import TokenCalculator

calc = TokenCalculator()
estimate = calc.estimate_file_read(lines=1500)
print(f"Estimated tokens: {estimate.tokens}")
```

### 2. foundationdb-queries

**When Claude Uses It**:
- Working with FDB persistence
- Multi-tenant data access
- Session management queries
- Workflow state persistence

**Capabilities**:
- FDB key pattern reference (all 19 models)
- Tenant isolation enforcement
- Repository pattern guidance
- Transaction error handling

**Key Patterns Covered**:
- `/{tenant_id}/users/{user_id}`
- `/{tenant_id}/workflows/{workflow_id}/state`
- `/{tenant_id}/auth_sessions/{session_id}`
- All models from `backend/src/db/models.rs`

### 3. rust-backend-patterns

**When Claude Uses It**:
- Implementing backend endpoints
- Auth middleware integration
- Error handling in Rust/Actix-web
- Repository pattern usage

**Capabilities**:
- Handler pattern templates
- JWT auth middleware usage
- TransactionCommitError handling
- Repository method references

### 4. communication-protocols (NEW - 2025-10-18)

**When Claude Uses It**:
- Executing CONTROL commands (PAUSE, CHECKPOINT, ESCALATE)
- Creating delegation templates for multi-agent coordination
- Generating handoff documents for session continuity
- Coordinating between orchestrator and subagents

**Capabilities**:
- CONTROL command syntax validation (PAUSE, CHECKPOINT, ESCALATE, RESUME, DELEGATE)
- Standard/parallel/sequential delegation patterns
- Quick handoff document generation (100-200 words)
- Full checkpoint document structure with file:line references
- Integration with orchestrator agent

**Executable Scripts**:
- `core/validate_control_command.py` - Validate CONTROL command syntax
- `core/delegation_template_generator.py` - Generate delegation YAML templates

**Example Usage**:
```python
from core.validate_control_command import ControlCommandValidator

validator = ControlCommandValidator()
is_valid, error, parsed = validator.validate("CONTROL: CHECKPOINT REASON: Token usage at 85%")
if is_valid:
    print(f"Command: {parsed.command.value}, Reason: {parsed.reason}")
```

### 5. search-strategies (NEW - 2025-10-18)

**When Claude Uses It**:
- Searching for code patterns across multiple files
- Locating specific files or directories
- Finding function/class definitions
- Deciding between Grep, Glob, Read, or agent invocation
- Multi-stage searches (broad → narrow → deep)

**Capabilities**:
- Tool selection decision tree (Read, Glob, Grep, agents)
- Multi-stage search patterns (Broad → Narrow → Deep)
- Search optimization rules (start narrow, use type filtering)
- Token cost comparison (manual vs optimized)
- Integration with codebase-locator, codebase-pattern-finder, codebase-analyzer agents

**Executable Scripts**:
- `core/optimize_search.py` - Recommend optimal search strategy and estimate token costs

**Example Usage**:
```python
from core.optimize_search import SearchOptimizer

optimizer = SearchOptimizer()
strategy = optimizer.recommend_strategy("Find all authentication-related files")
print(f"Complexity: {strategy.complexity.value}")
print(f"Estimated tokens: {strategy.estimated_tokens}")
```

**Search Decision Tree**:
- **Known file path** → Use Read (1K-3K tokens)
- **Filename pattern** → Use Glob (500-1K tokens)
- **Content keyword** → Use Grep (1K-5K tokens)
- **Pattern extraction** → Use codebase-pattern-finder (10K-15K tokens)
- **Understanding HOW** → Use codebase-analyzer (12K-20K tokens)
- **Open-ended search** → Use codebase-locator (8K-12K tokens)

### 6. framework-patterns (NEW - 2025-10-18)

**When Claude Uses It**:
- Implementing event-driven architecture
- Designing finite state machines (FSM)
- Creating C4 architecture diagrams
- Building reactive systems
- Modeling complex workflows

**Capabilities**:
- Event-driven architecture patterns (Event, Producer, Consumer, Bus)
- Finite state machine patterns (State, Transition, Guard, Action)
- C4 modeling (Context, Container, Component, Code diagrams)
- Reactive programming patterns (Observer, Streams)
- Integration with T2 recursive workflow FSM

**Executable Scripts**:
- `core/generate_c4_diagram.py` - Generate C4 architecture diagrams in Mermaid format
- `core/fsm_validator.py` - Validate FSM structure and transitions

**Example Usage**:
```python
from core.generate_c4_diagram import C4DiagramGenerator

generator = C4DiagramGenerator()
context_diagram = generator.generate_t2_context_diagram()
print(context_diagram)  # Outputs Mermaid diagram

from core.fsm_validator import create_t2_recursive_workflow_fsm

fsm = create_t2_recursive_workflow_fsm()
is_valid, errors = fsm.validate_structure()
if is_valid:
    print("✓ FSM structure is valid")
```

**FSM States (T2 Recursive Workflow)**:
- INITIATE → IDENTIFY → DOCUMENT → SOLVE → CODE → DEPLOY → TEST → VALIDATE → COMPLETE
- Special states: CHECKPOINT, SUSPENDED, ESCALATED
- Traceback logic: TEST → IDENTIFY/SOLVE/CODE (based on failure type)

## Reference Skills (Submodule)

The `.claude/skills-reference/` directory is a **git submodule** pointing to the official `anthropics/skills` repository.

**Available Reference Skills**:
1. **algorithmic-art** - Generative art creation
2. **artifacts-builder** - Build artifacts
3. **brand-guidelines** - Apply brand styling
4. **canvas-design** - Visual art design
5. **document-skills** - Word, PDF, PowerPoint, Excel manipulation
6. **internal-comms** - Internal communication templates
7. **mcp-builder** - MCP server creation
8. **skill-creator** - Create new skills (use this as a template!)
9. **slack-gif-creator** - Slack GIF generation
10. **template-skill** - Minimal skill template
11. **theme-factory** - Theme creation
12. **webapp-testing** - Web app testing patterns

**Update Reference Skills**:
```bash
cd .claude/skills-reference
git pull origin main
```

## How Claude Uses Skills

### Progressive Disclosure

Claude initially sees only skill names and descriptions. When a skill is relevant to the current task, Claude autonomously loads the SKILL.md file and any necessary resources.

**Example**:
```
User: "Implement user profile editing with backend API"

Claude's thought process:
1. Sees skill: "rust-backend-patterns" (description mentions backend endpoints)
2. Loads SKILL.md to get handler pattern
3. Sees skill: "foundationdb-queries" (description mentions FDB persistence)
4. Loads SKILL.md to get key patterns
5. Uses both skills together to implement feature
```

### Composability

Skills can work together:

```
Task: "Run security audit on authentication system"

Skills Used:
- multi-agent-workflow (orchestrate audit phases, manage tokens)
- rust-backend-patterns (understand auth middleware)
- foundationdb-queries (check session key patterns)
```

## Creating New Skills

### Step 1: Use the Template

```bash
cp -r .claude/skills-reference/template-skill .claude/skills/my-new-skill
cd .claude/skills/my-new-skill
```

### Step 2: Edit SKILL.md

```yaml
---
name: my-new-skill
description: When Claude should use this skill (be specific)
---

# My New Skill

## When to Use

- Scenario 1
- Scenario 2

## Core Capabilities

[Instructions for Claude]

## Examples

[Usage examples]

## Best Practices

✅ Do this
❌ Avoid this
```

### Step 3: Add Executable Scripts (Optional)

```bash
mkdir -p core examples
# Add Python scripts to core/
# Add usage examples to examples/
```

### Step 4: Test the Skill

Use the skill in a Claude Code session and observe:
1. Is it loaded when expected?
2. Does Claude interpret instructions correctly?
3. Do executable scripts run without errors?

## Skill Format Reference

### SKILL.md Structure

```markdown
---
name: unique-skill-identifier   # kebab-case, lowercase
description: Clear, specific description of when to use this skill
---

# Skill Title

## When to Use
[Specific scenarios - be precise!]

## Core Capabilities
[What this skill enables Claude to do]

## Examples
[Concrete usage examples]

## Guidelines
[Rules, constraints, best practices]

## Integration
[How this skill works with others]
```

### Executable Scripts

Skills can include Python scripts that Claude can execute:

```python
#!/usr/bin/env python3
"""
Script description
"""

def main():
    # Implementation
    pass

if __name__ == "__main__":
    main()
```

**Requirements**:
- Must be executable (`chmod +x`)
- Should include docstrings
- Should have example usage in `if __name__ == "__main__"`

## Best Practices

### Writing Effective Skills

✅ **Be Specific**: Clear, precise descriptions of when to use
✅ **Include Examples**: Concrete code examples > abstract explanations
✅ **Add Executable Code**: Python scripts for calculations/validation
✅ **Test Thoroughly**: Verify skills work in real sessions
✅ **Keep Focused**: One skill = one capability/domain
✅ **Document Integration**: How skills work together

❌ **Too Broad**: "General programming help" (not specific enough)
❌ **No Examples**: Instructions without concrete examples
❌ **Untested**: Skills that haven't been used in real sessions
❌ **Overlapping**: Multiple skills doing the same thing

### Skill Naming

- Use kebab-case: `multi-agent-workflow` ✅
- Be descriptive: `foundationdb-queries` ✅
- Avoid generic names: `helpers` ❌
- Match T2 domain: `rust-backend-patterns` ✅

## Integration with T2 Workflow

Skills complement the existing T2 infrastructure:

### Commands (54 total)
- **Purpose**: Explicit workflows invoked with `/command-name`
- **Examples**: `/complexity_gauge`, `/recursive_workflow`, `/create_plan`
- **Use When**: Specific, known workflow needed

### Agents (8 total)
- **Purpose**: Specialized AI assistants with specific tools
- **Examples**: `orchestrator`, `codebase-analyzer`, `codebase-locator`
- **Use When**: Multi-agent coordination or focused analysis needed

### Skills (6 custom + 12 reference)
- **Purpose**: Auto-loaded expertise with executable code
- **Examples**: `multi-agent-workflow`, `communication-protocols`, `search-strategies`
- **Use When**: Domain expertise + calculations/validation needed

### Workflow Pattern

```
1. User: "Implement feature X with security audit"
2. Claude loads skills:
   - multi-agent-workflow (token management)
   - communication-protocols (orchestrator delegation)
   - search-strategies (find auth files efficiently)
   - rust-backend-patterns (handler patterns)
   - foundationdb-queries (FDB persistence)
   - framework-patterns (event-driven for audit logging)
3. Uses /complexity_gauge command (from multi-agent-workflow skill)
4. Invokes orchestrator agent with delegation templates (from communication-protocols skill)
5. Orchestrator uses search-strategies to optimize file searches
6. Executes token_calculator.py to monitor budget
7. Returns comprehensive implementation plan with checkpoints
```

## Troubleshooting

### Skill Not Loading

**Problem**: Claude doesn't use skill when expected

**Solutions**:
- Check description is specific and relevant
- Verify SKILL.md format (YAML frontmatter correct?)
- Test with direct reference: "Use the multi-agent-workflow skill to..."

### Executable Script Fails

**Problem**: Python script in core/ throws errors

**Solutions**:
- Verify script is executable: `chmod +x core/script.py`
- Check Python path: `#!/usr/bin/env python3`
- Test script standalone: `python core/script.py`
- Verify Code Execution Tool beta is enabled

### Skills Overlap/Conflict

**Problem**: Multiple skills provide similar guidance

**Solutions**:
- Merge overlapping skills
- Make descriptions more specific
- Use hierarchical structure (general → specific)

## References

- **Official Repo**: https://github.com/anthropics/skills
- **Documentation**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills
- **Code Execution Tool**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **Research Source**: `thoughts/shared/research/2025-10-18-multi-agent-orchestration-research.md`

## Contributing

When adding new T2 skills:

1. Create skill folder in `.claude/skills/`
2. Follow the template structure
3. Add to this README under "Custom T2 Skills"
4. Test in real Claude Code session
5. Document integration points
6. Commit with message: `feat(skills): Add [skill-name] skill`

---

**Questions?** See `.claude/CLAUDE.md` for overall configuration documentation.
