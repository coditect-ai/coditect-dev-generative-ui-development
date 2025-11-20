# CODITECT Repository Reorganization - Tasklist

## Progress Summary

| Phase | Tasks | Completed | In Progress | Pending | % Complete |
|-------|-------|-----------|-------------|---------|------------|
| Phase 1: Preparation | 8 | 0 | 0 | 8 | 0% |
| Phase 2: Consolidations | 12 | 0 | 0 | 12 | 0% |
| Phase 3: Renames | 25 | 0 | 0 | 25 | 0% |
| Phase 4: Transfers | 6 | 0 | 0 | 6 | 0% |
| Phase 5: Restructure | 18 | 0 | 0 | 18 | 0% |
| Phase 6: References | 15 | 0 | 0 | 15 | 0% |
| Phase 7: Testing | 10 | 0 | 0 | 10 | 0% |
| Phase 8: Documentation | 8 | 0 | 0 | 8 | 0% |
| **Total** | **102** | **0** | **0** | **102** | **0%** |

---

## Phase 1: Preparation & Backup (Day 1 - 2 hours)

### 1.1 Backup Current State
**Agent**: `codi-devops-engineer`
**Duration**: 30 min
**Dependencies**: None

- [ ] Create backup directory `backups/pre-reorg-2025-11-19/`
- [ ] Copy current `.gitmodules` to backup
- [ ] Export current submodule SHAs: `git submodule status > backup/submodule-shas.txt`
- [ ] Create tarball of docs/ directory

**Acceptance**: Backup directory contains .gitmodules and SHA list

---

### 1.2 Create Rollback Script
**Agent**: `codi-devops-engineer`
**Duration**: 30 min
**Dependencies**: 1.1

- [ ] Create `scripts/rollback-reorg.sh`
- [ ] Script restores .gitmodules from backup
- [ ] Script resets submodule paths
- [ ] Test rollback on copy of repo

**Acceptance**: Rollback script documented and tested

---

### 1.3 Verify Permissions
**Agent**: `codi-devops-engineer`
**Duration**: 15 min
**Dependencies**: None

- [ ] Run `gh auth status` - verify admin access
- [ ] Verify write access to coditect-ai org
- [ ] Verify write access to halcasteel repos
- [ ] Test rename on throwaway repo

**Acceptance**: All permissions confirmed

---

## Phase 2: Consolidations & Merges (Day 1-2 - 2 hours)

### 2.1 Merge coditect-installer → coditect
**Agent**: `codi-devops-engineer`
**Duration**: 45 min
**Dependencies**: Phase 1 complete

- [ ] Clone both repos locally
- [ ] Copy coditect-installer content into coditect
- [ ] Resolve any conflicts
- [ ] Commit with merge message
- [ ] Push to halcasteel/coditect
- [ ] Archive coditect-ai/coditect-installer

**Acceptance**: All installer content in halcasteel/coditect

---

### 2.2 Merge coditect-license-server → coditect-license-manager
**Agent**: `codi-devops-engineer`
**Duration**: 45 min
**Dependencies**: Phase 1 complete

- [ ] Clone both repos locally
- [ ] Copy license-server content into license-manager
- [ ] Resolve any conflicts
- [ ] Update imports/references as needed
- [ ] Commit with merge message
- [ ] Push to coditect-ai/coditect-license-manager
- [ ] Archive coditect-ai/coditect-license-server

**Acceptance**: License server functionality in license-manager

---

### 2.3 Merge competitive research
**Agent**: `codi-devops-engineer`
**Duration**: 30 min
**Dependencies**: Phase 1 complete

- [ ] Copy az1.ai-coditect-AI-IDE-competitive-market-research content
- [ ] Add to halcasteel/coditect-competition
- [ ] Commit with merge message
- [ ] Archive source repo

**Acceptance**: All competitive research consolidated

---

## Phase 3: GitHub Renames (Day 2-3 - 1.5 hours)

### 3.1 Rename Core Repos (3)
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: Phase 2 complete

- [ ] `gh repo rename coditect-ai/coditect-project-dot-claude coditect-core-dotclaude`
- [ ] `gh repo rename coditect-ai/coditect-framework coditect-core-framework`
- [ ] `gh repo rename coditect-ai/coditect-distributed-architecture coditect-core-architecture`

**Acceptance**: All core repos renamed, redirects active

---

### 3.2 Rename Cloud Repos (5)
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: Phase 2 complete

- [ ] `gh repo rename coditect-ai/Coditect-v5-multiple-LLM-IDE coditect-cloud-ide`
- [ ] `gh repo rename coditect-ai/coditect-infrastructure coditect-cloud-infra`
- [ ] Verify coditect-cloud-backend (no change needed)
- [ ] Verify coditect-cloud-frontend (no change needed)
- [ ] Note: foundationdb added later from az1-ai

**Acceptance**: All cloud repos renamed

---

### 3.3 Rename Dev Repos (9)
**Agent**: `codi-devops-engineer`
**Duration**: 15 min
**Dependencies**: Phase 2 complete

- [ ] Verify coditect-cli (no change needed)
- [ ] Verify coditect-automation (no change needed)
- [ ] Verify coditect-analytics (no change needed)
- [ ] `gh repo rename coditect-ai/coditect-context-api coditect-dev-context`
- [ ] `gh repo rename coditect-ai/coditect-project-intelligence coditect-dev-intelligence`
- [ ] `gh repo rename coditect-ai/coditect-pdf-convertor coditect-dev-pdf`
- [ ] `gh repo rename coditect-ai/az1.ai-coditect-audio2text-workflow coditect-dev-audio2text`
- [ ] `gh repo rename coditect-ai/az1.ai-coditect-contact-qr-code-generator coditect-dev-qrcode`

**Acceptance**: All dev repos renamed

---

### 3.4 Rename Market Repos (3)
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: Phase 2 complete

- [ ] `gh repo rename coditect-ai/coditect-agent-marketplace coditect-market-agents`
- [ ] `gh repo rename coditect-ai/coditect-activity-data-model-ui coditect-market-activity`
- [ ] Note: enterprise-agents added later from az1-ai

**Acceptance**: All market repos renamed

---

### 3.5 Rename Docs Repos (5)
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: Phase 2 complete

- [ ] `gh repo rename coditect-ai/coditect-docs coditect-docs-main`
- [ ] Verify coditect-legal (no change needed)
- [ ] Verify coditect-blog-application → `coditect-docs-blog`
- [ ] `gh repo rename coditect-ai/az1.ai-coditect-ai-syllubus-curriculum-course-material coditect-docs-training`
- [ ] `gh repo rename coditect-ai/coditect-claude-code-initial-setup coditect-docs-setup`

**Acceptance**: All docs repos renamed

---

### 3.6 Rename Ops Repos (3)
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: Phase 2 complete

- [ ] `gh repo rename coditect-ai/coditect-rollout-master coditect-ops-master`
- [ ] Note: distribution and license renamed after transfer (Phase 4)
- [ ] `gh repo rename coditect-ai/coditect-projects coditect-ops-projects`

**Acceptance**: Ops repos renamed

---

### 3.7 Rename GTM Repos (7)
**Agent**: `codi-devops-engineer`
**Duration**: 15 min
**Dependencies**: Phase 2 complete

- [ ] `gh repo rename coditect-ai/coditect-communications coditect-gtm-comms`
- [ ] `gh repo rename coditect-ai/az1.ai-CODITECT.AI-GTM coditect-gtm-strategy`
- [ ] `gh repo rename coditect-ai/az1.ai-CODITECT-ERP-CRM coditect-gtm-crm`
- [ ] Note: competition renamed after transfer
- [ ] `gh repo rename coditect-ai/coditect-persona-customer-questions coditect-gtm-personas`
- [ ] `gh repo rename coditect-ai/coditect-customer-clipora-ravi-mehta coditect-gtm-customer-clipora`
- [ ] `gh repo rename coditect-ai/product-legitimacy-enterprise-software coditect-gtm-legitimacy`

**Acceptance**: All GTM repos renamed

---

### 3.8 Rename Labs Repos (14)
**Agent**: `codi-devops-engineer`
**Duration**: 20 min
**Dependencies**: Phase 2 complete

- [ ] `gh repo rename coditect-ai/NESTED-LEARNING-GOOGLE coditect-labs-learning`
- [ ] `gh repo rename coditect-ai/az1.ai-coditect-agent-new-standard-development coditect-labs-agent-standards`
- [ ] `gh repo rename coditect-ai/az1.ai-coditect-ai-screenshot-automator coditect-labs-screenshot`
- [ ] `gh repo rename coditect-ai/coditect-interactive-workflow-analyzer coditect-labs-workflow`
- [ ] `gh repo rename coditect-ai/agents-research-plan-code coditect-labs-agents-research`
- [ ] `gh repo rename coditect-ai/claude-code-functionality-tools-research coditect-labs-claude-research`
- [ ] `gh repo rename coditect-ai/az1.ai-coditect-first-principles-analysis coditect-labs-first-principles`
- [ ] `gh repo rename coditect-ai/CODITECTv4 coditect-labs-v4-archive`
- [ ] `gh repo rename coditect-ai/Coditect-MCP-RAG-Claude-Code-AUTH coditect-labs-mcp-auth`
- [ ] `gh repo rename coditect-ai/Coditect-Multi-Agent-RAG-Pipeline coditect-labs-multi-agent-rag`
- [ ] `gh repo rename coditect-ai/claude-cli-web-architecture coditect-labs-cli-web-arch`

**Acceptance**: All labs repos renamed

---

## Phase 4: Repo Transfers (Day 3 - 30 min)

### 4.1 Transfer halcasteel repos to coditect-ai
**Agent**: `codi-devops-engineer`
**Duration**: 15 min
**Dependencies**: Phase 3 complete

- [ ] `gh repo transfer halcasteel/coditect coditect-ai`
- [ ] `gh repo transfer halcasteel/coditect-competition coditect-ai`
- [ ] `gh repo transfer halcasteel/coditect-core-1.0 coditect-ai` (if needed)

**Acceptance**: Repos visible in coditect-ai org

---

### 4.2 Rename transferred repos
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: 4.1

- [ ] `gh repo rename coditect-ai/coditect coditect-ops-distribution`
- [ ] `gh repo rename coditect-ai/coditect-competition coditect-gtm-competition`
- [ ] `gh repo rename coditect-ai/coditect-license-manager coditect-ops-license`

**Acceptance**: Transferred repos follow naming convention

---

## Phase 5: Submodule Restructure (Day 3-4 - 1.5 hours)

### 5.1 Create folder structure
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: Phase 4 complete

- [ ] Create `submodules/core/`
- [ ] Create `submodules/cloud/`
- [ ] Create `submodules/dev/`
- [ ] Create `submodules/market/`
- [ ] Create `submodules/docs/`
- [ ] Create `submodules/ops/`
- [ ] Create `submodules/gtm/`
- [ ] Create `submodules/labs/`

**Acceptance**: All 8 category folders exist

---

### 5.2 Remove existing submodules
**Agent**: `codi-devops-engineer`
**Duration**: 30 min
**Dependencies**: 5.1

- [ ] Record all current submodule URLs
- [ ] Run `git submodule deinit -f --all`
- [ ] Remove submodule entries from .gitmodules
- [ ] Remove submodule directories
- [ ] Clean .git/modules

**Acceptance**: No submodules registered, clean state

---

### 5.3 Re-add core submodules
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: 5.2

- [ ] `git submodule add https://github.com/coditect-ai/coditect-core-dotclaude submodules/core/coditect-core-dotclaude`
- [ ] `git submodule add https://github.com/coditect-ai/coditect-core-framework submodules/core/coditect-core-framework`
- [ ] `git submodule add https://github.com/coditect-ai/coditect-core-architecture submodules/core/coditect-core-architecture`

**Acceptance**: Core submodules in submodules/core/

---

### 5.4 Re-add cloud submodules
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: 5.2

- [ ] Add coditect-cloud-backend to submodules/cloud/
- [ ] Add coditect-cloud-frontend to submodules/cloud/
- [ ] Add coditect-cloud-ide to submodules/cloud/
- [ ] Add coditect-cloud-infra to submodules/cloud/
- [ ] Add coditect-cloud-foundationdb to submodules/cloud/

**Acceptance**: Cloud submodules in submodules/cloud/

---

### 5.5 Re-add dev submodules
**Agent**: `codi-devops-engineer`
**Duration**: 15 min
**Dependencies**: 5.2

- [ ] Add all 9 dev repos to submodules/dev/

**Acceptance**: Dev submodules in submodules/dev/

---

### 5.6 Re-add market submodules
**Agent**: `codi-devops-engineer`
**Duration**: 5 min
**Dependencies**: 5.2

- [ ] Add all 3 market repos to submodules/market/

**Acceptance**: Market submodules in submodules/market/

---

### 5.7 Re-add docs submodules
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: 5.2

- [ ] Add all 5 docs repos to submodules/docs/

**Acceptance**: Docs submodules in submodules/docs/

---

### 5.8 Re-add ops submodules
**Agent**: `codi-devops-engineer`
**Duration**: 5 min
**Dependencies**: 5.2

- [ ] Add all 3 ops repos to submodules/ops/

**Acceptance**: Ops submodules in submodules/ops/

---

### 5.9 Re-add gtm submodules
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: 5.2

- [ ] Add all 7 gtm repos to submodules/gtm/

**Acceptance**: GTM submodules in submodules/gtm/

---

### 5.10 Re-add labs submodules
**Agent**: `codi-devops-engineer`
**Duration**: 15 min
**Dependencies**: 5.2

- [ ] Add all 14 labs repos to submodules/labs/

**Acceptance**: Labs submodules in submodules/labs/

---

### 5.11 Update communications submodule
**Agent**: `codi-devops-engineer`
**Duration**: 5 min
**Dependencies**: 5.2

- [ ] Move communications from root to submodules/gtm/coditect-gtm-comms

**Acceptance**: No submodules at root level (except .coditect)

---

## Phase 6: Reference Updates (Day 4-5 - 2 hours)

### 6.1 Update install.sh
**Agent**: `codi-devops-engineer`
**Duration**: 20 min
**Dependencies**: Phase 5 complete

- [ ] Update CODITECT_REPO URL to coditect-ai/coditect-ops-distribution
- [ ] Update raw.githubusercontent.com URLs
- [ ] Test URL accessibility
- [ ] Commit changes

**Acceptance**: install.sh uses new URLs

---

### 6.2 Update update.sh
**Agent**: `codi-devops-engineer`
**Duration**: 10 min
**Dependencies**: Phase 5 complete

- [ ] Update all GitHub URLs
- [ ] Test URL accessibility
- [ ] Commit changes

**Acceptance**: update.sh uses new URLs

---

### 6.3 Bulk update CLAUDE.md files
**Agent**: `codi-devops-engineer`
**Duration**: 30 min
**Dependencies**: Phase 5 complete

- [ ] Find all CLAUDE.md files in submodules
- [ ] Search/replace old repo names with new
- [ ] Verify no broken references
- [ ] Commit changes

**Acceptance**: All CLAUDE.md files updated

---

### 6.4 Bulk update README.md files
**Agent**: `codi-documentation-writer`
**Duration**: 30 min
**Dependencies**: Phase 5 complete

- [ ] Find all README.md files
- [ ] Update GitHub links to new repo names
- [ ] Update any architecture diagrams
- [ ] Commit changes

**Acceptance**: All README links valid

---

### 6.5 Update CI/CD workflows
**Agent**: `codi-devops-engineer`
**Duration**: 30 min
**Dependencies**: Phase 5 complete

- [ ] Find all .github/workflows/*.yml files
- [ ] Update repo name references
- [ ] Update checkout actions
- [ ] Test workflow syntax

**Acceptance**: All workflows use new names

---

### 6.6 Update main docs/
**Agent**: `codi-documentation-writer`
**Duration**: 20 min
**Dependencies**: Phase 5 complete

- [ ] Update all docs/*.md files
- [ ] Fix any internal links
- [ ] Update diagrams if needed

**Acceptance**: Documentation links valid

---

## Phase 7: Testing & Validation (Day 5 - 1 hour)

### 7.1 Fresh clone test
**Agent**: `codi-test-engineer`
**Duration**: 15 min
**Dependencies**: Phase 6 complete

- [ ] Clone coditect-ops-master with `--recurse-submodules`
- [ ] Verify all 49 submodules initialize
- [ ] Check submodule paths are correct

**Acceptance**: Fresh clone works perfectly

---

### 7.2 Submodule validation
**Agent**: `codi-test-engineer`
**Duration**: 15 min
**Dependencies**: 7.1

- [ ] Run `git submodule status` - all should show clean
- [ ] Verify each category folder has correct repos
- [ ] Check symlinks (.coditect → .claude)

**Acceptance**: All submodules functional

---

### 7.3 Install script test
**Agent**: `codi-test-engineer`
**Duration**: 15 min
**Dependencies**: Phase 6 complete

- [ ] Run install.sh in clean environment
- [ ] Verify it downloads from correct URL
- [ ] Check installation completes successfully

**Acceptance**: install.sh functional

---

### 7.4 Link validation
**Agent**: `codi-test-engineer`
**Duration**: 10 min
**Dependencies**: Phase 6 complete

- [ ] Check all GitHub links in README.md
- [ ] Verify old URLs redirect properly
- [ ] Test external documentation links

**Acceptance**: Zero broken links

---

### 7.5 Redirect validation
**Agent**: `codi-test-engineer`
**Duration**: 5 min
**Dependencies**: Phase 3 complete

- [ ] Test old repo URLs redirect to new names
- [ ] Verify halcasteel/coditect redirects to coditect-ai/coditect-ops-distribution

**Acceptance**: All redirects working

---

## Phase 8: Documentation & Communication (Day 5-6 - 1 hour)

### 8.1 Update main README.md
**Agent**: `codi-documentation-writer`
**Duration**: 20 min
**Dependencies**: Phase 7 complete

- [ ] Update submodule structure section
- [ ] Add new folder organization
- [ ] Update getting started instructions
- [ ] Update clone commands

**Acceptance**: README reflects new structure

---

### 8.2 Create REPO-NAMING-CONVENTION.md
**Agent**: `codi-documentation-writer`
**Duration**: 15 min
**Dependencies**: Phase 7 complete

- [ ] Document 8 category prefixes
- [ ] Provide examples for each category
- [ ] Add rules for new repo creation
- [ ] Include decision tree for categorization

**Acceptance**: Convention documented for future use

---

### 8.3 Update CLAUDE.md
**Agent**: `codi-documentation-writer`
**Duration**: 15 min
**Dependencies**: Phase 7 complete

- [ ] Update all submodule paths
- [ ] Update architecture diagrams
- [ ] Add new folder structure

**Acceptance**: CLAUDE.md accurate

---

### 8.4 Create migration guide
**Agent**: `codi-documentation-writer`
**Duration**: 10 min
**Dependencies**: Phase 7 complete

- [ ] Instructions for users with existing clones
- [ ] How to update remotes
- [ ] How to re-sync submodules

**Acceptance**: Migration guide available

---

## Completion Checklist

### Final Validation

- [ ] All 49 submodules in correct category folders
- [ ] All repos follow naming convention
- [ ] All repos in coditect-ai org
- [ ] install.sh works
- [ ] Fresh clone works
- [ ] Zero broken links
- [ ] Documentation updated
- [ ] Rollback script available (just in case)

### Commit & Push

- [ ] Commit all changes with comprehensive message
- [ ] Push to main branch
- [ ] Tag release: `v2.0.0-reorganized`
- [ ] Create GitHub release notes

---

## Agent Invocation Quick Reference

### Execute Full Reorganization
```python
Task(
    subagent_type="orchestrator",
    prompt="Execute repository reorganization following docs/TASKLIST-REPO-REORGANIZATION.md phases 1-8"
)
```

### Execute Single Phase
```python
Task(
    subagent_type="codi-devops-engineer",
    prompt="Execute Phase 3 (GitHub Renames) from docs/TASKLIST-REPO-REORGANIZATION.md"
)
```

### Validate Results
```python
Task(
    subagent_type="codi-test-engineer",
    prompt="Validate repository reorganization per Phase 7 of docs/TASKLIST-REPO-REORGANIZATION.md"
)
```

---

*Generated: 2025-11-19*
*Total Tasks: 102*
*Estimated Time: 11.5 hours*
*Categories: 8*
*Repos: 49*
