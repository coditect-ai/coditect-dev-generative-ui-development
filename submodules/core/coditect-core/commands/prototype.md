---
name: prototype
description: Rapid prototyping mode - builds quick proof-of-concept with focus on core functionality and fast iteration
---

# Prototype Mode

Build rapid prototype for: $ARGUMENTS

## Prototyping Guidelines

### Focus Areas
- **Core functionality only** - Skip edge cases initially
- **Fast iteration** - Optimize for learning, not production
- **Minimal dependencies** - Use standard library where possible
- **Clear TODO markers** - Document what's missing for production

### Acceptable Shortcuts
✅ **ALLOWED in prototypes**:
- Simplified error handling (basic try/catch)
- In-memory data structures (no persistence initially)
- Print statements for debugging
- Hardcoded config values
- TODO comments for production concerns

❌ **NEVER SKIP** (even in prototypes):
- Input validation (prevent crashes)
- Basic error messages (debuggability)
- Type hints (clarity)
- Core algorithm correctness
- Brief documentation

### Output Structure
```python
# Prototype: [Feature Name]
# Purpose: [What this proves/tests]
# Production TODO:
#   - Add circuit breakers for external calls
#   - Replace prints with structured logging
#   - Add comprehensive error handling
#   - Implement persistence (currently in-memory)
#   - Add metrics and observability

from typing import Optional

def prototype_function(input: str) -> Optional[dict]:
    """
    Prototype implementation of [feature].

    Args:
        input: Description

    Returns:
        Result or None if failed

    TODO: Production version needs:
        - Retry logic with backoff
        - Circuit breaker on external calls
        - Structured error types
    """
    try:
        # Core logic here
        result = process(input)
        print(f"✓ Processed: {result}")  # TODO: Replace with logger
        return result
    except Exception as e:
        print(f"✗ Error: {e}")  # TODO: Structured error handling
        return None
```

### Integration
- Auto-load: None (prototype mode is intentionally minimal)
- Use: Type hints for clarity
- Use: Input validation to prevent crashes

### Iteration Strategy
1. **Iteration 1**: Core happy path only
2. **Iteration 2**: Add basic error handling
3. **Iteration 3**: Add key edge cases
4. **Production**: Use `/implement` to build production version

## Best Practices

✅ **DO**:
- Mark all TODOs for production
- Validate inputs to prevent crashes
- Use type hints
- Keep it simple and focused
- Test the happy path
- Document assumptions

❌ **DON'T**:
- Over-engineer the prototype
- Spend time on perfect error handling
- Add complex abstractions
- Optimize prematurely
- Forget what needs production hardening
