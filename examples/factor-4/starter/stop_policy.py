"""
Factor 4：Knowing When to Stop（骨架代码）

目标：实现 turn termination policy，让 Harness 知道何时该停。
参考：nano-agent pkg/agent/turn_policy.go
"""

# TODO 1: 支持显式完成：模型调用 task_done 工具时，用 verifier 校验"完成"声明，不可轻信
# TODO 2: 支持隐式完成：finish_reason == "end_turn" 且没有 pending 工具调用时结束
# TODO 3: 循环检测一：同一工具签名连续重复 N 次 → 先警告，再强制停止
# TODO 4: 循环检测二：diminishing returns —— 最近 K 步没有产生任何新观测 → 停止
# TODO 5: 循环检测三：相似内容循环 —— 相邻输出相似度超过阈值（提示：difflib.SequenceMatcher）
# TODO 6: 错误熔断：连续错误达到阈值 → 熔断停止，并给出停止原因


class TurnPolicy:
    def __init__(self, max_repeat: int = 3, max_stale: int = 4, max_errors: int = 3):
        raise NotImplementedError("TODO")

    def should_stop(self, action: dict) -> tuple[bool, str]:
        """每个 turn 调用一次。返回 (是否停止, 原因)。"""
        raise NotImplementedError("TODO")
