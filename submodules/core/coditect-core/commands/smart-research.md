# Smart Research - Intelligent Market Research Automation

**Purpose**: Minimize user prompting while maximizing research autonomy through intelligent intent classification and auto-execution.

## How It Works

When user provides research request, this command:
1. **Classifies intent** using pattern matching
2. **Calculates confidence** in interpretation  
3. **Auto-executes** or requests minimal clarification
4. **Launches appropriate agents** with smart defaults
5. **Provides progress updates** and refinement options

## Usage Patterns

### Auto-Execution (High Confidence ≥80%)
```bash
User: "Research Cursor IDE pricing"
System: 🎯 Auto-detected: Pricing analysis for Cursor IDE
         🔍 Launching web-search-researcher with pricing focus...
         [Executes automatically]
```

### Quick Confirmation (Medium Confidence 40-79%)  
```bash
User: "Analyze the competitive landscape"
System: 📊 I'll analyze AI IDE competitive landscape including:
         • Competitor identification & profiling
         • Pricing strategy analysis  
         • Feature comparison matrix
         • Market positioning assessment
         
         Proceed with comprehensive analysis? (y/n/modify scope)
```

### Clarifying Questions (Low Confidence <40%)
```bash
User: "Help with my research"
System: 🤔 I can help with several types of research:
         [a] Market & competitive analysis
         [b] Technical architecture research  
         [c] Business strategy & positioning
         [d] Pricing & business model analysis
         
         What's your primary focus?
```

## Intent Classification Engine

### Market Research Patterns
```yaml
high_confidence_patterns:
  "research [company] pricing": 
    agent: web-search-researcher
    scope: pricing_analysis
    confidence: 0.95
    
  "analyze [company] vs [company]":
    agent: competitive-market-analyst  
    scope: comparative_analysis
    confidence: 0.90
    
  "[company] competitive analysis":
    agent: competitive-market-analyst
    scope: competitor_profiling
    confidence: 0.85

medium_confidence_patterns:
  "competitive landscape":
    agent: orchestrator
    scope: market_intelligence_workflow
    confidence: 0.70
    clarification: "Focus area? (pricing/features/positioning/comprehensive)"
    
  "market research":
    agent: competitive-market-analyst
    scope: market_analysis  
    confidence: 0.60
    clarification: "Specific companies or broad market analysis?"

low_confidence_patterns:
  "research":
    confidence: 0.30
    questions: ["What type of research?", "Specific companies/market?", "Business or technical focus?"]
```

## Auto-Scope Detection

### Context Clues for Smart Defaults
```yaml
company_detection:
  patterns: ["Cursor", "GitHub Copilot", "Tabnine", "Codeium", "Replit"]
  action: auto-focus analysis on detected companies
  
pricing_keywords:  
  patterns: ["pricing", "cost", "subscription", "plans", "tiers"]
  action: emphasize pricing analysis in research scope
  
comparison_indicators:
  patterns: ["vs", "versus", "compared to", "against"]  
  action: setup comparative analysis framework
  
launch_context:
  patterns: ["launching", "building", "creating", "developing"]
  action: include positioning and differentiation analysis
```

## Execution Logic

```python
def smart_research_execution(user_input):
    # Step 1: Intent Classification
    intent, confidence, suggested_agent, scope = classify_intent(user_input)
    
    # Step 2: Confidence-Based Routing
    if confidence >= 0.8:
        return auto_execute(suggested_agent, scope, user_input)
    elif confidence >= 0.4:
        return quick_confirmation(intent, scope, user_input)
    else:
        return clarifying_questions(intent, user_input)

def auto_execute(agent, scope, context):
    # Launch agent with smart defaults
    enhanced_prompt = f"""
    Execute {scope} analysis based on: {context}
    
    Auto-detected scope: {scope}
    Context clues: {extract_context_clues(context)}
    Smart defaults: {generate_smart_defaults(scope, context)}
    
    Provide progress updates and offer refinement options upon completion.
    """
    
    return launch_agent(agent, enhanced_prompt)
```

## Progressive Disclosure Points

### Natural Stopping Points
```yaml
initial_findings_complete:
  trigger: "Preliminary research gathered"
  action: "Present key findings + offer deep-dive options"
  options: ["Focus on top competitors", "Expand to adjacent markets", "Deep-dive pricing", "Technical analysis"]

scope_expansion_opportunity:
  trigger: "Interesting adjacent area discovered"  
  action: "Offer to expand research scope"
  example: "Found interesting partnership strategies. Include partnership analysis?"

conflicting_data_detected:
  trigger: "Contradictory information found"
  action: "Request clarification on approach"
  example: "Found conflicting pricing data. Focus on official sources or include analyst estimates?"
```

## Enhanced Agent Integration

### Agent Capability Enhancement
Each research agent gets enhanced with:
```yaml
enhanced_capabilities:
  auto_scope_detection: true
  context_awareness: true  
  progress_reporting: true
  refinement_suggestions: true
  
auto_reporting_triggers:
  - 25% progress: "Initial data gathering complete"
  - 50% progress: "Core analysis underway"  
  - 75% progress: "Synthesis and insights generation"
  - 100% progress: "Analysis complete + refinement options"
```

## Usage Examples

### Example 1: Automatic Execution
```
User: "Research GitHub Copilot pricing for enterprise customers"

System: 🎯 Auto-detected: Enterprise pricing analysis for GitHub Copilot
         🔍 Launching web-search-researcher...
         📊 Progress: Gathering official pricing data [██████████] 100%
         📋 Found: Enterprise pricing tiers, volume discounts, feature comparison
         
         ✅ Analysis Complete:
         • Enterprise tier: $39/user/month
         • Volume discounts: 10% at 100+ users, 20% at 500+ users  
         • Enterprise features: Advanced security, audit logs, priority support
         
         🔍 Next Steps:
         [a] Compare with competitors' enterprise pricing
         [b] Analyze ROI justification strategies
         [c] Research enterprise sales process
```

### Example 2: Smart Orchestration
```
User: "I need to understand how CODITECT should position against Cursor"

System: 🎯 Detected: Strategic positioning analysis 
         📊 This requires multi-faceted analysis. I'll coordinate:
         • Competitive analysis (features, pricing, positioning)
         • Market positioning assessment  
         • Differentiation opportunity identification
         
         🚀 Launching orchestrated research workflow...
         
         [Coordinates multiple agents automatically]
         [Provides integrated strategic recommendations]
```

## Success Metrics

- **Prompt Reduction**: 70% fewer clarification requests needed
- **Time to Insight**: 80% faster research initiation
- **Intent Accuracy**: 85%+ correct auto-classification
- **User Satisfaction**: Preferred automation vs manual agent selection

---

*Smart research command for maximizing automation while ensuring accurate intent fulfillment*