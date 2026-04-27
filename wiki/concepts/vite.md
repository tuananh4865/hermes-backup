---
title: Vite
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [vite, build-tool, frontend, esbuild, web-development]
---

# Vite

## Overview

Vite (French for "fast," pronounced `veet`) is a modern build tool and development server created by Evan You, the creator of [[Vue]]. It was designed to address the slow development experience of traditional bundlers like [[webpack]] by leveraging native ES modules in the browser and modern tooling. Vite has become one of the most widely adopted build tools in the frontend ecosystem, now powering [[Next.js]] (as an optional bundler), [[Svelte]], and countless other frameworks.

The core innovation of Vite is its dev server architecture: instead of bundling the entire application upfront during development, Vite serves files natively via native ES module imports. When a module is imported, Vite transforms it on-the-fly and sends it to the browser. This approach eliminates the漫长的等待 startup time that plagues webpack-based dev servers on large projects, often reducing cold-start times from minutes to milliseconds.

## Key Concepts

### Native ES Module (ESM) Dev Server

Traditional bundlers like webpack process all files and create a single bundled output before serving anything. Vite takes a different approach by acting as a middleware that transforms and serves ES modules on request. The browser requests a module, Vite transforms it (applying [[TypeScript]] compilation, [[CSS]] processing, [[JSX]] transformation, etc.), and delivers it immediately. Only the modules that are actually imported are ever processed.

This has dramatic implications for development speed. A project with 1,000 modules might take 30+ seconds to bundle on first load with webpack. With Vite, the browser loads the entry point instantly and subsequent module loads are parallelized naturally by the browser's module loader.

### Rollup-Based Production Build

While the dev server avoids bundling, Vite uses [[Rollup]] for production builds. Rollup produces highly optimized, tree-shaken bundles with smaller output sizes than webpack in many cases. Vite handles code splitting, chunking strategies, and asset handling through Rollup plugins, ensuring consistent behavior between development and production.

### HMR (Hot Module Replacement)

Vite provides instant hot module replacement that preserves application state. Unlike traditional HMR solutions that reload the entire page or lose component state, Vite's HMR works at the module level. When you edit a file, Vite only needs to re-import that specific module—not the entire dependency graph. This makes the feedback loop during development nearly instantaneous.

### Dependency Pre-Bundling

Vite pre-bundles dependencies using [[esbuild]], a Go-based bundler that is 10-100x faster than JavaScript-based bundlers. CommonJS dependencies that use named imports, packages with many internal modules, and legacy packages are all pre-bundled into ESM format during the initial dev server startup. This one-time cost (cached until `node_modules` changes) dramatically improves subsequent load times.

## How It Works

When you run `vite`, the following sequence occurs:

1. **Server Start**: Vite starts a dev server (typically on port 5173) and watches for file changes.
2. **Browser Request**: The browser requests `index.html`, which contains `<script type="module" src="/src/main.js">`.
3. **Module Resolution**: Vite intercepts the request and resolves the module path, applying any necessary transforms (TypeScript → JavaScript, JSX → function calls, CSS → style injection).
4. **Dependency Scanning**: As the browser parses imported modules, Vite transforms and serves each one on demand.
5. **Pre-bundling**: On first start, Vite uses esbuild to pre-bundle dependencies in `node_modules`, converting CommonJS modules to ESM and collapsing multi-file packages into single files.

For production builds, Vite delegates to Rollup, which performs a full bundling pass, applies tree-shaking, generates optimized chunks, and produces static assets ready for deployment.

## Practical Applications

Vite is used in a wide variety of frontend development scenarios:

- **Vue 3 Applications**: The official Vue CLI and [[create-vue]] both use Vite as the default build tool.
- **React Projects**: [[React]] applications can be scaffolded with `npm create vite@latest`, replacing the older Create React App workflow.
- **Library Development**: Vite's `library mode` produces optimized, tree-shaken bundles suitable for publishing to npm.
- **Monorepo Workspaces**: Vite integrates well with pnpm workspaces and [[npm]] monorepos, allowing shared dependencies to be pre-bundled efficiently.
- **Micro-frontend Architectures**: Vite's speed makes it suitable for developing and testing micro-frontend modules in isolation.

## Examples

A minimal Vite configuration for a React + TypeScript project:

```javascript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    target: 'esnext',
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
  server: {
    port: 3000,
    open: true,
  },
})
```

A typical project structure with Vite:

```
my-project/
├── index.html
├── package.json
├── vite.config.ts
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── components/
│   └── styles/
└── public/
    └── favicon.ico
```

## Related Concepts

- [[webpack]] — Traditional bundler that inspired Vite's architecture
- [[Rollup]] — The bundler powering Vite's production builds
- [[esbuild]] — Go-based bundler used for dependency pre-bundling
- [[frontend]] — Frontend development ecosystem
- [[Next.js]] — Framework that now supports Vite as a bundler option
- [[Svelte]] — Framework that uses Vite as its primary build tool
- [[TypeScript]] — Type superset commonly used with Vite
- [[React]] — Library commonly built with Vite

## Further Reading

- [Vite Official Documentation](https://vite.dev)
- [Vite GitHub Repository](https://github.com/vitejs/vite)
- [Evan You's original announcement of Vite](https://blog.vuejs.org/posts/vite-3)
- [esbuild documentation](https://esbuild.github.io/) — for understanding pre-bundling

## Personal Notes

Vite transformed how I approach frontend development. Cold-start times went from 30+ seconds to under a second on my projects. The best practice I've found is to keep the `optimizeDeps.exclude` list minimal—only excluding packages that cause issues, since excluding too much defeats the pre-bundling benefit. Also, Vite's HMR is not always perfect with stateful components; sometimes a full page reload (`window.location.reload()`) is cleaner than debugging HMR edge cases.
