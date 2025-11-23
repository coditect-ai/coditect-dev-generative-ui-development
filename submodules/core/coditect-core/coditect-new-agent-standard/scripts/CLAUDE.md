# Scripts Framework - Claude Code Instructions

## 🎯 Purpose

This directory contains the **Universal Agent Scripts Framework** - production-ready infrastructure for programmatic agent invocation and autonomous workflow management using the verified **Task Tool Proxy Pattern**.

## 📋 Claude Code Integration

### **Core Principle: Task Tool Proxy Pattern**
All agent invocations MUST use the verified protocol:

```python
# CORRECT: Verified working pattern
Task(subagent_type="general-purpose", prompt="Use [agent-name] subagent to [specific task]")

# INCORRECT: Direct calling (doesn't work)
Task(subagent_type="agent-name", prompt="[task]")
```

### **Agent Calling Standards**
When using the scripts framework:

1. **Always use AgentCaller class** for consistent invocation
2. **Follow AgentType enum** for type safety and validation  
3. **Include detailed task context** for autonomous execution
4. **Implement progress tracking** with TodoWrite integration
5. **Handle errors gracefully** with retry logic

## 🔧 Framework Components

### **Core Infrastructure (`core/`)**

#### **`agent_caller.py`**
- **Purpose**: Standardized agent calling using Task Tool Proxy Pattern
- **Usage**: Primary interface for all agent invocations
- **Key Features**: Progress tracking, session management, type safety

#### **`workflow_analyzer.py`**
- **Purpose**: Intelligent analysis of user requests to determine optimal agents/skills/commands
- **Usage**: Automatic agent selection for complex workflows
- **Key Features**: Context awareness, complexity assessment, resource estimation

#### **`autonomous_manager.py`**
- **Purpose**: Self-executing task management with orchestrator communication
- **Usage**: Autonomous workflow execution with minimal supervision
- **Key Features**: Multi-session tracking, error recovery, progress reporting

### **Templates (`templates/`)**

#### **`project_manager_script.py`**
- **Purpose**: Complete project management workflow template
- **Usage**: End-to-end project execution with autonomous coordination
- **Key Features**: Phase tracking, quality gates, deliverable generation

#### **`research_workflow_script.py`**
- **Purpose**: Comprehensive research automation template
- **Usage**: Multi-stream research with synthesis and analysis
- **Key Features**: Web research, competitive analysis, executive summaries

### **Workflows (`workflows/`)**

#### **`orchestrator_dispatcher.py`**
- **Purpose**: Intelligent workflow dispatch and custom script generation
- **Usage**: Analyzes requests and selects/generates appropriate workflows
- **Key Features**: Template selection, custom script generation, autonomous execution

## 🎭 Agent Coordination Patterns

### **Single Agent Invocation**
```python
from scripts.core.agent_caller import AgentCaller, AgentType

caller = AgentCaller()
task = caller.call_agent(
    AgentType.SECURITY_SPECIALIST,
    "conduct comprehensive security audit of authentication system with SOC2 compliance validation"
)
```

### **Multi-Agent Orchestration**
```python
orchestration = caller.call_orchestrator(
    workflow_description="Implement secure user profile management",
    agents_needed=[AgentType.BACKEND_ARCHITECT, AgentType.RUST_EXPERT_DEVELOPER, AgentType.SECURITY_SPECIALIST],
    task_breakdown=[
        "Design API endpoints with security validation",
        "Implement backend with Rust performance optimization", 
        "Conduct security review and compliance validation"
    ]
)
```

### **Intelligent Workflow Dispatch**
```python
from scripts.workflows.orchestrator_dispatcher import orchestrate_workflow

result = orchestrate_workflow(
    "Research competitive landscape for AI coding assistants and develop pricing strategy",
    context={
        "research_scope": "Global market analysis",
        "deliverable_format": "Executive summary with strategic recommendations",
        "timeline": "Comprehensive analysis within 45 minutes"
    }
)
```

## 📊 Progress Tracking Integration

### **TodoWrite Integration**
All scripts integrate with Claude Code's TodoWrite tool for progress tracking:

```python
# Automatic todo creation from task breakdown
todos = [
    {"content": "Analyze user requirements", "status": "in_progress", "priority": "high"},
    {"content": "Design API architecture", "status": "pending", "priority": "high"},
    {"content": "Implement security validation", "status": "pending", "priority": "medium"}
]
```

### **Cross-Session Persistence** 
- Session state automatically saved and resumable
- Progress checkpoints (25%, 50%, 75%, 100%)
- Error recovery and retry mechanisms
- Comprehensive execution logging

## 🚀 Usage Guidelines for Claude Code

### **When to Use This Framework**

#### **✅ ALWAYS USE for:**
- Complex multi-step workflows requiring agent coordination
- Project management with cross-session tracking
- Research projects requiring synthesis of multiple sources
- Custom workflows that don't fit standard patterns
- Autonomous execution with minimal supervision

#### **✅ PREFERRED for:**
- Any workflow involving more than 2 agents
- Tasks requiring structured progress tracking
- Development projects with multiple phases
- Security audits requiring comprehensive validation

#### **⚠️ CONSIDER for:**
- Simple single-agent tasks (may be overkill)
- Quick one-off analyses (use direct Task tool)

### **Framework Selection Logic**

1. **Simple Request** → Direct Task tool usage
2. **Complex Workflow** → Use `orchestrator_dispatcher.py`
3. **Known Pattern** → Use appropriate template script
4. **Research Focus** → Use `research_workflow_script.py`
5. **Project Management** → Use `project_manager_script.py`

## 🔒 Security and Quality Standards

### **Security Requirements**
- Never expose secrets or credentials in scripts
- Validate all inputs before agent invocation
- Use secure communication patterns for agent coordination
- Implement proper error boundaries

### **Quality Standards**
- All scripts must include comprehensive error handling
- Progress tracking required for multi-step workflows  
- Documentation and examples for all public functions
- Type hints for better code maintainability

### **Testing Requirements**
- Validate agent calling patterns work correctly
- Test error recovery and retry mechanisms
- Verify cross-session state persistence
- Validate integration with TodoWrite system

## 🔄 Workflow Integration with 47-Agent Framework

### **Skills Integration**
Scripts automatically leverage skills from `agents-reference-47/skills/`:
- **multi-agent-workflow** - Coordination patterns
- **production-patterns** - Error handling and observability
- **security-patterns** - Security validation frameworks

### **Commands Integration**
Scripts utilize commands from `agents-reference-47/commands/`:
- **Project planning**: `/create_plan`, `/validate_plan`, `/implement_plan`
- **Research workflows**: `/research`, `/smart-research`, `/multi-agent-research`
- **Security operations**: `/security_sast`, `/security_hardening`

## 📈 Performance Optimization

### **Token Management**
- Intelligent context management to prevent token overflow
- Progressive disclosure of information as needed
- Efficient agent coordination to minimize redundancy

### **Execution Efficiency**
- Parallel agent execution where possible
- Checkpoint-based resumption for long workflows
- Resource usage monitoring and optimization

## 🧩 Extension Patterns

### **Adding New Templates**
1. Follow existing template structure
2. Implement standard lifecycle methods
3. Include autonomous execution capabilities
4. Add comprehensive documentation

### **Custom Agent Integration**
1. Extend AgentType enum for new agents
2. Update agent_capabilities mapping
3. Test integration with existing workflows
4. Document usage patterns

## 📝 Development Guidelines

### **Code Standards**
- Follow Python PEP 8 style guidelines
- Use type hints for all function signatures
- Include docstrings for all public methods
- Implement comprehensive error handling

### **Documentation Requirements**
- README.md with usage examples
- Inline code documentation
- Integration patterns and best practices
- Performance characteristics and limitations

---

## 🎯 Key Success Metrics

The Scripts Framework should enable:

1. **95%+ autonomous execution** for complex workflows
2. **Cross-session continuity** with state persistence
3. **Intelligent agent coordination** with minimal manual intervention
4. **Production-grade reliability** with comprehensive error handling
5. **Extensible architecture** for rapid workflow development

**This framework transforms Claude Code from a conversational tool into a comprehensive autonomous development and research platform with enterprise-grade workflow management capabilities.**