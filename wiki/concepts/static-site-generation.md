---
title: "Static Site Generation"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [web-development, static-sites, ssg, jamstack, build-tools]
---

# Static Site Generation

## Overview

Static Site Generation (SSG) is a website architecture in which HTML pages are pre-rendered at build time rather than on-demand at request time. With SSG, every page is computed once — when the developer builds the project — and the resulting HTML, CSS, JavaScript, and asset files are served directly from a content delivery network (CDN). There is no server-side runtime processing each visitor's request; the server simply delivers flat files.

This approach stands in contrast to dynamic server-side rendering (SSR), where a backend framework assembles each page on the fly, and to client-side rendering (CSR), where the browser receives a minimal HTML shell and constructs the page entirely in JavaScript. SSG delivers the best of both worlds in many scenarios: the rich interactivity of a dynamic site with the performance and simplicity of serving static files.

SSG is the backbone of the [[Jamstack]] architecture, which pairs pre-generated static assets with JavaScript and APIs to create fast, scalable, and secure websites.

## Key Concepts

**Build-Time Rendering**: All pages — including blog posts, documentation, product listings — are rendered to static HTML during the `npm run build` step. This means data fetching (from a CMS, database, or Markdown files) happens once, at build time, not per-request.

**Incremental Static Regeneration (ISR)**: A hybrid approach popularized by [[Next.js]], where pages are statically generated but can be revalidated in the background. A page might be statically served for an hour before a fresh build is triggered. This bridges the gap between full SSG purity and the need for always-fresh content.

**Content Mesh**: Modern SSG tools can pull content from multiple headless CMS platforms, Markdown files, databases, and APIs simultaneously, compositing them into a unified site at build time. This decoupled architecture separates content management from presentation.

**Preview Modes**: Many SSG frameworks support "draft" or "preview" modes where a CMS can trigger an on-demand rebuild of specific pages, allowing content editors to see changes live before publishing.

## How It Works

A typical SSG workflow begins with a source repository containing templates (in React, Vue, Svelte, or plain HTML/CSS), content (Markdown, MDX, JSON, or remote API data), and configuration. When a developer runs the build command, the static site generator:

1. Reads all content sources
2. Applies templates to each piece of content, creating a page route per item
3. Runs any necessary transformations (syntax highlighting, image optimization, link rewriting)
4. Writes the final HTML, CSS, JS, and assets to a `dist/` or `out/` directory

That output directory can be deployed directly to any CDN or static hosting provider — Netlify, Vercel, Cloudflare Pages, GitHub Pages, or an S3 bucket.

```javascript
// Example: A simple SSG page in 11ty ( Eleventy )
// .eleventy.js
module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy("static");
  return {
    dir: { input: "src", output: "_site" }
  };
};
```

```html
<!-- src/index.njk -->
---
layout: base.njk
title: Welcome
---
<h1>{{ title }}</h1>
<p>This page was built at compile time.</p>
```

## Practical Applications

Documentation sites are the canonical use case for SSG. Tools like [[Docusaurus]], [[Gatsby]], and [[Hugo]] power the docs for React, Vue, Terraform, and thousands of open-source projects. The build-once-serve-forever model is perfect for reference documentation that changes infrequently.

Marketing sites and blogs benefit enormously from SSG: pre-rendered pages score perfectly on Core Web Vitals metrics, load instantly from CDN edge nodes, and are immune to many server-side security vulnerabilities since there is no runtime to exploit.

E-commerce product pages can use SSG for performance, with ISR refreshing prices and stock levels in the background. The critical path — hero images, product descriptions, layout — is static and instant.

## Examples

The world's most popular SSG frameworks include:

| Framework | Language | Notable For |
|---|---|---|
| [[Next.js]] | JavaScript/TypeScript | ISR, React integration |
| [[Gatsby]] | JavaScript/TypeScript | GraphQL data layer, plugins |
| [[Hugo]] | Go | Blazing fast builds, single binary |
| [[Eleventy]] (11ty) | JavaScript/TypeScript | Minimal, framework-agnostic |
| [[Astro]] | JavaScript | Islands architecture, zero JS by default |
| [[Docusaurus]] | JavaScript/TypeScript | Documentation, built by Meta/Meta |

A blog post in Markdown processed by any of these becomes a full HTML page with navigation, styling, and optimized assets — all before a single user visits the site.

## Related Concepts

- [[Jamstack]] — The architectural philosophy SSG embodies
- [[Next.js]] — Framework popularizing SSG and ISR in the React ecosystem
- [[Astro]] — Modern SSG framework known for "islands" architecture
- [[Content Delivery Network]] — Where static files are deployed and served from
- [[Web Performance]] — SSG's primary benefit is delivering fast, optimized pages

## Further Reading

- [Jamstack.org](https://jamstack.org/) — Resources, case studies, and community
- [MDN: Building a Static Site](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Designing_and_marking_up_a_web_page)
- *Modern Static Site Generation with Next.js, Astro, and more* — Pragmatic comparison of current tools

## Personal Notes

The first time I saw a Lighthouse score of 100/100 on a real site, it was an Eleventy blog. The page had no JavaScript, no database query, no server processing — just a pre-rendered HTML file served from a CDN edge node. That convinced me that SSG isn't a limitation, it's a design philosophy. The constraint of "everything must be known at build time" forces you to think clearly about your data model. When you need dynamic content (user-specific data, real-time prices), you reach for client-side fetching or ISR rather than defaulting to server-side rendering for everything.
