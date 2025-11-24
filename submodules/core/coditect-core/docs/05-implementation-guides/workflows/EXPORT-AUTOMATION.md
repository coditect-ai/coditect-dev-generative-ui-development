# CODITECT Context Export Automation

**Version:** 1.0
**Date:** 2025-11-16
**Status:** Production Ready

## Overview

The CODITECT export automation system provides a standardized way to export Claude Code conversation context with ISO-DATETIME naming conventions. This enables consistent MEMORY-CONTEXT management across all projects.

## Quick Start

### Simple Usage

```bash
# From any CODITECT project with .coditect symlink
.coditect/scripts/export-context.sh

# With custom description
.coditect/scripts/export-context.sh "Sprint Planning Session"
```

### Using the EXPORT Command

```bash
# From coditect-core
./commands/export

# With description
./commands/export "MEMORY-CONTEXT Implementation Complete"
```

## What It Does

1. **Generates ISO-DATETIME Timestamp** - Format: `YYYY-MM-DDTHH-MM-SSZ`
2. **Creates Export Directory** - `MEMORY-CONTEXT/exports/`
3. **Generates Filename** - `TIMESTAMP-description.txt`
4. **Creates Placeholder File** - Pre-formatted for /export command
5. **Creates Symlink** - `latest-export.txt` points to newest export
6. **Provides Instructions** - Step-by-step guide for completing export

## File Naming Convention

**Format:** `YYYY-MM-DDTHH-MM-SSZ-description.txt`

**Examples:**
- `2025-11-16T10-30-00Z-EXPORT-CONTEXT.txt` (no description)
- `2025-11-16T14-45-30Z-Sprint-Planning-Session.txt`
- `2025-11-16T16-20-15Z-MEMORY-CONTEXT-Implementation-Complete.txt`

**Rules:**
- Timestamp is in UTC (Z = Zulu time)
- Description is sanitized (spaces → hyphens, special chars removed)
- Extension is always `.txt`

## Directory Structure

```
MEMORY-CONTEXT/
└── exports/
    ├── 2025-11-16T10-30-00Z-EXPORT-CONTEXT.txt
    ├── 2025-11-16T14-45-30Z-Sprint-Planning-Session.txt
    ├── 2025-11-16T16-20-15Z-MEMORY-CONTEXT-Implementation.txt
    └── latest-export.txt → 2025-11-16T16-20-15Z-MEMORY-CONTEXT-Implementation.txt
```

## Usage Guide

### Step 1: Run Export Script

```bash
.coditect/scripts/export-context.sh "Your Description Here"
```

**Output:**
```
═══════════════════════════════════════════════════════════════
  CODITECT Context Export Automation
═══════════════════════════════════════════════════════════════

📋 Description: Your Description Here
🕐 Timestamp: 2025-11-16T10-45-32Z
📁 Output File: 2025-11-16T10-45-32Z-Your-Description-Here.txt
📂 Directory: /path/to/MEMORY-CONTEXT/exports

⚠️  This script will prepare the export file location.
    You need to manually run the /export command in Claude Code.

Please run the following command in Claude Code:

    /export

When prompted for the file path, use:

    /path/to/MEMORY-CONTEXT/exports/2025-11-16T10-45-32Z-Your-Description-Here.txt

✅ Export placeholder created
```

### Step 2: Run /export in Claude Code

In your Claude Code session, type:

```
/export
```

### Step 3: Save to Provided Path

When prompted, paste the file path provided by the script:

```
/path/to/MEMORY-CONTEXT/exports/2025-11-16T10-45-32Z-Your-Description-Here.txt
```

### Step 4: Commit to Git (Optional)

```bash
git add MEMORY-CONTEXT/exports/2025-11-16T10-45-32Z-Your-Description-Here.txt
git commit -m "Add context export: Your Description Here"
git push
```

## Use Cases

### 1. End of Session Export

```bash
.coditect/scripts/export-context.sh "Session Complete - Sprint Planning"
```

**When to use:**
- End of development session
- Before switching contexts
- After completing major tasks
- For MEMORY-CONTEXT continuity

### 2. Checkpoint Export

```bash
.coditect/scripts/export-context.sh "Checkpoint - Phase 1 Complete"
```

**When to use:**
- After creating checkpoint
- Phase gate completions
- Milestone achievements
- Sprint completions

### 3. Documentation Export

```bash
.coditect/scripts/export-context.sh "Architecture Documentation Sprint"
```

**When to use:**
- Capturing design decisions
- Documenting architecture choices
- Recording technical discussions
- Knowledge transfer sessions

### 4. Debug/Troubleshooting Export

```bash
.coditect/scripts/export-context.sh "Debug Session - API Performance Issue"
```

**When to use:**
- Debugging complex issues
- Performance troubleshooting
- Error investigation
- Root cause analysis

## Integration with MEMORY-CONTEXT

The export automation is designed to work seamlessly with the MEMORY-CONTEXT system:

### Session Export Flow

1. **Export Script Creates Placeholder**
   - Generates ISO-DATETIME filename
   - Creates directory structure
   - Sets up symlink to latest

2. **User Runs /export Command**
   - Saves conversation to prepared location
   - Includes all context, code, decisions

3. **MEMORY-CONTEXT Processes Export**
   - Session export engine reads file
   - Privacy controls applied
   - PII detection and redaction
   - Pattern extraction via NESTED LEARNING

4. **Context Available for Next Session**
   - Context loader can retrieve export
   - Relevance scoring applied
   - Token optimization used
   - Seamless session continuity

### Workflow Integration

```
Development Session
      ↓
  Checkpoint Created
      ↓
  Export Script Run
      ↓
  /export Command
      ↓
  File Saved
      ↓
  MEMORY-CONTEXT Processing
      ↓
  Context Available for Next Session
```

## Advanced Usage

### Scripting and Automation

The export script returns the filepath, enabling scripting:

```bash
# Capture filepath for further processing
EXPORT_PATH=$(./coditect/scripts/export-context.sh "Automated Export")

# Use in other scripts
echo "Export saved to: $EXPORT_PATH"

# Trigger post-export processing
python3 process-export.py "$EXPORT_PATH"
```

### Integration with Checkpoint Script

The checkpoint script can call the export script:

```python
import subprocess

def create_checkpoint_with_export(description):
    # Create checkpoint
    checkpoint_path = create_checkpoint(description)

    # Prepare export
    export_path = subprocess.check_output([
        '.coditect/scripts/export-context.sh',
        description
    ]).decode().strip()

    print(f"Checkpoint: {checkpoint_path}")
    print(f"Export ready: {export_path}")
    print("Please run /export in Claude Code")

    return checkpoint_path, export_path
```

### Batch Export Management

```bash
# List all exports
ls -lh .coditect/MEMORY-CONTEXT/exports/

# Find exports by date
ls .coditect/MEMORY-CONTEXT/exports/2025-11-16*.txt

# Find exports by description
ls .coditect/MEMORY-CONTEXT/exports/*Sprint*.txt

# View latest export
cat .coditect/MEMORY-CONTEXT/exports/latest-export.txt
```

## Distributed Intelligence Benefits

### Available Across All Submodules

Every submodule with `.coditect` symlink can use export automation:

```bash
# From coditect-cloud-backend
cd /path/to/coditect-cloud-backend
.coditect/scripts/export-context.sh "Backend API Implementation"

# From coditect-cloud-frontend
cd /path/to/coditect-cloud-frontend
.coditect/scripts/export-context.sh "Frontend Component Development"

# From coditect-cli
cd /path/to/coditect-cli
.coditect/scripts/export-context.sh "CLI Command Implementation"
```

### Cross-Project Context

Exports from different submodules share the same format:

- **Consistent naming** - ISO-DATETIME across all projects
- **Unified storage** - All in MEMORY-CONTEXT/exports/
- **Cross-project patterns** - NESTED LEARNING can identify patterns across projects
- **Team knowledge sharing** - Privacy controls enable team-level sharing

## Best Practices

### 1. Descriptive Names

✅ **Good:**
```bash
.coditect/scripts/export-context.sh "API Authentication Implementation"
.coditect/scripts/export-context.sh "Database Schema Migration Sprint"
.coditect/scripts/export-context.sh "Bug Fix - Login Token Expiry"
```

❌ **Bad:**
```bash
.coditect/scripts/export-context.sh "export"
.coditect/scripts/export-context.sh "test"
.coditect/scripts/export-context.sh "abc"
```

### 2. Regular Exports

- **End of each session** - Capture decisions and progress
- **After major changes** - Document significant code changes
- **Before context switch** - Save state before switching tasks
- **Milestone completions** - Record achievements

### 3. Git Integration

Always commit exports to preserve history:

```bash
# After completing export
git add MEMORY-CONTEXT/exports/
git commit -m "Add session export: [description]"
git push
```

### 4. Privacy Considerations

Be mindful of what's in the export:

- **Remove sensitive data** - API keys, credentials, PII
- **Use privacy controls** - Apply appropriate privacy level
- **Review before sharing** - Check content before team sharing
- **Follow compliance** - GDPR, CCPA, company policies

## Troubleshooting

### Export Directory Not Created

**Problem:** `MEMORY-CONTEXT/exports/` directory doesn't exist

**Solution:**
```bash
mkdir -p .coditect/MEMORY-CONTEXT/exports
```

### Permission Denied

**Problem:** Script not executable

**Solution:**
```bash
chmod +x .coditect/scripts/export-context.sh
```

### Symlink Not Created

**Problem:** `latest-export.txt` symlink failed

**Solution:**
```bash
cd .coditect/MEMORY-CONTEXT/exports
ln -sf [filename].txt latest-export.txt
```

### /export Command Not Found

**Problem:** Claude Code doesn't recognize /export

**Solution:**
- Ensure you're in Claude Code (not regular terminal)
- Check Claude Code version supports /export
- Try typing /help to see available commands

## Technical Details

### Script Location

- **Primary:** `coditect-core/scripts/export-context.sh`
- **Available via symlink:** Any project with `.coditect → ../../.coditect`

### Dependencies

- **bash** - Standard shell (macOS/Linux)
- **date** - ISO-DATETIME formatting (GNU coreutils)
- **git** (optional) - For git integration features

### Exit Codes

- **0** - Success (placeholder created)
- **1** - Error (directory creation failed, etc.)

### Environment Variables

None required. Script auto-detects:
- Script directory
- Base directory
- Git repository status

## Future Enhancements

### Planned Features (Sprint +1)

- [ ] **Automatic /export trigger** - Integrate with Claude Code API
- [ ] **Post-export processing** - Automatic MEMORY-CONTEXT ingestion
- [ ] **Privacy scanning** - Pre-export PII detection
- [ ] **Compression** - Automatic gzip for large exports
- [ ] **Cloud backup** - Optional S3/GCS upload
- [ ] **Metadata extraction** - Parse and index export metadata

### Long-term Vision

- **AI-powered summaries** - Automatic export summarization
- **Smart retention** - Automatic archival of old exports
- **Cross-project search** - Search all exports across projects
- **Context recommendations** - Suggest relevant past exports
- **Team dashboards** - Visualize team export patterns

## Related Documentation

- [MEMORY-CONTEXT Architecture](MEMORY-CONTEXT-ARCHITECTURE.md)
- [NESTED LEARNING Guide](NESTED-LEARNING-GUIDE.md)
- [Privacy Controls Specification](PRIVACY-CONTROLS-SPEC.md)
- [Checkpoint Creation Guide](../scripts/create-checkpoint.py)

## Support

For issues or questions:
- **Documentation:** Check this guide and related docs
- **Issues:** Report at GitHub repository
- **Contact:** CODITECT team via appropriate channels

---

**Maintained by:** AZ1.AI CODITECT Team
**Last Updated:** 2025-11-16
**Status:** Production Ready
**Version:** 1.0
