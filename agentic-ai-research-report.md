# Báo Cáo Nghiên Cứu: Agentic AI Agent
**Ngày cập nhật:** Tháng 4/2026
**Phạm vi:** Nghiên cứu 2025-2026

---

## 1. Định Nghĩa

### Agentic AI là gì?

**Agentic AI** (hay AI Agent) là một hệ thống AI tự chủ có khả năng hoạt động độc lập để đạt được các mục tiêu được xác định trước. Thuật ngữ "agentic" thể hiện khả năng của các hệ thống này để **hành động độc lập, theo cách định hướng mục tiêu**.

Theo định nghĩa khác, AI agents (còn gọi là compound AI systems hoặc agentic AI) là "một lớp các tác nhân thông minh được phân biệt bởi khả năng hoạt động tự chủ trong các môi trường phức tạp."

### Phân biệt Workflow vs Agent

| Khái niệm | Mô tả |
|-----------|-------|
| **Workflows** | Hệ thống nơi LLM và công cụ được điều phối thông qua các đường dẫn code được xác định trước |
| **Agents** | Hệ thống tự động hướng quá trình và việc sử dụng công cụ của chúng, duy trì quyền kiểm soát cách hoàn thành nhiệm vụ |

---

## 2. Các Thành Phần Cốt Lõi

### 2.1 Thành phần chính của AI Agent

| Thành phần | Chức năng |
|-----------|-----------|
| **Reasoning engines** | Xử lý suy luận và lập kế hoạch hành động |
| **Memory systems** | Lưu trữ và nhớ các tương tác trước đó với người dùng |
| **Cognitive skills** | Khả năng nhận thức và xử lý thông tin |
| **Tools và plugins** | Mở rộng khả năng của agent thông qua tích hợp bên ngoài |
| **Control flow (thường qua LLM)** | Điều khiển luồng xử lý và ra quyết định |
| **Orchestration software** | Tổ chức và điều phối các thành phần agent |

### 2.2 Cấu trúc mục tiêu phức tạp

AI agents sở hữu:
- **Complex goal structures** - Cấu trúc mục tiêu đa tầng, phức tạp
- **Natural language interfaces** - Giao diện ngôn ngữ tự nhiên
- **Capacity to act independently** - Khả năng hành động độc lập không cần giám sát liên tục
- **Tool integration** - Tích hợp phần mềm và hệ thống lập kế hoạch

### 2.3 Kiến trúc Memory

- **Short-term memory**: Lưu trữ ngữ cảnh hội thoại hiện tại
- **Long-term memory**: Tích lũy kiến thức và feedback qua thời gian
- **Reflexion pattern**: Sử dụng LLM để tạo phản hồi về kế hoạch hành động và lưu trữ trong memory cache

---

## 3. Mẫu Kiến Trúc (Architecture Patterns)

### 3.1 Các mẫu kiến trúc cốt lõi

| Mẫu | Mô tả |
|-----|-------|
| **Prompt Chaining** | Phân rã nhiệm vụ thành các bước tuần tự, mỗi LLM call xử lý output trước đó |
| **Routing** | Phân loại inputs và định hướng đến các task chuyên biệt |
| **Parallelization** | Chia LLM work thành các subtask độc lập hoặc voting cho outputs đa dạng |
| **Orchestrator-Workers** | Central LLM linh hoạt phân rã nhiệm vụ, ủy thác và tổng hợp kết quả |
| **Evaluator-Optimizer** | Một LLM tạo trong khi另一个 đánh giá trong vòng lặp |

### 3.2 Mẫu xử lý nâng cao

- **ReAct Pattern**: Quá trình lặp trong đó AI agent luân phiên giữa reasoning và taking actions
- **Planner-Critic**: Một agent đề xuất, agent khác đánh giá (iterative)
- **Sequential Processing**: Xử lý cố định, tuyến tính qua predefined pipeline
- **One-shot model querying**: Query model một lần để tạo plan of action

### 3.3 Kiến trúc triển khai (7-layer Reference Architecture - Ken Huang)

```
┌─────────────────────────────────────────┐
│ 7. Agent Ecosystem                      │ ← Giao diện với ứng dụng thực và users
├─────────────────────────────────────────┤
│ 6. Security & Compliance                │ ← Đảm bảo vận hành an toàn, bảo mật
├─────────────────────────────────────────┤
│ 5. Evaluation & Observability           │ ← Đánh giá safety và performance
├─────────────────────────────────────────┤
│ 4. Deployment & Infrastructure           │ ← Nền tảng kỹ thuật chạy agents
├─────────────────────────────────────────┤
│ 3. Agent Frameworks                     │ ← Tools đơn giản hóa phát triển
├─────────────────────────────────────────┤
│ 2. Data Operations                      │ ← Vector DB, data loaders, RAG
├─────────────────────────────────────────┤
│ 1. Foundation Models                     │ ← Core AI engines (LLM, etc.)
└─────────────────────────────────────────┘
```

### 3.4 Phân loại theo cấu trúc hệ thống

| Loại | Mô tả |
|------|-------|
| **Single-agent** | Một AI xử lý tất cả các nhiệm vụ một cách tuần tự |
| **Multi-agent - Horizontal** | Nhiều agents cộng tác cùng mức, lateral collaboration |
| **Multi-agent - Vertical** | Cấu trúc phân cấp, hierarchical |

---

## 4. Khả Năng Chính

### 4.1 Các đặc tính nổi bật

| Đặc tính | Mô tả |
|----------|-------|
| **Proactive** | Dự đoán nhu cầu, nhận diện patterns, chủ động sáng kiến |
| **Adaptable** | Điều chỉnh hành động dựa trên real-time input và context |
| **Collaborative** | Làm việc cùng humans và other AI agents |
| **Specialized** | Được xây dựng trên nhiều agents có chuyên môn hóa cao |

### 4.2 Chu kỳ hoạt động 4 giai đoạn

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ PERCEIVE│────▶│ REASON  │────▶│   ACT   │────▶│  LEARN  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │                                               │
     └───────────────────────────────────────────────┘
                     Continuous Loop
```

| Giai đoạn | Chi tiết |
|-----------|----------|
| **Perceive** | Thu thập real-time data từ đa dạng nguồn qua APIs |
| **Reason** | Powered by LLMs, diễn giải context và phát triển action plans |
| **Act** | Thực thi nhiệm vụ, tương tác với applications, có thể cần human approval |
| **Learn** | Sử dụng reinforcement learning (PPO, Q-learning) để cải thiện liên tục |

### 4.3 Khả năng tự chủ (Autonomy Levels)

Mức độ tự chủ của AI agents được so sánh với phân loại SAE của xe tự lái:

| Level | Mô tả |
|-------|-------|
| **Level 2-3** | Majority of applications hiện tại |
| **Level 4** | Đạt được trong một số trường hợp chuyên biệt cao |

### 4.4 Khả năng nhận thức (Cognitive)

- **RAG (Retrieval-Augmented Generation)**: Truy cập knowledge động
- **Tool/Agent Registry**: Tổ chức software functions hoặc các agents khác
- **Multi-turn reasoning**: Suy luận qua nhiều bước hội thoại
- **Iterative refinement**: Cải thiện liên tục thông qua feedback loops

---

## 5. Sự Khác Biệt với AI Truyền Thống

### 5.1 So sánh tổng quan

| Tiêu chí | AI Truyền thống | Agentic AI |
|----------|-----------------|------------|
| **Đặc điểm chính** | Content creation, prediction | Decision-making, autonomous action |
| **Sự tương tác** | Reactive - đợi user prompt | Proactive - tự động khởi tạo hành động |
| **Giám sát** | Continuous oversight required | Không cần oversight liên tục |
| **Độ phức tạp task** | Single, well-defined tasks | Complex, multi-step workflows |
| **Memory** | Stateless (thường) | Stateful với memory systems |
| **Tool usage** | Không có hoặc hạn chế | Tích hợp rộng rãi với external tools |
| **Output** | Content, predictions | Actions, decisions, task completion |

### 5.2 Đặc điểm cốt lõi phân biệt

| AI Truyền thống | Agentic AI |
|----------------|------------|
| Generative content | **Goal-oriented action** |
| Single-turn hoặc limited context | **Multi-turn, persistent memory** |
| Passive response | **Active initiation** |
| Predefined workflows | **Dynamic, model-driven decision-making** |
| Limited to training data | **RAG - dynamic knowledge retrieval** |

### 5.3 Trade-offs

| Khía cạnh | AI Truyền thống | Agentic AI |
|-----------|-----------------|------------|
| **Latency** | Thấp hơn | Cao hơn |
| **Cost** | Thấp hơn | Cao hơn (do complexity) |
| **Reliability** | Predictable | Flexible nhưng có thể unpredictable |
| **Scalability** | Tốt cho simple tasks | Tốt cho complex, scale-sensitive tasks |

### 5.4 Khi nào sử dụng loại nào

| Tình huống | Loại AI phù hợp |
|-----------|----------------|
| Simple prompts, direct answers | **Single LLM call** (truyền thống) |
| Well-defined, predictable tasks | **Workflows** |
| Flexibility, model-driven decisions at scale | **Agents** |

---

## 6. Best Practices (Anthropic Guidelines)

### Nguyên tắc cốt lõi khi xây dựng Agents

1. **Maintain simplicity** - Chỉ thêm complexity khi giải pháp đơn giản không đủ
2. **Prioritize transparency** - Đảm bảo có thể giải thích được hành động của agent
3. **Craft careful ACI (Agent-Computer Interface)** - Thiết kế interface giống như HCI

### Tool Design Best Practices

- Đặt mình vào perspective của model
- Làm cho parameter names trở nên rõ ràng, obvious
- Test extensively
- Sử dụng "poka-yoke" - làm cho mistakes khó xảy ra

---

## 7. Use Cases Nổi bật (2025-2026)

| Lĩnh vực | Ứng dụng |
|----------|-----------|
| **Customer Support** | Kết hợp hội thoại với tool integration để truy cập data và thực hiện actions |
| **Coding Agents** | Code có thể verify qua automated tests, cho phép iterative refinement |
| **Research & Analysis** | Tự động thu thập, tổng hợp thông tin từ nhiều nguồn |
| **Software Development** | Autonomous agents xây dựng, test và deploy phần mềm |
| **Enterprise Automation** | Xử lýworkflows phức tạp, tự động hóa quy trình nghiệp vụ |

---

## 8. Tóm tắt

### Key Takeaways

1. **Agentic AI** = AI có khả năng hành động tự chủ, định hướng mục tiêu
2. **Core components**: Reasoning engines, Memory systems, Tools, Orchestration
3. **Architecture patterns**: Single-agent, Multi-agent (horizontal/vertical)
4. **Khả năng chính**: Proactive, Adaptable, Collaborative, Self-learning
5. **Điểm khác biệt**: Decision-making > Content creation, Autonomous > Reactive

### Xu hướng 2025-2026

- **Multi-agent systems** ngày càng phổ biến
- **Autonomy levels** đang được nâng cao dần
- **ACI (Agent-Computer Interface)** trở thành focus quan trọng
- **Cost-latency tradeoffs** được cân bằng tốt hơn

---

## Nguồn tham khảo

- [AWS - What is Agentic AI](https://aws.amazon.com/what-is/agentic-ai/)
- [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Wikipedia - Agentic AI](https://en.wikipedia.org/wiki/Agentic_AI)
- [IBM - What is Agentic AI](https://www.ibm.com/topics/agentic-ai)
