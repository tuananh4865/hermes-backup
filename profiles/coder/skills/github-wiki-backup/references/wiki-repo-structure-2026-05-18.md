# Wiki Repo Structure Discovery — 2026-05-18

## Key Finding

**Local wiki sits INSIDE a parent git repo** — `.git` is at `/Volumes/Storage-1/Hermes/`, NOT inside `/Volumes/Storage-1/Hermes/wiki/`.

```bash
# This is the git repo ROOT (contains .git/)
/Volumes/Storage-1/Hermes/

# This is INSIDE that repo (wiki content)
/Volumes/Storage-1/Hermes/wiki/
```

**GitHub repo structure** (`my-llm-wiki`):
```
my-llm-wiki/           ← repo root = GitHub.com/tuananh4865/my-llm-wiki
├── .gitignore
├── hermes-agent-architecture.html
├── .hermes/            ← NOT tracked by local wiki git
├── memories/           ← NOT tracked by local wiki git
├── projects/           ← NOT tracked by local wiki git
├── scripts/            ← NOT tracked by local wiki git
├── skills/             ← NOT tracked by local wiki git
├── wiki/               ← Wiki content — maps to local /Volumes/Storage-1/Hermes/wiki/
│   ├── SCHEMA.md
│   ├── concepts/
│   ├── entities/
│   └── ...
└── workers/            ← NOT tracked by local wiki git
```

**GitHub API confirmed structure (2026-05-18):**
```bash
gh api repos/tuananh4865/my-llm-wiki/contents/
# Returns: .gitignore, .hermes, hermes-agent-architecture.html, memories, projects, scripts, skills, wiki, workers
```

## Critical Implication

Local wiki path `/Volumes/Storage-1/Hermes/wiki/` is tracked as `wiki/` subfolder in the GitHub repo. The local `.git/` is at the parent level, so:
- `git status` from `/Volumes/Storage-1/Hermes/wiki/` shows MODIFIED files in `wiki/` subfolder
- BUT: git commits from this location go to the parent repo, not a separate wiki repo
- GitHub's `wiki/` folder on main branch = local wiki content

## Browser Cannot Access Private Repo (Common Pitfall)

```bash
# This FAILS for private repos — browser requires login
browser_navigate("https://github.com/tuananh4865/my-llm-wiki")

# This WORKS — gh CLI uses stored auth credentials
gh api repos/tuananh4865/my-llm-wiki/contents/

# Workaround: Use gh cli instead of browser for private repo inspection
gh api repos/OWNER/REPO/contents/PATH
```

## Git Status Shows Only `log.md` Modified

```bash
cd /Volumes/Storage-1/Hermes/wiki && git status --short
# M log.md

# git ls-files shows 7588 files tracked (the wiki content)
```

## Cron Job for Wiki-Only Push

If Anh wants a cron that ONLY pushes wiki content (not parent .hermes, memories, etc.):
```bash
#!/bin/bash
# Push only wiki/ subfolder content
cd /Volumes/Storage-1/Hermes
git add wiki/ -f
git commit -m "Backup wiki: $(date +%Y-%m-%d)"
git push origin main
```

This respects the GitHub repo structure where `wiki/` is a subfolder, not root.