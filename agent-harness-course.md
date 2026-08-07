# Hands-on Course: Build AI Agents and Harness Engineering from Scratch

> A hands-on course for engineers: first write an Agent by hand, then polish it into a reliable runtime (Harness).
> This course is organized around the **Harness 12-Factor** principles, with each chapter corresponding to a production-grade design principle.

---

## Who Is This Course For

- Engineers who know Python and want to truly understand how Agents work
- People who aren't satisfied with "calling LangChain to run a demo" and want to understand the underlying mechanisms and failure modes
- People who want to build Agent infrastructure (orchestration, sandbox, permissions, observability)

**Prerequisites**: Python basics, command line, and an LLM API Key (Anthropic Claude recommended; any compatible API works).
**Not required**: Machine learning background. This course treats the LLM as an "occasionally flaky unreliable node" and builds resilience around it using engineering techniques.

---

## Core Mental Model (Throughout the Course)

> **Don't learn Agent as AI; learn it as an unreliable distributed system.**

The model is just a node in the network that drops packets, delivers out of order, and occasionally returns garbage. All Harness code you write is essentially about building resilience around this unreliable node: retry, timeout, idempotency, state machine, observability, and privilege isolation.

| Engineering Concepts You Already Know | The Harness Equivalent |
|---|---|
| Protocol state machine | Agent loop (think → call → observe → think again) |
| Retry / timeout / idempotency | Tool call failure recovery, avoiding duplicate side effects |
| Packet drop / degradation | Context truncation, fallback for model hallucinations |
| Packet capture / observability | Trace / events (without it you cannot debug the agent) |
| ACL / firewall / sandbox | Permission model, tool allowlist, file access isolation |

---

## Two Key Terms

- **Agent**: A loop that lets the model "do things" — it can call tools, observe results, and make multi-step decisions, rather than just a single Q&A.
- **Harness (Runtime / Scaffolding)**: All the engineering code that wraps a bare LLM API into a reliable Agent — context management, prompt assembly, tool execution, permission sandbox, sub-agent scheduling, error recovery, trace. Claude Code, Cursor, and OpenHands are fundamentally all Harnesses.

This course **builds the Agent first, then upgrades it to a Harness**, giving you firsthand experience of "why agents fail."

---

## Learning Philosophy

1. **Handwrite first, then use frameworks**: Framework abstractions block you from seeing the essence. The first few chapters use zero frameworks.
2. **Deliberately manufacture failures**: All the value of Harness Engineering lies in failure modes. You won't learn anything from reading design docs without having stepped in the mud.
3. **Read source code with questions in mind**: First step in the mud yourself, then read mature Harness code — every design decision will click with an "ah, that's why."
4. **Every chapter has a deliverable**: At the end of each chapter you have something that runs, ready to drop into your GitHub repository.

---

## Course Structure Overview (Harness 12-Factor)

| Factor | Principle | Key Deliverable | Original Module Map |
|---|---|---|---|
| Prerequisite | Environment and first API call | Get the minimal LLM call working | Module 0 |
| F1 | Single Agent Loop | 100-line minimal Agent | Module 1 |
| F2 | Explicit Tool Contract | A robust set of tool interfaces | Module 2 |
| F3 | Context Budgeting | An Agent that won't blow up its context | Module 3 |
| F4 | Failure-First Design | An Agent that can recover from errors | Module 4 (upper) |
| F5 | Graceful Degradation | An Agent that degrades rather than crashes when model/tool fails | Module 4 (lower) |
| F6 | Least-Privilege Tooling | An Agent with confirmation gates for dangerous operations | Module 5 (upper) |
| F7 | Human-in-the-Loop Gates | Irreversible operations require human confirmation, recoverable | Module 5 (lower) |
| F8 | Observable by Default | An Agent that can be fully debugged | Module 6 (upper) |
| F9 | Reproducible Runs | Reproduce a run using a trace | Module 6 (lower) |
| F10 | Composable Agents | Master-sub-agent orchestrator | Module 7 |
| F11 | Config-Driven Behavior | Model/prompt/tool/strategy configuration externalized | New |
| F12 | Continuous Evaluation | A Harness that can be quantitatively evaluated | New |
| Advanced | Reading Real Harnesses | A source-code deep-dive note | Module 8 |
| Wrap-up | A complete domain Agent | Comprehensive application of 12-Factor | Capstone project |

Suggested pace: Prerequisite + F1-F3 in about two weeks, F4-F7 in about three to four weeks (F4-F5 are the most critical — don't rush), F8-F12 + Advanced + Capstone project as interest-driven extensions.

---

# Prerequisite: Environment and First API Call

**Learning Goal**: Set up the environment and understand the minimal structure of an LLM request/response.

**Core Content**
- Install SDK (`anthropic` or equivalent), configure API Key (use environment variables, don't hardcode).
- The three elements of a minimal call: system prompt, messages, model parameters.
- Understand the concept of tokens: both input and output are billed and measured in tokens; this determines everything about context management later.
- Difference between streaming and non-streaming responses.

**Hands-on Exercises**
- Write a `chat.py` that receives a sentence from the command line and prints the model's reply.
- Add a multi-turn conversation loop, manually maintain the `messages` list, and observe how context grows with each turn.

**Deliverable**: A command-line script that can do multi-turn conversation and print the token count consumed per turn.

---

# F1: Single Agent Loop

**Learning Goal**: Implement the core of an Agent by hand — a tool-equipped REPL loop. Understand that "Agent is not magic."

**Core Content**
- The essence of the Agent loop is a state machine: `call model → parse tool call → execute tool → feed result back into context → call model again`, until the model says "done."
- Tool calling protocol: how to tell the model which tools are available (name / description / parameter schema).
- How to parse the model's returned tool_use blocks and dispatch to the corresponding Python function.
- Loop termination condition: the loop ends when the model no longer requests tools.

**Hands-on Exercises**
- Implement the loop in about 100 lines of Python, **without any agent framework**.
- Register the first tool, e.g. `run_command(cmd)` to run `ping` / `traceroute`, or file read, calculator, etc.
- Have the Agent complete a task requiring 2-3 tool calls, and print each step's thought and action.

**Deliverable**: A minimal but complete Agent that can autonomously call tools to complete multi-step tasks.
**Key Takeaway**: An Agent is just a loop that "decides what to call next on its own" — the magic disappears.

---

# F2: Explicit Tool Contract

**Learning Goal**: Tools are the Agent's only interface with the world. Learn to design tools that the model uses correctly and reliably.

**Core Content**
- **Tool description is prompt**: a poorly written description means the model uses the tool wrong.
- Parameter validation: the model may pass wrong types, missing fields, or hallucinated values — tools must validate internally.
- Return value design: what is returned to the model should be information "the model can understand and use to make decisions," not raw stack traces.
- Error returns: feed errors back as normal return values (let the model correct itself) rather than throwing exceptions that crash the loop.
- Side effects and idempotency: tools with write operations must consider the consequences of repeated calls.

**Hands-on Exercises**
- Refactor F1's tools, adding parameter validation and friendly error returns.
- Design a tool with side effects (e.g. writing a file / changing config), and think about how to prevent repeated execution.
- Deliberately give the model a vaguely described tool and observe how it misuses it.

**Deliverable**: A robust tool interface specification + 2-3 example tools.

---

# F3: Context Budgeting

**Learning Goal**: Solve the first real wall an Agent hits — context overflow.

**Core Content**
- Why it overflows: every round of tool results accumulates into context; long tasks or large outputs quickly fill the window.
- Three categories of coping strategies:
  - **Truncation**: keep only the key part of tool output.
  - **Summarization**: compress early conversation into a summary and continue.
  - **External memory**: store large chunks of information in files/database; keep only pointers in context.
- When to use which, and their tradeoffs (information loss vs extra call cost).
- The role of system prompt: which information should be permanent, which should be dynamically injected.

**Hands-on Exercises**
- Give the Agent a tool that outputs thousands of lines, reproduce the context overflow.
- Implement a simple output truncation strategy, then implement a "summarize when exceeding threshold" strategy.
- Compare task completion quality under the two strategies.

**Deliverable**: An Agent that won't crash under long tasks.

---

# F4: Failure-First Design

**Learning Goal**: Where Harness Engineering truly begins. Systematically identify and fix Agent failure modes.

**Core Content**
- **Infinite loops**: tool repeatedly errors, model repeatedly retries the same action. How to detect and break (max steps, repeat detection).
- **Drift**: in multi-step tasks the Agent deviates from the goal. How to pull it back with phased goals, self-checks, and human intervention.
- **Hallucinated calls**: the model calls a nonexistent tool, or fabricates parameters. Intercept and correct at the Harness layer.
- **Partial failure recovery**: in a multi-step task when one step fails, how to continue instead of starting over.
- **Retry and backoff**: API rate limits, timeouts — the most familiar part for network/backend engineers, directly transfer your experience.

**Hands-on Exercises**
- Artificially manufacture each type of failure: make tools error, inject rate limits, give a nonexistent tool name.
- Write Harness guards for each failure: max step limit, repeat action detection, unknown tool interception, API retry.
- Run a real multi-step task, record where it drifts, and improve.

**Deliverable**: An Agent that can self-recover from multiple types of errors.
**Core Takeaway**: In Agent code, "making it work" is only 20%; "making it not crash when things go wrong" is 80% — this is Harness Engineering.

---

# F5: Graceful Degradation

**Learning Goal**: When the model or tools fail, the system degrades rather than crashes.

**Core Content**
- **Degradation strategy pyramid**: full success → partial success → return approximate result → return safe fallback → graceful failure.
- **Model-side degradation**: when the model refuses/rambles, retry with a simpler prompt, a smaller model, or a preset template.
- **Tool-side degradation**: when a tool times out/exceptions, return "this tool is unavailable" and let the model find another path.
- **Partial results are valuable**: in multi-step tasks, completed portions should be preserved, not all discarded.
- **User-visible degradation**: when the Agent cannot complete, give a clear status explanation rather than a stack trace.

**Hands-on Exercises**
- Add a "degradation mode" switch to F4's Agent.
- Simulate a tool being completely unavailable, observe whether the Agent can provide an alternative or partial result.
- Design a "safe fallback response" for when the model repeatedly rambles.

**Deliverable**: An Agent that degrades rather than crashes in the face of failure.

---

# F6: Least-Privilege Tooling

**Learning Goal**: Let the Agent safely touch the real world. The security core of Harness.

**Core Content**
- **Why it's needed**: Agents autonomously decide actions; a wrong write operation could delete data or change production configs.
- **Tool allowlist**: which tools are callable, in what context they are callable.
- **Sandbox execution**: run tools in an isolated environment (restricted filesystem, network isolation, read-only mode).
- **Principle of least privilege**: read-only by default, write operations explicitly authorized — same mindset as firewall ACLs.

**Hands-on Exercises**
- Add a human confirmation gate to tools with side effects; only execute after confirmation.
- Implement a "read-only mode" switch: when enabled, all write operations are directly intercepted by the Harness.
- Write your Agent's "permission model": which operations auto-approve, which must confirm, which are permanently forbidden.

**Deliverable**: An Agent where dangerous operations require human confirmation and defaults to least privilege.

---

# F7: Human-in-the-Loop Gates

**Learning Goal**: Irreversible operations must pause for human confirmation, with suspend-resume support.

**Core Content**
- **Confirmation gate state machine**: running → suspended awaiting confirmation → resumed execution → completed.
- **Recoverable state**: when suspended, save full context and trace; a person can leave and resume later.
- **Batch confirmation vs single confirmation**: different risk levels use different strategies.
- **Timeout and default behavior**: what to do when the human doesn't respond for too long (cancel / use default safe option).
- **Audit log**: who, at what time, confirmed what operation.

**Hands-on Exercises**
- On top of F6, make "confirmation" an explicit state inside the loop, rather than a simple print inside the tool.
- Implement suspend-resume: after program exit, reload state and continue execution.
- Add timeout strategy and audit events to the confirmation gate.

**Deliverable**: An Agent with a recoverable human confirmation gate.

---

# F8: Observable by Default

**Learning Goal**: Without trace, you cannot debug the Agent. Make every step of the Agent visible, replayable.

**Core Content**
- **Why it's essential**: Agents are non-deterministic; the same input may take different paths. When things go wrong you need to know "what it was thinking, what it called, what it saw at the time." The Agent equivalent of packet capture.
- **Event model**: emit every step of the loop as a structured event (start thinking / decide to call tool / tool returns / error / complete).
- **Structured logging**: record each step's input/output, token consumption, time spent.
- **Replay and debugging**: how to reproduce an Agent run using the recorded trace.
- Cost and latency observability: how many tokens, how much money, how much time per task.

**Hands-on Exercises**
- Add an event emission layer to the Agent loop, writing each step as structured logs (JSON lines).
- Write a simple viewer that prints a run's trace as a readable timeline.
- Use the trace to debug a previously drifting task, pinpointing which step went wrong.

**Deliverable**: An Agent that produces a complete readable trace on every run.

---

# F9: Reproducible Runs

**Learning Goal**: Given a trace and configuration, reproduce or locate a failed run.

**Core Content**
- **Three elements of reproduction**: trace + config + seed (or at least model/temperature).
- **Determinism boundaries**: the LLM itself is not fully deterministic, but loop paths, tool calls, and failure points can be reproduced.
- **Regression testing**: turn a failed trace into a test case, verifying that after a fix the same class of failure no longer occurs.
- **Replay mode**: use an old trace to replace real model calls, quickly verifying Harness behavior.

**Hands-on Exercises**
- Save the complete trace + config of a failed run.
- Implement replay mode: read the trace, skip model calls, advance the loop according to the record, verifying Harness interception/recovery logic.
- Write a test: given a certain failed trace, the Agent must trigger degradation at step N.

**Deliverable**: An Agent where failures can be reproduced from trace and fixes can be tested.

---

# F10: Composable Agents

**Learning Goal**: Upgrade from a single Agent to an orchestrator — the advanced core of Harness Engineering.

**Core Content**
- **When multiple Agents are needed**: when tasks can be decomposed in parallel, when context isolation is needed, or when different "roles" are needed for division of labor.
- **Master-sub (orchestrator-worker) pattern**: the master Agent splits tasks, dispatches to sub-Agents, and aggregates results.
- **Context isolation**: each sub-Agent has its own independent context, preventing mutual contamination — sub-agents are also a form of context management.
- **A2A Protocol** (Agent-to-Agent Protocol): how Agents across different Harnesses discover capabilities, negotiate tasks. Google's open standard proposed in 2025, complementary to MCP — MCP solves Agent↔tool, A2A solves Agent↔Agent. When your Agent needs to call an Agent provided by an external team/service, A2A defines unified handshake, task delegation, and state synchronization.
- **Parallel execution**: multiple sub-Agents run simultaneously; how to collect and merge results.
- **Sub-Agent failure handling**: one sub-agent failing should not bring down the whole.
- Cost of orchestration: more complex, more expensive, harder to debug — when not to use multi-Agent.

**Hands-on Exercises**
- Implement a master Agent that can split a task into sub-tasks, each delegated to a sub-Agent.
- Implement parallel execution of multiple sub-Agents and aggregate results (e.g. parallel research on multiple topics / parallel diagnosis of multiple devices).
- Reuse F8's trace so that every sub-agent of the orchestrator is observable.

**Deliverable**: An orchestrator that can dispatch sub-tasks in parallel and aggregate results.

---

# F11: Config-Driven Behavior

**Learning Goal**: Externalize model, prompt, tool list, and security policy to configuration; make Harness behavior switchable and testable.

**Core Content**
- **What belongs in config**: model name, temperature, max_tokens, system prompt, tool list, security policy, confirmation gate threshold, degradation strategy.
- **Config format**: YAML/JSON/TOML, split by environment (dev / staging / prod).
- **Dynamic reload**: switch config without restarting the process (optional, depending on scenario).
- **A/B testing**: run the same batch of tasks with different configs, comparing completion rate and cost.
- **Config as contract**: config changes should trigger automated tests, ensuring loop behavior remains unchanged.

**Hands-on Exercises**
- Extract all hardcoded parameters from previous chapters (model, prompt, tool list, max_steps, permission policy) into a `config.yaml`.
- Write two configs: an "aggressive mode" (auto-confirm low-risk writes) and a "conservative mode" (all writes require human confirmation).
- Run the same task with both configs, observe behavioral differences.

**Deliverable**: A Harness whose behavior is fully driven by configuration.

---

# F12: Continuous Evaluation

**Learning Goal**: Harness quality should not be judged by whether the demo works, but measured continuously with metrics.

**Core Content**
- **Why it's needed**: a successful demo doesn't mean reliability; failure rate, recovery rate, and cost must be measured over many tasks.
- **Core metrics**:
  - Task completion rate
  - Failure rate
  - Recovery rate (proportion pulled back by Harness after failure)
  - Average steps / tokens / latency / cost
  - Human-in-the-loop rate
- **Evaluation dataset**: collect real tasks and known failure cases for periodic regression.
- **Evaluation harness**: write a runner that batch-runs tasks, automatically judges success/failure, and outputs a report.
- **Evaluation tool ecosystem (2026)**:
  - **DeepEval**: pytest-compatible LLM evaluation framework, 60+ metrics, native CI/CD integration.
  - **AgentAssay**: regression testing for non-deterministic Agent workflows, using behavioral fingerprints to detect 86% of regressions (traditional binary testing: 0%).
  - **promptfoo**: declarative YAML prompt testing + red-teaming, 50+ vulnerability plugins.
  - **LLM-as-Judge**: 2026 industry standard, 53.3% of organizations in use (LangChain survey data).
- **Designing from evaluation backwards**: whichever Factor's metrics are poor, prioritize improving that Factor.

**Hands-on Exercises**
- Prepare 10-20 representative tasks (including simple, complex, and trap cases).
- Write an `evaluate.py` that batch-runs and records each task's completion status, step count, tokens, and whether human confirmation was triggered.
- After modifying the Harness, rerun evaluation and see if key metrics improved.

**Deliverable**: A Harness that can be quantitatively evaluated and continuously improved.

---

# Advanced: Reading Real Harnesses

**Learning Goal**: With the pitfalls of the first 12 chapters in mind, read mature Harness source code and systematize scattered experience.

**Core Content**
- Recommended reading targets (pick one): open-source Agent runtimes, Coding Agent projects, or internal Harnesses.
- **Real Harnesses Worth Deep-Reading in 2026**:
  - **Vercel AI SDK 6**: TypeScript ecosystem benchmark, ToolLoopAgent + DevTools + full MCP support, 20M+ monthly downloads.
  - **Mastra**: TypeScript-native framework (22K+ stars), observational memory system (Observer + Reflector Agent), enterprise-grade RBAC.
  - **Microsoft Agent Framework 1.0**: unified Semantic Kernel + AutoGen, graph orchestration + middleware pipeline + DevUI debugger.
  - **OpenHands / SWE-agent**: open-source Coding Agent runtimes, see how they safely execute code in sandboxes.
  - **Temporal.io + Agent Orchestration**: persistent Agent workflows, learn how distributed system retry, state machines, and activity monitoring apply to Agents.
- Read with specific questions, not from beginning to end:
  - How does it manage context? (F3)
  - How does it handle tool errors and infinite loops? (F4/F5)
  - What does its permission/sandbox model look like? (F6/F7)
  - How is its trace/events designed? (F8/F9)
  - How does it do sub-agent / orchestration? (F10)
  - What do its config and evaluation look like? (F11/F12)

**Hands-on Exercises**
- Pick a real Harness and write a deep-reading note for each of the 6 questions above.
- Pick one design you think it does better than yours, and port it into your own Agent.

**Deliverable**: A source-code deep-reading note, plus at least one improvement to your own Agent.

---

# Capstone Project: A Complete Domain Agent

Combine all Factors into a truly problem-solving Agent. Pick a real task from your own domain:

- **Operations / Network direction**: A diagnostic Agent that can diagnose multiple devices in parallel (one sub-agent per device, master agent aggregates), write operations require human confirmation, full trace throughout.
- **Data direction**: A data analysis Agent that can autonomously query, clean, and generate reports.
- **Development direction**: A Coding Agent that can read a codebase, locate bugs, and propose fixes.

## Capstone Project Checklist (12-Factor Maturity Self-Assessment)

- [ ] **F1** Handwritten agent loop (not relying on heavy frameworks)
- [ ] **F2** A set of tools with validation and graceful error returns
- [ ] **F3** Context management strategy, long tasks don't crash
- [ ] **F4** Failure recovery: can handle tool errors, infinite loops, rate limits
- [ ] **F5** Degradation strategy: doesn't crash when model/tool fails
- [ ] **F6** Permission model: dangerous operations require confirmation, defaults to least privilege
- [ ] **F7** Human confirmation gate with suspend-resume
- [ ] **F8** Complete trace: every run is replayable and debuggable
- [ ] **F9** Failed runs can be reproduced / regression tested
- [ ] **F10** (Advanced) Multi-agent orchestration
- [ ] **F11** Key behavior driven by configuration
- [ ] **F12** Quantitative evaluation metrics and test suite

---

## Three Final Words to Learners

1. **Make it work first, then make it reliable, and only then make it complex** — don't jump straight to multi-Agent.
2. **Every Harness feature is born from some failure mode forcing it** — first manufacture failure, and you'll know why it's needed.
3. **Treat the model as an unreliable node, and yourself as the engineer building resilience around it** — this is the only truly important mental model of this course.

---

# Appendix: Course Website Implementation Plan

This course is presented as a static website, directly hosted on GitHub Pages / Cloudflare Pages, with no build step required.

## Technology Choices

| Dimension | Solution | Rationale |
|---|---|---|
| Build method | **Single-file HTML** (CSS/JS inline) | Zero dependencies, zero build, drag into browser and it works |
| Styling | Pure CSS, no external frameworks | Reduce loading, avoid CDN dependency |
| Fonts | System font stack | `system-ui, -apple-system, sans-serif`, Chinese fallback `"PingFang SC", "Microsoft YaHei"` |
| Code highlighting | Not for now | Add highlight.js later when code examples are expanded |
| Deployment | Cloudflare Pages (default) + GitHub Pages (fallback) | Push and it's live |

## Page Layout

```text
┌──────────────────────────────────────────────────┐
│  Top bar: course title + GitHub link + dark mode toggle      │
├────────────┬─────────────────────────────────────┤
│  Sidebar    │  Main content area (scroll through each Factor)        │
│  Prerequisite       │                                     │
│  F1-F12    │                                     │
│  Advanced/Capstone   │                                     │
├────────────┴─────────────────────────────────────┤
│  Footer: open source license / contribution guide                         │
└──────────────────────────────────────────────────┘
```

- **Sidebar**: 240px fixed position, doesn't move when scrolling
- **Content area**: max-width 780px centered
- **Mobile** (<768px): sidebar collapses to hamburger menu, content area full width

## HTML Structure for Each Factor

```html
<section id="factor-N">
  <h2>Factor N: Title</h2>
  <div class="goal-card">Learning Goal</div>
  <div class="content">Core content (body text + lists / tables)</div>
  <div class="exercises">Hands-on exercises (numbered cards)</div>
  <div class="output-card">Deliverable (highlighted block)</div>
</section>
```

## Visual Design

**Color scheme** (light/dark dual mode):

| Element | Light | Dark |
|---|---|---|
| Background | `#ffffff` | `#1a1a2e` |
| Body text | `#2d2d2d` | `#e0e0e0` |
| Sidebar | `#f7f7f8` | `#16213e` |
| Accent | `#2563eb` | `#60a5fa` |
| Card background | `#f0f4ff` | `#1e2a4a` |
| Key marker (★) | `#ef4444` | `#f87171` |

**Typography**: h1 2rem / h2 1.6rem / h3 1.25rem / body 1rem line-height 1.75. 4rem spacing between Factors.

**Special elements**:
- Core quote block: large font, left blue vertical line
- Learning goal: light blue background card
- Hands-on exercises: numbered cards, light gray background
- Deliverable: green left-border decorative block

## Interactive Features

| Feature | Implementation | Priority |
|---|---|---|
| Sidebar navigation | Anchor + `scroll-behavior: smooth` | Required |
| Current Factor highlight | `IntersectionObserver` dynamically adds `.active` | Required |
| Dark mode | CSS variables + `localStorage` memory | Required |
| Mobile menu | Hamburger button expands overlay | Required |
| Progress tracking | `localStorage` saves check state | Optional |
| Search | Skip, single-page Ctrl+F is enough | Skip |

## Content Adaptation Mapping

| Markdown Element | Web Presentation |
|---|---|
| `# Factor N: Title` | `<section id="factor-N"><h2>` |
| `**Learning Goal**` | Goal card component |
| `**Core Content**` + list | Body text + `<ul>` |
| `**Hands-on Exercises**` + list | Exercise cards (numbered) |
| `**Deliverable**` | Deliverable highlighted block |
| `> Quote` | Quote block (large font, blue vertical line) |
| Table | `<table>` clean horizontal-line style |

## Repository Structure

```text
agent-harness-course/
├── index.html                # Only page file (CSS/JS inline)
├── agent-harness-course.md   # Course original Markdown (for contributors to edit)
├── GLOSSARY.md               # Glossary
├── README.md                 # Repo description + online access URL + contribution guide
└── examples/                 # Skeleton code and reference implementations by Factor
```

Each Factor directory should contain: `README.md` (lecture notes), `starter/` (skeleton code), `solution/` (reference implementation), `exercises.md` (exercises).

## Future Expansion Directions

- ✅ Restructure course around 12-Factor
- ✅ Add skeleton code and reference implementations for each Factor (see `examples/`)
- ✅ Unified glossary (see `GLOSSARY.md`)
- Add architecture diagrams / flowcharts (Agent loop state machine diagram, Harness layering diagram, 12-Factor relationship diagram)
- Migrate to VitePress after content bloat (Markdown-driven, low migration cost)
- Multilingual support (English version)

---

# Appendix: 2026 Harness Ecosystem Overview

> This appendix records key protocols, frameworks, and standards in the Agent / Harness domain from 2025-2026, for learners to quickly understand the industry landscape after completing the course.

## Protocol Layer

| Protocol | Initiator | Problem Solved | Course Correlation |
|---|---|---|---|
| **MCP** (Model Context Protocol) | Anthropic (2024) | Standardize context exchange between Agent and external tools/data sources | F2 (Tool Contract), F6 (Permissions) |
| **A2A** (Agent-to-Agent) | Google (2025) | Capability discovery and task collaboration between different Agents | F10 (Composable Agents) |
| **AGENTS.md** | Anthropic → Community Standard | Describe project specs and safety constraints to coding Agents | F11 (Config-Driven) |
| **SKILL.md** | Anthropic → Community Standard | Standard format for Agent Skill packages | F10-F12 |

## Framework Layer (2026 Mainstream)

| Framework | Language | Core Features | Use Case |
|---|---|---|---|
| **Vercel AI SDK 6** | TypeScript | 20M+ monthly downloads, ToolLoopAgent, DevTools, full MCP support | Web / full-stack TS projects |
| **Mastra** | TypeScript | 22K+ stars, observational memory, enterprise RBAC, remote sandbox | Enterprise apps needing complex memory |
| **Microsoft Agent Framework 1.0** | Python / .NET | Unified Semantic Kernel + AutoGen, graph orchestration, middleware pipeline, DevUI | Microsoft ecosystem / enterprise .NET |
| **OpenAI Agents SDK** | Python | Native sandbox execution, configurable memory, MCP support | OpenAI model priority |
| **LangGraph** | Python / JS | Graph-structure orchestration, explicit state machines | Complex workflows |
| **Temporal + Agent** | Multi-language | Persistent Agent workflows, distributed-system-level reliability | Long-running tasks |

## Evaluation Tools

| Tool | Purpose | Course Correlation |
|---|---|---|
| **DeepEval** | pytest-compatible LLM evaluation framework, 60+ metrics | F12 |
| **AgentAssay** | Non-deterministic Agent regression testing, behavioral fingerprints | F9/F12 |
| **promptfoo** | Declarative prompt testing + red-teaming, 50+ vulnerability plugins | F2/F12 |
| **RAGAS** | RAG / Agent quality evaluation | F12 |

## Notable Enterprise Practices

- **Shopify Roast**: Ruby DSL structured AI workflows, "non-determinism is the enemy of reliability" — interleaving deterministic steps (shell, code) with Agent steps, version-controllable.
- **Anthropic Claude Code Quality Report**: Demonstrates how tiny Harness adjustments (prompt wording, cache headers, default parameters) compound into visible Agent degradation.
- **Red Hat Four-Pillar Model**: vibes → specs → skills → agents, from structured context to MCP integration, defining Harness from a human-Agent collaboration perspective.

## 2026 Key Trends

1. **Protocol Standardization**: MCP + A2A are unifying the "plugs" of the Agent ecosystem; the framework layer is no longer reinventing wheels individually.
2. **Evaluation as Infrastructure**: From "demo works" to "CI passes," Agent evaluation becomes a production gate.
3. **Memory System Divergence**: Short-term context (F3) vs long-term structured memory (Mastra Observer/Reflector) vs retrieval augmentation (RAG).
4. **CodeAct Execution Mode**: Agent generates Python programs to call multiple tools in one shot, reducing 52% latency and 64% tokens compared to per-round tool calls.
5. **Harness as Product**: Engineer value shifts from writing code to designing constraint environments — "environment-first engineering."

---

*This course is open-source learning material. Welcome to fork, adapt, and extend on GitHub.*
