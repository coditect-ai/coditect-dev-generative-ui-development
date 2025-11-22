---
name: code-analysis-planning-editor
description: Code analysis and planning editor for autonomous code modification with multi-file orchestration. Use when planning complex code changes across multiple files with dependency analysis.
version: 2.0.0
status: production
tags:
  - code-analysis
  - planning
  - autonomous
  - multi-file
  - dependency-analysis
---

# CODE_EDITOR Skill
*Autonomous Code Modification Agent for Production Systems*

## Overview
Production-grade skill for autonomous code editing with real-time preview capabilities, multi-file orchestration, and dependency-aware modifications. Optimized for token efficiency with checkpoint recovery.

## Core Capabilities

### 1. Code Analysis & Planning
- Multi-file dependency graph analysis
- Impact assessment before modifications
- Rollback capability with state snapshots
- Incremental change application

### 2. Modification Patterns
```python
@dataclass(frozen=True)
class CodeModificationTask:
    """Structured task for code modifications"""
    feedback: str
    target_files: List[str]
    constraints: List[str]
    dependencies: Dict[str, str]
    modification_scope: Literal["minimal", "feature", "refactor"]
    test_requirements: bool = True
    
    def to_prompt(self) -> str:
        return f"""
        TASK: {self.feedback}
        SCOPE: Modify {', '.join(self.target_files) if self.target_files else 'relevant files'}
        CONSTRAINTS: {'; '.join(self.constraints)}
        DEPENDENCIES: {json.dumps(self.dependencies)}
        MODE: {self.modification_scope}
        TESTS: {'Required' if self.test_requirements else 'Optional'}
        """
```

### 3. File Operation Templates
```python
class FileOperations:
    """Atomic file operations with rollback"""
    
    @staticmethod
    def create_file_change(
        path: str,
        content: str,
        operation: Literal["create", "modify", "delete"]
    ) -> Dict:
        return {
            "path": path,
            "content": content,
            "operation": operation,
            "timestamp": time.time(),
            "checksum": hashlib.sha256(content.encode()).hexdigest()
        }
    
    @staticmethod
    def validate_changes(changes: List[Dict]) -> bool:
        """Validate changes before application"""
        for change in changes:
            if change["operation"] == "modify":
                # Check syntax validity
                if not validate_syntax(change["content"], change["path"]):
                    return False
            # Check dependency consistency
            if not check_dependencies(change):
                return False
        return True
```

## Agent Configuration

### Primary Agent Prompt
```python
SYSTEM_PROMPT = """
You are an autonomous code editor with the following capabilities:
1. Multi-file code modifications with dependency awareness
2. Real-time preview integration understanding
3. Framework-specific best practices (React, Vue, Angular, etc.)
4. Automatic unused code removal
5. Import/export graph management

OPERATIONAL RULES:
- Plan modifications before execution
- Maintain working state at each step
- Use absolute file paths
- Remove unused imports/exports
- Ensure all components are rendered
- Validate against package.json dependencies
- Apply responsive design patterns
- Use specified UI libraries (shadcn/ui preference)

ERROR PREVENTION:
- Never modify protected files (main.tsx, index.html)
- Validate syntax before returning
- Check circular dependencies
- Ensure routing consistency
- Maintain backwards compatibility
"""
```

### Subagent Delegation Patterns

#### Pattern 1: Feature Implementation
```python
@dataclass
class FeatureImplementationTask:
    """Delegate complete feature implementation"""
    
    feature_description: str
    design_inspiration: str
    core_features: List[str]
    routing_requirements: bool
    ui_library: str = "shadcn/ui"
    
    def generate_subtasks(self) -> List[SubagentTask]:
        return [
            SubagentTask(
                objective=f"Create component architecture for: {feature}",
                output_format={"components": [], "routing": {}},
                tool_priorities=["file_create", "str_replace"],
                boundaries=["Use only installed dependencies"],
                effort_budget=10,
                success_criteria=["All components connected", "Routes defined"]
            )
            for feature in self.core_features
        ]
```

#### Pattern 2: Refactoring Operations
```python
@dataclass
class RefactoringTask:
    """Systematic code improvement"""
    
    refactor_type: Literal["performance", "maintainability", "modularity"]
    target_metrics: Dict[str, float]
    preserve_functionality: bool = True
    
    def execution_plan(self) -> Dict:
        return {
            "phases": [
                {"name": "analysis", "tools": ["view", "str_replace"], "budget": 5},
                {"name": "refactor", "tools": ["str_replace"], "budget": 15},
                {"name": "validation", "tools": ["bash_tool"], "budget": 5}
            ],
            "checkpoints": ["after_analysis", "after_each_file", "final"],
            "rollback_triggers": ["syntax_error", "test_failure", "build_failure"]
        }
```

## Token Optimization Strategies

### 1. Incremental Modifications
```python
class IncrementalEditor:
    """Token-efficient editing through incremental changes"""
    
    MAX_CONTEXT_PER_FILE = 5000
    
    def plan_edits(self, files: List[File], feedback: str) -> List[Edit]:
        """Generate minimal edit operations"""
        edits = []
        
        for file in files:
            if self.requires_modification(file, feedback):
                # Extract only relevant sections
                context = self.extract_minimal_context(file)
                edit = self.generate_edit(context, feedback)
                edits.append(edit)
        
        return self.optimize_edit_order(edits)
    
    def extract_minimal_context(self, file: File) -> str:
        """Extract only necessary code sections"""
        # Include imports, relevant functions/components, exports
        sections = []
        sections.append(self.get_imports(file))
        sections.append(self.get_relevant_code(file))
        sections.append(self.get_exports(file))
        return '\n'.join(sections)
```

### 2. Batch Operations
```python
class BatchEditor:
    """Batch similar operations for efficiency"""
    
    def batch_similar_changes(self, tasks: List[Task]) -> List[BatchOperation]:
        """Group similar modifications"""
        batches = defaultdict(list)
        
        for task in tasks:
            operation_type = self.classify_operation(task)
            batches[operation_type].append(task)
        
        return [
            BatchOperation(
                type=op_type,
                tasks=tasks,
                estimated_tokens=self.estimate_tokens(tasks)
            )
            for op_type, tasks in batches.items()
        ]
```

## Error Recovery Mechanisms

### 1. Syntax Validation
```python
class SyntaxValidator:
    """Pre-flight syntax checking"""
    
    VALIDATORS = {
        ".tsx": "typescript",
        ".jsx": "babel",
        ".py": "ast",
        ".vue": "vue-template-compiler"
    }
    
    async def validate_changes(self, changes: List[FileChange]) -> ValidationResult:
        """Validate all changes before application"""
        results = []
        
        for change in changes:
            ext = Path(change.path).suffix
            validator = self.VALIDATORS.get(ext)
            
            if validator:
                result = await self.run_validator(validator, change.content)
                results.append(result)
        
        return ValidationResult(
            valid=all(r.valid for r in results),
            errors=[r.error for r in results if r.error]
        )
```

### 2. Checkpoint System
```python
class CodeCheckpoint:
    """State preservation for rollback"""
    
    def __init__(self, storage_path: str = "/tmp/code_checkpoints"):
        self.storage = storage_path
        self.checkpoints = []
    
    async def create_checkpoint(self, state: Dict) -> str:
        """Create restoration point"""
        checkpoint_id = f"cp_{int(time.time())}_{hashlib.md5(str(state).encode()).hexdigest()[:8]}"
        
        checkpoint = {
            "id": checkpoint_id,
            "timestamp": time.time(),
            "files": state.get("files", {}),
            "dependencies": state.get("dependencies", {}),
            "metadata": state.get("metadata", {})
        }
        
        # Store checkpoint
        checkpoint_path = f"{self.storage}/{checkpoint_id}.json"
        async with aiofiles.open(checkpoint_path, 'w') as f:
            await f.write(json.dumps(checkpoint))
        
        self.checkpoints.append(checkpoint_id)
        return checkpoint_id
    
    async def rollback_to(self, checkpoint_id: str) -> bool:
        """Restore to specific checkpoint"""
        checkpoint_path = f"{self.storage}/{checkpoint_id}.json"
        
        if not os.path.exists(checkpoint_path):
            return False
        
        async with aiofiles.open(checkpoint_path, 'r') as f:
            checkpoint = json.loads(await f.read())
        
        # Restore files
        for path, content in checkpoint["files"].items():
            await self.restore_file(path, content)
        
        return True
```

## Quality Assurance

### 1. Change Validation Rules
```python
class ChangeValidator:
    """Comprehensive validation pipeline"""
    
    RULES = [
        ("no_protected_files", lambda c: "main.tsx" not in c.path),
        ("valid_imports", lambda c: validate_imports(c.content)),
        ("no_circular_deps", lambda c: check_circular_deps(c)),
        ("used_components", lambda c: check_component_usage(c)),
        ("dependency_match", lambda c: check_package_json(c))
    ]
    
    def validate(self, change: FileChange) -> ValidationResult:
        """Run all validation rules"""
        failures = []
        
        for rule_name, rule_func in self.RULES:
            if not rule_func(change):
                failures.append(rule_name)
        
        return ValidationResult(
            passed=len(failures) == 0,
            failures=failures
        )
```

### 2. Success Metrics
```python
@dataclass
class CodeEditMetrics:
    """Measure edit quality"""
    
    syntax_valid: bool
    tests_pass: bool
    build_success: bool
    dependencies_resolved: bool
    components_rendered: bool
    responsive_design: bool
    accessibility_score: float
    
    @property
    def success_score(self) -> float:
        """Composite success metric"""
        weights = {
            "syntax_valid": 0.3,
            "tests_pass": 0.2,
            "build_success": 0.2,
            "dependencies_resolved": 0.1,
            "components_rendered": 0.1,
            "responsive_design": 0.05,
            "accessibility_score": 0.05
        }
        
        score = 0
        for metric, weight in weights.items():
            value = getattr(self, metric)
            if isinstance(value, bool):
                score += weight if value else 0
            else:
                score += weight * value
        
        return score
```

## Usage Examples

### Example 1: Feature Addition
```python
async def add_dashboard_feature():
    """Add dashboard with table and chart"""
    
    task = CodeModificationTask(
        feedback="Add analytics dashboard with data table and chart visualization",
        target_files=["src/pages/Dashboard.tsx", "src/components/"],
        constraints=[
            "Use recharts for visualizations",
            "Use shadcn/ui for table",
            "Implement responsive design",
            "Add loading states"
        ],
        dependencies={"recharts": "^2.5.0", "@shadcn/ui": "latest"},
        modification_scope="feature"
    )
    
    # Create checkpoint before modification
    checkpoint = await checkpoint_system.create_checkpoint(current_state)
    
    try:
        # Execute modifications
        result = await code_editor.execute(task)
        
        # Validate result
        if await validator.validate_changes(result.files):
            await apply_changes(result.files)
            return result
        else:
            await checkpoint_system.rollback_to(checkpoint)
            raise ValidationError("Changes failed validation")
            
    except Exception as e:
        await checkpoint_system.rollback_to(checkpoint)
        raise
```

### Example 2: Refactoring Operation
```python
async def refactor_for_performance():
    """Optimize React components for performance"""
    
    refactor = RefactoringTask(
        refactor_type="performance",
        target_metrics={
            "bundle_size_reduction": 0.2,
            "render_time_reduction": 0.3,
            "memo_usage": 0.8
        }
    )
    
    plan = refactor.execution_plan()
    
    for phase in plan["phases"]:
        result = await execute_phase(phase)
        
        if phase["name"] in plan["checkpoints"]:
            await create_checkpoint(result)
        
        if check_rollback_trigger(result):
            await rollback_to_last_checkpoint()
            break
```

## Monitoring & Observability

### 1. Edit Tracking
```python
class EditTracker:
    """Track all code modifications"""
    
    def __init__(self):
        self.edits = []
        self.metrics = defaultdict(list)
    
    def record_edit(self, edit: Dict):
        """Record edit with metadata"""
        tracked_edit = {
            **edit,
            "timestamp": time.time(),
            "token_count": count_tokens(edit),
            "complexity_score": calculate_complexity(edit),
            "impact_radius": calculate_impact(edit)
        }
        
        self.edits.append(tracked_edit)
        self.update_metrics(tracked_edit)
    
    def get_efficiency_report(self) -> Dict:
        """Generate efficiency metrics"""
        return {
            "total_edits": len(self.edits),
            "avg_tokens_per_edit": np.mean(self.metrics["tokens"]),
            "success_rate": sum(self.metrics["success"]) / len(self.edits),
            "avg_complexity": np.mean(self.metrics["complexity"]),
            "rollback_rate": sum(self.metrics["rollbacks"]) / len(self.edits)
        }
```

### 2. Performance Metrics
```python
@dataclass
class PerformanceMetrics:
    """Code editor performance tracking"""
    
    edit_latency_p50: float
    edit_latency_p99: float
    token_efficiency: float  # Tokens per successful edit
    rollback_frequency: float
    validation_failure_rate: float
    
    def alert_thresholds(self) -> Dict[str, bool]:
        """Check if metrics exceed thresholds"""
        return {
            "high_latency": self.edit_latency_p99 > 30,
            "poor_token_efficiency": self.token_efficiency > 5000,
            "high_rollback": self.rollback_frequency > 0.2,
            "validation_issues": self.validation_failure_rate > 0.1
        }
```

## Best Practices

### DO
- Create checkpoints before major changes
- Validate syntax before returning
- Use minimal context for edits
- Batch similar operations
- Remove unused code automatically
- Apply framework best practices
- Include responsive design
- Add proper error boundaries

### DON'T
- Modify protected system files
- Make breaking changes without warning
- Ignore dependency constraints
- Create circular dependencies
- Skip validation steps
- Exceed token budgets
- Apply changes without testing
- Forget rollback mechanisms

## Integration Points

### 1. CI/CD Pipeline
```yaml
code_editor_integration:
  pre_commit:
    - syntax_validation
    - dependency_check
    - unused_code_removal
  
  pre_push:
    - build_verification
    - test_execution
    - performance_benchmarks
  
  post_merge:
    - production_validation
    - rollback_preparation
```

### 2. IDE Integration
```python
class IDEBridge:
    """Real-time IDE integration"""
    
    async def watch_changes(self, workspace: str):
        """Monitor file changes for validation"""
        async for change in watch_files(workspace):
            validation = await self.validator.validate(change)
            
            if not validation.passed:
                await self.notify_ide(validation.errors)
            
            # Auto-fix capability
            if self.auto_fix_enabled:
                fixed = await self.auto_fix(change, validation.errors)
                await self.apply_fix(fixed)
```

## Token Budget Guidelines

| Operation Type | Single File | Multi-File | Refactor |
|---------------|------------|------------|----------|
| Simple Edit | 500-1000 | 2000-5000 | 5000-10000 |
| Feature Add | 2000-5000 | 10000-20000 | 20000-50000 |
| Complex Refactor | 5000-10000 | 20000-50000 | 50000-100000 |

## Error Codes

| Code | Description | Recovery Action |
|------|-------------|-----------------|
| CE001 | Syntax validation failed | Rollback and retry with fixes |
| CE002 | Circular dependency detected | Restructure imports |
| CE003 | Missing dependencies | Update package.json |
| CE004 | Protected file modification | Skip file or request override |
| CE005 | Token budget exceeded | Batch operations or reduce scope |
| CE006 | Build failure | Check compilation errors |
| CE007 | Test failure | Fix failing tests |
| CE008 | Component not rendered | Update routing/imports |
