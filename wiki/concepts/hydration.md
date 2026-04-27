---
title: "Hydration"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [hydration, ssr, web-development, javascript]
---

# Hydration

Hydration is the process of attaching client-side JavaScript behavior to server-rendered HTML, enabling the static markup produced by the server to become interactive. In a typical [[SSR]] workflow, the server generates complete HTML and sends it to the browser, where it is displayed immediately. However, this HTML is inert—it has no event listeners, no reactive state, and does not respond to user interactions. Hydration bridges this gap by having the client-side JavaScript "take over" the static HTML, attaching all necessary handlers and initializing the application state without re-rendering the DOM.

## Overview

When a server renders a page using frameworks like React, Vue, or Svelte, it produces HTML that visually represents the component tree at the moment of rendering. This HTML includes elements with attributes like `data-reactid` or similar framework-specific markers that allow the client-side runtime to identify which server-rendered element corresponds to which component in the virtual DOM.

The hydration process begins after the browser downloads the JavaScript bundles associated with the page. The framework's client-side runtime loads, parses the server-rendered HTML, and compares it against the expected component output. Instead of replacing the HTML entirely (which would cause a flicker and lose the performance benefit of SSR), it incrementally attaches event listeners, initializes component state, and sets up reactivity systems. The result is a seamless transition where content appears instantly from the server render but becomes fully interactive once JavaScript completes its hydration phase.

This distinction between server-rendered content and client-side interactivity is fundamental to understanding why hydration exists. The server produces HTML for fast initial delivery and search engine indexing, while the client-side JavaScript adds the dynamic behavior that users expect from modern web applications. Without hydration, users would see a page that looks correct but becomes unresponsive the moment they try to interact with it.

## Why It Matters

Hydration is critical to the user experience in [[SSR]] applications. The primary goal of server-side rendering is to improve perceived performance by delivering meaningful content faster—the browser can paint the page before any JavaScript loads. However, this advantage would be lost if the page remained non-interactive until a full client-side re-render occurred. Hydration ensures that the performance benefits of SSR are preserved while maintaining the rich interactivity that modern applications require.

From a performance perspective, hydration represents a trade-off. The server provides fast first contentful paint, but users still need to wait for JavaScript to download, parse, and execute before the page becomes interactive. This waiting period is sometimes called "time to interactive" (TTI), and it is a key metric for measuring the responsiveness of web applications. Optimizing hydration strategies can significantly reduce TTI and improve the overall user experience.

Hydration also has important implications for accessibility and SEO. Server-rendered HTML is immediately available to assistive technologies and search engine crawlers, but only if the content is actually present in the initial HTML. If hydration were to replace server content with client-rendered content, crawlers that do not execute JavaScript might see different content than users. Properly implemented hydration preserves the integrity of server-rendered content across all contexts.

Another consideration is the developer experience. Frameworks that support hydration must carefully manage the boundary between server and client rendering, ensuring that components behave consistently in both environments. This requires understanding which APIs are available on the server versus the client, and designing components that can render correctly in both contexts—a concept sometimes called [[Isomorphic JavaScript]].

## Strategies

Several strategies exist for optimizing the hydration process, each with different trade-offs between performance, complexity, and user experience.

**Full Hydration** is the traditional approach where the entire page is hydrated at once. All JavaScript must be loaded and executed before any interactivity is enabled. While simple to implement, this can lead to slow TTI on pages with large JavaScript bundles, as users cannot interact with any part of the page until hydration completes.

**Progressive Hydration** addresses this by hydrating components incrementally, typically prioritizing above-the-fold content and deferring less critical sections. This allows users to interact with key parts of the page while other components continue hydrating in the background. React's `lazy` components with Suspense exemplify this approach, allowing developers to defer loading of component code until it is needed.

**Partial Hydration** takes the concept further by only hydrating components that require client-side interactivity, leaving static content permanently server-rendered without any JavaScript overhead. Frameworks like Astro pioneered this approach, sometimes called "island architecture," where interactive components are isolated islands within a sea of static HTML. This can dramatically reduce the amount of JavaScript that needs to be shipped to the client.

**Resumability** is a strategy employed by frameworks like Qwik, where the server serializes not just the HTML but also the component state and event handlers into the HTML itself. When the user interacts with an element, only the specific handler for that interaction needs to be loaded and executed. This avoids the need for a hydration phase entirely, as the page is immediately interactive from the moment it loads.

**Selective Hydration** is a React 18 feature that handles hydration of components wrapped in Suspense boundaries automatically. Rather than requiring developers to manually code progressive loading, React automatically prioritizes visible content and defers hidden or lower-priority components. This reduces the cognitive load on developers while providing good performance out of the box.

Choosing the right hydration strategy depends on the specific requirements of the application. Content-heavy sites with minimal interactivity may benefit from partial hydration or resumability, while highly interactive applications may prefer progressive or selective hydration to balance responsiveness with functionality.

## Related

- [[SSR]] - Server-Side Rendering, the technique that produces the HTML which hydration attaches to
- [[SSG]] - Static Site Generation, which can benefit from hydration in hybrid applications
- [[JavaScript]] - The client-side language that performs hydration
- [[Performance Optimization]] - Improving metrics like Time to Interactive through hydration strategies
- [[Next.js]] - A framework with sophisticated hydration support and optimizations
- [[Isomorphic JavaScript]] - Code that runs on both server and client, relevant to hydration architecture
