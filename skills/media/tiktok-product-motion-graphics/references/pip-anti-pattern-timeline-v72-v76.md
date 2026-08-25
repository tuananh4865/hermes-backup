---
title: PIP Anti-Pattern Timeline V72→V76 (Session 2026-07-18)
created: 2026-07-18
type: reference
tags: [pip, anti-pattern, timeline, session-specific, v72-v76, hyperframes, ffmpeg]
---

# PIP Anti-Pattern Timeline: V72 → V76 (2026-07-18)

> **Purpose:** Document 5 failed iterations in ONE session so future agents don't repeat the same mistakes. Session-specific detail — not the canonical recipe (see `v76-pip-4-layer-ffmpeg-recipe.md` for that).

## Tại sao file này tồn tại

Trong 1 phiên ngày 2026-07-18, em đã làm sai clip_0003 (Dodoto Lux Air V3) **5 lần liên tiếp** về PIP. Anh phải sửa 5 lần. Đây là timeline để agent sau biết tại sao MỖI version sai + version nào work cuối cùng.

## Timeline (chronological)

### V72 — `<video>` element cho PIP, nền đen

```html
<video class="pip-vid" data-start="30" muted playsinline preload="auto">
  <source src="assets/source/pip_pip_chart.mp4" />
</video>
```

```bash
# ffmpeg extract PIP
ffmpeg -vf "crop=ih*9/16:ih:0:0,scale=420:750"
```

**Lỗi của V72:**
- Dùng `<video>` element → HyperFrames KHÔNG play HTML video trong headless Chrome → render 1 frame tĩnh
- Crop `crop=ih*9/16:ih:0:0` trên source 1080×1920 = 607×720 từ Y=0 → chỉ lấy vùng background đen phía trên, MẶT ANH bị crop mất
- PIP 420×750 portrait sai format TikTok dọc

**Anh feedback:** "Pip vẫn là ảnh tĩnh không phải video thu nhỏ lại vào pip đó nền vẫn là video full chứ không phải nền đen như anh yêu cầu"

---

### V73 — Fix crop nhưng vẫn `<video>` element

```bash
ffmpeg -vf "crop=1080:1080:0:540,scale=420:420"  # đúng crop
```

**Lỗi của V73:**
- Crop đúng (vuông 1080×1080 từ Y=540, scale 420×420)
- VẪN dùng `<video>` element → vẫn 1 frame tĩnh
- Nền vẫn video source lộ ra vì `format=yuva420p` overlay

**Anh feedback:** vẫn sai, không có motion.

---

### V74 — Đổi sang `<img>` PNG tĩnh + `.pip-wrap { background: #000 }`

```bash
ffmpeg -ss 32 -i source.mp4 -frames:v 1 -vf "crop=1080:1080:0:540,scale=420:420" pip_chart.png
```

```html
<img src="assets/source/pip_chart.png" alt="Dodoto Lux Air V3" />
```

```css
.pip-wrap { background: #000; }  /* NỀN ĐEN RÕ RÀNG */
```

**Lỗi của V74:**
- PIP = ảnh tĩnh PNG → không motion
- Nền đen TOÀN CLIP → sai ý anh (anh chỉ muốn nền đen ở vùng PIP)
- 3 ảnh PNG tĩnh thay vì video

**Anh feedback:** "Pip vẫn hiện nền là video chứ không phải nền đen, pip lại chỉ xuất hiện ảnh tỉnh hoặc đôi khi là một khung trống không có gì - pip phải là crop scale down của video mới đúng"

---

### V75 — Extract PIP mp4 + 3-layer ffmpeg, nền = video full

```bash
ffmpeg -y -i full_bg.mp4 -i pip_chart.mp4 -i pip_usp.mp4 -i pip_final.mp4 -i output_silent.mov \
  -filter_complex "[bg][glass]overlay=0:0[base]; [base][pip1]overlay=80:80[v1]; [v1][pip2]overlay=80:80[v2]; [v2][pip3]overlay=80:80[v]"
```

**Lỗi của V75:**
- PIP mp4 đúng (motion thật)
- 3-layer ffmpeg đúng
- **NHƯNG nền = source video full 1080×1920 TOÀN CLIP** → đoạn PIP có nền video thay vì nền đen
- Em hiểu sai câu "nền vẫn là video" là nền video toàn clip, nhưng thực ra anh muốn nền video NGOÀI PIP + nền đen TRONG PIP

**Anh feedback:** "Trời ơi chỉ pip ở đoạn cần chèn chart hoặc có nhiều thông tin cần làm motion graphic thôi! Nền ở những đoạn pip là nền đen pip là video crop em đang làm đúng rồi nhưng nền phải là nền đen để show thông tin cho rõ!!!!"

---

### V76 — 4-layer ffmpeg + black_420x420 riêng dưới PIP ✅

```bash
ffmpeg -y \
  -i full_bg.mp4 \
  -i black_420x420.mp4 \      # LAVFI color=black:s=420x420
  -i pip_chart.mp4 -i pip_usp.mp4 -i pip_final.mp4 \
  -i output_silent.mov \
  -filter_complex "
    [bg][glass]overlay=0:0[base];
    [base][black]overlay=80:80[b1];
    [b1][pip1]overlay=80:80[v1];
    [v1][black]overlay=80:80[b2];
    [b2][pip2]overlay=80:80[v2];
    [v2][black]overlay=80:80[b3];
    [b3][pip3]overlay=80:80[v]
  "
```

**Đúng của V76:**
- PIP mp4 (motion thật) — đúng từ V75
- 4-layer ffmpeg — thêm 1 layer black_420x420 riêng cho vùng PIP
- Nền NGOÀI PIP = video full (V75 đúng phần này)
- Nền TRONG PIP = đen (anh muốn)
- PIP mp4 extract ĐÚNG timestamp phase (24-37 cho CHART, 37-52 cho USP, 55-72 cho CTA-TEST)
- Chain 3 lần black+pip vì mỗi phase PIP cần reset base

**Verified:** `clip0003_V76_82s_FINAL_PIP_BLACK_BG.mp4` (71.1 MB, 81.76s, 6,819 Kbps)

**Hạn chế còn lại:** Source clip talking head gần static → face tones tràn vào vùng PIP (avg ~95-97 thay vì <30). Anh nói "play bình thường" nên motion source thật ra có nhưng yếu.

---

## Tổng kết 5 bài học

| # | Bài học | Version đã sai |
|---|---|---|
| 1 | HyperFrames KHÔNG play HTML `<video>` trong headless | V72, V73 |
| 2 | PIP không được dùng `<img>` tĩnh nếu cần motion | V74 |
| 3 | Nền PIP không phải nền toàn clip — chỉ vùng PIP cần đen | V74, V75 |
| 4 | Crop source 1080×1920 phải dùng `crop=1080:1080:0:540` (vuông từ Y=540) | V72 |
| 5 | PIP mp4 phải cùng timestamp audio đoạn đó, không ghép đoạn khác vào | V72-V75 (chưa sai vì chưa có PIP mp4) |

## Tại sao em hiểu sai

**V75 → V76 confusion:** Em hiểu "nền vẫn là video full" là nền video toàn clip. Thực ra anh muốn:
- NGOÀI vùng PIP (đoạn HOOK/INTRO/USP/CTA-TEST): nền = video full
- TRONG vùng PIP (đoạn CHART/USP/FINAL): nền = đen

Câu "nền vẫn là video" ám chỉ "nền NGOÀI PIP vẫn là video, không phải nền đen toàn clip". Em hiểu sai câu này trong V75.

## Liên quan

- **Canonical recipe:** `references/v76-pip-4-layer-ffmpeg-recipe.md`
- **V75 superseded:** `references/v75-pip-video-3-layer-ffmpeg-pattern.md` (V76 supersede V75)
- **HyperFrames headless pitfall:** `references/motion-static-video-pitfall.md` (cũng cover `<video>` issue)
- **V74 superseded:** KHÔNG CÒN reference cho V74 PNG tĩnh (sai hoàn toàn)
