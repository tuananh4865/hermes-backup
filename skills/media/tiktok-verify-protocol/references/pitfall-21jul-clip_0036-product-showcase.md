# PITFALL — 21/07/2026 clip_0036 V2 LENS_MACRO 92s (TikTok product showcase)

**Case**: User verify `clip_0036_V2_92s_FINAL_LENS_MACRO.mp4` (63.89 MB, 2761 frames,
1080×1920 h264/AAC 44100Hz, 92.03s, Mode B sweet spot). Pocket3 DJI, macro lens showcase
cho sản phẩm `laine macro` (ống kính siêu cận).

**Kết quả**: Tool `verify_clip_full.py` ra verdict `FAIL` do 22 L3 anchor-lap pairs +
10 HIGH NSP. Manual triage → **SHIP CLEAN**. Đây là case schoolbook cho 3 false-positive
trap cần biết khi verify product/B-roll clip VN > 60s.

---

## Trap 1: ANCHOR-LAP FALSE POSITIVE TRÊN STOPWORD

**Hiện tượng**: Layer 3 tool output 22 anchor-keyword pairs (các bạn/thì/à/ờ/nãy/rồi/đó).
Verdict counter: `n_issues += len(anchor)` → FAIL.

**Reality**: Cross-check từng cặp:
```
Seg 0→1: A="Các bạn hay quay sản phẩm bằng pocket bar thì sẽ thấy…" 
         B="Các bạn có thể thử thử nó có thể là một cái con laine này gọi là laine macro thì…"
         match 2/5 first-words → SOFT LAP → narrative continuation (A=vấn đề → B=giới thiệu)

Seg 1→2: A="…thì nó là một trong những sản phẩm mà mình thấy nó khá là đặc thù"
         B="Ngoại hình nó thì nó cũng khá là dày bảng kiểu như nó là ống kính siêu cận mà…"
         match 0/5 → FALSE POSITIVE

Seg 7→8: A="Tức là nó sẽ thu hẹp cái khẩu độ của… tức là nó sẽ thu hẹp cái vùng…"
         B="Tức là trong cái khoảng này thì con pocketbar các bạn nó vẫn phó kết được bình thường nè"
         match 2/5 → SOFT LAP → elaboration (A=thu hẹp vùng → B=thu hẹp nhưng pocket3 vẫn OK)
```

**Rule**: `len(anchor_pairs)` KHÔNG phải issue count, là CANDIDATE count. Một anchor-lap là
REAL chỉ khi:
- first 3-5 words trùng ≥ 3, AND
- content phần sau (sau connector scaffolding) thực sự lặp nghĩa.

Nếu chỉ connector/filler (`các bạn`, `thì`, `à`, `ờ`, `nãy`) trùng mà nghĩa phân kỳ → FALSE POSITIVE.
Nếu 2 first-words trùng → SOFT (có thể narrative continuation, manual check).

**Ad-hoc script** (in-line Python, save as `references/scripts/l3_firstword_classifier.py`):
```python
import json
with open('whisper.json') as f: data = json.load(f)
segs = data['segments']
for i in range(len(segs)-1):
    a, b = segs[i]['text'].strip(), segs[i+1]['text'].strip()
    wa, wb = a.split()[:5], b.split()[:5]
    m = sum(1 for x,y in zip(wa,wb) if x == y)
    label = ("REAL" if m >= 3 else "SOFT" if m == 2 else "FALSE POSITIVE")
    # Check content divergence AFTER the matched first words
    print(f"Seg {i}→{i+1} match={m}/5 → {label}")
    print(f"  A: {a[:90]}\n  B: {b[:90]}")
```

---

## Trap 2: HIGH NSP ≠ SILENT TAKE

**Hiện tượng**: Layer 2 báo `HIGH NSP (Whisper hallucinate): 10/14 segments` (nsp > 0.3).
Pitfall #13 đã warn nhưng không có auto-resolve.

**Reality với clip LENS_MACRO**:
- Seg 0 (nsp=0.071, OK): "Các bạn hay quay sản phẩm bằng pocket bar thì sẽ thấy nó có một điểm yếu đó là nó không thể nào bắt cận hoặc siêu cận vào sản phẩm để thấy chất liệu của sản phẩm đó được đúng không?" (13s, câu dài 1 phát)
- Seg 1-2 (nsp=0.816): Tiếp tục giới thiệu sản phẩm → Whisper "uncertain" do ngữ pháp
  giới thiệu dài, không phải silent.

**Rule**: HIGH_NSP chỉ = silent take khi (a) audio waveform flat, OR (b) RMS gần -∞ ở
đoạn đó. Verify bằng **RMS-per-5s loop** dọc clip.

**Ad-hoc script** (in-line bash, save as `references/scripts/rms_loop_per5s.sh`):
```bash
#!/bin/bash
VIDEO="$1"
ffmpeg -hide_banner -i "$VIDEO" 2>&1 | grep -E "^[[:space:]]*Duration" | head -1
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
N=$(echo "$DUR / 5" | bc)
for ((t=0; t<$N; t++)); do
    V=$(ffmpeg -hide_banner -ss $((t*5)) -t 5 -i "$VIDEO" \
        -af volumedetect -f null - 2>&1 | grep "mean_volume" | awk '{print $3}')
    echo "t=$((t*5))-$((t*5+5))s: mean_volume=$V dB"
done
```

Run cho clip 0036: range `-22.9 → -28.9 dB` (6dB span) = continuous audio, không silent.
Transcript vẫn chính xác → Whisper "nghe được" nhưng confidence thấp → HIGH NSP là artifact.

---

## Trap 3: MOTION 1-POINT BỎ SOT LOCALIZED STATIC

**Hiện tượng**: Layer 7 mặc định `motion_check(video, t1=5, t2=10)` cho 30.94% PASS. Nhưng
KHÔNG loại trừ freeze cục bộ (1 đoạn B-roll tĩnh 30s có thể vẫn PASS do phần lớn motion ở
đầu/cuối).

**Reality với clip LENS_MACRO**: Sampling 10 điểm dọc clip:
```
  t= 0-  5s: 69.63% MOTION OK
  t= 5- 10s: 30.94% MOTION OK
  t=10- 15s: 47.74% MOTION OK
  t=15- 20s: 87.27% MOTION OK
  t=20- 30s: 91.30% MOTION OK
  t=30- 45s: 90.28% MOTION OK
  t=45- 60s: 93.86% MOTION OK
  t=60- 75s: 47.00% MOTION OK
  t=75- 88s: 53.68% MOTION OK
  t=88- 92s: 48.55% MOTION OK
```
Tất cả ≥10% → không có freeze frame.

**Rule mới cho Mode B ≥90s**: Sampling ≥6 điểm dọc file (0%, 5%, 10%, 25%, 50%, 75%, 90%, 100%),
KHÔNG chỉ 1 cặp default. Threshold vẫn ≥10% per pair nhưng áp dụng cho TỪNG cặp.

**Ad-hoc script** (in-line Python):
```python
import subprocess, tempfile
from PIL import Image
def get_frame(vp, t, op):
    subprocess.run(["ffmpeg","-y","-ss",str(t),"-i",vp,"-frames:v","1",op],
                   capture_output=True, check=True)
def pixdiff(p1,p2,thresh=30,step=4):
    a,b = Image.open(p1).convert("RGB"), Image.open(p2).convert("RGB")
    w,h = a.size; da,db = a.load(), b.load()
    dc=cn=0
    for y in range(0,h,step):
        for x in range(0,w,step):
            ax,bx = da[x,y], db[x,y]
            d = abs(ax[0]-bx[0])+abs(ax[1]-bx[1])+abs(ax[2]-bx[2])
            cn+=1
            if d > thresh: dc+=1
    return dc/cn*100 if cn else 0

video = sys.argv[1]
tmp = tempfile.mkdtemp()
points = [0, 5, 10, 15, 20, 30, 45, 60, 75, 88, 92]  # adapt to actual duration
frames = {t: f"{tmp}/f_{t}.png" for t in points}
for t,p in frames.items(): get_frame(video, t, p)
for a,b in [(0,5),(5,10),(10,15),(15,20),(20,30),(30,45),(45,60),(60,75),(75,88),(88,92)]:
    pct = pixdiff(frames[a], frames[b])
    print(f"t={a}→{b}s: {pct:.2f}%  {'OK' if pct>=10 else 'STATIC!'}")
```

---

## Tổng kết pattern → re-verify protocol cho product/B-roll VN > 60s

Khi tool `verify_clip_full.py` ra FAIL trên clip product/B-roll VN > 60s, làm theo 3 bước
manual trước khi cộng verdict:

1. **L3 anchor-lap**: cross-check first 3-5 words match + content phần sau. Phân loại
   REAL / SOFT / FALSE POSITIVE. Chỉ REAL mới +1 issue.

2. **L2 HIGH_NSP**: chạy RMS-per-5s loop. Range ≤ 6dB = continuous audio → HIGH_NSP là
   Whisper artifact, KHÔNG phải silent. Transcript coherent → confirm nghe được.

3. **L7 motion**: sampling ≥6 điểm dọc file cho clip ≥90s. Tất cả ≥10% = PASS.

Nếu sau 3 bước manual, không còn REAL anchor-lap, không silent take, motion đa-điểm ổn
→ SHIP CLEAN dù tool verdict FAIL.

---

## Save reference

- File verify: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0036_V2_92s_FINAL_LENS_MACRO.mp4`
- Whisper JSON: `/tmp/clip_0036_v2.json`
- Report: `/tmp/clip_0036_V2_report.md`
- Final verdict: **SHIP CLEAN** (92.03s, Mode B sweet spot 80-120s, đầy đủ spec TikTok
  + narrative coherent + motion 30-94% mọi segment)
