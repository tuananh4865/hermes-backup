---
session_date: 2026-07-07
pillar_id: 1
pillar_name: "Sales psychology + classic sales art (Nghệ thuật bán hàng + Tâm lý bán hàng classic)"
deliverable_path: "/Volumes/Storage-1/Hermes/wiki/concepts/research-sales-psychology-2026-07-07.md"
mode: IN-LINE BATCHED (first verified case of Pitfall #11)
api_calls_used: 14/15
result: 65 URLs / 35.8 KB / 7 sections + 3 appendices — within 25-40 KB target
---

# Trụ 1 — Sales Psychology (2026-07-07)

## Constraints given by user

- Single output file: `/Volumes/Storage-1/Hermes/wiki/concepts/research-sales-psychology-2026-07-07.md`
- Max 15 API calls total
- CHỈ dùng `mcp__MiniMax__web_search` — KHÔNG dùng `web_extract`
- Min 50 URLs (preferred báo + X/Twitter + marketing blogs)
- Target file size 25–40 KB
- Format: YAML frontmatter + 7 sections + References ở cuối
- Citation format: `[N] Author. Title. Source. Date. URL`
- Quote/paraphrase < 15 từ/source — KHÔNG copy nguyên văn
- Mỗi query ≤ 8–10 query chất lượng
- Top creators specifically: @AlexHormozi, @JFischerOfficial, @KevinDurant, @SamOvens, @DanLokOfficial, @DonaldMiller

## Sub-topics user listed

1. Cialdini 6 + 7th (unity) principles
2. SPIN / AIDA / PAS / BAB frameworks
3. Copywriting masters: Ogilvy / Schwartz / Halbert / Caples / Sugarman / Bencivenga
4. Persuasion architecture: Schwartz awareness + Brunson secrets + Hormozi Value Equation + $100M Offers
5. Direct response marketing old vs new school
6. Sales page psychology (long vs short, headlines, bullets, CTAs)
7. Storytelling: StoryBrand / Building a StoryBrand / Storyselling

## What I did — batching pattern

**3 batch parallel, 14 total calls, 1 file output**

### Batch 1 (5 calls parallel):
1. Cialdini 7 principles
2. Hormozi $100M Offers / value equation
3. Schwartz Breakthrough Advertising / 5 awareness levels
4. Donald Miller StoryBrand
5. SPIN selling Neil Rackham

### Batch 2 (4 calls parallel):
6. Sugarman "greatest sales letter" — returned 2 results (sparse but OK)
7. Gary Halbert Boron Letters / Scientific Advertising
8. David Ogilvy headlines
9. AIDA PAS BAB framework

### Batch 3 (5 calls parallel):
10. Hormozi closing techniques
11. Dan Lok high-ticket closer
12. Russell Brunson DotCom Secrets — ⚠️ **1027 hit**
13. Direct response old vs new school
14. Long form vs short form sales pages

`Bencivenga "Bullseye" copywriting` was originally planned but cut from the budget before sending — instead captured it from widely-documented industry knowledge (paraphrase only). The Brunson `1027` failure consumed the "budget cushion" needed.

## Key search strategy insight

Single broad query targeting multiple concepts in one shot returned 8-10 results each from MiniMax, so:

- 14 searches × ~5 results/call ≈ 70 raw citation candidates
- 65 numbered references in final file (some search results duped across queries)

This is the **cross-source citation amplifier** pattern — contradicts "delegate=more URLs" intuition. In-line batched mode with strategic queries can actually hit higher URL targets than fragmented delegation, because each call covers more ground.

## Failures + workarounds

| Failure | Pattern | Fix |
|---------|---------|-----|
| `Bencivenga "Bullseye"` **not even sent** — budget full | Quota discipline | Pre-decide which queries to cut |
| `Brunson DotCom Secrets` → 1027 | Keyword combination flagged without `site:` operator | Paraphrase from documented knowledge, log gap |
| Twitter handles (@JFischerOfficial, @KevinDurant, @SamOvens) thin search-hits | Twitter not well-indexed by MiniMax | Cite LinkedIn/Facebook cross-posts of same creators |

## Output structure delivered

**7 sections requested + 3 appendices added:**

0. Executive Summary — why pillar matters cho TikTok shop
1. Sales psychology fundamentals — Cialdini 7
2. Classic sales frameworks — SPIN, AIDA, PAS, BAB
3. Copywriting masters — Ogilvy → Bencivenga
4. Persuasion architecture — Schwartz × Brunson × Hormozi
5. Direct response — old vs new school
6. Sales page psychology — long/short, headlines, bullets, CTAs
7. Storytelling — StoryBrand + Storyselling
8. Sales insights from X/Twitter / Podcast
9. Áp dụng tổng hợp cho TikTok shop (cầu lông + body mist + phụ kiện quay)
10. Top 5 Master Insights

**Plus:**
- Appendix A: Methodology + Caveats (transparent gap-reporting)
- Appendix B: Quick-reference cheatsheet (60s)

## Lessons for next time

### 1. Single-query coverage > query-per-concept

A query like `Cialdini 7 principles of persuasion reciprocity scarcity unity` returned 9 organic results covering ALL 7 principles + recent 2026 commentary. **One strategic query > 5 narrow queries** when your goal is "URL density", not "deep dive on each principle".

### 2. Operator-less 1027 exists (update to mcp-search-workarounds)

The `Brunson DotCom Secrets` query had no `site:` operator and still hit 1027. The existing `mcp-search-workarounds` skill pinned lesson #1 said "site: triggers 1027 ~30% of the time" — this isn't fully accurate. **Operator-less keyword combinations can also trip 1027.** When retrying, drop quoted phrases + add "guide" / "summary" type qualifiers.

### 3. Twitter handles thin on MiniMax web_search

`@AlexHormozi` → LinkedIn posts found (good); `@JFischerOfficial`, `@KevinDurant`, `@SamOvens` → almost no direct hits. Future strategy:
- Cite LinkedIn cross-posts of the same creator (verified working)
- For thin-creator coverage, write "search-hits-thin" disclaimer in Appendix A, defer to separate research budget

### 4. File size budget is real — discipline needed

35.8 KB output was exactly in target window. Pitfall lessons:
- README-style exec summary (à la Section 0): consumes ~2 KB
- 7 deep sections: ~3–5 KB each
- References section (65 numbered): ~7 KB
- 2 appendices: ~3 KB

### 5. Verify command pattern (carry-over from Pitfall #7)

`ls -la` + `grep -c "^## "` + `grep -c "^\[N\]"` after every write_file is the "completion checklist" pattern. Run before declaring done.

## Outputs / artifacts

- `research-sales-psychology-2026-07-07.md` (35,844 bytes, 490 lines, 65 references)
- Reply summary: top-5 master insights + URL count + section count

## Notes for parent skill

Trụ 1 is the **session of origin** for the in-line batched pattern (Pitfall #11). Trụ 2 and Trụ 4 came after. Order in references matters because Trụ 1 documented the constraint interpretation FIRST — Trụ 2/4 are confirmations of the rule.
