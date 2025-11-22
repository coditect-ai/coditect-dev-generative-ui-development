# Code Editor Agent - Quick Start Guide

## Overview
Production-ready autonomous code editing agent with multi-file orchestration, dependency management, and rollback capabilities. Optimized for ~15x token multiplication in multi-agent systems.

## Installation

```bash
# Core dependencies
pip install aiofiles --break-system-packages
pip install anthropic --break-system-packages

# Optional for enhanced validation
npm install -g typescript esprima @vue/compiler-sfc
```

## Quick Usage

```python
from code_editor_agent import CodeEditorAgent

# Initialize
editor = CodeEditorAgent()

# Simple edit request
result = await editor.process_edit_request(
    feedback="Add user authentication with login/signup forms",
    files=[{"path": "/src/App.tsx", "content": "..."}],
    package_json={"dependencies": {"react": "^18.2.0"}}
)

if result["success"]:
    for file in result["files"]:
        print(f"Modified: {file['path']}")
```

## Delegation Patterns

### 1. Feature Implementation
```python
# Delegate to subagent
task = {
    "objective": "Create complete dashboard with 3 charts and data table",
    "output_format": {"components": [], "routes": [], "dependencies": []},
    "tool_priorities": ["create_file", "str_replace"],
    "boundaries": ["Use only recharts and shadcn/ui"],
    "effort_budget": 15,
    "success_criteria": ["All components render", "Data flows correctly"]
}
```

### 2. Refactoring
```python
task = {
    "objective": "Convert class components to functional with hooks",
    "target_files": ["src/components/*.tsx"],
    "constraints": ["Preserve all functionality", "Maintain prop interfaces"],
    "validation": ["Tests must pass", "No type errors"],
    "checkpoint_after": 5  # Checkpoint every 5 files
}
```

### 3. Bug Fixing
```python
task = {
    "objective": "Fix all TypeScript errors in build",
    "auto_fix": True,
    "rollback_on_failure": True,
    "max_attempts": 3,
    "priority": "critical"
}
```

## Token Budgets

| Scenario | Files | Token Budget | Typical Usage |
|----------|-------|--------------|---------------|
| Single Component | 1 | 2,500 | 1,800 |
| Feature (Simple) | 3-5 | 15,000 | 12,000 |
| Feature (Complex) | 5-10 | 30,000 | 25,000 |
| Refactor (Small) | 10-20 | 50,000 | 40,000 |
| Refactor (Large) | 20-50 | 100,000 | 85,000 |

## API Reference

### Core Methods

```python
# Main editing function
async def process_edit_request(
    feedback: str,                    # User request/feedback
    files: List[Dict[str, str]],     # Current files
    package_json: Dict,               # Package configuration
    history: List[Dict] = None        # Conversation history
) -> Dict[str, Any]

# Checkpoint management
async def create_checkpoint(files: List[CodeFile]) -> str
async def restore_checkpoint(checkpoint_id: str) -> List[CodeFile]

# Validation
async def validate_syntax(file: CodeFile) -> Dict
async def check_dependencies(files: List[CodeFile]) -> List[str]
```

### Response Format

```python
{
    "success": bool,
    "plan": str,                      # Explanation of changes
    "files": [                        # Modified files
        {"path": str, "content": str}
    ],
    "package_json": str,              # Updated dependencies
    "checkpoint_id": str,             # For rollback
    "metrics": {
        "execution_time": float,
        "files_modified": int,
        "tokens_estimated": int,
        "validation_score": float
    }
}
```

## Error Handling

### Automatic Recovery
- Syntax errors → Auto-fix common issues
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
    print(f"Restored {len(restored)} files")
```

## Monitoring

### Key Metrics
```python
editor.metrics["successes"][-1]  # Last successful operation
editor.metrics["failures"]      # All failures

# Performance tracking
{
    "avg_execution_time": 15.3,    # seconds
    "success_rate": 0.94,          # 94% success
    "avg_tokens_per_file": 2500,
    "rollback_rate": 0.06          # 6% require rollback
}
```

### Alerts
- Token usage > 10k per file → Review scope
- Rollback rate > 20% → Check validation
- Execution time > 60s → Consider parallelization

## Best Practices

### DO
✅ Create checkpoints before major changes
✅ Validate syntax before returning
✅ Use minimal file context
✅ Batch similar operations
✅ Remove unused code
✅ Test in isolated environment first

### DON'T
❌ Modify protected files (main.tsx, index.html)
❌ Skip dependency validation
❌ Ignore token budgets
❌ Apply untested changes to production
❌ Forget error boundaries

## Common Patterns

### 1. Add Feature with Routing
```python
await editor.process_edit_request(
    feedback="""
    Add user profile page with:
    - Profile display component
    - Edit profile form
    - Route at /profile
    - Navigation link in header
    """,
    files=existing_files,
    package_json=package_json
)
```

### 2. Optimize Performance
```python
await editor.process_edit_request(
    feedback="""
    Optimize React performance:
    - Add React.memo to pure components
    - Implement useMemo for expensive computations
    - Add lazy loading for routes
    - Split large components
    """,
    files=existing_files,
    package_json=package_json
)
```

### 3. Add Testing
```python
await editor.process_edit_request(
    feedback="""
    Add unit tests for all components:
    - Use Jest and React Testing Library
    - Test user interactions
    - Test edge cases
    - Achieve 80% coverage
    """,
    files=existing_files,
    package_json=package_json
)
```

## Integration Examples

### With CI/CD
```yaml
# .github/workflows/code-review.yml
name: AI Code Review
on: pull_request

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run AI Code Editor
        run: |
          python -m code_editor_agent review \
            --feedback "${{ github.event.pull_request.title }}" \
            --validate-only
```

### With VSCode Extension
```javascript
// Extension command
vscode.commands.registerCommand('codeEditor.refactor', async () => {
    const feedback = await vscode.window.showInputBox({
        prompt: 'Describe the refactoring'
    });
    
    const result = await codeEditorAPI.process({
        feedback,
        files: getCurrentFiles(),
        packageJson: getPackageJson()
    });
    
    if (result.success) {
        await applyChanges(result.files);
    }
});
```

### With Chat Interface
```python
# Integrate with chat UI
async def handle_code_request(user_message: str, context: Dict):
    # Extract code context
    files = context.get("current_files", [])
    package_json = context.get("package_json", {})
    history = context.get("chat_history", [])
    
    # Process with agent
    result = await editor.process_edit_request(
        feedback=user_message,
        files=files,
        package_json=package_json,
        history=history
    )
    
    # Stream response
    if result["success"]:
        yield f"✅ Modified {len(result['files'])} files\n"
        yield f"📝 Changes: {result['plan']}\n"
        for file in result['files']:
            yield f"  - {file['path']}\n"
    else:
        yield f"❌ {result['error']}\n"
        yield f"↩️ Rolled back to checkpoint {result['checkpoint_id']}\n"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| High token usage | Reduce file context, batch operations |
| Validation failures | Check syntax validators installed |
| Slow execution | Enable parallel processing |
| Missing dependencies | Ensure npm/pip packages installed |
| Rollback loops | Review error patterns, adjust auto-fix |

## Performance Optimization

### 1. Context Reduction
```python
# Only include relevant file sections
def extract_minimal_context(file_content: str) -> str:
    return '\n'.join([
        extract_imports(file_content),
        extract_relevant_functions(file_content),
        extract_exports(file_content)
    ])
```

### 2. Parallel Processing
```python
# Process independent files in parallel
async with asyncio.TaskGroup() as tg:
    for file in files:
        tg.create_task(process_file(file))
```

### 3. Caching
```python
# Cache validation results
validation_cache = {}
if file.checksum in validation_cache:
    return validation_cache[file.checksum]
```

## Support

- **Documentation**: `/mnt/skills/code_editor/`
- **Examples**: `/mnt/skills/code_editor/examples/`
- **Tests**: `pytest tests/test_code_editor.py`
- **Logs**: `/var/log/code_editor/`

## Version History

- **v2.0** - Multi-agent orchestration, checkpoint system
- **v1.5** - Added TypeScript/TSX validation
- **v1.0** - Basic code editing with rollback

## License
MIT - Use freely in production with attribution
