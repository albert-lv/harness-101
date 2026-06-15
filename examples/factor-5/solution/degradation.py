"""
Factor 5：Graceful Degradation（参考实现片段）
"""
import random


def call_model_with_degradation(messages, max_retries=3):
    """模拟模型调用：第一次可能失败，第二次用简化 prompt 重试，最后返回兜底。"""
    for attempt in range(max_retries):
        try:
            # 模拟成功概率随尝试增加
            if random.random() < 0.3 + attempt * 0.2:
                return {"role": "assistant", "content": "任务已完成。"}
            raise RuntimeError("模型拒绝或超时")
        except Exception as e:
            if attempt == max_retries - 1:
                return {
                    "role": "assistant",
                    "content": "[降级回复] 当前模型调用异常，我已记录错误，请稍后重试或简化任务。"
                }
            # 简化 prompt：只保留 system 和最后一条 user
            messages = [messages[0], messages[-1]]


def call_tool_with_degradation(tool_func, tool_input):
    try:
        return tool_func(**tool_input)
    except Exception as e:
        return f"[工具不可用] {type(e).__name__}: {e}。请尝试其他工具或路径。"


def degraded_calculator(expression: str):
    if expression == "fail":
        raise RuntimeError("故意失败")
    return eval(expression)


if __name__ == "__main__":
    msgs = [
        {"role": "system", "content": "你是助手。"},
        {"role": "user", "content": "帮我算 1+1"},
    ]
    print(call_model_with_degradation(msgs))
    print(call_tool_with_degradation(degraded_calculator, {"expression": "fail"}))
    print(call_tool_with_degradation(degraded_calculator, {"expression": "1+1"}))
