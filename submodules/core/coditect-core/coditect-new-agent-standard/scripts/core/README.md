# Core Infrastructure Documentation

## 📋 Overview

The `core/` directory contains the foundational infrastructure for the Universal Agent Scripts Framework, providing standardized agent calling, intelligent workflow analysis, and autonomous task management.

## 🏗️ Components

### **`agent_caller.py`** - Standardized Agent Invocation
**Purpose**: Primary interface for calling agents using the verified Task Tool Proxy Pattern

**Key Features:**
- ✅ **Type-safe agent calling** with AgentType enum
- ✅ **Progress tracking** with TaskProgress objects
- ✅ **Session management** for cross-session continuity
- ✅ **Multi-agent orchestration** with coordination strategies
- ✅ **Error handling** and retry mechanisms

**Example Usage:**
```python
from agent_caller import AgentCaller, AgentType

caller = AgentCaller()

# Single agent call
task = caller.call_agent(
    AgentType.SECURITY_SPECIALIST,
    "conduct comprehensive security audit of authentication system"
)

# Multi-agent orchestration
orchestration = caller.call_orchestrator(
    workflow_description="Implement secure user profile management",
    agents_needed=[AgentType.BACKEND_ARCHITECT, AgentType.RUST_EXPERT_DEVELOPER],
    task_breakdown=["Design API endpoints", "Implement backend", "Security review"]
)
```

### **`workflow_analyzer.py`** - Intelligent Agent Selection
**Purpose**: Analyzes workflow requirements to determine optimal agent coordination strategy

**Key Features:**
- ✅ **Workflow requirement extraction** from natural language descriptions
- ✅ **Agent recommendation engine** with confidence scoring
- ✅ **Skills and commands mapping** for each workflow phase
- ✅ **Complexity assessment** and resource estimation
- ✅ **Execution plan generation** with detailed phase breakdown

**Example Usage:**
```python
from workflow_analyzer import WorkflowAnalyzer

analyzer = WorkflowAnalyzer()

# Analyze complex workflow
analysis = analyzer.analyze_workflow(
    "Implement secure user authentication with Rust backend, including registration, login, session management, and comprehensive security validation"
)

# Returns comprehensive analysis:
# - agent_recommendations with confidence scores
# - execution_plan with phases and checkpoints
# - resource_requirements and timeline estimates
```

### **`autonomous_manager.py`** - Self-Executing Task Management
**Purpose**: Manages autonomous task execution with orchestrator communication and progress tracking

**Key Features:**
- ✅ **Autonomous task planning** from workflow descriptions
- ✅ **Self-executing workflows** with minimal supervision
- ✅ **Progress tracking** with 25%, 50%, 75%, 100% checkpoints
- ✅ **Error recovery** with intelligent retry logic
- ✅ **Orchestrator communication** for status reporting
- ✅ **Cross-session persistence** for long-running workflows

**Example Usage:**
```python
from autonomous_manager import AutonomousManager

manager = AutonomousManager()

# Create autonomous execution plan
tasks = manager.create_task_plan(
    "Implement secure user authentication with comprehensive testing"
)

# Register orchestrator callback for progress updates
def progress_callback(report):
    print(f"Progress: {report.overall_progress:.1f}% - {report.current_phase}")

manager.register_orchestrator_callback(progress_callback)

# Start autonomous execution
final_report = manager.start_autonomous_execution()
```

## 🔧 Integration Patterns

### **Task Tool Proxy Pattern Implementation**
All core components use the verified Task Tool Proxy Pattern:

```python
# CORRECT: Verified working pattern
Task(subagent_type="general-purpose", prompt="Use orchestrator subagent to coordinate...")

# Built into AgentCaller automatically:
task_prompt = f"Use {agent_type.value} subagent to {prompt}"
```

### **47-Agent Framework Integration**
Core components integrate with the 47-agent framework:

- **Agent Capabilities**: Maps to proven agent patterns and expertise areas
- **Skills Integration**: Leverages production automation patterns
- **Commands Utilization**: Executes workflow automation commands
- **Context Awareness**: Uses agent-specific context for better results

### **Progress Tracking Integration**
Seamless integration with Claude Code's TodoWrite system:

```python
# Automatic todo creation and management
progress = TaskProgress(
    task_id="task_001",
    agent_type=AgentType.ORCHESTRATOR,
    status="in_progress",
    progress=50,
    checkpoint="Core implementation underway"
)
```

## 📊 Architecture Patterns

### **Layered Architecture**
```
┌─────────────────────────┐
│   Script Templates      │  ← High-level workflow orchestration
├─────────────────────────┤
│   Core Infrastructure   │  ← This layer: agent calling, analysis, management
├─────────────────────────┤
│   Task Tool Protocol    │  ← Claude Code Task tool integration
├─────────────────────────┤
│   47-Agent Framework    │  ← Proven agent patterns and capabilities
└─────────────────────────┘
```

### **Component Interaction Flow**
```
WorkflowAnalyzer → AgentCaller → AutonomousManager
       ↓               ↓              ↓
   Requirements    Invocation    Execution
   Analysis        & Progress    Management
       ↓               ↓              ↓
   Agent           Task           Progress
   Selection       Tracking       Reporting
```

## 🚀 Usage Patterns

### **Simple Agent Coordination**
Use `AgentCaller` for straightforward agent invocation with progress tracking.

### **Intelligent Workflow Planning**
Use `WorkflowAnalyzer` to understand complex requirements and get agent recommendations.

### **Autonomous Execution**
Use `AutonomousManager` for self-executing workflows with minimal supervision.

### **Combined Usage**
Most templates combine all three for complete workflow automation:

```python
# Template pattern: Analysis → Calling → Autonomous Execution
analyzer = WorkflowAnalyzer()
caller = AgentCaller()
manager = AutonomousManager()

# 1. Analyze requirements
analysis = analyzer.analyze_workflow(description)

# 2. Set up calling infrastructure  
caller.setup_session(analysis)

# 3. Execute autonomously
tasks = manager.create_task_plan(description, analysis)
manager.add_tasks(tasks)
final_report = manager.start_autonomous_execution()
```

## 🔒 Quality Standards

### **Error Handling**
- All components include comprehensive error handling
- Retry logic with exponential backoff
- Graceful degradation for partial failures
- Error logging and recovery guidance

### **Performance**
- Efficient token usage with progressive context loading
- Parallel agent execution where possible
- Checkpoint-based resumption for long workflows
- Resource monitoring and optimization

### **Testing**
- Unit tests for all public interfaces
- Integration tests with actual agent calling
- Performance benchmarks for large workflows
- Error scenario validation

## 📖 API Documentation

### **AgentCaller Class**
- `call_agent(agent_type, prompt, task_id)` - Single agent invocation
- `call_orchestrator(workflow_description, agents_needed, task_breakdown)` - Multi-agent coordination
- `get_task_status(task_id)` - Progress monitoring
- `export_session_report()` - Session summary

### **WorkflowAnalyzer Class**
- `analyze_workflow(description, context)` - Comprehensive workflow analysis
- `recommend_agents(requirements)` - Agent selection with confidence scores
- `generate_execution_plan(recommendations)` - Phase-based execution planning

### **AutonomousManager Class**
- `create_task_plan(workflow_description, context)` - Autonomous task planning
- `start_autonomous_execution()` - Self-executing workflow management
- `register_orchestrator_callback(callback)` - Progress reporting setup
- `export_execution_summary()` - Complete execution report

## 🔗 Related Documentation

- **[Scripts Framework Overview](../README.md)** - Framework architecture and benefits
- **[Template Documentation](../templates/README.md)** - High-level workflow templates
- **[Orchestration Guide](../workflows/README.md)** - Intelligent workflow dispatch

---

**The Core Infrastructure provides the foundational building blocks for enterprise-grade autonomous agent workflows with comprehensive progress tracking and intelligent coordination.**