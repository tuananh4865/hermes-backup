#!/usr/bin/env python3
"""
gop_keyframe_extract.py — Reliable GOP/keyframe extraction từ MP4 (PITFALL #26).

Tool workaround cho bug: `ffprobe -skip_frame nokey -of csv=p=0` trả empty
cho MP4 encode bằng libx264 + Lavf. Dùng JSON show_frames + filter pict_type=I
thay thế — đảm bảo output đúng cho mọi encoder.

Usage:
    python3 gop_keyframe_extract.py <video.mp4>
    # Output:
    #   I-frames: 26
    #   GOP avg=3.93s min=1.80s max=7.23s
    #   First @ 0.000s  Last @ 98.333s

Exit 0 = success, 1 = no keyframes (corrupt file).

PITFALL context: xem references/lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md (PITFALL #26)
"""

import json
import subprocess
import sys


def extract_keyframes(video_path: str) -> dict:
    """Extract I-frame times via JSON show_frames + pict_type filter."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "frame=pts_time,pkt_pts_time,pict_type,key_frame",
        "-of", "json",
        video_path,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(r.stdout)
    frames = data.get("frames", [])
    iframes = [f for f in frames if f.get("pict_type") == "I"]
    times = []
    for f in iframes:
        ts = f.get("pts_time")
        if ts is not None:
            times.append(float(ts))
    return {
        "total_frames": len(frames),
        "iframes": len(times),
        "first_pts": times[0] if times else None,
        "last_pts": times[-1] if times else None,
        "times": times,
    }


def gop_stats(times: list) -> dict:
    """Compute GOP gaps statistics."""
    if len(times) < 2:
        return {"gaps": [], "avg": None, "min": None, "max": None}
    gaps = [round(times[i + 1] - times[i], 3) for i in range(len(times) - 1)]
    return {
        "gaps": gaps,
        "avg": round(sum(gaps) / len(gaps), 2),
        "min": min(gaps),
        "max": max(gaps),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 gop_keyframe_extract.py <video.mp4>", file=sys.stderr)
        sys.exit(2)

    video_path = sys.argv[1]
    result = extract_keyframes(video_path)
    times = result["times"]
    stats = gop_stats(times)

    print(f"Total frames: {result['total_frames']}")
    print(f"I-frames (keyframes): {result['iframes']}")
    if result["iframes"] > 0:
        print(f"First keyframe: {result['first_pts']:.3f}s")
        print(f"Last keyframe:  {result['last_pts']:.3f}s")
        if stats["avg"] is not None:
            print(f"GOP: avg={stats['avg']}s  min={stats['min']}s  max={stats['max']}s")
            # TikTok Shorts verdict
            if stats["max"] <= 7.0:
                print("Verdict: PASS (GOP ≤7s, OK cho TikTok Shorts)")
            elif stats["max"] <= 10.0:
                print("Verdict: ACCEPTABLE (GOP 7-10s, seek hơi chậm)")
            else:
                print(f"Verdict: WARNING (GOP >10s, max={stats['max']}s — slow seek)")
        sys.exit(0)
    else:
        print("Verdict: FAIL — 0 keyframes detected (file có thể corrupt)")
        sys.exit(1)


if __name__ == "__main__":
    main()