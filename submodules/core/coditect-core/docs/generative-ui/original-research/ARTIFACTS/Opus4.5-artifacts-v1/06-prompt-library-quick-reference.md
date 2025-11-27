# Generative UI Prompt Library

*Copy-paste ready prompts for UI generation*

---

## Quick Reference

| Category | Prompt Prefix | Use Case |
|----------|---------------|----------|
| Component | `You are a senior React + TypeScript engineer...` | Single components |
| Layout | `You are a senior React + TypeScript engineer and UX designer...` | Page layouts |
| Animation | `You are a senior React + TypeScript engineer and motion UI specialist...` | Animated UIs |
| Accessibility | `You are a senior accessibility engineer...` | WCAG compliance |
| Design | `You are a senior product designer...` | Design specs |

---

## 1. Component Prompts

### 1.1 Button Component

```
You are a senior React + TypeScript engineer.
Generate a production-ready, reusable `Button` component.

Requirements:
- Implement as a typed React functional component in TypeScript.
- Props:
  - `variant: "primary" | "secondary" | "ghost"`
  - `size?: "sm" | "md" | "lg"` (default: "md")
  - `fullWidth?: boolean`
  - `isLoading?: boolean`
  - `leftIcon?: React.ReactNode`
  - `rightIcon?: React.ReactNode`
  - Extend `React.ButtonHTMLAttributes<HTMLButtonElement>`.
- Styling: Tailwind CSS, touch-friendly padding, responsive typography.
- Accessibility:
  - Native `<button>` with `type="button"` default.
  - `aria-busy="true"` when loading.
  - Visible focus ring, keyboard operable.

Output only the complete TypeScript code. No explanations, no comments.
```

### 1.2 Search Bar

```
You are a senior React + TypeScript engineer.
Generate a responsive `SearchBar` component with debounce.

Requirements:
- React + TypeScript functional component.
- Props:
  - `placeholder?: string`
  - `onSearch: (query: string) => void`
  - `debounceMs?: number` (default: 300)
  - `isLoading?: boolean`
- Features:
  - Debounced search callback.
  - Clear button when input has value.
  - Loading spinner when `isLoading` is true.
- Accessibility:
  - `role="search"` on form.
  - `aria-label` on input.
  - Clear button has accessible name.
- Styling: Tailwind CSS, max-width: 480px.

Output only the complete TypeScript code. No explanations.
```

### 1.3 Card Component

```
You are a senior React + TypeScript engineer.
Generate a versatile `Card` component.

Requirements:
- React + TypeScript functional component.
- Props:
  - `children: React.ReactNode`
  - `variant?: "elevated" | "outlined" | "filled"`
  - `padding?: "none" | "sm" | "md" | "lg"`
  - `onClick?: () => void` (makes card clickable)
  - `as?: "div" | "article" | "section"`
- Features:
  - Hover effect when clickable.
  - Focus ring when focused.
  - Polymorphic element via `as` prop.
- Styling: Tailwind CSS, rounded corners, subtle shadows.

Output only the complete TypeScript code. No explanations.
```

---

## 2. Layout Prompts

### 2.1 Product Grid

```
You are a senior React + TypeScript engineer and UX designer.
Build a `ProductGrid` that displays product cards.

Requirements:
- React + TypeScript functional components.
- Data model: `Product { id: string; name: string; price: number; imageUrl: string; category: string; }`
- UI layout:
  - Responsive grid: 1 col mobile, 2 tablet, 3 desktop.
  - Each card shows image, name, formatted price, category badge.
  - "View Details" button.
- Behavior:
  - `onProductClick?: (productId: string) => void`.
  - Hover state with elevated shadow.
  - Empty state with message.
- Accessibility:
  - `<article>` for each card.
  - Proper alt text on images.
  - Focus-within ring.
- Styling: Tailwind CSS, light theme.

Output: Single TypeScript file with 6 sample products. No explanations.
```

### 2.2 Dashboard Layout

```
You are a senior React + TypeScript engineer.
Generate a responsive `DashboardLayout` component.

Requirements:
- React + TypeScript functional components.
- Layout:
  - Left sidebar: logo, nav items, collapse toggle.
  - Top bar: page title, search, user menu slot.
  - Main content: slot for page content.
- Responsive:
  - Desktop: full sidebar visible.
  - Tablet: collapsible to icons.
  - Mobile: off-canvas with hamburger.
- Accessibility:
  - `<nav>` landmark for sidebar.
  - `aria-current="page"` for active item.
  - Focus management on sidebar toggle.
- Styling: Tailwind CSS, subtle shadows.

Output: Single TypeScript file with mock nav items. No explanations.
```

### 2.3 Multi-Step Wizard

```
You are a senior React + TypeScript engineer.
Create a multi-step `ProjectWizard` component.

Requirements:
- React + TypeScript with hooks.
- Steps:
  1. Project details (name, description, type).
  2. Team (add/remove members with name + role).
  3. Review & submit.
- Navigation:
  - Next/Previous buttons.
  - Step indicator with progress bar.
  - Validation before advancing.
- Behavior:
  - Disable "Next" if invalid.
  - Inline validation errors.
  - Final step shows summary.
- Accessibility:
  - `aria-live="polite"` for step changes.
  - Focus heading on step change.
  - Error announcements.
- Styling: Tailwind CSS, centered card layout.

Output: Single TypeScript file with all components. No explanations.
```

---

## 3. Filter & Search Prompts

### 3.1 Filterable Item Grid

```
You are a senior React + TypeScript engineer and UX designer.
Build a `FilterableItemGrid` with filters and grid.

Requirements:
- React + TypeScript functional components.
- Data model: `Item { id: string; title: string; category: "design" | "engineering" | "product"; difficulty: "beginner" | "intermediate" | "advanced"; description: string; }`
- Filter bar:
  - Category tabs (All, Design, Engineering, Product).
  - Difficulty dropdown.
  - Search input.
- Grid:
  - Responsive: 1 col mobile, 2 tablet, 3 desktop.
  - Cards with title, category badge, difficulty, description.
- Behavior:
  - Filters combine with AND logic.
  - "No results" empty state with "Clear filters" button.
- Accessibility:
  - Proper roles for tabs and dropdown.
  - Keyboard navigation.
- Styling: Tailwind CSS.

Output: Single TypeScript file with sample items. No explanations.
```

---

## 4. Animation Prompts

### 4.1 Animated Onboarding Flow

```
You are a senior React + TypeScript engineer and motion UI specialist.
Generate a multi-screen onboarding flow with animations.

Requirements:
- React + TypeScript, use `framer-motion`.
- Screens:
  1. Welcome with product value props.
  2. Personalization preferences.
  3. Feature toggles.
  4. "You're all set" confirmation.
- Animations:
  - Screen transitions: slide horizontally (240ms, ease-out).
  - Staggered element entrance (50ms between).
  - Button hover: scale(1.02), 120ms.
  - Progress bar: animated width.
- Reduced motion: Respect `prefers-reduced-motion`.
- Accessibility:
  - Focus management on step change.
  - ARIA labels for progress.
- Styling: Tailwind CSS, centered card on desktop.

Output: Single TypeScript file with all components. No comments.
```

### 4.2 Motion Token System

```
You are a senior React + TypeScript engineer.
Generate a motion token system and animated component.

Requirements:
- Define motion tokens:
  - duration: fast (120ms), normal (240ms), slow (400ms)
  - easing: out (0.16, 1, 0.3, 1), inOut (0.65, 0, 0.35, 1)
  - distance: sm (8px), md (16px), lg (24px)
- Create `motion` utility object.
- Implement `AnimatedCard`:
  - Entrance: fade + slide up (16px), duration.normal.
  - Hover: translateY(-4px) + shadow, duration.fast.
  - Exit: fade + scale(0.95).
- Use `framer-motion`.

Output: TypeScript file with tokens and component. No explanations.
```

---

## 5. Accessibility-First Prompts

### 5.1 Accessible Modal

```
You are a senior accessibility engineer.
Generate an accessible `Modal` component.

Requirements:
- React + TypeScript functional component.
- Props:
  - `isOpen: boolean`
  - `onClose: () => void`
  - `title: string`
  - `children: React.ReactNode`
- Accessibility:
  - Role: `dialog`, `aria-modal="true"`.
  - `aria-labelledby` pointing to title.
  - Focus trap when open.
  - Close on Escape key.
  - Return focus on close.
  - Body scroll lock when open.
- Behavior:
  - Backdrop click closes.
  - Close button in header.
- Styling: Tailwind CSS, centered, max-width.

Output: TypeScript component with focus management hook. No explanations.
```

### 5.2 Accessible Tabs

```
You are a senior accessibility engineer.
Generate an accessible `Tabs` component.

Requirements:
- React + TypeScript functional component.
- Props:
  - `tabs: { id: string; label: string; content: React.ReactNode }[]`
  - `defaultTab?: string`
  - `onChange?: (tabId: string) => void`
- Accessibility:
  - Role: `tablist` for container.
  - Role: `tab` for triggers, `tabpanel` for content.
  - `aria-selected` on active tab.
  - `aria-controls` linking tab to panel.
  - Keyboard: Arrow keys navigate, Enter/Space activates.
- Styling: Tailwind CSS, underline indicator.

Output: TypeScript component. No explanations.
```

---

## 6. Design Spec Prompts

### 6.1 Motion Spec Request

```
You are a senior product designer and motion UI specialist.
Help me design a 3-4 step mobile onboarding flow with motion specs.

Work in these steps:

Step 1 – Clarify product & audience
- Ask 5-7 questions about product, persona, brand, platform.

Step 2 – Define structure
- Propose 3-4 screens with goal, message, UI elements.

Step 3 – Layout specs
- Spacing, hierarchy, color roles, responsive adaptation.

Step 4 – Motion specs
For each screen:
- Entrance: what animates, type, direction, duration, easing.
- Exit/transition: how screens enter/exit.
- Micro-interactions: hover, press, loops.
- Motion accessibility notes.

Step 5 – Token summary
- Named tokens for durations, easings, transitions.
- Map animations to tokens.

Step 6 – Accessibility checklist
- Reduced motion handling.
- Focus management.
- Timing considerations.

Output structured text with clear headings. Start with Step 1.
```

---

## 7. HTML/CSS Prompts

### 7.1 Standalone Search Bar

```
You are building a reusable UI snippet.
Generate a responsive search bar in plain HTML and CSS.

Requirements:
- Container with text input and submit button in row.
- Responsive: full-width on small, max 480px centered on large.
- Focus styles for accessibility.
- Subtle box-shadow.
- CSS variables for primary color and border radius.

Output: Single HTML file with `<style>` in `<head>`. No explanations.
```

### 7.2 Card Component

```
You are building a design system component.
Generate a card component in plain HTML and CSS.

Requirements:
- Three variants: elevated (shadow), outlined (border), filled (background).
- Padding options: small, medium, large.
- Hover effect on interactive cards.
- CSS custom properties for theming.
- BEM naming convention.

Output: Single HTML file demonstrating all variants. No explanations.
```

---

## 8. Storybook Prompts

### 8.1 Component + Stories

```
You are a senior React + TypeScript engineer with Storybook expertise.
Generate a `Button` component and Storybook stories.

Component requirements:
- Variants: primary, secondary, danger.
- Sizes: sm, md, lg.
- States: loading, disabled.
- Full-width option.

Storybook requirements:
- CSF 3.0 format.
- Stories: Default, Variants, Sizes, Loading, Disabled, FullWidth.
- Args for controls.
- argTypes for documentation.

Output two files:
1. `Button.tsx` - component code
2. `Button.stories.tsx` - Storybook stories

No explanations or comments.
```

---

## 9. Template Skeleton

### Universal Component Prompt

```
You are a senior [framework] engineer.
Generate a production-ready [framework] component named `[ComponentName]` that:
- [Behavior and state requirements]
- [Props/inputs with types]
- [Styling approach: Tailwind/CSS modules/etc.]
- [Accessibility requirements: ARIA, keyboard, focus]

Output only the complete [language] code. No explanations, no comments.
```

### Universal Layout Prompt

```
You are a senior [framework] engineer and UX designer.
Build a self-contained `[LayoutName]` layout that:
- [Structure description]
- [Responsive behavior]
- [Navigation/slots]
- [State management approach]

Accessibility:
- [Landmarks]
- [Keyboard navigation]

Styling:
- [Framework/approach]

Output: Single [language] file with mock data. No explanations.
```

---

## 10. Output Constraints

Always end prompts with one of these:

**For code only:**
```
Output only the complete TypeScript code. No explanations, no comments, no markdown fences.
```

**For code + types:**
```
Output only the complete TypeScript code (component + props type). No explanations.
```

**For multiple files:**
```
Output two files in sequence:
1. `[Component].tsx` - component code
2. `[Component].stories.tsx` - stories
No explanations or comments.
```

**For design specs:**
```
Output structured text with clear headings. No code.
```

---

*Version: 1.0*
*Compatible: Gemini Pro, Gemini Ultra, AI Studio, Vertex AI*
*Updated: November 2025*
