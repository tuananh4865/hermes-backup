---
title: "Your Harness, Your Memory"
date: 2026-04-11
type: article
source: https://blog.langchain.dev/your-harness-your-memory/
author: Harrison Chase
---

# Your Harness, Your Memory

Agent harnesses are becoming the dominant way to build agents, and they are not going anywhere. These harnesses are intimately tied to agent memory. If you used a closed harness - especially if it's behind a proprietary API - you are choosing to yield control of your agent's memory to a third party. Memory is incredibly important to creating good and sticky agentic experiences. This creates incredible lock in. Memory - and therefor harnesses - should be open, so that you own your own memory.

When things like web search are built into OpenAI and Anthropic's APIs - they are not "part of the model". Rather, they are part of a lightweight harness that sits behind their APIs and orchestrates the model with those web search APIs (via nothing other than tool calling).

There is sometimes sentiment that memory is a standalone service, separate from any particular harness. At this point in time, that is not true.

A large responsibility of the harness is to interact with context. As Sarah puts it:

Memory is just a form of context. Short term memory (messages in the conversation, large tool call results) are handled by the harness. Long term memory (cross session memory) needs to be updated and read by the harness. Sarah lists out many other ways the harness is tied to memory:

Right now, memory as a concept is in it's infancy. It's so early for memory. Transparently, we see that long term memory is often not part of the MVP. First you need to get an agent working generally, then you can worry about personalization. This means that we (as an industry) are still figuring out memory. This means there are not well known or common abstractions for memory. If memory does become more known, and as we discover best practices, it is possible that separate memory systems start to make sense. But not at this point in time. Right now, as Sarah said, "ultimately, how the harness manages context and state in general is the foundation for agent memory."

The harness is intimately tied to memory.

This manifests itself in several ways.

**Mildly bad**: If you use a stateful API (like OpenAI's Responses API, or Anthropic's server side compaction), you are storing state on their server. If you want to swap models and resume previous threads - that is no longer doable.

**Bad**: If you use a closed harness (like Claude Agent SDK, which uses Claude Code under the hood, which is not open source), this harness interacts with memory in a way that is unknown to you. Maybe it creates some artifacts client side - but what is the shape of those, and how should a harness use those? That is unknown, and therefor non-transferrable from one harness to another.

In this situation, you have zero ownership or visibility into memory, including long term memory. You do not know the harness (which means you don't know how to use the memory). But even worse - you don't even own the memory! Maybe some parts are exposed via API, maybe no parts are - you have no control over that.

When people say that the "models will absorb more and more of the harness" - this is what they really mean. They mean that these memory related parts will go behind the APIs that model providers offer.

Even if the whole harness isn't behind the API, model providers are incentivized to move more and more behind APIs - and are already doing so. For example: even though Codex is an open source, it generates an encrypted compaction summary (that is not usable outside of the OpenAI ecosystem).

**Why are they doing this?** Because memory is important, and it creates lock in that they don't get from just the model.

Although memory is early, it is clear to everyone that it is important. It is what allows agents to get better as users interact with them, and allows you build up a data flywheel. It is what allows your agent to be personalized to each of your users, and build up an agentic experience that molds to their desires and usage patterns.

With memory, you build up a proprietary dataset - a dataset of user interactions and preferences. This proprietary dataset allows you to provide a differentiated and increasingly intelligent experience.

It's been relatively easy to switch model providers to date. They have similar, if not identical, APIs. Sure, you have to change prompts a little bit, but that's not that hard.

But this is all because they are stateless.

As soon as there is any state associated, its much harder to switch. Because this memory matters. And if you switch, you lose access to it.

**A story**: I have an email assistant internally. It's built on top of a template in Fleet, our no-code platform for building Enterprise ready OpenClaws. This platform has memory built in, so as I interacted with my email assistant over the past few months it built up memory. A few weeks ago, my agent got deleted by accident. I was pissed! I tried to create an agent from the same template - but the experience was so much worse. I had to reteach it all my preferences, my tone, everything.

The plus side of my email agent deleted - it made me realize how powerful and sticky memory could be.

Memory needs to be opened, owned by whomever is developing the agentic experience. It allows you to build up a proprietary dataset that you actually control.

Memory (and therefor harnesses) should be separate from model providers. You should want optionality to try out whatever models are best for your use case. Model providers are incentivized to create lock in via memory.
