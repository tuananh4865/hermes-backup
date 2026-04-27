---
title: "React"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [react, javascript, frontend, ui-library, component-based, virtual-dom]
---

# React

## Overview

React is a JavaScript library for building user interfaces, developed and maintained by Meta (formerly Facebook). First released in 2013, React has become one of the most widely adopted tools in frontend development. It enables developers to create large web applications that can update data dynamically without requiring full page reloads. The core philosophy behind React centers on building reusable UI components that manage their own state, resulting in code that is more predictable, easier to debug, and simpler to reason about.

React is often described as a framework rather than a library due to its comprehensive ecosystem and the way it shapes modern web development practices. It follows a declarative programming paradigm, where developers describe what the UI should look like for any given application state, and React handles the underlying DOM manipulation automatically. This approach contrasts with imperative programming, where developers would manually specify each step of DOM updates.

The React ecosystem includes powerful companion libraries: [[React Router]] for navigation, [[Redux]] or [[Zustand]] for state management, and [[Next.js]] for server-side rendering and static site generation. This rich ecosystem makes React suitable for everything from small single-page applications to large-scale enterprise systems serving millions of users.

## Key Concepts

### Components

React applications are fundamentally built around the concept of components. A component is a self-contained module that renders some output, typically as a piece of the user interface. Components can be either class-based or functional, with functional components being the modern standard thanks to the introduction of hooks. Components can be composed together to create complex UIs from simple, reusable pieces, promoting code reuse and separation of concerns.

```jsx
// Functional component example
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  if (!user) return <LoadingSpinner />;
  
  return (
    <div className="profile">
      <Avatar src={user.avatarUrl} />
      <h2>{user.name}</h2>
      <p>{user.bio}</p>
    </div>
  );
}
```

### JSX

JSX (JavaScript XML) is a syntax extension that allows developers to write HTML-like code directly within JavaScript. It provides a familiar way to describe the structure of UI components, making code more readable and expressive. JSX is transpiled by tools like Babel into regular JavaScript function calls that create and update DOM elements. While JSX is not required to use React, it is the preferred approach in the React community for defining component structures.

```jsx
// JSX compiles to this JavaScript
const element = <h1 className="greeting">Hello, world!</h1>;

// Becomes
const element = React.createElement(
  'h1',
  { className: 'greeting' },
  'Hello, world!'
);
```

### State Management

State management is a fundamental concept in React applications. Local component state is managed using the `useState` hook, which allows functional components to hold and update data that affects their rendering. For application-wide state that needs to be shared across multiple components, React provides the Context API, which enables efficient data propagation without prop drilling. For more complex state management needs in large-scale applications, libraries like [[Redux]] and Zustand are commonly used, providing predictable state containers with robust developer tools.

```jsx
// Local state with useState
function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### Virtual DOM

React employs a Virtual DOM as an intermediary representation of the actual DOM. When state changes occur in a React application, the framework first updates the Virtual DOM, then efficiently diffs it against the previous version to determine the minimal set of changes needed to update the real DOM. This process, known as reconciliation, significantly improves performance compared to direct DOM manipulation, as React batches updates and applies them optimally.

## How It Works

React's rendering cycle follows a specific pattern:

**1. State Change Trigger**: When application state changes (via `setState`, props updates, or context changes), React marks the relevant component subtree as needing re-rendering.

**2. Virtual DOM Render**: React creates a new Virtual DOM tree representing the current UI state. This is a fast, pure JavaScript operation that doesn't touch the real DOM.

**3. Diffing (Reconciliation)**: React compares the new Virtual DOM with the previous version using a heuristic O(n) algorithm. It identifies the minimal set of DOM operations needed to transform the current DOM to match the new Virtual DOM.

**4. Batch Update**: React batches all the identified DOM changes and applies them in a single, optimized pass. This batching minimizes expensive DOM reflows and repaints.

**5. Commit Phase**: Once all updates are applied, React commits the changes and the component lifecycle continues.

```jsx
// Example: How state flows through components
function App() {
  // App-level state
  const [theme, setTheme] = useState('light');
  
  // Passed down to child components
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <Layout>
        <Header />
        <Content />
        <Footer />
      </Layout>
    </ThemeContext.Provider>
  );
}
```

## Practical Applications

**Single-Page Applications (SPAs)**: React excels at building SPAs where content updates without full page reloads. The [[React Router]] library handles client-side navigation, mapping URLs to components and managing browser history.

**Progressive Web Apps (PWAs)**: React can be combined with service workers to create installable web applications that work offline, similar to native mobile apps.

**Server-Side Rendering (SSR)**: Frameworks like [[Next.js]] render React components on the server for faster initial page loads and better SEO. SSR sends fully-rendered HTML to the client, with hydration attaching React's event handlers afterward.

**Static Site Generation (SSG)**: Next.js also supports static generation at build time, producing pre-rendered HTML files ideal for content-heavy sites like blogs or documentation.

**Mobile Development**: [[React Native]] extends React's paradigm to mobile platforms, sharing significant code between iOS and Android apps while still supporting platform-specific components.

**Desktop Applications**: Electron combined with React enables cross-platform desktop app development, used by tools like VS Code and Slack.

## Examples

Building a todo application demonstrates React's core patterns:

```jsx
import { useState } from 'react';

// Custom hook for todo logic
function useTodos(initialTodos) {
  const [todos, setTodos] = useState(initialTodos);
  
  const addTodo = (text) => {
    setTodos([...todos, { id: Date.now(), text, completed: false }]);
  };
  
  const toggleTodo = (id) => {
    setTodos(todos.map(t => 
      t.id === id ? { ...t, completed: !t.completed } : t
    ));
  };
  
  const deleteTodo = (id) => {
    setTodos(todos.filter(t => t.id !== id));
  };
  
  return { todos, addTodo, toggleTodo, deleteTodo };
}

// TodoList component
function TodoList({ todos, onToggle, onDelete }) {
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => onToggle(todo.id)}
          />
          <span style={{ 
            textDecoration: todo.completed ? 'line-through' : 'none' 
          }}>
            {todo.text}
          </span>
          <button onClick={() => onDelete(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}
```

## Related Concepts

- [[JavaScript]] - The programming language that serves as the foundation for React development
- [[JSX]] - The syntax extension used throughout React applications
- [[Hooks]] - React's mechanism for managing state and side effects in functional components
- [[Virtual DOM]] - React's performance optimization technique for efficient DOM updates
- [[Component-Based Architecture]] - The design pattern that forms the basis of React's approach
- [[Next.js]] - A full-stack framework built on React that supports server-side rendering
- [[React Native]] - A framework for building native mobile applications using React principles
- [[Redux]] - A popular state management library commonly used with React
- [[Vite]] - A modern build tool and development server often used for React projects
- [[TypeScript]] - Strongly-typed superset of JavaScript commonly used with React

## Further Reading

- Official React Documentation — comprehensive guide to React concepts and APIs
- "React: The Definitive Guide" — in-depth coverage of React patterns and best practices
- Thinking in React — official article on how to approach React UI construction
- React Hooks Documentation — detailed reference for all built-in hooks

## Personal Notes

React's component model fundamentally changed how I think about building UIs. The idea that every interactive piece of the page is a self-contained component with its own state and rendering logic makes code dramatically more modular and testable. The learning curve is primarily around understanding when state changes trigger re-renders and how the Virtual DOM diffing algorithm works under the hood. Once those click, React becomes much more intuitive. For large applications, invest early in a good state management pattern—[[Redux]] or Zustand—and establish conventions for component composition early, as the flexibility React offers can lead to inconsistent architecture if not guided.
