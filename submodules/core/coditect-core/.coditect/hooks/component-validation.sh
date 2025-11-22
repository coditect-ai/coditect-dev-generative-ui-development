#!/bin/bash
#
# Component Validation Hook for CODITECT
#
# Validates new agents, skills, and commands against STANDARDS.md
# Blocks component creation if validation fails
#
# Event: PreToolUse
# Matcher: tool_name = "Write"
# Files: .coditect/agents/*.md, .coditect/skills/*/SKILL.md, .coditect/commands/*.md
#

set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Read stdin containing hook input JSON
json=$(cat)

# Extract file path from hook input
file_path=$(echo "$json" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

# If we can't parse the JSON or get file path, allow operation
if [[ -z "$file_path" ]]; then
    echo '{"continue": true}'
    exit 0
fi

# Check if this is a component file
if [[ "$file_path" =~ \.coditect/(agents|skills|commands)/.*\.md$ ]]; then
    # Extract new content from hook input
    new_content=$(echo "$json" | jq -r '.tool_input.new_string // empty' 2>/dev/null || echo "")

    # If we can't get content, allow (might be deletion)
    if [[ -z "$new_content" ]]; then
        echo '{"continue": true}'
        exit 0
    fi

    # Run Python validation with the full JSON input
    if python3 "$SCRIPT_DIR/validate_component.py" < <(echo "$json"); then
        # Validation passed
        exit 0
    else
        # Validation failed - exit code from Python script indicates failure
        exit 1
    fi
else
    # Not a component file, allow operation
    echo '{"continue": true}'
    exit 0
fi
