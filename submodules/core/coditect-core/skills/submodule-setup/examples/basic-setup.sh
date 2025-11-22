#!/bin/bash
#
# Basic Submodule Setup Example
#
# This script demonstrates the minimal steps to set up a new CODITECT submodule
# with directory structure, symlinks, and templates.
#
# Usage:
#   ./basic-setup.sh <category> <repo-name>
#
# Examples:
#   ./basic-setup.sh cloud coditect-cloud-newservice
#   ./basic-setup.sh dev coditect-dev-newtool
#
# Exit Codes:
#   0: Success
#   1: Error

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

function usage() {
    echo "Usage: $0 <category> <repo-name>"
    echo ""
    echo "Categories: cloud, dev, gtm, labs, docs, ops, market, core"
    echo "Repo name: Must start with 'coditect-{category}-'"
    echo ""
    echo "Example: $0 cloud coditect-cloud-newservice"
    exit 2
}

function validate_inputs() {
    local category=$1
    local repo_name=$2

    # Validate category
    if [[ ! "$category" =~ ^(cloud|dev|gtm|labs|docs|ops|market|core)$ ]]; then
        echo -e "${RED}✗${NC} Invalid category: $category"
        echo "Must be one of: cloud, dev, gtm, labs, docs, ops, market, core"
        exit 1
    fi

    # Validate repo name starts with coditect-{category}-
    if [[ ! "$repo_name" =~ ^coditect-${category}- ]]; then
        echo -e "${RED}✗${NC} Invalid repo name: $repo_name"
        echo "Must start with: coditect-${category}-"
        exit 1
    fi

    echo -e "${GREEN}✓${NC} Input validation passed"
}

function verify_parent_directory() {
    # Check we're in rollout-master root
    if [[ ! -d ".coditect" ]]; then
        echo -e "${RED}✗${NC} Must run from coditect-rollout-master root directory"
        echo "Current directory: $(pwd)"
        exit 1
    fi

    # Check .coditect has agents
    if [[ ! -d ".coditect/agents" ]]; then
        echo -e "${RED}✗${NC} .coditect/agents not found"
        exit 1
    fi

    echo -e "${GREEN}✓${NC} Parent directory verified"
}

function create_submodule_directory() {
    local category=$1
    local repo_name=$2
    local submodule_path="submodules/${category}/${repo_name}"

    # Create category directory if doesn't exist
    mkdir -p "submodules/${category}"

    # Create submodule directory
    if [[ -d "$submodule_path" ]]; then
        echo -e "${YELLOW}⚠${NC} Directory already exists: $submodule_path"
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    mkdir -p "$submodule_path"
    echo -e "${GREEN}✓${NC} Created directory: $submodule_path"
}

function create_symlinks() {
    local category=$1
    local repo_name=$2
    local submodule_path="submodules/${category}/${repo_name}"

    cd "$submodule_path"

    # Create .coditect symlink
    ln -sf ../../../.coditect .coditect
    echo -e "${GREEN}✓${NC} Created symlink: .coditect -> ../../../.coditect"

    # Create .claude symlink
    ln -sf .coditect .claude
    echo -e "${GREEN}✓${NC} Created symlink: .claude -> .coditect"

    # Verify symlinks work
    if [[ ! -d ".coditect/agents" ]]; then
        echo -e "${RED}✗${NC} Symlink verification failed"
        exit 1
    fi

    echo -e "${GREEN}✓${NC} Symlink verification passed"

    cd ../../..
}

function create_basic_files() {
    local category=$1
    local repo_name=$2
    local submodule_path="submodules/${category}/${repo_name}"

    # Create README.md
    cat > "$submodule_path/README.md" <<EOF
# $repo_name

**Category:** $category

## Purpose

[Brief description of this submodule's purpose]

## Getting Started

This submodule is part of the CODITECT ecosystem and has access to 50+ agents, 74 commands, and 24 skills via the \`.coditect\` symlink.

### Prerequisites

- CODITECT rollout-master repository
- Git submodule access

### Quick Start

\`\`\`bash
# From rollout-master root
cd $submodule_path

# Verify CODITECT access
ls .coditect/agents/

# Start development
\`\`\`

## Documentation

- [PROJECT-PLAN.md](PROJECT-PLAN.md) - Implementation plan
- [TASKLIST.md](TASKLIST.md) - Task tracking

## License

MIT
EOF
    echo -e "${GREEN}✓${NC} Created README.md"

    # Create .gitignore
    cat > "$submodule_path/.gitignore" <<EOF
# Dependencies
node_modules/
venv/
__pycache__/

# Build outputs
dist/
build/
*.pyc

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# CODITECT
# Note: .coditect and .claude are symlinks, not tracked
EOF
    echo -e "${GREEN}✓${NC} Created .gitignore"

    # Create basic PROJECT-PLAN.md
    cat > "$submodule_path/PROJECT-PLAN.md" <<EOF
# $repo_name - Project Plan

## Overview

**Purpose:** [One sentence purpose]

**Timeline:** [Estimated duration]

**Status:** 🟡 Planning

## Phases

### Phase 1: Foundation
- [ ] Setup repository structure
- [ ] Configure development environment
- [ ] Create initial documentation

### Phase 2: Implementation
- [ ] Core functionality
- [ ] Testing
- [ ] Documentation

### Phase 3: Integration
- [ ] Integration with CODITECT ecosystem
- [ ] End-to-end testing
- [ ] Deployment preparation

## Success Criteria

- [ ] All tests passing
- [ ] Documentation complete
- [ ] Integration verified
EOF
    echo -e "${GREEN}✓${NC} Created PROJECT-PLAN.md"

    # Create TASKLIST.md
    cat > "$submodule_path/TASKLIST.md" <<EOF
# $repo_name - Task List

## Current Sprint

### Setup (Week 1)
- [x] Create submodule directory
- [x] Establish symlinks
- [x] Generate initial templates
- [ ] Initialize git repository
- [ ] Push to GitHub

### Development (Week 2+)
- [ ] Define requirements
- [ ] Implement core features
- [ ] Write tests
- [ ] Document APIs

## Backlog

- [ ] Additional features
- [ ] Performance optimization
- [ ] Advanced testing

## Completed

- [x] Submodule setup via CODITECT automation
EOF
    echo -e "${GREEN}✓${NC} Created TASKLIST.md"
}

function initialize_git() {
    local category=$1
    local repo_name=$2
    local submodule_path="submodules/${category}/${repo_name}"

    cd "$submodule_path"

    git init
    echo -e "${GREEN}✓${NC} Initialized git repository"

    # Note: Remote must be added manually with actual GitHub URL
    echo -e "${YELLOW}⚠${NC} Remember to add remote: git remote add origin <github-url>"

    cd ../../..
}

function main() {
    if [[ $# -ne 2 ]]; then
        usage
    fi

    local category=$1
    local repo_name=$2

    echo -e "${GREEN}CODITECT Submodule Setup${NC}"
    echo "Category: $category"
    echo "Repo: $repo_name"
    echo ""

    validate_inputs "$category" "$repo_name"
    verify_parent_directory
    create_submodule_directory "$category" "$repo_name"
    create_symlinks "$category" "$repo_name"
    create_basic_files "$category" "$repo_name"
    initialize_git "$category" "$repo_name"

    echo ""
    echo -e "${GREEN}✓ Submodule setup complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. cd submodules/$category/$repo_name"
    echo "2. git remote add origin <github-url>"
    echo "3. Customize PROJECT-PLAN.md"
    echo "4. Start development!"
}

main "$@"
