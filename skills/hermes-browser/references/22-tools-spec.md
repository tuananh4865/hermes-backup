# 22 MCP Tools Catalog — Hermes Browser Control

> **Adapted from:** Claude's Claude in Chrome extension (k-l-lambda reverse-engineered, Aug 2025)
> **Phase:** 3 (current Phase 2 has only ping + status)
> **Reference:** wiki/concepts/claude-chrome-extension-architecture-2026-08-13.md

## Tool List (Phase 3 Plan)

| # | Tool | Method | Description |
|---|---|---|---|
| 1 | `tabs_context_mcp` | tabs.list | List all open tabs (id, url, title, active, windowId) |
| 2 | `tabs_create_mcp` | tabs.create | Create new tab in current window |
| 3 | `tabs_close_mcp` | tabs.close | Close tab by id |
| 4 | `navigate` | browser.navigate | Navigate current tab to URL |
| 5 | `computer` | browser.action | Mouse + keyboard action (12 sub-actions) |
| 6 | `browser_batch` | browser.batch | Run multiple tool calls in one round-trip |
| 7 | `read_page` | page.read | Read page text + links + interactive elements |
| 8 | `find` | page.find | Find element by CSS/XPath/text |
| 9 | `form_input` | page.input | Fill text into input/textarea |
| 10 | `javascript_tool` | page.js | Run arbitrary JS in page context |
| 11 | `get_page_text` | page.text | Just text content (no DOM) |
| 12 | `resize_window` | browser.resize | Set window size |
| 13 | `read_console_messages` | devtools.console | Read browser console |
| 14 | `read_network_requests` | devtools.network | Read network log |
| 15 | `gif_creator` | record.gif | Record screen as GIF |
| 16 | `upload_image` | upload.image | Upload image to current page |
| 17 | `file_upload` | upload.file | Upload file via file input |
| 18 | `shortcuts_list` | shortcuts.list | List available keyboard shortcuts |
| 19 | `shortcuts_execute` | shortcuts.execute | Execute keyboard shortcut |
| 20 | `switch_browser` | browser.switch | Switch to different browser instance |
| 21 | `list_connected_browsers` | browser.list | List all browsers connected |
| 22 | `select_browser` | browser.select | Select browser to drive |

## `computer` Sub-actions

| Sub-action | Params | Description |
|---|---|---|
| `left_click` | `x, y` | Click at coordinates |
| `right_click` | `x, y` | Right-click at coordinates |
| `double_click` | `x, y` | Double-click |
| `triple_click` | `x, y` | Triple-click (select paragraph) |
| `type` | `text` | Type text into focused element |
| `key` | `keys` | Press keys (e.g. "ctrl+a", "Enter") |
| `scroll` | `amount, direction` | Scroll wheel |
| `scroll_to` | `x, y` | Scroll element into view |
| `hover` | `x, y` | Mouse hover (trigger tooltips) |
| `wait` | `ms` | Wait N ms |
| `left_click_drag` | `from_x, from_y, to_x, to_y` | Drag from point to point |
| `screenshot` | `path?` | Capture viewport to file or base64 |
| `zoom` | `level` | Set browser zoom level |

## Permission Gate (per-domain)

The extension uses `chrome.storage.local` to remember which domains the user has approved:

```js
// On first action request:
const granted = await chrome.storage.local.get(`always-allow:${domain}`);
if (!granted) {
  // Show user a confirm dialog
  const ok = await chrome.notifications.create({
    type: 'basic',
    iconUrl: '/src/icons/128.png',
    title: 'Hermes wants to interact with ' + domain,
    message: 'Click here to allow.',
  });
  if (ok === 'granted') {
    await chrome.storage.local.set({ [`always-allow:${domain}`]: true });
  }
}
```

This pattern is from k-l-lambda's reverse-engineering notes — short-circuit prompt for known sites.

## Privacy Defaults

- **Sensitive domains** (banking, healthcare, government) → ALWAYS prompt, never auto-allow
- **Trusted domains** (one-off allow) → cache for session
- **All actions logged** to `~/.hermes/logs/hermes-browser-actions.log`

## Anti-Patterns to Avoid

- ❌ Disable security headers or CSP — never
- ❌ Bypass CAPTCHA — never
- ❌ Auto-fill credentials without explicit per-action confirmation
- ❌ Persist sensitive data (cookies, tokens) without encryption
- ❌ Send DOM/console content to remote servers without user consent

## Related

- `wiki/concepts/claude-chrome-extension-architecture-2026-08-13.md` — 22 tools reverse-engineered from Claude
- `wiki/concepts/k-l-lambda-chrome-mcp-bridge-2026-08-13.md` — Re-implementation reference
- `references/protocol-framing.md` — Frame format
