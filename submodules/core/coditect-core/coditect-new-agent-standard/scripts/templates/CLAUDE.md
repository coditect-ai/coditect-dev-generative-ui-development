# Script Templates - Claude Code Instructions

## 🎯 Purpose

The `templates/` directory contains **production-ready workflow script templates** that provide complete, end-to-end automation for common workflow patterns using autonomous agent coordination.

## 📋 Claude Code Integration Guidelines

### **Template Philosophy**
Templates represent **complete workflow solutions** that Claude Code should use for:

- **Complex multi-step projects** requiring coordination across multiple agents
- **Autonomous execution** with minimal manual intervention
- **Cross-session continuity** for long-running development projects
- **Professional deliverable generation** with comprehensive documentation

### **When to Use Templates**

#### **✅ ALWAYS use `project_manager_script.py` for:**
- Full-stack feature development (backend + frontend + testing)
- System implementation projects (authentication, user management, etc.)
- Multi-phase development workflows requiring security validation
- Enterprise-grade projects needing documentation and compliance
- Any project requiring cross-session progress tracking

#### **✅ ALWAYS use `research_workflow_script.py` for:**
- Market research and competitive landscape analysis  
- Technology evaluation and comparison studies
- Business intelligence and strategic planning
- Multi-source research requiring synthesis and executive summaries

#### **✅ PREFER templates over direct agent calling when:**
- User requests involve multiple agents or complex coordination
- Workflows require structured progress tracking with checkboxes
- Professional deliverables are expected (reports, documentation, etc.)
- Cross-session continuity is beneficial for the user

## 🔧 Template Integration Patterns

### **Project Management Template Usage**

```python
# For complex development projects
from scripts.templates.project_manager_script import ProjectManagerScript

project = ProjectManagerScript(
    project_name="secure_user_authentication",
    description="Implement comprehensive user authentication system with JWT, OAuth2, session management, security validation, and comprehensive testing"
)

# Add rich context for better execution
context = {
    "tech_stack": ["Rust", "PostgreSQL", "Redis", "React"],
    "security_requirements": ["OAuth2", "JWT", "RBAC", "Rate limiting"],
    "compliance_needs": ["SOC2", "GDPR"],
    "deployment_target": "AWS ECS with auto-scaling",
    "testing_requirements": ["Unit tests", "Integration tests", "Security tests"],
    "documentation_needs": ["API docs", "Security guide", "Deployment guide"]
}

# Execute complete autonomous workflow
deliverables = project.run_complete_workflow(context)

# Result provides:
# - Complete implementation with all phases
# - Progress tracking with checkboxes
# - Quality gates and validation
# - Professional documentation package
# - Deployment-ready artifacts
```

### **Research Template Usage**

```python
# For comprehensive research projects  
from scripts.templates.research_workflow_script import ResearchWorkflowScript

research = ResearchWorkflowScript(
    research_topic="AI-powered development tools competitive positioning",
    scope="comprehensive"
)

# Execute multi-stream research workflow
deliverables = research.run_complete_research_workflow(
    requirements={
        "target_market": "Enterprise development teams",
        "geographic_scope": "Global market analysis",
        "time_horizon": "2025-2026 strategic planning",
        "decision_context": "Product positioning and pricing strategy"
    },
    research_areas=[
        "AI coding assistant market size and growth trends",
        "Developer productivity tools adoption patterns",
        "Enterprise software procurement decision factors",
        "Technology integration preferences and barriers"
    ],
    competitors=[
        "GitHub Copilot", "Cursor AI IDE", "JetBrains AI Assistant",
        "Amazon CodeWhisperer", "Tabnine", "Replit AI"
    ],
    codebase_areas=[
        "AI integration patterns in development tools",
        "User experience optimization for AI features",
        "Performance optimization for real-time AI assistance"
    ]
)

# Result provides:
# - Executive summary with strategic insights
# - Detailed competitive landscape analysis  
# - Market opportunity assessment
# - Strategic positioning recommendations
# - Supporting research materials and citations
```

## 🎭 Orchestrator Integration

### **Templates as Orchestrator Tools**
Templates serve as **intelligent orchestrator tools** that Claude Code can leverage:

#### **Automatic Template Selection**
```python
# Claude Code can analyze user requests and automatically select templates:

user_request = "Build a secure user profile management system with React frontend"

# Analysis determines this needs project_manager_script.py:
# - Multi-component development (backend + frontend)
# - Security requirements 
# - Testing and validation needs
# - Professional implementation standards

project = ProjectManagerScript("user_profile_management", user_request)
result = project.run_complete_workflow(extracted_context)
```

#### **Template Coordination**
```python
# Templates can coordinate with each other for complex workflows:

# 1. Research phase
research = ResearchWorkflowScript("modern_authentication_patterns", "focused")
research_insights = research.run_complete_research_workflow({
    "research_areas": ["JWT best practices", "OAuth2 implementation patterns"],
    "focus": "Technical implementation guidelines"
})

# 2. Implementation phase using research insights
project = ProjectManagerScript("authentication_system", "...")
implementation_context = {
    "research_insights": research_insights,
    "implementation_approach": "Research-informed development"
}
implementation_result = project.run_complete_workflow(implementation_context)
```

## 📊 Progress Tracking and Communication

### **Built-in Progress Reporting**
Templates automatically provide comprehensive progress tracking:

```python
# Templates report progress in standard format:
Progress Update: Phase 2 - Core Implementation (50%)
├─ ✅ Requirements analysis completed
├─ ✅ API design validated  
├─ 🔄 Backend implementation in progress
├─ ⏳ Frontend components pending
└─ ⏳ Testing and validation queued

Next Actions:
- Complete Rust backend implementation with security validation
- Begin React component development
- Prepare integration testing environment

Issues Encountered: None
Estimated Completion: 45-60 minutes
```

### **Orchestrator Communication**
Templates maintain communication with orchestrator for strategic guidance:

```python
# Templates automatically generate orchestrator updates:
orchestrator_report = f"""
PROJECT STATUS REPORT: {project_name}

Current Phase: {current_phase} ({progress}% complete)
Key Accomplishments:
- {completed_tasks_summary}

Current Focus:
- {active_tasks_summary}

Strategic Guidance Needed:
- {strategic_decisions_required}

Risk Assessment:
- {identified_risks_and_mitigations}

Resource Utilization:
- Token Usage: {token_usage}
- Agent Coordination: {agent_usage}
- Timeline Status: {timeline_status}

Recommendations for next phase execution and quality optimization.
"""
```

## 🔒 Quality and Security Standards

### **Built-in Quality Gates**
Templates enforce quality standards at each phase:

```python
# Automatic quality validation
quality_gates = {
    "requirements_phase": [
        "All requirements clearly documented",
        "Technical approach validated",
        "Resource requirements confirmed"
    ],
    "implementation_phase": [
        "Code follows established patterns",
        "Security requirements implemented",
        "Unit tests passing"
    ],
    "validation_phase": [
        "Integration tests passing",
        "Security validation completed", 
        "Performance requirements met"
    ],
    "completion_phase": [
        "All deliverables generated",
        "Documentation complete",
        "Handoff materials prepared"
    ]
}
```

### **Security Integration**
Templates automatically include security validation:

```python
# Security is built into every template
security_checkpoints = [
    "Input validation and sanitization",
    "Authentication and authorization patterns",
    "Data encryption and protection",
    "Security testing and validation",
    "Compliance verification (SOC2, GDPR, etc.)"
]
```

## 🚀 Autonomous Execution Guidelines

### **Minimal Supervision Execution**
Templates are designed for autonomous operation:

```python
# Templates handle common execution patterns:

# 1. Error Recovery
if task_failed:
    retry_with_modified_approach()
    if still_failing:
        escalate_to_orchestrator_for_guidance()

# 2. Progress Adaptation
if execution_time_exceeding_estimate:
    adjust_scope_or_approach()
    communicate_changes_to_user()

# 3. Quality Validation
if quality_gate_failed:
    identify_root_cause()
    implement_corrective_actions()
    re-validate_before_proceeding()
```

### **Cross-Session Continuity**
Templates maintain state across Claude Code sessions:

```python
# Session state automatically preserved:
session_state = {
    "project_name": project_name,
    "current_phase": current_phase,
    "completed_tasks": completed_tasks,
    "pending_tasks": pending_tasks,
    "context": execution_context,
    "deliverables": generated_deliverables,
    "next_actions": planned_next_actions
}

# Resumption logic:
if resuming_session:
    restore_state_from_previous_session()
    validate_environment_consistency()
    continue_from_last_checkpoint()
```

## 📈 Performance Optimization

### **Token Efficiency**
Templates optimize token usage through:

```python
# Intelligent context management
if context_exceeds_limit:
    summarize_previous_phases()
    focus_on_current_phase_context()
    maintain_critical_decision_history()

# Progressive disclosure
load_context_as_needed()
cache_frequently_used_information()
compress_historical_data()
```

### **Agent Coordination Efficiency**
Templates minimize coordination overhead:

```python
# Parallel execution where possible
independent_tasks = identify_parallel_tasks(task_queue)
execute_tasks_in_parallel(independent_tasks)

# Batched communication
batch_status_updates()
consolidate_orchestrator_communications()
minimize_context_switching_between_agents()
```

## 🎯 Template Success Metrics

### **Expected Outcomes**
Templates should consistently deliver:

1. **95%+ autonomous execution** with minimal manual intervention
2. **Professional-grade deliverables** ready for production use
3. **Comprehensive progress tracking** with clear checkpoint reporting
4. **Cross-session reliability** with consistent state management
5. **Quality assurance** with built-in validation and error recovery

### **Performance Benchmarks**
- **Project Management Template**: Complete feature implementation in 45-90 minutes
- **Research Template**: Comprehensive analysis with executive summary in 30-60 minutes  
- **Cross-session resumption**: <5 minutes to restore context and continue
- **Quality gate validation**: Automatic validation with <10% manual oversight needed

---

## 🎪 Claude Code Integration Summary

**Templates transform Claude Code from a conversational AI into a comprehensive autonomous development and research platform.** Use templates whenever:

1. **Complex workflows** require multi-agent coordination
2. **Professional deliverables** are expected or beneficial  
3. **Cross-session continuity** adds value for long-running projects
4. **Autonomous execution** allows focus on higher-level strategy

**Templates provide the intelligence layer that enables Claude Code to manage enterprise-grade workflows with minimal supervision while maintaining professional standards and comprehensive progress tracking.**