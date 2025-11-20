# CODITECT Repository Reorganization - Project Plan

## Project Overview

### Purpose
Consolidate and reorganize 173 repositories across 3 GitHub accounts (coditect-ai, halcasteel, az1-ai) into a unified, professionally-named structure with 8 clear categories and subfolder organization.

### Strategic Value
- **Immediate clarity** - Anyone can find any repo in seconds
- **Professional appearance** - Enterprise-ready organization
- **Scalability** - Convention works from 50 to 500+ repos
- **Developer onboarding** - New team members productive in minutes
- **Reduced cognitive load** - Clear hierarchy and naming

### Scope
- **Repos to reorganize**: 49 (current 29 submodules + 20 additions)
- **Categories**: 8 (core, cloud, dev, market, docs, ops, gtm, labs)
- **Organizations**: Consolidate to 1 (coditect-ai)
- **Timeline**: 1 week (6-8 focused hours)

---

## Implementation Phases

### Phase 1: Preparation & Backup (Day 1 - 2 hours)

**Goal**: Ensure safe rollback capability before making changes

**Team**:
- `codi-devops-engineer` - Backup scripts
- `project-organizer` - Structure validation

**Tasks**:
- Create full backup of .gitmodules
- Document current submodule SHAs
- Create rollback script
- Verify GitHub CLI authentication
- Test rename command on throwaway repo

**Budget**: 2 hours engineering

**Acceptance Criteria**:
- [ ] Backup created at `backups/pre-reorg-2025-11-19/`
- [ ] Rollback script tested and functional
- [ ] `gh auth status` shows correct permissions

---

### Phase 2: Consolidations & Merges (Day 1-2 - 2 hours)

**Goal**: Reduce repo count by merging duplicates

**Team**:
- `codi-devops-engineer` - Git operations
- `project-organizer` - Content organization

**Merges**:
1. `coditect-installer` → `coditect` (halcasteel) → becomes `coditect-ops-distribution`
2. `coditect-license-server` → `coditect-license-manager` → becomes `coditect-ops-license`
3. `az1.ai-coditect-AI-IDE-competitive-market-research` → `coditect-competition`

**Agent Orchestration**:
```python
# Sequential execution required
Task(subagent_type="codi-devops-engineer",
     prompt="Merge coditect-installer into halcasteel/coditect preserving git history")

Task(subagent_type="codi-devops-engineer",
     prompt="Merge coditect-license-server into coditect-license-manager")
```

**Acceptance Criteria**:
- [ ] All content from merged repos preserved
- [ ] Git history maintained where possible
- [ ] Source repos archived (not deleted)

---

### Phase 3: GitHub Renames (Day 2-3 - 1.5 hours)

**Goal**: Apply new naming convention to all repos

**Team**:
- `codi-devops-engineer` - Execute renames

**Rename Script**:
```bash
# Core (3)
gh repo rename coditect-ai/coditect-project-dot-claude coditect-core-dotclaude
gh repo rename coditect-ai/coditect-framework coditect-core-framework
gh repo rename coditect-ai/coditect-distributed-architecture coditect-core-architecture

# Cloud (5)
gh repo rename coditect-ai/Coditect-v5-multiple-LLM-IDE coditect-cloud-ide
gh repo rename coditect-ai/coditect-infrastructure coditect-cloud-infra
# backend and frontend keep names

# Dev (9)
gh repo rename coditect-ai/coditect-context-api coditect-dev-context
gh repo rename coditect-ai/coditect-project-intelligence coditect-dev-intelligence
gh repo rename coditect-ai/coditect-pdf-convertor coditect-dev-pdf
# ... etc

# Market (3)
gh repo rename coditect-ai/coditect-agent-marketplace coditect-market-agents
gh repo rename coditect-ai/coditect-activity-data-model-ui coditect-market-activity

# Docs (5)
gh repo rename coditect-ai/coditect-docs coditect-docs-main

# Ops (3)
gh repo rename coditect-ai/coditect-rollout-master coditect-ops-master

# GTM (7)
gh repo rename coditect-ai/coditect-communications coditect-gtm-comms
gh repo rename coditect-ai/az1.ai-CODITECT.AI-GTM coditect-gtm-strategy
gh repo rename coditect-ai/az1.ai-CODITECT-ERP-CRM coditect-gtm-crm

# Labs (14)
gh repo rename coditect-ai/NESTED-LEARNING-GOOGLE coditect-labs-learning
gh repo rename coditect-ai/az1.ai-coditect-agent-new-standard-development coditect-labs-agent-standards
# ... etc
```

**Acceptance Criteria**:
- [ ] All 49 repos renamed successfully
- [ ] GitHub redirects active for old URLs
- [ ] No permission errors

---

### Phase 4: Repo Transfers (Day 3 - 30 min)

**Goal**: Move halcasteel repos to coditect-ai org

**Team**:
- `codi-devops-engineer` - Transfer operations

**Transfers**:
```bash
gh repo transfer halcasteel/coditect coditect-ai
gh repo transfer halcasteel/coditect-competition coditect-ai
gh repo transfer halcasteel/coditect-core-1.0 coditect-ai
```

**Then rename**:
```bash
gh repo rename coditect-ai/coditect coditect-ops-distribution
gh repo rename coditect-ai/coditect-competition coditect-gtm-competition
```

**Acceptance Criteria**:
- [ ] All halcasteel CODITECT repos in coditect-ai org
- [ ] Ownership and permissions transferred correctly

---

### Phase 5: Submodule Restructure (Day 3-4 - 1.5 hours)

**Goal**: Reorganize submodules into category folders

**Team**:
- `codi-devops-engineer` - Git submodule operations
- `project-organizer` - Folder structure

**New Structure**:
```
submodules/
├── core/           # 3 repos
├── cloud/          # 5 repos
├── dev/            # 9 repos
├── market/         # 3 repos
├── docs/           # 5 repos
├── ops/            # 3 repos
├── gtm/            # 7 repos
└── labs/           # 14 repos
```

**Operations**:
1. Remove all existing submodules
2. Re-add with new paths and URLs
3. Update .gitmodules
4. Commit structure change

**Agent Orchestration**:
```python
Task(subagent_type="codi-devops-engineer",
     prompt="""Restructure submodules into category folders.

     1. Create folder structure: core/, cloud/, dev/, market/, docs/, ops/, gtm/, labs/
     2. Remove existing submodules (preserve .git)
     3. Re-add each submodule to correct category folder with new URL
     4. Update .gitmodules
     5. Verify all submodules initialize correctly

     Reference: docs/ROLLOUT-RESTRUCTURE-PROPOSAL-v1.md for complete mapping""")
```

**Acceptance Criteria**:
- [ ] All 49 submodules in correct category folders
- [ ] .gitmodules updated with new URLs
- [ ] `git submodule update --init --recursive` succeeds

---

### Phase 6: Reference Updates (Day 4-5 - 2 hours)

**Goal**: Update all hardcoded references to old repo names/URLs

**Team**:
- `codi-devops-engineer` - Script bulk updates
- `codi-documentation-writer` - Manual review

**Files to Update**:

| File | Changes |
|------|---------|
| `install.sh` | Update raw.githubusercontent.com URLs |
| `update.sh` | Update raw.githubusercontent.com URLs |
| `*/CLAUDE.md` | Update repo references |
| `*/README.md` | Update GitHub links |
| `.github/workflows/*` | Update repo names |
| `docs/*.md` | Update all GitHub links |

**Bulk Update Script**:
```bash
# Find and replace old URLs
find . -name "*.md" -type f -exec sed -i '' \
  's|halcasteel/coditect|coditect-ai/coditect-ops-distribution|g' {} \;

find . -name "*.sh" -type f -exec sed -i '' \
  's|halcasteel/coditect|coditect-ai/coditect-ops-distribution|g' {} \;
```

**Acceptance Criteria**:
- [ ] No references to old repo names remain
- [ ] install.sh works with new URLs
- [ ] All documentation links valid

---

### Phase 7: Testing & Validation (Day 5 - 1 hour)

**Goal**: Verify everything works correctly

**Team**:
- `codi-test-engineer` - Validation
- `codi-devops-engineer` - Functional tests

**Test Checklist**:
1. Fresh clone with `--recurse-submodules`
2. All submodules initialize correctly
3. install.sh downloads from correct URL
4. update.sh fetches correctly
5. All symlinks intact (.coditect → .claude)
6. CI/CD workflows pass

**Agent Orchestration**:
```python
Task(subagent_type="codi-test-engineer",
     prompt="""Validate repository reorganization:

     1. Clone coditect-ops-master fresh with --recurse-submodules
     2. Verify all 49 submodules present in correct folders
     3. Test install.sh in clean environment
     4. Verify GitHub redirects work for old URLs
     5. Check all internal links in documentation
     6. Report any broken references""")
```

**Acceptance Criteria**:
- [ ] Fresh clone succeeds with all submodules
- [ ] install.sh functional
- [ ] Zero broken links in documentation
- [ ] CI/CD passes

---

### Phase 8: Documentation & Communication (Day 5-6 - 1 hour)

**Goal**: Document new structure and communicate changes

**Team**:
- `codi-documentation-writer` - Update docs

**Deliverables**:
1. Update main README.md with new structure
2. Create REPO-NAMING-CONVENTION.md
3. Update CLAUDE.md with new paths
4. Create migration guide for existing users
5. Archive old structure documentation

**Acceptance Criteria**:
- [ ] README.md reflects new structure
- [ ] Naming convention documented
- [ ] Migration guide for existing clones

---

## Multi-Agent Orchestration Strategy

### Agent Roles

| Agent | Responsibility |
|-------|----------------|
| `codi-devops-engineer` | Git operations, renames, transfers, scripts |
| `project-organizer` | Folder structure, file organization |
| `codi-documentation-writer` | Documentation updates |
| `codi-test-engineer` | Validation and testing |

### Orchestration Patterns

**Phase 1-4**: Sequential execution (dependencies)
```python
# Must complete in order
Phase1() → Phase2() → Phase3() → Phase4()
```

**Phase 5-6**: Can parallelize some work
```python
# Structure and docs can overlap
parallel(Phase5_structure(), Phase6_docs())
```

**Phase 7-8**: Sequential (testing after changes)
```python
Phase7_test() → Phase8_communicate()
```

### Master Orchestration Command

```python
Task(
    subagent_type="orchestrator",
    prompt="""Execute CODITECT repository reorganization.

    Reference: docs/PROJECT-PLAN-REPO-REORGANIZATION.md
    Tasklist: docs/TASKLIST-REPO-REORGANIZATION.md

    Execute phases 1-8 in order:
    1. Preparation & Backup
    2. Consolidations & Merges
    3. GitHub Renames
    4. Repo Transfers
    5. Submodule Restructure
    6. Reference Updates
    7. Testing & Validation
    8. Documentation & Communication

    Coordinate agents as specified in each phase.
    Report progress after each phase completion.
    Stop and report if any phase fails."""
)
```

---

## Quality Gates

### Phase Completion Criteria

| Phase | Gate Criteria |
|-------|---------------|
| Phase 1 | Backup verified, rollback tested |
| Phase 2 | All merges complete, content preserved |
| Phase 3 | All renames successful, redirects active |
| Phase 4 | All transfers complete |
| Phase 5 | All submodules in correct folders |
| Phase 6 | Zero old references remain |
| Phase 7 | All tests pass |
| Phase 8 | Documentation complete |

### Rollback Triggers

Execute rollback if:
- More than 3 rename failures
- Submodule initialization fails
- Critical reference broken (install.sh)
- Data loss detected

---

## Risk Management

### High Priority Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Rename fails mid-execution | Low | High | Script all renames, test first |
| Broken install.sh | Medium | High | Test immediately after URL update |
| Lost git history | Low | Medium | Use proper merge techniques |
| Permission errors | Low | Medium | Verify gh auth before starting |

### Contingency Plans

**If rename fails**:
1. Note which repos completed
2. Continue from failure point
3. GitHub redirects protect partial state

**If install.sh breaks**:
1. Rollback URL changes immediately
2. Fix and re-test before continuing

---

## Success Metrics

### Technical Metrics
- [ ] All 49 submodules accessible
- [ ] Zero broken links
- [ ] install.sh functional
- [ ] CI/CD passes

### Organization Metrics
- [ ] 8 clear categories
- [ ] Consistent naming convention
- [ ] Alphabetical sorting works

### Efficiency Metrics
- [ ] Find any repo in <10 seconds
- [ ] New developer onboarding <30 minutes
- [ ] Zero ambiguity in repo purposes

---

## Budget Breakdown

### Time Investment

| Phase | Hours |
|-------|-------|
| Phase 1: Preparation | 2.0 |
| Phase 2: Consolidations | 2.0 |
| Phase 3: Renames | 1.5 |
| Phase 4: Transfers | 0.5 |
| Phase 5: Restructure | 1.5 |
| Phase 6: References | 2.0 |
| Phase 7: Testing | 1.0 |
| Phase 8: Documentation | 1.0 |
| **Total** | **11.5 hours** |

### Resource Requirements
- GitHub CLI (`gh`) with admin permissions
- Git with submodule support
- Text editor for bulk find/replace
- Test environment for install.sh validation

---

## Timeline

### Day 1 (4 hours)
- Phase 1: Preparation & Backup
- Phase 2: Consolidations & Merges
- Begin Phase 3: Renames

### Day 2 (3 hours)
- Complete Phase 3: Renames
- Phase 4: Transfers
- Begin Phase 5: Restructure

### Day 3 (3 hours)
- Complete Phase 5: Restructure
- Phase 6: Reference Updates

### Day 4 (1.5 hours)
- Phase 7: Testing & Validation
- Phase 8: Documentation

---

## Next Steps

1. **Review this plan** - Confirm phases and approach
2. **Generate tasklist** - Create TASKLIST-REPO-REORGANIZATION.md
3. **Execute Phase 1** - Start with backup and preparation
4. **Proceed sequentially** - Complete each phase before next

---

*Generated: 2025-11-19*
*Total Phases: 8*
*Total Time: 11.5 hours*
*Repos Affected: 49*
*Ready for: ORCHESTRATOR execution*
