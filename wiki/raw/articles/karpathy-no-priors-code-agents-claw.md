---
title: "Andre Karpathy - Code Agents, CLAW, Home Automation Agent"
created: 2026-04-13
source: https://youtu.be/kwSVtQ7dziU
type: raw-article
confidence: high
---

# Source

**Creator**: No Priors Podcast
**URL**: https://youtu.be/kwSVtQ7dziU
**Duration**: ~65 min
**Guest**: Andre Karpathy

---

# Transcript (Full)

[Full 65-min transcript saved. Key segments extracted below.]

---

# Key Segments

## On Code Agents ("Claw" / "Manifest")

```
0:11 I have to express my will to my agents for 16 hours a day. Manifest.
0:45 I kind of went from 80/20 to 20/80 of writing code by myself versus just delegating to agents.
1:58 I don't think I've typed like a line of code probably since December basically.
3:15 They just whisper to their agents all the time. It's the strangest work setting ever.
5:22 If you don't feel bounded by your ability to spend on tokens, then you are the bottleneck in the system that is max capability.
6:38 You're not maximizing your subscription. If you run out of the kod on codecs, you should switch to cloud.
```

## On Peter Steinberg's Setup

```
4:02 Peter is famous. He has a photo where he's in front of a monitor with lots of codecs agents working.
4:14 They all take about 20 minutes if you prompt them correctly.
4:18 He's just going between them and giving them work.
4:24 It's not just here's a line of code. It's here's a new functionality and delegate it to agent one.
```

## On Agent Memory

```
7:39 CLAW has more sophisticated memory than what you get by default which is just memory compaction when your context runs out.
```

## On Agent Personality

```
8:09 I actually think CLAW has a pretty good personality. It feels like a teammate.
8:16 For example, Codex is a lot more dry.
8:34 It doesn't understand what we're building.
8:42 When Claude gives me praise I do feel like I slightly deserve it.
8:59 I'm trying to earn its praise which is really weird.
```

## Dobby - Home Automation Agent

```
9:27 I built a claw I call Dobby the elf claw that takes care of my home.
9:41 I used agents to find all of the smart home subsystems on my local area network.
9:48 It did IP scan and found Sonos, reverse engineered how it works.
10:14 I asked: "Can you find my Sonos?" And music came out. I can't believe I just typed that.
10:27 Created APIs, created a dashboard for all my lights.
10:39 Dobby at sleepy time = all lights go off.
10:43 It controls all my lights, HVAC, shades, pool, spa, security system.
10:49 Camera pointed outside. When someone rolls in, Quinn model looks at videos.
11:03 It sends me a WhatsApp with image: "Hey, a FedEx truck just pulled up."
11:45 I don't have to use six different apps anymore. Dobby controls everything in natural language.
```

## On Software Consolidation

```
12:50 The unification across six different software systems speaks to: do people really want all the software today?
13:09 These apps in the app store for smart home devices - shouldn't they just be APIs?
13:17 Agents should just use them directly.
13:29 An LLM can drive the tools and call all the right tools.
13:38 There might be an overproduction of lots of custom bespoke apps that shouldn't exist.
13:43 Agents crumble them up. Everything should be exposed API endpoints.
13:51 Agents are the glue of the intelligence.
```

## On Open Source vs Frontier Labs

```
49:39 The closed models are ahead but open source is behind by like 6-8 months now.
49:50 In operating systems you have Windows and Mac OS but there's Linux that runs 60% of computers.
50:10 The industry has always felt demand for an open platform.
50:23 Big difference: everything is capex. Capital makes it harder to compete.
50:34 For vast majority of consumer use cases, open source models are actually quite good.
50:54 There's always going to be demand for frontier intelligence - Nobel Prize kind of work.
51:07 I kind of expect frontier labs to have closed AIs that are oracles, and open source behind by months.
51:36 I want there to be a thing that's behind and is a common working space for intelligences.
52:04 Centralization has a very poor track record.
```

## On Robotics

```
54:42 Self-driving is the first robotics application. Most startups didn't make it long-term.
55:03 Robotics because it's so difficult and requires huge amount of capital investment.
55:21 Digital space is going to change a huge amount, then physical space will lag behind.
55:41 Interface between digital and physical - sensors and actuators.
55:53 Eventually you run out of things to do purely in digital space. You have to go to the universe.
56:39 There's going to be huge amount of unbottling. Then it moves to interfaces.
57:14 The atoms are just a million times harder. It will lag behind but it's also a bigger market.
```

## On Education

```
1:03:30 I don't feel like I'm explaining things directly to people anymore. I'm explaining it to agents.
1:03:46 Skill is just a way to instruct the agent how to teach the thing.
1:04:13 If agents get it, they can be the router and target it to the human in their language with infinite patience.
1:04:45 Instead of HTML documents for humans, have markdown documents for agents.
1:04:57 The things that agents can't do is your job now.
1:05:01 The things that agents can do, they can probably do better than you or very soon.
1:05:07 You should be strategic about what you're actually spending time on.
```

## On microGPT

```
1:01:37 I've been simplifying LLMs to their bare essence.
1:02:15 Training neural nets is 200 lines of Python. Very simple to read.
1:02:50 I tried to get an agent to write microGPT. It can't do it. But it totally gets it.
1:05:30 My value add is the few bits of curriculum. The education after that is not my domain anymore.
```

---

# Key Insights

## 1. The New Engineering Workflow

- **December flip**: Went from 80/20 (human/agent) to 20/80
- **16 hours/day**: Expressing will to agents, not typing code
- **Token throughput**: You're the bottleneck if you don't max your subscription
- **Multi-agent**: One agent does research, one writes code, one comes up with plans

## 2. CLAW (Computer Launched Agentic Worker)

- Persistent agent that loops on its own
- Sophisticated memory system (beyond context compaction)
- Has personality - feels like a teammate
- Peter Steinberg pioneered this with Codex

## 3. Home Automation Agent (Dobby)

- Natural language control of entire home
- Replaces 6 different apps
- WhatsApp interface
- Security camera + AI detection
- Proactive notifications

## 4. Software unbundling/rebundling

- Apps shouldn't exist - should be APIs
- Agents are the new UX layer
- "Agents crumble up" bespoke apps

## 5. Open Source Balance

- Frontier labs = closed oracles
- Open source = 6-8 months behind
- Linux analogy: 60% of computers
- Healthy power balance for industry

## 6. Education Paradigm Shift

- Explain to agents, not humans
- Agents route to humans with infinite patience
- Markdown for agents > HTML for humans
- Focus on what agents can't do
