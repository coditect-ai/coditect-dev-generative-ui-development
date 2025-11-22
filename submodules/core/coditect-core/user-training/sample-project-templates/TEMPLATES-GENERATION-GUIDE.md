# Sample Templates Generation Guide

> **Complete sample templates will be generated during your training**
> **This directory will contain all expected outputs as you progress**

## Templates You'll Create During Training

### Module 2: Business Discovery Templates

Working through Module 2, you'll generate:

1. **01-market-research.md** - TAM/SAM/SOM, competitors, trends
2. **02-value-proposition.md** - Problem, solution, differentiation
3. **03-ideal-customer-profile.md** - Demographics, psychographics, behavioral
4. **04-product-market-fit.md** - 7-Fit framework analysis
5. **05-competitive-analysis.md** - Feature matrix, positioning
6. **06-go-to-market-strategy.md** - GTM motion, acquisition strategy
7. **07-pricing-strategy.md** - Pricing model, tiers, justification

### Module 3: Technical Specification Templates

Working through Module 3, you'll generate:

1. **01-system-architecture.md** - C4 diagrams, tech stack
2. **02-database-schema.md** - ERD, tables, relationships
3. **03-api-specification.md** - REST API, OpenAPI format
4. **04-software-design-document.md** - Module design, features
5. **ADR-001-database-choice.md** - Why PostgreSQL
6. **ADR-002-authentication-method.md** - Why JWT
7. **ADR-003-deployment-strategy.md** - Why Kubernetes

### Module 4: Project Management Templates

Working through Module 4, you'll generate:

1. **PROJECT-PLAN.md** - Complete project plan with phases
2. **TASKLIST-with-checkpoints.md** - All tasks with estimates
3. **README.md** - Project overview
4. **CLAUDE.md** - Project context

## How to Generate Templates

### Option 1: During Training (Recommended)

As you complete each module:
1. Save your generated documents to this directory
2. They become your reference templates
3. Compare future projects against these

### Option 2: Generate Complete Set Now

If you want all templates before starting training:

```python
# Use the orchestrator to generate complete sample project
Task(
    subagent_type="general-purpose",
    prompt="Use orchestrator subagent to create a complete project specification for PixelFlow - an all-in-one SaaS platform for design agencies.

Project Details:
- Name: PixelFlow
- Target: Small design agencies (5-20 people)
- Problem: Agencies use 10+ fragmented tools
- Solution: Unified platform for project management, time tracking, invoicing, client galleries
- Business Model: Freemium → Pro ($49/mo) → Agency ($199/mo)

Generate ALL of these documents with production-quality detail:

BUSINESS (save to user-training/sample-project-templates/business/):
1. 01-market-research.md
2. 02-value-proposition.md
3. 03-ideal-customer-profile.md
4. 04-product-market-fit.md
5. 05-competitive-analysis.md
6. 06-go-to-market-strategy.md
7. 07-pricing-strategy.md

TECHNICAL (save to user-training/sample-project-templates/technical/):
1. 01-system-architecture.md (with C4 diagrams)
2. 02-database-schema.md (with ERD)
3. 03-api-specification.md (OpenAPI 3.1 format)
4. 04-software-design-document.md
5. ADR-001-database-choice.md
6. ADR-002-authentication-method.md
7. ADR-003-deployment-strategy.md

PROJECT MANAGEMENT (save to user-training/sample-project-templates/project-management/):
1. PROJECT-PLAN.md (4 phases, timeline, risks)
2. TASKLIST-with-checkpoints.md (50+ tasks)
3. README.md
4. CLAUDE.md

Each document must be:
- Production-quality (investor/developer ready)
- Specific to PixelFlow (not generic)
- Complete with all sections
- Professional formatting
- Realistic and actionable"
)
```

### Option 3: Generate Individually

Generate each document one at a time using appropriate agents:

```python
# Market Research
Task(
    subagent_type="general-purpose",
    prompt="Use competitive-market-analyst subagent to create comprehensive market research for PixelFlow (design agency SaaS platform).

Target: Small design agencies (5-20 people)
Output: user-training/sample-project-templates/business/01-market-research.md

Include:
- TAM/SAM/SOM with calculations
- 7 key competitors analyzed
- Market trends with data
- Customer pain points validated
- Willingness to pay estimates"
)

# System Architecture
Task(
    subagent_type="general-purpose",
    prompt="Use senior-architect subagent to create system architecture for PixelFlow.

Output: user-training/sample-project-templates/technical/01-system-architecture.md

Include:
- C4 Context diagram (mermaid)
- C4 Container diagram (mermaid)
- Technology stack recommendations
- System boundaries
- Security architecture"
)

# PROJECT-PLAN
Task(
    subagent_type="general-purpose",
    prompt="Use orchestrator subagent to create complete PROJECT-PLAN.md for PixelFlow.

Output: user-training/sample-project-templates/project-management/PROJECT-PLAN.md

Include:
- Executive summary
- Objectives & success criteria
- 4 development phases
- Timeline with milestones
- Risk assessment
- Resource requirements"
)
```

## Why Templates Matter

**Before training:** Templates show what "good" looks like
**During training:** Compare your outputs to templates
**After training:** Use templates as quality benchmark

## Quality Standards

Each template must demonstrate:

✅ Production-ready quality
✅ Specific (not generic)
✅ Complete (all sections)
✅ Professional formatting
✅ Actionable (devs can build from it)

## Using Templates

### As Quality Benchmark

After generating a document:
1. Compare to template
2. Check level of detail
3. Verify completeness
4. Ensure professionalism
5. Refine if needed

### As Learning Tool

Study templates to understand:
- What sections to include
- How much detail is required
- How to structure information
- What makes specifications actionable

### As Starting Point

For future projects:
- Same structure, different content
- Adapt to your domain
- Maintain quality standards
- Customize for your needs

---

**Next Steps:**

1. Review user-training/sample-project-templates/README.md
2. Choose generation method (during training recommended)
3. Study completed templates before generating your own
4. Use templates as quality benchmark for all future work

**Remember:** The goal is not to copy templates, but to understand what production-quality specifications look like, then create your own at that level.
