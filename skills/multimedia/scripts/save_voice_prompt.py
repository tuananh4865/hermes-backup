#!/usr/bin/env python3
"""
Save OmniVoice VoiceClonePrompt từ ref audio → file .pt
Encode 1 lần, dùng mãi mãi (skip Whisper + audio encode mỗi session).

Usage:
  python3 save_voice_prompt.py save <ref_audio> "<ref text 1 câu>" <output_pt>
  python3 save_voice_prompt.py info <prompt_pt>

Critical rules (PITFALLS):
  - ref_text phải NGẮN (~100 chars, 1 câu) → tránh ref leak
  - ref audio phải có ref_rms >= 0.1 → nếu < 0.1, amplify trước
"""
import sys
import os
import time
import argparse
import torch  # noqa: F401  (always import, even for info-only)


def save(ref_audio: str, ref_text: str, output_pt: str):
    from omnivoice.models.omnivoice import OmniVoice

    print(f"Loading model (1st time: ~1:30, cached: ~2s)...", flush=True)
    t0 = time.time()
    model = OmniVoice.from_pretrained(
        "k2-fsa/OmniVoice",
        device_map="mps",
        dtype=torch.float16,
    )
    print(f"Model loaded in {time.time()-t0:.1f}s", flush=True)

    print(f"\nCreating voice clone prompt from: {ref_audio}", flush=True)
    print(f"ref_text ({len(ref_text)} chars): {ref_text[:80]}...", flush=True)

    t0 = time.time()
    prompt = model.create_voice_clone_prompt(
        ref_audio=ref_audio,
        ref_text=ref_text,
        preprocess_prompt=True,
    )
    print(f"Prompt created in {time.time()-t0:.1f}s", flush=True)
    print(f"  ref_rms: {prompt.ref_rms:.4f}", flush=True)
    if prompt.ref_rms < 0.1:
        print(f"  ⚠️  ref_rms < 0.1 → amplitude bug có thể xảy ra (PITFALL #2)", flush=True)
        print(f"  Suggest: amplify ref audio trước khi save (xem SKILL.md Phase 2)", flush=True)
    print(f"  ref_audio_tokens shape: {prompt.ref_audio_tokens.shape}", flush=True)

    os.makedirs(os.path.dirname(output_pt) or ".", exist_ok=True)
    prompt.save(output_pt)
    size = os.path.getsize(output_pt)
    print(f"\n✅ Saved {output_pt}", flush=True)
    print(f"   Size: {size} bytes ({size/1024:.1f}KB)", flush=True)
    print(f"\nDùng: model.generate(text=..., voice_clone_prompt=VoiceClonePrompt.load('{output_pt}'))", flush=True)


def info(prompt_pt: str):
    from omnivoice.models.omnivoice import VoiceClonePrompt

    p = VoiceClonePrompt.load(prompt_pt)
    print(f"Prompt file: {prompt_pt}")
    print(f"  ref_rms: {p.ref_rms:.4f}")
    if p.ref_rms < 0.1:
        print(f"  ⚠️  ref_rms < 0.1 (PITFALL #2)")
    print(f"  ref_audio_tokens shape: {p.ref_audio_tokens.shape}")
    print(f"  ref_text ({len(p.ref_text)} chars): {p.ref_text[:100]}...")
    if len(p.ref_text) > 120:
        print(f"  ⚠️  ref_text > 120 chars → có thể leak vào output (PITFALL #3)")


def main():
    parser = argparse.ArgumentParser(description="Save/inspect OmniVoice voice clone prompt")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_save = sub.add_parser("save", help="Encode ref audio → save .pt")
    p_save.add_argument("ref_audio", help="Path to ref audio (5-10s WAV/MP3/M4A/OGG)")
    p_save.add_argument("ref_text", help="Transcript of ref audio (NGẮN: 1 câu, ~100 chars)")
    p_save.add_argument("output_pt", help="Output .pt file path")

    p_info = sub.add_parser("info", help="Show info about existing .pt")
    p_info.add_argument("prompt_pt", help="Path to .pt file")

    args = parser.parse_args()

    if args.cmd == "save":
        save(args.ref_audio, args.ref_text, args.output_pt)
    elif args.cmd == "info":
        info(args.prompt_pt)


if __name__ == "__main__":
    main()
