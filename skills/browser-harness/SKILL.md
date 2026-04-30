---
title: Browser Harness
name: browser-harness
description: Direct browser control via CDP. Use when the user wants to automate, scrape, test, or interact with web pages. Connects to the user's already-running Chrome.
category: browser
tags: [browser, automation, CDP, web]
created: 2026-04-30
updated: 2026-04-30
source: ~/Developer/browser-harness/SKILL.md
relationships: [browser-use, browser]
---

# browser-harness

Direct browser control via CDP. For task-specific edits, use `~/Developer/browser-harness/agent-workspace/agent_helpers.py` and `~/Developer/browser-harness/agent-workspace/domain-skills/`. For setup, install, or connection problems, read `browser-install`.

## Quick test

```bash
browser-harness -c 'print(page_info())'
```

## Usage pattern

```bash
browser-harness -c '
new_tab("https://example.com")
wait_for_load()
print(page_info())
'
```

- Invoke as `browser-harness` — it's on $PATH. No cd, no uv run.
- First navigation is `new_tab(url)`, not `goto_url(url)` — goto runs in the user's active tab and clobbers their work.

## Key principles

- **Screenshots first**: `capture_screenshot()` to understand the current page, find visible targets, decide next action.
- **Coordinate clicks**: `capture_screenshot()` → read pixel → `click_at_xy(x, y)` → screenshot to verify.
- **Bulk HTTP**: `http_get(url) + ThreadPoolExecutor`. No browser for static pages.
- **After goto**: always `wait_for_load()`.
- **Auth wall**: redirected to login → stop and ask the user. Don't type credentials.

## Interaction skills (domain-agnostic)

Location: `~/Developer/browser-harness/interaction-skills/`
- cookies, cross-origin-iframes, dialogs, downloads, drag-and-drop, dropdowns
- iframes, network-requests, print-as-pdf, profile-sync, screenshots, scrolling
- shadow-dom, tabs, uploads, viewport

## Domain skills (site-specific)

Location: `~/Developer/browser-harness/agent-workspace/domain-skills/`
- tiktok/upload.md
- polymarket/scraping.md

Search first before inventing a new approach:
```bash
rg --files ~/Developer/browser-harness/agent-workspace/domain-skills
```

## Maintenance

- `browser-harness --doctor` — version, install mode, daemon + Chrome state
- `browser-harness --setup` — re-run browser attach flow
- `browser-harness --update -y` — pull latest, restart daemon (runs automatically when banner appears)

## Design constraints

- Coordinate clicks default — `Input.dispatchMouseEvent` passes through iframes/shadow/cross-origin
- Connect to user's running Chrome — don't launch a separate browser
- CDP for anything helpers don't cover: `cdp("Domain.method", params)`
- Keep `agent-workspace/agent_helpers.py` for task-specific helpers
