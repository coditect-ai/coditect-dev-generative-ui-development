---
name: suggest-agent
description: Generate correct agent invocation syntax for any request
---

# Suggest Agent - Smart Invocation Generator

Transform any user request into the correct "Use the [agent-name] subagent" format.

## Usage
```
/suggest-agent [describe what you want to do]
```

## System Behavior

When this command is used, Claude will:

1. **Analyze your request** to understand the task domain and complexity
2. **Select the best agent(s)** from our 46-agent framework
3. **Generate the exact invocation syntax** you should use
4. **Provide a brief explanation** of why this agent is optimal

## Quick Agent Reference

**🔍 Research & Analysis**
- `competitive-market-analyst` - Market research, pricing, competitor analysis
- `web-search-researcher` - External information gathering, documentation research  
- `thoughts-analyzer` - Analyze existing research documents
- `codebase-analyzer` - Understand HOW code works
- `codebase-locator` - Find WHERE code/files are located

**🛠️ Development**
- `rust-expert-developer` - Rust backend development
- `frontend-react-typescript-expert` - React/TypeScript UI development
- `orchestrator` - Complex multi-step workflows, full-stack features

**💾 Database & Infrastructure**
- `foundationdb-expert` - FoundationDB schema design
- `cloud-architect` - Deployment, CI/CD, infrastructure

**🔍 Quality & Testing**
- `testing-specialist` - Test coverage, TDD, quality gates
- `security-specialist` - Security audits, vulnerability assessment
- `qa-reviewer` - Documentation quality review

## Example Outputs

### Input: "I want to research Cursor's pricing strategy"
**Output:**
```
Use the competitive-market-analyst subagent to research Cursor's pricing strategy, analyze their tier structure, and identify market positioning approaches
```
*Why: Market research specialist with web search capabilities*

### Input: "Find all authentication-related files"
**Output:**
```
Use the codebase-locator subagent to find all authentication-related files including handlers, middleware, and configuration
```
*Why: Specialized in file discovery and code location*

### Input: "Implement user profile editing feature"
**Output:**
```
Use the orchestrator subagent to implement user profile editing with backend API endpoints, frontend React components, and comprehensive testing
```
*Why: Complex full-stack feature requiring coordination of multiple specialists*

### Input: "Understand how session management works"
**Output:**
```
Use the codebase-analyzer subagent to understand session management implementation, data flow, and authentication patterns
```
*Why: Specialized in analyzing existing code implementation*

### Input: "Research AI IDE market trends and analyze our current features"
**Output:**
```
Use the competitive-market-analyst subagent to research AI IDE market trends while having the codebase-analyzer subagent review our current feature implementation
```
*Why: Multi-agent coordination for external research + internal analysis*

## Command Integration

This works with your existing workflow:

```bash
# Step 1: Get the right invocation
/suggest-agent "optimize database performance"

# Step 2: Use the suggested output directly
"Use the foundationdb-expert subagent to analyze and optimize database performance including query patterns and schema efficiency"

# Step 3: Agent executes with proper specialization
```

## Pattern Recognition

The system recognizes these request patterns:

- **"Research [topic]"** → `competitive-market-analyst`
- **"Find [files/code]"** → `codebase-locator` 
- **"Understand [implementation]"** → `codebase-analyzer`
- **"Implement [feature]"** → Domain specialist + `orchestrator`
- **"Fix [bug]"** → Relevant domain specialist
- **"Review [code/docs]"** → `qa-reviewer` or domain specialist
- **"Design [architecture]"** → `senior-architect`
- **"Analyze [existing work]"** → `thoughts-analyzer`

## Multi-Agent Patterns

For complex requests, generates coordinated invocations:

```bash
# Parallel execution
"Use the [agent-1] subagent to [task-1] while having the [agent-2] subagent [task-2]"

# Sequential with handoff
"Use the [agent-1] subagent to [task-1], then use the [agent-2] subagent to [task-2]"

# Orchestrated workflow
"Use the orchestrator subagent to [coordinate complex multi-step task]"
```

## Tips for Best Results

1. **Be specific** about what you want to accomplish
2. **Mention the domain** if it's not obvious (backend, frontend, research, etc.)
3. **Indicate complexity** if it's a multi-step process
4. **Specify output format** if you have preferences

## Error Prevention

The system will:
- ✅ Always provide valid agent names from the 46-agent framework
- ✅ Generate syntactically correct invocation format
- ✅ Match task complexity to appropriate agent(s)
- ✅ Suggest alternatives if multiple approaches are viable
- ✅ Escalate to orchestrator for unclear or complex requests