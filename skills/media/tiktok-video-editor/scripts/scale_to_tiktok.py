#!/usr/bin/env python3
"""
scale_to_tiktok.py — Scale video về TikTok spec (1080×1920 30fps)
- Pad letterbox nếu source aspect ratio != 9:16
- 30fps (frame rate convert)
- H.264 yuv420p, AAC audio

Usage:
  python3 scale_to_tiktok.py <input.mp4> <output.mp4>
"""
import sys
import subprocess
from pathlib import Path


def probe_video(video_path):
    """Get width, height, fps, sar info"""
    result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=width,height,r_frame_rate,sample_aspect_ratio',
        '-of', 'csv=p=0', str(video_path)
    ], capture_output=True, text=True)
    parts = result.stdout.strip().split(',')
    if len(parts) >= 3:
        w, h = int(parts[0]), int(parts[1])
        fps_str = parts[2]
        sar = parts[3] if len(parts) > 3 else '1:1'
        num, den = (int(x) for x in fps_str.split('/'))
        fps = num / den if den else 30
        return w, h, fps, sar
    return 0, 0, 30, '1:1'


def main():
    if len(sys.argv) != 3:
        print("Usage: scale_to_tiktok.py <input.mp4> <output.mp4>", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"❌ Input not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    w, h, src_fps, sar = probe_video(input_path)
    print(f"Source: {w}×{h} @ {src_fps:.2f}fps (SAR={sar})")

    # Target: 1080×1920 @ 30fps
    # Nếu aspect ratio != 9:16 → pad letterbox
    target_w, target_h = 1080, 1920
    src_ar = w / h if h else 1
    target_ar = target_w / target_h  # 9:16 = 0.5625

    if abs(src_ar - target_ar) < 0.01:
        # Aspect ratio match → just scale
        scale_filter = f"scale={target_w}:{target_h}:flags=lanczos"
    elif src_ar > target_ar:
        # Source rộng hơn (landscape) → letterbox top/bottom
        new_w = int(target_h * src_ar)
        if new_w % 2 != 0:
            new_w += 1
        scale_filter = f"scale={new_w}:{target_h}:flags=lanczos,pad={target_w}:{target_h}:(ow-iw)/2:0:color=black"
    else:
        # Source cao hơn (portrait, narrow) → fit to width
        new_h = int(target_w / src_ar)
        if new_h % 2 != 0:
            new_h += 1
        scale_filter = f"scale={target_w}:{new_h}:flags=lanczos,pad={target_w}:{target_h}:0:(oh-ih)/2:color=black"

    # Force 30fps + h264 yuv420p
    filter_complex = (
        f"[0:v]{scale_filter},fps=30,"
        f"format=yuv420p,setpts=PTS-STARTPTS[v];"
        f"[0:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a]"
    )

    cmd = [
        'ffmpeg', '-y',
        '-i', str(input_path),
        '-filter_complex', filter_complex,
        '-map', '[v]', '-map', '[a]',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
        '-profile:v', 'high', '-level', '4.0',
        '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart',
        str(output_path)
    ]

    print(f"\nFilter: {filter_complex[:100]}...")
    print(f"\n→ Rendering to 1080×1920 30fps...")

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"❌ Render failed", file=sys.stderr)
        print(proc.stderr[-500:], file=sys.stderr)
        sys.exit(1)

    if not output_path.exists():
        print(f"❌ Output not created", file=sys.stderr)
        sys.exit(1)

    sz_mb = round(output_path.stat().st_size / 1024 / 1024, 2)
    print(f"✅ Scaled to TikTok spec: {sz_mb} MB")
    print(f"  Path: {output_path}")


if __name__ == '__main__':
    main()
