---
name: graph-query
description: Query and traverse the knowledge graph - find relationships, entities, and connections
version: 1.0.0
category: lifecycle
platforms: [macos, linux]
created: 2026-04-14
tags: [knowledge-graph, query, traversal, relationships]
requires_toolsets: [terminal]
---

# Graph Query

**Query the knowledge graph to find connections and relationships.**

This skill enables structured queries against the knowledge graph.

---

## When to Query

Use graph queries when:

1. **Research** — Finding related concepts
2. **Verification** — Checking if entity exists
3. **Relationship discovery** — Finding connections
4. **Contradiction check** — Finding conflicting claims
5. **Impact analysis** — What depends on X?

---

## Query Types

### Type 1: Find Entity

```
Question: "Does entity X exist?"
Query: Get entity by type and name
```

```bash
python3 ~/.hermes/projects/hermes-dojo/scripts/knowledge_graph.py \
  --db-path ~/.hermes/knowledge_graph.db \
  --query "Entity Name"
```

### Type 2: Find Relationships

```
Question: "What is X related to?"
Query: Find all related entities
```

```bash
python3 ~/.hermes/projects/hermes-dojo/scripts/knowledge_graph.py \
  --db-path ~/.hermes/knowledge_graph.db \
  --query "Entity Name"
```

### Type 3: Find by Relationship Type

```
Question: "What does X use?"
Query: Filter by relationship type
```

```bash
# Get specific relationship type
# (modify script or use direct SQL)
```

### Type 4: Find by Entity Type

```
Question: "Show me all Projects"
Query: List all entities of a type
```

```bash
python3 ~/.hermes/projects/hermes-dojo/scripts/knowledge_graph.py \
  --db-path ~/.hermes/knowledge_graph.db \
  --list-type Project
```

---

## Common Queries

### "What projects exist?"

```bash
python3 knowledge_graph.py --db-path ~/.hermes/knowledge_graph.db \
  --stats
```

### "Who owns Project X?"

```sql
SELECT p.name, p.role 
FROM entities e
JOIN relationships r ON e.name = r.from_entity
JOIN entities p ON r.to_entity = p.name
WHERE r.relationship_type = 'owns'
AND e.name = 'Project X'
```

### "What does Person X work on?"

```sql
SELECT DISTINCT e.name, e.entity_type
FROM entities e
JOIN relationships r ON e.name = r.to_entity
WHERE r.from_entity = 'Person X'
```

### "What uses Library X?"

```sql
SELECT e.name, e.entity_type
FROM entities e
JOIN relationships r ON e.name = r.from_entity
WHERE r.to_entity = 'Library X'
AND r.relationship_type = 'uses'
```

---

## Traversal Patterns

### Pattern 1: Two-Hop

```
Question: "What does Person X's projects use?"
1. Find Person X's projects
2. For each project, find what it uses
```

### Pattern 2: Impact Analysis

```
Question: "What breaks if Library X is removed?"
1. Find all entities that use Library X
2. Those entities are at risk
```

### Pattern 3: Chain Discovery

```
Question: "How is Concept X related to Project Y?"
1. Find direct connections
2. Find indirect paths
3. Build relationship chain
```

---

## Graph Statistics

```bash
# Get overall stats
python3 knowledge_graph.py --stats

# Output:
# Entities: N
# Relationships: N
# By type:
#   Person: N
#   Project: N
#   Concept: N
```

---

## The Query Workflow

### Step 1: Formulate Question

```
What do you want to know?
Be specific: entity name, relationship type, direction
```

### Step 2: Choose Query Type

```
- Simple lookup → Find entity
- Related entities → Find relationships
- Filtered → Find by type or relationship
- Aggregated → Get stats
```

### Step 3: Execute Query

```bash
python3 knowledge_graph.py --query "entity_name"
```

### Step 4: Interpret Results

```
Review results:
- Are results relevant?
- Are there gaps?
- Need to refine query?
```

---

## Example Session

```
Question: "What skills does Hermes Dojo have?"

1. Query: Find Hermes Dojo entity
   Result: Found [Project] Hermes Dojo

2. Query: Find relationships
   Result: owns → Tuấn Anh
          uses → Knowledge Graph
          uses → Python

3. Query: What skills owned by Hermes Dojo?
   (Not direct - need to traverse)

4. Conclusion:
   - Skills stored in skills/ directory
   - Linked in skills/INDEX.md
   - Graph tracks projects and concepts
```

---

## Integration

- Use [[entity-extraction]] — Populate the graph
- Use [[knowledge_graph.py]] — The underlying tool
- Use [[research-command]] — Query during research
- Use [[contradiction-resolution]] — Find conflicts

---

## Related

- [[entity-extraction]] — Populate graph
- [[knowledge_graph.py]] — Query tool
- [[contradiction-resolution]] — Find conflicts
