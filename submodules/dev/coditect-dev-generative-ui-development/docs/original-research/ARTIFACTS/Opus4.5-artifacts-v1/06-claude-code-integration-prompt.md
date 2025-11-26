# Claude Code Integration Prompt: Generative UI System for Coditect

*Autonomous installation and configuration instructions*

---

## MISSION

You are integrating a comprehensive Generative UI system into the Coditect autonomous development platform. This system enables AI-powered generation of production-ready UI components, layouts, and applications. Follow these instructions precisely to install, configure, and validate the integration.

---

## PHASE 1: RECONNAISSANCE

Before making any changes, gather context about the existing Coditect structure.

### 1.1 Explore Current Structure

```bash
# Map the existing directory structure
view /home/user/coditect

# Check for existing agent definitions
view /home/user/coditect/agents

# Check for existing skills
view /home/user/coditect/skills

# Check for existing commands/CLI
view /home/user/coditect/cli

# Check for configuration patterns
find /home/user/coditect -name "*.yaml" -o -name "*.yml" | head -20

# Check package.json for existing dependencies
view /home/user/coditect/package.json
```

### 1.2 Identify Integration Points

Look for these existing patterns to align with:
- Agent base classes and interfaces
- Skill registration mechanisms
- Command registration (slash commands)
- Configuration file patterns
- Event bus / message passing
- FoundationDB integration points
- Theia extension structure

---

## PHASE 2: DIRECTORY STRUCTURE CREATION

Create the Generative UI module structure within Coditect.

### 2.1 Create Core Directories

```bash
# Create the generative-ui module directory
mkdir -p /home/user/coditect/modules/generative-ui/{agents,skills,commands,templates,scripts,orchestration,config}

# Create sub-directories for agents
mkdir -p /home/user/coditect/modules/generative-ui/agents/{core,specialists,validators}

# Create sub-directories for templates
mkdir -p /home/user/coditect/modules/generative-ui/templates/{components,layouts,forms,animations}

# Create output directories
mkdir -p /home/user/coditect/modules/generative-ui/{cache,output}
```

### 2.2 Directory Structure Reference

```
/home/user/coditect/modules/generative-ui/
├── README.md                          # Module overview
├── SKILL.md                           # Skill definition (from 01-generative-ui-skill.md)
├── package.json                       # Module dependencies
├── tsconfig.json                      # TypeScript config
│
├── agents/
│   ├── index.ts                       # Agent registry
│   ├── base.ts                        # Base agent class
│   ├── core/
│   │   └── orchestrator.ts            # Main orchestrator (from 01-agent-architecture.md)
│   ├── specialists/
│   │   ├── intent-analyzer.ts
│   │   ├── ui-designer.ts
│   │   ├── motion-designer.ts
│   │   └── code-generator.ts
│   └── validators/
│       ├── a11y-auditor.ts
│       └── quality-reviewer.ts
│
├── commands/
│   ├── index.ts                       # Command registry
│   ├── ui.ts                          # /ui commands (from 02-slash-commands.md)
│   ├── motion.ts                      # /motion commands
│   ├── a11y.ts                        # /a11y commands
│   └── design.ts                      # /design commands
│
├── skills/
│   ├── SKILL.md                       # Main skill definition
│   └── sub-skills/
│       ├── component-generation.md
│       ├── layout-generation.md
│       ├── form-generation.md
│       └── animation-generation.md
│
├── templates/
│   ├── index.ts                       # Template registry
│   ├── components/                    # Component templates (from 04-llm-agnostic-prompts.md)
│   │   ├── basic-component.md
│   │   ├── compound-component.md
│   │   └── stateful-component.md
│   ├── layouts/
│   │   ├── page-layout.md
│   │   ├── dashboard-layout.md
│   │   └── wizard-layout.md
│   ├── forms/
│   │   ├── form-with-validation.md
│   │   └── dynamic-form.md
│   └── animations/
│       ├── motion-tokens.md
│       ├── animated-container.md
│       └── page-transition.md
│
├── orchestration/
│   ├── index.ts                       # Orchestration exports
│   ├── patterns/                      # Orchestration patterns (from 05-orchestration-framework.md)
│   │   ├── pipeline.ts
│   │   ├── fan-out.ts
│   │   ├── hierarchical.ts
│   │   └── iterative.ts
│   ├── context.ts                     # Execution context
│   ├── budget.ts                      # Token budget management
│   ├── recovery.ts                    # Error recovery strategies
│   └── quality-gates.ts               # Quality gate definitions
│
├── scripts/
│   ├── setup.sh                       # Setup script (from 03-automation-scripts.md)
│   ├── generate-component.sh
│   ├── a11y-audit.sh
│   ├── generate-motion-tokens.sh
│   └── batch-generate.sh
│
├── config/
│   ├── agents.yaml                    # Agent configuration
│   ├── orchestration.yaml             # Orchestration config
│   ├── quality-gates.yaml             # Quality gate definitions
│   └── defaults.yaml                  # Default settings
│
├── adapters/
│   ├── index.ts                       # LLM adapter exports
│   ├── claude.ts                      # Claude adapter
│   ├── openai.ts                      # OpenAI adapter
│   └── local.ts                       # Local model adapter
│
└── theia-integration/
    ├── frontend-module.ts             # Theia frontend extension
    ├── contribution.ts                # Command contributions
    ├── widget.ts                      # UI generation widget
    └── package.json                   # Theia extension package
```

---

## PHASE 3: FILE INSTALLATION

Install each artifact in its appropriate location.

### 3.1 Install Agent Architecture

```bash
# Copy the agent architecture document
cp /path/to/01-agent-architecture.md /home/user/coditect/modules/generative-ui/docs/architecture.md

# Extract and create TypeScript implementations from the architecture
# The document contains Python examples - convert to TypeScript for Coditect
```

**Create the base agent class:**

```typescript
// /home/user/coditect/modules/generative-ui/agents/base.ts

import { LLMAdapter, LLMResponse } from '../adapters';
import { ExecutionContext, AgentResult } from '../orchestration/context';

export enum AgentRole {
  ORCHESTRATOR = 'orchestrator',
  SPECIALIST = 'specialist',
  VALIDATOR = 'validator',
}

export interface AgentConfig {
  name: string;
  role: AgentRole;
  description: string;
  capabilities: string[];
  maxTokens: number;
  temperature: number;
  model: string;
}

export abstract class BaseAgent {
  protected config: AgentConfig;
  protected llm: LLMAdapter;
  
  constructor(config: AgentConfig, llm: LLMAdapter) {
    this.config = config;
    this.llm = llm;
  }
  
  abstract getSystemPrompt(): string;
  abstract process(input: Record<string, unknown>, context: ExecutionContext): Promise<AgentResult>;
  
  protected async callLLM(prompt: string): Promise<LLMResponse> {
    return this.llm.complete({
      system: this.getSystemPrompt(),
      prompt,
      maxTokens: this.config.maxTokens,
      temperature: this.config.temperature,
    });
  }
}
```

### 3.2 Install Skill Definition

```bash
# Copy the skill definition
cp /path/to/01-generative-ui-skill.md /home/user/coditect/modules/generative-ui/SKILL.md

# Also copy to the global skills directory if one exists
cp /path/to/01-generative-ui-skill.md /home/user/coditect/skills/generative-ui/SKILL.md
```

### 3.3 Install Slash Commands

```bash
# Copy the command documentation
cp /path/to/02-slash-commands.md /home/user/coditect/modules/generative-ui/docs/commands.md
```

**Create the command registry:**

```typescript
// /home/user/coditect/modules/generative-ui/commands/index.ts

import { CommandRegistry } from '@coditect/core';
import { uiCommands } from './ui';
import { motionCommands } from './motion';
import { a11yCommands } from './a11y';
import { designCommands } from './design';

export function registerGenerativeUICommands(registry: CommandRegistry): void {
  // Register /ui commands
  registry.registerCommand('ui', {
    description: 'Generate UI components and layouts',
    subcommands: uiCommands,
  });
  
  // Register /motion commands
  registry.registerCommand('motion', {
    description: 'Generate and manage motion/animation',
    subcommands: motionCommands,
  });
  
  // Register /a11y commands
  registry.registerCommand('a11y', {
    description: 'Accessibility audit and fixes',
    subcommands: a11yCommands,
  });
  
  // Register /design commands
  registry.registerCommand('design', {
    description: 'Design system generation',
    subcommands: designCommands,
  });
  
  // Register aliases
  registry.registerAlias('c', 'ui component');
  registry.registerAlias('l', 'ui layout');
  registry.registerAlias('f', 'ui form');
  registry.registerAlias('w', 'ui wizard');
  registry.registerAlias('d', 'ui dashboard');
  registry.registerAlias('a', 'ui animate');
  registry.registerAlias('m', 'motion');
}
```

### 3.4 Install Automation Scripts

```bash
# Copy scripts
cp /path/to/03-automation-scripts.md /home/user/coditect/modules/generative-ui/docs/scripts.md

# Extract and create individual scripts
mkdir -p /home/user/coditect/modules/generative-ui/scripts

# Make scripts executable
chmod +x /home/user/coditect/modules/generative-ui/scripts/*.sh
```

### 3.5 Install Prompt Templates

```bash
# Copy templates documentation
cp /path/to/04-llm-agnostic-prompts.md /home/user/coditect/modules/generative-ui/docs/prompts.md

# Create template files from the document
mkdir -p /home/user/coditect/modules/generative-ui/templates/{components,layouts,forms,animations,utilities}
```

**Create template registry:**

```typescript
// /home/user/coditect/modules/generative-ui/templates/index.ts

export interface PromptTemplate {
  id: string;
  name: string;
  category: 'component' | 'layout' | 'form' | 'animation' | 'utility';
  template: string;
  variables: string[];
  defaultValues: Record<string, string>;
}

export const templateRegistry: Map<string, PromptTemplate> = new Map();

export function registerTemplate(template: PromptTemplate): void {
  templateRegistry.set(template.id, template);
}

export function getTemplate(id: string): PromptTemplate | undefined {
  return templateRegistry.get(id);
}

export function renderTemplate(
  id: string,
  variables: Record<string, string>
): string {
  const template = getTemplate(id);
  if (!template) throw new Error(`Template not found: ${id}`);
  
  let rendered = template.template;
  for (const [key, value] of Object.entries(variables)) {
    rendered = rendered.replace(new RegExp(`\\{${key}\\}`, 'g'), value);
  }
  return rendered;
}

// Register built-in templates
import { componentTemplates } from './components';
import { layoutTemplates } from './layouts';
import { formTemplates } from './forms';
import { animationTemplates } from './animations';

[...componentTemplates, ...layoutTemplates, ...formTemplates, ...animationTemplates]
  .forEach(registerTemplate);
```

### 3.6 Install Orchestration Framework

```bash
# Copy orchestration documentation
cp /path/to/05-orchestration-framework.md /home/user/coditect/modules/generative-ui/docs/orchestration.md
```

**Create orchestration module:**

```typescript
// /home/user/coditect/modules/generative-ui/orchestration/index.ts

export * from './context';
export * from './budget';
export * from './recovery';
export * from './quality-gates';
export * from './patterns/pipeline';
export * from './patterns/fan-out';
export * from './patterns/hierarchical';
export * from './patterns/iterative';
```

---

## PHASE 4: CONFIGURATION

Create configuration files that integrate with Coditect's existing config system.

### 4.1 Agent Configuration

```yaml
# /home/user/coditect/modules/generative-ui/config/agents.yaml

version: 1

registry:
  orchestrator:
    class: OrchestratorAgent
    config:
      name: ui-orchestrator
      role: orchestrator
      maxTokens: 2000
      temperature: 0.3
  
  intent-analyzer:
    class: IntentAnalyzerAgent
    config:
      name: intent-analyzer
      role: specialist
      maxTokens: 3000
      temperature: 0.5
  
  ui-designer:
    class: UIDesignerAgent
    config:
      name: ui-designer
      role: specialist
      maxTokens: 5000
      temperature: 0.7
  
  motion-designer:
    class: MotionDesignerAgent
    config:
      name: motion-designer
      role: specialist
      maxTokens: 3000
      temperature: 0.6
  
  code-generator:
    class: CodeGeneratorAgent
    config:
      name: code-generator
      role: specialist
      maxTokens: 10000
      temperature: 0.2
  
  a11y-auditor:
    class: AccessibilityAuditorAgent
    config:
      name: a11y-auditor
      role: validator
      maxTokens: 3000
      temperature: 0.1
  
  quality-reviewer:
    class: QualityReviewerAgent
    config:
      name: quality-reviewer
      role: validator
      maxTokens: 3000
      temperature: 0.1

defaults:
  llmProvider: claude
  model: claude-sonnet-4-20250514
  fallbackProvider: openai
  fallbackModel: gpt-4
```

### 4.2 Orchestration Configuration

```yaml
# /home/user/coditect/modules/generative-ui/config/orchestration.yaml

version: 1

# Default orchestration pattern
pattern: pipeline

# Agent pipeline order
agents:
  - intent-analyzer
  - ui-designer
  - motion-designer
  - code-generator
  - a11y-auditor
  - quality-reviewer

# Budget configuration
budget:
  total: 50000
  strategy: dynamic
  reserve: 0.1
  allocations:
    intent-analyzer: 0.05
    ui-designer: 0.15
    motion-designer: 0.10
    code-generator: 0.40
    a11y-auditor: 0.10
    quality-reviewer: 0.10

# Quality gates
qualityGates:
  - name: accessibility
    threshold: 90
    severity: blocking
  - name: typescript_coverage
    threshold: 100
    severity: blocking
  - name: no_critical_security
    severity: blocking
  - name: performance_score
    threshold: 80
    severity: warning

# Error handling
errorHandling:
  maxRetries: 3
  backoffBase: 1.0
  circuitBreaker:
    failureThreshold: 3
    recoveryTimeout: 60
  fallbackStrategy: skip

# Iterative refinement settings
iterative:
  maxIterations: 3
  qualityThreshold: 0.9
```

### 4.3 Module Package Definition

```json
{
  "name": "@coditect/generative-ui",
  "version": "1.0.0",
  "description": "Generative UI system for Coditect",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/",
    "setup": "./scripts/setup.sh"
  },
  "dependencies": {
    "@coditect/core": "workspace:*",
    "@coditect/agents": "workspace:*",
    "@coditect/llm-adapters": "workspace:*",
    "framer-motion": "^10.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  },
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

---

## PHASE 5: THEIA INTEGRATION

Integrate the Generative UI system with Eclipse Theia.

### 5.1 Create Theia Extension Module

```typescript
// /home/user/coditect/modules/generative-ui/theia-integration/frontend-module.ts

import { ContainerModule } from '@theia/core/shared/inversify';
import { CommandContribution, MenuContribution } from '@theia/core/lib/common';
import { GenerativeUICommandContribution } from './contribution';
import { GenerativeUIWidget, GenerativeUIWidgetFactory } from './widget';
import { GenerativeUIService } from './service';

export default new ContainerModule(bind => {
  // Bind the service
  bind(GenerativeUIService).toSelf().inSingletonScope();
  
  // Bind contributions
  bind(CommandContribution).to(GenerativeUICommandContribution);
  bind(MenuContribution).to(GenerativeUICommandContribution);
  
  // Bind widget
  bind(GenerativeUIWidget).toSelf();
  bind(GenerativeUIWidgetFactory).toFactory(ctx => () => 
    ctx.container.get(GenerativeUIWidget)
  );
});
```

### 5.2 Create Command Contribution

```typescript
// /home/user/coditect/modules/generative-ui/theia-integration/contribution.ts

import { injectable, inject } from '@theia/core/shared/inversify';
import { 
  Command, 
  CommandContribution, 
  CommandRegistry,
  MenuContribution,
  MenuModelRegistry
} from '@theia/core/lib/common';
import { GenerativeUIService } from './service';

export const GenerativeUICommands = {
  GENERATE_COMPONENT: {
    id: 'generative-ui.generate-component',
    label: 'Generate UI Component',
  },
  GENERATE_LAYOUT: {
    id: 'generative-ui.generate-layout',
    label: 'Generate Layout',
  },
  AUDIT_ACCESSIBILITY: {
    id: 'generative-ui.audit-a11y',
    label: 'Audit Accessibility',
  },
};

@injectable()
export class GenerativeUICommandContribution implements CommandContribution, MenuContribution {
  
  @inject(GenerativeUIService)
  protected readonly service: GenerativeUIService;
  
  registerCommands(commands: CommandRegistry): void {
    commands.registerCommand(GenerativeUICommands.GENERATE_COMPONENT, {
      execute: () => this.service.generateComponent(),
    });
    
    commands.registerCommand(GenerativeUICommands.GENERATE_LAYOUT, {
      execute: () => this.service.generateLayout(),
    });
    
    commands.registerCommand(GenerativeUICommands.AUDIT_ACCESSIBILITY, {
      execute: () => this.service.auditAccessibility(),
    });
  }
  
  registerMenus(menus: MenuModelRegistry): void {
    menus.registerMenuAction(['ai-menu'], {
      commandId: GenerativeUICommands.GENERATE_COMPONENT.id,
      label: 'Generate UI Component',
    });
  }
}
```

---

## PHASE 6: FOUNDATIONDB INTEGRATION

Integrate with Coditect's FoundationDB layer for persistent state.

### 6.1 Create FDB Schemas

```typescript
// /home/user/coditect/modules/generative-ui/fdb/schemas.ts

import { FDBSchema } from '@coditect/fdb';

export const GenerativeUISchema: FDBSchema = {
  namespace: 'generative-ui',
  
  directories: {
    // Agent state persistence
    agentState: {
      path: ['agents', 'state'],
      keyType: 'tuple<string, string>', // [sessionId, agentName]
      valueType: 'json',
    },
    
    // Orchestration checkpoints
    checkpoints: {
      path: ['orchestration', 'checkpoints'],
      keyType: 'tuple<string, number>', // [sessionId, checkpointIndex]
      valueType: 'json',
    },
    
    // Generated component cache
    componentCache: {
      path: ['cache', 'components'],
      keyType: 'string', // hash of prompt + config
      valueType: 'json',
    },
    
    // Quality scores history
    qualityHistory: {
      path: ['quality', 'history'],
      keyType: 'tuple<string, timestamp>', // [componentId, timestamp]
      valueType: 'json',
    },
    
    // Token usage tracking
    tokenUsage: {
      path: ['metrics', 'tokens'],
      keyType: 'tuple<string, string, date>', // [userId, agentName, date]
      valueType: 'json',
    },
  },
};
```

### 6.2 Create FDB Repository

```typescript
// /home/user/coditect/modules/generative-ui/fdb/repository.ts

import { FDBClient, Transaction } from '@coditect/fdb';
import { GenerativeUISchema } from './schemas';
import { ExecutionContext, Checkpoint } from '../orchestration/context';

export class GenerativeUIRepository {
  constructor(private fdb: FDBClient) {}
  
  async saveCheckpoint(
    sessionId: string,
    checkpoint: Checkpoint
  ): Promise<void> {
    await this.fdb.transact(async (tx: Transaction) => {
      const key = [sessionId, checkpoint.index];
      await tx.set(
        GenerativeUISchema.directories.checkpoints,
        key,
        checkpoint
      );
    });
  }
  
  async getLatestCheckpoint(
    sessionId: string
  ): Promise<Checkpoint | null> {
    return this.fdb.transact(async (tx: Transaction) => {
      const range = await tx.getRange(
        GenerativeUISchema.directories.checkpoints,
        [sessionId],
        { reverse: true, limit: 1 }
      );
      return range[0]?.value ?? null;
    });
  }
  
  async cacheComponent(
    hash: string,
    component: unknown,
    ttlSeconds: number = 3600
  ): Promise<void> {
    await this.fdb.transact(async (tx: Transaction) => {
      await tx.set(
        GenerativeUISchema.directories.componentCache,
        hash,
        { component, expiresAt: Date.now() + ttlSeconds * 1000 }
      );
    });
  }
  
  async getCachedComponent(hash: string): Promise<unknown | null> {
    return this.fdb.transact(async (tx: Transaction) => {
      const cached = await tx.get(
        GenerativeUISchema.directories.componentCache,
        hash
      );
      if (!cached || cached.expiresAt < Date.now()) {
        return null;
      }
      return cached.component;
    });
  }
  
  async recordTokenUsage(
    userId: string,
    agentName: string,
    tokens: number
  ): Promise<void> {
    const date = new Date().toISOString().split('T')[0];
    
    await this.fdb.transact(async (tx: Transaction) => {
      const key = [userId, agentName, date];
      const existing = await tx.get(
        GenerativeUISchema.directories.tokenUsage,
        key
      ) ?? { total: 0, calls: 0 };
      
      await tx.set(
        GenerativeUISchema.directories.tokenUsage,
        key,
        {
          total: existing.total + tokens,
          calls: existing.calls + 1,
        }
      );
    });
  }
}
```

---

## PHASE 7: EVENT INTEGRATION

Integrate with Coditect's event-driven architecture.

### 7.1 Define Events

```typescript
// /home/user/coditect/modules/generative-ui/events/types.ts

import { DomainEvent } from '@coditect/events';

export interface UIGenerationRequestedEvent extends DomainEvent {
  type: 'generative-ui.generation.requested';
  payload: {
    sessionId: string;
    userId: string;
    request: string;
    config: Record<string, unknown>;
  };
}

export interface UIGenerationCompletedEvent extends DomainEvent {
  type: 'generative-ui.generation.completed';
  payload: {
    sessionId: string;
    componentId: string;
    code: string;
    qualityScore: number;
    tokensUsed: number;
  };
}

export interface UIGenerationFailedEvent extends DomainEvent {
  type: 'generative-ui.generation.failed';
  payload: {
    sessionId: string;
    error: string;
    recoverable: boolean;
    tokensUsed: number;
  };
}

export interface QualityGateEvaluatedEvent extends DomainEvent {
  type: 'generative-ui.quality-gate.evaluated';
  payload: {
    sessionId: string;
    gate: string;
    passed: boolean;
    score: number;
    threshold: number;
  };
}

export type GenerativeUIEvent =
  | UIGenerationRequestedEvent
  | UIGenerationCompletedEvent
  | UIGenerationFailedEvent
  | QualityGateEvaluatedEvent;
```

### 7.2 Create Event Handlers

```typescript
// /home/user/coditect/modules/generative-ui/events/handlers.ts

import { EventHandler, EventBus } from '@coditect/events';
import { GenerativeUIEvent } from './types';
import { GenerativeUIRepository } from '../fdb/repository';
import { MetricsCollector } from '@coditect/metrics';

export class GenerativeUIEventHandlers {
  constructor(
    private eventBus: EventBus,
    private repository: GenerativeUIRepository,
    private metrics: MetricsCollector
  ) {
    this.registerHandlers();
  }
  
  private registerHandlers(): void {
    this.eventBus.subscribe(
      'generative-ui.generation.completed',
      this.onGenerationCompleted.bind(this)
    );
    
    this.eventBus.subscribe(
      'generative-ui.generation.failed',
      this.onGenerationFailed.bind(this)
    );
    
    this.eventBus.subscribe(
      'generative-ui.quality-gate.evaluated',
      this.onQualityGateEvaluated.bind(this)
    );
  }
  
  private async onGenerationCompleted(
    event: GenerativeUIEvent
  ): Promise<void> {
    if (event.type !== 'generative-ui.generation.completed') return;
    
    const { sessionId, componentId, qualityScore, tokensUsed } = event.payload;
    
    // Record metrics
    this.metrics.gauge('generative_ui.quality_score', qualityScore, {
      componentId,
    });
    
    this.metrics.counter('generative_ui.tokens_used', tokensUsed, {
      status: 'success',
    });
    
    this.metrics.counter('generative_ui.generations', 1, {
      status: 'success',
    });
  }
  
  private async onGenerationFailed(
    event: GenerativeUIEvent
  ): Promise<void> {
    if (event.type !== 'generative-ui.generation.failed') return;
    
    const { sessionId, error, recoverable, tokensUsed } = event.payload;
    
    this.metrics.counter('generative_ui.generations', 1, {
      status: 'failed',
      recoverable: String(recoverable),
    });
    
    this.metrics.counter('generative_ui.tokens_used', tokensUsed, {
      status: 'failed',
    });
  }
  
  private async onQualityGateEvaluated(
    event: GenerativeUIEvent
  ): Promise<void> {
    if (event.type !== 'generative-ui.quality-gate.evaluated') return;
    
    const { gate, passed, score } = event.payload;
    
    this.metrics.counter('generative_ui.quality_gates', 1, {
      gate,
      passed: String(passed),
    });
  }
}
```

---

## PHASE 8: VALIDATION

Validate the installation is complete and functional.

### 8.1 Run Validation Checks

```bash
# Check all files are in place
ls -la /home/user/coditect/modules/generative-ui/

# Verify TypeScript compiles
cd /home/user/coditect/modules/generative-ui && npm run build

# Run tests
npm test

# Verify Theia extension loads
cd /home/user/coditect && npm run build:theia

# Check agent registry
cat /home/user/coditect/modules/generative-ui/config/agents.yaml

# Verify slash commands are registered
grep -r "registerCommand" /home/user/coditect/modules/generative-ui/commands/
```

### 8.2 Integration Test

```typescript
// /home/user/coditect/modules/generative-ui/__tests__/integration.test.ts

import { GenerativeUIModule } from '../index';
import { MockLLMAdapter } from '../adapters/__mocks__/mock-adapter';

describe('Generative UI Integration', () => {
  let module: GenerativeUIModule;
  
  beforeAll(async () => {
    module = new GenerativeUIModule({
      llmAdapter: new MockLLMAdapter(),
    });
    await module.initialize();
  });
  
  test('orchestrator processes simple component request', async () => {
    const result = await module.generate({
      request: 'Create a button component',
      config: { framework: 'react', styling: 'tailwind' },
    });
    
    expect(result.success).toBe(true);
    expect(result.output.code).toContain('Button');
    expect(result.qualityScore).toBeGreaterThanOrEqual(90);
  });
  
  test('quality gates block failing components', async () => {
    const result = await module.generate({
      request: 'Create an inaccessible component',
      config: { skipA11y: true },
    });
    
    expect(result.success).toBe(false);
    expect(result.blockingGates).toContain('accessibility');
  });
});
```

---

## PHASE 9: DOCUMENTATION

Create final documentation for the integration.

### 9.1 Create Module README

```markdown
# Generative UI Module for Coditect

## Overview

This module provides AI-powered UI generation capabilities for the Coditect platform.

## Features

- 🎨 Component generation (`/ui component`)
- 📐 Layout generation (`/ui layout`)
- 📝 Form generation (`/ui form`)
- 🧙 Wizard generation (`/ui wizard`)
- 📊 Dashboard generation (`/ui dashboard`)
- ♿ Accessibility auditing (`/a11y audit`)
- 🎬 Animation system (`/motion`)

## Quick Start

```bash
# Generate a button component
/ui component button --variants=primary,secondary --tests

# Generate a dashboard layout
/ui layout dashboard --sidebar --responsive

# Audit accessibility
/a11y audit ./src/components
```

## Configuration

See `config/` directory for configuration options.

## Architecture

See `docs/architecture.md` for system architecture.

## API

See `docs/api.md` for programmatic API reference.
```

---

## COMPLETION CHECKLIST

Before considering the integration complete, verify:

- [ ] All directories created per structure in Phase 2
- [ ] All artifacts copied to appropriate locations
- [ ] TypeScript files compile without errors
- [ ] All tests pass
- [ ] Theia extension loads correctly
- [ ] Slash commands are registered and functional
- [ ] FoundationDB schemas are registered
- [ ] Event handlers are subscribed
- [ ] Configuration files are valid YAML
- [ ] Documentation is complete
- [ ] Integration test passes

---

## ROLLBACK PROCEDURE

If integration fails:

```bash
# Remove the module
rm -rf /home/user/coditect/modules/generative-ui

# Remove from skills directory
rm -rf /home/user/coditect/skills/generative-ui

# Revert any changes to existing files
git checkout -- /home/user/coditect/

# Rebuild Coditect
cd /home/user/coditect && npm run build
```

---

*Document Version: 1.0*
*Target: Coditect Autonomous Development Platform*
*Generated: November 2025*
