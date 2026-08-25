#!/usr/bin/env python3
"""
edge_tts_vietnamese.py — Tạo audio tiếng Việt bằng Edge TTS

Dùng khi Whisper transcript sai về sản phẩm → cần audio mới với nội dung đúng.

Usage:
    python scripts/edge_tts_vietnamese.py --script "script.txt" --output audio.mp3
    python scripts/edge_tts_vietnamese.py --text "Text trực tiếp" --output audio.mp3

Voices Vietnamese:
    - vi-VN-HoaiMyNeural (female, recommended)
    - vi-VN-NamMinhNeural (male)

Recipe atempo stretch (khi audio ngắn/dài hơn video):
    # Audio 61s, video 85s → atempo = 61/85 = 0.719
    ffmpeg -y -i audio_v2.mp3 -filter:a "atempo=0.719" -c:a aac -b:a 128k audio.aac
"""

import argparse
import asyncio
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("❌ edge_tts not installed. Run: pip install edge-tts")
    sys.exit(1)


VOICES = {
    "hoai-my": "vi-VN-HoaiMyNeural",      # female (recommended)
    "nam-minh": "vi-VN-NamMinhNeural",   # male
}


async def generate_tts(text: str, voice: str, rate: str, output_path: Path):
    """Generate Vietnamese TTS audio using Edge TTS."""
    print(f"🎤 Edge TTS")
    print(f"   Voice: {voice}")
    print(f"   Rate: {rate}")
    print(f"   Output: {output_path}")
    print(f"   Text length: {len(text)} chars, {len(text.split())} words")

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))

    if output_path.exists():
        size = output_path.stat().st_size
        print(f"✅ Audio generated: {size/1024:.0f} KB")

        # Get duration
        import subprocess
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1", str(output_path)],
            capture_output=True, text=True, timeout=10
        )
        duration = result.stdout.strip().replace("duration=", "")
        print(f"   Duration: {duration}s")
    else:
        print(f"❌ Audio not generated")
        sys.exit(1)


async def atempo_stretch(input_path: Path, output_path: Path, target_duration: float):
    """Stretch audio to target duration using atempo filter."""
    import subprocess
    import re

    # Get input duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1", str(input_path)],
        capture_output=True, text=True, timeout=10
    )
    m = re.search(r'(\d+\.\d+)', result.stdout)
    input_duration = float(m.group(1)) if m else 0
    atempo = input_duration / target_duration

    print(f"🔄 Stretching audio")
    print(f"   Input: {input_duration:.2f}s")
    print(f"   Target: {target_duration:.2f}s")
    print(f"   Atempo: {atempo:.3f}")

    if atempo > 2.0 or atempo < 0.5:
        # Need 2 atempos
        atempo1 = max(0.5, min(2.0, atempo))
        atempo2 = atempo / atempo1
        filter_str = f"atempo={atempo1:.3f},atempo={atempo2:.3f}"
    else:
        filter_str = f"atempo={atempo:.3f}"

    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-filter:a", filter_str,
        "-c:a", "aac", "-b:a", "128k",
        str(output_path)
    ]
    subprocess.run(cmd, capture_output=True, timeout=30)

    if output_path.exists():
        # Verify
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1", str(output_path)],
            capture_output=True, text=True, timeout=10
        )
        final_duration = result.stdout.strip().replace("duration=", "")
        print(f"✅ Stretched audio: {final_duration}s")
    else:
        print(f"❌ Stretch failed")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Vietnamese TTS audio via Edge TTS (used when Whisper transcript is wrong)"
    )
    parser.add_argument("--text", help="Text to speak directly")
    parser.add_argument("--script", help="Path to .txt file with script (preferred for long scripts)")
    parser.add_argument("--output", "-o", required=True, help="Output .mp3 file path")
    parser.add_argument("--voice", choices=VOICES.keys(), default="hoai-my",
                        help="Vietnamese voice (default: hoai-my female)")
    parser.add_argument("--rate", default="-10%",
                        help="Speech rate (e.g. -10%% slower, +10%% faster, default: -10%%)")
    parser.add_argument("--stretch-to", type=float,
                        help="Stretch audio to target duration (e.g. 85.0 for 85s video)")

    args = parser.parse_args()

    # Get text
    if args.script:
        script_path = Path(args.script)
        if not script_path.exists():
            print(f"❌ Script file not found: {script_path}")
            sys.exit(1)
        text = script_path.read_text(encoding="utf-8").strip()
        print(f"📝 Loaded script from: {script_path}")
    elif args.text:
        text = args.text
    else:
        print("❌ Provide --text or --script")
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate TTS
    voice = VOICES[args.voice]
    asyncio.run(generate_tts(text, voice, args.rate, output_path))

    # Stretch if requested
    if args.stretch_to:
        stretched_path = output_path.with_name(f"{output_path.stem}_stretched.mp3")
        asyncio.run(atempo_stretch(output_path, stretched_path, args.stretch_to))


if __name__ == "__main__":
    main()
