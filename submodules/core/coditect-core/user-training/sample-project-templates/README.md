# Sample Project Templates - Design Agency SaaS

> **Complete example outputs for the training sample project**
> **Study these BEFORE creating your own project specifications**
> **See what "good" looks like**

---

## Purpose

These templates show the **expected quality and format** for all CODITECT deliverables. Study them to understand:

✅ What level of detail is required
✅ How to structure each document
✅ What makes a professional specification
✅ How business and technical docs connect

**Do NOT copy blindly** - Use these as reference for your own projects!

---

## Sample Project: Design Agency SaaS Platform

**Project Name:** PixelFlow
**Tagline:** All-in-one platform for design agencies
**Target Customer:** Small creative agencies (5-20 people)
**Problem:** Agencies use 10+ fragmented tools (project management, time tracking, invoicing, client galleries)
**Solution:** Unified platform specifically built for design agency workflows
**Business Model:** Freemium → Pro ($49/mo) → Agency ($199/mo)

---

## Directory Structure

```
sample-project-templates/
├── README.md (this file)
│
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
    └── README.md
    └── CLAUDE.md
```

---

## How to Use These Templates

### During Training

**Module 2 (Business Discovery):**

1. **Before generating documents:** Read corresponding template
2. **Understand the structure:** Note sections, level of detail
3. **Generate your version:** Use agent to create document
4. **Compare with template:** Is your output similar quality?
5. **Refine if needed:** Improve prompts to match template quality

**Example workflow:**
```
Step 1: Read business/01-market-research.md (template)
Step 2: Invoke competitive-market-analyst agent
Step 3: Review generated output
Step 4: Compare with template - is TAM/SAM/SOM as detailed?
Step 5: If not, refine prompt and regenerate
```

---

**Module 3 (Technical Specification):**

Same process:
1. Read template first
2. Note C4 diagram structure, table formats, level of detail
3. Generate your version
4. Compare and refine

---

**Module 4 (Project Management):**

Study:
- How PROJECT-PLAN phases are structured
- How TASKLIST tasks are formatted with checkboxes
- Checkpoint format and content

---

### After Training (For Your Own Projects)

**Use templates as:**

✅ **Quality benchmark** - "Is my output this detailed?"
✅ **Structure reference** - "What sections should I include?"
✅ **Format guide** - "How should I format tables/diagrams?"
✅ **Completeness check** - "Did I miss anything?"

❌ **Do NOT:**
- Copy/paste content (templates are for PixelFlow, not your project)
- Skip understanding why structure works
- Ignore context - adapt to your project needs

---

## Template Quality Standards

Each template demonstrates:

### Business Documents

**Market Research:**
- ✅ Specific TAM/SAM/SOM calculations (show your math!)
- ✅ 5-7 competitor profiles (not just names, actual analysis)
- ✅ Market trends with data/sources
- ✅ Customer pain points validated
- ✅ Willingness to pay estimates

**Value Proposition:**
- ✅ Clear problem statement (specific, not generic)
- ✅ Solution description (how it works)
- ✅ Differentiation (vs alternatives)
- ✅ Target benefits (quantified if possible)

**Ideal Customer Profile:**
- ✅ Demographics (company size, revenue, role, geography)
- ✅ Psychographics (pain points, goals, values)
- ✅ Behavioral (current tools, budget, triggers)

**Product-Market Fit:**
- ✅ All 7 fits analyzed (not skipped!)
- ✅ Evidence for each fit
- ✅ Gaps identified
- ✅ Action plan to achieve fit

**Competitive Analysis:**
- ✅ Feature comparison matrix
- ✅ Pricing comparison
- ✅ Strengths/weaknesses
- ✅ Market positioning

**Go-to-Market Strategy:**
- ✅ GTM motion selected with rationale
- ✅ Customer acquisition strategy
- ✅ Channel plan
- ✅ Success metrics

**Pricing Strategy:**
- ✅ Pricing model justified
- ✅ Tier structure
- ✅ Competitive benchmarking
- ✅ Value-based pricing rationale

---

### Technical Documents

**System Architecture:**
- ✅ C4 Context diagram (mermaid, renders correctly)
- ✅ C4 Container diagram (shows tech stack)
- ✅ Technology choices justified
- ✅ System boundaries clear
- ✅ Security considerations

**Database Schema:**
- ✅ Entity Relationship Diagram (mermaid)
- ✅ All tables with columns, types, constraints
- ✅ Relationships and foreign keys
- ✅ Indexes for performance
- ✅ Multi-tenancy approach (if applicable)

**API Specification:**
- ✅ All CRUD endpoints
- ✅ OpenAPI 3.1 format (or well-structured markdown)
- ✅ Request/response schemas
- ✅ Authentication approach
- ✅ Error responses
- ✅ 10+ endpoints minimum

**Architecture Decision Records:**
- ✅ Title clearly states decision
- ✅ Status (Proposed/Accepted)
- ✅ Context explains why decision needed
- ✅ Decision states what was chosen
- ✅ Consequences (positive, negative, neutral)

**Software Design Document:**
- ✅ Feature breakdown
- ✅ Module architecture
- ✅ Key algorithms/logic
- ✅ Security design
- ✅ Performance considerations
- ✅ Error handling approach

---

### Project Management Documents

**PROJECT-PLAN.md:**
- ✅ Executive summary
- ✅ Clear objectives with success criteria
- ✅ 4 development phases with deliverables
- ✅ Timeline with milestones
- ✅ Risk assessment with mitigations
- ✅ Resource requirements
- ✅ Living document (update as project evolves)

**TASKLIST-with-checkpoints.md:**
- ✅ Tasks organized by phase
- ✅ Proper checkbox format: `- [ ] **[Phase X]** Task - Priority: HIGH - Est: Xh`
- ✅ Realistic time estimates
- ✅ Priority assignments (HIGH/MEDIUM/LOW)
- ✅ 50+ tasks for complete project
- ✅ Agent assignments (which agent to use)
- ✅ Checkpoints after each phase

---

## Using Templates for Self-Assessment

### Quality Checklist

After generating a document, ask yourself:

**Business Documents:**
- [ ] Is it as detailed as the template?
- [ ] Did I show calculations (not just state numbers)?
- [ ] Did I provide evidence/sources?
- [ ] Is it specific to my project (not generic)?
- [ ] Could a developer/investor understand my vision from this?

**Technical Documents:**
- [ ] Are diagrams complete and rendering correctly?
- [ ] Did I document ALL key decisions (not just some)?
- [ ] Is schema normalized and complete?
- [ ] Are all endpoints documented?
- [ ] Could a developer start coding from this spec?

**Project Management:**
- [ ] Are phases logical and achievable?
- [ ] Are tasks granular enough (not too large)?
- [ ] Did I identify risks realistically?
- [ ] Is timeline realistic?
- [ ] Can I track progress daily with this TASKLIST?

---

## Common Gaps (What Learners Often Miss)

### Business Discovery

❌ **Too generic:** "Target market is small businesses"
✅ **Specific:** "Design agencies with 5-20 employees, $500K-$2M annual revenue, using 8-12 different tools"

❌ **No calculations:** "TAM is large"
✅ **Show math:** "TAM = 50,000 agencies × $2,400/year = $120M"

❌ **Competitor list only:** "Competitors: Asana, Monday, ClickUp"
✅ **Analysis:** Feature comparison, pricing, why we're different

---

### Technical Specification

❌ **Vague architecture:** "We'll use microservices"
✅ **Specific:** C4 Container diagram showing exact services, databases, message queues

❌ **Incomplete schema:** List of table names
✅ **Complete:** ERD + all columns with types, relationships, indexes

❌ **No ADRs:** Decisions made but not documented
✅ **ADRs:** Why PostgreSQL over MongoDB, why JWT auth, why Kubernetes

---

### Project Management

❌ **Too high-level:** "Build frontend"
✅ **Granular:** "Implement project list component", "Create project detail view", "Add project filtering"

❌ **No time estimates:** Just task list
✅ **Estimated:** Every task has realistic hour estimate

❌ **No priorities:** All tasks equal
✅ **Prioritized:** Clear HIGH/MEDIUM/LOW for each task

---

## Adapting Templates to Your Project

### Same Structure, Different Content

**Template shows:** Design agency SaaS
**Your project:** E-commerce platform for handmade goods

**Adapt by:**
- Keep document structure (sections, format)
- Change content to your market/product
- Adjust competitive set to your industry
- Modify tech stack to your requirements

### Size Adjustments

**Smaller project:**
- Fewer competitors (3-5 instead of 7)
- Simpler architecture (monolith vs microservices)
- Fewer endpoints (essential CRUD only)

**Larger project:**
- More detailed breakdown
- Additional ADRs
- More granular tasks
- Multi-repo structure

---

## Training Exercise

**Before starting Module 2:**

1. **Read all business templates** (30 minutes)
2. **Note what makes them good:**
   - Specificity
   - Evidence/data
   - Clear structure
   - Professional tone
3. **Make a checklist** of quality markers
4. **Use checklist** when generating your documents

**Before starting Module 3:**

1. **Read all technical templates** (30 minutes)
2. **Study diagram formats** (mermaid syntax)
3. **Understand ADR format** (Status, Context, Decision, Consequences)
4. **Note level of detail** in schemas and APIs

**Before starting Module 4:**

1. **Read PROJECT-PLAN and TASKLIST** (15 minutes)
2. **Count tasks** (understand granularity)
3. **Review estimates** (are they realistic?)
4. **Note checkpoint format**

---

## After Completing Sample Project

### Self-Evaluation

Compare your generated documents to templates:

**Score yourself (1-5):**
- **Detail level:** Is mine as detailed?
- **Clarity:** Is mine as clear?
- **Completeness:** Did I cover all sections?
- **Professionalism:** Ready to show a client/investor?
- **Actionability:** Can dev team start building?

**If scoring <4 on any:**
- Review template again
- Identify gaps
- Refine prompts
- Regenerate document

### Portfolio Pieces

Your sample project outputs can be:
- ✅ Portfolio examples (show potential employers/clients)
- ✅ Template starting points for future projects
- ✅ Reference for quality standards

---

## Next Steps

1. **Read this README** ✅ You're doing it now
2. **Browse templates** (don't read in detail yet)
3. **Start Module 2 training**
4. **Read templates BEFORE generating each document**
5. **Generate your versions**
6. **Compare quality**
7. **Refine until matching template standards**

---

## Template Versioning

**Version:** 1.0
**Based on:** PixelFlow Design Agency SaaS
**Last Updated:** 2025-11-16
**Quality Level:** Production-ready, investor-grade

**Updates:** Templates will evolve based on pilot user feedback

---

**Remember:** These templates are your quality benchmark. Don't settle for less detailed output. CODITECT agents can generate this quality - your prompts need to be specific enough to guide them there.

**Quality motto:** "If it's not as good as the template, refine your prompt."

🎯 **Now you know what "good" looks like. Let's create it for your project.**
