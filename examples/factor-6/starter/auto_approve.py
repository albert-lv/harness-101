"""
Factor 6：Permission Models —— Auto-Approve 策略（骨架代码）

目标：在最小权限基线之上，实现安全/效率光谱中的 auto 审批模式。
参考：nano-agent docs/development/PERMISSION_AUTO_APPROVAL.md 与 PERMISSION_POLICY.md
"""

# TODO 1: 定义权限模式枚举：ask（逐个确认）→ allowlist（会话白名单）→ auto → yolo
# TODO 2: 实现两级风险分类器：只读工具为 safe，写/执行类工具为 risky
# TODO 3: 实现 workdir 快速路：auto 模式下，workdir 内的文件编辑直接放行
# TODO 4: 实现可配置失败策略：分类器异常时按 on_error="ask"/"deny" 处理
# TODO 5: 实现带 15s 超时的人工确认（超时视为拒绝）
# TODO 6: 记录审计日志：每次决策写入（tool, mode, decision, reason）


class PermissionEngine:
    def __init__(self, mode: str = "ask", workdir: str = ".", on_error: str = "ask"):
        raise NotImplementedError("TODO")

    def decide(self, tool_name: str, tool_input: dict) -> bool:
        raise NotImplementedError("TODO")
