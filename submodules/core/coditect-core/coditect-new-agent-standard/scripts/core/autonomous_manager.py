#!/usr/bin/env python3
"""
Autonomous Task Manager - Self-Executing Agent Coordination System
Manages autonomous task execution with progress reporting and orchestrator communication.
"""

import json
import time
import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta

from agent_caller import AgentCaller, AgentType, TaskProgress
from workflow_analyzer import WorkflowAnalyzer

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AutonomousTask:
    """Enhanced task definition for autonomous execution"""
    task_id: str
    description: str
    agent_type: AgentType
    priority: TaskPriority
    status: TaskStatus
    dependencies: List[str]  # Task IDs this task depends on
    skills_required: List[str]
    commands_to_execute: List[str]
    expected_deliverables: List[str]
    max_retry_attempts: int = 3
    timeout_minutes: int = 30
    created_at: str = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress: int = 0
    results: Optional[Dict] = None
    error_log: List[str] = None
    retry_count: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.error_log is None:
            self.error_log = []

@dataclass
class ExecutionReport:
    """Report for orchestrator communication"""
    session_id: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    blocked_tasks: int
    overall_progress: float
    current_phase: str
    next_actions: List[str]
    issues_encountered: List[str]
    recommendations: List[str]
    resource_usage: Dict
    timestamp: str

class AutonomousManager:
    """Autonomous task execution and management system"""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"autonomous_{int(time.time())}"
        self.agent_caller = AgentCaller()
        self.workflow_analyzer = WorkflowAnalyzer()
        self.task_queue: List[AutonomousTask] = []
        self.active_tasks: Dict[str, AutonomousTask] = {}
        self.completed_tasks: List[AutonomousTask] = []
        self.orchestrator_callbacks: List[Callable] = []
        self.execution_log: List[Dict] = []
        
    def register_orchestrator_callback(self, callback: Callable):
        """Register callback for orchestrator communication"""
        self.orchestrator_callbacks.append(callback)
    
    def create_task_plan(self, workflow_description: str, context: Dict = None) -> List[AutonomousTask]:
        """
        Create autonomous task plan from workflow description
        Uses WorkflowAnalyzer to determine optimal agent coordination
        """
        analysis = self.workflow_analyzer.analyze_workflow(workflow_description, context)
        tasks = []
        
        task_counter = 1
        
        # Create tasks from execution plan
        for phase in analysis["execution_plan"]:
            for task_desc in phase["tasks"]:
                # Determine agent type from task description
                agent_type = self._determine_agent_type(task_desc, analysis["agent_recommendations"])
                
                # Extract skills and commands
                agent_rec = next((rec for rec in analysis["agent_recommendations"] 
                                if rec.agent_type in task_desc), None)
                
                skills = agent_rec.skills_needed if agent_rec else []
                commands = agent_rec.commands_suggested if agent_rec else []
                
                # Create autonomous task
                task = AutonomousTask(
                    task_id=f"{self.session_id}_task_{task_counter:03d}",
                    description=task_desc,
                    agent_type=AgentType(agent_type),
                    priority=TaskPriority.HIGH,
                    status=TaskStatus.PENDING,
                    dependencies=self._extract_dependencies(task_counter, phase),
                    skills_required=skills,
                    commands_to_execute=commands,
                    expected_deliverables=phase["deliverables"],
                    timeout_minutes=self._estimate_timeout(task_desc)
                )
                
                tasks.append(task)
                task_counter += 1
        
        return tasks
    
    def _determine_agent_type(self, task_desc: str, recommendations: List) -> str:
        """Determine agent type from task description"""
        for rec in recommendations:
            if rec.agent_type in task_desc.lower():
                return rec.agent_type
        
        # Fallback logic
        if any(keyword in task_desc.lower() for keyword in ["locate", "find", "discover"]):
            return "codebase-locator"
        elif any(keyword in task_desc.lower() for keyword in ["analyze", "review"]):
            return "codebase-analyzer"  
        elif any(keyword in task_desc.lower() for keyword in ["implement", "develop"]):
            return "rust-expert-developer"
        elif any(keyword in task_desc.lower() for keyword in ["security", "validate"]):
            return "security-specialist"
        else:
            return "orchestrator"
    
    def _extract_dependencies(self, task_number: int, phase: Dict) -> List[str]:
        """Extract task dependencies based on execution order"""
        dependencies = []
        if task_number > 1:
            # Most tasks depend on the previous task in sequence
            dependencies.append(f"{self.session_id}_task_{task_number-1:03d}")
        return dependencies
    
    def _estimate_timeout(self, task_desc: str) -> int:
        """Estimate task timeout based on complexity"""
        if any(keyword in task_desc.lower() for keyword in ["implement", "develop", "build"]):
            return 45  # Implementation tasks take longer
        elif any(keyword in task_desc.lower() for keyword in ["security", "validate", "test"]):
            return 30  # Validation tasks
        else:
            return 15  # Analysis and discovery tasks
    
    def add_tasks(self, tasks: List[AutonomousTask]):
        """Add tasks to execution queue"""
        for task in tasks:
            self.task_queue.append(task)
            self._log_event("task_added", {
                "task_id": task.task_id,
                "description": task.description,
                "agent_type": task.agent_type.value
            })
    
    def start_autonomous_execution(self) -> ExecutionReport:
        """
        Start autonomous task execution
        Executes tasks respecting dependencies and reporting progress
        """
        self._log_event("execution_started", {
            "total_tasks": len(self.task_queue),
            "session_id": self.session_id
        })
        
        while self.task_queue or self.active_tasks:
            # Find ready tasks (dependencies satisfied)
            ready_tasks = self._find_ready_tasks()
            
            # Execute ready tasks
            for task in ready_tasks:
                self._execute_task(task)
            
            # Check for completed tasks
            self._check_task_completion()
            
            # Report progress to orchestrator
            if ready_tasks:  # Only report if we made progress
                report = self._generate_progress_report()
                self._notify_orchestrator(report)
            
            # Prevent busy waiting
            time.sleep(1)
        
        # Final report
        final_report = self._generate_final_report()
        self._notify_orchestrator(final_report)
        
        return final_report
    
    def _find_ready_tasks(self) -> List[AutonomousTask]:
        """Find tasks ready for execution (dependencies satisfied)"""
        ready_tasks = []
        completed_task_ids = {task.task_id for task in self.completed_tasks}
        
        for task in self.task_queue[:]:  # Copy list to modify during iteration
            if task.status != TaskStatus.PENDING:
                continue
                
            # Check if all dependencies are satisfied
            deps_satisfied = all(dep_id in completed_task_ids for dep_id in task.dependencies)
            
            if deps_satisfied:
                ready_tasks.append(task)
                self.task_queue.remove(task)
        
        return ready_tasks
    
    def _execute_task(self, task: AutonomousTask):
        """Execute a single autonomous task"""
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now().isoformat()
        self.active_tasks[task.task_id] = task
        
        self._log_event("task_started", {
            "task_id": task.task_id,
            "agent_type": task.agent_type.value,
            "description": task.description
        })
        
        try:
            # Build enhanced prompt with context
            enhanced_prompt = self._build_enhanced_prompt(task)
            
            # Call agent using Task protocol
            progress = self.agent_caller.call_agent(
                task.agent_type,
                enhanced_prompt,
                task.task_id
            )
            
            # Update task with progress info
            task.progress = 50  # Execution started
            
            # Simulate task execution (in real implementation, this would be async)
            # For now, mark as completed after brief delay
            time.sleep(2)  # Simulate work
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            task.progress = 100
            task.results = {"status": "success", "deliverables": task.expected_deliverables}
            
            self._log_event("task_completed", {
                "task_id": task.task_id,
                "duration_seconds": 2,
                "deliverables": task.expected_deliverables
            })
            
        except Exception as e:
            self._handle_task_error(task, str(e))
    
    def _build_enhanced_prompt(self, task: AutonomousTask) -> str:
        """Build enhanced prompt with full context for autonomous execution"""
        prompt_parts = [
            f"AUTONOMOUS TASK EXECUTION:",
            f"Task ID: {task.task_id}",
            f"Description: {task.description}",
            f"Priority: {task.priority.value}",
            f"Session: {self.session_id}",
            "",
            f"CONTEXT:",
            f"- Expected deliverables: {', '.join(task.expected_deliverables)}",
            f"- Skills to utilize: {', '.join(task.skills_required)}",
            f"- Commands available: {', '.join(task.commands_to_execute)}",
            f"- Max execution time: {task.timeout_minutes} minutes",
            "",
            f"AUTONOMOUS EXECUTION REQUIREMENTS:",
            f"1. Execute this task completely and autonomously",
            f"2. Provide structured deliverables as specified",
            f"3. Report any issues or blockers encountered",
            f"4. Include progress checkpoints (25%, 50%, 75%, 100%)",
            f"5. Generate summary for orchestrator handoff",
            "",
            f"TASK EXECUTION:",
            task.description
        ]
        
        return "\n".join(prompt_parts)
    
    def _handle_task_error(self, task: AutonomousTask, error: str):
        """Handle task execution errors with retry logic"""
        task.error_log.append(f"{datetime.now().isoformat()}: {error}")
        task.retry_count += 1
        
        if task.retry_count < task.max_retry_attempts:
            task.status = TaskStatus.PENDING
            self.task_queue.append(task)  # Re-queue for retry
            
            self._log_event("task_retry", {
                "task_id": task.task_id,
                "retry_count": task.retry_count,
                "error": error
            })
        else:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now().isoformat()
            
            self._log_event("task_failed", {
                "task_id": task.task_id,
                "final_error": error,
                "retry_count": task.retry_count
            })
    
    def _check_task_completion(self):
        """Check active tasks for completion and move to completed list"""
        completed_tasks = []
        
        for task_id, task in self.active_tasks.items():
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                completed_tasks.append(task_id)
                self.completed_tasks.append(task)
        
        # Remove from active tasks
        for task_id in completed_tasks:
            del self.active_tasks[task_id]
    
    def _generate_progress_report(self) -> ExecutionReport:
        """Generate progress report for orchestrator"""
        total = len(self.task_queue) + len(self.active_tasks) + len(self.completed_tasks)
        completed = len([t for t in self.completed_tasks if t.status == TaskStatus.COMPLETED])
        failed = len([t for t in self.completed_tasks if t.status == TaskStatus.FAILED])
        blocked = len([t for t in self.active_tasks.values() if t.status == TaskStatus.BLOCKED])
        
        overall_progress = (completed / total * 100) if total > 0 else 0
        
        return ExecutionReport(
            session_id=self.session_id,
            total_tasks=total,
            completed_tasks=completed,
            failed_tasks=failed,
            blocked_tasks=blocked,
            overall_progress=overall_progress,
            current_phase=self._determine_current_phase(),
            next_actions=self._determine_next_actions(),
            issues_encountered=[task.error_log[-1] for task in self.completed_tasks if task.error_log],
            recommendations=self._generate_recommendations(),
            resource_usage=self._calculate_resource_usage(),
            timestamp=datetime.now().isoformat()
        )
    
    def _generate_final_report(self) -> ExecutionReport:
        """Generate final execution report"""
        report = self._generate_progress_report()
        report.current_phase = "Completed"
        report.next_actions = ["Review deliverables", "Validate results", "Plan next iteration"]
        return report
    
    def _determine_current_phase(self) -> str:
        """Determine current execution phase"""
        if not self.completed_tasks:
            return "Discovery & Planning"
        elif len(self.completed_tasks) < len(self.task_queue) + len(self.active_tasks) + len(self.completed_tasks) * 0.5:
            return "Core Implementation"
        elif len(self.completed_tasks) < len(self.task_queue) + len(self.active_tasks) + len(self.completed_tasks) * 0.75:
            return "Validation & Security"
        else:
            return "Integration & Completion"
    
    def _determine_next_actions(self) -> List[str]:
        """Determine next actions based on current state"""
        if self.task_queue:
            return [f"Execute {task.description}" for task in self.task_queue[:3]]
        elif self.active_tasks:
            return [f"Complete {task.description}" for task in self.active_tasks.values()]
        else:
            return ["Generate final deliverables", "Prepare orchestrator handoff"]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on execution history"""
        recommendations = []
        
        if any(task.retry_count > 0 for task in self.completed_tasks):
            recommendations.append("Consider increasing timeout for complex tasks")
        
        if len(self.completed_tasks) > 0:
            avg_duration = sum(2 for task in self.completed_tasks) / len(self.completed_tasks)  # Simplified
            if avg_duration > 30:
                recommendations.append("Consider breaking down complex tasks further")
        
        return recommendations
    
    def _calculate_resource_usage(self) -> Dict:
        """Calculate resource usage statistics"""
        return {
            "agents_utilized": len(set(task.agent_type for task in self.completed_tasks)),
            "total_execution_time": f"{len(self.completed_tasks) * 2} seconds",  # Simplified
            "estimated_token_usage": f"{len(self.completed_tasks) * 5000} tokens",
            "retry_rate": f"{sum(task.retry_count for task in self.completed_tasks) / max(len(self.completed_tasks), 1):.1%}"
        }
    
    def _notify_orchestrator(self, report: ExecutionReport):
        """Notify orchestrator of progress"""
        for callback in self.orchestrator_callbacks:
            try:
                callback(report)
            except Exception as e:
                self._log_event("orchestrator_notification_failed", {"error": str(e)})
    
    def _log_event(self, event_type: str, data: Dict):
        """Log execution events"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "session_id": self.session_id,
            "data": data
        }
        self.execution_log.append(log_entry)
    
    def export_execution_summary(self) -> Dict:
        """Export complete execution summary"""
        return {
            "session_id": self.session_id,
            "execution_summary": {
                "total_tasks": len(self.completed_tasks),
                "successful_tasks": len([t for t in self.completed_tasks if t.status == TaskStatus.COMPLETED]),
                "failed_tasks": len([t for t in self.completed_tasks if t.status == TaskStatus.FAILED]),
                "total_retries": sum(task.retry_count for task in self.completed_tasks)
            },
            "task_details": [asdict(task) for task in self.completed_tasks],
            "execution_log": self.execution_log,
            "final_deliverables": [
                deliverable 
                for task in self.completed_tasks 
                if task.status == TaskStatus.COMPLETED
                for deliverable in task.expected_deliverables
            ]
        }

# Example usage
if __name__ == "__main__":
    manager = AutonomousManager()
    
    # Create autonomous execution plan
    tasks = manager.create_task_plan(
        "Implement secure user authentication with Rust backend including API design, security validation, and testing"
    )
    
    # Add tasks and start execution
    manager.add_tasks(tasks)
    
    # Register orchestrator callback
    def orchestrator_callback(report):
        print(f"Progress: {report.overall_progress:.1f}% - {report.current_phase}")
        if report.issues_encountered:
            print(f"Issues: {report.issues_encountered}")
    
    manager.register_orchestrator_callback(orchestrator_callback)
    
    # Start autonomous execution
    final_report = manager.start_autonomous_execution()
    
    print("Execution completed!")
    print(json.dumps(asdict(final_report), indent=2))