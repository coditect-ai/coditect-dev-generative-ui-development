#!/bin/bash
# Organize extracted diagrams into phase directories

cd diagrams/mermaid-source

# Phase 1 diagrams (already created manually, skip 01-03)
# diagram-01: Phase 1 C1
# diagram-02: Phase 1 C2
# diagram-03: Phase 1 C3

# Phase 2 diagrams (already created manually, skip 04-06)
# diagram-04: Phase 2 C1
# diagram-05: Phase 2 C2
# diagram-06: Phase 2 C3

# Phase 3 diagrams
cp diagram-07.mmd ../phase-3-workflow-analyzer/phase3-c1-system-context.mmd
cp diagram-08.mmd ../phase-3-workflow-analyzer/phase3-c2-container.mmd
cp diagram-09.mmd ../phase-3-workflow-analyzer/phase3-c3-orchestration.mmd

# Phase 4 diagrams
cp diagram-10.mmd ../phase-4-license-management/phase4-c1-system-context.mmd
cp diagram-11.mmd ../phase-4-license-management/phase4-c2-container.mmd
cp diagram-12.mmd ../phase-4-license-management/phase4-c3-authentication.mmd
cp diagram-13.mmd ../phase-4-license-management/phase4-c3-license-management.mmd
cp diagram-14.mmd ../phase-4-license-management/phase4-c3-session-management.mmd

# Phase 5 diagrams
cp diagram-15.mmd ../phase-5-marketplace-analytics/phase5-c1-system-context.mmd
cp diagram-16.mmd ../phase-5-marketplace-analytics/phase5-c2-marketplace.mmd
cp diagram-17.mmd ../phase-5-marketplace-analytics/phase5-c2-analytics.mmd

# Phase 6 diagrams
cp diagram-18.mmd ../phase-6-orchestration/phase6-c1-system-context.mmd
cp diagram-19.mmd ../phase-6-orchestration/phase6-c2-infrastructure.mmd
cp diagram-20.mmd ../phase-6-orchestration/phase6-c3-inter-agent-communication.mmd

# Phase 7 diagrams
cp diagram-21.mmd ../phase-7-enterprise-scale/phase7-c1-system-context.mmd
cp diagram-22.mmd ../phase-7-enterprise-scale/phase7-c2-self-service.mmd
cp diagram-23.mmd ../phase-7-enterprise-scale/phase7-c3-auto-provisioning.mmd
cp diagram-24.mmd ../phase-7-enterprise-scale/phase7-c3-offboarding.mmd

echo "Diagram organization complete!"
