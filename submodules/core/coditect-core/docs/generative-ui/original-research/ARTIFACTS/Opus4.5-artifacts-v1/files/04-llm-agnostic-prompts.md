# LLM-Agnostic Prompt Templates

*Portable prompts for any AI model - Claude, GPT-4, Gemini, Llama, etc.*

---

## Overview

These prompt templates are designed to work across different LLM providers. They use consistent structure and clear instructions that translate well between models. Variables are marked with `{variable_name}` syntax for easy substitution.

---

## 1. Template Architecture

### Universal Prompt Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL PROMPT STRUCTURE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ ROLE DEFINITION                                                  │   │
│  │ "You are a senior {role} engineer specializing in {domain}."   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ TASK SPECIFICATION                                               │   │
│  │ Clear description of what to generate, including:                │   │
│  │ - Component/artifact name                                        │   │
│  │ - Type and purpose                                               │   │
│  │ - Target framework                                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ REQUIREMENTS                                                     │   │
│  │ Structured list of:                                              │   │
│  │ - Functional requirements                                        │   │
│  │ - Props/API surface                                              │   │
│  │ - Behavior specifications                                        │   │
│  │ - Styling requirements                                           │   │
│  │ - Accessibility requirements                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ OUTPUT CONSTRAINTS                                               │   │
│  │ - Format (code only, JSON, etc.)                                 │   │
│  │ - Language/framework                                             │   │
│  │ - What to exclude (explanations, comments)                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Variable Reference

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `{component_name}` | Name of component | Button, Card, Modal |
| `{framework}` | Target framework | react, vue, svelte, html |
| `{styling}` | Styling approach | tailwind, css-modules, styled-components |
| `{a11y_level}` | Accessibility level | A, AA, AAA |
| `{variants}` | Component variants | primary, secondary, ghost |
| `{props}` | Component props | children, onClick, disabled |
| `{language}` | Programming language | TypeScript, JavaScript |

---

## 2. Component Generation Templates

### 2.1 Basic Component

```
You are a senior {framework} + {language} engineer.
Generate a production-ready `{component_name}` component.

Requirements:
- Implement as a typed {framework} functional component.
- Props:
{props_definition}
- Styling: Use {styling} utility classes.
- Accessibility:
  - Use native semantic HTML elements.
  - Include appropriate ARIA attributes.
  - Support keyboard navigation.
  - Provide visible focus indicators.

Output only the complete {language} code for the component.
Do not include explanations, comments, or markdown formatting.
```

**Example Instantiation:**

```
You are a senior React + TypeScript engineer.
Generate a production-ready `Button` component.

Requirements:
- Implement as a typed React functional component.
- Props:
  - variant: "primary" | "secondary" | "ghost" (default: "primary")
  - size: "sm" | "md" | "lg" (default: "md")
  - isLoading?: boolean
  - disabled?: boolean
  - children: React.ReactNode
  - Extend React.ButtonHTMLAttributes<HTMLButtonElement>
- Styling: Use Tailwind CSS utility classes.
- Accessibility:
  - Use native semantic HTML elements.
  - Include appropriate ARIA attributes.
  - Support keyboard navigation.
  - Provide visible focus indicators.

Output only the complete TypeScript code for the component.
Do not include explanations, comments, or markdown formatting.
```

### 2.2 Component with States

```
You are a senior {framework} + {language} engineer.
Generate a production-ready `{component_name}` component with multiple states.

Requirements:
- Implement as a typed {framework} functional component.
- Props:
{props_definition}
- States to handle:
{states_definition}
- Styling: {styling}
- Each state should have distinct visual representation.
- Transitions between states should be smooth.
- Accessibility:
  - Announce state changes to screen readers.
  - Maintain focus management across state changes.
  - Support reduced motion preferences.

Output only the complete {language} code.
No explanations, no markdown.
```

### 2.3 Compound Component

```
You are a senior {framework} + {language} engineer.
Generate a compound `{component_name}` component with sub-components.

Requirements:
- Implement as a compound component pattern.
- Main component: `{component_name}`
- Sub-components:
{subcomponents_definition}
- Use Context API for state sharing between components.
- Props for main component:
{props_definition}
- Styling: {styling}
- Accessibility:
  - Proper ARIA relationships between components.
  - Keyboard navigation across the compound structure.

Output the complete {language} code including all sub-components.
No explanations.
```

---

## 3. Layout Generation Templates

### 3.1 Page Layout

```
You are a senior {framework} + {language} engineer and UX designer.
Generate a `{layout_name}` layout component.

Requirements:
- {framework} + {language} functional components.
- Layout structure:
{structure_definition}
- Responsive behavior:
  - Mobile: {mobile_behavior}
  - Tablet: {tablet_behavior}
  - Desktop: {desktop_behavior}
- Slots/children areas:
{slots_definition}
- Accessibility:
  - Use proper landmark elements (<nav>, <main>, <aside>, <footer>).
  - Include skip links for keyboard users.
  - Manage focus appropriately.
- Styling: {styling}

Output: Single {language} file with all layout components.
No explanations.
```

### 3.2 Dashboard Layout

```
You are a senior {framework} + {language} engineer.
Generate a `DashboardLayout` component with sidebar navigation.

Requirements:
- {framework} + {language} functional components.
- Structure:
  - Collapsible sidebar with navigation items.
  - Top bar with title, search, and user menu slot.
  - Main content area as children slot.
  - Optional footer.
- Responsive behavior:
  - Desktop: Sidebar visible, collapsible to icons.
  - Tablet: Sidebar starts collapsed.
  - Mobile: Off-canvas sidebar with hamburger toggle.
- Props:
  - navItems: Array of {icon, label, href, active}
  - title: string
  - userMenu: ReactNode slot
  - children: ReactNode
- Accessibility:
  - <nav> landmark for sidebar.
  - aria-current="page" for active item.
  - Focus trap when mobile sidebar open.
  - Escape key closes mobile sidebar.
- Styling: {styling}

Output: Complete {language} code with all components.
No explanations.
```

### 3.3 Multi-Step Wizard Layout

```
You are a senior {framework} + {language} engineer.
Generate a `WizardLayout` component for multi-step flows.

Requirements:
- {framework} + {language} functional components.
- Structure:
  - Progress indicator (bar or steps).
  - Step content area.
  - Navigation buttons (Previous, Next, Skip).
- Props:
  - steps: Array of {id, title, component}
  - currentStep: number
  - onStepChange: (step: number) => void
  - onComplete: () => void
  - allowSkip?: boolean
- Behavior:
  - Validate step before advancing (via callback).
  - Support navigation via progress indicator clicks.
  - Animate step transitions.
- Accessibility:
  - aria-live region for step announcements.
  - Focus management on step change.
  - Progress indicator is screen reader friendly.
- Styling: {styling}

Output: Complete {language} code.
No explanations.
```

---

## 4. Form Generation Templates

### 4.1 Form with Validation

```
You are a senior {framework} + {language} engineer.
Generate a `{form_name}` form component with validation.

Requirements:
- {framework} + {language} functional component.
- Fields:
{fields_definition}
- Validation:
  - Use {validation_library} for schema validation.
  - Show inline error messages.
  - Validate on blur and on submit.
- Props:
  - onSubmit: (data: FormData) => void | Promise<void>
  - initialValues?: Partial<FormData>
  - isSubmitting?: boolean
- States:
  - Default (empty/filled).
  - Error (validation failed).
  - Success (submission complete).
  - Loading (during submit).
- Accessibility:
  - Label all inputs with associated <label> elements.
  - Use aria-describedby for error messages.
  - aria-invalid="true" for invalid fields.
  - Announce errors to screen readers.
- Styling: {styling}

Output: Complete {language} code including form schema.
No explanations.
```

### 4.2 Dynamic Form Builder

```
You are a senior {framework} + {language} engineer.
Generate a `DynamicForm` component that renders forms from a schema.

Requirements:
- {framework} + {language} functional component.
- Accept a form schema defining fields:
  - Field types: text, email, password, number, select, checkbox, radio, textarea
  - Validation rules: required, min, max, pattern, custom
  - Conditional visibility based on other field values
- Props:
  - schema: FormSchema
  - onSubmit: (data: Record<string, any>) => void
  - onChange?: (data: Record<string, any>) => void
- Features:
  - Render appropriate input component for each field type.
  - Handle nested field groups.
  - Support field arrays (add/remove items).
- Accessibility:
  - All inputs properly labeled.
  - Error announcements.
  - Logical tab order.
- Styling: {styling}

Output: Complete {language} code including schema types.
No explanations.
```

---

## 5. Animation Templates

### 5.1 Motion Token System

```
You are a senior {framework} + {language} engineer specializing in motion design.
Generate a motion token system for UI animations.

Requirements:
- Create a typed token object with:
  - Durations: instant (0ms), fast (120ms), normal (240ms), slow (400ms), slower (600ms)
  - Easings: linear, easeOut, easeIn, easeInOut (as cubic-bezier arrays)
  - Distances: xs (4px), sm (8px), md (16px), lg (24px), xl (32px)
- Include pre-built animation variants for {animation_library}:
  - fadeIn / fadeOut
  - slideUp / slideDown
  - slideLeft / slideRight
  - scale
  - stagger container
- Include CSS custom properties version for non-JS usage.
- Include reduced motion media query support.

Output: Complete {language} code as a single module.
No explanations.
```

### 5.2 Animated Component Wrapper

```
You are a senior {framework} + {language} engineer and motion specialist.
Generate an `AnimatedContainer` component using {animation_library}.

Requirements:
- {framework} + {language} functional component.
- Props:
  - children: ReactNode
  - animation: "fadeIn" | "slideUp" | "slideRight" | "scale" (default: "fadeIn")
  - delay?: number (milliseconds)
  - duration?: number (milliseconds)
  - stagger?: boolean (for children animation)
  - staggerDelay?: number (milliseconds between children)
  - className?: string
- Behavior:
  - Respect prefers-reduced-motion system preference.
  - Use motion tokens for consistent timing.
  - Exit animations when unmounting.
- Accessibility:
  - No motion that could cause discomfort.
  - Instant transitions for reduced motion users.

Output: Complete {language} code.
No explanations.
```

### 5.3 Page Transition

```
You are a senior {framework} + {language} engineer.
Generate a `PageTransition` component for route transitions.

Requirements:
- {framework} + {language} functional component.
- Props:
  - children: ReactNode
  - transitionKey: string | number (unique per page)
  - direction?: "forward" | "backward"
- Transitions:
  - Forward navigation: Current page slides left, new page slides from right.
  - Backward navigation: Reverse of forward.
  - Duration: 240ms with easeOut.
- Use AnimatePresence (or equivalent) for exit animations.
- Accessibility:
  - Respect reduced motion preference.
  - Maintain focus after transition.

Output: Complete {language} code.
No explanations.
```

---

## 6. Accessibility Templates

### 6.1 Accessible Modal

```
You are a senior {framework} + {language} engineer specializing in accessibility.
Generate an accessible `Modal` component following WAI-ARIA patterns.

Requirements:
- {framework} + {language} functional component.
- Props:
  - isOpen: boolean
  - onClose: () => void
  - title: string
  - description?: string
  - children: ReactNode
  - size?: "sm" | "md" | "lg" | "full"
  - closeOnOverlayClick?: boolean (default: true)
  - closeOnEscape?: boolean (default: true)
- Accessibility (MUST implement all):
  - role="dialog" with aria-modal="true"
  - aria-labelledby pointing to title
  - aria-describedby pointing to description (if provided)
  - Focus trap: Tab cycles within modal
  - Focus return: Return focus to trigger element on close
  - Escape key closes modal
  - Body scroll lock when open
- Styling: {styling}

Output: Complete {language} code including focus trap hook.
No explanations.
```

### 6.2 Accessible Tabs

```
You are a senior {framework} + {language} engineer specializing in accessibility.
Generate an accessible `Tabs` component following WAI-ARIA tabs pattern.

Requirements:
- {framework} + {language} functional component.
- Props:
  - tabs: Array of {id, label, content, disabled?}
  - defaultTab?: string
  - onChange?: (tabId: string) => void
  - orientation?: "horizontal" | "vertical"
- Accessibility (MUST implement all):
  - role="tablist" on tab container
  - role="tab" on each tab trigger
  - role="tabpanel" on each content panel
  - aria-selected="true/false" on tabs
  - aria-controls linking tab to panel
  - aria-labelledby linking panel to tab
  - Keyboard navigation:
    - Arrow keys move between tabs
    - Home/End go to first/last tab
    - Enter/Space activate tab
    - Tab key moves to panel content
- Styling: {styling}

Output: Complete {language} code.
No explanations.
```

### 6.3 Skip Link Component

```
You are a senior {framework} + {language} engineer specializing in accessibility.
Generate a `SkipLink` component for keyboard navigation.

Requirements:
- {framework} + {language} functional component.
- Props:
  - links: Array of {id, label} for skip targets
- Behavior:
  - Hidden until focused (visually hidden, not display:none).
  - Appears at top of viewport on focus.
  - Clicking/pressing Enter moves focus to target.
- Accessibility:
  - First focusable element on page.
  - Clear visual indication when focused.
  - Proper focus management on activation.
- Styling: {styling}

Output: Complete {language} code.
No explanations.
```

---

## 7. Data Display Templates

### 7.1 Data Table

```
You are a senior {framework} + {language} engineer.
Generate a `DataTable` component with sorting and selection.

Requirements:
- {framework} + {language} functional component.
- Props:
  - columns: Array of {key, header, sortable?, render?}
  - data: Array of row objects
  - onSort?: (key: string, direction: "asc" | "desc") => void
  - selectable?: boolean
  - onSelectionChange?: (selectedIds: string[]) => void
  - emptyMessage?: string
- Features:
  - Sortable columns with visual indicators.
  - Row selection with checkbox column.
  - Select all checkbox in header.
  - Empty state display.
- Accessibility:
  - Proper <table> markup with <thead>, <tbody>.
  - scope attributes on headers.
  - aria-sort on sortable columns.
  - Row selection announced to screen readers.
- Styling: {styling}

Output: Complete {language} code.
No explanations.
```

### 7.2 Card Grid

```
You are a senior {framework} + {language} engineer.
Generate a `CardGrid` component for displaying card collections.

Requirements:
- {framework} + {language} functional component.
- Props:
  - items: Array of {id, title, description, image?, metadata?}
  - columns: {sm: number, md: number, lg: number, xl: number}
  - gap?: number
  - onItemClick?: (id: string) => void
  - renderItem?: (item) => ReactNode (custom render)
- Features:
  - Responsive column layout.
  - Loading skeleton state.
  - Empty state.
- Accessibility:
  - List semantics (role="list", role="listitem").
  - Clickable cards are keyboard accessible.
  - Images have alt text.
- Styling: {styling}

Output: Complete {language} code.
No explanations.
```

---

## 8. Utility Templates

### 8.1 Custom Hook: Reduced Motion

```
You are a senior {framework} + {language} engineer.
Generate a `useReducedMotion` hook for detecting motion preferences.

Requirements:
- {framework} + {language} custom hook.
- Behavior:
  - Return boolean indicating prefers-reduced-motion.
  - Update on system preference change.
  - SSR-safe (default to false on server).
- Usage example:
  ```
  const prefersReducedMotion = useReducedMotion();
  // Use to disable or simplify animations
  ```

Output: Complete {language} code.
No explanations.
```

### 8.2 Custom Hook: Focus Management

```
You are a senior {framework} + {language} engineer.
Generate focus management hooks for accessible components.

Requirements:
- Generate two hooks:
  1. `useFocusTrap(ref)`: Trap focus within an element.
  2. `useFocusReturn()`: Store and return focus to previous element.
- Behavior for useFocusTrap:
  - Find all focusable elements within container.
  - Tab cycles through only those elements.
  - Shift+Tab cycles backward.
- Behavior for useFocusReturn:
  - On mount, store currently focused element.
  - On unmount, return focus to stored element.
- SSR-safe implementations.

Output: Complete {language} code for both hooks.
No explanations.
```

### 8.3 Custom Hook: Media Query

```
You are a senior {framework} + {language} engineer.
Generate a `useMediaQuery` hook for responsive behavior.

Requirements:
- {framework} + {language} custom hook.
- Props:
  - query: string (CSS media query)
- Return:
  - matches: boolean
- Behavior:
  - Return current match state.
  - Update on viewport/preference changes.
  - SSR-safe (default to false on server).
- Include helper hooks:
  - `useIsMobile()` - matches "(max-width: 640px)"
  - `useIsTablet()` - matches "(min-width: 641px) and (max-width: 1024px)"
  - `useIsDesktop()` - matches "(min-width: 1025px)"

Output: Complete {language} code for all hooks.
No explanations.
```

---

## 9. Template Composition

### Combining Templates

For complex components, compose multiple templates:

```
{role_definition}

{task_definition}

Requirements:

## Functional Requirements
{functional_requirements}

## Props/API
{props_definition}

## Accessibility Requirements
{accessibility_requirements}

## Animation Requirements
{animation_requirements}

## Styling Requirements
{styling_requirements}

{output_constraints}
```

### Template Chaining

For iterative generation:

```
Step 1: Generate base component
→ Use "Basic Component" template

Step 2: Add animation
→ Use "Animated Component Wrapper" template with Step 1 output

Step 3: Add accessibility audit
→ Use "Accessibility Audit" template with Step 2 output

Step 4: Generate tests
→ Use "Component Tests" template with Step 3 output
```

---

## 10. Provider-Specific Adjustments

### Claude Adjustments

Claude works well with:
- Detailed, structured prompts
- Explicit output constraints
- XML-style tags for structure (optional)

```
<task>
Generate a Button component...
</task>

<requirements>
- Variant support...
</requirements>

<output>
Only TypeScript code, no explanations.
</output>
```

### GPT-4 Adjustments

GPT-4 works well with:
- System/user message separation
- JSON output mode for structured responses
- Clear role definition in system message

### Gemini Adjustments

Gemini works well with:
- Multimodal inputs (image + text for design-to-code)
- Structured output specifications
- Step-by-step reasoning prompts

### Local Models (Llama, Mistral)

Local models may need:
- Simpler, more direct prompts
- Fewer requirements per prompt
- Multiple passes for complex components
- Lower temperature for code generation

---

*Document Version: 1.0*
*Compatibility: Claude, GPT-4, Gemini, Llama, Mistral, and other instruction-following models*
*Last Updated: November 2025*
