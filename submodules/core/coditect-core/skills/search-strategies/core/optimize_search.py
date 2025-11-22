#!/usr/bin/env python3
"""
Search Strategy Optimizer

Recommends optimal search strategy based on search goal and context.
"""

from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass


class SearchTool(Enum):
    """Available search tools"""
    READ = "Read"
    GLOB = "Glob"
    GREP = "Grep"
    CODEBASE_LOCATOR = "codebase-locator"
    CODEBASE_PATTERN_FINDER = "codebase-pattern-finder"
    CODEBASE_ANALYZER = "codebase-analyzer"


class SearchComplexity(Enum):
    """Search complexity levels"""
    SIMPLE = "simple"  # Single tool, one call
    MODERATE = "moderate"  # 2-3 tool calls
    COMPLEX = "complex"  # Multiple stages or agent needed


@dataclass
class SearchStrategy:
    """Recommended search strategy"""
    complexity: SearchComplexity
    steps: List[dict]
    estimated_tokens: Tuple[int, int]  # (min, max)
    rationale: str


class SearchOptimizer:
    """Optimize search strategies for codebase exploration"""

    # Token cost estimates
    TOKEN_COSTS = {
        SearchTool.READ: (1000, 3000),
        SearchTool.GLOB: (500, 1000),
        SearchTool.GREP: (1000, 5000),
        SearchTool.CODEBASE_LOCATOR: (8000, 12000),
        SearchTool.CODEBASE_PATTERN_FINDER: (10000, 15000),
        SearchTool.CODEBASE_ANALYZER: (12000, 20000),
    }

    def recommend_strategy(self, search_goal: str) -> SearchStrategy:
        """
        Recommend optimal search strategy based on goal.

        Args:
            search_goal: Natural language description of what to find

        Returns:
            SearchStrategy with recommended steps
        """
        goal_lower = search_goal.lower()

        # Pattern 1: Exact file path known
        if "read" in goal_lower or "file:" in goal_lower:
            return self._strategy_exact_file()

        # Pattern 2: Filename pattern
        if any(word in goal_lower for word in ["find files", "all files", "*.ts", "*.rs"]):
            return self._strategy_filename_pattern(search_goal)

        # Pattern 3: Content search for specific term
        if any(word in goal_lower for word in ["find function", "find class", "find string"]):
            return self._strategy_content_search(search_goal)

        # Pattern 4: Understanding/analysis needed
        if any(word in goal_lower for word in ["how does", "understand", "analyze", "explain"]):
            return self._strategy_analysis(search_goal)

        # Pattern 5: Find patterns across files
        if any(word in goal_lower for word in ["pattern", "similar", "all instances"]):
            return self._strategy_pattern_search(search_goal)

        # Pattern 6: Open-ended search
        if any(word in goal_lower for word in ["find all", "locate", "where is"]):
            return self._strategy_open_ended(search_goal)

        # Default: Conservative open-ended search
        return self._strategy_open_ended(search_goal)

    def _strategy_exact_file(self) -> SearchStrategy:
        """Strategy when exact file path is known"""
        return SearchStrategy(
            complexity=SearchComplexity.SIMPLE,
            steps=[
                {
                    "step": 1,
                    "tool": SearchTool.READ.value,
                    "action": "Read the file directly",
                    "example": "Read('backend/src/main.rs')"
                }
            ],
            estimated_tokens=(1000, 3000),
            rationale="Exact file path known - use Read tool directly for fastest result"
        )

    def _strategy_filename_pattern(self, search_goal: str) -> SearchStrategy:
        """Strategy for filename pattern matching"""
        # Try to extract pattern from goal
        pattern = "**/*.{ts,rs}"  # Default pattern

        if "*.ts" in search_goal or "typescript" in search_goal.lower():
            pattern = "**/*.ts"
        elif "*.rs" in search_goal or "rust" in search_goal.lower():
            pattern = "**/*.rs"
        elif "test" in search_goal.lower():
            pattern = "**/*test*.{ts,rs}"

        return SearchStrategy(
            complexity=SearchComplexity.SIMPLE,
            steps=[
                {
                    "step": 1,
                    "tool": SearchTool.GLOB.value,
                    "action": f"Use Glob with pattern: {pattern}",
                    "example": f"Glob('{pattern}')"
                }
            ],
            estimated_tokens=(500, 1000),
            rationale="Searching by filename pattern - Glob is fastest and most efficient"
        )

    def _strategy_content_search(self, search_goal: str) -> SearchStrategy:
        """Strategy for searching file contents"""
        # Extract search term (simplified)
        search_term = "search_term"

        # Determine if should use type filter
        file_type = None
        if "typescript" in search_goal.lower() or ".ts" in search_goal:
            file_type = "ts"
        elif "rust" in search_goal.lower() or ".rs" in search_goal:
            file_type = "rust"

        steps = [
            {
                "step": 1,
                "tool": SearchTool.GREP.value,
                "action": f"Search for content: '{search_term}'",
                "example": f"Grep('{search_term}', type='{file_type}')" if file_type else f"Grep('{search_term}')",
                "output": "files_with_matches"
            },
            {
                "step": 2,
                "tool": SearchTool.GREP.value,
                "action": "Get context around matches",
                "example": f"Grep('{search_term}', output_mode='content', C=5)",
                "optional": True
            },
            {
                "step": 3,
                "tool": SearchTool.READ.value,
                "action": "Read specific files for full context",
                "example": "Read('<file_from_step_1>')",
                "optional": True
            }
        ]

        return SearchStrategy(
            complexity=SearchComplexity.MODERATE,
            steps=steps,
            estimated_tokens=(2000, 8000),
            rationale="Content search - use Grep for initial match, optionally expand with context or Read"
        )

    def _strategy_analysis(self, search_goal: str) -> SearchStrategy:
        """Strategy when understanding/analysis is needed"""
        return SearchStrategy(
            complexity=SearchComplexity.COMPLEX,
            steps=[
                {
                    "step": 1,
                    "tool": SearchTool.CODEBASE_LOCATOR.value,
                    "action": "Locate relevant files",
                    "example": "Task(subagent_type='codebase-locator', prompt='Find auth files')"
                },
                {
                    "step": 2,
                    "tool": SearchTool.CODEBASE_ANALYZER.value,
                    "action": "Analyze how code works",
                    "example": "Task(subagent_type='codebase-analyzer', prompt='Analyze auth flow')"
                }
            ],
            estimated_tokens=(20000, 32000),
            rationale="Understanding needed - use codebase-analyzer for comprehensive analysis"
        )

    def _strategy_pattern_search(self, search_goal: str) -> SearchStrategy:
        """Strategy for finding patterns across files"""
        return SearchStrategy(
            complexity=SearchComplexity.COMPLEX,
            steps=[
                {
                    "step": 1,
                    "tool": SearchTool.CODEBASE_PATTERN_FINDER.value,
                    "action": "Find patterns across codebase",
                    "example": "Task(subagent_type='codebase-pattern-finder', prompt='Find CRUD patterns')"
                }
            ],
            estimated_tokens=(10000, 15000),
            rationale="Pattern search - use codebase-pattern-finder to extract and compare patterns"
        )

    def _strategy_open_ended(self, search_goal: str) -> SearchStrategy:
        """Strategy for open-ended searches"""
        return SearchStrategy(
            complexity=SearchComplexity.COMPLEX,
            steps=[
                {
                    "step": 1,
                    "tool": SearchTool.CODEBASE_LOCATOR.value,
                    "action": "Locate relevant files and code",
                    "example": "Task(subagent_type='codebase-locator', prompt='{search_goal}')"
                }
            ],
            estimated_tokens=(8000, 12000),
            rationale="Open-ended search - use codebase-locator agent to iterate and refine results"
        )

    def compare_strategies(
        self,
        manual_approach: List[str],
        optimized_approach: SearchStrategy
    ) -> dict:
        """
        Compare manual approach vs optimized strategy.

        Args:
            manual_approach: List of tool calls in manual approach
            optimized_approach: Recommended SearchStrategy

        Returns:
            Comparison with token savings
        """
        # Estimate manual approach tokens
        manual_tokens = 0
        for tool_call in manual_approach:
            # Simple heuristic: each tool call costs average of its range
            if "Grep" in tool_call:
                manual_tokens += sum(self.TOKEN_COSTS[SearchTool.GREP]) // 2
            elif "Glob" in tool_call:
                manual_tokens += sum(self.TOKEN_COSTS[SearchTool.GLOB]) // 2
            elif "Read" in tool_call:
                manual_tokens += sum(self.TOKEN_COSTS[SearchTool.READ]) // 2

        optimized_min, optimized_max = optimized_approach.estimated_tokens
        optimized_avg = (optimized_min + optimized_max) // 2

        return {
            "manual_tokens": manual_tokens,
            "optimized_tokens": optimized_avg,
            "savings": manual_tokens - optimized_avg,
            "savings_percent": ((manual_tokens - optimized_avg) / manual_tokens * 100) if manual_tokens > 0 else 0,
            "recommendation": "Use optimized approach" if optimized_avg < manual_tokens else "Manual approach acceptable"
        }


def print_strategy(strategy: SearchStrategy):
    """Pretty print a search strategy"""
    print(f"Complexity: {strategy.complexity.value}")
    print(f"Estimated Tokens: {strategy.estimated_tokens[0]:,} - {strategy.estimated_tokens[1]:,}")
    print(f"Rationale: {strategy.rationale}\n")
    print("Steps:")
    for i, step in enumerate(strategy.steps, 1):
        optional = " (optional)" if step.get("optional") else ""
        print(f"  {i}. {step['action']}{optional}")
        print(f"     Tool: {step['tool']}")
        print(f"     Example: {step['example']}")
        if "output" in step:
            print(f"     Output: {step['output']}")
        print()


def main():
    """Example usage"""
    optimizer = SearchOptimizer()

    test_goals = [
        "Read backend/src/main.rs",
        "Find all TypeScript test files",
        "Find the login_handler function",
        "How does authentication work in the backend?",
        "Find all CRUD patterns in handlers",
        "Locate all session management code"
    ]

    print("=== Search Strategy Optimizer ===\n")

    for goal in test_goals:
        print(f"Goal: {goal}")
        print("-" * 60)

        strategy = optimizer.recommend_strategy(goal)
        print_strategy(strategy)

    # Example comparison
    print("\n=== Manual vs Optimized Comparison ===\n")
    print("Goal: Find all authentication files\n")

    manual = [
        "Grep('auth')",  # Too broad
        "Grep('authentication')",  # Still broad
        "Grep('fn login')",  # Getting specific
        "Read('backend/src/handlers/auth.rs')",
        "Read('backend/src/middleware/auth.rs')",
    ]

    optimized = optimizer.recommend_strategy("Find all authentication files")

    print("Manual Approach:")
    for i, step in enumerate(manual, 1):
        print(f"  {i}. {step}")

    print(f"\nOptimized Approach:")
    print_strategy(optimized)

    comparison = optimizer.compare_strategies(manual, optimized)
    print("Comparison:")
    print(f"  Manual tokens: {comparison['manual_tokens']:,}")
    print(f"  Optimized tokens: {comparison['optimized_tokens']:,}")
    print(f"  Savings: {comparison['savings']:,} tokens ({comparison['savings_percent']:.1f}%)")
    print(f"  Recommendation: {comparison['recommendation']}")


if __name__ == "__main__":
    main()
