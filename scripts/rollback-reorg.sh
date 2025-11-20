#!/bin/bash
# CODITECT Repository Reorganization Rollback Script
# Created: 2025-11-19
# Purpose: Restore repository state to pre-reorganization state

set -e

BACKUP_DIR="backups/pre-reorg-2025-11-19"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== CODITECT Repository Reorganization Rollback ==="
echo ""
echo "This script will restore the repository to its pre-reorganization state."
echo "Backup directory: $BACKUP_DIR"
echo ""

# Check if backup directory exists
if [ ! -d "$REPO_ROOT/$BACKUP_DIR" ]; then
    echo "ERROR: Backup directory not found: $REPO_ROOT/$BACKUP_DIR"
    exit 1
fi

# Confirm rollback
read -p "Are you sure you want to rollback? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Rollback cancelled."
    exit 0
fi

cd "$REPO_ROOT"

echo ""
echo "Step 1: Deinitializing all submodules..."
git submodule deinit -f --all || true

echo ""
echo "Step 2: Restoring .gitmodules from backup..."
cp "$BACKUP_DIR/.gitmodules.backup" .gitmodules

echo ""
echo "Step 3: Removing .git/modules directory..."
rm -rf .git/modules/submodules

echo ""
echo "Step 4: Removing submodules directory..."
rm -rf submodules

echo ""
echo "Step 5: Re-initializing submodules from backup..."
git submodule update --init --recursive

echo ""
echo "Step 6: Verifying submodule status..."
git submodule status

echo ""
echo "=== Rollback Complete ==="
echo ""
echo "NOTE: This script only rolls back local changes."
echo "If GitHub renames/transfers were executed, you may need to:"
echo "1. Manually rename repos back using 'gh repo rename'"
echo "2. Transfer repos back to original organizations"
echo "3. Update remote URLs in submodules"
echo ""
echo "Backup SHA list available at: $BACKUP_DIR/submodule-shas.txt"
