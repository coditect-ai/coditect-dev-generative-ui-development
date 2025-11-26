# Prompt Engineering Patterns for Generative UI

*Production-ready prompt templates for Gemini/AI Studio UI generation*

---

## Overview

This document provides a comprehensive library of prompt patterns for generating production-quality UI components using Google's Generative UI capabilities. Each pattern includes the prompt structure, expected output characteristics, and optimization guidelines.

---

## 1. Foundational Prompt Architecture

### 1.1 Universal Prompt Structure

Every effective generative UI prompt follows this structure:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROMPT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│  1. ROLE SPECIFICATION                                          │
│     "You are a senior [framework] + [language] engineer..."    │
│                                                                 │
│  2. TASK DEFINITION                                             │
│     "Generate a [component type] component named [name]..."    │
│                                                                 │
│  3. REQUIREMENTS BLOCK                                          │
│     - Functional requirements                                   │
│     - Props/API surface                                         │
│     - Styling approach                                          │
│     - Accessibility requirements                                │
│                                                                 │
│  4. OUTPUT CONSTRAINTS                                          │
│     "Output only [format]. No explanations, no comments..."    │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Role Specification Variants

```markdown
# For component-level generation
"You are a senior React + TypeScript engineer."

# For design system components
"You are a senior React + TypeScript engineer and design system architect."

# For animated UI
"You are a senior React + TypeScript engineer and motion UI specialist."

# For full applications
"You are a senior full-stack engineer specializing in [framework]."

# For accessibility-focused
"You are a senior React accessibility engineer with WCAG expertise."
```

---

## 2. Component Generation Patterns

### 2.1 Pattern: Simple Component with Props

**Use Case:** Basic reusable components (buttons, inputs, cards)

```markdown
You are a senior React + TypeScript engineer.
Generate a production-ready, reusable `[ComponentName]` component.

Requirements:
- Implement as a typed React functional component in TypeScript.
- Props:
  - `[prop1]: [type]` - [description]
  - `[prop2]?: [type]` - [description] (default: [value])
  - Extend `React.[HTMLElement]Attributes<HTML[Element]Element>`.
- Styling:
  - Use Tailwind CSS utility classes.
  - [Specific styling requirements]
- Accessibility:
  - [ARIA requirements]
  - Keyboard navigation support.
  - Visible focus states.

Output only the complete TypeScript code. No explanations, no comments.
```

**Example - Button Component:**

```markdown
You are a senior React + TypeScript engineer.
Generate a production-ready, reusable `Button` component.

Requirements:
- Implement as a typed React functional component in TypeScript.
- Props:
  - `variant: "primary" | "secondary" | "ghost"` - visual style
  - `size?: "sm" | "md" | "lg"` - size variant (default: "md")
  - `fullWidth?: boolean` - stretch to 100% width
  - `isLoading?: boolean` - show spinner and disable
  - `leftIcon?: React.ReactNode` - icon before label
  - `rightIcon?: React.ReactNode` - icon after label
  - Extend `React.ButtonHTMLAttributes<HTMLButtonElement>`.
- Styling:
  - Use Tailwind CSS utility classes.
  - Touch-friendly padding (min 44px tap target).
  - Responsive typography scaling.
- Accessibility:
  - Native `<button>` with `type="button"` default.
  - `aria-busy="true"` when loading.
  - `aria-disabled="true"` when disabled/loading.
  - Visible focus ring meeting WCAG contrast.

Output only the complete TypeScript code. No explanations, no comments.
```

### 2.2 Pattern: Data Display Component

**Use Case:** Cards, lists, tables, grids

```markdown
You are a senior React + TypeScript engineer and UX designer.
Build a self-contained `[ComponentName]` that displays data.

Requirements:
- React + TypeScript functional components.
- Data model: `[TypeName] { [field]: [type]; ... }`.
- UI layout:
  - [Layout description]
  - Responsive: [breakpoint behaviors]
- Behavior:
  - [Interactivity requirements]
  - [State management approach]
- Accessibility:
  - [Semantic structure]
  - [Keyboard navigation]
- Styling:
  - Use Tailwind CSS utility classes.

Output: A single TypeScript file with sample data defined inline. No explanations.
```

**Example - Product Grid:**

```markdown
You are a senior React + TypeScript engineer and UX designer.
Build a self-contained `ProductGrid` that displays product cards.

Requirements:
- React + TypeScript functional components.
- Data model: `Product { id: string; name: string; price: number; imageUrl: string; category: string; }`.
- UI layout:
  - Responsive grid: 1 col mobile, 2 tablet, 3 desktop.
  - Each card shows image, name, formatted price, category badge.
- Behavior:
  - Optional `onProductClick` callback.
  - Hover state with subtle shadow.
- Accessibility:
  - `<article>` for each card.
  - Image alt text from product name.
  - Focus-within ring for keyboard navigation.
- Styling:
  - Use Tailwind CSS utility classes.
  - Light theme with subtle shadows.

Output: A single TypeScript file with 6 sample products. No explanations.
```

### 2.3 Pattern: Interactive Filter Component

**Use Case:** Search bars, filter panels, faceted navigation

```markdown
You are a senior React + TypeScript engineer.
Generate an interactive `[ComponentName]` with filter capabilities.

Requirements:
- React + TypeScript with controlled state.
- Filter types:
  - [List filter types: search, dropdown, toggle, range, etc.]
- Behavior:
  - Filters combine with AND logic.
  - Debounced search input ([ms] delay).
  - Clear all filters button.
  - "No results" empty state.
- Accessibility:
  - Proper roles for filter controls.
  - `aria-describedby` for filter counts.
  - Keyboard navigation between filters.
- Styling:
  - Tailwind CSS, horizontal filter bar layout.
  - Mobile: stacked vertical filters.

Output: Complete TypeScript file with inline mock data. No explanations.
```

---

## 3. Layout Generation Patterns

### 3.1 Pattern: Dashboard Layout

```markdown
You are a senior React + TypeScript engineer.
Generate a responsive `DashboardLayout` component.

Requirements:
- React + TypeScript functional components.
- Layout structure:
  - Left sidebar: logo, nav items, collapse toggle.
  - Top bar: page title, search, user menu.
  - Main content area: slot for page content.
- Responsive behavior:
  - Desktop: full sidebar visible.
  - Tablet: collapsible sidebar (icons only when collapsed).
  - Mobile: off-canvas sidebar with hamburger toggle.
- Accessibility:
  - `<nav>` landmark for sidebar.
  - `aria-current="page"` for active nav item.
  - Focus trap when mobile sidebar open.
- Styling:
  - Tailwind CSS, light theme.
  - Subtle shadows and borders.

Output: Single TypeScript file with `DashboardLayout` and mock nav items.
```

### 3.2 Pattern: Multi-Step Wizard

```markdown
You are a senior React + TypeScript engineer.
Create a multi-step wizard component `[WizardName]`.

Requirements:
- React + TypeScript with hooks for state.
- Steps: [List steps with descriptions]
- Step component structure:
  - Each step as separate component.
  - Shared state via props or context.
- Navigation:
  - Next/Previous buttons.
  - Step indicator (progress bar or dots).
  - Validation before advancing.
- Behavior:
  - Disable "Next" until step is valid.
  - Show validation errors inline.
  - Final step shows summary.
- Accessibility:
  - `aria-live="polite"` for step changes.
  - Focus management on navigation.
  - Error announcements.
- Styling:
  - Tailwind CSS, centered card layout.
  - Mobile: full-width steps.

Output: Single TypeScript file with all components. No explanations.
```

---

## 4. Animation Specification Patterns

### 4.1 Pattern: Animated Onboarding Flow

```markdown
You are a senior React + TypeScript engineer and motion UI specialist.
Generate a multi-screen onboarding flow with animations.

Requirements:
- React + TypeScript functional components.
- Animation library: `framer-motion`.
- Screens: [List 3-4 screens with purpose]
- Animation specifications:
  - Screen transitions:
    - Forward: current slides left + fades, next slides from right
    - Backward: reverse direction
    - Duration: 240ms, easing: ease-out
  - Element entrances:
    - Staggered reveal (title, then body, then buttons)
    - Delay: 50ms between elements
  - Micro-interactions:
    - Button hover: scale(1.02), 120ms
    - Button press: scale(0.98), 80ms
  - Progress indicator:
    - Animated width change, 200ms
- Reduced motion:
  - Respect `prefers-reduced-motion`.
  - Fall back to instant transitions.
- Accessibility:
  - Focus management on step change.
  - ARIA labels for progress.

Output: Single TypeScript file with all components. No comments.
```

### 4.2 Motion Token System

```markdown
You are a senior React + TypeScript engineer.
Generate a motion token system and animated component.

Requirements:
- Define motion tokens as TypeScript constants:
  ```
  motion.duration.fast = 120ms
  motion.duration.normal = 240ms
  motion.duration.slow = 400ms
  motion.easing.out = cubic-bezier(0.16, 1, 0.3, 1)
  motion.easing.inOut = cubic-bezier(0.65, 0, 0.35, 1)
  ```
- Create a `motion` utility object mapping tokens.
- Implement `AnimatedCard` component using tokens:
  - Entrance: fade + slide up 16px, duration.normal, easing.out
  - Hover: translateY(-4px) + shadow, duration.fast
  - Exit: fade + scale down to 0.95

Output: TypeScript file with tokens object and component. No explanations.
```

---

## 5. Design-to-Code Patterns

### 5.1 Pattern: Mockup to Component

```markdown
You are a senior React + TypeScript engineer.
Convert the following design specification into a React component.

Design specification:
- [Paste detailed design spec here]
- Layout: [Describe spatial arrangement]
- Colors: [List color tokens or values]
- Typography: [Font sizes, weights, line heights]
- Spacing: [Padding, margins, gaps]
- States: [Hover, focus, disabled, loading]

Requirements:
- React + TypeScript functional component.
- Use Tailwind CSS for styling.
- Match the design specification exactly.
- Include all interactive states.
- Accessibility: [ARIA requirements]

Output: Complete TypeScript component code. No explanations.
```

### 5.2 Pattern: Design System Component

```markdown
You are a senior design system engineer.
Generate a `[ComponentName]` following design system patterns.

Design system context:
- Token prefix: `[prefix]-` (e.g., `ds-`)
- Color palette: primary, secondary, neutral, semantic
- Typography scale: xs, sm, base, lg, xl, 2xl
- Spacing scale: 0, 1, 2, 3, 4, 6, 8, 12, 16 (4px base)
- Border radius: none, sm, md, lg, full
- Shadow: none, sm, md, lg

Component requirements:
- Name: `[ComponentName]`
- Variants: [List variants]
- Props: [List props with types]
- Composition: [How it composes with other components]

Output: TypeScript component with design system tokens. No explanations.
```

---

## 6. Accessibility-First Patterns

### 6.1 Pattern: Screen Reader Optimized

```markdown
You are a senior accessibility engineer.
Generate an accessible `[ComponentName]` optimized for screen readers.

Requirements:
- Semantic HTML structure.
- ARIA attributes:
  - Role: [Specify if non-standard]
  - States: [aria-expanded, aria-selected, etc.]
  - Properties: [aria-label, aria-describedby, etc.]
  - Live regions: [For dynamic content]
- Focus management:
  - Logical tab order.
  - Focus trap for modals.
  - Return focus on close.
- Keyboard navigation:
  - [List supported keys and actions]
- Screen reader announcements:
  - [What should be announced when]

Output: TypeScript component with comprehensive accessibility. No explanations.
```

### 6.2 Pattern: WCAG AAA Compliance

```markdown
You are a senior accessibility engineer specializing in WCAG compliance.
Generate a `[ComponentName]` meeting WCAG 2.1 AAA standards.

Requirements:
- Color contrast: minimum 7:1 for text.
- Target size: minimum 44x44px for touch.
- Focus indicators: 3px solid with offset.
- Animation:
  - Respect `prefers-reduced-motion`.
  - No content that flashes >3 times/second.
- Text:
  - Support 200% zoom without horizontal scroll.
  - Line height minimum 1.5.
  - Paragraph spacing minimum 2x font size.
- Timing:
  - No time limits or provide extension.
  - Session timeout warnings.

Output: TypeScript component meeting AAA requirements. No explanations.
```

---

## 7. Storybook Integration Patterns

### 7.1 Pattern: Component + Stories

```markdown
You are a senior React + TypeScript engineer with Storybook expertise.
Generate a `[ComponentName]` and its Storybook stories.

Component requirements:
- [Props and behavior as in other patterns]

Storybook requirements:
- CSF 3.0 format.
- Stories for:
  - Default state
  - All variants
  - All sizes
  - Interactive states (hover, focus, active)
  - Loading state
  - Disabled state
  - Edge cases (long text, empty data)
- Args for interactive controls.
- argTypes for documentation.

Output two files in sequence:
1. `[ComponentName].tsx` - component code
2. `[ComponentName].stories.tsx` - Storybook stories

No explanations or comments.
```

---

## 8. Framework-Specific Patterns

### 8.1 Next.js App Router Component

```markdown
You are a senior Next.js engineer.
Generate a server component `[ComponentName]` for Next.js App Router.

Requirements:
- Server component by default (no 'use client').
- Data fetching: [async/await pattern]
- Streaming: Suspense boundaries for loading.
- Error handling: error.tsx integration.
- Metadata: generateMetadata if page-level.
- Styling: Tailwind CSS.

Output: TypeScript component for app/ directory. No explanations.
```

### 8.2 Flutter Widget

```markdown
You are a senior Flutter engineer.
Generate a `[WidgetName]` widget for Flutter.

Requirements:
- StatelessWidget or StatefulWidget as appropriate.
- Properties: [List with types]
- Theming: Use Theme.of(context) for colors/typography.
- Responsiveness: LayoutBuilder for breakpoints.
- Platform-aware: Cupertino vs Material where appropriate.
- Accessibility: Semantics widgets for screen readers.

Output: Complete Dart code for the widget. No explanations.
```

---

## 9. Prompt Chaining Strategies

### 9.1 Iterative Refinement Chain

```
Step 1: Generate basic component structure
Step 2: Add accessibility features
Step 3: Add animation specifications
Step 4: Add responsive behaviors
Step 5: Generate Storybook stories
Step 6: Generate unit tests
```

### 9.2 Design-to-Production Chain

```
Step 1: Analyze design spec → extract requirements
Step 2: Generate component skeleton
Step 3: Implement styling
Step 4: Add interactivity
Step 5: Implement accessibility
Step 6: Add error states and edge cases
Step 7: Generate documentation
```

---

## 10. Anti-Patterns to Avoid

### 10.1 Prompt Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Vague requirements | Inconsistent output | Explicit specs for each aspect |
| Missing accessibility | Inaccessible components | Include a11y in every prompt |
| No output constraints | Explanations mixed with code | "No explanations, no comments" |
| Single massive prompt | Token overflow, quality drop | Chain smaller focused prompts |
| Missing types | Runtime errors | Require TypeScript types |

### 10.2 Output Anti-Patterns to Reject

- Components using `any` type extensively
- Missing keyboard navigation
- Hardcoded colors instead of design tokens
- No error boundaries
- Missing loading states
- No empty state handling

---

## 11. Quality Checklist

Use this checklist to validate generated output:

```markdown
□ TypeScript types for all props
□ Default values for optional props
□ Native HTML elements where appropriate
□ ARIA attributes for non-native patterns
□ Keyboard navigation implemented
□ Focus states visible
□ Loading state handled
□ Error state handled
□ Empty state handled
□ Responsive breakpoints
□ Design tokens used (not magic numbers)
□ No accessibility violations
□ Reduced motion support
□ Touch-friendly targets (44px+)
```

---

*Document Version: 1.0*
*Compatible with: Gemini Pro, Gemini Ultra, AI Studio, Vertex AI*
*Last Updated: November 2025*
