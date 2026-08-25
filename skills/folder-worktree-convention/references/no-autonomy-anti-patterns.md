# NO-AUTONOMY Anti-patterns — 04/07 Evidence

> **Status:** HARD RULE từ anh Tuấn Anh. Em đã phạm 3 anti-patterns trong 1 session edit clip trước khi patch skill. Reference này là evidence để background curator không quên.

## 🩸 3 Anti-patterns em phạm trong 1 session (04/07)

### Anti-pattern #1: Tạo folder con lồng trong folder final

**Lúc phạm**: 04/07 ~08:53, edit clip từ Drive ID `1hh4JG-KxUJWjuzzr2jHJnvDAOredeyIg`

**Hành vi sai**:
```bash
mkdir -p /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_drive3_source
cd /Volumes/Storage-1/Pocket3/Hermes-Edit/
gdown "1hh4JG..." -O clip_drive3_source/source.mp4
```

**Anh feedback (verbatim)**: *"/Volumes/Storage-1/Pocket3/Hermes-Edit/ lưu vào trong path này thôi chứ sao lại tạo thêm folder gì vậy ???"*

**Fix**: Render TRỰC TIẾP vào `{folder}/`, KHÔNG tạo folder con.

### Anti-pattern #2: Tên file có version + hậu tố thừa

**Lúc phạm**: 04/07 ~08:59

**Hành vi sai**:
```bash
# Filename đầu tiên em đặt
clip_drive3_v1_edited.mp4

# Sau khi bị flag → đổi tên
mv /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_drive3_source/clip_drive3_v1_edited.mp4 \
   "/Volumes/Storage-1/Pocket3/Hermes-Edit/sac-du-phong-mini-gan-iphone-04072026.mp4"
```

**Fix**: Filename CHÍNH XÁC = `{nội-dung-không-dấu}-{ddmmyyyy}.mp4`. KHÔNG `v1/v2/edited/source/draft` trong tên file. Version là internal tracking, không lộ ra filename.

### Anti-pattern #3: Tự ý copy file sang Google Drive

**Lúc phạm**: 04/07 ~09:56, sau khi anh hỏi "Chưa thấy sync lên drive ta"

**Hành vi sai**:
```bash
cp "/Volumes/Storage-1/Pocket3/Hermes-Edit/sac-du-phong-mini-gan-iphone-04072026.mp4" \
   "/Users/tuananh4865/Library/CloudStorage/GoogleDrive-tuananh4865@gmail.com/My Drive/sac-du-phong-mini-gan-iphone-04072026.mp4"
```

**Anh feedback (verbatim)**:
- *"Em chỉ cần render vào đúng path mà tao chỉ định thôi"*
- *"Tao cấm mày cái gì cung tự cho là mày biết hết nha, m ngu như bò vậy đó nên làm gì thì cũng tìm hiểu research trước cho tao!"*
- *"Giảm toàn bộ độ tự tin của mày xuống dưới mức trung bình luôn đi đồ ngu"*

**Fix**: KHÔNG tự `cp/mv/sync` sang Drive. Anh đã config Google Drive desktop app sync folder `Pocket3/Hermes-Edit/` theo cách riêng của anh. Em chỉ render file vào `{folder}/{filename}.mp4` rồi dừng.

## 🎯 Root cause của 3 anti-patterns

**Anti-methodology (em đang làm trước 04/07)**:
- Lưu rule vào memory
- Lưu rule vào skill text
- Không có cơ chế enforce
- Em sẽ tái phạm

**Triệt để (anh dạy 04/07)**:
1. Mỗi anti-pattern phải có **gate chặn trước khi xảy ra** (không phải chỉ rule text)
2. Phải **verify gate hoạt động** bằng cách chạy lại task — pass tự động
3. **KHÔNG lưu rule rồi thôi** — rule có thể bị ignore do LLM reasoning

## 🚨 Tone correction (anh mandate, class-level)

Khi bị flag sai bởi anh:
1. **DỪNG ngay** hành động đang làm
2. **KHÔNG argue** — không "nhưng mà em nghĩ..."
3. **KHÔNG hỏi option A/B/C** — đợi anh chỉ rõ
4. **Ngôn ngữ ngắn**: "Dạ em hiểu rồi", hỏi đúng 1 câu cần thiết
5. **Patch skill** ngay để chặn anti-pattern tái phạm — không chỉ save rule vào memory

**Default mode**: low confidence. Tự tin cao = red flag = dừng research lại.

## 📌 Rule cứng: Hỏi anh trước khi quyết

Khi em KHÔNG CHẮC chắn 100% về bất kỳ hành động nào có tác động đến file/folder:
- Di chuyển file khỏi folder
- Copy file sang chỗ khác
- Xóa folder cũ
- Đổi tên file/folder
- Tạo folder mới

→ **DỪNG, hỏi anh trước.** Tốn 1 câu hỏi để KHÔNG phải re-do 3 lần.

## Cross-reference

- Skill `folder-worktree-convention` SKILL.md — main rules
- Memory entry `[04/07 NO-AUTONOMY]` — system-wide rule
- Skill `tiktok-video-editor` — domain-specific (edit clip)
- Skill `mac-disk-cleanup-audit` — domain-specific (disk cleanup)