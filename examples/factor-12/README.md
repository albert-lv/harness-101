# Factor 12: Observability & Continuous Evaluation

This Factor merges the former "Observable by Default" and "Continuous Evaluation" chapters: events / metrics / traces are the data foundation that evaluation runs on.

## How to Run

```bash
python solution/trace_logger.py
python solution/evaluate.py
```

## Files

- `starter/trace_logger.py`: Skeleton code with TODOs.
- `solution/trace_logger.py`: Reference implementation of JSONL event log + timeline viewer.
- `starter/evaluate.py`: Skeleton code with TODOs.
- `solution/evaluate.py`: Batch task evaluation runner and report output reference implementation — the traces you emit in production become the regression dataset here.
