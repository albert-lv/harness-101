# Factor 5: Failure-First Design & Graceful Degradation

This Factor merges the former "Failure-First Design" and "Graceful Degradation" chapters: assume failure will happen, contain it, and degrade instead of crashing.

## How to Run

```bash
# resilience.py needs an API key; degradation.py is a pure local simulation
export ANTHROPIC_API_KEY=your_key
python solution/resilience.py
python solution/degradation.py
```

## Files

- `starter/resilience.py`: Skeleton code with TODOs.
- `solution/resilience.py`: Reference implementation integrating max steps, repetition detection, unknown tool interception, and API retry.
- `starter/degradation.py`: Skeleton code with TODOs.
- `solution/degradation.py`: Reference implementation demonstrating degradation strategies and fallback responses.
