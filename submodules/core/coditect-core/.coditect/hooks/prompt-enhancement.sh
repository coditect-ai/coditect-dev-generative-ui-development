#!/bin/bash
#
# Prompt Enhancement Hook for CODITECT
#
# Automatically enhances user prompts with relevant CODITECT context
# before Claude processes them, providing intelligent context without duplication.
#
# Event: UserPromptSubmit
# Matcher: {} (all prompts)
#

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Read stdin containing hook input JSON
json=$(cat)

# Run Python enhancement
python3 "$SCRIPT_DIR/enhance_prompt.py" < <(echo "$json")
exit $?
