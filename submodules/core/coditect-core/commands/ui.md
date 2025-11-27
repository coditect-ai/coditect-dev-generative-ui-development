---
name: ui
description: Generate production-ready React + TypeScript UI components with WCAG compliance
---

# Generate UI Component

You are using the CODITECT Generative UI system to create a production-ready React + TypeScript component.

## Your Task
Generate a complete UI component based on the user's request with:
- **TypeScript strict mode** (no 'any' types)
- **Tailwind CSS styling** (utility-first approach)
- **WCAG AA accessibility compliance** (minimum standard)
- **Responsive design** (mobile-first)
- **Proper props interface** (TypeScript types)
- **JSDoc documentation** (comprehensive)

## Process
1. **Use IntentAnalyzerAgent** to parse the request into UISpec
2. **Use UIArchitectAgent** to design component architecture
3. **Use CodeGeneratorAgent** to create TypeScript code
4. **Use AccessibilityAuditorAgent** to validate WCAG compliance
5. **Use QualityReviewerAgent** for final approval

## Output Format
- **Complete .tsx file** with component code
- **Props interface** with TypeScript types
- **Usage example** showing component integration
- **Accessibility notes** (ARIA, keyboard, screen reader)
- **Token usage and cost estimate**

## Component Standards
- Use React 18+ with hooks (functional components only)
- Follow React best practices (memoization, proper effects)
- Include error boundaries where appropriate
- Add loading and error states
- Support dark mode via Tailwind classes
- Include comprehensive prop validation

## Example Usage
```
/ui Create a primary button with loading state
/ui Build a responsive navbar with mobile menu
/ui Generate a card component with image and description
/ui Create a form with validation and error messages
/ui Build a modal dialog with backdrop and focus trap
```

## Advanced Options
You can request specific features:
- **Variants:** "with primary, secondary, and danger variants"
- **States:** "with loading, disabled, and error states"
- **Animations:** "with hover and click animations"
- **Accessibility:** "with WCAG AAA compliance"
- **Responsive:** "with mobile, tablet, and desktop layouts"

## Quality Gates
All components must pass:
1. TypeScript strict mode compilation (no errors)
2. WCAG 2.1 AA accessibility (minimum 4.5:1 contrast)
3. No ESLint errors or warnings
4. Responsive design validation (breakpoints: 640px, 768px, 1024px)
5. Props interface completeness check

---

**Ask the user what component they want to generate.**
