#!/bin/bash
################################################################################
# CODITECT Submodule Update Automation Script
#
# Purpose: Systematically update all 19 submodules in dependency-aware order
# Author: AZ1.AI CODITECT Team
# Version: 1.0
# Date: 2025-11-16
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MASTER_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Log file
LOG_FILE="$MASTER_DIR/logs/submodule-updates-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$MASTER_DIR/logs"

# Counters
TOTAL=0
SUCCESS=0
FAILED=0
SKIPPED=0

# Arrays for tracking
declare -a FAILED_MODULES
declare -a SUCCESS_MODULES
declare -a SKIPPED_MODULES

# Default values
DRY_RUN=false
SPECIFIC_TIER=""
COMMIT_MESSAGE=""

################################################################################
# Helper Functions
################################################################################

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"
}

print_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Update all CODITECT submodules in dependency-aware order.

OPTIONS:
    --dry-run           Show what would be done without making changes
    --tier N            Update only submodules in tier N (0-6)
    --message "MSG"     Custom commit message
    --help              Show this help message

EXAMPLES:
    # Update all submodules
    $0

    # Dry run to see what would happen
    $0 --dry-run

    # Update only Tier 2 (Backend Services)
    $0 --tier 2

    # Custom commit message
    $0 --message "Update framework integration"

TIERS:
    0 - Framework (coditect-project-dot-claude)
    1 - Core Infrastructure (framework, infrastructure, legal)
    2 - Backend Services (backend, analytics, automation)
    3 - Frontend & CLI (frontend, cli, docs)
    4 - Marketplace & Extensions
    5 - Supporting Tools
    6 - Strategic & Research
EOF
}

################################################################################
# Submodule Definitions (Dependency-Aware Order)
################################################################################

# Tier 0: Framework
TIER_0=(
    "coditect-project-dot-claude:Framework:Core CODITECT framework"
)

# Tier 1: Core Infrastructure
TIER_1=(
    "coditect-framework:Core Infrastructure:Framework implementation"
    "coditect-infrastructure:Core Infrastructure:Infrastructure as code"
    "coditect-legal:Core Infrastructure:Legal documents"
)

# Tier 2: Backend Services
TIER_2=(
    "coditect-cloud-backend:Backend Services:FastAPI backend"
    "coditect-analytics:Backend Services:ClickHouse analytics"
    "coditect-automation:Backend Services:Autonomous orchestration"
)

# Tier 3: Frontend & CLI
TIER_3=(
    "coditect-cloud-frontend:Frontend & CLI:React frontend"
    "coditect-cli:Frontend & CLI:Python CLI tools"
    "coditect-docs:Frontend & CLI:Docusaurus docs"
)

# Tier 4: Marketplace & Extensions
TIER_4=(
    "coditect-agent-marketplace:Marketplace & Extensions:Agent marketplace"
    "coditect-activity-data-model-ui:Marketplace & Extensions:Activity feed UI"
)

# Tier 5: Supporting Tools
TIER_5=(
    "az1.ai-coditect-ai-screenshot-automator:Supporting Tools:Screenshot automation"
    "coditect-interactive-workflow-analyzer:Supporting Tools:Workflow analysis"
    "Coditect-v5-multiple-LLM-IDE:Supporting Tools:Multi-LLM IDE"
)

# Tier 6: Strategic & Research
TIER_6=(
    "az1.ai-CODITECT.AI-GTM:Strategic & Research:GTM strategy"
    "az1.ai-coditect-agent-new-standard-development:Strategic & Research:Agent standards"
    "NESTED-LEARNING-GOOGLE:Strategic & Research:Educational research"
    "coditect-blog-application:Strategic & Research:Blog platform"
)

################################################################################
# Update Function
################################################################################

update_submodule() {
    local submodule_name="$1"
    local tier_name="$2"
    local description="$3"
    local tier_num="$4"

    TOTAL=$((TOTAL + 1))

    print_header "[$TOTAL/19] $submodule_name"
    log "Tier $tier_num: $tier_name"
    log "Description: $description"

    local submodule_path="$MASTER_DIR/submodules/$submodule_name"

    # Check if submodule exists
    if [ ! -d "$submodule_path" ]; then
        error "Submodule directory not found: $submodule_path"
        FAILED=$((FAILED + 1))
        FAILED_MODULES+=("$submodule_name (not found)")
        return 1
    fi

    cd "$submodule_path"

    # Check if there are changes
    if ! git status --porcelain | grep -q .; then
        warning "No changes in $submodule_name - skipping"
        SKIPPED=$((SKIPPED + 1))
        SKIPPED_MODULES+=("$submodule_name")
        cd "$MASTER_DIR"
        return 0
    fi

    log "Changes detected in $submodule_name"
    git status --short

    if [ "$DRY_RUN" = true ]; then
        warning "DRY RUN: Would commit and push changes"
        SKIPPED=$((SKIPPED + 1))
        SKIPPED_MODULES+=("$submodule_name (dry run)")
        cd "$MASTER_DIR"
        return 0
    fi

    # Prepare commit message
    local commit_msg
    if [ -n "$COMMIT_MESSAGE" ]; then
        commit_msg="$COMMIT_MESSAGE"
    else
        commit_msg="Add distributed intelligence symlinks

- .coditect → ../../.coditect (access to master CODITECT brain)
- .claude → .coditect (Claude Code compatibility)

Enables:
✅ Access to 50 agents, 189 skills, 72 commands
✅ Distributed intelligence architecture
✅ Consistent development experience

Part of: CODITECT Distributed Intelligence Rollout
Tier: $tier_num - $tier_name"
    fi

    # Add changes
    log "Staging changes..."
    git add .coditect .claude .coditect.local.backup 2>/dev/null || git add .coditect .claude 2>/dev/null || true

    # Check if anything was staged
    if git diff --cached --quiet; then
        warning "No changes staged in $submodule_name - skipping"
        SKIPPED=$((SKIPPED + 1))
        SKIPPED_MODULES+=("$submodule_name")
        cd "$MASTER_DIR"
        return 0
    fi

    # Commit
    log "Committing changes..."
    if git commit -m "$commit_msg"; then
        success "Committed changes in $submodule_name"

        # Push
        log "Pushing to remote..."
        if git push; then
            success "Pushed $submodule_name successfully"
            SUCCESS=$((SUCCESS + 1))
            SUCCESS_MODULES+=("$submodule_name")
        else
            error "Failed to push $submodule_name"
            FAILED=$((FAILED + 1))
            FAILED_MODULES+=("$submodule_name (push failed)")
            cd "$MASTER_DIR"
            return 1
        fi
    else
        error "Failed to commit $submodule_name"
        FAILED=$((FAILED + 1))
        FAILED_MODULES+=("$submodule_name (commit failed)")
        cd "$MASTER_DIR"
        return 1
    fi

    cd "$MASTER_DIR"

    # Update submodule pointer in master
    log "Updating submodule pointer in master..."
    git add "submodules/$submodule_name"

    return 0
}

################################################################################
# Process Tier
################################################################################

process_tier() {
    local tier_num=$1
    local tier_var="TIER_$tier_num[@]"
    local tier_array=("${!tier_var}")

    if [ ${#tier_array[@]} -eq 0 ]; then
        warning "No submodules in tier $tier_num"
        return
    fi

    print_header "TIER $tier_num"

    for entry in "${tier_array[@]}"; do
        IFS=':' read -r name category desc <<< "$entry"
        update_submodule "$name" "$category" "$desc" "$tier_num"
    done
}

################################################################################
# Main Execution
################################################################################

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --tier)
                SPECIFIC_TIER="$2"
                shift 2
                ;;
            --message)
                COMMIT_MESSAGE="$2"
                shift 2
                ;;
            --help)
                print_usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done

    # Print banner
    print_header "CODITECT Submodule Update Automation"
    log "Master Directory: $MASTER_DIR"
    log "Log File: $LOG_FILE"

    if [ "$DRY_RUN" = true ]; then
        warning "DRY RUN MODE - No changes will be made"
    fi

    # Navigate to master directory
    cd "$MASTER_DIR"

    # Process tiers
    if [ -n "$SPECIFIC_TIER" ]; then
        log "Processing only Tier $SPECIFIC_TIER"
        process_tier "$SPECIFIC_TIER"
    else
        log "Processing all tiers (0-6)"
        for tier in {0..6}; do
            process_tier $tier
        done
    fi

    # Commit master repo changes
    if [ "$DRY_RUN" = false ] && [ "$SUCCESS" -gt 0 ]; then
        print_header "Updating Master Repository"
        log "Committing submodule pointer updates..."

        if git diff --cached --quiet; then
            warning "No submodule pointers to update"
        else
            git commit -m "Update submodule pointers: Distributed intelligence rollout

Updated $SUCCESS submodules with distributed intelligence symlinks.
See individual submodule commits for details.

Summary:
- Success: $SUCCESS
- Failed: $FAILED
- Skipped: $SKIPPED
"
            success "Master repository updated"

            log "Pushing master repository..."
            if git push; then
                success "Master repository pushed successfully"
            else
                error "Failed to push master repository"
            fi
        fi
    fi

    # Print summary
    print_header "UPDATE SUMMARY"
    log "Total Submodules: $TOTAL"
    success "Successful: $SUCCESS"
    error "Failed: $FAILED"
    warning "Skipped: $SKIPPED"

    if [ ${#SUCCESS_MODULES[@]} -gt 0 ]; then
        echo -e "\n${GREEN}Successful Updates:${NC}"
        printf '%s\n' "${SUCCESS_MODULES[@]}" | sed 's/^/  ✅ /'
    fi

    if [ ${#FAILED_MODULES[@]} -gt 0 ]; then
        echo -e "\n${RED}Failed Updates:${NC}"
        printf '%s\n' "${FAILED_MODULES[@]}" | sed 's/^/  ❌ /'
    fi

    if [ ${#SKIPPED_MODULES[@]} -gt 0 ]; then
        echo -e "\n${YELLOW}Skipped Updates:${NC}"
        printf '%s\n' "${SKIPPED_MODULES[@]}" | sed 's/^/  ⏭️  /'
    fi

    echo -e "\n${BLUE}Log file: $LOG_FILE${NC}\n"

    # Exit with error if any failed
    if [ "$FAILED" -gt 0 ]; then
        exit 1
    fi
}

# Run main function
main "$@"
