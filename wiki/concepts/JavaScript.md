---
title: JavaScript
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [javascript, programming-language, web, frontend]
---

# JavaScript

## Overview

JavaScript is a high-level, interpreted programming language that forms one of the core technologies of the World Wide Web, alongside [[HTML]] and [[CSS]]. Originally developed by Brendan Eich at Netscape Communications in 1995, JavaScript was designed to add interactivity and dynamic behavior to web pages. Today, it is the most widely deployed scripting language in the world, running on virtually every web browser and increasingly on servers and embedded devices through runtime environments like [[Node.js]].

JavaScript is a multi-paradigm language that supports object-oriented, functional, and event-driven programming styles. Its syntax draws heavily from C-style languages, making it accessible to developers familiar with languages like Java, C++, and C#. However, JavaScript's type system and execution model are quite different from those compiled, statically typed languages, which gives it a distinctive character and considerable flexibility.

## History

JavaScript was created in 1995 during a period of intense competition between Netscape Navigator and Microsoft Internet Explorer. Netscape tasked Brendan Eich with developing a scripting language for their web browser in an extremely short timeframe—reportedly just ten days. The initial version, initially called Mocha and later renamed LiveScript, was shipped with Netscape Navigator 2.0. When Netscape partnered with Sun Microsystems to promote Java technology, the language was rebranded as JavaScript, though the two languages are fundamentally different in design.

The rapid adoption of JavaScript by web developers led Microsoft to reverse-engineer the language for Internet Explorer 3.0, releasing JScript in 1996. This created a fragmented landscape where web developers had to write browser-specific code. To standardize the language, Netscape submitted JavaScript to the European Computer Manufacturers Association (ECMA) in 1996, resulting in the ECMAScript specification (ECMA-262) being published in 1997.

Since then, ECMAScript has undergone numerous revisions. ES3 (1999) was the first widely implemented version, followed by ES5 (2009) which introduced strict mode and JSON support. ES6 (ES2015) was a landmark release that added classes, modules, arrow functions, template literals, and many other features. The language now follows an annual release cycle, with ES2024 being the most recent major specification.

## Core Features

JavaScript's type system is dynamic and loosely typed, meaning variables do not require explicit type declarations and can hold values of any type. The language supports several data types including numbers, strings, booleans, objects, arrays, and special values like null and undefined. JavaScript uses [[prototypal inheritance]] rather than classical class-based inheritance—a distinctive feature where objects can inherit directly from other objects through a prototype chain.

The event-driven programming model is central to JavaScript's role in web development. Web browsers emit events such as user clicks, keyboard input, page loading, and network responses, and JavaScript functions can be registered as handlers to respond to these events asynchronously. This model enables non-blocking, responsive user interfaces even while performing operations like network requests or timers.

JavaScript also supports first-class functions, meaning functions are treated as values that can be assigned to variables, passed as arguments, and returned from other functions. This capability underlies patterns like callbacks, closures, and higher-order functions, enabling powerful functional programming techniques. Additionally, JavaScript includes a concurrency model based on an event loop, allowing it to handle asynchronous operations efficiently without multithreading.

## Runtime

JavaScript code executes within a runtime environment that provides the language engine, standard library, and host objects. The most common runtime is the web browser, where JavaScript has access to the Document Object Model (DOM), Browser Object Model (BOM), and various Web APIs. Each major browser includes its own JavaScript engine: Google's V8 powers Chrome and Edge, Mozilla's SpiderMonkey runs in Firefox, and Apple's JavaScriptCore (Nitro) powers Safari.

[[Node.js]] revolutionized JavaScript by bringing the language outside the browser. Built on the V8 engine, Node.js enables server-side JavaScript execution and provides a rich set of APIs for file system access, networking, and other system-level operations. It introduced the CommonJS module system and later embraced the ES Module standard, making JavaScript viable for building scalable network applications, command-line tools, and microservices.

Modern JavaScript engines employ sophisticated optimization techniques including just-in-time (JIT) compilation, inline caching, and garbage collection. V8, for example, compiles JavaScript to machine code directly, achieving performance levels that rival natively compiled languages for many workloads. This optimization, combined with the language's portability and ubiquity, has made JavaScript one of the most versatile and widely used programming languages in existence.

## Related

- [[Node.js]] - Server-side JavaScript runtime built on V8
- [[TypeScript]] - Typed superset of JavaScript that compiles to plain JS
- [[React]] - JavaScript library for building user interfaces
- [[HTML]] - HyperText Markup Language, the standard for web page structure
- [[CSS]] - Cascading Style Sheets for web page presentation
- [[Prototypal Inheritance]] - JavaScript's object inheritance mechanism
- [[Event Loop]] - JavaScript's concurrency model for handling async operations
- [[V8]] - Google's high-performance JavaScript engine used in Chrome and Node.js
