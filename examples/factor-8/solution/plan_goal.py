"""
Factor 8：Plan & Goal Modes（参考实现）

Plan 模式：探索（只读）→ 出计划 → 人审门禁 → 执行；获批前禁止写操作。
Goal 模式：声明目标与完成判据，evaluator 未判满足前自主续跑。
参考：nano-agent docs/features/PLAN_MODE.md 与 /goal 命令；nano-symphony plan runs
"""

READONLY_TOOLS = {"read_file", "list_dir", "search"}
WRITE_TOOLS = {"write_file", "delete_file", "run_command"}


class PlanMode:
    """阶段：explore -> plan -> 等待审批 -> execute。审批前只读。"""

    def __init__(self, approver):
        self.approver = approver  # callable(plan: list[str]) -> bool
        self.phase = "explore"
        self.plan: list[str] = []

    def check_tool(self, tool_name: str) -> bool:
        """Harness 门禁：explore/plan 阶段只放行只读工具。"""
        if self.phase == "execute":
            return True
        return tool_name in READONLY_TOOLS

    def submit_plan(self, plan: list[str]):
        self.plan = plan
        self.phase = "review"
        if self.approver(plan):
            print("[plan] 计划获批，进入执行阶段")
            self.phase = "execute"
        else:
            print("[plan] 计划被驳回，回到探索阶段")
            self.phase = "explore"

    def run(self, agent):
        while self.phase != "execute":
            action = agent.act(self.phase)
            if action["type"] == "tool":
                allowed = self.check_tool(action["tool"])
                print(f"[plan:{self.phase}] {action['tool']} -> {'放行' if allowed else '拦截（只读阶段）'}")
                if allowed:
                    agent.observe(f"{action['tool']} 的结果")
            elif action["type"] == "plan":
                self.submit_plan(action["plan"])
        for step in self.plan:
            print(f"[execute] {step}")


class GoalMode:
    """声明目标与完成判据，evaluator 判满足才停；max_turns 兜底。"""

    def __init__(self, goal: str, evaluator, max_turns: int = 20):
        self.goal = goal
        self.evaluator = evaluator  # callable(state: dict) -> tuple[bool, str]
        self.max_turns = max_turns

    def run(self, agent):
        print(f"[goal] 目标: {self.goal}")
        for turn in range(self.max_turns):
            state = agent.act("execute")
            done, reason = self.evaluator(state)
            print(f"[goal] turn={turn} state={state} -> {'满足' if done else '未满足'}: {reason}")
            if done:
                return True
        print(f"[goal] 达到 max_turns={self.max_turns}，强制停止")
        return False


class DemoAgent:
    """模拟 agent：先探索，提交计划；goal 模式下逐步累积进度。"""

    def __init__(self):
        self.observations = []
        self.progress = 0
        self._tried_write = False

    def observe(self, obs: str):
        self.observations.append(obs)

    def act(self, phase: str):
        if phase == "execute":
            self.progress += 1
            return {"progress": self.progress}
        if len(self.observations) >= 2:
            return {"type": "plan", "plan": ["step1: 改代码", "step2: 跑测试"]}
        if not self._tried_write:
            # 先尝试写操作，演示只读阶段的拦截
            self._tried_write = True
            return {"type": "tool", "tool": "write_file"}
        return {"type": "tool", "tool": "read_file"}


if __name__ == "__main__":
    print("== Plan 模式 ==")
    PlanMode(approver=lambda plan: True).run(DemoAgent())
    print("== Goal 模式 ==")
    GoalMode(
        goal="把进度推进到 3",
        evaluator=lambda s: (s["progress"] >= 3, f"progress={s['progress']}/3"),
        max_turns=10,
    ).run(DemoAgent())
