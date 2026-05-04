# Three-Focus Autoresearch Structure

## Approved Focus Areas (2026-05-04)

### Focus 1: Skills Improvement (PRIMARY)
```python
SHS = stale_skills × 10 + missing_examples × 5 + broken_links × 3 + low_confidence × 2
Target: SHS = 0
```
- Improve ~/.hermes/skills/
- Add examples, pitfalls, verification steps
- Fix broken links, update stale info

### Focus 2: AI Agents Research
```python
Agents_Score = frameworks_found × 10 + patterns_found × 5 + techniques_added × 3
Target: 5+ techniques documented
```
- Monitor LangChain, Mastra, Flowise, n8n
- Research MCP, A2A protocols
- Update wiki: ai-agent-trends-*.md

### Focus 3: Hermes Agentic Features (MOST CREATIVE)
```python
Hermes_Score = features_proposed × 10 + features_implemented × 20 + wiki_pages_updated × 2
Target: Hermes_Score >= 50
```
- New capabilities for Hermes
- Self-improvement patterns
- Tool creation
- Memory optimization
- Multi-agent coordination

## Success Criteria (STOP when ANY met)
- SHS = 0
- 5+ AI agent techniques documented
- Hermes_Score >= 50
- 1+ working prototype implemented

## Loop Structure
```
LOOP FOREVER:
1. Read program.md, knowledge.md, DISCARDED.md
2. Pick ONE focus area
3. Research / implement
4. Measure improvement
5. If improved → git commit
6. If no progress → git reset, try different angle
7. Update knowledge.md
8. Every 30 min: progress report to telegram
9. STOP only when success criteria met OR human interrupts
```

## Infinite Repeat
- Cron job: `repeat: 0` (forever)
- Only stops when goal achieved or human interrupts
