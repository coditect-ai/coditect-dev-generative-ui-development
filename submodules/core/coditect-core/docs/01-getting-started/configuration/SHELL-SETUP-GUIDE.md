# CODITECT Shell Setup Guide

**Quick shell configuration for instant CODITECT AI Router access**

---

## 🎯 What This Sets Up

Add convenient aliases to your shell so you can type:
- `cr "your request"` instead of the full path
- `cri` for interactive mode
- Works from **any directory** on your system

---

## 📋 One-Time Setup (5 minutes)

### Step 1: Add Aliases to Your Shell

**For ZSH (macOS default, Oh My Zsh):**

```bash
cat >> ~/.zshrc << 'EOF'

# =============================================================================
# CODITECT AI Command Router
# =============================================================================
# Never memorize 72 slash commands - just describe what you want in plain English!
# Usage: cr "I need to add user authentication"
#        cri  (interactive mode - ask multiple questions)

# Determine CODITECT location (works from anywhere)
if [[ -d "$HOME/PROJECTS/coditect-rollout-master/.coditect" ]]; then
    # Master rollout project
    export CODITECT_ROUTER="$HOME/PROJECTS/coditect-rollout-master/.coditect/scripts/coditect-router"
elif [[ -d "$HOME/.coditect" ]]; then
    # Global installation
    export CODITECT_ROUTER="$HOME/.coditect/scripts/coditect-router"
elif [[ -d "$(pwd)/.coditect" ]]; then
    # Current project
    export CODITECT_ROUTER="$(pwd)/.coditect/scripts/coditect-router"
fi

# Create aliases if router found
if [[ -n "$CODITECT_ROUTER" && -x "$CODITECT_ROUTER" ]]; then
    alias cr='$CODITECT_ROUTER'
    alias cri='$CODITECT_ROUTER -i'
    alias coditect-router='$CODITECT_ROUTER'
fi

# End of CODITECT AI Command Router
# =============================================================================
EOF
```

**For Bash (Linux, older macOS):**

```bash
cat >> ~/.bashrc << 'EOF'

# =============================================================================
# CODITECT AI Command Router
# =============================================================================
# Never memorize 72 slash commands - just describe what you want in plain English!
# Usage: cr "I need to add user authentication"
#        cri  (interactive mode - ask multiple questions)

# Determine CODITECT location (works from anywhere)
if [[ -d "$HOME/PROJECTS/coditect-rollout-master/.coditect" ]]; then
    # Master rollout project
    export CODITECT_ROUTER="$HOME/PROJECTS/coditect-rollout-master/.coditect/scripts/coditect-router"
elif [[ -d "$HOME/.coditect" ]]; then
    # Global installation
    export CODITECT_ROUTER="$HOME/.coditect/scripts/coditect-router"
elif [[ -d "$(pwd)/.coditect" ]]; then
    # Current project
    export CODITECT_ROUTER="$(pwd)/.coditect/scripts/coditect-router"
fi

# Create aliases if router found
if [[ -n "$CODITECT_ROUTER" && -x "$CODITECT_ROUTER" ]]; then
    alias cr='$CODITECT_ROUTER'
    alias cri='$CODITECT_ROUTER -i'
    alias coditect-router='$CODITECT_ROUTER'
fi

# End of CODITECT AI Command Router
# =============================================================================
EOF
```

### Step 2: Reload Your Shell Configuration

**ZSH:**
```bash
source ~/.zshrc
```

**Bash:**
```bash
source ~/.bashrc
```

### Step 3: Verify Aliases Work

```bash
# Test that aliases are loaded
which cr
which cri

# Should output:
# cr: aliased to $CODITECT_ROUTER
# cri: aliased to $CODITECT_ROUTER -i
```

---

## 🚀 Usage

### Basic Command Selection

```bash
cr "I need to add user authentication"
```

Output:
```
🤖 CODITECT AI Command Router
======================================================================

📍 RECOMMENDED COMMAND: /implement
   Description: Production-ready implementation mode
   Purpose: Build production code with error handling

💭 REASONING:
   Detected implementation request (keywords: add, authentication)

🔄 ALTERNATIVES:
   • /prototype: Rapid prototyping mode
   • /feature_development: End-to-end feature workflow

📋 NEXT STEPS:
   1. Use /implement for production-ready code
   2. Include error handling and security hardening

💻 USAGE:
   Type in Claude Code: /implement
```

### Interactive Mode (Recommended)

```bash
cri
```

Then ask multiple questions:
```
📝 What do you want to do? > fix a bug
📝 What do you want to do? > add tests
📝 What do you want to do? > create documentation
📝 What do you want to do? > quit
```

### Examples by Scenario

**Implementation:**
```bash
cr "build a REST API endpoint"
cr "add user registration feature"
cr "create a new React component"
```

**Debugging:**
```bash
cr "fix a bug in payment processing"
cr "my app is crashing on startup"
cr "debug authentication errors"
```

**Planning:**
```bash
cr "plan a new feature"
cr "design system architecture"
cr "create project roadmap"
```

**Testing:**
```bash
cr "generate unit tests"
cr "add integration tests"
cr "test coverage analysis"
```

**Documentation:**
```bash
cr "create API documentation"
cr "write a README"
cr "document the architecture"
```

---

## ⚡ Two Modes

### Heuristic Mode (Default - Works Immediately)

- ✅ No setup required
- ✅ Uses intelligent keyword pattern matching
- ✅ Fast and reliable
- ✅ Good for common scenarios
- ✅ **Always available as fallback**

### AI-Powered Mode (Optional - For Complex Requests)

**Setup:**

Add to your shell configuration (~/.zshrc or ~/.bashrc):

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Benefits:**
- 🧠 Deep understanding of context and nuance
- 🎯 Better handling of complex, multi-step requests
- 📝 More detailed reasoning and explanations
- 🔄 Smarter alternative suggestions

**Get Your API Key:**
1. Sign up at https://console.anthropic.com/
2. Navigate to API Keys section
3. Create a new API key
4. Add to your shell config as shown above
5. Reload: `source ~/.zshrc` (or `source ~/.bashrc`)

---

## 🛠️ Troubleshooting

### Alias Not Found

**Problem:** `command not found: cr`

**Solution:**
```bash
# Reload your shell configuration
source ~/.zshrc  # or source ~/.bashrc

# Verify the router path is set
echo $CODITECT_ROUTER

# If empty, make sure CODITECT is installed at one of these locations:
# - $HOME/PROJECTS/coditect-rollout-master/.coditect
# - $HOME/.coditect
# - $(pwd)/.coditect
```

### Router Script Not Executable

**Problem:** `Permission denied`

**Solution:**
```bash
chmod +x ~/.coditect/scripts/coditect-router
chmod +x ~/.coditect/scripts/coditect-command-router.py
```

### Python Import Errors

**Problem:** `ModuleNotFoundError: No module named 'anthropic'`

**This is normal!** The router works in heuristic mode without the `anthropic` package. To enable AI mode:

```bash
pip install anthropic
```

### AI Mode Not Working

**Problem:** Router falls back to heuristic mode even with API key set

**Check:**
```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# If empty, add to ~/.zshrc or ~/.bashrc:
export ANTHROPIC_API_KEY="your-key"

# Reload shell
source ~/.zshrc
```

---

## 📚 Advanced Configuration

### Custom Installation Path

If CODITECT is installed in a custom location:

```bash
# Add to ~/.zshrc or ~/.bashrc
export CODITECT_ROUTER="/path/to/your/.coditect/scripts/coditect-router"
alias cr='$CODITECT_ROUTER'
alias cri='$CODITECT_ROUTER -i'
```

### Multiple CODITECT Projects

The auto-detection checks in this order:
1. `$HOME/PROJECTS/coditect-rollout-master/.coditect` (master project)
2. `$HOME/.coditect` (global installation)
3. `$(pwd)/.coditect` (current directory)

To force a specific path, set `CODITECT_ROUTER` explicitly.

### Custom Aliases

Prefer different names? Customize:

```bash
# Short aliases
alias c='$CODITECT_ROUTER'
alias ci='$CODITECT_ROUTER -i'

# Descriptive aliases
alias command-help='$CODITECT_ROUTER'
alias ai-router='$CODITECT_ROUTER'

# Context-specific
alias coditect='$CODITECT_ROUTER'
alias slash='$CODITECT_ROUTER'
```

---

## 🎓 Learning More

**Full Documentation:**
- [1-2-3-SLASH-COMMAND-QUICK-START.md](../quick-starts/1-2-3-SLASH-COMMAND-QUICK-START.md) - Complete slash command guide
- [SLASH-COMMANDS-REFERENCE.md](docs/SLASH-COMMANDS-REFERENCE.md) - All 72 commands catalog
- [scripts/README.md](../../../scripts/README.md) - Router implementation details

**Training Materials:**
- [user-training/README.md](user-training/README.md) - CODITECT Operator training
- [user-training/1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md](user-training/1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md) - Quick start guide

---

## ✅ Quick Verification Checklist

After setup, verify everything works:

- [ ] Aliases loaded: `which cr` shows alias definition
- [ ] Router executable: `$CODITECT_ROUTER --help` works
- [ ] Heuristic mode: `cr "test"` returns command suggestion
- [ ] (Optional) AI mode: `cr "complex request"` uses Claude AI
- [ ] Interactive mode: `cri` starts interactive session

---

**Status:** One-time setup complete! You can now use `cr` from any directory.

**Support:** See [TROUBLESHOOTING-GUIDE.md](user-training/CODITECT-TROUBLESHOOTING-GUIDE.md) for issues.
