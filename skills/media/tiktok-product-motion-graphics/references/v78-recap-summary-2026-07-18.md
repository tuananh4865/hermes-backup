# V78 FRESH-FROM-SOURCE WORKFLOW — QUICK REFERENCE (18/07/2026)

> **Khi dùng:** V_n motion verify fail (<10% pixels/10s) hoặc chain-edit ≥3 version mà vẫn không fix được → fresh-from-source.

## SHIPPED

| Field | Value |
|---|---|
| File | `clip0003_V78_82s_FINAL_with_audio.mp4` |
| Size | **41.9 MB** |
| Duration | 82.000s |
| Codec | H.264 1080×1920, AAC 44100Hz |
| Bit rate | **4.29 Mbps** |
| Motion | **33.05% / 32.95% / 32.41%** pixels changed @ 0-25s / 25-55s / 55-80s |

## 5 BƯỚC (đã PASS)

1. **Copy source gốc** (KHÔNG speed 1.3x):
   ```bash
   ffmpeg -y -i source_goc.mp4 -an -c:v copy assets/source/full_bg.mp4
   ```

2. **Extract 3 PIP** từ source gốc tại đúng timestamp phase:
   ```bash
   ffmpeg -ss 24 -t 13 -i source_goc.mp4 -vf "crop=1080:1080:0:540,scale=420:420" \
          -an -c:v libx264 -preset fast -crf 23 assets/source/pip/pip_chart.mp4
   ffmpeg -ss 37 -t 15 -i source_goc.mp4 -vf "crop=1080:1080:0:540,scale=420:420" \
          -an -c:v libx264 -preset fast -crf 23 assets/source/pip/pip_usp.mp4
   ffmpeg -ss 55 -t 17 -i source_goc.mp4 -vf "crop=1080:1080:0:540,scale=420:420" \
          -an -c:v libx264 -preset fast -crf 23 assets/source/pip/pip_final.mp4
   ```

3. **HTML composition** — 4 video elements direct child of root (xem `references/v78-fresh-from-source-workflow-2026-07-18.md` cho full HTML)

4. **GSAP timeline** register + pause videos (KHÔNG `currentTime = 0`):
   ```js
   window.__timelines["clip0003-V78"] = gsap.timeline({ paused: true });
   document.querySelectorAll('video').forEach(v => v.pause());
   ```

5. **Render silent + ffmpeg ghép audio cuối**:
   ```bash
   npx hyperframes render --quality draft --output output_silent.mp4
   ffmpeg -i output_silent.mp4 -i audio.aac -c:v copy -c:a aac -shortest FINAL.mp4
   ```

## DECISION RULE

| V_n motion output | Action |
|---|---|
| <10% / 10s | **FRESH FROM SOURCE** (chain-edit fail) |
| 10-25% / 10s | Consider fresh-from-source (50/50) |
| ≥25% / 10s | Chain-edit OK |

## EM ĐÃ SAI 18/07 (LỖI CẦN TRÁNH)

1. **Báo source clip 0003 "static 100%"** — thực tế source motion 30.86%/5s
2. **Dùng `motion_diff_check.py` chỉ check top-left** — source talking head ở giữa khung → miss motion
3. **Chain-edit V72→V77 qua 6 version** — mỗi version patch 1 thứ, motion quality giảm dần

## MULTI-REGION MOTION VERIFY (FULL RECIPE)

Xem `references/v78-fresh-from-source-workflow-2026-07-18.md` section "Lesson vĩnh viễn: Multi-Region Motion Verify" cho full Python code sample 5 vùng (face_mouth, face_chin, hand_mic, bg_top, bg_bottom) + threshold rule.

## ANTI-PATTERNS (đã fail 4 lần liên tiếp V72-V76)

- ❌ Patch V_n HTML để fix motion → chain-edit tippler, motion vẫn yếu
- ❌ Dùng `<video>` element trong HyperFrames index.html → KHÔNG play → render 1 frame tĩnh
- ❌ Extract PIP mp4 riêng + overlay qua ffmpeg `format=yuva420p` → motion freeze
- ❌ Dùng `currentTime = 0` thay vì `pause()` → HyperFrames không seek đúng frame
- ❌ Chỉ extract 1 PIP rồi reuse cho 3 phase → sai timing audio
- ❌ Dùng `motion_diff_check.py` chỉ check 1 vùng → kết luận sai "static"

## CROSS-REFERENCE

- **Master SKILL.md section**: `## 🟢 V78 FRESH-FROM-SOURCE WORKFLOW (VERIFIED 18/07/2026)` — chỉ ngắn gọn, link tới file này
- **Full forensic + Python code**: `references/v78-fresh-from-source-workflow-2026-07-18.md` (đã ghi 18/07)
- **Wiki entity**: `/Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md` — section `[2026-07-18] V78 RECAP — Làm lại từ source gốc`
- **Wiki log**: `/Volumes/Storage-1/Hermes/wiki/log.md` — entry 18/07 13:xx session V78