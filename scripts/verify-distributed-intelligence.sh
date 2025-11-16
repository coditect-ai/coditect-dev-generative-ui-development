#!/bin/bash
################################################################################
# CODITECT Distributed Intelligence Verification Script
#
# Purpose: Verify all submodules have correct symlinks and can access framework
# Author: AZ1.AI CODITECT Team
# Version: 1.0
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

MASTER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOTAL=0
PASSED=0
FAILED=0
declare -a FAILED_CHECKS

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  CODITECT Distributed Intelligence Verification${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"

cd "$MASTER_DIR"

# Check master repo symlinks
echo -e "${BLUE}Checking Master Repository...${NC}"
TOTAL=$((TOTAL + 2))

if [ -L ".coditect" ]; then
    target=$(readlink .coditect)
    if [ "$target" = "submodules/coditect-project-dot-claude" ]; then
        echo -e "${GREEN}✅ Master .coditect symlink correct${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌ Master .coditect symlink incorrect: $target${NC}"
        FAILED=$((FAILED + 1))
        FAILED_CHECKS+=("Master .coditect → $target (expected: submodules/coditect-project-dot-claude)")
    fi
else
    echo -e "${RED}❌ Master .coditect symlink missing${NC}"
    FAILED=$((FAILED + 1))
    FAILED_CHECKS+=("Master .coditect missing")
fi

if [ -L ".claude" ]; then
    target=$(readlink .claude)
    if [ "$target" = ".coditect" ]; then
        echo -e "${GREEN}✅ Master .claude symlink correct${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌ Master .claude symlink incorrect: $target${NC}"
        FAILED=$((FAILED + 1))
        FAILED_CHECKS+=("Master .claude → $target (expected: .coditect)")
    fi
else
    echo -e "${RED}❌ Master .claude symlink missing${NC}"
    FAILED=$((FAILED + 1))
    FAILED_CHECKS+=("Master .claude missing")
fi

echo ""

# Check each submodule
echo -e "${BLUE}Checking All Submodules...${NC}\n"

for submodule_path in submodules/*/; do
    if [ ! -d "$submodule_path" ]; then
        continue
    fi
    
    submodule_name=$(basename "$submodule_path")
    echo -e "${BLUE}[$submodule_name]${NC}"
    
    cd "$submodule_path"
    
    # Check .coditect symlink
    TOTAL=$((TOTAL + 1))
    if [ -L ".coditect" ]; then
        target=$(readlink .coditect)
        if [ "$target" = "../../.coditect" ]; then
            echo -e "  ${GREEN}✅ .coditect → $target${NC}"
            PASSED=$((PASSED + 1))
        else
            echo -e "  ${RED}❌ .coditect → $target (expected: ../../.coditect)${NC}"
            FAILED=$((FAILED + 1))
            FAILED_CHECKS+=("$submodule_name/.coditect → $target")
        fi
    else
        echo -e "  ${RED}❌ .coditect symlink missing${NC}"
        FAILED=$((FAILED + 1))
        FAILED_CHECKS+=("$submodule_name/.coditect missing")
    fi
    
    # Check .claude symlink
    TOTAL=$((TOTAL + 1))
    if [ -L ".claude" ] || [ -L ".claude/.coditect" ]; then
        if [ -L ".claude/.coditect" ]; then
            # Some repos have .claude as directory with .coditect inside
            target=$(readlink .claude/.coditect)
            echo -e "  ${GREEN}✅ .claude/.coditect → $target${NC}"
            PASSED=$((PASSED + 1))
        else
            target=$(readlink .claude)
            if [ "$target" = ".coditect" ]; then
                echo -e "  ${GREEN}✅ .claude → $target${NC}"
                PASSED=$((PASSED + 1))
            else
                echo -e "  ${RED}❌ .claude → $target (expected: .coditect)${NC}"
                FAILED=$((FAILED + 1))
                FAILED_CHECKS+=("$submodule_name/.claude → $target")
            fi
        fi
    else
        echo -e "  ${RED}❌ .claude symlink missing${NC}"
        FAILED=$((FAILED + 1))
        FAILED_CHECKS+=("$submodule_name/.claude missing")
    fi
    
    # Test framework access
    TOTAL=$((TOTAL + 1))
    if [ -d ".coditect/agents" ] || [ -L ".coditect/agents" ]; then
        echo -e "  ${GREEN}✅ Framework accessible${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}❌ Framework not accessible${NC}"
        FAILED=$((FAILED + 1))
        FAILED_CHECKS+=("$submodule_name framework not accessible")
    fi
    
    cd "$MASTER_DIR"
    echo ""
done

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  VERIFICATION SUMMARY${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"

echo -e "Total Checks: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 ALL CHECKS PASSED - Distributed Intelligence 100% Operational${NC}\n"
    exit 0
else
    echo -e "\n${RED}❌ FAILED CHECKS:${NC}"
    printf '%s\n' "${FAILED_CHECKS[@]}" | sed 's/^/  ❌ /'
    echo ""
    exit 1
fi
