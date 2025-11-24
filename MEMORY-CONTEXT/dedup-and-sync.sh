#!/bin/bash
#
# Automated Dedup and Git Sync Workflow
#
# This script automates the complete workflow:
# 1. Run deduplication on latest export
# 2. Check all submodules for changes
# 3. Commit and push changes in each submodule
# 4. Check master repo for changes
# 5. Commit and push master repo changes
#
# Usage:
#   ./dedup-and-sync.sh [--no-backup]
#
# Author: AZ1.AI CODITECT
# License: MIT

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MASTER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Counters
SUBMODULES_WITH_CHANGES=0
SUBMODULES_COMMITTED=0
SUBMODULES_PUSHED=0

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Automated Dedup and Git Sync Workflow${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Step 1: Run deduplication
echo -e "${YELLOW}Step 1: Running deduplication...${NC}"
cd "$SCRIPT_DIR"

if [ "$1" = "--no-backup" ]; then
    ./reindex-dedup.sh --no-backup
else
    ./reindex-dedup.sh
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Deduplication completed successfully${NC}"
else
    echo -e "${RED}✗ Deduplication failed${NC}"
    exit 1
fi

echo ""

# Step 1.5: Rebuild search index
echo -e "${YELLOW}Step 1.5: Rebuilding search index...${NC}"
cd "$SCRIPT_DIR/scripts"

if [ -f "index-messages.py" ]; then
    python3 index-messages.py --rebuild

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Search index rebuilt successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Search index rebuild failed (non-critical)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ index-messages.py not found, skipping search index${NC}"
fi

echo ""

# Step 1.6: Regenerate dashboard
echo -e "${YELLOW}Step 1.6: Regenerating dashboard data...${NC}"

if [ -f "generate-dashboard.py" ]; then
    python3 generate-dashboard.py

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dashboard data regenerated successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Dashboard regeneration failed (non-critical)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ generate-dashboard.py not found, skipping dashboard${NC}"
fi

echo ""

# Step 2: Process all submodules
echo -e "${YELLOW}Step 2: Processing submodules...${NC}"
cd "$MASTER_ROOT"

# Get list of all submodules
SUBMODULES=$(git submodule status | awk '{print $2}')

if [ -z "$SUBMODULES" ]; then
    echo -e "${YELLOW}⚠ No submodules found${NC}"
else
    echo -e "Found $(echo "$SUBMODULES" | wc -l | xargs) submodules"
    echo ""

    for SUBMODULE_PATH in $SUBMODULES; do
        echo -e "${BLUE}▶ Checking submodule: ${SUBMODULE_PATH}${NC}"

        cd "$MASTER_ROOT/$SUBMODULE_PATH"

        # Check if there are changes
        if [ -n "$(git status --porcelain)" ]; then
            SUBMODULES_WITH_CHANGES=$((SUBMODULES_WITH_CHANGES + 1))

            echo -e "${YELLOW}  Changes detected${NC}"

            # Show what changed
            git status --short | head -10

            # Stage all changes
            git add -A

            # Create commit message
            TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
            COMMIT_MSG="chore: Auto-sync after deduplication

Automated commit from dedup-and-sync.sh
Timestamp: $TIMESTAMP

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

            # Commit
            git commit -m "$COMMIT_MSG"

            if [ $? -eq 0 ]; then
                SUBMODULES_COMMITTED=$((SUBMODULES_COMMITTED + 1))
                echo -e "${GREEN}  ✓ Changes committed${NC}"

                # Push
                CURRENT_BRANCH=$(git branch --show-current)
                git push origin "$CURRENT_BRANCH"

                if [ $? -eq 0 ]; then
                    SUBMODULES_PUSHED=$((SUBMODULES_PUSHED + 1))
                    echo -e "${GREEN}  ✓ Changes pushed to origin/$CURRENT_BRANCH${NC}"
                else
                    echo -e "${RED}  ✗ Failed to push changes${NC}"
                fi
            else
                echo -e "${RED}  ✗ Failed to commit changes${NC}"
            fi
        else
            echo -e "${GREEN}  ✓ No changes${NC}"
        fi

        echo ""
    done
fi

# Step 3: Process master repo
echo -e "${YELLOW}Step 3: Processing master repository...${NC}"
cd "$MASTER_ROOT"

# Check for submodule pointer updates
git submodule update --remote --merge 2>/dev/null || true

# Check if there are changes (including submodule pointers)
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Changes detected in master repository${NC}"

    # Show what changed
    git status --short

    # Stage all changes
    git add -A

    # Create commit message
    TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    # Check if submodule pointers changed
    SUBMODULE_CHANGES=$(git diff --cached --name-only | grep "^submodules/" || true)

    if [ -n "$SUBMODULE_CHANGES" ]; then
        COMMIT_MSG="chore: Update submodule pointers after dedup sync

Submodules updated:
$(echo "$SUBMODULE_CHANGES" | sed 's/^/- /')

Automated commit from dedup-and-sync.sh
Timestamp: $TIMESTAMP

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
    else
        COMMIT_MSG="chore: Auto-sync master repository

Automated commit from dedup-and-sync.sh
Timestamp: $TIMESTAMP

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
    fi

    # Commit
    git commit -m "$COMMIT_MSG"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Master repository changes committed${NC}"

        # Push
        CURRENT_BRANCH=$(git branch --show-current)
        git push origin "$CURRENT_BRANCH"

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Master repository changes pushed to origin/$CURRENT_BRANCH${NC}"
        else
            echo -e "${RED}✗ Failed to push master repository changes${NC}"
        fi
    else
        echo -e "${RED}✗ Failed to commit master repository changes${NC}"
    fi
else
    echo -e "${GREEN}✓ No changes in master repository${NC}"
fi

echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "Submodules with changes: ${YELLOW}${SUBMODULES_WITH_CHANGES}${NC}"
echo -e "Submodules committed:    ${GREEN}${SUBMODULES_COMMITTED}${NC}"
echo -e "Submodules pushed:       ${GREEN}${SUBMODULES_PUSHED}${NC}"
echo ""
echo -e "${GREEN}✅ Workflow completed successfully!${NC}"
