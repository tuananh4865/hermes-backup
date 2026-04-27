---
title: Redux
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [redux, state-management, javascript, react]
---

# Redux

## Overview

Redux is a predictable state container for JavaScript applications, most commonly paired with [[React]] to manage application state in a centralized and deterministic manner. Created by Dan Abramov and Andrew Clark in 2015, Redux was inspired by the Flux architecture and functional programming principles, particularly the Elm language. Its core philosophy is that state changes should always be traceable, testable, and predictable—every mutation flows through a single pipeline that explicitly describes what happened.

Redux centralizes all application state into a single immutable object tree called the store. This eliminates the problem of scattered, hard-to-track state that plagues many frontend applications. Because every state change is expressed as an explicit action dispatched through a pure reducer function, developers can implement powerful features like time-travel debugging, undo/redo, and persistent state replay. Redux works with any JavaScript framework, though it pairs most naturally with React due to shared functional programming values and unidirectional data flow.

## Key Concepts

### The Store

The store is the heart of Redux—a single, immutable object tree holding your entire application state. You create it with `createStore` (or `configureStore` from Redux Toolkit), passing in your root reducer. The store exposes three essential methods:

```javascript
import { configureStore } from '@reduxjs/toolkit';
import usersReducer from './usersSlice';
import postsReducer from './postsSlice';

const store = configureStore({
  reducer: {
    users: usersReducer,
    posts: postsReducer,
  },
});

console.log(store.getState());
// { users: { list: [], loading: false }, posts: { items: [], error: null } }

store.dispatch({ type: 'users/addUser', payload: { id: 1, name: 'Alice' } });
store.subscribe(() => console.log(store.getState()));
```

### Actions and Action Creators

Actions are plain JavaScript objects describing what happened—the only trigger for state changes. They must have a `type` string and may carry a `payload`. Action creators are functions that return actions, making them reusable and testable.

```javascript
// Action creator pattern
const addTodo = (text) => ({
  type: 'todos/addTodo',
  payload: { id: Date.now(), text, completed: false },
});

store.dispatch(addTodo('Learn Redux'));
```

### Reducers

Reducers are pure functions `(state, action) => newState` that specify how state changes in response to an action. The name comes from `Array.prototype.reduce`—reducers take a cumulative value and fold in new values. Crucially, reducers must never mutate the existing state; they produce a new state object when changes occur.

```javascript
const initialState = { items: [], loading: false };

function todosReducer(state = initialState, action) {
  switch (action.type) {
    case 'todos/addTodo':
      return {
        ...state,
        items: [...state.items, action.payload],
      };
    case 'todos/toggleTodo':
      return {
        ...state,
        items: state.items.map((todo) =>
          todo.id === action.payload
            ? { ...todo, completed: !todo.completed }
            : todo
        ),
      };
    default:
      return state;
  }
}
```

## How Redux Toolkit Simplifies Things

Redux Toolkit (RTK) is the official recommended approach for writing Redux logic. It includes utilities that drastically reduce boilerplate:

- `createSlice`: Generates action creators and reducers together from a single configuration object
- `configureStore`: Sets up the store with good default middleware (including Redux Thunk)
- `createAsyncThunk`: Handles async logic (data fetching) with automatic action dispatching

```javascript
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUsers = createAsyncThunk('users/fetchAll', async () => {
  const response = await fetch('/api/users');
  return response.json();
});

const usersSlice = createSlice({
  name: 'users',
  initialState: { entities: [], loading: 'idle' },
  reducers: {
    addUser: (state, action) => {
      state.entities.push(action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = 'pending';
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.entities = action.payload;
        state.loading = 'succeeded';
      });
  },
});

export const { addUser } = usersSlice.actions;
export default usersSlice.reducer;
```

## Practical Applications

**Global UI State**: User authentication status, theme preferences, sidebar open/closed state—anything accessed by multiple unrelated components.

**Server-Side Data Cache**: Redux can store API responses, preventing redundant network requests and providing a single source of truth for fetched data.

**Complex Form State**: Forms with multi-step wizards or validation across many fields benefit from Redux's predictable state model.

**Undo/Redo**: Because every state change is explicit and immutable, implementing time-travel debugging and undo/redo is straightforward.

## Examples

```jsx
import React from 'react';
import { Provider, useSelector, useDispatch } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

const store = configureStore({ reducer: { counter: counterReducer } });

function Counter() {
  const count = useSelector((state) => state.counter.count);
  const dispatch = useDispatch();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch({ type: 'counter/increment' })}>
        Increment
      </button>
    </div>
  );
}

export default function App() {
  return (
    <Provider store={store}>
      <Counter />
    </Provider>
  );
}
```

## Related Concepts

- [[React]] — The most common library paired with Redux for building user interfaces
- [[MobX]] — An alternative state management library with reactive, object-oriented approach
- [[State Management]] — The broader concept of managing application data and UI state
- [[JavaScript]] — The programming language Redux is implemented in
- [[React Context API]] — Built-in React mechanism for sharing data, often compared to Redux
- [[Redux Toolkit]] — The official Redux utility library that simplifies store setup and reduces boilerplate

## Further Reading

- [Redux Documentation](https://redux.js.org/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
- [Dan Abramov's original talk introducing Redux](https://youtube.com/watch?v=xsSnOQynTHs)
- [Idiomatic Redux course by Dan Abramov](https://egghead.io/courses/fundamentals-of-redux)

## Personal Notes

Redux's ceremony (actions, reducers, store setup) can feel like overkill for small projects. For those cases, React's `useState` or Context API often suffices. But once an application reaches a certain complexity—with many components needing to share and mutate shared state, with async operations, with the need to debug or test state changes—Redux's explicit data flow becomes a massive asset rather than a burden. Redux Toolkit has also come a long way in reducing the boilerplate that made early Redux infamous.
