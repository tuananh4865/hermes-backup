#!/usr/bin/env python3
"""
build_concat_list.py — Build ffmpeg Concat demuxer từ keep_plan.json

Usage:
  python3 build_concat_list.py <keep_plan.json> <concat_list.txt> <input.mp4>
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) != 4:
        print("Usage: build_concat_list.py <keep_plan.json> <concat_list.txt> <input.mp4>",
              file=sys.stderr)
        sys.exit(1)

    keep_plan = Path(sys.argv[1])
    concat_list = Path(sys.argv[2])
    input_mp4 = sys.argv[3]

    if not keep_plan.exists():
        print(f"❌ keep_plan.json not found: {keep_plan}", file=sys.stderr)
        sys.exit(1)

    with open(keep_plan) as f:
        plan = json.load(f)

    keep = []
    for r in plan.get('ranges', []):
        if r.get('action') == 'KEEP':
            # Sử dụng padded boundaries nếu có (từ smart_keep_plan.py)
            start = r.get('start_padded', r.get('start'))
            end = r.get('end_padded', r.get('end'))
            keep.append((float(start), float(end)))

    if not keep:
        print(f"❌ No KEEP ranges in keep_plan", file=sys.stderr)
        sys.exit(1)

    expected = plan.get('expected_duration')
    actual_dur = sum(e - s for s, e in keep)
    print(f"Plan: {len(keep)} KEEP ranges, expected={expected}s, actual={actual_dur:.2f}s")
    if plan.get('padded_summary'):
        s = plan['padded_summary']
        print(f"  Padded: {s['ranges_padded']}/{s['total_ranges']} ranges (avg gap {s['avg_gap_before_padding']}s → 0.1s)")

    with open(concat_list, 'w') as f:
        for s, e in keep:
            f.write(f"file '{input_mp4}'\n")
            f.write(f"inpoint {s}\n")
            f.write(f"outpoint {e}\n")
    print(f"Wrote {len(keep)} segments to {concat_list}")


if __name__ == '__main__':
    main()
