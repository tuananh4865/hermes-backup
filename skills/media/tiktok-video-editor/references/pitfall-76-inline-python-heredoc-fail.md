# PITFALL #76 — Inline Python heredoc + f-string quote escape (v0.01)

## Reproducible shell bug
Trong `transcribe.sh`, em viết:
```bash
python3 -c "
import json, re
with open('$JSON') as f: d = json.load(f)
segs = d.get('segments', [])
md_path = '$WORK/transcript.md'
with open(md_path, 'w') as out:
    out.write(f'# Transcript — {segs[-1][\"end\"]:.1f}s total, {len(segs)} segments\n\n')
    ...
"
```

Output: `transcribe.sh: line 57: {wtext}: command not found` — bash interprets `{wtext}` as command substitution.

Bug: Triple-quoted f-string trong bash double-quoted heredoc có escape rules phức tạp. Backslash-escape `\"` trong Python bị bash ăn trước.

## Fix v0.01
Move Python code sang dedicated helper script:

`scripts/generate_transcript_md.py`:
```python
#!/usr/bin/env python3
import sys
import json
from pathlib import Path

def main():
    whisper = Path(sys.argv[1])
    output = Path(sys.argv[2])
    if not whisper.exists():
        print(f"❌ Whisper JSON not found: {whisper}", file=sys.stderr)
        sys.exit(1)
    with open(whisper) as f:
        d = json.load(f)
    segs = d.get('segments', [])
    if not segs:
        print("❌ No segments", file=sys.stderr)
        sys.exit(1)
    with open(output, 'w') as out:
        out.write(f'# Transcript — {segs[-1]["end"]:.1f}s total, {len(segs)} segments\n\n')
        # ... full Python code without bash escape
```

Trong shell:
```bash
python3 scripts/generate_transcript_md.py "$JSON" "$WORK/transcript.md"
```

## Bài học (universal shell pattern)
Khi cần inline Python trong bash script:
- ❌ `python3 -c "..."` với f-string có `\"` — bug-prone
- ❌ `python3 << 'EOF' ... EOF` (heredoc) với nested quotes — bug-prone
- ✅ ALWAYS viết dedicated `.py` file rồi `python3 script.py arg1 arg2`

Trade-off: thêm file `.py`, nhưng:
- Syntax highlight trong IDE
- Có thể `pytest`, lint, type-check
- Reusable cho sessions khác
- Shell invocation clear + chuẩn
