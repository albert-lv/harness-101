"""
Factor 5：Graceful Degradation（骨架代码）

目标：模型/工具失败时，Agent 能降级而不是崩溃。
"""

# TODO 1: 实现一个 fallback_model_call，当主模型失败时换用更简单的 prompt 或更小的模型
# TODO 2: 实现一个 safe_tool_call，工具异常时返回 "该工具不可用" 而不是抛异常
# TODO 3: 实现一个 degrade_response，当连续失败时返回清晰的状态说明


def call_model_with_degradation(messages, max_retries=3):
    raise NotImplementedError("TODO")


def call_tool_with_degradation(tool_name, tool_input):
    raise NotImplementedError("TODO")
