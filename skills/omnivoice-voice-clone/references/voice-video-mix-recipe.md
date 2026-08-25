---
title: Voice + Video Mix Recipe
type: reference
skill: omnivoice-voice-clone
created: 2026-07-14
---

# Mix Generated Voice with Original Video Audio (TikTok Shorts Workflow)

When anh wants voice Tuấn Anh ở đầu video (HOOK), rồi fade in audio gốc của video ngay sau voice kết thúc.

## The CORRECT pattern (verified 2026-07-14, clip PaxRmpR_S-Y 46.88s)

```bash
VIDEO="/Volumes/Storage-1/Tiktok-Tuan-Anh/<id>_iphone.mp4"
VOICE="<output_wav_from_generate_voice.py>"
AUDIO_TMP="/tmp/<id>_audio.m4a"
OUT="/Volumes/Storage-1/Tiktok-Tuan-Anh/<id>_with_voice.mp4"
VO_DUR=3.6    # measured from voice file
FADE_DUR=2.0  # fade-in duration for original audio
AUDIO_DUR=46.88  # measured from video

# 1. Extract audio gốc từ video
ffmpeg -y -i "$VIDEO" -vn -c:a copy "$AUDIO_TMP"

# 2. Mix voice + audio gốc (3 filter stages)
ffmpeg -y \
  -i "$VOICE" \
  -i "$AUDIO_TMP" \
  -filter_complex \
    "[0:a]aresample=44100,afade=t=out:st=$((VO_DUR - 3)):d=0.03,apad=whole_dur=$AUDIO_DUR[v]; \
     [1:a]aresample=44100,volume=enable='between(t,0,$VO_DUR)':volume=0,afade=t=in:st=$VO_DUR:d=$FADE_DUR[a]; \
     [v][a]amix=inputs=2:duration=longest:dropout_transition=0[mix]; \
     [mix]loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary[out]" \
  -map "[out]" \
  -c:a aac -b:a 128k \
  /tmp/audio_mixed.m4a

# 3. RE-ENCODE audio to stereo 44100Hz BEFORE combining with video
ffmpeg -y -i /tmp/audio_mixed.m4a -ac 2 -ar 44100 -c:a aac -b:a 128k /tmp/audio_stereo.m4a

# 4. Combine with video (copy video stream)
ffmpeg -y -i "$VIDEO" -i /tmp/audio_stereo.m4a \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 128k \
  -movflags +faststart \
  "$OUT"
```

## The 3 NON-OBVIOUS gotchas (mỗi cái fail 1 lần trong session 14/07)

### Gotcha 1: `amix` ALWAYS divides by number of inputs → audio giảm 6 dB

`amix=inputs=2` produces `output = (track_a + track_b) / 2`. Khi voice đã silent (sau 3.6s) và audio gốc full → output = audio_gốc / 2 = giảm ~6 dB.

**Fix:** `loudnorm=I=-16:TP=-1.5` ở cuối chain sẽ boost lên chuẩn TikTok (-16 LUFS, peak -1.5 dB). Audio gốc từ -34 dB mean sẽ lên -27 dB mean (vẫn nghe rõ, không clip).

**Anti-pattern:** KHÔNG dùng `amix` rồi skip loudnorm → ship audio bị giảm 6 dB.

### Gotcha 2: `loudnorm` filter tự đổi sample_rate thành 96000 Hz

`loudnorm` filter (libebur128) internally chạy ở 96kHz. Nếu không re-encode riêng → file cuối có `sample_rate=96000` → iPhone play OK nhưng TikTok spec strict 44100.

**Fix:** Bước 3 — re-encode audio sang 44100 + stereo SAU loudnorm.

```bash
ffmpeg -y -i /tmp/audio_mixed.m4a -ac 2 -ar 44100 -c:a aac -b:a 128k /tmp/audio_stereo.m4a
```

### Gotcha 3: Mono voice → kết quả mono audio stream → iPhone play 1 bên tai

Voice OmniVoice output 24kHz mono. Sau mix → audio stream mono. iPhone play stereo từ cả 2 bên tai tốt hơn.

**Fix:** Bước 3 force `-ac 2` (stereo).

## Filter chain breakdown (từng filter 1 lý do)

```
[0:a]aresample=44100,afade=t=out:st=2.97:d=0.03,apad=whole_dur=46.88[v]
                ^^^^^^^^^^^^                 ^^^^^^^^      ^^^^^^^^^^^^^^^
                |                            |             |
                resample voice từ 24kHz → 44100 (match audio gốc)
                                            30ms fade out ở cuối voice (Pitfall #6 omnivoice)
                                                              pad silence tới cuối audio (46.88s)
                                                               → khi mix, voice track dài đúng bằng audio

[1:a]aresample=44100,volume=enable='between(t,0,3.6)':volume=0,afade=t=in:st=3.6:d=2.0[a]
                ^^^^^^^^^^^^                          ^^^^^^                 ^^^^^^^^^^^
                |                                     |                      |
                resample audio gốc → 44100           MUTE 0-3.6s (voice đang chạy)
                                                                    fade in 3.6-5.6s (voice vừa kết thúc)
                                                                    → audio nghe rõ từ giây 5.6

[v][a]amix=inputs=2:duration=longest:dropout_transition=0[mix]
            ^^^^^^                    ^^^^^^^^^^^^^^^^^^^^^^^
            |                         |
            mix 2 tracks              dropout_transition=0: chuyển gấp không smooth (đúng ý vì voice kết thúc thẳng)
            duration=longest: output dài bằng track dài nhất (audio gốc)

[mix]loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary[out]
       ^^^^^^^^                              ^^^^^^^
       |                                     |
       normalize chuẩn TikTok                 summary → in log để anh thấy LUFS + peak
```

## Volume verification recipe (kiểm tra mix đúng)

```bash
for t in 0.5 1.5 3.0 3.5 4.5 6.0 10.0 25.0 45.0; do
  ffmpeg -y -ss $t -i "$OUT" -t 1.0 -vn -f wav /tmp/check.wav
  ffmpeg -i /tmp/check.wav -af volumedetect -vn -f null - 2>&1 | grep -E "max_volume|mean_volume"
done
```

**Expected pattern (PaxRmpR_S-Y clip 46.88s, voice 3.6s):**
| t | max | mean | What's playing |
|---|---|---|---|
| 0.5s | -1.6 dB | -17 dB | Voice (loud) |
| 1.5s | -1.7 dB | -15 dB | Voice (loud) |
| 3.0s | -2.9 dB | -19 dB | Voice cuối |
| 3.5s | -19 dB | -37 dB | Voice vừa kết thúc |
| 4.5s | -11.6 dB | -30 dB | Audio gốc fading in |
| 6.0s+ | -2 to -10 dB | -26 to -36 dB | Audio gốc full |

## When NOT to use this recipe

- Video không có audio gốc (silent video) → skip bước extract + audio track
- Voice muốn ở GIỮA video (không phải đầu) → dùng `adelay` để position voice
- Voice muốn OVERLAY audio gốc (không phải thay thế) → skip `volume=0` cho audio track, dùng weights trong amix
- Anh muốn 2+ voice segments ghép → dùng `concat_segments.py` của skill omnivoice TRƯỚC, rồi apply recipe này

## Related

- `references/04-recipes.md` — Recipe 11 emotion tags (đã dùng `[surprise-oh]` + `[laughter]`)
- `references/00-pitfalls.md` — Pitfall #6 về 30ms fade out (áp dụng cho voice clip này)
- Skill SKILL.md Phase 4 — emotion tags MANDATORY