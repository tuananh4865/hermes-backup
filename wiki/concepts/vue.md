---
title: "Vue.js"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [vue, javascript, frontend, framework, web-development]
---

# Vue.js

## Overview

Vue.js is a progressive, open-source JavaScript framework for building user interfaces and single-page applications (SPAs). Created by Evan You and first released in 2014, Vue was designed from the ground up to be incrementally adoptable—meaning you can use as much or as little of it as your project requires. Unlike monolithic frameworks that demand a full commitment, Vue lets developers drop it into a project as a simple script tag for basic interactivity, or scale it up to a full-featured SPA with routing, state management, and build tooling for complex enterprise applications.

Vue's core library focuses exclusively on the view layer, adopting a component-based architecture where UIs are decomposed into reusable, self-contained pieces. Each Vue component encapsulates its own template (HTML structure), logic (JavaScript), and styling (CSS). This encapsulation makes Vue applications easier to reason about, test, and maintain, especially as codebases grow in size.

Vue occupies a unique position in the frontend landscape: it offers the reactivity and component model that developers love about [[React]], while maintaining a syntax and structure that beginners find accessible. Its gentle learning curve, excellent documentation, and active community have made it one of the most popular JavaScript frameworks in use today, employed by organizations ranging from independent freelancers to large enterprises like Alibaba, GitLab, and Nintendo.

## Key Concepts

Several core concepts form the foundation of Vue.js development.

**Reactivity** is Vue's crown jewel. In Vue 3 (the current major version), a reactive system is built on top of JavaScript Proxies. When you declare reactive state, Vue automatically tracks dependencies and re-renders only the components that depend on changed data. This fine-grained reactivity eliminates the need for manual DOM manipulation or virtual DOM diffing at the component level, resulting in highly performant applications.

```javascript
import { ref, reactive, computed } from 'vue'

// Primitive reactivity with ref
const count = ref(0)
count.value++ // triggers re-render in templates

// Object reactivity with reactive
const state = reactive({
  message: 'Hello Vue',
  items: ['apple', 'banana']
})

// Computed properties
const doubledCount = computed(() => count.value * 2)
```

**Components** are the primary building blocks in Vue. A component can receive data from its parent via `props` and emit events upward. Vue components support both Options API (the classic, more verbose approach using `data`, `methods`, `computed`, etc.) and the newer Composition API (which uses functions like `ref` and `reactive` directly, enabling better TypeScript support and reusable logic extraction via composables).

**Single File Components (SFCs)** use the `.vue` file extension and bundle template, script, and style into a single file. Build tools like Vite and Webpack parse SFCs using vue-loader or vite-plugin-vue, extracting and processing each section appropriately.

**Directives** are special attributes prefixed with `v-` that add reactive behavior to templates. Built-in directives include `v-if` and `v-for` for conditional rendering and list rendering, `v-bind` for attribute binding (often shortened to `:`), `v-on` for event handling (shortened to `@`), and `v-model` for two-way data binding on form inputs.

## How It Works

Vue's runtime consists of several interconnected parts that work together to render your application.

At its heart, Vue uses a virtual DOM—an in-memory representation of the actual DOM. When reactive state changes, Vue computes the minimum number of DOM updates needed and applies them batched in the next update cycle. Vue 3's compiler can also generate optimized code at build time, known as "compile-time hoisting," which reduces runtime overhead significantly.

The component lifecycle follows a well-defined sequence: when a component is created, Vue sets up reactivity (making data reactive), compiles the template, mounts the component to the DOM, and then keeps it updated as state changes. Lifecycle hooks like `onMounted`, `onUpdated`, and `onUnmounted` allow developers to inject custom logic at specific points in this lifecycle.

Vue Router handles client-side routing, mapping URL paths to specific components and enabling navigation without page reloads. Pinia (the officially recommended store) manages global application state, providing a simple API for shared data that multiple components need to access.

## Practical Applications

Vue is versatile enough to power a wide range of applications:

- **Content Management Systems (CMS)**: Vue's simplicity and performance make it popular for admin dashboards and content-heavy applications.
- **E-commerce Platforms**: Progressive enhancement allows e-commerce sites to add interactivity (cart updates, filtering, search) without a full SPA architecture.
- **SaaS Applications**: Vue's component model scales well for large teams building complex, feature-rich business tools.
- **Progressive Web Apps (PWAs)**: Vue's ecosystem includes `@vitejs/plugin-pwa` for building offline-capable, installable web applications.

## Examples

A simple Vue component demonstrating the Options API:

```vue
<template>
  <div class="greeting">
    <h1>{{ greeting }}</h1>
    <p>Count: {{ count }}</p>
    <button @click="increment">Increment</button>
    <ul>
      <li v-for="item in items" :key="item.id">{{ item.name }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      greeting: 'Welcome to Vue!',
      count: 0,
      items: [
        { id: 1, name: 'First item' },
        { id: 2, name: 'Second item' }
      ]
    }
  },
  methods: {
    increment() {
      this.count++
    }
  }
}
</script>

<style scoped>
.greeting {
  font-family: sans-serif;
  padding: 1rem;
}
button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
```

## Related Concepts

- [[frontend]] — The broader discipline of building user-facing web interfaces
- [[javascript]] — The programming language Vue is built upon
- [[react]] — A competing UI library with a similar component model
- [[typescript]] — A typed superset of JavaScript, well-supported in Vue 3
- [[webpack]] — A module bundler commonly used with Vue projects

## Further Reading

- [Vue.js Official Documentation](https://vuejs.org/) — Comprehensive guides and API reference
- [Vue School](https://vueschool.io/) — Video tutorials and courses
- [Vue Mastery](https://www.vuemastery.com/) — Another excellent learning platform

## Personal Notes

Vue strikes the best balance between approachability and power among the major frontend frameworks. The single-file component format is intuitive and keeps related concerns together. The Composition API in Vue 3 is a significant improvement, especially for TypeScript users and for extracting reusable logic into composables (the Vue equivalent of React hooks custom hooks). The community-maintained Vue ecosystem is rich but can occasionally feel fragmented compared to React's more centralized tooling landscape.
