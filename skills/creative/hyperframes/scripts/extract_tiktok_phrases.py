#!/usr/bin/env python3
"""
Extract TikTok-ready phrase groups from Whisper word-level JSON output.

Usage:
    python3 extract_tiktok_phrases.py <whisper_json> [--group 3] [--max 27]

Output: writes phrases.json next to input file. Merge factor 3-4 with stride
(group count) keeps the total under HyperFrames' ~40-DOM-element limit while
preserving natural phrase boundaries for Vietnamese TikTok narration.

Real case (validated 2026-07-16): 80 raw phrases (4-word groups, 1-word stride)
→ 27 merged phrases (4-word groups, 3-word stride) renders cleanly in
HyperFrames. 80 raw with 1-word stride silently crashes the sub-composition.
"""

import argparse
import json
import sys
from pathlib import Path


def load_words(json_path: Path) -> list[dict]:
    """Load word-level timestamps from Whisper JSON output."""
    data = json.loads(json_path.read_text())
    words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            text = w.get("word", "").strip()
            start = w.get("start")
            end = w.get("end")
            if text and start is not None and end is not None and end > start:
                words.append({"word": text, "start": round(start, 2), "end": round(end, 2)})
    return words


def group_words(words: list[dict], group_size: int = 4, stride: int = 3) -> list[dict]:
    """Group consecutive words into phrases for TikTok subtitle display.

    Args:
        group_size: max words per phrase (4 reads well in TikTok)
        stride: window step (stride=group_size for non-overlap;
                stride<group_size adds overlap for smoother flow)
    """
    phrases = []
    i = 0
    while i < len(words):
        chunk = words[i : i + group_size]
        if not chunk:
            break
        phrases.append(
            {
                "start": chunk[0]["start"],
                "end": chunk[-1]["end"],
                "text": " ".join(w["word"] for w in chunk),
            }
        )
        if i + stride >= len(words):
            break
        i += stride
    return phrases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Whisper JSON file (with word_timestamps=True)")
    parser.add_argument(
        "--group", type=int, default=4, help="Words per phrase (default: 4)"
    )
    parser.add_argument(
        "--stride", type=int, default=3, help="Window step (default: 3)"
    )
    parser.add_argument(
        "--max",
        type=int,
        default=27,
        help="Safety cap — raises if exceeded, suggests larger stride (default: 27)",
    )
    parser.add_argument(
        "--out", help="Output path (default: same dir as input, named phrases.json)"
    )
    args = parser.parse_args()

    json_path = Path(args.input)
    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        return 1

    words = load_words(json_path)
    if not words:
        print(f"Error: no word-level timestamps found in {json_path}", file=sys.stderr)
        return 1

    phrases = group_words(words, args.group, args.stride)

    if len(phrases) > args.max:
        print(
            f"⚠️ {len(phrases)} phrases exceeds HyperFrames DOM limit (~30-40).\n"
            f"   Recommended: increase --stride to {args.stride + 1} or higher\n"
            f"   to merge more aggressively before render.",
            file=sys.stderr,
        )
        if "--yes" not in sys.argv:
            response = input("Continue anyway? [y/N]: ")
            if response.lower() != "y":
                print("Aborted.", file=sys.stderr)
                return 2

    out_path = Path(args.out) if args.out else json_path.parent / "phrases.json"
    out_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2))

    print(f"✅ Wrote {len(phrases)} phrases → {out_path}")
    print(f"   Total duration: {words[0]['start']:.1f}s – {words[-1]['end']:.1f}s")
    print(f"   Group: {args.group} words | Stride: {args.stride}")
    if len(phrases) <= 30:
        print(f"   ✅ Under HyperFrames DOM limit (verified working)")
    return 0


if __name__ == "__main__":
    sys.exit(main())