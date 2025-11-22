# Delegation Examples

Real-world delegation patterns for multi-agent coordination.

## Example 1: Full-Stack Feature Development

**Scenario:** Implement user profile editing feature

**Phase 1: Research (Parallel Delegation)**
```yaml
parallel_delegation:
  coordinator: orchestrator
  agents:
    - agent: codebase-locator
      task: "Find all user profile-related files (backend + frontend)"
      timeout: 5min
    - agent: codebase-pattern-finder
      task: "Extract CRUD patterns for user resources"
      timeout: 10min
    - agent: thoughts-locator
      task: "Find user profile requirements and design decisions"
      timeout: 3min
  aggregation_strategy: "Wait for all, create comprehensive feature plan"
```

**Phase 2: Implementation (Standard Delegation)**
```yaml
delegation:
  from_agent: orchestrator
  to_agent: orchestrator  # Self-delegation for implementation
  task:
    description: "Implement PUT /api/v5/users/me/profile endpoint"
    scope:
      - backend/src/handlers/users.rs
      - backend/src/db/repositories.rs
      - src/components/ProfileEditor.tsx
    deliverable: "Working backend + frontend with tests"
  context:
    current_phase: "Implementation"
    token_budget: 25000
    priority: HIGH
```

## Example 2: Bug Investigation

**Scenario:** Session timeout not working correctly

**Sequential Delegation Chain:**
```yaml
sequential_delegation:
  workflow: "Bug Fix - Session Timeout Issue #456"
  steps:
    - step: 1
      agent: codebase-locator
      task: "Find all session timeout-related code"
      output_to: step_2_input
    - step: 2
      agent: codebase-analyzer
      task: "Analyze session timeout logic in {step_2_input}"
      output_to: step_3_input
    - step: 3
      agent: codebase-pattern-finder
      task: "Find similar timeout implementations for comparison"
      output_to: step_4_input
    - step: 4
      agent: orchestrator
      task: "Implement fix based on analysis: {step_3_input} and patterns: {step_4_input}"
```

## Example 3: Security Audit

**Scenario:** Comprehensive authentication security review

**Phase 1: Inventory (Parallel)**
```yaml
parallel_delegation:
  coordinator: orchestrator
  agents:
    - agent: codebase-locator
      task: "Find all authentication-related files"
      timeout: 5min
    - agent: codebase-locator
      task: "Find all JWT-related code"
      timeout: 5min
    - agent: thoughts-locator
      task: "Find security requirements and past audit results"
      timeout: 3min
  aggregation_strategy: "Merge into comprehensive inventory"
```

**Phase 2: Analysis (Standard)**
```yaml
delegation:
  from_agent: orchestrator
  to_agent: codebase-analyzer
  task:
    description: "Analyze authentication implementation for OWASP Top 10 vulnerabilities"
    scope:
      - backend/src/handlers/auth.rs
      - backend/src/middleware/auth.rs
      - backend/src/db/repositories.rs (session methods)
    deliverable: "Security report with severity levels (CRITICAL, HIGH, MEDIUM, LOW)"
  context:
    current_phase: "Security Analysis"
    token_budget: 18000
    priority: CRITICAL
```

## Example 4: Deployment Validation

**Scenario:** Validate GKE deployment configuration

**Parallel Validation:**
```yaml
parallel_delegation:
  coordinator: orchestrator
  agents:
    - agent: codebase-analyzer
      task: "Analyze k8s manifests for security best practices"
      timeout: 10min
    - agent: codebase-analyzer
      task: "Validate environment variable configuration"
      timeout: 5min
    - agent: thoughts-locator
      task: "Find deployment checklists and requirements"
      timeout: 3min
  aggregation_strategy: "Create deployment validation report with pass/fail status"
```

## Example 5: Code Quality Improvement

**Scenario:** Refactor session management module

**Sequential Quality Chain:**
```yaml
sequential_delegation:
  workflow: "Code Quality - Session Management Refactor"
  steps:
    - step: 1
      agent: codebase-analyzer
      task: "Identify code smells in session management (backend/src/handlers/sessions.rs)"
      output_to: step_2_input
    - step: 2
      agent: codebase-pattern-finder
      task: "Find better patterns from similar modules"
      output_to: step_3_input
    - step: 3
      agent: orchestrator
      task: "Refactor based on smells: {step_2_input} using patterns: {step_3_input}"
      output_to: step_4_input
    - step: 4
      agent: orchestrator
      task: "Add tests for refactored code"
```

## Example 6: Documentation Generation

**Scenario:** Generate API documentation for new endpoints

**Parallel Documentation:**
```yaml
parallel_delegation:
  coordinator: orchestrator
  agents:
    - agent: codebase-analyzer
      task: "Extract API endpoint signatures from handlers/"
      timeout: 8min
    - agent: codebase-pattern-finder
      task: "Find existing API documentation format examples"
      timeout: 5min
    - agent: thoughts-locator
      task: "Find API design decisions and specifications"
      timeout: 3min
  aggregation_strategy: "Generate OpenAPI 3.0 specification with examples"
```

## Example 7: Migration Task

**Scenario:** Migrate from in-memory sessions to FDB sessions

**Complex Sequential Migration:**
```yaml
sequential_delegation:
  workflow: "Migration - In-Memory to FDB Sessions"
  steps:
    - step: 1
      agent: codebase-locator
      task: "Find all in-memory session usage"
      output_to: step_2_input
    - step: 2
      agent: codebase-analyzer
      task: "Analyze session data model and access patterns in {step_2_input}"
      output_to: step_3_input
    - step: 3
      agent: codebase-pattern-finder
      task: "Find FDB repository pattern examples"
      output_to: step_4_input
    - step: 4
      agent: orchestrator
      task: "Design FDB session schema based on {step_3_input}"
      output_to: step_5_input
    - step: 5
      agent: orchestrator
      task: "Implement FDB session repository using pattern: {step_4_input}"
      output_to: step_6_input
    - step: 6
      agent: orchestrator
      task: "Migrate all session access to FDB: {step_6_input}"
      output_to: step_7_input
    - step: 7
      agent: orchestrator
      task: "Add tests and validation for migrated sessions"
```

## Example 8: Emergency Hotfix

**Scenario:** Critical production bug - JWT tokens expiring too early

**Fast-Track Sequential:**
```yaml
sequential_delegation:
  workflow: "HOTFIX - JWT Expiration Bug"
  steps:
    - step: 1
      agent: codebase-locator
      task: "URGENT: Find JWT token generation code"
      output_to: step_2_input
    - step: 2
      agent: codebase-analyzer
      task: "URGENT: Analyze token expiration logic in {step_2_input}"
      output_to: step_3_input
    - step: 3
      agent: orchestrator
      task: "URGENT: Fix expiration calculation and create hotfix PR"
```

## Control Command Examples

### Example: High Token Usage

```
CONTROL: CHECKPOINT
REASON: Token usage at 136K/160K (85%), creating recovery point before TEST phase

Checkpoint ID: ckpt_auth_refactor_test_phase
State: CODE phase complete, entering TEST phase
Next: Run integration tests for authentication
```

### Example: Ambiguous Requirements

```
CONTROL: PAUSE
REASON: User requested "add caching" but didn't specify:
  - What to cache? (Sessions, user data, API responses?)
  - Cache backend? (Redis, in-memory, FDB?)
  - TTL strategy? (Fixed, sliding, none?)

Questions for user:
1. Which data should be cached?
2. What cache backend should we use?
3. What's the desired TTL?
```

### Example: Iteration Limit

```
CONTROL: ESCALATE
REASON: Iteration limit exceeded (10 attempts to fix compilation errors)

Summary:
- Attempted 10 different fixes for trait bound issue
- Each fix introduced new compilation errors
- Root cause unclear - may require manual code inspection

Request: Human review of trait bounds in backend/src/db/repositories.rs:450-500
```

### Example: Delegation

```
CONTROL: DELEGATE codebase-analyzer
REASON: Security audit requires specialized SAST analysis

Task: Analyze authentication handlers for OWASP Top 10 vulnerabilities
Scope: backend/src/handlers/auth.rs, backend/src/middleware/auth.rs
Deliverable: Security report with CRITICAL/HIGH/MEDIUM/LOW severity levels
Token Budget: 15K
```

## Best Practices from Real Usage

### ✅ DO: Parallel Research Phase

```yaml
# Good: Research in parallel, implement sequentially
parallel_delegation:
  coordinator: orchestrator
  agents:
    - agent: codebase-locator      # Fast (5 min)
    - agent: codebase-pattern-finder  # Medium (10 min)
    - agent: thoughts-locator      # Fast (3 min)
```

### ❌ DON'T: Parallel Implementation

```yaml
# Bad: Implementation should be sequential to avoid conflicts
parallel_delegation:
  coordinator: orchestrator
  agents:
    - agent: orchestrator  # Implementing backend
    - agent: orchestrator  # Implementing frontend
  # This causes race conditions and merge conflicts!
```

### ✅ DO: Clear Output Chaining

```yaml
# Good: Clear data flow between steps
sequential_delegation:
  steps:
    - step: 1
      task: "Locate files"
      output_to: step_2_input  # Clear what next step receives
    - step: 2
      task: "Analyze {step_2_input}"  # Explicit input usage
      output_to: step_3_input
```

### ❌ DON'T: Vague Tasks

```yaml
# Bad: Vague delegation
delegation:
  to_agent: codebase-analyzer
  task: "Look at the auth code"  # Too vague!
  deliverable: "Report"  # What kind of report?
```

### ✅ DO: Specific Deliverables

```yaml
# Good: Specific, measurable deliverable
delegation:
  to_agent: codebase-analyzer
  task: "Analyze authentication handlers for SQL injection vulnerabilities"
  deliverable: "Security report with file:line references, severity levels (CRITICAL/HIGH/MEDIUM/LOW), and fix recommendations"
```
