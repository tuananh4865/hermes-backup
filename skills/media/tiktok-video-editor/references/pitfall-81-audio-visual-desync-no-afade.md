# PITFALL #81 — Audio-visual desync do Concat demuxer (no afade)

**Detected:** 23/07/2026 bởi anh Tuấn Anh (clip 0029 test v0.01)
**Fixed:** v0.01.1

## Symptom

Khi clip có nhiều KEEP segments (≥3) concat bằng Concat demuxer:
- Video frames cắt hard tại boundary
- Audio cũng cắt hard tại boundary cùng lúc
- → Người nghe cảm giác "speech ends too sharp, image changes instantly" 
- → Có cảm giác hình đi trước tiếng (anh flag verbatim 23/07)
- → Audio "pop" nhỏ tại boundary

## Repro

```bash
# Build pre-speed (v0.01)
ffmpeg -f concat -safe 0 -i concat_list.txt \
    -c:v libx264 -preset medium -crf 18 \
    -c:a aac -b:a 192k \
    final_pre_speed.mp4
```

Concat demuxer chỉ stream copy → audio KHÔNG qua filter chain → KHÔNG có fade.

## Fix v0.01.1

Replace Concat demuxer với `filter_complex` (Hard Rule #3 browser-use/video-use):

```bash
# Trim từng segment + afade 30ms in/out
i=0
FILTER=""
while IFS=' ' read -r start end; do
    seg_dur=$(python3 -c "print(round($end - $start, 3))")
    fade_out=$(python3 -c "print(round(max(0, $seg_dur - 0.03), 3))")
    FILTER="${FILTER}[0:v]trim=start=$start:end=$end,setpts=PTS-STARTPTS[v${i}];"
    FILTER="${FILTER}[0:a]atrim=start=$start:end=$end,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03,afade=t=out:st=$fade_out:d=0.03[a${i}];"
    i=$((i+1))
done

# Concat
FILTER="${FILTER}[v0][a0][v1][a1]...concat=n=${N}:v=1:a=1[outv][outa]"

ffmpeg -i source.mp4 -filter_complex "$FILTER" -map "[outv]" -map "[outa]" \
    -c:v libx264 -c:a aac final_pre_speed.mp4
```

**30ms** = đủ nghe mượt, không cảm giác lag hoặc pop.

## Bonus Compat Fix

macOS bash 3.2.57 (default `/bin/bash`) KHÔNG có `mapfile` builtin:

```bash
# macOS bash 3.2 fails:
mapfile -t arr <<< "$data"
# → bash: mapfile: command not found
```

**Fix:** Dùng `mktemp` write ra file tạm + `while read`:

```bash
RANGES_FILE=$(mktemp)
python3 <<PYEOF > "$RANGES_FILE"
... print ranges
PYEOF

while IFS=' ' read -r start end; do
    ...
done < "$RANGES_FILE"

rm -f "$RANGES_FILE"
```

## Verified

| Metric | v0.01 (broken) | v0.01.1 (fix) |
|---|---|---|
| Audio boundary | Hard cut | 30ms fade in/out |
| Listener cảm giác | "pop" nhỏ tại boundary | Mượt, không pop |
| Audio-visual sync | Hard sync (off) | Smooth transition |
| Test clip | 0029 Body Mist | 0029 Body Mist |
| Result | ❌ Anh flag | ✅ Re-render mượt |

## Related

- browser-use/video-use Hard Rule #3: 30ms audio fades ở mỗi segment boundary
- PITFALL #75: bash `set -e` + Python exit code (related: how verify_recheck.py interacts with recheck.sh)
