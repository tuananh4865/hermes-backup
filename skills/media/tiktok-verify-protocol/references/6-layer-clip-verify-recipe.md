# 7-Layer Clip Verification Recipe (clip final .mp4) — UPDATED 21/07/2026

**Source scripts** (shipped with `tiktok-video-editor` skill):
- `~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py` → L3
- `~/.hermes/skills/media/tiktok-video-editor/scripts/scan_false_start.py` → L6
- `~/.hermes/skills/media/tiktok-video-editor/scripts/scan_treo.py` → **L7 (NEW 21/07 — HARD CHECK)**

**Input contract**:
- `<clip.mp4>` — final rendered output (path user-specified)
- `<source.mp4>` — original raw footage (for L5 ratio)
- Optional: filename hint (e.g. `clip_0031_V1_87s_FINAL_...mp4` → target duration = 87s)

**Layer definitions** (the 7 L's):

| L | Check | Tool | Pass criteria |
|---|-------|------|---------------|
| L1 | File size > 30 MB | `ls -la` + `du -m` | ≥ 30 MB |
| L2 | Spec 1080×1920 h264 yuv420p, audio 44100 Hz | `ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,pix_fmt -of default=nw=1` + `select_streams a:0 -show_entries stream=codec_name,sample_rate,channels` | All fields match |
| L3 | Audio fade at every cut boundary | `check_audio_fade.py` | **exit 0** AND output "✅ PASS - All N cut boundaries" |
| L4 | Duration vs filename | `ffprobe -show_entries format=duration` | `|actual - target| ≤ 5s` |
| L5 | Source/clip speed ratio plausible | `ffprobe` × 2 + python ratio | Actual ratio in 1.0-3.0x range; report mismatch if differs from task brief (PITFALL #23: Mode B → use indirect keep_coverage 30-80%) |
| L6 | No FALSE START (anchor/SP over-repeat) | `scan_false_start.py` | **exit 0** |
| L7 | **No CÂU TREO (cut mid-sentence) — HARD CHECK** | `scan_treo.py` | **exit 0** — if exit 1 → MUST re-edit keep_plan, list each câu treo with ts + text + reason |

**Critical recipes** (PITFALL #25 + #26):

```bash
# L3 — audio fade (exit 0 = PASS)
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py \
    "<clip.mp4>" >/tmp/l3_out.txt 2>&1
L3=$?
cat /tmp/l3_out.txt | tail -20

# L6 — false start (NEVER pipe exit code through tail)
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/scan_false_start.py \
    "<clip.mp4>" >/tmp/l6_out.txt 2>&1
L6=$?      # ← real exit code, NOT filter exit
cat /tmp/l6_out.txt

# L7 — câu treo (HARD CHECK — exit 1 = must re-edit)
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/scan_treo.py \
    "<clip.mp4>" >/tmp/l7_out.txt 2>&1
L7=$?      # ← real exit code (script truncates output to 15 issues!)
cat /tmp/l7_out.txt

# ⚠️ scan_treo.py chỉ print first 15 issues + "... +N câu khác" (saw 19 thực tế vs 15 in report).
# Để list FULL câu treo, dump JSON whisper + run scan logic inline:
python3 << 'PYEOF'
import subprocess, json, os, sys, re, tempfile
v = "<clip.mp4>"
audio = tempfile.mktemp(suffix='.wav')
subprocess.run(['ffmpeg', '-y', '-i', v, '-vn', '-acodec', 'pcm_s16le',
                '-ar', '16000', '-ac', '1', audio], capture_output=True, timeout=60)
out_dir = tempfile.mkdtemp(prefix='whisper_treo_')
json_p = f'{out_dir}/{os.path.basename(audio).replace(".wav",".json")}'
subprocess.run(['mlx_whisper', '--model', 'mlx-community/whisper-medium-mlx',
                '--language', 'vi', '--output-dir', out_dir,
                '--output-format', 'json', '--word-timestamps', 'True', audio],
               capture_output=True, timeout=300)
d = json.load(open(json_p)); segs = d['segments']
issues = []
for i, s in enumerate(segs[:-1]):
    t = s['text'].strip(); nx = segs[i+1]['text'].strip()
    if not t: continue
    cm = re.search(r'\s(và|với|của|là|thì|nhưng|nên|rồi|mà|để|cho|khi|nếu|vì|đó|như|vậy|nhé|nha)$', t.lower())
    ec, es = bool(cm), len(t.split()[-1]) <= 2
    nl = nx[0].islower() if nx else False
    sig = sum([ec, es, nl])
    if sig >= 2:
        issues.append((s['start'], s['end'], sig, t[:80], nx[:50], cm.group().strip() if cm else ''))
print(f'TOTAL: {len(issues)} câu treo')
for j,(st,en,sig,t,nx,c) in enumerate(sorted(issues), 1):
    print(f'#{j:2d} [{st:6.2f}-{en:6.2f}] sig={sig} | {t} | next: {nx}')
PYEOF

# L5 — actual speed ratio (case 0031: brief said 1.3x, actual = 2.01x)
SRC=$(ffprobe -v error -show_entries format=duration \
     -of default=noprint_wrappers=1:nokey=1 "<source.mp4>")
CLIP=$(ffprobe -v error -show_entries format=duration \
       -of default:noprint_wrappers=1:nokey=1 "<clip.mp4>")
python3 -c "print(f'src={$SRC}s clip={$CLIP}s ratio={$SRC/$CLIP:.4f}x')"
```

**Verdict table format** (for final report):

```
| Layer | Check                  | Result                       |
|-------|------------------------|------------------------------|
| L1    | Size > 30 MB           | ✅ 68.6 MB                   |
| L2    | 1080×1920/44100Hz      | ✅                           |
| L3    | check_audio_fade       | ✅ exit 0                    |
| L4    | \|actual-87\| ≤ 5      | ✅ 0.167s                    |
| L5    | speed ratio            | ⚠️ actual=2.01x (brief: 1.3x)|
| L6    | scan_false_start       | ❌ exit 1                    |
| L7    | scan_treo (HARD CHECK) | ❌ exit 1 — 19 câu treo      |
```

**Final verdict rule**: VERDICT = FAIL nếu BẤT KỲ layer nào FAIL. L7 = HARD CHECK = nếu exit 1 phải re-edit keep_plan (không ship được).

**Failure modes to remember**:
- `script.py | tail; echo $?` → `$?` = `tail` exit (almost always 0). Use redirect-to-file.
- Don't trust brief's claimed speed without computing actual ratio.
- `scan_false_start.py` thresholds: TÊN SP ≥ 5 mentions = FAIL, anchor "Các bạn" ≥ 3 đầu câu = FAIL, filler đầu câu ≥ 3 = FAIL, TAKE_LAP identical 5-10 word phrase cách 3-20s = FAIL.
- `check_audio_fade.py` PITFALL #39 fix: silence-only boundaries trivially PASS (no fade needed).
- Whisper step in `scan_false_start.py` requires `mlx_whisper` CLI + model `mlx-community/whisper-medium-mlx`. If whisper missing → script fails early.
- **`scan_treo.py` truncates to first 15 issues** in stdout (line 110 `sorted(...)[:15]`) — if total > 15, must re-run inline to dump full list per user requirement "liệt kê cụ thể các câu treo, không tổng quát". Real case 21/07 clip 0030: 19 câu treo, script printed 15 + "+4 câu khác" — bị incomplete.
- **`scan_treo.py` signals (≥2/3)**: (1) conj/filler end: `và/với/của/là/thì/nhưng/nên/rồi/mà/để/cho/khi/nếu/vì/đó/như/vậy/nhé/nha`, (2) last word ≤ 2 chars, (3) next segment starts lowercase. High Vietnamese conversational filler density → expect 15-20 câu treo even on clean edits; semantic filter needed (focus on #1, #9, #11, #13, #15, #17 patterns where meaning actually breaks).
- **L7 != filler-only**: VOUFILLER pattern (e.g. "là", "thì", "đó", "vì vậy" ở cuối) là linking verb/connector hợp lệ trong tiếng Việt hội thoại. Re-edit keep_plan nên ưu tiên câu MẤT Ý (predicate bị cắt) hơn câu chỉ có filler pattern.
