# Wiki Repo Flattening — 2026-05-08

## The Problem

GitHub repo showed `wiki/concepts/`, `wiki/entities/` etc. — user wanted content at root: `concepts/`, `entities/` directly.

User said: "anh chỉ muốn git repo chứa những gì bên trong thư mục wiki thôi"

## Resolution: Flatten the Repo

```bash
#!/bin/bash
# Clone fresh, flatten, force push

cd /tmp
rm -rf my-llm-wiki-flat
git clone https://github.com/tuananh4865/my-llm-wiki.git my-llm-wiki-flat
cd my-llm-wiki-flat

# Move wiki/* to root
mv wiki/* .
mv wiki/.* . 2>/dev/null
rm -rf wiki

# Remove non-wiki artifacts (test outputs, cache, etc.)
rm -rf test-agent-output outputs .pytest_cache
rm -f *.bak log.md.tmp

# Clean and push
git add -A
git commit -m "Flatten: move wiki/* to root"
git push origin main --force
```

## Key Signals

| Signal | Meaning |
|--------|---------|
| GitHub shows `wiki/` folder wrapping content | Repo structure is wrong — content should be at root |
| "Commit những gì bên trong thư mục wiki thôi" | User wants flat structure, not nested |

## Flat Structure (Correct)

```
my-llm-wiki/
├── concepts/     ✅
├── entities/     ✅
├── raw/          ✅
├── SCHEMA.md     ✅
├── index.md      ✅
└── log.md        ✅
```

## Nested Structure (Wrong — what we had before)

```
my-llm-wiki/
└── wiki/         ❌ Too deep
    ├── concepts/
    ├── entities/
    └── ...
```

## After Flattening

- 4351 files changed, 48765 deletions
- `wiki/` folder no longer exists in repo
- Content now at root level
- Force push was required because old structure diverged from new

## Verification

```bash
# Check GitHub web UI — should see concepts/, entities/ at root, NOT inside wiki/
gh repo view tuananh4865/my-llm-wiki --web

# From local clone:
ls -la  # Should show concepts/, entities/ directly, no wiki/ wrapper
```
