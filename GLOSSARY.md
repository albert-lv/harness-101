# Glossary

> Consistent terminology used throughout this course. Contributors should prioritize the definitions in this table when adding new content to avoid ambiguity.

## Agent

A loop that enables large language models to "do things": it can call tools, observe results, and make multi-step decisions, rather than just answering questions. The core of an Agent is the **loop**, not the model itself.

## Harness / Agent Harness

All engineering code and runtime that wraps a bare LLM API into a reliable Agent: context management, prompt assembly, tool execution, permission sandboxing, sub-agent scheduling, error recovery, and tracing. Claude Code, Cursor, and OpenHands are fundamentally Harnesses.

## Agent Loop

The core state machine of an Agent: `call model → parse tool calls → execute tools → feed results back into context → call model again` until the model decides to finish.

## Tool

The only interface through which an Agent interacts with the external world. Each tool includes a name, description (the "prompt" visible to the model), parameter schema, and the actual execution function.

## Tool Contract

The complete agreement of a tool: name, description, parameter schema, return format, side effects, and idempotency semantics. The quality of the contract directly determines whether the model calls it correctly.

## Context / Context Window

All input text visible to the model. Length is limited by the model's context window, and token billing is based on it. The Harness must manage context budget and quality.

## Context Budgeting

Managing context as a finite resource: truncation, summarization, external memory — making trade-offs between information loss and cost.

## Tool Call

When the model requests to invoke a tool in its response, including the tool name and arguments. The Harness is responsible for parsing, executing, and returning results to the model.

## Hallucinated Call

When the model calls a non-existent tool or invents non-existent parameters. The Harness must intercept and correct this.

## Dead Loop

The Agent repeatedly performs the same action or repeatedly errors, unable to make forward progress. Must be interrupted through max steps, repetition detection, and staged goals.

## Drift

The Agent deviates from the original goal during multi-step tasks. Usually corrected through staged goals, self-checks, and human intervention.

## Idempotency

Performing an operation multiple times has the same effect as performing it once. Critical for tools with side effects (writing files, modifying configs).

## Allow-List

Explicitly listing which tools are available in which contexts. The principle of least privilege: default deny, explicit grant.

## Human-in-the-Loop

For dangerous or irreversible operations, the Harness pauses execution and waits for human confirmation, with recoverable state.

## Sandbox

Restricting tool execution to an isolated environment (limited file system, network isolation, read-only mode) to reduce the blast radius of Agent misoperations.

## Trace

A complete structured record of an Agent run: thoughts, tool calls, results, errors, completion. The trace is the Agent's "black box".

## Event

A single structured record within a Trace. Common event types: think, tool_call, tool_result, error, complete.

## Orchestrator-Worker

Multi-Agent architecture: the main Agent (orchestrator) breaks down tasks and dispatches them to sub-Agents (workers), which complete independently and return results to the main Agent for aggregation.

## 12-Factor Harness

The production-grade Harness design methodology proposed in this course, consisting of 12 principles covering loop, tools, context, fault tolerance, permissions, observability, orchestration, configuration, and evaluation.

## Config-Driven

Model selection, system prompts, tool lists, security policies, and other behaviors should be externalized to configuration rather than hard-coded, enabling environment switching and A/B testing.

## Continuous Evaluation

Harness quality should not be judged solely by whether demos succeed, but continuously measured through failure rate, recovery rate, task completion rate, cost, and latency.

## MCP / Model Context Protocol

An open standard protocol proposed by Anthropic (2024) for standardizing context exchange between LLM applications and external data sources/tools. Widely adopted by OpenAI, Google, and others in 2025–2026, becoming the industry standard for Agent tool integration.

## A2A / Agent-to-Agent Protocol

An open protocol proposed by Google (2025) for task discovery, capability negotiation, and collaborative communication between different Agents. Complements MCP: MCP solves Agent↔Tool, A2A solves Agent↔Agent.

## AGENTS.md

A context file standard for coding Agents (proposed by Anthropic, adopted by OpenAI, etc.), used to describe project structure, conventions, and security constraints to the Agent. Essentially the Agent's "README".

## SKILL.md

An open standard format for Agent Skills (proposed by Anthropic), defining skill packages that Agents can load: instruction sets, tool definitions, and reference documentation. Adopted by platforms such as OpenClaw.

## CodeAct

An Agent execution mode (popularized by Microsoft) where the Agent generates short Python programs that invoke multiple tools in a sandbox at once, reducing latency by 52% and token consumption by 64% compared to round-by-round tool calls.
