# Node CLI Install from GitHub — Detailed Walkthrough

> Session-specific reference. Companion to SKILL.md's Pitfall section.
> Captured from session 2026-06-26 installing `renezander030/capcut-cli` v0.11.3.

## When This Reference Applies

User wants a Node-based CLI tool that:
- Lives on GitHub (not just npm registry)
- Wants source editable / version-controlled locally
- Needs TypeScript build step OR has non-trivial `bin/` wrapper
- Will be invoked from arbitrary directories, not just the repo dir

## End-to-End Recipe (verified)

```bash
# 1. Pre-flight — verify repo is real (see SKILL.md Step 0)
curl -sL "https://api.github.com/repos/<owner>/<repo>" \
  | grep -E '"stargazers_count"|"forks_count"|"pushed_at"|"size"|"language"|"license"'

# 2. Clone to ~/tools/
mkdir -p ~/tools
cd ~/tools
git clone https://github.com/<owner>/<repo>.git
cd <repo>

# 3. Install + Build
npm install          # or yarn / pnpm — read package.json
npm run build        # MOST TypeScript repos need this; check "scripts.build"

# 4. Inspect what got built
ls -la bin/                    # usually a 2-line wrapper script
ls dist/index.* 2>/dev/null    # actual entry — what bin/ imports

# 5. Link to PATH (symlink, NOT npm install -g, to keep source editable)
ln -sf "$(pwd)/bin/<name>" /opt/homebrew/bin/<name>
# Fallback if /opt/homebrew/bin/ doesn't exist:
ln -sf "$(pwd)/bin/<name>" /usr/local/bin/<name>

# 6. Smoke test
which <name>                   # should print the symlink path
<name> --version               # expect semver
<name> --help | head -20       # confirm commands listed
<name> doctor 2>/dev/null      # if it has doctor — check optional deps
```

## Real Trace: capcut-cli v0.11.3 (2026-06-26)

| Step | Observation | Resolution |
|------|-------------|------------|
| `curl api.github.com/repos/renezander030/capcut-cli` | 106 stars, 19 forks, pushed 6 days ago, MIT, JavaScript | Green light |
| `git clone` | Clean clone, 5MB | OK |
| `npm install` | 41 packages, "1 low severity vulnerability" (devDeps only) | OK — read advisory, didn't auto-fix |
| `npm run build` | `tsc && node -e "import('node:fs').then(fs=>fs.copyFileSync('src/enums.json','dist/enums.json'))"` — emits `dist/` + copies enums.json | Built successfully |
| `ls bin/` | Only `capcut` file, 48 bytes, contains `import("../dist/index.js");` | Wrapper script, NOT direct entry |
| `node bin/capcut --version` | **FAIL**: `MODULE_NOT_FOUND /Users/.../bin/capcut.js` | bin/capcut is shell wrapper, not JS — run via `dist/index.js` |
| `node dist/index.js --version` | OK: `0.11.3` | Real entry confirmed |
| `ln -sf bin/capcut /opt/homebrew/bin/capcut` | OK | Linked |
| `capcut --version` from `~/` | OK: `0.11.3` | Symlink works |
| `capcut doctor` | 4/7 ok, 3 warns (whisper, ANTHROPIC_API_KEY, JianYing dir) | Warnings OK — affect optional subcommands only |
| `capcut projects` | Lists 7 of anh's drafts | Real CapCut dir auto-detected |
| `capcut info /abs/path/...` | Reads 30.3s TikTok project successfully | Real data roundtrip |

## Pitfalls Deep-Dive

### Pitfall A: bin/ wrapper ≠ real entry

`bin/capcut` content:
```js
#!/usr/bin/env node
import("../dist/index.js");
```

When you `node bin/capcut` directly, Node treats `capcut` as the module to run (because no `.js` extension + no package.json in bin/), so it tries to resolve `bin/capcut.js` → doesn't exist → `MODULE_NOT_FOUND`.

**Why it works as a symlink:** When you symlink it into `/opt/homebrew/bin/capcut` and run `capcut --version`, Node reads the file, sees the `#!/usr/bin/env node` shebang, and runs IT as a script (which then `import()`s `dist/index.js` correctly).

**The fix for testing:** Always test the **symlink**, not the file directly. Or use `node dist/index.js` directly if you want to bypass.

### Pitfall B: `dist/` doesn't exist until `npm run build`

TypeScript repos compile to `dist/`. If you `npm install` only, `dist/` is empty. Running the binary fails with `MODULE_NOT_FOUND` or `Cannot find module './commands/info.js'`.

**Symptom check:**
```bash
ls dist/ 2>/dev/null && echo "BUILT" || echo "NEED BUILD"
```

**Always build before linking.**

### Pitfall C: doctor warnings are NOT failures

`capcut doctor` returns `{"ok": true}` even with warnings. The `ok` field is about whether the CORE commands work. Warnings block specific subcommands:
- `whisper` missing → blocks `capcut caption`
- `ANTHROPIC_API_KEY` missing → blocks `capcut translate`
- `draft-dir JianYing` missing → blocks `--jianying` flag

Don't try to install optional deps preemptively. Only set up when user actually wants that feature.

### Pitfall D: symlink target must exist at link time

`ln -sf "$(pwd)/bin/capcut" /opt/homebrew/bin/capcut` — the `$(pwd)` resolves to `/Users/tuananh4865/tools/capcut-cli` at that moment. If you run it from a different cwd later, the resolved path is wrong.

**Pattern:** Run the `ln -sf` from INSIDE the repo dir, or use absolute path:
```bash
ln -sf "/Users/tuananh4865/tools/capcut-cli/bin/capcut" /opt/homebrew/bin/capcut
```

### Pitfall E: PATH order matters

If both `/usr/local/bin/capcut` AND `/opt/homebrew/bin/capcut` exist, which wins depends on `echo $PATH` order. On Apple Silicon with Homebrew, `/opt/homebrew/bin` comes first by default. Check with `which -a capcut` to see all candidates.

## Files to Capture to Wiki

After successful install, save a wiki page at:
`/Volumes/Storage-1/Hermes/wiki/entities/<tool-name>.md`

Frontmatter minimum:
```yaml
---
title: <Tool Name>
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: tool
tags: [tool-category, platform]
sources:
  - https://github.com/<owner>/<repo>
  - https://www.npmjs.com/package/<pkg>
confidence: high
relationships:
  - learned-about-tuananh
---
```

Body sections:
1. Tổng quan (1 paragraph)
2. Tại sao cài (anh's reason)
3. Cài đặt trên máy anh (table of steps with status)
4. Doctor/smoke test output (verbatim JSON if possible)
5. Commands quan trọng (table)
6. Workflow E2E typical use case
7. Related (wikilinks)

## Related

- SKILL.md — umbrella workflow
- [[google-antigravity-install]] — different install pattern (DMG), sibling skill
- [[learned-about-tuananh]] — anh's preferences
