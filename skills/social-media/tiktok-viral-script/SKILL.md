---
name: tiktok-viral-script
title: TikTok Viral Script
description: Research trending TikTok content and write viral scripts in Tuấn Anh's voice — hook, body, CTA structure for TikTok Shop Vietnam affiliate content.
trigger: When Anh asks to write a TikTok script, research trending products/sounds, or create content calendar.
created: 2026-05-08
updated: 2026-05-09
type: skill
tags: [tiktok, content, vietnam, social-media]
confidence: high
relationships: [hermes-autoresearch, xurl, gen-z-slang-2026-04]
---

# TikTok Viral Script Skill

Write viral TikTok Shop scripts in Tuấn Anh's authentic Vietnamese voice.

## Trigger Conditions
- Anh asks to write/create a TikTok script
- Anh asks to research trending products/sounds on TikTok Vietnam
- Anh asks for a content calendar or content plan
- Any request involving TikTok Shop affiliate content

## Workflow

### Step 1: Research (MANDATORY before any script)
Research 3 areas in parallel using web search:
1. **TikTok Shop Vietnam trending products** — use FindNiche or FastMoss data
2. **Vietnam TikTok trending sounds** — chartex.com/vietnam, 35express.org
3. **Gen Z Vietnamese slang** — current slang terms, what's hot vs dead

### Step 2: Identify Top Hooks
From research, identify 3-5 viral hooks currently working:
- Format: `Hook Type → Template text → Best for`
- Prioritize NEW trends (within 7 days) over stale ones

### Step 3: Create Daily Briefs (Morning + Evening)
When running as cron job or daily research, produce TWO briefs:

**Morning Brief (8AM)** — Focus: trending products + sounds + hooks for today's content
**Evening Brief (6PM)** — Focus: deeper analysis + scripts for tonight + next-day preview

```
Output path: ~/hermes/workers/content-creator/outputs/YYYY-MM-DD-[morning/evening]-brief.md
```

**Morning brief structure:**
1. Platform pulse (market status, key stats)
2. Trending products table (product, orders, price, category)
3. Trending sounds table (rank, sound, creator, 7-day creates, why it works)
4. NEW trend highlights (with source link + date)
5. Gen Z slang update (hot terms + dead terms to avoid)
6. Top 5 viral hooks currently working
7. 7-day content calendar (each day: topic, hook type, sound, script direction)
8. Script of the day (first day of calendar)

**Evening brief structure (richer than morning):**
1. Platform pulse (add demographic shift notes — Millennials drive revenue, Gen Z drives virality)
2. Trending products table (ADD GMV column — shows revenue potential, not just volume)
3. Rising sound alerts (watch for sounds with high 24h growth vs 7-day — early detection)
4. Gen Z slang update (same as morning)
5. Top viral hooks (same as morning)
6. 7-day content calendar with scripts for TONIGHT (not just tomorrow)
7. 2-3 full scripts ready to film
8. Market insights: commission math, fee reality, product prioritization
9. Tomorrow's focus preview

**Output files:**
- Brief: `~/hermes/workers/content-creator/outputs/YYYY-MM-DD-[morning/evening]-brief.md`
- Heartbeat: `~/hermes/workers/content-creator/HEARTBEAT.md` (status tracking)

### Step 4: Write Individual Scripts
Per script request:

**Structure (max 25 seconds):**
```
[HOOK — 0-3s]
Cầu cứu hốt hoảng + tình huống cụ thể
VD: "Mấy con vợ ơi cứu anh với!" hoặc drama tension opening

[BODY — 3-20s]
Trải nghiệm timeline — kể chuyện, KHÔNG liệt kê specs
- Tập trung vào cảm xúc và trải nghiệm cá nhân
- Dùng Gen Z slang mới nhất
- Proof social: "X nghìn đơn trong 7 ngày"

[CTA — 20-25s]
"Mua ủng hộ anh đi mấy con vợ chứ" — casual, không pushy
```

## Tuấn Anh's Voice Rules

### Pronouns (NEVER deviate)
- Speaker: **"anh"**
- Audience: **"mấy con vợ"**
- ❌ NEVER: "mấy đứa", "mấy chị", "các bạn", "các bạn ơi"

### Script Style
- Hook: Cầu cứu hốt hoảng + tình huống cụ thể HOẶC drama tension
- Body: Kể chuyện, storytelling — KHÔNG liệt kê specs
- CTA: Casual, thân mật

### Gen Z Slang Rules
- Use CURRENT slang — research fresh each session
- Hot May 2026: nam thư, ra dại, meoxink, lọ (HOT from "lỏ"), chuzz, các mom ơi
- DEAD (never use): "quất một phát", "đỉnh nóc kịch trần", template scripts
- Intensifiers: "hơi bị", "vãi cộng đồng mạng"

### Algorithm Changes — May 2026 Update (CRITICAL)

**Commerce Signals > Entertainment Signals**
As of May 2026, TikTok's algorithm has shifted weighting from entertainment signals (likes, shares, watch time) to commerce signals (product page clicks, add-to-cart, completed purchases).

**What this means for scripts:**
- A video that is "entertaining" but doesn't drive commerce actions will NOT be distributed
- Hook must create urgency to CLICK, not just to watch
- Every script should have a natural "click moment" — a point where viewer wants to see the product price/detail
- OLD tactic: "Mua ngay!" hook → WORKS LESS now (algorithm sees it as pressure, not signal)
- NEW tactic: Show product in use → let viewer CHOOSE to click = real commerce signal

**Creator Health Rating (CHR) — ACTIVE**
- Every creator has a CHR score (0-1000, starts at 200)
- Green (200-1000): Safe, full distribution
- Orange (151-199): Light restrictions
- Red (1-150): Commercial features blocked
- 0: Permanently banned
- **⚠️ Action:** Only partner with creators who have GREEN CHR. Red CHR = your affiliate content goes into algorithmic dead zone.

**Completion Rate Bar: 70%** (up from ~50% in 2024)
- Below 50%: Very limited distribution
- 50-70%: Moderate
- 70%+: Strong, potential virality
- 80%+ with rewatches: High virality
- **Script impact:** Every second must earn the next second. Front-load the hook payoff.

**Follower-First Distribution**
- Video is now tested FIRST with the account's followers before broader FYP
- If followers don't engage, video dies in cold start — even if content is good
- **Script impact:** First video with a new product should be FOR followers, not to go viral

**Original Audio Prioritized**
- Reposted content (watermark from IG/YT) = reduced distribution
- Original audio/sounds = algorithmic bonus
- AI-generated content (pure text-to-speech, no human presence) = penalized
- **Script impact:** Record with real voice, use original sounds or well-known trending audio

### QA Checklist (every script)
- [ ] Hook urgency in first 3 seconds
- [ ] Body tells story, not specs
- [ ] CTA casual, not pushy
- [ ] Gen Z slang appropriate and current
- [ ] Dead phrases avoided
- [ ] Pronouns correct (anh + mấy con vợ)
- [ ] Script is UNIQUE — no template repetition
- [ ] **Has a "click moment" — viewer wants to see product price/detail**
- [ ] **Completion rate optimized — every second earns the next**

### QA-CORRECT-BEFORE-DELIVERY Protocol (2026-05-08 — MANDATORY)

**⚠️ This is not optional.** When a script fails QA:
1. Identify the specific TRÁHN violation
2. **Fix it inline immediately** — rewrite the failing phrase with fresh wording
3. Verify the fix passes QA
4. THEN report the corrected version to Anh

**NEVER report a failed script to Anh without correcting it first.** "Flagged for correction" is not a valid end state — the corrected version must be what gets delivered.

**Known TRÁHN violations (verify these in EVERY script):**
- ❌ "đỉnh nóc" or "đỉnh nóc kịch trần" → replace with "ngon vậy", "hơi bị ok", etc.
- ❌ "quất một phát" → replace with action phrasing
- ❌ "đã X là Y" cấu trúc cứng nhắc → replace with conversational
## Critical Research Finding (May 2026)

### Gen Z Purchase Behavior — What Actually Drives Buying

From academic research (Tra Vinh University, 394 respondents, SEM analysis):

| Factor | Beta | P-value | Significance |
|--------|------|---------|--------------|
| **KOL/KOC Influence** | 0.580 | <0.001 | ✅ MOST IMPORTANT |
| Content Trust | 0.301 | <0.001 | ✅ Important |
| Entertainment Value | 0.014 | 0.790 | ❌ ZERO — not significant |

**⚠️ Entertainment does NOT drive purchases.** Gen Z buys because they trust the person recommending, NOT because content is entertaining.

**Practical implications:**
- Funny/entertaining scripts get views but don't convert
- Authentic personal recommendation scripts convert better
- Micro-influencer (small creator) recommendations convert 60% better than big influencers
- "Trust me because I actually used it" > "This product is so amazing everyone needs it"

**Script strategy:**
- Lead with PERSONAL EXPERIENCE ("anh đã dùng 2 tuần...")
- Add SOCIAL PROOF ("164K đơn trong 7 ngày" or "bạn mình cũng mua rồi")
- Keep it REAL — Gen Z smells fake marketing from miles away

## Sources
- Products: https://findniche.com/tiktok/trending-products-vn
- Sounds: https://chartex.com/tiktok/sounds/7-days/vietnam
- Trends: https://35express.org (search "trend")
- Slang: https://trykaiwa.com/blog/vietnamese-gen-z-slang-phrases-2026
- Algorithm: https://zonflip.com/tiktok-shops-may-2026-algorithm-decoded (May 2026 update)
- CHR System: https://dembuon.vn/threads/cap-nhat-chinh-sach-affiliate-tiktok-2026
- Gen Z Research: Tra Vinh University Journal of Science — "Factors Affecting Gen Z Online Purchase Intention on TikTok Shop"
- Product research: https://findniche.com/tiktok/trending-products-vn

## Output Paths
- Morning briefs: `~/hermes/workers/content-creator/outputs/YYYY-MM-DD-morning-brief.md`
- Wiki log: Append to `/Volumes/Storage-1/Hermes/wiki/log.md` with `## [YYYY-MM-DD] cron | content-creator-morning-brief`

## Pitfalls (AVOID THESE)

### Script Structure Mistakes
- ❌ **Listing specs instead of telling story** — "product has 200ml, made of bamboo, organic" = boring. Instead: "anh dùng 2 tuần rồi, da em nó mềm lắm luôn"
- ❌ **Template repetition** — using same hook structure as previous script. Each script MUST be unique
- ❌ **Dead phrases** — "đỉnh nóc kịch trần", "quất một phát", "đã X là Y" = instantly dated
- ❌ **"Mua ngay!" CTA** — too pushy, triggers algorithm pressure detection, lower distribution

### Pronoun Mistakes (INSTANT REJECT)
- ❌ "mấy đứa", "mấy chị", "các bạn", "các bạn ơi" — NEVER use these
- ✅ ONLY "anh" + "mấy con vợ"
- These are Tuấn Anh's signature pronouns — deviation breaks authenticity

### Research Mistakes
- ❌ **Skipping research** — writing script without fresh Gen Z slang research = outdated voice
- ❌ **Using stale trends** — trends older than 7 days = missed opportunity
- ❌ **Ignoring CHR** — partnering with red-CHR creators = affiliate content dies in algorithmic dead zone

### Algorithm Mistakes
- ❌ **Entertainment-focused scripts** — "entertainment value" has ZERO statistical impact on purchases (beta=0.014, p=0.790)
- ❌ **Generic viral hooks** — "This is amazing everyone needs this" = no trust signal
- ❌ **No "click moment"** — if viewer doesn't want to see price/detail, algorithm won't push

### Voice & Style Mistakes
- ❌ **Polished/formal tone** — sounds fake to Gen Z. Authentic roughness > corporate polish
- ❌ **Over-using intensifiers** — "hơi bị" every sentence = loses impact. Use sparingly
- ❌ **Repetitive Gen Z terms** — same slang in every script = copy-paste feel

## Example Scripts

### Example 1: Product Discovery Hook (Kẹp Tóc Nơ Bong Bóng)
```
[HOOK — 0-3s]
"Anh nhìn thấy cái này trên TikTok lúc 2h sáng và không ngủ được luôn"

[BODY — 3-20s]
"Mấy con vợ ơi, anh thề luôn, cái nơ bong bóng này nó cute vãi. 
Anh mua cho em gái, xem review 1星 → 5星 hết luôn. 
Mà giá chỉ 36K thôi, vừa túi học sinh. 
Cái này bán 19K đơn trong 7 ngày — nghe có vẻ nhiều nhưng mà ạ, 
ai bán được cái này commission nó ngon lắm luôn."

[CTA — 20-25s]
"Link in bio đó mấy con vợ ơi, mua ủng hộ anh đi chứ"
```

### Example 2: Warning Hook (Nam Thư Parody)
```
[HOOK — 0-3s]
"⚠️ CẢNH BÁO CÓ NAM THƯ — mấy con vợ né gấp"

[BODY — 3-20s]
"Không phải dating nam thư đâu, là cái kẹp tóc nam thư này 
nó toxic cho ví tiền của mấy con vợ luôn. 
Mấy ơi, 32K thôi mà ai cũng mua, hàng 32K đơn trong tuần. 
Anh tính nhẩm xong hoảng luôn — sản phẩm này ai bán cũng ăn commission."

[CTA — 20-25s]
"Nhé, mua ủng hộ anh đi mấy con vợ chứ"
```

### Example 3: Transformation Hook (Charm Chữ Mini)
```
[HOOK — 0-3s]
"Ngay cả nhân viên ngân hàng cũng hỏi anh mua ở đâu"

[BODY — 3-20s]
"Không phải anh khoe đâu, charm mini này nó làm cả phòng đều hỏi. 
21K một cái, 164K đơn trong 7 ngày — mấy con vợ biết cái gì hot chưa? 
Anh thì biết rồi, vì anh đã bán được 2 tuần nay."

[CTA — 20-25s]
"Mua link in bio đi, giao nhanh lắm luôn"
```

## Related
- [[hermes-autoresearch]] — Autoresearch skill for nightly research runs
- [[xurl]] — X/Twitter trends research (separate platform)
- [[gen-z-slang-2026-04]] — Gen Z slang reference (updated May 2026)
