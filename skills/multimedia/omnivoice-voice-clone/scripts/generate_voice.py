#!/usr/bin/env python3
"""
Generate voice từ file voice clone (.pt) + text có emotion tags.

Workflow ĐƠN GIẢN — chỉ cần 2 thứ:
  1. --prompt: file voice clone .pt đã save
  2. --text: target text (kèm emotion tags)

Auto-trim trailing silence >10ms để concat mượt (verified 24/07).
"""
import sys
import os
import json
import argparse
import subprocess
from pathlib import Path


def find_venv_python():
    candidates = [
        "/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python",
        os.path.expanduser("~/.hermes/.venv/bin/python"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return sys.executable


def trim_trailing_silence(path: str, threshold: float = 0.001) -> float:
    """Trim trailing silence >10ms. Returns new duration."""
    try:
        import soundfile as sf
        import numpy as np
        audio, sr = sf.read(path)
        abs_audio = np.abs(audio)
        n = len(audio)
        # Find last active sample
        last_active = n
        for i in range(n - 1, -1, -1):
            if abs_audio[i] > threshold:
                last_active = i + 1
                break
        # Trim 240 samples (10ms at 24kHz) sau last_active
        trim_to = min(last_active + 240, n)
        if trim_to < n - int(0.01 * sr):  # Chỉ trim nếu >10ms silent
            trimmed = audio[:trim_to]
            sf.write(path, trimmed, sr)
            return len(trimmed) / sr
    except Exception as e:
        print(f"  ⚠️ trim_trailing_silence failed: {e}")
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
    parser = argparse.ArgumentParser(description="Generate voice từ file voice clone + text có emotion tags")
    parser.add_argument("--prompt", required=True, help="File voice clone .pt (đã save)")
    parser.add_argument("--text", help="Target text (kèm emotion tags)")
    parser.add_argument("--output", help="Output WAV file")
    parser.add_argument("--jsonl", help="JSONL input file (batch mode)")
    parser.add_argument("--output-dir", help="Output directory (batch mode)")
    args = parser.parse_args()

    if not args.text and not args.jsonl:
        parser.error("Cần --text HOẶC --jsonl")

    python = find_venv_python()

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
print(f"Voice clone: ref_rms={{prompt.ref_rms:.4f}}", flush=True)

gc = OmniVoiceGenerationConfig(
    pad_duration=0.0,
    fade_duration=0.0,
    denoise=True,
    layer_penalty_factor=1.0,
    position_temperature=3.0,
)
SPEED = 0.95
'''

    if args.text:
        code += f'''
audio = model.generate(
    text={json.dumps(args.text)},
    language="vi",
    voice_clone_prompt=prompt,
    generation_config=gc,
    speed=SPEED,
)[0]
sf.write("{args.output}", audio, model.sampling_rate)
print(f"✅ Saved → {args.output}")
'''
    else:
        jsonl_path = os.path.abspath(args.jsonl)
        output_dir = os.path.abspath(args.output_dir)
        code += f'''
os.makedirs("{output_dir}", exist_ok=True)
with open("{jsonl_path}") as f:
    samples = [json.loads(line) for line in f if line.strip()]
print(f"\\nGenerating {{len(samples)}} files...", flush=True)
for i, s in enumerate(samples, 1):
    sid = s["id"]
    text = s["text"]
    lang = s.get("language", "vi")
    out = os.path.join("{output_dir}", f"{{sid}}.wav")
    t0 = time.time()
    audio = model.generate(
        text=text,
        language=lang,
        voice_clone_prompt=prompt,
        generation_config=gc,
        speed=SPEED,
    )[0]
    dt = time.time() - t0
    sf.write(out, audio, model.sampling_rate)
    peak = float(np.abs(audio).max())
    dur = len(audio) / model.sampling_rate
    status = "✅" if peak > 0.3 else "⚠️"
    print(f"  [{{i}}/{{len(samples)}}] {{sid}}: {{dur:.1f}}s peak={{peak:.3f}} {{status}}", flush=True)
'''

    subprocess.run([python, "-c", code])

    # Auto-trim trailing silence (verified 24/07 fix nghe "mờ đầu/cuối")
    print("\n=== Auto-trim trailing silence ===")
    files = []
    if args.text:
        files = [args.output]
    else:
        files = sorted([os.path.join(args.output_dir, f) for f in os.listdir(args.output_dir) if f.endswith(".wav")])

    for f in files:
        new_dur = trim_trailing_silence(f)
        if new_dur > 0:
            print(f"  ✂️ {os.path.basename(f)} trimmed → {new_dur:.2f}s")

    # POST-VERIFY
    print("\n=== POST-VERIFY ===")
    for f in files:
        vol = ffprobe_volume(f)
        print(f"  {os.path.basename(f)}: {vol}")


if __name__ == "__main__":
    main()
