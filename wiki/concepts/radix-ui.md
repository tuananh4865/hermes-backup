---
title: Radix UI
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ui, components, react, headless, accessible, design-system, primitives]
---

# Radix UI

## Overview

Radix UI is a headless (unstyled) UI component library for React that provides accessible, production-ready components as building blocks for design systems. Unlike traditional component libraries that come with opinionated styles and visual designs, Radix provides the behavioral logic—the interactions, accessibility attributes, and keyboard navigation—without imposing any visual styling. This "headless" approach gives developers complete control over appearance while ensuring their applications are accessible by default.

The library emerged from the recognition that building accessible, interactive UI components is surprisingly complex. A simple dropdown menu, for instance, requires managing focus states, keyboard navigation (arrow keys, escape, enter), screen reader announcements, touch support, and proper ARIA attributes. Doing this correctly for every component is time-consuming and error-prone. Radix encapsulates this complexity into primitives that handle the hard parts, leaving visual implementation to developers.

Radix powers popular design systems including [[shadcn-ui]], which provides beautiful pre-styled components built on Radix primitives. This layered approach—behavior primitives plus styled implementations—offers both flexibility and speed.

## Key Concepts

### Headless Architecture

Radix components provide zero styles out of the box. This is intentional:

```
Traditional Component Library:
┌─────────────────────────────┐
│ Button + Styles + Behavior  │  ← Coupled, hard to customize
└─────────────────────────────┘

Radix Headless Approach:
┌──────────────┐  +  ┌──────────────────┐
│ Radix Primit │  +  │ Your Custom Styles│  ← Separated concerns
└──────────────┘     └──────────────────┘
```

### Accessibility by Default

Every Radix component is built with accessibility at the core:

```tsx
import * as Dialog from '@radix-ui/react-dialog';

function MyModal({ open, onOpenChange, children }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="modal-overlay" />
        <Dialog.Content className="modal-content">
          <Dialog.Title>Dialog Title</Dialog.Title>
          <Dialog.Description>
            Screen readers automatically announce this description.
          </Dialog.Description>
          {children}
          {/* Focus is trapped automatically */}
          {/* Escape key closes automatically */}
          {/* Background scroll is locked automatically */}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

The component handles:
- Focus management and trapping
- ARIA attribute management
- Keyboard navigation
- Screen reader announcements
- Touch/click outside detection
- Scroll lock when open

### Component Collection

Radix provides primitives for most common UI patterns:

| Component | Purpose |
|-----------|---------|
| Dialog | Modal dialogs, alerts, floating panels |
| Dropdown Menu | Context menus, navigation menus |
| Popover | Tooltips, floating panels, hover cards |
| Tabs | Tabbed interfaces |
| Accordion | Collapsible sections |
| Toast | Notifications, alerts |
| Tooltip | Hover hints |
| Slider | Range inputs |
| Switch | Toggle switches |
| Checkbox | Checkbox inputs with indeterminate state |
| Radio Group | Radio button collections |
| Select | Custom select dropdowns |

## How It Works

### Component API Design

Radix uses a compositional API where components are built from smaller parts:

```tsx
import * as NavigationMenu from '@radix-ui/react-navigation-menu';

function MyNav() {
  return (
    <NavigationMenu.Root>
      <NavigationMenu.List>
        <NavigationMenu.Item>
          <NavigationMenu.Trigger>Products</NavigationMenu.Trigger>
          <NavigationMenu.Content>
            {/* Content with automatic viewport collision detection */}
          </NavigationMenu.Content>
        </NavigationMenu.Item>
      </NavigationMenu.List>
    </NavigationMenu.Root>
  );
}
```

### Slot Pattern

Radix uses the `Slot` pattern to merge props onto the underlying DOM element:

```tsx
import { Slot } from '@radix-ui/react-slot';

function IconButton(props) {
  return (
    <button className="icon-btn" {...props}>
      {props.children}
    </button>
  );
}
```

## Practical Applications

### Building a Design System

```tsx
// button.tsx - Building on Radix primitives
import { Slot } from '@radix-ui/react-slot';
import { type ButtonHTMLAttributes, forwardRef } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost';
  asChild?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'default', className = '', asChild, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    
    return (
      <Comp
        ref={ref}
        className={`btn btn-${variant} ${className}`}
        {...props}
      />
    );
  }
);
```

### Custom Styling with CSS

```css
/* dialog.css */
.modal-overlay {
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  inset: 0;
  animation: overlayShow 150ms cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-content {
  background: white;
  border-radius: 6px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 25px;
  animation: contentShow 150ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes overlayShow {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes contentShow {
  from { opacity: 0; transform: translate(-50%, -48%) scale(0.96); }
  to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}
```

## Related Concepts

- [[shadcn-ui]] — Beautiful component collection built on Radix
- [[design-systems]] — Design system context and principles
- [[react]] — The framework Radix targets
- [[accessibility]] — ARIA, keyboard navigation, screen readers
- [[css-in-js]] — Styling approaches used with Radix
- [[headless-components]] — The headless UI pattern

## Further Reading

- [Radix UI Official Site](https://www.radix-ui.com/)
- [Radix GitHub Repository](https://github.com/radix-ui/primitives)
- [Radix UI Documentation](https://www.radix-ui.com/primitives/docs/overview/introduction)
- [shadcn/ui](https://ui.shadcn.com/)

## Personal Notes

Radix changed how I think about component architecture. The headless approach requires more initial setup but pays dividends in flexibility and accessibility. The shadcn/ui project demonstrates the pattern beautifully—copy-pasteable components with full style control. One gotcha: because Radix doesn't provide styles, documentation can feel incomplete until you realize you're meant to style everything yourself. The tradeoff is worth it for production applications where visual differentiation matters.
