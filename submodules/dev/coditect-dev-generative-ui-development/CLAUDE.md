# CLAUDE.md - CODITECT Generative UI Development Context

## Project Overview

**CODITECT Generative UI Development** - Research-driven implementation of AI-powered user interface generation for multi-agent development systems.

**Status**: Research complete (17,134 lines), implementation beginning
**Phase**: Foundation - Core library and agent development
**Parent Project**: CODITECT Rollout Master

## What is This Project?

This repository explores and implements **generative UI capabilities** - the ability for AI agents to dynamically create production-quality user interfaces from natural language specifications. Unlike traditional code completion or template systems, generative UI involves:

1. **Intent Analysis** - Understanding what the user wants to accomplish
2. **UI Architecture** - Designing appropriate layouts and components
3. **Code Generation** - Producing production-ready TypeScript/React code
4. **Quality Gates** - Ensuring accessibility, performance, and best practices

## Research Foundation

### Comprehensive Analysis (17K+ Lines)

The `docs/original-research/` directory contains extensive analysis:

**Core Documents:**
1. **generative-ui-skill.md** - Complete skill definition with usage patterns
2. **generative-ui-technical-analysis.md** - Architecture deep-dive (Google Generative UI, v0.dev, Claude Artifacts)
3. **implementation-guide.md** - Step-by-step integration strategies
4. **enterprise-integration-strategy.md** - Governance and adoption frameworks
5. **comparative-analysis.md** - Market landscape and competitive positioning

**Technical Specifications:**
- **Agent Architecture** - Multi-agent system coordination patterns
- **Prompt Engineering** - Template patterns optimized for UI generation
- **Automation Scripts** - CLI tools and generation pipelines
- **Slash Commands** - User-facing command interfaces (/ui component, /ui layout)
- **Orchestration Framework** - Workflow management for complex UI tasks
- **LLM-Agnostic Prompts** - Cross-model compatibility strategies

### Key Research Findings

**Token Economics:**
- Simple component: 200 prompt + 800 completion tokens (~$0.001)
- Complex layout: 500 prompt + 3,000 completion tokens (~$0.004)
- Full application: 1,500 prompt + 15,000 completion tokens (~$0.020)
- Multi-agent overhead: 15x base cost (requires optimization)

**Quality Attributes:**
- Accessibility: WCAG AA/AAA compliance enforced through prompt templates
- Responsiveness: Mobile-first with breakpoint specifications
- Performance: Tree-shakeable code, GPU-accelerated animations
- Maintainability: TypeScript strict mode, no `any` types

**Optimization Strategies:**
- Component caching: 40-60% token savings
- Incremental generation: 30-50% token savings
- Template hybridization: 20-40% token savings

## Repository Structure

```
coditect-dev-generative-ui-development/
├── .coditect -> ../../core/coditect-core    # CODITECT brain
├── .claude -> .coditect                     # Claude Code compatibility
├── docs/
│   └── original-research/                   # 17K+ lines research
│       └── ARTIFACTS/
│           └── Opus4.5-artifacts-v1/       # 20+ technical documents
├── src/
│   ├── agents/                              # AI agent implementations
│   │   ├── intent-analyzer/                 # Parse user requirements
│   │   ├── ui-architect/                    # Design layouts
│   │   ├── code-generator/                  # Produce code
│   │   ├── accessibility-auditor/           # WCAG validation
│   │   └── quality-reviewer/                # Performance & best practices
│   ├── commands/                            # Slash commands
│   │   ├── ui-component.md                  # /ui component
│   │   ├── ui-layout.md                     # /ui layout
│   │   └── ui-app.md                        # /ui app
│   ├── skills/                              # Reusable generation skills
│   │   ├── generative-ui/                   # Core skill
│   │   └── accessibility-checker/           # A11y validation
│   ├── prompts/                             # Prompt templates
│   │   ├── component-templates/
│   │   ├── layout-templates/
│   │   └── animation-templates/
│   ├── lib/                                 # Core libraries
│   │   ├── ui-synthesis-engine.ts           # UI generation logic
│   │   ├── token-optimizer.ts               # Cost management
│   │   └── quality-gates.ts                 # Validation rules
│   └── types/                               # TypeScript definitions
│       ├── ui-spec.ts                       # UI specification types
│       └── generation-config.ts             # Configuration types
├── tests/
│   ├── unit/                                # Unit tests
│   ├── integration/                         # Agent coordination tests
│   └── e2e/                                 # End-to-end generation tests
├── examples/                                # Generated UI examples
│   ├── components/
│   ├── layouts/
│   └── applications/
└── scripts/                                 # Automation
    ├── generate-ui.ts                       # CLI tool
    ├── analyze-tokens.ts                    # Cost analysis
    └── validate-output.ts                   # Quality validation
```

## Development Workflow

### Phase 1: Foundation (Current)

**Objectives:**
1. Implement core UI synthesis engine
2. Create basic prompt templates for components and layouts
3. Build slash command infrastructure
4. Establish quality gates (TypeScript strict, accessibility, performance)

**Key Tasks:**
- [ ] Implement `ui-synthesis-engine.ts` with component/layout generation
- [ ] Create prompt template system with variable substitution
- [ ] Build `/ui component` slash command with framework detection
- [ ] Add accessibility validation using axe-core
- [ ] Implement token cost tracking and optimization

### Phase 2: Agent Integration

**Objectives:**
1. Develop specialized agents for multi-agent orchestration
2. Implement agent discovery and task routing
3. Create quality gate automation
4. Build component caching system

**Key Tasks:**
- [ ] Develop intent-analyzer agent (parse requirements)
- [ ] Develop ui-architect agent (design layout structure)
- [ ] Develop code-generator agent (produce TypeScript/React)
- [ ] Develop accessibility-auditor agent (WCAG validation)
- [ ] Implement agent coordination via CODITECT orchestrator

### Phase 3: Advanced Features

**Objectives:**
1. Add multi-framework support (Vue, Svelte)
2. Implement design-to-code (Figma/Sketch import)
3. Build component library generator
4. Add animation synthesis capabilities

### Working with Research Materials

**Before implementing features:**

1. **Read relevant research documents** in `docs/original-research/ARTIFACTS/`
2. **Extract patterns and specifications** from the 17K+ lines of analysis
3. **Follow architectural patterns** defined in technical-analysis.md
4. **Use prompt templates** from the research as starting points
5. **Apply token optimization** strategies from comparative-analysis.md

**Example workflow:**
```bash
# Implementing button component generator:
# 1. Read: 01-generative-ui-skill.md (lines 119-137 - Component Template)
# 2. Read: 03-implementation-guide.md (component generation patterns)
# 3. Extract prompt template and requirements
# 4. Implement in src/prompts/component-templates/button.ts
# 5. Add tests in tests/unit/components/button.test.ts
```

## Integration with CODITECT

### Distributed Intelligence

**Symlink Chains:**
- `.coditect -> ../../core/coditect-core` - Access to 52 agents, 81 commands, 26 skills
- `.claude -> .coditect` - Claude Code compatibility

**Shared Context:**
- MEMORY-CONTEXT system for session preservation
- Cross-submodule agent coordination
- Checkpoint creation for continuity

### Agent Invocation

**Use Task Tool Pattern (CRITICAL):**

```python
# CORRECT - Invokes specialized agent
Task(
    subagent_type="general-purpose",
    prompt="Use ui-architect subagent to design dashboard layout with sidebar and topbar"
)

# INCORRECT - Just prompts base Claude
"Use ui-architect agent to design dashboard"
```

### Command Integration

Generative UI slash commands integrate with CODITECT framework:

```bash
# Component generation
/ui component button --variant=primary,secondary --size=sm,md,lg

# Layout generation
/ui layout dashboard --sidebar --topbar --responsive

# Full application
/ui app settings --sections=profile,notifications,security
```

## Quality Standards

### Code Quality

**Required:**
- TypeScript strict mode (100% typed, no `any`)
- ESLint + Prettier configured
- Unit test coverage ≥ 80%
- Integration tests for agent coordination

**Recommended:**
- Storybook for component documentation
- Lighthouse accessibility score ≥ 95
- Bundle size analysis

### Accessibility

**WCAG AA Compliance:**
- Semantic HTML elements (`<button>`, `<nav>`, `<main>`)
- ARIA attributes for custom patterns
- Keyboard navigation support
- Visible focus states
- Color contrast ratios ≥ 4.5:1

**Validation:**
```bash
npm run test:a11y  # Automated axe-core checks
```

### Performance

**Targets:**
- Bundle size: < 50KB per component
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Lighthouse Performance: ≥ 90

## Token Budget Management

### Optimization Strategies

1. **Prompt Compression** - Minimize redundant context
2. **Component Caching** - Reuse successfully generated patterns
3. **Incremental Generation** - Build iteratively vs. monolithic
4. **Template Hybridization** - Combine static + generated code

### Cost Tracking

```typescript
// Track token usage per generation
interface TokenUsage {
  promptTokens: number;
  completionTokens: number;
  totalCost: number;
  generationType: 'component' | 'layout' | 'application';
}

// Log and analyze costs
npm run analyze-tokens
```

## Testing Strategy

### Unit Tests

```bash
# Test individual functions and utilities
npm run test:unit

# Examples:
# - Prompt template rendering
# - Token cost calculation
# - Accessibility rule validation
```

### Integration Tests

```bash
# Test agent coordination
npm run test:integration

# Examples:
# - Intent analysis → UI architecture flow
# - UI architecture → Code generation flow
# - Full pipeline: intent → code → validation
```

### E2E Tests

```bash
# Test actual UI generation
npm run test:e2e

# Examples:
# - Generate button component, validate output
# - Generate dashboard layout, check responsiveness
# - Generate full app, run accessibility audit
```

## Common Tasks

### Generate a UI Component

```bash
# Using slash command
/ui component button --variant=primary,secondary --size=sm,md,lg --loading

# Using script
npm run generate -- component button --variants=primary,secondary --sizes=sm,md,lg
```

### Generate a Layout

```bash
# Using slash command
/ui layout dashboard --sidebar --topbar --responsive

# Using script
npm run generate -- layout dashboard --sidebar --topbar
```

### Analyze Token Costs

```bash
# Analyze historical generation costs
npm run analyze-tokens

# Output:
# - Average cost per component: $0.001
# - Most expensive generation: $0.020 (full app)
# - Total spent this month: $5.43
# - Optimization opportunities: 3 found
```

### Validate Accessibility

```bash
# Run accessibility audit on generated code
npm run validate:a11y examples/components/Button.tsx

# Output:
# ✓ Semantic HTML used
# ✓ ARIA attributes correct
# ✓ Keyboard navigation functional
# ✗ Color contrast ratio: 3.8:1 (requires 4.5:1)
```

## AI Agent Coordination

### When to Use Which Agent

**intent-analyzer** - Parse user requirements
- Input: Natural language description
- Output: Structured UI specification
- Use when: User request is ambiguous or complex

**ui-architect** - Design layout structure
- Input: UI specification
- Output: Component hierarchy and layout plan
- Use when: Multiple components needed, complex layouts

**code-generator** - Produce TypeScript/React code
- Input: Layout plan or component spec
- Output: Production-ready code files
- Use when: Ready to generate actual code

**accessibility-auditor** - Validate WCAG compliance
- Input: Generated code
- Output: Accessibility report with violations
- Use when: Quality gate for production deployments

**quality-reviewer** - Performance and best practices
- Input: Generated code
- Output: Quality report (bundle size, performance, maintainability)
- Use when: Final validation before deployment

### Multi-Agent Orchestration Example

```python
# Complex UI generation workflow
Task(
    subagent_type="general-purpose",
    prompt="""Use orchestrator agent to coordinate generative UI creation:

    User request: "Build a dashboard for project management with kanban board, team activity feed, and metrics widgets"

    Phase 1: Intent Analysis
    - Use intent-analyzer to parse requirements
    - Extract: components needed, layout structure, interactions

    Phase 2: UI Architecture
    - Use ui-architect to design layout
    - Specify: grid structure, responsive breakpoints, component slots

    Phase 3: Code Generation
    - Use code-generator for each component
    - Generate: Dashboard.tsx, KanbanBoard.tsx, ActivityFeed.tsx, MetricsWidget.tsx

    Phase 4: Quality Gates
    - Use accessibility-auditor for WCAG validation
    - Use quality-reviewer for performance check

    Phase 5: Assembly
    - Combine components
    - Generate tests and Storybook stories
    - Create deployment package

    Token budget: 20,000 tokens
    Quality threshold: Accessibility ≥ 90, Performance ≥ 90
    """
)
```

## Troubleshooting

### Issue: Generated code has TypeScript errors

**Solution:**
1. Check prompt template includes proper type definitions
2. Verify framework detection (React version, TypeScript version)
3. Review `tsconfig.json` in generated output
4. Run `npm run validate:types` to diagnose

### Issue: Accessibility audit fails

**Solution:**
1. Review WCAG requirements in prompt template
2. Check semantic HTML usage (should use native elements)
3. Validate ARIA attributes match pattern guidelines
4. Run `npm run test:a11y -- --verbose` for detailed report

### Issue: Token costs too high

**Solution:**
1. Enable component caching: `npm run generate -- --cache`
2. Use incremental generation: `npm run generate -- --incremental`
3. Analyze prompt efficiency: `npm run analyze-tokens -- --optimize`
4. Review prompt templates for redundancy

## Contributing

### Before Making Changes

1. **Read CODITECT conventions** in parent `.coditect/README.md`
2. **Review research materials** relevant to your feature
3. **Check existing patterns** in `src/` directory
4. **Create feature branch**: `feature/ui-component-generator`

### Commit Conventions

```
feat(ui-gen): Add button component generator with accessibility
fix(a11y): Correct ARIA label in dashboard layout
docs(research): Add v0.dev comparative analysis
test(e2e): Add dashboard generation end-to-end test

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Pull Request Checklist

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Accessibility audit passes
- [ ] TypeScript strict mode (no `any`)
- [ ] Documentation updated
- [ ] Token cost analyzed
- [ ] Research references cited

## Resources

### Internal Documentation

- `docs/original-research/` - 17K+ lines of research
- `.coditect/agents/` - 52 specialized agents
- `.coditect/commands/` - 81 slash commands
- `.coditect/skills/` - 26 production skills

### External References

- **Google Generative UI**: https://ai.google.dev/gemini-api/docs/structured-output
- **Claude Artifacts**: https://www.anthropic.com/news/artifacts
- **v0.dev**: https://v0.dev
- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/
- **React TypeScript**: https://react-typescript-cheatsheet.netlify.app/

## Support

**Parent Project**: CODITECT Rollout Master
**Repository**: https://github.com/coditect-ai/coditect-dev-generative-ui-development
**Owner**: AZ1.AI INC
**Lead**: Hal Casteel, Founder/CEO/CTO

---

**Last Updated**: 2025-11-26
**Research Status**: Complete (17,134 lines)
**Implementation Status**: Foundation phase
**Production Ready**: 20% (structure complete, code in progress)
