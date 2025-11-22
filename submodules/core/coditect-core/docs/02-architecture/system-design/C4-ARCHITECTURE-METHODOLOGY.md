# C4 Model Architecture Methodology

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**
**Developed by Hal Casteel, Founder/CEO/CTO**
**Part of the AZ1.AI CODITECT Project Management & Development Platform**

---

## Overview

The C4 Model provides a hierarchical approach to visualizing software architecture through four levels of abstraction:

1. **C1: System Context** - The big picture (10,000 foot view)
2. **C2: Container** - High-level technology choices (5,000 foot view)
3. **C3: Component** - Component-level architecture (1,000 foot view)
4. **C4: Code** - Class diagrams and implementation details (ground level)

This methodology ensures **complete architectural clarity** from business stakeholders to developers.

---

## C1: System Context Diagram

### Purpose
Show how your system fits into the world around it - who uses it and what other systems it interacts with.

### Audience
- Business stakeholders
- Product managers
- Executive team
- Non-technical team members

### What to Include
- Your software system (center)
- People who use it (actors/personas)
- External systems it integrates with
- Data flows between systems

### Mermaid Template

```mermaid
C4Context
    title System Context Diagram for [Your Product Name]

    Person(customer, "Customer", "End user of the system")
    Person(admin, "Admin", "System administrator")

    System(yourSystem, "[Your Product]", "Core system that delivers [value proposition]")

    System_Ext(paymentGateway, "Payment Gateway", "Processes payments")
    System_Ext(emailService, "Email Service", "Sends transactional emails")
    System_Ext(analytics, "Analytics Platform", "Tracks usage metrics")

    Rel(customer, yourSystem, "Uses", "HTTPS")
    Rel(admin, yourSystem, "Manages", "HTTPS")
    Rel(yourSystem, paymentGateway, "Processes payments via", "API/HTTPS")
    Rel(yourSystem, emailService, "Sends emails via", "SMTP/API")
    Rel(yourSystem, analytics, "Sends events to", "HTTPS")
```

### Example: AI Screenshot Automator

```mermaid
C4Context
    title System Context - AI Screenshot Automator

    Person(developer, "Developer", "Uses tool for documentation")
    Person(qaEngineer, "QA Engineer", "Uses for visual testing")

    System(screenshotter, "AI Screenshot Automator", "Automates screenshot capture and documentation for AI-assisted development")

    System_Ext(github, "GitHub", "Stores screenshots and documentation")
    System_Ext(cicd, "CI/CD Pipeline", "Runs automated captures")
    System_Ext(browser, "Web Browser", "Target for web app screenshots")
    System_Ext(macOS, "macOS", "Target for native app screenshots")

    Rel(developer, screenshotter, "Runs before/after captures", "CLI")
    Rel(qaEngineer, screenshotter, "Automates visual regression tests", "CLI")
    Rel(screenshotter, github, "Commits screenshots to", "Git")
    Rel(screenshotter, cicd, "Integrates with", "Webhooks")
    Rel(screenshotter, browser, "Controls via", "Playwright/Puppeteer")
    Rel(screenshotter, macOS, "Controls via", "AppleScript")
```

**Output**: Save as `/docs/architecture/diagrams/c1-system-context.mmd`

---

## C2: Container Diagram

### Purpose
Show the high-level technology choices and how containers (applications, databases, file systems) interact.

### Audience
- Technical team leads
- DevOps engineers
- Solution architects
- Security team

### What to Include
- Web applications
- Mobile apps
- Desktop applications
- Databases
- File storage
- Message queues
- APIs
- Technology choices for each container

### Mermaid Template

```mermaid
C4Container
    title Container Diagram for [Your Product Name]

    Person(user, "User", "End user")

    Container_Boundary(c1, "[Your Product]") {
        Container(webApp, "Web Application", "React/Next.js", "Provides UI for users")
        Container(api, "API Application", "Node.js/Express", "Handles business logic")
        Container(authService, "Auth Service", "Auth0/Keycloak", "Manages authentication")
        ContainerDb(database, "Database", "PostgreSQL", "Stores application data")
        ContainerDb(cache, "Cache", "Redis", "Caches frequently accessed data")
        Container(workerQueue, "Background Workers", "Bull/BullMQ", "Processes async jobs")
    }

    System_Ext(emailService, "Email Service", "Sends emails")

    Rel(user, webApp, "Uses", "HTTPS")
    Rel(webApp, api, "Calls", "HTTPS/REST")
    Rel(api, authService, "Validates tokens", "OAuth 2.0")
    Rel(api, database, "Reads/Writes", "SQL")
    Rel(api, cache, "Reads/Writes", "Redis Protocol")
    Rel(api, workerQueue, "Enqueues jobs", "Redis")
    Rel(workerQueue, emailService, "Sends emails via", "SMTP/API")
```

### Example: AI Screenshot Automator

```mermaid
C4Container
    title Container Diagram - AI Screenshot Automator

    Person(developer, "Developer")

    Container_Boundary(screenshotter, "AI Screenshot Automator") {
        Container(cli, "CLI Tool", "Bash/Node.js", "Command-line interface")
        Container(orchestrator, "Capture Orchestrator", "Node.js", "Coordinates screenshot capture")
        Container(macAutomation, "macOS Automation", "AppleScript", "Controls native macOS apps")
        Container(webAutomation, "Web Automation", "Playwright", "Controls web browsers")
        ContainerDb(config, "Configuration", "JSON Files", "Stores app configs")
        Container(markdownGen, "Markdown Generator", "Node.js", "Creates documentation")
    }

    System_Ext(filesystem, "File System", "Stores screenshots")
    System_Ext(git, "Git Repository", "Versions screenshots")

    Rel(developer, cli, "Runs commands", "Shell")
    Rel(cli, orchestrator, "Invokes", "Function calls")
    Rel(orchestrator, macAutomation, "Uses for native apps", "")
    Rel(orchestrator, webAutomation, "Uses for web apps", "")
    Rel(orchestrator, config, "Reads", "File I/O")
    Rel(orchestrator, markdownGen, "Generates docs", "")
    Rel(orchestrator, filesystem, "Saves screenshots to", "File I/O")
    Rel(markdownGen, git, "Commits to", "Git CLI")
```

**Output**: Save as `/docs/architecture/diagrams/c2-container.mmd`

---

## C3: Component Diagram

### Purpose
Break down each container into its major components and show their responsibilities and interactions.

### Audience
- Software architects
- Senior developers
- Code reviewers

### What to Include
- Major classes/modules within a container
- Interfaces between components
- External dependencies
- Data flow between components

### Mermaid Template

```mermaid
C4Component
    title Component Diagram - [Container Name]

    Container_Boundary(containerName, "[Container Name]") {
        Component(controller, "API Controller", "Express Router", "Handles HTTP requests")
        Component(service, "Business Logic Service", "TypeScript Class", "Implements core logic")
        Component(repository, "Data Repository", "TypeScript Class", "Handles data access")
        Component(validator, "Input Validator", "Joi/Zod", "Validates requests")
        Component(mapper, "Data Mapper", "TypeScript", "Maps between DTOs and entities")
    }

    ContainerDb(database, "Database", "PostgreSQL")
    System_Ext(externalAPI, "External API")

    Rel(controller, validator, "Validates input", "")
    Rel(controller, service, "Calls", "")
    Rel(service, repository, "Reads/Writes data", "")
    Rel(service, mapper, "Maps data", "")
    Rel(repository, database, "SQL queries", "SQL")
    Rel(service, externalAPI, "Calls", "HTTPS")
```

### Example: AI Screenshot Automator - Capture Orchestrator

```mermaid
C4Component
    title Component Diagram - Capture Orchestrator

    Container_Boundary(orchestrator, "Capture Orchestrator") {
        Component(commandParser, "Command Parser", "TypeScript", "Parses CLI arguments")
        Component(configManager, "Config Manager", "TypeScript", "Loads and validates configs")
        Component(captureEngine, "Capture Engine", "TypeScript", "Coordinates captures")
        Component(platformDetector, "Platform Detector", "TypeScript", "Detects OS/platform")
        Component(screenshotHandler, "Screenshot Handler", "TypeScript", "Manages screenshot files")
        Component(beforeAfterManager, "Before/After Manager", "TypeScript", "Tracks states")
    }

    Container(macAutomation, "macOS Automation")
    Container(webAutomation, "Web Automation")
    ContainerDb(filesystem, "File System")

    Rel(commandParser, configManager, "Loads config", "")
    Rel(commandParser, captureEngine, "Initiates capture", "")
    Rel(captureEngine, platformDetector, "Detects platform", "")
    Rel(captureEngine, macAutomation, "Uses for macOS", "")
    Rel(captureEngine, webAutomation, "Uses for web", "")
    Rel(captureEngine, screenshotHandler, "Saves screenshots", "")
    Rel(beforeAfterManager, screenshotHandler, "Tracks states", "")
    Rel(screenshotHandler, filesystem, "Writes files", "")
```

**Output**: Save as `/docs/architecture/diagrams/c3-component-[container-name].mmd`

---

## C4: Code Diagram

### Purpose
Show the actual code structure - classes, interfaces, methods, and their relationships.

### Audience
- Developers implementing the code
- Code reviewers
- New team members onboarding

### What to Include
- Class diagrams (UML)
- Interfaces
- Important methods
- Inheritance relationships
- Composition relationships

### Mermaid Template

```mermaid
classDiagram
    class CaptureOrchestrator {
        -ConfigManager config
        -PlatformDetector detector
        -ScreenshotHandler handler
        +capture(options: CaptureOptions): Promise~Result~
        +compareBefore After(issueId: string): Promise~Comparison~
        -selectAutomationEngine(): AutomationEngine
    }

    class ConfigManager {
        -ConfigSchema schema
        +loadConfig(path: string): Config
        +validateConfig(config: Config): boolean
        +getPageConfig(pageName: string): PageConfig
    }

    class PlatformDetector {
        +detectPlatform(): Platform
        +isMacOS(): boolean
        +isWeb(): boolean
        +getBrowserType(): BrowserType
    }

    class ScreenshotHandler {
        -FileSystem fs
        +saveScreenshot(data: Buffer, path: string): Promise~void~
        +getBeforeScreenshot(issueId: string): Promise~string~
        +getAfterScreenshot(issueId: string): Promise~string~
        +generateComparison(before: string, after: string): Promise~Image~
    }

    interface AutomationEngine {
        <<interface>>
        +navigate(page: string): Promise~void~
        +click(selector: string): Promise~void~
        +capture(): Promise~Buffer~
    }

    class MacOSAutomation implements AutomationEngine {
        +navigate(page: string): Promise~void~
        +click(selector: string): Promise~void~
        +capture(): Promise~Buffer~
        -executeAppleScript(script: string): Promise~string~
    }

    class WebAutomation implements AutomationEngine {
        -Browser browser
        -Page page
        +navigate(page: string): Promise~void~
        +click(selector: string): Promise~void~
        +capture(): Promise~Buffer~
    }

    CaptureOrchestrator --> ConfigManager
    CaptureOrchestrator --> PlatformDetector
    CaptureOrchestrator --> ScreenshotHandler
    CaptureOrchestrator --> AutomationEngine
    MacOSAutomation ..|> AutomationEngine
    WebAutomation ..|> AutomationEngine
```

**Output**: Save as `/docs/architecture/diagrams/c4-code-[component-name].mmd`

---

## C4 Workflow Integration

### When to Create Each Diagram

#### Discovery Phase (Week 1-2)
- [ ] **C1: System Context** - During market research
  - Understand external dependencies
  - Map user personas
  - Identify integration points

#### Strategy Phase (Week 2-3)
- [ ] **C2: Container** - During technical architecture planning
  - Choose technology stack
  - Plan data storage
  - Design deployment architecture

#### Planning Phase (Week 3-4)
- [ ] **C3: Component** - Before sprint planning
  - Break down containers into components
  - Define interfaces
  - Plan implementation order

#### Execution Phase (Week 4+)
- [ ] **C4: Code** - During implementation
  - Create for complex components
  - Document class hierarchies
  - Guide code reviews

---

## Mermaid Diagram Standards

### File Naming Convention

```
/docs/architecture/diagrams/
├── c1-system-context.mmd
├── c2-container.mmd
├── c3-component-api.mmd
├── c3-component-frontend.mmd
├── c3-component-worker.mmd
├── c4-code-capture-engine.mmd
└── c4-code-automation-interface.mmd
```

### Rendering Diagrams

**In GitHub/GitLab**:
- Mermaid renders automatically in markdown
- Wrap in code fences with `mermaid` language

**Generating SVG**:
```bash
# Install mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Generate SVG from .mmd file
mmdc -i c1-system-context.mmd -o c1-system-context.svg

# Generate PNG
mmdc -i c1-system-context.mmd -o c1-system-context.png -b transparent
```

### Diagram Checklist

For each C4 level diagram:

- [ ] Title clearly states what is being shown
- [ ] Legend explains symbols (if complex)
- [ ] Technology choices labeled
- [ ] Relationships show direction and protocol
- [ ] External systems clearly marked
- [ ] Stored in `/docs/architecture/diagrams/`
- [ ] Referenced in architecture documentation
- [ ] Kept up to date with code changes

---

## Advanced C4 Patterns

### Sequence Diagrams for Workflows

Use alongside C4 to show **how** systems interact over time:

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Orchestrator
    participant macOS
    participant FileSystem

    User->>CLI: ai-doc --app MyApp --issue 002 --state before
    CLI->>Orchestrator: initiate_capture(issue: 002, state: before)
    Orchestrator->>macOS: activate_app(MyApp)
    macOS-->>Orchestrator: app_activated
    Orchestrator->>macOS: capture_window()
    macOS-->>Orchestrator: screenshot_buffer
    Orchestrator->>FileSystem: save(buffer, screenshots/002/before/)
    FileSystem-->>Orchestrator: saved
    Orchestrator-->>CLI: capture_complete
    CLI-->>User: ✓ Captured: 002/before/main-window.png
```

### State Machine Diagrams

Show state transitions:

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Capturing: start_capture()
    Capturing --> NavigatingApp: app_activated
    NavigatingApp --> CapturingScreen: page_loaded
    CapturingScreen --> SavingFile: screenshot_taken
    SavingFile --> GeneratingDocs: file_saved
    GeneratingDocs --> Idle: docs_generated

    Capturing --> Error: app_not_found
    NavigatingApp --> Error: navigation_failed
    CapturingScreen --> Error: capture_failed
    Error --> Idle: retry()
    Error --> [*]: abort()
```

### Deployment Diagrams

Show physical deployment:

```mermaid
graph TB
    subgraph Developer_Machine[Developer's Machine]
        CLI[CLI Tool]
        Config[Config Files]
        Screenshots[Local Screenshots]
    end

    subgraph CI_CD[CI/CD Pipeline - GitHub Actions]
        Worker[Action Runner]
        Playwright[Headless Browser]
    end

    subgraph Storage[Cloud Storage]
        S3[AWS S3]
        GitHub[GitHub Repository]
    end

    CLI --> Screenshots
    CLI --> Config
    Worker --> Playwright
    Worker --> S3
    Screenshots --> GitHub
    S3 --> GitHub
```

---

## C4 → ADR Integration

### Linking Architecture Decisions to Diagrams

When writing ADRs, reference specific C4 diagrams:

**Example ADR**:
```markdown
# ADR-003: Use Playwright for Web Automation

## Context

See C2 Container Diagram (`c2-container.mmd`) - we need a web automation engine for the Web Automation container.

## Decision

We will use Playwright over Puppeteer or Selenium.

## Consequences

### Positive
- See C3 Component Diagram (`c3-component-web-automation.mmd`)
- Unified API across browsers
- Better debugging tools
- Active development

### Updated Diagrams
- `c2-container.mmd` - Updated Web Automation container
- `c3-component-web-automation.mmd` - Created component breakdown
```

---

## C4 Model Checklist

### For Every New Project

- [ ] **Week 1**: Create C1 System Context
  - Identify all external systems
  - Map all user types
  - Document integration points

- [ ] **Week 2**: Create C2 Container
  - Choose technology stack
  - Plan database architecture
  - Design API structure

- [ ] **Week 3**: Create C3 Components (for each container)
  - Break down frontend components
  - Break down API components
  - Break down worker components

- [ ] **Week 4+**: Create C4 Code (for complex components)
  - Document key interfaces
  - Show inheritance hierarchies
  - Guide implementation

### Ongoing Maintenance

- [ ] Update diagrams when architecture changes
- [ ] Review diagrams in code reviews
- [ ] Link diagrams to ADRs
- [ ] Use diagrams in onboarding
- [ ] Generate SVGs for presentations

---

## C4 Model Resources

### Official Resources
- **C4 Model**: https://c4model.com/
- **Mermaid Docs**: https://mermaid.js.org/
- **Mermaid Live Editor**: https://mermaid.live/

### AZ1.AI CODITECT Standards
- All diagrams must use Mermaid (no proprietary tools)
- Store as `.mmd` files in version control
- Generate `.svg` for presentations
- Keep diagrams close to code (in `/docs/architecture/`)
- Update with each architectural change

---

## Copyright Notice

**Copyright © 2025 AZ1.AI INC. All Rights Reserved.**

This C4 Architecture Methodology document is proprietary to AZ1.AI INC. and is part of the AZ1.AI CODITECT Project Management & Development Platform.

**Developed by**: Hal Casteel, Founder/CEO/CTO, AZ1.AI INC.

**Licensed under**: AZ1.AI CODITECT Platform License

**Unauthorized reproduction, distribution, or use is prohibited.**

For licensing inquiries: [Contact Information]

---

**AZ1.AI CODITECT** - Systematic Excellence in Software Development
