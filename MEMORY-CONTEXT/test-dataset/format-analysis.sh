#!/bin/bash

echo "=== COMPREHENSIVE FORMAT ANALYSIS ==="
echo ""

# 1. Analyze line patterns in text exports
echo "1. TEXT EXPORT LINE PATTERNS"
echo "   Checking first 100 lines of 5 random text exports..."
echo ""

for file in $(ls exports/*.txt | shuf | head -5); do
    echo "   File: $(basename $file)"
    
    # Check for markers
    user_markers=$(grep -c "^⏺" "$file" 2>/dev/null || echo 0)
    assistant_markers=$(grep -c "^⎿" "$file" 2>/dev/null || echo 0)
    bullet_markers=$(grep -c "^●" "$file" 2>/dev/null || echo 0)
    indent_markers=$(grep -c "^  ⎿" "$file" 2>/dev/null || echo 0)
    
    echo "     - ⏺ (user): $user_markers"
    echo "     - ⎿ (result): $assistant_markers"
    echo "     - ● (action): $bullet_markers"
    echo "     - '  ⎿' (indented result): $indent_markers"
    echo ""
done

# 2. Check JSON structure consistency
echo ""
echo "2. JSON EXPORT STRUCTURE"
echo "   Analyzing JSON keys..."
echo ""

for file in exports/*.json; do
    if [ -f "$file" ]; then
        echo "   $(basename $file):"
        jq -r 'keys | .[]' "$file" 2>/dev/null | head -3 | sed 's/^/     - /'
        break
    fi
done

# 3. Checkpoint section patterns
echo ""
echo "3. CHECKPOINT SECTION HEADINGS"
echo "   Common sections found:"
echo ""

grep "^##" checkpoints/*.md | cut -d: -f2 | sort | uniq -c | sort -rn | head -10 | sed 's/^/   /'

# 4. File size distribution
echo ""
echo "4. FILE SIZE DISTRIBUTION"
echo "   Text exports:"
ls -lh exports/*.txt | awk '{print $5}' | sort | uniq -c | head -5 | sed 's/^/   /'

echo ""
echo "   JSON exports:"
ls -lh exports/*.json | awk '{print $5}' | sort | uniq -c | sed 's/^/   /'

echo ""
echo "   Checkpoints:"
ls -lh checkpoints/*.md | awk '{print $5}' | sort | uniq -c | head -5 | sed 's/^/   /'

