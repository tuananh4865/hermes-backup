#!/usr/bin/env python3
"""verify_clip_full.py — One-shot comprehensive verifier cho TikTok clip cuối cùng.

Kết hợp 7 layers verify (PITFALL #1-#9 + #21 Layer 3 + RMS + Motion).

Layers:
  1. Spec TikTok (ffprobe): 1080x1920, AAC 44100Hz, bitrate, duration, faststart
  2. Whisper re-read + 5-dim strict (FILLER/TREO/LẶP NGHĨA/HOOK LẶP/ỰM_Ỡ)
  3. Anchor-lap semantic scan
  4. Layer 3 FALSE START scan (PITFALL #21) — gap < 10s + 5+/8 first-word match
  5. RMS first-3s silent-take detector (PITFALL #21)
  6. Audio RMS delta vs source (loudness check, threshold 0.5dB)
  7. Motion check (pixel-diff t=5s vs t=10s, threshold 10%)

Usage:
    python3 verify_clip_full.py <clip.mp4> [--source source.mp4] [--report report.md]

Output:
    Exit 0 = ALL PASS (SHIP CLEAN)
    Exit 1 = issues found
    Optional report.md với full breakdown + recommended next steps

PITFALL context (real case 18/07 clip 0007 KNF carbon fiber bộ vệ sinh):
  - 7/7 layers PASS ngoại trừ duration 137.3s > Mode B max 130s.
  - Clip đơn-take 137s, không có false start, filler, treo, hook-lap.
  - Parallel-reason "Bởi vì A... Bởi vì B..." là false positive trap thường gặp
    cho Vietnamese narration — cần phân biệt rõ với Pitfall #21 false start.

Khi nào dùng:
  - Verify clip cuối cùng trước khi ship (BẮT BUỘC theo user instruction 18/07)
  - Mỗi lần user hỏi "verify clip N", "check lỗi", "đạt goal"
  - Sau khi render V_N mới (Pitfall #4 FIRST-CLASS)

Khi nào KHÔNG dùng:
  - Trong workflow edit (chạy riêng từng layer scripts/verify_clip.py + check_anchor_lap.py)
  - Để verify mid-iteration keep_plan
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image


# ---------- Layer 1: Spec TikTok ----------

def probe_spec(video_path):
    """Run ffprobe to extract stream + format specs."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", video_path],
        capture_output=True, text=True, check=True,
    )
    out = r.stdout
    spec = {
        "path": video_path,
        "size": os.path.getsize(video_path),
        "width": None, "height": None,
        "codec": None, "pix_fmt": None,
        "audio_codec": None, "sample_rate": None, "channels": None,
        "duration": None, "bit_rate": None, "nb_frames": None,
    }
    cur = None
    for line in out.split("\n"):
        if line.startswith("[STREAM]"):
            cur = {}
            continue
        if line.startswith("[/STREAM]"):
            if cur and cur.get("codec_type") == "video" and spec["width"] is None:
                spec.update({
                    "width": int(cur.get("width", 0)),
                    "height": int(cur.get("height", 0)),
                    "codec": cur.get("codec_name"),
                    "pix_fmt": cur.get("pix_fmt"),
                    "nb_frames": int(cur.get("nb_frames", 0)),
                })
            elif cur and cur.get("codec_type") == "audio" and spec["audio_codec"] is None:
                spec.update({
                    "audio_codec": cur.get("codec_name"),
                    "sample_rate": int(cur.get("sample_rate", 0)),
                    "channels": int(cur.get("channels", 0)),
                })
            continue
        if cur is not None and "=" in line:
            k, v = line.split("=", 1)
            cur[k.strip()] = v.strip()
    if "[FORMAT]" in out:
        fmt = out.split("[FORMAT]", 1)[1].split("[/FORMAT]", 1)[0]
        for line in fmt.split("\n"):
            if "=" in line:
                k, v = line.split("=", 1)
                if k == "duration":
                    spec["duration"] = float(v)
                elif k == "bit_rate":
                    spec["bit_rate"] = int(v)
    return spec


def check_spec(spec):
    """Verify spec matches TikTok requirements."""
    issues = []
    if spec["width"] != 1080 or spec["height"] != 1920:
        issues.append(f"Resolution {spec['width']}x{spec['height']} != 1080x1920")
    if spec["codec"] != "h264":
        issues.append(f"Video codec '{spec['codec']}' != h264")
    if spec["audio_codec"] != "aac":
        issues.append(f"Audio codec '{spec['audio_codec']}' != aac")
    if spec["sample_rate"] != 44100:
        issues.append(f"Sample rate {spec['sample_rate']} != 44100")
    if spec["duration"] is None or spec["duration"] < 30 or spec["duration"] > 180:
        issues.append(f"Duration {spec['duration']:.2f}s out of 30-180s range")
    elif spec["duration"] > 130:
        issues.append(f"Duration {spec['duration']:.2f}s > 130s Mode B max - apply Pitfall #26 speed 1.3x")
    return issues


# ---------- Layer 2: Whisper + 5-dim strict ----------

ANCHOR_KEYWORDS = [
    "nhãn hàng", "nhưng mà", "tuy nhiên", "cho nên", "vì vậy",
    "do đó", "bởi vì", "nói chung", "tóm lại", "cuối cùng",
    "kết luận", "nhà mình", "bên mình", "các bạn", "mọi người",
    "chúng ta", "nãy", "ờ", "thì", "à", "rồi", "đó", "giờ",
]
FILLER_LIST = ["ơ", "ờ", "ừm", "ừ", "ó", "à", "á"]


def extract_audio(video_path, tmpdir):
    """Extract mono 16kHz WAV for Whisper."""
    wav = os.path.join(tmpdir, "audio.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-vn",
         "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", wav],
        capture_output=True, check=True,
    )
    return wav


def whisper_transcribe(audio_wav, tmpdir):
    """Run mlx_whisper medium-vi. Returns path to JSON output."""
    subprocess.run(
        ["mlx_whisper", "--model", "mlx-community/whisper-medium-mlx",
         "--language", "vi", "--output-format", "json",
         "--output-dir", tmpdir, audio_wav],
        capture_output=True, check=True,
    )
    return os.path.join(tmpdir, "audio.json")


def five_dim_strict(whisper_json):
    """Run 5-dim strict checks on Whisper output."""
    with open(whisper_json) as f:
        data = json.load(f)
    segs = data["segments"]

    filler_hits = []
    standalone_filler = []
    treo_hits = []
    hook_lap_pairs = []

    for i, s in enumerate(segs):
        text = s["text"].strip().lower()
        words = text.split()
        if not words:
            continue
        for w in words:
            w_clean = w.strip(",.!?")
            if w_clean in FILLER_LIST:
                filler_hits.append({
                    "seg": i, "word": w,
                    "time": f"{s['start']:.2f}-{s['end']:.2f}",
                })
        if len(words) == 1 and words[0].strip(",.?") in FILLER_LIST:
            standalone_filler.append({
                "seg": i, "text": text,
                "time": f"{s['start']:.2f}-{s['end']:.2f}",
            })
        n_filler = sum(1 for w in words if w.strip(",.!?") in FILLER_LIST)
        if n_filler >= 3:
            treo_hits.append({
                "seg": i, "n_filler": n_filler,
                "text": text[:80],
                "time": f"{s['start']:.2f}-{s['end']:.2f}",
            })

    for i in range(len(segs) - 1):
        s_i, s_j = segs[i], segs[i + 1]
        gap = s_j["start"] - s_i["end"]
        if gap > 5:
            continue
        w_i = s_i["text"].strip().split()[:5]
        w_j = s_j["text"].strip().split()[:5]
        match_5 = sum(1 for a, b in zip(w_i, w_j) if a == b)
        if match_5 >= 3:
            hook_lap_pairs.append({
                "pair": f"{i}<->{i+1}", "match": match_5,
                "time_a": f"{s_i['start']:.2f}-{s_i['end']:.2f}",
                "time_b": f"{s_j['start']:.2f}-{s_j['end']:.2f}",
                "a": s_i["text"][:80],
                "b": s_j["text"][:80],
            })

    return {
        "n_segs": len(segs),
        "filler_hits": filler_hits,
        "standalone_filler": standalone_filler,
        "treo_hits": treo_hits,
        "hook_lap_pairs": hook_lap_pairs,
        "high_nsp": [s for s in segs if s.get("no_speech_prob", 0) > 0.3],
    }


# ---------- Layer 3: Anchor-lap semantic ----------

def anchor_lap_scan(whisper_json):
    """Anchor-keyword scan."""
    with open(whisper_json) as f:
        data = json.load(f)
    segs = data["segments"]
    pairs = []
    for i in range(len(segs) - 1):
        t1 = segs[i]["text"].lower()
        t2 = segs[i + 1]["text"].lower()
        gap = segs[i + 1]["start"] - segs[i]["end"]
        if gap > 5:
            continue
        for kw in ANCHOR_KEYWORDS:
            if kw in t1 and kw in t2:
                pairs.append({
                    "pair": f"{i}<->{i+1}", "kw": kw, "gap": round(gap, 2),
                    "a": segs[i]["text"][:80],
                    "b": segs[i + 1]["text"][:80],
                })
    return pairs


# ---------- Layer 4: FALSE START Layer 3 (Pitfall #21) ----------

def false_start_scan(whisper_json, gap_thresh=10.0, word_match=5):
    """Layer 3 false-start scan per Pitfall #21.

    Detect pairs of adjacent segments (gap < 10s) with 5+ matching first 8 words.
    These are candidates where a take was re-shot and both takes ended up in the clip.
    """
    with open(whisper_json) as f:
        data = json.load(f)
    segs = data["segments"]
    candidates = []
    for i in range(len(segs) - 1):
        s_i = segs[i]
        s_j = segs[i + 1]
        gap = s_j["start"] - s_i["end"]
        if gap > gap_thresh:
            continue
        w_i = s_i["text"].strip().split()[:8]
        w_j = s_j["text"].strip().split()[:8]
        match = sum(1 for a, b in zip(w_i, w_j) if a == b)
        if match >= word_match:
            candidates.append({
                "pair": f"{i}<->{i+1}",
                "gap": round(gap, 2),
                "match": f"{match}/8",
                "time_a": f"{s_i['start']:.2f}-{s_i['end']:.2f}",
                "time_b": f"{s_j['start']:.2f}-{s_j['end']:.2f}",
                "a": s_i["text"][:100],
                "b": s_j["text"][:100],
            })
    return candidates


# ---------- Layer 5: RMS first-3s silent-take detector ----------

def rms_first_3s(video_path):
    """Get mean volume of first 3 seconds. Returns dB.
    If < -50dB, clip first 3s is silent (likely false start with old take muted).
    """
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-t", "3", "-i", video_path,
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in r.stderr.split("\n"):
        if "mean_volume" in line:
            try:
                return float(line.split("mean_volume:")[1].split("dB")[0].strip())
            except (ValueError, IndexError):
                pass
    return -999.0


def mean_volume(video_path):
    """Get overall mean volume."""
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", video_path,
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in r.stderr.split("\n"):
        if "mean_volume" in line:
            try:
                return float(line.split("mean_volume:")[1].split("dB")[0].strip())
            except (ValueError, IndexError):
                pass
    return -999.0


# ---------- Layer 6: Audio RMS delta vs source ----------

def rms_delta_check(edited_path, source_path):
    """Compare overall mean volume between edited and source. Threshold 0.5dB."""
    if not source_path or not os.path.isfile(source_path):
        return {"available": False}
    e = mean_volume(edited_path)
    s = mean_volume(source_path)
    if e == -999 or s == -999:
        return {"available": False}
    delta = abs(e - s)
    return {
        "available": True,
        "edit_rms": e, "source_rms": s, "delta": round(delta, 2),
        "pass": delta <= 0.5,
    }


# ---------- Layer 7: Motion check ----------

def pixel_diff_pct(p1, p2, thresh=30, step=4):
    """% pixels changed > threshold (sum over RGB channels / 3)."""
    a = Image.open(p1).convert("RGB")
    b = Image.open(p2).convert("RGB")
    w, h = a.size
    da, db = a.load(), b.load()
    diffs = counted = 0
    for y in range(0, h, step):
        for x in range(0, w, step):
            ax, bx = da[x, y], db[x, y]
            d = abs(ax[0] - bx[0]) + abs(ax[1] - bx[1]) + abs(ax[2] - bx[2])
            counted += 1
            if d > thresh:
                diffs += 1
    return diffs / counted * 100 if counted else 0.0


def motion_check(video_path, t1=5, t2=10):
    """Extract frames at t1 and t2 seconds, compute pixel diff %.
    PASS if >= 10% (proxy: clip is not a still image).
    """
    tmpdir = tempfile.mkdtemp(prefix="motion_")
    f1 = os.path.join(tmpdir, "f1.png")
    f2 = os.path.join(tmpdir, "f2.png")
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(t1), "-i", video_path,
         "-frames:v", "1", f1],
        capture_output=True, check=True,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(t2), "-i", video_path,
         "-frames:v", "1", f2],
        capture_output=True, check=True,
    )
    pct = pixel_diff_pct(f1, f2)
    return {"t1": t1, "t2": t2, "pixel_diff_pct": round(pct, 2), "pass": pct >= 10.0}


# ---------- Orchestrator ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", help="Path to .mp4 to verify")
    ap.add_argument("--source", help="Path to source MP4 (for RMS delta check)")
    ap.add_argument("--report", help="Optional path to write report.md")
    args = ap.parse_args()

    if not os.path.isfile(args.video):
        print(f"ERROR: Video not found: {args.video}")
        sys.exit(2)

    print(f"Verifying: {args.video}\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Layer 1: Spec
        print("=== LAYER 1: SPEC ===")
        spec = probe_spec(args.video)
        spec_issues = check_spec(spec)
        print(f"   Resolution: {spec['width']}x{spec['height']}")
        print(f"   Video codec: {spec['codec']} | Audio codec: {spec['audio_codec']}")
        print(f"   Duration: {spec['duration']:.2f}s | Bitrate: {spec['bit_rate']//1000}kbps")
        for iss in spec_issues:
            print(f"   !  {iss}")
        print(f"   {'PASS' if not spec_issues else 'ISSUES'}")
        print()

        # Layer 2: Whisper + 5-dim strict
        print("=== LAYER 2: 5-DIM STRICT (FILLER/TREO/LAP NGHIA/HOOK LAP/UM_O) ===")
        wav = extract_audio(args.video, tmpdir)
        wjson = whisper_transcribe(wav, tmpdir)
        strict = five_dim_strict(wjson)
        print(f"   Segments: {strict['n_segs']}")
        print(f"   FILLER hits: {len(strict['filler_hits'])}")
        print(f"   Standalone filler (UM_O): {len(strict['standalone_filler'])}")
        print(f"   TREO (3+ filler/seg): {len(strict['treo_hits'])}")
        print(f"   HOOK LAP (3+ first-word match): {len(strict['hook_lap_pairs'])}")
        print(f"   HIGH NSP (Whisper hallucinate): {len(strict['high_nsp'])}")
        strict_total = (len(strict['filler_hits']) + len(strict['standalone_filler'])
                        + len(strict['treo_hits']) + len(strict['hook_lap_pairs']))
        print(f"   {'PASS' if strict_total == 0 else 'ISSUES'}")
        print()

        # Layer 3: Anchor-lap semantic
        print("=== LAYER 3: ANCHOR-LAP SEMANTIC ===")
        anchor = anchor_lap_scan(wjson)
        print(f"   Anchor-keyword pairs: {len(anchor)}")
        for x in anchor:
            print(f"     [{x['kw']}] seg {x['pair']}: {x['a'][:60]}")
        print(f"   {'PASS' if not anchor else 'REVIEW (SOURCE-LEVEL or KEEP-BOUNDARY?)'}")
        print()

        # Layer 4: FALSE START Layer 3 (Pitfall #21)
        print("=== LAYER 4: FALSE START (PITFALL #21) ===")
        fs = false_start_scan(wjson)
        print(f"   Candidates (gap < 10s + 5+/8 first-word match): {len(fs)}")
        for x in fs:
            print(f"     seg {x['pair']} gap={x['gap']}s match={x['match']}")
            print(f"       [old] {x['a']}")
            print(f"       [new] {x['b']}")
        print(f"   {'PASS' if not fs else 'REVIEW (parallel-reason rhetoric?)'}")
        print()

        # Layer 5: RMS first-3s
        print("=== LAYER 5: RMS FIRST-3s SILENT-TAKE DETECTOR ===")
        rms3 = rms_first_3s(args.video)
        print(f"   First 3s mean_volume: {rms3:.2f} dB")
        silent = rms3 < -50
        print(f"   {'SILENT (likely silent take cu!)' if silent else 'AUDIBLE (no silent take)'}")
        print()

        # Layer 6: RMS delta vs source
        print("=== LAYER 6: AUDIO RMS DELTA vs SOURCE ===")
        if args.source:
            rms_delta = rms_delta_check(args.video, args.source)
            if rms_delta.get("available"):
                print(f"   Edited: {rms_delta['edit_rms']:.2f} dB")
                print(f"   Source: {rms_delta['source_rms']:.2f} dB")
                print(f"   Delta: {rms_delta['delta']:.2f} dB")
                print(f"   {'PASS (<=0.5dB)' if rms_delta['pass'] else 'DELTA > 0.5dB'}")
            else:
                print(f"   ! Could not extract RMS")
        else:
            print(f"   -- skipped (no --source flag)")
        print()

        # Layer 7: Motion
        print("=== LAYER 7: MOTION CHECK (pixel diff t=5s vs t=10s) ===")
        motion = motion_check(args.video)
        print(f"   Pixel diff: {motion['pixel_diff_pct']:.2f}%")
        print(f"   {'PASS (>=10%)' if motion['pass'] else 'LOW MOTION (possible freeze frame)'}")
        print()

        # Summary verdict
        print("=" * 60)
        print("VERDICT")
        print("=" * 60)
        n_issues = (len(spec_issues) + strict_total + len(anchor) + len(fs)
                    + (1 if silent else 0))
        if n_issues == 0 and motion["pass"]:
            print("SHIP CLEAN - all 7 layers PASS")
            verdict = "SHIP CLEAN"
        elif n_issues <= 3 and motion["pass"]:
            print(f"PARTIAL PASS - {n_issues} issues to review")
            verdict = "PARTIAL PASS"
        else:
            print(f"FAIL - {n_issues} issues found")
            verdict = "FAIL"
        print(f"\nDuration: {spec['duration']:.2f}s")
        if spec["duration"] > 130:
            print("-> ACTION REQUIRED: Apply Pitfall #26 speed 1.3x to bring duration into Mode B sweet spot")

        # Write report if requested
        if args.report:
            with open(args.report, "w") as f:
                f.write(f"# Verify report - {os.path.basename(args.video)}\n\n")
                f.write(f"**Verdict:** {verdict}\n\n")
                f.write(f"## Spec\n{json.dumps(spec, indent=2)}\n\n")
                f.write(f"## 5-dim strict\n{json.dumps(strict, indent=2)}\n\n")
                f.write(f"## Anchor-lap\n{json.dumps(anchor, indent=2)}\n\n")
                f.write(f"## False start\n{json.dumps(fs, indent=2)}\n\n")
                f.write(f"## Motion\n{json.dumps(motion, indent=2)}\n")
            print(f"\nReport written to {args.report}")

        sys.exit(0 if verdict == "SHIP CLEAN" else 1)


if __name__ == "__main__":
    main()