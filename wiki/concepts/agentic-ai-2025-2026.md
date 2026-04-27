---
title: Agentic AI Agent — Báo Cáo Nghiên Cứu 2025-2026
created: 2026-04-27
updated: 2026-04-27
type: concept
tags: [ai-agent, agentic-ai, research]
confidence: high
relationships: [ai-agent-trends-2026-04-13, ai-agent-infrastructure-2026, code-agents-claw, rag, mastra, flowise]
---

# Agentic AI Agent — Báo Cáo Nghiên Cứu 2025-2026

> **Nguồn tổng hợp:** CogitX (2026-04), Tao An Medium (2026-01), Sparrow AI Blog (2025-12), Classic Informatics (2025-09), GeeksforGeeks (2026-04), IBM Think (2025), Akka (2025-08), AaiNova (2026-03), Bain & Company (2025-09)

---

## 1. Định Nghĩa

### Agentic AI là gì?

Agentic AI (AI Có Tác Tính) là lớp hệ thống AI tự chủ — không chỉ phản hồi prompt mà **tự định nghĩa mục tiêu, tự phân rã thành hành động, tự thực hiện, và tự thích ứng** cho đến khi hoàn thành nhiệm vụ mà không cần con người duyệt ở từng bước.

Khác với AI truyền thống "lắng nghe rồi trả lời", Agentic AI hoạt động trong một vòng lặp liên tục: **Perceive → Reason → Plan → Act → Observe → Adapt**.

### Định nghĩa theo các nguồn

| Nguồn | Định nghĩa |
|-------|-----------|
| CogitX 2026 | "Autonomous systems that perceive, reason, and take real-world actions to achieve goals without human approval at every step" |
| IBM 2025 | "Agents differ from traditional AI assistants that need a prompt each time — user gives high-level task, agent handles the rest" |
| Classic Informatics 2025 | "Agentic AI systems are capable of goal-directed behavior, breaking objectives into actionable steps without being told how" |
| GeeksforGeeks 2026 | "Agentic AI adapts and learns to manage complex, dynamic goals vs traditional AI handles routine tasks" |

### Phân biệt các cấp độ "tính tự chủ"

```
Reactive AI      → Prompt → Output (chatbot đơn giản)
Generative AI    → Prompt → Generation (GPT, Claude)
AI Agent         → Goal → Multi-step execution (web search, code run)
Agentic AI       → Complex Goal → Autonomous decomposition → Self-correcting loop → Outcome
```

---

## 2. Thành Phần Cốt Lõi (Core Components)

### 2.1 Perception (Tri Giác)

Agent nhận dữ liệu từ môi trường — có thể là text, hình ảnh, API response, file, database result, sensor data.

Đây không chỉ là "nhận input" đơn giản. Perception bao gồm:
- **Context gathering** — thu thập toàn bộ ngữ cảnh xung quanh mục tiêu
- **Environment state reading** — đọc trạng thái hiện tại của hệ thống/workspace
- **Memory retrieval** — gọi lại thông tin từ memory store

### 2.2 Reasoning (Lập Luận)

LLM đóng vai trò "brain" — suy luận, phân tích, đánh giá các lựa chọn. Điều này dựa trên:
- Chain-of-thought prompting
- ReAct (Reason + Act) pattern
- Constitutional AI / RLHF alignment

### 2.3 Planning (Lập Kế Hoạch)

Agent phân rã mục tiêu lớn thành các sub-tasks. Các pattern phổ biến:

| Pattern | Mô tả |
|---------|-------|
| **ReAct** |交替执行 Reasoning và Action — nghĩ trước, làm sau |
| **Plan-and-Execute** | Lập kế hoạch toàn bộ trước, rồi thực thi từng bước |
| **Executive Supervisor** | Một agent trung tâm điều phối nhiều worker agents |
| **Hierarchical** | Multi-level planning — strategic → operational → executable |

### 2.4 Memory (Bộ Nhớ)

Memory là thành phần then chốt để agent hoạt động qua thời gian dài:

- **Short-term / Working Memory** — context window của LLM, lưu trạng thái hiện tại của task
- **Long-term / Persistent Memory** — vector database, kiến thức tích lũy qua sessions
- **Semantic Memory** — tri thức có cấu trúc (facts, rules, knowledge graphs)
- **Episodic Memory** — lịch sử hành động đã thực hiện (audit trail, replay)

> **Lưu ý từ Bain 2025:** "Audit logs and traceable memory lineage are now core features — memory vừa là secret sauce vừa là threat surface."

### 2.5 Tool Use (Sử Dụng Công Cụ)

Agent tương tác với thế giới thực qua tools:

| Loại tool | Ví dụ |
|-----------|-------|
| **Web** | Search, scraping, API calls |
| **Code Execution** | Python, JavaScript runtime, shell |
| **File System** | Read/write files, document processing |
| **Database** | SQL queries, vector search |
| **External APIs** | Slack, email, CRM, ERP integrations |
| **Computer Use** | Browser automation, GUI control |

**MCP (Model Context Protocol)** — protocol chuẩn hóa cách agent kết nối tools và data, loại bỏ custom integration work (2025-2026 trend chính).

### 2.6 Action (Hành Động)

Thực thi thực tế — gọi API, viết code, điều hướng web, gửi message. Action có thể:
- Gọi 1 tool duy nhất
- Gọi song song nhiều tools
- Gửi task cho sub-agent

### 2.7 Self-Correction / Reflection (Tự Sửa Lỗi)

Agent đánh giá kết quả hành động, nhận diện lỗi, và tự điều chỉnh plan:
- Error detection và retry logic
- Feedback loops từ environment
- Meta-cognition — "agent thinking about its own thinking"

---

## 3. Kiến Trúc

### 3.1 Single Agent Architecture

```
┌─────────────────────────────────────────┐
│              User / Environment          │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│              PERCEPTION                   │
│   (context + memory retrieval + input)  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│              REASONING                    │
│        (LLM Brain + CoT + ReAct)        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│              PLANNING                     │
│  (task decomposition + tool selection)  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│               ACTION                     │
│    (tool calls, code exec, API calls)    │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────▼─────────┐
         │  OBSERVE / FEEDBACK │
         └─────────┬─────────┘
                   │  ←── Self-correction loop
```

### 3.2 Multi-Agent Architecture (2026 Trend Chính)

2026 chuyển từ "single smart agent" sang **distributed, interoperable, multi-agent ecosystems**.

```
┌──────────────────────────────────────────────┐
│              User (High-Level Goal)          │
└────────────────────┬─────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│           SUPERVISOR / ORCHESTRATOR          │
│     (top-level planning + task routing)      │
└──────┬───────────────┬─────────────────┬────┘
       │               │                 │
┌──────▼──────┐ ┌──────▼──────┐  ┌───────▼──────┐
│  RESEARCHER │ │   CODER     │  │   REVIEWER   │
│   Agent     │ │   Agent     │  │    Agent     │
└──────┬──────┘ └──────┬──────┘  └───────┬──────┘
       │               │                 │
┌──────▼──────┐ ┌──────▼──────┐  ┌───────▼──────┐
│  Web Search │ │  Code Exec  │  │  Test Runner │
│   Tools     │ │   Tools     │  │    Tools     │
└─────────────┘ └─────────────┘  └──────────────┘
```

**Các pattern multi-agent phổ biến 2026:**

| Pattern | Mô tả |
|---------|-------|
| **Computer-Using Agent (CUA)** | Agent điều khiển máy tính như con người — click, type, browse |
| **Agent-to-Agent (A2A)** | Google protocol — agents giao tiếp với nhau, chia sẻ state |
| **Shared Tool Pool** | Multiple agents cùng access một bộ tools |
| **Hierarchical Task Networks** | Mỗi cấp agent có scope khác nhau |

### 3.3 Enterprise Architecture Layers

```
┌─────────────────────────────────────────┐
│         Agentic AI Applications          │
│  (Customer Support, SWE, Finance, etc.)  │
├─────────────────────────────────────────┤
│           Agent Framework Layer          │
│   (LangGraph, AutoGen, CrewAI, Mastra)   │
├─────────────────────────────────────────┤
│           LLM Foundation Layer            │
│   (GPT-4o, Claude 3.5, Gemini 2.0, etc.) │
├─────────────────────────────────────────┤
│        Tool & Integration Layer           │
│   (MCP, APIs, Code Runtime, RAG)         │
├─────────────────────────────────────────┤
│         Infrastructure Layer              │
│   (Compute, Storage, Monitoring)          │
└─────────────────────────────────────────┘
```

### 3.4 Key Frameworks (2025-2026)

| Framework | Đặc điểm | Vendor |
|-----------|---------|--------|
| **LangGraph** | Graph-based agent orchestration, state management, cycle handling | LangChain |
| **AutoGen** | Multi-agent conv, code execution, Microsoft ecosystem | Microsoft |
| **CrewAI** | Role-based agents, task delegation, enterprise-ready | CrewAI Inc |
| **Mastra** | TypeScript-first, structured agentic workflows | Mastra |
| **Flowise** | Visual drag-drop agent builder, low-code | Flowise |
| **AWS Bedrock Agents** | Managed agentic infrastructure, Nova models | AWS |
| **Google ADK + Agent Engine** | A2A protocol, agent interoperability | Google |
| **Snowflake AISQL** | Agentic AI trong database queries | Snowflake |

---

## 4. Khả Năng (Capabilities)

### 4.1 Khả Năng Cơ Bản

| Khả năng | Mô tả |
|----------|-------|
| **Autonomous Goal Pursuit** | Tự đặt mục tiêu con từ mục tiêu lớn, không cần human-in-the-loop ở mỗi bước |
| **Multi-Step Reasoning** | Suy luận qua nhiều bước, duy trì context qua toàn bộ task |
| **Tool Orchestration** | Gọi và phối hợp nhiều tools/API theo thứ tự |
| **Code Generation & Execution** | Viết và chạy code (Python, JS, shell) để thực thi task |
| **Web & API Interaction** | Browse web, gọi REST API, tương tác với external services |
| **Persistent Memory** | Ghi nhớ qua sessions, học từ interactions trước |
| **Self-Correction** | Phát hiện lỗi, retry, điều chỉnh approach khi fails |
| **File & Document Processing** | Đọc, viết, phân tích file (PDF, spreadsheet, code) |
| **Multi-Agent Collaboration** | Phối hợp với agents khác để chia nhỏ và hoàn thành task phức tạp |
| **Computer Use** | Điều khiển desktop/GUI — click, type, drag như người dùng thực |

### 4.2 Enterprise Use Cases (2025-2026)

| Lĩnh vực | Ứng dụng |
|----------|---------|
| **Software Engineering** | Autonomous code review, bug fix, PR creation, CI/CD pipeline |
| **Customer Support** | Agentic chatbots xử lý toàn bộ ticket — không chỉ trả lời mà thực sự resolve |
| **Finance** | Automated financial analysis, fraud detection, report generation |
| **Healthcare** | Clinical documentation, drug interaction analysis, patient triage |
| **Business Operations** | Autonomous workflow automation, data pipeline management |
| **Sales & CRM** | Lead qualification, follow-up sequences, pipeline management |
| **Legal** | Contract review, compliance checking, document analysis |

> Theo AaiNova (2026-03): **"40% of enterprise applications will include task-specific AI agents by year-end 2026, up from less than 5% in 2025."**

### 4.3 Production Readiness Indicators (2026)

Các dấu hiệu Agentic AI đã sẵn sàng production:

- **Agent SDKs production-ready** — tất cả major AI companies đều shipping agent SDKs (2025)
- **Standardized protocols** — MCP, A2A giải quyết vấn đề integration
- **Enterprise-grade guardrails** — security, compliance, audit logging
- **Cost optimization** — token optimization, caching, smarter tool selection
- **Reliability improvements** — self-healing, retry mechanisms, fallback strategies

---

## 5. Khác Với AI Truyền Thống

### 5.1 So Sánh Chi Tiết

| Tiêu chí | Traditional AI | Agentic AI |
|-----------|---------------|------------|
| **Paradigm** | Reactive — lắng nghe, đợi prompt | Proactive — chủ động hành động |
| **Input** | Prompt cụ thể, chi tiết | Mục tiêu cấp cao (high-level goal) |
| **Output** | Một response duy nhất | Multi-step execution → outcome |
| **Scope** | Single task | Multi-step workflows |
| **Decision-making** | Người quyết ở mỗi bước | Agent tự quyết, chịu trách nhiệm |
| **Adaptability** | Cố định theo training data | Thích ứng real-time qua feedback |
| **Context** | Context window hiện tại | Persistent memory + context |
| **Error handling** | Trả lỗi cho user | Self-correct, retry, fallback |
| **Human involvement** | Human-in-the-loop liên tục | Human-in-the-loop ở checkpoint |
| **Learning** | Static (sau training) | Dynamic — học từ mỗi task |
| **Output optimization** | Tối ưu output quality | Tối ưu overall outcome |

### 5.2 AI Truyền Thống vs GenAI vs Agentic AI

```
Traditional ML
├── Narrow task (classification, regression)
├── Fixed output space
├── Requires structured data
├── Human selects features + model
└── Static after deployment

Generative AI (GenAI)
├── Creates content (text, image, code)
├── Unbounded output space
├── Works with unstructured input
├── Human crafts prompt
└── Same model, different prompt each time

Agentic AI
├── Completes complex goals
├── Dynamic action sequencing
├── Multi-modal + multi-system
├── AI determines execution plan
└── Self-correcting loop, learns per task
```

### 5.3 Đừng Nhầm Lẫn

| Nhầm lẫn | Thực tế |
|----------|--------|
| "AI chatbot = Agent" | Chatbot chỉ respond, agent execute actions |
| "GenAI + automation = Agentic AI" | Cần autonomous goal pursuit + self-correction loop |
| "Agentic AI cần humanoid robot" | Không — agent operate trong digital environment |
| "Agentic AI hoàn toàn tự động" | Vẫn cần guardrails, checkpointing, human oversight |
| "Single LLM = Agentic AI" | Cần thêm: memory, tool use, planning, feedback loop |

### 5.4 Khi Nào Cần / Không Cần Agentic AI

| Dùng Agentic AI | Dùng Traditional AI/GenAI |
|----------------|--------------------------|
| Multi-step workflows (>3 bước) | Single task responses |
| Cross-system operations | Within-system queries |
| Long-running tasks (hours/days) | Real-time quick responses |
| Dynamic problem-solving | Predictable, routine tasks |
| Requires tool use (APIs, code, files) | Pure content generation |
| Uncertain/unstructured goals | Well-defined, bounded goals |

---

## 6. Thực Trạng & Triển Vọng (2025-2026)

### 2025: Năm Agent SDK Bùng Nổ

- Tất cả major AI vendors shipping production-ready agent SDKs
- MCP trở thành de facto standard cho tool integration
- Multi-agent orchestration từ experimental → production

### 2026: Từ Single Agent → Agent Ecosystem

- **2026 is clearly shifting from "single smart agent" to distributed, interoperable, multi-agent ecosystems**
- Patterns: Computer-Using Agents, Agent-to-Agent protocols
- 40% enterprise apps sẽ có task-specific agents (tăng từ <5% năm 2025)
- Câu hỏi không còn "có dùng agentic AI không" mà là "dùng như thế nào"

### Thách Thức Còn Lại

- **Hallucination** trong multi-step reasoning — errors compound qua các bước
- **Security & Governance** — agent có quyền thực thi thực tế, cần guardrails mạnh
- **Cost control** — multi-agent = multi-LLM-call = chi phí cao hơn nhiều
- **Reliability** — 99% reliability không đủ cho production chains (cần 99.99%)
- **Audit & Compliance** — traceable memory lineage là mandatory trong enterprise

---

## Related

- [[ai-agent-trends-2026-04-13]] — AI agent trends deep research
- [[ai-agent-infrastructure-2026]] — Agent infrastructure stack
- [[code-agents-claw]] — CLAW: Computer Launched Agentic Workers
- [[rag]] — RAG patterns (memory layer cho agents)
- [[mastra]] — TypeScript agent framework
- [[flowise]] — Visual agent builder
- [[skill-graph]] — Skill graph pattern cho content agents
