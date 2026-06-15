"""
Factor 12：Continuous Evaluation（参考实现片段）
"""
import json
import time


class Evaluator:
    def __init__(self, tasks: list[dict]):
        self.tasks = tasks

    def run(self, agent_fn):
        results = []
        for task in self.tasks:
            start = time.time()
            try:
                result = agent_fn(task["prompt"])
                status = "success"
            except Exception as e:
                result = str(e)
                status = "failure"
            elapsed = time.time() - start
            results.append({
                "id": task["id"],
                "status": status,
                "result": result,
                "elapsed_ms": int(elapsed * 1000),
            })
        return results

    def report(self, results: list[dict]) -> dict:
        total = len(results)
        successes = sum(1 for r in results if r["status"] == "success")
        failures = total - successes
        avg_time = sum(r["elapsed_ms"] for r in results) / total if total else 0
        return {
            "total": total,
            "success_rate": successes / total if total else 0,
            "failure_rate": failures / total if total else 0,
            "avg_elapsed_ms": avg_time,
        }


def dummy_agent(prompt: str) -> str:
    if "陷阱" in prompt:
        raise RuntimeError("故意失败")
    return f"完成: {prompt}"


if __name__ == "__main__":
    tasks = [
        {"id": "t1", "prompt": "简单任务"},
        {"id": "t2", "prompt": "复杂任务"},
        {"id": "t3", "prompt": "带陷阱的任务"},
    ]
    evaluator = Evaluator(tasks)
    results = evaluator.run(dummy_agent)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print(json.dumps(evaluator.report(results), ensure_ascii=False, indent=2))
