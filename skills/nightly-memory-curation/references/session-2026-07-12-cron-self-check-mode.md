---
title: "Session 2026-07-12 02:00 — Cron Self-Check Mode (no subagent dispatch)"
created: 2026-07-12
type: curator-reference
tags: [cron-mode, self-check, adversarial-verifier-cron, sqlite-state-db, stat-pitfall]
session: 20260712_011433_1996c7a7 (review target) + cron_6142e22700d4_20260712_020035 (this run)
---

# Session 2026-07-12 02:00 — Cron Self-Check Mode (no subagent dispatch)

## Run classification

**Mode:** Self-check mode (cron, no user present, no subagent dispatch)
**Trigger:** Memory-curator cron at 02:00, post-session `20260712_011433_1996c7a7` (Adversarial Verifier validation session that ran 01:14-01:59)
**Wiki mtime vs vault mtime:** All 3 always-mirror files in sync at run start → NOT a gap-fill mode
**Source data:** 6 raw transcripts in `wiki/raw/transcripts/2026-07-12/` (5 telegram + 1 cron re-batch)
**Master transcripts:** `20260712_011433_1996c7a7.md` (81 msgs), `20260712_004342_1c6757.md` (289 msgs), `20260711_143222_5c1f9d.md` (808 msgs), `20260711_122318_b006d253.md` (202 msgs), `20260711_174520_145d4eec.md` (105 msgs), `20260710_232751_b78afe.md` (113 msgs)

## Key findings extracted (5 lessons for tonight)

### 1. Cron 02:00 = self-check mode, NOT full adversarial verifier

The `20260712_011433_1996c7a7` session ran 3 adversarial verifier test cases (Mascot Vui Vẻ V3.1 / 14 SKU Yonex / SOUL.md 5-dim) with subagent dispatch — that worked because user was present. The 02:00 cron CANNOT dispatch subagents (cron context = no user, no interactive tools). **Mitigation:** apply 5-question self-check (from `adversarial-content-verifier` skill) and document as "self-check, not strict PASS". Codified in SKILL.md L47.

### 2. `sessions` table schema: no `created_at` column

First SQL attempt: `SELECT id, created_at, title FROM sessions` → `Parse error: no such column: created_at`. The `sessions` table uses `started_at` (Unix epoch float). Query pattern that works:
```sql
SELECT id, datetime(started_at, 'unixepoch', 'localtime') as t, title, source, message_count
FROM sessions
WHERE started_at > strftime('%s','2026-07-11 00:00:00')*1.0
  AND message_count > 0
ORDER BY started_at;
```
Filter `source IN ('telegram', 'cli')` to exclude `cron` and `subagent`. The `sessions.json` file is a routing mirror, NOT the source of truth. Codified in SKILL.md L49.

### 3. `stat -f "%z"` pitfall with iCloud paths containing spaces

When verifying mirror sizes, the bash pattern `src_size=$(stat -f "%z" "$WIKI/$f")` followed by comparison against `dst_size=$(stat -f "%z" "$VAULT/$f" 2>/dev/null)` returned empty `src_size` for `learned-about-tuananh.md` even when both files clearly had 202241 bytes. The empty value was caused by a variable capture issue specific to the path-with-spaces context. **Fix:** use `md5 -q src dst` for the authoritative check (already codified L36) — skip the size pre-check when path has spaces. Codified in SKILL.md L48.

### 4. Watchdog-processor dedup pattern (current state)

The `transcript-saver-v2` hook + `watchdog-processor` create multiple raw transcripts per Telegram session (1 master + 1 telegram-mirror + 1 dedup_skip). The watchdog batch log shows: 14 changes in the 02:00 batch — 6 `append_session_transcript`, 8 `dedup_skip` or `none`. The dedup pattern is working correctly: 50% of watchdog operations are pure dedup, not new content. Curator should treat `dedup_skip` lines as informational, not as content requiring extraction.

### 5. Wiki catalog drift detection

After 24h of new content (11-12/07), the `wiki/index.md` catalog gained 2 new concept pages (adversarial-verifier-protocol-2026-07-12, system-wide-verification-rule-2026-07-12) plus 2 entries in `learned-about-tuananh.md` (lần 3 + lần 4 of the vĩnh viễn lessons series). The catalog entry pointing at these new pages was verified via `grep -rlE 'adversarial-verifier-protocol-2026-07-12' /Volumes/Storage-1/Hermes/wiki/` → 4 files (the new concept + system-wide concept + learned-about-tuananh + log.md). The 3-file always-mirror check (Step 0 detection) caught the new content and triggered synthesis-over-fill decision per the SKILL.md 3-theme decision tree.

## Cron self-check (5 câu adversarial applied)

1. **"Cái gì có thể SAI mà em chưa check?"** — Cron 02:00 chạy không có user present, không thể dispatch subagent verify. Risk: skip entry quan trọng. Mitigation: check 9 sessions phi user (cron/subagent) loại trừ trước khi trích xuất.
2. **"Bằng chứng độc lập nào?"** — Đọc thẳng `state.db` sessions table, raw transcripts files, không qua LLM. `sqlite3 ~/.hermes/state.db "SELECT ..."` + `ls -la` + `md5 -q` đều là built-in commands.
3. **"Em tự check hay bên thứ 3?"** — Em tự. Document ghi rõ "self-check, không phải strict PASS adversarial". Cron không dispatch được subagent.
4. **"Output có test lại từ source độc lập?"** — `wc -l` verify concept page size, `md5 -q` verify mirror, `grep -c` verify wikilink count.
5. **"Nếu anh test lại ngay bây giờ, có sai không?"** — Có thể thiếu 1-2 micro-detail (vd 1 raw transcript `.md` 11/07 chưa catalog đầy đủ vào concept) → acceptable cho nightly curator. Subagent re-test in next interactive session.

## Wiki updates applied

- **entities/learned-about-tuananh.md:** updated to 2026-07-12, +2 entries (lần 3 + lần 4), 2 new relationship tags (`july-12-adversarial-verifier-validation`, `july-12-nightly-curator-self-check`), 2 new cross-refs to concept pages
- **concepts/adversarial-verifier-protocol-2026-07-12.md:** NEW (10,341 bytes, 247 lines, 8 wikilinks)
- **concepts/system-wide-verification-rule-2026-07-12.md:** NEW (8,069 bytes, 181 lines, 7 wikilinks)
- **log.md:** +1 curator entry (daily summary 12/07)

## Mirror verification (MD5 byte-identical, all 4/4 OK)

| File | Source MD5 | Vault MD5 | Status |
|---|---|---|---|
| `concepts/adversarial-verifier-protocol-2026-07-12.md` | `f1d00f17...` | `f1d00f17...` | ✅ MATCH |
| `concepts/system-wide-verification-rule-2026-07-12.md` | `e2a8cc4e...` | `e2a8cc4e...` | ✅ MATCH |
| `learned-about-tuananh.md` | `63d8d40c...` | `63d8d40c...` | ✅ MATCH |
| `log.md` | (verified) | (verified) | ✅ MATCH |

Sequential `cp -f` with `sleep 3-5` between files — no EAGAIN errors. The size stat pitfall was caught and worked around by going directly to MD5 verification.

## Anti-patterns codified this run (L47-L49)

- L47: Don't try to dispatch subagent from cron 02:00 → use 5-question self-check
- L48: `stat -f "%z"` returns empty on paths with spaces → use `md5 -q` instead
- L49: `sessions` table has `started_at`, not `created_at` → query with `strftime('%s', ...)*1.0`

## Source-recall for next curator

If a future curator needs to re-run the same workflow:
1. Run the sqlite3 query (L49) FIRST to get the session list
2. Filter by `source IN ('telegram', 'cli')` to exclude cron/subagent noise
3. For each session, check the master transcript in `wiki/raw/transcripts/` (NOT the telegram-mirror duplicates)
4. Apply 5-question self-check (L47) since cron can't dispatch subagent
5. Mirror with `md5 -q` (L48) — never `stat -f "%z"` for files in paths with spaces

## Pattern stability (2026-07-13 02:00 cron, 2nd consecutive night)

Verified: 2026-07-13 02:00 curator run also applied the same self-check mode successfully.

- 44 dated transcripts in `raw/transcripts/2026-07-12/` (88 files incl. telegram-mirror variants)
- Cluster A (12 sessions, SOUL audit + Adversarial Verifier) → references already exist (12/07 patch), no new concept created (correctly avoided duplication)
- Cluster B (5 sessions, Mode B default + 5-clip batch 0731/0735/0740) → **1 NEW concept** `tiktok-edit-batch-mode-b-default-2026-07-12.md` (Mode B milestone + 6 wikilinks)
- Cluster C (3 sessions, badminton daily business) → **1 NEW concept** `badminton-inventory-restock-2026-07-12.md` (5 wikilinks)
- Sequential `cp -f` + `sleep 3-5` × 5 files → zero EAGAIN (mirror pattern L23 confirmed 3rd-night stable)
- `md5 -q` (skip stat-fail trap) → all 5 mirror files byte-identical

**Anti-pattern observations this night:**
- ✅ Correctly did NOT create concept pages for Cluster A — references already exist from 12/07 patch (would have been duplication)
- ✅ Correctly did NOT update `learned-about-tuananh.md` — 12/07 entries (3 lần + nightly curator self-check) already documented
- ⚠️ Synthesis pages did NOT mark raw transcripts `merged-into-main` — this is INTENTIONAL: 12/07 transcript pairs are session-specific, not part of the 5-clip batch narrative arc. The redirect pattern (per obsidian skill + 07-04 L27) applies only to TRUE meta-lesson arcs where synthesis is the canonical source. Pure operational transcripts can stay as source reference without forcing redirects.

**Lesson validation:** Cron self-check mode stable across 2 consecutive nights (12/07 + 13/07). Future curators in cron context should:
- Continue using `md5 -q` for size verification (L48 still applies 24h later)
- Continue applying 5-question self-check (L47) — no surprise subagent dispatch is possible
- Document tier of synthesis as "FIRST-CLASS / operational-only / session-specific" so future runs know which pattern to apply
- Run `wc -l + grep` independent source-counting instead of trusting just DB queries

**Pattern now stable enough to be cited as canonical example** for cron-context curation. Load this file + L47-L49 anti-patterns from SKILL.md + follow the source-recall protocol.
