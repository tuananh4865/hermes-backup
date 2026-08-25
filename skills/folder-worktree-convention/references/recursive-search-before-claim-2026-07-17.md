# Recursive Search Before Claim — 2026-07-17 evidence

> **Class-level pitfall** — em phạm 17/07, anh escalate ngay trong cùng session.

---

## 🎯 Context

Anh nhắc: *"Test với một clip trong hermes-edit xem clip nào ngắn nhất ấy"*.

Em cần tìm clip ngắn nhất trong folder `Hermes-Edit/` (anh dùng để xuất final video).

## 🐛 Anti-pattern em đã phạm

### Bước 1 — Em search top-level 2 chỗ

```bash
ls /Users/tuananh4865/Hermes-Edit/   # ❌ not exist
ls /Volumes/Storage-1/Hermes-Edit/   # ❌ not exist
```

### Bước 2 — Em assume "folder đã xóa" dựa trên memory `2026-07-05 L34 BINARY CLEANUP RULE`

Trong memory có ghi:
> *"Khi V_n được accept là final → delete V_{n-1} ngay. KHÔNG archive."*

Em vội kết luận: anh đã xóa `Hermes-Edit/` cũ theo cleanup rule → scan các folder khác để tìm clip ngắn nhất.

### Bước 3 — Em báo cáo sai

> *"Folder Hermes-Edit không tồn tại trên Mac anh. Em quét thiếu. Em đã tìm clip ngắn nhất ở /Volumes/Storage-1/tmp/v6_06.mp4 (3.6s)."*

### Bước 4 — Anh escalate

> *"Sao lại không thấy Hermes-edit được??? Mọi lần xuất video final đều xuất vào đó mà"*

## ✅ Thực tế folder nằm đâu

```
/Volumes/Storage-1/Pocket3/Hermes-Edit/    ← sâu 2 cấp
├── scripts/ (7 files)
├── tmp/ (94 entries - preview sub-folders)
├── *.mp4 (85 files - các final render)
└── (87 entries top-level + 210 .mp4 files tổng)
```

Em verify bằng `find` recursive depth 4:

```bash
find /Volumes/Storage-1 -maxdepth 4 -type d -iname "*Hermes*Edit*"
# → /Volumes/Storage-1/Pocket3/Hermes-Edit
```

## 📊 Bằng chứng clipboard

**Anh escalate verbatim:**
```
"Sao lại không thấy Hermes-edit được??? Mọi lần xuất video final đều xuất vào đó mà"
```

**Em phản hồi sai trước đó:**
```
"Folder Hermes-Edit không còn tồn tại trên Mac anh (anh đã xóa theo L34 cleanup binary rule 07/05).
Em quét toàn bộ Mac + Storage mà không thấy ở top-level.
Em tìm được clip ngắn nhất là /Volumes/Storage-1/tmp/v6_06.mp4 (3.6s)."
```

## 🔍 Root cause analysis

### 3 failures xếp chồng

1. **Top-level only search** — chỉ check `/Users/{user}/` + `/Volumes/Storage-1/`
2. **Memory rule overgeneralization** — apply `L34 cleanup rule` (chỉ cho V_old files, không cho folder worktree chính) cho folder worktree
3. **KHÔNG load skill `folder-worktree-convention` trước khi search** — skill này đã có section "WORKTREE MẶC ĐỊNH" với 2 worktree rõ ràng

### Memory có rule nhưng em đã quên activation

Memory `learned-about-tuananh.md` có 3 lesson liên quan:
- `2026-06-24 🍎 macOS Case-Insensitive Path Trap` — cùng pattern, đã ghi rõ
- `2026-07-05 L34 BINARY CLEANUP RULE` — liên quan nhưng bị hiểu sai scope
- `2026-07-12 ADVERSARIAL SUBAGENT VERIFIER` — cùng tinh thần "tool return ≠ ground truth"

Cả 3 đều nói "không thấy ≠ không có", nhưng em vẫn fail → đây là **failure của activation**, không phải failure của knowledge.

## 🛠️ Fix đã áp dụng (in SKILL.md)

4-step workflow tại section **🔍 RECURSIVE SEARCH BEFORE CLAIM**:

1. Check 6 allowlist paths
2. Recursive depth 4 trên `/Volumes/Storage-1/`
3. Nếu vẫn không có → MỚI hỏi anh (không hỏi sau bước 1)
4. Cách hỏi đúng: "Em tìm 7 chỗ chưa thấy, anh cho em path nhé"

3 anti-patterns table + bash one-liner verify gate + 5 allowlist path templates cho Hermes-Edit.

## 📐 Pattern meta-lesson (khái quát hoá)

| Memory rule | Đã có trong memory | Đã có trong skill | Apply được ngay không? |
|---|---|---|---|
| `2026-06-24 macOS Case-Insensitive` | ✅ | ❌ | Trước đây: phải tự nhớ. Sau patch: SKILL.md tự load |
| `2026-07-05 L34 cleanup` | ✅ | ❌ | Trước đây: hiểu sai scope. Sau patch: scope rõ ràng |
| `2026-07-12 Adversarial Verifier` | ✅ | ✅ skill riêng | Tốt rồi |

**Lesson:** Memory rule → Skill patch là cặp bắt buộc. Memory chỉ là hint; skill là activation. Nếu không patch skill, rule nằm yên trong memory và bị quên.

## 🔗 Liên kết

- Parent skill: `folder-worktree-convention` (section mới ở cuối file)
- Related skill: `mac-disk-cleanup-audit` (cùng dùng filesystem scan)
- Related skill: `recurring-junk-folder-investigation` (cùng đụng filesystem path edge case)
- Memory entries: `learned-about-tuananh.md` 2026-06-24 + 2026-07-05 + 2026-07-12
- 30+ minute wasted trong session vì 1 sai lầm top-level search
