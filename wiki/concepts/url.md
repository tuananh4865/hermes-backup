---
title: "Url"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [web, http, networking, routing, API-design]
---

# Url

## Overview

A Uniform Resource Locator (URL) is a reference to a web resource that specifies its location and access mechanism. URLs are the fundamental addressing system of the web, enabling users and programs to locate and retrieve resources: HTML pages, images, API endpoints, files, and services. Every URL follows a standardized format defined in RFC 3986, consisting of scheme, authority (host and port), path, query string, and fragment identifier.

The terms URL and [[URI]] (Uniform Resource Identifier) are often used interchangeably, though technically URI is the broader concept. A URI can be a locator, a name, or both; a URL specifically indicates the access mechanism (how to retrieve the resource). In common usage, web addresses are URLs.

URLs are critical to [[REST-API]] design, [[Web Architecture]], routing in [[Single Page Application|single-page applications]], and [[SEO]] optimization. Modern web development involves URL manipulation for routing, [[API Gateway|API gateways]], [[CDN]] configuration, and deep linking.

## Key Concepts

### URL Anatomy

```
https://example.com:443/api/users?id=42&filter=active#results
\__/   \____________/ \_/ \_____/ \________/ \_______/
scheme     authority   port   path     query    fragment
```

**Scheme**: Protocol identifier (`http`, `https`, `ftp`, `mailto`). The scheme determines how the URL should be accessed.

**Authority**: Hostname and optional port. `example.com` or `localhost:3000`. The host is resolved via [[DNS]] to an IP address.

**Path**: Hierarchical resource location, starting with `/`. `/api/users`, `/products/123`. Paths are case-sensitive by convention (though servers vary).

**Query String**: Non-hierarchical parameters after `?`. `?id=42&filter=active`. Parameters are key-value pairs separated by `&`.

**Fragment Identifier**: Reference to a secondary resource, prefixed with `#`. `#results` typically points to an anchor within an HTML document or scroll position.

### URL Encoding (Percent-Encoding)

Special characters within URL components must be percent-encoded. Spaces become `%20`, ampersands within query values become `%26`, non-ASCII characters are UTF-8 encoded then percent-encoded.

```javascript
// URL encoding in JavaScript
encodeURIComponent("hello world&world")  // "hello%20world%26world"
encodeURI("https://example.com/path")    // "https://example.com/path" (doesn't encode ://)
```

### Absolute vs Relative URLs

**Absolute URLs** include full scheme and authority: `https://example.com/api/info`.

**Relative URLs** omit scheme and authority, resolved against a base URL:
- `//example.com/api` inherits scheme from base
- `/api/info` is absolute path from domain root
- `../images/logo.png` navigates up one directory

### Reserved and Unreserved Characters

**Unreserved** characters don't need encoding: `A-Z`, `a-z`, `0-9`, `-`, `.`, `_`, `~`.

**Reserved** characters have semantic meaning and may need encoding depending on context: `:/?#[]@!$&'()*+,;=`. The `@` in email addresses, for instance, must be encoded in some URL contexts.

## How It Works

When a browser navigates to a URL:

**1. Scheme Determination** — Browser checks if the scheme indicates HTTP/HTTPS and should use a network request, or if it's a built-in handler (mailto, tel).

**2. DNS Resolution** — For HTTP(S) URLs, the hostname is resolved to an IP address via DNS lookup. This involves recursive resolver queries through the DNS hierarchy.

**3. TCP Connection** — Browser establishes a TCP connection to the target IP (and port, defaulting to 80 for HTTP, 443 for HTTPS). [[tls]] adds the TLS handshake before HTTP traffic begins.

**4. HTTP Request** — Browser sends an HTTP request including the full URL path, query string, headers, and cookies.

**5. Response Handling** — Server processes the request and returns a response. The browser then renders or processes the response according to its media type.

## Practical Applications

### API Design

RESTful APIs use URL paths to represent resources and query strings for filtering:

```
GET /api/users              # List users
GET /api/users/123          # Get specific user
GET /api/users?role=admin   # Filter users by role
```

URL structure communicates resource hierarchy and API design philosophy.

### Routing in Web Frameworks

Modern [[Web Framework|web frameworks]] define route patterns with parameters:

```javascript
// Express.js routing
app.get('/users/:userId/posts/:postId', (req, res) => {
  const { userId, postId } = req.params;
  // /users/123/posts/456 → userId=123, postId=456
});

// React Router v6
<Route path="/users/:userId/posts/:postId" element={<Post />} />
```

### [[SEO]] Optimization

Search engines interpret URLs as content signals. Descriptive paths (`/products/wireless-headphones`) rank better than cryptic ones (`/p?id=3829`). [[URL Slugs]] should be lowercase, hyphen-separated, and meaningful.

## Examples

JavaScript URL manipulation:

```javascript
// Parse URL
const url = new URL('https://example.com/api/search?q=javascript&page=1');
console.log(url.hostname);        // "example.com"
console.log(url.pathname);        // "/api/search"
console.log(url.searchParams.get('q'));  // "javascript"

// Build URL
const base = new URL('https://api.example.com');
base.pathname = '/users';
base.searchParams.set('page', '2');
console.log(base.toString());     // "https://api.example.com/users?page=2"

// Relative URL resolution
const base = new URL('https://example.com/a/b/c/index.html');
new URL('../images/logo.png', base).toString();
// "https://example.com/a/b/images/logo.png"
```

## Related Concepts

- [[HTTP]] - The protocol accessed via most URLs
- [[DNS]] - System that resolves hostnames to IP addresses
- [[REST API]] - Architectural style using URLs for resource identification
- [[Web Architecture]] - Role of URLs in web systems
- [[URI]] - Uniform Resource Identifier (broader concept than URL)

## Further Reading

- RFC 3986 — The official URL specification
- MDN Web Docs: URL — Practical URL documentation with browser APIs

## Personal Notes

URLs are user-facing API contracts—once published, they should be stable. I've learned to treat URL design seriously: use descriptive paths, version APIs explicitly (`/v1/`, `/v2/`), and avoid changing structures that external systems depend on. Redirects preserve SEO when URLs must change. Also, always URL-encode user input when constructing URLs; otherwise, special characters break parsing. The `URL` object in modern JavaScript makes this manipulation reliable.
