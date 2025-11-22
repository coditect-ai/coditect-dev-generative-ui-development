# Intent Classification Skill - Smart Research Automation

## Description
Advanced natural language intent classification for market research automation. Analyzes user prompts to automatically detect research intent, confidence levels, entities, and optimal execution strategies.

## Core Intent Classification Patterns

### Market Research Intents (High Confidence ≥85%)
```yaml
competitive_analysis:
  patterns: ["competitive analysis", "analyze competitors", "competitive landscape", "competitor research"]
  entities: ["company names", "product names"]
  auto_agent: "competitive-market-analyst"
  confidence: 0.90

pricing_research:
  patterns: ["pricing", "pricing strategy", "cost", "subscription", "plans", "price comparison"]
  entities: ["company names", "product tiers"]
  auto_agent: "web-search-researcher"
  confidence: 0.85

market_landscape:
  patterns: ["market landscape", "market analysis", "market overview", "industry analysis"]
  entities: ["market segments", "industry terms"]
  auto_agent: "competitive-market-analyst"
  confidence: 0.88

feature_comparison:
  patterns: ["feature comparison", "features", "capabilities", "functionality comparison"]
  entities: ["product names", "feature categories"]
  auto_agent: "competitive-market-analyst"
  confidence: 0.87
```

### Comparative Analysis Intents (High Confidence ≥80%)
```yaml
direct_comparison:
  patterns: ["vs", "versus", "compared to", "compare", "A vs B"]
  entities: ["company A", "company B"]
  auto_agent: "competitive-market-analyst"
  confidence: 0.95
  scope: "comparative_analysis"

positioning_analysis:
  patterns: ["positioning", "market position", "how to position", "competitive positioning"]
  entities: ["company names", "target markets"]
  auto_agent: "competitive-market-analyst" 
  confidence: 0.82
  scope: "strategic_positioning"
```

### Workflow Complexity Intents (Medium Confidence 60-79%)
```yaml
comprehensive_research:
  patterns: ["comprehensive", "complete analysis", "full research", "in-depth", "thorough"]
  auto_agent: "orchestrator"
  confidence: 0.75
  workflow: "multi_agent_research"

quick_overview:
  patterns: ["quick", "brief", "overview", "summary", "fast research"]
  auto_agent: "web-search-researcher"
  confidence: 0.70
  scope: "summary_research"
```

## Entity Detection Algorithms

### Company/Product Detection
```python
def detect_entities(text):
    companies = [
        "Cursor", "GitHub Copilot", "Tabnine", "Codeium", "Replit", 
        "Amazon CodeWhisperer", "JetBrains AI", "Sourcegraph Cody",
        "OpenAI Codex", "Anthropic Claude", "Google Bard"
    ]
    
    products = [
        "IDE", "code assistant", "development tool", "AI IDE", 
        "coding assistant", "code completion", "pair programming"
    ]
    
    detected_companies = [c for c in companies if c.lower() in text.lower()]
    detected_products = [p for p in products if p.lower() in text.lower()]
    
    return {
        "companies": detected_companies,
        "products": detected_products,
        "has_comparison": any(word in text.lower() for word in ["vs", "versus", "compared to", "compare"])
    }
```

### Scope Keywords Detection
```python
def detect_scope_keywords(text):
    scope_categories = {
        "pricing": ["pricing", "cost", "price", "subscription", "plans", "tiers", "pricing strategy"],
        "features": ["features", "capabilities", "functionality", "comparison", "technical"],
        "positioning": ["positioning", "market position", "strategy", "differentiation"],
        "market": ["market", "landscape", "overview", "analysis", "size", "trends"],
        "technical": ["technical", "architecture", "implementation", "API", "integration"]
    }
    
    detected_scopes = []
    for category, keywords in scope_categories.items():
        if any(keyword in text.lower() for keyword in keywords):
            detected_scopes.append(category)
    
    return detected_scopes
```

## Confidence Scoring Algorithm

### Multi-Factor Confidence Calculation
```python
def calculate_confidence(text, intent_patterns):
    confidence_factors = {
        "exact_pattern_match": 0.4,      # Exact phrase found
        "keyword_density": 0.2,          # Relevant keywords per total words
        "entity_specificity": 0.2,       # Specific companies/products mentioned
        "context_clarity": 0.1,          # Clear vs ambiguous phrasing
        "scope_specificity": 0.1         # Specific scope keywords present
    }
    
    base_confidence = calculate_pattern_match(text, intent_patterns)
    
    # Boost for entity specificity
    entities = detect_entities(text)
    if entities["companies"]:
        base_confidence += 0.1
    
    # Boost for clear scope
    scopes = detect_scope_keywords(text)
    if len(scopes) >= 2:
        base_confidence += 0.05
    
    # Boost for comparison indicators
    if entities["has_comparison"]:
        base_confidence += 0.15
    
    return min(base_confidence, 1.0)
```

## Auto-Execution Decision Matrix

### Confidence-Based Routing
```yaml
execution_strategy:
  high_confidence: # ≥80%
    action: "auto_execute"
    message: "🎯 Auto-detected: {intent} - Executing {agent}..."
    
  medium_confidence: # 40-79%
    action: "quick_confirmation" 
    message: "📊 Detected: {intent}. Proceed with {scope}? (y/n/modify)"
    
  low_confidence: # <40%
    action: "clarifying_questions"
    message: "🤔 I can help with: {options}. What's your focus?"
```

### Smart Default Generation
```python
def generate_smart_defaults(intent, entities, scopes):
    defaults = {
        "agent": select_optimal_agent(intent, scopes),
        "scope": prioritize_scope_areas(scopes),
        "entities": focus_entity_list(entities),
        "methodology": select_methodology(intent, entities)
    }
    
    return defaults
```

## Enhanced Prompt Generation

### Context-Aware Prompt Building
```python
def build_enhanced_prompt(original_prompt, classification_results):
    enhanced_prompt = f"""
Original Request: {original_prompt}

Auto-Detected Context:
- Intent: {classification_results.intent} (confidence: {classification_results.confidence})
- Focus Areas: {classification_results.scopes}
- Key Entities: {classification_results.entities}
- Recommended Approach: {classification_results.methodology}

Enhanced Instructions:
{generate_contextual_instructions(classification_results)}

Execute this research with your enhanced context awareness, providing progress updates at your defined checkpoints.
"""
    return enhanced_prompt
```

## Usage Integration Examples

### Example 1: High Confidence Auto-Execution
```
User Input: "Research Cursor vs GitHub Copilot pricing for enterprise customers"

Classification Results:
- Intent: pricing_research + direct_comparison
- Confidence: 0.95 (HIGH)
- Entities: ["Cursor", "GitHub Copilot"] 
- Scope: ["pricing", "enterprise"]
- Agent: competitive-market-analyst

Auto-Execution:
🎯 Auto-detected: Enterprise pricing comparison - Launching competitive-market-analyst...
```

### Example 2: Medium Confidence Quick Confirmation
```
User Input: "I need to understand the competitive landscape"

Classification Results:
- Intent: competitive_analysis
- Confidence: 0.65 (MEDIUM)
- Entities: []
- Scope: ["competitive", "market"]
- Agent: competitive-market-analyst

Quick Confirmation:
📊 Detected: Competitive landscape analysis for AI development tools.
Proceed with comprehensive competitor research? (y/n/modify scope)
```

### Example 3: Low Confidence Clarification
```
User Input: "Help me with research"

Classification Results:
- Intent: unclear
- Confidence: 0.25 (LOW)
- Entities: []
- Scope: []

Clarifying Questions:
🤔 I can help with several types of research:
[a] Competitive market analysis
[b] Pricing strategy research  
[c] Technical feature comparison
[d] Market landscape overview

What's your primary focus?
```

## Implementation Integration

### Command Integration
This skill integrates with `/smart-research` command:
```bash
/smart-research "user prompt here"
# Automatically applies intent classification and executes optimal workflow
```

### Agent Enhancement Integration
Enhanced agents use classification results:
```yaml
agent_context_enhancement:
  - Receives classification results in enhanced prompt
  - Auto-adapts methodology based on detected intent/scope
  - Provides targeted progress reporting
  - Suggests relevant expansion options
```

## Success Metrics

### Classification Accuracy
- **Target**: 85% correct intent classification
- **Measurement**: User confirmation/correction rates
- **Optimization**: Continuous learning from user feedback

### Automation Efficiency  
- **Target**: 70% reduction in required user prompting
- **Measurement**: Prompt count before/after implementation
- **Optimization**: Confidence threshold tuning

### User Satisfaction
- **Target**: 90% user preference for automated vs manual
- **Measurement**: User feedback and usage patterns
- **Optimization**: Balance automation vs control preferences

---

*Intent classification skill for maximizing research automation intelligence*