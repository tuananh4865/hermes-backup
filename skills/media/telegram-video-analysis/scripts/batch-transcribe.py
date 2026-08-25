#!/usr/bin/env python3
"""Batch compress + Whisper transcribe many Telegram videos at once.

Use when Tuấn Anh sends N>1 video attachments in one batch and wants them
all transcribed. Sequential per-video is reliable; whisper-large-v3-turbo
on Apple Silicon is fast enough (~30s/clip) that parallelism is not worth
the memory pressure.

Usage:
    python3 batch-transcribe.py                  # auto-detect newest N from cache
    python3 batch-transcribe.py --limit 16      # cap to N most recent
    python3 batch-transcribe.py VIDEO_IDS...    # explicit list

Output:
    /tmp/videos-batch-<DATE>/<VIDEO_ID>/compressed.mp4 + compressed.srt

Why this exists:
- Single-video script (analyze-telegram-video.sh) doesn't scale when user
  sends 10-20 videos at once
- Sequential is reliable: mlx-whisper uses MPS memory; parallel calls OOM
- Skip-if-srt-exists makes it idempotent — re-running resumes from where it stopped
"""
import argparse
import subprocess
import sys
from pathlib import Path

CACHE = Path("/Users/tuananh4865/.hermes/cache/videos")


def get_video_candidates(min_size_bytes=1_000_000, hours=24):
    """Get videos from cache modified within last N hours, sorted newest first."""
    import time
    cutoff = time.time() - hours * 3600
    candidates = []
    for f in CACHE.glob("video_*.mp4"):
        if f.stat().st_size >= min_size_bytes and f.stat().st_mtime >= cutoff:
            candidates.append(f)
    return sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)


def get_metadata(path):
    """Return dict with duration, width, height — for log/inspection."""
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error",
             "-show_entries", "format=duration",
             "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-of", "csv=s=x:p=0", str(path)],
            text=True
        )
        # Output: "WIDTHxHEIGHT\nDURATION"
        lines = out.strip().split("\n")
        wh = lines[0] if lines else "?"
        dur = lines[1] if len(lines) > 1 else "?"
        return {"resolution": wh, "duration_s": dur}
    except Exception:
        return {}


def process_video(vid_id, src, out_root):
    """Compress + Whisper for one video. Returns (status, srt_path)."""
    work_dir = out_root / vid_id
    work_dir.mkdir(parents=True, exist_ok=True)
    compressed = work_dir / "compressed.mp4"
    srt = work_dir / "compressed.srt"

    # Skip if SRT already exists (idempotent)
    if srt.exists():
        return "skip-existing", srt

    # Compress
    print(f"[{vid_id}] Compressing {src.name}...")
    if not compressed.exists():
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(src),
                 "-c:v", "libx264", "-preset", "fast", "-crf", "28",
                 "-vf", "scale=-2:720",
                 "-c:a", "aac",
                 str(compressed)],
                capture_output=True, timeout=120
            )
            print(f"[{vid_id}] Done compress: {compressed.stat().st_size} bytes")
        except Exception as e:
            return f"compress-error: {e}", None

    # Whisper
    print(f"[{vid_id}] Whisper...")
    try:
        subprocess.run(
            ["mlx_whisper", str(compressed),
             "--model", "mlx-community/whisper-large-v3-turbo",
             "--language", "vi",
             "--output-dir", str(work_dir),
             "--output-format", "srt"],
            capture_output=True, timeout=300
        )
        if srt.exists():
            print(f"[{vid_id}] Done whisper: {srt.stat().st_size} bytes")
            return "ok", srt
        else:
            return "whisper-error", None
    except Exception as e:
        return f"whisper-error: {e}", None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("videos", nargs="*", help="Explicit video hash IDs (8 chars)")
    parser.add_argument("--limit", type=int, default=20, help="Max videos to process")
    parser.add_argument("--hours", type=int, default=24, help="Look back N hours")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output dir (default /tmp/videos-batch-DATE)")
    args = parser.parse_args()

    # Determine which videos
    if args.videos:
        vids = [CACHE / f"video_{v}.mp4" for v in args.videos]
        vids = [v for v in vids if v.exists()]
    else:
        candidates = get_video_candidates(hours=args.hours)
        vids = candidates[:args.limit]

    if not vids:
        print("❌ No videos found")
        sys.exit(1)

    # Output dir
    from datetime import datetime
    out_root = args.out or Path(f"/tmp/videos-batch-{datetime.now():%Y-%m-%d}")
    out_root.mkdir(parents=True, exist_ok=True)

    print(f"📦 Processing {len(vids)} videos → {out_root}")
    print()

    results = {"ok": 0, "skip-existing": 0, "compress-error": 0, "whisper-error": 0}
    failures = []

    for i, src in enumerate(vids, 1):
        vid_id = src.stem.replace("video_", "")
        meta = get_metadata(src)
        print(f"\n=== [{i}/{len(vids)}] {vid_id} | {meta.get('resolution', '?')} | {meta.get('duration_s', '?')}s ===")
        status, srt_path = process_video(vid_id, src, out_root)
        results[status.split(":")[0]] = results.get(status.split(":")[0], 0) + 1
        if "error" in status:
            failures.append((vid_id, status))

    # Summary
    print("\n" + "=" * 60)
    print(f"✅ DONE: {sum(v for v in results.values())} videos processed")
    print(f"   ok: {results['ok']}")
    print(f"   skip-existing (idempotent): {results['skip-existing']}")
    print(f"   errors: {sum(v for k, v in results.items() if 'error' in k)}")
    print(f"\n📂 Output: {out_root}")

    # Print per-video status for inspection
    print("\n📋 Per-video status:")
    for vid_id_dir in sorted(out_root.iterdir()):
        srt = vid_id_dir / "compressed.srt"
        status = "✓" if srt.exists() else "✗"
        size = srt.stat().st_size if srt.exists() else 0
        print(f"   {status} {vid_id_dir.name} → {size} bytes")

    if failures:
        print("\n❌ Failures:")
        for vid_id, status in failures:
            print(f"   - {vid_id}: {status}")
        sys.exit(1)


if __name__ == "__main__":
    main()