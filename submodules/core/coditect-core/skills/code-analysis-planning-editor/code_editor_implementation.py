"""
Code Editor Agent - Production Implementation
Autonomous code modification system with multi-agent orchestration
"""

import asyncio
import hashlib
import json
import os
import time
import aiofiles
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal, Any
from enum import Enum
from pathlib import Path
import ast
import re
from collections import defaultdict

# ============= Core Data Models =============

@dataclass(frozen=True)
class CodeFile:
    """Immutable file representation"""
    path: str
    content: str
    language: str
    size: int
    checksum: str
    
    @classmethod
    def from_path(cls, path: str, content: str) -> "CodeFile":
        """Create from file path and content"""
        return cls(
            path=path,
            content=content,
            language=Path(path).suffix.lstrip('.'),
            size=len(content),
            checksum=hashlib.sha256(content.encode()).hexdigest()
        )

@dataclass
class EditOperation:
    """Atomic edit operation"""
    file_path: str
    operation_type: Literal["create", "modify", "delete", "rename"]
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    line_range: Optional[tuple[int, int]] = None
    dependencies_added: List[str] = field(default_factory=list)
    dependencies_removed: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "file_path": self.file_path,
            "operation_type": self.operation_type,
            "old_content": self.old_content[:100] if self.old_content else None,
            "new_content": self.new_content[:100] if self.new_content else None,
            "line_range": self.line_range,
            "dependencies_added": self.dependencies_added,
            "dependencies_removed": self.dependencies_removed
        }

@dataclass
class EditPlan:
    """Execution plan for code modifications"""
    objective: str
    operations: List[EditOperation]
    estimated_tokens: int
    risk_level: Literal["low", "medium", "high"]
    rollback_strategy: str
    validation_steps: List[str]
    
    def get_critical_operations(self) -> List[EditOperation]:
        """Get operations that could break the build"""
        critical_types = ["delete", "rename"]
        return [op for op in self.operations if op.operation_type in critical_types]

# ============= Validation System =============

class SyntaxValidator:
    """Multi-language syntax validation"""
    
    def __init__(self):
        self.validators = {
            "python": self._validate_python,
            "py": self._validate_python,
            "javascript": self._validate_javascript,
            "js": self._validate_javascript,
            "typescript": self._validate_typescript,
            "ts": self._validate_typescript,
            "tsx": self._validate_tsx,
            "jsx": self._validate_jsx,
        }
    
    async def validate(self, file: CodeFile) -> Dict[str, Any]:
        """Validate file syntax"""
        validator = self.validators.get(file.language)
        
        if not validator:
            return {"valid": True, "skipped": True, "reason": "No validator for language"}
        
        try:
            result = await validator(file.content)
            return {"valid": result["valid"], "errors": result.get("errors", [])}
        except Exception as e:
            return {"valid": False, "errors": [str(e)]}
    
    async def _validate_python(self, content: str) -> Dict:
        """Validate Python syntax using AST"""
        try:
            ast.parse(content)
            return {"valid": True}
        except SyntaxError as e:
            return {
                "valid": False, 
                "errors": [{
                    "line": e.lineno,
                    "column": e.offset,
                    "message": e.msg
                }]
            }
    
    async def _validate_javascript(self, content: str) -> Dict:
        """Basic JavaScript validation"""
        # Simple bracket matching for now
        # In production, use proper parser like Esprima
        brackets = {"(": ")", "{": "}", "[": "]"}
        stack = []
        
        for i, char in enumerate(content):
            if char in brackets:
                stack.append((char, i))
            elif char in brackets.values():
                if not stack:
                    return {"valid": False, "errors": [f"Unmatched bracket at position {i}"]}
                opening, _ = stack.pop()
                if brackets[opening] != char:
                    return {"valid": False, "errors": [f"Mismatched bracket at position {i}"]}
        
        if stack:
            return {"valid": False, "errors": ["Unclosed brackets"]}
        
        return {"valid": True}
    
    async def _validate_typescript(self, content: str) -> Dict:
        """TypeScript validation - would use tsc in production"""
        # Basic validation + type annotation check
        js_result = await self._validate_javascript(content)
        if not js_result["valid"]:
            return js_result
        
        # Check for basic TypeScript patterns
        if "interface" in content or "type " in content or ": " in content:
            return {"valid": True, "typescript": True}
        
        return {"valid": True, "warning": "No TypeScript features detected"}
    
    async def _validate_tsx(self, content: str) -> Dict:
        """TSX validation for React components"""
        ts_result = await self._validate_typescript(content)
        if not ts_result["valid"]:
            return ts_result
        
        # Check JSX syntax
        if "<" in content and ">" in content:
            # Basic JSX validation
            jsx_pattern = r'<(\w+)[^>]*>.*?</\1>|<(\w+)[^>]*/>'
            if re.search(jsx_pattern, content):
                return {"valid": True, "jsx": True}
        
        return ts_result
    
    async def _validate_jsx(self, content: str) -> Dict:
        """JSX validation"""
        js_result = await self._validate_javascript(content)
        if not js_result["valid"]:
            return js_result
        
        # Similar to TSX but without TypeScript
        jsx_pattern = r'<(\w+)[^>]*>.*?</\1>|<(\w+)[^>]*/>'
        if re.search(jsx_pattern, content):
            return {"valid": True, "jsx": True}
        
        return {"valid": True, "warning": "No JSX elements found"}

# ============= Dependency Management =============

class DependencyManager:
    """Manage package dependencies and imports"""
    
    def __init__(self):
        self.known_packages = {
            "React": "react",
            "useState": "react",
            "useEffect": "react",
            "LineChart": "recharts",
            "BarChart": "recharts", 
            "Button": "@shadcn/ui",
            "Card": "@shadcn/ui",
            "axios": "axios",
            "lodash": "lodash",
        }
        
        self.version_map = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "recharts": "^2.5.0",
            "@shadcn/ui": "^0.8.0",
            "axios": "^1.6.0",
            "lodash": "^4.17.21",
        }
    
    def extract_imports(self, content: str) -> List[Dict]:
        """Extract all imports from file content"""
        imports = []
        
        # ES6 imports
        es6_pattern = r'import\s+(?:{[^}]+}|\*\s+as\s+\w+|\w+)\s+from\s+["\']([^"\']+)["\']'
        for match in re.finditer(es6_pattern, content):
            imports.append({
                "type": "es6",
                "module": match.group(1),
                "full_statement": match.group(0)
            })
        
        # CommonJS requires
        cjs_pattern = r'(?:const|let|var)\s+\w+\s*=\s*require\(["\']([^"\']+)["\']\)'
        for match in re.finditer(cjs_pattern, content):
            imports.append({
                "type": "commonjs",
                "module": match.group(1),
                "full_statement": match.group(0)
            })
        
        # Python imports
        py_pattern = r'^(?:from\s+(\S+)\s+)?import\s+(.+)$'
        for match in re.finditer(py_pattern, content, re.MULTILINE):
            module = match.group(1) or match.group(2).split(',')[0].strip()
            imports.append({
                "type": "python",
                "module": module,
                "full_statement": match.group(0)
            })
        
        return imports
    
    def identify_missing_dependencies(
        self, 
        imports: List[Dict], 
        package_json: Dict
    ) -> List[str]:
        """Find dependencies not in package.json"""
        current_deps = package_json.get("dependencies", {})
        current_dev_deps = package_json.get("devDependencies", {})
        all_deps = {**current_deps, **current_dev_deps}
        
        missing = []
        for imp in imports:
            module = imp["module"]
            
            # Skip relative imports
            if module.startswith('.'):
                continue
            
            # Extract package name from module path
            package = module.split('/')[0] if '/' in module else module
            
            # Remove @ scope if present
            if package.startswith('@'):
                parts = module.split('/')
                package = '/'.join(parts[:2]) if len(parts) >= 2 else parts[0]
            
            if package not in all_deps and package not in ["react", "fs", "path", "os"]:
                missing.append(package)
        
        return list(set(missing))
    
    def resolve_versions(self, packages: List[str]) -> Dict[str, str]:
        """Resolve package versions"""
        resolved = {}
        for package in packages:
            if package in self.version_map:
                resolved[package] = self.version_map[package]
            else:
                # Default to latest
                resolved[package] = "latest"
        
        return resolved

# ============= Checkpoint System =============

class CheckpointManager:
    """Manage code state checkpoints for rollback"""
    
    def __init__(self, checkpoint_dir: str = "/tmp/code_checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.active_checkpoint: Optional[str] = None
        self.checkpoint_stack: List[str] = []
    
    async def create_checkpoint(
        self, 
        files: List[CodeFile], 
        metadata: Dict = None
    ) -> str:
        """Create a new checkpoint"""
        checkpoint_id = f"cp_{int(time.time())}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        checkpoint_path.mkdir()
        
        # Save files
        files_data = {}
        for file in files:
            file_checkpoint_path = checkpoint_path / "files" / file.path.lstrip('/')
            file_checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(file_checkpoint_path, 'w') as f:
                await f.write(file.content)
            
            files_data[file.path] = {
                "checksum": file.checksum,
                "size": file.size
            }
        
        # Save metadata
        checkpoint_meta = {
            "id": checkpoint_id,
            "timestamp": time.time(),
            "files": files_data,
            "metadata": metadata or {}
        }
        
        async with aiofiles.open(checkpoint_path / "checkpoint.json", 'w') as f:
            await f.write(json.dumps(checkpoint_meta, indent=2))
        
        self.checkpoint_stack.append(checkpoint_id)
        self.active_checkpoint = checkpoint_id
        
        # Cleanup old checkpoints if > 10
        if len(self.checkpoint_stack) > 10:
            old_checkpoint = self.checkpoint_stack.pop(0)
            await self._cleanup_checkpoint(old_checkpoint)
        
        return checkpoint_id
    
    async def restore_checkpoint(self, checkpoint_id: str = None) -> List[CodeFile]:
        """Restore files from checkpoint"""
        checkpoint_id = checkpoint_id or self.active_checkpoint
        if not checkpoint_id:
            raise ValueError("No checkpoint to restore")
        
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        
        # Load metadata
        async with aiofiles.open(checkpoint_path / "checkpoint.json", 'r') as f:
            checkpoint_meta = json.loads(await f.read())
        
        # Restore files
        restored_files = []
        for file_path, file_meta in checkpoint_meta["files"].items():
            file_checkpoint_path = checkpoint_path / "files" / file_path.lstrip('/')
            
            async with aiofiles.open(file_checkpoint_path, 'r') as f:
                content = await f.read()
            
            restored_files.append(CodeFile.from_path(file_path, content))
        
        return restored_files
    
    async def _cleanup_checkpoint(self, checkpoint_id: str):
        """Remove old checkpoint"""
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        if checkpoint_path.exists():
            import shutil
            shutil.rmtree(checkpoint_path)

# ============= Main Code Editor Agent =============

class CodeEditorAgent:
    """Main autonomous code editing agent"""
    
    def __init__(self):
        self.validator = SyntaxValidator()
        self.dependency_manager = DependencyManager()
        self.checkpoint_manager = CheckpointManager()
        self.metrics = defaultdict(list)
        
    async def process_edit_request(
        self,
        feedback: str,
        files: List[Dict[str, str]],
        package_json: Dict,
        history: List[Dict] = None
    ) -> Dict[str, Any]:
        """Main entry point for code editing"""
        
        start_time = time.time()
        
        # Convert to CodeFile objects
        code_files = [
            CodeFile.from_path(f["path"], f["content"]) 
            for f in files
        ]
        
        # Create checkpoint
        checkpoint_id = await self.checkpoint_manager.create_checkpoint(
            code_files,
            {"feedback": feedback, "timestamp": time.time()}
        )
        
        try:
            # Phase 1: Analysis and Planning
            plan = await self._analyze_and_plan(feedback, code_files, history)
            
            # Phase 2: Execute modifications
            modified_files = await self._execute_plan(plan, code_files)
            
            # Phase 3: Validate changes
            validation_results = await self._validate_all(modified_files)
            
            if not all(r["valid"] for r in validation_results.values()):
                # Attempt auto-fix
                modified_files = await self._auto_fix_issues(
                    modified_files, 
                    validation_results
                )
            
            # Phase 4: Dependency resolution
            updated_package_json = await self._resolve_dependencies(
                modified_files, 
                package_json
            )
            
            # Phase 5: Final validation
            final_validation = await self._final_validation(
                modified_files, 
                updated_package_json
            )
            
            if not final_validation["success"]:
                raise ValueError(f"Final validation failed: {final_validation['errors']}")
            
            # Success - prepare response
            result = {
                "success": True,
                "plan": plan.objective,
                "files": [
                    {"path": f.path, "content": f.content} 
                    for f in modified_files
                ],
                "package_json": json.dumps(updated_package_json, indent=2),
                "checkpoint_id": checkpoint_id,
                "metrics": {
                    "execution_time": time.time() - start_time,
                    "files_modified": len(modified_files),
                    "tokens_estimated": plan.estimated_tokens,
                    "validation_score": final_validation.get("score", 1.0)
                }
            }
            
            # Record metrics
            self._record_success(result["metrics"])
            
            return result
            
        except Exception as e:
            # Rollback on failure
            restored_files = await self.checkpoint_manager.restore_checkpoint(checkpoint_id)
            
            self._record_failure(str(e))
            
            return {
                "success": False,
                "error": str(e),
                "checkpoint_id": checkpoint_id,
                "rollback": True,
                "restored_files": len(restored_files)
            }
    
    async def _analyze_and_plan(
        self, 
        feedback: str, 
        files: List[CodeFile],
        history: List[Dict] = None
    ) -> EditPlan:
        """Analyze request and create execution plan"""
        
        # Simplified planning logic
        # In production, this would use LLM for analysis
        
        operations = []
        
        # Determine operation type from feedback
        if "add" in feedback.lower() or "create" in feedback.lower():
            # Feature addition
            operations.extend(self._plan_feature_addition(feedback, files))
        elif "refactor" in feedback.lower():
            # Refactoring
            operations.extend(self._plan_refactoring(feedback, files))
        elif "fix" in feedback.lower():
            # Bug fix
            operations.extend(self._plan_bug_fix(feedback, files))
        else:
            # General modification
            operations.extend(self._plan_general_modification(feedback, files))
        
        # Estimate tokens
        estimated_tokens = len(operations) * 2000 + len(str(history or [])) * 10
        
        # Assess risk
        risk_level = "low"
        if any(op.operation_type in ["delete", "rename"] for op in operations):
            risk_level = "high"
        elif len(operations) > 10:
            risk_level = "medium"
        
        return EditPlan(
            objective=feedback,
            operations=operations,
            estimated_tokens=estimated_tokens,
            risk_level=risk_level,
            rollback_strategy="checkpoint_restore",
            validation_steps=[
                "syntax_validation",
                "import_resolution", 
                "dependency_check",
                "build_test"
            ]
        )
    
    def _plan_feature_addition(
        self, 
        feedback: str, 
        files: List[CodeFile]
    ) -> List[EditOperation]:
        """Plan feature addition operations"""
        operations = []
        
        # Example: Adding a dashboard feature
        if "dashboard" in feedback.lower():
            operations.append(
                EditOperation(
                    file_path="/src/components/Dashboard.tsx",
                    operation_type="create",
                    new_content=self._generate_dashboard_template(),
                    dependencies_added=["recharts", "@shadcn/ui"]
                )
            )
            
            # Update main app file
            app_file = next((f for f in files if "App" in f.path), None)
            if app_file:
                operations.append(
                    EditOperation(
                        file_path=app_file.path,
                        operation_type="modify",
                        old_content=app_file.content,
                        new_content=self._add_dashboard_import(app_file.content)
                    )
                )
        
        return operations
    
    def _generate_dashboard_template(self) -> str:
        """Generate dashboard component template"""
        return """import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '@shadcn/ui';

const Dashboard: React.FC = () => {
  const data = [
    { name: 'Jan', value: 400 },
    { name: 'Feb', value: 300 },
    { name: 'Mar', value: 600 },
    { name: 'Apr', value: 800 },
    { name: 'May', value: 500 }
  ];

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Analytics</CardTitle>
          </CardHeader>
          <CardContent>
            <LineChart width={400} height={300} data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#8884d8" />
            </LineChart>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <p>Total: 2,600</p>
              <p>Average: 520</p>
              <p>Peak: 800</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;"""
    
    def _add_dashboard_import(self, app_content: str) -> str:
        """Add dashboard import to app file"""
        import_line = "import Dashboard from './components/Dashboard';\n"
        
        # Add after last import
        import_end = app_content.rfind("import")
        if import_end != -1:
            next_newline = app_content.find("\n", import_end)
            return (
                app_content[:next_newline + 1] + 
                import_line + 
                app_content[next_newline + 1:]
            )
        
        return import_line + app_content
    
    def _plan_refactoring(self, feedback: str, files: List[CodeFile]) -> List[EditOperation]:
        """Plan refactoring operations"""
        # Simplified - would be more sophisticated in production
        return []
    
    def _plan_bug_fix(self, feedback: str, files: List[CodeFile]) -> List[EditOperation]:
        """Plan bug fix operations"""
        # Simplified - would analyze error patterns
        return []
    
    def _plan_general_modification(
        self, 
        feedback: str, 
        files: List[CodeFile]
    ) -> List[EditOperation]:
        """Plan general modifications"""
        # Simplified - would use LLM for planning
        return []
    
    async def _execute_plan(
        self, 
        plan: EditPlan, 
        files: List[CodeFile]
    ) -> List[CodeFile]:
        """Execute the modification plan"""
        modified_files = {f.path: f for f in files}
        
        for operation in plan.operations:
            if operation.operation_type == "create":
                # Create new file
                new_file = CodeFile.from_path(
                    operation.file_path, 
                    operation.new_content
                )
                modified_files[operation.file_path] = new_file
                
            elif operation.operation_type == "modify":
                # Modify existing file
                if operation.file_path in modified_files:
                    new_file = CodeFile.from_path(
                        operation.file_path,
                        operation.new_content
                    )
                    modified_files[operation.file_path] = new_file
                    
            elif operation.operation_type == "delete":
                # Delete file
                if operation.file_path in modified_files:
                    del modified_files[operation.file_path]
                    
            elif operation.operation_type == "rename":
                # Rename file
                if operation.file_path in modified_files:
                    old_file = modified_files[operation.file_path]
                    new_file = CodeFile.from_path(
                        operation.new_content,  # new path
                        old_file.content
                    )
                    del modified_files[operation.file_path]
                    modified_files[operation.new_content] = new_file
        
        return list(modified_files.values())
    
    async def _validate_all(
        self, 
        files: List[CodeFile]
    ) -> Dict[str, Dict]:
        """Validate all files"""
        results = {}
        
        for file in files:
            result = await self.validator.validate(file)
            results[file.path] = result
        
        return results
    
    async def _auto_fix_issues(
        self, 
        files: List[CodeFile], 
        validation_results: Dict
    ) -> List[CodeFile]:
        """Attempt to auto-fix validation issues"""
        fixed_files = []
        
        for file in files:
            if file.path in validation_results:
                result = validation_results[file.path]
                if not result["valid"] and "errors" in result:
                    # Attempt fixes based on error type
                    fixed_content = await self._apply_auto_fixes(
                        file.content, 
                        result["errors"]
                    )
                    fixed_files.append(
                        CodeFile.from_path(file.path, fixed_content)
                    )
                else:
                    fixed_files.append(file)
            else:
                fixed_files.append(file)
        
        return fixed_files
    
    async def _apply_auto_fixes(self, content: str, errors: List) -> str:
        """Apply automatic fixes for common errors"""
        # Simplified - would be more sophisticated
        
        for error in errors:
            if isinstance(error, dict):
                if "bracket" in str(error.get("message", "")).lower():
                    # Fix bracket issues
                    content = self._fix_brackets(content)
                elif "import" in str(error.get("message", "")).lower():
                    # Fix import issues  
                    content = self._fix_imports(content)
        
        return content
    
    def _fix_brackets(self, content: str) -> str:
        """Fix common bracket issues"""
        # Very simplified
        return content
    
    def _fix_imports(self, content: str) -> str:
        """Fix import issues"""
        # Very simplified
        return content
    
    async def _resolve_dependencies(
        self, 
        files: List[CodeFile], 
        package_json: Dict
    ) -> Dict:
        """Resolve and update dependencies"""
        
        all_imports = []
        for file in files:
            imports = self.dependency_manager.extract_imports(file.content)
            all_imports.extend(imports)
        
        missing = self.dependency_manager.identify_missing_dependencies(
            all_imports, 
            package_json
        )
        
        if missing:
            versions = self.dependency_manager.resolve_versions(missing)
            package_json["dependencies"] = {
                **package_json.get("dependencies", {}),
                **versions
            }
        
        return package_json
    
    async def _final_validation(
        self, 
        files: List[CodeFile], 
        package_json: Dict
    ) -> Dict:
        """Final validation before returning results"""
        
        # Check all files validate
        validation_results = await self._validate_all(files)
        all_valid = all(r["valid"] for r in validation_results.values())
        
        # Check no circular dependencies
        circular = self._check_circular_dependencies(files)
        
        # Check all components used
        unused = self._find_unused_components(files)
        
        score = 1.0
        errors = []
        
        if not all_valid:
            score -= 0.3
            errors.append("Some files have syntax errors")
        
        if circular:
            score -= 0.3
            errors.append(f"Circular dependencies detected: {circular}")
        
        if unused:
            score -= 0.2
            errors.append(f"Unused components: {unused}")
        
        return {
            "success": score >= 0.5,
            "score": score,
            "errors": errors,
            "warnings": [] if score >= 0.8 else ["Quality could be improved"]
        }
    
    def _check_circular_dependencies(self, files: List[CodeFile]) -> List[str]:
        """Check for circular import dependencies"""
        # Simplified - would build proper dependency graph
        return []
    
    def _find_unused_components(self, files: List[CodeFile]) -> List[str]:
        """Find components that are defined but never used"""
        # Simplified - would analyze usage
        return []
    
    def _record_success(self, metrics: Dict):
        """Record successful operation metrics"""
        self.metrics["successes"].append({
            "timestamp": time.time(),
            **metrics
        })
    
    def _record_failure(self, error: str):
        """Record failure metrics"""
        self.metrics["failures"].append({
            "timestamp": time.time(),
            "error": error
        })

# ============= Usage Example =============

async def main():
    """Example usage of the code editor agent"""
    
    # Initialize agent
    editor = CodeEditorAgent()
    
    # Example files
    files = [
        {
            "path": "/src/App.tsx",
            "content": """import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>My Application</h1>
    </div>
  );
}

export default App;"""
        }
    ]
    
    # Package.json
    package_json = {
        "name": "my-app",
        "version": "1.0.0",
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        }
    }
    
    # Edit request
    result = await editor.process_edit_request(
        feedback="Add a dashboard with charts and a data table",
        files=files,
        package_json=package_json
    )
    
    if result["success"]:
        print(f"✅ Edit successful!")
        print(f"Modified {len(result['files'])} files")
        print(f"Execution time: {result['metrics']['execution_time']:.2f}s")
    else:
        print(f"❌ Edit failed: {result['error']}")
        if result.get("rollback"):
            print(f"Rolled back to checkpoint: {result['checkpoint_id']}")

if __name__ == "__main__":
    asyncio.run(main())
