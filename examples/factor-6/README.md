# Factor 6: Permission Models

Least privilege is the baseline; this Factor also explores the safety/efficiency spectrum: confirm every call → session allowlist → auto mode → YOLO, with an audit log recording every decision.

## How to Run

```bash
python solution/permissions.py
python solution/auto_approve.py
```

> This Factor mainly demonstrates permission models and sandbox design. No API key required.

## Files

- `starter/permissions.py`: Skeleton code with TODOs.
- `solution/permissions.py`: Reference implementation of tool allow-list, read-only mode, and path blocklist.
- `starter/auto_approve.py`: Skeleton code with TODOs.
- `solution/auto_approve.py`: Reference implementation of auto-approval policy — two-level risk classifier, in-workdir edit fast path, configurable failure policy, 15s confirm timeout, and an audit log.
