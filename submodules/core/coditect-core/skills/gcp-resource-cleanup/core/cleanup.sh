#!/bin/bash
# GCP Resource Cleanup Script
# Automated cleanup with safety checks and cost tracking

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Defaults
DRY_RUN=false
TARGET=""
NAMESPACE="coditect-app"
REGION="us-central1"
AGE_DAYS=7
KEEP_COUNT=5
FORCE_AGE_CHECK=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --target)
      TARGET="$2"
      shift 2
      ;;
    --name)
      RESOURCE_NAME="$2"
      shift 2
      ;;
    --namespace)
      NAMESPACE="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --age-days)
      AGE_DAYS="$2"
      shift 2
      ;;
    --keep-count)
      KEEP_COUNT="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --force-age-check)
      FORCE_AGE_CHECK=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Check resource age (safety check)
check_age() {
  local resource_date=$1
  local min_age_seconds=$((AGE_DAYS * 86400))

  if [ -z "$resource_date" ]; then
    echo -e "${RED}Error: Could not determine resource age${NC}"
    return 1
  fi

  local resource_timestamp=$(date -d "$resource_date" +%s 2>/dev/null || echo "0")
  local current_timestamp=$(date +%s)
  local age_seconds=$((current_timestamp - resource_timestamp))

  if [ $age_seconds -lt $min_age_seconds ] && [ "$FORCE_AGE_CHECK" = false ]; then
    echo -e "${YELLOW}Warning: Resource is only $((age_seconds / 86400)) days old (< ${AGE_DAYS} days)${NC}"
    echo -e "${RED}Skipping for safety. Use --force-age-check to override.${NC}"
    return 1
  fi

  return 0
}

# Check if resource is referenced in ingress
check_ingress_references() {
  local resource_name=$1
  local namespace=$2

  if kubectl get ingress -n "$namespace" -o yaml 2>/dev/null | grep -q "$resource_name"; then
    echo -e "${RED}Error: Resource is referenced in active ingress!${NC}"
    echo "Run: kubectl get ingress -n $namespace -o yaml | grep $resource_name"
    return 1
  fi

  return 0
}

# Create backup manifest
create_backup_manifest() {
  local resource_type=$1
  local resource_name=$2
  local namespace=$3
  local backup_dir=".coditect/backups/$(date +%Y-%m-%d)"

  mkdir -p "$backup_dir"

  if [ -n "$namespace" ]; then
    kubectl get "$resource_type" "$resource_name" -n "$namespace" -o yaml > "$backup_dir/${resource_name}.yaml" 2>/dev/null || true
    echo -e "${GREEN}✓ Backup saved: $backup_dir/${resource_name}.yaml${NC}"
  fi
}

# Cleanup GKE deployment
cleanup_gke_deployment() {
  local deployment_name=$1
  local namespace=$2

  echo -e "\n${YELLOW}=== Cleaning up GKE deployment: $deployment_name ===${NC}"

  # Check if deployment exists
  if ! kubectl get deployment "$deployment_name" -n "$namespace" &>/dev/null; then
    echo -e "${YELLOW}Deployment $deployment_name not found in namespace $namespace${NC}"
    return 0
  fi

  # Get deployment age
  local created_at=$(kubectl get deployment "$deployment_name" -n "$namespace" -o jsonpath='{.metadata.creationTimestamp}')
  echo "Deployment created: $created_at"

  # Safety check: Age
  if ! check_age "$created_at"; then
    return 1
  fi

  # Safety check: Ingress references
  if ! check_ingress_references "$deployment_name" "$namespace"; then
    return 1
  fi

  # Get pod count
  local pod_count=$(kubectl get deployment "$deployment_name" -n "$namespace" -o jsonpath='{.spec.replicas}')
  echo "Pod count: $pod_count"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would delete:${NC}"
    echo "  - Deployment: $deployment_name"
    echo "  - Service: $deployment_name (if exists)"
    echo "  - ConfigMaps/Secrets: (dependent resources)"
    echo "  - Freed resources: $pod_count pods"
    return 0
  fi

  # Create backup
  create_backup_manifest "deployment" "$deployment_name" "$namespace"

  # Delete deployment
  echo -e "${GREEN}Deleting deployment...${NC}"
  kubectl delete deployment "$deployment_name" -n "$namespace"

  # Delete service (if exists)
  if kubectl get service "$deployment_name" -n "$namespace" &>/dev/null; then
    echo -e "${GREEN}Deleting service...${NC}"
    kubectl delete service "$deployment_name" -n "$namespace"
  fi

  echo -e "${GREEN}✅ Cleanup complete for $deployment_name${NC}"
}

# Cleanup orphaned Cloud Run services
cleanup_cloud_run_orphans() {
  echo -e "\n${YELLOW}=== Scanning for orphaned Cloud Run services ===${NC}"

  # Get all Cloud Run services
  local services=$(gcloud run services list --region="$REGION" --format='value(name)' 2>/dev/null)

  if [ -z "$services" ]; then
    echo "No Cloud Run services found in region $REGION"
    return 0
  fi

  local orphan_count=0
  local total_cost=0

  for service in $services; do
    echo -e "\nChecking: ${YELLOW}$service${NC}"

    # Get service details
    local created_at=$(gcloud run services describe "$service" --region="$REGION" --format='value(metadata.creationTimestamp)' 2>/dev/null)
    local url=$(gcloud run services describe "$service" --region="$REGION" --format='value(status.url)' 2>/dev/null)

    echo "  Created: $created_at"
    echo "  URL: $url"

    # Check if referenced in GKE ingress
    local ingress_count=$(kubectl get ingress --all-namespaces -o yaml 2>/dev/null | grep -c "$service" || echo "0")

    if [ "$ingress_count" -eq 0 ]; then
      echo -e "  ${RED}Status: ORPHAN (no ingress references)${NC}"
      orphan_count=$((orphan_count + 1))

      # Estimate cost (rough: $5-10/month per idle service)
      local age_days=$(( ($(date +%s) - $(date -d "$created_at" +%s)) / 86400 ))
      local est_cost=5
      if [ $age_days -gt 30 ]; then
        est_cost=8
      fi
      total_cost=$((total_cost + est_cost))

      echo "  Estimated cost: ~\$${est_cost}/month"

      if [ "$DRY_RUN" = true ]; then
        echo -e "  ${YELLOW}[DRY RUN] Would delete${NC}"
      else
        # Delete Cloud Run service
        echo -e "  ${GREEN}Deleting...${NC}"
        gcloud run services delete "$service" --region="$REGION" --quiet
        echo -e "  ${GREEN}✅ Deleted${NC}"
      fi
    else
      echo -e "  ${GREEN}Status: ACTIVE (referenced in $ingress_count ingress)${NC}"
    fi
  done

  echo -e "\n${YELLOW}=== Summary ===${NC}"
  echo "Orphaned services: $orphan_count"
  echo "Estimated monthly savings: ~\$${total_cost}"
}

# Cleanup old Artifact Registry images
cleanup_old_images() {
  echo -e "\n${YELLOW}=== Cleaning up old Artifact Registry images ===${NC}"
  echo "Age threshold: > $AGE_DAYS days"
  echo "Keep count: $KEEP_COUNT latest per package"

  # Get all packages
  local packages=$(gcloud artifacts docker images list --format='value(package)' 2>/dev/null | sort -u)

  for package in $packages; do
    echo -e "\nPackage: ${YELLOW}$package${NC}"

    # Get all images for this package
    local images=$(gcloud artifacts docker images list "$package" --format='value(createTime,image)' --sort-by='~createTime' 2>/dev/null)
    local image_count=0

    while IFS= read -r line; do
      image_count=$((image_count + 1))
      local created_at=$(echo "$line" | awk '{print $1}')
      local image=$(echo "$line" | awk '{print $2}')

      # Keep first KEEP_COUNT images
      if [ $image_count -le $KEEP_COUNT ]; then
        echo "  ✓ Keep: $image (position $image_count)"
        continue
      fi

      # Check age
      local age_seconds=$(( $(date +%s) - $(date -d "$created_at" +%s) ))
      local age_days=$((age_seconds / 86400))

      if [ $age_days -gt $AGE_DAYS ]; then
        echo -e "  ${RED}Delete: $image (${age_days}d old)${NC}"

        if [ "$DRY_RUN" = false ]; then
          gcloud artifacts docker images delete "$image" --quiet
        fi
      else
        echo "  ✓ Keep: $image (${age_days}d old, under threshold)"
      fi
    done <<< "$images"
  done
}

# Main execution
main() {
  echo -e "${GREEN}=== GCP Resource Cleanup ===${NC}"
  echo "Target: $TARGET"
  echo "Namespace: $NAMESPACE"
  echo "Region: $REGION"
  echo "Dry Run: $DRY_RUN"
  echo ""

  case $TARGET in
    gke-api)
      if [ -z "$RESOURCE_NAME" ]; then
        echo -e "${RED}Error: --name required for gke-api target${NC}"
        exit 1
      fi
      cleanup_gke_deployment "$RESOURCE_NAME" "$NAMESPACE"
      ;;
    cloud-run-orphans)
      cleanup_cloud_run_orphans
      ;;
    images)
      cleanup_old_images
      ;;
    *)
      echo -e "${RED}Error: Invalid target. Use: gke-api, cloud-run-orphans, or images${NC}"
      exit 1
      ;;
  esac

  echo -e "\n${GREEN}✅ Cleanup complete!${NC}"
}

# Run main
main
