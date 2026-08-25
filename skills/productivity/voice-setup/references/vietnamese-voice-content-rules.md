# Vietnamese Voice Content Rules (Tuấn Anh's TikTok)

> Hard rules for generating Vietnamese TTS voice messages for TikTok scripts.

## Source

User verbatim feedback 21/07/2026:
> *"Không nêu giá và mã sản phẩm! Sản phẩm là tripod thì gọi nó là chiếc tripod này thôi không gọi mã MA66 ai hiểu?"*

User also said: *"Giảm speed xuống 1.4 mặc định!"*

## Hard rules

### 1. NEVER mention prices

❌ **BAD:**
- "Giá 599k"
- "Trả góp 67k một tháng"
- "Rẻ hơn ly cafe Đà Lạt mà balo nhẹ đi được 1,5 ký" — still has the cost-comparison framing

✅ **GOOD:**
- Remove all price mentions entirely. Let social proof do the work ("3.599 người đã mua", "4.9 sao").
- "Freeship luôn, hoàn tiền 14%" — this is OK because it's about perks, not the price itself.

**Why**: User finds price mentions break the storytelling flow of the voice. The voice should feel like someone sharing a tip, not a salesperson reciting specs.

### 2. NEVER mention product model codes

❌ **BAD:**
- "MA66" (model code for ULANZI Magnetic Quick Release)
- "Pocket 3" (DJI camera model)
- "GOOJODOQ BD3035" (product SKU)
- "ARMAF Odyssey 200ml"

✅ **GOOD — use everyday names:**
- "Chiếc tripod này" (this tripod)
- "Máy quay" (camera) — generic
- "Cây tripod"
- "Cái loa bluetooth này"
- "Chai nước hoa này"

### 3. Trust signals ARE allowed

These are NOT product codes, they are social proof:
- ✅ "3.599 người đã mua"
- ✅ "4.9 sao trên 96 review"
- ✅ "780 người mua trong 30 ngày"
- ✅ "Sáu nghìn sáu trăm người mua lại"
- ✅ "Có chị creator trên Instagram khen đây là favorite của chị"

Numbers like review counts, sale counts, ratings are fine. The rule is about **product identifiers** (model codes, SKUs) and **prices**.

## When these rules DON'T apply

These rules apply to **voice audio output** (the TTS script).

Written artifacts can keep prices and codes for record-keeping:
- ✅ `wiki/projects/tuan-anh-review-tiktok/products/<slug>.md` — keep prices, codes, full specs (for research)
- ✅ `wiki/projects/tuan-anh-review-tiktok/scripts/<slug>-v1.md` — keep prices, codes in written scripts (editors need them for on-screen text)
- ❌ Voice script content (the TTS input string) — strip prices and codes per rules above

## Default speed: 1.4x

Apply via ffmpeg atempo (NOT edge-tts `--rate`, which silently fails):
```python
subprocess.run(["ffmpeg", "-y", "-i", "input.mp3", "-filter:a", "atempo=1.4",
                "-vn", "-c:a", "libmp3lame", "-b:a", "192k", "output-1.4x.mp3"])
```

User feedback 21/07: 1.5x was too fast for comfortable listening, 1.4x is the sweet spot.

## Rate limit retry pattern

When generating **N consecutive voice files** (3+ files in a row), edge-tts may hit rate limits:

**Symptom**: exit code 1, 0KB output file, stderr contains `asyncio.run(amain)` and `util.py:141`

**Fix recipe**:
```python
import time
import subprocess

def generate_voice(text, voice_path, max_retries=3):
    for attempt in range(max_retries):
        r = subprocess.run(
            ["edge-tts", "--voice", "vi-VN-NamMinhNeural", "--text", text, "--write-media", voice_path],
            capture_output=True, text=True, timeout=120
        )
        if r.returncode == 0:
            return True
        # Rate limit or transient failure: wait + retry
        wait = 5 * (attempt + 1)  # 5s, 10s, 15s
        print(f"Attempt {attempt+1} failed, waiting {wait}s...")
        time.sleep(wait)
    return False

# Optional: test with minimal text before retrying full script
def check_edge_tts_alive():
    test_path = "/tmp/test-voice-alive.mp3"
    r = subprocess.run(
        ["edge-tts", "--voice", "vi-VN-NamMinhNeural", "--text", "Test", "--write-media", test_path],
        capture_output=True, text=True, timeout=30
    )
    return r.returncode == 0
```

**Verified case 21/07/2026**: 3-version TikTok script voice generation:
- V2A: failed first attempt (rate limit) → 10s wait → retry succeeded
- V2B: succeeded on first try
- V2C: succeeded on first try

## Complete workflow

1. **Strip prices and codes** from the written script → create voice-only version
2. **Generate** via edge-tts CLI 1.0x (don't use --rate flag)
3. **Speed up** via ffmpeg atempo=1.4 (if user requests speed up; default = 1.4x for Tuấn Anh)
4. **Verify** with ffprobe: duration should be 1/1.4 of original
5. **Send** via `MEDIA:/absolute/path.mp3` in Telegram reply

## Checklist before generating

- [ ] Removed all price mentions (e.g., 599k, 67k)
- [ ] Replaced model codes with everyday names (e.g., "chiếc tripod này" not "MA66")
- [ ] Kept social proof numbers (review counts, ratings, sale counts)
- [ ] Generated via edge-tts CLI (NOT the `text_to_speech` tool, which fails silently on long Vietnamese)
- [ ] Applied atempo=1.4 (default for Tuấn Anh)
- [ ] Verified duration ratio = 1.40x via ffprobe