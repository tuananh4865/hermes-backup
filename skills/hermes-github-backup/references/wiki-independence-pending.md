# Wiki Independence: Cross-Skill Reference — 2026-05-18

## Context

Tuấn Anh approved Option A: Make wiki its own independent repo. This is a cross-skill operation.

## Operation Summary

**Problem:** Wiki at `/Volumes/Storage-1/Hermes/wiki/` is inside parent repo at `/Volumes/Storage-1/Hermes/`. Parent repo tracks `.hermes/`, `memories/`, `projects/`, `workers/`, etc. alongside wiki. Anh only wants wiki content pushed to GitHub.

**Solution:** Initialize fresh git in `wiki/` folder, set remote to `my-llm-wiki`, push independently.

## Cross-Skill Links

| Skill | Role |
|-------|------|
| `github-wiki-backup` | Primary skill — contains `references/wiki-independence-2026-05-18.md` with full procedure |
| `hermes-github-backup` | Updated — now points to `github-wiki-backup` for wiki independence operation |

## Operation Status

**Status**: PENDING EXECUTION — waiting for user confirmation to proceed.

**Files created/modified:**
- `github-wiki-backup/references/wiki-independence-2026-05-18.md` — NEW (2026-05-18)
- `github-wiki-backup/SKILL.md` — PATCHED (added Problem 4: Wiki sits inside parent git repo)
- `hermes-github-backup/SKILL.md` — PATCHED (updated Wiki Backup Architecture section)

## Key Facts

- `.git/` is at `/Volumes/Storage-1/Hermes/`, NOT in `wiki/`
- Wiki folder has NO `.git` of its own yet
- GitHub `my-llm-wiki` has `wiki/` as subfolder — after independence, wiki content will be at repo ROOT
- Parent repo at `/Volumes/Storage-1/Hermes/` continues to exist separately after separation