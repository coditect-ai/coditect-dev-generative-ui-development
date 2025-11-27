# Generative UI Slash Commands

*Command reference for Claude Code and compatible environments*

---

## Command Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GENERATIVE UI COMMAND TREE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  /ui                          # Root command for UI generation          │
│  ├── component <name>         # Generate single component               │
│  ├── layout <type>            # Generate page layout                    │
│  ├── form <name>              # Generate form with validation           │
│  ├── wizard <name>            # Generate multi-step wizard              │
│  ├── dashboard <name>         # Generate dashboard layout               │
│  ├── animate <target>         # Add animations to existing code         │
│  ├── audit <target>           # Audit existing code for a11y            │
│  └── config                   # Configure generation settings           │
│                                                                         │
│  /motion                      # Motion/animation commands               │
│  ├── tokens                   # Generate motion token system            │
│  ├── add <animation>          # Add animation to component              │
│  └── audit                    # Audit motion accessibility              │
│                                                                         │
│  /a11y                        # Accessibility commands                  │
│  ├── audit <target>           # Full accessibility audit                │
│  ├── fix <target>             # Auto-fix accessibility issues           │
│  └── report                   # Generate accessibility report           │
│                                                                         │
│  /design                      # Design system commands                  │
│  ├── tokens                   # Generate design tokens                  │
│  ├── component <name>         # Generate design system component        │
│  └── docs                     # Generate component documentation        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. /ui Commands

### /ui component

Generate a single UI component.

```bash
/ui component <name> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--variants` | string[] | - | Component variants (comma-separated) |
| `--sizes` | string[] | - | Size variants (comma-separated) |
| `--states` | string[] | - | State variants (comma-separated) |
| `--props` | string[] | - | Additional props to include |
| `--framework` | string | react | Target framework |
| `--styling` | string | tailwind | Styling approach |
| `--a11y` | string | AA | Accessibility level |
| `--typescript` | boolean | true | Generate TypeScript |
| `--tests` | boolean | false | Generate tests |
| `--stories` | boolean | false | Generate Storybook stories |

**Examples:**

```bash
# Basic button
/ui component button

# Button with variants and loading state
/ui component button --variants=primary,secondary,ghost --states=loading,disabled

# Card with image and actions
/ui component card --props=image,title,description,actions --variants=elevated,outlined

# Input with validation
/ui component input --variants=text,email,password --states=error,success,disabled --props=label,helperText

# Full component with tests and stories
/ui component searchbar --props=onSearch,placeholder,loading --tests --stories
```

**Output:**

```
✓ Generated Button.tsx (1,247 tokens)
✓ Accessibility score: 94/100
✓ TypeScript coverage: 100%

Files created:
  → src/components/Button.tsx
  → src/components/Button.test.tsx (if --tests)
  → src/components/Button.stories.tsx (if --stories)
```

---

### /ui layout

Generate a page layout with slots.

```bash
/ui layout <type> [options]
```

**Layout Types:**

| Type | Description | Complexity |
|------|-------------|------------|
| `dashboard` | Admin dashboard with sidebar | High |
| `form` | Form layout with sections | Medium |
| `grid` | Responsive grid layout | Low |
| `split` | Two-panel layout | Low |
| `stack` | Stacked sections | Low |
| `sidebar` | Content with sidebar | Medium |

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--sidebar` | boolean | false | Include sidebar |
| `--topbar` | boolean | false | Include top navigation |
| `--footer` | boolean | false | Include footer |
| `--responsive` | boolean | true | Make responsive |
| `--breakpoints` | string | sm,md,lg | Responsive breakpoints |

**Examples:**

```bash
# Dashboard with sidebar and topbar
/ui layout dashboard --sidebar --topbar --responsive

# Form layout with 3 sections
/ui layout form --sections=personal,preferences,security

# Split layout with resizable panels
/ui layout split --resizable --ratio=1:2

# Grid layout with responsive columns
/ui layout grid --cols=1,2,3,4 --gap=6
```

---

### /ui form

Generate a form with validation.

```bash
/ui form <name> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--fields` | string[] | - | Field definitions |
| `--validation` | string | zod | Validation library |
| `--submit` | string | - | Submit handler name |
| `--layout` | string | stack | Form layout |
| `--sections` | string[] | - | Group fields into sections |

**Field Definition Syntax:**

```
fieldName:type:required:validation

Examples:
- email:email:required:email
- password:password:required:min=8
- name:text:required
- age:number:optional:min=0,max=120
- terms:checkbox:required
```

**Examples:**

```bash
# Login form
/ui form login --fields=email:email:required,password:password:required --submit=handleLogin

# Registration form with sections
/ui form registration \
  --sections=account,profile,preferences \
  --fields=email:email:required,password:password:required,name:text:required,bio:textarea:optional

# Contact form
/ui form contact --fields=name:text:required,email:email:required,message:textarea:required --submit=handleSubmit
```

---

### /ui wizard

Generate a multi-step wizard.

```bash
/ui wizard <name> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--steps` | number/string[] | 3 | Number or names of steps |
| `--progress` | string | bar | Progress indicator type |
| `--validation` | boolean | true | Validate before next |
| `--skip` | boolean | false | Allow skipping steps |
| `--animation` | string | slide | Transition animation |

**Examples:**

```bash
# Simple 3-step wizard
/ui wizard onboarding --steps=3

# Named steps wizard
/ui wizard checkout --steps=cart,shipping,payment,confirmation --progress=dots

# Onboarding with skip option
/ui wizard setup --steps=welcome,profile,preferences,complete --skip --animation=fade
```

---

### /ui dashboard

Generate a dashboard with widgets.

```bash
/ui dashboard <name> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--widgets` | string[] | - | Widget types to include |
| `--layout` | string | grid | Widget layout |
| `--sidebar` | boolean | true | Include navigation sidebar |
| `--responsive` | boolean | true | Make responsive |

**Widget Types:**

- `stats` - Statistics cards
- `chart` - Chart placeholder
- `table` - Data table
- `list` - Item list
- `calendar` - Calendar widget
- `activity` - Activity feed

**Examples:**

```bash
# Analytics dashboard
/ui dashboard analytics --widgets=stats,chart,table --sidebar

# User dashboard
/ui dashboard user --widgets=stats,activity,list --layout=masonry
```

---

### /ui animate

Add animations to existing code.

```bash
/ui animate <target> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--entrance` | string | fade | Entrance animation |
| `--exit` | string | - | Exit animation |
| `--hover` | string | - | Hover animation |
| `--stagger` | number | - | Stagger delay (ms) |
| `--library` | string | framer-motion | Animation library |

**Examples:**

```bash
# Add fade-in to a component
/ui animate ./src/components/Card.tsx --entrance=fadeUp --hover=lift

# Add staggered animation to a list
/ui animate ./src/components/ProductGrid.tsx --stagger=50 --entrance=slideIn

# Add page transitions
/ui animate ./src/pages --entrance=slideRight --exit=slideLeft
```

---

### /ui audit

Audit existing code for accessibility and quality.

```bash
/ui audit <target> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--level` | string | AA | WCAG level |
| `--fix` | boolean | false | Auto-fix issues |
| `--report` | string | - | Output report file |

**Examples:**

```bash
# Audit a component
/ui audit ./src/components/Button.tsx

# Audit and fix
/ui audit ./src/components --fix

# Generate report
/ui audit ./src --report=a11y-report.md
```

---

### /ui config

Configure generation settings.

```bash
/ui config [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--init` | boolean | false | Initialize config file |
| `--set` | string | - | Set a config value |
| `--get` | string | - | Get a config value |
| `--list` | boolean | false | List all settings |

**Examples:**

```bash
# Initialize configuration
/ui config --init

# Set framework
/ui config --set framework=react

# Set accessibility level
/ui config --set a11y.level=AAA

# List all settings
/ui config --list
```

---

## 2. /motion Commands

### /motion tokens

Generate a motion token system.

```bash
/motion tokens [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--output` | string | ./tokens | Output directory |
| `--format` | string | ts | Output format |
| `--library` | string | framer-motion | Target library |

**Examples:**

```bash
# Generate motion tokens
/motion tokens --output=./src/tokens

# Generate CSS custom properties
/motion tokens --format=css --output=./src/styles
```

**Output:**

```typescript
// motion-tokens.ts
export const motion = {
  duration: {
    instant: 0,
    fast: 120,
    normal: 240,
    slow: 400,
  },
  easing: {
    linear: [0, 0, 1, 1],
    easeOut: [0.16, 1, 0.3, 1],
    easeInOut: [0.65, 0, 0.35, 1],
  },
  // ...
};
```

---

### /motion add

Add animation to a component.

```bash
/motion add <animation> <target> [options]
```

**Animation Types:**

| Type | Description |
|------|-------------|
| `fadeIn` | Fade in from transparent |
| `fadeOut` | Fade out to transparent |
| `slideUp` | Slide up with fade |
| `slideDown` | Slide down with fade |
| `slideLeft` | Slide from left |
| `slideRight` | Slide from right |
| `scale` | Scale from small |
| `bounce` | Bouncy entrance |

**Examples:**

```bash
# Add fade in
/motion add fadeIn ./src/components/Modal.tsx

# Add slide up with custom duration
/motion add slideUp ./src/components/Toast.tsx --duration=300

# Add hover scale
/motion add scale ./src/components/Card.tsx --trigger=hover
```

---

### /motion audit

Audit motion for accessibility.

```bash
/motion audit <target> [options]
```

**Examples:**

```bash
# Audit motion accessibility
/motion audit ./src/components

# Check reduced motion support
/motion audit ./src --check=reduced-motion
```

---

## 3. /a11y Commands

### /a11y audit

Perform accessibility audit.

```bash
/a11y audit <target> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--level` | string | AA | WCAG level |
| `--rules` | string[] | all | Specific rules to check |
| `--format` | string | text | Output format |

**Examples:**

```bash
# Full audit
/a11y audit ./src/components

# Specific level
/a11y audit ./src --level=AAA

# Specific rules
/a11y audit ./src --rules=color-contrast,keyboard-nav
```

---

### /a11y fix

Auto-fix accessibility issues.

```bash
/a11y fix <target> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--severity` | string | all | Fix by severity |
| `--dry-run` | boolean | false | Preview changes |

**Examples:**

```bash
# Fix all issues
/a11y fix ./src/components

# Fix only critical issues
/a11y fix ./src --severity=critical

# Preview fixes
/a11y fix ./src --dry-run
```

---

### /a11y report

Generate accessibility report.

```bash
/a11y report [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--output` | string | - | Output file |
| `--format` | string | md | Report format |
| `--include-passed` | boolean | false | Include passed checks |

**Examples:**

```bash
# Generate markdown report
/a11y report --output=./docs/a11y-report.md

# Generate JSON for CI
/a11y report --format=json --output=./a11y.json
```

---

## 4. /design Commands

### /design tokens

Generate design tokens.

```bash
/design tokens [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--colors` | string[] | - | Color palette |
| `--spacing` | string | 4 | Base spacing unit |
| `--typography` | string | - | Typography scale |
| `--output` | string | ./tokens | Output directory |

**Examples:**

```bash
# Generate full token system
/design tokens --output=./src/design-system

# Generate with custom colors
/design tokens --colors=primary:#2563eb,secondary:#64748b
```

---

### /design component

Generate design system component.

```bash
/design component <name> [options]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--tokens` | string | ./tokens | Token source |
| `--docs` | boolean | true | Generate documentation |

**Examples:**

```bash
# Generate design system button
/design component button --docs

# Generate with custom tokens
/design component card --tokens=./src/design-system/tokens
```

---

### /design docs

Generate component documentation.

```bash
/design docs <target> [options]
```

**Examples:**

```bash
# Generate docs for all components
/design docs ./src/components

# Generate single component docs
/design docs ./src/components/Button.tsx
```

---

## 5. Command Aliases

For convenience, these aliases are available:

```bash
# Short aliases
/c = /ui component
/l = /ui layout
/f = /ui form
/w = /ui wizard
/d = /ui dashboard
/a = /ui animate
/m = /motion
```

**Usage:**

```bash
# These are equivalent:
/ui component button
/c button

# These are equivalent:
/motion add fadeIn ./Button.tsx
/m add fadeIn ./Button.tsx
```

---

## 6. Global Options

These options are available for all commands:

| Option | Type | Description |
|--------|------|-------------|
| `--help`, `-h` | boolean | Show help |
| `--verbose`, `-v` | boolean | Verbose output |
| `--quiet`, `-q` | boolean | Minimal output |
| `--dry-run` | boolean | Preview without changes |
| `--debug` | boolean | Debug mode |
| `--config` | string | Config file path |

---

## 7. Configuration File

Commands read from `.ui-gen.yaml` in the project root:

```yaml
# .ui-gen.yaml
version: 1

# Framework settings
framework: react
typescript: true
styling: tailwind

# Accessibility
accessibility:
  level: AA
  auto_fix: true

# Animation
animation:
  library: framer-motion
  preference: subtle
  reduced_motion: true

# Output
output:
  components: ./src/components
  hooks: ./src/hooks
  tokens: ./src/design-system/tokens

# Quality gates
quality:
  typescript_strict: true
  a11y_score: 90
  test_coverage: 80

# LLM settings (for agent system)
llm:
  provider: claude  # claude | openai | local
  model: claude-sonnet-4-20250514
  temperature: 0.7
  max_tokens: 10000
```

---

## 8. Environment Variables

```bash
# LLM Provider
export UI_GEN_LLM_PROVIDER=claude
export UI_GEN_LLM_MODEL=claude-sonnet-4-20250514

# Framework defaults
export UI_GEN_FRAMEWORK=react
export UI_GEN_STYLING=tailwind
export UI_GEN_TYPESCRIPT=true

# Accessibility
export UI_GEN_A11Y_LEVEL=AA

# Animation
export UI_GEN_ANIMATION_LIB=framer-motion

# Debug
export UI_GEN_DEBUG=false
export UI_GEN_VERBOSE=false
```

---

## 9. Interactive Mode

Start interactive mode for complex generation:

```bash
/ui interactive
```

Interactive mode provides:
- Step-by-step guidance
- Real-time preview
- Iterative refinement
- Quality feedback

---

## 10. Pipeline Integration

### GitHub Actions

```yaml
- name: Generate UI Components
  run: |
    /ui audit ./src/components --format=json > a11y-results.json
    if [ $(jq '.score' a11y-results.json) -lt 90 ]; then
      exit 1
    fi
```

### Pre-commit Hook

```bash
#!/bin/bash
# .husky/pre-commit

# Audit changed components
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(tsx|jsx)$')

if [ -n "$changed_files" ]; then
  /a11y audit $changed_files --format=json
fi
```

---

*Document Version: 1.0*
*Compatibility: Claude Code, Cursor, VS Code terminals*
*Last Updated: November 2025*
