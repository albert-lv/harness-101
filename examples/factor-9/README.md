# Factor 9: Workspace & Artifacts Management

Every task runs in an isolated workspace (git baseline, lifecycle hooks, cleanup policy), and artifacts are the persistent output contract of a run: collected from the workspace, persisted with a manifest, downloadable, and renderable in a UI.

Reference implementation: nano-symphony's workspace and unified artifact management.

## How to Run

```bash
python solution/workspace.py
```

> Pure standard library (uses `git` via `subprocess` for the baseline). No API key required.

## Files

- `starter/workspace.py`: Skeleton code with TODOs.
- `solution/workspace.py`: Reference implementation — isolated per-task workspace with git baseline and lifecycle hooks, plus artifact collection with a manifest.
