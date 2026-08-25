#!/usr/bin/env python3
"""
verify_false_start.py — Cross-check L4 FALSE START candidates bằng re-whisper từng side.

Workflow per PITFALL #28: khi `verify_clip_full.py` L4 flag candidate
(gap < 10s + 5+/8 first-word match), KHÔNG trust ngay — phải re-whisper
từng segment audio độc lập để phân biệt:
  - FALSE START thật: 2 takes khác nhau (transcripts decode khác biệt rõ)
  - RHETORIC false positive: parallel-reason VN narration (transcripts gần giống)

Usage:
    python3 verify_false_start.py <video.mp4> <seg_a_start> <seg_a_end> <seg_b_start> <seg_b_end>

Example (clip 0038 V2):
    python3 verify_false_start.py clip.mp4 47.70 51.10 53.70 56.70

Exit 0 = RHETORIC (không cần cut), Exit 1 = FALSE START (cần cut seg_a).

PITFALL context: xem references/lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md (PITFALL #28)
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def extract_audio(video_path: str, start: float, end: float, out_path: str) -> None:
    """Extract audio segment to 16kHz mono WAV."""
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-ss", str(start), "-to", str(end),
        "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        out_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def whisper_transcribe(wav_path: str) -> str:
    """Run whisper tiny Vietnamese, return text."""
    cmd = [
        "whisper", wav_path,
        "--model", "tiny",
        "--language", "Vietnamese",
        "--output_format", "txt",
        "--output_dir", str(Path(wav_path).parent),
    ]
    subprocess.run(cmd, capture_output=True)
    txt_path = Path(wav_path).with_suffix(".txt")
    if txt_path.exists():
        return txt_path.read_text().strip()
    return ""


def first_n_words(text: str, n: int = 8) -> str:
    """First N words của transcript (lowercased)."""
    text = text.lower().strip()
    # Whisper có thể output với [timestamp] prefix
    text = re.sub(r"\[\d+:\d+\.\d+\s*-->\s*\d+:\d+\.\d+\]\s*", "", text)
    words = text.split()
    return " ".join(words[:n])


def word_overlap(a: str, b: str) -> int:
    """Count word overlap between two first-N-word strings."""
    wa = set(a.split())
    wb = set(b.split())
    return len(wa & wb)


def classify(transcript_a: str, transcript_b: str, seg_a_range: tuple, seg_b_range: tuple) -> dict:
    """Classify candidate as FALSE_START or RHETORIC."""
    fa = first_n_words(transcript_a)
    fb = first_n_words(transcript_b)
    overlap = word_overlap(fa, fb)

    # If transcripts decode to clearly different content (different nouns/verbs after first 2-3 connector words)
    # AND first-word overlap is high (heuristic trigger) → FALSE START
    # If transcripts are near-identical (only connector words differ) → RHETORIC

    # Check length diff
    len_a, len_b = len(transcript_a.split()), len(transcript_b.split())

    # Decode quality heuristic: if either transcript is mostly garbage (e.g. < 3 words decoded)
    if len_a < 3 or len_b < 3:
        return {
            "verdict": "INDETERMINATE",
            "reason": f"whisper decode poor (len_a={len_a}, len_b={len_b}); retry với model base",
            "transcript_a": transcript_a,
            "transcript_b": transcript_b,
            "first_overlap": overlap,
        }

    # Check if same content with minor variations
    common = sum(1 for w in transcript_a.lower().split() if w in transcript_b.lower().split())
    similarity = common / max(len_a, len_b)

    if similarity > 0.85:
        return {
            "verdict": "RHETORIC",
            "reason": f"transcripts {similarity*100:.0f}% similar → cùng take với minor rephrase, KHÔNG cut",
            "transcript_a": transcript_a,
            "transcript_b": transcript_b,
            "first_overlap": overlap,
            "similarity_pct": round(similarity * 100, 1),
            "action": "NO ACTION (parallel-reason VN narration)",
        }
    else:
        return {
            "verdict": "FALSE_START",
            "reason": f"transcripts chỉ {similarity*100:.0f}% similar + first-word overlap {overlap}/8 → 2 takes khác nhau, CẦN CẮT seg_a",
            "transcript_a": transcript_a,
            "transcript_b": transcript_b,
            "first_overlap": overlap,
            "similarity_pct": round(similarity * 100, 1),
            "action": f"CUT seg_a ({seg_a_range[0]}-{seg_a_range[1]}s), KEEP seg_b ({seg_b_range[0]}-{seg_b_range[1]}s)",
        }


def main():
    if len(sys.argv) != 6:
        print("Usage: python3 verify_false_start.py <video.mp4> <seg_a_start> <seg_a_end> <seg_b_start> <seg_b_end>", file=sys.stderr)
        sys.exit(2)

    video_path = sys.argv[1]
    seg_a_start, seg_a_end = float(sys.argv[2]), float(sys.argv[3])
    seg_b_start, seg_b_end = float(sys.argv[4]), float(sys.argv[5])

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_a = f"{tmpdir}/seg_a.wav"
        wav_b = f"{tmpdir}/seg_b.wav"
        extract_audio(video_path, seg_a_start, seg_a_end, wav_a)
        extract_audio(video_path, seg_b_start, seg_b_end, wav_b)
        transcript_a = whisper_transcribe(wav_a)
        transcript_b = whisper_transcribe(wav_b)

    result = classify(transcript_a, transcript_b, (seg_a_start, seg_a_end), (seg_b_start, seg_b_end))

    print(f"Seg A ({seg_a_start}-{seg_a_end}s): {result['transcript_a']}")
    print(f"Seg B ({seg_b_start}-{seg_b_end}s): {result['transcript_b']}")
    print()
    print(f"VERDICT: {result['verdict']}")
    print(f"Reason:  {result['reason']}")
    if "first_overlap" in result:
        print(f"First-word overlap: {result['first_overlap']}/8")
    if "similarity_pct" in result:
        print(f"Transcript similarity: {result['similarity_pct']}%")
    print(f"Action:  {result['action']}")

    sys.exit(1 if result["verdict"] == "FALSE_START" else 0)


if __name__ == "__main__":
    main()