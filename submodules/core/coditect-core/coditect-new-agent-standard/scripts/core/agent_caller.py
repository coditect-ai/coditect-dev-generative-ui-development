#!/usr/bin/env python3
"""
Core Agent Caller - Standardized Task Tool Proxy Pattern Implementation
Provides consistent, reusable agent invocation using verified Task protocol.
"""

import json
import time
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    """Available agent types from 47-agent framework"""
    ORCHESTRATOR = "orchestrator"
    PROJECT_ORGANIZER = "project-organizer" 
    CODEBASE_ANALYZER = "codebase-analyzer"
    CODEBASE_LOCATOR = "codebase-locator"
    SECURITY_SPECIALIST = "security-specialist"
    BACKEND_ARCHITECT = "backend-architect"
    RUST_EXPERT_DEVELOPER = "rust-expert-developer"
    COMPETITIVE_MARKET_ANALYST = "competitive-market-analyst"
    WEB_SEARCH_RESEARCHER = "web-search-researcher"

@dataclass
class TaskProgress:
    """Track task execution progress with checkpoints"""
    task_id: str
    agent_type: AgentType
    status: str  # pending, in_progress, completed, failed
    progress: int  # 0-100
    checkpoint: str  # Current checkpoint description
    started_at: str
    completed_at: Optional[str] = None
    results: Optional[Dict] = None
    errors: Optional[List[str]] = None

class AgentCaller:
    """Core agent calling infrastructure using Task Tool Proxy Pattern"""
    
    def __init__(self):
        self.session_id = f"session_{int(time.time())}"
        self.task_history: List[TaskProgress] = []
        
    def call_agent(self, 
                   agent_type: AgentType,
                   prompt: str,
                   task_id: Optional[str] = None) -> TaskProgress:
        """
        Call agent using verified Task Tool Proxy Pattern
        
        Args:
            agent_type: Agent to invoke from AgentType enum
            prompt: Detailed task description for the agent
            task_id: Optional task identifier for tracking
            
        Returns:
            TaskProgress object for monitoring execution
        """
        if not task_id:
            task_id = f"task_{int(time.time())}"
            
        # Create progress tracker
        progress = TaskProgress(
            task_id=task_id,
            agent_type=agent_type,
            status="pending",
            progress=0,
            checkpoint="Initializing agent call",
            started_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Build Task protocol prompt
        task_prompt = f"Use {agent_type.value} subagent to {prompt}"
        
        # Log the call
        self.task_history.append(progress)
        
        print(f"🎯 Calling {agent_type.value} agent...")
        print(f"📋 Task: {task_prompt}")
        print(f"🆔 Task ID: {task_id}")
        
        # This would integrate with Claude Code's Task tool
        # For now, return the progress tracker
        progress.status = "in_progress"
        progress.checkpoint = "Agent invoked, awaiting response"
        
        return progress
    
    def call_orchestrator(self,
                         workflow_description: str,
                         agents_needed: List[AgentType],
                         task_breakdown: List[str]) -> TaskProgress:
        """
        Call orchestrator for multi-agent coordination
        
        Args:
            workflow_description: High-level workflow description
            agents_needed: List of agents to coordinate
            task_breakdown: List of specific tasks to execute
            
        Returns:
            TaskProgress for orchestration workflow
        """
        agents_list = [agent.value for agent in agents_needed]
        tasks_formatted = "\n".join([f"- {task}" for task in task_breakdown])
        
        prompt = f"""coordinate a comprehensive workflow for: {workflow_description}

Required agents for coordination: {', '.join(agents_list)}

Task breakdown:
{tasks_formatted}

Please provide:
1. Detailed execution plan with checkboxes
2. Agent coordination strategy  
3. Progress checkpoints (25%, 50%, 75%, 100%)
4. Resource and timeline estimates
5. Quality gates and validation steps"""
        
        return self.call_agent(AgentType.ORCHESTRATOR, prompt)
    
    def get_task_status(self, task_id: str) -> Optional[TaskProgress]:
        """Get current status of a task"""
        for task in self.task_history:
            if task.task_id == task_id:
                return task
        return None
    
    def list_active_tasks(self) -> List[TaskProgress]:
        """Get all tasks that are currently in progress"""
        return [task for task in self.task_history 
                if task.status == "in_progress"]
    
    def export_session_report(self) -> Dict:
        """Export complete session report with all task history"""
        return {
            "session_id": self.session_id,
            "total_tasks": len(self.task_history),
            "completed_tasks": len([t for t in self.task_history if t.status == "completed"]),
            "failed_tasks": len([t for t in self.task_history if t.status == "failed"]),
            "task_history": [
                {
                    "task_id": t.task_id,
                    "agent_type": t.agent_type.value,
                    "status": t.status,
                    "progress": t.progress,
                    "started_at": t.started_at,
                    "completed_at": t.completed_at
                }
                for t in self.task_history
            ]
        }

# Example usage patterns
if __name__ == "__main__":
    caller = AgentCaller()
    
    # Single agent call
    task = caller.call_agent(
        AgentType.CODEBASE_ANALYZER,
        "analyze the authentication system implementation and document security patterns"
    )
    
    # Multi-agent orchestration
    orchestration = caller.call_orchestrator(
        workflow_description="Implement secure user profile management feature",
        agents_needed=[
            AgentType.CODEBASE_LOCATOR,
            AgentType.BACKEND_ARCHITECT, 
            AgentType.RUST_EXPERT_DEVELOPER,
            AgentType.SECURITY_SPECIALIST
        ],
        task_breakdown=[
            "Locate existing user management code",
            "Design API endpoints for profile updates", 
            "Implement backend with security validation",
            "Conduct security review and testing"
        ]
    )
    
    print(f"Session report: {caller.export_session_report()}")