#!/usr/bin/env python3
"""
Universal Format Template Validator - Quick validation system
Validates universal agent format compliance in under 8K tokens.
"""

import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Template validation result"""
    valid: bool
    score: int  # 0-100
    errors: List[str]
    warnings: List[str]
    recommendations: List[str]

class TemplateValidator:
    """Quick universal format template validator"""
    
    def __init__(self):
        self.required_fields = [
            'name', 'description', 'platform_compatibility',
            'invocation_pattern', 'skills', 'automation_features'
        ]
        
        self.platform_targets = ['claude', 'gpt', 'gemini', 'enterprise']
    
    def validate_template(self, template_data: Dict) -> ValidationResult:
        """Validate universal format template"""
        errors = []
        warnings = []
        recommendations = []
        score = 100
        
        # Check required fields
        for field in self.required_fields:
            if field not in template_data:
                errors.append(f"Missing required field: {field}")
                score -= 20
        
        # Validate platform compatibility
        if 'platform_compatibility' in template_data:
            platforms = template_data['platform_compatibility']
            if not isinstance(platforms, list) or len(platforms) < 2:
                warnings.append("Should support 2+ platforms for universal compatibility")
                score -= 10
        
        # Check automation features
        if 'automation_features' in template_data:
            auto_features = template_data['automation_features']
            if not auto_features.get('context_awareness'):
                recommendations.append("Add context awareness for better performance")
                score -= 5
        
        # Validate invocation pattern
        if 'invocation_pattern' in template_data:
            pattern = template_data['invocation_pattern']
            if 'Task(' not in str(pattern):
                errors.append("Invocation pattern must use Task tool proxy format")
                score -= 15
        
        return ValidationResult(
            valid=len(errors) == 0,
            score=max(0, score),
            errors=errors,
            warnings=warnings,
            recommendations=recommendations
        )
    
    def generate_template_from_47agent(self, agent_path: str) -> Dict:
        """Generate universal template from 47-agent format"""
        return {
            "name": "generated_agent",
            "description": "Converted from 47-agent framework",
            "platform_compatibility": self.platform_targets,
            "invocation_pattern": "Task(subagent_type='general-purpose', prompt='Use {name} subagent to {task}')",
            "skills": ["multi-agent-workflow", "production-patterns"],
            "automation_features": {
                "context_awareness": True,
                "auto_scope_detection": True,
                "progress_tracking": True
            }
        }

# Quick validation function
def validate_agent_template(template: Dict) -> ValidationResult:
    """Quick template validation"""
    validator = TemplateValidator()
    return validator.validate_template(template)

if __name__ == "__main__":
    # Test validation
    test_template = {
        "name": "test-agent",
        "description": "Test universal agent",
        "platform_compatibility": ["claude", "gpt"],
        "invocation_pattern": "Task(subagent_type='general-purpose', prompt='Use test-agent subagent to...')",
        "skills": ["production-patterns"],
        "automation_features": {"context_awareness": True}
    }
    
    result = validate_agent_template(test_template)
    print(f"Valid: {result.valid}, Score: {result.score}")
    if result.errors:
        print(f"Errors: {result.errors}")