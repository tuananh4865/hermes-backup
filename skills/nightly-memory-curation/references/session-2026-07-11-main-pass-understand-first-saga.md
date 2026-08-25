# Session 2026-07-11 02:00 — Main Pass: UNDERSTAND-FIRST → 7 Key Insights Synthesis (10 transcripts → 1 page)

**Curator mode:** MAIN PASS (60 NEW transcripts Jul 10 + 3 always-mirror files all 25-46h stale)

## Staleness state on entry

| File | Stale by | Resolution |
|------|---------:|------------|
| `log.md` | 45h52m | Mirror recovered |
| `learned-about-tuananh.md` | 45h3m | Mirror recovered |
| `index.md` | 25h53m | Mirror recovered |

This is the 9th day since the last full main pass. Vault staleness across all 3 always-mirror files = canonical gap-fill signal.

## Theme clustering

Today's transcripts split cleanly into 5 buckets:

| Theme | Transcripts | Treatment |
|-------|-------------|-----------|
| UNDERSTAND-FIRST → 7 Key Insights saga (tiktok-video-editor v3.19.0 → v3.20.0) | 10 (22:11, 22:27, 22:30, 22:35, 22:39, 22:46, 22:58, 23:10, 23:19, 23:42) | **NEW synthesis page** |
| Badminton hot shorts research (21:57 + 22:02 subagent batch) | 2 | Operational → link to existing [[badminton-trend-research-2026-w26]] |
| YouTube Shorts downloads + Smash-Hub text removal (15:07-15:40) | 5 | Operational → existing skills cover |
| Worktree mandate setup (10:33 + 10:08 subagent) | 2 | Already codified in [[folder-worktree-convention]] skill (`references/outputs-worktree-2026-07-10.md`) |
| Cleanup batch + concept-stub cleanup (00:14, 11:20) | 2 | Operational |

## The synthesis-over-fill decision (10 transcripts → 1 page)

**Decision: 1 synthesis page + 0 stub redirects** (no watchdog stubs existed yet for these Jul 10 sessions — first curator pass on this batch).

The 10-transcript UNDERSTAND-FIRST saga:
- 22:11 (trigger) → 22:27 (mandate) → 22:30 (hard call-out) → 22:35 (skill rewrite v3.19.1) → 22:39 (verify) → 22:46 (first test fail) → 22:58 (side-by-side) → 23:10 (deep analysis → 7 KEY INSIGHTS) → 23:19 (validation clip 0705, FIRST TIME em ≤ anh) → 23:42 (7-clip batch accepted)

→ [[tiktok-video-editor-v3.19-v3.20-understand-first-7-insights-2026-07-10]] (25.7 KB, 20 unique wikilinks: 10 to raw transcripts + 10 to existing concept pages)

**This is the 5th-verified case of synthesis-over-fill scaling** (after 07-01, 07-02, 07-04, 07-08). Confirms the pattern works at 10-transcript batch size — between the smaller 7-transcript case and the larger 22-transcript case.

## New L45 lesson: UNDERSTAND-FIRST is the 2nd recurring "rule-based ≠ understand-based" instance

Codified in `learned-about-tuananh.md` 2026-07-11 02:00 reflection section:

**Meta-pattern (3rd iteration, verifiable timeline):**
- 2026-07-02: editor's-ear-rework (V1.6 → V2.37 over-engineering) — too many rules obscured judgment
- 2026-07-08: mode-a-over-completion (V3.16 rule-bypass fix) — rule layer didn't prevent over-cut
- 2026-07-10: UNDERSTAND-FIRST (v3.19.0 → v3.19.1) — agent applied rules without reading narrative

**Pattern:** Each rule layer accumulates, but the bottom layer (read + understand + judge) can never be fully procedural. The antidote is forced read-first verification at every level.

## New methodology captured: Source-recall + beat-by-beat comparison

Anh's pivotal instruction at 23:10: *"Anh cần em phân tích sâu hơn xem anh đã làm gì và em đã làm gì, khác nhau chỗ nào, cách làm của anh là gì? Từ đó đưa ra được các key quan trọng để thay đổi và update cho skill"*

**The methodology that produced v3.20.0's 7 KEY INSIGHTS:**
1. Pick 1 source clip with 2 versions (anh's manual edit + agent's auto-cut)
2. Beat-by-beat comparison of the 2 versions
3. Identify what anh kept that agent dropped (the diff)
4. Extract durable insights from the diff (7 in this case)
5. Encode as procedural rules with self-check questions

This is the 3rd skill-upgrade methodology type after Transcript-First (v2.13.0) and UNDERSTAND-FIRST (v3.19.1). Each adds a NEW mandatory stage that cannot be procedural-skipped:

| Methodology | Stage added | Trigger | Hardness |
|-------------|-------------|---------|----------|
| Transcript-First (v2.13.0) | Read framework skill BEFORE selecting KEEP | "em edit không ưng" | Hard rule |
| UNDERSTAND-FIRST (v3.19.1) | Read full transcript + answer 5 narrative questions | "em không hiểu được nội dung clip" | Hard rule |
| Source-recall + beat-by-beat (v3.20.0) | When stuck, deep-compare 2 versions, extract diff as insights | "phân tích sâu hơn xem anh đã làm gì và em đã làm gì" | Methodology |

## Operational handling (5 themes correctly skipped as synthesis-worthy)

The pattern from SKILL.md §4 step-3 ("Operational transcripts vs synthesis-worthy transcripts") worked correctly today. All 5 operational categories linked to existing pages/skills instead of creating new synthesis pages:

- **Badminton research** → existing [[badminton-trend-research-2026-w26]] (07-03 curator synthesis)
- **YT Shorts downloads** → existing [[telegram-video-20mb-limit]] (06-24 lesson)
- **Smash-Hub text removal** → ffmpeg filter pattern (no synthesis needed)
- **Worktree mandate** → already in [[folder-worktree-convention]] skill `references/outputs-worktree-2026-07-10.md`
- **Cleanup batch** → operational, no synthesis

**Lesson reinforcement:** Don't manufacture synthesis pages for operational work. The 5-evidence-gate test ("would filling produce ≥2 unique wikilinks + new meta-lesson?") passed all 5 operational categories correctly today.

## Mirror verification (post-work gate)

All 4 files byte-identical via `diff -q` AND MD5 (L36 authoritative hierarchy):

```
✓ log.md byte-identical + MD5 58c1d09e339cb31e3162d633484744d5
✓ learned-about-tuananh.md byte-identical + MD5 902007b73032fc48b31b4077ab4d7f08
✓ index.md byte-identical + MD5 67e1dcdc1c7ac35759af0c0320850616
✓ tiktok-video-editor-v3.19-v3.20-... byte-identical + MD5 6c01219bb1b1c5a1acadae8f3b29593e
```

All 4 mirrored first-try, no EAGAIN. Sleep 3 between files worked (canonical pattern from 07-01 lesson).

## Wikilink validation (L35 pre-write check)

Before writing the synthesis page, validated all 10 raw transcript wikilinks resolve + 10 concept page wikilinks resolve. All 20 destinations confirmed via `ls`. Zero broken wikilinks in the new page.

## What's reusable for next curator pass

1. **10-transcript synthesis case is now documented.** Pattern confirmed at 10 transcripts (between 7-transcript and 22-transcript cases). Future curators can confidently apply synthesis-over-fill at 10-transcript batch.

2. **L45 meta-pattern codified.** The 3rd "rule-based ≠ understand-based" iteration is now in the timeline. Future escalations on the same pattern will be recognized faster (currently takes ~5h to drive from hard call-out to skill rewrite — if L45 is consulted first, maybe 2-3h).

3. **Source-recall + beat-by-beat methodology is reproducible.** When anh says "phân tích sâu hơn", the 5-step methodology from this run can be applied directly. Codified in the synthesis page's "Personal Notes" section.

4. **Operational-vs-synthesis test passed all 5 categories.** Reinforces the existing pattern (07-06 L29-followup) without needing new rule changes.