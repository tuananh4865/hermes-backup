---
title: Observable Pattern
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [patterns, design-patterns, observable, reactive, javascript]
---

# Observable Pattern

## Overview

The Observable Pattern is a behavioral design pattern in which an object, known as the subject or observable, maintains a list of its dependents—called observers—and notifies them automatically of any state changes. This pattern is fundamental to event-driven programming and forms the basis of modern reactive systems. The key benefit is that it enables loose coupling between the subject and its observers: the subject does not need to know anything about the observers it will notify, only that they conform to a common interface.

The pattern is ubiquitous in user interface programming, where changes in underlying data need to be reflected in the UI without tightly coupling the data model to the view layer. It also appears in distributed systems for event dissemination, in sensor networks where multiple processors need to react to incoming signals, and in many layered architecture designs where changes at one layer must propagate to dependent layers.

## How It Works

The pattern involves two primary abstractions: the `Subject` (or `Observable`) and the `Observer`. The Subject holds the canonical state and exposes methods for attaching, detaching, and notifying observers. Observers implement an `update` method (or equivalent) that the Subject calls when its state changes.

```javascript
class Observable {
  constructor() {
    this.observers = [];
    this.state = null;
  }

  subscribe(observer) {
    this.observers.push(observer);
    // Return an unsubscribe function
    return () => {
      this.observers = this.observers.filter(o => o !== observer);
    };
  }

  notify(data) {
    this.observers.forEach(observer => observer.update(data));
  }

  setState(newState) {
    this.state = newState;
    this.notify(newState);
  }
}

class Observer {
  update(data) {
    console.log('Received update:', data);
  }
}

const subject = new Observable();
const observer = new Observer();
const unsubscribe = subject.subscribe(observer);
subject.setState({ message: 'Hello' });
unsubscribe(); // Clean up
```

The subject does not push data to every observer indiscriminately. In more refined implementations, observers can subscribe to specific event types or use predicates to filter the notifications they receive. This selective notification reduces noise for observers that only care about specific changes.

## Key Concepts

**Push vs Pull** — In the push model (used above), the subject actively sends data to observers during notification. In a pull model, observers receive a reference to the subject and extract the data they need on demand. Push is simpler; pull offers more flexibility to observers.

**Subscription Management** — Proper cleanup is essential to prevent memory leaks. Observers that are no longer needed should be unsubscribed. Many implementations return an unsubscribe function from the subscribe method, making cleanup straightforward.

**Hot vs Cold Observables** — A cold observable generates fresh data for each subscriber (like a video-on-demand service). A hot observable multicasts the same data to all current subscribers (like a live broadcast). This distinction affects how subscriptions behave and is especially important in [[reactive-programming]] contexts.

## Practical Applications

The Observable Pattern is the backbone of many UI frameworks. In React, component state changes trigger re-renders through a similar mechanism. In Angular, the `Subject` and `BehaviorSubject` from RxJS are used extensively for component communication and async operations. In [[mobx]], observable state automatically triggers updates in reactive computed values and reactions.

Beyond UI programming, the pattern appears in logging frameworks where multiple appenders (observers) receive log events from a central logger (subject). It is used in financial trading systems where price updates must be distributed to multiple consuming components. It also underlies many pub/sub message brokers and event buses.

## Examples

Consider a stock price tracker. Multiple display components (a price chart, a portfolio summary, a price alert system) all need to react when a stock's price changes. Rather than each component polling for updates, they all subscribe to a `StockPriceService` (the subject). When a price update arrives, the service notifies all subscribers:

```javascript
const priceService = new Observable();

const chart = new Observer();
const portfolio = new Observer();
const alertSystem = new Observer();

priceService.subscribe(chart);
priceService.subscribe(portfolio);
priceService.subscribe(alertSystem);

// When a price tick arrives
priceService.setState({ symbol: 'AAPL', price: 178.52 });
// All three observers receive and react to the update
```

## Related Concepts

- [[mobx]] — State management library that heavily uses the observable pattern
- [[reactive-programming]] — Paradigm built on observables and streams
- [[observer-pattern]] — The classic Gang of Four Observer pattern (closely related)
- [[event-driven-architecture]] — Architecture style where observable patterns are common
- [[rxjs]] — Library providing rich observable primitives for reactive programming

## Further Reading

- Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four)
- RxJS Documentation
- MobX Official Guide

## Personal Notes

The Observable Pattern is one of those patterns that seems simple but reveals deeper complexity as you use it in production systems. Subscription management is where most teams run into trouble—failing to unsubscribe from observables is one of the most common sources of memory leaks in JavaScript applications, particularly in Single Page Applications with frequent component mounting and unmounting. Using composition patterns and leveraging higher-level abstractions like `useEffect` cleanup functions in React or `takeUntil` operators in RxJS can help avoid these pitfalls.
