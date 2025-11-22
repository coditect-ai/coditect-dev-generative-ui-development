#!/usr/bin/env python3
"""
Work Reuse & Token Optimization System

Intelligently leverages previously created work to minimize token usage and avoid
reinventing the wheel. Scans existing content, scripts, and patterns for reuse.
"""

import json
import yaml
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import hashlib

@dataclass
class ReusableAsset:
    """Represents a reusable work asset"""
    asset_id: str
    asset_type: str  # content, script, template, pattern, framework
    file_path: str
    description: str
    tokens_saved: int
    reuse_count: int
    compatibility_score: float
    adaptation_effort: str  # low, medium, high
    last_used: str

@dataclass
class ReuseRecommendation:
    """Recommendation for reusing existing work"""
    asset: ReusableAsset
    adaptation_strategy: str
    token_savings: int
    effort_estimate: str
    confidence: float

class WorkReuseOptimizer:
    """Intelligently identifies and recommends reusable work assets"""
    
    def __init__(self, project_root: str = "/home/halcasteel/AI-SYLLUBUS"):
        self.project_root = Path(project_root)
        self.asset_registry = {}
        self.reuse_history = {}
        self.token_savings_log = []
        
        # Load existing asset registry
        self._load_asset_registry()
        
    def scan_existing_work(self) -> Dict[str, List[ReusableAsset]]:
        """Scan project for reusable assets"""
        
        assets = {
            "content": [],
            "scripts": [],
            "templates": [],
            "frameworks": [],
            "patterns": []
        }
        
        # Scan content files
        content_patterns = ["**/*.md", "**/*.yaml", "**/*.json"]
        for pattern in content_patterns:
            for file_path in self.project_root.glob(pattern):
                if self._is_valuable_content(file_path):
                    asset = self._analyze_content_asset(file_path)
                    if asset:
                        assets["content"].append(asset)
        
        # Scan executable scripts
        for file_path in self.project_root.glob("**/*.py"):
            if self._is_reusable_script(file_path):
                asset = self._analyze_script_asset(file_path)
                if asset:
                    assets["scripts"].append(asset)
        
        # Scan templates and frameworks
        template_dirs = ["templates", "notebooklm_templates", "assessment_frameworks"]
        for template_dir in template_dirs:
            template_path = self.project_root / template_dir
            if template_path.exists():
                for file_path in template_path.rglob("*"):
                    if file_path.is_file():
                        asset = self._analyze_template_asset(file_path)
                        if asset:
                            assets["templates"].append(asset)
        
        self._update_asset_registry(assets)
        return assets
    
    def recommend_reuse(self, task_description: str, requirements: Dict) -> List[ReuseRecommendation]:
        """Recommend existing work for reuse based on task requirements"""
        
        recommendations = []
        
        # Analyze task requirements
        task_tokens = self._estimate_task_tokens(task_description, requirements)
        task_keywords = self._extract_keywords(task_description)
        
        # Find compatible assets
        for asset_type, assets in self.asset_registry.items():
            for asset in assets:
                compatibility = self._calculate_compatibility(task_keywords, asset)
                
                if compatibility > 0.3:  # 30% compatibility threshold
                    adaptation_strategy = self._determine_adaptation_strategy(task_description, asset)
                    token_savings = int(task_tokens * compatibility * 0.8)  # Conservative estimate
                    
                    recommendation = ReuseRecommendation(
                        asset=asset,
                        adaptation_strategy=adaptation_strategy,
                        token_savings=token_savings,
                        effort_estimate=asset.adaptation_effort,
                        confidence=compatibility
                    )
                    recommendations.append(recommendation)
        
        # Sort by token savings potential
        recommendations.sort(key=lambda x: x.token_savings, reverse=True)
        return recommendations[:5]  # Top 5 recommendations
    
    def generate_reuse_plan(self, recommendations: List[ReuseRecommendation]) -> Dict:
        """Generate comprehensive reuse plan with implementation steps"""
        
        total_token_savings = sum(rec.token_savings for rec in recommendations)
        
        plan = {
            "reuse_summary": {
                "total_assets": len(recommendations),
                "estimated_token_savings": total_token_savings,
                "implementation_effort": self._calculate_total_effort(recommendations),
                "roi_score": self._calculate_roi(recommendations)
            },
            "implementation_steps": [],
            "asset_adaptations": [],
            "validation_checkpoints": []
        }
        
        for i, rec in enumerate(recommendations, 1):
            plan["implementation_steps"].append({
                "step": i,
                "action": f"Adapt {rec.asset.asset_type}: {rec.asset.description}",
                "strategy": rec.adaptation_strategy,
                "token_savings": rec.token_savings,
                "effort": rec.effort_estimate,
                "file_path": rec.asset.file_path
            })
            
            plan["asset_adaptations"].append({
                "asset_id": rec.asset.asset_id,
                "adaptation_instructions": self._generate_adaptation_instructions(rec),
                "validation_criteria": self._generate_validation_criteria(rec)
            })
        
        # Add validation checkpoints
        plan["validation_checkpoints"] = [
            "Verify adapted content meets new requirements",
            "Confirm token usage reduction achieved",
            "Validate quality standards maintained",
            "Test integration with existing framework"
        ]
        
        return plan
    
    def _analyze_content_asset(self, file_path: Path) -> Optional[ReusableAsset]:
        """Analyze content file for reusability"""
        
        try:
            content = file_path.read_text()
            
            # Calculate content metrics
            word_count = len(content.split())
            estimated_tokens = word_count * 1.3  # Rough token estimation
            
            # Determine asset type and reusability
            if "beginner" in str(file_path) or "intermediate" in str(file_path):
                asset_type = "multi_level_content"
                compatibility_score = 0.8
            elif "assessment" in str(file_path) or "quiz" in str(file_path):
                asset_type = "assessment_framework"
                compatibility_score = 0.7
            elif "notebooklm" in str(file_path).lower():
                asset_type = "notebooklm_optimization"
                compatibility_score = 0.9
            else:
                asset_type = "general_content"
                compatibility_score = 0.5
            
            return ReusableAsset(
                asset_id=self._generate_asset_id(file_path),
                asset_type=asset_type,
                file_path=str(file_path),
                description=f"{asset_type} from {file_path.name}",
                tokens_saved=int(estimated_tokens * 0.7),
                reuse_count=0,
                compatibility_score=compatibility_score,
                adaptation_effort="low" if compatibility_score > 0.7 else "medium",
                last_used="never"
            )
            
        except Exception as e:
            return None
    
    def _analyze_script_asset(self, file_path: Path) -> Optional[ReusableAsset]:
        """Analyze Python script for reusability"""
        
        try:
            content = file_path.read_text()
            
            # Identify script type
            if "execute_TASK_" in str(file_path):
                asset_type = "task_execution_template"
                compatibility_score = 0.9
                adaptation_effort = "low"
            elif "agent_dispatcher" in str(file_path):
                asset_type = "agent_coordination_framework"
                compatibility_score = 0.8
                adaptation_effort = "medium"
            elif "project_manager" in str(file_path):
                asset_type = "project_management_system"
                compatibility_score = 0.7
                adaptation_effort = "medium"
            else:
                asset_type = "utility_script"
                compatibility_score = 0.5
                adaptation_effort = "high"
            
            # Estimate token savings
            lines = len(content.split('\n'))
            estimated_tokens = lines * 15  # Rough estimation for code
            
            return ReusableAsset(
                asset_id=self._generate_asset_id(file_path),
                asset_type=asset_type,
                file_path=str(file_path),
                description=f"{asset_type} - {file_path.stem}",
                tokens_saved=int(estimated_tokens * 0.8),
                reuse_count=0,
                compatibility_score=compatibility_score,
                adaptation_effort=adaptation_effort,
                last_used="never"
            )
            
        except Exception as e:
            return None
    
    def _analyze_template_asset(self, file_path: Path) -> Optional[ReusableAsset]:
        """Analyze template file for reusability"""
        
        try:
            content = file_path.read_text()
            word_count = len(content.split())
            estimated_tokens = word_count * 1.2
            
            return ReusableAsset(
                asset_id=self._generate_asset_id(file_path),
                asset_type="template",
                file_path=str(file_path),
                description=f"Template: {file_path.name}",
                tokens_saved=int(estimated_tokens * 0.6),
                reuse_count=0,
                compatibility_score=0.6,
                adaptation_effort="low",
                last_used="never"
            )
            
        except Exception as e:
            return None
    
    def _generate_asset_id(self, file_path: Path) -> str:
        """Generate unique asset ID"""
        return hashlib.md5(str(file_path).encode()).hexdigest()[:8]
    
    def _calculate_compatibility(self, task_keywords: List[str], asset: ReusableAsset) -> float:
        """Calculate compatibility score between task and asset"""
        
        asset_keywords = self._extract_keywords(asset.description + " " + asset.file_path)
        
        if not task_keywords or not asset_keywords:
            return 0.0
        
        # Simple keyword overlap calculation
        overlap = len(set(task_keywords) & set(asset_keywords))
        total_unique = len(set(task_keywords) | set(asset_keywords))
        
        base_compatibility = overlap / total_unique if total_unique > 0 else 0.0
        
        # Boost compatibility for high-value asset types
        if asset.asset_type in ["task_execution_template", "notebooklm_optimization", "multi_level_content"]:
            base_compatibility *= 1.2
        
        return min(base_compatibility, 1.0)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        
        # Common curriculum development keywords
        keywords = []
        important_terms = [
            "content", "assessment", "beginner", "intermediate", "advanced", "expert",
            "notebooklm", "quiz", "project", "curriculum", "module", "task", 
            "agent", "automation", "template", "framework", "optimization"
        ]
        
        text_lower = text.lower()
        for term in important_terms:
            if term in text_lower:
                keywords.append(term)
        
        return keywords
    
    def _estimate_task_tokens(self, task_description: str, requirements: Dict) -> int:
        """Estimate tokens needed for new task"""
        
        # Base estimation from task complexity
        base_tokens = 10000  # Default baseline
        
        # Adjust for scope
        if "modules" in requirements:
            base_tokens += len(requirements["modules"]) * 5000
        
        if "skill_levels" in requirements:
            base_tokens += len(requirements["skill_levels"]) * 3000
        
        # Adjust for task complexity keywords
        complexity_keywords = {
            "comprehensive": 2.0,
            "complete": 1.8,
            "detailed": 1.5,
            "advanced": 1.4,
            "expert": 1.6,
            "basic": 0.8,
            "simple": 0.6
        }
        
        multiplier = 1.0
        for keyword, mult in complexity_keywords.items():
            if keyword in task_description.lower():
                multiplier = max(multiplier, mult)
        
        return int(base_tokens * multiplier)
    
    def _determine_adaptation_strategy(self, task_description: str, asset: ReusableAsset) -> str:
        """Determine how to adapt existing asset for new task"""
        
        strategies = {
            "task_execution_template": "Copy script and update task parameters, agent assignments, and deliverables",
            "multi_level_content": "Adapt content structure and replace topic-specific information",
            "assessment_framework": "Modify question types and scoring criteria for new subject matter",
            "notebooklm_optimization": "Update metadata tags and cross-references for new content domain",
            "agent_coordination_framework": "Reconfigure agent assignments and workflow parameters"
        }
        
        return strategies.get(asset.asset_type, "Review and adapt core patterns to new requirements")
    
    def _generate_adaptation_instructions(self, recommendation: ReuseRecommendation) -> List[str]:
        """Generate specific adaptation instructions"""
        
        instructions = [
            f"1. Copy {recommendation.asset.file_path} to new location",
            f"2. {recommendation.adaptation_strategy}",
            "3. Update file headers and metadata",
            "4. Test adapted version with sample inputs",
            "5. Validate outputs meet new requirements"
        ]
        
        return instructions
    
    def _generate_validation_criteria(self, recommendation: ReuseRecommendation) -> List[str]:
        """Generate validation criteria for adapted work"""
        
        criteria = [
            "Adapted work functions correctly in new context",
            f"Token savings of {recommendation.token_savings} achieved",
            "Quality standards maintained or improved",
            "Integration successful with existing framework",
            "No functionality regression introduced"
        ]
        
        return criteria
    
    def _calculate_total_effort(self, recommendations: List[ReuseRecommendation]) -> str:
        """Calculate total implementation effort"""
        
        effort_scores = {"low": 1, "medium": 3, "high": 5}
        total_score = sum(effort_scores.get(rec.effort_estimate, 3) for rec in recommendations)
        
        if total_score <= 5:
            return "low"
        elif total_score <= 15:
            return "medium"
        else:
            return "high"
    
    def _calculate_roi(self, recommendations: List[ReuseRecommendation]) -> float:
        """Calculate return on investment for reuse strategy"""
        
        total_savings = sum(rec.token_savings for rec in recommendations)
        effort_cost = len(recommendations) * 1000  # Estimated effort cost in tokens
        
        if effort_cost == 0:
            return float('inf')
        
        return total_savings / effort_cost
    
    def _is_valuable_content(self, file_path: Path) -> bool:
        """Determine if content file has reuse value"""
        
        # Skip system files and temporary files
        if file_path.name.startswith('.') or file_path.suffix in ['.tmp', '.log']:
            return False
        
        # Look for substantial content files
        try:
            content = file_path.read_text()
            return len(content) > 500  # Minimum content threshold
        except:
            return False
    
    def _is_reusable_script(self, file_path: Path) -> bool:
        """Determine if script has reuse value"""
        
        # Look for substantial scripts with reusable patterns
        try:
            content = file_path.read_text()
            
            # Check for reusable patterns
            reusable_indicators = [
                "class ", "def ", "Task(", "subagent_type",
                "curriculum", "assessment", "agent", "template"
            ]
            
            return any(indicator in content for indicator in reusable_indicators)
        except:
            return False
    
    def _load_asset_registry(self):
        """Load existing asset registry"""
        registry_file = self.project_root / "scripts" / "core" / "asset_registry.json"
        
        if registry_file.exists():
            try:
                with open(registry_file, 'r') as f:
                    data = json.load(f)
                    # Convert dict data back to ReusableAsset objects
                    for asset_type, assets in data.items():
                        self.asset_registry[asset_type] = [
                            ReusableAsset(**asset_data) for asset_data in assets
                        ]
            except Exception as e:
                print(f"Warning: Could not load asset registry: {e}")
                self.asset_registry = {}
        else:
            self.asset_registry = {}
    
    def _update_asset_registry(self, assets: Dict):
        """Update and save asset registry"""
        self.asset_registry.update(assets)
        
        # Save to file
        registry_file = self.project_root / "scripts" / "core" / "asset_registry.json"
        registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert ReusableAsset objects to dicts for JSON serialization
        serializable_data = {}
        for asset_type, assets in self.asset_registry.items():
            serializable_data[asset_type] = [
                {
                    "asset_id": asset.asset_id,
                    "asset_type": asset.asset_type,
                    "file_path": asset.file_path,
                    "description": asset.description,
                    "tokens_saved": asset.tokens_saved,
                    "reuse_count": asset.reuse_count,
                    "compatibility_score": asset.compatibility_score,
                    "adaptation_effort": asset.adaptation_effort,
                    "last_used": asset.last_used
                } for asset in assets
            ]
        
        try:
            with open(registry_file, 'w') as f:
                json.dump(serializable_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save asset registry: {e}")
    
    def track_reuse_success(self, asset_id: str, actual_token_savings: int):
        """Track successful reuse for future recommendations"""
        
        # Update asset reuse count and accuracy
        for asset_type, assets in self.asset_registry.items():
            for asset in assets:
                if asset.asset_id == asset_id:
                    asset.reuse_count += 1
                    asset.last_used = "2025-11-09"
                    
                    # Log savings for accuracy improvement
                    self.token_savings_log.append({
                        "asset_id": asset_id,
                        "predicted_savings": asset.tokens_saved,
                        "actual_savings": actual_token_savings,
                        "accuracy": actual_token_savings / asset.tokens_saved if asset.tokens_saved > 0 else 0
                    })
                    
                    break
        
        # Update registry
        self._update_asset_registry(self.asset_registry)

def main():
    """Example usage of work reuse optimizer"""
    
    print("🔄 WORK REUSE & TOKEN OPTIMIZATION SYSTEM")
    print("="*60)
    
    # Initialize optimizer
    optimizer = WorkReuseOptimizer()
    
    # Scan existing work
    print("📊 Scanning existing work assets...")
    assets = optimizer.scan_existing_work()
    
    total_assets = sum(len(asset_list) for asset_list in assets.values())
    print(f"✅ Found {total_assets} reusable assets:")
    
    for asset_type, asset_list in assets.items():
        if asset_list:
            print(f"   {asset_type}: {len(asset_list)} assets")
    
    # Example task for reuse recommendations
    task_description = "Create comprehensive Module 2 Machine Learning content with assessments across all skill levels"
    requirements = {
        "modules": ["module2_machine_learning"],
        "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
        "deliverables": ["content", "assessments", "notebooklm_optimization"]
    }
    
    print(f"\n🎯 Task: {task_description}")
    print("🔍 Analyzing reuse opportunities...")
    
    # Get recommendations
    recommendations = optimizer.recommend_reuse(task_description, requirements)
    
    if recommendations:
        print(f"\n💡 Found {len(recommendations)} reuse opportunities:")
        
        total_savings = 0
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec.asset.description}")
            print(f"   Token Savings: {rec.token_savings:,}")
            print(f"   Confidence: {rec.confidence:.1%}")
            print(f"   Effort: {rec.effort_estimate}")
            print(f"   Strategy: {rec.adaptation_strategy}")
            total_savings += rec.token_savings
        
        print(f"\n🎊 Total Estimated Token Savings: {total_savings:,}")
        
        # Generate reuse plan
        print("\n📋 Generating comprehensive reuse plan...")
        reuse_plan = optimizer.generate_reuse_plan(recommendations)
        
        print(f"✅ Plan Summary:")
        print(f"   Assets to Reuse: {reuse_plan['reuse_summary']['total_assets']}")
        print(f"   Token Savings: {reuse_plan['reuse_summary']['estimated_token_savings']:,}")
        print(f"   Implementation Effort: {reuse_plan['reuse_summary']['implementation_effort']}")
        print(f"   ROI Score: {reuse_plan['reuse_summary']['roi_score']:.1f}x")
        
    else:
        print("\n📝 No significant reuse opportunities found - proceeding with fresh development")
    
    print(f"\n🚀 Work Reuse Optimization Complete!")

if __name__ == "__main__":
    main()