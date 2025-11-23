#!/usr/bin/env python3
"""
Workflow Analyzer - Intelligent Agent/Skills/Commands Selection
Analyzes problems and use cases to determine optimal agent coordination strategy.
"""

import re
import json
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum

@dataclass
class WorkflowRequirement:
    """Represents a workflow requirement with context"""
    category: str
    description: str
    complexity: str  # simple, moderate, complex
    priority: str    # low, medium, high, critical
    estimated_effort: str  # time estimate
    dependencies: List[str]  # other requirements this depends on

@dataclass
class AgentRecommendation:
    """Recommendation for which agent to use"""
    agent_type: str
    confidence: float  # 0.0 - 1.0
    reasoning: str
    skills_needed: List[str]
    commands_suggested: List[str]
    coordination_role: str  # primary, supporting, validator

class WorkflowAnalyzer:
    """Intelligent workflow analysis and agent selection"""
    
    def __init__(self):
        self.load_agent_capabilities()
        self.load_skills_commands_mapping()
    
    def load_agent_capabilities(self):
        """Load agent capability mappings from 47-agent framework"""
        self.agent_capabilities = {
            "orchestrator": {
                "primary_roles": ["coordination", "planning", "project_management"],
                "keywords": ["plan", "coordinate", "manage", "workflow", "multiple", "complex"],
                "complexity_range": ["moderate", "complex"],
                "best_for": ["multi-agent workflows", "project planning", "resource coordination"]
            },
            "codebase-analyzer": {
                "primary_roles": ["analysis", "documentation", "architecture_review"],
                "keywords": ["analyze", "review", "understand", "document", "architecture"],
                "complexity_range": ["simple", "moderate", "complex"],
                "best_for": ["code analysis", "technical documentation", "system understanding"]
            },
            "codebase-locator": {
                "primary_roles": ["search", "discovery", "mapping"],
                "keywords": ["find", "locate", "search", "discover", "where", "which"],
                "complexity_range": ["simple", "moderate"],
                "best_for": ["file discovery", "code location", "dependency mapping"]
            },
            "security-specialist": {
                "primary_roles": ["security", "compliance", "vulnerability_assessment"],
                "keywords": ["security", "secure", "vulnerability", "compliance", "audit", "penetration"],
                "complexity_range": ["moderate", "complex"],
                "best_for": ["security audits", "compliance validation", "vulnerability assessment"]
            },
            "backend-architect": {
                "primary_roles": ["api_design", "architecture", "scalability"],
                "keywords": ["api", "backend", "service", "architecture", "scalability", "design"],
                "complexity_range": ["moderate", "complex"],
                "best_for": ["API design", "backend architecture", "scalability planning"]
            },
            "rust-expert-developer": {
                "primary_roles": ["rust_implementation", "performance", "systems_programming"],
                "keywords": ["rust", "implement", "performance", "systems", "low-level"],
                "complexity_range": ["moderate", "complex"],
                "best_for": ["Rust implementation", "performance optimization", "systems programming"]
            },
            "competitive-market-analyst": {
                "primary_roles": ["market_research", "competitive_analysis", "business_intelligence"],
                "keywords": ["market", "competitive", "research", "analysis", "business", "strategy"],
                "complexity_range": ["moderate", "complex"],
                "best_for": ["market research", "competitive analysis", "business strategy"]
            },
            "web-search-researcher": {
                "primary_roles": ["research", "information_gathering", "web_analysis"],
                "keywords": ["research", "search", "information", "web", "investigate"],
                "complexity_range": ["simple", "moderate"],
                "best_for": ["web research", "information gathering", "trend analysis"]
            }
        }
    
    def load_skills_commands_mapping(self):
        """Load skills and commands mapping"""
        self.skills_mapping = {
            "project_management": ["multi-agent-workflow", "evaluation-framework", "communication-protocols"],
            "development": ["production-patterns", "framework-patterns", "code-analysis-planning-editor"],
            "security": ["security-patterns", "compliance-validation"],
            "analysis": ["search-strategies", "token-cost-tracking", "internal-comms"],
            "infrastructure": ["gcp-resource-cleanup", "git-workflow-automation"]
        }
        
        self.commands_mapping = {
            "planning": ["/create_plan", "/validate_plan", "/implement_plan"],
            "research": ["/research", "/research_codebase", "/smart-research"],
            "development": ["/feature_development", "/rust_scaffold", "/component_scaffold"],
            "security": ["/security_deps", "/security_sast", "/security_hardening"],
            "deployment": ["/config_validate", "/monitor_setup", "/db_migrations"]
        }
    
    def analyze_workflow(self, description: str, context: Dict = None) -> Dict:
        """
        Analyze workflow description to determine agent requirements
        
        Args:
            description: Natural language description of the workflow
            context: Additional context (existing codebase, constraints, etc.)
            
        Returns:
            Comprehensive workflow analysis with agent recommendations
        """
        requirements = self._extract_requirements(description, context)
        agent_recommendations = self._recommend_agents(requirements, description)
        coordination_strategy = self._plan_coordination(agent_recommendations)
        
        return {
            "workflow_summary": description,
            "requirements": requirements,
            "agent_recommendations": agent_recommendations,
            "coordination_strategy": coordination_strategy,
            "execution_plan": self._generate_execution_plan(agent_recommendations),
            "estimated_complexity": self._estimate_complexity(requirements),
            "resource_requirements": self._estimate_resources(agent_recommendations)
        }
    
    def _extract_requirements(self, description: str, context: Dict) -> List[WorkflowRequirement]:
        """Extract workflow requirements from description"""
        requirements = []
        
        # Security requirements
        if any(keyword in description.lower() for keyword in ["security", "secure", "audit", "compliance"]):
            requirements.append(WorkflowRequirement(
                category="security",
                description="Security validation and compliance verification",
                complexity="moderate",
                priority="high",
                estimated_effort="30-60 minutes",
                dependencies=[]
            ))
        
        # Development requirements  
        if any(keyword in description.lower() for keyword in ["implement", "build", "create", "develop"]):
            requirements.append(WorkflowRequirement(
                category="development",
                description="Implementation and development work",
                complexity="moderate",
                priority="high", 
                estimated_effort="60-120 minutes",
                dependencies=["analysis"]
            ))
        
        # Analysis requirements
        if any(keyword in description.lower() for keyword in ["analyze", "understand", "review", "examine"]):
            requirements.append(WorkflowRequirement(
                category="analysis",
                description="Code analysis and system understanding",
                complexity="simple",
                priority="medium",
                estimated_effort="15-30 minutes", 
                dependencies=[]
            ))
        
        # Research requirements
        if any(keyword in description.lower() for keyword in ["research", "investigate", "find", "discover"]):
            requirements.append(WorkflowRequirement(
                category="research",
                description="Information gathering and research",
                complexity="simple",
                priority="medium",
                estimated_effort="20-40 minutes",
                dependencies=[]
            ))
        
        return requirements
    
    def _recommend_agents(self, requirements: List[WorkflowRequirement], description: str) -> List[AgentRecommendation]:
        """Recommend agents based on requirements analysis"""
        recommendations = []
        
        # Determine if orchestration is needed
        if len(requirements) > 2 or any(req.complexity == "complex" for req in requirements):
            recommendations.append(AgentRecommendation(
                agent_type="orchestrator",
                confidence=0.9,
                reasoning="Multi-step workflow requires coordination",
                skills_needed=["multi-agent-workflow", "communication-protocols"],
                commands_suggested=["/create_plan", "/implement_plan"],
                coordination_role="primary"
            ))
        
        # Match agents to requirements
        for req in requirements:
            if req.category == "security":
                recommendations.append(AgentRecommendation(
                    agent_type="security-specialist",
                    confidence=0.85,
                    reasoning="Security requirements identified",
                    skills_needed=["security-patterns"],
                    commands_suggested=["/security_sast", "/security_hardening"],
                    coordination_role="supporting"
                ))
            
            elif req.category == "analysis":
                recommendations.append(AgentRecommendation(
                    agent_type="codebase-analyzer", 
                    confidence=0.8,
                    reasoning="Analysis and documentation needed",
                    skills_needed=["code-analysis-planning-editor"],
                    commands_suggested=["/research_codebase"],
                    coordination_role="supporting"
                ))
            
            elif req.category == "development" and "rust" in description.lower():
                recommendations.append(AgentRecommendation(
                    agent_type="rust-expert-developer",
                    confidence=0.9,
                    reasoning="Rust development expertise required",
                    skills_needed=["rust-backend-patterns", "production-patterns"],
                    commands_suggested=["/rust_scaffold", "/feature_development"],
                    coordination_role="supporting"
                ))
            
            elif req.category == "research":
                recommendations.append(AgentRecommendation(
                    agent_type="codebase-locator",
                    confidence=0.75,
                    reasoning="Research and discovery needed",
                    skills_needed=["search-strategies"],
                    commands_suggested=["/smart-research"],
                    coordination_role="supporting"
                ))
        
        return recommendations
    
    def _plan_coordination(self, recommendations: List[AgentRecommendation]) -> Dict:
        """Plan agent coordination strategy"""
        primary_agents = [r for r in recommendations if r.coordination_role == "primary"]
        supporting_agents = [r for r in recommendations if r.coordination_role == "supporting"]
        
        if primary_agents:
            coordinator = primary_agents[0].agent_type
        else:
            coordinator = "orchestrator"  # Default coordinator
        
        return {
            "coordinator": coordinator,
            "execution_pattern": "sequential" if len(supporting_agents) <= 2 else "parallel_then_integrate",
            "communication_flow": [
                {"from": coordinator, "to": agent.agent_type, "type": "task_assignment"}
                for agent in supporting_agents
            ],
            "validation_points": [
                "After discovery phase",
                "After implementation phase", 
                "Before final delivery"
            ]
        }
    
    def _generate_execution_plan(self, recommendations: List[AgentRecommendation]) -> List[Dict]:
        """Generate step-by-step execution plan"""
        plan = []
        
        # Phase 1: Discovery and Planning
        plan.append({
            "phase": "Discovery & Planning",
            "progress": 25,
            "tasks": [
                f"Execute discovery using {rec.agent_type}" 
                for rec in recommendations 
                if rec.agent_type in ["codebase-locator", "codebase-analyzer"]
            ],
            "deliverables": ["Requirements analysis", "Implementation strategy"]
        })
        
        # Phase 2: Core Implementation
        plan.append({
            "phase": "Core Implementation", 
            "progress": 50,
            "tasks": [
                f"Execute implementation using {rec.agent_type}"
                for rec in recommendations
                if rec.agent_type in ["rust-expert-developer", "backend-architect"]
            ],
            "deliverables": ["Working implementation", "Initial testing"]
        })
        
        # Phase 3: Validation and Security
        plan.append({
            "phase": "Validation & Security",
            "progress": 75,
            "tasks": [
                f"Execute validation using {rec.agent_type}"
                for rec in recommendations
                if rec.agent_type in ["security-specialist"]
            ],
            "deliverables": ["Security validation", "Quality assurance"]
        })
        
        # Phase 4: Integration and Completion
        plan.append({
            "phase": "Integration & Completion",
            "progress": 100,
            "tasks": ["Final integration", "Documentation", "Deployment preparation"],
            "deliverables": ["Complete solution", "Documentation", "Deployment guide"]
        })
        
        return plan
    
    def _estimate_complexity(self, requirements: List[WorkflowRequirement]) -> str:
        """Estimate overall workflow complexity"""
        if any(req.complexity == "complex" for req in requirements):
            return "complex"
        elif len(requirements) > 3 or any(req.complexity == "moderate" for req in requirements):
            return "moderate"
        else:
            return "simple"
    
    def _estimate_resources(self, recommendations: List[AgentRecommendation]) -> Dict:
        """Estimate resource requirements"""
        return {
            "agent_count": len(recommendations),
            "estimated_duration": f"{len(recommendations) * 15}-{len(recommendations) * 30} minutes",
            "token_budget": f"{len(recommendations) * 20}K-{len(recommendations) * 40}K tokens",
            "coordination_overhead": "10-20%" if len(recommendations) > 2 else "5-10%"
        }

# Example usage
if __name__ == "__main__":
    analyzer = WorkflowAnalyzer()
    
    # Analyze a complex workflow
    analysis = analyzer.analyze_workflow(
        "Implement secure user profile management with Rust backend, including API endpoints, database updates, security validation, and comprehensive testing"
    )
    
    print(json.dumps(analysis, indent=2, default=str))