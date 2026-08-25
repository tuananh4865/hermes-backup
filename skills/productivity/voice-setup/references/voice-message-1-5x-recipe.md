# Voice Message 1.5x Speed Recipe (21/07/2026)

> **Khi nào dùng:** User yêu cầu "tạo voice gửi vào đây" / "voice reply" / "gửi voice" + speed multiplier (1.3x, 1.5x, 2x).
> **Verified case:** 21/07/2026 — 5 bài học TikTok script + 3 version MA66 → voice 53.88s → ffmpeg atempo=1.5 → 35.91s MP3 → gửi Telegram.
> **Skill reference:** Công thức chính ở `~/.hermes/skills/productivity/voice-setup/SKILL.md` section "Send Voice Message to Telegram".

## Recipe 3 bước

### 1. Generate base audio bằng edge-tts CLI

```python
import subprocess
OUT = "/Volumes/Storage-1/Hermes/scratch/voice-messages/<filename>.mp3"
subprocess.run(
    ["edge-tts", "--voice", "vi-VN-HoaiMyNeural",
     "--text", SCRIPT, "--write-media", OUT],
    capture_output=True, timeout=120
)
```

**Lưu ý:**
- `text_to_speech` tool của Hermes FAIL silent với long Vietnamese text. LUÔN dùng CLI.
- Save vào `/Volumes/Storage-1/Hermes/scratch/voice-messages/` (Hermes-only folder rule).

### 2. Speed up bằng ffmpeg atempo

```python
SPEED = "1.5"
OUT_FAST = OUT.replace(".mp3", f"-{SPEED}x.mp3")
subprocess.run(
    ["ffmpeg", "-y", "-i", OUT,
     "-filter:a", f"atempo={SPEED}",
     "-vn", "-c:a", "libmp3lame", "-b:a", "192k",
     OUT_FAST],
    capture_output=True, timeout=60
)
```

**Verify duration:**
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 <OUT>      # original
ffprobe -v error -show_entries format=duration -of csv=p=0 <OUT_FAST> # sped up
# Ratio MUST = SPEED value (vd 1.5x)
```

### 3. Send to Telegram

```python
response_text = f"MEDIA:{OUT_FAST}"
```

Telegram sẽ tự detect `.mp3` là audio attachment. Voice bubble cần `.ogg` (chuyển đổi nếu user yêu cầu cụ thể).

## Constraints

| Hạn chế | Cách xử lý |
|---|---|
| `atempo` chỉ accept 0.5–2.0 | Speed > 2x: chain `atempo=2.0,atempo=1.5` |
| Long text fail với text_to_speech tool | LUÔN dùng edge-tts CLI direct |
| Speed setting trong config.yaml KHÔNG honored | Dùng ffmpeg post-process |
| Save vào `/tmp/` không survive | Dùng `/Volumes/Storage-1/Hermes/scratch/voice-messages/` |

## Anti-patterns

- ❌ Gọi `text_to_speech()` tool → silent fail `"No audio was received"` (Hermes tool bug)
- ❌ Skip duration verify sau atempo → có thể filter không apply mà không biết
- ❌ Set `speed: 1.5` trong `~/.hermes/config.yaml` edge section → KHÔNG có effect
- ❌ Save audio ra `/Users/tuananh4865/` thay vì `/Volumes/Storage-1/Hermes/scratch/voice-messages/` → mất sau backup

## Files created trong case 21/07

- `/Volumes/Storage-1/Hermes/scratch/voice-messages/tiktok-script-lesson-2026-07-21.mp3` (53.88s, 315KB)
- `/Volumes/Storage-1/Hermes/scratch/voice-messages/tiktok-script-lesson-2026-07-21-1.5x.mp3` (35.91s, 703KB) ← shipped to Telegram