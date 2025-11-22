---
name: implement
description: Production-ready implementation mode - builds code with full error handling, circuit breakers, async patterns, observability, and tests
---

# Implementation Mode

Build production-ready implementation for: $ARGUMENTS

## Implementation Requirements

### Code Quality Standards
- **Full error handling** with circuit breakers on external calls
- **Async/await patterns** - No blocking I/O
- **Type hints** on all functions (Python 3.11+)
- **Observability hooks** - Metrics, logging, tracing
- **Checkpoint capabilities** for long-running operations
- **Unit tests** included with >80% coverage
- **Inline documentation** with examples
- **Migration notes** in comments where applicable

### Architecture Patterns
- **Code style**: Production (not prototype/toy examples)
- **Framework**: Event-driven where applicable
- **Error handling**: Fail-fast with detailed context
- **Concurrency**: Bulkheads and timeout boundaries

### Integration
- Auto-load: `production-patterns` skill (circuit breakers, error handling)
- Auto-load: `rust-backend-patterns` skill (if Rust)
- Auto-load: `foundationdb-queries` skill (if FDB)
- Auto-load: `framework-patterns` skill (if event-driven/FSM)

### Quality Gates
| Aspect | Threshold | Action |
|--------|-----------|--------|
| Type coverage | < 100% | Reject - add type hints |
| Error handling | < 100% | Reject - add try/catch |
| Tests | < 80% coverage | Reject - add tests |
| Observability | Missing | Reject - add metrics/logs |
| Circuit breakers | Missing on external | Reject - add protection |

## Output Structure

```python
# 1. Imports with type hints
from typing import Optional, List
import asyncio

# 2. Error classes
class OperationError(ApplicationError):
    """Specific error with context"""
    pass

# 3. Implementation with full error handling
async def operation(input: str) -> Result:
    """
    Operation description with examples.

    Args:
        input: Description

    Returns:
        Result description

    Raises:
        OperationError: When X happens
    """
    # Observability
    metrics.increment("operation_calls", tags={"type": "user"})

    # Circuit breaker for external calls
    try:
        result = await circuit_breaker.call(external_call)
    except CircuitBreakerOpenError:
        logger.warning("Circuit open, using cache")
        return cached_result

    # Return
    return result

# 4. Tests
async def test_operation_success():
    result = await operation("test")
    assert result.status == "success"

async def test_operation_failure():
    with pytest.raises(OperationError):
        await operation("invalid")
```

## Best Practices

✅ **DO**:
- Include circuit breakers on all external calls
- Use async/await (no blocking time.sleep())
- Add observability hooks (metrics.increment, logger.info)
- Implement retries with exponential backoff
- Include comprehensive tests
- Document edge cases and error conditions

❌ **DON'T**:
- Skip error handling "for brevity"
- Use synchronous I/O
- Forget type hints
- Skip tests
- Ignore observability
- Use toy/prototype code patterns
