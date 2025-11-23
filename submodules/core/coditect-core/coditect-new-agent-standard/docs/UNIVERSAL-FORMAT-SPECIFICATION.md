# Universal Agent Format Specification v2.0
## Complete Technical Specification for Cross-Platform AI Agents

### Overview
The Universal Agent Format (UAF) v2.0 provides a standardized, extensible format for AI agents that works across multiple LLM platforms while maintaining backward compatibility and platform-specific optimizations.

---

## Architecture Principles

### 1. Layered Compatibility
- **Layer 1**: Universal metadata (all platforms)
- **Layer 2**: LLM-specific adaptations
- **Layer 3**: Protocol integrations (MCP, A2A, etc.)
- **Layer 4**: Enterprise governance
- **Layer 5**: Enhanced features (platform-dependent)

### 2. Graceful Degradation
- Basic platforms receive core functionality
- Advanced platforms access enhanced features
- No platform fails due to unsupported features

### 3. Standard Compliance
- AGENTS.md instruction format
- Anthropic Skills/Commands integration
- OpenAI function calling compatibility
- Google MCP/A2A protocol support
- Enterprise governance hooks

---

## Format Specification

### Complete YAML Structure

```yaml
---
# ============================================================================
# UNIVERSAL AGENT FORMAT v2.0 - COMPLETE SPECIFICATION
# ============================================================================

# LAYER 1: Universal Metadata (REQUIRED - ALL PLATFORMS)
name: [agent-name]                    # Lowercase, hyphens, max 64 chars
description: [capability-description] # Max 1024 chars, no XML tags
version: "2.0.0"                     # Semantic versioning
created: "[YYYY-MM-DD]"              # Creation date
author: "[author-or-team]"           # Creator identification

# LAYER 2: LLM Platform Compatibility Matrix (REQUIRED)
llm_compatibility:
  anthropic_claude:
    supported: [true/false]           # Platform support flag
    model: "[model-name]"             # Preferred model
    tools: [tool-list]                # Available tools
    skills_enabled: [true/false]      # Skills framework support
    commands_enabled: [true/false]    # Commands framework support
    
  openai_gpt:
    supported: [true/false]
    model: "[model-name]"
    tools_mapping:                    # Tool name mappings
      [universal-name]: [platform-specific-name]
    function_calling: [true/false]    # Function calling support
    
  google_gemini:
    supported: [true/false]
    model: "[model-name]"
    mcp_enabled: [true/false]         # MCP protocol support
    tools_via_mcp: [true/false]       # Tools accessed via MCP
    
  grok_xai:
    supported: [true/false]
    model: "[model-name]"
    openai_compatible: [true/false]   # OpenAI API compatibility
    structured_output: [true/false]   # JSON schema support

# LAYER 3A: Anthropic Skills Integration (OPTIONAL)
skills:
  primary_skills:
    - name: "[skill-name]"            # Skill identifier
      path: "skills/[directory]"      # Relative path to skill
      description: "[skill-purpose]"  # What the skill does
      version: "[version]"            # Skill version
      dependencies: [dependency-list] # Required dependencies

# LAYER 3B: Anthropic Commands Integration (OPTIONAL)
commands:
  [command-group]:
    - name: "/[command-name]"         # Command with slash prefix
      description: "[command-purpose]" # Command functionality
      usage: "/[command] [params]"    # Usage syntax
      parameters:                     # Parameter definitions
        - name: "[param-name]"
          type: "[param-type]"
          required: [true/false]
          description: "[param-desc]"

# LAYER 4: Context Awareness DNA (ENHANCED FEATURE)
context_awareness:
  auto_scope_keywords:               # Automatic scope detection
    [domain-name]: [keyword-list]   # Domain-specific keywords
    
  entity_detection:                 # Entity recognition
    frameworks: [framework-list]    # Relevant frameworks
    tools: [tool-list]             # Platform tools
    patterns: [pattern-list]       # Design patterns
    
  confidence_boosters:             # Quality indicators
    - "[indicator-description]"    # When to use this agent

# LAYER 5: Cross-Platform Protocol Support (OPTIONAL)
protocols:
  # Anthropic Standards
  task_protocol:
    enabled: [true/false]
    invocation: '[invocation-pattern]'
    
  # Universal Standards
  agents_md:
    compatible: [true/false]
    instruction_format: "[format]"
    
  # Communication Protocols
  mcp_integration:
    enabled: [true/false]
    capabilities: [capability-list]
    servers: [server-list]
    
  a2a_communication:
    enabled: [true/false]
    discovery_enabled: [true/false]
    can_coordinate_with: [agent-list]

# LAYER 6: Enterprise Governance (OPTIONAL)
enterprise_governance:
  identity:
    agent_id: "[unique-identifier]"   # Unique agent ID
    classification: "[security-level]" # Security classification
    owner: "[owner-contact]"          # Responsible party
    cost_center: "[cost-center]"      # Billing allocation
    
  security:
    authentication: [auth-methods]    # Auth requirements
    authorization: [authz-methods]    # Authorization methods
    data_access: [access-levels]      # Data access permissions
    encryption: [encryption-reqs]     # Encryption requirements
    
  quality_standards:
    az1_verification: [required/optional] # Testing requirements
    testing_protocols: [test-list]    # Required testing
    certification: [cert-list]        # Compliance certifications
    sla_requirements: [sla-specs]     # Service level agreements
    
  lifecycle:
    provisioning: "[provision-method]" # How agent is deployed
    monitoring: "[monitor-level]"     # Monitoring requirements
    audit_trail: "[audit-level]"     # Audit requirements
    decommissioning: "[decommit-process]" # Retirement process

# LAYER 7: Automation & Progress Features (ENHANCED)
automation_features:
  auto_scope_detection: [true/false]    # Automatic task scoping
  context_aware_prompting: [true/false] # Context-based prompts
  progress_reporting: [true/false]      # Progress tracking
  refinement_suggestions: [true/false]  # Improvement suggestions
  error_recovery: [true/false]          # Automatic error handling

progress_checkpoints:
  25: "[25%-milestone-description]"     # Quarter progress
  50: "[50%-milestone-description]"     # Half progress
  75: "[75%-milestone-description]"     # Three-quarter progress
  100: "[completion-description]"       # Full completion

# LAYER 8: Multi-Agent Coordination (OPTIONAL)
coordination_patterns:
  works_with:
    - agent: "[partner-agent-name]"     # Coordinating agent
      coordination: "[coordination-desc]" # How they work together
      handoff_triggers: [trigger-list]  # When to hand off
      shared_context: [context-list]    # Shared information
      
  orchestration:
    can_orchestrate: [true/false]      # Can coordinate others
    orchestration_patterns: [pattern-list] # Coordination patterns
    conflict_resolution: "[resolution-method]" # Conflict handling

# LAYER 9: Performance & Metrics (OPTIONAL)
performance:
  estimated_tokens:
    input_avg: [number]                # Average input tokens
    output_avg: [number]               # Average output tokens
    context_window: [number]           # Required context window
    
  performance_metrics:
    latency_target: "[time-specification]" # Target response time
    throughput_target: "[rate-specification]" # Target throughput
    accuracy_target: "[percentage]"    # Target accuracy
    
  resource_requirements:
    memory_mb: [number]                # Memory requirements
    compute_units: [number]            # Compute requirements
    storage_mb: [number]               # Storage requirements

# LAYER 10: Deployment Configuration (OPTIONAL)
deployment:
  environments:
    development:
      enabled: [true/false]
      config_overrides: [config-list]
    staging:
      enabled: [true/false]
      config_overrides: [config-list]
    production:
      enabled: [true/false]
      config_overrides: [config-list]
      
  scaling:
    min_instances: [number]            # Minimum instances
    max_instances: [number]            # Maximum instances
    auto_scaling: [true/false]         # Auto-scaling enabled
    scaling_triggers: [trigger-list]   # Scaling conditions
    
  integration_points:
    apis: [api-list]                   # External API dependencies
    databases: [database-list]         # Database connections
    message_queues: [queue-list]       # Message queue integrations
    external_services: [service-list]  # External service dependencies
---

# AGENTS.md Compatible Instructions
[Standard markdown instructions following AGENTS.md format]
```

---

## Implementation Guidelines

### 1. Minimum Viable Implementation
**Required Layers**: 1-2 (Universal metadata + LLM compatibility)
**Optional Layers**: All others based on platform capabilities

### 2. Platform-Specific Implementations
- **Anthropic**: Layers 1-4 + Skills/Commands (3A/3B)
- **OpenAI**: Layers 1-2 + Function calling adaptations
- **Google**: Layers 1-2 + MCP integration (Layer 5)
- **Enterprise**: Layers 1-2 + Governance (Layer 6)

### 3. Validation Requirements
- YAML syntax validation
- Platform compatibility verification
- Protocol compliance testing
- Performance benchmark validation

### 4. Migration Strategy
- Start with proven agent archetypes
- Implement universal format incrementally
- Maintain backward compatibility
- Test cross-platform functionality

---

## Compatibility Matrix

| Layer | Anthropic | OpenAI | Google | Enterprise | Purpose |
|-------|-----------|---------|---------|------------|---------|
| 1 | ✅ | ✅ | ✅ | ✅ | Universal metadata |
| 2 | ✅ | ✅ | ✅ | ✅ | Platform compatibility |
| 3A/3B | ✅ | ❌ | ❌ | ❌ | Skills/Commands |
| 4 | ✅ | Partial | Partial | ❌ | Context awareness |
| 5 | ✅ | Partial | ✅ | ❌ | Protocol support |
| 6 | Partial | ❌ | ❌ | ✅ | Enterprise governance |
| 7 | ✅ | ❌ | ❌ | Partial | Enhanced automation |
| 8 | ✅ | ❌ | ✅ | ✅ | Multi-agent coordination |
| 9 | Optional | Optional | Optional | ✅ | Performance metrics |
| 10 | Optional | Optional | Optional | ✅ | Deployment config |

**Result: Universal compatibility with platform-specific optimizations**