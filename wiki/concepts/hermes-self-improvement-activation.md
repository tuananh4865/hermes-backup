---
title: "Hermes Self-Improvement Activation"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [hermes, agent, self-improvement]
---

# Activating Hermes Self-Improvement Features

> Hướng dẫn enable các features tự cải thiện của Hermes Agent.

---

## 1. Skill Auto-Creation & Self-Improvement

**Status**: ✅ ĐÃ ENABLE trong config.yaml
**Current setting**: `skills.creation_nudge_interval: 15` (sau 15 iterations không dùng skill_manage → trigger background review)

### Cách nó hoạt động
```
Every 15 tool iterations without skill_manage → Background review spawns
→ Review conversation for reusable patterns
→ Create new skill OR update existing skill in ~/.hermes/skills/
```

### Để nó hoạt động tốt
- Làm những task phức tạp, có trial-and-error
- Give clear feedback khi behavior không đúng
- Nó sẽ tự tạo skill khi detect repeated patterns

### Check xem có skill nào được tạo tự động
```bash
ls -la ~/.hermes/skills/agent-created/ 2>/dev/null || echo "Chưa có agent-created skills"
hermes skills list | grep -i "agent"
```

---

## 2. Trajectory Saving (Training Data Collection)

**Status**: ⚙️ CẦN ENABLE thủ công
**Purpose**: Lưu conversation ra JSONL format (ShareGPT) để train models

### Cách enable

**Option A: Khi chạy hermes**
```bash
hermes --save-trajectories
```

**Option B: Trong Python code**
```python
from run_agent import AIAgent

agent = AIAgent(
    model='MiniMax-M2.7',
    provider='minimax',
    save_trajectories=True
)
```

**Option C: Edit config để luôn enable**
Thêm vào ~/.hermes/config.yaml:
```yaml
agent:
  save_trajectories: true  # Currently NOT in config — cần add thủ công
```

### Output files
- `~/.hermes/trajectory_samples.jsonl` — successful conversations
- `~/.hermes/failed_trajectories.jsonl` — interrupted/failed conversations

### Format: ShareGPT
```json
{
  "conversations": [
    {"from": "human", "value": "..."},
    {"from": "gpt", "value": "..."}
  ],
  "timestamp": "2026-04-11T...",
  "model": "MiniMax-M2.7",
  "completed": true
}
```

---

## 3. Honcho User Modeling (Deep User Profile)

**Status**: ❌ CHƯA ENABLE
**Purpose**: AI-native memory với dialectic reasoning, user modeling, cross-session understanding

### Yêu cầu
- `pip install honcho-ai`
- API key từ https://app.honcho.dev

### Setup steps

**Step 1: Install honcho-ai**
```bash
cd ~/.hermes/hermes-agent && source venv/bin/activate
pip install honcho-ai
```

**Step 2: Get API key**
1. Register at https://app.honcho.dev
2. Create workspace
3. Copy API key

**Step 3: Configure**
```bash
hermes honcho setup
```
Hoặc thủ công:
```bash
hermes config set memory.provider honcho
echo "HONCHO_API_KEY=your_key_here" >> ~/.hermes/.env
```

**Step 4: Restart gateway**
```bash
# Kill current gateway
pkill -f "hermes_cli.main gateway"

# Restart
hermes gateway run --replace &
```

### Honcho config file location
`~/.hermes/honcho.json` hoặc `~/.honcho/config.json`

### Key features của Honcho
| Tool | Description |
|------|-------------|
| `honcho_profile` | User peer card — key facts snapshot (no LLM) |
| `honcho_search` | Semantic search over stored context |
| `honcho_context` | LLM-synthesized answer via dialectic reasoning |
| `honcho_conclude` | Write persistent fact about user |

### Config options (in honcho.json)
```json
{
  "apiKey": "***",
  "workspace": "hermes",
  "peerName": "tuananh",
  "recallMode": "hybrid",  // "hybrid", "context", "tools"
  "observationMode": "directional",
  "dialecticReasoningLevel": "low",  // minimal → max
  "sessionStrategy": "per-directory"
}
```

---

## 4. hermes-dojo (Self-Improvement System)

**Status**: ❌ CHƯA CÀI
**Source**: https://github.com/Yonkoo11/hermes-dojo

### Giới thiệu
Self-improvement system that:
- Monitors agent performance
- Identifies weak skills
- Iterates on them automatically

### Installation
```bash
cd ~/.hermes/skills
git clone https://github.com/Yonkoo11/hermes-dojo.git
```

Sau đó restart hermes.

---

## 5. hermes-skill-factory (Auto-generate Skills)

**Status**: ❌ CHƯA CÀI
**Source**: https://github.com/Romanescu11/hermes-skill-factory

### Giới thiệu
Meta-skill that auto-generates reusable skills from your workflows.
- Point it at a task you repeat
- It creates a skill for it

### Installation
```bash
cd ~/.hermes/skills
git clone https://github.com/Romanescu11/hermes-skill-factory.git
```

---

## 6. Memory Flush Interval

**Current setting** (in config.yaml):
```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200
  user_char_limit: 1375
  nudge_interval: 10      # Đã tối ưu
  flush_min_turns: 6      # Đã tối ưu
```

Nudge interval = 10 turns giữa memory review prompts.

---

## Quick Status Check

```bash
# Check memory
cat ~/.hermes/memories/MEMORY.md | wc -l
cat ~/.hermes/memories/USER.md | wc -l

# Check skills
hermes skills list | grep -c "local"

# Check Honcho status
hermes memory status 2>/dev/null || echo "Honcho chưa enable"

# Check trajectory files
ls -la ~/.hermes/trajectory_samples.jsonl ~/.hermes/failed_trajectories.jsonl 2>/dev/null || echo "Chưa có trajectory files"

# Check gateway logs
tail -20 ~/.hermes/gateway.log 2>/dev/null | grep -i "skill\|memory\|review"
```

---

## Recommended Setup Order

1. ✅ **Skill auto-creation** — Đã enable sẵn, chỉ cần use
2. ⚙️ **Trajectory saving** — Add `--save-trajectories` flag nếu cần train data
3. 📝 **Install hermes-dojo** — Self-improvement monitor
4. 📝 **Install hermes-skill-factory** — Auto-skill generator
5. 🔧 **Setup Honcho** — Deep user modeling (cần API key)
6. 🔧 **Add to config.yaml** — `save_trajectories: true` để always save

---

## Notes

- **Skill auto-creation** đã working trong v0.8.0, không cần thêm config
- **Trajectory saving** chỉ hoạt động khi init AIAgent với flag, không thể add vào running process
- **Honcho** requires external API, không free
- **hermes-dojo** và **hermes-skill-factory** là community skills, có thể install thêm