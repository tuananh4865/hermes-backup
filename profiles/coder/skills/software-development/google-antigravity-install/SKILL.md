---
title: Google Antigravity Install
name: google-antigravity-install
description: Install Google Antigravity IDE on Mac when antigravity.google is inaccessible. Browser-based download + DMG mount workflow.
tags: [mac, installation, google, ai-tool]
created: 2026-05-03
updated: 2026-05-03
source: session-2026-05-03
relationships: [hermes-agent]
---

# Google Antigravity Install

Install Google Antigravity (AI agentic IDE by Google/DeepMind) on Mac when the official domain `antigravity.google` is blocked or DNS doesn't resolve.

## When to Use

- User asks to install Google Antigravity
- `antigravity.google` returns DNS error or ERR_NAME_NOT_RESOLVED
- Chrome Web Store search shows no results

## Workflow

### Step 1: Find Mirror Download URL

Navigate to a software download site that hosts Antigravity:

```
https://mac.filehorse.com/download-google-antigravity/
```

Click "Start Download" or "Free Download" button, then use browser console to extract the direct `.dmg` URL:

```javascript
document.querySelector('a[href*=".dmg"]')?.href
```

Alternative: Inspect Network tab for download button click.

### Step 2: Download DMG via Terminal

```bash
curl -L -o ~/Downloads/Antigravity.dmg "https://edgedl.me.gvt1.com/edgedl/release2/.../Antigravity.dmg"
```

### Step 3: Mount and Install

```bash
hdiutil attach ~/Downloads/Antigravity.dmg -nobrowse
cp -R /Volumes/Antigravity/Antigravity.app /Applications/
hdiutil detach /Volumes/Antigravity
```

### Step 4: First Launch

Open from Launchpad or Finder → Applications. macOS will ask confirmation on first launch (normal for downloaded apps).

## Key Notes

- Version 1.23.2 (as of May 2026), ~195MB DMG
- Requires personal Gmail account for preview access
- Apple Silicon + Intel Mac supported

## Related

- [[hermes-agent]] — AI agent framework that can benefit from Antigravity integration
