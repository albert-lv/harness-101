"""
模块 4：失败模式与容错（参考实现片段）

展示如何在 Agent Loop 中集成：最大步数、重复检测、未知工具拦截、API 重试。
"""
import os
import time
from anthropic import Anthropic, APIStatusError

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
TOOLS = [
    {
        "name": "run_command",
        "description": "运行只读命令并返回输出",
        "input_schema": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]},
    }
]


def call_model_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=1024,
                messages=messages,
                tools=TOOLS,
            )
        except APIStatusError as e:
            if e.status_code == 429:
                wait = 2 ** attempt
                print(f"限流，等待 {wait}s 后重试...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("API 调用多次重试失败")


def is_duplicate(recent_calls, threshold=2):
    if len(recent_calls) < threshold:
        return False
    return len(set(recent_calls[-threshold:])) == 1


def run_command(cmd: str) -> str:
    import subprocess
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout or result.stderr
    except Exception as e:
        return f"命令失败: {e}"


def agent_loop(task: str, max_steps: int = 10):
    messages = [{"role": "user", "content": task}]
    recent_calls = []

    for step in range(max_steps):
        if step > 0 and step % 3 == 0:
            messages.append({
                "role": "user",
                "content": "[Harness 自检] 请用一句话总结当前目标，并确认下一步是否合理。"
            })

        response = call_model_with_retry(messages)

        if response.stop_reason != "tool_use":
            print("最终回复:", response.content[0].text)
            return

        tool_use = next((b for b in response.content if b.type == "tool_use"), None)
        if not tool_use:
            continue

        call_sig = f"{tool_use.name}:{tool_use.input}"
        recent_calls.append(call_sig)

        if tool_use.name not in {t["name"] for t in TOOLS}:
            result = f"[错误] 未知工具: {tool_use.name}。可用工具: {[t['name'] for t in TOOLS]}"
        elif is_duplicate(recent_calls):
            result = "[警告] 检测到重复动作，请换一种方式推进任务。"
        else:
            result = run_command(tool_use.input.get("cmd", ""))

        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": result}],
        })

    print("达到最大步数，循环结束。")
