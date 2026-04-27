---
title: MobX
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [mobx, state-management, reactive, javascript]
---

# MobX

## Overview

MobX is a popular [[reactive programming]] library for JavaScript and TypeScript that provides transparent [[state management]] for applications. Unlike traditional state management approaches that require explicit updates and subscriptions, MobX enables developers to create scalable applications by automatically tracking dependencies and updating only the parts of the UI that need to react to state changes. It follows the principle of "what you write is what you get" — meaning you write code that modifies state, and MobX handles the propagation of those changes throughout your application automatically.

Originally created by Michel Weststrate in 2015, MobX has gained significant traction in the [[JavaScript]] ecosystem, particularly within the [[React]] community. It draws inspiration from the [[observable pattern]] and builds upon ideas from the [[MVVM]] architectural pattern. MobX is often described as "scalable" because it handles everything from small interactive components to large enterprise applications with the same intuitive API. The library is framework-agnostic, meaning it works with React, Vue, Angular, or even vanilla JavaScript, though it is most commonly associated with React through the `mobx-react-lite` bindings package.

## Core Concepts

MobX is built around three fundamental pillars that work together to create reactive state management: observables, actions, and computed values.

**Observables** represent the reactive state in your application. Any piece of data that can change over time should be marked as an observable. MobX can observe primitive values, objects, arrays, and even class instances. When you define a property as observable, MobX wraps it with tracking logic that automatically records which parts of your code depend on that data. You can define observables using the `@observable` decorator in ES7+ environments or the `observable()` function in plain JavaScript or TypeScript. For example, a simple observable store might contain an observable `count` property that tracks how many times a button has been clicked.

**Actions** are functions that modify observable state. They represent the only places where state mutations should occur in MobX applications. By convention and for optimal performance, all state modifications should go through actions because MobX can optimize around them — for instance, batching multiple synchronous state changes into a single notification cycle. Actions can be defined using the `@action` decorator or the `action()` function. MobX also supports asynchronous actions for handling async operations, and there are specific patterns for ensuring proper tracking during async workflows.

**Computed values** (also called derivations) are values that are automatically derived from your observable state. They are functions that observe observables and return a value based on the current state. MobX only recomputes computed values when the observables they depend on have changed, and it caches the result until those dependencies change again. This makes computed values extremely efficient because they do no unnecessary work. For example, if you have an observable `firstName` and `lastName`, you could create a computed `fullName` that automatically updates whenever either of those values changes.

## Comparison

MobX and [[Redux]] are both state management solutions for JavaScript applications, but they take fundamentally different approaches to solving the same problem.

Redux follows a strict unidirectional data flow pattern with a single immutable state tree. All state changes are dispatched through actions and processed by pure functions called reducers. The immutability of state is enforced, meaning you never modify state directly — you always create new copies with the changes applied. Redux also requires additional packages like `redux-thunk` or `redux-saga` for handling asynchronous operations. This architecture provides strong predictability and makes debugging easier through features like time-travel debugging, but it requires more boilerplate code and a specific mindset to work effectively.

MobX takes a more pragmatic and flexible approach. State is stored in observable objects or classes, and you modify it directly through actions. MobX handles change detection automatically through its dependency tracking system, eliminating the need for manual selectors or subscription management. This results in significantly less boilerplate code compared to Redux. MobX also handles asynchronous operations natively without additional middleware. However, this flexibility comes with less enforcement — since state can be modified from anywhere, it requires discipline to maintain a clean architecture.

The choice between MobX and Redux often comes down to team preferences and project requirements. Redux's strict patterns make it easier to onboard new team members and maintain consistency across large teams, while MobX's developer experience is often preferred for rapid development and smaller to medium-sized applications where the overhead of Redux's ceremony is not justified.

## Related

- [[reactive-programming]] - The programming paradigm that MobX implements
- [[Redux]] - Alternative state management library for JavaScript applications
- [[JavaScript]] - The primary language MobX targets
- [[React]] - The most common UI framework used with MobX
- [[State Management]] - The broader discipline of managing application state
- [[observable-pattern]] - The design pattern that underpins MobX's reactivity system
- [[MVVM]] - Architectural pattern that influenced MobX's design
