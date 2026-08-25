#!/usr/bin/env python3
"""verify_motion.py — Motion verify cho diverse-motion clip (PITFALL #9, 18/07/2026).

Dual-signal motion detector cho source DJI/GoPro/iPhone quay thiếu sáng.
Pure pixel-diff với threshold 15 cho FALSE FREEZE trên dark source vì
mean RGB < 30 → nền đen chiếm đa số pixel.

Usage:
    python3 scripts/verify_motion.py <video.mp4> [--frames 22] [--interval 5] [--phases 8]

Output:
    Phase-by-phase matrix + dual-signal verdict (MOVING/STATIC) per consecutive frame pair.

PITFALL #9 rationale:
    - pixel-diff threshold 15 → 21/21 windows < 5% → FALSE "freeze"
    - pixel-diff threshold 5 + mean RGB Δ ≥ 3 → 18/21 windows MOVING → CORRECT
    - Vision check: text overlay (Bước 1/2/3, Bấm link) tạo motion dù camera static

Snippets embedded dưới cho ad-hoc verification (không cần render lại video).
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


def extract_frames(video_path: str, num_frames: int, interval: float) -> list:
    """Extract N frames at `interval`-second spacing using ffmpeg."""
    tmpdir = tempfile.mkdtemp(prefix="verify_motion_")
    duration_cmd = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True, check=True,
    )
    duration = float(duration_cmd.stdout.strip())
    times = [round(i * interval, 2) for i in range(num_frames) if i * interval < duration]
    frames = []
    for i, t in enumerate(times):
        out = os.path.join(tmpdir, f"frame_{i:02d}_t{t:.0f}s.jpg")
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(t), "-i", video_path,
             "-frames:v", "1", "-q:v", "2", out],
            capture_output=True, check=True,
        )
        frames.append((t, out))
    return frames


def pixel_diff_pct(p1: str, p2: str, thresh: int = 5) -> float:
    """% pixels changed > threshold. Default thresh=5 (relaxed from default 15
    để detect motion trên dark source)."""
    a = Image.open(p1).convert("RGB")
    b = Image.open(p2).convert("RGB")
    if a.size != b.size:
        b = b.resize(a.size)
    diff = ImageChops.difference(a, b).convert("L")
    px = list(diff.getdata())
    return sum(1 for p in px if p > thresh) / len(px) * 100


def mean_rgb_delta(p1: str, p2: str) -> float:
    """Mean delta of RGB channels giữa 2 frames (scene change indicator)."""
    s1 = ImageStat.Stat(Image.open(p1).convert("RGB")).mean
    s2 = ImageStat.Stat(Image.open(p2).convert("RGB")).mean
    return sum(abs(s1[i] - s2[i]) for i in range(3)) / 3


def motion_dual_signal(p1: str, p2: str, pixel_thresh: float = 5.0, rgb_thresh: float = 3.0):
    """Dual-signal: MOVING nếu pixel_diff ≥ pixel_thresh HOẶC ΔRGB ≥ rgb_thresh."""
    pd = pixel_diff_pct(p1, p2, thresh=5)
    rd = mean_rgb_delta(p1, p2)
    moving = (pd >= pixel_thresh) or (rd >= rgb_thresh)
    return moving, pd, rd


def make_phases(num_phases: int, duration_s: float) -> list:
    """Chia clip thành N phase boundaries. Default 8-phase diverse-motion."""
    names = ["HOOK", "PROBLEM", "INTRO", "FEATURE",
             "DEMO", "COMPARE", "PROOF", "CTA"]
    n = min(num_phases, len(names))
    chunk = duration_s / n
    return [(round(i * chunk, 1), round((i + 1) * chunk, 1), names[i])
            for i in range(n)]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", help="Path to .mp4 file")
    ap.add_argument("--frames", type=int, default=22,
                    help="Số frames extract (default 22 = mỗi 5s cho clip 110s)")
    ap.add_argument("--interval", type=float, default=5.0,
                    help="Giây giữa 2 frames (default 5s)")
    ap.add_argument("--phases", type=int, default=8,
                    help="Số phase boundaries (default 8 diverse-motion)")
    ap.add_argument("--pixel-thresh", type=float, default=5.0)
    ap.add_argument("--rgb-thresh", type=float, default=3.0)
    args = ap.parse_args()

    if not os.path.isfile(args.video):
        print(f"❌ Video not found: {args.video}")
        sys.exit(2)

    # Probe duration
    dur_cmd = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", args.video],
        capture_output=True, text=True, check=True,
    )
    duration = float(dur_cmd.stdout.strip())
    print(f"📹 Video: {args.video}")
    print(f"   Duration: {duration:.2f}s")
    print(f"   Frames: {args.frames} @ interval {args.interval}s")
    print()

    # Extract frames
    frames = extract_frames(args.video, args.frames, args.interval)
    print(f"Extracted {len(frames)} frames to {os.path.dirname(frames[0][1])}\n")

    # Consecutive motion matrix
    print("=== CONSECUTIVE MOTION (dual-signal) ===")
    print(f"{'From→To':>14s} | {'Pdiff%':>7s} | {'ΔRGB':>6s} | Verdict")
    n_moving = 0
    for i in range(len(frames) - 1):
        t1, f1 = frames[i]
        t2, f2 = frames[i + 1]
        moving, pd, rd = motion_dual_signal(f1, f2, args.pixel_thresh, args.rgb_thresh)
        verdict = "MOVING" if moving else "STATIC"
        if moving:
            n_moving += 1
        print(f"{t1:>5.1f}s→{t2:<5.1f}s | {pd:>6.2f}% | {rd:>5.2f} | {verdict}")
    n_total = len(frames) - 1
    print(f"\n→ {n_moving}/{n_total} consecutive windows MOVING ({n_moving/n_total*100:.0f}%)")

    # Phase-by-phase matrix
    phases = make_phases(args.phases, duration)
    frame_map = {t: f for t, f in frames}
    print(f"\n=== PHASE-BY-PHASE (8-phase diverse-motion) ===")
    print(f"{'Phase':10s} | {'Window':10s} | {'PeakPdiff':>9s} | {'MeanΔRGB':>9s} | Verdict")

    n_pass = 0
    for start, end, name in phases:
        avail = sorted(t for t in frame_map if start <= t <= end)
        if len(avail) < 2:
            print(f"{name:10s} | {start:>4.1f}-{end:>4.1f}s | (insufficient frames)")
            continue
        peak_pdiff = max(
            pixel_diff_pct(frame_map[avail[i]], frame_map[avail[i + 1]])
            for i in range(len(avail) - 1)
        )
        peak_drgb = max(
            mean_rgb_delta(frame_map[avail[i]], frame_map[avail[i + 1]])
            for i in range(len(avail) - 1)
        )
        # Phase verdict: PASS nếu peak Pdiff ≥ 8% HOẶC ΔRGB ≥ 1.0 (HOOK/CTA fade)
        is_hooked_cta = name in ("HOOK", "CTA")
        pass_threshold_pdiff = 5.0 if is_hooked_cta else 8.0
        pass_threshold_rgb = 1.0  # HOOK/CTA fade mạnh
        if is_hooked_cta:
            passed = (peak_drgb >= pass_threshold_rgb) or (peak_pdiff >= pass_threshold_pdiff)
        else:
            passed = peak_pdiff >= pass_threshold_pdiff

        verdict = "✓ PASS" if passed else "⚠ LOW"
        if passed:
            n_pass += 1
        print(f"{name:10s} | {start:>4.1f}-{end:>4.1f}s | {peak_pdiff:>8.2f}% | {peak_drgb:>8.2f} | {verdict}")

    print(f"\n→ {n_pass}/{len(phases)} phases PASS")

    # Final verdict
    print()
    if n_moving / n_total >= 0.85 and n_pass >= 4:
        print("✅ VERDICT: MOTION OK — diverse-motion clip ready to ship")
        sys.exit(0)
    elif n_moving / n_total >= 0.7 and n_pass >= 3:
        print("⚠️ VERDICT: CONDITIONAL PASS — accept nếu dark source hoặc text overlay drives motion")
        sys.exit(0)
    else:
        print("❌ VERDICT: MOTION FAIL — clip có quá nhiều static windows, re-render hoặc thêm motion graphic")
        sys.exit(1)


if __name__ == "__main__":
    main()