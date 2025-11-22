# CODITECT Glossary

> **Complete reference of terms, concepts, and acronyms**
> **Your quick-lookup guide for CODITECT terminology**
> **Last Updated:** 2025-11-16

---

## Table of Contents

- [Core Concepts](#core-concepts)
- [CODITECT Components](#coditect-components)
- [Business Discovery](#business-discovery)
- [Technical Architecture](#technical-architecture)
- [Project Management](#project-management)
- [Claude Code Platform](#claude-code-platform)
- [Development Methodologies](#development-methodologies)
- [Acronyms & Abbreviations](#acronyms--abbreviations)

---

## Core Concepts

### CODITECT
**COD**e + Arch**ITECT** - A comprehensive multi-agent AI framework for systematic software project specification and development. Consists of 50 specialized agents, 189 skills, 72 commands, and automation scripts built on top of Claude Code.

### Agent
A specialized AI assistant focused on a specific domain or task. CODITECT has 49 agents across 8 domains (Research, Development, Infrastructure, Testing, Architecture, Business, Orchestration, Quality).

**Example:** `competitive-market-analyst` agent specializes in market research and competitive analysis.

### Skill
A reusable capability or tool that agents can access. CODITECT includes 189 skills ranging from database queries to communication protocols.

**Example:** `rust-backend-patterns` skill provides Rust development best practices.

### Command
A slash command that expands into a full prompt. CODITECT has 72 custom commands for workflows.

**Example:** `/market-research` expands into a prompt for competitive market analysis.

### Operator
A person trained to use CODITECT effectively. Operators orchestrate agents to create comprehensive project specifications.

**Certification Levels:** Foundation → Business → Technical → Project → Expert

### Task Tool Pattern
The ONLY verified method to invoke CODITECT agents. Always uses `subagent_type="general-purpose"` with a prompt that starts "Use [agent-name] subagent to...".

**Example:**
```python
Task(
    subagent_type="general-purpose",
    prompt="Use competitive-market-analyst subagent to research AI IDE market"
)
```

---

## CODITECT Components

### `.coditect/` Directory
The core CODITECT framework directory containing all agents, skills, commands, and scripts. Usually added as a git submodule from `coditect-core` repository.

**Structure:**
```
.coditect/
├── agents/          # 50 specialized agents
├── skills/          # 189 reusable skills
├── commands/        # 72 slash commands
├── scripts/         # Automation scripts
├── orchestration/   # Multi-agent coordination
└── templates/       # Document templates
```

### `.claude` Symlink
A symbolic link from `.claude` to `.coditect`. Required because Claude Code expects a `.claude` directory, but CODITECT uses `.coditect` as the canonical name.

**Command:** `ln -s .coditect .claude`

### MEMORY-CONTEXT System
A directory structure for preserving knowledge across sessions to prevent catastrophic forgetting.

**Structure:**
```
MEMORY-CONTEXT/
├── sessions/        # Session summaries
├── decisions/       # ADRs
├── business/        # Business research
└── technical/       # Technical research
```

### Orchestrator
A special agent that coordinates multiple agents in complex workflows. Manages task dependencies and sequencing.

**Example:** Orchestrator can coordinate `competitive-market-analyst` → `business-intelligence-analyst` → `senior-architect` workflow.

---

## Business Discovery

### TAM (Total Addressable Market)
The total revenue opportunity available if a product achieved 100% market share in all possible markets globally.

**Example:** "All 27M software developers worldwide × $100/year = $2.7B TAM"

### SAM (Serviceable Available Market)
The portion of TAM that your product can realistically serve based on your business model and geographic reach.

**Example:** "English-speaking developers in startups (5M) × $100/year = $500M SAM"

### SOM (Serviceable Obtainable Market)
The portion of SAM you can realistically capture in the short term (typically Year 1-3).

**Example:** "0.1% of SAM = 5,000 customers × $100/year = $500K SOM Year 1"

### Value Proposition
A clear statement of the tangible benefits and unique value your product delivers to customers that differentiates it from alternatives.

**Formula:** [Product] helps [Target Customer] [Solve Problem] by [Unique Approach] unlike [Alternatives].

### ICP (Ideal Customer Profile)
A detailed description of the perfect customer for your product across three dimensions:
1. **Demographics:** Company size, industry, revenue, role, geography
2. **Psychographics:** Pain points, goals, values, decision process
3. **Behavioral:** Current tools, budget, buying triggers, information sources

### PMF (Product-Market Fit)
The degree to which a product satisfies strong market demand. CODITECT uses the 7-Fit Framework with dimensions: Problem-Solution, Product-Market, Product-Channel, Channel-Model, Model-Market, Market-Value, Value-Company.

### GTM (Go-to-Market)
The strategy for bringing a product to market and reaching target customers. Four primary motions:
- **PLG:** Product-Led Growth (self-serve, free trial)
- **SLG:** Sales-Led Growth (sales team, enterprise)
- **MLG:** Marketing-Led Growth (content, demand gen)
- **Partner-Led Growth:** (channel partners, integrations)

### Competitive Analysis
Systematic evaluation of competitors including their products, positioning, pricing, strengths, weaknesses, and market share.

**Output:** Competitive matrix comparing features, pricing, target customers, and differentiators.

### Business Model Canvas
A strategic management template with 9 blocks: Customer Segments, Value Propositions, Channels, Customer Relationships, Revenue Streams, Key Resources, Key Activities, Key Partnerships, Cost Structure.

---

## Technical Architecture

### C4 Architecture
A hierarchical approach to software architecture diagrams with four levels:
1. **Context:** System landscape (highest abstraction)
2. **Container:** Applications and data stores
3. **Component:** Modules within containers
4. **Code:** Classes and functions (lowest abstraction)

### ADR (Architecture Decision Record)
A document capturing an important architectural decision, including context, decision made, and consequences.

**Format:**
```markdown
# ADR-XXX: Title

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What factors influenced this decision?]

## Decision
[What was decided?]

## Consequences
[Positive, negative, and neutral outcomes]
```

### SDD (Software Design Document)
A comprehensive document describing the software design including:
- Feature breakdown
- Module architecture
- Data structures
- Algorithms
- Security considerations
- Performance requirements

### TDD (Test Design Document)
A document specifying the testing strategy, test cases, test data, and QA approach for a project.

### ERD (Entity Relationship Diagram)
A visual representation of database schema showing entities (tables), attributes (columns), and relationships (foreign keys).

### API (Application Programming Interface)
A set of protocols and tools for building software applications. CODITECT generates OpenAPI 3.1 specifications.

**REST API:** Representational State Transfer - uses HTTP methods (GET, POST, PUT, DELETE) for CRUD operations.

### Microservices
An architectural style where an application is composed of small, independent services that communicate over a network.

**Alternative:** Monolithic architecture - single, unified application.

### Database Schema
The structure of a database including tables, columns, data types, relationships, constraints, and indexes.

**Normalization:** Process of organizing data to reduce redundancy (1NF, 2NF, 3NF, BCNF).

### Technology Stack
The set of technologies used to build an application:
- **Frontend:** React, Vue, Angular
- **Backend:** Node.js, Python, Rust, Go
- **Database:** PostgreSQL, MongoDB, MySQL
- **Infrastructure:** AWS, GCP, Azure, Kubernetes
- **Tools:** Git, Docker, CI/CD

---

## Project Management

### PROJECT-PLAN.md
A comprehensive project planning document including:
- Executive summary
- Objectives & success criteria
- Technical architecture
- Development phases
- Timeline & milestones
- Risk assessment
- Resource requirements

**Living Document:** Updated throughout the project lifecycle.

### TASKLIST.md
A granular task tracking document with checkboxes, priorities, time estimates, and phase associations.

**Format:** `- [ ] **[Phase X]** Task description - Priority: HIGH - Est: 8h - Agent: agent-name`

### Checkpoint
A snapshot of project state at a significant milestone including:
- Sprint summary
- Deliverables completed
- Key decisions made
- Lessons learned
- Next steps
- Metrics

**Naming:** `YYYY-MM-DDTHH-MM-SSZ-description.md` (ISO 8601 datetime)

### Sprint
A time-boxed period (typically 1-4 weeks) focused on completing specific objectives. Part of Agile methodology.

**CODITECT Sprints:** Often organized around project phases (Business Discovery, Technical Specification, etc.)

### Phase
A major stage of project development with distinct objectives and deliverables.

**Typical Phases:**
1. Business Discovery
2. Technical Specification
3. Development
4. Testing & QA
5. Deployment
6. Maintenance

### Risk Assessment
Identification and evaluation of potential project risks with mitigation strategies.

**Categories:**
- **Technical:** Technology limitations, complexity
- **Business:** Market changes, competition
- **Resource:** Budget, team capacity
- **Timeline:** Delays, dependencies

### Milestone
A significant event or achievement in project timeline.

**Examples:**
- "Business Discovery Complete"
- "Technical Specification Approved"
- "MVP Launch"
- "Production Deployment"

---

## Claude Code Platform

### Claude Code
Anthropic's official command-line interface for Claude AI. The underlying platform that CODITECT is built upon.

**Features:** File operations, git integration, multi-file context, code generation.

### Context Window
The amount of information Claude can process in a single session. Currently 200,000 tokens (~150,000 words).

**Includes:** Input tokens (messages, file reads) + Output tokens (responses, generated code).

### Token
A unit of text (roughly 4 characters or 3/4 of a word) used to measure context usage.

**Example:** "Hello, world!" = ~4 tokens

### Session
One continuous conversation with Claude Code from start to exit. All context is lost when session ends unless exported.

**Session Lifecycle:**
1. Start Claude Code
2. Accumulate context
3. Export summary before limit
4. Exit
5. New session (no memory of previous)

### Tool
A capability Claude Code can use to interact with the environment.

**Built-in Tools:**
- **Read:** Read file contents
- **Write:** Create new files
- **Edit:** Modify existing files
- **Bash:** Execute shell commands
- **Grep:** Search file contents
- **Glob:** Find files by pattern
- **WebFetch:** Fetch web content
- **WebSearch:** Search the internet
- **Task:** Invoke specialized agents

### Catastrophic Forgetting
When AI loses context from previous sessions, forgetting project decisions, research findings, and architectural choices.

**Prevention:** MEMORY-CONTEXT system with session summaries and ADRs.

### Work Reuse
Strategy of referencing previously completed work instead of re-reading files or re-doing research. Saves tokens and time.

**Example:** "Use MEMORY-CONTEXT/business/market-research-summary.md instead of re-researching the market"

---

## Development Methodologies

### Agile
An iterative approach to software development emphasizing flexibility, collaboration, and continuous delivery.

**Principles:** Working software, customer collaboration, responding to change.

### Waterfall
A sequential development approach with distinct phases: Requirements → Design → Implementation → Testing → Deployment → Maintenance.

**CODITECT Approach:** Hybrid - waterfall for specification, agile for implementation.

### CI/CD (Continuous Integration / Continuous Deployment)
Automated processes for integrating code changes and deploying to production.

**CI:** Automatically build and test code on every commit.
**CD:** Automatically deploy tested code to production.

### DevOps
A culture and set of practices combining software development and IT operations for faster, more reliable releases.

**Tools:** Docker, Kubernetes, Jenkins, GitLab CI, GitHub Actions.

### TDD (Test-Driven Development)
A development approach where tests are written before code.

**Cycle:** Red (write failing test) → Green (make it pass) → Refactor.

### DDD (Domain-Driven Design)
An approach to software design that models software based on the business domain.

**Concepts:** Entities, value objects, aggregates, repositories, domain events.

### SOLID Principles
Five design principles for object-oriented software:
- **S**ingle Responsibility Principle
- **O**pen/Closed Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

---

## Acronyms & Abbreviations

### Project & Business

| Acronym | Full Term | Definition |
|---------|-----------|------------|
| **ADR** | Architecture Decision Record | Document capturing architectural decisions |
| **API** | Application Programming Interface | Set of protocols for building software |
| **B2B** | Business-to-Business | Business selling to other businesses |
| **B2C** | Business-to-Consumer | Business selling directly to consumers |
| **CAC** | Customer Acquisition Cost | Cost to acquire one new customer |
| **CEO** | Chief Executive Officer | Top executive in organization |
| **CTO** | Chief Technology Officer | Top technology executive |
| **GTM** | Go-to-Market | Strategy for bringing product to market |
| **ICP** | Ideal Customer Profile | Description of perfect customer |
| **KPI** | Key Performance Indicator | Metric measuring success |
| **LTV** | Lifetime Value | Total revenue from one customer |
| **MRR** | Monthly Recurring Revenue | Predictable monthly revenue |
| **MVP** | Minimum Viable Product | Simplest version with core value |
| **PMF** | Product-Market Fit | Product satisfying market demand |
| **ROI** | Return on Investment | Profit relative to cost |
| **SAM** | Serviceable Available Market | Reachable portion of TAM |
| **SOM** | Serviceable Obtainable Market | Realistically capturable portion |
| **TAM** | Total Addressable Market | Total market opportunity |
| **VC** | Venture Capital | Investment in startups |

### Technical

| Acronym | Full Term | Definition |
|---------|-----------|------------|
| **ACID** | Atomicity, Consistency, Isolation, Durability | Database transaction properties |
| **API** | Application Programming Interface | Interface for software interaction |
| **AWS** | Amazon Web Services | Cloud computing platform |
| **CDN** | Content Delivery Network | Distributed server network |
| **CLI** | Command-Line Interface | Text-based user interface |
| **CORS** | Cross-Origin Resource Sharing | HTTP header-based mechanism |
| **CRUD** | Create, Read, Update, Delete | Basic database operations |
| **CSS** | Cascading Style Sheets | Styling language for web |
| **DB** | Database | Organized data collection |
| **DNS** | Domain Name System | Internet naming system |
| **ERD** | Entity Relationship Diagram | Database schema visualization |
| **GCP** | Google Cloud Platform | Cloud computing services |
| **HTML** | HyperText Markup Language | Web page structure language |
| **HTTP** | HyperText Transfer Protocol | Web communication protocol |
| **HTTPS** | HTTP Secure | Encrypted HTTP |
| **JSON** | JavaScript Object Notation | Data interchange format |
| **JWT** | JSON Web Token | Authentication token format |
| **ORM** | Object-Relational Mapping | Database abstraction layer |
| **REST** | Representational State Transfer | API architectural style |
| **SDD** | Software Design Document | Detailed design specification |
| **SQL** | Structured Query Language | Database query language |
| **SSH** | Secure Shell | Encrypted network protocol |
| **SSL** | Secure Sockets Layer | Encryption protocol (deprecated, use TLS) |
| **TDD** | Test-Driven Development | Tests-first development approach |
| **TLS** | Transport Layer Security | Encryption protocol |
| **UI** | User Interface | User interaction layer |
| **URL** | Uniform Resource Locator | Web address |
| **UX** | User Experience | User interaction quality |
| **VM** | Virtual Machine | Emulated computer system |
| **VPN** | Virtual Private Network | Encrypted network connection |
| **XML** | eXtensible Markup Language | Markup language for data |
| **YAML** | YAML Ain't Markup Language | Human-readable data format |

### Development & Tools

| Acronym | Full Term | Definition |
|---------|-----------|------------|
| **CI/CD** | Continuous Integration / Continuous Deployment | Automated build and deploy |
| **DDD** | Domain-Driven Design | Business-focused design approach |
| **IDE** | Integrated Development Environment | Code editing software |
| **MVC** | Model-View-Controller | Software design pattern |
| **QA** | Quality Assurance | Testing and quality control |
| **REPL** | Read-Eval-Print Loop | Interactive programming environment |
| **SaaS** | Software as a Service | Cloud-based software delivery |
| **SDK** | Software Development Kit | Development tools package |
| **SOLID** | Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion | OOP design principles |
| **VCS** | Version Control System | Code versioning tool (e.g., git) |

### CODITECT-Specific

| Term | Definition |
|------|------------|
| **.coditect/** | Core framework directory |
| **.claude** | Symlink to .coditect |
| **MEMORY-CONTEXT** | Knowledge preservation system |
| **Task Tool Pattern** | Agent invocation method |
| **Operator** | CODITECT-trained user |
| **PLG** | Product-Led Growth |
| **SLG** | Sales-Led Growth |
| **MLG** | Marketing-Led Growth |
| **C4** | Context-Container-Component-Code architecture |

---

## Usage Guide

### How to Use This Glossary

**During Training:**
```
"What does PMF mean?"
→ Look up "PMF" in Business Discovery or Acronyms sections
```

**When Reading Documentation:**
```
"The document mentions ADRs - what are those?"
→ Look up "ADR" in Technical Architecture section
```

**When Working on Projects:**
```
Keep this glossary open in a separate window for quick reference
```

**When Teaching Others:**
```
"See CODITECT-GLOSSARY.md for definitions of all terms"
```

### Quick Lookup Tips

1. **Ctrl+F / Cmd+F:** Search for term in browser
2. **Table of Contents:** Jump to relevant section
3. **Cross-references:** Many terms link to related concepts
4. **Examples:** Most definitions include practical examples

---

## Updating This Glossary

As CODITECT evolves, new terms and concepts will be added. Operators are encouraged to:

1. **Submit new terms:** When you encounter undefined concepts
2. **Improve definitions:** If explanations could be clearer
3. **Add examples:** Real-world usage helps understanding
4. **Fix errors:** Report any inaccuracies

**Process:**
1. Edit CODITECT-GLOSSARY.md
2. Add term in alphabetical order within section
3. Provide clear, concise definition
4. Include example if helpful
5. Commit with message: "Add [term] to glossary"

---

## Related Resources

**For deeper learning:**
- `CODITECT-OPERATOR-TRAINING-SYSTEM.md` - Full training program
- `CODITECT-OPERATOR-FAQ.md` - Common questions
- `CLAUDE-CODE-BASICS.md` - Platform fundamentals
- `../CLAUDE.md` - Framework overview
- `../agents/` - Individual agent descriptions

---

**Document Version:** 1.0
**Last Updated:** 2025-11-16
**Total Terms:** 100+
**Maintainer:** CODITECT Training Team

**Remember:** Understanding terminology accelerates learning. When in doubt, look it up!
