#!/usr/bin/env python3
"""3-way side-by-side comparison contact sheet for trailer/motion graphics QA.

Use case: After rendering trailer, generate a vision-AI-evaluable contact sheet
showing reference vs my version(s) at the same timestamps.

Usage:
    python3 trailer_contact_compare.py \\
        --ref /path/to/reference.mp4 \\
        --my /path/to/my.mp4 \\
        --out /tmp/compare.jpg \\
        --timestamps 4 8 13 17 25

Produces a JPG with vertical stack of timestamp rows. Left = reference, right = my.
"""
import os, math, subprocess, argparse, json
from PIL import Image, ImageDraw, ImageOps

def extract_frames(video_path: str, timestamps: list, out_dir: str, prefix: str) -> list:
    os.makedirs(out_dir, exist_ok=True)
    out = []
    for ts in timestamps:
        fn = f'{out_dir}/{prefix}_{ts}.jpg'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(ts),'-i', video_path,
                        '-frames:v','1','-vf','scale=540:-1', fn], check=False)
        if os.path.exists(fn):
            out.append(fn)
    return out

def build_contact(mapping: list, out_path: str, TILE: int = 540, GAP: int = 12, BG=(8,8,8)):
    """mapping = list of (label, [path_or_None, path_or_None]) tuples"""
    cols = max(len(item[1]) for item in mapping)
    LABEL_H = 40
    GROUP_H = 32
    W = cols * TILE + (cols+1) * GAP
    H = LABEL_H + len(mapping) * (GROUP_H + TILE + GAP) + GAP
    s = Image.new('RGB', (W, H), BG)
    dr = ImageDraw.Draw(s)
    headers = ['REFERENCE'] + ['MY']*(cols-1)
    for ci, h in enumerate(headers):
        x = GAP + ci * (TILE + GAP)
        dr.text((x + 10, 8), h, fill='#88ff88')
    for ri, (label, paths) in enumerate(mapping):
        y = LABEL_H + GAP + ri * (GROUP_H + TILE + GAP)
        dr.text((GAP + 8, y + 8), label, fill='#ffaa00')
        for ci, p in enumerate(paths):
            if not p or not os.path.exists(p): continue
            im = ImageOps.fit(Image.open(p).convert('RGB'), (TILE, TILE), Image.LANCZOS)
            x = GAP + ci * (TILE + GAP)
            s.paste(im, (x, y + GROUP_H))
    s.save(out_path, quality=88)
    print(f'Wrote {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', required=True, help='Reference MP4')
    ap.add_argument('--my',  required=True, help='My MP4')
    ap.add_argument('--out', default='/tmp/trailer_compare.jpg')
    ap.add_argument('--frames-dir', default='/tmp/trailer_compare_frames')
    ap.add_argument('--timestamps', nargs='+', type=int,
                    default=[4, 8, 13, 17, 25, 28],
                    help='Timestamps to extract (seconds)')
    args = ap.parse_args()
    ref_frames = extract_frames(args.ref, args.timestamps, args.frames_dir, 'ref')
    my_frames  = extract_frames(args.my,  args.timestamps, args.frames_dir, 'my')
    mapping = []
    for i, ts in enumerate(args.timestamps):
        label = f't = {ts}s'
        ref_path = ref_frames[i] if i < len(ref_frames) else None
        my_path  = my_frames[i]  if i < len(my_frames)  else None
        mapping.append((label, [ref_path, my_path]))
    build_contact(mapping, args.out)
    print(json.dumps({'mapping': mapping, 'out': args.out}, indent=2))

if __name__ == '__main__':
    main()