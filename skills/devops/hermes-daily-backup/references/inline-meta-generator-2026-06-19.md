# Inline Content Creator Metadata Generator (Fallback)

**When to use:** `scripts/sync-content-creator-meta.sh` is referenced by `hermes-daily-backup` SKILL.md pitfall #13 but **not yet bundled**. Use this inline generator until the script ships.

## Source

`~/Workspace/Claude/Projects/Content Creator/` — Content Creator project workspace.

## Anti-pattern rules (MUST respect)

- **Metadata ONLY** — structure + sizes + fingerprints. NO file contents.
- **Do NOT commit `.md` body content** — research files may contain unreleased scripts, deal links, internal notes.
- **Idempotent** — safe to re-run daily; date-stamped filenames preserve history.

## Path A: Inline Python (richest output — preferred when Python is available)

This is the version that ran successfully on **2026-06-20** (24 files CC meta snapshot,
8 .md files, 62691 bytes, 5 dirs). Drop into an `execute_code` call:

```python
import json, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

CC_DIR = Path.home() / "Workspace/Claude/Projects/Content Creator"
OUT_DIR = Path.home() / ".hermes/backups/content-creator-meta-2026-06-20"
OUT_DIR.mkdir(parents=True, exist_ok=True)

date_str = "2026-06-20"
now = datetime.now(timezone.utc).isoformat()

# --- Tree (structure + sizes, no content) ---
tree_lines = []
file_count = 0
total_bytes = 0
file_types = {}
dir_count = 0

for root, dirs, files in os.walk(CC_DIR):
    dirs.sort()
    rel = Path(root).relative_to(CC_DIR)
    depth = len(rel.parts)
    indent = "  " * depth
    dir_name = rel.parts[-1] if rel.parts else "Content Creator"
    tree_lines.append(f"{indent}[D] {dir_name}/")
    dir_count += 1
    for f in sorted(files):
        fp = Path(root) / f
        try:
            sz = fp.stat().st_size
        except OSError:
            sz = -1
        total_bytes += max(sz, 0)
        file_count += 1
        ext = Path(f).suffix.lower() or "(no ext)"
        file_types[ext] = file_types.get(ext, 0) + 1
        tree_lines.append(f"{indent}  [F {sz:>7}B] {f}")

tree_text = "\n".join(tree_lines) + "\n"
(OUT_DIR / f"tree-{date_str}.txt").write_text(tree_text)

# --- Metadata JSON (path + size + mtime + sha1-4k fingerprint, no content) ---
files_meta = []
for root, dirs, files in os.walk(CC_DIR):
    for f in sorted(files):
        fp = Path(root) / f
        rel = fp.relative_to(CC_DIR.parent)
        try:
            st = fp.stat()
            sz = st.st_size
            mtime = datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat()
            # sha1 of FIRST 4KB only (fingerprint without reading full content)
            h = hashlib.sha1()
            with open(fp, "rb") as fh:
                h.update(fh.read(4096))
            sha1_short = h.hexdigest()[:12]
        except OSError:
            sz, mtime, sha1_short = -1, "", ""
        files_meta.append({
            "path": str(rel),
            "size": sz,
            "mtime": mtime,
            "sha1_4k": sha1_short,
        })

metadata = {
    "snapshot_date": date_str,
    "generated_at": now,
    "source_dir": str(CC_DIR),
    "totals": {
        "files": file_count,
        "dirs": dir_count,
        "bytes": total_bytes,
        "file_types": dict(sorted(file_types.items(), key=lambda x: -x[1])),
    },
    "files": files_meta,
    "notes": "METADATA ONLY — no file contents. fingerprint = sha1 of first 4KB.",
}

(OUT_DIR / f"metadata-{date_str}.json").write_text(
    json.dumps(metadata, indent=2, ensure_ascii=False)
)
```

**Output schema:**
- `tree-<date>.txt` — human-readable, indented `[D] dirname/` and `[F size B] filename`
- `metadata-<date>.json` — structured: `totals` (files, dirs, bytes, file_types) + per-file `path/size/mtime/sha1_4k`

**Why `sha1_4k` not full sha1:** full content hashing reads every byte into memory (fine for 60KB but wasteful for bigger folders); 4KB prefix is enough to detect file identity changes and stays cheap. If exact dup-detection matters, swap `fh.read()` (no arg) for `fh.read(4096)`.

## Path B: Shell-only (no Python dependency)

For environments where Python is missing or `execute_code` is restricted. Output is less rich (no per-file sha1, no mtime) but still satisfies the "structure only" rule:

```bash
CC_DIR="$HOME/Workspace/Claude/Projects/Content Creator"
DATE="2026-06-20"
OUT="$HOME/.hermes/backups/content-creator-meta-$DATE"
mkdir -p "$OUT"

find "$CC_DIR" \( -type f -o -type d \) | sort | while read -r p; do
  if [ -d "$p" ]; then
    echo "[D] ${p#$CC_DIR/}/"
  else
    sz=$(stat -f%z "$p" 2>/dev/null || stat -c%s "$p")
    rel=${p#$CC_DIR/}
    printf "[F %7d B] %s\n" "$sz" "$rel"
  fi
done > "$OUT/tree-$DATE.txt"
```

Then commit `tree-<date>.txt` to `content-creator-meta` branch as before. Skip JSON metadata (or write a stub manually).

## Integration with the multi-branch cron flow

After generator runs:

```bash
# Still on content-creator-meta branch
cp ~/.hermes/backups/content-creator-meta-<date>/metadata-<date>.json \
   ~/.hermes/content-creator-meta/metadata-<date>.json
cp ~/.hermes/backups/content-creator-meta-<date>/metadata-<date>.json \
   ~/.hermes/content-creator-meta/metadata.json    # latest snapshot
cp ~/.hermes/backups/content-creator-meta-<date>/tree-<date>.txt \
   ~/.hermes/content-creator-meta/tree-<date>.txt
cp ~/.hermes/backups/content-creator-meta-<date>/tree-<date>.txt \
   ~/.hermes/content-creator-meta/tree.txt        # latest snapshot
cd ~/.hermes
git add content-creator-meta/
git commit -m "Sync content-creator meta: <date>"
git push origin content-creator-meta
git checkout main
```

The date-stamped files preserve history (each day you can diff `metadata-2026-06-19.json` vs `metadata-2026-06-20.json` to see what changed), while the no-date files give a quick "current state" view.
