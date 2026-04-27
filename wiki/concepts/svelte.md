---
title: Svelte
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [svelte, javascript, framework, frontend, reactive, compile]
---

# Svelte

## Overview

Svelte is a front-end framework that takes a fundamentally different approach from React and Vue: rather than shipping a runtime that reconciles virtual DOM diffs, Svelte compiles components at build time into highly efficient, direct DOM manipulation code. The result is smaller bundles, faster runtime performance, and a component authoring experience that feels closer to writing vanilla HTML, CSS, and JavaScript than working with a heavy framework abstraction.

Svelte was created by Rich Harris and first released in 2016. It has gone through major revisions—Svelte 3 in 2019 introduced the reactive declaration syntax that became its signature, Svelte 4 refined stores and transitions, and Svelte 5 (runes) introduced a new reactive primitive system. The framework is particularly popular in the [[javascript]] ecosystem for applications where performance and bundle size matter, and it has a dedicated following among developers who prefer a less opinionated, more "vanilla" development experience.

## Key Concepts

- **Compile-time reactivity**: Svelte shifts reactivity from runtime diffing to compile-time analysis. When you write `<script>` tags and `let` declarations, the compiler generates precise DOM update instructions.
- **Runes (Svelte 5)**: The new reactive primitive system replacing the Svelte 3/4 `export let`, `$:`, and `store` patterns. Runes are explicit signals (`$state`, `$derived`, `$effect`) that work consistently inside and outside components.
- **Stores**: Cross-component state management via writable/ readable stores that components subscribe to. Still widely used in Svelte 3/4 projects.
- **No virtual DOM**: Svelte updates the DOM directly. Without the diffing overhead, Svelte applications typically outperform React equivalents in benchmarks.
- **Scoped styles**: CSS inside a `.svelte` file is automatically scoped to that component, eliminating class name collisions.
- **Transitions and animations**: Built-in transition directives (`fade`, `fly`, `slide`) make animations declarative and easy.

## How It Works

A `.svelte` file combines HTML-like markup, a `<script>` block for logic, and a `<style>` block for scoped CSS. The compiler transforms this into a JavaScript module that surgically updates only the DOM nodes that changed.

```svelte
<!-- Counter.svelte -->
<script>
  let count = $state(0);      // Svelte 5 rune for reactive state

  function increment() {
    count += 1;
  }

  $derived.double = () => count * 2;  // derived value
</script>

<button onclick={increment}>
  Count: {count}, Double: {double}
</button>

<style>
  button {
    padding: 0.5rem 1rem;
    background: #ff3e00;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>
```

The compiler transforms this into something like:

```javascript
// Generated (simplified)
import { mount } from 'svelte';
function create_fragment(ctx) {
  let button = document.createElement('button');
  button.addEventListener('click', ctx.increment);
  return { mount(element) { element.appendChild(button); } };
}
// Updates are surgical: only the text node inside the button changes
```

## Practical Applications

- **High-performance dashboards**: Where every millisecond of interaction latency matters
- **Mobile-first web apps**: Smaller bundle sizes benefit users on slower networks
- **Data visualization**: Fine-grained reactivity for charts and graphs that update frequently
- **Progressive web apps (PWAs)**: SvelteKit provides routing, SSR, and offline support
- **Embedded widgets**: Lightweight components to drop into existing pages

## Examples

### SvelteKit Full-Stack Page

```typescript
// src/routes/posts/[slug]/+page.ts
export async function load({ params, fetch }) {
  const res = await fetch(`/api/posts/${params.slug}`);
  return { post: await res.json() };
}

// src/routes/posts/[slug]/+page.svelte
<script>
  let { data } = $props();
</script>

<h1>{data.post.title}</h1>
<article>{@html data.post.content}</article>
```

### Reactive Store (Svelte 3/4 style)

```javascript
// stores.js
import { writable, derived } from 'svelte/store';

export const count = writable(0);
export const double = derived(count, $count => $count * 2);

export const cart = writable({ items: [], total: 0 });
cart.update(c => ({
  ...c,
  items: [...c.items, 'new item'],
  total: c.total + 1
}));
```

### Fetching and Displaying Data

```svelte
<script>
  let { postId } = $props();
  let post = $state(null);
  let loading = $state(true);

  $effect(() => {
    fetch(`/api/posts/${postId}`)
      .then(r => r.json())
      .then(data => {
        post = data;
        loading = false;
      });
  });
</script>

{#if loading}
  <p>Loading...</p>
{:else if post}
  <h1>{post.title}</h1>
  <p>{post.excerpt}</p>
{:else}
  <p>Post not found.</p>
{/if}
```

## Related Concepts

- [[javascript]] — The language Svelte compiles to
- [[frontend]] — The broader discipline of building user-facing web applications
- [[http]] — Used for fetching data in SvelteKit load functions and `$effect`
- [[performance-testing]] — Benchmarking Svelte apps against other frameworks
- [[typescript]] — Svelte and SvelteKit have first-class TypeScript support

## Further Reading

- Svelte Documentation — svelte.dev/docs
- "Runes" — Svelte 5's new reactivity system: https://svelte.dev/blog/runes
- Rich Harris, "Virtual DOM is pure overhead" — the original motivation talk

## Personal Notes

Svelte's steepest learning curve isn't the syntax—it's unlearning the React mental model. Once you stop thinking in terms of component trees with diff reconciliation and start thinking in terms of direct DOM updates, everything clicks. Svelte 5's runes make reactivity more explicit and easier to reason about, though the migration from Svelte 3/4 stores has some friction. For new projects, SvelteKit is the clear choice—it handles routing, server-side rendering, and API routes elegantly. The ecosystem is smaller than React's, but the quality of libraries (Svelte Motion, Threlte for 3D) is excellent.
