# Session Reference: Pillar 4 Behavioral Science Research (2026-07-07)

> **Use case:** Tuấn Anh yêu cầu research Trụ 4 (Khoa học Hành vi + Behavioral Economics Nâng cao) — trụ cuối cùng trong series 4-pillar research cho kênh TikTok shop (cầu lông + body mist + phụ kiện).

## Context

- **Project:** Content Creator tại `/Volumes/Storage-1/Hermes/wiki/concepts/`
- **Pivot:** Trụ 4 là trụ NÂNG CAO sau khi đã cover Trụ 1 (sales), Trụ 2 (crowd psychology), Trụ 3 (consumer). Tập trung heuristics/biases + persuasion principles + 2026 marketing applications.
- **Mục tiêu:** Apply behavioral triggers vào TikTok content (script hook, CTA design, scarcity messaging)
- **Output:** Single wiki concept file (KHÔNG dispatch 4 file riêng như multi-pillar gốc)

## Constraints từ user (verbatim, đã extract)

- **Tools:** Chỉ `mcp__MiniMax__web_search` (KHÔNG dùng `web_extract`)
- **API budget:** Tối đa **15 calls**
- **URL minimum:** 50 (delivered 90 numbered citations + 88 unique URLs)
- **Topics:** 19 sub-topics explicit listed (System 1/2 → 2026 marketing)
- **Format:** YAML frontmatter + sections + URL list cuối file
- **Citation format:** `[N] Author. Title. Source. Date. URL`
- **Quote rule:** <15 words/source
- **Output path:** `/Volumes/Storage-1/Hermes/wiki/concepts/research-behavioral-science-2026-07-07.md`

## Decision: In-line Batched Calls (xác nhận Pitfall #11 lần 2)

**Đã verify:** Hard budget (15 calls) + explicit topic list (19 items) + single output path → **IN-LINE BATCHED MODE**, KHÔNG delegate_task.

### Strategy đã dùng

- 5 parallel calls/batch × 3 batches = 15 calls (đúng budget)
- Batch 1 (5 calls): Kahneman + Ariely + Cialdini + Thaler + Gilbert
- Batch 2 (5 calls): Loss aversion + Endowment + Sunk cost + Social proof + Scarcity
- Batch 3 (5 calls): FOMO + Reciprocity + Milgram + Liking + Marketing 2026
- Mỗi call query = 4-6 keywords chất lượng (không quá ngắn, không quá dài)

### Result đạt được

- 88 unique URLs (50% over minimum 50)
- 24 principles/biases covered trên 19 sub-topics
- File 32.9 KB (single file tổng hợp)
- Top 5 master insights cho TikTok shop cụ thể (cầu lông + body mist + phụ kiện)

## Lesson learned (verify Pitfall #11 generalization)

**Pitfall #11 đã được verify lần 2.** Pattern tổng quát:

| Signal trong user prompt | Decision |
|--------------------------|----------|
| "max N API calls" + N ≤ 20 | IN-LINE MODE |
| Topic list explicit (≥8 items) | IN-LINE MODE |
| Single output path đã chỉ định | IN-LINE MODE |
| "chỉ dùng web_search X" (không web_extract) | IN-LINE MODE |
| User muốn 1 file tổng hợp | IN-LINE MODE |
| **Ngược lại:** "research rộng", "không giới budget", multi-file output | DELEGATE MODE (default) |

## Khi nào KHÔNG dùng pattern này (warnings)

- Nếu user nói "research 19 topics mà không có budget constraint" → delegate 19 subagents là OK (theo Bước 2 gốc)
- Nếu user muốn mỗi pillar 1 file riêng → delegate (theo Bước 2 + Bước 4 file naming)
- Nếu budget = 50+ calls → delegate OK, in-line wasted efficiency

## Master insights produced (top 5)

1. **S1 thắng S2 trên TikTok** — hook 3s đầu = S1 trigger, caption dài = S2 skip
2. **Loss aversion 2:1** — "ĐỪNG MẤT 30%" convert gấp 2 lần "NHẬN 30%"
3. **Free > discount** — Ariely zero-cost bias: free ship/sample convert +30-50%
4. **FOMO + Scarcity + Social Proof** = combo TikTok killer
5. **Pre-suas 3s đầu** — Cialdini 2016: shocking image/curiosity, rồi persuasion

## File produced

- Path: `/Volumes/Storage-1/Hermes/wiki/concepts/research-behavioral-science-2026-07-07.md`
- Size: 32.9 KB
- Format: YAML frontmatter + 19 sections + 90 numbered refs + top-5 insights block
- Telegram embed: ✅ Master framework embed trong reply (theo Pitfall #9)

## Cross-references

- `references/session-2026-06-17-content-creator.md` — Multi-pillar với delegate_task
- SKILL.md Pitfall #11 — "Tự động delegate khi user đã set hard API budget" (verified Trụ 2 + Trụ 4)
- Related wiki files in `/Volumes/Storage-1/Hermes/wiki/concepts/`:
  - `research-sales-techniques-2026-07-07.md`
  - `research-crowd-psychology-2026-07-07.md`
  - `research-consumer-behavior-2026-07-07.md` (Trụ 3)
  - `research-behavioral-science-2026-07-07.md` (Trụ 4 — file này)
