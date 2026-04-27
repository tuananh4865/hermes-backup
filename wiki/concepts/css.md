---
title: "CSS"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [css, web, styling, frontend]
---

# CSS

Cascading Style Sheets (CSS) is the cornerstone technology for styling [[HTML]] documents on the web. While [[HTML]] provides the structural backbone and content of a webpage, CSS controls its visual presentation, including colors, typography, spacing, layout, and responsive behavior across different devices and screen sizes. CSS follows the principle of separation of concerns, keeping presentation logic independent from structural markup, which improves maintainability and enables teams to work on structure and design in parallel.

CSS operates on a cascade model where multiple style rules can apply to the same element, with specific precedence rules determining which styles take effect. The cascade considers origin (author, user, browser default), specificity (how targeted a selector is), and source order to resolve conflicts. Understanding the cascade is fundamental to writing predictable and maintainable stylesheets.

## Overview

CSS was first introduced in 1996 by the World Wide Web Consortium (W3C) to address the growing need for visual styling capabilities that HTML was never designed to handle. Before CSS, web designers relied on HTML attributes and font tags to control appearance, resulting in cluttered markup and inconsistent designs. CSS enabled a cleaner separation of concerns and paved the way for more sophisticated, visually rich web experiences.

Modern CSS supports a wide range of features including animations, transitions, gradients, custom properties (variables), grid layouts, and flexbox. CSS is also the foundation for CSS-in-JS solutions and preprocessors like [[Sass]] and [[Less]], which extend the language with features like nesting, mixins, and functions that compile down to standard CSS. CSS frameworks such as [[Tailwind CSS]], [[Bootstrap]], and [[Foundation]] provide pre-built component styles and utility classes to accelerate development.

CSS is interpreted by web browsers, which render the styled result on screen, in print, or in speech. Browser support for CSS features varies, which is why developers often use tools like Autoprefixer, Can I Use, and CSS polyfills to ensure cross-browser compatibility.

## Selectors

Selectors are the mechanism by which CSS targets specific elements in an [[HTML]] document to apply styles. A selector can target elements by tag name, class, ID, attribute, relationship to other elements, or their state. Understanding the full range of selector types is essential for writing precise, maintainable styles.

**Basic selectors** include the universal selector (`*`), element selectors (`div`, `p`, `span`), class selectors (`.button`), ID selectors (`#header`), and attribute selectors (`[type="text"]`). These form the foundation of any stylesheet.

**Combinators** extend selectors by expressing relationships between elements. The descendant combinator (` `) targets elements nested within another, the child combinator (`>`) targets direct children, the adjacent sibling combinator (`+`) targets elements immediately following another, and the general sibling combinator (`~`) targets all siblings following an element.

**Pseudo-classes** and **pseudo-elements** target elements based on state or structure rather than explicit attributes. Pseudo-classes like `:hover`, `:focus`, `:active`, and `:nth-child()` style elements in particular states or positions. Pseudo-elements like `::before`, `::after`, and `::first-line` allow insertion of generated content or styling of specific portions of an element.

Specificity determines which competing selectors take precedence. Inline styles have highest specificity, followed by IDs, then classes and pseudo-classes, then elements and pseudo-elements. Understanding specificity is critical to debugging unexpected styling results.

## Box Model

The CSS box model describes how every element in [[HTML]] is rendered as a rectangular box with four distinct layers: content, padding, border, and margin. The content area holds the element's actual content (text, images, etc.), surrounded by padding, then border, then margin. The box-sizing property controls whether width and height calculations include padding and border or apply only to the content area.

By default, the standard box model calculates an element's total dimensions by adding padding and border to the specified width and height. This often leads to unexpected layout results. The `box-sizing: border-box` declaration shifts to the alternative box model where width and height encompass content, padding, and border, making size calculations more intuitive. This practice has become a widespread convention in modern CSS development.

The margin property can exhibit collapse behavior where the vertical margins of adjacent block-level elements combine into a single margin equal to the larger of the two. This behavior applies only to margins, not padding or borders, and understanding it is crucial for predicting vertical spacing in a layout.

Visual formatting properties include `display`, which determines an element's box type (block, inline, inline-block, flex, grid, etc.), along with properties for controlling overflow, visibility, float, and positioning. The `display` property is particularly powerful as it fundamentally changes how an element participates in layout.

## Layout

CSS layout has evolved dramatically from simple document flows to sophisticated two-dimensional systems. Modern CSS provides multiple layout models that serve different purposes and offer different degrees of control.

**Flexbox** (Flexible Box Layout) is a one-dimensional layout system designed for distributing space along a single axis—either horizontal or vertical. Flexbox excels at centering content, creating navigation bars, aligning items within a container, and handling dynamic sizing where content should fill available space while respecting constraints. The `justify-content`, `align-items`, `flex-direction`, and `flex-wrap` properties control flex container behavior, while `flex-grow`, `flex-shrink`, and `flex-basis` control individual item sizing.

**CSS Grid** is a two-dimensional layout system that handles both columns and rows simultaneously. Grid is ideal for creating complex page layouts, image galleries, dashboard interfaces, and any design requiring precise control over both axes. Grid introduces `grid-template-columns`, `grid-template-rows`, `gap`, and the ability to name areas for intuitive layout definition. The combination of `fr` units, `auto-fill`, and `auto-fit` creates responsive grid systems without media queries.

**Float layouts** were the dominant technique before flexbox and grid, relying on the `float` property to shift elements to the left or right within their container. Floats remain useful for wrapping text around images but are no longer recommended for page-level layouts due to their complexity and side effects like container collapse.

**Positioning** provides granular control over element placement using `position: static`, `relative`, `absolute`, `fixed`, or `sticky`. Each value establishes a different containing block and stacking context, enabling overlays, sticky headers, modal dialogs, and complex decorative positioning.

**Responsive design** in CSS relies heavily on media queries (`@media`) to apply different styles based on viewport characteristics, along with fluid sizing using units like `vw`, `vh`, `rem`, and percentages. Mobile-first development has become standard practice, where base styles target small screens and progressive enhancement handles larger viewports.

## Related

- [[HTML]] - The markup language that CSS styles
- [[JavaScript]] - Often used alongside CSS for dynamic interactions and DOM manipulation
- [[Sass]] - A CSS preprocessor that adds powerful features to CSS syntax
- [[Tailwind CSS]] - A utility-first CSS framework
- [[Bootstrap]] - A popular component-based CSS framework
- [[Web Development]] - The broader discipline that encompasses CSS alongside HTML and JavaScript
- [[Responsive Design]] - The practice of building websites that adapt to all screen sizes
- [[Box Model]] - Fundamental concept underlying CSS layout
- [[Flexbox]] - One-dimensional layout system in CSS
- [[CSS Grid]] - Two-dimensional layout system in CSS
