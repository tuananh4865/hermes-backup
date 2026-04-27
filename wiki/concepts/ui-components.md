---
title: UI Components
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ui-components, frontend, design-systems]
---

# UI Components

## Overview

UI components are reusable interface elements that encapsulate structure, styling, and behavior into self-contained building blocks. Buttons, inputs, cards, modals, and navigation bars are all classic examples of UI components. Rather than building each instance from scratch, developers compose applications from component libraries, achieving consistency and reducing duplication across an application.

A well-designed UI component exposes a clear interface—typically through properties (props), events, and slots—that controls its appearance and behavior without exposing internal implementation details. This separation of concerns allows designers and developers to work independently: designers can update visual systems while engineers integrate components without touching their logic.

Components exist on a spectrum from primitive to composite. Primitive components (atoms) handle basic elements like text or icons. Composite components (molecules or organisms) combine primitives into more complex structures, such as a search bar that combines an input field, a button, and a clear indicator.

## Component Libraries

Modern frontend frameworks ship with or rely on component libraries that provide production-ready UI elements.

**React** has the largest ecosystem. Popular libraries include [[shadcn-ui]], [[radix-ui]] (uncontrolled, accessible primitives), [[material-ui]] (MUI), and [[chakra-ui]]. React's component model uses props for data flow and hooks like [[hooks]] for managing state and side effects.

**SwiftUI** is Apple's declarative framework for building UIs across iOS, macOS, and watchOS. It uses a compositional syntax where views are constructed by chaining modifiers. SwiftUI components are strongly typed and integrate natively with [[swift]] and Apple's developer tools.

**Other notable libraries:**
- [[vue]] with Vuetify and Nuxt UI
- [[nextjs]] with its built-in component patterns
- [[svelte]] with SvelteKit component libraries
- Flutter's extensive widget ecosystem for cross-platform mobile

Enterprise teams often build internal [[design-systems]] that standardize components organization-wide, ensuring brand consistency and reducing the learning curve across projects.

## Composition

Composition is the practice of building complex UIs by combining smaller components. Rather than inheritance hierarchies, modern UI frameworks favor composition: a `Card` component might contain `Button`, `Image`, and `Text` components, each with their own props.

Key composition patterns include:

- **Children props / slots**: Passing content into components to be rendered within their boundaries
- **Compound components**: Related components (like `Tabs`, `TabList`, `TabPanel`) that share state implicitly
- **Higher-order components (HOCs)**: Functions that wrap components to add behavior
- **Render props**: Components that accept render functions as props for maximum flexibility

Effective composition requires thoughtful API design. Components should be loosely coupled, highly cohesive, and follow the single responsibility principle—each component does one thing well.

## Related

- [[design-systems]] — Organizational systems for UI consistency
- [[frontend]] — broader web development context
- [[react]] — dominant component-based framework
- [[hooks]] — React's state and lifecycle patterns
- [[swiftui]] — Apple's declarative UI framework
- [[state]] — Managing data within components
- [[props]] — Component inputs and interfaces
