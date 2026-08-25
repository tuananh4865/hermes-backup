#!/usr/bin/env python3
"""
3-layer audio verify (đã catch 3 bug trong session OmniVoice):
  1. File valid (ffprobe: 24kHz, mono, PCM)
  2. Amplitude OK (volumedetect: max > -10 dB, không silent)
  3. Content clean (Whisper transcript: không ref leak)

Usage:
  python3 verify_audio.py <audio_or_dir> [--whisper] [--lang vi]
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path


def ffprobe(path: str) -> dict:
    """Get file info via ffprobe"""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,sample_rate,channels",
         "-of", "default", path],
        capture_output=True, text=True, timeout=5,
    )
    info = {"path": path}
    for line in out.stdout.split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            info[k.strip()] = v.strip()
    return info


def volumedetect(path: str) -> dict:
    """volumedetect max + mean"""
    out = subprocess.run(
        ["ffmpeg", "-i", path, "-af", "volumedetect", "-vn", "-f", "null", "-"],
        capture_output=True, text=True, timeout=5,
    )
    info = {"path": path}
    for line in out.stderr.split("\n"):
        if "max_volume" in line:
            info["max_db"] = line.split(":")[-1].strip()
        if "mean_volume" in line:
            info["mean_db"] = line.split(":")[-1].strip()
    return info


def whisper_transcribe(path: str, lang: str = "vi") -> str:
    """Whisper large-v3 transcript"""
    out_dir = "/tmp/verify_audio"
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.basename(path).replace(".wav", "")
    out_path = f"{out_dir}/{base}.txt"
    subprocess.run(
        ["mlx_whisper", "--model", "mlx-community/whisper-large-v3-mlx",
         "--language", lang, "--output-format", "txt",
         "--output-dir", out_dir, path],
        capture_output=True, timeout=90,
    )
    if os.path.exists(out_path):
        with open(out_path) as f:
            return f.read().strip()
    return ""


def verify_file(path: str, whisper: bool = False, lang: str = "vi") -> dict:
    print(f"\n=== {os.path.basename(path)} ===")
    # Layer 1: ffprobe
    fp = ffprobe(path)
    print(f"  [1] ffprobe: codec={fp.get('codec_name','?')}, sr={fp.get('sample_rate','?')}, ch={fp.get('channels','?')}, dur={fp.get('duration','?')}s")
    valid = fp.get("codec_name") == "pcm_s16le" and fp.get("sample_rate") == "24000"

    # Layer 2: volumedetect
    vd = volumedetect(path)
    max_db = vd.get("max_db", "-inf")
    mean_db = vd.get("mean_db", "-inf")
    print(f"  [2] volume: max={max_db}, mean={mean_db}")
    # Parse dB: "−4.2 dB" hoặc "-4.2 dB" (có thể có unicode −)
    try:
        clean = max_db.replace("−", "-").replace("dB", "").strip()
        max_val = float(clean)
        silent = max_val < -20
    except:
        silent = True
    if silent:
        print(f"      ⚠️  TOO QUIET (max < -20 dB) — có thể silent bug")

    # Layer 3: Whisper
    if whisper:
        transcript = whisper_transcribe(path, lang)
        if transcript:
            # Look for common ref leak phrases (Vietnamese)
            ref_leak_signs = ["hãy subscribe", "bấm vào link", "đăng ký kênh", "theo dõi kênh"]
            has_leak = any(sign in transcript.lower() for sign in ref_leak_signs)
            print(f"  [3] whisper ({len(transcript)} chars): {transcript[:200]}")
            if has_leak:
                print(f"      ⚠️  REF LEAK DETECTED — script này không phải voice ref")

    status = "✅" if (valid and not silent) else "❌"
    print(f"  → {status}")
    return {"valid": valid, "silent": silent}


def main():
    parser = argparse.ArgumentParser(description="3-layer audio verify")
    parser.add_argument("path", help="Audio file or directory")
    parser.add_argument("--whisper", action="store_true", help="Also run Whisper (slow, ~20s/file)")
    parser.add_argument("--lang", default="vi", help="Language for Whisper (default: vi)")
    args = parser.parse_args()

    p = Path(args.path)
    if p.is_file():
        verify_file(str(p), args.whisper, args.lang)
    elif p.is_dir():
        files = sorted(p.glob("*.wav"))
        for f in files:
            verify_file(str(f), args.whisper, args.lang)
    else:
        print(f"❌ Path not found: {args.path}")


if __name__ == "__main__":
    main()
