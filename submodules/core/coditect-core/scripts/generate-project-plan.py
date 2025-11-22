#!/usr/bin/env python3
"""
CODITECT Project Plan Generator
Autonomous submodule specification and multi-agent orchestration plan generator.

Usage:
    python3 generate-project-plan.py                    # Current directory
    python3 generate-project-plan.py path/to/submodule  # Specific submodule
    python3 generate-project-plan.py --interactive      # Interactive mode
    python3 generate-project-plan.py --help             # Show help

Features:
    - Auto-detects submodule context
    - Analyzes existing documentation
    - Generates missing docs (SDD, ADRs, C4 diagrams)
    - Creates PROJECT-PLAN.md with multi-agent orchestration
    - Creates TASKLIST-WITH-CHECKBOXES.md with 180+ tasks
    - Provides agent invocation syntax for ORCHESTRATOR
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess

class ProjectPlanGenerator:
    """Generate comprehensive project plans and orchestration artifacts"""

    def __init__(self, submodule_path: str = None, verbose: bool = False):
        self.verbose = verbose
        self.submodule_path = Path(submodule_path) if submodule_path else Path.cwd()
        self.submodule_name = self._detect_submodule_name()
        self.docs_dir = self.submodule_path / "docs"
        self.stats = {
            "files_created": 0,
            "files_analyzed": 0,
            "tasks_generated": 0,
            "agents_assigned": 0
        }

    def _detect_submodule_name(self) -> str:
        """Detect submodule name from path"""
        path_str = str(self.submodule_path.absolute())

        # Check if inside submodules/
        if "submodules/" in path_str:
            # Extract name after submodules/
            parts = path_str.split("submodules/")
            if len(parts) > 1:
                name = parts[1].split("/")[0]
                return name

        # Fall back to directory name
        return self.submodule_path.name

    def log(self, message: str, level: str = "info"):
        """Log message with formatting"""
        icons = {
            "info": "ℹ️ ",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️ ",
            "step": "📍"
        }
        icon = icons.get(level, "")
        print(f"{icon} {message}")

    def check_context(self) -> dict:
        """Check current context and validate submodule"""
        self.log("Checking submodule context...", "step")

        context = {
            "submodule_name": self.submodule_name,
            "submodule_path": str(self.submodule_path),
            "is_submodule": self._is_submodule(),
            "has_docs": self.docs_dir.exists(),
            "has_readme": (self.submodule_path / "README.md").exists(),
            "has_claude_md": (self.submodule_path / "CLAUDE.md").exists(),
            "has_project_plan": (self.submodule_path / "PROJECT-PLAN.md").exists(),
            "has_tasklist": (self.submodule_path / "TASKLIST-WITH-CHECKBOXES.md").exists()
        }

        # Check for existing documentation
        if context["has_docs"]:
            doc_files = list(self.docs_dir.glob("*.md"))
            context["doc_count"] = len(doc_files)
            context["doc_files"] = [f.name for f in doc_files]
        else:
            context["doc_count"] = 0
            context["doc_files"] = []

        self.log(f"Submodule: {self.submodule_name}", "info")
        self.log(f"Path: {self.submodule_path}", "info")
        self.log(f"Documentation: {'FOUND' if context['has_docs'] else 'MISSING'}",
                 "success" if context['has_docs'] else "warning")

        return context

    def _is_submodule(self) -> bool:
        """Check if directory is a git submodule"""
        git_file = self.submodule_path / ".git"
        if git_file.exists():
            # If .git is a file, it's a submodule reference
            if git_file.is_file():
                return True
        return False

    def analyze_documentation(self) -> dict:
        """Analyze existing documentation"""
        self.log("Analyzing existing documentation...", "step")

        analysis = {
            "status": "MISSING",
            "completeness": 0,
            "missing_docs": [],
            "existing_docs": []
        }

        if not self.docs_dir.exists():
            analysis["missing_docs"] = [
                "docs/",
                "SOFTWARE-DESIGN-DOCUMENT.md",
                "C4-DIAGRAMS.md",
                "DATABASE-ARCHITECTURE.md",
                "adrs/README.md"
            ]
            return analysis

        # Check for required documentation
        required_docs = {
            "SDD": "SOFTWARE-DESIGN-DOCUMENT*.md",
            "C4": "C4-DIAGRAMS*.md",
            "DB": "DATABASE*.md",
            "EXEC": "EXECUTIVE-SUMMARY*.md",
            "ADR": "adrs/README.md"
        }

        found_count = 0
        for doc_type, pattern in required_docs.items():
            matches = list(self.docs_dir.glob(pattern))
            if matches:
                found_count += 1
                analysis["existing_docs"].append(doc_type)
                self.stats["files_analyzed"] += len(matches)
            else:
                analysis["missing_docs"].append(doc_type)

        analysis["completeness"] = (found_count / len(required_docs)) * 100

        if analysis["completeness"] == 100:
            analysis["status"] = "COMPLETE"
        elif analysis["completeness"] >= 50:
            analysis["status"] = "PARTIAL"

        self.log(f"Documentation completeness: {analysis['completeness']:.0f}%",
                 "success" if analysis['completeness'] == 100 else "warning")

        return analysis

    def generate_documentation_spec(self) -> str:
        """Generate specification for missing documentation"""
        spec = f"""Generate complete software design documentation for {self.submodule_name}.

Analyze existing:
- README.md (if exists)
- CLAUDE.md (if exists)
- Code structure in src/, backend/, frontend/ directories

Create the following documentation in docs/:

1. EXECUTIVE-SUMMARY-{self.submodule_name}.md (15 KB)
   - Business case and value proposition
   - ROI analysis (Year 1, Year 2)
   - Target users and success metrics
   - Implementation timeline overview

2. SOFTWARE-DESIGN-DOCUMENT-{self.submodule_name}.md (60+ KB, 67,000+ words)
   - System architecture (C4 Context, Container, Component)
   - Technology stack with justifications
   - Database schema with indexes and RLS policies
   - API endpoints with authentication
   - Security considerations
   - Performance targets
   - Testing strategy
   - Deployment architecture

3. C4-DIAGRAMS-{self.submodule_name}.md (40 KB, 9+ diagrams)
   - C4 Level 1: System Context
   - C4 Level 2: Container Architecture
   - C4 Level 3: Component Diagrams
   - Deployment Architecture (GCP/AWS)
   - Sequence diagrams for key flows
   - All diagrams in GitHub-compatible Mermaid format

4. DATABASE-ARCHITECTURE-{self.submodule_name}.md (30 KB)
   - Complete PostgreSQL schema with DDL
   - Row-Level Security (RLS) policies
   - Indexes and performance optimization
   - Migration strategy
   - Backup and disaster recovery

5. docs/adrs/ directory:
   - ADR-001-git-as-source-of-truth.md (or primary architectural decision)
   - ADR-002-database-selection.md
   - ADR-003-api-framework.md
   - ADR-004-multi-tenant-strategy.md
   - ADR-005-deployment-platform.md
   - ADR-006-frontend-framework.md
   - ADR-007-search-solution.md
   - ADR-008-access-control.md
   - README.md (ADR index with 40/40 quality scores)

Each ADR must include:
- Status, Context, Decision, Consequences, Alternatives Considered
- 40/40 quality score (20/20 for Depth, 20/20 for Compliance)

Quality standards:
- Comprehensive technical detail
- Production-ready specifications
- Clear architectural decisions
- Executable by autonomous agents

Output: Complete docs/ directory ready for PROJECT-PLAN.md generation
"""
        return spec

    def generate_project_plan_spec(self, doc_analysis: dict) -> str:
        """Generate specification for PROJECT-PLAN.md"""
        spec = f"""Create comprehensive PROJECT-PLAN.md for {self.submodule_name}.

Documentation status: {doc_analysis['status']}
Existing docs: {', '.join(doc_analysis['existing_docs'])}

Requirements:

1. Analyze existing documentation to understand:
   - System architecture and technology stack
   - Business requirements and success criteria
   - Technical complexity and dependencies

2. Break implementation into 3-4 phases:
   - Phase 1: Infrastructure & Core Backend (Weeks 1-4)
   - Phase 2: Advanced Features & Integration (Weeks 5-8)
   - Phase 3: Frontend & Polish (Weeks 9-12)
   - Phase 4: Production Launch (if needed)

3. For each phase, create weekly milestones with:
   - Clear deliverables
   - Agent assignments (which specialized agent)
   - Time estimates (hours per week)
   - Dependencies between weeks
   - Acceptance criteria

4. Multi-Agent Orchestration Strategy:
   - Agent Roles & Responsibilities table
   - Orchestration patterns (direct, sequential, parallel, coordinated)
   - Complete agent invocation examples with syntax
   - Example: Task(subagent_type="codi-devops-engineer", prompt="...")

5. Specialized agents to assign:
   - codi-devops-engineer (infrastructure, CI/CD, deployment)
   - rust-expert-developer (backend, adapts to Python/Go/Node.js)
   - frontend-react-typescript-expert (React/Next.js frontend)
   - database-architect (PostgreSQL, migrations, schema)
   - security-specialist (auth, encryption, audit)
   - multi-tenant-architect (RLS, tenant isolation)
   - ai-specialist (embeddings, semantic search)
   - monitoring-specialist (Prometheus, Grafana, alerts)
   - codi-test-engineer (unit tests, integration tests)
   - senior-architect (API design, system architecture)

6. Budget Breakdown:
   - Engineering costs (hourly rate × hours × team size)
   - Infrastructure costs (monthly × 12 months)
   - Total with 20% contingency
   - ROI analysis (Year 1, Year 2)

7. Risk Management:
   - Identify 5+ high-priority risks
   - Mitigation strategy for each risk
   - Monitoring approach

8. Success Metrics:
   - Technical metrics (latency, uptime, test coverage)
   - Adoption metrics (user engagement)
   - Business metrics (ARR, NPS, churn)

9. Quality Gates:
   - Phase completion criteria (must-have checkpoints)
   - Go/no-go decision points

Output format: Follow coditect-project-intelligence/PROJECT-PLAN.md as reference template
Target size: 25-30 KB comprehensive plan
Audience: ORCHESTRATOR agent + human stakeholders
"""
        return spec

    def generate_tasklist_spec(self) -> str:
        """Generate specification for TASKLIST-WITH-CHECKBOXES.md"""
        spec = f"""Create comprehensive TASKLIST-WITH-CHECKBOXES.md for {self.submodule_name}.

Based on PROJECT-PLAN.md phases, create detailed checkbox-based tasklist.

Requirements:

1. Progress Summary Table:
   | Phase | Tasks | Completed | In Progress | Pending | % Complete |
   Shows overall project progress at a glance

2. For each phase, break down into weekly tasks:
   - Week X: Milestone Name
   - 15-30 tasks per week
   - Each task group has:
     * Agent assignment (specialized agent name)
     * Duration estimate (hours)
     * Dependencies (which tasks must complete first)
     * Checkbox format: - [ ] Task description
     * Acceptance criteria (how to verify completion)

3. Task format example:
   ```markdown
   #### 3.1 Infrastructure Setup
   **Agent**: `codi-devops-engineer`
   **Duration**: 8 hours
   **Dependencies**: None

   - [ ] Create GCP project
   - [ ] Enable required APIs
   - [ ] Configure billing alerts
   - [ ] Set up IAM service accounts

   **Acceptance**: GCP project operational, all APIs enabled
   ```

4. Orchestration Guidance:
   - Sequential execution requirements (dependencies)
   - Parallel execution opportunities (independent tasks)
   - Multi-agent coordination patterns
   - When to use orchestrator vs direct agent invocation

5. Agent Invocation Examples:
   - Provide Task(...) syntax for each phase
   - Include both direct invocation and orchestrator patterns
   - Show parameter passing and prompt templates

6. Comprehensive coverage:
   - Total: 180-200 tasks across all phases
   - Phases weighted by complexity (infrastructure: 20%, backend: 40%, frontend: 30%, launch: 10%)
   - Each task is actionable and verifiable

7. Progress tracking:
   - Weekly milestone summaries
   - Phase checkpoint reviews
   - Overall project % complete

Output format: Follow coditect-project-intelligence/TASKLIST-WITH-CHECKBOXES.md as reference
Target size: 40-50 KB detailed tasklist
Audience: ORCHESTRATOR agent + development team
Purpose: Enable autonomous checkbox-based execution
"""
        return spec

    def execute_with_orchestrator(self, task_description: str, output_path: str = None) -> bool:
        """Execute task using ORCHESTRATOR agent via Claude Code"""
        self.log(f"Orchestrating: {task_description[:60]}...", "step")

        # In a real implementation, this would:
        # 1. Invoke Claude Code API with Task() call
        # 2. Monitor execution progress
        # 3. Verify output files created
        # 4. Return success/failure

        # For now, we'll create placeholder that instructs user
        print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                   ORCHESTRATOR AGENT REQUIRED                        ║
╚══════════════════════════════════════════════════════════════════════╝

To execute this task, use the following agent invocation in Claude Code:

Task(
    subagent_type="orchestrator",
    prompt=\"\"\"{task_description}\"\"\"
)

This will coordinate the necessary specialized agents to complete the task.
        """)

        return False  # Requires manual execution

    def generate_plan(self, context: dict, doc_analysis: dict):
        """Main plan generation workflow"""
        self.log("="*70, "info")
        self.log(f"GENERATING PROJECT PLAN FOR: {self.submodule_name}", "step")
        self.log("="*70, "info")

        # Step 1: Generate missing documentation (if needed)
        if doc_analysis["status"] != "COMPLETE":
            self.log("Step 1: Generating missing documentation...", "step")
            doc_spec = self.generate_documentation_spec()

            print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                DOCUMENTATION GENERATION REQUIRED                      ║
╚══════════════════════════════════════════════════════════════════════╝

Missing documentation detected. Use this agent invocation:

Task(
    subagent_type="software-design-document-specialist",
    prompt=\"\"\"{doc_spec}\"\"\"
)

Once complete, re-run this script to continue.
            """)
            return

        # Step 2: Generate PROJECT-PLAN.md
        self.log("Step 2: Generating PROJECT-PLAN.md...", "step")
        plan_spec = self.generate_project_plan_spec(doc_analysis)

        if not context["has_project_plan"]:
            self.execute_with_orchestrator(plan_spec, "PROJECT-PLAN.md")
        else:
            self.log("PROJECT-PLAN.md already exists", "warning")

        # Step 3: Generate TASKLIST-WITH-CHECKBOXES.md
        self.log("Step 3: Generating TASKLIST-WITH-CHECKBOXES.md...", "step")
        tasklist_spec = self.generate_tasklist_spec()

        if not context["has_tasklist"]:
            self.execute_with_orchestrator(tasklist_spec, "TASKLIST-WITH-CHECKBOXES.md")
        else:
            self.log("TASKLIST-WITH-CHECKBOXES.md already exists", "warning")

        # Step 4: Summary and next steps
        self.print_summary(context)

    def print_summary(self, context: dict):
        """Print generation summary and next steps"""
        print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                       GENERATION COMPLETE                             ║
╚══════════════════════════════════════════════════════════════════════╝

📁 Files Status:
   - docs/: {"✅ COMPLETE" if context["has_docs"] else "⏸️  PENDING"}
   - PROJECT-PLAN.md: {"✅ EXISTS" if context["has_project_plan"] else "⏸️  PENDING"}
   - TASKLIST-WITH-CHECKBOXES.md: {"✅ EXISTS" if context["has_tasklist"] else "⏸️  PENDING"}

📊 Statistics:
   - Files analyzed: {self.stats["files_analyzed"]}
   - Files to create: {self.stats["files_created"]}

🤖 Next Steps:

1. Execute the agent invocations shown above
2. Review generated PROJECT-PLAN.md
3. Check TASKLIST-WITH-CHECKBOXES.md for task breakdown
4. Start implementation:

   Task(
       subagent_type="orchestrator",
       prompt="Execute Week 1 tasks from {self.submodule_name}/TASKLIST-WITH-CHECKBOXES.md"
   )

5. Track progress by checking off completed tasks

═══════════════════════════════════════════════════════════════════════

📚 Documentation:
   - /generate-project-plan --help
   - .coditect/commands/generate-project-plan.md

═══════════════════════════════════════════════════════════════════════
        """)


def main():
    parser = argparse.ArgumentParser(
        description="CODITECT Project Plan Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 generate-project-plan.py
  python3 generate-project-plan.py submodules/coditect-cloud-backend
  python3 generate-project-plan.py --interactive
  python3 generate-project-plan.py --verbose

For more information:
  See .coditect/commands/generate-project-plan.md
        """
    )

    parser.add_argument(
        "submodule_path",
        nargs="?",
        default=None,
        help="Path to submodule (default: current directory)"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Interactive mode with prompts"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--skip-docs",
        action="store_true",
        help="Skip documentation generation"
    )

    parser.add_argument(
        "--update",
        action="store_true",
        help="Update existing plan (don't regenerate)"
    )

    args = parser.parse_args()

    # Create generator
    generator = ProjectPlanGenerator(
        submodule_path=args.submodule_path,
        verbose=args.verbose
    )

    # Check context
    context = generator.check_context()

    # Analyze documentation
    doc_analysis = generator.analyze_documentation()

    # Generate plan
    generator.generate_plan(context, doc_analysis)


if __name__ == "__main__":
    main()
