---
title: JSX
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [jsx, react, javascript, frontend, web-development, ui]
---

# JSX

## Overview

JSX (JavaScript XML) is a syntax extension for JavaScript that allows developers to write HTML-like code directly within JavaScript, primarily used in React to describe what the user interface should look like. Rather than separating markup and logic into separate files or using a template language, JSX blends them together in a familiar, declarative style that resembles the HTML developers already know. Under the hood, JSX is transformed into standard JavaScript function calls that create and manipulate DOM elements.

JSX was introduced by Facebook (now Meta) alongside React in 2013 as a way to make component code more readable and expressive. Before JSX, React components were constructed using `React.createElement()` calls with verbose JavaScript objects, making complex component trees difficult to read and write. JSX provides a clean, visual syntax that maps closely to the resulting component structure.

Despite looking like HTML, JSX has important differences and rules. Because JSX is JavaScript under the hood, there are restrictions on how certain words can be used (class becomes className, for example). Expressions can be embedded using curly braces, and components are composed by using them like HTML tags. This combination of visual HTML-like syntax with JavaScript's full expressive power is what makes JSX both approachable and capable of handling complex UI logic.

## Key Concepts

**JSX Elements** are the basic units of JSX syntax. They look like HTML tags but are actually JavaScript expressions that evaluate to objects. A JSX element can be a self-closing tag like `<img src="..." />` or an opening/closing tag pair like `<div><h1>Hello</h1></div>`. These elements have attributes and children, just like HTML.

**Expressions and Variables** can be embedded in JSX using curly braces. This allows dynamic values, calculations, and function calls to be inserted into the markup. For example, `<h1>{user.name}</h1>` renders the user's name, and `<p>{2 + 2}</p>` renders 4. Any valid JavaScript expression can appear inside the curly braces.

**Conditional Rendering** in JSX uses standard JavaScript operators. The ternary operator (`condition ? <A /> : <B />`) is common for simple conditionals, while `&&` is used when you want to render something only if a condition is true. For more complex logic, the expression might be moved outside the JSX or a helper function might be used.

**Lists and Keys** are important when rendering collections. Using the `.map()` method, you can transform an array into a list of JSX elements. Each element in a rendered list should have a unique `key` prop to help React identify which items have changed, been added, or removed. Keys should be stable and unique within the list.

**Component Composition** is the practice of building complex UIs from simpler, reusable components. In JSX, this looks exactly like using HTML tags—you can nest any component within another. This pattern encourages separation of concerns and makes it easy to reason about and test individual pieces of the UI.

## How It Works

JSX is not valid JavaScript—browsers cannot execute it directly. Instead, JSX must be transformed (compiled) into standard JavaScript before execution. This transformation is typically performed by build tools like Babel, which converts JSX syntax into `React.createElement()` calls.

```jsx
// JSX syntax
const element = <h1 className="greeting">Hello, world!</h1>;

// After transformation (simplified)
const element = React.createElement(
  'h1',
  { className: 'greeting' },
  'Hello, world!'
);
```

`React.createElement()` returns a plain JavaScript object (called a "React element") that describes what should appear on screen. This object contains information about the element type, its props, and any children. React then uses these objects to build or update the DOM.

Modern frameworks like React have moved beyond requiring explicit `React` imports in many cases, and the transformation handles this automatically. With React 17+, the new JSX transform means you don't need to import React at all for JSX to work—the transform handles the necessary runtime requirements automatically.

JSX can also represent React fragments (`<></>`) which group elements without adding extra DOM nodes. This is useful when you need to return multiple elements from a component but don't want to wrap them in an unnecessary container div.

## Practical Applications

**Component Definition** is the most common use of JSX. Developers write React components as functions that return JSX, making the relationship between component logic and presentation explicit. A button component might receive an `onClick` handler and `label` prop, rendering them directly in JSX.

**Dynamic UIs** leverage JSX's ability to embed expressions. A weather app might take an API response and render it with `<WeatherDisplay temperature={data.temp} condition={data.condition} />`, embedding the data directly in the component tree.

**Form Handling** in React often uses JSX to define both the form structure and connect it to state management. Controlled components bind form inputs to state variables, with JSX binding both the value and change handlers.

**Layouts and Pages** are composed using JSX, with nested components representing headers, sidebars, main content areas, and footers. Component libraries and design systems provide pre-built components that developers compose into full pages using JSX syntax.

```jsx
// Example: A simple React component with JSX
function UserCard({ user, onSelect }) {
  return (
    <div className="user-card" onClick={() => onSelect(user.id)}>
      <img src={user.avatar} alt={user.name} className="avatar" />
      <h2>{user.name}</h2>
      <p className="email">{user.email}</p>
      {user.isAdmin && <span className="badge">Admin</span>}
    </div>
  );
}
```

## Examples

A todo list application might render items using `.map()`:

```jsx
function TodoList({ todos, onToggle }) {
  return (
    <ul className="todo-list">
      {todos.map(todo => (
        <li 
          key={todo.id}
          className={todo.completed ? 'completed' : ''}
          onClick={() => onToggle(todo.id)}
        >
          <input 
            type="checkbox" 
            checked={todo.completed}
            readOnly
          />
          <span>{todo.text}</span>
        </li>
      ))}
    </ul>
  );
}
```

A data dashboard might conditionally render different views based on data availability:

```jsx
function Dashboard({ data, loading, error }) {
  if (loading) return <SkeletonLoader />;
  if (error) return <ErrorMessage message={error} />;
  if (!data) return <EmptyState message="No data available" />;
  
  return (
    <div className="dashboard">
      <StatsGrid metrics={data.metrics} />
      <Chart data={data.chartData} />
    </div>
  );
}
```

## Related Concepts

- [[React]] — The framework JSX was designed for
- [[Props]] — React's mechanism for passing data to components
- [[State]] — React's mechanism for managing component data
- [[Babel]] — The compiler that transforms JSX to JavaScript
- [[Frontend Development]] — The broader discipline JSX is part of
- [[Component-Based Architecture]] — Design pattern enabled by JSX

## Further Reading

- React documentation on JSX
- Babel JSX compiler documentation
- "Learning React" by Alex Banks and Eve Porcello

## Personal Notes

JSX clicked for me when I stopped thinking of it as HTML and started thinking of it as a domain-specific language for describing UI trees. The curly brace embedding takes getting used to, but it's powerful once you realize you can put any expression there. One gotcha: always close tags (including self-closing ones) or you'll get cryptic errors.
