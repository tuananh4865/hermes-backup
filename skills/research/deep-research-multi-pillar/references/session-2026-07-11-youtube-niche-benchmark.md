# Session Reference — 2026-07-11: YouTube Niche Benchmark → Strategy Report

## Unique mode (NOT in main skill)
- **Scope:** SINGLE vertical niche benchmark — not multi-pillar. User asked: "research top kênh YouTube cầu lông/edutainment VN thành công - benchmark để Tuấn Anh học theo".
- **Output type:** One consolidated strategic markdown report (4,842 chữ / 28KB / 418 lines) saved directly to user home `/Users/tuananh4865/...md`.
- **Difference from existing skill modes:**
  - Not multi-pillar synthesis (this was 1 vertical: YouTube VN cầu lông + 1 cross-vertical benchmark: edutainment pattern).
  - Not in-line bounded mode with hard API budget (no max-calls constraint stated).
  - Not Telegram/remote mode (user on Claude CLI → save-file + summary is fine).
- **Did use parallel + delegation-rejected path:** parent agent did all searches in-line (32 `mcp__exa__web_search_exa` + `mcp__MiniMax__web_search` calls batched) without `delegate_task`. Worked because:
  - All searches were independent (no cross-feed needed).
  - Total budget stayed reasonable (~32 calls × ~1.5s each = ~5 min wall time).
  - Single output file made in-line synthesis simpler than multi-file stitching.

## Verified pattern — what worked

1. **Two-tier research target structure** that produced the synthesis matrix:
   - **Tier 1 (primary niche, deep dive):** Top 10 channels of target niche with case studies on top 3.
   - **Tier 2 (cross-vertical benchmark):** Top 5 channels of an adjacent proven niche (edutainment) to extract cross-applicable format formulas.
   - This is the cleanest structure for "X for a specific user/learn from Y" requests.

2. **Channel data sourcing pattern** — 5+ separate sources per channel ranking:
   - Social Blade / NoxInfluencer / youtubers.me / vidIQ (sub & view counts)
   - Per-channel `youtubers.me/[slug]/youtuber-stats` earnings snapshots
   - Per-channel Playboard report (when available)
   - Top video view counts from individual video pages (for view distribution analysis)
   - Press coverage / founder interviews for context (e.g., emdep.vn Founder Phan Tuấn Anh interview for VNB history)

3. **Output report structure that user can ACTION:**
   - Executive Summary (1 paragraph, concrete numbers)
   - Big comparison tables (subs/view/view-per-month/video-count)
   - Case study deep-dive on 1–3 channels with view distribution analysis
   - Gap analysis with concrete content series ideas (not just "find a gap")
   - **30/60/90 roadmap** with specific KPI per phase (NOT just generic advice)
   - Failure modes list (8–10 specific mistakes to avoid)
   - Decision checklist (5 pre-flight questions) at the end

4. **Numbers to anchor** (verified useful for Tuấn Anh's use case):
   - VN RPM: $0.25–1.5 long-form, $0.05–0.30 shorts → AMPLIFY that AdSense is NOT the revenue driver.
   - 100K view benchmarks for niche channels (realistic vs unicorn).
   - 90-day sub milestone that maps to affiliate revenue threshold (~5K subs → first brand deal conversation).

## What did NOT need a skill (and shouldn't)

- This was a one-shot research deliverable for a personal decision. Did NOT need to create a new dedicated skill ("youtube-channel-benchmark-research") because:
  - It's too narrow to warrant class-level coverage.
  - The patterns that worked are general research-report-writing patterns, not domain-specific techniques.
  - Capturing it as a skill would create a long flat list — explicitly discouraged.
- Better placed as a **reference** to the existing `deep-research-multi-pillar` skill so future "benchmark X niche channels" requests can pull this verified pattern.

## When to re-run this pattern (re-trigger conditions)

A future session should re-use this exact pattern when:
- User asks "research top [N] [platform] channels in [country/niche] for [purpose]"
- Cross-vertical format benchmark is implied ("X edutainment channels have proven formula — apply to niche Y")
- Output must be strategic/actionable (not just data dump)
- Single consolidated report file expected (not multi-pillar split)
- No explicit channel constraint (Telegram/CLI/Obsidian) → file save + reply summary OK

## Pitfall observed (didn't fire, worth knowing)

**Multiple-source-numbering inconsistency:** The data points from different analytics services (Social Blade, youtubers.me, vidIQ) sometimes disagree by 10–30% on the same channel for the same date. When unsure which to use: cite the range (e.g., "976K subs (youtubers.me, Q2/2026)") rather than picking one. Verified helpful — user got realistic sense not over-precise numbers that turn out wrong next week.

**Cross-vertical benchmark strength:** The most actionable insight in this report came from CROSS-referencing edutainment channels (Vui Vẻ 1.17M, Dương biết tuốt 1.44M) onto the badminton niche. Pure badminton-internal research would have produced only "VNB is leader, others are fragmented". The cross-vertical import gave the actual format formula. **Always pair primary-niche research with ≥1 proven-formula adjacent niche.**
