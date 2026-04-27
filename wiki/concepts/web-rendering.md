---
title: "Web Rendering"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [web-development, rendering, performance, seo, ssr, csr, ssg]
---

# Web Rendering

## Overview

Web rendering refers to the process by which web content is generated and displayed in a user's browser. It encompasses a spectrum of techniques for determining when, where, and how HTML is produced—from the original model of server-generated HTML delivered to the browser, through the JavaScript-heavy single-page application era, to modern hybrid approaches that combine multiple rendering strategies based on the needs of each page. Understanding rendering strategies is essential for making performance, SEO, and user experience trade-offs in web application development.

The fundamental question of web rendering is: where does the work of converting application data into displayable HTML happen? The answer ranges from entirely on the server (traditional web applications), to partially on the server with client-side enhancement ([[Server Side Rendering]]), to entirely in the browser ([[Client Side Rendering]]), to ahead of time at build time ([[Static Site Generation]]). Each approach has distinct characteristics around Time to First Byte (TTFB), Time to Interactive (TTI), SEO suitability, infrastructure complexity, and the developer experience.

Modern web frameworks like [[Next.js]], [[Nuxt]], [[SvelteKit]], and [[Remix]] have abstracted these patterns into developer-friendly primitives, enabling mixed rendering strategies within a single application. A typical production application today might use SSG for marketing pages (fast, cached, SEO-friendly), SSR for pages requiring personalized content, and CSR for highly interactive dashboard sections. This mixing of strategies within one application is sometimes called "island architecture" or "partial hydration."

## Key Concepts

**Time to First Byte (TTFB)** — Measures the delay between requesting a URL and receiving the first byte of data. Server-rendered pages typically have slightly higher TTFB than cached static files but lower than JavaScript-dependent pages. TTFB is a foundational performance metric; high TTFB cascades into poor [[Web Vitals]] across the board.

**First Contentful Paint (FCP)** — The point when the browser renders the first piece of meaningful content. SSR and SSG achieve FCP quickly because the server sends complete HTML. CSR pages delay FCP until JavaScript downloads and executes, potentially showing a blank screen (the "blank page problem").

**Time to Interactive (TTI)** — When the page is fully responsive—DOM is rendered, event listeners attached, and the page can handle user interactions. CSR pages often have poor TTI because the entire JavaScript bundle must load before the page becomes interactive. SSR with hydration improves TTI over pure CSR.

**Largest Contentful Paint (LCP)** — Measures when the largest visible element (typically a hero image or headline) is rendered. This correlates strongly with perceived load speed. SSR and SSG perform better on LCP because content is in the initial HTML; CSR must wait for JavaScript to inject the LCP element.

**Cumulative Layout Shift (CLS)** — Measures visual stability—how much does the page layout shift as content loads? CSR pages often have poor CLS because content is injected after initial render, pushing other elements down. SSR/SSG pages can better control layout because content is present in the initial HTML.

**Hydration** — The process of taking server-rendered HTML and attaching JavaScript behavior to it on the client side. The server renders static HTML; the client loads JavaScript and "hydrates" that HTML, adding interactivity. This is a core concept in [[Server Side Rendering]] and is often where performance issues arise (full hydration vs. partial/selective hydration).

**Islands Architecture** — An architectural pattern popularized by Astro where interactive components ("islands") are hydrated individually, while the majority of the page remains static server-rendered HTML. This minimizes JavaScript sent to the browser and improves performance. Each "island" is a self-contained interactive component.

## Rendering Spectrum

Modern web applications can be understood as operating along a spectrum:

```text
Server-rendered + Cached                Client-rendered
        ↓                                          ↓
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Static Site    │  │  Server-Side    │  │  Client-Side    │
│  Generation     │  │  Rendering      │  │  Rendering      │
│  (SSG)          │  │  (SSR)          │  │  (CSR)          │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ Build time      │  │ Per-request     │  │ Browser         │
│ HTML generation │  │ HTML generation │  │ JavaScript      │
│ Maximum         │  │ Dynamic         │  │ Maximum         │
│ performance     │  │ personalization │  │ interactivity   │
└─────────────────┘  └─────────────────┘  └─────────────────┘

Modern hybrid approaches combine these:
┌──────────────────────────────────────────────────────────────┐
│          Incremental Static Regeneration (ISR)               │
│    Static pages rebuilt in background on content change       │
├──────────────────────────────────────────────────────────────┤
│             Streaming SSR with Suspense                      │
│    HTML sent progressively as components resolve              │
├──────────────────────────────────────────────────────────────┤
│               Islands Architecture                            │
│    Static HTML with selective client-side hydration          │
└──────────────────────────────────────────────────────────────┘
```

## How It Works

Each rendering strategy has distinct request/response flows:

**Static Site Generation (SSG):**
```text
[Build Time]
Developer → Framework → HTML files generated → CDN/deploy

[Request Time]
User → CDN (cache HIT) → Pre-built HTML served instantly
```

**Server-Side Rendering (SSR):**
```text
[Request Time]
User → Server → Execute component tree → Query data → Render HTML → Send response
```

**Client-Side Rendering (CSR):**
```text
[Request Time]
User → CDN → Minimal HTML shell + JS bundle → Browser downloads JS → Executes JS → API calls → Render content
```

**Incremental Static Regeneration (Next.js ISR):**
```text
[Request Time]
User → CDN → [cache HIT]? serve cached : [server renders] → cache for next request
```

## Practical Applications

- **Marketing and content sites** — SSG is ideal for blogs, documentation, and landing pages where content changes infrequently but SEO and performance are paramount.
- **E-commerce product pages** — ISR balances static-like performance for product details with ability to update prices and inventory in near-real-time.
- **SaaS dashboards** — CSR excels for highly interactive, personalized applications behind login where SEO is irrelevant and the app-like experience justifies the initial load cost.
- **News and media sites** — Often use a hybrid: SSR for homepage/breaking news (SEO + freshness) and SSG for article pages (performance + caching).
- **User-specific pages** — SSR is necessary for personalized content that depends on authentication state (cookies, sessions) since server code can read request headers directly.
- **Progressive web applications** — CSR frameworks combined with service workers can achieve near-native performance and offline capability, but require careful code splitting to minimize initial payload.

## Examples

**Next.js Rendering Strategies** — Next.js (the most popular React framework) exposes all major rendering strategies:

```javascript
// Static Site Generation (SSG) - built at compile time
export async function getStaticProps() {
  const posts = await fetchAllPosts();
  return { props: { posts }, revalidate: 60 }; // ISR: revalidate every 60s
}

// Server-Side Rendering (SSR) - run per request
export async function getServerSideProps(context) {
  const { req, params } = context;
  const session = await getSession(req); // Can read cookies/headers
  const userData = await fetchUserData(session.user.id);
  return { props: { userData } };
}

// Client-Side Rendering - useEffect fetches on client
import { useEffect, useState } from 'react';
function Dashboard() {
  const [data, setData] = useState(null);
  useEffect(() => { fetchDashboardData().then(setData); }, []);
  return <div>{data ? <Metrics data={data} /> : <Loading />}</div>;
}
```

**Astro Islands** — Astro uses the islands architecture by default:

```astro
---
// This runs at build time - generates static HTML
const posts = await fetchAllPosts();
---

<!-- This runs at build time, zero JS sent to client -->
<h1>Latest Posts</h1>

<!-- This is an island - interactive, hydrated on client -->
<Counter client:visible />

<!-- This also an island, loaded when visible -->
<Comments client:visible />
```

## Related Concepts

- [[Server Side Rendering]] — Generating HTML on the server per request
- [[Client Side Rendering]] — Generating HTML in the browser with JavaScript
- [[Static Site Generation]] — Pre-building HTML at build time
- [[Single Page Application]] — CSR-heavy architecture with client-side routing
- [[Web Vitals]] — Performance metrics: LCP, INP, CLS
- [[Hydration]] — Attaching client-side JavaScript to server-rendered HTML
- [[Next.js]] — Framework with built-in hybrid rendering support
- [[Remix]] — Framework focused on web standards and progressive enhancement

## Further Reading

- "Rendering on the Web" — Google Web Dev guide comparing rendering strategies.
- "Islands Architecture" by Jason Miller — The original article proposing the pattern.
- Next.js Documentation on Rendering — Official guide to SSG, SSR, ISR, and streaming.
- "The Partial Hydration Problem" — Understanding why hydration is expensive and solutions.

## Personal Notes

The web rendering landscape has matured to the point where "pick one" is the wrong approach. The modern meta-frameworks have made it easy to mix strategies per route, which is how it should be. The interesting questions are no longer "SSR or CSR?" but rather "which parts of this page need to be dynamic, and at what granularity?" The island architecture feels like the right mental model—most content is static and should ship as static HTML; only genuinely interactive pieces should ship JavaScript. React Server Components (RSC) in Next.js App Router push this further by letting server and client components coexist in the same tree, with the framework handling the boundary automatically. We're moving toward less JavaScript, not more, even as frameworks get more powerful.
