# User Corrections — Omnivoice Voice Clone (24/07 session)

## L1: `volume=enable='between':value` does NOT restore outside range

**Push-back:** User task "Xoá logo SB + ghép voice" required audio mix: voice 0-3.8s, audio gốc mute trong khoảng đó, fade in sau. Em tried:
```python
[2:a]aresample=44100,volume=enable='between(t,0.3,3.8)':volume=0
# Expected: volume 1.0 outside range, 0 inside
# Actual: volume 0 EVERYWHERE — both inside AND outside range
```

**Symptom:** Audio gốc play trong khoảng 0-0.3s và 5.8s+ đúng, nhưng silent ở 4.5s+ (ngoài range). Volume 0 cố định cả clip.

**Root cause:** ffmpeg `volume` filter với `enable='between(t,a,b)':volume=0` → chỉ apply volume=0 KHI trong range, nhưng KHI NGOÀI range vẫn giữ volume=0 (không restore). Filter `volume` KHÔNG preserve giá trị ngoài `enable` range.

**Workaround (correct):** Dùng `volume=expression` với piecewise function. Expression evaluate theo frame, giá trị ngoài `if/else` chain = last matched branch.

```python
# Voice: 3.8s. Audio gốc: fade out 0-0.3, mute 0.3-3.8, fade in 3.8-5.8, full 5.8+
volume='if(lt(t,0.0),1,if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,3.8),0,if(lt(t,5.8),(t-3.8)/2,1))))'
# Output:
# t<0.0:    1.0  (full)
# 0.0-0.3:  linear fadeout (1→0)
# 0.3-3.8:  0    (mute while voice)
# 3.8-5.8:  linear fadein (0→1)
# 5.8+:     1.0  (full)
```

**Ap dụng `:eval=frame`** để expression eval mỗi frame (default `eval=once` chỉ eval 1 lần = sai).

**Verified case 24/07:** clip `lGZQgDMMMac_iphone.mp4` 28.82s, voice 3.8s. Volume sampling before fix: t=4.5s+ = -91 dB (silent). After fix: t=4.5s+ = -4 to -8 dB (full audio gốc).

**Anti-pattern (NEVER use):**
```python
# ❌ KHÔNG dùng cách này — mute cố định toàn clip
volume=enable='between(t,0.3,3.8)':volume=0
# ❌ KHÔNG dùng 2 stage filter để "fix"
volume=enable='between(t,0,3.8)':volume=0,
volume=enable='between(t,3.8,999)':volume=1
# CŨNG SAI — ffmpeg filter chain KHÔNG đảm bảo order apply đúng
```

**Correct pattern:** Piecewise volume expression (verified work) — use for ALL cases of "mute X, restore Y, fade Z".

## L2: ffmpeg rejects `-r + -vsync 0` combo

**Verified 24/07:** Logo SB removal script dùng `-r 60` để fix duration sai, gặp:
> "One of -r/-fpsmax was specified together a non-CFR -vsync/-fps_mode. This is contradictory."

**Workaround:** Chỉ dùng `-vsync 0` (passthrough source FPS). Source video 60fps sẽ output 60fps PNG. KHÔNG cần `-r 60`.

```bash
# ❌ Reject
ffmpeg -i source.mp4 -vsync 0 -r 60 frame_%05d.png

# ✅ OK
ffmpeg -i source.mp4 -vsync 0 frame_%05d.png
```

For VFR source cần CFR output, dùng `-fps_mode cfr`:
```bash
ffmpeg -i source.mp4 -fps_mode cfr -r 60 frame_%05d.png
```

## L3: Detect source FPS with `avg_frame_rate`, not `r_frame_rate`

**Verified 24/07:** Clip `lGZQgDMMMac_iphone.mp4` 28.82s, 1724 frames @ 60fps. Em hardcode `FPS=30` → re-encode output 57.4s (2x duration). Hardcode `FPS=60` would halve.

**Correct:**
```python
fps_str = subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0",
     "-show_entries", "stream=avg_frame_rate",
     "-of", "default=nw=1:nk=1", VIDEO],
    capture_output=True, text=True
).stdout.strip()
FPS = float(fps_str.split('/')[0]) / float(fps_str.split('/')[1])
# Common: 30/1 = 30, 60/1 = 60
```

`avg_frame_rate` is averaged across all frames (reliable), `r_frame_rate` is the lowest framerate (can be wrong for VFR).

## L4: Voice clone `.pt` file for Tuấn Anh

**Path:** `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt` (9.9 KB)

**Usage:**
```python
PROMPT = "/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt"
cmd = [VENV, f"{SCRIPT_DIR}/generate_voice.py",
       "--prompt", PROMPT,
       "--text", "[question-ah] có mấy bạn xem video này làm được như bạn ở trong video nào?",
       "--output", "/Volumes/Storage-1/Hermes/scratch/voice-clone/clip.wav"]
```

**Verified 24/07:** Generated 3.8s WAV, peak -3.3 dB, mean -19.3 dB (PASS volumedetect). Voice là giọng Tuấn Anh, emotion `[question-ah]` cho cảm giác hỏi.
