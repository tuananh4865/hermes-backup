# YouTube Channel Deep-Dive — Output Template

**Purpose:** Template for "research kênh YouTube X sâu" / "phân tích kênh Y" requests. Use when user sends a channel URL + asks for deep analysis (typically to learn patterns for their own channel).

**Verified:** 2026-07-11 with @VuiVe (1.18M subs, 828 videos, edutainment/facts niche)

---

## When to use this template

Trigger phrases:
- "nghiên cứu kênh youtube này"
- "phân tích kênh X"
- "research kênh Y"
- "học cách làm của kênh Z"

Always pair with: SKILL.md section "YouTube Channel Deep-Dive Workflow" (2-prong parallel subagent pattern).

---

## Section 1: Channel Profile (snapshot data, ground-truth only)

```markdown
## 📊 Profile kênh {NAME} @{HANDLE}

| Field | Value |
|---|---|
| Tên kênh | {Name} |
| Handle | @{handle} |
| Subscribers | {X}M hoặc {X}K |
| Tổng video | {N} |
| Verified | ✅ / ❌ |
| Ngày tạo | {YYYY-MM} (nếu có) |
| Slogan | "{channel slogan}" |
| Email liên hệ | {email} (signal monetization) |
| Niche | {category} |
```

**Data source:** `browser_navigate https://www.youtube.com/@{handle}` → capture from snapshot. NEVER fabricate.

---

## Section 2: Content Pattern Analysis (Subagent A output)

Required fields:

### 2.1 Format mix
```markdown
| Format | % | Avg duration | Avg views |
|---|---|---|---|
| Long-form (>10min) | {X}% | {Y} min | {Z}K |
| Mid-form (5-10min) | {X}% | {Y} min | {Z}K |
| Short-form (<1min) | {X}% | {Y}s | {Z}K |
```

### 2.2 Top 5 chủ đề (last 30-50 videos)
```markdown
| Chủ đề | Count | Avg views |
|---|---|---|
| {topic 1} | {N} | {X}K |
| {topic 2} | {N} | {X}K |
| ...
```

### 2.3 Title formulas (pattern recognition from 30+ titles)
```markdown
| Formula | Ví dụ | Frequency |
|---|---|---|
| "Tất cả [X] trong Y phút" | {example} | {N}/{total} |
| "Những [adj] nhất về [topic] (Phần N)" | {example} | {N}/{total} |
| ...
```

### 2.4 Hook patterns (first 10 seconds)
- {Pattern 1: how video opens}
- {Pattern 2: ...}
- {Pattern 3: ...}

### 2.5 Thumbnail style
- {Colors, faces, text overlay, visual motif}

### 2.6 Monetization signals
- {Sponsored segments (Brand name in title or video)}
- {Affiliate links in description}
- {Channel membership}
- {Merch/shop}

### 2.7 Upload frequency
- {N video/tuần}
- {Best posting day/time if observable}

### 2.8 Engagement rate estimate
- {Avg views / subscribers = ER%}
- {Likes/views ratio if visible}

---

## Section 3: Market Benchmark (Subagent B output)

### 3.1 Top channels in same niche (sorted by subs)

```markdown
| Channel | Subs | Avg views | ER% | Format | Notable |
|---|---|---|---|---|---|
| {Name} | {X}M | {Y}K | {Z}% | {Long/Short} | {USP} |
| ... |
```

### 3.2 Top channels in adjacent niche (edutainment/knowledge)
- {List 5-10 channels user could learn from}

### 3.3 Common success formulas across winners
- {Hook pattern}
- {Title pattern}
- {Posting cadence}
- {Monetization model}

### 3.4 What's NOT working (low-view outliers)
- {Topic X had low views despite high subs — signal market saturation}

---

## Section 4: Gap Analysis (cross-reference for user's niche)

**If user's purpose is "build channel in niche A inspired by channel B in niche C":**

### 4.1 Transferable formulas
| Formula from {channel B} | Can apply to {niche A}? | How |
|---|---|---|
| {formula 1} | Yes / Partial / No | {specific adaptation} |
| {formula 2} | Yes / Partial / No | {specific adaptation} |

### 4.2 Gaps in {niche A} market
- {Gap 1: format nobody is doing}
- {Gap 2: audience segment unserved}
- {Gap 3: topic nobody covers}

### 4.3 Risks
- {Risk 1: why this might not work}
- {Risk 2: ...}

---

## Section 5: Roadmap 30/60/90 days (actionable next steps)

### Month 1 (Days 1-30): Foundation
- {Action 1: e.g., "Xác định niche chính xác + chọn 5 chủ đề pilot"}
- {Action 2: ...}

### Month 2 (Days 31-60): First batch + learning
- {Action 1: e.g., "Sản xuất 8 video pilot (2/tuần)"}
- {Action 2: ...}

### Month 3 (Days 61-90): Scale or pivot
- {Decision criteria: e.g., "Nếu 1 trong 8 video >50K views → scale"}
- {Alternative: pivot to format mới}

---

## Section 6: Caveats (mandatory)

Always include:
```markdown
## ⚠️ Caveats
- **Tool used:** {browser_navigate + Exa + MiniMax search}
- **View counts:** {Cập nhật đến ngày X, có thể đã tăng/giảm}
- **Sub count:** {Cập nhật đến ngày X}
- **Sample size:** {N video analyzed}
- **Confidence:** {high/medium/low} — vì {lý do}
- **Không truy cập được:** {YouTube Analytics, revenue, audience demographics — cần channel owner}
```

---

## Working example: @VuiVe case (2026-07-11)

User request: *"https://www.youtube.com/@VuiVe nghiên cứu kênh youtube này, nghiên cứu sâu nhé!!!"*

Outcome:
- Channel profile: 1.18M subs, 828 videos, Verified ✅, slogan "Mọi thứ cũng đơn giản thôi", contact partners.98smedia@gmail.com (sponsored content)
- Format: 100% long-form 13-30 min, 2-3 video/tuần
- Top chủ đề: Listicle kiến thức (con người, động vật, lịch sử, địa danh, IQ test)
- Title formula: "Tất cả [X] trong Y phút" + "Những [adj] nhất về [topic] (Phần N)" + sponsored tag
- Hook: thường visual hook + question opening, fast-paced listicle
- Monetization: Sponsored content (CellphoneS, etc.) + YouTube Ad
- Transferable cho kênh cầu lông: "Tất cả các loại smash trong 15 phút", "Những cây vợt Yonex tốt nhất cho người mới"
- Gap: cầu lông edutainment VN chưa có channel chuyên dạng listicle knowledge

**Lessons applied to next session:**
1. Always `browser_navigate` for YouTube — never `web_extract`
2. Dispatch 2 subagents in parallel (analyze + benchmark)
3. Embed inline in Telegram — save file only if >4000 chars
4. Include 4-dim caveats: tool, view freshness, sample size, confidence