---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 deep-research (extracted)
  - 🔗 terminal-startup-flow (extracted)
  - 🔗 sdd-template (extracted)
relationship_count: 3
---

# Request to SDD Workflow

## Luat Vang

**KHONG BAO GIO execute khi chua co Anh accept SDD.**

```
Request -> Analysis -> Deep Research -> SDD (confidence >= 8.5) -> Anh Accept -> DO
                                              ^
                                        Lap lai neu
                                        Anh khong accept
```

---

## Flow Chi Tiet

### Phase 1: Analysis & Topic Extraction

Khi nhan request tu Anh:
1. Hieu muc tieu chinh
2. Xac dinh sub-goals, constraints, success criteria
3. Tao danh sach topics + keywords

### Phase 2: Deep Research (15-50 sources)

Dung `deep-research` skill:
- 5-10 sub-queries
- 15-50 unique sources
- Citations day du

### Phase 3: SDD Generation

SDD phai co:
- Confidence score >= 8.5/10
- Chi tiet, cu the
- Alternatives considered
- Trade-offs analyzed

### Phase 4: Human Approval

Gui SDD cho Anh review:
- Accept -> Execute
- Reject -> Research lai
- Modify -> Dieu chinh + resend

### Phase 5: Execute

Sau khi accept:
- Execute theo SDD
- Commit sau milestone
- KHONG thay doi SDD khi dang run

---

## Confidence Scoring

| Criterion | Weight |
|-----------|--------|
| Research Depth | 30% |
| Solution Clarity | 25% |
| Feasibility | 20% |
| Completeness | 15% |
| Risk Awareness | 10% |

Score = weighted_sum * 2 (0-10 scale)

---

## Quality Gates

| Phase | Gate |
|-------|------|
| Analysis | Topics >= 2 |
| Research | 15-50 sources |
| SDD | Confidence >= 8.5 |
| Approval | Explicit accept |

---

## Khi Nao Chay

**LUON CHAY:**
- Request moi tu Anh
- Hoi "lam X duoc khong?"
- Build something moi

**CO THE SKIP:**
- Anh noi "cu lam di" (pre-approved)
- Task da co SDD accept
- Routine maintenance

---

## Related

- [[deep-research]] - Research methodology
- [[terminal-startup-flow]] - Startup-specific flow
- [[sdd-template]] - SDD template
