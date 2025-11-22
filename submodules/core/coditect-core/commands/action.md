---
name: action
description: Implementation mode - emits working code in persistent artifacts, ONE artifact per response to prevent state explosion
---

# ACTION MODE

Implement working code for: $ARGUMENTS

## Mode Rules

### ✅ REQUIRED BEHAVIORS
- **ONE artifact per response** - Prevents state explosion
- **Emit working code** - Not pseudocode, actual implementation
- **Persistent artifacts** - Code that can be executed
- **Incremental progress** - Build up functionality step by step

### ❌ FORBIDDEN BEHAVIORS
- **NO planning** - Use DELIBERATION for that
- **NO verification** - Use RESEARCH for that
- **NO multiple artifacts** - State explosion risk
- **NO toy examples** - Production code only

## Action Framework

### Artifact Update vs Rewrite

**UPDATE (preferred)**:
- Small changes to existing code
- Bug fixes
- Adding single function
- Modifying one section

**REWRITE (only when necessary)**:
- Major refactoring
- File reorganization
- Complete redesign
- Previous version broken

### Code Quality Requirements
From `/implement` command:
- Full error handling with circuit breakers
- Async/await patterns (no blocking I/O)
- Type hints on all functions
- Observability hooks (metrics, logging)
- Checkpoint capabilities (if long-running)
- Unit tests included
- Inline documentation

### Iteration Pattern

```
User: "Implement feature X"

Response 1: [DELIBERATION complete - plan created]

Response 2: [RESEARCH complete - verified approach]

Response 3: [ACTION - File 1: core logic]
- ONE artifact: core.py
- Working implementation
- Tests included

Response 4: [ACTION - File 2: integration]
- ONE artifact: integration.py
- Uses core.py
- Tests included

Response 5: [ACTION - File 3: API endpoint]
- ONE artifact: api.py
- Exposes functionality
- Tests included

[Feature complete]
```

## Output Structure

```markdown
# Action: [Specific Implementation Step]

## What This Implements
[Brief description of this piece]

## Dependencies
- Requires: [Previous artifacts/files]
- Used by: [What will use this]

## Implementation

[ONE CODE ARTIFACT]
```python
# Artifact: filename.py
# Complete, working implementation

from typing import Optional
import asyncio

async def implementation():
    """Full implementation with all requirements"""
    # Implementation here
    pass

# Tests
async def test_implementation():
    """Test the implementation"""
    result = await implementation()
    assert result == expected
```

## Integration Points
[How this connects to other parts]

## Next Step
[What to implement next]
```

## Integration
- Auto-load: `production-patterns` skill (circuit breakers, error handling)
- Auto-load: `rust-backend-patterns` skill (if Rust)
- Auto-load: `foundationdb-queries` skill (if FDB)
- Follow: `/implement` command requirements

## State Tracking

Include in EVERY response:
```
CURRENT STATE:
- Phase: [current phase from deliberation]
- Active artifact: [filename of current artifact]
- Iteration: [which iteration number]
- Integration: [how pieces connect]
- Next: [what's next to implement]
```

## Best Practices

✅ **DO**:
- ONE artifact per response
- Include tests with code
- Add error handling
- Use type hints
- Document integration points
- Track state explicitly

❌ **DON'T**:
- Multiple artifacts in one response
- Skip tests
- Forget error handling
- Ignore production requirements
- Lose track of state
- Mix planning with implementation
