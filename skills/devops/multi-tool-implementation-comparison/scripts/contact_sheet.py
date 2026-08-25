#!/usr/bin/env python3
"""
Build N-tool × M-timestamp contact sheet for visual comparison.
Usage: python3 contact_sheet.py <tools.json> <out.jpg>

tools.json format:
{
  "REMOTION": "/path/to/file.mp4",
  "MANIM": "/path/to/another.mp4",
  "HYPERFRAMES": "/path/to/third.mp4"
}

Defaults to 4 timestamps aligned to scene midpoints: 3, 13, 17, 26s.
"""
import json, sys, os, subprocess, math
from PIL import Image, ImageDraw, ImageOps

if len(sys.argv) < 3:
    print("Usage: python3 contact_sheet.py <tools.json> <out.jpg>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    tools = json.load(f)

out_jpg = sys.argv[2]
SAMPLES = [3, 13, 17, 26]  # 4 timestamps aligned to scene midpoints
TILE = 640
GAP = 12
H_LABEL = 48
W = len(tools) * TILE + (len(tools)+1) * GAP
H = H_LABEL + len(SAMPLES) * (TILE + GAP) + GAP + 60

tmpdir = '/tmp/_contact_sheet_frames'
os.makedirs(tmpdir, exist_ok=True)

imgs = {}
for tool, path in tools.items():
    for ts in SAMPLES:
        fn = f'{tmpdir}/{tool.lower()}_t{ts}.jpg'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(ts),
                        '-i', path, '-frames:v', '1', '-q:v', '2', fn], check=False)
        if os.path.exists(fn):
            imgs[(tool, ts)] = Image.open(fn).convert('RGB')
            print(f'{tool} @ {ts}s -> {imgs[(tool, ts)].size}')

sheet = Image.new('RGB', (W, H), (15, 15, 15))
dr = ImageDraw.Draw(sheet)

# Column headers
for ci, tool in enumerate(tools.keys()):
    x = GAP + ci * (TILE + GAP)
    dr.text((x + 16, 12), tool, fill='#aaffaa')

# Row labels + frames
for ri, ts in enumerate(SAMPLES):
    y = H_LABEL + GAP + ri * (TILE + GAP)
    dr.text((GAP, y + TILE//2), f't = {ts}s', fill='#ffaa00')
    for ci, tool in enumerate(tools.keys()):
        im = imgs.get((tool, ts))
        if im is None:
            continue
        iw, ih = im.size
        scale = min(TILE/iw, TILE/ih)
        nw, nh = int(iw*scale), int(ih*scale)
        resized = im.resize((nw, nh), Image.LANCZOS)
        x = GAP + ci * (TILE + GAP) + (TILE - nw)//2
        sheet.paste(resized, (x, y))

# Footer
ts_list = SAMPLES
dr.text((GAP, H - 50),
        f'Samples: {ts_list[0]}s • {ts_list[1]}s • {ts_list[2]}s • {ts_list[3]}s (mid-scene)',
        fill='#888')

sheet.save(out_jpg, quality=82)
print(f'Wrote {out_jpg}: {os.path.getsize(out_jpg)/1024:.1f} KB')