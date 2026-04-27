---
title: "Global State"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [global-state, state-management, react, redux, javascript]
---

# Global State

## Overview

Global state refers to application data that is accessible from anywhere in the component tree, rather than being confined to a single component or passed explicitly through props. In component-based architectures, prop drilling—passing data through multiple layers of components that don't directly need it—becomes unwieldy. Global state solutions solve this by providing a centralized store that any component can read from or write to, decoupling data logic from component hierarchy.

Global state becomes necessary when multiple unrelated components need to share the same data. Consider a user's authentication status: the navbar needs to show the user's avatar, the sidebar needs to display the user's permissions, and the main content area needs to know whether to show a login form or the protected content. Passing auth state through props from a root component to all these destinations is tedious and creates fragile code. A global auth store solves this elegantly.

The distinction between global state and [[Local State]] is not about the technology but about scope. Local state lives in a single component (managed with useState in [[React]]). Global state lives in a store accessible throughout the application. The same principles apply to [[Vue]] (Pinia/Vuex), [[Angular]] (NgRx/services), and [[Svelte]] (stores). Global state is particularly relevant in [[Single Page Application]] architectures where client-side state persists across route changes.

## Key Concepts

**Single Source of Truth** is a fundamental principle. When auth status lives in a global store, every component that needs it reads from the same place. When the user logs out, all components reflecting auth state update simultaneously. This prevents the classic bug where different parts of the UI show contradictory information because they're reading from duplicated or stale state.

**Unidirectional Data Flow** (associated with [[Flux Architecture]]) is the pattern most global state systems follow. Components don't modify global state directly; they dispatch actions that describe what happened. The store processes the action and emits the new state. Components subscribe to store updates and re-render when state changes. This predictability makes debugging easier.

**Immutability** is typically enforced in global state systems. Rather than mutating state directly (`state.user.name = 'Alice'`), you create new state objects (`{ ...state, user: { ...state.user, name: 'Alice' } }`). Immutability enables powerful features like time-travel debugging (Redux DevTools can "undo" state changes), efficient change detection (shallow equality checks), and easier reasoning about when and how state changes.

**Derived Data** (computed state, selectors) is a common pattern. Rather than storing `fullName` as separate state, derive it from `firstName` and `lastName`. This prevents inconsistencies where `fullName` is updated but the underlying fields aren't. Libraries like [[Redux]] with reselect make this efficient by memoizing selector results.

## How It Works

The most prevalent global state pattern is the [[Redux]] store, which follows the Flux architecture:

```javascript
// Define actions (plain objects describing what happened)
const SET_USER = 'SET_USER';
const LOGOUT = 'LOGOUT';

const setUser = (user) => ({ type: SET_USER, payload: user });
const logout = () => ({ type: LOGOUT });

// Define reducer (pure function: given current state + action, returns new state)
const authReducer = (state = { user: null, isAuthenticated: false }, action) => {
  switch (action.type) {
    case SET_USER:
      return { user: action.payload, isAuthenticated: true };
    case LOGOUT:
      return { user: null, isAuthenticated: false };
    default:
      return state;
  }
};

// Create store (holds state, lets components dispatch actions, notifies subscribers)
import { createStore } from 'redux';
const store = createStore(authReducer);

// Component reads from and writes to the store
function Navbar() {
  const { user, isAuthenticated } = useSelector(state => state.auth);
  const dispatch = useDispatch();

  return (
    <nav>
      {isAuthenticated ? (
        <span>Welcome, {user.name}</span>
      ) : (
        <button onClick={() => dispatch(setUser({ name: 'Alice' }))}>Login</button>
      )}
    </nav>
  );
}
```

**React Context** provides a lighter-weight alternative to Redux for global state that doesn't change frequently:

```javascript
import React, { createContext, useContext, useState } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function ThemedButton() {
  const { theme, setTheme } = useContext(ThemeContext);
  return <button className={theme}>Theme: {theme}</button>;
}
```

## Practical Applications

**User Authentication State** is the most common global state. Whether a user is logged in, their profile data, their permissions, and their authentication tokens—all need to be accessible across the entire application. Storing auth state globally avoids the need to pass auth context through every component.

**Theme and UI Preferences** like dark/light mode, language/locale settings, and sidebar collapsed state are natural fits for global state. Many components may respond to these settings, and they often need to persist to localStorage.

**Shopping Cart** in e-commerce applications must persist across page navigation and be accessible from checkout, product pages, and cart icons in the header. Global state ensures the cart is always consistent regardless of how the user navigates.

**Real-Time Data Feeds** like notifications, live sports scores, or collaborative editing cursors often use global state with subscriptions. Components subscribe to specific slices of global state, and WebSocket or polling updates push changes to the store, which then notifies subscribed components.

**Form Wizard State** that spans multiple pages (like a multi-step checkout or onboarding flow) can use global state to persist data as users navigate between steps. This way, users can go back and forth without losing their entered data.

## Related Concepts

- [[State Management]] — The broader discipline that includes global state
- [[Local State]] — Component-specific state vs. shared state
- [[Redux]] — The most popular global state library for React
- [[Flux Architecture]] — The pattern that influenced Redux
- [[React Context API]] — Built-in mechanism for sharing global data
- [[Single Page Application]] — Architecture where global state is most valuable

## Further Reading

- [Redux Docs](https://redux.js.org/) — Comprehensive Redux documentation
- [React Context Docs](https://react.dev/learn/passing-data-deeply-with-context) — When to use Context vs. Redux
- [You Might Not Need Redux](https://medium.com/@dan_abramov/you-might-not-need-redux-be46359cf36d) — Dan Abramov on when Redux is appropriate

## Personal Notes

I've seen global state become a dumping ground for everything, creating a massive, slow store that's the tightest coupling in the application. The rule I follow: global state is for truly global data (auth, theme, locale) or for state that's genuinely shared across many unrelated components. Everything else should start as local state and only get promoted to global when prop drilling becomes genuinely painful. Overusing global state makes it hard to track where data changes and why—when debugging, you want state to be as local as possible so its data flow is easy to trace.
