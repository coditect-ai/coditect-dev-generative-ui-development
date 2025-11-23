#!/usr/bin/env python3
"""
Performance Monitor - Token Optimization and Execution Tracking
Provides comprehensive performance monitoring with token cost optimization.
"""

import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from contextlib import contextmanager

@dataclass 
class PerformanceMetrics:
    """Performance metrics for agent execution"""
    session_id: str
    agent_type: str
    task_description: str
    start_time: str
    end_time: Optional[str] = None
    duration_seconds: Optional[float] = None
    estimated_tokens: Optional[int] = None
    actual_tokens: Optional[int] = None
    token_efficiency: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None
    optimization_opportunities: List[str] = None
    
    def __post_init__(self):
        if self.optimization_opportunities is None:
            self.optimization_opportunities = []

@dataclass
class SessionSummary:
    """Summary statistics for a performance monitoring session"""
    session_id: str
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    total_duration: float
    total_estimated_tokens: int
    total_actual_tokens: int
    average_efficiency: float
    top_optimizations: List[str]
    performance_grade: str

class PerformanceMonitor:
    """
    Comprehensive performance monitoring with token optimization
    Provides real-time tracking and optimization recommendations
    """
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or f"perf_{int(time.time())}"
        self.metrics: List[PerformanceMetrics] = []
        self.active_tasks: Dict[str, PerformanceMetrics] = {}
        self.optimization_rules = self._load_optimization_rules()
        self.token_budgets = self._load_token_budgets()
        
    def _load_optimization_rules(self) -> Dict[str, Dict]:
        """Load performance optimization rules"""
        return {
            "token_efficiency": {
                "excellent": 0.9,
                "good": 0.75,
                "acceptable": 0.6,
                "needs_optimization": 0.4
            },
            "duration_thresholds": {
                "quick_task": 30,      # seconds
                "normal_task": 120,    # seconds  
                "complex_task": 300,   # seconds
                "long_task": 600       # seconds
            },
            "optimization_patterns": {
                "high_token_usage": "Consider context compression or prompt optimization",
                "slow_execution": "Review agent selection and task complexity",
                "low_efficiency": "Optimize prompt structure and context management",
                "frequent_retries": "Improve error handling and validation",
                "context_overflow": "Implement progressive disclosure patterns"
            }
        }
    
    def _load_token_budgets(self) -> Dict[str, int]:
        """Load token budgets for different agent types and tasks"""
        return {
            # Agent-specific budgets
            "orchestrator": 15000,
            "project-organizer": 8000,
            "codebase-analyzer": 12000,
            "security-specialist": 10000,
            "research-agent": 6000,
            
            # Task-specific budgets  
            "quick_analysis": 3000,
            "comprehensive_analysis": 15000,
            "autonomous_execution": 20000,
            "multi_agent_coordination": 25000,
            
            # Default budgets
            "default_agent": 5000,
            "default_task": 8000
        }
    
    @contextmanager
    def track_performance(self, agent_type: str, task_description: str, estimated_tokens: int = None):
        """
        Context manager for tracking performance of agent execution
        
        Usage:
        with monitor.track_performance("orchestrator", "project analysis") as tracker:
            # Execute agent task
            result = execute_agent_task()
            tracker.log_success(actual_tokens=1500)
        """
        
        # Generate unique task ID
        task_id = f"{agent_type}_{int(time.time())}"
        
        # Create performance metrics
        metrics = PerformanceMetrics(
            session_id=self.session_id,
            agent_type=agent_type,
            task_description=task_description,
            start_time=datetime.now().isoformat(),
            estimated_tokens=estimated_tokens or self._estimate_tokens(agent_type, task_description)
        )
        
        # Add to active tasks
        self.active_tasks[task_id] = metrics
        
        # Create tracker object
        tracker = PerformanceTracker(self, task_id, metrics)
        
        try:
            yield tracker
        except Exception as e:
            # Log failure
            tracker.log_failure(str(e))
            raise
        finally:
            # Finalize metrics
            self._finalize_task_metrics(task_id)
    
    def _estimate_tokens(self, agent_type: str, task_description: str) -> int:
        """Estimate token usage based on agent type and task complexity"""
        
        # Base estimate from agent type
        base_tokens = self.token_budgets.get(agent_type, self.token_budgets["default_agent"])
        
        # Adjust based on task complexity
        complexity_multiplier = 1.0
        
        # Task complexity indicators
        if any(keyword in task_description.lower() for keyword in ['comprehensive', 'complete', 'detailed']):
            complexity_multiplier = 1.5
        elif any(keyword in task_description.lower() for keyword in ['quick', 'simple', 'basic']):
            complexity_multiplier = 0.7
        elif any(keyword in task_description.lower() for keyword in ['autonomous', 'coordinate', 'multi-agent']):
            complexity_multiplier = 2.0
        
        # Task type adjustments
        if 'analysis' in task_description.lower():
            base_tokens = max(base_tokens, self.token_budgets.get("comprehensive_analysis", 15000))
        elif 'research' in task_description.lower():
            base_tokens = max(base_tokens, self.token_budgets.get("research-agent", 6000))
        
        return int(base_tokens * complexity_multiplier)
    
    def _finalize_task_metrics(self, task_id: str):
        """Finalize metrics for completed task"""
        if task_id in self.active_tasks:
            metrics = self.active_tasks[task_id]
            
            # Calculate duration
            if metrics.end_time:
                start = datetime.fromisoformat(metrics.start_time)
                end = datetime.fromisoformat(metrics.end_time)
                metrics.duration_seconds = (end - start).total_seconds()
            
            # Calculate efficiency
            if metrics.estimated_tokens and metrics.actual_tokens:
                metrics.token_efficiency = min(metrics.estimated_tokens / metrics.actual_tokens, 1.0)
            
            # Generate optimization opportunities
            metrics.optimization_opportunities = self._analyze_optimization_opportunities(metrics)
            
            # Move to completed metrics
            self.metrics.append(metrics)
            del self.active_tasks[task_id]
    
    def _analyze_optimization_opportunities(self, metrics: PerformanceMetrics) -> List[str]:
        """Analyze performance metrics and suggest optimizations"""
        opportunities = []
        
        # Token efficiency analysis
        if metrics.token_efficiency is not None:
            if metrics.token_efficiency < self.optimization_rules["token_efficiency"]["needs_optimization"]:
                opportunities.append("High token usage detected - consider prompt optimization")
            elif metrics.token_efficiency < self.optimization_rules["token_efficiency"]["acceptable"]:
                opportunities.append("Moderate token inefficiency - review context management")
        
        # Duration analysis
        if metrics.duration_seconds is not None:
            thresholds = self.optimization_rules["duration_thresholds"]
            if metrics.duration_seconds > thresholds["long_task"]:
                opportunities.append("Long execution time - consider task decomposition")
            elif metrics.duration_seconds > thresholds["complex_task"]:
                opportunities.append("Complex task detected - validate agent selection")
        
        # Error analysis
        if not metrics.success and metrics.error_message:
            if "timeout" in metrics.error_message.lower():
                opportunities.append("Timeout detected - increase limits or optimize complexity")
            elif "token" in metrics.error_message.lower():
                opportunities.append("Token limit issue - implement context compression")
            else:
                opportunities.append("Error handling - review input validation and retry logic")
        
        # Agent-specific optimizations
        agent_type = metrics.agent_type.lower()
        if "orchestrator" in agent_type and metrics.duration_seconds and metrics.duration_seconds > 180:
            opportunities.append("Long orchestration - consider parallel agent execution")
        elif "analyzer" in agent_type and metrics.token_efficiency and metrics.token_efficiency < 0.6:
            opportunities.append("Analysis inefficiency - optimize search patterns and context")
        
        return opportunities
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        
        if not self.metrics:
            return {
                "session_id": self.session_id,
                "status": "no_data",
                "message": "No performance data available"
            }
        
        # Calculate summary statistics
        total_tasks = len(self.metrics)
        successful_tasks = len([m for m in self.metrics if m.success])
        failed_tasks = total_tasks - successful_tasks
        
        total_duration = sum(m.duration_seconds for m in self.metrics if m.duration_seconds)
        
        total_estimated = sum(m.estimated_tokens for m in self.metrics if m.estimated_tokens)
        total_actual = sum(m.actual_tokens for m in self.metrics if m.actual_tokens)
        
        # Calculate average efficiency
        efficiencies = [m.token_efficiency for m in self.metrics if m.token_efficiency]
        average_efficiency = sum(efficiencies) / len(efficiencies) if efficiencies else 0.0
        
        # Collect top optimization opportunities
        all_opportunities = []
        for m in self.metrics:
            all_opportunities.extend(m.optimization_opportunities)
        
        # Count and rank opportunities
        opportunity_counts = {}
        for opp in all_opportunities:
            opportunity_counts[opp] = opportunity_counts.get(opp, 0) + 1
        
        top_optimizations = sorted(opportunity_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_optimizations = [f"{opp} ({count} occurrences)" for opp, count in top_optimizations]
        
        # Determine performance grade
        performance_grade = self._calculate_performance_grade(average_efficiency, failed_tasks, total_tasks)
        
        return {
            "session_summary": SessionSummary(
                session_id=self.session_id,
                total_tasks=total_tasks,
                successful_tasks=successful_tasks,
                failed_tasks=failed_tasks,
                total_duration=total_duration,
                total_estimated_tokens=total_estimated,
                total_actual_tokens=total_actual,
                average_efficiency=average_efficiency,
                top_optimizations=top_optimizations,
                performance_grade=performance_grade
            ),
            "detailed_metrics": [asdict(m) for m in self.metrics],
            "optimization_recommendations": self._generate_optimization_recommendations(),
            "token_usage_analysis": self._analyze_token_usage(),
            "performance_trends": self._analyze_performance_trends()
        }
    
    def _calculate_performance_grade(self, efficiency: float, failed_tasks: int, total_tasks: int) -> str:
        """Calculate overall performance grade"""
        
        # Efficiency score (0-40 points)
        if efficiency >= 0.9:
            efficiency_score = 40
        elif efficiency >= 0.75:
            efficiency_score = 30
        elif efficiency >= 0.6:
            efficiency_score = 20
        else:
            efficiency_score = 10
        
        # Success rate score (0-40 points)
        success_rate = (total_tasks - failed_tasks) / total_tasks if total_tasks > 0 else 0
        if success_rate >= 0.95:
            success_score = 40
        elif success_rate >= 0.85:
            success_score = 30
        elif success_rate >= 0.7:
            success_score = 20
        else:
            success_score = 10
        
        # Task completion score (0-20 points)
        if total_tasks >= 10:
            completion_score = 20
        elif total_tasks >= 5:
            completion_score = 15
        elif total_tasks >= 3:
            completion_score = 10
        else:
            completion_score = 5
        
        total_score = efficiency_score + success_score + completion_score
        
        if total_score >= 90:
            return "A+ (Excellent)"
        elif total_score >= 80:
            return "A (Very Good)" 
        elif total_score >= 70:
            return "B+ (Good)"
        elif total_score >= 60:
            return "B (Satisfactory)"
        elif total_score >= 50:
            return "C+ (Needs Improvement)"
        else:
            return "C (Requires Optimization)"
    
    def _generate_optimization_recommendations(self) -> List[str]:
        """Generate specific optimization recommendations"""
        recommendations = []
        
        if not self.metrics:
            return ["No data available for optimization analysis"]
        
        # Analyze token efficiency
        efficiencies = [m.token_efficiency for m in self.metrics if m.token_efficiency]
        if efficiencies:
            avg_efficiency = sum(efficiencies) / len(efficiencies)
            if avg_efficiency < 0.6:
                recommendations.append("Implement context compression and prompt optimization strategies")
            elif avg_efficiency < 0.8:
                recommendations.append("Review prompt engineering for better token efficiency")
        
        # Analyze execution times
        durations = [m.duration_seconds for m in self.metrics if m.duration_seconds]
        if durations:
            avg_duration = sum(durations) / len(durations)
            if avg_duration > 300:  # 5 minutes
                recommendations.append("Consider task decomposition and parallel execution")
            elif avg_duration > 120:  # 2 minutes
                recommendations.append("Optimize agent selection and task complexity")
        
        # Analyze failure patterns
        failed_metrics = [m for m in self.metrics if not m.success]
        if len(failed_metrics) > len(self.metrics) * 0.1:  # >10% failure rate
            recommendations.append("Improve error handling and input validation")
        
        # Agent-specific recommendations
        agent_performance = {}
        for m in self.metrics:
            if m.agent_type not in agent_performance:
                agent_performance[m.agent_type] = []
            agent_performance[m.agent_type].append(m)
        
        for agent_type, metrics_list in agent_performance.items():
            avg_efficiency = sum(m.token_efficiency for m in metrics_list if m.token_efficiency) / len(metrics_list)
            if avg_efficiency < 0.5:
                recommendations.append(f"Optimize {agent_type} agent prompts and context management")
        
        return recommendations[:10]  # Top 10 recommendations
    
    def _analyze_token_usage(self) -> Dict[str, Any]:
        """Analyze token usage patterns"""
        
        if not self.metrics:
            return {"status": "no_data"}
        
        # Calculate token statistics
        estimated_tokens = [m.estimated_tokens for m in self.metrics if m.estimated_tokens]
        actual_tokens = [m.actual_tokens for m in self.metrics if m.actual_tokens]
        
        analysis = {
            "total_estimated": sum(estimated_tokens) if estimated_tokens else 0,
            "total_actual": sum(actual_tokens) if actual_tokens else 0,
            "average_estimated": sum(estimated_tokens) / len(estimated_tokens) if estimated_tokens else 0,
            "average_actual": sum(actual_tokens) / len(actual_tokens) if actual_tokens else 0,
            "estimation_accuracy": 0.0,
            "token_efficiency_distribution": {},
            "high_usage_tasks": []
        }
        
        # Calculate estimation accuracy
        if estimated_tokens and actual_tokens and len(estimated_tokens) == len(actual_tokens):
            accuracy_scores = [min(est/act, act/est) for est, act in zip(estimated_tokens, actual_tokens) if act > 0]
            analysis["estimation_accuracy"] = sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0.0
        
        # Efficiency distribution
        efficiencies = [m.token_efficiency for m in self.metrics if m.token_efficiency]
        if efficiencies:
            ranges = [(0, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]
            for min_eff, max_eff in ranges:
                count = len([e for e in efficiencies if min_eff <= e < max_eff])
                analysis["token_efficiency_distribution"][f"{min_eff}-{max_eff}"] = count
        
        # High usage tasks
        if actual_tokens:
            high_threshold = sum(actual_tokens) / len(actual_tokens) * 1.5  # 150% of average
            for m in self.metrics:
                if m.actual_tokens and m.actual_tokens > high_threshold:
                    analysis["high_usage_tasks"].append({
                        "agent": m.agent_type,
                        "task": m.task_description[:50] + "..." if len(m.task_description) > 50 else m.task_description,
                        "tokens": m.actual_tokens
                    })
        
        return analysis
    
    def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        
        if len(self.metrics) < 3:
            return {"status": "insufficient_data", "message": "Need at least 3 tasks for trend analysis"}
        
        # Sort by start time
        sorted_metrics = sorted(self.metrics, key=lambda m: m.start_time)
        
        # Calculate rolling averages
        window_size = min(3, len(sorted_metrics))
        rolling_efficiency = []
        rolling_duration = []
        
        for i in range(window_size - 1, len(sorted_metrics)):
            window = sorted_metrics[i-window_size+1:i+1]
            
            # Efficiency trend
            effs = [m.token_efficiency for m in window if m.token_efficiency]
            if effs:
                rolling_efficiency.append(sum(effs) / len(effs))
            
            # Duration trend
            durs = [m.duration_seconds for m in window if m.duration_seconds]
            if durs:
                rolling_duration.append(sum(durs) / len(durs))
        
        trends = {
            "efficiency_trend": "stable",
            "duration_trend": "stable",
            "overall_improvement": False
        }
        
        # Analyze efficiency trend
        if len(rolling_efficiency) >= 2:
            if rolling_efficiency[-1] > rolling_efficiency[0] * 1.1:
                trends["efficiency_trend"] = "improving"
            elif rolling_efficiency[-1] < rolling_efficiency[0] * 0.9:
                trends["efficiency_trend"] = "declining"
        
        # Analyze duration trend
        if len(rolling_duration) >= 2:
            if rolling_duration[-1] < rolling_duration[0] * 0.9:  # Faster is better
                trends["duration_trend"] = "improving"
            elif rolling_duration[-1] > rolling_duration[0] * 1.1:
                trends["duration_trend"] = "declining"
        
        # Overall improvement
        trends["overall_improvement"] = (
            trends["efficiency_trend"] == "improving" or 
            trends["duration_trend"] == "improving"
        )
        
        return trends
    
    def save_performance_report(self, filename: str = None) -> str:
        """Save performance report to file"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{self.session_id}_{timestamp}.json"
        
        report_path = os.path.join(os.getcwd(), ".session", "performance", filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        # Generate and save report
        report = self.generate_performance_report()
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📊 Performance report saved: {report_path}")
        return report_path


class PerformanceTracker:
    """Helper class for tracking individual task performance"""
    
    def __init__(self, monitor: PerformanceMonitor, task_id: str, metrics: PerformanceMetrics):
        self.monitor = monitor
        self.task_id = task_id
        self.metrics = metrics
    
    def log_success(self, actual_tokens: int = None, additional_data: Dict = None):
        """Log successful task completion"""
        self.metrics.end_time = datetime.now().isoformat()
        self.metrics.actual_tokens = actual_tokens
        self.metrics.success = True
        
        if additional_data:
            # Store additional performance data
            pass
    
    def log_failure(self, error_message: str):
        """Log task failure"""
        self.metrics.end_time = datetime.now().isoformat()
        self.metrics.success = False
        self.metrics.error_message = error_message
    
    def update_token_estimate(self, new_estimate: int):
        """Update token estimate during execution"""
        self.metrics.estimated_tokens = new_estimate


# Convenience functions for easy integration
def track_agent_performance(agent_type: str, task_description: str, monitor: PerformanceMonitor = None):
    """Decorator for tracking agent performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            perf_monitor = monitor or PerformanceMonitor()
            
            with perf_monitor.track_performance(agent_type, task_description) as tracker:
                try:
                    result = func(*args, **kwargs)
                    # Estimate tokens from result if available
                    estimated_tokens = len(str(result)) * 0.75 if result else 1000
                    tracker.log_success(actual_tokens=int(estimated_tokens))
                    return result
                except Exception as e:
                    tracker.log_failure(str(e))
                    raise
        return wrapper
    return decorator

# Example usage
if __name__ == "__main__":
    # Create performance monitor
    monitor = PerformanceMonitor("test_session")
    
    # Example: Track a task
    with monitor.track_performance("orchestrator", "project analysis", 5000) as tracker:
        time.sleep(2)  # Simulate work
        tracker.log_success(actual_tokens=4200)
    
    # Generate report
    report = monitor.generate_performance_report()
    print("Performance Report Generated!")
    print(f"Grade: {report['session_summary'].performance_grade}")
    print(f"Efficiency: {report['session_summary'].average_efficiency:.1%}")
    
    # Save report
    monitor.save_performance_report()