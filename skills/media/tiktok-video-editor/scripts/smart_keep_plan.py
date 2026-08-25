#!/usr/bin/env python3
"""
smart_keep_plan.py — Pad KEEP ranges từ word_timestamps
Đảm bảo từ đầu/cuối của mỗi range capture đúng first/last word (no audio gap)

Usage:
  python3 smart_keep_plan.py <whisper.json> <keep_plan.json> [--output new_keep.json]
"""
import sys
import json
from pathlib import Path


def find_word_range(words, seg_start, seg_end):
    """Find first + last word in [seg_start, seg_end]"""
    first_word_start = None
    last_word_end = None

    for w in words:
        ws, we = w.get('start', 0), w.get('end', 0)
        # Word starts in range OR overlaps range
        if seg_start <= ws < seg_end:
            if first_word_start is None:
                first_word_start = ws
            last_word_end = we

    return first_word_start, last_word_end


def main():
    if len(sys.argv) < 3:
        print("Usage: smart_keep_plan.py <whisper.json> <keep_plan.json> [--output new.json]",
              file=sys.stderr)
        sys.exit(1)

    whisper_json = Path(sys.argv[1])
    keep_plan = Path(sys.argv[2])
    output = keep_plan
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        output = Path(sys.argv[idx + 1])

    if not whisper_json.exists():
        print(f"❌ Whisper JSON not found", file=sys.stderr)
        sys.exit(1)
    if not keep_plan.exists():
        print(f"❌ keep_plan.json not found", file=sys.stderr)
        sys.exit(1)

    # Load whisper
    with open(whisper_json) as f:
        d = json.load(f)

    # Collect all words
    all_words = []
    for s in d.get('segments', []):
        for w in s.get('words', []):
            all_words.append(w)
    all_words.sort(key=lambda x: x['start'])

    # Load keep_plan
    with open(keep_plan) as f:
        plan = json.load(f)

    fixed_count = 0
    padded_count = 0
    avg_gap_before = 0
    avg_gap_after = 0

    new_ranges = []
    for r in plan.get('ranges', []):
        if r.get('action') != 'KEEP':
            new_ranges.append(r)
            continue

        orig_start = float(r['start'])
        orig_end = float(r['end'])

        fw_start, fw_end = find_word_range(all_words, orig_start, orig_end)
        if fw_start is None:
            print(f"⚠️  [{orig_start}-{orig_end}] {r.get('reason', '')}: No words in range!")
            new_ranges.append(r)
            continue

        # Pad 0.05s to ensure audio fade in/out + cleanup
        # (Don't include too much silence around word boundaries)
        new_start = max(0, fw_start - 0.05)
        new_end = fw_end + 0.05

        old_gap = (fw_start - orig_start) + (orig_end - fw_end)
        new_gap = 0.1  # 0.05s start + 0.05s end padding
        avg_gap_before += old_gap
        avg_gap_after += new_gap

        if abs(new_start - orig_start) > 0.01 or abs(new_end - orig_end) > 0.01:
            padded_count += 1
            r['start_padded'] = round(new_start, 2)
            r['end_padded'] = round(new_end, 2)
            r['orig_start'] = orig_start
            r['orig_end'] = orig_end
            r['padded_note'] = f"word-aligned (saved {old_gap:.2f}s of head+tail silence)"

        new_ranges.append(r)

    plan['ranges'] = new_ranges
    plan['padded_summary'] = {
        'ranges_padded': padded_count,
        'total_ranges': len([r for r in new_ranges if r.get('action') == 'KEEP']),
        'avg_gap_before_padding': round(avg_gap_before / max(1, padded_count), 3),
        'avg_gap_after_padding': 0.1,
    }

    # Write output
    with open(output, 'w') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    print(f"═══ SMART PAD RESULT ═══")
    print(f"  Ranges padded: {padded_count}/{plan['padded_summary']['total_ranges']}")
    print(f"  Saved head+tail silence (per range): avg {avg_gap_before / max(1, padded_count):.2f}s → 0.1s")
    print(f"  Output: {output}")


if __name__ == '__main__':
    main()
