#!/usr/bin/env python3
"""
Update phase README files to link to diagram documentation.

This script updates the "Diagrams" section in each phase README to link to
the comprehensive markdown documentation files for each diagram.
"""

import re
from pathlib import Path

BASE_DIR = Path("/Users/halcasteel/PROJECTS/coditect-rollout-master/diagrams")

PHASE_DIAGRAM_LINKS = {
    "phase-1-claude-framework": [
        ("phase1-c1-system-context", "C1 - System Context Diagram", "Shows how developers interact with the CODITECT framework and external systems"),
        ("phase1-c2-container", "C2 - Container Diagram", "Shows the internal structure of the .coditect directory"),
        ("phase1-c3-agent-execution", "C3 - Component Diagram (Agent Execution)", "Shows how agents are discovered, dispatched, and executed"),
    ],
    "phase-2-ide-cloud": [
        ("phase2-c1-system-context", "C1 - System Context Diagram", "Shows how users access the cloud IDE and external integrations"),
        ("phase2-c2-container", "C2 - Container Diagram", "Shows the GKE deployment architecture"),
        ("phase2-c3-theia-ide", "C3 - Component Diagram (Theia IDE)", "Shows internal structure of Eclipse Theia IDE"),
    ],
    "phase-3-workflow-analyzer": [
        ("phase3-c1-system-context", "C1 - System Context Diagram", "Shows the 8-agent workflow analysis platform integration"),
        ("phase3-c2-container", "C2 - Container Diagram", "Shows backend services and database architecture"),
        ("phase3-c3-orchestration", "C3 - Component Diagram (Orchestration)", "Shows the 8-agent workflow analysis system"),
    ],
    "phase-4-license-management": [
        ("phase4-c1-system-context", "C1 - System Context Diagram", "Shows unified platform with authentication and licensing"),
        ("phase4-c2-container", "C2 - Container Diagram", "Shows backend services architecture"),
        ("phase4-c3-authentication", "C3 - Component Diagram (Authentication)", "Shows JWT authentication and authorization flow"),
        ("phase4-c3-license-management", "C3 - Component Diagram (License Management)", "Shows license tiers and usage tracking"),
        ("phase4-c3-session-management", "C3 - Component Diagram (Session Management)", "Shows cross-system state synchronization"),
    ],
    "phase-5-marketplace-analytics": [
        ("phase5-c1-system-context", "C1 - System Context Diagram", "Shows marketplace and analytics platform integration"),
        ("phase5-c2-marketplace", "C2 - Container Diagram (Marketplace)", "Shows agent marketplace architecture"),
        ("phase5-c2-analytics", "C2 - Container Diagram (Analytics)", "Shows ClickHouse analytics platform"),
    ],
    "phase-6-orchestration": [
        ("phase6-c1-system-context", "C1 - System Context Diagram", "Shows multi-agent orchestration platform (95% autonomy!)"),
        ("phase6-c2-infrastructure", "C2 - Container Diagram (Infrastructure)", "Shows RabbitMQ, Redis, and orchestration services"),
        ("phase6-c3-inter-agent-communication", "C3 - Component Diagram (Inter-Agent Communication)", "Shows message bus and task queue for autonomous operation"),
    ],
    "phase-7-enterprise-scale": [
        ("phase7-c1-system-context", "C1 - System Context Diagram", "Shows enterprise platform with all user types and SSO"),
        ("phase7-c2-self-service", "C2 - Container Diagram (Self-Service)", "Shows onboarding and offboarding flows"),
        ("phase7-c3-auto-provisioning", "C3 - Component Diagram (Auto Provisioning)", "Shows automated resource provisioning (<60 seconds)"),
        ("phase7-c3-offboarding", "C3 - Component Diagram (Offboarding)", "Shows automated data export and cleanup"),
    ],
}

def update_diagrams_section(readme_path: Path, phase_key: str) -> bool:
    """Update the Diagrams section in a phase README."""

    if not readme_path.exists():
        print(f"   ⚠️  README not found: {readme_path}")
        return False

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Diagrams section
    diagrams_pattern = r'## Diagrams\n\n(.*?)(?=\n##|\n---|\Z)'
    match = re.search(diagrams_pattern, content, re.DOTALL)

    if not match:
        print(f"   ⚠️  No Diagrams section found")
        return False

    # Generate new diagrams section
    diagram_links = PHASE_DIAGRAM_LINKS.get(phase_key, [])
    new_diagrams_content = "## Diagrams\n\n"

    for filename, title, description in diagram_links:
        new_diagrams_content += f"### {title}\n"
        new_diagrams_content += f"**[📄 View Documentation]({filename}.md)** | [📊 View Diagram]({filename}.mmd)\n\n"
        new_diagrams_content += f"{description}\n\n"

    # Replace the old Diagrams section with the new one
    new_content = re.sub(
        diagrams_pattern,
        new_diagrams_content,
        content,
        flags=re.DOTALL
    )

    # Write back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    """Update all phase README files."""
    print("🔄 Updating Phase README Files")
    print("=" * 60)

    updated_count = 0
    failed_count = 0

    for phase_key in PHASE_DIAGRAM_LINKS.keys():
        phase_dir = BASE_DIR / phase_key
        readme_path = phase_dir / "README.md"

        print(f"\n📂 {phase_key}")

        if update_diagrams_section(readme_path, phase_key):
            print(f"   ✅ Updated diagrams section")
            updated_count += 1
        else:
            print(f"   ❌ Failed to update")
            failed_count += 1

    print("\n" + "=" * 60)
    print(f"✅ Update complete!")
    print(f"   Updated: {updated_count} READMEs")
    print(f"   Failed: {failed_count} READMEs")

if __name__ == "__main__":
    main()
