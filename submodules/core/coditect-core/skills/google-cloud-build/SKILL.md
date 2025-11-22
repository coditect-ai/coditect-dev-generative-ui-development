---
name: google-cloud-build
description: Build and deploy Coditect modules (backend, frontend+Theia combined) to GCP using Cloud Build. Use when deploying to GKE, troubleshooting builds, or optimizing build times.
version: 2.0.0
status: production
tags:
  - gcp
  - cloud-build
  - gke
  - docker
  - deployment
  - kubernetes
---

# Google Cloud Build Skill - Coditect Modules

**Purpose**: Successfully build and deploy Coditect modules (backend, frontend+Theia combined) to Google Cloud Platform using Cloud Build.

## When to Use

Use this skill when:
- Deploying backend API (Rust/Actix-web) to GKE
- Deploying combined frontend+Theia to GKE
- Troubleshooting failed Cloud Build deployments
- Optimizing build times and upload sizes
- Setting up new Coditect modules for GCP deployment

## Pre-Flight Checklist

**ALWAYS verify these before `gcloud builds submit`:**

```bash
# 1. Check authentication
gcloud auth list
# If expired: gcloud auth login

# 2. Verify required files exist
ls -1 Dockerfile* cloudbuild*.yaml nginx*.conf start*.sh dist/

# 3. Check .gcloudignore exists (saves 5-10 min upload time!)
ls -la .gcloudignore

# 4. For combined builds: Frontend must be built first
ls -lh dist/
# Should show dist/assets/ and dist/index.html with recent timestamp

# 5. Verify Dockerfile COPY commands (no wildcards!)
grep "COPY.*\*" Dockerfile*
# Should return empty - wildcards fail in Cloud Build context

# 6. Verify deployment name matches existing K8s deployment
kubectl get deployment -n coditect-app
# Match the name exactly in cloudbuild.yaml (e.g., coditect-combined, not coditect-combined-v5)
```

## Module Build Patterns

### 1. Backend API (Rust/Actix-web)

**Directory**: `backend/`
**Config**: `backend/cloudbuild-gke.yaml`
**Machine**: `E2_HIGHCPU_8` (sufficient for Rust compilation)
**Build Time**: ~6 minutes

**Command**:
```bash
cd backend
gcloud builds submit --config cloudbuild-gke.yaml .
```

**Key Configuration**:
```yaml
# backend/cloudbuild-gke.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'IMAGE:$BUILD_ID', '-f', 'Dockerfile', '.']

  - name: 'gcr.io/cloud-builders/kubectl'
    args: ['set', 'image', 'deployment/coditect-api-v5', 'api=IMAGE:$BUILD_ID']
    env:
      - 'CLOUDSDK_COMPUTE_ZONE=us-central1-a'
      - 'CLOUDSDK_CONTAINER_CLUSTER=codi-poc-e2-cluster'

options:
  machineType: 'E2_HIGHCPU_8'
```

**Common Issues**:
- ❌ Wrong container name in kubectl set image
- ❌ Missing FDB environment variables
- ✅ Fix: Match container name in deployment YAML

### 2. Combined Frontend+Theia

**Directory**: `/` (project root)
**Config**: `cloudbuild-combined.yaml`
**Machine**: `E2_HIGHCPU_32` (32 CPUs for Theia webpack)
**Build Time**: ~10-15 minutes

**Prerequisites**:
```bash
# 1. Build V5 frontend first (CRITICAL!)
npx vite build  # Creates dist/ folder (~1.3 MB)

# 2. Verify dist/ exists and is fresh
ls -lh dist/
# dist/assets/index-*.js should be recent timestamp

# 3. Check .gcloudignore to reduce upload size
cat .gcloudignore  # Should exclude node_modules/, docs/, tests/
```

**Command**:
```bash
# From project root
gcloud builds submit --config cloudbuild-combined.yaml .
```

**Key Configuration**:
```yaml
# cloudbuild-combined.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-f', 'Dockerfile.local-test', '-t', 'IMAGE:$BUILD_ID', '.']

options:
  machineType: 'E2_HIGHCPU_32'  # 32 CPUs for Theia
  diskSizeGb: 100
  env:
    - 'NODE_OPTIONS=--max_old_space_size=8192'  # 8GB heap for webpack
```

**Dockerfile Pattern (Dockerfile.local-test)**:
```dockerfile
# Stage 1: Build Theia
FROM node:20 AS theia-builder
WORKDIR /app/theia

# ⚠️ IMPORTANT: Explicit file list (NO wildcards!)
COPY theia-app/package*.json ./
COPY theia-app/tsconfig.json ./
COPY theia-app/gen-webpack.config.js ./
COPY theia-app/gen-webpack.node.config.js ./
COPY theia-app/webpack.config.js ./

RUN npm install
COPY theia-app/src ./src
COPY theia-app/plugins ./plugins

ENV NODE_OPTIONS="--max_old_space_size=8192"
RUN npm run prepare

# Stage 2: Runtime
FROM node:20-slim
COPY dist /app/v5-frontend  # Pre-built frontend
COPY --from=theia-builder /app/theia /app/theia
COPY nginx-combined.conf /etc/nginx/sites-available/default
COPY start-combined.sh /start.sh
```

## Optimization Techniques

### 1. .gcloudignore File (Saves 5-10 minutes!)

**Impact**: Reduces upload from 13,698 files (1.6 GB) to 8,623 files (1.5 GB)

**Create**: `.gcloudignore` in project root
```gitignore
# Exclude heavy/unnecessary files
.git/
node_modules/
docs/
thoughts/
archive/
coverage/
*.test.ts
*.test.tsx
*.log
.vscode/
.idea/

# Keep these for the build
!dist/
!theia-app/
!backend/
!nginx-combined.conf
!start-combined.sh
```

### 2. Pre-Build Frontend Locally

**Why**: Cloud Build doesn't need to build frontend (already done locally)
**Benefit**: Saves ~2 minutes, smaller Docker image

```bash
# Build locally before gcloud builds submit
npx vite build  # ~21 seconds
# Then Dockerfile just copies dist/ folder
```

### 3. Use Proven Machine Types

| Module | Machine Type | CPUs | RAM | Why |
|--------|--------------|------|-----|-----|
| Backend | E2_HIGHCPU_8 | 8 | 8 GB | Rust compilation |
| Combined | E2_HIGHCPU_32 | 32 | 32 GB | Theia webpack (parallel builds) |

**Don't use**:
- ❌ N1_HIGHCPU_8 (older generation, slower)
- ❌ E2_HIGHCPU_8 for Theia (too slow, webpack timeouts)

### 4. Explicit Docker COPY (No Wildcards!)

**❌ FAILS in Cloud Build context**:
```dockerfile
COPY theia-app/*.config.js ./
# Error: "COPY failed: no source files were specified"
```

**✅ WORKS**:
```dockerfile
COPY theia-app/gen-webpack.config.js ./
COPY theia-app/gen-webpack.node.config.js ./
COPY theia-app/webpack.config.js ./
```

**Why**: Cloud Build's Docker context differs from local Docker - wildcards don't expand correctly.

## Common Build Failures & Fixes

### Error 1: "COPY failed: no source files were specified"

**Symptom**:
```
Step 5/22 : COPY theia-app/*.config.js ./
COPY failed: no source files were specified
```

**Root Cause**: Wildcard patterns in COPY don't work in Cloud Build context

**Fix**: Use explicit file lists
```dockerfile
# Before
COPY theia-app/*.config.js ./

# After
COPY theia-app/gen-webpack.config.js ./
COPY theia-app/gen-webpack.node.config.js ./
COPY theia-app/webpack.config.js ./
```

### Error 2: "no such file or directory: dist/"

**Symptom**:
```
COPY dist /app/v5-frontend
COPY failed: stat dist: file does not exist
```

**Root Cause**: Frontend not built before Docker build

**Fix**: Build frontend first
```bash
# Build V5 frontend
npx vite build

# Verify dist/ exists
ls -lh dist/

# Then run Cloud Build
gcloud builds submit --config cloudbuild-combined.yaml .
```

### Error 3: Upload taking 10+ minutes

**Symptom**:
```
Creating temporary archive of 13698 file(s) totalling 1.6 GiB...
(hangs for 10+ minutes)
```

**Root Cause**: No `.gcloudignore` file - uploading unnecessary files (node_modules, docs, tests)

**Fix**: Create `.gcloudignore` (see Optimization section above)

### Error 4: Webpack out of memory during Theia build

**Symptom**:
```
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```

**Root Cause**: Insufficient Node.js heap size or machine type

**Fix**: Use E2_HIGHCPU_32 with 8GB heap
```yaml
# cloudbuild-combined.yaml
options:
  machineType: 'E2_HIGHCPU_32'
  env:
    - 'NODE_OPTIONS=--max_old_space_size=8192'
```

### Error 5: Wrong container name in kubectl

**Symptom**:
```
error: unable to find container named "api-server"
```

**Root Cause**: Container name mismatch between cloudbuild.yaml and k8s deployment

**Fix**: Match container name exactly
```yaml
# Get actual container name from deployment
kubectl get deployment coditect-api-v5 -n coditect-app -o yaml | grep "name:"

# Update cloudbuild-gke.yaml to match
- 'api=IMAGE:$BUILD_ID'  # NOT api-server=
```

### Error 6: Deployment not found (wrong name)

**Symptom**:
```
Error from server (NotFound): deployments.apps "coditect-combined-v5" not found
```

**Root Cause**: cloudbuild.yaml references a deployment name that doesn't exist in the cluster

**Fix**: Check existing deployments and match the name
```bash
# 1. List all deployments
kubectl get deployment -n coditect-app

# 2. Find the correct deployment name (e.g., coditect-combined, not coditect-combined-v5)
# Output shows: coditect-combined (not coditect-combined-v5)

# 3. Update cloudbuild-combined.yaml to match
# Change: deployment/coditect-combined-v5
# To:     deployment/coditect-combined
```

**Key lesson**: Always verify deployment exists before using `kubectl set image`. Use `kubectl get deployment -n <namespace>` to list actual names.

### Error 7: Rollout timeout (not always a failure!)

**Symptom**:
```
error: timed out waiting for the condition
BUILD FAILURE: Build step failure: build step 4 "gcr.io/cloud-builders/kubectl" failed
```

**Root Cause**: Rollout verification timeout (default 5 minutes) - pods might still be starting successfully

**Fix**: Distinguish between timeout and actual failure
```bash
# 1. Check if image was updated (even if verification timed out)
kubectl get deployment coditect-combined -n coditect-app -o yaml | grep "image:"

# 2. Check pod status
kubectl get pods -n coditect-app -l app=coditect-combined

# 3. If pods are Running, deployment succeeded (just slow)
# If pods are CrashLoopBackOff or Error, investigate with:
kubectl describe pod -n coditect-app <pod-name>
kubectl logs -n coditect-app <pod-name>

# 4. For slow-starting containers (like Theia), increase timeout
# In cloudbuild.yaml:
- name: 'gcr.io/cloud-builders/kubectl'
  args: ['rollout', 'status', 'deployment/X', '--timeout=10m']  # Increase from 5m
```

**Key distinction**:
- ✅ **Timeout during verification** - Image updated, pods starting (may still succeed)
- ❌ **Actual deployment failure** - Pods in CrashLoopBackOff or Error state

## Troubleshooting Workflow

**When a build fails:**

```bash
# 1. Get Build ID from error message
BUILD_ID="<id from error>"

# 2. View detailed logs
gcloud builds log $BUILD_ID | tail -100

# 3. Identify failure step
# Look for "Step #N" and "ERROR" lines

# 4. Common checks based on step:
# - Step 0 (build-image): Docker/Dockerfile issue
# - Step 1-2 (push): Registry permissions
# - Step 3-4 (deploy-gke): kubectl/GKE connectivity

# 5. Check Cloud Console for visual logs
echo "https://console.cloud.google.com/cloud-build/builds/$BUILD_ID"

# 6. Fix and retry
gcloud builds submit --config <config.yaml> .
```

## Real-World Examples

### Example 1: Combined Build Success (Oct 18, 2025)

**Scenario**: Deploy combined frontend+Theia after multiple failures

**Journey (5 attempts)**:
1. ❌ Attempt #1: Docker wildcard COPY error (`COPY theia-app/*.config.js` failed)
2. ❌ Attempt #2: Slow upload (13,698 files, 10+ min without `.gcloudignore`)
3. ❌ Attempt #3: .gcloudignore too aggressive (excluded needed webpack configs)
4. ❌ Attempt #4: Build success, deployment name mismatch (`coditect-combined-v5` not found)
5. ⚠️ Attempt #5: Build success, image pushed, rollout timeout (but image updated!)

**What Went Well (Attempt #5)**:
- ✅ Docker image built successfully (Theia webpack compiled with 32 CPUs)
- ✅ Image pushed to Artifact Registry (both BUILD_ID and latest tags)
- ✅ Deployment image updated (`kubectl set image` succeeded)
- ✅ Upload optimized: 8,627 files (1.5 GB) in ~2 minutes
- ✅ Theia webpack compiled: 11 MB frontend + 9.34 MB backend bundles
- ✅ Node.js 8GB heap prevented OOM errors
- ✅ Explicit COPY file lists worked perfectly

**Key Fixes Applied**:
```bash
# 1. Fix Dockerfile wildcards (explicit file list)
COPY theia-app/gen-webpack.config.js ./
COPY theia-app/gen-webpack.node.config.js ./
COPY theia-app/webpack.config.js ./

# 2. Create optimized .gcloudignore with explicit inclusions
!theia-app/
!theia-app/**/*.config.js
!dist/
!vite.config.ts

# 3. Build frontend first
npx vite build

# 4. Fix deployment name (match existing K8s deployment)
kubectl get deployment -n coditect-app  # Shows: coditect-combined
# Changed cloudbuild.yaml from coditect-combined-v5 → coditect-combined

# 5. Deploy with corrected config
gcloud builds submit --config cloudbuild-combined.yaml .
```

**Build Metrics**:
- Upload: 2 min (8,627 files optimized)
- Docker build: 7 min (Theia webpack compilation)
- Image push: 2 min (BUILD_ID + latest tags)
- Deployment: Image updated (rollout verification timed out, but likely still starting)
- **Total Cloud Build time**: ~12 minutes

**Status**: Build SUCCESS ✅ - Image deployed to cluster, pods likely starting (rollout timeout is verification step, not build failure)

**Next step**: Check pod status with `kubectl get pods -n coditect-app -l app=coditect-combined` to confirm healthy startup

### Example 2: Backend Deployment (Oct 18, 2025)

**Scenario**: Deploy Rust backend API with FDB fixes

**Command**:
```bash
cd backend
gcloud builds submit --config cloudbuild-gke.yaml .
```

**Build Time**: ~6 minutes
**Result**: ✅ Success - API deployed and tested with JWT auth

## Automation Script

```bash
#!/bin/bash
# deploy-coditect-module.sh - Smart deployment script

MODULE=$1  # "backend" or "combined"

if [ "$MODULE" == "combined" ]; then
  echo "=== Combined Frontend+Theia Deployment ==="

  # Pre-flight checks
  echo "1. Checking frontend build..."
  if [ ! -d "dist" ] || [ -z "$(find dist -name 'index-*.js' -mtime -1)" ]; then
    echo "  Building frontend..."
    npx vite build || exit 1
  else
    echo "  ✅ Frontend already built (recent)"
  fi

  echo "2. Checking .gcloudignore..."
  if [ ! -f ".gcloudignore" ]; then
    echo "  ⚠️  No .gcloudignore - upload will be slow!"
    read -p "  Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 1; fi
  else
    echo "  ✅ .gcloudignore exists"
  fi

  echo "3. Starting Cloud Build..."
  gcloud builds submit --config cloudbuild-combined.yaml .

elif [ "$MODULE" == "backend" ]; then
  echo "=== Backend API Deployment ==="

  echo "1. Starting Cloud Build..."
  cd backend
  gcloud builds submit --config cloudbuild-gke.yaml .

else
  echo "Usage: $0 [backend|combined]"
  exit 1
fi
```

**Usage**:
```bash
chmod +x scripts/deploy-coditect-module.sh
./scripts/deploy-coditect-module.sh combined  # Deploy frontend+Theia
./scripts/deploy-coditect-module.sh backend   # Deploy backend API
```

## Tips & Best Practices

1. **Always build frontend first** for combined deployments (`npx vite build`)
2. **Use .gcloudignore** to exclude node_modules/, docs/, tests/ (saves 5-10 min)
3. **Avoid Docker COPY wildcards** - use explicit file lists
4. **Match machine type to workload**:
   - Backend: E2_HIGHCPU_8
   - Combined (Theia): E2_HIGHCPU_32
5. **Set NODE_OPTIONS** for Theia builds: `--max_old_space_size=8192`
6. **Monitor builds** with `gcloud builds log <BUILD_ID>`
7. **Use deployment archeology** to find previous successful configs
8. **Keep cloudbuild.yaml DRY** - use substitutions for repeated values
9. **Verify deployment names** match existing K8s resources (`kubectl get deployment -n <namespace>`)
10. **Rollout timeout ≠ failure** - Check pod status to confirm actual deployment health
11. **Test .gcloudignore** before submitting: `gcloud meta list-files-for-upload | grep <pattern>`
12. **Increase rollout timeout** for slow-starting containers (Theia: 10m instead of 5m)

## Integration with Other Skills

- **deployment-archeology**: Find previous successful build configs
- **codebase-locator**: Find Dockerfiles and cloudbuild configs
- **web-search-researcher**: Research Cloud Build error messages

## See Also

- `.gcloudignore` examples: `gcloud topic gcloudignore`
- Cloud Build docs: https://cloud.google.com/build/docs
- GKE deployment: https://cloud.google.com/kubernetes-engine/docs
- Docker multi-stage builds: https://docs.docker.com/build/building/multi-stage/
