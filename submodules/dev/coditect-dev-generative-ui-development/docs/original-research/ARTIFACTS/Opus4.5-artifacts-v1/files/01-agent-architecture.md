# Generative UI Agent Architecture

*LLM-agnostic multi-agent system for autonomous UI generation*

---

## Overview

This document defines a modular agent architecture for Generative UI that operates within Claude Code or any compatible agentic coding environment. The architecture is designed to be LLM-agnostic, allowing deployment with Claude, GPT-4, Gemini, or local models.

---

## 1. Agent Taxonomy

### 1.1 Agent Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GENERATIVE UI AGENT ECOSYSTEM                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    ORCHESTRATOR AGENT                            │   │
│  │  - Request routing                                               │   │
│  │  - Token budget management                                       │   │
│  │  - Quality gate enforcement                                      │   │
│  │  - Result synthesis                                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│       ┌──────────────────────┼──────────────────────┐                  │
│       ↓                      ↓                      ↓                  │
│  ┌──────────┐          ┌──────────┐          ┌──────────┐             │
│  │ INTENT   │          │   UI     │          │  CODE    │             │
│  │ ANALYZER │          │ DESIGNER │          │ GENERATOR│             │
│  └──────────┘          └──────────┘          └──────────┘             │
│       │                      │                      │                  │
│       ↓                      ↓                      ↓                  │
│  ┌──────────┐          ┌──────────┐          ┌──────────┐             │
│  │ A11Y     │          │ MOTION   │          │ QUALITY  │             │
│  │ AUDITOR  │          │ DESIGNER │          │ REVIEWER │             │
│  └──────────┘          └──────────┘          └──────────┘             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Agent Definitions

```yaml
# agents/orchestrator.yaml
agent:
  name: ui-orchestrator
  role: orchestrator
  description: |
    Coordinates UI generation workflow, routes tasks to specialized agents,
    manages token budgets, and enforces quality gates.
  
  capabilities:
    - task_decomposition
    - agent_routing
    - budget_management
    - result_synthesis
    - quality_enforcement
  
  triggers:
    - /ui
    - /component
    - /layout
    - /design
  
  delegation_rules:
    simple_component:
      agents: [code-generator]
      budget: 5000
    
    complex_component:
      agents: [intent-analyzer, ui-designer, code-generator, a11y-auditor]
      budget: 20000
    
    full_layout:
      agents: [intent-analyzer, ui-designer, motion-designer, code-generator, a11y-auditor, quality-reviewer]
      budget: 50000
    
    design_to_code:
      agents: [intent-analyzer, ui-designer, code-generator, a11y-auditor]
      budget: 30000
  
  quality_gates:
    - accessibility_score: ">= 90"
    - type_coverage: ">= 95"
    - no_critical_security: true
```

```yaml
# agents/intent-analyzer.yaml
agent:
  name: intent-analyzer
  role: specialist
  description: |
    Analyzes user requests to extract UI requirements, constraints,
    and implicit expectations. Produces structured specifications.
  
  capabilities:
    - requirement_extraction
    - constraint_inference
    - ambiguity_resolution
    - spec_generation
  
  input_schema:
    user_request: string
    context:
      existing_components: list[string]
      design_system: string?
      framework: string?
  
  output_schema:
    component_type: enum[button, input, card, layout, form, wizard, dashboard]
    requirements:
      functional: list[string]
      props: list[{name: string, type: string, required: boolean}]
      states: list[string]
      behaviors: list[string]
    constraints:
      accessibility_level: enum[A, AA, AAA]
      framework: string
      styling: string
      responsive: boolean
    ambiguities: list[{question: string, default: string}]
  
  prompt_template: |
    Analyze this UI request and extract structured requirements:
    
    REQUEST: {user_request}
    CONTEXT: {context}
    
    Output a JSON specification with:
    - component_type
    - requirements (functional, props, states, behaviors)
    - constraints (accessibility, framework, styling)
    - ambiguities (questions needing clarification)
```

```yaml
# agents/ui-designer.yaml
agent:
  name: ui-designer
  role: specialist
  description: |
    Creates UI structure, layout specifications, and component hierarchy
    based on analyzed requirements.
  
  capabilities:
    - layout_design
    - component_hierarchy
    - responsive_planning
    - design_token_mapping
  
  input_schema:
    requirements: RequirementsSpec
    design_system: DesignSystemConfig?
  
  output_schema:
    structure:
      root_element: string
      children: list[ComponentNode]
    layout:
      type: enum[flex, grid, stack]
      responsive_breakpoints: map[breakpoint, LayoutConfig]
    design_tokens:
      colors: map[role, token]
      spacing: map[role, token]
      typography: map[role, token]
    component_api:
      props: list[PropDefinition]
      slots: list[SlotDefinition]
      events: list[EventDefinition]
  
  prompt_template: |
    Design the UI structure for this component:
    
    REQUIREMENTS: {requirements}
    DESIGN_SYSTEM: {design_system}
    
    Create:
    1. Component hierarchy (semantic HTML structure)
    2. Layout specification (flex/grid, responsive)
    3. Design token mappings
    4. Component API (props, slots, events)
```

```yaml
# agents/motion-designer.yaml
agent:
  name: motion-designer
  role: specialist
  description: |
    Designs animation and motion specifications for UI components,
    including transitions, micro-interactions, and loading states.
  
  capabilities:
    - entrance_animations
    - transition_design
    - micro_interactions
    - reduced_motion_fallbacks
  
  input_schema:
    ui_structure: UIStructure
    motion_preference: enum[none, subtle, rich]
  
  output_schema:
    motion_tokens:
      durations: map[name, milliseconds]
      easings: map[name, cubic_bezier]
      distances: map[name, pixels]
    animations:
      entrance: list[AnimationSpec]
      exit: list[AnimationSpec]
      transitions: list[TransitionSpec]
      micro_interactions: list[MicroInteractionSpec]
    reduced_motion:
      strategy: enum[disable, simplify, instant]
      fallbacks: map[animation_name, fallback]
  
  prompt_template: |
    Design motion specifications for this UI:
    
    STRUCTURE: {ui_structure}
    MOTION_PREFERENCE: {motion_preference}
    
    Define:
    1. Motion tokens (durations, easings, distances)
    2. Entrance/exit animations
    3. State transitions
    4. Micro-interactions (hover, press, focus)
    5. Reduced motion fallbacks
```

```yaml
# agents/code-generator.yaml
agent:
  name: code-generator
  role: specialist
  description: |
    Generates production-ready code from UI specifications.
    Supports multiple frameworks and styling approaches.
  
  capabilities:
    - react_generation
    - vue_generation
    - html_css_generation
    - typescript_typing
    - tailwind_styling
  
  input_schema:
    ui_design: UIDesign
    motion_spec: MotionSpec?
    framework: enum[react, vue, svelte, html]
    styling: enum[tailwind, css_modules, styled_components, vanilla]
    typescript: boolean
  
  output_schema:
    files:
      - path: string
        content: string
        language: string
    dependencies: list[{name: string, version: string}]
    usage_example: string
  
  prompt_template: |
    Generate production code for this UI:
    
    DESIGN: {ui_design}
    MOTION: {motion_spec}
    FRAMEWORK: {framework}
    STYLING: {styling}
    TYPESCRIPT: {typescript}
    
    Requirements:
    - Full TypeScript types (if enabled)
    - Complete error handling
    - Accessibility attributes
    - Responsive implementation
    - Motion implementation (if provided)
    
    Output only valid code, no explanations.
```

```yaml
# agents/a11y-auditor.yaml
agent:
  name: a11y-auditor
  role: validator
  description: |
    Audits generated code for accessibility compliance,
    identifies issues, and suggests remediations.
  
  capabilities:
    - wcag_validation
    - aria_checking
    - keyboard_navigation
    - color_contrast
    - focus_management
  
  input_schema:
    code: string
    target_level: enum[A, AA, AAA]
  
  output_schema:
    score: number  # 0-100
    level_achieved: enum[A, AA, AAA, NONE]
    issues:
      - severity: enum[critical, serious, moderate, minor]
        rule: string
        element: string
        message: string
        remediation: string
    passed_checks: list[string]
  
  validation_rules:
    critical:
      - "Images must have alt text"
      - "Form inputs must have labels"
      - "Buttons must have accessible names"
      - "No keyboard traps"
    serious:
      - "Color contrast meets requirements"
      - "Focus indicators visible"
      - "ARIA attributes valid"
    moderate:
      - "Headings in logical order"
      - "Link text is descriptive"
      - "Touch targets >= 44px"
```

```yaml
# agents/quality-reviewer.yaml
agent:
  name: quality-reviewer
  role: validator
  description: |
    Reviews generated code for quality, security, performance,
    and adherence to best practices.
  
  capabilities:
    - code_review
    - security_scanning
    - performance_analysis
    - best_practices
  
  input_schema:
    code: string
    framework: string
  
  output_schema:
    quality_score: number  # 0-100
    security:
      score: number
      findings: list[SecurityFinding]
    performance:
      score: number
      findings: list[PerformanceFinding]
    best_practices:
      score: number
      findings: list[BestPracticeFinding]
    approved: boolean
    blocking_issues: list[string]
  
  checks:
    security:
      - "No eval() usage"
      - "No dangerouslySetInnerHTML without sanitization"
      - "No hardcoded secrets"
      - "No inline event handlers in strings"
    performance:
      - "No unnecessary re-renders"
      - "Images have loading='lazy'"
      - "Lists have stable keys"
    best_practices:
      - "Prefer const over let"
      - "Use semantic HTML"
      - "Proper error boundaries"
```

---

## 2. Agent Communication Protocol

### 2.1 Message Format

```typescript
interface AgentMessage {
  id: string;
  timestamp: string;
  from: AgentId;
  to: AgentId;
  type: MessageType;
  payload: unknown;
  context: ExecutionContext;
  budget: TokenBudget;
}

type MessageType = 
  | 'task_request'
  | 'task_response'
  | 'validation_request'
  | 'validation_response'
  | 'error'
  | 'checkpoint';

interface ExecutionContext {
  session_id: string;
  user_request: string;
  accumulated_results: Record<AgentId, unknown>;
  quality_gates_passed: string[];
  token_usage: number;
}

interface TokenBudget {
  allocated: number;
  consumed: number;
  remaining: number;
  hard_limit: boolean;
}
```

### 2.2 Orchestration Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AGENT COMMUNICATION FLOW                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  User Request: "/ui create a product card with hover effects"           │
│       │                                                                 │
│       ↓                                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ ORCHESTRATOR                                                     │   │
│  │ 1. Parse command                                                 │   │
│  │ 2. Classify complexity → moderate                                │   │
│  │ 3. Allocate budget → 15000 tokens                                │   │
│  │ 4. Create execution plan                                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ↓ task_request                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ INTENT ANALYZER                                                  │   │
│  │ Extract: component_type=card, states=[default,hover],            │   │
│  │          motion=subtle, a11y=AA                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ↓ task_response (requirements_spec)                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ UI DESIGNER                                                      │   │
│  │ Design: structure, layout, tokens, API                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ↓ task_response (ui_design)                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ MOTION DESIGNER                                                  │   │
│  │ Define: hover scale, shadow transition, duration tokens          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ↓ task_response (motion_spec)                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ CODE GENERATOR                                                   │   │
│  │ Generate: ProductCard.tsx with full implementation               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ↓ validation_request                                              │
│  ┌──────────────────────┐    ┌──────────────────────┐                  │
│  │ A11Y AUDITOR         │    │ QUALITY REVIEWER     │                  │
│  │ Score: 94/100        │    │ Score: 88/100        │                  │
│  │ Issues: 1 minor      │    │ Approved: true       │                  │
│  └──────────────────────┘    └──────────────────────┘                  │
│       │                             │                                   │
│       ↓                             ↓                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ ORCHESTRATOR                                                     │   │
│  │ - All gates passed                                               │   │
│  │ - Total tokens: 12,847                                           │   │
│  │ - Return final result                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       │                                                                 │
│       ↓                                                                 │
│  Final Output: ProductCard.tsx + usage example                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Agent Implementation Templates

### 3.1 Base Agent Class

```python
# agents/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
import json
import hashlib

class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    SPECIALIST = "specialist"
    VALIDATOR = "validator"

@dataclass
class AgentConfig:
    name: str
    role: AgentRole
    description: str
    capabilities: List[str]
    max_tokens: int = 10000
    temperature: float = 0.7
    model: str = "default"  # LLM-agnostic

@dataclass
class AgentContext:
    session_id: str
    user_request: str
    accumulated_results: Dict[str, Any] = field(default_factory=dict)
    token_usage: int = 0
    checkpoints: List[Dict] = field(default_factory=list)

@dataclass
class AgentResult:
    success: bool
    output: Any
    tokens_used: int
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseAgent(ABC):
    """Base class for all Generative UI agents"""
    
    def __init__(self, config: AgentConfig, llm_client: Any):
        self.config = config
        self.llm = llm_client
        self._prompt_cache: Dict[str, str] = {}
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    @abstractmethod
    def process(self, input_data: Dict, context: AgentContext) -> AgentResult:
        """Process input and return result"""
        pass
    
    def _call_llm(self, prompt: str, context: AgentContext) -> tuple[str, int]:
        """Make LLM call - implementation is LLM-agnostic"""
        # This method should be implemented by a provider-specific adapter
        response = self.llm.complete(
            system=self.get_system_prompt(),
            prompt=prompt,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        return response.content, response.token_count
    
    def _cache_key(self, prompt: str) -> str:
        """Generate cache key for prompt"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def checkpoint(self, context: AgentContext, state: Dict) -> None:
        """Save checkpoint for recovery"""
        context.checkpoints.append({
            "agent": self.config.name,
            "state": state,
            "tokens": context.token_usage
        })
```

### 3.2 Orchestrator Implementation

```python
# agents/orchestrator.py
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"

@dataclass
class ExecutionPlan:
    complexity: TaskComplexity
    agents: List[str]
    token_budget: int
    quality_gates: List[str]
    parallel_stages: List[List[str]]

class OrchestratorAgent(BaseAgent):
    """Coordinates UI generation workflow"""
    
    COMPLEXITY_BUDGETS = {
        TaskComplexity.SIMPLE: 5000,
        TaskComplexity.MODERATE: 15000,
        TaskComplexity.COMPLEX: 35000,
        TaskComplexity.ENTERPRISE: 75000,
    }
    
    COMPLEXITY_AGENTS = {
        TaskComplexity.SIMPLE: ["code-generator"],
        TaskComplexity.MODERATE: ["intent-analyzer", "ui-designer", "code-generator", "a11y-auditor"],
        TaskComplexity.COMPLEX: ["intent-analyzer", "ui-designer", "motion-designer", "code-generator", "a11y-auditor", "quality-reviewer"],
        TaskComplexity.ENTERPRISE: ["intent-analyzer", "ui-designer", "motion-designer", "code-generator", "a11y-auditor", "quality-reviewer"],
    }
    
    def __init__(self, config: AgentConfig, llm_client: Any, agent_registry: Dict[str, BaseAgent]):
        super().__init__(config, llm_client)
        self.agents = agent_registry
    
    def get_system_prompt(self) -> str:
        return """You are the UI Generation Orchestrator. Your role is to:
1. Analyze user requests for UI generation
2. Classify complexity (simple/moderate/complex/enterprise)
3. Create execution plans
4. Coordinate specialist agents
5. Enforce quality gates
6. Synthesize final results

Always respond with structured JSON."""
    
    def process(self, input_data: Dict, context: AgentContext) -> AgentResult:
        # 1. Classify request complexity
        complexity = self._classify_complexity(input_data["request"])
        
        # 2. Create execution plan
        plan = self._create_plan(complexity, input_data)
        
        # 3. Execute plan
        results = self._execute_plan(plan, context)
        
        # 4. Validate quality gates
        gate_results = self._check_quality_gates(results, plan.quality_gates)
        
        # 5. Synthesize final result
        if all(g["passed"] for g in gate_results):
            return AgentResult(
                success=True,
                output=self._synthesize_output(results),
                tokens_used=context.token_usage,
                metadata={"plan": plan, "gates": gate_results}
            )
        else:
            return AgentResult(
                success=False,
                output=None,
                tokens_used=context.token_usage,
                errors=[g["reason"] for g in gate_results if not g["passed"]]
            )
    
    def _classify_complexity(self, request: str) -> TaskComplexity:
        """Classify request complexity based on keywords and structure"""
        request_lower = request.lower()
        
        enterprise_keywords = ["enterprise", "compliance", "audit", "wcag aaa"]
        complex_keywords = ["wizard", "dashboard", "multi-step", "animation", "motion"]
        moderate_keywords = ["form", "layout", "grid", "filter", "responsive"]
        
        if any(kw in request_lower for kw in enterprise_keywords):
            return TaskComplexity.ENTERPRISE
        elif any(kw in request_lower for kw in complex_keywords):
            return TaskComplexity.COMPLEX
        elif any(kw in request_lower for kw in moderate_keywords):
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.SIMPLE
    
    def _create_plan(self, complexity: TaskComplexity, input_data: Dict) -> ExecutionPlan:
        """Create execution plan for the request"""
        return ExecutionPlan(
            complexity=complexity,
            agents=self.COMPLEXITY_AGENTS[complexity],
            token_budget=self.COMPLEXITY_BUDGETS[complexity],
            quality_gates=self._select_quality_gates(complexity),
            parallel_stages=self._determine_parallelization(complexity)
        )
    
    def _select_quality_gates(self, complexity: TaskComplexity) -> List[str]:
        """Select quality gates based on complexity"""
        gates = ["type_coverage"]
        
        if complexity in [TaskComplexity.MODERATE, TaskComplexity.COMPLEX, TaskComplexity.ENTERPRISE]:
            gates.extend(["accessibility", "security"])
        
        if complexity == TaskComplexity.ENTERPRISE:
            gates.extend(["performance", "documentation"])
        
        return gates
    
    def _determine_parallelization(self, complexity: TaskComplexity) -> List[List[str]]:
        """Determine which agents can run in parallel"""
        if complexity == TaskComplexity.SIMPLE:
            return [["code-generator"]]
        
        # Validators can run in parallel after code generation
        return [
            ["intent-analyzer"],
            ["ui-designer"],
            ["motion-designer"] if complexity >= TaskComplexity.COMPLEX else [],
            ["code-generator"],
            ["a11y-auditor", "quality-reviewer"]  # Parallel validation
        ]
    
    def _execute_plan(self, plan: ExecutionPlan, context: AgentContext) -> Dict[str, AgentResult]:
        """Execute the plan by calling agents in sequence"""
        results = {}
        
        for stage in plan.parallel_stages:
            stage_agents = [a for a in stage if a]  # Filter empty
            
            for agent_name in stage_agents:
                if agent_name not in self.agents:
                    continue
                
                agent = self.agents[agent_name]
                agent_input = self._prepare_agent_input(agent_name, results, context)
                
                result = agent.process(agent_input, context)
                results[agent_name] = result
                context.accumulated_results[agent_name] = result.output
                context.token_usage += result.tokens_used
                
                # Check budget
                if context.token_usage > plan.token_budget:
                    break
        
        return results
    
    def _prepare_agent_input(self, agent_name: str, results: Dict, context: AgentContext) -> Dict:
        """Prepare input for an agent based on previous results"""
        base_input = {"user_request": context.user_request}
        
        if agent_name == "ui-designer" and "intent-analyzer" in results:
            base_input["requirements"] = results["intent-analyzer"].output
        
        if agent_name == "motion-designer" and "ui-designer" in results:
            base_input["ui_structure"] = results["ui-designer"].output
        
        if agent_name == "code-generator":
            if "ui-designer" in results:
                base_input["ui_design"] = results["ui-designer"].output
            if "motion-designer" in results:
                base_input["motion_spec"] = results["motion-designer"].output
        
        if agent_name in ["a11y-auditor", "quality-reviewer"]:
            if "code-generator" in results:
                base_input["code"] = results["code-generator"].output
        
        return base_input
    
    def _check_quality_gates(self, results: Dict, gates: List[str]) -> List[Dict]:
        """Check quality gates against results"""
        gate_results = []
        
        for gate in gates:
            if gate == "accessibility" and "a11y-auditor" in results:
                score = results["a11y-auditor"].output.get("score", 0)
                gate_results.append({
                    "gate": gate,
                    "passed": score >= 90,
                    "score": score,
                    "reason": f"Accessibility score: {score}/100"
                })
            
            elif gate == "security" and "quality-reviewer" in results:
                security = results["quality-reviewer"].output.get("security", {})
                passed = security.get("score", 0) >= 80 and not security.get("critical", [])
                gate_results.append({
                    "gate": gate,
                    "passed": passed,
                    "score": security.get("score", 0),
                    "reason": "Security review passed" if passed else "Security issues found"
                })
            
            elif gate == "type_coverage":
                # Check if TypeScript types are present
                code = results.get("code-generator", {}).output or ""
                has_types = "interface" in str(code) or "type " in str(code)
                gate_results.append({
                    "gate": gate,
                    "passed": has_types,
                    "reason": "TypeScript types present" if has_types else "Missing TypeScript types"
                })
        
        return gate_results
    
    def _synthesize_output(self, results: Dict) -> Dict:
        """Synthesize final output from all agent results"""
        return {
            "code": results.get("code-generator", {}).output,
            "accessibility": results.get("a11y-auditor", {}).output,
            "quality": results.get("quality-reviewer", {}).output,
            "design": results.get("ui-designer", {}).output,
            "motion": results.get("motion-designer", {}).output,
        }
```

---

## 4. LLM Adapter Interface

```python
# adapters/llm_adapter.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class LLMResponse:
    content: str
    token_count: int
    model: str
    finish_reason: str

class LLMAdapter(ABC):
    """Abstract adapter for LLM providers"""
    
    @abstractmethod
    def complete(
        self,
        system: str,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        stop_sequences: Optional[List[str]] = None
    ) -> LLMResponse:
        pass

# Claude adapter
class ClaudeAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key
        self.model = model
    
    def complete(self, system: str, prompt: str, **kwargs) -> LLMResponse:
        # Implementation for Anthropic API
        pass

# OpenAI adapter
class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
    
    def complete(self, system: str, prompt: str, **kwargs) -> LLMResponse:
        # Implementation for OpenAI API
        pass

# Local model adapter (Ollama, vLLM, etc.)
class LocalModelAdapter(LLMAdapter):
    def __init__(self, endpoint: str, model: str):
        self.endpoint = endpoint
        self.model = model
    
    def complete(self, system: str, prompt: str, **kwargs) -> LLMResponse:
        # Implementation for local inference
        pass
```

---

## 5. Configuration Files

### 5.1 Agent Registry

```yaml
# config/agents.yaml
registry:
  orchestrator:
    class: OrchestratorAgent
    config:
      name: ui-orchestrator
      role: orchestrator
      max_tokens: 2000
      temperature: 0.3
  
  intent-analyzer:
    class: IntentAnalyzerAgent
    config:
      name: intent-analyzer
      role: specialist
      max_tokens: 3000
      temperature: 0.5
  
  ui-designer:
    class: UIDesignerAgent
    config:
      name: ui-designer
      role: specialist
      max_tokens: 5000
      temperature: 0.7
  
  motion-designer:
    class: MotionDesignerAgent
    config:
      name: motion-designer
      role: specialist
      max_tokens: 3000
      temperature: 0.6
  
  code-generator:
    class: CodeGeneratorAgent
    config:
      name: code-generator
      role: specialist
      max_tokens: 10000
      temperature: 0.2
  
  a11y-auditor:
    class: AccessibilityAuditorAgent
    config:
      name: a11y-auditor
      role: validator
      max_tokens: 3000
      temperature: 0.1
  
  quality-reviewer:
    class: QualityReviewerAgent
    config:
      name: quality-reviewer
      role: validator
      max_tokens: 3000
      temperature: 0.1

defaults:
  llm_provider: claude
  model: claude-sonnet-4-20250514
  fallback_provider: openai
  fallback_model: gpt-4
```

---

*Document Version: 1.0*
*Compatibility: Claude Code, Cursor, VS Code, any MCP-compatible environment*
*Last Updated: November 2025*
