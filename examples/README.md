# Hands-On Code Examples

This directory is organized by **Harness 12-Factor**. Each chapter provides runnable skeleton code (`starter/`) and reference implementations (`solution/`).

> **Learning Tip**: Try to implement it yourself based on the course lectures first. Check `solution/` only when you're stuck or want to compare.

## Directory Structure

```text
examples/
├── prep/                  # Prep: Environment & first API call
├── factor-1/              # Single Agent Loop
├── factor-2/              # Explicit Tool Contract
├── factor-3/              # Context Budgeting
├── factor-4/              # Failure-First Design
├── factor-5/              # Graceful Degradation
├── factor-6/              # Least-Privilege Tooling
├── factor-7/              # Human-in-the-Loop Gates
├── factor-8/              # Observable by Default
├── factor-9/              # Reproducible Runs
├── factor-10/             # Composable Agents
├── factor-11/             # Config-Driven Behavior
└── factor-12/             # Continuous Evaluation
```

Each Factor directory should ideally contain:

- `README.md` — Instructions and how to run the code for this Factor
- `starter/` — Skeleton code with TODOs for you to fill in
- `solution/` — Reference implementation
- `exercises.md` — Additional exercises for the code

## Quick Start

```bash
# Enter any Factor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python starter/xxx.py
```

## Contributing Code Examples

1. Keep examples consistent with the course lectures.
2. Prioritize standard library + `anthropic` (or OpenAI API-compatible library), avoid introducing frameworks.
3. Document required environment variables (e.g. `ANTHROPIC_API_KEY`) in `README.md`.
