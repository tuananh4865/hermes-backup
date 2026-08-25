---
title: "Loop Engineering session 2026-06-16: Profile terminology + HERMES_HOME-aware"
date: 2026-06-16
author: Hermes Agent
session_type: full-deployment + redo
---

# Session 2026-06-16 — Loop Engineering Deployment (with Profile Redo)

## What was deployed

5-component Loop Engineering system (Maker→Checker→Orchestrator→User pipeline):

1. `quality-checker` skill — universal quality gate, 3/3 tests pass
2. `loop-goal` primitive — bash loop runner + Python AST condition parser, 6/6 tests pass
3. State template — at `~/.hermes/profiles/_template/state.md` (CORRECTED — was `workers/_template/`)
4. State helper — `profile_state.py`, HERMES_HOME-aware, 7/7 tests pass
5. Wiki page — `wiki/concepts/Loop-Engineering-System.md` (also mirrored to iCloud Obsidian)

Plus append-only changelog at `~/.hermes/loop-engineering/CHANGELOG.md` and JSONL.

## Key signal that fired user correction

User caught the wrong terminology: "trong hermes không hề có gì có tên gọi là worker hết! em lên github của hermes verify lại xem".

I had designed the state file path as `~/.hermes/workers/{name}/state.md` and used "worker" throughout all docs. The user was right — Hermes has only `Profile` (persistent) and `Sub-agent` (1-shot via `delegate_task`).

**Lesson encoded in skill:** The Skill's Component 3 path now says `~/.hermes/profiles/_template/state.md` and the body has a "Hermes Profile vs Worker" pitfall section.

## Verbatim quote from user (worker vs profile signal)

> "anh mới verify thấy trong hermes không hề có gì có tên gọi là worker hết! em lên github của hermes verify lại xem"

## Second signal: explicit logging preference

> "từng bước từng file em làm em hãy lưu vào một file log về chủ đề này để khi cần có thê check logback lại được xem đã sửa và thay đổi những chỗ nào"

→ Triggered the append-only changelog convention. Already in skill, but user explicitly validated it.

## Third signal: wiki mirror

> "cho log vào wiki nữa"

→ User wants changelog ALSO in wiki, not just local `~/.hermes/loop-engineering/CHANGELOG.md`. Skill's "Wiki-Mirror Requirement" section was added BEFORE this signal but is what made the response work.

## Test results

| Component | Test type | Result |
|-----------|-----------|--------|
| quality-checker | 3 cases (good/bad voice/no sources) | 3/3 pass |
| loop-goal | 6 cases (parser + CLI + loop + state) | 6/6 pass |
| profile_state | 7 cases (HERMES_HOME-aware, ensure, append, list) | 7/7 pass |
| **Total** | **16 cases** | **16/16 pass** |

## What went well

- Caught the worker→profile mistake in time (only 2 files were created with wrong terminology, rest were planned)
- Changelog format worked well — easy to grep, append-only, audit trail clear
- Wiki mirror caught user's exact need (they wanted it on Obsidian iOS)

## What to improve next time

- Default to `os.environ.get("HERMES_HOME", ...)` from the very first file, not retrofit it later
- Don't trust memory for canonical concepts — verify with `web_extract` or `mcp_exa` against `hermes-agent.nousresearch.com/docs/`
- Test scripts should default to tempdir, not production paths
