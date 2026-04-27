---
title: "Flux Architecture"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [javascript, react, state-management, frontend,单向数据流]
---

# Flux Architecture

## Overview

Flux is an application architecture pattern developed by Facebook for building client-side web applications, particularly those with complex state that changes over time. Introduced alongside React in 2014, Flux addresses the problem of maintaining predictable state in applications with many interconnected View components. The core insight is that data should flow in a single direction: from Actions through a Dispatcher to Stores, which then notify Views of updates. This unidirectional data flow makes state changes explicit and applications easier to reason about.

Flux is not a framework itself but an architectural pattern with several concrete implementations including the original Facebook dispatcher, Redux (the most widely adopted), and MobX. The pattern emerged from Facebook's struggle with complex MVC applications where bidirectional data binding made it difficult to trace where changes originated and debug state inconsistencies. Flux enforces a strict data flow that makes applications more debuggable and maintainable at the cost of some boilerplate.

## Key Concepts

**Actions**: Actions are payloads of data that describe what happened in the application. They are simple objects with a `type` field identifying the action and a `payload` containing relevant data. Actions are created by action creators—functions that package user interactions or API responses into a standardized format before dispatching.

**Dispatcher**: The dispatcher is the central hub that routes actions to stores. It is essentially a pub/sub system with one important constraint: all callbacks registered by stores are executed synchronously in the order they were registered. The dispatcher guarantees that stores process actions in a predictable sequence.

**Stores**: Stores contain application state and business logic specific to a domain. Unlike models in MVC, stores manage data for an entire portion of the application, not just single records. Stores register callbacks with the dispatcher and update their internal state when relevant actions are dispatched. When state changes, stores emit change events.

**Views**: Views are React components that subscribe to stores and re-render when the stores they depend on change. Views are the presentation layer that displays data from stores and dispatches actions in response to user interactions.

## How It Works

The Flux data flow follows a strict sequence:

1. User interacts with a View (clicks a button)
2. View calls an Action Creator function
3. Action Creator creates an Action object
4. Action is dispatched to all registered callbacks
5. Stores receive the action and update their state
6. Stores emit a change event
7. Views receive the change event and re-render with new state

```javascript
// Dispatcher setup
import { Dispatcher } from 'flux';

const dispatcher = new Dispatcher();

// Action Creator
const TodoActions = {
  addTodo(text) {
    dispatcher.dispatch({
      type: 'TODO_ADD',
      payload: { text, id: Date.now() }
    });
  },
  
  deleteTodo(id) {
    dispatcher.dispatch({
      type: 'TODO_DELETE',
      payload: { id }
    });
  }
};

// Store
class TodoStore {
  constructor() {
    this.todos = [];
    
    dispatcher.register(action => {
      switch (action.type) {
        case 'TODO_ADD':
          this.todos.push(action.payload);
          this.emitChange();
          break;
        case 'TODO_DELETE':
          this.todos = this.todos.filter(t => t.id !== action.payload.id);
          this.emitChange();
          break;
      }
    });
  }
  
  getAll() {
    return [...this.todos];
  }
}

// View (React component)
import React from 'react';

function TodoView() {
  const [todos, setTodos] = React.useState([]);
  
  React.useEffect(() => {
    const callback = () => setTodos(todoStore.getAll());
    todoStore.addListener(callback);
    return () => todoStore.removeListener(callback);
  }, []);
  
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

## Practical Applications

Flux architecture is particularly valuable for applications with complex client-side state—dashboards with real-time data updates, collaborative editing tools, notification systems, and e-commerce shopping carts. It scales well because adding new features typically means adding new actions and expanding stores rather than modifying existing code paths. The explicit nature of Flux makes it easier to implement features like undo/redo, time-travel debugging, and state persistence.

The pattern pairs naturally with [[React Components]] and [[Single Page Applications]], providing a state management solution that scales better than local component state or bidirectional data binding approaches.

## Examples

A practical todo application using Flux:

```javascript
// Complete Flux implementation with async handling
const AppDispatcher = new Dispatcher();

// Payload for async actions
class TodoAsyncActions {
  static loadTodos() {
    AppDispatcher.dispatch({ type: 'LOAD_TODOS_START' });
    
    fetch('/api/todos')
      .then(response => response.json())
      .then(todos => {
        AppDispatcher.dispatch({
          type: 'LOAD_TODOS_SUCCESS',
          payload: { todos }
        });
      })
      .catch(error => {
        AppDispatcher.dispatch({
          type: 'LOAD_TODOS_ERROR',
          payload: { error }
        });
      });
  }
}
```

## Related Concepts

- [[Redux]] - The most popular Flux implementation with a single store
- [[React State Management]] - Managing state in React applications
- [[单向数据流]] - The fundamental principle underlying Flux
- [[Event-Driven Architecture]] - Similar pub/sub patterns in backend systems
- [[React Components]] - Views in the Flux pattern
- [[Immutability]] - How Flux stores typically manage state updates

## Further Reading

- Facebook's original Flux documentation and todo tutorial
- "Getting Started with Redux" by Dan Abramov - Comprehensive Flux-inspired state management
- "The Evolution of Flux Frameworks" - Article comparing Redux, MobX, and other implementations

## Personal Notes

I first encountered Flux through Redux and appreciated its strictness after working on a project with complex MVC where state changes were difficult to trace. Redux's single store and pure reducers make testing straightforward—actions and reducers are pure functions. The boilerplate was initially off-putting, but tools like Redux Toolkit have significantly reduced ceremony. For smaller projects, I often reach for React's built-in Context and useReducer before adding Redux, since the overhead isn't always justified. But for applications where state is complex and debugging matters, Flux and its descendants remain excellent choices.
