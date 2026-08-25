# Tuấn Anh Workflow Mandate — Reference (2026-06-18)

> Session transcript + gap analysis that drove the SKILL.md updates.
> Future agents: this is the WHY behind the mandatory-checklist rule.

## Original mandate (verbatim, translated)

> "Imagine you're working on a big project lasting many days or months.
> How would you set up the workflow system so things don't get messy?
> Know exactly which item is worked on where, when, by whom, for which
> project, which phase, who's doing, who's fixing. Which items depend on
> which other items?
>
> I need you to design a workflow to manage details for each project like that.
> Every new project must strictly follow this workflow.
> Every small action any agent takes must be logged per task so it's easy
> for the manager and orchestrator to manage."

Then a follow-up turn added:

> "I want you to set it up so for every current and future project, you must
> create a specific detailed plan with a checklist. Each big and small item
> needs a plan and checklist to work and mark which task is done vs not yet.
> Research what concept I'm asking for exactly and apply it so you log, plan,
> and check list for ALL projects big or small I let you join! This is to
> ensure every action you take is recorded for backlog when I need it or
> when other agents need it!"

## What Tuấn Anh is describing (researched concept)

Combination of:
- **Work Breakdown Structure (WBS)** — hierarchical decomposition of project into phases → tasks → sub-tasks → actions
- **Kanban backlog tracking** — every item has status (TODO/DOING/DONE), assignee, dependencies
- **GTD (Getting Things Done)** — David Allen's "capture everything out of your head into a trusted system" principle

This is **exactly what Hermes Kanban provides** out of the box — but the user is saying we (the orchestrator) are NOT using it as the systematic backbone for every project. We had built a parallel system at `/Volumes/Storage-1/Hermes/wiki/projects/{id}/` with task files + action logs, which is good for documentation but doesn't give him:
- Live board view (Kanban dashboard at http://127.0.0.1:9119)
- Atomic claim/complete lifecycle
- Persistent SQLite audit trail of every transition
- Standard dashboard for "what's in flight right now"

## Gap discovered in session 2026-06-18

| Layer | Status before | Status after |
|-------|---------------|--------------|
| Kanban skill loaded | ✅ | ✅ |
| Kanban DB healthy | ❌ corrupted since 28/05 | ✅ `hermes kanban init` re-created |
| Default board exists | ✅ with 8 done + 1 blocked | ✅ |
| Task body uses checklist | ❌ prose-only | ✅ template enforced |
| SOUL.md wired to Kanban | ❌ | ⏳ (next step) |
| Content Creator board | ❌ | ⏳ (next step) |

## Recommended rollout for next session

1. Create dedicated Kanban board for Content Creator project: `hermes kanban boards` → new board
2. Migrate existing T-01.1, T-01.2, T-01.3 into Kanban tasks (with checklist bodies)
3. Inject "use Kanban for every task" rule into `~/.hermes/SOUL.md`
4. Verify dashboard at `http://127.0.0.1:9119` works
5. Backfill Content Creator backlog with remaining T-01.4 → T-01.6 tasks

## Key Tuấn Anh preferences captured

From `~/.hermes/memories/MEMORY.md` (consolidated 2026-06-17):
- **work-style**: RESEARCH before doing, VERIFY/QA/TEST before declaring done (evidence-based, not assumption)
- **decision-style**: lead with trigger conditions + when NOT to fire
- **system-architecture**: Fable-5 = foundation (always on), Loop Engine = weapon (for dev work)
- **communication**: Vietnamese casual ("anh" + "em"), concise, no fluff
- **prohibited behaviors**: don't ask "X hay Y", don't request confirmation mid-task, don't list options without committing

## Why this lives in SKILL.md, not just memory

Memory captures "Tuấn Anh is a content creator, prefers concise responses, current project is Content Creator." That tells future agents WHO the user is.

This SKILL.md captures "when working with Tuấn Anh, every Kanban task body must have this specific checklist structure because he explicitly required it on 2026-06-18." That tells future agents HOW to handle his Kanban tasks correctly the first time, without him having to repeat the mandate.

If we only saved this to memory, the next session might load `kanban-orchestrator` skill (which previously said "use delegate_task for small one-shots") and skip Kanban entirely. Now the skill itself says "override that rule when working with Tuấn Anh."

## Related artifacts created in session 2026-06-18

- `templates/task-checklist.md` (sibling file) — the structured body format
- `~/.hermes/SOUL.md` (turn earlier in session) — added "PROJECT WORKFLOW SYSTEM" section
- `~/.hermes/profiles/_shared/sub-agent-workflow.md` — sub-agent reference
- `~/.hermes/profiles/_shared/fable5-patterns.md` — Fable-5 foundation patterns
- `~/.hermes/profiles/_shared/project-loop-engine.md` — Loop Engine v2.3
- `wiki/projects/content-creator/dashboard.md` — first project dashboard
- `wiki/projects/content-creator/dependency-graph.md` — first dependency map

## Conversation timestamp

2026-06-18, ~08:30 ICT, Telegram session with Tuấn Anh (tuananh4865).
Original message thread: [Vietnamese, transcribed above].