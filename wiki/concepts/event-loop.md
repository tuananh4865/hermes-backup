---
title: "Event Loop"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [javascript, event-loop, asynchronous, concurrency, runtime, callbacks]
---

## Overview

The event loop is the core mechanism that enables JavaScript to handle asynchronous operations despite being single-threaded. JavaScript executes code on a single call stack, but the event loop allows it to respond to events, execute callbacks, and perform non-blocking operations by continuously monitoring the call stack, the task queue, and the microtask queue. This architecture enables responsive applications that can perform I/O operations, timers, and user interactions without freezing the UI.

Understanding the event loop is crucial for writing performant JavaScript, debugging async issues, and comprehending how frameworks like React, Node.js, and browser APIs actually work under the hood. Many mysterious bugs—race conditions, callback ordering issues, unexpected execution timing—stem from misunderstanding how the event loop processes tasks and microtasks.

The event loop's existence stems from JavaScript's origin as a scripting language for browsers. It was designed to be simple and to handle user interactions (clicks, keypresses) without blocking. This single-threaded model avoids complex synchronization issues that plague multi-threaded programming while still enabling responsive applications.

## Key Concepts

**Call Stack** is a LIFO (last-in-first-out) data structure that tracks function execution. When a function is called, its frame is pushed onto the stack. When it returns, the frame is popped. If the stack grows beyond its limit, you get a "stack overflow" error.

**Task Queue** (macrotask queue) holds callbacks waiting to be executed. Tasks include events (click handlers), I/O callbacks, setTimeout, setInterval, and UI rendering in browsers. After the current task completes, the event loop picks the next task from the queue.

**Microtask Queue** has higher priority than the task queue. Microtasks include Promise callbacks (.then, .catch, .finally), queueMicrotask(), and MutationObserver callbacks. After the current task and all synchronous code finish, the event loop processes ALL microtasks before picking the next task.

**Macrotasks vs Microtasks**: This distinction is critical. Promise.resolve().then() is a microtask; setTimeout() is a macrotask. Microtasks can starve the event loop if they continuously add more microtasks (as in `Promise.resolve().then(() => queueMicrotask(...))` loops).

## How It Works

The event loop follows a simple algorithm that repeats indefinitely:

1. Execute all synchronous code (call stack empties)
2. Process all microtasks in the queue (until empty)
3. Perform any necessary rendering (browsers)
4. Pick the next task from the task queue and execute it
5. Repeat

```javascript
console.log('1: synchronous');

setTimeout(() => console.log('4: setTimeout (macrotask)'), 0);

Promise.resolve()
  .then(() => console.log('3: Promise (microtask)'))
  .then(() => console.log('5: Promise chain (microtask)'));

console.log('2: synchronous');

// Output order: 1, 2, 3, 5, 4
// Because microtasks (3, 5) run before next macrotask (4)
```

In this example, despite setTimeout having 0ms delay, it runs after Promise callbacks because microtasks always execute before the next task is picked up.

Node.js has additional phase concepts in its event loop: timers, pending callbacks, idle/prepare, poll, check, and close callbacks. Timers (setTimeout, setInterval) execute in the "timers" phase, while setImmediate executes in the "check" phase.

## Practical Applications

Understanding the event loop helps optimize UI performance. Long-running tasks should be broken into smaller chunks using techniques like requestIdleCallback or setTimeout, allowing the browser to render between chunks. This prevents "jank"—frozen or stuttering interfaces.

Async/await syntax simplifies callback chains by making asynchronous code look synchronous, but it still interacts with the event loop. `await` pauses the async function and schedules the continuation as a microtask.

In Node.js, the event loop enables high-concurrency servers without threads. I/O operations schedule callbacks that execute when data is ready, allowing the server to handle thousands of simultaneous connections. Frameworks like Express.js build on this model.

## Examples

```javascript
// Breaking up long computation to prevent UI blocking
function processLargeDataset(items, onProgress) {
  let index = 0;
  
  function processChunk() {
    const chunkSize = 100;
    const chunk = items.slice(index, index + chunkSize);
    
    // Process chunk...
    chunk.forEach(processItem);
    
    index += chunkSize;
    onProgress(index / items.length);
    
    if (index < items.length) {
      // Yield to event loop for rendering/other tasks
      setTimeout(processChunk, 0);
    }
  }
  
  processChunk();
}

// Correct ordering with async/await
async function fetchAndProcess(userId) {
  try {
    // These run concurrently - faster than sequential
    const [user, posts] = await Promise.all([
      fetchUser(userId),
      fetchPosts(userId)
    ]);
    
    return { user, posts };
  } catch (error) {
    console.error('Failed to load data:', error);
  }
}
```

## Related Concepts

- [[JavaScript]] - The language that uses the event loop
- [[async-await]] - Syntactic sugar over Promises
- [[Promises]] - The microtask-producing mechanism
- [[Callbacks]] - The original async pattern in JavaScript
- [[Node.js]] - Server-side runtime with its own event loop phases

## Further Reading

- "You Don't Know JS: Async & Performance" by Kyle Simpson
- Philip Roberts' talk "What the heck is the event loop?"
- Jake Archibald's blog posts on the event loop and microtasks

## Personal Notes

I spent years confused about async behavior until I truly internalized the microtask vs macrotask distinction. Now I can predict execution order reliably and debug subtle timing bugs. I recommend visualizing the event loop and practicing with simple examples before tackling complex async code. Understanding this core mechanism makes everything else—React state updates, Node.js I/O, browser rendering—much more understandable.
