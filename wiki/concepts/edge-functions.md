---
title: "Edge Functions"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [serverless, edge-computing, cloudflare-workers, vercel, aws-lambda, performance]
---

# Edge Functions

## Overview

Edge functions are serverless functions that execute at the edge of the network—physically distributed servers close to end users rather than in centralized data centers. This positioning dramatically reduces latency by minimizing the physical distance data must travel. When a user in Tokyo makes a request to an application with edge functions, the code executes in a Tokyo edge location rather than bouncing to a US-based server and back.

Edge functions represent an evolution in the serverless model, extending compute from regional data centers to a global network of edge nodes. They inherit the benefits of serverless—automatic scaling, no server management, pay-per-invocation pricing—while adding the latency advantages of distributed computing. This makes them particularly suitable for latency-sensitive applications like personalization, authentication, and content transformation.

Major cloud providers and CDNs have adopted edge function platforms: Cloudflare Workers, Vercel Edge Functions, AWS Lambda@Edge, Fastly Compute@Edge, and Deno Deploy. Each offers similar core functionality but differs in runtime (V8 isolates vs. OS containers), supported languages, and integration with other services.

## Key Concepts

**Edge Locations**: A globally distributed network of servers. Where traditional CDNs cache static content at the edge, edge functions execute dynamic code there. Providers like Cloudflare operate 200+ data centers globally, ensuring most users are within ~50ms of an edge node.

**V8 Isolates**: Cloudflare Workers and similar platforms use V8 JavaScript isolates rather than containers or VMs. Isolates start in microseconds (vs. hundreds of milliseconds for cold-starting containers), enable denser packing of functions per machine, and provide strong isolation without the overhead of full process isolation.

**Cold Start**: The delay when a function instance must be created for a new request. Traditional serverless (AWS Lambda) can have cold starts of 100ms-1s. Edge functions with V8 isolates achieve cold starts under 5ms, making them viable for latency-sensitive paths.

**Request/Response Manipulation**: Edge functions intercept requests before they reach origin servers, enabling modification of headers, cookies, URLs, and bodies. They can short-circuit requests with cached responses, redirect users, add authentication headers, or rewrite URLs.

**Regional Affinity**: Unlike traditional serverless that abstracts location, edge functions can be deployed to specific geographic regions. This enables compliance with data residency requirements while maintaining low latency.

## How It Works

When a request reaches an edge function:

1. **DNS Routing**: The request is routed to the nearest edge location
2. **Edge Node Reception**: The edge node receives the incoming request
3. **Function Execution**: The edge function code executes in a V8 isolate
4. **Potential Origin Fetch**: If needed, the function fetches data from origin
5. **Response Modification**: The response is modified (if needed) and returned
6. **Response to Client**: The modified response travels back to the user

```
Traditional Request:
User (Tokyo) → CDN Cache (miss) → Origin Server (US) → Response
                           ↓ 500ms+ round trip

Edge Function Request:
User (Tokyo) → Edge Node (Tokyo) → [Execute edge function] → Response
                           ↓ <10ms to edge node
```

The origin fetch is often the bottleneck. Effective edge function design minimizes or eliminates origin calls, either by returning cached data, using edge storage (KV, Durable Objects), or performing computation that doesn't require origin data.

## Practical Applications

**Personalization**: Returning customized content without origin round-trips. The edge function reads user preferences from a cookie or JWT, modifies HTML or API responses accordingly, and delivers a personalized experience in <50ms total.

**Authentication/Authorization**: Validating JWT tokens or session cookies at the edge. Invalid requests are rejected immediately without reaching origin, reducing load and improving security.

**A/B Testing**: Distributing traffic between variants at the edge based on cookies or headers. Enables experimentation without origin infrastructure.

**Bot Detection**: Inspecting request patterns, user agents, and behavior signals at the edge. Suspicious traffic can be challenged or blocked before reaching origin.

**Content Transformation**: Modifying responses—converting images, minifying HTML/CSS/JS, adding security headers—without origin involvement.

## Examples

Cloudflare Worker handling authentication and request modification:

```javascript
export default {
  async fetch(request, env) {
    // Parse the request URL
    const url = new URL(request.url);
    
    // Check for authentication token
    const token = request.headers.get('Authorization')?.split(' ')[1];
    
    if (!token && !url.pathname.startsWith('/public/')) {
      // Return login page for unauthenticated users
      return new Response('Please log in', {
        status: 302,
        headers: { 'Location': '/login' }
      });
    }
    
    // Validate token (simplified)
    if (token && !await validateToken(token, env)) {
      return new Response('Unauthorized', { status: 401 });
    }
    
    // Add user context to headers before forwarding to origin
    const modifiedRequest = new Request(request, {
      headers: {
        ...Object.fromEntries(request.headers),
        'X-User-ID': token ? getUserId(token) : 'anonymous',
        'X-Request-Start': Date.now().toString()
      }
    });
    
    // Forward to origin
    return fetch(modifiedRequest);
  }
};
```

Vercel Edge Function with geolocation:

```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const country = request.geo?.country || 'US';
  const city = request.geo?.city || 'Unknown';
  
  // Redirect users from certain countries
  if (country === 'RU') {
    return NextResponse.redirect(new URL('/unavailable', request.url));
  }
  
  // Add localization headers
  const response = NextResponse.next();
  response.headers.set('X-User-Country', country);
  response.headers.set('X-User-City', city);
  
  return response;
}
```

## Related Concepts

- [[Serverless]] - Cloud execution models without server management
- [[CDN]] - Content delivery networks and edge caching
- [[Cloudflare Workers]] - V8 isolate-based edge runtime
- [[AWS Lambda]] - Traditional serverless functions
- [[Web Architecture]] - Edge functions in the broader web stack
- [[JWT]] - Tokens often validated at the edge
- [[Vercel]] - Platform with edge function support

## Further Reading

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Vercel Edge Functions](https://vercel.com/docs/edge-functions)
- [AWS Lambda@Edge](https://docs.aws.amazon.com/lambda/latest/dg/lambda-edge.html)
- [The Edge Computing Revolution](https://blog.cloudflare.com/tag/edge/)

## Personal Notes

Edge functions have matured significantly since their introduction. My first production use was implementing geo-based redirects for a media company—they wanted to serve region-locked content with appropriate messaging rather than a generic error. The latency improvement was dramatic: what had been a 300ms round-trip became a 20ms response. The gotcha that burned us: edge functions have limited execution time (typically 50ms CPU on Cloudflare Workers, vs. 15 minutes for Lambda). You can't do heavy computation or long-running tasks at the edge. Also, some operations that seem simple (like cryptographic operations) can quickly consume your CPU budget if you're not careful. For anything data-intensive, look into edge storage solutions like Cloudflare KV or Durable Objects which provide persistent state at the edge.
