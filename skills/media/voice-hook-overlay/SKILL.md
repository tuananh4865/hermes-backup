---
name: voice-hook-overlay
title: Voice HOOK overlay onto video with audio fade-in
description: Overlay a synthetic or cloned voice HOOK at start of video, fade in original audio after voice ends.
version: 0.1.0
author: Hermes
platforms: [macos]
metadata:
  hermes:
    tags: [Voice, Video, Audio, ffmpeg, TikTok, Mix, HOOK, Fade]
---

# Voice HOOK Overlay onto Video with Audio Fade-In

Overlay a short voice clip (3-6s) at the START of a video as the HOOK, with the original audio MUTED while voice plays and FADED IN after voice ends. Standard pattern for TikTok Shorts where anh wants to add authentic voice commentary before the video's natural audio kicks in.

## When to Use

- Anh sends a video file (YouTube Shorts, Facebook Reel, native MP4) and asks to add voice HOOK
- "tạo voice HOOK cho clip X" / "ghép voice vào đầu video" / "fade in audio sau khi voice đọc xong"
- Voice source: OmniVoice clone (giọng Tuấn Anh) hoặc bất kỳ WAV 24kHz+ mono
- Source video có audio gốc muốn giữ nguyên sau voice HOOK
- Final output: TikTok spec H.264/AAC/44100Hz/stereo

Trigger phrases: "tạo voice HOOK", "ghép voice vào clip", "voice ở đầu video", "fade in audio gốc", "voice TikTok HOOK", "voice kiểu cười cười vào đầu clip".

## Prerequisites

- `ffmpeg` + `ffprobe` on PATH
- Source video file accessible (local path, đã download từ YouTube/Facebook trước)
- Voice WAV file (24kHz mono từ OmniVoice, hoặc bất kỳ format nào ffmpeg hiểu)
- Read+write on output folder (typically `/Volumes/Storage-1/Tiktok-Tuan-Anh/`)

## How to Run

Provide 3 inputs:
1. **VIDEO** path — local MP4 file
2. **VOICE** path — WAV file của voice HOOK (typically 3-6s)
3. **OUT** path — destination MP4 (suggest `<video_id>_with_voice.mp4`)

Skill returns MEDIA: line ready for Telegram.

## Quick Reference

- **Voice duration:** `ffprobe -show_entries format=duration` của VOICE file → `VO_DUR`
- **Video duration:** `ffprobe -show_entries format=duration` của VIDEO → `AUDIO_DUR`
- **Fade in duration:** Default 2.0s (anh có thể yêu cầu khác)
- **Filter pattern:** 4 filter stages cuối cùng, không skip bước nào
- **Verify spec final:** H.264 + AAC + **44100Hz + STEREO** + đúng duration VIDEO

## Procedure

### Step 1: Measure durations

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VOICE"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VIDEO"
```

Lưu vào biến `VO_DUR` (voice) và `AUDIO_DUR` (video).

### Step 2: Extract audio gốc từ video

```bash
AUDIO_TMP="/tmp/<video_id>_audio.m4a"
ffmpeg -y -i "$VIDEO" -vn -c:a copy "$AUDIO_TMP"
```

3. **Mix voice + audio gốc**

```bash
VO_DUR=3.6
FADE_DUR=2.0
AUDIO_DUR=46.88

ffmpeg -y \
  -i "$VOICE" \
  -i "$AUDIO_TMP" \
  -filter_complex \
    "[0:a]aresample=44100,afade=t=out:st=$((VO_DUR - 3)):d=0.03,apad=whole_dur=$AUDIO_DUR,volume=1.4[v]; \
     [1:a]aresample=44100,volume='if(lt(t,0),1,if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,$VO_DUR),0,if(lt(t,$(($VO_DUR + $FADE_DUR))),(t-$VO_DUR)/$FADE_DUR,1))))':eval=frame[a]; \
     [v][a]amix=inputs=2:duration=longest:dropout_transition=0[mix]; \
     [mix]aresample=44100,pan=stereo|c0=c0|c1=c0[out]" \
  -map "[out]" \
  -c:a aac -b:a 128k \
  /tmp/audio_mixed.m4a
```

**Filter breakdown:**
- `[0:a]aresample=44100` — Voice 24kHz → 44100 Hz (match audio gốc)
- `afade=t=out:st=$((VO_DUR - 3)):d=0.03` — 30ms fade out ở cuối voice (Pitfall #6 omnivoice)
- `apad=whole_dur=$AUDIO_DUR` — pad silence tới cuối audio gốc (để mix đúng độ dài)
- `volume=1.4` — boost voice 1.4× để compensate amix divide (~6 dB loss) — see P1
- `[1:a]volume='if(lt(t,X),1,...)':eval=frame` — **piecewise volume expression** để mute audio gốc trong voice range (0→VO_DUR) mà VẪN restore ở ngoài range. **KHÔNG dùng** `volume=enable='between(t,...)':volume=0` — chỉ apply rule trong range, mute cả ngoài range (xem P8)
- `amix=inputs=2:duration=longest:dropout_transition=0` — mix 2 tracks
- `aresample=44100,pan=stereo|c0=c0|c1=c0` — convert cuối sang stereo 44100 để bỏ qua bước re-encode riêng (P2+P3)

**Khác biệt với v0.1.0:** Filter chain này KHÔNG dùng loudnorm (vì loudnorm làm peak > -1 dB và đổi sample_rate về 96000). Em replace bằng `volume=1.4` cho voice + `pan=stereo` ở cuối. Kết quả giống loudnorm nhưng không có downsides.

### Step 4: Combine với video

```bash
ffmpeg -y \
  -i "$VIDEO" \
  -i /tmp/audio_mixed.m4a \
  -map 0:v \
  -map 1:a \
  -c:v copy \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "$OUT"
```

`-c:v copy` để giữ video nguyên (không re-encode). Audio đã ở stereo 44100 Hz (built vào step 3 bằng `pan=stereo` ở cuối filter chain) nên không cần re-encode riêng như v0.1.0.

### Step 5: Verify spec cuối

```bash
ffprobe -v error \
  -show_entries stream=codec_name,codec_type,width,height,sample_rate,channels \
  -show_entries format=duration,size,format_name \
  -of default=nw=1 \
  "$OUT"
```

**PASS criteria:**
- `codec_name=h264` (video)
- `codec_name=aac` (audio)
- `sample_rate=44100` (KHÔNG 96000)
- `channels=2` (KHÔNG 1)
- `format_name` chứa `mp4`

### Step 6: Verify volume mix đúng

```bash
for t in 0.5 1.5 3.0 3.5 4.5 6.0 10.0 25.0 45.0; do
  ffmpeg -y -ss $t -i "$OUT" -t 1.0 -vn -f wav /tmp/check.wav
  ffmpeg -i /tmp/check.wav -af volumedetect -vn -f null - 2>&1 | grep -E "max_volume|mean_volume"
done
```

**Pattern đúng (verified PaxRmpR_S-Y clip 46.88s, voice 3.6s):**

| t | max dB | mean dB | What's playing |
|---|---|---|---|
| 0.5s | ~-3 to -6 | ~-17 to -21 | Voice (peak rises với emotion + volume 1.4x) |
| 1.5s | ~-3 to -6 | ~-15 to -20 | Voice |
| 3.0s | ~-5 to -6 | ~-19 to -21 | Voice cuối |
| 3.5s | ~-19 to -23 | ~-37 to -41 | Voice vừa kết thúc, audio gốc đang hồi |
| 4.5s | ~-11.6 | ~-30 | Audio gốc fading in (peak 50% of full) |
| 6.0s+ | -2 to -10 | -26 to -36 | Audio gốc full |

**Note v0.2.0:** Piecewise volume (no loudnorm) cho values KHÁC v0.1.0. Voice nghe nhỏ hơn một chút (do không có -16 LUFS normalize) nhưng audio gốc sau voice nghe RÕ HƠN (mean -27 dB vs v0.1.0 -35 dB). Acceptable trade-off — tránh loudnorm downsides (peak > -1 dB, sample_rate → 96000).

## Pitfalls

### P1. `amix` ALWAYS divides by number of inputs → audio gốc giảm 6 dB

`amix=inputs=2` produces `output = (track_a + track_b) / 2`. Khi voice đã silent (sau VO_DUR) và audio gốc full → output = audio_gốc / 2 = giảm ~6 dB.

**Fix:** `loudnorm=I=-16:TP=-1.5` ở cuối mix chain sẽ boost lên chuẩn TikTok (-16 LUFS, peak -1.5 dB). Audio gốc từ -34 dB mean sẽ lên -27 dB mean (vẫn nghe rõ, không clip).

**Anti-pattern:** Skip loudnorm → ship audio bị giảm 6 dB → user báo "nghe nhỏ quá".

### P2. `loudnorm` filter tự đổi sample_rate thành 96000 Hz

`loudnorm` filter (libebur128) internally chạy ở 96kHz. Nếu không re-encode riêng → file cuối có `sample_rate=96000` → iPhone play OK nhưng TikTok spec strict 44100.

**Fix:** Bước 4 — re-encode audio sang 44100 SAU loudnorm.

```bash
ffmpeg -y -i /tmp/audio_mixed.m4a -ac 2 -ar 44100 -c:a aac -b:a 128k /tmp/audio_stereo.m4a
```

### P3. Voice mono → mixed audio mono → iPhone play 1 bên tai

Voice OmniVoice output 24kHz mono. Sau mix → audio stream mono. iPhone play stereo từ cả 2 bên tai tốt hơn.

**Fix:** Bước 4 force `-ac 2` (stereo).

### P4. KHÔNG bỏ bước apad voice

Nếu voice ngắn hơn audio gốc (gần như luôn luôn), cần `apad=whole_dur=$AUDIO_DUR` để voice track dài đúng bằng audio gốc. Nếu skip, amix sẽ không mix phần audio gốc sau voice kết thúc.

### P5. KHÔNG bỏ `-movflags +faststart`

Final output cần `+faststart` để iPhone/Telegram stream play ngay không delay.

### P6. KHÔNG re-encode video (giữ `-c:v copy`)

Video đã H.264 + AAC chuẩn rồi, không cần re-encode. Re-encode video mất ~30s extra + có thể giảm quality. Step 5 dùng `-c:v copy`.

### P7. KHÔNG dùng acrossfade cho 2 track không overlap

`acrossfade` designed cho 2 tracks overlap thời gian. Ở đây voice + audio gốc KHÔNG overlap (voice 0-VO_DUR, audio VO_DUR-AUDIO_DUR), KHÔNG cần acrossfade. Dùng `amix` (mix thẳng) + `apad` (pad voice) là đúng.

## When NOT to Use

- Voice muốn ở GIỮA video (không phải đầu) → dùng `adelay` để position voice
- Voice muốn OVERLAY audio gốc (không phải thay thế) → skip `volume=0` cho audio track, dùng `amix` weights để cả 2 cùng nghe
- Video không có audio gốc → skip bước 2 (extract) + audio track input 1
- Voice dài ≥ 50% video → fade in thời gian không đủ, cần logic khác

## Verification

Pass = tất cả 4:
1. `ffprobe` shows `h264` + `aac` + `44100 Hz` + `channels=2` + `format_name` chứa `mp4`
2. Volume sampling đúng pattern (voice loud 0-VO_DUR, audio fade in sau)
3. File play được trên iPhone Photos app không lỗi
4. Telegram nhận file và play ngay (no delay)

## Related Skills

- `omnivoice-voice-clone` — Generate voice clone trước khi mix
- `youtube-shorts-to-iphone-download` — Download source video (TikTok/FB Reel) trước khi overlay voice

## Note (2026-07-25)

This skill (v0.1.0/v0.2.0) overlaps significantly with `voice-overlay-clip-workflow` (Mode A). Both cover: voice prepend → piecewise volume expression → amix voice + audio. The main difference is `voice-overlay-clip-workflow` adds Mode B (translate+replace segments). Suggested curator action: consolidate `voice-hook-overlay` into `voice-overlay-clip-workflow` Mode A; keep VOICE pattern (HOOK + fade in) as a sub-variant.

## References

- `references/voice-video-mix-recipe.md` (under omnivoice-voice-clone) — Same recipe, dạng reference document