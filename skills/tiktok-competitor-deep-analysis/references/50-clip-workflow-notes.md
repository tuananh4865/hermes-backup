# TikTok Competitor DEEP Analysis — Reference (2026-06-16)

**For the new `tiktok-competitor-deep-analysis` skill.**
**Last verified:** 2026-06-16 (50-clip @u40hoc.xay.kenh session)

## Quy trình chuẩn (7 bước)

### Step 1: Metadata (ALL videos)
```bash
yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(duration_string)s|%(view_count)s|%(timestamp)s" \
  "https://www.tiktok.com/@USERNAME" > /tmp/username-all-metadata.txt
```

### Step 2: Stratified sampling (Python)
```python
import random
random.seed(42)
videos.sort(key=lambda x: x['views'], reverse=True)
top10 = [v['id'] for v in videos[:10]]
mid_pool = [v for v in videos if 10000 <= v['views'] < 50000 and not v['is_reply']]
random.shuffle(mid_pool)
mid10 = [v['id'] for v in mid_pool[:10]]
replies = [v for v in videos if v['is_reply']]
replies.sort(key=lambda x: x['views'], reverse=True)
reply10 = [v['id'] for v in replies[:10]]
videos_by_date = sorted([v for v in videos if v['timestamp'] > 0], key=lambda x: x['timestamp'], reverse=True)
newest10 = [v['id'] for v in videos_by_date[:10]]
chosen = set(top10 + mid10 + reply10 + newest10)
remaining = [v for v in videos if v['id'] not in chosen]
random.shuffle(remaining)
random10 = [v['id'] for v in remaining[:10]]
```

### Step 3: Download (BATCH)
```bash
yt-dlp -S "res:540,ext:mp4:m4a" -o "u50-${vid}.mp4" \
  "https://www.tiktok.com/@user/video/${vid}"
```

### Step 4: Extract audio + Transcribe (PARALLEL 3 jobs)
```bash
for f in u50-*.mp4; do
  vid=$(basename "$f" .mp4)
  ffmpeg -y -i "$f" -ar 16000 -ac 1 -c:a pcm_s16le "/tmp/${vid}.wav" 2>/dev/null
done

for f in u50-*.wav; do
  vid=$(basename "$f" .wav)
  if [ ! -f "/tmp/${vid}-transcript.txt" ]; then
    mlx_whisper --model mlx-community/whisper-large-v3-mlx \
      --output-format txt --output-name "/tmp/${vid}-transcript" "$f" > /dev/null 2>&1 &
    while [ $(jobs -r | wc -l) -ge 3 ]; do sleep 0.5; done
  fi
done
wait
```

### Step 5: Frame extract (SKIP audio-only)
```bash
for f in u50-*.mp4; do
  vid=$(basename "$f" .mp4)
  if ! ffmpeg -y -i "$f" -vf "select=eq(n\,15),scale=320:-1" -vframes 1 "/tmp/${vid}-frame-1.jpg" 2>/dev/null; then
    ffmpeg -y -i "$f" -ss 1 -frames:v 1 "/tmp/${vid}-frame-1.jpg" 2>/dev/null
  fi
done
```

### Step 6: Analysis pipeline (text-based)
```python
# Hook patterns
hook_patterns = {
    'cau_hoi': r'(Sao|Tại sao|Vì sao|Thế.*\?|Bạn.*\?|Có.*\?)',
    'phu_dinh': r'(Đừng|Sai lầm|Không nên|Tránh)',
    'top_X': r'(Top \d+|\d+ cách|\d+ lỗi|\d+ mẹo|\d+ thứ|\d+ bước)',
    'tinh_nang_an': r'(Tính năng ẩn|Bí mật|Mẹo ẩn|Hidden)',
    'reply_user': r'(Replying|@)',
    'analogy': r'(cũng giống|cũng như|như là)',
    'cta_specific': r'(Hãy|Nhớ|Thử|Dùng|Làm theo)',
    'cta_provoke': r'(Còn bạn|Thế nên mọi người|Bạn vẫn đang)',
}
```

### Step 7: Honest reporting + sửa sai lầm cũ
- Báo cáo thẳng thắn hạn chế
- Sửa pattern cũ nếu sai + cite evidence

## Real session data: @u40hoc.xay.kenh (50 clips, 16/06/2026)

**Data collected:**
- 50/50 video downloaded
- 48/50 transcripts (1 silent, 1 missing)
- 31/50 frames (17 audio-only TikTok slideshows)
- ~50 phút tổng thời gian

**5 phát hiện MỚI (sửa sai lầm cũ):**
1. **Hook CÂU HỎI phổ biến nhất 52%** (không phải Tính năng ẩn như file 04 cũ nói)
2. **Sweet spot 150-179 từ + 60-69s** = view 2.37M avg
3. **Reply template lặp lại:** "Thử bán X bằng video ngắn, mọi người xem có muốn mua không"
4. **CTA "specific action" 42%** (KHÔNG phải provoke 4%) — SAI LẦM CŨ đã sửa
5. **TikTok slideshow (audio-only) = format phổ biến thứ 2** — không cần studio

**Bài học rút ra:**
- 4 viral clips ≠ 50 clips
- Always stratified sampling
- Always honest reporting về hạn chế

## Pitfalls gặp phải (cho future reference)

### 1. Format selector hardcoded
- ❌ `-f h264_540p_805128-0` — hardcoded ID fails
- ✅ `-S "res:540,ext:mp4:m4a"` — soft selection

### 2. Audio-only TikTok (17/50)
- Detection: `ffprobe -select_streams v -show_entries stream=codec_type`
- Workaround: skip frame extraction, dùng transcript only

### 3. Whisper model not cached
- ❌ `mlx-community/whisper-small` returns 401
- ✅ `mlx-community/whisper-large-v3-mlx` cached local

### 4. VLM API lỗi intermittent
- ❌ `vision_analyze` → "No models loaded"
- ✅ `mcp_MiniMax_understand_image` (but có thể trả 1033 system error → retry)

### 5. Sửa sai lầm cũ PHẢI ghi rõ
- Nếu file cũ nói X, file mới nói Y → ghi rõ evidence
- Không xóa — sửa + cite

### 6. Kịch bản "Ngày 1" — HỎI trước khi viết
- Gợi ý outline + 3-5 options
- KHÔNG viết chi tiết nếu user chọn "đợi review"

## Deliverable file
- `04-phan-tich-N-clip-V2-DEEP.md` in project root
- 14 sections (xem SKILL.md)

## Related
- `tiktok-viral-script` (parent skill)
- `tiktok-competitor-deep-analysis/SKILL.md` (this skill)
- `default-project-hub-pattern` (Quality bar 13/06)
- `video-download-yt-dlp` (yt-dlp format selector)
- `youtube-transcript-extractor` (Whisper fallback)
