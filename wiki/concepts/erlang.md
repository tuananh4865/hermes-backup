---
title: "Erlang"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [programming-languages, concurrency, functional-programming, fault-tolerance, distributed-systems]
---

# Erlang

## Overview

Erlang is a functional programming language and runtime system designed by Joe Armstrong, Robert Virding, and Mike Williams at Ericsson in the late 1980s. Originally created to develop software for telephone switches, Erlang excels at building distributed, fault-tolerant, real-time systems that must run continuously for years without failure. The language's core philosophy centers on concurrency, isolation, and graceful error recovery.

Erlang's defining characteristic is its lightweight process model. Creating thousands or even millions of concurrent processes is normal and inexpensive because Erlang processes share no memory—communication happens exclusively through message passing. This model makes it trivial to distribute computation across multiple machines, scale horizontally, and recover from failures without stopping the system.

The BEAM (Bogdan/Björn's Erlang Abstract Machine) is the virtual machine that runs Erlang and Elixir code. BEAM provides pre-emptive scheduling, garbage collection per process (avoiding stop-the-world pauses), and built-in support for distribution, hot code loading, and fault recovery. Erlang/OTP (Open Telecom Platform) extends the language with a collection of libraries and design patterns for building robust applications.

## Key Concepts

**Processes**: Erlang's fundamental unit of execution. Unlike operating system threads, Erlang processes are extremely lightweight (starting at about 300 words of memory) and are scheduled cooperatively by the BEAM. Each process has its own mailbox for receiving messages and maintains isolated state.

**Message Passing**: The only way processes communicate. A process sends a message (any Erlang term) to another process's mailbox using the `!` operator. The receiving process retrieves messages using `receive`, which can pattern-match on message contents.

**OTP Behaviors**: Design patterns implemented as Erlang/OTP libraries. The most important behaviors include:
- `gen_server`: For implementing client-server relationships
- `gen_fsm`: For finite state machines
- `gen_event`: For event handling
- `supervisor`: For fault-tolerant supervision trees

**Supervision Trees**: A fault tolerance pattern where processes are organized in a tree structure. When a child process fails, its supervisor can restart it according to configured strategies (one_for_one, rest_for_one, one_for_all). This "let it crash" philosophy avoids defensive programming.

**Hot Code Loading**: Erlang's ability to update code in a running system without stopping. A module can have two versions loaded simultaneously; new processes use the new code while existing processes continue with the old until they explicitly switch.

## How It Works

Erlang programs are structured as collections of modules, each containing functions. The entry point is typically a module that starts the supervision tree. When the system boots, the OTP application controller starts the top-level supervisor, which recursively starts child workers and supervisors according to the application specification.

```erlang
%% Example: A simple gen_server
-module(counter).
-behavior(gen_server).

-export([start_link/0, increment/0, get/0]).
-export([init/1, handle_call/3, handle_cast/2, terminate/2]).

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

increment() ->
    gen_server:cast(?MODULE, increment).

get() ->
    gen_server:call(?MODULE, get).

%% Callbacks
init(_Args) ->
    {ok, 0}.

handle_cast(increment, State) ->
    {noreply, State + 1}.

handle_call(get, _From, State) ->
    {reply, State, State}.

terminate(_Reason, _State) ->
    ok.
```

The BEAM's pre-emptive scheduler distributes execution time across processes. When a process makes a blocking call (like receiving from an empty mailbox), the scheduler transparently switches to another runnable process. This cooperative nature, combined with the reduction counting that prevents any single process from monopolizing CPU time, provides concurrency without the complexity of locks or mutexes.

## Practical Applications

**Telecom Infrastructure**: Erlang was designed for telephone switches and remains dominant in telecom. Ericsson, Nokia, and Nortel have used Erlang for protocol stacks, authentication servers, and billing systems.

**Messaging Systems**: WhatsApp famously used Erlang to support 900 million users with a small engineering team. The language's distribution and fault tolerance are ideal for message routing infrastructure.

**Financial Trading**: Low-latency trading systems benefit from Erlang's predictable performance and built-in distribution. The language handles massive message volumes without GC pauses.

**IoT Gateways**: Erlang's ability to manage thousands of concurrent connections makes it suitable for IoT platforms that must maintain connections to many devices simultaneously.

**Web Frameworks**: Cowboy (HTTP server) and RabbitMQ (message broker) are Erlang-based projects powering countless web applications.

## Examples

Building a supervised worker pool:

```erlang
%% Supervisor specification for a worker pool
-module(worker_pool_sup).
-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init(_Args) ->
    Children = [
        #{id => worker1,
          start => {worker, start_link, []},
          restart => permanent,
          shutdown => 5000,
          type => worker,
          modules => [worker]},
        #{id => worker2,
          start => {worker, start_link, []},
          restart => permanent,
          shutdown => 5000,
          type => worker,
          modules => [worker]}
    ],
    {ok, {#{strategy => one_for_one, intensity => 5, period => 60}, Children}}.
```

## Related Concepts

- [[Elixir]] - A Ruby-inspired language running on the BEAM
- [[BEAM]] - The Erlang virtual machine
- [[OTP]] - The framework built on top of Erlang
- [[Actor Model]] - Similar message-passing concurrency model
- [[Functional Programming]] - The paradigm Erlang follows
- [[Distributed Systems]] - Erlang's natural domain

## Further Reading

- "Programming Erlang: Software for a Concurrent World" by Joe Armstrong - The definitive Erlang book
- "Learn You Some Erlang for Great Good!" by Fred Hébert - Accessible online tutorial
- "Erlang and OTP in Action" by Martin Logan and Eric Merritt - Practical OTP patterns
- Joe Armstrong's PhD Thesis - "Making reliable distributed systems in the presence of software errors"

## Personal Notes

Erlang's "let it crash" philosophy was revolutionary when introduced and remains counterintuitive to developers trained in defensive programming. The idea is that instead of writing defensive code everywhere to handle every possible error, you write the happy path and let supervisors handle failures. This dramatically simplifies code and makes error handling consistent.

The isolation between processes also eliminates entire categories of bugs. No mutex can be held forever because processes can't forcibly acquire locks. No deadlocks from lock ordering because there's no locking. No data corruption from concurrent writes because there's no shared mutable state. These properties don't make Erlang immune to bugs, but they eliminate an entire class of concurrency bugs that plague other languages.
