---
name: skill-from-experience
description: Create skills autonomously from repeated task patterns - extracts reusable workflows from experience
version: 1.0.0
category: lifecycle
platforms: [macos, linux]
created: 2026-04-14
tags: [skill-creation, autonomous-learning, pattern-extraction, self-improvement]
requires_toolsets: [terminal]
---

# Skill From Experience

**Every repeated task is an opportunity to create reusable knowledge.**

This skill extracts patterns from repeated work and creates new skills automatically.

---

## When to Trigger

Create a skill when you notice:

1. **Repetition** — Same 5+ step workflow done 3+ times
2. **Error recovery** — Recovery pattern that worked
3. **User correction** — User showed the correct approach
4. **Non-obvious success** — Unusual path that worked well
5. **Multi-tool pattern** — Same tool sequence used repeatedly

---

## The Skill Creation Workflow

### Step 1: Identify the Pattern

```
Questions:
- Has this exact task been done before?
- Is this a 5+ step process?
- Will this be useful in 6 months?

If YES to the above → Create a skill.
```

### Step 2: Extract the Steps

```
1. What was the trigger for this task?
2. What were the exact steps taken?
3. What decisions were made along the way?
4. What was the verification?
5. What mistakes were made and corrected?
```

### Step 3: Create the Skill File

```bash
mkdir -p ~/.hermes/skills/{category}/{skill-name}/
```

```markdown
---
name: {skill-name}
description: {Brief description - one line}
version: 1.0.0
category: {category}
platforms: [macos, linux]
created: {YYYY-MM-DD}
tags: [{tag1}, {tag2}]
---

# {Skill Name}

## Purpose
{What this skill does}

## When to Use
{Trigger conditions}

## Steps
1. {Step 1}
2. {Step 2}
3. {Step 3}

## Example
```
{Example usage}
```

## Notes
{Lessons learned}
```

### Step 4: Update the Index

```markdown
|  | {Description} | {YYYY-MM-DD} |
```

---

## Example: Creating a Skill

```
Situation: "I've set up 3 Python projects the same way this week"

PATTERN IDENTIFIED:
1. Create project directory
2. Set up venv
3. Install requirements.txt
4. Create basic structure (src/, tests/)
5. Initialize git
6. Create README.md

SKILL CREATED: setup-python-project
```

```markdown
---
name: setup-python-project
description: Standard Python project setup workflow
version: 1.0.0
category: devops
created: 2026-04-14
tags: [python, project-setup, venv]
---

# Setup Python Project

## When to Use
Starting a new Python project from scratch.

## Steps
1. Create project directory
2. python3 -m venv venv
3. source venv/bin/activate
4. Create requirements.txt (minimal)
5. mkdir -p src/ tests/
6. git init
7. Create README.md

## Example
```bash
mkdir myproject && cd myproject
python3 -m venv venv && source venv/bin/activate
pip install pytest
```
```

---

## Triggers in Detail

### Trigger 1: Repetition (3+ times)

```
Signs:
- "I've done this before"
- "This is the third time this week"
- Same 5+ steps repeated

Action:
- Create skill immediately
- Don't wait for 4th time
```

### Trigger 2: Error Recovery

```
Signs:
- Made a mistake
- Found a way to fix it
- Recovery was non-obvious

Action:
- Document the recovery pattern
- Future agents will make same mistake
- Prevent re-learning
```

### Trigger 3: User Correction

```
Signs:
- User says "No, it should be done this way"
- User provides correct approach
- Corrected a misunderstanding

Action:
- Document the correct approach
- Note what was wrong
- This becomes training data
```

### Trigger 4: Non-Obvious Success

```
Signs:
- Unusual approach worked
- "I didn't expect this to work"
- Clever workaround found

Action:
- Document why it worked
- Note the insight
- Make it reproducible
```

---

## Skill Quality Checklist

- [ ] Name is clear and searchable
- [ ] Description is one line
- [ ] When-to-use is specific
- [ ] Steps are numbered and complete
- [ ] Example is included
- [ ] No unnecessary complexity

---

## Curation Rule

```
NOT: Save everything
BUT: Save what will be useful in 6 months

Questions to ask:
1. Will this pattern repeat?
2. Is this non-obvious?
3. Would a new agent struggle without this?
4. Is this already documented elsewhere?

If YES to 2+: Create skill
If NO: Don't save
```

---

## Integration

- Use [[memory-manage]] — Manages the memory tier
- Use [[skill-self-improve]] — For improving the skill later
- Use [[periodic-nudge]] — Triggers skill creation

---

## Related

- [[skill-self-improve]] — Improve skills over time
- [[periodic-nudge]] — Periodic reflection triggers
- [[memory-manage]] — Memory tier management
