---
title: HTML
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [html, web, markup, frontend]
---

# HTML

## Overview

HTML (HyperText Markup Language) is the standard markup language used to create and structure content on the World Wide Web. It provides the foundational building blocks for virtually every webpage, defining elements such as headings, paragraphs, links, images, tables, forms, and multimedia. HTML describes the structure of a webpage using a series of elements that tell the browser how to display content. It was first introduced by Tim Berners-Lee in 1991 at CERN and has since evolved through multiple versions, with HTML5 being the current major standard.

HTML works in conjunction with [[CSS]] for styling and presentation, and [[JavaScript]] for interactivity and dynamic behavior. Together, these three technologies form the core triad of frontend web development. HTML documents are text files saved with an .html or .htm extension and are interpreted by web browsers such as Chrome, Firefox, Safari, and Edge. The browser parses the HTML and renders it into the visual representation users see on screen.

## Structure

The structure of an HTML document is organized hierarchically, starting with a Document Type Declaration (DOCTYPE) followed by the root `<html>` element, which contains the `<head>` and `<body>` sections. The `<head>` element holds metadata about the document, including the title, character encoding, linked stylesheets, and scripts. The `<body>` element contains all the visible content that users interact with.

### Elements

HTML elements are the fundamental building blocks of any webpage. An element typically consists of an opening tag, content, and a closing tag. For example, `<p>This is a paragraph.</p>` creates a paragraph element. Elements can be nested within other elements to create complex structures. Common elements include headings (`<h1>` through `<h6>`), paragraphs (`<p>`), links (`<a>`), images (`<img>`), lists (`<ul>`, `<ol>`, `<li>`), tables (`<table>`, `<tr>`, `<td>`), and divisions (`<div>`).

Elements can also be self-closing, meaning they do not require a separate closing tag. The `<img>` and `<br>` elements are examples of self-closing tags. Void elements like these carry all their information within the opening tag itself.

### Attributes

Attributes provide additional information about HTML elements and are always specified in the opening tag. They consist of a name and a value pair, such as `href="https://example.com"` in an anchor tag. Attributes customize element behavior, define relationships, or specify resource sources. The `class` and `id` attributes are particularly important for [[CSS]] styling and [[JavaScript]] manipulation. Other common attributes include `src` for specifying resource sources in media elements, `alt` for providing alternative text for images, and `style` for inline CSS styling.

## Semantic HTML

Semantic HTML refers to the practice of using HTML elements that accurately describe their meaning and purpose, rather than using generic containers like `<div>` and `<span>` for everything. Semantic elements clearly convey the role of their content to both browsers and developers. Examples include `<header>` for introductory content, `<nav>` for navigation sections, `<main>` for the primary content area, `<article>` for self-contained content, `<section>` for thematic groupings, `<aside>` for tangential content, and `<footer>` for footer information.

Using semantic HTML improves accessibility for screen readers and assistive technologies, enhances search engine optimization (SEO) by helping search engines understand page structure, makes code more readable and maintainable, and provides better defaults for styling. Semantic elements work alongside traditional structural elements and are a core principle of modern web development practices. They are closely related to the concept of the [[DOM]] (Document Object Model), which represents the structure of a webpage as a tree of objects that scripts can manipulate.

## HTML5

HTML5 is the fifth and current major version of the HTML standard, finalized in 2014 by the World Wide Web Consortium (W3C). It introduced numerous new features and APIs that extended HTML beyond its original purpose of structuring documents. HTML5 moved away from proprietary plugins like Adobe Flash by adding native support for audio (`<audio>`) and video (`<audio>`) playback directly in the browser.

Key features of HTML5 include the `<canvas>` element for drawing graphics and animations via [[JavaScript]], the `<svg>` element for scalable vector graphics, form input types like `email`, `date`, `range`, and `url` that provide built-in validation and specialized keyboards on mobile devices, local storage (`localStorage` and `sessionStorage`) for client-side data persistence, the Geolocation API for accessing user location, Web Workers for background script execution, and the History API for manipulating the browser history stack.

HTML5 also introduced structural elements like `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, and `<footer>`, which formalized the semantic markup practices discussed above. It also improved error handling, ensuring that browsers handle malformed HTML more consistently. HTML5 is designed to be backward compatible with older HTML versions while supporting modern web application requirements. It powers everything from simple blogs to complex single-page applications and interactive multimedia experiences across the web.

## Related

- [[CSS]] - Cascading Style Sheets, used to style and layout HTML elements
- [[JavaScript]] - Programming language that adds interactivity and dynamic behavior to webpages
- [[Web Development]] - The broader discipline of building websites and web applications
- [[DOM]] - Document Object Model, the programming interface for HTML documents
- [[HTTP]] - Hypertext Transfer Protocol, the foundation for data communication on the web
- [[URL]] - Uniform Resource Locator, the address used to locate HTML documents and resources
- [[Browser]] - Software application used to access and display HTML pages on the web
