---
title: Intelligent Wiki Agent System Architecture
created: 2026-04-16
type: concept
---

# Intelligent Wiki Agent System Architecture

## Overview

A multi-agent system for autonomous wiki maintenance, knowledge synthesis, and continuous learning. The system employs specialized agents that collaborate through a shared message bus and knowledge graph.

---

## 1. Major Components

### 1.1 Orchestrator Agent (Team Lead)

The central coordination hub that manages task decomposition, agent dispatch, and result aggregation.

**Responsibilities:**
- Receives user requests and high-level goals
- Decomposes tasks into atomic subtasks assignable to specialist agents
- Routes tasks to appropriate agents based on their capabilities
- Monitors progress and handles timeout/failure recovery
- Aggregates results from multiple agents into coherent responses

**Interfaces:**
- User input gateway (Slack, CLI, API)
- Agent dispatch table
- Result aggregator

---

### 1.2 Knowledge Graph Store

A graph-based storage layer that maintains entities, relationships, and provenance metadata.

**Responsibilities:**
- Stores wiki content as nodes (entities) and edges (relationships)
- Tracks provenance (source, author, timestamp, confidence)
- Provides query API for semantic search and relationship traversal
- Handles versioning and conflict resolution
- Supports inference queries for knowledge synthesis

**Data Model:**
- Nodes: concepts, documents, agents, sessions
- Edges: `relates_to`, `contradicts`, `supports`, `derives_from`, `part_of`
- Properties: confidence score, source reliability, temporal validity

---

### 1.3 Ingestion Agent (Researcher)

Specialized agent for acquiring, parsing, and integrating external knowledge.

**Responsibilities:**
- Monitors configured sources (RSS, APIs, web scrapers, file watchers)
- Parses diverse formats (Markdown, HTML, PDF, JSON, CSV)
- Extracts entities and relationships using NER and relation extraction
- Deduplicates content against existing knowledge graph
- Flags low-confidence or conflicting information for review

**Output:**
- Structured knowledge entries → Knowledge Graph Store
- Confidence-scored assertions with source attribution

---

### 1.4 Reasoning Agent (Analyst)

Specialized agent for synthesis, inference, and knowledge consolidation.

**Responsibilities:**
- Performs multi-hop reasoning over the knowledge graph
- Identifies gaps, contradictions, and redundancies
- Generates new inferred knowledge from explicit facts
- Answers complex queries requiring multiple sources
- Produces explanations with traced reasoning paths

**Capabilities:**
- Forward/backward chaining
- Analogical reasoning
- Argument mapping and evaluation

---

### 1.5 Editor Agent (Writer)

Specialized agent for content creation, summarization, and maintenance.

**Responsibilities:**
- Generates or updates wiki content from structured knowledge
- Creates summaries optimized for different audiences
- Maintains consistency in style, tone, and formatting
- Flags content needing human review (controversial, low-confidence)
- Archives outdated content

---

## 2. Data Flow

### 2.1 Request Lifecycle

```
User Input
    │
    ▼
┌─────────────────┐
│  Orchestrator   │ ←── Task Queue (persistent)
└────────┬────────┘
         │ dispatch
         ▼
┌─────────────────────────────────────────┐
│           Message Bus (in-memory)        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │Ingestion │ │Reasoning│ │ Editor  │  │
│  │  Agent   │ │  Agent  │ │  Agent  │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│       │            │            │         │
│       └────────────┴────────────┘         │
│                    │                      │
└────────────────────┼──────────────────────┘
                     │ write/read
                     ▼
┌─────────────────────────────────────────┐
│           Knowledge Graph Store          │
│         (SQLite/PostgreSQL + graph)      │
└─────────────────────────────────────────┘
```

### 2.2 Ingestion Flow

1. **Source Poll** → Raw content fetched
2. **Parse** → Format-specific extraction
3. **Extract** → Entity + relation detection
4. **Deduplicate** → Check against existing nodes
5. **Score** → Assign confidence based on source reliability
6. **Write** → Persist to Knowledge Graph
7. **Notify** → Signal Reasoning Agent of new content

### 2.3 Query Flow

1. **Parse** → Decompose query into sub-questions
2. **Route** → Identify relevant agents for each sub-question
3. **Execute** → Agents query Knowledge Graph in parallel
4. **Synthesize** → Reasoning Agent combines results
5. **Generate** → Editor Agent formats response
6. **Return** → Orchestrator returns final answer + provenance

---

## 3. Agent Roles Summary

| Agent | Role Type | Core Responsibility | Key Tools |
|-------|-----------|---------------------|-----------|
| **Orchestrator** | Coordinator | Task routing, workflow management | Task queue, agent registry |
| **Ingestion** | Researcher | Content acquisition, entity extraction | Web scraper, NER, dedup engine |
| **Reasoning** | Analyst | Inference, synthesis, gap analysis | Graph query, inference engine |
| **Editor** | Writer | Content generation, summarization | Template engine, format converter |

---

## 4. Communication Protocol

### Agent Messages

All agents communicate via typed messages on the message bus:

```json
{
  "type": "TASK",
  "from": "orchestrator",
  "to": "reasoning",
  "payload": {
    "task_id": "uuid",
    "intent": "answer_question",
    "query": "What are the dependencies of project X?",
    "context": {}
  },
  "reply_to": "uuid-of-origin-message"
}
```

### Message Types

- `TASK` — Work assignment with payload
- `RESULT` — Task completion with results
- `QUERY` — Synchronous knowledge graph query
- `EVENT` — Asynchronous notifications (new content, conflicts)
- `ERROR` — Task failure with error details

---

## 5. Persistence & State

- **Short-term**: Agent working memory (in-memory, lost on restart)
- **Long-term**: Knowledge Graph (persisted to SQLite/PostgreSQL)
- **Task Queue**: Persistent queue for durability across restarts
- **Checkpoints**: Periodic state snapshots for recovery

---

## 6. Failure Handling

- **Agent crash**: Orchestrator re-dispatches to another capable agent
- **Timeout**: Partial results returned with `incomplete` flag
- **Conflict**: Multiple assertions → flagged for human review
- **Graph corruption**: Periodic integrity checks + backup restore
