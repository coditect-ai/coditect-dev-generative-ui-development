# Documentation Librarian Skill - Quick Start

Transform scattered documentation into organized, navigable systems in minutes.

## What This Skill Does

**documentation-librarian** is a production-ready skill that:
- ✅ Organizes 20-100+ documentation files into logical directory structures
- ✅ Generates README.md and CLAUDE.md navigation files automatically
- ✅ Consolidates duplicate content (typically 30-50% file reduction)
- ✅ Validates and fixes cross-references after reorganizations
- ✅ Creates automation for ongoing documentation quality

## Quick Start (3 Steps)

### 1. Analyze Current Documentation

```bash
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to analyze docs/ directory and create reorganization plan"
)
```

**You get:**
- Complete inventory of all markdown files
- Categorization by audience and purpose
- Duplicate content identification
- Consolidation recommendations

### 2. Execute Reorganization

```bash
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to reorganize documentation following the approved plan"
)
```

**You get:**
- Files moved to proper subdirectories (git history preserved)
- Duplicate content consolidated into master documents
- README.md generated for each directory
- All cross-references validated and fixed

### 3. Set Up Automation (Optional)

```bash
Task(
    subagent_type="general-purpose",
    prompt="Use documentation-librarian subagent to create automated link validation and freshness monitoring"
)
```

**You get:**
- Python script for link validation
- Freshness monitoring system
- Auto-generated documentation index
- Git hooks for documentation quality

## Real Results

**CODITECT Core Documentation (Nov 2025)**
- Before: 138 files, 57 in docs root, no navigation
- After: 97 files (-30%), 0 in root, complete navigation
- Time: 7 hours end-to-end
- Maintenance saved: 100+ hours over 12 months

## Common Use Cases

### 1. Messy Documentation Root
**Problem:** 50+ files scattered in docs/ root with no organization

**Solution:**
```bash
Task(subagent_type="general-purpose",
     prompt="Use documentation-librarian subagent to move all files from docs root into proper subdirectories")
```

### 2. Duplicate Content
**Problem:** Multiple files covering same topics, creating confusion

**Solution:**
```bash
Task(subagent_type="general-purpose",
     prompt="Use documentation-librarian subagent to identify and consolidate duplicate content")
```

### 3. Broken Links After Reorganization
**Problem:** Links broken after moving files between directories

**Solution:**
```bash
Task(subagent_type="general-purpose",
     prompt="Use documentation-librarian subagent to validate and fix all cross-references")
```

### 4. Missing Navigation
**Problem:** No README.md files, users can't find documentation

**Solution:**
```bash
Task(subagent_type="general-purpose",
     prompt="Use documentation-librarian subagent to generate README.md for all subdirectories")
```

## When to Use This Skill

✅ **Use documentation-librarian when:**
- You have 20+ documentation files scattered across directories
- Documentation has grown organically without structure
- You need to consolidate duplicate or overlapping content
- Links are broken after reorganizations
- You're setting up a new documentation system

❌ **Don't use documentation-librarian when:**
- Writing new documentation content (use codi-documentation-writer)
- Single-file quick edits (use Edit tool directly)
- Generating API documentation (use codi-documentation-writer)

## Integration with Other Skills

Works seamlessly with:
- **code-editor** - For multi-file code organization
- **build-deploy-workflow** - For documentation deployment
- **git-workflow-automation** - For automated documentation commits

## Documentation

- **Full Documentation:** [SKILL.md](SKILL.md)
- **Agent Documentation:** [../../agents/documentation-librarian.md](../../agents/documentation-librarian.md)
- **Command Reference:** [../../commands/documentation-librarian.md](../../commands/documentation-librarian.md)
- **Standards:** [../../docs/04-implementation-guides/standards/CODITECT-COMPONENT-CREATION-STANDARDS.md](../../docs/04-implementation-guides/standards/CODITECT-COMPONENT-CREATION-STANDARDS.md)

## Token Budget

| Task Size | Files | Estimated Tokens | Time Saved |
|-----------|-------|------------------|------------|
| Small | 10-20 | 15K-25K | 5-10 hours |
| Medium | 20-50 | 30K-50K | 20-40 hours |
| Large | 50-100 | 60K-100K | 50-100 hours |

**ROI:** 10x token efficiency through reusable templates and batch operations

## Support

For issues or questions:
1. Check [SKILL.md](SKILL.md) for detailed documentation
2. Review [agent documentation](../../agents/documentation-librarian.md)
3. See [CODITECT standards](../../docs/04-implementation-guides/standards/)

---

**Production-proven** - Successfully reorganized CODITECT core documentation in November 2025.
