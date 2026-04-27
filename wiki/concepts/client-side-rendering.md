---
title: "Client Side Rendering"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [web-development, javascript, react, frontend, rendering-strategies]
---

# Client Side Rendering

## Overview

Client Side Rendering (CSR) is a web page loading technique where the browser downloads a minimal HTML shell and then renders the entire page content using JavaScript running in the browser. Instead of the server generating complete HTML for each page, the server sends a mostly empty HTML document along with JavaScript bundles. The browser downloads and executes those bundles, which then construct the Document Object Model (DOM) dynamically, populating the page with content fetched from APIs.

CSR became the dominant rendering strategy with the rise of single-page application (SPA) frameworks like React, Vue, and Angular in the mid-2010s. It enables highly interactive, app-like web experiences where page transitions happen without full browser refreshes. However, CSR comes with trade-offs around initial load performance, SEO, and Time-to-Interactive (TTI) that have driven the emergence of hybrid rendering approaches like [[Server Side Rendering]] (SSR), [[Static Site Generation]] (SSG), and modern frameworks like Next.js that combine multiple strategies.

## Key Concepts

**Single Page Application (SPA)** — A web application that loads once and then handles all subsequent navigation via JavaScript routing, avoiding full page reloads. React Router, Vue Router, and Angular Router are common libraries that manage SPA navigation. In a true SPA, the browser never performs a traditional page navigation; instead, JavaScript intercepts link clicks and updates the URL and content programmatically.

**JavaScript Bundle** — The compiled JavaScript code that contains the application logic, component definitions, and routing logic. Large bundle sizes are a common CSR performance problem because the browser must download, parse, and execute the entire bundle before the page becomes interactive.

**Hydration** — The process by which server-rendered HTML is "enhanced" by attaching JavaScript event handlers to make it interactive. In SSR/CSR hybrid setups (like Next.js pages that are rendered on the server but also hydrated on the client), hydration reconciles the server-generated HTML with the client-side React/Vue component tree. Mismatches between server and client renders can cause hydration errors.

**Time to First Byte (TTFB)** — A metric measuring how quickly the server responds. CSR pages typically have fast TTFB because the server is just serving static files, but they then wait for JavaScript to download and execute before showing content, resulting in poor Largest Contentful Paint (LCP) scores.

**Web Vitals** — Google's framework for measuring user experience: LCP (Largest Contentful Paint), FID/INP (Interaction to Next Paint), and CLS (Cumulative Layout Shift). CSR often scores poorly on LCP because the initial HTML contains no meaningful content, delaying when the browser can render anything visible.

**Code Splitting** — The practice of breaking the JavaScript bundle into smaller chunks loaded on demand. Dynamic `import()` statements allow routes or components to be lazy-loaded, reducing initial bundle size and improving TTI. This is a standard optimization for CSR applications.

## How It Works

A typical CSR flow with React looks like this:

1. User navigates to `https://myapp.com/` in the browser.
2. Server responds with a minimal `index.html` containing only a `<div id="root">` and `<script>` tags loading the JS bundle.
3. Browser downloads the HTML (which is nearly empty) and begins downloading the JavaScript bundle.
4. Once the bundle is downloaded, the browser parses and executes it (the "parse and execute" phase).
5. React (or Vue/Angular) runs, creates a virtual DOM, and renders the actual page content into the `#root` div.
6. If the app fetches data from APIs, additional network requests are made and the UI updates as data arrives.
7. The page is now fully interactive.

```html
<!-- index.html served by the server -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My CSR App</title>
</head>
<body>
  <div id="root"></div>
  <!-- This is the ONLY meaningful content in the initial HTML -->
  <script type="module" src="/static/js/bundle.js"></script>
</body>
</html>
```

```javascript
// The React component that actually renders the page content
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
```

## Practical Applications

- **Dashboards and Admin Panels** — Highly interactive data visualization apps where SEO is irrelevant and interactivity is paramount.
- **Social Media Feeds** — Infinite scroll, real-time updates, and complex client-side state management are natural fits for CSR.
- **SaaS Web Applications** — Like Figma, Linear, or Notion, where the app feels like native software.
- **Progressive Web Apps (PWAs)** — CSR frameworks pair well with service workers for offline functionality and caching strategies.
- **Rich Interactive Portals** — Sites where most content is behind authentication and doesn't need search engine indexing.

## Examples

**Create React App (CRA)** — A popular starter kit that configures webpack to build a CSR React app. It scaffolds an `index.html`, `index.js` entry point, and App component. The entire React app runs in the browser with no server-side rendering.

**Gatsby** — A React-based framework that uses SSR at build time to generate static HTML (SSG), but also hydrates into a CSR SPA after load. Gatsby bridges the gap between static and dynamic.

**Vite + React** — Modern build tooling that supports on-demand module loading via ES modules. During development, Vite serves individual modules natively without bundling, making CSR apps feel instant. Production builds still bundle everything for performance.

**React Router in a CSR App** — The router intercepts navigation events and updates the component tree without triggering browser navigation:

```javascript
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function Home() { return <h1>Welcome Home</h1>; }
function About() { return <h1>About Us</h1>; }

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link> | <Link to="/about">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## Related Concepts

- [[Server Side Rendering]] — Rendering HTML on the server for faster initial loads and better SEO
- [[Static Site Generation]] — Pre-building HTML pages at build time for maximum performance
- [[Single Page Application]] — Applications that load once and handle navigation client-side
- [[React]] — The most popular library used for building CSR applications
- [[Hydration]] — Attaching client-side JavaScript to server-rendered HTML
- [[Web Vitals]] — Metrics for measuring page performance (LCP, INP, CLS)
- [[Code Splitting]] — Breaking JS bundles into smaller chunks for faster loading

## Further Reading

- "Rendering on the Web" — Google Web Dev guide comparing SSR, CSR, SSG, and hybrid approaches.
- "React DOM Architecture" — Official React documentation on client-side rendering internals.
- "Web Vitals" — Google's documentation on Core Web Vitals and performance measurement.
- "Building a Single Page Application" — MDN guide to SPA concepts and implementation.

## Personal Notes

CSR was initially celebrated as the future of web development, and in many ways it delivered: SPAs revolutionized user experience expectations for web apps. But the pendulum has swung back toward hybrid approaches as the community absorbed lessons about initial load pain and SEO challenges. The modern "meta-framework" landscape (Next.js, Nuxt, SvelteKit) is really about giving developers fine-grained control over rendering strategy per route, rather than committing wholesale to CSR or SSR. The right answer is almost always "it depends" — and the best modern tools let you mix and match.
