# Hooks Directory

This directory can contain pre/post execution hooks for Claude Code.

## Hook Types

Hooks are executable shell scripts that run before/after tool invocations:

### Pre-Tool Hooks
- `pre-bash.sh` - Run before Bash commands
- `pre-write.sh` - Run before file writes
- `pre-edit.sh` - Run before file edits

### Post-Tool Hooks
- `post-bash.sh` - Run after Bash commands
- `post-write.sh` - Run after file writes
- `post-git.sh` - Run after git operations

## Example Use Cases

For t2 project:
- **pre-write**: Validate file paths, check permissions
- **post-edit**: Run formatters, update checksums
- **post-git**: Trigger file-monitor logs, update FDB

## Hook Environment

Hooks receive context via environment variables:
- `$TOOL_NAME` - Tool being executed
- `$FILE_PATH` - File being operated on (if applicable)
- `$COMMAND` - Full command being run

## Safety

Hooks should be:
- ✅ Fast (< 1 second)
- ✅ Idempotent
- ✅ Error-tolerant
- ❌ Never blocking or interactive

## References

- Claude Code hooks documentation
- coditect-v4/.codi/scripts/ for monitoring examples
