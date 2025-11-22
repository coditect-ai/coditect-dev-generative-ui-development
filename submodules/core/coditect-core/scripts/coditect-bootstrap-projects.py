#!/usr/bin/env python3

"""
AZ1.AI CODITECT Project Bootstrap Script

Copyright © 2025 AZ1.AI INC. All Rights Reserved.
Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.

Purpose: Automated setup of all CODITECT rollout projects
- Creates project directories
- Initializes Git repositories
- Creates GitHub repositories
- Applies CODITECT methodology (PROJECT-PLAN.md, TASKLIST.md, etc.)
- Sets up standard structure
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any
import json

# Colors
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


# Project definitions
PROJECTS = [
    {
        "name": "coditect-cloud-backend",
        "description": "FastAPI backend for CODITECT Cloud Platform - user lifecycle, licensing, and API services",
        "type": "backend",
        "tech_stack": ["Python", "FastAPI", "PostgreSQL", "Redis", "Celery"],
        "github_org": "coditect-ai",
        "private": True,
        "topics": ["fastapi", "python", "saas", "user-management", "licensing"]
    },
    {
        "name": "coditect-cloud-frontend",
        "description": "React frontend for CODITECT Cloud Platform - user portal and admin dashboard",
        "type": "frontend",
        "tech_stack": ["React", "TypeScript", "TailwindCSS", "Vite"],
        "github_org": "coditect-ai",
        "private": True,
        "topics": ["react", "typescript", "tailwindcss", "admin-dashboard", "user-portal"]
    },
    {
        "name": "coditect-cli",
        "description": "Command-line tools for CODITECT - setup, Git automation, and project management",
        "type": "cli",
        "tech_stack": ["Python", "Click", "Rich", "GitPython"],
        "github_org": "coditect-ai",
        "private": False,
        "topics": ["cli", "python", "git-automation", "developer-tools"]
    },
    {
        "name": "coditect-docs",
        "description": "Official CODITECT documentation site - guides, tutorials, and API reference",
        "type": "docs",
        "tech_stack": ["Docusaurus", "Markdown", "Mermaid"],
        "github_org": "coditect-ai",
        "private": False,
        "topics": ["documentation", "docusaurus", "guides", "tutorials"]
    },
    {
        "name": "coditect-agent-marketplace",
        "description": "Marketplace for discovering and sharing specialized AI agents",
        "type": "fullstack",
        "tech_stack": ["Next.js", "TypeScript", "PostgreSQL", "Algolia"],
        "github_org": "coditect-ai",
        "private": True,
        "topics": ["nextjs", "marketplace", "ai-agents", "discovery"]
    },
    {
        "name": "coditect-analytics",
        "description": "Analytics and monitoring platform - usage tracking and business intelligence",
        "type": "backend",
        "tech_stack": ["Python", "ClickHouse", "Grafana", "Prometheus"],
        "github_org": "coditect-ai",
        "private": True,
        "topics": ["analytics", "monitoring", "grafana", "prometheus", "clickhouse"]
    },
    {
        "name": "coditect-infrastructure",
        "description": "Infrastructure as Code - Terraform, CI/CD, and deployment automation",
        "type": "infrastructure",
        "tech_stack": ["Terraform", "Docker", "GitHub Actions", "GCP"],
        "github_org": "coditect-ai",
        "private": True,
        "topics": ["terraform", "devops", "gcp", "infrastructure-as-code", "ci-cd"]
    },
    {
        "name": "coditect-legal",
        "description": "Legal documents and compliance tracking - EULA, NDA, privacy policy, etc.",
        "type": "docs",
        "tech_stack": ["Markdown", "PDF"],
        "github_org": "coditect-ai",
        "private": True,
        "topics": ["legal", "compliance", "eula", "nda", "privacy-policy"]
    }
]


class ProjectBootstrapper:
    """Bootstrap all CODITECT rollout projects"""

    def __init__(self, workspace_dir: Path = None):
        self.workspace_dir = workspace_dir or Path.home() / "PROJECTS"
        self.coditect_dir = self.workspace_dir / ".coditect"

    def run_command(self, cmd: List[str], cwd: Path = None, check=True) -> subprocess.CompletedProcess:
        """Execute shell command"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.workspace_dir,
                check=check,
                capture_output=True,
                text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}✗ Command failed: {' '.join(cmd)}{Colors.END}")
            print(f"{Colors.RED}  Error: {e.stderr}{Colors.END}")
            if check:
                raise
            return e

    def create_project_directory(self, project: Dict[str, Any]) -> Path:
        """Create project directory"""
        project_dir = self.workspace_dir / project["name"]
        project_dir.mkdir(parents=True, exist_ok=True)
        print(f"{Colors.GREEN}✓ Created directory: {project_dir}{Colors.END}")
        return project_dir

    def initialize_git(self, project_dir: Path, project: Dict[str, Any]):
        """Initialize Git repository"""
        if not (project_dir / ".git").exists():
            self.run_command(['git', 'init'], cwd=project_dir)
            self.run_command(['git', 'branch', '-m', 'main'], cwd=project_dir)
            print(f"{Colors.GREEN}✓ Git initialized{Colors.END}")

    def create_gitignore(self, project_dir: Path, project: Dict[str, Any]):
        """Create .gitignore from CODITECT template"""
        template_path = self.coditect_dir / "templates" / "gitignore-universal-template"
        gitignore_path = project_dir / ".gitignore"

        if template_path.exists():
            import shutil
            shutil.copy(template_path, gitignore_path)
            print(f"{Colors.GREEN}✓ Created .gitignore from template{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠ Template not found, skipping .gitignore{Colors.END}")

    def create_project_plan(self, project_dir: Path, project: Dict[str, Any]):
        """Create PROJECT-PLAN.md"""
        plan_path = project_dir / "PROJECT-PLAN.md"

        content = f"""# {project['name']} - Project Plan

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.**

**Project Type:** {project['type'].title()}
**Status:** Phase 1 - Discovery & Planning
**Last Updated:** 2025-11-15

---

## Executive Summary

**Problem**: [Define the problem this project solves]

**Solution**: {project['description']}

**Tech Stack**: {', '.join(project['tech_stack'])}

---

## Phase 1: Discovery & Validation

### Value Proposition

[Define the value proposition for this component]

### Ideal Customer Profile (ICP)

**Internal Users**:
- AZ1.AI development team
- Platform administrators
- Support team

**External Users** (if applicable):
- CODITECT platform users
- Third-party developers
- Integration partners

### Competitive Analysis

[Analyze similar tools/platforms if applicable]

---

## Phase 2: Strategy & Planning

### Technical Architecture

[C4 diagrams go here]

### Technology Stack

{chr(10).join(f"- **{tech}**: [Purpose/justification]" for tech in project['tech_stack'])}

### Architecture Decision Records (ADRs)

- [Create ADRs for key decisions]

---

## Phase 3: Execution & Delivery

### Development Roadmap

**Sprint 1** (Weeks 1-2):
- [ ] Project setup and infrastructure
- [ ] [Additional tasks]

**Sprint 2** (Weeks 3-4):
- [ ] Core functionality
- [ ] [Additional tasks]

[Add more sprints as needed]

### Success Metrics

**Technical Metrics**:
- [ ] [Define technical success criteria]

**Business Metrics**:
- [ ] [Define business success criteria]

---

## Next Steps

### Immediate Actions
1. [ ] Complete this project plan
2. [ ] Create TASKLIST.md
3. [ ] Create ADRs for key decisions
4. [ ] Design architecture (C4 diagrams)

---

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
"""

        with open(plan_path, 'w') as f:
            f.write(content)

        print(f"{Colors.GREEN}✓ Created PROJECT-PLAN.md{Colors.END}")

    def create_tasklist(self, project_dir: Path, project: Dict[str, Any]):
        """Create TASKLIST.md"""
        tasklist_path = project_dir / "TASKLIST.md"

        content = f"""# {project['name']} - Task List

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Status:** Planning
**Last Updated:** 2025-11-15

---

## Phase 1: Setup & Planning ⏳

- [x] Create project directory
- [x] Initialize Git repository
- [x] Create PROJECT-PLAN.md
- [x] Create TASKLIST.md
- [ ] Complete project plan (fill in details)
- [ ] Create C4 architecture diagrams
- [ ] Write ADRs for key decisions
- [ ] Setup CI/CD pipeline
- [ ] Create README.md

**Status:** IN PROGRESS (20% complete)

---

## Phase 2: Development 📝

### Sprint 1 (Weeks 1-2)

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

### Sprint 2 (Weeks 3-4)

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

**Status:** PENDING

---

## Phase 3: Testing & Deployment 🚀

- [ ] Unit tests
- [ ] Integration tests
- [ ] Documentation
- [ ] Deployment to staging
- [ ] Beta testing
- [ ] Deployment to production

**Status:** PENDING

---

## Blockers & Risks

**Current Blockers:**
- None

**Identified Risks:**
1. [Risk 1]
   - Mitigation: [Strategy]
   - Status: [Monitoring/Resolved]

---

**Last Review:** 2025-11-15
**Next Review:** [Date]
**Project Lead:** Hal Casteel (CEO/CTO)
"""

        with open(tasklist_path, 'w') as f:
            f.write(content)

        print(f"{Colors.GREEN}✓ Created TASKLIST.md{Colors.END}")

    def create_readme(self, project_dir: Path, project: Dict[str, Any]):
        """Create README.md"""
        readme_path = project_dir / "README.md"

        visibility = "🔒 Private" if project['private'] else "🌐 Public"

        content = f"""# {project['name']}

{visibility}

**{project['description']}**

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.**

---

## Overview

[Project overview goes here]

## Tech Stack

{chr(10).join(f"- {tech}" for tech in project['tech_stack'])}

## Getting Started

### Prerequisites

[List prerequisites]

### Installation

```bash
# Installation steps
```

### Configuration

[Configuration instructions]

## Development

### Setup Development Environment

```bash
# Development setup
```

### Running Locally

```bash
# Run commands
```

### Running Tests

```bash
# Test commands
```

## Deployment

[Deployment instructions]

## Documentation

- [Project Plan](PROJECT-PLAN.md)
- [Task List](TASKLIST.md)
- [Architecture Decision Records](docs/adrs/)

## Contributing

This is a private repository for AZ1.AI INC. internal development.

## License

Copyright © 2025 AZ1.AI INC. All Rights Reserved.

Proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

**Built with Excellence by AZ1.AI CODITECT**

*Systematic Development. Continuous Context. Exceptional Results.*
"""

        with open(readme_path, 'w') as f:
            f.write(content)

        print(f"{Colors.GREEN}✓ Created README.md{Colors.END}")

    def create_github_repo(self, project: Dict[str, Any]):
        """Create GitHub repository using gh CLI"""
        repo_name = f"{project['github_org']}/{project['name']}"
        visibility = "--private" if project['private'] else "--public"

        print(f"\n{Colors.CYAN}Creating GitHub repository: {repo_name}{Colors.END}")

        try:
            # Check if gh CLI is installed
            subprocess.run(['gh', '--version'], check=True, capture_output=True)
        except FileNotFoundError:
            print(f"{Colors.YELLOW}⚠ GitHub CLI (gh) not installed. Skipping GitHub repo creation.{Colors.END}")
            print(f"{Colors.YELLOW}  Install: brew install gh{Colors.END}")
            return False

        # Create repository
        try:
            result = subprocess.run(
                ['gh', 'repo', 'create', repo_name,
                 visibility,
                 '--description', project['description'],
                 '--confirm'],
                check=True,
                capture_output=True,
                text=True
            )

            print(f"{Colors.GREEN}✓ Created GitHub repository: {repo_name}{Colors.END}")

            # Add topics
            if project.get('topics'):
                topics_str = ' '.join(project['topics'])
                subprocess.run(
                    ['gh', 'repo', 'edit', repo_name, '--add-topic', topics_str],
                    check=False,
                    capture_output=True
                )
                print(f"{Colors.GREEN}✓ Added topics: {topics_str}{Colors.END}")

            return True

        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr:
                print(f"{Colors.YELLOW}⚠ Repository already exists: {repo_name}{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}✗ Failed to create repository: {e.stderr}{Colors.END}")
                return False

    def setup_remote(self, project_dir: Path, project: Dict[str, Any]):
        """Setup GitHub remote"""
        remote_url = f"https://github.com/{project['github_org']}/{project['name']}.git"

        try:
            # Check if remote exists
            result = self.run_command(['git', 'remote', 'get-url', 'origin'], cwd=project_dir, check=False)

            if result.returncode != 0:
                # Add remote
                self.run_command(['git', 'remote', 'add', 'origin', remote_url], cwd=project_dir)
                print(f"{Colors.GREEN}✓ Added remote: origin{Colors.END}")
            else:
                print(f"{Colors.YELLOW}ℹ Remote already configured{Colors.END}")

        except Exception as e:
            print(f"{Colors.YELLOW}⚠ Could not setup remote: {e}{Colors.END}")

    def initial_commit(self, project_dir: Path, project: Dict[str, Any]):
        """Create initial commit"""
        try:
            # Add all files
            self.run_command(['git', 'add', '.'], cwd=project_dir)

            # Create commit
            commit_message = f"""Initialize {project['name']}

- Add PROJECT-PLAN.md
- Add TASKLIST.md
- Add README.md
- Configure .gitignore

Copyright © 2025 AZ1.AI INC. All Rights Reserved."""

            self.run_command(['git', 'commit', '-m', commit_message], cwd=project_dir)

            print(f"{Colors.GREEN}✓ Created initial commit{Colors.END}")

        except subprocess.CalledProcessError:
            print(f"{Colors.YELLOW}⚠ No changes to commit{Colors.END}")

    def push_to_github(self, project_dir: Path, project: Dict[str, Any]):
        """Push to GitHub"""
        try:
            self.run_command(['git', 'push', '-u', 'origin', 'main'], cwd=project_dir)
            print(f"{Colors.GREEN}✓ Pushed to GitHub{Colors.END}")

        except subprocess.CalledProcessError as e:
            print(f"{Colors.YELLOW}⚠ Could not push to GitHub: {e.stderr}{Colors.END}")
            print(f"{Colors.YELLOW}  You may need to authenticate first: gh auth login{Colors.END}")

    def bootstrap_project(self, project: Dict[str, Any]):
        """Bootstrap single project"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}Bootstrapping: {project['name']}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}\n")

        # Create directory
        project_dir = self.create_project_directory(project)

        # Initialize Git
        self.initialize_git(project_dir, project)

        # Create standard files
        self.create_gitignore(project_dir, project)
        self.create_project_plan(project_dir, project)
        self.create_tasklist(project_dir, project)
        self.create_readme(project_dir, project)

        # Create GitHub repository
        github_created = self.create_github_repo(project)

        # Setup remote
        if github_created:
            self.setup_remote(project_dir, project)

        # Initial commit
        self.initial_commit(project_dir, project)

        # Push to GitHub
        if github_created:
            self.push_to_github(project_dir, project)

        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Project bootstrap complete: {project['name']}{Colors.END}\n")

    def bootstrap_all(self):
        """Bootstrap all projects"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}║         AZ1.AI CODITECT Project Bootstrap v1.0                 ║{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}║  Setting up {len(PROJECTS)} projects for CODITECT rollout                  ║{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚════════════════════════════════════════════════════════════════╝{Colors.END}\n")

        print(f"{Colors.BOLD}Projects to create:{Colors.END}")
        for i, project in enumerate(PROJECTS, 1):
            visibility = "🔒" if project['private'] else "🌐"
            print(f"  {i}. {visibility} {project['name']}")

        print()
        response = input(f"{Colors.YELLOW}Proceed with bootstrap? (y/n): {Colors.END}").strip().lower()

        if response != 'y':
            print(f"{Colors.YELLOW}Bootstrap cancelled{Colors.END}")
            return

        # Bootstrap each project
        for project in PROJECTS:
            try:
                self.bootstrap_project(project)
            except Exception as e:
                print(f"{Colors.RED}✗ Error bootstrapping {project['name']}: {e}{Colors.END}")
                continue

        # Summary
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                  ALL PROJECTS BOOTSTRAPPED! 🎉                 ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚════════════════════════════════════════════════════════════════╝{Colors.END}\n")

        print(f"{Colors.BOLD}Projects created in: {self.workspace_dir}{Colors.END}\n")

        print(f"{Colors.BOLD}Next steps:{Colors.END}")
        print(f"  1. Review each PROJECT-PLAN.md and fill in details")
        print(f"  2. Create C4 architecture diagrams")
        print(f"  3. Write ADRs for key technology decisions")
        print(f"  4. Begin Sprint 1 development")
        print()


def main():
    """Entry point"""
    bootstrapper = ProjectBootstrapper()
    bootstrapper.bootstrap_all()


if __name__ == '__main__':
    main()
