"""
模块 0：环境与第一次 API 调用（骨架代码）

目标：从命令行接收一句话，调用 LLM 并打印回复。
前置：设置环境变量 ANTHROPIC_API_KEY
"""
import os
from anthropic import Anthropic

# TODO 1: 从环境变量读取 API Key，不要硬编码
client = Anthropic(api_key=...)  # type: ignore

# TODO 2: 构造第一次调用所需的三要素
# system_prompt = ...
# messages = ...
# model = ...

response = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    # 补全 system / messages
)

print("回复：", response.content[0].text)
print("输入 token:", response.usage.input_tokens)
print("输出 token:", response.usage.output_tokens)
