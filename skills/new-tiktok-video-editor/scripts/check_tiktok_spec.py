#!/usr/bin/env python3
"""
check_tiktok_spec.py — Verify output đạt TikTok spec
- 1080×1920 (TikTok portrait)
- 30fps
- H.264 high profile
- AAC audio

Usage:
  python3 check_tiktok_spec.py <video.mp4>
"""
import sys
import subprocess
import json
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: check_tiktok_spec.py <video.mp4>", file=sys.stderr)
        sys.exit(1)

    video = Path(sys.argv[1])
    if not video.exists():
        print(f"❌ Video not found: {video}", file=sys.stderr)
        sys.exit(1)

    # ffprobe
    result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=index,codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels,profile',
        '-of', 'json', str(video)
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ ffprobe failed", file=sys.stderr)
        sys.exit(1)

    data = json.loads(result.stdout)
    streams = data.get('streams', [])

    video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
    audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), {})

    # Get duration
    fmt_result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0', str(video)
    ], capture_output=True, text=True)
    duration = float(fmt_result.stdout.strip()) if fmt_result.stdout.strip() else 0

    # Check spec
    width = int(video_stream.get('width', 0))
    height = int(video_stream.get('height', 0))
    fps_str = video_stream.get('r_frame_rate', '0/1')
    fps_num, fps_den = (int(x) for x in fps_str.split('/'))
    fps = fps_num / fps_den if fps_den else 0
    vcodec = video_stream.get('codec_name', '')
    pix = video_stream.get('pix_fmt', '')
    profile = video_stream.get('profile', '')

    acodec = audio_stream.get('codec_name', '')
    sample_rate = int(audio_stream.get('sample_rate', 0))

    failures = []

    print(f"═══ TIKTOK SPEC CHECK ═══")
    print(f"  Width × Height: {width}×{height}")
    print(f"  Frame rate: {fps:.2f} fps ({fps_str})")
    print(f"  Video codec: {vcodec} (profile: {profile})")
    print(f"  Pixel format: {pix}")
    print(f"  Audio codec: {acodec} @ {sample_rate}Hz")
    print(f"  Duration: {duration:.2f}s")
    print()

    if width != 1080:
        failures.append(f"width={width} (expected 1080)")
    if height != 1920:
        failures.append(f"height={height} (expected 1920)")
    if abs(fps - 30) > 0.5:
        failures.append(f"fps={fps:.2f} (expected 30)")
    if vcodec != 'h264':
        failures.append(f"codec={vcodec} (expected h264)")
    if pix != 'yuv420p':
        failures.append(f"pix_fmt={pix} (expected yuv420p)")
    if acodec != 'aac':
        failures.append(f"audio_codec={acodec} (expected aac)")

    if failures:
        print(f"❌ SPEC MISMATCH:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"✅ ALL PASS — TikTok spec: 1080×1920 30fps h264 aac")
        sys.exit(0)


if __name__ == '__main__':
    main()
