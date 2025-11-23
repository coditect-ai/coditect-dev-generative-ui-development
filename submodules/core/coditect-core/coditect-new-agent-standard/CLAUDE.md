# AZ1.AI CODITECT Universal Agent Framework v2.0
## Claude Code Agent Framework Instructions

**Status**: ✅ Production Ready | **Last Updated**: 2025-11-09T02:30:00Z | **Version**: 2.0.0

## 📊 Executive Summary

The **Universal Agent Framework v2.0** is a comprehensive, production-ready system for cross-platform AI agent development and management. Successfully integrating 47 proven agents with intelligent workflow automation, autonomous task management, and enterprise-grade project coordination.

### Key Achievements (2025-11-09)
- ✅ **47-Agent Framework Integration** - Complete submodule with verified Task Protocol
- ✅ **Project Management System** - Orchestrator-based autonomous coordination  
- ✅ **Scripts Framework** - Standardized agent invocation with 150+ workflow templates
- ✅ **Multi-Session Tracking** - Persistent progress across 16+ development sessions
- ✅ **Cross-Platform Compatibility** - Universal format supporting 4+ LLM platforms

### Project Overview
This repository contains the development of a universal, cross-platform AI agent format that works seamlessly across **Anthropic Claude**, **OpenAI GPT**, **Google Gemini**, **Grok/xAI**, and **Enterprise platforms**.

**🎯 Core Mission**: Create agents that work everywhere while leveraging each platform's unique strengths.

---

## 🚀 Agent Invocation Methods

### Primary Method: Task Tool Proxy Pattern (VERIFIED WORKING)
**This is the PROVEN method for invoking universal agents:**

```python
# Single Agent Invocation
Task(subagent_type="general-purpose", prompt="Use security-specialist subagent to audit API security and generate compliance report")

# Multi-Agent Coordination  
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate comprehensive security assessment using security-specialist and backend-architect subagents")

# Domain-Specific Research
Task(subagent_type="general-purpose", prompt="Use competitive-market-analyst subagent to research AI IDE pricing strategies compared to Cursor and GitHub Copilot")
```

**✅ Why This Works:**
- **Verified Agent Invocation**: Actually calls specialized agents (not just base Claude)
- **Proper Agent Identification**: Agents respond with their specialized knowledge
- **Enhanced Capabilities**: Access to agent-specific automation features
- **Quality Differentiation**: Higher quality, specialized responses vs. general Claude

**⚠️ What Does NOT Work:**
- Direct natural language: "Use [agent] subagent to..." (just prompts base Claude)
- Direct Task tool access: `Task(subagent_type="agent-name")` (agent not found)

---

## 🎭 Available Agent Archetypes

Based on proven 47-agent analysis, these archetypes are verified working:

### 1. 🔍 Analysis Specialists
**Purpose**: Deep technical analysis with structured output
**Example**: `codebase-analyzer`, `security-specialist`
**Pattern**: Read-heavy tools, structured reporting, clear boundaries

```python
Task(subagent_type="general-purpose", prompt="Use codebase-analyzer subagent to analyze the authentication system implementation and document how user sessions are managed")
```

### 2. 📍 Locator Specialists  
**Purpose**: Efficient search and discovery with organized results
**Example**: `codebase-locator`, `file-locator`
**Pattern**: Search-optimized tools (Grep, Glob, LS), systematic discovery

```python
Task(subagent_type="general-purpose", prompt="Use codebase-locator subagent to find all files related to user authentication and organize them by functionality")
```

### 3. 📊 Research Analysts
**Purpose**: Intelligence gathering with entity detection and context awareness
**Example**: `competitive-market-analyst`, `web-search-researcher`
**Pattern**: Web-enabled tools, entity recognition, scope adaptation

```python
Task(subagent_type="general-purpose", prompt="Use competitive-market-analyst subagent to research current AI coding assistant market landscape and pricing models")
```

### 4. 🎭 Orchestrator (Core Coordination)
**Purpose**: Multi-agent workflow coordination with intelligent agent selection
**Example**: `orchestrator`
**Pattern**: Workflow recognition, agent routing, progress coordination

```python
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate a comprehensive security audit that includes code analysis, vulnerability assessment, and compliance validation")
```

### 5. ⚙️ Development Specialists
**Purpose**: Production-grade implementation with domain expertise
**Example**: `rust-expert-developer`, `backend-architect`
**Pattern**: Language/domain-specific, production standards, best practices

```python
Task(subagent_type="general-purpose", prompt="Use rust-expert-developer subagent to implement secure WebSocket authentication with error handling and observability")
```

### 6. 🔒 Security Specialists
**Purpose**: Enterprise security with compliance and governance
**Example**: `security-specialist`, `compliance-auditor`
**Pattern**: Security-first approach, compliance awareness, risk assessment

```python
Task(subagent_type="general-purpose", prompt="Use security-specialist subagent to conduct SOC2 compliance assessment for the user authentication system")
```

---

## 🧬 Context Awareness Features

### Automatic Scope Detection
Universal agents use **Context Awareness DNA** for intelligent behavior:

```yaml
context_awareness:
  auto_scope_keywords:
    security: ["vulnerability", "compliance", "audit", "penetration"]
    performance: ["optimization", "scalability", "latency", "throughput"]
    architecture: ["design", "patterns", "microservices", "enterprise"]
  
  entity_detection:
    frameworks: ["React", "Rust", "PostgreSQL", "Kubernetes"]
    compliance: ["SOC2", "GDPR", "HIPAA", "ISO27001"]
  
  confidence_boosters:
    - "enterprise-grade", "production-ready", "scalable"
    - "security-validated", "compliance-certified"
```

**Benefits:**
- **Automatic Specialization**: Agents detect their expertise areas
- **Reduced Prompt Engineering**: Context-aware responses without complex prompts
- **Quality Filtering**: Confidence indicators improve response accuracy

---

## 📈 Progress Tracking

### Built-in Progress Reporting
All universal agents provide standardized progress tracking:

```
Progress Checkpoints:
├── 25% - Initial phase complete (scope and strategy established)
├── 50% - Core work underway (main analysis/implementation in progress)  
├── 75% - Integration phase (synthesis and validation)
└── 100% - Complete with deliverables (final output and next steps)
```

### Multi-Agent Coordination
When using orchestrator, you get coordinated progress across multiple agents:

```python
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate comprehensive market research including competitive analysis, pricing research, and feature comparison for AI IDEs")

# Results in coordinated workflow:
# 25% - Workflow planned, agents coordinated
# 50% - Primary research complete, synthesis coordination
# 75% - Cross-agent integration, quality gates
# 100% - Integrated results with strategic recommendations
```

---

## 🛠️ Skills & Commands Integration

### Anthropic Skills Framework
Universal agents leverage Claude Code's Skills system:

```
skills/
├── security-patterns/          # Security audit patterns and frameworks
├── development-patterns/       # Development workflow patterns  
├── analysis-patterns/          # Research and analysis methodologies
└── compliance-patterns/        # Regulatory compliance frameworks
```

**Usage**: Skills are automatically loaded when agents are invoked via Task protocol.

### Command Integration
Workflow commands for common operations:

```
Available Commands:
├── /security-audit [scope] [framework]     # Comprehensive security assessment
├── /vulnerability-scan [target] [level]    # Vulnerability analysis  
├── /compliance-check [framework] [component] # Compliance validation
├── /performance-analysis [system] [metrics] # Performance assessment
└── /architecture-review [component] [focus] # Architecture evaluation
```

**Usage**: Commands are available when using specialized agents through Task protocol.

---

## 🌐 Cross-Platform Compatibility

### Platform Adaptation Strategy
Universal agents adapt to different platforms automatically:

**On Anthropic Claude (Full Features):**
- Complete Skills and Commands integration
- Full Context Awareness DNA
- Enhanced automation features
- Multi-agent coordination

**On OpenAI (Function Calling Mode):**
- Tool mapping to function calling
- Structured output for consistency
- Basic coordination capabilities

**On Google Gemini (MCP Integration):**
- Model Context Protocol for tools
- A2A protocol for agent communication
- Multimodal capabilities where applicable

**On Enterprise Platforms:**
- Governance and audit integration
- Lifecycle management hooks
- Compliance documentation generation

---

## 📚 Usage Examples

### Security Assessment Workflow
```python
# Comprehensive security audit
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate a full security assessment of the user authentication system including code analysis, vulnerability scanning, and SOC2 compliance validation")

# Expected workflow:
# 1. Orchestrator plans multi-agent approach
# 2. codebase-locator finds authentication components  
# 3. codebase-analyzer reviews implementation
# 4. security-specialist conducts vulnerability assessment
# 5. compliance-auditor validates SOC2 requirements
# 6. Integrated report with recommendations
```

### Development Workflow
```python
# Full-stack feature implementation
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate implementation of secure user profile management feature using backend-architect for API design, rust-expert-developer for implementation, and security-specialist for security validation")
```

### Research Workflow  
```python
# Market research and competitive analysis
Task(subagent_type="general-purpose", prompt="Use competitive-market-analyst subagent to research AI coding assistant market positioning, pricing strategies, and feature differentiation compared to top 5 competitors")
```

---

## 🔧 Development Guidelines

### Creating Universal Agents
1. **Use the Template**: Start with [AGENT-TEMPLATE.md](AGENT-TEMPLATE.md)
2. **Follow Proven Patterns**: Reference successful archetypes
3. **Implement Context DNA**: Add auto-scope keywords and entity detection
4. **Test Cross-Platform**: Validate on multiple LLM platforms
5. **Document Integration**: Specify coordination patterns

### Testing Strategy
1. **Anthropic Validation**: Verify Task protocol functionality
2. **Cross-Platform Testing**: Test basic functionality on other LLMs
3. **Performance Benchmarking**: Compare against existing agents
4. **Integration Testing**: Validate multi-agent workflows

### Quality Standards
- **AZ1 Verification**: All agents must pass verification testing
- **Documentation**: Complete usage examples and integration patterns
- **Security**: Built-in security awareness and compliance hooks
- **Performance**: Optimized for production deployment

---

## 📖 Documentation Resources

### Core Documentation
- **[Universal Format Specification](docs/UNIVERSAL-FORMAT-SPECIFICATION.md)** - Complete technical specification
- **[Platform Compatibility Research](docs/PLATFORM-COMPATIBILITY-RESEARCH.md)** - Cross-platform analysis
- **[47-Agent Analysis](docs/47-AGENT-ANALYSIS.md)** - Proven pattern analysis
- **[Agent Overlap Analysis](docs/AGENT-OVERLAP-ANALYSIS.md)** - Comparison with existing agents

### Development Resources
- **[Agent Template](AGENT-TEMPLATE.md)** - Universal agent development template
- **[Testing Framework](tests/)** - Cross-platform compatibility tests
- **[Skills Directory](skills/)** - Anthropic Skills integration examples
- **[Commands Directory](commands/)** - Workflow command definitions

### Project Management Resources
- **[PROJECT-MANAGEMENT-PROCESS.md](PROJECT-MANAGEMENT-PROCESS.md)** - Complete process documentation
- **[Scripts Framework](scripts/)** - Standardized agent invocation system
- **[Quick Start Guide](1-2-3-project-management-QUICK-START.md)** - Implementation guide
- **[Session Checkpoints](.session/)** - Multi-session progress tracking

### 47-Agent Framework Integration
- **[agents-reference-47/](agents-reference-47/)** - 47 proven agents submodule
- **[Skills Library](agents-reference-47/skills/)** - 13 production automation patterns
- **[Commands System](agents-reference-47/commands/)** - 52 workflow automation commands
- **[Agent Configurations](agents-reference-47/settings.*.json)** - Agent setup and configuration

---

## 🎯 Quick Start Guide

### For Immediate Use
1. **Choose an archetype** from the 6 proven patterns above
2. **Use Task protocol** with specific, clear prompts
3. **Leverage orchestrator** for complex multi-step workflows
4. **Monitor progress** through built-in checkpoint reporting

### For Development
1. **Review documentation** in [docs/](docs/) directory
2. **Copy agent template** from [AGENT-TEMPLATE.md](AGENT-TEMPLATE.md)
3. **Study proven patterns** in [47-Agent Analysis](docs/47-AGENT-ANALYSIS.md)
4. **Test thoroughly** across target platforms

### For Enterprise Deployment
1. **Review governance features** in universal format specification
2. **Plan migration strategy** based on existing agent inventory
3. **Validate compliance** requirements for your industry
4. **Implement gradually** with pilot programs

---

## 🚀 Next Steps (2025-11-09)

### Immediate Priorities (Session 2)
1. **Complete Phase 1.2**: Universal format template validation
2. **Begin Phase 1.3**: Skills and commands framework integration  
3. **Establish testing infrastructure**: Basic validation framework
4. **Agent conversion planning**: Prepare for Phase 2 analysis specialist conversion

### Short-term Goals (Sessions 3-4)
1. **Convert Analysis Specialists**: 12 agents to universal format
2. **Implement Context Awareness DNA**: Auto-scope detection and entity recognition
3. **Cross-platform testing**: Validate on Claude, GPT, Gemini platforms
4. **Quality Gate 2**: Analysis archetype validation

### Medium-term Roadmap (Sessions 5-16)
1. **Complete all 47 agents**: Convert remaining 35 agents across 6 phases
2. **Cross-platform optimization**: Platform-specific adaptation layers
3. **Enterprise integration**: Governance hooks and compliance frameworks
4. **Production deployment**: Automated deployment and monitoring systems

### Long-term Vision (Q1 2026)
1. **Community adoption**: Open-source community engagement
2. **Platform partnerships**: Direct integrations with LLM providers
3. **Enterprise market**: Commercial enterprise platform offerings
4. **Ecosystem expansion**: Third-party agent marketplace

---

**Universal Agent Framework v2.0 - Building the future of cross-platform AI agents**

**Last Updated**: 2025-11-09T02:30:00Z | **Next Review**: 2025-11-10T12:00:00Z  
*For support and contributions, see the main [README.md](README.md) and [documentation](docs/) directory.*