---
title: Functional Reactive Programming
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [functional-reactive-programming, frp, reactive-programming, functional-programming, rxjs, observables, asynchronous]
---

# Functional Reactive Programming

## Overview

Functional Reactive Programming (FRP) is a programming paradigm that combines the principles of functional programming with reactive programming to handle time-varying values and event streams in a declarative, composable manner. FRP represents a significant refinement of traditional reactive programming, applying the rigor and expressiveness of functional programming concepts—immutability, pure functions, function composition, and higher-order functions—to the domain of asynchronous data streams.

At its core, FRP models dynamic values, called "signals" or "behaviors," as functions that map time to values. Events are modeled as discrete occurrences with associated times, while behaviors represent continuous values that change over time. This mathematical foundation provides precise semantics for reasoning about time-dependent computations, eliminating many of the ambiguities that plague callback-based asynchronous code.

The distinction between FRP and plain reactive programming lies in the emphasis on functional principles. Where traditional reactive programming might allow side effects within operators and subscriptions, FRP insists on pure, composable transformations. An FRP expression describes what computation to perform, not how to perform it stepwise. This separation of concerns makes FRP programs more predictable, testable, and amenable to formal verification.

## Key Concepts

**Signals (Behaviors)** represent values that vary continuously over time. In classic FRP, a signal is a function `Signal a = Time -> a` that yields a value of type `a` at any given point in time. For example, the current mouse position, the user's session state, or the current stock price can be modeled as signals. Signals are always defined, providing a value at every instant.

**Events** represent discrete occurrences that happen at specific points in time. Unlike signals, events are absent most of the time—they exist only at the moments when something happens. A button click, a keyboard press, an HTTP response arrival—these are all events. Events carry a value (the click coordinates, the key pressed, the response data) and occur at a particular time.

**Cellular** is a concept from some FRP implementations that represents a discrete-time signal—a value that changes only at specific moments but remains constant between changes. This is particularly useful for modeling state that updates in response to events, such as a counter that increments on button clicks.

**Functional Composition** in FRP means that signals and events are transformed through pure functions. The `map` operation applies a function to every value in a stream. The `filter` operation keeps only values that satisfy a predicate. The `combine` operation merges multiple streams into one. These compositions can be nested arbitrarily, building complex data flow pipelines from simple, reusable components.

```haskell
-- Classic FRP in Haskell (Netwire/Apecs style)
-- A behavior that increases faster when mouse is on the right
velocity :: Behavior (V2 Double)
velocity = (\pos -> V2 (hTerm 80) (vTerm 60))
  where
    pos = mousePosition
    hTerm w = (fromIntegral w / 2 - mouseX) * 0.01
    vTerm h = (fromIntegral h / 2 - mouseY) * 0.01
```

## How It Works

FRP implementations typically use one of two evaluation models: pull-based (demand-driven) or push-based (data-driven). Pull-based systems compute values only when they are needed, like a spreadsheet recalculating only visible cells. Push-based systems compute values immediately when input signals change, propagating updates through the dependency graph.

Modern FRP libraries in JavaScript/TypeScript, such as those built on RxJS, adopt a push-based model aligned with event-driven execution. When an event occurs, the system pushes the new value through a chain of operators to all subscribers. Each operator in the chain is a pure function that transforms the stream without modifying the original.

```typescript
// FRP-style composition in TypeScript with RxJS
import { interval, combineLatest, map, scan, startWith } from 'rxjs';

// A temperature reading that updates every second
const temperature$ = interval(1000).pipe(
  map(() => 20 + Math.random() * 10), // Simulated sensor
  startWith(20)
);

// A humidity reading that updates every second
const humidity$ = interval(1000).pipe(
  map(() => 40 + Math.random() * 20), // Simulated sensor
  startWith(40)
);

// Combine into a comfort index using pure functions
const comfortIndex$ = combineLatest([temperature$, humidity$]).pipe(
  map(([temp, humidity]) => {
    // Pure function: no side effects, same inputs always yield same outputs
    const discomfort = Math.abs(temp - 22) * 2 + Math.abs(humidity - 50);
    return {
      temperature: Math.round(temp * 10) / 10,
      humidity: Math.round(humidity * 10) / 10,
      comfort: discomfort < 10 ? 'comfortable' : discomfort < 20 ? 'tolerable' : 'uncomfortable'
    };
  }),
  scan((acc, curr) => ({ ...acc, latest: curr }), { latest: null })
);

comfortIndex$.subscribe(reading => {
  console.log(`Comfort: ${reading.latest?.comfort} (${reading.latest?.temperature}°C, ${reading.latest?.humidity}%)`);
});
```

The semantics of time in FRP also handle problems like "glitches" (inconsistent intermediate states during propagation) and memory leaks (dangling subscriptions). Well-designed FRP implementations guarantee that events are processed in causal order and that subscription lifetimes are properly managed through explicit disposal or automatic cleanup.

## Practical Applications

**Interactive User Interfaces** benefit enormously from FRP. UI state—form field values, selection states, visibility toggles—naturally forms a reactive graph. FRP allows expressing complex UI update logic as compositions of simple transformations, making it easier to reason about behavior and test individual components in isolation.

**Simulation and Game Development** use FRP to model entities with continuous state (position, velocity, health) that evolves over time. The declarative nature of FRP makes it straightforward to compose multiple simulation elements and add new behaviors without modifying existing code.

**Signal Processing** in audio, video, or financial applications aligns well with FRP's model of time-varying values. Processing pipelines can be expressed as compositions of filters, transforms, and aggregators, with clear data flow that aids optimization and debugging.

**Robotics and Control Systems** model sensor inputs and actuator outputs as continuous signals, applying control theory concepts like feedback loops and filters through FRP's compositional operators.

## Examples

Consider a chat application where messages arrive as events and need to be displayed:

```typescript
import { fromEvent, merge, EMPTY } from 'rxjs';
import { scan, startWith, map, filter, distinctUntilChanged } from 'rxjs/operators';

// Message events from various sources
const socketMessages$ = fromEvent(socket, 'message').pipe(
  map(event => JSON.parse(event.data))
);

const localMessages$ = fromEvent(form, 'submit').pipe(
  map(event => ({ type: 'local', text: event.target.value, timestamp: Date.now() })),
  filter(text => text.length > 0)
);

// All messages combined into a stream of conversation states
const conversation$ = merge(socketMessages$, localMessages$).pipe(
  scan((conversation, message) => ({
    messages: [...conversation.messages, message],
    unreadCount: message.type === 'remote' ? conversation.unreadCount + 1 : conversation.unreadCount
  }), { messages: [], unreadCount: 0 }),
  startWith({ messages: [], unreadCount: 0 })
);

// Derived states computed from conversation stream
const unreadCount$ = conversation$.pipe(
  map(c => c.unreadCount),
  distinctUntilChanged()
);

const recentMessages$ = conversation$.pipe(
  map(c => c.messages.filter(m => Date.now() - m.timestamp < 60000)),
  startWith([])
);

// UI updates driven purely by state changes
unreadCount$.subscribe(count => {
  badge.textContent = count > 0 ? String(count) : '';
});
```

## Related Concepts

- [[reactive-programming]] — The broader paradigm FRP extends
- [[rxjs]] — Popular reactive library with functional composition patterns
- [[functional-programming]] — The programming style FRP draws from
- [[observable-pattern]] — The underlying observer pattern
- [[asynchronous-programming]] — Time-dependent computation context
- [[redux]] — Predictable state management inspired by FRP principles

## Further Reading

- "Functional Reactive Programming" by Stephen Blackheath and Anthony Jones
- "RxJS in Action" by Ben Lesh and Dan J. Miller
- "Essentials of Reactive Programming" by Jonas Deußer and Rafael Winter
- The Reactive Extensions (Rx) documentation at reactivex.io

## Personal Notes

FRP changed how I think about state. Instead of mutable variables updated by callbacks, I now see dynamic values as streams that can be composed, transformed, and combined through pure functions. The initial learning curve is steeper than plain reactive programming due to the functional concepts, but the payoff in testability and composability is substantial. I recommend starting with simple event transformations before tackling complex state machines. The key insight is that FRP lets you describe what computations should happen, not when or how to execute them step by step.
