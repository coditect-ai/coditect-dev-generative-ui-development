#!/bin/bash
# CODITECT Core Repository - Phase 2 Cleanup Script
# Updates .gitignore with comprehensive rules
# Execute from repository root

set -e  # Exit on error

echo "=========================================="
echo "CODITECT Core - Phase 2 .gitignore Update"
echo "=========================================="
echo ""

# Check we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    echo "ERROR: Must be run from coditect-core repository root"
    exit 1
fi

echo "Step 1: Backing up current .gitignore"
if [ -f ".gitignore" ]; then
    cp .gitignore .gitignore.backup
    echo "✅ Backup created: .gitignore.backup"
else
    echo "⚠️  No existing .gitignore found"
fi

echo ""
echo "Step 2: Creating comprehensive .gitignore"
cat > .gitignore << 'EOF'
# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
# venv/  # Uncomment if venv should not be versioned
ENV/
env/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.project
.pydevproject

# OS Files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Testing
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.hypothesis/
.cache

# Logs
*.log
logs/
*.log.*

# Temporary files
*.tmp
*.bak
*.swp
*~

# MEMORY-CONTEXT session exports (uncomment if exports should not be versioned)
# MEMORY-CONTEXT/exports/*.txt
EOF

echo "✅ Comprehensive .gitignore created"
echo "   - Python build artifacts"
echo "   - Virtual environments"
echo "   - IDE files"
echo "   - OS metadata files"
echo "   - Test coverage files"
echo "   - Logs and temporary files"

echo ""
echo "Step 3: Committing .gitignore update"
git add .gitignore
git commit -m "chore: Update .gitignore with comprehensive rules

- Added Python build artifact rules
- Added virtual environment exclusions
- Added IDE file exclusions (.vscode, .idea, etc.)
- Added OS metadata exclusions (.DS_Store, Thumbs.db)
- Added test coverage exclusions
- Added log and temporary file exclusions

Per PROJECT-STRUCTURE-ASSESSMENT.md recommendations"

echo ""
echo "=========================================="
echo "✅ Phase 2 .gitignore Update Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Comprehensive .gitignore with 30+ rules"
echo "  - Previous .gitignore backed up to .gitignore.backup"
echo "  - Changes committed to git"
echo ""
echo "Next: Run ./cleanup-phase3.sh to move test file"
