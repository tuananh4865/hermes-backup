---
title: "Adapter Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [adapter-pattern, design-pattern, structural-pattern, interface-compatibility, software-design]
---

# Adapter Pattern

## Overview

The Adapter Pattern is a structural design pattern that allows objects with incompatible interfaces to collaborate. It acts as a bridge between two incompatible interfaces by wrapping one interface (the adaptee) and exposing a different interface that the client expects. The pattern is called "adapter" because it performs exactly the same function as a power adapter traveling with you to a foreign country — translating one interface into another so that devices (or in our case, software components) can work together despite having different interfaces.

The Adapter Pattern is one of the classic Gang of Four (GoF) design patterns, first documented in the seminal "Design Patterns: Elements of Reusable Object-Oriented Software." It falls under the structural category of patterns, which deal with how classes and objects are composed to form larger structures.

In practice, adapters are everywhere in software systems. When you use a third-party library that has a different interface than what your code expects, you often create or use an adapter. When you integrate with a legacy system, you wrap it in an adapter to present a modern interface to new code. When you test components in isolation, you use test adapters (mocks and stubs) to simulate dependencies.

## Key Concepts

**Wrapper** is the core concept behind the adapter. The adapter wraps the adaptee (the thing with the incompatible interface) and presents itself to the client with an interface the client understands. The client thinks it's talking to something that speaks its language, but the adapter is actually translating those requests into something the adaptee understands.

**Interface Compatibility** is what adapters achieve. The adapter doesn't change the adaptee's behavior — it changes how that behavior is accessed. If the adaptee speaks German and the client speaks English, the adapter is the translator who conveys the same meaning in different words. The underlying message and behavior remain identical.

**Two-Way Adapters** are possible but less common. A typical adapter translates client requests to adaptee calls. A two-way adapter can also translate adaptee callbacks or events back to the client in the client's expected format. This is necessary when both sides need to initiate communication.

**Class Adapters vs Object Adapters** represent the two primary implementation strategies. Class adapters use inheritance (the adapter inherits from both the target interface and the adaptee), while object adapters use composition (the adapter holds a reference to the adaptee and delegates calls to it). Object adapters are more common because they allow adaptation of classes you don't control and don't require altering the inheritance hierarchy.

## How It Works

The adapter pattern involves four key participants:

1. **Target** — the interface that the client knows and expects to work with
2. **Client** — the code that has a dependency on the Target interface
3. **Adaptee** — the existing class or component with an incompatible interface that needs adapting
4. **Adapter** — the wrapper that implements Target and internally uses Adaptee to fulfill requests

```python
from abc import ABC, abstractmethod

# The interface the client expects (Target)
class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount: float, currency: str) -> dict:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> dict:
        pass

# The existing third-party service with a different interface (Adaptee)
class LegacyPayPalAPI:
    def send_payment(self, sum_in_cents: int, from_account: str, to_account: str) -> str:
        # Legacy API uses cents instead of decimal, different parameter names
        return f"TXN-{sum_in_cents}-{from_account}-{to_account}"

    def reverse_transaction(self, transaction_reference: str) -> bool:
        return True

# The adapter that bridges the gap (Adapter)
class PayPalAdapter(PaymentGateway):
    def __init__(self, legacy_api: LegacyPayPalAPI):
        self._api = legacy_api

    def pay(self, amount: float, currency: str) -> dict:
        # Convert decimal to cents, restructure parameters
        cents = int(amount * 100)
        # In real code, you'd look up accounts based on currency
        transaction_id = self._api.send_payment(cents, "OUR_ACCOUNT", "MERCHANT_ACCOUNT")
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "currency": currency,
            "amount": amount
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        success = self._api.reverse_transaction(transaction_id)
        return {
            "status": "success" if success else "failed",
            "refunded_amount": amount
        }

# Client code works with the PaymentGateway interface
def process_payment(gateway: PaymentGateway, amount: float):
    result = gateway.pay(amount, "USD")
    print(f"Payment {result['transaction_id']}: {result['status']}")

# Usage
legacy_api = LegacyPayPalAPI()
adapter = PayPalAdapter(legacy_api)
process_payment(adapter, 99.99)  # Works! Client is happy.
```

In this example, the client expects a `PaymentGateway` interface with `pay()` and `refund()` methods. The legacy `LegacyPayPalAPI` has a completely different interface using `send_payment()` and `reverse_transaction()` with different parameter types. The `PayPalAdapter` wraps the legacy API and presents the interface the client expects, doing any necessary translation internally.

## Practical Applications

**Third-Party Library Integration** is the most common use case. When you adopt a new library, it rarely has the exact interface your codebase expects. You create adapters to make the library conform to your interface, allowing you to swap out the library later without changing client code. This is essentially the dependency inversion principle in action.

**Legacy System Modernization** allows new code to work with old systems without rewriting them. The adapter presents a modern interface to new code while internally calling the legacy system in whatever protocol or format it requires. This is particularly valuable in large organizations where legacy systems can't be replaced immediately.

**Testing and Mocking** uses adapters extensively. Test doubles (mocks, stubs, fakes) are adapters that implement the same interface as production dependencies but produce controlled, predictable behavior for tests. The adapter pattern explains why test doubles can seamlessly replace real dependencies.

**Cross-Language Integration** becomes possible through adapters. When components are written in different programming languages, adapters can bridge the gap, translating calls and data structures between language ecosystems. This is common in polyglot microservice architectures.

**Cloud Service Abstraction** allows applications to remain cloud-agnostic. By defining a internal interface and creating adapters for AWS, GCP, and Azure services, you can switch cloud providers or use different providers in different environments without changing application code.

## Examples

**XML to JSON Adapter:**

```python
import xml.etree.ElementTree as ET
import json

class XMLToJSONAdapter:
    """Adapts XML data to look like JSON-accessible data."""

    def __init__(self, xml_string: str):
        self._root = ET.fromstring(xml_string)

    def get(self, key: str):
        """Simulate dict-like access, converting XML to pseudo-JSON."""
        # Handle root element attributes
        if key == self._root.tag:
            result = {}
            # Add attributes
            for attr, value in self._root.attrib.items():
                result[attr] = value
            # Add child elements
            for child in self._root:
                result[child.tag] = child.text
            return result
        raise KeyError(f"Key '{key}' not found in XML document")

    def __getitem__(self, key: str):
        return self.get(key)

# Usage
xml_data = '''<?xml version="1.0"?>
<user id="123">
    <name>Alice Smith</name>
    <email>alice@example.com</email>
</user>'''

adapter = XMLToJSONAdapter(xml_data)
print(adapter["user"]["name"])  # "Alice Smith"
print(adapter["user"]["id"])     # "123"
```

**Database Adapter (Repository Pattern combined with Adapter):**

```python
from abc import ABC, abstractmethod
from typing import List, Optional

# Target interface for data access
class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    def find_all(self) -> List[dict]:
        pass

    @abstractmethod
    def save(self, user: dict) -> dict:
        pass

# Adaptee: Legacy in-memory database with different interface
class LegacyUserDatabase:
    def getUserByID(self, id: int) -> Optional[dict]:
        for user in self._users:
            if user['userId'] == id:
                return user
        return None

    def getAllUsers(self) -> List[dict]:
        return self._users

    def insertUser(self, user: dict) -> None:
        user['userId'] = len(self._users) + 1
        self._users.append(user)

    _users = []

# Adapter
class LegacyUserAdapter(UserRepository):
    def __init__(self, legacy_db: LegacyUserDatabase):
        self._db = legacy_db

    def find_by_id(self, user_id: int) -> Optional[dict]:
        # Translate our interface to legacy interface
        user = self._db.getUserByID(user_id)
        if user:
            return self._translate_to_external(user)
        return None

    def find_all(self) -> List[dict]:
        users = self._db.getAllUsers()
        return [self._translate_to_external(u) for u in users]

    def save(self, user: dict) -> dict:
        # Translate from external format to legacy format
        legacy_user = {
            'firstName': user.get('first_name', ''),
            'lastName': user.get('last_name', ''),
            'email': user.get('email', '')
        }
        self._db.insertUser(legacy_user)
        return self._translate_to_external(legacy_user)

    def _translate_to_external(self, legacy_user: dict) -> dict:
        """Convert legacy format to our standard external format."""
        return {
            'id': legacy_user['userId'],
            'first_name': legacy_user.get('firstName', ''),
            'last_name': legacy_user.get('lastName', ''),
            'email': legacy_user.get('email', '')
        }
```

## Related Concepts

- [[Decorator Pattern]] - Both wrap something, but decorator adds behavior while adapter changes interface
- [[Facade Pattern]] - Both provide simplified interfaces, but facade simplifies a complex subsystem while adapter bridges incompatible interfaces
- [[Proxy Pattern]] - Proxy provides a surrogate for the same interface; adapter provides a different interface
- [[Bridge Pattern]] - Similar in separating abstraction from implementation, but Bridge starts with two independent interfaces while Adapter starts with incompatible interfaces to reconcile
- [[Repository Pattern]] - Often implemented alongside Adapter for database access abstraction
- [[Software Design Patterns]] - The broader category containing the Adapter pattern

## Further Reading

- "Design Patterns: Elements of Reusable Object-Oriented Software" — Gang of Four, the original reference for the Adapter pattern
- "Head First Design Patterns" — Eric Freeman and Elisabeth Robson, an accessible introduction
- "Patterns of Enterprise Application Architecture" — Martin Fowler, includes treatment of adapter patterns in enterprise contexts
- "The Adapter Pattern in Practice" — Various online tutorials demonstrating real-world adapter implementations

## Personal Notes

The Adapter pattern is one of those patterns I use almost every day without necessarily thinking about it by name. Every time I write a wrapper around a library call, I'm creating an adapter. The value of recognizing it as a formal pattern is knowing when to invest in a proper adapter vs. just doing inline translation.

What I've learned is that adapter interfaces should be defined by the client needs, not by the adaptee's structure. It's tempting to simply expose the adaptee's interface with minimal translation, but that usually means the adapter is leakier than it should be and changes to the adaptee ripple through to clients. A well-designed adapter defines its own clean interface and completely hides the adaptee's interface behind it.

The testability benefit is huge. Once you have adapters for your external dependencies (databases, HTTP clients, file systems), testing your business logic becomes trivial — you just inject mock adapters. The adapter pattern is essentially a prerequisite for clean unit testing in any non-trivial system.

I sometimes see adapters confused with facades. The key distinction: adapters are for clients that need to use the adaptee (the existing component), while facades are for clients that don't need all the functionality of the underlying subsystem. If you want to use a component but it has the wrong interface, you need an adapter. If you have a complex subsystem and most clients only need a simplified view, you need a facade.
