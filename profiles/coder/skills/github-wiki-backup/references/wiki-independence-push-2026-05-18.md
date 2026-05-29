# Wiki Independence Push — 2026-05-18

## Achievement
Successfully made wiki its own independent git repo and force-pushed to `my-llm-wiki`.

**Before:** Wiki was INSIDE parent repo at `/Volumes/Storage-1/Hermes/`. GitHub root had `.hermes/`, `memories/`, `workers/`, `projects/`, `scripts/`, `skills/`, `wiki/` — everything pushed together.

**After:** Wiki IS the repo. GitHub root has ONLY wiki content: `SCHEMA.md`, `index.md`, `log.md`, `concepts/`, `entities/`, `scripts/`, `skills/`, `projects/`, `queries/`, `references/`, `learning/`, `_meta/`, `auto-ingest/`, `outputs/`, etc.

## Files Changed
- `wiki_self_heal.py` — 3 patches (case sensitivity fix for `_safe_slug`, path separator handling, summary print)
- `~/.hermes/scripts/wiki_health.sh` — Full replacement with 2-phase cron (check + auto-fix)
- `/Volumes/Storage-1/Hermes/wiki/` — Fresh independent git repo init

## GitHub Verify Command
```bash
gh api repos/tuananh4865/my-llm-wiki/contents/ --jq '.[].name' | sort
# Confirmed: NO .hermes, memories, workers, projects, scripts, skills, wiki/
# Confirmed: YES — all wiki content folders at root level
```

## Key Lessons
1. Option A (independent repo) was chosen over Option B (subfolder sync)
2. Force push required because remote had old commits with parent folders
3. Wiki has ~7086 files (mostly stub pages created by self-heal)
4. 389 bad stubs exist from path-separator bug (still unfixed — not cleaned up)