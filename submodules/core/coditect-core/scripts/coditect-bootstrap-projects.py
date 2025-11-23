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
from typing import List, Dict, Any, Optional
import json
import logging
import shutil
from datetime import datetime
import time

# ============================================================================
# EXCEPTION HIERARCHY
# ============================================================================

class BootstrapError(Exception):
    """Base exception for bootstrap errors."""
    pass


class PrerequisiteError(BootstrapError):
    """Raised when prerequisites are not met."""
    pass


class GitOperationError(BootstrapError):
    """Raised when git operation fails."""
    pass


class GitHubOperationError(BootstrapError):
    """Raised when GitHub operation fails."""
    pass


class TemplateGenerationError(BootstrapError):
    """Raised when template generation fails."""
    pass


class DirectoryCreationError(BootstrapError):
    """Raised when directory creation fails."""
    pass


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging(log_file: Path = None, verbose: bool = False) -> logging.Logger:
    """
    Configure dual logging (file + stdout) with production formatting.

    Args:
        log_file: Path to log file (default: logs/bootstrap_TIMESTAMP.log)
        verbose: Enable debug-level logging

    Returns:
        Configured logger instance
    """
    # Create logs directory if needed
    if log_file is None:
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"bootstrap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Configure root logger
    logger = logging.getLogger("coditect_bootstrap")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # File handler - detailed logs
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler - user-friendly output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logging initialized: {log_file}")
    return logger


# ============================================================================
# TERMINAL COLORS
# ============================================================================

class Colors:
    """ANSI color codes for terminal output."""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


# ============================================================================
# EXIT CODES
# ============================================================================

class ExitCode:
    """Standardized exit codes."""
    SUCCESS = 0
    GENERAL_ERROR = 1
    PREREQUISITE_ERROR = 2
    GIT_ERROR = 3
    GITHUB_ERROR = 4
    TEMPLATE_ERROR = 5


# ============================================================================
# PROJECT DEFINITIONS
# ============================================================================

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


# ============================================================================
# MAIN CLASS
# ============================================================================

class ProjectBootstrapper:
    """Bootstrap all CODITECT rollout projects with production-grade error handling."""

    def __init__(self, workspace_dir: Path = None, logger: logging.Logger = None):
        """
        Initialize bootstrapper.

        Args:
            workspace_dir: Root workspace directory (default: ~/PROJECTS)
            logger: Logger instance (will create if not provided)
        """
        self.workspace_dir = workspace_dir or Path.home() / "PROJECTS"
        self.coditect_dir = self.workspace_dir / ".coditect"
        self.logger = logger or setup_logging()
        self.created_projects: List[str] = []
        self.failed_projects: List[tuple] = []  # (name, error)

    def check_prerequisites(self) -> None:
        """
        Verify all prerequisites are met.

        Raises:
            PrerequisiteError: If prerequisites not met
        """
        self.logger.info("Checking prerequisites...")

        # Check workspace directory exists
        if not self.workspace_dir.exists():
            raise PrerequisiteError(f"Workspace directory does not exist: {self.workspace_dir}")

        # Check .coditect directory exists
        if not self.coditect_dir.exists():
            self.logger.warning(f".coditect directory not found at {self.coditect_dir}")
            self.logger.info("Continuing without CODITECT templates")

        # Check git installed
        try:
            result = self.run_command(['git', '--version'], check_output=False)
            self.logger.debug(f"Git version: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise PrerequisiteError("Git is not installed or not in PATH")

        # Check git configured
        try:
            self.run_command(['git', 'config', 'user.name'], check_output=False)
            self.run_command(['git', 'config', 'user.email'], check_output=False)
        except subprocess.CalledProcessError:
            raise PrerequisiteError(
                "Git user.name and user.email not configured. "
                "Run: git config --global user.name 'Your Name' && "
                "git config --global user.email 'you@example.com'"
            )

        # Check GitHub CLI (optional but recommended)
        try:
            result = self.run_command(['gh', '--version'], check_output=False)
            self.logger.debug(f"GitHub CLI version: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning("GitHub CLI (gh) not installed - repository creation will be skipped")
            self.logger.info("Install with: brew install gh")

        self.logger.info(f"{Colors.GREEN}✓ Prerequisites verified{Colors.END}")

    def run_command(
        self,
        cmd: List[str],
        cwd: Path = None,
        check: bool = True,
        check_output: bool = True,
        timeout: int = 30,
        retry_count: int = 3,
        retry_delay: int = 2
    ) -> subprocess.CompletedProcess:
        """
        Execute shell command with retry logic.

        Args:
            cmd: Command and arguments as list
            cwd: Working directory (default: workspace_dir)
            check: Raise exception on non-zero exit
            check_output: Capture stdout/stderr
            timeout: Command timeout in seconds
            retry_count: Number of retry attempts for network operations
            retry_delay: Delay between retries in seconds

        Returns:
            CompletedProcess instance

        Raises:
            subprocess.CalledProcessError: If check=True and command fails
            subprocess.TimeoutExpired: If command exceeds timeout
        """
        for attempt in range(1, retry_count + 1):
            try:
                self.logger.debug(f"Running command (attempt {attempt}/{retry_count}): {' '.join(cmd)}")

                result = subprocess.run(
                    cmd,
                    cwd=cwd or self.workspace_dir,
                    check=check,
                    capture_output=check_output,
                    text=True,
                    timeout=timeout
                )

                if check_output and result.stdout:
                    self.logger.debug(f"Command output: {result.stdout.strip()}")

                return result

            except subprocess.TimeoutExpired as e:
                self.logger.error(f"Command timed out after {timeout}s: {' '.join(cmd)}")
                if attempt >= retry_count:
                    raise
                self.logger.info(f"Retrying in {retry_delay}s...")
                time.sleep(retry_delay)

            except subprocess.CalledProcessError as e:
                self.logger.error(f"Command failed: {' '.join(cmd)}")
                self.logger.error(f"Exit code: {e.returncode}")
                if e.stderr:
                    self.logger.error(f"Error output: {e.stderr.strip()}")

                # Retry for network-related operations
                if any(term in ' '.join(cmd) for term in ['clone', 'push', 'pull', 'fetch']) and attempt < retry_count:
                    self.logger.info(f"Network operation failed, retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue

                if check:
                    raise
                return e

        # Should not reach here, but just in case
        raise subprocess.CalledProcessError(1, cmd, "Max retries exceeded")

    def create_project_directory(self, project: Dict[str, Any]) -> Path:
        """
        Create project directory.

        Args:
            project: Project configuration dictionary

        Returns:
            Path to created project directory

        Raises:
            DirectoryCreationError: If directory creation fails
        """
        try:
            project_dir = self.workspace_dir / project["name"]

            if project_dir.exists():
                self.logger.warning(f"Directory already exists: {project_dir}")
                return project_dir

            project_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"{Colors.GREEN}✓ Created directory: {project_dir}{Colors.END}")
            return project_dir

        except Exception as e:
            raise DirectoryCreationError(f"Failed to create directory {project['name']}: {e}")

    def initialize_git(self, project_dir: Path, project: Dict[str, Any]) -> None:
        """
        Initialize Git repository.

        Args:
            project_dir: Project directory path
            project: Project configuration

        Raises:
            GitOperationError: If git initialization fails
        """
        try:
            if (project_dir / ".git").exists():
                self.logger.info("Git repository already initialized")
                return

            self.run_command(['git', 'init'], cwd=project_dir)
            self.run_command(['git', 'branch', '-m', 'main'], cwd=project_dir)
            self.logger.info(f"{Colors.GREEN}✓ Git initialized{Colors.END}")

        except subprocess.CalledProcessError as e:
            raise GitOperationError(f"Git initialization failed: {e}")

    def create_gitignore(self, project_dir: Path, project: Dict[str, Any]) -> None:
        """
        Create .gitignore from CODITECT template.

        Args:
            project_dir: Project directory path
            project: Project configuration

        Raises:
            TemplateGenerationError: If gitignore creation fails
        """
        try:
            template_path = self.coditect_dir / "templates" / "gitignore-universal-template"
            gitignore_path = project_dir / ".gitignore"

            if gitignore_path.exists():
                self.logger.info(".gitignore already exists")
                return

            if template_path.exists():
                shutil.copy(template_path, gitignore_path)
                self.logger.info(f"{Colors.GREEN}✓ Created .gitignore from template{Colors.END}")
            else:
                self.logger.warning("Template not found, creating basic .gitignore")
                self._create_basic_gitignore(gitignore_path, project)

        except Exception as e:
            raise TemplateGenerationError(f".gitignore creation failed: {e}")

    def _create_basic_gitignore(self, gitignore_path: Path, project: Dict[str, Any]) -> None:
        """Create basic .gitignore when template not available."""
        content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Node
node_modules/
npm-debug.log*

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/

# Logs
*.log

# Environment
.env
.env.local
"""
        gitignore_path.write_text(content)
        self.logger.info(f"{Colors.GREEN}✓ Created basic .gitignore{Colors.END}")

    def create_project_plan(self, project_dir: Path, project: Dict[str, Any]) -> None:
        """
        Create PROJECT-PLAN.md.

        Args:
            project_dir: Project directory path
            project: Project configuration

        Raises:
            TemplateGenerationError: If creation fails
        """
        try:
            plan_path = project_dir / "PROJECT-PLAN.md"

            if plan_path.exists():
                self.logger.info("PROJECT-PLAN.md already exists")
                return

            content = f"""# {project['name']} - Project Plan

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.**

**Project Type:** {project['type'].title()}
**Status:** Phase 1 - Discovery & Planning
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

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

            plan_path.write_text(content)
            self.logger.info(f"{Colors.GREEN}✓ Created PROJECT-PLAN.md{Colors.END}")

        except Exception as e:
            raise TemplateGenerationError(f"PROJECT-PLAN.md creation failed: {e}")

    def create_tasklist(self, project_dir: Path, project: Dict[str, Any]) -> None:
        """
        Create TASKLIST.md.

        Args:
            project_dir: Project directory path
            project: Project configuration

        Raises:
            TemplateGenerationError: If creation fails
        """
        try:
            tasklist_path = project_dir / "TASKLIST.md"

            if tasklist_path.exists():
                self.logger.info("TASKLIST.md already exists")
                return

            content = f"""# {project['name']} - Task List

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Status:** Planning
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

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

**Last Review:** {datetime.now().strftime('%Y-%m-%d')}
**Next Review:** [Date]
**Project Lead:** Hal Casteel (CEO/CTO)
"""

            tasklist_path.write_text(content)
            self.logger.info(f"{Colors.GREEN}✓ Created TASKLIST.md{Colors.END}")

        except Exception as e:
            raise TemplateGenerationError(f"TASKLIST.md creation failed: {e}")

    def create_readme(self, project_dir: Path, project: Dict[str, Any]) -> None:
        """
        Create README.md.

        Args:
            project_dir: Project directory path
            project: Project configuration

        Raises:
            TemplateGenerationError: If creation fails
        """
        try:
            readme_path = project_dir / "README.md"

            if readme_path.exists():
                self.logger.info("README.md already exists")
                return

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

            readme_path.write_text(content)
            self.logger.info(f"{Colors.GREEN}✓ Created README.md{Colors.END}")

        except Exception as e:
            raise TemplateGenerationError(f"README.md creation failed: {e}")

    def create_github_repo(self, project: Dict[str, Any]) -> bool:
        """
        Create GitHub repository using gh CLI.

        Args:
            project: Project configuration

        Returns:
            True if successful, False otherwise

        Raises:
            GitHubOperationError: If creation fails critically
        """
        repo_name = f"{project['github_org']}/{project['name']}"
        visibility = "--private" if project['private'] else "--public"

        self.logger.info(f"Creating GitHub repository: {repo_name}")

        try:
            # Check if gh CLI is installed
            self.run_command(['gh', '--version'], check_output=False)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning("GitHub CLI (gh) not installed - skipping repository creation")
            return False

        # Create repository
        try:
            self.run_command(
                ['gh', 'repo', 'create', repo_name,
                 visibility,
                 '--description', project['description'],
                 '--confirm'],
                retry_count=2
            )

            self.logger.info(f"{Colors.GREEN}✓ Created GitHub repository: {repo_name}{Colors.END}")

            # Add topics
            if project.get('topics'):
                topics_str = ' '.join(project['topics'])
                try:
                    self.run_command(
                        ['gh', 'repo', 'edit', repo_name, '--add-topic', topics_str],
                        check=False
                    )
                    self.logger.info(f"{Colors.GREEN}✓ Added topics: {topics_str}{Colors.END}")
                except subprocess.CalledProcessError:
                    self.logger.warning("Failed to add topics (non-critical)")

            return True

        except subprocess.CalledProcessError as e:
            if e.stderr and "already exists" in e.stderr:
                self.logger.warning(f"Repository already exists: {repo_name}")
                return True
            else:
                self.logger.error(f"Failed to create repository: {e.stderr if e.stderr else str(e)}")
                return False

    def setup_remote(self, project_dir: Path, project: Dict[str, Any]) -> None:
        """
        Setup GitHub remote.

        Args:
            project_dir: Project directory path
            project: Project configuration

        Raises:
            GitOperationError: If setup fails
        """
        try:
            remote_url = f"https://github.com/{project['github_org']}/{project['name']}.git"

            # Check if remote exists
            result = self.run_command(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=project_dir,
                check=False
            )

            if result.returncode != 0:
                # Add remote
                self.run_command(['git', 'remote', 'add', 'origin', remote_url], cwd=project_dir)
                self.logger.info(f"{Colors.GREEN}✓ Added remote: origin{Colors.END}")
            else:
                self.logger.info("Remote already configured")

        except subprocess.CalledProcessError as e:
            raise GitOperationError(f"Remote setup failed: {e}")

    def initial_commit(self, project_dir: Path, project: Dict[str, Any]) -> None:
        """
        Create initial commit.

        Args:
            project_dir: Project directory path
            project: Project configuration

        Raises:
            GitOperationError: If commit fails
        """
        try:
            # Check if there are changes to commit
            status_result = self.run_command(
                ['git', 'status', '--porcelain'],
                cwd=project_dir
            )

            if not status_result.stdout.strip():
                self.logger.info("No changes to commit")
                return

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

            self.logger.info(f"{Colors.GREEN}✓ Created initial commit{Colors.END}")

        except subprocess.CalledProcessError as e:
            # Empty commit is not an error
            if "nothing to commit" in (e.stderr or ""):
                self.logger.info("Nothing to commit")
            else:
                raise GitOperationError(f"Initial commit failed: {e}")

    def push_to_github(self, project_dir: Path, project: Dict[str, Any]) -> None:
        """
        Push to GitHub.

        Args:
            project_dir: Project directory path
            project: Project configuration

        Raises:
            GitOperationError: If push fails
        """
        try:
            self.run_command(
                ['git', 'push', '-u', 'origin', 'main'],
                cwd=project_dir,
                retry_count=2
            )
            self.logger.info(f"{Colors.GREEN}✓ Pushed to GitHub{Colors.END}")

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            self.logger.warning(f"Push failed: {error_msg}")
            self.logger.info("You may need to authenticate with: gh auth login")

    def bootstrap_project(self, project: Dict[str, Any]) -> None:
        """
        Bootstrap single project.

        Args:
            project: Project configuration

        Raises:
            BootstrapError: If bootstrap fails
        """
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}Bootstrapping: {project['name']}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}\n")

        try:
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

            self.created_projects.append(project['name'])
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Project bootstrap complete: {project['name']}{Colors.END}\n")

        except Exception as e:
            self.logger.error(f"Failed to bootstrap {project['name']}: {e}", exc_info=True)
            self.failed_projects.append((project['name'], str(e)))
            raise

    def bootstrap_all(self, skip_confirmation: bool = False) -> None:
        """
        Bootstrap all projects.

        Args:
            skip_confirmation: Skip user confirmation prompt

        Raises:
            BootstrapError: If critical error occurs
        """
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

        if not skip_confirmation:
            response = input(f"{Colors.YELLOW}Proceed with bootstrap? (y/n): {Colors.END}").strip().lower()

            if response != 'y':
                print(f"{Colors.YELLOW}Bootstrap cancelled{Colors.END}")
                return

        # Bootstrap each project
        for project in PROJECTS:
            try:
                self.bootstrap_project(project)
            except Exception as e:
                self.logger.error(f"Error bootstrapping {project['name']}: {e}")
                # Continue with next project
                continue

        # Summary
        self._print_summary()

    def _print_summary(self) -> None:
        """Print bootstrap summary."""
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                  BOOTSTRAP COMPLETE! 🎉                        ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}║                                                                ║{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚════════════════════════════════════════════════════════════════╝{Colors.END}\n")

        print(f"{Colors.BOLD}Results:{Colors.END}")
        print(f"  Successful: {len(self.created_projects)}/{len(PROJECTS)}")
        if self.failed_projects:
            print(f"  {Colors.RED}Failed: {len(self.failed_projects)}{Colors.END}")
            for name, error in self.failed_projects:
                print(f"    - {name}: {error}")

        print(f"\n{Colors.BOLD}Projects created in: {self.workspace_dir}{Colors.END}\n")

        if self.created_projects:
            print(f"{Colors.BOLD}Next steps:{Colors.END}")
            print(f"  1. Review each PROJECT-PLAN.md and fill in details")
            print(f"  2. Create C4 architecture diagrams")
            print(f"  3. Write ADRs for key technology decisions")
            print(f"  4. Begin Sprint 1 development")
        print()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code
    """
    import argparse

    parser = argparse.ArgumentParser(description='CODITECT Project Bootstrap')
    parser.add_argument('--workspace', '-w', type=Path, help='Workspace directory (default: ~/PROJECTS)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation prompt')
    parser.add_argument('--log-file', type=Path, help='Log file path')

    args = parser.parse_args()

    try:
        # Setup logging
        logger = setup_logging(log_file=args.log_file, verbose=args.verbose)

        # Create bootstrapper
        bootstrapper = ProjectBootstrapper(
            workspace_dir=args.workspace,
            logger=logger
        )

        # Check prerequisites
        bootstrapper.check_prerequisites()

        # Bootstrap all projects
        bootstrapper.bootstrap_all(skip_confirmation=args.yes)

        # Return success if at least some projects succeeded
        if bootstrapper.created_projects:
            return ExitCode.SUCCESS
        else:
            return ExitCode.GENERAL_ERROR

    except PrerequisiteError as e:
        print(f"{Colors.RED}✗ Prerequisites not met: {e}{Colors.END}")
        return ExitCode.PREREQUISITE_ERROR

    except GitOperationError as e:
        print(f"{Colors.RED}✗ Git operation failed: {e}{Colors.END}")
        return ExitCode.GIT_ERROR

    except GitHubOperationError as e:
        print(f"{Colors.RED}✗ GitHub operation failed: {e}{Colors.END}")
        return ExitCode.GITHUB_ERROR

    except TemplateGenerationError as e:
        print(f"{Colors.RED}✗ Template generation failed: {e}{Colors.END}")
        return ExitCode.TEMPLATE_ERROR

    except Exception as e:
        print(f"{Colors.RED}✗ Unexpected error: {e}{Colors.END}")
        logging.exception("Unexpected error during bootstrap")
        return ExitCode.GENERAL_ERROR


if __name__ == '__main__':
    sys.exit(main())
