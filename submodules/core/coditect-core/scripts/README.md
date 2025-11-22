# CODITECT Scripts

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.**

---

## 🚀 Quick Start Scripts

### coditect-quicklaunch.sh

**Purpose**: Automated setup for new CODITECT users

**Usage**:
```bash
# Download and run
curl -fsSL https://raw.githubusercontent.com/coditect-ai/coditect-core/main/scripts/coditect-quicklaunch.sh | bash

# Or run locally
./coditect-quicklaunch.sh
```

**Features**:
- Creates ~/PROJECTS workspace
- Installs .coditect framework as submodule
- Sets up multi-LLM CLI symlinks
- Creates MEMORY-CONTEXT directory
- Launches interactive tutorial

### coditect-tutorial.sh

**Purpose**: Interactive tutorial for CODITECT 1-2-3 methodology

**Usage**:
```bash
~/PROJECTS/.coditect/scripts/coditect-tutorial.sh
```

**What You'll Learn** (~30 minutes):
- Project plan creation
- Tasklist with checkboxes workflow
- Architecture Decision Records (ADRs)
- C4 Model architecture visualization
- MEMORY-CONTEXT session continuity
- AI-First Autonomous Development Process

**Tutorial Example**: Creates complete sample project at `~/PROJECTS/coditect-tutorial-example/`

### coditect-router

**🤖 AI-Powered Command Selection Tool** (NEW!)

**Purpose**: Never memorize slash commands again - just describe what you want in plain English

**Usage**:
```bash
# Basic usage
coditect-router "I need to add user authentication"

# Interactive mode (recommended)
coditect-router -i

# With AI-powered analysis (set ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY="your-key-here"
coditect-router "Fix the bug in payment processing"
```

**Features**:
- 🧠 **AI-Powered Analysis**: Uses Claude to understand your request and suggest the perfect command
- 🎯 **Heuristic Fallback**: Works without API key using intelligent keyword matching
- 📋 **Detailed Recommendations**: Shows why a command is recommended, alternatives, and next steps
- 💬 **Interactive Mode**: Ask multiple questions in one session
- ⚡ **Instant Results**: Get command suggestions in seconds

**Example Output**:
```
🤖 CODITECT AI Command Router
======================================================================

📍 RECOMMENDED COMMAND: /implement
   Description: Production-ready implementation mode
   Purpose: Build production code with error handling

💭 REASONING:
   Detected implementation request (keywords: add, authentication)

🔄 ALTERNATIVES:
   • /prototype: Rapid prototyping mode
   • /feature_development: End-to-end feature workflow

📋 NEXT STEPS:
   1. Use /implement for production-ready code
   2. Include error handling and security hardening

💻 USAGE:
   Type in Claude Code: /implement
```

**Quick Aliases** (add to ~/.bashrc or ~/.zshrc):
```bash
alias cr='coditect-router'
alias cri='coditect-router -i'
```

**Files**:
- `coditect-router` - Shell wrapper script
- `coditect-command-router.py` - Python implementation

---

## 🏗️ **Two-Type Script Architecture**

### **📋 Project-Specific Scripts**
Scripts tailored for this specific AI Curriculum Development project

### **🛠️ Purpose-Specific Scripts** 
Reusable automation patterns applicable across different projects

---

## 📂 **Proposed Directory Structure**

```
.claude/scripts/
├── project_specific/              # AI Curriculum Development focused
│   ├── curriculum/
│   │   ├── content_generators/    # Generate AI curriculum content
│   │   ├── assessment_builders/   # Create educational assessments
│   │   └── notebooklm_optimizers/ # NotebookLM content preparation
│   ├── educational/
│   │   ├── skill_level_adapters/  # Adapt content for skill levels
│   │   ├── learning_progressions/ # Track educational progressions
│   │   └── quality_validators/    # Educational content validation
│   └── workflows/
│       ├── curriculum_project_manager.py  # Complete curriculum projects
│       └── module_coordinators/   # Multi-module orchestration
│
├── purpose_specific/              # Reusable automation patterns
│   ├── automation/
│   │   ├── agent_dispatchers/     # Smart agent selection systems
│   │   ├── task_executors/        # Generic task automation
│   │   └── workflow_orchestrators/ # Multi-agent coordination
│   ├── optimization/
│   │   ├── work_reuse_analyzers/  # Asset reuse and token optimization
│   │   ├── efficiency_trackers/   # ROI and performance monitoring
│   │   └── resource_managers/     # Token and time budget management
│   ├── quality_assurance/
│   │   ├── validation_frameworks/ # Generic quality validation
│   │   ├── testing_orchestrators/ # Automated testing coordination
│   │   └── compliance_checkers/   # Standards compliance validation
│   └── project_management/
│       ├── task_generators/       # Auto-generate executable tasks
│       ├── progress_trackers/     # Multi-session state management
│       └── milestone_managers/    # Project milestone coordination
│
└── generated_tasks/               # R&D Archive (current location)
    ├── README.md                  # Reuse documentation
    └── execute_TASK_*.py          # Task automation templates
```

---

## 🎯 **Classification Guidelines**

### **Project-Specific Scripts** ✅
**Criteria**: Deeply tied to AI curriculum development domain

**Examples**:
- `curriculum_content_generator.py` - Creates AI/ML educational content
- `skill_level_adapter.py` - Adapts content for beginner→expert progression
- `notebooklm_content_optimizer.py` - Formats content for AI book generation
- `assessment_bias_detector.py` - Validates educational fairness
- `learning_analytics_tracker.py` - Monitors student progress patterns

**Characteristics**:
- Domain-specific logic (AI, ML, education)
- Educational frameworks integration
- Curriculum standards compliance
- Learning objective alignment

### **Purpose-Specific Scripts** 🛠️
**Criteria**: Reusable automation patterns applicable to any project

**Examples**:
- `smart_agent_dispatcher.py` - Intelligently selects optimal agents for any task
- `work_reuse_optimizer.py` - Analyzes reusable assets across domains
- `task_automation_generator.py` - Creates executable scripts from requirements
- `multi_agent_orchestrator.py` - Coordinates complex workflows
- `roi_efficiency_tracker.py` - Monitors token usage and optimization

**Characteristics**:
- Domain-agnostic automation
- Framework-independent patterns
- Cross-project reusability
- Generic workflow coordination

---

## 🔄 **Migration Plan**

### **Current Scripts Analysis**:

| Script | Current Location | Proposed Classification | Target Location |
|--------|------------------|------------------------|-----------------|
| `curriculum_project_manager.py` | `workflows/` | **Project-Specific** | `project_specific/workflows/` |
| `agent_dispatcher.py` | `core/` | **Purpose-Specific** | `purpose_specific/automation/` |
| `work_reuse_optimizer.py` | `core/` | **Purpose-Specific** | `purpose_specific/optimization/` |
| `smart_task_executor.py` | `core/` | **Purpose-Specific** | `purpose_specific/automation/` |
| `execute_TASK_*.py` | `generated_tasks/` | **R&D Archive** | `generated_tasks/` (keep as-is) |

### **Implementation Steps**:

1. **Create new directory structure**
2. **Migrate existing scripts** to appropriate categories
3. **Update all path references** in documentation
4. **Create category-specific README files** with usage guidelines
5. **Add cross-reference documentation** for script relationships

---

## 💡 **Benefits of This Structure**

### **For Project-Specific Scripts**:
- **Domain Focus**: Optimized for educational content development
- **Deep Integration**: Leverages educational frameworks and standards  
- **Quality Assurance**: Built-in educational validation and bias detection
- **Learning Analytics**: Progress tracking and adaptive content features

### **For Purpose-Specific Scripts**:
- **High Reusability**: Applicable to business, technical, creative projects
- **Framework Agnostic**: Works with any content domain or project type
- **Pattern Library**: Reusable automation templates for future projects
- **ROI Optimization**: Maximizes efficiency across different use cases

### **For Team Collaboration**:
- **Clear Separation**: Easy to understand script purpose and scope
- **Easier Maintenance**: Focused updates within specific categories
- **Knowledge Transfer**: New team members quickly understand organization
- **Template Creation**: Easy to extract patterns for new project types

---

## 🚀 **Future Extension Opportunities**

### **Additional Project-Specific Categories**:
- **Corporate Training Scripts** - Business education content generators
- **Technical Documentation Scripts** - API docs and tutorial creators  
- **Certification Programs Scripts** - Competency-based assessment builders

### **Additional Purpose-Specific Categories**:
- **Content Marketing Automation** - Blog series and content calendar generators
- **Documentation Orchestrators** - Multi-format documentation creation
- **Quality Assurance Frameworks** - Cross-domain validation and testing
- **Analytics and Reporting** - Performance tracking and insights generation

---

**Recommendation**: Implement this two-type architecture to create a scalable, maintainable script organization that maximizes both project effectiveness and cross-project reusability.