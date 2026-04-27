---
title: "Decorator Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [decorator-pattern, design-pattern, structural-pattern, open-closed-principle, dynamic-behavior]
---

# Decorator Pattern

## Overview

The Decorator Pattern is a structural design pattern that allows behavior to be added to an individual object dynamically, without affecting the behavior of other objects from the same class. It is one of the Gang of Four (GoF) design patterns and is particularly important in languages that support open-ended extension of functionality, where it provides an alternative to inheritance for extending class behavior.

The pattern works by wrapping the original object in a "decorator" class that adds the new functionality while delegating the original behavior to the wrapped object. Because the decorator implements the same interface as the original object, clients cannot tell whether they're dealing with the original object or a decorated version. This transparency is a key feature of the pattern.

The Decorator pattern is sometimes called the "Wrapper" pattern, though this name is shared with the Adapter pattern. The distinction is that decorators add functionality while adapters change interfaces. A good mnemonic: "Decorators decorate — they add shiny new features. Adapters adapt — they bridge incompatible plugs."

## Key Concepts

**Dynamic Behavior Addition** is the primary capability of decorators. Unlike inheritance, which adds behavior at compile time and affects all instances of a class, decorators add behavior at runtime to specific instances. This means you can have ten objects of the same base type, each decorated differently, each with its own unique combination of added behaviors. This flexibility is impossible to achieve cleanly with simple inheritance.

**Transparent Wrapping** ensures that the decorated object is indistinguishable from the original from the client's perspective. The decorator implements the same interface as the wrapped object and forwards calls to it (either implicitly or with modifications). This means you can add decorators without changing any client code that uses the original object.

**Composition Over Inheritance** is the guiding principle. The decorator pattern exemplifies this SOLID design principle by using composition rather than inheritance to achieve extension. Instead of creating subclasses for every combination of features (which leads to class explosions), you create a single decorator class for each feature and compose objects at runtime.

**Layered Decorators** can be stacked. Because each decorator wraps another decorator (or the base object), you can add multiple layers of behavior by wrapping the decorated object again. The outermost decorator's call will flow through all layers before reaching the base object, and the response will flow back through all layers in reverse order.

## How It Works

The pattern involves four key participants:

1. **Component** — the base interface that defines the common interface for both the concrete object and decorators
2. **ConcreteComponent** — the base implementation of the component interface that decorators will wrap
3. **Decorator** — the base class for decorators, also implementing the component interface, which wraps a component
4. **ConcreteDecorator** — specific decorator implementations that add particular behaviors

```python
from abc import ABC, abstractmethod

# Component interface
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

# ConcreteComponent - the base object we want to decorate
class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.00

    def description(self) -> str:
        return "Simple coffee"

# Decorator - abstract base for all decorators
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()

# ConcreteDecorators - add specific behaviors
class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.50

    def description(self) -> str:
        return f"{self._coffee.description()} + milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.25

    def description(self) -> str:
        return f"{self._coffee.description()} + sugar"

class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.75

    def description(self) -> str:
        return f"{self._coffee.description()} + whipped cream"

# Usage - compose objects dynamically at runtime
coffee = SimpleCoffee()
print(f"{coffee.description()}: ${coffee.cost():.2f}")
# Output: Simple coffee: $2.00

# Add milk
coffee = MilkDecorator(coffee)
print(f"{coffee.description()}: ${coffee.cost():.2f}")
# Output: Simple coffee + milk: $2.50

# Add sugar on top of milk
coffee = SugarDecorator(coffee)
print(f"{coffee.description()}: ${coffee.cost():.2f}")
# Output: Simple coffee + milk + sugar: $2.75

# Add whipped cream
coffee = WhippedCreamDecorator(coffee)
print(f"{coffee.description()}: ${coffee.cost():.2f}")
# Output: Simple coffee + milk + sugar + whipped cream: $3.50
```

## Practical Applications

**I/O Stream Wrapping** is the classic example from early OOP literature. In Java's standard library, `InputStreamReader` is an adapter while `BufferedInputStream` is a decorator. BufferedInputStream wraps an InputStream and adds buffering behavior without changing the underlying stream's interface. You can stack `BufferedInputStream` with `GZIPInputStream` and `FileInputStream` to get buffered, compressed file reading with no changes to how you use the API.

**Web Middleware** in frameworks like Express.js uses the decorator concept. Each middleware function wraps the request-response cycle, adding behavior (logging, authentication, CORS handling) and then passing control to the next middleware. The middleware pattern is essentially the decorator pattern applied to HTTP request handling.

**Logging and Tracing** decorators can wrap any service or repository to add automatic logging of method calls, parameters, and return values without modifying the underlying class. This cross-cutting concern is a perfect use case for decorators because you want to add it selectively to some objects but not others.

**Caching** decorators wrap expensive operations and return cached results when the same inputs occur again. The caching decorator appears identical to the wrapped service from the outside, but saves computation time on repeated calls.

**Validation and Security** decorators can add input validation, authorization checks, or rate limiting to any service method. Business logic classes remain clean and focused while security policies are applied through wrapping.

## Examples

**Python Decorators (Function Decorators):**

```python
import functools
import time

# Decorator with arguments
def retry(max_attempts=3, delay=1.0):
    """Decorator that retries a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# Decorator without arguments
def log_calls(func):
    """Decorator that logs function calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    """Fetch data from a URL with retry logic."""
    # Implementation here
    pass

# Equivalent to: fetch_data = log_calls(retry(max_attempts=3, delay=0.5)(fetch_data))
```

**Class Decorators (Adding Responsibility):**

```python
from datetime import datetime

class TimestampedMixin:
    """Mixin that adds created/updated timestamps to any class."""
    def __init__(self):
        super().__init__()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        self.updated_at = datetime.utcnow()
        # Actual save logic would go here
        print(f"Saving {self.__class__.__name__} at {self.updated_at}")

class AuditableMixin:
    """Mixin that tracks who created/modified records."""
    def __init__(self):
        super().__init__()
        self.created_by = None
        self.modified_by = []

    def set_creator(self, user_id: str):
        self.created_by = user_id

    def record_modification(self, user_id: str):
        self.modified_by.append({
            'user': user_id,
            'timestamp': datetime.utcnow()
        })

# Composable decorators
class User:
    def __init__(self, name: str):
        self.name = name

# Add timestamping and auditing to User
class AuditedUser(TimestampedMixin, AuditableMixin, User):
    pass

user = AuditedUser("Alice")
user.set_creator("system")
user.record_modification("alice")
user.save()
# Output: Saving AuditedUser at <timestamp>
```

**JavaScript/TypeScript Decorators:**

```typescript
// Decorator to measure execution time
function measure(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = function(...args: any[]) {
        const start = performance.now();
        const result = originalMethod.apply(this, args);
        const end = performance.now();
        console.log(`${propertyKey} took ${end - start}ms`);
        return result;
    };

    return descriptor;
}

function validate(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = function(...args: any[]) {
        // Simple validation: ensure first arg is positive
        if (args[0] <= 0) {
            throw new Error("Argument must be positive");
        }
        return originalMethod.apply(this, args);
    };

    return descriptor;
}

class Calculator {
    @measure
    @validate
    factorial(n: number): number {
        if (n <= 1) return 1;
        return n * this.factorial(n - 1);
    }
}

const calc = new Calculator();
calc.factorial(5);
// Console: "factorial took 0.1ms" (or similar)
```

## Related Concepts

- [[Adapter Pattern]] - Both wrap something, but adapter changes interface while decorator adds functionality
- [[Facade Pattern]] - Both provide simplified access, but facade simplifies a complex subsystem while decorator adds behavior
- [[Proxy Pattern]] - Proxy controls access to an object; decorator adds behavior without controlling access
- [[Open-Closed Principle]] - The design principle that decorators exemplify
- [[Composition Over Inheritance]] - The SOLID principle that motivates using decorators
- [[Software Design Patterns]] - The broader category containing the Decorator pattern

## Further Reading

- "Design Patterns: Elements of Reusable Object-Oriented Software" — Gang of Four, original definition of the Decorator pattern
- "Head First Design Patterns" — Eric Freeman and Elisabeth Robson, visually-oriented introduction
- Python's `functools.wraps` documentation — Understanding how Python decorators maintain metadata
- Java I/O Streams documentation — Classic real-world example of the decorator pattern in action

## Personal Notes

The decorator pattern fundamentally changed how I think about adding functionality to code. Before understanding it, I would solve most extension needs with inheritance — creating subclasses for every combination of features. This leads to the class explosion problem where you need exponentially more subclasses as features multiply.

The decorator pattern taught me to think in layers. Each decorator is a layer that either adds behavior before calling the wrapped object, after receiving the response, or both. This layering model maps incredibly well to real-world concerns like logging (add before and after), caching (check before calling), validation (check before calling), and retry (call multiple times on failure).

I use Python decorators constantly now, especially with functools. The `@login_required`, `@retry`, `@cache`, and `@measure` decorators I write have become fundamental tools in my development practice. The key insight is that decorators are just a syntactic sugar for the same wrapping pattern described in the GoF book — the pattern works the same way whether it's formally implemented or implemented through language syntax.

One caveat: decorators can create "gotchas" if they don't properly forward all arguments or preserve metadata. Using `functools.wraps` in Python or equivalent mechanisms in other languages is essential for maintaining introspection capabilities. I've spent debugging time on issues caused by decorators that silently changed function signatures or broke debuggers' ability to inspect stack traces.
