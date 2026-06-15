"""
Factor 10：Composable Agents（参考实现片段）

简化版 orchestrstrator-worker，使用 concurrent.futures 并行执行。
"""
from concurrent.futures import ThreadPoolExecutor, as_completed


class Worker:
    def __init__(self, name: str, skills: list):
        self.name = name
        self.skills = skills

    def run(self, subtask: str) -> dict:
        # 这里应替换为真实子 Agent 调用
        return {
            "worker": self.name,
            "subtask": subtask,
            "result": f"[{self.name}] 完成: {subtask}",
        }


class Orchestrator:
    def __init__(self, workers: list[Worker]):
        self.workers = workers

    def split(self, task: str) -> list[str]:
        # 简化：按逗号拆分子任务
        return [t.strip() for t in task.split(",") if t.strip()]

    def run(self, task: str) -> dict:
        subtasks = self.split(task)
        results = []
        errors = []

        with ThreadPoolExecutor(max_workers=len(self.workers)) as executor:
            futures = {
                executor.submit(worker.run, subtask): (worker.name, subtask)
                for worker, subtask in zip(self.workers, subtasks)
            }
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    name, subtask = futures[future]
                    errors.append({"worker": name, "subtask": subtask, "error": str(e)})

        return {"results": results, "errors": errors}


if __name__ == "__main__":
    workers = [Worker(f"worker-{i}", ["general"]) for i in range(3)]
    orch = Orchestrator(workers)
    print(orch.run("调研 A, 调研 B, 调研 C"))
