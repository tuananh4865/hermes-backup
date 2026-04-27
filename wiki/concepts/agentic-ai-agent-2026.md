---
title: Agentic AI Agent — Báo cáo Nghiên cứu 2025-2026
created: 2026-04-27
updated: 2026-04-27
type: concept
tags: [agent, ai-agent, architecture, agentic-ai]
confidence: high
relationships: [ai-agent-trends-2026-04-10, ai-agent-trends-2026-04-12, ai-agent-trends-2026-04-13, rag, lm-studio, mcp]
---

# Agentic AI Agent — Báo cáo Nghiên cứu 2025-2026

> **Scope:** Định nghĩa, thành phần cốt lõi, kiến trúc, khả năng, và sự khác biệt với AI truyền thống.
> **Nguồn:** 25+ bài báo, paper, và tài liệu kỹ thuật từ 2025-2026.

---

## 1. Định nghĩa

### Định nghĩa chính thức

**Agentic AI** là hệ thống AI được thiết kế để **tự chủ động theo đuổi mục tiêu phức tạp** — không chỉ phản hồi một prompt đơn lẻ, mà liên tục thực hiện chuỗi quyết định và hành động để đạt được kết quả mong muốn.

**AI Agent** (hay đơn giản là "agent") là một hệ thống tự trị sử dụng LLM làm engine reasoning, kết hợp với tools, memory, và instructions để theo đuổi mục tiêu đa bước mà không cần human-in-the-loop ở mỗi bước.

Theo NJ Raman (2026):

> *"An agent is a Perceive → Reason → Act → Observe (PRAO) loop running over an extended horizon, where the model retains or reconstructs enough context to act coherently across steps."*

Theo Google Cloud Architecture documentation:

> *"An agent is an application that achieves a goal by processing input, performing reasoning with available tools, and taking actions based on its decisions."*

Theo Springer Nature — Artificial Intelligence Review (2025):

> *"An AI Agent is a self-contained autonomous system designed to accomplish a goal. It operates primarily in isolation, though it may interact with tools and APIs. Its agency is defined by its autonomy, proactivity, and its ability to complete a task from start to finish independently."*

### Phân biệt Agentic AI vs AI Agent

| Khái niệm | Ý nghĩa |
|-----------|---------|
| **AI Agent** | Một hệ thống đơn lẻ — nhận mục tiêu, tự hoàn thành công việc |
| **Agentic AI** | Trường phái kiến trúc rộng hơn — có thể điều phối multi-agent, thể hiện mức độ tự chủ cao |
| **Multi-Agent System** | Nhiều agent chuyên biệt phối hợp với nhau qua message passing |

Theo một số tài liệu, **Agentic AI** là lớp capability, còn **AI Agent** là construct phần mềm sử dụng capability đó làm reasoning engine.

---

## 2. Thành phần cốt lõi

Mọi production-grade AI agent đều built from **4 thành phần nền tảng** (Agentic Academy, 2026):

### 2.1 Reasoning Engine (LLM — "Brain")

LLM là "brain" của agent. Nó interpret inputs, reason about next steps, và generate outputs — có thể là natural language, tool call, hoặc quyết định dừng lại.

- Context windows: 128K → 2M tokens (2026 frontier)
- Native tool-calling support
- Chain-of-thought, Tree-of-thoughts reasoning
- Model quality directly shapes agent capability

### 2.2 Tools ("Hands")

**Tools** là cách agent tương tác với thế giới bên ngoài. Không có tools, agent chỉ là text generator.

Các loại tools phổ biến:
- **Knowledge tools**: databases, documents, APIs, vector search, web browsing
- **Action tools**: tạo records, gửi messages, trigger workflows
- **Code execution**: chạy Python, shell commands
- **UI manipulation**: computer-use agents điều khiển giao diện

Về mặt kỹ thuật, tool là **typed function signature** mà model emit dưới dạng structured call (JSON), runtime intercepts và executes.

**Model Context Protocol (MCP)** — introduced by Anthropic (Nov 2024), adopted by OpenAI (Mar 2025) — đã trở thành de facto standard cho agent-tool communication.

### 2.3 Instructions ("Identity")

Instructions định nghĩa agent là ai và behave thế nào. Có 3 layers:

| Layer | Vai trò |
|-------|---------|
| **Agent instructions** | Identity, expertise, behavioral rules |
| **Workflow instructions** | Step-by-step procedures cho specific tasks |
| **System instructions** | Organizational constraints, strategic intent, safety boundaries |

### 2.4 Memory ("Continuity")

Memory là thành phần phân biệt agent với stateless chatbot. Có 4 layers:

| Layer | Scope | Infrastructure |
|-------|-------|----------------|
| **In-Context (Short-term)** | Current session, conversation | Context window |
| **Episodic** | Specific past events, session logs | Vector DB, logs |
| **Semantic** | Factual knowledge | Knowledge graphs, RAG |
| **Procedural** | Learned behaviors, tool definitions | Frozen in weights |

Short-term memory: conversation context, what user asked, what tools returned, what decisions were made.

Long-term memory: user preferences, past interactions, learned facts — persisting across sessions.

---

## 3. Kiến trúc

### 3.1 Core Loop: PRAO (Perceive → Reason → Act → Observe)

Đây là nền tảng kiến trúc của mọi agentic system:

```
1. Perceive  → Nhận input (user message, tool output, system event, API response)
2. Reason    → LLM đánh giá state, cân nhắc tools + instructions, quyết định action tiếp theo
3. Act       → Execute action (call tool, generate response, request info)
4. Observe   → Đánh giá kết quả. Đã đạt goal? Cần continue? Cần adapt?
5. Loop      → Repeat cho đến khi goal satisfied hoặc stop condition reached
```

ReAct (Reason + Act) — introduced by Yao et al. ICLR 2023 — là pattern phổ biến nhất, interleaves reasoning traces với action execution trong một loop.

### 3.2 Planning Strategies

| Strategy | Mô tả | Phù hợp khi |
|----------|-------|-------------|
| **Reactive (step-by-step)** | Quyết định từng bước một | Ambiguous tasks, novel situations |
| **Plan-then-Execute** | Tạo full plan trước, execute sau | Clear sequential dependencies (data pipelines, form processing) |
| **Hybrid** | High-level upfront plan + dynamic re-plan | Complex real-world tasks |

**Tree-of-Thoughts** và **Language Agent Tree Search (LATS)** cho phép agent explore nhiều reasoning paths, đánh giá và chọn optimal approach.

### 3.3 Kiến trúc đa agent

| Architecture | Mô tả |
|-------------|-------|
| **Single Agent** | Một agent handle tất cả. Đơn giản nhưng limited. |
| **Sequential / Pipeline** | Agents handoff cho nhau theo defined order |
| **Parallel** | Multiple agents work simultaneously trên different aspects |
| **Supervisor-Worker** | Central orchestrator decomposes goal, delegates subtasks, collects results |
| **Hierarchical** | Supervisory agent delegates to subordinates, subordinates có thể delegate tiếp |
| **Adaptive/Decentralized** | Agents communicate peer-to-peer, no central coordinator |

**Orchestrator** (supervisor) pattern phổ biến nhất trong production enterprise systems.

### 3.4 Production Agent Architecture Stack (6 layers)

Theo NJ Raman (2026) — production-grade agent có 6 components:

```
Layer 1: Foundation Model (LLM reasoning engine)
Layer 2: Tool Interface (function calling, MCP)
Layer 3: Memory System (4 layers: in-context, episodic, semantic, procedural)
Layer 4: Planning Module (task decomposition, ReAct/ToT/LATS)
Layer 5: Orchestration Layer (workflow coordination, multi-agent)
Layer 6: Guardrails & Safety (policy enforcement, audit, sandboxing)
```

### 3.5 Các framework phổ biến (2026)

| Framework | Type | Đặc điểm |
|-----------|------|----------|
| **LangGraph** | Graph-based orchestration | Cycles, state machines, production-grade |
| **LangChain** | General agent framework | Batteries included, but verbose |
| **CrewAI** | Multi-agent | Role-based agents, sequential + parallel workflows |
| **AutoGen** | Multi-agent | Microsoft, conversation-based |
| **Mastra** | Agent framework | Built on TypeScript |
| **Flowise** | Visual builder | Low-code agent builder |
| **n8n** | Workflow + AI | Automation with AI nodes |

---

## 4. Khả năng (Capabilities)

### 4.1 Core Capabilities

| Capability | Mô tả |
|-----------|-------|
| **Autonomy** | Khởi tạo và hoàn thành tasks độc lập, không cần human tại mỗi bước |
| **Goal-Oriented** | Đặt và điều chỉnh goals động dựa trên context và feedback |
| **Multi-step Execution** | Decompose goals thành subtasks, execute tuần tự hoặc song song |
| **Tool Use** | Invoke external systems: APIs, databases, code execution, web browsing |
| **Environmental Interaction** | Tương tác với APIs, file systems, databases, communication channels |
| **Adaptability** | Thay đổi strategy khi gặp unexpected conditions hoặc failures |
| **Memory** | Retain context within session (short-term) và across sessions (long-term) |
| **Self-Correction** | Self-critique, phát hiện lỗi, retry với alternative approach |
| **Learning from Feedback** | Đánh giá outcomes, refine internal strategies theo thời gian |
| **Reasoning** | Chain-of-thought, đánh giá nhiều options, contextual decision-making |

### 4.2 Đặc biệt về Multi-Agent

| Capability | Mô tả |
|-----------|-------|
| **Inter-Agent Communication** | Message passing, shared workspaces, structured protocols |
| **Dynamic Routing** | Route tasks to best-equipped peer agent |
| **Collaborative Problem-Solving** | Multiple specialized agents giải quyết complex problems |
| **Hierarchical Delegation** | Supervisor decompose và delegate recursively |

### 4.3 Autonomy Spectrum (4 Levels)

| Level | Type | Description |
|-------|------|-------------|
| **L1** | Copilot | Assistive suggestion, human does the work |
| **L2** | Assistant | Executes predefined steps, narrow autonomy |
| **L3** | Agent | Goal-oriented execution, decides own actions |
| **L4** | Swarm | Multi-agent coordination, collective autonomy |

---

## 5. Agentic AI vs Traditional AI

### So sánh tổng thể

| Dimension | Traditional AI | Agentic AI |
|-----------|---------------|------------|
| **Operational Mode** | Reactive — waits for prompt, responds to input | Proactive — pursues goals, initiates actions independently |
| **Decision Making** | Predefined rules, decision trees | Reasons autonomously, evaluates options |
| **Adaptability** | Rigid — breaks when conditions change | Flexible — adapts strategy based on outcomes |
| **Context Handling** | Limited to programmed scenarios | Understands nuance, handles ambiguity |
| **Learning** | Static after deployment, needs retraining | Continuous improvement through feedback loops |
| **Tool Use** | Hardcoded integrations only | Dynamic tool selection and API orchestration |
| **Error Handling** | Fails or follows error branch | Attempts alternative approaches autonomously |
| **Task Scope** | Narrow, single-step tasks | Complex, multi-step workflows |
| **Memory** | Stateless or session-based | Persistent, cross-session memory |
| **Human Oversight** | Required for all decisions | Goal-setting and exception handling only |
| **Core Paradigm** | Rule-based, reactive | Goal-oriented, proactive |
| **Output** | A response (text, image, prediction) | A completed outcome or project |

### Sự khác biệt cốt lõi

**Traditional AI:**
- Là **reactive tool** — bạn hỏi, nó trả lời
- Hoạt động trong fixed, narrowly defined rules
- Không có khả năng tự quyết định bước tiếp theo
- Không adapt được khi conditions change
- Learning: batch retraining (weekly/monthly)

**Agentic AI:**
- Là **proactive agent** — nhận mục tiêu, tự tìm cách đạt được
- Understands context, sets objectives, analyzes alternatives, revises plan along the way
- Writes its own "if-then" paths, improvises solutions, reprioritizes goals
- Near real-time learning from feedback
- Operates across multiple systems without human intervention at each step

### Ví dụ minh họa

| Task | Traditional AI | Agentic AI |
|------|---------------|------------|
| "Tối ưu SEO website" | Liệt kê tips chung | Research, integrate, test, iteratively refine — tự làm hết |
| "Xử lý customer ticket" | Phân loại và gợi ý response | Hiểu issue, tra cứu account, process resolution, communicate với customer |
| "Research competitor" | Tìm và tổng hợp thông tin | Decompose question, gather from multiple sources, synthesize report, deliver completed output |

Theo GSD Council (2026):

> *"Classic AI has no facility to make its own decisions; it can only react to input injected by human beings... It is reactive. It will never act except when told."*

> *"Agentic AI is proactive in navigating the environment and tends to adapt in the process of acting purposefully... While conventional AI is a tool that has to be told what to do, agentic AI is much more like a teammate that can think, learn, and act on its own."*

### Câu nói tổng kết

> *"Traditional AI follows instructions. Agentic AI pursues objectives."*

— Planetary Labour, 2026

> *"Give traditional AI a task with specific steps, and it executes them. Give agentic AI a goal, and it determines the steps needed, adapts when things go wrong, and keeps working until the objective is achieved."*

---

## 6. Tổng kết

Agentic AI Agent represent một **paradigm shift** từ reactive tool sang autonomous, goal-oriented system:

- **Định nghĩa:** Hệ thống tự chủ đạt mục tiêu qua Perceive → Reason → Act → Observe loop
- **4 thành phần cốt lõi:** Reasoning Engine (LLM), Tools, Instructions, Memory
- **Kiến trúc:** PRAO loop + planning strategies + multi-agent patterns (sequential, parallel, hierarchical)
- **Khả năng:** Autonomy, multi-step execution, tool use, adaptation, self-correction, learning
- **Khác AI truyền thống:** Proactive vs reactive, goal-oriented vs rule-based, adaptive vs static, continuous learning vs batch retraining

**Thị trường:** Agentic AI market projected $5.25B (2024) → $199B (2034). Đến 2026, 40% enterprise apps sẽ có AI agents (tăng từ <5% năm 2025).

---

## Nguồn

- NJ Raman — "The Architecture of Agency: A Deep Technical Guide to Agentic AI Systems in 2026" (Medium, Apr 2026)
- Google Cloud — "Choose your agentic AI architecture components" (2026)
- Agentic Academy — "How Do AI Agents Work? Architecture, Components, and Patterns" (Mar 2026)
- Planetary Labour — "Agentic AI vs Traditional AI: What's Changed? Complete Guide 2026" (Jan 2026)
- Exabeam — "Agentic AI Architecture: Types, Components & Best Practices" (Oct 2025)
- Springer Nature — "Agentic AI: a comprehensive survey of architectures, applications, and future directions" (Artificial Intelligence Review, Nov 2025)
- AWS Prescriptive Guidance — "Comparing traditional AI to software agents and agentic AI" (2026)
- Poorani TSR — "The Building Blocks of Agentic AI" (Medium, Feb 2026)
- Harshalsant — "Agentic AI Architecture: The Complete Deep Dive" (Medium, Apr 2026)
- AAIA Research — "Introduction to Agentic AI: The Architecture of Autonomy" (Jan 2026)
- Redis — "Agentic AI System Components: Building Production-Ready Agents" (Feb 2026)
- Glean — "7 Core Components of an AI Agent Architecture Explained" (Apr 2026)
- FullStack — "Agentic AI vs Traditional AI: Key Differences" (Apr 2026)
- arxiv — "A Survey on LLM-based Agents" (2601.12560, 2026)
- arxiv — "Agentic AI: Planning, Memory, and Tool Use" (2601.02749, 2026)
- GSDA Council — "How Does Agentic AI Differ from Traditional AI?" (2026)
- Classic Informatics — "Agentic AI vs Traditional AI: Key Differences & Use Cases" (Sep 2025)
- Zencoder — "Agentic AI vs AI Agents: What's the Real Difference?" (Dec 2025)
- Jishu Labs — "Building AI Agents for Enterprise: A Practical Guide to Agentic AI in 2026" (Feb 2026)
- ScaleMind — "Agentic AI Fundamentals: Planning, Tools, Memory, and Control Loops" (Feb 2026)
- Moxo — "Agentic AI Architecture: Planning, Memory, and Tool Use" (Feb 2026)
- Nevo — "AI Agent Components: Memory, Reasoning, Tools, and Planning" (Mar 2026)
- GoPenAI — "The Core Architecture of AI Agents" (Mar 2026)
- Synvestable — "Agentic AI Systems: Enterprise Implementation Guide 2026" (Jan 2026)
- Calmops — "Agentic AI Architecture: Building Autonomous AI Systems in 2026" (Mar 2026)
- Leobit — "Agentic AI vs Traditional Automation" (Apr 2026)
- Beyond Key — "Agentic AI vs Traditional AI" (Dec 2025)
- Prismberry — "The Autonomy Revolution: Agentic AI vs Traditional AI" (Dec 2025)
- AppsInsider — "Agentic AI vs Traditional AI: 10 Key Differences 2026" (Jan 2026)
- AI Agents Kit — "AI Agents vs Agentic AI: What's the Real Difference?" (Mar 2026)

---

*Report compiled: 2026-04-27*
