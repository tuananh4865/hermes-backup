#!/usr/bin/env python3
"""
verify_with_keep_awareness.py - Layer 2 verify với keep boundary awareness

Khi Whisper output từ file render có nhiều segments LIÊN TIẾP trong cùng 1 keep,
`check_anchor_lap.py` báo false positive vì cùng anchor keyword xuất hiện 2+ lần.

Script này check anchor-lap CHỈ giữa các keeps RIÊNG BIỆT (cross-boundary),
không tính anchor TRONG cùng 1 keep (false positive).

Usage:
    python3 scripts/verify_with_keep_awareness.py <verify.json> <keeps.json>

Exit codes:
    0 = no cross-keep anchor-lap (PASS)
    1 = cross-keep anchor-lap detected (FAIL)
    2 = file not found / invalid JSON
"""

import json
import sys
from pathlib import Path

# Anchor keywords (cập nhật theo real case 14/07)
ANCHORS = [
    # Sponsor / brand
    "nhãn hàng", "nhà sản xuất", "thương hiệu",
    # Connective / filler words
    "nhưng mà", "tuy nhiên", "cho nên", "vì vậy", "do đó", "bởi vì",
    "nói chung", "tóm lại", "cuối cùng", "kết luận",
    # Pronouns / deictic (từ real case 14/07)
    "nhà mình", "bên mình", "các bạn", "mọi người", "chúng ta",
    "thì đó", "nói như vậy", "ý là",
]

# Gap threshold (giây)
GAP_THRESHOLD_S = 5.0
# Tolerance cho keep boundary (giây) - Whisper seg phải nằm GẦN boundary
KEEP_TOLERANCE_S = 0.5


def is_in_keep(seg, keep_ranges):
    """Check if Whisper segment falls within ANY keep range."""
    seg_start = seg.get("start", 0)
    seg_end = seg.get("end", 0)
    seg_mid = (seg_start + seg_end) / 2

    for ks, ke in keep_ranges:
        # Segment midpoint phải nằm trong keep ± tolerance
        if ks - KEEP_TOLERANCE_S <= seg_mid <= ke + KEEP_TOLERANCE_S:
            return True
    return False


def check_cross_keep_anchor_lap(verify_path: str, keeps_path: str) -> list:
    """
    Check anchor-lap CHỈ giữa các keeps RIÊNG BIỆT.
    Trả về list các issues cross-boundary.
    """
    p_verify = Path(verify_path)
    p_keeps = Path(keeps_path)

    if not p_verify.exists():
        print(f"❌ Verify file không tồn tại: {verify_path}")
        sys.exit(2)
    if not p_keeps.exists():
        print(f"❌ Keeps file không tồn tại: {keeps_path}")
        sys.exit(2)

    try:
        verify = json.loads(p_verify.read_text(encoding="utf-8"))
        keeps = json.loads(p_keeps.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(2)

    segs = verify.get("segments", [])
    if not segs:
        print("⚠️ No segments in verify file")
        return []

    # Build keep ranges
    keep_ranges = []
    for k in keeps:
        if "start" in k and "end" in k:
            keep_ranges.append((float(k["start"]), float(k["end"])))

    if not keep_ranges:
        print("⚠️ No keeps provided, falling back to standard check")
        keep_ranges = []

    fails = []
    for i in range(len(segs) - 1):
        s1, s2 = segs[i], segs[i + 1]
        t1 = (s1.get("text") or "").lower()
        t2 = (s2.get("text") or "").lower()
        gap = s2.get("start", 0) - s1.get("end", 0)

        for kw in ANCHORS:
            if kw in t1 and kw in t2 and gap < GAP_THRESHOLD_S:
                # Check if both segments are in the SAME keep (false positive)
                if keep_ranges and is_in_keep(s1, keep_ranges) and is_in_keep(s2, keep_ranges):
                    # Same keep - likely false positive
                    continue
                # Real cross-keep anchor-lap
                fails.append({
                    "seg_pair": [s1.get("id"), s2.get("id")],
                    "keyword": kw,
                    "gap_s": round(gap, 2),
                    "a": t1[:80],
                    "b": t2[:80],
                })

    return fails


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 verify_with_keep_awareness.py <verify.json> <keeps.json>")
        sys.exit(2)

    verify_path = sys.argv[1]
    keeps_path = sys.argv[2]

    fails = check_cross_keep_anchor_lap(verify_path, keeps_path)

    if fails:
        print(f"❌ CROSS-KEEP ANCHOR-LAP detected: {len(fails)} pair(s)\n")
        for f in fails:
            print(f"  pair seg{f['seg_pair']} keyword='{f['keyword']}' gap={f['gap_s']}s")
            print(f"    A: {f['a']}")
            print(f"    B: {f['b']}\n")
        sys.exit(1)

    print("✅ No cross-keep anchor-lap (Layer 2 PASS)")
    sys.exit(0)


if __name__ == "__main__":
    main()
