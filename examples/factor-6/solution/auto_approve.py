"""
Factor 6：Permission Models —— Auto-Approve 策略（参考实现）

安全/效率光谱：ask（逐个确认）→ allowlist（会话白名单）→ auto（分类器自动审批）→ yolo。
auto 模式 = 两级风险分类器 + workdir 内编辑快速路 + 可配置失败策略 + 15s 确认超时。
所有决策写入审计日志。参考：nano-agent PERMISSION_AUTO_APPROVAL.md / PERMISSION_POLICY.md
"""
import os
import time

READONLY_TOOLS = {"read_file", "list_dir", "search"}
WRITE_TOOLS = {"write_file", "delete_file", "run_command"}
CONFIRM_TIMEOUT_S = 15


def classify_risk(tool_name: str) -> str:
    """两级分类器：safe（只读）/ risky（写或执行）。未知工具视为 risky。"""
    if tool_name in READONLY_TOOLS:
        return "safe"
    if tool_name in WRITE_TOOLS:
        return "risky"
    raise ValueError(f"未知工具: {tool_name}")


def confirm_with_timeout(prompt: str, timeout: float = CONFIRM_TIMEOUT_S) -> bool:
    """人工确认，超过 timeout 秒未响应视为拒绝。演示环境无人应答，直接走到超时分支。"""
    deadline = time.time() + timeout
    answered = False  # 真实实现：在此阻塞读取用户输入，超过 deadline 仍未输入则保持 False
    return answered and time.time() <= deadline


class PermissionEngine:
    def __init__(self, mode: str = "ask", workdir: str = ".", on_error: str = "ask"):
        assert mode in {"ask", "allowlist", "auto", "yolo"}
        assert on_error in {"ask", "deny"}
        self.mode = mode
        self.workdir = os.path.abspath(workdir)
        self.on_error = on_error
        self.session_allowlist: set[str] = set()
        self.audit_log: list[dict] = []

    def _audit(self, tool_name: str, decision: bool, reason: str):
        entry = {"tool": tool_name, "mode": self.mode, "decision": decision, "reason": reason}
        self.audit_log.append(entry)
        print(f"[audit] {entry}")

    def _in_workdir(self, tool_input: dict) -> bool:
        path = tool_input.get("path")
        if not path:
            return False
        return os.path.abspath(path).startswith(self.workdir + os.sep)

    def _auto_decide(self, tool_name: str, tool_input: dict) -> tuple[bool, str]:
        try:
            risk = classify_risk(tool_name)
        except ValueError:
            # 失败策略：分类器异常时按配置降级为人工确认或直接拒绝
            if self.on_error == "deny":
                return False, "分类器失败，on_error=deny"
            return confirm_with_timeout(f"未知工具 {tool_name}"), "分类器失败，转人工确认"
        if risk == "safe":
            return True, "只读工具，自动放行"
        if tool_name == "write_file" and self._in_workdir(tool_input):
            return True, "workdir 内编辑，快速路放行"
        return confirm_with_timeout(f"允许 {tool_name}?"), "risky 操作，转人工确认"

    def decide(self, tool_name: str, tool_input: dict) -> bool:
        if self.mode == "yolo":
            decision, reason = True, "yolo 模式全放行"
        elif tool_name in self.session_allowlist:
            decision, reason = True, "命中会话白名单"
        elif self.mode == "allowlist":
            decision, reason = confirm_with_timeout(f"允许 {tool_name}?"), "allowlist 模式逐个确认"
            if decision:
                self.session_allowlist.add(tool_name)
        elif self.mode == "auto":
            decision, reason = self._auto_decide(tool_name, tool_input)
        else:
            decision, reason = confirm_with_timeout(f"允许 {tool_name}?"), "ask 模式逐个确认"
        self._audit(tool_name, decision, reason)
        return decision


if __name__ == "__main__":
    engine = PermissionEngine(mode="auto", workdir="/tmp/demo", on_error="deny")
    print(engine.decide("read_file", {"path": "/etc/hosts"}))                # safe -> True
    print(engine.decide("write_file", {"path": "/tmp/demo/notes.txt"}))       # 快速路 -> True
    print(engine.decide("run_command", {"cmd": "rm -rf /tmp/demo"}))          # risky -> 超时拒绝
    print(engine.decide("mystery_tool", {}))                                  # 分类器失败 -> deny
