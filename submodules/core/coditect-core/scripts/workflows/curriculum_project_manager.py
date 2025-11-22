#!/usr/bin/env python3
"""
Curriculum Project Manager

Autonomous project management system for AI curriculum development using the 
orchestrator agent and educational framework. Creates detailed project plans 
with checkboxes, manages multi-session progress, and coordinates agent workflows.
"""

import json
import yaml
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ProjectPhase(Enum):
    INITIATION = "initiation"
    PLANNING = "planning" 
    RESEARCH = "research"
    DEVELOPMENT = "development"
    QUALITY_ASSURANCE = "quality_assurance"
    OPTIMIZATION = "optimization"
    DEPLOYMENT = "deployment"
    COMPLETION = "completion"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    DEFERRED = "deferred"

@dataclass
class ProjectTask:
    id: str
    title: str
    description: str
    assigned_agent: str
    status: TaskStatus
    phase: ProjectPhase
    dependencies: List[str]
    deliverables: List[str]
    estimated_tokens: int
    estimated_duration: str
    actual_tokens: Optional[int] = None
    actual_duration: Optional[str] = None
    completion_date: Optional[str] = None
    notes: List[str] = None
    
    def __post_init__(self):
        if self.notes is None:
            self.notes = []

@dataclass
class ProjectMilestone:
    id: str
    title: str
    description: str
    target_date: str
    completion_percentage: float
    required_tasks: List[str]
    status: TaskStatus

@dataclass
class CurriculumProject:
    project_id: str
    title: str
    description: str
    start_date: str
    target_completion: str
    current_phase: ProjectPhase
    overall_progress: float
    tasks: Dict[str, ProjectTask]
    milestones: Dict[str, ProjectMilestone]
    resource_usage: Dict[str, Any]
    quality_gates: List[Dict[str, Any]]
    risk_register: List[Dict[str, Any]]

class CurriculumProjectManager:
    """Autonomous project manager for AI curriculum development"""
    
    def __init__(self, project_file: Optional[str] = None):
        self.project_file = project_file or f"curriculum_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.project: Optional[CurriculumProject] = None
        self.task_templates = self._load_task_templates()
        
    def _load_task_templates(self) -> Dict[str, Any]:
        """Load predefined task templates for common curriculum development activities"""
        return {
            "content_generation": {
                "agent": "ai-curriculum-specialist",
                "skills": ["ai-curriculum-development"],
                "commands": ["generate-curriculum-content"],
                "base_tokens": 15000,
                "base_duration": "2-3 hours"
            },
            "assessment_creation": {
                "agent": "assessment-creation-agent", 
                "skills": ["ai-curriculum-development"],
                "commands": [],
                "base_tokens": 8000,
                "base_duration": "1-2 hours"
            },
            "notebooklm_optimization": {
                "agent": "ai-curriculum-specialist",
                "skills": ["notebooklm-content-optimization"],
                "commands": [],
                "base_tokens": 5000,
                "base_duration": "30-60 minutes"
            },
            "quality_review": {
                "agent": "orchestrator",
                "skills": ["multi-agent-workflow"],
                "commands": ["ai_review"],
                "base_tokens": 10000,
                "base_duration": "1-2 hours"
            }
        }
    
    def create_project(self, title: str, description: str, scope: Dict[str, Any]) -> CurriculumProject:
        """Create new curriculum development project with automated task breakdown"""
        
        project_id = f"curriculum_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize project
        project = CurriculumProject(
            project_id=project_id,
            title=title,
            description=description,
            start_date=datetime.now().isoformat(),
            target_completion=self._calculate_target_date(scope),
            current_phase=ProjectPhase.INITIATION,
            overall_progress=0.0,
            tasks={},
            milestones={},
            resource_usage={
                "total_estimated_tokens": 0,
                "total_actual_tokens": 0,
                "token_budget": scope.get("token_budget", 500000),
                "sessions_count": 0
            },
            quality_gates=[],
            risk_register=[]
        )
        
        # Generate tasks based on scope
        tasks = self._generate_project_tasks(scope)
        project.tasks = {task.id: task for task in tasks}
        
        # Generate milestones
        milestones = self._generate_milestones(tasks)
        project.milestones = {milestone.id: milestone for milestone in milestones}
        
        # Calculate resource estimates
        total_tokens = sum(task.estimated_tokens for task in tasks)
        project.resource_usage["total_estimated_tokens"] = total_tokens
        
        # Initialize quality gates
        project.quality_gates = self._define_quality_gates(scope)
        
        # Initialize risk register
        project.risk_register = self._identify_initial_risks(scope, total_tokens)
        
        self.project = project
        self.save_project()
        
        return project
    
    def _generate_project_tasks(self, scope: Dict[str, Any]) -> List[ProjectTask]:
        """Generate detailed task breakdown based on project scope"""
        
        tasks = []
        task_counter = 1
        
        modules = scope.get("modules", ["module1_foundations"])
        skill_levels = scope.get("skill_levels", ["beginner", "intermediate", "advanced", "expert"])
        deliverables = scope.get("deliverables", ["content", "assessments"])
        
        # Phase 1: Project Initiation
        tasks.append(ProjectTask(
            id=f"TASK_{task_counter:03d}",
            title="Project Kickoff and Requirements Analysis",
            description="Analyze project requirements, establish success criteria, and create detailed project plan",
            assigned_agent="orchestrator",
            status=TaskStatus.PENDING,
            phase=ProjectPhase.INITIATION,
            dependencies=[],
            deliverables=["project_plan", "requirements_document"],
            estimated_tokens=5000,
            estimated_duration="30-60 minutes"
        ))
        task_counter += 1
        
        # Phase 2: Research and Planning
        tasks.append(ProjectTask(
            id=f"TASK_{task_counter:03d}",
            title="Curriculum Architecture Research",
            description="Research existing curriculum structures, pedagogical frameworks, and best practices",
            assigned_agent="ai-curriculum-specialist",
            status=TaskStatus.PENDING,
            phase=ProjectPhase.RESEARCH,
            dependencies=["TASK_001"],
            deliverables=["research_report", "architecture_recommendations"],
            estimated_tokens=8000,
            estimated_duration="1-2 hours"
        ))
        task_counter += 1
        
        # Phase 3: Development Tasks (per module and skill level)
        for module in modules:
            for skill_level in skill_levels:
                
                # Content Generation Task
                if "content" in deliverables:
                    tasks.append(ProjectTask(
                        id=f"TASK_{task_counter:03d}",
                        title=f"Generate {module} Content - {skill_level.title()} Level",
                        description=f"Create comprehensive {skill_level} level educational content for {module}",
                        assigned_agent="ai-curriculum-specialist",
                        status=TaskStatus.PENDING,
                        phase=ProjectPhase.DEVELOPMENT,
                        dependencies=["TASK_002"],
                        deliverables=[f"{module}_{skill_level}_content.md"],
                        estimated_tokens=self._estimate_content_tokens(module, skill_level),
                        estimated_duration="2-4 hours"
                    ))
                    task_counter += 1
                
                # Assessment Creation Task
                if "assessments" in deliverables:
                    tasks.append(ProjectTask(
                        id=f"TASK_{task_counter:03d}",
                        title=f"Create {module} Assessments - {skill_level.title()} Level",
                        description=f"Design adaptive assessments and evaluation frameworks for {module} at {skill_level} level",
                        assigned_agent="assessment-creation-agent",
                        status=TaskStatus.PENDING,
                        phase=ProjectPhase.DEVELOPMENT,
                        dependencies=[f"TASK_{task_counter-1:03d}"],  # Depends on content
                        deliverables=[f"{module}_{skill_level}_assessments.yaml"],
                        estimated_tokens=self._estimate_assessment_tokens(skill_level),
                        estimated_duration="1-2 hours"
                    ))
                    task_counter += 1
        
        # Phase 4: Integration and Quality Assurance
        tasks.append(ProjectTask(
            id=f"TASK_{task_counter:03d}",
            title="Cross-Module Integration and Consistency Review",
            description="Ensure consistency across modules and skill levels, validate learning progression",
            assigned_agent="orchestrator",
            status=TaskStatus.PENDING,
            phase=ProjectPhase.QUALITY_ASSURANCE,
            dependencies=[task.id for task in tasks if task.phase == ProjectPhase.DEVELOPMENT],
            deliverables=["integration_report", "consistency_validation"],
            estimated_tokens=12000,
            estimated_duration="2-3 hours"
        ))
        task_counter += 1
        
        # Phase 5: NotebookLM Optimization
        if scope.get("notebooklm_optimization", True):
            tasks.append(ProjectTask(
                id=f"TASK_{task_counter:03d}",
                title="NotebookLM Content Optimization",
                description="Optimize all content for Google NotebookLM processing, enhance metadata and cross-references",
                assigned_agent="ai-curriculum-specialist",
                status=TaskStatus.PENDING,
                phase=ProjectPhase.OPTIMIZATION,
                dependencies=[f"TASK_{task_counter-1:03d}"],
                deliverables=["optimized_content_suite", "notebooklm_ready_materials"],
                estimated_tokens=8000,
                estimated_duration="1-2 hours"
            ))
            task_counter += 1
        
        # Phase 6: Final Validation and Deployment
        tasks.append(ProjectTask(
            id=f"TASK_{task_counter:03d}",
            title="Final Quality Validation and Deployment Preparation",
            description="Comprehensive quality check, final validation, and preparation for deployment",
            assigned_agent="orchestrator",
            status=TaskStatus.PENDING,
            phase=ProjectPhase.COMPLETION,
            dependencies=[task.id for task in tasks[-2:]],  # Last few tasks
            deliverables=["final_quality_report", "deployment_package"],
            estimated_tokens=6000,
            estimated_duration="1-2 hours"
        ))
        
        return tasks
    
    def _generate_milestones(self, tasks: List[ProjectTask]) -> List[ProjectMilestone]:
        """Generate project milestones based on tasks and phases"""
        
        milestones = []
        
        # Phase-based milestones
        phase_tasks = {}
        for task in tasks:
            if task.phase not in phase_tasks:
                phase_tasks[task.phase] = []
            phase_tasks[task.phase].append(task.id)
        
        milestone_counter = 1
        for phase in ProjectPhase:
            if phase in phase_tasks:
                milestones.append(ProjectMilestone(
                    id=f"MILESTONE_{milestone_counter:02d}",
                    title=f"{phase.value.title().replace('_', ' ')} Complete",
                    description=f"All {phase.value} phase tasks completed successfully",
                    target_date=self._calculate_milestone_date(phase, len(phase_tasks[phase])),
                    completion_percentage=0.0,
                    required_tasks=phase_tasks[phase],
                    status=TaskStatus.PENDING
                ))
                milestone_counter += 1
        
        return milestones
    
    def _estimate_content_tokens(self, module: str, skill_level: str) -> int:
        """Estimate token usage for content generation based on module and skill level"""
        
        base_tokens = {
            "beginner": 8000,
            "intermediate": 12000,
            "advanced": 18000,
            "expert": 25000
        }
        
        # Adjust based on module complexity
        module_multipliers = {
            "foundations": 1.0,
            "machine_learning": 1.2,
            "deep_learning": 1.5,
            "nlp": 1.4,
            "computer_vision": 1.3,
            "generative_ai": 1.6,
            "reinforcement_learning": 1.7,
            "ai_systems": 1.3
        }
        
        module_key = module.split("_", 1)[-1] if "_" in module else module
        multiplier = module_multipliers.get(module_key, 1.0)
        
        return int(base_tokens[skill_level] * multiplier)
    
    def _estimate_assessment_tokens(self, skill_level: str) -> int:
        """Estimate token usage for assessment creation"""
        
        return {
            "beginner": 4000,
            "intermediate": 6000, 
            "advanced": 8000,
            "expert": 10000
        }[skill_level]
    
    def generate_orchestrator_plan(self) -> str:
        """Generate detailed project plan for orchestrator agent"""
        
        if not self.project:
            raise ValueError("No active project. Create project first.")
        
        plan = f"""
# AI Curriculum Development Project Plan

## Project Overview
- **Project ID**: {self.project.project_id}
- **Title**: {self.project.title}
- **Description**: {self.project.description}
- **Start Date**: {self.project.start_date}
- **Target Completion**: {self.project.target_completion}
- **Current Phase**: {self.project.current_phase.value}

## Resource Budget
- **Total Estimated Tokens**: {self.project.resource_usage['total_estimated_tokens']:,}
- **Token Budget**: {self.project.resource_usage['token_budget']:,}
- **Budget Utilization**: {self.project.resource_usage['total_estimated_tokens'] / self.project.resource_usage['token_budget'] * 100:.1f}%

## Task Breakdown

"""
        
        # Group tasks by phase
        for phase in ProjectPhase:
            phase_tasks = [task for task in self.project.tasks.values() if task.phase == phase]
            if phase_tasks:
                plan += f"### {phase.value.title().replace('_', ' ')} Phase\n\n"
                
                for task in phase_tasks:
                    status_icon = {
                        TaskStatus.PENDING: "⏳",
                        TaskStatus.IN_PROGRESS: "🔄", 
                        TaskStatus.COMPLETED: "✅",
                        TaskStatus.BLOCKED: "🚫",
                        TaskStatus.DEFERRED: "📋"
                    }[task.status]
                    
                    plan += f"- {status_icon} **{task.id}**: {task.title}\n"
                    plan += f"  - **Agent**: {task.assigned_agent}\n"
                    plan += f"  - **Dependencies**: {', '.join(task.dependencies) if task.dependencies else 'None'}\n"
                    plan += f"  - **Estimated**: {task.estimated_tokens:,} tokens, {task.estimated_duration}\n"
                    plan += f"  - **Deliverables**: {', '.join(task.deliverables)}\n"
                    if task.notes:
                        plan += f"  - **Notes**: {'; '.join(task.notes)}\n"
                    plan += "\n"
        
        # Add milestones
        plan += "## Project Milestones\n\n"
        for milestone in self.project.milestones.values():
            progress_icon = "✅" if milestone.completion_percentage == 100 else "🔄" if milestone.completion_percentage > 0 else "⏳"
            plan += f"- {progress_icon} **{milestone.id}**: {milestone.title}\n"
            plan += f"  - **Target Date**: {milestone.target_date}\n"
            plan += f"  - **Progress**: {milestone.completion_percentage:.1f}%\n"
            plan += f"  - **Required Tasks**: {', '.join(milestone.required_tasks)}\n\n"
        
        # Add quality gates
        plan += "## Quality Gates\n\n"
        for i, gate in enumerate(self.project.quality_gates, 1):
            plan += f"**Gate {i}**: {gate['name']}\n"
            plan += f"- **Criteria**: {gate['criteria']}\n"
            plan += f"- **Phase**: {gate['phase']}\n\n"
        
        # Add risk register
        plan += "## Risk Register\n\n"
        for risk in self.project.risk_register:
            plan += f"**{risk['category']}**: {risk['description']}\n"
            plan += f"- **Impact**: {risk['impact']} | **Probability**: {risk['probability']}\n"
            plan += f"- **Mitigation**: {risk['mitigation']}\n\n"
        
        return plan
    
    def generate_task_execution_script(self, task_id: str) -> str:
        """Generate executable script for specific task"""
        
        if not self.project or task_id not in self.project.tasks:
            raise ValueError(f"Task {task_id} not found in current project")
        
        task = self.project.tasks[task_id]
        
        script = f'''#!/usr/bin/env python3
"""
Task Execution Script: {task.title}
Project: {self.project.title}
Task ID: {task_id}
"""

def execute_task():
    """Execute {task_id} using {task.assigned_agent}"""
    
    task_prompt = """
    Task: {task.title}
    
    Description: {task.description}
    
    Deliverables Required:
    {chr(10).join("- " + d for d in task.deliverables)}
    
    Context:
    - Project: {self.project.title}
    - Phase: {task.phase.value}
    - Dependencies: {", ".join(task.dependencies) if task.dependencies else "None"}
    
    Instructions:
    1. Execute the task according to the description
    2. Ensure all deliverables are created
    3. Follow educational content development best practices
    4. Include proper metadata for NotebookLM optimization
    5. Report progress and any blockers
    
    Expected Output:
    - Completed deliverables
    - Progress report with completion status
    - Recommendations for next steps
    - Any identified issues or dependencies
    """
    
    # Task execution using Claude Code Task protocol
    task_call = f"""
Task(
    subagent_type="general-purpose",
    description="{task.title}",
    prompt=\"\"\"Use {task.assigned_agent} subagent to {{task_prompt}}\"\"\"
)
"""
    
    print("Executing Task Call:")
    print(task_call)
    
    # Update project status
    update_task_status("{task_id}", "in_progress")
    
    return task_call

def update_task_status(task_id: str, status: str):
    """Update task status in project file"""
    import json
    
    with open("{self.project_file}", "r") as f:
        project_data = json.load(f)
    
    if task_id in project_data["tasks"]:
        project_data["tasks"][task_id]["status"] = status
        if status == "completed":
            from datetime import datetime
            project_data["tasks"][task_id]["completion_date"] = datetime.now().isoformat()
    
    with open("{self.project_file}", "w") as f:
        json.dump(project_data, f, indent=2)

if __name__ == "__main__":
    print("Starting task execution...")
    result = execute_task()
    print("Task execution initiated.")
'''
        
        return script
    
    def _calculate_target_date(self, scope: Dict[str, Any]) -> str:
        """Calculate target completion date based on scope"""
        from datetime import datetime, timedelta
        
        # Estimate based on complexity
        modules = len(scope.get("modules", ["module1"]))
        skill_levels = len(scope.get("skill_levels", ["beginner", "intermediate"]))
        
        # Rough estimation: 1 week per module per 2 skill levels
        estimated_weeks = (modules * skill_levels) / 2
        target_date = datetime.now() + timedelta(weeks=max(1, estimated_weeks))
        
        return target_date.isoformat()
    
    def _calculate_milestone_date(self, phase: ProjectPhase, task_count: int) -> str:
        """Calculate milestone target date"""
        from datetime import datetime, timedelta
        
        phase_order = list(ProjectPhase)
        phase_index = phase_order.index(phase)
        
        # Estimate weeks based on phase and task count
        base_weeks = (phase_index + 1) * 0.5
        task_weeks = task_count * 0.2
        
        target_date = datetime.now() + timedelta(weeks=base_weeks + task_weeks)
        return target_date.isoformat()
    
    def _define_quality_gates(self, scope: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define quality gates for the project"""
        
        return [
            {
                "name": "Content Quality Gate",
                "phase": "development", 
                "criteria": "All content meets pedagogical standards and technical accuracy",
                "validation_method": "Automated review + expert validation"
            },
            {
                "name": "Assessment Quality Gate",
                "phase": "development",
                "criteria": "Assessments align with learning objectives and show no bias",
                "validation_method": "Bias detection algorithms + accessibility audit"
            },
            {
                "name": "Integration Quality Gate", 
                "phase": "quality_assurance",
                "criteria": "Cross-module consistency and smooth learning progression",
                "validation_method": "Cross-reference validation + learner journey mapping"
            },
            {
                "name": "NotebookLM Optimization Gate",
                "phase": "optimization",
                "criteria": "Content optimized for AI processing with rich metadata",
                "validation_method": "NotebookLM compatibility testing + metadata validation"
            }
        ]
    
    def _identify_initial_risks(self, scope: Dict[str, Any], total_tokens: int) -> List[Dict[str, Any]]:
        """Identify initial project risks"""
        
        risks = []
        
        # Token budget risk
        token_budget = scope.get("token_budget", 500000)
        if total_tokens > token_budget * 0.8:
            risks.append({
                "category": "Resource",
                "description": "Estimated token usage exceeds 80% of budget",
                "impact": "High",
                "probability": "Medium", 
                "mitigation": "Implement token monitoring and optimize content generation"
            })
        
        # Complexity risk
        if len(scope.get("modules", [])) > 4:
            risks.append({
                "category": "Scope",
                "description": "High number of modules may lead to timeline overruns",
                "impact": "Medium",
                "probability": "Medium",
                "mitigation": "Prioritize core modules and consider phased delivery"
            })
        
        # Quality risk
        risks.append({
            "category": "Quality",
            "description": "Maintaining consistency across skill levels and modules",
            "impact": "High",
            "probability": "Low",
            "mitigation": "Implement automated quality gates and regular reviews"
        })
        
        return risks
    
    def save_project(self):
        """Save project state to file"""
        if self.project:
            project_dict = asdict(self.project)
            
            # Convert enums to strings for JSON serialization
            for task in project_dict["tasks"].values():
                task["status"] = task["status"].value if isinstance(task["status"], TaskStatus) else task["status"]
                task["phase"] = task["phase"].value if isinstance(task["phase"], ProjectPhase) else task["phase"]
            
            for milestone in project_dict["milestones"].values():
                milestone["status"] = milestone["status"].value if isinstance(milestone["status"], TaskStatus) else milestone["status"]
                
            project_dict["current_phase"] = project_dict["current_phase"].value if isinstance(project_dict["current_phase"], ProjectPhase) else project_dict["current_phase"]
            
            with open(self.project_file, "w") as f:
                json.dump(project_dict, f, indent=2)
    
    def load_project(self, project_file: str):
        """Load project from file"""
        with open(project_file, "r") as f:
            project_dict = json.load(f)
        
        # Convert string enums back to enum objects
        for task in project_dict["tasks"].values():
            task["status"] = TaskStatus(task["status"])
            task["phase"] = ProjectPhase(task["phase"])
        
        for milestone in project_dict["milestones"].values():
            milestone["status"] = TaskStatus(milestone["status"])
            
        project_dict["current_phase"] = ProjectPhase(project_dict["current_phase"])
        
        self.project = CurriculumProject(**project_dict)
        self.project_file = project_file

def main():
    """Example usage of curriculum project manager"""
    
    print("="*60)
    print("AI CURRICULUM PROJECT MANAGER")
    print("="*60)
    
    # Initialize project manager
    pm = CurriculumProjectManager()
    
    # Define project scope
    project_scope = {
        "modules": ["module1_foundations", "module2_machine_learning", "module3_deep_learning"],
        "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
        "deliverables": ["content", "assessments", "notebooklm_optimization"],
        "token_budget": 750000,
        "notebooklm_optimization": True
    }
    
    # Create project
    project = pm.create_project(
        title="Comprehensive AI Curriculum Development",
        description="Create multi-level AI curriculum with content, assessments, and NotebookLM optimization",
        scope=project_scope
    )
    
    print(f"✅ Project Created: {project.project_id}")
    print(f"📊 Total Tasks: {len(project.tasks)}")
    print(f"🎯 Milestones: {len(project.milestones)}")
    print(f"⚡ Estimated Tokens: {project.resource_usage['total_estimated_tokens']:,}")
    
    # Generate orchestrator plan
    orchestrator_plan = pm.generate_orchestrator_plan()
    
    print("\\n" + "="*40)
    print("ORCHESTRATOR PROJECT PLAN GENERATED")
    print("="*40)
    print("\\nPlan saved and ready for orchestrator execution.")
    print("\\nTo execute with orchestrator:")
    print("Task(subagent_type='general-purpose', prompt='Use orchestrator subagent to execute this project plan')")
    
    # Generate sample task execution script
    first_task_id = list(project.tasks.keys())[0]
    script = pm.generate_task_execution_script(first_task_id)
    
    script_filename = f"execute_{first_task_id}.py"
    with open(script_filename, "w") as f:
        f.write(script)
    
    print(f"\\n📝 Sample task script generated: {script_filename}")
    print("\\n🚀 Project ready for autonomous execution!")

if __name__ == "__main__":
    main()