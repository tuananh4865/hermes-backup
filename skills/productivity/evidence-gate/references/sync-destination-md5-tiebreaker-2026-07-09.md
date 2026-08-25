---
title: Sync destination verification — md5 content tiebreaker for iCloud / Dropbox / GDrive
created: 2026-07-09
type: reference
applies_to: evidence-gate
trigger: Mirror or sync operations to iCloud-monitored / Dropbox / Google Drive / OneDrive / Synology Drive destinations — when size+mtime verification is INSUFFICIENT.
related_skill: physical-product-ecommerce-content (no), obsidian (parent of original observation site)
---

# Sync Destination Verification — md5 Content Tiebreaker

## The pitfall (compressed)

When the **destination** of a copy / sync operation is a path that lives under a cloud-sync daemon (iCloud Drive, Dropbox, Google Drive, OneDrive, Synology Drive, Box, etc.), **size+mtime verification will report false-positive drift**.

Concretely:
- The daemon opens the dst file with `O_RDWR` and holds an mmap handle while uploading to the cloud.
- Your `cp` succeeds (exit 0, file written).
- Seconds later, the daemon closes the fd, which macOS/APFS records as an mtime touch.
- Now `stat -f %Sm` shows dst mtime = src mtime + 2s, while `stat -f %z` shows identical byte count.
- A naive evidence-gate pass would either (a) panic about the mtime diff, or (b) declare the size match good enough.

**Neither is correct.** The actual content is identical. You need a deterministic content verifier: `md5 -q`.

## The fix (canonical command)

```bash
# Drop-in for sync-destination verification, replacing stat-based checks
src_md5=$(md5 -q "$src" 2>/dev/null)
dst_md5=$(md5 -q "$dst" 2>/dev/null)
if [ "$src_md5" = "$dst_md5" ] && [ -n "$src_md5" ]; then
  echo "OK md5=$src_md5 $(basename "$src")"
  return 0
else
  echo "DRIFT src=$src_md5 dst=$dst_md5 $(basename "$src")"
  # Fall back to EAGAIN recovery (sleep + retry, cat > tmp + mv)
  return 1
fi
```

## Decision tree (which verifier, when)

```
Mirror succeeded?
├── cp returned exit 1 → EAGAIN recovery (sleep + retry, cat > tmp + mv)
│
└── cp returned exit 0
    ├── Is dst under a cloud-sync daemon? (iCloud / Dropbox / GDrive / etc.)
    │   ├── YES → ALWAYS run md5 -q first
    │   │   ├── md5 match → OK, mtime drift is benign (iCloud metadata refresh)
    │   │   └── md5 mismatch → real DRIFT, fall back to EAGAIN recovery + cat>tmp+mv
    │   │
    │   └── NO → standard stat-based check is reliable
    │       ├── size + mtime match → OK
    │       ├── size match only → re-cp + verify (rare, but indicates partial write)
    │       └── size mismatch → cp failed silently, retry with verbose flags
    │
    └── For HIGH-STAKES local files (config, cron, skill patches)
        → Still prefer md5 over stat (cost ~5ms, catches 100% of corruption classes)
```

## Why md5 is the decisive verifier (cost/benefit)

| Metric | Granularity | Catches truncation | Catches zero-byte | Catches content drift | Speed |
|---|---|---|---|---|---|
| `stat -f %z` (size) | exact byte | ✅ | ✅ | ❌ false-negative risk if dst is right-size wrong-bytes | O(1) |
| `stat -f %Sm` (mtime) | 1 second (APFS) | ❌ | ❌ | ❌ unreliable on iCloud dst | O(1) |
| `md5 -q` | exact byte | ✅ | ✅ | ✅ only deterministic verifier | ~5ms / MB |

For sync-destination verification, the 5ms cost is negligible compared to the cost of shipping a stale page to the vault and discovering the drift in 3 days.

## Companion: icloud-EAGAIN-recovery (handled separately)

This skill covers **what to do when cp APPEARS TO SUCCEED** (silent drift, metadata touch). The companion reference file under `note-taking/obsidian/SKILL.md` (`references/icloud-eagain-recovery-2026-06-27.md`) covers **what to do when cp FAILS LOUDLY** (Resource deadlock avoided, mmap EAGAIN).

Both are needed for a robust iCloud-mirror pipeline:

```
Mirror INTO iCloud vault
  ↓
cp -f returned exit 0?
  ├── NO  → EAGAIN flow (sleep + retry, cat > tmp + mv, give up after 3 attempts)
  └── YES → verify with md5 -q  ← THIS SKILL COVERS
            ├── md5 match → OK
            └── md5 mismatch → fall back to EAGAIN flow + cat > tmp + mv
```

## Reusable bash: full sync pipeline with both gates

```bash
#!/usr/bin/env bash
# Mirror one file into a cloud-monitored dst with EAGAIN + md5 gates.
# Returns 0 on confirmed OK, 1 on permanent failure.

mirror_with_gates() {
  local src="$1" dst="$2"
  # Gate 1: loud-failure recovery (EAGAIN)
  for attempt in 1 2 3; do
    cp -f "$src" "$dst" 2>/dev/null && break
    case "$attempt" in
      1) sleep 10 ;;
      2) sleep 30; cat "$src" > "$dst.tmp" && mv "$dst.tmp" "$dst" && break ;;
      3) echo "EAGAIN permanent failure: $src" >&2; return 1 ;;
    esac
  done

  # Gate 2: content-match verification (md5)
  local src_md5 dst_md5
  src_md5=$(md5 -q "$src" 2>/dev/null)
  dst_md5=$(md5 -q "$dst" 2>/dev/null)
  if [ "$src_md5" = "$dst_md5" ] && [ -n "$src_md5" ]; then
    echo "OK md5=$src_md5 $(basename "$src")"
    return 0
  else
    echo "DRIFT src=$src_md5 dst=$dst_md5 $(basename "$src")" >&2
    return 1
  fi
}

# Batch usage: mirror many files with sequential sleep between (avoid concurrent iCloud file locks)
SRC_ROOT="/Volumes/Storage-1/Hermes/wiki"
DST_ROOT="/Users/tuananh4865/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain"
for f in $SRC_ROOT/concepts/foo.md $SRC_ROOT/concepts/bar.md; do
  sleep 3
  rel="${f#$SRC_ROOT/}"
  mirror_with_gates "$f" "$DST_ROOT/$rel" || echo "skipped: $f"
done
```

## Origin (2026-07-09 02:00 curator pass)

The cron memory-curator nightly run on 2026-07-09 mirrored 7 files from `/Volumes/Storage-1/Hermes/wiki/` → iCloud Obsidian vault. Initial stat-based verification reported "MISMATCH" on all 7 (size match, dst mtime +2s). Without this skill, the curator would either:
- (a) panic and ship a stale claim of "drift detected, run recovery", polluting the curator log, or
- (b) ship a "size matches, OK" claim that's correct by chance but leaves an unverified assumption.

md5 was added to the verification step. All 7 files confirmed identical bytes. Curator pass shipped clean. Total overhead: ~5s for 7 files.

## Where this should NOT apply

- **Local file writes** (within `/Volumes/Storage-1/Hermes/wiki/` or any non-cloud-monitored path) — `stat -f %z` and `stat -f %Sm` are reliable. md5 is overkill.
- **Git commits / pushes** — `git log -1` + `git ls-remote` are the natural verifiers (decisive at the protocol level). md5 of working tree files is redundant.
- **DB row writes** — `SELECT count(*) WHERE id = X` is the natural verifier.

This reference is **destination-specific**: any code path ending in a write to iCloud/Dropbox/GDrive/OneDrive/Synology-monitored directory MUST use md5 as final gate.

## Related

- `references/icloud-eagain-recovery-2026-06-27.md` (in `note-taking/obsidian/SKILL.md`) — companion: loud-failure recovery for the same destination class.
- `SKILL.md` § "Anti-Patterns to Avoid" pitfall #8 — preferred embedding over a separate reference.
- `SKILL.md` § "Verification Checklist" — explicit checkbox for sync destinations.
- `SKILL.md` § "Quick-Reference" table — row for "Sync destinations (iCloud et al.)".
