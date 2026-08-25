# PITFALL #86 — Concat demuxer strips audio filters (audio-visual desync)

**Detected:** 23/07/2026 by anh Tuấn Anh

## Symptom

Using `ffmpeg -f concat -safe 0 -i list.txt` (Concat demuxer mode) produces
clean cuts at boundaries BUT: audio is hard-cut (no fade in/out), causing
listener to perceive "pop" + "image changes before speech ends" (audio-visual
desync). User feedback verbatim:

> *"Audio cắt chỉnh fade out nhỏ hơn! Hinh đang đi trước tiếng, cảm giác
> âm thanh giọng đọc và hình ảnh không khớp nhau!"*

## Root cause

Concat demuxer = `stream copy` mode. Audio samples concatenated byte-for-byte
without re-encoding. No filter chain applies. Cannot attach `afade` filter.

## Fix (v0.01.1)

Replace `build_pre_speed.sh` Concat demuxer with `filter_complex`:

```bash
# Per segment: trim + afade 30ms in + out
[i:v]trim=start=S:end=E,setpts=PTS-STARTPTS[vN]
[i:a]atrim=start=S:end=E,asetpts=PTS-STARTPTS,
     afade=t=in:st=0:d=0.03,afade=t=out:st={E-S-0.03}:d=0.03[aN]

# Concatenate
[v0][a0][v1][a1]...[vN][aN]concat=n=N:v=1:a=1[outv][outa]
```

`d=0.03` = 30ms fade. Browser-use/video-use Hard Rule #3.

## Related PITFALLs

- **PITFALL #73** (v3.78 era): Concat demuxer `select='not(mod(n,3))'` caused
  1.68MB corrupt files. Fix was Concat demuxer (then) — but that introduced
  THIS desync PITFALL #86.
- Browser-use Hard Rule #3 applies to ALL concat cuts, not just DJI macros.

## Verified

Clip 0029 V1_67_FINAL_BODY_MIST — anh confirmed audio smooth after fix.
Clip 0034 V1_76_FINAL_VACUUM — same.
