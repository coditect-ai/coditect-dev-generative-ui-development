#!/bin/bash
# Git Workflow Automation Script
# Automated git operations with conventional commit format and safety checks

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Defaults
ACTION=""
BRANCH_NAME=""
BRANCH_TYPE="feature"
COMMIT_MESSAGE=""
COMMIT_TYPE=""
COMMIT_SCOPE=""
COMMIT_BODY=""
PR_TITLE=""
PR_BODY=""
DRY_RUN=false
AUTO_PUSH=false
REBASE=false
FORCE=false
PROJECT_ROOT="/home/hal/v4/PROJECTS/t2"

# Valid commit types
VALID_TYPES=("feat" "fix" "docs" "style" "refactor" "test" "chore")

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --status)
      ACTION="status"
      shift
      ;;
    --branch)
      ACTION="branch"
      shift
      ;;
    --commit)
      ACTION="commit"
      shift
      ;;
    --pr)
      ACTION="pr"
      shift
      ;;
    --sync)
      ACTION="sync"
      shift
      ;;
    --name)
      BRANCH_NAME="$2"
      shift 2
      ;;
    --type)
      if [[ "$ACTION" == "branch" ]]; then
        BRANCH_TYPE="$2"
      else
        COMMIT_TYPE="$2"
      fi
      shift 2
      ;;
    --message)
      COMMIT_MESSAGE="$2"
      shift 2
      ;;
    --scope)
      COMMIT_SCOPE="$2"
      shift 2
      ;;
    --body)
      COMMIT_BODY="$2"
      shift 2
      ;;
    --title)
      PR_TITLE="$2"
      shift 2
      ;;
    --pr-body)
      PR_BODY="$2"
      shift 2
      ;;
    --push)
      AUTO_PUSH=true
      shift
      ;;
    --rebase)
      REBASE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --force)
      FORCE=true
      shift
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Navigate to project root
cd "$PROJECT_ROOT"

# Check git status
check_status() {
  echo -e "${YELLOW}=== Git Status ===${NC}"

  # Branch info
  CURRENT_BRANCH=$(git branch --show-current)
  echo -e "${BLUE}Current branch:${NC} $CURRENT_BRANCH"

  # Remote tracking
  if git rev-parse --abbrev-ref @{u} &>/dev/null; then
    UPSTREAM=$(git rev-parse --abbrev-ref @{u})
    echo -e "${BLUE}Tracking:${NC} $UPSTREAM"

    # Check if ahead/behind
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    BASE=$(git merge-base @ @{u})

    if [ "$LOCAL" = "$REMOTE" ]; then
      echo -e "${GREEN}✓ Up to date with remote${NC}"
    elif [ "$LOCAL" = "$BASE" ]; then
      echo -e "${YELLOW}⚠ Behind remote (need to pull)${NC}"
    elif [ "$REMOTE" = "$BASE" ]; then
      echo -e "${YELLOW}⚠ Ahead of remote (need to push)${NC}"
    else
      echo -e "${YELLOW}⚠ Diverged from remote${NC}"
    fi
  else
    echo -e "${YELLOW}⚠ No remote tracking branch${NC}"
  fi

  echo ""

  # Modified files
  git status --short

  # Summary
  MODIFIED=$(git status --short | grep -c "^ M" || echo "0")
  ADDED=$(git status --short | grep -c "^A " || echo "0")
  DELETED=$(git status --short | grep -c "^D " || echo "0")
  UNTRACKED=$(git status --short | grep -c "^??" || echo "0")

  echo ""
  echo -e "${BLUE}Summary:${NC} $MODIFIED modified, $ADDED added, $DELETED deleted, $UNTRACKED untracked"
}

# Validate commit type
validate_commit_type() {
  local type=$1

  for valid_type in "${VALID_TYPES[@]}"; do
    if [ "$type" = "$valid_type" ]; then
      return 0
    fi
  done

  echo -e "${RED}Error: Invalid commit type '$type'${NC}"
  echo "Valid types: ${VALID_TYPES[*]}"
  return 1
}

# Create feature branch
create_branch() {
  echo -e "${YELLOW}=== Creating Branch ===${NC}"

  if [ -z "$BRANCH_NAME" ]; then
    echo -e "${RED}Error: --name required${NC}"
    exit 1
  fi

  # Check for uncommitted changes
  if [ -n "$(git status --porcelain)" ] && [ "$FORCE" = false ]; then
    echo -e "${RED}Error: Uncommitted changes detected${NC}"
    echo "Commit or stash changes before creating branch"
    echo "Use --force to override (not recommended)"
    exit 1
  fi

  # Construct full branch name
  local full_branch="${BRANCH_TYPE}/${BRANCH_NAME}"

  # Check if branch exists
  if git show-ref --verify --quiet "refs/heads/$full_branch"; then
    echo -e "${RED}Error: Branch '$full_branch' already exists${NC}"
    exit 1
  fi

  echo "Branch name: $full_branch"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would create and checkout branch${NC}"
    return 0
  fi

  # Create and checkout branch
  git checkout -b "$full_branch"

  echo -e "${GREEN}✓ Created and switched to branch: $full_branch${NC}"
}

# Commit changes
commit_changes() {
  echo -e "${YELLOW}=== Committing Changes ===${NC}"

  if [ -z "$COMMIT_MESSAGE" ]; then
    echo -e "${RED}Error: --message required${NC}"
    exit 1
  fi

  if [ -z "$COMMIT_TYPE" ]; then
    echo -e "${RED}Error: --type required${NC}"
    exit 1
  fi

  # Validate commit type
  if ! validate_commit_type "$COMMIT_TYPE"; then
    exit 1
  fi

  # Build commit message
  local commit_msg=""

  if [ -n "$COMMIT_SCOPE" ]; then
    commit_msg="${COMMIT_TYPE}(${COMMIT_SCOPE}): ${COMMIT_MESSAGE}"
  else
    commit_msg="${COMMIT_TYPE}: ${COMMIT_MESSAGE}"
  fi

  # Add body if provided
  if [ -n "$COMMIT_BODY" ]; then
    commit_msg="${commit_msg}

${COMMIT_BODY}"
  fi

  # Add automation footer
  commit_msg="${commit_msg}

🤖 Automated via git-workflow-automation skill

Co-Authored-By: Claude <noreply@anthropic.com>"

  echo "Commit message:"
  echo "---"
  echo "$commit_msg"
  echo "---"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would stage, commit, and optionally push${NC}"
    return 0
  fi

  # Stage all changes
  git add .

  # Show what will be committed
  echo -e "${BLUE}Files to commit:${NC}"
  git status --short
  echo ""

  # Commit
  git commit -m "$commit_msg"

  echo -e "${GREEN}✓ Changes committed${NC}"

  # Push if requested
  if [ "$AUTO_PUSH" = true ]; then
    echo ""
    echo -e "${YELLOW}=== Pushing to Remote ===${NC}"

    CURRENT_BRANCH=$(git branch --show-current)

    # Check if upstream exists
    if ! git rev-parse --abbrev-ref @{u} &>/dev/null; then
      echo "Setting upstream to origin/$CURRENT_BRANCH"
      git push -u origin "$CURRENT_BRANCH"
    else
      git push
    fi

    echo -e "${GREEN}✓ Changes pushed to remote${NC}"
  fi
}

# Create pull request
create_pr() {
  echo -e "${YELLOW}=== Creating Pull Request ===${NC}"

  # Check if gh CLI is installed
  if ! command -v gh &>/dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) not installed${NC}"
    echo "Install with: sudo apt install gh"
    exit 1
  fi

  if [ -z "$PR_TITLE" ]; then
    echo -e "${RED}Error: --title required${NC}"
    exit 1
  fi

  # Auto-generate body if not provided
  if [ -z "$PR_BODY" ]; then
    echo "Auto-generating PR body..."

    # Get commits since branching from main
    COMMITS=$(git log --oneline main..HEAD 2>/dev/null || git log --oneline -5)

    PR_BODY="## Summary
${COMMITS}

## Changes
[Auto-extracted from git diff]

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing complete

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes

🤖 Generated via git-workflow-automation skill"
  fi

  echo "PR Title: $PR_TITLE"
  echo ""
  echo "PR Body:"
  echo "---"
  echo "$PR_BODY"
  echo "---"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would create pull request${NC}"
    return 0
  fi

  # Create PR using heredoc for body
  gh pr create --title "$PR_TITLE" --body "$(cat <<EOF
$PR_BODY
EOF
)"

  echo -e "${GREEN}✓ Pull request created${NC}"
}

# Sync with remote
sync_remote() {
  echo -e "${YELLOW}=== Syncing with Remote ===${NC}"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would fetch and pull${NC}"
    return 0
  fi

  # Fetch
  echo "Fetching from origin..."
  git fetch origin

  # Pull or rebase
  if [ "$REBASE" = true ]; then
    echo "Rebasing on origin/main..."
    git pull --rebase origin main
  else
    echo "Pulling from origin..."
    git pull
  fi

  echo -e "${GREEN}✓ Synced with remote${NC}"
}

# Main execution
main() {
  echo -e "${GREEN}🔧 Git Workflow Automation${NC}"
  echo "Action: $ACTION"
  echo "Dry Run: $DRY_RUN"
  echo ""

  case $ACTION in
    status)
      check_status
      ;;
    branch)
      create_branch
      ;;
    commit)
      commit_changes
      ;;
    pr)
      create_pr
      ;;
    sync)
      sync_remote
      ;;
    "")
      echo -e "${RED}Error: No action specified${NC}"
      echo "Usage: $0 --status|--branch|--commit|--pr|--sync [options]"
      exit 1
      ;;
    *)
      echo -e "${RED}Error: Invalid action: $ACTION${NC}"
      exit 1
      ;;
  esac

  echo ""
  echo -e "${GREEN}✓ Done!${NC}"
}

# Run main
main
