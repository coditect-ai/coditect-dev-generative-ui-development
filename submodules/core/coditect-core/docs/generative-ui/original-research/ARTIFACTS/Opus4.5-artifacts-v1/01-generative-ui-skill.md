# Generative UI Skill

*SKILL.md for UI component and layout generation*

---

## Skill Metadata

```yaml
name: generative-ui
version: 2.0.0
description: Generate production-ready UI components, layouts, and applications
author: platform-team
category: code-generation
tags:
  - ui
  - react
  - typescript
  - accessibility
  - components
```

---

## Overview

This skill enables generation of production-quality UI code from natural language descriptions. It supports multiple frameworks, includes accessibility by default, and can generate complete component systems with animations.

---

## Capabilities

| Capability | Description | Complexity |
|------------|-------------|------------|
| `component` | Single UI component | Low |
| `layout` | Page layout with slots | Medium |
| `form` | Form with validation | Medium |
| `wizard` | Multi-step flow | High |
| `dashboard` | Dashboard with widgets | High |
| `design-system` | Component library | Very High |

---

## Usage

### Basic Component Generation

```bash
# Generate a button component
/ui component button --variant=primary,secondary,ghost --size=sm,md,lg

# Generate a card component
/ui component card --clickable --image --badges

# Generate an input with validation
/ui component input --type=text,email,password --validation --error-state
```

### Layout Generation

```bash
# Generate a dashboard layout
/ui layout dashboard --sidebar --topbar --responsive

# Generate a form layout
/ui layout form --steps=3 --progress --validation

# Generate a grid layout
/ui layout grid --cols=1,2,3,4 --responsive --gap=4
```

### Full Application

```bash
# Generate a settings page
/ui app settings --sections=profile,notifications,security

# Generate a product listing
/ui app product-listing --filters --sorting --pagination
```

---

## Configuration

### Framework Selection

```yaml
# .ui-gen.yaml
framework: react  # react | vue | svelte | html
typescript: true
styling: tailwind  # tailwind | css-modules | styled-components | vanilla
```

### Accessibility Settings

```yaml
accessibility:
  level: AA  # A | AA | AAA
  reduced_motion: true
  color_contrast: true
  focus_indicators: true
```

### Animation Settings

```yaml
animation:
  library: framer-motion  # framer-motion | css | none
  preference: subtle  # none | subtle | rich
  reduced_motion_fallback: true
```

---

## Prompt Templates

### Component Template

```
You are a senior {framework} + TypeScript engineer.
Generate a production-ready `{component_name}` component.

Requirements:
- Implement as a typed {framework} functional component in TypeScript.
- Props:
{props_list}
- Styling: {styling} utility classes.
- Accessibility:
  - Native semantic elements where possible.
  - ARIA attributes for custom patterns.
  - Keyboard navigation.
  - Visible focus states.
{additional_requirements}

Output only the complete TypeScript code. No explanations, no comments.
```

### Layout Template

```
You are a senior {framework} + TypeScript engineer and UX designer.
Build a `{layout_name}` layout component.

Requirements:
- {framework} + TypeScript functional components.
- Layout structure:
{structure_description}
- Responsive behavior:
{responsive_spec}
- Accessibility:
  - Proper landmarks (<nav>, <main>, <aside>).
  - Skip links if complex navigation.
  - Focus management for dynamic content.
- Styling: {styling}.

Output: Single TypeScript file with all components. No explanations.
```

### Animation Template

```
You are a senior {framework} + TypeScript engineer and motion UI specialist.
Add animations to this component using {animation_library}.

Component: {component_code}

Animation requirements:
- Entrance: {entrance_spec}
- Exit: {exit_spec}
- Interactions: {interaction_spec}
- Reduced motion: Respect prefers-reduced-motion.

Motion tokens to use:
- duration.fast: 120ms
- duration.normal: 240ms
- easing.out: cubic-bezier(0.16, 1, 0.3, 1)

Output the updated component code. No explanations.
```

---

## Output Structure

### Single Component

```
output/
├── {ComponentName}.tsx       # Main component
├── {ComponentName}.types.ts  # TypeScript types (if separate)
├── {ComponentName}.test.tsx  # Unit tests (if requested)
└── {ComponentName}.stories.tsx  # Storybook (if requested)
```

### Component Library

```
output/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.types.ts
│   │   └── index.ts
│   ├── Card/
│   └── Input/
├── hooks/
│   ├── useReducedMotion.ts
│   └── useFocusManagement.ts
├── tokens/
│   └── motion.ts
└── index.ts
```

---

## Quality Gates

### Required Checks

| Check | Threshold | Blocking |
|-------|-----------|----------|
| TypeScript strict | 100% | Yes |
| Accessibility score | ≥ 90 | Yes |
| No `any` types | 100% | Yes |
| Keyboard navigable | 100% | Yes |

### Recommended Checks

| Check | Threshold | Blocking |
|-------|-----------|----------|
| Test coverage | ≥ 80% | No |
| Bundle size | < 50KB | No |
| Lighthouse a11y | ≥ 95 | No |

---

## Integration with Claude Code

### Environment Variables

```bash
export UI_GEN_FRAMEWORK=react
export UI_GEN_STYLING=tailwind
export UI_GEN_A11Y_LEVEL=AA
export UI_GEN_ANIMATION=framer-motion
```

### Project Detection

The skill auto-detects project configuration from:

1. `package.json` dependencies
2. `tsconfig.json` presence
3. `tailwind.config.js` presence
4. `.ui-gen.yaml` explicit config

---

## Examples

### Example 1: Accessible Button

**Input:**
```
/ui component button with loading state and icons
```

**Output:** (truncated)
```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", size = "md", isLoading, ...props }, ref) => {
    // ... implementation
  }
);
```

### Example 2: Dashboard Layout

**Input:**
```
/ui layout dashboard with collapsible sidebar and user menu
```

**Output:** Multi-file component with:
- `DashboardLayout.tsx`
- `Sidebar.tsx`
- `TopBar.tsx`
- `UserMenu.tsx`

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Missing types | Ensure `typescript: true` in config |
| No animations | Check `animation.library` setting |
| Accessibility warnings | Review ARIA attributes in output |
| Large bundle | Enable tree-shaking, check imports |

### Debug Mode

```bash
/ui component button --debug
```

Outputs:
- Prompt sent to LLM
- Token usage
- Quality gate results
- Intermediate artifacts

---

## Version History

| Version | Changes |
|---------|---------|
| 2.0.0 | Multi-framework support, animation system |
| 1.5.0 | Added wizard and dashboard generators |
| 1.0.0 | Initial release with component generation |

---

*Skill Location: `/mnt/skills/user/generative-ui/SKILL.md`*
