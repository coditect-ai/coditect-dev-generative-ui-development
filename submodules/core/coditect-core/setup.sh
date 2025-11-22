#!/usr/bin/env bash
# =============================================================================
# CODITECT Framework - Development Environment Setup
# =============================================================================
#
# This script sets up the Python virtual environment and installs all
# dependencies required for the CODITECT framework, including the
# conversation deduplication system.
#
# Usage:
#   ./setup.sh              # Full setup (venv + dependencies + tests)
#   ./setup.sh --venv-only  # Create venv only (no dependency install)
#   ./setup.sh --deps-only  # Install dependencies only (assumes venv exists)
#   ./setup.sh --test       # Run tests to verify setup
#   ./setup.sh --clean      # Remove venv and start fresh
#
# Requirements:
#   - Python 3.9 or higher
#   - pip (Python package installer)
#
# =============================================================================

set -euo pipefail  # Exit on error, undefined variables, pipe failures

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"
REQUIREMENTS_FILE="${SCRIPT_DIR}/requirements.txt"
PYTHON_MIN_VERSION="3.9"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo -e "${BLUE}=================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# =============================================================================
# Python Version Check
# =============================================================================

check_python_version() {
    print_info "Checking Python version..."

    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python ${PYTHON_MIN_VERSION} or higher."
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

    if [[ "$PYTHON_MAJOR" -lt 3 ]] || [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 9 ]]; then
        print_error "Python ${PYTHON_VERSION} detected. Minimum required: ${PYTHON_MIN_VERSION}"
        exit 1
    fi

    print_success "Python ${PYTHON_VERSION} detected"
}

# =============================================================================
# Virtual Environment Setup
# =============================================================================

create_venv() {
    print_header "Creating Python Virtual Environment"

    if [[ -d "$VENV_DIR" ]]; then
        print_warning "Virtual environment already exists at: $VENV_DIR"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Skipping venv creation"
            return 0
        fi
        print_info "Removing existing venv..."
        rm -rf "$VENV_DIR"
    fi

    print_info "Creating virtual environment at: $VENV_DIR"
    python3 -m venv "$VENV_DIR"

    print_success "Virtual environment created successfully"
}

# =============================================================================
# Dependency Installation
# =============================================================================

install_dependencies() {
    print_header "Installing Dependencies"

    if [[ ! -d "$VENV_DIR" ]]; then
        print_error "Virtual environment not found. Run with --venv-only first or no arguments."
        exit 1
    fi

    # Activate venv
    print_info "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate"

    # Upgrade pip
    print_info "Upgrading pip..."
    python -m pip install --upgrade pip --quiet

    # Install dependencies
    if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
        print_error "requirements.txt not found at: $REQUIREMENTS_FILE"
        exit 1
    fi

    print_info "Installing dependencies from requirements.txt..."
    pip install -r "$REQUIREMENTS_FILE"

    print_success "All dependencies installed successfully"

    # Show installed packages
    print_info "Installed packages:"
    pip list | grep -E "pytest|coverage|black|flake8|mypy|isort|psycopg2|ipython|gitpython" || true
}

# =============================================================================
# Test Suite
# =============================================================================

run_tests() {
    print_header "Running Test Suite"

    if [[ ! -d "$VENV_DIR" ]]; then
        print_error "Virtual environment not found. Run setup first."
        exit 1
    fi

    # Activate venv
    source "${VENV_DIR}/bin/activate"

    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        print_error "pytest not installed. Run setup with dependency installation first."
        exit 1
    fi

    # Run tests
    print_info "Running tests..."
    if pytest "${SCRIPT_DIR}/tests/" -v --cov="${SCRIPT_DIR}/scripts/" --cov-report=term-missing; then
        print_success "All tests passed!"
    else
        print_error "Some tests failed. Please review the output above."
        exit 1
    fi
}

# =============================================================================
# Cleanup
# =============================================================================

clean_venv() {
    print_header "Cleaning Up"

    if [[ -d "$VENV_DIR" ]]; then
        print_warning "This will remove the virtual environment at: $VENV_DIR"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR"
            print_success "Virtual environment removed"
        else
            print_info "Cleanup cancelled"
        fi
    else
        print_info "No virtual environment found to clean"
    fi
}

# =============================================================================
# Usage Information
# =============================================================================

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Setup the CODITECT Framework development environment.

Options:
  (no args)        Full setup: create venv + install dependencies
  --venv-only      Create virtual environment only
  --deps-only      Install dependencies only (assumes venv exists)
  --test           Run test suite to verify setup
  --clean          Remove virtual environment
  --help, -h       Show this help message

Examples:
  $0                 # Full setup
  $0 --test          # Run tests after setup
  $0 --clean         # Clean up and start over

Requirements:
  - Python ${PYTHON_MIN_VERSION} or higher
  - pip (Python package installer)

For more information, see README.md
EOF
}

# =============================================================================
# Main Script Logic
# =============================================================================

main() {
    # Change to script directory
    cd "$SCRIPT_DIR"

    # Parse arguments
    case "${1:-}" in
        --venv-only)
            check_python_version
            create_venv
            print_success "Setup complete! Activate with: source venv/bin/activate"
            ;;
        --deps-only)
            check_python_version
            install_dependencies
            print_success "Dependencies installed!"
            ;;
        --test)
            run_tests
            ;;
        --clean)
            clean_venv
            ;;
        --help|-h)
            show_usage
            ;;
        "")
            # Full setup
            print_header "CODITECT Framework Setup"
            check_python_version
            create_venv
            install_dependencies
            print_success "Setup complete!"
            echo ""
            print_info "To activate the virtual environment, run:"
            echo -e "  ${GREEN}source venv/bin/activate${NC}"
            echo ""
            print_info "To run tests:"
            echo -e "  ${GREEN}./setup.sh --test${NC}"
            echo ""
            print_info "To deactivate when done:"
            echo -e "  ${GREEN}deactivate${NC}"
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
