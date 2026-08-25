---
name: hermes-browser
description: Chrome extension điều khiển Chrome từ Hermes Agent — click/type/fill/screenshot/navigate qua native messaging + MCP. Self-signed, load unpacked. Trigger khi anh nói: "mở trang web", "click nút X", "fill form", "screenshot trang", "điều khiển chrome", "browser tự động", "browser MCP", "điều khiển browser", "tự động hóa trình duyệt".
version: 0.1.0
author: 'Tuấn Anh + Hermes Agent (v0.1.0 — Phase 1 foundation 13/08/2026)'
license: MIT
platforms: [macos]
metadata:
  category: browser
  tags: [browser, chrome, mcp, native-messaging, control, automation, click, type, fill, screenshot, navigate]
  triggers:
    - "mở trang web"
    - "click nút"
    - "fill form"
    - "screenshot trang"
    - "điều khiển chrome"
    - "browser tự động"
    - "browser MCP"
    - "tự động hóa trình duyệt"
    - "control chrome"
    - "browser automation"
---

# Hermes Browser Control — Chrome Extension

> Let Hermes Agent control your Chrome browser — automate tasks, fill forms, take screenshots, navigate pages. Native messaging bridge to Hermes CLI. Pattern mirrors Anthropic's Claude in Chrome extension but self-signed for personal use.

## When to use this skill

Use when anh wants Hermes to:
- Open a URL in Chrome
- Click a button on a page
- Fill in a form field (type text)
- Take a screenshot of current page
- Read page content / DOM / ARIA tree
- Run JavaScript on a page
- Create new tab
- Close tab
- Switch between tabs
- Read console logs / network requests

## Architecture (mirrors Claude pattern)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Google Chrome                                                      │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Service Worker (MV3) — package.json                     │    │
│  │  - Listens for side-panel messages                       │    │
│  │  - Forwards tool calls to native host via                 │    │
│  │    chrome.runtime.connectNative("com.hermes.browser_extension") │ │
│  │  - Streams responses back to side panel                  │    │
│  └──────────────────────────────────────────────────────────┘    │
│  ┌──────────────────┐  ┌──────────────────────────────────────┐  │
│  │  Side Panel UI   │  │  Content Script (per tab)            │  │
│  │  (chat + tools)  │  │  (reads DOM, ARIA, runs JS)         │  │
│  └──────────────────┘  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  ▲
                                  │ Native Messaging API
                                  │ (4-byte LE length + UTF-8 JSON)
                                  │
   ┌──────────────────────────────────────────────────────────┐
   │  native-host/hermes_browser_host.js (Node.js)          │
   │  - Spawned by Chrome with stdio pipes                 │
   │  - Receives tool calls from extension                  │
   │  - Forwards to Hermes CLI via MCP (JSON-RPC 2.0)      │
   │  - Returns results back to extension                   │
   └──────────────────────────────────────────────────────────┘
                                  ▲
                                  │ JSON-RPC 2.0 (MCP protocol 2025-06-18)
                                  │
   ┌──────────────────────────────────────────────────────────┐
   │  Hermes CLI / Claude Code / any MCP host                │
   └──────────────────────────────────────────────────────────┘
```

## What's different from Claude's extension

| Aspect | Claude | Hermes |
|---|---|---|
| Manifest writes | 7 browser folders (controversial) | **Chrome only** (HARD RULE) |
| Auto-install on app launch | Yes (privacy issue) | **Manual click "Install" button** |
| Native host source | Closed binary (Rust) | Open-source Node.js (readable) |
| Sign-in | Required (claude.ai) | None — Hermes CLI talks directly |
| MCP tools | 22 closed-source | Same 22, open source, transparent |


## Available Tools (Phase 3 — v0.2.0)

### TIER 1: Read-only (safe, no state change)
- `tabs_context_mcp` — List all open tabs
- `read_page` — Read page text, headings, links, form count
- `get_page_text` — Just the innerText

### TIER 2: Navigate
- `navigate` — `chrome.tabs.update({url})` — blocks non-http(s) schemes
- `tabs_create_mcp` — Open new tab
- `tabs_close_mcp` — Close tab

### Future (Phase 4+): See references/22-tools-spec.md
- `computer` (left_click, type, etc.) — high risk, needs CDP
- `find` / `javascript_tool` / `form_input` — content script helpers (already in content-script.js)
- `upload_image`, `gif_creator`, `read_network_requests`, etc.

## Architecture Decision: Direct vs CDP

We chose **Option C (direct chrome.* APIs)** over **Option B (CDP)**:
- Extension service worker calls `chrome.tabs.*`, `chrome.scripting.*` directly
- Native host is a thin relay (Phase 3 doesn't need browser control from outside)
- Trade-off: can't drive Chrome when native host is sandboxed separately, BUT we don't need to

Future: when we need Phase 4+ control (click, drag), add Option B (CDP via native host).

## HARD RULES (LESSON FROM HANFF CONTROVERSY)

1. **NEVER silent install** — always require user click "Install" button
2. **NEVER write to multiple browser folders** — Chrome only
3. **NEVER rewrite manifest on every Hermes launch**
4. **NEVER auto-restart native host**
5. **ALWAYS log install/uninstall** to `~/.hermes/logs/hermes-browser-host-install.log`
6. **PROVIDE uninstall button** in popup (one-click kill + manifest removal)
7. **DOCUMENT every permission** in popup + this file

## Status

- **Phase 1: Foundation** ✅ (manifest V3 + service worker stub + side panel UI)
- **Phase 2: Native Messaging Bridge** ✅ (Node.js host, 5/5 ping-pong tests pass, install/uninstall scripts)
- **Phase 3: Tool Dispatch** ✅ (5 tools: tabs_context_mcp, read_page, get_page_text, navigate, tabs_create_mcp, tabs_close_mcp — DIRECT execution by SW, no CDP needed)
- Phase 2: Native messaging bridge
- Phase 3: Core 22 tools
- Phase 4: Self-signed packaging
- Phase 5: Privacy audit + wiki mirror

## Lessons learned (13/08)

**L128: Chrome extension manifest MUST be `manifest.json` at root.** Earlier draft used `package.json` (Node.js convention) — Chrome refused to load. Renamed to `manifest.json` and verified Chrome MV3 required fields present. NEVER claim "ready to test" without actually loading unpacked in Chrome Dev Mode first.
- **Bug + fix:** First install failed because `manifest.path` pointed to Node binary (Chrome exec'd Node with JSON stdin → SyntaxError). Fixed by: (1) adding `#!/usr/bin/env node` shebang, (2) `chmod +x` script, (3) updating manifest template + install.sh to use `__HOST_SCRIPT_PATH__` instead of `__NODE_BIN_PATH__`. Re-install verified 5/5 ping-pong pass. See wiki/concepts/chrome-native-messaging-path-bug-2026-08-13.md.

## Install

```bash
# 1. Load unpacked in Chrome Dev Mode
# Open chrome://extensions/ → enable Developer mode → "Load unpacked" → select this folder

# 2. Install native host (Chrome ONLY, no silent install)
bash ~/.hermes/skills/hermes-browser/native-host/install.sh

# 3. Test ping-pong (verifies native host works)
echo -n '{"jsonrpc":"2.0","id":1,"method":"ping"}' | \
  /Users/tuananh4865/.hermes/node/bin/node \
  /Volumes/Storage-1/Hermes/skills/hermes-browser/native-host/hermes_browser_host.js

# 4. Uninstall (clean removal)
bash ~/.hermes/skills/hermes-browser/native-host/uninstall.sh
```

## Files

- `package.json` — Manifest V3
- `src/service-worker.js` — MV3 service worker
- `src/content-script.js` — Per-tab DOM access
- `src/side-panel.html` — Claude-like sidebar UI
- `src/popup.html` — Extension popup (settings, install, uninstall)
- `src/icons/` — Placeholder icons (replace later)
- `native-host/hermes_browser_host.js` — Node.js bridge (Phase 2)
- `native-host/install.sh` — One-click install (Phase 2)
- `references/22-tools-spec.md` — Claude tool catalog adapted (Phase 3)

## Related

- `wiki/concepts/claude-chrome-extension-architecture-2026-08-13.md` — Reference architecture
- `wiki/projects/hermes-chrome-extension/PLAN.md` — Build plan
- skill `browser-harness` — Re-use CDP infrastructure
- skill `macos-computer-use` — Fallback for stateful actions
