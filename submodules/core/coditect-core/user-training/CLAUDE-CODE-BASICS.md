# Claude Code Basics for CODITECT Operators

> **Essential Claude Code knowledge for effective CODITECT operation**
> **Master the underlying platform before diving into CODITECT agents**
> **Last Updated:** 2025-11-16

---

## Table of Contents

- [What is Claude Code?](#what-is-claude-code)
- [Installation & Setup](#installation--setup)
- [Core Concepts](#core-concepts)
- [Slash Commands](#slash-commands)
- [File Operations](#file-operations)
- [Git Integration](#git-integration)
- [Session Management](#session-management)
- [Best Practices](#best-practices)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)

---

## What is Claude Code?

**Claude Code** is Anthropic's official command-line interface (CLI) for Claude - a powerful AI coding assistant that helps you write, edit, and understand code.

### Key Features

- **File Operations:** Read, write, edit files with AI assistance
- **Git Integration:** Commit, push, manage repositories
- **Multi-file Context:** Understand entire codebases
- **Code Generation:** Write complete applications
- **Documentation:** Generate comprehensive docs
- **Architecture:** Design system architectures
- **Debugging:** Find and fix issues

### Claude Code vs CODITECT

| Feature | Claude Code | CODITECT |
|---------|-------------|----------|
| **Purpose** | General AI coding assistant | Specialized project specification framework |
| **Agents** | Single general-purpose Claude | 50+ specialized domain agents |
| **Skills** | Built-in tools | 189 reusable skills |
| **Commands** | Basic slash commands | 72+ workflow commands |
| **Focus** | Code writing & editing | Business discovery + technical spec + project management |
| **Best For** | Development & implementation | Planning, specification, architecture |

**Think of it this way:**
- **Claude Code** = The powerful AI engine and CLI platform
- **CODITECT** = The specialized framework built on top of Claude Code for project specification

---

## Installation & Setup

### Prerequisites

```bash
# macOS
brew install claude-code

# Linux
curl -fsSL https://anthropic.com/install.sh | sh

# Windows (WSL2 recommended)
curl -fsSL https://anthropic.com/install.sh | sh
```

### Initial Configuration

```bash
# Authenticate with Anthropic
claude auth login

# Verify installation
claude --version

# Check available models
claude models list
```

### Project Setup

```bash
# Navigate to your project directory
cd ~/PROJECTS/my-project

# Claude Code looks for .claude/ directory for custom configuration
# CODITECT uses .coditect/ with symlink
ln -s .coditect .claude
```

---

## Core Concepts

### 1. Conversation Context

Claude Code maintains **conversation context** - it remembers what you've discussed, files you've read, and decisions you've made during a session.

**Context Window:** 200,000 tokens (~150,000 words)
- Input: Your messages, file reads, tool calls
- Output: Claude's responses, code generation

**When context fills up:**
- Export session summary
- Start new session
- Load context from MEMORY-CONTEXT

### 2. Tool Use

Claude Code has built-in tools:

| Tool | Purpose | Example |
|------|---------|---------|
| **Read** | Read file contents | Read `src/main.rs` |
| **Write** | Create new files | Write new file `api.ts` |
| **Edit** | Modify existing files | Edit function in `utils.js` |
| **Bash** | Run shell commands | Run `npm install` |
| **Grep** | Search file contents | Search for "TODO" |
| **Glob** | Find files by pattern | Find all `*.md` files |
| **WebFetch** | Fetch web content | Fetch docs from URL |
| **WebSearch** | Search the web | Search for "React hooks tutorial" |

### 3. Working Directory

Claude Code operates from your current working directory:

```bash
# Always verify where you are
pwd

# Claude Code will read/write files relative to this location
cd ~/PROJECTS/my-project
claude
```

### 4. File Permissions

Claude Code asks for permission before:
- Writing new files
- Editing existing files
- Running bash commands
- Installing packages

You can configure auto-approval in settings.

---

## Slash Commands

Slash commands are shortcuts that expand into full prompts defined in `.claude/commands/` directory.

### Built-in Slash Commands

**General Commands:**

```bash
/help                 # Show help information
/clear                # Clear conversation history
/reset                # Reset session (lose all context)
/exit                 # Exit Claude Code
/quit                 # Exit Claude Code
```

**File Commands:**

```bash
/read <file>          # Read a file
/edit <file>          # Edit a file
/search <pattern>     # Search for pattern in codebase
```

### CODITECT Custom Slash Commands

CODITECT adds 72 custom slash commands in `.coditect/commands/`:

**Project Setup:**

```bash
/init-project         # Initialize new CODITECT project
/setup-memory         # Set up MEMORY-CONTEXT structure
```

**Business Discovery:**

```bash
/market-research      # Run competitive market analysis
/value-prop           # Generate value proposition
/icp                  # Create ideal customer profile
/pmf                  # Analyze product-market fit
/gtm                  # Generate go-to-market strategy
/pricing              # Create pricing strategy
```

**Technical Specification:**

```bash
/architecture         # Generate system architecture (C4)
/database-schema      # Design database schema
/api-spec             # Create API specification
/adr                  # Create Architecture Decision Record
/tech-stack           # Recommend technology stack
```

**Project Management:**

```bash
/project-plan         # Generate PROJECT-PLAN.md
/tasklist             # Generate TASKLIST.md
/checkpoint           # Create project checkpoint
/status               # Show project status
```

**Orchestration:**

```bash
/orchestrate          # Run multi-agent workflow
/agent-list           # List all available agents
/skill-list           # List all available skills
```

### Creating Custom Slash Commands

Create a new command file in `.coditect/commands/`:

```bash
# Create: .coditect/commands/my-command.md
```

**Command file format:**

```markdown
# My Custom Command

You are tasked with [specific task].

## Instructions

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Output

[Description of what should be generated]

## Example

[Show example output]
```

**Usage:**

```bash
/my-command
# The prompt from my-command.md will expand into the conversation
```

---

## File Operations

### Reading Files

```
"Read the file src/main.rs"
"Show me the contents of README.md"
"What's in the package.json file?"
```

Claude will use the Read tool to display file contents.

**Reading multiple files:**

```
"Read these files:
- src/main.rs
- src/lib.rs
- Cargo.toml"
```

**Reading with line ranges:**

```
"Read lines 50-100 of src/utils.rs"
```

### Writing Files

```
"Create a new file src/api.ts with a basic Express server setup"
"Write a README.md file explaining this project"
```

Claude will generate the content and ask for permission before writing.

**Best practice:** Be specific about:
- File path (absolute or relative)
- File contents
- Code style/conventions
- Dependencies

### Editing Files

```
"Edit src/main.rs and add error handling to the main function"
"Update package.json to add a new dev dependency: typescript"
"Fix the typo in README.md line 42"
```

Claude will:
1. Read the existing file
2. Generate the edit
3. Show you the changes
4. Ask for permission to apply

**Edit strategies:**
- **Small changes:** Claude edits in place
- **Large changes:** Claude may rewrite sections
- **Refactoring:** Claude rewrites entire file

### Searching Files

**Search for text:**

```
"Search for all TODO comments in the codebase"
"Find all instances of 'deprecated' in src/"
"Show me where API_KEY is used"
```

**Search by pattern:**

```
"Find all .ts files that import React"
"Show me all test files"
"Find functions named 'calculate*'"
```

---

## Git Integration

Claude Code has excellent git integration for version control.

### Basic Git Operations

**Check status:**

```
"Show git status"
"What files have changed?"
```

**Stage files:**

```
"Git add all modified files"
"Stage src/main.rs"
```

**Commit changes:**

```
"Commit these changes with message: Add user authentication"
"Create a git commit for the changes we just made"
```

**View history:**

```
"Show recent git commits"
"What was changed in the last commit?"
"Show git log for the past week"
```

**Branching:**

```
"Create a new branch: feature/user-auth"
"Switch to branch main"
"Show all branches"
```

### CODITECT Git Workflow

When working with CODITECT projects:

**1. After completing business discovery:**

```
"Create a git commit for the business discovery work we completed:
- Market research
- Value proposition
- ICP
- Product-market fit analysis
- Competitive analysis
- GTM strategy
- Pricing strategy

Use a descriptive commit message"
```

Claude will:
- Run `git status` to see changes
- Run `git diff` to review changes
- Stage relevant files
- Create a commit with proper formatting
- Include co-author attribution

**2. After technical specification:**

```
"Commit the technical specification work:
- System architecture
- Database schema
- API specification
- ADRs

Include all docs/architecture/ and docs/decisions/ files"
```

**3. Daily commits:**

```
"Commit today's progress on the TASKLIST tasks"
```

### Commit Message Format

Claude Code generates well-formatted commit messages:

```
Add comprehensive business discovery documentation

- Market research with TAM/SAM/SOM analysis
- Value proposition and ICP
- Product-market fit using 7-Fit framework
- Competitive analysis of 5 key players
- Go-to-market strategy (PLG approach)
- Pricing strategy (freemium model)

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Push to Remote

```
"Push to GitHub"
"Push this branch to origin"
```

⚠️ **Important:** Claude Code will never force push without explicit permission.

---

## Session Management

### Understanding Sessions

A **session** = one continuous conversation with Claude Code from start to exit.

**Session lifecycle:**

```
1. Start Claude Code → New session begins
2. Work on project → Context accumulates
3. Token budget approaches limit → Export summary
4. Exit Claude Code → Session ends
5. Start Claude Code again → New session (no memory of previous)
```

### Exporting Session Summaries

Before your session ends (especially when approaching token limit):

```
"Create a session summary of all the work we've done today and export it to MEMORY-CONTEXT/sessions/2025-11-16-business-discovery.md"
```

**Good session summary includes:**

```markdown
# Session Summary: 2025-11-16 Business Discovery

## Work Completed
- Generated market research document
- Created value proposition
- Defined ideal customer profile
- Analyzed product-market fit (7-Fit framework)

## Key Decisions
1. **Target Market:** Small design agencies (5-20 people)
2. **GTM Motion:** Product-led growth (PLG) with freemium
3. **Pricing:** $0 (free) → $49/mo (pro) → $199/mo (agency)

## Files Created
- docs/research/01-market-research.md
- docs/business/01-value-proposition.md
- docs/business/02-ideal-customer-profile.md
- docs/business/03-product-market-fit.md

## Next Steps
1. Complete competitive analysis
2. Finalize GTM strategy document
3. Start technical specification (system architecture)

## Context for Next Session
We're building a SaaS platform for design agencies. Business discovery is 80% complete. Next session should start with competitive analysis and then move to technical architecture.
```

### Continuing Work Across Sessions

**Starting a new session:**

```
"I'm continuing work on the design agency SaaS project. Please read:
- MEMORY-CONTEXT/sessions/2025-11-16-business-discovery.md
- PROJECT-PLAN.md
- TASKLIST.md

Let me know what we were working on and what's next."
```

Claude will:
1. Read the session summary
2. Load context about the project
3. Tell you where you left off
4. Suggest next steps from TASKLIST

### Token Budget Monitoring

Monitor your token usage:

```
"How much of the token budget have we used?"
"Should I export a session summary soon?"
```

**Warning signs:**
- Session feels slow
- Claude mentions approaching limits
- You've read 50+ files
- You've had 100+ message exchanges

**Action:**
```
"Let's create a checkpoint now before we run out of tokens"
```

---

## Best Practices

### 1. Be Specific and Direct

❌ **Vague:**
```
"Make the code better"
"Fix the bug"
"Add a feature"
```

✅ **Specific:**
```
"Refactor the `calculateTotal` function to use reduce instead of a for loop"
"Fix the null pointer exception on line 42 of src/utils.ts"
"Add user authentication using JWT tokens with email/password login"
```

### 2. Provide Context

❌ **No context:**
```
"Create an API"
```

✅ **With context:**
```
"Create a RESTful API for the booking system. It should have endpoints for:
- GET /bookings (list all bookings)
- POST /bookings (create new booking)
- GET /bookings/:id (get single booking)
- PUT /bookings/:id (update booking)
- DELETE /bookings/:id (delete booking)

Use Express.js and TypeScript. Include authentication middleware."
```

### 3. Verify Before Proceeding

```
"Before we implement this, show me the plan"
"Let's review the architecture before writing code"
"Can you explain what this code does?"
```

### 4. Use Incremental Development

Instead of:
```
"Build the entire application"
```

Do:
```
"Let's start with the data models"
→ "Now let's create the API routes"
→ "Now let's add authentication"
→ "Now let's write tests"
```

### 5. Commit Frequently

```
"Let's commit this change before moving to the next feature"
"Create a checkpoint now that we've completed the authentication module"
```

### 6. Leverage MEMORY-CONTEXT

```
"Save this architectural decision to MEMORY-CONTEXT/decisions/ADR-001-database-choice.md"
"Export this research to MEMORY-CONTEXT/technical/jwt-authentication-notes.md"
```

---

## Common Workflows

### Workflow 1: Starting a New Project

```bash
# 1. Create project directory
mkdir ~/PROJECTS/my-new-project
cd ~/PROJECTS/my-new-project

# 2. Start Claude Code
claude

# 3. Initialize CODITECT
"Run the CODITECT initialization script to set up this project"

# 4. Create initial documentation
"Create a README.md explaining this project's purpose"
"Create CLAUDE.md with context about what we're building"

# 5. First commit
"Initialize git and commit the initial project structure"
```

### Workflow 2: Business Discovery Session

```bash
# 1. Start session
"I'm working on business discovery for [project name].
Project: [one-sentence description]
Target customer: [brief description]

Let's start with market research using the competitive-market-analyst agent."

# 2. Generate business documents (using Task tool pattern)
# - Market research
# - Value proposition
# - ICP
# - PMF analysis
# - Competitive analysis
# - GTM strategy
# - Pricing

# 3. Review and refine
"Review the value proposition - is it differentiated enough?"

# 4. Export summary
"Create a session summary for today's business discovery work"

# 5. Commit
"Commit all the business discovery documents with a descriptive message"
```

### Workflow 3: Technical Specification Session

```bash
# 1. Load context
"I'm continuing the [project name] project. Read:
- MEMORY-CONTEXT/sessions/[latest-session].md
- docs/business/01-value-proposition.md
- PROJECT-PLAN.md

We're ready to start technical specification."

# 2. Generate technical documents
"Use the senior-architect agent to create:
1. System architecture with C4 diagrams
2. Database schema
3. API specification

Based on the business requirements we defined earlier."

# 3. Create ADRs
"Create Architecture Decision Records for:
- Database choice
- Authentication method
- Deployment strategy"

# 4. Commit
"Commit the technical specification work"
```

### Workflow 4: Debug and Fix Issues

```bash
# 1. Describe the problem
"I'm getting this error when running npm start:
[paste error message]

Can you help debug?"

# 2. Let Claude investigate
Claude will:
- Read relevant files
- Search for related code
- Identify the issue
- Propose a fix

# 3. Review the fix
"Show me exactly what you're going to change before applying the fix"

# 4. Apply and test
"Apply the fix"
"Run npm start to verify it works"

# 5. Commit
"Commit this bug fix"
```

### Workflow 5: Code Review

```bash
# 1. Request review
"Review the code in src/auth/ directory for:
- Security issues
- Best practices
- Performance concerns
- Missing error handling"

# 2. Address findings
"Fix the security issue you found in src/auth/jwt.ts"

# 3. Commit improvements
"Commit the security improvements from code review"
```

---

## Troubleshooting

### Issue: Claude Can't Find Files

**Problem:**
```
"I can't find the file you're referring to"
```

**Solutions:**

1. **Check working directory:**
```bash
pwd
# Make sure you're in the right directory
cd ~/PROJECTS/my-project
```

2. **Use absolute paths:**
```
"Read /Users/halcasteel/PROJECTS/my-project/src/main.rs"
```

3. **List files first:**
```
"Show me all .rs files in the src/ directory"
```

### Issue: Edits Not Working

**Problem:**
```
"I couldn't apply that edit - the old content doesn't match"
```

**Solutions:**

1. **Read the file first:**
```
"Read src/main.rs"
# Then make edits
```

2. **Use Write instead of Edit for large changes:**
```
"Write a new version of src/main.rs with these changes..."
```

3. **Specify exact line numbers:**
```
"Replace lines 42-45 in src/main.rs with [new code]"
```

### Issue: Git Commits Failing

**Problem:**
```
"Git commit failed - please configure user.name and user.email"
```

**Solution:**
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

**Problem:**
```
"No changes to commit"
```

**Solution:**
```
"Show git status"
# Verify there are actually changes
# If yes: "Stage all files and commit"
```

### Issue: Running Out of Tokens

**Problem:**
```
"We're approaching the token limit"
```

**Solutions:**

1. **Export summary immediately:**
```
"Create a session summary right now and export to MEMORY-CONTEXT/sessions/"
```

2. **Commit work:**
```
"Commit all our work with a descriptive message"
```

3. **Start new session:**
```bash
exit
claude
"I'm continuing [project]. Read MEMORY-CONTEXT/sessions/[latest].md"
```

### Issue: Agent Invocation Not Working

**Problem:**
```
"I don't see an agent by that name"
```

**Solution:**

Check you're using the Task Tool Pattern:

❌ **Wrong:**
```
/competitive-market-analyst
```

✅ **Correct:**
```
"Use the Task tool with:
- subagent_type: general-purpose
- prompt: Use competitive-market-analyst subagent to..."
```

### Issue: Slow Performance

**Possible causes:**

1. **Large file reads:**
   - Solution: Read specific sections instead of entire files

2. **Too much context:**
   - Solution: Export summary, start new session

3. **Complex requests:**
   - Solution: Break into smaller steps

**Best practice:**
```
"Let's break this into smaller tasks:
1. First, [step 1]
2. Then, [step 2]
3. Finally, [step 3]"
```

---

## Quick Reference

### Essential Commands

```bash
# Start Claude Code
claude

# Exit Claude Code
exit
# or Ctrl+D

# Clear conversation (keep context)
/clear

# Reset session (lose all context)
/reset
```

### Common Prompts

```bash
# Reading
"Read [file-path]"
"Show me [file-path]"
"What's in [file-path]?"

# Writing
"Create [file-path] with [description]"
"Write a new file [file-path]"

# Editing
"Edit [file-path] to [change]"
"Update [file-path] and [change]"

# Searching
"Search for [pattern]"
"Find all [pattern] in [directory]"
"Where is [function/class] defined?"

# Git
"Git status"
"Commit with message: [message]"
"Push to origin"

# Session Management
"Create a session summary"
"Export summary to MEMORY-CONTEXT/"
"How much token budget have we used?"
```

### CODITECT Integration

```bash
# Agent invocation (always use this pattern!)
Task(
    subagent_type="general-purpose",
    prompt="Use [agent-name] subagent to [detailed task]"
)

# Common agents
- competitive-market-analyst
- business-intelligence-analyst
- senior-architect
- software-design-architect
- rust-expert-developer
- frontend-react-typescript-expert
```

---

## Next Steps

Now that you understand Claude Code basics, you're ready to:

1. **Complete Foundation Training:** [CODITECT-OPERATOR-TRAINING-SYSTEM.md](./CODITECT-OPERATOR-TRAINING-SYSTEM.md)
2. **Learn Task Tool Pattern:** Module 1, Lesson 1.3
3. **Start Your First Project:** Use [1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md](./1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md)
4. **Master CODITECT Agents:** Review [../agents/](../agents/) directory
5. **Practice with Sample Project:** Follow the training exercises

---

## Additional Resources

**Official Claude Code Documentation:**
- https://code.claude.com/docs

**CODITECT Training Materials:**
- `1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md` - 30-minute rapid start
- `1-2-3-CODITECT-ONBOARDING-GUIDE.md` - Comprehensive guide
- `CODITECT-OPERATOR-TRAINING-SYSTEM.md` - 4-6 hour training program
- `CODITECT-OPERATOR-ASSESSMENTS.md` - Quizzes and certification
- `CODITECT-OPERATOR-FAQ.md` - Frequently asked questions

**Framework Documentation:**
- `../CLAUDE.md` - CODITECT framework overview
- `../README.md` - Repository structure
- `../agents/` - All agent descriptions
- `../commands/` - All slash commands
- `../skills/` - All reusable skills

---

**Document Version:** 1.0
**Last Updated:** 2025-11-16
**Maintainer:** CODITECT Training Team
