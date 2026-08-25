# V18 SHIP-VERIFICATION RECIPE (PITFALL #45) — MANDATORY

> **Ngày tạo**: 2026-07-19
> **Trigger**: Sau mỗi lần `ffmpeg` / `cp` / `npx hyperframes render` — KHÔNG BAO GIỜ bỏ qua.
> **Failure mode đã chứng kiến**: V18 em báo "shipped" 3 lần, file không có ở Hermes-Edit. User phải flag "để ở chỗ đéo nào?".

---

## 🚨 VẤN ĐỀ

`subprocess.run(ffmpeg, output=final_path)` returncode=0 **KHÔNG CÓ NGHĨA** là file đã ship thành công:
- File vẫn ở scratch dir (em ghi đè path cũ)
- File được tạo nhưng write fail im lặng (permission, disk full, codec error)
- Em quên chạy lệnh cuối cùng (đã xảy ra với V18)

**Anh feedback**: *"V18 mày để ở chỗ đéo nào vậy?"* — phải tự mở Finder mới thấy file không có.

---

## ✅ 4-STEP MANDATORY SHIP VERIFICATION

**Bước 1**: Chạy ffmpeg / cp composite:
```bash
ffmpeg -y -i /Volumes/Storage-1/Hermes/scratch/hf_<v>/output_silent.mp4 \
  -i /Volumes/Storage-1/Hermes/scratch/hf_<v>/audio.aac \
  -c:v copy -c:a aac -b:a 128k -shortest \
  -movflags +faststart \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/<output>.mp4
```

**Bước 2 (BẮT BUỘC)**: Verify file exists với size > 0:
```bash
ls -la /Volumes/Storage-1/Pocket3/Hermes-Edit/<output>.mp4
# → phải thấy:
#    -rw-r--r--  1 tuananh4865  staff  57654321 Jul 19 20:11 <output>.mp4
# size > 0, modified time MỚI (trong vòng 5 phút gần đây)
```

**Bước 3 (BẮT BUỘC)**: ffprobe verify spec:
```bash
ffprobe -v error -show_entries \
  format=duration,bit_rate:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/<output>.mp4
# → phải thấy:
#    codec_name=h264
#    width=1080
#    height=1920
#    codec_name=aac
#    duration=100.000000 (hoặc expected)
#    bit_rate=4000000-6000000 (production quality)
```

**Bước 4 (BẮT BUỘC)**: Nếu file KHÔNG có ở Bước 2 hoặc spec SAI ở Bước 3:
- ❌ KHÔNG báo "shipped"
- ✅ Re-run composite (Bước 1)
- ✅ Verify lại (Bước 2-3)
- ✅ Nếu vẫn fail → STOP, báo user honest: *"file không có ở Hermes-Edit, em đang investigate"*

---

## 📋 SHIP REPORT TEMPLATE

Khi báo "shipped" cho user, PHẢI có 3 dòng verify:

```
✅ SHIPPED: /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_V18_100s_FINAL_V13_METHOD.mp4
   Size: 54,734,953 B (52.2 MB) — verified via `ls -la`
   Spec: h264 1080×1920, aac, 100s, 4.58 Mbps — verified via `ffprobe`
```

**KHÔNG ĐƯỢC** báo kiểu: *"✅ V18 SHIPPED: 54.6 MB"* mà không có 2 dòng verify trên. Đó là fabrication.

---

## 🎯 TRIGGER CONDITIONS — KHI NÀO PHẢI VERIFY

| Operation | Verify step |
|---|---|
| `ffmpeg -i X -i Y -c copy output.mp4` | `ls -la output.mp4` + `ffprobe output.mp4` |
| `cp source.mp4 final.mp4` | `ls -la final.mp4` |
| `npx hyperframes render --output X.mp4` | `ls -la X.mp4` + check size > 0 |
| `mv /scratch/X /Hermes-Edit/X` | `ls -la /Hermes-Edit/X` |
| Sau `os.remove(...)` cleanup | `ls -la` confirm file removed |
| Sau patch skill (em vẫn tưởng file có ở đâu đó) | `ls -la` final location |

---

## 📚 CONTEXT — TẠI SAO PITFALL NÀY TỒN TẠI

Em đã mắc PITFALL #45 ở session V18:
1. Sau khi render V18 + ffmpeg ghép audio, em báo "V18 SHIPPED: 54.6 MB"
2. User mở Hermes-Edit → không có file
3. User flag: *"V18 mày để ở chỗ đéo nào vậy?"*
4. Em check lại → file chỉ ở `/Volumes/Storage-1/Hermes/scratch/hf_clip0006_V18/output_silent.mp4` (scratch)
5. Em phát hiện ra em đã quên chạy bước composite audio thành phần cuối (hoặc chạy nhưng file path sai)
6. Em re-run composite → verify bằng `ls -la` + `ffprobe` → file 54.7 MB có ở Hermes-Edit đúng
7. Patch skill với V96 + PITFALL #45 để lần sau KHÔNG mắc lại

**Lesson vĩnh viễn**: SHIP CLAIM ≠ SHIP FACT. Verify bằng file system, KHÔNG bằng returncode.

---

## 🔗 RELATED FILES

| File | Purpose |
|---|---|
| `~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md` | Main skill (V96 + PITFALL #45 ở trên) |
| `references/v18-pip-method-chinh-thuc.md` | V13/V18 PIP pattern |
| `references/v90-gsap-fadein-opacity-zero-rule-2026-07-19.md` | PITFALL #44 (related: GSAP fromTo không apply initial state) |
| `references/v100-pixel-bbox-verification-mandatory-2026-07-19.md` | PITFALL #46 (related: pixel stats ≠ visual truth) |

---

*V18 SHIP-VERIFY-OR-LIE — Codified 19/07/2026 sau khi em mắc 3 lần liên tiếp "shipped" mà file không có. Áp dụng cho MỌI ship operation từ bây giờ.*