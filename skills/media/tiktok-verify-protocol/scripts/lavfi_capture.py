#!/usr/bin/env python3
"""
lavfi_capture.py — Capture lavfi filter output đúng cách (PITFALL #27).

Tool workaround cho bug: `ffmpeg -v error -af ebur128 ... -f null` SUPPRESS
info-level output từ lavfi filters (ebur128, blackdetect, silencedetect),
làm agent nghĩ "no output = clean" — SAI.

Dùng đúng flag để capture:
  - ebur128 → no -v error, capture stderr to log
  - blackdetect → -v info + grep "black"
  - silencedetect → no -v error, grep "silence_"
  - volumedetect → always prints summary, không bị suppress

Usage:
    python3 lavfi_capture.py <video.mp4> [filter]

Filters: ebur128 (default), blackdetect, silencedetect, volumedetect

Exit 0 = success, 1 = filter not found / capture failed.

PITFALL context: xem references/lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md (PITFALL #27)
"""

import subprocess
import sys
import tempfile


def run_ebur128(video_path: str) -> dict:
    """Capture EBU R128 loudness summary."""
    cmd = ["ffmpeg", "-i", video_path, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    stderr = r.stderr
    # Extract summary lines
    summary_idx = stderr.find("Summary:")
    if summary_idx < 0:
        return {"error": "no summary found", "stderr_tail": stderr[-500:]}
    summary = stderr[summary_idx:]
    return {"summary": summary, "stderr_full_size": len(stderr)}


def run_blackdetect(video_path: str) -> dict:
    """Detect black frames (need -v info to see black events)."""
    cmd = [
        "ffmpeg", "-v", "info", "-nostats", "-i", video_path,
        "-vf", "blackdetect=d=0.5:pic_th=0.95:pix_th=0.10",
        "-an", "-f", "null", "-",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    black_lines = [l for l in r.stderr.split("\n") if "black" in l.lower()]
    return {
        "black_events": black_lines,
        "count": len(black_lines),
        "verdict": "CLEAN (0 black frames)" if not black_lines else f"{len(black_lines)} black events",
    }


def run_silencedetect(video_path: str, threshold_db: float = -40, min_duration: float = 1.0) -> dict:
    """Detect silent stretches."""
    cmd = [
        "ffmpeg", "-i", video_path, "-vn",
        "-af", f"silencedetect=n={threshold_db}dB:d={min_duration}",
        "-f", "null", "-",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    silence_lines = [l for l in r.stderr.split("\n")
                     if "silence_start" in l or "silence_end" in l]
    return {
        "silence_events": silence_lines,
        "count": len(silence_lines) // 2,  # start + end pairs
        "verdict": "CLEAN (no silent stretches)" if not silence_lines else f"{len(silence_lines) // 2} silent stretches",
    }


def run_volumedetect(video_path: str, first_n_seconds: float = None) -> dict:
    """Run volumedetect (always prints summary)."""
    cmd = ["ffmpeg", "-hide_banner", "-i", video_path, "-vn", "-af", "volumedetect", "-f", "null", "-"]
    if first_n_seconds:
        cmd = ["ffmpeg", "-hide_banner", "-t", str(first_n_seconds), "-i", video_path,
               "-vn", "-af", "volumedetect", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    parsed = {}
    for line in r.stderr.split("\n"):
        if "mean_volume:" in line:
            parsed["mean_volume_db"] = line.split("mean_volume:")[-1].strip().split(" ")[0]
        elif "max_volume:" in line:
            parsed["max_volume_db"] = line.split("max_volume:")[-1].strip().split(" ")[0]
        elif "n_samples:" in line:
            parsed["n_samples"] = line.split("n_samples:")[-1].strip()
    return parsed


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 lavfi_capture.py <video.mp4> [filter]", file=sys.stderr)
        print("Filters: ebur128 (default), blackdetect, silencedetect, volumedetect", file=sys.stderr)
        sys.exit(2)

    video_path = sys.argv[1]
    filt = sys.argv[2] if len(sys.argv) > 2 else "ebur128"

    if filt == "ebur128":
        result = run_ebur128(video_path)
        if "summary" in result:
            print(result["summary"])
        else:
            print(f"ERROR: {result['error']}")
            sys.exit(1)
    elif filt == "blackdetect":
        result = run_blackdetect(video_path)
        print(f"Verdict: {result['verdict']}")
        for ev in result["black_events"][:10]:
            print(f"  {ev}")
    elif filt == "silencedetect":
        result = run_silencedetect(video_path)
        print(f"Verdict: {result['verdict']}")
        for ev in result["silence_events"][:10]:
            print(f"  {ev}")
    elif filt == "volumedetect":
        result = run_volumedetect(video_path)
        for k, v in result.items():
            print(f"  {k}: {v}")
    else:
        print(f"Unknown filter: {filt}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()