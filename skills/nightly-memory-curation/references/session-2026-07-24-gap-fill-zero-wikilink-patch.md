# 2026-07-24 02:00 — Gap-fill recovery: 36h vault staleness + 6 missing pages + 2 zero-wikilink patches

## Context

- **Run:** memory-curator cron 02:00 (heavy gap-fill)
- **Trigger:** 3-file staleness check fired
  - log.md: 36.9h stale
  - learned-about-tuananh.md: 36.8h stale
  - index.md: 8.5h stale
- **Step 0.5 set-diff:** wiki=88 concepts vs vault=197 (EXTRA 112 from historical accumulation) — 3 missing concepts; wiki=4 entities vs vault=7 (EXTRA 6) — 3 missing entities.
- **Sessions:** 1 user session (07-23 15:00 "Check OmniVoice repo", 337 messages) — no cron transcript (transcript-saver-v2 hooks not archived in raw/transcripts/2026-07-23).

## Root cause

The 07-22 main pass created 3 concept pages via watchdog (`gemma-4-toan-dien-2026-07-22`, `tiktok-script-lesson-from-ulanzi-clip-2026-07-21`, `voice-script-product-context-2026-07-21`) AND 3 entity pages (`2026-07-02-editor-s-ear-rework`, `capcut-cli`, `youtube-trending-gear-2026-06-28`) — but mirrored only the 3 always-mirror files. The 07-23 02:00 cron under-delivered (no log entry from that run). Compounded = 36h staleness.

This is the **L52/L54 pattern again** (third gap-fill miss in 5 days documented in 07-21 reference). The 3-file mtime check fires correctly but the scope-bounded-to-always-mirror miss is the dominant gap-fill failure mode.

## New lessons

### L57: Watchdog stub pages have ZERO wikilinks — patch before mirror

**Symptom:** 2 of 3 newly-created concept pages had 0 wikilinks in the body. The watchdog stub template does NOT auto-populate `## Related Concepts`.

**Detection:** Run `re.findall(r'\[\[([^\]]+)\]\]', content)` before declaring pages mirrored. If count < 2 → patch before mirror.

**Fix discipline:**
1. Wikilink count check on each new page
2. If < 2, add `## Related Concepts` section with ≥3 wikilinks to existing siblings
3. THEN mirror (so MD5 reflects the patched version)

**Verified 07-24:**
- `tiktok-script-lesson-from-ulanzi-clip-2026-07-21.md`: 0 → 6 wikilinks (added Related Concepts with [[tiktok-product-script]], [[content-creator-product-selling-yonex-astrox-2026-07-05]], [[body-mist-keep-plan-v4-2026-07-06]], [[hook-psychology-neuroscience]], [[psychology-viral-master-framework-2026]], [[learned-about-tuananh]])
- `voice-script-product-context-2026-07-21.md`: 0 → 4 wikilinks (added [[tiktok-product-script]], [[tiktok-script-lesson-from-ulanzi-clip-2026-07-21]], [[content-creator-project]], [[learned-about-tuananh]])

### L58: 9-file mirror is below threshold for mass-mirror script

**Symptom:** The `safe-mirror-set-diff.sh` script has a known bug: `mirror_dir` returns 0 (the OK count) but the caller assigns that to `TOTAL_OK` `$((TOTAL_OK + $?))`, so successful runs increment TOTAL_OK by the OK count while failed runs increment TOTAL_FAIL by the OK count. Total counters are misleading.

**Workaround for <10 files:** Inline Python loop with explicit `sleep 3` + `md5 -q` verify per file. For ≥10 files, use the script but verify totals manually.

**Verified 07-24:** 9 files mirrored in ~28 seconds (3s × 9 sleeps + cp overhead). All 9 verified first-try with 0 EAGAIN escalations. 3 always-mirror files passed `diff -q` byte-identical gate.

## Work done (chronological)

1. **Step 0 detection** — 3-file staleness check fires (all 3 stale)
2. **Step 0.5 set-diff** — 3 missing concepts + 3 missing entities
3. **Patch wikilinks** in 2 zero-wikilink pages (L57 fix)
4. **Mirror 9 files** with sequential `cp -f` + `sleep 3` + `md5 -q` per file
5. **diff -q final gate** on 3 always-mirror files → byte-identical
6. **Append curator entry** to wiki log.md (L51 ordering trap: append FIRST, mirror LAST)
7. **Re-mirror log.md** to reflect new entry
8. **5-question self-check** (L47 cron adversarial protocol) — PASS with disclaimer

## Lesson ordering recap (L1-L58)

| # | Date | Lesson |
|---|---|---|
| L55 | 2026-07-21 | set-diff > file-count subtraction |
| L56 | 2026-07-21 | silent cron under-delivery root cause |
| **L57** | **2026-07-24** | **zero-wikilink watchdog stubs need patch-before-mirror** |
| **L58** | **2026-07-24** | **9-file mirror is below mass-mirror script threshold** |

## Anti-patterns confirmed (no new ones, but these fired again)

- **L52 (07-21):** 3-file staleness check insufficient — confirmed this pass (still missed 6 pages).
- **L54 (07-21):** scope-bounded-to-always-mirror — confirmed this pass (3 pages + 3 entities mirrored technically but never actually copied).
- **L51 (07-16):** mirror-before-append ordering trap — AVOIDED this pass (append-then-mirror sequence followed).

## Self-check verdict (L47)

PASS (self-check, NOT adversarial — cron context, no subagent). All 9 files MD5 byte-identical, 3 always-mirror diff -q exit=0.
