#!/bin/bash
#
# Standards Compliance Validation Hook for CODITECT
#
# Enforces STANDARDS.md compliance for all code changes.
# Prevents modifications that violate architectural decisions.
#
# Event: PreToolUse
# Matcher: tool_name = "Edit"
# Trigger: When editing files
#

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Read stdin containing hook input JSON
json=$(cat)

# Run Python compliance check
python3 "$SCRIPT_DIR/standards_compliance.py" < <(echo "$json")
exit $?
