<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# explain Google AI Generative views for UI development and coding

Google’s “generative views” / “generative UI” is a new pattern where Gemini doesn’t just return text, but synthesizes an entire interactive UI—tables, galleries, planners, tools—on‑the‑fly for a given prompt, and the same stack also shows up in AI Studio / Vertex AI as code- and UI-generating capabilities for developers.[^1_1][^1_2][^1_3]

## What “generative UI/views” means

- In the Gemini app and Search AI Mode, Gemini 3 dynamically builds bespoke interfaces—interactive tools, simulations, layouts—tailored to the user’s intent (e.g., travel planners, comparison dashboards, learning aides) instead of a static answer.[^1_1][^1_4]
- Two concrete patterns Google names are “dynamic view” (task-focused, interactive response) and “visual layout” (rich, visual arrangement of content), both powered by an internal generative-UI implementation on top of Gemini’s agentic coding capabilities.[^1_1][^1_2]


## How this relates to UI development

- The same underlying capability—“prompt to interface”—is being exposed to developers via Google AI Studio and Vertex AI Studio, where prompts can generate app UIs, components, and layout code (HTML/CSS/JS, Flutter, etc.) from natural language or mockups.[^1_5][^1_3][^1_6]
- Tools like Stitch (“Design with AI”) explicitly target UI ideation by generating mobile and web screens that designers or engineers can then refine and productionize, effectively turning high‑level requirements into concrete interface proposals.[^1_7][^1_8]


## How this relates to coding

- Gemini Code Assist and the Gemini API provide multimodal code generation: full functions, UI components, and even entire app “vibe-coded” workflows from natural language specs, often conditioned on your existing repo or project context.[^1_9][^1_10][^1_11]
- On Vertex AI, there are dedicated code-completion and code-generation endpoints (e.g., CodeGemma / code-completion APIs) that can turn comments, partial code, or example UIs into completed components and boilerplate, with low-latency completions integrated into IDEs.[^1_12][^1_11]


## Developer-facing building blocks

- Google AI Studio “Build mode” is the low-friction environment where you can chat-spec an app (including UI behavior), test it, and then deploy or export code; this is effectively a hosted, agentic multi-tool orchestrator wrapped in a dev-friendly UI.[^1_13][^1_5]
- Vertex AI (and the broader “AI for developers” stack) gives you production-grade APIs, model garden access, and an Agent Development Kit to embed generative UIs and code-gen agents inside your own products—rather than only inside Google surfaces like Search or the Gemini app.[^1_3][^1_6][^1_14]


## How to explore this hands-on

- Public, “black-box” experience of generative views: use the Gemini app or Google Search AI Mode with Gemini 3 (Pro/Ultra) and watch how prompts like “plan a 5-day trip to Tokyo with a visual timeline and budget sliders” yield interactive layouts instead of paragraphs.[^1_1][^1_4][^1_2]
- Developer exploration: in AI Studio, experiment with Build mode to natural-language-spec small CRUD apps or dashboards, and in Vertex AI Studio, try “image mockup to HTML” and code-generation samples to see how prompts become both UI structure and implementation code.[^1_3][^1_13][^1_6]

If you want, the next step can be a very focused “prompt skeleton” for: a) using AI Studio Build mode to generate a specific UI flow, or b) wiring the Gemini API into your existing multi-agent stack to let agents propose and patch React/Flutter UIs on the fly.
<span style="display:none">[^1_15][^1_16][^1_17][^1_18][^1_19][^1_20]</span>

<div align="center">⁂</div>

[^1_1]: https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/

[^1_2]: https://blog.google/products/gemini/gemini-3-gemini-app/

[^1_3]: https://cloud.google.com/vertex-ai

[^1_4]: https://ediscoverytoday.com/2025/11/19/generative-ui-a-new-ai-driven-user-experience-paradigm-from-google-artificial-intelligence-trends/

[^1_5]: https://aistudio.google.com

[^1_6]: https://cloud.google.com/ai/generative-ai

[^1_7]: https://stitch.withgoogle.com

[^1_8]: https://dl.acm.org/doi/10.1145/3715336.3735780

[^1_9]: https://cloud.google.com/use-cases/ai-for-developers

[^1_10]: https://ai.google.dev

[^1_11]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models

[^1_12]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-sdk-code-completion-comment

[^1_13]: https://ai.google.dev/gemini-api/docs/aistudio-build-mode

[^1_14]: https://docs.cloud.google.com/docs/generative-ai

[^1_15]: https://cloud.google.com/generative-ai-studio

[^1_16]: https://www.constellationr.com/blog-news/insights/google-launches-gemini-3-google-antigravity-generative-ui-features

[^1_17]: https://www.youtube.com/watch?v=a8NtWQbQI4E

[^1_18]: https://stackoverflow.com/questions/79752817/vertex-ai-video-generation-how-to-publish-progress-updates-to-a-pub-sub-topic

[^1_19]: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content

[^1_20]: https://jakobnielsenphd.substack.com/p/generative-ui-google


---

# Show example prompts and generated code for a UI component

Here are concrete, copy-pastable examples for prompting Gemini to generate a UI component and the kind of code you’d expect back (React and plain HTML/CSS). The prompts are structured so you can drop them into AI Studio / Vertex AI Studio or your own Gemini API client.[^2_1][^2_2][^2_3]

***

## Example 1: React component (cards grid)

**Prompt (to Gemini / AI Studio / Vertex AI Studio)**

> You are a senior React + TypeScript engineer.
> Create a self-contained React functional component named `ProductGrid` that:
> - Accepts a `products` prop: array of `{ id: string; name: string; price: number; imageUrl: string; }`.
> - Renders a responsive CSS grid of product cards (3 columns on desktop, 2 on tablet, 1 on mobile).
> - Each card shows the image, name, formatted price (`$12.99` style), and a “View details” button.
> - Uses Tailwind CSS utility classes for styling.
> - Includes minimal hover effects and focus states for accessibility.
> Output only valid TypeScript React code for the component and its props type. No explanations, no markdown, no backticks.

**Representative generated code (simplified)**

```tsx
import React from "react";

type Product = {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
};

type ProductGridProps = {
  products: Product[];
  onViewDetails?: (productId: string) => void;
};

export const ProductGrid: React.FC<ProductGridProps> = ({
  products,
  onViewDetails,
}) => {
  return (
    <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
      {products.map((product) => (
        <article
          key={product.id}
          className="rounded-lg border border-slate-200 bg-white shadow-sm hover:shadow-md transition-shadow focus-within:ring-2 focus-within:ring-blue-500"
        >
          <img
            src={product.imageUrl}
            alt={product.name}
            className="h-48 w-full object-cover rounded-t-lg"
          />
          <div className="p-4 flex flex-col gap-2">
            <h2 className="text-base font-semibold text-slate-900 line-clamp-2">
              {product.name}
            </h2>
            <p className="text-sm font-medium text-blue-600">
              {product.price.toLocaleString("en-US", {
                style: "currency",
                currency: "USD",
              })}
            </p>
            <button
              type="button"
              onClick={() => onViewDetails?.(product.id)}
              className="mt-2 inline-flex items-center justify-center rounded-md bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
            >
              View details
            </button>
          </div>
        </article>
      ))}
    </div>
  );
};
```

This mirrors typical Gemini output when asked for a typed React component with Tailwind and explicit prop contracts.[^2_4][^2_5]

***

## Example 2: Plain HTML/CSS component (search bar)

**Prompt**

> You are building a reusable UI snippet for a design system.
> Generate a minimal, responsive **search bar** component in plain HTML and CSS that:
> - Has a container with a text input and a submit button in a single row.
> - On small screens, the bar is full-width; on large screens, it is centered and max 480px wide.
> - Includes focus styles for accessibility and a subtle box-shadow.
> - Uses CSS variables for primary color and border radius.

```
> Output a single HTML file with a `<style>` block in the `<head>` and the search bar inside `<body>`. No explanations, no markdown.
```

**Representative generated code (simplified)**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Search Bar Component</title>
  <style>
    :root {
      --primary: #2563eb;
      --radius: 9999px;
    }

    * {
      box-sizing: border-box;
    }

    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
        sans-serif;
      margin: 0;
      padding: 2rem;
      display: flex;
      justify-content: center;
    }

    .search-wrapper {
      width: 100%;
      max-width: 480px;
    }

    .search-bar {
      display: flex;
      align-items: stretch;
      background: #ffffff;
      border-radius: var(--radius);
      box-shadow: 0 6px 18px rgba(15, 23, 42, 0.12);
      overflow: hidden;
      border: 1px solid #e2e8f0;
    }

    .search-input {
      flex: 1;
      border: none;
      padding: 0.75rem 1rem;
      font-size: 0.95rem;
      outline: none;
    }

    .search-input::placeholder {
      color: #9ca3af;
    }

    .search-input:focus-visible {
      outline: 2px solid transparent;
    }

    .search-button {
      border: none;
      background: var(--primary);
      color: #ffffff;
      padding: 0 1.25rem;
      font-size: 0.95rem;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 150ms ease-in-out;
    }

    .search-button:hover {
      background: #1d4ed8;
    }

    .search-button:focus-visible {
      outline: 2px solid #1d4ed8;
      outline-offset: 2px;
    }

    @media (max-width: 480px) {
      body {
        padding: 1rem;
      }
    }
  </style>
</head>
<body>
  <div class="search-wrapper">
    <form class="search-bar" role="search">
      <input
        type="search"
        class="search-input"
        placeholder="Search..."
        aria-label="Search"
      />
      <button type="submit" class="search-button">
        Search
      </button>
    </form>
  </div>
</body>
</html>
```

This matches how people use Gemini in AI Studio to generate “HTML + CSS in one file” for quick UI prototyping.[^2_6][^2_7]

***

## Example 3: Prompt skeleton for your own components

You can adapt this template for any component (React, Vue, Flutter, etc.):

> You are a senior [framework] engineer.
> Generate a production-ready [framework] component named `[ComponentName]` that:
> - [Behavior and state, e.g., “shows a paginated list of items with sorting and filtering”]
> - [Props / inputs, with types or interfaces]
> - [Styling approach: Tailwind, CSS modules, Material UI, etc.]
> - [Accessibility requirements: keyboard navigation, ARIA roles, focus states]
> Output only the complete [language] code for the component (and its types if applicable). No explanations, no markdown, no comments.

If you tell me your target stack (e.g., React+MUI, Flutter, SvelteKit) and a specific UI widget you care about, a follow-up can give you a tailored prompt+output pair tuned to that environment.
<span style="display:none">[^2_10][^2_11][^2_12][^2_13][^2_14][^2_15][^2_16][^2_17][^2_18][^2_19][^2_20][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery

[^2_2]: https://dev.to/googleai/from-prompt-to-deployed-app-in-less-than-2-minutes-dh3

[^2_3]: https://ai.google.dev/gemini-api/docs/quickstart

[^2_4]: https://dev.to/tahrim_bilal/how-to-integrate-gemini-api-with-reactjs-a-step-by-step-guide-341b

[^2_5]: https://github.com/google-gemini/cookbook

[^2_6]: https://javascript.plainenglish.io/i-built-an-ai-powered-random-web-page-generator-all-in-one-html-file-812ed4a78582

[^2_7]: https://www.youtube.com/watch?v=4akqDpxFlm8

[^2_8]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/samples

[^2_9]: https://cloud.google.com/vertex-ai

[^2_10]: https://github.com/GoogleCloudPlatform/vertex-ai-samples

[^2_11]: https://www.youtube.com/watch?v=V8P_S9OLI_I

[^2_12]: https://www.youtube.com/watch?v=0yboGn8errU

[^2_13]: https://codelabs.developers.google.com/devsite/codelabs/building-ai-agents-vertexai

[^2_14]: https://ai.google.dev/gemini-api/docs/langgraph-example

[^2_15]: https://bravenewgeek.com/automating-infrastructure-as-code-with-vertex-ai/

[^2_16]: https://www.youtube.com/watch?v=My0M-a4FSMc

[^2_17]: https://www.codecademy.com/article/how-to-build-agents-with-vertex-ai-builder

[^2_18]: https://cloud.google.com/generative-ai-studio

[^2_19]: https://www.reddit.com/r/webdev/comments/1at66c9/i_asked_gemini_to_write_a_very_simple_react/

[^2_20]: https://ai.google/get-started/


---

# Generate a prompt to create a responsive React button component

Here’s a focused, ready-to-use prompt you can paste into Gemini / AI Studio / your LLM client to generate a responsive React button component:

> You are a senior React + TypeScript engineer.
> Generate a production-ready, reusable **`Button`** component that is responsive and accessible.
> Requirements:
> - Implement as a typed React functional component in TypeScript.
> - Props:
>   - `variant: "primary" | "secondary" | "ghost"`
>   - `size?: "sm" | "md" | "lg"` (default `md`)
>   - `fullWidth?: boolean` to make the button take 100% width on small screens.
>   - `isLoading?: boolean` to show a spinner and disable the button.
>   - `leftIcon?: ReactNode`, `rightIcon?: ReactNode`.
>   - Standard button props via `React.ButtonHTMLAttributes<HTMLButtonElement>`.
> - Styling:
>   - Use Tailwind CSS utility classes.
>   - Button should be touch-friendly and adapt spacing/typography on small vs large screens.
>   - Respect `fullWidth` on mobile but allow auto width on larger screens.
> - Accessibility:
>   - Proper `type` handling, `aria-busy` when loading, keyboard focus styles, and disabled state.
> Output:
> - Only the complete TypeScript code for the component (including props type/interface and default export).
> - No explanations, no comments, no markdown fences.
<span style="display:none">[^3_1][^3_2][^3_3][^3_4][^3_5][^3_6][^3_7][^3_8][^3_9]</span>

<div align="center">⁂</div>

[^3_1]: https://www.telerik.com/kendo-react-ui/aiprompt

[^3_2]: https://stackoverflow.com/questions/51942009/best-way-to-create-new-react-component-using-create-react-app

[^3_3]: https://blogs.purecode.ai/blogs/react-button

[^3_4]: https://dev.to/sharkham/building-a-writing-prompt-generator-with-functional-react-1k1o

[^3_5]: https://javascript.plainenglish.io/how-i-use-ai-to-review-react-code-like-a-pro-38bd730aeb3e

[^3_6]: https://www.geeksforgeeks.org/reactjs/how-to-create-a-responsive-like-button-in-reactjs/

[^3_7]: https://www.reddit.com/r/react/comments/14q6d2f/how_to_make_an_ultimate_button_component_with/

[^3_8]: https://www.builder.io/blog/build-react-components

[^3_9]: https://www.figma.com/solutions/ai-ui-generator/


---

# Include accessibility features and ARIA attributes for the button

Here’s an updated, drop-in prompt that explicitly bakes in accessibility features and ARIA attributes for the responsive React button:

> You are a senior React + TypeScript engineer.
> Generate a production-ready, reusable `Button` component that is responsive, accessible, and ARIA-compliant.
> Requirements:
> - Implement as a typed React functional component in TypeScript.
> - Props:
>   - `variant: "primary" | "secondary" | "ghost"`
>   - `size?: "sm" | "md" | "lg"` (default `md`)
>   - `fullWidth?: boolean` to make the button take 100% width on small screens.
>   - `isLoading?: boolean` to show a spinner and disable interactions.
>   - `leftIcon?: React.ReactNode`, `rightIcon?: React.ReactNode`.
>   - `ariaLabel?: string` for icon-only or ambiguous labels.
>   - Inherit standard button props via `React.ButtonHTMLAttributes<HTMLButtonElement>`.
> - Responsiveness \& styling:
>   - Use Tailwind CSS utility classes.
>   - Button should be touch-friendly with adequate hit area, and adapt spacing/typography on small vs large screens.
>   - Respect `fullWidth` on mobile while allowing auto width on larger screens.
> - Accessibility \& ARIA:

```
>   - Use a native `<button>` element, not a `<div>`.  
```

>   - Ensure correct `type` handling (`button` by default).
>   - When `isLoading` is true:
>     - Set `aria-busy="true"` and `aria-disabled="true"`.
>     - Disable the button and prevent `onClick` from firing.
>   - Support passing `aria-label`, `aria-describedby`, and `aria-controls` through props.
>   - Provide visible focus styles that meet WCAG contrast guidelines.
>   - If `leftIcon` or `rightIcon` is purely decorative, ensure it is hidden from screen readers (`aria-hidden="true"`).
>   - Ensure the button is fully keyboard operable (Tab / Shift+Tab / Space / Enter).
> Output:
> - Only the complete TypeScript code for the component (including props type/interface and default export).
> - No explanations, no comments, no markdown fences.

---

# continue creating multiple generative ui prompt examples

Here are several focused generative-UI prompt examples you can reuse and adapt. Each is designed to produce both UI structure and implementation (React) when you run it through Gemini / AI Studio.

You asked earlier for a button; these expand to richer components and layouts.

## 1) Accessible responsive button (refined)

> You are a senior React + TypeScript engineer.
> Generate a production-ready, reusable `Button` component that is responsive, accessible, and ARIA-compliant.
> Requirements:
> - React functional component in TypeScript.
> - Props:
>   - `variant: "primary" | "secondary" | "ghost"`
>   - `size?: "sm" | "md" | "lg"` (default `md`)
>   - `fullWidth?: boolean` to stretch to 100% width on small screens.
>   - `isLoading?: boolean` to show a spinner and block clicks.
>   - `leftIcon?: React.ReactNode`, `rightIcon?: React.ReactNode`.
>   - `ariaLabel?: string` for icon-only usage.
>   - Extend `React.ButtonHTMLAttributes<HTMLButtonElement>`.
> - Behavior \& accessibility:
>   - Use native `<button>` with `type="button"` by default.
>   - When `isLoading` is true: set `aria-busy="true"`, `aria-disabled="true"`, disable the button, and ignore `onClick`.
>   - Support `aria-label`, `aria-describedby`, `aria-controls` pass-through.
>   - Visible focus ring that meets WCAG contrast; fully keyboard operable.
>   - If icons are decorative, mark them `aria-hidden="true"`.
> - Styling:
>   - Use Tailwind CSS for layout and variants.
>   - Touch-friendly padding and typography, responsive spacing for mobile vs desktop.
> Output only the complete TypeScript code (component + props), no comments, no markdown fences, no explanation.

## 2) Responsive card list with filters (generative UI pattern)

> You are a senior React + TypeScript engineer and UX designer.
> Build a small, self-contained UI consisting of:
> - A responsive filter bar and a grid of cards that update based on the filters.
> Requirements:
> - Implement using React + TypeScript with functional components.
> - Data model: `Item { id: string; title: string; category: "design" | "engineering" | "product"; difficulty: "beginner" | "intermediate" | "advanced"; description: string; }`.
> - UI layout:
>   - A top filter bar with:
>     - Category tabs (All, Design, Engineering, Product).
>     - A difficulty dropdown.
>     - A search input that filters by title.
>   - Below, a responsive grid of cards (1 column mobile, 2 tablet, 3+ desktop).
> - Behavior:
>   - Filters should combine (category + difficulty + search).
>   - Show a “No results” empty state with a short message and “Clear filters” button.
> - Accessibility:
>   - Use proper roles and labels for tabs, dropdown, and search input.
>   - Keyboard navigation for tabs and filters.
> - Styling:
>   - Use Tailwind CSS utility classes and a light theme.
> Output: A single TypeScript file that includes sample `items` data and renders a root `FilterableItemGrid` component. No explanations or comments.

## 3) Multi-step form wizard (dynamic view)

> You are a senior React + TypeScript engineer.
> Create a responsive multi-step “Project Creation Wizard” UI.
> Requirements:
> - Implement as a React app in a single TypeScript file with:
>   - `ProjectWizard` (root), and child components per step.
> - Steps:
>   1) Project details (name, description, type select).
>   2) Team (add/remove team members with name + role).
>   3) Review \& confirm (read-only summary + submit).
> - UI behavior:
>   - Next/Previous navigation with validation per step.
>   - Disable “Next” if required fields are missing.
>   - Show a step indicator (1/3, 2/3, 3/3) and a progress bar.
> - Accessibility:
>   - Appropriate labels and `aria-describedby` for inputs and errors.
>   - Announce validation errors using `aria-live="polite"`.
>   - Keyboard-accessible for all interactive elements.
> - Responsiveness:
>   - Single-column on mobile; two-column layout for form + summary on desktop where appropriate.
> - Styling:
>   - Tailwind CSS utility classes only.
> Output: A single TypeScript file with all components and minimal in-memory state (no external libraries). No explanation or comments.

## 4) Dashboard layout with sidebar and cards

> You are a senior React + TypeScript engineer.
> Generate a responsive “Analytics Dashboard” layout.
> Requirements:
> - React + TypeScript functional components.
> - Layout:
>   - Left sidebar with logo, nav items, and a collapse/expand toggle.
>   - Top bar with title, search, and user menu.
>   - Main content area with a responsive grid of “stat tiles” and a table.
> - Behavior:
>   - Sidebar collapses to icons-only on small screens and can be toggled.
>   - Cards resize from 1 column on small screens up to 4 on large screens.
> - Data:
>   - Use mock stats data and a small table of records (e.g., transactions).
> - Accessibility:
>   - Use `nav` landmarks, `aria-current="page"` for active item, focus management on sidebar toggle.
> - Styling:
>   - Tailwind CSS, light theme, subtle shadows.
> Output: A single TypeScript file exposing a `DashboardPage` component with mock data defined inline. No explanations or comments.

## 5) Prompt to generate both UI and storybook stories

> You are a senior React + TypeScript engineer with Storybook expertise.
> Generate a responsive `Button` UI component and Storybook stories for it.
> Requirements:
> - Implement the `Button` as a React + TypeScript component with the following props:
>   - `variant: "primary" | "secondary" | "danger"`
>   - `size?: "sm" | "md" | "lg"`
>   - `isLoading?: boolean`
>   - `fullWidth?: boolean`
>   - Extend `React.ButtonHTMLAttributes<HTMLButtonElement>`.
> - Accessibility:
>   - Native `<button>` element with proper `type` default.
>   - `aria-busy` and `aria-disabled` when loading or disabled.
>   - Focus-visible ring, keyboard support.
> - Styling:
>   - Tailwind CSS utilities.
> - Storybook:
>   - Generate a CSF file with stories for: Default, Variants, Sizes, Loading state, Full-width.
> Output: Two files worth of code in sequence:
>   1) `Button.tsx`
>   2) `Button.stories.tsx`
> No explanations, no comments, no markdown fences.

If you tell me your target stack (e.g., Next.js + MUI, Chakra, Radix, or a design system you already use), the next step can be a tailored set of prompts tuned to that stack, plus variants for “design mockup to code” and “existing code to improved generative UI.”
<span style="display:none">[^5_1][^5_2][^5_3][^5_4][^5_5][^5_6][^5_7][^5_8][^5_9]</span>

<div align="center">⁂</div>

[^5_1]: https://uxplanet.org/steal-these-10-gemini-prompts-to-create-stunning-ui-design-for-free-001706844f38

[^5_2]: https://github.com/ZeroLu/awesome-gemini-ai

[^5_3]: https://www.techradar.com/ai-platforms-assistants/gemini/google-gemini-3-has-dropped-here-are-6-prompts-that-show-what-it-can-do

[^5_4]: https://www.reddit.com/r/PromptEngineering/comments/1n9s0yy/geminis_google_nano_banana_prompts_for_daily/

[^5_5]: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery

[^5_6]: https://www.upwork.com/resources/google-gemini-prompts

[^5_7]: https://cloud.google.com/gemini-enterprise/resources/prompt-guide

[^5_8]: https://clickup.com/blog/gemini-prompts/

[^5_9]: https://www.reddit.com/r/GoogleGeminiAI/comments/1knazl7/30_gemini_25_use_cases_you_can_try_today_with/


---

# Write Gemini prompts for generating an onboarding flow with animations

Here are several ready-to-paste Gemini prompts for generating an animated onboarding flow in React. Each one is focused and assumes you want both UI and animation behavior in the output.

You can treat each as a separate run, or chain them (e.g., first layout, then refine animations).

1) Multi-screen onboarding flow with animated transitions

> You are a senior React + TypeScript engineer and product designer.
> Generate a multi-screen onboarding flow for a web app, implemented in React + TypeScript.
> Requirements:
> - Use functional components with hooks.
> - The flow should have 3–4 steps, for example:
>   1) Welcome screen with product value props.
>   2) Personalization (collect basic preferences).
>   3) Permissions / feature toggles.
>   4) Final “You’re all set” confirmation.
> - Include Next / Back / Skip buttons, with keyboard-accessible navigation.
> - Implement animated transitions between steps using a lightweight animation library (e.g., `framer-motion`) or CSS transitions:
>   - Steps slide horizontally or fade+scale when moving forward/back.
>   - Buttons have subtle hover and press animations.
> - Make the layout responsive (single column on mobile, centered card on desktop).
> - Include basic accessibility: focus management when the step changes, appropriate ARIA labels for headings and buttons.
> Output: a single TypeScript file containing the main `OnboardingFlow` component and any subcomponents, ready to drop into a React app. No explanations or comments; output only code.

2) Mobile-first onboarding with Lottie or SVG animations

> You are a senior React + TypeScript engineer.
> Build a mobile-first onboarding flow with illustration-style animations.
> Requirements:
> - Use React + TypeScript functional components.
> - Each onboarding screen includes:
>   - A short headline and description.
>   - An animated illustration (you can assume an existing Lottie JSON or SVG; just wire it up).
>   - Primary and secondary CTAs.
> - Integrate animations using either:
>   - `lottie-react` for Lottie JSON files, or
>   - CSS keyframe animation for SVG icons.
> - Layout:
>   - Optimized for mobile viewport first, responsive up to desktop.
>   - Content vertically centered with safe-area considerations.
> - Animations:
>   - Each screen’s illustration should loop gently.
>   - The whole card should have a subtle entrance animation on initial mount (e.g., fade up).
> - Accessibility:
>   - Provide ARIA labels / alt text for animated elements that convey meaning, and hide purely decorative animations from screen readers.
> Output: a single TypeScript file with an `OnboardingScreens` component, mock animation imports, and minimal styling (Tailwind CSS or basic CSS-in-JS). No explanations or comments.

3) Progress-indicator onboarding with animated progress and transitions

> Act as a senior React + TypeScript engineer.
> Create a responsive onboarding wizard with a visual progress indicator and animations.
> Requirements:
> - Use React + TypeScript.
> - Components:
>   - `OnboardingWizard` (root container).
>   - Step components (e.g., `StepWelcome`, `StepProfile`, `StepPreferences`).
>   - A top progress indicator:
>     - Horizontal bar that animates width when advancing steps.
>     - Optional step dots that animate active/inactive state.
> - Animations:
>   - Use `framer-motion` or CSS transitions for:
>     - Progress bar width changes.
>     - Step content entering and leaving (e.g., fade+slide).
>   - Animate buttons on hover/focus for feedback.
> - Behavior:
>   - Next/back navigation with basic validation for required fields.
>   - Disable “Next” until valid.
> - Responsiveness:
>   - On small screens, stack everything vertically.
>   - On larger screens, constrain the flow to a centered card with max-width.
> - Accessibility:
>   - Announce step changes using ARIA (e.g., `aria-live="polite"` region for step title).
>   - Ensure all controls are keyboard accessible with visible focus states.
> Output: a single TypeScript file with all components and inline mock data/state. Use Tailwind CSS classes for styling. No comments or explanation text.

4) Full onboarding experience + state management + exit animation

> You are a senior React + TypeScript engineer.
> Implement a complete onboarding experience with animations and shared state.
> Requirements:
> - React + TypeScript, functional components.
> - Maintain onboarding state in a single parent component and pass it down via props.
> - Steps:
>   - Intro screen.
>   - Basic profile form.
>   - Feature selection (toggle chips).
>   - Summary + “Finish” button.
> - Animations:
>   - Use `framer-motion` for:
>     - Animated container transitions (slide/fade) when moving between steps.
>     - Slight scale/opacity animation on hover for feature chips.
>     - Exit animation when onboarding completes (e.g., the card shrinks and fades out).
> - Responsiveness:
>   - Mobile-first, with sensible spacing and typography.
>   - On desktop, center the onboarding card, with max-width and subtle background gradient.
> - Accessibility:
>   - Preserve focus when steps change (send focus to the main heading of each step).
>   - Provide ARIA attributes for toggles, buttons, and progress indicators.
> Output: a single TypeScript file exporting `OnboardingExperience`. Use Tailwind CSS for styling and assume `framer-motion` is available. Output only code.

5) Design-to-code: generating onboarding UI from a textual spec

> You are a senior React + TypeScript + Motion UI engineer.
> Convert the following textual specification into a responsive onboarding flow with animations in React + TypeScript:
> - [PASTE MY SPECS HERE: target audience, brand tone, color palette, copy examples, etc.]
> Implementation requirements:
> - Use React + TypeScript functional components.
> - Use Tailwind CSS for layout and styling.
> - Use `framer-motion` for:
>   - Step transitions (e.g., swipe horizontally).
>   - Animated staggered reveals of text and buttons.
> - Implement 3–4 steps as described in the spec, with Next/Back/Skip, and a final “Get started” action.
> - Include basic validation on any form fields.
> - Add ARIA attributes and focus management for step changes.
> Output: a single TypeScript file with all onboarding components and hooks, ready to drop into a Next.js or CRA app. Do not include explanations or comments.

If you tell me your preferred animation lib (pure CSS vs framer-motion) and target app stack (Next.js / CRA / Remix), the next iteration can turn one of these into a very specific “copy-paste into this file name” prompt tailored to your setup.
<span style="display:none">[^6_1][^6_2][^6_3][^6_4][^6_5][^6_6][^6_7][^6_8][^6_9]</span>

<div align="center">⁂</div>

[^6_1]: https://workspace.google.com/resources/ai/prompts-for-hr/

[^6_2]: https://cloud.google.com/gemini-enterprise/resources/prompt-guide

[^6_3]: https://natesnewsletter.substack.com/p/the-gemini-3-vs-chatgpt-51-prompting

[^6_4]: https://www.youtube.com/watch?v=V8Ka2OyG1QM

[^6_5]: https://support.google.com/a/users/answer/14200040?hl=en

[^6_6]: https://clickup.com/p/ai/prompts/onboarding-guide

[^6_7]: https://ai.google.dev/gemini-api/docs/prompting-strategies

[^6_8]: https://www.youtube.com/watch?v=QUoxvf4tZHQ

[^6_9]: https://edu.google.com/intl/ALL_us/ai/gemini-for-education/


---

# Provide a step by step Gemini prompt to design onboarding screens with motion specs

Here’s a structured, step‑by‑step Gemini prompt you can paste directly into AI Studio to design onboarding screens with explicit motion specs. It walks Gemini through requirements, screen content, motion, and output format.

***

## Step‑by‑step Gemini design prompt

> You are a senior product designer and motion UI specialist.
> Help me **design a 3–4 step mobile onboarding flow** for a modern SaaS app, including **visual layout, copy, and detailed motion specs**.
>
> Work in the following steps, and clearly label each section in your answer:
>
> **Step 1 – Clarify product \& audience**
> - Ask me 5–7 concise questions to clarify:
>   - What the product does.
>   - Primary user persona and their goals.
>   - Brand personality (e.g., playful, professional, calm).
>   - Platform focus (iOS, Android, responsive web).
>   - Any constraints (accessibility level, no 3D, etc.).
> - After my answers, restate the product and audience in 3 short bullets.
>
> **Step 2 – Define onboarding structure**
> - Propose a 3–4 screen onboarding flow as a bullet list.
> - For each screen, specify:
>   - Goal of the screen.
>   - Core message in one sentence.
>   - Key UI elements (hero illustration, title, body text, primary CTA, secondary CTA, progress indicator, etc.).
> - Keep copy short and friendly; avoid lorem ipsum.
>
> **Step 3 – Screen‑level layout specs**
> For each screen, provide **layout specifications** that a designer or engineer could implement without guessing:
> - Describe hierarchy and approximate spacing (e.g., “stacked vertical layout, center-aligned, ~24px gap between title and body”).
> - Define how the layout adapts from small mobile to larger screens (e.g., max width card centered on web).
> - Call out color roles, not specific hex values (e.g., “brand-primary”, “surface”, “on-surface-muted”).
>
> **Step 4 – Motion \& interaction specs**
> For each screen and transition, define **motion specs** in a structured way:
> - **Entrance animation:**
>   - What animates (e.g., card container, hero illustration, buttons).
>   - Type (fade, slide, scale, staggered sequence).
>   - Direction and distance (e.g., “slide up 24px”).
>   - Duration and easing (e.g., “220ms, ease-out”).
> - **Exit / transition animation between steps:**
>   - How the current screen leaves and next screen enters (e.g., “current slides left + fades out, next slides in from right”).
>   - Any shared element transitions (e.g., progress indicator animating width).
> - **Micro‑interactions:**
>   - Button hover/press states.
>   - Progress indicator animation.
>   - Any subtle looping animations on illustrations (e.g., “gentle 2s bobbing motion”).
> - Include a short note on **motion accessibility**, e.g., how to reduce or disable motion for “prefers-reduced-motion”.
>
> **Step 5 – Implementation‑ready motion spec summary**
> - Summarize the motion as if handing off to an engineer using a framework like `framer-motion` or CSS:
>   - Provide a table or list mapping **named tokens** to values, for example:
>     - `motion.duration.short = 180ms`
>     - `motion.duration.medium = 240ms`
>     - `motion.easing.out = cubic-bezier(0.16, 1, 0.3, 1)`
>     - `motion.transition.screenForward = slideX(+32px) + fade, 240ms, easing.out`
>   - Map each screen transition and key element animation to these tokens.
>
> **Step 6 – Accessibility checklist**
> - Provide an onboarding‑specific motion \& interaction accessibility checklist:
>   - How to handle reduced‑motion users.
>   - Focus management when changing steps.
>   - Minimum tap targets and timing considerations (e.g., avoid very fast, flashy loops).
>
> Output everything as structured text with clear headings for each step (Step 1–6), bullet lists where appropriate, and **no code**.
> Start with Step 1 now.
<span style="display:none">[^7_1][^7_2][^7_3][^7_4][^7_5][^7_6][^7_7][^7_8]</span>

<div align="center">⁂</div>

[^7_1]: https://cloud.google.com/gemini-enterprise/resources/prompt-guide

[^7_2]: https://ai.google.dev/gemini-api/docs/prompting-strategies

[^7_3]: https://www.youtube.com/watch?v=4xic0AViHm0

[^7_4]: https://www.promptingguide.ai/models/gemini

[^7_5]: https://uxplanet.org/steal-these-10-gemini-prompts-to-create-stunning-ui-design-for-free-001706844f38

[^7_6]: https://workspace.google.com/resources/ai/prompts-for-hr/

[^7_7]: https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/

[^7_8]: https://www.youtube.com/watch?v=bnBzvHlhJ0E\&vl=en

