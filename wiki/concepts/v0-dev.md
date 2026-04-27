---
title: "v0 (Vercel)"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: [ai-coding, react, nextjs, vercel, prototyping, ui]
related:
  - [[cursor]]
  - [[claude-code]]
  - [[bolt-new]]
  - [[vibe-coding-solo-developer]]
  - [[tailwind-css]]
  - [[shadcn-ui]]
---

# v0 (Vercel)

Vercel's AI-powered React/Next.js code generation tool. Generates production-ready UI components and full-page layouts from natural language prompts. Focused on the modern React/Next.js/Tailwind stack.

## Overview

v0 is Vercel's AI tool for generating React components using:
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **Next.js App Router** conventions
- **TypeScript** throughout

**Primary use case**: Rapidly generate UI components and page layouts, then export to your codebase. Not a full application builder — focused on the presentation layer.

## Key Concepts

### How It Works

v0 uses a fine-tuned model optimized for React/Tailwind generation:

1. **Prompt input**: Describe the UI you want (e.g., "pricing page with 3 tiers, toggle for monthly/annual, feature comparison table")
2. **AI generation**: Produces React component with Tailwind classes
3. **Preview**: See rendered component in real-time
4. **Refine**: Ask for changes ("make the primary button blue instead of indigo")
5. **Export**: Copy code or push directly to GitHub

### Model Training

v0 is built on Vercel's internal AI research plus:
- Fine-tuned on shadcn/ui component patterns
- Trained on Vercel deployment patterns
- Optimized for Next.js App Router conventions

### Core Capabilities

- **Component generation**: Buttons, cards, forms, modals, tables, etc.
- **Full page layouts**: Landing pages, dashboards, pricing pages
- **Responsive design**: Mobile-first by default
- **Dark mode**: Built-in dark mode support
- **Animation**: Framer Motion patterns included
- **Copy/paste**: Works in any React/Next.js project

### The shadcn/ui Connection

shadcn/ui is NOT a component library — it's copy-paste component source code:

- Components live in your project as regular `.tsx` files
- Full customization — edit the source directly
- No package dependencies to manage
- v0 generates components that match shadcn/ui patterns

```bash
# Install shadcn/ui
npx shadcn-ui@latest init

# Add a component
npx shadcn-ui@latest add button
# This copies the button source into your project
```

## Practical Applications

### Best For

1. **UI prototyping**: Generate component, evaluate, iterate
2. **Landing pages**: Generate full layouts from wireframe descriptions
3. **Dashboard UIs**: Tables, charts, forms with consistent design
4. **Design system components**: Match your brand with custom Tailwind
5. **Learning React patterns**: See how shadcn/ui writes React

### Comparison with Alternatives

| Feature | v0 | Cursor | Claude Code |
|---------|-----|--------|------------|
| Focus | UI components | Full application | Full application |
| Stack | React/Tailwind | Any | Any |
| Code quality | Excellent (Tailwind) | Good | Good |
| Export | Copy + GitHub push | Copy + paste | Copy + paste |
| Pricing | 200 generations/mo free, $30/mo Pro | $20/mo | $20/mo |

### Prompting v0 Effectively

**Good prompt structure**:
```
[Component type]: [description of visual + interaction]
[States]: [default, hover, disabled, loading]
[Styling]: [brand colors, spacing preferences]
[Data]: [what props it accepts]
```

**Example prompts**:
- "Hero section with large heading, subheading, two CTA buttons, and a product screenshot on the right. Dark background with gradient accent."
- "Data table with sortable columns, pagination, search input, and row selection checkboxes. Uses indigo color scheme."
- "Pricing toggle between monthly/annual with savings badge. Three cards with feature lists."

### Limitations

- **React only**: Not for Vue, Svelte, or plain HTML
- **Tailwind required**: Generates Tailwind — no CSS modules or styled-components
- **No logic**: Focuses on presentation, not business logic
- **Can hallucinate APIs**: Sometimes generates non-existent component props
- **Context length**: Long conversations can lose earlier design decisions

## Integration with Solo Developer Stack

v0 fits into the solo dev workflow:

```
1. v0: Generate UI components ("pricing page", "landing hero")
2. v0: Generate dashboard components ("data table", "chart")
3. Cursor/Claude Code: Add business logic and API routes
4. Deploy: Vercel auto-deploys Next.js apps
```

**Solo dev typical stack**:
- **Frontend UI**: v0 + shadcn/ui
- **Backend**: Supabase or Railway
- **AI coding**: Cursor or Claude Code
- **Hosting**: Vercel (free tier generous)
- **Payments**: Lemonsqueezy

## Related Concepts

- [[cursor]] — Desktop AI-first IDE
- [[claude-code]] — Terminal-native AI coding agent
- [[bolt-new]] — Browser-based full-stack IDE
- [[vibe-coding-solo-developer]] — Solo dev workflow with AI
- [[tailwind-css]] — Utility-first CSS framework
- [[shadcn-ui]] — Copy-paste component system

## Further Reading

- [v0.dev](https://v0.dev) — Official product
- [shadcn/ui](https://ui.shadcn.com) — Component library
- [Tailwind CSS](https://tailwindcss.com) — Styling framework

---

*Synthesized from AI agent frameworks research — 2026-04-21*
