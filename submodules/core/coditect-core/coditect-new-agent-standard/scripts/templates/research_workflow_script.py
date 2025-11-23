#!/usr/bin/env python3
"""
Research Workflow Script Template - Intelligent Research Automation
Reusable template for comprehensive research projects with multi-agent coordination.
"""

import sys
import os
import json
from datetime import datetime

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from agent_caller import AgentCaller, AgentType
from workflow_analyzer import WorkflowAnalyzer

class ResearchWorkflowScript:
    """Reusable research workflow automation template"""
    
    def __init__(self, research_topic: str, scope: str = "comprehensive"):
        self.research_topic = research_topic
        self.scope = scope  # comprehensive, focused, quick
        self.session_id = f"research_{int(datetime.now().timestamp())}"
        
        # Initialize components
        self.agent_caller = AgentCaller()
        self.workflow_analyzer = WorkflowAnalyzer()
        
        # Research state
        self.research_findings = {}
        self.sources = []
        self.analysis_results = {}
        
    def plan_research_strategy(self, requirements: dict) -> dict:
        """
        Step 1: Plan comprehensive research strategy
        Uses orchestrator to coordinate research approach
        """
        print(f"🔍 Planning research strategy for: {self.research_topic}")
        
        planning_prompt = f"""plan a comprehensive research strategy for: {self.research_topic}

Research Scope: {self.scope}
Requirements: {json.dumps(requirements, indent=2)}

Create detailed research plan including:
1. Research phases with specific objectives
2. Information sources and search strategies  
3. Analysis frameworks and methodologies
4. Quality validation and fact-checking approach
5. Deliverable structure and format
6. Agent coordination for parallel research streams

Provide structured plan with checkboxes for task tracking."""
        
        strategy_task = self.agent_caller.call_agent(
            AgentType.ORCHESTRATOR,
            planning_prompt,
            f"{self.session_id}_strategy"
        )
        
        print(f"✅ Research strategy planned")
        return {"strategy": strategy_task}
    
    def execute_web_research(self, research_areas: list) -> dict:
        """
        Step 2: Execute web research across multiple areas
        Uses web-search-researcher for intelligent information gathering
        """
        print(f"🌐 Executing web research for {len(research_areas)} areas...")
        
        research_results = {}
        
        for i, area in enumerate(research_areas):
            print(f"   Researching: {area}")
            
            research_prompt = f"""conduct comprehensive web research on: {area}

Context: This is part of broader research on "{self.research_topic}"
Research Scope: {self.scope}

Research Requirements:
1. Gather current information (2024-2025 timeframe preferred)
2. Identify authoritative sources and recent developments
3. Extract key facts, statistics, and trends
4. Note source credibility and publication dates
5. Organize findings by relevance and importance
6. Flag any conflicting information for further investigation

Focus Areas for {area}:
- Current market state and recent changes
- Key players and their positions
- Trends and future projections  
- Critical success factors
- Challenges and opportunities

Provide structured research summary with source citations."""
            
            research_task = self.agent_caller.call_agent(
                AgentType.WEB_SEARCH_RESEARCHER,
                research_prompt,
                f"{self.session_id}_web_research_{i+1}"
            )
            
            research_results[area] = research_task
        
        print(f"✅ Web research completed for all areas")
        return research_results
    
    def execute_competitive_analysis(self, competitors: list) -> dict:
        """
        Step 3: Execute competitive analysis
        Uses competitive-market-analyst for strategic intelligence
        """
        print(f"🏆 Executing competitive analysis for {len(competitors)} entities...")
        
        analysis_prompt = f"""conduct comprehensive competitive analysis for: {self.research_topic}

Competitors to analyze: {json.dumps(competitors, indent=2)}
Analysis Scope: {self.scope}

Competitive Analysis Framework:
1. Market positioning and value propositions
2. Pricing strategies and business models
3. Product/service feature comparison
4. Strengths, weaknesses, opportunities, threats (SWOT)
5. Market share and growth trends
6. Strategic partnerships and ecosystem positioning
7. Technology differentiation and innovation
8. Customer segments and targeting strategies

Deliverables Required:
- Competitive landscape overview
- Detailed competitor profiles
- Feature comparison matrix
- Pricing analysis and benchmarks
- Strategic recommendations for differentiation
- Market opportunity assessment

Focus on actionable intelligence for strategic decision-making."""
        
        competitive_task = self.agent_caller.call_agent(
            AgentType.COMPETITIVE_MARKET_ANALYST,
            analysis_prompt,
            f"{self.session_id}_competitive_analysis"
        )
        
        print(f"✅ Competitive analysis completed")
        return {"competitive_analysis": competitive_task}
    
    def execute_codebase_research(self, codebase_areas: list) -> dict:
        """
        Step 4: Execute codebase research (when applicable)
        Uses codebase-locator and codebase-analyzer for technical research
        """
        if not codebase_areas:
            print("📝 Skipping codebase research (not applicable)")
            return {}
            
        print(f"💻 Executing codebase research for {len(codebase_areas)} areas...")
        
        codebase_results = {}
        
        # First, locate relevant code
        for area in codebase_areas:
            print(f"   Locating code for: {area}")
            
            location_prompt = f"""locate and catalog code related to: {area}

Research Context: {self.research_topic}
Search Strategy: Comprehensive discovery

Location Tasks:
1. Find all files related to {area}
2. Identify key components and modules
3. Map dependencies and relationships
4. Catalog API endpoints and interfaces
5. Document configuration and setup files
6. Note testing and documentation coverage

Provide organized file inventory with descriptions."""
            
            location_task = self.agent_caller.call_agent(
                AgentType.CODEBASE_LOCATOR,
                location_prompt,
                f"{self.session_id}_locate_{area.replace(' ', '_')}"
            )
            
            # Then analyze the found code
            analysis_prompt = f"""analyze code implementation for: {area}

Research Context: {self.research_topic}
Analysis Scope: Technical architecture and implementation patterns

Analysis Requirements:
1. Review implementation quality and patterns
2. Assess architectural decisions and trade-offs  
3. Identify strengths and potential improvements
4. Document dependencies and technology choices
5. Evaluate security and performance considerations
6. Note testing coverage and documentation quality

Provide comprehensive technical analysis with findings."""
            
            analysis_task = self.agent_caller.call_agent(
                AgentType.CODEBASE_ANALYZER,
                analysis_prompt,
                f"{self.session_id}_analyze_{area.replace(' ', '_')}"
            )
            
            codebase_results[area] = {
                "location": location_task,
                "analysis": analysis_task
            }
        
        print(f"✅ Codebase research completed")
        return codebase_results
    
    def synthesize_findings(self, all_research_data: dict) -> dict:
        """
        Step 5: Synthesize all research findings
        Uses orchestrator to coordinate comprehensive analysis
        """
        print(f"🧠 Synthesizing research findings...")
        
        synthesis_prompt = f"""synthesize comprehensive research findings for: {self.research_topic}

Research Data Summary:
{json.dumps(list(all_research_data.keys()), indent=2)}

Synthesis Requirements:
1. Integrate findings from all research streams
2. Identify key insights and patterns across sources
3. Resolve any conflicting information
4. Generate strategic conclusions and recommendations
5. Assess market opportunities and risks
6. Create executive summary with key takeaways
7. Develop actionable recommendations
8. Identify areas requiring follow-up research

Deliverable Structure:
- Executive Summary (key findings in 2-3 paragraphs)
- Market Landscape Analysis
- Competitive Intelligence Summary
- Technical Assessment (if applicable)
- Strategic Recommendations
- Risk Assessment and Mitigation
- Next Steps and Follow-up Research Areas

Focus on actionable intelligence for decision-making."""
        
        synthesis_task = self.agent_caller.call_agent(
            AgentType.ORCHESTRATOR,
            synthesis_prompt,
            f"{self.session_id}_synthesis"
        )
        
        print(f"✅ Research synthesis completed")
        return {"synthesis": synthesis_task}
    
    def generate_research_deliverables(self, synthesis: dict) -> dict:
        """
        Step 6: Generate final research deliverables
        Creates comprehensive research report and supporting materials
        """
        print(f"📄 Generating research deliverables...")
        
        deliverables = {
            "research_overview": {
                "topic": self.research_topic,
                "scope": self.scope,
                "session_id": self.session_id,
                "completion_date": datetime.now().isoformat(),
                "research_methodology": "Multi-agent coordinated research"
            },
            "executive_summary": {
                "key_findings": "Generated from synthesis",
                "market_opportunities": "Extracted from competitive analysis",
                "strategic_recommendations": "Derived from comprehensive analysis",
                "next_steps": "Based on research gaps identified"
            },
            "detailed_findings": {
                "web_research_summary": "Comprehensive market intelligence",
                "competitive_landscape": "Strategic competitive positioning",
                "technical_analysis": "Technology and implementation insights",
                "synthesis_report": "Integrated analysis and recommendations"
            },
            "supporting_materials": {
                "source_inventory": "Complete list of research sources",
                "data_validation": "Fact-checking and verification notes",
                "methodology_notes": "Research process documentation",
                "follow_up_areas": "Additional research opportunities"
            }
        }
        
        print(f"✅ Research deliverables generated")
        print(f"   - Executive summary with key findings")
        print(f"   - Detailed analysis report")
        print(f"   - Strategic recommendations")
        print(f"   - Supporting research materials")
        
        return deliverables
    
    def run_complete_research_workflow(self, 
                                     requirements: dict,
                                     research_areas: list = None,
                                     competitors: list = None,
                                     codebase_areas: list = None) -> dict:
        """
        Execute complete research workflow
        One-command execution of entire research process
        """
        print(f"\n🔬 Starting Complete Research Workflow")
        print(f"Topic: {self.research_topic}")
        print(f"Scope: {self.scope}")
        print(f"Session: {self.session_id}")
        print("=" * 60)
        
        try:
            all_research_data = {}
            
            # Step 1: Research Strategy Planning
            strategy = self.plan_research_strategy(requirements)
            all_research_data["strategy"] = strategy
            
            # Step 2: Web Research
            if research_areas:
                web_research = self.execute_web_research(research_areas)
                all_research_data["web_research"] = web_research
            
            # Step 3: Competitive Analysis
            if competitors:
                competitive_analysis = self.execute_competitive_analysis(competitors)
                all_research_data["competitive_analysis"] = competitive_analysis
            
            # Step 4: Codebase Research  
            if codebase_areas:
                codebase_research = self.execute_codebase_research(codebase_areas)
                all_research_data["codebase_research"] = codebase_research
            
            # Step 5: Synthesis
            synthesis = self.synthesize_findings(all_research_data)
            all_research_data["synthesis"] = synthesis
            
            # Step 6: Generate Deliverables
            deliverables = self.generate_research_deliverables(synthesis)
            
            print("\n" + "=" * 60)
            print(f"🎉 RESEARCH COMPLETE: {self.research_topic}")
            print(f"✅ All research streams completed successfully")
            print(f"📊 Comprehensive deliverables ready for review")
            
            return deliverables
            
        except Exception as e:
            print(f"\n❌ Research workflow failed: {str(e)}")
            return {"error": str(e), "session_id": self.session_id}

# Example usage patterns
def market_research_example():
    """Example: AI IDE market research"""
    research = ResearchWorkflowScript(
        research_topic="AI-powered IDE market positioning and pricing strategy",
        scope="comprehensive"
    )
    
    return research.run_complete_research_workflow(
        requirements={
            "target_market": "Professional developers and enterprises",
            "geographic_scope": "Global, focus on US/EU markets", 
            "time_horizon": "2025-2026 planning horizon",
            "decision_context": "Product positioning and pricing strategy"
        },
        research_areas=[
            "AI coding assistant market size and growth",
            "Developer productivity tools adoption trends",
            "Enterprise software procurement patterns",
            "AI technology integration preferences"
        ],
        competitors=[
            "GitHub Copilot",
            "Cursor AI IDE", 
            "JetBrains AI Assistant",
            "Amazon CodeWhisperer",
            "Tabnine"
        ]
    )

def technology_research_example():
    """Example: Technology stack research"""
    research = ResearchWorkflowScript(
        research_topic="Modern web development framework comparison",
        scope="focused"
    )
    
    return research.run_complete_research_workflow(
        requirements={
            "project_context": "Large-scale enterprise application",
            "performance_requirements": "High scalability and maintainability",
            "team_context": "Mixed experience levels",
            "timeline": "6-month development cycle"
        },
        research_areas=[
            "React ecosystem maturity and trends",
            "Vue.js enterprise adoption",
            "Angular framework evolution", 
            "Performance benchmarking studies"
        ],
        codebase_areas=[
            "Frontend component libraries",
            "State management patterns",
            "Build and deployment configurations"
        ]
    )

def competitive_intelligence_example():
    """Example: Pure competitive intelligence"""
    research = ResearchWorkflowScript(
        research_topic="Cloud infrastructure competitive landscape",
        scope="comprehensive"
    )
    
    return research.run_complete_research_workflow(
        requirements={
            "analysis_focus": "Multi-cloud strategy implications",
            "business_context": "Enterprise migration planning",
            "cost_considerations": "TCO optimization priorities",
            "compliance_needs": "SOC2, GDPR, HIPAA requirements"
        },
        research_areas=[
            "Multi-cloud adoption trends",
            "Hybrid cloud market evolution",
            "Cloud cost optimization strategies"
        ],
        competitors=[
            "Amazon Web Services",
            "Microsoft Azure",
            "Google Cloud Platform", 
            "Digital Ocean",
            "Linode"
        ]
    )

if __name__ == "__main__":
    # Run example research
    if len(sys.argv) > 1:
        research_type = sys.argv[1]
        
        if research_type == "market":
            result = market_research_example()
        elif research_type == "technology":
            result = technology_research_example() 
        elif research_type == "competitive":
            result = competitive_intelligence_example()
        else:
            print("Usage: python research_workflow_script.py [market|technology|competitive]")
            sys.exit(1)
    else:
        # Custom research
        research = ResearchWorkflowScript(
            research_topic="Your research topic here",
            scope="comprehensive"
        )
        result = research.run_complete_research_workflow(
            requirements={"context": "Your requirements here"},
            research_areas=["Area 1", "Area 2"],
            competitors=["Competitor 1", "Competitor 2"]
        )
    
    print(f"\nResearch deliverables: {list(result.keys())}")