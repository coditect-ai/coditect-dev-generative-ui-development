#!/bin/bash
#
# Verify Submodules - Validation Script
#
# Comprehensive verification of CODITECT submodule setup including symlink integrity,
# template generation, git configuration, and framework accessibility.
#
# Usage:
#   ./verify-submodules.sh [submodule-path]
#   ./verify-submodules.sh --all
#   ./verify-submodules.sh --category cloud
#
# Examples:
#   ./verify-submodules.sh submodules/cloud/coditect-cloud-backend
#   ./verify-submodules.sh --all
#   ./verify-submodules.sh --category dev
#
# Exit Codes:
#   0: Success - All checks passed
#   1: Validation failed - Some checks failed
#   2: Usage error - Invalid arguments

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
total_checks=0
passed_checks=0
failed_checks=0
warning_checks=0

function usage() {
    echo "Usage: $0 [submodule-path]"
    echo "       $0 --all"
    echo "       $0 --category <category>"
    echo ""
    echo "Examples:"
    echo "  $0 submodules/cloud/coditect-cloud-backend"
    echo "  $0 --all"
    echo "  $0 --category cloud"
    exit 2
}

function check() {
    local test_name="$1"
    local test_cmd="$2"

    ((total_checks++))

    if eval "$test_cmd" &>/dev/null; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((passed_checks++))
        return 0
    else
        echo -e "${RED}✗${NC} $test_name"
        ((failed_checks++))
        return 1
    fi
}

function check_warning() {
    local test_name="$1"
    local test_cmd="$2"

    ((total_checks++))

    if eval "$test_cmd" &>/dev/null; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((passed_checks++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $test_name (warning)"
        ((warning_checks++))
        return 1
    fi
}

function verify_submodule() {
    local submodule_path="$1"
    local submodule_name=$(basename "$submodule_path")

    echo ""
    echo -e "${BLUE}Verifying:${NC} $submodule_path"
    echo "=================================================="

    # Check directory exists
    if [ ! -d "$submodule_path" ]; then
        echo -e "${RED}✗${NC} Directory does not exist: $submodule_path"
        return 1
    fi

    cd "$submodule_path"

    # Symlink Checks
    echo ""
    echo "Symlink Checks:"
    check ".coditect symlink exists" "[ -L .coditect ]"
    check ".coditect points to ../../../.coditect" "[ \$(readlink .coditect) = '../../../.coditect' ]"
    check ".coditect is accessible" "[ -d .coditect ]"
    check ".claude symlink exists" "[ -L .claude ]"
    check ".claude points to .coditect" "[ \$(readlink .claude) = '.coditect' ]"
    check "Agents accessible" "[ \$(ls .coditect/agents/*.md 2>/dev/null | wc -l) -gt 40 ]"
    check "Skills accessible" "[ \$(ls -d .coditect/skills/*/ 2>/dev/null | wc -l) -gt 20 ]"
    check "Commands accessible" "[ \$(ls .coditect/commands/*.md 2>/dev/null | wc -l) -gt 60 ]"

    # Template Checks
    echo ""
    echo "Template Checks:"
    check "PROJECT-PLAN.md exists" "[ -f PROJECT-PLAN.md ]"
    check "PROJECT-PLAN.md has content" "[ \$(wc -l < PROJECT-PLAN.md) -gt 10 ]"
    check "TASKLIST.md exists" "[ -f TASKLIST.md ]"
    check "TASKLIST.md has checkbox format" "grep -q '\- \[ \]' TASKLIST.md"
    check "README.md exists" "[ -f README.md ]"
    check "README.md has description" "[ \$(wc -l < README.md) -gt 10 ]"
    check ".gitignore exists" "[ -f .gitignore ]"

    # Git Configuration Checks
    echo ""
    echo "Git Configuration Checks:"
    check "Git repository initialized" "[ -d .git ]"
    check "Git remote 'origin' configured" "git remote | grep -q origin"
    check "Remote URL is GitHub coditect-ai" "git remote get-url origin | grep -q 'github.com/coditect-ai'"
    check "On main branch" "[ \$(git branch --show-current) = 'main' ]"
    check_warning "No uncommitted changes" "[ -z \"\$(git status --porcelain)\" ]"
    check_warning "No unpushed commits" "[ -z \"\$(git log @{u}.. --oneline 2>/dev/null)\" ]"

    # Parent Integration Checks
    echo ""
    echo "Parent Integration Checks:"
    cd ../../..
    check "Entry in .gitmodules" "grep -q \"$submodule_name\" .gitmodules"
    check "Git submodule status shows submodule" "git submodule status | grep -q \"$submodule_path\""

    cd - > /dev/null

    # Summary
    echo ""
    echo "=================================================="
    echo -e "${BLUE}Summary for $submodule_name:${NC}"
    echo "  Total checks: $total_checks"
    echo -e "  ${GREEN}Passed: $passed_checks${NC}"
    echo -e "  ${YELLOW}Warnings: $warning_checks${NC}"
    echo -e "  ${RED}Failed: $failed_checks${NC}"

    if [ $failed_checks -eq 0 ]; then
        echo -e "${GREEN}✓ Verification passed${NC}"
        if [ $warning_checks -gt 0 ]; then
            echo -e "${YELLOW}⚠ Some warnings present${NC}"
        fi
        return 0
    else
        echo -e "${RED}✗ Verification failed${NC}"
        return 1
    fi
}

function main() {
    if [ $# -eq 0 ]; then
        usage
    fi

    # Check we're in rollout-master root
    if [ ! -d .coditect ]; then
        echo -e "${RED}✗${NC} Must run from coditect-rollout-master root directory"
        exit 1
    fi

    local exit_code=0

    if [ "$1" = "--all" ]; then
        echo "Verifying all submodules..."
        for category_dir in submodules/*/; do
            for submodule_dir in ${category_dir}*/; do
                if [ -d "$submodule_dir" ]; then
                    verify_submodule "$submodule_dir" || exit_code=1
                fi
            done
        done
    elif [ "$1" = "--category" ]; then
        if [ $# -lt 2 ]; then
            echo "Error: --category requires category name"
            usage
        fi
        category="$2"
        echo "Verifying all submodules in category: $category"
        for submodule_dir in submodules/${category}/*/; do
            if [ -d "$submodule_dir" ]; then
                verify_submodule "$submodule_dir" || exit_code=1
            fi
        done
    else
        verify_submodule "$1" || exit_code=1
    fi

    exit $exit_code
}

main "$@"
