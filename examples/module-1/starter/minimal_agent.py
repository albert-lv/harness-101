"""
模块 1：手写 Agent Loop（骨架代码）

目标：约 100 行实现一个带工具的 Agent Loop。
"""
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# TODO 1: 定义工具列表（name / description / input_schema）
TOOLS = []


def run_command(cmd: str) -> str:
    """TODO 2: 执行命令并返回结果。"""
    return f"模拟执行: {cmd}"


def agent_loop(task: str, max_steps: int = 10):
    messages = [{"role": "user", "content": task}]
    for step in range(max_steps):
        # TODO 3: 调用模型，传入 tools
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            messages=messages,
            # tools=...,
        )

        # TODO 4: 判断是文本回复还是工具调用
        # 如果是工具调用，执行工具并把结果塞回 messages
        # 如果是文本回复，打印并结束循环
        print(f"步骤 {step}:", response.content)
        break


if __name__ == "__main__":
    agent_loop("帮我查一下本机到 baidu.com 的网络延迟")
