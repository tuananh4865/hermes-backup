---
title: "Bookmarks — Web Clipper"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [obsidian, clipping, workflow]
---

# Bookmarks — Web Clipper

Obsidian web clipper via bookmarklet — saves articles directly to vault as markdown.

## Setup (Desktop)

1. Run the generator:
   ```bash
   python3 ~/wiki/scripts/generate-bookmarklet.py
   ```
2. Copy the generated `javascript:` bookmarklet code
3. Create a new bookmark in browser
4. Paste the code into the URL field

## Setup (iOS Safari)

1. Generate the bookmarklet code on desktop
2. Copy the entire `javascript:` line
3. On iPhone: Save any bookmark first (e.g., from any webpage)
4. Edit that bookmark: paste the javascript code into the URL field
5. Name it "Clip to Obsidian"
6. Navigate to any article in Safari, tap the bookmark to clip

## Usage

- Tap the bookmarklet while viewing any article
- Opens Obsidian with a new note containing:
  - Title, source URL, date clipped
  - Article content converted to markdown
  - Tags as configured in `generate-bookmarklet.py`

## Configuration

Edit settings in `~/wiki/scripts/generate-bookmarklet.py`:
- `VAULT` — vault name (leave empty for default)
- `FOLDER` — folder path inside vault (default: `Clippings/`)
- `TAGS` — comma-separated tags

## iOS Testing Status (Manual — Requires User)

**Status:** Setup guide complete. Manual testing required on iOS device.

### What to Test:
1. **iOS Safari bookmarklet** — Generate bookmarklet on desktop, copy JS, paste into bookmark URL on iPhone
2. **Obsidian URL scheme** — Confirm `obsidian://new` opens Obsidian app on iOS
3. **Full clip flow** — Navigate to article in Safari → tap bookmarklet → verify note created in Obsidian vault

### Test Commands (on iOS):
```
# Test if Obsidian handles the URL scheme
obsidian://new?vault=YourVaultName&content=Test%20Note
```

### Verification Checklist:
- [ ] Bookmarklet appears in Safari bookmarks bar on iOS
- [ ] Tapping bookmarklet triggers Obsidian to open
- [ ] New note contains: title, URL, date clipped, markdown content
- [ ] Tags are applied as configured in `generate-bookmarklet.py`

**Note:** This task requires Tuấn Anh to test manually on their iOS device. The setup documentation is complete.
