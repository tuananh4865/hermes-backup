# ASCII Video Reference

Formerly a standalone skill. Content absorbed into `ascii-art`.

## Overview

Convert video or audio to ASCII animated output (MP4/GIF).

## Tools

- `ascii-video` skill — main tool
- `ffmpeg` — video processing backend

## Common Workflow

```bash
# Convert video to ASCII MP4
ffmpeg -i input.mp4 -vf "ascii" output.mp4

# Convert audio to ASCII waveform GIF
ascii-video audio2gif input.mp3 output.gif
```

## Tips

- Higher resolution input = more detailed ASCII output
- Use `-r 15` to reduce frame rate for smaller output
- Grayscale ASCII works better than colored for readability
