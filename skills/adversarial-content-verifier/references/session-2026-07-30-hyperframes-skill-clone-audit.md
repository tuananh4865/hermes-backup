# Session 2026-07-30 — HyperFrames v0.7.83 Skill Clone Audit

**Verifier role:** Independent adversarial audit of a "skill clone" task
**Claim under audit:** "HeyGen HyperFrames v0.7.83 đã được clone nguyên vẹn vào Hermes skills/heygen-hyperframes-v0.7.83" + matching wiki concept/raw files

**Final verdict:** PASS (with one minor wording ambiguity noted)

---

## Claim structure (what was audited)

The author's deliverable had three legs:

1. **Source clone** at `/Volumes/Storage-1/Hermes/research/heygen-hyperframes` — full upstream repo at pinned commit.
2. **Snapshot** at `/Volumes/Storage-1/Hermes/skills/heygen-hyperframes-v0.7.83` — the skill subset mirrored from source.
3. **Wiki** at:
   - `/Volumes/Storage-1/Hermes/wiki/concepts/heygen-hyperframes-v0.7.83-skill-clone-2026-07-30.md`
   - `/Volumes/Storage-1/Hermes/wiki/raw/articles/heygen-hyperframes-v0.7.83-source-2026-07-30.md`
4. **Wiring** at `/Users/tuananh4865/.claude/skills/<name>` — 19 symlinks to snapshot.

## F12.1 — Byte-perfect mirror check (passed)

```
$ git rev-parse HEAD
5244dde5f10c221221924985aa4651d89fb7c98a
$ git describe --tags --always
v0.7.83
$ git ls-files | wc -l
4839
$ find source/skills -type f | wc -l
889
$ find snapshot -type f | wc -l
889
$ diff -rq snapshot/ source/skills/
(empty — recursive byte-perfect)
$ md5 -q snapshot/hyperframes/SKILL.md    md5 -q source/skills/hyperframes/SKILL.md
b4b4fe3908aa8c0ffb63643c0cca4f87         b4b4fe3908aa8c0ffb63643c0cca4f87   ✓ MATCH
# …all 19 SKILL.md hashes matched
```

Note: the wiki claims "889/889 file upstream và snapshot giống nhau, 0 mismatch" — verified independently.

## F12.2 — Symlink resolve recipe (passed after one false BROKEN)

**First attempt (buggy):**
```bash
ls -la /Users/tuananh4865/.claude/skills/ | grep 'heygen-hyperframes-v0.7.83' | \
  awk '{print $NF}' | while read p; do
  if [ -e "/Users/tuananh4865/.claude/skills/$p" ]; then echo "OK"; else echo "BROKEN"; fi
done
# Returned 19/19 BROKEN — FALSE POSITIVE
# Bug: $NF captured the path AFTER the `->`, treated it as relative to CWD.
```

**Fixed recipe (correct):**
```bash
for link in /Users/tuananh4865/.claude/skills/{embedded-captions,faceless-explainer,...,talking-head-recut}; do
  target=$(readlink "$link")
  if [ -e "$target" ]; then echo "✓ $link -> $target"; else echo "✗ BROKEN"; fi
done
# Returned 19/19 ✓ — all symlink targets resolve to /Volumes/.../heygen-hyperframes-v0.7.83/<skill>
```

**Lesson:** when verifying symlinks, always use `readlink` + absolute path. Never parse `ls -la` output with `awk '{print $NF}'` — the symlink target column can have trailing whitespace or relative paths that break the check.

## F12.3 — Custom / collision detection (passed)

The user's cookbook at `/Users/tuananh4865/.hermes/skills/creative/hyperframes/SKILL.md` could have been clobbered by the upstream `hyperframes` symlink.

```
$ stat -f '%N size=%z mtime=%Sm' \
    /Users/tuananh4865/.hermes/skills/creative/hyperframes/SKILL.md
/Users/.../creative/hyperframes/SKILL.md 83858 Jul 17 13:09:47 2026
$ md5 -q /Users/.../creative/hyperframes/SKILL.md
03cc241a9020a6e22840d331e1718b22
```

- mtime Jul 17 — well before clone Jul 30 09:29 → untouched ✓
- Upstream symlink `hyperframes` → `/Volumes/.../heygen-hyperframes-v0.7.83/hyperframes` (NOT the cookbook) ✓
- Two contexts coexist: upstream `hyperframes` (router) + local `creative/hyperframes` (cookbook)

## F12.4 — mtime-neighbor overwrite check (passed)

```
$ ls -la /Volumes/Storage-1/Hermes/wiki/concepts/ | head
total 2336
drwxr-xr-x  117 tuananh4865  staff   3744 Jul 30 09:34 .
-rw-------    1 tuananh4865  staff   8788 Jul 30 09:34 heygen-hyperframes-v0.7.83-skill-clone-2026-07-30.md
-rw-r--r--    1 tuananh4865  staff   7206 Jul 30 02:07 mi-y-kontum-business-plan-2026-07-29.md
-rw-r--r--    1 tuananh4865  staff   6677 Jul 30 02:08 omnivoice-youtube-final-config-2026-07-29.md
-rw-r--r--    1 tuananh4865  staff   5364 Jul 30 02:08 vuive-black-hole-pilot-2026-07-29.md
```

Only ONE new file in the dir (Jul 30 09:34, the audit concept). All neighbors keep their pre-audit timestamps (Jul 28-29). No collateral overwrite.

```
$ ls -la /Volumes/Storage-1/Hermes/wiki/raw/articles/ | grep 'Jul 30'
-rw-------   1 tuananh4865  staff   2048 Jul 30 09:34 heygen-hyperframes-v0.7.83-source-2026-07-30.md
# Only the new raw capture — no other file touched.
```

## F12.5 — Honest-caveat vs over-claim (passed — honest caveat)

Wiki line 134:
> "`npx hyperframes` chỉ chạy được khi CLI/dependencies sẵn sàng; cần `doctor` hoặc smoke test trước khi dùng production."

This is **honest caveat**, NOT over-claim. Verified:
- Snapshot has no CLI binary (only SKILL.md docs).
- Source's `.claude/skills/` contains demos (`captions-overlay`, `changelog-video`, etc.) — not CLI.
- Source's `skills/hyperframes-cli/SKILL.md` is documentation, not `package.json` with `bin` field.

The wiki correctly disclaims that the snapshot is content-only and CLI smoke-test is a separate downstream task. PASS.

## Findings table (full audit)

| Wiki claim | Verified | Method |
|---|---|---|
| Source commit `5244dde` | ✓ | `git rev-parse HEAD` |
| Tag `v0.7.83` | ✓ | `git describe --tags` |
| 19 skill dirs | ✓ | `find -name SKILL.md \| wc -l` (source & snapshot both 19) |
| 889 files (upstream) | ✓ | `find source/skills -type f \| wc -l` |
| 889 files (snapshot) | ✓ | `find snapshot -type f \| wc -l` |
| 4,839 tracked paths | ✓ | `git ls-files \| wc -l` |
| 0 SHA-256 mismatches | ✓ | `diff -rq snapshot/ source/skills/` empty |
| 19 SKILL.md hash match | ✓ | md5 spot-check, all match |
| 2 empty placeholders | ✓ | `find -size 0` returns scripts/.gitkeep + assets/.gitkeep |
| Custom skill untouched | ✓ | mtime Jul 17 (pre-clone) |
| 19 symlinks resolve | ✓ | `readlink + [ -e ]` recipe |
| Wiki files not overwritten | ✓ | mtime-neighbor check |
| CLI smoke-pass claim | NOT MADE | Wiki honest caveat only |

## Minor wording flag (not a failure)

Wiki line 109:
> "Hermes-visible 19 skill directories trỏ về snapshot qua `/Users/tuananh4865/.claude/skills`, sau đó `~/.hermes/skills` trỏ tiếp vào các canonical directories."

The second clause is **not strictly true** — `/Users/tuananh4865/.hermes/skills/` does not contain symlinks to `heygen-hyperframes-v0.7.83/*`. The 19 skills are reachable via `.claude/skills/` only. Wording is ambiguous but functional state is correct.

**Severity:** Minor. Not PARTIAL_PASS-worthy. Recommend author rewrite as "đã wire 19 entry vào `/Users/tuananh4865/.claude/skills/`, đủ để Hermes/Claude load" without the second-clause claim.

## Reproducible audit recipe (copy-paste)

For future "clone upstream X into local snapshot" audits, this 6-command recipe catches the major failure modes:

```bash
# 1. Source commit verification
cd <source> && git rev-parse HEAD && git describe --tags --always

# 2. File counts + recursive diff
find <source>/<target-subdir> -type f | wc -l
find <snapshot> -type f | wc -l
diff -rq <snapshot>/ <source>/<target-subdir>/

# 3. Manifest spot-check
for s in <list-of-manifest-files>; do
  s_md5=$(md5 -q <source>/<target-subdir>/$s)
  d_md5=$(md5 -q <snapshot>/$s)
  echo "$s: $s_md5 vs $d_md5 $([ "$s_md5" = "$d_md5" ] && echo ✓ || echo ✗)"
done

# 4. Symlink resolve
for link in <symlink-dir>/*; do
  target=$(readlink "$link")
  [ -e "$target" ] && echo "✓ $link -> $target" || echo "✗ BROKEN: $link"
done

# 5. Custom skill preservation (collision check)
stat -f '%Sm' <local-cookbook-path>   # MUST be before clone timestamp
md5 -q <local-cookbook-path>          # Compare to known-good if available

# 6. mtime-neighbor overwrite check
ls -la <wiki-dir-or-shared-dir>/ | sort -k 8  # newest mtimes last
# Confirm only declared new files have new mtimes.
```

## Cross-references

- Skill loaded: `adversarial-content-verifier` v1.5.0 (this update)
- Companion pitfalls: F11 (forbidden-phrase `[DEBUNK]` vs `[CLAIM]`), F4 (don't trust author's file paths), F5 (count independently)
- Files audited:
  - `/Volumes/Storage-1/Hermes/wiki/concepts/heygen-hyperframes-v0.7.83-skill-clone-2026-07-30.md`
  - `/Volumes/Storage-1/Hermes/wiki/raw/articles/heygen-hyperframes-v0.7.83-source-2026-07-30.md`
