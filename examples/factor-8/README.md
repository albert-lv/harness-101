# Factor 8: Plan & Goal Modes

Two structured run modes beyond the plain loop:

- **Plan mode**: explore (read-only) → produce a plan → human approval gate → execute. No writes before approval.
- **Goal mode**: declare a goal with explicit completion criteria; the agent keeps running autonomously until the evaluator says the criteria are met.

Reference implementations: nano-agent `docs/features/PLAN_MODE.md` and the `/goal` command; nano-symphony's plan runs with approval gates.

## How to Run

```bash
python solution/plan_goal.py
```

> Pure standard library; the agent and human approver are simulated. No API key required.

## Files

- `starter/plan_goal.py`: Skeleton code with TODOs.
- `solution/plan_goal.py`: Reference implementation of both modes — read-only plan phase with an approval gate, and a goal loop driven by an evaluator.
