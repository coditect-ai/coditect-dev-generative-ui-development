#!/usr/bin/env python3
"""
AZ1.AI CODITECT Master Project Setup Automation

This script creates a MASTER PLAN repository with all sub-projects as git submodules,
enabling autonomous AI-first CODITECT development with centralized orchestration.

This represents a core CODITECT capability: master project orchestration with automated
sub-project management, making it easy for any user to manage complex multi-repo projects.

Copyright © 2025 AZ1.AI INC. All Rights Reserved.
Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
import logging
import shutil

# Custom exceptions
class MasterProjectSetupError(Exception):
    """Base exception for master project setup errors."""
    pass

class PrerequisiteError(MasterProjectSetupError):
    """Raised when prerequisites check fails."""
    pass

class DirectorySetupError(MasterProjectSetupError):
    """Raised when directory setup fails."""
    pass

class GitOperationError(MasterProjectSetupError):
    """Raised when git operation fails."""
    pass

class GitHubAPIError(MasterProjectSetupError):
    """Raised when GitHub API operation fails."""
    pass

class NetworkError(MasterProjectSetupError):
    """Raised when network operation fails."""
    pass

class CoditectMasterProjectSetup:
    """
    Autonomous setup of CODITECT master project with sub-project orchestration.

    This class embodies CODITECT's core capability: treating a master project plan
    as the orchestrator for multiple sub-projects (as git submodules), with full
    automation for creation, tracking, and synchronization.
    """

    def __init__(self, master_project_name: str = "coditect-rollout-master",
                 projects_root: str = None):
        """
        Initialize master project setup.

        Args:
            master_project_name: Name of master orchestration project
            projects_root: Root directory for all projects (default: ~/PROJECTS)
        """
        # Validate inputs
        if not master_project_name or not isinstance(master_project_name, str):
            raise ValueError("master_project_name must be a non-empty string")

        self.master_project_name = master_project_name
        self.projects_root = Path(projects_root or os.path.expanduser("~/PROJECTS"))
        self.master_project_path = self.projects_root / master_project_name

        # GitHub organization for CODITECT projects
        self.github_org = "coditect-ai"

        # Session tracking
        self.session_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.session_log = []
        self.rollback_actions = []  # Track actions for rollback

        # Color codes for output
        self.GREEN = "\033[92m"
        self.YELLOW = "\033[93m"
        self.RED = "\033[91m"
        self.BLUE = "\033[94m"
        self.RESET = "\033[0m"

        # Setup logging
        self.setup_logging()

        # Master project structure - all sub-projects
        self.sub_projects = self._define_sub_projects()

        # Network retry configuration
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        self.rate_limit_delay = 5  # seconds for GitHub API rate limiting

    def setup_logging(self):
        """Configure dual logging to stdout and file."""
        log_file = Path(f"coditect-master-setup-{self.session_id}.log")

        # Create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # File handler (DEBUG level)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)

        # Console handler (INFO level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_format)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info(f"Logging initialized: {log_file}")

    def _define_sub_projects(self) -> List[Dict[str, Any]]:
        """
        Define all sub-projects for the CODITECT platform rollout.

        This is the master list of all repositories that will be created
        and managed as submodules under the master orchestration project.
        """
        return [
            {
                "name": "coditect-cloud-backend",
                "description": "FastAPI backend for CODITECT Cloud Platform with user management, authentication, and license tracking",
                "type": "backend",
                "tech_stack": ["Python 3.11+", "FastAPI", "PostgreSQL 15", "Redis 7", "Celery"],
                "github_org": self.github_org,
                "private": True,
                "priority": "P0",
                "timeline": "12 weeks",
                "budget": "$135K",
                "team_size": 3
            },
            {
                "name": "coditect-cloud-frontend",
                "description": "React TypeScript frontend for CODITECT Cloud Platform with user onboarding and admin dashboard",
                "type": "frontend",
                "tech_stack": ["React 18", "TypeScript", "TailwindCSS", "Vite", "React Router"],
                "github_org": self.github_org,
                "private": True,
                "priority": "P0",
                "timeline": "10 weeks",
                "budget": "$110K",
                "team_size": 2
            },
            {
                "name": "coditect-cli",
                "description": "Python CLI tools for CODITECT setup, git automation, and session management",
                "type": "cli",
                "tech_stack": ["Python 3.11+", "Click/Typer", "Rich", "GitPython", "PyYAML"],
                "github_org": self.github_org,
                "private": False,
                "priority": "P0",
                "timeline": "8 weeks",
                "budget": "$75K",
                "team_size": 2
            },
            {
                "name": "coditect-docs",
                "description": "Docusaurus documentation site for CODITECT with tutorials, API docs, and guides",
                "type": "documentation",
                "tech_stack": ["Docusaurus", "React", "MDX", "Algolia Search"],
                "github_org": self.github_org,
                "private": False,
                "priority": "P0",
                "timeline": "6 weeks",
                "budget": "$55K",
                "team_size": 1
            },
            {
                "name": "coditect-agent-marketplace",
                "description": "Next.js marketplace for AI agents with discovery, ratings, and installation",
                "type": "frontend",
                "tech_stack": ["Next.js 14", "TypeScript", "Prisma", "PostgreSQL", "Stripe"],
                "github_org": self.github_org,
                "private": False,
                "priority": "P1",
                "timeline": "10 weeks",
                "budget": "$95K",
                "team_size": 2
            },
            {
                "name": "coditect-analytics",
                "description": "ClickHouse analytics platform for usage tracking and insights with Grafana dashboards",
                "type": "backend",
                "tech_stack": ["ClickHouse", "Grafana", "Prometheus", "Python", "TimescaleDB"],
                "github_org": self.github_org,
                "private": True,
                "priority": "P1",
                "timeline": "6 weeks",
                "budget": "$65K",
                "team_size": 1
            },
            {
                "name": "coditect-infrastructure",
                "description": "Terraform infrastructure as code for GCP deployment with Docker and Kubernetes",
                "type": "infrastructure",
                "tech_stack": ["Terraform", "GCP", "Docker", "Kubernetes", "GitHub Actions"],
                "github_org": self.github_org,
                "private": True,
                "priority": "P0",
                "timeline": "8 weeks",
                "budget": "$85K",
                "team_size": 1
            },
            {
                "name": "coditect-legal",
                "description": "Legal documents repository with EULA, NDA, Terms of Service, and compliance templates",
                "type": "documentation",
                "tech_stack": ["Markdown", "LaTeX", "Pandoc"],
                "github_org": self.github_org,
                "private": True,
                "priority": "P0",
                "timeline": "4 weeks",
                "budget": "$35K",
                "team_size": 1
            },
            {
                "name": "coditect-framework",
                "description": "Core CODITECT framework with .claude directory, agents, skills, and templates",
                "type": "framework",
                "tech_stack": ["Python", "Markdown", "YAML", "Jinja2"],
                "github_org": self.github_org,
                "private": False,
                "priority": "P0",
                "timeline": "Ongoing",
                "budget": "Included",
                "team_size": 1
            },
            {
                "name": "coditect-automation",
                "description": "Autonomous AI-first orchestration with multi-agent coordination and task automation",
                "type": "backend",
                "tech_stack": ["Python", "RabbitMQ", "Redis", "PostgreSQL", "LangGraph"],
                "github_org": self.github_org,
                "private": True,
                "priority": "P1",
                "timeline": "8 weeks",
                "budget": "$100K",
                "team_size": 2
            }
        ]

    def print_banner(self):
        """Print welcome banner."""
        print(f"\n{self.BLUE}{'='*80}")
        print(f"  AZ1.AI CODITECT Master Project Setup")
        print(f"  Autonomous AI-First Development Orchestration")
        print(f"{'='*80}{self.RESET}\n")

    def print_status(self, message: str, status: str = "INFO"):
        """Print status message with color coding."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status == "SUCCESS":
            color = self.GREEN
            icon = "✓"
            log_level = logging.INFO
        elif status == "WARNING":
            color = self.YELLOW
            icon = "⚠"
            log_level = logging.WARNING
        elif status == "ERROR":
            color = self.RED
            icon = "✗"
            log_level = logging.ERROR
        else:
            color = self.BLUE
            icon = "→"
            log_level = logging.INFO

        formatted_message = f"{color}[{timestamp}] {icon} {message}{self.RESET}"
        print(formatted_message)
        self.logger.log(log_level, f"[{status}] {message}")
        self.session_log.append({"timestamp": timestamp, "status": status, "message": message})

    def run_command_with_retry(self, cmd: List[str], cwd: Path = None,
                               max_retries: int = None) -> subprocess.CompletedProcess:
        """
        Run command with exponential backoff retry logic.

        Args:
            cmd: Command to execute
            cwd: Working directory
            max_retries: Maximum retry attempts (default: self.max_retries)

        Returns:
            CompletedProcess result

        Raises:
            NetworkError: If network operation fails after retries
            subprocess.CalledProcessError: If command fails for non-network reasons
        """
        max_retries = max_retries or self.max_retries
        last_error = None

        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    cmd,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=30  # 30 second timeout
                )
                return result
            except subprocess.TimeoutExpired as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    self.print_status(
                        f"Command timeout (attempt {attempt + 1}/{max_retries}), retrying in {delay}s...",
                        "WARNING"
                    )
                    time.sleep(delay)
                else:
                    raise NetworkError(f"Command timed out after {max_retries} attempts: {' '.join(cmd)}")
            except subprocess.CalledProcessError as e:
                # Check if it's a network-related error
                if "network" in e.stderr.lower() or "connection" in e.stderr.lower():
                    last_error = e
                    if attempt < max_retries - 1:
                        delay = self.retry_delay * (2 ** attempt)
                        self.print_status(
                            f"Network error (attempt {attempt + 1}/{max_retries}), retrying in {delay}s...",
                            "WARNING"
                        )
                        time.sleep(delay)
                    else:
                        raise NetworkError(f"Network error after {max_retries} attempts: {e.stderr}")
                else:
                    # Non-network error, re-raise immediately
                    raise

        # Should not reach here, but handle it
        if last_error:
            raise NetworkError(f"Failed after {max_retries} attempts: {last_error}")

    def check_prerequisites(self) -> bool:
        """Check that required tools are installed."""
        self.print_status("Checking prerequisites...", "INFO")

        required_tools = {
            "git": "git --version",
            "gh": "gh --version",
            "python3": "python3 --version"
        }

        all_present = True
        for tool, check_cmd in required_tools.items():
            try:
                result = subprocess.run(check_cmd.split(),
                                      capture_output=True, text=True, check=True, timeout=10)
                version = result.stdout.split("\n")[0]
                self.print_status(f"{tool}: {version}", "SUCCESS")
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
                self.print_status(f"{tool} not found or failed: {e}", "ERROR")
                all_present = False

        if not all_present:
            raise PrerequisiteError("Missing required tools. Please install them first.")

        # Check GitHub CLI authentication
        try:
            subprocess.run(["gh", "auth", "status"],
                         capture_output=True, check=True, timeout=10)
            self.print_status("GitHub CLI authenticated", "SUCCESS")
        except subprocess.CalledProcessError:
            raise PrerequisiteError("GitHub CLI not authenticated. Run: gh auth login")
        except subprocess.TimeoutExpired:
            raise PrerequisiteError("GitHub CLI authentication check timed out")

        return True

    def create_master_project_directory(self) -> bool:
        """Create master project directory structure."""
        self.print_status(f"Creating master project directory: {self.master_project_path}", "INFO")

        try:
            if self.master_project_path.exists():
                self.print_status(f"Directory already exists: {self.master_project_path}", "WARNING")
                response = input(f"{self.YELLOW}Delete and recreate? (yes/no): {self.RESET}")
                if response.lower() == "yes":
                    shutil.rmtree(self.master_project_path)
                    self.print_status("Deleted existing directory", "SUCCESS")
                else:
                    raise DirectorySetupError("User cancelled setup - directory already exists")

            self.master_project_path.mkdir(parents=True, exist_ok=True)
            self.rollback_actions.append(("rmdir", self.master_project_path))
            self.print_status(f"Created: {self.master_project_path}", "SUCCESS")

            # Create subdirectories
            subdirs = [
                "docs",           # Master documentation
                "scripts",        # Orchestration scripts
                "templates",      # Project templates
                "workflows",      # CI/CD workflows
                "reports",        # Status reports
                "MEMORY-CONTEXT"  # Session exports
            ]

            for subdir in subdirs:
                subdir_path = self.master_project_path / subdir
                subdir_path.mkdir(exist_ok=True)
                self.print_status(f"Created subdirectory: {subdir}/", "SUCCESS")

            return True
        except PermissionError as e:
            raise DirectorySetupError(f"Permission denied creating directory: {e}")
        except OSError as e:
            raise DirectorySetupError(f"OS error creating directory: {e}")

    def initialize_git_repository(self) -> bool:
        """Initialize git repository in master project."""
        self.print_status("Initializing git repository...", "INFO")

        try:
            os.chdir(self.master_project_path)

            # Initialize git
            subprocess.run(["git", "init"], check=True, capture_output=True, timeout=10)
            subprocess.run(["git", "branch", "-M", "main"], check=True, capture_output=True, timeout=10)
            self.rollback_actions.append(("git_deinit", self.master_project_path))
            self.print_status("Git repository initialized", "SUCCESS")

            # Copy .gitignore from template
            template_gitignore = self.projects_root / "coditect-core" / "templates" / "gitignore-universal-template"
            if template_gitignore.exists():
                shutil.copy(template_gitignore, self.master_project_path / ".gitignore")
                self.print_status("Copied universal .gitignore template", "SUCCESS")

            return True
        except subprocess.CalledProcessError as e:
            raise GitOperationError(f"Git initialization failed: {e.stderr}")
        except subprocess.TimeoutExpired:
            raise GitOperationError("Git initialization timed out")

    def create_master_readme(self) -> bool:
        """Create comprehensive README for master project."""
        self.print_status("Creating master README.md...", "INFO")

        try:
            readme_content = f"""# {self.master_project_name.upper().replace('-', ' ')}

**Master Orchestration Repository for AZ1.AI CODITECT Platform Rollout**

---

## Overview

This repository serves as the **MASTER PLAN** orchestration point for the complete AZ1.AI CODITECT platform rollout from beta through pilot to full Go-to-Market (GTM).

**Key Capabilities:**
- **Centralized Orchestration:** Single source of truth for all sub-projects
- **Automated Coordination:** Git submodules for seamless multi-repo management
- **Autonomous AI-First:** Designed for AI agents to coordinate development
- **Human-in-the-Loop:** Strategic guidance and approvals at phase gates

---

## Architecture

This master project uses **git submodules** to coordinate {len(self.sub_projects)} sub-projects:

"""

            # Add sub-projects table
            readme_content += "| Project | Description | Type | Priority | Timeline |\n"
            readme_content += "|---------|-------------|------|----------|----------|\n"

            for project in self.sub_projects:
                readme_content += f"| [{project['name']}](submodules/{project['name']}) | {project['description'][:60]}... | {project['type']} | {project['priority']} | {project['timeline']} |\n"

            readme_content += f"""

---

## Quick Start

### 1. Clone Master Repository with All Submodules

```bash
# Clone with all submodules
git clone --recurse-submodules https://github.com/{self.github_org}/{self.master_project_name}.git

# Or if already cloned, initialize submodules
git submodule update --init --recursive
```

### 2. Work on a Sub-Project

```bash
# Navigate to sub-project
cd submodules/coditect-cloud-backend

# Start CODITECT session
python3 ../../scripts/coditect-git-helper.py start-session "Implement user authentication"

# Make changes...

# Auto-commit and push
python3 ../../scripts/coditect-git-helper.py auto-commit "Add JWT authentication"
python3 ../../scripts/coditect-git-helper.py auto-push
```

### 3. Sync All Submodules

```bash
# Update all submodules to latest
git submodule update --remote --merge

# Commit submodule pointer updates in master
git add .
git commit -m "Update submodule pointers to latest"
git push
```

---

## Status

**Session Started:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Sub-Projects:** {len(self.sub_projects)}
**Timeline:** 10 months (Development → GTM)
**Budget:** $2.566M
**Status:** In Setup

---

*Built with Excellence by AZ1.AI CODITECT*
*Systematic Development. Continuous Context. Exceptional Results.*
"""

            readme_path = self.master_project_path / "README.md"
            readme_path.write_text(readme_content)
            self.print_status("Created comprehensive README.md", "SUCCESS")

            return True
        except (OSError, IOError) as e:
            raise DirectorySetupError(f"Failed to create README.md: {e}")

    def copy_master_documents(self) -> bool:
        """Copy master planning documents to master project."""
        self.print_status("Copying master planning documents...", "INFO")

        source_project = self.projects_root / "coditect-core"
        docs_to_copy = [
            "CODITECT-MASTER-ORCHESTRATION-PLAN.md",
            "CODITECT-ROLLOUT-MASTER-PLAN.md",
            "CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md"
        ]

        docs_dir = self.master_project_path / "docs"

        for doc in docs_to_copy:
            try:
                source_file = source_project / doc
                if source_file.exists():
                    shutil.copy(source_file, docs_dir / doc)
                    self.print_status(f"Copied: {doc}", "SUCCESS")
                else:
                    self.print_status(f"Not found: {doc}", "WARNING")
            except (OSError, IOError) as e:
                self.print_status(f"Failed to copy {doc}: {e}", "WARNING")

        return True

    def copy_automation_scripts(self) -> bool:
        """Copy automation scripts to master project."""
        self.print_status("Copying automation scripts...", "INFO")

        source_project = self.projects_root / "coditect-core"
        scripts_to_copy = [
            "scripts/coditect-git-helper.py",
            "scripts/coditect-setup.py",
            "scripts/coditect-bootstrap-projects.py"
        ]

        scripts_dir = self.master_project_path / "scripts"

        for script_path in scripts_to_copy:
            try:
                source_file = source_project / script_path
                if source_file.exists():
                    dest_file = scripts_dir / Path(script_path).name
                    shutil.copy(source_file, dest_file)
                    # Make executable
                    dest_file.chmod(0o755)
                    self.print_status(f"Copied and made executable: {Path(script_path).name}", "SUCCESS")
                else:
                    self.print_status(f"Not found: {script_path}", "WARNING")
            except (OSError, IOError) as e:
                self.print_status(f"Failed to copy {script_path}: {e}", "WARNING")

        return True

    def copy_templates(self) -> bool:
        """Copy templates to master project."""
        self.print_status("Copying templates...", "INFO")

        source_project = self.projects_root / "coditect-core"
        templates_dir = source_project / "templates"

        if templates_dir.exists():
            dest_templates = self.master_project_path / "templates"

            for template_file in templates_dir.glob("*"):
                if template_file.is_file():
                    try:
                        shutil.copy(template_file, dest_templates / template_file.name)
                        self.print_status(f"Copied template: {template_file.name}", "SUCCESS")
                    except (OSError, IOError) as e:
                        self.print_status(f"Failed to copy template {template_file.name}: {e}", "WARNING")

        return True

    def make_initial_commit(self) -> bool:
        """Make initial commit of master project before creating GitHub repo."""
        self.print_status("Making initial commit...", "INFO")

        os.chdir(self.master_project_path)

        try:
            # Add all files
            subprocess.run(["git", "add", "."], check=True, capture_output=True, timeout=10)

            # Create initial commit
            commit_msg = """Initial master project setup

Master orchestration repository for AZ1.AI CODITECT platform rollout.

Includes:
- Master planning documents
- Automation scripts
- Project templates
- Directory structure for submodules

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"""

            subprocess.run(["git", "commit", "-m", commit_msg],
                         check=True, capture_output=True, timeout=10)

            self.print_status("Initial commit created", "SUCCESS")
            return True
        except subprocess.CalledProcessError as e:
            raise GitOperationError(f"Initial commit failed: {e.stderr}")
        except subprocess.TimeoutExpired:
            raise GitOperationError("Initial commit timed out")

    def create_github_repository(self, dry_run: bool = False) -> bool:
        """Create GitHub repository for master project with retry logic."""
        self.print_status(f"Creating GitHub repository: {self.github_org}/{self.master_project_name}", "INFO")

        if dry_run:
            self.print_status("DRY RUN: Would create GitHub repository", "WARNING")
            return True

        try:
            # Create repository using gh CLI with retry
            cmd = [
                "gh", "repo", "create",
                f"{self.github_org}/{self.master_project_name}",
                "--private",
                "--description", "Master orchestration repository for AZ1.AI CODITECT platform rollout",
                "--source", str(self.master_project_path),
                "--remote", "origin",
                "--push"
            ]

            # GitHub API rate limiting consideration
            time.sleep(self.rate_limit_delay)

            result = self.run_command_with_retry(cmd)
            self.print_status(f"Created GitHub repository: {self.github_org}/{self.master_project_name}", "SUCCESS")

            return True
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr.lower():
                self.print_status("GitHub repository already exists", "WARNING")
                # Add remote if not already added
                try:
                    subprocess.run([
                        "git", "remote", "add", "origin",
                        f"https://github.com/{self.github_org}/{self.master_project_name}.git"
                    ], capture_output=True, check=True, timeout=10)
                except subprocess.CalledProcessError:
                    pass  # Remote already exists
                return True
            else:
                raise GitHubAPIError(f"GitHub repository creation failed: {e.stderr}")
        except NetworkError as e:
            raise GitHubAPIError(f"Network error creating GitHub repository: {e}")

    def create_sub_project(self, project: Dict[str, Any], dry_run: bool = False) -> bool:
        """
        Create individual sub-project repository and add as submodule.

        Args:
            project: Project definition dictionary
            dry_run: If True, don't actually create GitHub repos
        """
        project_name = project["name"]
        self.print_status(f"\n{'='*60}", "INFO")
        self.print_status(f"Setting up sub-project: {project_name}", "INFO")
        self.print_status(f"{'='*60}", "INFO")

        # Create local directory for sub-project
        submodules_dir = self.master_project_path / "submodules"
        submodules_dir.mkdir(exist_ok=True)

        project_path = submodules_dir / project_name

        if project_path.exists():
            self.print_status(f"Sub-project directory already exists: {project_name}", "WARNING")
            return True

        try:
            # Create project directory
            project_path.mkdir(parents=True, exist_ok=True)
            os.chdir(project_path)

            # Initialize git
            subprocess.run(["git", "init"], check=True, capture_output=True, timeout=10)
            subprocess.run(["git", "branch", "-M", "main"], check=True, capture_output=True, timeout=10)

            # Create .gitignore
            template_gitignore = self.master_project_path / "templates" / "gitignore-universal-template"
            if template_gitignore.exists():
                shutil.copy(template_gitignore, project_path / ".gitignore")

            # Create README.md
            readme_content = f"""# {project_name}

{project["description"]}

## Technology Stack

{chr(10).join(f"- {tech}" for tech in project["tech_stack"])}

## Project Details

- **Type:** {project["type"]}
- **Priority:** {project["priority"]}
- **Timeline:** {project["timeline"]}
- **Budget:** {project["budget"]}
- **Team Size:** {project["team_size"]} engineer(s)

## Quick Start

[TODO: Add setup instructions]

## Development

[TODO: Add development workflow]

## License

Copyright © 2025 AZ1.AI INC. All Rights Reserved.

---

*Part of AZ1.AI CODITECT Platform*
"""
            (project_path / "README.md").write_text(readme_content)

            # Create PROJECT-PLAN.md
            project_plan_content = f"""# {project_name} - Project Plan

## Overview

{project["description"]}

## Timeline

**Duration:** {project["timeline"]}
**Team Size:** {project["team_size"]} engineer(s)
**Budget:** {project["budget"]}

## Milestones

- [ ] Week 1: Project setup and architecture
- [ ] Week 2-4: Core implementation
- [ ] Week 5-6: Testing and refinement
- [ ] Final: Documentation and deployment

## Technology Decisions

### Tech Stack
{chr(10).join(f"- **{tech}**" for tech in project["tech_stack"])}

---

*Built with AZ1.AI CODITECT*
"""
            (project_path / "PROJECT-PLAN.md").write_text(project_plan_content)

            # Create TASKLIST.md
            tasklist_content = f"""# {project_name} - Task List

## Setup (Week 1)

- [ ] Initialize project structure
- [ ] Setup development environment
- [ ] Configure CI/CD pipeline
- [ ] Setup monitoring and logging

## Implementation (Weeks 2-4)

- [ ] Task 1: [TODO]
- [ ] Task 2: [TODO]
- [ ] Task 3: [TODO]

---

*Use `- [x]` to mark tasks as complete*
"""
            (project_path / "TASKLIST.md").write_text(tasklist_content)

            # Initial commit
            subprocess.run(["git", "add", "."], check=True, capture_output=True, timeout=10)
            commit_msg = f"""Initial commit for {project_name}

{project["description"]}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"""

            subprocess.run(["git", "commit", "-m", commit_msg],
                          check=True, capture_output=True, timeout=10)

            self.print_status(f"Initialized local repository for {project_name}", "SUCCESS")

            # Create GitHub repository
            if not dry_run:
                try:
                    privacy_flag = "--private" if project.get("private", True) else "--public"

                    # GitHub API rate limiting
                    time.sleep(self.rate_limit_delay)

                    cmd = [
                        "gh", "repo", "create",
                        f"{project['github_org']}/{project_name}",
                        privacy_flag,
                        "--description", project["description"],
                        "--source", str(project_path),
                        "--remote", "origin",
                        "--push"
                    ]

                    result = self.run_command_with_retry(cmd)
                    self.print_status(f"Created GitHub repository: {project['github_org']}/{project_name}", "SUCCESS")

                except subprocess.CalledProcessError as e:
                    if "already exists" in e.stderr.lower():
                        self.print_status(f"GitHub repository already exists: {project_name}", "WARNING")
                        # Add remote
                        try:
                            subprocess.run([
                                "git", "remote", "add", "origin",
                                f"https://github.com/{project['github_org']}/{project_name}.git"
                            ], capture_output=True, timeout=10)
                            subprocess.run(["git", "push", "-u", "origin", "main"],
                                         capture_output=True, check=True, timeout=30)
                        except subprocess.CalledProcessError:
                            pass
                    else:
                        raise GitHubAPIError(f"Failed to create GitHub repository: {e.stderr}")
            else:
                self.print_status(f"DRY RUN: Would create GitHub repo for {project_name}", "WARNING")

            # Add as submodule to master project
            os.chdir(self.master_project_path)

            try:
                submodule_url = f"https://github.com/{project['github_org']}/{project_name}.git"
                submodule_path = f"submodules/{project_name}"

                subprocess.run([
                    "git", "submodule", "add",
                    submodule_url,
                    submodule_path
                ], check=True, capture_output=True, timeout=30)

                self.print_status(f"Added {project_name} as submodule", "SUCCESS")
            except subprocess.CalledProcessError as e:
                self.print_status(f"Failed to add submodule: {e.stderr}", "WARNING")

            return True
        except Exception as e:
            self.print_status(f"Error creating sub-project {project_name}: {e}", "ERROR")
            return False

    def create_all_sub_projects(self, dry_run: bool = False) -> bool:
        """Create all sub-projects and add as submodules."""
        self.print_status(f"\nCreating {len(self.sub_projects)} sub-projects...\n", "INFO")

        success_count = 0
        for i, project in enumerate(self.sub_projects, 1):
            self.print_status(f"\nProgress: {i}/{len(self.sub_projects)}", "INFO")

            if self.create_sub_project(project, dry_run=dry_run):
                success_count += 1
                # Rate limiting between projects
                time.sleep(self.rate_limit_delay)
            else:
                self.print_status(f"Failed to create {project['name']}", "ERROR")

        self.print_status(f"\nCreated {success_count}/{len(self.sub_projects)} sub-projects",
                         "SUCCESS" if success_count == len(self.sub_projects) else "WARNING")

        return success_count == len(self.sub_projects)

    def create_submodule_sync_script(self) -> bool:
        """Create script to sync all submodules."""
        self.print_status("Creating submodule sync script...", "INFO")

        sync_script = """#!/bin/bash
# Sync all submodules to latest from their respective main branches

set -e

echo "🔄 Syncing all CODITECT submodules..."

# Update all submodules to latest
git submodule update --remote --merge

# Show status
echo ""
echo "📊 Submodule status:"
git submodule status

echo ""
echo "✅ Submodules synced successfully!"
echo ""
echo "To commit the updates to the master project:"
echo "  git add ."
echo "  git commit -m 'Update submodule pointers to latest'"
echo "  git push"
"""

        try:
            sync_script_path = self.master_project_path / "scripts" / "sync-all-submodules.sh"
            sync_script_path.write_text(sync_script)
            sync_script_path.chmod(0o755)

            self.print_status("Created sync-all-submodules.sh", "SUCCESS")
            return True
        except (OSError, IOError) as e:
            self.print_status(f"Failed to create sync script: {e}", "WARNING")
            return False

    def create_status_report_script(self) -> bool:
        """Create script to generate status report across all submodules."""
        self.print_status("Creating status report script...", "INFO")

        status_script = """#!/usr/bin/env python3
\"\"\"
Generate status report across all CODITECT sub-projects.
\"\"\"

import subprocess
import os
from pathlib import Path
from datetime import datetime

def get_submodule_status(submodule_path):
    \"\"\"Get git status for a submodule.\"\"\"
    try:
        os.chdir(submodule_path)

        # Get current branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()

        # Get latest commit
        commit = subprocess.check_output(
            ["git", "log", "-1", "--format=%h - %s"],
            text=True
        ).strip()

        # Get uncommitted changes
        status = subprocess.check_output(
            ["git", "status", "--short"],
            text=True
        ).strip()

        uncommitted = len(status.split("\\n")) if status else 0

        return {
            "branch": branch,
            "commit": commit,
            "uncommitted": uncommitted,
            "status": "✓" if uncommitted == 0 else "⚠"
        }
    except Exception as e:
        return {
            "branch": "ERROR",
            "commit": str(e),
            "uncommitted": 0,
            "status": "✗"
        }

def main():
    master_root = Path(__file__).parent.parent
    submodules_dir = master_root / "submodules"

    print(f"\\n{'='*80}")
    print(f"  CODITECT Platform - Status Report")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\\n")

    if not submodules_dir.exists():
        print("❌ No submodules directory found")
        return

    submodules = [d for d in submodules_dir.iterdir() if d.is_dir() and (d / ".git").exists()]

    print(f"Total Sub-Projects: {len(submodules)}\\n")
    print(f"{'Project':<35} {'Branch':<15} {'Status':<8} {'Uncommitted'}")
    print(f"{'-'*80}")

    for submodule in sorted(submodules):
        status = get_submodule_status(submodule)
        uncommitted_str = f"{status['uncommitted']} files" if status['uncommitted'] > 0 else "Clean"
        print(f"{submodule.name:<35} {status['branch']:<15} {status['status']:<8} {uncommitted_str}")

    print(f"\\n{'='*80}\\n")

if __name__ == "__main__":
    main()
"""

        try:
            status_script_path = self.master_project_path / "scripts" / "status-report.py"
            status_script_path.write_text(status_script)
            status_script_path.chmod(0o755)

            self.print_status("Created status-report.py", "SUCCESS")
            return True
        except (OSError, IOError) as e:
            self.print_status(f"Failed to create status report script: {e}", "WARNING")
            return False

    def final_commit_and_push(self, dry_run: bool = False) -> bool:
        """Make final commit of master project and push."""
        self.print_status("Making final commit of master project...", "INFO")

        os.chdir(self.master_project_path)

        try:
            # Add all files
            subprocess.run(["git", "add", "."], check=True, capture_output=True, timeout=10)

            # Commit
            commit_msg = """Initial master project setup with all sub-projects

This master orchestration repository coordinates the complete AZ1.AI CODITECT
platform rollout from beta through pilot to GTM.

Sub-projects created:
""" + "\n".join(f"- {p['name']}: {p['description']}" for p in self.sub_projects) + """

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"""

            subprocess.run(["git", "commit", "-m", commit_msg],
                         check=True, capture_output=True, timeout=10)

            self.print_status("Committed master project", "SUCCESS")

            if not dry_run:
                # Push to GitHub with retry
                self.run_command_with_retry(
                    ["git", "push", "-u", "origin", "main"],
                    cwd=self.master_project_path
                )
                self.print_status("Pushed to GitHub", "SUCCESS")
            else:
                self.print_status("DRY RUN: Would push to GitHub", "WARNING")

            return True
        except subprocess.CalledProcessError as e:
            raise GitOperationError(f"Commit/push failed: {e.stderr}")
        except NetworkError as e:
            raise GitOperationError(f"Push failed due to network error: {e}")

    def save_session_log(self):
        """Save session log to MEMORY-CONTEXT."""
        try:
            log_file = self.master_project_path / "MEMORY-CONTEXT" / f"SESSION-{self.session_id}.json"

            log_data = {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "master_project": self.master_project_name,
                "sub_projects_created": len(self.sub_projects),
                "log": self.session_log
            }

            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)

            self.print_status(f"Session log saved: {log_file.name}", "SUCCESS")
        except (OSError, IOError) as e:
            self.print_status(f"Failed to save session log: {e}", "WARNING")

    def rollback(self):
        """Rollback changes in case of failure."""
        self.print_status("Rolling back changes...", "WARNING")

        for action_type, target in reversed(self.rollback_actions):
            try:
                if action_type == "rmdir":
                    if target.exists():
                        shutil.rmtree(target)
                        self.print_status(f"Removed directory: {target}", "SUCCESS")
                elif action_type == "git_deinit":
                    git_dir = target / ".git"
                    if git_dir.exists():
                        shutil.rmtree(git_dir)
                        self.print_status(f"Removed git repository: {target}", "SUCCESS")
            except Exception as e:
                self.print_status(f"Rollback failed for {target}: {e}", "ERROR")

    def print_summary(self):
        """Print summary of what was created."""
        print(f"\n{self.GREEN}{'='*80}")
        print(f"  ✅ CODITECT Master Project Setup Complete!")
        print(f"{'='*80}{self.RESET}\n")

        print(f"{self.BLUE}📁 Master Project:{self.RESET}")
        print(f"   Location: {self.master_project_path}")
        print(f"   GitHub: https://github.com/{self.github_org}/{self.master_project_name}")

        print(f"\n{self.BLUE}📦 Sub-Projects Created: {len(self.sub_projects)}{self.RESET}")
        for project in self.sub_projects:
            print(f"   • {project['name']} ({project['priority']}) - {project['timeline']}")

        print(f"\n{self.BLUE}🚀 Next Steps:{self.RESET}")
        print(f"   1. Review master project README: {self.master_project_path / 'README.md'}")
        print(f"   2. Review planning docs in: {self.master_project_path / 'docs/'}")
        print(f"   3. Start development on priority P0 projects")
        print(f"   4. Use scripts/status-report.py to track progress")

        print(f"\n{self.GREEN}{'='*80}{self.RESET}\n")

    def run(self, dry_run: bool = False):
        """Run complete master project setup."""
        self.print_banner()

        steps = [
            ("Checking prerequisites", self.check_prerequisites),
            ("Creating master project directory", self.create_master_project_directory),
            ("Initializing git repository", self.initialize_git_repository),
            ("Creating master README", self.create_master_readme),
            ("Copying master documents", self.copy_master_documents),
            ("Copying automation scripts", self.copy_automation_scripts),
            ("Copying templates", self.copy_templates),
            ("Making initial commit", self.make_initial_commit),
            ("Creating GitHub repository", lambda: self.create_github_repository(dry_run)),
            ("Creating all sub-projects", lambda: self.create_all_sub_projects(dry_run)),
            ("Creating sync script", self.create_submodule_sync_script),
            ("Creating status report script", self.create_status_report_script),
            ("Final commit and push", lambda: self.final_commit_and_push(dry_run)),
            ("Saving session log", self.save_session_log)
        ]

        try:
            for step_name, step_func in steps:
                self.print_status(f"\n{'─'*60}", "INFO")
                self.print_status(f"Step: {step_name}", "INFO")
                self.print_status(f"{'─'*60}", "INFO")

                if not step_func():
                    self.print_status(f"Step failed: {step_name}", "ERROR")
                    self.rollback()
                    return False

            self.print_summary()
            return True
        except Exception as e:
            self.print_status(f"Unexpected error: {e}", "ERROR")
            self.logger.exception("Full exception traceback:")
            self.rollback()
            return False
        finally:
            # Ensure cleanup
            pass


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="AZ1.AI CODITECT Master Project Setup - Autonomous AI-First Orchestration"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (don't create GitHub repositories)"
    )
    parser.add_argument(
        "--master-name",
        default="coditect-rollout-master",
        help="Name of master orchestration project (default: coditect-rollout-master)"
    )
    parser.add_argument(
        "--projects-root",
        default=None,
        help="Root directory for projects (default: ~/PROJECTS)"
    )

    args = parser.parse_args()

    try:
        setup = CoditectMasterProjectSetup(
            master_project_name=args.master_name,
            projects_root=args.projects_root
        )

        success = setup.run(dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
