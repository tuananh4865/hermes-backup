---
title: "Props"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [react, components, props, javascript, front-end]
---

# Props

Props (short for "properties") are React's primary mechanism for passing data from parent components to child components, enabling the composition of reusable, declarative UI components. Props flow downward in the component tree, making React's data flow unidirectional.

## Overview

In React's component model, props are the means by which parent components communicate with children. When you render a component, you can pass any JavaScript value as a prop—strings, numbers, booleans, arrays, objects, functions, or even other React elements. The child component receives these props as a single object argument to its function (or as `this.props` in class components).

Props are read-only—components must never modify their own props. This constraint is fundamental to React's architecture: it ensures that data flows predictably through the application, making debugging easier and enabling deterministic rendering behavior.

The immutability of props encourages a programming style where components are pure functions of their inputs. Given the same props, a component always renders the same output. State (via [[React Hooks]]) handles data that changes over time within a component.

Props also serve as the API surface for reusable components. Well-designed props enable library-style components (like UI component libraries) to be flexible enough for many use cases while remaining simple to use for common cases.

## Key Concepts

**Unidirectional Data Flow**: Data in React flows down the component tree via props. A parent component passes props to children; children cannot directly modify props but can communicate back via callbacks passed as props.

**Prop Drilling**: The pattern of passing props through multiple levels of components, even when intermediate components don't need the data. This can become cumbersome and is addressed by Context or state management solutions.

**PropTypes/TypeScript**: As applications grow, runtime PropTypes (deprecated in recent React) gave way to static type systems like TypeScript, which provide compile-time checking of prop types.

**Default Props**: Values assigned to props when no value is provided, ensuring components have sensible defaults.

**Children Props**: A special prop (`children`) that contains whatever is passed between a component's opening and closing tags, enabling composition patterns.

**Spread Props**: Using `{...props}` to pass an entire object of props to a child component, useful for forwarding props through wrapper components.

## How It Works

Props in React function components:

1. **Passing Props**: When rendering a component, attributes become props. `<UserCard name="Alice" age={30} />` passes `name` and `age` to the component.

2. **Receiving Props**: The component function receives a single `props` object argument containing all passed values.

3. **Using Props**: Components access props by name: `props.name` or destructured: `const { name, age } = props`.

4. **Prop Validation**: Props can be validated with TypeScript types (recommended) or PropTypes for runtime validation in development.

5. **Re-rendering**: When a parent's state changes, it re-renders and passes new props to children. Children re-render when their props change.

```jsx
// Passing props to a component
function App() {
    const user = { name: 'Alice', role: 'admin' };
    return <UserCard name={user.name} role={user.role} />;
}

// Receiving and using props
function UserCard({ name, role }) {
    return (
        <div className="user-card">
            <h2>{name}</h2>
            <span className="badge">{role}</span>
        </div>
    );
}

// Children prop for composition
function Card({ title, children }) {
    return (
        <div className="card">
            <h3 className="card-title">{title}</h3>
            <div className="card-content">{children}</div>
        </div>
    );
}

// Usage with children
function App() {
    return (
        <Card title="Welcome">
            <p>This content becomes the children prop!</p>
            <button>Click me</button>
        </Card>
    );
}

// Prop spreading for forwarding
function Button({ variant, ...restProps }) {
    // restProps contains everything except variant
    return <button className={`btn btn-${variant}`} {...restProps} />;
}
```

## Practical Applications

- **Component Libraries**: Building reusable UI components (buttons, modals, forms) that accept props for customization (colors, sizes, handlers).

- **Configuration Components**: Components that receive rendering configuration as props, enabling complex composition without inheritance.

- **Render Props Pattern**: A technique where a prop is a function that returns React elements, enabling code sharing between components.

- **Higher-Order Components (HOCs)**: Functions that take a component and return a new component with enhanced props.

- **Portals**: Using props to pass content outside the normal DOM hierarchy while maintaining React's component model.

## Examples

**Destructuring Props**:
```jsx
// Without destructuring
function UserProfile(props) {
    return (
        <div>
            <h1>{props.name}</h1>
            <p>{props.bio}</p>
            <img src={props.avatarUrl} alt={props.name} />
        </div>
    );
}

// With destructuring (recommended)
function UserProfile({ name, bio, avatarUrl }) {
    return (
        <div>
            <h1>{name}</h1>
            <p>{bio}</p>
            <img src={avatarUrl} alt={name} />
        </div>
    );
}

// With default values
function Button({ label = 'Submit', onClick, variant = 'primary' }) {
    return (
        <button className={`btn btn-${variant}`} onClick={onClick}>
            {label}
        </button>
    );
}
```

**TypeScript Props**:
```tsx
interface CardProps {
    title: string;
    description?: string;  // Optional prop
    onClick: () => void;
    tags: string[];
}

function Card({ title, description, onClick, tags }: CardProps) {
    return (
        <div onClick={onClick}>
            <h2>{title}</h2>
            {description && <p>{description}</p>}
            <div className="tags">
                {tags.map(tag => <span key={tag}>{tag}</span>)}
            </div>
        </div>
    );
}
```

## Related Concepts

- [[React Components]] — The building blocks of React UIs
- [[React Hooks]] — Functions for managing state and side effects
- [[State Management]] — Patterns for managing application state
- [[Context API]] — React's built-in solution for prop drilling
- [[JSX]] — The syntax extension for writing React elements
- [[Component Composition]] — Patterns for combining components

## Further Reading

- [React Docs: Components and Props](https://react.dev/learn/passing-props-to-a-component) — Official documentation
- [Thinking in React](https://react.dev/learn/thinking-in-react) — Mental model for React development
- [PropTypes Reference](https://react.dev/reference/react/PropTypes) — Legacy prop validation

## Personal Notes

Props are deceptively simple—most developers understand them quickly but miss the depth of what composition enables. The children prop is underutilized; thinking of components as "holes" to fill rather than rigid templates opens up powerful composition patterns. I also find TypeScript with React eliminates an entire category of bugs that runtime PropTypes would have caught, and the IDE support for prop autocompletion is invaluable on large codebases.
