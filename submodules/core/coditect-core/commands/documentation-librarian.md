---
name: documentation-librarian
description: Invoke documentation-librarian agent for documentation organization, navigation file generation, content deduplication, and quality automation
---

# Documentation Librarian Command

Invoke the **documentation-librarian** agent to transform scattered documentation into organized, navigable systems with automated quality monitoring.

## Usage

```bash
/documentation-librarian [task description]
```

The command expands to proper Task tool invocation with the documentation-librarian agent.

## Examples

### Example 1: Analyze Documentation

```bash
/documentation-librarian analyze docs/ directory for duplicate content and create reorganization plan
```

Expands to:
```
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to analyze docs/ directory for duplicate content and create reorganization plan"
)
```

**Result:**
- Complete inventory of markdown files
- Categorization by audience and purpose
- Duplicate content identification
- Consolidation recommendations
- Proposed directory structure

### Example 2: Reorganize Documentation

```bash
/documentation-librarian reorganize 50+ markdown files from docs root into proper subdirectories
```

Expands to:
```
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to reorganize 50+ markdown files from docs root into proper subdirectories"
)
```

**Result:**
- Files moved to logical subdirectories (git history preserved)
- 0 files remaining in docs root
- All cross-references validated

### Example 3: Generate Navigation Files

```bash
/documentation-librarian generate README.md and CLAUDE.md files for all subdirectories in docs/
```

Expands to:
```
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to generate README.md and CLAUDE.md files for all subdirectories in docs/"
)
```

**Result:**
- README.md in each directory with file listings
- CLAUDE.md with agent-specific context
- Cross-reference links between related docs

### Example 4: Consolidate Duplicate Content

```bash
/documentation-librarian identify and consolidate duplicate documentation into master documents
```

Expands to:
```
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to identify and consolidate duplicate documentation into master documents"
)
```

**Result:**
- Similarity analysis of all documents
- Merged content preserving all unique information
- Typically 30-50% file reduction
- Updated cross-references

### Example 5: Validate Cross-References

```bash
/documentation-librarian validate all cross-references and fix broken links
```

Expands to:
```
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to validate all cross-references and fix broken links"
)
```

**Result:**
- All markdown links validated
- Broken links fixed with correct paths
- Report of links updated
- Orphaned documents flagged

### Example 6: Set Up Automation

```bash
/documentation-librarian create automated link validation and freshness monitoring system
```

Expands to:
```
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to create automated link validation and freshness monitoring system"
)
```

**Result:**
- Python script for link validation
- Freshness monitoring (weekly reports)
- Auto-generated documentation index
- Git hooks for documentation checks

## When to Use

✅ **Use /documentation-librarian when:**
- Organizing 20+ documentation files scattered across directories
- Creating navigation systems (README.md, CLAUDE.md)
- Consolidating duplicate or overlapping content
- Validating and fixing cross-references after reorganizations
- Setting up automated documentation quality monitoring
- Generating documentation indexes and maps
- Auditing documentation completeness and freshness

❌ **Don't use /documentation-librarian when:**
- Writing new documentation content (use `/document` instead)
- Single-file quick edits (use direct Edit tool)
- Generating API documentation (use `/document`)
- Code documentation (use language-specific commands)

## Common Workflows

### Workflow 1: Complete Documentation Reorganization

```bash
# Step 1: Analyze current state
/documentation-librarian analyze docs/ directory and create comprehensive reorganization plan

# Step 2: Review plan, then execute
/documentation-librarian execute approved reorganization plan

# Step 3: Set up ongoing quality
/documentation-librarian create automation for link validation and freshness monitoring
```

### Workflow 2: Fix Broken Links After Migration

```bash
# After moving files manually or via other tools
/documentation-librarian find all broken links and fix them with correct paths
```

### Workflow 3: Content Consolidation

```bash
# Step 1: Identify duplicates
/documentation-librarian analyze all documentation for duplicate and overlapping content

# Step 2: Consolidate
/documentation-librarian consolidate identified duplicates into master documents preserving all unique information
```

### Workflow 4: Generate Navigation

```bash
# Create README.md and CLAUDE.md for entire documentation tree
/documentation-librarian generate comprehensive navigation files for all directories in docs/
```

## Output Format

The agent provides structured outputs including:

**Analysis Reports:**
- File inventory with metadata (count, sizes, last modified)
- Categorization matrix (audience x purpose)
- Duplicate content analysis with similarity scores
- Gap identification (missing documentation)
- Consolidation recommendations with impact assessment

**Reorganization Plans:**
- Proposed directory structure with rationale
- Migration plan with git mv commands
- Before/after file count comparison
- Risk assessment and rollback strategy

**Implementation Results:**
- Files moved (count and locations)
- Duplicates consolidated (file reduction percentage)
- Links validated and fixed (statistics)
- Navigation files generated (README.md, CLAUDE.md)

**Automation Artifacts:**
- Python/Bash scripts for link validation
- Freshness monitoring configuration
- Git hooks for documentation checks
- Documentation metrics dashboard

## Related Commands

- `/document` - Create new documentation content (codi-documentation-writer)
- `/strategy` - System architecture and design documentation
- `/project-organizer` - Overall project structure optimization
- `/qa-reviewer` - Documentation quality validation

## Integration

The documentation-librarian command works seamlessly with:

**Agent Ecosystem:**
```
/documentation-librarian → documentation-librarian agent
/document → codi-documentation-writer agent
/qa-reviewer → qa-reviewer agent
```

**Workflow Integration:**
```
orchestrator → /documentation-librarian (Phase 1: Analysis)
orchestrator → /documentation-librarian (Phase 2: Organization)
orchestrator → /documentation-librarian (Phase 3: Automation)
```

## Real-World Results

**CODITECT Core Documentation Reorganization (Nov 2025):**

**Before:**
- 138 markdown files
- 57 files in docs/ root (disorganized)
- No navigation systems
- Duplicate content across 12 categories

**Command Used:**
```bash
/documentation-librarian analyze docs for duplicates and create reorganization plan
/documentation-librarian execute approved plan
/documentation-librarian generate README.md for all subdirectories
```

**After:**
- 97 markdown files (-30% reduction)
- 0 files in docs/ root (100% organized)
- README.md in all subdirectories
- Consolidated master documents

**Impact:**
- Time: 7 hours end-to-end
- Maintenance saved: 100+ hours over 12 months
- Token budget: ~50K tokens

## Tips & Best Practices

### Be Specific with Task Descriptions

**Good:**
```bash
/documentation-librarian analyze docs/ for duplicate content and create consolidation plan with similarity scores >60%
```

**Better:**
```bash
/documentation-librarian analyze docs/ for duplicate content, create consolidation plan targeting 30-50% file reduction, generate before/after metrics
```

### Provide Context for Large Reorganizations

**Good:**
```bash
/documentation-librarian reorganize 100+ files from docs root
```

**Better:**
```bash
/documentation-librarian reorganize 100+ files from docs root into 9-category structure (architecture, implementation, planning, reference, etc.) using git mv to preserve history
```

### Combine Multiple Operations

**Instead of:**
```bash
/documentation-librarian analyze docs
/documentation-librarian create plan
/documentation-librarian execute plan
```

**Use:**
```bash
/documentation-librarian analyze docs/, create reorganization plan, and execute approved plan with validation
```

## Troubleshooting

### Issue: Agent not found

**Error:** "Unknown subagent type: documentation-librarian"

**Solution:** Ensure you're using the command in a repository with CODITECT framework installed. The documentation-librarian agent should exist in `.coditect/agents/documentation-librarian.md`

### Issue: Links still broken after validation

**Cause:** Some links use absolute paths or external references

**Solution:**
```bash
/documentation-librarian find all broken links, categorize by type (relative, absolute, external), and fix relative/absolute links
```

### Issue: Too aggressive consolidation

**Cause:** Similarity threshold too low, merging dissimilar content

**Solution:** Specify threshold in command:
```bash
/documentation-librarian consolidate duplicates with >70% similarity threshold
```

## Advanced Usage

### Custom Directory Structures

```bash
/documentation-librarian create custom 5-category documentation structure: (1) getting-started, (2) architecture, (3) api-reference, (4) tutorials, (5) troubleshooting
```

### Targeted Consolidation

```bash
/documentation-librarian consolidate only TOON-related documentation (18 files) into 3 master documents: integration, testing, performance
```

### Automated Quality Gates

```bash
/documentation-librarian create pre-commit hook that validates: (1) no files in docs root, (2) all directories have README.md, (3) no broken links
```

---

**This command is production-ready** - Successfully reorganized CODITECT core documentation in November 2025.
