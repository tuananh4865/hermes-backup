# Session 2026-07-07 — Standard mode (1-NEW-transcript) + MD5 mirror verification

**Mode:** STANDARD (synthesis work was completed 2026-07-06 02:00 by gap-fill curator; today's 02:00 cron only needed to handle the 1 NEW session that arrived after yesterday's run)

**Pre-pass state (3-file staleness check):**
- `log.md`: 0h stale (yesterday's curator wrote entry at 02:00, vault mirror at 02:06)
- `learned-about-tuananh.md`: 0h stale (L32-L34 added yesterday, mirror at 02:07)
- `index.md`: 0h stale (2 new synthesis entries added yesterday, mirror at 02:07)

**Detection logic outcome:** All 3 files in sync → not a gap-fill trigger. NEW transcripts exist (1 session in `raw/transcripts/2026-07-06/`) → not a noop. → **STANDARD mode** (this codifies a NEW mode distinct from the existing main/noop/gap-fill trichotomy in SKILL.md Step 0).

## Why STANDARD is a new mode (and not just "main pass")

The existing Step 0 table defines:
- **Main pass** — First cron of the night, OR >24h since last main pass
- **Noop** — no NEW content, no staleness
- **Gap-fill** — vault is stale OR pending work exists

The 2026-07-07 pass did NOT fit any of these cleanly:
- 02:00 cron of the night → matched "main pass" trigger
- But synthesis work was ALREADY done by yesterday's gap-fill (07-06 02:00 added 2 synthesis pages + 11 redirects)
- So running a "main pass" would manufacture synthesis pages from the 1 NEW transcript (wrong — too small a batch)
- It also didn't fit noop (NEW transcript arrived) or gap-fill (vault in sync)
- → Correct mode: **STANDARD** — synthesis done, only stub fills needed

**Recommendation for SKILL.md update:** Add STANDARD as a 4th mode in the Step 0 detection table. Trigger: vault in sync (≤2h stale) AND NEW transcripts exist (1-5 typical) AND yesterday's pass was a synthesis/gap-fill that already created the structural pages. Action: fill only the new stubs per `obsidian` skill watchdog-protocol + telegram-mirror dedup; do NOT manufacture new synthesis pages.

## What happened in this pass

1. **Staleness check (Step 0):** all 3 files in sync → STANDARD mode detected
2. **Discovery:** 1 NEW session in `raw/transcripts/2026-07-06/` (11:28 telegram, anh gửi App Store link + "Phân tích game này" → Top Heroes game analysis)
3. **Watchdog outputs:** 2 stub files in `wiki/concepts/` (dated-prefix main + telegram-mirror duplicate)
4. **Fill main stub** `concepts/11-28-28_20260706_httpsappsapplecomvnappthe1bb9di-c491.md`:
   - Full 5-section synthesis (Summary, Key Points, Detailed Breakdown, Examples, Related Concepts, Personal Notes)
   - 12 wikilinks to verified-existing pages
5. **Mark telegram-mirror** `concepts/11-28-28_telegram_Tuấn-Anh-httpsappsapple.md`:
   - Added `status: merged-into-main` to frontmatter
   - Body replaced with thin redirect
6. **Updated `index.md`**: 2 entries (body-mist-keep-plan-v4 acknowledgment + Top Heroes)
7. **Updated `log.md`**: +65 lines curator report
8. **Mirror to vault**: 4 files (log.md, index.md, 2 concept pages), sequential `cp` with `sleep 3-5`, no EAGAIN
9. **Verification:** MD5 byte-identical on all 4 files

## NEW lessons from this pass

### L35 — Wikilink destination validation (mandatory pre-write check)

**The mistake:** In the 07-07 Top Heroes fill, the first version of the synthesis page had 2 wikilinks to pages that don't exist:
- `[[droid-cli-research-2026]]` (no such file in `wiki/concepts/`)
- `[[tiktok-game-content-niche]]` (no such file)

**The catch:** After `write_file`, ran `ls /Volumes/Storage-1/Hermes/wiki/concepts/ | grep -E "droid.cli|tiktok.game|content.creator.project"` to verify the wikilink targets. Both wikilinks failed. Patched mid-run with `patch` tool to substitute valid alternatives (`20-57-07_telegram_tìm-hiểu-cho-anh-droid-cli` and `00-10-50_20260622_loại-bỏ-game-forest-wanderer-đi-tập-trun`).

**The rule:** Before writing a filled stub, validate every `[[wikilink]]` destination exists. Order of operations: (1) draft content, (2) list intended wikilinks, (3) `ls` each destination filename, (4) substitute non-existent ones with verified alternatives, (5) write file.

**Why this matters:** Broken wikilinks = dead graph edges. Obsidian graph view shows them as orphan links. Future agents searching for the linked concept get no hit. A "filled" stub with broken wikilinks has lower graph value than a "TODO" stub with no broken links (TODO stubs at least have correct links to the source `raw/transcripts/...`).

**Cost of catching mid-run vs pre-write:** 2 extra tool calls (the `ls` check + 2 `patch` calls). Cost of NOT catching: every future agent that follows the broken link wastes 1 search + 1 read call, then either fabricates a redirect or skips the link entirely. Pre-write validation scales better.

### L36 — MD5 as authoritative mirror verification, mtime is unreliable

**The discovery:** On the happy path (no EAGAIN), `cp -f` succeeds and sets the destination mtime to the *current write time*, not the source mtime. All 4 mirrored files in the 07-07 run had mtimes diverged by 16-48 seconds from source even though sizes matched perfectly and MD5s were byte-identical.

**Verification hierarchy (codified):**
1. **MD5 (`md5 -q src dst`) — AUTHORITATIVE.** Byte-identical = mirror succeeded. Use as final gate.
2. **Size match (`stat -f %z`) — fast pre-check.** Cheap to run on all files first; skip MD5 on any file that fails size check.
3. **Mtime match (`stat -f %Sm`) — UNRELIABLE for cross-process copies.** Only meaningful when both files were last touched by the same process in the same second (rare). For iCloud mirrors via `cp -f` from another filesystem, mtime will ALWAYS differ. Don't treat mtime mismatch as sync failure.

**Update to existing SKILL.md Step 5b:** The current text says "size is tiebreaker" when mtime granularity is 1s. This was correct in the 06-26 cat>tmp+mv context (where `mv` preserves source-tmp mtime), but for ordinary `cp -f` mirrors, the source mtime is never preserved. Replace "size is tiebreaker" with "MD5 is the final gate; size is the pre-check; mtime is unreliable for cross-process copies."

**Verification transcript (2026-07-07, representative):**
```
log.md:  size=476450 src/dst match, mtime diverged 16s, MD5=29081b04665664d421e2f0ae0e302e39 IDENTICAL
index.md: size=42563 src/dst match, mtime diverged 51s, MD5=4d19b922a77f2cd8636cbf6def84bd1a IDENTICAL
11-28-28 main: size=8274 src/dst match, mtime diverged 78s, MD5=6de67d7cb6848e47dac8e4954fdedfbb IDENTICAL
11-28-28 redirect: size=1629 src/dst match, mtime diverged 108s, MD5=90e7626b6d8af973435d222516a555a3 IDENTICAL
```

### L37 — 1-NEW-transcript policy (synthesis-over-fill for small batches)

**The pattern:** When STANDARD mode fires with exactly 1 NEW transcript, do NOT try to create a synthesis page. A single transcript IS the unit of work — fill its stub directly.

**Why this differs from synthesis-over-fill (L27):** L27 is the rule for ≥5 related transcripts sharing a single theme — create 1-3 synthesis pages + N merged-into-main redirects. The opposite case (1 transcript) doesn't share a theme with anything; the synthesis page IS the filled stub. Manufacturing a "synthesis page" for 1 source is the same anti-pattern as filling 5 individual stubs for 5 sources of a shared theme — wrong unit of work.

**Procedure for the 1-NEW-transcript case:**
1. Identify watchdog outputs: 1 dated-prefix stub + 1 telegram-mirror stub
2. Fill dated-prefix with full 5-section synthesis
3. Mark telegram-mirror as `status: merged-into-main` with thin redirect
4. Add 1 line to `index.md`
5. Add curator report entry to `log.md`
6. Mirror 4 files (log + index + 2 concept), MD5-verify

**Judgment range for 2-4 transcripts:** cluster by theme if a clear theme emerges, otherwise fill each separately. The "clear theme" test: would the synthesis page produce ≥5 unique wikilinks that none of the individual fills would produce? If yes, synthesize. If no, fill separately.

## Reflection on the 3-mode trichotomy evolution

The 07-07 run is the first documented STANDARD-mode pass. The 7 previous gap-fill runs in 13 days (06-25, 06-28, 06-29, 07-01, 07-03, 07-04, 07-06) showed that gap-fill was the dominant case for vault-staleness reasons, not content-volume reasons. The 07-07 STANDARD mode shows there's a third dimension: **content recency** (how much NEW content arrived since last pass) vs **vault staleness** (how far behind iCloud is).

Future curators should track all 3 dimensions in Step 0:
- **NEW content (N transcripts)**: 0, 1-4 (STANDARD), 5+ (MAIN or SYNTHESIS-AT-SCALE)
- **Vault staleness (h behind wiki)**: 0-2 (in sync), 2-6 (mild gap), 6+ (gap-fill mandatory)
- **Previous pass mode**: main / standard / gap-fill / noop (track in log entry so next pass can detect transitions)

The decision tree becomes:
- Vault >6h stale OR pending work → **GAP-FILL** (regardless of new content)
- Vault ≤2h stale AND 0 NEW transcripts → **NOOP**
- Vault ≤2h stale AND 1-4 NEW transcripts → **STANDARD** (fill stubs, no synthesis)
- Vault ≤2h stale AND 5+ NEW transcripts clustering in 1-2 themes → **MAIN with synthesis-over-fill**
- Vault ≤2h stale AND 5+ NEW transcripts with no clear theme → **MAIN with per-stub fill**

## Output stats (07-07 02:00)

- Mode: STANDARD
- Sessions consolidated: 1 (session `20260706_112734_1044e6f1`)
- Pages updated: 4 (1 main fill, 1 redirect, 1 index, 1 log)
- New pages created: 0
- Cross-references added: 17 (12 in main + 3 in redirect + 2 in index)
- iCloud mirror: ✓ (4/4 files MD5-identical)
- Mode transitions since 07-06 02:00: gap-fill → standard (first documented transition)

## Cross-references to other references

- `references/session-2026-07-06-gap-fill-pending-mirror-recovery.md` — The previous run that this STANDARD pass follows up on. Documents the synthesis work that 07-07 inherited as already-done.
- `references/session-2026-07-04-main-pass-synthesis-at-scale.md` — The MAIN pass worked example that defined the synthesis-over-fill pattern (L27). 07-07's STANDARD mode is the opposite end of the synthesis-over-fill spectrum (1 transcript → direct fill, not synthesis).
- `references/session-2026-07-03-gap-fill-broken-promise-resolution.md` — Documents the structural-resolution Track B that produces the synthesis pages this STANDARD pass inherited.
- `references/session-2026-07-01-curator-telegram-mirror-and-batch-cp.md` — The 07-01 reference that codified the telegram-mirror dedup pattern this pass applied.
