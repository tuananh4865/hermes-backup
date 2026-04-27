---
title: "React Context Api"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [react, state-management, context, javascript, frontend, react-hooks]
---

# React Context API

React Context API is a built-in mechanism for sharing data across the component tree without prop drilling—passing props through intermediate components that don't need the data. Introduced in React 16.3, Context provides a way to pass data through the component hierarchy without manually threading props through every level.

## Key Concepts

**Context** — A React object created via `React.createContext()`. It holds a value and provides it to descendant components that opt-in via `useContext` or `Context.Consumer`.

**Provider** — A component that wraps a subtree and provides the context value. Providers can be nested, with inner providers overriding outer ones for specific values.

**Consumer** — A component that subscribes to context changes. In modern React, `useContext` Hook provides a cleaner way to consume context.

**Default Value** — The value used when a consumer is outside a provider tree. Helps with testing and partial context usage.

## How It Works

### Creating Context

```javascript
import { createContext, useContext, useState } from 'react';

// Create context with default value
const ThemeContext = createContext('light');

// Provider component
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Consumer component using Hook
function ThemedButton() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  
  return (
    <button 
      className={theme}
      onClick={toggleTheme}
    >
      Current: {theme}
    </button>
  );
}
```

### Using Multiple Contexts

Applications typically layer multiple contexts for different concerns:

```javascript
// Authentication context
const AuthContext = createContext(null);

// Theme context
const ThemeContext = createContext('light');

// User preferences context
const PreferencesContext = createContext({});

function App() {
  return (
    <AuthContext.Provider value={authState}>
      <ThemeContext.Provider value={themeState}>
        <PreferencesContext.Provider value={prefs}>
          <Dashboard />
        </PreferencesContext.Provider>
      </ThemeContext.Provider>
    </AuthContext.Provider>
  );
}
```

## Practical Applications

**Global State** — User authentication status, theme preferences, language settings—data that affects multiple unrelated components.

**Dependency Injection** — Passing services or utilities (API clients, logging) through the component tree without explicit prop passing.

**Prop Drilling Alternative** — When data needs to reach deeply nested components and intermediate components don't need the data, Context avoids passing it through unrelated layers.

## When to Use Context

Context is appropriate when:
- Data changes infrequently (theme, locale, auth)
- Data spans many components at different nesting levels
- Data isn't held in a global store like [[Redux]]

Context is NOT ideal for:
- Frequently changing data (risks excessive re-renders)
- Data only needed by 2-3 components (use props instead)
- Complex state logic (use [[state-management]] libraries)

## Performance Considerations

Each `useContext` call subscribes to context changes, potentially triggering re-renders in all consumers when context value changes. Optimization strategies:

```javascript
// Memoize context value to prevent unnecessary renders
const memoizedValue = useMemo(() => ({
  theme, 
  toggleTheme
}), [theme, toggleTheme]);

return (
  <ThemeContext.Provider value={memoizedValue}>
    {children}
  </ThemeContext.Provider>
);
```

## Related Concepts

- [[React Hooks]] — Modern hooks like useContext, useState, useReducer
- [[State Management]] — Approaches for managing application state
- [[Redux]] — External state management library
- [[Component Lifecycle]] — Understanding React component phases

## Further Reading

- React Documentation: Context
- Kent C. Dodds: How to use React Context effectively

## Personal Notes

Context clicked for me when I stopped thinking of it as "global state" and more as "dependency injection for React." It shines for truly global concerns like theme and auth, but I've learned to be cautious about stuffing too much state into it—the re-render cascade can be subtle and confusing.
