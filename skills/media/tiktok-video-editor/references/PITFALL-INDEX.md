# PITFALL-INDEX — tiktok-video-editor v0.01

> **MỤC ĐÍCH:** Danh sách PITFALL apply cho v0.01 (fresh rewrite 22/07, không kế thừa version cũ). Sort by ID. Click vào files kế bên để đọc chi tiết.

> **Note versioning:** Skill cũ (v2.13 → v2.37 → v3.74-v3.79) đã backup ở `/Volumes/Storage-1/Hermes/_archive/skill-tiktok-video-editor-v2.37.0-legacy-2026-07-22/`. KHÔNG áp dụng PITFALL/HARD RULE cũ. v0.01 đếm version slate mới.
> **Rule (anh dặn 22/07):** Khi skill được rewrite từ đầu → RESET version về 0.01, KHÔNG giữ version số từ skill cũ dù có "evolution" tiếp nối. Fresh slate.

---

## 🎯 PITFALLS v0.01 (7 cái — captured 22/07 session)

### #75 — Bash `set -e` + Python exit code misinterpretation

**Context:** `recheck.sh` sau khi Python verify FAIL thì vẫn return exit 0 → bug silent khó debug.

**Repro:**
```bash
set -e
python3 verify_script.py   # exit 1
VERIFY_EXIT=$?              # returns 0 từ exit of last cmd
```

**Fix:** Không dùng `set -e` cho verify scripts. Dùng:
```bash
python3 verify_script.py > /tmp/report.txt 2>&1
VERIFY_EXIT=$?
cat /tmp/report.txt
if [ $VERIFY_EXIT -eq 0 ]; then ... else exit $VERIFY_EXIT; fi
```

→ Chi tiết: `pitfall-75-set-e-python-exit-code.md`

---

### #76 — Inline Python heredoc + f-string quote escape

**Context:** `transcribe.sh` có Python script dùng f-string nested quotes trong bash heredoc → SyntaxError `{wtext}: command not found`.

**Fix:** Tách Python script thành file riêng (`generate_transcript_md.py`), gọi qua `python3 script.py`.

→ Chi tiết: `pitfall-76-inline-python-heredoc-fail.md`

---

### #79 — Word-aligned padding required (no audio fade cụt)

**Context:** Whisper segment timestamp rộng hơn word timestamps → từ đầu/cuối KEEP range có dead gap 0.28-0.76s → mất câu khi concat.

**User trigger (22/07):** *"Anh thấy vào đầu và cuối mỗi đoạn cắt audio bị fade out đúng không?"*

**Fix:** `smart_keep_plan.py`:
```python
new_start = first_word_in_range.start - 0.05
new_end = last_word_in_range.end + 0.05
```

**Verified:** 9/9 KEEP ranges padded, saved 1.5s tổng dead gap trong clip 0036 V3.

→ Chi tiết: `pitfall-79-word-aligned-padding-required.md`

---

### #80 — Filler rule after speed 1.3x

**Context:** Speed 1.3x + Concat demuxer làm Whisper re-segment clusters. Một số re-segment có "ừm/ờ/rồi" ở đầu câu → false positive filler flag.

**Fix:** `verify_recheck.py` smart filler rule:
```python
if filler at start:
    gap_before = segs[i].start - segs[i-1].end
    if 0.2 <= gap_before <= 0.7:  # Process transition OK
        continue  # Allow (Whisper re-segmentation sau speed)
    if gap_before > 0.7:          # Cut boundary thật
        continue  # Allow
    if gap_before < 0.2:          # Re-segmentation chặt
        fail_reasons.append(filler)
```

→ Chi tiết: `pitfall-80-filler-rule-after-speed-13x.md`

---

### #81 — Hermes hook auto-mirrors skill files SILENT (v0.01 fresh addition)

**Context:** Hook Hermes auto-detect file writes to `/Volumes/Storage-1/Hermes/skills/<name>/` → invoke auto-mirror sang `~/.hermes/skills/<name>/` mà KHÔNG cần user approval. Em phát hiện lúc revert session 22/07.

**Root cause:** Hook chạy silent trên write_file. Parent agent (em) không biết files ở target đã thay đổi.

**Fix v0.01:**
1. Sau mỗi write ở Hermes → check md5 ở `~/.hermes/skills/<name>/` xem hook đã mirror chưa
2. Nếu muốn commit atomic → chạy explicit `cp -r` sang `~/.hermes/` song song
3. Backup ở `_archive/` KHÔNG được mirror (chỉ changed files mới mirror)

→ Chi tiết: `pitfall-81-hook-auto-mirror-silent.md`

---

### #82 — `BASH_SOURCE` skill path resolution (v0.01 fresh addition)

**Context:** Scripts hard-code `python3 /Volumes/Storage-1/Hermes/skills/.../smart_keep_plan.py` → chỉ work ở Hermes dev path. Khi apply skill sang `~/.hermes/skills/`, scripts SAI path → fail.

**Fix v0.01:** Detect skill path tự động với BASH_SOURCE:
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/smart_keep_plan.py" ...
```

→ Applied cho `smart_pad.sh` và `build_pre_speed.sh` (verified 22/07 end-to-end).

→ Chi tiết: `pitfall-82-bash-source-script-path-detect.md`

---

### #83 — TikTok spec 1080×1920 30fps mandatory (v0.01 fresh addition)

**Context:** Anh yêu cầu verbatim 22/07: *"Mặc định convert xuống 1080x1920 30fps cho phù hợp với tiktok"*.

**Fix v0.01:**
1. Render command áp filter_complex: `scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:...,fps=30,format=yuv420p`
2. HARD GATE `scripts/check_tiktok_spec.py` exit 0 = PASS required trước recheck
3. AAC 44100Hz stereo bắt buộc
4. H.264 high profile level 4.0 (TikTok optimal)
5. `+faststart` cho streaming-friendly moov atom

**Verified:** clip_0036 V3 final.mp4: 1080×1920, 30fps, AAC 44100Hz → ALL PASS.

→ Chi tiết: `pitfall-83-tiktok-spec-1080x1920-30fps.md`

---

## 📚 Legacy Note

Skill v2.13 → v2.37 (24 versions) và v3.74-v3.79 đã deprecated 22/07. PITFALL #1 → #74 không còn apply. v0.01 bắt đầu đếm PITFALL từ #75 trở đi.

Backup đầy đủ ở `/Volumes/Storage-1/Hermes/_archive/skill-tiktok-video-editor-v2.37.0-legacy-2026-07-22/` (nếu muốn tham khảo).

## 📌 Architecture Summary (v0.01)

| Component | Purpose |
|---|---|
| `SKILL.md` | Entry point (210 dòng, 9-step flow + 12 HARD RULES) |
| `scripts/` (13 files) | Pipeline tự động (init_project → transcribe → smart_pad → build_pre_speed → render_speed → recheck → ship) |
| `references/pitfall-*.md` (7 files) | PITFALL #75-#83 chi tiết |
| `references/PITFALL-INDEX.md` | Quick reference + sơ đồ decision making |
| `templates/keep_plan.schema.md` | Keep plan JSON schema example |

## 🎯 PITFALL #81 — Audio-visual desync do Concat demuxer (no afade)

**Context:** `build_pre_speed.sh` v0.01 dùng `ffmpeg -f concat -safe 0` (Concat demuxer). Demuxer này **NO audio filter applied** → audio cut abruptly tại segment boundaries → người nghe bị "pop" + cảm giác hình đi trước tiếng (anh flag 23/07).

**Repro:**
```bash
# Concat demuxer
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
# Output: video frame cuts hard at boundary, audio cuts hard cùng lúc
# → listener cảm giác "speech ends too sharp, image changes instantly"
```

**Fix v0.01.1:** Replace Concat demuxer với `filter_complex`:
```bash
[i:v]trim=start=S:end=E,setpts=PTS-STARTPTS[vN]
[i:a]atrim=start=S:end=E,asetpts=PTS-STARTPTS,
     afade=t=in:st=0:d=0.03,afade=t=out:st={E-S-0.03}:d=0.03[aN]
[v0][a0][v1][a1]...concat=n=N:v=1:a=1[outv][outa]
```
→ 30ms fade in/out mỗi segment = audio mượt, không bị "pop"

**Bonus fix:** macOS bash 3.2 (default) không có `mapfile` builtin. Dùng `mktemp` + `while read` thay thế.

**Verified:** Applied trên clip 0029 (23/07) — audio nghe mượt, không pop. Verified bằng recheck script.

→ Chi tiết: `pitfall-81-audio-visual-desync-no-afade.md`

---

## 🎯 PITFALL #91 — KEEP_PLAN_OVERLAP: audio+visual lặp 2 lần (28/07)

**Context:** User flag 28/07 lần 2: 7 clip ship 26/07 "vẫn bị lặp overlap". Em đã re-render 7 clip với `filter_complex` thay concat demuxer, subagent PASS SSIM boundary, nhưng user VẪN thấy lặp. Root cause: **keep_plan.json có vùng source overlap giữa 2 keep liên tiếp** (e.g. clip_0088 RECAP [69.09-84.73] + DETAIL [83.75-93.31] overlap 0.98s).

**Real case 28/07 (7 clip ship 26/07):**
- clip_0085: 0.52s overlap
- clip_0086: 0.58s overlap
- clip_0088: **2.22s overlap** (worst)
- clip_0091: 0.54s overlap
- clip_0093: 0.50s overlap
- clip_0094, 0095: 0s (clean)

**Repro:**
- OLD duration khớp `sum(end_padded - start_padded) / 1.3` (with overlap)
- NEW duration khớp `sum_no_overlap / 1.3` → trim OK

**Fix v0.05.1:**
1. `python3 scripts/check_overlap.py <keep_plan.json>` — detect overlap (exit 1 nếu có)
2. `python3 scripts/check_overlap.py <file> --auto-fix --in-place` — auto-trim `end_padded = min(end_padded, next.start_padded)`
3. `build_pre_speed.sh` có defensive auto-trim layer (phòng khi keep_plan.json bỏ sót)

→ Chi tiết: `pitfall-91-keep-plan-overlap-audio-repeat.md`
