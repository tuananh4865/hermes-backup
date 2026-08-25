# PITFALL #25 — Technical/Encoding 7-LAYER Verify với tool thật

**Ngày phát hiện:** 21/07/2026 (clip 0037 V1 — user yêu cầu "verify clip 0037 với 7 LAYERS tool THẬT", focus vào technical compliance không phải transcript/filler).

## Trigger

Khi user yêu cầu "verify clip với N LAYERS tool THẬT" / "verify đúng spec kỹ thuật" / "check encoding integrity" — KHÔNG phải verify transcript/filler/hook. Focus vào: codec, duration exact, resolution, audio intact, visual không corrupt.

Khác với verify-protocol chính (transcript-level): session này dùng 100% shell tools, không cần whisper.

## 7-Layer pattern (chạy bằng shell, parallel batching)

### Turn 1 — song song (độc lập, tiết kiệm round-trips)

**L1 File identity:**
```bash
ls -la "$FILE"
shasum -a 256 "$FILE"
stat -f "%z bytes" "$FILE"
du -h "$FILE"
```

**L2 Codec/Resolution/fps:**
```bash
ffprobe -v error -show_format -show_streams -of json "$FILE"
```
Check: codec_name (h264), width/height (1080×1920), pix_fmt (must be `yuv420p` cho TikTok), profile (High), level (40), nb_frames.

**L7-prep Integrity check (chạy song song L1/L2):**
```bash
ffmpeg -v error -i "$FILE" -f null -
echo "exit=$?"  # exit 0 = không corrupt
```

### Turn 2 — song song

**L3/L4 Duration:** từ L2 ffprobe output — `format.duration` (raw) + so với spec (vd "88s"). Tolerance ≤ 1 frame (33.3ms @ 30fps). Audio thường exact hơn video.

**L5 Audio integrity:** stream index 1 từ L2 — codec (aac LC), sample_rate (44100), channels (2 stereo), bit_rate (~128 kbps OK), nb_frames.

**L6 Video integrity:**
```bash
# Keyframe count (GOP analysis)
ffprobe -v error -select_streams v:0 -skip_frame nokey \
  -show_entries frame=pts_time -of csv=p=0 "$FILE" | wc -l
# GOP ~5-7s OK cho TikTok Shorts, không cần 2s fixed
```

### Turn 3 — L7 Visual content sampling

**Bước 1: Extract 5 frames @ 0/25/50/75/100%**
```bash
OUTDIR="/tmp/clip_verify_frames"
rm -rf "$OUTDIR" && mkdir -p "$OUTDIR"
ffmpeg -v error -i "$FILE" \
  -vf "select='eq(n,0)+eq(n,660)+eq(n,1321)+eq(n,1981)+eq(n,2641)',scale=270:480" \
  -vsync vfr -frame_pts 1 "$OUTDIR/f_%02d.png"
# Adjust N values theo nb_frames/4 mỗi frame
```

**Bước 2: Vision check (parallel, có thể strip output):**
Gọi `vision_analyze` cho mỗi frame song song. **NOTE:** vision model có thể trả `"screenshot removed to save context"` cho 1-2 frames — ĐÂY là lý do cần fallback.

**Bước 3: Fallback pixel stats (BẮT BUỘC, không được skip):**
```python
from PIL import Image
import os

OUTDIR = "/tmp/clip_verify_frames"
frames = sorted(os.listdir(OUTDIR))
print(f"{'FRAME':<18} {'BRIGHTNESS':<12} {'STD':<10} {'VERDICT'}")
print("-" * 70)
for fn in frames:
    p = os.path.join(OUTDIR, fn)
    img = Image.open(p).convert("L")  # grayscale
    pixels = list(img.getdata())
    n = len(pixels)
    mean = sum(pixels) / n
    std = (sum((x - mean) ** 2 for x in pixels) / n) ** 0.5
    if mean < 5:
        v = "BLACK (suspicious)"
    elif mean > 250:
        v = "WHITE (suspicious)"
    elif std < 5:
        v = "FLAT (corrupt)"
    else:
        v = "OK (real content)"
    print(f"{fn:<18} {mean:>8.2f}    {std:>7.2f}   {v}")
```

**Thresholds:**
- `mean < 5` → BLACK frame (corrupt or empty)
- `mean > 250` → WHITE frame (corrupt or overexposed)
- `std < 5` → FLAT frame (no variation = corrupt)
- `mean 80-180 + std > 30` → Real content ✅
- `mean 50-200 + std > 20` → Acceptable real content

## Evidence format PASS/FAIL

```markdown
| # | Layer | Check | Kết quả | Tool |
|---|---|---|---|---|
| L1 | File existence & basic | Tồn tại, hash, size | ✅ XX MB (X bytes) | ls, stat, shasum |
| L2 | Codec/Resolution/fps | h264, 1080×1920, 30fps | ✅ H.264 High@4.0, 9:16, yuv420p | ffprobe -show_streams |
| L3 | Duration raw | Format duration | ✅ 88.066667s | ffprobe -show_format |
| L4 | Duration = spec | Match yêu cầu | ✅ 88.067s ≈ 88s (off 66.7ms) | ffprobe duration_ts |
| L5 | Audio integrity | AAC LC 44.1kHz stereo | ✅ AAC LC, 44100Hz, 2ch | ffprobe index 1 |
| L6 | Video integrity | Bitrate/profile/keyframes | ✅ 5.6 Mbps, High@4.0, 16 keyframes | ffprobe -skip_frame nokey |
| L7 | Visual sampling | Frame extract + pixel analysis | ✅ 5/5 OK (brightness X-Y, std > 30) | ffmpeg extract + PIL |
```

Sau đó 1 phần **"Lưu ý nhỏ (không fail)"** ghi deviation không critical:
- Duration lệch <100ms (1-3 frames ở 30fps là bình thường do encoder)
- GOP variable 5-7s thay vì 2s fixed (vẫn seekable)
- Data stream tmcd từ Pocket 3 (không ảnh hưởng playback)

Kết luận cuối: **"PASS — 7/7 layers đều pass"** hoặc list chính xác layer fail.

## PITFALL cụ thể (đừng quên)

- ❌ KHÔNG dùng `ffmpeg signalstats` filter để check brightness trên PNG đã extract — output im lặng không in ra terminal. Dùng PIL/Python thay thế.
- ❌ KHÔNG trust vision model 100% — luôn có fallback pixel stats vì model có thể strip 1-2 frames với message "screenshot removed to save context".
- ❌ KHÔNG fail chỉ vì duration off <100ms (1-3 frames ở 30fps là bình thường do encoder rounding).
- ❌ KHÔNG fail khi có data stream tmcd từ Pocket 3 source — ghi nhận "không ảnh hưởng playback" thay vì fail.
- ❌ KHÔNG bỏ L7-prep integrity check (`ffmpeg -f null -`) — đây là check tuyệt đối cho corruption, chạy song song L1/L2 turn đầu.
- ✅ LUÔN chạy L1 hash + L2 ffprobe + L7-prep ffmpeg -f null song song ngay turn đầu (độc lập hoàn toàn).
- ✅ LUÔN parallel batch vision_analyze cho 5 frames cùng lúc — không serial.
- ✅ Real content frame: brightness 80-180 + std > 30. Nếu std < 5 → corrupt.
- ✅ GOP 5-7s OK cho TikTok Shorts, không cần 2s cố định.

## Repro recipe (clip 0037 V1 — đã pass)

File: `clip_0037_V1_88s_FINAL_BODY_MIST_AMAP.mp4` (60.27 MB, SHA256 `ca67f789...638a8`)
Spec: 1080×1920, 30fps, H.264, AAC 44.1kHz stereo, ~88s, Pocket 3 source.

Results: H.264 High@4.0, 1080×1920 yuv420p, 88.067s video / 88.000s audio, AAC LC 127.5 kbps, 5.6 Mbps, 16 keyframes, 5/5 frames real content (brightness 99-115, std 45-50). **PASS.**

---

# PITFALL #26 — Audio + Motion + Vision CROSS-MODAL verify (câu treo / fade / speed / false-start)

**Ngày phát hiện:** 21/07/2026 (clip 0029 V1 — user yêu cầu "verify clip 0029 với 7 LAYERS tool THẬT" nhưng **L3 fade, L5 speed, L6 false-start, L7 câu treo đều cần evidence không phải transcript**).

## Trigger

Khi L3/L5/L6/L7 của 7-layer verify-protocol **KHÔNG dùng được whisper** (vì:
- User chỉ yêu cầu "tool thật" (= shell/ffmpeg, không ASR), HOẶC
- Cần verify nhanh không qua pipeline transcript, HOẶC
- Audio có thể không phải speech thuần (BGM, narration, tiếng động vật...))

Thì dùng **3 cross-modal tools** dưới đây. Đây là supplement cho #25, KHÔNG thay thế — #25 vẫn cần cho L1/L2/L4 spec check.

## L3 fade detection — brightness dense sampling

**Vấn đề:** Vision 1 frame không đủ — content có thể naturally tối/sáng. Phải sample **density 0.1s** cả đầu lẫn cuối.

**Recipe:**
```bash
# Start: 0-3s, mỗi 0.1s
for t in $(seq 0 0.1 3.0); do
  ffmpeg -v error -ss "$t" -i "$FILE" -frames:v 1 -y "frames/dense_start/${t}.png"
done
# End: duration-4s đến duration, mỗi 0.1s
END=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FILE")
for t in $(seq $(echo "$END-4" | bc) 0.1 "$END"); do
  ffmpeg -v error -ss "$t" -i "$FILE" -frames:v 1 -y "frames/dense_end/${t}.png"
done
```

**Python brightness check (BẮT BUỘC — ffmpeg signalstats im lặng khi dùng trên PNG đã extract):**
```python
from PIL import Image
import os

def avg_brightness(path):
    img = Image.open(path).convert("L")
    return sum(img.getdata()) / (img.width * img.height)

all_b = []
for d in ["frames/dense_start", "frames/dense_end"]:
    for f in sorted(os.listdir(d)):
        all_b.append((f, avg_brightness(os.path.join(d, f))))

print(f"Min brightness in dense samples: {min(b for _,b in all_b):.1f}")
print(f"Max brightness: {max(b for _,b in all_b):.1f}")
```

**Verdict heuristic:**
- Fade-in thật: 3-5 frame đầu `brightness < 30` (gần đen), sau đó ramp up
- Fade-out thật: 3-5 frame cuối ramp down về `brightness < 30`
- KHÔNG fade: min brightness vẫn `> 50` (content thật dao động theo chủ thể)
- **Pocket 3 talking-head clip thường dao động 100-125** → bất kỳ frame nào < 80 hoặc > 200 là suspect

**Pitfall #26-A:** KHÔNG judge fade chỉ bằng 1 frame. Phải dense sample 0.1s để thấy ramp. Nếu clip không có fade-in/out → report "hard-cut" (vẫn OK nếu user không yêu cầu fade).

## L5 speed-change detection — motion YAVG distribution

**Vấn đề:** Muốn biết clip có bị speed ramp (1.0x → 2.0x → 1.0x) ở giữa hay không. Không cần Whisper — dùng motion.

**Recipe:**
```bash
ffmpeg -v error -i "$FILE" \
  -vf "tblend=all_mode=difference,signalstats,metadata=print:file=/tmp/motion.txt" \
  -an -f null -

# Parse YAVG per frame
python3 << 'EOF'
import re
motions = [float(m.group(1)) for m in re.finditer(r"YAVG=([\d.]+)", open("/tmp/motion.txt").read())]
# Phân tích theo 5s windows
for i in range(0, len(motions), 150):
    chunk = motions[i:i+150]
    if chunk: print(f"frames {i}-{i+len(chunk)}  avg={sum(chunk)/len(chunk):.3f}")
# Edge detection
q1 = motions[:len(motions)//4]
mid = motions[len(motions)//4:3*len(motions)//4]
q4 = motions[3*len(motions)//4:]
ratios = [sum(q1)/len(q1), sum(mid)/len(mid), sum(q4)/len(q4)]
if max(ratios) / min(ratios) > 1.8:
    print("LIKELY SPEED CHANGE detected")
else:
    print("Motion roughly uniform")
EOF
```

**Heuristic:** Motion YAVG của frame-difference ~ tỷ lệ thuận với speed. Ratio `middle/edges > 1.8x` = speed change. Pocket 3 talking-head thường `mean YAVG 2-4` dao động tự nhiên theo gesture/speech.

**Pitfall #26-B:** Motion cao ở segment nào không phải lúc nào cũng là speed change — có thể là **gesture lớn** (vẫy tay, quay đầu) hoặc **scene cut** (chuyển góc camera). Cross-check bằng vision nếu ratio > 1.5x.

## L6 false-start detection — silence segmentation

**Vấn đề:** False start = speaker bắt đầu nói, dừng giữa chừng, rồi nói lại. Cần phân biệt với **breath pause tự nhiên** (nói liên tục có pause 0.3-0.5s).

**Recipe — dual-threshold silence detection:**
```python
import wave, struct, math
wf = wave.open("audio.wav", "rb")
sr, nframes = wf.getframerate(), wf.getnframes()

def rms(chunk):
    if not chunk: return 0
    return math.sqrt(sum(s*s for s in chunk) / len(chunk)) / 32768.0

def get(s, e):
    wf.setpos(int(s*sr))
    raw = wf.readframes(int((e-s)*sr))
    return list(struct.unpack(f"<{len(raw)//2}h", raw))

# Analyze first 6s in 50ms windows với DUAL threshold
threshold_speech = 0.015   # start speaking
threshold_silence = 0.008  # confirmed silence (lower than speech to avoid breath)

segments, state, start = [], "silence", 0.0
for i in range(120):
    s, e = i*0.05, (i+1)*0.05
    r = rms(get(s, e))
    if state == "silence" and r > threshold_speech:
        state, start = "speech", s
    elif state == "speech" and r < threshold_silence:
        state, segments = "silence", segments + [("speech", start, s)]
```

**False start vs natural breath — verdict heuristic:**
| First speech duration | Gap | Verdict |
|---|---|---|
| < 0.5s | > 0.5s | **LIKELY false start** |
| 0.5-1.0s | 0.3-0.6s | **AMBIGUOUS** (could be breath) |
| > 1.0s | any | **Natural pause** — KHÔNG phải false start |

**Pitfall #26-C:** Whisper/ASR thường bỏ sót false start < 0.5s vì nó quá ngắn. Silence-based detection đáng tin hơn cho pattern này.

## L7 câu treo detection — 3-modality cross-check

**Đây là verify quan trọng nhất và khó nhất.** Phải confirm audio bị cắt giữa câu (không phải fade out chủ động).

**Modality 1: Audio tail RMS (peak analysis)**
```python
# Last 3s, per 100ms
samples = get(duration-3, duration)
for i in range(30):
    chunk = samples[(30-i-1)*int(0.1*sr):(30-i)*int(0.1*sr)]
    peak = max(abs(s) for s in chunk)
    print(f"t-{3.0-i*0.1:.1f}s  peak={peak} ({peak/32768*100:.1f}%)")
```

**Modality 2: Hard-cut vs fade ratio**
```python
last_50ms = samples[-int(0.05*sr):]
last_500ms = samples[-int(0.5*sr):]
peak_50 = max(abs(s) for s in last_50ms)
peak_500 = max(abs(s) for s in last_500ms)
ratio = peak_50 / peak_500 if peak_500 else 0
# ratio < 0.1 = audio đã fade sạch (peak 0.05s cuối << peak 0.5s cuối)
# ratio > 0.5 = hard cut (peak cuối vẫn còn active, không fade)
```

**Modality 3: Vision cross-check frame tại điểm cut**
Gọi `vision_analyze` frame ở `duration - 0.5s` (giữa câu) và frame ở `duration` (cuối clip):
- "Person's mouth still open mid-sentence?" → YES = câu treo
- "Expression calm/closed mouth, looking at camera?" → NO = kết thúc bình thường

**Verdict matrix (3-modality):**
| Audio tail (RMS) | Last 0.5s vs 0.05s ratio | Vision mouth | Verdict |
|---|---|---|---|
| Active speech (RMS > 0.02) đến sát cuối | ratio > 0.5 (hard cut) | Mouth open | **CÂU TREO confirmed** |
| Active speech đến sát cuối | ratio < 0.1 (fade sạch) | Mouth closed | Normal fade-out |
| Silence kéo dài > 1s cuối | ratio < 0.1 | Mouth closed | Hard cut OK (sentence done) |
| Active → silence → active (2 lần) | any | any | Multi-cut, cần check kỹ |

**Pitfall #26-D (CỰC QUAN TRỌNG):** Vision model MỸ/CN phổ biến hay trả lời **lễ phép** ("mouth slightly parted, calm") khi thực tế miệng đang mở nói. Phải hỏi specific: "Is the mouth visibly OPEN with teeth/tongue showing, consistent with active speech?" — question cụ thể buộc model phân tích.

**Pitfall #26-E:** `silencedetect=noise=-30dB:d=0.1` đôi khi MISS các gap nhỏ (< 0.1s) và gap nhiễu nền cao. Kết hợp cả `silencedetect` filter (cho overview) + RMS manual (cho chi tiết 50-100ms) là robust nhất.

## Evidence format bổ sung

Khi report L3/L5/L6/L7 fail, evidence phải có:
- L3 fade: bảng brightness 0-3s + 110-114s (mỗi 0.1s) — min/max verdict
- L5 speed: motion YAVG per 5s window + ratio q1/mid/q4
- L6 false-start: silence segmentation table (first 6s, 50ms windows)
- L7 câu treo: 3-modality matrix ở trên + vision quote cụ thể ("mouth visibly open with teeth")

**KHÔNG skip modality nào** trong câu treo — audio-only có thể false-positive (người nói "...ờ" rồi cut), vision-only có thể ambiguous (pose "calm" nhưng thực ra chưa hết câu).

## Repro recipe (clip 0029 V1 — partial pass)

File: `clip_0029_V1_114s_FINAL_BODY_MIST.mp4` (77.19 MB)
Results matrix:

| Layer | Result | Evidence |
|---|---|---|
| L1 Size | ✅ | 1080×1920, MP4 |
| L2 Spec | ✅ | H.264 High@4.0, AAC LC 44.1kHz stereo, 5.6 Mbps |
| L3 Fade | ❌ | Min brightness 102.5, max 123.6 → content-driven, NO fade in/out |
| L4 Duration | ✅ | 114.033s ≈ 114s spec |
| L5 Speed | ✅ | Motion YAVG ratio q1:mid:q4 = 1.00:0.87:1.17, no speed change |
| L6 False start | ⚠️ AMBIGUOUS | First speech 0.35-4.35s (4s) + gap 0.65s + speech 5s+. Could be natural breath |
| L7 Câu treo | ❌ | RMS last 0.5s=422 (1.3%), last 0.05s=6 (0.0%); vision 113.5s mouth open; vision 114.0s "slightly parted" = treo |

**OVERALL:** 4/7 PASS sạch, 2 FAIL (L3 fade nếu brief yêu cầu, L7 câu treo confirmed), 1 ambiguous (L6).

---

# PITFALL #27 — Segment boundary frame-duplication check (filter_complex re-render verify)

**Ngày phát hiện:** 27/07/2026 (7 clip V2 batch: 0085/0086/0088/0091/0093/0094/0095 — user yêu cầu "verify 7 clip TikTok v2 đã re-render bằng filter_complex, file cũ dùng `ffmpeg -f concat -c copy` stream-copy bị frame đè/lặp ở segment boundary").

## Trigger

Khi user yêu cầu verify clip đã **re-render** để fix bug concat demuxer (`-f concat -c copy`) gây **frame freezing / duplicate** ở boundary giữa các segment. Đây là scenario KHÔNG nằm trong #25/#26 — đó là verify *clip có đúng spec không*, còn đây là verify *render pipeline có splice segment đúng không*.

Trigger phrases:
- "verify clip V2 đã re-render bằng filter_complex"
- "file cũ dùng concat -c copy, check frame có bị đè/lặp boundary không"
- "check segment splice, frame trước/sau boundary khác nhau không"

## Bug pattern cần phát hiện

`ffmpeg -f concat -i list.txt -c copy output.mp4` (concat demuxer + stream copy):
- Khi 2 segment input có cùng codec/resolution/fps → KHÔNG transcode, chỉ ghép packets
- **BUG:** Tại boundary, GOP của segment B bắt đầu từ next keyframe → các frame giữa boundary và next keyframe bị "treo" lặp lại frame cuối của segment A
- Visual: ~10-30 frame bị duplicate (giữ nguyên pose/position) → trông như video bị "lag"

`filter_complex` concat (e.g., `[0:v][0:a][1:v][1:a]...concat=n=N:v=1:a=1[outv][outa]`) → transcode lại từng frame, KHÔNG có bug freeze.

**Verify task:** confirm re-render KHÔNG còn frame freeze ở mọi boundary.

## 3-LAYER verify protocol (proven PASS trên 7 clip batch)

### Layer 1 — STRUCTURAL (file integrity, parallel ffprobe)
```bash
for c in $CLIPS; do
  F=$(ls clip_${c}_V2_*.mp4 | head -1)
  ls -la "$F"
  ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate \
    -show_entries format=duration,size,bit_rate -of default=noprint_wrappers=1 "$F"
done
```
Check: size > 10MB, width=1080, height=1920, codec=h264, fps=30/1, audio=44100/aac, duration ≈ filename claim ±1s.

### Layer 2 — SEMANTIC (pre-speed + keep_plan + source symlink)
```bash
# Mỗi clip phải có:
# - tmp/clip_NNNN/v3_pre_speed.mp4 (>30MB, duration = keep_plan.expected_duration ±1s)
# - tmp/clip_NNNN/keep_plan.json có field "keeps" (array ≥4 segments)
# - tmp/clip_NNNN/source.MOV symlink RESOLVED
ls -la "tmp/clip_${c}/v3_pre_speed.mp4"
python3 -c "import json; d=json.load(open('tmp/clip_${c}/keep_plan.json')); print(len(d['keeps']), d['expected_duration'])"
readlink "tmp/clip_${c}/source.MOV"
```
Verify symlink target file actually exists (broken symlink = source footage moved/deleted = clip render unreliable).

### Layer 3 — FUNCTIONAL (boundary frame diff) — **QUAN TRỌNG NHẤT**

**Bước 1: Tính boundary timestamps trong pre-speed timeline**
```python
import json
with open(f"tmp/clip_{c}/keep_plan.json") as f:
    plan = json.load(f)
cum = 0.0
boundaries = []
for i, k in enumerate(plan["keeps"][:-1]):  # all but last segment
    cum += k["end_padded"] - k["start_padded"]
    boundaries.append(cum)  # end-of-seg-i in pre-speed
print(f"boundaries: {boundaries}")
```
Pre-speed = concat của tất cả segments theo thứ tự. Boundary = cumulative end của segment trước (= start của segment sau).

**Bước 2: Extract 3 frames tại mỗi boundary: t-0.5, t, t+0.5**
```bash
mkdir -p /tmp/clip_verify
V="tmp/clip_${c}/v3_pre_speed.mp4"
for off in -0.5 0 0.5; do
  ts=$(python3 -c "print(f'{${BOUNDARY}+${off}:.3f}')")
  ffmpeg -hide_banner -loglevel error -ss "$ts" -i "$V" -frames:v 1 -q:v 2 -y "/tmp/clip_verify/b${c}_t${ts//./_}.jpg"
done
```

**Bước 3: ⚠️ OUTPUT-SEEK cho frame-accurate extraction (PITFALL #27-A, CỰC QUAN TRỌNG)**
```bash
# ❌ SAI - input-seek snap to keyframe, 2 timestamps < 1 GOP apart cho CÙNG frame
ffmpeg -ss "$ts" -i "$V" -frames:v 1 ...

# ✅ ĐÚNG - output-seek, decode chính xác từng frame
ffmpeg -i "$V" -ss "$ts" -frames:v 1 ...
```

**Adversarial finding từ session này:** Initial test extract với `-ss` BEFORE `-i` (input-seek) ra 21 frames, trong đó có 3 cặp frames MD5-identical (clip 0088 15.47s/15.50s, clip 0093 15.57s/15.60s, clip 0094 15.37s/15.40s). Lúc đầu tưởng là BUG freeze, nhưng thực ra là ffmpeg snap-to-keyframe artifact (timestamps 30ms apart < 1 GOP thường = same keyframe). Re-extract với `-ss` AFTER `-i` (output-seek) → TẤT CẢ MD5 unique → confirm render đúng, không có frame freeze.

**Bài học:** LUÔN dùng output-seek cho boundary check. Nếu thấy MD5-identical frames ở <1 GOP distance, đó là artifact, không phải bug. Verify lại bằng output-seek trước khi kết luận.

**Bước 4: Pixel-level diff bằng PIL (objective signal)**
```python
from PIL import Image
import numpy as np

def diff_stats(a_path, b_path):
    a = np.array(Image.open(a_path).convert("RGB"), dtype=np.int16)
    b = np.array(Image.open(b_path).convert("RGB"), dtype=np.int16)
    mae = float(np.mean(np.abs(a - b)))
    pcc = float(np.corrcoef(a.flatten(), b.flatten())[0,1])
    diff = np.mean(np.abs(a - b), axis=2)
    pct_changed = float((diff > 5).mean()) * 100
    return mae, pcc, pct_changed

# Compare pre-boundary (t-0.5) vs post-boundary (t+0.5)
# SSIM cũng work — ffmpeg -i A -i B -lavfi ssim
```

**Heuristic thresholds:**
- PCC > 0.999 + MAE < 2 + pct_changed < 2% → **NGHI NGỜ FRAME FREEZE** (verify bằng vision + output-seek check)
- PCC 0.7-0.95 + MAE 5-25 → Continuous talking shot (normal)
- PCC < 0.5 + MAE > 25 → Clear scene change (very good)

**Bước 5: vision_analyze cho semantic confirmation**
```python
# Dùng tool vision_analyze (KHÔNG dùng hermes_tools.vision_analyze — đó là wrapper)
# Batch parallel: gọi 3 frames cùng lúc cho mỗi clip
```
Question template:
```
Describe this image in detail: what product is shown, what is the person's 
pose/position, what is the camera angle, and what is in the background?
```

**Distinguish "frame freeze" vs "natural continuous shot":**
- Frame freeze: 2 frames ở boundary CÙNG pose, CÙNG eye state, CÙNG hand position, CÙNG product angle → render bug
- Natural continuous: 2 frames khác nhau ở micro-motion (mouth open/close, blink, hand shift) → valid continuous talking take

**Pitfall semantic awareness:** Một số boundary "tương tự" là EXPECTED, không phải bug:
- HOOK split: seg1 + seg2 cùng 1 continuous HOOK take (silence detection cắt giữa take) → 2 segment visual giống nhau là bình thường
- Long talking shot: speaker giữ product 30s+ liên tục → seg2→seg3 boundary có thể fall trong cùng 1 shot
- Cross-check bằng source timestamp: nếu seg2.start_padded > seg1.end_padded trong source (overlap), thì visual giống nhau là do 2 segment overlap trong source

## PITFALL cụ thể (đừng quên)

- ❌ **KHÔNG dùng input-seek (`-ss` BEFORE `-i`) để extract frame-accurate** — sẽ tạo MD5-identical frames do keyframe snap, gây false-positive "frame freeze". LUÔN dùng output-seek (`-ss` AFTER `-i`) cho boundary check.
- ❌ **KHÔNG judge chỉ bằng pixel diff** — talking-head clip có thể có PCC > 0.99 ở mid-sentence (người đứng yên nói). Phải vision-analyze để confirm có thực sự là duplicate hay chỉ là tự nhiên.
- ❌ **KHÔNG bỏ L2 source symlink check** — broken symlink = footage moved = clip unreliable dù file render OK.
- ❌ **KHÔNG check chỉ 1 boundary rồi kết luận** — re-render có thể fix được boundary 1 nhưng vẫn freeze ở boundary 3, 5, 7. Nếu user chỉ yêu cầu "1 boundary đầu tiên", thì chỉ cần 1 — NHƯNG nếu nghi ngờ, check thêm boundary khác (boundary giữa 2 segment có source cách xa nhau = real scene change, dễ phát hiện freeze nhất).
- ❌ **KHÔNG tin MD5 identical = frame freeze** — đầu tiên check xem có phải output-seek hay input-seek. Nếu là input-seek → false positive.
- ✅ LUÔN chạy L1+L2 song song turn đầu (độc lập).
- ✅ LUÔN parallel batch vision_analyze (3 frames × N clips = 3N calls / batch).
- ✅ Tính boundary từ keep_plan.json TRƯỚC khi extract, đừng đoán.
- ✅ Pre-speed duration check (`sum(end_padded - start_padded) ≈ ffprobe duration`) — nếu lệch > 1s thì keep_plan sai.
- ✅ Per-clip verdict format: `VERDICT: PASS/FAIL + 3 layers evidence + raw data (size/MD5/vision desc)`.
- ✅ Final verdict riêng ("OVERALL: PASS/FAIL") + list cụ thể clip nào fail layer nào.
- ✅ Khi thấy MD5 identical ở <1 GOP distance: dùng output-seek verify, nếu MD5 khác → input-seek artifact, render OK.

## Repro recipe (7 clip V2 batch 27/07/2026 — PASS)

Files verified:
| Clip | Product | Pre-Speed Size | Segments | Final Dur | Boundary SSIM | Verdict |
|---|---|---|---|---|---|---|
| 0085 | BODY_MIST | 107.2MB | 10 | 137.833s | 0.911 | PASS |
| 0086 | LENSPEN | 75.6MB | 9 | 97.800s | 0.820 | PASS |
| 0088 | POCKET3_FULL | 61.2MB | 6 | 73.294s | 0.747 | PASS |
| 0091 | BODY_MIST | 78.0MB | 8 | 101.069s | 0.814 | PASS |
| 0093 | BODY_MIST | 81.2MB | 8 | 103.855s | 0.823 | PASS |
| 0094 | POCKET3_FLIP | 39.7MB | 5 | 48.467s | 0.714 | PASS (strongest scene change) |
| 0095 | LENSPEN | 59.2MB | 5 | 81.167s | 0.736 | PASS |

**Key evidence:** Initial input-seek extractions showed 3 pairs MD5-identical (0088, 0093, 0094). Re-extraction với output-seek confirmed all 21 frames unique → ffmpeg keyframe-snap artifact, NOT real video bug.

**OVERALL: PASS ✅** — filter_complex re-render successfully fixed concat demuxer frame-overlap bug.

## Workflow template (copy-paste cho batch verify tương lai)

```bash
# Setup
WORKDIR="/Volumes/Storage-1/Pocket3/Hermes-Edit"
mkdir -p /tmp/clip_verify
cd "$WORKDIR"

# Layer 1+2 parallel (turn 1)
CLIPS="0085 0086 0088 0091 0093 0094 0095"
for c in $CLIPS; do
  F=$(ls clip_${c}_V2_*.mp4 | head -1)
  echo "=== $c ==="
  ls -la "$F"
  ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate \
    -show_entries format=duration -of default=noprint_wrappers=1 "$F"
  echo "--- pre_speed ---"
  ls -la "tmp/clip_${c}/v3_pre_speed.mp4"
  echo "--- keep_plan ---"
  python3 -c "
import json
d = json.load(open('tmp/clip_${c}/keep_plan.json'))
print(f\"segments={len(d['keeps'])} expected={d['expected_duration']:.2f}\")
"
  echo "--- source symlink ---"
  readlink "tmp/clip_${c}/source.MOV"
done

# Layer 3a — tính boundary timestamps
for c in $CLIPS; do
  python3 -c "
import json
d = json.load(open('tmp/clip_${c}/keep_plan.json'))
cum = 0.0
for k in d['keeps'][:-1]:
    cum += k['end_padded'] - k['start_padded']
print(f\"{cum:.3f}\")
" > /tmp/boundary_${c}.txt
done

# Layer 3b — OUTPUT-SEEK extract (frame-accurate, KHÔNG input-seek)
for c in $CLIPS; do
  V="tmp/clip_${c}/v3_pre_speed.mp4"
  B=$(cat /tmp/boundary_${c}.txt)
  for off in -0.5 0 0.5; do
    ts=$(python3 -c "print(f'{${B}+${off}:.3f}')")
    out="/tmp/clip_verify/b${c}_t${ts//./_}.jpg"
    ffmpeg -hide_banner -loglevel error -i "$V" -ss "$ts" -frames:v 1 -q:v 2 -y "$out"
  done
done

# Layer 3c — pixel diff + vision_analyze parallel
python3 << 'EOF'
from PIL import Image
import numpy as np
for c in ["0085","0086","0088","0091","0093","0094","0095"]:
    pre = f"/tmp/clip_verify/b{c}_t[boundary-0.5].jpg"
    post = f"/tmp/clip_verify/b{c}_t[boundary+0.5].jpg"
    # ... diff_stats
EOF
# + vision_analyze tool calls in parallel batch (3 frames per clip × N clips)

# Final report → /tmp/clip_verify/VERDICT.md
```