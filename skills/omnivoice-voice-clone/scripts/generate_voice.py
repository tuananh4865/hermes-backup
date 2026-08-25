#!/usr/bin/env python3
"""
Generate audio từ text dùng OmniVoice + VoiceClonePrompt.
Skip Whisper + audio encode mỗi lần (5x speedup vs re-encode).

DEFAULT: pad_duration=0, fade_duration=0 (NO padding/fade để concat mượt)

Usage:
  # Single
  python3 generate_voice.py --prompt <pt> --text "..." --output out.wav

  # Batch
  python3 generate_voice.py --prompt <pt> --jsonl inputs.jsonl --output-dir batch_results/

JSONL schema (mỗi line 1 sample):
  {"id": "sample_001", "text": "...", "language": "vi", "emotion_tags": false}
"""
import sys
import os
import time
import json
import argparse
import subprocess
from pathlib import Path


def find_venv_python():
    """Tìm OmniVoice venv theo convention"""
    candidates = [
        "/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python",
        os.path.expanduser("~/.hermes/.venv/bin/python"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return sys.executable


def ffprobe_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, timeout=5,
    )
    try:
        return float(out.stdout.strip())
    except Exception:
        return 0.0


def ffprobe_volume(path: str) -> dict:
    out = subprocess.run(
        ["ffmpeg", "-i", path, "-af", "volumedetect", "-vn", "-f", "null", "-"],
        capture_output=True, text=True, timeout=5,
    )
    info = {}
    for line in out.stderr.split("\n"):
        if "max_volume" in line:
            info["max"] = line.split(":")[-1].strip()
        if "mean_volume" in line:
            info["mean"] = line.split(":")[-1].strip()
    return info


def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio từ text dùng OmniVoice")
    parser.add_argument("--prompt", required=True, help="Path to .pt voice clone prompt")
    parser.add_argument("--text", help="Single text to synthesize")
    parser.add_argument("--output", help="Output WAV file (for --text mode)")
    parser.add_argument("--jsonl", help="JSONL input file (batch mode)")
    parser.add_argument("--output-dir", help="Output directory (for --jsonl mode)")
    parser.add_argument("--no-verify", action="store_true", help="Skip volumedetect verify")
    parser.add_argument("--with-padding", action="store_true",
                        help="Enable 100ms padding (default: NO padding)")
    args = parser.parse_args()

    if not args.text and not args.jsonl:
        parser.error("Need either --text or --jsonl")

    python = find_venv_python()
    print(f"Using Python: {python}", file=sys.stderr, flush=True)

    # Build code
    pad_duration = "0.0" if not args.with_padding else "0.1"
    fade_duration = "0.0" if not args.with_padding else "0.1"

    code = f'''
import sys, json, time, torch, os
import numpy as np, soundfile as sf
sys.path.insert(0, "/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/lib/python3.11/site-packages")
from omnivoice import OmniVoice, VoiceClonePrompt, OmniVoiceGenerationConfig

print("Loading model...", flush=True)
t0 = time.time()
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
print(f"Model loaded in {{time.time()-t0:.1f}}s", flush=True)

prompt = VoiceClonePrompt.load("{args.prompt}")
print(f"Prompt: ref_rms={{prompt.ref_rms:.4f}}", flush=True)

gc = OmniVoiceGenerationConfig(
    pad_duration=0.15,
    fade_duration=0.02,
    denoise=True,
    layer_penalty_factor=2.0,
    position_temperature=2.5,
)
print(f"Generation: pad_duration={{gc.pad_duration}}, fade_duration={{gc.fade_duration}}", flush=True)

def trim_trailing_silence(audio, sr, threshold=0.001):
    abs_audio = np.abs(audio)
    active = np.flatnonzero(abs_audio > threshold)
    if active.size == 0:
        return audio
    keep_to = min(int(active[-1]) + 1 + int(0.01 * sr), len(audio))
    return audio[:keep_to]
'''

    if args.text:
        output = args.output
        code += f'''
audio = model.generate(text={json.dumps(args.text)}, language="vi", voice_clone_prompt=prompt, generation_config=gc, speed=0.90)[0]
audio = trim_trailing_silence(audio, model.sampling_rate)
sf.write("{output}", audio, model.sampling_rate)
print(f"✅ Saved {{os.path.getsize('{output}')}} bytes → {output}")
import os
'''
    else:
        jsonl_path = os.path.abspath(args.jsonl)
        output_dir = os.path.abspath(args.output_dir)
        os.makedirs(output_dir, exist_ok=True)
        code += f'''
import json, os
with open("{jsonl_path}") as f:
    samples = [json.loads(line) for line in f if line.strip()]

print(f"\\nGenerating {{len(samples)}} files → {output_dir}/", flush=True)
for i, s in enumerate(samples, 1):
    sid = s["id"]
    text = s["text"]
    lang = s.get("language", "vi")
    out = os.path.join("{output_dir}", f"{{sid}}.wav")
    t0 = time.time()
    audio = model.generate(text=text, language="vi", voice_clone_prompt=prompt, generation_config=gc, speed=0.90)[0]
    audio = trim_trailing_silence(audio, model.sampling_rate)
    dt = time.time() - t0
    peak = float(np.abs(audio).max())
    dur = len(audio) / model.sampling_rate
    sf.write(out, audio, model.sampling_rate)
    status = "✅" if peak > 0.3 else "⚠️"
    print(f"  [{{i}}/{{len(samples)}}] {{sid}}: {{dur:.1f}}s peak={{peak:.3f}} t={{dt:.1f}}s {{status}}", flush=True)
'''

    result = subprocess.run([python, "-c", code], capture_output=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    if not args.no_verify:
        print("\n=== POST-VERIFY ===", file=sys.stderr)
        if args.text:
            vol = ffprobe_volume(args.output)
            print(f"  {args.output}: {vol}", file=sys.stderr)
        else:
            for fname in sorted(os.listdir(args.output_dir)):
                if fname.endswith(".wav"):
                    p = os.path.join(args.output_dir, fname)
                    vol = ffprobe_volume(p)
                    print(f"  {fname}: {vol}", file=sys.stderr)


if __name__ == "__main__":
    main()
