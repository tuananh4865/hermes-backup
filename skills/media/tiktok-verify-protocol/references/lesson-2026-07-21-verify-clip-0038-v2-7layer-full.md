# Lesson 2026-07-21 — Verify clip 0038 V2 với verify_clip_full.py 7-layer (transcript-level)

## Context

User request 21/07/2026 13:50: "Verify clip 0038 V2 với 7 LAYERS tool THẬT" với input `clip_0038_V2_100s_FINAL_POCKETBAR_OPP_KNET.mp4`. L4 yêu cầu duration 100s. Đây là V2 (re-edit sau V1) nên transcript khác V1 batch log (0038 V1 keep_coverage=56.4% PASS Mode B per `lesson-2026-07-21-verify-7-clip-batch-dji-0029-0038.md`).

Khác với PITFALL #25 (technical-spec verify — codec/duration/keyframes/visual integrity), session này chạy **full transcript-level verify** qua `verify_clip_full.py` (7 layers L1-L7 = spec + 5-dim strict + anchor-lap + false-start + RMS first-3s + RMS delta vs source + motion).

## Tool chính

```bash
python3 ~/.hermes/skills/media/tiktok-verify-protocol/scripts/verify_clip_full.py \
    "$INPUT" \
    --report /tmp/clip_0038_V2_verify.md
# Exit 0 = PASS all 7 layers, Exit 1 = issues found
```

Output khi run thực tế:
- L1 PASS (1080×1920 h264 yuv420p + aac 44100Hz, 100.70s, 6.42Mbps)
- L2 ISSUES (2 FILLER hits seg 33 + seg 34 ở 97-101s)
- L3 REVIEW (29 anchor-lap pairs, gap=0 consecutive edits = rhetoric)
- L4 REVIEW (1 false-start candidate seg 16↔17, gap=2.6s, 6/8 first-word match)
- L5 PASS (first-3s mean_volume=-24.3dB, audible)
- L6 SKIPPED (no --source flag)
- L7 PASS (pixel diff 83.39% @ t=5 vs t=10)
- **VERDICT: FAIL (33 issues)**

## PITFALL #26 — GOP/keyframe extraction gotcha với -skip_frame nokey + csv=p=0

### Vấn đề

```bash
# KHÔNG hoạt động — output rỗng (chỉ newline) cho MP4 encode bằng libx264 + Lavf:
ffprobe -v error -select_streams v:0 -skip_frame nokey \
    -show_entries frame=pkt_pts_time -of csv=p=0 "$FILE"
# Total keyframes: 0  ← SAI (file có 26 keyframes thật)
```

### Root cause

`-skip_frame nokey` skips ALL non-keyframes, bao gồm cả pkt_pts_time field của remaining I-frames khi combined với `-of csv=p=0`. Format csv=p=0 expect field separator behavior khác JSON.

### Correct approach — JSON + filter pict_type=I

```bash
ffprobe -v error -select_streams v:0 \
    -show_entries frame=pts_time,pkt_pts_time,pict_type,key_frame \
    -of json "$FILE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
iframes = [f for f in data.get('frames', []) if f.get('pict_type') == 'I']
print(f'I-frames: {len(iframes)}')
times = [float(f['pts_time']) for f in iframes]
gaps = [round(times[i+1]-times[i], 3) for i in range(len(times)-1)]
print(f'GOP avg={sum(gaps)/len(gaps):.2f}s min={min(gaps):.2f}s max={max(gaps):.2f}s')
"
# Output: I-frames: 26, GOP avg=3.93s min=1.80s max=7.23s
```

### Repro recipe cho clip 0038 V2

- File: `clip_0038_V2_100s_FINAL_POCKETBAR_OPP_KNET.mp4` (77MB)
- Total frames: 3021 (100.7s @ 30fps)
- I-frames: 26
- GOP avg=3.93s, range 1.80s-7.23s (variable GOP — OK cho TikTok Shorts, không cần 2s fixed)

## PITFALL #27 — lavfi filter stderr pattern (ebur128 / blackdetect / silencedetect)

### Vấn đề

```bash
# KHÔNG capture được summary output:
ffmpeg -v error -i "$FILE" -vn -af "ebur128=peak=true" -f null - 2> /tmp/ebur.log
# /tmp/ebur.log rỗng (size 0)
grep -E "I:|LRA:|Peak" /tmp/ebur.log  # No matches
```

### Root cause

`-v error` SUPPRESSES info-level output từ lavfi filters. `ebur128`, `blackdetect`, `silencedetect` log summary lines ở level INFO (không phải ERROR). Khi pipe `-v error`, agent nghĩ "no output = no issues" — SAI. Blackdetect thực ra KHÔNG print gì khi không phát hiện black frames, nhưng cũng không in "done" line → không có stderr signal để confirm "checked fully".

### Correct approach — capture verbose stderr hoặc explicit metadata

```bash
# Cách 1: Không suppress info-level
ffmpeg -i "$FILE" -vn -af "ebur128=peak=true" -f null - 2> /tmp/ebur.log
grep "Summary" /tmp/ebur.log -A 10
# Output: Integrated loudness I=-21.3 LUFS, LRA=4.9 LU, Peak=-2.5 dBFS

# Cách 2: Dùng volumedetect (luôn in summary regardless of silence)
ffmpeg -hide_banner -i /tmp/first3s.wav -af volumedetect -vn -f null - 2>&1 | grep -E "mean_volume|max_volume|n_samples"
# Output: n_samples=264600, mean_volume=-24.3 dB, max_volume=-4.4 dB

# Cách 3: Cho blackdetect, dùng -v info + grep "black"
ffmpeg -v info -nostats -i "$FILE" -vf "blackdetect=d=0.5:pic_th=0.95:pix_th=0.10" -an -f null - 2> /tmp/black.log
grep -c "black_end" /tmp/black.log  # 0 = no black frames detected
```

### Repro cho clip 0038 V2

- EBU R128 Integrated loudness: **-21.3 LUFS** (Mode B target -23 LUFS, delta +1.7 LU = slightly hot, OK cho narration TikTok)
- LRA: 4.9 LU (very consistent dynamic range)
- True peak: -2.5 dBFS (headroom OK, no clipping)
- Black frames: 0 (clean)
- Silence stretches >1s @ -40dB: 0 (no dead air)

## PITFALL #28 — L4 FALSE START candidate phải re-whisper từng side độc lập

### Vấn đề

`verify_clip_full.py` L4 scan heuristic: gap < 10s + 5+/8 first-word match → flag candidate. Với Vietnamese narration, nhiều pattern tu từ (parallel-reason) match heuristic này = false positive. Phải cross-check bằng cách re-whisper từng seg độc lập để xác nhận đây là 2 takes khác nhau hay cùng 1 đoạn speech bị lặp.

### Workflow

```bash
# Step 1: Extract audio từng seg độc lập theo report timestamps
# Ví dụ clip 0038 V2 L4 candidate: seg 16 @ 47.70-51.10s + seg 17 @ 53.70-56.70s
ffmpeg -y -v error -ss 47.70 -to 51.10 -i "$FILE" -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/seg16.wav
ffmpeg -y -v error -ss 53.70 -to 56.70 -i "$FILE" -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/seg17.wav

# Step 2: Whisper từng cái với --model tiny (nhanh, đủ distinguish)
whisper /tmp/seg16.wav --model tiny --language Vietnamese --output_format txt --output_dir /tmp/whisper_out
whisper /tmp/seg17.wav --model tiny --language Vietnamese --output_format txt --output_dir /tmp/whisper_out

# Step 3: So sánh transcripts
# Nếu transcripts KHÁC biệt rõ + cùng opening = 2 takes (FALSE START thật, cần cut seg 16)
# Nếu transcripts GẦN GIỐNG nhau = cùng take với minor rephrase (parallel-reason rhetoric, KHÔNG cut)
```

### Clip 0038 V2 thực tế — confirmed FALSE START

Seg 16 transcript (tiny decode): *"Thì mà bỏ kế bỏ kế bỏ kế bà vào để quay cho tế bên ngoài đường nâng."*
Seg 17 transcript (tiny decode): *"Thì mà chúng ta bỏ chiếc bác vào đây để ra ngoài đường ngoài tất cả"*

Decoded khác biệt rõ ràng (`bỏ kế bỏ kế` vs `chúng ta bỏ chiếc bác`; `vào để quay` vs `vào đây để ra`), cùng opening hook "Thì mà bỏ ... vào để quay thực tế ở ngoài đường" → **2 takes thật**, đây là FALSE START cần fix.

Action: Cắt seg 16 (47.70-51.10s), giữ seg 17 (53.70-56.70s). Gap 2.6s là dead air giữa 2 takes.

### Anti-pattern (parallel-reason rhetoric — KHÔNG cut)

Nếu transcripts gần giống nhau (chỉ khác 1-2 từ connector như "thì/vì vậy/tiếp đến") thì là **anchor-lap rhetoric**, không phải false start. Ví dụ:

```
Take A: "Vì vậy mình đã xem qua con ốp này. Con ốp này bảo vệ 360 độ luôn."
Take B: "Vì vậy mình đã xem qua con ốp này. Con ốp này bảo vệ 360 độ luôn thật."
```

→ Cùng 1 take với filler cuối, KHÔNG phải 2 takes. Action: chỉ cắt filler.

## PITFALL #29 — L3 anchor-lap gap=0 consecutive edits = rhetoric KHÔNG phải edit-boundary lap

### Vấn đề

`verify_clip_full.py` L3 scan trên clip 0038 V2 flag 29 anchor-lap pairs. Tất cả gap=0 (consecutive segs). Đây KHÔNG phải edit-boundary lap mà là **Vietnamese narration transitions**:

- "Vì vậy mình đã..." → "Đây là con ốp của nhà Knet"
- "Tiếp đến nữa là" → "Nó có cái gấp đôi số lượng O"
- "Ở bên ngoài thì kiểu cái..." → "Nhưng mà về bảo vệ toàn diện"
- "Và ở trên này là 2 cái roll nữa" → "Để mà có thể bảo vệ cái..."

### Correct classification

Anchor-keyword (`à` / `ờ`) match trong consecutive edits là **NORMAL VN narration**, không phải lỗi edit. Khi review report, chỉ tập trung vào pairs có **gap > 0.5s** (chỉ ra 2 takes khác nhau) hoặc **first-word match >= 3** (HOOK LAP per L2).

### Quy tắc phân loại

```python
def classify_anchor_lap(pair):
    if pair['gap'] == 0 and pair['kw'] in ['à', 'ờ']:
        return "RHETORIC (gap=0 consecutive, VN connector)"  # Không cần action
    elif pair['gap'] > 0.5:
        return "REVIEW (gap={:.1f}s suggests different takes)".format(pair['gap'])
    elif pair['match'] >= 3:
        return "HOOK LAP (first-word match >=3)"  # Same as L2 hook_lap_pairs
    else:
        return "RHETORIC"
```

### Clip 0038 V2 — 29 pairs breakdown

- 28/29 pairs: gap=0 consecutive → RHETORIC (no action needed)
- 1/29 pair (16↔17): gap=2.6s → REVIEW → confirmed FALSE START via PITFALL #28 workflow → action: cut seg 16

## PITFALL #30 — FILLER `á` ở cuối clip cần context-aware decision

### Vấn đề

Clip 0038 V2 L2 flag 2 FILLER hits ở seg 33 (97.2-98.2s) + seg 34 (98.2-101.2s). Re-whisper confirm:
- Seg 33: *"Rồi cơm mạnh luôn á, kiểu."*
- Seg 34: *"và mình nghè con cono nhận"* (decode noise từ outro music/silence)

Filler `á` xuất hiện cuối substantive sentence trước khi outro music vào.

### Correct decision matrix

```python
def filler_at_clip_end_action(clip_duration, filler_time, segment_type):
    if filler_time > clip_duration - 5:
        # Filler trong 5s cuối — thường là "luôn á, kiểu." outro natural
        if segment_type == 'outro_call_to_action':
            return "ACCEPT (filler natural vào outro, fix cost > value)"
        else:
            return "RE-TAKE 3s cuối (cheap, clean outro)"
    elif filler_time < 10:
        # Filler ở đầu clip — KHÔNG BAO GIỜ chấp nhận (hook quality critical)
        return "MUST FIX (hook filler destroys retention)"
    else:
        return "STANDARD FIX (cắt filler word, re-stitch)"
```

### Clip 0038 V2 recommendation

- Seg 33 filler `á` @ 97.2s trên clip 100.70s = 3.5s từ cuối → RE-TAKE 3s cuối hoặc ACCEPT (depends on user tolerance)
- Nếu re-take: chỉ cần re-record 97-101s với script clean hơn, splice lại tại 96.5s cut point

## Tools used

- `verify_clip_full.py` (7-layer one-shot)
- `ffprobe -show_format -show_streams -show_frames` (cho GOP + pict_type filter)
- `ffprobe -skip_frame nokey` (đã biết là broken cho MP4 này, PITFALL #26)
- `ffmpeg -af ebur128=peak=true` (L5 audio loudness, PITFALL #27 capture pattern)
- `ffmpeg -vf blackdetect=d=0.5` (silent frame detection, PITFALL #27)
- `ffmpeg -af silencedetect=n=-40dB:d=1.0` (silent stretch detection)
- `ffmpeg -af volumedetect` (alternative cho ebur128, always prints summary)
- `whisper --model tiny --language Vietnamese` (L4 re-whisper protocol, PITFALL #28)
- `PIL.ImageChops` (L7 motion pixel diff independent verification)

## Final verdict cho clip 0038 V2

| # | Layer | Tool | Kết quả |
|---|---|---|---|
| L1 | Spec TikTok | ffprobe | ✅ PASS 1080×1920 h264 yuv420p + aac 44100Hz, 100.70s, 6.42Mbps |
| L2 | 5-dim strict (FILLER) | whisper | ⚠️ 2 FILLER `á` @ seg 33-34 (97-101s, clip end) |
| L3 | Anchor-lap | heuristic | 📝 REVIEW 29 pairs (28 rhetoric + 1 false-start) |
| L4 | FALSE START | heuristic + re-whisper | ⚠️ 1 candidate seg 16↔17 confirmed via PITFALL #28 |
| L5 | RMS first-3s | volumedetect | ✅ PASS mean=-24.3dB, audible |
| L6 | RMS delta vs source | — | ⏭ SKIPPED (no --source) |
| L7 | Motion | PIL | ✅ PASS pixel diff 14.29% @ t=5 vs t=10 |

**Overall: FAIL** — cần fix L4 (cut seg 16) + L2 (re-take 3s cuối hoặc accept filler) trước khi ship.

## Action items

1. **CẮT seg 16 (47.70-51.10s)** để fix L4 false-start
2. **Re-take 3s cuối (97-101s)** để fix L2 filler `á` (hoặc accept nếu user OK với minor filler)
3. **Re-run verify_clip_full.py** sau khi fix — expect PASS nếu cả 2 fix applied
4. **Optional: run với --source flag** để enable L6 (audio RMS delta vs source check)