# Generative UI Orchestration Framework

*Multi-agent coordination for autonomous UI generation*

---

## Overview

This framework defines how multiple specialized agents coordinate to generate production-quality UI. It is designed to work within Claude Code, Cursor, or any MCP-compatible environment, and is LLM-agnostic.

---

## 1. Orchestration Patterns

### 1.1 Pipeline Pattern

Sequential execution where each agent's output feeds the next.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      PIPELINE PATTERN                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  User Request                                                           │
│       │                                                                 │
│       ↓                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐ │
│  │  INTENT    │───→│    UI      │───→│   CODE     │───→│  QUALITY   │ │
│  │  ANALYZER  │    │  DESIGNER  │    │ GENERATOR  │    │  REVIEWER  │ │
│  └────────────┘    └────────────┘    └────────────┘    └────────────┘ │
│                                                                         │
│  Output: Sequential refinement, each stage adds detail                  │
│  Use when: Clear, well-defined requirements                             │
│  Budget: O(n) where n = number of agents                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
class PipelineOrchestrator:
    """Execute agents in sequence, passing output forward"""
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
    
    async def execute(
        self, 
        request: str, 
        context: AgentContext
    ) -> OrchestrationResult:
        current_input = {"user_request": request}
        results = []
        
        for agent in self.agents:
            # Execute agent
            result = await agent.process(current_input, context)
            results.append(result)
            
            # Check for failure
            if not result.success:
                return OrchestrationResult(
                    success=False,
                    results=results,
                    error=f"Pipeline failed at {agent.config.name}"
                )
            
            # Prepare input for next agent
            current_input = {
                **current_input,
                agent.config.name: result.output
            }
        
        return OrchestrationResult(success=True, results=results)
```

### 1.2 Fan-Out/Fan-In Pattern

Parallel execution with result aggregation.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FAN-OUT / FAN-IN PATTERN                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  User Request                                                           │
│       │                                                                 │
│       ↓                                                                 │
│  ┌────────────┐                                                         │
│  │ DISPATCHER │                                                         │
│  └────────────┘                                                         │
│       │                                                                 │
│       ├──────────────┬──────────────┐                                  │
│       ↓              ↓              ↓                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐                                │
│  │ AGENT  │    │ AGENT  │    │ AGENT  │   (Parallel)                   │
│  │   A    │    │   B    │    │   C    │                                │
│  └────────┘    └────────┘    └────────┘                                │
│       │              │              │                                   │
│       └──────────────┴──────────────┘                                  │
│                      ↓                                                  │
│              ┌────────────┐                                             │
│              │ AGGREGATOR │                                             │
│              └────────────┘                                             │
│                      ↓                                                  │
│              Combined Result                                            │
│                                                                         │
│  Output: Multiple perspectives combined                                 │
│  Use when: Independent analysis tasks, validation                       │
│  Budget: O(max(agent_budgets)) + aggregation                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
class FanOutOrchestrator:
    """Execute agents in parallel and aggregate results"""
    
    def __init__(self, agents: List[BaseAgent], aggregator: AggregatorAgent):
        self.agents = agents
        self.aggregator = aggregator
    
    async def execute(
        self, 
        request: str, 
        context: AgentContext
    ) -> OrchestrationResult:
        # Fan out: Execute all agents in parallel
        tasks = [
            agent.process({"user_request": request}, context)
            for agent in self.agents
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle failures
        successful_results = [
            (agent.config.name, r) 
            for agent, r in zip(self.agents, results)
            if isinstance(r, AgentResult) and r.success
        ]
        
        if not successful_results:
            return OrchestrationResult(
                success=False,
                error="All parallel agents failed"
            )
        
        # Fan in: Aggregate results
        aggregated = await self.aggregator.process(
            {"results": dict(successful_results)},
            context
        )
        
        return OrchestrationResult(
            success=aggregated.success,
            results=results,
            aggregated=aggregated.output
        )
```

### 1.3 Hierarchical Pattern

Orchestrator delegates to sub-orchestrators.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HIERARCHICAL PATTERN                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  User Request                                                           │
│       │                                                                 │
│       ↓                                                                 │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    ROOT ORCHESTRATOR                           │    │
│  │  - Task decomposition                                          │    │
│  │  - Sub-task routing                                            │    │
│  │  - Result synthesis                                            │    │
│  └────────────────────────────────────────────────────────────────┘    │
│       │                                                                 │
│       ├──────────────────────┬──────────────────────┐                  │
│       ↓                      ↓                      ↓                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│  │ UI DESIGN    │    │   MOTION     │    │ VALIDATION   │             │
│  │ ORCHESTRATOR │    │ ORCHESTRATOR │    │ ORCHESTRATOR │             │
│  └──────────────┘    └──────────────┘    └──────────────┘             │
│       │                      │                      │                  │
│   ┌───┴───┐              ┌───┴───┐              ┌───┴───┐             │
│   ↓       ↓              ↓       ↓              ↓       ↓             │
│ ┌───┐   ┌───┐         ┌───┐   ┌───┐         ┌───┐   ┌───┐            │
│ │ A │   │ B │         │ C │   │ D │         │ E │   │ F │            │
│ └───┘   └───┘         └───┘   └───┘         └───┘   └───┘            │
│                                                                         │
│  Output: Complex task decomposition with specialized handling           │
│  Use when: Enterprise-grade, multi-domain tasks                         │
│  Budget: O(depth * breadth)                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
class HierarchicalOrchestrator:
    """Multi-level orchestration with sub-orchestrators"""
    
    def __init__(self, sub_orchestrators: Dict[str, BaseOrchestrator]):
        self.sub_orchestrators = sub_orchestrators
    
    async def execute(
        self, 
        request: str, 
        context: AgentContext
    ) -> OrchestrationResult:
        # Decompose task into sub-tasks
        sub_tasks = await self.decompose_task(request)
        
        # Route sub-tasks to appropriate orchestrators
        results = {}
        for task in sub_tasks:
            orchestrator = self.sub_orchestrators.get(task.domain)
            if orchestrator:
                result = await orchestrator.execute(task.description, context)
                results[task.id] = result
        
        # Synthesize results
        final_output = await self.synthesize_results(results)
        
        return OrchestrationResult(
            success=all(r.success for r in results.values()),
            results=results,
            output=final_output
        )
    
    async def decompose_task(self, request: str) -> List[SubTask]:
        """Decompose request into domain-specific sub-tasks"""
        # Use LLM to analyze and decompose
        pass
    
    async def synthesize_results(self, results: Dict) -> Any:
        """Combine sub-orchestrator results into final output"""
        # Use LLM to synthesize
        pass
```

### 1.4 Iterative Refinement Pattern

Repeated cycles until quality threshold met.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   ITERATIVE REFINEMENT PATTERN                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  User Request                                                           │
│       │                                                                 │
│       ↓                                                                 │
│  ┌────────────┐                                                         │
│  │ GENERATOR  │◄─────────────────────────────┐                          │
│  └────────────┘                              │                          │
│       │                                      │                          │
│       ↓                                      │ Feedback                 │
│  ┌────────────┐                              │                          │
│  │  REVIEWER  │──── Quality OK? ─── NO ──────┘                          │
│  └────────────┘                                                         │
│       │                                                                 │
│       YES                                                               │
│       ↓                                                                 │
│  Final Output                                                           │
│                                                                         │
│  Output: Progressively refined result                                   │
│  Use when: Quality is critical, creative tasks                          │
│  Budget: O(iterations * agent_cost)                                     │
│  Max iterations: 3-5 to prevent infinite loops                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
class IterativeOrchestrator:
    """Refine output until quality threshold met"""
    
    def __init__(
        self, 
        generator: BaseAgent, 
        reviewer: BaseAgent,
        max_iterations: int = 3,
        quality_threshold: float = 0.9
    ):
        self.generator = generator
        self.reviewer = reviewer
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
    
    async def execute(
        self, 
        request: str, 
        context: AgentContext
    ) -> OrchestrationResult:
        current_output = None
        feedback = None
        iterations = []
        
        for i in range(self.max_iterations):
            # Generate (or refine)
            gen_input = {
                "user_request": request,
                "previous_output": current_output,
                "feedback": feedback
            }
            gen_result = await self.generator.process(gen_input, context)
            
            if not gen_result.success:
                return OrchestrationResult(
                    success=False,
                    error=f"Generation failed at iteration {i}"
                )
            
            current_output = gen_result.output
            
            # Review
            review_result = await self.reviewer.process(
                {"code": current_output},
                context
            )
            
            quality_score = review_result.output.get("score", 0)
            
            iterations.append({
                "iteration": i,
                "quality_score": quality_score,
                "issues": review_result.output.get("issues", [])
            })
            
            # Check quality threshold
            if quality_score >= self.quality_threshold:
                return OrchestrationResult(
                    success=True,
                    output=current_output,
                    metadata={"iterations": iterations}
                )
            
            # Prepare feedback for next iteration
            feedback = self._format_feedback(review_result.output)
        
        # Max iterations reached
        return OrchestrationResult(
            success=True,  # Return best effort
            output=current_output,
            warnings=["Max iterations reached without meeting quality threshold"],
            metadata={"iterations": iterations}
        )
    
    def _format_feedback(self, review: Dict) -> str:
        """Format review output as actionable feedback"""
        issues = review.get("issues", [])
        return "\n".join([
            f"- {issue['severity']}: {issue['message']}"
            for issue in issues
        ])
```

---

## 2. Context Management

### 2.1 Context Structure

```python
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

@dataclass
class ExecutionContext:
    """Shared context across all agents in an orchestration"""
    
    # Identification
    session_id: str
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    
    # Request
    original_request: str = ""
    parsed_requirements: Dict[str, Any] = field(default_factory=dict)
    
    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)
    
    # Accumulated results
    agent_results: Dict[str, AgentResult] = field(default_factory=dict)
    
    # Budget tracking
    token_budget: int = 50000
    tokens_used: int = 0
    
    # Checkpoints for recovery
    checkpoints: List[Dict] = field(default_factory=list)
    
    # Timing
    started_at: datetime = field(default_factory=datetime.utcnow)
    
    # Quality tracking
    quality_scores: Dict[str, float] = field(default_factory=dict)
    
    @property
    def tokens_remaining(self) -> int:
        return max(0, self.token_budget - self.tokens_used)
    
    @property
    def budget_utilization(self) -> float:
        return self.tokens_used / self.token_budget if self.token_budget > 0 else 0
    
    def add_result(self, agent_name: str, result: AgentResult) -> None:
        """Add agent result and update token usage"""
        self.agent_results[agent_name] = result
        self.tokens_used += result.tokens_used
    
    def checkpoint(self, label: str) -> None:
        """Create checkpoint for recovery"""
        self.checkpoints.append({
            "label": label,
            "timestamp": datetime.utcnow().isoformat(),
            "tokens_used": self.tokens_used,
            "agents_completed": list(self.agent_results.keys())
        })
    
    def get_result(self, agent_name: str) -> Optional[Any]:
        """Get output from a specific agent"""
        result = self.agent_results.get(agent_name)
        return result.output if result else None
```

### 2.2 Context Passing

```python
class ContextManager:
    """Manage context passing between agents"""
    
    @staticmethod
    def prepare_input(
        agent_name: str,
        context: ExecutionContext
    ) -> Dict[str, Any]:
        """Prepare input for an agent based on context"""
        
        # Base input
        input_data = {
            "user_request": context.original_request,
            "requirements": context.parsed_requirements,
            "config": context.config
        }
        
        # Agent-specific context
        dependencies = AGENT_DEPENDENCIES.get(agent_name, [])
        for dep in dependencies:
            if dep in context.agent_results:
                input_data[dep] = context.get_result(dep)
        
        return input_data

# Agent dependency graph
AGENT_DEPENDENCIES = {
    "intent-analyzer": [],
    "ui-designer": ["intent-analyzer"],
    "motion-designer": ["ui-designer"],
    "code-generator": ["ui-designer", "motion-designer"],
    "a11y-auditor": ["code-generator"],
    "quality-reviewer": ["code-generator"],
}
```

---

## 3. Budget Management

### 3.1 Token Budget Allocation

```python
from dataclasses import dataclass
from typing import Dict
from enum import Enum

class BudgetStrategy(Enum):
    FIXED = "fixed"      # Fixed allocation per agent
    DYNAMIC = "dynamic"  # Allocate based on task complexity
    ADAPTIVE = "adaptive"  # Adjust during execution

@dataclass
class BudgetAllocation:
    """Budget allocation for orchestration"""
    
    total: int
    allocations: Dict[str, int]
    strategy: BudgetStrategy
    reserve: float = 0.1  # 10% reserve for retries

class BudgetManager:
    """Manage token budgets across orchestration"""
    
    # Default allocations (percentage of total)
    DEFAULT_ALLOCATIONS = {
        "intent-analyzer": 0.05,
        "ui-designer": 0.15,
        "motion-designer": 0.10,
        "code-generator": 0.40,
        "a11y-auditor": 0.10,
        "quality-reviewer": 0.10,
        "reserve": 0.10
    }
    
    def __init__(self, total_budget: int, strategy: BudgetStrategy):
        self.total_budget = total_budget
        self.strategy = strategy
        self.allocations = self._calculate_allocations()
        self.usage = {agent: 0 for agent in self.allocations}
    
    def _calculate_allocations(self) -> Dict[str, int]:
        """Calculate token allocations per agent"""
        return {
            agent: int(self.total_budget * percentage)
            for agent, percentage in self.DEFAULT_ALLOCATIONS.items()
        }
    
    def request_budget(self, agent_name: str, requested: int) -> int:
        """Request budget for an agent, return granted amount"""
        allocated = self.allocations.get(agent_name, 0)
        used = self.usage.get(agent_name, 0)
        available = allocated - used
        
        if self.strategy == BudgetStrategy.FIXED:
            # Strict allocation
            granted = min(requested, available)
        
        elif self.strategy == BudgetStrategy.DYNAMIC:
            # Can borrow from reserve
            if requested > available:
                reserve_available = self.allocations["reserve"] - self.usage.get("reserve", 0)
                granted = min(requested, available + reserve_available)
                if granted > available:
                    self.usage["reserve"] = self.usage.get("reserve", 0) + (granted - available)
            else:
                granted = requested
        
        else:  # ADAPTIVE
            # Can borrow from any unused allocation
            total_available = sum(
                self.allocations[a] - self.usage[a]
                for a in self.allocations
            )
            granted = min(requested, total_available)
        
        return granted
    
    def record_usage(self, agent_name: str, tokens: int) -> None:
        """Record actual token usage"""
        self.usage[agent_name] = self.usage.get(agent_name, 0) + tokens
    
    def get_summary(self) -> Dict:
        """Get budget utilization summary"""
        return {
            agent: {
                "allocated": self.allocations.get(agent, 0),
                "used": self.usage.get(agent, 0),
                "utilization": self.usage.get(agent, 0) / self.allocations.get(agent, 1)
            }
            for agent in self.allocations
        }
```

### 3.2 Cost Estimation

```python
class CostEstimator:
    """Estimate token costs before execution"""
    
    # Average tokens per task type
    TASK_ESTIMATES = {
        "simple_component": {"input": 500, "output": 1500},
        "complex_component": {"input": 1000, "output": 3000},
        "layout": {"input": 800, "output": 4000},
        "form": {"input": 600, "output": 2500},
        "wizard": {"input": 1200, "output": 6000},
        "dashboard": {"input": 1500, "output": 8000},
    }
    
    # Agent overhead multipliers
    AGENT_MULTIPLIERS = {
        "intent-analyzer": 0.1,
        "ui-designer": 0.2,
        "motion-designer": 0.15,
        "code-generator": 1.0,
        "a11y-auditor": 0.15,
        "quality-reviewer": 0.15,
    }
    
    @classmethod
    def estimate(
        cls,
        task_type: str,
        agents: List[str],
        complexity_factor: float = 1.0
    ) -> Dict[str, int]:
        """Estimate tokens for a task"""
        base = cls.TASK_ESTIMATES.get(task_type, cls.TASK_ESTIMATES["simple_component"])
        
        estimates = {}
        for agent in agents:
            multiplier = cls.AGENT_MULTIPLIERS.get(agent, 0.1)
            estimates[agent] = {
                "input": int(base["input"] * multiplier * complexity_factor),
                "output": int(base["output"] * multiplier * complexity_factor),
                "total": int((base["input"] + base["output"]) * multiplier * complexity_factor)
            }
        
        estimates["total"] = sum(e["total"] for e in estimates.values())
        return estimates
```

---

## 4. Error Handling & Recovery

### 4.1 Error Classification

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class ErrorSeverity(Enum):
    RECOVERABLE = "recoverable"  # Can retry or skip
    DEGRADED = "degraded"        # Continue with reduced quality
    FATAL = "fatal"              # Must abort

class ErrorCategory(Enum):
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    VALIDATION = "validation"
    BUDGET_EXCEEDED = "budget_exceeded"
    QUALITY_THRESHOLD = "quality_threshold"
    LLM_ERROR = "llm_error"
    UNKNOWN = "unknown"

@dataclass
class OrchestrationError:
    """Structured error for orchestration"""
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    agent: Optional[str] = None
    recoverable: bool = True
    retry_after: Optional[int] = None  # Seconds
    
    @classmethod
    def from_exception(cls, e: Exception, agent: str) -> "OrchestrationError":
        """Create error from exception"""
        if "rate limit" in str(e).lower():
            return cls(
                category=ErrorCategory.RATE_LIMIT,
                severity=ErrorSeverity.RECOVERABLE,
                message=str(e),
                agent=agent,
                recoverable=True,
                retry_after=60
            )
        elif "timeout" in str(e).lower():
            return cls(
                category=ErrorCategory.TIMEOUT,
                severity=ErrorSeverity.RECOVERABLE,
                message=str(e),
                agent=agent,
                recoverable=True
            )
        else:
            return cls(
                category=ErrorCategory.UNKNOWN,
                severity=ErrorSeverity.DEGRADED,
                message=str(e),
                agent=agent
            )
```

### 4.2 Recovery Strategies

```python
from abc import ABC, abstractmethod
import asyncio

class RecoveryStrategy(ABC):
    """Base class for recovery strategies"""
    
    @abstractmethod
    async def recover(
        self,
        error: OrchestrationError,
        context: ExecutionContext,
        agent: BaseAgent
    ) -> Optional[AgentResult]:
        pass

class RetryStrategy(RecoveryStrategy):
    """Retry with exponential backoff"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def recover(
        self,
        error: OrchestrationError,
        context: ExecutionContext,
        agent: BaseAgent
    ) -> Optional[AgentResult]:
        if not error.recoverable:
            return None
        
        for attempt in range(self.max_retries):
            delay = self.base_delay * (2 ** attempt)
            
            if error.retry_after:
                delay = max(delay, error.retry_after)
            
            await asyncio.sleep(delay)
            
            try:
                input_data = ContextManager.prepare_input(agent.config.name, context)
                return await agent.process(input_data, context)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return None
                continue
        
        return None

class FallbackStrategy(RecoveryStrategy):
    """Use fallback agent or default output"""
    
    def __init__(self, fallback_agent: Optional[BaseAgent] = None):
        self.fallback_agent = fallback_agent
    
    async def recover(
        self,
        error: OrchestrationError,
        context: ExecutionContext,
        agent: BaseAgent
    ) -> Optional[AgentResult]:
        if self.fallback_agent:
            input_data = ContextManager.prepare_input(
                self.fallback_agent.config.name,
                context
            )
            return await self.fallback_agent.process(input_data, context)
        
        # Return degraded default
        return AgentResult(
            success=True,
            output=self._get_default_output(agent.config.name),
            tokens_used=0,
            warnings=[f"Using default output due to {error.category.value}"]
        )
    
    def _get_default_output(self, agent_name: str) -> Any:
        """Get safe default output for an agent"""
        defaults = {
            "motion-designer": {"animations": [], "tokens": {}},
            "a11y-auditor": {"score": 0, "issues": [], "skipped": True},
            "quality-reviewer": {"score": 0, "issues": [], "skipped": True},
        }
        return defaults.get(agent_name, {})

class SkipStrategy(RecoveryStrategy):
    """Skip the failed agent and continue"""
    
    async def recover(
        self,
        error: OrchestrationError,
        context: ExecutionContext,
        agent: BaseAgent
    ) -> Optional[AgentResult]:
        return AgentResult(
            success=True,
            output=None,
            tokens_used=0,
            warnings=[f"Agent {agent.config.name} skipped: {error.message}"]
        )
```

### 4.3 Circuit Breaker

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable, Any
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

@dataclass
class CircuitBreaker:
    """Prevent cascading failures"""
    
    failure_threshold: int = 3
    recovery_timeout: float = 60.0
    half_open_requests: int = 1
    
    def __post_init__(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.success_count = 0
    
    async def call(
        self,
        func: Callable[..., Any],
        *args,
        **kwargs
    ) -> Any:
        """Execute function with circuit breaker protection"""
        
        # Check if circuit should transition
        self._check_state_transition()
        
        if self.state == CircuitState.OPEN:
            raise CircuitOpenError(
                f"Circuit breaker open, retry after {self.recovery_timeout}s"
            )
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _check_state_transition(self) -> None:
        """Check if state should transition"""
        if self.state == CircuitState.OPEN:
            if self.last_failure_time:
                elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
                if elapsed >= self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
    
    def _on_success(self) -> None:
        """Handle successful call"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_requests:
                self.state = CircuitState.CLOSED
    
    def _on_failure(self) -> None:
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

class CircuitOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass
```

---

## 5. Quality Gates

### 5.1 Gate Definitions

```python
from dataclasses import dataclass
from typing import Callable, Any, List
from enum import Enum

class GateSeverity(Enum):
    BLOCKING = "blocking"      # Must pass to continue
    WARNING = "warning"        # Log warning, continue
    INFORMATIONAL = "info"     # Log only

@dataclass
class QualityGate:
    """Definition of a quality gate"""
    
    name: str
    description: str
    severity: GateSeverity
    check: Callable[[ExecutionContext], bool]
    threshold: Any
    
    def evaluate(self, context: ExecutionContext) -> "GateResult":
        """Evaluate the gate"""
        try:
            passed = self.check(context)
            return GateResult(
                gate=self,
                passed=passed,
                actual_value=self._get_actual_value(context),
                message=self._get_message(passed)
            )
        except Exception as e:
            return GateResult(
                gate=self,
                passed=False,
                error=str(e)
            )
    
    def _get_actual_value(self, context: ExecutionContext) -> Any:
        """Override to get actual value for reporting"""
        return None
    
    def _get_message(self, passed: bool) -> str:
        """Generate result message"""
        if passed:
            return f"{self.name}: PASSED"
        return f"{self.name}: FAILED (threshold: {self.threshold})"

@dataclass
class GateResult:
    """Result of gate evaluation"""
    gate: QualityGate
    passed: bool
    actual_value: Any = None
    error: Optional[str] = None
    message: str = ""

# Pre-defined gates
QUALITY_GATES = {
    "accessibility": QualityGate(
        name="accessibility",
        description="Component meets WCAG accessibility standards",
        severity=GateSeverity.BLOCKING,
        check=lambda ctx: ctx.quality_scores.get("a11y", 0) >= 90,
        threshold=90
    ),
    
    "typescript_coverage": QualityGate(
        name="typescript_coverage",
        description="Full TypeScript type coverage",
        severity=GateSeverity.BLOCKING,
        check=lambda ctx: "interface" in str(ctx.get_result("code-generator")),
        threshold="100%"
    ),
    
    "no_critical_security": QualityGate(
        name="no_critical_security",
        description="No critical security issues",
        severity=GateSeverity.BLOCKING,
        check=lambda ctx: not ctx.quality_scores.get("security_critical", False),
        threshold=0
    ),
    
    "performance_score": QualityGate(
        name="performance_score",
        description="Meets performance requirements",
        severity=GateSeverity.WARNING,
        check=lambda ctx: ctx.quality_scores.get("performance", 0) >= 80,
        threshold=80
    ),
    
    "documentation": QualityGate(
        name="documentation",
        description="Component is documented",
        severity=GateSeverity.INFORMATIONAL,
        check=lambda ctx: "/**" in str(ctx.get_result("code-generator")),
        threshold="JSDoc present"
    ),
}
```

### 5.2 Gate Evaluation

```python
class GateEvaluator:
    """Evaluate quality gates for an orchestration"""
    
    def __init__(self, gates: List[QualityGate]):
        self.gates = gates
    
    def evaluate_all(self, context: ExecutionContext) -> "GateEvaluationResult":
        """Evaluate all gates"""
        results = [gate.evaluate(context) for gate in self.gates]
        
        blocking_failures = [
            r for r in results
            if not r.passed and r.gate.severity == GateSeverity.BLOCKING
        ]
        
        warnings = [
            r for r in results
            if not r.passed and r.gate.severity == GateSeverity.WARNING
        ]
        
        return GateEvaluationResult(
            results=results,
            passed=len(blocking_failures) == 0,
            blocking_failures=blocking_failures,
            warnings=warnings
        )

@dataclass
class GateEvaluationResult:
    """Result of evaluating all gates"""
    results: List[GateResult]
    passed: bool
    blocking_failures: List[GateResult]
    warnings: List[GateResult]
    
    def to_report(self) -> str:
        """Generate human-readable report"""
        lines = ["Quality Gate Evaluation", "=" * 40]
        
        for result in self.results:
            status = "✓" if result.passed else "✗"
            lines.append(f"{status} {result.gate.name}: {result.message}")
        
        lines.append("")
        lines.append(f"Overall: {'PASSED' if self.passed else 'FAILED'}")
        
        if self.blocking_failures:
            lines.append("")
            lines.append("Blocking failures:")
            for failure in self.blocking_failures:
                lines.append(f"  - {failure.gate.name}: {failure.message}")
        
        return "\n".join(lines)
```

---

## 6. Configuration

### Orchestration Config File

```yaml
# .ui-gen/orchestration.yaml

version: 1

# Orchestration pattern
pattern: pipeline  # pipeline | fan_out | hierarchical | iterative

# Agent pipeline (order matters for pipeline pattern)
agents:
  - intent-analyzer
  - ui-designer
  - motion-designer
  - code-generator
  - a11y-auditor
  - quality-reviewer

# Budget configuration
budget:
  total: 50000
  strategy: dynamic  # fixed | dynamic | adaptive
  reserve: 0.1  # 10% reserve

# Quality gates
quality_gates:
  - accessibility
  - typescript_coverage
  - no_critical_security
  - performance_score

# Error handling
error_handling:
  max_retries: 3
  backoff_base: 1.0
  circuit_breaker:
    failure_threshold: 3
    recovery_timeout: 60
  fallback_strategy: skip  # retry | fallback | skip | abort

# Iterative refinement (if pattern = iterative)
iterative:
  max_iterations: 3
  quality_threshold: 0.9

# Parallelization (if pattern = fan_out)
parallel:
  max_concurrent: 5
  timeout: 30
```

---

*Document Version: 1.0*
*Compatibility: Python 3.9+, asyncio-based*
*Last Updated: November 2025*
