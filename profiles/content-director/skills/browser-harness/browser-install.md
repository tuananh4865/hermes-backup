---
title: Browser Harness Install
name: browser-install
description: Install and bootstrap browser-harness into Hermes Agent, then connect it to the user's real Chrome with minimal prompting.
category: browser
tags: [browser, automation, CDP, install]
created: 2026-04-30
updated: 2026-04-30
source: ~/Developer/browser-harness/install.md
relationships: [browser-harness]
---

# browser-harness install

Use this for first-time install, reconnect, or cold-start browser bootstrap. For day-to-day browser work, use the `browser-harness` skill.

## Already installed?

If `~/Developer/browser-harness` exists and `command -v browser-harness` works, skip to Browser Bootstrap.

## Install

```bash
# Clone to stable location (not /tmp)
git clone https://github.com/browser-use/browser-harness ~/Developer/browser-harness

cd ~/Developer/browser-harness
uv tool install -e .
command -v browser-harness
```

## Browser bootstrap

### Best: one-command setup
```bash
browser-harness --setup
```

### Manual bootstrap (if --setup fails)

1. Run `uv sync` in the repo if needed.
2. Test directly:
```bash
uv run browser-harness -c 'print(page_info())'
```
3. If it works, skip the rest.

4. If it fails with **"DevToolsActivePort missing"** → open `chrome://inspect/#remote-debugging` and tick the checkbox + click Allow.
   - On macOS with Chrome already running:
```bash
osascript -e 'tell application "Google Chrome" to activate' \
          -e 'tell application "Google Chrome" to open location "chrome://inspect/#remote-debugging"'
```

5. If it fails with **stale websocket** → restart daemon:
```bash
uv run python - <<'PY'
from browser_harness.admin import restart_daemon
restart_daemon()
PY
```

6. Verify:
```bash
browser-harness -c 'print(page_info())'
```

## If Chrome won't start properly

```bash
pkill -9 -f "Google Chrome"
rm -f /tmp/bu-default.sock /tmp/bu-default.pid
open -a "Google Chrome"
# wait 5 seconds
browser-harness -c 'print(page_info())'
```

## Maintenance

- `browser-harness --doctor` — check install + daemon state
- `browser-harness --setup` — re-run browser attach
- `browser-harness --update -y` — update + restart daemon (auto-runs when banner appears)

## Key reminders

- The remote-debugging checkbox is **per-profile sticky** — only needed the first time per profile
- Prefer `browser-harness --setup` over manual steps when available
- On macOS: use AppleScript `open location` over `open -a` when Chrome is already running
- Always contribute back domain skills after learning non-obvious site mechanics
