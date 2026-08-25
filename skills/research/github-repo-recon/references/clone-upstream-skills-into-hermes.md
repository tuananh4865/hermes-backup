# Clone Upstream Skills Into Hermes — Reference

Skill ngắn này là chi tiết hóa Phase 6 của `github-repo-recon`. Mỗi khi anh yêu cầu "phân tích + clone skill trong repo X về" thì dùng workflow này. Phase 1-5 vẫn giữ nguyên trong SKILL.md gốc.

## Pattern đã verified (2026-07-30, heygen-com/hyperframes v0.7.83)

- Source clone vào `/Volumes/Storage-1/Hermes/research/<repo>/` (read-only reference, dùng `git clone --depth 1`).
- Snapshot immutable tại `/Volumes/Storage-1/Hermes/skills/<repo>-<version>/` (vd: `heygen-hyperframes-v0.7.83`).
- Backup bản cũ vào `/Volumes/Storage-1/Hermes/archive/<repo>-pre-<version>-<STAMP>/`.
- Wire Hermes qua symlink chain: `~/.claude/skills/<entry>` → `/Volumes/Storage-1/Hermes/skills/<repo>-<version>/<entry>`, sau đó `~/.hermes/skills/<entry>` → `~/.claude/skills/<entry>` (nếu `~/.hermes/skills/` chưa có entry đó).
- User-owned cookbook `~/.hermes/skills/creative/<entry>/SKILL.md` KHÔNG bị đụng vì nằm category-prefixed, khác path với upstream short names.

## Commands cookbook

### 1. Clone + size audit

```bash
git clone --depth 1 https://github.com/<owner>/<repo>.git /Volumes/Storage-1/Hermes/research/<repo>
git -C /Volumes/Storage-1/Hermes/research/<repo> log -1 --format='%H %s'
git -C /Volumes/Storage-1/Hermes/research/<repo> ls-tree -r --name-only HEAD | wc -l
```

Ghi nhận commit SHA + tag + tổng tracked paths vào raw source capture page trên wiki.

### 2. Snapshot to immutable path

```bash
SRC=/Volumes/Storage-1/Hermes/research/<repo>/skills
DEST=/Volumes/Storage-1/Hermes/skills/<repo>-<version>
mkdir -p "$DEST"
for d in "$SRC"/*; do [ -d "$d" ] || continue; cp -a "$d" "$DEST/$(basename "$d")"; done
```

### 3. Hash-perfect verification

```bash
python3 - <<PY
import hashlib
from pathlib import Path
src=Path('$SRC'); dst=Path('$DEST')
mism=[r.name for r in src.rglob('*') if r.is_file()
      and not (dst/r.relative_to(src)).exists()
      or hashlib.sha256(r.read_bytes()).digest()
         !=hashlib.sha256((dst/r.relative_to(src)).read_bytes()).digest()]
print('MISMATCH',len(mism),mism[:5])
PY
```

Expect `MISMATCH 0`. Sai = investigate file đó trước khi tiếp.

### 4. SKILL.md frontmatter + name uniqueness

```bash
python3 - <<PY
import yaml,re
from pathlib import Path
names=[]
for p in sorted(Path('$DEST').glob('*/SKILL.md')):
    t=p.read_text(); assert t.startswith('---')
    end=t.find('\n---',3); fm=yaml.safe_load(t[3:end])
    assert fm.get('name') and fm.get('description'), p
    names.append(fm['name'])
assert len(names)==len(set(names)), names
PY
```

Expect unique names, all 19 cho HyperFrames.

### 5. Backup + symlink chain

```bash
BACKUP=/Volumes/Storage-1/Hermes/archive/<repo>-pre-<version>-$(date +%Y%m%d-%H%M%S)
mkdir -p "$BACKUP"
CLAUDE=$HOME/.claude/skills
HERMES=$HOME/.hermes/skills
for n in <list upstream skill names>; do
  p=$CLAUDE/$n
  if [ -e "$p" ] || [ -L "$p" ]; then mv "$p" "$BACKUP/$n"; fi
  ln -s "$DEST/$n" "$CLAUDE/$n"
  [ -L "$HERMES/$n" ] || ln -s "$CLAUDE/$n" "$HERMES/$n"
done
```

### 6. Loader visibility check

```bash
hermes skills list 2>&1 | grep -E '<entry>'
ls -la "$HERMES/<entry>" "$CLAUDE/<entry>"
```

Expect mỗi entry = enabled + symlink chain resolves tới snapshot.

### 7. CLI smoke test (chỉ khi repo có CLI package)

```bash
TMP=/Volumes/Storage-1/Hermes/outputs/scratch/<repo>-smoke-$(date +%Y%m%d)
mkdir -p "$TMP"
npx --yes <package>@<version> init "$TMP/project" --non-interactive --example blank --resolution portrait
(cd "$TMP/project" && npx --yes <package>@<version> lint --json)
(cd "$TMP/project" && npx --yes <package>@<version> check --json --no-contrast)
```

Expect exit 0 cho cả 3. Fail → flag ngay với stderr, KHÔNG pretend pass.

### 8. File-edit log

```bash
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py append "$DEST/<file>" --reason "Clone upstream <repo> v<version>" --action create
```

Mirror path = `Hermes/skills/<repo>-<version>/<file>`. Append mỗi file trong snapshot + backup.

### 9. Wiki pages

- Raw source: `wiki/raw/articles/<repo>-v<version>-source-<YYYY-MM-DD>.md` với frontmatter `type: query`, sources = repo + commit + tag.
- Vietnamese analysis: `wiki/concepts/<repo>-v<version>-skill-clone-<YYYY-MM-DD>.md` với frontmatter `type: concept`, sources = raw + repo URL, relationships = [[remotion]] hoặc tương tự.
- `wiki/index.md` thêm entry dưới "Products & Tools".
- `wiki/log.md` append entry `## [YYYY-MM-DD] research | <repo> v<version>`.
- `wiki/entities/learned-about-tuananh.md` thêm tag relationships.

### 10. Adversarial verifier (nếu skill lớn > 5 tool calls + nhiều file)

Delegate subagent đọc lại tất cả artifact, chạy lại SHA-256, symlink resolve, custom cookbook preservation, CLI smoke. PASS 3-layer mới ship.

## Failure modes đã catch

- `~/.hermes/skills/<short-name>/` bị đè bởi upstream cùng tên → user cookbook mất. Fix = clone vào path có version + symlink entry lên `~/.claude/skills/` thay vì ghi thẳng vào `~/.hermes/skills/`.
- SHA-256 mismatch sau install = snapshot chưa hoàn tất `cp -a`. Re-clone entry đó, log lại.
- `npx <cli> --version` fail = environment thiếu dependency. Log evidence, flag; đừng giả vờ pass.
- Custom cookbook bị symlink đè nếu vô tình `ln -s "$DEST/<short>" "$HERMES/<short>"`. Mitigation = chỉ symlink entry nào có trong `$DEST`, không touch category-prefixed (`creative/`, `media/`, `software/`, ...).

## Handoff checklist

- [ ] Source commit + tag + path captured in wiki raw page
- [ ] Snapshot hash-match source (0 mismatch)
- [ ] Backup archived với timestamp + diff hint
- [ ] Symlink chain resolves từ `~/.hermes/skills/` đến snapshot
- [ ] Custom cookbook preserved (SHA256 + mtime unchanged)
- [ ] CLI smoke test passed (init/lint/check exit 0) hoặc fail được flag
- [ ] File-edit log appended cho mọi file mới
- [ ] Wiki index/log/entities cập nhật
- [ ] Adversarial verifier PASS 3-layer (nếu task lớn)
