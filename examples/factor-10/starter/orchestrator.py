"""
Factor 10：Composable Agents（骨架代码）

目标：实现主-子 Agent 编排器，支持并行派发与失败隔离。
"""

# TODO 1: 实现 Orchestrator 类，能把任务拆成子任务
# TODO 2: 实现 Worker 类，每个 Worker 是一个独立子 Agent
# TODO 3: 实现并行执行多个 Worker 并汇总结果
# TODO 4: 实现子 Agent 失败隔离：一个失败不拖垮整体


class Orchestrator:
    def __init__(self, workers: list):
        self.workers = workers

    def run(self, task: str):
        raise NotImplementedError("TODO")
