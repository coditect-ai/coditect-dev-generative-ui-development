#!/bin/bash
# CODITECT Core Repository - Phase 3 Cleanup Script
# Moves test file to proper location
# Execute from repository root

set -e  # Exit on error

echo "=========================================="
echo "CODITECT Core - Phase 3 Test File Move"
echo "=========================================="
echo ""

# Check we're in the right directory
if [ ! -f "CLAUDE.md" ] || [ ! -d "tests" ]; then
    echo "ERROR: Must be run from coditect-core repository root"
    exit 1
fi

echo "Step 1: Creating tests/core directory if needed"
mkdir -p tests/core
echo "✅ tests/core directory ready"

echo ""
echo "Step 2: Moving test_real_export.py to tests/core/"
if [ -f "test_real_export.py" ]; then
    mv test_real_export.py tests/core/
    echo "✅ test_real_export.py moved to tests/core/"
else
    echo "⚠️  test_real_export.py not found (may already be moved)"
fi

echo ""
echo "Step 3: Committing change"
if [ -f "tests/core/test_real_export.py" ]; then
    git add tests/core/test_real_export.py
    git commit -m "chore: Move test_real_export.py to tests/core/

- Moved test file from root to proper tests/ directory
- Improves organizational consistency
- Per PROJECT-STRUCTURE-ASSESSMENT.md recommendations"
    echo "✅ Changes committed"
else
    echo "⚠️  No changes to commit"
fi

echo ""
echo "=========================================="
echo "✅ Phase 3 Test File Move Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - test_real_export.py moved to tests/core/"
echo "  - Root directory now contains only essential files"
echo "  - Changes committed to git"
echo ""
echo "Next: Review PROJECT-STRUCTURE-ASSESSMENT.md for optional Phase 4 (LICENSE)"
