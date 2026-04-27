---
title: "Object Oriented Programming"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [oop, programming-paradigm, software-engineering, design]
---

# Object Oriented Programming

## Overview

Object Oriented Programming (OOP) is a fundamental programming paradigm that organizes software design around data, or objects, rather than functions and logic. In OOP, an object is a self-contained unit that combines both state (data attributes) and behavior (methods functions) into a single entity. This approach to programming emerged from the need to manage increasing software complexity and promote reusable, maintainable code.

The core idea behind OOP is to model real-world concepts as objects within the program. For example, a banking application might have Account objects, Customer objects, and Transaction objects, each encapsulating their relevant data and behaviors. This modeling approach makes it easier to reason about systems because objects map more naturally to how we perceive the real world.

OOP is distinguished from procedural programming paradigms by its emphasis on abstraction, encapsulation, and message passing between objects. Rather than having a program flow through a series of procedures operating on scattered data, OOP brings data and behavior together and defines clear interfaces for how objects interact. This organization helps manage complexity in large-scale software systems and is the dominant paradigm in many popular programming languages including Java, Python, C++, and C#.

The concept of objects and classes (templates for creating objects) forms the foundation of OOP. A class defines the structure and behavior that all objects of that type will possess, while individual objects are instances of their respective classes. This class-based approach enables developers to create blueprints for complex systems and instantiate as many objects as needed.

## Pillars

The four fundamental principles of Object Oriented Programming, often called the "four pillars," provide the guidelines and constraints that shape how OOP systems are designed and how objects interact.

**Encapsulation** is the mechanism of bundling data and methods that operate on that data within a single unit, while restricting direct access to some of an object's internal state. Encapsulation protects an object's integrity by preventing external code from arbitrarily modifying its internal data. Instead, interactions occur through a well-defined public interface (getters, setters, and other methods). This data hiding prevents unintended dependencies and allows implementation details to change without affecting the code that uses the object. Languages implement encapsulation using access modifiers like private, protected, and public to control visibility.

**Inheritance** enables a class (called a subclass or derived class) to acquire the properties and behaviors of another class (called a superclass or parent class). Inheritance promotes code reuse by allowing common functionality to be defined once in a parent class and shared across multiple child classes. A subclass can extend the capabilities of its parent by adding new attributes and methods, or it can override existing behavior to provide specialized implementations. This creates a hierarchy of classes that reflects "is-a" relationships, such as a SavingsAccount "is-a" type of BankAccount.

**Polymorphism** allows objects of different classes to be treated uniformly through a common interface. The term means "many forms" and refers to the ability of different objects to respond to the same method call in ways specific to their type. In compile-time polymorphism (overloading), multiple methods share the same name but differ in their parameter types or arity. In runtime polymorphism (overriding), a subclass provides a specific implementation of a method already defined in its parent class, and the correct version is determined dynamically at runtime through mechanisms like virtual dispatch.

**Abstraction** is the concept of hiding complex implementation details behind a simplified interface. Abstraction allows developers to interact with objects at a high level without needing to understand the intricate details of how they work internally. Like encapsulation, abstraction simplifies code usage and reduces dependencies, making systems more modular and easier to change. Abstract classes and interfaces in languages like Java and C# formalize this concept by defining contracts that implementing classes must fulfill.

## Related

- [[Class]] - The blueprint template for creating objects in OOP
- [[Object]] - An instance of a class that encapsulates state and behavior
- [[Inheritance]] - The OOP mechanism for acquiring properties from parent classes
- [[Encapsulation]] - Bundling data and methods while restricting internal access
- [[Polymorphism]] - The ability of objects to take on many forms through common interfaces
- [[Abstraction]] - Hiding complex implementation details behind simplified interfaces
- [[Design Patterns]] - Reusable solutions to common OOP design problems
- [[SOLID Principles]] - Five design principles for writing maintainable OOP code
- [[Method]] - A function defined within a class that operates on objects
- [[Constructor]] - A special method used to initialize new objects
