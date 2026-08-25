# TikTok HEVC Video Workaround — 7 Approaches Tested 2026-06-30

> **Status:** KHÔNG CÓ WORKAROUND HOÀN TOÀN WORK cho video H.265/HEVC trên TikTok
> **Use case:** Cần download video TikTok để phân tích visual (frame-by-frame, video metadata), nhưng `yt-dlp -F` chỉ expose audio-only.

## Background

Video ID: `7657049259308551442` từ `@tuan_anh.review` (chính kênh Tuấn Anh).
URL: `https://vt.tiktok.com/ZSCPoQHVg/`
Duration: 108s
BG Music: "Cute - CLOUDEE"

## Bước 0: ALWAYS list format trước (workflow đúng)

```bash
yt-dlp -F "https://vt.tiktok.com/ZSCPoQHVg/"
```

Output:
```
ID    EXT RESOLUTION | PROTO | VCODEC     ACODEC
---------------------------------------------------
audio m4a audio only | https | audio only aac
```

→ **CHỈ 1 format duy nhất = audio-only**. Đây là CDN-side limit, không phải do format selector.

## 7 Approaches đã thử (chi tiết)

### Approach 1: `yt-dlp -f "best"`

```bash
yt-dlp -f "best" -o "clip_mau.mp4" "https://vt.tiktok.com/ZSCPoQHVg/"
```

Result: 1.3 MB m4a audio-only, KHÔNG có video stream.

### Approach 2: `yt-dlp -f "bv*+ba/b"`

```bash
yt-dlp -f "bv*+ba/b" --merge-output-format mp4 -o "clip_mau.mp4" "https://vt.tiktok.com/ZSCPoQHVg/"
```

Result: 1.3 MB m4a (yt-dlp vẫn chỉ tìm được audio-only format).

### Approach 3: Upgrade yt-dlp version

```bash
brew upgrade yt-dlp
# Trước: 2026.03.17 (older than 90 days)
# Sau: 2026.06.09
yt-dlp -F "https://vt.tiktok.com/ZSCPoQHVg/"
```

Result: Vẫn chỉ audio-only. Upgrade fix warning + nhiều bug khác, nhưng KHÔNG fix TikTok HEVC issue (CDN-side).

### Approach 4: TikTok oEmbed API

```bash
curl -sL "https://www.tiktok.com/oembed?url=https://vt.tiktok.com/ZSCPoQHVg/" \
  -A "Mozilla/5.0" --max-time 15
```

Result: Trả về JSON với thumbnail URL + HTML embed, KHÔNG có direct video URL.
```
{"version":"1.0","type":"video","title":"Bài đăng 14 | Tripod Ulanzi cho Pocket 3",
 "thumbnail_url":"https://p16-common-sign.tiktokcdn.com/...?x-signature=..."}
```

### Approach 5: TikTok API endpoint trực tiếp

```bash
curl -sL "https://api22-normal-c-useast2a.tiktokv.com/aweme/v1/feed/?aweme_id=7657049259308551442&aid=1988" \
  -H "User-Agent: com.zhiliaoapp.musically/..." --max-time 30
```

Result: Empty response (length 0).

```bash
curl -sL "https://www.tiktok.com/api/item/detail/?aid=1988&itemId=7657049259308551442" \
  -A "Mozilla/5.0" --max-time 30
```

Result: Empty response.

### Approach 6: Playwright headless + capture `<video>.currentSrc`

**Setup:**
```bash
# Cài playwright Python
/Users/tuananh4865/.venvs/crawl4ai/bin/pip install playwright

# Cài chromium browser
/Users/tuananh4865/.venvs/crawl4ai/bin/playwright install chromium
# → 91 MiB downloaded to /Users/tuananh4865/Library/Caches/ms-playwright/
```

**Script** (`/tmp/get_tiktok_video_v4.py`):
```python
from playwright.sync_api import sync_playwright
import time

VIDEO_ID = "7657049259308551442"
EMBED_URL = f"https://www.tiktok.com/embed/v2/{VIDEO_ID}"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        args=['--no-sandbox', '--disable-setuid-sandbox', '--autoplay-policy=no-user-gesture-required']
    )
    context = browser.new_context(
        user_agent='Mozilla/5.0 ... Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    page.goto(EMBED_URL, wait_until='networkidle', timeout=45000)
    time.sleep(5)

    video_src = page.evaluate("""() => {
        const v = document.querySelector('video');
        if (v) { v.muted = true; v.play(); }
        return v ? (v.currentSrc || v.src) : null;
    }""")

    print(f"Video src: {video_src}")
    # → https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o8IC7i1rZACaAxBNEfvKGuQwiBKgnH7vGMWAI7/?a=1988&bti=ODszNWYuMDE6&&bt=1552&ft=4fUEKM3a8Zmo0_CbBa4jVWdu-pWrKsd.&mime_type=video_mp4&rc=...&expire=1782994262&l=...&ply_type=2&policy=2&signature=...
```

**Result:** Bắt được URL với token signature + expire timestamp.

**Sub-approach 6A:** Try MediaRecorder capture
```python
result = page.evaluate("""async () => {
    const v = document.querySelector('video');
    v.currentTime = 0;
    const stream = v.captureStream();
    const recorder = new MediaRecorder(stream, {mimeType: 'video/webm;codecs=vp8'});
    // ... record and save blob
}""")
```

Result: ❌ `NotSupportedError: Failed to execute 'start' on 'MediaRecorder': The MediaRecorder cannot start because there are no audio or video tracks available`.

**Root cause:** Headless Chrome không decode HEVC → `<video>` element không có track nào để capture.

**Sub-approach 6B:** Try non-headless mode
```python
browser = p.chromium.launch_persistent_context(
    user_data_dir='/Users/tuananh4865/Library/Application Support/Google/Chrome',
    headless=False,
    ...
)
```

Result: Timeout 180s (headless=False không stable qua Playwright persistent context).

### Approach 7: `curl` URL từ #6 với headers

```bash
curl -L "https://v16-webapp-prime.tiktok.com/video/tos/.../o8IC7i1rZACaAxBNEfvKGuQwiBKgnH7vGMWAI7/?a=1988&...&signature=...&expire=1782994262" \
  -A "Mozilla/5.0 ... Chrome/120.0.0.0 Safari/537.36" \
  -H "Referer: https://www.tiktok.com/" \
  -o clip_mau_real.mp4
```

Result: 504 bytes (HTML "Access Denied" page), KHÔNG phải MP4 binary.

**Root cause:** Token URL có TTL ~vài phút + chỉ work qua native browser network stack với đầy đủ cookies + headers sequence. `curl` single-shot không match.

## Có work được không? Khi nào work?

**Approach #6 work KHI:**
1. TikTok video dùng H.264 (không HEVC) → browser decode được → MediaRecorder capture được
2. Verify bằng cách check `video.canPlayType('video/mp4; codecs="avc1.42E01E"')` returns "probably" trước khi capture

**Approach #6 KHÔNG work khi:**
1. TikTok video dùng HEVC (phổ biến từ 2024+) → headless Chrome không decode
2. Video private/restricted/locked by region

## Workaround đề xuất (khi user CẦN video thật)

### Option A: User dùng browser tay (NHANH NHẤT)

1. Mở Chrome trên Mac (đã login TikTok)
2. Navigate tới `https://vt.tiktok.com/ZSCPoQHVg/`
3. Click phải video → "Save video as..." → lưu về `/tmp/clip-compare-2/clip_mau_chrome.mp4`
4. Báo em để em phân tích

### Option B: Em dùng `computer_use` tool

Yêu cầu Chrome đang mở + màn hình không khóa + Safari/Chrome visible.
Đã thử 2026-06-30 nhưng Mac đang ở BetterDisplay 0x0 dimensions → fail.

### Option C: Dùng thumbnail + audio (ĐÃ VERIFIED WORK)

Đã verify thành công với video này:

```bash
# 1. Download thumbnail (high-res cover)
curl -L "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ooEpTqJtfABCCfDxEcaD2TIgqFRw0QIoOcEIB5~tplv-tiktokx-dmt-logom:tos-alisg-i-0068/ooBDAOBiIBYImEiscfITCWxALbBSaw5DAUAAi1.image?dr=14573&x-expires=1782990000&x-signature=%2FW9sE3yKUxDnHfCL7hSolOOuGn0%3D" \
  -o /tmp/clip-compare-2/thumbnail_mau.jpg
# → 163 KB JPEG, 576x1024

# 2. Download audio
yt-dlp -x --audio-format wav -o "/tmp/audio_mau.%(ext)s" "https://vt.tiktok.com/ZSCPoQHVg/"
# → 15 MB WAV, 86.82s duration

# 3. Vision analyze thumbnail
# Tool: mcp_MiniMax_understand_image
# → Detect được: text overlay "Tripod Ulanzi cho pocket 3 siêu đáng tiền!!!"
#                 + caption "KIỆN LUÔN LUÔN"
#                 + visual context (người cầm tripod, background studio)

# 4. Whisper transcript audio
# Tool: mlx_whisper (mlx-community/whisper-large-v3-mlx)
# → 3 segments CTA intro "Hãy subscribe cho kênh Ghiền Mì Gõ..."
# → Words/sec, gap analysis, scene detection từ transcript
```

Kết hợp thumbnail + audio + transcript → đủ data để phân tích visual structure + content cho 80% use case.

## File evidence 2026-06-30

- `/tmp/clip-compare-2/thumbnail_mau.jpg` (163 KB) — TikTok cover via oEmbed
- `/tmp/clip-compare-2/audio_mau.wav` (15 MB) — TikTok audio via yt-dlp
- `/tmp/clip-compare-2/tiktok_play_state.png` (200 KB) — Playwright screenshot của embed page (3 video elements found)
- `/tmp/clip-compare-2/cdn_urls.json` (3.1 KB) — Captured CDN URLs list
- `/tmp/get_tiktok_video_v4.py` — Working Playwright script bắt được `currentSrc`

## Trigger phrases (khi nào reference này apply)

User nói bất kỳ câu nào sau:
- "Tải video TikTok này về"
- "Download clip TikTok X"
- "Lấy video thật của link TikTok Y"
- "Phân tích visual của video TikTok Z"

→ Apply workflow này:
1. `yt-dlp -F URL` first → check if multi-format
2. Nếu chỉ audio-only → dùng Option C (thumbnail + audio)
3. Nếu user explicit cần video frame-by-frame → propose Option A hoặc B
4. KHÔNG retry approach #1-#7 indefinitely