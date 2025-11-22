---
name: document
description: Documentation generation mode - creates API docs, architecture diagrams, runbooks, and user guides
---

# Documentation Mode

Generate documentation for: $ARGUMENTS

## Documentation Types

### API Documentation
**Format**: OpenAPI 3.0 specification

```yaml
openapi: 3.0.0
info:
  title: API Name
  version: 1.0.0
paths:
  /resource:
    get:
      summary: Brief description
      parameters:
        - name: param
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
              example:
                id: "123"
                name: "Example"
```

### Architecture Documentation
**Format**: C4 diagrams + ADR

Use `framework-patterns` skill to generate:
- Context diagram (Level 1)
- Container diagram (Level 2)
- Component diagram (Level 3)

Include Architecture Decision Records for major decisions.

### Runbooks
**Format**: Step-by-step operational guides

```markdown
# Runbook: [Operation Name]

## Purpose
[What this runbook helps with]

## Prerequisites
- Access to [system/tool]
- Permissions: [required permissions]

## Steps

### 1. Check Status
```bash
# Command to check status
curl https://api/health
```

**Expected output**: `{"status": "healthy"}`

### 2. Perform Operation
```bash
# Command with explanation
./script.sh --param value
```

**If this fails**: [Troubleshooting steps]

### 3. Verify Success
[How to confirm operation succeeded]

## Rollback
[Steps to undo if needed]

## Common Issues
- **Error X**: [Cause and solution]
- **Error Y**: [Cause and solution]
```

### User Guides
**Format**: Task-oriented tutorials

```markdown
# How to [Task]

## Overview
[Brief description of what user will accomplish]

## Prerequisites
- [Requirement 1]
- [Requirement 2]

## Steps

### Step 1: [Action]
[Detailed instructions with screenshots if applicable]

```python
# Example code
result = do_thing()
```

**Expected outcome**: [What user should see]

### Step 2: [Next Action]
[Continue with detailed steps]

## Troubleshooting
**Problem**: [Common issue]
**Solution**: [How to fix]

## Next Steps
[What user can do after completing this guide]
```

### Integration
- Auto-load: `framework-patterns` skill (C4 diagrams)
- Auto-load: `evaluation-framework` skill (documentation quality rubric)

## Best Practices

✅ **DO**:
- Include concrete examples
- Add expected outputs/outcomes
- Provide troubleshooting sections
- Use clear, simple language
- Include diagrams for architecture
- Link to related documentation

❌ **DON'T**:
- Use jargon without explanation
- Skip error cases
- Forget to update version numbers
- Omit prerequisites
- Make assumptions about user knowledge
