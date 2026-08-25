# LEARN-FULL Protocol + 15 Hard Rule Checklist (anh command 19/07/2026)

> **Source:** clip_0006 V4→V5→V6→V7 iteration (19/07/2026)
> **Anh explicit correction (19/07):** *"Hôm qua em làm 0003_v84 được mà sao hôm nay lại không làm được, hôn qua anh đã bảo em phải learn full rồi mà"*
> **Anh explicit command (19/07):** *"Learn full và biến mọi rule thành hard rule"*

## BÀI HỌC GỐC

Em wasted 3 versions (V5: 35.3 MB, V6: 29.1 MB, V7 đầu: 39.4 MB) cho clip_0006 vì:
1. **Skip LEARN FULL** — không đọc `~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md` trước
2. **Dùng memory cũ** (memory compacted 19/07) thay vì đọc RECAP sections
3. **Patch shortcut** — fix 1 chỗ thấy fail, không apply full checklist

V7 (52.5 MB) chỉ pass 14/15 HR sau khi em LEARN FULL từ V86 RECAP (đã có sẵn trong skill) → extract 15 HR → build theo từng rule.

## PROTOCOL: 6 BƯỚC LEARN-FULL

### Step 0 — LEARN FULL (BẮT BUỘC trước mọi build)
```bash
# 1. Đọc skill tiktok-product-motion-graphics
cat ~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md | head -300

# 2. Tìm tất cả "V## RECAP" sections
grep -n "RECAP" ~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md

# 3. Đọc references key
ls ~/.hermes/skills/media/tiktok-product-motion-graphics/references/
```

### Step 1 — EXTRACT HARD RULE CHECKLIST
Từ RECAP sections, extract tất cả HARD RULE thành checklist (15 rules cho clip_0006):

| # | HARD RULE | Verify method |
|---|---|---|
| 1 | Source spec (ffprobe + 3 frames motion ≥ 10%) | `ffprobe` + `python3 PIL diff` |
| 2 | PIP timing scale theo duration tier (70-130s: chart 30%, port 60%) | Timeline math |
| 3 | **STAMP "CHÍNH HÃNG" đã BỎ** (anh flag 19/07) | grep "stamp" trong HTML |
| 4 | V85 safe zone 10% mỗi cạnh (192/108) | CSS check |
| 5 | Vùng cấm mặt y=547-1140, x=308-1526 | Pixel scan |
| 6 | 11 phase V85 (anh approved V84) | Timeline verify |
| 7 | countUp INTEGER ONLY (Math.floor) | grep `Math.floor` trong HTML |
| 8 | CTA canh giữa (transform translate) | CSS check |
| 9 | PIP structure (div.pip-wrap + video) | HTML check |
| 10 | Liquid glass opacity 0.15 | CSS check |
| 11 | HTML clean (no watermark/ANH ĐANG NÓI/caption) | grep |
| 12 | Source preservation (full_bg no audio) | ffprobe |
| 13 | BG video play (videos.pause + tl.seek(0)) | HTML check |
| 14 | ffmpeg ghép audio cuối (KHÔNG overlay) | Bash script |
| 15 | Verify trước khi ship (5 check items) | Final gate |

### Step 2 — VERIFY SOURCE
```bash
# Check source spec
ffprobe -v error -show_entries format=duration,bit_rate:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 source.mp4

# Sample 3 frames motion
for t in 1 50 95; do
  ffmpeg -y -ss $t -i source.mp4 -frames:v 1 -vf "scale=420:-1" /tmp/check_t${t}.jpg
done
# Check motion ≥ 10% per transition
```

### Step 3 — BUILD HTML (theo checklist từng rule một)
ĐỪNG patch shortcut. Mỗi rule cần verify trước khi move sang rule tiếp theo.

### Step 4 — VERIFY TỪNG RULE
```bash
# Rule #1: Source spec check
# Rule #2: PIP timing math
# Rule #3: grep "stamp" HTML
# Rule #4-5: CSS extract + pixel scan
# Rule #6: Timeline scale
# Rule #7: grep Math.floor
# Rule #8: CSS transform check
# Rule #9: HTML structure check
# Rule #10: opacity CSS check
# Rule #11: grep ANH ĐANG NÓI/watermark
# Rule #12: ffprobe no audio
# Rule #13: JS check
# Rule #14: ffmpeg command verify
# Rule #15: Final 5-evidence gate
```

### Step 5 — SHIP
```bash
# ghép audio cuối
ffmpeg -y -i output_silent.mp4 -i audio.aac \
  -c:v copy -c:a aac -b:a 128k -shortest \
  -movflags +faststart \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<id>_V<n>_FINAL_<desc>.mp4
```

### Step 6 — PATCH SKILL với version mới
Mỗi iteration thành công → thêm V## RECAP section vào skill để:
- Document hard rule mới
- Note 1 line: "Apply 14/15 HR checklist" hoặc "Apply N/N HR"
- Reference file path

## ANTI-PATTERN (em đã fail thực tế)

| Anti-pattern | Result | Fix |
|---|---|---|
| Build V5 trước khi đọc V86 RECAP | 35.3 MB fail (STAMP bỏ OK nhưng PIP blank) | Đọc skill TRƯỚC |
| Dùng memory cũ (compacted) thay vì RECAP | Build sai vì memory đã bị nén | RECAP sections là knowledge base |
| Patch shortcut (fix 1 chỗ thấy fail) | 3 versions wasted | Apply full checklist |
| Không verify motion per transition | Ship clip PIP blank | PIL pixel diff ≥ 10% |

## REAL CASE: clip_0006 (19/07/2026)

| Version | HR pass | Note |
|---|---|---|
| V4 (39.4 MB) | 12/15 | Build trước, miss 3 rule |
| V5 (35.3 MB) | 13/15 | STAMP bỏ, miss PIP |
| V6 (29.1 MB) | 13/15 | Timeline fix, miss PIP |
| **V7 (52.5 MB)** | **14/15** | LEARN FULL → V86 RECAP → 15 HR checklist |

**Lesson vĩnh viễn:** Apply LEARN-FULL protocol trước mọi build, không bao giờ patch shortcut.

## REFERENCES

- Skill: `~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md` (đã có V78→V87 RECAP)
- Pitfall details: `references/hyperframes-pip-video-limitation-2026-07-19.md`
- Real case analysis: `wiki/entities/learned-about-tuananh.md` (search "V7 RECAP")
