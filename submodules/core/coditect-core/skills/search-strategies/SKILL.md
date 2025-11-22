---
name: search-strategies
description: Grep/Glob search optimization, file location strategies, and multi-stage search patterns. Use when searching codebase, locating files, or finding patterns across multiple files.
license: MIT
allowed-tools: [Grep, Glob, Read, Task]
metadata:
  token-efficiency: "Optimized search reduces token usage 60-80% (manual iteration → agent delegation)"
  integration: "All agents + Orchestrator - Fundamental skill for code navigation"
  tech-stack: "Grep/Glob patterns, regex, multi-stage search, agent coordination"
---

# Search Strategies

Expert skill for optimizing codebase searches using Grep, Glob, Read, and specialized agents.

## When to Use

✅ **Use this skill when:**
- Searching for specific function/class definitions (Grep: `"fn login_handler"`)
- Finding all files matching a pattern (Glob: `"**/*auth*.rs"`)
- Locating configuration values (Grep: `"DATABASE_URL"` with -C context)
- Multi-stage search needed (broad → narrow → deep)
- Uncertain which tool to use (decision tree helps)
- Need to avoid manual iteration waste (use agents for open-ended)
- Need time savings: 60-80% token reduction (manual → agent delegation)

❌ **Don't use this skill when:**
- Exact file path already known (just use Read tool directly)
- Simple single-file task (no search needed)
- Need deep analysis (use codebase-analyzer instead of search)

## Tool Selection Decision Tree

```
START
  │
  ├─ Do you know the exact file path?
  │  └─ YES → Use Read tool directly
  │
  ├─ Are you searching by filename pattern?
  │  └─ YES → Use Glob tool
  │       Examples: "**/*.rs", "src/**/*test*.ts"
  │
  ├─ Are you searching file contents?
  │  └─ YES → Use Grep tool
  │       Examples: "function login", "struct User"
  │
  ├─ Is this an open-ended search (may require multiple rounds)?
  │  └─ YES → Use codebase-locator or codebase-pattern-finder agent
  │       Agents can iterate and refine searches
  │
  └─ Need to understand HOW something works?
     └─ YES → Use codebase-analyzer agent
          Provides analysis, not just locations
```

## Search Tools Comparison

| Tool | Best For | Speed | Context | Example |
|------|----------|-------|---------|---------|
| **Read** | Exact file path known | Fastest | File contents | Read `backend/src/main.rs` |
| **Glob** | Filename patterns | Fast | File paths | `**/*.test.ts` |
| **Grep** | Content search | Medium | Matching lines | `"function login"` |
| **codebase-locator** | Open-ended search | Slower | Categorized results | "Find all auth files" |
| **codebase-pattern-finder** | Pattern extraction | Slower | Code examples | "Find CRUD patterns" |
| **codebase-analyzer** | Understanding code | Slowest | Analysis + context | "How does auth work?" |

## Multi-Stage Search Patterns

### Pattern 1: Broad → Narrow → Deep

**Stage 1: Broad (Glob)** - Find candidate files
```bash
Glob: "**/*auth*"
Result: 15 files (auth.rs, auth_middleware.rs, auth_test.rs, ...)
```

**Stage 2: Narrow (Grep)** - Filter by content
```bash
Grep: "login_handler" in previous 15 files
Result: 3 files contain "login_handler"
```

**Stage 3: Deep (Read)** - Examine details
```bash
Read: backend/src/handlers/auth.rs
Result: Full file with line numbers
```

### Pattern 2: Keyword → Context → Analysis

**Stage 1: Keyword (Grep)** - Find all occurrences
```bash
Grep: "JWT_SECRET" -output_mode: "files_with_matches"
Result: List of files using JWT_SECRET
```

**Stage 2: Context (Grep with -C)** - Get surrounding lines
```bash
Grep: "JWT_SECRET" -C: 5 -output_mode: "content"
Result: Matches with 5 lines before/after
```

**Stage 3: Analysis (codebase-analyzer)** - Understand usage
```bash
Agent: "Use codebase-analyzer to understand how JWT_SECRET is used across files"
Result: Analysis of JWT secret management with security implications
```

### Pattern 3: Parallel Search

**When:** Need different perspectives on same topic

```yaml
parallel_search:
  - tool: Glob
    pattern: "**/*session*"
    purpose: "Find all session-related files"

  - tool: Grep
    pattern: "create_session"
    purpose: "Find session creation code"

  - tool: Grep
    pattern: "invalidate_session"
    purpose: "Find session invalidation code"

merge_strategy: "Create comprehensive session management inventory"
```

## Search Optimization Rules

### Rule 1: Start Narrow, Expand if Needed

❌ **Bad: Start too broad**
```bash
Grep: "user"  # Too generic, 1000+ results
```

✅ **Good: Start specific**
```bash
Grep: "pub struct User"  # Precise, ~5 results
```

### Rule 2: Use Type Filtering

❌ **Bad: Search all files**
```bash
Grep: "function login"  # Searches all file types
```

✅ **Good: Filter by file type**
```bash
Grep: "function login" -type: "ts"  # TypeScript only
Grep: "fn login" -type: "rust"  # Rust only
```

### Rule 3: Leverage Glob for Structure

❌ **Bad: Grep for file paths**
```bash
Grep: "backend/src/handlers/"  # Wrong tool!
```

✅ **Good: Glob for structure**
```bash
Glob: "backend/src/handlers/*.rs"  # Correct tool
```

### Rule 4: Use Agents for Open-Ended Searches

❌ **Bad: Manual iteration**
```bash
# Try Grep
Grep: "authentication"
# Too many results, try narrower
Grep: "authentication handler"
# Still too many, try even narrower
Grep: "pub fn login"
# Multiple rounds, wasting tokens
```

✅ **Good: Use agent**
```bash
Task(
  subagent_type="codebase-locator",
  description="Find authentication handlers",
  prompt="Find all authentication-related handler functions in the backend"
)
# Agent iterates internally, returns refined results
```

## Search Strategy Selection

### Scenario: Find a Specific Function

**Goal:** Find the `login_handler` function

**Strategy:**
1. **Grep** for function definition: `"fn login_handler"` (Rust) or `"function login_handler"` (TypeScript)
2. If multiple matches, use `-n` flag for line numbers
3. **Read** the file at the correct line to see implementation

**Estimated tokens:** 2K-5K

### Scenario: Find All Test Files

**Goal:** Locate all test files in the project

**Strategy:**
1. **Glob** with pattern: `"**/*test*.{ts,rs}"`
2. Or **Glob** with pattern: `"**/*.test.ts"` for TypeScript tests
3. Or **Glob** with pattern: `"**/tests/**/*.rs"` for Rust test directory

**Estimated tokens:** 1K-2K

### Scenario: Understand Authentication System

**Goal:** Comprehensive understanding of how auth works

**Strategy:**
1. **codebase-locator** agent: "Find all authentication-related files"
2. **codebase-pattern-finder** agent: "Extract authentication patterns"
3. **codebase-analyzer** agent: "Analyze authentication flow"

**Estimated tokens:** 20K-30K (but provides comprehensive analysis)

### Scenario: Find Configuration Values

**Goal:** Find where `DATABASE_URL` is used

**Strategy:**
1. **Grep** with `-i` flag: `"DATABASE_URL"` (case-insensitive)
2. **Grep** with context: `"DATABASE_URL" -C: 3` to see usage context
3. Use `-type: "env"` or `-glob: "*.env*"` to search env files specifically

**Estimated tokens:** 1K-3K

### Scenario: Find Similar Implementations

**Goal:** Find other endpoints similar to `POST /auth/login`

**Strategy:**
1. **codebase-pattern-finder** agent: "Find all POST endpoint implementations"
2. Agent will extract patterns and provide examples
3. More efficient than manual Grep iteration

**Estimated tokens:** 10K-15K

## Common Search Mistakes

### Mistake 1: Using Wrong Tool

❌ **Using Grep for filenames**
```bash
Grep: "auth.rs"  # Searches file CONTENTS for string "auth.rs"
```

✅ **Use Glob for filenames**
```bash
Glob: "**/*auth*.rs"  # Finds files named "*auth*.rs"
```

### Mistake 2: Too Broad Initial Search

❌ **Broad search**
```bash
Grep: "error"  # Returns 10,000+ lines
```

✅ **Narrow search**
```bash
Grep: "ApiError::" -type: "rust"  # Specific error type in Rust files
```

### Mistake 3: Not Using Context Flags

❌ **No context**
```bash
Grep: "login_handler" -output_mode: "content"
# Just shows matching line, no context
```

✅ **With context**
```bash
Grep: "login_handler" -output_mode: "content" -C: 5
# Shows 5 lines before/after, easier to understand
```

### Mistake 4: Manual Iteration Instead of Agent

❌ **Manual iteration (wastes tokens)**
```bash
# Round 1
Grep: "session"  # Too many results

# Round 2
Grep: "create_session"  # Still many results

# Round 3
Grep: "pub fn create_session"  # Finally specific enough

# 3 tool calls, 3x token cost
```

✅ **Use agent (single delegation)**
```bash
Task(
  subagent_type="codebase-locator",
  description="Find session creation",
  prompt="Find all session creation functions in the backend"
)
# Agent iterates internally, returns refined results in ONE response
```

## Advanced Search Techniques

### Technique 1: Regex Patterns

**Use case:** Find all functions matching a pattern

```bash
# Find all handler functions
Grep: "fn \w+_handler" -type: "rust"

# Find all React components
Grep: "export (default )?function \w+" -type: "ts"

# Find all environment variables
Grep: "process\.env\.\w+" -type: "ts"
```

### Technique 2: Combining Grep Flags

**Use case:** Find tests for login functionality

```bash
Grep: "test.*login" -type: "rust" -output_mode: "files_with_matches"
# Finds test files containing "login"

# Then narrow down
Grep: "#\[test\]" -path: "tests/auth_test.rs" -output_mode: "content" -C: 10
# Shows test functions with context
```

### Technique 3: Search Result Refinement

**Use case:** Find critical security issues

```bash
# Stage 1: Find all password-related code
Grep: "password" -type: "rust" -output_mode: "files_with_matches"

# Stage 2: Look for potential plaintext passwords
Grep: "password.*=.*\"" -type: "rust" -output_mode: "content" -C: 3

# Stage 3: Analyze findings
# Use codebase-analyzer to determine if passwords are properly hashed
```

### Technique 4: Cross-File Pattern Analysis

**Use case:** Ensure consistency across modules

```bash
# Find all error handling patterns
Task(
  subagent_type="codebase-pattern-finder",
  description="Extract error patterns",
  prompt="Find all error handling patterns in backend handlers and check for consistency"
)
# Agent finds patterns and compares them across files
```

## Search Strategy Templates

### Template: API Endpoint Discovery

```yaml
search_strategy:
  goal: "Find all API endpoints in backend"
  steps:
    - tool: Glob
      pattern: "backend/src/handlers/*.rs"
      purpose: "Identify handler files"

    - tool: Grep
      pattern: "#\\[(get|post|put|delete)\\(\""
      type: "rust"
      purpose: "Find route decorators"

    - tool: Read
      files: "{results_from_grep}"
      purpose: "Extract full endpoint definitions"
```

### Template: Security Audit Search

```yaml
search_strategy:
  goal: "Security audit for authentication"
  steps:
    - agent: codebase-locator
      task: "Find all auth-related files"

    - tool: Grep
      pattern: "password|secret|token|jwt"
      files: "{results_from_agent}"
      case_sensitive: false

    - agent: codebase-analyzer
      task: "Analyze security of authentication implementation"
```

### Template: Dependency Usage Analysis

```yaml
search_strategy:
  goal: "Find all usages of actix-web crate"
  steps:
    - tool: Grep
      pattern: "use actix_web::"
      type: "rust"
      output: "files_with_matches"

    - tool: Grep
      pattern: "use actix_web::"
      type: "rust"
      output: "content"
      context: 2

    - agent: codebase-pattern-finder
      task: "Extract common actix-web usage patterns"
```

## Executable Scripts

See `core/optimize_search.py` for search strategy optimization.

## Best Practices

✅ **Know your tools** - Use the right tool for the job
✅ **Start specific** - Narrow searches are faster and more accurate
✅ **Use agents for iteration** - Don't waste tokens on manual refinement
✅ **Combine tools** - Glob → Grep → Read for efficient multi-stage searches
✅ **Use context flags** - `-C` flag provides surrounding lines for better understanding

❌ **Don't use Grep for filenames** - Use Glob instead
❌ **Don't start too broad** - Refine your search pattern first
❌ **Don't iterate manually** - Use agents for open-ended searches
❌ **Don't forget file type filters** - `-type` flag saves tokens

## Integration with Agents

**When to use search tools directly:**
- Exact file path known (Read)
- Simple filename pattern (Glob)
- Single keyword search (Grep)

**When to use agents:**
- Open-ended search requiring iteration
- Need to understand patterns across files (codebase-pattern-finder)
- Need analysis, not just locations (codebase-analyzer)
- Unclear what you're looking for (codebase-locator)

**Example agent invocation for complex search:**
```
Task(
  subagent_type="codebase-locator",
  description="Find session management",
  prompt="""Find all session management related code:
  - Session creation functions
  - Session validation logic
  - Session storage (FDB repositories)
  - Session expiration handling

  Return categorized file list with file:line references."""
)
```

## Troubleshooting

### Issue 1: Grep Returns Too Many Results

**Symptom:** 1000+ matches, unusable output

**Cause:** Search pattern too broad

**Fix:** Add type filter and narrow pattern
```bash
# WRONG: Too broad
Grep: "user"  # Matches "user", "username", "user_id" everywhere

# CORRECT: Specific pattern + type filter
Grep: "pub struct User" -type: "rust"  # Rust struct definitions only
Grep: "interface User" -type: "ts"     # TypeScript interfaces only
```

### Issue 2: Glob Pattern Not Matching Expected Files

**Symptom:** Glob returns empty or incomplete results

**Cause:** Incorrect glob syntax or case sensitivity

**Fix:** Verify glob pattern syntax
```bash
# WRONG: Missing wildcards
Glob: "backend/src/handlers"  # Matches directory, not files!

# CORRECT: Proper glob pattern
Glob: "backend/src/handlers/*.rs"  # Matches all .rs files
Glob: "backend/src/handlers/**/*.rs"  # Recursive match
```

### Issue 3: Manual Iteration Wasting Tokens

**Symptom:** 5+ Grep/Glob calls to find what you need

**Cause:** Not using agents for open-ended search

**Fix:** Delegate to codebase-locator agent
```bash
# WRONG: Manual iteration (30K tokens wasted)
Grep: "authentication"           # Too broad
Grep: "authentication handler"   # Still too many
Grep: "login_handler"           # Getting closer
Grep: "fn login_handler"        # Finally!

# CORRECT: Use agent (10K tokens, single delegation)
Task(
  subagent_type="codebase-locator",
  prompt="Find authentication handlers in backend"
)
```

**Token Savings:** 67% reduction (30K → 10K)

### Issue 4: Missing Context in Grep Results

**Symptom:** Grep shows matching line but can't understand usage

**Cause:** No context flags used

**Fix:** Add -C flag for surrounding lines
```bash
# WRONG: No context
Grep: "JWT_SECRET" -output_mode: "content"
# Result: Just "JWT_SECRET" on line 45

# CORRECT: With context
Grep: "JWT_SECRET" -output_mode: "content" -C: 5
# Result: 5 lines before + matching line + 5 lines after
```

### Issue 5: Searching Wrong Location

**Symptom:** Search returns no results but you know code exists

**Cause:** Searching wrong directory or file type

**Fix:** Verify search path and use path parameter
```bash
# Check project structure first
Glob: "**/*.rs"  # Find all Rust files

# Then narrow search
Grep: "login_handler" -path: "backend/" -type: "rust"
```

## Token Economics

**Manual Search vs Agent Delegation:**

| Search Type | Tool Calls | Token Cost | Time | Success Rate |
|-------------|-----------|-----------|------|--------------|
| Manual iteration (bad) | 5-10 Grep/Glob | 20K-40K | 15 min | 60% |
| Optimized manual (good) | 2-3 Grep/Glob | 5K-10K | 5 min | 80% |
| Agent delegation (best) | 1 Task | 8K-15K | 3 min | 95% |

**Recommendation:**
- Simple searches (1-2 tools): Use Grep/Glob directly
- Complex searches (3+ iterations expected): Use agents

**ROI Example:**
- Finding all auth files manually: 10 Grep calls = 30K tokens
- Using codebase-locator agent: 1 Task call = 12K tokens
- **Savings: 60% reduction (30K → 12K)**
