# CODITECT Submodule Update Process

**Version:** 1.0  
**Date:** 2025-11-16  
**Status:** Production Ready

## Overview

This document defines the standard process for updating all 19 submodules in the coditect-rollout-master repository in a consistent, dependency-aware order.

## Update Order (Dependency-Based)

### Tier 0: Framework (Foundation)
**Must be updated first** - All other projects depend on this
1. **coditect-core** - Core CODITECT framework (master brain)

### Tier 1: Core Infrastructure
**Update second** - Foundation for platform services
2. **coditect-framework** - Framework implementation
3. **coditect-infrastructure** - Infrastructure as code
4. **coditect-legal** - Legal documents and compliance

### Tier 2: Backend Services
**Update third** - Data layer and APIs
5. **coditect-cloud-backend** - FastAPI backend services
6. **coditect-analytics** - ClickHouse analytics
7. **coditect-automation** - Autonomous orchestration

### Tier 3: Frontend & CLI
**Update fourth** - User-facing interfaces
8. **coditect-cloud-frontend** - React frontend
9. **coditect-cli** - Python CLI tools
10. **coditect-docs** - Docusaurus documentation site

### Tier 4: Marketplace & Extensions
**Update fifth** - Extended platform features
11. **coditect-agent-marketplace** - Next.js marketplace
12. **coditect-activity-data-model-ui** - Activity feed UI

### Tier 5: Supporting Tools
**Update sixth** - Development and workflow tools
13. **az1.ai-coditect-ai-screenshot-automator** - Screenshot automation
14. **coditect-interactive-workflow-analyzer** - Workflow analysis
15. **Coditect-v5-multiple-LLM-IDE** - Multi-LLM IDE

### Tier 6: Strategic & Research
**Update seventh** - Strategy and research projects
16. **az1.ai-CODITECT.AI-GTM** - Go-to-market strategy
17. **az1.ai-coditect-agent-new-standard-development** - Agent standards
18. **NESTED-LEARNING-GOOGLE** - Educational technology research
19. **coditect-blog-application** - Blog and content

## Standard Update Workflow

For each submodule (in order):

```bash
1. Navigate to submodule directory
2. Check git status
3. Stage changes (.coditect, .claude, and any other modifications)
4. Commit with standardized message
5. Push to remote
6. Navigate back to master
7. Update submodule pointer in master
8. Continue to next submodule
```

## Commit Message Template

```
Add distributed intelligence symlinks

- .coditect → ../../.coditect (access to master CODITECT brain)
- .claude → .coditect (Claude Code compatibility)

Enables:
✅ Access to 49 agents, 189 skills, 72 commands
✅ Distributed intelligence architecture
✅ Consistent development experience across all projects

Part of: CODITECT Distributed Intelligence Rollout
Tier: [0-6] - [Category]
```

## Automation Script

Use the provided script: `scripts/update-all-submodules.sh`

```bash
# Update all submodules with symlinks
./scripts/update-all-submodules.sh

# Update specific tier only
./scripts/update-all-submodules.sh --tier 2

# Dry run (show what would happen)
./scripts/update-all-submodules.sh --dry-run
```

## Error Handling

If a submodule update fails:
1. Script logs the error
2. Continues with remaining submodules
3. Provides summary report at end
4. Failed submodules can be retried individually

## Verification

After all updates:
1. Check master repo submodule status
2. Verify all submodule pointers updated
3. Test framework access from sample submodule
4. Create checkpoint documenting the update

## Best Practices

✅ **Always run in order** - Respects dependency hierarchy  
✅ **Review changes** - Check git diff before committing  
✅ **Test after update** - Verify framework access works  
✅ **Document updates** - Create checkpoint after completion  
✅ **Communicate changes** - Update team if breaking changes  

---

**Maintained by:** AZ1.AI CODITECT Team  
**Last Updated:** 2025-11-16
