---
title: "Async I/O"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: [async, io, performance]
confidence: medium
sources: []
---

# Async I/O

## Overview

Asynchronous I/O is a programming paradigm where a program can initiate an I/O operation (network request, disk read, database query) without blocking the execution thread. The program continues running and receives notification when the I/O operation completes.

## Why It Matters

In web applications, most latency comes from I/O wait times. Async I/O allows a single thread to handle many concurrent connections by yielding CPU time during I/O waits.

## Related Concepts

- [[async-await]] — Syntactic sugar for async operations
- [[event-loop]] — Mechanism that processes async callbacks
- [[promises]] — Promise-based async pattern
- [[nodejs]] — Runtime built around async I/O
- [[hotspots]] — Where async I/O helps performance
