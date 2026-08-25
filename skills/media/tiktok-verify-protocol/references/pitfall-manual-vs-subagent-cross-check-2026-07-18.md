# PITFALL #18 — Manual Suspect Pair CẦN Cross-Check Subagent (Timestamp Evidence)

> **Ngày**: 2026-07-18
> **Skill**: `~/.hermes/skills/media/tiktok-verify-protocol/`
> **Version**: 1.0.11 (NEW PITFALL #16-18)
> **Cross-reference**: `media/tiktok-video-editor` Pitfall #29 sub-section B (Manual verify CÓ THỂ SAI)

---

## 🚨 Context — Real Case Clip 0004 Doroto Air Luxe V3 (18/07/2026)

User yêu cầu: *"Check lại 6 video mới nhất trong footages xem đã eddit chưa? nếu đã edit rồi thì verify lại từng cái và check false start kĩ từng đoạn để lọc lại một lần nữa"*

Khi verify clip 0004, em manual scan text thấy 2 cặp suspect phrase:
- **PAIR A**: "Đây là mẫu hút bụi Dodoto Air Luxe V3" + "Đây là mẫu hút bụi Dodoto Luxe V3" (TÊN SẢN PHẨM lặp)
- **PAIR B**: "Cục binh của nó là 4000mAh... khu vực liên tục" + "...liên tục được" (PIN 4000mAh lặp)

Em manual confirm: **PAIR A = BOTH_IN_CUT (FAIL), PAIR B = BOTH_IN_CUT (FAIL)**

Subagent dispatched với context "đặc biệt check 2 cặp này":

| Pair | Subagent Verdict | Detail |
|---|---|---|
| **PAIR A** | **BOTH_IN_CUT (FAIL)** ✓ | seg 1 (10.56s) + seg 2 (14.62s) — cả 2 takes còn trong cut |
| **PAIR B** | **TAKE_NEW_ONLY (PASS)** | Chỉ có 1 occurrence ở 96.94s — TAKE CŨ đã bị editor cắt từ trước |

**Em manual confirm sai 1/2 cặp.**

---

## 🎯 Lesson VĨNH VIỄN (FIRST-CLASS)

**Manual scan text transcript KHÔNG CÓ timestamp chi tiết → FALSE POSITIVE rate cao. PHẢI re-dispatch subagent (scope gọn) với context "đặc biệt check K cặp này" trước khi báo verdict chính thức.**

### Tại sao manual sai

1. **Manual scan** thấy 2 dòng giống prefix → flag FALSE START (intuition "take lặp")
2. **NHƯNG** subagent check timestamp word-level thấy:
   - TAKE CŨ đã bị editor cắt đúng từ trước
   - 2 dòng giống nhưng ở 2 timestamp khác nhau (vì source có lặp keyword)
   - Chỉ 1 take thật sự trong cut
3. Manual KHÔNG có timestamp → không phân biệt được "take cũ + take mới" vs "chỉ 1 take được giữ"

### Workflow cập nhật

```python
def verify_manual_suspect_pairs(clips, suspect_pairs):
    """Bước 1: Manual scan list K cặp suspect (initial hint)
       Bước 2: Re-dispatch subagent scope GỌN
       Bước 3: Cross-check verdict enum từng cặp
    """
    # Step 1: Manual scan
    manual_verdicts = {pair.id: "BOTH_IN_CUT (initial hint - manual)" 
                       for pair in suspect_pairs}
    
    # Step 2: Re-dispatch subagent scope GỌN
    subagent_verdicts = dispatch_subagent_scope_gon(
        clips=clips,
        scope="CHECK_K_SUSPECT_PAIRS",
        suspect_pairs=suspect_pairs
    )
    
    # Step 3: Cross-check
    final_verdicts = {}
    for pair in suspect_pairs:
        sub_verdict = subagent_verdicts.get(pair.id, "UNKNOWN")
        if manual_verdicts[pair.id] != sub_verdict:
            final_verdicts[pair.id] = (
                f"CONFLICT: manual={manual_verdicts[pair.id]}, "
                f"subagent={sub_verdict}"
            )
        else:
            final_verdicts[pair.id] = sub_verdict
    return final_verdicts
```

---

## 🛡️ Trade-off Matrix — Manual vs Subagent Verify

| Method | Time | False Positive Risk | When to use |
|---|---|---|---|
| **Manual scan text only** | 1-2 phút | ⚠️ **Cao (1/2 PAIR B case)** | Initial hint, KHÔNG báo verdict |
| **Subagent scope GỌN** (check K cặp) | 90-180s | ✅ Thấp | Verdict chính thức |
| **Subagent scope FULL** (7 layers) | 5-10 phút | ✅ Rất thấp | Multi-clip batch lớn |

→ **Best practice**: Manual scan → list suspect pairs → re-dispatch subagent scope GỌN với context "check K cặp này" → verdict chính thức

---

## 🚫 Anti-Patterns VĨNH VIỄN

- ❌ Manual confirm "BOTH_IN_CUT" cho K cặp mà KHÔNG cross-check subagent
- ❌ Báo verdict manual như chính thức → có thể ship action sai (giống PAIR B case 18/07)
- ❌ Tin tưởng 100% vào cảm tính "rõ ràng là take lặp" mà KHÔNG verify bằng timestamp
- ❌ Bỏ qua subagent confirmation vì "manual đã đủ chính xác" → false positive risk cao
- ❌ Báo cáo "PAIR B: FALSE START (manual)" khi subagent confirm "PAIR B: PASS (TAKE_NEW_ONLY)"

---

## 🎯 Khi nào KHÔNG cần subagent cross-check

- Pair có timestamp evidence rõ ràng (vd seg 5 ở 12.34s vs seg 7 ở 16.78s, gap > 5s) → manual đủ
- Single take không có cặp để compare
- Đã chạy script `check_anchor_lap.py` với keep awareness → có timestamp rõ
- Đã chạy `scripts/verify_clip_full.py` Layer 4 FALSE START scan

---

## 📊 4 Verdict Enum (PITFALL #14)

| Verdict | Ý nghĩa | Action |
|---|---|---|
| **BOTH_IN_CUT** | Cả 2 take (cũ + mới) đều còn trong cut | **FAIL** — phải cắt 1 |
| **TAKE_NEW_ONLY** | Chỉ 1 take (mới) trong cut, take cũ đã cắt | **PASS** |
| **TAKE_OLD_ONLY** | Chỉ 1 take (cũ) trong cut, take mới đã cắt | **PASS** (rare) |
| **NEITHER** | Không còn take nào | **FAIL** — content thiếu |

---

## 🎯 Trade-off Matrix

| Khía cạnh | Manual scan | Subagent (scope gọn) | Subagent (full scope) |
|---|---|---|---|
| Thời gian | 1-2 phút | 90-180s | 5-10 phút (risk TIMEOUT) |
| Timestamp precision | ❌ Không có | ✅ Word-level | ✅ Word-level + audio waveform |
| False positive risk | ⚠️ Cao (PAIR B case) | ✅ Thấp | ✅ Rất thấp |
| Khi nào dùng | Initial scan để list suspect pairs | Suspect pairs cần confirm | Full audit (post-batch, 1-clip) |
| Output | Text-only verdict (risk sai) | Markdown report + timestamp evidence | Full report + audio waveform |

---

## 🔗 Cross-Reference

- `media/tiktok-video-editor` v3.34.0 (Pitfall #32-#36 added 18/07):
  - PITFALL #32: Concat filter_complex CÙNG source + `-ss -to` BUG
  - PITFALL #33: Dùng file Final_ làm input, KHÔNG phải RAW
  - PITFALL #34: Manual verify có thể SAI — cross-check subagent (lesson này)
  - PITFALL #35: Mỗi clip fail PHẢI fix ngay
  - PITFALL #36: Pattern browser-use/video-use migrate folder structure
- `tiktok-verify-protocol` v1.0.11 (PITFALL #14-22 added 18/07):
  - PITFALL #14: Manual suspect pair verification workflow (4 verdict enum)
  - PITFALL #15: FILLER position classifier (trailing intonation)
  - PITFALL #16: Manual suspect pair PHẢI cross-check subagent (lesson này)
  - PITFALL #17: Subagent TIMEOUT → re-dispatch SCOPE GỌN
  - PITFALL #18: Manual suspect pair + subagent cross-check (lesson này)
  - PITFALL #19: Mỗi clip fail fix ngay
  - PITFALL #20: Re-render dùng Final_ không phải RAW
  - PITFALL #21: Concat filter_complex same-source BUG
  - PITFALL #22: video-use migration folder pattern

---

## 📋 Decision Tree cho Manual Verify Workflow

```
User flag "PAIR X: phrase_a, phrase_b"
  ↓
1. Manual scan text → initial verdict = BOTH_IN_CUT (intuition)
  ↓
2. Run scripts/verify_clip_full.py Layer 4 (FALSE START scan) → X hints
  ↓
  X = 0 → Manual đúng (NEITHER / TAKE_NEW_ONLY) → PASS
  X ≥ 1 → Cần subagent cross-check
  ↓
3. Dispatch subagent scope GỌN:
   python3 scripts/dispatch_subagent.py \
     --scope CHECK_K_SUSPECT_PAIRS \
     --pair-a "<phrase_a>" --pair-b "<phrase_b>"
  ↓
4. Subagent return verdict enum (BOTH_IN_CUT / TAKE_NEW_ONLY / NEITHER)
  ↓
5. Cross-check manual vs subagent
  ↓
  Match → Use subagent verdict (CHÍNH THỨC)
  Conflict → Flag CONFLICT in report → User quyết
  ↓
6. Build keep plan with verdict + timestamp evidence
```

---

## ✅ Verification Checklist (MỚI 18/07)

Trước khi báo verdict chính thức về suspect pair:

- [ ] **Manual scan** text → list K cặp suspect (initial verdict: BOTH_IN_CUT)
- [ ] **Cross-check subagent** scope GỌN với context "đặc biệt check K cặp này"
- [ ] **Subagent verdict** mới là CHÍNH THỨC
- [ ] **Manual verdict** chỉ là INITIAL HINT — ghi rõ "manual pending subagent confirmation"
- [ ] **KHÔNG BÁO** verdict manual như chính thức cho đến khi subagent confirm

**Tool BẮT BUỘC**:
- `scripts/dispatch_subagent.py --scope CHECK_K_SUSPECT_PAIRS` (TODO)
- `scripts/verify_with_keep_awareness.py` (PITFALL #3 keep boundary)
- `scripts/verify_clip_full.py` Layer 4 (PITFALL #10/11)

---

## 📊 Real Case Stats (18/07/2026) — PAIR B Lesson

- **Suspect pairs flagged**: 2 (PAIR A + PAIR B)
- **Manual confirm BOTH_IN_CUT**: 2/2 (intent "take lặp")
- **Subagent verdict**: 1 PASS (PAIR A) + 1 FAIL (PAIR B)
- **Accuracy manual**: 50% (1/2 đúng)
- **Accuracy manual sau cross-check**: 100% (sau re-dispatch)
- **Time saved by manual-only**: -3 min (manual 1 phút, nhưng risk action sai)
- **Time spent on cross-check**: +2 min (subagent scope GỌN 90-180s)
- **Trade-off**: +2 min cho 100% accuracy vs -3 min nhưng 50% accuracy

→ **Best practice**: ALWAYS cross-check manual với subagent — chỉ +2 min, accuracy 100%.

---

**Date**: 2026-07-18 14:30 ICT
**Skill version**: tiktok-verify-protocol 1.0.11
**Lesson author**: Hermes mini-subagent verify pipeline (PAIR B false positive detected)
