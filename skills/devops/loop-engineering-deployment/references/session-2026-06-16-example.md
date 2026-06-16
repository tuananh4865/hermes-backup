# Session 2026-06-16 — First Loop Engineering Deployment

## Context
Tuấn Anh read Addy Osmani's "Loop Engineering" Substack essay (8 June 2026) and asked the agent to deploy the pattern system-wide on Hermes Agent.

## Trigger phrases from user
1. "anh muốn áp dụng ở quy mô hệ thống luôn để từ nay về sau toàn bộ hệ thống của hermes agent trên máy này sẽ hoạt động chính xác như vậy hoàn toàn tự động mà anh không cần phải nhắc lại nữa" → system-wide deployment
2. "từng bước từng file em làm em hãy lưu vào một file log về chủ đề này để khi cần có thê check logback lại được xem đã sửa và thay đổi những chỗ nào" → append-only changelog

## The 5 components planned
1. **quality-checker skill** — universal quality gate
2. **loop-goal primitive** — verifiable loop runner
3. **state file template** — `~/.hermes/workers/_template/state.md`
4. **gateway hook** — auto-invoke on agent:end
5. **wiki page** — `loop-engineering-system.md`

## What was actually created in this session

| File | Status | Notes |
|------|--------|-------|
| `~/.hermes/loop-engineering/CHANGELOG.md` | ✅ Created | INIT section logged |
| `~/.hermes/loop-engineering/changelog.jsonl` | ✅ Created | One JSON line |
| `~/.hermes/loop-engineering/log_helper.py` | ✅ Created | CLI + Python API |
| `/Volumes/Storage-1/Hermes/wiki/concepts/Loop-Engineering-System.md` | ✅ Created | Wiki mirror (after user said "cho log vào wiki nữa") |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/Loop-Engineering-System.md` | ✅ Created | iCloud Obsidian mirror |
| `/Volumes/Storage-1/Hermes/wiki/index.md` | ✅ Edited | Added `[[Loop-Engineering-System]]` to Hermes Agent section |
| `/Volumes/Storage-1/Hermes/wiki/log.md` | ✅ Edited | Appended entry for 2026-06-16 |

## Additional user signal during this session

3. "cho log vào wiki nữa" → user wants CHANGELOG mirrored to wiki, not just local file. Wiki must include navigation update (`index.md`) and log entry (`log.md`).
4. "báo cáo của em bị ngắt ở đoạn..." → user noticed the 5-component plan got truncated mid-sentence in Telegram. Future deployments with N>3 components must CHUNK reports into multiple messages, not deliver all at once.

## Steps NOT yet executed (deferred to future session)
- STEP-1: quality-checker skill
- STEP-2: loop-goal primitive
- STEP-3: state file template
- STEP-4: gateway hook
- STEP-5: wiki page
- E2E test
- Final report

## Lesson learned for future sessions
The user is comfortable with high-level architecture proposals but expects:
1. Changelog before any file change
2. Step-by-step execution with QA gates
3. Verifiable output, not just promises
4. Final report with what changed and where to verify

When in doubt: ask the user to confirm scope ("is this for one project or system-wide?") before deploying.

## New lesson (2026-06-16, mid-session): Critical-issue override in any checker/verifier

The first test run of `quality-checker` revealed a bug: a test case with banned words "mấy con vợ" 3x in a content-creator project scored 8.8 (would be WARN) and was being passed through. The pure score-based verdict was wrong because a critical issue (banned word in forbidden list) was masked by otherwise good scores.

**Fix:** `quality-checker` now has a `critical_override` rule — any issue with `severity: critical` → verdict = FAIL, regardless of score.

**Why this matters for ALL checkers/verifiers (code review, lint, content review, security scan):** Score measures quality. Severity measures safety. A passing score with a critical safety issue is still a fail. Critical issues are: banned words, missing required sections, fabricated data, security violations, broken contracts.

When designing any checker, include a critical-issue override. Score-based alone is too lenient on safety-relevant issues.

## New lesson (2026-06-16): Chrome ≥ 2026.x CDP WebSocket requires --remote-allow-origins

A separate sub-task tried to extract Chrome cookies via CDP for X/Twitter automation. The Python `websocket-client` got HTTP 403 on the WebSocket handshake because Chrome 2026.x blocks WebSocket connections from non-allowed origins.

**Fix:** launch Chrome with `--remote-allow-origins=*` (in addition to `--remote-debugging-port=9222`). Documented in the `browser-harness` skill's "Quick test" section.

**Worth knowing:** This is a Chrome security tightening, not a bug. The 403 message even tells you what flag to use. But `browser-harness --doctor` will still report "ok" because it uses HTTP `/json`, not WebSocket — so the bug is invisible from doctor output.
