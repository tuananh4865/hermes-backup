# Hermes v0.16 "Surface Release" (June 2, 2026)

> Desktop app + 100 PRs + 159 contributors + 176K stars

## Key Features

| Feature | Details |
|---------|---------|
| **Native Desktop App** | First desktop preview — bundles memory, skills, scheduling, browser automation |
| **NVIDIA RTX AI Garage** | New partnership for GPU-accelerated workflows |
| **`/undo` command** | New command for reverting last action |
| **100 PRs merged** | Major release cycle |
| **159 contributors** | Largest contributor count to date |
| **294 commits past previous tag** | Active development velocity |
| **176K+ GitHub stars** | Up from ~157K on May 25 |

## Community

- **@mhdfaran** (Farhan, Hermes founder): "next evolution of Hermes Agent is here" — June 2 teaser
- **@KSimback** (Kevin Simback): Auto-PR from release notes workflow working in production
- **@prthamesh** (pratos_): X Premium + Grok integration with Hermes now working

## Upgrade

```bash
pip3 install 'hermes-agent>=0.16' -q
pip3 show hermes-agent | grep Version
```

## Security Notes

- **CVE-2026-10548** (June 2): Credential Pool Exposure — affects ≤ v2026.4.23
- **CVE-2026-7396** (May 23): File gateway vulnerability — affects v0.8.x only
- Both patched in v0.16 ✅

## Source

- https://hermes-ai.net/changelog
- GitHub release (confirm exact tag name via `git tag | sort -V | tail -5`)
