# CODITECT Estimation Engine - Project Requirements Document (PRD)

**Document Version:** 1.0
**Created:** 2025-11-22
**Document Owner:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
**Project Type:** New CODITECT Submodule (ops category)
**Repository:** `coditect-ops-estimation-engine`
**Status:** Requirements Definition Phase

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Strategic Context](#strategic-context)
4. [User Personas](#user-personas)
5. [Functional Requirements](#functional-requirements)
6. [Technical Requirements](#technical-requirements)
7. [Use Cases & User Stories](#use-cases--user-stories)
8. [Data Model](#data-model)
9. [API Specification](#api-specification)
10. [Reporting Requirements](#reporting-requirements)
11. [Integration Plan](#integration-plan)
12. [Success Metrics](#success-metrics)
13. [Risk Assessment](#risk-assessment)
14. [Implementation Roadmap](#implementation-roadmap)
15. [Budget & Resources](#budget--resources)

---

## Executive Summary

### Purpose

The **CODITECT Estimation Engine** is a production-ready estimation, budgeting, and reporting tool for software projects using evidence-based methodologies. It provides developers, project managers, and executives with accurate cost/time/resource estimates based on industry-standard calculation methods and historical project data.

### Goals

**Primary Goals:**

1. **Automate Software Estimation** - Replace manual spreadsheets with automated calculation engine
2. **Evidence-Based Methodology** - Use COCOMO II, Function Points, Story Points, and bottom-up WBS
3. **Historical Accuracy** - Learn from past projects to improve future estimates
4. **Multi-Format Reports** - Generate budgets, timelines, Gantt charts, risk analysis
5. **CODITECT Integration** - Slash commands, agents, skills for seamless workflow

**Secondary Goals:**

6. **Codebase Analysis** - Automatically count LOC, complexity, language distribution
7. **GitHub/JIRA Integration** - Import actual data for estimate validation
8. **Sales Enablement** - Generate customer quotes from requirements
9. **Audit Trail** - Track estimate vs. actual for accountability

### Success Criteria

**By Production Launch:**

✅ Support all 6 estimation methodologies (COCOMO II, Bottom-Up, Story Points, Function Points, Three-Point, Parametric)
✅ Automated codebase analysis via `cloc`/`tokei` integration
✅ 5+ report formats (Budget, Timeline, Risk, Comparison, Export)
✅ CODITECT integration (`/estimate` command, estimation-calculator skill, budget-analyst agent)
✅ Historical project database with 10+ reference projects
✅ <2s estimation latency for typical projects
✅ Accuracy within ±20% for projects with historical data
✅ Complete API documentation (OpenAPI 3.1)
✅ Web UI + CLI + API access modes

### Value Proposition

**For Project Managers:**
- "Estimate project costs in 5 minutes instead of 5 hours"
- "Evidence-based budgets validated with historical data"

**For CTOs/CEOs:**
- "Validate vendor quotes and internal estimates with industry models"
- "Track estimate accuracy over time to improve budgeting"

**For Developers:**
- "Estimate feature work using story points + team velocity"
- "Integrate estimation into development workflow"

**For Sales Teams:**
- "Generate customer quotes from requirements in minutes"
- "Provide confidence intervals and risk analysis"

---

## Problem Statement

### What Problem Does This Solve?

**Current Pain Points:**

1. **Manual Estimation is Slow** - Teams spend hours in spreadsheets calculating budgets
2. **Inconsistent Methodologies** - Different people use different estimation approaches
3. **No Historical Learning** - Past projects don't inform future estimates
4. **Optimism Bias** - Estimates are often 50-100% under actual costs
5. **No Validation** - No way to verify if vendor quotes are reasonable
6. **Disconnected Tools** - Estimation happens outside development workflow

**Impact of Poor Estimation:**

- Projects run over budget by 50-100% (average software project)
- Timeline delays damage customer relationships
- Inaccurate quotes lead to unprofitable contracts
- Lack of accountability for estimation quality
- Difficult to justify budget requests to stakeholders

### Who Has This Problem?

**Primary Users:**

- **Project Managers** - Creating project budgets before development
- **CTOs/VPs Engineering** - Validating budget proposals and resource allocation
- **Founders/CEOs** - Approving development investments
- **Sales Engineers** - Generating customer quotes from requirements

**Secondary Users:**

- **Developers** - Estimating story/task effort
- **Product Managers** - Prioritizing features by cost
- **Consultants** - Providing clients with accurate SOWs
- **Auditors** - Verifying project cost accuracy

### Why Does This Matter?

**Business Context:**

- Software projects are notorious for cost overruns (Standish Group: 45% over budget)
- Estimation errors reduce profitability and damage reputation
- Executives need data-driven budgets for investment decisions
- Sales teams need accurate quotes to close deals profitably
- Historical tracking enables continuous improvement

**AZ1.AI/CODITECT Context:**

- CODITECT customers are building software projects
- They need to estimate their own development costs
- Integration with CODITECT workflow provides unique value
- Differentiates CODITECT from generic development tools
- Enables CODITECT to provide end-to-end project lifecycle support

---

## Strategic Context

### Ecosystem Role

**CODITECT Architecture Position:**

```
coditect-rollout-master/
├── submodules/
│   ├── ops/                              # Operations category
│   │   ├── coditect-ops-estimation-engine/  # ⭐ THIS SUBMODULE
│   │   ├── coditect-ops-license/         # License management
│   │   ├── coditect-ops-distribution/    # Installation/updates
│   │   ├── coditect-ops-compliance/      # Compliance tracking
│   │   └── coditect-ops-projects/        # Project templates
```

**Category:** `ops` (Operations)
**Priority:** P1 (Important - Revenue enabler)
**Dependencies:**
- `coditect-core` - Agent framework, commands, skills
- `coditect-ops-projects` - Historical project data
- `coditect-cloud-backend` - Optional cloud storage for estimates

**Dependents:**
- Sales teams (quote generation)
- Project planning workflows
- Budget approval processes
- Customer project templates

### Integration with CODITECT Platform

**Distributed Intelligence Pattern:**

```
coditect-ops-estimation-engine/
├── .coditect -> ../../../.coditect    # Symlink to master brain
├── .claude -> .coditect               # Claude Code compatibility
├── src/                               # Estimation engine code
├── data/                              # Historical project database
├── reports/                           # Generated reports
└── scripts/                           # CLI tools
```

**CODITECT Components Added:**

1. **Agent:** `budget-analyst` - Specialized agent for financial analysis and estimation
2. **Command:** `/estimate` - Quick estimation slash command
3. **Skill:** `estimation-calculator` - Reusable estimation patterns
4. **Script:** `estimate-project.py` - CLI estimation tool
5. **Script:** `analyze-codebase.py` - Automated LOC/complexity analysis

### Market Positioning

**Competitive Landscape:**

| Tool | Strengths | Weaknesses |
|------|-----------|------------|
| **Jira Roadmaps** | Team velocity tracking | No COCOMO/Function Points |
| **Microsoft Project** | Timeline/Gantt charts | No evidence-based estimation |
| **COCOMO II Tool** | Industry-standard model | Standalone, no integration |
| **Story Point Calculators** | Agile-friendly | No bottom-up or parametric |
| **Spreadsheets** | Flexible | Manual, error-prone, no learning |

**CODITECT Advantage:**

✅ All 6 methodologies in one tool
✅ Integrated with development workflow
✅ Historical learning from project database
✅ AI-assisted estimation (budget-analyst agent)
✅ Automated codebase analysis
✅ Multi-format reporting
✅ API-first architecture

**Unique Value Proposition:**

> "The only estimation engine that combines industry-standard methodologies with AI-assisted analysis, automated codebase scanning, and seamless integration into your CODITECT development workflow."

---

## User Personas

### Persona 1: Project Manager (Primary)

**Name:** Sarah Chen
**Role:** Senior Project Manager at SaaS Startup
**Experience:** 8 years managing software projects

**Goals:**
- Create accurate project budgets before development starts
- Track estimate vs. actual to improve accuracy over time
- Justify budget requests to executives with data
- Identify high-risk areas requiring contingency

**Pain Points:**
- Spends 4-6 hours per project on manual estimation
- Estimates often 50% under actual costs
- No consistent methodology across projects
- Difficult to explain variances to stakeholders

**Workflows:**
1. Receives project requirements from product team
2. Breaks down into work breakdown structure (WBS)
3. Estimates effort for each task (hours/days)
4. Applies overhead factors (testing, PM, rework)
5. Calculates total cost and timeline
6. Generates budget report for executive approval
7. Tracks actual vs. estimate during execution

**Success Criteria:**
- Reduce estimation time from 6 hours to 1 hour
- Improve accuracy from ±50% to ±20%
- Generate professional budget reports automatically
- Have historical data to defend estimates

**Estimation Engine Usage:**
- Uses `/estimate` command in Claude Code
- Inputs WBS tasks with granular estimates
- Reviews AI-suggested overhead factors
- Exports budget as PDF for executives
- Updates with actuals for historical learning

---

### Persona 2: CTO/VP Engineering (Primary)

**Name:** Marcus Rodriguez
**Role:** CTO at Enterprise Software Company
**Experience:** 15 years in engineering leadership

**Goals:**
- Validate budget proposals from project managers
- Make data-driven resource allocation decisions
- Evaluate vendor quotes for reasonableness
- Improve organizational estimation maturity

**Pain Points:**
- No way to verify if estimates are realistic
- Different teams use different methodologies
- Vendor quotes vary wildly (2x-5x difference)
- No historical data to benchmark against

**Workflows:**
1. Reviews budget proposals from PM team
2. Challenges assumptions and overhead factors
3. Compares against historical similar projects
4. Evaluates vendor proposals for outsourced work
5. Approves or requests revisions
6. Tracks estimation accuracy over time

**Success Criteria:**
- Ability to validate estimates in <30 minutes
- Access to historical project database for benchmarking
- Confidence intervals and risk analysis for decisions
- Year-over-year improvement in estimation accuracy

**Estimation Engine Usage:**
- Reviews budget-analyst agent risk assessments
- Compares parametric model against bottom-up estimates
- Uses COCOMO II to validate vendor quotes
- Generates comparison reports (estimate vs. actual)
- Tracks team velocity and productivity metrics

---

### Persona 3: Founder/CEO (Secondary)

**Name:** Emily Tran
**Role:** CEO at Early-Stage Startup
**Experience:** 3 years running company, non-technical background

**Goals:**
- Understand development costs for investor presentations
- Make build vs. buy decisions with accurate data
- Set realistic timelines for product launches
- Avoid budget surprises that threaten runway

**Pain Points:**
- Can't evaluate if engineering team's estimates are reasonable
- Vendor quotes seem expensive but hard to verify
- No visibility into what drives software costs
- Past projects have gone 2x over budget

**Workflows:**
1. Receives product requirements from product team
2. Asks CTO for development estimate
3. Evaluates estimate against budget/runway
4. Decides to approve, defer, or descope
5. Presents budget to board/investors
6. Monitors actual spending vs. budget

**Success Criteria:**
- Understand cost drivers (LOC, complexity, team size)
- Get confidence intervals (best/worst/likely scenarios)
- Compare internal estimates against industry benchmarks
- Explain budget to non-technical stakeholders

**Estimation Engine Usage:**
- Reviews executive summary reports
- Uses three-point estimation for scenario planning
- Compares function point cost against vendor quotes
- Shares Gantt charts with investors
- Tracks burn rate against original estimate

---

### Persona 4: Sales Engineer (Secondary)

**Name:** Jordan Kim
**Role:** Pre-Sales Engineer at Software Consulting Firm
**Experience:** 5 years in pre-sales and solution architecture

**Goals:**
- Generate accurate customer quotes quickly
- Win deals with competitive but profitable pricing
- Provide scope-of-work (SOW) documents
- Set realistic customer expectations

**Pain Points:**
- Manual quote creation takes 2-3 days
- No consistent pricing methodology
- Quotes are often too low (unprofitable) or too high (lose deal)
- Difficult to justify pricing to customers

**Workflows:**
1. Receives RFP or customer requirements
2. Schedules scoping call with customer
3. Documents functional requirements
4. Estimates development effort
5. Applies pricing model (hourly rate × hours)
6. Generates SOW with timeline and milestones
7. Presents to customer and negotiates

**Success Criteria:**
- Generate quote in <2 hours instead of 2 days
- Win rate >40% with profitable margins
- Professional SOW documents with Gantt charts
- Customers trust pricing as fair and transparent

**Estimation Engine Usage:**
- Uses function point analysis for requirements
- Applies company's standard hourly rates
- Generates PDF quote with risk analysis
- Exports timeline as Gantt chart
- Tracks won/lost deals by estimate accuracy

---

### Persona 5: Developer (Tertiary)

**Name:** Alex Patel
**Role:** Senior Full-Stack Developer
**Experience:** 6 years software development

**Goals:**
- Estimate story/task effort for sprint planning
- Understand team velocity for capacity planning
- Improve personal estimation accuracy
- Advocate for realistic timelines

**Pain Points:**
- Story point estimation feels arbitrary
- No historical data to reference for similar tasks
- Pressure to underestimate to make commitments
- Unclear how individual estimates roll up to project budget

**Workflows:**
1. Reviews user story in sprint planning
2. Estimates story points based on complexity
3. Discusses with team to reach consensus
4. Commits to sprint based on team velocity
5. Tracks actual hours during development
6. Updates estimate if scope changes

**Success Criteria:**
- Story point estimates within ±1 point of actual
- Personal velocity is predictable over time
- Can reference similar past stories for calibration
- Transparent connection between story points and budget

**Estimation Engine Usage:**
- Uses story point calculator with historical velocity
- Reviews similar completed stories for reference
- Tracks personal velocity trends over time
- Converts story points to hours for PM budgets
- Gets automated complexity analysis for new tasks

---

## Functional Requirements

### FR-1: Estimation Methodologies

**Must Support All 6 Industry-Standard Methods:**

#### FR-1.1: COCOMO II (Constructive Cost Model)

**Purpose:** Industry-standard parametric model for software estimation

**Inputs:**
- **Size:** KLOC (thousands of lines of code) OR Function Points (auto-converted)
- **Scale Factors (5):** Precedentedness, Development Flexibility, Architecture/Risk Resolution, Team Cohesion, Process Maturity
- **Effort Multipliers (17):** Product attributes (reliability, database size, complexity), Platform (execution time, storage), Personnel (analyst capability, programmer capability, experience), Project (tools, schedule, multisite)

**Formula:**
```
Effort (person-months) = A × Size^E × ∏(EM_i)
where:
  A = calibration constant (default 2.94)
  E = exponent (0.91 + 0.01 × Σ(SF_i))
  EM_i = effort multiplier values (0.75 - 2.00)
```

**Outputs:**
- Effort (person-months)
- Development time (months)
- Team size (people)
- Cost ($) = Effort × Blended Hourly Rate × Hours/Month

**Acceptance Criteria:**
- [ ] Accurate COCOMO II calculation matching COPSEMO reference tool
- [ ] Auto-convert Function Points to KLOC using language-specific ratios
- [ ] All 5 scale factors configurable (0-5 scale)
- [ ] All 17 effort multipliers configurable
- [ ] Support for multiple language productivity rates
- [ ] Generate sensitivity analysis (which factors impact most)

---

#### FR-1.2: Bottom-Up Estimation (Work Breakdown Structure)

**Purpose:** Granular task-by-task estimation with rollup to project total

**Inputs:**
- **WBS Hierarchy:** Project → Phases → Modules → Tasks
- **Task Details:** Name, description, estimated hours, assigned role
- **Roles:** Junior Dev, Mid Dev, Senior Dev, Lead Dev, PM, QA, DevOps (with hourly rates)
- **Overhead Factors:** Testing (%), PM (%), Infrastructure (%), Rework (%), Contingency (%)

**Process:**
1. User creates hierarchical WBS (tree structure)
2. For each leaf task, enters estimated hours
3. Assigns role(s) to each task
4. System calculates:
   - Direct effort (sum of all task hours)
   - Overhead (testing, PM, infra, rework)
   - Contingency (risk buffer)
   - Total effort (direct + overhead + contingency)
   - Total cost (effort × blended rate)
   - Duration (effort / team size / availability %)

**Outputs:**
- Total effort (hours)
- Total cost ($)
- Duration (weeks/months)
- Cost breakdown by role
- Cost breakdown by phase/module
- Critical path analysis

**Acceptance Criteria:**
- [ ] Support unlimited WBS depth (nesting)
- [ ] Drag-and-drop task reorganization
- [ ] Bulk import from CSV/Excel
- [ ] Auto-calculate overhead percentages
- [ ] Visualize WBS as tree diagram
- [ ] Export WBS to Microsoft Project format

---

#### FR-1.3: Story Points + Velocity

**Purpose:** Agile-friendly estimation using historical team velocity

**Inputs:**
- **Stories:** List of user stories with story point estimates (1, 2, 3, 5, 8, 13, 21)
- **Team Velocity:** Average story points completed per sprint (from historical data)
- **Sprint Duration:** Length of sprint in weeks (default 2)
- **Team Size:** Number of developers on team

**Calculation:**
```
Total Story Points = Σ(story_points)
Number of Sprints = Total Story Points / Team Velocity
Duration (weeks) = Number of Sprints × Sprint Duration
Effort (hours) = Total Story Points × Hours per Point × Team Size
Cost ($) = Effort × Blended Hourly Rate
```

**Outputs:**
- Total story points
- Number of sprints required
- Duration (weeks)
- Effort (hours)
- Cost ($)
- Velocity trend chart (if historical data available)

**Acceptance Criteria:**
- [ ] Import stories from JIRA/Linear API
- [ ] Calculate team velocity from last 3-6 sprints
- [ ] Support multiple teams with different velocities
- [ ] Fibonacci sequence story point picker
- [ ] Planning poker consensus tracking
- [ ] Burndown chart projection

---

#### FR-1.4: Function Point Analysis

**Purpose:** Language-agnostic size measurement based on functionality

**Inputs:**
- **External Inputs (EI):** User inputs, forms (Simple/Average/Complex)
- **External Outputs (EO):** Reports, screens (Simple/Average/Complex)
- **External Inquiries (EQ):** Queries, lookups (Simple/Average/Complex)
- **Internal Logical Files (ILF):** Database tables (Simple/Average/Complex)
- **External Interface Files (EIF):** External data sources (Simple/Average/Complex)
- **Complexity Adjustment Factors (14):** Data communications, distributed functions, performance, etc.

**Calculation:**
```
Unadjusted Function Points (UFP) = Σ(count × weight)
  where weight based on complexity (Simple/Avg/Complex)

Value Adjustment Factor (VAF) = 0.65 + (0.01 × Σ(CAF_i))
  where CAF_i = 0-5 rating for 14 factors

Adjusted Function Points (AFP) = UFP × VAF

Effort (hours) = AFP × Language Productivity Factor
  (e.g., Python: 20 hours/FP, Java: 30 hours/FP)
```

**Outputs:**
- Unadjusted Function Points
- Adjusted Function Points
- Estimated KLOC (converted)
- Effort (hours)
- Cost ($)

**Acceptance Criteria:**
- [ ] Guided wizard for function point counting
- [ ] Language-specific productivity tables (15+ languages)
- [ ] Convert Function Points to KLOC and vice versa
- [ ] Export as IFPUG-compliant report
- [ ] Historical FP/KLOC ratio tracking by language

---

#### FR-1.5: Three-Point Estimation (PERT)

**Purpose:** Probabilistic estimation with optimistic, likely, pessimistic scenarios

**Inputs:**
- **Optimistic (O):** Best-case effort (10th percentile)
- **Most Likely (M):** Realistic effort (50th percentile)
- **Pessimistic (P):** Worst-case effort (90th percentile)
- **Confidence Level:** Desired confidence (e.g., 80%, 90%)

**Formulas:**
```
Expected Effort (E) = (O + 4M + P) / 6
Standard Deviation (σ) = (P - O) / 6
Variance = σ²

Confidence Intervals:
  68% confidence: E ± σ
  95% confidence: E ± 2σ
  99.7% confidence: E ± 3σ
```

**Outputs:**
- Expected effort (weighted average)
- Standard deviation (uncertainty measure)
- Confidence intervals (range of outcomes)
- Probability distribution graph
- Risk level (High if P > 2M)

**Acceptance Criteria:**
- [ ] Support task-level, module-level, and project-level PERT
- [ ] Monte Carlo simulation for combined uncertainty
- [ ] Visualize probability distribution as bell curve
- [ ] Identify high-variance tasks for risk mitigation
- [ ] Export scenarios as separate estimates

---

#### FR-1.6: Parametric Models (Historical Regression)

**Purpose:** Statistical prediction based on similar past projects

**Inputs:**
- **Project Attributes:** Size (KLOC, FP), Domain, Team Size, Language, Platform
- **Historical Database:** Past projects with actual effort/cost/duration
- **Similarity Filters:** Domain, language, team size range

**Process:**
1. Filter historical projects by similarity criteria
2. Build regression model: Effort = f(Size, Team, Complexity, ...)
3. Apply model to new project attributes
4. Calculate confidence interval based on model fit (R²)

**Outputs:**
- Predicted effort (hours)
- Predicted cost ($)
- Predicted duration (weeks)
- Confidence interval (e.g., ±20%)
- Similar projects used in model
- Model accuracy (R² value)

**Acceptance Criteria:**
- [ ] Minimum 10 historical projects required for model
- [ ] Support linear, polynomial, and exponential regression
- [ ] Filter by domain, language, team size, year
- [ ] Show which projects contributed to prediction
- [ ] Warn if new project is outside training data range
- [ ] Auto-update model as new projects complete

---

### FR-2: Automated Codebase Analysis

**Purpose:** Automatically measure project size without manual counting

#### FR-2.1: Lines of Code (LOC) Counting

**Tools:**
- **Primary:** `cloc` (Count Lines of Code) - https://github.com/AlDanial/cloc
- **Secondary:** `tokei` (for Rust-friendly alternative)

**Metrics:**
- Total LOC (all files)
- LOC by language (Python: 5000, JavaScript: 3000, etc.)
- Code vs. Comments vs. Blank lines
- LOC by directory/module
- Language distribution (%)

**Acceptance Criteria:**
- [ ] Integrate `cloc` as subprocess
- [ ] Parse `cloc` JSON output
- [ ] Visualize language distribution as pie chart
- [ ] Track LOC growth over time (git history)
- [ ] Ignore generated code and vendor directories

---

#### FR-2.2: Complexity Analysis

**Tools:**
- **Cyclomatic Complexity:** `radon` (Python), `eslint-complexity` (JS)
- **Cognitive Complexity:** SonarQube metrics
- **Halstead Metrics:** Volume, difficulty, effort

**Metrics:**
- Average cyclomatic complexity per function
- High-complexity hotspots (>10 complexity)
- Code maintainability index
- Estimated development time based on complexity

**Acceptance Criteria:**
- [ ] Calculate cyclomatic complexity for Python/JS/Java/Go
- [ ] Identify top 10 most complex files
- [ ] Apply complexity multiplier to COCOMO estimates
- [ ] Visualize complexity distribution histogram
- [ ] Flag files with complexity >15 as high-risk

---

#### FR-2.3: Dependency Analysis

**Tools:**
- **Python:** `pipdeptree`
- **JavaScript:** `npm ls`, `yarn why`
- **Java:** `mvn dependency:tree`

**Metrics:**
- Number of external dependencies
- Dependency depth (direct vs. transitive)
- Outdated dependencies (security risk)
- License compliance

**Acceptance Criteria:**
- [ ] Count total dependencies by ecosystem
- [ ] Identify deprecated or unmaintained deps
- [ ] Estimate integration effort (1 hour per new dependency)
- [ ] Flag GPL/copyleft licenses for legal review

---

### FR-3: Integration with External Systems

#### FR-3.1: GitHub API Integration

**Purpose:** Import actual data for estimate validation

**Capabilities:**
- **Pull Requests:** Analyze merged PR stats (lines changed, review time)
- **Commits:** Count commits, authors, commit frequency
- **Issues:** Track issue resolution time
- **Velocity:** Calculate team velocity from closed issues

**Acceptance Criteria:**
- [ ] Authenticate with GitHub Personal Access Token
- [ ] Fetch repository statistics (LOC, contributors, activity)
- [ ] Calculate average PR cycle time
- [ ] Import issues with labels as story points
- [ ] Track estimate vs. actual (issue estimate vs. PR LOC)

---

#### FR-3.2: JIRA/Linear Integration

**Purpose:** Import story points and sprint velocity

**Capabilities:**
- **Stories:** Import user stories with story point estimates
- **Sprints:** Fetch sprint velocity (points completed per sprint)
- **Epics:** Aggregate story points by epic
- **Velocity Trends:** Chart velocity over last 6 sprints

**Acceptance Criteria:**
- [ ] Authenticate with JIRA API token
- [ ] Fetch all stories in a project with story points
- [ ] Calculate team velocity from completed sprints
- [ ] Import epic hierarchy for WBS
- [ ] Sync estimates back to JIRA (optional)

---

### FR-4: Reporting & Visualization

**Required Report Types:**

#### FR-4.1: Budget Estimate Report

**Contents:**
- Project summary (name, size, timeline)
- Estimation methodology used
- Input parameters and assumptions
- Cost breakdown by role/phase
- Total cost with confidence interval
- Risk factors and mitigation

**Format:** PDF, Markdown, HTML

**Acceptance Criteria:**
- [ ] Professional formatting with company logo
- [ ] Executive summary (1 page)
- [ ] Detailed breakdown (3-5 pages)
- [ ] Assumptions and disclaimers
- [ ] Signature block for approval

---

#### FR-4.2: Timeline Projection (Gantt Chart)

**Contents:**
- Project phases as horizontal bars
- Task dependencies (arrows)
- Critical path highlighted
- Milestones as diamonds
- Resource allocation

**Format:** Interactive HTML, PNG image, Microsoft Project XML

**Acceptance Criteria:**
- [ ] Render Gantt chart with D3.js or Mermaid
- [ ] Show critical path in red
- [ ] Support task dependencies (finish-to-start, start-to-start)
- [ ] Export to MS Project for editing
- [ ] Responsive design for mobile viewing

---

#### FR-4.3: Risk Analysis Report

**Contents:**
- Risk factors identified (complexity, team, schedule)
- Probability × Impact matrix
- Sensitivity analysis (which factors matter most)
- Mitigation recommendations
- Confidence intervals

**Format:** PDF, Interactive Dashboard

**Acceptance Criteria:**
- [ ] Calculate risk score (0-100)
- [ ] Visualize probability distribution
- [ ] Identify top 5 risk drivers
- [ ] Provide mitigation guidance
- [ ] Track risk over project lifecycle

---

#### FR-4.4: Estimate vs. Actual Comparison

**Purpose:** Track estimation accuracy for continuous improvement

**Contents:**
- Original estimate vs. actual cost/time
- Variance % (over/under)
- Breakdown by phase/module
- Root cause analysis (what was missed)
- Lessons learned

**Format:** PDF, Dashboard

**Acceptance Criteria:**
- [ ] Require actual data input at project completion
- [ ] Calculate variance % for effort, cost, duration
- [ ] Identify patterns (always underestimate testing?)
- [ ] Update parametric model with actuals
- [ ] Track accuracy trends over time

---

#### FR-4.5: Export Formats

**Required Exports:**
- **PDF:** Professional reports for executives
- **Excel:** Editable budgets for finance teams
- **JSON:** API integration with other tools
- **Markdown:** Version-controlled estimates in git
- **CSV:** Data export for analysis
- **MS Project XML:** Timeline import

**Acceptance Criteria:**
- [ ] All reports support PDF export
- [ ] Excel export with formulas intact
- [ ] JSON follows OpenAPI schema
- [ ] Markdown renders on GitHub
- [ ] CSV with proper escaping

---

## Technical Requirements

### TR-1: Technology Stack

#### TR-1.1: Calculation Engine (Backend)

**Language:** Python 3.10+

**Rationale:**
- Excellent scientific computing libraries (NumPy, SciPy)
- Mature data manipulation (Pandas)
- Fast development for complex calculations
- Easy integration with AI/ML for parametric models

**Key Libraries:**
- **NumPy:** Matrix calculations, statistical functions
- **Pandas:** Data manipulation, historical database
- **SciPy:** Regression analysis, optimization
- **scikit-learn:** Machine learning for parametric models
- **Pydantic:** Data validation and schemas

**Acceptance Criteria:**
- [ ] Python 3.10+ compatible
- [ ] Type hints throughout codebase
- [ ] 80%+ test coverage with pytest
- [ ] No dependencies on proprietary software

---

#### TR-1.2: REST API (Backend)

**Framework:** FastAPI

**Rationale:**
- Modern async Python framework
- Auto-generated OpenAPI 3.1 docs
- Fast performance (comparable to Node.js)
- Built-in validation with Pydantic
- Easy deployment (Docker, Uvicorn)

**API Design:**
- RESTful endpoints (`/estimates`, `/projects`, `/reports`)
- JWT authentication for multi-user
- Rate limiting for API abuse prevention
- Versioned API (`/api/v1/`)
- CORS support for web UI

**Acceptance Criteria:**
- [ ] OpenAPI 3.1 spec auto-generated
- [ ] All endpoints documented with examples
- [ ] <200ms response time for estimates
- [ ] Support 100+ concurrent requests
- [ ] Comprehensive error handling

---

#### TR-1.3: Web UI (Frontend)

**Framework:** React 18 + TypeScript

**Rationale:**
- Component reusability (estimation forms, charts)
- Strong typing with TypeScript
- Large ecosystem for charting (Recharts, D3.js)
- CODITECT standard for frontend

**UI Components:**
- **Forms:** Estimation input wizards
- **Charts:** Gantt charts, pie charts, line charts
- **Tables:** WBS hierarchies, cost breakdowns
- **Exports:** PDF generation (jsPDF), Excel (SheetJS)

**Acceptance Criteria:**
- [ ] Responsive design (mobile-friendly)
- [ ] Accessible (WCAG 2.1 Level AA)
- [ ] Dark mode support
- [ ] <3s initial load time
- [ ] Offline support (PWA) for saved estimates

---

#### TR-1.4: CLI Tool

**Framework:** Python Click

**Rationale:**
- Quick estimates from command line
- Integration with CI/CD pipelines
- Scriptable for automation
- Lightweight (no UI dependencies)

**Commands:**
```bash
# Estimate from codebase
coditect-estimate analyze ./src --method cocomo

# Estimate from WBS file
coditect-estimate wbs tasks.csv --output budget.pdf

# Import from JIRA
coditect-estimate jira PROJECT-123 --method velocity

# Generate report
coditect-estimate report estimate-id-456 --format pdf
```

**Acceptance Criteria:**
- [ ] Help text for all commands
- [ ] Support piped input/output
- [ ] Exit codes for CI/CD integration
- [ ] Progress bars for long operations
- [ ] Config file support (~/.coditect/estimate.yaml)

---

#### TR-1.5: Database

**Primary:** SQLite (for local/embedded use)
**Optional:** PostgreSQL (for cloud multi-user)

**Rationale:**
- SQLite: Zero-config, embedded, fast for single-user
- PostgreSQL: Full ACID, multi-user, cloud-ready

**Schema:**
- **projects:** id, name, created_at, updated_at, status
- **estimates:** id, project_id, method, inputs (JSON), outputs (JSON)
- **actuals:** id, project_id, actual_effort, actual_cost, actual_duration
- **historical_data:** Aggregated metrics for parametric models

**Acceptance Criteria:**
- [ ] SQLite for CLI and standalone use
- [ ] PostgreSQL support for cloud backend
- [ ] Alembic migrations for schema changes
- [ ] Backup/restore functionality
- [ ] Data export as JSON for portability

---

### TR-2: Performance Requirements

| Metric | Requirement | Measurement |
|--------|-------------|-------------|
| **Estimation Latency** | <2s for typical project | Time from API request to response |
| **Codebase Analysis** | <30s for 100K LOC | Time for `cloc` + complexity analysis |
| **Report Generation** | <10s for PDF export | Time to generate 10-page report |
| **API Throughput** | 100+ requests/sec | Load testing with Locust |
| **Database Query** | <100ms for historical lookup | Query response time |
| **UI Responsiveness** | <200ms for input validation | Time to validate form field |

**Acceptance Criteria:**
- [ ] Load test with 1000 concurrent users
- [ ] Profile slow endpoints with cProfile
- [ ] Cache frequently accessed data (Redis optional)
- [ ] Optimize database queries (indexes, explain plans)
- [ ] Lazy load UI components

---

### TR-3: Security Requirements

**Authentication:**
- JWT tokens for API access
- Session-based auth for web UI
- API keys for CLI integration

**Authorization:**
- Role-based access control (Admin, PM, Developer, Viewer)
- Project-level permissions (who can view/edit estimates)

**Data Protection:**
- Encrypt sensitive data at rest (SQLCipher for SQLite)
- HTTPS required for all API calls
- No logging of sensitive inputs
- Regular security audits (npm audit, safety)

**Acceptance Criteria:**
- [ ] All endpoints require authentication
- [ ] Passwords hashed with bcrypt
- [ ] HTTPS enforced (HSTS header)
- [ ] Rate limiting (100 requests/min per user)
- [ ] No SQL injection vulnerabilities
- [ ] OWASP Top 10 compliance

---

### TR-4: Scalability Requirements

**Horizontal Scaling:**
- Stateless API (can run multiple instances)
- Load balancer support (Nginx, HAProxy)
- Database connection pooling

**Vertical Scaling:**
- Efficient memory usage (<500MB per process)
- CPU optimization (multiprocessing for analysis)
- Disk space limits (historical data pruning)

**Data Volume:**
- Support 10,000+ projects in database
- 1,000+ estimates per project
- 100MB+ historical data

**Acceptance Criteria:**
- [ ] Tested with 10K projects in database
- [ ] Response time <2s even with 10K projects
- [ ] Pagination for large result sets
- [ ] Database indexes on common queries
- [ ] Background jobs for long-running analysis

---

### TR-5: Deployment & Operations

**Deployment Options:**

1. **Local/CLI:** Pip install, runs on developer machine
2. **Docker:** Single container with SQLite
3. **Docker Compose:** Multi-container with PostgreSQL
4. **Kubernetes:** Cloud deployment with auto-scaling
5. **Cloud (Optional):** Hosted on `coditect-cloud-backend`

**Monitoring:**
- Prometheus metrics (request count, latency, errors)
- Structured logging (JSON logs)
- Health check endpoint (`/health`)
- Error tracking (Sentry integration optional)

**Acceptance Criteria:**
- [ ] Dockerfile with <500MB image size
- [ ] Docker Compose for local development
- [ ] Kubernetes YAML manifests
- [ ] Health check returns 200 OK in <1s
- [ ] Logs include request ID for tracing

---

## Use Cases & User Stories

### UC-1: Estimate New Project from Requirements

**Actor:** Project Manager (Sarah)
**Goal:** Get a budget estimate before development starts

**Preconditions:**
- Sarah has project requirements document
- She knows desired estimation method (Bottom-Up WBS)

**Main Flow:**

1. Sarah opens CODITECT estimation engine web UI
2. She clicks "New Estimate" and selects "Bottom-Up (WBS)"
3. She enters project name: "Customer Portal Redesign"
4. She creates WBS hierarchy:
   ```
   Customer Portal Redesign
   ├── Phase 1: Design
   │   ├── Wireframes (8 hours, Designer)
   │   ├── UI Mockups (16 hours, Designer)
   │   └── Design Review (4 hours, PM)
   ├── Phase 2: Frontend Development
   │   ├── Login Module (24 hours, Senior Dev)
   │   ├── Dashboard (32 hours, Mid Dev)
   │   └── Settings Page (16 hours, Mid Dev)
   ├── Phase 3: Backend API
   │   ├── Auth Service (40 hours, Senior Dev)
   │   ├── User API (24 hours, Mid Dev)
   │   └── Database Schema (16 hours, Senior Dev)
   └── Phase 4: Testing & Deployment
       ├── Unit Tests (32 hours, QA)
       ├── Integration Tests (24 hours, QA)
       └── Deployment (16 hours, DevOps)
   ```
5. System calculates:
   - Direct Effort: 252 hours
   - Overhead (40%): 101 hours
   - Contingency (15%): 53 hours
   - **Total: 406 hours**
6. Sarah sets blended rate at $120/hour
7. System calculates **Total Cost: $48,720**
8. Sarah generates PDF budget report
9. She emails report to CTO for approval

**Postconditions:**
- Estimate saved in database
- PDF report generated
- Sarah can track actual vs. estimate later

**Alternative Flows:**
- **A1:** Sarah imports WBS from CSV instead of manual entry
- **A2:** System suggests overhead percentages based on historical data
- **A3:** CTO requests changes; Sarah edits estimate and regenerates report

**Acceptance Criteria:**
- [ ] Complete estimate in <30 minutes
- [ ] PDF report is professional and clear
- [ ] Estimate is saved and retrievable
- [ ] Can edit and regenerate report

**User Story:**
```
As a Project Manager,
I want to create bottom-up estimates from a WBS,
So that I can generate accurate budgets for executive approval.

Acceptance:
- WBS editor supports unlimited nesting
- Overhead factors auto-suggested from history
- PDF export in <10 seconds
- Estimate saved in database
```

---

### UC-2: Validate Vendor Quote with COCOMO

**Actor:** CTO (Marcus)
**Goal:** Verify if vendor's quote is reasonable

**Preconditions:**
- Vendor provided quote: $180K for 50K LOC Java application
- Marcus has access to estimation engine

**Main Flow:**

1. Marcus receives vendor quote for $180K
2. He opens estimation engine CLI
3. He runs:
   ```bash
   coditect-estimate cocomo \
     --kloc 50 \
     --language java \
     --complexity average \
     --team-experience high \
     --output vendor-validation.pdf
   ```
4. System calculates using COCOMO II:
   - Size: 50 KLOC
   - Effort Multipliers: Complexity (1.2), Team Exp (0.85)
   - Scale Factors: Team Cohesion (4), Process Maturity (3)
   - **Estimated Effort:** 140 person-months
   - **Estimated Cost:** $168K (at $100/hour blended rate)
5. System generates report showing:
   - Estimated cost: $168K (±20% = $134K - $202K)
   - Vendor quote: $180K
   - **Assessment:** Within reasonable range ✅
6. Marcus approves vendor quote with confidence

**Postconditions:**
- Marcus has data-backed validation
- Report saved for future reference
- Can negotiate if quote was outside range

**Alternative Flows:**
- **A1:** Vendor quote is $250K (49% over estimate) → Marcus negotiates or finds another vendor
- **A2:** Marcus doesn't know KLOC → Uses function point method instead

**Acceptance Criteria:**
- [ ] COCOMO calculation matches reference tools
- [ ] Confidence interval clearly displayed
- [ ] Report explains assumptions
- [ ] CLI completes in <5 seconds

**User Story:**
```
As a CTO,
I want to validate vendor quotes with COCOMO,
So that I can ensure we're not overpaying for development.

Acceptance:
- CLI accepts KLOC, language, complexity
- Report generated in <5s
- Confidence interval shown (e.g., ±20%)
- Clear pass/fail assessment
```

---

### UC-3: Track Team Velocity for Sprint Planning

**Actor:** Developer (Alex)
**Goal:** Estimate sprint capacity based on historical velocity

**Preconditions:**
- Team has completed 6 sprints
- JIRA integration configured

**Main Flow:**

1. Alex opens sprint planning meeting
2. Product owner presents 18 stories totaling 75 story points
3. Alex runs:
   ```bash
   coditect-estimate jira \
     --project PROJ-123 \
     --method velocity \
     --sprints 6
   ```
4. System fetches from JIRA:
   - Sprint 1: 28 points completed
   - Sprint 2: 32 points completed
   - Sprint 3: 26 points completed
   - Sprint 4: 30 points completed
   - Sprint 5: 34 points completed
   - Sprint 6: 31 points completed
5. System calculates:
   - **Average Velocity:** 30 points/sprint
   - **Standard Deviation:** 3 points
   - **Recommended Commitment:** 27-33 points (90% confidence)
6. Alex reports to team: "We can commit to 30 points this sprint"
7. Team selects top 30 points of work from backlog

**Postconditions:**
- Team has realistic commitment
- Stakeholders have accurate timeline (75 points / 30 per sprint = 3 sprints)

**Alternative Flows:**
- **A1:** Velocity is declining → System warns of potential issues
- **A2:** New team member joining → System suggests reducing commitment

**Acceptance Criteria:**
- [ ] JIRA API fetches last N sprints
- [ ] Velocity trend chart displayed
- [ ] Recommended commitment shown with confidence
- [ ] Can export as chart for stakeholders

**User Story:**
```
As a Developer,
I want to calculate team velocity from JIRA,
So that we can make realistic sprint commitments.

Acceptance:
- Fetch velocity from last 6 sprints
- Calculate average and std deviation
- Show velocity trend chart
- Recommend commitment with confidence level
```

---

### UC-4: Generate Customer Quote from Requirements

**Actor:** Sales Engineer (Jordan)
**Goal:** Create SOW with pricing for customer RFP

**Preconditions:**
- Customer provided requirements document
- Company standard rates configured ($150/hour)

**Main Flow:**

1. Jordan receives RFP for "E-commerce Marketplace MVP"
2. He analyzes requirements and counts:
   - 15 external inputs (forms)
   - 12 external outputs (reports)
   - 8 external inquiries (searches)
   - 6 internal files (database tables)
   - 3 external interfaces (payment gateway, shipping API, auth)
3. He opens estimation engine and selects "Function Point Analysis"
4. He enters function point counts with complexity ratings
5. System calculates:
   - Unadjusted Function Points: 245
   - Complexity Adjustment: 1.15 (above average complexity)
   - **Adjusted Function Points: 282**
6. System converts to effort:
   - Language: Python/React
   - Productivity: 25 hours/FP
   - **Estimated Effort:** 7,050 hours
7. Jordan applies company rate:
   - Effort: 7,050 hours
   - Rate: $150/hour
   - **Quoted Price:** $1,057,500
8. He adds 15% contingency: **Final Quote: $1,216,000**
9. System generates SOW PDF with:
   - Functional requirements summary
   - Function point breakdown
   - Timeline: 9 months (7,050 hours / 40 hours/week / 5 devs = 35 weeks)
   - Payment milestones (25% upfront, 25% at design complete, 25% at beta, 25% at launch)
10. Jordan presents to customer and wins deal

**Postconditions:**
- Professional SOW generated
- Pricing is competitive and profitable
- Timeline is realistic

**Alternative Flows:**
- **A1:** Customer negotiates → Jordan reduces scope to hit budget
- **A2:** Customer requests fixed-price → Jordan adds 25% contingency

**Acceptance Criteria:**
- [ ] Function point calculator with guided wizard
- [ ] SOW template with company branding
- [ ] Payment milestone options
- [ ] Timeline as Gantt chart
- [ ] PDF generation in <10s

**User Story:**
```
As a Sales Engineer,
I want to generate customer quotes from function points,
So that I can respond to RFPs quickly with accurate pricing.

Acceptance:
- Function point wizard (guided questions)
- Auto-convert FP to effort and cost
- SOW template with timeline and milestones
- Professional PDF in <10s
```

---

### UC-5: Improve Estimates with Historical Data

**Actor:** Project Manager (Sarah)
**Goal:** Use past project data to calibrate new estimates

**Preconditions:**
- 15 completed projects in database
- Sarah is estimating a similar new project

**Main Flow:**

1. Sarah starts new estimate for "Mobile App - Fitness Tracker"
2. She selects "Parametric Model (Historical)"
3. System prompts for project attributes:
   - Domain: Mobile App
   - Platform: iOS + Android
   - Team Size: 3 developers
   - Size Estimate: 20K LOC
4. System searches historical database for similar projects:
   - Filters: Domain = Mobile App, Team Size = 2-5
   - Finds 5 matching projects:
     ```
     Project A: 18K LOC, 4 devs, 1200 hours actual
     Project B: 25K LOC, 3 devs, 1680 hours actual
     Project C: 15K LOC, 2 devs, 960 hours actual
     Project D: 22K LOC, 4 devs, 1440 hours actual
     Project E: 19K LOC, 3 devs, 1260 hours actual
     ```
5. System builds linear regression model:
   - Formula: Effort = 45 + (60 × KLOC)
   - R² = 0.89 (good fit)
6. System predicts for 20K LOC project:
   - **Estimated Effort:** 1,245 hours (±15%)
   - **Confidence Interval:** 1,060 - 1,430 hours
7. Sarah reviews similar projects and trusts the estimate
8. She generates budget using parametric estimate
9. After project completes (actual: 1,310 hours), system updates model

**Postconditions:**
- Estimate is calibrated to company's historical performance
- Model improves with each completed project
- Sarah has confidence in accuracy

**Alternative Flows:**
- **A1:** No similar projects found → System falls back to COCOMO
- **A2:** Model fit is poor (R² < 0.5) → System warns and suggests manual review

**Acceptance Criteria:**
- [ ] Historical database with 10+ projects
- [ ] Similarity filters (domain, size, team)
- [ ] Regression model with R² displayed
- [ ] Confidence interval based on model fit
- [ ] Model auto-updates with new actuals

**User Story:**
```
As a Project Manager,
I want to estimate using historical project data,
So that my estimates reflect our team's actual performance.

Acceptance:
- Search historical projects by similarity
- Build regression model from 5+ projects
- Show confidence interval based on fit
- Auto-update model with new actuals
```

---

## Data Model

### Entity-Relationship Diagram (ERD)

```
┌─────────────────┐
│    projects     │
├─────────────────┤
│ id (PK)         │
│ name            │
│ description     │
│ domain          │
│ status          │
│ created_at      │
│ updated_at      │
│ created_by_id   │◄────┐
└─────────────────┘     │
        │               │
        │ 1:N           │
        ▼               │
┌─────────────────┐     │
│   estimates     │     │
├─────────────────┤     │
│ id (PK)         │     │
│ project_id (FK) │     │
│ method          │     │
│ inputs (JSON)   │     │
│ outputs (JSON)  │     │
│ created_at      │     │
│ created_by_id   │─────┘
└─────────────────┘
        │
        │ 1:1
        ▼
┌─────────────────┐
│    actuals      │
├─────────────────┤
│ id (PK)         │
│ estimate_id(FK) │
│ actual_effort   │
│ actual_cost     │
│ actual_duration │
│ variance_%      │
│ lessons_learned │
│ completed_at    │
└─────────────────┘

┌─────────────────┐
│      users      │
├─────────────────┤
│ id (PK)         │
│ email           │
│ password_hash   │
│ role            │
│ created_at      │
└─────────────────┘

┌─────────────────┐
│historical_data  │
├─────────────────┤
│ id (PK)         │
│ project_id (FK) │
│ domain          │
│ language        │
│ platform        │
│ team_size       │
│ kloc            │
│ function_points │
│ effort_hours    │
│ duration_weeks  │
│ cost_usd        │
│ year            │
└─────────────────┘
```

---

### Schema Details

#### Table: `projects`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique project identifier |
| `name` | VARCHAR(255) | NOT NULL | Project name |
| `description` | TEXT | NULLABLE | Project description |
| `domain` | VARCHAR(50) | NULLABLE | Domain (web, mobile, desktop, embedded, etc.) |
| `status` | ENUM | NOT NULL | Status (planning, active, completed, archived) |
| `created_at` | TIMESTAMP | NOT NULL | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL | Last update timestamp |
| `created_by_id` | UUID | FOREIGN KEY | User who created project |

**Indexes:**
- `idx_projects_status` on `status`
- `idx_projects_created_by` on `created_by_id`

---

#### Table: `estimates`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique estimate identifier |
| `project_id` | UUID | FOREIGN KEY | Associated project |
| `method` | VARCHAR(50) | NOT NULL | Estimation method (cocomo, wbs, velocity, function_points, three_point, parametric) |
| `inputs` | JSON | NOT NULL | Estimation inputs (method-specific) |
| `outputs` | JSON | NOT NULL | Estimation results (effort, cost, duration, etc.) |
| `created_at` | TIMESTAMP | NOT NULL | Creation timestamp |
| `created_by_id` | UUID | FOREIGN KEY | User who created estimate |

**Indexes:**
- `idx_estimates_project_id` on `project_id`
- `idx_estimates_method` on `method`

**Inputs JSON Schema (COCOMO example):**
```json
{
  "size_kloc": 50,
  "language": "java",
  "scale_factors": {
    "precedentedness": 3,
    "development_flexibility": 4,
    "architecture_risk_resolution": 3,
    "team_cohesion": 4,
    "process_maturity": 3
  },
  "effort_multipliers": {
    "required_reliability": 1.0,
    "database_size": 1.2,
    "product_complexity": 1.3,
    "analyst_capability": 0.85,
    "programmer_capability": 0.9
  }
}
```

**Outputs JSON Schema:**
```json
{
  "effort_person_months": 140,
  "effort_hours": 22400,
  "duration_months": 18,
  "team_size": 8,
  "cost_usd": 168000,
  "confidence_interval": {
    "low": 134000,
    "high": 202000
  }
}
```

---

#### Table: `actuals`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique actual identifier |
| `estimate_id` | UUID | FOREIGN KEY | Associated estimate |
| `actual_effort` | INTEGER | NOT NULL | Actual effort in hours |
| `actual_cost` | DECIMAL(10,2) | NOT NULL | Actual cost in USD |
| `actual_duration` | INTEGER | NOT NULL | Actual duration in days |
| `variance_percent` | DECIMAL(5,2) | COMPUTED | (actual - estimate) / estimate * 100 |
| `lessons_learned` | TEXT | NULLABLE | Post-mortem notes |
| `completed_at` | TIMESTAMP | NOT NULL | Project completion date |

**Indexes:**
- `idx_actuals_estimate_id` on `estimate_id`

---

#### Table: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `role` | ENUM | NOT NULL | Role (admin, pm, developer, viewer) |
| `created_at` | TIMESTAMP | NOT NULL | Account creation date |

**Indexes:**
- `idx_users_email` on `email`

---

#### Table: `historical_data`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique record identifier |
| `project_id` | UUID | FOREIGN KEY | Associated project (if applicable) |
| `domain` | VARCHAR(50) | NOT NULL | Domain (web, mobile, etc.) |
| `language` | VARCHAR(50) | NOT NULL | Primary language (python, java, etc.) |
| `platform` | VARCHAR(50) | NULLABLE | Platform (cloud, on-prem, etc.) |
| `team_size` | INTEGER | NOT NULL | Number of developers |
| `kloc` | DECIMAL(10,2) | NULLABLE | Lines of code (thousands) |
| `function_points` | INTEGER | NULLABLE | Function points |
| `effort_hours` | INTEGER | NOT NULL | Total effort in hours |
| `duration_weeks` | INTEGER | NOT NULL | Total duration in weeks |
| `cost_usd` | DECIMAL(10,2) | NOT NULL | Total cost in USD |
| `year` | INTEGER | NOT NULL | Year project completed |

**Indexes:**
- `idx_historical_domain` on `domain`
- `idx_historical_language` on `language`
- `idx_historical_team_size` on `team_size`

**Populated with:**
- Internal AZ1.AI projects
- Anonymized customer projects (with permission)
- Public datasets (ISBSG, NASA COCOMO)

---

## API Specification

### OpenAPI 3.1 Overview

**Base URL:** `https://api.coditect.ai/estimation/v1`
**Authentication:** Bearer token (JWT)
**Content-Type:** `application/json`

---

### Endpoints

#### POST `/estimates`

**Purpose:** Create new estimate

**Request Body:**
```json
{
  "project_id": "uuid",
  "method": "cocomo" | "wbs" | "velocity" | "function_points" | "three_point" | "parametric",
  "inputs": {
    // Method-specific inputs (see data model)
  }
}
```

**Response (201 Created):**
```json
{
  "estimate_id": "uuid",
  "project_id": "uuid",
  "method": "cocomo",
  "outputs": {
    "effort_hours": 22400,
    "cost_usd": 168000,
    "duration_months": 18,
    "team_size": 8,
    "confidence_interval": {
      "low": 134000,
      "high": 202000
    }
  },
  "created_at": "2025-11-22T10:30:00Z"
}
```

**Error Codes:**
- `400 Bad Request` - Invalid inputs
- `401 Unauthorized` - Missing/invalid token
- `404 Not Found` - Project not found

---

#### GET `/estimates/{estimate_id}`

**Purpose:** Retrieve existing estimate

**Response (200 OK):**
```json
{
  "estimate_id": "uuid",
  "project_id": "uuid",
  "method": "cocomo",
  "inputs": { /* ... */ },
  "outputs": { /* ... */ },
  "created_at": "2025-11-22T10:30:00Z"
}
```

---

#### POST `/estimates/{estimate_id}/actuals`

**Purpose:** Record actual results for completed project

**Request Body:**
```json
{
  "actual_effort": 24000,
  "actual_cost": 185000,
  "actual_duration": 20,
  "lessons_learned": "Underestimated database complexity"
}
```

**Response (201 Created):**
```json
{
  "actual_id": "uuid",
  "estimate_id": "uuid",
  "variance_percent": 10.5,
  "completed_at": "2025-11-22T10:30:00Z"
}
```

---

#### POST `/analyze/codebase`

**Purpose:** Analyze existing codebase for LOC and complexity

**Request Body:**
```json
{
  "repository_url": "https://github.com/user/repo",
  "branch": "main"
}
```

**Response (200 OK):**
```json
{
  "total_loc": 125000,
  "languages": {
    "python": 75000,
    "javascript": 35000,
    "html": 15000
  },
  "complexity": {
    "average_cyclomatic": 5.2,
    "high_complexity_files": 12
  },
  "estimated_kloc": 125
}
```

---

#### POST `/reports/{estimate_id}/generate`

**Purpose:** Generate report in specified format

**Request Body:**
```json
{
  "format": "pdf" | "excel" | "markdown" | "json",
  "report_type": "budget" | "timeline" | "risk" | "comparison"
}
```

**Response (200 OK):**
```json
{
  "report_url": "https://api.coditect.ai/reports/uuid.pdf",
  "expires_at": "2025-11-29T10:30:00Z"
}
```

---

#### GET `/historical`

**Purpose:** Query historical project data for parametric models

**Query Parameters:**
- `domain`: Filter by domain (web, mobile, etc.)
- `language`: Filter by language
- `team_size_min`: Minimum team size
- `team_size_max`: Maximum team size
- `year_min`: Minimum year

**Response (200 OK):**
```json
{
  "projects": [
    {
      "id": "uuid",
      "domain": "web",
      "language": "python",
      "team_size": 4,
      "kloc": 50,
      "effort_hours": 8000,
      "duration_weeks": 24,
      "cost_usd": 120000,
      "year": 2024
    }
  ],
  "count": 15,
  "regression_model": {
    "formula": "effort = 45 + (60 * kloc)",
    "r_squared": 0.89
  }
}
```

---

### Rate Limiting

- **Free Tier:** 100 requests/day
- **Paid Tier:** 10,000 requests/day
- **Enterprise:** Unlimited

**Headers:**
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Timestamp when limit resets

---

## Reporting Requirements

### Report 1: Budget Estimate Report

**Template:** Professional PDF with AZ1.AI/CODITECT branding

**Sections:**

1. **Executive Summary** (1 page)
   - Project name and description
   - Total cost estimate with confidence interval
   - Timeline estimate
   - Key assumptions and risks

2. **Estimation Methodology** (0.5 page)
   - Method used (e.g., COCOMO II)
   - Why this method was chosen
   - Input parameters

3. **Cost Breakdown** (1-2 pages)
   - By role (developer, QA, PM, etc.)
   - By phase (design, development, testing, deployment)
   - By module/feature
   - Overhead factors (testing, PM, infrastructure, rework)

4. **Timeline Projection** (1 page)
   - Total duration (weeks/months)
   - Key milestones
   - Critical path items
   - Resource allocation

5. **Risk Analysis** (1 page)
   - Risk factors identified
   - Probability × Impact assessment
   - Mitigation recommendations
   - Contingency allocation

6. **Assumptions & Disclaimers** (0.5 page)
   - Team composition assumptions
   - Technology stack assumptions
   - Availability assumptions
   - Exclusions (what's not included)

7. **Appendix** (optional)
   - Detailed WBS
   - Historical data references
   - Sensitivity analysis

**Format:**
- PDF (primary)
- Markdown (for version control)
- HTML (for embedding in dashboards)

**Branding:**
- AZ1.AI logo in header
- CODITECT footer
- Professional color scheme (blue/gray)

---

### Report 2: Timeline Projection (Gantt Chart)

**Visualization:** Interactive Gantt chart

**Features:**
- Horizontal bars for tasks/phases
- Dependencies shown as arrows
- Critical path highlighted in red
- Milestones as diamonds
- Resource allocation shown
- Today marker (current date line)

**Interactivity (Web UI):**
- Hover to see task details
- Click to edit (if permissions allow)
- Zoom in/out on timeline
- Filter by resource/phase

**Export Formats:**
- PNG image (for presentations)
- HTML (interactive, embeddable)
- Microsoft Project XML (for editing in MS Project)
- JSON (for API integration)

**Libraries:**
- D3.js or Mermaid for rendering
- FullCalendar or Gantt-task-react

---

### Report 3: Risk Analysis Report

**Purpose:** Identify and quantify project risks

**Sections:**

1. **Risk Score Summary**
   - Overall risk score (0-100)
   - Risk level (Low/Medium/High)
   - Comparison to similar projects

2. **Risk Factors**
   - Technical complexity
   - Team experience
   - Schedule pressure
   - Requirement uncertainty
   - External dependencies

3. **Probability × Impact Matrix**
   - Visual matrix (4x4 grid)
   - Risks plotted by probability and impact
   - Color-coded (green/yellow/red)

4. **Sensitivity Analysis**
   - Tornado chart showing factor impact
   - "What-if" scenarios
   - Most influential factors highlighted

5. **Mitigation Recommendations**
   - Top 5 risks with mitigation strategies
   - Contingency allocation
   - Risk monitoring plan

**Visualization:**
- Probability distribution curve
- Monte Carlo simulation results
- Risk heatmap

---

### Report 4: Estimate vs. Actual Comparison

**Purpose:** Track estimation accuracy for continuous improvement

**Sections:**

1. **Variance Summary**
   - Original estimate vs. actual
   - Variance % (over/under)
   - Breakdown by effort, cost, duration

2. **Breakdown by Phase/Module**
   - Table showing estimate vs. actual for each phase
   - Identify where estimation was off

3. **Root Cause Analysis**
   - What was underestimated? (testing, complexity, rework)
   - What was overestimated? (learning curve, reuse)
   - Patterns across projects

4. **Lessons Learned**
   - Free-form notes from PM
   - Recommendations for future estimates

5. **Historical Accuracy Trends**
   - Chart showing accuracy over time
   - Goal: Improve from ±50% to ±20%

**Update Workflow:**
- PM marks project complete
- Enters actual effort/cost/duration
- System calculates variance
- PM writes lessons learned
- Data added to historical database

---

### Report 5: Export Formats

**All reports support:**

- **PDF:** Professional documents for executives
- **Excel:** Editable spreadsheets for finance teams
- **JSON:** API integration with other tools
- **Markdown:** Version-controlled estimates in git
- **CSV:** Data export for analysis

**Export Features:**
- Preserve formatting (headers, colors, logos)
- Include metadata (created date, author, version)
- Compress large exports (ZIP)
- Password-protect sensitive reports (optional)

---

## Integration Plan

### Integration with CODITECT Ecosystem

#### INT-1: Slash Command (`/estimate`)

**Purpose:** Quick estimation from Claude Code workflow

**Usage:**
```
/estimate cocomo --kloc 50 --language java
/estimate wbs --file tasks.csv
/estimate jira PROJECT-123
```

**Implementation:**
- Add to `coditect-core/commands/estimate.md`
- CLI wrapper calls estimation engine API or local script
- Output formatted as Markdown in Claude response

**Acceptance Criteria:**
- [ ] Command registered in CODITECT commands/
- [ ] Help text with examples
- [ ] Output is human-readable
- [ ] Integrates with current project context

---

#### INT-2: Skill (`estimation-calculator`)

**Purpose:** Reusable estimation patterns for other agents

**Skill Definition:**
```yaml
name: estimation-calculator
category: project-management
description: |
  Calculate software project estimates using COCOMO, WBS, Function Points,
  Story Points, Three-Point, or Parametric models.
inputs:
  - method: Estimation method
  - project_attributes: Size, complexity, team, etc.
outputs:
  - effort: Estimated effort in hours
  - cost: Estimated cost in USD
  - duration: Estimated duration in weeks
  - confidence_interval: Range of possible outcomes
```

**Usage by Agents:**
- `project-manager` agent uses for budget creation
- `budget-analyst` agent uses for validation
- `sales-engineer` agent uses for quote generation

---

#### INT-3: Agent (`budget-analyst`)

**Purpose:** Specialized agent for financial analysis and estimation

**Agent Definition:**
```yaml
name: budget-analyst
category: finance
expertise:
  - Software cost estimation
  - Budget validation
  - Financial modeling
  - ROI analysis
capabilities:
  - Estimate project costs using multiple methods
  - Validate vendor quotes
  - Generate budget reports
  - Track estimate vs. actual
  - Recommend cost optimizations
tools:
  - estimation-calculator skill
  - /estimate command
  - Historical project database
```

**Example Invocation:**
```
Use budget-analyst subagent to create a budget estimate for
the Customer Portal Redesign project with 50K LOC Java codebase.
```

**Agent Response:**
- Asks clarifying questions (team size, timeline, complexity)
- Runs multiple estimation methods (COCOMO, historical)
- Compares results and explains differences
- Generates professional budget report
- Recommends contingency percentage

**Acceptance Criteria:**
- [ ] Agent definition in `coditect-core/agents/budget-analyst.md`
- [ ] Responds to estimation requests
- [ ] Uses estimation-calculator skill
- [ ] Generates professional reports
- [ ] Explains methodology clearly

---

#### INT-4: Script (`estimate-project.py`)

**Purpose:** CLI tool for estimation outside Claude workflow

**Location:** `coditect-ops-estimation-engine/scripts/estimate-project.py`

**Usage:**
```bash
# COCOMO estimation
python estimate-project.py cocomo \
  --kloc 50 \
  --language java \
  --output budget.pdf

# WBS estimation
python estimate-project.py wbs \
  --file tasks.csv \
  --rate 120 \
  --output budget.pdf

# Codebase analysis
python estimate-project.py analyze \
  --repo /path/to/repo \
  --method cocomo
```

**Acceptance Criteria:**
- [ ] Supports all 6 estimation methods
- [ ] CLI help text with examples
- [ ] Output to PDF, JSON, CSV
- [ ] Progress indicators for long operations
- [ ] Exit codes for CI/CD integration

---

#### INT-5: Script (`analyze-codebase.py`)

**Purpose:** Automated LOC and complexity analysis

**Usage:**
```bash
# Analyze local repository
python analyze-codebase.py /path/to/repo

# Analyze GitHub repository
python analyze-codebase.py --github https://github.com/user/repo

# Output as JSON for API integration
python analyze-codebase.py /path/to/repo --format json
```

**Output:**
```json
{
  "total_loc": 125000,
  "languages": {
    "python": 75000,
    "javascript": 35000,
    "html": 15000
  },
  "complexity": {
    "average_cyclomatic": 5.2,
    "high_complexity_files": [
      "src/engine/calculator.py (complexity: 18)",
      "src/api/routes.py (complexity: 15)"
    ]
  },
  "estimated_kloc": 125,
  "suggested_cocomo_inputs": {
    "size_kloc": 125,
    "complexity_multiplier": 1.2
  }
}
```

**Acceptance Criteria:**
- [ ] Integrates `cloc` as subprocess
- [ ] Parses and enriches output
- [ ] Identifies high-complexity files
- [ ] Suggests estimation inputs
- [ ] Works on local and remote repos

---

### Integration with External Systems

#### INT-6: GitHub API Integration

**Purpose:** Import codebase stats and PR data

**Authentication:** Personal Access Token (PAT)

**Endpoints Used:**
- `GET /repos/{owner}/{repo}` - Repo metadata
- `GET /repos/{owner}/{repo}/stats/contributors` - LOC by contributor
- `GET /repos/{owner}/{repo}/pulls` - Pull request stats

**Data Imported:**
- Total LOC (from contributors endpoint)
- Language distribution
- Commit frequency
- PR cycle time (open to merge)

**Acceptance Criteria:**
- [ ] OAuth or PAT authentication
- [ ] Fetch repository statistics
- [ ] Calculate average PR cycle time
- [ ] Use for velocity estimation

---

#### INT-7: JIRA/Linear Integration

**Purpose:** Import story points and velocity

**Authentication:** API token

**JIRA Endpoints:**
- `GET /rest/api/3/search` - Search for issues
- `GET /rest/agile/1.0/board/{boardId}/sprint` - Get sprints
- `GET /rest/agile/1.0/sprint/{sprintId}/issue` - Get issues in sprint

**Data Imported:**
- User stories with story points
- Sprint velocity (points completed per sprint)
- Epic hierarchy

**Acceptance Criteria:**
- [ ] JIRA Cloud API integration
- [ ] Fetch story points from custom field
- [ ] Calculate velocity from last 6 sprints
- [ ] Support epic rollup

---

### CODITECT Cloud Backend Integration (Optional)

**Purpose:** Store estimates in cloud for multi-user access

**Architecture:**
```
coditect-ops-estimation-engine (this repo)
    ↓ API calls (optional)
coditect-cloud-backend
    ↓ Database storage
PostgreSQL (cloud-hosted)
```

**Benefits:**
- Multi-user access
- Centralized historical database
- Team collaboration on estimates
- Cloud backup and sync

**Implementation:**
- Estimation engine checks for cloud API URL in config
- If present, syncs estimates to cloud
- If absent, stores locally in SQLite

**Acceptance Criteria:**
- [ ] Optional cloud sync configuration
- [ ] Syncs estimates on save
- [ ] Conflict resolution (local vs. cloud)
- [ ] Offline mode with sync-on-reconnect

---

## Success Metrics

### Primary Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| **Estimation Accuracy** | ±20% variance | Compare estimate vs. actual for 10+ projects |
| **Time Savings** | 80% reduction | User survey: time to create estimate |
| **User Adoption** | 50+ active users | Monthly active users in first 6 months |
| **Report Generation** | <10s for PDF | Performance monitoring |
| **API Uptime** | 99.5% | Prometheus uptime tracking |

---

### Secondary Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| **API Usage** | 1,000+ estimates/month | API request logs |
| **Historical Database Growth** | 100+ projects in Year 1 | Database record count |
| **Customer Satisfaction** | NPS >50 | User survey |
| **Bug Rate** | <5 critical bugs/quarter | GitHub issue tracking |
| **Documentation Completeness** | 100% API endpoints documented | OpenAPI spec coverage |

---

### Success Criteria by Phase

**Phase 1: Alpha (Weeks 1-4)**
- [ ] All 6 estimation methods implemented
- [ ] CLI tool functional
- [ ] Basic API endpoints working
- [ ] 5+ internal projects estimated

**Phase 2: Beta (Weeks 5-8)**
- [ ] Web UI functional
- [ ] PDF reports generated
- [ ] 10+ beta testers using tool
- [ ] Historical database with 20+ projects

**Phase 3: Production (Weeks 9-12)**
- [ ] Public API launch
- [ ] CODITECT integration complete
- [ ] 50+ active users
- [ ] Documentation complete

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **COCOMO calculation errors** | Medium | High | Validate against reference tools (COPSEMO) |
| **Codebase analysis failures** | Medium | Medium | Fallback to manual LOC input |
| **API performance issues** | Low | High | Load testing, caching, horizontal scaling |
| **Database scalability** | Low | Medium | Partition historical data, add indexes |
| **Integration bugs (JIRA/GitHub)** | Medium | Medium | Comprehensive API mocking and testing |

---

### Business Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Low user adoption** | Medium | High | Strong CODITECT integration, user training |
| **Competitors with similar tools** | High | Medium | Differentiate with AI agent integration |
| **Inaccurate estimates damage reputation** | Medium | High | Confidence intervals, clear disclaimers |
| **Insufficient historical data** | Medium | Medium | Seed with public datasets (ISBSG, NASA) |
| **Pricing model unclear** | Low | Medium | Start free for CODITECT users, enterprise upsell |

---

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Maintenance burden** | Medium | Medium | Automated testing, CI/CD, monitoring |
| **Security vulnerabilities** | Low | High | Regular audits, OWASP compliance |
| **Data privacy concerns** | Low | High | Encrypt sensitive data, GDPR compliance |
| **Dependency on external APIs** | Medium | Medium | Rate limiting, graceful degradation |

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)

**Goal:** Core estimation engine with CLI

**Deliverables:**
- [ ] COCOMO II calculator (Python)
- [ ] Bottom-Up WBS estimator
- [ ] Story Points + Velocity calculator
- [ ] Function Point Analysis
- [ ] Three-Point Estimation (PERT)
- [ ] Parametric model (historical regression)
- [ ] CLI tool with all methods
- [ ] SQLite database schema
- [ ] Unit tests (80% coverage)

**Team:**
- 1 Backend Developer (Python)
- 1 QA Engineer (Testing)

**Duration:** 4 weeks
**Budget:** $40K (1 dev @ $150/hr × 160 hrs/month × 1 month + QA @ $100/hr × 80 hrs)

---

### Phase 2: API & Web UI (Weeks 5-8)

**Goal:** REST API and web interface

**Deliverables:**
- [ ] FastAPI REST endpoints
- [ ] OpenAPI 3.1 documentation
- [ ] React/TypeScript web UI
- [ ] Estimation form wizards
- [ ] Charts and visualizations
- [ ] PDF report generation
- [ ] JWT authentication
- [ ] Integration tests

**Team:**
- 1 Backend Developer (FastAPI)
- 1 Frontend Developer (React)
- 1 QA Engineer

**Duration:** 4 weeks
**Budget:** $60K (2 devs @ $150/hr × 160 hrs + QA @ $100/hr × 160 hrs)

---

### Phase 3: Integrations (Weeks 9-12)

**Goal:** GitHub, JIRA, and CODITECT integrations

**Deliverables:**
- [ ] Automated codebase analysis (`cloc`, `tokei`)
- [ ] Complexity analysis (cyclomatic, Halstead)
- [ ] GitHub API integration
- [ ] JIRA/Linear API integration
- [ ] CODITECT slash command (`/estimate`)
- [ ] CODITECT skill (`estimation-calculator`)
- [ ] CODITECT agent (`budget-analyst`)
- [ ] Historical database seeding (50+ projects)

**Team:**
- 1 Integration Engineer (APIs)
- 1 CODITECT Specialist (Agent/Skills)
- 1 Data Engineer (Historical DB)

**Duration:** 4 weeks
**Budget:** $50K (3 engineers @ $150/hr × 133 hrs each)

---

### Phase 4: Reporting & Polish (Weeks 13-16)

**Goal:** Production-ready reports and deployment

**Deliverables:**
- [ ] Budget estimate report (PDF)
- [ ] Timeline Gantt chart (interactive)
- [ ] Risk analysis report
- [ ] Estimate vs. actual comparison
- [ ] Export formats (Excel, JSON, CSV, Markdown)
- [ ] Docker deployment
- [ ] Kubernetes manifests
- [ ] Monitoring (Prometheus, Grafana)
- [ ] Documentation (user guide, API reference)

**Team:**
- 1 Backend Developer (Reporting)
- 1 Frontend Developer (Visualizations)
- 1 DevOps Engineer (Deployment)
- 1 Technical Writer (Docs)

**Duration:** 4 weeks
**Budget:** $70K (4 people @ $150/hr × 100 hrs each, tech writer @ $100/hr)

---

### Total Implementation

**Duration:** 16 weeks (4 months)
**Budget:** $220K
**Team:** 4-6 engineers (rotating)

---

## Budget & Resources

### Development Budget Breakdown

| Phase | Duration | Team | Cost |
|-------|----------|------|------|
| **Phase 1: Foundation** | 4 weeks | 1 Backend Dev + 1 QA | $40K |
| **Phase 2: API & UI** | 4 weeks | 1 Backend + 1 Frontend + 1 QA | $60K |
| **Phase 3: Integrations** | 4 weeks | 1 Integration + 1 CODITECT + 1 Data | $50K |
| **Phase 4: Reporting** | 4 weeks | 2 Devs + 1 DevOps + 1 Writer | $70K |
| **Total Development** | **16 weeks** | **4-6 engineers** | **$220K** |

---

### Ongoing Costs (Annual)

| Category | Cost/Year | Notes |
|----------|-----------|-------|
| **Cloud Hosting** | $3,600 | GCP: VM, database, storage |
| **API Costs** | $1,200 | GitHub, JIRA API usage |
| **Monitoring** | $600 | Prometheus Cloud, Grafana |
| **Support & Maintenance** | $30K | 20% dev time for bugs/updates |
| **Total Ongoing** | **$35,400/year** | |

---

### Resource Requirements

**Engineers:**
- **Backend Developer (Python):** 320 hours
- **Frontend Developer (React):** 160 hours
- **Integration Engineer:** 160 hours
- **CODITECT Specialist:** 160 hours
- **Data Engineer:** 160 hours
- **DevOps Engineer:** 160 hours
- **QA Engineer:** 320 hours
- **Technical Writer:** 80 hours

**Total:** 1,520 engineering hours over 16 weeks

---

### Revenue Projection (Optional)

**Pricing Model:**

- **Free Tier:** 10 estimates/month (for CODITECT users)
- **Pro Tier:** $49/month - 100 estimates/month, advanced reports
- **Enterprise Tier:** $499/month - Unlimited, multi-user, API access, cloud hosting

**Projected Revenue (Year 1):**

- Month 1-3: Beta (free)
- Month 4-6: 50 Pro users × $49 = $2,450/month
- Month 7-12: 150 Pro users × $49 + 5 Enterprise × $499 = $9,845/month

**Year 1 Total Revenue:** ~$50K
**Break-Even:** Month 18 (if standalone product)

**Note:** Likely bundled with CODITECT Core as value-add, not standalone revenue.

---

## Appendices

### Appendix A: Industry Research Sources

**Estimation Methodologies:**
- COCOMO II: http://csse.usc.edu/csse/research/COCOMOII/cocomo_main.html
- ISBSG: https://www.isbsg.org/ (historical data benchmarks)
- Function Point Users Group (IFPUG): https://www.ifpug.org/
- Agile Estimation (Story Points): Mike Cohn, "Agile Estimating and Planning"

**Tools & Libraries:**
- cloc: https://github.com/AlDanial/cloc
- tokei: https://github.com/XAMPPRocky/tokei
- Radon (Python complexity): https://radon.readthedocs.io/
- scikit-learn: https://scikit-learn.org/

---

### Appendix B: Sample Historical Data

**Dataset:** NASA COCOMO Historical Projects (anonymized)

| Project | Domain | Language | Team | KLOC | Effort (hrs) | Duration (weeks) | Cost (USD) |
|---------|--------|----------|------|------|--------------|------------------|------------|
| Project A | Embedded | C | 5 | 30 | 12000 | 48 | $180K |
| Project B | Web | Python | 3 | 15 | 4500 | 24 | $67K |
| Project C | Mobile | Swift | 4 | 20 | 7200 | 32 | $108K |
| Project D | Desktop | Java | 6 | 50 | 18000 | 56 | $270K |
| Project E | Web | JavaScript | 2 | 10 | 3000 | 20 | $45K |

**Usage:** Seed historical database for parametric models

---

### Appendix C: Glossary

- **COCOMO:** Constructive Cost Model - Parametric software estimation model
- **KLOC:** Thousands of Lines of Code
- **Function Points:** Language-agnostic measure of software functionality
- **WBS:** Work Breakdown Structure - Hierarchical task decomposition
- **Story Points:** Relative measure of effort in Agile development
- **PERT:** Program Evaluation and Review Technique - Three-point estimation
- **Cyclomatic Complexity:** Measure of code complexity based on control flow
- **Halstead Metrics:** Software complexity metrics (volume, difficulty, effort)
- **Blended Rate:** Average hourly rate across all roles on project
- **Overhead:** Indirect costs (testing, PM, infrastructure, rework)
- **Contingency:** Risk buffer added to estimates

---

## Document Control

**Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-22 | Hal Casteel | Initial requirements document |

**Approvals:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **CEO** | Hal Casteel | _______________ | _______ |
| **CTO** | Hal Casteel | _______________ | _______ |
| **Product Lead** | ___________ | _______________ | _______ |

**Next Steps:**

1. **Review:** Stakeholder review and approval (1 week)
2. **Planning:** Detailed technical design document (1 week)
3. **Kickoff:** Phase 1 implementation start (Week 3)

---

**END OF DOCUMENT**

---

**Contact:**
- **Document Owner:** Hal Casteel (hal@az1.ai)
- **Repository:** `coditect-ops-estimation-engine`
- **Organization:** AZ1.AI INC
- **License:** MIT (open-source after production launch)

---

© 2025 AZ1.AI INC. All Rights Reserved.
