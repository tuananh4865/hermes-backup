---
title: "CSS Grid"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [css, layout, web-development, frontend, responsive-design]
---

# CSS Grid

## Overview

CSS Grid Layout (often simply called CSS Grid) is a two-dimensional layout system for the web, introduced in CSS3 and widely supported across modern browsers since 2017. Unlike previous CSS layout techniques that primarily handled one dimension at a time (block or inline), CSS Grid allows developers to work with both rows and columns simultaneously, enabling complex, responsive layouts that were difficult or impossible with float, inline-block, or flexbox alone.

CSS Grid revolutionizes web layout by treating the container as a grid with definable tracks (rows and columns) and allowing child elements to span or position themselves anywhere within this grid. It provides precise control over alignment, spacing, and layout structure without resorting to hacks or clearfixes that characterized older approaches.

The specification is maintained by the W3C, with Level 1 (the core grid system) achieving broad browser support and Level 2 (subgrid) gradually gaining adoption to address nested grid alignment.

## Key Concepts

**Grid Container**: The parent element with `display: grid` or `display: inline-grid`. It establishes the grid formatting context and controls how child elements are positioned.

**Grid Tracks**: The rows and columns of the grid. Defined using `grid-template-rows` and `grid-template-columns`. Tracks can use fixed sizes (px, em), flexible units (fr), or content-based sizing (auto, min-content, max-content).

**Grid Line**: The dividing lines that make up the grid structure. Lines are numbered (1, 2, 3...) or can be named in the track definition. Grid items position themselves by referencing line numbers or names.

**Grid Cell**: The intersection of a row and column—the smallest unit of the grid. A grid item occupies at least one cell.

**Grid Area**: Any rectangular space on the grid, potentially containing multiple cells. Grid items can span multiple rows and/or columns using `grid-column` and `grid-row` properties.

**Gap**: The spacing between grid tracks. Controlled via `gap`, `row-gap`, and `column-gap` properties.

**fr Unit**: The flexible "fraction" unit. `1fr 2fr 1fr` divides available space proportionally—2 parts to the middle column, 1 part each to the outer columns.

**Subgrid**: A feature (now supported in modern browsers) where a nested grid can participate in the parent grid's tracks, ensuring alignment across nesting boundaries.

## How It Works

The fundamental CSS Grid workflow:

1. **Create a grid container** with `display: grid`
2. **Define grid tracks** using `grid-template-columns` and `grid-template-rows`
3. **Place grid items** either automatically (auto-placement) or explicitly using line numbers or named areas
4. **Adjust spacing and alignment** using gap and alignment properties

```css
/* Basic Grid Setup */
.grid-container {
    display: grid;
    
    /* Define 3 columns: 200px, 1fr (flexible), 200px */
    grid-template-columns: 200px 1fr 200px;
    
    /* Define rows: auto-sized header, 1fr content, 100px footer */
    grid-template-rows: auto 1fr 100px;
    
    /* Gap between tracks */
    gap: 20px;
    
    /* Optional: name grid areas for cleaner placement */
    grid-template-areas:
        "header header header"
        "sidebar main main"
        "footer footer footer";
}

.grid-item {
    /* Position by grid lines */
    grid-column: 2 / 4;  /* Span columns 2 through 4 */
    grid-row: 2 / 3;     /* Row 2 only */
}

/* Or position by named areas */
.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

```html
<div class="grid-container">
    <header class="header">Header</header>
    <aside class="sidebar">Sidebar</aside>
    <main class="main">Main Content</main>
    <footer class="footer">Footer</footer>
</div>
```

## Practical Applications

- **Page-level layouts**: CSS Grid excels at creating the overall page structure—headers, sidebars, main content areas, and footers with precise control over proportions.
- **Card grids**: Responsive card layouts that automatically adjust column counts based on viewport width using `auto-fill` or `auto-fit` with flexible `fr` units.
- **Overlapping elements**: Grid items can occupy the same cells, enabling overlay effects without absolute positioning or z-index complexity.
- **Alignment-focused layouts**: Grid's alignment properties (justify-items, align-items, place-items) make centering and distributed layouts straightforward.
- **Holy Grail layout**: The classic sidebar-content-sidebar with header-footer layout is nearly trivial with CSS Grid's named areas.

## Examples

**Responsive Card Grid** that adapts from 1 to 4 columns:

```css
.card-grid {
    display: grid;
    /* Create as many 250px columns as fit, then stretch remaining space */
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 24px;
}

.card {
    background: white;
    border-radius: 8px;
    padding: 24px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

This one line of grid-template-columns creates a responsive layout that:
- Creates as many 250px minimum columns as fit in the container
- Stretches columns to fill remaining space (`1fr`)
- Automatically wraps to new rows as needed
- Requires no media queries for basic responsiveness

**Dashboard Layout**:

```css
.dashboard {
    display: grid;
    grid-template-columns: 260px 1fr;
    grid-template-rows: 60px 1fr 40px;
    height: 100vh;
    grid-template-areas:
        "nav header"
        "nav main"
        "nav footer";
}

nav { grid-area: nav; }
header { grid-area: header; }
main { grid-area: main; overflow-y: auto; }
footer { grid-area: footer; }
```

## Related Concepts

- [[Flexbox]] - One-dimensional layout for distributing space along a single axis
- [[CSS Layout]] - Broader topic of positioning elements on web pages
- [[Responsive Design]] - Techniques for adapting layouts to different viewports
- [[CSS]] - The styling language that includes Grid
- [[Box Model]] - Foundation concept for how elements occupy space

## Further Reading

- CSS Grid Specification (W3C): https://www.w3.org/TR/css-grid-1/
- Rachel Andrew, "The New CSS Layout" — Comprehensive Grid coverage
- CSS-Tricks "A Complete Guide to CSS Grid" — Classic reference

## Personal Notes

CSS Grid became my default layout tool the moment browser support became universal. The mental model shift—from thinking about elements flowing sequentially to thinking about a coordinate space where items can be placed anywhere—is initially disorienting but ultimately liberating. I still use Flexbox for component-level layouts where content drives size (button icons, nav items, form elements), but CSS Grid for structural page layout. The combination of both handles virtually every layout scenario I've encountered.
