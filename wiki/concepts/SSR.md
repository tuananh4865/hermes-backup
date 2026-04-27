---
title: SSR
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ssr, server-side-rendering, web-development, performance]
---

# SSR

## Overview

Server-Side Rendering (SSR) is a web rendering technique where HTML pages are generated on the server rather than in the user's browser. When a user requests a page from an SSR-enabled website, the server processes the request, executes any necessary application logic, retrieves data from databases or external APIs, and renders the complete HTML document before sending it to the client. This contrasts with [[Client-Side Rendering]] (CSR), where the browser downloads a minimal HTML shell and then builds the entire page using JavaScript.

SSR has become a foundational technique in modern web development, particularly with the rise of frameworks like Next.js, Nuxt, and SvelteKit that provide built-in support for server-side rendering. The approach represents a return to the original model of the web, where servers were responsible for generating HTML, but now combined with the interactivity and dynamic capabilities of modern JavaScript applications.

## How It Works

The SSR lifecycle begins when a user's browser sends an HTTP request to the server. The server receives this request and passes it to the application runtime, which executes the relevant code to generate the page. This typically involves routing the request to the appropriate handler, running any data-fetching logic, and rendering a template or component tree into final HTML.

For example, in a React application using Next.js, when a request arrives for `/products`, the server executes the page component, runs any `getServerSideProps` functions to fetch data, renders the React component tree to HTML, and returns the complete document. The browser receives fully formed HTML and can begin displaying content immediately, even before any JavaScript has loaded or executed.

After the initial HTML is delivered, the browser downloads the JavaScript bundles associated with the page. Once downloaded, the JavaScript executes and "hydrates" the static HTML—attaching event listeners, initializing React state, and enabling full interactivity. This hydration process is critical because it bridges the gap between the server-rendered static content and the dynamic, interactive client-side application. Without proper hydration, the page would appear to render correctly but become unresponsive to user interactions.

The server can also conditionally render content based on request headers, authentication status, or cookies. This makes SSR particularly powerful for applications that need to serve different content to different users, such as personalized dashboards or authenticated dashboards.

## Benefits and Drawbacks

SSR offers several significant advantages for web applications. The most immediate benefit is improved initial page load performance, especially on slower devices or networks, since users see meaningful content faster than with client-side rendering. Search engine crawlers can index the fully rendered HTML directly, which eliminates the need for complex SEO workarounds like pre-rendering or dynamic rendering. Server-side rendering also reduces the computational burden on client devices, making applications more accessible to users on low-powered hardware.

However, SSR also introduces certain challenges. Each page request typically requires the server to execute application code and render HTML, which increases server load and response latency compared to serving static files. This makes SSR applications more resource-intensive to host and scales differently than static or client-rendered applications. Additionally, since rendering happens on the server, sensitive logic or data access must be carefully managed to prevent exposing secrets or private information.

Another drawback is the complexity of managing the boundary between server and client code. Developers must be explicit about which code runs where, and attempting to access browser APIs like `window` or `document` during server-side rendering will cause errors. Modern frameworks handle much of this complexity automatically, but it still requires careful architecture decisions.

## Related

- [[Client-Side Rendering]] - The alternative approach where rendering happens in the browser
- [[Static Site Generation]] - Pre-renders pages at build time for maximum performance
- [[Hydration]] - The process of attaching client-side interactivity to server-rendered HTML
- [[Isomorphic JavaScript]] - JavaScript code that can run on both server and client
- [[Next.js]] - A React framework with first-class SSR support
- [[Performance Optimization]] - Techniques for improving web application speed
