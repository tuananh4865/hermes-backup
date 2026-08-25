#!/usr/bin/env python3
"""
Static logo inpaint per frame (verified work 24/07 on lGZQgDMMMac).
- Logo box: x, y, w, h (with 10px padding)
- Inpaint Telea radius 7
- Background-comparison mask
- Re-encode with original audio

Use: /opt/homebrew/bin/python3 scripts/static_logo_inpaint.py
"""
import cv2
import numpy as np
import subprocess
import os
import sys

# Defaults from 24/07 verified run — override via sys.argv or edit here
VIDEO = "/Volumes/Storage-1/Tiktok-Tuan-Anh/lGZQgDMMMac_iphone.mp4"
VOICE = "/Volumes/Storage-1/Hermes/scratch/voice-clone/clip_lgz_question.wav"
OUT = "/Volumes/Storage-1/Tiktok-Tuan-Anh/lGZQgDMMMac_no_wm_v2.mp4"

# Logo SB: x=22-135, y=531-663, size 113x132 (verify before use)
LOGO_X, LOGO_Y = 22, 531
LOGO_W, LOGO_H = 113, 132
PAD = 10

if os.path.exists(OUT):
    os.remove(OUT)

# Get FPS and duration
fps_str = subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0",
     "-show_entries", "stream=avg_frame_rate",
     "-of", "default=nw=1:nk=1", VIDEO],
    capture_output=True, text=True
).stdout.strip()
FPS = float(fps_str.split('/')[0]) / float(fps_str.split('/')[1])

v_dur_str = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=nw=1:nk=1", VIDEO],
    capture_output=True, text=True
).stdout
v_dur = float(v_dur_str.strip()) if v_dur_str else 0.0

print(f"Video: {v_dur:.2f}s, FPS: {FPS}")

# Extract frames
print("\n=== Extract frames ===")
FRAME_DIR = "/tmp/lgz_frames"
os.makedirs(FRAME_DIR, exist_ok=True)
for f in os.listdir(FRAME_DIR):
    os.remove(f"{FRAME_DIR}/{f}")
subprocess.run(
    ["ffmpeg", "-y", "-i", VIDEO, "-vsync", "0", f"{FRAME_DIR}/frame_%05d.png"],
    capture_output=True, text=True
)
total = len(os.listdir(FRAME_DIR))
print(f"Total frames: {total}")

# Inpaint
x1, y1 = max(0, LOGO_X - PAD), max(0, LOGO_Y - PAD)
x2, y2 = LOGO_X + LOGO_W + PAD, LOGO_Y + LOGO_H + PAD

PROCESSED_DIR = "/tmp/lgz_processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)
for f in os.listdir(PROCESSED_DIR):
    os.remove(f"{PROCESSED_DIR}/{f}")

print("\n=== Inpaint ===")
for i in range(total):
    frame_path = f"{FRAME_DIR}/frame_{i:05d}.png"
    if not os.path.exists(frame_path):
        continue
    frame = cv2.imread(frame_path)
    if frame is None:
        continue

    roi = frame[y1:y2, x1:x2].copy()
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Background sample from outer edges
    edges = np.concatenate([
        gray_roi[:PAD, :].flatten(),
        gray_roi[-PAD:, :].flatten(),
        gray_roi[:, :PAD].flatten(),
        gray_roi[:, -PAD:].flatten()
    ])
    bg = np.median(edges)
    bg_std = np.std(edges)

    mask = (np.abs(gray_roi.astype(float) - bg) > max(15, bg_std * 2)).astype(np.uint8) * 255
    bright_mask = ((gray_roi > 80) & (gray_roi < 230)).astype(np.uint8) * 255
    mask = cv2.bitwise_or(mask, bright_mask)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)

    inpainted = cv2.inpaint(roi, mask, 7, cv2.INPAINT_TELEA)
    frame[y1:y2, x1:x2] = inpainted

    cv2.imwrite(f"{PROCESSED_DIR}/frame_{i:05d}.png", frame)

print(f"Processed {total} frames")

# Re-encode with optional voice overlay
if os.path.exists(VOICE):
    vo_dur_str = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", VOICE],
        capture_output=True, text=True
    ).stdout
    vo_dur = float(vo_dur_str.strip()) if vo_dur_str else 0.0
    FADE_DUR = 2.0

    AUDIO_TMP = "/tmp/lgz_audio.m4a"
    subprocess.run(
        ["ffmpeg", "-y", "-i", VIDEO, "-vn", "-c:a", "copy", AUDIO_TMP],
        capture_output=True, text=True
    )

    filter_complex = (
        f"[1:a]aresample=44100,afade=t=out:st={vo_dur - 0.03}:d=0.03,"
        f"apad=whole_dur={v_dur},volume=1.4[voice];"
        f"[2:a]aresample=44100,"
        f"volume='if(lt(t,0.0),1,if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,{vo_dur}),0,if(lt(t,{vo_dur+FADE_DUR}),(t-{vo_dur})/{FADE_DUR},1))))'"
        f":eval=frame[audio];"
        f"[voice][audio]amix=inputs=2:duration=longest:dropout_transition=0[mix];"
        f"[mix]aresample=44100,pan=stereo|c0=c0|c1=c0[out]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", f"{PROCESSED_DIR}/frame_%05d.png",
        "-i", VOICE, "-i", AUDIO_TMP,
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT
    ]
else:
    # No voice, just extract audio
    AUDIO_TMP = "/tmp/lgz_audio.m4a"
    subprocess.run(
        ["ffmpeg", "-y", "-i", VIDEO, "-vn", "-c:a", "copy", AUDIO_TMP],
        capture_output=True, text=True
    )
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", f"{PROCESSED_DIR}/frame_%05d.png",
        "-i", AUDIO_TMP,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT
    ]

print(f"\n=== Re-encode ===")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
print(f"Exit: {result.returncode}")

if os.path.exists(OUT):
    print(f"\n✅ {OUT} ({os.path.getsize(OUT)/1024/1024:.2f} MB)")
