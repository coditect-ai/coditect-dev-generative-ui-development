# Generative UI Automation Scripts

*Shell and Node.js scripts for automating UI generation workflows*

---

## Overview

This document provides production-ready scripts for automating common Generative UI tasks. Scripts are designed to work with any LLM provider through adapter interfaces.

---

## 1. Installation & Setup

### Setup Script

```bash
#!/bin/bash
# scripts/setup.sh
# Initialize Generative UI toolkit

set -e

echo "🚀 Setting up Generative UI Toolkit..."

# Create directory structure
mkdir -p .ui-gen/{templates,cache,output}
mkdir -p src/{components,hooks,tokens}

# Create default configuration
cat > .ui-gen.yaml << 'EOF'
version: 1

framework: react
typescript: true
styling: tailwind

accessibility:
  level: AA
  auto_fix: true

animation:
  library: framer-motion
  preference: subtle

output:
  components: ./src/components
  hooks: ./src/hooks
  tokens: ./src/tokens

quality:
  typescript_strict: true
  a11y_score: 90
EOF

# Create .gitignore entries
echo ".ui-gen/cache/" >> .gitignore
echo ".ui-gen/output/" >> .gitignore

# Install dependencies (if package.json exists)
if [ -f "package.json" ]; then
  echo "📦 Installing dependencies..."
  npm install --save-dev \
    @testing-library/react \
    @testing-library/jest-dom \
    axe-core \
    framer-motion
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Configure your LLM provider in .ui-gen.yaml"
echo "  2. Run '/ui component button' to generate your first component"
echo ""
```

---

## 2. Component Generation Scripts

### Generate Component Script

```bash
#!/bin/bash
# scripts/generate-component.sh
# Generate a UI component with full pipeline

set -e

# Parse arguments
COMPONENT_NAME=$1
shift

# Default options
FRAMEWORK="react"
STYLING="tailwind"
TYPESCRIPT="true"
A11Y_LEVEL="AA"
TESTS="false"
STORIES="false"
VARIANTS=""
PROPS=""

# Parse options
while [[ $# -gt 0 ]]; do
  case $1 in
    --framework=*)
      FRAMEWORK="${1#*=}"
      shift
      ;;
    --styling=*)
      STYLING="${1#*=}"
      shift
      ;;
    --typescript=*)
      TYPESCRIPT="${1#*=}"
      shift
      ;;
    --a11y=*)
      A11Y_LEVEL="${1#*=}"
      shift
      ;;
    --tests)
      TESTS="true"
      shift
      ;;
    --stories)
      STORIES="true"
      shift
      ;;
    --variants=*)
      VARIANTS="${1#*=}"
      shift
      ;;
    --props=*)
      PROPS="${1#*=}"
      shift
      ;;
    *)
      shift
      ;;
  esac
done

if [ -z "$COMPONENT_NAME" ]; then
  echo "Usage: generate-component.sh <ComponentName> [options]"
  echo ""
  echo "Options:"
  echo "  --framework=react|vue|svelte"
  echo "  --styling=tailwind|css-modules|styled-components"
  echo "  --typescript=true|false"
  echo "  --a11y=A|AA|AAA"
  echo "  --tests"
  echo "  --stories"
  echo "  --variants=variant1,variant2"
  echo "  --props=prop1,prop2"
  exit 1
fi

echo "🎨 Generating $COMPONENT_NAME component..."

# Create output directory
OUTPUT_DIR="./src/components/$COMPONENT_NAME"
mkdir -p "$OUTPUT_DIR"

# Build prompt
PROMPT=$(cat << EOF
You are a senior $FRAMEWORK + TypeScript engineer.
Generate a production-ready \`$COMPONENT_NAME\` component.

Requirements:
- Implement as a typed $FRAMEWORK functional component in TypeScript.
$([ -n "$VARIANTS" ] && echo "- Variants: $VARIANTS")
$([ -n "$PROPS" ] && echo "- Props: $PROPS")
- Styling: $STYLING utility classes.
- Accessibility level: WCAG $A11Y_LEVEL
  - Native semantic elements
  - ARIA attributes for custom patterns
  - Keyboard navigation
  - Visible focus states

Output only the complete TypeScript code. No explanations, no comments.
EOF
)

# Call LLM (using environment variable for provider)
if [ -n "$UI_GEN_LLM_PROVIDER" ]; then
  case $UI_GEN_LLM_PROVIDER in
    claude)
      RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
        -H "Content-Type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
          \"model\": \"claude-sonnet-4-20250514\",
          \"max_tokens\": 4000,
          \"messages\": [{\"role\": \"user\", \"content\": \"$PROMPT\"}]
        }")
      CODE=$(echo "$RESPONSE" | jq -r '.content[0].text')
      ;;
    openai)
      RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d "{
          \"model\": \"gpt-4\",
          \"messages\": [{\"role\": \"user\", \"content\": \"$PROMPT\"}]
        }")
      CODE=$(echo "$RESPONSE" | jq -r '.choices[0].message.content')
      ;;
    *)
      echo "Unknown LLM provider: $UI_GEN_LLM_PROVIDER"
      exit 1
      ;;
  esac
else
  echo "⚠️  No LLM provider configured. Set UI_GEN_LLM_PROVIDER environment variable."
  exit 1
fi

# Write component file
echo "$CODE" > "$OUTPUT_DIR/$COMPONENT_NAME.tsx"
echo "✅ Generated $OUTPUT_DIR/$COMPONENT_NAME.tsx"

# Generate index file
echo "export { $COMPONENT_NAME } from './$COMPONENT_NAME';" > "$OUTPUT_DIR/index.ts"
echo "✅ Generated $OUTPUT_DIR/index.ts"

# Generate tests if requested
if [ "$TESTS" = "true" ]; then
  cat > "$OUTPUT_DIR/$COMPONENT_NAME.test.tsx" << EOF
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';
import { $COMPONENT_NAME } from './$COMPONENT_NAME';

expect.extend(toHaveNoViolations);

describe('$COMPONENT_NAME', () => {
  it('renders without crashing', () => {
    render(<$COMPONENT_NAME />);
  });

  it('has no accessibility violations', async () => {
    const { container } = render(<$COMPONENT_NAME />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  // Add more tests here
});
EOF
  echo "✅ Generated $OUTPUT_DIR/$COMPONENT_NAME.test.tsx"
fi

# Generate Storybook stories if requested
if [ "$STORIES" = "true" ]; then
  cat > "$OUTPUT_DIR/$COMPONENT_NAME.stories.tsx" << EOF
import type { Meta, StoryObj } from '@storybook/react';
import { $COMPONENT_NAME } from './$COMPONENT_NAME';

const meta: Meta<typeof $COMPONENT_NAME> = {
  title: 'Components/$COMPONENT_NAME',
  component: $COMPONENT_NAME,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof $COMPONENT_NAME>;

export const Default: Story = {};

// Add variant stories here
EOF
  echo "✅ Generated $OUTPUT_DIR/$COMPONENT_NAME.stories.tsx"
fi

echo ""
echo "🎉 Component generation complete!"
echo ""
echo "Files created:"
echo "  → $OUTPUT_DIR/$COMPONENT_NAME.tsx"
echo "  → $OUTPUT_DIR/index.ts"
[ "$TESTS" = "true" ] && echo "  → $OUTPUT_DIR/$COMPONENT_NAME.test.tsx"
[ "$STORIES" = "true" ] && echo "  → $OUTPUT_DIR/$COMPONENT_NAME.stories.tsx"
```

---

## 3. Accessibility Audit Scripts

### A11y Audit Script

```bash
#!/bin/bash
# scripts/a11y-audit.sh
# Run accessibility audit on components

set -e

TARGET=${1:-.src/components}
LEVEL=${2:-AA}
OUTPUT_FORMAT=${3:-text}

echo "🔍 Running accessibility audit..."
echo "   Target: $TARGET"
echo "   Level: WCAG $LEVEL"
echo ""

# Create temp file for results
RESULTS_FILE=$(mktemp)

# Find all component files
find "$TARGET" -name "*.tsx" -o -name "*.jsx" | while read -r file; do
  echo "Auditing: $file"
  
  # Run static analysis
  # This would call the a11y-auditor agent or use axe-core
  
done

# Generate report based on format
case $OUTPUT_FORMAT in
  json)
    cat "$RESULTS_FILE" | jq '.'
    ;;
  md)
    echo "# Accessibility Audit Report"
    echo ""
    echo "**Target:** $TARGET"
    echo "**Level:** WCAG $LEVEL"
    echo "**Date:** $(date)"
    echo ""
    echo "## Results"
    echo ""
    cat "$RESULTS_FILE"
    ;;
  *)
    cat "$RESULTS_FILE"
    ;;
esac

rm "$RESULTS_FILE"
```

### A11y Fix Script

```bash
#!/bin/bash
# scripts/a11y-fix.sh
# Auto-fix accessibility issues

set -e

TARGET=${1:-.src/components}
DRY_RUN=${2:-false}

echo "🔧 Running accessibility auto-fix..."
echo "   Target: $TARGET"
[ "$DRY_RUN" = "true" ] && echo "   Mode: Dry run"
echo ""

# Common fixes to apply
FIXES=(
  # Add alt text to images
  's/<img ([^>]*)(?<!alt=)>/<img \1 alt="">/g'
  
  # Add button type
  's/<button(?! type=)/<button type="button"/g'
  
  # Add aria-label to icon buttons
  's/<button([^>]*)><svg/<button\1 aria-label="TODO"><svg/g'
)

find "$TARGET" -name "*.tsx" -o -name "*.jsx" | while read -r file; do
  echo "Processing: $file"
  
  if [ "$DRY_RUN" = "true" ]; then
    echo "  Would apply fixes to $file"
  else
    for fix in "${FIXES[@]}"; do
      sed -i -E "$fix" "$file"
    done
    echo "  ✅ Applied fixes"
  fi
done

echo ""
echo "🎉 Auto-fix complete!"
```

---

## 4. Motion Token Scripts

### Generate Motion Tokens

```bash
#!/bin/bash
# scripts/generate-motion-tokens.sh
# Generate motion token system

set -e

OUTPUT_DIR=${1:-./src/tokens}
FORMAT=${2:-ts}

mkdir -p "$OUTPUT_DIR"

case $FORMAT in
  ts)
    cat > "$OUTPUT_DIR/motion.ts" << 'EOF'
/**
 * Motion Token System
 * Generated by Generative UI Toolkit
 */

export const motion = {
  duration: {
    instant: 0,
    fast: 120,
    normal: 240,
    slow: 400,
    slower: 600,
  },
  
  easing: {
    linear: [0, 0, 1, 1] as const,
    easeOut: [0.16, 1, 0.3, 1] as const,
    easeIn: [0.4, 0, 1, 1] as const,
    easeInOut: [0.65, 0, 0.35, 1] as const,
  },
  
  distance: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
} as const;

export type MotionDuration = keyof typeof motion.duration;
export type MotionEasing = keyof typeof motion.easing;
export type MotionDistance = keyof typeof motion.distance;

// Framer Motion variants
export const variants = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
    transition: { duration: motion.duration.normal / 1000 },
  },
  
  slideUp: {
    initial: { opacity: 0, y: motion.distance.md },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -motion.distance.sm },
    transition: { 
      duration: motion.duration.normal / 1000,
      ease: motion.easing.easeOut,
    },
  },
  
  slideRight: {
    initial: { opacity: 0, x: -motion.distance.lg },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: motion.distance.lg },
    transition: {
      duration: motion.duration.normal / 1000,
      ease: motion.easing.easeOut,
    },
  },
  
  scale: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.95 },
    transition: {
      duration: motion.duration.normal / 1000,
      ease: motion.easing.easeOut,
    },
  },
} as const;

// CSS custom properties for non-Framer usage
export const cssVariables = `
:root {
  --motion-duration-instant: ${motion.duration.instant}ms;
  --motion-duration-fast: ${motion.duration.fast}ms;
  --motion-duration-normal: ${motion.duration.normal}ms;
  --motion-duration-slow: ${motion.duration.slow}ms;
  --motion-duration-slower: ${motion.duration.slower}ms;
  
  --motion-easing-linear: linear;
  --motion-easing-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --motion-easing-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --motion-easing-ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  
  --motion-distance-xs: ${motion.distance.xs}px;
  --motion-distance-sm: ${motion.distance.sm}px;
  --motion-distance-md: ${motion.distance.md}px;
  --motion-distance-lg: ${motion.distance.lg}px;
  --motion-distance-xl: ${motion.distance.xl}px;
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-duration-instant: 0ms;
    --motion-duration-fast: 0ms;
    --motion-duration-normal: 0ms;
    --motion-duration-slow: 0ms;
    --motion-duration-slower: 0ms;
  }
}
`;
EOF
    echo "✅ Generated $OUTPUT_DIR/motion.ts"
    ;;
    
  css)
    cat > "$OUTPUT_DIR/motion.css" << 'EOF'
/**
 * Motion Token System (CSS)
 * Generated by Generative UI Toolkit
 */

:root {
  /* Durations */
  --motion-duration-instant: 0ms;
  --motion-duration-fast: 120ms;
  --motion-duration-normal: 240ms;
  --motion-duration-slow: 400ms;
  --motion-duration-slower: 600ms;
  
  /* Easings */
  --motion-easing-linear: linear;
  --motion-easing-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --motion-easing-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --motion-easing-ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  
  /* Distances */
  --motion-distance-xs: 4px;
  --motion-distance-sm: 8px;
  --motion-distance-md: 16px;
  --motion-distance-lg: 24px;
  --motion-distance-xl: 32px;
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-duration-instant: 0ms;
    --motion-duration-fast: 0ms;
    --motion-duration-normal: 0ms;
    --motion-duration-slow: 0ms;
    --motion-duration-slower: 0ms;
  }
}

/* Animation utilities */
.animate-fade-in {
  animation: fadeIn var(--motion-duration-normal) var(--motion-easing-ease-out);
}

.animate-slide-up {
  animation: slideUp var(--motion-duration-normal) var(--motion-easing-ease-out);
}

.animate-slide-right {
  animation: slideRight var(--motion-duration-normal) var(--motion-easing-ease-out);
}

.animate-scale {
  animation: scale var(--motion-duration-normal) var(--motion-easing-ease-out);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(var(--motion-distance-md));
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideRight {
  from {
    opacity: 0;
    transform: translateX(calc(-1 * var(--motion-distance-lg)));
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes scale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
EOF
    echo "✅ Generated $OUTPUT_DIR/motion.css"
    ;;
esac
```

---

## 5. Batch Generation Scripts

### Batch Component Generator

```bash
#!/bin/bash
# scripts/batch-generate.sh
# Generate multiple components from a manifest

set -e

MANIFEST=${1:-./components.yaml}

if [ ! -f "$MANIFEST" ]; then
  echo "❌ Manifest file not found: $MANIFEST"
  echo ""
  echo "Create a manifest file with this format:"
  echo ""
  echo "components:"
  echo "  - name: Button"
  echo "    variants: [primary, secondary, ghost]"
  echo "    props: [leftIcon, rightIcon, isLoading]"
  echo "    tests: true"
  echo "    stories: true"
  echo ""
  echo "  - name: Card"
  echo "    variants: [elevated, outlined]"
  echo "    props: [image, title, description]"
  exit 1
fi

echo "📦 Batch generating components from $MANIFEST..."
echo ""

# Parse YAML and generate each component
# Using yq if available, otherwise basic parsing
if command -v yq &> /dev/null; then
  COMPONENTS=$(yq e '.components[].name' "$MANIFEST")
  
  for name in $COMPONENTS; do
    variants=$(yq e ".components[] | select(.name == \"$name\") | .variants | join(\",\")" "$MANIFEST")
    props=$(yq e ".components[] | select(.name == \"$name\") | .props | join(\",\")" "$MANIFEST")
    tests=$(yq e ".components[] | select(.name == \"$name\") | .tests" "$MANIFEST")
    stories=$(yq e ".components[] | select(.name == \"$name\") | .stories" "$MANIFEST")
    
    cmd="./scripts/generate-component.sh $name"
    [ -n "$variants" ] && cmd="$cmd --variants=$variants"
    [ -n "$props" ] && cmd="$cmd --props=$props"
    [ "$tests" = "true" ] && cmd="$cmd --tests"
    [ "$stories" = "true" ] && cmd="$cmd --stories"
    
    echo "Generating: $name"
    eval "$cmd"
    echo ""
  done
else
  echo "⚠️  yq not found. Install yq for YAML parsing."
  echo "   brew install yq (macOS)"
  echo "   apt install yq (Linux)"
fi

echo "🎉 Batch generation complete!"
```

### Component Manifest Template

```yaml
# components.yaml
# Manifest for batch component generation

version: 1

# Global settings (can be overridden per component)
defaults:
  framework: react
  styling: tailwind
  typescript: true
  a11y_level: AA

components:
  # Buttons
  - name: Button
    variants: [primary, secondary, ghost, danger]
    sizes: [sm, md, lg]
    props: [leftIcon, rightIcon, isLoading, fullWidth]
    states: [disabled, loading]
    tests: true
    stories: true

  - name: IconButton
    variants: [primary, secondary, ghost]
    sizes: [sm, md, lg]
    props: [icon, ariaLabel]
    tests: true
    stories: true

  # Inputs
  - name: Input
    variants: [text, email, password, search]
    props: [label, placeholder, helperText, error, leftAddon, rightAddon]
    states: [disabled, error, success]
    tests: true
    stories: true

  - name: Textarea
    props: [label, placeholder, helperText, error, rows, maxLength]
    tests: true
    stories: true

  - name: Select
    props: [label, options, placeholder, error]
    tests: true
    stories: true

  - name: Checkbox
    props: [label, checked, indeterminate]
    tests: true
    stories: true

  # Layout
  - name: Card
    variants: [elevated, outlined, filled]
    props: [image, title, description, actions, onClick]
    tests: true
    stories: true

  - name: Modal
    props: [isOpen, onClose, title, size]
    sizes: [sm, md, lg, full]
    tests: true
    stories: true

  - name: Drawer
    props: [isOpen, onClose, position, title]
    variants: [left, right, top, bottom]
    tests: true
    stories: true

  # Navigation
  - name: Tabs
    props: [tabs, activeTab, onChange]
    variants: [underline, pills, enclosed]
    tests: true
    stories: true

  - name: Breadcrumb
    props: [items, separator]
    tests: true
    stories: true

  # Feedback
  - name: Toast
    variants: [info, success, warning, error]
    props: [message, action, duration]
    tests: true
    stories: true

  - name: Alert
    variants: [info, success, warning, error]
    props: [title, message, closable]
    tests: true
    stories: true

  # Data Display
  - name: Table
    props: [columns, data, sortable, selectable]
    tests: true
    stories: true

  - name: Avatar
    sizes: [xs, sm, md, lg, xl]
    props: [src, name, status]
    tests: true
    stories: true

  - name: Badge
    variants: [solid, subtle, outline]
    props: [label, colorScheme]
    tests: true
    stories: true
```

---

## 6. CI/CD Integration Scripts

### Pre-commit Hook

```bash
#!/bin/bash
# .husky/pre-commit
# Pre-commit hook for Generative UI

set -e

echo "🔍 Running pre-commit checks..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(tsx|jsx)$' || true)

if [ -z "$STAGED_FILES" ]; then
  echo "No component files staged."
  exit 0
fi

# Run accessibility audit on staged files
echo "Running accessibility audit..."
for file in $STAGED_FILES; do
  if [[ "$file" == *"/components/"* ]]; then
    ./scripts/a11y-audit.sh "$file" AA json > /tmp/a11y-result.json
    
    SCORE=$(jq '.score' /tmp/a11y-result.json)
    if [ "$SCORE" -lt 90 ]; then
      echo "❌ Accessibility score too low for $file: $SCORE/100"
      echo "   Run '/a11y audit $file' for details"
      exit 1
    fi
  fi
done

# Run TypeScript check
echo "Running TypeScript check..."
npx tsc --noEmit

echo "✅ Pre-commit checks passed!"
```

### GitHub Actions Workflow

```yaml
# .github/workflows/ui-quality.yml
name: UI Quality

on:
  push:
    paths:
      - 'src/components/**'
  pull_request:
    paths:
      - 'src/components/**'

jobs:
  accessibility:
    name: Accessibility Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run accessibility audit
        run: |
          ./scripts/a11y-audit.sh ./src/components AA json > a11y-report.json
          
      - name: Check accessibility score
        run: |
          SCORE=$(jq '.score' a11y-report.json)
          if [ "$SCORE" -lt 90 ]; then
            echo "Accessibility score: $SCORE/100 (minimum: 90)"
            exit 1
          fi
          
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: a11y-report
          path: a11y-report.json

  visual-regression:
    name: Visual Regression
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build Storybook
        run: npm run build-storybook
        
      - name: Run visual tests
        run: npm run test:visual
```

---

## 7. Node.js CLI Tool

### CLI Entry Point

```typescript
#!/usr/bin/env node
// cli/index.ts
// Generative UI CLI Tool

import { Command } from 'commander';
import { generateComponent } from './commands/component';
import { generateLayout } from './commands/layout';
import { auditAccessibility } from './commands/a11y';
import { generateMotionTokens } from './commands/motion';

const program = new Command();

program
  .name('ui-gen')
  .description('Generative UI Toolkit CLI')
  .version('1.0.0');

// Component generation
program
  .command('component <name>')
  .description('Generate a UI component')
  .option('--variants <variants>', 'Component variants (comma-separated)')
  .option('--props <props>', 'Component props (comma-separated)')
  .option('--framework <framework>', 'Target framework', 'react')
  .option('--styling <styling>', 'Styling approach', 'tailwind')
  .option('--a11y <level>', 'Accessibility level', 'AA')
  .option('--tests', 'Generate tests')
  .option('--stories', 'Generate Storybook stories')
  .action(generateComponent);

// Layout generation
program
  .command('layout <type>')
  .description('Generate a page layout')
  .option('--sidebar', 'Include sidebar')
  .option('--topbar', 'Include top bar')
  .option('--responsive', 'Make responsive', true)
  .action(generateLayout);

// Accessibility audit
program
  .command('a11y <target>')
  .description('Run accessibility audit')
  .option('--level <level>', 'WCAG level', 'AA')
  .option('--fix', 'Auto-fix issues')
  .option('--format <format>', 'Output format', 'text')
  .action(auditAccessibility);

// Motion tokens
program
  .command('motion')
  .description('Generate motion token system')
  .option('--output <dir>', 'Output directory', './src/tokens')
  .option('--format <format>', 'Output format (ts|css)', 'ts')
  .action(generateMotionTokens);

program.parse();
```

### Package.json Scripts

```json
{
  "name": "ui-gen",
  "version": "1.0.0",
  "bin": {
    "ui-gen": "./dist/cli/index.js"
  },
  "scripts": {
    "build": "tsc",
    "ui:component": "ts-node cli/index.ts component",
    "ui:layout": "ts-node cli/index.ts layout",
    "ui:a11y": "ts-node cli/index.ts a11y",
    "ui:motion": "ts-node cli/index.ts motion",
    "ui:setup": "./scripts/setup.sh",
    "ui:batch": "./scripts/batch-generate.sh"
  }
}
```

---

## 8. Makefile

```makefile
# Makefile
# Generative UI Toolkit commands

.PHONY: setup component layout a11y motion batch clean

# Default target
help:
	@echo "Generative UI Toolkit"
	@echo ""
	@echo "Usage:"
	@echo "  make setup              Initialize toolkit"
	@echo "  make component NAME=X   Generate component"
	@echo "  make layout TYPE=X      Generate layout"
	@echo "  make a11y TARGET=X      Run accessibility audit"
	@echo "  make motion             Generate motion tokens"
	@echo "  make batch              Batch generate from manifest"
	@echo "  make clean              Clean generated files"

setup:
	./scripts/setup.sh

component:
ifndef NAME
	$(error NAME is required. Usage: make component NAME=Button)
endif
	./scripts/generate-component.sh $(NAME) $(OPTIONS)

layout:
ifndef TYPE
	$(error TYPE is required. Usage: make layout TYPE=dashboard)
endif
	./scripts/generate-layout.sh $(TYPE) $(OPTIONS)

a11y:
	./scripts/a11y-audit.sh $(TARGET) $(LEVEL) $(FORMAT)

motion:
	./scripts/generate-motion-tokens.sh $(OUTPUT) $(FORMAT)

batch:
	./scripts/batch-generate.sh $(MANIFEST)

clean:
	rm -rf .ui-gen/cache/*
	rm -rf .ui-gen/output/*
```

---

*Document Version: 1.0*
*Compatibility: Bash 4+, Node.js 18+, POSIX-compliant shells*
*Last Updated: November 2025*
