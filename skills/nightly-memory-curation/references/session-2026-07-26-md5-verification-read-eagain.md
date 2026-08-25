# Session 2026-07-26 02:00 — MD5 verification reads can EAGAIN (L59)

## What happened

Synthesis-mode main pass consolidating 2 active Telegram sessions from 2026-07-25:
- `20260725_125025_4f70fed0` (3h, 147 msg, 74 tool calls) — 4-SP script writing batch
- `20260725_162505_28bfb07b` (~50m, 182 msg, 99 tool calls) — 7-clip edit batch

**Output:**
- 2 new concept pages (`tiktok-product-script-batch-4-products-2026-07-25.md` 5489B + `clip-7-edit-batch-shipped-2026-07-25.md` 5156B)
- 3 updated pages (log.md, learned-about-tuananh.md with L62-L67, index.md)
- 5 files mirrored to vault

## The L59 surprise

After successfully mirror-write on all 5 files (4 with `cp -f` first-try, 1 with `cat>tmp+mv` atomic-rename after cp EAGAIN'd), the post-mirror verification loop hit an unexpected failure:

```bash
$ md5 -q "$SRC/entities/learned-about-tuananh.md" "$VAULT/learned-about-tuananh.md"
md5: /Users/tuananh4865/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/learned-about-tuananh.md: Resource deadlock avoided
```

The 113KB `learned-about-tuananh.md` file had just been successfully written via `cat>tmp+mv` (atomic-rename). MD5 returned `Resource deadlock avoided` on the read — same errno 35 / EAGAIN that affects `cp`, but on the **verification read** instead of the write.

The reason: macOS BSD `md5` mmaps the file for performance. mmap against an iCloud-locked inode returns EAGAIN, same as the write-side lock the L53 escalation pattern already documents.

## Recovery: 2-tier verification stack

After 3 retries with `sleep 30 + sleep 60 + sleep 30` (all returned EAGAIN), the curator fell back to `cmp -s`:

```bash
$ cmp -s "$SRC/entities/learned-about-tuananh.md" "$VAULT/learned-about-tuananh.md"
$ echo $?
0   # exit 0 = byte-identical
```

**Why `cmp -s` works when `md5` doesn't:** `cmp` uses POSIX `open(2)` + sequential `read(2)` syscalls. macOS `md5` (BSD) mmap's the file. Different syscall path, different failure surface.

**Caveat (Linux):** GNU `md5sum` on Linux does NOT mmap by default, so it typically succeeds where macOS `md5` EAGAINs. This lesson is macOS-specific. Verify with `which md5` before assuming.

## Lesson captured (L59)

> **Verification is a 2-tier stack.** md5 first (fast, mmap-based, can EAGAIN mid-day on macOS iCloud paths) → cmp -s as the safety net (slow, sequential-read, always works). A curator pass that ends with "md5 EAGAIN'd and I gave up" is NOT a valid termination — fall back to cmp -s before declaring done.

Updated in SKILL.md:
- § 5b verification hierarchy now lists `cmp -s` as #1 fallback below md5
- New anti-pattern entry: "Treating md5 verification failure as terminal (L59 — extends L53/L36)"
- New bullet in the Verification checklist: "Final byte-identical gate PASSED via md5 OR cmp -s"

## Verification table

| File | md5 first-try | md5 EAGAIN | cmp -s fallback | Final result |
|---|---|---|---|---|
| `concepts/tiktok-product-script-batch-4-products-2026-07-25.md` | ✓ | — | — | PASS |
| `concepts/clip-7-edit-batch-shipped-2026-07-25.md` | ✓ | — | — | PASS |
| `log.md` | ✓ | — | — | PASS |
| `entities/learned-about-tuananh.md` | — | 3x EAGAIN | ✓ exit 0 | PASS via fallback |
| `index.md` | ✓ | — | — | PASS |

**Total:** 5/5 files byte-identical. 4 verified via md5 first-try, 1 verified via cmp -s after md5 EAGAIN'd.

## When to re-read this reference

- When `md5 -q` returns `Resource deadlock avoided` on a vault file that was JUST successfully written — this is the L59 pattern, not a fresh EAGAIN
- When designing any new curator verification script — use `cmp -s` as the safety net, not just md5
- When porting the curator pattern from macOS to Linux — the macOS-specific md5 EAGAIN does NOT apply to GNU md5sum, but `cmp -s` is still the universal safety net
- When upgrading `safe-mirror.sh` or `safe-mirror-set-diff.sh` scripts — add cmp -s fallback to the verification step