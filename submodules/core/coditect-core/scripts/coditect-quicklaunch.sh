#!/bin/bash

################################################################################
# AZ1.AI CODITECT Quick Launch Setup Script
#
# Copyright © 2025 AZ1.AI INC. All Rights Reserved.
# Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
#
# Purpose: Automated setup for new CODITECT users
# - Creates PROJECTS workspace structure
# - Installs .coditect framework as submodule
# - Sets up multi-LLM CLI symlinks
# - Creates MEMORY-CONTEXT directory
# - Launches interactive tutorial
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
WORKSPACE_DIR="${HOME}/PROJECTS"
CODITECT_REPO="https://github.com/coditect-ai/coditect-core.git"
DEFAULT_LLM="claude"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${CYAN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║                                                                ║${NC}"
    echo -e "${CYAN}${BOLD}║         AZ1.AI CODITECT Quick Launch Setup v1.0                ║${NC}"
    echo -e "${CYAN}${BOLD}║                                                                ║${NC}"
    echo -e "${CYAN}${BOLD}║  AI-First Project Management & Development Platform            ║${NC}"
    echo -e "${CYAN}${BOLD}║                                                                ║${NC}"
    echo -e "${CYAN}${BOLD}║  Copyright © 2025 AZ1.AI INC. All Rights Reserved.             ║${NC}"
    echo -e "${CYAN}${BOLD}║  Developed by Hal Casteel, Founder/CEO/CTO                     ║${NC}"
    echo -e "${CYAN}${BOLD}║                                                                ║${NC}"
    echo -e "${CYAN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}\n"
}

print_step() {
    echo -e "\n${BLUE}${BOLD}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ ERROR: $1${NC}"
}

confirm() {
    read -p "$(echo -e ${YELLOW}$1 [y/N]: ${NC})" -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

################################################################################
# Pre-flight Checks
################################################################################

check_prerequisites() {
    print_step "Running pre-flight checks..."

    # Check for git
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install git first."
        exit 1
    fi
    print_success "Git found: $(git --version)"

    # Check if workspace already exists
    if [ -d "$WORKSPACE_DIR" ]; then
        if [ -d "$WORKSPACE_DIR/.coditect" ]; then
            print_info "CODITECT workspace already exists at $WORKSPACE_DIR"
            if ! confirm "Workspace exists. Re-initialize?"; then
                print_info "Setup cancelled by user."
                exit 0
            fi
        fi
    fi
}

################################################################################
# Workspace Setup
################################################################################

create_workspace() {
    print_step "Creating PROJECTS workspace structure..."

    # Create workspace directory
    mkdir -p "$WORKSPACE_DIR"
    cd "$WORKSPACE_DIR"
    print_success "Created workspace directory: $WORKSPACE_DIR"

    # Initialize git if not already initialized
    if [ ! -d ".git" ]; then
        git init
        git branch -m main
        print_success "Initialized git repository"
    else
        print_info "Git repository already initialized"
    fi
}

install_coditect_framework() {
    print_step "Installing AZ1.AI CODITECT framework..."

    cd "$WORKSPACE_DIR"

    # Remove existing .coditect if re-initializing
    if [ -d ".coditect" ]; then
        print_info "Removing existing .coditect framework..."
        rm -rf .coditect
        git rm -rf .coditect 2>/dev/null || true
    fi

    # Add as submodule
    git submodule add "$CODITECT_REPO" .coditect 2>/dev/null || {
        print_info "Submodule already exists, updating instead..."
        git submodule update --init --remote .coditect
    }

    print_success "CODITECT framework installed"
}

setup_llm_symlinks() {
    print_step "Setting up multi-LLM CLI integration..."

    cd "$WORKSPACE_DIR"

    # Supported LLM CLIs
    LLMS=("claude" "gemini" "copilot" "cursor" "grok" "cody")

    for llm in "${LLMS[@]}"; do
        if [ -L ".$llm" ]; then
            print_info ".$llm symlink already exists"
        else
            ln -s .coditect ".$llm"
            print_success "Created .$llm -> .coditect symlink"
        fi
    done

    print_success "Multi-LLM CLI integration ready"
}

create_memory_context() {
    print_step "Creating MEMORY-CONTEXT directory..."

    cd "$WORKSPACE_DIR"

    # Create MEMORY-CONTEXT directory
    mkdir -p MEMORY-CONTEXT

    # Copy README template
    if [ -f ".coditect/templates/MEMORY-CONTEXT-README.md" ]; then
        cp .coditect/templates/MEMORY-CONTEXT-README.md MEMORY-CONTEXT/README.md
        print_success "Created MEMORY-CONTEXT/README.md from template"
    else
        print_info "Template not found, creating basic README"
        cat > MEMORY-CONTEXT/README.md << 'EOF'
# MEMORY-CONTEXT

**Session Exports and Development History**

This folder contains exported conversations and session summaries. These files serve as historical context and knowledge base for future sessions.

See ~/PROJECTS/.coditect/MEMORY-CONTEXT-GUIDE.md for complete usage guide.

---

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
EOF
    fi

    print_success "MEMORY-CONTEXT directory created"
}

configure_gitignore() {
    print_step "Configuring .gitignore..."

    cd "$WORKSPACE_DIR"

    # Create/update .gitignore
    cat > .gitignore << 'EOF'
# Symlinks to .coditect (project-specific, not version controlled)
.claude
.gemini
.copilot
.cursor
.grok
.cody

# Individual project directories (have their own git repos)
*/

# Memory context files (session exports and summaries)
MEMORY-CONTEXT/

# macOS
.DS_Store

# Keep only the framework structure
!.gitignore
!.gitmodules
!README.md
!SETUP-SUMMARY.md
EOF

    print_success ".gitignore configured"
}

create_workspace_readme() {
    print_step "Creating workspace README..."

    cd "$WORKSPACE_DIR"

    cat > README.md << 'EOF'
# AZ1.AI CODITECT PROJECTS Workspace

**AI-First Project Management & Development Platform**

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.**

---

## 🎯 What is This Workspace?

This is your **CODITECT PROJECTS workspace** - a centralized development environment for all your projects using the AZ1.AI CODITECT Platform.

## 📂 Directory Structure

```
~/PROJECTS/
├── .coditect/              # CODITECT Framework (submodule - DO commit)
├── .claude -> .coditect    # Claude Code symlink (gitignored)
├── .gemini -> .coditect    # Gemini symlink (gitignored)
├── .copilot -> .coditect   # Copilot symlink (gitignored)
├── .cursor -> .coditect    # Cursor symlink (gitignored)
├── MEMORY-CONTEXT/         # Session history (gitignored)
├── .gitignore
├── .gitmodules
├── README.md
└── [your-projects]/        # Individual project folders
```

## 🚀 Getting Started

### 1. Read the CODITECT Quickstart Guide

```bash
cat .coditect/AZ1.AI-CODITECT-1-2-3-QUICKSTART.md
```

### 2. Launch the Interactive Tutorial

```bash
.coditect/scripts/coditect-tutorial.sh
```

### 3. Create Your First Project

```bash
mkdir my-first-project
cd my-first-project
# Start Claude Code (or your preferred LLM CLI)
# Follow the CODITECT 1-2-3 process
```

## 📖 Documentation

**Core Framework Docs** (in `.coditect/`):
- `AZ1.AI-CODITECT-1-2-3-QUICKSTART.md` - Complete 3-phase methodology
- `C4-ARCHITECTURE-METHODOLOGY.md` - C4 Model architecture guide
- `MULTI-LLM-CLI-INTEGRATION.md` - Multi-LLM CLI setup
- `MEMORY-CONTEXT-GUIDE.md` - Session continuity guide
- `PLATFORM-EVOLUTION-ROADMAP.md` - Platform roadmap

**Quick Reference**:
```bash
# Update CODITECT framework
git submodule update --remote .coditect

# Export session context (in Claude Code)
/export 2025-XX-XX-EXPORT-CONTEXT-[TOPIC].txt
mv 2025-XX-XX-EXPORT-CONTEXT-[TOPIC].txt ~/PROJECTS/MEMORY-CONTEXT/

# Review previous session
cat MEMORY-CONTEXT/SESSION-SUMMARY-$(ls MEMORY-CONTEXT/SESSION-SUMMARY-*.md | tail -1)
```

## 🎓 Learning Path

1. **Beginner**: Follow interactive tutorial
2. **Intermediate**: Create sample project using CODITECT 1-2-3
3. **Advanced**: Review ORCHESTRATOR-PROJECT-PLAN.md for autonomous development

## 🔄 Updating Framework

```bash
cd ~/PROJECTS
git submodule update --remote .coditect
git add .coditect
git commit -m "Update CODITECT framework to latest version"
```

## 🆘 Support

- **Documentation**: `~/PROJECTS/.coditect/`
- **Issues**: https://github.com/coditect-ai/coditect-core/issues
- **Email**: support@az1.ai

---

**Built with Excellence by AZ1.AI CODITECT**

*Systematic Development. Continuous Context. Exceptional Results.*

**AZ1.AI INC.**
Founded 2025
Innovation Through AI-First Development
EOF

    print_success "Workspace README created"
}

commit_workspace_structure() {
    print_step "Committing workspace structure..."

    cd "$WORKSPACE_DIR"

    # Stage files
    git add .coditect .gitignore .gitmodules README.md

    # Commit
    git commit -m "Initialize AZ1.AI CODITECT workspace

- Add .coditect framework as submodule
- Configure multi-LLM CLI symlinks
- Create MEMORY-CONTEXT directory
- Setup workspace structure

Copyright © 2025 AZ1.AI INC. All Rights Reserved." 2>/dev/null || {
        print_info "No changes to commit (workspace already initialized)"
    }

    print_success "Workspace structure committed"
}

################################################################################
# Tutorial Launch
################################################################################

launch_tutorial() {
    print_step "Setup complete! Ready to launch tutorial?"

    echo -e "\n${CYAN}The interactive tutorial will walk you through:${NC}"
    echo -e "  ${GREEN}✓${NC} Creating a project plan"
    echo -e "  ${GREEN}✓${NC} Building a tasklist with checkboxes"
    echo -e "  ${GREEN}✓${NC} Following the AZ1.AI AUTONOMOUS DEVELOPMENT PROCESS"
    echo -e "  ${GREEN}✓${NC} Learning CODITECT best practices"

    if confirm "\nLaunch interactive tutorial now?"; then
        if [ -f "$WORKSPACE_DIR/.coditect/scripts/coditect-tutorial.sh" ]; then
            bash "$WORKSPACE_DIR/.coditect/scripts/coditect-tutorial.sh"
        else
            print_error "Tutorial script not found. Please run manually:"
            echo -e "${YELLOW}  bash ~/PROJECTS/.coditect/scripts/coditect-tutorial.sh${NC}"
        fi
    else
        print_info "You can launch the tutorial later with:"
        echo -e "${YELLOW}  bash ~/PROJECTS/.coditect/scripts/coditect-tutorial.sh${NC}"
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    print_header

    check_prerequisites
    create_workspace
    install_coditect_framework
    setup_llm_symlinks
    create_memory_context
    configure_gitignore
    create_workspace_readme
    commit_workspace_structure

    echo -e "\n${GREEN}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}${BOLD}║                                                                ║${NC}"
    echo -e "${GREEN}${BOLD}║                    SETUP COMPLETE! 🎉                          ║${NC}"
    echo -e "${GREEN}${BOLD}║                                                                ║${NC}"
    echo -e "${GREEN}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}\n"

    echo -e "${CYAN}Your CODITECT workspace is ready at:${NC}"
    echo -e "${BOLD}  $WORKSPACE_DIR${NC}\n"

    echo -e "${CYAN}Next steps:${NC}"
    echo -e "  ${GREEN}1.${NC} Launch the interactive tutorial"
    echo -e "  ${GREEN}2.${NC} Read the quickstart guide: ${YELLOW}.coditect/AZ1.AI-CODITECT-1-2-3-QUICKSTART.md${NC}"
    echo -e "  ${GREEN}3.${NC} Create your first project!"

    launch_tutorial
}

# Run main function
main "$@"
