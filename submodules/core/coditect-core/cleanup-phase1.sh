#!/bin/bash
# CODITECT Core Repository - Phase 1 Cleanup Script
# Moves misplaced files and removes build artifacts
# Execute from repository root

set -e  # Exit on error

echo "=========================================="
echo "CODITECT Core - Phase 1 Cleanup"
echo "=========================================="
echo ""

# Check we're in the right directory
if [ ! -f "CLAUDE.md" ] || [ ! -d "MEMORY-CONTEXT" ]; then
    echo "ERROR: Must be run from coditect-core repository root"
    exit 1
fi

echo "Step 1: Moving session export to MEMORY-CONTEXT/exports/"
if [ -f "2025-11-22-EXPORT-AGENT-REVIEW-cr-analyze-the-new-checkpoint-in-submodulescore.txt" ]; then
    mv 2025-11-22-EXPORT-AGENT-REVIEW-cr-analyze-the-new-checkpoint-in-submodulescore.txt \
       MEMORY-CONTEXT/exports/
    echo "✅ Session export moved"
else
    echo "⚠️  Session export file not found (may already be moved)"
fi

echo ""
echo "Step 2: Removing macOS .DS_Store metadata files"
DS_COUNT=$(find . -name ".DS_Store" -type f | wc -l | tr -d ' ')
if [ "$DS_COUNT" -gt 0 ]; then
    find . -name ".DS_Store" -type f -delete
    echo "✅ Removed $DS_COUNT .DS_Store files"
else
    echo "✅ No .DS_Store files found"
fi

echo ""
echo "Step 3: Removing Python __pycache__ directories"
CACHE_COUNT=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l | tr -d ' ')
if [ "$CACHE_COUNT" -gt 0 ]; then
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    echo "✅ Removed $CACHE_COUNT __pycache__ directories"
else
    echo "✅ No __pycache__ directories found"
fi

echo ""
echo "Step 4: Staging changes in git"
git add -u
if [ -f "MEMORY-CONTEXT/exports/2025-11-22-EXPORT-AGENT-REVIEW-cr-analyze-the-new-checkpoint-in-submodulescore.txt" ]; then
    git add MEMORY-CONTEXT/exports/
fi

echo ""
echo "Step 5: Committing cleanup"
git commit -m "chore: Clean up root directory - move exports, remove metadata and cache files

- Moved session export to MEMORY-CONTEXT/exports/
- Removed $DS_COUNT .DS_Store macOS metadata files
- Removed $CACHE_COUNT Python __pycache__ directories
- Cleaned up build artifacts per PROJECT-STRUCTURE-ASSESSMENT.md"

echo ""
echo "=========================================="
echo "✅ Phase 1 Cleanup Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Session export moved to proper location"
echo "  - Build artifacts removed"
echo "  - Changes committed to git"
echo ""
echo "Next: Run ./cleanup-phase2.sh to update .gitignore"
