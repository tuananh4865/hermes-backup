---
name: tiktok-viral-script
title: TikTok Viral Script
description: Research trending TikTok content and write viral scripts in Tuấn Anh's voice — hook, body, CTA structure for TikTok Shop Vietnam affiliate content.
trigger: When Anh asks to write a TikTok script, research trending products/sounds, or create content calendar.
created: 2026-05-08
updated: 2026-05-15
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

**⚠️ CRITICAL (2026-05-13): When Anh shares a URL first — READ IT BEFORE researching.**
User's workflow: URL shared → Extract/read content → Confirm understanding → Then research if asked.

**Why this matters:** In 2026-05-13 session, agent assumed @ecom_linus tweet was about "TikTok algorithm" without reading it. The tweet was actually about AI UGC + affiliate marketing. User had to correct twice.

**Correct sequence when URL is shared:**
```
1. web_extract or browser_navigate to read the URL content
2. Summarize what it's about — confirm with user
3. Only THEN do deep research if user asks
```

**If extraction fails (400 error, paywall, etc.):**
- Try browser_navigate → read content from rendered page
- If browser also blocked → report failure honestly, ask user to paste content
- NEVER proceed with research assuming what the URL contains

**Research 3 areas in parallel using web search:**
1. **TikTok Shop Vietnam trending products** — use FindNiche or FastMoss data
2. **Vietnam TikTok trending sounds** — chartex.com/vietnam, 35express.org
3. **Gen Z Vietnamese slang** — current slang terms, what's hot vs dead

### Step 2: Identify Top Hooks
From research, identify 3-5 viral hooks currently working:
- Format: `Hook Type → Template text → Best for`
- Prioritize NEW trends (within 7 days) over stale ones

### Step 3: Create Daily Content (Morning + Evening)
When running as cron job or daily research, produce content files:

**Morning (8AM)** — Scripts for today + updated 7-day plan
**Evening (6PM)** — Scripts for tonight + next-day preview

```
Output path: ~/hermes/workers/content-creator/outputs/YYYY-MM-DD-[morning/evening]-content.md
```

**⚠️ FILENAME NOTE:** The skill previously said "*-brief.md" but actual output is "*-content.md". 
- Research Agent outputs: `*-brief.md` (market analysis)
- Content Creator outputs: `*-content.md` (scripts + calendar)

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
- Morning brief: `/Users/tuananh4865/.hermes/workers/content-creator/outputs/YYYY-MM-DD-morning-brief.md`
- Evening brief: `/Users/tuananh4865/.hermes/workers/content-creator/outputs/YYYY-MM-DD-evening-brief.md`
- Heartbeat: `/Users/tuananh4865/.hermes/workers/content-creator/HEARTBEAT.md` (status tracking)

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

### Gen Z Slang Update (May 14, 2026 — from May 14 orchestrator session research)

### 🚨🚨 TRÁHN-VIOLATION LEVEL: "LỌ" vs "LỎ" — SCRIPT-KILLING ERROR!
**Source: TCC Agency (May 5, 2026). Confirmed again in May 15 morning research — this distinction keeps getting missed.**

| Từ | Nghĩa | Dùng khi |
|-----|-------|----------|
| **lọ** | HOT 🔥 | Cái gì cool, đỉnh, viral, trending |
| **lỏ** | KÉM ❌ | Cái gì fail, không ok, chất lượng kém |

**⚠️ THIS IS A TRÁHN VIOLATION — BLOCK DELIVERY if detected:**
- ❌ "Sản phẩm này lỏ quá" (meaning HOT) → WRONG → Gen Z will roast you
- ✅ "Sản phẩm này lắm lọ quá" → means HOT 🔥
- ❌ "video này lỏ quá" (meaning viral) → WRONG → means the video is FAIL
- ✅ "video này lọ quá" → means the video is fire 🔥

| Từ | Nghĩa | Dùng khi |
|-----|-------|----------|
| **lọ** | HOT 🔥 | Cái gì cool, đỉnh, viral, trending |
| **lỏ** | KÉM ❌ | Cái gì fail, không ok, chất lượng kém |

**⚠️ SCRIPT-KILLING ERROR TO AVOID:**
- ❌ "Sản phẩm này lỏ quá" → NGƯỜI NÓI ĐANG NÓI NÓ KÉM
- ✅ "Sản phẩm này lắm lọ quá" → NGƯỜI NÓI ĐANG KHEN NÓ HOT

**Các biến thể:**
- **lọd** — biến thể meme của "lỏ" (fail)
- **lỏ vãi** — cực kỳ kém (nhấn mạnh mức độ)
- **lỏ nhẹ** — fail nhẹ (ý trêu chọc)
- **hơi lỏ** — hơi fail (nhẹ hơn)
- **lọ** — HOT (đỉnh, cool) ≠ "lỏ"

### 🔥 TOP PRIORITY (135M+ TikTok posts)
- **SÍT RỊT** — "secret", 135M+ posts, USE IN EVERY SCRIPT

### NEW (found May 13-14 — from evening content)
- **thơm vãi** — sensory intensifier for fragrance (like "mát vãi" but for smell). Pattern: [sensory adjective] + "vãi" = extreme. mát vãi, thơm vãi, ngon vãi, xinh vãi
- **pin trâu** — long battery life (buffalo = strong/enduring)
- **sống nổi** — survive (heat), used for cooling products
- **ướt mát** — wet cool sensation (spray/mist products)
- **ra dại** — Điên cuồng vì vui (going wild from joy) — still hot
- **lọ** — HOT 🔥 (NOT "lỏ"!) — viral May 2026, still hot
- **nấu xói** — emerging Gen Z slang (May 14, meaning still emerging)

### 🌍 Global Trend (May 12-13, 2026)
- **#StandBanhMi** — "Stand By Me" → "Stand Banh Mi" on TikTok. Tourists eating banh mi on Vietnamese streets + lyric twist. Vietnamese street food going global. Content angle: "đời thường, du lịch, khám phá" = globally resonant.
- **Trình là gì mà trình ai chấm** — From HIEUTHUHAI song (Nov 2024), viral May 2026. "Ối dồi ôi, trình là gì mà trình ai chấm!" — đáp trả khi bị chỉ trích
- **Ối dồi ôi** — Thốt ra khi không tin được (surprise/disbelief)
- **Nam thư** — Toxic/flirty person to avoid
- **Ra dại** — Điên cuồng vì vui (going wild from joy)
- **lọ** — HOT (from "lỏ", viral May 2026)
- **Các mom ơi** — Cách gọi thân mật (variation of "mấy con vợ")

### Still Valid (from May 9)
- meoxink, chuzz, delulu is the solulu, main character energy, green/red flag, lỏ vãi

### DEAD (never use)
- "quất một phát" — FINISHED
- "đỉnh nóc kịch trần" — FINISHED
- "Bốc trúng sít rịt" — Fading out

### Intensifiers
- **vãi** — extreme intensifier (mềm dai vãi, lỏ vãi, thơm vãi, mát vãi)
- **hơi bị** — really, quite (use sparingly)

## Gen Z Slang Rules
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
- [ ] **Has trust signal, not just entertainment** — Personal experience or social proof present

### QA-CORRECT-BEFORE-DELIVERY Protocol (2026-05-08 — MANDATORY)

**⚠️ This is not optional.** When a script fails QA:
1. Identify the specific TRÁHN violation
2. **Fix it inline immediately** — rewrite the failing phrase with fresh wording
3. Verify the fix passes QA
4. THEN report the corrected version to Anh

**NEVER report a failed script to Anh without correcting it first.** "Flagged for correction" is not a valid end state — the corrected version must be what gets delivered.

**MANDATORY ENFORCEMENT (add to every session involving scripts):**

Before ANY script content is delivered, run:
```bash
# TRÁHN scan
SCRIPT_FILE="$1"  # or find latest
VIOLATIONS=$(grep -c "đỉnh nóc\|quất một phát\|đỉnh nóc kịch trần" "$SCRIPT_FILE" 2>/dev/null || echo "0")
if [ "$VIOLATIONS" -gt 0 ]; then
    echo "🚨 TRÁHN BLOCK: $VIOLATIONS violation(s)"
    grep -n "đỉnh nóc\|quất một phát" "$SCRIPT_FILE"
    echo "FIX REQUIRED — edit file inline, re-scan, only then proceed"
    exit 1
fi
echo "✅ TRÁHN PASS"
```

**Known TRÁHN violations (verify these in EVERY script):**
- ❌ "đỉnh nóc" or "đỉnh nóc kịch trần" → replace with "ngon vậy", "hơi bị ok", etc.
- ❌ "quất một phát" → replace with action phrasing
- ❌ "đã X là Y" cấu trúc cứng nhắc → replace with conversational

**⚠️ PITFALL (2026-05-09):** Despite QA-CORRECT-BEFORE-DELIVERY being documented since 2026-05-08, the orchestrator still delivered content with TRÁHN violations in this session. The protocol was documented but not executed as a runtime gate. This skill now has the enforcement script above — use it.

**Known TRÁHN violations (verify these in EVERY script):**
- ❌ "đỉnh nóc" or "đỉnh nóc kịch trần" → replace with "ngon vậy", "hơi bị ok", etc.
- ❌ "quất một phát" → replace with action phrasing
- ❌ "đã X là Y" cấu trúc cứng nhắc → replace with conversational
## 🚨 CRITICAL FINDING: Gen Z ≠ Revenue (May 9, 2026)

**This is the single most important insight for content strategy.**

From academic research (Tra Vinh University, 394 respondents, SEM analysis):

| Factor | Beta | P-value | Significance |
|--------|------|---------|--------------|
| **KOL/KOC Influence** | 0.580 | <0.001 | ✅ MOST IMPORTANT |
| Content Trust | 0.301 | <0.001 | ✅ Important |
| Entertainment Value | 0.014 | 0.790 | ❌ ZERO — not significant |

**⚠️ Entertainment does NOT drive purchases.** Gen Z buys because they trust the person recommending, NOT because content is entertaining.

**Practical implications:**
- Funny/entertaining scripts get views but **don't convert**
- Authentic personal recommendation scripts **convert better**
- "Trust me because I actually used it" > "This product is so amazing everyone needs it"

**Script strategy shift:**
- Lead with PERSONAL EXPERIENCE ("anh đã dùng 2 tuần...")
- Add SOCIAL PROOF ("164K đơn trong 7 ngày" or "bạn mình cũng mua rồi")
- Keep it REAL — Gen Z smells fake marketing from miles away
- **Stop chasing "funny viral" → Focus on trust-building content**

---

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
## 🚨 NEW TREND (May 4 viral): "Sound Các Câu Nói Buồn Của Úc Phượng"
- **Meaning:** Sad, dramatic voice over mundane content
- **Format:** Slow, emotional voice → contrast with normal/funny video
- **Why it viral:** Contrast humor — sad music + everyday content = comedy
- **Comedy technique:** Nội dung thật: hết tiền → ghép sound buồn → thành "bi kịch cuộc đời"
- **Best for:** Product reveals with emotional storytelling, "twist" reveals
- **Voice:** Chậm, trầm, hơi "kịch nhưng thật"
- **Source:** 35express.org (May 4, 2026)

## Weekend Strategy (Saturday/Sunday Specific)
- **Higher female engagement** on weekends
- **Focus:** Aesthetic products, beauty, accessories
- **Gen Z drives virality** Sat/Sun → Millennials convert Mon-Fri
- **Sound strategy:** Piano Solo Cherry Blossom (soft aesthetic) for morning/afternoon, upbeat (Lùi Lại Lấy Đà) for evening
- **Hook focus:** POV meoxink, ra dại reaction, aesthetic reveal

## Sources
- Products: https://findniche.com/tiktok/trending-products-vn
- Sounds: https://chartex.com/tiktok/sounds/7-days/vietnam
- Trends: https://35express.org (search "trend")
- Slang: https://trykaiwa.com/blog/vietnamese-gen-z-slang-phrases-2026
- `references/tiktok-algorithm-may-2026.md` — comprehensive CHR, fee math, commerce signals, completion rate, demographic split
- `references/tiktok-shop-product-links-may-2026.md` — Real TikTok Shop product links by trending keyword (May 14-15, 2026). Affiliate-ready PDP links for cooling products, beauty, lifestyle. Built from actual Shopee/TikTok search data.
- `references/tiktok-trending-products-may-13-2026.md` — Body Mist LACOON, Cooling Neck Ring, Mini Cooler 2nd push, #StandBanhMi, "thơm vãi" sensory intensifier (May 13 session findings)
- `references/may-14-2026-findings.md` — LỌ vs LỎ critical distinction, Summer Cooling margins, FindNiche top products, Gen Z slang update (May 14 orchestrator session)
- `references/may-15-2026-findings.md` — Sunscreen ASUNMEE SPF50+ push, Summer peak data (+21% GMV), Top products chart, weekend calendar (May 15 session)
- **Ecom_Linus AI UGC Model:** See `references/ecom-linus-affiliate-model.md` — Glitchy setup, Vietnam affiliate networks, AI tools stack, angle research methodology
- Gen Z Research: Tra Vinh University Journal of Science — "Factors Affecting Gen Z Online Purchase Intention on TikTok Shop"
- Product research: https://findniche.com/tiktok/trending-products-vn

## Output Paths

**⚠️ CRITICAL: Workers use TWO path variants — check BOTH (2026-05-13)**
- Workers write to `/Users/tuananh4865/hermes/workers/*/outputs/` (primary)
- BUT the skill docs and some checks look at `/Users/tuananh4865/.hermes/workers/*/outputs/`
- These may be the SAME directory (symlink) or DIFFERENT — always check both
- Wiki is at `/Volumes/Storage-1/Hermes/wiki/` (separate volume)
- The cron output dir is `/Users/tuananh4865/.hermes/cron/output/{job_id}/`

**⚠️ CRITICAL: Always use absolute paths in cron/worker context (2026-05-10)**
- Tilde (`~`) does NOT expand in cron environment ($HOME=/var/empty)
- Workers write to `/Users/tuananh4865/hermes/workers/*/outputs/` (local Mac path)
- See `references/worker-output-path-architecture.md` for full architecture

**Actual worker output locations by cron job ID:**
| Cron ID | Worker | Schedule | Path |
|---------|--------|----------|------|
| `ce3701b4dcdd` | Content Creator Morning | 8AM | `/Users/tuananh4865/.hermes/cron/output/ce3701b4dcdd/` |
| `50bc2c2dfbb3` | Content Creator Evening | 6PM | `/Users/tuananh4865/.hermes/cron/output/50bc2c2dfbb3/` |
| `e4fb0c36e9f7` | Research Analyst Morning | 8:30AM | `/Users/tuananh4865/.hermes/cron/output/e4fb0c36e9f7/` |
| `1c425ba42980` | Research Analyst Evening | 6:30PM | `/Users/tuananh4865/.hermes/cron/output/1c425ba42980/` |

**Cron output dir — list today's files:**
```bash
ls -lt /Users/tuananh4865/.hermes/cron/output/*/2026-$(date +%Y-%m-%d)*.md 2>/dev/null
```

## Pitfalls (AVOID THESE)

### Script Structure Mistakes
- ❌ **Listing specs instead of telling story** — "product has 200ml, made of bamboo, organic" = boring. Instead: "anh dùng 2 tuần rồi, da em nó mềm lắm luôn"
- ❌ **Template repetition** — using same hook structure as previous script. Each script MUST be unique
- ❌ **Dead phrases** — "đỉnh nóc kịch trần", "quất một phát", "đã X là Y" = instantly dated
- ❌ **"Mua ngay!" CTA** — too pushy, triggers algorithm pressure detection, lower distribution
- ❌ **Evening content without demo** — 6PM is prime filming time. Evening scripts should have physically demonstrable moments ("thử xem nào", "bật lên demo", "quay lại đây") rather than just description. Morning scripts can describe; evening scripts should SHOW.

### Pronoun Mistakes (INSTANT REJECT)
- ❌ "mấy đứa", "mấy chị", "các bạn", "các bạn ơi" — NEVER use these
- ✅ ONLY "anh" + "mấy con vợ"
- These are Tuấn Anh's signature pronouns — deviation breaks authenticity

### Research Mistakes
- ❌ **Skipping research** — writing script without fresh Gen Z slang research = outdated voice
- ❌ **Using stale trends** — trends older than 7 days = missed opportunity
- ❌ **Ignoring CHR** — partnering with red-CHR creators = affiliate content dies in algorithmic dead zone
- ❌ **Assuming URL content** — seeing a URL and assuming what it says without reading it first. The user is sharing content for a REASON — read it and confirm your understanding before acting. In 2026-05-13, agent assumed @ecom_linus tweet was about TikTok algorithm when it was actually about AI UGC affiliate marketing. This caused wasted research effort and user had to correct twice.
- ❌ **Single-path worker check** — checking only one path variant when workers can write to two different paths. Always check BOTH `/Users/tuananh4865/hermes/workers/*/outputs/` AND `/Users/tuananh4865/.hermes/workers/*/outputs/`. Workers may have fired (cron output exists) but written to a different path than expected.

### Algorithm Mistakes
- ❌ **Entertainment-focused scripts** — "entertainment value" has ZERO statistical impact on purchases (beta=0.014, p=0.790). Views ≠ revenue. Stop chasing funny viral.
- ❌ **Generic viral hooks** — "This is amazing everyone needs this" = no trust signal
- ❌ **No "click moment"** — if viewer doesn't want to see price/detail, algorithm won't push
- ❌ **Generic discovery hooks without trust** — must add personal experience or social proof

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

## X/Twitter Integration — Absorbed from `xitter`

`xitter` (third-party x-cli wrapper) is **deprecated**. All X/Twitter operations should use `xurl` instead.

**Why:** `xurl` is the official X developer platform CLI, maintained by X's team, supports OAuth 2.0 PKCE with auto-refresh, covers a larger API surface (DMs, media, raw v2 endpoints), and uses the official API rather than a third-party Python wrapper.

**Migration:** If you see `xitter` referenced, update to use `xurl` commands instead.

## Research Analyst — Absorbed into content-creator

This skill has been merged into `tiktok-viral-script` as section **Research Analyst Workflow**.

The content-creator workflow is a two-role system:
- **Research Analyst** = market economics, commission math, product validation, fee analysis (evening research cron)
- **Content Creator** = scripts, trends, daily calendars, Gen Z slang

Both roles are part of the same content-creator business. They are documented together in this single skill under their respective sections.

Key references absorbed from `research-analyst`:
- Fee structure (12.5-14.5% platform, 5% transaction, ₫3,000/order — May 2026)
- Commission survival math (60%+ gross margin OR 15%+ commission required)
- Coolmate case study (₫14.61B booking revenue, 1,370 KOCs, 369 videos/day)
- Summer Cooling margins (neck fan 64%, cooling pillow 65%)
- Gen Z ≠ revenue insight (entertainment beta=0.014, KOL influence beta=0.580)
- Platform fee trajectory (2024: 2-3% → 2027E: 15-17%)

See: `references/commission-reference.md` (absorbed from research-analyst)

## Related
- [[hermes-autoresearch]] — Autoresearch loop for nightly research runs
- [[xurl]] — X/Twitter trends research (separate platform)
- `scripts/tráhn-qa-gate.sh` — Runtime TRÁHN enforcement (exit 1 = block delivery)
- `references/tiktok-browser-access.md` — TikTok CAPTCHA workarounds, competitor research via news scraping
- `references/worker-dual-path-discovery.md` — Worker output dual-path issue: `/hermes/workers/` vs `/.hermes/workers/` (2026-05-13)

## Fail-Fast Protocol

**Signal:** After 2 `browser-harness` attempts, if `page_info()` returns CAPTCHA ("Drag the slider") → **HARD STOP** on browser approach. Switch to web search + news scraping immediately.

**Why waste more attempts:** TikTok's CAPTCHA is deterministic for CDP sessions — retrying the same approach yields identical results. Each additional attempt risks IP temporary block and session contamination.

**Detection method:**
```python
# browser-harness
goto_url("https://www.tiktok.com/@username")
wait_for_load()
text = js("document.body.innerText")
# If contains "Drag the slider" or "puzzle" → CAPTCHA detected
# If shows only profile stats (followers, likes) but no video links → partial block
```

**Correct sequence:**
1. Try `browser-harness` → get profile text
2. If CAPTCHA present → try 1 more refresh with wait(5)
3. If still CAPTCHA after 2 attempts → hard stop, switch to `mcp_exa_web_search_exa` + news site parsing
4. Report findings with "Data from [source] on [date]" notation

**Session example (today):** Lê Tuấn Khang profile research:
- Browser opened profile → CAPTCHA detected
- Tried `js()` to extract video links → empty array
- Tried clicking/slider solutions → failed
- Switched to `mcp_exa_web_search_exa` → got complete viral video data from news sites
- **Result:** 300M view viral video identified, profile stats confirmed, full competitor brief delivered

**Key insight:** Profile stats (13.3M followers, 156.5M likes) pass through HTML. Video-level data blocked by CAPTCHA. Use news sites for historical video metrics.
