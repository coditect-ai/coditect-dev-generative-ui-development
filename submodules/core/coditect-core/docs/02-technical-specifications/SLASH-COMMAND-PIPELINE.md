# Slash Command Pipeline (Phase 2B)

**Status:** Complete
**Version:** 1.0.0
**Date:** November 23, 2025
**Phase:** Phase 2B - Command Execution Pipeline

---

## Overview

The Slash Command Pipeline enables programmatic execution of CODITECT slash commands with structured results, external API access, and automated workflows. This transforms commands from CLI-only tools into first-class programmable components.

**Key Benefits:**
- **Programmatic Access:** Execute commands via Python API, not just Claude Code CLI
- **Structured Results:** JSON-serializable results with metadata
- **External Integration:** CI/CD, GitHub Actions, testing frameworks
- **Command Chaining:** Automated multi-command workflows
- **Cost Tracking:** Per-command cost and token usage

---

## Architecture

```
User/API Request
     ↓
SlashCommandRouter.execute("/analyze target=src/main.rs")
     ↓
CommandParser → Parse command + args
     ↓
CommandSpec → Validate arguments
     ↓
Create AgentTask with metadata
     ↓
TaskExecutor.execute_async() [Uses Phase 2A bindings]
     ↓
AgentLlmConfig → Get optimal LLM provider
     ↓
LlmFactory → Instantiate provider
     ↓
LLM Execution (with Phase 2C framework knowledge)
     ↓
CommandResult (structured output)
```

---

## Core Components

### 1. CommandResult Data Structure

**Location:** `orchestration/command_result.py`

```python
@dataclass
class CommandResult:
    """Structured result from slash command execution."""

    # Core fields
    command: str                      # "/analyze"
    status: CommandStatus             # SUCCESS, FAILED, PARTIAL, PENDING
    output: str                       # Primary output text

    # Execution metadata
    agent_used: Optional[str]         # "code-reviewer"
    llm_provider: Optional[str]       # "anthropic-claude"
    llm_model: Optional[str]          # "claude-3-5-haiku-20241022"

    # Timing
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    execution_time_seconds: Optional[float]

    # Resource usage
    tokens_used: Optional[int]
    estimated_cost: Optional[float]

    # Structured data (command-specific)
    structured_data: Dict[str, Any]

    # Additional metadata
    metadata: Dict[str, Any]

    # Error information
    error_message: Optional[str]
    error_type: Optional[str]

    def to_dict() -> Dict[str, Any]

    @property
    def success() -> bool

    @property
    def cost_formatted() -> str
```

### 2. CommandSpec Registry

**Location:** `orchestration/command_result.py`

```python
@dataclass
class CommandSpec:
    """Specification for a slash command."""

    name: str                         # "/analyze"
    agent_id: str                     # "code-reviewer"
    description: str

    # Arguments
    required_args: List[str]
    optional_args: List[str]

    # Execution config
    task_type: str                    # For system prompt selection
    streaming_enabled: bool

    # Documentation
    examples: List[str]
    category: Optional[str]
    tags: List[str]

    def validate_args(args: Dict) -> tuple[bool, Optional[str]]
```

**Available Commands:**

| Command | Agent | Task Type | Required Args | Category |
|---------|-------|-----------|---------------|----------|
| `/analyze` | code-reviewer | code-generation | (none) | development |
| `/implement` | rust-expert-developer | code-generation | description | development |
| `/research` | web-search-researcher | research | topic | research |
| `/strategy` | software-design-architect | architecture | goal | architecture |
| `/optimize` | senior-architect | code-generation | target | performance |
| `/document` | codi-documentation-writer | documentation | type | documentation |
| `/new-project` | orchestrator | general | description | project |

### 3. CommandParser

**Location:** `orchestration/command_router.py`

```python
class CommandParser:
    """Parses slash commands into structured format."""

    @staticmethod
    def parse(command_str: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parse command string into (command_name, arguments).

        Examples:
            "/analyze" → ("/analyze", {})
            "/analyze target=src/main.rs" → ("/analyze", {"target": "src/main.rs"})
            "/implement description='Add auth'" → ("/implement", {"description": "Add auth"})
        """
```

**Supported Formats:**
- Simple: `/analyze`
- Key=value: `/analyze target=src/main.rs`
- Multiple args: `/analyze target=src/main.rs focus=security`
- Quoted values: `/implement description='Add JWT authentication'`
- Double quotes: `/research topic="GraphQL vs REST"`
- Auto-description: `/implement Add authentication` → `{"description": "Add authentication"}`

### 4. SlashCommandRouter

**Location:** `orchestration/command_router.py`

```python
class SlashCommandRouter:
    """
    Routes slash commands to agents via LLM bindings.

    Provides programmatic command execution with structured results.
    """

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        executor: Optional[TaskExecutor] = None
    )

    def list_commands(category: Optional[str] = None) -> List[CommandSpec]

    def get_command_spec(command: str) -> Optional[CommandSpec]

    def get_command_help(command: str) -> str

    async def execute(
        command_str: str,
        args: Optional[Dict[str, Any]] = None
    ) -> CommandResult
```

---

## Usage Examples

### Example 1: Basic Command Execution

```python
from orchestration import get_command_router

# Get router instance
router = get_command_router()

# Execute command
result = await router.execute("/analyze target=src/main.rs")

# Check result
print(f"Status: {result.status}")              # CommandStatus.SUCCESS
print(f"Agent: {result.agent_used}")           # "code-reviewer"
print(f"Provider: {result.llm_provider}")      # "anthropic-claude"
print(f"Model: {result.llm_model}")            # "claude-3-5-haiku-20241022"
print(f"Time: {result.execution_time_seconds}s")  # 2.3
print(f"Cost: {result.cost_formatted}")        # "$0.0032"
print(f"Output:\n{result.output}")
```

### Example 2: Automated Workflow

```python
from orchestration import get_command_router, CommandStatus

router = get_command_router()

# Execute workflow
commands = [
    "/research topic='Multi-tenant SaaS architecture patterns'",
    "/strategy goal='Design multi-tenant architecture'",
    "/implement description='Add tenant isolation middleware'",
    "/analyze target=src/middleware/tenant_isolation.rs",
]

results = []

for cmd in commands:
    result = await router.execute(cmd)
    results.append(result)

    if not result.success:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {result.error_message}")
        break

    print(f"✅ {cmd} completed in {result.execution_time_seconds}s")

# Summary
total_cost = sum(r.estimated_cost or 0 for r in results)
total_time = sum(r.execution_time_seconds or 0 for r in results)

print(f"\nWorkflow complete:")
print(f"Total cost: ${total_cost:.4f}")
print(f"Total time: {total_time:.1f}s")
```

### Example 3: CI/CD Integration

```python
# GitHub Actions workflow step
from orchestration import get_command_router
import sys

router = get_command_router()

# Run code analysis
result = await router.execute("/analyze focus=security")

# Check quality gate
if result.structured_data.get("quality_score", 0) < 8:
    print(f"❌ Quality gate failed: {result.structured_data['quality_score']}/10")
    sys.exit(1)

print("✅ Quality gate passed")
```

### Example 4: Testing Framework

```python
import pytest
from orchestration import get_command_router, CommandStatus

@pytest.mark.asyncio
async def test_analyze_command():
    """Test /analyze command execution."""
    router = get_command_router()

    result = await router.execute("/analyze target=src/main.rs")

    assert result.status == CommandStatus.SUCCESS
    assert result.agent_used == "code-reviewer"
    assert result.execution_time_seconds < 5.0
    assert len(result.output) > 0

@pytest.mark.asyncio
async def test_implement_command_missing_args():
    """Test /implement fails without required args."""
    router = get_command_router()

    result = await router.execute("/implement")

    assert result.status == CommandStatus.FAILED
    assert result.error_type == "InvalidArguments"
    assert "description" in result.error_message
```

### Example 5: Command Chaining with Error Handling

```python
from orchestration import get_command_router

async def build_feature_with_quality_gates(feature_description: str):
    """Build feature with automated quality checks."""
    router = get_command_router()

    # Step 1: Research best practices
    research = await router.execute(
        f"/research topic='{feature_description} best practices'"
    )
    if not research.success:
        return {"error": "Research failed", "details": research.error_message}

    # Step 2: Design architecture
    strategy = await router.execute(
        f"/strategy goal='Design {feature_description}'"
    )
    if not strategy.success:
        return {"error": "Strategy failed", "details": strategy.error_message}

    # Step 3: Implement
    implement = await router.execute(
        f"/implement description='{feature_description}'"
    )
    if not implement.success:
        return {"error": "Implementation failed", "details": implement.error_message}

    # Step 4: Analyze quality
    analyze = await router.execute("/analyze")
    if not analyze.success:
        return {"error": "Analysis failed", "details": analyze.error_message}

    # Return results
    return {
        "success": True,
        "total_cost": sum(
            r.estimated_cost or 0
            for r in [research, strategy, implement, analyze]
        ),
        "total_time": sum(
            r.execution_time_seconds or 0
            for r in [research, strategy, implement, analyze]
        ),
        "quality_score": analyze.structured_data.get("quality_score"),
    }
```

---

## Command Specifications

### /analyze

**Agent:** code-reviewer
**Task Type:** code-generation
**Description:** Analyze code quality, security, and performance

**Arguments:**
- `target` (optional): File or directory to analyze
- `focus` (optional): Analysis focus (quality, security, performance)
- `depth` (optional): Analysis depth (quick, standard, comprehensive)

**Examples:**
```python
await router.execute("/analyze")
await router.execute("/analyze target=src/main.rs")
await router.execute("/analyze focus=security depth=comprehensive")
```

### /implement

**Agent:** rust-expert-developer
**Task Type:** code-generation
**Description:** Implement production-ready code with error handling

**Arguments:**
- `description` (**required**): What to implement
- `language` (optional): Programming language
- `framework` (optional): Framework to use

**Examples:**
```python
await router.execute("/implement description='Add JWT authentication'")
await router.execute("/implement description='WebSocket server' framework=actix-web")
```

### /research

**Agent:** web-search-researcher
**Task Type:** research
**Description:** Research external information with multi-source validation

**Arguments:**
- `topic` (**required**): Research topic
- `depth` (optional): Research depth
- `sources` (optional): Number of sources

**Examples:**
```python
await router.execute("/research topic='GraphQL vs REST performance 2025'")
await router.execute("/research topic='Rust async patterns' depth=comprehensive")
```

### /strategy

**Agent:** software-design-architect
**Task Type:** architecture
**Description:** Architectural planning with C4 diagrams and ADRs

**Arguments:**
- `goal` (**required**): Architecture goal
- `constraints` (optional): Constraints
- `style` (optional): Architecture style

**Examples:**
```python
await router.execute("/strategy goal='Design multi-tenant SaaS'")
await router.execute("/strategy goal='API design' style=REST")
```

### /optimize

**Agent:** senior-architect
**Task Type:** code-generation
**Description:** Performance optimization and scalability analysis

**Arguments:**
- `target` (**required**): What to optimize
- `metric` (optional): Performance metric
- `threshold` (optional): Target threshold

**Examples:**
```python
await router.execute("/optimize target=database_queries")
await router.execute("/optimize target=api_endpoints metric=latency")
```

### /document

**Agent:** codi-documentation-writer
**Task Type:** documentation
**Description:** Generate comprehensive documentation

**Arguments:**
- `type` (**required**): Documentation type (api, architecture, deployment)
- `target` (optional): Target component
- `format` (optional): Output format

**Examples:**
```python
await router.execute("/document type=api")
await router.execute("/document type=architecture target=auth_system")
```

### /new-project

**Agent:** orchestrator
**Task Type:** general
**Description:** Complete project creation from discovery to structure

**Arguments:**
- `description` (**required**): Project description
- `type` (optional): Project type
- `stack` (optional): Technology stack

**Examples:**
```python
await router.execute("/new-project description='Build SaaS API'")
await router.execute("/new-project description='E-commerce' stack=rust")
```

---

## Integration with Phase 2A & 2C

### Phase 2A: Agent-LLM Bindings

SlashCommandRouter leverages Phase 2A bindings for optimal LLM selection:

```python
# /analyze uses code-reviewer agent
# → Phase 2A binds code-reviewer to Claude Haiku (fast, cheap)

# /implement uses rust-expert-developer agent
# → Phase 2A binds rust-expert-developer to GPT-4o (code generation)

# /research uses web-search-researcher agent
# → Phase 2A binds web-search-researcher to Claude Sonnet (research)
```

### Phase 2C: Framework Knowledge

Commands receive framework-aware system prompts:

```python
# /strategy command → task_type="architecture"
# → SystemPromptBuilder injects:
#    - C4 methodology requirements
#    - ADR documentation standards
#    - Available architecture patterns
#    - Related agents (multi-tenant-architect, security-specialist)
```

---

## Testing

### Running Tests

```bash
# Run all command router tests
pytest tests/test_command_router.py -v

# Run specific test class
pytest tests/test_command_router.py::TestSlashCommandRouter -v

# Run with coverage
pytest tests/test_command_router.py --cov=orchestration
```

### Test Coverage

**29/29 tests passing (100%)**

**Test Categories:**
1. **CommandParser** (6 tests)
   - Simple commands
   - Single/multiple arguments
   - Quoted values
   - Auto-description

2. **CommandRegistry** (3 tests)
   - Command availability
   - Command specifications
   - Agent mappings

3. **CommandSpec** (3 tests)
   - Argument validation
   - Required vs optional args
   - Error messages

4. **SlashCommandRouter** (10 tests)
   - Router initialization
   - Command listing/filtering
   - Command help
   - Execution (success/failure)
   - Unknown commands
   - Missing arguments

5. **CommandResult** (6 tests)
   - Data structure creation
   - JSON serialization
   - Success property
   - Cost formatting

6. **Singleton** (1 test)
   - get_command_router() returns same instance

---

## Error Handling

### Unknown Command

```python
result = await router.execute("/unknown")

assert result.status == CommandStatus.FAILED
assert result.error_type == "UnknownCommand"
assert result.error_message == "Unknown command: /unknown"
```

### Missing Required Arguments

```python
result = await router.execute("/implement")  # Missing 'description'

assert result.status == CommandStatus.FAILED
assert result.error_type == "InvalidArguments"
assert "Missing required argument: description" in result.error_message
```

### Execution Failure

```python
# If LLM call fails
result = await router.execute("/analyze")

if not result.success:
    print(f"Error Type: {result.error_type}")
    print(f"Error Message: {result.error_message}")
    print(f"Agent Used: {result.agent_used}")
```

---

## Performance Characteristics

### Latency

| Command | Typical Latency | LLM Provider | Notes |
|---------|----------------|--------------|-------|
| `/analyze` | 1-2s | Claude Haiku | Fast, cheap QA model |
| `/implement` | 2-4s | GPT-4o | Code generation model |
| `/research` | 3-5s | Claude Sonnet | Multi-source validation |
| `/strategy` | 4-6s | Claude Sonnet | Complex architecture |
| `/new-project` | 10-20s | Orchestrator | Multi-agent workflow |

### Cost

| Command | Typical Cost | Tokens | Provider |
|---------|-------------|--------|----------|
| `/analyze` | $0.002-0.004 | 500-1000 | Claude Haiku |
| `/implement` | $0.008-0.015 | 2000-3000 | GPT-4o |
| `/research` | $0.005-0.010 | 1500-2500 | Claude Sonnet |
| `/strategy` | $0.010-0.020 | 3000-4000 | Claude Sonnet |

**Monthly Estimate (100 commands):**
- 40 /analyze: $0.12
- 30 /implement: $0.36
- 20 /research: $0.15
- 10 /strategy: $0.15
- **Total: ~$0.78/month**

---

## Files

**Implementation:**
- `orchestration/command_result.py` (200 lines) - Data structures
- `orchestration/command_router.py` (380 lines) - Router and parser
- `orchestration/__init__.py` - Updated exports

**Tests:**
- `tests/test_command_router.py` (340 lines) - 29 tests, 100% passing

**Documentation:**
- `docs/02-technical-specifications/SLASH-COMMAND-PIPELINE.md` - This file

---

## Future Enhancements

### Phase 3: Additional Features

1. **Streaming Results**
   - Real-time command output streaming
   - Progress updates for long-running commands

2. **Command History**
   - Persistent command history
   - Replay commands with same arguments

3. **Command Macros**
   - Define custom command combinations
   - Parameterized workflows

4. **REST API**
   - HTTP endpoint for command execution
   - WebSocket for streaming results
   - API authentication and rate limiting

5. **CLI Tool**
   - Standalone `coditect` CLI tool
   - Interactive command mode
   - Shell completion

---

## Related Documentation

- [Phase 2A: Agent-LLM Bindings](AGENT-LLM-BINDINGS-GUIDE.md)
- [Phase 2C: Framework Knowledge Registration](FRAMEWORK-KNOWLEDGE-REGISTRATION.md)
- [TaskExecutor Documentation](../../orchestration/executor.py)
- [LlmFactory Documentation](../../llm_abstractions/llm_factory.py)

---

**Last Updated:** November 23, 2025
**Phase:** 2B - Slash Command Pipeline Complete
**Next Phase:** 2D - Multi-Agent Communication Bus
