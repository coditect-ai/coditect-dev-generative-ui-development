#!/usr/bin/env python3
"""
Project Manager Script Template - Complete Workflow Management
Reusable template for comprehensive project management with autonomous execution.
"""

import sys
import os
import json
from datetime import datetime

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from agent_caller import AgentCaller, AgentType
from workflow_analyzer import WorkflowAnalyzer  
from autonomous_manager import AutonomousManager, TaskPriority

class ProjectManagerScript:
    """Reusable project management script template"""
    
    def __init__(self, project_name: str, description: str):
        self.project_name = project_name
        self.description = description
        self.session_id = f"pm_{project_name}_{int(datetime.now().timestamp())}"
        
        # Initialize core components
        self.agent_caller = AgentCaller()
        self.workflow_analyzer = WorkflowAnalyzer()
        self.autonomous_manager = AutonomousManager(self.session_id)
        
        # Project state
        self.project_plan = None
        self.execution_report = None
        self.deliverables = []
        
    def analyze_requirements(self, additional_context: dict = None) -> dict:
        """
        Step 1: Analyze project requirements using WorkflowAnalyzer
        Returns comprehensive analysis with agent recommendations
        """
        print(f"🔍 Analyzing requirements for: {self.project_name}")
        
        context = additional_context or {}
        context.update({
            "project_name": self.project_name,
            "session_id": self.session_id
        })
        
        analysis = self.workflow_analyzer.analyze_workflow(self.description, context)
        
        print(f"📋 Analysis complete:")
        print(f"   - Complexity: {analysis['estimated_complexity']}")
        print(f"   - Agents needed: {len(analysis['agent_recommendations'])}")
        print(f"   - Phases: {len(analysis['execution_plan'])}")
        
        return analysis
    
    def create_execution_plan(self, analysis: dict) -> list:
        """
        Step 2: Create detailed execution plan with autonomous tasks
        Returns list of AutonomousTask objects
        """
        print(f"📊 Creating execution plan...")
        
        tasks = self.autonomous_manager.create_task_plan(self.description, analysis)
        
        print(f"✅ Execution plan created:")
        print(f"   - Total tasks: {len(tasks)}")
        print(f"   - Estimated duration: {sum(task.timeout_minutes for task in tasks)} minutes")
        
        return tasks
    
    def setup_orchestrator_monitoring(self):
        """
        Step 3: Setup orchestrator communication and monitoring
        Registers callbacks for progress reporting
        """
        print(f"🎭 Setting up orchestrator monitoring...")
        
        def progress_callback(report):
            """Handle progress reports from autonomous execution"""
            print(f"\n📈 Progress Update:")
            print(f"   Phase: {report.current_phase}")
            print(f"   Progress: {report.overall_progress:.1f}%")
            print(f"   Completed: {report.completed_tasks}/{report.total_tasks}")
            
            if report.issues_encountered:
                print(f"   ⚠️  Issues: {len(report.issues_encountered)}")
                
            if report.next_actions:
                print(f"   Next: {report.next_actions[0]}")
        
        def orchestrator_callback(report):
            """Send reports to orchestrator agent"""
            # Call orchestrator agent with progress update
            orchestrator_prompt = f"""
            AUTONOMOUS EXECUTION PROGRESS REPORT
            
            Project: {self.project_name}
            Session: {self.session_id}
            Current Phase: {report.current_phase}
            Overall Progress: {report.overall_progress:.1f}%
            
            Status Summary:
            - Total Tasks: {report.total_tasks}
            - Completed: {report.completed_tasks} 
            - Failed: {report.failed_tasks}
            - Blocked: {report.blocked_tasks}
            
            Current State:
            {json.dumps(report.next_actions, indent=2)}
            
            Issues Encountered:
            {json.dumps(report.issues_encountered, indent=2)}
            
            Please provide:
            1. Strategic guidance for next phase
            2. Risk assessment and mitigation
            3. Resource optimization recommendations
            4. Quality gate validation
            """
            
            # This would call the actual orchestrator agent
            # self.agent_caller.call_agent(AgentType.ORCHESTRATOR, orchestrator_prompt)
        
        self.autonomous_manager.register_orchestrator_callback(progress_callback)
        self.autonomous_manager.register_orchestrator_callback(orchestrator_callback)
        
        print(f"✅ Orchestrator monitoring active")
    
    def execute_autonomous_workflow(self, tasks: list) -> dict:
        """
        Step 4: Execute autonomous workflow with full monitoring
        Returns final execution report
        """
        print(f"🚀 Starting autonomous execution...")
        
        # Add tasks to manager
        self.autonomous_manager.add_tasks(tasks)
        
        # Start execution
        final_report = self.autonomous_manager.start_autonomous_execution()
        
        print(f"\n🎯 Execution Complete:")
        print(f"   Success Rate: {(final_report.completed_tasks / final_report.total_tasks * 100):.1f}%")
        print(f"   Total Duration: Estimated based on task count")
        
        return final_report
    
    def generate_deliverables(self) -> dict:
        """
        Step 5: Generate final project deliverables
        Consolidates all outputs and creates comprehensive documentation
        """
        print(f"📄 Generating project deliverables...")
        
        execution_summary = self.autonomous_manager.export_execution_summary()
        
        deliverables = {
            "project_overview": {
                "name": self.project_name,
                "description": self.description,
                "session_id": self.session_id,
                "completion_time": datetime.now().isoformat()
            },
            "execution_summary": execution_summary,
            "deliverables_list": execution_summary.get("final_deliverables", []),
            "quality_metrics": {
                "success_rate": f"{(execution_summary['execution_summary']['successful_tasks'] / execution_summary['execution_summary']['total_tasks'] * 100):.1f}%",
                "retry_rate": f"{(execution_summary['execution_summary']['total_retries'] / execution_summary['execution_summary']['total_tasks']):.1f}",
                "total_execution_time": "Calculated based on task complexity"
            },
            "recommendations": [
                "Review all generated deliverables for quality",
                "Validate security implementations", 
                "Test all functionality end-to-end",
                "Plan deployment and monitoring strategy"
            ]
        }
        
        print(f"✅ Deliverables generated:")
        print(f"   - Final deliverables: {len(deliverables['deliverables_list'])}")
        print(f"   - Success rate: {deliverables['quality_metrics']['success_rate']}")
        
        return deliverables
    
    def run_complete_workflow(self, additional_context: dict = None) -> dict:
        """
        Execute complete project management workflow
        One-command execution of entire process
        """
        print(f"\n🎯 Starting Complete Project Management Workflow")
        print(f"Project: {self.project_name}")
        print(f"Description: {self.description}")
        print(f"Session: {self.session_id}")
        print("=" * 60)
        
        try:
            # Step 1: Requirements Analysis
            analysis = self.analyze_requirements(additional_context)
            
            # Step 2: Execution Planning  
            tasks = self.create_execution_plan(analysis)
            
            # Step 3: Orchestrator Setup
            self.setup_orchestrator_monitoring()
            
            # Step 4: Autonomous Execution
            execution_report = self.execute_autonomous_workflow(tasks)
            
            # Step 5: Generate Deliverables
            deliverables = self.generate_deliverables()
            
            print("\n" + "=" * 60)
            print(f"🎉 PROJECT COMPLETE: {self.project_name}")
            print(f"✅ All workflows executed successfully")
            print(f"📊 Final deliverables ready for review")
            
            return deliverables
            
        except Exception as e:
            print(f"\n❌ Workflow execution failed: {str(e)}")
            return {"error": str(e), "session_id": self.session_id}
    
    def save_session_state(self, filename: str = None):
        """Save complete session state for later analysis"""
        if not filename:
            filename = f"session_{self.session_id}.json"
        
        state = {
            "project_name": self.project_name,
            "description": self.description, 
            "session_id": self.session_id,
            "execution_summary": self.autonomous_manager.export_execution_summary(),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2, default=str)
        
        print(f"💾 Session state saved to: {filename}")

# Example usage patterns
def example_backend_project():
    """Example: Backend API development project"""
    project = ProjectManagerScript(
        project_name="user_authentication_api",
        description="Implement secure user authentication API with Rust backend, including registration, login, session management, and comprehensive security validation"
    )
    
    context = {
        "tech_stack": ["Rust", "PostgreSQL", "Redis"],
        "security_requirements": ["OAuth2", "JWT", "Rate limiting"],
        "compliance_needs": ["SOC2", "GDPR"]
    }
    
    return project.run_complete_workflow(context)

def example_frontend_project():
    """Example: Frontend application project"""
    project = ProjectManagerScript(
        project_name="user_dashboard", 
        description="Create responsive user dashboard with React, including profile management, data visualization, and real-time updates"
    )
    
    context = {
        "tech_stack": ["React", "TypeScript", "Material-UI"],
        "features": ["Profile editing", "Charts", "WebSocket updates"],
        "performance_targets": ["<3s load time", "90+ Lighthouse score"]
    }
    
    return project.run_complete_workflow(context)

def example_research_project():
    """Example: Market research project"""
    project = ProjectManagerScript(
        project_name="ai_ide_market_analysis",
        description="Comprehensive market research and competitive analysis for AI-powered IDE positioning and pricing strategy"
    )
    
    context = {
        "competitors": ["Cursor", "GitHub Copilot", "JetBrains AI"],
        "research_areas": ["Pricing models", "Feature differentiation", "Market size"],
        "deliverable_format": ["Executive summary", "Competitive matrix", "Recommendations"]
    }
    
    return project.run_complete_workflow(context)

if __name__ == "__main__":
    # Run example project
    if len(sys.argv) > 1:
        example_type = sys.argv[1]
        
        if example_type == "backend":
            result = example_backend_project()
        elif example_type == "frontend":  
            result = example_frontend_project()
        elif example_type == "research":
            result = example_research_project()
        else:
            print("Usage: python project_manager_script.py [backend|frontend|research]")
            sys.exit(1)
    else:
        # Custom project
        project = ProjectManagerScript(
            project_name="custom_project",
            description="Your project description here"
        )
        result = project.run_complete_workflow()
    
    print(f"\nFinal result keys: {list(result.keys())}")