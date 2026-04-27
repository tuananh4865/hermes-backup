---
title: "Prototypal Inheritance"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [javascript, inheritance, oop, prototype-chain, prototype]
---

# Prototypal Inheritance

Prototypal inheritance is a JavaScript-specific inheritance mechanism where objects inherit properties and methods directly from other objects via their prototype chain, rather than through class-based hierarchies. Unlike classical inheritance (used in Java, C++, Python), prototypal inheritance is dynamic—objects can inherit from other objects at runtime, and the prototype chain can be modified after creation.

## Overview

JavaScript's prototypal inheritance model is one of its most distinctive and powerful features. In JavaScript, almost everything is an object—including functions and arrays—and every object has an internal property called `[[Prototype]]` (exposed as `__proto__` in older environments or accessible via `Object.getPrototypeOf()`).

When you access a property on an object, JavaScript first looks at the object's own properties. If not found, it looks at the object's prototype, then the prototype's prototype, and so on up the chain until it reaches `Object.prototype` (whose prototype is `null`). This chain of objects is the prototype chain.

Prototypal inheritance enables object composition, delegation, and object cloning without the constraints of class hierarchies. It was initially misunderstood as a limitation compared to classical OOP, but experienced developers recognize it as a flexible pattern supporting many inheritance models including class-like syntax (which in JavaScript is syntactic sugar over prototypes).

## Key Concepts

**Prototype Chain**: A linked list of objects where each object has a reference to its prototype. Property lookup traverses this chain until the property is found or the chain ends at `null`.

**`__proto__` vs `prototype`**: `__proto__` is an object's actual prototype (its internal `[[Prototype]]`). `prototype` is a property on constructor functions that becomes the prototype of objects created with `new`.

**Constructor Functions**: Before ES6 classes, constructor functions were the primary way to create objects with shared methods. The `prototype` property on constructor functions allowed methods to be shared across instances.

**Object.create()**: The explicit way to create an object with a specific prototype, allowing inheritance without constructor functions.

**ES6 Classes**: The `class` keyword provides cleaner syntax for prototypal inheritance but desugars to the same underlying prototype chain mechanism.

## How It Works

Understanding the prototype chain mechanics:

1. **Object Creation**: When you create an object with `{}` or `Object.create()`, it automatically gets a prototype assigned.

2. **Property Lookup**: Accessing `obj.property` triggers a lookup: check own properties → check `obj.__proto__` → check `obj.__proto__.__proto__` → repeat until found or chain ends.

3. **Method Resolution**: Methods on an object are resolved through the prototype chain. When you call `obj.method()`, `this` inside the method still refers to `obj`, not the prototype.

4. **Shadowing**: If you assign a property to an object that exists on a prototype, it creates an "own property" that shadows the prototype's property.

5. **Modification**: Adding properties to a prototype automatically makes them available to all objects that inherit from it, even those created before the modification.

```javascript
// Constructor function pattern
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    return `${this.name} makes a sound`;
};

const dog = new Animal('Rex');
console.log(dog.speak()); // "Rex makes a sound"

// Object.create pattern for explicit inheritance
const feline = Object.create(Animal.prototype);
feline.name = 'Whiskers';
console.log(feline.speak()); // "Whiskers makes a sound"

// ES6 class pattern (syntactic sugar over prototypes)
class Vehicle {
    constructor(wheels) {
        this.wheels = wheels;
    }
    
    describe() {
        return `A vehicle with ${this.wheels} wheels`;
    }
}

class Car extends Vehicle {
    constructor(color) {
        super(4);
        this.color = color;
    }
}
```

## Practical Applications

- **Code Reuse**: Share methods across multiple object instances without duplicating function definitions in memory.

- **Mixins**: Create reusable pieces of functionality that can be composed into any object, even if the object already has a different prototype chain.

- **Library Patterns**: Many JavaScript libraries (lodash, express, mongoose) use prototypal inheritance internally for performance and memory efficiency.

- **Framework Extension**: Plugins often extend base objects by modifying their prototypes, adding methods to all instances retroactively.

- **Feature Detection**: The prototype chain can be checked to detect browser features (e.g., checking if `Array.prototype.includes` exists).

## Examples

**Mixin Pattern**:
```javascript
// A mixin adds methods to an object
const speaker = {
    speak(words) {
        return `${this.name} says: ${words}`;
    }
};

const walker = {
    walk() {
        return `${this.name} is walking`;
    }
};

// Compose behaviors
const person = Object.assign({}, speaker, walker);
person.name = 'Alice';
console.log(person.speak('Hello!')); // "Alice says: Hello!"
console.log(person.walk()); // "Alice is walking"
```

**Prototype Chain Inspection**:
```javascript
const arr = [1, 2, 3];

// Inspect the prototype chain
console.log(Object.getPrototypeOf(arr));        // Array.prototype
console.log(Object.getPrototypeOf([]));        // Array.prototype
console.log(Object.getPrototypeOf(Array.prototype)); // Object.prototype
console.log(Object.getPrototypeOf(Object.prototype)); // null
```

## Related Concepts

- [[JavaScript]] — The language that implements prototypal inheritance
- [[Class Inheritance]] — The classical OOP model that contrasts with prototypes
- [[Object-Oriented Programming]] — Broader programming paradigm
- [[Constructor Pattern]] — Pattern for creating objects with shared behavior
- [[Mixins]] — Compositional pattern for adding functionality
- [[This Keyword]] — How `this` binding works in prototype methods

## Further Reading

- [MDN: Inheritance and the prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)
- [You Don't Know JS: this & Object Prototypes](https://github.com/getify/You-Dont-Know-JS) — Deep dive by Kyle Simpson
- [Prototypes as Classes in JavaScript](https://blog.digitalbunker.dev/2020/08/03/why-prototypal-inheritance-matters/) — Article on the merits of prototypal over classical

## Personal Notes

Prototypal inheritance was JavaScript's most misunderstood feature in the jQuery era, with many developers treating ES6 classes as "real" inheritance and prototypes as legacy. Now that the mental model is better understood, the power of dynamic inheritance is appreciated again. The key insight is that classes in JavaScript are just a convenient syntax—underneath, it's still objects linked through prototypes. Understanding this helps debug tricky issues with `this` binding and `super` calls.
