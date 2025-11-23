# Workflows - Claude Code Instructions

## 🎯 Purpose

The `workflows/` directory contains the **intelligent orchestration engine** that serves as the central dispatch system for all workflow automation. This is the **primary entry point** for complex task coordination and autonomous execution.

## 📋 Core Integration Principle

### **Single Entry Point Philosophy**
The `orchestrator_dispatcher.py` should be Claude Code's **primary interface** for complex workflows:

```python
from scripts.workflows.orchestrator_dispatcher import orchestrate_workflow

# ✅ PREFERRED: Universal workflow entry point
result = orchestrate_workflow(user_request, context)

# This handles EVERYTHING:
# - Workflow analysis and type detection  
# - Template selection or custom script generation
# - Agent coordination and execution
# - Progress tracking and reporting
# - Quality validation and deliverables
```

### **When to Use Orchestrator Dispatcher**

#### **✅ ALWAYS use for:**
- **Complex user requests** involving multiple steps or agents
- **Ambiguous requirements** where optimal approach is unclear
- **Professional deliverable needs** requiring structured outputs
- **Cross-session projects** requiring progress tracking
- **Unknown workflow patterns** that may need custom solutions

#### **✅ PREFERRED over direct agent calling when:**
- User request involves coordination between multiple components
- Workflow may benefit from autonomous execution
- Professional documentation or reports are expected
- Timeline or resource planning would be beneficial

#### **Example Decision Logic:**
```python
# Simple request → Direct Task tool
"Fix the typo in README.md" → Task(subagent_type="general-purpose", prompt="...")

# Complex request → Orchestrator Dispatcher  
"Implement secure user authentication with testing" → orchestrate_workflow(...)

# Research request → Orchestrator Dispatcher
"Research competitive landscape for AI tools" → orchestrate_workflow(...)

# Multi-phase project → Orchestrator Dispatcher  
"Build user profile management system" → orchestrate_workflow(...)
```

## 🚀 Orchestrator Usage Patterns

### **Automatic Workflow Analysis**
The orchestrator automatically analyzes any request:

```python
# Claude Code integration pattern:
def handle_complex_request(user_request: str, available_context: dict = None):
    # Let orchestrator analyze and dispatch optimal approach
    result = orchestrate_workflow(
        user_request=user_request,
        context=available_context or {}
    )
    
    # Orchestrator provides:
    # - Workflow type classification
    # - Agent coordination strategy
    # - Execution approach (template vs custom)
    # - Complete autonomous execution
    
    return result

# Example usage:
user_request = "Implement secure user profile management with React frontend and Rust backend including comprehensive testing"

context = {
    "existing_codebase": "Authentication system already implemented",
    "tech_preferences": "Modern stack with performance focus", 
    "timeline": "2-week development cycle",
    "security_requirements": "SOC2 compliance needed"
}

result = handle_complex_request(user_request, context)
```

### **Template Selection Logic**
Orchestrator intelligently selects the best approach:

```python
# Automatic template dispatch based on analysis:

# Project Management workflows
"Build/Implement/Create [system/feature]" → project_manager_script.py

# Research workflows  
"Research/Analyze/Study [market/technology]" → research_workflow_script.py

# Security workflows
"Audit/Secure/Validate [security aspects]" → security_audit_script.py

# Custom workflows
"[Unique combination or novel requirements]" → Custom script generation

# Hybrid workflows
"[Multiple workflow types combined]" → Multi-template coordination
```

### **Custom Script Generation**
For unique requirements, orchestrator generates custom solutions:

```python
# Orchestrator determines when to generate custom scripts:
if workflow_type == WorkflowType.CUSTOM:
    # Generate custom script using agent-based code generation
    custom_script = generate_custom_workflow_script(
        requirements=extracted_requirements,
        base_template="project_manager_script.py",
        agent_recommendations=recommended_agents
    )
    
    # Execute generated script autonomously
    execution_result = execute_generated_script(custom_script, context)
    
    return {
        "approach": "custom_script_generation",
        "generated_script": custom_script,
        "execution_result": execution_result
    }
```

## 🎭 Agent Coordination Strategies

### **Multi-Agent Orchestration**
The orchestrator coordinates multiple agents seamlessly:

```python
# Example: Full-stack development workflow
orchestrated_workflow = {
    "coordinator": "orchestrator",
    "execution_strategy": "parallel_then_integrate",
    "agent_assignments": {
        "requirements_analysis": "codebase-analyzer",
        "api_design": "backend-architect", 
        "implementation": "rust-expert-developer",
        "frontend_development": "frontend-developer",
        "security_validation": "security-specialist"
    },
    "integration_points": [
        {"phase": "Design Review", "agents": ["backend-architect", "security-specialist"]},
        {"phase": "Implementation Integration", "agents": ["rust-expert-developer", "frontend-developer"]},
        {"phase": "Final Validation", "agents": ["security-specialist", "orchestrator"]}
    ]
}
```

### **Adaptive Execution**
Orchestrator adapts execution based on real-time feedback:

```python
# Adaptive execution patterns in orchestrator:
def adaptive_execution_monitoring():
    if execution_time > estimated_time * 1.2:
        # Execution taking longer than expected
        adjust_scope_or_parallelize_tasks()
        
    if quality_gate_failures > threshold:
        # Quality issues detected
        add_additional_validation_agent()
        escalate_to_senior_specialist()
        
    if token_usage > budget * 0.8:
        # Resource constraints approaching
        optimize_context_management()
        prioritize_critical_path_tasks()
        
    if user_requirements_change:
        # Adaptive requirements handling
        re_analyze_workflow_requirements()
        adjust_execution_plan_dynamically()
```

## 📊 Progress Tracking and Communication

### **Standardized Progress Reporting**
Orchestrator provides consistent progress updates:

```python
# Standard progress format for Claude Code integration:
progress_update = {
    "session_id": "orchestrator_session_123",
    "workflow_type": "project_management", 
    "overall_progress": 67.5,  # Percentage complete
    "current_phase": "Implementation & Integration",
    "phase_breakdown": {
        "Requirements Analysis": {"status": "completed", "progress": 100},
        "Architecture Design": {"status": "completed", "progress": 100},
        "Implementation": {"status": "in_progress", "progress": 45},
        "Testing & Validation": {"status": "pending", "progress": 0},
        "Documentation": {"status": "pending", "progress": 0}
    },
    "active_agents": ["rust-expert-developer", "frontend-developer"],
    "next_milestones": [
        "Complete backend API implementation",
        "Integrate frontend components", 
        "Execute integration testing"
    ],
    "estimated_completion": "25-35 minutes remaining"
}

# Claude Code should display this information to keep user informed
print_progress_update(progress_update)
```

### **Quality Gate Integration**
Orchestrator enforces quality standards automatically:

```python
# Built-in quality validation:
quality_gates = {
    "phase_1_requirements": {
        "criteria": ["Requirements documented", "Approach validated", "Resources confirmed"],
        "validation": "automatic",
        "blocking": True
    },
    "phase_2_implementation": {
        "criteria": ["Code standards met", "Security patterns followed", "Tests passing"],
        "validation": "agent_review",
        "blocking": True  
    },
    "phase_3_integration": {
        "criteria": ["Integration working", "Performance acceptable", "Documentation complete"],
        "validation": "comprehensive_testing",
        "blocking": True
    }
}

# Quality gates prevent progression until criteria met
def enforce_quality_gate(phase):
    if not validate_quality_criteria(phase):
        remediate_quality_issues()
        re_validate_before_continuing()
```

## 🔧 Integration with Core Infrastructure

### **Seamless Core Component Usage**
Orchestrator leverages all core infrastructure:

```python
# Orchestrator uses core components transparently:
from scripts.core.agent_caller import AgentCaller
from scripts.core.workflow_analyzer import WorkflowAnalyzer  
from scripts.core.autonomous_manager import AutonomousManager

class OrchestratorDispatcher:
    def __init__(self):
        # Core infrastructure integration
        self.agent_caller = AgentCaller()
        self.workflow_analyzer = WorkflowAnalyzer()
        self.autonomous_manager = AutonomousManager()
        
    def analyze_and_dispatch(self, request, context):
        # 1. Intelligent analysis
        analysis = self.workflow_analyzer.analyze_workflow(request, context)
        
        # 2. Dispatch decision
        strategy = self.determine_optimal_strategy(analysis)
        
        # 3. Autonomous execution
        if strategy.requires_autonomous_management:
            tasks = self.autonomous_manager.create_task_plan(request, analysis)
            result = self.autonomous_manager.start_autonomous_execution()
        
        return result
```

### **Template Integration**
Orchestrator coordinates with all templates:

```python
# Dynamic template instantiation and execution:
def execute_template_workflow(template_name, request, context):
    if template_name == "project_manager_script.py":
        from scripts.templates.project_manager_script import ProjectManagerScript
        template = ProjectManagerScript(extract_project_name(request), request)
        return template.run_complete_workflow(context)
        
    elif template_name == "research_workflow_script.py":
        from scripts.templates.research_workflow_script import ResearchWorkflowScript
        template = ResearchWorkflowScript(extract_research_topic(request))
        return template.run_complete_research_workflow(
            extract_requirements(context),
            extract_research_areas(context),
            extract_competitors(context)
        )
```

## 🔒 Error Handling and Recovery

### **Comprehensive Error Management**
Orchestrator handles all error scenarios:

```python
# Multi-level error handling:
def handle_execution_errors():
    try:
        # Attempt optimal execution strategy
        result = execute_primary_strategy()
        
    except AgentInvocationError as e:
        # Agent calling failed - try alternative agent
        result = execute_with_alternative_agent()
        
    except WorkflowComplexityError as e:
        # Workflow too complex for single approach
        result = break_into_smaller_workflows()
        
    except ResourceConstraintError as e:
        # Resource limits exceeded  
        result = optimize_and_retry_with_constraints()
        
    except QualityGateFailure as e:
        # Quality validation failed
        result = remediate_and_revalidate()
        
    except Exception as e:
        # Unknown error - escalate to orchestrator agent
        result = escalate_to_orchestrator_for_guidance()
        
    return result
```

### **Graceful Degradation**
When full automation isn't possible:

```python
# Graceful degradation strategies:
if autonomous_execution_failing:
    # Fall back to guided execution
    provide_step_by_step_guidance()
    enable_manual_checkpoints()
    
if template_not_suitable:
    # Fall back to core infrastructure  
    use_agent_caller_directly()
    provide_manual_coordination_guidance()
    
if complexity_exceeds_capabilities:
    # Break down into manageable pieces
    decompose_into_simpler_workflows()
    execute_sequentially_with_checkpoints()
```

## 📈 Performance and Optimization

### **Intelligent Resource Management**
Orchestrator optimizes resource usage:

```python
# Resource optimization strategies:
def optimize_resource_usage():
    # Token budget management
    if approaching_token_limit():
        compress_context_history()
        focus_on_critical_information()
        
    # Agent coordination efficiency  
    if coordination_overhead_high():
        batch_agent_communications()
        reduce_context_switching()
        
    # Execution time optimization
    if execution_time_excessive():
        increase_parallelization()
        simplify_non_critical_tasks()
```

### **Learning and Adaptation**
Orchestrator improves over time:

```python
# Pattern learning for better dispatch decisions:
def learn_from_execution_patterns():
    # Track successful workflow patterns
    successful_patterns = analyze_successful_executions()
    
    # Identify common failure modes
    failure_patterns = analyze_failed_executions()
    
    # Update dispatch logic
    improve_workflow_type_detection()
    refine_template_selection_criteria()
    enhance_complexity_assessment()
    
    # Optimize agent coordination
    improve_agent_selection_confidence()
    refine_execution_strategies()
```

## 🎯 Claude Code Success Patterns

### **Recommended Usage Flow**
For optimal Claude Code integration:

```python
# 1. Initial Assessment
if user_request_is_complex():
    use_orchestrator_dispatcher()
else:
    use_direct_task_tool()

# 2. Orchestrator Dispatch  
result = orchestrate_workflow(user_request, available_context)

# 3. Progress Communication
communicate_progress_to_user(result["execution_progress"])

# 4. Deliverable Presentation
present_structured_deliverables(result["deliverables"])

# 5. Next Steps Guidance
provide_next_steps_recommendations(result["recommendations"])
```

### **Quality Metrics for Claude Code**
Orchestrator should consistently provide:

1. **90%+ accuracy** in workflow type detection
2. **95%+ success rate** in template selection appropriateness  
3. **85%+ autonomous execution** with minimal manual intervention
4. **Professional deliverables** ready for immediate use
5. **Clear progress tracking** with actionable next steps

---

**The Workflows system transforms Claude Code into an intelligent orchestration platform that can handle enterprise-grade complexity while maintaining simplicity and professional deliverable quality.**