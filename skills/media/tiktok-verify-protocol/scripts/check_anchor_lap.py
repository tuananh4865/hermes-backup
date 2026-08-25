#!/usr/bin/env python3
"""
check_anchor_lap.py - Bổ sung semantic layer cho verify_clip.py v3.21.4

Phát hiện anchor-keyword lặp giữa các Whisper verify segments liên tiếp
(không phụ thuộc chosen_segs filter của verify_clip).

Dùng SAU khi verify_clip.py PASS, như pitfall #1 trong SKILL.md.

Usage:
    python3 scripts/check_anchor_lap.py <verify.json>

Exit codes:
    0 = no anchor-lap detected
    1 = anchor-lap found (in ra chi tiết)
    2 = file not found / invalid JSON
"""
import json
import sys
from pathlib import Path

# Anchor keywords thường gây lap_nghia khi xuất hiện 2+ lần trong segs adjacent
ANCHORS = [
    # Sponsor / brand
    "nhãn hàng", "nhà sản xuất", "thương hiệu",
    # Connective / filler words
    "nhưng mà", "tuy nhiên", "cho nên", "vì vậy", "do đó", "bởi vì",
    "nói chung", "tóm lại", "cuối cùng", "kết luận",
    # Pronouns / deictic
    "nhà mình", "bên mình", "các bạn", "mọi người", "chúng ta",
    # Discourse markers that open takes
    "thì đó", "nói như vậy", "ý là",
]

# Gap threshold (giây) — nếu 2 segs anchor cùng keyword mà cách nhau < gap → coi là lap
GAP_THRESHOLD_S = 5.0


def check_anchor_lap(verify_path: str) -> list:
    p = Path(verify_path)
    if not p.exists():
        print(f"❌ File không tồn tại: {verify_path}")
        sys.exit(2)

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(2)

    segs = data.get("segments", [])
    if not segs:
        print("⚠️ No segments in verify file")
        return []

    fails = []
    for i in range(len(segs) - 1):
        s1, s2 = segs[i], segs[i + 1]
        t1 = (s1.get("text") or "").lower()
        t2 = (s2.get("text") or "").lower()
        gap = s2.get("start", 0) - s1.get("end", 0)

        for kw in ANCHORS:
            if kw in t1 and kw in t2 and gap < GAP_THRESHOLD_S:
                fails.append({
                    "seg_pair": [s1.get("id"), s2.get("id")],
                    "keyword": kw,
                    "gap_s": round(gap, 2),
                    "a": t1[:80],
                    "b": t2[:80],
                })

    return fails


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_anchor_lap.py <verify.json>")
        sys.exit(2)

    fails = check_anchor_lap(sys.argv[1])

    if fails:
        print(f"❌ ANCHOR-LAP detected: {len(fails)} pair(s)\n")
        for f in fails[:20]:
            print(f"  pair seg{f['seg_pair']} keyword='{f['keyword']}' gap={f['gap_s']}s")
            print(f"    A: {f['a']}")
            print(f"    B: {f['b']}\n")
        sys.exit(1)

    # Recount segments for transparency
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    seg_count = len(data.get("segments", []))
    print(f"✅ No anchor-lap across {seg_count} segments ({len(ANCHORS)} keywords, gap<{GAP_THRESHOLD_S}s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
