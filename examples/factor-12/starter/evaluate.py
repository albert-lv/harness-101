"""
Factor 12：Continuous Evaluation（骨架代码）

目标：批量运行任务，记录完成率、失败率、恢复率、token、延迟等指标。
"""

# TODO 1: 准备评估数据集（tasks.json），包含简单/复杂/带陷阱的任务
# TODO 2: 实现 Evaluator 类，批量调用 Agent 并记录结果
# TODO 3: 实现指标统计：完成率、失败率、恢复率、平均步数、平均延迟
# TODO 4: 输出报表（Markdown/JSON）


class Evaluator:
    def __init__(self, tasks: list):
        self.tasks = tasks

    def run(self, agent_fn):
        raise NotImplementedError("TODO")
