# Scripts Framework Documentation

## 📋 Overview

This directory contains the complete **Universal Agent Scripts Framework** - a comprehensive system for programmatic agent invocation, workflow automation, and autonomous task management using the verified Task Tool Proxy Pattern.

## 🏗️ Architecture

```
scripts/
├── core/                    # Core infrastructure for agent calling
│   ├── agent_caller.py      # Standardized Task Tool Proxy Pattern implementation  
│   ├── workflow_analyzer.py # Intelligent workflow analysis & agent selection
│   └── autonomous_manager.py # Self-executing task management with progress tracking
├── templates/               # Reusable workflow script templates  
│   ├── project_manager_script.py # Complete project management workflow
│   └── research_workflow_script.py # Comprehensive research automation
├── workflows/              # Orchestration and intelligent dispatch
│   └── orchestrator_dispatcher.py # Intelligent workflow dispatch & custom script generation
├── utils/                  # Supporting utilities (future expansion)
├── README.md              # This documentation
└── CLAUDE.md              # Claude Code agent instructions
```

## 🎯 Key Components

### **Core Infrastructure (`core/`)**
- **Agent calling framework** using Task Tool Proxy Pattern
- **Workflow analysis** for intelligent agent selection
- **Autonomous task management** with progress tracking

### **Script Templates (`templates/`)**
- **Reusable workflow scripts** for common patterns
- **Project management automation** with multi-session tracking
- **Research workflow coordination** with multi-agent synthesis

### **Orchestration Engine (`workflows/`)**
- **Intelligent workflow dispatch** based on request analysis
- **Template selection** or **custom script generation**
- **End-to-end automation** with autonomous execution

## 🚀 Quick Start

### **1. Simple Agent Calling**
```python
from scripts.core.agent_caller import AgentCaller, AgentType

caller = AgentCaller()
task = caller.call_agent(
    AgentType.ORCHESTRATOR, 
    "coordinate secure authentication implementation"
)
```

### **2. Intelligent Workflow Dispatch**
```python
from scripts.workflows.orchestrator_dispatcher import orchestrate_workflow

result = orchestrate_workflow(
    "Implement user profile management with security validation",
    context={"tech_stack": ["Rust", "React", "PostgreSQL"]}
)
```

### **3. Template-Based Execution**
```python
from scripts.templates.project_manager_script import ProjectManagerScript

project = ProjectManagerScript(
    project_name="authentication_system",
    description="Secure user authentication with JWT and OAuth2"
)
deliverables = project.run_complete_workflow()
```

## 🔧 Usage Patterns

### **For Project Management**
- Use `orchestrator_dispatcher.py` for automatic workflow planning
- Use `project_manager_script.py` for comprehensive project execution
- Leverage autonomous task management for multi-session continuity

### **For Research Projects**  
- Use `research_workflow_script.py` for multi-stream research coordination
- Combine web research, competitive analysis, and codebase analysis
- Generate executive summaries with strategic recommendations

### **For Custom Workflows**
- Let `orchestrator_dispatcher.py` generate custom scripts automatically
- Use `workflow_analyzer.py` to understand agent requirements
- Build on existing templates for consistency

## 📊 Integration with 47-Agent Framework

This scripts framework integrates seamlessly with the **47-Agent Framework** submodule:

- **Agents**: Uses all 47 verified agents through Task protocol
- **Skills**: Leverages production automation patterns from skills library
- **Commands**: Executes workflow automation using command system
- **Coordination**: Orchestrates multi-agent workflows with progress tracking

## 🎯 Benefits

### **Standardization**
- Consistent agent calling patterns across all workflows
- Reusable script templates for common use cases
- Standardized progress tracking and reporting

### **Automation**
- Autonomous task execution with minimal supervision
- Intelligent agent selection based on workflow analysis
- Multi-session progress tracking with state persistence

### **Scalability**
- Modular architecture for easy extension
- Template-based approach for rapid workflow development
- Orchestrator coordination for complex multi-agent workflows

## 📖 Documentation

Each subdirectory contains:
- **README.md** - Technical documentation and usage examples
- **CLAUDE.md** - Claude Code specific instructions and integration patterns
- **Example scripts** - Working examples for common patterns

## 🔗 Related Documentation

- **[1-2-3-project-management-QUICK-START.md](../1-2-3-project-management-QUICK-START.md)** - Complete quick start guide
- **[Universal Format Specification](../docs/UNIVERSAL-FORMAT-SPECIFICATION.md)** - Technical specifications
- **[47-Agent Analysis](../docs/47-AGENT-ANALYSIS.md)** - Proven pattern analysis

## 🤝 Contributing

When adding new scripts or templates:

1. **Follow the established patterns** in existing templates
2. **Use the Task Tool Proxy Pattern** for agent calling
3. **Implement progress tracking** with TodoWrite integration
4. **Include comprehensive documentation** with usage examples
5. **Test with multiple workflow types** to ensure reliability

## 📝 Notes

- All scripts use **Python 3.7+** with standard libraries
- **No external dependencies** beyond the core Claude Code framework
- **Cross-platform compatibility** for Linux, macOS, and Windows
- **Production-ready** with error handling and retry logic

---

**The Scripts Framework provides the complete infrastructure for building autonomous, multi-agent workflows with enterprise-grade reliability and comprehensive progress tracking.**