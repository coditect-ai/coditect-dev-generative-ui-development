#!/bin/bash
# Sync all submodules to latest from their respective main branches

set -e

echo "🔄 Syncing all CODITECT submodules..."

# Update all submodules to latest
git submodule update --remote --merge

# Show status
echo ""
echo "📊 Submodule status:"
git submodule status

echo ""
echo "✅ Submodules synced successfully!"
echo ""
echo "To commit the updates to the master project:"
echo "  git add ."
echo "  git commit -m 'Update submodule pointers to latest'"
echo "  git push"
