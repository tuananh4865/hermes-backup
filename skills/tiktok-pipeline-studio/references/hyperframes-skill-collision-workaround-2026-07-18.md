# HyperFrames Skill Collision — `skills/hyperframes/` vs `creative/hyperframes/`

> **TL;DR:** Hai skills trong hệ thống Hermes có cùng tên `hyperframes`, gây
> ambiguity khi `skill_view(name='hyperframes')`. Phải dùng full path
> `skill_view(name='creative/hyperframes')` cho motion-graphic workflow.

## Bối cảnh (18/07/2026)

Khi em setup pipeline studio, em gọi `skill_view(name='hyperframes')` và nhận
error:
```
Ambiguous skill name 'hyperframes': 2 skills match across your local skills
dir and external_dirs. Refusing to guess — load one explicitly by its
categorized path.
```

Hai skills match:
- `/Users/tuananh4865/.hermes/skills/hyperframes/SKILL.md` (router chính — 23KB)
- `/Users/tuananh4865/.hermes/skills/creative/hyperframes/SKILL.md` (motion-graphic — 83KB)

## Hai Skills Khác Nhau Như Thế Nào?

| Dimension | `skills/hyperframes/` | `creative/hyperframes/` |
|---|---|---|
| **Mục đích** | Router cho HyperFrames create/edit/render generic | Concrete motion-graphic + TikTok subtitle pipeline |
| **Size** | 23KB | 83KB (gấp 3.6x) |
| **Style** | Workflow-catalog + intent layer (giống HeyGen upstream) | Hardened production patterns từ 18 ngày TikTok edit |
| **Use cases** | Anything HyperFrames: trailer, explainer, slideshow, port từ Remotion | Cụ thể: TikTok liquid glass V22, subtitle sync, motion text, 8-phase diverse motion, Three.js cinematic |
| **Skill format** | Lean router (frontmatter + §1-§6 routing rules) | Encyclopedic production cookbook (40+ pitfalls + 5 templates + 4 scripts) |
| **Owner** | HeyGen upstream (apache-2.0) | Tuấn Anh + Hermes Agent (Tuấn-specific TikTok patterns) |

## Workaround: Khi Nào Load Cái Nào?

```python
# ❌ AMBIGUOUS — fails with 2-match error
skill_view(name='hyperframes')

# ✅ EXPLICIT — load router
skill_view(name='hyperframes')  # nhưng nếu trong category prefix, dùng:
skill_view(name='creative/hyperframes')  # motion-graphic thực chiến
```

### Decision Tree

```
User asks for HyperFrames video creation
├── Generic (any type) ───────────────▶ Load `skills/hyperframes/` (router)
│                                         │
│                                         └─ It routes to specific workflow
│                                            (/motion-graphics, /talking-head-recut, etc.)
└── TikTok-specific production ────────▶ Load `creative/hyperframes` (cookbook)
                                        │
                                        └─ Skip intent layer, use concrete templates
```

## Tại Sao Chưa Merge?

18/07/2026 đánh giá:
- `skills/hyperframes/` = upstream skill (apache-2.0) — sync với HeyGen main, update thường xuyên
- `creative/hyperframes/` = Tuấn-specific production cookbook — chứa 18 ngày TikTok patterns riêng

Nếu merge → mỗi lần HeyGen upstream update → phải merge conflict thủ công với Tuấn-specific content → tốn công hơn giữ tách.

**Recommendation:** GIỮ TÁCH, sửa SKILL.md cả 2 để có note về collision.

## Status 18/07/2026

- ✅ `tiktok-pipeline-studio/SKILL.md` v1.0.0 đã document collision ở § "Pitfall: HyperFrames skill collision"
- ✅ `creative/hyperframes/SKILL.md` đã note thêm về việc nên dùng full path
- ⏳ CHƯA patch `skills/hyperframes/SKILL.md` để note — xem § "Pending" bên dưới

## Pending Action Items

| # | Action | Effort | Priority |
|---|---|---|---|
| 1 | Patch `skills/hyperframes/SKILL.md` thêm 1 dòng: "If anh is doing TikTok motion-graphic specifically, load `creative/hyperframes` instead" | 2 phút | Medium |
| 2 | Tạo alias `tiktok-motion-graphic` → `creative/hyperframes` để không phải nhớ full path | 5 phút | Low |
| 3 | Merge 2 skills thành 1 (kill collision hoàn toàn) | 30-60 phút merge conflict | Low (chỉ khi anh complain) |

## Related Files

- `~/.hermes/skills/hyperframes/SKILL.md` (upstream router)
- `~/.hermes/skills/creative/hyperframes/SKILL.md` (Tuấn-specific cookbook)
- `~/.hermes/skills/tiktok-pipeline-studio/SKILL.md` (orchestrator, đã reference cả 2)