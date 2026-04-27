---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 local-llm (extracted)
  - 🔗 apple-silicon-llm-optimization (extracted)
  - 🔗 automation (extracted)
relationship_count: 3
---

# MLX Wiki Agent Setup

## Overview

The MLX Wiki Agent is a Python script that:
1. Monitors the `raw/` folder for new content
2. Uses a local LLM (MLX) to read and analyze content
3. Automatically generates wiki concept pages

## Prerequisites

- Mac with Apple Silicon (M1/M2/M3/M4)
- Python 3.8+
- ~5GB free disk space for models

## Installation

### Step 1: Install MLX

```bash
pip install mlx mlx-lm
```

### Step 2: Download a Model

**Recommended models (in order of preference):**

| Model | Size | Memory | Best For |
|-------|------|--------|----------|
| `mlx-community/SmolLM2-360M-Instruct` | 360M | ~1GB | Fast, good quality |
| `mlx-community/Qwen2.5-0.5B-Instruct` | 500M | ~2GB | Better reasoning |
| `mlx-community/Qwen2.5-1.5B-Instruct` | 1.5B | ~4GB | Best quality |

**Download a model:**

```bash
# Option 1: Download via mlx_lm
mlx_lm.download --model mlx-community/SmolLM2-360M-Instruct

# Option 2: Or use Hugging Face CLI
pip install huggingface_hub
huggingface-cli download mlx-community/SmolLM2-360M-Instruct
```

### Step 3: Verify Installation

```bash
# Test inference
mlx_lm.generate --model mlx-community/SmolLM2-360M-Instruct --prompt "Hello, how are you?"
```

## Usage

### Run the Agent

```bash
cd ~/wiki
python3 scripts/mlx-wiki-agent/agent.py
```

### Run with Specific Model

```bash
python3 scripts/mlx-wiki-agent/agent.py --model mlx-community/Qwen2.5-0.5B-Instruct
```

### Process Only New Files

```bash
python3 scripts/mlx-wiki-agent/agent.py --watch
```

### Dry Run (Don't Write Files)

```bash
python3 scripts/mlx-wiki-agent/agent.py --dry-run
```

## Cron Job Setup

### Option 1: Simple Cron (Every Hour)

```bash
crontab -e

# Add this line:
0 * * * * cd ~/wiki && /usr/bin/python3 scripts/mlx-wiki-agent/agent.py >> logs/agent.log 2>&1
```

### Option 2: Watch Mode (Real-time)

```bash
# Run continuously in background
nohup python3 scripts/mlx-wiki-agent/agent.py --watch > logs/agent.log 2>&1 &

# Check if running
ps aux | grep agent.py

# Stop
pkill -f agent.py
```

### Option 3: LaunchAgent (Mac Native)

```bash
# Create plist
cat > ~/Library/LaunchAgents/com.anhtuan.wiki-agent.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.anhtuan.wiki-agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/tuananh4865/wiki/scripts/mlx-wiki-agent/agent.py</string>
        <string>--watch</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/tuananh4865/wiki/logs/agent.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/tuananh4865/wiki/logs/agent.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/tuananh4865/wiki</string>
</dict>
</plist>
EOF

# Load the agent
launchctl load ~/Library/LaunchAgents/com.anhtuan.wiki-agent.plist

# Check status
launchctl list | grep wiki-agent

# Stop
launchctl unload ~/Library/LaunchAgents/com.anhtuan.wiki-agent.plist
```

## Configuration

Edit `config.yaml` in the script directory:

```yaml
model: mlx-community/SmolLM2-360M-Instruct
watch_mode: false
auto_commit: true
max_tokens: 2048
temperature: 0.7
```

## Troubleshooting

### "Module not found: mlx"
```bash
pip install mlx mlx-lm
```

### "Model not found"
```bash
mlx_lm.download --model mlx-community/SmolLM2-360M-Instruct
```

### Out of memory
- Use a smaller model (SmolLM2 360M)
- Close other apps
- Reduce batch size

### Slow inference
- Use SmolLM2 360M for speed
- Use Qwen2.5 1.5B for quality (slower)

## Logs

Check `~/wiki/logs/agent.log` for:
- Files processed
- Errors encountered
- Generated content previews

## Related Concepts

- [[local-llm]] — Local LLM inference setup
- [[apple-silicon-llm-optimization]] — Apple Silicon ML optimization
- [[automation]] — Automation scripts for wiki maintenance
