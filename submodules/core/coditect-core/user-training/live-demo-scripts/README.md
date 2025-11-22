# CODITECT Live Demo Scripts

> **Experience CODITECT in action - Watch a complete project specification being built**
> **Step-by-step orchestrated scripts that teach by demonstration**
> **Run these scripts to generate sample templates and learn the workflow**

**Author:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
**Framework:** CODITECT
**Copyright:** © 2025 AZ1.AI INC. All rights reserved.

---

## What Are These Scripts?

These are **orchestrated demonstration scripts** that:

✅ **Show you exactly how** CODITECT operators work
✅ **Generate all sample templates** for the PixelFlow project
✅ **Explain every step** with commentary and narration
✅ **Teach by doing** - watch real agent invocations
✅ **Verify your environment** before you start
✅ **Guide you sequentially** through the complete workflow

Think of them as **watching an expert operator over their shoulder** as they create a complete project specification.

---

## Scripts Overview

### 0️⃣ `00-setup-check.py`
**Purpose:** Verify your environment is ready
**Runtime:** 2 minutes
**What it does:**
- Checks Claude Code installation
- Verifies git configuration
- Tests Python version
- Confirms directory structure
- Creates project workspace

**Run this FIRST before anything else!**

---

### 1️⃣ `01-master-orchestrator.py`
**Purpose:** Main control script that runs everything
**Runtime:** 30-45 minutes (full demo)
**What it does:**
- Orchestrates all phases in sequence
- Provides real-time narration
- Shows Task Tool Pattern in action
- Generates complete sample project
- Creates all business and technical templates

**This is your "one command to see it all" script!**

---

### 2️⃣ `02-phase1-business-discovery.py`
**Purpose:** Business discovery phase demonstration
**Runtime:** 10-15 minutes
**What it does:**
- Invokes competitive-market-analyst
- Generates market research with TAM/SAM/SOM
- Creates value proposition and ICP
- Develops product-market fit analysis
- Produces competitive analysis
- Designs GTM strategy and pricing

**Generates:** 7 business documents in `sample-project-templates/business/`

---

### 3️⃣ `03-phase2-technical-spec.py`
**Purpose:** Technical specification phase demonstration
**Runtime:** 15-20 minutes
**What it does:**
- Invokes senior-architect for system design
- Creates C4 architecture diagrams
- Generates database schema with ERD
- Produces API specification (OpenAPI 3.1)
- Writes Architecture Decision Records (ADRs)
- Creates Software Design Document

**Generates:** 7 technical documents in `sample-project-templates/technical/`

---

### 4️⃣ `04-phase3-project-management.py`
**Purpose:** Project management phase demonstration
**Runtime:** 5-10 minutes
**What it does:**
- Invokes orchestrator for project planning
- Generates PROJECT-PLAN with 4 phases
- Creates TASKLIST with 50+ tasks
- Produces README and CLAUDE.md
- Creates first checkpoint

**Generates:** 4 project management documents in `sample-project-templates/project-management/`

---

### 5️⃣ `05-session-management-demo.py`
**Purpose:** Demonstrate session continuity
**Runtime:** 5 minutes
**What it does:**
- Shows how to export session summaries
- Demonstrates MEMORY-CONTEXT usage
- Simulates multi-session workflow
- Teaches work reuse strategies

**Educational only - teaches session management**

---

## How to Use These Scripts

### Quick Start (Recommended Path)

```bash
# Step 1: Navigate to live-demo-scripts directory
cd .coditect/user-training/live-demo-scripts/

# Step 2: Check environment (REQUIRED FIRST)
python3 00-setup-check.py

# Step 3: Run master orchestrator (generates everything)
python3 01-master-orchestrator.py

# Sit back and watch! The script will:
# - Explain each step
# - Show agent invocations
# - Generate all templates
# - Create complete sample project
#
# Total time: 30-45 minutes
```

---

### Step-by-Step Path (Learn Each Phase)

```bash
# Step 1: Environment check
python3 00-setup-check.py

# Step 2: Business discovery only
python3 02-phase1-business-discovery.py
# Review generated business documents
# Study the agent invocation patterns

# Step 3: Technical specification only
python3 03-phase2-technical-spec.py
# Review generated technical docs
# Study C4 diagrams and ADRs

# Step 4: Project management only
python3 04-phase3-project-management.py
# Review PROJECT-PLAN and TASKLIST
# See how everything ties together

# Step 5: Session management demo
python3 05-session-management-demo.py
# Learn session continuity techniques
```

---

### Custom Path (Pick What You Need)

```bash
# Just want to see business discovery?
python3 02-phase1-business-discovery.py

# Just want technical specs?
python3 03-phase2-technical-spec.py

# Just want to understand session management?
python3 05-session-management-demo.py
```

---

## What You'll See During Execution

### Real-Time Narration

Each script provides **color-coded narration**:

```
🎯 PHASE STARTING: Business Discovery
═══════════════════════════════════════

📋 Step 1: Market Research
────────────────────────────────────

💭 EXPLANATION:
   We're about to invoke the competitive-market-analyst agent
   to research the design agency SaaS market.

   This agent will:
   • Calculate TAM/SAM/SOM (Total/Serviceable/Obtainable Market)
   • Identify 5-7 key competitors
   • Analyze market trends
   • Validate customer pain points

🤖 INVOKING AGENT: competitive-market-analyst
═══════════════════════════════════════════════

Task(
    subagent_type="general-purpose",
    prompt="Use competitive-market-analyst subagent to research..."
)

⏳ Working... (this may take 2-3 minutes)

✅ COMPLETE: Market research generated
   Output: sample-project-templates/business/01-market-research.md

📊 QUALITY CHECK:
   ✓ TAM/SAM/SOM calculations present
   ✓ 7 competitors identified and analyzed
   ✓ Market trends documented with sources
   ✓ Professional formatting

────────────────────────────────────
```

---

### Task Tool Pattern Demonstrations

You'll see **exactly how to invoke agents** with real examples:

```python
# Business Discovery
Task(
    subagent_type="general-purpose",
    prompt="Use competitive-market-analyst subagent to conduct comprehensive market research for PixelFlow - an all-in-one SaaS platform for design agencies.

Target Customer: Small creative agencies (5-20 people)
Problem: Agencies frustrated with using 10+ fragmented tools
Solution: Unified platform for project management, time tracking, invoicing, client galleries

Research Requirements:
1. Market Sizing
   - TAM: Total addressable market (all design agencies globally)
   - SAM: Serviceable market (agencies 5-20 people, English-speaking)
   - SOM: Obtainable market (realistic Year 1-3 capture)

2. Competitive Landscape
   - Identify 7 key competitors (Asana, Monday, ClickUp, Agency Analytics, etc.)
   - Feature comparison matrix
   - Pricing comparison
   - Strengths/weaknesses analysis
   - Market positioning

3. Market Trends
   - Remote work impact on agency operations
   - Consolidation trend (all-in-one vs fragmented tools)
   - Agency technology adoption patterns

4. Customer Validation
   - Pain points with current solutions
   - Willingness to pay estimates
   - Feature priorities from customer perspective

Output: sample-project-templates/business/01-market-research.md

Format as professional market research document with:
- Executive summary
- Detailed TAM/SAM/SOM calculations (show your math!)
- Competitor profiles (not just list - actual analysis)
- Market trend analysis with data/sources
- Customer insights and validation
- Recommendations and market opportunities"
)
```

---

### Progress Tracking

Scripts show **real-time progress**:

```
CODITECT Live Demo Progress
═══════════════════════════

Phase 1: Business Discovery
├─ ✅ Market Research (3 mins)
├─ ✅ Value Proposition (2 mins)
├─ ✅ Ideal Customer Profile (2 mins)
├─ ✅ Product-Market Fit (3 mins)
├─ ⏳ Competitive Analysis (in progress...)
├─ ⏸️  Go-to-Market Strategy (pending)
└─ ⏸️  Pricing Strategy (pending)

Time Elapsed: 10 minutes
Estimated Remaining: 5 minutes
```

---

## Generated Outputs

### After Running Master Orchestrator

```
sample-project-templates/
├── business/
│   ├── 01-market-research.md
│   ├── 02-value-proposition.md
│   ├── 03-ideal-customer-profile.md
│   ├── 04-product-market-fit.md
│   ├── 05-competitive-analysis.md
│   ├── 06-go-to-market-strategy.md
│   └── 07-pricing-strategy.md
│
├── technical/
│   ├── 01-system-architecture.md
│   ├── 02-database-schema.md
│   ├── 03-api-specification.md
│   ├── 04-software-design-document.md
│   ├── ADR-001-database-choice.md
│   ├── ADR-002-authentication-method.md
│   └── ADR-003-deployment-strategy.md
│
└── project-management/
    ├── PROJECT-PLAN.md
    ├── TASKLIST-with-checkpoints.md
    ├── README.md
    └── CLAUDE.md
```

**Total:** 18 production-quality documents ready for reference

---

## Educational Features

### 1. Step-by-Step Explanations

Before each action, scripts explain:
- **What** is about to happen
- **Why** we're doing it this way
- **Which agent** will be used
- **What to expect** in the output

### 2. Commentary on Decisions

Scripts provide context:
- Why this agent vs another agent?
- Why these prompt details matter?
- How does this fit into larger workflow?
- What quality standards to check?

### 3. Best Practices Highlighted

Scripts demonstrate:
- ✅ Correct Task Tool Pattern usage
- ✅ Detailed, specific prompts
- ✅ Output quality verification
- ✅ Session management techniques
- ✅ Git workflow integration

### 4. Common Mistakes Avoided

Scripts show what NOT to do:
- ❌ Vague prompts
- ❌ Wrong agent invocation
- ❌ Missing output file paths
- ❌ Skipping quality checks

---

## Requirements

### Software

- **Python 3.7+** (check: `python3 --version`)
- **Claude Code** (check: `claude --version`)
- **Git** (check: `git --version`)

### Disk Space

- ~50 MB for generated templates
- ~10 MB for script outputs

### Time

- **Full demo:** 30-45 minutes
- **Single phase:** 5-20 minutes
- **Setup check:** 2 minutes

### Network

- Internet connection required (agents fetch research data)
- GitHub access for commits (optional)

---

## Troubleshooting

### "Claude Code not found"

```bash
# Install Claude Code first
# Visit: https://claude.com/code

# Or use setup check script to guide you:
python3 00-setup-check.py
```

### "Permission denied"

```bash
# Make scripts executable
chmod +x *.py
```

### "Script hangs or times out"

- Some agent invocations take 3-5 minutes
- Be patient - scripts show progress
- If stuck >10 minutes, Ctrl+C and restart

### "Output quality seems low"

- Scripts use detailed prompts
- If output is generic, Claude Code might be overloaded
- Try running at off-peak hours
- Check your Claude Code version (update if old)

---

## Learning Tips

### First Time Users

1. **Run 00-setup-check.py** - Don't skip this!
2. **Run 01-master-orchestrator.py** - See the full workflow
3. **Review generated templates** - Study the quality
4. **Re-run individual phases** - Focus on what interests you
5. **Try your own project** - Apply what you learned

### Visual Learners

- Scripts include ASCII art and formatting
- Color-coded output (explanations, actions, results)
- Progress bars and status indicators
- Before/after comparisons

### Hands-On Learners

- Modify script prompts and re-run
- Experiment with different project scenarios
- Compare template quality variations
- Try generating for your own project idea

---

## Advanced Usage

### Customize for Your Project

Edit scripts to generate templates for YOUR project:

```python
# In any phase script, modify PROJECT_INFO:

PROJECT_INFO = {
    "name": "Your Project Name",
    "description": "Your project description",
    "target_customer": "Your target customer",
    "problem": "Problem you're solving",
    "solution": "Your solution",
    # ... etc
}
```

Then run the script - templates generated for your project!

### Integration with Training

**Before Module 2:** Run `02-phase1-business-discovery.py`
→ See what business documents should look like

**Before Module 3:** Run `03-phase2-technical-spec.py`
→ See what technical specs should look like

**Before Module 4:** Run `04-phase3-project-management.py`
→ See what project plans should look like

**Throughout training:** Reference generated templates as quality benchmarks

---

## What Makes These Scripts Special?

### Not Just Documentation Generators

These scripts are **teaching tools** that:

✅ **Demonstrate best practices** - Show don't tell
✅ **Explain the "why"** - Not just the "how"
✅ **Build mental models** - Help you understand the system
✅ **Provide templates** - Give you quality benchmarks
✅ **Save time** - Generate hours of work in minutes

### Interactive Learning Experience

- **Real-time feedback** - See results immediately
- **Guided exploration** - Learn at your own pace
- **Hands-on practice** - Modify and experiment
- **Quality benchmarks** - Know what "good" looks like

---

## FAQ

**Q: Do I need to run all scripts?**
A: No. Run `00-setup-check.py` first, then pick what interests you. `01-master-orchestrator.py` runs everything.

**Q: Can I run scripts multiple times?**
A: Yes! Scripts overwrite previous outputs, so re-run anytime.

**Q: Will this use my Claude Code credits/tokens?**
A: Yes, scripts invoke real agents. Full demo uses ~50K-100K tokens (~$1-2 worth).

**Q: Can I pause and resume?**
A: Run individual phase scripts (02, 03, 04) separately. Master orchestrator runs continuously.

**Q: What if I don't have Claude Code?**
A: Run `00-setup-check.py` - it will guide you through installation.

**Q: Are these scripts maintained?**
A: Yes, scripts evolve with CODITECT framework. Check repo for updates.

---

## Next Steps

**Ready to start?**

```bash
# 1. Check your environment
python3 00-setup-check.py

# 2. Run the full demo
python3 01-master-orchestrator.py

# 3. Study the generated templates
ls -R sample-project-templates/

# 4. Start your own project
# Use these templates as quality benchmarks!
```

**Questions?** See main FAQ: `../CODITECT-OPERATOR-FAQ.md`

---

**Author:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
**Framework:** CODITECT
**Copyright:** © 2025 AZ1.AI INC. All rights reserved.
**Version:** 1.0
**Last Updated:** 2025-11-16

🚀 **Let the live demonstration begin!**
