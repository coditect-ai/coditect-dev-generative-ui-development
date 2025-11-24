#!/bin/bash
#
# Reindex Deduplication State - Rebuild Indices from Source Data
#
# This script rebuilds the deduplication indices from the unique_messages.jsonl
# source file. Use this to:
# - Recover from corrupted index files
# - Recalculate statistics after manual changes
# - Verify index integrity
#
# Usage:
#   ./reindex-dedup.sh              # Reindex with automatic backup
#   ./reindex-dedup.sh --no-backup  # Reindex without backup (faster)
#
# Author: AZ1.AI CODITECT
# License: MIT

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to the deduplicator script
DEDUP_SCRIPT="${SCRIPT_DIR}/../submodules/core/coditect-core/scripts/core/message_deduplicator.py"

# Storage directory
STORAGE_DIR="${SCRIPT_DIR}/dedup_state"

# Check if dedup script exists
if [ ! -f "$DEDUP_SCRIPT" ]; then
    echo "❌ Error: Deduplicator script not found at $DEDUP_SCRIPT"
    echo "Please ensure the coditect-core submodule is initialized."
    exit 1
fi

# Check if storage directory exists
if [ ! -d "$STORAGE_DIR" ]; then
    echo "❌ Error: Storage directory not found at $STORAGE_DIR"
    echo "No deduplication state to reindex."
    exit 1
fi

# Run reindex
echo "🔄 Reindexing deduplication state..."
echo "Storage: $STORAGE_DIR"
echo ""

python3 "$DEDUP_SCRIPT" --reindex --storage-dir "$STORAGE_DIR" "$@"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Reindex completed successfully!"
else
    echo ""
    echo "❌ Reindex failed with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
