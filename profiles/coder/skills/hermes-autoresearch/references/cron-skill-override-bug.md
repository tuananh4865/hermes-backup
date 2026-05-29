# Cron Skill Override Bug — 2026-05-08

## Incident

User requested a new cron job: "Daily Session Review at 0AM" — read session logs, extract learnings, update wiki.

**What went wrong:**
- Created cron with `--skills ["hermes-autoresearch"]` and `--prompt "session review..."`
- Cron ran and output was autoresearch skill content, NOT the session review prompt
- Root cause: Attaching a skill to a cron OVERRIDEs the prompt with the skill's full content

## Files Modified

- `~/.hermes/cron/output/5aea298eb0a8/2026-05-08_08-49-50.md` — first (wrong) run, 45KB autoresearch content
- `~/.hermes/cron/output/5aea298eb0a8/2026-05-08_08-58-24.md` — second (correct) run after skill removed

## Lesson

When creating a cron with a specific task (NOT an autoresearch loop), use:
```
--skills []  --prompt "..."
```

Only attach `hermes-autoresearch` skill when the cron IS an autoresearch task (2AM main loop, 7AM X research).

## Verification After Cron Create

```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list | grep {new_job_id}
# Skills column must be [] for custom-task crons
```
