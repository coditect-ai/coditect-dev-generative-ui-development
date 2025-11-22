# CODITECT Operator Certification Assessments

> **Purpose:** Verify operator competency at each training stage
> **Format:** Self-graded assessments with answer keys
> **Passing Score:** 80% or higher to advance
> **Time Allocation:** 10-15 minutes per module assessment

---

## Table of Contents

- [Module 1: Foundation Assessment](#module-1-foundation-assessment)
- [Module 2: Business Discovery Assessment](#module-2-business-discovery-assessment)
- [Module 3: Technical Specification Assessment](#module-3-technical-specification-assessment)
- [Module 4: Project Management Assessment](#module-4-project-management-assessment)
- [Module 5: Advanced Operations Assessment](#module-5-advanced-operations-assessment)
- [Final Certification Practical Exam](#final-certification-practical-exam)
- [Answer Keys](#answer-keys)

---

## Module 1: Foundation Assessment

**Total Points:** 20 (Pass: 16/20)
**Time Limit:** 10 minutes

### Section A: Environment Setup (5 points)

**Q1.1** (1 point) What command initializes a new CODITECT project?

```bash
A) ./scripts/coditect-project-init.sh
B) git clone coditect
C) npm install coditect
D) coditect init
```

**Q1.2** (2 points) What are the THREE required directory structures in every CODITECT project? (Select 3)

```
A) .coditect/
B) node_modules/
C) MEMORY-CONTEXT/
D) docs/
E) build/
F) .cache/
```

**Q1.3** (2 points) Why is `.claude` a symlink to `.coditect`?

```
A) To save disk space
B) Claude Code requires `.claude` directory by convention
C) For backward compatibility
D) It's not a symlink, it's a copy
```

### Section B: Framework Understanding (5 points)

**Q1.4** (2 points) How many specialized agents are in the CODITECT framework?

```
A) 25
B) 35
C) 50
D) 72
```

**Q1.5** (3 points) Match each agent domain to its correct count:

```
Research & Analysis:     ___ agents
Development:             ___ agents
Infrastructure:          ___ agents
Orchestration:           ___ agents

Options: 2, 8, 13, 27
```

### Section C: Task Tool Pattern (10 points)

**Q1.6** (3 points) What is the ONLY verified method to invoke CODITECT agents?

```python
A) agent.invoke("competitive-market-analyst")
B) /competitive-market-analyst
C) Task(subagent_type="general-purpose", prompt="Use competitive-market-analyst...")
D) run_agent("competitive-market-analyst")
```

**Q1.7** (4 points) Fix this BROKEN agent invocation:

```python
# BROKEN CODE:
Task(
    subagent_type="competitive-market-analyst",
    prompt="Research AI IDE market"
)
```

**Your corrected code:**
```python
# Write your corrected version here:






```

**Q1.8** (3 points) What are the THREE components every Task tool call must include?

```
1. _______________________
2. _______________________
3. _______________________
```

---

## Module 2: Business Discovery Assessment

**Total Points:** 25 (Pass: 20/25)
**Time Limit:** 15 minutes

### Section A: Market Research (8 points)

**Q2.1** (3 points) What does TAM/SAM/SOM stand for, and arrange them from largest to smallest:

```
TAM = Total ________________ Market
SAM = ________________ ________________ Market
SOM = ________________ ________________ Market

Order (largest to smallest): ___ → ___ → ___
```

**Q2.2** (2 points) Which agent is best suited for competitive market analysis?

```
A) business-intelligence-analyst
B) competitive-market-analyst
C) senior-architect
D) orchestrator
```

**Q2.3** (3 points) List THREE key outputs from market research:

```
1. _______________________
2. _______________________
3. _______________________
```

### Section B: Product-Market Fit (9 points)

**Q2.4** (4 points) The 7-Fit PMF Framework includes which dimensions? (Select all that apply)

```
□ Problem-Solution Fit
□ Product-Market Fit
□ Technology-Stack Fit
□ Product-Channel Fit
□ Channel-Model Fit
□ Pricing-Market Fit
□ Model-Market Fit
□ Team-Execution Fit
```

**Q2.5** (3 points) What is a Value Proposition? Write a one-sentence definition:

```
_________________________________________________________________
_________________________________________________________________
```

**Q2.6** (2 points) True/False: An Ideal Customer Profile (ICP) only needs demographic data.

```
□ True
□ False

If False, what else is needed? _________________________________
```

### Section C: Go-to-Market Strategy (8 points)

**Q2.7** (4 points) Match each GTM motion to its description:

```
___ PLG (Product-Led Growth)
___ SLG (Sales-Led Growth)
___ MLG (Marketing-Led Growth)
___ Partner-Led Growth

A) Enterprise deals, long sales cycles, relationship-driven
B) Free trial/freemium, viral growth, self-serve
C) Content marketing, SEO, demand generation
D) Channel partners, integrations, co-selling
```

**Q2.8** (4 points) You're launching a SaaS tool for solo developers. Which GTM motion is most appropriate and why?

```
GTM Motion: _________________

Reasoning (2-3 sentences):
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Module 3: Technical Specification Assessment

**Total Points:** 25 (Pass: 20/25)
**Time Limit:** 15 minutes

### Section A: C4 Architecture (8 points)

**Q3.1** (4 points) The C4 model has four levels. Place them in order from highest to lowest abstraction:

```
___ Code
___ Component
___ Container
___ Context

Correct order: ___ → ___ → ___ → ___
```

**Q3.2** (4 points) Match each C4 level to what it shows:

```
___ Context
___ Container
___ Component
___ Code

A) Classes, interfaces, functions
B) System landscape, users, external systems
C) Modules, services, responsibilities within a container
D) Applications, databases, microservices
```

### Section B: Database Design (7 points)

**Q3.3** (3 points) What are THREE key outputs from database schema design?

```
1. _______________________
2. _______________________
3. _______________________
```

**Q3.4** (4 points) You have a multi-tenant SaaS app. List TWO key design decisions you must make for the database schema:

```
1. _________________________________________________________________

2. _________________________________________________________________
```

### Section C: ADRs and Documentation (10 points)

**Q3.5** (3 points) What does ADR stand for?

```
A________________ D________________ R________________
```

**Q3.6** (4 points) An ADR must include which sections? (Select all that apply)

```
□ Title
□ Status (Proposed, Accepted, Deprecated, Superseded)
□ Context
□ Budget
□ Decision
□ Consequences
□ Team Members
□ Timeline
```

**Q3.7** (3 points) When should you create an ADR? (Select best answer)

```
A) Only for major architectural decisions
B) For any decision that impacts system design or technology choices
C) Only when required by management
D) At the end of the project for documentation
```

---

## Module 4: Project Management Assessment

**Total Points:** 20 (Pass: 16/20)
**Time Limit:** 12 minutes

### Section A: PROJECT-PLAN.md (10 points)

**Q4.1** (5 points) A PROJECT-PLAN.md must include which sections? (Select 5 minimum)

```
□ Project Overview
□ Team Bios
□ Objectives & Success Criteria
□ Marketing Budget
□ Technical Architecture
□ Development Phases
□ Timeline & Milestones
□ Risk Assessment
□ HR Policies
□ Resource Requirements
```

**Q4.2** (3 points) What is the purpose of dividing work into Phases and Sprints?

```
_________________________________________________________________
_________________________________________________________________
```

**Q4.3** (2 points) True/False: PROJECT-PLAN.md should be updated only at the start of the project.

```
□ True
□ False

Explanation: ______________________________________________________
```

### Section B: TASKLIST.md (10 points)

**Q4.4** (4 points) Write a properly formatted TASKLIST entry with checkbox, phase, priority, and estimate:

```markdown
Your task entry here:




```

**Q4.5** (3 points) What are the THREE priority levels used in TASKLIST.md?

```
1. _______________________
2. _______________________
3. _______________________
```

**Q4.6** (3 points) How often should TASKLIST.md be updated during active development?

```
A) Weekly
B) Daily or after significant progress
C) Only at sprint boundaries
D) When all tasks are complete
```

---

## Module 5: Advanced Operations Assessment

**Total Points:** 25 (Pass: 20/25)
**Time Limit:** 15 minutes

### Section A: Session Management (8 points)

**Q5.1** (3 points) What is "catastrophic forgetting" in AI context?

```
_________________________________________________________________
_________________________________________________________________
```

**Q5.2** (5 points) The MEMORY-CONTEXT system has four subdirectories. Name them and their purpose:

```
1. ________________/ - Purpose: _______________________________
2. ________________/ - Purpose: _______________________________
3. ________________/ - Purpose: _______________________________
4. ________________/ - Purpose: _______________________________
```

### Section B: Work Reuse (7 points)

**Q5.3** (4 points) What is the primary benefit of the work reuse system?

```
A) Saves disk space
B) Avoids re-reading files and re-doing research across sessions
C) Makes git commits faster
D) Reduces code complexity
```

**Q5.4** (3 points) When should you export a session summary to MEMORY-CONTEXT? (Select all that apply)

```
□ End of each work session
□ After major research or architectural decisions
□ Before context window fills up
□ Only at project completion
□ When switching between different project phases
```

### Section C: Token Budget Management (10 points)

**Q5.5** (3 points) What is the typical token budget for a Claude Code session?

```
A) 50,000 tokens
B) 100,000 tokens
C) 200,000 tokens
D) Unlimited
```

**Q5.6** (4 points) You have 180,000 tokens used out of 200,000. What should you do? (Select best two actions)

```
□ Continue working, plenty of tokens left
□ Export session summary to MEMORY-CONTEXT
□ Start a new session
□ Delete previous messages
□ Ignore it, Claude will manage automatically
□ Create checkpoint and prepare for session continuation
```

**Q5.7** (3 points) Why is it important to create checkpoints during long projects?

```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Final Certification Practical Exam

**Total Points:** 100 (Pass: 80/100)
**Time Limit:** 90 minutes
**Format:** Hands-on project execution

### Scenario

You are a newly certified CODITECT Operator. A client has approached you with this request:

**"I want to build a SaaS platform for freelance photographers to manage client bookings, deliver photo galleries, and handle invoicing. I'm not technical, so I need complete specification before hiring developers."**

### Your Mission

Using CODITECT agents and processes, create a complete project specification package.

### Deliverables Checklist

**Part 1: Environment Setup (10 points)**

```
□ Initialize project: coditect-project-init.sh
□ Create project directory: photography-saas-platform
□ Verify .coditect/ framework loaded
□ Verify MEMORY-CONTEXT/ created
□ Create initial README.md with project description
```

**Part 2: Business Discovery (30 points)**

Using appropriate agents, generate:

```
□ Market Research (docs/research/01-market-research.md)
  - TAM/SAM/SOM for photography SaaS market
  - 5 competitors identified
  - Market trends analysis

□ Value Proposition (docs/business/01-value-proposition.md)
  - Clear problem statement
  - Solution description
  - Unique differentiators

□ Ideal Customer Profile (docs/business/02-ideal-customer-profile.md)
  - Demographics: Freelance photographers, revenue range
  - Psychographics: Pain points, goals
  - Behavioral: Current tool usage

□ Product-Market Fit Analysis (docs/business/03-product-market-fit.md)
  - 7-Fit framework applied
  - Validation of market need

□ Go-to-Market Strategy (docs/business/05-go-to-market-strategy.md)
  - Recommended GTM motion
  - Customer acquisition strategy
  - Pricing model recommendation
```

**Part 3: Technical Specification (35 points)**

Using appropriate agents, generate:

```
□ System Architecture (docs/architecture/01-system-architecture.md)
  - C4 Context diagram (mermaid)
  - C4 Container diagram (mermaid)
  - Technology stack recommendations

□ Database Schema (docs/architecture/02-database-schema.md)
  - Entity Relationship Diagram
  - Tables: users, clients, bookings, galleries, photos, invoices
  - Relationships and constraints

□ API Specification (docs/architecture/03-api-specification.md)
  - RESTful API design
  - Key endpoints (minimum 10)
  - Authentication approach

□ Software Design Document (docs/architecture/04-software-design-document.md)
  - Feature breakdown
  - Module design
  - Security considerations

□ Architecture Decision Records (docs/decisions/)
  - ADR-001: Database choice
  - ADR-002: Authentication method
  - ADR-003: File storage approach
```

**Part 4: Project Management (15 points)**

```
□ PROJECT-PLAN.md with:
  - Executive summary
  - Objectives & success criteria
  - 4 development phases defined
  - Timeline (12-week estimate)
  - Risk assessment
  - Resource requirements

□ TASKLIST.md with:
  - Minimum 25 tasks across phases
  - Proper checkbox formatting
  - Priority assignments
  - Time estimates
  - Phase associations
```

**Part 5: Session Management (10 points)**

```
□ Created session summary in MEMORY-CONTEXT/sessions/
□ Exported key decisions to MEMORY-CONTEXT/decisions/
□ Checkpoint created with ISO datetime
□ All work committed to git
□ Repository ready for handoff
```

### Evaluation Criteria

**Grading Rubric:**

| Category | Points | Criteria |
|----------|--------|----------|
| **Completeness** | 30 | All required documents created |
| **Quality** | 25 | Documents are detailed, actionable, professional |
| **Agent Usage** | 20 | Correct agent invocations, proper Task tool pattern |
| **Process Adherence** | 15 | Following CODITECT methodology |
| **Documentation** | 10 | Clear, well-organized, ready for developers |

**Certification Levels:**

- **90-100 points:** Expert Operator - Ready for complex multi-agent projects
- **80-89 points:** Advanced Operator - Ready for most projects with occasional reference
- **70-79 points:** Intermediate Operator - Needs more practice, review modules
- **Below 70:** Foundation Operator - Review training materials, retry exam

---

## Answer Keys

### Module 1 Answer Key

**Q1.1:** A) ./scripts/coditect-project-init.sh

**Q1.2:** A) .coditect/, C) MEMORY-CONTEXT/, D) docs/

**Q1.3:** B) Claude Code requires `.claude` directory by convention

**Q1.4:** C) 50

**Q1.5:**
- Research & Analysis: 13 agents
- Development: 8 agents
- Infrastructure: 8 agents
- Orchestration: 2 agents

**Q1.6:** C) Task(subagent_type="general-purpose", prompt="Use competitive-market-analyst...")

**Q1.7:** Corrected code:
```python
Task(
    subagent_type="general-purpose",
    prompt="Use competitive-market-analyst subagent to research AI IDE market including market size, trends, key players, and growth opportunities"
)
```

**Q1.8:**
1. subagent_type (always "general-purpose")
2. prompt (must specify which agent to use)
3. detailed task description

---

### Module 2 Answer Key

**Q2.1:**
- TAM = Total Addressable Market
- SAM = Serviceable Available Market
- SOM = Serviceable Obtainable Market
- Order: TAM → SAM → SOM

**Q2.2:** B) competitive-market-analyst

**Q2.3:** Any three of:
1. Market size (TAM/SAM/SOM)
2. Competitive landscape
3. Customer segments and pain points
4. Market trends
5. Growth opportunities
6. Barriers to entry

**Q2.4:** All except "Technology-Stack Fit" and "Pricing-Market Fit":
- ☑ Problem-Solution Fit
- ☑ Product-Market Fit
- ☑ Product-Channel Fit
- ☑ Channel-Model Fit
- ☑ Model-Market Fit

**Q2.5:** Sample answer: "A clear statement of the unique value and benefits your product delivers to customers that differentiates it from alternatives."

**Q2.6:** False. ICP needs Demographics, Psychographics, and Behavioral data.

**Q2.7:**
- PLG = B (Free trial/freemium, viral growth, self-serve)
- SLG = A (Enterprise deals, long sales cycles, relationship-driven)
- MLG = C (Content marketing, SEO, demand generation)
- Partner-Led = D (Channel partners, integrations, co-selling)

**Q2.8:**
- GTM Motion: PLG (Product-Led Growth)
- Reasoning: Solo developers prefer self-serve, low-friction adoption. Free trial or freemium model allows them to evaluate the tool independently without sales calls. Low price point enables quick purchasing decisions.

---

### Module 3 Answer Key

**Q3.1:**
- Correct order: Context → Container → Component → Code

**Q3.2:**
- Context = B (System landscape, users, external systems)
- Container = D (Applications, databases, microservices)
- Component = C (Modules, services, responsibilities within a container)
- Code = A (Classes, interfaces, functions)

**Q3.3:** Any three of:
1. Entity Relationship Diagram
2. Table definitions with columns and types
3. Relationships and foreign keys
4. Indexes and constraints
5. Data migration strategy

**Q3.4:** Sample answers:
1. Multi-tenancy strategy: Shared schema with tenant_id, separate schemas per tenant, or separate databases per tenant
2. Data isolation and security approach to prevent cross-tenant data leakage

**Q3.5:** Architecture Decision Record

**Q3.6:**
- ☑ Title
- ☑ Status (Proposed, Accepted, Deprecated, Superseded)
- ☑ Context
- ☑ Decision
- ☑ Consequences

**Q3.7:** B) For any decision that impacts system design or technology choices

---

### Module 4 Answer Key

**Q4.1:** Required sections (select 5):
- ☑ Project Overview
- ☑ Objectives & Success Criteria
- ☑ Technical Architecture
- ☑ Development Phases
- ☑ Timeline & Milestones
- ☑ Risk Assessment
- ☑ Resource Requirements

**Q4.2:** Sample answer: "Phases and sprints break complex projects into manageable chunks, enable progress tracking, facilitate team coordination, and provide natural checkpoints for review and adjustment."

**Q4.3:** False. PROJECT-PLAN.md is a living document that should be updated as the project evolves, risks change, and new information emerges.

**Q4.4:** Sample properly formatted entry:
```markdown
- [ ] **[Phase 1]** Implement user authentication system - `Priority: HIGH` - `Est: 8h`
```

**Q4.5:**
1. HIGH (or P0)
2. MEDIUM (or P1)
3. LOW (or P2)

**Q4.6:** B) Daily or after significant progress

---

### Module 5 Answer Key

**Q5.1:** Sample answer: "Catastrophic forgetting occurs when AI loses context from previous conversations or sessions, resulting in loss of important project knowledge, decisions, and context."

**Q5.2:**
1. sessions/ - Purpose: Session exports and summaries
2. decisions/ - Purpose: Architecture Decision Records (ADRs)
3. business/ - Purpose: Business research, market analysis, product specs
4. technical/ - Purpose: Technical research, code patterns, implementation notes

**Q5.3:** B) Avoids re-reading files and re-doing research across sessions

**Q5.4:**
- ☑ End of each work session
- ☑ After major research or architectural decisions
- ☑ Before context window fills up
- ☑ When switching between different project phases

**Q5.5:** C) 200,000 tokens

**Q5.6:** Best two actions:
- ☑ Export session summary to MEMORY-CONTEXT
- ☑ Create checkpoint and prepare for session continuation

**Q5.7:** Sample answer: "Checkpoints preserve project state, capture decisions and progress, enable session continuity, and provide recovery points if issues arise. They ensure no work is lost and context can be restored in new sessions."

---

## Certification Process

### How to Use These Assessments

1. **Self-Paced Learning:** Complete each module's training, then take the corresponding assessment
2. **Open Book:** You may reference training materials during assessments
3. **Self-Graded:** Use answer keys to grade yourself honestly
4. **Mastery Required:** Must achieve 80% or higher to advance
5. **Retry Policy:** If you score below 80%, review the module and retake assessment

### Certification Levels

**Level 1: Foundation Operator**
- Passed Module 1 Assessment
- Can set up CODITECT environment
- Understands Task Tool Pattern
- Ready to begin business discovery work

**Level 2: Business Operator**
- Passed Modules 1-2 Assessments
- Can generate complete business specifications
- Understands market research and PMF
- Ready for technical specification work

**Level 3: Technical Operator**
- Passed Modules 1-3 Assessments
- Can generate technical architecture
- Creates ADRs and design documents
- Ready for full project management

**Level 4: Project Operator**
- Passed Modules 1-4 Assessments
- Manages complete project lifecycle
- Creates and maintains PROJECT-PLAN and TASKLIST
- Ready for advanced multi-agent work

**Level 5: Expert Operator**
- Passed all 5 Module Assessments
- Passed Final Practical Exam (80%+)
- Can independently execute complex projects
- Qualified to train other operators

### Certification Badge

Upon completing all assessments and the final practical exam, you earn:

```
╔════════════════════════════════════════╗
║   CODITECT CERTIFIED OPERATOR          ║
║                                        ║
║   Level: [Expert/Advanced/Intermediate]║
║   Date: [YYYY-MM-DD]                   ║
║   Score: [XX/100]                      ║
║                                        ║
║   Authorized to independently execute  ║
║   multi-agent AI development projects  ║
║   using CODITECT methodology           ║
╚════════════════════════════════════════╝
```

---

## Assessment Tips

### For Trainers

- Review answer keys before assigning assessments
- Provide feedback on practical exam deliverables
- Adjust passing scores based on organizational needs
- Use assessments to identify knowledge gaps

### For Learners

- Take assessments seriously - they verify real competency
- Don't rush - understanding is more important than speed
- Review incorrect answers thoroughly
- Practice hands-on before final practical exam
- Use the training materials as reference
- Ask questions if concepts are unclear

### Quality Standards

These assessments ensure CODITECT Operators can:

✅ Set up projects independently
✅ Invoke agents correctly every time
✅ Generate professional business specifications
✅ Create production-ready technical designs
✅ Manage complex multi-phase projects
✅ Handle session continuity and context management
✅ Work autonomously without constant guidance

**Remember:** The goal is not to memorize answers, but to become a capable, independent CODITECT Operator who can confidently execute real-world projects.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-16
**Maintainer:** CODITECT Training Team
