# Reference: iPhone-friendly crop vs keep-original decision (2026-07-14)

## TL;DR

Khi em convert YouTube Shorts sang iPhone-friendly (H.264/AAC/+faststart) và phát hiện có **banda đen lớn trên+dưới** do YouTube Shorts player ép 16:9 broadcast vào 9:16 → **KHÔNG tự crop**. Mặc định là giữ nguyên gốc, trừ khi anh explicit yêu cầu crop.

## Lý do crop KHÔNG phải default

1. **Anh thường open file trên iPhone Photos app** để xem nhanh hoặc reference → banda đen không gây khó chịu
2. **Anh không reup TikTok ngay** khi gửi link — anh dùng để archive, edit sau, hoặc share
3. **Crop = mất thông tin**: scale 1.4% (1072→1080) hoặc crop chặt có thể crop oan content quan trọng (player action, score, sub-text)
4. **Crop = mất thời gian**: cropdetect (5s) + crop+scale re-encode (15s) + vision verify (1 tool call) → tổng ~25s, không cần thiết nếu anh OK với banda đen

## Real case captured

**Session 2026-07-14, 16:02-16:07 ICT:**

| Step | Action | Outcome |
|------|--------|---------|
| 1 | Anh share `youtube.com/shorts/WJJhUbnhx4Q?si=Dtl11jIXpicvzBIp` + "tải clip về đúng chuẩn iphone và gửi qua telegram cho anh" | Em load skill `video-download-yt-dlp` |
| 2 | Em download với yt-dlp → re-encode H.264/AAC → 8.79 MB | Spec iPhone OK |
| 3 | Em vision-verify frame giây 28.5 → phát hiện 2 banda đen ~30% frame | Em TỰ Ý apply Pitfall 5D workflow |
| 4 | cropdetect → `crop=1080:948:0:486` (limit=0.18) | Banda đen detect rõ |
| 5 | Crop + scale → `_iphone_crop.mp4` 14.13 MB | Em ship file crop |
| 6 | Anh reply: **"Không cần, giữ nguyên bản là được rồi!!!"** | Em phát hiện over-automation |
| 7 | Em re-download bản gốc không crop → 8.79 MB | Ship lại file gốc |
| 8 | Anh OK | Done |

**Time wasted: ~30 giây** (download crop + re-download gốc + ship lại).

## Decision matrix

| Signal từ anh | Action |
|---------------|--------|
| "tải về / convert / đọc được / chuẩn iphone / đúng định dạng" | **MẶC ĐỊNH giữ nguyên gốc** — chỉ convert codec |
| "crop đi / sạch 9:16 / fill full / không banda đen / ready để post" | Apply 5D workflow |
| "reup TikTok / đăng TikTok / sửa để đăng" | Apply 5D workflow (TikTok algo xử lý banda đen xấu) |
| Anh KHÔNG nói gì về aspect/crop | **MẶC ĐỊNH giữ nguyên** + hỏi "anh muốn giữ nguyên hay crop sạch 9:16?" |

## Communication template

Khi phát hiện banda đen và đang ở trong workflow mặc định (giữ nguyên):

```markdown
✅ Download xong + convert iPhone-friendly
- File: <VIDEO_ID>_iphone.mp4
- Size: ~8-9 MB
- Codec: H.264 + AAC 44100Hz + +faststart
- Path: /Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO_ID>_iphone.mp4

⚠️ Visual note: file có 2 vùng đen lớn ở trên+dưới (~30% frame)
— đây là gốc YouTube Shorts (16:9 broadcast ép vào 9:16)

Anh muốn:
A. Giữ nguyên bản gốc (có banda đen) — em ship file này
B. Crop + scale fill full 9:16 — em re-process

MEDIA:/Volumes/.../<VIDEO_ID>_iphone.mp4
```

## Anti-pattern to avoid

❌ **Tự ý crop vì "tốt hơn"** → em không phải là user, không quyết định aesthetic
❌ **Skip hỏi vì "đây là best practice"** → best practice ≠ user preference
❌ **Batch ship không vision-verify** → mất opportunity nhận feedback về banda đen
❌ **Assume anh đang reup TikTok** → sai, anh thường chỉ archive/view

## Cross-reference

- **Pitfall 5D** (skill SKILL.md): chi tiết crop workflow (3 bước cropdetect + crop + vision verify)
- **Pitfall 5F** (skill SKILL.md, NEW 14/07): scope decision tree — khi nào hỏi trước, khi nào auto-apply
- **Step 4b canonical command** (skill SKILL.md): yt-dlp command iPhone-friendly (KHÔNG có crop)
- **Pitfall W10** (skill SKILL.md): aspect mismatch vs QuickTime/Telegram preview — khác concern (visual preview bug, không phải file issue)