# ARMAF Odyssey Body Spray 200ML — Worked Case Study

> **Date:** 2026-07-07
> **Skill version:** tiktok-product-script v0.4.0
> **Pipeline end-to-end time:** ~12 minutes
> **Purpose:** Real worked example showing Phase -1 → 8 in action. Use as a template for any new product research run. Note: this case study is the source of the 2× user correction that promoted Phase -1 routing to BLOCKING.

---

## 0. Phase -1 — Routing (the part that broke)

**Initial mistake (2026-07-07, twice):** agent auto-saved ARMAF Odyssey files into `tuan-anh-badminton/` because 95% of past sessions were badminton work. User flagged:

> *"Xịt khử mùi đâu liên quan đến project tuan anh badminton đâu, nó là kênh tiktok của anh mà!!!"*

…and then again:

> *"Sản phẩm nếu không thuộc ngành hàng cầu lông, phụ kiện cầu lông thì không cho vào project cầu lông! Armaf là nước hoa body mist"*

**Routing table fired correctly on second pass** — `ARMAF` keyword matched row 2 of the routing table → `wiki/projects/tuan-anh-review-tiktok/`. Files were moved.

**Lesson that hardened into a rule**: Phase -1 is now BLOCKING in the procedure. The agent must explicitly check the routing table before any save. If the keyword list doesn't match, ask the user ONCE with: *"Sp này vô shop cầu lông hay kênh review lifestyle anh?"*

## 1. Input from user

```
[Image: TikTok screenshot of product listing]
[Text: "đây là clip anh đã đăng"]
```

The user supplied a TikTok Shop listing image for ARMAF Odyssey Body Spray 200ML. No prior product-research cache existed. Pipeline ran fresh.

## 2. Phase 0 — Research output (6 sources)

| Source | Type | Key data captured |
|---|---|---|
| [1] Fragrantica | Wikipedia-equivalent | Brand origin: UAE, founded 1999 by Hassan Naeem, parent = Sterling Parfums Industries LLC |
| [2] YouTube Samy Andraus | Review | "19 Armaf Odyssey Fragrances" — confirms 19 variants |
| [3] Whizz.ae | Brand site | "Armaf Odyssey Mandarin Sky Limited Edition 6.8 Oz / 200ml" |
| [4] Amazon.ae | Reviews | 4.2/5 rating on 112 reviews, Oriental fragrance family |
| [5] Sharaf DG UAE | Distributor | "Long-lasting 200ml body spray for all-day freshness" |
| [6] ARMAF reseller Instagram | Marketing | "100% Authentic Direct Import from UAE" |

**Reject rule fired once**: "Xịt 1 lần lưu 2-2.5h" → no ARMAF-specific longevity study → kept only as community estimate, NOT cited as brand fact.

## 3. Phase 1-3 — Awareness + visual hooks

- **Awareness level**: 4 (Product Aware). Customers already know ARMAF + body mist category; need CTA push.
- **Visual hook**: ARMAF logo in silver on Limited Edition yellow + 4.4K / 42 buyers / $168-390 price gap.
- **Trigger cues** (lifestyle, not cầu lông): sân cầu lông / gym / cafe / đi biển.

## 4. Phase 4 — Principle selection

| Principle | Has verified data? | Decision |
|---|---|---|
| #1 Hook 3s | ✅ "4.4K inbox" + "19 mùi" | ✅ USE |
| #2 Free > Discount | ✅ Freeship + túi mesh + 30K | ✅ USE (later) |
| #3 Loss aversion 2:1 | ✅ Limited Edition 48 chai | ✅ USE |
| #4 Trigger density | ✅ 4 chỗ: sân / gym / cafe / biển | ⚠️ Drop (4 would be over) |
| #5 Social proof | ✅ Amazon.ae 4.2/5 web-cited | ✅ USE |
| #6 Fewer choices | ✅ "19 mùi, chọn nhóm citrus/woody/oriental" | ⚠️ Drop |
| #7 Reciprocity | ✅ "Tặng bảng 19 mùi khi comment ARMAF" | ✅ USE |

**Final combo: #1 + #3 + #5** (3 principles, exactly at the cap).

## 5. Phase 5 — 11-phase blueprint (3 versions side-by-side)

| Phase | Time | V1A (tư vấn 1-1) | V1B (viral — RECOMMENDED) | V1C (storytelling) |
|---|---|---|---|---|
| 1 HOOK 3s | 0-3s | "Anh em ơi ARMAF chính hãng về chính hãng Việt Nam đây" | "4.4K inbox shop chính hãng 30 ngày qua" | "Hôm qua anh Khoa inbox em hỏi mua ARMAF Odyssey" |
| 2 HOOK PRICE | 3-6s | "Giá gốc 390 - sale chính hãng còn 168 freeship nha anh em" | "Giá gốc 390 - shop chính hãng sale còn 168 - freeship" | "Bây giờ giá gốc 390 - sale chính hãng còn 168 thôi" |
| 3 SETUP | 6-12s | "Lên sân - gym - cafe - biển đều xịt được" | "Trước khi sân / gym / cafe cuối tuần / biển 4 chỗ đều xịt" | "Thằng Khoa nói lên sân cầu lông xịt - tối gym vẫn thơm" |
| 4 AUTHORITY | 12-18s | "ARMAF brand UAE 1999 - chai 200ml Limited Edition - body spray chứ không phải nước hoa nha" | "ARMAF brand UAE 25 năm rồi - chai 200ml Limited Edition shop chính hãng về đúng 48 chai" | "ARMAF brand Ả Rập 1999 - chai 200ml Limited Edition hiếm - body spray" |
| 5 USP | 18-28s | "Xịt 1 cái mùi Oriental - ngọt ấm - không nồng đầu - dùng cả ngày" | "Xịt 1 lần mùi Oriental - ngọt ấm - đồng đội cầu lông hỏi mùi" | "Xịt 1 cái thơm cả ngày - mùi Oriental không nồng - thằng Khoa gật đầu" |
| 6 PROOF | 28-38s | "Amazon.ae 4.2 trên 112 review - shop 30 ngày 4.4K người" | "Amazon.ae 4.2 trên 112 review - shop 30 ngày 4.4K người - 42 đã bán TikTok Shop" | "Anh em inbox shop tháng qua 4.4K - 42 đã bán tuần này" |
| 7 SPEC | 38-48s | "Odyssey 19 mùi - chai 200ml Long-lasting - 4 mùi top bán chạy" | "Odyssey 19 biến thể - chọn nhóm citrus - woody - oriental" | "Odyssey 19 mùi - top bán chạy em kể anh sau" |
| 8 PUNCHLINE | 48-60s | "Ngon hơn mấy chai 50k ngoài chợ - chính hãng UAE về đàng hoàng" | "Đừng đợi lô Limited Edition hết rồi đi hỏi mua lại giá gốc" | "Anh Khoa mua xong 3 ngày sau đã inbox mua thêm - vợ khen thơm" |
| 9 RECIPROCITY | 60-75s | "Mua 2 tặng 1 túi mesh Yonex đựng vợt + 30K trị giá" | "Mua 2 tặng 1 túi mesh Yonex đựng vợt + 30K freeship" | "Mua 2 tặng 1 túi mesh Yonex - anh Khoa đựng vợt luôn" |
| 10 PROSPECTIVE | 75-95s | "Sáng sân - chiều cafe - tối gym cả ngày 1 chai đủ" | "Cầm chai sân - cafe - gym - 1 chai đủ cả ngày" | "Sáng sân - chiều anh Khoa cafe - ai cũng hỏi mùi" |
| 11 CTA (2 keeps ≥10s) | 95-125s | "Lô Limited 48 chai shop chính hãng - hết chờ 6-8 tuần" + "Inbox ARMAF + sđt em gửi bảng 19 mùi" | "48 chai cuối lô Limited - về đúng 1 lần" + "Inbox ARMAF gửi bảng 19 mùi + túi mesh trước khi lô hết" | "Lô chính hãng cuối - inbox ARMAF + sđt em tư vấn mùi" + "Như anh Khoa - inbox là em gửi bảng so sánh" |

## 6. Phase 7 — Cross-verify (what got caught and fixed)

| Dimension | Initial state | Fix applied |
|---|---|---|
| Hook word-count ≤8 | V1B Phase 1 had 14 words ("30 ngày qua 4.4K anh em inbox shop chính hãng mua chai ARMAF này") | Compressed to 8: "4.4K inbox shop chính hãng 30 ngày qua" |
| Citation map | All 3 versions traced back to [1]-[5] + shop listing | PASS after compression |

**Lesson that hardened into a rule**: the hook word-count check is now a mandatory line in Phase 7, not an afterthought.

## 7. Phase 8 — Delivery shape

Telegram embed contained:
1. 11-phase blueprint table (3 versions side-by-side)
2. Full keep_plan for each version
3. Citation map showing every claim → [N] source
4. 5 KPI targets (hook rate / completion / comments / inbox / conversion)
5. 1-line "Sources pointer" → `wiki/projects/tuan-anh-review-tiktok/products/armaf-odyssey-body-spray-200ml.md` (CORRECTED PATH from original tuananh-badminton/)
6. Recommendation: V1B for TikTok Shop launch (concrete-number hook matches mass-view intent).

## 8. Files persisted (corrected paths after Phase -1 fix)

| Path | Size | Purpose |
|---|---|---|
| `wiki/projects/tuan-anh-review-tiktok/products/armaf-odyssey-body-spray-200ml.md` | 5.7 KB | Phase 0 research cache — re-usable for any future ARMAF Odyssey script |
| `wiki/projects/tuan-anh-review-tiktok/scripts/armaf-odyssey-body-spray-200ml-v1.md` | 14.8 KB | 3-version script deliverable |

> **Before Phase -1 fix**: files were saved at `wiki/projects/tuan-anh-badminton/products/` and `wiki/projects/tuan-anh-badminton/scripts/` — WRONG PROJECT. Manual cleanup required user flag + move.

## 9. Reuse rules

- If the user asks for another ARMAF Odyssey clip in the future, **skip Phase 0** and read the existing cache directly. Re-research only if the product line or pricing changes.
- The 3-version structure (tư vấn / viral / storytelling) is the default template — only change the angle, not the phase skeleton.
- The Amazon.ae 4.2/5 citation is the strongest social proof for this category; keep it as the default Phase 6 anchor unless the user explicitly asks for shop-side numbers only.

## 10. What this case proves about the routing rule

If the agent had run Phase -1 first (table check), it would have routed `ARMAF` → row 2 → `tuan-anh-review-tiktok/` automatically. The 2× user correction + cleanup would never have been needed. The 30s cost of running the table is worth saving 5-10 min of file moves + user frustration.