---
title: Server Side Rendering
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ssr, web-development, react, nextjs, rendering]
---

## Overview

Server-Side Rendering (SSR) is a web page rendering technique where the server generates complete HTML for a page on each request, rather than sending an empty HTML shell to be populated by JavaScript in the browser. In SSR, the server executes application logic and renders components to HTML, then sends the fully formed document to the client. This approach improves initial page load time, enhances SEO, and provides better support for browsers with JavaScript disabled or limited capabilities.

## Key Concepts

**Hydration**: After the server-rendered HTML arrives, the browser parses it and displays content immediately. Then JavaScript loads and "hydrates" the static HTML—attaching event listeners and making it interactive. Modern frameworks like React and Vue handle hydration differently, with optimizations like resumability (Qwik) and selective hydration (React 18 streaming).

**Streaming SSR**: React 18 introduced streaming rendering where the server sends HTML in chunks as components render, allowing the browser to display content progressively. This improves perceived performance for pages with slow components at the bottom.

**Edge Rendering**: Rendering at CDN edge locations rather than origin servers reduces latency by generating HTML geographically closer to users. Cloudflare Workers, Vercel Edge Functions, and Deno Deploy support this pattern, combining SSR with CDN benefits.

**Static vs Dynamic Rendering**: Some pages can be pre-rendered at build time (Static Site Generation/SSG) while others require fresh data per request. Hybrid frameworks like Next.js support both via `getStaticProps` and `getServerSideProps`, choosing per-page.

## How It Works

The SSR lifecycle differs from client-side rendering:

```text
1. Browser sends HTTP request
2. Server receives request
3. Server executes page component (API calls, database queries)
4. Server renders component tree to HTML string
5. Server sends complete HTML document with embedded data
6. Browser renders HTML immediately (First Contentful Paint)
7. JavaScript bundle downloads
8. Hydration: React/Vue attaches to HTML, establishes reactivity
9. Page becomes interactive (Time to Interactive)
```

Traditional SSR (Next.js Pages Router, Vue SSR):
```javascript
// Next.js Pages Router SSR
export async function getServerSideProps() {
  const data = await fetchDataFromAPI();
  return { props: { data } };
}
```

Next.js App Router (React Server Components) represents a shift where components render on server by default, with client components explicitly marked.

## Practical Applications

SSR is essential for content-heavy sites requiring SEO (blogs, e-commerce, marketing pages) and applications where initial load performance directly impacts user engagement. News sites, documentation portals, and product catalogs benefit from instant first-paint and crawlable content. Applications requiring authentication state based on cookies or headers also favor SSR since server code can read cookies directly.

## Examples

- **Next.js**: The most popular SSR framework for React, with App Router as the modern standard
- **Nuxt.js**: Vue's SSR framework with similar conventions to Next.js
- **Remix**: Framework focused on web standards with progressive enhancement
- **Angular Universal**: Angular's SSR solution for Angular applications

```javascript
// Next.js App Router Server Component
async function BlogPost({ params }) {
  const post = await db.posts.find(params.slug);
  return <article>{post.content}</article>;
}
```

## Related Concepts

- [[Single Page Applications]] - CSR counterpart that SSR often replaces
- [[Client Side Rendering]] - Alternative rendering strategy
- [[Static Site Generation]] - Pre-rendering at build time
- [[Search Engine Optimization]] - SEO benefits of SSR
- [[Web Performance]] - Core metrics SSR improves (FCP, LCP)

## Further Reading

- [React SSR Documentation](https://react.dev/reference/react-dom/server)
- [Next.js Rendering Documentation](https://nextjs.org/docs/app/building-your-application/rendering)
- [Web.dev: Rendering on the Web](https://web.dev/articles/rendering-on-the-web)

## Personal Notes

SSR vs CSR isn't binary anymore—modern apps use hybrid approaches. Next.js App Router's Server Components changed the calculus by reducing client bundle size. I still reach for SSR whenever SEO matters or TTI (Time to Interactive) on slow devices is a concern. The hydration step remains the tricky part—mismatches between server and client state cause hydration errors.
