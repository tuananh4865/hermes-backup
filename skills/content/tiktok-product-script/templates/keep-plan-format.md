# TikTok keep_plan.txt Template

> Use this format for Phase 6 output. Each KEEP line corresponds to one audio segment the editor will cut around in CapCut / tiktok-video-editor.

## Template (one-line-per-keep, TSV-friendly)

```
# === Phase 1 - HOOK 3s ===
KEEP hh:mm.SSS-hh:mm.SSS | "<8 words max, concrete number or specific pain>"

# === Phase 2 - HOOK PRICE ===
KEEP hh:mm.SSS-hh:mm.SSS | "<price + crossed-out original + discount % or freeship>"

# === Phase 3 - SETUP trigger cues ===
KEEP hh:mm.SSS-hh:mm.SSS | "<3-4 situation cues connected by commas or dashes>"

# === Phase 4 - AUTHORITY ===
KEEP hh:mm.SSS-hh:mm.SSS | "<brand + origin + product line + size + format>"

# === Phase 5 - USP #1 ===
KEEP hh:mm.SSS-hh:mm.SSS | "<sensory benefit, NOT spec, customer-facing language>"

# === Phase 6 - PROOF specific ===
KEEP hh:mm.SSS-hh:mm.SSS | "<verified citation [N] OR exact customer name + day count>"

# === Phase 7 - SPEC ===
KEEP hh:mm.SSS-hh:mm.SSS | "<1-2 technical specs that differentiate>"

# === Phase 8 - PUNCHLINE emotion ===
KEEP hh:mm.SSS-hh:mm.SSS | "<emotional hook OR loss-aversion>"

# === Phase 9 - RECIPROCITY bonus ===
KEEP hh:mm.SSS-hh:mm.SSS | "<free gift + value OR bundle offer>"

# === Phase 10 - PROSPECTIVE ===
KEEP hh:mm.SSS-hh:mm.SSS | "<customer imagines using product across the day>"

# === Phase 11 - CTA PUNCH (2 keeps, ≥10s combined) ===
KEEP hh:mm.SSS-hh:mm.SSS | "<deadline OR scarcity OR limited stock>"
KEEP hh:mm.SSS-hh:mm.SSS | "<micro-commit instruction + reciprocal value>"
```

## Worked example — ARMAF Odyssey V1B (viral TikTok)

```
# === Phase 1 - HOOK 3s (8 words max) ===
KEEP 00:00.000-00:03.500 | "4.4K inbox shop chính hãng 30 ngày qua"

# === Phase 2 - HOOK PRICE ===
KEEP 00:03.500-00:06.500 | "Giá gốc 390 - shop chính hãng sale còn 168 - freeship"

# === Phase 3 - SETUP trigger cues ===
KEEP 00:06.500-00:12.500 | "Trước khi lên sân cầu lông - trước khi vào phòng gym - đi cafe cuối tuần - đi biển 2 ngày 4 chỗ đều xịt"

# === Phase 4 - AUTHORITY ===
KEEP 00:12.500-00:18.500 | "ARMAF brand UAE 25 năm rồi - chai 200ml Limited Edition shop chính hãng về đúng 48 chai"

# === Phase 5 - USP #1 ===
KEEP 00:18.500-00:28.500 | "Xịt 1 lần mùi Oriental - ngọt ấm - đồng đội cầu lông đi cùng sân hỏi mùi gì"

# === Phase 6 - PROOF specific ===
KEEP 00:28.500-00:38.500 | "Amazon.ae 4.2 trên 112 review - shop 30 ngày 4.4K người - 42 đã bán trên TikTok Shop"

# === Phase 7 - SPEC ===
KEEP 00:38.500-00:48.500 | "Odyssey 19 biến thể - chọn theo nhóm citrus - woody - oriental - hỏi em tư vấn"

# === Phase 8 - PUNCHLINE emotion (loss-aversion) ===
KEEP 00:48.500-01:00.500 | "Đừng đợi lô Limited Edition hết rồi đi hỏi mua lại giá gốc nha anh em"

# === Phase 9 - RECIPROCITY bonus ===
KEEP 01:00.500-01:15.500 | "Mua 2 tặng 1 túi mesh Yonex đựng vợt - tặng kèm 30K freeship"

# === Phase 10 - PROSPECTIVE ===
KEEP 01:15.500-01:35.500 | "Cầm chai lên sân cầu lông - đi cafe - đi gym - 1 chai đủ dùng cả ngày"

# === Phase 11 - CTA PUNCH (2 keeps ≥10s) ===
KEEP 01:35.500-01:55.500 | "48 chai cuối lô Limited - shop chính hãng về đúng 1 lần này thôi"
KEEP 01:55.500-02:05.500 | "Inbox ARMAF gửi bảng 19 mùi - tặng thêm túi mesh Yonex - trước khi lô hết"
```

## Hard rules per keep

| Rule | Why | How to verify |
|---|---|---|
| No câu treo | Editor will cut mid-clause if predicate incomplete | Read each keep aloud — does it answer "what about it?" |
| Hook ≤8 words | TikTok viewers drop after 8 words in the first 3s | `wc -w` on Phase 1 line; fix if >8 |
| CTA punch ≥10s combined | Phase 11 must span ≥2 keeps | Sum duration of Phase 11 keeps; fix if <10s |
| Each claim with number / brand / spec cites a [N] | Phase 0 research is the source of truth | grep `\[[0-9]\]` near claim; if absent, drop or rewrite |
| ≥1 keep with loss-aversion cue | Trigger #3 must land | grep "đừng\|hết lô\|6-8 tuần\|Limited" in script |
| ≥1 keep with concrete social proof | Trigger #5 must land | grep a specific number (4.2, 112, 4.4K, 42) |

## 3-version template (drop the version-specific framing)

Same skeleton, three different voices:

| Version | Voice | Hook style | Best for |
|---|---|---|---|
| A — Tư vấn 1-1 | Calm, peer-to-peer, "anh em ơi" | Soft fact or statement | Re-targeting existing followers |
| B — Viral TikTok | High energy, concrete number first | Hard number / social proof mass-appeal | First post in a series, mass view goal |
| C — Storytelling | Personal narrative, named character | Specific person + day | Audience that already trusts the KOL |

All three versions share the same Phase 0 citation map and the same 11-phase skeleton. Only the words per keep change.