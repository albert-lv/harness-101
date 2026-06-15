"""
Factor 9：Reproducible Runs（参考实现片段）
"""
import json
import os


def save_run(trace: list, config: dict, path: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"trace": trace, "config": config}, f, ensure_ascii=False, indent=2)


def replay(trace_path: str):
    """按 trace 推进 loop，不调用真实模型。"""
    with open(trace_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    trace = data["trace"]
    config = data["config"]

    step = 0
    for event in trace:
        print(f"[replay] step={step} type={event['type']}")
        if event["type"] == "tool_call":
            # 模拟 Harness 层的拦截检查
            if event["content"]["name"] not in config.get("allowed_tools", []):
                print("  -> Harness 拦截：未知工具")
        step += 1
    print("[replay] 完成")


def regression_test(trace_path: str, expected_intercept_step: int) -> bool:
    with open(trace_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for i, event in enumerate(data["trace"]):
        if event["type"] == "error":
            if i == expected_intercept_step:
                return True
            return False
    return False


if __name__ == "__main__":
    sample_trace = [
        {"type": "think", "content": {"task": "算 1+1"}},
        {"type": "tool_call", "content": {"name": "calculator", "input": {"expression": "1+1"}}},
        {"type": "error", "content": {"message": "工具结果异常"}},
    ]
    sample_config = {"allowed_tools": ["calculator"]}
    save_run(sample_trace, sample_config, "sample_trace.json")
    replay("sample_trace.json")
    print("回归测试通过:", regression_test("sample_trace.json", 2))
