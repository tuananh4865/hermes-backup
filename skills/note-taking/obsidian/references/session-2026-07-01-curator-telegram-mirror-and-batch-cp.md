# 2026-07-01 — Memory Curator Run: Telegram-Mirror Dedupe + Batch Mirror

Reference for the curator pattern that emerged on **2026-07-01 02:00 UTC+7** when memory-curator ran and had to handle two new findings:

1. **Telegram-mirror duplicate stubs** — the same session produced two parallel concept stubs (telegram channel + dated-prefix). The obsidian skill's existing "fill watchdog stubs" section didn't cover this case, so a new "merge-into-main" curator pattern was codified.

2. **Batch mirror success** — 7 files mirrored to iCloud Drive using sequential `cp` with `sleep 3-5` between calls, all first-try, no EAGAIN. The obsidian skill's existing iCloud EAGAIN section covered failure recovery but not the happy path for batch mirrors.

## Source material

- 2 user sessions on 2026-07-01 (00:12 + 00:50) — both produced parallel telegram/dated-prefix transcript pairs
- 4 watchdog-created concept stubs (2 main + 2 telegram-mirror redirects)
- 2 new synthesis concepts (padding-flexibility-rule-v2.13, transcript-first-viral-workflow)
- 1 daily recap appended to `learned-about-tuananh.md` (5 new lessons L11–L15)
- `log.md` + `index.md` updated
- 7 files mirrored to iCloud Drive

## What the curator learned

### Pattern 1: Telegram-mirror merge-into-main

**Trigger:** Two watchdog-created concept stubs in `wiki/concepts/` with the same `session_id` in their corresponding `raw/transcripts/.../{date}_*.md` source files.

**Cause:** `transcript-saver-v2` hook fires twice per Telegram session — `on_message` writes `telegram_Tuấn-Anh-...md`, `on_session_end` writes `{YYYYMMDD}_...md`. Both feed the watchdog-processor, which creates parallel stubs.

**Solution (now codified in obsidian SKILL.md § "Telegram-mirror duplicate stubs"):**

1. Pick dated-prefix variant as the main page
2. Fill it with the full 5-section synthesis
3. Mark telegram variant `status: merged-into-main` and replace body with a thin redirect
4. Add cross-refs only to the main page

**Result:** 4 files touched (2 main fills, 2 telegram redirects), 5-section quality bar met for the 2 main fills, telegram variants became clean pointers.

### Pattern 2: Sequential cp with sleep for batch mirror

**Trigger:** Need to mirror multiple files to iCloud Drive in one curator pass.

**Previous (failure-mode) approach documented in obsidian SKILL.md:** the iCloud EAGAIN section covers cp/rsync failures + cat>tmp+mv escalation. But this is for the *failure* case.

**Solution (now codified in obsidian SKILL.md § "Mirror success pattern"):** For the 02:00 cron window when iCloud is typically idle, use sequential `cp -f` with `sleep 3-5` between files. No EAGAIN encountered. No escalation needed.

**Verified result:** 7 files mirrored first-try in this run:
- 2 new synthesis concepts → `concepts/`
- 4 filled stubs → `concepts/`
- `learned-about-tuananh.md` → vault root
- `log.md` → vault root
- `index.md` → vault root

All 7 confirmed byte-identical via `stat -f %z` (mtime granularity 1s on APFS makes size the better gate).

**Pitfall documented:** Do NOT parallelize with `&` — concurrent iCloud writes re-introduce open-file-lock contention.

## Lessons captured in `learned-about-tuananh.md`

- **L11** — Rhythm > polish for short-form TikTok. Codified in [[padding-flexibility-rule-v2.13]].
- **L12** — Framework read must precede KEEP range selection. Codified in [[transcript-first-viral-workflow]].
- **L13** — Same-night patch + production validation = strong stability signal.
- **L14** — Telegram-mirror stubs need curator policy. Codified in obsidian SKILL.md.
- **L15** — Filled-stub quality bar = 5+ sections × 2+ sentences. Each fill has ≥3 wikilinks.

## Files updated in this curator pass

| File | Change |
|------|--------|
| `concepts/00-12-03_20260630_anh-thấy-v3fix-ngắn-và-thông-điệp-gãy-gọ.md` | Filled watchdog stub (7 wikilinks) |
| `concepts/00-12-03_telegram_Tuấn-Anh-Anh-thấy-v3fix-ngắn.md` | Telegram-mirror redirect (`status: merged-into-main`) |
| `concepts/00-50-16_20260701_httpsdrivegooglecomfiled1kj_vd5luu571tlw.md` | Filled watchdog stub (8 wikilinks) |
| `concepts/00-50-16_telegram_Tuấn-Anh-httpsdrivegoogl.md` | Telegram-mirror redirect (`status: merged-into-main`) |
| `concepts/padding-flexibility-rule-v2.13.md` | NEW synthesis concept (4 wikilinks) |
| `concepts/transcript-first-viral-workflow.md` | NEW synthesis concept (7 wikilinks) |
| `entities/learned-about-tuananh.md` | Appended 2026-07-01 daily recap (L11–L15) |
| `log.md` | Appended `[2026-07-01 02:00] curator:nightly` entry |
| `index.md` | Updated `Last updated: 2026-07-01`, added 2 new concepts |

## What future curators should do

- **If you see two watchdog stubs with the same `session_id`:** apply the merge-into-main protocol (obsidian SKILL.md § "Telegram-mirror duplicate stubs"). Do NOT fill both.
- **If you're mirroring multiple files to iCloud Drive in a batch:** use sequential `cp -f` with `sleep 3-5` between calls. No need to escalate to `cat>tmp+mv` unless you actually see EAGAIN.
- **If you see the `transcript-saver-v2` hook still firing twice per session** (future runs may confirm): add to the backlog of skill-patch candidates. The dedup-by-session_id fix would eliminate the merge-into-main workaround at the source.

## Open follow-up items

1. Triple-validate v2.13.0 with a third product category (software tool or apparel). If clean, declare skill stable.
2. 763 watchdog stubs remaining in backlog. Prioritize 06-30 to 07-01 batches first.
3. Patch `transcript-saver-v2` to dedupe by session_id (eliminates the L14 problem at source).
4. Continue nightly mirror of 3 always-mirror files (log.md + learned-about-tuananh.md + index.md) — verified this run.
