---
title: Next.js
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [nextjs, react, framework, frontend, fullstack, ssr]
---

# Next.js

## Overview

Next.js is a React framework that enables developers to build full-stack web applications with server-side rendering (SSR), static site generation (SSG), and client-side rendering capabilities. Created by Vercel, Next.js has become one of the most popular frameworks for modern web development because it abstracts away the complexity of setting up a production-ready React application while providing powerful features for performance, SEO, and user experience.

At its core, Next.js extends React with routing, server-side rendering, and build optimization features that would otherwise require significant custom configuration. It allows developers to create pages as React components and handles the infrastructure concerns—code splitting, prefetching, image optimization, and environment configuration—automatically. This lets teams focus on building features rather than configuring build tools.

Next.js supports various rendering strategies within a single application. Pages can be statically generated at build time for fast performance, server-rendered on each request for dynamic content, or incrementally regenerated to balance freshness and performance. This flexibility, called "hybrid" rendering, allows developers to optimize each page based on its specific requirements.

## Key Concepts

**App Router**: Introduced in Next.js 13, the App Router is the newer approach to building Next.js applications. It uses React Server Components by default, allowing components to run on the server with the ability to stream content to the client. The App Router uses a file-system-based routing convention where folders define routes.

**Pages Router**: The original routing system in Next.js, still supported. Pages are defined as files in the `pages/` directory, and each file automatically becomes a route. The Pages Router is simpler but doesn't support React Server Components.

**Server-Side Rendering (SSR)**: Pages marked with `getServerSideProps` are rendered on the server for each request. This ensures content is always fresh and enables dynamic, personalized pages. SSR is essential for pages that need to show user-specific data or content that changes frequently.

**Static Site Generation (SSG)**: Pages are rendered at build time, producing static HTML files. These pages load instantly and are ideal for content that doesn't change often—blogs, documentation, marketing pages. Next.js supports SSG with `getStaticProps` and incremental static regeneration.

**API Routes**: Next.js allows creating API endpoints as serverless functions within the same project. These `/pages/api` or `/app/api` routes handle backend logic like form submissions, database operations, or third-party integrations without needing a separate backend service.

**Image Optimization**: The `<Image>` component automatically optimizes images—resizing, compressing, and converting to modern formats like WebP. Images are served from Vercel's global CDN with responsive sizes based on the viewing device.

## How It Works

Next.js applications start with a directory structure and configuration:

```javascript
// package.json - dependencies
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "scripts": {
    "dev": "next dev",      // Start development server
    "build": "next build",   // Build for production
    "start": "next start"    // Start production server
  }
}
```

```javascript
// next.config.js - configuration
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['example.com'],
    formats: ['image/avif', 'image/webp']
  },
  async rewrites() {
    return [
      { source: '/api/:path*', destination: 'https://api.example.com/:path*' }
    ]
  }
}

module.exports = nextConfig
```

## Practical Applications

**Marketing Websites**: Next.js's static generation and image optimization make it excellent for marketing sites that need fast load times and good SEO. The hybrid approach allows dynamic elements like pricing or user testimonials to be personalized.

**E-commerce Platforms**: Product pages benefit from SSG for performance while cart and checkout flows use SSR for real-time inventory and pricing. API routes handle payment processing without a separate backend.

**SaaS Dashboards**: Dashboards can use a mix of approaches—initial page loads via SSR for fast first paint, then client-side React for interactive features. Next.js's code splitting ensures dashboards load quickly despite their complexity.

**Blogs and Content Sites**: Next.js's built-in support for MDX (Markdown + JSX) makes it popular for blogs and documentation. Static generation ensures fast page loads worldwide from CDN.

**API Backends**: Small to medium backends can be built entirely within Next.js using API routes. This reduces infrastructure complexity—everything is in one codebase and deploys together.

## Examples

**App Router Page with Server Components**:

```javascript
// app/users/page.jsx - Server Component (default)
async function UsersPage() {
  // This runs on the server - direct database access
  const users = await db.query('SELECT * FROM users ORDER BY created_at DESC');
  
  return (
    <main>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            <Link href={`/users/${user.id}`}>{user.name}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}

export default UsersPage;
```

**Client Component with Interactivity**:

```javascript
// app/counter/client.jsx - Client Component
'use client';

import { useState } from 'react';

export function Counter({ initialCount = 0 }) {
  const [count, setCount] = useState(initialCount);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={() => setCount(c => c - 1)}>Decrement</button>
    </div>
  );
}
```

**API Route for Data Mutation**:

```javascript
// app/api/users/route.js
import { NextResponse } from 'next/server';
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email()
});

export async function POST(request) {
  try {
    const body = await request.json();
    const validated = userSchema.parse(body);
    
    const user = await db.users.create(validated);
    
    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Invalid request' },
      { status: 400 }
    );
  }
}
```

## Related Concepts

- [[react]] — The UI library that Next.js builds upon
- [[frontend]] — Frontend development in general
- [[server-side-rendering]] — SSR as a concept
- [[static-site-generation]] — SSG as a concept
- [[vercel]] — The platform that created and hosts Next.js deployments
- [[fullstack]] — Full-stack development capabilities
- [[react-server-components]] — Server Components in React/Next.js

## Further Reading

- [Next.js Documentation](https://nextjs.org/docs) — Official docs
- [Next.js 14 Release Notes](https://nextjs.org/blog/next-14) — Latest features
- [React Server Components](https://react.dev/blog/2023/03/22/react-labs-what-new-in-react-dev-2023#react-server-components) — RFC and explanation

## Personal Notes

Next.js's evolution from a simple SSR framework to a full-stack platform with React Server Components represents a significant shift in how we think about the frontend/backend boundary. The ability to have components that run on the server but render on the client (via hydration) blurs the traditional separation. That said, the framework has grown complex, and keeping up with its rapid changes can be challenging. The App Router is clearly the future direction, but the Pages Router isn't going away soon.
