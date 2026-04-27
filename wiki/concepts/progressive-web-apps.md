---
title: "Progressive Web Apps"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [pwa, web-development, mobile, offline-first, service-workers]
---

# Progressive Web Apps

## Overview

Progressive Web Apps (PWAs) are web applications that use modern web capabilities to deliver an app-like experience to users. PWAs combine the best of traditional web pages—universal reach, linkability, and searchability—with the powerful capabilities of native mobile applications—such as offline functionality, push notifications, home screen installation, and background synchronization. The term was coined by Google engineer Alex Russell in 2015, and the approach has since been adopted by major companies including Twitter, Spotify, Starbucks, and Pinterest.

The defining characteristic of a PWA is its progressive enhancement: the application works for every user regardless of browser choice, but provides enhanced functionality for users on capable browsers. A PWA starts as a regular website with valid HTML, CSS, and JavaScript, and layers on features like [[Service Workers]] and Web App Manifests only when the browser supports them. This means the core content and functionality remain accessible even in environments that don't support PWA features.

## Key Concepts

**Responsive Design** is a prerequisite for PWAs. The application must adapt seamlessly to any screen size—from mobile phones to desktop monitors—using flexible grids, relative units, and media queries. This isn't unique to PWAs, but it's foundational: a PWA that doesn't work well on mobile defeats its purpose.

**Service Workers** are the technical backbone of PWAs. A service worker is a JavaScript file that runs in the background, separately from the main browser thread. It can intercept network requests, cache responses, serve cached content when offline, and handle push notifications. Service workers follow a lifecycle of registration, installation, and activation, and they communicate with the main page via the [[Post Message API]].

**Web App Manifest** is a JSON file that defines how the PWA appears when installed on a user's device. It specifies the app name, icons, theme colors, display mode (standalone, fullscreen, minimal-ui), start URL, and splash screen. The manifest enables the "Add to Home Screen" prompt in mobile browsers.

**HTTPS** is mandatory for PWAs. Service workers can intercept network traffic, which makes them powerful but also a significant security risk if misused. Therefore, browsers only allow service worker registration on secure origins (HTTPS or localhost during development).

## How It Works

A PWA begins as a standard web application with responsive HTML, CSS, and JavaScript. To transform it into a PWA, developers add two key components:

1. **Service Worker Registration**: In the main JavaScript, the application registers a service worker file:

```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(registration => {
      console.log('Service Worker registered:', registration.scope);
    })
    .catch(error => {
      console.log('Service Worker registration failed:', error);
    });
}
```

2. **Service Worker Implementation**: The `sw.js` file defines caching strategies—commonly cache-first for static assets and network-first for dynamic content:

```javascript
const CACHE_NAME = 'my-pwa-cache-v1';
const urlsToCache = ['/', '/styles/main.css', '/script/main.js'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

3. **Web App Manifest**: A `manifest.json` file linked from all HTML pages:

```json
{
  "name": "My Progressive Web App",
  "short_name": "MyPWA",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3178c6",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

## Practical Applications

**Offline-First Applications** are the most compelling use case for PWAs. Applications like Google Maps, Google Docs, and Spotify's web player use service workers to cache critical resources, allowing users to continue interacting with core features even without an internet connection. For enterprise applications used in areas with unreliable connectivity—field service apps, inventory systems, transportation logistics—PWAs can maintain productivity where native apps might fail.

**Push Notifications** enable PWAs to re-engage users even when the browser is closed. Combined with background synchronization, this allows applications to pull fresh data and notify users of important updates, much like native mobile apps do. News sites, social media platforms, and e-commerce applications use this to drive engagement.

**Home Screen Installation** gives PWAs a presence on the user's device alongside native apps. The app icon appears on the home screen or app list, and the app launches in its own window without browser chrome, creating a native-like experience.

**Cross-Platform Consistency** is a major advantage. A single codebase serves iOS, Android, and desktop browsers. This dramatically reduces development and maintenance costs compared to maintaining separate native applications for each platform.

## Examples

**Twitter Lite** is often cited as a canonical PWA success story. Twitter rebuilt their mobile web experience as a PWA, achieving a 30% increase in pages viewed per session, a 75% increase in tweets sent, and a 65% decrease in bounce rate. The application works offline, loads in under 3 seconds on 3G networks, and consumes significantly less data than the previous iteration.

**Starbucks' PWA** for their ordering system allows customers to browse the menu, customize orders, and add items to their cart even when offline. When connectivity returns, the app synchronizes the pending orders automatically.

**Pinterest** rebuilt their mobile web experience as a PWA and saw a 40% increase in time spent on the site and a 50% increase in core engagements.

## Related Concepts

- [[Service Workers]] — The technology enabling offline functionality and push notifications
- [[Single Page Application]] — The architecture most PWAs are built upon
- [[Web App Manifest]] — The metadata file enabling home screen installation
- [[Offline-First Architecture]] — Design philosophy prioritizing offline functionality
- [[HTTPS]] — Required security foundation for PWAs
- [[Cache API]] — Browser API used for storing cached responses

## Further Reading

- [Web.dev: Progressive Web Apps](https://web.dev/progressive-web-apps/) — Google's comprehensive PWA documentation
- [MDN: Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps) — Mozilla's reference guide
- [PWABuilder](https://www.pwabuilder.com/) — Microsoft's tool for packaging PWAs for app stores

## Personal Notes

The first time I used a PWA offline and it just worked, I was impressed by how invisible the technology was. The user shouldn't need to know or care whether they're online or offline—the app should handle both gracefully. This "resilient to connectivity loss" property is what makes PWAs fundamentally different from traditional web apps, not just the ability to install to the home screen. The key insight is that PWA features layer on progressively: the app is still useful without them, but increasingly native-like with them.
