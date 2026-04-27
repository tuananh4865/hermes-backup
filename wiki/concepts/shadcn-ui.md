---
title: shadcn/ui
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ui, components, react, tailwind, design-system, radix-ui, frontend]
sources: []
---

# shadcn/ui

## Overview

shadcn/ui is a collection of beautifully designed, accessible, and customizable React components built on top of Radix UI primitives and styled with Tailwind CSS. Unlike traditional component libraries (Material UI, Chakra UI, Ant Design) that you install as a dependency and import from, shadcn/ui is copy-and-paste based — you own the code. You select components via a CLI and the component source code is added directly to your project, giving you full control to modify, extend, and customize every aspect of the component without fighting library abstractions or overriding `!important` CSS rules.

The project emerged in 2023 and quickly became one of the most popular UI projects in the React ecosystem because it solved a real problem: component libraries force you into their abstractions, their default styles, and their upgrade paths. shadcn/ui flips this by giving you beautifully crafted building blocks that you own outright. Every component is headless at its core (using Radix UI for behavior and accessibility) and styled with Tailwind CSS for full visual control. The result is production-quality UI with none of the lock-in.

## Key Concepts

**Copy-and-Paste, Not a Package** — The fundamental differentiator. You run `npx shadcn-ui@latest add button` and the `button.tsx` source file is added to your `components/ui/` directory. You own it, you read it, you modify it. There's no `import { Button } from 'shadcn'` that you can't break into.

**Radix UI Primitives** — shadcn/ui uses Radix UI for component behavior. Radix provides unstyled, accessible component primitives that handle complex UI patterns: dialogs, dropdown menus, popovers, tabs, accordions, data tables, and more. These primitives handle keyboard navigation, focus management, ARIA attributes, and screen reader support — the hard parts of UI development that most developers get wrong.

**Tailwind CSS for Styling** — Every component is styled with Tailwind CSS utility classes. This means no separate CSS files, no CSS-in-JS runtime overhead, and full access to Tailwind's design token system (colors, spacing, typography, shadows) for customization. If you know Tailwind, you can customize any shadcn/ui component instantly.

**Accessible by Default** — Because they're built on Radix primitives, shadcn/ui components handle accessibility correctly out of the box. Keyboard navigation, focus trapping, ARIA roles, and screen reader announcements are all handled correctly — no extra effort required from the developer.

**Figma-to-Code Alignment** — The components are designed in Figma with Tailwind-compatible design tokens, making it straightforward for designers and developers to collaborate with shared language and values.

**CLI Tool** — The `shadcn-ui` CLI (`npx shadcn-ui@latest init`) initializes the project with a configuration file (`components.json`) that specifies where components are installed, which Tailwind config to use, and which CSS variables to apply. The `add` command pulls individual components.

## How It Works

**Installation** — Initialize shadcn/ui in an existing Next.js, Vite, or other React project:

```bash
npx shadcn-ui@latest init
```

The init command creates `components.json` with your preferences and adds a base CSS file with CSS custom properties (design tokens) that control colors, borders, and radii.

**Adding Components** — Add individual components:

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add form
```

Each `add` command creates a file like `components/ui/button.tsx` with the full component source code.

**Using Components** — Import and use directly:

```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

export function MyComponent() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="default">Open Dialog</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>My Dialog</DialogTitle>
        </DialogHeader>
        <Input placeholder="Enter your name..." />
      </DialogContent>
    </Dialog>
  )
}
```

**Customization via Tailwind** — Since you own the code, override any class:

```tsx
// Custom button with specific branding
<Button className="bg-[#1a1a2e] text-white hover:bg-[#16213e] rounded-full px-8">
  Get Started
</Button>
```

## Practical Applications

**Rapid UI Development** — shadcn/ui accelerates building polished admin dashboards, marketing sites, and internal tools. The components are production-ready with sensible defaults, so developers spend time on business logic rather than reinventing dropdown menus and modals.

**Design System Foundations** — Teams adopting shadcn/ui as the foundation of a custom design system can extend it with brand-specific colors, typography, and components while inheriting the accessibility and structural quality Radix provides.

**Landing Pages and Marketing Sites** — With Tailwind's utility classes and shadcn/ui's polished components, building high-conversion landing pages is significantly faster than with CSS-only approaches or inflexible component libraries.

**AI Agent Interfaces** — Particularly relevant for AI agent UIs, where you need chat interfaces, command palettes, dropdown menus, toasts, and data tables that feel premium. shadcn/ui's dark mode support and composability make it ideal for AI product interfaces.

**Dashboard and Data Visualization** — Built-in support for data tables, charts (via Recharts integration), cards, and forms makes building data-rich dashboards straightforward.

## Examples

**Form with shadcn/ui and React Hook Form:**

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

const formSchema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "Password must be 8+ characters"),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", password: "" },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log("Login:", values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">Sign In</Button>
      </form>
    </Form>
  )
}
```

**Dark mode toggle with next-themes:**

```tsx
"use client"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  const { setTheme, theme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
```

## Related Concepts

- [[radix-ui]] — The underlying accessible component primitives that shadcn/ui builds upon
- [[design-systems]] — The broader discipline of creating consistent, reusable UI at scale
- [[Tailwind CSS]] — The utility-first CSS framework used for styling shadcn/ui components
- [[React]] — The UI library/framework that shadcn/ui components are built for
- [[next-js]] — The React framework commonly paired with shadcn/ui for production applications

## Further Reading

- shadcn/ui Official Site — shadcn-ui.com
- Radix UI Documentation — radix-ui.com — the underlying primitives
- Tailwind CSS Documentation — tailwindcss.com
- "Why I Use shadcn/ui Instead of Material UI" — various blog posts comparing approaches
- shadcn/ui GitHub Repository — github.com/radix-ui/primitives

## Personal Notes

shadcn/ui is the clearest example of "the ecosystem evolving past component libraries" that I've seen. The copy-paste model is not a regression — it's empowerment. When you own the component code, you can fix bugs, add features, and customize styles without waiting for a library maintainer to merge your PR. The design quality is consistently excellent — these components look like they belong in a premium SaaS product, not a generic admin template. If you're starting a new React project in 2026 and not using shadcn/ui, you're doing extra work. Pair it with Tailwind, zod for validation, react-hook-form for forms, and next-themes for dark mode, and you have a world-class UI stack that's fully in your control.
