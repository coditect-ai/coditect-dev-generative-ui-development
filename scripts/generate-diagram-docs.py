#!/usr/bin/env python3
"""
Generate comprehensive markdown documentation for all CODITECT architecture diagrams.

This script creates individual .md files for each .mmd diagram, following the
established pattern from Phase 1 documentation.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Base directory
BASE_DIR = Path("/Users/halcasteel/PROJECTS/coditect-rollout-master/diagrams")

# Phase configurations
PHASES = {
    "phase-2-ide-cloud": {
        "number": 2,
        "name": "Full IDE in the Cloud",
        "status": "✅ Deployed (Production)",
        "url": "https://coditect.ai",
        "diagrams": [
            ("phase2-c1-system-context", "C1 - System Context"),
            ("phase2-c2-container", "C2 - Container"),
            ("phase2-c3-theia-ide", "C3 - Component (Theia IDE)"),
        ]
    },
    "phase-3-workflow-analyzer": {
        "number": 3,
        "name": "Workflow Analyzer Integration",
        "status": "✅ Deployed",
        "diagrams": [
            ("phase3-c1-system-context", "C1 - System Context"),
            ("phase3-c2-container", "C2 - Container"),
            ("phase3-c3-orchestration", "C3 - Component (Orchestration)"),
        ]
    },
    "phase-4-license-management": {
        "number": 4,
        "name": "License & User Management",
        "status": "🔨 In Development",
        "diagrams": [
            ("phase4-c1-system-context", "C1 - System Context"),
            ("phase4-c2-container", "C2 - Container"),
            ("phase4-c3-authentication", "C3 - Component (Authentication)"),
            ("phase4-c3-license-management", "C3 - Component (License Management)"),
            ("phase4-c3-session-management", "C3 - Component (Session Management)"),
        ]
    },
    "phase-5-marketplace-analytics": {
        "number": 5,
        "name": "Agent Marketplace & Analytics",
        "status": "📋 Planned",
        "diagrams": [
            ("phase5-c1-system-context", "C1 - System Context"),
            ("phase5-c2-marketplace", "C2 - Container (Marketplace)"),
            ("phase5-c2-analytics", "C2 - Container (Analytics)"),
        ]
    },
    "phase-6-orchestration": {
        "number": 6,
        "name": "Multi-Agent Orchestration",
        "status": "📋 Planned (CRITICAL for 95% autonomy)",
        "diagrams": [
            ("phase6-c1-system-context", "C1 - System Context"),
            ("phase6-c2-infrastructure", "C2 - Container (Infrastructure)"),
            ("phase6-c3-inter-agent-communication", "C3 - Component (Inter-Agent Communication)"),
        ]
    },
    "phase-7-enterprise-scale": {
        "number": 7,
        "name": "Enterprise Scale & Self-Service",
        "status": "📋 Planned (GTM Phase)",
        "diagrams": [
            ("phase7-c1-system-context", "C1 - System Context"),
            ("phase7-c2-self-service", "C2 - Container (Self-Service)"),
            ("phase7-c3-auto-provisioning", "C3 - Component (Auto Provisioning)"),
            ("phase7-c3-offboarding", "C3 - Component (Offboarding)"),
        ]
    },
}

def read_file(filepath: Path) -> str:
    """Read file content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_diagram_type(filename: str) -> str:
    """Extract diagram level (C1, C2, C3) from filename."""
    if '-c1-' in filename:
        return 'C1 - System Context'
    elif '-c2-' in filename:
        return 'C2 - Container'
    elif '-c3-' in filename:
        return 'C3 - Component'
    return 'Unknown'

def generate_introduction(phase_num: int, phase_name: str, diagram_type: str, diagram_name: str) -> str:
    """Generate introduction section."""
    level_descriptions = {
        'C1': 'highest-level view',
        'C2': 'container architecture',
        'C3': 'component-level structure'
    }

    level = diagram_type.split(' - ')[0]
    desc = level_descriptions.get(level, 'detailed view')

    return f"""## Introduction

This diagram provides the **{desc}** of the CODITECT Phase {phase_num} architecture: {phase_name}. It shows the major systems, their interactions, and key architectural decisions at this phase of platform evolution.

**Key Insight:** Phase {phase_num} builds upon previous phases, adding critical capabilities that enable the next level of platform maturity.

## What This Diagram Shows

- **Architecture Level:** {diagram_type}
- **Phase Focus:** {phase_name}
- **Key Components:** Major systems and their relationships
- **Integration Points:** External dependencies and data flows
"""

def generate_markdown(
    phase_key: str,
    diagram_name: str,
    diagram_type: str,
    mermaid_content: str,
    phase_readme: str
) -> str:
    """Generate comprehensive markdown documentation for a diagram."""

    phase_info = PHASES[phase_key]
    phase_num = phase_info["number"]
    phase_name = phase_info["name"]
    status = phase_info["status"]

    # Extract relevant sections from phase README
    key_elements = extract_key_elements(phase_readme, diagram_name)

    template = f"""# Phase {phase_num} - {diagram_type.split(' - ')[1]}

**Diagram Type:** {diagram_type}
**Phase:** {phase_num} - {phase_name}
**Status:** {status}
**Last Updated:** 2025-11-20

{generate_introduction(phase_num, phase_name, diagram_type, diagram_name)}

## Key Elements

{key_elements}

## Detailed Explanation

### Architecture Overview

Phase {phase_num} introduces critical capabilities that advance the CODITECT platform toward full autonomous operation. This diagram shows how these components work together to deliver {phase_name.lower()}.

### Component Interactions

The components shown in this diagram interact through well-defined interfaces:
- **API Calls:** RESTful APIs for synchronous operations
- **Message Passing:** Asynchronous communication via message bus (Phase 6+)
- **Data Flows:** Persistent storage and state management
- **Authentication:** Secure access control and authorization

## Architecture Patterns

### Pattern 1: Scalable Architecture
**Decision:** Design for horizontal scaling from the start
**Rationale:**
- Supports growth from 100 to 50,000+ users
- Enables independent component scaling
- Maintains performance under load
- Reduces operational complexity

### Pattern 2: Security First
**Decision:** Built-in security at every layer
**Rationale:**
- Enterprise-grade requirements
- Multi-tenant isolation
- Compliance (SOC2, GDPR)
- Zero-trust architecture

### Pattern 3: Cloud-Native Design
**Decision:** Kubernetes-based orchestration
**Rationale:**
- Platform portability
- Auto-scaling and self-healing
- Industry-standard deployment
- DevOps automation

## Technical Details

### Technology Stack

**Platform:**
- Google Kubernetes Engine (GKE)
- Cloud Load Balancer
- Persistent Disk SSD storage

**Runtime:**
- Rust/Actix-web backend
- React 18 frontend
- FoundationDB/PostgreSQL data layer

**Observability:**
- Prometheus metrics
- Grafana dashboards
- Structured logging

### Performance Characteristics

**Latency Targets:**
- API responses: <200ms (p95)
- Page loads: <2 seconds
- Agent execution: 2-10 seconds (LLM-bound)

**Scalability:**
- Horizontal pod scaling
- Database read replicas
- CDN for static assets

## Limitations & Future Evolution

### Current Phase Limitations

{generate_limitations(phase_num)}

### Next Phase Additions

{generate_next_phase(phase_num)}

## Diagram

```mermaid
{mermaid_content.strip()}
```

## Related Documentation

- **Phase Overview:** [README.md](README.md)
{generate_related_links(phase_key, diagram_name)}
- **Architecture Evolution:** [../../docs/CODITECT-C4-ARCHITECTURE-EVOLUTION.md](../../docs/CODITECT-C4-ARCHITECTURE-EVOLUTION.md)
- **Master Plan:** [../../docs/CODITECT-MASTER-ORCHESTRATION-PLAN.md](../../docs/CODITECT-MASTER-ORCHESTRATION-PLAN.md)

---

**Maintained By:** AZ1.AI CODITECT Team
**Repository:** https://github.com/coditect-ai/coditect-rollout-master
**Framework:** https://github.com/coditect-ai/coditect-core
"""

    return template

def extract_key_elements(phase_readme: str, diagram_name: str) -> str:
    """Extract key elements from phase README."""
    # This is a simplified version - in production, would parse README more intelligently
    return """### Users
- Developers accessing the platform
- Team administrators managing licenses
- System operators monitoring performance

### Systems
- **Primary Platform:** Core CODITECT services
- **External Dependencies:** Cloud providers, APIs, integrations
- **Data Stores:** Databases, caching layers, persistent storage

### Integrations
- GitHub for source control
- Anthropic Claude API for AI agents
- Extension registries (NPM, Open VSX)
"""

def generate_limitations(phase_num: int) -> str:
    """Generate limitations section based on phase."""
    if phase_num < 4:
        return """❌ **No Centralized Authentication**
- Basic JWT only
- No SSO integration
- Limited access control

❌ **No License Management**
- Open access (no tiers)
- No usage quotas
- No billing integration"""
    elif phase_num < 6:
        return """❌ **No Inter-Agent Communication**
- Agents cannot invoke each other
- Human-in-the-loop required
- Blocks autonomous workflows

❌ **Limited Analytics**
- Basic usage tracking only
- No behavioral insights
- No optimization recommendations"""
    else:
        return """❌ **Not Yet Enterprise-Ready**
- No self-service onboarding
- Manual provisioning required
- Limited compliance features"""

def generate_next_phase(phase_num: int) -> str:
    """Generate next phase additions."""
    if phase_num < 7:
        return f"""Phase {phase_num + 1} adds:
- Enhanced capabilities for next maturity level
- Additional infrastructure components
- Improved automation and intelligence
- Expanded platform features"""
    else:
        return """Future Evolution:
- Global expansion (multi-region)
- Advanced AI capabilities
- Ecosystem integrations
- Community features"""

def generate_related_links(phase_key: str, diagram_name: str) -> str:
    """Generate related documentation links."""
    phase_diagrams = PHASES[phase_key]["diagrams"]
    links = []
    for diag_name, diag_type in phase_diagrams:
        if diag_name != diagram_name:
            links.append(f"- **{diag_type}:** [{diag_name}.md]({diag_name}.md)")
    return '\n'.join(links)

def main():
    """Generate documentation for all phase diagrams."""
    print("🚀 CODITECT Diagram Documentation Generator")
    print("=" * 60)

    total_created = 0
    total_skipped = 0

    for phase_key, phase_info in PHASES.items():
        phase_dir = BASE_DIR / phase_key
        if not phase_dir.exists():
            print(f"⚠️  Phase directory not found: {phase_dir}")
            continue

        # Read phase README for context
        readme_path = phase_dir / "README.md"
        phase_readme = read_file(readme_path) if readme_path.exists() else ""

        print(f"\n📂 Phase {phase_info['number']}: {phase_info['name']}")
        print(f"   Status: {phase_info['status']}")

        for diagram_name, diagram_type in phase_info["diagrams"]:
            mmd_file = phase_dir / f"{diagram_name}.mmd"
            md_file = phase_dir / f"{diagram_name}.md"

            if not mmd_file.exists():
                print(f"   ⚠️  Mermaid file not found: {mmd_file}")
                continue

            if md_file.exists():
                print(f"   ⏭️  Skipping (exists): {md_file.name}")
                total_skipped += 1
                continue

            # Read mermaid content
            mermaid_content = read_file(mmd_file)

            # Generate markdown documentation
            markdown_content = generate_markdown(
                phase_key,
                diagram_name,
                diagram_type,
                mermaid_content,
                phase_readme
            )

            # Write markdown file
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"   ✅ Created: {md_file.name}")
            total_created += 1

    print("\n" + "=" * 60)
    print(f"✅ Documentation generation complete!")
    print(f"   Created: {total_created} files")
    print(f"   Skipped: {total_skipped} files (already exist)")
    print(f"   Total: {total_created + total_skipped} files")

if __name__ == "__main__":
    main()
