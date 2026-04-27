---
title: Reactive Programming
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [reactive-programming, programming-paradigm, rxjs, observables, asynchronous]
---

# Reactive Programming

## Overview

Reactive programming is a programming paradigm oriented around data streams and the propagation of change. Rather than executing code imperatively—fetch data, process, wait for result, continue—reactive programming defines pipelines that automatically propagate updates through a series of transformations. When a data source changes, all dependent computations and UI elements update automatically, without explicit polling or callback management.

The concept rests on the Observer pattern, where subscribers register interest in a data source and receive notifications when that source emits new values. However, reactive programming extends this pattern with powerful operators for transforming, combining, filtering, and error handling. Streams can be merged, split, buffered, sampled, and composed in ways that would be cumbersome with traditional callbacks.

This paradigm has gained significant traction with the rise of modern web applications, where handling asynchronous events—user inputs, API responses, WebSocket messages, sensor data—is central to creating responsive experiences. Languages and frameworks like JavaScript (RxJS), Java (Project Reactor), Swift (Combine), and .NET (System.Reactive) provide reactive libraries that make event-driven programming more manageable and expressive.

## Key Concepts

**Observables** are data sources that emit values over time. They represent the "reactive" side of the paradigm—the things being observed. An observable might emit user keystrokes, stock price updates, sensor readings, or any sequence of values arriving asynchronously. Observables are lazy; they don't produce values until something subscribes to them.

**Subscribers** (or Observers) register to receive values from an observable. When a subscriber is no longer interested, it unsubscribes to prevent memory leaks and unnecessary computation. The subscription relationship defines the lifecycle of data flow.

**Operators** are functions that transform, combine, or filter data streams. They include map (transform each value), filter (keep values meeting a condition), reduce (accumulate values), merge (combine multiple streams), debounce (rate-limit based on time), and many others. Composing operators creates expressive data processing pipelines.

```javascript
// RxJS example: Search input with debouncing
import { fromEvent } from 'rxjs';
import { debounceTime, distinctUntilChanged, map, switchMap } from 'rxjs/operators';

const searchInput = document.querySelector('#search');
const results = document.querySelector('#results');

// Create observable from input events
const search$ = fromEvent(searchInput, 'input').pipe(
  map(event => event.target.value),           // Extract search term
  debounceTime(300),                          // Wait for typing pause
  distinctUntilChanged(),                     // Ignore duplicate terms
  switchMap(query => searchAPI(query))        // Cancel previous, switch to new
);

search$.subscribe(results => renderResults(results));
```

**Backpressure** handles scenarios where data arrives faster than it can be processed. Reactive streams provide mechanisms to buffer, drop, or throttle data, preventing system overload. Operators like throttleTime, sampleTime, or bufferCount give developers control over consumption rates.

**Cold vs Hot Observables** distinguish between sources that emit from the beginning for each subscriber (cold) and sources that share emissions with all subscribers from a single source (hot). A cold observable is like a video-on-demand; each viewer gets the full content from start. A hot observable is like a live broadcast; subscribers join mid-stream and miss earlier content.

## How It Works

Reactive libraries implement the Observable pattern with push-based notification. When an observable emits a value, it pushes that value to all registered subscribers synchronously or asynchronously depending on the source. Operators are themselves functions that return new observables, allowing chaining.

```typescript
// Composing reactive streams in TypeScript
import { interval, Subject, BehaviorSubject } from 'rxjs';
import { take, map, scan, filter, shareReplay } from 'rxjs/operators';

// State management with BehaviorSubject
interface AppState {
  count: number;
  history: number[];
}

const state$ = new BehaviorSubject<AppState>({ count: 0, history: [] });

// Derived observables
const count$ = state$.pipe(
  map(s => s.count),
  distinctUntilChanged()
);

const doubledCount$ = count$.pipe(
  map(n => n * 2)
);

// Update state - automatically propagates to all subscribers
function increment() {
  const current = state$.value;
  state$.next({
    count: current.count + 1,
    history: [...current.history, current.count + 1]
  });
}
```

The execution model relies on Schedulers to control when subscriptions receive values. Schedulers can coordinate timing for intervals, animation frames, or immediate execution, providing deterministic behavior for testing and predictable performance in production.

## Practical Applications

**Real-time Dashboards** benefit from reactive programming when displaying live data. Rather than repeatedly querying APIs or managing timer-based refreshes, components subscribe to data streams and update automatically when new information arrives.

**Form Validation** uses reactive streams to validate user input as they type, applying debouncing to avoid excessive validation calls while providing immediate feedback. Complex interdependent validations (field A required only if field B has a value) are expressed clearly through operator composition.

**Event-driven Architectures** in microservices use reactive patterns to handle asynchronous messaging. Reactive frameworks like Spring WebFlux enable non-blocking request handling that scales efficiently with IO-bound workloads.

## Examples

Handling errors in reactive streams with graceful recovery:

```javascript
import { fromFetch } from 'rxjs/fetch';
import { catchError, retry, switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

const data$ = fromFetch('https://api.example.com/data').pipe(
  switchMap(response => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  }),
  retry({ count: 3, delay: 1000 }),  // Retry failed requests
  catchError(error => {
    console.error('Fetch failed:', error);
    return of({ error: true, message: error.message });
  })
);
```

## Related Concepts

- [[mobx]] — State management library using reactive principles
- [[observable-pattern]] — The underlying design pattern
- [[rxjs]] — Popular reactive library for JavaScript
- [[functional-programming]] — Composing operators mirrors functional composition
- [[asynchronous-programming]] — Broader context of handling time-based operations

## Further Reading

- "RxJS in Action" by Ben Lesh and Dan J. Miller
- Reactive Extensions documentation at reactivex.io
- "Functional Reactive Programming" by Stephen Blackheath and Anthony Jones

## Personal Notes

Reactive programming requires a mental shift from imperative to declarative data flow. The initial learning curve can be steep—understanding which operators to use, when to subscribe and unsubscribe, and how to debug stream issues takes practice. I've found that starting with simple cases like event handling before tackling complex stream composition helps build intuition. The payoff is significant: code that would otherwise require extensive callback or promise chaining becomes linear and readable. Memory leak prevention through proper subscription management is critical—always consider what happens when a subscriber completes or errors.
