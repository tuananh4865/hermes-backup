---
title: Local Storage
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [storage, web, browser, indexeddb, localstorage, persistence]
sources: []
---

# Local Storage

## Overview

Local storage refers to mechanisms for persisting data on a user's device without requiring a server round-trip. In the context of web development, this primarily means browser-based storage APIs like `localStorage`, `sessionStorage`, and IndexedDB. In broader computing, local storage also encompasses native file systems, application-specific configuration stores, and operating system keychain/credential managers. Local storage is fundamental to building offline-capable web applications, improving performance by caching data locally, and storing user preferences and state across sessions.

The key advantage of local storage is **data locality** — data is stored close to where it's consumed, eliminating network latency and reducing server load. For web applications, local storage enables features like remembering login state, caching API responses, storing offline work that syncs later, and persisting user preferences. For AI agents, local storage can be used to maintain conversation history, cache model outputs, store embeddings for retrieval-augmented generation (RAG), and persist agent memory across sessions.

However, local storage comes with constraints. Browser storage is sandboxed per origin, limited in size (typically 5–10 MB for localStorage), and can be cleared by the user or browser policies. Native file systems offer more capacity but require appropriate OS permissions. Understanding the trade-offs between different local storage mechanisms is essential for building robust, performant applications.

## Key Concepts

**localStorage** — A simple, synchronous key-value store available in all modern browsers. Data stored in localStorage persists until explicitly deleted and is shared across all tabs and windows from the same origin. It supports only string values (objects must be serialized with JSON.stringify). The synchronous API makes it fast but blocking, and it's subject to a ~5-10 MB size limit depending on the browser.

**sessionStorage** — Similar to localStorage but scoped to the browser tab or window session. Data is deleted when the tab or window is closed. It's useful for temporary state that shouldn't persist across sessions.

**IndexedDB** — A low-level, asynchronous database in the browser capable of storing structured data including files and blobs. IndexedDB supports indexes, transactions, cursors, and significantly larger storage limits (often hundreds of megabytes or more with user permission). It has a complex, callback-heavy API that has historically made it difficult to use — modern wrappers like Dexie.js simplify this significantly.

**Cache API** — A web API for storing Request/Response pairs, primarily designed for caching HTTP requests (Service Worker use case). It's part of the Service Workers specification and is increasingly used for offline-first application data.

**Native File System Access** — The File System Access API (available in Chromium browsers) allows web apps to read and write files directly on the user's file system with user permission, bridging the gap between web and native applications.

**Origin Private File System (OPFS)** — A storage endpoint private to the origin, offering a file system metaphor with persisted files. It's used by some web-based code editors and compilers to store generated code reliably.

## How It Works

Each browser storage mechanism has distinct characteristics:

**localStorage and sessionStorage** work through a synchronous JavaScript API backed by the browser's internal storage. When you call `localStorage.setItem('key', 'value')`, the browser synchronously writes to disk. This is fast but blocks the main thread for the duration of the write, which can cause jank if storing large amounts of data.

**IndexedDB** operates asynchronously (all operations are non-blocking), using an underlying object store organized by key paths and indexes. Transactions ensure atomicity — a multi-step operation either fully completes or fully rolls back. IndexedDB can store structured data (not just strings), binary blobs, and files. It supports queries via indexes and cursors for efficient iteration over large datasets.

**Storage Limits and Eviction**: Browsers enforce quotas per origin. When the quota is exceeded, the browser may evict data (typically LRU — least recently used) or reject the write. The Storage API (`navigator.storage.estimate()`) allows checking available quota and usage.

**Data Portability**: Data in localStorage is tied to the specific browser and origin. Clearing browser data, switching browsers, or using private/incognito mode may delete or isolate stored data. IndexedDB is similarly scoped but can be more resilient depending on browser implementation.

## Practical Applications

**Offline Web Applications (PWAs)** — Progressive Web Apps use local storage (often via Service Workers and the Cache API) to store assets and data, enabling the app to function without network connectivity. IndexedDB stores structured offline data that syncs when connectivity returns.

**User Preferences and Settings** — Storing UI preferences (theme, language, layout choices), session state, and feature flags locally improves UX by remembering user choices across visits.

**API Response Caching** — Caching API responses locally reduces redundant network requests, speeds up repeated queries, and enables offline access to previously viewed data. Particularly valuable for AI agents that query the same information multiple times.

**AI Agent Memory** — Local storage (especially IndexedDB) can store conversation history, embeddings for RAG pipelines, and agent state. This allows agents to maintain context across sessions without relying on a central database.

**Document Editing** — Rich text editors use local storage to auto-save work in progress, preventing data loss from accidental tab closes or crashes. The origin-private file system (OPFS) is ideal for this use case.

## Examples

**localStorage for simple key-value persistence:**
```javascript
// Storing and retrieving data
localStorage.setItem('user_preferences', JSON.stringify({
  theme: 'dark',
  language: 'en',
  notifications: true
}));

const prefs = JSON.parse(localStorage.getItem('user_preferences'));
console.log(`Theme: ${prefs.theme}, Language: ${prefs.language}`);
```

**IndexedDB with Dexie.js wrapper for structured data:**
```javascript
// Requires: npm install dexie
import Dexie from 'dexie';

const db = new Dexie('AgentMemoryDB');

db.version(1).stores({
  conversations: '++id, timestamp, agentId',
  embeddings: '++id, content, vector, createdAt'
});

// Store a conversation
await db.conversations.add({
  agentId: 'agent-001',
  timestamp: new Date().toISOString(),
  messages: [
    { role: 'user', content: 'What is RAG?' },
    { role: 'assistant', content: 'Retrieval-Augmented Generation...' }
  ]
});

// Query conversations
const recent = await db.conversations
  .where('agentId').equals('agent-001')
  .reverse()
  .limit(10)
  .toArray();

console.log(`Found ${recent.length} recent conversations`);
```

**File System Access API for native file read/write:**
```javascript
// Open a file for reading
const [fileHandle] = await window.showOpenFilePicker();
const file = await fileHandle.getFile();
const contents = await file.text();
console.log(`Read ${contents.length} characters from ${file.name}`);

// Open a file for writing
const writable = await fileHandle.createWritable();
await writable.write('New content');
await writable.close();
```

## Related Concepts

- [[cloud-storage]] — Remote storage solutions (AWS S3, Google Cloud Storage) that contrast with local-only approaches
- [[data-persistence]] — The broader concept of keeping data across sessions, of which local storage is one implementation
- [[IndexedDB]] — A specific browser database API for storing structured data
- [[Progressive Web Apps (PWA)]] — Web applications that leverage local storage and Service Workers for offline capability
- [[SQLite]] — A lightweight, embedded database engine used natively that shares conceptual ground with IndexedDB

## Further Reading

- MDN Web Docs: Web Storage API — developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API
- MDN Web Docs: IndexedDB — developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API
- Dexie.js Documentation — dexie.org — a Promise-based IndexedDB wrapper
- File System Access API — developer.mozilla.org/en-US/docs/Web/API/File_System_Access_API
- "Building Offline-First Web Apps" — various PWA resources on Google Web Fundamentals

## Personal Notes

localStorage is the 80% solution — it's synchronous, dead simple, and handles the vast majority of use cases where you just need to store user preferences or small amounts of cached data. When you need more structure, larger volumes, or asynchronous operations, IndexedDB is the answer, but use a wrapper like Dexie. The raw IndexedDB API is notoriously painful to work with. For AI agents specifically, I've found IndexedDB invaluable for storing conversation history and embeddings — it survives browser restarts and works offline, which is important for privacy-sensitive applications. Just remember: local storage is per-origin, per-browser, and can be cleared by the user at any time. Never treat it as a source of truth for critical data that needs replication or durability.
