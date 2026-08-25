# Reference Run — 2026-07-03 02:00 (Gap-Fill Mode — Broken-Promise Resolution)

> Companion to `session-2026-07-02-gap-fill-synthesis-pattern.md`. Read this when the previous curator run flagged a "broken-promise guard" (synthesis pages reference main-page stubs as "main page [[X]]" but X is still TODO), AND/OR when you're tempted to skip a no-new-content curator pass as a "noop."

## Why this run matters

This is the **first gap-fill run that resolved a broken-promise guard**. Previous gap-fill runs recovered vault staleness and resolved telegram-mirror duplicates — but the 2026-07-02 reference flagged a NEW class of gap: synthesis pages reference main-page stubs that were never filled. Leaving them as TODO creates a graph inconsistency — wikilinks to pages that say "[TODO]" instead of the synthesis the surrounding context implies exists.

## Inputs

- **Mode trigger (Step 0):** 3 always-mirror files stale on iCloud vault:
  - `log.md` — 21h behind wiki (last vault update: 2026-07-02 02:07; wiki: 2026-07-02 23:00)
  - `learned-about-tuananh.md` — 10h behind (07-02 02:07 vs 07-02 12:57)
  - `index.md` — 1h behind (07-02 02:08 vs 07-02 04:00)
- **No new raw transcripts since 2026-07-02 23:00** — the 07-02 02:00 gap-fill run had already captured the day's content (3 synthesis pages + 4 telegram-mirror merges).
- **Pending work item from 07-02 reflection:** Item 4 — "Fill 4 main-page synthesis stubs (15-25-45, 15-47-01, 17-14-22, 17-36-02) — the lessons are now in 3 synthesis pages, but the source-of-truth pages still say TODO"
- **876 watchdog stub backlog** at start — out of scope per SKILL.md "if >5 stubs" rule.

## Curator strategy: gap-fill + structural resolution

Two-track approach:

### Track A — Mirror recovery (always mandatory)

Standard 3-file mirror using the EAGAIN-safe `cp -f` + 3s sleep pattern. All 3 succeeded first-try, no escalation needed.

### Track B — Broken-promise resolution (conditional)

The 07-02 reflection left 4 main-page synthesis stubs as TODO. The 3 synthesis pages ([debug-loop-anti-pattern], [whisper-hallucinate-at-multi-range-concat], [script-use-mandate-system-wide]) all reference these as "main page [[X]]" in their `## Related Concepts` sections. The graph is currently inconsistent — wikilinks resolve to TODO pages.

The right fix is to **fill the 4 main pages** (not convert them to merged-into-main redirects). Why:
- Each of the 4 sessions has distinct, non-overlapping content that the synthesis pages summarize but don't fully replicate.
- The synthesis pages are umbrella concepts (meta-lessons). The main pages are session-specific evidence (concrete V_n → V_{n+1} trade tables).
- Converting to redirects would lose the per-session evidence trail — future agents debugging similar issues wouldn't be able to read the original V14 trade table or the per-segment audit discovery.

### Fill discipline applied (per `obsidian` skill § "Watchdog-processor auto-TODOs")

For each of the 4 pages:
1. Read the corresponding raw transcript (`raw/transcripts/2026-07-01/{timestamp}_20260701_*.md`) to extract concrete facts
2. Synthesize, not copy-paste (per the stub template's explicit rule)
3. ≥3 wikilinks to related concepts (achieved range: 7-9, well above minimum)
4. Replace the `## Summary`, `## Key Points`, `## Detailed Breakdown`, `## Examples`, `## Personal Notes` TODO blocks with 2+ sentences each
5. Add frontmatter `status: filled` + `filled_by: memory-curator 2026-07-03 02:00`

The fill produced:
- `15-25-45_20260701_cắt-lại-cho-đầy-đủ-nghĩa-thử-đọc-transcr.md` (4.9 KB, 9 wikilinks) — CONTENT INTEGRITY > ANTI-BIGRAM saga
- `15-47-01_20260701_edit-lại-từ-file-gốc-đi-em-cắt-cụt-hết-n.md` (5.4 KB, 8 wikilinks) — USP preservation saga + anh's "edit lại từ file gốc" reset signal
- `17-14-22_20260701_em-đang-chọn-seg-để-lấy-nhưng-em-không-c.md` (5.7 KB, 7 wikilinks) — per-segment content audit + Pitfall #85 origin
- `17-36-02_20260701_ủa-fix-kiểu-gì-vẫn-lỗi-vậy.md` (5.5 KB, 8 wikilinks) — iteration oscillation evidence (cleanest single piece)

## Wiki updates made

| Target | Action | Why |
|--------|--------|-----|
| `wiki/log.md` | Append curator entry (40 lines) | Daily summary + broken-promise resolution record |
| `wiki/entities/learned-about-tuananh.md` | Append L21-L23 section + Daily Recap for 07-03 (~80 lines) | 3 new lessons: gap-fill-as-default, broken-promise resolution, mirror reliability |
| `wiki/index.md` | Add 4 wikilinks (AI Agents → Psychology & Viral Content section) | Catalog newly-filled pages |
| `wiki/concepts/15-25-45_20260701_cắt-lại-cho-đầy-đủ-nghĩa-thử-đọc-transcr.md` | **FILLED** (TODO → synthesized, 9 wikilinks) | Broken-promise guard resolved |
| `wiki/concepts/15-47-01_20260701_edit-lại-từ-file-gốc-đi-em-cắt-cụt-hết-n.md` | **FILLED** (TODO → synthesized, 8 wikilinks) | Broken-promise guard resolved |
| `wiki/concepts/17-14-22_20260701_em-đang-chọn-seg-để-lấy-nhưng-em-không-c.md` | **FILLED** (TODO → synthesized, 7 wikilinks) | Broken-promise guard resolved |
| `wiki/concepts/17-36-02_20260701_ủa-fix-kiểu-gì-vẫn-lỗi-vậy.md` | **FILLED** (TODO → synthesized, 8 wikilinks) | Broken-promise guard resolved |

## iCloud mirror (EAGAIN-safe pattern, 7 files, first-try success)

```bash
VAULT="/Users/tuananh4865/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain"
WIKI="/Volumes/Storage-1/Hermes/wiki"

# Track A — always-mirror files (re-mirrored after edits)
sleep 3; cp -f "$WIKI/log.md" "$VAULT/log.md"
sleep 3; cp -f "$WIKI/entities/learned-about-tuananh.md" "$VAULT/learned-about-tuananh.md"
sleep 3; cp -f "$WIKI/index.md" "$VAULT/index.md"

# Track B — 4 newly-filled pages
sleep 3; cp -f "$WIKI/concepts/15-25-45_20260701_cắt-lại-cho-đầy-đủ-nghĩa-thử-đọc-transcr.md" "$VAULT/concepts/15-25-45_20260701_cắt-lại-cho-đầy-đủ-nghĩa-thử-đọc-transcr.md"
sleep 3; cp -f "$WIKI/concepts/15-47-01_20260701_edit-lại-từ-file-gốc-đi-em-cắt-cụt-hết-n.md" "$VAULT/concepts/15-47-01_20260701_edit-lại-từ-file-gốc-đi-em-cắt-cụt-hết-n.md"
sleep 3; cp -f "$WIKI/concepts/17-14-22_20260701_em-đang-chọn-seg-để-lấy-nhưng-em-không-c.md" "$VAULT/concepts/17-14-22_20260701_em-đang-chọn-seg-để-lấy-nhưng-em-không-c.md"
sleep 3; cp -f "$WIKI/concepts/17-36-02_20260701_ủa-fix-kiểu-gì-vẫn-lỗi-vậy.md" "$VAULT/concepts/17-36-02_20260701_ủa-fix-kiểu-gì-vẫn-lỗi-vậy.md"
```

**Verification gate (all PASS):**
```bash
diff -q "$WIKI/log.md" "$VAULT/log.md"                                # empty = identical
diff -q "$WIKI/entities/learned-about-tuananh.md" "$VAULT/learned-about-tuananh.md"  # empty
diff -q "$WIKI/index.md" "$VAULT/index.md"                            # empty
diff -q "$WIKI/concepts/15-25-45_*.md" "$VAULT/concepts/15-25-45_*.md"  # empty (×4)
```

## New lessons captured (L21-L23)

### L21 (NEW): Gap-fill runs are real curator value, not just maintenance

- 5th gap-fill in 11 days. The pattern is stable enough to be default, not exception handling.
- This run produced: (1) 21h vault staleness recovery, (2) broken-promise guard resolution (4 main-page fills).
- The Step 0 detection (3-file staleness check) has now caught gap-fill on 2026-06-25, 06-28, 06-29, 07-01, and 07-03 — 100% of gap-fill cases identified correctly, no false positives.
- **Lesson:** A "no new content" curator pass is not a no-op. The mirror + structural resolution work alone justify the cron fire.
- **Action item:** Codify gap-fill-as-default in SKILL.md (not just a fall-through in Step 0).

### L22 (NEW): Broken-promise guard anti-pattern resolved cleanly with 4-fill batch

- 4 main pages filled in a single curator pass — each sourced from the existing raw transcript, paraphrased per obsidian skill rule (no copy-paste from source).
- Each fill added 7-9 wikilinks to related concepts.
- **Synthesis-over-fill pattern (L22 reinforcement):** even though the 4 transcripts each became their own page (per the original synthesis-page plan from 07-02), the pages cross-link heavily to the synthesis pages that carry the meta-lessons. The graph stays connected both directions.
- **Why not redirect:** each main page contains unique session-specific evidence (V14 trade table, per-segment audit discovery) that the synthesis page summarizes but doesn't replicate.

### L23 (CONTINUING): The mirror step is now first-try reliable with sequential cp + 3s sleep

- 7 files mirrored in this run (3 always-mirror + 4 filled pages), zero EAGAIN errors, zero cat>tmp+mv escalations needed.
- Matches the 2026-07-01 batch mirror pattern (verified 7-file first-try success on 2026-07-01).
- The escalation patterns in the obsidian skill are still correct for the failure case (mid-day syncs, active editing on another device), but for 02:00 cron window when iCloud Drive is typically idle, sequential cp + sleep is the right default.

## Anti-patterns observed (negative signals for SKILL.md)

### 1. Bash heredoc with apostrophes in content fails with `unexpected EOF`

When using `bash <<'EOF' ... EOF` with content that contains apostrophes (e.g., *"em không hiểu"*, *Pitfall #84*), the bash parser fails with:

```
/bin/bash: eval: line 78: unexpected EOF while looking for matching `''
/bin/bash: eval: line 81: syntax error: unexpected end of file
```

**Fix pattern (verified working in this run):**
1. Write the multi-line content to `/tmp/{name}.md` using `write_file` (which uses no shell parsing)
2. Append to the target file using `cat /tmp/{name}.md >> "$TARGET_FILE"` (no heredoc, no shell expansion)

This worked first-try for both `log.md` (4.0 KB entry) and `learned-about-tuananh.md` (4.5 KB entry).

**Why this matters for curators:** log.md and entity pages are append-heavy. Heredoc is the natural bash idiom. The apostrophe failure means: any curator writing multi-line markdown with quoted user feedback will hit this. The fix is universal — write to /tmp first, then `cat >>`.

### 2. Step 0 detection pattern is over-relied on as a "boolean" — but the 3-file check is *continuous*

The current SKILL.md wording treats the 3-file check as a yes/no trigger ("ANY_STALE=1 → GAP-FILL"). But the actual value is the staleness *deltas* — they tell you how much work the run needs:
- log.md 21h stale = wiki has ~21h of session activity not in vault → full mirror recovery
- learned-about-tuananh.md 10h stale = entity page has ~10h of preference evolution not in vault → mirror recovery + possible new lessons
- index.md 1h stale = catalog has 1h of new pages not in vault → mirror recovery + add new entries

The deltas should be reported in the curator log entry so future runs can spot trends (e.g., "vault is consistently 5-10h behind wiki = iCloud sync is the bottleneck, not the curator").

## Final report (as returned to cron)

```
## 📊 Consolidation Report — 2026-07-03 02:00 +0700
- Mode: GAP-FILL (Step 0 3-file staleness check caught 21h/10h/1h vault gaps)
- Sessions consolidated: 0 (no new activity since 2026-07-02 22:53)
- Pages updated: 4 (broken-promise main-page synthesis stubs filled)
- New pages created: 0
- Pages catalogued in index.md: 4 (Psychology & Viral Content section)
- Cross-references added: 32 (7-9 wikilinks per filled page, all above 3-minimum bar)
- iCloud mirror: ✓ (all 7 files byte-identical via diff -q)
- Pending items resolved: 1 of 6 from 2026-07-02 reflection (item 4: fill 4 main-page synthesis stubs)
```

**Key finding:** This is a "no new content" gap-fill run — 5th gap-fill in 11 days. The value produced was structural, not new-capture: (1) recovered 21h of iCloud vault staleness across the 3 always-mirror files, (2) resolved the broken-promise guard by filling the 4 main-page synthesis stubs that [[debug-loop-anti-pattern]], [[whisper-hallucinate-at-multi-range-concat]], and [[script-use-mandate-system-wide]] all referenced but were still TODO. Without this resolution, the Obsidian graph would have shown dangling wikilinks for the next 24h+.

## When to use this reference

- A previous curator run flagged a "broken-promise guard" — synthesis pages reference main-page stubs as "main page [[X]]" but X is still TODO. This run's pattern (fill, don't redirect) is the fix.
- You're tempted to skip a no-new-content curator pass as a "noop." This run shows the value: 21h vault recovery + 4-page broken-promise resolution in 6 minutes of curator work.
- Step 0 detection fired with non-trivial staleness deltas — use this run as the reference for how to handle them (mirror recovery + structural resolution in one pass).
- You're writing multi-line markdown via bash heredoc and the content has apostrophes — use the `/tmp` write-then-cat pattern from this run's anti-pattern #1.