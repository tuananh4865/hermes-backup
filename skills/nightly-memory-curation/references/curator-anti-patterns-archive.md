# Curator Anti-Patterns Archive (L27, L36, L47, L50, L52-L56, L62, L70-L72)

Full text of curator anti-patterns extracted from `SKILL.md` to keep that file under the 100KB character limit. Future anti-patterns land here too. See `SKILL.md` for in-line anti-patterns through L27 (each one is short enough to keep inline).

---

## L72 — Initial-pass synthesis can undercount substantive sessions

When the first synthesis pass produces N concept pages, ALWAYS run a second `state.db` scan to count substantive (`message_count > 10`, source = telegram/subagent) sessions vs concept pages created. If substantive > concept pages by 2×, the pass likely missed something.

**Verified 2026-07-28 02:00:** first pass only saw 1 substantive session (7-clip V2, 193 msg) and created 2 synthesis pages; the second scan caught the 19-msg Huashu-Design recon session that needed its own concept page.

**Pattern:** re-scan `state.db` AFTER first synthesis round, BEFORE mirroring.

---

## L62 (predecessor) — Heavy single-session thread: don't transcribe everything

When the past 24h has exactly ONE heavy session (8h+, 100+ tool calls, Telegram still ongoing at cron fire time), resist the urge to read full transcript + extract every detail. Real value lives in: (a) anh's PUSH-BACKS (verbatim quotes from user turns that correct em's design), (b) KEY DECISIONS (anything that changed the implementation direction), (c) anh's MANDATES ("luôn", "bắt buộc", "chốt skill").

Synthesizing every test iteration, every "giờ anh gửi em voice mới để clone" cycle, every "Test thêm script" loop inflates concept pages with low-value noise that will be skipped by future agents.

**Verified 2026-07-25 02:00:** synthesized 276 messages / 117 tool calls into 4 concept pages (7272/4476/4800/4947 bytes) + L58-L61 — every page anchored on a specific push-back or mandate, no transcript transcription.

**Pattern:** for heavy ongoing sessions, build a "decision catalog" first (user-prompt → assistant-action → key-correction tuple) and ONLY synthesize the corrections, not the full arc. Verified 4 new pages × 3-7 wikilinks each × 5 lessons captured = the most efficient curator output per byte of session material to date.

---

## L70 — L-number collision check

When a curator run adds a new L-numbered lesson to `wiki/log.md` or `learned-about-tuananh.md`, the natural assumption is "the next number is free." Verified wrong 2026-07-27: assigned L65 (no-op protocol) → found existing L65 (workflow batch scalability from 2026-07-25 session) → renumbered to L68 → but L66 + L67 also existed (lặp câu bug + Mode B duration exception). The collision + renumber cycle cost 2 extra patches.

**Fix:** before writing any L-N reference, run:
```bash
grep -E "^\*\*L[0-9]+ \(" wiki/entities/learned-about-tuananh.md | \
  grep -oE "L[0-9]+" | sort -un
```
to find the highest existing L-number + scan the gap for any orphans. Then assign max+1. Apply this whenever proposing a new lesson in a curator log entry, an anti-pattern addition, or an SOUL.md update.

Pattern: L-numbers are the agent's serial numbering scheme for durable lessons; collisions corrupt the audit trail (future agents reading "L65" get one lesson, but it could be either of two).

---

## L52 / L54 / L55 (set-diff, scope-bounded, count-vs-set)

### L52/L54 — Scope-bounded-to-always-mirror

The 3-file mtime check is necessary but NOT sufficient. A previous pass can mirror the 3 always-mirror files (passes mtime check) but skip N concept/entity pages entirely. Verified 07-21: 07-19 main-pass created 43 concept pages + 3 entity pages but mirrored only the 3 always-mirror. The 07-20 cron under-delivered, leaving the N pages absent from vault.

**Detection:** after mtime check passes (or fires), run a set-diff against `wiki/concepts/`, `wiki/entities/`, `wiki/comparisons/`.

### L55 — Set-diff, not count subtraction

The vault can have STALE files no longer in wiki inflating its count. Verified 07-21: vault had 196 concept files vs wiki's 84, but the asymmetry was 43 wiki files missing from vault (the actual gap). The signal that matters is **asymmetric set membership (`comm -23 wiki_files vault_files`), not subtraction**.

A vault count that exceeds wiki count by N is NOT a "vault has more" signal — it's a "wiki has missing in vault" signal.

**Iterative set-diff (codified 2026-07-28):** each mirror round changes the set of vault files. Re-run set-diff AFTER each mirror round and after creating any new page.

**Pattern:** re-run set-diff at minimum 2 times per curator pass (pre-mirror and post-mirror) plus once after creating any new page.

---

## L50 — Bulk-injecting wikilinks into `relationships:` frontmatter via regex

Verified failure mode in main pass on 16 transcript files. The naive pattern:
```python
re.sub(r"(relationships: \[.*?)(\])", rf"\1, [[{concept}]]\2", content)
```
produces `relationships: [[[[learned-about-tuananh, [[concept]], [[next]], ...` — 3 opening brackets, 2 closing, YAML broken. Three follow-up fix attempts (non-greedy `.+?`, depth counter, `r"\[\[([^\[\]]+?)\]\]"`) ALL failed because the regex doesn't see the structural relationship between the YAML-list-opener `[` and the first wikilink-opener `[[`.

**The only reliable approach is FULL REBUILD from the authoritative body `## Related` section.**

**Verification gate:** after any bulk `relationships` patch, run `grep -c 'relationships:.*\[\[\[\[' <files>` and assert zero matches.

---

## L47 — Cron context can't dispatch adversarial verifier subagents

When a curator cron tries to call `delegate_task()` to verify its own work, it silently under-delivers. Mitigation for cron contexts is **5-question self-check** (from `adversarial-content-verifier` skill):
1. "What could be SAI that I haven't checked?"
2. "Independent evidence?"
3. "Self-check or 3rd party?"
4. "Output re-tested from independent source?"
5. "If anh tested right now, would it fail?"

Document the self-check result in the curator log entry as a NON-PASS disclaimer — "this is a self-check, not a strict adversarial PASS". Use the full subagent protocol in interactive sessions; use the self-check in cron contexts.

---

## L36 — MD5 as authoritative verification (vs unreliable mtime)

The `diff -q` gate above is correct but operates on the always-mirror files. For any NEW concept/redirect page mirrored in a curator pass, use `md5 -q` instead. Mtime is unreliable for cross-process copies — `cp -f` sets destination mtime to current write time, not source mtime, so mtime will always diverge by seconds.

**Verification hierarchy:**
1. **MD5 (`md5 -q src dst`) — AUTHORITATIVE.** Byte-identical = mirror succeeded.
2. **Size match (`stat -f %z`) — fast pre-check.** If sizes differ, MD5 will obviously differ.
3. **Mtime match (`stat -f "%Sm"`) — UNRELIABLE for cross-process copies.** Treat mtime divergence as expected, NOT as a failure signal.

**Verified 2026-07-07:** 4 mirrored files, all sizes matched, all MD5s byte-identical, all mtimes diverged by 16-108 seconds. Mtime match would have FALSELY flagged all 4 as out-of-sync.

**L59 (extends L53/L36) — MD5 EAGAIN fallback to cmp -s (macOS only):** macOS `md5` mmap's the file for performance, and mmap against an iCloud-locked inode returns EAGAIN. **Symptom:** md5 fails with `Resource deadlock avoided` (errno 35) in the verification step. **Fix:** fall back to `cmp -s "$src" "$dst"` (sequential read, no mmap). Returns exit 0 on match, 1 on mismatch. Do NOT skip verification — fall back, don't give up.

---

## L27 (predecessor, kept in SKILL.md) — synthesis-over-fill as DEFAULT

See SKILL.md § "Step 4. Update wiki pages" for the full text of L27 (kept inline because it's the core synthesis-over-fill decision tree).

---

**Index of all curator anti-patterns (in `SKILL.md` body through L27 + in this reference file from L36 forward):**

| L# | Location | Topic |
|----|----------|-------|
| L27 | SKILL.md inline | synthesis-over-fill as DEFAULT |
| L36 | this file | MD5 authoritative vs unreliable mtime |
| L47 | this file | cron context can't dispatch subagent |
| L50 | this file | YAML relationships corruption via regex |
| L52/L54 | this file | scope-bounded-to-always-mirror detection |
| L55 | this file | set-diff not count subtraction |
| L62 | this file | heavy single-session thread: don't transcribe |
| L70 | this file | L-number collision check |
| L72 | this file | initial-pass synthesis undercount |
| L74 | 2026-07-29 reference | iCloud vault root-listing 30s hang |
| L75 | 2026-07-29 reference | per-session extraction at N=2 |
| L77 | 2026-07-29 reference | junk `_test_*` file skew on set-diff |