#!/usr/bin/env python3
"""Transcribe a video via local mlx_whisper (offline, free).

Drop-in replacement for the original Groq/OpenAI whisper module. Same public
API (`load_api_key`, `transcribe_video`, `transcribe_chunks`, helper fns),
same segment shape `{start, end, text}` so watch.py doesn't care where the
transcript came from.

Strategy: extract audio (mono 16kHz wav → mlx_whisper wants 16kHz float) →
call mlx_whisper.transcribe() with mlx-community/whisper-large-v3-mlx →
parse verbose_json['segments'].

Patched for Tuấn Anh 27/07/2026:
- Replaces Groq/OpenAI API calls with local Apple Silicon mlx_whisper
- Uses large-v3 by default (most accurate for technical terms)
- No API key, no internet, no cost
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_MODEL = "mlx-community/whisper-large-v3-mlx"
FALLBACK_MODEL = "mlx-community/whisper-medium-mlx"


def extract_audio(video_path: str, out_path: Path) -> Path:
    """Extract mono 16kHz audio → format follows out_path suffix (.wav | .mp3).

    mlx_whisper wants 16kHz float. .wav (pcm_s16le) is the lowest-overhead
    intermediate; .mp3 matches the upstream Groq path so watch.py's default
    audio_out=`audio.mp3` keeps working.
    """
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is not installed. Install with: brew install ffmpeg")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = out_path.suffix.lower()
    if suffix == ".wav":
        codec_args = ["-acodec", "pcm_s16le"]
    elif suffix == ".mp3":
        codec_args = ["-acodec", "libmp3lame", "-b:a", "64k"]
    else:
        raise SystemExit(f"unsupported audio suffix: {suffix} (use .wav or .mp3)")

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-i", str(Path(video_path).resolve()),
        "-vn",
        *codec_args,
        "-ar", "16000",
        "-ac", "1",
        str(out_path.resolve()),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"ffmpeg audio extraction failed: {result.stderr.strip()}")
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise SystemExit("ffmpeg produced no audio — video may have no audio track")
    return out_path


def audio_duration(audio_path: Path) -> float:
    """Return the duration of an audio file in seconds via ffprobe."""
    if shutil.which("ffprobe") is None:
        raise SystemExit("ffprobe is not installed. Install with: brew install ffmpeg")

    result = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            str(audio_path.resolve()),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"ffprobe failed: {result.stderr.strip()}")
    fmt = json.loads(result.stdout or "{}").get("format", {})
    return float(fmt.get("duration") or 0.0)


def chunk_by_seconds(
    total_seconds: float,
    chunk_seconds: float,
) -> list[tuple[float, float]]:
    """Split a duration into contiguous (offset, duration) chunks of ≤chunk_seconds."""
    if total_seconds <= chunk_seconds or total_seconds <= 0:
        return [(0.0, total_seconds)]
    n = int(total_seconds // chunk_seconds) + 1
    chunk = total_seconds / n
    return [
        (
            round(i * chunk, 3),
            round(total_seconds - i * chunk if i == n - 1 else chunk, 3),
        )
        for i in range(n)
    ]


def split_audio(
    full_audio: Path,
    work_dir: Path,
    plan: list[tuple[float, float]],
) -> list[tuple[Path, float]]:
    """Slice full_audio into per-plan chunk wav files."""
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is not installed. Install with: brew install ffmpeg")

    work_dir.mkdir(parents=True, exist_ok=True)
    chunks: list[tuple[Path, float]] = []
    for index, (offset, duration) in enumerate(plan):
        out_path = work_dir / f"chunk_{index:03d}.wav"
        cmd = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-y",
            "-ss", f"{offset:.3f}",
            "-i", str(full_audio.resolve()),
            "-t", f"{duration:.3f}",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(out_path.resolve()),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not out_path.exists() or out_path.stat().st_size == 0:
            raise SystemExit(
                f"ffmpeg failed to split audio chunk {index + 1}: {result.stderr.strip()}"
            )
        chunks.append((out_path, offset))
    return chunks


def shift_segments(segments: list[dict], offset_seconds: float) -> list[dict]:
    """Shift chunk-relative timestamps back to source time."""
    if offset_seconds == 0:
        return segments
    return [
        {
            "start": round(seg["start"] + offset_seconds, 2),
            "end": round(seg["end"] + offset_seconds, 2),
            "text": seg["text"],
        }
        for seg in segments
    ]


def _segments_from_response(data: dict) -> list[dict]:
    """Convert mlx_whisper verbose_json → {start, end, text}."""
    out: list[dict] = []
    for seg in data.get("segments") or []:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        out.append({
            "start": round(float(seg.get("start") or 0.0), 2),
            "end": round(float(seg.get("end") or 0.0), 2),
            "text": text,
        })
    if not out:
        full = (data.get("text") or "").strip()
        if full:
            out.append({"start": 0.0, "end": 0.0, "text": full})
    return out


def _transcribe_file(audio_path: Path, model: str, language: str = "vi") -> list[dict]:
    """Call mlx_whisper on one audio file → return 0-based segments."""
    try:
        import mlx_whisper
    except ImportError as exc:
        raise SystemExit(
            "mlx_whisper is not installed. Install with: pip install mlx-whisper"
        ) from exc

    result = mlx_whisper.transcribe(
        str(audio_path),
        path_or_hf_repo=model,
        language=language,
        verbose=False,
    )
    if not isinstance(result, dict):
        raise SystemExit(f"mlx_whisper returned unexpected type: {type(result)}")
    return _segments_from_response(result)


def transcribe_chunks(
    chunks: list[tuple[Path, float]],
    transcribe_one,
) -> list[dict]:
    """Transcribe each chunk, shift by offset, concatenate. Skip on per-chunk fail."""
    segments: list[dict] = []
    failures = 0
    for index, (path, offset) in enumerate(chunks):
        try:
            chunk_segments = transcribe_one(path)
        except Exception as exc:
            failures += 1
            print(
                f"[watch] chunk {index + 1}/{len(chunks)} failed — skipping ({exc})",
                file=sys.stderr,
            )
            continue
        segments.extend(shift_segments(chunk_segments, offset))
        print(
            f"[watch] chunk {index + 1}/{len(chunks)} → {len(chunk_segments)} segments",
            file=sys.stderr,
        )
    if failures == len(chunks):
        raise SystemExit("Whisper failed on every audio chunk")
    return segments


def load_api_key(*_args, **_kwargs) -> tuple[str, str] | tuple[None, None]:
    """No-op shim — local whisper has no API key. Returns ("local", "mlx").

    Kept so watch.py code path stays byte-identical to the upstream skill.
    """
    return "local", "mlx"


def transcribe_video(
    video_path: str,
    audio_out: Path,
    backend: str | None = None,
    api_key: str | None = None,
    language: str = "vi",
    model: str | None = None,
    _chunk_seconds: float = 600.0,
) -> tuple[list[dict], str]:
    """Run the full flow: extract audio → mlx_whisper → parse segments.

    Returns (segments, "local"). Raises SystemExit on any failure.
    """
    chosen_model = (
        model
        or os.environ.get("WATCH_WHISPER_MODEL")
        or DEFAULT_MODEL
    )

    print(f"[watch] extracting audio for local Whisper (model={chosen_model})…", file=sys.stderr)
    audio_path = extract_audio(video_path, audio_out)
    audio_bytes = audio_path.stat().st_size

    # Local mlx has no upload cap; chunk only if the user opted in via env var.
    long_form = os.environ.get("WATCH_WHISPER_CHUNK_SECONDS")
    if long_form:
        chunk_seconds = float(long_form)
        duration = audio_duration(audio_path)
        plan = chunk_by_seconds(duration, chunk_seconds)
        print(
            f"[watch] audio: {duration:.0f}s — splitting into {len(plan)} chunks of ≤{chunk_seconds:.0f}s…",
            file=sys.stderr,
        )
        chunks = split_audio(audio_path, audio_out.parent / "chunks", plan)

        def transcribe_one(path: Path) -> list[dict]:
            return _transcribe_file(path, chosen_model, language)

        segments = transcribe_chunks(chunks, transcribe_one)
    else:
        print(
            f"[watch] audio: {audio_bytes / 1024:.0f} kB — running mlx_whisper…",
            file=sys.stderr,
        )
        segments = _transcribe_file(audio_path, chosen_model, language)

    if not segments:
        raise SystemExit("Whisper returned no transcript segments")

    backend_used = "local-mlx"
    print(f"[watch] transcribed {len(segments)} segments via {backend_used}", file=sys.stderr)
    return segments, backend_used


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: whisper.py <video-path> [<audio-out.wav>] [--language vi] [--model <hf-repo>]", file=sys.stderr)
        raise SystemExit(2)

    video = sys.argv[1]
    audio_out = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else Path("audio.wav")
    language = "vi"
    model = None
    if "--language" in sys.argv:
        language = sys.argv[sys.argv.index("--language") + 1]
    if "--model" in sys.argv:
        model = sys.argv[sys.argv.index("--model") + 1]

    segments, backend = transcribe_video(video, audio_out, language=language, model=model)
    print(json.dumps({"backend": backend, "segments": segments}, indent=2, ensure_ascii=False))
