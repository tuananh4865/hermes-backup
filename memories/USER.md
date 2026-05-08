§ [PREFERENCES] — explicit preferences discovered over sessions
- communication: Vietnamese casual
- response_style: concise, no fluff
- tiktok_script_style: "anh" + "mấy con vợ"
§ [PROJECTS] — ongoing work
- tiktok-content: active
- hermes-agent: memory-optimizing
§ [FACTS] — durable facts about user, environment, tools
- communication: Vietnamese casual
- response_style: concise, no fluff
- tiktok_script_style: "anh" + "mấy con vợ"
- tiktok-content: active
- hermes-agent: memory-optimizing
Tuấn Anh: Frustrated by marketing vs reality gap on "self-improving memory". Expected agent to autonomously remember work-in-progress. Wants complete session continuity + auto memory extraction without manual prompts.
Tuấn Anh login X (Twitter) là @TyayUno (Anh Trinh) — thấy qua browser-harness lúc switch sang tab X
Felix Model agentic company: Anh = Strategic Owner, Hermes = Orchestrator. Workers: Content-Creator + Research-Analyst. Workers need SOUL.md + HEARTBEAT.md + CRON to be truly autonomous. Cron worker IDs: ce3701b4dcdd, 50bc2c2dfbb3, e4fb0c36e9f7, 1c425ba42980. "Configured" ≠ "Running".
ByteRover preference: 100% local with LM Studio, NO cloud account needed. Initially incorrectly told him ByteRover "requires cloud account" — he caught this by reading docs himself. Must verify claims more carefully before stating as fact.
ByteRover setup (verified working 2026-05-06):
- Provider: openai-compatible (LM Studio localhost:1234)
- Models tested: gemma-4-e2b ✅ (~76s curate/query), gemma-4-e4b ✅, qwen3.6-35b ❌ timeout
- Command: brv providers connect openai-compatible --base-url http://localhost:1234/v1 --model google/gemma-4-e2b --api-key "no-key"
- No MiniMax API key needed when using local model
- LM Studio server: localhost:1234 (Mac Mini at 192.168.0.187 is down, using local LM Studio instead)
- [project] tiktok-content
- [model] gemma
- [preference] phải bốc trúng đâu, đây là toang rồi [HIGH]
- 2026-05-07: Testing memory phases
§ [SESSIONS] — session history summaries
- 2026-05-08: Anh ơi test memory hooks
§ [ENTITY_INDEX] — cross-session entity tracking
§ [GROWTH_LOG] — how user/agent improved
