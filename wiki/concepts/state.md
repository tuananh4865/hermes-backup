---
title: State
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [state, state-management, react, frontend]
---

## Overview

State refers to the data an application maintains at a given point in time, ranging from simple UI flags like modal visibility to complex structures like user transaction lists. Managing state effectively is critical for building responsive, predictable, and maintainable applications.

Applications typically have multiple sources of state that must be kept in sync. Changes in one area can ripple across the system, so developers need clear patterns for reading, updating, and distributing state data. Without proper state management, applications become difficult to debug and prone to UI inconsistencies.

## Types of State

### Client State vs Server State

**Client state** resides entirely in the browser or application client. It includes UI state (such as form inputs, active tabs, or hover states), session data, and cached information that does not need to be persisted to a backend. Client state is ephemeral by nature and is lost when the user refreshes or closes the application.

Server state lives on the backend and is fetched via API calls, including user data, product catalogs, and transaction records. It introduces challenges like network latency, caching, synchronization, and handling stale or conflicting data.

The distinction matters because server state and client state require different approaches. Server state often involves asynchronous operations and must account for race conditions, while client state typically needs immediate, synchronous updates for UI responsiveness.

Other common categories include navigation state (current path, history), form state (inputs, validation), and session state (temporary user data).

## Management Patterns

### Redux

Redux is a predictable state container for JavaScript applications, commonly used with React. It enforces a unidirectional data flow where state changes are dispatched as actions and processed by pure functions called reducers. Redux centralizes state in a single store, making it easier to track changes and debug applications using time-travel debugging. However, Redux requires boilerplate code and is often considered overkill for smaller applications.

### Zustand

Zustand offers a minimalist alternative to Redux. It creates a global store using a simple hook-based API without requiring actions or reducers. State updates work through direct mutations or setter functions, and middleware is available for side effects like logging or persistence. Its lightweight footprint and straightforward API make it popular for projects wanting global state without Redux's complexity.

### Jotai

Jotai takes an atomic approach to state management. Instead of a single global store, state is broken into small units called atoms. Components subscribe only to the atoms they need, and dependent atoms automatically recalculate when their dependencies change. This model excels at granular reactivity and reduces unnecessary re-renders.

## Related

- [[React]] — Popular UI library paired with various state management solutions
- [[Component Lifecycle]] — Component mount, update, and unmount phases tied to state management
- [[API Design]] — Backend design affects how server state is fetched and cached
- [[Caching]] — Essential for managing server state and reducing API calls
- [[Local Storage]] — Browser storage for persisting client-side state
