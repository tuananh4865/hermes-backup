---
title: Futures
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [futures, async, concurrency, programming]
---

## Overview

A Future represents a value that will be available at some point in the future, rather than immediately. It serves as a placeholder for a result of an asynchronous operation, allowing a program to continue executing while waiting for the operation to complete. Futures are fundamental to asynchronous programming models in languages like Python, JavaScript, Rust, Scala, and many others. Instead of blocking the execution thread while waiting for a slow operation such as a network request, database query, or file read, a Future allows the program to register a callback or chain operations that will be executed once the value becomes available.

The core idea behind Futures is the separation of the initiation of an asynchronous task from the consumption of its result. When you initiate an asynchronous operation, you receive a Future object immediately. This object can be passed around, stored in data structures, and composed with other Futures. The actual computation happens in the background, often on a separate thread or by the event loop, and when it completes, the Future holds the resulting value for any code that needs it.

Futures are closely related to the concept of [[Promises]], which serve a similar role in some languages and libraries. In many implementations, the terms are used interchangeably, though in some contexts a Promise refers to the writable side of a data channel while a Future represents the readable side. Together, these abstractions form the backbone of modern asynchronous programming, enabling efficient concurrency without the complexity of manual thread management.

## States

A Future can exist in one of three distinct states that describe where it is in its lifecycle.

**Pending** is the initial state of a Future. The asynchronous operation has been started but has not yet completed. While in the pending state, the Future does not hold a value and any attempt to read the value will typically block or throw an exception, depending on the language and library. The program continues executing other tasks during this time, making efficient use of resources.

**Fulfilled** (also called resolved or completed) is the state reached when the asynchronous operation finished successfully. The Future now holds the expected value, and any registered callbacks or continuation tasks are executed. Code waiting on the Future can now retrieve the value without blocking, as it is immediately available.

**Failed** (also called rejected) is the state reached when the asynchronous operation encountered an error or exception. Instead of a value, the Future holds the error information. Proper error handling in asynchronous code involves checking for this state and handling failures gracefully, often through dedicated error callbacks or try-catch mechanisms in the continuation chain.

Some Future implementations also support a **Cancelled** state, indicating that the asynchronous operation was explicitly cancelled before completion. This allows programs to abandon long-running tasks when they are no longer needed, freeing resources and preventing unnecessary computation.

## Related

- [[Promises]] - A closely related abstraction, often paired with Futures for async programming
- [[async-await]] - Syntactic sugar built on top of Futures for cleaner asynchronous code
- [[Concurrency]] - The broader concept of managing multiple simultaneous operations
- [[Event Loop]] - The mechanism that drives asynchronous execution in many languages
- [[Callbacks]] - An older pattern that Futures largely supersede for async programming
- [[Thread Pool]] - Collections of worker threads commonly used to execute asynchronous tasks
