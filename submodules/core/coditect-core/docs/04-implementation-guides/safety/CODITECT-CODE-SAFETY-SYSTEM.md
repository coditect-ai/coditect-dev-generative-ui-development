# CODITECT Code Safety System
## Multi-Repository Automated Backup & Safety Architecture

**Author:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
**Date:** 2025-11-15
**Priority:** CRITICAL
**Status:** Design Complete, Ready for Implementation

---

## Problem Statement

**Current Risk:** With 19+ active repositories, multiple submodules, AI agents working autonomously, and frequent uncommitted changes across many codebases, we face significant risk of code loss due to:

1. **System Shutdown** - Uncommitted changes lost if system shuts down
2. **Human Error** - Forgetting to commit before closing laptop
3. **AI Agent Errors** - Agents creating changes but not committing
4. **Context Switching** - Moving between repos without systematic commits
5. **Submodule Complexity** - Uncommitted changes in nested repositories
6. **Session Continuity** - Lost context when sessions end abruptly

**Impact:** Hours or days of work lost, AI context broken, project momentum disrupted.

---

## Solution Architecture: Multi-Layered Safety System

### Layer 1: Real-Time Monitoring (Every 5 Minutes)
### Layer 2: Pre-Shutdown Hooks (System Events)
### Layer 3: Scheduled Checkpoints (Every 30 Minutes)
### Layer 4: AI Agent Safety (Built-in)
### Layer 5: Manual Safety Commands (User-Triggered)
### Layer 6: Recovery System (Post-Incident)

---

## Layer 1: Real-Time Monitoring System

### Component: `coditect-watcher` Daemon

**Purpose:** Continuously monitor all repositories for uncommitted changes

**Implementation:**

```bash
#!/bin/bash
# /Users/halcasteel/.coditect/daemons/coditect-watcher.sh

WATCH_INTERVAL=300  # 5 minutes
LOG_FILE="$HOME/.coditect/logs/watcher.log"
STATE_FILE="$HOME/.coditect/state/repositories.json"

# Repositories to monitor
REPOS=(
  "$HOME/PROJECTS"
  "$HOME/PROJECTS/coditect-rollout-master"
  "$HOME/PROJECTS/mac-os-systemd-brew-update-controls"
  "$HOME"
)

log() {
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $1" >> "$LOG_FILE"
}

check_repo() {
  local repo="$1"
  cd "$repo" || return

  # Check for uncommitted changes
  if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    log "UNCOMMITTED: $repo has uncommitted changes"
    echo "$repo" >> "$HOME/.coditect/alerts/uncommitted-repos.txt"
    return 1
  fi

  # Check for untracked files
  if [ -n "$(git ls-files --others --exclude-standard)" ]; then
    log "UNTRACKED: $repo has untracked files"
    echo "$repo" >> "$HOME/.coditect/alerts/untracked-repos.txt"
    return 1
  fi

  # Check if ahead of remote
  LOCAL=$(git rev-parse @ 2>/dev/null)
  REMOTE=$(git rev-parse @{u} 2>/dev/null)
  if [ "$LOCAL" != "$REMOTE" ] && [ -n "$REMOTE" ]; then
    log "UNPUSHED: $repo has unpushed commits"
    echo "$repo" >> "$HOME/.coditect/alerts/unpushed-repos.txt"
    return 1
  fi

  return 0
}

check_all_repos() {
  rm -f "$HOME/.coditect/alerts/"*.txt
  mkdir -p "$HOME/.coditect/alerts"

  local clean_count=0
  local dirty_count=0

  for repo in "${REPOS[@]}"; do
    if check_repo "$repo"; then
      ((clean_count++))
    else
      ((dirty_count++))
    fi
  done

  log "Scan complete: $clean_count clean, $dirty_count with changes"

  # Send notification if changes detected
  if [ $dirty_count -gt 0 ]; then
    osascript -e "display notification \"$dirty_count repositories have uncommitted changes\" with title \"CODITECT Safety Alert\""
  fi
}

# Main loop
log "CODITECT Watcher started"
while true; do
  check_all_repos
  sleep $WATCH_INTERVAL
done
```

**launchd Configuration:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.az1.coditect.watcher</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/halcasteel/.coditect/daemons/coditect-watcher.sh</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/halcasteel/.coditect/logs/watcher-stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/halcasteel/.coditect/logs/watcher-stderr.log</string>

    <key>WorkingDirectory</key>
    <string>/Users/halcasteel</string>
</dict>
</plist>
```

**Installation:**

```bash
# Copy plist to LaunchAgents
cp ~/PROJECTS/Scripts/ai.az1.coditect.watcher.plist ~/Library/LaunchAgents/

# Load the daemon
launchctl load ~/Library/LaunchAgents/ai.az1.coditect.watcher.plist

# Verify it's running
launchctl list | grep coditect.watcher
```

---

## Layer 2: Pre-Shutdown Hook System

### Component: `coditect-shutdown-handler`

**Purpose:** Automatically commit and push all changes before system shutdown

**Implementation:**

```bash
#!/bin/bash
# /Users/halcasteel/.coditect/hooks/shutdown-handler.sh

LOG_FILE="$HOME/.coditect/logs/shutdown-handler.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log() {
  echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Repositories to auto-commit on shutdown
REPOS=(
  "$HOME/PROJECTS"
  "$HOME/PROJECTS/coditect-rollout-master"
  "$HOME/PROJECTS/mac-os-systemd-brew-update-controls"
  "$HOME"
)

auto_commit_repo() {
  local repo="$1"
  local repo_name=$(basename "$repo")

  cd "$repo" || return 1

  # Check if git repo
  if [ ! -d ".git" ]; then
    log "SKIP: $repo is not a git repository"
    return 0
  fi

  # Check for changes
  if git diff-index --quiet HEAD -- 2>/dev/null && \
     [ -z "$(git ls-files --others --exclude-standard)" ]; then
    log "CLEAN: $repo has no changes"
    return 0
  fi

  log "COMMITTING: $repo has uncommitted changes"

  # Add all changes
  git add -A

  # Create auto-save commit
  git commit -m "🚨 AUTO-SAVE: Pre-shutdown commit at $TIMESTAMP

This is an automatic safety commit created by CODITECT shutdown handler.
System shutdown was initiated with uncommitted changes.

Repository: $repo_name
Timestamp: $TIMESTAMP
Trigger: System shutdown event

Please review these changes and create a proper commit message
if this auto-save contained meaningful work.

🤖 Generated by CODITECT Code Safety System" 2>&1 | tee -a "$LOG_FILE"

  # Attempt to push (may fail if no remote configured)
  if git push origin HEAD 2>&1 | tee -a "$LOG_FILE"; then
    log "SUCCESS: $repo changes pushed to remote"
  else
    log "WARNING: $repo changes committed locally but not pushed"
  fi

  return 0
}

# Process all repositories
log "=== SHUTDOWN HANDLER STARTED ==="
log "System shutdown detected, processing repositories..."

success_count=0
error_count=0

for repo in "${REPOS[@]}"; do
  if auto_commit_repo "$repo"; then
    ((success_count++))
  else
    ((error_count++))
  fi
done

log "=== SHUTDOWN HANDLER COMPLETE ==="
log "Processed: $success_count successful, $error_count errors"

# Send final notification
osascript -e "display notification \"$success_count repositories auto-saved\" with title \"CODITECT Shutdown Safety\""

exit 0
```

**macOS Shutdown Hook via IOKit:**

```python
#!/usr/bin/env python3
# /Users/halcasteel/.coditect/hooks/iokit-shutdown-listener.py

import subprocess
import os
import sys
import signal
from Foundation import NSObject, NSRunLoop
from AppKit import NSWorkspace, NSWorkspaceWillPowerOffNotification

class ShutdownHandler(NSObject):
    def init(self):
        self = super(ShutdownHandler, self).init()
        if self is None:
            return None

        # Register for shutdown notification
        workspace = NSWorkspace.sharedWorkspace()
        nc = workspace.notificationCenter()
        nc.addObserver_selector_name_object_(
            self,
            'handleShutdown:',
            NSWorkspaceWillPowerOffNotification,
            None
        )

        return self

    def handleShutdown_(self, notification):
        print("Shutdown notification received!")

        # Run shutdown handler script
        script_path = os.path.expanduser('~/.coditect/hooks/shutdown-handler.sh')
        subprocess.call(['/bin/bash', script_path])

def main():
    # Create shutdown handler
    handler = ShutdownHandler.alloc().init()

    # Run event loop
    print("CODITECT Shutdown Listener started...")
    NSRunLoop.currentRunLoop().run()

if __name__ == '__main__':
    main()
```

**launchd Configuration for Shutdown Listener:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.az1.coditect.shutdown-listener</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/halcasteel/.coditect/hooks/iokit-shutdown-listener.py</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/halcasteel/.coditect/logs/shutdown-listener-stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/halcasteel/.coditect/logs/shutdown-listener-stderr.log</string>
</dict>
</plist>
```

---

## Layer 3: Scheduled Checkpoint System

### Component: `coditect-checkpoint` Service

**Purpose:** Create systematic checkpoints every 30 minutes

**Implementation:**

```bash
#!/bin/bash
# /Users/halcasteel/.coditect/daemons/coditect-checkpoint.sh

CHECKPOINT_DIR="$HOME/.coditect/checkpoints"
LOG_FILE="$HOME/.coditect/logs/checkpoint.log"
REPOS_FILE="$HOME/.coditect/config/monitored-repos.txt"

log() {
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $1" >> "$LOG_FILE"
}

create_checkpoint() {
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local checkpoint_id="checkpoint-$timestamp"
  local checkpoint_path="$CHECKPOINT_DIR/$checkpoint_id"

  mkdir -p "$checkpoint_path"

  log "Creating checkpoint: $checkpoint_id"

  # Read monitored repositories
  while IFS= read -r repo; do
    [ -z "$repo" ] && continue
    [ "${repo:0:1}" = "#" ] && continue

    local repo_name=$(basename "$repo")
    cd "$repo" || continue

    # Create diff snapshot
    git diff > "$checkpoint_path/$repo_name.diff" 2>/dev/null
    git diff --cached > "$checkpoint_path/$repo_name-staged.diff" 2>/dev/null

    # Save status
    git status --porcelain > "$checkpoint_path/$repo_name.status" 2>/dev/null

    # Save stash if changes exist
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
      git stash push -m "CODITECT Checkpoint: $timestamp" --include-untracked 2>&1 | tee -a "$LOG_FILE"
      git stash show -p stash@{0} > "$checkpoint_path/$repo_name-stash.diff" 2>/dev/null
      git stash pop 2>&1 | tee -a "$LOG_FILE"
    fi

    log "Checkpoint created for: $repo_name"
  done < "$REPOS_FILE"

  # Cleanup old checkpoints (keep last 48 hours)
  find "$CHECKPOINT_DIR" -type d -name "checkpoint-*" -mtime +2 -exec rm -rf {} \; 2>/dev/null

  log "Checkpoint complete: $checkpoint_id"
}

# Main execution
log "CODITECT Checkpoint service started"
create_checkpoint
```

**launchd Configuration for Scheduled Checkpoints:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.az1.coditect.checkpoint</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/halcasteel/.coditect/daemons/coditect-checkpoint.sh</string>
    </array>

    <key>StartInterval</key>
    <integer>1800</integer> <!-- 30 minutes -->

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/halcasteel/.coditect/logs/checkpoint-stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/halcasteel/.coditect/logs/checkpoint-stderr.log</string>
</dict>
</plist>
```

---

## Layer 4: AI Agent Safety Integration

### Component: `coditect-agent-safety` Module

**Purpose:** Built-in safety for AI agents working autonomously

**Implementation:**

```python
#!/usr/bin/env python3
# /Users/halcasteel/.coditect/lib/agent_safety.py

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

class AgentSafetyModule:
    """Safety module for AI agents to auto-commit changes"""

    def __init__(self, repo_path: str, agent_id: str):
        self.repo_path = Path(repo_path)
        self.agent_id = agent_id
        self.safety_log = Path.home() / '.coditect' / 'logs' / 'agent-safety.log'

    def log(self, message: str):
        """Log safety events"""
        timestamp = datetime.utcnow().isoformat() + 'Z'
        with open(self.safety_log, 'a') as f:
            f.write(f"[{timestamp}] [{self.agent_id}] {message}\n")

    def check_uncommitted_changes(self) -> bool:
        """Check if repository has uncommitted changes"""
        os.chdir(self.repo_path)

        # Check git diff
        result = subprocess.run(
            ['git', 'diff-index', '--quiet', 'HEAD', '--'],
            capture_output=True
        )

        return result.returncode != 0

    def auto_save(self, context: str = ""):
        """Automatically save changes with context"""
        if not self.check_uncommitted_changes():
            self.log("No changes to auto-save")
            return False

        os.chdir(self.repo_path)
        timestamp = datetime.utcnow().isoformat() + 'Z'

        # Stage all changes
        subprocess.run(['git', 'add', '-A'])

        # Create commit message
        commit_msg = f"""🤖 AI AGENT AUTO-SAVE: {timestamp}

Agent: {self.agent_id}
Context: {context or 'Autonomous work in progress'}
Timestamp: {timestamp}

This is an automatic safety commit created by the CODITECT AI Agent.
Changes were committed to prevent loss during autonomous operation.

Please review and potentially squash with a proper commit message.

Generated by CODITECT Agent Safety Module"""

        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            capture_output=True,
            text=True
        )

        self.log(f"Auto-save commit created: {result.stdout}")

        # Attempt push
        push_result = subprocess.run(
            ['git', 'push', 'origin', 'HEAD'],
            capture_output=True,
            text=True
        )

        if push_result.returncode == 0:
            self.log("Auto-save pushed to remote")
        else:
            self.log(f"Auto-save committed locally (push failed): {push_result.stderr}")

        return True

    def create_safety_branch(self, branch_name: str = None):
        """Create a safety branch for risky operations"""
        if not branch_name:
            timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
            branch_name = f"safety/{self.agent_id}/{timestamp}"

        os.chdir(self.repo_path)

        # Create and checkout branch
        subprocess.run(['git', 'checkout', '-b', branch_name])
        self.log(f"Created safety branch: {branch_name}")

        return branch_name

# Example usage in AI agent code:
if __name__ == "__main__":
    # AI Agent initialization
    safety = AgentSafetyModule(
        repo_path="/Users/halcasteel/PROJECTS/coditect-cloud-backend",
        agent_id="backend-agent-001"
    )

    # Before risky operation
    safety.create_safety_branch()

    # ... AI does work ...

    # Periodic auto-save (every 15 minutes or major milestone)
    safety.auto_save(context="Implemented OAuth 2.0 authentication endpoints")
```

---

## Layer 5: Manual Safety Commands

### Component: `coditect` CLI Safety Commands

**Purpose:** User-triggered safety operations

**Implementation:**

```bash
#!/bin/bash
# /Users/halcasteel/.coditect/bin/coditect-safety

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cmd_safety_check() {
  echo "🔍 Checking all repositories for uncommitted changes..."

  python3 << 'EOF'
import subprocess
import os
from pathlib import Path

repos = [
    Path.home() / "PROJECTS",
    Path.home() / "PROJECTS" / "coditect-rollout-master",
    Path.home() / "PROJECTS" / "mac-os-systemd-brew-update-controls",
    Path.home(),
]

for repo in repos:
    if not (repo / ".git").exists():
        continue

    os.chdir(repo)

    # Check status
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True
    )

    if result.stdout.strip():
        print(f"⚠️  {repo.name}: HAS UNCOMMITTED CHANGES")
        print(result.stdout)
    else:
        print(f"✅ {repo.name}: Clean")
EOF
}

cmd_safety_save_all() {
  echo "💾 Auto-saving all repositories..."
  bash "$HOME/.coditect/hooks/shutdown-handler.sh"
}

cmd_safety_checkpoint() {
  echo "📸 Creating checkpoint..."
  bash "$HOME/.coditect/daemons/coditect-checkpoint.sh"
}

cmd_safety_recover() {
  local checkpoint_id="$1"
  echo "🔄 Recovering from checkpoint: $checkpoint_id"

  if [ -z "$checkpoint_id" ]; then
    echo "Available checkpoints:"
    ls -lt "$HOME/.coditect/checkpoints/" | head -10
    return 1
  fi

  local checkpoint_path="$HOME/.coditect/checkpoints/$checkpoint_id"

  if [ ! -d "$checkpoint_path" ]; then
    echo "❌ Checkpoint not found: $checkpoint_id"
    return 1
  fi

  echo "Checkpoint contains:"
  ls -lh "$checkpoint_path"

  echo ""
  echo "To recover:"
  echo "  cd <repository>"
  echo "  git apply $checkpoint_path/<repo>.diff"
}

cmd_safety_status() {
  echo "📊 CODITECT Safety System Status"
  echo ""

  # Check if watcher is running
  if launchctl list | grep -q "ai.az1.coditect.watcher"; then
    echo "✅ Watcher daemon: RUNNING"
  else
    echo "❌ Watcher daemon: NOT RUNNING"
  fi

  # Check if shutdown listener is running
  if launchctl list | grep -q "ai.az1.coditect.shutdown-listener"; then
    echo "✅ Shutdown listener: RUNNING"
  else
    echo "❌ Shutdown listener: NOT RUNNING"
  fi

  # Check if checkpoint service is running
  if launchctl list | grep -q "ai.az1.coditect.checkpoint"; then
    echo "✅ Checkpoint service: RUNNING"
  else
    echo "❌ Checkpoint service: NOT RUNNING"
  fi

  echo ""
  echo "Last checkpoint:"
  ls -lt "$HOME/.coditect/checkpoints/" | head -2 | tail -1

  echo ""
  echo "Recent alerts:"
  tail -5 "$HOME/.coditect/logs/watcher.log" 2>/dev/null || echo "No alerts"
}

# Command router
case "$1" in
  check)
    cmd_safety_check
    ;;
  save-all)
    cmd_safety_save_all
    ;;
  checkpoint)
    cmd_safety_checkpoint
    ;;
  recover)
    cmd_safety_recover "$2"
    ;;
  status)
    cmd_safety_status
    ;;
  *)
    echo "CODITECT Safety System"
    echo ""
    echo "Usage: coditect-safety <command>"
    echo ""
    echo "Commands:"
    echo "  check        - Check all repos for uncommitted changes"
    echo "  save-all     - Auto-save all repositories now"
    echo "  checkpoint   - Create checkpoint now"
    echo "  recover <id> - Recover from checkpoint"
    echo "  status       - Show safety system status"
    ;;
esac
```

---

## Layer 6: Recovery System

### Component: `coditect-recovery` Tools

**Purpose:** Recover lost work from checkpoints and auto-saves

**Implementation:**

```bash
#!/bin/bash
# /Users/halcasteel/.coditect/bin/coditect-recovery

CHECKPOINT_DIR="$HOME/.coditect/checkpoints"
BACKUP_DIR="$HOME/.coditect/backups"

cmd_list_checkpoints() {
  echo "Available checkpoints:"
  ls -lt "$CHECKPOINT_DIR" | grep "^d" | awk '{print $NF}' | head -20
}

cmd_show_checkpoint() {
  local checkpoint_id="$1"
  local checkpoint_path="$CHECKPOINT_DIR/$checkpoint_id"

  if [ ! -d "$checkpoint_path" ]; then
    echo "Checkpoint not found: $checkpoint_id"
    return 1
  fi

  echo "Checkpoint: $checkpoint_id"
  echo "Created: $(stat -f %Sm -t "%Y-%m-%d %H:%M:%S" "$checkpoint_path")"
  echo ""
  echo "Files:"
  ls -lh "$checkpoint_path"
  echo ""
  echo "Repositories with changes:"
  for file in "$checkpoint_path"/*.diff; do
    if [ -f "$file" ] && [ -s "$file" ]; then
      local repo=$(basename "$file" .diff)
      local lines=$(wc -l < "$file")
      echo "  - $repo: $lines lines changed"
    fi
  done
}

cmd_recover_repository() {
  local checkpoint_id="$1"
  local repo_name="$2"
  local checkpoint_path="$CHECKPOINT_DIR/$checkpoint_id"

  if [ ! -d "$checkpoint_path" ]; then
    echo "Checkpoint not found: $checkpoint_id"
    return 1
  fi

  local diff_file="$checkpoint_path/$repo_name.diff"
  local staged_file="$checkpoint_path/$repo_name-staged.diff"

  if [ ! -f "$diff_file" ]; then
    echo "No changes for repository: $repo_name"
    return 1
  fi

  echo "Recovering $repo_name from checkpoint $checkpoint_id"
  echo ""
  echo "Preview of changes:"
  head -50 "$diff_file"
  echo ""
  read -p "Apply these changes? (y/N): " confirm

  if [ "$confirm" = "y" ]; then
    # Find repository
    local repo_path=$(find "$HOME/PROJECTS" -name ".git" -type d | grep "$repo_name" | head -1 | xargs dirname)

    if [ -z "$repo_path" ]; then
      echo "Repository not found: $repo_name"
      return 1
    fi

    cd "$repo_path"

    # Apply diff
    git apply "$diff_file" && echo "✅ Changes applied successfully"

    if [ -f "$staged_file" ] && [ -s "$staged_file" ]; then
      git apply --cached "$staged_file" && echo "✅ Staged changes applied"
    fi
  fi
}

cmd_find_autosaves() {
  local repo_name="$1"

  echo "Searching for auto-save commits in $repo_name..."

  local repo_path=$(find "$HOME/PROJECTS" -name ".git" -type d | grep "$repo_name" | head -1 | xargs dirname)

  if [ -z "$repo_path" ]; then
    echo "Repository not found: $repo_name"
    return 1
  fi

  cd "$repo_path"

  echo "Auto-save commits:"
  git log --all --grep="AUTO-SAVE" --oneline --graph | head -20

  echo ""
  echo "To view a specific auto-save:"
  echo "  git show <commit-hash>"
  echo ""
  echo "To recover an auto-save:"
  echo "  git cherry-pick <commit-hash>"
}

# Command router
case "$1" in
  list)
    cmd_list_checkpoints
    ;;
  show)
    cmd_show_checkpoint "$2"
    ;;
  recover)
    cmd_recover_repository "$2" "$3"
    ;;
  autosaves)
    cmd_find_autosaves "$2"
    ;;
  *)
    echo "CODITECT Recovery System"
    echo ""
    echo "Usage: coditect-recovery <command> [args]"
    echo ""
    echo "Commands:"
    echo "  list                     - List available checkpoints"
    echo "  show <checkpoint-id>     - Show checkpoint details"
    echo "  recover <checkpoint> <repo> - Recover repository from checkpoint"
    echo "  autosaves <repo>         - Find auto-save commits"
    ;;
esac
```

---

## Installation & Setup

### Quick Install Script

```bash
#!/bin/bash
# /Users/halcasteel/PROJECTS/Scripts/install-code-safety-system.sh

echo "🛡️  Installing CODITECT Code Safety System"
echo ""

# Create directory structure
mkdir -p "$HOME/.coditect/"{daemons,hooks,bin,logs,checkpoints,backups,alerts,state,config}

# Create monitored repos config
cat > "$HOME/.coditect/config/monitored-repos.txt" << 'EOF'
# CODITECT Monitored Repositories
# One repository path per line, comments start with #

/Users/halcasteel/PROJECTS
/Users/halcasteel/PROJECTS/coditect-rollout-master
/Users/halcasteel/PROJECTS/mac-os-systemd-brew-update-controls
/Users/halcasteel
EOF

# Copy scripts (assuming they're in PROJECTS/Scripts)
cp ~/PROJECTS/Scripts/coditect-watcher.sh "$HOME/.coditect/daemons/"
cp ~/PROJECTS/Scripts/shutdown-handler.sh "$HOME/.coditect/hooks/"
cp ~/PROJECTS/Scripts/iokit-shutdown-listener.py "$HOME/.coditect/hooks/"
cp ~/PROJECTS/Scripts/coditect-checkpoint.sh "$HOME/.coditect/daemons/"
cp ~/PROJECTS/Scripts/coditect-safety "$HOME/.coditect/bin/"
cp ~/PROJECTS/Scripts/coditect-recovery "$HOME/.coditect/bin/"
cp ~/PROJECTS/Scripts/agent_safety.py "$HOME/.coditect/lib/"

# Make scripts executable
chmod +x "$HOME/.coditect/daemons/"*
chmod +x "$HOME/.coditect/hooks/"*
chmod +x "$HOME/.coditect/bin/"*

# Copy launchd plists
cp ~/PROJECTS/Scripts/ai.az1.coditect.watcher.plist ~/Library/LaunchAgents/
cp ~/PROJECTS/Scripts/ai.az1.coditect.shutdown-listener.plist ~/Library/LaunchAgents/
cp ~/PROJECTS/Scripts/ai.az1.coditect.checkpoint.plist ~/Library/LaunchAgents/

# Load launchd services
echo "Loading services..."
launchctl load ~/Library/LaunchAgents/ai.az1.coditect.watcher.plist
launchctl load ~/Library/LaunchAgents/ai.az1.coditect.shutdown-listener.plist
launchctl load ~/Library/LaunchAgents/ai.az1.coditect.checkpoint.plist

# Add to PATH
if ! grep -q ".coditect/bin" ~/.zshrc; then
  echo 'export PATH="$HOME/.coditect/bin:$PATH"' >> ~/.zshrc
fi

echo ""
echo "✅ CODITECT Code Safety System installed"
echo ""
echo "Services running:"
launchctl list | grep coditect
echo ""
echo "Try these commands:"
echo "  coditect-safety status"
echo "  coditect-safety check"
echo "  coditect-recovery list"
```

---

## Usage Examples

### Developer Workflow

```bash
# Morning: Check status
coditect-safety status

# Before leaving: Save everything
coditect-safety save-all

# After crash: Recover
coditect-recovery list
coditect-recovery show checkpoint-2025-11-15T14:30:00Z
coditect-recovery recover checkpoint-2025-11-15T14:30:00Z coditect-rollout-master
```

### AI Agent Integration

```python
# In AI agent code
from coditect.lib.agent_safety import AgentSafetyModule

# Initialize
safety = AgentSafetyModule(
    repo_path="/Users/halcasteel/PROJECTS/coditect-cloud-backend",
    agent_id="backend-development-agent"
)

# Before risky operation
safety.create_safety_branch("experiment/oauth-refactor")

# After major milestone
safety.auto_save("Completed OAuth 2.0 implementation")

# Every 15 minutes during long-running tasks
while working:
    # ... do work ...
    if time_elapsed % 15_minutes == 0:
        safety.auto_save("Work in progress checkpoint")
```

---

## Monitoring & Alerts

### Dashboard View

```bash
#!/bin/bash
# Quick dashboard

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         CODITECT CODE SAFETY SYSTEM STATUS                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Service status
echo "Services:"
launchctl list | grep coditect | awk '{print "  " $3 " - " ($1 == "-" ? "❌ Stopped" : "✅ Running")}'

echo ""
echo "Repositories:"
cat "$HOME/.coditect/config/monitored-repos.txt" | grep -v "^#" | grep -v "^$" | while read repo; do
  cd "$repo" 2>/dev/null || continue
  if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "  ✅ $(basename $repo): Clean"
  else
    echo "  ⚠️  $(basename $repo): Uncommitted changes"
  fi
done

echo ""
echo "Last checkpoint: $(ls -lt $HOME/.coditect/checkpoints | head -2 | tail -1 | awk '{print $NF}')"
echo "Disk usage: $(du -sh $HOME/.coditect/checkpoints | awk '{print $1}')"
```

---

## Advanced Features

### Integration with CODITECT Dashboard

```go
// Add to ServiceDashboard app.go

func (a *App) GetCodeSafetyStatus() models.SafetyStatus {
    // Check launchd services
    watcherRunning := a.checkService("ai.az1.coditect.watcher")
    checkpointRunning := a.checkService("ai.az1.coditect.checkpoint")
    shutdownRunning := a.checkService("ai.az1.coditect.shutdown-listener")

    // Check for uncommitted changes
    repos := a.getMonitoredRepos()
    uncommittedCount := 0
    for _, repo := range repos {
        if a.hasUncommittedChanges(repo) {
            uncommittedCount++
        }
    }

    return models.SafetyStatus{
        WatcherActive:     watcherRunning,
        CheckpointActive:  checkpointRunning,
        ShutdownActive:    shutdownRunning,
        UncommittedRepos:  uncommittedCount,
        LastCheckpoint:    a.getLastCheckpointTime(),
        DiskUsage:         a.getCheckpointDiskUsage(),
    }
}
```

### Slack/Discord Notifications

```python
# Add to agent_safety.py

def send_alert(self, message: str, severity: str = "warning"):
    """Send alert to Slack/Discord"""
    webhook_url = os.getenv('CODITECT_WEBHOOK_URL')

    if not webhook_url:
        return

    payload = {
        "text": f"🚨 CODITECT Safety Alert",
        "attachments": [{
            "color": "warning" if severity == "warning" else "danger",
            "text": message,
            "footer": f"Agent: {self.agent_id}",
            "ts": int(datetime.utcnow().timestamp())
        }]
    }

    requests.post(webhook_url, json=payload)
```

---

## Testing & Validation

### Test Suite

```bash
#!/bin/bash
# Test the safety system

echo "🧪 Testing CODITECT Code Safety System"

# Test 1: Check services are running
echo "Test 1: Verify services..."
if launchctl list | grep -q coditect.watcher; then
  echo "  ✅ Watcher service running"
else
  echo "  ❌ Watcher service not running"
fi

# Test 2: Create test changes
echo "Test 2: Create test changes..."
cd /tmp
git init test-repo
cd test-repo
echo "test" > test.txt
git add test.txt
git commit -m "initial"
echo "change" >> test.txt

# Test 3: Run safety check
echo "Test 3: Run safety check..."
cd /tmp/test-repo
if "$HOME/.coditect/bin/coditect-safety" check | grep -q "uncommitted"; then
  echo "  ✅ Detected uncommitted changes"
else
  echo "  ❌ Failed to detect changes"
fi

# Test 4: Create checkpoint
echo "Test 4: Create checkpoint..."
"$HOME/.coditect/daemons/coditect-checkpoint.sh"
if [ -d "$HOME/.coditect/checkpoints/checkpoint-$(date -u +%Y-%m-%d)*" ]; then
  echo "  ✅ Checkpoint created"
else
  echo "  ❌ Checkpoint creation failed"
fi

# Cleanup
rm -rf /tmp/test-repo
```

---

## Cost & Performance

**Storage:**
- Checkpoints (48 hours): ~100-500 MB
- Logs (7 days): ~10-50 MB
- Total: <1 GB

**CPU:**
- Watcher (every 5 min): <0.1% CPU
- Checkpoint (every 30 min): <0.5% CPU for 1-2 seconds
- Total impact: Negligible

**Disk I/O:**
- Minimal (only on change detection)

---

## Migration & Rollback

**Enable:**
```bash
bash ~/PROJECTS/Scripts/install-code-safety-system.sh
```

**Disable:**
```bash
launchctl unload ~/Library/LaunchAgents/ai.az1.coditect.*.plist
rm ~/Library/LaunchAgents/ai.az1.coditect.*.plist
```

**Complete Removal:**
```bash
rm -rf ~/.coditect
```

---

## Security Considerations

1. **Credentials:** Never auto-commit files with secrets (.env, credentials.json)
2. **Large Files:** Skip binary files, use git LFS if needed
3. **Permissions:** Scripts run as user, no elevated privileges needed
4. **Network:** Optional remote push, works offline
5. **Privacy:** All data stays local unless pushed to remote

---

## Conclusion

This multi-layered safety system eliminates the risk of code loss during multi-agent, multi-repository development:

✅ **Real-time monitoring** catches uncommitted changes immediately
✅ **Pre-shutdown hooks** auto-save before system powers off
✅ **Scheduled checkpoints** create regular snapshots
✅ **AI agent integration** ensures autonomous work is saved
✅ **Manual commands** give developers control
✅ **Recovery tools** restore lost work from any point

**Result:** Zero risk of losing code, maximum development velocity.

---

**Document Version:** 1.0
**Author:** Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.
**Priority:** CRITICAL - Implement Immediately
**Status:** Design Complete, Ready for Build

---

## Next Steps

1. ⏸️ Create all scripts in PROJECTS/Scripts/
2. ⏸️ Test on single repository
3. ⏸️ Deploy to all repositories
4. ⏸️ Integrate with ServiceDashboard UI
5. ⏸️ Add to CODITECT-BUILDS-CODITECT workflow

---

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**

*Safety First. Code Never Lost.*
