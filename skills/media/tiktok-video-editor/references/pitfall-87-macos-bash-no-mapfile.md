# PITFALL #87 — macOS bash 3.2 has no `mapfile` builtin

**Detected:** 23/07/2026 while building `build_pre_speed.sh` v0.01.1

## Symptom

Writing bash loops to read array from stdin:

```bash
# FAILS on macOS:
mapfile -t arr <<< "$data"
for x in "${arr[@]}"; do ... done
# bash: mapfile: command not found
```

`mapfile` (a.k.a. `readarray`) was introduced in **bash 4.0**. macOS ships
`bash 3.2.57` as `/bin/bash` (default for shell scripts via shebang `#!/bin/bash`).
`brew install bash` gives 5.x but `/bin/bash` is still 3.2.

## Fix

Use `mktemp` + `while read`:

```bash
RANGES_FILE=$(mktemp)
python3 <<PYEOF > "$RANGES_FILE"
import json
...
PYEOF

while IFS=' ' read -r start end; do
    [[ "$start" == TOTAL:* ]] && continue
    [ -z "$start" ] && continue
    # ... process
done < "$RANGES_FILE"

rm -f "$RANGES_FILE"
```

Or use `readarray` check + fallback:

```bash
if declare -f mapfile >/dev/null 2>&1; then
    mapfile -t arr <<< "$data"
else
    # macOS path
    while IFS= read -r line; do arr+=("$line"); done <<< "$data"
fi
```

## Related

- All Hermes skill scripts should assume `bash 3.2` for max portability
- Test scripts with `bash script.sh`, NOT `zsh script.sh`
- If you need bash 4+ features (associative arrays, coproc, `;&`), declare
  `#!/usr/bin/env bash` AND require user install `brew install bash`
