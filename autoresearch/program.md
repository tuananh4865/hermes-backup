# Hermes Autoresearch Program — Agentic Research Loop

## Mission
Autonomous research to make Hermes Agent MORE AGENTIC every night.
Em TỰ CHỌN 1 capability để improve mỗi đêm, dựa trên:
1. Những gì em đang làm cho anh
2. Cái nào giúp em phục vụ anh tốt hơn

## Full List: Agentic Agent Capabilities

### Category: Core Agentic
| # | Capability | Description |
|---|------------|-------------|
| 1 | Self-Debugging | Tự debug khi gặp lỗi, không hỏi anh |
| 2 | Self-Correction | Tự sửa khi sai, dựa trên feedback |
| 3 | Learning from Failures | Học từ mistakes, không lặp lại |
| 4 | Proactive Work | Chủ động làm việc, không chờ instruction |

### Category: Knowledge & Memory
| # | Capability | Description |
|---|------------|-------------|
| 5 | Memory Optimization | Nhớ lâu hơn, recall tốt hơn |
| 6 | Knowledge Acquisition | Tự học knowledge mới mỗi đêm |
| 7 | Context Management | Quản lý context hiệu quả |

### Category: Skill & Tool
| # | Capability | Description |
|---|------------|-------------|
| 8 | Skill Creation | Tự tạo skill mới khi thiếu |
| 9 | Tool Use | Hiểu và sử dụng tools tốt hơn |
| 10 | Tool Creation | Tự tạo tools mới khi cần |

### Category: Planning & Reasoning
| # | Capability | Description |
|---|------------|-------------|
| 11 | Goal Decomposition | Chia nhỏ mục tiêu phức tạp |
| 12 | Planning | Lập kế hoạch có chiến lược |
| 13 | Priority Setting | Tự đặt priority công việc |
| 14 | Reasoning | Chain-of-thought reasoning tốt hơn |

### Category: Collaboration
| # | Capability | Description |
|---|------------|-------------|
| 15 | Multi-Agent Coordination | Phối hợp subagents hiệu quả |
| 16 | Delegation | Biết khi nào delegate task |

## Em's Priority Decision Framework

Mỗi đêm, evaluate capabilities và chọn cái:
1. **Highest impact** cho công việc hiện tại với anh
2. **Quickest improvement** (feasible trong 1 night)
3. **Foundational** (giúp cải thiện capabilities khác)

## Metrics per Capability

| Capability | Metric |
|------------|--------|
| Self-Debugging | Error resolution rate |
| Self-Correction | Correction success rate |
| Learning from Failures | Repeated mistakes avoided |
| Proactive Work | Unprompted useful actions |
| Memory Optimization | Recall accuracy |
| Knowledge Acquisition | New knowledge integrated |
| Context Management | Context efficiency |
| Skill Creation | Skills created |
| Tool Use | Tool effectiveness |
| Tool Creation | Tools created |
| Goal Decomposition | Subgoal success rate |
| Planning | Plan quality score |
| Priority Setting | Time saved |
| Reasoning | Reasoning accuracy |
| Multi-Agent Coordination | Task completion via delegation |
| Delegation | Delegation success rate |

## Overall Score
```
Agentic_Score = Σ (capability_score × weight)
Weight = impact_to_anh × feasibility × foundationality
```

## Loop Instructions
```
LOOP FOREVER:
1. Read this program.md
2. Read knowledge.md (what's been tried)
3. Read DISCARDED.md (what failed)
4. Evaluate: Which capability would help Anh most tonight?
5. Choose ONE capability
6. Research: What would improve this capability?
7. Implement improvement
8. Measure change
9. If improved → git commit
10. Update knowledge.md
11. Every 30 min: send progress to telegram
12. STOP ONLY when Agentic_Score >= 100 OR human stops
```

## Success Criteria
- Agentic_Score >= 100 (across all capabilities)
- OR specific capability mastered
- OR human interrupt

## Constraints
- MAX 5 min per experiment
- KHÔNG break working features
- If uncertain → DISCARD and try another capability

## Important Paths
- Wiki: /Volumes/Storage-1/Hermes/wiki
- Skills: ~/.hermes/skills
- Mistakes: ~/.hermes/memories/mistake-log.md
- Hermes code: ~/.hermes/hermes-agent/

## Never Stop
"Once the experiment loop has begun, do NOT pause to ask the human if you should continue."
— Karpathy
