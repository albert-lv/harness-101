# Factor 4: Knowing When to Stop

A harness must decide when a run ends: explicit completion via a `task_done` tool (validated, not trusted blindly), implicit completion via `finish_reason`, loop detection (repeated calls, diminishing returns, similar content), and an error-threshold circuit breaker.

Reference implementation: nano-agent's turn termination policy (`pkg/agent/turn_policy.go`).

## How to Run

```bash
python solution/stop_policy.py
```

> Pure standard library; the model is simulated so the policy logic is observable end to end. No API key required.

## Files

- `starter/stop_policy.py`: Skeleton code with TODOs.
- `solution/stop_policy.py`: Reference implementation of a turn termination policy — completion validation, three loop detectors, and an error circuit breaker.
