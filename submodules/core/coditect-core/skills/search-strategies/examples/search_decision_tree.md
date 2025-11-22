# Search Decision Tree Examples

Real-world examples of choosing the right search tool.

## Example 1: Finding a Specific Function

**Goal:** Find the `create_session` function in Rust backend

### Decision Process
```
Q: Do I know the exact file?
A: No

Q: Am I searching by filename?
A: No, searching by content

Q: Is this a simple keyword search?
A: Yes - function name "create_session"

→ Use Grep tool
```

### Execution
```bash
# Step 1: Find function definition
Grep: "fn create_session" -type: "rust"
Result: backend/src/handlers/sessions.rs:45
        backend/src/db/repositories.rs:234

# Step 2: Read the implementation
Read: backend/src/handlers/sessions.rs (offset: 45, limit: 50)
```

**Tokens Used:** ~3K
**Time:** Fast (2 tool calls)

---

## Example 2: Finding All Test Files

**Goal:** Locate all test files in the project

### Decision Process
```
Q: Do I know the exact file?
A: No

Q: Am I searching by filename?
A: Yes - files with "test" in name or in tests/ directory

Q: What's the pattern?
A: **/*test*.{ts,rs} or **/tests/**/*

→ Use Glob tool
```

### Execution
```bash
# Find TypeScript test files
Glob: "**/*.test.ts"
Result: 23 files

# Find Rust test files
Glob: "**/tests/**/*.rs"
Result: 15 files
```

**Tokens Used:** ~1K
**Time:** Very fast (2 tool calls)

---

## Example 3: Understanding Authentication Flow

**Goal:** Understand how authentication works end-to-end

### Decision Process
```
Q: Do I know the exact file?
A: No

Q: Am I searching by filename?
A: No

Q: Is this a simple keyword search?
A: No - need to UNDERSTAND, not just locate

Q: Is this open-ended requiring analysis?
A: Yes

→ Use codebase-analyzer agent
```

### Execution
```bash
Task(
  subagent_type="codebase-analyzer",
  description="Analyze authentication flow",
  prompt="""Analyze the complete authentication flow:
  - Login endpoint
  - JWT generation
  - Session creation in FDB
  - Middleware validation
  - Token refresh

  Provide flow diagram with file:line references."""
)
```

**Tokens Used:** ~18K
**Time:** Slower but comprehensive (1 agent call)

---

## Example 4: Finding Environment Variable Usage

**Goal:** Find all places where `JWT_SECRET` is used

### Decision Process
```
Q: Do I know the exact file?
A: No

Q: Am I searching by filename?
A: No

Q: Is this a simple keyword search?
A: Yes - string literal "JWT_SECRET"

→ Use Grep tool
```

### Execution
```bash
# Step 1: Find all occurrences
Grep: "JWT_SECRET" -output_mode: "files_with_matches"
Result: 5 files

# Step 2: Get context
Grep: "JWT_SECRET" -output_mode: "content" -C: 5
Result: Matches with surrounding lines

# Analysis
Files:
- backend/src/main.rs:23 - Reading from env
- backend/src/middleware/auth.rs:45 - Using for JWT validation
- .env.example:10 - Documentation
- docker-compose.yml:34 - Environment variable
- k8s/secrets.yaml:12 - Kubernetes secret
```

**Tokens Used:** ~4K
**Time:** Fast (2 tool calls)

---

## Example 5: Finding Similar Implementations

**Goal:** Find all POST endpoint handlers to use as reference

### Decision Process
```
Q: Do I know the exact file?
A: No

Q: Am I searching by filename?
A: No

Q: Is this a simple keyword search?
A: No - need to find PATTERNS across files

Q: Need pattern extraction?
A: Yes

→ Use codebase-pattern-finder agent
```

### Execution
```bash
Task(
  subagent_type="codebase-pattern-finder",
  description="Extract POST endpoint patterns",
  prompt="""Find all POST endpoint implementations:
  - Extract common patterns
  - Show authentication handling
  - Show request validation
  - Show response formatting

  Return code examples with file:line references."""
)
```

**Tokens Used:** ~12K
**Time:** Moderate (1 agent call with pattern extraction)

---

## Example 6: Finding Configuration Files

**Goal:** Find all Docker and Kubernetes configuration files

### Decision Process
```
Q: Do I know the exact file?
A: No

Q: Am I searching by filename?
A: Yes - Docker and K8s config files

Q: What's the pattern?
A: docker-compose*.yml, Dockerfile*, k8s/*.yaml

→ Use Glob tool
```

### Execution
```bash
# Find Docker configs
Glob: "docker-compose*.yml"
Glob: "Dockerfile*"

# Find K8s configs
Glob: "k8s/**/*.yaml"

# Find all YAML configs
Glob: "**/*.{yml,yaml}"
```

**Tokens Used:** ~1K
**Time:** Very fast (multiple Glob calls)

---

## Example 7: Debugging a Specific Error

**Goal:** Find where "TransactionCommitError" is handled

### Decision Process
```
Q: Do I know the exact file?
A: No

Q: Am I searching by filename?
A: No

Q: Is this a simple keyword search?
A: Yes - error type "TransactionCommitError"

→ Use Grep tool
```

### Execution
```bash
# Step 1: Find error handling
Grep: "TransactionCommitError" -type: "rust" -output_mode: "content" -C: 5

# Step 2: Look for map_err usage
Grep: "map_err.*TransactionCommitError" -type: "rust"

# Results show error handling pattern
Result: backend/src/db/repositories.rs:156, 234, 445
        All using: .map_err(|e| ApiError::DatabaseError(format!("...", e)))
```

**Tokens Used:** ~3K
**Time:** Fast (2 tool calls)

---

## Example 8: Finding Dependencies

**Goal:** Find all files importing actix-web

### Decision Process
```
Q: Do I know the exact file?
A: No

Q: Am I searching by filename?
A: No

Q: Is this a simple keyword search?
A: Yes - import statement "use actix_web"

→ Use Grep tool
```

### Execution
```bash
# Find all actix-web imports
Grep: "use actix_web" -type: "rust" -output_mode: "files_with_matches"

# Find specific imports
Grep: "use actix_web::{web, HttpResponse}" -type: "rust"
```

**Tokens Used:** ~2K
**Time:** Fast (2 tool calls)

---

## Comparison Table

| Search Goal | Tool Choice | Tokens | Speed | Rationale |
|-------------|-------------|--------|-------|-----------|
| Find specific function | Grep | 3K | Fast | Simple content search |
| Find test files | Glob | 1K | Very fast | Filename pattern |
| Understand auth flow | Agent (analyzer) | 18K | Slow | Analysis needed |
| Find env var usage | Grep | 4K | Fast | Keyword search with context |
| Find similar patterns | Agent (pattern-finder) | 12K | Moderate | Pattern extraction |
| Find config files | Glob | 1K | Very fast | Filename pattern |
| Debug error handling | Grep | 3K | Fast | Keyword with context |
| Find dependencies | Grep | 2K | Fast | Import statement search |

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Using Grep for Filenames

**Bad:**
```bash
Grep: "auth.rs"  # Searches file CONTENTS for string "auth.rs"
```

**Good:**
```bash
Glob: "**/*auth*.rs"  # Finds files NAMED *auth*.rs
```

---

### ❌ Anti-Pattern 2: Too Broad Initial Search

**Bad:**
```bash
Grep: "error"  # 10,000+ results
```

**Good:**
```bash
# Be specific
Grep: "ApiError::" -type: "rust"

# Or use multiple stages
Glob: "**/*error*.rs"  # First find error-related files
Grep: "ApiError::" -path: "{glob_results}"  # Then search within
```

---

### ❌ Anti-Pattern 3: Manual Iteration Instead of Agent

**Bad:**
```bash
# Round 1
Grep: "session"  # Too many

# Round 2
Grep: "create_session"  # Still many

# Round 3
Grep: "pub fn create_session"  # Finally

# 3 tool calls = 9K tokens wasted
```

**Good:**
```bash
# Single agent call
Task(
  subagent_type="codebase-locator",
  description="Find session creation",
  prompt="Find all session creation functions"
)
# Agent iterates internally, returns refined results in ONE response
# 8K tokens, cleaner results
```

---

### ❌ Anti-Pattern 4: Reading Multiple Files Sequentially

**Bad:**
```bash
Read: "backend/src/handlers/auth.rs"
Read: "backend/src/handlers/sessions.rs"
Read: "backend/src/handlers/users.rs"
# 3 sequential reads = slow
```

**Good:**
```bash
# Use parallel tool calls
Read: "backend/src/handlers/auth.rs"
Read: "backend/src/handlers/sessions.rs"
Read: "backend/src/handlers/users.rs"
# All in ONE message = parallel execution
```

---

## Decision Tree Summary

```
START: What are you searching for?
│
├─ "I know the exact file path"
│  └─ Use: Read
│     Tokens: 1K-3K
│     Example: Read('backend/src/main.rs')
│
├─ "I'm searching by filename/pattern"
│  └─ Use: Glob
│     Tokens: 500-1K
│     Example: Glob('**/*.test.ts')
│
├─ "I'm searching for a keyword/string in files"
│  └─ Use: Grep
│     Tokens: 1K-5K
│     Example: Grep('fn login_handler', type='rust')
│
├─ "I need to find patterns across multiple files"
│  └─ Use: codebase-pattern-finder agent
│     Tokens: 10K-15K
│     Example: Task(subagent_type='general-purpose', prompt='Use codebase-pattern-finder subagent to')
│
├─ "I need to understand HOW something works"
│  └─ Use: codebase-analyzer agent
│     Tokens: 12K-20K
│     Example: Task(subagent_type='general-purpose', prompt='Use codebase-analyzer subagent to')
│
└─ "I'm not sure what I'm looking for (open-ended)"
   └─ Use: codebase-locator agent
      Tokens: 8K-12K
      Example: Task(subagent_type='codebase-locator')
```

---

## Best Practices

1. **Start with the cheapest tool that can solve the problem**
   - Known file → Read (1K)
   - Filename → Glob (500)
   - Keyword → Grep (2K)
   - Pattern → Agent (10K+)

2. **Use agents when iteration is likely**
   - Open-ended searches
   - Pattern extraction
   - Analysis tasks

3. **Combine tools efficiently**
   - Glob → Grep → Read (narrow down at each stage)
   - Parallel tool calls when independent

4. **Don't waste tokens on refinement**
   - If you find yourself running 3+ searches
   - Switch to an agent
   - Let it iterate internally
