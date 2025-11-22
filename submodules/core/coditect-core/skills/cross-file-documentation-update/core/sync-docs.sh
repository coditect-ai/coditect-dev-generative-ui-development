#!/bin/bash
# Cross-File Documentation Update Script
# Synchronized updates to CLAUDE.md, README.md, .claude/CLAUDE.md

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Defaults
DOC_PATH=""
DOC_TITLE=""
DESCRIPTION=""
DRY_RUN=false
PROJECT_ROOT="/home/hal/v4/PROJECTS/t2"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --doc-path)
      DOC_PATH="$2"
      shift 2
      ;;
    --doc-title)
      DOC_TITLE="$2"
      shift 2
      ;;
    --description)
      DESCRIPTION="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --skip-validation)
      SKIP_VALIDATION=true
      shift
      ;;
    --force-duplicate)
      FORCE_DUPLICATE=true
      shift
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$DOC_PATH" ]; then
  echo -e "${RED}Error: --doc-path required${NC}"
  echo "Usage: $0 --doc-path=\"docs/11-analysis/FILE.md\" --doc-title=\"Title\" --description=\"Description\""
  exit 1
fi

if [ -z "$DOC_TITLE" ]; then
  echo -e "${RED}Error: --doc-title required${NC}"
  exit 1
fi

if [ -z "$DESCRIPTION" ]; then
  echo -e "${RED}Error: --description required${NC}"
  exit 1
fi

# Navigate to project root
cd "$PROJECT_ROOT"

echo -e "${GREEN}📚 Cross-File Documentation Update${NC}"
echo "Document: $(basename $DOC_PATH)"
echo "Title: $DOC_TITLE"
echo "Description: $DESCRIPTION"
echo "Dry Run: $DRY_RUN"
echo ""

# Validate document path
validate_doc_path() {
  echo -e "${YELLOW}=== Validating document path ===${NC}"

  if [ "$SKIP_VALIDATION" = true ]; then
    echo -e "${YELLOW}Skipping validation (--skip-validation)${NC}"
    return 0
  fi

  # Check file exists
  if [ ! -f "$DOC_PATH" ]; then
    echo -e "${RED}Error: Document does not exist: $DOC_PATH${NC}"
    return 1
  fi

  # Check path format (docs/XX-category/FILE.md)
  if [[ ! "$DOC_PATH" =~ ^docs/[0-9]{2}-[a-z-]+/.+\.md$ ]]; then
    echo -e "${YELLOW}Warning: Path format doesn't match expected pattern (docs/XX-category/FILE.md)${NC}"
    echo "Continuing anyway..."
  fi

  echo -e "${GREEN}✅ Document path valid${NC}"
  echo ""
}

# Check for duplicate entries
check_duplicates() {
  echo -e "${YELLOW}=== Checking for duplicates ===${NC}"

  if [ "$FORCE_DUPLICATE" = true ]; then
    echo -e "${YELLOW}Skipping duplicate check (--force-duplicate)${NC}"
    return 0
  fi

  local found=false

  # Check CLAUDE.md
  if grep -q "$DOC_PATH" CLAUDE.md 2>/dev/null; then
    echo -e "${RED}Duplicate found in CLAUDE.md${NC}"
    found=true
  fi

  # Check README.md
  if grep -q "$(basename $DOC_PATH)" README.md 2>/dev/null; then
    echo -e "${RED}Duplicate found in README.md${NC}"
    found=true
  fi

  # Check .claude/CLAUDE.md
  if grep -q "$DOC_PATH" .claude/CLAUDE.md 2>/dev/null; then
    echo -e "${RED}Duplicate found in .claude/CLAUDE.md${NC}"
    found=true
  fi

  if [ "$found" = true ]; then
    echo -e "${RED}Error: Document already referenced in one or more files${NC}"
    echo "Use --force-duplicate to add anyway"
    return 1
  fi

  echo -e "${GREEN}✅ No duplicates found${NC}"
  echo ""
}

# Update CLAUDE.md (critical reads section)
update_claude_md() {
  echo -e "${YELLOW}=== Updating CLAUDE.md ===${NC}"

  local file="CLAUDE.md"
  local marker="**Critical first reads**:"

  # Find line number of marker
  local line_num=$(grep -n "$marker" "$file" | head -1 | cut -d: -f1)

  if [ -z "$line_num" ]; then
    echo -e "${RED}Error: Could not find '$marker' in $file${NC}"
    return 1
  fi

  # Calculate insertion line (after marker line)
  local insert_line=$((line_num + 1))

  # Create new entry
  local new_entry="- [\`$DOC_PATH\`]($DOC_PATH) - $DESCRIPTION"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would insert at line $insert_line:${NC}"
    echo "$new_entry"
  else
    # Use sed to insert new line
    sed -i "${insert_line}i\\${new_entry}" "$file"
    echo -e "${GREEN}✅ Updated $file (line $insert_line)${NC}"
  fi

  echo ""
}

# Update README.md (docs/ structure)
update_readme_md() {
  echo -e "${YELLOW}=== Updating README.md ===${NC}"

  local file="README.md"

  # Extract directory from DOC_PATH (e.g., "docs/11-analysis/")
  local doc_dir=$(dirname "$DOC_PATH")
  local doc_filename=$(basename "$DOC_PATH")

  # Find the section for this directory
  local marker="├── $(basename $doc_dir)/"
  local line_num=$(grep -n "$marker" "$file" | head -1 | cut -d: -f1)

  if [ -z "$line_num" ]; then
    echo -e "${YELLOW}Warning: Could not find directory marker '$marker' in $file${NC}"
    echo "Skipping README.md update"
    return 0
  fi

  # Find next line with proper indentation for file entry
  local insert_line=$((line_num + 1))

  # Create new entry with proper tree structure
  local new_entry="│   │   └── $doc_filename  # $DESCRIPTION"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would insert at line $insert_line:${NC}"
    echo "$new_entry"
  else
    sed -i "${insert_line}i\\${new_entry}" "$file"
    echo -e "${GREEN}✅ Updated $file (line $insert_line)${NC}"
  fi

  echo ""
}

# Update .claude/CLAUDE.md (documentation hierarchy)
update_claude_config_md() {
  echo -e "${YELLOW}=== Updating .claude/CLAUDE.md ===${NC}"

  local file=".claude/CLAUDE.md"
  local marker="**Always read these in order when starting a session:**"

  # Find line number of marker
  local line_num=$(grep -n "$marker" "$file" | head -1 | cut -d: -f1)

  if [ -z "$line_num" ]; then
    echo -e "${RED}Error: Could not find '$marker' in $file${NC}"
    return 1
  fi

  # Find the last numbered item (e.g., "3. ")
  local last_item_line=$(awk "NR > $line_num && /^[0-9]+\. / { line=NR } END { print line }" "$file")

  if [ -z "$last_item_line" ]; then
    # No numbered items found, insert after marker
    insert_line=$((line_num + 1))
    item_number=1
  else
    # Extract last item number
    local last_number=$(sed -n "${last_item_line}p" "$file" | grep -oP '^\d+')
    item_number=$((last_number + 1))
    insert_line=$((last_item_line + 1))
  fi

  # Create new entry
  local new_entry="${item_number}. \`/workspace/PROJECTS/t2/$DOC_PATH\` - $DESCRIPTION"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would insert at line $insert_line:${NC}"
    echo "$new_entry"
  else
    sed -i "${insert_line}i\\${new_entry}" "$file"
    echo -e "${GREEN}✅ Updated $file (line $insert_line)${NC}"
  fi

  echo ""
}

# Git commit and push
git_commit_push() {
  echo -e "${YELLOW}=== Git commit and push ===${NC}"

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN] Would commit and push:${NC}"
    echo "Files: CLAUDE.md, README.md, .claude/CLAUDE.md"
    echo "Message: docs: Add $DOC_TITLE to documentation hierarchy"
    return 0
  fi

  # Stage files
  git add CLAUDE.md README.md .claude/CLAUDE.md

  # Create commit message
  local commit_msg="docs: Add $DOC_TITLE to documentation hierarchy

- Added to CLAUDE.md critical reads
- Added to README.md docs/ structure
- Added to .claude/CLAUDE.md hierarchy
- Description: $DESCRIPTION

🤖 Automated via cross-file-documentation-update skill"

  # Commit
  git commit -m "$commit_msg"

  # Push
  git push

  echo -e "${GREEN}✅ Commit and push complete${NC}"
  echo ""
}

# Main execution
main() {
  validate_doc_path
  check_duplicates
  update_claude_md
  update_readme_md
  update_claude_config_md
  git_commit_push

  echo -e "${GREEN}=== 🎉 Documentation synchronized across 4 files! ===${NC}"
  echo ""
  echo "Updated:"
  echo "  - CLAUDE.md (critical reads)"
  echo "  - README.md (docs/ structure)"
  echo "  - .claude/CLAUDE.md (documentation hierarchy)"
  echo "  - Git repository (committed and pushed)"
}

# Run main
main
