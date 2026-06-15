"""
模块 1：手写 Agent Loop（参考实现）

一个约 100 行的最小 Agent：能调用 shell 命令完成多步任务。
"""
import os
import subprocess
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

TOOLS = [
    {
        "name": "run_command",
        "description": "在本地 shell 中运行一个命令并返回标准输出。命令必须是只读的（如 ping、cat、ls），禁止写操作。",
        "input_schema": {
            "type": "object",
            "properties": {
                "cmd": {"type": "string", "description": "要执行的 shell 命令"}
            },
            "required": ["cmd"]
        }
    }
]


def run_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout or result.stderr
    except Exception as e:
        return f"命令执行失败: {e}"


def agent_loop(task: str, max_steps: int = 10):
    messages = [{"role": "user", "content": task}]
    for step in range(max_steps):
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            messages=messages,
            tools=TOOLS,
        )

        print(f"\n--- 步骤 {step} ---")
        print("模型输出:", response.content)

        if response.stop_reason != "tool_use":
            print("\n最终回复:", response.content[0].text)
            return

        tool_use = next((b for b in response.content if b.type == "tool_use"), None)
        if not tool_use:
            return

        print("调用工具:", tool_use.name, tool_use.input)
        result = run_command(tool_use.input["cmd"])

        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                }
            ],
        })

    print("达到最大步数，循环结束。")


if __name__ == "__main__":
    agent_loop("帮我查一下本机到 baidu.com 的网络延迟")
