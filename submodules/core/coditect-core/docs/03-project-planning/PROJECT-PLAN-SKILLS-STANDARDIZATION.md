# PROJECT-PLAN-SKILLS-STANDARDIZATION.md

## Project Overview

**Project Name**: CODITECT Skills Standardization Initiative
**Start Date**: 2025-11-19
**Estimated Duration**: 1-2 days
**Priority**: P1 (High - Foundational Quality)
**Status**: Planning Complete

### Objective

Standardize all 21 CODITECT skill directories to ensure consistent structure, proper YAML frontmatter, required sections, and accurate REGISTRY.json entries. This establishes quality foundations for the skill ecosystem and enables reliable AI agent skill discovery.

### Success Criteria

- [ ] All 21 skills have properly named `SKILL.md` files
- [ ] All skills have valid YAML frontmatter with `name` and `description` fields
- [ ] All skills contain required sections: When to Use, Core Capabilities, Examples, Guidelines
- [ ] REGISTRY.json updated with all 21 skills (currently missing 6)
- [ ] 100% compliance with skill format standard from README.md

---

## Current State Analysis

### Skills Inventory (21 Total)

| # | Skill Directory | SKILL.md Exists | YAML Frontmatter | Required Sections | In REGISTRY |
|---|-----------------|-----------------|------------------|-------------------|-------------|
| 1 | ai-curriculum-development | Yes | Yes | Yes | No |
| 2 | build-deploy-workflow | Yes | Needs Audit | Needs Audit | Yes |
| 3 | code-analysis-planning-editor | NO (wrong name) | N/A | N/A | No |
| 4 | code-editor | Yes | Yes | Needs Audit | Yes |
| 5 | communication-protocols | Yes | Yes | Needs Audit | Yes |
| 6 | cross-file-documentation-update | Yes | Needs Audit | Needs Audit | Yes |
| 7 | deployment-archeology | Yes | NO | Partial | No |
| 8 | document-skills | Has subdirs | Needs Audit | Needs Audit | No |
| 9 | evaluation-framework | Yes | Needs Audit | Needs Audit | Yes |
| 10 | foundationdb-queries | Yes | Needs Audit | Needs Audit | Yes |
| 11 | framework-patterns | Yes | Needs Audit | Needs Audit | Yes |
| 12 | gcp-resource-cleanup | Yes | Needs Audit | Needs Audit | Yes |
| 13 | git-workflow-automation | Yes | Needs Audit | Needs Audit | Yes |
| 14 | google-cloud-build | Yes | NO | Partial | No |
| 15 | internal-comms | Yes | Needs Audit | Needs Audit | Yes |
| 16 | multi-agent-workflow | Yes | Needs Audit | Needs Audit | Yes |
| 17 | notebooklm-content-optimization | Yes | Yes | Yes | No |
| 18 | production-patterns | Yes | Needs Audit | Needs Audit | Yes |
| 19 | rust-backend-patterns | Yes | Needs Audit | Needs Audit | Yes |
| 20 | search-strategies | Yes | Needs Audit | Needs Audit | Yes |
| 21 | token-cost-tracking | Yes | Needs Audit | Needs Audit | Yes |

### Critical Issues Identified

1. **Missing SKILL.md**: `code-analysis-planning-editor` has `CODE_EDITOR_SKILL.md` instead of `SKILL.md`
2. **Missing YAML Frontmatter**: `deployment-archeology` and `google-cloud-build` lack proper frontmatter
3. **Missing from REGISTRY**: 6 skills not in REGISTRY.json:
   - ai-curriculum-development
   - code-analysis-planning-editor
   - deployment-archeology
   - document-skills
   - google-cloud-build
   - notebooklm-content-optimization

### REGISTRY.json Status

- **Current entries**: 15 skills
- **Should have**: 21 skills
- **Missing**: 6 entries

---

## Skill Format Standard

### Required SKILL.md Structure

```yaml
---
name: skill-name          # kebab-case, lowercase
description: Clear description of when to use
---

# Skill Title

## When to Use

[Specific scenarios - bulleted list]

## Core Capabilities

[What this skill enables]

## Examples

[Concrete usage examples]

## Guidelines/Best Practices

[Rules, constraints, dos and don'ts]
```

### Optional Elements

- `core/` - Executable Python scripts
- `examples/` - Usage examples
- `templates/` - Templates for generation

---

## Phase Plan

### Phase 1: Audit (2-3 hours)

**Goal**: Complete assessment of all 21 skills against the standard

**Agent Assignment**: qa-reviewer (quality assurance specialist)

**Tasks**:
1. Audit each skill directory for:
   - SKILL.md existence and naming
   - YAML frontmatter validity
   - Required section presence
   - Content quality
2. Generate compliance report
3. Categorize issues by severity:
   - **Critical**: Missing SKILL.md or YAML frontmatter
   - **Major**: Missing required sections
   - **Minor**: Formatting or content quality issues

**Deliverables**:
- Compliance audit report for each skill
- Summary of all issues categorized by severity
- Prioritized fix list

### Phase 2: Fix (4-6 hours)

**Goal**: Remediate all compliance issues

**Agent Assignment**: codi-documentation-writer (technical documentation specialist)

**Tasks**:
1. **Critical Fixes** (Must complete):
   - Rename `CODE_EDITOR_SKILL.md` to `SKILL.md` in code-analysis-planning-editor
   - Add YAML frontmatter to `deployment-archeology/SKILL.md`
   - Add YAML frontmatter to `google-cloud-build/SKILL.md`

2. **Major Fixes** (Must complete):
   - Add missing "When to Use" sections
   - Add missing "Core Capabilities" sections
   - Add missing "Examples" sections
   - Add missing "Guidelines" sections

3. **REGISTRY.json Updates** (Must complete):
   - Add entry for ai-curriculum-development
   - Add entry for code-analysis-planning-editor
   - Add entry for deployment-archeology
   - Add entry for document-skills (with subdirectory notes)
   - Add entry for google-cloud-build
   - Add entry for notebooklm-content-optimization

4. **Minor Fixes** (As time permits):
   - Improve content quality
   - Standardize formatting
   - Add cross-references

**Deliverables**:
- All 21 skills compliant with standard
- REGISTRY.json with all 21 entries
- Git commit with all changes

### Phase 3: Validate (1-2 hours)

**Goal**: Verify all fixes are correct and complete

**Agent Assignment**: qa-reviewer

**Tasks**:
1. Re-audit all 21 skills
2. Verify REGISTRY.json validity (JSON syntax)
3. Test skill loading in Claude Code
4. Update README.md if needed
5. Final sign-off

**Deliverables**:
- Final compliance report (100% pass)
- Validation summary
- Updated README.md (if changes needed)

---

## Timeline

### Day 1 (Estimated 6-8 hours)

| Time | Phase | Tasks | Agent |
|------|-------|-------|-------|
| Hour 1-2 | Phase 1 | Full audit of all 21 skills | qa-reviewer |
| Hour 3 | Phase 1 | Compile audit report, prioritize fixes | qa-reviewer |
| Hour 4-6 | Phase 2 | Fix critical and major issues | codi-documentation-writer |
| Hour 7-8 | Phase 2 | Update REGISTRY.json, minor fixes | codi-documentation-writer |

### Day 2 (If needed, 2-4 hours)

| Time | Phase | Tasks | Agent |
|------|-------|-------|-------|
| Hour 1-2 | Phase 2 | Complete remaining fixes | codi-documentation-writer |
| Hour 3-4 | Phase 3 | Validation and final sign-off | qa-reviewer |

---

## Risk Assessment

### Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Skills have dependencies on current structure | High | Low | Test skill loading after changes |
| REGISTRY.json syntax errors | Medium | Medium | Validate JSON syntax before commit |
| Missing content requires research | Medium | Medium | Flag for follow-up if complex |
| Breaking changes to skill names | High | Low | Update all references in CLAUDE.md |

### Rollback Plan

If issues are discovered post-standardization:
1. Git revert to pre-standardization commit
2. Investigate specific failing skills
3. Apply targeted fixes
4. Re-validate before next commit

---

## Success Metrics

### Quantitative Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Skills with valid SKILL.md | 21/21 (100%) | File existence check |
| Skills with YAML frontmatter | 21/21 (100%) | YAML parser validation |
| Skills with required sections | 21/21 (100%) | Section header check |
| REGISTRY.json entries | 21/21 (100%) | Entry count |
| Audit pass rate | 100% | Final audit results |

### Qualitative Metrics

- Consistent skill structure across all 21 skills
- Clear, actionable "When to Use" guidance
- Comprehensive "Core Capabilities" documentation
- Practical, copy-paste-ready examples
- Actionable "Guidelines" with dos and don'ts

---

## Resource Requirements

### Agent Requirements

1. **qa-reviewer** (Audit and Validation)
   - Phase 1: Full audit (~3 hours)
   - Phase 3: Final validation (~2 hours)
   - Total: ~5 hours

2. **codi-documentation-writer** (Fixes)
   - Phase 2: All remediation (~6 hours)
   - Total: ~6 hours

### Tools Required

- Read tool (inspect SKILL.md files)
- Write tool (create/update files)
- Edit tool (modify existing content)
- Grep tool (search for patterns)
- Glob tool (find all SKILL.md files)
- Bash tool (git operations)

### Token Budget

- Phase 1 (Audit): ~30K tokens
- Phase 2 (Fix): ~50K tokens
- Phase 3 (Validate): ~20K tokens
- **Total**: ~100K tokens

---

## Deliverables Checklist

### Phase 1 Deliverables
- [ ] Individual audit report for each skill
- [ ] Compliance summary with severity ratings
- [ ] Prioritized fix list

### Phase 2 Deliverables
- [ ] All SKILL.md files renamed/created
- [ ] All YAML frontmatter added/fixed
- [ ] All required sections present
- [ ] Updated REGISTRY.json with 21 entries
- [ ] Git commit with all changes

### Phase 3 Deliverables
- [ ] Final audit report (100% compliance)
- [ ] JSON validation confirmation
- [ ] Claude Code loading test results
- [ ] Updated README.md (if needed)
- [ ] Project completion sign-off

---

## Next Steps

1. **Immediate**: Review this PROJECT-PLAN and approve
2. **Start Phase 1**: Execute TASKLIST-SKILLS-STANDARDIZATION.md audit tasks
3. **Execute Phases 2-3**: Follow tasklist checkboxes
4. **Final**: Commit all changes with descriptive message

---

## Related Documents

- **TASKLIST-SKILLS-STANDARDIZATION.md** - Detailed checkbox tasks
- **skills/README.md** - Skill format standard reference
- **skills/REGISTRY.json** - Current registry (15 entries)
- **SKILL-ENHANCEMENT-LOG.md** - Previous skill improvements

---

**Document Version**: 1.0
**Created**: 2025-11-19
**Author**: Orchestrator Agent
**Status**: Ready for Execution
