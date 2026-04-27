---
title: "Async/Await"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: [javascript, async, programming]
confidence: medium
sources: []
---

# Async/Await

## Overview

`async/await` is syntactic sugar over JavaScript Promises that makes asynchronous code read like synchronous code. Introduced in ES2017, it allows you to write promise-based code without explicit `.then()` chaining.

## Basic Usage

```javascript
async function fetchData() {
  const response = await fetch('/api/data');
  const data = await response.json();
  return data;
}
```

## Related Concepts

- [[promises]] — The underlying mechanism async/await builds on
- [[event-loop]] — How JavaScript handles async operations
- [[callbacks]] — Older async pattern that promises replaced
- [[async-io]] — Asynchronous I/O operations
