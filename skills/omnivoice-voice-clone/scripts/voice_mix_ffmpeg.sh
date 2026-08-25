#!/bin/bash
# voice_mix_ffmpeg.sh — Mix voice clone with original audio using piecewise volume
#
# PROBLEM this solves: ffmpeg `volume=enable='between':value` does NOT restore outside range.
# Use piecewise volume=expression (with :eval=frame) instead.
#
# Usage:
#   bash voice_mix_ffmpeg.sh <video> <voice.wav> <output.mp4>
#
# Voice runs 0-VO_DUR. Audio gốc: full 0-0s, fade out 0-0.3s, mute 0.3-VO_DUR, fade in VO_DUR-(VO_DUR+2), full after.
#
# Verified: 24/07 clip lGZQgDMMMac, voice 3.8s, fade in 2s.

set -e
VIDEO="$1"
VOICE="$2"
OUT="$3"
VO_DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VOICE" | tr -d '\n')
V_DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$VIDEO" | tr -d '\n')

ffmpeg -y \
  -i "$VIDEO" -i "$VOICE" \
  -filter_complex "
    [0:a]volume='if(lt(t,0.0),1,if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,${VO_DUR}),0,if(lt(t,${VO_DUR}+2),(t-${VO_DUR})/2,1))))':eval=frame[audio];
    [1:a]aresample=44100,afade=t=out:st=$(echo "$VO_DUR - 0.03" | bc):d=0.03,apad=whole_dur=${V_DUR},volume=1.4[voice];
    [voice][audio]amix=inputs=2:duration=longest:dropout_transition=0[mix];
    [mix]aresample=44100,pan=stereo|c0=c0|c1=c0[a]
  " \
  -map 0:v -map "[a]" \
  -c:v copy \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "$OUT"

echo "✅ ${OUT}"
