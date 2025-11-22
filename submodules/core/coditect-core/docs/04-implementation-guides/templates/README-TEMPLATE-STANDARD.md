# README Standardization Template

## Overview

This template defines the standard structure for all CODITECT submodule README.md files. The goal is to ensure consistency, clarity, and futureproofing across all 42 submodules.

---

## Standard README Template

```markdown
# {REPO_NAME}

**{CATEGORY} Repository - AZ1.AI CODITECT Ecosystem**

---

## Overview

{Brief 2-3 sentence description of what this repository does and its role in the CODITECT ecosystem.}

**Status:** {Active | P0 | P1 | Archive | In Development}
**Category:** {core | cloud | dev | market | docs | ops | gtm | labs}
**Priority:** {P0 | P1 | P2}

---

## Purpose

{Detailed explanation of:}
- What problem this repository solves
- Who uses it (developers, users, operators)
- How it fits into the larger CODITECT platform

---

## Key Features

- **Feature 1** - Description
- **Feature 2** - Description
- **Feature 3** - Description

---

## Technology Stack

{List primary technologies used}

- **Language:** {Python 3.x | TypeScript | Rust | etc.}
- **Framework:** {FastAPI | React | Next.js | etc.}
- **Database:** {PostgreSQL | Redis | etc.} (if applicable)
- **Infrastructure:** {GCP | Terraform | Docker | etc.} (if applicable)

---

## Quick Start

### Prerequisites

- {Required software/tools}
- {Environment requirements}
- {Dependencies}

### Installation

```bash
# Clone repository
git clone https://github.com/coditect-ai/{repo-name}.git
cd {repo-name}

# Install dependencies
{installation commands}

# Run
{run commands}
```

### Development

```bash
# Run tests
{test commands}

# Build
{build commands}

# Lint
{lint commands}
```

---

## Directory Structure

```
{repo-name}/
├── .coditect -> ../../../.coditect    # Distributed intelligence symlink
├── .claude -> .coditect               # Claude Code compatibility
├── src/                               # Source code
├── tests/                             # Test suite
├── docs/                              # Documentation
├── scripts/                           # Utility scripts
├── README.md                          # This file
├── CLAUDE.md                          # AI agent configuration
├── PROJECT-PLAN.md                    # Project plan (if applicable)
└── TASKLIST.md                        # Task tracking (if applicable)
```

---

## Distributed Intelligence

This repository is part of the CODITECT distributed intelligence architecture:

```
.coditect -> ../../../.coditect  # Links to master brain
.claude -> .coditect             # Claude Code compatibility
```

**Benefits:**
- Access to 50 specialized AI agents
- 72 slash commands available
- 24 reusable skills
- Consistent development patterns across all projects

**Learn more:** [WHAT-IS-CODITECT.md](https://github.com/coditect-ai/coditect-core/blob/main/WHAT-IS-CODITECT.md)

---

## Integration with CODITECT Platform

### Dependencies

{List other CODITECT repositories this depends on}

- [coditect-core](../core/coditect-core) - Core framework
- {Other dependencies}

### Dependents

{List repositories that depend on this one}

- {Dependent repos}

---

## Development Guidelines

### Code Style

- Follow {language} best practices
- Use {linting tool} for code quality
- Maintain test coverage above {X}%

### Commit Messages

Follow conventional commit format:
```
type(scope): description

feat: new feature
fix: bug fix
docs: documentation
refactor: code refactoring
test: adding tests
chore: maintenance
```

### Pull Requests

1. Create feature branch from `main`
2. Write tests for new functionality
3. Update documentation as needed
4. Request review from team

---

## Testing

```bash
# Run all tests
{test command}

# Run specific test
{specific test command}

# Generate coverage report
{coverage command}
```

---

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - AI agent configuration and context
- **[docs/](docs/)** - Additional documentation (if applicable)
- **[Architecture Diagrams](docs/architecture/)** - System diagrams (if applicable)

---

## Related Resources

- **Master Repository:** [coditect-rollout-master](https://github.com/coditect-ai/coditect-rollout-master)
- **Core Framework:** [coditect-core](https://github.com/coditect-ai/coditect-core)
- **Documentation Site:** [docs.coditect.ai](https://docs.coditect.ai) (when available)

---

## Contributing

See individual sub-project READMEs for contribution guidelines.

For CODITECT-wide contribution guidelines, see the [master repository](https://github.com/coditect-ai/coditect-rollout-master).

---

## License

Copyright (C) 2025 AZ1.AI INC. All Rights Reserved.

**PROPRIETARY AND CONFIDENTIAL** - This repository contains AZ1.AI INC. trade secrets and confidential information. Unauthorized copying, transfer, or use is strictly prohibited.

---

*Built with Excellence by AZ1.AI CODITECT*
*Systematic Development. Continuous Context. Exceptional Results.*
```

---

## Section Requirements by Category

### Core Repositories (core/)

Required sections:
- All standard sections
- Framework integration details
- Agent/skill/command inventory (for dotclaude)
- Training materials reference (for dotclaude)

### Cloud Repositories (cloud/)

Required sections:
- All standard sections
- API documentation reference
- Deployment instructions
- Environment configuration
- Health check endpoints

### Development Tools (dev/)

Required sections:
- All standard sections
- CLI usage examples
- Configuration options
- Input/output formats

### Marketplace (market/)

Required sections:
- All standard sections
- User-facing features
- Business logic overview
- Integration points

### Documentation (docs/)

Required sections:
- All standard sections
- Content structure overview
- Publishing workflow
- Style guide reference

### Operations (ops/)

Required sections:
- All standard sections
- Operational procedures
- Monitoring/alerting
- Runbook references

### Go-to-Market (gtm/)

Required sections:
- All standard sections
- Target audience
- Business context
- Campaign/strategy overview

### Labs/Research (labs/)

Required sections:
- All standard sections
- Research objectives
- Methodology
- Findings/results summary
- Future work

---

## Quality Criteria

A well-standardized README should:

1. **Complete** - All required sections present
2. **Accurate** - Information is current and correct
3. **Clear** - Easy to understand for new developers
4. **Actionable** - Quick start works without issues
5. **Consistent** - Follows template structure
6. **Futureproofed** - Includes placeholders for planned features
7. **Linked** - References related repositories and docs

---

## File Size Guidelines

- **Minimum:** 100 lines (basic project)
- **Typical:** 150-300 lines (standard project)
- **Maximum:** 600 lines (complex project with extensive docs)

If README exceeds 600 lines, consider:
- Moving detailed content to docs/ directory
- Creating separate guides for specific topics
- Linking to external documentation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-19 | Initial template creation |

---

*This template ensures consistency across all CODITECT repositories while maintaining flexibility for project-specific needs.*
