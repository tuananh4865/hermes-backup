#!/usr/bin/env python3
"""
generate_transcript_md.py — Convert Whisper JSON → paragraph-format Markdown
Usage: python3 generate_transcript_md.py <whisper.json> <output.md>
"""
import sys
import json
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_transcript_md.py <whisper.json> <output.md>",
              file=sys.stderr)
        sys.exit(1)

    whisper = Path(sys.argv[1])
    output = Path(sys.argv[2])

    if not whisper.exists():
        print(f"❌ Whisper JSON not found: {whisper}", file=sys.stderr)
        sys.exit(1)

    with open(whisper) as f:
        d = json.load(f)

    segs = d.get('segments', [])
    if not segs:
        print("❌ No segments in Whisper output", file=sys.stderr)
        sys.exit(1)

    total_dur = segs[-1]['end']

    with open(output, 'w') as out:
        out.write(f'# Transcript — {total_dur:.1f}s total, {len(segs)} segments\n\n')
        out.write('---\n\n')
        for i, s in enumerate(segs):
            start = s['start']
            end = s['end']
            text = s['text'].strip()
            words = s.get('words', [])
            word_count = len(words) if words else len(text.split())
            out.write(f'### Segment {i:03d} [{start:.1f}s - {end:.1f}s] ({word_count} words)\n\n')
            out.write(f'{text}\n\n')
            if words:
                out.write('<details><summary>Word-level timestamps</summary>\n\n')
                out.write('| Word | Start | End |\n|------|------:|------:|\n')
                for w in words:
                    ws = w.get('start', 0)
                    we = w.get('end', 0)
                    wtext = w.get('word', '').strip()
                    out.write(f'| `{wtext}` | {ws:.2f}s | {we:.2f}s |\n')
                out.write('\n</details>\n\n')

    print(f'Generated transcript.md ({len(segs)} segments, {total_dur:.1f}s)')


if __name__ == '__main__':
    main()
