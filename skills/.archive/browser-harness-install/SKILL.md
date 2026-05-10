---
title: Browser Harness Install
name: browser-harness-install
description: Install browser-use/browser-harness as a Hermes skill. Clone repo, uv tool install, create Hermes skill, attach to Chrome. MUST be run by user for Chrome security dialog — cannot be automated.
category: browser
tags: [browser, automation, CDP, install]
created: 2026-04-30
updated: 2026-04-30
relationships: [browser-harness]
---

# browser-harness-install

Install browser-use/browser-harness (Browser Harness — self-healing CDP browser control) as a Hermes skill.

## What it is

Browser Harness connects to the user's already-running Chrome via CDP (Chrome DevTools Protocol). Self-healing, ~592 lines of Python. No framework, no recipes, no rails. One websocket to Chrome.

**Repo**: https://github.com/browser-use/browser-harness
**Stars**: ~8K

## Install Steps

### 1. Clone to stable location (NOT /tmp)

```bash
git clone https://github.com/browser-use/browser-harness ~/Developer/browser-harness
```

### 2. Install as uv tool (editable, keeps command on PATH)

```bash
cd ~/Developer/browser-harness
uv tool install -e .
command -v browser-harness
```

### 3. Create Hermes skill files

Create `/Volumes/Storage-1/Hermes/skills/browser-harness/SKILL.md` pointing to `~/Developer/browser-harness/SKILL.md`.

Also copy `browser-install.md` with bootstrap instructions.

### 4. Verify command works

```bash
browser-harness --doctor
```

Expected output: shows chrome running, daemon state, active connections.

### 5. Attach to Chrome — REQUIRES USER INTERACTION

```bash
browser-harness --setup
```

**⚠️ CRITICAL**: This step shows a looped message "click Allow on chrome://inspect". The `--setup` command polls for Chrome security dialog acceptance — the USER must manually:
1. Open `chrome://inspect/#remote-debugging` in Chrome
2. Tick the checkbox if shown
3. Click "Allow"

This is a Chrome security policy — cannot be automated. Tell the user to do this, then verify with `browser-harness --doctor`.

### 6. Verify full attachment

```bash
browser-harness -c 'print(page_info())'
```

Should return page URL, title, dimensions.

## If --setup fails with DevToolsActivePort missing

Chrome's remote-debugging has never been enabled on this profile. On macOS:
```bash
osascript -e 'tell application "Google Chrome" to activate' \
          -e 'tell application "Google Chrome" to open location "chrome://inspect/#remote-debugging"'
```
Then have user tick checkbox + click Allow.

## If daemon stale after Chrome restart

```bash
pkill -9 -f "Google Chrome"
rm -f /tmp/bu-default.sock /tmp/bu-default.pid
open -a "Google Chrome"
browser-harness --doctor
```

## Verification checklist

- [ ] `command -v browser-harness` returns path
- [ ] `browser-harness --doctor` shows: chrome running, daemon alive, 1+ active connection
- [ ] `browser-harness -c 'print(page_info())'` returns page data

## Skill files created

- `browser-harness/SKILL.md` — main skill pointing to ~/Developer/browser-harness
- `browser-harness/browser-install.md` — bootstrap instructions

## Screenshot behavior

`capture_screenshot()` ghi đè `/tmp/shot.png` mỗi lần gọi. Copy ra file riêng ngay sau chụp nếu cần giữ lại.

## Source

- SKILL.md: `~/Developer/browser-harness/SKILL.md`
- Install guide: `~/Developer/browser-harness/install.md`
