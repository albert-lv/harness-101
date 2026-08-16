# Factor 11: Config-Driven & Reproducible Runs

This Factor merges the former "Config-Driven Behavior" and "Reproducible Runs" chapters: configuration is the behavior contract, and a run is reproducible when its config + trace fully determine the path.

## How to Run

```bash
export ANTHROPIC_API_KEY=your_key
python solution/config_driven.py
python solution/replay.py
```

## Files

- `starter/config_driven.py`: Skeleton code with TODOs.
- `solution/config_driven.py`: Reference implementation of loading configuration and driving Agent behavior.
- `starter/replay.py`: Skeleton code with TODOs.
- `solution/replay.py`: Reference implementation of trace replay and regression testing — pin a run's behavior via its config, then replay it without calling the real model.
