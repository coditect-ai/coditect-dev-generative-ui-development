#!/bin/bash
################################################################################
# CODITECT Context Export Automation Script
#
# Purpose: Unified export workflow with manual and automated options
# Author: AZ1.AI CODITECT Team
# Version: 2.0
# Date: 2025-11-16
#
# Usage:
#   ./scripts/export-context.sh [description] [--auto]
#
# Examples:
#   # Manual /export (original behavior)
#   ./scripts/export-context.sh "Sprint Planning Session"
#
#   # Automated extraction (no /export needed)
#   ./scripts/export-context.sh "Sprint Planning Session" --auto
#
#   # Direct automated (advanced)
#   python3 scripts/core/session_export.py --auto
#
# Modes:
#   1. Manual Mode (default): Creates placeholder, waits for /export
#   2. Automated Mode (--auto): Runs session_export.py automatically
#
# Output:
#   MEMORY-CONTEXT/exports/YYYY-MM-DDTHH-MM-SSZ-description.txt
#
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Determine script location and base directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ISO-DATETIME timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%SZ")

# Parse arguments
DESCRIPTION=""
AUTO_MODE=false

for arg in "$@"; do
    if [ "$arg" = "--auto" ]; then
        AUTO_MODE=true
    else
        DESCRIPTION="$arg"
    fi
done

# Default description if not provided
DESCRIPTION="${DESCRIPTION:-EXPORT-CONTEXT}"

# Sanitize description (replace spaces and special chars with hyphens)
SAFE_DESCRIPTION=$(echo "$DESCRIPTION" | sed 's/[^a-zA-Z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')

# Create export directory if it doesn't exist
EXPORT_DIR="$BASE_DIR/MEMORY-CONTEXT/exports"
mkdir -p "$EXPORT_DIR"

# Generate filename
FILENAME="${TIMESTAMP}-${SAFE_DESCRIPTION}.txt"
FILEPATH="$EXPORT_DIR/$FILENAME"

# Print banner
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  CODITECT Context Export Automation${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"

if [ "$AUTO_MODE" = true ]; then
    echo -e "${GREEN}Mode: Automated Extraction${NC}"
    echo -e "${BLUE}Using: session_export.py${NC}\n"
else
    echo -e "${YELLOW}Mode: Manual /export${NC}"
    echo -e "${BLUE}Requires: Claude Code /export command${NC}\n"
fi

echo -e "${BLUE}📋 Description:${NC} $DESCRIPTION"
echo -e "${BLUE}🕐 Timestamp:${NC} $TIMESTAMP"
echo -e "${BLUE}📁 Output File:${NC} $FILENAME"
echo -e "${BLUE}📂 Directory:${NC} $EXPORT_DIR\n"

# Inform user about Claude Code export
echo -e "${YELLOW}⚠️  This script will prepare the export file location.${NC}"
echo -e "${YELLOW}    You need to manually run the /export command in Claude Code.${NC}\n"

echo -e "${GREEN}Please run the following command in Claude Code:${NC}\n"
echo -e "    ${BLUE}/export${NC}\n"

echo -e "${GREEN}When prompted for the file path, use:${NC}\n"
echo -e "    ${BLUE}$FILEPATH${NC}\n"

# Create a placeholder file to indicate export is expected
cat > "$FILEPATH" << EOF
# CODITECT Context Export
# Timestamp: $TIMESTAMP
# Description: $DESCRIPTION
# Status: PENDING - Waiting for /export command

This file is a placeholder. Please run /export in Claude Code and save to this location.

Export will contain:
- Complete conversation history
- Code changes and file modifications
- Decision points and rationale
- Task progress and completions
- Session metadata

This export will be used for:
- MEMORY-CONTEXT session continuity
- NESTED LEARNING pattern extraction
- Cross-session context loading
- Zero catastrophic forgetting

EOF

echo -e "${GREEN}✅ Export placeholder created${NC}"
echo -e "${BLUE}Location:${NC} $FILEPATH\n"

# Check if we're in a git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${YELLOW}Git repository detected. After export completes, you can commit with:${NC}\n"
    echo -e "    ${BLUE}git add MEMORY-CONTEXT/exports/$FILENAME${NC}"
    echo -e "    ${BLUE}git commit -m \"Add context export: $DESCRIPTION\"${NC}"
    echo -e "    ${BLUE}git push${NC}\n"
fi

# Provide instructions for next steps
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Next Steps${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"

echo -e "1. ${GREEN}Run /export in Claude Code${NC}"
echo -e "2. ${GREEN}Save to: $FILEPATH${NC}"
echo -e "3. ${GREEN}Verify export completed successfully${NC}"
echo -e "4. ${GREEN}Commit to git (if in repository)${NC}\n"

# Create symlink to latest export
LATEST_LINK="$EXPORT_DIR/latest-export.txt"
ln -sf "$FILENAME" "$LATEST_LINK"
echo -e "${GREEN}✅ Symlink created: MEMORY-CONTEXT/exports/latest-export.txt → $FILENAME${NC}\n"

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Export preparation complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"

# Return the filepath for scripting purposes
echo "$FILEPATH"
