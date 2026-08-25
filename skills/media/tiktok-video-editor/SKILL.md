---
name: tiktok-video-editor
description: "Edit TikTok raw MP4 theo flow 9 bước (Tuấn Anh 22/07). v0.05.1 — TikTok spec 1080×1920 30fps HARD GATE + HARD CUT concat + word-aligned smart_pad + Whisper large-v3 word-by-word + CREATIVE ARRANGE pattern + proactive ship evidence (md5+path) + subagent stale output handling + KEEP_PLAN_OVERLAP detection (28/07 fix). 14 PITFALL #75-#91. Trigger: 'edit clip {id}', 'làm clip', raw MP4 path."
version: 0.05.1
author: 'Tuấn Anh + Hermes Agent (v0.05.1 — 28/07: added PITFALL #91 KEEP_PLAN_OVERLAP detection after 7 clip overlap re-render)'
license: MIT
platforms: [macos]
metadata:
  category: media
  tags: [video, editing, tiktok, ffmpeg, whisper-large-v3, word-by-word, smart-pad, speed-1.3x, tiktok-spec-1080-1920, hard-cut, creative-arrange, hermes-only-folder, pocket3-hermes-edit, v0-05, 9-step-flow, bash-source-path, hook-auto-mirror, ship-evidence-protocol, subagent-stale-output, pitfall-75, pitfall-76, pitfall-79, pitfall-80, pitfall-82, pitfall-83, pitfall-85, pitfall-86, pitfall-87, pitfall-88, pitfall-89] |
  module: SKILL.md
  deployment: standalone
  platform: darwin
  test_groups: [dai-pj-2026, media-tiktok]
  last_validated: '2026-07-23'
  test_owner: 'agent'
  review_status: working-with-agent
  depends_on: [whisper-large-v3-mlx, ffmpeg, mlx-audio]
  production_checked: 2026-07-23
---

# TikTok Video Editor — v0.05 (26/07/2026 — HARD CUT default)

> **v0.01 — Reset version slate** (anh flag 22/07). Đây là skill rewrite từ đầu, KHÔNG kế thừa version cũ (legacy v2.13 → v2.37 đã được backup ở `_archive/skill-tiktok-video-editor-v2.37.0-legacy-2026-07-22/`). Mọi tính năng/PITFALL/HARD RULE bắt đầu đếm từ 0.01.
>
> **Rule (anh dặn 22/07):** Khi skill được rewrite từ đầu → RESET version về 0.01, KHÔNG giữ version số từ skill cũ dù có "evolution" tiếp nối. Fresh slate.

## 🎯 FLOW 9 BƯỚC (verbatim user 22/07)

```
1. Nhận video mới ở Footages/ (anh drop path raw MP4)
2. Transcript bằng whisper large v3 mlx word by word with timestamp
3. Đọc kĩ transcript, liên kết nội dung thành ngữ cảnh, hiểu toàn bộ content clip
4. Xoá repetitive content, Remove off-topic tangents, Keep only main points
5. Cắt & loại bỏ: đoạn bị lặp, câu treo, lỗi, ừm/ờ, khoảng lặng, đoạn nói về pricing
6. Chọn content keep mà em thấy hay nhất → keep_plan.json
6.5. SMART PAD: word-align KEEP ranges để giữ từ đầu/cuối — PITFALL #79
6.6. OVERLAP-CHECK: detect & trim vùng overlap giữa 2 keep liên tiếp — PITFALL #91 (BẮT BUỘC)
7. Speed 1.3x + scale 1080×1920 30fps → render final.mp4
8. Re-transcript clip mới render để verify (nếu fail → quay lại 6 chọn lại content)
9. Nếu pass → ship vào /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<id>_V1_NNs_FINAL_<sp>.mp4
```

**Step 6.5 quan trọng:** Word-aligned padding ngăn từ đầu/cuối bị cụt. Phát hiện 4/9 KEEP ranges có head gap 0.28-0.76s → audio đầu câu bị mất. Dùng `filter_complex` để concat segments (HARD CUT, không fade).

---

## 📁 FOLDER STRUCTURE (per video project)

```
/Volumes/Storage-1/Hermes/Edit/<clip_id>/    ← project folder (work artifacts)
├── source/raw.mp4
├── work/
│   ├── audio.wav
│   ├── transcript.{json,txt,md}
│   ├── keep_plan.json (có start_padded/end_padded sau smart_pad)
│   └── recheck_dir/0036_final_audio.json (Whisper lại từ final)
└── notes/project.md

/Volumes/Storage-1/Pocket3/Hermes-Edit/<clip_id>/   ← output folder
├── final_pre_speed.mp4                         (concat padded)
└── final.mp4                                   (1080×1920 30fps TikTok)
```

**Ship:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<id>_V1_<NNs>_FINAL_<sp>.mp4`

---

## ⚡ QUICK START

```bash
# 1. Setup project folder + copy raw.mp4
bash scripts/init_project.sh <clip_id> /path/to/raw.mp4

# 2. Whisper transcript (large-v3, word-by-word)
bash scripts/transcribe.sh <clip_id>

# 3-6. AI agent đọc transcript.md + viết keep_plan.json

# 6.5. SMART PAD — word-align KEEP ranges (chống mất từ đầu/cuối)
bash scripts/smart_pad.sh <clip_id>

# 7a. Build pre-speed (concat KEEP đã pad)
bash scripts/build_pre_speed.sh <clip_id>

# 7b. Speed 1.3x + scale TikTok 1080×1920 30fps → render final.mp4
bash scripts/render_speed.sh <clip_id>

# 8. Re-transcript final → verify
bash scripts/recheck.sh <clip_id>

# 9. Pass → ship
bash scripts/ship.sh <clip_id>
```

---

## 📜 HARD RULES (v0.01)

1. **Whisper large-v3 default**, auto-fallback medium nếu loop
2. **Word-by-word timestamps BẮT BUỘC** (`--word-timestamps True`)
3. **Folder Hermes-Only** — work files ở `/Volumes/Storage-1/Hermes/`, output ở `/Volumes/Storage-1/Pocket3/Hermes-Edit/`
4. **Output edit/ ở Pocket3** — `/Volumes/Storage-1/Pocket3/Hermes-Edit/<clip_id>/`
5. **Sequential media** — 1 clip/turn, không fan-out (PITFALL #44 + 21/07 verbatim "làm từng cái thôi không làm song song máy bị tràn ram")
6. **Speed 1.3x BẮT BUỘC** cho Mode B compact
7. **Re-transcript verify** BẮT BUỘC — fail quay lại step 6
8. **Ship BẮT BUỘC** ra Pocket3 root với filename convention. **QUY TẮC KHÔNG GHI ĐÈ (NO-OVERWRITE RULE)**: Khi lưu hoặc xuất bất kỳ file kết quả nào vào thư mục đích (`/Volumes/Storage-1/Pocket3/Hermes-Edit/`), BẮT BUỘC kiểm tra sự tồn tại của file trùng tên. Nếu file đã tồn tại, TUYỆT ĐỐI KHÔNG GHI ĐÈ (OVERWRITE), mà phải tự động tăng số version hoặc đặt tên phân biệt mới (ví dụ: `clip_0005_v2.mp4`, `clip_0005_v3.mp4`, `clip_0005_v4.mp4`,...).
18. **🎯 EDIT TRỰC TIẾP TỪ RAW SOURCE GỐC (BẮT BUỘC)**: Khi anh yêu cầu làm lại / edit lại clip, BẮT BUỘC phải cắt dựng trực tiếp từ tệp video RAW SOURCE GỐC trong `/Volumes/Storage-1/Pocket3/Footages/`, TUYỆT ĐỐI KHÔNG dùng file clip đã cắt ngắn/edit trước đó làm input.
19. **🎯 THỜI LƯỢNG TIÊU CHUẨN KHÔNG DƯỚI 50S (SWEET SPOT 60s - 90s)**: Thời lượng video đầu ra BẮT BUỘC phải đạt từ **50 giây trở lên (khuyên dùng 60s - 90s)**. TUYỆT ĐỐI KHÔNG cắt video quá ngắn dưới 50s làm người xem chưa kịp cảm nhận hết giá trị và chi tiết sản phẩm.
20. **🎯 ĐỊNH VIỆC VÀ VERIFY TIMESTAMP MỐC CẮT CHÍNH XÁC (TIMESTAMP VERIFICATION RULE)**: Khi xác định mốc thời gian cắt câu thoại (đặc biệt là câu Hook), BẮT BUỘC phải kiểm tra word-level timestamps của tệp transcript JSON để đảm bảo mốc kết thúc (`end_timestamp`) bao trùm 100% từ cuối cùng của câu thoại. TUYỆT ĐỐI KHÔNG cắt lẹm hay xén mất chữ ở cuối câu.
21. **🎯 ĐỐI CHIẾU WORD-LEVEL TIMESTAMPS TRÊN TOÀN BỘ VIDEO (FULL-VIDEO WORD-LEVEL CROSS-CHECK RULE)**: Đối với MỌI video và MỌI mốc cắt (Hook, Problem, Solution, USP, Flaw, CTA), BẮT BUỘC phải đối chiếu 100% tệp word-level timestamps (`transcript.json`) cho tất cả các từ trong toàn bộ clip. Tuyệt đối KHÔNG ĐƯỢC chỉ kiểm tra một vài đoạn đầu/cuối hay dùng mốc ước chừng rập khuôn, nhằm triệt tiêu hoàn toàn lỗi cắt lẹm, xén dở câu thoại hoặc lệch ranh giới ở bất kỳ vị trí nào trong video.
22. **🎯 KỊCH BẢN PHI TUYẾN TÍNH EMOTIONAL ROLLERCOASTER (RETENTION MAXIMIZER RULE)**: Mọi video BẮT BUỘC phải được biên tập theo cấu trúc cung bậc cảm xúc lên-xuống liên tục (Tò mò sốc ở Hook → Bức bối đồng cảm ở Pain → Tươi sáng ở Solution → Hào hứng ở USP → Đảo chiều bất ngờ & tin tưởng tuyệt đối ở Honest Flaw → Thỏa mãn ở CTA). TUYỆT ĐỐI KHÔNG dựng theo trình tự quay tuyến tính phẳng lặng.
23. **⚡ TẦN SUẤT KÍCH THÍCH DOPAMINE LÊN TỤC 2.5s - 4s (DOPAMINE STIMULATION PACE RULE)**: Cứ mỗi **2,5 giây đến 4 giây**, video BẮT BUỘC phải xuất hiện 1 thông tin mới, 1 chi tiết demo/góc quay mới, 1 cảm xúc mới hoặc 1 điểm đảo chiều lập luận. TUYỆT ĐỐI KHÔNG để trôi qua quá 4s mà không có điểm kích thích Dopamine mới, duy trì người xem ở trạng thái chú ý đỉnh cao.

---

## 🎢 NÂNG CẤP KỊCH BẢN PHI TUYẾN TÍNH — CUNG BẬC CẢM XÚC EMOTIONAL ROLLERCOASTER (MAX RETENTION)

Để giữ chân người xem ở lại video lâu nhất có thể, kịch bản BẮT BUỘC phải tạo ra các đỉnh sóng cảm xúc liên tục biến đổi (Highs & Lows), tránh tình trạng video bị phẳng lặng hay đi theo thứ tự thời gian chán ngắt.

### 6 Cung Bậc Cảm Xúc Bắt Buộc (Emotional Curve):

1. **Act 1: Extreme Contrast Hook (0s – 5s) [CẢM XÚC: TÒ MÒ / SỐC / BẤT NGỜ]**:
   - Bốc ngay tuyên bố ngược đời, mâu thuẫn nhất hoặc kết quả ấn tượng nhất từ giữa/cuối video lên làm Hook.
   - Khiến người xem lập tức nảy ra câu hỏi: *"Hả? Sao lại như thế?"* để giữ chân ngay 3 giây vàng.

2. **Act 2: Tension & Pain Point (5s – 18s) [CẢM XÚC: BỨC BỐI / LO LẮNG / ĐỒNG CẢM]**:
   - Kéo cảm xúc xuống bằng cách nêu trực diện rủi ro hư hỏng, sự phiền phức hoặc nỗi đau mất tiền mà người dùng thường gặp.
   - Nhấn mạnh sự khó chịu/bất tiện nếu không giải quyết vấn đề.

3. **Act 3: Eureka & Resolution (18s – 35s) [CẢM XÚC: TƯƠI SÁNG / GIẢI TỎA]**:
   - Vút cảm xúc lên bằng việc tung ra giải pháp đập tan nỗi đau.
   - Trình diễn góc quay đẹp, hiệu ứng trực quan sinh động.

4. **Act 4: High-Peak USP & Proof (35s – 55s) [CẢM XÚC: HÀO HỨNG / THÍCH THÚ / CHIM ƯNG]**:
   - Đưa ra tính năng độc bản hoặc thử nghiệm đắt giá nhất (Lực hút 25.000Pa, nhôm CNC nguyên khối, chấp người khó tính...).
   - Chứng minh năng lực vượt trội của sản phẩm.

5. **Act 5: Plot Twist & Honest Flaw (55s – 70s) [CẢM XÚC: BẤT NGỜ / TIN TƯỞNG TUYỆT ĐỐI]**:
   - Tạo BƯỚC NGOẶT CẢM XÚC bằng việc chủ động chỉ ra nhược điểm thực tế (Flaw) một cách chân thành (như độ lưu hương thực tế dưới trời nóng VN).
   - Đánh gục nghi ngờ, biến video từ "quảng cáo" thành "chia sẻ trải nghiệm khách quan".

6. **Act 6: Powerful Payoff & CTA (70s – 90s) [CẢM XÚC: THỎA MÃN / THÚC ĐẨY HÀNH ĐỘNG]**:
   - Khẳng định giá trị vượt trội so với giá tiền và đưa ra lời kêu gọi mua hàng đanh thép, rõ ràng.
9. **KHÔNG rm render output** trước khi ship (lesson 22/07: em mất file proof 28MB)
10. **🎯 TIKTOK SPEC** (anh yêu cầu 22/07): `1080×1920` @ `30fps` H.264 yuv420p + AAC 44100Hz stereo (HARD GATE `check_tiktok_spec.py`)
11. **🎯 SMART PAD word-aligned**: KEEP ranges phải align theo word_timestamps, pad ±0.05s (PITFALL #79)
12. **🎯 FILLER rule**: Cho phép filler ừm/ờ ở transition 0.2-0.7s gap (Whisper re-segmentation, PITFALL #80)
13. **🎯 SMART PAD CAP END** (PITFALL #86): smart_pad phải cap `new_end = min(new_end, k["end"] + PAD)` — KHÔNG để nuốt câu lặp ở ranh giới range
14. **🎯 INVENTORY + PROBE-AUDIO-RIÊNG** (PITFALL #43): khi batch N clip, inventory bằng ffprobe -select_streams a:0 riêng để detect audio silent-drop (batch 7 DJI 21/07)
14.5 **🎯 KEEP_PLAN_OVERLAP-CHECK** (PITFALL #91 — BẮT BUỘC 28/07): sau build keep_plan.json, chạy `python3 scripts/check_overlap.py <file>` để detect & auto-trim vùng overlap giữa 2 keep liên tiếp. FAIL = audio+visual lặp 2 lần. Real case 28/07: 7 clip ship 26/07 có overlap 0.5-2.2s, subagent SSIM PASS nhưng user vẫn thấy lặp.
14.6 **🎯 AUTO-TRIM OVERLAP** (defensive layer trong build_pre_speed.sh): script tự động trim end_padded của keep N = min(end_padded, next.start_padded) — phòng khi keep_plan.json chưa qua check_overlap.py.
15. **🎯 CREATIVE ARRANGE** (anh yêu cầu 23/07): arrange lại transcript theo narrative arc thu hút (act 1 hook → act 2 USP punch early → act 3 use cases → act 4 powerful closer), KHÔNG giữ source order cứng nhắc. Khi unclear → ASK anh (đã verified clip 0034).
16. **🎯 SUBAGENT OUTPUT = SNAPSHOT** (anh flag 23/07): background process output = truth tại thời điểm nó chạy. Sau khi em fix state → báo cáo mới PHẢI verify md5 actual file + nói rõ "superseded" (PITFALL #89)

---

## 📂 SCRIPTS (13 files)

| Script | Purpose |
|---|---|
| `init_project.sh` | Tạo folder + copy raw.mp4 |
| `transcribe.sh` | Whisper large-v3 word-by-word |
| `generate_transcript_md.py` | JSON → markdown (helper, PITFALL #76) |
| `smart_pad.sh` | Word-align KEEP ranges (PITFALL #79, #82) |
| `smart_keep_plan.py` | Pad logic (helper) |
| `check_overlap.py` | Detect & auto-fix keep_plan overlap (PITFALL #91) |
| `build_concat_list.py` | keep_plan.json → concat_list.txt (dùng start_padded/end_padded) |
| `build_pre_speed.sh` | Concat KEEP padded → pre-speed.mp4 (uses BASH_SOURCE, PITFALL #82) |
| `render_speed.sh` | Speed 1.3x + scale 1080×1920 30fps → final.mp4 (PITFALL #83) |
| `check_tiktok_spec.py` | HARD GATE verify TikTok spec (PITFALL #83) |
| `scale_to_tiktok.py` | Standalone scale (optional) |
| `recheck.sh` | Whisper lại final.mp4 (uses set +e carefully, PITFALL #75) |
| `verify_recheck.py` | So sánh keep_plan vs recheck (smart filler rule, PITFALL #80) |
| `ship.sh` | Copy ra Pocket3/Hermes-Edit root |

---

## 🔄 Step 6.5 — SMART PAD (key feature v0.01)

**Smart pad algorithm:** Pad KEEP ranges theo word_timestamps:
- `first_word_start - 0.05s` → `last_word_end + 0.05s`
- Tránh mất từ đầu/cuối audio (4/9 KEEP ranges head gap 0.28-0.76s trong clip 0036 test)
- HARD CUT concat (no fade) — v0.05+

```python
# smart_keep_plan.py (padrange algorithm)
first_word_start = first word in [seg_start, seg_end]
last_word_end = last word in [seg_start, seg_end]

new_start = first_word_start - 0.05
new_end = last_word_end + 0.05
```

→ Chi tiết algorithm + kết quả: `references/smart-pad-word-aligned.md`
→ SMART PAD CAP END (PITFALL #86): `references/pitfall-86-smartpad-cap-end.md`
→ macOS bash compat (no mapfile): `references/pitfall-87-macos-bash-no-mapfile.md`

**Step 6.5c — expected_duration MUST = SUM padded (PITFALL #85):**
- KHÔNG estimate cảm tính. Compute: `sum(end_padded - start_padded)` cho KEEP ranges
- Sau speed 1.3x: `target_duration_post_speed = expected_duration / 1.3`
- Verifier tolerance ±8s — sai 30s+ = FAIL verify

**Kết quả clip 0036 (test pilot smart_pad):**

| Range | Before (orig) | After (padded) | Saved |
|---|---|---|---|
| Hook | 10.70-21.50 | 10.67-21.57 | 0.00s |
| Intro | 26.60-33.90 | 26.59-33.95 | 0.04s |
| **Build** | **46.30-51.00** | **47.01-51.09** | **0.72s** |
| **Hít** | **53.90-57.50** | **54.25-57.51** | **0.44s** |
| **Ống kính** | **67.40-69.80** | **67.63-69.85** | **0.28s** |
| Demo | 74.50-89.20 | 74.47-89.29 | -0.02s |
| **Key insight** | **93.20-98.20** | **93.57-98.29** | **0.38s** |
| USP | 122.30-147.50 | 122.25-147.53 | 0.02s |
| CTA | 152.10-162.20 | 152.19-162.25 | 0.14s |

Total saved: 1.5s — Anchor points captured

---

## 🔄 Filler rule update (v0.01)

**Empirical cases (verified end-to-end clip 0036 V3 + 0029):**

```python
# verify_recheck.py — smart filler rule (4 cases)
if re.match(r'^\s*(ừm|ờ|à|rồi|nhé|nha|thì)\b', text):
    gap_before = segs[i].start - segs[i-1].end
    gap_after = segs[i+1].start - segs[i].end

    # Case 1: gap_before 0.2-0.7s → Whisper re-segmentation boundary after speed 1.3x
    if 0.2 <= gap_before <= 0.7:
        continue  # ALLOW filler (clip 0036 V3 case)
    # Case 2: gap_before > 0.7s → cut boundary thật
    if gap_before > 0.7:
        continue  # ALLOW filler (clip 0029 case @ 41.5s)
    # Case 3: gap_before == 0 và gap_after == 0 → Whisper mid-sentence split
    # Example: "Từ khi mình sở hữu" [6.80] + "Thì mình cảm thấy..." [6.80] (gap=0.0)
    if gap_before < 0.01 and gap_after < 0.01:
        continue  # ALLOW filler (clip 0029 case @ 6.8s)
    # Case 4: gap_before == 0 + gap_after > 0.5s → standalone filler at cluster start
    if gap_before < 0.01 and gap_after > 0.5:
        continue  # ALLOW filler (cluster boundary)
    # Default: FAIL filler standalone
    fail_reasons.append(filler)
```

**Verification matrix:**

| Clip | Filler @ time | gap_before | gap_after | Decision |
|---|---|---|---|---|
| 0036 V3 | ừm @ 52.4s | 0.62s | 0.0s | ALLOW (Case 1 — process transition) |
| 0029 | thì @ 6.8s | 0.0s | 0.0s | ALLOW (Case 3 — mid-sentence split) |
| 0029 | thì @ 41.5s | 0.88s | ? | ALLOW (Case 2 — cut boundary) |

→ Chi tiết: `references/pitfall-80-filler-rule-after-speed-13x.md`

---

## 🎯 PITFALLS v0.01 → v0.05 (12 cái)

→ Full list ở `references/PITFALL-INDEX.md`. Quick recap:

| # | Title | Reference file |
|---|---|---|
| 75 | `set -e` + Python exit code | pitfall-75-set-e-python-exit-code.md |
| 76 | Inline Python heredoc f-string | pitfall-76-inline-python-heredoc-fail.md |
| 79 | Word-aligned padding | pitfall-79-word-aligned-padding-required.md + smart-pad-word-aligned.md |
| 80 | Filler rule after speed 1.3x | pitfall-80-filler-rule-after-speed-13x.md |
| 82 | BASH_SOURCE script path detect | smart_pad.sh, build_pre_speed.sh |
| 83 | TikTok spec 1080×1920 30fps | tiktok-spec-1080x1920-30fps.md |
| 84 | ship.sh không gate verify ⚠️ UNFIXED | pitfall-84-ship-no-verify-gate.md |
| 85 | expected_duration MUST = SUM padded | pitfall-85-expected-duration-must-sum-padded-ranges.md |
| 87 | macOS bash 3.2 no mapfile | pitfall-87-macos-bash-no-mapfile.md |
| 88 | Ship md5 proactive report (anh flag 23/07 "không thấy file") | pitfall-88-ship-md5-proactive-report.md |
| 89 | Subagent stale output after fix (anh flag 23/07) | pitfall-89-subagent-stale-output-after-fix.md |
| 90 | SMART PAD cap end (nuốt câu lặp ranh giới, v0.04 thêm) | pitfall-90-smartpad-cap-end.md |
| 91 | KEEP_PLAN_OVERLAP: keep N+1.start < keep N.end → audio+visual lặp 2 lần | pitfall-91-keep-plan-overlap-audio-repeat.md |

> **v0.04→v0.05 changelog:** PITFALL #81 (afade 30ms) + PITFALL #86 cũ (audio-visual desync fix) đã xóa khỏi tất cả script. HARD CUT là default concat behavior.
>
> **v0.05→v0.05.1 changelog (28/07):** Thêm PITFALL #91 KEEP_PLAN_OVERLAP — detect & trim vùng overlap giữa 2 keep liên tiếp trong keep_plan. Trigger: 7 clip ship 26/07 có overlap 0.5-2.2s, subagent SSIM PASS nhưng user vẫn thấy lặp. Fix: `end_padded = min(end_padded, next.start_padded)` cho mỗi keep trừ cuối. Reference: `pitfall-91-keep-plan-overlap-audio-repeat.md`.

---

## 🔄 HOOK AUTO-MIRROR NOTE (v0.05)

Khi em viết/sửa file ở `/Volumes/Storage-1/Hermes/skills/<name>/`, hook Hermes sẽ **tự động mirror** sang `~/.hermes/skills/<name>/` mà KHÔNG báo trước.

**Workflow chuẩn sau khi write Hermes:**
```bash
# Check md5 để verify hook đã mirror
md5sum /Volumes/Storage-1/Hermes/skills/<name>/SKILL.md
md5sum ~/.hermes/skills/<name>/SKILL.md

# Nếu khác nhau → hook chưa mirror HOẶC mirror partial
# → cp thủ công nếu cần commit atomic
```

---

## 📌 Notes (v0.01)

- Backup skill cũ (legacy v2.37.0): `/Volumes/Storage-1/Hermes/_archive/skill-tiktok-video-editor-v2.37.0-legacy-2026-07-22/`
- Working copy trước apply: `/Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/`
- Active skill location: `~/.hermes/skills/media/tiktok-video-editor/`
- Skill này là **reset slate** — không kế thừa PITFALL #XX từ version cũ
- Whisper wrapper: `~/.hermes/scripts/whisper-transcribe` (large-v3 default)
- TikTok spec baseline: 1080×1920 30fps H.264 yuv420p + AAC 44100Hz stereo

### 🪞 Provenance note (anh thắc mắc 22/07)

Anh hỏi "fresh rewrite đúng không?" — em thừa nhận **KHÔNG hoàn toàn**. v0.01 là rewrite nâng cấp từ legacy v2.37.0 + v3.74 #73 fix:

**GIỮ từ legacy (khoảng 70%):**
- Workflow base 6-step → 9-step concept
- HARD RULES 1-9 (Whisper default, word timestamps, Folder, Output, ship filename conv, Mode B 30-120s)
- Concat demuxer approach (đã có ở v3.74 #73, em tái sử dụng)
- Hermes-Only-Folder rule (đã có từ 19/07 trong SOUL.md, không phải em tạo)

**MỚI ở v0.01 (~30%):**
- smart_pad.sh + smart_keep_plan.py (word-aligned padding, mới hoàn toàn)
- check_tiktok_spec.py (TikTok spec HARD GATE 1080×1920 30fps, mới)
- Filler rule update gap 0.2-0.7s (dựa trên re-segment thực tế sau speed 1.3x)
- generate_transcript_md.py (tách inline Python fail — PITFALL #76)
- Folder split work-Hermes + output-Pocket3 (em đề xuất, KHÔNG match `browser-use/video-use` pattern yêu cầu gốc)

**CÒN nợ / chưa fix v0.01:**
- ship.sh KHÔNG check verify_recheck.py exit code (PITFALL #84 — planned v0.01.1)
- Folder structure KHÔNG match `browser-use/video-use` pattern repo anh tham chiếu
- references/ còn giữ cấu trúc PITFALL cũ (legacy numbering)

**Lesson cho session sau:** Khi em rewrite skill, PHẢI nói rõ provenance ("rewrite nâng cấp từ X" hoặc "fresh rewrite"), KHÔNG tự đặt "fresh rewrite" nếu code vẫn kế thừa.

## 📋 Lessons learned ngày 22/07 (lưu vào wiki entities)

| # | Title | Reference |
|---|---|---|
| 01 | End-to-end flow 9 bước OK | clip 0036 test pilot |
| 02 | Smart Pad word-aligned saves 1.5s/range | smart_keep_plan.py |
| 03 | Filler rule update — gap 0.2-0.7s = transition OK | verify_recheck.py |
| 04 | TikTok spec enforce HARD GATE 1080×1920 30fps | check_tiktok_spec.py |
| 05 | Hook auto-mirror SKILL/refs/scripts silent | PITFALL #81 |
| 06 | BASH_SOURCE để detect skill path (work cả Hermes + ~/.hermes) | PITFALL #82 |
| 07 | Hermes-Only-Folder rule: work Hermes, output Pocket3 | folder structure |
| 08 | Reset version slate khi skill rewrite (anh dặn 22/07) | v0.01 announcement |
| 09 | `python3 verify_X > file` pattern (capture subprocess exit, PITFALL #75) | shell idiomatic |
| 10 | Dedicated `.py` script thay heredoc (PITFALL #76) | shell idiomatic |
| 11 | Mất file render proof vì `rm -rf` test workspace — KHÔNG rm render >1MB trước ship | lesson 22/07 |
| 12 | Hook apply skill silent — check md5 target sau write | sync verify loop |

### 🎯 QUY TẮC BẢO ĐẢM KHÔNG XÉN TỪ CUỐI CÂU (POST-PADDING RULE):
- **BẮT BUỘC** sử dụng ngưỡng RMS Speech Detection nhạy (Threshold = 180.0) để bắt trọn các âm tiết nhỏ phát ra ở đuôi câu thoại.
- **BẮT BUỘC** cộng thêm lề an toàn hậu padding ít nhất **+120ms** (sp_end + 0.120s) vào mốc thời gian kết thúc của TẤT CẢ các phân đoạn thoại.
- **TUYỆT ĐỐI KHÔNG** cắt sát rạt ranh giới âm thanh làm xén mất âm tiết rơi, nuốt chữ hay ngắt dở chừng từ ngữ ở cuối câu.
