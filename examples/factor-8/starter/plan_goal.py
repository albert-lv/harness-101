"""
Factor 8：Plan & Goal Modes（骨架代码）

目标：在普通 Agent Loop 之上实现两种结构化运行模式。
参考：nano-agent docs/features/PLAN_MODE.md 与 /goal 命令；nano-symphony 的 plan runs + 审批门禁
"""

# TODO 1: 实现 PlanMode：
# - 探索阶段只允许只读工具（read_file / list_dir / search）
# - 产出计划后进入审批门禁，获批前禁止任何写操作
# - 审批通过后才切换到执行阶段，放开写工具
# TODO 2: 实现 GoalMode：
# - 声明目标 + 完成判据（evaluator 函数）
# - 每个 turn 结束后用 evaluator 检查判据，满足则停止，否则自主续跑
# - 仍要有 max_turns 兜底
# TODO 3: 演示：写一个模拟 agent，在两种模式下各跑一遍


class PlanMode:
    def __init__(self, approver):
        raise NotImplementedError("TODO")

    def run(self, agent):
        raise NotImplementedError("TODO")


class GoalMode:
    def __init__(self, goal: str, evaluator, max_turns: int = 20):
        raise NotImplementedError("TODO")

    def run(self, agent):
        raise NotImplementedError("TODO")
