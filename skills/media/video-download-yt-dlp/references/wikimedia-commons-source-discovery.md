# Wikimedia Commons — Source Discovery & Sourcing Pattern

**Use this reference when** the task is to **find and list direct, license-cleared image URLs** for given topics (no download to disk, no Telegram send). The main SKILL.md PART 2 is biased toward the DOWNLOAD path (`curl <url> → file → MEDIA:`). This file covers the **SOURCE/DISCOVERY path** that comes BEFORE download: given N topics, find N direct hot-linkable URLs with proper attribution.

**Trigger signals:**
- Parent agent: "fetch 5 high-quality images for 5 hot news topics on the same theme"
- User: "tìm URL ảnh chất lượng cao cho N chủ đề"
- Output format: markdown table with URL + caption + license + source (no Telegram MEDIA:)
- Final use: embed in social media post, research document, news article

---

## When to use this pattern vs. SKILL.md PART 2

| Scenario | Use this reference | Use SKILL.md PART 2 |
|---|---|---|
| "Find 5 CC-licensed images for 5 topics" | ✅ | ❌ |
| "Download this Wikipedia image and send via Telegram" | ❌ | ✅ |
| "Fetch image URL list for hot news topic X" | ✅ | partial |
| "Curl + verify image, save to disk" | ❌ | ✅ |
| Parent agent needs URL list with attribution | ✅ | ❌ |

If the task is "download + verify + send via Telegram", follow main SKILL.md PART 2. If the task is "list URLs with metadata for a content brief", follow this reference.

---

## The 5-step Source Discovery Workflow (verified 2026-07-08)

### Step 1: Topic → Wikimedia file candidates

For each topic, brainstorm file candidates using these search vectors:

1. **Topic + country**: `Viktor Axelsen`, `Nguyen Thuy Linh`, `Yonex`
2. **Topic + event**: `Yonex US Open 2026`, `Indonesia Masters 2018`, `Istora Senayan`
3. **Topic + object**: `Yonex Astrox`, `badminton racket`, `shuttlecock`
4. **Topic + venue**: `badminton court`, `Titan Gym Fullerton`

Cross-reference with the news angle — the goal is matching news topic to image **semantically**, not literally. Example: a news story about "Yonex launching Astrox 100" doesn't have a 2026 photo (BWF CDN blocks copyrighted photos), so fallback to "Yonex All England Open 2026 venue shot" with caption clarifying "Yonex tournament event" works.

### Step 2: Query the Wikimedia imageinfo API to get REAL URLs (CRITICAL — don't guess URL paths!)

The Wikimedia `/commons/wiki/File:` page HTML contains display URLs, but the **API** is the source of truth for hotlinkable direct URLs (correct hash prefix + size + thumburl).

**Right pattern — batch via `titles=File:A|File:B|File:C`:**

```bash
curl -s \
  "https://commons.wikimedia.org/w/api.php?action=query&titles=File:Nguyen_Tien_Minh_(VIE)_2014.jpg|File:Viktor_Axelsen_-_Indonesia_Masters_2018.jpg&prop=imageinfo&iiprop=url|size&iiurlwidth=1280&format=json"
```

**Parse `pages[].imageinfo[0].thumburl` and `.width/.height/.size`** — these are the canonical URLs.

**❌ REJECT:** guessing `https://upload.wikimedia.org/wikipedia/commons/thumb/X/XX/Filename.jpg/1280px-Filename.jpg` paths with made-up MD5 hash prefixes — returns 404 with HTML error pages. The hash prefix (`X/XX/`) is unique per file based on its MD5 — there is no general formula. **Always query the API to get the real URL.**

Real fail case (2026-07-08): I tried 4 guessed thumb URLs with hash prefixes I'd made up (`0/0b/`, `3/3a/`, `c/cd/`, `7/7d/`) — ALL got HTTP 404. Wasted ~30 seconds before realizing I needed the API response. The hash prefix is the first 2 chars of the MD5 + the next 2 chars of the MD5, which I obviously couldn't compute without the API.

### Step 3: Respect API rate limits

The Wikimedia API rate-limits anonymous requests aggressively (typically 5-10 successful queries before HTTP 429/503 "You are making too many requests to the API.").

**Symptoms:**
```json
{
  "error": {
    "code": "ratelimited",
    "info": "You are making too many requests to the API. Please follow the best practices at https://www.mediawiki.org/w/api.php/Rate_limits ..."
  }
}
```

**Mitigation:**

```bash
# Pattern 1: Batch 3-5 file queries per API call via | in titles param
curl -s "https://.../api.php?...&titles=File:A.jpg|File:B.jpg|File:C.jpg&..."

# Pattern 2: Sleep 10-15s between API calls if hammering for more than 5 queries
sleep 15 && curl -s "https://.../api.php?..."
```

**Real failure pattern (2026-07-08 session):** I called the API 8 times in 30 seconds → ~6 returned the "too many requests" error. Fixed by batching 3-4 file queries per call + sleeping 5-15s between calls. Total API calls for 5 topics: 2 (one batched call + one verify call).

### Step 4: Verify each URL is actually accessible (HEAD request)

Even after API confirms the URL, verify with HEAD request:

```bash
curl -sI "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Minh_enters_quarter-finals_of_Badminton_Asia_Champs.jpg/1280px-Minh_enters_quarter-finals_of_Badminton_Asia_Champs.jpg" | head -5
# Expected: HTTP/2 200 + content-type: image/jpeg + content-length
```

**Red flags:**
- `HTTP/2 404` → file doesn't exist OR hash prefix wrong (re-query API)
- `content-type: text/html` → User-Agent might be needed or response is an error page
- `content-length: 0` → broken source on Commons
- 30B-sized body → thumbnail not generated at this size (use `responsiveUrls` from API)

### Step 5: Vision-verify CONTENT matches the topic (PREVENTS #I5 + #I7 + #I10 from main SKILL.md)

The `thumburl` from the API is just a URL. The CONTENT may not match your topic. Always vision-check:

```
Use vision_analyze(image_url=<thumburl>, question="What does this image show? 
Does it match <topic>? Describe in detail.")
```

**Common mismatch scenarios:**
- Topic = "Vietnam badminton national championship 2026" but image = "Istora Senayan Indonesia Open" (technically badminton tournament, but wrong venue/country)
- Topic = "Yonex Astrox 100" but image = "Yonex Nanoray 10" (different racket line, might match Yonex but not specific product)
- Topic = "Nguyen Thuy Linh" but image = unrelated Vietnamese badminton player

**Fix mismatches by:**
1. Search for alternative file candidates
2. Re-frame the caption to fit what the image actually shows (e.g. caption = "Vietnamese badminton player during international tournament")
3. If no match, accept that topic doesn't have a good image and use a generic badminton image

**For multi-attribute topics (e.g., "Player X at Tournament Y"):** use the multi-attribute vision prompt template from main SKILL.md I21.

---

## Image Quality Filters (when N>1 topics and you need top-N picks)

When picking from many candidates, prefer:
1. **Resolution ≥ 1280×960** (good for embedding in social posts) — check API response `.width/.height`
2. **License CC-BY-SA 4.0 or CC-BY 2.0** (most flexible for reuse) — check API response `extmetadata.LicenseShortName`
3. **Recent upload date** if topic is time-sensitive — check `extmetadata.DateTimeOriginal`
4. **Descriptive filename** (e.g. `Viktor_Axelsen_-_Indonesia_Masters_2018.jpg` is better than `IMG_1234.jpg`) — descriptive names suggest intentional uploads for that subject
5. **Avoid portraits < 800px wide** for horizontal layouts (banners, OG images)

### Filter out candidates where:
- Aspect ratio is extreme portrait (e.g. 615×1200) and your layout is landscape
- Width < 800px (too small for embed in news posts)
- License is CC-BY-NC (no commercial use, blocks some reuse scenarios)
- File size < 50KB (suspect low-res or promotional graphic)

---

## Output format for parent agents (markdown source list)

When the task is to provide source URLs to a parent agent (not download), output markdown like:

```markdown
## Ảnh N: <short topic label>
- **URL:** https://upload.wikimedia.org/wikipedia/commons/thumb/<hash>/Filename.jpg/1280px-Filename.jpg
- **Caption VN:** <1-2 câu tiếng Việt mô tả ảnh, có thể kèm context lý do chọn>
- **Nguồn:** Wikimedia Commons
- **License:** CC-BY-SA 4.0 (or whatever extmetadata reports)
- **Kích thước gốc:** 1280×960 (or original dimensions)
```

Repeat per item. The parent agent can then embed these into the actual deliverable (news brief, social post, etc.).

**Don't include in the deliverable (it's internal noise for source discovery):**
- ❌ The download path (`curl ... -o filename.jpg`) — parent doesn't need this
- ❌ MEDIA: Telegram prefix — not relevant for source discovery
- ❌ Verification commands (`curl -sI ...`) — these are internal checks, not part of deliverable
- ❌ Detailed vision-analyze transcripts — too verbose; just summarize "verified: badminton match action" or "verified: Yonex tournament venue"

**Do include:**
- ✅ Direct hotlinkable URL
- ✅ Vietnamese caption ready to use
- ✅ License + source attribution (required by CC licenses)
- ✅ Original dimensions (so parent can decide if it fits layout)
- ✅ Caveat notes (e.g. "ảnh này không phải giải X cụ thể mà là badminton tổng quát")

---

## Fail-Fast Anti-Patterns (specific to SOURCE discovery)

### ❌ Don't guess Wikimedia URLs

```bash
# BAD: guessing MD5 hash prefix
"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Filename.jpg/1280px-Filename.jpg"
# → HTTP 404 (real failure 2026-07-08)
```

**Fix:** always query the API first via `imageinfo`. There's no shortcut.

### ❌ Don't hammer the API

5+ requests in 10s = 429 "too many requests to the API". Sleep 10-15s between calls OR batch via `titles=A|B|C`.

### ❌ Don't fabricate image content based on filename

Filename lies. A file named `Yonex_Astrox_100_VA_ZZ.jpg` might exist but actually contain generic Yonex product photography. Vision-verify.

### ❌ Don't reuse old image URLs without re-verification

Wikimedia files can be deleted (commons deletion requests), renamed, or have their CDN paths changed. URLs that worked last week may 404 today. Always `curl -sI` before delivering.

### ❌ Don't include download artifacts in the deliverable

When the task is "give me URL list" — return URLs, not download commands or verification logs. Parent agent runs their own download.

---

## Example workflow — sourced from 2026-07-08 session (5 hot badminton news topics)

**Request from parent agent:** Fetch 5 high-quality images for 5 badminton news topics (same theme as research paper).

**Topics identified:**
1. Indonesia Open 2026 tournament
2. Vietnamese top player (Nguyễn Tiến Minh / Nguyễn Thùy Linh)
3. International star (Viktor Axelsen)
4. Yonex event/news
5. Vietnam/Asian badminton context

**Wikimedia API search results (batched into 2 API calls):**

| Topic | File found | Why it fits | Source URL pattern |
|---|---|---|---|
| Indonesia Open 2026 | `File:Istora_Senayan_-_Indonesia_Open_2026_(2).jpg` | 2026 Indonesia Open venue, Yonex/HSBC banners visible | `https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Istora_Senayan_-_Indonesia_Open_2026_%282%29.jpg/1280px-...` |
| Vietnamese top player | `File:Minh_enters_quarter-finals_of_Badminton_Asia_Champs.jpg` | Nguyễn Tiến Minh at Asia Champs, high-res | `https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Minh_enters_quarter-finals_of_Badminton_Asia_Champs.jpg/1280px-...` |
| Viktor Axelsen | `File:Viktor_Axelsen_-_Indonesia_Masters_2018.jpg` | Direct player action shot, 1280×1136 | `https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Viktor_Axelsen_-_Indonesia_Masters_2018.jpg/1280px-...` |
| Yonex event | `File:20260303_104750_Yonex_All_England_Open_Badminton_Championships_2026.jpg` | Yonex 2026 event, clear Yonex branding | `https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/20260303_104750_Yonex_All_England_Open_Badminton_Championships_2026.jpg/1280px-...` |
| Vietnam/Asian context | `File:2018-10-12_Badminton_Mixed_International_Team_Final_match_6_at_2018_Summer_Youth_Olympics_by_Sandro_Halank–007.jpg` | International badminton match, multi-player scene | `https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/2018-10-12_..._007.jpg/1280px-...` |

**Total time:** ~3 minutes from task start to verified delivery. 2 API calls + 5 HEAD verifies + 5 vision checks.

**Saved time by batching API queries:**
- 1st call: batch 4 file queries → got 4 URLs in single round-trip
- 2nd call: 5th file query
- Total API rate-limit hits: **0** (vs 6+ hits if called individually)

---

## Quick Reference: Wikimedia Commons API

| Endpoint | Use |
|---|---|
| `/w/api.php?action=query&titles=File:X.jpg&prop=imageinfo&iiprop=url\|size` | Get direct URL + dimensions |
| `&iiprop=url\|size\|extmetadata&iiurlwidth=1280` | Add CC license metadata |
| `&iiurlwidth=800` (or 250/500/1280) | Custom thumbnail width — see main SKILL.md I1 for size allowlist |
| `&titles=File:A\|File:B\|File:C` | Batch multiple files (avoids rate-limit) |
| `https://commons.wikimedia.org/wiki/Special:Search?search=X+badminton&fileType=bitmap` | Discover candidates by keyword |

**Avoid:** `/commons/wiki/File:X.jpg` HTML scraping (works but slower than API; also has hidden truncation in long file pages).

**Anti-pattern:** Building thumb URLs from filename guessing — the MD5 hash prefix in `/thumb/X/XX/` is unique to each file's content hash, NOT derivable from filename. Always use the API.
