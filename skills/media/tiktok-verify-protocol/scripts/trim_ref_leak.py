#!/usr/bin/env python3
"""
trim_ref_leak.py — Tự động trim ref-text leak khỏi TTS voice-clone output.

PITFALL #96: TTS output voice-clone (OmniVoice, ElevenLabs, F5-TTS, ...) thường
inject câu cuối ref text vào đầu/giữa generated audio. Container + amplitude
(PITFALL #95) check KHÔNG catch được — phải dùng Whisper word-level.

Recipe:
1. Chạy Whisper word-level timestamps trên mỗi file output
2. Detect word đầu tiên KHÔNG thuộc REF_PHRASES
3. Trim leading audio từ 0s đến đó (margin 0.15s)
4. Save file mới `*_trim.wav`

Usage:
    # Single file
    python3 trim_ref_leak.py path/to/output.wav

    # Folder (auto-process all .wav)
    python3 trim_ref_leak.py path/to/folder/

    # Custom REF_PHRASES (nếu ref audio khác)
    python3 trim_ref_leak.py folder/ --ref-text "câu transcript của ref audio"

Output: same folder/ hoặc alongside source, file mới có suffix `_trim.wav`.

Real case 23/07/2026 — OmniVoice sequential 5 (HOOK→PROBLEM→SOLUTION→USP→CTA):
- Input 5 file, total 38.80s
- Output 5 file_trim, total 26.13s
- Saved 12.67s ref leak
- All 5 file content clean (no ref words leak)
"""

import argparse
import os
import sys
import json
import subprocess
import glob
from pathlib import Path

# Default ref phrases — câu thường gặp ở đầu ref audio Tiếng Việt voice-clone
# (Nếu ref audio khác, override bằng --ref-text hoặc sửa list này)
DEFAULT_REF_PHRASES = [
    "xin chào", "đây là giọng", "giọng đọc của", "giọng nói của",
    "tôi năm nay", "năm nay", "tuổi đang",
    "và bây giờ", "bây giờ đang", "giờ đang",
    "đang nhờ", "nhờ ai", "nhờ a i",
    "làm kịch bản", "kịch bản cho tôi",
    "đang thất nghiệp", "thất nghiệp",
    "mình tên là", "tôi tên là",
    "chào các bạn", "các bạn ơi", "hello",
]

TRIM_MARGIN_S = 0.15  # giữ 150ms trước first real word (tránh cắt mất âm đầu)


def build_ref_words(ref_phrases):
    """Build set of ref words từ phrases."""
    ref_words = set()
    for p in ref_phrases:
        for w in p.lower().split():
            ref_words.add(w)
    return ref_words


def is_ref_word(word, ref_words):
    """Check word có thuộc ref set không (lowercase, no punct)."""
    wl = word.lower().strip(".,!?;:\"'()[]{}…")
    return wl in ref_words


def get_first_real_word_start(wav_path, ref_words, mlx_whisper_path="mlx_whisper",
                              model="mlx-community/whisper-large-v3-mlx",
                              language="vi"):
    """Whisper word-level → first non-ref word's start time (with margin)."""
    out_dir = "/tmp/trim_ref_leak_whisper/"
    os.makedirs(out_dir, exist_ok=True)
    base = Path(wav_path).stem

    cmd = [
        mlx_whisper_path, "--model", model,
        "--language", language,
        "--output-format", "json",
        "--output-dir", out_dir,
        "--word-timestamps", "True",
        wav_path,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Whisper timeout for {wav_path}")
        return 0
    except FileNotFoundError:
        print(f"  ❌ mlx_whisper not found: {mlx_whisper_path}")
        print(f"     Install: pip install mlx-whisper (Apple Silicon)")
        return 0

    json_path = os.path.join(out_dir, f"{base}.json")
    if not os.path.exists(json_path):
        print(f"  ⚠️  Whisper JSON not found: {json_path}")
        return 0

    with open(json_path) as f:
        data = json.load(f)

    # Find first non-ref word
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            wt = w.get("word", "").strip()
            if not wt:
                continue
            if not is_ref_word(wt, ref_words):
                start = w.get("start", 0)
                return max(0, start - TRIM_MARGIN_S)

    # Fallback: no ref word found → don't trim
    return 0


def trim_wav(in_path, out_path, trim_start):
    """Trim audio từ `trim_start` seconds. Returns new duration."""
    import soundfile as sf
    audio, sr = sf.read(in_path)
    if audio.ndim > 1:
        audio = audio[:, 0]  # mono if stereo
    start_sample = int(trim_start * sr)
    if start_sample >= len(audio):
        return 0.0
    trimmed = audio[start_sample:]
    sf.write(out_path, trimmed, sr)
    return len(trimmed) / sr


def process_file(wav_path, ref_words, verbose=True):
    """Process 1 file. Returns (trim_start, new_duration, original_duration)."""
    if verbose:
        print(f"  Processing: {os.path.basename(wav_path)}")

    import soundfile as sf
    orig_dur = sf.info(wav_path).duration
    trim_start = get_first_real_word_start(wav_path, ref_words)

    out_path = str(wav_path).replace(".wav", "_trim.wav")
    if out_path == str(wav_path):
        out_path = str(wav_path) + "_trim"

    new_dur = trim_wav(wav_path, out_path, trim_start)
    return trim_start, new_dur, orig_dur, out_path


def main():
    parser = argparse.ArgumentParser(
        description="Trim ref-text leak từ TTS voice-clone output (PITFALL #96)."
    )
    parser.add_argument("input", help="Input .wav file hoặc folder chứa .wav files")
    parser.add_argument(
        "--ref-text", type=str, default=None,
        help="Optional: ref text thực tế (auto-extract REF_PHRASES)"
    )
    parser.add_argument(
        "--ref-phrases", type=str, default=None,
        help="Optional: comma-separated list ref phrases (override default)"
    )
    parser.add_argument(
        "--model", default="mlx-community/whisper-large-v3-mlx",
        help="Whisper model (default: large-v3)"
    )
    parser.add_argument(
        "--language", default="vi",
        help="Language code (default: vi)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Chỉ phân tích, KHÔNG ghi file"
    )

    args = parser.parse_args()

    # Build ref_words
    if args.ref_phrases:
        ref_phrases = [p.strip() for p in args.ref_phrases.split(",")]
        print(f"Using custom REF_PHRASES: {ref_phrases[:5]}...")
    elif args.ref_text:
        # Auto-extract: split text thành bigrams + unigrams
        import re
        words = re.findall(r"\w+", args.ref_text.lower())
        ref_phrases = [" ".join(words[i:i+2]) for i in range(len(words)-1)]
        ref_phrases += words  # unigrams
        print(f"Auto-extracted {len(ref_phrases)} REF_PHRASES từ ref_text")
    else:
        ref_phrases = DEFAULT_REF_PHRASES
        print(f"Using DEFAULT REF_PHRASES ({len(ref_phrases)} phrases)")

    ref_words = build_ref_words(ref_phrases)
    print(f"Built REF_WORDS set: {len(ref_words)} unique words")

    # Collect files
    input_path = Path(args.input)
    if input_path.is_file():
        files = [str(input_path)]
    elif input_path.is_dir():
        files = sorted(glob.glob(os.path.join(str(input_path), "*.wav")))
        # Exclude already-trimmed files
        files = [f for f in files if "_trim.wav" not in f]
    else:
        print(f"❌ Input không tồn tại: {args.input}")
        sys.exit(1)

    if not files:
        print(f"❌ Không tìm thấy .wav files trong {args.input}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"TRIM REF LEAK — {len(files)} file(s)")
    print(f"{'='*60}")

    results = []
    for f in files:
        if args.dry_run:
            trim_start = get_first_real_word_start(f, ref_words, model=args.model,
                                                  language=args.language)
            import soundfile as sf
            orig_dur = sf.info(f).duration
            new_dur = orig_dur - trim_start
            print(f"  {os.path.basename(f)}: {orig_dur:.2f}s → trim {trim_start:.2f}s → {new_dur:.2f}s (DRY-RUN)")
            results.append((f, orig_dur, new_dur, trim_start))
        else:
            trim_start, new_dur, orig_dur, out_path = process_file(f, ref_words)
            saved = orig_dur - new_dur
            status = "✅" if trim_start > 0.1 else "⚠️ no ref leak"
            print(f"  {os.path.basename(f)}: {orig_dur:.2f}s → trim {trim_start:.2f}s → {new_dur:.2f}s {status}")
            print(f"    → {out_path}")
            results.append((f, orig_dur, new_dur, trim_start))

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    total_orig = sum(r[1] for r in results)
    total_new = sum(r[2] for r in results)
    print(f"Total: {total_orig:.2f}s → {total_new:.2f}s (saved {total_orig-total_new:.2f}s)")

    if args.dry_run:
        print("(DRY-RUN mode — không có file nào được ghi)")
    else:
        print(f"\nVerify lại bằng Whisper word-level:")
        print(f"  for f in <output_folder>/*_trim.wav; do")
        print(f"    mlx_whisper --model {args.model} --language {args.language} --word-timestamps True \"$f\"")
        print(f"    # Check: 0 ref words leak")
        print(f"  done")


if __name__ == "__main__":
    main()
