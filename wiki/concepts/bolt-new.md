---
title: "Bolt.new"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: [ai-coding, browser-ide, full-stack, webdev, stackblitz]
related:
  - [[cursor]]
  - [[claude-code]]
  - [[v0-dev]]
  - [[vibe-coding-solo-developer]]
  - [[solo-developer-ai-workflow]]
---

# Bolt.new

Browser-based AI-powered full-stack development environment by StackBlitz. Write, test, and deploy complete web applications entirely in the browser — no local setup required.

## Overview

Bolt.new combines AI code generation with a WebContainer-based in-browser runtime. It can prompt an AI to build an entire application, run it, make changes via chat, and deploy to production — all without leaving the browser or installing dependencies locally.

**Key differentiator**: WebContainer runs Node.js entirely in the browser via WebAssembly, enabling instant hot reload and full dev server capability without Docker or local Node installation.

## Key Concepts

### How It Works

Bolt.new uses a combination of:
- **WebContainer**: In-browser Node.js runtime (WebAssembly-based)
- **AI Code Generation**: Claude-powered prompt-to-code
- **Instant Preview**: Full Next.js/React/Vite apps run live in browser
- **Deploy Integration**: One-click deploy to Cloudflare, Vercel, or Netlify

### Core Features

- **Natural language to code**: Describe what you want, Bolt.new builds it
- **Live error fixing**: AI identifies and fixes errors during development
- **Full-stack support**: API routes, databases, authentication — all in browser
- **Template library**: Start from 50+ templates (Next.js, React, Vue, Svelte, etc.)
- **File editing**: Direct file tree editing alongside AI chat
- **Terminal access**: Built-in terminal for npm/pnpm commands

### WebContainer Technology

WebContainer is a browser-native OS that runs Node.js:
- Boots in ~200ms (vs minutes for Docker)
- Full npm install support
- Hot module replacement without page reload
- Native POSIX file system API
- SharedArrayBuffer + WebWorkers for multi-process

## Practical Applications

### Best For

1. **Rapid prototyping**: Turn idea description into running app in minutes
2. **No-setup environments**: Interview coding, client demos, classroom coding
3. **Full-stack demos**: Ship working prototypes to stakeholders
4. **Learning**: Explore frameworks without installation overhead
5. **Bug reproduction**: Create minimal repro cases to share

### Comparison with Alternatives

| Feature | Bolt.new | Cursor | Claude Code |
|---------|----------|--------|-------------|
| Environment | Browser | Desktop | Terminal |
| Setup time | 0 seconds | Minutes | Minutes |
| AI model | Claude | Multiple | Claude |
| Full-stack | Excellent | Good | Good |
| Keyboard-first | No | Yes | Yes |
| Local files | No | Yes | Yes |
| Pricing | Free tier + Pro | $20/mo | $20/mo |

### Workflow Example

```
1. Open bolt.new
2. Describe: "Next.js app with Prisma, PostgreSQL, and auth"
3. AI scaffolds full project, installs deps, runs dev server
4. Preview shows running app in iframe
5. Chat: "Add a dashboard page with charts"
6. AI writes code, preview hot-reloads
7. Click "Deploy" — choose Vercel/Cloudflare
8. Get production URL in seconds
```

### Limitations

- **Cold starts**: WebContainer takes 2-5 seconds to boot
- **No Python/Ruby/Go**: Only Node.js-based stacks
- **Browser memory**: Large apps may hit memory limits
- **Vendor lock-in**: Project stays on StackBlitz infrastructure
- **Complex backends**: Database connections can be tricky (WebContainer networking)

## Related Concepts

- [[cursor]] — Desktop AI-first IDE
- [[claude-code]] — Terminal-native AI coding agent
- [[v0-dev]] — Vercel's React/Next.js prototyping tool
- [[vibe-coding-solo-developer]] — Solo dev using AI tools
- [[solo-developer-ai-workflow]] — Full solo dev workflow

## Further Reading

- [Bolt.new Official Site](https://bolt.new) — Product homepage
- [StackBlitz WebContainer](https://stackblitz.com/webcontainer) — Technology explanation
- [WebContainer API Docs](https://webcontainer.io) — Technical documentation

---

*Synthesized from AI agent frameworks research — 2026-04-21*
