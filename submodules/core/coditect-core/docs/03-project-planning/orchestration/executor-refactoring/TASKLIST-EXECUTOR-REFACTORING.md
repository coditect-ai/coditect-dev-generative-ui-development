# TaskExecutor Refactoring - Task List

**Document Version:** 1.0
**Last Updated:** 2025-11-23
**Document Owner:** Hal Casteel, CEO/CTO, AZ1.AI INC.
**Total Tasks:** 186 tasks across 6 phases
**Total Hours:** 80 hours
**Status:** PLANNING - Ready for Execution

---

## Progress Summary

| Phase | Total Tasks | Completed | In Progress | Pending | Hours | Status |
|-------|-------------|-----------|-------------|---------|-------|--------|
| **Phase 1A** | 32 | 0 | 0 | 32 | 16 | 📅 Planned |
| **Phase 1B** | 34 | 0 | 0 | 34 | 16 | 📅 Planned |
| **Phase 2A** | 32 | 0 | 0 | 32 | 16 | 📅 Planned |
| **Phase 2B** | 32 | 0 | 0 | 32 | 16 | 📅 Planned |
| **Phase 3** | 28 | 0 | 0 | 28 | 16 | 📅 Planned |
| **Phase 4** | 28 | 0 | 0 | 28 | 16 | 📅 Planned |
| **TOTAL** | **186** | **0** | **0** | **186** | **80** | 📅 Planned |

**Current Phase:** None (awaiting go/no-go decision)
**Next Milestone:** Phase 1A Foundation Complete

---

## Phase 1A: Foundation (Week 1, Days 1-2, 16 hours)

**Goal:** Create LlmFactory and implement AnthropicLlm with official SDK

**Agent Assignments:**
- **rust-expert-developer:** Tasks 1.1-1.15
- **codi-test-engineer:** Tasks 1.16-1.32

**Deliverables:**
- ✅ `llm_abstractions/factory.py` (200 lines)
- ✅ `llm_abstractions/anthropic.py` (150 lines)
- ✅ Unit tests (200 lines)

---

### 1.1 LlmFactory Implementation (6 hours)

**Agent:** rust-expert-developer
**Time Estimate:** 6 hours

#### Setup & Architecture

- [ ] **T1.1.1** Create `llm_abstractions/factory.py` file (5 min)
- [ ] **T1.1.2** Add module docstring with copyright and description (10 min)
- [ ] **T1.1.3** Import required dependencies (typing, os, importlib, enum) (5 min)
- [ ] **T1.1.4** Define provider registry data structure (30 min)

#### Provider Registry

- [ ] **T1.1.5** Create `_PROVIDER_REGISTRY` dict with Anthropic entry (15 min)
  - Module path: `llm_abstractions.anthropic`
  - Class name: `AnthropicLlm`
  - Env var: `ANTHROPIC_API_KEY`
  - Dependencies: `["anthropic"]`

- [ ] **T1.1.6** Add OpenAI entry to registry (10 min)
  - Module path: `llm_abstractions.openai_llm`
  - Class name: `OpenAILlm`
  - Env var: `OPENAI_API_KEY`
  - Dependencies: `["openai"]`

- [ ] **T1.1.7** Add Gemini entry to registry (10 min)
  - Module path: `llm_abstractions.gemini`
  - Class name: `GeminiLlm`
  - Env var: `GOOGLE_API_KEY`
  - Dependencies: `["google-generativeai"]`

#### LlmFactory Class

- [ ] **T1.1.8** Create `LlmFactory` class with docstring (15 min)
- [ ] **T1.1.9** Implement `get_provider()` static method signature (10 min)
- [ ] **T1.1.10** Add provider validation logic (check registry) (20 min)
- [ ] **T1.1.11** Add API key validation logic (check env var) (20 min)
- [ ] **T1.1.12** Implement dynamic module import (importlib.import_module) (30 min)
- [ ] **T1.1.13** Implement provider class instantiation (getattr + call) (20 min)
- [ ] **T1.1.14** Add error handling (ValueError, ImportError, RuntimeError) (30 min)

#### Helper Methods

- [ ] **T1.1.15** Implement `list_available_providers()` static method (30 min)
  - Check each provider's API key
  - Check each provider's dependencies (try import)
  - Return list of available AgentTypes

- [ ] **T1.1.16** Implement `is_provider_available()` static method (15 min)
  - Check if single provider available
  - Return bool

#### Type Hints & Documentation

- [ ] **T1.1.17** Add complete type hints to all methods (30 min)
- [ ] **T1.1.18** Write detailed docstrings for all methods (45 min)
- [ ] **T1.1.19** Add usage examples in module docstring (15 min)

#### Code Review

- [ ] **T1.1.20** Self-review: Check type hints coverage (10 min)
- [ ] **T1.1.21** Self-review: Run mypy type checker (10 min)
- [ ] **T1.1.22** Self-review: Run black code formatter (5 min)

**Subtotal:** 6 hours

---

### 1.2 AnthropicLlm Implementation (6 hours)

**Agent:** rust-expert-developer
**Time Estimate:** 6 hours

#### Setup

- [ ] **T1.2.1** Create `llm_abstractions/anthropic.py` file (5 min)
- [ ] **T1.2.2** Add module docstring with copyright and description (10 min)
- [ ] **T1.2.3** Import required dependencies (anthropic, asyncio, os, typing) (10 min)
- [ ] **T1.2.4** Import `BaseLlm` from base_llm (5 min)

#### AnthropicLlm Class

- [ ] **T1.2.5** Create `AnthropicLlm` class inheriting from `BaseLlm` (10 min)
- [ ] **T1.2.6** Implement `__init__()` method signature (15 min)
  - Parameters: model, api_key, **kwargs
  - Defaults: model="claude-sonnet-4-5-20250929"

- [ ] **T1.2.7** Add API key validation in `__init__()` (20 min)
  - Check parameter or environment variable
  - Raise ValueError if missing

- [ ] **T1.2.8** Initialize `AsyncAnthropic` client (15 min)
- [ ] **T1.2.9** Store configuration attributes (model, api_key) (10 min)

#### Message Conversion

- [ ] **T1.2.10** Create `_extract_system_prompt()` helper method (30 min)
  - Parse messages list for system role
  - Return system prompt string or None

- [ ] **T1.2.11** Create `_convert_to_claude_format()` helper method (45 min)
  - Convert OpenAI format to Claude format
  - Handle role mapping (system → messages, user, assistant)
  - Return Claude-compatible messages list

#### Content Generation

- [ ] **T1.2.12** Implement `generate_content_async()` method signature (15 min)
- [ ] **T1.2.13** Extract system prompt from messages (10 min)
- [ ] **T1.2.14** Convert messages to Claude format (10 min)
- [ ] **T1.2.15** Call `client.messages.create()` with await (30 min)
  - Pass model, system, messages, max_tokens, temperature
  - Handle kwargs for additional parameters

- [ ] **T1.2.16** Extract text content from response (20 min)
  - Access response.content[0].text
  - Handle potential errors (empty response, etc.)

- [ ] **T1.2.17** Add error handling for API errors (30 min)
  - anthropic.AuthenticationError
  - anthropic.RateLimitError
  - anthropic.APIError
  - General exceptions

#### Type Hints & Documentation

- [ ] **T1.2.18** Add complete type hints to all methods (30 min)
- [ ] **T1.2.19** Write detailed docstrings for all methods (45 min)
- [ ] **T1.2.20** Add usage examples in class docstring (15 min)

#### Code Review

- [ ] **T1.2.21** Self-review: Check type hints coverage (10 min)
- [ ] **T1.2.22** Self-review: Run mypy type checker (10 min)
- [ ] **T1.2.23** Self-review: Run black code formatter (5 min)

**Subtotal:** 6 hours

---

### 1.3 Unit Tests for LlmFactory (2 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 2 hours

#### Test Setup

- [ ] **T1.3.1** Create `tests/test_factory.py` file (5 min)
- [ ] **T1.3.2** Add test module docstring (5 min)
- [ ] **T1.3.3** Import pytest and required modules (10 min)
- [ ] **T1.3.4** Create pytest fixtures for mock providers (20 min)

#### get_provider() Tests

- [ ] **T1.3.5** Test valid provider instantiation (Anthropic) (15 min)
- [ ] **T1.3.6** Test valid provider with custom model (15 min)
- [ ] **T1.3.7** Test invalid agent type raises ValueError (10 min)
- [ ] **T1.3.8** Test missing API key raises RuntimeError (15 min)
- [ ] **T1.3.9** Test missing dependencies raises ImportError (15 min)

#### list_available_providers() Tests

- [ ] **T1.3.10** Test all providers available (mock env vars + imports) (15 min)
- [ ] **T1.3.11** Test partial providers available (some missing keys) (15 min)
- [ ] **T1.3.12** Test no providers available (no keys set) (10 min)

#### is_provider_available() Tests

- [ ] **T1.3.13** Test provider available (API key + dependencies) (10 min)
- [ ] **T1.3.14** Test provider unavailable (missing API key) (10 min)
- [ ] **T1.3.15** Test provider unavailable (missing dependencies) (10 min)

**Subtotal:** 2 hours

---

### 1.4 Unit Tests for AnthropicLlm (2 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 2 hours

#### Test Setup

- [ ] **T1.4.1** Create `tests/test_anthropic.py` file (5 min)
- [ ] **T1.4.2** Add test module docstring (5 min)
- [ ] **T1.4.3** Import pytest, asyncio, and required modules (10 min)
- [ ] **T1.4.4** Create pytest fixtures for mock AsyncAnthropic client (20 min)

#### Initialization Tests

- [ ] **T1.4.5** Test initialization with API key parameter (10 min)
- [ ] **T1.4.6** Test initialization with env var (10 min)
- [ ] **T1.4.7** Test initialization fails without API key (10 min)
- [ ] **T1.4.8** Test initialization with custom model (10 min)

#### Message Conversion Tests

- [ ] **T1.4.9** Test _extract_system_prompt() with system message (15 min)
- [ ] **T1.4.10** Test _extract_system_prompt() without system message (10 min)
- [ ] **T1.4.11** Test _convert_to_claude_format() with valid messages (15 min)
- [ ] **T1.4.12** Test _convert_to_claude_format() handles edge cases (15 min)

#### Content Generation Tests

- [ ] **T1.4.13** Test generate_content_async() success path (mock response) (20 min)
- [ ] **T1.4.14** Test generate_content_async() with custom parameters (15 min)
- [ ] **T1.4.15** Test generate_content_async() handles API errors (15 min)

**Subtotal:** 2 hours

---

### Phase 1A Quality Gate

**Exit Criteria:**
- [ ] **QG1.1** All Phase 1A tasks completed (32/32 checked)
- [ ] **QG1.2** LlmFactory can instantiate AnthropicLlm
- [ ] **QG1.3** AnthropicLlm successfully calls Claude API (integration test)
- [ ] **QG1.4** Test coverage ≥90% for factory.py and anthropic.py
- [ ] **QG1.5** All unit tests pass (100% pass rate)
- [ ] **QG1.6** Code review approved by senior-architect

**Validation Commands:**
```bash
pytest tests/test_factory.py tests/test_anthropic.py -v --cov
pytest tests/integration/test_anthropic_real_api.py -v
pytest --cov=llm_abstractions --cov-report=term-missing
```

---

## Phase 1B: Dual-Mode Executor (Week 1, Days 3-5, 16 hours)

**Goal:** Add dual-mode execution to TaskExecutor with graceful fallback

**Agent Assignments:**
- **rust-expert-developer:** Tasks 2.1-2.20
- **codi-test-engineer:** Tasks 2.21-2.34

**Deliverables:**
- ✅ Updated `orchestration/executor.py` (+150 lines)
- ✅ Unit tests (150 lines)
- ✅ Integration tests (50 lines)

---

### 2.1 TaskExecutor Modifications (8 hours)

**Agent:** rust-expert-developer
**Time Estimate:** 8 hours

#### Helper Methods

- [ ] **T2.1.1** Create `_build_messages_from_task()` method signature (15 min)
- [ ] **T2.1.2** Implement system prompt generation (30 min)
  - Include task ID, title, agent name
  - Follow standard format

- [ ] **T2.1.3** Implement user prompt generation (30 min)
  - Include task description
  - Add deliverables section if present
  - Add success criteria section if present

- [ ] **T2.1.4** Return OpenAI-format messages list (15 min)
- [ ] **T2.1.5** Add type hints and docstring (20 min)

#### _execute_via_llm() Method

- [ ] **T2.1.6** Create `_execute_via_llm()` method signature (15 min)
  - Parameters: task, agent_config, result
  - Returns: ExecutionResult

- [ ] **T2.1.7** Set result status to IN_PROGRESS (5 min)
- [ ] **T2.1.8** Import LlmFactory (handle import errors) (15 min)
- [ ] **T2.1.9** Call LlmFactory.get_provider() (30 min)
  - Pass agent_type from agent_config
  - Pass model from task.metadata if present
  - Handle provider instantiation errors

- [ ] **T2.1.10** Build messages using _build_messages_from_task() (10 min)
- [ ] **T2.1.11** Implement async/sync detection (30 min)
  - Check if event loop is running
  - Use await if in async context
  - Use asyncio.run() if in sync context

- [ ] **T2.1.12** Call provider.generate_content_async() (20 min)
- [ ] **T2.1.13** Handle successful response (20 min)
  - Set result.status = SUCCESS
  - Set result.output = response
  - Set result.completed_at
  - Set metadata["execution_mode"] = "llm_direct"

#### Error Handling

- [ ] **T2.1.14** Handle ImportError (provider dependencies missing) (20 min)
  - Set result.status = FAILED
  - Set metadata["fallback_reason"] = "missing_dependencies"

- [ ] **T2.1.15** Handle RuntimeError (API key missing) (20 min)
  - Set result.status = FAILED
  - Set metadata["fallback_reason"] = "missing_api_key"

- [ ] **T2.1.16** Handle general exceptions (20 min)
  - Set result.status = FAILED
  - Set result.error = str(e)

- [ ] **T2.1.17** Add type hints and comprehensive docstring (30 min)

#### Modify _execute_api() Method

- [ ] **T2.1.18** Add feature flag check (use_direct_llm) (15 min)
  - Default to True
  - Read from task.metadata

- [ ] **T2.1.19** Implement dual-mode routing (45 min)
  - If use_direct_llm=True: Call _execute_via_llm()
  - If use_direct_llm=False: Call _execute_via_script()

- [ ] **T2.1.20** Implement graceful fallback (45 min)
  - Check if _execute_via_llm() failed with fallback_reason
  - Print fallback warning
  - Reset result status
  - Call _execute_via_script()

**Subtotal:** 8 hours

---

### 2.2 Async/Sync Compatibility Layer (4 hours)

**Agent:** rust-expert-developer
**Time Estimate:** 4 hours

#### Event Loop Detection

- [ ] **T2.2.1** Create `_get_or_create_event_loop()` helper (45 min)
  - Try to get running loop
  - Create new loop if none exists
  - Handle RuntimeError gracefully

- [ ] **T2.2.2** Create `_run_async_in_sync_context()` helper (45 min)
  - Wrapper around asyncio.run()
  - Handle event loop cleanup
  - Add error handling

#### Integration into _execute_via_llm()

- [ ] **T2.2.3** Update _execute_via_llm() to use helpers (30 min)
- [ ] **T2.2.4** Test async context execution (manual testing) (30 min)
- [ ] **T2.2.5** Test sync context execution (manual testing) (30 min)

#### Edge Case Handling

- [ ] **T2.2.6** Handle nested event loops (30 min)
  - Detect if already in async context
  - Use nest_asyncio if needed (optional)

- [ ] **T2.2.7** Handle loop cleanup on errors (30 min)
- [ ] **T2.2.8** Add comprehensive error messages (20 min)

**Subtotal:** 4 hours

---

### 2.3 Unit Tests for Dual-Mode Executor (3 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 3 hours

#### Test Setup

- [ ] **T2.3.1** Create `tests/test_executor_dual_mode.py` file (5 min)
- [ ] **T2.3.2** Add test module docstring (5 min)
- [ ] **T2.3.3** Import pytest, asyncio, mock, and required modules (10 min)
- [ ] **T2.3.4** Create fixtures for TaskExecutor, AgentTask, AgentConfig (20 min)
- [ ] **T2.3.5** Create mock LlmFactory and providers (30 min)

#### _build_messages_from_task() Tests

- [ ] **T2.3.6** Test message building with minimal task (15 min)
- [ ] **T2.3.7** Test message building with deliverables (15 min)
- [ ] **T2.3.8** Test message building with success criteria (15 min)
- [ ] **T2.3.9** Test message building with all fields (15 min)

#### _execute_via_llm() Tests

- [ ] **T2.3.10** Test successful execution (mock provider) (20 min)
- [ ] **T2.3.11** Test execution with custom model (15 min)
- [ ] **T2.3.12** Test execution handles missing dependencies (15 min)
- [ ] **T2.3.13** Test execution handles missing API key (15 min)
- [ ] **T2.3.14** Test execution handles provider errors (15 min)

#### _execute_api() Dual-Mode Tests

- [ ] **T2.3.15** Test use_direct_llm=True routes to _execute_via_llm() (15 min)
- [ ] **T2.3.16** Test use_direct_llm=False routes to _execute_via_script() (15 min)
- [ ] **T2.3.17** Test graceful fallback on provider unavailability (20 min)
- [ ] **T2.3.18** Test fallback warning is displayed (15 min)

**Subtotal:** 3 hours

---

### 2.4 Integration Tests (1 hour)

**Agent:** codi-test-engineer
**Time Estimate:** 1 hour

#### Integration Test Setup

- [ ] **T2.4.1** Create `tests/integration/test_executor_anthropic.py` file (5 min)
- [ ] **T2.4.2** Add integration test docstring (5 min)
- [ ] **T2.4.3** Add pytest marker for integration tests (@pytest.mark.integration) (5 min)
- [ ] **T2.4.4** Check for ANTHROPIC_API_KEY in environment (skip if missing) (10 min)

#### Real API Tests

- [ ] **T2.4.5** Test TaskExecutor executes task via AnthropicLlm (20 min)
  - Create real AgentTask
  - Set use_direct_llm=True
  - Execute and verify response

- [ ] **T2.4.6** Test graceful fallback (remove API key temporarily) (15 min)

**Subtotal:** 1 hour

---

### Phase 1B Quality Gate

**Exit Criteria:**
- [ ] **QG2.1** All Phase 1B tasks completed (34/34 checked)
- [ ] **QG2.2** TaskExecutor executes tasks via AnthropicLlm when use_direct_llm=True
- [ ] **QG2.3** Graceful fallback to script execution works
- [ ] **QG2.4** Async/sync compatibility layer functional
- [ ] **QG2.5** Test coverage ≥90% for new executor code
- [ ] **QG2.6** All unit + integration tests pass (100% pass rate)
- [ ] **QG2.7** Code review approved by senior-architect

**Validation Commands:**
```bash
pytest tests/test_executor_dual_mode.py -v --cov
pytest tests/integration/test_executor_anthropic.py -v
pytest --cov=orchestration.executor --cov-report=term-missing
```

---

## Phase 2A: OpenAI Implementation (Week 2, Days 1-2, 16 hours)

**Goal:** Implement OpenAILlm with AsyncOpenAI SDK

**Agent Assignments:**
- **rust-expert-developer:** Tasks 3.1-3.11
- **codi-test-engineer:** Tasks 3.12-3.32

**Deliverables:**
- ✅ `llm_abstractions/openai_llm.py` (150 lines)
- ✅ Updated `llm_abstractions/factory.py` (+10 lines)
- ✅ Unit + integration tests (150 lines)
- ✅ Performance benchmark (100 lines)

---

### 3.1 OpenAILlm Implementation (6 hours)

**Agent:** rust-expert-developer
**Time Estimate:** 6 hours

#### Setup

- [ ] **T3.1.1** Create `llm_abstractions/openai_llm.py` file (5 min)
- [ ] **T3.1.2** Add module docstring with copyright and description (10 min)
- [ ] **T3.1.3** Import required dependencies (openai, asyncio, os, typing) (10 min)
- [ ] **T3.1.4** Import `BaseLlm` from base_llm (5 min)

#### OpenAILlm Class

- [ ] **T3.1.5** Create `OpenAILlm` class inheriting from `BaseLlm` (10 min)
- [ ] **T3.1.6** Implement `__init__()` method (20 min)
  - Parameters: model, api_key, **kwargs
  - Default: model="gpt-4o"

- [ ] **T3.1.7** Add API key validation (15 min)
- [ ] **T3.1.8** Initialize `AsyncOpenAI` client (2025 SDK) (20 min)
- [ ] **T3.1.9** Store configuration attributes (15 min)

#### Content Generation

- [ ] **T3.1.10** Implement `generate_content_async()` method (45 min)
  - Call client.chat.completions.create()
  - Pass model, messages, max_tokens, temperature
  - Handle kwargs

- [ ] **T3.1.11** Extract text content from response (20 min)
  - Access choices[0].message.content
  - Handle empty responses

#### Error Handling

- [ ] **T3.1.12** Add error handling for OpenAI errors (45 min)
  - AuthenticationError
  - RateLimitError
  - APIError
  - General exceptions

#### Type Hints & Documentation

- [ ] **T3.1.13** Add complete type hints (30 min)
- [ ] **T3.1.14** Write detailed docstrings (45 min)
- [ ] **T3.1.15** Add usage examples (15 min)

#### Code Review

- [ ] **T3.1.16** Self-review: Type hints (10 min)
- [ ] **T3.1.17** Self-review: Run mypy (10 min)
- [ ] **T3.1.18** Self-review: Run black (5 min)

**Subtotal:** 6 hours

---

### 3.2 Factory Registration (2 hours)

**Agent:** rust-expert-developer
**Time Estimate:** 2 hours

- [ ] **T3.2.1** Update `llm_abstractions/factory.py` (5 min)
- [ ] **T3.2.2** Verify OpenAI entry in _PROVIDER_REGISTRY (already exists) (5 min)
- [ ] **T3.2.3** Test factory can instantiate OpenAILlm (15 min)
- [ ] **T3.2.4** Update `llm_abstractions/__init__.py` to export OpenAILlm (10 min)
- [ ] **T3.2.5** Manual smoke test with real API key (30 min)

**Subtotal:** 2 hours

---

### 3.3 Unit Tests for OpenAILlm (2 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 2 hours

#### Test Setup

- [ ] **T3.3.1** Create `tests/test_openai_llm.py` file (5 min)
- [ ] **T3.3.2** Add test module docstring (5 min)
- [ ] **T3.3.3** Import pytest, asyncio, and required modules (10 min)
- [ ] **T3.3.4** Create fixtures for mock AsyncOpenAI client (20 min)

#### Initialization Tests

- [ ] **T3.3.5** Test initialization with API key parameter (10 min)
- [ ] **T3.3.6** Test initialization with env var (10 min)
- [ ] **T3.3.7** Test initialization fails without API key (10 min)
- [ ] **T3.3.8** Test initialization with custom model (10 min)

#### Content Generation Tests

- [ ] **T3.3.9** Test generate_content_async() success (mock response) (20 min)
- [ ] **T3.3.10** Test generate_content_async() with custom parameters (15 min)
- [ ] **T3.3.11** Test generate_content_async() handles API errors (15 min)

**Subtotal:** 2 hours

---

### 3.4 Integration Tests (2 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 2 hours

- [ ] **T3.4.1** Create `tests/integration/test_executor_openai.py` file (5 min)
- [ ] **T3.4.2** Add integration test docstring (5 min)
- [ ] **T3.4.3** Add pytest marker (@pytest.mark.integration) (5 min)
- [ ] **T3.4.4** Check for OPENAI_API_KEY (skip if missing) (10 min)
- [ ] **T3.4.5** Test TaskExecutor with OpenAILlm (real API) (30 min)
- [ ] **T3.4.6** Test fallback behavior (remove API key) (15 min)

**Subtotal:** 2 hours

---

### 3.5 Performance Benchmarks (4 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 4 hours

#### Benchmark Setup

- [ ] **T3.5.1** Create `benchmarks/openai_comparison.py` file (10 min)
- [ ] **T3.5.2** Add benchmark module docstring (10 min)
- [ ] **T3.5.3** Import required modules (time, statistics, TaskExecutor) (10 min)
- [ ] **T3.5.4** Create sample AgentTask for benchmarking (15 min)

#### Benchmark Implementation

- [ ] **T3.5.5** Implement `benchmark_subprocess_execution()` (30 min)
  - Set use_direct_llm=False
  - Run 10 iterations
  - Record times

- [ ] **T3.5.6** Implement `benchmark_direct_llm_execution()` (30 min)
  - Set use_direct_llm=True
  - Run 10 iterations
  - Record times

- [ ] **T3.5.7** Calculate statistics (mean, median, std dev) (20 min)
- [ ] **T3.5.8** Calculate improvement percentage (15 min)
- [ ] **T3.5.9** Generate benchmark report (30 min)
  - Format: Markdown table
  - Include: mean, median, improvement %
  - Save to `benchmarks/openai-results.md`

#### Validation

- [ ] **T3.5.10** Run benchmarks with real API (1 hour)
- [ ] **T3.5.11** Verify ≥30% improvement (15 min)
- [ ] **T3.5.12** Document results in test-results/ directory (15 min)

**Subtotal:** 4 hours

---

### Phase 2A Quality Gate

**Exit Criteria:**
- [ ] **QG3.1** All Phase 2A tasks completed (32/32 checked)
- [ ] **QG3.2** OpenAILlm successfully calls GPT-4 API
- [ ] **QG3.3** TaskExecutor executes tasks via OpenAILlm
- [ ] **QG3.4** Performance benchmark shows ≥30% improvement
- [ ] **QG3.5** Test coverage ≥90% for openai_llm.py
- [ ] **QG3.6** All unit + integration tests pass
- [ ] **QG3.7** Performance validation report approved

**Validation Commands:**
```bash
pytest tests/test_openai_llm.py tests/integration/test_executor_openai.py -v
python benchmarks/openai_comparison.py
pytest --cov=llm_abstractions.openai_llm --cov-report=term-missing
```

---

## Phase 2B: Gemini Implementation (Week 2, Days 3-5, 16 hours)

**Goal:** Complete Gemini implementation (replace placeholder)

**Agent Assignments:**
- **rust-expert-developer:** Tasks 4.1-4.11
- **codi-test-engineer:** Tasks 4.12-4.32

**Deliverables:**
- ✅ Updated `llm_abstractions/gemini.py` (150 lines)
- ✅ Updated factory registry
- ✅ Unit + integration tests (150 lines)
- ✅ Performance benchmark (100 lines)

---

### 4.1 GeminiLlm Implementation (6 hours)

**Agent:** rust-expert-developer
**Time Estimate:** 6 hours

#### Update Existing File

- [ ] **T4.1.1** Open `llm_abstractions/gemini.py` (5 min)
- [ ] **T4.1.2** Review existing placeholder code (15 min)
- [ ] **T4.1.3** Update imports (add google.generativeai) (10 min)

#### Update Initialization

- [ ] **T4.1.4** Update `__init__()` to use google-generativeai SDK (30 min)
  - Configure API key: genai.configure(api_key=self.api_key)
  - Create model: genai.GenerativeModel(model)

- [ ] **T4.1.5** Update default model to "gemini-1.5-pro" (5 min)
- [ ] **T4.1.6** Add API key validation (10 min)

#### Message Conversion

- [ ] **T4.1.7** Create `_convert_to_gemini_format()` helper (45 min)
  - Convert OpenAI messages to Gemini format
  - Handle role mapping
  - Handle multi-turn conversations

#### Content Generation

- [ ] **T4.1.8** Replace placeholder `generate_content_async()` (1 hour)
  - Convert messages to Gemini format
  - Call model.generate_content_async()
  - Pass generation_config with temperature, max_output_tokens

- [ ] **T4.1.9** Extract text from response (20 min)
  - Access response.text
  - Handle empty responses

#### Error Handling

- [ ] **T4.1.10** Add error handling for Gemini API errors (45 min)
  - google.api_core.exceptions.PermissionDenied
  - google.api_core.exceptions.ResourceExhausted
  - General exceptions

#### Type Hints & Documentation

- [ ] **T4.1.11** Update type hints (30 min)
- [ ] **T4.1.12** Update docstrings (45 min)
- [ ] **T4.1.13** Add usage examples (15 min)

#### Code Review

- [ ] **T4.1.14** Self-review: Type hints (10 min)
- [ ] **T4.1.15** Self-review: Run mypy (10 min)
- [ ] **T4.1.16** Self-review: Run black (5 min)

**Subtotal:** 6 hours

---

### 4.2 Factory Registration (2 hours)

**Agent:** rust-expert-developer
**Time Estimate:** 2 hours

- [ ] **T4.2.1** Verify Gemini entry in _PROVIDER_REGISTRY (5 min)
- [ ] **T4.2.2** Update dependencies to `["google-generativeai"]` (5 min)
- [ ] **T4.2.3** Test factory can instantiate GeminiLlm (15 min)
- [ ] **T4.2.4** Update `__init__.py` exports (10 min)
- [ ] **T4.2.5** Manual smoke test with real API key (30 min)

**Subtotal:** 2 hours

---

### 4.3 Unit Tests for GeminiLlm (2 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 2 hours

#### Test Setup

- [ ] **T4.3.1** Create or update `tests/test_gemini.py` file (5 min)
- [ ] **T4.3.2** Add test module docstring (5 min)
- [ ] **T4.3.3** Import pytest, asyncio, and required modules (10 min)
- [ ] **T4.3.4** Create fixtures for mock Gemini client (20 min)

#### Initialization Tests

- [ ] **T4.3.5** Test initialization with API key parameter (10 min)
- [ ] **T4.3.6** Test initialization with env var (10 min)
- [ ] **T4.3.7** Test initialization fails without API key (10 min)
- [ ] **T4.3.8** Test initialization with custom model (10 min)

#### Content Generation Tests

- [ ] **T4.3.9** Test generate_content_async() success (mock response) (20 min)
- [ ] **T4.3.10** Test generate_content_async() with custom parameters (15 min)
- [ ] **T4.3.11** Test generate_content_async() handles API errors (15 min)

**Subtotal:** 2 hours

---

### 4.4 Integration Tests (2 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 2 hours

- [ ] **T4.4.1** Create `tests/integration/test_executor_gemini.py` file (5 min)
- [ ] **T4.4.2** Add integration test docstring (5 min)
- [ ] **T4.4.3** Add pytest marker (@pytest.mark.integration) (5 min)
- [ ] **T4.4.4** Check for GOOGLE_API_KEY (skip if missing) (10 min)
- [ ] **T4.4.5** Test TaskExecutor with GeminiLlm (real API) (30 min)
- [ ] **T4.4.6** Test fallback behavior (15 min)
- [ ] **T4.4.7** Create `tests/integration/test_all_providers.py` (30 min)
  - Test all 3 providers (Anthropic, OpenAI, Gemini)
  - Verify factory can instantiate all
  - Run comprehensive provider test suite

**Subtotal:** 2 hours

---

### 4.5 Performance Benchmarks (4 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 4 hours

- [ ] **T4.5.1** Create `benchmarks/gemini_comparison.py` (similar to OpenAI) (30 min)
- [ ] **T4.5.2** Implement subprocess benchmark (20 min)
- [ ] **T4.5.3** Implement direct LLM benchmark (20 min)
- [ ] **T4.5.4** Calculate statistics and improvement (20 min)
- [ ] **T4.5.5** Run benchmarks with real API (1 hour)
- [ ] **T4.5.6** Verify ≥30% improvement (15 min)
- [ ] **T4.5.7** Create `benchmarks/all_providers_comparison.py` (1 hour)
  - Compare all 3 providers
  - Generate comprehensive report
  - Validate all meet ≥30% target
- [ ] **T4.5.8** Document results (15 min)

**Subtotal:** 4 hours

---

### Phase 2B Quality Gate

**Exit Criteria:**
- [ ] **QG4.1** All Phase 2B tasks completed (32/32 checked)
- [ ] **QG4.2** GeminiLlm successfully calls Gemini API
- [ ] **QG4.3** TaskExecutor executes tasks via GeminiLlm
- [ ] **QG4.4** Performance benchmark shows ≥30% improvement
- [ ] **QG4.5** Test coverage ≥90% for gemini.py
- [ ] **QG4.6** All unit + integration tests pass
- [ ] **QG4.7** All 3 providers working (Anthropic, OpenAI, Gemini)
- [ ] **QG4.8** Comprehensive provider test passes

**Validation Commands:**
```bash
pytest tests/test_gemini.py tests/integration/test_executor_gemini.py -v
python benchmarks/gemini_comparison.py
python benchmarks/all_providers_comparison.py
pytest tests/integration/test_all_providers.py -v
```

---

## Phase 3: Script Deprecation (Week 3, 16 hours)

**Goal:** Gracefully deprecate execute_*.py scripts over 6 months

**Agent Assignments:**
- **codi-documentation-writer:** Tasks 5.1-5.20
- **senior-architect:** Tasks 5.21-5.28

**Deliverables:**
- ✅ Updated execute_*.py scripts with warnings
- ✅ Migration guide (2,000 words)
- ✅ Updated documentation
- ✅ Rollback procedure

---

### 5.1 Add Deprecation Warnings (2 hours)

**Agent:** codi-documentation-writer
**Time Estimate:** 2 hours

#### execute_claude.py

- [ ] **T5.1.1** Open `scripts/llm_execution/execute_claude.py` (5 min)
- [ ] **T5.1.2** Add deprecation warning at top of main() (20 min)
  - Use warnings.warn()
  - Include removal date (6 months from now)
  - Reference migration guide

- [ ] **T5.1.3** Test deprecation warning displays (10 min)

#### execute_gpt.py

- [ ] **T5.1.4** Open `scripts/llm_execution/execute_gpt.py` (5 min)
- [ ] **T5.1.5** Add deprecation warning (15 min)
- [ ] **T5.1.6** Test warning displays (10 min)

#### execute_gemini.py

- [ ] **T5.1.7** Open `scripts/llm_execution/execute_gemini.py` (5 min)
- [ ] **T5.1.8** Add deprecation warning (15 min)
- [ ] **T5.1.9** Test warning displays (10 min)

#### Set Removal Date

- [ ] **T5.1.10** Calculate removal date (6 months from Phase 3 completion) (5 min)
- [ ] **T5.1.11** Update all warnings with exact date (10 min)
- [ ] **T5.1.12** Document removal date in PROJECT-PLAN (10 min)

**Subtotal:** 2 hours

---

### 5.2 Create Migration Guide (6 hours)

**Agent:** codi-documentation-writer
**Time Estimate:** 6 hours

#### Setup

- [ ] **T5.2.1** Create `docs/EXECUTOR-MIGRATION-GUIDE.md` file (5 min)
- [ ] **T5.2.2** Add document header and metadata (10 min)

#### Content Sections

- [ ] **T5.2.3** Write "Why Migrate?" section (30 min)
  - Performance improvements (30-50%)
  - Async support for Phase 1
  - Easier testing and maintenance

- [ ] **T5.2.4** Write "Before You Start" section (30 min)
  - Prerequisites (Python 3.10+, API keys)
  - Dependencies installation
  - Compatibility check

- [ ] **T5.2.5** Write "Step-by-Step Migration" section (1.5 hours)
  - Step 1: Enable direct LLM mode
  - Step 2: Test dual-mode execution
  - Step 3: Validate performance
  - Step 4: Remove feature flag (defaults to True)

- [ ] **T5.2.6** Write "Testing Your Migration" section (1 hour)
  - Unit test examples
  - Integration test examples
  - Performance benchmark examples

- [ ] **T5.2.7** Write "Rollback Procedure" section (30 min)
  - How to revert to script execution
  - When to rollback
  - Validation after rollback

- [ ] **T5.2.8** Write "Troubleshooting" section (1 hour)
  - Missing API keys
  - Missing dependencies
  - Provider unavailability
  - Performance not as expected

- [ ] **T5.2.9** Write "FAQ" section (45 min)
  - When will scripts be removed?
  - What if I can't migrate by Month 6?
  - How do I get help?
  - Can I use both modes simultaneously?

- [ ] **T5.2.10** Add code examples throughout (30 min)

#### Review & Polish

- [ ] **T5.2.11** Proofread and edit (30 min)
- [ ] **T5.2.12** Validate all code examples (15 min)
- [ ] **T5.2.13** Check word count (~2,000 words) (5 min)

**Subtotal:** 6 hours

---

### 5.3 Update Documentation (6 hours)

**Agent:** codi-documentation-writer
**Time Estimate:** 6 hours

#### README.md

- [ ] **T5.3.1** Update main README.md (1 hour)
  - Add section on new LLM abstraction layer
  - Update TaskExecutor usage examples
  - Reference migration guide

#### Architecture Documentation

- [ ] **T5.3.2** Update `docs/architecture/ORCHESTRATION.md` (1 hour)
  - Document new architecture
  - Update diagrams (if applicable)
  - Explain dual-mode execution

#### API Documentation

- [ ] **T5.3.3** Update API docs for TaskExecutor (1 hour)
  - Document new methods (_execute_via_llm, _build_messages_from_task)
  - Update _execute_api documentation
  - Add feature flag documentation

- [ ] **T5.3.4** Create API docs for LlmFactory (45 min)
- [ ] **T5.3.5** Create API docs for AnthropicLlm (30 min)
- [ ] **T5.3.6** Create API docs for OpenAILlm (30 min)
- [ ] **T5.3.7** Create API docs for GeminiLlm (30 min)

#### Developer Guide

- [ ] **T5.3.8** Update developer guide (1 hour)
  - How to use new TaskExecutor
  - How to add new LLM providers
  - Best practices for async execution

**Subtotal:** 6 hours

---

### 5.4 Create Rollback Procedure (2 hours)

**Agent:** senior-architect
**Time Estimate:** 2 hours

#### Rollback Documentation

- [ ] **T5.4.1** Create `docs/EXECUTOR-ROLLBACK-PROCEDURE.md` file (5 min)
- [ ] **T5.4.2** Add document header (5 min)
- [ ] **T5.4.3** Write "Quick Rollback" section (30 min)
  - Feature flag approach
  - Code examples
  - Verification steps

- [ ] **T5.4.4** Write "Full Rollback" section (30 min)
  - Git revert procedure
  - Commit SHAs to revert
  - Validation after revert

- [ ] **T5.4.5** Write "When to Rollback" section (20 min)
  - Critical bugs
  - Performance regressions
  - Provider unavailability

#### Testing Rollback Procedure

- [ ] **T5.4.6** Test quick rollback (feature flag) (20 min)
- [ ] **T5.4.7** Validate scripts still work (10 min)
- [ ] **T5.4.8** Document test results (10 min)

**Subtotal:** 2 hours

---

### Phase 3 Quality Gate

**Exit Criteria:**
- [ ] **QG5.1** All Phase 3 tasks completed (28/28 checked)
- [ ] **QG5.2** All execute_*.py scripts display deprecation warnings
- [ ] **QG5.3** Migration guide reviewed and approved (~2,000 words)
- [ ] **QG5.4** Documentation updated (README, architecture, API, developer guide)
- [ ] **QG5.5** Rollback procedure tested and validated
- [ ] **QG5.6** Removal date documented (6 months from Phase 3 completion)

**Validation Commands:**
```bash
echo '{}' | python scripts/llm_execution/execute_claude.py 2>&1 | grep -i deprecat
cat docs/EXECUTOR-MIGRATION-GUIDE.md | wc -w
./docs/EXECUTOR-ROLLBACK-PROCEDURE.sh --dry-run
```

---

## Phase 4: Testing & Polish (Week 4, 16 hours)

**Goal:** Comprehensive testing, performance validation, and production readiness

**Agent Assignments:**
- **codi-test-engineer:** Tasks 6.1-6.15
- **security-specialist-agent:** Tasks 6.16-6.20
- **senior-architect:** Tasks 6.21-6.28

**Deliverables:**
- ✅ Integration test report
- ✅ Performance validation report
- ✅ Load test report
- ✅ Security review report
- ✅ Production readiness checklist
- ✅ Phase 1 foundation validation

---

### 6.1 Integration Testing (4 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 4 hours

#### Test Suite Execution

- [ ] **T6.1.1** Run all unit tests (30 min)
  - `pytest tests/ -m "not integration" -v`
  - Verify 100% pass rate

- [ ] **T6.1.2** Run all integration tests (1 hour)
  - `pytest tests/integration/ -v`
  - Requires all 3 API keys
  - Verify 100% pass rate

- [ ] **T6.1.3** Run coverage report (30 min)
  - `pytest --cov=llm_abstractions --cov=orchestration --cov-report=html`
  - Verify ≥90% coverage for new code

#### Integration Test Report

- [ ] **T6.1.4** Create `test-results/integration-test-report.md` (1 hour)
  - Summary of test results
  - Pass/fail rates
  - Coverage metrics
  - Issues found (if any)

- [ ] **T6.1.5** Document any test failures (30 min)
  - Root cause analysis
  - Remediation plan

**Subtotal:** 4 hours

---

### 6.2 Performance Validation (4 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 4 hours

#### Run All Benchmarks

- [ ] **T6.2.1** Run Anthropic benchmarks (45 min)
  - Execute 20 iterations
  - Calculate statistics
  - Verify ≥30% improvement

- [ ] **T6.2.2** Run OpenAI benchmarks (45 min)
- [ ] **T6.2.3** Run Gemini benchmarks (45 min)
- [ ] **T6.2.4** Run comprehensive provider comparison (45 min)

#### Performance Report

- [ ] **T6.2.5** Create `test-results/performance-validation.md` (1 hour)
  - Benchmark results table
  - Improvement percentages
  - Latency comparisons
  - Charts/graphs (optional)

- [ ] **T6.2.6** Validate all providers meet ≥30% target (15 min)

**Subtotal:** 4 hours

---

### 6.3 Load Testing (4 hours)

**Agent:** codi-test-engineer
**Time Estimate:** 4 hours

#### Load Test Setup

- [ ] **T6.3.1** Create `tests/load/test_concurrent_execution.py` (1 hour)
  - Test 100+ concurrent tasks
  - Use ThreadPoolExecutor or asyncio.gather
  - Measure throughput, latency, errors

#### Run Load Tests

- [ ] **T6.3.2** Run with Anthropic provider (45 min)
- [ ] **T6.3.3** Run with OpenAI provider (45 min)
- [ ] **T6.3.4** Run with Gemini provider (45 min)

#### Load Test Report

- [ ] **T6.3.5** Create `test-results/load-test-report.md` (45 min)
  - Concurrent tasks handled
  - Throughput (tasks/second)
  - Average latency
  - Error rate
  - Resource usage (memory, CPU)

**Subtotal:** 4 hours

---

### 6.4 Security Review (3 hours)

**Agent:** security-specialist-agent
**Time Estimate:** 3 hours

#### Code Review

- [ ] **T6.4.1** Review API key handling in LlmFactory (30 min)
  - Verify keys not logged
  - Verify keys not exposed in errors

- [ ] **T6.4.2** Review API key handling in all providers (30 min)
- [ ] **T6.4.3** Review error messages (30 min)
  - Ensure no sensitive data leaked
  - Check for information disclosure

- [ ] **T6.4.4** Review async/sync compatibility (30 min)
  - Check for race conditions
  - Validate thread safety

#### Security Report

- [ ] **T6.4.5** Create `test-results/security-review.md` (1 hour)
  - Findings (critical, high, medium, low)
  - Remediation recommendations
  - Sign-off or block

**Subtotal:** 3 hours

---

### 6.5 Production Readiness Review (4 hours)

**Agent:** senior-architect
**Time Estimate:** 4 hours

#### Checklist Creation

- [ ] **T6.5.1** Create `docs/PRODUCTION-READINESS-CHECKLIST.md` (1 hour)
  - Code quality checks
  - Test coverage checks
  - Performance validation
  - Security review
  - Documentation completeness
  - Rollback procedure tested
  - Deprecation warnings in place

#### Checklist Validation

- [ ] **T6.5.2** Validate code quality (30 min)
  - Run mypy type checker
  - Run black formatter
  - Check for TODO/FIXME comments

- [ ] **T6.5.3** Validate test coverage (30 min)
  - Review coverage report
  - Ensure ≥90% for new code

- [ ] **T6.5.4** Validate performance (30 min)
  - Review benchmark results
  - Confirm ≥30% improvement

- [ ] **T6.5.5** Validate security (30 min)
  - Review security report
  - Confirm no critical issues

- [ ] **T6.5.6** Validate documentation (30 min)
  - Review migration guide
  - Check API docs
  - Verify examples work

- [ ] **T6.5.7** Final sign-off (30 min)
  - Complete checklist
  - Approve for production deployment

**Subtotal:** 4 hours

---

### 6.6 Phase 1 Foundation Validation (1 hour)

**Agent:** senior-architect
**Time Estimate:** 1 hour

#### Foundation Validation

- [ ] **T6.6.1** Create `docs/PHASE-1-FOUNDATION-VALIDATION.md` (30 min)
  - Validate async/await support
  - Validate factory pattern ready for Message Bus
  - Validate provider abstraction supports future agents

- [ ] **T6.6.2** Document Phase 1 readiness (20 min)
  - What's ready now
  - What Phase 1 can build on
  - Any remaining gaps

- [ ] **T6.6.3** Final approval for Phase 1 foundation (10 min)

**Subtotal:** 1 hour

---

### Phase 4 Quality Gate (Final)

**Exit Criteria:**
- [ ] **QG6.1** All Phase 4 tasks completed (28/28 checked)
- [ ] **QG6.2** All integration tests pass (100% success rate)
- [ ] **QG6.3** Performance benchmarks show ≥30% improvement (all providers)
- [ ] **QG6.4** Load tests handle 100+ concurrent tasks without failures
- [ ] **QG6.5** Test coverage ≥90% for all new code
- [ ] **QG6.6** Security review finds no critical issues
- [ ] **QG6.7** API key handling follows best practices
- [ ] **QG6.8** Error messages don't leak sensitive data
- [ ] **QG6.9** Production readiness checklist 100% complete
- [ ] **QG6.10** Phase 1 Message Bus foundation validated
- [ ] **QG6.11** Final sign-off from senior-architect

**Production Deployment:**
- [ ] **DEPLOY1** Merge to main branch
- [ ] **DEPLOY2** Tag release (v1.0.0-executor-refactoring)
- [ ] **DEPLOY3** Deploy to production
- [ ] **DEPLOY4** Monitor for issues (24 hours)
- [ ] **DEPLOY5** Announce to users (migration guide)

**Rollback Safety:**
Set `use_direct_llm=False` globally if critical issues arise.

---

## Progress Tracking

### Daily Progress Template

```markdown
## Daily Progress - YYYY-MM-DD

**Phase:** [Phase Name]
**Day:** [Day X of Phase]

### Tasks Completed Today
- [x] T1.1.1: Create factory.py file
- [x] T1.1.2: Add module docstring

### Tasks In Progress
- [ ] T1.1.3: Import dependencies (75% complete)

### Blockers
- None

### Hours Logged
- rust-expert-developer: 6 hours
- codi-test-engineer: 0 hours

### Notes
- Factory implementation going smoothly
- Need to review provider registry structure tomorrow
```

### Weekly Progress Summary

```markdown
## Week 1 Progress Summary

**Phases Completed:**
- ✅ Phase 1A: Foundation (16/16 hours, 32/32 tasks)
- 🔄 Phase 1B: Dual-Mode Executor (12/16 hours, 28/34 tasks)

**Key Accomplishments:**
- LlmFactory fully implemented and tested
- AnthropicLlm working with real API
- TaskExecutor dual-mode 80% complete

**Metrics:**
- Total hours: 28/32 (87.5%)
- Test coverage: 92% (target: 90%)
- Integration tests: 100% pass rate

**Next Week:**
- Complete Phase 1B
- Start Phase 2A (OpenAI)
```

---

## Appendix

### Task Effort Estimation Guide

| Task Type | Time Estimate |
|-----------|---------------|
| File creation | 5-10 min |
| Module docstring | 5-10 min |
| Simple method implementation | 15-30 min |
| Complex method implementation | 45-90 min |
| Error handling | 20-30 min |
| Type hints | 20-30 min |
| Detailed docstrings | 30-60 min |
| Unit test (simple) | 10-15 min |
| Unit test (complex) | 20-30 min |
| Integration test | 20-40 min |
| Performance benchmark | 30-60 min |
| Documentation section | 30-60 min |
| Code review | 10-30 min |

### Abbreviations

| Abbrev | Meaning |
|--------|---------|
| **T** | Task |
| **QG** | Quality Gate |
| **min** | minutes |
| **hrs** | hours |

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-23 | Hal Casteel | Initial task list created (186 tasks) |

---

**Document Status:** ✅ READY FOR EXECUTION
**Last Updated:** 2025-11-23
**Next Review:** After Phase 1A completion
**Owner:** Hal Casteel, CEO/CTO, AZ1.AI INC.
