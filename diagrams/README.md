# CODITECT Architecture Diagrams

## Overview

This directory contains **C4 Model architecture diagrams** for the CODITECT platform, documenting the evolution from Phase 1 (local .claude framework) through Phase 7 (enterprise scale).

**Methodology:** C4 Model (Context → Container → Component → Code)

## Directory Structure

```
diagrams/
├── mermaid-source/          # Master mermaid diagram source files
├── phase-1-claude-framework/    # Phase 1: Local .claude framework
├── phase-2-ide-cloud/           # Phase 2: Browser-based IDE in cloud
├── phase-3-workflow-analyzer/   # Phase 3: Workflow analysis integration
├── phase-4-license-management/  # Phase 4: Auth, licensing, sessions
├── phase-5-marketplace-analytics/ # Phase 5: Agent marketplace & analytics
├── phase-6-orchestration/       # Phase 6: Multi-agent orchestration
└── phase-7-enterprise-scale/    # Phase 7: Enterprise features & scale
```

## Diagram Naming Convention

All diagrams follow this naming pattern:

```
{phase}-{level}-{component}-{variant}.mmd
```

**Examples:**
- `phase1-c1-system-context.mmd` - Phase 1, C1 level, system context diagram
- `phase4-c3-authentication-flow.mmd` - Phase 4, C3 level, authentication flow
- `phase6-c2-orchestration-infrastructure.mmd` - Phase 6, C2 level, orchestration infrastructure

## C4 Model Levels

### C1 - System Context
**Who uses the system and what external systems does it interact with?**
- Focus: Users, external dependencies
- Audience: Everyone (technical and non-technical)
- Detail Level: Highest level overview

### C2 - Container
**What are the major building blocks and how do they communicate?**
- Focus: Applications, data stores, microservices
- Audience: Technical stakeholders
- Detail Level: Deployment architecture

### C3 - Component
**What components exist inside each container?**
- Focus: Major structural building blocks
- Audience: Developers, architects
- Detail Level: Code organization

### C4 - Code (optional)
**How are components implemented?**
- Focus: Classes, interfaces, implementation details
- Audience: Developers working on specific components
- Detail Level: Code-level details

## Phase Overview

| Phase | Status | User Scale | Timeline | Focus |
|-------|--------|-----------|----------|-------|
| **1** | ✅ Active | <5 | Current | .claude Framework (Local) |
| **2** | ✅ Deployed | Public | Current | IDE in Cloud (coditect.ai) |
| **3** | ✅ Deployed | Public | Current | Workflow Analyzer |
| **4** | 🔨 Planned | 100-1K | Mo 2-4 | License/User/Session Management |
| **5** | 📋 Planned | 1K-5K | Mo 7-9 | Marketplace & Analytics |
| **6** | 📋 Planned | 5K-10K | Mo 4-7 | Multi-Agent Orchestration |
| **7** | 📋 Planned | 10K-50K+ | Mo 9-12 | Enterprise Scale & Self-Service |

## Usage

### Viewing Diagrams

**Option 1: Mermaid Live Editor**
1. Visit https://mermaid.live/
2. Copy/paste diagram content
3. View rendered diagram

**Option 2: VS Code Extension**
1. Install "Markdown Preview Mermaid Support" extension
2. Open any .mmd file
3. Use preview pane

**Option 3: Command Line (mermaid-cli)**
```bash
# Install
npm install -g @mermaid-js/mermaid-cli

# Export to SVG
mmdc -i phase1-c1-system-context.mmd -o phase1-c1-system-context.svg

# Export to PNG
mmdc -i phase1-c1-system-context.mmd -o phase1-c1-system-context.png

# Export to PDF
mmdc -i phase1-c1-system-context.mmd -o phase1-c1-system-context.pdf
```

### Embedding in Documentation

**Markdown:**
```markdown
![Phase 1 System Context](diagrams/phase-1-claude-framework/phase1-c1-system-context.svg)
```

**HTML:**
```html
<img src="diagrams/phase-1-claude-framework/phase1-c1-system-context.svg" alt="Phase 1 System Context">
```

## Diagram Count by Phase

- **Phase 1:** 3 diagrams (C1, C2, C3)
- **Phase 2:** 3 diagrams (C1, C2, C3)
- **Phase 3:** 3 diagrams (C1, C2, C3)
- **Phase 4:** 5 diagrams (C1, C2, 3×C3)
- **Phase 5:** 3 diagrams (C1, 2×C2)
- **Phase 6:** 3 diagrams (C1, C2, C3)
- **Phase 7:** 4 diagrams (C1, C2, 2×C3)
- **Master:** 1 diagram (Gantt chart)

**Total:** 25 architecture diagrams

## Cross-References

These diagrams are referenced in the following documentation:

- **docs/CODITECT-C4-ARCHITECTURE-EVOLUTION.md** - Complete architecture evolution (source of all diagrams)
- **docs/CODITECT-MASTER-ORCHESTRATION-PLAN.md** - Master orchestration and governance
- **docs/CODITECT-ROLLOUT-MASTER-PLAN.md** - Detailed implementation plan
- **CLAUDE.md** - AI agent configuration and context

## Maintenance

**When to Update Diagrams:**
1. Architecture changes (new containers, components)
2. Technology stack changes (PostgreSQL → ClickHouse)
3. Integration points added/removed
4. Phase transitions (e.g., Phase 2 → Phase 3)
5. Security model changes
6. Scaling strategy adjustments

**Update Process:**
1. Edit .mmd files in appropriate phase directory
2. Test diagram renders correctly (mermaid.live)
3. Update this README if structure changes
4. Regenerate PNG/SVG exports if needed
5. Update cross-references in documentation
6. Commit changes with descriptive message

## Color Scheme

Diagrams use consistent colors for component types:

- **Primary Systems:** `#4A90E2` (blue)
- **Supporting Services:** `#50E3C2` (teal)
- **External Systems:** `#F5A623` (orange)
- **Data Stores:** `#BD10E0` (purple)
- **Security/Auth:** `#7ED321` (green)

## Export Formats

Each diagram can be exported to:
- **SVG** - Scalable Vector Graphics (best for web/docs)
- **PNG** - Raster image (best for presentations)
- **PDF** - Portable Document Format (best for printing)

## Questions?

For questions about:
- **Architecture:** See docs/CODITECT-C4-ARCHITECTURE-EVOLUTION.md
- **Implementation:** See docs/CODITECT-ROLLOUT-MASTER-PLAN.md
- **Diagram syntax:** See https://mermaid.js.org/

---

**Last Updated:** 2025-11-20
**Maintained By:** AZ1.AI CODITECT Team
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
