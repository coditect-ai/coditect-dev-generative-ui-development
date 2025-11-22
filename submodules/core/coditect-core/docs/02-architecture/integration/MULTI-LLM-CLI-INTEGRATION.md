# Multi-LLM CLI Integration Guide

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.**
**Part of the AZ1.AI CODITECT Project Management & Development Platform**

---

## Overview

The AZ1.AI CODITECT framework is **LLM-agnostic** and designed to work with multiple AI coding assistant CLIs through the unified `.claude` → `.coditect` symlink pattern.

### Supported LLM CLIs

| CLI Tool | Provider | Status | Configuration Path |
|----------|----------|--------|-------------------|
| **Claude Code** | Anthropic | ✅ Primary | `.claude/` (symlink) |
| **Gemini Code Assist** | Google | 🚧 Planned | `.gemini/` (symlink) |
| **GitHub Copilot CLI** | GitHub/OpenAI | 🚧 Planned | `.copilot/` (symlink) |
| **Cursor** | Cursor AI | 🚧 Planned | `.cursor/` (symlink) |
| **Grok CLI** | xAI | 🚧 Planned | `.grok/` (symlink) |
| **Cody** | Sourcegraph | 🚧 Planned | `.cody/` (symlink) |

---

## Architecture

### Universal Framework Structure

```
/PROJECTS/
├── .coditect/                    # Master framework (git submodule)
│   ├── AZ1.AI-CODITECT-1-2-3-QUICKSTART.md
│   ├── C4-ARCHITECTURE-METHODOLOGY.md
│   ├── agents/
│   ├── commands/
│   ├── skills/
│   └── ...
│
├── .claude -> .coditect          # Symlink for Claude Code
├── .gemini -> .coditect          # Symlink for Gemini Code Assist
├── .copilot -> .coditect         # Symlink for GitHub Copilot
├── .cursor -> .coditect          # Symlink for Cursor
├── .grok -> .coditect            # Symlink for Grok CLI
├── .cody -> .coditect            # Symlink for Cody
│
└── .gitignore                    # Ignores all symlinks
```

### Why Multiple Symlinks?

**Problem**: Different LLM CLIs look for configuration in different directories.

**Solution**: Create tool-specific symlinks that all point to the same `.coditect` framework.

**Benefits**:
- ✅ Single source of truth (`.coditect`)
- ✅ Multi-tool compatibility
- ✅ No code duplication
- ✅ Easy framework updates (update once, affects all tools)
- ✅ Proper AZ1.AI CODITECT branding

---

## Setup Instructions

### 1. Claude Code (Anthropic)

**Status**: ✅ Currently Active

```bash
cd ~/PROJECTS

# Already configured
ls -l .claude
# Output: .claude -> .coditect
```

**Claude Code Configuration**:
- Detects `.claude/` directory automatically
- Loads agents from `.claude/agents/`
- Loads commands from `.claude/commands/`
- Loads skills from `.claude/skills/`

### 2. Gemini Code Assist (Google)

**Status**: 🚧 Planned

```bash
cd ~/PROJECTS

# Create symlink for Gemini
ln -s .coditect .gemini

# Add to .gitignore
echo ".gemini" >> .gitignore
```

**Gemini Configuration**:
- Install: `npm install -g @google-ai/gemini-code-assist`
- Detects `.gemini/` directory
- Supports custom prompts and workflows

### 3. GitHub Copilot CLI

**Status**: 🚧 Planned

```bash
cd ~/PROJECTS

# Create symlink for Copilot
ln -s .coditect .copilot

# Add to .gitignore
echo ".copilot" >> .gitignore
```

**GitHub Copilot CLI Configuration**:
- Install: `gh extension install github/gh-copilot`
- Custom instructions via `.copilot/`
- Workspace context loading

### 4. Cursor

**Status**: 🚧 Planned

```bash
cd ~/PROJECTS

# Create symlink for Cursor
ln -s .coditect .cursor

# Add to .gitignore
echo ".cursor" >> .gitignore
```

**Cursor Configuration**:
- Install Cursor app from cursor.sh
- Detects `.cursor/` for workspace rules
- Custom AI instructions support

### 5. Grok CLI (xAI)

**Status**: 🚧 Planned

```bash
cd ~/PROJECTS

# Create symlink for Grok
ln -s .coditect .grok

# Add to .gitignore
echo ".grok" >> .gitignore
```

**Grok CLI Configuration** (when available):
- Expected to support workspace configuration
- Custom prompt engineering
- Real-time context

### 6. Cody (Sourcegraph)

**Status**: 🚧 Planned

```bash
cd ~/PROJECTS

# Create symlink for Cody
ln -s .coditect .cody

# Add to .gitignore
echo ".cody" >> .gitignore
```

**Cody Configuration**:
- Install: VSCode extension or JetBrains plugin
- Custom commands via `.cody/`
- Codebase context support

---

## Universal Setup Script

Create a script to set up all LLM CLI symlinks at once:

```bash
#!/bin/bash
# File: ~/PROJECTS/setup-llm-symlinks.sh

# AZ1.AI CODITECT Multi-LLM CLI Setup Script
# Copyright © 2025 AZ1.AI INC. All Rights Reserved.

cd ~/PROJECTS

echo "Setting up AZ1.AI CODITECT multi-LLM CLI integration..."

# List of supported LLM CLIs
LLMS=("claude" "gemini" "copilot" "cursor" "grok" "cody")

# Create symlinks
for llm in "${LLMS[@]}"; do
    if [ -L ".$llm" ]; then
        echo "✓ .$llm symlink already exists"
    else
        ln -s .coditect ."$llm"
        echo "✓ Created .$llm -> .coditect symlink"

        # Add to .gitignore if not already present
        if ! grep -q "^\.$llm\$" .gitignore 2>/dev/null; then
            echo ".$llm" >> .gitignore
            echo "  Added .$llm to .gitignore"
        fi
    fi
done

echo ""
echo "Multi-LLM CLI integration complete!"
echo ""
echo "Supported LLM CLIs:"
echo "  - Claude Code (Anthropic)"
echo "  - Gemini Code Assist (Google)"
echo "  - GitHub Copilot CLI"
echo "  - Cursor"
echo "  - Grok CLI (xAI)"
echo "  - Cody (Sourcegraph)"
echo ""
echo "All tools now have access to the AZ1.AI CODITECT framework."
```

**Usage**:
```bash
chmod +x ~/PROJECTS/setup-llm-symlinks.sh
~/PROJECTS/setup-llm-symlinks.sh
```

---

## Framework Adaptation by LLM CLI

### Claude Code
- ✅ Uses `agents/` directory for specialized agents
- ✅ Uses `commands/` directory for slash commands
- ✅ Uses `skills/` directory for reusable skills
- ✅ Reads `CLAUDE.md` for project context

### Gemini Code Assist
- 🔄 Adapts `agents/` to Gemini "specialists"
- 🔄 Converts `commands/` to Gemini workflows
- 🔄 Uses `skills/` as reusable prompts
- 🔄 Reads framework markdown for context

### GitHub Copilot CLI
- 🔄 Uses framework as custom instructions
- 🔄 Adapts `commands/` to `gh copilot` commands
- 🔄 Uses quickstart as system prompt

### Cursor
- 🔄 Loads `.cursor/` rules for AI behavior
- 🔄 Uses framework for workspace context
- 🔄 Custom instructions from quickstart

### Grok CLI
- 🔄 Real-time context from framework
- 🔄 Custom prompts from agents/
- 🔄 Workflow automation from commands/

### Cody
- 🔄 Custom commands from `commands/`
- 🔄 Codebase context enhanced by framework
- 🔄 Recipe system from `skills/`

---

## LLM CLI Selection Guide

### When to Use Claude Code
- ✅ Best for complex reasoning and planning
- ✅ Excellent long-context understanding
- ✅ Strong architecture design capabilities
- ✅ Currently the most mature integration

### When to Use Gemini Code Assist
- 🔄 Best for Google Cloud integration
- 🔄 Strong multimodal capabilities
- 🔄 Large context window (1M+ tokens)
- 🔄 Good for data analysis tasks

### When to Use GitHub Copilot CLI
- 🔄 Best for GitHub-centric workflows
- 🔄 Excellent autocomplete and suggestions
- 🔄 Good for rapid prototyping
- 🔄 Strong VSCode integration

### When to Use Cursor
- 🔄 Best for full IDE experience
- 🔄 Excellent codebase understanding
- 🔄 Multi-file editing
- 🔄 Good for refactoring tasks

### When to Use Grok CLI
- 🔄 Best for real-time context (when available)
- 🔄 X (Twitter) data integration
- 🔄 Fast iteration speed
- 🔄 Good for current events context

### When to Use Cody
- 🔄 Best for enterprise codebases
- 🔄 Excellent code search
- 🔄 Cross-repository understanding
- 🔄 Good for large monorepos

---

## Configuration Files

### Universal `.gitignore` Entry

Add to `~/PROJECTS/.gitignore`:

```gitignore
# LLM CLI symlinks (all point to .coditect)
.claude
.gemini
.copilot
.cursor
.grok
.cody
```

### Per-Tool API Keys

Store API keys securely (never commit to git):

```bash
# Claude Code (Anthropic)
export ANTHROPIC_API_KEY="sk-ant-..."

# Gemini Code Assist (Google)
export GEMINI_API_KEY="AIza..."

# GitHub Copilot (via GitHub)
# Uses GitHub authentication

# Cursor
# Built into app, or:
export CURSOR_API_KEY="..."

# Grok CLI (when available)
export XAI_API_KEY="xai-..."

# Cody (Sourcegraph)
export SRC_ACCESS_TOKEN="sgp_..."
```

**Recommended**: Use macOS Keychain or environment variables, never plaintext files.

---

## Integration Checklist

### For Early Adopters

- [x] **Claude Code** - Primary LLM CLI (Active)
- [ ] **Gemini Code Assist** - Google AI integration (Planned)
- [ ] **GitHub Copilot CLI** - GitHub workflows (Planned)
- [ ] **Cursor** - IDE experience (Planned)
- [ ] **Grok CLI** - xAI integration (Planned)
- [ ] **Cody** - Enterprise code search (Planned)

### For Each LLM CLI

1. **Installation**
   - [ ] Install CLI tool
   - [ ] Configure API keys
   - [ ] Verify installation

2. **Framework Integration**
   - [ ] Create symlink to `.coditect`
   - [ ] Add to `.gitignore`
   - [ ] Test framework access

3. **Testing**
   - [ ] Test framework loading
   - [ ] Verify agent/command access
   - [ ] Confirm workflow compatibility

4. **Documentation**
   - [ ] Update this guide with findings
   - [ ] Document tool-specific quirks
   - [ ] Share best practices

---

## Best Practices

### 1. Choose the Right Tool for the Task

Don't use the same LLM CLI for everything:
- **Architecture design** → Claude Code (superior reasoning)
- **Quick autocomplete** → GitHub Copilot (fast suggestions)
- **Codebase exploration** → Cody (excellent search)
- **Multi-file refactoring** → Cursor (IDE integration)

### 2. Keep Framework Updated

```bash
cd ~/PROJECTS
git submodule update --remote .coditect

# All LLM CLIs now have the latest framework
```

### 3. Use Consistent Patterns

All LLM CLIs should:
- Follow the AZ1.AI CODITECT 1-2-3 Quickstart process
- Use C4 Model for architecture
- Apply 6-step issue resolution
- Reference framework documentation

### 4. API Key Management

```bash
# Good: Environment variables
export ANTHROPIC_API_KEY="$(cat ~/.anthropic-key)"

# Good: macOS Keychain
security find-generic-password -s "anthropic-api-key" -w

# Bad: Hardcoded in files
# NEVER: API_KEY="sk-ant-..." in .zshrc or config files
```

---

## Troubleshooting

### Symlink Not Detected

**Problem**: LLM CLI doesn't see the `.coditect` framework

**Solution**:
```bash
cd ~/PROJECTS

# Check symlink
ls -la | grep -E "\.(claude|gemini|copilot|cursor|grok|cody)"

# Recreate if broken
rm .claude  # or whichever tool
ln -s .coditect .claude
```

### Framework Not Loading

**Problem**: LLM CLI loads but framework features don't work

**Solution**:
```bash
# Verify submodule is populated
ls -la .coditect/

# If empty, initialize submodule
git submodule update --init --recursive
```

### Multiple CLI Conflicts

**Problem**: Two LLM CLIs interfere with each other

**Solution**: Use one tool at a time per session, or use separate terminal windows

---

## Roadmap

### Phase 1: Claude Code (Current)
- ✅ Full integration
- ✅ 50+ agents
- ✅ 72+ commands
- ✅ 189 skills

### Phase 2: Gemini Code Assist (Q1 2025)
- 🔄 Symlink setup
- 🔄 Framework adaptation
- 🔄 Testing with early adopters
- 🔄 Documentation updates

### Phase 3: Additional CLIs (Q2 2025)
- 🔄 GitHub Copilot CLI integration
- 🔄 Cursor workspace rules
- 🔄 Cody custom commands
- 🔄 Grok CLI (when available)

### Phase 4: Unified CLI (Q3 2025)
- 🔄 AZ1.AI CODITECT CLI wrapper
- 🔄 Auto-detect and route to best LLM
- 🔄 Unified command interface
- 🔄 Multi-LLM orchestration

---

## Contributing

### Testing New LLM CLIs

If you want to test a new LLM CLI with the AZ1.AI CODITECT framework:

1. Create symlink: `ln -s .coditect .newtool`
2. Test framework access
3. Document findings in this file
4. Submit pull request to https://github.com/coditect-ai/coditect-core

### Reporting Issues

Found a problem with multi-LLM integration?

1. Check symlinks are correct
2. Verify .coditect submodule is up to date
3. Test with Claude Code (known working)
4. Document the issue
5. Report via GitHub Issues

---

## Copyright Notice

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**

This Multi-LLM CLI Integration Guide is proprietary to AZ1.AI INC. and is part of the AZ1.AI CODITECT Project Management & Development Platform.

**Developed by**: Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.

**Authorized for use by**: AZ1.AI team members, early adopters, and affiliates during pilot testing phase.

**Unauthorized reproduction, distribution, or use is prohibited.**

---

**Built with Excellence by AZ1.AI CODITECT**

*One framework, multiple AI assistants, infinite possibilities.*

**AZ1.AI INC.**
Founded 2025
Innovation Through Systematic Development
