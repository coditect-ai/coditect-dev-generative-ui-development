# ADR-001: Async TaskExecutor Refactoring - CODITECT Core Framework

```yaml
Document: ADR-001-async-task-executor-refactoring
Version: 1.0.0
Purpose: Make TaskExecutor.execute() async to align with ProjectOrchestrator and enable Phase 1 autonomous agents
Audience: Engineering teams, architects, framework developers
Date Created: 2025-11-23
Status: ACCEPTED
Related ADRs: None (first ADR for coditect-core)
Related Documents:
  - PROJECT-PLAN-EXECUTOR-REFACTORING.md
  - ASYNC-EXECUTOR-STRATEGIC-PLAN.md
  - docs/03-project-planning/PROJECT-PLAN.md (Phase 1 Message Bus)
```

---

## Table of Contents
- [Executive Summary](#executive-summary)
- [Context and Problem Statement](#context-and-problem-statement)
- [Decision Drivers](#decision-drivers)
- [Considered Options](#considered-options)
- [Decision Outcome](#decision-outcome)
- [Consequences](#consequences)
- [Implementation Details](#implementation-details)
- [Validation and Compliance](#validation-and-compliance)

---

## Executive Summary

**Decision**: Make `TaskExecutor.execute()` an **async method** and convert all 7 execution-related methods to async/await pattern, eliminating the async/sync boundary that currently blocks true async orchestration.

**User Feedback Integration**:
> "I agree with your analysis. Please explicitly detail making `TaskExecutor.execute` async to align seamlessly with `ProjectOrchestrator.execute_task`'s async nature."

**Why This Matters**: This change is **foundational** for Phase 1 Message Bus autonomous agents. Without end-to-end async flow, agents cannot coordinate asynchronously, parallel task execution is impossible, and the system remains fundamentally human-in-the-loop.

**Key Principle**: Eliminate the `asyncio.run()` wrapper that creates new event loops for each task, enabling true async orchestration from `ProjectOrchestrator` → `TaskExecutor` → `LlmFactory` → `BaseLlm` providers.

---

## Context and Problem Statement

### The Challenge

The TaskExecutor refactoring project (PROJECT-PLAN-EXECUTOR-REFACTORING.md) is moving from subprocess-based `execute_*.py` scripts to direct LLM abstraction layer. However, the original plan left `TaskExecutor.execute()` as a **sync method** with an `asyncio.run()` wrapper:

**Current Architecture (Problematic):**
```python
# ProjectOrchestrator.execute_task() - SYNC
def execute_task(self, task_id: str, agent: Optional[str] = None) -> ExecutionResult:
    task = self.get_task(task_id)
    result = self.executor.execute(task, agent=agent)  # SYNC call
    return result

# TaskExecutor.execute() - SYNC
def execute(self, task: AgentTask, agent: Optional[str] = None) -> ExecutionResult:
    result = self._execute_via_llm(task, agent_config, result)  # SYNC
    return result

# TaskExecutor._execute_via_llm() - SYNC with asyncio.run() wrapper
def _execute_via_llm(self, task, agent_config, result):
    # Uses asyncio.run() to wrap async LLM calls
    if asyncio.get_event_loop().is_running():
        output = await provider.generate_content_async(messages)  # ASYNC
    else:
        output = asyncio.run(provider.generate_content_async(messages))  # SYNC → ASYNC
    return result
```

**Problems with This Architecture:**

1. **Event Loop Overhead**: `asyncio.run()` creates a **new event loop** for each task (~10-20ms overhead)
2. **Blocks Async Orchestration**: Cannot use `await` in `ProjectOrchestrator.execute_task()`, forcing sequential execution
3. **Prevents Parallel Execution**: 3 tasks take 6 seconds (sequential) instead of 2 seconds (parallel)
4. **Phase 1 Blocker**: Message Bus autonomous agents **require** async coordination

### Business Context

**Phase 1 Message Bus Requirements**:
- Async agent-to-agent task delegation
- Concurrent task queue processing
- Non-blocking orchestration (orchestrator remains responsive)
- Event-driven agent coordination

**Performance Goals**:
- Single task: 30-50% improvement (subprocess → direct LLM) ✅ Already achieved
- Parallel tasks: **3x improvement** (sequential → concurrent) ⏸️ Blocked by sync executor

**Strategic Alignment**:
- User explicitly requested async alignment with `ProjectOrchestrator`
- Foundation for $100K+ Phase 1 autonomous agent implementation
- Enables future async workflows (batch processing, pipeline orchestration)

**Risk of Not Changing**:
- Phase 1 Message Bus becomes architecturally impossible
- Performance gains limited to single-task scenarios
- Technical debt accumulates (async/sync boundaries multiply)

---

## Decision Drivers

### Mandatory Requirements (Must-Have)

1. **User Alignment** - User explicitly requested async executor to align with ProjectOrchestrator
2. **Phase 1 Foundation** - Message Bus autonomous agents require end-to-end async
3. **Performance** - Enable parallel task execution (3x speedup for concurrent tasks)
4. **Architecture Purity** - Eliminate async/sync boundaries and event loop overhead
5. **Future-Proofing** - Enable async workflows without future refactoring

### Important Goals (Should-Have)

6. **Backward Compatibility** - Maintain dual-mode execution (direct LLM + script fallback)
7. **Test Coverage** - 90%+ coverage with `pytest-asyncio`
8. **Budget Efficiency** - Minimize cost increase ($750 for 6 hours additional work)
9. **Timeline Impact** - Keep project within 4-5 weeks
10. **Developer Experience** - Clear async/await patterns throughout

### Nice-to-Have

11. **Real-time Responsiveness** - Orchestrator remains responsive during long-running tasks
12. **Observability** - Easy to trace async execution flows
13. **Error Handling** - Async exceptions properly propagated

---

## Considered Options

### Option 1: **Keep Sync Executor with asyncio.run() Wrapper** (REJECTED ❌)

**Architecture**:
```python
def execute(self, task):
    # Sync method
    result = asyncio.run(provider.generate_content_async(messages))
    return result
```

**Pros**:
- ✅ No signature changes (backward compatible)
- ✅ Minimal code changes (6-8 hours work)
- ✅ Simpler for sync callers

**Cons**:
- ❌ Creates new event loop per task (~10-20ms overhead)
- ❌ Blocks async orchestration (cannot use `await`)
- ❌ Prevents parallel task execution (3 tasks = 6s sequential)
- ❌ Makes Phase 1 Message Bus architecturally impossible
- ❌ User explicitly disagreed with this approach

**Decision**: **REJECTED** - User feedback and Phase 1 requirements make this non-viable.

---

### Option 2: **Hybrid Approach (Dual Sync/Async Methods)** (REJECTED ❌)

**Architecture**:
```python
def execute(self, task):
    # Sync method for backward compatibility
    return asyncio.run(self.execute_async(task))

async def execute_async(self, task):
    # Async method for new callers
    result = await self._execute_via_llm(task, agent_config, result)
    return result
```

**Pros**:
- ✅ Backward compatible (sync method still exists)
- ✅ Enables async callers to use `execute_async()`
- ✅ Gradual migration path

**Cons**:
- ❌ API confusion (two methods doing same thing)
- ❌ Sync method still creates event loop overhead
- ❌ Doubles maintenance burden (two code paths)
- ❌ Doesn't fully solve async/sync boundary problem

**Decision**: **REJECTED** - Adds complexity without solving core problem.

---

### Option 3: **Make TaskExecutor.execute() Async** (SELECTED ✅)

**Architecture**:
```python
async def execute(self, task):
    # Fully async method
    result = await self._execute_via_llm(task, agent_config, result)
    return result

async def _execute_via_llm(self, task, agent_config, result):
    # No asyncio.run() wrapper needed
    output = await provider.generate_content_async(messages)
    return result

# All callers updated
async def execute_task(self, task_id):
    result = await self.executor.execute(task)  # Async call
    return result
```

**Pros**:
- ✅ **Eliminates async/sync boundary** (no event loop overhead)
- ✅ **Enables parallel execution** (3 tasks = 2s concurrent vs 6s sequential)
- ✅ **Foundation for Phase 1** (Message Bus can coordinate async agents)
- ✅ **User-approved** (explicit alignment with ProjectOrchestrator)
- ✅ **Architecture purity** (async all the way through)
- ✅ **Future-proof** (enables all async workflows)

**Cons**:
- ❌ Breaking change (all callers must use `await executor.execute()`)
- ❌ Test migration required (pytest-asyncio for all tests)
- ❌ +6 hours work (+$750 budget increase)
- ❌ +3 days timeline (4.5 weeks vs 4 weeks)

**Decision**: **SELECTED** ✅ - Pros massively outweigh cons. Strategic alignment with user feedback and Phase 1 requirements.

---

## Decision Outcome

### Chosen Option

**Option 3: Make TaskExecutor.execute() Async** ✅

**Rationale**:

1. **User Alignment**: User explicitly requested async executor to align with ProjectOrchestrator
2. **Phase 1 Critical**: Message Bus cannot be built without async executor
3. **Performance**: 3x speedup for parallel tasks (6s → 2s for 3 concurrent tasks)
4. **ROI**: $750 investment enables $100K+ Phase 1 implementation (10x+ ROI)
5. **Architecture**: Eliminates technical debt before it accumulates

### Method Signature Changes

**7 Methods Converted to Async:**

1. `TaskExecutor.execute()` - Main entry point
2. `TaskExecutor._execute_via_llm()` - Direct LLM execution
3. `TaskExecutor._execute_api()` - API execution mode
4. `ProjectOrchestrator.execute_task()` - Orchestrator integration
5. `ProjectOrchestrator.execute_tasks_parallel()` - Batch execution (new)
6. `ProjectOrchestrator._execute_task_internal()` - Internal helper
7. Test helper methods - All async with `@pytest.mark.asyncio`

**Before (Sync):**
```python
def execute(
    self,
    task: AgentTask,
    agent: Optional[str] = None,
    mode: Optional[str] = None
) -> ExecutionResult:
    """Execute a single task using specified agent."""
    ...
```

**After (Async):**
```python
async def execute(
    self,
    task: AgentTask,
    agent: Optional[str] = None,
    mode: Optional[str] = None
) -> ExecutionResult:
    """
    Execute a single task using specified agent.

    Note:
        This method is async to enable concurrent task execution
        and seamless integration with async LLM providers.
    """
    ...
```

---

## Consequences

### Positive Consequences

1. **End-to-End Async Flow** ✅
   - No `asyncio.run()` wrappers
   - Single event loop throughout execution
   - True async orchestration enabled

2. **Parallel Task Execution** ✅
   ```python
   # 3 tasks execute concurrently
   tasks = [task1, task2, task3]
   results = await asyncio.gather(*[executor.execute(t) for t in tasks])
   # Time: 2s (concurrent) vs 6s (sequential) = 3x speedup
   ```

3. **Phase 1 Foundation** ✅
   - Message Bus can coordinate async agents
   - Agent-to-agent communication works
   - Non-blocking orchestration enabled

4. **Performance Gains** ✅
   - Single task: 30-50% improvement (already achieved)
   - Parallel tasks: **3x improvement** (new capability)
   - No event loop overhead (~10-20ms saved per task)

5. **Architecture Purity** ✅
   - Clean async/await pattern throughout
   - No sync/async boundaries
   - Future async workflows easy to add

### Negative Consequences

1. **Breaking Change** ⚠️
   - All callers must migrate to `await executor.execute()`
   - Synchronous callers must wrap in `asyncio.run()` externally
   - **Mitigation**: Comprehensive migration guide (docs/EXECUTOR-MIGRATION-GUIDE.md)

2. **Test Migration** ⚠️
   - All tests need `@pytest.mark.asyncio`
   - Test fixtures need async support
   - **Mitigation**: Automated test migration script + 6 hours allocated

3. **Budget Increase** ⚠️
   - Original: $10,000 (80 hours)
   - Updated: $10,750 (86 hours)
   - Delta: +$750 (+7.5%)
   - **Mitigation**: ROI is 10x+ (enables $100K+ Phase 1)

4. **Timeline Impact** ⚠️
   - Original: 4 weeks
   - Updated: 4.5 weeks
   - Delta: +3 days
   - **Mitigation**: Concentrated in Phase 1B, no impact to Weeks 2-4

### Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| **Async/await bugs** | Comprehensive test suite + mypy type checking |
| **pytest-asyncio issues** | Use latest version (0.23+), test early in Phase 1B |
| **Event loop conflicts** | Use `asyncio_mode=auto` in pytest.ini |
| **Parallel execution race conditions** | Add asyncio.Lock() for shared state, thorough testing |
| **Caller migration errors** | Migration guide + example code + rollback plan |

**Rollback Plan**:
If async refactoring causes critical issues:
1. Revert `TaskExecutor.execute()` to sync
2. Re-add `asyncio.run()` wrapper in `_execute_via_llm()`
3. Keep script execution as fallback
4. Defer async refactoring to Phase 2

---

## Implementation Details

### Phase 1B Updates (22 hours, up from 16 hours)

**Original Phase 1B Tasks:**
1. Add `_execute_via_llm()` method - 8 hours
2. Add async/sync compatibility layer - 4 hours
3. Write unit tests - 4 hours

**Updated Phase 1B Tasks:**
1. **Make `_execute_via_llm()` fully async** - 2 hours (remove asyncio.run())
2. **Make `TaskExecutor.execute()` async** - 4 hours (signature change + caller updates)
3. **Make `TaskExecutor._execute_api()` async** - 2 hours (await calls)
4. **Make `ProjectOrchestrator.execute_task()` async** - 2 hours (signature change)
5. **Update internal method calls with await** - 4 hours (orchestrator methods)
6. **Write async unit tests with pytest-asyncio** - 6 hours (test migration)
7. **Integration tests for async flow** - 2 hours (end-to-end async validation)

### Testing Strategy

**Add to requirements-dev.txt:**
```python
pytest-asyncio==0.23.0
```

**pytest.ini Configuration:**
```ini
[pytest]
asyncio_mode = auto
```

**Test Migration Example:**

**Before (Sync):**
```python
def test_execute_task():
    result = executor.execute(task)
    assert result.status == ExecutionStatus.SUCCESS
```

**After (Async):**
```python
@pytest.mark.asyncio
async def test_execute_task():
    result = await executor.execute(task)
    assert result.status == ExecutionStatus.SUCCESS
```

**Parallel Execution Test:**
```python
@pytest.mark.asyncio
async def test_parallel_execution():
    tasks = [AgentTask(title=f"Task {i}") for i in range(3)]

    start = time.time()
    results = await asyncio.gather(*[executor.execute(task) for task in tasks])
    end = time.time()

    assert all(r.status == ExecutionStatus.SUCCESS for r in results)
    assert end - start < 3.0  # Verify parallel execution (3 tasks in ~2s)
```

### Performance Benchmarks

**Baseline (Current Sync + asyncio.run()):**
```
Task 1: |---LLM API (2s)---|
Task 2:                     |---LLM API (2s)---|
Task 3:                                         |---LLM API (2s)---|
Total: 6s (sequential)
```

**Target (Fully Async):**
```
Task 1: |---LLM API (2s)---|
Task 2: |---LLM API (2s)---|
Task 3: |---LLM API (2s)---|
Total: 2s (concurrent) = 3x speedup
```

**Success Criteria:**
- ✅ Single task: 30%+ improvement (already validated)
- ✅ **Parallel tasks (3): <3s total (3x vs sequential)** ← NEW
- ✅ **No asyncio.run() wrappers in production code** ← NEW
- ✅ **pytest-asyncio test suite operational** ← NEW

### Budget & Timeline Impact

**Budget:**
- Original: $10,000 (80 hours)
- Updated: $10,750 (86 hours)
- Delta: +$750 (+7.5%)
- **Justification**: Enables $100K+ Phase 1 implementation (10x+ ROI)

**Timeline:**
- Original: 4 weeks
- Updated: 4.5 weeks
- Delta: +3 days (concentrated in Phase 1B)

**Week 1 (Updated):**
- Days 1-2: Phase 1A (Foundation) - 16 hours
- Days 3-5.5: Phase 1B (Async Executor) - 22 hours (+6 hours)

**Weeks 2-4:** No changes (providers already async-compatible)

---

## Validation and Compliance

### Validation Checklist

**Technical Validation:**
- [ ] All 7 methods converted to async
- [ ] All callers updated with `await`
- [ ] pytest-asyncio installed and configured
- [ ] All tests migrated to async
- [ ] Parallel execution test passes (<3s for 3 tasks)
- [ ] No asyncio.run() in production code
- [ ] Type hints updated (`async def` signatures)

**Performance Validation:**
- [ ] Single task: ≥30% improvement (vs subprocess)
- [ ] Parallel tasks: ≥3x improvement (vs sequential)
- [ ] Event loop overhead eliminated
- [ ] Benchmarks documented in test-results/

**Quality Validation:**
- [ ] Test coverage ≥90%
- [ ] Integration tests pass (all providers)
- [ ] No regression in backward compatibility (dual-mode still works)
- [ ] Documentation updated (migration guide, API docs)

**Phase 1 Validation:**
- [ ] ProjectOrchestrator.execute_task() is async
- [ ] Message Bus can call executor asynchronously
- [ ] Agent-to-agent coordination works
- [ ] Foundation report created (docs/PHASE-1-FOUNDATION-VALIDATION.md)

### Compliance Requirements

**Backward Compatibility:**
- Dual-mode execution maintained (direct LLM + script fallback)
- Feature flag `use_direct_llm` still controls execution path
- Script execution still works (deprecated but functional)

**Migration Support:**
- Migration guide published: docs/EXECUTOR-MIGRATION-GUIDE.md
- Example code for async callers
- Rollback procedure documented

**Documentation:**
- ADR created (this document)
- ASYNC-EXECUTOR-STRATEGIC-PLAN.md comprehensive analysis
- PROJECT-PLAN-EXECUTOR-REFACTORING.md updated with async section
- API documentation reflects async signatures

---

## Links

### Related Documents

**Project Planning:**
- [PROJECT-PLAN-EXECUTOR-REFACTORING.md](../../PROJECT-PLAN-EXECUTOR-REFACTORING.md) - Complete refactoring plan
- [ASYNC-EXECUTOR-STRATEGIC-PLAN.md](../../docs/ASYNC-EXECUTOR-STRATEGIC-PLAN.md) - 62KB comprehensive async analysis
- [ASYNC-EXECUTOR-INTEGRATION-SECTION.md](../../docs/ASYNC-EXECUTOR-INTEGRATION-SECTION.md) - Integration instructions

**Phase 1 Context:**
- [docs/03-project-planning/PROJECT-PLAN.md](../../docs/03-project-planning/PROJECT-PLAN.md) - Overall CODITECT roadmap
- Phase 1 Message Bus requirements (autonomous agents)

**Code Locations:**
- `orchestration/executor.py` - TaskExecutor implementation
- `orchestration/orchestrator.py` - ProjectOrchestrator implementation
- `llm_abstractions/` - LLM provider implementations

**Testing:**
- `tests/test_executor_dual_mode.py` - Async executor tests
- `tests/integration/test_executor_anthropic.py` - Integration tests
- `benchmarks/executor_performance.py` - Performance benchmarks

### External References

**Best Practices:**
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [FastAPI async patterns](https://fastapi.tiangolo.com/async/) - Similar async architecture

**Multi-Agent Orchestration:**
- [docs/MULTI-AGENT-ARCHITECTURE-BEST-PRACTICES.md](../../docs/MULTI-AGENT-ARCHITECTURE-BEST-PRACTICES.md) - Research on async patterns

---

## Status History

| Date | Status | Author | Notes |
|------|--------|--------|-------|
| 2025-11-23 | PROPOSED | Claude Analysis | Initial draft based on user feedback |
| 2025-11-23 | ACCEPTED | Hal Casteel | User approved async executor approach |

---

## Approval

**Decision Maker:** Hal Casteel, CEO/CTO, AZ1.AI INC.

**Decision Status:** ✅ **ACCEPTED**

**Date Approved:** 2025-11-23

**Conditions for Approval:**
- ✅ User explicitly requested async alignment
- ✅ Budget increase approved ($750 for 6 hours)
- ✅ Timeline impact acceptable (+3 days)
- ✅ Phase 1 foundation critical path
- ✅ ROI validated (10x+ return)

**Implementation Authorization:**
- Proceed with Phase 1B async refactoring (22 hours)
- Budget: $10,750 (up from $10,000)
- Timeline: 4.5 weeks (up from 4 weeks)
- Next checkpoint: Phase 1B completion (end of Week 1)

---

**Document Status:** ✅ APPROVED
**Last Updated:** 2025-11-23
**Next Review:** After Phase 1B completion
**Owner:** Hal Casteel, CEO/CTO, AZ1.AI INC.
