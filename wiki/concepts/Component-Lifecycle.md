---
title: "Component Lifecycle"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [component-lifecycle, react, frontend, web-development, hooks]
---

# Component Lifecycle

## Overview

Component lifecycle refers to the sequence of stages a UI component goes through from its creation to its destruction. In [[React]] and similar component-based frameworks, understanding lifecycle is essential for managing side effects, optimizing performance, and ensuring proper resource cleanup. Components are born (mounted), grow (update with new props or state), and eventually die (unmounted)—and developers need hooks to intervene at each stage.

The lifecycle is most commonly discussed in React, which has class components with explicit lifecycle methods and functional components using the [[Hooks API]]. While class component lifecycle methods (componentDidMount, componentDidUpdate, componentWillUnmount) are well-defined, the hooks model (useEffect) provides a more flexible and composable approach. Other frameworks like [[Vue]], [[Angular]], and [[Svelte]] have their own lifecycle models, but the concepts translate.

The lifecycle matters because real applications need to perform side effects: fetching data from APIs, setting up subscriptions, manipulating the DOM directly, starting timers, or integrating with third-party libraries. All of these must be set up during lifecycle phases and properly cleaned up when the component is destroyed, or they cause memory leaks and stale behavior.

## Mounting Phase

The mounting phase begins when a component is first created and inserted into the DOM. This is where initialization happens.

**Class Components**: The constructor runs first, initializing state and binding event handlers. Then render() produces the initial HTML-like output. Finally, componentDidMount() runs—this is where side effects like DOM manipulation, data fetching, and subscriptions should be initiated.

**Functional Components with Hooks**: The function body runs first, setting up state with useState and other hooks. Then useEffect with no dependency array (or an empty array) runs after render, serving the same purpose as componentDidMount:

```jsx
import React, { useState, useEffect } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // componentDidMount equivalent
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      });

    // Optional: return cleanup function for componentWillUnmount
    return () => {
      console.log('Component unmounting, cleanup needed');
    };
  }, [userId]); // Re-run only if userId changes

  if (loading) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

## Update Phase

Components update when their props or state change. In React, this triggers a re-render with new data.

**Class Components**: When state changes via setState() or new props arrive, render() runs again. After the DOM updates, componentDidUpdate() fires, receiving the previous props and state as parameters. This is where you might make DOM measurements, fetch new data based on prop changes, or call forceUpdate() for manual re-renders.

**Functional Components**: State updates via the setter from useState trigger a re-render. useEffect with dependencies runs when those dependencies change:

```jsx
function SearchResults({ query }) {
  const [results, setResults] = useState([]);

  // Runs when 'query' changes (componentDidUpdate for query changes)
  useEffect(() => {
    if (query) {
      searchAPI(query).then(data => setResults(data));
    }
  }, [query]);

  // Runs after every render (like componentDidUpdate with no guards)
  useEffect(() => {
    console.log('Component re-rendered');
  });

  return <ul>{results.map(r => <li key={r.id}>{r.title}</li>)}</ul>;
}
```

## Unmounting Phase

Unmounting occurs when a component is removed from the DOM—navigating away, conditional rendering, or a parent removing the component.

**Class Components**: componentWillUnmount() is the designated cleanup method. This is where you cancel network requests, remove event listeners, invalidate timers, and unsubscribe from stores or services. Failure to clean up properly causes memory leaks, stale closures, and unexpected behavior after the component is gone.

**Functional Components**: Cleanup happens in the function returned by useEffect:

```jsx
function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.connect();

    // This returned function is componentWillUnmount
    return () => {
      connection.disconnect();
    };
  }, [roomId]);

  return <div>Chat Room: {roomId}</div>;
}
```

## Error Handling

React 16 introduced error boundaries—special components that catch JavaScript errors anywhere in their child tree, log them, and display a fallback UI. Class components implement getDerivedStateFromError() or componentDidCatch() to define error boundary behavior:

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}
```

## Practical Applications

**Data Fetching** is the most common use of lifecycle. Fetch data in useEffect with proper dependency arrays, cancel requests with AbortController, and handle loading and error states.

**Subscriptions** to WebSocket connections, Redux stores, or EventEmitter-style systems must be set up and torn down properly. The cleanup function should match the setup.

**Timer Management** with setInterval and setTimeout requires cleanup. For intervals, always clear them in the cleanup function. For timeouts, track the ID and clear if the component unmounts before it fires.

**DOM Manipulation** via refs (useRef in functional components) often needs to happen after mount. Reading measurements, focusing inputs, or integrating with third-party libraries that manipulate the DOM should happen in the effect after initial render.

## Related Concepts

- [[React]] — The framework where lifecycle is most commonly discussed
- [[Hooks API]] — Modern way to manage lifecycle in functional components
- [[Component-Based Architecture]] — The paradigm that necessitates lifecycle management
- [[Side Effects]] — Operations that happen outside the render cycle
- [[useEffect]] — The primary hook for lifecycle operations in modern React

## Further Reading

- [React Docs: Lifecycle of Components](https://react.dev/learn/lifecycle-of-reactive-effects) — Official React documentation on effect lifecycle
- [A Complete Guide to useEffect](https://overreacted.io/a-complete-guide-to-useeffect/) — Dan Abramov's deep dive into the mental model

## Personal Notes

The biggest shift in thinking about lifecycle came with hooks: instead of thinking about lifecycle stages, think about synchronization with external systems. The question isn't "when does this run?" but "what external system am I synchronized with?" This reframing makes dependencies obvious and cleanup intuitive. When you find yourself fighting the dependency array in useEffect, it's usually because the mental model is off—you're likely either synchronizing with something you shouldn't be, or trying to express multiple unrelated synchronizations that should be separate useEffect calls.
