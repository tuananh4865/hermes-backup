#!/usr/bin/env python3
"""
check_overlap.py — PITFALL #91 KEEP_PLAN_OVERLAP detection & auto-fix

Usage:
    python3 check_overlap.py <keep_plan.json> [--auto-fix] [--in-place]

Options:
    --auto-fix    Trim end_padded của keep N = min(end_padded, next.start_padded)
                  cho mọi keep (trừ keep cuối). Ghi đè keep_plan.json (--in-place) hoặc
                  output JSON mới.
    --in-place    Ghi đè file gốc (chỉ khi --auto-fix).

Exit codes:
    0  - no overlap detected (hoặc đã auto-fix thành công)
    1  - overlap detected, KHÔNG auto-fix
    2  - file not found / parse error
"""
import json
import sys
import argparse

def check_overlap(keep_plan):
    """Trả về list các (idx_a, name_a, idx_b, name_b, overlap_sec)."""
    keeps = keep_plan.get("keeps", [])
    overlaps = []
    for i in range(len(keeps) - 1):
        cur = keeps[i]
        nxt = keeps[i+1]
        s_cur = cur.get("start_padded", cur["start"])
        e_cur = cur.get("end_padded", cur["end"])
        s_nxt = nxt.get("start_padded", nxt["start"])
        overlap = e_cur - s_nxt
        if overlap > 0.05:  # 50ms tolerance cho word-boundary rounding
            overlaps.append({
                "from_idx": i,
                "to_idx": i+1,
                "from_name": cur.get("name", f"keep_{i}"),
                "to_name": nxt.get("name", f"keep_{i+1}"),
                "overlap_sec": round(overlap, 3),
                "from_range": [round(s_cur, 3), round(e_cur, 3)],
                "to_range": [round(s_nxt, 3), round(nxt.get("end_padded", nxt["end"]), 3)],
            })
    return overlaps

def auto_fix(keep_plan):
    """Trim end_padded của keep N = min(end_padded, next.start_padded)."""
    keeps = keep_plan.get("keeps", [])
    total_trimmed = 0.0
    for i in range(len(keeps) - 1):
        e_cur = keeps[i]["end_padded"]
        s_nxt = keeps[i+1]["start_padded"]
        if e_cur > s_nxt:
            total_trimmed += e_cur - s_nxt
            keeps[i]["end_padded"] = s_nxt
    # Recompute expected_duration nếu có
    if "expected_duration" in keep_plan:
        keep_plan["expected_duration"] = sum(
            k["end_padded"] - k["start_padded"] for k in keeps
        )
    return total_trimmed

def main():
    parser = argparse.ArgumentParser(description="PITFALL #91 KEEP_PLAN_OVERLAP checker")
    parser.add_argument("keep_plan", help="Path to keep_plan.json")
    parser.add_argument("--auto-fix", action="store_true", help="Auto-trim overlap")
    parser.add_argument("--in-place", action="store_true", help="Overwrite original file (with --auto-fix)")
    args = parser.parse_args()

    try:
        with open(args.keep_plan) as f:
            keep_plan = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ ERROR reading {args.keep_plan}: {e}", file=sys.stderr)
        sys.exit(2)

    overlaps = check_overlap(keep_plan)
    if not overlaps:
        print(f"✓ no overlap in {args.keep_plan}")
        sys.exit(0)

    print(f"⚠️ KEEP_PLAN_OVERLAP detected ({len(overlaps)} pairs):")
    total = 0.0
    for o in overlaps:
        print(f"   {o['from_name']} ({o['from_range']}) → {o['to_name']} ({o['to_range']}): {o['overlap_sec']}s overlap")
        total += o["overlap_sec"]
    print(f"   TOTAL overlap: {total:.3f}s")

    if not args.auto_fix:
        print("\n→ FIX: chạy `python3 check_overlap.py <file> --auto-fix --in-place` để trim tự động")
        print("   HOẶC sửa keep_plan.json bằng tay: end_padjusted_keep_N = min(end_padded, next.start_padded)")
        sys.exit(1)

    # Auto-fix
    trimmed = auto_fix(keep_plan)
    print(f"\n→ Auto-fix: trimmed {trimmed:.3f}s overlap")

    if args.in_place:
        with open(args.keep_plan, "w") as f:
            json.dump(keep_plan, f, indent=2, ensure_ascii=False)
        print(f"   Wrote {args.keep_plan}")
    else:
        # Output to stdout for piping
        print("→ New keep_plan (use --in-place to write):")
        print(json.dumps(keep_plan, indent=2, ensure_ascii=False))

    sys.exit(0)

if __name__ == "__main__":
    main()
