# Google Drive Download Pattern (no gdown required)

**Source:** 2026-06-30 session — downloaded 543 MB MP4 from `https://drive.google.com/file/d/1hlmtEy1syTSI67IbHWRn2dQLb6tzIqpU/view?usp=drivesdk`

## Why not `gdown`

- `gdown` not installed in whisper-env (no pip there)
- System Python has PEP 668 protection — can't `pip install` either
- `gdown` often fails on files >100MB anyway due to Google's virus scan warning UI

## Why curl + drive.usercontent.google.com works

The Google Drive "Virus scan warning" page is an HTML form. It contains:
- A `<input name="confirm">` value (cookie-style token, NOT what we want)
- A `<input name="uuid">` value (36-char UUID like `a1438a0f-b564-4b0f-86cd-da35252b60e9`)

The UUID is the actual download authorization. Using `drive.usercontent.google.com` with that UUID bypasses the warning UI entirely.

## The 4-step recipe

```bash
# 1. Get confirm page (HTML form)
FILE_ID="1hlmtEy1syTSI67IbHWRn2dQLb6tzIqpU"
curl -sLc cookies.txt "https://drive.google.com/uc?export=download&id=${FILE_ID}" -o confirm.html

# 2. Extract UUID from <input name="uuid" value="...">
UUID=$(grep -oE 'value="[a-f0-9-]{36}"' confirm.html | head -1 | sed 's/value="//;s/"//')
echo "UUID: $UUID"

# 3. Download via drive.usercontent.google.com
curl -L "https://drive.usercontent.google.com/download?id=${FILE_ID}&export=download&confirm=t&uuid=${UUID}" \
  -o clip.mp4 -s -w "HTTP: %{http_code} | Size: %{size_download} bytes\n"

# 4. VERIFY it's actually a video (not HTML error page)
file clip.mp4
# MUST say "ISO Media, MP4 Base Media" or similar
# If says "HTML document" → step 3 failed silently, retry with fresh cookies
```

## Failure modes & fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `clip.mp4` is 2446 bytes HTML | Cookie confirm token (not UUID) was used | Use UUID from `<input name="uuid">`, not the cookie `confirm` param |
| `clip.mp4` is HTML with "Quota exceeded" | File too large for unauthenticated download | User must share with link-sharing enabled, or use `--confirm=t` flag |
| curl returns 403 | IP rate limited | Wait 60s, retry; or use VPN |
| `grep -oE` finds no UUID | Drive UI updated (rare) | Check confirm.html manually — look for any `<input name="..." value="UUID-format-string">` |

## Variants

### For shared folder links
```bash
FOLDER_ID="abc123"
curl -L "https://drive.usercontent.google.com/download?id=${FOLDER_ID}&export=download&confirm=t" \
  -o folder.zip
```

### For files under 100MB (no warning UI)
```bash
# Skip the confirm.html step entirely
curl -L "https://drive.usercontent.google.com/download?id=${FILE_ID}&export=download&confirm=t" \
  -o clip.mp4
```

## When to fall back to `yt-dlp`

If Google Drive keeps failing (auth required, rate limited), ask user to:
1. Upload to YouTube (unlisted) → use `video-download-yt-dlp` skill
2. Upload to Dropbox/OneDrive with direct download link → use curl directly
3. Re-share with "Anyone with the link can view" → retry Drive recipe

NEVER substitute an alternative source without telling user first — they may have shared Drive intentionally to avoid uploading elsewhere.