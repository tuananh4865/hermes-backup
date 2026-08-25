#!/usr/bin/env python3
"""Quantitative motion check: % pixels that change between 2 frames at small dt.

Use case: Verify the "no static pixel" rule for animated trailers/clips.
Extracts 2 frames separated by ~0.3s, computes pixel-wise difference, reports
% pixels that changed (threshold = brightness delta > 10/255).

Usage:
    python3 motion_diff_check.py <video.mp4> [--t1 0.3] [--t2 0.6] [--threshold 10]
    python3 motion_diff_check.py <video.mp4> --diff-out /tmp/diff.png

Pass criteria:
    > 30% pixels changed = excellent motion (high animation density)
    15-30% = good motion (active animation)
    5-15%  = weak motion (mostly static, needs more animation)
    <  5%  = appears frozen, animation missing

For trailers with grain/scanline/particles, expect 30-50% at 0.3s intervals.
This is the tool for verifying anh's rule (2026-07-17):
"nếu làm animation thì mọi hình ảnh trên screen đều phải được animation hết
chứ không được có ảnh hoặc chỗ nào tĩnh hết"

Real cases (verified 2026-07-17, 30s trailers @ 1920x1080):
    HyperFrames V1 (basic):       ~22% changed @ 0.3s — basic motion
    HyperFrames V2 (CSS 3D):      ~28% — improved but still static sections
    HyperFrames V3 (master rAF):  ~41% — every-pixel-animates pass
    HyperFrames V4 (Three.js):   ~38% — 3D meshes have static inter-frame pixels
"""
import argparse
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageChops


def extract_frame(video: str, t: float, out_path: str, size: int = 360) -> str:
    """Extract a single frame at timestamp t, scaled to size×size for fast diff."""
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', video,
           '-frames:v', '1', '-vf', f'scale={size}:-1', out_path]
    subprocess.run(cmd, check=True)
    return out_path


def pixel_diff_pct(p1: str, p2: str, threshold: int = 10) -> tuple:
    """Return (total_px, changed_px, pct)."""
    a = np.array(Image.open(p1).convert('RGB'))
    b = np.array(Image.open(p2).convert('RGB'))
    if a.shape != b.shape:
        h = min(a.shape[0], b.shape[0])
        w = min(a.shape[1], b.shape[1])
        a = a[:h, :w]
        b = b[:h, :w]
    delta = np.abs(a.astype(int) - b.astype(int)).sum(axis=-1)
    changed = int((delta > threshold).sum())
    total = int(a.shape[0] * a.shape[1])
    return total, changed, changed / total * 100


def verdict(avg_pct: float) -> tuple:
    """Return (status_label, exit_code)."""
    if avg_pct > 30:
        return ('✅ EXCELLENT motion', 0)
    elif avg_pct > 15:
        return ('✅ GOOD motion', 0)
    elif avg_pct > 5:
        return ('⚠️  WEAK motion', 0)
    else:
        return ('❌ NO motion (frozen)', 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video', help='Path to MP4 to check')
    ap.add_argument('--t1', type=float, default=0.0,
                    help='First frame timestamp (default 0.0)')
    ap.add_argument('--t2', type=float, default=0.3,
                    help='Second frame timestamp (default 0.3)')
    ap.add_argument('--t3', type=float, default=0.6,
                    help='Third frame timestamp (default 0.6, 0 disables)')
    ap.add_argument('--threshold', type=int, default=10,
                    help='Brightness delta threshold 0-255 (default 10)')
    ap.add_argument('--size', type=int, default=360,
                    help='Frame size for diff (default 360)')
    ap.add_argument('--diff-out', help='Save amplified diff image to this path')
    args = ap.parse_args()

    if not os.path.exists(args.video):
        sys.exit(f'Video not found: {args.video}')

    out_dir = '/tmp/motion_diff_frames'
    os.makedirs(out_dir, exist_ok=True)
    p1 = extract_frame(args.video, args.t1, f'{out_dir}/f1.jpg', args.size)
    p2 = extract_frame(args.video, args.t2, f'{out_dir}/f2.jpg', args.size)
    p3 = None
    if args.t3 and args.t3 > 0:
        p3 = extract_frame(args.video, args.t3, f'{out_dir}/f3.jpg', args.size)

    total, changed, pct = pixel_diff_pct(p1, p2, args.threshold)
    print(f'At {args.t2}s vs {args.t1}s: {changed}/{total} pixels changed ({pct:.1f}%)')

    pct3 = None
    if p3:
        _, changed3, pct3 = pixel_diff_pct(p2, p3, args.threshold)
        print(f'At {args.t3}s vs {args.t2}s: {changed3}/{total} pixels changed ({pct3:.1f}%)')
        avg = (pct + pct3) / 2
    else:
        avg = pct
    print(f'Average: {avg:.1f}%')

    if args.diff_out:
        a = Image.open(p1).convert('RGB')
        b = Image.open(p2).convert('RGB')
        diff = ImageChops.difference(a, b)
        # Amplify diff for visibility (4x brightness)
        diff_arr = np.array(diff).astype(int) * 4
        diff_arr = np.clip(diff_arr, 0, 255).astype(np.uint8)
        Image.fromarray(diff_arr).save(args.diff_out)
        print(f'Saved diff: {args.diff_out}')

    print()
    status, code = verdict(avg)
    print(status)
    sys.exit(code)


if __name__ == '__main__':
    main()
