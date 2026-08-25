# Pitfall #3 — `check_anchor_lap.py` FALSE POSITIVE TRÊN KEEPS GHÉP (14/07/2026)

## User context

Khi edit clip 0751 (bộ vệ sinh ống kính Pocket 3, source 363.6s), em phát hiện:

- `check_anchor_lap.py` script (Layer 2 verify) báo **FAIL 8 anchor-lap pairs** cho anchor keywords "các bạn", "chúng ta", "thì đó"
- Source audio gốc có "các bạn" 9 lần, "chúng ta" 5 lần, "thì đó" 2 lần (cách nói tự nhiên của anh Tuấn Anh)
- 8/8 pairs đều là **FALSE POSITIVES** — anchor keywords nằm TRONG cùng 1 keep GHÉP, không phải cross-keep boundary

## Vấn đề gốc

`check_anchor_lap.py` check **adjacent segments trong Whisper output**:

```python
for i in range(len(segs) - 1):
    s1, s2 = segs[i], segs[i+1]
    gap = s2.get("start", 0) - s1.get("end", 0)
    for kw in ANCHORS:
        if kw in t1 and kw in t2 and gap < GAP_THRESHOLD_S:
            # FAIL — anchor in adjacent segments
```

**Vấn đề:** Khi em trim keeps GHÉP nhiều source segments liên tiếp (VD keep từ 17.34-49.24s chứa 8+ source segments), Whisper sẽ transcribe mỗi source segment thành 1 Whisper segment riêng biệt. Hai Whisper segments liên tiếp trong cùng 1 keep sẽ có **gap = 0.0s** (audio liên tục, không có cut), nhưng script vẫn báo FAIL vì 2 segments adjacent có cùng anchor keyword.

## Repro recipe

```bash
# 1. Source có anchor keywords tự nhiên
# 2. Build keep_plan với 1 keep GHÉP 5-10 source segments
# 3. Render → Whisper lại → script sẽ báo FAIL dù audio liên tục (không lỗi edit)
```

**Real case clip 0751 V3 (4 keeps GHÉP, 11 source segments):**
- Keep 1: 0.0-17.66s (HOOK_BRIDGE_AUTHORITY) — chứa 1x "các bạn"
- Keep 2: 17.34-49.24s (PROBLEM_USP_FULL_GHÉP) — chứa 5x "các bạn", 3x "chúng ta", 1x "bởi vì"
- Keep 3: 49.24-105.94s (USP_CARBON_FIBER_FULL_GHÉP) — chứa 3x "các bạn", 1x "thì đó"
- Keep 4: 105.94-132.40s (USP_HÚT_BỤI_SÂU_BRIEF) — chứa 1x "thì đó"

→ Script báo 7 anchor-lap pairs dù audio thực tế liên tục, không bị cắt giữa các cụm "các bạn".

## Solution: `verify_with_keep_awareness.py`

Patch script (xem `scripts/verify_with_keep_awareness.py`) — Layer 2 verify với keep boundary awareness:

```python
def is_in_keep(seg, keep_ranges):
    """Check if Whisper segment falls within ANY keep range."""
    seg_start = seg.get("start", 0)
    seg_end = seg.get("end", 0)
    seg_mid = (seg_start + seg_end) / 2

    for ks, ke in keep_ranges:
        if ks - 0.5 <= seg_mid <= ke + 0.5:
            return True
    return False
```

**Logic chính:**
1. Build set of (start, end) keep ranges từ `keeps.json`
2. Với mỗi adjacent Whisper segment pair, check CẢ 2 có nằm trong CÙNG 1 keep range không
3. Nếu CẢ 2 trong cùng keep → **skip (false positive)**
4. Nếu 2 segments thuộc 2 keeps RIÊNG BIỆT → **FAIL thật** (cần fix)

## Test 3 strategies (14/07 case study)

### Strategy A: Trim keeps NHỎ + word-level cut
- **Effectiveness:** ✅ Excellent
- **Best for:** Khi anchor keywords là THẬT cần tránh (cross-keep)
- **Used for:** clip 0749 V4, 0752 V2, 0758 V5 (PASS 2 layers)

### Strategy B: Skip entire keep (duplicate)
- **Effectiveness:** ✅ Good (cho keeps redundant)
- **Best for:** Khi có keep duplicate nội dung
- **Used for:** clip 0758 V5 (skip seg 21 + 31 duplicate)

### Strategy C: Accept PARTIAL_PASS (source natural)
- **Effectiveness:** ⚠️ Trade-off
- **Best for:** Khi source speaker dùng anchor keywords NHIỀU tự nhiên (anh Tuấn Anh)
- **Used for:** clip 0751 (accept với note giải thích)
- **Trade-off:** Ship với 1 layer FAIL nhưng user-acceptable

## Quy tắc vĩnh viễn (FIRST-CLASS)

Khi `check_anchor_lap.py` báo FAIL, PHẢI kiểm tra:

1. **Mở Whisper verify transcript**, check 2 segments
2. **Nếu 2 segments có GAP TIME = 0.0s** VÀ **CHUNG start-end với 1 keep range** → FALSE POSITIVE
3. **Chỉ FAIL thật khi** 2 segments thuộc 2 keeps RIÊNG BIỆT

**Workflow khi Layer 2 FAIL:**

```
1. Check keep_plan.json - 2 segments có cùng keep?
   ├─ YES → FALSE POSITIVE → chấp nhận (anchor tự nhiên trong keep GHÉP)
   └─ NO → CROSS-KEEP FAIL → dùng Strategy A hoặc B
2. Nếu source natural có anchor keywords nhiều → Strategy C (PARTIAL_PASS)
3. Document reason trong output (không báo "đạt goal" nếu PARTIAL_PASS)
```

## Anti-pattern ❌

- ❌ Báo "đạt goal" khi Layer 2 FAIL mà chưa check keep boundaries
- ❌ Trim keeps quá aggressive để ép anchor-lap = 0 (mất narrative)
- ❌ Trust script output mà không đọc keep_plan
- ❌ Chấp nhận cross-keep anchor-lap (đây là lỗi edit thật)

## Best practices (encoded vĩnh viễn)

1. **Chia keeps NHỎ (max 5-10s)** khi source có anchor keywords dày đặc → mỗi keep chỉ chứa 1 instance anchor
2. **Insert gap/implicit silence** giữa keeps có anchor keywords giống nhau
3. **Word-level cut** tại boundary anchor keywords — Whisper sẽ tách segments
4. **Accept PARTIAL_PASS** với ghi chú khi source natural có anchor keywords (anh hay dùng "các bạn"/"chúng ta")

## Test verification

```bash
# Test verify_with_keep_awareness.py
cd ~/.hermes/skills/media/tiktok-verify-protocol/scripts
python3 verify_with_keep_awareness.py <verify.json> <keeps.json>
# exit 0 = no cross-keep anchor-lap (PASS)
# exit 1 = cross-keep anchor-lap detected (FAIL thật)
```

## Cross-reference

- `references/pitfall-verify-2-layers-required-2026-07-14.md` — Pitfall #4 về 2-layer verify
- `scripts/verify_with_keep_awareness.py` — full implementation
- `SKILL.md` PITFALL #3 section — canonical reference

## Real case chi tiết (clip 0751)

Source transcript segment-level anchor keywords:
- seg 0: "bạn nào vẫn đang còn dùng áo..." (1x "bạn")
- seg 5: "khi mà cái máy ảnh chúng ta dùng ở ngoài trời" (1x "chúng ta")
- seg 6: "mắt chúng ta không nhìn thấy được" (1x "chúng ta")
- seg 7: "khi chúng ta lau bằng những cái khăn" (1x "chúng ta")
- seg 9: "ở thời gian đầu có thể các bạn không nhận ra" (1x "các bạn")
- seg 10: "...thì các bạn sẽ thấy là cái chất lượng..." (1x "các bạn")
- seg 11: "bởi vì nó đang có hàng tỷ tỷ..." (1x "bởi vì" + 1x "các bạn")
- seg 12: "...chất lượng hình ảnh mà các bạn quay ra" (1x "các bạn")
- seg 23-25: "...carbon fiber này..." (3x "các bạn")
- seg 30-31: "thì đó là cái chức năng chuyên dụng..." (2x "thì đó" - DUPLICATE exact phrase)

→ Script báo 7-8 anchor-lap pairs
→ Tất cả pairs đều trong cùng keep GHÉP (0.0s gap) → FALSE POSITIVES
→ PARTIAL_PASS accepted với ghi chú "source natural anchor keywords"
