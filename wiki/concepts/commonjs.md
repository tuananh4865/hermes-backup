---
title: "CommonJS"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [javascript, modules, nodejs, npm, module-system, es-modules]
---

# CommonJS

## Overview

CommonJS (CJS) is a module system for JavaScript that was designed to enable server-side JavaScript outside the browser. Created around 2009 as part of an effort to establish a standard library for JavaScript outside browser environments, CommonJS defined the `require()` function and `module.exports` object that became the backbone of Node.js module loading. Before ES Modules (ESM) were standardized in ES2015, CommonJS was the dominant module system for JavaScript on the server, npm's ecosystem, and build tools. While modern JavaScript has adopted ES Modules as the standard, CommonJS remains deeply embedded in the Node.js ecosystem and remains relevant for understanding legacy code and many npm packages still distributed in CJS format.

## Key Concepts

**`module` object** — In Node.js, every file is implicitly wrapped in a module scope. The `module` object is a plain JavaScript object that has properties describing the current module, most importantly `exports` (and its alias `module.exports`). The `module.exports` object is what gets returned when another module calls `require()` on this module.

**`require()` function** — This is the primary API for loading modules in CommonJS. When you call `require('some-module')`, Node.js resolves the module path, executes its code, and returns whatever that module has assigned to `module.exports`. The resolution algorithm searches in `node_modules/` directories, relative paths, and core modules.

**The Module Wrapper** — Node.js does not execute modules in a completely global scope. Each module is wrapped in a function that provides the `module`, `exports`, `require`, `__filename`, and `__dirname` variables. This is why these identifiers exist in Node.js modules but not in browser JavaScript by default.

**Circular Dependencies** — CommonJS handles circular requires gracefully, though with caveats. If module A requires module B, and module B requires module A, Node.js will return whatever `module.exports` has been populated with so far (even if incomplete), rather than throwing an error.

## How It Works

When Node.js executes `require('./math.js')`:

1. Node.js resolves the path to an absolute file path
2. It checks the module cache — if already loaded, returns cached `module.exports`
3. If not cached, creates a new `Module` object and inserts it into the cache (to handle circular deps)
4. Loads the file content and wraps it in the module function
5. Executes the module code, which populates `module.exports`
6. Returns `module.exports` to the caller

```javascript
// math.js
const add = (a, b) => a + b;
const multiply = (a, b) => a * b;

module.exports = { add, multiply };
// or equivalently:
// exports.add = add;
// exports.multiply = multiply;

// main.js
const { add, multiply } = require('./math');
console.log(add(2, 3)); // 5
console.log(multiply(4, 5)); // 20
```

## Practical Applications

- **Node.js server-side code** — All Node.js applications before ESM adoption use CommonJS by default
- **npm packages** — The majority of npm packages in the registry are distributed as CommonJS modules (they contain `"main": "index.js"` pointing to CJS bundles)
- **Build tools and CLIs** — Webpack, Babel, ESLint, and many other tools are written in CommonJS
- **Testing frameworks** — Jest, Mocha, and AVA all work seamlessly with CommonJS modules
- **Legacy codebases** — Many existing projects still use CJS and will continue to for years

## Examples

A practical example of a module that exports multiple things:

```javascript
// database.js
const { Pool } = require('pg'); // external CJS package
const connectionString = process.env.DATABASE_URL;

const pool = new Pool({ connectionString });

async function query(text, params) {
  const result = await pool.query(text, params);
  return result.rows;
}

function getClient() {
  return pool.connect();
}

// Export multiple ways to use this module
module.exports = {
  query,
  getClient,
  pool, // also expose internals when needed
};
```

Using the module:

```javascript
// app.js
const db = require('./database');

async function getUser(id) {
  const rows = await db.query('SELECT * FROM users WHERE id = $1', [id]);
  return rows[0];
}
```

## Related Concepts

- [[ES Modules]] — The ECMAScript-standardized module system (import/export) that is now preferred in modern JavaScript
- [[Node.js]] — The runtime environment where CommonJS became the de facto standard
- [[npm]] — The package manager and registry that distributes CommonJS modules
- [[Module Resolution]] — The algorithm Node.js uses to find modules from require() calls
- [[Bundlers]] — Tools like Webpack and Rollup that understand both CJS and ESM

## Further Reading

- [Node.js Modules Documentation](https://nodejs.org/api/modules.html) — Official module system docs
- [CommonJS Spec](http://wiki.commonjs.org/wiki/Modules/1.1) — The original CommonJS proposal
- [ES Modules: A cartoon deep-dive](https://hacks.mozilla.org/2018/03/es-modules-a-cartoon-deep-dive/) — How ESM differs from CJS

## Personal Notes

CommonJS is one of those technologies I use daily but rarely think about. The module wrapper function is a clever piece of engineering — it gives every module its own scope without requiring explicit scoping syntax. The distinction between `module.exports` and `exports` is a common stumbling block: `exports` is just a reference to `module.exports`, so reassigning `exports = {}` breaks the link while `exports.foo = 'bar'` works fine. Even though ES Modules are now the standard, understanding CommonJS is still essential for working with Node.js codebases.
