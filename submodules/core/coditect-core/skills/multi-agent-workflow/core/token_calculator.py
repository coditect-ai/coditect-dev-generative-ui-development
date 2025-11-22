#!/usr/bin/env python3
"""
Token Calculator for Multi-Agent Workflows

Estimates token usage for various operations to prevent context collapse.
Based on Claude Sonnet 4.5 limits (160K tokens).
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class TokenEstimate:
    """Token usage estimate for an operation"""
    operation: str
    tokens: int
    confidence: str  # "low", "medium", "high"


class TokenCalculator:
    """Calculate and track token usage across workflow phases"""

    # Claude Sonnet 4.5 limits
    MAX_TOKENS = 160_000
    SAFE_THRESHOLD = int(MAX_TOKENS * 0.70)  # 112K
    WARNING_THRESHOLD = int(MAX_TOKENS * 0.85)  # 136K
    CRITICAL_THRESHOLD = int(MAX_TOKENS * 0.95)  # 152K

    # Estimation constants (based on empirical observations)
    TOKENS_PER_LINE = 20
    TOKENS_PER_FILE_SMALL = 2_000  # < 500 lines
    TOKENS_PER_FILE_MEDIUM = 5_000  # 500-2000 lines
    TOKENS_PER_FILE_LARGE = 10_000  # > 2000 lines

    TOKENS_PER_SUBAGENT = {
        "codebase-locator": 8_000,
        "codebase-analyzer": 12_000,
        "codebase-pattern-finder": 10_000,
        "thoughts-analyzer": 8_000,
        "thoughts-locator": 6_000,
        "web-search-researcher": 15_000,  # Includes web results
        "project-organizer": 7_000,
    }

    TOKENS_PER_PHASE_TYPE = {
        "research": (20_000, 40_000),  # min, max
        "design": (10_000, 20_000),
        "implementation": (25_000, 50_000),
        "testing": (15_000, 25_000),
        "documentation": (8_000, 15_000),
    }

    def __init__(self):
        self.current_usage = 0
        self.phase_usage = {}

    def estimate_file_read(self, lines: int) -> TokenEstimate:
        """Estimate tokens for reading a file"""
        if lines < 500:
            tokens = self.TOKENS_PER_FILE_SMALL
            confidence = "high"
        elif lines < 2000:
            tokens = self.TOKENS_PER_FILE_MEDIUM
            confidence = "high"
        else:
            tokens = self.TOKENS_PER_FILE_LARGE
            confidence = "medium"

        return TokenEstimate(
            operation=f"Read file ({lines} lines)",
            tokens=tokens,
            confidence=confidence
        )

    def estimate_subagent_call(self, agent_type: str) -> TokenEstimate:
        """Estimate tokens for invoking a subagent"""
        tokens = self.TOKENS_PER_SUBAGENT.get(agent_type, 10_000)
        return TokenEstimate(
            operation=f"Invoke {agent_type}",
            tokens=tokens,
            confidence="high"
        )

    def estimate_phase(self, phase_type: str) -> Tuple[int, int]:
        """Estimate token range for a phase type"""
        return self.TOKENS_PER_PHASE_TYPE.get(phase_type, (10_000, 30_000))

    def add_usage(self, operation: str, tokens: int):
        """Record token usage"""
        self.current_usage += tokens
        phase = operation.split(":")[0]  # Extract phase name
        if phase not in self.phase_usage:
            self.phase_usage[phase] = 0
        self.phase_usage[phase] += tokens

    def get_status(self) -> str:
        """Get current token budget status"""
        if self.current_usage < self.SAFE_THRESHOLD:
            return "Safe Zone"
        elif self.current_usage < self.WARNING_THRESHOLD:
            return "Warning Zone"
        elif self.current_usage < self.CRITICAL_THRESHOLD:
            return "Critical Zone"
        else:
            return "Over-budget"

    def get_remaining_budget(self) -> int:
        """Get remaining token budget"""
        return self.MAX_TOKENS - self.current_usage

    def get_usage_percentage(self) -> float:
        """Get usage as percentage of max tokens"""
        return (self.current_usage / self.MAX_TOKENS) * 100

    def should_checkpoint(self) -> bool:
        """Determine if a checkpoint is needed"""
        return self.current_usage >= self.WARNING_THRESHOLD

    def recommend_compression_level(self) -> int:
        """Recommend compression level (1-3)"""
        percentage = self.get_usage_percentage()
        if percentage < 70:
            return 0  # No compression needed
        elif percentage < 85:
            return 1  # Light compression
        elif percentage < 95:
            return 2  # Moderate compression
        else:
            return 3  # Heavy compression

    def estimate_workflow(self, phases: List[str], file_counts: Dict[str, int]) -> Dict:
        """Estimate total token usage for a multi-phase workflow"""
        estimates = []
        total_min = 0
        total_max = 0

        for phase in phases:
            min_tokens, max_tokens = self.estimate_phase(phase)
            estimates.append({
                "phase": phase,
                "min_tokens": min_tokens,
                "max_tokens": max_tokens,
                "avg_tokens": (min_tokens + max_tokens) // 2
            })
            total_min += min_tokens
            total_max += max_tokens

        return {
            "estimates": estimates,
            "total_min": total_min,
            "total_max": total_max,
            "total_avg": (total_min + total_max) // 2,
            "status": self._predict_status((total_min + total_max) // 2),
            "recommendation": self._get_recommendation((total_min + total_max) // 2)
        }

    def _predict_status(self, projected_tokens: int) -> str:
        """Predict status for projected token usage"""
        if projected_tokens < self.SAFE_THRESHOLD:
            return "Safe Zone"
        elif projected_tokens < self.WARNING_THRESHOLD:
            return "Warning Zone"
        elif projected_tokens < self.CRITICAL_THRESHOLD:
            return "Critical Zone"
        else:
            return "Over-budget"

    def _get_recommendation(self, projected_tokens: int) -> str:
        """Get recommendation based on projected usage"""
        if projected_tokens < self.SAFE_THRESHOLD:
            return "Proceed normally - sufficient budget"
        elif projected_tokens < self.WARNING_THRESHOLD:
            return "Apply Level 1 compression mid-workflow"
        elif projected_tokens < self.CRITICAL_THRESHOLD:
            return "Apply Level 2 compression + mandatory checkpoint"
        else:
            return "Split into 2 sessions with context_save between"


def main():
    """Example usage"""
    calc = TokenCalculator()

    # Example: Estimate a full-stack feature workflow
    phases = ["research", "design", "implementation", "testing", "documentation"]
    file_counts = {"backend": 5, "frontend": 8, "tests": 10}

    result = calc.estimate_workflow(phases, file_counts)

    print("=== Workflow Token Estimate ===")
    print(f"Total Range: {result['total_min']:,} - {result['total_max']:,} tokens")
    print(f"Average: {result['total_avg']:,} tokens")
    print(f"Status: {result['status']}")
    print(f"Recommendation: {result['recommendation']}")
    print()
    print("Per-Phase Breakdown:")
    for estimate in result['estimates']:
        print(f"  {estimate['phase']}: {estimate['avg_tokens']:,} tokens (avg)")


if __name__ == "__main__":
    main()
