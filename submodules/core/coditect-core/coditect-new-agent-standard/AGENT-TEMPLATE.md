# Universal Agent Template v2.0
## Template for creating cross-platform compatible agents

```yaml
---
# ============================================================================
# UNIVERSAL LLM-AGNOSTIC AGENT TEMPLATE v2.0
# Copy this template to create new universal agents
# Compatible with: Anthropic, OpenAI, Gemini, Grok, Enterprise platforms
# ============================================================================

# LAYER 1: Universal Metadata (Required for ALL platforms)
name: [agent-name]
description: [Specific capability and when to use this agent]
version: "2.0.0"
created: "[YYYY-MM-DD]"
author: "Universal Agent Framework"

# LAYER 2: LLM Platform Compatibility Matrix
llm_compatibility:
  anthropic_claude:
    supported: true
    model: "sonnet"
    tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "TodoWrite"]
    skills_enabled: true
    commands_enabled: true
    
  openai_gpt:
    supported: true
    model: "gpt-4"
    tools_mapping:
      Read: "file_reader"
      Write: "file_writer"
      Bash: "code_interpreter"
    function_calling: true
    
  google_gemini:
    supported: true
    model: "gemini-2.0-flash-thinking"
    mcp_enabled: true
    tools_via_mcp: true
    
  grok_xai:
    supported: true
    model: "grok-3"
    openai_compatible: true
    structured_output: true

# LAYER 3: Anthropic Skills Integration
skills:
  primary_skills:
    - name: "[skill-name]"
      path: "skills/[skill-directory]"
      description: "[skill purpose and capabilities]"

# LAYER 4: Anthropic Commands Integration
commands:
  command_group:
    - name: "/[command-name]"
      description: "[command purpose]"
      usage: "/[command-name] [parameters]"

# LAYER 5: Context Awareness DNA (47-Agent Proven Pattern)
context_awareness:
  auto_scope_keywords:
    primary_domain: ["keyword1", "keyword2", "domain-terms"]
    secondary_domain: ["related-terms", "context-clues"]
    
  entity_detection:
    frameworks: ["relevant-frameworks", "technologies"]
    tools: ["specific-tools", "platforms"]
    patterns: ["design-patterns", "methodologies"]
    
  confidence_boosters:
    - "quality indicators that trigger this agent"
    - "expertise markers that suggest this agent's use"

# LAYER 6: Cross-Platform Protocol Support
protocols:
  # Anthropic Standards
  task_protocol: 
    enabled: true
    invocation: 'Task(subagent_type="general-purpose", prompt="Use [agent-name] subagent to [task]")'
    
  # Universal Standards
  agents_md:
    compatible: true
    instruction_format: "markdown"
    
  # Communication Protocols
  mcp_integration:
    enabled: [true/false]
    capabilities: ["capability1", "capability2"]
    
  a2a_communication:
    enabled: [true/false]
    can_coordinate_with: ["agent1", "agent2"]

# LAYER 7: Enterprise Governance
enterprise_governance:
  identity:
    agent_id: "[unique-agent-id]"
    classification: "[standard/confidential/enterprise-critical]"
    owner: "[team-email]"
    
  quality_standards:
    az1_verification: [required/optional]
    testing_protocols: ["test1", "test2"]
    certification: ["cert1", "cert2"]
    
  lifecycle:
    provisioning: "[auto/manual/approval-required]"
    monitoring: "[basic/enhanced/continuous]"
    audit_trail: "[minimal/standard/full-logging]"

# LAYER 8: Automation & Progress (Proven Pattern)
automation_features:
  auto_scope_detection: true
  context_aware_prompting: true
  progress_reporting: true
  refinement_suggestions: [true/false]

progress_checkpoints:
  25: "[25% milestone description]"
  50: "[50% milestone description]"
  75: "[75% milestone description]"
  100: "[completion milestone description]"

coordination_patterns:
  works_with:
    - agent: "[partner-agent-1]"
      coordination: "[coordination description]"
    - agent: "[partner-agent-2]"
      coordination: "[coordination description]"
---

# Universal Agent Instructions (AGENTS.md Compatible)

You are [role description]. Your primary responsibility is [core function].

## Platform-Specific Behavior

### When running on Anthropic Claude:
- [Anthropic-specific behavior and capabilities]
- Utilize Skills for [specific use cases]
- Execute Commands for [workflow automation]
- Use Task Protocol for [coordination patterns]

### When running on OpenAI:
- [OpenAI-specific behavior and function calling]
- Map tools to [function descriptions]
- Use structured output for [consistent results]

### When running on Google Gemini:
- [Gemini-specific behavior and MCP integration]
- Utilize MCP for [tool integration]
- Leverage [specific Gemini capabilities]

### When running on Enterprise Platforms:
- [Enterprise-specific governance and compliance]
- Implement [authentication/authorization flows]
- Generate [compliance documentation]

## Core Responsibilities

1. **Primary Function**
   - [Specific responsibility 1]
   - [Specific responsibility 2]
   - [Specific responsibility 3]

2. **Secondary Functions**
   - [Supporting capability 1]
   - [Supporting capability 2]

## Output Standards

### [Output Type 1]
```
[Template or format description]
```

### [Output Type 2]  
```
[Template or format description]
```

## Integration Patterns

**Multi-Agent Workflows:**
- [Description of how this agent works with others]
- [Coordination patterns and handoff procedures]

**Cross-Platform Compatibility:**
- [Platform-specific integration notes]
- [Fallback behaviors for unsupported features]
```

### Usage Instructions

1. **Copy this template** to create a new universal agent
2. **Fill in all bracketed placeholders** with agent-specific information
3. **Remove unused optional sections** to keep the agent definition clean
4. **Test on target platforms** before deployment
5. **Validate backward compatibility** with existing systems

### Template Sections Guide

- **Layers 1-2**: Required for basic cross-platform functionality
- **Layers 3-4**: Anthropic-specific Skills and Commands
- **Layers 5-6**: Enhanced features and protocol support
- **Layers 7-8**: Enterprise governance and automation

### Compatibility Notes

- **Minimum viable**: Layers 1-2 for basic functionality
- **Anthropic full**: All layers for complete feature set
- **Enterprise**: Emphasis on Layer 7 for governance
- **Cross-platform**: Layer 6 for protocol interoperability