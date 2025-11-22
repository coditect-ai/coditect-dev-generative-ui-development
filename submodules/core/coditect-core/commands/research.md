---
name: research
description: Verification mode - executes focused tool calls to verify assumptions, check APIs exist, and validate technical choices before implementation
---

# RESEARCH MODE

Verify assumptions and validate technical approach for: $ARGUMENTS

## Mode Rules

### ✅ ALLOWED ACTIVITIES
- **Focused tool calls** (5-20 calls typical)
- **Read documentation** files
- **Check package existence** (npm, cargo, pip)
- **Verify API availability**
- **Validate approach feasibility**
- **Search for examples** in codebase

### ❌ FORBIDDEN ACTIVITIES
- **NO code implementation** - Verification only
- **NO full codebase refactoring** - Spot checks only
- **NO extensive modifications** - Research phase
- **NO production code** - Use IMPLEMENT mode for that

## Research Framework

### Phase 1: Package/Library Verification
```markdown
## Dependency Verification

### Required Packages
- [ ] `package-name` (version X.Y.Z)
  - Check: npm/cargo/pip search
  - Status: ✓ Exists / ✗ Missing
  - Alternative: [If missing]

### API Availability
- [ ] External API: `api.example.com/endpoint`
  - Check: Documentation read or test call
  - Status: ✓ Available / ✗ Deprecated / ⚠ Rate limited
```

### Phase 2: Technical Feasibility
```markdown
## Feasibility Checks

### Assumption 1: [Technical assumption]
**Verification method**: [How we'll check]
**Result**: [What we found]
**Confidence**: High / Medium / Low

### Assumption 2: [Another assumption]
[... repeat structure ...]

## Blockers Identified
- [Blocker 1]: [Description and potential workaround]
- [Blocker 2]: [Description and potential workaround]
```

### Phase 3: Example Discovery
```markdown
## Similar Implementations

### Example 1: [Description]
**Location**: file.ts:123-145
**Pattern**: [What pattern it uses]
**Applicable**: ✓ Yes / ✗ No / ⚠ Partially

### Example 2: [Description]
[... repeat structure ...]
```

## Research Strategies

### Strategy 1: Codebase Pattern Search
Use `search-strategies` skill for optimal search:
```
1. Glob for candidate files: "**/*auth*"
2. Grep for specific pattern: "async fn login"
3. Read implementation: auth.rs:45-120
4. Extract pattern
```

### Strategy 2: Documentation Verification
```
1. Read package.json / Cargo.toml / requirements.txt
2. Check version compatibility
3. Read docs for API changes
4. Verify example code still works
```

### Strategy 3: External API Check
```
1. Read API documentation
2. Check rate limits
3. Verify authentication method
4. Test with sample call (if safe)
```

## Output Structure

```markdown
# Research Report: [Feature/Task Name]

## Verification Summary
- **Packages**: X/Y verified, Z missing
- **APIs**: X/Y available, Z deprecated
- **Examples**: Found X similar implementations
- **Blockers**: X identified, Y resolved, Z remaining

## Detailed Findings

### Dependency Status
[See Phase 1 above]

### Technical Feasibility
[See Phase 2 above]

### Code Examples
[See Phase 3 above]

## Recommendations

### ✅ Proceed with Original Plan
[If all assumptions verified]

### ⚠ Modify Approach
**Changes needed**:
1. [Modification 1]
2. [Modification 2]

**Reason**: [Why original won't work]

### ✗ Blocked / Requires Discussion
**Blockers**:
1. [Critical blocker]

**Options**:
1. [Alternative 1]
2. [Alternative 2]

## Next Steps
**If verified**: Transition to ACTION mode (implementation)
**If blocked**: Escalate to user or revise approach in DELIBERATION
```

## Integration
- Auto-load: `search-strategies` skill (optimal search patterns)
- Auto-load: `codebase-locator` agent (if open-ended search needed)
- Use: Read, Grep, Glob tools

## Best Practices

✅ **DO**:
- Be systematic in verification
- Document what you checked
- Note version numbers
- Find concrete examples
- Identify blockers early
- Stay focused (5-20 calls max)

❌ **DON'T**:
- Start implementing
- Make hundreds of tool calls
- Assume without checking
- Skip version verification
- Ignore deprecation warnings
