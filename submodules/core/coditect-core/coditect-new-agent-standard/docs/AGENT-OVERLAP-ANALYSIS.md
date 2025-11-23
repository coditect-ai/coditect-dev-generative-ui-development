# Agent Overlap Analysis

## ORIGINAL SYSTEM (86 agents)
**Location**: `/home/halcasteel/.claude/agents-reference/` (Production system)  
**Format**: Basic Anthropic format (YAML with name/description/model)  
**By Domain:**

### Development Languages (19 agents)
- rust-pro, python-pro, javascript-pro, typescript-pro, golang-pro
- java-pro, cpp-pro, c-pro, csharp-pro, php-pro, ruby-pro, scala-pro, elixir-pro
- django-pro, fastapi-pro, flutter-expert, ios-developer, unity-developer, minecraft-bukkit-pro

### Architecture & Backend (8 agents)
- backend-architect, cloud-architect, hybrid-cloud-architect, kubernetes-architect
- graphql-architect, docs-architect, architect-review, terraform-specialist

### Security (3 agents)
- security-auditor, backend-security-coder, frontend-security-coder

### Development Tools (8 agents)
- frontend-developer, mobile-developer, code-reviewer, debugger, error-detective
- performance-engineer, test-automator, tdd-orchestrator

### Infrastructure & Operations (6 agents)
- database-admin, database-optimizer, devops-troubleshooter, deployment-engineer
- network-engineer, observability-engineer

### AI/ML & Data (4 agents)
- ai-engineer, ml-engineer, mlops-engineer, data-scientist, data-engineer

### Business & Content (16 agents)
- business-analyst, prompt-engineer, content-marketer, tutorial-engineer
- reference-builder, payment-integration, customer-support, hr-pro, legal-advisor
- risk-manager, quant-analyst, sales-automator
- seo-* (9 SEO specialists)

### Specialized Tools (5 agents)
- mermaid-expert, context-manager, dx-optimizer, legacy-modernizer, search-specialist

---

## NEW SYSTEM (47 agents)
**Location**: External repository `agents-reference-47/` (Research target)  
**Format**: Enhanced format with Context Awareness DNA and automation features

### Research & Analysis (7 agents)
- competitive-market-analyst, web-search-researcher, codebase-analyzer
- codebase-locator, codebase-pattern-finder, thoughts-analyzer, thoughts-locator

### Coordination (3 agents)
- orchestrator, orchestrator-code-review, orchestrator-detailed-backup

### Development (8 agents)
- rust-expert-developer, rust-qa-specialist, frontend-react-typescript-expert
- actix-web-specialist, websocket-protocol-designer, wasm-optimization-expert
- terminal-integration-specialist, script-utility-analyzer

### Database (2 agents)
- foundationdb-expert, database-architect

### AI & Analysis (5 agents)
- ai-specialist, novelty-detection-specialist, prompt-analyzer-specialist
- skill-quality-enhancer, research-agent

### Infrastructure (6 agents)
- cloud-architect, cloud-architect-code-reviewer, monitoring-specialist
- k8s-statefulset-specialist, multi-tenant-architect, devops-engineer

### Quality Assurance (4 agents)
- testing-specialist, qa-reviewer, security-specialist, adr-compliance-specialist

### Architecture (4 agents)
- senior-architect, software-design-architect, software-design-document-specialist, coditect-adr-specialist

### CODI Integration (4 agents)
- codi-devops-engineer, codi-documentation-writer, codi-qa-specialist, codi-test-engineer

### Business Intelligence (2 agents)
- business-intelligence-analyst, venture-capital-business-analyst

### Project Management (1 agent)
- project-organizer

---

## OVERLAP ANALYSIS

### DIRECT OVERLAPS (Similar Function)
1. **cloud-architect** ↔ **cloud-architect** (EXACT MATCH)
2. **security-auditor** ↔ **security-specialist** (SIMILAR)
3. **backend-architect** ↔ **database-architect/senior-architect** (RELATED)
4. **ai-engineer** ↔ **ai-specialist** (SIMILAR)
5. **test-automator** ↔ **testing-specialist** (SIMILAR)
6. **devops-troubleshooter** ↔ **devops-engineer** (RELATED)
7. **business-analyst** ↔ **business-intelligence-analyst** (RELATED)
8. **rust-pro** ↔ **rust-expert-developer** (SIMILAR)
9. **frontend-developer** ↔ **frontend-react-typescript-expert** (SPECIALIZED)

### PARTIAL OVERLAPS (Related but Different Focus)
- **code-reviewer** vs **orchestrator-code-review** (different scope)
- **database-admin** vs **foundationdb-expert** (general vs specialized)
- **performance-engineer** vs **monitoring-specialist** (performance vs monitoring focus)
- **prompt-engineer** vs **prompt-analyzer-specialist** (creation vs analysis)

### UNIQUE TO ORIGINAL (77 agents unique)
- **19 language specialists** (python-pro, java-pro, etc.)
- **16 business/content agents** (SEO specialists, sales, legal, etc.)
- **Mobile specialists** (mobile-developer, ios-developer, flutter-expert)
- **Specialized domains** (blockchain-developer, payment-integration, etc.)

### UNIQUE TO NEW (38 agents unique)
- **Research specialists** (competitive-market-analyst, web-search-researcher)
- **Orchestration framework** (3 orchestrator variants)
- **Advanced analysis** (novelty-detection, thoughts-analyzer)
- **CODI integration** (4 CODI-specific agents)
- **Specialized architectures** (multi-tenant-architect, adr-compliance)

---

## SUMMARY
- **Direct Overlaps**: 9 agents (~20% of new system)
- **Partial Overlaps**: 4 agents (~9% of new system)  
- **Unique Capabilities**: 
  - Original: 77 agents (90% unique)
  - New: 38 agents (81% unique)

**CONCLUSION**: Very low overlap (~29%) - mostly complementary capabilities!