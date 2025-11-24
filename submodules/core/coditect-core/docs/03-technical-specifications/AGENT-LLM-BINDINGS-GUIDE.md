# Agent-to-LLM Bindings Guide (Phase 2A)

**Status:** Complete
**Version:** 1.0.0
**Date:** November 23, 2025
**Phase:** Phase 2A - LLM Integration

---

## Overview

The Agent-to-LLM Bindings system maps CODITECT's 52 specialized agents to optimal LLM providers, enabling intelligent provider selection based on task requirements, cost optimization, and performance characteristics.

**Key Benefits:**
- **Cost Optimization:** Match agents to appropriate LLM tier (premium/fast/cheap/free/local)
- **Performance Tuning:** Configure temperature, max_tokens per agent
- **Flexibility:** Easy provider switching without code changes
- **Centralized Configuration:** Single YAML file for all agent-LLM mappings

---

## Architecture

```
CODITECT Agent Request
         ↓
agent-llm-bindings.yaml ← Configuration file
         ↓
AgentLlmConfig Loader ← Reads and caches config
         ↓
LlmConfig (provider, model, settings)
         ↓
LlmFactory ← Instantiates provider
         ↓
BaseLlm Implementation (Claude, GPT-4, Gemini, etc.)
         ↓
Task Execution → Result
```

---

## Configuration File

**Location:** `.coditect/config/agent-llm-bindings.yaml`

### Schema

```yaml
# Default configuration (fallback for unmapped agents)
defaults:
  provider: <provider-name>
  model: <model-name>
  api_key: <key-or-env-var>  # Optional
  max_tokens: <int>           # Optional (default: 4096)
  temperature: <float>        # Optional (default: 0.7)
  metadata: {}                # Optional

# Agent-specific bindings
agents:
  <agent-id>:
    provider: <provider-name>
    model: <model-name>
    api_key: <key>             # Optional
    max_tokens: <int>          # Optional
    temperature: <float>       # Optional
    metadata:
      description: <string>    # Documentation
      use_case: <string>       # When to use this agent
      <custom-key>: <value>    # Provider-specific settings
```

### Supported Providers

| Provider | Type | Cost | Use Cases |
|----------|------|------|-----------|
| **anthropic-claude** | Cloud | $0.003/1K | Complex reasoning, architecture, critical decisions |
| **openai-gpt** | Cloud | $0.0025/1K | Code generation, comprehensive docs |
| **google-gemini** | Cloud | FREE* | Research, high-volume simple tasks |
| **huggingface** | Cloud | FREE* | Experimentation, 100K+ models |
| **ollama** | Local | $0 | Dev/test, privacy-sensitive, fast lookups |
| **lmstudio** | Local | $0 | Dev/test, private, GUI management |

*Free tier with rate limits

---

## Cost Optimization Strategy

### Tier 1: Premium Models (Complex Reasoning)

**Models:** Claude Sonnet, GPT-4o
**Cost:** ~$10-12/month for 400 tasks
**Use For:**
- System architecture decisions
- Multi-agent orchestration
- Critical business logic
- Complex technical analysis

**Agents:**
- `ai-specialist` → Claude Sonnet
- `orchestrator` → Claude Sonnet
- `senior-architect` → GPT-4o

### Tier 2: Fast/Cheap Models (Routine Tasks)

**Models:** Claude Haiku, GPT-3.5
**Cost:** ~$1-2/month for 200 tasks
**Use For:**
- Code review
- QA checks
- Simple documentation
- Standards compliance

**Agents:**
- `qa-reviewer` → Claude Haiku
- `rust-qa-specialist` → Claude Haiku

### Tier 3: Free Models (High Volume)

**Models:** Gemini Pro
**Cost:** $0 (rate-limited to 60 req/min)
**Use For:**
- Research tasks
- Web search
- Information gathering
- Non-critical analysis

**Agents:**
- `research-agent` → Gemini Pro

### Tier 4: Local Models (Unlimited, Private)

**Models:** Ollama (llama3.2, codellama), LM Studio
**Cost:** $0 (runs locally)
**Use For:**
- Development/testing
- Codebase navigation
- Privacy-sensitive tasks
- High-volume simple operations

**Agents:**
- `codebase-locator` → Ollama llama3.2
- `codebase-analyzer` → Ollama llama3.2

### Monthly Cost Estimate

**1,000 agent invocations:**
- 400 premium tasks (Claude Sonnet, GPT-4o): $10-12
- 200 fast/cheap tasks (Claude Haiku): $1-2
- 200 free tasks (Gemini): $0
- 200 local tasks (Ollama): $0

**Total: ~$11-14/month**

---

## Usage

### Python API

```python
from llm_abstractions import AgentLlmConfig, get_agent_config, LlmFactory

# Method 1: Using convenience function
config = get_agent_config("ai-specialist")
llm = LlmFactory.get_provider(
    agent_type=config.provider,
    **config.to_factory_kwargs()
)

response = await llm.generate_content_async([
    {"role": "user", "content": "Explain async/await"}
])

# Method 2: Using AgentLlmConfig directly
loader = AgentLlmConfig.get_instance()
config = loader.get_agent_config("rust-expert-developer")

llm = LlmFactory.get_provider(
    agent_type=config.provider,
    model=config.model,
    api_key=config.api_key,
    max_tokens=config.max_tokens,
    temperature=config.temperature
)
```

### TaskExecutor Integration

The TaskExecutor automatically uses agent bindings:

```python
from orchestration import TaskExecutor, AgentRegistry
from orchestration.task import AgentTask, TaskStatus

# Create task
task = AgentTask(
    task_id="TASK-001",
    title="Implement authentication",
    description="Add JWT authentication middleware",
    agent="rust-expert-developer",  # Will use GPT-4o per bindings
    status=TaskStatus.PENDING
)

# Execute - automatically uses bindings
executor = TaskExecutor(registry=registry)
result = await executor.execute_async(task_id="TASK-001")

# Check metadata
print(result.metadata["execution_method"])  # "llm_bindings"
print(result.metadata["provider"])          # "openai-gpt"
print(result.metadata["model"])             # "gpt-4o"
print(result.metadata["binding_source"])    # "agent-llm-bindings.yaml"
```

---

## Configuration Examples

### Example 1: Premium Agent (Complex Reasoning)

```yaml
agents:
  ai-specialist:
    provider: anthropic-claude
    model: claude-3-5-sonnet-20241022
    max_tokens: 4096
    temperature: 0.7
    metadata:
      description: "Core AI orchestration - needs premium reasoning"
      use_case: "Model selection, prompt optimization, AI strategy"
```

### Example 2: Code Generation Agent

```yaml
agents:
  rust-expert-developer:
    provider: openai-gpt
    model: gpt-4o
    max_tokens: 4096
    temperature: 0.4  # Lower for deterministic code
    metadata:
      description: "Rust code generation - GPT-4o excellent for code"
      use_case: "Rust implementation, async patterns, production code"
```

### Example 3: Local Agent (Fast, Free)

```yaml
agents:
  codebase-locator:
    provider: ollama
    model: llama3.2
    max_tokens: 2048
    temperature: 0.5
    metadata:
      description: "Simple search tasks - local Ollama, fast and free"
      use_case: "File discovery, component location, directory structure"
```

### Example 4: Search-Augmented Agent

```yaml
agents:
  web-search-researcher:
    provider: anthropic-claude
    model: claude-3-5-sonnet-20241022
    max_tokens: 4096
    temperature: 0.7
    metadata:
      description: "Web search + LLM - needs current information"
      use_case: "Latest news, current pricing, recent updates"
      search_augmented: true  # Flag for SearchAugmentedLlm wrapper
```

---

## Environment Variables

API keys can be specified directly or via environment variables:

### Direct Configuration

```yaml
agents:
  ai-specialist:
    api_key: "sk-ant-api03-..."  # Not recommended (exposes key in config)
```

### Environment Variable (Recommended)

```yaml
agents:
  ai-specialist:
    api_key: "${ANTHROPIC_API_KEY}"  # Resolved at runtime
```

Or omit entirely (uses environment variable by default):

```yaml
agents:
  ai-specialist:
    provider: anthropic-claude
    model: claude-3-5-sonnet-20241022
    # api_key omitted - will use ANTHROPIC_API_KEY from environment
```

### Required Environment Variables

```bash
# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# OpenAI GPT
export OPENAI_API_KEY="sk-..."

# Google Gemini
export GOOGLE_API_KEY="..."

# Hugging Face
export HUGGINGFACE_API_KEY="..."

# Ollama (no API key required - local)
# LM Studio (no API key required - local)
```

---

## Advanced Features

### Custom Provider Settings

Provider-specific settings can be added via `metadata`:

```yaml
agents:
  custom-agent:
    provider: anthropic-claude
    model: claude-3-5-sonnet-20241022
    metadata:
      # Anthropic-specific
      top_k: 40
      top_p: 0.9

      # Custom application settings
      retry_count: 3
      timeout: 60
      cache_responses: true
```

### Conditional Configuration

Different configs for different environments:

```yaml
# Production: Use premium models
agents:
  ai-specialist:
    provider: anthropic-claude
    model: claude-3-5-sonnet-20241022

# Development: Use local models (override via environment)
# Set AGENT_ENV=development
# Then agent uses ollama instead
```

### Dynamic Reload

Reload configuration without restarting:

```python
from llm_abstractions import AgentLlmConfig

# Force reload from disk
config = AgentLlmConfig.reload()

# New bindings immediately active
```

---

## Testing

### Running Tests

```bash
# Run all binding tests
pytest tests/test_agent_llm_bindings.py -v

# Run specific test class
pytest tests/test_agent_llm_bindings.py::TestAgentLlmConfig -v

# Run with coverage
pytest tests/test_agent_llm_bindings.py --cov=llm_abstractions
```

### Test Coverage

**15/15 tests passing (100%)**

**Test Categories:**
1. Configuration Loading (7 tests)
   - Load valid config
   - Get existing agent config
   - Fallback to defaults
   - Custom path loading

2. Specific Agent Bindings (5 tests)
   - ai-specialist → Claude Sonnet
   - rust-expert → GPT-4o
   - codebase-locator → Ollama
   - qa-reviewer → Claude Haiku
   - research-agent → Gemini

3. TaskExecutor Integration (3 tests)
   - Import availability
   - Config loading
   - Multiple agent configs

---

## Troubleshooting

### Issue: FileNotFoundError - Config Not Found

```
FileNotFoundError: Agent-LLM bindings config not found
```

**Solution:**
```bash
# Check file exists
ls .coditect/config/agent-llm-bindings.yaml

# If missing, create it
mkdir -p .coditect/config
cp .coditect/config/agent-llm-bindings.yaml.example .coditect/config/agent-llm-bindings.yaml
```

### Issue: ValueError - Provider Not Registered

```
ValueError: No LLM provider registered for 'custom-provider'
```

**Solution:** Use only supported providers:
- anthropic-claude
- openai-gpt
- google-gemini
- huggingface
- ollama
- lmstudio

### Issue: ImportError - PyYAML Not Found

```
ImportError: PyYAML is required for agent configuration
```

**Solution:**
```bash
pip install pyyaml>=6.0.0
```

### Issue: Agent Uses Wrong Provider

**Check:**
1. Agent ID matches exactly (case-sensitive)
2. Config file syntax is valid YAML
3. Reload config after changes: `AgentLlmConfig.reload()`

---

## Best Practices

### 1. Start with Defaults

Begin with sensible defaults, override only when needed:

```yaml
defaults:
  provider: anthropic-claude
  model: claude-3-5-sonnet-20241022
  max_tokens: 4096
  temperature: 0.7

agents:
  # Only override what's different
  codebase-locator:
    provider: ollama  # Free for simple tasks
    model: llama3.2
```

### 2. Cost-Aware Assignment

- Premium models: Architecture, orchestration, critical decisions
- Cheap models: QA, simple docs, routine checks
- Free models: Research, high-volume lookups
- Local models: Dev/test, privacy-sensitive

### 3. Temperature Tuning

```yaml
# Code generation: Lower temperature (0.3-0.5) for deterministic output
rust-expert-developer:
  temperature: 0.4

# Research: Higher temperature (0.7-0.9) for creative exploration
research-agent:
  temperature: 0.8

# QA/Review: Medium temperature (0.5-0.6) for balanced consistency
qa-reviewer:
  temperature: 0.5
```

### 4. Token Limits

```yaml
# Long-form documentation: Higher max_tokens
documentation-writer:
  max_tokens: 8192

# Simple lookups: Lower max_tokens (saves cost)
codebase-locator:
  max_tokens: 2048
```

### 5. Environment-Specific Configs

Keep sensitive keys in environment:

```yaml
# ✅ Good: Use environment variable
agents:
  ai-specialist:
    api_key: "${ANTHROPIC_API_KEY}"

# ❌ Bad: Hardcode key in file
agents:
  ai-specialist:
    api_key: "sk-ant-api03-hardcoded-key"  # Security risk!
```

---

## Migration Guide

### From Hardcoded Providers

**Before (Phase 1C):**
```python
# Hardcoded provider selection
llm = LlmFactory.get_provider(
    agent_type="anthropic-claude",  # Hardcoded
    model="claude-3-5-sonnet-20241022",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

**After (Phase 2A):**
```python
# Configuration-driven provider selection
config = get_agent_config("ai-specialist")
llm = LlmFactory.get_provider(
    agent_type=config.provider,  # From config
    **config.to_factory_kwargs()
)
```

### Adding New Agents

1. Add to `.coditect/config/agent-llm-bindings.yaml`:

```yaml
agents:
  my-new-agent:
    provider: anthropic-claude
    model: claude-3-5-haiku-20241022  # Fast and cheap
    max_tokens: 2048
    temperature: 0.6
    metadata:
      description: "New specialized agent"
      use_case: "Specific domain tasks"
```

2. No code changes required - bindings automatically loaded

3. Use immediately:

```python
config = get_agent_config("my-new-agent")
llm = LlmFactory.get_provider(agent_type=config.provider, **config.to_factory_kwargs())
```

---

## Performance Characteristics

### Latency

| Provider | p50 Latency | p95 Latency | p99 Latency |
|----------|-------------|-------------|-------------|
| Ollama (local) | <500ms | <1s | <2s |
| Claude Haiku | 1-2s | 3-4s | 5s |
| Claude Sonnet | 2-3s | 5-7s | 10s |
| GPT-4o | 1-2s | 4-5s | 8s |
| Gemini Pro | 2-4s | 6-8s | 12s |

### Throughput

| Provider | Max Concurrent | Rate Limit | Notes |
|----------|----------------|------------|-------|
| Ollama | Unlimited* | None | *CPU-bound |
| Claude | 100/min | 100,000 tokens/min | Tier 2 |
| GPT-4 | 3,500 req/min | 40,000 tokens/min | Pay-as-you-go |
| Gemini | 60/min | Free tier | Rate-limited |

---

## Files

**Configuration:**
- `.coditect/config/agent-llm-bindings.yaml` - Agent-to-LLM mappings

**Implementation:**
- `llm_abstractions/agent_llm_config.py` - Configuration loader
- `orchestration/executor.py` - TaskExecutor integration (lines 364-442)

**Tests:**
- `tests/test_agent_llm_bindings.py` - 15 tests (100% passing)

**Documentation:**
- `docs/02-technical-specifications/AGENT-LLM-BINDINGS-GUIDE.md` - This file

---

## Related Documentation

- [Phase 1C Status Report](../06-research-analysis/completion-reports/PHASE-1C-STATUS-REPORT.md)
- [LLM Provider Quick Reference](../06-research-analysis/completion-reports/PHASE-1C-QUICK-REFERENCE.md)
- [TaskExecutor Documentation](../../orchestration/executor.py)
- [LlmFactory Documentation](../../llm_abstractions/llm_factory.py)

---

**Last Updated:** November 23, 2025
**Phase:** 2A - Agent-to-LLM Bindings Complete
**Next Phase:** 2B - Slash Command Pipeline (3-4 days)
