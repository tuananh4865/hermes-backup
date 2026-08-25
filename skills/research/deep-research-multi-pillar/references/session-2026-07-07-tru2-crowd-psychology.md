# Session Reference: Trụ 2 Crowd Psychology Research (2026-07-07)

> **Use case:** Tuấn Anh yêu cầu deep research TRỤ 2 (Tâm lý học đám đông + Viral mechanics) trong series "nghệ thuật bán hàng" multi-pillar research. Output 1 file wiki tổng hợp thay vì 4 file riêng.

## Context

- **Project:** nghiên cứu nghệ thuật bán hàng cho content creator TikTok Việt Nam
- **Trụ:** TÂM LÝ HỌC ĐÁM ĐÔNG + VIRAL MECHANICS
- **Pillar mục tiêu:** 50+ URLs, 14 sub-topics cụ thể
- **Output path:** `/Volumes/Storage-1/Hermes/wiki/concepts/research-crowd-psychology-2026-07-07.md`
- **Channel:** Hermes CLI (không phải Telegram — file-save OK)

## Hard constraints từ user

- **Max 15 API calls** — budget cứng
- **CHỈ dùng `mcp__MiniMax__web_search`** — cấm `web_extract`
- **Format YAML frontmatter + sections + 50+ URLs cuối file**
- **Quote/paraphrase < 15 từ/source**
- **Source citation format:** `[N] Author. Title. Source. Date. URL`
- **Reply phải có:** tổng số URLs, tổng số mechanisms, top 5 master insights

## Decision: IN-LINE BATCHED CALLS (không dùng delegate_task)

**Lý do:**
1. Budget 15 calls TỔNG → delegate_task × 14 subagents = vượt budget
2. Output muốn 1 file duy nhất → tách 14 subagents rồi synthesize = thừa
3. Path output đã cụ thể (wiki/concepts/) → không cần subagent phân chia theo pillar
4. Cấm `web_extract` cũng độc lập với mode chạy

**Approach đã dùng:**
- **Batch 1:** 8 parallel `mcp__MiniMax__web_search` (Le Bon, Berger, Berger/Milkman, Watts, Hatfield, Christakis/Fowler, Aral, Salganik law of small numbers)
- **Batch 2:** 7 parallel (Salganik music lab, TikTok 2026, IG Reels 2026, Crilly, Berger Word of Mouth, Made to Stick, Twitter threads)
- **Total calls used:** 15/15 (đạt ceiling nhưng đủ)
- **Kết quả:** 56 URLs (vượt 50+), 18 mechanisms, 5 master insights

## Output structure thành công

```
01. Le Bon (3 mechanisms: collective mind, contagion, suggestibility)
02. Berger STEPPS (S-T-E-P-P-S framework)
03. Berger & Milkman 2012 (high-arousal emotions)
04. Watts Six Degrees 2003 (small-world, cascades)
05. Hatfield 1993 (mimicry → feedback → contagion)
06. Christakis/Fowler 2009 (3 degrees of influence)
07. Aral (peer effects, influentials ≠ susceptibles)
08. Christakis network science tổng quát
09. Heath Brothers Made to Stick (SUCCES)
10. Crilly earnest research
11. Viral mechanics social media 2026 (TikTok, IG, Twitter)
12. Tổng hợp 18 mechanisms + 5 master insights
[Nguồn tham khảo] — 56 URLs ở cuối file
```

## File YAML frontmatter structure đã dùng

```yaml
---
title: "Trụ 2 — Tâm Lý Học Đám Đông & Viral Mechanics"
date: 2026-07-07
author: "Hermes Agent (subagent delegate, miniMax search)"
topic: crowd-psychology
tags: [tâm-lý-đám-đông, viral, contagion, STEPPS, network-effect, christakis, watts, berger, hatfield, tiktok-algorithm]
target_user: "Anh Tuấn Anh — TikTok content creator, bán shop cầu lông + body mist + phụ kiện quay"
total_urls: 56
total_mechanisms: 18
master_insights: 5
source_format: "[N] Author. Title. Source. Date. URL"
---
```

## Synthesis format cuối reply (đã dùng thành công)

```
## Summary — Trụ 2 Research: Tâm Lý Học Đám Đông + Viral Mechanics

**File created:** `<path>`

### Tổng kết
- **Tổng URLs:** 56 (yêu cầu ≥ 50 ✅)
- **Tổng mechanisms identified:** 18
- **Master insights:** 5
- **API calls used:** 15/15 (max)
```

Đặt NGAY đầu reply — user scan trong 3s có overview toàn bộ research.

## Các top 5 insights đã viết

1. **Awe + Concrete > Polish** — Real + emotional content wins
2. **Trigger density = Reach density** — Body mist cần gắn nhiều situation cues
3. **First 10 susceptibles > 10K passive** — Target early-engaging nodes (Aral)
4. **Network > Broadcast** — TikTok interest-graph cho phép 0→5M views
5. **Earnestness kills slickness** — Authenticity = asymmetric advantage

## Pitfalls gặp phải + fix

1. **Một search trả về 0 result hữu ích** (Salganik music lab — chỉ tìm được 1 PDF link) — fix: dùng knowledge đã có về "Law of Small Numbers" + Tversky/Kahneman 1971 → Mlodinow Drunkard's Walk → Salganik music lab extension. Cross-cite từ research mình biết, không bịa số.
2. **Crilly "earnest" — không có paper specific high-profile** — fix: cite qua các paper khác reference Crilly (C. Zollo, Ishak dissertation). Ghi chú honest "phần này lightweight nhất" trong issues section.
3. **Không có vấn đề với channel delivery** — session này chạy trên Hermes CLI (KHÔNG phải Telegram), nên OK chỉ save file + summary, không cần embed toàn bộ content như Pitfall #9 của Telegram mode.

## Lesson learned (encoded thành Pitfall #11)

**Khi user set hard budget (≤20 calls) → IN-LINE BATCHED web_search, KHÔNG delegate_task** dù skill default nói "launch subagents". Hard budget = constraint mạnh hơn skill default.

Verify case này: 14 sub-topics + max 15 calls + 1 output file → in-line batch là approach tối ưu. Delegating subagents = vượt budget 14×.

## Related

- [[mcp-search-workarounds]] — workaround khi `mcp__MiniMax_web_search` 1027 error
- [[session-2026-06-17-content-creator]] — case study gốc 3-pillar với delegate_task
