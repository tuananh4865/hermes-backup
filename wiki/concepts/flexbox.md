---
title: "Flexbox"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [css, layout, web-development, frontend, responsive-design]
---

# Flexbox

## Overview

Flexbox (formally the Flexible Box Layout Module) is a two-dimensional [[CSS]] layout system designed to arrange items in a container along a single axis — either horizontal or vertical — with powerful alignment, spacing, and sizing capabilities. Introduced as a W3C standard in 2012 and widely adopted across modern browsers, Flexbox addresses many of the layout challenges that previously required complex floats, positioning hacks, or JavaScript-based solutions.

Unlike earlier layout approaches that relied on document flow and explicit positioning, Flexbox operates on a parent-child relationship: a **flex container** establishes the layout context, and its direct children become **flex items** that follow the container's layout rules. This parent-controlled model makes it intuitive to build complex, aligned interfaces by adjusting just a few container properties, rather than manipulating individual items.

Flexbox excels at one-dimensional layouts — arranging items in a row or a column — and is particularly well-suited for components like navigation bars, card grids, form layouts, and centering content. For full two-dimensional layouts (rows and columns simultaneously), [[CSS Grid]] is often the better tool, though Flexbox and Grid are complementary and frequently used together.

## Key Concepts

**Flex Container**: An element with `display: flex` or `display: inline-flex` becomes a flex container. All direct children automatically become flex items and participate in the flex layout. The container establishes the coordinate system for alignment and distribution.

**Main Axis and Cross Axis**: Every flex container has two axes — the **main axis** (the direction flex items flow) and the **cross axis** (perpendicular to the main axis). `flex-direction` controls which way items flow. If set to `row`, the main axis is horizontal; if `column`, it is vertical.

**Flex Direction**: Controls the direction items flow within the container.

```css
.container { flex-direction: row | row-reverse | column | column-reverse; }
```

**Justify Content**: Distributes items along the **main axis**. This is the primary tool for controlling horizontal spacing in a row layout or vertical spacing in a column layout.

```css
.container { justify-content: flex-start | flex-end | center | space-between | space-around | space-evenly; }
```

**Align Items**: Distributes items along the **cross axis**. This controls vertical alignment in a row layout or horizontal alignment in a column layout.

```css
.container { align-items: stretch | flex-start | flex-end | center | baseline; }
```

**Flex Wrap**: By default, flex items try to fit on one line (`nowrap`). The `wrap` property allows items to flow onto multiple lines when they can't shrink below their minimum content size.

```css
.container { flex-wrap: nowrap | wrap | wrap-reverse; }
```

**Flex Grow and Shrink**: These properties control how flex items expand to fill available space or shrink when space is constrained.

```css
.item {
  flex-grow: 0;   /* Default: don't grow */
  flex-shrink: 1; /* Default: can shrink */
  flex-basis: auto; /* Initial main size */
}
```

## How It Works

When an element is given `display: flex`, its children become flex items that follow the flex formatting context. The browser calculates the flex base size of each item (typically based on `width`/`height` or content size), then applies `flex-grow` and `flex-shrink` factors to determine how items distribute available space.

The `justify-content` property handles the remaining space after flex sizing is resolved. For example, `justify-content: space-between` places the first item at the start, the last item at the end, and distributes remaining space equally between items. This kind of equal-spacing was notoriously difficult to achieve before Flexbox.

For cross-axis alignment, `align-items` defaults to `stretch`, meaning items by default fill the full height of a row layout (or full width of a column layout). This default behavior is what makes it possible to create equal-height columns with just `display: flex` on the container.

The `align-self` property on individual items allows overriding the container's `align-items` setting for specific items, enabling mixed alignment within the same container.

## Practical Applications

**Navigation Bars**: Flexbox is the de facto standard for building horizontal or vertical navigation. `justify-content: space-between` on a nav container places logo items on one end and menu items on the other, regardless of how many items exist.

```css
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

**Centering Content**: The canonical example of Flexbox's power — vertically and horizontally centering an element within its container:

```css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

**Card Layouts with Equal Heights**: Flex items in a `row` layout default to `stretch` on the cross axis, automatically equalizing heights across all cards in the row.

**Form Layouts**: Aligning labels and inputs in forms is straightforward with Flexbox's cross-axis alignment:

```css
.form-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.form-row label {
  flex: 0 0 120px; /* Fixed width, no grow/shrink */
}

.form-row input {
  flex: 1; /* Grow to fill remaining space */
}
```

## Examples

A responsive card grid using Flexbox:

```css
/* Container with wrapping */
.card-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  padding: 24px;
}

/* Each card grows to fill row, minimum 280px */
.card {
  flex: 1 1 280px;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

/* Card content pushes footer to bottom */
.card-body {
  flex: 1;
}

.card-footer {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #eee;
}
```

A holy grail layout with header, footer, and three columns:

```css
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  flex: 0 0 auto;
}

.main {
  flex: 1;
  display: flex;
}

.sidebar-left,
.sidebar-right {
  flex: 0 0 200px;
}

.content {
  flex: 1;
}

.footer {
  flex: 0 0 auto;
}
```

## Related Concepts

- [[CSS]] - The styling language that provides Flexbox
- [[CSS Grid]] - A complementary two-dimensional layout system
- [[Responsive Design]] - Creating layouts that adapt to different screen sizes
- [[HTML]] - The markup language structured by Flexbox layouts
- [[Frontend]] - The client-side of web development
- [[Web Development]] - The broader discipline of building for the web

## Further Reading

- [MDN: Flexbox Guide](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox)
- [CSS-Tricks Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [W3C Flexbox Specification](https://www.w3.org/TR/css-flexbox-1/)

## Personal Notes

Flexbox transformed [[CSS]] layout from a frustrating series of hacks to a logical, predictable system. I use it constantly for one-dimensional layouts — navbars, form rows, button groups, and card interiors. For full page layouts, [[CSS Grid]] is often more appropriate, but the two complement each other beautifully. A common pattern: Grid for the overall page structure, Flexbox for component-level alignment. The `gap` property (originally Flexbox-spec but now universally supported) is particularly useful for consistent spacing without margin hacks.
