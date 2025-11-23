# Script Templates Documentation

## 📋 Overview

The `templates/` directory contains **reusable workflow script templates** that provide complete, end-to-end automation for common patterns. These templates build on the core infrastructure to deliver production-ready workflow solutions.

## 🏗️ Available Templates

### **`project_manager_script.py`** - Complete Project Management Workflow
**Purpose**: End-to-end project management with autonomous execution and cross-session tracking

**Key Features:**
- ✅ **Complete project lifecycle** from analysis to deliverables
- ✅ **Multi-agent coordination** with orchestrator communication
- ✅ **Cross-session continuity** with persistent progress tracking
- ✅ **Quality gates** and validation checkpoints
- ✅ **Autonomous execution** with minimal supervision
- ✅ **Comprehensive reporting** with structured deliverables

**Use Cases:**
- Full-stack feature development (backend + frontend + testing)
- System implementation projects (authentication, user management, etc.)
- Multi-phase development workflows with security validation
- Enterprise-grade projects requiring documentation and compliance

**Example Usage:**
```python
from project_manager_script import ProjectManagerScript

# Complete project management workflow
project = ProjectManagerScript(
    project_name="user_authentication_system",
    description="Implement secure user authentication with JWT, OAuth2, session management, and comprehensive security validation"
)

# Add project context
context = {
    "tech_stack": ["Rust", "PostgreSQL", "Redis"],
    "security_requirements": ["OAuth2", "JWT", "Rate limiting"],
    "compliance_needs": ["SOC2", "GDPR"],
    "deployment_target": "AWS ECS"
}

# Execute complete workflow autonomously
deliverables = project.run_complete_workflow(context)

# Result: Complete project with all phases executed:
# - Requirements analysis and planning
# - Backend implementation with security
# - Testing and quality validation  
# - Documentation and deployment preparation
```

### **`research_workflow_script.py`** - Comprehensive Research Automation
**Purpose**: Multi-stream research coordination with intelligent synthesis and executive reporting

**Key Features:**
- ✅ **Multi-stream research** (web, competitive, codebase analysis)
- ✅ **Intelligent agent coordination** for parallel research execution
- ✅ **Comprehensive synthesis** with cross-source validation
- ✅ **Executive summary generation** with strategic recommendations
- ✅ **Source tracking** and credibility assessment
- ✅ **Structured deliverables** ready for business decision-making

**Use Cases:**
- Market research and competitive landscape analysis
- Technology evaluation and comparison studies
- Business intelligence and strategic planning
- Academic research with multiple source streams

**Example Usage:**
```python
from research_workflow_script import ResearchWorkflowScript

# Comprehensive research workflow
research = ResearchWorkflowScript(
    research_topic="AI-powered IDE market positioning and pricing strategy",
    scope="comprehensive"
)

# Execute complete research workflow
deliverables = research.run_complete_research_workflow(
    requirements={
        "target_market": "Professional developers and enterprises",
        "geographic_scope": "Global, focus on US/EU markets",
        "decision_context": "Product positioning and pricing strategy"
    },
    research_areas=[
        "AI coding assistant market size and growth",
        "Developer productivity tools adoption trends", 
        "Enterprise software procurement patterns"
    ],
    competitors=[
        "GitHub Copilot", "Cursor AI IDE", "JetBrains AI Assistant",
        "Amazon CodeWhisperer", "Tabnine"
    ]
)

# Result: Complete research package with:
# - Executive summary with key findings
# - Detailed competitive landscape analysis
# - Market opportunity assessment
# - Strategic positioning recommendations
```

## 🔧 Template Architecture

### **Common Template Structure**
All templates follow a consistent architecture pattern:

```python
class TemplateScript:
    def __init__(self, primary_description: str, scope: str = "comprehensive"):
        # Initialize core components
        self.agent_caller = AgentCaller()
        self.workflow_analyzer = WorkflowAnalyzer()
        self.autonomous_manager = AutonomousManager()
        
        # Template-specific initialization
        self.setup_template_specifics()
    
    def analyze_requirements(self, context: dict) -> dict:
        """Step 1: Analyze requirements using WorkflowAnalyzer"""
        
    def create_execution_plan(self, analysis: dict) -> list:
        """Step 2: Create detailed execution plan with autonomous tasks"""
        
    def setup_orchestrator_monitoring(self):
        """Step 3: Setup orchestrator communication and monitoring"""
        
    def execute_autonomous_workflow(self, tasks: list) -> dict:
        """Step 4: Execute autonomous workflow with full monitoring"""
        
    def generate_deliverables(self) -> dict:
        """Step 5: Generate final deliverables and documentation"""
        
    def run_complete_workflow(self, context: dict = None) -> dict:
        """Execute complete workflow end-to-end"""
```

### **Integration with Core Infrastructure**
Templates leverage all core components:

- **AgentCaller** - Standardized agent invocation with progress tracking
- **WorkflowAnalyzer** - Intelligent requirement analysis and agent selection
- **AutonomousManager** - Self-executing task management with orchestrator communication

### **47-Agent Framework Integration**
Templates automatically integrate with the 47-agent framework:

- **Agent Selection** - Uses proven agent patterns and capabilities
- **Skills Utilization** - Leverages production automation patterns
- **Commands Execution** - Executes workflow automation commands
- **Quality Gates** - Implements validation and compliance checkpoints

## 🚀 Template Usage Patterns

### **For Complete Project Management**
Use `project_manager_script.py` when you need:

- **Full-stack development** with backend, frontend, and testing
- **Multi-phase projects** with planning, implementation, and validation
- **Enterprise requirements** including security, compliance, and documentation
- **Cross-session tracking** for complex multi-day projects

```python
# Pattern: Complete feature development
project = ProjectManagerScript("secure_user_profile_management", "...")
deliverables = project.run_complete_workflow({
    "tech_stack": ["Rust", "React", "PostgreSQL"],
    "security_requirements": ["Authentication", "Authorization", "Data encryption"],
    "compliance_needs": ["GDPR", "SOC2"]
})
```

### **For Comprehensive Research**  
Use `research_workflow_script.py` when you need:

- **Multi-source research** combining web, competitive, and technical analysis
- **Strategic intelligence** for business decision-making
- **Executive summaries** with actionable recommendations
- **Competitive landscape** analysis with positioning insights

```python
# Pattern: Strategic research and analysis
research = ResearchWorkflowScript("cloud_infrastructure_competitive_landscape", "comprehensive")
deliverables = research.run_complete_research_workflow({
    "research_areas": ["Multi-cloud trends", "Cost optimization", "Security compliance"],
    "competitors": ["AWS", "Azure", "GCP", "Digital Ocean"],
    "business_context": "Enterprise migration planning"
})
```

### **For Custom Workflows**
Extend existing templates for domain-specific needs:

```python
# Pattern: Custom template extension
class SecurityAuditScript(ProjectManagerScript):
    def __init__(self, audit_scope: str):
        super().__init__(f"security_audit_{audit_scope}", "security audit workflow")
        self.audit_frameworks = ["OWASP", "NIST", "SOC2"]
    
    def analyze_requirements(self, context: dict) -> dict:
        # Add security-specific analysis
        base_analysis = super().analyze_requirements(context)
        security_analysis = self.analyze_security_requirements(context)
        return {**base_analysis, **security_analysis}
    
    def create_execution_plan(self, analysis: dict) -> list:
        # Override with security-focused execution plan
        return self.create_security_audit_plan(analysis)
```

## 📊 Template Lifecycle

### **Phase 1: Requirements Analysis (25%)**
- Analyze user requirements and context
- Determine optimal agent coordination strategy
- Create detailed execution plan with checkboxes
- Validate resource requirements and timeline

### **Phase 2: Core Execution (50%)**
- Execute primary workflow using selected agents
- Coordinate parallel and sequential agent tasks
- Monitor progress and handle error recovery
- Validate intermediate deliverables

### **Phase 3: Validation & Quality (75%)**
- Execute quality gates and validation checkpoints
- Perform security review and compliance validation
- Integrate results from multiple agent streams
- Prepare final deliverable packages

### **Phase 4: Completion & Reporting (100%)**
- Generate comprehensive final deliverables
- Create executive summaries and documentation
- Prepare handoff materials for next phases
- Archive session state for future reference

## 🔒 Quality Standards

### **Template Requirements**
All templates must include:

- **Comprehensive error handling** with retry logic
- **Progress tracking** with 25%, 50%, 75%, 100% checkpoints
- **Orchestrator communication** for status reporting
- **Cross-session persistence** for complex workflows
- **Quality gates** at each major phase
- **Complete documentation** with usage examples

### **Security Standards**
- **Input validation** for all user-provided context
- **Secret management** with no credential exposure
- **Secure agent communication** using established patterns
- **Audit trail** for all major decisions and actions

### **Performance Standards**
- **Token efficiency** with progressive context loading
- **Parallel execution** where possible for independent tasks
- **Resource monitoring** with usage optimization
- **Timeout management** for long-running operations

## 🧩 Extension Guidelines

### **Creating New Templates**

1. **Copy existing template** as starting point
2. **Modify template-specific methods** for your domain
3. **Update agent selection logic** for domain expertise
4. **Add domain-specific quality gates** and validation
5. **Include comprehensive documentation** and examples

### **Template Integration Patterns**

```python
# Pattern: Template composition
class HybridWorkflowScript:
    def __init__(self):
        self.project_manager = ProjectManagerScript("development", "...")
        self.research_manager = ResearchWorkflowScript("market_analysis", "...")
    
    def run_hybrid_workflow(self, context: dict) -> dict:
        # 1. Research phase
        research_results = self.research_manager.execute_research_streams(context)
        
        # 2. Development phase using research insights
        development_context = {**context, "research_insights": research_results}
        development_results = self.project_manager.run_complete_workflow(development_context)
        
        # 3. Integrated deliverables
        return self.synthesize_hybrid_deliverables(research_results, development_results)
```

## 📖 API Documentation

### **ProjectManagerScript Class**
- `analyze_requirements(context)` - Requirements analysis with agent recommendations
- `create_execution_plan(analysis)` - Detailed task breakdown with dependencies
- `setup_orchestrator_monitoring()` - Progress tracking and communication setup
- `execute_autonomous_workflow(tasks)` - Self-executing workflow management
- `generate_deliverables()` - Final deliverable package generation
- `run_complete_workflow(context)` - One-command complete execution

### **ResearchWorkflowScript Class**
- `plan_research_strategy(requirements)` - Research approach planning
- `execute_web_research(areas)` - Web research coordination
- `execute_competitive_analysis(competitors)` - Competitive intelligence
- `execute_codebase_research(areas)` - Technical analysis (when applicable)
- `synthesize_findings(data)` - Cross-source synthesis and analysis
- `run_complete_research_workflow(...)` - One-command complete research

## 🔗 Related Documentation

- **[Core Infrastructure](../core/README.md)** - Foundational components and APIs
- **[Orchestration Engine](../workflows/README.md)** - Intelligent workflow dispatch
- **[Scripts Framework Overview](../README.md)** - Complete framework architecture

---

**Script Templates provide production-ready, autonomous workflow solutions that combine intelligent agent coordination with comprehensive progress tracking and professional deliverable generation.**