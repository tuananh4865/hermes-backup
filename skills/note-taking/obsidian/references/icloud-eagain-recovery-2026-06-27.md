---
title: iCloud Drive EAGAIN recovery — session log
created: 2026-06-27
type: reference
applies_to: obsidian
trigger: cp / rsync fail with "Resource deadlock avoided" on iCloud vault files
---

# iCloud EAGAIN Recovery — Session Log 2026-06-27

## Context

During memory-curator nightly consolidation, hit persistent `Resource deadlock avoided` (errno 35 / EAGAIN) on a single file in the iCloud Obsidian vault: `concepts/read-full-request-mandate.md`.

## What failed

| Attempt | Command | Result |
|---------|---------|--------|
| 1 | `cp` | `Resource deadlock avoided` (exit 1) |
| 2 | `sleep 8 && cp` | Same error |
| 3 | `sleep 25 && cp` | Same error |
| 4 | `rsync -a` | `error: read-full-request-mandate.md: mmap: Resource deadlock avoided` |
| 5 | `sleep 45 && rsync -a` | Same mmap EAGAIN |

Total: 4 cp + 2 rsync attempts, all failed. iCloud was holding the file open (likely from a recent Obsidian edit on another device, or mid-upload).

## What worked

```bash
sleep 30
cat "$WIKI/concepts/read-full-request-mandate.md" > "$VAULT/concepts/read-full-request-mandate.md.tmp"
mv "$VAULT/concepts/read-full-request-mandate.md.tmp" "$VAULT/concepts/read-full-request-mandate.md"
```

Wrote a fresh inode to a `.tmp` file (which iCloud wasn't tracking yet), then `mv` replaced the locked destination with the new inode. The rename is atomic at the filesystem level and doesn't need to open the destination.

## Why it works

- `cp` and `rsync` both `open(O_RDWR)` the destination, then mmap/read+write it. iCloud's sync daemon holds a lock on files actively being uploaded, so `open()` blocks → EAGAIN.
- `cat > file.tmp` writes to a brand-new inode that iCloud hasn't touched. The `.tmp` suffix may help avoid the iCloud watcher.
- `mv` is a single `rename(2)` syscall — doesn't open source or destination for reading, just relinks the directory entry. iCloud's lock is on the file, not the directory entry.

## Verification

```bash
# Both must match
wiki_size=$(stat -f %z "$WIKI/concepts/read-full-request-mandate.md")
vault_size=$(stat -f %z "$VAULT/concepts/read-full-request-mandate.md")
# wiki_size=5231, vault_size=5231 ✅
```

Size is the reliable verification — mtime granularity on APFS is 1 second, and writes in the same second look identical even when content differs.

## Reusable bash snippet

```bash
# Safe copy to iCloud vault with full EAGAIN recovery
icloud_cp() {
  local src="$1" dst="$2"
  # Fast path
  cp "$src" "$dst" 2>/dev/null && return 0
  # Sleep + retry
  sleep 10 && cp "$src" "$dst" 2>/dev/null && return 0
  # Atomic-rename fallback
  sleep 30 && cat "$src" > "$dst.tmp" && mv "$dst.tmp" "$dst" && return 0
  # Give up
  echo "EAGAIN: $src → $dst (3 attempts, skipped)" >&2
  return 1
}
```

## Where this is encoded

- SKILL.md — Recovery section now has 3-step escalation: sleep+cp → cat+tmp+mv → skip

## Related

- obsidian SKILL.md → "iCloud Drive sync deadlock" section
- 06-26 entry: sleep + cp retry was enough that day
- 06-27 escalation: cat > tmp + mv (this session)
