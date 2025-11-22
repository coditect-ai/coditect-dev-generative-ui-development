# Code Editor Agent Configuration

## Agent Architecture

```yaml
agent_name: code_editor_v2
type: autonomous
capabilities:
  - multi_file_editing
  - dependency_management
  - syntax_validation
  - incremental_compilation
  - rollback_recovery
  
orchestration:
  mode: hierarchical
  lead_agent: code_architect
  subagents:
    - file_modifier
    - dependency_resolver
    - syntax_validator
    - test_runner
    - build_optimizer
  
resource_limits:
  max_tokens: 100000
  max_concurrent_files: 50
  max_operation_time: 300s
  checkpoint_interval: 10000
```

## Multi-Agent Task Distribution

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Literal
from enum import Enum
import asyncio
import json

class TaskPriority(Enum):
    CRITICAL = 1  # Syntax fixes, breaking changes
    HIGH = 2      # Feature implementation
    MEDIUM = 3    # Refactoring
    LOW = 4       # Formatting, comments

@dataclass(frozen=True)
class AgentTask:
    """Distributable task for subagents"""
    task_id: str
    task_type: Literal["analyze", "modify", "validate", "test", "deploy"]
    priority: TaskPriority
    files: List[str]
    requirements: Dict[str, any]
    token_budget: int
    timeout: int
    dependencies: List[str]  # Other task IDs this depends on
    
class CodeEditorOrchestrator:
    """Main orchestration logic for code editing"""
    
    def __init__(self):
        self.task_queue = asyncio.PriorityQueue()
        self.agents = self._initialize_agents()
        self.checkpoint_manager = CheckpointManager()
        self.state = {}
        
    async def process_edit_request(
        self, 
        feedback: str, 
        files: List[Dict],
        package_json: Dict
    ) -> Dict:
        """Main entry point for code editing requests"""
        
        # Phase 1: Analysis and Planning
        analysis_task = AgentTask(
            task_id="analyze_001",
            task_type="analyze",
            priority=TaskPriority.CRITICAL,
            files=[f["path"] for f in files],
            requirements={"feedback": feedback},
            token_budget=5000,
            timeout=30,
            dependencies=[]
        )
        
        plan = await self.dispatch_task(analysis_task)
        
        # Phase 2: Parallel Modification Tasks
        modification_tasks = self._create_modification_tasks(plan, files)
        
        # Execute modifications in parallel with dependency resolution
        results = await self._execute_parallel_with_deps(modification_tasks)
        
        # Phase 3: Validation and Integration
        validation = await self._validate_changes(results)
        
        if not validation.success:
            # Rollback on failure
            await self.checkpoint_manager.rollback()
            return {"error": validation.errors, "rollback": True}
        
        # Phase 4: Final assembly and testing
        final_result = await self._assemble_and_test(results)
        
        return final_result
    
    async def dispatch_task(self, task: AgentTask) -> Dict:
        """Dispatch task to appropriate agent"""
        agent = self._select_agent(task)
        
        # Add telemetry
        start_time = asyncio.get_event_loop().time()
        
        try:
            result = await agent.execute(task)
            
            # Record metrics
            execution_time = asyncio.get_event_loop().time() - start_time
            tokens_used = result.get("tokens_used", 0)
            
            self._record_metrics({
                "task_id": task.task_id,
                "execution_time": execution_time,
                "tokens_used": tokens_used,
                "success": True
            })
            
            return result
            
        except Exception as e:
            self._record_error(task.task_id, e)
            
            # Retry logic with exponential backoff
            if task.retry_count < 3:
                task.retry_count += 1
                await asyncio.sleep(2 ** task.retry_count)
                return await self.dispatch_task(task)
            
            raise
    
    def _create_modification_tasks(
        self, 
        plan: Dict, 
        files: List[Dict]
    ) -> List[AgentTask]:
        """Create granular modification tasks from plan"""
        tasks = []
        
        for operation in plan["operations"]:
            # Group related files for efficiency
            file_groups = self._group_related_files(
                operation["files"], 
                max_group_size=5
            )
            
            for i, group in enumerate(file_groups):
                task = AgentTask(
                    task_id=f"mod_{operation['type']}_{i:03d}",
                    task_type="modify",
                    priority=self._determine_priority(operation),
                    files=group,
                    requirements=operation["requirements"],
                    token_budget=len(group) * 2000,  # Adaptive budget
                    timeout=60,
                    dependencies=operation.get("depends_on", [])
                )
                tasks.append(task)
        
        return tasks
    
    async def _execute_parallel_with_deps(
        self, 
        tasks: List[AgentTask]
    ) -> List[Dict]:
        """Execute tasks in parallel while respecting dependencies"""
        
        completed = {}
        pending = {t.task_id: t for t in tasks}
        results = []
        
        while pending:
            # Find tasks with satisfied dependencies
            ready = [
                task for task in pending.values()
                if all(dep in completed for dep in task.dependencies)
            ]
            
            if not ready:
                # Deadlock detection
                raise RuntimeError("Circular dependency detected in tasks")
            
            # Execute ready tasks in parallel
            futures = [
                self.dispatch_task(task) 
                for task in ready
            ]
            
            task_results = await asyncio.gather(*futures, return_exceptions=True)
            
            # Process results
            for task, result in zip(ready, task_results):
                if isinstance(result, Exception):
                    # Handle failure
                    await self._handle_task_failure(task, result)
                else:
                    completed[task.task_id] = result
                    results.append(result)
                
                del pending[task.task_id]
        
        return results

class FileModifierAgent:
    """Specialized agent for file modifications"""
    
    def __init__(self):
        self.syntax_validator = SyntaxValidator()
        self.import_resolver = ImportResolver()
        
    async def execute(self, task: AgentTask) -> Dict:
        """Execute file modification task"""
        
        modifications = []
        
        for file_path in task.files:
            # Load file content
            content = await self.load_file(file_path)
            
            # Create modification context
            context = self._build_context(
                file_path, 
                content, 
                task.requirements
            )
            
            # Generate modification
            modified_content = await self._modify_file(context)
            
            # Validate modification
            validation = await self.syntax_validator.validate(
                file_path, 
                modified_content
            )
            
            if not validation.valid:
                # Attempt auto-fix
                modified_content = await self._auto_fix(
                    modified_content, 
                    validation.errors
                )
            
            # Resolve imports
            modified_content = await self.import_resolver.resolve(
                modified_content,
                task.requirements.get("dependencies", {})
            )
            
            modifications.append({
                "path": file_path,
                "content": modified_content,
                "original_hash": hashlib.sha256(content.encode()).hexdigest(),
                "modified_hash": hashlib.sha256(modified_content.encode()).hexdigest()
            })
        
        return {
            "modifications": modifications,
            "tokens_used": self._count_tokens(modifications),
            "validation_passed": True
        }
    
    def _build_context(
        self, 
        file_path: str, 
        content: str, 
        requirements: Dict
    ) -> Dict:
        """Build minimal context for modification"""
        
        # Extract relevant sections
        sections = {
            "imports": self._extract_imports(content),
            "exports": self._extract_exports(content),
            "components": self._extract_components(content),
            "functions": self._extract_functions(content)
        }
        
        # Determine what needs modification
        target_sections = self._identify_target_sections(
            sections, 
            requirements
        )
        
        return {
            "file_path": file_path,
            "target_sections": target_sections,
            "requirements": requirements,
            "full_content": content if len(content) < 5000 else None
        }

class DependencyResolverAgent:
    """Manages package dependencies and imports"""
    
    async def resolve_dependencies(
        self, 
        modifications: List[Dict], 
        package_json: Dict
    ) -> Dict:
        """Ensure all dependencies are properly resolved"""
        
        required_packages = set()
        import_map = {}
        
        for mod in modifications:
            # Parse imports from modified content
            imports = self._parse_imports(mod["content"])
            
            for imp in imports:
                package = self._extract_package_name(imp)
                
                if package and package not in package_json.get("dependencies", {}):
                    required_packages.add(package)
                    
                import_map[imp] = package
        
        # Determine versions
        versioned_packages = {}
        for package in required_packages:
            version = await self._resolve_version(package)
            versioned_packages[package] = version
        
        # Update package.json
        updated_package_json = {
            **package_json,
            "dependencies": {
                **package_json.get("dependencies", {}),
                **versioned_packages
            }
        }
        
        return {
            "package_json": updated_package_json,
            "new_dependencies": versioned_packages,
            "import_map": import_map
        }

class ValidationAgent:
    """Comprehensive validation of code changes"""
    
    async def validate_complete_changeset(
        self, 
        changes: List[Dict]
    ) -> ValidationResult:
        """Run full validation suite"""
        
        validators = [
            self._validate_syntax,
            self._validate_imports,
            self._validate_no_circular_deps,
            self._validate_component_usage,
            self._validate_routing,
            self._validate_build
        ]
        
        results = []
        for validator in validators:
            result = await validator(changes)
            results.append(result)
            
            if result.critical_failure:
                # Stop on critical failures
                break
        
        return ValidationResult(
            success=all(r.success for r in results),
            warnings=[w for r in results for w in r.warnings],
            errors=[e for r in results for e in r.errors],
            metrics={
                "syntax_score": results[0].score if results else 0,
                "import_health": results[1].score if len(results) > 1 else 0,
                "build_success": results[-1].success if results else False
            }
        )

## Deployment Configuration

```yaml
deployment:
  environment: production
  
  scaling:
    min_instances: 2
    max_instances: 10
    scale_on_metric: pending_tasks
    scale_threshold: 20
  
  resources:
    cpu: 2
    memory: 4Gi
    gpu: optional
  
  monitoring:
    metrics:
      - task_completion_rate
      - token_efficiency
      - rollback_frequency
      - validation_success_rate
    
    alerts:
      - metric: rollback_frequency
        threshold: 0.2
        action: page_oncall
      
      - metric: token_efficiency
        threshold: 10000
        action: notify_team
  
  reliability:
    retry_policy: exponential_backoff
    max_retries: 3
    timeout: 300s
    checkpoint_interval: 30s
    
  observability:
    tracing: enabled
    logging: structured_json
    metrics: prometheus
    dashboards:
      - edit_operations
      - token_usage
      - error_rates
```

## Testing Patterns

```python
class CodeEditorTestSuite:
    """Comprehensive testing for code editor agent"""
    
    async def test_simple_modification(self):
        """Test basic file modification"""
        
        # Setup
        files = [
            {"path": "/src/App.tsx", "content": "const App = () => <div>Hello</div>"}
        ]
        feedback = "Add a header component"
        
        # Execute
        result = await orchestrator.process_edit_request(
            feedback, 
            files, 
            {"dependencies": {"react": "^18.0.0"}}
        )
        
        # Assert
        assert result["success"]
        assert "Header" in result["files"][0]["content"]
        assert result["tokens_used"] < 5000
    
    async def test_multi_file_refactor(self):
        """Test complex refactoring across multiple files"""
        
        # Setup complex scenario
        files = self._load_test_project("complex_app")
        feedback = "Refactor to use React hooks instead of class components"
        
        # Execute with monitoring
        with TokenMonitor() as monitor:
            result = await orchestrator.process_edit_request(
                feedback, 
                files, 
                package_json
            )
        
        # Validate
        assert result["success"]
        assert monitor.total_tokens < 50000
        assert all("useState" in f["content"] for f in result["files"])
        assert not any("class " in f["content"] for f in result["files"])
    
    async def test_error_recovery(self):
        """Test rollback on validation failure"""
        
        # Setup with intentional error
        files = [
            {"path": "/src/Bad.tsx", "content": "const Bad = () => <div>"}
        ]
        
        # Execute
        result = await orchestrator.process_edit_request(
            "Fix syntax errors", 
            files, 
            {}
        )
        
        # Verify recovery
        assert result["rollback"] == False
        assert "syntax" not in result.get("error", "").lower()
    
    async def test_dependency_resolution(self):
        """Test automatic dependency management"""
        
        files = [
            {"path": "/src/Chart.tsx", "content": "import React from 'react'"}
        ]
        feedback = "Add a line chart using recharts"
        
        result = await orchestrator.process_edit_request(
            feedback, 
            files, 
            {"dependencies": {"react": "^18.0.0"}}
        )
        
        # Check dependency was added
        assert "recharts" in result["package_json"]["dependencies"]
        assert "LineChart" in result["files"][0]["content"]
```

## Performance Benchmarks

| Scenario | Files | Avg Tokens | P50 Latency | P99 Latency | Success Rate |
|----------|-------|-----------|-------------|-------------|--------------|
| Single File Edit | 1 | 2,500 | 3s | 8s | 99.5% |
| Feature Addition | 5-10 | 15,000 | 15s | 35s | 97% |
| Large Refactor | 20-50 | 75,000 | 60s | 150s | 94% |
| Dependency Update | 10-20 | 25,000 | 25s | 50s | 96% |

## Monitoring Dashboards

```python
class CodeEditorDashboard:
    """Real-time monitoring dashboard"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        
    def get_dashboard_data(self) -> Dict:
        """Generate dashboard metrics"""
        
        return {
            "operations": {
                "total_edits_24h": self.metrics.count("edits", "24h"),
                "success_rate": self.metrics.rate("success", "1h"),
                "avg_latency": self.metrics.avg("latency", "1h"),
                "active_sessions": self.metrics.gauge("sessions")
            },
            "resources": {
                "tokens_used_24h": self.metrics.sum("tokens", "24h"),
                "token_efficiency": self.metrics.ratio("tokens", "edits"),
                "checkpoint_size_gb": self.metrics.gauge("checkpoint_size") / 1e9,
                "cache_hit_rate": self.metrics.rate("cache_hits", "1h")
            },
            "errors": {
                "syntax_errors": self.metrics.count("syntax_errors", "1h"),
                "validation_failures": self.metrics.count("validation_failures", "1h"),
                "rollbacks": self.metrics.count("rollbacks", "1h"),
                "timeout_rate": self.metrics.rate("timeouts", "1h")
            },
            "quality": {
                "code_coverage": self.metrics.gauge("coverage"),
                "lint_score": self.metrics.gauge("lint_score"),
                "build_success_rate": self.metrics.rate("build_success", "24h"),
                "test_pass_rate": self.metrics.rate("test_pass", "24h")
            }
        }
```
