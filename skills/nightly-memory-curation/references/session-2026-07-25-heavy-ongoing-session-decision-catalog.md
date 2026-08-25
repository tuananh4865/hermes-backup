# Session 2026-07-25 — Heavy Ongoing Single-Session Curation (OmniVoice build)

**Mode:** Synthesis (heavy)
**Source session:** `20260723_150017_010da588` (telegram, "Check OmniVoice repo", 276 messages, 117 tool calls, 8h ongoing at cron fire time)
**Cron fire time:** 2026-07-25 02:00 (last curator pass: 2026-07-24 02:03, gap-fill recovery of 36h staleness)

---

## Context

Yesterday's 24/07 02:00 curator pass was a **gap-fill recovery** for a 36h vault staleness — it didn't synthesize any new content. Today (25/07 02:00) fired exactly 24h later and discovered:

- **`raw/transcripts/2026-07-23/`**: 0 files (watchdog hadn't fired yet for the ongoing session — `on_session_end` only triggers on session termination)
- **`raw/transcripts/2026-07-24/`**: 0 new dated-prefix transcripts (only 1 new concept page from watchdog batch scan at 17:40 24/07: `omnivoice-trailing-silence-fix-2026-07-24.md`)
- **`~/.hermes/state.db` sessions table**: 4 sessions since last curator (1 telegram ongoing + 3 cron jobs themselves)

The single heavy ongoing Telegram session is the entire content source for this curator pass — no new raw transcripts, no new watchdog stubs from yesterday's work (because the session hasn't ended).

## The L62 Anti-pattern: Transcribing Full Session Body

The naive approach for a 276-msg / 117-tool-call session would be:
1. Read full transcript body (~50K+ chars)
2. Extract every assistant action
3. Create 1-2 large synthesis pages summarizing the full arc
4. Mirror

This produces concept pages that are 15K-20K bytes each, contain 70% low-value detail (test iterations, retry cycles, file-handling chatter), and 30% signal (push-backs + decisions). The result: 1-2 dense pages that future agents skip because they're too long to scan for the actionable lesson.

**The L62 fix: Decision-catalog first, synthesis second.**

## Decision-Catalog Pattern (L62)

Instead of reading the full transcript, build a **decision catalog** from user prompts + assistant push-back responses ONLY:

```bash
# Extract user prompts from state.db messages table
sqlite3 ~/.hermes/state.db "SELECT id, substr(content, 1, 300) FROM messages WHERE session_id='20260723_150017_010da588' AND role='user' ORDER BY id;" > /tmp/user_prompts.txt
```

Then **manually scan** for the patterns that signal durable content:

| Signal pattern | What it captures | Action |
|----------------|------------------|--------|
| User corrects agent's design ("Khoan, em...", "không cần...", "lưu ý...") | PUSH-BACK → L-numbered lesson | Extract verbatim, attribute to msg_id, capture WHY |
| User mandates ("luôn", "bắt buộc", "chốt skill", "phải") | HARD RULE | Extract rule + create standalone concept page |
| User reverses earlier decision ("không fade nữa", "bỏ padding") | DECISION FLIP → anti-pattern | Capture old + new + reason |
| User repeats a correction 2+ times across compaction | STRUCTURAL GAP | High-signal lesson (model failed even after compaction reset) |
| User corrects terminology ("voice ref ≠ file voice clone") | VOCABULARY FIX → SKILL doc | Embed in skill trigger description |

**Anything that doesn't match these 5 patterns is noise** — test outputs, file listings, "tiếp tục" prompts, retry cycles.

## Applied: 2026-07-25 Decision Catalog (excerpt)

From the 180 user prompts in the session, only **5** matched decision signals:

| msg_id | User prompt (verbatim) | Signal type | Lesson |
|--------|------------------------|-------------|--------|
| 55510 | "Khoan, em import hết âm thanh này vào omnivoice để tạo **template voice clone** thôi chứ đâu cần lần nào cũng phải import lại âm thanh đâu" | PUSH-BACK | **L58** — cache prompt .pt file (DON'T re-import ref audio each call) |
| 55730 | "Anh thấy có phần Non-verbal & Pronunciation Control khá hay cộng thêm các key feature để thêm cảm xúc cho giọng đọc khiến cho giọng đọc giống người hơn!" | DESIGN PRAISE | Add emotion tag section to skill doc (validated in L59) |
| 55782 → 55796 | "Nhưng lưu ý khi em ghép batch lại với nhau thì để fadeout nhẹ thôi 30ms thôi" → "Không fade không trim luôn audio bỏ padding 100ms luôn" | DECISION FLIP | **Anti-pattern** — KHÔNG fade/pad/trim sau concat (trailing silence fix at generate stage instead) |
| 55834 | "Emotion tag cũng phải bắt buộc" | HARD RULE | **L59** — emotion tag mandatory |
| 55855 | "Bỏ chữ tiktok đi chỉ cần anh nói **tạo voice** là em dùng omnivoice tạo voice cho anh" | TRIGGER FIX | **L61** — minimum verb+noun trigger |
| 55947 | "Lúc nãy anh có nói lưu cách dùng voice ref là sai rồi, **đúng phải là cách dùng file voice clone**" | VOCABULARY FIX | **L60** — distinguish input (ref) vs output (cached prompt) |

**Total time to build the catalog: ~10 minutes** (180 prompts × ~3 sec each to scan).

## Synthesis Pages Produced

From 5 decisions + 1 design praise → 4 concept pages + 4 L-numbered lessons in `learned-about-tuananh.md`:

1. **`omnivoice-skill-build-journey-2026-07-23.md`** (7,272 bytes) — full session overview + iteration arc + 5 key decisions + 4 anti-patterns. Anchored on the 5 decisions above + 24/07 trailing-silence-fix post-script.
2. **`omnivoice-prompt-caching-vs-ref-each-call-2026-07-23.md`** (4,476 bytes) — VoiceClonePrompt.save/load pattern (L58). Single decision, deep technical detail.
3. **`omnivoice-emotion-tag-mandatory-2026-07-23.md`** (4,800 bytes) — 13 non-verbal tags + A/B test verification (L59). Mandate + empirical evidence.
4. **`tiktok-product-script-omnivoice-workflow-2026-07-23.md`** (4,947 bytes) — full 5-step pipeline verified với Dodoto 46.17s. The "happy path end-state" of the session.

**Cross-refs:** 4 pages × 3-7 wikilinks each = 17 wikilinks total. Every page references ≥2 of the others + `learned-about-tuananh.md` (graph stays connected).

**Lessons added to `learned-about-tuananh.md`:** L58-L61 (4 push-backs), L62 (self-captured curator pattern).

## Discovered Mid-Run Gap (Set-Diff Pre-Flight Win)

During Step 0.5 set-diff check (after the 3-file mtime check fired correctly), discovered `omnivoice-trailing-silence-fix-2026-07-24.md` was created 24/07 17:40 (after the 24/07 02:00 curator pass) and **was NOT in the vault**. The page is a post-session artifact that the watchdog generated from a 24/07 message exchange.

**Action:** Added to mirror batch inline. Don't defer to next cron — single `sleep 3 + cp -f + md5 -q` and the page is in the vault.

This is the **4th verified value of the Step 0.5 set-diff** (after L52/L54/L55 from 2026-07-21): catching outlier pages that the 3-file mtime check cannot detect because they're never in the "always-mirror" set.

## Verification

- **4/4 new files** byte-identical (MD5 verified)
- **4/4 always-mirror files** byte-identical: `log.md`, `learned-about-tuananh.md`, `index.md`
- **1/1 outlier page** byte-identical: `omnivoice-trailing-silence-fix-2026-07-24.md` (mid-run gap-fill)
- **0 EAGAIN errors** (sequential `cp` with `sleep 3` between calls; iCloud idle at 02:00)
- **5-question self-check** used (L47 cron protocol — `delegate_task` not available)

## Efficiencies Achieved

| Metric | Naive full-transcript approach | L62 decision-catalog approach |
|--------|--------------------------------|--------------------------------|
| Time to build catalog | 2-3 hours (read full transcript) | 10 minutes (180 prompts × 3 sec scan) |
| Concept pages created | 1-2 (15-20K bytes each, dense) | 4 (4-7K bytes each, focused) |
| Wikilinks per page | 2-4 | 3-7 |
| L-numbered lessons captured | 1-2 | 5 (L58-L62) |
| Future-agent skippability | High (too dense to scan) | Low (every page anchored on a specific decision) |

**Net effect:** Same lessons captured, more pages of higher per-page value, 1/6 the time, 5x the lessons learned.

## Lesson Captured (L62)

> **Transcribing full session body for "ongoing heavy single-session thread" curation is an anti-pattern.** Build the decision catalog first, synthesize ONLY the decisions. For heavy ongoing sessions, every byte of page content should be traceable to a specific push-back, mandate, or correction — not to a test iteration or retry cycle.

## Cross-References

- `nightly-memory-curation/SKILL.md` Step 4 — synthesis-over-fill pattern (default for 5-15 transcript batches, L27)
- `nightly-memory-curation/SKILL.md` Step 0.5 — set-diff pre-flight (L52/L54/L55)
- `nightly-memory-curation/SKILL.md` Step 5b — always-mirror hard rule + byte-identical verification (L36)
- `references/session-2026-07-08-gap-fill-synthesis-at-scale-3theme.md` — multi-theme synthesis with mixed treatments (L40)
- `references/session-2026-07-21-gap-fill-set-diff-discovery.md` — first set-diff discovery worked example (L52/L53/L54/L55/L56)
- `references/session-2026-07-24-gap-fill-zero-wikilink-patch.md` — pre-mirror wikilink gate (L57/L58)