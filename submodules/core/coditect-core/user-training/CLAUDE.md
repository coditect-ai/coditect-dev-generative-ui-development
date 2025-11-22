# Claude Context: CODITECT User Training Program

> **Context file for AI assistants working on CODITECT training materials**
> **Last Updated:** 2025-11-16

---

## Purpose of This Directory

The `user-training/` directory contains the complete CODITECT Operator Training Program - a comprehensive system designed to transform complete beginners into certified, independent CODITECT Operators in 4-6 hours of hands-on training.

**Goal:** Enable users to become self-taught experts capable of:
- Specifying complete software projects from idea through production
- Orchestrating 50+ specialized AI agents
- Generating comprehensive business discovery and technical specification documentation
- Managing complex multi-phase projects independently

---

## Training Philosophy

### Core Principles

**1. Fast Path to Capability**
- 30-minute quick start for immediate productivity
- 4-6 hour comprehensive training for full certification
- Hands-on, learn-by-doing approach
- No programming knowledge required for business discovery

**2. Self-Contained Learning**
- All materials designed for independent study
- No external instructor required
- Progressive disclosure of complexity
- Multiple learning paths for different experience levels

**3. Practical Application**
- Every lesson includes hands-on exercises
- Sample projects with real-world scenarios
- Assessments verify actual capability, not memorization
- Final practical exam creates complete project specification

**4. Zero Ambiguity**
- Exact Task Tool Pattern documented
- Step-by-step instructions with screenshots/examples
- Troubleshooting guides for common issues
- Glossary defines all terminology

---

## Training Materials Overview

### Core Training Documents

**1. [README.md](./README.md) - Training Program Index**
- Entry point for all learners
- Explains learning paths (quick/comprehensive/reference)
- Lists all training resources
- Provides recommended learning sequences

**2. [1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md](./1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md)**
- Ultra-fast 30-minute onboarding
- Gets users productive immediately
- Covers: setup, initialization, agent invocation, first document
- For experienced developers who want to start NOW

**3. [CODITECT-OPERATOR-TRAINING-SYSTEM.md](./CODITECT-OPERATOR-TRAINING-SYSTEM.md)**
- Comprehensive 4-6 hour training program
- 5 modules with hands-on exercises
- Sample project: Design Agency SaaS
- Certification path from Foundation → Expert Operator

**4. [1-2-3-CODITECT-ONBOARDING-GUIDE.md](./1-2-3-CODITECT-ONBOARDING-GUIDE.md)**
- Exhaustive reference guide
- Complete CODITECT philosophy and methodology
- All 49 agents explained with examples
- Advanced topics: multi-repo, custom agents, enterprise-scale

**5. [CLAUDE-CODE-BASICS.md](./CLAUDE-CODE-BASICS.md)**
- Claude Code platform fundamentals
- Slash commands reference
- File operations, git integration, session management
- For users new to Claude Code

**5b. [1-2-3-SLASH-COMMAND-QUICK-START.md](../1-2-3-SLASH-COMMAND-QUICK-START.md)** (NEW! - Essential)
- Master all 72 slash commands in 3 simple steps
- **🤖 AI Command Router** (`coditect-router`) - Never memorize commands, just describe what you want
- Decision trees for command selection
- Agent invocation with /suggest-agent and /agent-dispatcher
- Common scenario workflows (features, bugs, research, optimization)
- Quick reference card for immediate productivity
- Perfect companion to all training paths

### Assessment & Tracking

**6. [CODITECT-OPERATOR-ASSESSMENTS.md](./CODITECT-OPERATOR-ASSESSMENTS.md)**
- Quizzes for each of the 5 training modules
- Final certification practical exam (90 minutes)
- Answer keys and grading rubrics
- Certification levels: Foundation → Business → Technical → Project → Expert

**7. [CODITECT-OPERATOR-PROGRESS-TRACKER.md](./CODITECT-OPERATOR-PROGRESS-TRACKER.md)**
- Self-guided progress tracking worksheet
- Checkboxes for every lesson, quiz, exercise
- Skills inventory and confidence ratings
- Project portfolio tracker
- Reflection and goal-setting sections

### Support Resources

**8. [CODITECT-OPERATOR-FAQ.md](./CODITECT-OPERATOR-FAQ.md)**
- 100+ frequently asked questions
- Organized by topic: Environment, Agents, Business, Technical, etc.
- Quick reference tables
- Real-world examples

**9. [CODITECT-TROUBLESHOOTING-GUIDE.md](./CODITECT-TROUBLESHOOTING-GUIDE.md)**
- Solutions to common problems
- Step-by-step diagnostic procedures
- Recovery procedures for various failures
- Prevention best practices

**10. [CODITECT-GLOSSARY.md](./CODITECT-GLOSSARY.md)**
- 100+ terms, concepts, and acronyms defined
- Organized by category
- Examples for each definition
- Cross-references to related concepts

---

## Target Audience

### Primary Audiences

**1. Non-technical Founders (40%)**
- Want to specify their SaaS/startup before hiring developers
- Need comprehensive business and technical specs
- No coding knowledge
- Focus: Business discovery, value proposition, market research

**2. Technical Consultants (30%)**
- Deliver project specifications to clients
- Need to reduce spec time while increasing quality
- Experienced in software but new to AI agents
- Focus: Complete specification workflow

**3. Product Managers (20%)**
- Create detailed requirements and architecture
- Work with development teams
- Some technical background
- Focus: Technical specification, project management

**4. Development Teams (10%)**
- Standardize project planning and documentation
- Use AI agents to accelerate specification phase
- Experienced developers
- Focus: Technical architecture, ADRs, advanced orchestration

### Experience Levels

**Beginners (50%)**
- No CODITECT experience
- May be new to Claude Code
- Need step-by-step guidance
- Path: Quick Start → Full Training → Practice Projects

**Intermediate (30%)**
- Familiar with AI tools, new to CODITECT
- Comfortable with command line
- Can skip basics, focus on CODITECT-specific patterns
- Path: Quick Start → Module 2-5 of Training → Certification

**Advanced (20%)**
- Experienced developers
- Want to adopt CODITECT methodology
- Need only CODITECT-specific knowledge
- Path: Quick Start → Skim Training → Practical Exam

---

## Training Modules Breakdown

### Module 1: Foundation (60 minutes)
**Objective:** Environment setup, framework understanding, Task Tool Pattern mastery

**Key Learnings:**
- Initialize CODITECT project
- Understand 49 agents, 189 skills, 72 commands
- Master the ONLY working agent invocation pattern
- Successfully invoke first agent

**Critical Success Factor:** Task Tool Pattern must be memorized and executed perfectly

---

### Module 2: Business Discovery (90 minutes)
**Objective:** Generate complete business specification package

**Key Learnings:**
- Market research with TAM/SAM/SOM calculations
- Value proposition and ICP creation
- Product-market fit (7-Fit framework)
- Competitive analysis
- Go-to-market strategy (PLG/SLG/MLG/Partner-Led)
- Pricing strategy

**Deliverables:** 9 business documents in docs/business/ and docs/research/

---

### Module 3: Technical Specification (90 minutes)
**Objective:** Generate production-ready technical architecture

**Key Learnings:**
- C4 architecture diagrams (Context, Container, Component, Code)
- Database schema design (ERD, tables, relationships)
- API specification (OpenAPI 3.1)
- Architecture Decision Records (ADRs)
- Software Design Document (SDD)
- Test Design Document (TDD)

**Deliverables:** Complete technical specification package

---

### Module 4: Project Management (60 minutes)
**Objective:** Master project planning and task management

**Key Learnings:**
- Generate PROJECT-PLAN.md with phases, timeline, risks
- Create TASKLIST.md with checkboxes, priorities, estimates
- Checkpoint creation
- Project lifecycle management

**Deliverables:** PROJECT-PLAN.md, TASKLIST.md, first checkpoint

---

### Module 5: Advanced Operations (30-60 minutes)
**Objective:** Handle session continuity and multi-session projects

**Key Learnings:**
- Session management and catastrophic forgetting prevention
- MEMORY-CONTEXT system (sessions/, decisions/, business/, technical/)
- Token budget management (200K token limit)
- Work reuse strategies
- Multi-session project continuity

**Critical Success Factor:** Never lose context between sessions

---

## Sample Project: Design Agency SaaS

**Used throughout training for consistency**

**Premise:**
- All-in-one platform for freelance photographers
- Target: Small design agencies (5-20 people)
- Features: Project management, client galleries, invoicing, time tracking
- Market: Small creative agencies frustrated with fragmented tools
- Business model: Freemium → Pro ($49/mo) → Agency ($199/mo)

**Why This Project:**
- Realistic and relatable
- Clear target customer
- Well-defined problem
- Allows demonstration of all CODITECT capabilities
- Representative of typical SaaS project

**Students also encouraged to:**
- Use their own project ideas
- Apply training to real problems
- Build portfolio of CODITECT specifications

---

## Task Tool Pattern (Critical)

**This is THE most important concept in all training materials.**

### The ONLY Working Method

```python
Task(
    subagent_type="general-purpose",
    prompt="Use [agent-name] subagent to [detailed task description with requirements and expected outputs]"
)
```

### Critical Components

1. **subagent_type** is ALWAYS "general-purpose" (never the agent name)
2. **prompt** MUST start with "Use [agent-name] subagent to"
3. Detailed task description with:
   - Project context
   - Specific requirements
   - Expected deliverables
   - Output file path

### Common Mistakes to Avoid

❌ **WRONG:**
```python
Task(subagent_type="competitive-market-analyst", prompt="Research market")
```

❌ **WRONG:**
```python
/competitive-market-analyst
```

❌ **WRONG:**
```python
"competitive-market-analyst: research the market"
```

✅ **CORRECT:**
```python
Task(
    subagent_type="general-purpose",
    prompt="Use competitive-market-analyst subagent to research the AI IDE market including TAM/SAM/SOM, competitor analysis (5-7 companies), market trends, and growth opportunities. Output to docs/research/01-market-research.md"
)
```

---

## Certification Levels

### Level 1: Foundation Operator
- Passed Module 1 Assessment (80%+)
- Can set up environment and invoke agents

### Level 2: Business Operator
- Passed Modules 1-2 Assessments
- Can generate complete business specifications

### Level 3: Technical Operator
- Passed Modules 1-3 Assessments
- Can create technical architecture and design documents

### Level 4: Project Operator
- Passed Modules 1-4 Assessments
- Can manage complete project lifecycle

### Level 5: Expert Operator
- Passed all 5 Module Assessments + Final Practical Exam (80%+)
- Can work independently on complex projects
- Qualified to train other operators

---

## Quality Standards for Training Materials

### Clarity
- Every instruction must be unambiguous
- Screenshots/examples for visual learners
- Step-by-step numbered procedures
- No assumptions about prior knowledge

### Completeness
- Every concept fully explained
- All edge cases covered
- Troubleshooting for common issues
- No "TODO" or placeholder content

### Consistency
- Terminology used uniformly across all documents
- Same sample project throughout
- Consistent formatting (headings, code blocks, tables)
- Cross-references between documents

### Practicality
- Every lesson includes hands-on exercise
- Real-world examples, not toy problems
- Assessments test actual capability
- Immediate applicability to user's work

---

## Maintenance and Updates

### When to Update Training Materials

**Critical Updates (Immediate):**
- Framework changes (agent names, invocation patterns)
- Errors or inaccuracies discovered
- Security issues or vulnerabilities
- Broken links or missing resources

**Important Updates (Within 1 week):**
- New agents, skills, or commands added
- User feedback on confusing sections
- Additional examples requested
- FAQ entries for common questions

**Enhancement Updates (Ongoing):**
- Additional sample projects
- More advanced topics
- Video tutorials (future)
- Community contributions

### Update Process

1. Identify what needs updating
2. Update affected documents
3. Verify consistency across all materials
4. Test exercises and code examples
5. Update "Last Updated" dates
6. Commit with clear message
7. Notify users of significant changes

---

## Key Success Metrics

### Training Effectiveness

**Target Metrics:**
- 90%+ completion rate for Quick Start (30 min)
- 80%+ completion rate for Full Training (4-6 hrs)
- 70%+ pass rate on Final Practical Exam
- 85%+ user satisfaction rating

**Actual Metrics (Pilot):**
- TBD - currently in pilot phase

### User Capability

**After Quick Start:**
- Can initialize projects
- Can invoke agents correctly
- Can generate first business document

**After Full Training:**
- Can independently create complete project specifications
- Can orchestrate multi-agent workflows
- Can manage session continuity
- Ready for real client/professional work

**After Certification:**
- Expert Operators can train others
- Can handle enterprise-scale projects
- Can customize agents and workflows
- Can contribute to CODITECT framework

---

## Common Training Issues & Solutions

### Issue: Task Tool Pattern Confusion
**Solution:** Emphasize repeatedly, provide template, show mistakes and corrections

### Issue: Vague Prompts Leading to Generic Output
**Solution:** Teach prompt engineering, show before/after examples, require specific context

### Issue: Session Context Lost
**Solution:** Train on MEMORY-CONTEXT early, make session summaries a habit

### Issue: Information Overload
**Solution:** Progressive disclosure, quick start path, focus on hands-on practice

### Issue: Not Completing Assessments
**Solution:** Explain importance, make engaging, provide immediate feedback

---

## Future Enhancements

### Planned Additions

**Short-term (Next 3 months):**
- Video walkthrough of sample project
- Interactive quiz platform
- Community forum for operators
- Case study library

**Medium-term (6 months):**
- Advanced orchestration patterns
- Custom agent development course
- Enterprise deployment guide
- Team collaboration workflows

**Long-term (12 months):**
- Certification program with badges
- Operator community marketplace
- Advanced specialization tracks
- Train-the-trainer program

---

## For AI Assistants Working on Training Materials

### When Creating New Content

1. **Read existing materials first** to maintain consistency
2. **Use Design Agency SaaS** as the sample project
3. **Follow the Task Tool Pattern** exactly as documented
4. **Include hands-on exercises** for every concept
5. **Provide troubleshooting** for common issues
6. **Define all terms** in Glossary
7. **Cross-reference** related documents
8. **Test all code examples** and commands
9. **Update progress tracker** if adding lessons
10. **Add to FAQ** if answering common questions

### When Updating Existing Content

1. **Maintain existing structure** unless improving it
2. **Preserve user's progress** if updating tracker
3. **Update "Last Updated" date**
4. **Check cross-references** are still valid
5. **Verify consistency** across all affected documents
6. **Test updated examples** thoroughly

### Voice and Tone

- **Professional but approachable** - not overly technical
- **Encouraging and supportive** - building confidence
- **Clear and direct** - no ambiguity
- **Action-oriented** - tell users what to do, not just what is
- **Realistic about challenges** - don't sugarcoat difficulties
- **Celebrate progress** - acknowledge achievements

---

## Essential Tools for Training Delivery

### 🤖 AI Command Router (`cr` alias)

**Purpose:** Eliminate command memorization burden for trainees by providing natural language command selection.

**Location:** `.coditect/scripts/coditect-command-router.py`

**Key Training Points:**
1. **Setup is part of onboarding** - Shell aliases configured in first 2 minutes
2. **Primary usage pattern** - `cr "plain English request"` → get command suggestion
3. **Interactive mode** - `cri` for multi-question workflows
4. **AI vs Heuristic modes** - Works with or without Anthropic API key
5. **Integration point** - Taught in Module 1 (Foundation) and reinforced throughout

**For AI Assistants:**
- When users ask "which command should I use?", remind them about `cr` tool
- If users struggle with command selection, suggest: `cr "describe your goal"`
- Reference this in troubleshooting: "Confused about commands? Use the cr alias!"

**Shell Setup (teach users to add to ~/.zshrc or ~/.bashrc):**
```bash
# CODITECT AI Command Router
alias cr='python3 ~/.coditect/scripts/coditect-router'
alias cri='python3 ~/.coditect/scripts/coditect-router -i'
```

**Example Training Dialogue:**
```
Student: "I want to add user authentication but don't know which command to use"
AI Assistant: "Great question! This is exactly what the cr alias is for. Try running:

cr 'I need to add user authentication'

This will analyze your request and suggest the optimal slash command."
```

---

### 📍 Checkpoint Automation System

**Purpose:** Zero catastrophic forgetting between sessions through automated context capture and GitHub backup.

**Location:** `.coditect/scripts/create-checkpoint.py`

**Critical Training Concept:** Checkpoints are taught in Module 4 (Project Management) but should be created starting from Module 1.

**Key Training Points:**

1. **When to Checkpoint:**
   - End of every training module (Module 1 done → checkpoint)
   - After completing significant work (business discovery → checkpoint)
   - Before switching contexts (documentation → coding → checkpoint)
   - End of every training session (even if incomplete)

2. **The One Command Pattern:**
   ```bash
   python3 .coditect/scripts/create-checkpoint.py "Sprint description" --auto-push
   ```

3. **What It Does (7-Step Process):**
   - ✅ Captures git status, recent commits, submodule states
   - ✅ Extracts completed tasks from all TASKLISTs
   - ✅ Generates checkpoint document in `MEMORY-CONTEXT/checkpoints/`
   - ✅ Updates README.md with checkpoint reference
   - ✅ Creates session export in `MEMORY-CONTEXT/sessions/` for next session
   - ✅ Commits all changes locally
   - ✅ **Pushes to GitHub remote** (submodule + parent repo with --auto-push)

4. **Checkpoint Flags:**
   - `--auto-push` (recommended) - Commits AND pushes to remote
   - `--auto-commit` (legacy) - Commits but doesn't push
   - No flags - Manual review before commit

5. **Training Schedule:**
   - Module 1 complete → First checkpoint
   - Module 2 complete → Checkpoint (Business Discovery Complete)
   - Module 3 complete → Checkpoint (Technical Architecture Complete)
   - Module 4 complete → Checkpoint (PROJECT-PLAN and TASKLIST Created)
   - Module 5 complete → Checkpoint (Training Complete - Certification Ready)

**For AI Assistants:**

When working with trainees:
1. **Remind about checkpoints** after every significant accomplishment
2. **Model the behavior** - "Let's create a checkpoint now that we've finished X"
3. **Explain the why** - "This ensures if your session ends unexpectedly, we can resume exactly where we left off"
4. **Use specific descriptions** - Not "checkpoint", but "Business Discovery Phase 1 Complete"

**Example Training Dialogue:**
```
AI Assistant: "Great work completing your first market research document!
Before we move on, let's create a checkpoint to save your progress:

python3 .coditect/scripts/create-checkpoint.py 'Module 2 Market Research Complete' --auto-push

This will:
1. Capture your completed work
2. Update your README with progress
3. Backup everything to GitHub
4. Create a session export so we can resume seamlessly next time"
```

**Integration with MEMORY-CONTEXT System:**

Checkpoints are the PRIMARY mechanism for session continuity:
- **Before session ends:** Create checkpoint with --auto-push
- **Next session starts:** AI reads most recent checkpoint from `MEMORY-CONTEXT/checkpoints/`
- **Context loaded:** Session export in `MEMORY-CONTEXT/sessions/` provides complete context
- **Zero forgetting:** All decisions, completions, and next steps preserved

**Common Training Issues:**

1. **Students forget to checkpoint** → Build it into module completion rituals
2. **Vague checkpoint descriptions** → Teach: "What you accomplished" not "checkpoint"
3. **Manual commit workflow** → Emphasize --auto-push for automatic GitHub backup
4. **Not reading checkpoints at session start** → First step of every session: read last checkpoint

**Assessment Integration:**

In Module 4 Assessment, students must demonstrate:
- [ ] Create a properly-named checkpoint
- [ ] Use --auto-push flag correctly
- [ ] Verify checkpoint appears in README.md
- [ ] Locate checkpoint document in MEMORY-CONTEXT/checkpoints/
- [ ] Explain when to create checkpoints (5 scenarios)

---

## Document Metadata

**Directory:** user-training/
**Total Documents:** 10 core documents + this CLAUDE.md
**Total Content:** ~240,000 words
**Training Time:** 4-6 hours (comprehensive), 30 minutes (quick start)
**Certification Exam:** 90 minutes
**Target Audience:** Non-technical founders, consultants, PMs, developers
**Version:** 1.0 (Pilot)
**Last Updated:** 2025-11-16
**Maintainer:** CODITECT Training Team
**Status:** Pilot Phase - gathering feedback

---

## Quick Reference for This Directory

```
user-training/
├── README.md                              # Start here - Training index
├── CLAUDE.md                              # This file - Context for AI
│
├── Core Training (Pick your path)
│   ├── 1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md       # 30-min quick start
│   ├── CODITECT-OPERATOR-TRAINING-SYSTEM.md        # 4-6 hr comprehensive
│   ├── 1-2-3-CODITECT-ONBOARDING-GUIDE.md          # Exhaustive reference
│   └── CLAUDE-CODE-BASICS.md                        # Platform fundamentals
│
├── Assessment & Tracking
│   ├── CODITECT-OPERATOR-ASSESSMENTS.md             # Quizzes & exam
│   └── CODITECT-OPERATOR-PROGRESS-TRACKER.md        # Progress tracking
│
└── Support Resources
    ├── CODITECT-OPERATOR-FAQ.md                     # FAQs
    ├── CODITECT-TROUBLESHOOTING-GUIDE.md            # Problem solving
    └── CODITECT-GLOSSARY.md                         # Terminology
```

---

**This training program represents the culmination of extensive work to create the fastest possible path from complete beginner to capable, certified CODITECT Operator.**

**Goal: Enable anyone to become a self-taught expert in 4-6 hours.**

**Status: Mission accomplished. Training materials complete and ready for pilot users.**
