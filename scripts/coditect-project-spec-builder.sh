#!/usr/bin/env bash
#
# CODITECT Project Specification Builder
# Automated generation of complete project specifications
#
# This script guides you through business discovery and generates:
# - All 9 business discovery documents
# - Technical specifications (SDD, TDD, ADRs)
# - PROJECT-PLAN.md with complete roadmap
# - TASKLIST.md with checkboxes
# - Competitive analysis and market research
# - Architecture and design documents
#
# Usage:
#   cd ~/PROJECTS/my-project
#   ../../scripts/coditect-project-spec-builder.sh
#
# Prerequisites:
#   - Project initialized with coditect-project-init.sh
#   - Claude Code CLI installed
#   - ANTHROPIC_API_KEY set
#
# Copyright © 2025 AZ1.AI INC. All Rights Reserved.
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Configuration
PROJECT_DIR="$(pwd)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"
TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S")
TEMPLATES_DIR="$(dirname "$0")/../templates"

# Helper functions
log_header() {
    echo ""
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${MAGENTA}  $1${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

log_info() { echo -e "${BLUE}ℹ${NC}  $1"; }
log_success() { echo -e "${GREEN}✅${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC}  $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }
log_step() { echo -e "${CYAN}▸${NC}  $1"; }

# Display banner
clear
echo -e "${MAGENTA}"
cat << "EOF"
   ______  ____  ____ __________  ______  ______
  / ____/ / __ \/ __ \\_  _/_  __/ / ____/ / ____/
 / /     / / / / / / // /  / /   / __/   / /
/ /___  / /_/ / /_/ // /  / /   / /___  / /___
\____/  \____/_____/___/ /_/   /_____/  \____/

  Project Specification Builder v1.0
  Automated Business Discovery & Technical Design
EOF
echo -e "${NC}"

log_header "CODITECT PROJECT SPECIFICATION BUILDER"

# Validate environment
log_info "Validating environment..."

if [ ! -f "README.md" ] || [ ! -f "CLAUDE.md" ]; then
    log_error "Not in a CODITECT project directory"
    log_error "Run this from a project initialized with coditect-project-init.sh"
    exit 1
fi

if ! command -v claude &>/dev/null; then
    log_warning "Claude Code CLI not found - some features may not work"
fi

log_success "Environment validated"

# Interactive project idea gathering
log_header "Step 1/10: Project Idea & Vision"

echo -e "${CYAN}Let's start with your project idea...${NC}"
echo ""

read -p "Project name (current: $PROJECT_NAME): " input_name
if [ -n "$input_name" ]; then
    PROJECT_NAME="$input_name"
fi

echo ""
echo "Describe your project idea in 2-3 sentences:"
echo "(What problem does it solve? Who is it for? What makes it unique?)"
echo ""
read -p "> " PROJECT_IDEA

echo ""
echo "What is the primary value proposition? (One sentence)"
read -p "> " VALUE_PROP

echo ""
echo "Who is your target customer? (Be specific)"
read -p "> " TARGET_CUSTOMER

log_success "Project vision captured"

# Generate project specification prompts file
SPEC_FILE="$PROJECT_DIR/.coditect-spec-prompts.md"
cat > "$SPEC_FILE" << SPEC_EOF
# CODITECT Project Specification Prompts
# Auto-generated: $TIMESTAMP

## Project Basics
- **Name**: $PROJECT_NAME
- **Idea**: $PROJECT_IDEA
- **Value Proposition**: $VALUE_PROP
- **Target Customer**: $TARGET_CUSTOMER

---

## Agent Invocation Prompts

Use these prompts with CODITECT agents to generate your complete project specification.

### Phase 1: Market Research (30-45 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use competitive-market-analyst subagent to conduct comprehensive market research for: $PROJECT_NAME

Project Description: $PROJECT_IDEA
Target Customer: $TARGET_CUSTOMER

Research Focus:
1. Industry Analysis
   - Market size (TAM/SAM/SOM calculation)
   - Growth trends and forecasts
   - Technology trends enabling this solution
   - Regulatory environment

2. Competitive Landscape
   - Direct competitors (identify 5-7)
   - Indirect competitors and substitutes
   - Competitive positioning map
   - Market gaps and opportunities

3. Customer Insights
   - Customer segments and personas
   - Pain points and needs
   - Buying behavior and triggers
   - Willingness to pay indicators

Output: Complete docs/research/01-market-research.md with:
- Executive summary
- TAM/SAM/SOM calculations with sources
- Competitor analysis matrix
- Market trends and insights
- References and data sources
\"\"\"
)
\`\`\`

### Phase 2: Customer Discovery (30-60 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use business-intelligence-analyst subagent to create comprehensive customer discovery framework for: $PROJECT_NAME

Target Customer: $TARGET_CUSTOMER
Value Proposition: $VALUE_PROP

Create Ideal Customer Profile (ICP) with:

1. Demographics (Firmographics)
   - Industry vertical(s)
   - Company size (employees, revenue)
   - Geographic focus
   - Decision-maker titles and roles

2. Psychographics
   - Pain points (rate severity 0-10)
   - Goals and motivations
   - Buying triggers and timing
   - Success metrics they care about

3. Behavioral
   - Current tools and workarounds
   - Budget range and procurement process
   - Technical sophistication level
   - Integration requirements

4. Customer Interview Guide
   - 10 discovery questions
   - Pain point validation questions
   - Solution concept testing questions
   - Pricing sensitivity questions

Output: Complete docs/research/03-customer-discovery.md with:
- Detailed ICP (3-dimensional model)
- Interview guide and scripts
- Validation criteria
- Customer segmentation
\"\"\"
)
\`\`\`

### Phase 3: Competitive Analysis (45-60 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use competitive-market-analyst subagent to create detailed competitive analysis for: $PROJECT_NAME

Project: $PROJECT_IDEA
Market Research: (reference docs/research/01-market-research.md)

Analysis Framework:

1. Competitor Deep-Dive (for each major competitor)
   - Company background and funding
   - Product features and capabilities
   - Pricing model and tiers
   - Target customer segments
   - Strengths and weaknesses
   - Market share and positioning

2. Competitive Advantage Analysis
   - Our Unfair Advantage (what competitors can't replicate)
   - Our Differentiation (how we're measurably better)
   - Our Moat (defensibility over time)

3. Feature Comparison Matrix
   - Must-have features (table stakes)
   - Nice-to-have features
   - Unique features (ours only)
   - Future roadmap items

4. Pricing Analysis
   - Competitor pricing tiers
   - Average contract values
   - Price positioning (low/mid/high)
   - Value-to-price ratios

Output: Complete docs/strategy/04-competitive-analysis.md with:
- Detailed competitor profiles (5-7 companies)
- Feature comparison matrix
- Pricing landscape analysis
- Strategic positioning recommendations
- SWOT analysis
\"\"\"
)
\`\`\`

### Phase 4: Product Scope & Definition (30-45 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use product-manager subagent to define complete product scope for: $PROJECT_NAME

Vision: $PROJECT_IDEA
Value Prop: $VALUE_PROP
Customer: $TARGET_CUSTOMER

Product Definition:

1. Product Classification
   - Is this a Feature / Application / Product / Business?
   - Core value proposition (one sentence)
   - Category positioning

2. MVP Scope
   - Must-have features (5-10 core features)
   - Success criteria for each feature
   - User stories and acceptance criteria

3. Out of Scope (for MVP)
   - Future features (post-MVP roadmap)
   - Enterprise features (for later)
   - Nice-to-have capabilities

4. Technical Requirements
   - Performance requirements
   - Scalability targets
   - Security requirements
   - Compliance needs

Output: Complete docs/product/02-product-scope.md with:
- Product classification and positioning
- Detailed MVP feature list with user stories
- Out-of-scope items with prioritization
- Technical and non-functional requirements
- Success metrics
\"\"\"
)
\`\`\`

### Phase 5: Value Proposition & Positioning (20-30 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use business-intelligence-analyst subagent to craft compelling value proposition for: $PROJECT_NAME

Context:
- Product: $PROJECT_IDEA
- Target: $TARGET_CUSTOMER
- Competitive Analysis: (reference docs/strategy/04-competitive-analysis.md)

Value Proposition Framework:

For [TARGET CUSTOMER]
Who [STATEMENT OF NEED/OPPORTUNITY]
Our [PRODUCT NAME]
Is a [PRODUCT CATEGORY]
That [STATEMENT OF KEY BENEFIT]
Unlike [PRIMARY COMPETITIVE ALTERNATIVE]
Our product [STATEMENT OF PRIMARY DIFFERENTIATION]

Create multiple variations (3-5) and recommend the strongest.

Also include:
1. Elevator pitch (30 seconds)
2. One-sentence description
3. Three key benefits (measurable outcomes)
4. Emotional benefits (how it makes users feel)
5. Supporting proof points

Output: Complete docs/strategy/05-value-proposition.md with:
- Finalized value proposition statement
- Multiple variations tested
- Elevator pitch and descriptions
- Key benefits with proof
- Messaging framework
\"\"\"
)
\`\`\`

### Phase 6: Product-Market Fit Plan (30-45 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use product-manager subagent to create 7-Fit Product-Market Fit validation plan for: $PROJECT_NAME

Reference all previous research and strategy documents.

7-Fit Framework:

PRE-LAUNCH (Customer Value Creation):
1. Problem-Solution Fit
   - Validation method
   - Success criteria
   - Timeline

2. Solution-Market Fit
   - Market size validation (TAM/SAM/SOM)
   - Target market accessibility
   - Success criteria

3. Product-Channel Fit
   - Customer acquisition channels
   - Channel testing plan
   - CAC targets (< 1/3 of LTV)

POST-LAUNCH (Business Value Creation):
4. Channel-Model Fit
   - Distribution economics
   - Channel alignment with business model
   - Success criteria

5. Model-Market Fit
   - Unit economics (CAC, LTV, payback period)
   - Success criteria: LTV:CAC ≥ 3:1, CAC recovery < 12 months

6. Product-Market Fit
   - Retention targets (>90% monthly for B2B)
   - Word-of-mouth referrals
   - Success signals

7. Business-Market Fit
   - Path to profitability
   - Scalability validation
   - Sustainable growth

Output: Complete docs/strategy/06-product-market-fit-plan.md with:
- Detailed validation plan for all 7 fits
- Success metrics and criteria
- Timeline and milestones
- Validation methods and tools
\"\"\"
)
\`\`\`

### Phase 7: Pricing Strategy (30-45 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use business-intelligence-analyst subagent to design comprehensive pricing strategy for: $PROJECT_NAME

Context:
- Product: $PROJECT_IDEA
- Customer: $TARGET_CUSTOMER
- Competitors: (reference docs/strategy/04-competitive-analysis.md)

Pricing Analysis:

1. Cost Structure
   - Cost per user calculation
   - Infrastructure costs
   - Support and sales costs
   - Target gross margin (70-80% for SaaS)

2. Competitive Pricing Landscape
   - Low-end pricing ($__ /month)
   - Mid-tier pricing ($__ /month)
   - High-end pricing ($__ /month)
   - Enterprise (custom)

3. Pricing Model Selection
   Evaluate and recommend from:
   - Per-User (Seat-Based)
   - Usage-Based (Consumption)
   - Flat-Rate (Unlimited)
   - Freemium + Paid Tiers
   - Feature-Based Tiers
   - Hybrid (Usage + Seats)

4. Pricing Tier Design (4-tier model)
   - Free/Trial: Features, limitations
   - Starter: Price, target persona, features
   - Pro: Price, target persona, features
   - Enterprise: Custom, target, features

5. Pricing Rationale
   - Value-based pricing calculation
   - Competitive positioning
   - Psychological pricing tactics
   - Annual discount strategy

Output: Complete docs/strategy/07-pricing-strategy.md with:
- Detailed pricing tier structure
- Pricing model with rationale
- Competitive positioning
- Revenue projections
- A/B testing recommendations
\"\"\"
)
\`\`\`

### Phase 8: Go-to-Market Strategy (45-60 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use business-intelligence-analyst subagent to create comprehensive GTM strategy for: $PROJECT_NAME

Context:
- ICP: (reference docs/research/03-customer-discovery.md)
- Pricing: (reference docs/strategy/07-pricing-strategy.md)
- Product: (reference docs/product/02-product-scope.md)

GTM Framework:

1. GTM Motion Selection
   Evaluate and recommend from:
   - Product-Led Growth (PLG): Self-serve, freemium, viral
   - Sales-Led Growth (SLG): Outbound, enterprise, consultative
   - Marketing-Led Growth (MLG): Inbound, content, nurture
   - Partner-Led: Marketplace, integrations, resellers

2. Customer Acquisition Strategy
   Phase 1 (Month 1-3):
   - Target: __ customers
   - Primary channel: __
   - Budget: $__
   - Tactics: [list 3-5]

   Phase 2 (Month 4-6):
   - Target: __ customers (2-3x Phase 1)
   - Channels: [multi-channel]
   - Budget: $__
   - Tactics: [list 5-7]

   Phase 3 (Month 7-12):
   - Target: __ customers (5-10x Phase 1)
   - Channels: [scaled]
   - Budget: $__
   - Tactics: [list 10+]

3. Unit Economics
   - CAC calculation and targets
   - LTV calculation
   - LTV:CAC ratio target (≥3:1)
   - Months to recover CAC (target <12)
   - Monthly churn target (<5% for B2B)

4. Launch Plan
   - Pre-launch activities
   - Launch day execution
   - Post-launch growth tactics
   - Success metrics tracking

Output: Complete docs/strategy/08-go-to-market-strategy.md with:
- GTM motion selection and rationale
- 3-phase acquisition roadmap
- Channel strategy and tactics
- Unit economics model
- Launch execution plan
\"\"\"
)
\`\`\`

### Phase 9: Executive Summary (20-30 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use business-intelligence-analyst subagent to create executive summary for: $PROJECT_NAME

Synthesize all previous documents into one-page executive summary.

Reference:
- All docs/research/* files
- All docs/strategy/* files
- docs/product/02-product-scope.md

Executive Summary Structure:

1. One-Sentence Description
   For [TARGET] who [NEED], our [PRODUCT] is a [CATEGORY] that [BENEFIT].
   Unlike [COMPETITOR], we [DIFFERENTIATION].

2. The Opportunity
   - Problem statement
   - Market size (TAM/SAM/SOM)
   - Market trends

3. The Solution
   - Product overview
   - Key features (MVP)
   - Differentiation

4. Target Customer
   - ICP summary
   - Customer pain points
   - Addressable segments

5. Business Model
   - Revenue model
   - Pricing summary
   - Unit economics

6. Go-to-Market
   - GTM motion
   - Customer acquisition strategy
   - Distribution channels

7. Competitive Landscape
   - Key competitors
   - Our competitive advantages
   - Our moat

8. Financial Projections
   - Year 1: Revenue, Customers, Burn
   - Year 2: Revenue, Customers, Burn
   - Year 3: Revenue, Customers, Path to profitability

9. Ask / Next Steps
   - Immediate priorities
   - Resource needs
   - Timeline

Output: Complete docs/executive-summary.md (one-page, investor-ready)
\"\"\"
)
\`\`\`

### Phase 10: Technical Architecture (60-90 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use senior-architect subagent to design complete system architecture for: $PROJECT_NAME

Context:
- Product Scope: (reference docs/product/02-product-scope.md)
- MVP Features: [list from scope doc]
- Non-functional requirements: [performance, scale, security from scope]

Architecture Design (C4 Methodology):

1. C1 - System Context Diagram
   - System boundary
   - External users and personas
   - External systems (APIs, services)
   - Key interactions

2. C2 - Container Diagram
   - Frontend applications
   - Backend services
   - Databases and data stores
   - Message queues
   - Caching layers
   - External integrations

3. C3 - Component Diagrams (for each container)
   - Internal components
   - Responsibilities
   - Interactions and dependencies
   - Technology choices

4. Technology Stack Selection
   - Frontend: [Framework, libraries]
   - Backend: [Language, framework]
   - Database: [SQL/NoSQL, rationale]
   - Infrastructure: [Cloud provider, services]
   - DevOps: [CI/CD, monitoring]

5. Architecture Decision Records (ADRs)
   Create ADRs for:
   - Technology stack selection
   - Database choice
   - API design (REST vs GraphQL)
   - Authentication approach
   - Deployment strategy

Output:
- docs/architecture/ARCHITECTURE.md (complete C4 diagrams in Mermaid)
- docs/decisions/ADR-001-technology-stack.md
- docs/decisions/ADR-002-database-choice.md
- docs/decisions/ADR-003-api-design.md
- docs/decisions/ADR-004-authentication.md
- docs/decisions/ADR-005-deployment-strategy.md
\"\"\"
)
\`\`\`

### Phase 11: Database Design (30-45 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use database-specialist subagent to design complete database schema for: $PROJECT_NAME

Context:
- Architecture: (reference docs/architecture/ARCHITECTURE.md)
- Database choice: (reference docs/decisions/ADR-002-database-choice.md)
- Product features: (reference docs/product/02-product-scope.md)

Database Design:

1. Entity-Relationship Model
   - All entities (tables)
   - Relationships (1:1, 1:N, N:N)
   - Cardinality and optionality
   - ER diagram (Mermaid)

2. Schema Definition
   For each table:
   - Column names and types
   - Primary keys
   - Foreign keys and relationships
   - Indexes (for performance)
   - Constraints (unique, not null, check)

3. Data Migration Strategy
   - Initial schema migration
   - Migration tooling
   - Versioning approach
   - Rollback procedures

4. Sample Queries
   - Common read queries (with indexes)
   - Common write queries
   - Complex queries (joins, aggregations)
   - Performance optimization notes

Output:
- docs/database/DATABASE-SCHEMA.md (complete schema with SQL DDL)
- docs/database/ER-DIAGRAM.md (Mermaid ER diagram)
- docs/database/MIGRATIONS.md (migration strategy)
\"\"\"
)
\`\`\`

### Phase 12: API Specification (45-60 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use backend-architect subagent to design complete API specification for: $PROJECT_NAME

Context:
- Architecture: (reference docs/architecture/ARCHITECTURE.md)
- Database Schema: (reference docs/database/DATABASE-SCHEMA.md)
- Product Features: (reference docs/product/02-product-scope.md)

API Design:

1. API Architecture
   - REST or GraphQL (reference ADR-003)
   - Versioning strategy
   - Base URL structure
   - Authentication method (JWT, OAuth, API keys)

2. Endpoint Specification
   For each endpoint:
   - HTTP method and path
   - Request parameters (path, query, body)
   - Request schema (JSON)
   - Response schema (JSON)
   - Status codes (success and error)
   - Rate limiting
   - Authentication requirements

3. Resource Models
   - Data transfer objects (DTOs)
   - Validation rules
   - Transformation logic

4. Error Handling
   - Error response format
   - Error codes and messages
   - Validation errors

5. OpenAPI 3.1 Specification
   Complete machine-readable API spec

Output:
- docs/api/API-SPECIFICATION.yaml (OpenAPI 3.1 spec)
- docs/api/API-OVERVIEW.md (human-readable API guide)
- docs/api/AUTHENTICATION.md (auth flow documentation)
\"\"\"
)
\`\`\`

### Phase 13: Software Design Document (SDD) (60-90 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use software-design-architect subagent to create comprehensive Software Design Document for: $PROJECT_NAME

Context: Reference ALL previous documents

SDD Structure:

1. Introduction
   - Purpose and scope
   - Intended audience
   - Document conventions
   - References

2. System Overview
   - System context (from C1 diagram)
   - High-level architecture (from C2 diagram)
   - Technology stack summary

3. Design Considerations
   - Assumptions and dependencies
   - Constraints
   - Design goals and guidelines

4. Detailed Design
   For each major component:
   - Purpose and responsibilities
   - Interface specification
   - Internal structure (from C3 diagrams)
   - Data flow
   - Error handling
   - Logging and monitoring

5. Data Design
   - Database schema (reference DATABASE-SCHEMA.md)
   - Data flow diagrams
   - Data persistence strategy
   - Caching strategy

6. Interface Design
   - User interfaces (screens and flows)
   - API interfaces (reference API-SPECIFICATION.yaml)
   - External system interfaces

7. Security Design
   - Authentication and authorization
   - Data encryption (at rest and in transit)
   - Security controls
   - Compliance requirements

8. Performance Design
   - Performance requirements
   - Optimization strategies
   - Scalability approach
   - Load balancing

9. Deployment Design
   - Deployment architecture
   - Infrastructure components
   - CI/CD pipeline
   - Monitoring and alerting

Output: docs/technical/SDD-SOFTWARE-DESIGN-DOCUMENT.md (complete detailed design)
\"\"\"
)
\`\`\`

### Phase 14: Test Design Document (TDD) (45-60 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use testing-specialist subagent to create comprehensive Test Design Document for: $PROJECT_NAME

Context:
- SDD: (reference docs/technical/SDD-SOFTWARE-DESIGN-DOCUMENT.md)
- Product Features: (reference docs/product/02-product-scope.md)

TDD Structure:

1. Test Strategy
   - Testing objectives
   - Testing scope (in-scope and out-of-scope)
   - Testing approach
   - Quality goals (coverage targets, defect rates)

2. Test Levels
   Unit Testing:
   - Coverage target (80%+)
   - Testing frameworks
   - Mocking strategy

   Integration Testing:
   - API contract testing
   - Database integration tests
   - External service mocking

   End-to-End Testing:
   - Critical user flows
   - Browser/device coverage
   - Test data management

   Performance Testing:
   - Load testing scenarios
   - Stress testing
   - Performance benchmarks

3. Test Cases
   For each major feature:
   - Test scenarios
   - Test cases with steps
   - Expected results
   - Pass/fail criteria

4. Test Environment
   - Environment setup
   - Test data requirements
   - Configuration management

5. Defect Management
   - Bug tracking process
   - Severity and priority definitions
   - Defect lifecycle

6. Test Automation
   - Automation framework
   - CI/CD integration
   - Automated test coverage goals

Output: docs/technical/TDD-TEST-DESIGN-DOCUMENT.md (complete test plan)
\"\"\"
)
\`\`\`

### Phase 15: Project Plan & Task List (30-45 minutes)

\`\`\`python
Task(
    subagent_type="general-purpose",
    prompt=\"\"\"Use orchestrator subagent to create complete PROJECT-PLAN.md and TASKLIST.md for: $PROJECT_NAME

Context: Reference ALL previous documents (business + technical)

PROJECT-PLAN.md Structure:

1. Executive Summary
   - Project overview
   - Key objectives
   - Success criteria

2. Project Phases
   Phase 1: Requirements & Architecture (Week 1-2)
   - Duration, team, deliverables
   - Milestones and quality gates

   Phase 2: Backend Development (Week 3-6)
   - All backend features broken down
   - Sprint-by-sprint plan

   Phase 3: Frontend Development (Week 4-8, parallel)
   - All frontend features broken down
   - UI/UX milestones

   Phase 4: Integration & Testing (Week 7-9)
   - Integration approach
   - Testing phases

   Phase 5: Deployment & Launch (Week 9-10)
   - Deployment steps
   - Launch checklist

3. Resource Allocation
   - Team composition
   - Agent assignments
   - Time estimates

4. Timeline & Milestones
   - Gantt chart (Mermaid)
   - Critical path
   - Dependencies

5. Risk Management
   - Risk register
   - Mitigation strategies

TASKLIST.md Structure:

Complete task breakdown with:
- All tasks from all phases
- Checkboxes for tracking
- Agent assignments
- Time estimates
- Dependencies
- Priority levels (P0, P1, P2)

Example:
- [ ] **Task 1.1.1**: Market research
  - **Assigned**: competitive-market-analyst
  - **Est**: 4 hours
  - **Priority**: P0
  - **Dependencies**: None

Output:
- PROJECT-PLAN.md (complete multi-phase plan)
- TASKLIST.md (100+ tasks with checkboxes)
\"\"\"
)
\`\`\`

---

## Execution Order

Run these phases sequentially (each builds on previous):

1. Market Research (Phase 1)
2. Customer Discovery (Phase 2)
3. Competitive Analysis (Phase 3)
4. Product Scope (Phase 4)
5. Value Proposition (Phase 5)
6. Product-Market Fit Plan (Phase 6)
7. Pricing Strategy (Phase 7)
8. Go-to-Market Strategy (Phase 8)
9. Executive Summary (Phase 9)
10. Technical Architecture (Phase 10)
11. Database Design (Phase 11)
12. API Specification (Phase 12)
13. Software Design Document (Phase 13)
14. Test Design Document (Phase 14)
15. Project Plan & Task List (Phase 15)

Total Time: 10-15 hours (can be spread across multiple days with session exports)

---

## Tips for Success

1. **Use MEMORY-CONTEXT**: Export at end of each phase
2. **Review Before Next**: Start each session reviewing last phase outputs
3. **Iterate**: Refine documents as you learn more
4. **Validate**: Review outputs, ask agents to improve
5. **Track Progress**: Update TASKLIST.md as you complete phases

---

**Generated**: $TIMESTAMP
**Project**: $PROJECT_NAME
SPEC_EOF

log_success "Specification prompts generated: .coditect-spec-prompts.md"

# Summary
log_header "Specification Builder Complete!"

echo ""
echo -e "${GREEN}✅ Your project specification prompts are ready!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${CYAN}What Was Created:${NC}"
echo "  📄 .coditect-spec-prompts.md"
echo "     Complete guide with 15 phases of agent invocations"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo ""
echo "1️⃣  Review the prompts file:"
echo "    open .coditect-spec-prompts.md"
echo ""
echo "2️⃣  Start with Phase 1 (Market Research):"
echo "    Copy the Task(...) prompt and run in Claude Code"
echo ""
echo "3️⃣  Continue through all 15 phases sequentially"
echo "    Each phase builds on previous outputs"
echo ""
echo "4️⃣  Export context after each phase:"
echo "    /export 2025-XX-XX-PHASE-N-[NAME].txt"
echo ""
echo "5️⃣  Review and iterate:"
echo "    Ask agents to improve/refine any document"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}📊 Complete Specification Includes:${NC}"
echo ""
echo "  Business Discovery (9 documents):"
echo "  ✅ Market Research (TAM/SAM/SOM)"
echo "  ✅ Customer Discovery (ICP)"
echo "  ✅ Competitive Analysis"
echo "  ✅ Product Scope"
echo "  ✅ Value Proposition"
echo "  ✅ Product-Market Fit Plan"
echo "  ✅ Pricing Strategy"
echo "  ✅ Go-to-Market Strategy"
echo "  ✅ Executive Summary"
echo ""
echo "  Technical Specification (6 documents):"
echo "  ✅ Architecture (C4 Diagrams)"
echo "  ✅ Database Schema"
echo "  ✅ API Specification (OpenAPI)"
echo "  ✅ Software Design Document (SDD)"
echo "  ✅ Test Design Document (TDD)"
echo "  ✅ Architecture Decision Records (5 ADRs)"
echo ""
echo "  Project Management (2 documents):"
echo "  ✅ PROJECT-PLAN.md (complete roadmap)"
echo "  ✅ TASKLIST.md (100+ tasks with checkboxes)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${MAGENTA}Estimated Time: 10-15 hours total${NC}"
echo -e "${MAGENTA}Can be done over 2-3 days with session exports${NC}"
echo ""
echo -e "${GREEN}Ready to build a world-class project specification! 🚀${NC}"
echo ""
