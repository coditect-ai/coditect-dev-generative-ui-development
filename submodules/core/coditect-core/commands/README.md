# CODITECT Commands Directory

This directory contains 75+ custom slash commands for the CODITECT framework, providing comprehensive automation for AI-first development workflows.

## 🤖 AI Command Router (Easiest Way!)

**Never memorize commands** - just describe what you want:

```bash
# Simple command selection
coditect-router "I need to add user authentication"

# Interactive mode
coditect-router -i

# Quick aliases (add to shell)
alias cr='coditect-router'
alias cri='coditect-router -i'
```

The AI-powered router analyzes your request and recommends the optimal command with reasoning, alternatives, and next steps.

## Command Structure

Each command is defined in a Markdown file with YAML frontmatter:

```markdown
---
name: command-name
description: What this command does
version: 1.0
category: category-name
tags: [tag1, tag2]
keywords: [keyword1, keyword2]
purpose: One-sentence purpose
trigger_phrases:
  - "phrase that triggers this command"
  - "another trigger phrase"
automation_level: fully_automated|semi_automated|interactive
estimated_time: duration
output_files:
  - file1.md
  - file2.md
agents_used:
  - agent-name (role)
requires_human: true|false
---

Instructions for Claude to execute when user types /command-name
```

## Core Commands

### Project Management

#### `/generate-project-plan` (NEW!)
**Autonomous project specification and multi-agent orchestration plan generator**

- **Purpose**: Generate complete PROJECT-PLAN.md and TASKLIST-WITH-CHECKBOXES.md for any submodule
- **Automation**: Fully automated with orchestrator agent coordination
- **Output**: 25-30 KB PROJECT-PLAN.md, 40-50 KB TASKLIST with 180+ tasks
- **Time**: 10-30 minutes (autonomous execution)
- **Agents**: orchestrator, software-design-document-specialist, agent-dispatcher

**Usage**:
```bash
# Navigate to submodule
cd submodules/my-new-project

# Generate comprehensive project plan
/generate-project-plan

# Or use Python script directly
python3 ../../.coditect/scripts/generate-project-plan.py
```

**Features**:
- ✅ Auto-detects submodule context and technology stack
- ✅ Analyzes existing documentation (or generates if missing)
- ✅ Creates 12-week phased implementation plan
- ✅ Generates 180+ checkbox tasks with agent assignments
- ✅ Provides complete orchestrator agent invocation syntax
- ✅ Budget tracking, risk management, success metrics
- ✅ Multi-agent coordination patterns (direct, sequential, parallel, coordinated)

**CR Integration**:
The command router will recommend this when you say:
- "create project plan for [submodule]"
- "generate implementation plan"
- "need project specifications"
- "set up multi-agent orchestration"
- "create tasklist for submodule"

#### `/create_plan`
**Feature-level planning for individual features**

- **Purpose**: Create focused implementation plans for specific features
- **Scope**: Days to 2 weeks, 5-20 tasks
- **Automation**: Interactive with human guidance
- **Best for**: Single features, bug fixes, enhancements

**Comparison with `/generate-project-plan`**:

| Aspect | /generate-project-plan | /create_plan |
|--------|----------------------|--------------|
| **Scope** | Entire submodule | Single feature |
| **Timeline** | Weeks to months | Days to 2 weeks |
| **Tasks** | 180+ tasks | 5-20 tasks |
| **Automation** | Fully autonomous | Interactive |
| **Agents** | Multi-agent orchestration | Single agent or manual |
| **Output** | PROJECT-PLAN + TASKLIST | Simple plan outline |
| **Use Case** | New submodule creation | Feature development |

### Development Workflow

#### `/implement`
Production-ready implementation with error handling, circuit breakers, and observability

#### `/prototype`
Rapid proof-of-concept with focus on core functionality

#### `/debug`
Debug issues with systematic error analysis

#### `/test_generate`
Generate comprehensive unit tests with TDD patterns

### Analysis & Review

#### `/analyze`
Code review and quality assessment

#### `/security_sast`
Static Application Security Testing for vulnerability analysis

#### `/optimize`
Performance optimization and scalability improvements

### Architecture & Strategy

#### `/strategy`
Architectural planning with C4 diagrams and ADRs

#### `/deliberation`
Pure planning mode - analysis and task decomposition without code execution

### Documentation

#### `/document`
Generate comprehensive API docs, architecture diagrams, runbooks, and user guides

### UI Development (NEW!)

#### `/ui`
**AI-powered UI component generation with production-ready React + TypeScript**

- **Purpose**: Generate complete React + TypeScript components with WCAG compliance
- **Tech Stack**: React 18+, TypeScript strict mode, Tailwind CSS, Framer Motion
- **Quality**: WCAG AA minimum (90+ score), bundle size < 50KB, 80%+ test coverage
- **Agents**: generative-ui-intent-analyzer, generative-ui-architect, generative-ui-code-generator, generative-ui-accessibility-auditor, generative-ui-quality-reviewer

**Usage**:
```bash
/ui component button with primary, secondary variants
/ui layout dashboard with sidebar and header
/ui application task manager with CRUD operations
```

#### `/motion`
**Add Framer Motion animations to components**

- **Purpose**: Enhance components with production-ready animations
- **Features**: Entrance/exit, hover, tap, scroll, loading animations
- **Accessibility**: Respects prefers-reduced-motion
- **Performance**: 60fps optimized animations

**Usage**:
```bash
/motion add slide-in animation to sidebar
/motion create loading skeleton for card
/motion add hover effects to button
```

#### `/a11y`
**Comprehensive WCAG 2.1 accessibility auditing**

- **Purpose**: Audit components for AA/AAA compliance
- **Checks**: Semantic HTML, ARIA, keyboard nav, color contrast, focus, screen readers
- **Output**: Violation report with severity levels, remediation steps, before/after examples

**Usage**:
```bash
/a11y audit the dashboard layout
/a11y check navbar for WCAG AAA compliance
/a11y review form accessibility
```

### Agent Coordination

#### `/suggest-agent`
Get agent invocation syntax for any request

#### `/agent-dispatcher`
Intelligent multi-agent orchestration and coordination

#### `/COMMAND-GUIDE`
Decision trees and workflow guidance for command selection

## Command Categories

- **Project Management** (5 commands)
  - `/generate-project-plan`, `/create_plan`, `/create_plan_generic`

- **Development** (12 commands)
  - `/implement`, `/prototype`, `/debug`, `/test_generate`, `/tdd_cycle`

- **Analysis** (8 commands)
  - `/analyze`, `/security_sast`, `/optimize`, `/full_review`

- **Architecture** (6 commands)
  - `/strategy`, `/deliberation`, `/db_migrations`

- **Documentation** (4 commands)
  - `/document`, `/doc_generate`

- **Research** (8 commands)
  - `/research`, `/research_codebase`, `/multi-agent-research`

- **Agent Coordination** (10 commands)
  - `/suggest-agent`, `/agent-dispatcher`, `/COMMAND-GUIDE`

- **Education** (6 commands)
  - `/generate-curriculum-content`

- **Infrastructure** (8 commands)
  - `/build-monitor`, `/deploy-mvp`, `/start-theia`

**Total**: 75+ slash commands

## Quick Reference

### For New Projects/Submodules
1. `/generate-project-plan` - Complete project specification and orchestration plan
2. `/strategy` - Architectural design and system architecture
3. `/implement` - Production-ready implementation

### For Existing Code
1. `/analyze` - Code quality review
2. `/debug` - Fix bugs and errors
3. `/optimize` - Performance improvements
4. `/document` - Generate documentation

### For Research & Planning
1. `/research` - Investigate and explore codebase
2. `/deliberation` - Pure planning without execution
3. `/multi-agent-research` - Comprehensive competitive analysis

### For Agent Help
1. `/suggest-agent` - Get agent syntax recommendations
2. `/agent-dispatcher` - Coordinate multiple agents
3. `/COMMAND-GUIDE` - Command selection guidance

## Integration with CR Router

All commands include metadata for the coditect-router AI command selection tool:

- **trigger_phrases**: Natural language phrases that trigger command recommendations
- **keywords**: Searchable terms for command discovery
- **automation_level**: Indicates if command is fully_automated, semi_automated, or interactive
- **agents_used**: List of specialized agents involved
- **estimated_time**: Duration for command execution

This enables the CR router to provide intelligent command recommendations based on natural language descriptions.

## See Also

- **[docs/SLASH-COMMANDS-REFERENCE.md](../docs/SLASH-COMMANDS-REFERENCE.md)** - Complete command catalog
- **[scripts/coditect-command-router.py](../scripts/coditect-command-router.py)** - AI command selection tool
- **[1-2-3-SLASH-COMMAND-QUICK-START.md](../1-2-3-SLASH-COMMAND-QUICK-START.md)** - Quick start guide

## References

- [Claude Code slash command documentation](https://code.claude.com/docs/commands)
- [CODITECT Framework Documentation](../README.md)
- [Agent Index](../AGENT-INDEX.md) - 50 specialized agents
