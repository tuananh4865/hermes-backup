---
title: "WebKit"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [browser, rendering-engine, webkit, safari, apple, open-source]
---

# WebKit

## Overview

WebKit is an open-source browser rendering engine originally developed by Apple as a fork of KHTML (which itself came from KDE's Konqueror browser). WebKit powers Safari on macOS, iOS, iPadOS, and in older versions of Chrome on Windows (before Chrome switched to Blink). It is one of the two dominant rendering engines in use today, alongside Blink (used by Chrome, Edge, Opera, and Samsung Internet). WebKit's architecture separates parsing (building a DOM tree from HTML), layout (computing element positions), painting (drawing elements to the screen), and JavaScript execution into distinct components. This clean separation has made WebKit a popular subject for browser engine research and a foundational technology for the web rendering ecosystem. WebKit also underpins many hybrid mobile app frameworks through UIWebView and WKWebView on iOS.

## Key Concepts

**WebCore** is the core rendering library of WebKit. It handles HTML parsing, DOM tree construction, CSS parsing and style calculation, layout (the box model and reflow), and SVG rendering. WebCore is the part of WebKit that understands the structure and style of a web page — it's platform-agnostic and shared across all WebKit ports.

**JavaScriptCore (JSC)** is WebKit's native JavaScript engine. While Chrome uses V8, WebKit historically used JavaScriptCore, which has its own JIT (Just-In-Time) compiler, interpreter, and garbage collector. JSC has evolved significantly and includes multiple tiers of execution optimization for faster startup and peak performance.

**WKWebView** is the modern web view component for iOS and macOS apps. Replaced the deprecated UIWebView, WKWebView runs in a separate process from the app, supports Nitro JavaScript engine (the same JIT used in Safari), and provides proper memory management. It is the only supported way to embed web content in iOS apps.

**Blink** is Google's fork of WebKit, created in 2013 when Google split from WebKit to pursue independent development. Blink and WebKit share ancestry but have diverged significantly. Most features developed after 2013 (like CSS Grid, WebAssembly, and numerous performance optimizations) are implemented independently in each engine.

## How It Works

The WebKit rendering pipeline for a typical web page:

1. **Navigation** — WebKit receives a URL and initiates a network request
2. **HTML Parsing** — The HTML tokenizer breaks the response into tokens and constructs the DOM tree
3. **CSS Parsing** — External stylesheets, inline `<style>` tags, and inline styles are parsed into CSSOM (CSS Object Model)
4. **Render Tree Construction** — DOM and CSSOM are combined into a render tree — a tree of visible elements with computed styles
5. **Layout** — WebKit calculates the position and size of each render tree node (this is called reflow in some other engines)
6. **Painting** — Render objects are painted to layers using the graphics framework (Core Graphics on Apple platforms)
7. **Compositing** — Multiple layers are composited together for final display, enabling smooth scrolling and animations

## Practical Applications

- **Safari browser** — WebKit is the rendering engine for all Apple browsers
- **iOS Web Views** — Hybrid mobile apps using WKWebView embed WebKit to display web content
- **Mail.app and other Apple apps** — Apple uses WebKit in macOS/iOS system apps that render HTML
- **Nintendo Switch and other embedded browsers** — Several game consoles use WebKit for their web-based UIs
- **In-App Browsers** — Apps like Slack, Discord, and social media apps often embed WebKit for link previews

## Examples

Checking WebKit browser version via JavaScript:

```javascript
// Detect WebKit-based browser (Safari, older Chrome)
const isWebKit = /WebKit/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent);

// Get WebKit version
const webKitMatch = navigator.userAgent.match(/AppleWebKit\/(\d+)/);
const webKitVersion = webKitMatch ? webKitMatch[1] : null;

// WKWebView detection on iOS
const isWKWebView = /WebKit\//.test(navigator.userAgent) && !/Chrome\//.test(navigator.userAgent) && (window.webkit && window.webkit.messageHandlers);
```

CSS vendor prefix for WebKit browsers:

```css
/* WebKit-specific prefixes are still needed for some experimental features */
.my-element {
  -webkit-backdrop-filter: blur(10px);
  -webkit-mask-image: linear-gradient(black, transparent);
  -webkit-transform: rotate(45deg);
}
```

## Related Concepts

- [[Blink]] — Google's fork of WebKit, used by Chrome and most Chromium-based browsers
- [[Gecko]] — Mozilla's rendering engine, used by Firefox — the other major engine alongside WebKit
- [[Rendering Engine]] — General concept of how browsers turn HTML/CSS/JS into pixels
- [[Safari]] — Apple's browser that uses WebKit as its rendering engine
- [[W3C]] — Standards body that defines the HTML, CSS, and DOM specs WebKit implements

## Further Reading

- [WebKit Project Page](https://webkit.org/) — Official project site and blog
- [WebKit Architecture](https://webkit.org/architecture/) — Deep dive into WebKit's internal architecture
- [How Browsers Work](https://web.dev/articles/howbrowserswork) — Tali Garsiel's comprehensive explainer (covers WebKit)

## Personal Notes

WebKit has a special place in my understanding of browser history. Apple's decision to fork KHTML and create WebKit was controversial in the open source community at the time, but it produced a very clean, well-documented codebase. One practical implication of WebKit's dominance on iOS is that all iOS browsers are actually WebKit under the hood — Chrome and Firefox on iOS can't use their own engines due to Apple's App Store policies. This makes WebKit the de facto engine for mobile web development. The WebKit team's commitment to performance (especially JavaScript performance with JSC) is often underappreciated compared to V8.
