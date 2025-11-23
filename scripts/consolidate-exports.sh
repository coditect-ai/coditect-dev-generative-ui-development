#!/bin/bash
# Consolidate Export Files Script
# Purpose: Move all export files (txt files with ISO dates) to MEMORY-CONTEXT/exports-archive/

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ARCHIVE_DIR="MEMORY-CONTEXT/exports-archive"
LOG_FILE="MEMORY-CONTEXT/consolidation-log-$(date +%Y-%m-%d-%H%M%S).txt"

# Ensure archive directory exists
mkdir -p "$ARCHIVE_DIR"

echo -e "${BLUE}=== Export File Consolidation ===${NC}" | tee "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Counter
MOVED=0
SKIPPED=0

# Find all export files (excluding those already in exports-archive)
echo -e "${BLUE}Finding export files...${NC}" | tee -a "$LOG_FILE"
FILES=$(find . -type f -name "*.txt" -path "*/20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]*" 2>/dev/null | grep -v '.git/' | grep -v 'MEMORY-CONTEXT/exports-archive/')

TOTAL=$(echo "$FILES" | wc -l | tr -d ' ')
echo -e "${YELLOW}Found $TOTAL files to process${NC}" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Process each file
while IFS= read -r FILE; do
    if [ -z "$FILE" ]; then
        continue
    fi

    BASENAME=$(basename "$FILE")
    DEST="$ARCHIVE_DIR/$BASENAME"

    # Check if destination already exists
    if [ -f "$DEST" ]; then
        # File exists, add source path prefix
        SOURCE_DIR=$(dirname "$FILE" | sed 's|^\./||' | sed 's|/|-|g')
        NEW_BASENAME="${SOURCE_DIR}--${BASENAME}"
        DEST="$ARCHIVE_DIR/$NEW_BASENAME"

        if [ -f "$DEST" ]; then
            echo -e "${YELLOW}[SKIP]${NC} $FILE (duplicate already exists)" | tee -a "$LOG_FILE"
            ((SKIPPED++))
            continue
        fi
    fi

    # Move file
    echo -e "${GREEN}[MOVE]${NC} $FILE → $DEST" | tee -a "$LOG_FILE"
    mv "$FILE" "$DEST"
    ((MOVED++))

done <<< "$FILES"

echo "" | tee -a "$LOG_FILE"
echo -e "${BLUE}=== Summary ===${NC}" | tee -a "$LOG_FILE"
echo "Total files processed: $TOTAL" | tee -a "$LOG_FILE"
echo -e "${GREEN}Moved: $MOVED${NC}" | tee -a "$LOG_FILE"
echo -e "${YELLOW}Skipped (duplicates): $SKIPPED${NC}" | tee -a "$LOG_FILE"
echo "Completed: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Log saved to: $LOG_FILE" | tee -a "$LOG_FILE"
