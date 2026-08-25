# KarmaVid Pivot V2 — Case Study 11/07/2026

> Session-specific detail về pivot KarmaVid project từ V1 (đồ ăn biến hình + 2.5D Pixar) → V2 (CON NGƯỜI + Voxel 3D pixel). Đây là case study VERIFIED — dùng làm template cho future rapid pivot trên animation project khác.

## Context

**Project:** KarmaVid — TikTok animation channel (lấy cảm hứng từ @herocat2309 — onion girl universe, 120.7M views top video)
**Setup date:** 2026-06-26 (V1)
**Pivot date:** 2026-07-11 16:32 + 16:38 (V2 — 2 lệnh trong 6 phút)
**Owner:** Tuấn Anh
**Orchestrator:** Hermes (default profile, MiniMax-M3)

## Timeline chi tiết (reconstructed từ session)

| Time (ICT) | Event |
|------------|-------|
| **16:32** | Anh: *"đọc project karmavid"* |
| **16:32-16:50** | Em load 5 file context (hub.md + 4 research file) + tóm tắt nhanh cho anh |
| **16:50-16:55** | Em embed summary KarmaVid V1 + hỏi anh muốn làm gì tiếp (5 options) |
| **16:55 (16:38 next message)** | **Anh: *"tất cả các nhân vật thay đổi lại thành con người"*** |
| **16:55** | Em hiểu = pivot lớn. Bắt đầu re-read hub.md + T-02.1 universe + T-03.1 template + T-03.2 samples |
| **~16:58 (16:38 thứ 2 trong 16:55 block)** | **Anh: *"style hoạt hình 3D pixal"*** (typo "pixal" = pixel) |
| **16:58** | Em identify pivot = 2 trụ: (1) nhân vật đồ ăn → CON NGƯỜI, (2) visual 2.5D → voxel 3D pixel |
| **16:58-17:15** | Em re-design 4 file với pivot matrix (V1 vs V2):<br>- hub.md (5.1 KB → 10.8 KB)<br>- T-02.1 universe (14.1 KB → 19.7 KB)<br>- T-03.1 template (12.8 KB → 13.6 KB)<br>- T-03.2 samples (11.8 KB → 17.3 KB) |
| **17:15-17:20** | Em update hub.md pivot summary + verify 4 file đã update |
| **17:20-17:25** | Em log pivot event vào logs/2026-07-11-pivot-v2-session.md |
| **17:25** | Em embed summary Telegram (V1 vs V2 table + sample script demo + next steps) |

**Total elapsed:** ~30 phút từ lệnh pivot đầu tiên → embed summary xong.

## Pivot Matrix (V1 → V2)

### Thay đổi (ĐỔI)

| Element | V1 (26/06) | V2 (11/07) |
|---------|-------------|-------------|
| Nhân vật chính | Phở (bát phở voxel), Ớt Hiểm (quả ớt voxel), Bánh Mì Bé (ổ bánh mì voxel) | Phở Phi (cô đầu bếp voxel), Ớt Hiểm (anh nông dân voxel), Bánh Mì Bé (cậu bé bán báo voxel) |
| Phản diện | Bà Mụ Già (bà già mập voxel), Nước Mắm Phú (chai nước mắm voxel), Xúc Xích Xấu (cây xúc xích voxel) | Bà Mụ Già (bà chủ nhà hàng voxel), Nước Mắm Phú (anh trai phản bội voxel), Xúc Xích Xấu (mẹ kế ác voxel) |
| Visual style | 2.5D low-poly Pixar-like smooth | Voxel 3D pixel (Minecraft + Among Us hybrid) |
| Frame rate | 24-30 FPS mịn | 12-24 FPS voxel giật nhẹ (retro feel) |
| Camera | 3D free camera | Isometric 30-45° + close-up voxel |
| Palette | Vibrant smooth gradient | 16-32 màu flat shading retro pixel |
| Lighting | Smooth gradient + bloom | Flat shading + warm ambient + flash pixel |

### Giữ nguyên 100% (KHÔNG ĐỔI)

| Element | Detail |
|---------|--------|
| Concept | "Karma là luật chơi" — kẻ ác bị trừng phạt, người tốt được đền đáp |
| Universe rules | 5 rules: Karma Rule, Transformation Rule, Real Person Rule, Power Rule, Villain Weakness Rule |
| Setting | Karmacity — Sài Gòn thập niên 90-2000 |
| 5 locations | Quán Phở Bà Linh, Biệt thự Bà Mụ, Cây Đa Đầu Làng, Chợ Nổi, Miếu Thờ |
| Catchphrases | *"Phở nào cũng phải nấu bằng tình yêu thương!"*, *"Cay thì phải chịu, nhưng ác thì phải trả!"*, *"Bánh mì nè! Ai cho thêm pate vô không?"*, etc. |
| Voice | Giọng Việt (Phở Phi = nữ dịu dàng, Ớt Hiểm = nam trầm hơi khàn, Bánh Mì Bé = nam cao trong trẻo, etc.) |
| Series arcs | 5 parts Phở Phi / 6 parts Ớt Hiểm / 8 parts Bánh Mì Bé |
| Công thức | 8-scene + 11-scene (≤20 từ thoại, 8 giây/scene) |

## Frontmatter Pivot Convention (áp dụng cho mọi file pivot)

```yaml
---
title: [Title]
created: YYYY-MM-DD (V1)
updated: YYYY-MM-DD (V2 - pivot date)
type: research
tags: [...]
supersedes: [filename-v1]   # ← Trỏ về file V1 cũ
pivot_date: YYYY-MM-DD
pivot_reason: "Anh yêu cầu X → Y"
---
```

## Hub Pivot Summary Template (áp dụng cho hub.md pivot)

```markdown
## ⚡ PIVOT NGÀY YYYY-MM-DD (Quan trọng - đọc trước)

**Lý do pivot:** Anh muốn thay đổi hoàn toàn 2 yếu tố visual:

| Element | V1 | V2 |
|---------|----|----|
| [yếu tố 1] | [old] | [new] |
| [yếu tố 2] | [old] | [new] |

**GIỮ NGUYÊN 100%:**
- [Concept]
- [Rules]
- [Setting]
- [Voice]
- [Series arcs]
```

## File-by-file Pivot Action Plan (template)

Khi gặp rapid pivot (2 lệnh liên tiếp <10 phút), làm theo thứ tự:

### 1. ĐỌC 4 file cũ song song (5-10 min)

Dùng `read_file` hoặc `execute_code` để load song song:
- `hub.md` (project overview)
- `research/T-XX-universe.md` (character design)
- `research/T-XX-template.md` (script formula)
- `research/T-XX-samples.md` (sample scripts)

### 2. IDENTIFY GIỮ NGUYÊN vs ĐỔI (5 min)

Tạo pivot matrix trong đầu (hoặc note nhanh). Trong KarmaVid case:
- GIỮ NGUYÊN: concept Karma, universe rules, setting, voice, arcs, formula 8-scene
- ĐỔI: nhân vật form (đồ ăn → người) + visual style (2.5D → voxel 3D)

### 3. RE-DESIGN từng file với "GIỮ NGUYÊN + ĐỔI" matrix (15-20 min)

Mỗi file:
- Update frontmatter (thêm `supersedes`, `pivot_date`, `pivot_reason`)
- Update content (giữ nguyên 70-80%, đổi 20-30%)
- Thêm section "V1 vs V2" ở cuối file để track pivot

### 4. UPDATE hub.md với PIVOT SUMMARY (5 min)

Hub = điểm vào duy nhất. PHẢI có section "⚡ PIVOT NGÀY YYYY-MM-DD" ngay đầu file để future sessions đọc trước.

### 5. LOG pivot event vào logs/ (2 min)

`logs/YYYY-MM-DD-pivot-vN-session.md` — session log với:
- Timeline
- Pivot matrix
- Deliverables
- Lessons learned

### 6. EMBED SUMMARY Telegram (1 turn)

Output cho anh đọc:
- V1 vs V2 table (markdown)
- Sample script demo (1 scene)
- Next steps (4 options)

## Lessons learned (cho future rapid pivot sessions)

### Lesson 1: Rapid pivot signal = 2 lệnh liên tiếp <10 phút

Khi anh ra lệnh A → lệnh B trong <10 phút, đó là signal pivot lớn. EM phải:
- KHÔNG hỏi "anh có chắc không?" (đã trigger quick pivot = anh chắc chắn)
- KHÔNG re-research từ đầu (đã có context)
- ĐỌC NHANH file cũ → RE-DESIGN NGAY → UPDATE NGAY

### Lesson 2: Frontmatter `supersedes` field là bắt buộc cho pivot

Mỗi file pivot PHẢI có:
```yaml
supersedes: T-XX-v1-filename.md   # ← Trỏ về V1 cũ
pivot_date: YYYY-MM-DD
pivot_reason: "[verbatim từ anh]"
```

Để future sessions hiểu: file này thay thế file nào, khi nào, vì lý do gì.

### Lesson 3: V1 vs V2 table ở cuối file = audit trail

Mỗi file pivot nên có section cuối:
```markdown
## 📊 SO SÁNH V1 vs V2

| Element | V1 | V2 |
|---------|----|----|
| ... | ... | ... |
```

Để dễ scan và verify pivot consistency giữa các file.

### Lesson 4: Hub.md pivot summary = single source of truth

Hub.md PHẢI có section "⚡ PIVOT NGÀY YYYY-MM-DD" ngay đầu file (SAU frontmatter, TRƯỚC phần NORTH STAR). Đây là điểm vào duy nhất để future sessions hiểu project đã pivot.

### Lesson 5: 30 phút total elapsed = benchmark

KarmaVid case: 2 lệnh pivot → 4 file updated (61.4 KB content) → embed summary Telegram = ~30 phút. Đây là benchmark cho future rapid pivot sessions. Nếu > 60 phút = em bị stuck.

## Anti-patterns (KHÔNG làm khi gặp rapid pivot)

❌ Hỏi anh "anh có chắc muốn đổi không?" — anh đã chắc chắn khi ra 2 lệnh liên tiếp
❌ Re-research từ đầu mà không đọc file cũ — lãng phí time + cost
❌ Pivot 1 file rồi dừng — phải pivot TẤT CẢ file liên quan (hub + universe + template + samples)
❌ Không update hub.md pivot summary — future sessions không biết project đã pivot
❌ Không log pivot event — mất audit trail
❌ Pivot sang style KHÔNG có sẵn MagicaVoxel/Blender support — phải verify tools trước khi commit

## Related skill triggers

Khi trigger này fire, load skill `voxel-3d-character-animation` (SKILL.md mục 5):
- "đổi nhân vật từ A → B" + "đổi visual style" (2 lệnh liên tiếp)
- "voxel" / "3D pixel" / "Minecraft style character"
- "MagicaVoxel export" / "Blender render voxel"
- "character bible voxel"

## File paths (verified)

- Project root: `/Volumes/Storage-1/Hermes/wiki/projects/karmavid/`
- Hub: `hub.md` (V2 = 10.8 KB, updated 11/07/2026)
- Research: `research/T-02.1-karmavid-universe.md` (V2 = 19.7 KB)
- Template: `research/T-03.1-karmavid-script-template.md` (V2 = 13.6 KB)
- Samples: `research/T-03.2-karmavid-script-samples.md` (V2 = 17.3 KB)
- Session log: `logs/2026-07-11-pivot-v2-session.md`