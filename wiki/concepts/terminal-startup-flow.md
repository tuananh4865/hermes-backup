---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 terminal-build-startup (extracted)
  - 🔗 deep-research (extracted)
  - 🔗 autonomous-wiki-agent (extracted)
  - 🔗 agentic-workflows-agentic-graphs (extracted)
relationship_count: 4
---

# Terminal Startup Flow

> Flow để đi từ ý tưởng đến MVP có người dùng trong 1 ngày.
> Kết hợp: Terminal + Coding Agents + Deep Research + SDD-first

---

## Core Philosophy

```
Research First, Build Second
30% research time → 80% result quality
```

**Luật vàng:**
1. **Deep Research** trước khi code (15-30 phút)
2. **SDD** viết trước khi build
3. **Launch sớm** > launch hoàn hảo
4. **Terminal-only** để tránh context switching

---

## Complete Flow

```
IDEA → RESEARCH → SDD → BUILD → DEPLOY → ITERATE
         ↑                    ↓
         └────────────────────┘
              (feedback loop)
```

---

## Phase 1: Deep Research (15-30 phút)

**Mục tiêu:** Hiểu thị trường, đối thủ, khoảng trống

### 1.1 Market Analysis (5 phút)
Dùng `deep-research` skill để phân tích:
- Đối thủ đang làm gì?
- Mô hình kinh doanh của họ?
- Điểm yếu của họ?
- Khoảng trống chưa ai lấp?

**Output:** Bản phân tích đủ chi tiết để ra quyết định

### 1.2 Competitive Analysis (5 phút)
```
Sub-queries:
- [domain] competitors landscape 2025
- [domain] pricing models
- [domain] weaknesses complaints
- [domain] underserved use cases
```

### 1.3 Opportunity Identification (5 phút)
- USP rõ ràng?
- Khoảng trống nào chưa ai làm?
- Mình có lợi thế gì?

**Output:** One-pager xác định WHAT to build

---

## Phase 2: SDD - System Design Document (15-30 phút)

**Đây là bước QUAN TRỌNG NHẤT**

> "Có SDD rõ ràng thì agent build nhanh và đúng. Không có thì nó build lung tung."

### 2.1 Architecture Design
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────┐
│   Gateway   │
└──────┬──────┘
       │
┌──────▼──────┐
│  Backend    │ ← Bun/Next.js
└──────┬──────┘
       │
┌──────▼──────┐
│  Database   │ ← SQLite → PostgreSQL
└─────────────┘
```

### 2.2 API Endpoints Design
```
POST /api/v1/analyze
GET  /api/v1/status
POST /api/v1/deploy
```

### 2.3 Tech Stack Decision
```
Backend:    Bun / Next.js / FastAPI
Frontend:  Next.js / React
Database:  SQLite (start) → Supabase (scale)
Auth:      JWT / Clerk
Deploy:    Railway + Vercel
```

### 2.4 Fallback Strategy
```
Layer 1: Primary provider
Layer 2: Fallback provider A
Layer 3: Fallback provider B
Layer 4: Graceful degradation
```

**Output:** SDD hoàn chỉnh (Markdown file)

---

## Phase 3: Build (2-4 giờ)

**Nguyên tắc:** Đưa SDD cho agent, để nó đọc hiểu và build

### 3.1 Backend (1-2 giờ)
```bash
# Tạo project structure
mkdir project && cd project

# Initialize
bun init
```

### 3.2 Frontend (1-2 giờ)
```bash
npx create-next-app@latest frontend
```

### 3.3 Integration Tests
```bash
bun test
```

---

## Phase 4: Deploy (30 phút)

```bash
# Railway
railway init
railway up

# Vercel  
vercel --prod
```

**Output:** Live production URL

---

## Phase 5: Iterate (liên tục)

### 5.1 Monitor
```bash
# Check errors
railway logs --tail

# Check metrics
curl analytics API
```

### 5.2 Fix Fast
> "48 commits trong ngày hôm đó"

- Error rate ngày đầu = 49% → OK, launch anyway
- Error rate ngày 3 = 0%

### 5.3 User Feedback
```bash
# Email outreach từ Terminal
# Không cần mở Gmail
```

---

## Research → Build → Deploy Timeline

```
12:00  - Ý tưởng
12:15  - Research starts
12:30  - SDD starts  
13:00  - SDD done
13:15  - Build starts
17:00  - Build done
17:30  - Deploy
19:00  - LIVE with users
```

---

## Quality Gates

| Phase | Gate | Pass Criteria |
|-------|------|---------------|
| Research | 15-50 sources | Đủ để hiểu thị trường |
| SDD | Review checklist | Architecture + API + DB done |
| Build | CI passes | Unit tests green |
| Deploy | Health check | `/health` returns 200 |

---

## Terminal Tools Checklist

```bash
# Core
hermes          # Main agent
claude-code     # Coding agent  
codex           # Alternative coding agent

# Deployment  
railway         # Backend deploy
vercel          # Frontend deploy

# Utilities
gh              # GitHub CLI
mcporter        # MCP tools
agent-reach     # Web scraping
```

---

## Key Insight: AI = Builder, Human = Decision Maker

| Human làm | AI làm |
|-----------|--------|
| Chọn thị trường | Research theo chỉ đạo |
| Xác định USP | Build theo SDD |
| Quyết định pivot | Deploy, fix bugs |
| Chọn feature nào bỏ | |
| Khi nào launch | |

---

## Related

- [[terminal-build-startup]] — Nguồn gốc bài viết
- [[deep-research]] — Research methodology (15-50 sources)
- [[autonomous-wiki-agent]] — Agent execution framework
- [[agentic-workflows-agentic-graphs]] — Node-based workflow patterns
