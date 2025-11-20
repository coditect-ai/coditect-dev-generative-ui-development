# CODITECT Repository Naming Convention

## Overview

All CODITECT repositories follow a standardized naming convention that organizes projects by category and provides clear, consistent identification across the ecosystem.

## Naming Pattern

```
coditect-{category}-{name}
```

**Components:**
- **coditect**: Organization prefix (always lowercase)
- **category**: One of 8 standardized categories (see below)
- **name**: Descriptive name for the specific project (lowercase, hyphenated)

## Categories

### 1. core - Core Framework Components
**Prefix:** `coditect-core-`

Essential framework components that form the foundation of CODITECT.

| Repository | Description |
|------------|-------------|
| coditect-core | Core .claude framework with agents, skills, commands |
| coditect-core-framework | CODITECT framework utilities and shared code |
| coditect-core-architecture | Architecture documentation and decisions |

### 2. cloud - Cloud Platform
**Prefix:** `coditect-cloud-`

Cloud-hosted services and infrastructure for CODITECT Cloud Platform.

| Repository | Description |
|------------|-------------|
| coditect-cloud-backend | FastAPI backend services |
| coditect-cloud-frontend | React TypeScript frontend |
| coditect-cloud-ide | Cloud IDE based on Eclipse Theia |
| coditect-cloud-infra | Terraform infrastructure as code |

### 3. dev - Developer Tools
**Prefix:** `coditect-dev-`

Developer-focused tools, utilities, and integrations.

| Repository | Description |
|------------|-------------|
| coditect-cli | Command-line interface tools |
| coditect-analytics | Usage analytics and metrics |
| coditect-automation | AI orchestration automation |
| coditect-dev-context | Context management tools |
| coditect-dev-intelligence | Development intelligence features |
| coditect-dev-pdf | PDF generation utilities |
| coditect-dev-audio2text | Audio transcription tools |
| coditect-dev-qrcode | QR code generation |

### 4. market - Marketplace
**Prefix:** `coditect-market-`

Agent marketplace and related commercial features.

| Repository | Description |
|------------|-------------|
| coditect-market-agents | Agent marketplace platform |
| coditect-market-activity | Activity feed and notifications |

### 5. docs - Documentation
**Prefix:** `coditect-docs-`

Documentation sites, training materials, and legal documents.

| Repository | Description |
|------------|-------------|
| coditect-docs-main | Main documentation site (Docusaurus) |
| coditect-docs-blog | Blog and content management |
| coditect-docs-training | Training materials and courses |
| coditect-docs-setup | Setup and installation guides |
| coditect-legal | Legal documents (EULA, Terms, Privacy) |

### 6. ops - Operations
**Prefix:** `coditect-ops-`

Operations, distribution, and licensing systems.

| Repository | Description |
|------------|-------------|
| coditect-ops-distribution | Installer and updater scripts |
| coditect-ops-license | License management system |
| coditect-ops-projects | Project orchestration (this repo) |

### 7. gtm - Go-to-Market
**Prefix:** `coditect-gtm-`

Marketing, sales, and customer-facing materials.

| Repository | Description |
|------------|-------------|
| coditect-gtm-strategy | GTM strategy and planning |
| coditect-gtm-legitimacy | Credibility and social proof |
| coditect-gtm-comms | Communications and messaging |
| coditect-gtm-crm | CRM integration |
| coditect-gtm-personas | User personas and research |
| coditect-gtm-customer-clipora | Customer success stories |

### 8. labs - Research & Experiments
**Prefix:** `coditect-labs-`

Research projects, experimental features, and archives.

| Repository | Description |
|------------|-------------|
| coditect-labs-agent-standards | Agent development standards |
| coditect-labs-agents-research | Multi-agent research |
| coditect-labs-claude-research | Claude integration research |
| coditect-labs-workflow | Workflow analysis tools |
| coditect-labs-screenshot | Screenshot automation |
| coditect-labs-v4-archive | V4 codebase archive |
| coditect-labs-multi-agent-rag | RAG research |
| coditect-labs-cli-web-arch | CLI/Web architecture research |
| coditect-labs-first-principles | First principles research |
| coditect-labs-learning | Learning experiments |
| coditect-labs-mcp-auth | MCP authentication research |

## Rules for New Repositories

### DO:
1. Always use lowercase for all components
2. Use hyphens to separate words within the name
3. Choose the most appropriate category from the 8 options
4. Keep names concise but descriptive (2-4 words)
5. Use singular nouns when possible (e.g., `workflow` not `workflows`)

### DON'T:
1. Use underscores or CamelCase
2. Include version numbers in repo names
3. Use abbreviations unless widely understood
4. Create repos outside the 8 category structure
5. Use special characters or spaces

## Examples

### Good Names:
- `coditect-dev-context` - Developer tool for context management
- `coditect-cloud-backend` - Cloud platform backend service
- `coditect-labs-mcp-auth` - Research project for MCP authentication
- `coditect-docs-training` - Training documentation

### Bad Names (Avoid):
- `Coditect-Dev-Context` - Wrong: uses CamelCase
- `coditect_dev_context` - Wrong: uses underscores
- `coditect-context` - Wrong: missing category
- `coditect-dev-context-v2` - Wrong: version in name
- `coditect-misc-stuff` - Wrong: vague name

## Migration Notes

When renaming existing repositories:

1. Update all internal references (CLAUDE.md, README.md, imports)
2. Update .gitmodules in parent repositories
3. Update GitHub repo settings and remote URLs
4. Communicate changes to team members
5. Update CI/CD configurations

## Directory Structure

In the master repository, submodules are organized by category:

```
coditect-rollout-master/
├── submodules/
│   ├── core/           # 3 repos
│   │   ├── coditect-core/
│   │   ├── coditect-core-framework/
│   │   └── coditect-core-architecture/
│   ├── cloud/          # 4 repos
│   │   ├── coditect-cloud-backend/
│   │   ├── coditect-cloud-frontend/
│   │   ├── coditect-cloud-ide/
│   │   └── coditect-cloud-infra/
│   ├── dev/            # 9 repos
│   │   ├── coditect-cli/
│   │   ├── coditect-analytics/
│   │   └── ...
│   ├── market/         # 2 repos
│   ├── docs/           # 5 repos
│   ├── ops/            # 3 repos
│   ├── gtm/            # 6 repos
│   └── labs/           # 11 repos
```

**Total: 42 submodules across 8 categories**

---

**Last Updated:** November 19, 2025
**Author:** AZ1.AI INC
