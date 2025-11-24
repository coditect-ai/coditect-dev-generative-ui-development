# Framework Knowledge Registration System

**Status:** Design Phase
**Version:** 1.0.0
**Date:** November 23, 2025
**Phase:** Phase 2C - LLM Framework Awareness

---

## Overview

The Framework Knowledge Registration System makes LLMs aware of CODITECT's 180 components (53 agents, 27 skills, 79 commands, 21 scripts) to enable intelligent recommendations, proper invocations, and automated workflows.

**Problem:**
- LLMs don't know what agents exist or when to use them
- LLMs don't know available skills, commands, or scripts
- LLMs can't recommend optimal workflows
- Users must manually specify which components to use

**Solution:**
Three-tier knowledge system:
1. **Structured Metadata Files** - Machine-readable component registry
2. **System Prompt Templates** - Core framework knowledge injection
3. **RAG (Future)** - Dynamic knowledge retrieval for deep queries

---

## Architecture

```
User Request
     ↓
TaskExecutor
     ↓
FrameworkKnowledgeLoader ← Loads component metadata
     ↓
SystemPromptBuilder ← Injects framework knowledge
     ↓
AgentLlmConfig ← Gets LLM provider
     ↓
LlmFactory
     ↓
LLM Provider (with framework awareness)
     ↓
Response (with component recommendations)
```

---

## Tier 1: Structured Metadata Files

### Component Registry Schema

**Location:** `.coditect/config/framework-registry.json`

```json
{
  "framework_version": "1.0.0",
  "last_updated": "2025-11-23",
  "components": {
    "agents": {
      "total": 53,
      "categories": {
        "project_lifecycle": [...],
        "research_analysis": [...],
        "coordination": [...],
        "development": [...],
        "database": [...],
        "ai_analysis": [...],
        "infrastructure": [...],
        "testing_qa": [...],
        "documentation": [...],
        "architecture": [...],
        "business_intelligence": [...],
        "educational": [...]
      }
    },
    "skills": {
      "total": 27,
      "list": [...]
    },
    "commands": {
      "total": 79,
      "categories": {
        "project_creation": [...],
        "development": [...],
        "analysis": [...],
        "deployment": [...]
      }
    },
    "scripts": {
      "total": 21,
      "list": [...]
    }
  }
}
```

### Individual Component Metadata

**Agent Metadata Example:**

```json
{
  "id": "ai-specialist",
  "name": "AI Specialist",
  "category": "ai_analysis",
  "description": "Multi-provider AI routing specialist for intelligent model selection",
  "capabilities": [
    "Model selection based on task requirements",
    "Prompt optimization",
    "Cost-optimized routing",
    "Provider fallback strategies"
  ],
  "use_cases": [
    "Complex reasoning requiring premium models",
    "AI strategy decisions",
    "Model performance comparison"
  ],
  "typical_invocation": "Task(subagent_type='general-purpose', prompt='Use ai-specialist subagent to select optimal LLM for code generation task')",
  "llm_binding": {
    "provider": "anthropic-claude",
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "estimated_cost_per_task": "$0.012",
  "tags": ["ai", "routing", "optimization", "premium"]
}
```

**Skill Metadata Example:**

```json
{
  "id": "production-patterns",
  "name": "Production Patterns",
  "description": "Production-ready code patterns including circuit breakers, error handling, observability hooks",
  "provides": [
    "Circuit breaker implementations",
    "Async error handling patterns",
    "Observability hooks (Prometheus, Jaeger)",
    "Fault tolerance strategies"
  ],
  "use_cases": [
    "Building resilient production systems",
    "Implementing error recovery",
    "Adding observability"
  ],
  "activation": "Skill(skill='production-patterns')",
  "tags": ["production", "resilience", "observability"]
}
```

**Command Metadata Example:**

```json
{
  "id": "new-project",
  "name": "/new-project",
  "description": "Complete project creation workflow from discovery to production-ready structure",
  "syntax": "/new-project \"<project description>\"",
  "workflow": [
    "Interactive discovery interview",
    "Git infrastructure setup",
    "PROJECT-PLAN.md generation",
    "Production-ready directory structure",
    "Starter templates and configuration"
  ],
  "example": "/new-project \"Build an API for team project management\"",
  "typical_duration": "5-10 minutes",
  "agents_invoked": [
    "project-discovery-specialist",
    "submodule-orchestrator",
    "software-design-document-specialist",
    "project-structure-optimizer"
  ],
  "tags": ["project-creation", "workflow", "automation"]
}
```

**Script Metadata Example:**

```json
{
  "id": "create-checkpoint",
  "name": "create-checkpoint.py",
  "path": ".coditect/scripts/create-checkpoint.py",
  "description": "Create session checkpoint with conversation export and deduplication",
  "usage": "python3 .coditect/scripts/create-checkpoint.py \"<description>\" --auto-commit",
  "arguments": [
    {"name": "description", "required": true, "type": "string"},
    {"name": "--auto-commit", "required": false, "type": "flag"}
  ],
  "output": "MEMORY-CONTEXT/checkpoints/<checkpoint-file>.md",
  "tags": ["memory", "session", "automation"]
}
```

---

## Tier 2: System Prompt Templates

### Core Framework Prompt

**Location:** `.coditect/config/system-prompts/framework-core.txt`

```
You are working within the AZ1.AI CODITECT framework - a comprehensive project management and development platform with 180 specialized components.

## Available Resources

**53 Specialized Agents** across 12 categories:
- Project Lifecycle (4): project-discovery-specialist, project-structure-optimizer, project-organizer, submodule-orchestrator
- Research & Analysis (7): competitive-market-analyst, web-search-researcher, codebase-analyzer, codebase-locator, codebase-pattern-finder, thoughts-analyzer, thoughts-locator
- Coordination (3): orchestrator, orchestrator-code-review, orchestrator-detailed-backup
- Development (8): rust-expert-developer, rust-qa-specialist, frontend-react-typescript-expert, actix-web-specialist, websocket-protocol-designer, wasm-optimization-expert, terminal-integration-specialist, script-utility-analyzer
- Database (2): foundationdb-expert, database-architect
- AI Analysis (5): ai-specialist, novelty-detection-specialist, prompt-analyzer-specialist, skill-quality-enhancer, research-agent
- Infrastructure (6): cloud-architect, cloud-architect-code-reviewer, monitoring-specialist, k8s-statefulset-specialist, multi-tenant-architect, devops-engineer
- Testing & QA (4): testing-specialist, qa-reviewer, security-specialist, adr-compliance-specialist
- Documentation (1): documentation-librarian
- Architecture (4): senior-architect, software-design-architect, software-design-document-specialist, coditect-adr-specialist
- Business Intelligence (2): business-intelligence-analyst, venture-capital-business-analyst
- Educational (3): ai-curriculum-specialist, educational-content-generator, assessment-creation-agent

**27 Production Skills** including:
- Project management: submodule-setup, submodule-validation, submodule-configuration, submodule-health, submodule-orchestrator
- Development patterns: production-patterns, rust-backend-patterns, framework-patterns
- Documentation: cross-file-documentation-update, documentation-librarian
- Automation: git-workflow-automation, build-deploy-workflow, code-editor

**79 Slash Commands** for:
- Project creation: /new-project
- Development: /implement, /analyze, /optimize, /prototype
- Research: /research, /multi-agent-research
- Deployment: /build-deploy-workflow
- Planning: /strategy, /deliberation

**21 Python Scripts** for automation in `.coditect/scripts/`

## Agent Invocation Pattern

**CRITICAL**: Use the Task tool to invoke specialized agents:

```python
# Correct invocation
Task(subagent_type="general-purpose", prompt="Use <agent-name> subagent to <task>")

# Examples:
Task(subagent_type="general-purpose", prompt="Use ai-specialist subagent to select optimal LLM for this code generation task")
Task(subagent_type="general-purpose", prompt="Use rust-expert-developer subagent to implement async WebSocket server with Actix-web")
```

## When to Recommend Components

**For New Projects**: Use /new-project command or project-discovery-specialist agent
**For Code Analysis**: Use codebase-analyzer, codebase-locator, or codebase-pattern-finder agents
**For Research**: Use web-search-researcher or research-agent
**For Complex Workflows**: Use orchestrator agent to coordinate multiple agents
**For Documentation**: Use documentation-librarian agent or /document command
**For Deployment**: Use /build-deploy-workflow or cloud-architect agent

## Framework Context

Current directory has CODITECT framework accessible via:
- `.coditect/` - Master framework directory
- `.claude/` - Symlink to .coditect for Claude Code compatibility

Framework documentation available in:
- `.coditect/docs/` - Comprehensive documentation
- `.coditect/AGENT-INDEX.md` - Complete agent catalog
- `.coditect/COMPLETE-INVENTORY.md` - All 180 components

Use this framework knowledge to provide optimal recommendations and workflows.
```

### Task-Specific Prompt Templates

**Location:** `.coditect/config/system-prompts/`

- `task-code-generation.txt` - Prompt for code generation tasks
- `task-research.txt` - Prompt for research tasks
- `task-architecture.txt` - Prompt for architecture tasks
- `task-deployment.txt` - Prompt for deployment tasks
- `task-documentation.txt` - Prompt for documentation tasks

---

## Tier 3: Implementation

### FrameworkKnowledgeLoader Class

**Location:** `llm_abstractions/framework_knowledge.py`

```python
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
from dataclasses import dataclass, field


@dataclass
class ComponentMetadata:
    """Metadata for a single framework component."""

    id: str
    name: str
    category: str
    description: str
    capabilities: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FrameworkRegistry:
    """Complete framework component registry."""

    framework_version: str
    last_updated: str
    agents: Dict[str, ComponentMetadata]
    skills: Dict[str, ComponentMetadata]
    commands: Dict[str, ComponentMetadata]
    scripts: Dict[str, ComponentMetadata]


class FrameworkKnowledgeLoader:
    """
    Loads framework component metadata and system prompt templates.

    Singleton pattern for efficient knowledge loading.
    """

    _instance: Optional['FrameworkKnowledgeLoader'] = None

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize knowledge loader."""
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = self._find_config_dir()

        self.registry: Optional[FrameworkRegistry] = None
        self.system_prompts: Dict[str, str] = {}

        # Load on initialization
        self._load_registry()
        self._load_system_prompts()

    @classmethod
    def get_instance(cls, config_dir: Optional[Path] = None) -> 'FrameworkKnowledgeLoader':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls(config_dir)
        return cls._instance

    def _find_config_dir(self) -> Path:
        """Find .coditect/config directory."""
        candidates = [
            Path(".coditect/config"),
            Path(".claude/config"),
            Path("../coditect-core/.coditect/config"),
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()

        return Path(".coditect/config")

    def _load_registry(self):
        """Load framework component registry from JSON."""
        registry_file = self.config_dir / "framework-registry.json"

        if not registry_file.exists():
            print(f"⚠️  Framework registry not found: {registry_file}")
            return

        with open(registry_file, 'r') as f:
            data = json.load(f)

        # Parse agents
        agents = {}
        for category, agent_list in data["components"]["agents"]["categories"].items():
            for agent in agent_list:
                agents[agent["id"]] = ComponentMetadata(**agent)

        # Parse skills, commands, scripts similarly...

        self.registry = FrameworkRegistry(
            framework_version=data["framework_version"],
            last_updated=data["last_updated"],
            agents=agents,
            skills={},  # TODO: Parse
            commands={},  # TODO: Parse
            scripts={}  # TODO: Parse
        )

    def _load_system_prompts(self):
        """Load system prompt templates."""
        prompt_dir = self.config_dir / "system-prompts"

        if not prompt_dir.exists():
            return

        for prompt_file in prompt_dir.glob("*.txt"):
            prompt_name = prompt_file.stem
            with open(prompt_file, 'r') as f:
                self.system_prompts[prompt_name] = f.read()

    def get_agent_metadata(self, agent_id: str) -> Optional[ComponentMetadata]:
        """Get metadata for specific agent."""
        if not self.registry:
            return None
        return self.registry.agents.get(agent_id)

    def get_system_prompt(self, prompt_type: str = "framework-core") -> str:
        """Get system prompt template."""
        return self.system_prompts.get(prompt_type, "")

    def get_component_summary(self, component_type: str = "all") -> str:
        """
        Get summary of framework components for injection into LLM context.

        Args:
            component_type: "agents", "skills", "commands", "scripts", or "all"

        Returns:
            Formatted summary string
        """
        if not self.registry:
            return ""

        summary_parts = []

        if component_type in ["agents", "all"]:
            agent_count = len(self.registry.agents)
            summary_parts.append(f"**{agent_count} Specialized Agents** available")

        if component_type in ["skills", "all"]:
            skill_count = len(self.registry.skills)
            summary_parts.append(f"**{skill_count} Production Skills** available")

        if component_type in ["commands", "all"]:
            command_count = len(self.registry.commands)
            summary_parts.append(f"**{command_count} Slash Commands** available")

        if component_type in ["scripts", "all"]:
            script_count = len(self.registry.scripts)
            summary_parts.append(f"**{script_count} Automation Scripts** available")

        return ", ".join(summary_parts)

    def recommend_agent(self, task_description: str, category: Optional[str] = None) -> List[str]:
        """
        Recommend agents for a given task.

        Simple keyword matching (Phase 2C).
        Future: Use embeddings for semantic search (Phase 3).

        Args:
            task_description: Description of the task
            category: Optional category filter

        Returns:
            List of recommended agent IDs
        """
        if not self.registry:
            return []

        keywords = task_description.lower().split()
        recommendations = []

        for agent_id, agent in self.registry.agents.items():
            # Filter by category if specified
            if category and agent.category != category:
                continue

            # Keyword matching in description, capabilities, use_cases
            text = f"{agent.description} {' '.join(agent.capabilities)} {' '.join(agent.use_cases)}".lower()

            score = sum(1 for keyword in keywords if keyword in text)

            if score > 0:
                recommendations.append((agent_id, score))

        # Sort by score descending
        recommendations.sort(key=lambda x: x[1], reverse=True)

        return [agent_id for agent_id, _ in recommendations[:5]]


# Convenience function
def get_framework_knowledge() -> FrameworkKnowledgeLoader:
    """Get framework knowledge loader instance."""
    return FrameworkKnowledgeLoader.get_instance()
```

### SystemPromptBuilder Class

**Location:** `llm_abstractions/system_prompt_builder.py`

```python
from typing import Dict, List, Optional
from .framework_knowledge import FrameworkKnowledgeLoader


class SystemPromptBuilder:
    """
    Builds context-aware system prompts with framework knowledge.
    """

    def __init__(self, knowledge_loader: Optional[FrameworkKnowledgeLoader] = None):
        """Initialize prompt builder."""
        self.knowledge = knowledge_loader or FrameworkKnowledgeLoader.get_instance()

    def build_prompt(
        self,
        task_type: str = "general",
        include_agents: bool = True,
        include_skills: bool = True,
        include_commands: bool = True,
        include_scripts: bool = False,
        custom_context: Optional[str] = None
    ) -> str:
        """
        Build system prompt with framework knowledge.

        Args:
            task_type: Type of task (general, code-generation, research, architecture, etc.)
            include_agents: Include agent catalog
            include_skills: Include skill library
            include_commands: Include command reference
            include_scripts: Include script inventory
            custom_context: Additional custom context

        Returns:
            Complete system prompt
        """
        prompt_parts = []

        # Core framework prompt
        core_prompt = self.knowledge.get_system_prompt("framework-core")
        if core_prompt:
            prompt_parts.append(core_prompt)

        # Task-specific prompt
        task_prompt = self.knowledge.get_system_prompt(f"task-{task_type}")
        if task_prompt:
            prompt_parts.append(task_prompt)

        # Component summaries
        component_types = []
        if include_agents:
            component_types.append("agents")
        if include_skills:
            component_types.append("skills")
        if include_commands:
            component_types.append("commands")
        if include_scripts:
            component_types.append("scripts")

        if component_types:
            summary = self.knowledge.get_component_summary("all")
            prompt_parts.append(f"\n## Framework Components Available\n\n{summary}")

        # Custom context
        if custom_context:
            prompt_parts.append(f"\n## Additional Context\n\n{custom_context}")

        return "\n\n".join(prompt_parts)

    def build_agent_invocation_prompt(self, agent_id: str) -> str:
        """
        Build prompt for invoking a specific agent.

        Includes agent metadata (capabilities, use cases, typical invocation).
        """
        agent_metadata = self.knowledge.get_agent_metadata(agent_id)

        if not agent_metadata:
            return f"Agent '{agent_id}' not found in framework registry."

        prompt = f"""
## Agent: {agent_metadata.name}

**Description:** {agent_metadata.description}

**Capabilities:**
{chr(10).join(f'- {cap}' for cap in agent_metadata.capabilities)}

**Typical Use Cases:**
{chr(10).join(f'- {uc}' for uc in agent_metadata.use_cases)}

**Invocation Pattern:**
```python
{agent_metadata.metadata.get('typical_invocation', f'Task(subagent_type="general-purpose", prompt="Use {agent_id} subagent to <task>")')}
```
"""
        return prompt
```

---

## Integration with TaskExecutor

### Modified `_execute_api()` Method

**Location:** `orchestration/executor.py` (lines 364-442)

```python
async def _execute_api(
    self,
    task: AgentTask,
    agent_config: AgentConfig,
    result: ExecutionResult
) -> ExecutionResult:
    """
    Execute task via direct API call with framework knowledge injection.
    """
    result.status = ExecutionStatus.IN_PROGRESS

    if LLM_ABSTRACTIONS_AVAILABLE and AGENT_LLM_CONFIG_AVAILABLE:
        try:
            agent_id = agent_config.name

            # Get agent-specific LLM configuration
            config_loader = AgentLlmConfig.get_instance()
            llm_config = config_loader.get_agent_config(agent_id)

            # Get LLM provider
            llm = LlmFactory.get_provider(
                agent_type=llm_config.provider,
                model=llm_config.model,
                api_key=llm_config.api_key,
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature
            )

            # 🆕 NEW: Build framework-aware system prompt
            from llm_abstractions import SystemPromptBuilder

            prompt_builder = SystemPromptBuilder()
            system_prompt = prompt_builder.build_prompt(
                task_type=task.metadata.get("task_type", "general"),
                include_agents=True,
                include_skills=True,
                include_commands=True,
                custom_context=agent_config.metadata.get("system_prompt")
            )

            # Prepare messages
            messages = []

            # Add framework-aware system prompt
            messages.append({
                "role": "system",
                "content": system_prompt
            })

            # Add task description as user message
            messages.append({
                "role": "user",
                "content": task.description
            })

            # Add context if available
            if task.metadata.get("context"):
                messages.append({
                    "role": "user",
                    "content": f"Context:\n{task.metadata['context']}"
                })

            # Call LLM
            response = await llm.generate_content_async(messages)

            # Success
            result.status = ExecutionStatus.SUCCESS
            result.output = response
            result.completed_at = datetime.now()
            result.metadata["execution_method"] = "llm_bindings"
            result.metadata["provider"] = llm_config.provider
            result.metadata["model"] = llm_config.model
            result.metadata["framework_aware"] = True  # 🆕 NEW

            return result

        except Exception as e:
            print(f"⚠️  LLM API call failed: {e}")
            result.metadata["llm_factory_error"] = str(e)

    # Fallback to script-based execution
    return await self._execute_via_script(...)
```

---

## Usage Examples

### Example 1: Agent Recommendation

```python
from llm_abstractions import get_framework_knowledge

knowledge = get_framework_knowledge()

# User asks: "I need to analyze competitors in the AI IDE market"
recommended_agents = knowledge.recommend_agent(
    "analyze competitors in AI IDE market",
    category="research_analysis"
)

print(recommended_agents)
# Output: ['competitive-market-analyst', 'web-search-researcher', 'business-intelligence-analyst']
```

### Example 2: Framework-Aware Task Execution

```python
from orchestration import TaskExecutor, AgentTask, TaskStatus

# Create task with framework awareness
task = AgentTask(
    task_id="TASK-001",
    title="Design authentication system",
    description="Design JWT authentication for our API",
    agent="senior-architect",
    status=TaskStatus.PENDING,
    metadata={
        "task_type": "architecture",  # Triggers architecture-specific prompt
        "framework_aware": True
    }
)

# Execute - LLM receives framework knowledge
executor = TaskExecutor(registry=registry)
result = await executor.execute_async(task_id="TASK-001")

# LLM now knows about:
# - All 53 agents and when to recommend them
# - Available skills like framework-patterns
# - Relevant commands like /strategy
# - Architecture best practices from framework
```

### Example 3: Custom System Prompt with Framework Knowledge

```python
from llm_abstractions import SystemPromptBuilder

builder = SystemPromptBuilder()

# Build prompt for code generation task
prompt = builder.build_prompt(
    task_type="code-generation",
    include_agents=True,
    include_skills=True,
    include_commands=False,  # Don't need commands for coding
    custom_context="Project uses Rust + Actix-web + FoundationDB stack"
)

# LLM receives:
# - Core framework knowledge
# - Code generation best practices
# - Relevant agents (rust-expert-developer, foundationdb-expert)
# - Production patterns skill
# - Custom project context
```

---

## Implementation Roadmap

### Phase 2C: Basic Framework Awareness (3-4 days)

**Tasks:**
1. ✅ Design framework knowledge registration system
2. ⏸️ Create framework-registry.json with all 180 components
3. ⏸️ Create agent metadata files (53 agents)
4. ⏸️ Create system prompt templates (5 templates)
5. ⏸️ Implement FrameworkKnowledgeLoader class
6. ⏸️ Implement SystemPromptBuilder class
7. ⏸️ Integrate with TaskExecutor
8. ⏸️ Test framework awareness with 5 agents
9. ⏸️ Document knowledge registration system

**Deliverables:**
- Structured metadata files for all components
- System prompt templates
- FrameworkKnowledgeLoader class (200 lines)
- SystemPromptBuilder class (150 lines)
- Updated TaskExecutor with knowledge injection
- Test suite (10 tests)
- Documentation

**Success Criteria:**
- LLMs can recommend appropriate agents for tasks
- LLMs understand available skills and commands
- System prompts inject framework knowledge
- Tests verify knowledge awareness

### Phase 3: Advanced Knowledge Features (1 week)

**Tasks:**
1. Add RAG (Retrieval Augmented Generation) for deep queries
2. Implement vector embeddings for semantic agent search
3. Create dynamic knowledge graph of component relationships
4. Add usage analytics (which agents recommended most)
5. Implement knowledge freshness monitoring

**Deliverables:**
- Vector database integration (Pinecone, Weaviate, or Chroma)
- Semantic search for agents/skills/commands
- Knowledge graph visualization
- Analytics dashboard

---

## Benefits

### For LLMs

1. **Intelligent Recommendations**
   - LLMs can suggest optimal agents for tasks
   - LLMs know when to use skills vs commands vs scripts
   - LLMs understand workflow patterns

2. **Proper Component Invocation**
   - LLMs use correct syntax for agent invocation
   - LLMs pass appropriate parameters
   - LLMs compose multi-agent workflows

3. **Cost Optimization**
   - LLMs recommend cost-effective agents (local vs cloud)
   - LLMs avoid premium models for simple tasks

### For Users

1. **Reduced Cognitive Load**
   - Don't need to memorize all 180 components
   - LLM recommends right tool for the job
   - Guided workflows

2. **Better Outcomes**
   - Optimal component selection
   - Proper usage patterns
   - Faster task completion

3. **Learning Assistance**
   - Discover new components through recommendations
   - Understand component relationships
   - Learn framework capabilities

---

## Future Enhancements

### Phase 4: Autonomous Component Discovery (Future)

- LLMs automatically discover new components
- Self-updating knowledge base
- Component capability inference from code

### Phase 5: Usage Pattern Learning (Future)

- Track which agents work best for which tasks
- Learn user preferences
- Personalized recommendations

### Phase 6: Multi-Framework Support (Future)

- Support multiple frameworks (CODITECT, LangChain, etc.)
- Cross-framework knowledge transfer
- Unified knowledge interface

---

## Files

**Configuration:**
- `.coditect/config/framework-registry.json` - Complete component registry
- `.coditect/config/system-prompts/` - System prompt templates

**Implementation:**
- `llm_abstractions/framework_knowledge.py` - Knowledge loader (300 lines)
- `llm_abstractions/system_prompt_builder.py` - Prompt builder (150 lines)
- `orchestration/executor.py` - Updated executor with knowledge injection

**Tests:**
- `tests/test_framework_knowledge.py` - Knowledge loading tests (10 tests)
- `tests/test_system_prompt_builder.py` - Prompt building tests (8 tests)

**Documentation:**
- `docs/02-technical-specifications/FRAMEWORK-KNOWLEDGE-REGISTRATION.md` - This file

---

**Last Updated:** November 23, 2025
**Phase:** 2C - Framework Knowledge Registration
**Next Phase:** 2D - Multi-Agent Communication Bus
