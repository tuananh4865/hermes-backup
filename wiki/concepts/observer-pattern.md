---
title: "Observer Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, gang-of-four, behavioral-patterns, event-driven, software-design, architecture]
---

# Observer Pattern

## Overview

The Observer Pattern is a behavioral [[design-patterns|design pattern]] defined by the Gang of Four (Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides) in their seminal 1994 book "Design Patterns: Elements of Reusable Object-Oriented Software." The pattern defines a one-to-many dependency between objects so that when one object (the subject) changes state, all its dependents (observers) are automatically notified and updated. This is also known as the Publish-Subscribe pattern, though there are subtle differences between classic Observer and Pub-Sub implementations.

The Observer Pattern is one of the most widely used patterns in software development because it provides an elegant solution to a common problem: how to keep multiple parts of a system in sync without tightly coupling them. The pattern decouples the object that holds state (the subject) from the objects that need to react to state changes (the observers). This separation of concerns makes systems easier to understand, test, and evolve.

The pattern appears throughout modern software development under different names and implementations. JavaScript's event handling system, React's state management, reactive programming libraries like RxJS, and message-oriented middleware all draw from Observer's core insight: define a subscription mechanism that allows dependents to register for and receive state change notifications from a central publisher.

## Key Concepts

**Subject** (also called Observable or Publisher) is the object that holds the state others want to observe. The subject maintains a collection of observers and provides methods to attach, detach, and notify observers. Crucially, the subject does not need to know anything about what its observers do with the notifications—it simply broadcasts changes to all registered parties.

**Observer** (also called Subscriber or Listener) defines an update interface with a method (often called `update()`, `notify()`, or `onNext()`) that the subject calls when state changes. Observers register themselves with the subject to receive notifications. The observer interface decouples the subject from specific observer implementations.

**Notification** is the mechanism by which the subject communicates state changes to observers. In the simplest implementation, the subject passes no data and observers must pull the state they need. In richer implementations, the subject passes changed data directly to observers (push model), reducing the need for observers to query state.

**Subscription Lifecycle** describes how observers come to receive and stop receiving notifications. Observers subscribe by calling an attach/register method on the subject, and unsubscribe by calling a detach/unregister method. Proper subscription management prevents memory leaks (observers that remain registered after they're no longer needed, preventing garbage collection).

**Push vs. Pull Models**: In a push model, the subject sends changed data to observers during notification. This is efficient when observers need specific data, but couples observers to the subject's data structure. In a pull model, the subject sends only a notification saying "state changed," and observers query the subject for what they need. The pull model is more decoupled but may trigger redundant updates.

## How It Works

The Observer Pattern can be implemented in many languages in a straightforward way. Here is a canonical Python implementation:

```python
from abc import ABC, abstractmethod
from typing import List

# Observer interface
class Observer(ABC):
    @abstractmethod
    def on_update(self, subject: "Subject", event: str, data: any) -> None:
        """Called when the subject's state changes."""
        pass

# Subject (Observable) class
class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
        self._state: dict = {}

    def attach(self, observer: Observer) -> None:
        """Register an observer to receive notifications."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Unregister an observer."""
        self._observers.remove(observer)

    def _notify(self, event: str, data: any = None) -> None:
        """Notify all registered observers of a state change."""
        for observer in self._observers:
            observer.on_update(self, event, data)

    @property
    def state(self) -> dict:
        return self._state.copy()

    def set_state(self, key: str, value: any) -> None:
        """Update state and notify observers."""
        self._state[key] = value
        self._notify(f"state.{key}", {"key": key, "value": value})


# Concrete observer implementation
class DataDashboard(Observer):
    def __init__(self, name: str):
        self.name = name

    def on_update(self, subject: Subject, event: str, data: any) -> None:
        print(f"[{self.name}] Received: {event} with data {data}")
        print(f"[{self.name}] Current state: {subject.state}")
```

The pattern can also be implemented as a generic observable with typed event handlers, which is how many modern reactive libraries work:

```python
# Modern event-based observable (similar to many JS/RxJS implementations)
class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, List[callable]] = {}

    def on(self, event: str, handler: callable) -> callable:
        """Register a handler for an event. Returns unsubscribe function."""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(handler)
        
        # Return unsubscribe function
        def unsubscribe():
            self._listeners[event].remove(handler)
        return unsubscribe

    def emit(self, event: str, data: any = None) -> None:
        """Emit an event to all registered handlers."""
        for handler in self._listeners.get(event, []):
            handler(data)

# Usage:
emitter = EventEmitter()
unsubscribe = emitter.on("order_placed", lambda data: print(f"Order: {data}"))
emitter.emit("order_placed", {"order_id": 123, "total": 99.99})
unsubscribe()  # Stop receiving events
```

## Practical Applications

The Observer Pattern is foundational to many real-world software systems:

**UI Frameworks** use Observer extensively for data-binding. When a model changes, the UI automatically re-renders. In [[react-components]], state changes trigger re-renders. In [[vue.js]], the reactivity system uses Observer-like mechanisms to track dependencies and update the DOM. See [[state-management]] and [[reactive-programming]].

**Event Systems** in languages and frameworks are direct applications of Observer. Node.js's `EventEmitter`, Python's `asyncio.Event`, Java's `PropertyChangeSupport`, and C#'s `event` keyword all implement Observer or variants. See [[event-handling]].

**Messaging and Event Streaming** systems like [[kafka]], [[rabbitmq]], and [[message-brokers]] implement a distributed version of Observer where the subject is a message topic and observers are consumers. This scales Observer beyond a single process.

**Distributed Systems Notifications** use Observer-like patterns for service discovery and configuration updates. When a microservice configuration changes in a central registry, all affected services are notified. Tools like [[consul]] and [[etcd]] implement key-value observation for distributed configuration.

**Model-View-Controller (MVC)** architecture uses Observer to keep views synchronized with models. The model is the subject, views are observers. When the model changes, all attached views automatically update. See [[model-view-controller]].

## Examples

A practical use of the Observer Pattern in a notification system:

```python
# Observer-based notification system for a trading platform
from decimal import Decimal
from datetime import datetime

class PriceAlert(Observer):
    """Observer that triggers alerts when price thresholds are crossed."""
    def __init__(self, symbol: str, threshold: Decimal, direction: str):
        self.symbol = symbol
        self.threshold = threshold
        self.direction = direction  # "above" or "below"
        self.triggered = False

    def on_update(self, subject: "StockTicker", event: str, data: dict) -> None:
        if event == "price_update" and data["symbol"] == self.symbol:
            price = data["price"]
            should_trigger = (
                (self.direction == "above" and price >= self.threshold) or
                (self.direction == "below" and price <= self.threshold)
            )
            if should_trigger and not self.triggered:
                self.triggered = True
                print(f"ALERT: {self.symbol} is now {self.direction} {self.threshold} at {price}")

class StockTickerSubject:
    """Subject that publishes price updates to all registered observers."""
    def __init__(self):
        self._observers: List[Observer] = []
        self._prices: Dict[str, Decimal] = {}

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def _notify(self, event: str, data: dict):
        for obs in self._observers:
            obs.on_update(self, event, data)

    def update_price(self, symbol: str, price: Decimal):
        self._prices[symbol] = price
        self._notify("price_update", {"symbol": symbol, "price": price, "time": datetime.now()})

# Usage:
ticker = StockTickerSubject()
alert = PriceAlert("AAPL", Decimal("150.00"), "above")
ticker.attach(alert)
ticker.update_price("AAPL", Decimal("151.00"))  # Triggers alert
```

## Related Concepts

- [[Publish-Subscribe Pattern]] — A related messaging pattern that extends Observer with a message broker intermediary
- [[Event-Driven Architecture]] — Architectural style built on patterns like Observer
- [[Reactive Programming]] — Programming paradigm based on Observer (e.g., RxJS, reactive extensions)
- [[Model-View Controller]] — Architecture that often uses Observer for view synchronization
- [[Event Handling]] — The practical application of Observer in UI systems
- [[State Management]] — Observer is a fundamental mechanism in state management systems
- [[Message Queue]] — Distributed extension of Observer concepts
- [[Gang of Four]] — The authors who documented this pattern among 23 foundational design patterns
- [[Behavioral Patterns]] — The category of design patterns to which Observer belongs
- [[Design Patterns]] — The broader discipline of reusable software architecture
- [[Component Lifecycle]] — Observer registration often ties into component lifecycle events

## Further Reading

- Gamma, Helm, Johnson, Vlissides — "Design Patterns: Elements of Reusable Object-Oriented Software" (Gang of Four book)
- Martin Fowler, "Patterns of Enterprise Application Architecture" — Discusses Observer in enterprise contexts
- [[behavioral-patterns]]

## Personal Notes

> The Observer Pattern's biggest pitfall in practice is managing the subscription lifecycle carefully. If observers don't unsubscribe when they're done, you get memory leaks — especially in long-running applications. In languages without automatic garbage collection, this is more obvious; in garbage-collected languages like Python and JavaScript, it shows up as subtle memory growth over time. I always pair Observer implementations with context managers or weak references where possible. Also, be careful about update order — if observers can modify the subject's state, you can get cascading updates that are hard to reason about.
