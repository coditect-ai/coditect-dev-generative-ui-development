# MEMORY-CONTEXT Directory Guide

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.**
**Part of the AZ1.AI CODITECT Project Management & Development Platform**

---

## 🎯 Overview

The **MEMORY-CONTEXT** directory is a standard component of the AZ1.AI CODITECT framework that provides session continuity, historical context, and knowledge transfer across development cycles.

**Purpose**: Store conversation exports, session summaries, and development history to maintain project knowledge and enable seamless collaboration with AI assistants.

---

## 📂 Standard Directory Structure

Every CODITECT workspace should have this structure:

```
~/PROJECTS/                           # Your workspace root
├── .coditect/                        # CODITECT framework (submodule)
├── .claude -> .coditect              # Symlink for Claude Code
├── MEMORY-CONTEXT/                   # Session history (gitignored)
│   ├── README.md                     # Directory documentation
│   ├── 2025-11-XX-EXPORT-CONTEXT-[TOPIC].txt
│   ├── SESSION-SUMMARY-2025-11-XX.md
│   └── ...                           # Additional context files
│
└── [individual-projects]/            # Your project directories
    ├── my-project/
    │   ├── MEMORY-CONTEXT/           # Project-specific context
    │   ├── src/
    │   ├── docs/
    │   └── ...
    └── another-project/
        ├── MEMORY-CONTEXT/           # Project-specific context
        ├── src/
        └── ...
```

---

## 🎯 Why MEMORY-CONTEXT?

### Problem: Context Loss

**Without MEMORY-CONTEXT**:
- ❌ Lose context between AI assistant sessions
- ❌ Re-explain decisions and rationale repeatedly
- ❌ Forget why certain approaches were taken
- ❌ Team members lack historical knowledge
- ❌ Difficult to resume work after breaks

**With MEMORY-CONTEXT**:
- ✅ Preserve complete conversation history
- ✅ Maintain decision rationale and design discussions
- ✅ Enable seamless session resumption
- ✅ Facilitate team knowledge transfer
- ✅ Create audit trail for project evolution

### Benefits for AI-Assisted Development

**For Claude Code / AI Assistants**:
1. **Session Continuity** - Resume where you left off
2. **Context Awareness** - Understand previous decisions
3. **Consistent Approach** - Maintain architectural patterns
4. **Avoid Rework** - Don't revisit settled discussions

**For Development Teams**:
1. **Knowledge Transfer** - New members understand history
2. **Audit Trail** - Traceable development decisions
3. **Best Practices** - Learn from past successes/failures
4. **Documentation** - Auto-generated development history

---

## 📖 File Types and Naming Conventions

### 1. Session Exports (Conversation History)

**Format**: `YYYY-MM-DD-EXPORT-CONTEXT-[TOPIC].txt`

**Purpose**: Complete conversation export from AI assistant sessions

**When to Create**:
- After major development sessions (>1 hour)
- Before major architectural decisions
- After completing significant milestones
- Before long breaks in development

**Example**:
```
2025-11-15-EXPORT-CONTEXT-AZ1.AI-CODITECT-QUICKSTART.txt
2025-11-20-EXPORT-CONTEXT-AUTHENTICATION-IMPLEMENTATION.txt
2025-12-01-EXPORT-CONTEXT-PERFORMANCE-OPTIMIZATION.txt
```

**How to Create** (Claude Code):
```bash
# In Claude Code, use the /export command
/export 2025-11-XX-EXPORT-CONTEXT-[YOUR-TOPIC].txt

# Move to MEMORY-CONTEXT
mv 2025-11-XX-EXPORT-CONTEXT-[YOUR-TOPIC].txt ~/PROJECTS/MEMORY-CONTEXT/
```

### 2. Session Summaries (Executive Summaries)

**Format**: `SESSION-SUMMARY-YYYY-MM-DD.md`

**Purpose**: Concise summary of session accomplishments

**Contents**:
- **Executive Summary** - High-level overview
- **Accomplishments** - What was delivered
- **Metrics** - Lines of code, docs created, etc.
- **Next Steps** - What's planned next
- **Decisions Made** - Key architectural/technical decisions

**Example**:
```
SESSION-SUMMARY-2025-11-15.md
SESSION-SUMMARY-2025-11-20.md
SESSION-SUMMARY-2025-12-01.md
```

**Template**:
```markdown
# Session Summary - YYYY-MM-DD

## Executive Summary
[High-level overview of session focus and outcomes]

## Accomplishments
- [Major deliverable 1]
- [Major deliverable 2]
- [Major deliverable 3]

## Metrics
- **Session Duration**: X hours
- **Files Created/Modified**: X files
- **Lines of Code/Docs**: X lines
- **Features Completed**: X

## Key Decisions
1. **[Decision Topic]**
   - Context: [Why this decision was needed]
   - Decision: [What was decided]
   - Rationale: [Why this approach]

## Next Steps
- [ ] Immediate (Week 1)
- [ ] Short-term (Month 1)
- [ ] Long-term (Quarter)

**Status**: [Complete/In Progress]
**Next Session**: [Date]
```

### 3. Decision Records (Architecture Decisions)

**Format**: `DECISION-RECORD-YYYY-MM-DD-[TOPIC].md`

**Purpose**: Document significant architectural or technical decisions

**Contents** (ADR format):
- **Context** - Situation and problem
- **Decision** - What was decided
- **Consequences** - Positive and negative outcomes
- **Alternatives Considered** - What else was evaluated

**Example**:
```
DECISION-RECORD-2025-11-15-MULTI-LLM-SYMLINK-ARCHITECTURE.md
DECISION-RECORD-2025-11-20-DATABASE-CHOICE-POSTGRESQL.md
DECISION-RECORD-2025-12-01-AUTHENTICATION-STRATEGY.md
```

### 4. Research Notes

**Format**: `RESEARCH-YYYY-MM-DD-[TOPIC].md`

**Purpose**: Capture research findings, competitive analysis, technology evaluation

**Example**:
```
RESEARCH-2025-11-15-C4-MODEL-BEST-PRACTICES.md
RESEARCH-2025-11-20-LLM-CLI-COMPARISON.md
RESEARCH-2025-12-01-PERFORMANCE-OPTIMIZATION-TECHNIQUES.md
```

---

## 🛠️ Setup Guide

### For New Workspace

```bash
# 1. Create PROJECTS workspace
mkdir -p ~/PROJECTS
cd ~/PROJECTS

# 2. Initialize git
git init
git branch -m main

# 3. Add .coditect framework
git submodule add https://github.com/coditect-ai/coditect-core.git .coditect
ln -s .coditect .claude

# 4. Create MEMORY-CONTEXT directory
mkdir -p MEMORY-CONTEXT
cp .coditect/templates/MEMORY-CONTEXT-README.md MEMORY-CONTEXT/README.md

# 5. Update .gitignore
cat >> .gitignore << 'EOF'
# Claude Code symlink
.claude

# Memory context (local working files)
MEMORY-CONTEXT/

# Individual project directories
*/
!.gitignore
!.gitmodules
!README.md
!SETUP-SUMMARY.md
EOF

# 6. Commit structure
git add .coditect .gitignore
git commit -m "Initialize CODITECT workspace with MEMORY-CONTEXT"
```

### For Individual Projects

```bash
# In your project directory
cd ~/PROJECTS/my-project

# Create project-specific MEMORY-CONTEXT
mkdir -p MEMORY-CONTEXT
cp ../.coditect/templates/MEMORY-CONTEXT-README.md MEMORY-CONTEXT/README.md

# Add to project .gitignore
echo "
# Project memory context (local working files)
MEMORY-CONTEXT/" >> .gitignore
```

---

## 📋 Workflow Integration

### Starting a New Session

**Before beginning work**:
```bash
# 1. Review previous session summary
cd ~/PROJECTS/MEMORY-CONTEXT
cat SESSION-SUMMARY-$(ls SESSION-SUMMARY-*.md | tail -1)

# 2. Review last export if needed
cat $(ls *-EXPORT-CONTEXT-*.txt | tail -1)

# 3. Start Claude Code with context
cd ~/PROJECTS/my-project
# Reference previous context in first message
```

### During Development

**Export at natural checkpoints**:
- After completing a feature
- Before changing approaches
- After important discussions
- Before breaks/end of day

**Create decision records**:
- After architectural decisions
- After technology selections
- After process changes

### Ending a Session

**Wrap-up checklist**:
```bash
# 1. Export conversation
/export 2025-XX-XX-EXPORT-CONTEXT-[TOPIC].txt
mv 2025-XX-XX-EXPORT-CONTEXT-[TOPIC].txt ~/PROJECTS/MEMORY-CONTEXT/

# 2. Create session summary
cd ~/PROJECTS/MEMORY-CONTEXT
# (Create summary using template above)

# 3. Update README.md file index
# (Add new files to table)

# 4. Commit any code changes (but not MEMORY-CONTEXT)
cd ~/PROJECTS
git status  # MEMORY-CONTEXT should be gitignored
```

---

## 🔄 Best Practices

### DO ✅

- **Export regularly** - After every significant session
- **Write summaries** - Concise executive summaries help future you
- **Document decisions** - Capture rationale while fresh
- **Use consistent naming** - Follow naming conventions
- **Index your files** - Maintain README.md with file table
- **Review before starting** - Read previous summary before new session

### DON'T ❌

- **Don't commit to git** - MEMORY-CONTEXT is gitignored (local only)
- **Don't include secrets** - Sanitize any API keys or credentials
- **Don't skip exports** - You'll regret not having context later
- **Don't be too brief** - Better too much detail than too little
- **Don't forget dates** - Always include dates in filenames
- **Don't mix personal/work** - Keep separate MEMORY-CONTEXT per workspace

---

## 🤖 AI Assistant Integration

### For Claude Code

**Starting a session with context**:
```
Hi Claude, I'm continuing work on [PROJECT]. Please review the last
session summary in ~/PROJECTS/MEMORY-CONTEXT/SESSION-SUMMARY-2025-XX-XX.md
to understand what we accomplished and where we left off.

Today's focus: [SPECIFIC GOALS]
```

**Exporting at end of session**:
```
/export 2025-XX-XX-EXPORT-CONTEXT-[TOPIC].txt
```

### For Other LLM CLIs

**Gemini, Copilot, Cursor, etc.**:
- Include relevant context files in first prompt
- Reference decision records for architectural questions
- Summarize previous session in your own words if CLI doesn't support file reading

---

## 📊 File Index Maintenance

**Update MEMORY-CONTEXT/README.md regularly**:

```markdown
## 📊 File Index

| File | Date | Topic | Size | Status |
|------|------|-------|------|--------|
| 2025-11-15-EXPORT-CONTEXT-QUICKSTART.txt | 2025-11-15 | Platform init | 27KB | Complete |
| SESSION-SUMMARY-2025-11-15.md | 2025-11-15 | Session summary | 16KB | Complete |
| 2025-11-20-EXPORT-CONTEXT-AUTH.txt | 2025-11-20 | Authentication | 15KB | Complete |
| SESSION-SUMMARY-2025-11-20.md | 2025-11-20 | Auth session | 8KB | Complete |

**Total**: XX files, XXXKB of context and history
```

---

## 🚀 Advanced Usage

### Multi-Project Knowledge Sharing

**Workspace-level MEMORY-CONTEXT**:
- Stores cross-project patterns and decisions
- Shared learnings and best practices
- Framework updates and changes

**Project-level MEMORY-CONTEXT**:
- Project-specific implementation details
- Feature development history
- Bug investigation and fixes

### Team Collaboration

**Sharing context with team**:
1. Create sanitized summaries (remove any sensitive info)
2. Share via team wiki or documentation
3. Reference decision records in code reviews
4. Use as onboarding material for new team members

### Integration with Documentation

**Convert context to formal docs**:
```bash
# Use session summaries as source for:
- Technical documentation
- Architecture guides
- Development process documentation
- Lessons learned / postmortems
```

---

## 📜 Copyright & License

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**

This MEMORY-CONTEXT Guide is part of the AZ1.AI CODITECT Project Management & Development Platform.

**Developed by**: Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.

**Usage**: Free to use with AZ1.AI CODITECT framework

---

**Built with Excellence by AZ1.AI CODITECT**

*Systematic Development. Continuous Context. Exceptional Results.*

**AZ1.AI INC.**
Founded 2025
Innovation Through Systematic Development
