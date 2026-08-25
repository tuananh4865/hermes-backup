#!/usr/bin/env python3
"""
Audio Highlight Detector — CLI entry point.

Production-ready detector for finding crowd-cheer / applause / loud-event
candidates in long-form audio/video. Outputs timestamped segments as JSON.

Usage:
    python detect_highlights.py input.mp4 --top 10 --output highlights.json
    python detect_highlights.py input.wav --adaptive --percentile 85
    python detect_highlights.py match.mp4 --centroid-thr 2000 --zcr-thr 0.15

Default settings tuned for sports broadcasts (badminton/football/basketball).
For concerts/podcasts, adjust --centroid-thr and --percentile.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import librosa
from scipy.ndimage import uniform_filter1d


@dataclass
class HighlightCandidate:
    start: float          # seconds
    end: float            # seconds
    duration: float       # seconds
    peak_rms_db: float    # peak RMS in dB
    mean_centroid_hz: float
    mean_zcr: float
    score: float          # 0..1
    kind: str             # "applause" | "cheer" | "whistle" | "music"


def extract_audio(video_path: Path, out_path: Path, sr: int = 22050) -> Path:
    """Extract mono PCM audio from video using ffmpeg."""
    import subprocess
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", str(sr),
        "-c:a", "pcm_s16le", str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path


def compute_features(
    y: np.ndarray,
    sr: int,
    frame_length: int = 2048,
    hop_length: int = 512,
    smooth_window: int = 20,
) -> dict:
    """Compute and smooth all features needed for highlight detection."""
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)

    centroid = librosa.feature.spectral_centroid(
        y=y, sr=sr, hop_length=hop_length
    )[0]
    zcr = librosa.feature.zero_crossing_rate(
        y, frame_length=frame_length, hop_length=hop_length
    )[0]

    return {
        "rms_db": uniform_filter1d(rms_db, size=smooth_window),
        "centroid": uniform_filter1d(centroid, size=smooth_window),
        "zcr": uniform_filter1d(zcr, size=smooth_window),
        "times": librosa.frames_to_time(
            np.arange(len(rms_db)), sr=sr, hop_length=hop_length
        ),
    }


def compute_score(rms_db: float, centroid: float, zcr: float) -> float:
    """Combine 3 features into a [0, 1] highlight score."""
    rms_score = float(np.clip((rms_db + 30) / 20, 0, 1))
    cent_score = float(np.clip((centroid - 1500) / 3000, 0, 1))
    zcr_score = float(np.clip((zcr - 0.1) / 0.3, 0, 1))
    return round(0.5 * rms_score + 0.3 * cent_score + 0.2 * zcr_score, 3)


def classify_kind(rms_db: float, centroid: float, zcr: float, duration: float) -> str:
    """Rough classification of detected event type."""
    if duration < 1.0 and zcr > 0.30 and 2000 < centroid < 4500:
        return "whistle"
    if duration >= 5.0:
        return "cheer"
    if rms_db > -15:
        return "cheer"
    return "applause"


def extract_segments(
    mask: np.ndarray,
    times: np.ndarray,
    feats: dict,
    min_duration: float = 2.0,
) -> list[HighlightCandidate]:
    """Convert per-frame boolean mask to candidate segments."""
    candidates: list[HighlightCandidate] = []
    in_seg = False
    start_t = 0.0

    for t, m in zip(times, mask):
        if m and not in_seg:
            start_t = float(t)
            in_seg = True
        elif not m and in_seg:
            end_t = float(t)
            dur = end_t - start_t
            if dur >= min_duration:
                m_frame = (times >= start_t) & (times < end_t)
                peak_db = float(feats["rms_db"][m_frame].max())
                mean_cent = float(feats["centroid"][m_frame].mean())
                mean_zcr = float(feats["zcr"][m_frame].mean())
                candidates.append(HighlightCandidate(
                    start=round(start_t, 2),
                    end=round(end_t, 2),
                    duration=round(dur, 2),
                    peak_rms_db=round(peak_db, 1),
                    mean_centroid_hz=round(mean_cent, 0),
                    mean_zcr=round(mean_zcr, 3),
                    score=compute_score(peak_db, mean_cent, mean_zcr),
                    kind=classify_kind(peak_db, mean_cent, mean_zcr, dur),
                ))
            in_seg = False

    # Trailing segment
    if in_seg and (times[-1] - start_t) >= min_duration:
        m_frame = times >= start_t
        peak_db = float(feats["rms_db"][m_frame].max())
        mean_cent = float(feats["centroid"][m_frame].mean())
        mean_zcr = float(feats["zcr"][m_frame].mean())
        dur = float(times[-1] - start_t)
        candidates.append(HighlightCandidate(
            start=round(start_t, 2),
            end=round(float(times[-1]), 2),
            duration=round(dur, 2),
            peak_rms_db=round(peak_db, 1),
            mean_centroid_hz=round(mean_cent, 0),
            mean_zcr=round(mean_zcr, 3),
            score=compute_score(peak_db, mean_cent, mean_zcr),
            kind=classify_kind(peak_db, mean_cent, mean_zcr, dur),
        ))

    return candidates


def detect(
    audio_path: Path,
    *,
    sr: int = 22050,
    frame_length: int = 2048,
    hop_length: int = 512,
    smooth_window: int = 20,
    percentile: int = 85,
    centroid_thr: float = 2000.0,
    zcr_thr: float = 0.15,
    min_duration: float = 2.0,
    top_n: int | None = None,
) -> list[HighlightCandidate]:
    """Main detection pipeline. Returns candidates sorted by score (desc)."""
    y, sr = librosa.load(str(audio_path), sr=sr, mono=True)
    duration = len(y) / sr
    print(f"[detect] {audio_path} — {duration:.1f}s @ {sr}Hz", file=sys.stderr)

    feats = compute_features(y, sr, frame_length, hop_length, smooth_window)
    n = len(feats["times"])
    if n == 0:
        return []

    # Adaptive RMS threshold (top-percentile)
    rms_thr = float(np.percentile(feats["rms_db"], percentile))
    print(f"[detect] adaptive RMS threshold (p{percentile}): {rms_thr:.1f} dB", file=sys.stderr)

    # Combined gate
    mask = (
        (feats["rms_db"] > rms_thr)
        & (feats["centroid"] > centroid_thr)
        & (feats["zcr"] > zcr_thr)
    )

    candidates = extract_segments(mask, feats["times"], feats, min_duration)
    candidates.sort(key=lambda c: c.score, reverse=True)

    print(f"[detect] {len(candidates)} candidates (min_duration={min_duration}s)", file=sys.stderr)

    if top_n is not None:
        candidates = candidates[:top_n]
    return candidates


def main():
    parser = argparse.ArgumentParser(
        description="Detect highlight moments in audio/video via energy-based features.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="Path to audio or video file")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Output JSON path (default: <input>.highlights.json)")
    parser.add_argument("--top", "-n", type=int, default=None,
                        help="Keep only top N candidates by score")
    parser.add_argument("--sr", type=int, default=22050, help="Sample rate")
    parser.add_argument("--percentile", "-p", type=int, default=85,
                        help="Adaptive RMS threshold percentile (default 85 = top 15%% loud)")
    parser.add_argument("--centroid-thr", type=float, default=2000.0,
                        help="Spectral centroid threshold in Hz")
    parser.add_argument("--zcr-thr", type=float, default=0.15,
                        help="Zero-crossing rate threshold")
    parser.add_argument("--min-duration", type=float, default=2.0,
                        help="Minimum segment duration in seconds")
    parser.add_argument("--extract-audio", action="store_true",
                        help="Force re-extraction of audio (default: use as-is if WAV/MP3)")

    args = parser.parse_args()

    input_path: Path = args.input.resolve()
    if not input_path.exists():
        print(f"ERROR: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve audio path (extract if needed)
    audio_exts = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
    if input_path.suffix.lower() in audio_exts and not args.extract_audio:
        audio_path = input_path
    else:
        audio_path = input_path.with_suffix(".extracted.wav")
        extract_audio(input_path, audio_path, sr=args.sr)

    candidates = detect(
        audio_path,
        sr=args.sr,
        percentile=args.percentile,
        centroid_thr=args.centroid_thr,
        zcr_thr=args.zcr_thr,
        min_duration=args.min_duration,
        top_n=args.top,
    )

    # Output
    output_path = args.output or input_path.with_suffix(".highlights.json")
    payload = {
        "source": str(input_path),
        "audio_extracted": str(audio_path),
        "total_candidates": len(candidates),
        "candidates": [asdict(c) for c in candidates],
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"[detect] wrote {output_path}", file=sys.stderr)

    # Console summary
    print(f"\nFound {len(candidates)} highlight candidates:")
    for c in candidates[:10]:
        print(f"  {c.start:7.1f}s - {c.end:7.1f}s ({c.duration:5.1f}s) "
              f"[{c.kind:8s}] score={c.score:.2f} peak={c.peak_rms_db:.1f}dB")


if __name__ == "__main__":
    main()