---
name: deployment-archeology
description: Find and restore previous successful deployment configurations by analyzing git history, Cloud Build logs, and Kubernetes deployments. Use when investigating deployment regressions or recovering from configuration changes.
version: 2.0.0
status: production
tags:
  - deployment
  - gcp
  - kubernetes
  - cloud-build
  - recovery
  - git-history
---

# Deployment Archeology Skill

**Purpose**: Find and restore previous successful deployment configurations by analyzing git history, Cloud Build logs, and Kubernetes deployments.

## When to Use

Use this skill when:
- Current deployment failing and need to find what worked before
- Need to understand how a service was originally deployed
- Investigating deployment regressions
- Recovering from accidental configuration changes

## Process

### Step 1: Identify Current Deployment Date
```bash
# Get deployment creation timestamp from Kubernetes
kubectl get deployment <DEPLOYMENT_NAME> -n <NAMESPACE> -o jsonpath='{.metadata.creationTimestamp}'
```

### Step 2: Search Cloud Build History
```bash
# List builds around the deployment date
gcloud builds list \
  --filter="createTime>='YYYY-MM-DDT00:00:00Z' AND createTime<='YYYY-MM-DDT23:59:59Z'" \
  --format="table(id,status,createTime)" \
  --limit=50
```

### Step 3: Analyze Successful Build
```bash
# Get build configuration from successful build closest to deployment time
gcloud builds describe <BUILD_ID> --format="yaml(steps,substitutions,options)"
```

Key things to extract:
- Dockerfile name (check `args` for `-f` flag)
- Machine type (`options.machineType`)
- Environment variables (`options.env`)
- Build steps and deployment method

### Step 4: Search Git History
```bash
# Find commits around deployment date
git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --oneline --all

# Check if files were archived
git log --all --full-history -- <FILENAME>
```

### Step 5: Restore Configuration
```bash
# Find archived files
find . -name "<FILENAME>" -type f

# Check git history for file content at specific date
git show <COMMIT>:<PATH>

# Restore from archive directory if needed
cp docs/99-archive/deployment-obsolete/<FILE> ./<FILE>
```

## Example: Combined Service Recovery (Oct 18, 2025)

**Problem**: Dockerfile.combined failing to build

**Investigation**:
1. Found deployment created: `2025-10-13T09:58:29Z`
2. Found successful build: `6e95a4d9-2f19-456c-bba8-5a1ed7a8fdf7` at `09:50:07Z`
3. Build used: `Dockerfile.local-test` (not Dockerfile.combined!)
4. Machine: `E2_HIGHCPU_32` with `NODE_OPTIONS=--max_old_space_size=8192`
5. File archived in commit `04ef4b4` to `docs/99-archive/deployment-obsolete/`

**Recovery**:
```bash
# Restore working Dockerfile
cp docs/99-archive/deployment-obsolete/Dockerfile.local-test ./

# Update cloudbuild config
# Change: Dockerfile.combined -> Dockerfile.local-test
# Change: N1_HIGHCPU_8 -> E2_HIGHCPU_32
# Add: NODE_OPTIONS=--max_old_space_size=8192

# Rebuild with proven config
gcloud builds submit --config cloudbuild-combined.yaml .
```

## Automation Script

```bash
#!/bin/bash
# deployment-archeology.sh - Find previous successful build config

DEPLOYMENT=$1
NAMESPACE=${2:-default}

echo "=== Deployment Archeology ==="

# Step 1: Get deployment date
DEPLOY_DATE=$(kubectl get deployment $DEPLOYMENT -n $NAMESPACE -o jsonpath='{.metadata.creationTimestamp}')
SEARCH_DATE=$(date -d $DEPLOY_DATE '+%Y-%m-%d')

echo "Deployment created: $DEPLOY_DATE"
echo "Searching builds on: $SEARCH_DATE"

# Step 2: Find builds on that date
echo ""
echo "=== Cloud Build History ==="
gcloud builds list \
  --filter="createTime>='${SEARCH_DATE}T00:00:00Z' AND createTime<='${SEARCH_DATE}T23:59:59Z'" \
  --format="table(id,status,createTime)" \
  --limit=20

# Step 3: Show git commits around that date
echo ""
echo "=== Git History ==="
git log --since="$SEARCH_DATE" --until="$(date -d "$SEARCH_DATE + 1 day" '+%Y-%m-%d')" --oneline --all | head -20

echo ""
echo "Next steps:"
echo "1. Identify successful build ID (STATUS=SUCCESS)"
echo "2. Run: gcloud builds describe <BUILD_ID> --format='yaml(steps,options)'"
echo "3. Check for archived files: find . -name 'Dockerfile*' | grep archive"
echo "4. Compare current config vs successful build config"
```

## Tips

1. **Look for BUILD_ID vs SHORT_SHA**: Manual builds use `$BUILD_ID`, git triggers use `$SHORT_SHA`
2. **Check machine type**: Theia builds need high CPU (E2_HIGHCPU_32)
3. **Node memory**: Webpack builds often need 8GB+ heap (`NODE_OPTIONS=--max_old_space_size=8192`)
4. **Archive directories**: Check `docs/99-archive/` and `archive/` for old configs
5. **Git submodules**: May contain reference implementations

## Common Gotchas

- ❌ Assuming current files match deployed version
- ❌ Not checking environment variables in Cloud Build options
- ❌ Forgetting to check for archived/moved files
- ❌ Using wrong Dockerfile (may have multiple variants)
- ❌ Missing build prerequisites (like pre-built `dist/` directory)

## Integration with Other Skills

- **codebase-locator**: Find all Dockerfile variants
- **thoughts-locator**: Find deployment session exports
- **web-search-researcher**: Research Cloud Build error messages
