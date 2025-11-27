# CODITECT Generative UI - Quick Start Guide

## 1. Install Dependencies

```bash
npm install
```

## 2. Verify Installation

```bash
# Check TypeScript compilation
npm run typecheck

# Run tests
npm test

# Build the project
npm run build
```

## 3. Basic Usage

### Using the High-Level API

```typescript
import { generateUI } from '@coditect/generative-ui';

// Generate a button component
const result = await generateUI(
  'Create a Button component with primary, secondary, and ghost variants in small, medium, and large sizes'
);

console.log('Specification:', result.spec);
console.log('Architecture:', result.architecture);
console.log('Generated Files:', result.files.map(f => f.filePath));
console.log('Token Usage:', result.metadata.tokens);
```

### Using Individual Agents

```typescript
import { IntentAnalyzer, UIArchitect, CodeGenerator } from '@coditect/generative-ui';

// Step 1: Analyze intent
const intentAnalyzer = new IntentAnalyzer();
const intentResult = await intentAnalyzer.execute(
  { description: 'Create a responsive dashboard layout with sidebar' },
  context
);

// Step 2: Design architecture
const uiArchitect = new UIArchitect();
const archResult = await uiArchitect.execute(intentResult.data, context);

// Step 3: Generate code
const codeGenerator = new CodeGenerator();
const codeResult = await codeGenerator.execute({
  architecture: archResult.data,
  framework: 'react',
  styling: 'tailwind',
  strictTypes: true,
}, context);

console.log('Generated:', codeResult.data);
```

## 4. Development Workflow

### Run Tests in Watch Mode

```bash
npm run test:watch
```

### Format Code

```bash
npm run format
```

### Lint Code

```bash
npm run lint
npm run lint:fix  # Auto-fix issues
```

## 5. What You Can Generate

### Components
- Buttons with variants and sizes
- Input fields with validation
- Cards, modals, tooltips
- Form controls
- Navigation elements

### Layouts
- Dashboard layouts (sidebar + main)
- Landing pages
- Settings pages
- Multi-step wizards

### Applications
- Full-stack applications with routing
- Admin dashboards
- User portals

## 6. Generated Code Features

All generated code includes:
- TypeScript strict mode (100% typed)
- Tailwind CSS styling
- WCAG AA accessibility
- Responsive design
- Keyboard navigation
- Unit tests
- Storybook examples (future)

## 7. Next Steps

- Read `CLAUDE.md` for comprehensive documentation
- Check `INSTALLATION-SUMMARY.md` for implementation roadmap
- Review research docs in `docs/original-research/`
- Explore examples in `examples/`

## 8. Troubleshooting

**TypeScript errors:**
```bash
npm run typecheck
```

**Test failures:**
```bash
npm test -- --verbose
```

**Build issues:**
```bash
npm run clean
npm run build
```

---

**Happy Generating!** 🚀
