---
confidence: high
last_verified: 2026-04-12
relationships:
  - SCHEMA
  - index
  - log
---

# Start Here — AI Agent Session Startup

> **CRITICAL: Read this file at the START OF EVERY NEW SESSION**
> This file is the definitive instruction for how to work with this wiki.
> If memory conflicts with this file, FOLLOW THIS FILE.

## Who I Am
I am an AI agent working with this wiki. The user is the human I assist.

## My Memory vs This Wiki
- **My memory** (the AI's internal memory): Has a small note to check this wiki
- **This wiki**: The user's actual brain — where all knowledge lives permanently
- This wiki is more durable than my memory. Trust this wiki over my memory.

## Session Startup Sequence

```
1. Read start-here.md  → This file
2. Read SCHEMA.md            → Understand domain, conventions, tag taxonomy
3. Read index.md             → Learn what pages exist
4. Read log.md (last 20)     → See what happened recently
5. Read entities/learned-about-tuananh.md → Anh's preferences, style, rules
6. Scan projects/ directory  → Quick check for active projects (optional)
7. Present project summary   → Let Anh choose which project to work on
8. Load full context ONLY when Anh selects a project
9. Proceed with the user's request
```

---

## TOPIC WORKFLOW (CRITICAL — MANDATORY FOR EXTERNAL SOURCES)

When Anh shares a URL, article, or content to ingest:

### Step 1: Capture Raw Source
- URL → save to `raw/articles/[descriptive-name].md`
- PDF → save to `raw/papers/[descriptive-name].md`
- NEVER save to `raw/transcripts/` — that folder is only for meeting/interview notes

### Step 2: Orient
- Read `SCHEMA.md` — understand conventions
- Search existing pages for mentioned entities/concepts

### Step 3: Create Wiki Pages
- **People/Companies/Products** → `entities/[name].md`
- **Topics/Ideas/Techniques** → `concepts/[topic].md`
- **Comparisons** → `comparisons/[name].md`
- Every page must link to at least 2 other wiki pages

### Step 4: Update Navigation
- Add new pages to `index.md`
- Append to `log.md`

### Step 5: Report
- List all files created/updated

---

## PROJECT WORKFLOW

### Project Structure
Each project lives in `projects/{project-name}/`:
- `hub.md` — Project overview
- `phase-N-name.md` — Phase notes
- `decisions/` — Technical decision logs
- `mistakes/` — Per-project mistakes
- `retrospectives/` — Session reviews

### Session Flow
```
1. Scan projects/ for active projects
2. Show summary (status, phase, blockers, next action)
3. Anh picks project → load hub + current phase
4. Work on tasks
5. End of session → offer retrospective
```

---

## REQUEST-TO-SDD WORKFLOW

**LUAT VANG: KHONG BAO GIO execute khi chua co Anh accept SDD.**

```
Request → Analysis → Deep Research (15-50 sources) → SDD (confidence >= 8.5) → Anh Accept → Execute
                                              ^
                                        Lap lai neu
                                        Anh reject
```

---

## Wiki Self-Maintenance

### Scripts (in `scripts/`)
| Script | Purpose |
|--------|---------|
| `wiki_self_heal.py` | Auto-fix broken links, missing frontmatter |
| `wiki_self_critique.py` | Score page quality |
| `wiki_gap_analyzer.py` | Find missing topics |
| `wiki_lint.py` | Health check all wiki issues |

### Watchdog
- `scripts/watchdog_daemon.py` — File watcher (polls 5s, debounce 10s)

---

## Key Rules

1. **Always update `entities/learned-about-tuananh.md`** when learning new about Anh
2. **Never modify files in `raw/`** — sources are immutable
3. **Always update `index.md`** and `log.md** when creating/modifying pages
4. **Minimum 2 wikilinks** on every wiki page
5. **Commit + push after every task**
6. **Project scan at session start**
7. **Log mistakes without judgment**
8. **Trust wiki over memory**

---

## Wiki Architecture

```
wiki/
├── start-here.md    ← YOU ARE HERE
├── SCHEMA.md              ← Conventions, structure, taxonomy
├── index.md               ← Content catalog
├── log.md                 ← Action log
├── raw/                   ← Immutable sources
│   ├── articles/          ← Web articles, blog posts
│   ├── papers/            ← Academic papers
│   └── transcripts/       ← Meeting/interview notes ONLY
├── entities/              ← People, companies, products
├── concepts/              ← Topics, ideas, techniques
├── comparisons/           ← Side-by-side analyses
└── queries/               ← Filed query results
```

---

*Last updated: 2026-04-12*
