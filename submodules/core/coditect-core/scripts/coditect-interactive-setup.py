#!/usr/bin/env python3
"""
CODITECT Interactive Project Setup

Interactive Python script to set up a new CODITECT project with:
- Custom project directory selection
- Automated .coditect framework installation
- MEMORY-CONTEXT structure creation
- Sample project initialization
- Initial documentation generation

Usage:
    python3 coditect-interactive-setup.py

Or make executable:
    chmod +x coditect-interactive-setup.py
    ./coditect-interactive-setup.py
"""

import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('coditect-interactive-setup.log')
    ]
)
logger = logging.getLogger(__name__)


# Custom Exceptions
class CoditectSetupError(Exception):
    """Base exception for CODITECT setup errors"""
    pass


class PrerequisiteError(CoditectSetupError):
    """Raised when required tools are missing"""
    pass


class DirectoryCreationError(CoditectSetupError):
    """Raised when directory creation fails"""
    pass


class GitOperationError(CoditectSetupError):
    """Raised when git operations fail"""
    pass


class FrameworkInstallError(CoditectSetupError):
    """Raised when framework installation fails"""
    pass


class DocumentationError(CoditectSetupError):
    """Raised when documentation creation fails"""
    pass


# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(message):
    """Print a formatted header message."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def print_success(message):
    """Print a success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    """Print an error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message):
    """Print an info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    try:
        logger.debug(f"Running command: {cmd} (cwd={cwd})")
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        logger.debug(f"Command completed: returncode={result.returncode}")
        return result
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command timed out after 5 minutes: {cmd}")
        print_error(f"Command timed out: {cmd}")
        if check:
            raise GitOperationError(f"Command timed out: {cmd}")
        return None
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd} - {e.stderr}")
        print_error(f"Command failed: {cmd}")
        print_error(f"Error: {e.stderr}")
        if check:
            raise GitOperationError(f"Command failed: {cmd}\n{e.stderr}")
        return e
    except Exception as e:
        logger.error(f"Unexpected error running command '{cmd}': {str(e)}")
        print_error(f"Unexpected error: {str(e)}")
        if check:
            raise GitOperationError(f"Unexpected error running command: {str(e)}")
        return None


def check_prerequisites():
    """Check if required tools are installed."""
    print_header("Checking Prerequisites")

    all_good = True

    # Check Python version
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 6:
        print_success(f"Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        print_error(f"Python 3.6+ required (you have {py_version.major}.{py_version.minor})")
        all_good = False

    # Check git
    result = run_command("git --version", check=False)
    if result.returncode == 0:
        version = result.stdout.strip()
        print_success(f"Git installed: {version}")
    else:
        print_error("Git not installed - please install git first")
        all_good = False

    # Check Claude Code (optional but recommended)
    result = run_command("claude --version", check=False)
    if result.returncode == 0:
        version = result.stdout.strip()
        print_success(f"Claude Code installed: {version}")
    else:
        print_warning("Claude Code not found - install from https://claude.com/code")
        print_info("You can continue setup and install Claude Code later")

    if not all_good:
        print_error("\nMissing prerequisites. Please install required tools and try again.")
        sys.exit(1)

    print_success("\nAll prerequisites met!")
    return True


def get_project_directory():
    """Interactive prompt for project directory path."""
    print_header("Project Directory Setup")

    print(f"{Colors.BOLD}Enter the full path to your new PROJECTS folder.{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Examples:{Colors.ENDC}")
    print(f"  • ~/PROJECTS/my-saas-project")
    print(f"  • /Users/yourusername/PROJECTS/design-agency-app")
    print(f"  • /home/user/development/ecommerce-platform")
    print()

    while True:
        project_path = input(f"{Colors.BOLD}Project path:{Colors.ENDC} ").strip()

        if not project_path:
            print_error("Path cannot be empty. Please try again.")
            continue

        # Expand user home directory
        project_path = os.path.expanduser(project_path)
        project_path = os.path.abspath(project_path)

        # Check if path already exists
        if os.path.exists(project_path):
            print_warning(f"Directory already exists: {project_path}")
            response = input(f"{Colors.WARNING}Continue anyway? (y/n):{Colors.ENDC} ").strip().lower()
            if response != 'y':
                continue

        # Confirm path
        print()
        print(f"{Colors.BOLD}You entered:{Colors.ENDC} {project_path}")
        confirm = input(f"{Colors.BOLD}Is this correct? (y/n):{Colors.ENDC} ").strip().lower()

        if confirm == 'y':
            return Path(project_path)
        else:
            print_info("Let's try again...")


def get_project_info():
    """Interactive prompt for project information."""
    print_header("Project Information")

    print(f"{Colors.BOLD}Let's collect some basic information about your project.{Colors.ENDC}")
    print()

    # Project name
    project_name = input(f"{Colors.BOLD}Project name:{Colors.ENDC} ").strip()
    if not project_name:
        project_name = "My CODITECT Project"

    # Project description
    print()
    print(f"{Colors.BOLD}Project description (1-2 sentences):{Colors.ENDC}")
    project_description = input("> ").strip()
    if not project_description:
        project_description = "A software project specified using CODITECT multi-agent framework."

    # Target customer (optional)
    print()
    target_customer = input(f"{Colors.BOLD}Target customer (optional):{Colors.ENDC} ").strip()

    # Project type (optional)
    print()
    print(f"{Colors.BOLD}Project type (optional):{Colors.ENDC}")
    print("  1. SaaS Application")
    print("  2. Mobile App")
    print("  3. Enterprise Software")
    print("  4. Developer Tool")
    print("  5. E-commerce Platform")
    print("  6. Other")
    project_type_choice = input("> ").strip()

    project_type_map = {
        "1": "SaaS Application",
        "2": "Mobile App",
        "3": "Enterprise Software",
        "4": "Developer Tool",
        "5": "E-commerce Platform",
        "6": "Other"
    }
    project_type = project_type_map.get(project_type_choice, "Software Project")

    return {
        "name": project_name,
        "description": project_description,
        "target_customer": target_customer,
        "project_type": project_type
    }


def create_directory_structure(project_path):
    """Create the project directory structure."""
    print_header("Creating Directory Structure")

    # Create main project directory
    project_path.mkdir(parents=True, exist_ok=True)
    print_success(f"Created: {project_path}")

    # Create MEMORY-CONTEXT subdirectories
    memory_context = project_path / "MEMORY-CONTEXT"
    subdirs = ["sessions", "decisions", "business", "technical"]

    for subdir in subdirs:
        path = memory_context / subdir
        path.mkdir(parents=True, exist_ok=True)

        # Create README in each subdirectory
        readme_content = {
            "sessions": "# Session Summaries\n\nExport session summaries here to maintain context across sessions.\n",
            "decisions": "# Architecture Decision Records\n\nStore ADRs (Architecture Decision Records) here.\n",
            "business": "# Business Research Notes\n\nStore market research, customer insights, and business strategy notes here.\n",
            "technical": "# Technical Research Notes\n\nStore code patterns, implementation notes, and technical research here.\n"
        }

        readme_file = path / "README.md"
        readme_file.write_text(readme_content[subdir])
        print_success(f"Created: {path}")

    # Create docs structure
    docs = project_path / "docs"
    doc_subdirs = ["research", "business", "architecture", "decisions"]

    for subdir in doc_subdirs:
        path = docs / subdir
        path.mkdir(parents=True, exist_ok=True)
        print_success(f"Created: {path}")

    # Create MEMORY-CONTEXT/checkpoints directory
    checkpoints = project_path / "MEMORY-CONTEXT" / "checkpoints"
    checkpoints.mkdir(parents=True, exist_ok=True)
    print_success(f"Created: {checkpoints}")

    return True


def install_coditect_framework(project_path):
    """Install .coditect framework as git submodule."""
    print_header("Installing CODITECT Framework")

    # Initialize git repository
    print_info("Initializing git repository...")
    result = run_command("git init", cwd=project_path, check=False)
    if result.returncode == 0:
        print_success("Git repository initialized")
    else:
        print_warning("Git repository may already exist")

    # Check if .coditect already exists
    coditect_path = project_path / ".coditect"
    if coditect_path.exists():
        print_warning(".coditect directory already exists")
        response = input(f"{Colors.WARNING}Remove and reinstall? (y/n):{Colors.ENDC} ").strip().lower()
        if response == 'y':
            shutil.rmtree(coditect_path)
        else:
            print_info("Keeping existing .coditect directory")
            return True

    # Add .coditect as git submodule
    print_info("Cloning CODITECT framework...")
    submodule_url = "https://github.com/coditect-ai/coditect-core.git"

    result = run_command(
        f'git submodule add {submodule_url} .coditect',
        cwd=project_path,
        check=False
    )

    if result.returncode == 0:
        print_success("CODITECT framework installed as .coditect/")
    else:
        # Try direct clone if submodule fails
        print_warning("Submodule add failed, trying direct clone...")
        result = run_command(
            f'git clone {submodule_url} .coditect',
            cwd=project_path,
            check=False
        )
        if result.returncode == 0:
            print_success("CODITECT framework cloned to .coditect/")
        else:
            print_error("Failed to install CODITECT framework")
            print_info(f"You can manually clone: git clone {submodule_url} .coditect")
            return False

    # Create .claude symlink
    print_info("Creating .claude symlink...")
    claude_link = project_path / ".claude"
    if claude_link.exists():
        claude_link.unlink()

    os.symlink(".coditect", str(claude_link))
    print_success("Created .claude -> .coditect symlink")

    # Initialize submodules recursively
    print_info("Initializing submodules...")
    run_command("git submodule update --init --recursive", cwd=project_path, check=False)

    # Verify installation
    agents_dir = project_path / ".coditect" / "agents"
    if agents_dir.exists():
        agent_count = len(list(agents_dir.glob("*.md")))
        print_success(f"Verified: {agent_count} agents available")

    return True


def create_initial_documentation(project_path, project_info):
    """Create initial project documentation."""
    print_header("Creating Initial Documentation")

    # Create README.md
    readme_content = f"""# {project_info['name']}

> {project_info['description']}

## Project Overview

- **Type:** {project_info['project_type']}
- **Target Customer:** {project_info.get('target_customer', 'TBD')}
- **Status:** Specification Phase
- **Created:** {datetime.now().strftime('%Y-%m-%d')}

## Project Structure

```
{project_path.name}/
├── .coditect/              # CODITECT framework (submodule)
├── .claude -> .coditect    # Symlink for Claude Code
├── MEMORY-CONTEXT/         # Session persistence
│   ├── sessions/           # Session summaries
│   ├── decisions/          # ADRs
│   ├── business/           # Business research
│   └── technical/          # Technical research
├── docs/                   # Project documentation
│   ├── research/           # Market research
│   ├── business/           # Business documents
│   ├── architecture/       # Technical specs
│   └── decisions/          # ADRs
├── MEMORY-CONTEXT/         # Session continuity system
│   ├── checkpoints/        # Project checkpoints
│   ├── sessions/           # Session summaries
│   ├── exports/            # Raw exports
│   └── archive/            # Historical data
├── PROJECT-PLAN.md         # Project plan
├── TASKLIST.md             # Task tracking
├── README.md               # This file
└── CLAUDE.md               # Claude context
```

## Getting Started

### Prerequisites

- Claude Code installed
- Git configured
- CODITECT operator training completed

### Next Steps

1. **Business Discovery** (2-4 hours)
   - Market research
   - Value proposition
   - Ideal customer profile
   - Product-market fit analysis
   - Competitive analysis
   - Go-to-market strategy
   - Pricing strategy

2. **Technical Specification** (4-6 hours)
   - System architecture (C4 diagrams)
   - Database schema
   - API specification
   - Architecture decision records
   - Software design document

3. **Project Planning** (2-3 hours)
   - Generate PROJECT-PLAN.md
   - Create TASKLIST.md with all tasks
   - Define phases and milestones

4. **Development** (varies)
   - Follow TASKLIST
   - Create checkpoints
   - Maintain documentation

## CODITECT Training

If you haven't completed CODITECT training yet:

1. **Quick Start (30 min):** `.coditect/user-training/1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md`
2. **Full Training (4-6 hrs):** `.coditect/user-training/CODITECT-OPERATOR-TRAINING-SYSTEM.md`
3. **Certification:** `.coditect/user-training/CODITECT-OPERATOR-ASSESSMENTS.md`

## Resources

- **Training:** `.coditect/user-training/`
- **Agents:** `.coditect/agents/`
- **Commands:** `.coditect/commands/`
- **Skills:** `.coditect/skills/`

## Session Management

**Before ending each session:**

```
"Create a session summary including work completed, decisions made, and next steps.
Export to: MEMORY-CONTEXT/sessions/YYYY-MM-DD-session-summary.md"
```

**Starting a new session:**

```
"Read MEMORY-CONTEXT/sessions/[latest].md, PROJECT-PLAN.md, and TASKLIST.md
to load project context."
```

## Project Status

- [ ] Business discovery complete
- [ ] Technical specification complete
- [ ] Project plan created
- [ ] Development started
- [ ] Testing & QA
- [ ] Production deployment

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**CODITECT Version:** 1.0
"""

    readme_file = project_path / "README.md"
    readme_file.write_text(readme_content)
    print_success("Created: README.md")

    # Create CLAUDE.md
    claude_content = f"""# Claude Context: {project_info['name']}

> **Project context for Claude Code sessions**
> **Keep this updated as the project evolves**

## Project Overview

{project_info['description']}

## Project Vision

[Describe the long-term vision for this project]

## Target Customer

{project_info.get('target_customer', 'TBD - Define during business discovery')}

## Key Features (Planned)

1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

## Current Phase

**Status:** Specification - Business Discovery

**Next Steps:**
1. Complete market research
2. Define value proposition
3. Create ideal customer profile

## Important Context

### Business Context
- **Market:** [Market segment]
- **Competition:** [Key competitors]
- **Differentiation:** [What makes this unique]

### Technical Context
- **Architecture:** [TBD - Will define during technical specification]
- **Tech Stack:** [TBD - Will define during technical specification]
- **Deployment:** [TBD - Will define during technical specification]

## Key Decisions

(Will be documented as ADRs in docs/decisions/ and MEMORY-CONTEXT/decisions/)

### ADR-001: [Decision Title]
- **Status:** [Proposed/Accepted]
- **Decision:** [What was decided]
- **Rationale:** [Why this was decided]

## Project Constraints

- **Budget:** [If applicable]
- **Timeline:** [If applicable]
- **Technical:** [Any technical constraints]
- **Business:** [Any business constraints]

## Success Criteria

**Business Success:**
1. [Criterion 1]
2. [Criterion 2]

**Technical Success:**
1. [Criterion 1]
2. [Criterion 2]

## Resources & References

- **Market Research:** docs/research/
- **Business Documents:** docs/business/
- **Technical Specs:** docs/architecture/
- **Session History:** MEMORY-CONTEXT/sessions/

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Project Started:** {datetime.now().strftime('%Y-%m-%d')}
"""

    claude_file = project_path / "CLAUDE.md"
    claude_file.write_text(claude_content)
    print_success("Created: CLAUDE.md")

    # Create PROJECT-PLAN.md (template)
    project_plan_content = f"""# Project Plan: {project_info['name']}

> **Comprehensive project planning document**
> **Living document - update throughout project lifecycle**

## Executive Summary

**Project:** {project_info['name']}
**Type:** {project_info['project_type']}
**Status:** Specification Phase
**Started:** {datetime.now().strftime('%Y-%m-%d')}

{project_info['description']}

## Objectives & Success Criteria

### Business Objectives

1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

### Technical Objectives

1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

### Success Criteria

**Must Have:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Should Have:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Nice to Have:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Technical Architecture

(To be completed during technical specification phase)

### Technology Stack

**Frontend:**
- TBD

**Backend:**
- TBD

**Database:**
- TBD

**Infrastructure:**
- TBD

## Development Phases

### Phase 1: Business Discovery (Weeks 1-2)

**Objectives:**
- Complete market research
- Define value proposition and ICP
- Analyze product-market fit
- Develop go-to-market strategy

**Deliverables:**
- Market research document
- Value proposition
- Ideal customer profile
- Product-market fit analysis
- Competitive analysis
- Go-to-market strategy
- Pricing strategy

### Phase 2: Technical Specification (Weeks 3-4)

**Objectives:**
- Design system architecture
- Define database schema
- Specify APIs
- Document key decisions

**Deliverables:**
- System architecture (C4 diagrams)
- Database schema (ERD)
- API specification (OpenAPI 3.1)
- Architecture Decision Records
- Software Design Document
- Test Design Document

### Phase 3: Development (Weeks 5-12)

**Objectives:**
- Implement core features
- Write tests
- Integrate components

**Deliverables:**
- Working application
- Test suite
- Documentation

### Phase 4: Testing & Launch (Weeks 13-14)

**Objectives:**
- QA testing
- Bug fixes
- Production deployment

**Deliverables:**
- Tested application
- Deployment documentation
- User documentation

## Timeline & Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Business Discovery Complete | Week 2 | Pending |
| Technical Specification Complete | Week 4 | Pending |
| MVP Development Complete | Week 10 | Pending |
| Testing Complete | Week 13 | Pending |
| Production Launch | Week 14 | Pending |

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | Medium | High | [Mitigation strategy] |

### Business Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | Low | Medium | [Mitigation strategy] |

## Resource Requirements

### Team
- [Role 1]: [Availability]
- [Role 2]: [Availability]

### Tools & Services
- [Tool 1]: [Cost]
- [Service 1]: [Cost]

### Budget
- Total Estimated Budget: [Amount]
- Breakdown: [Details]

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Next Review:** [Date]
"""

    project_plan_file = project_path / "PROJECT-PLAN.md"
    project_plan_file.write_text(project_plan_content)
    print_success("Created: PROJECT-PLAN.md")

    # Create TASKLIST.md
    tasklist_content = f"""# Task List: {project_info['name']}

> **Granular task tracking with checkboxes**
> **Update daily as you complete tasks**

## Format

`- [ ] **[Phase X]** Task description - Priority: HIGH/MEDIUM/LOW - Est: Xh - Agent: agent-name`

---

## Phase 1: Business Discovery

### Market Research

- [ ] **[Phase 1]** Conduct market research using competitive-market-analyst - `Priority: HIGH` - `Est: 2h` - `Agent: competitive-market-analyst`
  - TAM/SAM/SOM calculations
  - Competitor analysis (5-7 companies)
  - Market trends
  - Customer pain points

- [ ] **[Phase 1]** Review and refine market research document - `Priority: HIGH` - `Est: 1h`

### Value Proposition & ICP

- [ ] **[Phase 1]** Create value proposition using business-intelligence-analyst - `Priority: HIGH` - `Est: 1h` - `Agent: business-intelligence-analyst`

- [ ] **[Phase 1]** Define ideal customer profile - `Priority: HIGH` - `Est: 1h` - `Agent: business-intelligence-analyst`
  - Demographics
  - Psychographics
  - Behavioral characteristics

### Product-Market Fit

- [ ] **[Phase 1]** Analyze product-market fit using 7-Fit framework - `Priority: HIGH` - `Est: 2h` - `Agent: business-intelligence-analyst`

- [ ] **[Phase 1]** Validate market assumptions - `Priority: MEDIUM` - `Est: 1h`

### Competitive Analysis

- [ ] **[Phase 1]** Research 5-7 key competitors - `Priority: HIGH` - `Est: 2h` - `Agent: competitive-market-analyst`

- [ ] **[Phase 1]** Create competitive matrix - `Priority: MEDIUM` - `Est: 1h`

### Go-to-Market & Pricing

- [ ] **[Phase 1]** Develop go-to-market strategy - `Priority: HIGH` - `Est: 1.5h` - `Agent: business-intelligence-analyst`

- [ ] **[Phase 1]** Define pricing strategy - `Priority: HIGH` - `Est: 1.5h` - `Agent: business-intelligence-analyst`

### Business Discovery Checkpoint

- [ ] **[Phase 1]** Review all business documents - `Priority: HIGH` - `Est: 1h`

- [ ] **[Phase 1]** Create Phase 1 checkpoint - `Priority: HIGH` - `Est: 0.5h`

- [ ] **[Phase 1]** Commit business discovery work to git - `Priority: HIGH` - `Est: 0.5h`

---

## Phase 2: Technical Specification

### System Architecture

- [ ] **[Phase 2]** Design system architecture using senior-architect - `Priority: HIGH` - `Est: 3h` - `Agent: senior-architect`
  - C4 Context diagram
  - C4 Container diagram
  - C4 Component diagram
  - Technology stack recommendations

- [ ] **[Phase 2]** Review and refine architecture - `Priority: HIGH` - `Est: 1h`

### Database Design

- [ ] **[Phase 2]** Design database schema - `Priority: HIGH` - `Est: 2h` - `Agent: senior-architect`
  - Entity Relationship Diagram
  - Table definitions
  - Relationships and constraints

- [ ] **[Phase 2]** Validate schema design - `Priority: MEDIUM` - `Est: 1h`

### API Specification

- [ ] **[Phase 2]** Create API specification - `Priority: HIGH` - `Est: 3h` - `Agent: software-design-architect`
  - OpenAPI 3.1 spec
  - All endpoints documented
  - Authentication approach

### Architecture Decision Records

- [ ] **[Phase 2]** Create ADR-001: Database choice - `Priority: HIGH` - `Est: 0.5h`

- [ ] **[Phase 2]** Create ADR-002: Authentication method - `Priority: HIGH` - `Est: 0.5h`

- [ ] **[Phase 2]** Create ADR-003: Deployment strategy - `Priority: HIGH` - `Est: 0.5h`

### Design Documents

- [ ] **[Phase 2]** Write Software Design Document - `Priority: HIGH` - `Est: 2h` - `Agent: software-design-architect`

- [ ] **[Phase 2]** Write Test Design Document - `Priority: MEDIUM` - `Est: 1.5h` - `Agent: testing-specialist`

### Technical Specification Checkpoint

- [ ] **[Phase 2]** Review all technical documents - `Priority: HIGH` - `Est: 1h`

- [ ] **[Phase 2]** Create Phase 2 checkpoint - `Priority: HIGH` - `Est: 0.5h`

- [ ] **[Phase 2]** Commit technical specification to git - `Priority: HIGH` - `Est: 0.5h`

---

## Phase 3: Development

(Tasks will be added during technical specification phase)

---

## Phase 4: Testing & Launch

(Tasks will be added during development phase)

---

## Notes

- **Priority Levels:**
  - `HIGH`: Critical path, must be done
  - `MEDIUM`: Important but not blocking
  - `LOW`: Nice to have, if time permits

- **Time Estimates:**
  - Be realistic
  - Include time for review and refinement
  - Add 20-30% buffer for unknowns

- **Agent Assignment:**
  - Specify which CODITECT agent to use
  - Helps with planning and execution

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Total Tasks:** (Count as you add)
**Completed:** 0
**In Progress:** 0
**Pending:** (Initial count)
"""

    tasklist_file = project_path / "TASKLIST.md"
    tasklist_file.write_text(tasklist_content)
    print_success("Created: TASKLIST.md")

    return True


def create_gitignore(project_path):
    """Create a sensible .gitignore file."""
    gitignore_content = """# Operating System
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
*.egg-info/

# Environment variables
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp

# Database
*.db
*.sqlite
*.sqlite3

# Secrets (never commit these!)
secrets/
credentials/
*.key
*.pem
*.cert

# Large files
*.zip
*.tar.gz
*.rar
```

    gitignore_file = project_path / ".gitignore"
    gitignore_file.write_text(gitignore_content)
    print_success("Created: .gitignore")
    return True


def initial_git_commit(project_path, project_info):
    """Create initial git commit."""
    print_header("Creating Initial Git Commit")

    # Configure git if needed
    result = run_command("git config user.name", cwd=project_path, check=False)
    if not result.stdout.strip():
        print_info("Git user not configured. Let's set it up...")
        user_name = input(f"{Colors.BOLD}Your name:{Colors.ENDC} ").strip()
        user_email = input(f"{Colors.BOLD}Your email:{Colors.ENDC} ").strip()

        run_command(f'git config user.name "{user_name}"', cwd=project_path)
        run_command(f'git config user.email "{user_email}"', cwd=project_path)
        print_success("Git user configured")

    # Stage all files
    print_info("Staging files...")
    run_command("git add .", cwd=project_path)

    # Create commit
    commit_message = f"""Initial CODITECT project setup: {project_info['name']}

- Initialized project structure
- Installed CODITECT framework as .coditect/
- Created MEMORY-CONTEXT system
- Generated initial documentation (README, CLAUDE.md, PROJECT-PLAN, TASKLIST)
- Set up directory structure for business and technical specs

Project Type: {project_info['project_type']}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🤖 Generated with CODITECT Interactive Setup
"""

    print_info("Creating commit...")
    run_command(f'git commit -m "{commit_message}"', cwd=project_path)
    print_success("Initial commit created")

    return True


def print_next_steps(project_path, project_info):
    """Print next steps for the user."""
    print_header("Setup Complete! 🎉")

    print(f"{Colors.OKGREEN}{Colors.BOLD}Your CODITECT project is ready!{Colors.ENDC}\n")

    print(f"{Colors.BOLD}Project Location:{Colors.ENDC}")
    print(f"  {project_path}\n")

    print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}\n")

    print(f"{Colors.OKCYAN}1. Navigate to your project:{Colors.ENDC}")
    print(f"   cd {project_path}\n")

    print(f"{Colors.OKCYAN}2. Start Claude Code:{Colors.ENDC}")
    print(f"   claude\n")

    print(f"{Colors.OKCYAN}3. Load project context:{Colors.ENDC}")
    print(f'   "Read README.md and CLAUDE.md to understand the project context."\n')

    print(f"{Colors.OKCYAN}4. Start business discovery:{Colors.ENDC}")
    print(f'''   "Let's start business discovery for {project_info['name']}.
   Use the competitive-market-analyst agent to research the market."
''')

    print(f"\n{Colors.BOLD}Training Resources:{Colors.ENDC}\n")
    print(f"  • Quick Start (30 min): .coditect/user-training/1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md")
    print(f"  • Full Training (4-6 hrs): .coditect/user-training/CODITECT-OPERATOR-TRAINING-SYSTEM.md")
    print(f"  • FAQ: .coditect/user-training/CODITECT-OPERATOR-FAQ.md")
    print(f"  • Troubleshooting: .coditect/user-training/CODITECT-TROUBLESHOOTING-GUIDE.md\n")

    print(f"{Colors.BOLD}Helpful Commands:{Colors.ENDC}\n")
    print(f"  • Check project status: ls -la")
    print(f"  • View git status: git status")
    print(f"  • List available agents: ls .coditect/agents/")
    print(f"  • Read training index: cat .coditect/user-training/README.md\n")

    print(f"{Colors.OKGREEN}{Colors.BOLD}Happy building! 🚀{Colors.ENDC}\n")


def main():
    """Main setup workflow with comprehensive error handling."""
    project_path = None
    created_resources = []

    try:
        print_header("CODITECT Interactive Project Setup")
        print(f"{Colors.BOLD}Welcome to CODITECT!{Colors.ENDC}")
        print(f"This script will set up a new CODITECT project with all necessary structure.\n")
        logger.info("Starting CODITECT interactive setup")

        # Check prerequisites
        try:
            check_prerequisites()
        except PrerequisiteError as e:
            logger.error(f"Prerequisites check failed: {str(e)}")
            print_error(f"\nPrerequisites not met: {str(e)}")
            print_info("\nPlease install required tools and try again.")
            return 1

        # Get project directory
        try:
            project_path = get_project_directory()
            logger.info(f"Project path selected: {project_path}")
        except (KeyboardInterrupt, EOFError):
            logger.info("User cancelled project directory selection")
            print_warning("\nSetup cancelled by user")
            return 130
        except Exception as e:
            logger.error(f"Failed to get project directory: {str(e)}")
            print_error(f"\nFailed to select project directory: {str(e)}")
            return 1

        # Get project information
        try:
            project_info = get_project_info()
            logger.info(f"Project info collected: {project_info['name']}")
        except (KeyboardInterrupt, EOFError):
            logger.info("User cancelled project info entry")
            print_warning("\nSetup cancelled by user")
            return 130
        except Exception as e:
            logger.error(f"Failed to get project info: {str(e)}")
            print_error(f"\nFailed to collect project information: {str(e)}")
            return 1

        # Confirm before proceeding
        print_header("Ready to Create Project")
        print(f"{Colors.BOLD}Project Details:{Colors.ENDC}")
        print(f"  Name: {project_info['name']}")
        print(f"  Type: {project_info['project_type']}")
        print(f"  Location: {project_path}")
        print()

        try:
            confirm = input(f"{Colors.BOLD}Proceed with setup? (y/n):{Colors.ENDC} ").strip().lower()
            if confirm != 'y':
                logger.info("User cancelled setup at confirmation")
                print_warning("Setup cancelled by user")
                return 130
        except (KeyboardInterrupt, EOFError):
            logger.info("User cancelled setup at confirmation")
            print_warning("\nSetup cancelled by user")
            return 130

        # Execute setup steps with individual error handling
        try:
            logger.info("Creating directory structure")
            create_directory_structure(project_path)
            created_resources.append("directory_structure")

            logger.info("Installing CODITECT framework")
            install_coditect_framework(project_path)
            created_resources.append("framework")

            logger.info("Creating initial documentation")
            create_initial_documentation(project_path, project_info)
            created_resources.append("documentation")

            logger.info("Creating .gitignore")
            create_gitignore(project_path)
            created_resources.append("gitignore")

            logger.info("Creating initial git commit")
            initial_git_commit(project_path, project_info)
            created_resources.append("git_commit")

            logger.info("Setup completed successfully")
            print_next_steps(project_path, project_info)
            return 0

        except DirectoryCreationError as e:
            logger.error(f"Directory creation failed: {str(e)}")
            print_error(f"\nDirectory creation failed: {str(e)}")
            print_info("\nPlease check permissions and disk space.")
            return 1

        except FrameworkInstallError as e:
            logger.error(f"Framework installation failed: {str(e)}")
            print_error(f"\nFramework installation failed: {str(e)}")
            print_info("\nYou may need to manually clone the framework:")
            print_info("  git clone https://github.com/coditect-ai/coditect-core.git .coditect")
            return 1

        except GitOperationError as e:
            logger.error(f"Git operation failed: {str(e)}")
            print_error(f"\nGit operation failed: {str(e)}")
            print_info("\nThe project structure was created but git initialization failed.")
            print_info("You can manually initialize git in the project directory.")
            return 1

        except DocumentationError as e:
            logger.error(f"Documentation creation failed: {str(e)}")
            print_error(f"\nDocumentation creation failed: {str(e)}")
            print_info("\nThe project structure was created but documentation generation failed.")
            return 1

    except KeyboardInterrupt:
        logger.info("Setup interrupted by user (Ctrl+C)")
        print_warning("\n\nSetup interrupted by user")

        # Attempt cleanup if project partially created
        if project_path and created_resources:
            print_info(f"\nPartially created resources: {', '.join(created_resources)}")
            print_info(f"Project directory: {project_path}")
            print_info("You may want to remove the partial setup manually.")

        return 130

    except Exception as e:
        logger.exception("Unexpected error during setup")
        print_error(f"\n\nSetup failed with unexpected error: {str(e)}")
        print_info("\nPlease check the log file 'coditect-interactive-setup.log' for details.")

        # Show created resources for cleanup
        if created_resources:
            print_info(f"\nPartially created resources: {', '.join(created_resources)}")

        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.exception("Fatal error in main")
        print(f"\n{Colors.FAIL}Fatal error: {str(e)}{Colors.ENDC}")
        sys.exit(1)
