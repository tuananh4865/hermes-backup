#!/usr/bin/env python3
"""
merge_tiktok_phrases.py — Merge Whisper word-level phrases for HyperFrames.

HyperFrames silently crashes if a sub-composition has >40 DOM phrase elements.
This script groups raw word-level phrases (1-4 words each from Whisper) into
merged phrases of 7-12 words each — reducing 80 raw phrases to ~27 merged phrases,
well under the limit.

Usage:
    python3 merge_tiktok_phrases.py phrases_raw.json [phrases_merged.json] [--group-size 3] [--stride 3]

Input JSON format:
    [
        {"start": 0.0, "end": 1.64, "text": "làm content"},
        {"start": 1.64, "end": 2.54, "text": "được một"},
        ...
    ]

Output JSON format: same as input.
"""
import json
import sys
import argparse


def merge_phrases(raw_phrases, group_size=3, stride=3):
    """Merge phrases bằng cách gộp `group_size` phrases liên tiếp thành 1,
    với stride = group_size (không overlap) hoặc stride < group_size (có overlap).

    Args:
        raw_phrases: list of {start, end, text} từ Whisper word-level timestamps
        group_size: số phrases gộp thành 1 (default 3)
        stride: bước nhảy giữa các nhóm (default 3 = no overlap)

    Returns:
        list of merged phrases
    """
    merged = []
    i = 0
    while i < len(raw_phrases):
        chunk = raw_phrases[i:i + group_size]
        if not chunk:
            break
        merged.append({
            "start": chunk[0]["start"],
            "end": chunk[-1]["end"],
            "text": " ".join(p["text"] for p in chunk).strip(),
        })
        i += stride
    return merged


def to_js_array(phrases):
    """Convert phrases to JS array literal format compatible with HyperFrames template."""
    lines = []
    for p in phrases:
        text_safe = p["text"].replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
        lines.append(f"        {{start: {p['start']}, end: {p['end']}, text: '{text_safe}'}}")
    return "[\n" + ",\n".join(lines) + "\n      ]"


def main():
    parser = argparse.ArgumentParser(description="Merge Whisper phrases for HyperFrames sub-composition.")
    parser.add_argument("input", help="Input JSON file (raw phrases from Whisper)")
    parser.add_argument("output", nargs="?", default=None,
                        help="Output JSON file (default: <input>_merged.json)")
    parser.add_argument("--group-size", type=int, default=3,
                        help="Number of phrases to merge per group (default: 3)")
    parser.add_argument("--stride", type=int, default=None,
                        help="Stride between groups (default: same as group-size, no overlap)")
    parser.add_argument("--js", action="store_true",
                        help="Output as JS array literal (paste into HTML template)")
    args = parser.parse_args()

    if args.stride is None:
        args.stride = args.group_size

    with open(args.input) as f:
        raw = json.load(f)

    merged = merge_phrases(raw, args.group_size, args.stride)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        print(f"✅ Merged {len(raw)} → {len(merged)} phrases → {args.output}")
    else:
        # Default: input_raw.json → input_raw_merged.json
        default_out = args.input.replace(".json", "_merged.json")
        with open(default_out, "w") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        print(f"✅ Merged {len(raw)} → {len(merged)} phrases → {default_out}")

    if args.js:
        js_str = to_js_array(merged)
        print("\nJS array (paste into HTML template `__PHRASES_DATA__`):")
        print(js_str)

    # Warning if still too many
    if len(merged) > 30:
        print(f"\n⚠️  Still {len(merged)} phrases. HyperFrames may crash. Try --group-size 5 or 6.")


if __name__ == "__main__":
    main()
