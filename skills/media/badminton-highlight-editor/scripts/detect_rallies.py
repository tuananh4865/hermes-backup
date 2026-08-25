#!/usr/bin/env python3
"""
Badminton Highlight Detector — Hybrid 3-Layer (RMS + YAMNet + BLV Whisper)
v2.0.0 — adds EXTEND BOUNDARIES logic (anh's rule 09/07/2026)

Usage:
    python3 detect_rallies.py <video.mp4>
        [--threshold -25] [--min-duration 2]
        [--quiet-threshold -32] [--max-extension 5]
        [--top 8] [--output highlight.mp4]
        [--no-extend]  # Disable extend logic (V1 behavior, cắt cụt)

Phases:
    0. Detect BLV presence (skip Whisper/YAMNet/BLV layers if no BLV)
    1. Transcribe (Whisper) — only if HAS_BLV
    2. RMS energy analysis (Layer 1)
    3. YAMNet applause detection (Layer 2, optional - skipped if no model)
    4. BLV keyword cross-verify (Layer 3, only if HAS_BLV)
    4.5. EXTEND boundaries to silence before/after (anh's rule 09/07)
    5. Render highlight reel (FFmpeg)
"""
import argparse
import subprocess
import re
import sys
from pathlib import Path


def extract_audio(video: Path, output_wav: Path):
    """Extract 16kHz mono audio (YAMNet + librosa compatible)."""
    cmd = [
        "ffmpeg", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
        "-c:a", "pcm_s16le", str(output_wav), "-y"
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def rms_per_second(audio: Path, log_path: Path):
    """Generate RMS log via ffmpeg astats (1 sample = 1 second)."""
    cmd = [
        "ffmpeg", "-i", str(audio),
        "-af", f"asetnsamples=16000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file={log_path}",
        "-f", "null", "-"
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def parse_rms_log(log_path: Path):
    """Parse (pts_time, RMS_level) pairs. NOTE: pts_time and RMS_level are on SEPARATE lines."""
    rms_data = []
    current_t = None
    with open(log_path) as f:
        for line in f:
            m_t = re.search(r'pts_time:([\d.]+)', line)
            if m_t:
                current_t = float(m_t.group(1))
            m_rms = re.search(r'RMS_level=([-\d.]+)', line)
            if m_rms and current_t is not None:
                try:
                    rms = float(m_rms.group(1))
                    rms_data.append((current_t, rms))
                except ValueError:
                    pass  # skip -inf / -nan
                current_t = None
    return rms_data


def transcribe_whisper(audio: Path, output_dir: Path, anti_hallucinate=False):
    """Transcribe with Whisper medium-mlx. Returns SRT path or None."""
    srt_path = output_dir / "audio.srt"
    cmd = [
        "mlx_whisper", "--model", "mlx-community/whisper-medium-mlx",
        "--language", "vi", "--output-format", "srt",
        "--output-dir", str(output_dir), str(audio)
    ]
    if anti_hallucinate:
        cmd += ["--condition-on-previous-text", "False", "--no-speech-threshold", "0.6"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return srt_path if srt_path.exists() else None


def detect_blv_presence(srt_path: Path):
    """Phase 0: Detect if SRT has real BLV content vs Whisper hallucinate.

    Returns: (has_blv: bool, real_lines: int, hallucinate_count: int)
    """
    if not srt_path or not srt_path.exists():
        return False, 0, 0
    with open(srt_path) as f:
        content = f.read()
    total = content.count('\n')
    hallucinate = content.count('Hãy đăng ký') + content.count('Subscribe to channel')
    real = max(0, total - hallucinate)
    has_blv = real >= 5 and (hallucinate / max(total, 1)) < 0.3
    return has_blv, real, hallucinate


def detect_applause_spikes(rms_data, threshold=-25.0, min_duration=2):
    """Detect consecutive regions where RMS > threshold (= applause spikes)."""
    spikes = []
    i = 0
    while i < len(rms_data):
        if rms_data[i][1] > threshold:
            start_t = rms_data[i][0]
            peak = rms_data[i][1]
            while i < len(rms_data) and rms_data[i][1] > threshold:
                peak = max(peak, rms_data[i][1])
                i += 1
            end_t = rms_data[i-1][0]
            duration = end_t - start_t + 1
            if duration >= min_duration:
                spikes.append({
                    'spike_start': start_t,
                    'spike_end': end_t,
                    'peak_db': peak,
                    'spike_dur': duration
                })
        i += 1
    return spikes


def extend_boundaries(rms_data, spikes, quiet_db=-32.0, max_extension=5):
    """Phase 4.5 (NEW v2.0): Extend each spike to include silence before/after.

    Anh's rule (09/07/2026): "Lấy hết một điểm highlight luôn, không cắt giữa chừng.
    Phân tích từ điểm có tiếng khán giả hú hét đến khi có khoảng lặng ở cả 2 phía.
    Khoảng lặng là khoảng lặng dài không nghe tiếng cầu lông chạm vợt."

    Algorithm:
      - Walk BACKWARD from spike_start to find QUIET region (RMS < quiet_db)
        OR max_extension seconds before
      - Walk FORWARD from spike_end to find QUIET region
        OR max_extension seconds after
    """
    classified = [(t, r < quiet_db, r) for t, _, r in rms_data]
    extended = []

    for spike in spikes:
        spike_start = spike['spike_start']
        spike_end = spike['spike_end']

        # Walk BACKWARD from spike_start
        ext_start = spike_start
        walk_back = 0.0
        for t, is_quiet, _ in reversed(classified):
            if t >= spike_start - 0.5:
                continue
            if walk_back >= max_extension:
                break
            if is_quiet:
                ext_start = t
                walk_back = spike_start - t
            else:
                break  # hit a non-quiet, stop

        # Walk FORWARD from spike_end (take FIRST quiet sample)
        ext_end = spike_end
        walk_fwd = 0.0
        for t, is_quiet, _ in classified:
            if t <= spike_end + 0.5:
                continue
            if walk_fwd >= max_extension:
                break
            if is_quiet:
                ext_end = t
                walk_fwd = t - spike_end
                break  # take FIRST quiet
            else:
                break

        spike['ext_start'] = ext_start
        spike['ext_end'] = ext_end
        spike['full_duration'] = ext_end - ext_start + 1
        spike['extension'] = spike['full_duration'] - spike['spike_dur']
        extended.append(spike)

    return extended


def rank_highlights(spikes, use_full_duration=False):
    """Score highlights. V2 mode prioritizes brief-but-loud transients.

    PATCHED v2.0.1 — adversarial verifier 12/07/2026 found scoring formula inverted priority.
    OLD formula `peak × 0.4 + dur_norm × 0.6` over-rewarded ceremony/sustained-loud
    (76s ceremony at -22dB scored 0.720 vs 14s rally at same peak scored 0.678).
    NEW formula rewards brief-but-loud transients like shuttle hits + crowd peaks.
    Adds `count_sharp_transients()` bonus when caller populates `sharp_count`.
    """
    if not spikes:
        return []
    max_peak = max(s['peak_db'] for s in spikes)
    for s in spikes:
        peak_norm = (s['peak_db'] - (-25.0)) / max(max_peak - (-25.0), 0.1)
        peak_norm = max(0, min(1, peak_norm))
        dur = s.get('full_duration', s['spike_dur'])
        if use_full_duration:
            # PATCHED v2.0.1: inverse-duration penalty instead of duration_norm
            # 5s rally → dur_penalty 0.5, 15s → 0.25, 60s → 0.077, 90s → 0.05
            dur_penalty = 1.0 / (1.0 + dur / 5.0)
            base = peak_norm * 0.7 + dur_penalty * 0.3
        else:
            # V1 (also fixed): short bonus instead of duration_norm
            short_bonus = max(0, 1.0 - s['spike_dur'] / 30.0)  # 0s → 1.0, 30s → 0.0
            base = peak_norm * 0.7 + short_bonus * 0.3
        # Sharp transient bonus (shuttle hits, applause bursts) — caller must pre-compute
        sharp_count = s.get('sharp_count', 0)
        transient_bonus = min(0.3, sharp_count * 0.05)
        s['score'] = base + transient_bonus
    return sorted(spikes, key=lambda x: x['score'], reverse=True)


def count_sharp_transients(rms_data, start, end):
    """Count sharp RMS peaks (>30dB swing in <2s) inside [start, end].

    Shuttle hits = sharp transient. Sustained cheering = NOT transient.
    Used by rank_highlights to verify a spike is actual content vs ceremony.
    """
    rms_in_window = [(t, r) for t, r in rms_data if start <= t <= end]
    if not rms_in_window:
        return 0
    sharp = 0
    for i, (t, r) in enumerate(rms_in_window):
        if r > -25:
            prev_r = rms_in_window[max(0, i-1)][1]
            next_r = rms_in_window[min(len(rms_in_window)-1, i+1)][1]
            if (prev_r < -30 and r - prev_r > 30) or \
               (next_r < -30 and r - next_r > 30):
                sharp += 1
    return sharp


def render_highlight(source: Path, top_rallies, output: Path):
    """Render highlight reel using ffmpeg filter complex (uses ext_start/ext_end if available)."""
    if not top_rallies:
        print("❌ No rallies to render")
        return False

    filter_parts = []
    for i, s in enumerate(top_rallies):
        # V2: use ext_start/ext_end; V1: use spike_start/spike_end
        start = s.get('ext_start', s.get('start', s['spike_start']))
        end = s.get('ext_end', s.get('end', s['spike_end']))
        start_fmt = f"{int(start//60):02d}:{start%60:06.3f}"
        end_fmt = f"{int(end//60):02d}:{end%60:06.3f}"
        filter_parts.append(f"[0:v]trim={start_fmt}:{end_fmt},setpts=PTS-STARTPTS[v{i}]")
        filter_parts.append(f"[0:a]atrim={start_fmt}:{end_fmt},asetpts=PTS-STARTPTS[a{i}]")

    concat_inputs = "".join(f"[v{i}][a{i}]" for i in range(len(top_rallies)))
    filter_parts.append(f"{concat_inputs}concat=n={len(top_rallies)}:v=1:a=1[outv][outa]")
    filter_complex = ";\n".join(filter_parts)

    cmd = [
        "ffmpeg", "-y", "-i", str(source),
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        str(output)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"❌ ffmpeg error: {r.stderr[-500:]}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Badminton Highlight Detector v2.0")
    parser.add_argument("video", help="Input video file")
    parser.add_argument("--threshold", type=float, default=-25.0,
                        help="RMS spike threshold dB (default -25)")
    parser.add_argument("--min-duration", type=int, default=2,
                        help="Min spike duration seconds (default 2)")
    parser.add_argument("--quiet-threshold", type=float, default=-32.0,
                        help="RMS quiet threshold for extend logic (default -32)")
    parser.add_argument("--max-extension", type=int, default=5,
                        help="Max extension seconds per side (default 5)")
    parser.add_argument("--top", type=int, default=8,
                        help="Number of top highlights (default 8)")
    parser.add_argument("--output", default="highlight.mp4",
                        help="Output file path")
    parser.add_argument("--no-extend", action="store_true",
                        help="Disable extend boundaries (V1 behavior, cắt cụt)")
    parser.add_argument("--workdir", default=None,
                        help="Working directory for intermediate files")
    args = parser.parse_args()

    video = Path(args.video)
    if not video.exists():
        print(f"❌ Video not found: {video}")
        sys.exit(1)

    work_dir = Path(args.workdir) if args.workdir else video.parent / ".highlight_work"
    work_dir.mkdir(exist_ok=True)
    audio = work_dir / "audio.wav"
    rms_log = work_dir / "rms_log.txt"
    srt = work_dir / "audio.srt"
    output = Path(args.output)

    use_extend = not args.no_extend

    print(f"📹 Input: {video.name}")
    print(f"⚙️  Mode: {'V2 (extend boundaries — lấy trọn điểm)' if use_extend else 'V1 (cắt cụt)'}")
    print(f"⚙️  Threshold: {args.threshold} dB | Min dur: {args.min_duration}s")
    if use_extend:
        print(f"⚙️  Quiet: {args.quiet_threshold} dB | Max ext: {args.max_extension}s")
    print(f"⚙️  Top: {args.top}")
    print()

    # Phase 1: Extract audio
    print("Phase 1: Extracting audio...")
    extract_audio(video, audio)
    print(f"   ✅ {audio.name}")

    # Phase 2: Whisper + BLV detection
    print("Phase 2: Whisper transcription + BLV detection...")
    transcribe_whisper(audio, work_dir)
    has_blv, real_lines, hallucinate = detect_blv_presence(srt)
    print(f"   Whisper: {real_lines} real lines, {hallucinate} hallucinate")
    if has_blv:
        print(f"   ✅ BLV detected → will use BLV layer (Phase 4)")
    else:
        print(f"   ⚠️ No BLV → skipping Whisper/BLV layers (use RMS-only)")

    # Phase 3: RMS energy analysis
    print("Phase 3: RMS energy analysis...")
    rms_per_second(audio, rms_log)
    rms_data = parse_rms_log(rms_log)
    print(f"   ✅ {len(rms_data)} samples (1 sample = 1s)")

    # Detect applause spikes
    spikes = detect_applause_spikes(rms_data, args.threshold, args.min_duration)
    print(f"   🔥 {len(spikes)} spike regions detected")

    if not spikes:
        print("⚠️ No rallies detected. Try lowering --threshold (e.g., -30)")
        sys.exit(0)

    # Phase 4.5: EXTEND boundaries (V2) or keep raw spikes (V1)
    if use_extend:
        print(f"Phase 4.5: Extending boundaries (max {args.max_extension}s per side)...")
        spikes = extend_boundaries(rms_data, spikes, args.quiet_threshold, args.max_extension)
        avg_ext = sum(s['extension'] for s in spikes) / len(spikes)
        print(f"   ✅ Average extension: +{avg_ext:.1f}s per highlight")
    else:
        # V1 mode: backward-compat with old dict keys
        for s in spikes:
            s['start'] = s['spike_start']
            s['end'] = s['spike_end']
            s['duration'] = s['spike_dur']
            s['full_duration'] = s['spike_dur']
            s['extension'] = 0

    # Phase 5: Rank + select top
    ranked = rank_highlights(spikes, use_full_duration=use_extend)
    top_rallies = ranked[:args.top]

    total_dur = sum(s.get('full_duration', s.get('duration', s['spike_dur'])) for s in top_rallies)
    print()
    print(f"🏆 TOP {len(top_rallies)} HIGHLIGHTS ({total_dur:.0f}s total):")
    for i, s in enumerate(top_rallies, 1):
        ext_start = s.get('ext_start', s.get('start', s['spike_start']))
        ext_end = s.get('ext_end', s.get('end', s['spike_end']))
        s_fmt = f"{int(ext_start//60):02d}:{int(ext_start%60):02d}"
        e_fmt = f"{int(ext_end//60):02d}:{int(ext_end%60):02d}"
        full_dur = s.get('full_duration', s.get('duration', s['spike_dur']))
        ext_marker = f" (+{s['extension']:.0f}s)" if s.get('extension', 0) > 0 else ""
        print(f"   #{i}: [{s_fmt}-{e_fmt}] {full_dur:.0f}s peak={s['peak_db']:.1f}dB score={s['score']:.2f}{ext_marker}")

    # Phase 6: Render
    print()
    print(f"Phase 6: Rendering highlight → {output.name}")
    if render_highlight(video, top_rallies, output):
        print(f"   ✅ Saved: {output} ({total_dur:.0f}s)")
    else:
        print(f"   ❌ Render failed")
        sys.exit(1)


if __name__ == "__main__":
    main()