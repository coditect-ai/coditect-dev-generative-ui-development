#!/usr/bin/env python3
"""
Smart Task Executor with Work Reuse Integration

Automatically checks for reusable work before executing new tasks to minimize
token usage and avoid reinventing the wheel.
"""

import json
from typing import Dict, List, Optional
from work_reuse_optimizer import WorkReuseOptimizer, ReuseRecommendation

class SmartTaskExecutor:
    """Intelligent task executor that leverages previous work"""
    
    def __init__(self):
        self.optimizer = WorkReuseOptimizer()
        self.execution_log = []
        
    def execute_with_reuse_check(self, task_description: str, requirements: Dict, 
                                force_new: bool = False) -> Dict:
        """Execute task with automatic reuse checking"""
        
        print(f"🎯 Task: {task_description}")
        print("="*60)
        
        execution_plan = {
            "task": task_description,
            "requirements": requirements,
            "reuse_analysis": {},
            "execution_strategy": "",
            "token_budget": {},
            "recommendations": []
        }
        
        if not force_new:
            # Step 1: Analyze reuse opportunities
            print("🔍 Checking for reusable work...")
            recommendations = self.optimizer.recommend_reuse(task_description, requirements)
            
            if recommendations:
                execution_plan["reuse_analysis"] = self._analyze_reuse_value(recommendations)
                
                if execution_plan["reuse_analysis"]["recommended_strategy"] == "REUSE_HEAVY":
                    execution_plan["execution_strategy"] = "reuse_and_adapt"
                    execution_plan["recommendations"] = self._create_reuse_plan(recommendations)
                    
                    print(f"✅ HIGH REUSE OPPORTUNITY DETECTED!")
                    print(f"   Token Savings: {execution_plan['reuse_analysis']['total_savings']:,}")
                    print(f"   ROI: {execution_plan['reuse_analysis']['roi']:.1f}x")
                    print(f"   Strategy: Adapt {len(recommendations)} existing assets")
                    
                elif execution_plan["reuse_analysis"]["recommended_strategy"] == "REUSE_PARTIAL":
                    execution_plan["execution_strategy"] = "hybrid_approach"
                    execution_plan["recommendations"] = self._create_hybrid_plan(recommendations)
                    
                    print(f"💡 PARTIAL REUSE OPPORTUNITY")
                    print(f"   Token Savings: {execution_plan['reuse_analysis']['total_savings']:,}")
                    print(f"   Strategy: Reuse templates + generate new content")
                    
                else:
                    execution_plan["execution_strategy"] = "fresh_development"
                    print("📝 FRESH DEVELOPMENT RECOMMENDED")
                    print("   No significant reuse opportunities found")
            else:
                execution_plan["execution_strategy"] = "fresh_development"
                print("📝 No reusable assets found - proceeding with fresh development")
        else:
            execution_plan["execution_strategy"] = "fresh_development"
            print("🔨 FORCED FRESH DEVELOPMENT (force_new=True)")
        
        # Step 2: Calculate token budget
        execution_plan["token_budget"] = self._calculate_token_budget(
            task_description, requirements, execution_plan["execution_strategy"],
            execution_plan.get("reuse_analysis", {})
        )
        
        print(f"\n💰 TOKEN BUDGET:")
        print(f"   Estimated Need: {execution_plan['token_budget']['estimated_need']:,}")
        print(f"   With Reuse: {execution_plan['token_budget']['with_reuse']:,}")
        print(f"   Savings: {execution_plan['token_budget']['savings']:,}")
        
        # Step 3: Generate execution instructions
        execution_instructions = self._generate_execution_instructions(execution_plan)
        execution_plan["instructions"] = execution_instructions
        
        print(f"\n🚀 EXECUTION STRATEGY: {execution_plan['execution_strategy'].upper()}")
        print("\n📋 NEXT STEPS:")
        for i, instruction in enumerate(execution_instructions, 1):
            print(f"   {i}. {instruction}")
        
        # Log execution plan
        self.execution_log.append(execution_plan)
        self._save_execution_log()
        
        return execution_plan
    
    def _analyze_reuse_value(self, recommendations: List[ReuseRecommendation]) -> Dict:
        """Analyze the value of reuse recommendations"""
        
        total_savings = sum(rec.token_savings for rec in recommendations)
        total_confidence = sum(rec.confidence for rec in recommendations) / len(recommendations)
        high_confidence_count = sum(1 for rec in recommendations if rec.confidence > 0.7)
        
        # Decision logic
        if total_savings > 100000 and total_confidence > 0.6:
            strategy = "REUSE_HEAVY"
        elif total_savings > 50000 or high_confidence_count >= 3:
            strategy = "REUSE_PARTIAL"
        else:
            strategy = "FRESH_DEVELOPMENT"
        
        # Calculate ROI
        implementation_cost = len(recommendations) * 2000  # Estimated adaptation cost
        roi = total_savings / implementation_cost if implementation_cost > 0 else 0
        
        return {
            "recommended_strategy": strategy,
            "total_savings": total_savings,
            "average_confidence": total_confidence,
            "high_confidence_assets": high_confidence_count,
            "roi": roi,
            "implementation_effort": self._estimate_implementation_effort(recommendations)
        }
    
    def _create_reuse_plan(self, recommendations: List[ReuseRecommendation]) -> List[Dict]:
        """Create detailed reuse implementation plan"""
        
        plan = []
        for rec in recommendations:
            plan.append({
                "action": "adapt_existing_asset",
                "asset_type": rec.asset.asset_type,
                "source_file": rec.asset.file_path,
                "adaptation_strategy": rec.adaptation_strategy,
                "token_savings": rec.token_savings,
                "confidence": rec.confidence,
                "effort": rec.effort_estimate,
                "instructions": [
                    f"Copy {rec.asset.file_path} as template",
                    rec.adaptation_strategy,
                    "Update metadata and cross-references",
                    "Validate adapted content meets requirements"
                ]
            })
        
        return plan
    
    def _create_hybrid_plan(self, recommendations: List[ReuseRecommendation]) -> List[Dict]:
        """Create hybrid development plan (reuse + new development)"""
        
        plan = []
        
        # Use high-confidence recommendations
        high_confidence = [rec for rec in recommendations if rec.confidence > 0.7]
        for rec in high_confidence:
            plan.append({
                "action": "adapt_existing_asset",
                "asset_type": rec.asset.asset_type,
                "source_file": rec.asset.file_path,
                "adaptation_strategy": rec.adaptation_strategy,
                "token_savings": rec.token_savings,
                "confidence": rec.confidence
            })
        
        # Add fresh development for gaps
        plan.append({
            "action": "develop_new_content",
            "scope": "Fill gaps not covered by reused assets",
            "estimated_tokens": 25000,  # Conservative estimate for new work
            "focus": "Novel content and specialized assessments"
        })
        
        return plan
    
    def _calculate_token_budget(self, task_description: str, requirements: Dict, 
                               strategy: str, reuse_analysis: Dict) -> Dict:
        """Calculate realistic token budget based on strategy"""
        
        # Base estimation
        base_estimate = self.optimizer._estimate_task_tokens(task_description, requirements)
        
        if strategy == "reuse_and_adapt":
            # Heavy reuse - significant savings
            high_confidence_count = reuse_analysis.get("high_confidence_assets", 0)
            adaptation_cost = high_confidence_count * 3000
            with_reuse = adaptation_cost
            savings = base_estimate - with_reuse
            
        elif strategy == "hybrid_approach":
            # Partial reuse - moderate savings
            total_reuse_savings = reuse_analysis.get("total_savings", 0)
            with_reuse = base_estimate - int(total_reuse_savings * 0.6)  # Conservative
            savings = base_estimate - with_reuse
            
        else:
            # Fresh development - no savings
            with_reuse = base_estimate
            savings = 0
        
        return {
            "estimated_need": base_estimate,
            "with_reuse": with_reuse,
            "savings": savings,
            "efficiency_gain": (savings / base_estimate * 100) if base_estimate > 0 else 0
        }
    
    def _generate_execution_instructions(self, plan: Dict) -> List[str]:
        """Generate step-by-step execution instructions"""
        
        strategy = plan["execution_strategy"]
        
        if strategy == "reuse_and_adapt":
            return [
                "Use work_reuse_optimizer to identify adaptation targets",
                "Copy highest-value existing assets to new locations",
                "Adapt content structure and topic-specific information",
                "Update metadata for new subject domain",
                "Validate adapted content meets quality standards",
                "Integrate adapted assets into cohesive curriculum"
            ]
            
        elif strategy == "hybrid_approach":
            return [
                "Reuse high-confidence existing assets as foundation",
                "Adapt reusable templates and frameworks",
                "Generate new content for gaps and specialized needs",
                "Ensure consistency between reused and new content",
                "Integrate all components into unified structure",
                "Conduct comprehensive quality validation"
            ]
            
        else:  # fresh_development
            return [
                "Proceed with complete fresh development using agents",
                "Follow standard curriculum development process",
                "Generate all content and assessments from scratch",
                "Apply NotebookLM optimization throughout",
                "Conduct full quality assurance process"
            ]
    
    def _estimate_implementation_effort(self, recommendations: List[ReuseRecommendation]) -> str:
        """Estimate total implementation effort"""
        
        effort_weights = {"low": 1, "medium": 3, "high": 5}
        total_effort = sum(effort_weights.get(rec.effort_estimate, 3) for rec in recommendations)
        
        if total_effort <= 5:
            return "minimal"
        elif total_effort <= 15:
            return "moderate"
        else:
            return "substantial"
    
    def _save_execution_log(self):
        """Save execution log for analysis and improvement"""
        
        log_file = "/home/halcasteel/AI-SYLLUBUS/scripts/core/smart_execution_log.json"
        
        try:
            with open(log_file, 'w') as f:
                json.dump(self.execution_log, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save execution log: {e}")
    
    def get_efficiency_report(self) -> Dict:
        """Generate efficiency report from execution history"""
        
        total_tasks = len(self.execution_log)
        if total_tasks == 0:
            return {"message": "No execution history available"}
        
        reuse_tasks = sum(1 for log in self.execution_log 
                         if log["execution_strategy"] != "fresh_development")
        
        total_savings = sum(log["token_budget"].get("savings", 0) 
                           for log in self.execution_log)
        
        avg_efficiency = sum(log["token_budget"].get("efficiency_gain", 0) 
                            for log in self.execution_log) / total_tasks
        
        return {
            "total_tasks_analyzed": total_tasks,
            "reuse_strategy_used": reuse_tasks,
            "reuse_adoption_rate": (reuse_tasks / total_tasks * 100),
            "total_tokens_saved": total_savings,
            "average_efficiency_gain": avg_efficiency,
            "recommendation": self._generate_efficiency_recommendation(avg_efficiency)
        }
    
    def _generate_efficiency_recommendation(self, avg_efficiency: float) -> str:
        """Generate recommendation based on efficiency metrics"""
        
        if avg_efficiency > 50:
            return "Excellent reuse strategy - continue current approach"
        elif avg_efficiency > 25:
            return "Good reuse adoption - consider expanding asset library"
        elif avg_efficiency > 10:
            return "Moderate reuse - focus on creating more reusable templates"
        else:
            return "Low reuse efficiency - review asset creation and categorization"

def main():
    """Example usage of smart task executor"""
    
    print("🧠 SMART TASK EXECUTOR WITH WORK REUSE")
    print("="*60)
    
    executor = SmartTaskExecutor()
    
    # Example task execution
    task_description = "Create comprehensive Module 2 Machine Learning content with assessments across all skill levels"
    requirements = {
        "modules": ["module2_machine_learning"],
        "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
        "deliverables": ["content", "assessments", "notebooklm_optimization"]
    }
    
    # Execute with reuse analysis
    execution_plan = executor.execute_with_reuse_check(task_description, requirements)
    
    print(f"\n📊 EXECUTION PLAN SUMMARY:")
    print(f"   Strategy: {execution_plan['execution_strategy']}")
    print(f"   Token Budget: {execution_plan['token_budget']['with_reuse']:,}")
    print(f"   Efficiency Gain: {execution_plan['token_budget']['efficiency_gain']:.1f}%")
    
    # Generate efficiency report
    print(f"\n📈 EFFICIENCY REPORT:")
    report = executor.get_efficiency_report()
    for key, value in report.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.1f}")
        else:
            print(f"   {key}: {value}")

if __name__ == "__main__":
    main()