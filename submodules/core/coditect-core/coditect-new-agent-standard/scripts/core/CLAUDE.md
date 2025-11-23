# Core Infrastructure - Claude Code Instructions

## 🎯 Purpose

The `core/` directory provides the foundational infrastructure for programmatic agent invocation using the **verified Task Tool Proxy Pattern**. These modules are the building blocks for all autonomous workflows.

## 📋 Core Principles for Claude Code

### **1. Always Use Task Tool Proxy Pattern**
All agent invocations MUST use the verified pattern implemented in `agent_caller.py`:

```python
# ✅ CORRECT: Use AgentCaller for consistent invocation
from agent_caller import AgentCaller, AgentType

caller = AgentCaller()
task = caller.call_agent(AgentType.ORCHESTRATOR, "coordinate workflow...")

# ❌ INCORRECT: Direct Task tool calling
# Task(subagent_type="orchestrator", prompt="coordinate workflow...")
```

### **2. Leverage Intelligent Analysis**
Always use `workflow_analyzer.py` for complex workflows requiring multiple agents:

```python
# ✅ RECOMMENDED: Analyze before executing
from workflow_analyzer import WorkflowAnalyzer

analyzer = WorkflowAnalyzer()
analysis = analyzer.analyze_workflow("implement secure authentication...")

# This provides:
# - Optimal agent selection with confidence scores
# - Required skills and commands identification  
# - Execution plan with phases and checkpoints
# - Resource and timeline estimates
```

### **3. Enable Autonomous Execution**
Use `autonomous_manager.py` for self-executing workflows with minimal supervision:

```python
# ✅ POWERFUL: Autonomous workflow execution
from autonomous_manager import AutonomousManager

manager = AutonomousManager()
tasks = manager.create_task_plan("build user profile system...")
final_report = manager.start_autonomous_execution()

# Provides:
# - Self-managing task execution
# - Progress reporting to orchestrator
# - Error recovery and retry logic
# - Cross-session state persistence
```

## 🔧 Component Usage Guidelines

### **`agent_caller.py` - When to Use**

#### **✅ ALWAYS use for:**
- Any agent invocation requiring progress tracking
- Multi-agent workflows needing coordination
- Sessions requiring resumability across conversations
- Production workflows needing error handling

#### **✅ PREFERRED for:**
- Single agent calls that might expand to multi-agent
- Workflows where you want session history
- Any agent calling in script templates

#### **Example Integration:**
```python
# In your Claude Code responses:
from scripts.core.agent_caller import AgentCaller, AgentType

caller = AgentCaller()

# For single agent tasks
security_task = caller.call_agent(
    AgentType.SECURITY_SPECIALIST,
    "conduct comprehensive security audit with SOC2 compliance validation"
)

# For orchestrated workflows
project_task = caller.call_orchestrator(
    workflow_description="Implement secure user authentication system",
    agents_needed=[AgentType.BACKEND_ARCHITECT, AgentType.SECURITY_SPECIALIST],
    task_breakdown=["API design", "Implementation", "Security validation"]
)
```

### **`workflow_analyzer.py` - When to Use**

#### **✅ ALWAYS use for:**
- Complex user requests involving multiple steps
- Workflows where optimal agent selection is unclear
- Resource planning and timeline estimation
- Unknown or custom workflow patterns

#### **✅ PREFERRED for:**
- User requests with ambiguous requirements
- Complex technical implementations
- Research projects with multiple streams
- Any workflow analysis before execution

#### **Example Integration:**
```python
# Analyze user request before execution
user_request = "Implement user profile management with security and testing"

analyzer = WorkflowAnalyzer()
analysis = analyzer.analyze_workflow(user_request)

# Use analysis results for optimal execution
recommended_agents = [rec.agent_type for rec in analysis["agent_recommendations"]]
execution_phases = analysis["execution_plan"]

print(f"Recommended approach: {len(recommended_agents)} agents across {len(execution_phases)} phases")
```

### **`autonomous_manager.py` - When to Use**

#### **✅ ALWAYS use for:**
- Workflows requiring autonomous execution
- Multi-session projects with state tracking
- Complex workflows needing progress reporting
- Production workflows with quality gates

#### **✅ PREFERRED for:**
- Long-running development tasks
- Research projects with multiple phases
- Any workflow benefiting from automation
- Workflows requiring orchestrator communication

#### **Example Integration:**
```python
# Set up autonomous execution for complex workflows
manager = AutonomousManager(session_id="user_auth_implementation")

# Create comprehensive task plan
tasks = manager.create_task_plan(
    "Implement secure user authentication with comprehensive testing and deployment"
)

# Register progress callback for user updates
def update_user(report):
    print(f"🎯 Phase: {report.current_phase} ({report.overall_progress:.1f}% complete)")
    if report.issues_encountered:
        print(f"⚠️ Issues: {len(report.issues_encountered)} items need attention")

manager.register_orchestrator_callback(update_user)

# Execute autonomously
manager.add_tasks(tasks)
final_report = manager.start_autonomous_execution()
```

## 📊 Integration with 47-Agent Framework

### **Agent Capabilities Mapping**
The core infrastructure maps to proven 47-agent patterns:

```python
# agent_caller.py uses these verified agent types:
AgentType.ORCHESTRATOR           # → orchestrator agent
AgentType.CODEBASE_ANALYZER      # → codebase-analyzer agent  
AgentType.SECURITY_SPECIALIST    # → security-specialist agent
AgentType.BACKEND_ARCHITECT      # → backend-architect agent
AgentType.RUST_EXPERT_DEVELOPER  # → rust-expert-developer agent
# ... and more
```

### **Skills Integration**
`workflow_analyzer.py` automatically suggests skills from the 47-agent framework:

```python
# Automatic skills mapping based on workflow analysis:
workflow_analysis = {
    "security_requirements": ["security-patterns", "compliance-validation"],
    "development_needs": ["production-patterns", "rust-backend-patterns"],
    "coordination_requirements": ["multi-agent-workflow", "communication-protocols"]
}
```

### **Commands Utilization**
`autonomous_manager.py` can execute commands from the 47-agent framework:

```python
# Commands automatically selected based on task type:
task_commands = {
    "planning": ["/create_plan", "/validate_plan"],
    "development": ["/feature_development", "/rust_scaffold"],
    "security": ["/security_sast", "/security_hardening"],
    "research": ["/research", "/smart-research"]
}
```

## 🎭 Orchestrator Communication Patterns

### **Progress Reporting**
All core components report to the orchestrator agent:

```python
# Automatic orchestrator updates
orchestrator_prompt = f"""
AUTONOMOUS EXECUTION PROGRESS REPORT

Session: {session_id}
Current Phase: {current_phase}
Overall Progress: {progress_percentage:.1f}%

Status Summary:
- Completed Tasks: {completed_count}
- Active Tasks: {active_count}
- Blocked Tasks: {blocked_count}

Next Actions:
{json.dumps(next_actions, indent=2)}

Request strategic guidance for next phase execution.
"""

# This calls the orchestrator agent automatically
orchestrator_task = caller.call_agent(AgentType.ORCHESTRATOR, orchestrator_prompt)
```

### **Quality Gate Integration**
Core components enforce quality gates:

```python
# Quality validation checkpoints
quality_gates = [
    {"phase": "Discovery", "criteria": "Requirements validated", "progress": 25},
    {"phase": "Implementation", "criteria": "Core functionality working", "progress": 50},
    {"phase": "Validation", "criteria": "Security and quality verified", "progress": 75},
    {"phase": "Completion", "criteria": "All deliverables ready", "progress": 100}
]
```

## 🔒 Security and Error Handling

### **Error Boundaries**
All core components implement comprehensive error handling:

```python
# Built-in error recovery patterns
def handle_task_error(self, task, error):
    task.error_log.append(f"{datetime.now().isoformat()}: {error}")
    task.retry_count += 1
    
    if task.retry_count < task.max_retry_attempts:
        # Retry with exponential backoff
        task.status = TaskStatus.PENDING
        self.task_queue.append(task)
    else:
        # Escalate to orchestrator for guidance
        task.status = TaskStatus.FAILED
        self.notify_orchestrator_of_failure(task, error)
```

### **Security Validation**
Never expose sensitive information in agent calls:

```python
# ✅ CORRECT: Sanitized agent calling
sanitized_prompt = prompt.replace(secret_key, "[REDACTED]")
task = caller.call_agent(agent_type, sanitized_prompt)

# ❌ INCORRECT: Exposing secrets
# task = caller.call_agent(agent_type, f"Deploy with key: {secret_key}")
```

## 📈 Performance Optimization

### **Token Management**
Core components optimize token usage:

```python
# Progressive context loading
if context_size > MAX_CONTEXT:
    # Use summary instead of full context
    context_summary = summarize_context(context)
    prompt = build_prompt_with_summary(task_description, context_summary)
```

### **Parallel Execution**
Enable parallel agent coordination:

```python
# Execute independent tasks in parallel
parallel_tasks = [task for task in task_queue if not task.dependencies]
for task in parallel_tasks:
    self.execute_task_async(task)
```

## 📝 Development Guidelines

### **When Building on Core Infrastructure**

1. **Always import from core modules** rather than reimplementing
2. **Use AgentType enum** for type safety and validation
3. **Implement progress tracking** with TaskProgress objects
4. **Include error handling** with retry mechanisms
5. **Document integration patterns** for future developers

### **Extension Patterns**

```python
# ✅ CORRECT: Extending core infrastructure
class CustomWorkflowManager(AutonomousManager):
    def __init__(self):
        super().__init__()
        self.custom_capabilities = self.load_custom_capabilities()
    
    def create_custom_task_plan(self, domain_specific_requirements):
        base_tasks = super().create_task_plan(requirements)
        custom_tasks = self.add_domain_specific_tasks(base_tasks)
        return custom_tasks
```

## 🎯 Success Metrics

Using the core infrastructure should provide:

1. **95%+ reliability** in agent invocation success
2. **Seamless cross-session continuity** with state persistence
3. **Intelligent agent selection** with >90% optimal matches
4. **Autonomous execution** requiring <10% manual intervention
5. **Comprehensive progress tracking** with real-time updates

---

**The Core Infrastructure transforms Claude Code into a reliable, autonomous agent orchestration platform with enterprise-grade capabilities for complex workflow management.**