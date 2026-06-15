"""
Factor 7：Human-in-the-Loop Gates（骨架代码）

目标：不可逆操作暂停等人确认，并支持挂起-恢复。
"""

# TODO 1: 定义 HumanGate 状态机：running / pending / resumed / cancelled
# TODO 2: 实现 request_approval(action)：保存状态并返回 pending
# TODO 3: 实现 resume(state, decision)：根据人类决策恢复或取消
# TODO 4: 把状态持久化到文件，支持进程重启后恢复


class HumanGate:
    def __init__(self, state_file: str = "human_gate_state.json"):
        self.state_file = state_file

    def request_approval(self, action: dict) -> str:
        raise NotImplementedError("TODO")

    def resume(self, decision: str) -> dict:
        raise NotImplementedError("TODO")
