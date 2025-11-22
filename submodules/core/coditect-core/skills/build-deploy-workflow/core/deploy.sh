#!/bin/bash
# Build-Deploy-Workflow Script
# Automated build, deploy, and documentation for GKE deployments

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Defaults
BUILD_NUM=""
CHANGES=""
TARGET="all"  # all, backend, combined
SKIP_LOCAL_BUILD=false
UPDATE_CHECKLIST=false
DRY_RUN=false
NAMESPACE="coditect-app"
PROJECT="serene-voltage-464305-n2"
REGION="us-central1"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --build-num)
      BUILD_NUM="$2"
      shift 2
      ;;
    --changes)
      CHANGES="$2"
      shift 2
      ;;
    --target)
      TARGET="$2"
      shift 2
      ;;
    --skip-local-build)
      SKIP_LOCAL_BUILD=true
      shift
      ;;
    --update-checklist)
      UPDATE_CHECKLIST=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$BUILD_NUM" ]; then
  echo -e "${RED}Error: --build-num required${NC}"
  exit 1
fi

if [ -z "$CHANGES" ]; then
  echo -e "${RED}Error: --changes required (describe what changed)${NC}"
  exit 1
fi

# Navigate to project root
cd /home/hal/v4/PROJECTS/t2

echo -e "${GREEN}=== Build-Deploy-Workflow ===${NC}"
echo "Build Number: #$BUILD_NUM"
echo "Changes: $CHANGES"
echo "Target: $TARGET"
echo "Dry Run: $DRY_RUN"
echo ""

# Phase 1: Local Verification
verify_local_builds() {
  echo -e "${YELLOW}=== Phase 1: Local Verification ===${NC}"

  if [ "$SKIP_LOCAL_BUILD" = true ]; then
    echo -e "${YELLOW}Skipping local builds (--skip-local-build)${NC}"
    return 0
  fi

  # Backend build
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "backend" ]; then
    echo "Building backend..."
    if ! (cd backend && cargo build --release 2>&1 | tail -5); then
      echo -e "${RED}Backend build failed!${NC}"
      exit 1
    fi
    echo -e "${GREEN}✅ Backend build passed${NC}"
  fi

  # Frontend build
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "combined" ]; then
    echo "Building frontend..."
    if ! npm run build 2>&1 | tail -10; then
      echo -e "${RED}Frontend build failed!${NC}"
      exit 1
    fi
    echo -e "${GREEN}✅ Frontend build passed${NC}"
  fi

  echo ""
}

# Phase 2: Cloud Builds
trigger_cloud_builds() {
  echo -e "${YELLOW}=== Phase 2: Cloud Builds ===${NC}"

  BACKEND_BUILD_ID=""
  COMBINED_BUILD_ID=""
  BACKEND_START_TIME=$(date +%s)
  COMBINED_START_TIME=$(date +%s)

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would trigger Cloud Builds${NC}"
    BACKEND_BUILD_ID="dry-run-backend-id"
    COMBINED_BUILD_ID="dry-run-combined-id"
    return 0
  fi

  # Backend build
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "backend" ]; then
    echo "Triggering backend Cloud Build..."
    BACKEND_OUTPUT=$(gcloud builds submit --config backend/cloudbuild-gke.yaml backend/ 2>&1)
    BACKEND_BUILD_ID=$(echo "$BACKEND_OUTPUT" | grep -oP 'builds/\K[a-f0-9-]+' | tail -1)

    if [ -z "$BACKEND_BUILD_ID" ]; then
      echo -e "${RED}Failed to extract backend build ID!${NC}"
      echo "$BACKEND_OUTPUT"
      exit 1
    fi

    echo "Backend Build ID: $BACKEND_BUILD_ID"
    echo "Waiting for backend build..."
    gcloud builds wait "$BACKEND_BUILD_ID"

    BACKEND_END_TIME=$(date +%s)
    BACKEND_DURATION=$((BACKEND_END_TIME - BACKEND_START_TIME))
    echo -e "${GREEN}✅ Backend build complete (${BACKEND_DURATION}s)${NC}"
  fi

  # Combined build
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "combined" ]; then
    echo "Triggering combined Cloud Build..."
    COMBINED_START_TIME=$(date +%s)
    COMBINED_OUTPUT=$(gcloud builds submit --config cloudbuild-combined.yaml . 2>&1)
    COMBINED_BUILD_ID=$(echo "$COMBINED_OUTPUT" | grep -oP 'builds/\K[a-f0-9-]+' | tail -1)

    if [ -z "$COMBINED_BUILD_ID" ]; then
      echo -e "${RED}Failed to extract combined build ID!${NC}"
      echo "$COMBINED_OUTPUT"
      exit 1
    fi

    echo "Combined Build ID: $COMBINED_BUILD_ID"
    echo "Waiting for combined build..."
    gcloud builds wait "$COMBINED_BUILD_ID"

    COMBINED_END_TIME=$(date +%s)
    COMBINED_DURATION=$((COMBINED_END_TIME - COMBINED_START_TIME))
    echo -e "${GREEN}✅ Combined build complete (${COMBINED_DURATION}s)${NC}"
  fi

  echo ""
}

# Phase 3: GKE Deployment
deploy_to_gke() {
  echo -e "${YELLOW}=== Phase 3: GKE Deployment ===${NC}"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would deploy to GKE${NC}"
    return 0
  fi

  # Backend deployment
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "backend" ]; then
    if [ -n "$BACKEND_BUILD_ID" ]; then
      echo "Deploying backend to GKE..."
      BACKEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT/coditect/coditect-v5-api:$BACKEND_BUILD_ID"

      kubectl set image deployment/coditect-api-v5 \
        api="$BACKEND_IMAGE" \
        -n "$NAMESPACE"

      echo "Waiting for backend rollout..."
      kubectl rollout status deployment/coditect-api-v5 -n "$NAMESPACE" --timeout=300s

      echo -e "${GREEN}✅ Backend deployed successfully${NC}"
    fi
  fi

  # Combined deployment
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "combined" ]; then
    if [ -n "$COMBINED_BUILD_ID" ]; then
      echo "Deploying combined to GKE..."
      COMBINED_IMAGE="$REGION-docker.pkg.dev/$PROJECT/coditect/coditect-combined:$COMBINED_BUILD_ID"

      kubectl set image deployment/coditect-combined \
        combined="$COMBINED_IMAGE" \
        -n "$NAMESPACE"

      echo "Waiting for combined rollout..."
      kubectl rollout status deployment/coditect-combined -n "$NAMESPACE" --timeout=300s

      echo -e "${GREEN}✅ Combined deployed successfully${NC}"
    fi
  fi

  echo ""
}

# Phase 4: Verification
verify_deployment() {
  echo -e "${YELLOW}=== Phase 4: Verification ===${NC}"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would verify deployment${NC}"
    return 0
  fi

  # Check backend pods
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "backend" ]; then
    echo "Checking backend pods..."
    kubectl get pods -n "$NAMESPACE" | grep coditect-api-v5

    BACKEND_READY=$(kubectl get deployment coditect-api-v5 -n "$NAMESPACE" -o jsonpath='{.status.readyReplicas}')
    if [ "$BACKEND_READY" != "3" ]; then
      echo -e "${RED}Backend not ready: $BACKEND_READY/3 pods${NC}"
      exit 1
    fi
    echo -e "${GREEN}✅ Backend: 3/3 pods running${NC}"
  fi

  # Check combined pods
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "combined" ]; then
    echo "Checking combined pods..."
    kubectl get pods -n "$NAMESPACE" | grep coditect-combined

    COMBINED_READY=$(kubectl get deployment coditect-combined -n "$NAMESPACE" -o jsonpath='{.status.readyReplicas}')
    if [ "$COMBINED_READY" != "3" ]; then
      echo -e "${RED}Combined not ready: $COMBINED_READY/3 pods${NC}"
      exit 1
    fi
    echo -e "${GREEN}✅ Combined: 3/3 pods running${NC}"
  fi

  echo ""
}

# Phase 5: Documentation
update_checklist() {
  echo -e "${YELLOW}=== Phase 5: Documentation ===${NC}"

  if [ "$UPDATE_CHECKLIST" = false ]; then
    echo "Skipping checklist update (use --update-checklist to enable)"
    return 0
  fi

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would update checklist${NC}"
    return 0
  fi

  CHECKLIST_FILE="docs/10-execution-plans/PHASED-DEPLOYMENT-CHECKLIST.md"
  CURRENT_DATE=$(date +%Y-%m-%d)

  echo "Updating $CHECKLIST_FILE..."

  # Backend entry
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "backend" ]; then
    cat >> "$CHECKLIST_FILE" <<EOF

- [x] **Build and deploy Backend Build #${BUILD_NUM}** ✅ COMPLETE ($CURRENT_DATE)
  - Build ID: \`${BACKEND_BUILD_ID}\`
  - Build time: ${BACKEND_DURATION}s ($(date -d@${BACKEND_DURATION} -u +%Mm%Ss))
  - Image: \`us-central1-docker.pkg.dev/.../coditect-v5-api:${BACKEND_BUILD_ID}\`
  - Pods: 3/3 running ✅
  - Changes: ${CHANGES}
  - Deployment: Rolled out successfully ✅
EOF
  fi

  # Combined entry
  if [ "$TARGET" = "all" ] || [ "$TARGET" = "combined" ]; then
    cat >> "$CHECKLIST_FILE" <<EOF

- [x] **Build and deploy Combined Build #${BUILD_NUM}** ✅ COMPLETE ($CURRENT_DATE)
  - Build ID: \`${COMBINED_BUILD_ID}\`
  - Build time: ${COMBINED_DURATION}s ($(date -d@${COMBINED_DURATION} -u +%Mm%Ss))
  - Image: \`us-central1-docker.pkg.dev/.../coditect-combined:${COMBINED_BUILD_ID}\`
  - Pods: 3/3 running ✅
  - Changes: ${CHANGES}
  - Deployment: Rolled out successfully ✅
EOF
  fi

  # Git commit
  git add "$CHECKLIST_FILE"
  git commit -m "docs: Add Build #${BUILD_NUM} to deployment checklist

Backend: ${BACKEND_BUILD_ID}
Combined: ${COMBINED_BUILD_ID}
Changes: ${CHANGES}

🎉 Automated deployment via build-deploy-workflow skill"

  git push

  echo -e "${GREEN}✅ Checklist updated and pushed${NC}"
  echo ""
}

# Main execution
main() {
  verify_local_builds
  trigger_cloud_builds
  deploy_to_gke
  verify_deployment
  update_checklist

  echo -e "${GREEN}=== 🎉 Build #${BUILD_NUM} Deployment Complete! ===${NC}"

  if [ "$TARGET" = "all" ]; then
    echo "Backend Build ID: $BACKEND_BUILD_ID"
    echo "Combined Build ID: $COMBINED_BUILD_ID"
  elif [ "$TARGET" = "backend" ]; then
    echo "Backend Build ID: $BACKEND_BUILD_ID"
  elif [ "$TARGET" = "combined" ]; then
    echo "Combined Build ID: $COMBINED_BUILD_ID"
  fi

  echo ""
  echo "Next steps:"
  echo "1. Verify production: https://coditect.ai"
  echo "2. Check API: https://api.coditect.ai/health"
  echo "3. Monitor pods: kubectl get pods -n $NAMESPACE"
}

# Run main
main
