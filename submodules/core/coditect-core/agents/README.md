# Custom Agents Directory - 47 Production-Ready AI Agents

This directory contains 46 custom AI agents for the AZ1.AI CODITECT AI IDE Market Research project, fully configured with YAML frontmatter for automatic Claude Code recognition.

## Quick Agent Reference

**Total Agents**: 47 (all properly configured ✅)  
**Format**: Markdown with YAML frontmatter  
**Auto-Recognition**: `.claude/agents/` directory structure  
**Invocation**: Direct explicit or Task tool proxy pattern  

## 🎯 Coordination & Orchestration (3 agents)

### [orchestrator.md](orchestrator.md) 🚀
**Primary multi-agent coordinator** - Use for complex workflows requiring multiple agents
- **Tools**: TodoWrite, Read, Grep, Glob, Bash, Write, Edit
- **Capabilities**: 7 production workflows, token budget management (160K), parallel execution
- **Usage**: `"Use the orchestrator subagent to implement user profile editing with backend API and frontend UI"`

### [orchestrator-code-review.md](orchestrator-code-review.md)
**Code review orchestration specialist** - ADR compliance + multi-agent coordination
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the orchestrator-code-review subagent to review authentication implementation"`

### [orchestrator-detailed-backup.md](orchestrator-detailed-backup.md)
**Detailed orchestration patterns** - Complex task decomposition and planning
- **Tools**: TodoWrite, Read, Grep, Glob, Bash
- **Usage**: `"Use the orchestrator-detailed-backup subagent for comprehensive project planning"`

## 🔍 Research & Analysis (6 agents)

### [competitive-market-analyst.md](competitive-market-analyst.md) 📊
**Primary research agent** - Comprehensive competitive intelligence and market analysis
- **Tools**: WebSearch, WebFetch, TodoWrite, Read, Write, Edit, Grep, Glob, LS, Bash
- **Usage**: `"Use the competitive-market-analyst subagent to research AI IDE pricing strategies"`

### [web-search-researcher.md](web-search-researcher.md) 🌐
**External intelligence specialist** - Deep web research and information gathering
- **Tools**: WebSearch, WebFetch, TodoWrite, Read, Grep, Glob, LS
- **Usage**: `"Use the web-search-researcher subagent to research latest AI development tools"`

### [codebase-analyzer.md](codebase-analyzer.md)
**Implementation analysis** - Understanding HOW code works
- **Tools**: Read, Grep, Glob, LS
- **Usage**: `"Use the codebase-analyzer subagent to understand authentication implementation"`

### [codebase-locator.md](codebase-locator.md)
**File discovery** - Finding WHERE code lives
- **Tools**: Grep, Glob, LS
- **Usage**: `"Use the codebase-locator subagent to find all session management files"`

### [codebase-pattern-finder.md](codebase-pattern-finder.md)
**Pattern extraction** - Finding similar implementations and usage examples
- **Tools**: Grep, Glob, Read, LS
- **Usage**: `"Use the codebase-pattern-finder subagent to find API endpoint patterns"`

### [thoughts-analyzer.md](thoughts-analyzer.md)
**Research synthesis** - Deep dive analysis of research documents
- **Tools**: Read, Grep, Glob, LS
- **Usage**: `"Use the thoughts-analyzer subagent to analyze market research findings"`

### [thoughts-locator.md](thoughts-locator.md)
**Document discovery** - Finding relevant documents in thoughts/ directory
- **Tools**: Grep, Glob, LS
- **Usage**: `"Use the thoughts-locator subagent to find design decisions about pricing"`

## 🛠️ Development Specialists (8 agents)

### [rust-expert-developer.md](rust-expert-developer.md) 🦀
**Advanced Rust specialist** - Production-grade Rust development
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the rust-expert-developer subagent to implement async API endpoints"`

### [rust-qa-specialist.md](rust-qa-specialist.md)
**Rust quality assurance** - Code safety, performance, security validation
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the rust-qa-specialist subagent to review backend code quality"`

### [frontend-react-typescript-expert.md](frontend-react-typescript-expert.md) ⚛️
**React/TypeScript specialist** - Modern frontend development
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the frontend-react-typescript-expert subagent to build user interface components"`

### [actix-web-specialist.md](actix-web-specialist.md)
**Actix-web framework expert** - High-performance async web services
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the actix-web-specialist subagent to optimize API performance"`

### [websocket-protocol-designer.md](websocket-protocol-designer.md)
**Real-time communication** - WebSocket protocol design and optimization
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the websocket-protocol-designer subagent to implement real-time features"`

### [wasm-optimization-expert.md](wasm-optimization-expert.md)
**WebAssembly optimization** - WASM performance and compilation optimization
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the wasm-optimization-expert subagent to optimize WebAssembly performance"`

### [terminal-integration-specialist.md](terminal-integration-specialist.md)
**Terminal emulation** - WebAssembly terminal with Kubernetes integration
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite, LS
- **Usage**: `"Use the terminal-integration-specialist subagent to implement terminal features"`

### [script-utility-analyzer.md](script-utility-analyzer.md)
**Script analysis** - Shell scripts, build scripts, and automation tools
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite, LS
- **Usage**: `"Use the script-utility-analyzer subagent to evaluate build scripts"`

## 💾 Database Specialists (2 agents)

### [foundationdb-expert.md](foundationdb-expert.md) 🗄️
**FoundationDB specialist** - Distributed database architecture and optimization
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the foundationdb-expert subagent to design multi-tenant data schemas"`

### [database-architect.md](database-architect.md)
**SQL/NoSQL architect** - PostgreSQL, MySQL, Redis, MongoDB coverage
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the database-architect subagent to design database architecture"`

## 🤖 AI & Analysis Specialists (5 agents)

### [ai-specialist.md](ai-specialist.md) 🧠
**Multi-provider AI routing** - Intelligent model selection and prompt optimization
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the ai-specialist subagent to optimize AI model routing"`

### [novelty-detection-specialist.md](novelty-detection-specialist.md) ✨
**Meta-cognitive analysis** - Autonomous situation assessment and adaptive response
- **Tools**: Read, Write, Edit, Grep, Glob, TodoWrite, WebSearch, WebFetch, LS, Bash
- **Usage**: `"Use the novelty-detection-specialist subagent to assess if this represents genuine innovation"`

### [prompt-analyzer-specialist.md](prompt-analyzer-specialist.md)
**Prompt analysis platform** - AI prompt development and optimization
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite, LS
- **Usage**: `"Use the prompt-analyzer-specialist subagent to optimize AI prompts"`

### [skill-quality-enhancer.md](skill-quality-enhancer.md)
**Agent optimization** - Agent skill assessment and enhancement
- **Tools**: Read, Write, Edit, Bash, Glob, Grep
- **Usage**: `"Use the skill-quality-enhancer subagent to improve agent capabilities"`

### [research-agent.md](research-agent.md)
**Technical research** - Implementation decisions and best practices research
- **Tools**: WebSearch, WebFetch, Read, Grep, Glob
- **Usage**: `"Use the research-agent subagent to research technical implementation options"`

## ☁️ Infrastructure & Operations (6 agents)

### [cloud-architect.md](cloud-architect.md) ☁️
**Cloud infrastructure** - GCP deployment, CI/CD, zero-downtime deployments
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the cloud-architect subagent to design deployment architecture"`

### [cloud-architect-code-reviewer.md](cloud-architect-code-reviewer.md)
**Infrastructure code review** - Cloud-native patterns and deployment readiness
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the cloud-architect-code-reviewer subagent to review infrastructure code"`

### [monitoring-specialist.md](monitoring-specialist.md) 📊
**Observability architect** - Comprehensive monitoring and alerting systems
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the monitoring-specialist subagent to implement system monitoring"`

### [k8s-statefulset-specialist.md](k8s-statefulset-specialist.md)
**Kubernetes specialist** - StatefulSet patterns and container orchestration
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the k8s-statefulset-specialist subagent to configure Kubernetes"`

### [multi-tenant-architect.md](multi-tenant-architect.md)
**Multi-tenant architecture** - Enterprise SaaS patterns and tenant isolation
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the multi-tenant-architect subagent to design tenant isolation"`

### [devops-engineer.md](devops-engineer.md)
**DevOps automation** - CI/CD pipelines and infrastructure automation
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the devops-engineer subagent to automate deployment pipelines"`

## 🔍 Testing & Quality Assurance (4 agents)

### [testing-specialist.md](testing-specialist.md) 🧪
**Comprehensive testing** - TDD, quality gates, 95% coverage enforcement
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the testing-specialist subagent to implement comprehensive test coverage"`

### [qa-reviewer.md](qa-reviewer.md)
**Documentation quality** - ADR and technical documentation review
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite, LS
- **Usage**: `"Use the qa-reviewer subagent to review documentation quality"`

### [security-specialist.md](security-specialist.md) 🔒
**Enterprise security** - Multi-tenant isolation, compliance, vulnerability assessment
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the security-specialist subagent to implement security hardening"`

### [adr-compliance-specialist.md](adr-compliance-specialist.md)
**Architecture compliance** - ADR standard enforcement and quality scoring
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the adr-compliance-specialist subagent to validate ADR compliance"`

## 🏗️ Architecture & Standards (4 agents)

### [senior-architect.md](senior-architect.md) 🏛️
**Enterprise architecture** - System design and full-stack development leadership
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the senior-architect subagent for enterprise system design"`

### [software-design-architect.md](software-design-architect.md)
**Software design documentation** - SDD creation with C4 methodology
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the software-design-architect subagent to create system architecture documentation"`

### [software-design-document-specialist.md](software-design-document-specialist.md)
**SDD specialist** - Comprehensive system architecture documentation
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the software-design-document-specialist subagent for detailed technical specifications"`

### [coditect-adr-specialist.md](coditect-adr-specialist.md)
**CODITECT ADR compliance** - Project-specific architectural standards
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the coditect-adr-specialist subagent to enforce CODITECT standards"`

## 🔧 CODI System Integration (4 agents)

### [codi-devops-engineer.md](codi-devops-engineer.md)
**CODI infrastructure** - CI/CD automation for CODI systems
- **Tools**: Bash, Read, Write, Edit, Grep, Glob, TodoWrite
- **Usage**: `"Use the codi-devops-engineer subagent to manage CODI infrastructure"`

### [codi-documentation-writer.md](codi-documentation-writer.md)
**CODI documentation** - Technical documentation with enterprise quality standards
- **Tools**: Read, Write, Edit, Grep, Glob, TodoWrite, Bash
- **Usage**: `"Use the codi-documentation-writer subagent to create CODI system documentation"`

### [codi-qa-specialist.md](codi-qa-specialist.md)
**CODI quality assurance** - Testing strategies and quality gate implementation
- **Tools**: Bash, Read, Write, Edit, Grep, Glob, TodoWrite
- **Usage**: `"Use the codi-qa-specialist subagent to implement CODI quality standards"`

### [codi-test-engineer.md](codi-test-engineer.md)
**CODI test automation** - Advanced testing infrastructure and validation frameworks
- **Tools**: Bash, Read, Write, Edit, Grep, Glob, TodoWrite
- **Usage**: `"Use the codi-test-engineer subagent to build CODI test automation"`

## 💼 Business Intelligence & Analysis (3 agents)

### [business-intelligence-analyst.md](business-intelligence-analyst.md) 📈
**Strategic business analysis** - Market sizing, competitive analysis, financial modeling
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the business-intelligence-analyst subagent to analyze market opportunities"`

### [venture-capital-business-analyst.md](venture-capital-business-analyst.md)
**Investment analysis** - VC perspective, Series A-B valuations, SaaS metrics
- **Tools**: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
- **Usage**: `"Use the venture-capital-business-analyst subagent to assess investment readiness"`

## 📋 Project Management (1 agent)

### [project-organizer.md](project-organizer.md) 📁
**Project structure maintenance** - Production-ready directory organization
- **Tools**: Read, Glob, LS, Grep, Bash
- **Usage**: `"Use the project-organizer subagent to organize project files"`

## 🚀 Agent Usage Patterns

### **Method 1: Direct Explicit Invocation**
```bash
"Use the competitive-market-analyst subagent to research Cursor pricing strategy"
"Use the orchestrator subagent to coordinate multi-agent competitive analysis"
"Use the rust-expert-developer subagent to implement API authentication"
```

### **Method 2: Task Tool Proxy Pattern** 🆕
```python
Task(subagent_type="general-purpose", prompt="Use competitive-market-analyst subagent to research Cursor pricing strategy")
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate multi-agent competitive analysis")
Task(subagent_type="general-purpose", prompt="Use rust-expert-developer subagent to implement API authentication")
```

### **Method 3: Multi-Agent Coordination**
```bash
# Direct explicit
"Use the web-search-researcher subagent to gather external intelligence while having the thoughts-analyzer subagent review internal research"

# Task tool proxy
Task(subagent_type="general-purpose", prompt="Use web-search-researcher subagent to gather external intelligence while having thoughts-analyzer subagent review internal research")
```

### **Method 4: Orchestrated Workflows**
```bash
# Direct explicit
"Use the orchestrator subagent to implement user profile editing with backend API and frontend UI"

# Task tool proxy
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to implement user profile editing with backend API and frontend UI")
```

## 📋 Agent Management Commands

```bash
/agents                    # View all available agents
/agents create [name]      # Create new agent
/agents edit [name]        # Edit existing agent
/suggest-agent [task]      # Generate correct invocation syntax
/agent-dispatcher [task]   # Intelligent agent selection workflow
```

## 🎯 Agent Invocation Helper

**Need help with the correct syntax?** Use these workflow tools:

### Quick Invocation Generator
Use the prompt in [AGENT-INVOCATION-GENERATOR.md](../../AGENT-INVOCATION-GENERATOR.md):
```
Based on my 46-agent framework, what is the correct agent invocation syntax for:
"[YOUR TASK HERE]"
```

### Smart Agent Selection
```bash
/suggest-agent "implement user authentication with testing"
# Returns: "Use the orchestrator subagent to implement user authentication with backend API, security validation, and comprehensive test coverage"
```

### Intelligent Dispatcher
```bash  
/agent-dispatcher "research AI IDE market and analyze our competitive position"
# Returns: Multi-agent coordination strategy with proper syntax
```

## ⚙️ Configuration Details

**Directory Structure**: All agents in `.claude/agents/` for automatic recognition  
**YAML Frontmatter**: All 49 agents have complete `name`, `description`, `tools`, `model` fields  
**Tool Coverage**: Comprehensive tool access (Read, Write, Edit, Bash, Grep, Glob, TodoWrite, WebSearch, WebFetch)  
**Model Configuration**: All agents use `sonnet` model for optimal performance  

## 🔗 Related Documentation

- **Complete Agent Index**: [AGENT-INDEX.md](../AGENT-INDEX.md) - Full catalog with detailed capabilities
- **Project Configuration**: [CLAUDE.md](../../CLAUDE.md) - Main project instructions  
- **Command Inventory**: [../commands/README.md](../commands/README.md) - 52+ available commands
- **Evidence-Based Optimization**: [../../EVIDENCE-BASED-AGENT-OPTIMIZATION-PLAN.md](../../EVIDENCE-BASED-AGENT-OPTIMIZATION-PLAN.md)

---

**Agent Framework Status**: ✅ 46/49 agents properly configured and production-ready  
**Auto-Recognition**: ✅ Enabled via `.claude/agents/` directory structure  
**Quality Validation**: ✅ All agents have complete YAML frontmatter  
**Usage Ready**: ✅ Explicit invocation syntax: `"Use the [agent-name] subagent"`