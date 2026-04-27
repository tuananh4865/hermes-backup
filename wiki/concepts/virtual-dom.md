---
title: Virtual DOM
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [virtual-dom, react, performance, dom, frontend]
---

# Virtual DOM

The Virtual DOM (VDOM) is a lightweight JavaScript in-memory representation of the actual DOM (Document Object Model). React popularized this technique to minimize expensive direct DOM manipulations by batching updates and calculating minimal DOM changes before applying them.

## Overview

Direct DOM operations are slow because the browser's DOM is a tree structure where any change can trigger reflows, repaints, and cascading style recalculations. The Virtual DOM addresses this by maintaining a JavaScript representation of what the UI should look like, then efficiently computing and applying only the necessary changes to the real DOM.

When state changes occur, React:
1. Creates a new Virtual DOM tree reflecting the updated state
2. Compares it with the previous Virtual DOM (reconciliation/diffing)
3. Calculates the minimal set of changes needed
4. Batch-applies only those changes to the real DOM

This diffing algorithm makes UI updates dramatically faster than manipulating the DOM directly on every change.

## Key Concepts

### Reconciliation

Reconciliation is the process React uses to determine which parts of the tree changed:
- React assumes (incorrectly, in practice) that two trees with different root elements are completely different
- Elements of different types produce different trees
- The algorithm compares children of the same type recursively

```javascript
// Simplified reconciliation logic
function reconcile(oldElement, newElement) {
    if (oldElement.type !== newElement.type) {
        // Different types = replace entire subtree
        return newElement;
    }
    
    if (typeof newElement.type === 'string') {
        // DOM element - update attributes
        updateDOMProperties(oldElement.props, newElement.props);
        return newElement;
    }
    
    // Component - instance may stay, props update
    return reconcileChildren(oldElement, newElement);
}
```

### Fiber Architecture

React Fiber (React 16+) refactored the reconciliation algorithm into a fiber tree:
- Each React element has a corresponding fiber node
- Fibers form a linked list enabling incremental rendering
- Work can be paused, aborted, or prioritized
- Enables concurrent features like Suspense

### Keys

Keys help React identify which elements have changed:
```jsx
// Without keys - may cause unnecessary re-renders
{myList.map(item => <Item name={item.name} />)}

// With keys - React knows exactly which item changed
{myList.map(item => <Item key={item.id} name={item.name} />)}
```

## How It Works

1. **Render Phase**: Component functions execute, producing React elements
2. **Virtual DOM Creation**: React elements form a tree in memory
3. **Diffing**: New virtual tree compared with previous version
4. **Work Scheduling**: Minimal set of DOM operations determined
5. **Commit Phase**: Actual DOM changes applied in a single batch
6. **Browser Paint**: Browser renders the updated DOM to screen

## Practical Applications

- **React Applications**: All React UI updates use Virtual DOM
- **React Native**: Uses similar concept for native mobile views
- **Vue.js**: Implements its own reactivity-based virtual DOM
- **Benchmark Tools**: Performance measurement of reconciliation
- **Animation Libraries**: Efficient batch DOM updates for smooth animations

## Examples

### Creating Virtual DOM Elements

```jsx
// JSX compiles to React.createElement calls
const element = (
    <div className="container">
        <h1>Hello, {name}!</h1>
        <button onClick={handleClick}>Click me</button>
    </div>
);

// This compiles to:
const element = React.createElement(
    'div',
    { className: 'container' },
    React.createElement('h1', null, 'Hello, ', name, '!'),
    React.createElement('button', { onClick: handleClick }, 'Click me')
);
```

### Manual Virtual DOM Comparison

```javascript
// Simplified virtual DOM diffing
function diff(oldTree, newTree) {
    const patches = [];
    
    function walk(oldNode, newNode, index = 0) {
        if (!oldNode) {
            patches.push({ type: 'INSERT', node: newNode });
        } else if (!newNode) {
            patches.push({ type: 'REMOVE', index });
        } else if (typeof oldNode !== typeof newNode || oldNode.type !== newNode.type) {
            patches.push({ type: 'REPLACE', node: newNode });
        } else if (oldNode.props !== newNode.props) {
            patches.push({ type: 'PROPS', props: diffProps(oldNode.props, newNode.props) });
        } else {
            // Recurse into children
            oldNode.children?.forEach((child, i) => walk(child, newNode.children[i], i));
        }
    }
    
    walk(oldTree, newTree);
    return patches;
}
```

### Hooks and State Updates

```jsx
import React, { useState, useEffect } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    // Virtual DOM re-renders when state changes
    useEffect(() => {
        document.title = `Count: ${count}`;
        // Side effect runs after commit
    }, [count]);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(c => c + 1)}>
                Increment
            </button>
        </div>
    );
}
```

## Related Concepts

- [[react]] — JavaScript library that popularized Virtual DOM
- [[frontend]] — Frontend development context
- [[performance-optimization]] — Improving UI performance
- [[reconciliation]] — React's diffing algorithm
- [[state-management]] — Managing component state in React

## Further Reading

- React Reconciliation Documentation
- "A Deep Dive into React Fiber" (React Conf talks)
- Lin Clark's "A Cartoon Intro to Fiber" (Mozilla Hacks)
- "Virtual DOM: The Idea" by Vladimir Shapiro

## Personal Notes

The Virtual DOM is often misunderstood as a performance optimization for all cases. For simple apps with infrequent updates, the overhead of the virtual DOM reconciliation actually makes things slower than direct DOM manipulation. The real benefits emerge with complex UIs where many updates happen—React can batch and minimize operations. The idea also influenced other frameworks; Vue adopted a similar approach while Svelte went the opposite direction, compiling away the virtual DOM entirely for potentially better baseline performance. It's worth understanding the tradeoffs rather than assuming "virtual DOM = fast."
