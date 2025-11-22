---
name: code-editor
description: Autonomous code modification system with multi-file orchestration, dependency management, and checkpoint rollback. Use when implementing features requiring 3+ file changes with automatic dependency resolution and syntax validation.
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
metadata:
  token-multiplier: "15x"
  max-context-per-file: "5000"
  checkpoint-storage: ".coditect/checkpoints/"
  supported-languages: "Python, TypeScript, TSX, JSX, JavaScript, Rust"
---

# Code Editor Skill

Production-ready autonomous code modification agent with multi-file orchestration, dependency-aware modifications, and checkpoint recovery. Optimized for ~15x token multiplication in multi-agent systems.

## When to Use This Skill

✅ **Use code-editor when:**
- Implementing features with 3+ file modifications
- Need automatic dependency resolution (package.json, Cargo.toml)
- Want syntax validation before commit (Python, TS, TSX, JSX, Rust)
- Require rollback capability for safe autonomous editing
- Working on full-stack features (backend + frontend + tests)
- Need token-efficient incremental editing

❌ **Don't use code-editor when:**
- Single file changes (use Edit tool directly)
- Simple text replacements
- Documentation-only updates
- Quick bug fixes in 1-2 files

## Core Capabilities

### 1. Multi-File Orchestration
Coordinate changes across multiple files with dependency tracking.

**Example:**
```
Implementing user profile editing:
- Create ProfileEditor.tsx (frontend component)
- Create PUT /api/v5/users/me/profile (backend endpoint)
- Update package.json (add form validation library)
- Update Cargo.toml (add backend dependencies)
- All changes validated before commit
```

### 2. Checkpoint/Rollback System
Create state snapshots before modifications for safe rollback.

**Workflow:**
1. Create checkpoint → 2. Apply modifications → 3. Validate → 4. Rollback if errors

**Checkpoint Storage:** `.coditect/checkpoints/` (persists across sessions)

### 3. Syntax Validation
Multi-language syntax checking before commit:

| Language | Validator | Method |
|----------|-----------|--------|
| Python | AST parsing | `ast.parse(content)` |
| TypeScript | Type annotation detection | Pattern matching |
| TSX/JSX | React component validation | JSX pattern matching |
| JavaScript | Bracket matching | Structural validation |
| Rust | Cargo check | `cargo check` |

### 4. Dependency Management
Automatic package.json and Cargo.toml updates based on detected imports.

**Features:**
- Extract ES6 imports (`import X from 'Y'`)
- Extract CommonJS requires (`const X = require('Y')`)
- Extract Python imports (`from X import Y`)
- Extract Rust crate imports (`use crate::X`)
- Resolve versions with default version map
- Validate against existing dependencies

### 5. Token Optimization
Incremental editing with minimal context per file (max 5000 tokens).

**Token Budgets:**

| Scenario | Files | Budget | Typical Usage | Savings |
|----------|-------|--------|---------------|---------|
| Single Component | 1 | 2,500 | 1,800 | - |
| Simple Feature | 3-5 | 15,000 | 12,000 | 20% |
| Complex Feature | 5-10 | 30,000 | 25,000 | 37% |
| Small Refactor | 10-20 | 50,000 | 40,000 | 40% |
| Large Refactor | 20-50 | 100,000 | 85,000 | 45% |

**Optimization Techniques:**
- Extract minimal context (imports + relevant code + exports)
- Batch similar operations
- Validate incrementally

## Usage Pattern

### Step 1: Initialize Code Editor

```python
from code_editor import CodeEditorAgent

editor = CodeEditorAgent()
```

### Step 2: Define Edit Request

```python
result = await editor.process_edit_request(
    feedback="Add user profile editing with form validation",
    files=[
        {"path": "/src/App.tsx", "content": "..."},
        {"path": "/backend/src/handlers/users.rs", "content": "..."}
    ],
    package_json={"dependencies": {"react": "^18.2.0"}},
    cargo_toml={"dependencies": {"actix-web": "4.0"}}
)
```

### Step 3: Handle Result

```python
if result["success"]:
    # Apply changes
    for file in result["files"]:
        write_file(file["path"], file["content"])

    # Update dependencies
    write_file("package.json", result["package_json"])
    write_file("Cargo.toml", result["cargo_toml"])
else:
    # Rollback
    restored = await editor.restore_checkpoint(result["checkpoint_id"])
    print(f"Rolled back {len(restored)} files")
```

## Execution Workflow

### Phase 1: Analysis & Planning
- Parse feedback to identify required operations
- Determine operation types (create, modify, delete, rename)
- Estimate token usage
- Assess risk level (low, medium, high)
- Plan validation steps

### Phase 2: Execute Modifications
- Apply all edit operations atomically
- Track dependencies added/removed
- Maintain file integrity (checksums)

### Phase 3: Validation
- Syntax check all modified files
- Identify validation errors
- Attempt auto-fix for common issues

### Phase 4: Dependency Resolution
- Extract all imports from modified files
- Identify missing dependencies
- Resolve package versions
- Update package.json/Cargo.toml

### Phase 5: Final Validation
- Comprehensive quality check
- Syntax validation (all files must pass)
- Circular dependency detection
- Unused component detection
- Quality score (0.0-1.0, threshold: 0.5)

## Data Models

### CodeFile (Immutable)
```python
@dataclass(frozen=True)
class CodeFile:
    path: str          # File path
    content: str       # File content
    language: str      # File extension (py, ts, tsx, rs)
    size: int          # Content length
    checksum: str      # SHA-256 hash
```

### EditOperation (Atomic)
```python
@dataclass
class EditOperation:
    file_path: str
    operation_type: Literal["create", "modify", "delete", "rename"]
    old_content: Optional[str]
    new_content: Optional[str]
    line_range: Optional[tuple[int, int]]
    dependencies_added: List[str]
    dependencies_removed: List[str]
```

### EditPlan
```python
@dataclass
class EditPlan:
    objective: str                 # User's feedback
    operations: List[EditOperation]
    estimated_tokens: int          # Token budget
    risk_level: Literal["low", "medium", "high"]
    rollback_strategy: str         # "checkpoint_restore"
    validation_steps: List[str]    # Validation phases
```

## Integration with T2 Orchestrator

### Orchestrator Phase 3: Implementation

```
Phase 3: Implementation
├─ Use code-editor skill to implement ProfileEditor component
│  - Create src/components/ProfileEditor.tsx
│  - Update src/App.tsx imports
│  - Add form validation dependencies
│  - Checkpoint before/after modifications
│
├─ Use code-editor skill to implement backend endpoint
│  - Create backend/src/handlers/profile.rs
│  - Update Cargo.toml dependencies
│  - Validate Rust syntax
│
└─ Validate with TDD validator (tests must pass)
```

### Integration Workflow

1. **Orchestrator delegates** → Code editor generates code
2. **Code editor validates** → Syntax + dependencies
3. **TDD validator tests** → Run tests, check coverage
4. **Quality gate validates** → Security, performance, accessibility
5. **Completion gate validates** → All deliverables present

## Error Recovery

### Automatic Recovery
- Syntax errors → Auto-fix common issues (brackets, imports)
- Missing imports → Add required imports
- Circular deps → Restructure imports
- Build failures → Rollback to checkpoint

### Manual Recovery
```python
# On failure, restore previous state
if not result["success"]:
    restored = await editor.checkpoint_manager.restore_checkpoint(
        result["checkpoint_id"]
    )
    print(f"Restored {len(restored)} files to last checkpoint")
```

### Common Auto-Fixes
1. **Bracket Matching** - Fix unclosed brackets
2. **Import Resolution** - Add missing import statements
3. **Dependency Updates** - Auto-add to package.json/Cargo.toml
4. **Type Errors** - Add missing type annotations (TypeScript)

## Best Practices

### DO ✅
- Create checkpoints before major changes
- Validate syntax before returning
- Use minimal file context (extract imports + relevant code + exports)
- Batch similar operations (all creates, then modifies, then deletes)
- Remove unused code automatically
- Test in isolated environment first

### DON'T ❌
- Modify protected files (main.tsx, index.html, Cargo.toml [package] section)
- Skip dependency validation
- Ignore token budgets (max 100K per operation)
- Apply untested changes to production
- Forget error boundaries
- Use OPFS as primary storage (use FoundationDB)

## T2-Specific Patterns

### Frontend Feature Addition
```python
await editor.process_edit_request(
    feedback="""
    Add analytics dashboard with:
    - Dashboard.tsx component with charts
    - Route at /dashboard
    - Navigation link in Header.tsx
    - Use recharts for visualization
    - Use shadcn/ui for UI components
    """,
    files=existing_files,
    package_json=package_json
)
```

### Backend API Endpoint
```python
await editor.process_edit_request(
    feedback="""
    Add PUT /api/v5/users/me/profile endpoint:
    - Handler in backend/src/handlers/profile.rs
    - JWT auth middleware
    - FoundationDB session validation
    - Return updated user data
    """,
    files=backend_files,
    cargo_toml=cargo_toml
)
```

### Full-Stack Feature
```python
# Combine frontend + backend in single request
await editor.process_edit_request(
    feedback="""
    Implement user profile editing:

    Frontend:
    - ProfileEditor.tsx component with form validation
    - Update App.tsx routing
    - Add @hookform/resolvers dependency

    Backend:
    - PUT /api/v5/users/me/profile in profile.rs
    - Validate user owns session
    - Update FDB user record
    - Add validator crate dependency
    """,
    files=frontend_files + backend_files,
    package_json=package_json,
    cargo_toml=cargo_toml
)
```

## Performance Metrics

### Expected Success Rates
- Syntax validation: >95% accuracy
- Dependency resolution: >90% accuracy
- Rollback success: >99% reliability
- Token efficiency: 30-40% reduction vs manual

### Quality Thresholds
- Validation score >= 0.5 → PASS
- Validation score 0.5-0.8 → WARNING (manual review)
- Validation score < 0.5 → FAIL (automatic rollback)

### Monitoring
```python
# Track metrics
editor.metrics["successes"][-1]  # Last successful operation
editor.metrics["failures"]       # All failures

# Performance tracking
{
    "avg_execution_time": 15.3,    # seconds
    "success_rate": 0.94,          # 94% success
    "avg_tokens_per_file": 2500,
    "rollback_rate": 0.06          # 6% require rollback
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| High token usage | Reduce file context, batch operations |
| Validation failures | Check syntax validators installed (npm, cargo) |
| Slow execution | Enable parallel processing for independent files |
| Missing dependencies | Ensure package managers installed (npm, cargo) |
| Rollback loops | Review error patterns, adjust auto-fix rules |
| Checkpoint corruption | Verify `.coditect/checkpoints/` permissions |

## Alerts

- Token usage > 10K per file → Review scope
- Rollback rate > 20% → Check validation
- Execution time > 60s → Consider parallelization
- Validation score < 0.5 → Auto-rollback triggered

## Advanced Features

### 1. Incremental Context Extraction
```python
MAX_CONTEXT_PER_FILE = 5000

def extract_minimal_context(file: File) -> str:
    """Extract only necessary code sections"""
    sections = [
        get_imports(file),      # Import statements
        get_relevant_code(file), # Relevant functions/components
        get_exports(file)        # Export statements
    ]
    return '\n'.join(sections)
```

### 2. Batch Operations
```python
def batch_similar_changes(tasks: List[Task]) -> List[BatchOperation]:
    """Group similar modifications"""
    batches = defaultdict(list)

    for task in tasks:
        operation_type = classify_operation(task)
        batches[operation_type].append(task)

    return [
        BatchOperation(type=op_type, tasks=tasks)
        for op_type, tasks in batches.items()
    ]
```

### 3. Parallel File Processing
```python
# Process independent files in parallel
async with asyncio.TaskGroup() as tg:
    for file in files:
        tg.create_task(process_file(file))
```

## Reference Materials

- **Quickstart Guide:** See `quickstart.md` for quick start examples and API reference
- **Configuration Guide:** See `config.md` for agent configuration details
- **Implementation:** See `implementation.py` for Python source code (906 lines)

## Version History

- **v2.0** - Multi-agent orchestration, checkpoint system, T2 integration
- **v1.5** - Added TypeScript/TSX validation
- **v1.0** - Basic code editing with rollback

## License

MIT - Use freely in production with attribution

---

**Status:** Production-ready ✅
**Token Efficiency:** 30-40% reduction for multi-file features
**Integration:** T2 Orchestrator Phase 3 (Implementation)
**Checkpoint Storage:** `.coditect/checkpoints/` (session-aware, persistent)
