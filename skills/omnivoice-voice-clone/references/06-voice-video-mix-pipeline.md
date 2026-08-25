---
title: Voice + Video Mix Pipeline (iPhone-friendly)
created: 2026-07-14
type: recipe
tags: [recipe, voice-clone, video-mix, ffmpeg, iPhone]
---

# Voice + Video Mix Pipeline

Ghép voice OmniVoice (24kHz mono WAV) vào video iPhone-friendly (H.264 + AAC + 44100Hz, MP4) với fade in audio gốc sau khi voice kết thúc.

## Pipeline 5 bước (đã verify 14/07 với PaxRmpR_S-Y + vsQ5ORUBimY)

### Bước 1: Extract audio gốc từ video

```bash
ffmpeg -y -i "$VIDEO" -vn -c:a copy /tmp/video_audio.m4a
```

### Bước 2: Mix voice + audio gốc

```bash
ffmpeg -y \
  -i voice.wav \
  -i /tmp/video_audio.m4a \
  -filter_complex \
    "[0:a]aresample=44100,afade=t=out:st=VO_DUR-0.03:d=0.03,apad=whole_dur=VIDEO_DUR[v]; \
     [1:a]aresample=44100,volume=enable='between(t,0,VO_DUR)':volume=0,afade=t=in:st=VO_DUR:d=FADE_DUR[a]; \
     [v][a]amix=inputs=2:duration=longest:dropout_transition=0[mix]; \
     [mix]loudnorm=I=-16:TP=-1.5:LRA=11[out]" \
  -map "[out]" \
  -ac 2 -ar 44100 \
  -c:a aac -b:a 128k \
  /tmp/audio_mixed.m4a
```

⚠️ **BẮT BUỘC** `-ac 2 -ar 44100` sau loudnorm — loudnorm đổi thành 96000Hz+mono.

### Bước 3: Combine audio mixed với video

```bash
ffmpeg -y \
  -i "$VIDEO" \
  -i /tmp/audio_mixed.m4a \
  -map 0:v -map 1:a \
  -c:v copy \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "${VIDEO%.mp4}_with_voice.mp4"
```

## Verify spec

```bash
ffprobe -v error \
  -show_entries stream=codec_name,codec_type,sample_rate,channels \
  -show_entries format=duration,size \
  -of default=nw=1 \
  "${VIDEO%.mp4}_with_voice.mp4"
```

| Field | Expected |
|---|---|
| Video codec | h264 |
| Audio codec | aac |
| Audio sample_rate | **44100** (KHÔNG 96000) |
| Audio channels | **2 (stereo)** (KHÔNG mono) |
| Duration | VIDEO_DUR |

## Verify mix logic (volume sampling)

```bash
for t in 0.5 1.5 3.0 3.5 4.5 6.0; do
  ffmpeg -ss $t -i output.mp4 -t 1 -vn -af volumedetect -f null - 2>&1 | grep max_volume
done
```

| Time | Expected |
|---|---|
| 0 → VO_DUR | Voice peak -2 to -10 dB |
| VO_DUR | Voice fade out (peak drop) |
| VO_DUR → VO_DUR+2s | Audio gốc fade in (peak tăng dần) |
| VO_DUR+2s+ | Audio gốc full volume |

## Pitfalls

| # | Pitfall | Fix |
|---|---|---|
| M1 | `amix` thuần divide by 2 → audio gốc giảm 6dB | `amix=...:dropout_transition=0` + loudnorm |
| M2 | `adelay` logic sai → duration nhân đôi | KHÔNG dùng adelay, dùng `apad=whole_dur=VIDEO_DUR` + `volume=enable='between...':volume=0` |
| M3 | `loudnorm` KHÔNG reset sample_rate → 96000Hz | Thêm `-ac 2 -ar 44100` ở output mapping |
| M4 | Ghép voice vào SAI VIDEO NGUỒN — user flag "M ghép lộn video rồi video mới kêu tải đâu?" | **Verify VIDEO_ID match user request trước khi ghép**. KHÔNG đoán từ folder mtime |
| M5 | Voice mono (24kHz mono từ OmniVoice) → output stereo mất channel | Force `-ac 2` ở audio mixed output |

## Workflow trước khi ghép

1. **Xác nhận VIDEO_ID** từ user message (KHÔNG đoán từ folder mtime)
2. **Check file voice đã generate chưa** (nếu chưa → Phase 4 skill omnivoice)
3. **Apply pipeline 5 bước**
4. **Verify** bằng ffprobe + volume sampling
5. **Send `MEDIA:` qua Telegram** + summary table

## Real case (14/07)

- Voice: "momota đoạn này thì đại đế phải gọi bằng mồm" với `[surprise-oh]` + `[laughter]`
- Voice duration: 3.6s @ 24kHz mono
- Video ban đầu ghép sai → user flag → re-ghép đúng clip vsQ5ORUBimY 21.32s
- Output final: 21.42s, H.264 + AAC + 44100Hz + stereo, 3.93 MB