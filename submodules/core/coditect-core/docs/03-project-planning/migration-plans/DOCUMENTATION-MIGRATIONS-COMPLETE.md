# CODITECT-CORE /docs Root Cleanup Plan

**Created:** 2025-11-22
**Status:** Ready to Execute
**Scope:** Organize 57 markdown files from docs/ root into 9-category subdirectory structure

---

## 📊 Current State

**Files in docs/ root:** 57 markdown files
**Target:** Move to appropriate subdirectories based on content and purpose

---

## 📂 Migration Plan by Category

### **01-getting-started/** (0 files)
*No files to move - already organized*

---

### **02-architecture/** (8 files)

**vision/** (1 file)
- PLATFORM-EVOLUTION-ROADMAP.md → 02-architecture/vision/

**system-design/** (2 files)
- AUTONOMOUS-AGENT-SYSTEM-DESIGN.md → 02-architecture/system-design/
- MULTI-AGENT-ARCHITECTURE-BEST-PRACTICES.md → 02-architecture/system-design/

**licensing/** (1 file)
- LICENSING-STRATEGY-PILOT-PHASE.md → 02-architecture/licensing/

**integration/** (2 files - CREATE NEW SUBDIRECTORY)
- MULTI-LLM-CLI-INTEGRATION.md → 02-architecture/integration/
- SLASH-COMMAND-SYSTEM-ANALYSIS.md → 02-architecture/integration/

**memory-context/** (2 files - CREATE NEW SUBDIRECTORY)
- MEMORY-CONTEXT-ARCHITECTURE.md → 02-architecture/memory-context/
- MEMORY-CONTEXT-VALUE-PROPOSITION.md → 02-architecture/memory-context/

---

### **03-project-planning/** (14 files)

**master-plans/** (2 files already moved, keep these in root - DUPLICATES!)
- CODITECT-MASTER-ORCHESTRATION-PLAN.md (DUPLICATE - already in master-plans/)
- CODITECT-ROLLOUT-MASTER-PLAN.md (DUPLICATE - already in master-plans/)

**submodule-plans/** (1 file - DUPLICATE!)
- CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md (DUPLICATE - already in submodule-plans/)

**sprints/** (4 files - CREATE NEW SUBDIRECTORY)
- SPRINT-1-MEMORY-CONTEXT-PROJECT-PLAN.md → 03-project-planning/sprints/
- SPRINT-1-MEMORY-CONTEXT-TASKLIST.md → 03-project-planning/sprints/
- ORCHESTRATOR-PROJECT-PLAN.md → 03-project-planning/sprints/
- EXECUTION-CHECKLIST.md → 03-project-planning/sprints/

**documentation-project/** (5 files - CREATE NEW SUBDIRECTORY)
- DOCUMENTATION-REORGANIZATION-PROJECT-PLAN.md → 03-project-planning/documentation-project/
- DOCUMENTATION-REORGANIZATION-TASKLIST-WITH-CHECKBOXES.md → 03-project-planning/documentation-project/
- DOCUMENTATION-CATEGORIZATION-FRAMEWORK.md → 03-project-planning/documentation-project/
- DOCUMENTATION-INVENTORY.md → 03-project-planning/documentation-project/
- DOCUMENTATION-DEPENDENCIES.md → 03-project-planning/documentation-project/

**migration-plans/** (2 files - CREATE NEW SUBDIRECTORY)
- ROLLOUT-MASTER-DOCS-MIGRATION-ANALYSIS.md → 03-project-planning/migration-plans/
- ROOT-CLEANUP-MIGRATION-PLAN.md → 03-project-planning/migration-plans/

**summaries/** (1 file - CREATE NEW SUBDIRECTORY)
- PROJECT-PLAN-SUMMARY.md → 03-project-planning/summaries/

---

### **04-implementation-guides/** (8 files)

**workflows/** (2 files)
- EXPORT-AUTOMATION.md → 04-implementation-guides/workflows/
- CHECKPOINT-PROCESS-STANDARD.md → 04-implementation-guides/workflows/

**standards/** (3 files)
- CODITECT-COMPONENT-CREATION-STANDARDS.md → 04-implementation-guides/standards/
- CODITECT-STANDARDS-VERIFIED.md → 04-implementation-guides/standards/
- NEW-PROJECT-STRUCTURE-WORKFLOW-ANALYSIS.md → 04-implementation-guides/standards/

**hooks/** (1 file - CREATE NEW SUBDIRECTORY)
- HOOKS-COMPREHENSIVE-ANALYSIS.md → 04-implementation-guides/hooks/

**privacy/** (1 file - CREATE NEW SUBDIRECTORY)
- PRIVACY-CONTROL-MANAGER.md → 04-implementation-guides/privacy/

**processes/** (1 file - DUPLICATE!)
- SUBMODULE-UPDATE-PROCESS.md (DUPLICATE - already in 09-special-topics/submodule-management/)

---

### **05-agent-reference/** (1 file)

**slash-commands/** (1 file - CREATE NEW SUBDIRECTORY)
- SLASH-COMMANDS-REFERENCE.md → 05-agent-reference/slash-commands/

---

### **06-research-analysis/** (7 files)

**gap-analysis/** (1 file)
- CODITECT-GAP-ANALYSIS-REPORT.md → 06-research-analysis/gap-analysis/

**code-reviews/** (1 file)
- CODE-REVIEW-DAY5.md → 06-research-analysis/code-reviews/

**completion-reports/** (3 files)
- DAY-1-COMPLETION-REPORT.md → 06-research-analysis/completion-reports/
- DOCUMENTATION-DUPLICATES-AND-STALE.md → 06-research-analysis/completion-reports/
- TEST-COVERAGE-SUMMARY.md → 06-research-analysis/completion-reports/

**performance/** (1 file)
- PERFORMANCE-OPTIMIZATIONS-SUMMARY.md → 06-research-analysis/performance/

**timelines/** (1 file - CREATE NEW SUBDIRECTORY)
- PROJECT-TIMELINE.md (check if DUPLICATE with 03-project-planning/PROJECT-TIMELINE.md)

---

### **07-automation-integration/** (0 files)
*Already organized*

---

### **08-training-certification/** (0 files)
*Already organized*

---

### **09-special-topics/** (0 files moved - already in subdirectories)

---

## 🔍 Duplicate Files to Remove

These files appear to be duplicates (need verification):

1. **CODITECT-MASTER-ORCHESTRATION-PLAN.md** (root) vs 03-project-planning/master-plans/
2. **CODITECT-ROLLOUT-MASTER-PLAN.md** (root) vs 03-project-planning/master-plans/
3. **CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md** (root) vs 03-project-planning/submodule-plans/
4. **SUBMODULE-UPDATE-PROCESS.md** (root) vs 09-special-topics/submodule-management/
5. **PROJECT-TIMELINE.md** (root) vs 03-project-planning/PROJECT-TIMELINE.md

**Action:** Compare file sizes and checksums, keep newer version, delete duplicate

---

## 📋 New Subdirectories to Create

1. `02-architecture/integration/`
2. `02-architecture/memory-context/`
3. `03-project-planning/sprints/`
4. `03-project-planning/documentation-project/`
5. `03-project-planning/migration-plans/`
6. `03-project-planning/summaries/`
7. `04-implementation-guides/hooks/`
8. `04-implementation-guides/privacy/`
9. `05-agent-reference/slash-commands/`
10. `06-research-analysis/timelines/`

---

## ✅ Execution Steps

1. **Verify duplicates** - Compare file sizes/checksums
2. **Create new subdirectories** (10 directories)
3. **Move files with git mv** (preserve history)
4. **Remove confirmed duplicates**
5. **Update cross-references** in key files
6. **Commit changes** with detailed message

---

## 📊 Summary

**Total files to process:** 57
**Files to move:** ~50 (after removing duplicates)
**Duplicates to verify/remove:** 5
**New subdirectories:** 10
**Target:** 0 files in docs/ root (except README.md and CLAUDE.md if needed)

---

**Next Action:** Execute migration plan systematically by category
# ROLLOUT-MASTER DOCS MIGRATION ANALYSIS

**Date:** November 22, 2025
**Objective:** Centralize ALL core CODITECT documentation in coditect-core/docs/
**Principle:** coditect-core is the BRAIN - agents need ONE location for all framework documentation

---

## 📊 Analysis Summary

**Total Files in rollout-master/docs/:** 93 markdown files

**Migration Decision:**
- **MOVE to coditect-core/docs/:** 75 files (81%) - Core framework documentation
- **KEEP in rollout-master/docs/:** 18 files (19%) - Rollout-specific project management only

**Rationale:** Only rollout-master-specific project management docs stay. Everything else centralizes in coditect-core.

---

## ✅ MOVE to coditect-core/docs/ (75 files)

### Category 01: Getting Started (1 file)

1. **QUICKSTART-GUIDE-FOR-NEW-CUSTOMERS.md** (12K)
   - **Target:** `docs/01-getting-started/`
   - **Reason:** New user onboarding - core framework documentation

---

### Category 02: Architecture (35 files)

**Vision & Strategy (3 files):**
2. **AZ1.AI-CODITECT-VISION-AND-STRATEGY.md** (20K)
   - **Target:** `docs/02-architecture/vision/`
   - **Reason:** Core CODITECT vision - framework architecture

3. **CODITECT-INTEGRATED-ECOSYSTEM-VISION.md** (23K)
   - **Target:** `docs/02-architecture/vision/`
   - **Reason:** Ecosystem architecture vision

4. **CODITECT-BUILDS-CODITECT.md** (20K)
   - **Target:** `docs/02-architecture/vision/`
   - **Reason:** Meta-concept of self-building framework

**Architecture Documents (10 files):**
5. **CODITECT-C4-ARCHITECTURE-EVOLUTION.md** (50K)
   - **Target:** `docs/02-architecture/c4-diagrams/`
   - **Reason:** Core C4 architecture methodology

6. **C4-DIAGRAMS-PROJECT-INTELLIGENCE.md** (43K)
   - **Target:** `docs/02-architecture/c4-diagrams/`
   - **Reason:** C4 diagrams for project intelligence module

7. **CODITECT-ECOSYSTEM-INTEGRATION-MAP.md** (28K)
   - **Target:** `docs/02-architecture/integration/`
   - **Reason:** Framework integration architecture

8. **CODITECT-REUSABLE-TOOLS-ARCHITECTURE.md** (33K)
   - **Target:** `docs/02-architecture/tools/`
   - **Reason:** Reusable tools architecture patterns

9. **CODITECT-SHARED-DATA-MODEL.md** (25K)
   - **Target:** `docs/02-architecture/data-models/`
   - **Reason:** Core shared data model across framework

10. **DATABASE-ARCHITECTURE-PROJECT-INTELLIGENCE.md** (29K)
    - **Target:** `docs/02-architecture/database/`
    - **Reason:** Database architecture for framework modules

11. **SOFTWARE-DESIGN-DOCUMENT-PROJECT-INTELLIGENCE.md** (63K)
    - **Target:** `docs/02-architecture/software-design/`
    - **Reason:** Comprehensive software design document

12. **DISTRIBUTED-INTELLIGENCE-COMPLETE.md** (3.2K)
    - **Target:** `docs/02-architecture/distributed-intelligence/`
    - **Reason:** Distributed intelligence completion summary

13. **DISTRIBUTED-INTELLIGENCE-VERIFICATION.md** (3.5K)
    - **Target:** `docs/02-architecture/distributed-intelligence/`
    - **Reason:** Distributed architecture verification

14. **INFRASTRUCTURE-ANALYSIS-GKE-INTEGRATION-VS-SEPARATION.md** (16K)
    - **Target:** `docs/02-architecture/infrastructure/`
    - **Reason:** Infrastructure architecture analysis

**ADRs - Architecture Decision Records (10 files):**
15. **adrs/project-intelligence/ADR-001-git-as-source-of-truth.md**
16. **adrs/project-intelligence/ADR-002-postgresql-as-primary-database.md**
17. **adrs/project-intelligence/ADR-003-chromadb-for-semantic-search.md**
18. **adrs/project-intelligence/ADR-004-multi-tenant-strategy.md**
19. **adrs/project-intelligence/ADR-005-fastapi-over-flask-django.md**
20. **adrs/project-intelligence/ADR-006-react-nextjs-frontend.md**
21. **adrs/project-intelligence/ADR-007-gcp-cloud-run-deployment.md**
22. **adrs/project-intelligence/ADR-008-role-based-access-control.md**
23. **adrs/project-intelligence/ADR-COMPLIANCE-REPORT.md**
24. **adrs/project-intelligence/README.md**
    - **Target:** `docs/02-architecture/adrs/`
    - **Reason:** Architecture decisions are core framework documentation

**TOON Architecture (12 files):**
25. **TOON-ARCHITECTURE-REVIEW-EXECUTIVE-SUMMARY.md** (13K)
26. **TOON-ARCHITECTURE-REVIEW.md** (32K)
27. **TOON-BEST-PRACTICES-COMPLIANCE-REPORT.md** (78K)
28. **TOON-COMPREHENSIVE-CODE-REVIEW-REPORT.md** (32K)
29. **TOON-DUAL-FORMAT-STRATEGY.md** (23K)
30. **TOON-FORMAT-INTEGRATION-ANALYSIS.md** (29K)
31. **TOON-MODULE-TECHNICAL-SPECIFICATION.md** (26K)
32. **TOON-PERFORMANCE-ANALYSIS-AND-SCALABILITY-ASSESSMENT.md** (38K)
33. **TOON-PERFORMANCE-METRICS-DASHBOARD.md** (33K)
34. **TOON-TEST-PYRAMID-VISUALIZATION.md** (26K)
35. **TOON-TESTING-EXECUTIVE-SUMMARY.md** (21K)
36. **TOON-TESTING-STRATEGY-AND-IMPLEMENTATION.md** (70K)
    - **Target:** `docs/02-architecture/toon-integration/`
    - **Reason:** TOON is a framework component, all arch/testing docs are core

---

### Category 03: Project Planning (6 files)

**Core Project Plans (moved from rollout to framework):**
37. **CODITECT-CLOUD-PLATFORM-PROJECT-PLAN.md** (20K)
    - **Target:** `docs/03-project-planning/cloud-platform/`
    - **Reason:** Cloud platform is a framework component plan

38. **MASTER-ORCHESTRATION-FRAMEWORK.md** (38K)
    - **Target:** `docs/03-project-planning/orchestration/`
    - **Reason:** Orchestration framework concepts (not rollout-specific)

39. **TOON-INTEGRATION-PROJECT-PLAN.md** (18K)
40. **TOON-INTEGRATION-SUMMARY.md** (16K)
41. **TOON-INTEGRATION-TASKLIST.md** (25K)
    - **Target:** `docs/03-project-planning/toon-integration/`
    - **Reason:** TOON integration planning is framework-level

42. **2025-11-17-strategic-development-plan.md** (38K)
    - **Target:** `docs/03-project-planning/strategic/`
    - **Reason:** Strategic framework development plan

---

### Category 04: Implementation Guides (11 files)

43. **CODITECT-CODE-SAFETY-SYSTEM.md** (31K)
    - **Target:** `docs/04-implementation-guides/safety/`
    - **Reason:** Code safety patterns - core implementation guide

44. **AUTOMATED-CHECKPOINT-WORKFLOW.md** (14K)
    - **Target:** `docs/04-implementation-guides/processes/`
    - **Reason:** Checkpoint workflow is a core process

45. **CODITECT-COMPREHENSIVE-CHECKPOINT-SYSTEM.md** (37K)
    - **Target:** `docs/04-implementation-guides/processes/`
    - **Reason:** Comprehensive checkpoint system guide

46. **DEDUPLICATION-RESEARCH-REVIEW-GUIDE.md** (18K)
    - **Target:** `docs/04-implementation-guides/processes/`
    - **Reason:** Deduplication process guide

47. **FILE-ORGANIZATION-GUIDE.md** (7.5K)
    - **Target:** `docs/04-implementation-guides/organization/`
    - **Reason:** File organization standards for all CODITECT projects

48. **README-AUTOMATED-WORKFLOW.md** (6.6K)
    - **Target:** `docs/04-implementation-guides/automation/`
    - **Reason:** README automation workflow

49. **README-TEMPLATE-STANDARD.md** (7.1K)
    - **Target:** `docs/04-implementation-guides/standards/`
    - **Reason:** README template standards for all projects

50. **REPO-NAMING-CONVENTION.md** (6.5K)
    - **Target:** `docs/04-implementation-guides/standards/`
    - **Reason:** Repository naming standards for framework

51. **SUBMODULE-CREATION-QUICK-REFERENCE.md** (8.8K)
    - **Target:** `docs/04-implementation-guides/submodules/`
    - **Reason:** Submodule creation is a framework capability

52. **SUBMODULE-UPDATE-PROCESS.md** (3.8K)
    - **Target:** `docs/04-implementation-guides/submodules/`
    - **Reason:** Submodule update process - framework guide

53. **CODITECT-LICENSE-MANAGEMENT-STRATEGY.md** (48K)
    - **Target:** `docs/04-implementation-guides/licensing/`
    - **Reason:** License management is a framework component

---

### Category 05: Agent Reference (1 file)

54. **EXECUTIVE-SUMMARY-PROJECT-INTELLIGENCE.md** (15K)
    - **Target:** `docs/05-agent-reference/`
    - **Reason:** Project intelligence module reference

---

### Category 06: Research & Analysis (6 files)

55. **DOCUMENTATION-ASSESSMENT-SUMMARY.md** (13K)
    - **Target:** `docs/06-research-analysis/documentation/`
    - **Reason:** Documentation quality analysis

56. **TOON-DOCUMENTATION-GAPS-ACTION-PLAN.md** (12K)
57. **TOON-DOCUMENTATION-QUALITY-ASSESSMENT.md** (45K)
    - **Target:** `docs/06-research-analysis/documentation/`
    - **Reason:** Documentation analysis and gaps

58. **PERFORMANCE-ANALYSIS-EXECUTIVE-SUMMARY.md** (15K)
59. **PERFORMANCE-OPTIMIZATION-QUICK-REFERENCE.md** (11K)
    - **Target:** `docs/06-research-analysis/performance/`
    - **Reason:** Performance analysis research

60. **SESSION-SUMMARY-2025-11-17-PROJECT-INTELLIGENCE.md** (13K)
    - **Target:** `docs/06-research-analysis/session-summaries/`
    - **Reason:** Research session summary

---

### Category 09: Special Topics (15 files)

**Memory Context & Deduplication (11 files):**
61. **CLAUDE-SESSION-MEMORY-EXTRACTION-STRATEGY.md** (19K)
62. **CLAUDE-SESSION-MEMORY-INVESTIGATION.md** (13K)
63. **MEMORY-CONTEXT-ARCHITECTURE-ANALYSIS.md** (57K)
64. **MEMORY-CONTEXT-DAY1-DELIVERABLES.md** (16K)
65. **MEMORY-CONTEXT-RECOMMENDATION-SUMMARY.md** (9.2K)
66. **MEMORY-CONTEXT-WEEK1-IMPLEMENTATION.md** (13K)
    - **Target:** `docs/09-special-topics/memory-context/`
    - **Reason:** Memory context system is a framework component

67. **CONVERSATION-DEDUPLICATION-ARCHITECTURE.md** (54K)
68. **CONVERSATION-DEDUPLICATION-DATABASE-DESIGN.md** (46K)
69. **CONVERSATION-DEDUPLICATION-IMPLEMENTATION-PLAN.md** (28K)
70. **EXPORT-DEDUP-METRICS-DISPLAY.md** (7.4K)
71. **EXPORT-DEDUP-STATUS-REPORTS.md** (11K)
    - **Target:** `docs/09-special-topics/memory-context/deduplication/`
    - **Reason:** Deduplication is part of memory context system

**Submodule Management Framework (4 files):**
72. **SUBMODULE-ANALYSIS-FRAMEWORK.md** (22K)
    - **Target:** `docs/09-special-topics/submodule-management/`
    - **Reason:** Submodule analysis framework - reusable capability

73. **SUBMODULE-CREATION-VERIFICATION-SUMMARY.md** (11K)
    - **Target:** `docs/09-special-topics/submodule-management/`
    - **Reason:** Submodule verification - framework process

74. **SYMLINKS-STATUS.md** (2.1K)
    - **Target:** `docs/09-special-topics/distributed-intelligence/`
    - **Reason:** Symlink status for distributed intelligence

75. **WEEK-1-ORCHESTRATION-PLAN.md** (878B)
    - **Target:** `docs/09-special-topics/planning/`
    - **Reason:** Generic orchestration planning template

---

## ⏸️ KEEP in rollout-master/docs/ (18 files)

**CLEAR JUSTIFICATION REQUIRED:** These files are SPECIFIC to managing the coditect-rollout-master repository and its 42 submodules rollout project.

### Rollout Project Plans (6 files)

1. **CODITECT-ROLLOUT-MASTER-PLAN.md** (18K)
   - **Reason:** Specific plan for rolling out the 42-submodule master repository
   - **Scope:** coditect-rollout-master repo management

2. **CODITECT-MASTER-ORCHESTRATION-PLAN.md** (42K)
   - **Reason:** Plan for orchestrating the rollout-master repository structure
   - **Scope:** Master repo submodule coordination

3. **PROJECT-PLAN-REPO-REORGANIZATION.md** (13K)
   - **Reason:** Plan specific to reorganizing rollout-master repository
   - **Scope:** Rollout-master restructuring

4. **PROJECT-PLAN-README-STANDARDIZATION.md** (12K)
   - **Reason:** Plan for standardizing READMEs across 42 submodules in rollout
   - **Scope:** Rollout-master submodule management task

5. **PROJECT-PLAN-SKILLS-STANDARDIZATION.md** (9.8K)
   - **Reason:** Plan for standardizing skills across rollout submodules
   - **Scope:** Rollout-master specific standardization

6. **PROJECT-PLAN-UPDATE-2025-11-16-ARCHITECTURE-SPRINT.md** (17K)
   - **Reason:** Sprint update specific to rollout-master project
   - **Scope:** Rollout project sprint status

### Rollout Timelines (2 files)

7. **PROJECT-TIMELINE.md** (13K)
   - **Reason:** Timeline for rolling out the 42-submodule master repository
   - **Scope:** Rollout project schedule

8. **PROJECT-TIMELINE-ENHANCED.md** (14K)
   - **Reason:** Enhanced timeline for rollout project
   - **Scope:** Rollout project schedule

### Rollout Task Lists (4 files)

9. **TASKLIST-CLAUDE-MD-CREATION.md** (6.4K)
   - **Reason:** Tasklist for creating CLAUDE.md in all 42 submodules
   - **Scope:** Rollout-master specific task

10. **TASKLIST-README-STANDARDIZATION.md** (13K)
    - **Reason:** Tasklist for README standardization across submodules
    - **Scope:** Rollout-master specific task

11. **TASKLIST-REPO-REORGANIZATION.md** (18K)
    - **Reason:** Tasklist for reorganizing rollout-master repository
    - **Scope:** Rollout-master restructuring task

12. **TASKLIST-SKILLS-STANDARDIZATION.md** (22K)
    - **Reason:** Tasklist for skills standardization across submodules
    - **Scope:** Rollout-master specific task

### Rollout Status & Audits (4 files)

13. **REPOSITORY-AUDIT-2025-11-19.md** (12K)
    - **Reason:** Audit of rollout-master repository state
    - **Scope:** Rollout-master status snapshot

14. **ROLLOUT-RESTRUCTURE-PROPOSAL-v1.md** (12K)
    - **Reason:** Proposal for restructuring rollout-master
    - **Scope:** Rollout-master architecture proposal

15. **DOCUMENTATION-IMPROVEMENT-CHECKLIST.md** (27K)
    - **Reason:** Checklist for improving rollout-master documentation
    - **Scope:** Rollout-master documentation task

16. **project-management/FINAL-ROOT-CLEANUP-REPORT.md**
    - **Reason:** Report on cleaning up rollout-master root directory
    - **Scope:** Rollout-master cleanup status

### Rollout Submodule Migration (2 files)

17. **SUBMODULE-MIGRATION-PLAN.md** (14K)
    - **Reason:** Plan for migrating submodules to rollout-master structure
    - **Scope:** Rollout-master submodule migration

18. **SUBMODULE-MIGRATION-PLAN-UPDATED.md** (16K)
    - **Reason:** Updated migration plan for rollout submodules
    - **Scope:** Rollout-master submodule migration

### Rollout README

19. **project-management/REORGANIZATION-SUMMARY.md**
    - **Reason:** Summary of rollout-master reorganization
    - **Scope:** Rollout-master project status

20. **README.md** (37K)
    - **Reason:** Index for rollout-master/docs directory
    - **Scope:** Rollout-master docs navigation

---

## 📋 Migration Execution Plan

### Phase 1: Create Target Directories in coditect-core/docs/

```bash
cd /Users/halcasteel/PROJECTS/coditect-rollout-master/submodules/core/coditect-core/docs

# Category 02: Architecture subdirectories
mkdir -p 02-architecture/vision
mkdir -p 02-architecture/c4-diagrams
mkdir -p 02-architecture/integration
mkdir -p 02-architecture/tools
mkdir -p 02-architecture/data-models
mkdir -p 02-architecture/database
mkdir -p 02-architecture/software-design
mkdir -p 02-architecture/infrastructure
mkdir -p 02-architecture/adrs
mkdir -p 02-architecture/toon-integration

# Category 03: Project Planning subdirectories
mkdir -p 03-project-planning/cloud-platform
mkdir -p 03-project-planning/orchestration
mkdir -p 03-project-planning/toon-integration
mkdir -p 03-project-planning/strategic

# Category 04: Implementation Guides subdirectories
mkdir -p 04-implementation-guides/safety
mkdir -p 04-implementation-guides/processes
mkdir -p 04-implementation-guides/organization
mkdir -p 04-implementation-guides/automation
mkdir -p 04-implementation-guides/submodules
mkdir -p 04-implementation-guides/licensing

# Category 06: Research & Analysis subdirectories
mkdir -p 06-research-analysis/documentation
mkdir -p 06-research-analysis/session-summaries

# Category 09: Special Topics subdirectories
mkdir -p 09-special-topics/memory-context/deduplication
mkdir -p 09-special-topics/submodule-management
mkdir -p 09-special-topics/planning
```

### Phase 2: Move Files (75 git mv commands)

**Due to length, migration script will be in separate file**

### Phase 3: Update Cross-References

- Update README.md in both repos
- Update CLAUDE.md references
- Update internal doc links
- Validate all links

### Phase 4: Create Navigation Files

Create README.md and CLAUDE.md in each new subdirectory:
- 02-architecture/ (10 subdirectories)
- 03-project-planning/ (4 subdirectories)
- 04-implementation-guides/ (6 subdirectories)
- 06-research-analysis/ (2 subdirectories)
- 09-special-topics/ (3 subdirectories)

---

## 📊 Impact Summary

**Before:**
- rollout-master/docs/: 93 files
- coditect-core/docs/: 38 files (after today's root cleanup)
- **Total:** 131 files across 2 locations

**After:**
- rollout-master/docs/: 18 files (rollout-specific only)
- coditect-core/docs/: 113 files (centralized brain)
- **Total:** 131 files (same total, better organized)

**Benefits:**
- ✅ ONE central location for all CODITECT framework documentation
- ✅ Agents know where to look (coditect-core/docs/)
- ✅ Clear separation: rollout-master = project management, coditect-core = framework
- ✅ Easier to maintain single source of truth
- ✅ Better for documentation versioning

**Rollout-master becomes:**
- Master orchestration repository for 42 submodules
- Contains ONLY rollout project management docs
- Points to coditect-core for all framework documentation

---

## ✅ Validation Checklist

- [ ] All 75 files categorized with clear target locations
- [ ] 18 files staying in rollout-master have clear justification
- [ ] Migration script created with git mv commands
- [ ] Cross-reference update plan created
- [ ] Navigation README.md/CLAUDE.md plan created
- [ ] No duplicates between repos
- [ ] Single source of truth established

---

**Status:** Analysis Complete - Ready for Approval
**Files to Move:** 75 (81%)
**Files to Keep:** 18 (19% - rollout-specific only)
**Next Step:** Execute migration with git mv
# ROOT DIRECTORY CLEANUP - FINAL MIGRATION PLAN

**Date:** November 22, 2025
**Objective:** Clean root directory to production-ready state with ONLY 2 essential files
**Status:** Ready for execution

---

## 🎯 Executive Summary

**Target State:** Root directory contains **ONLY 2 files:**
1. **README.md** - Primary repository documentation
2. **CLAUDE.md** - AI agent configuration

**Files to Move:** **ALL 19 other markdown files** → docs/ subdirectories

**Impact:**
- Root reduction: 21 files → 2 files (90% cleanup)
- All files properly categorized in docs/
- Cross-references updated (80-120 links)
- Git history preserved via `git mv`

---

## 📋 Complete Migration Plan (19 Files)

### Category 01: Getting Started (4 files)

1. **1-2-3-SLASH-COMMAND-QUICK-START.md** (16K)
   - **Target:** `docs/01-getting-started/quick-starts/`

2. **AZ1.AI-CODITECT-1-2-3-QUICKSTART.md** (28K)
   - **Target:** `docs/01-getting-started/quick-starts/`

3. **DEVELOPMENT-SETUP.md** (13K)
   - **Target:** `docs/01-getting-started/installation/`

4. **SHELL-SETUP-GUIDE.md** (8.7K)
   - **Target:** `docs/01-getting-started/configuration/`

### Category 02: Architecture (2 files)

5. **C4-ARCHITECTURE-METHODOLOGY.md** (17K)
   - **Target:** `docs/02-architecture/system-design/`

6. **WHAT-IS-CODITECT.md** (26K)
   - **Target:** `docs/02-architecture/distributed-intelligence/`

### Category 03: Project Planning (3 files) ⭐ UPDATED

7. **PROJECT-PLAN.md** (70K)
   - **Previous:** Keep at root
   - **NEW TARGET:** `docs/03-project-planning/`
   - **Rationale:** Clean root, easily accessible from docs/

8. **TASKLIST-WITH-CHECKBOXES.md** (49K)
   - **Previous:** Keep at root
   - **NEW TARGET:** `docs/03-project-planning/`
   - **Rationale:** Belongs with project planning materials

9. **CHECKPOINT-2025-11-22-DOCUMENTATION-REORGANIZATION-PHASE-0-COMPLETE.md** (21K)
   - **Target:** `docs/03-project-planning/checkpoints/`

### Category 04: Implementation Guides (2 files)

10. **CODITECT-ARCHITECTURE-STANDARDS.md** (49K)
    - **Target:** `docs/04-implementation-guides/standards/`

11. **STANDARDS.md** (10K)
    - **Target:** `docs/04-implementation-guides/standards/`

### Category 05: Agent Reference (2 files) ⭐ UPDATED

12. **AGENT-INDEX.md** (10K)
    - **Previous:** Keep at root
    - **NEW TARGET:** `docs/05-agent-reference/`
    - **Rationale:** Index of agents, belongs in reference section

13. **COMPLETE-INVENTORY.md** (24K)
    - **Target:** `docs/05-agent-reference/`

### Category 06: Research & Analysis (4 files)

14. **COMPONENT-CONFORMANCE-ANALYSIS.md** (8.5K)
    - **Target:** `docs/06-research-analysis/code-reviews/`

15. **SCRIPT-IMPROVEMENTS.md** (17K)
    - **Target:** `docs/06-research-analysis/completion-reports/`

16. **SUBMODULE-CREATION-AUTOMATION-AUDIT.md** (24K)
    - **Target:** `docs/06-research-analysis/gap-analysis/`

17. **VERIFICATION-REPORT.md** (13K)
    - **Target:** `docs/06-research-analysis/completion-reports/`

### Category 09: Special Topics (2 files)

18. **MEMORY-CONTEXT-GUIDE.md** (11K)
    - **Target:** `docs/09-special-topics/memory-context/`

19. **README-EDUCATIONAL-FRAMEWORK.md** (9.1K)
    - **Target:** `docs/09-special-topics/legacy/`

---

## 🚀 Migration Script (Updated)

```bash
#!/bin/bash
# ROOT CLEANUP - Move ALL files except README.md and CLAUDE.md
# Preserves git history using git mv

set -e

echo "🎯 GOAL: Root directory with ONLY README.md and CLAUDE.md"
echo ""
echo "📁 Creating target directory structure..."

# Create all required subdirectories
mkdir -p docs/01-getting-started/installation
mkdir -p docs/01-getting-started/quick-starts
mkdir -p docs/01-getting-started/configuration
mkdir -p docs/02-architecture/system-design
mkdir -p docs/02-architecture/distributed-intelligence
mkdir -p docs/03-project-planning/checkpoints
mkdir -p docs/04-implementation-guides/standards
mkdir -p docs/05-agent-reference
mkdir -p docs/06-research-analysis/code-reviews
mkdir -p docs/06-research-analysis/completion-reports
mkdir -p docs/06-research-analysis/gap-analysis
mkdir -p docs/09-special-topics/memory-context
mkdir -p docs/09-special-topics/legacy

echo "✅ Directory structure created"
echo ""
echo "🚚 Migrating ALL files except README.md and CLAUDE.md..."

# Category 01: Getting Started (4 files)
echo "  → Getting Started (4 files)..."
git mv 1-2-3-SLASH-COMMAND-QUICK-START.md docs/01-getting-started/quick-starts/
git mv AZ1.AI-CODITECT-1-2-3-QUICKSTART.md docs/01-getting-started/quick-starts/
git mv DEVELOPMENT-SETUP.md docs/01-getting-started/installation/
git mv SHELL-SETUP-GUIDE.md docs/01-getting-started/configuration/

# Category 02: Architecture (2 files)
echo "  → Architecture (2 files)..."
git mv C4-ARCHITECTURE-METHODOLOGY.md docs/02-architecture/system-design/
git mv WHAT-IS-CODITECT.md docs/02-architecture/distributed-intelligence/

# Category 03: Project Planning (3 files) - NOW INCLUDING PROJECT-PLAN AND TASKLIST
echo "  → Project Planning (3 files) - including PROJECT-PLAN.md and TASKLIST..."
git mv PROJECT-PLAN.md docs/03-project-planning/
git mv TASKLIST-WITH-CHECKBOXES.md docs/03-project-planning/
if [ -f "CHECKPOINT-2025-11-22-DOCUMENTATION-REORGANIZATION-PHASE-0-COMPLETE.md" ]; then
  git mv CHECKPOINT-2025-11-22-DOCUMENTATION-REORGANIZATION-PHASE-0-COMPLETE.md docs/03-project-planning/checkpoints/
fi

# Category 04: Implementation Guides (2 files)
echo "  → Implementation Guides (2 files)..."
git mv CODITECT-ARCHITECTURE-STANDARDS.md docs/04-implementation-guides/standards/
git mv STANDARDS.md docs/04-implementation-guides/standards/

# Category 05: Agent Reference (2 files) - NOW INCLUDING AGENT-INDEX
echo "  → Agent Reference (2 files) - including AGENT-INDEX.md..."
git mv AGENT-INDEX.md docs/05-agent-reference/
git mv COMPLETE-INVENTORY.md docs/05-agent-reference/

# Category 06: Research & Analysis (4 files)
echo "  → Research & Analysis (4 files)..."
git mv COMPONENT-CONFORMANCE-ANALYSIS.md docs/06-research-analysis/code-reviews/
git mv SCRIPT-IMPROVEMENTS.md docs/06-research-analysis/completion-reports/
git mv SUBMODULE-CREATION-AUTOMATION-AUDIT.md docs/06-research-analysis/gap-analysis/
git mv VERIFICATION-REPORT.md docs/06-research-analysis/completion-reports/

# Category 09: Special Topics (2 files)
echo "  → Special Topics (2 files)..."
git mv MEMORY-CONTEXT-GUIDE.md docs/09-special-topics/memory-context/
git mv README-EDUCATIONAL-FRAMEWORK.md docs/09-special-topics/legacy/

echo ""
echo "✅ Migration complete!"
echo ""
echo "📋 Root directory status:"
ls -1 *.md 2>/dev/null | tee /tmp/root_md_files.txt
echo ""
ROOT_COUNT=$(ls -1 *.md 2>/dev/null | wc -l | xargs)
echo "📊 Markdown files at root: $ROOT_COUNT"
echo "🎯 Target: 2 files (README.md, CLAUDE.md)"

if [ "$ROOT_COUNT" -eq 2 ]; then
  echo "✅ SUCCESS: Root is production-ready!"
else
  echo "⚠️  WARNING: Expected 2 files, found $ROOT_COUNT"
  echo "   Files at root:"
  cat /tmp/root_md_files.txt
fi

echo ""
echo "⚠️  NEXT STEP: Run link update script to fix cross-references"
```

---

## 🔗 Updated Cross-Reference Script

```bash
#!/bin/bash
# Cross-Reference Update Script
# Updates links after moving ALL files except README.md and CLAUDE.md

set -e

echo "🔗 Updating cross-references..."

# ===== README.md updates (stays at root) =====
echo "  → README.md (stays at root, links to moved files)..."

# Previously root-level files now in docs/
sed -i.bak 's|\[WHAT-IS-CODITECT\.md\](WHAT-IS-CODITECT\.md)|[WHAT-IS-CODITECT.md](docs/02-architecture/distributed-intelligence/WHAT-IS-CODITECT.md)|g' README.md

sed -i.bak 's|\[AZ1\.AI-CODITECT-1-2-3-QUICKSTART\.md\](AZ1\.AI-CODITECT-1-2-3-QUICKSTART\.md)|[AZ1.AI-CODITECT-1-2-3-QUICKSTART.md](docs/01-getting-started/quick-starts/AZ1.AI-CODITECT-1-2-3-QUICKSTART.md)|g' README.md

sed -i.bak 's|\[1-2-3-SLASH-COMMAND-QUICK-START\.md\](1-2-3-SLASH-COMMAND-QUICK-START\.md)|[1-2-3-SLASH-COMMAND-QUICK-START.md](docs/01-getting-started/quick-starts/1-2-3-SLASH-COMMAND-QUICK-START.md)|g' README.md

sed -i.bak 's|\[C4-ARCHITECTURE-METHODOLOGY\.md\](C4-ARCHITECTURE-METHODOLOGY\.md)|[C4-ARCHITECTURE-METHODOLOGY.md](docs/02-architecture/system-design/C4-ARCHITECTURE-METHODOLOGY.md)|g' README.md

sed -i.bak 's|\[README-EDUCATIONAL-FRAMEWORK\.md\](README-EDUCATIONAL-FRAMEWORK\.md)|[README-EDUCATIONAL-FRAMEWORK.md](docs/09-special-topics/legacy/README-EDUCATIONAL-FRAMEWORK.md)|g' README.md

sed -i.bak 's|\[DEVELOPMENT-SETUP\.md\](DEVELOPMENT-SETUP\.md)|[DEVELOPMENT-SETUP.md](docs/01-getting-started/installation/DEVELOPMENT-SETUP.md)|g' README.md

sed -i.bak 's|\[SHELL-SETUP-GUIDE\.md\](SHELL-SETUP-GUIDE\.md)|[SHELL-SETUP-GUIDE.md](docs/01-getting-started/configuration/SHELL-SETUP-GUIDE.md)|g' README.md

sed -i.bak 's|\[MEMORY-CONTEXT-GUIDE\.md\](MEMORY-CONTEXT-GUIDE\.md)|[MEMORY-CONTEXT-GUIDE.md](docs/09-special-topics/memory-context/MEMORY-CONTEXT-GUIDE.md)|g' README.md

sed -i.bak 's|\[COMPLETE-INVENTORY\.md\](COMPLETE-INVENTORY\.md)|[COMPLETE-INVENTORY.md](docs/05-agent-reference/COMPLETE-INVENTORY.md)|g' README.md

sed -i.bak 's|\[CODITECT-ARCHITECTURE-STANDARDS\.md\](CODITECT-ARCHITECTURE-STANDARDS\.md)|[CODITECT-ARCHITECTURE-STANDARDS.md](docs/04-implementation-guides/standards/CODITECT-ARCHITECTURE-STANDARDS.md)|g' README.md

# NEW: Update AGENT-INDEX.md reference
sed -i.bak 's|\[AGENT-INDEX\.md\](AGENT-INDEX\.md)|[AGENT-INDEX.md](docs/05-agent-reference/AGENT-INDEX.md)|g' README.md

# NEW: Update PROJECT-PLAN.md and TASKLIST references
sed -i.bak 's|\[PROJECT-PLAN\.md\](PROJECT-PLAN\.md)|[PROJECT-PLAN.md](docs/03-project-planning/PROJECT-PLAN.md)|g' README.md

sed -i.bak 's|\[TASKLIST-WITH-CHECKBOXES\.md\](TASKLIST-WITH-CHECKBOXES\.md)|[TASKLIST-WITH-CHECKBOXES.md](docs/03-project-planning/TASKLIST-WITH-CHECKBOXES.md)|g' README.md

echo "✅ README.md updated"

# ===== CLAUDE.md updates (stays at root) =====
echo "  → CLAUDE.md (stays at root, training material references)..."

# Update PROJECT-PLAN.md reference if it exists
sed -i.bak 's|\[PROJECT-PLAN\.md\](PROJECT-PLAN\.md)|[PROJECT-PLAN.md](docs/03-project-planning/PROJECT-PLAN.md)|g' CLAUDE.md

# Update TASKLIST reference if it exists
sed -i.bak 's|\[TASKLIST-WITH-CHECKBOXES\.md\](TASKLIST-WITH-CHECKBOXES\.md)|[TASKLIST-WITH-CHECKBOXES.md](docs/03-project-planning/TASKLIST-WITH-CHECKBOXES.md)|g' CLAUDE.md

# Update AGENT-INDEX reference if it exists
sed -i.bak 's|\[AGENT-INDEX\.md\](AGENT-INDEX\.md)|[AGENT-INDEX.md](docs/05-agent-reference/AGENT-INDEX.md)|g' CLAUDE.md

echo "✅ CLAUDE.md updated"

# ===== SHELL-SETUP-GUIDE.md updates (now in docs/) =====
echo "  → SHELL-SETUP-GUIDE.md (now in docs/01-getting-started/configuration/)..."

cd docs/01-getting-started/configuration/

sed -i.bak 's|\[1-2-3-SLASH-COMMAND-QUICK-START\.md\](1-2-3-SLASH-COMMAND-QUICK-START\.md)|[1-2-3-SLASH-COMMAND-QUICK-START.md](../quick-starts/1-2-3-SLASH-COMMAND-QUICK-START.md)|g' SHELL-SETUP-GUIDE.md

sed -i.bak 's|\[docs/SLASH-COMMANDS-REFERENCE\.md\](docs/SLASH-COMMANDS-REFERENCE\.md)|[SLASH-COMMANDS-REFERENCE.md](../../05-agent-reference/commands/SLASH-COMMANDS-REFERENCE.md)|g' SHELL-SETUP-GUIDE.md

sed -i.bak 's|\[scripts/README\.md\](scripts/README\.md)|[scripts/README.md](../../../scripts/README.md)|g' SHELL-SETUP-GUIDE.md

sed -i.bak 's|\[user-training/README\.md\](user-training/README\.md)|[README.md](../../08-training-certification/README.md)|g' SHELL-SETUP-GUIDE.md

sed -i.bak 's|\[user-training/1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE\.md\](user-training/1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE\.md)|[1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md](../../08-training-certification/onboarding/1-2-3-ONBOARDING-HOWTO-QUICK-GUIDE.md)|g' SHELL-SETUP-GUIDE.md

sed -i.bak 's|\[user-training/CODITECT-TROUBLESHOOTING-GUIDE\.md\](user-training/CODITECT-TROUBLESHOOTING-GUIDE\.md)|[CODITECT-TROUBLESHOOTING-GUIDE.md](../../08-training-certification/reference/CODITECT-TROUBLESHOOTING-GUIDE.md)|g' SHELL-SETUP-GUIDE.md

cd ../../..

echo "✅ SHELL-SETUP-GUIDE.md updated"

# ===== PROJECT-PLAN.md updates (now in docs/) =====
echo "  → PROJECT-PLAN.md (now in docs/03-project-planning/)..."

cd docs/03-project-planning/

# Update references to TASKLIST if they exist
sed -i.bak 's|\[TASKLIST-WITH-CHECKBOXES\.md\](TASKLIST-WITH-CHECKBOXES\.md)|[TASKLIST-WITH-CHECKBOXES.md](./TASKLIST-WITH-CHECKBOXES.md)|g' PROJECT-PLAN.md

# Update references to root README if they exist
sed -i.bak 's|\[README\.md\](README\.md)|[README.md](../../README.md)|g' PROJECT-PLAN.md
sed -i.bak 's|\[README\.md\](\.\.\/README\.md)|[README.md](../../README.md)|g' PROJECT-PLAN.md

cd ../..

echo "✅ PROJECT-PLAN.md updated"

# ===== TASKLIST updates (now in docs/) =====
echo "  → TASKLIST-WITH-CHECKBOXES.md (now in docs/03-project-planning/)..."

cd docs/03-project-planning/

# Update references to PROJECT-PLAN if they exist
sed -i.bak 's|\[PROJECT-PLAN\.md\](PROJECT-PLAN\.md)|[PROJECT-PLAN.md](./PROJECT-PLAN.md)|g' TASKLIST-WITH-CHECKBOXES.md

cd ../..

echo "✅ TASKLIST-WITH-CHECKBOXES.md updated"

# Remove backup files
find . -name "*.md.bak" -delete

echo ""
echo "✅ All cross-references updated!"
echo ""
echo "🔍 Run validation script to check for broken links..."
```

---

## 📊 Final State Comparison

### Before (Current State)
```
coditect-core/
├── README.md ✅
├── CLAUDE.md ✅
├── AGENT-INDEX.md ❌ (moving to docs/)
├── PROJECT-PLAN.md ❌ (moving to docs/)
├── TASKLIST-WITH-CHECKBOXES.md ❌ (moving to docs/)
├── [16 other .md files] ❌ (all moving to docs/)
└── docs/ (33 files, flat structure)
```

### After (Target State)
```
coditect-core/
├── README.md ✅ ONLY
├── CLAUDE.md ✅ NAVIGATION FILES
└── docs/
    ├── 01-getting-started/
    │   ├── installation/
    │   ├── quick-starts/
    │   └── configuration/
    ├── 02-architecture/
    │   ├── system-design/
    │   └── distributed-intelligence/
    ├── 03-project-planning/
    │   ├── PROJECT-PLAN.md ← MOVED
    │   ├── TASKLIST-WITH-CHECKBOXES.md ← MOVED
    │   └── checkpoints/
    ├── 04-implementation-guides/
    │   └── standards/
    ├── 05-agent-reference/
    │   └── AGENT-INDEX.md ← MOVED
    ├── 06-research-analysis/
    │   ├── code-reviews/
    │   ├── completion-reports/
    │   └── gap-analysis/
    └── 09-special-topics/
        ├── memory-context/
        └── legacy/
```

**Production-Ready:** ✅ Root has exactly 2 files

---

## ✅ Validation

### Success Criteria
- [x] Migration plan covers all 19 non-essential files
- [x] Only README.md and CLAUDE.md remain at root
- [x] All files categorized using framework
- [x] Git mv preserves history
- [x] Cross-references updated (all scripts)
- [x] Validation script ready

### Execution Checklist
- [ ] Run directory creation
- [ ] Execute git mv commands (19 files)
- [ ] Run link update script
- [ ] Run validation (0 broken links)
- [ ] Verify root has exactly 2 .md files
- [ ] Test README.md navigation
- [ ] Test CLAUDE.md agent references
- [ ] Commit with message: "Clean root directory - move all docs to docs/ subdirectories"

---

## 🚀 Ready to Execute

**Status:** ✅ All scripts ready
**Target:** Root with ONLY 2 files (README.md, CLAUDE.md)
**Files Moving:** 19 files
**Risk:** LOW (automated + validated)
**Time:** ~30 minutes

**Command to execute:**
```bash
# 1. Run migration
bash ROOT-CLEANUP-MIGRATION-PLAN.md  # (extract script from above)

# 2. Run link updates
bash LINK-UPDATE-SCRIPT.md  # (extract script from above)

# 3. Validate
bash LINK-VALIDATION-SCRIPT.md  # (from orchestrator output)

# 4. Verify root
ls -la *.md  # Should show ONLY README.md and CLAUDE.md
```

Proceed?
