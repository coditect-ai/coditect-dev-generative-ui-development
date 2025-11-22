#!/bin/bash
#
# Documentation Sync Hook for CODITECT
#
# Automatically updates component inventories and documentation
# when new agents, skills, or commands are created.
#
# Event: PostToolUse
# Matcher: tool_name = "Write"
# Trigger: New .coditect/agents/*.md, .coditect/skills/*/SKILL.md, .coditect/commands/*.md
#

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Read stdin containing hook input JSON
json=$(cat)

# Run Python sync in background (non-blocking PostToolUse hook)
(
    python3 "$SCRIPT_DIR/sync_documentation.py" < <(echo "$json") 2>/dev/null || true
) &

# Return immediately (non-blocking)
echo '{"continue": true, "suppressOutput": true}'
exit 0
