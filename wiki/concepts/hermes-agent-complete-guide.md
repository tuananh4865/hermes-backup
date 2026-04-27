---
title: "Hermes Agent Complete Guide"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [hermes, agent, documentation]
---

# Hermes Agent — Complete Guide (橙皮书)

> Nguồn: [hermes-agent-orange-book](https://github.com/alchaincyf/hermes-agent-orange-book) by 花叔 (HuaShu)
> Phiên bản: v260407 (dựa trên Hermes v0.7.0)
> Tài liệu đầy đủ: [PDF (Chinese)](https://github.com/alchaincyf/hermes-agent-orange-book/raw/main/Hermes-Agent-从入门到精通-v260407.pdf)

---

## Tổng Quan

Hermes Agent là framework mã nguồn mở của [Nous Research](https://nousresearch.com), ra mắt Feb 2026. Điểm khác biệt cốt lõi so với OpenClaw/Claude Code: **built-in self-improving learning loop + three-layer memory + automatic Skill creation & evolution**.

Harness Engineering concept lần đầu được productize hoàn chỉnh.

**17 chapters, 5 parts:**

| Part | Content | Chapters |
|------|---------|----------|
| Concepts | Từ Harness đến Hermes | §01-02 |
| Core Mechanisms | Learning loop, memory, Skills, tools | §03-06 |
| Hands-On Setup | Installation, first conversation, multi-platform | §07-11 |
| Real-World Scenarios | Knowledge assistant, dev, content, multi-Agent | §12-15 |
| Deep Thinking | Three-way comparison, self-improving boundaries | §16-17 |

---

## §01 — Từ Harness Engineering đến Hermes

### Harness Engineering là gì?

LangChain team làm experiment: cùng model (GPT-5.2-Codex), chỉ adjust "harness" configuration, accuracy từ 52.8% → 66.5%, rank từ Top 30 → Top 5. Model không đổi dòng nào.

Mitchell Hashimoto đặt tên: **Harness Engineering** — mỗi lần AI sai, thêm một rule vào CLAUDE.md. File là活的 (alive), luôn growing.

### Five Components Mapping

| Harness Component | Manual Implementation | Hermes Built-in |
|-------------------|----------------------|------------------|
| Instructions | Hand-write CLAUDE.md | Skill system (markdown, auto-create + self-improve) |
| Constraints | Config hooks/linter/CI | Tool permissions + sandbox + toolset on-demand |
| Feedback | Manual review / evaluator agent | Self-improving learning loop (auto review after tasks) |
| Memory | Manual knowledge base | Three-layer memory + Honcho user modeling |
| Orchestration | Manual multi-agent pipeline | Subagent delegation + cron scheduling |

Hermes = 5 components đều built-in + auto operate.

### Điểm khác biệt so với OpenClaw

- **OpenClaw**: Bạn viết SOUL.md, nó thành hình bạn muốn.记忆系统完善，Skill生态庞大，但主要靠人工编写维护。
- **Hermes**: 5 dimensions đều built-in + tự động vận hành. Bạn không cần ngồi cấu hình, nó tự học từ experience.

### Trois工具不是替代，是递进

- **Claude Code**: 交互式编码 — bạn ngồi terminal, realtime collaboration. Là kỹ sư pair programming.
- **OpenClaw**: 配置即行为 — viết SOUL.md, nó thành hình bạn muốn. Config minh bạch, ClawHub 44000+ Skills.
- **Hermes**: 自主后台+自改进 — bạn không cần ngồi đó. Nó tự chạy, tự học, tự进化. 24/7 online, qua Telegram/Discord.

> **核心建议**: Claude Code đủ nếu chỉ viết code. Muốn 7x24 backend agent tự grow thông minh → xem Hermes.

---

## §02 — Hermes Agent全景：60秒看懂

### Architecture

```
学习循环 → 三层记忆 → Skill系统 → 40+工具 → 多平台Gateway
```

- **学习循环**: Hermes的心脏。每次完成任务 tự động复盘:记住什么、提炼什么Skill、现有 Skill需不需要优化。持续运转，không cần manual trigger.
- **三层记忆**: Hermes的大脑。会话记忆记住「刚才发生什么」，持久记忆记住「你是谁」，Skill记忆记住「怎么做事」。
- **Skill系统**: Hermes的技能库。每个 Skill = markdown file trong `~/.hermes/skills/`。会self-evolve.
- **40+工具**: Hermes的手脚。5 categories: 执行、信息、媒体、记忆、协调。
- **多平台Gateway**: Hermes的入口。12+ platforms: Telegram, Discord, Slack, WhatsApp...

### Key Data

| Metric | Value |
|--------|-------|
| GitHub stars | 27,000+ (2 tháng) |
| 内置工具 | 40+ |
| 支持平台 | 12+ |
| MCP可接入 | 6,000+ 应用 |
| 子Agent并发 | 最多3个 |
| 最低部署成本 | $5/月 VPS |
| 内存占用 | <500MB (不跑本地LLM) |
| 许可证 | MIT |

---

## §03 — 学习循环：Agent自己给自己造缰绳

### Five-Stage Flywheel

```
策划记忆 → 创建Skill → Skill自改进 → FTS5召回 → 用户建模
```

**环节一：策划记忆**
- Mỗi turn xong, Hermes chủ động quyết định cái gì đáng记住
- Không phải để nguyên đống history, mà tự review: có gì mới, user có preference mới không
- Nudge mechanism định kỳ nhắc Agent回顾近期交互

**环节二：自主创建Skill**
- Khi hoàn thành complex task, hỏi: "Solution này sau này còn dùng không?"
- Nếu yes → tạo Skill file trong `~/.hermes/skills/`
- Ví dụ: CSV to database task → tạo `csv-to-database.md` ghi lại steps + preferences

**环节三：Skill自改进**
- Skill tạo ra không phải end point
- User feedback → Hermes update Skill file
- VD: "nên check table tồn tại trước" → không chỉ sửa output, mà back-update Skill

**环节四：FTS5跨会话召回**
- SQLite FTS5 full-text index
- Mỗi conversation mới, search relevant history → load related chunks
- Không load all history, chỉ load cái liên quan

**环节五：用户建模 (Honcho)**
- Optional external integration (Plastic Labs)
- Infer preferences từ behavior patterns, không chỉ what user said
- VD: thấy user toàn chọn cheapest option → infer "cost-sensitive"

### Key Distinction

| | Traditional AI Memory | Hermes Memory |
|--|----------------------|---------------|
| Format | 对话记录堆积 (录像带) | 经验蒸馏 (笔记本) |
| Behavior | Càng thêm càng dài → tràn | Có index → dùng mãi mãi |
| Improvement | Không | Tự cải thiện |

### Mitchell Hashimoto的对比

| | Mitchell (手动) | Hermes (自动) |
|--|----------------|---------------|
| 规则来源 | Người观察到问题后手写 | Agent自己从反馈提炼 |
| 存储位置 | CLAUDE.md (single file) | 多Skill文件 + 记忆数据库 |
| 触发改进 | 人记得要加才加 | 每次使用后自动评估 |
| 跨项目迁移 | 需要手动复制 | Skill全局生效 |
| 改进速度 | 取决于人的勤快程度 | 持续自动 |

---

## §04 — 三层记忆：从金鱼到老友

### 为什么记忆是最难的问题

AI的记忆 không phải đơn giản là "存聊天记录". Active user một ngày几千字，一个月几万字。全塞进去 → context window tràn hoặc model bị overload vì信息太多。

好的记忆系统: 不是存得多，是找得准。

### 三层架构

**第一层：会话记忆**
- 回答: "发生了什么？"
- 技术: SQLite + FTS5 full-text index
- 设计决策: 按需检索而不是全量加载

| | 全量加载 | FTS5按需检索 |
|--|---------|-------------|
| 上下文占用 | 线性膨胀 → tràn | 基本恒定 |
| 检索精度 | 什么都有，什么都找不到 | 精准匹配 |
| 长期可用性 | 几天后就撑不住 | 可用几个月甚至几年 |
| 响应速度 | 越来越慢 | 基本不变 |

**第二层：持久记忆**
- 回答: "你是谁？"
- 内容: preferences, project习惯, 常用工具链, 工作时间规律
- 技术: SQLite,纯文件级, 无外部服务器
- 便携性: `~/.hermes/` backup → 迁移到 máy mới

**第三层：Skill记忆**
- 回答: "怎么做事？"
- 三层对应认知科学三种记忆:

```
情景记忆 (发生了什么) → 语义记忆 (世界是什么样的) → 程序性记忆 (怎么做事)
```

### Honcho用户建模

可选external provider (Plastic Labs). Làm việc sâu hơn "记住你说了什么" — nó infer你没说的东西.

Ví dụ: 连续三周每天写Python脚本 → Honcho có thể infer:
- 技术水平: 不是纯新手但也不是专家
- 工作节奏: 通常在晚上9-11点活跃
- 沟通风格: 喜欢先看结果再问原理
- 目标推断:可能在准备数据分析项目
- 情绪模式: 代码报错时会有点急躁

### 和Claude Code对比

| Dimension | Claude Code | Hermes Agent |
|-----------|-------------|--------------|
| 记忆格式 | CLAUDE.md + auto-memory文本文件 | SQLite + FTS5 + Skill文件 |
| 写入方式 | CLAUDE.md手动写，auto-memory半自动 | 全自动写入 |
| 检索方式 | 启动时全量加载CLAUDE.md | 按需FTS5检索 |
| 记忆粒度 | 项目级（每项目一份CLAUDE.md） | 全局级 + 项目级 |
| 用户建模 | 无 | Honcho自动推理 |
| 程序性记忆 | CLAUDE.md中的指令 | 独立Skill文件，可自改进 |

### 记忆的Limitations

**什么不该记:**
- 一次性任务细节 (生日贺词)
- 过时信息 (旧API版本号)
- 错误的推断
- 敏感信息 (密码、密钥)

> ⚠️ **Lưu ý**: Hermes目前没有自动过期机制。记忆数据库会持续增长。建议定期检查 `~/.hermes/` 大小，清理过时Skill。

---

## §05 — Skill系统：会自我进化的能力

### Skill是什么

每个Skill = markdown file trong `~/.hermes/skills/`. Ghi lại **程序性记忆**: Agent怎么做某件事.

三种来源:

| 来源 | 说明 | 数量 |
|------|------|------|
| Bundled Skills | 安装时自带，覆盖常见场景 | 40+ |
| Agent自主创建 | 完成复杂任务后自动提炼 | 按使用积累 |
| Skills Hub | 社区贡献，一键安装 | 持续增长 |

### agentskills.io 标准

Skill不是封闭生态。采用 **agentskills.io 标准**, 30+ tools support (Claude Code, Cursor, Copilot, Gemini CLI...).

你为Claude Code写的Skill → 直接在Hermes用。反过来也一样.

> USB接口逻辑: 一个Skill插到哪都能跑. 不是App Store的"每个平台一套生态".

### 自改进机制 (最大区别)

```
1. 执行Skill → Agent按Skill步骤完成任务
2. 收集反馈 → 用户反应记录到会话记忆
3. 更新Skill → Agent分析反馈，自动修改Skill文件
4. 下次执行 → 使用新版本Skill
```

### 和OpenClaw对比

| Dimension | OpenClaw Skill | Hermes Skill |
|-----------|----------------|--------------|
| 创建方式 | 人工编写SOUL.md | Agent自主创建+人工编写 |
| 维护方式 | 人工更新 | 自动进化+人工干预 |
| 个性化 | 通用模板，user fork后自定义 | 从你的使用习惯中自然生长 |
| 生态规模 | 44000+ (大) | 40+预置+社区 (成长中) |

### 实战：创建Skill的过程

Yêu cầu: "每天早上整理昨天的GitHub通知"

第三次/第四次之后, Hermes sẽ tạo file như:

```markdown
# GitHub Daily Digest
## 触发条件
用户提到"GitHub通知"、"每日总结"等关键词
## 执行步骤
1. 调用GitHub MCP获取过去24小时的通知
2. 过滤掉bot账号的自动通知
3. 按类型分组（PR / Issue / Discussion）
4. 按重要程度排序
5. 以简洁列表形式呈现
## 用户偏好
- 不需要详细内容，只要标题和状态
- PR和Issue分开显示
```

---

## §06 — 40+工具与MCP：连接一切

### 五大类工具

| 类别 | 核心工具 | 功能 |
|------|---------|------|
| 执行类 | terminal, code_execution, file | 跑命令、执行代码（沙箱隔离）、读写文件 |
| 信息类 | web, browser, session_search | 搜索网页、浏览器自动化、检索历史对话 |
| 媒体类 | vision, image_gen, tts | 理解图片、生成图片、文字转语音 |
| 记忆类 | memory, skills, todo, cronjob | 操作记忆层、管理Skill、任务规划、定时调度 |
| 协调类 | delegation, moa, clarify | 委派子Agent、多模型推理、向用户请求澄清 |

### 值得注意的工具

- **session_search**: FTS5全文索引搜索历史对话 + LLM摘要. Cho phép "上周我们讨论过的那个方案"
- **moa** (Multi-model Orchestrated Answering): 同时调用多个LLM，综合回答. 用于高可靠性场景（事实核查、技术判断）
- **cronjob**: 自然语言定义定时任务. "每天早上9点帮我看GitHub通知" → tạo scheduled job

### Toolset机制

40+工具全开会overwhelming và gây chậm. Toolset chia theo chức năng, config.yaml按需启用:

```yaml
toolsets:
  - web          # 网页搜索
  - terminal     # 终端命令
  - file         # 文件操作
  - skills       # Skill管理
  - delegation   # 子Agent委派
  # - homeassistant  # 不需要就注释掉
```

Benefits: Agent注意力更集中，响应更快，token消耗更少. 也是安全边界.

### MCP (Model Context Protocol)

MCP = AI工具世界的USB接口. Hermes支持stdio和HTTP两种方式连接MCP Server.

配置示例:
```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxx"
```

6000+ ứng dụng: GitHub, Slack, Jira, Google Drive, database...

per-server工具过滤:
```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    allowed_tools:
      - "list_issues"
      - "create_issue"
      - "get_pull_request"
```

### 子Agent委派 (delegate_task)

| 特性 | 说明 |
|------|------|
| 独立上下文 | 每个子Agent有自己对话历史，互不干扰 |
| 受限工具集 | 可以指定子Agent能用哪些工具 |
| 最多3个并发 | 硬编码限制，防止资源耗尽 |
| 结果回传 | 子Agent完成后，结果返回主Agent汇总 |

### 三重约束层

1. **Toolset控制**: config.yaml里启用的才能调用
2. **code_execution沙箱**: 隔离环境运行
3. **子Agent受限工具集**: 负责搜索的子Agent不需要terminal权限

---

## §07-11 — Installation & Setup

### Ba cách cài đặt

**方式一：本地安装（5分钟）**
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes  # start chatting
```

**方式二：Docker**
```bash
docker pull nousresearch/hermes-agent:latest
docker run -v ~/.hermes:/opt/data nousresearch/hermes-agent:latest
```

**方式三：$5 VPS 24/7**
- Recommended: Hetzner CX22 ~$4/月, DigitalOcean $5/月, Vultr $5/月
- Ubuntu 22.04 LTS, memory <500MB nếu không chạy local LLM

### Config.yaml最小配置

```yaml
model:
  provider: openrouter
  api_key: sk-or-xxxxx
  model: anthropic/claude-sonnet-4
terminal: local
gateway:
  telegram:
    token: YOUR_BOT_TOKEN
```

### Model Providers

| Provider | 推荐模型 | 适用场景 |
|----------|---------|----------|
| OpenRouter | Claude Sonnet 4 / GPT-4o | 200+模型可选 |
| Nous Portal | Hermes 3系列 | 官方推荐 |
| Ollama | Hermes 3 8B/70B | 完全离线，隐私优先 |

> ⚠️ **Lưu ý**: 2026年4月起，Anthropic封禁第三方工具通过Claude订阅访问Claude。建議优先OpenRouter或Nous Portal。

### 第一对话会发生什么

1. Bạn nói chuyện → Hermes lưu vào SQLite + FTS5 index
2. Bạn nói preferences → Hermes写入持久记忆层
3. Bạn làm task phức tạp → Hermes自动创建Skill

```
~/.hermes/
├── config.yaml
├── state.db (对话历史 + FTS5索引)
├── skills/
│   └── bundled/
└── memories/
```

### Telegram Bot Setup (3 bước)

1. Tìm @BotFather, gửi `/newbot` → lấy Token
2. Thêm vào config.yaml:
```yaml
gateway:
  telegram:
    token: 123456789:ABCdefGhIJKlmNoPQRsTUVwxyz
```
3. `hermes` → Bot tự kết nối

### MCP Setup

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxx"
```

---

## §12-15 — Real-World Scenarios

### 个人知识助手

**关键价值**: 跨会话记忆. 三周调研项目， traditional AI每次都要重新铺垫背景. Hermes记住之前排除的方案、已确认的信息.

三层记忆各司其职:
```
会话记忆 → 细节按需检索
持久记忆 → 背景自动加载
Skill记忆 → 方法论复用
```

### 开发自动化

**Claude Code写代码 → Hermes看守流水线**

```
Claude Code 写代码提PR
→ Hermes 自动审查PR
→ Hermes 跑测试验证
→ Hermes 生成日报汇总
```

自动代码审查: cron调度 + GitHub MCP + 记忆系统. 你睡觉时它也在干活.

**区别**:
- Claude Code是工匠: 写代码、重构、调试
- Hermes是管家: 巡检、监控、汇总、调度

### 内容创作

**系列选题 vs 单篇文章**

单篇商单 → Claude Code (交互快)
系列选题 → Hermes (Skill tự积累风格，慢慢长出来)

**子Agent并行调研**:
```
主Agent定义任务模板
→ 子Agent A调研Claude Code
→ 子Agent B调研Cursor  
→ 子Agent C调研Hermes
→ 主Agent汇总
```

原来40分钟的调研 → 15分钟搞定.

**Skill积累写作风格**:
- 一开始: 几条简单规则（别用"综上所述"、段落3-5行）
- 每次审校: Hermes观察并学习
- 一个月后: 几十条规则，全部来自真实反馈
- 变成专属编辑手册，而且自动维护

### 多Agent编排

**delegate_task详解**:

| 特性 | 说明 |
|------|------|
| 独立上下文 | 子Agent有自己对话历史，不污染主Agent |
| 受限工具集 | 调研Agent只给web+browser，编码Agent只给terminal+file |
| 最多3个并发 | 超过3个，主Agent汇总质量急剧下降 |
| 结果回传 | 主Agent做汇总 |

**Anthropic三Agent架构 vs Hermes delegate_task**:

| | Anthropic三Agent | Hermes delegate_task |
|--|-----------------|---------------------|
| 角色划分 | 固定 (规划/执行/评估) | 任务驱动，角色灵活 |
| 通信方式 | 链式传递 | 星形结构 |
| 并行性 | 通常串行 | 最多3个并发 |
| 记忆 | 无内置记忆 | 主Agent保持完整记忆 |

> **经验法则**: 只有在上下文不够用 hoặc 需要并行加速时才用 delegate_task. 不然拆分反而增加通信开销.

---

## §16 — Hermes vs OpenClaw vs Claude Code

### 三个物种

| | Claude Code | OpenClaw | Hermes Agent |
|--|-------------|----------|--------------|
| 核心理念 | 交互式编码 | 配置即行为 | 自主后台+自改进 |
| 你的角色 | 坐在终端前指挥 | 写配置文件定义行为 | 部署后偶尔检查 |
| 记忆机制 | CLAUDE.md + auto-memory | 多层记忆，透明可控 | 三层自改进记忆 |
| Skill来源 | 手动安装 | ClawHub 44000+ | Agent自创+社区Hub |
| 运行模式 | 按需启动 | 按需启动 | 24/7后台运行 |
| 部署方式 | 本地CLI（订阅制） | 本地CLI（免费+API费） | $5 VPS/Docker/Serverless |

### 什么场景用哪个

| 场景 | 推荐工具 |
|------|----------|
| 写新功能、重构代码 | Claude Code |
| 给团队搭标准化Agent | OpenClaw |
| 7x24代码审查 | Hermes |
| 个人知识助手 | Hermes |
| 搭建客服/社区Bot | Hermes |
| 快速验证产品想法 | Claude Code |
| 需要高度可控企业场景 | OpenClaw |
| 长期内容创作项目 | Hermes + Claude Code |

### agentskills.io的意义

Skill不再是某个Agent的专属资产. 你在Claude Code积累的Skill，Hermes直接用. 选Agent时不用担心迁移成本.

---

## §17 — 自改进Agent的边界：它能走多远

### Self-Improvement的约束

从技术层面, Hermes的Skill自改进有几个约束:
- Skill文件是可读markdown，不是黑箱
- 记忆数据在本地SQLite，可以查看和删除
- 工具权限有沙箱，Agent不能随意获取新权限

**但问题是**: 你真的会每天去看Agent改了哪些Skill吗？大多数人部署Hermes是因为「不用管它」。这个矛盾是根本性的: 自主Agent的价值在于你不用盯着，但安全需要你盯着。

### 开源 vs 闭源

- **Claude Code (闭源)**: 你不知道内部逻辑. 但Anthropic有商业激励让Agent行为可预测 (出了事会丢用户)
- **Hermes (开源)**: 你可以看到所有代码. 但MIT的另一面是: 后果自负

两种信任的形状:
- "我信任你的商业动机" (闭源)
- "我信任自己的审计能力" (开源)

### Self-Improvement的天花板

**不在技术，在反馈信号**.

Hermes的自改进循环依赖: 它能判断自己的改进是好是坏. 但「更好」是**谁定义**的?

- 你在场给反馈 → loop有效. 你说"不对"，它调整.
- 你不在场 → Agent只能用自己的评估标准. 它觉得"快"和"准"，但不等于"对".

> **花叔的判断**: 让Agent在「怎么做」上自改进，你只管「做什么」和「别做什么」。这是另一种on the loop.

### 值得持续思考的问题

1. 你愿意让Agent自主改进到什么程度？
2. 谁来审计自改进的结果？
3. 自改进Agent需要「遗忘」机制吗？（记忆只增不减 vs 过时经验需要被忘掉）
4. 如果Agent自己设计自己的缰绳，将来谁来判断缰绳设计得对不对？

---

## Các tính năng đã dùng trên máy này

### Đã có sẵn
- **Hermes v0.8.0** chạy tại `~/.hermes/hermes-agent`
- **92+ skills** trong `~/.hermes/skills/`
- **Apple skills plugin** đã cài (swiftui, uikit, healthkit, v.v.)
- **Telegram gateway** active (chat_id: 1132914873)
- **三层记忆**: SQLite FTS5, Honcho (chưa enable)
- **delegate_task**: Có thể spawn subagents

### Chưa dùng / có thể kích hoạt
- **Skill自改进**: Vẫn đang manual, chưa observe thấy tự động create
- **Honcho用户建模**: Có trong config nhưng chưa setup
- **Trajectory saving**: Có thể enable để train data
- **MCP servers**: Có thể thêm GitHub, database, v.v.
- **hermes-dojo self-improvement**: Chưa explore
- **hermes-skill-factory**: Chưa thử

---

## Liên kết

- [Official Docs](https://hermes-agent.nousresearch.com/docs/)
- [GitHub](https://github.com/NousResearch/hermes-agent)
- [Awesome Hermes Agent](https://github.com/0xNyk/awesome-hermes-agent)
- [Orange Book PDF](https://github.com/alchaincyf/hermes-agent-orange-book/raw/main/Hermes-Agent-从入门到精通-v260407.pdf)
- [huasheng.ai/orange-books](https://www.huasheng.ai/orange-books)