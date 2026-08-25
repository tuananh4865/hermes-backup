# Folder Cleanup Protocol — Khi gặp folder cũ trong folder làm việc

> **Status:** Protocol BẮT BUỘC trước khi động vào bất kỳ folder cũ nào. Em đã phạm sai 04/07 → patch skill để chặn tái phạm.

## 🎯 Vấn đề

Folder em đang làm việc có thể chứa **folder/file cũ** từ session trước (transcripts/, sources/, clips cũ, audio extract, etc.). Em KHÔNG ĐƯỢC tự ý xóa — phải hỏi anh trước.

## 📋 Protocol 5 bước

### Step 1: Scan folder chính, identify candidates

```bash
FOLDER="/Volumes/Storage-1/Pocket3/Hermes-Edit"  # hoặc folder bất kỳ

# List tất cả non-standard items
ls -la "$FOLDER/" | grep -vE "\.mp4$|\.DS_Store|^\.|\.\.$|tmp$"

# Identify:
# - Folder không phải tmp/ và KHÔNG phải file final (vd: sources/, transcripts/, chunks*/)
# - File audio/image/json KHÔNG phải .mp4
# - File backup/archive cũ
```

### Step 2: Phân loại candidates

**Mục tiêu**: gom nhóm candidates thành các batch để hỏi anh 1 lần, không hỏi nhiều lần.

```markdown
## Candidates để cleanup trong {folder}:

**Folder cũ** (chiếm N MB):
- sources/ — 2.2GB chứa source MP4 của clip edit trước
- transcripts/ — 129MB transcript Whisper cũ theo ngày
- chunks30june/ — 58MB audio chunks từ session 30/06

**File cũ không phải clip final**:
- clip_raw.mov — 1GB raw video DJI
- clip_drive2_audio.wav — 5.4MB audio extract cũ
- first_frame.jpg, frame_*.jpg — 0.5MB frame test

**File clip cũ** (KHÔNG phải clip hôm nay):
- clip2_edited_*.mp4, clip3_edited_*.mp4, clip_drive2_v*.mp4 — ~3GB các version edit cũ
```

### Step 3: Hỏi anh với 3-4 options (clarify tool)

Khi candidates KHÔNG chắc chắn an toàn → hỏi anh với options:

```
Q: Em thấy N candidates cũ trong {folder}. Xử lý sao anh?

Options:
1. Move vào tmp/legacy-{name}/ (an toàn nhất, giữ nguyên data)
2. Xóa luôn (anh chịu trách nhiệm nếu cần lại)
3. Giữ nguyên (folder cũ, không động)
4. Move vào tmp/ chỉ phần nhỏ (transcripts), giữ nguyên phần lớn (sources)
```

### Step 4: Execute theo option anh chọn

```bash
# Option 1: Move an toàn
mkdir -p "$FOLDER/tmp/legacy-sources-2026-07-04"
mv "$FOLDER/sources" "$FOLDER/tmp/legacy-sources-2026-07-04/"

# Option 2: Xóa (chỉ khi anh explicit)
rm -rf "$FOLDER/sources"

# Option 3: Không làm gì
echo "Anh chọn giữ nguyên, không động"
```

### Step 5: Verify + report

```bash
# Verify move/xóa OK
ls -la "$FOLDER/" | head -10
ls "$FOLDER/tmp/" | head -10

# Report cho anh
echo "✅ Đã move sources/ → tmp/legacy-sources-2026-07-04/ (2.2GB)"
echo "✅ Folder giờ chỉ còn: {final files} + tmp/"
```

## 🚨 Anti-patterns cần tránh

### Anti-pattern #1: Tự xóa folder cũ không hỏi
```bash
# ❌ SAI
rm -rf /Volumes/Storage-1/Pocket3/Hermes-Edit/sources/
```

**Consequence**: Mất data khi cần lại. Trust damage với anh.

### Anti-pattern #2: Tự move mà không confirm destination
```bash
# ❌ SAI - move ra ngoài folder root (vd ~/Desktop/..)
mv sources ~/Desktop/old-sources/
# → anh không thấy file, khó tìm lại
```

**Consequence**: Folder bị phân tán, khó quản lý.

### Anti-pattern #3: Move nhưng rename lung tung
```bash
# ❌ SAI - rename thành tên mới
mv sources old_stuff_backup_v2_dont_delete
# → khó tìm, không nhất quán với convention tmp/legacy-*/
```

**Consequence**: Naming không nhất quán, khó grep/automate sau này.

### Anti-pattern #4: Move NHIỀU folder cũ vào 1 tmp/legacy-*/ chung
```bash
# ❌ SAI
mkdir -p tmp/legacy-old-stuff
mv sources tmp/legacy-old-stuff/
mv transcripts tmp/legacy-old-stuff/
mv chunks30june tmp/legacy-old-stuff/
mv clip_raw.mov tmp/legacy-old-stuff/
# → 1 folder chứa 4GB lẫn lộn, khó debug từng phần
```

**Fix**: Mỗi folder/file cũ → 1 folder `tmp/legacy-{name}-{ngày}/` riêng.

```bash
# ✅ ĐÚNG
mkdir -p tmp/legacy-sources-2026-07-04
mv sources tmp/legacy-sources-2026-07-04/
mkdir -p tmp/legacy-transcripts-2026-07-04
mv transcripts tmp/legacy-transcripts-2026-07-04/
mkdir -p tmp/legacy-chunks30june-2026-07-04
mv chunks30june tmp/legacy-chunks30june-2026-07-04/
```

## 🔄 Khi nào KHÔNG cần hỏi anh

- **File do em tạo trong session này** mà chưa commit/save → em có thể xóa tự do (vd: `/tmp/audio_extract.wav` do em tạo, cleanup khi task xong)
- **Empty folder** mà em biết chắc 100% là rác (vd folder rỗng 0 byte)
- **System `/tmp` files** do em tạo trong task

→ Các case này OK để cleanup không hỏi.

## Cross-reference

- Skill `folder-worktree-convention` SKILL.md — main rule
- `references/no-autonomy-anti-patterns.md` — 3 anti-patterns 04/07 evidence
- Skill `recurring-junk-folder-investigation` — khi folder keep reappear (sibling concept)