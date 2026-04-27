---
title: "GitHub Sync Setup"
created: 2026-04-08
updated: 2026-04-08
type: concept
tags: [obsidian, sync, github, setup]
---

# GitHub Sync Setup

## What We Did

Set up GitHub as the free sync backend for the wiki vault.

## Repo Created
- **URL:** https://github.com/tuananh4865/my-llm-wiki
- **Private** — only Anh can access

## Setup Components

### post-commit hook (auto-push)
Location: `.git/hooks/post-commit`
- After every commit, automatically pushes to GitHub
- No manual steps needed

### sync.sh
Location: `~/wiki/sync.sh`
- Manual sync script
- Commit all changes + push in one step

### .gitignore
Excludes: `.DS_Store`, `.obsidian/workspace.json`, `.obsidian/graph.json`, temp files

## How to Use

**On this Mac:**
- Any commit automatically pushes to GitHub
- To pull from another device: `cd ~/wiki && git pull`

**On other devices:**
```bash
# Clone once
git clone https://github.com/tuananh4865/my-llm-wiki.git ~/wiki

# Then open ~/wiki as an Obsidian vault
```

**On iOS:**
- Use Working Copy app to clone the repo
- Open in Obsidian

## Key Rules
- Don't edit the same note on multiple devices simultaneously — merge conflicts happen
- If conflicts occur: pull → resolve manually → commit → push
- Keep it simple and it works smoothly

## Status
✅ Complete — wiki synced to GitHub
