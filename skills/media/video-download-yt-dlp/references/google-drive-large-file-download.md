# Google Drive Large File Download (curl + confirm uuid)

## Context

Khi user share link Google Drive dạng `https://drive.google.com/file/d/<FILE_ID>/view?usp=drivesdk` cho file > 100MB (ví dụ: 655MB video 7 phút camera phone HEVC, hoặc 711MB video tiktok 1 phút), `yt-dlp` có thể fail vì:

1. Drive cần **virus scan confirmation** cho file > 100MB
2. yt-dlp không handle tốt confirm token + redirect pattern
3. File 1GB+ cần download với progress tracking

→ **Dùng `curl` với Drive's usercontent endpoint** thay thế.

## Workflow verified (2026-07-02, DRIVE clip phone-stand 711MB)

### Step 1: Extract FILE_ID từ URL

```bash
URL="https://drive.google.com/file/d/1B9g8VX5s1HVpndOZ_KRFlVOeQihXCDhv/view?usp=drivesdk"
FILE_ID=$(echo "$URL" | sed -E 's|.*/file/d/([^/]+)/.*|\1|')
echo "FILE_ID: $FILE_ID"
```

### Step 2: Get confirm page → extract uuid

```bash
curl -L "https://drive.usercontent.google.com/download?id=${FILE_ID}&export=download&confirm=t" \
  -o /tmp/confirm_page.html

# Extract uuid từ HTML
UUID=$(grep -oE 'uuid" value="[^"]+"' /tmp/confirm_page.html | sed 's/uuid" value="//;s/"//')
echo "UUID: $UUID"

# Verify file size + name từ HTML
grep -oE 'uc-name-size.*\(([0-9]+M)\)' /tmp/confirm_page.html
```

### Step 3: Download với confirm uuid

```bash
FINAL_URL="https://drive.usercontent.google.com/download?id=${FILE_ID}&export=download&confirm=t&uuid=${UUID}"

curl -L "$FINAL_URL" \
  -o "/Volumes/Storage-1/Pocket3/Footages/DRIVE_${FILE_ID}.mp4"
```

### Step 4: Verify

```bash
ls -la /Volumes/Storage-1/Pocket3/Footages/DRIVE_${FILE_ID}.mp4
file /Volumes/Storage-1/Pocket3/Footages/DRIVE_${FILE_ID}.mp4
# → ISO Media, MP4 Base Media v1 [ISO 14496-12:2003] (REAL video, không phải HTML)

ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 \
  /Volumes/Storage-1/Pocket3/Footages/DRIVE_${FILE_ID}.mp4
```

## Pitfall: UTF-8 decode error in subprocess (Python)

**Triệu chứng:** Khi dùng `subprocess.run(['curl', ...], capture_output=True, text=True)` trong Python để capture HTML, có thể fail với:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd4 in position 39: invalid continuation byte
```

**Fix:** Dùng `terminal()` tool thay vì `execute_code()` cho việc curl download lần đầu (Step 2). Hoặc skip text=True:
```python
r = subprocess.run(['curl', '-L', url], capture_output=True, timeout=30)
# Không dùng text=True
html = r.stdout.decode('utf-8', errors='ignore')  # decode safe
```

## Pitfall: Download cap at 100MB mà không có uuid

**Triệu chứng:** `curl -L "https://drive.google.com/uc?export=download&id=${FILE_ID}"` → trả về HTML page thay vì file binary (file "Google Drive - Virus scan warning"). Nếu chỉ save 2446 bytes → URL chưa có confirm.

**Fix:** Luôn follow 2-step:
1. Step 1: lấy confirm page
2. Step 2: extract uuid từ form
3. Step 3: download với uuid

## Pitfall: `/tmp` disk 100% full

**Triệu chứng:** Sau nhiều lần transcribe/render, `/tmp` đầy 228GB/228GB → `OSError: I/O error: No space left on device (os error 28)`.

**Fix:**
```bash
# Clean up segments rác trước
rm -f /tmp/v*.mp4 /tmp/lemony_*.wav /tmp/drive_*.wav

# Move working file sang /Volumes/Storage-1/ thay vì /tmp
mkdir -p /Volumes/Storage-1/Hermes/temp_render
```

## Khi nào dùng approach này thay vì yt-dlp

| File size | Approach |
|-----------|----------|
| < 100MB | `yt-dlp --output "raw.%(ext)s" "https://drive.google.com/uc?id=${FILE_ID}"` (Pitfall #11) |
| **100MB - 2GB** | **curl + confirm uuid (workflow này)** |
| > 2GB | Cân nhắc upload lên cloud khác (S3, Dropbox) — Drive download chậm với file lớn |

## Cross-reference

- `media/video-download-yt-dlp/SKILL.md` — Pitfall #11 (Google Drive via yt-dlp, cho file < 100MB)
- `media/tiktok-video-editor/SKILL.md` — Workflow edit clip Drive sau khi tải
- `media/telegram-video-analysis/SKILL.md` — Phân tích video Drive nhận từ Telegram

## Verified command (verbatim từ session 2026-07-02)

```bash
# Setup
URL="https://drive.google.com/file/d/1B9g8VX5s1HVpndOZ_KRFlVOeQihXCDhv/view?usp=drivesdk"
FILE_ID="1B9g8VX5s1HVpndOZ_KRFlVOeQihXCDhv"
TARGET="/Volumes/Storage-1/Pocket3/Footages/DRIVE_1B9g8VX5.mp4"

# Step 1: Get confirm page
curl -L "https://drive.usercontent.google.com/download?id=${FILE_ID}&export=download&confirm=t" -o /tmp/confirm.html

# Step 2: Extract uuid
UUID=$(grep -oE 'uuid" value="[^"]+"' /tmp/confirm.html | head -1 | sed 's/uuid" value="//;s/"//')

# Step 3: Download với uuid
curl -L "https://drive.usercontent.google.com/download?id=${FILE_ID}&export=download&confirm=t&uuid=${UUID}" \
  -o "${TARGET}"

# Step 4: Verify
ls -la "${TARGET}"  # 746MB
file "${TARGET}"    # ISO Media, MP4 Base Media v1
ffprobe -v error -show_entries format=duration -of csv=p=0 "${TARGET}"  # 149.58s
```

## Anti-patterns

- ❌ `curl "https://drive.google.com/uc?id=${FILE_ID}"` cho file > 100MB → HTML page thay vì binary
- ❌ `yt-dlp` không có progress tracking tốt cho file 700MB+ → curl với `-#` flag có progress bar
- ❌ Save về `/tmp` khi disk full → OSError → save về `/Volumes/Storage-1/`
- ❌ Bỏ qua Step 1 (confirm page) → Step 3 fail vì thiếu uuid
