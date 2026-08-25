#!/usr/bin/env python3
"""
Concat N audio files với 30ms fadeout ONLY (fix PITFALL #6 audio gap).

ĐÃ FIX: KHÔNG cần trim padding - dùng `pad_duration=0` khi generate (xem generate_voice.py).
Audio segments đã không có lead/trail silence nên concat mượt tự nhiên.

Chỉ apply 30ms fade out ở cuối mỗi segment để smooth transition.

Usage:
  python3 concat_segments.py --inputs f1.wav f2.wav f3.wav --output final.wav
  python3 concat_segments.py --inputs-dir batch_results/ --output final.wav
"""
import sys
import os
import argparse
import subprocess
from pathlib import Path


def get_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, timeout=5,
    )
    try:
        return float(out.stdout.strip())
    except:
        return 0.0


def concat_files(inputs: list, output: str, fade_ms: int = 30):
    if not inputs:
        print("❌ No input files")
        return
    if len(inputs) == 1:
        subprocess.run(["cp", inputs[0], output])
        print(f"✅ Copied {inputs[0]} → {output}")
        return

    durations = [get_duration(f) for f in inputs]
    total_input = sum(durations)
    print(f"Concatenating {len(inputs)} files, total input: {total_input:.2f}s")

    # Build filter: 30ms fade out ONLY ở cuối mỗi segment
    parts = []
    for i, dur in enumerate(durations):
        fade_out_start = max(0, dur - (fade_ms / 1000))
        filter_str = (
            f"[{i}]afade=t=out:st={fade_out_start}:d={fade_ms/1000}[a{i}]"
        )
        parts.append(filter_str)

    inputs_str = "".join(f"[a{i}]" for i in range(len(inputs)))
    concat_filter = f"{inputs_str}concat=n={len(inputs)}:v=0:a=1[out]"
    full_filter = ";".join(parts) + ";" + concat_filter

    cmd = ["ffmpeg", "-y"]
    for f in inputs:
        cmd.extend(["-i", f])

    cmd.extend([
        "-filter_complex", full_filter,
        "-map", "[out]",
        "-ar", "24000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        output,
    ])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ ffmpeg error:\n{result.stderr[-500:]}")
        return

    out_dur = get_duration(output)
    print(f"✅ Concat → {output}")
    print(f"   Input: {total_input:.2f}s | Output: {out_dur:.2f}s")


def main():
    parser = argparse.ArgumentParser(description="Concat audio files với 30ms fadeout")
    parser.add_argument("--inputs", nargs="+", help="Input WAV files")
    parser.add_argument("--inputs-dir", help="Directory of WAV files")
    parser.add_argument("--pattern", default="*.wav", help="Glob pattern (default: *.wav)")
    parser.add_argument("--output", required=True, help="Output WAV file")
    parser.add_argument("--fade-ms", type=int, default=30, help="Fade duration in ms (default: 30)")
    args = parser.parse_args()

    inputs = []
    if args.inputs:
        inputs = args.inputs
    elif args.inputs_dir:
        inputs = sorted([str(p) for p in Path(args.inputs_dir).glob(args.pattern)])
        print(f"Found {len(inputs)} files in {args.inputs_dir} (pattern: {args.pattern})")

    if not inputs:
        print("❌ No input files. Use --inputs or --inputs-dir")
        return

    concat_files(inputs, args.output, args.fade_ms)


if __name__ == "__main__":
    main()
