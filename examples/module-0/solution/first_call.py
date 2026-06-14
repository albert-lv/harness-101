"""
模块 0：环境与第一次 API 调用（参考实现）
"""
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

system_prompt = "你是一个乐于助人的助手。"
messages = [
    {"role": "user", "content": input("请输入你想说的话：")}
]

response = client.messages.create(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    system=system_prompt,
    messages=messages,
)

print("回复：", response.content[0].text)
print("输入 token:", response.usage.input_tokens)
print("输出 token:", response.usage.output_tokens)
