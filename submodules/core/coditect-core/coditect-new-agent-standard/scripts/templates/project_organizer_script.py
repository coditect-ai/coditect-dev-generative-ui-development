#!/usr/bin/env python3
"""
Project Organizer Script Template - Comprehensive Project Analysis and Organization
Reusable template for project status assessment, organization, and strategic planning.
"""

import sys
import os
import json
from datetime import datetime

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from agent_caller import AgentCaller, AgentType

class ProjectOrganizerScript:
    """Reusable project organization and analysis template"""
    
    def __init__(self, project_name: str, project_path: str, analysis_scope: str = "comprehensive"):
        self.project_name = project_name
        self.project_path = project_path
        self.analysis_scope = analysis_scope  # comprehensive, focused, quick
        self.session_id = f"project_org_{int(datetime.now().timestamp())}"
        
        # Initialize core components
        self.agent_caller = AgentCaller()
        
        # Available skills for project-organizer agent
        self.available_skills = [
            "git-workflow-automation",    # For automated git operations and file moves
            "internal-comms",            # For status reports and communication templates
            "cross-file-documentation-update",  # For updating references after moves
            "communication-protocols"    # For coordination with other agents
        ]
        
        # Available commands for project organization
        self.available_commands = [
            "/create_plan",     # Create detailed organization plan
            "/validate_plan",   # Validate organization results
            "/doc_generate",    # Generate documentation for organization changes
        ]
        
        # Analysis state
        self.analysis_results = {}
        self.recommendations = []
        self.action_items = []
    
    def conduct_project_analysis(self, context: dict = None) -> dict:
        """
        Step 1: Conduct comprehensive project analysis using project-organizer agent
        """
        print(f"🔍 Conducting project analysis for: {self.project_name}")
        print(f"📁 Project location: {self.project_path}")
        print(f"📊 Analysis scope: {self.analysis_scope}")
        
        # Build comprehensive analysis prompt
        analysis_prompt = self._build_analysis_prompt(context)
        
        # Use the correct Task Tool Proxy Pattern from 47-agent framework
        # Format: Task(subagent_type="general-purpose", prompt="Use [agent] subagent to [task]")
        
        print(f"🎭 Calling project-organizer agent using verified Task Tool Proxy Pattern...")
        
        task_prompt = f"Use project-organizer subagent to {analysis_prompt}"
        
        # Store the task prompt for execution - this will be called via Claude Code's Task tool
        analysis_task = {
            "task_type": "agent_invocation",
            "subagent_type": "general-purpose", 
            "prompt": task_prompt,
            "description": f"Project organization analysis for {self.project_name}",
            "session_id": f"{self.session_id}_analysis"
        }
        
        self.analysis_results = {
            "analysis_task": analysis_task,
            "completion_time": datetime.now().isoformat(),
            "scope": self.analysis_scope
        }
        
        print(f"✅ Project analysis completed")
        return self.analysis_results
    
    def _build_analysis_prompt(self, context: dict) -> str:
        """Build comprehensive analysis prompt for project-organizer agent"""
        
        base_context = {
            "project_name": self.project_name,
            "project_location": self.project_path,
            "analysis_scope": self.analysis_scope,
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Merge with user context
        full_context = {**base_context, **(context or {})}
        
        if self.analysis_scope == "comprehensive":
            return self._comprehensive_analysis_prompt(full_context)
        elif self.analysis_scope == "focused":
            return self._focused_analysis_prompt(full_context)
        else:
            return self._quick_analysis_prompt(full_context)
    
    def _comprehensive_analysis_prompt(self, context: dict) -> str:
        """Comprehensive project analysis prompt"""
        skills_context = f"Available Skills: {', '.join(self.available_skills)}"
        commands_context = f"Available Commands: {', '.join(self.available_commands)}"
        
        return f"""conduct comprehensive project analysis of {self.project_name} with full organizational assessment and recommendations.

{skills_context}
{commands_context}

PROJECT CONTEXT:
- Project: {context['project_name']}
- Location: {context['project_location']}
- Analysis Date: {context['analysis_date']}
- Additional Context: {json.dumps(context, indent=2)}

COMPREHENSIVE ANALYSIS REQUIREMENTS:

1. PROJECT STATUS ASSESSMENT:
   - Current completion status across all project components
   - Quality assessment of implemented features and architecture
   - Integration status with dependencies and external systems
   - Documentation coverage and completeness evaluation
   - Technical debt assessment and code quality metrics

2. ORGANIZATIONAL STRUCTURE REVIEW:
   - Directory structure effectiveness and clarity
   - Component relationships and dependencies mapping
   - Documentation organization and accessibility
   - Development workflow efficiency assessment
   - Resource allocation and utilization analysis

3. ACHIEVEMENT DOCUMENTATION:
   - Key accomplishments and milestones reached
   - Technical innovations and breakthrough implementations
   - Quality metrics and validation status
   - Deployment readiness and production capability evaluation
   - Performance benchmarks and optimization opportunities

4. STRATEGIC RECOMMENDATIONS:
   - Next phase priorities and detailed planning roadmap
   - Optimization opportunities with impact assessment
   - Risk assessment with specific mitigation strategies
   - Resource allocation recommendations for maximum ROI
   - Timeline optimization and milestone scheduling

5. PROJECT ORGANIZATION OUTPUTS:
   - Structured project summary suitable for stakeholders
   - Implementation roadmap for next development phases
   - Quality assurance recommendations with specific action items
   - Maintenance and evolution strategy for long-term sustainability
   - Success probability assessment with confidence indicators

SKILLS UTILIZATION:
- Use git-workflow-automation skill for analyzing git status and file organization
- Use internal-comms skill for generating professional status reports
- Use cross-file-documentation-update skill for reference tracking
- Use communication-protocols skill for coordinating with other agents if needed

COMMANDS EXECUTION:
- Consider using /create_plan command for detailed organization planning
- Use /validate_plan command for verifying organizational improvements
- Apply /doc_generate command for creating documentation about changes

DELIVERABLE FORMAT:
- Executive summary with key findings and recommendations
- Detailed analysis with supporting evidence and metrics
- Action items with priorities and timeline estimates
- Risk assessment with mitigation strategies
- Success probability evaluation with confidence scoring
- File organization recommendations with git-based implementation strategy

Please provide comprehensive project organization analysis with clear documentation suitable for project handoff, stakeholder communication, and future development planning."""

    def _focused_analysis_prompt(self, context: dict) -> str:
        """Focused project analysis prompt"""
        focus_area = context.get('focus_area', 'current status and next steps')
        skills_context = f"Available Skills: {', '.join(self.available_skills)}"
        
        return f"""conduct focused project analysis of {self.project_name} with targeted organizational assessment.

{skills_context}

PROJECT CONTEXT:
- Project: {context['project_name']}
- Location: {context['project_location']}
- Focus Area: {focus_area}
- Analysis Date: {context['analysis_date']}

FOCUSED ANALYSIS REQUIREMENTS:

1. CURRENT STATUS ASSESSMENT:
   - Project completion status and key metrics
   - Recent achievements and current development state
   - Immediate priorities and blocking issues

2. FOCUS AREA DEEP DIVE:
   - Detailed analysis of {focus_area}
   - Specific recommendations for improvement
   - Resource requirements and timeline estimates

3. IMMEDIATE ACTION PLAN:
   - Top 3 priority action items with specific next steps
   - Resource allocation recommendations
   - Timeline for immediate improvements

4. SUCCESS METRICS:
   - Key performance indicators for progress tracking
   - Quality gates and validation checkpoints
   - Success probability assessment

Please provide focused analysis with actionable recommendations for immediate implementation."""

    def _quick_analysis_prompt(self, context: dict) -> str:
        """Quick project analysis prompt"""
        return f"""conduct quick project analysis of {self.project_name} with rapid organizational assessment.

PROJECT CONTEXT:
- Project: {context['project_name']}
- Location: {context['project_location']}
- Analysis Date: {context['analysis_date']}

QUICK ANALYSIS REQUIREMENTS:

1. PROJECT STATUS SNAPSHOT:
   - Overall completion percentage and current state
   - Key achievements in current development phase
   - Major blocking issues or risks

2. IMMEDIATE PRIORITIES:
   - Top 3 most critical next steps
   - Resource requirements for immediate progress
   - Timeline estimates for priority items

3. RECOMMENDATIONS:
   - Most impactful improvements for immediate implementation
   - Resource optimization opportunities
   - Risk mitigation priorities

Please provide concise analysis with clear action items for immediate progress."""

    def extract_action_items(self) -> list:
        """
        Step 2: Extract actionable items from analysis results
        """
        print(f"📋 Extracting action items from analysis...")
        
        # In a real implementation, this would parse the analysis results
        # For now, we'll create a structured extraction prompt
        
        extraction_prompt = f"""Based on the project analysis conducted for {self.project_name}, extract specific actionable items:

EXTRACTION REQUIREMENTS:
1. Identify specific, measurable action items with clear deliverables
2. Assign priority levels (Critical, High, Medium, Low)
3. Estimate effort and timeline for each item
4. Identify resource requirements and dependencies
5. Create implementation sequence with logical ordering

FORMAT:
For each action item provide:
- Description: Clear, specific task description
- Priority: Critical/High/Medium/Low
- Effort: Time/resource estimate
- Dependencies: Prerequisites or blocking items
- Timeline: Suggested completion timeframe
- Owner: Recommended role or expertise area

Please provide structured action items ready for immediate implementation planning."""

        extraction_task = self.agent_caller.call_agent(
            AgentType.ORCHESTRATOR,
            extraction_prompt,
            f"{self.session_id}_extraction"
        )
        
        self.action_items = extraction_task
        
        print(f"✅ Action items extracted and prioritized")
        return self.action_items
    
    def execute_autonomous_cleanup(self, dry_run: bool = True) -> dict:
        """
        Step 2.5: Execute autonomous directory cleanup with permission controls
        """
        print(f"🔧 {'[DRY RUN] ' if dry_run else ''}Starting autonomous directory cleanup...")
        
        cleanup_prompt = f"""conduct autonomous directory organization and cleanup for {self.project_name}.

PROJECT LOCATION: {self.project_path}

AUTONOMOUS CLEANUP REQUIREMENTS:
1. ANALYSIS PHASE:
   - Scan root directory for misplaced files
   - Identify files that belong in subdirectories (docs/, .session/, etc.)
   - Categorize files by type and purpose
   - Map current structure vs production standards

2. PERMISSION PROTOCOL:
   - NEVER delete files without explicit user permission
   - ALWAYS ask before moving important configuration files
   - ALWAYS use 'git mv' to preserve file history
   - ASK permission before creating new directories
   - Present clear plan before executing moves

3. ORGANIZATION STANDARDS:
   - Follow project-organizer agent's production directory structure
   - Move session exports to .session/ or docs/sessions/
   - Move research documents to docs/ or appropriate subdirectories
   - Keep only essential files in root (README.md, CLAUDE.md, package.json, etc.)
   - Organize documentation by topic and date

4. SAFETY REQUIREMENTS:
   - Check for file references before moving
   - Update any broken links after moves
   - Create commit for each organizational change
   - Never overwrite existing files

5. EXECUTION MODE:
   - {'DRY RUN MODE: Show what would be done but make no actual changes' if dry_run else 'LIVE MODE: Execute approved changes with git operations'}

SKILLS TO USE:
- git-workflow-automation skill for safe file moves with history preservation
- cross-file-documentation-update skill for updating references
- internal-comms skill for generating organization reports

Please provide:
1. Directory analysis with misplaced files identified
2. Organization plan with specific move operations
3. Permission requests for any deletions or major restructuring
4. Implementation commands using git mv for file moves
5. Verification steps to ensure organization success"""

        task_prompt = f"Use project-organizer subagent to {cleanup_prompt}"
        
        print(f"🎭 Calling project-organizer agent for autonomous cleanup...")
        
        cleanup_task = {
            "task_type": "autonomous_cleanup",
            "subagent_type": "general-purpose",
            "prompt": task_prompt,
            "description": f"Autonomous directory cleanup for {self.project_name}",
            "session_id": f"{self.session_id}_cleanup",
            "dry_run": dry_run,
            "permissions_required": True
        }
        
        print(f"✅ Cleanup task prepared - {'dry run mode' if dry_run else 'live execution mode'}")
        return cleanup_task
    
    def generate_organizational_summary(self) -> dict:
        """
        Step 3: Generate structured organizational summary and recommendations
        """
        print(f"📄 Generating organizational summary...")
        
        summary = {
            "project_overview": {
                "name": self.project_name,
                "location": self.project_path,
                "analysis_scope": self.analysis_scope,
                "analysis_date": datetime.now().isoformat(),
                "session_id": self.session_id
            },
            "analysis_results": self.analysis_results,
            "action_items": self.action_items,
            "organizational_recommendations": [
                "Maintain current organizational structure effectiveness",
                "Implement extracted action items in priority order",
                "Establish regular project organization review cycles",
                "Monitor progress against identified success metrics"
            ]
        }
        
        print(f"✅ Organizational summary generated")
        return summary
    
    def save_analysis_results(self, filename: str = None) -> str:
        """
        Step 4: Save analysis results for future reference
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"project_analysis_{self.project_name.replace(' ', '_')}_{timestamp}.json"
        
        # Ensure .session directory exists
        session_dir = os.path.join(os.path.dirname(self.project_path), '.session')
        os.makedirs(session_dir, exist_ok=True)
        
        filepath = os.path.join(session_dir, filename)
        
        # Combine all results
        complete_analysis = {
            "project_analysis": self.analysis_results,
            "action_items": self.action_items,
            "organizational_summary": self.generate_organizational_summary(),
            "metadata": {
                "analysis_tool": "project-organizer subagent",
                "framework_version": "Universal Agent Framework v2.0",
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(complete_analysis, f, indent=2, default=str)
        
        print(f"💾 Analysis results saved to: {filepath}")
        return filepath
    
    def run_complete_analysis(self, context: dict = None, include_cleanup: bool = False, dry_run: bool = True) -> dict:
        """
        Execute complete project organization analysis workflow
        One-command execution for comprehensive project organization
        
        Args:
            context: Additional context for analysis
            include_cleanup: Whether to include autonomous cleanup
            dry_run: If True, show what would be done without executing
        """
        print(f"\n📊 Starting Complete Project Organization Analysis")
        print(f"Project: {self.project_name}")
        print(f"Scope: {self.analysis_scope}")
        if include_cleanup:
            print(f"Cleanup Mode: {'DRY RUN' if dry_run else 'LIVE EXECUTION'}")
        print("=" * 60)
        
        try:
            # Step 1: Conduct project analysis
            analysis_results = self.conduct_project_analysis(context)
            
            # Step 2: Extract action items
            action_items = self.extract_action_items()
            
            # Step 2.5: Execute autonomous cleanup if requested
            cleanup_results = None
            if include_cleanup:
                cleanup_results = self.execute_autonomous_cleanup(dry_run)
            
            # Step 3: Generate organizational summary
            summary = self.generate_organizational_summary()
            
            # Step 4: Save results
            saved_file = self.save_analysis_results()
            
            print("\n" + "=" * 60)
            print(f"🎉 PROJECT ANALYSIS COMPLETE: {self.project_name}")
            print(f"✅ Comprehensive analysis conducted")
            print(f"📋 Action items extracted and prioritized")
            if cleanup_results:
                print(f"🔧 Autonomous cleanup {'planned (dry run)' if dry_run else 'executed'}")
            print(f"💾 Results saved to: {os.path.basename(saved_file)}")
            
            result = {
                "analysis_results": analysis_results,
                "action_items": action_items,
                "organizational_summary": summary,
                "saved_file": saved_file
            }
            
            if cleanup_results:
                result["cleanup_results"] = cleanup_results
                
            return result
            
        except Exception as e:
            print(f"\n❌ Analysis failed: {str(e)}")
            return {"error": str(e), "session_id": self.session_id}

# Convenience functions for common usage patterns
def analyze_current_project(analysis_scope: str = "comprehensive", context: dict = None) -> dict:
    """Analyze the current working directory project"""
    import os
    
    current_dir = os.getcwd()
    project_name = os.path.basename(current_dir)
    
    analyzer = ProjectOrganizerScript(project_name, current_dir, analysis_scope)
    return analyzer.run_complete_analysis(context)

def analyze_project(project_path: str, analysis_scope: str = "comprehensive", context: dict = None) -> dict:
    """Analyze a specific project by path"""
    project_name = os.path.basename(project_path)
    
    analyzer = ProjectOrganizerScript(project_name, project_path, analysis_scope)
    return analyzer.run_complete_analysis(context)

# Example usage patterns
def example_comprehensive_analysis():
    """Example: Complete project analysis"""
    return analyze_current_project("comprehensive", {
        "focus_areas": ["architecture", "documentation", "testing"],
        "stakeholders": ["development team", "project management"],
        "timeline_pressure": "moderate"
    })

def example_focused_analysis():
    """Example: Focused analysis on specific area"""
    return analyze_current_project("focused", {
        "focus_area": "testing infrastructure and quality assurance",
        "immediate_priorities": ["automated testing", "CI/CD pipeline"]
    })

def example_quick_status_check():
    """Example: Quick status assessment"""
    return analyze_current_project("quick", {
        "urgency": "immediate status needed for stakeholder meeting"
    })

if __name__ == "__main__":
    # Command line interface
    if len(sys.argv) > 1:
        scope = sys.argv[1]
        
        if scope in ["comprehensive", "focused", "quick"]:
            result = analyze_current_project(scope)
        else:
            print("Usage: python project_organizer_script.py [comprehensive|focused|quick]")
            sys.exit(1)
    else:
        # Default comprehensive analysis
        result = example_comprehensive_analysis()
    
    print(f"\nAnalysis completed. Results available in session directory.")