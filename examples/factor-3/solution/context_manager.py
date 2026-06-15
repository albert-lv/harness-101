"""
Factor 3：Context Budgeting（参考实现片段）

简化版：按字符数估算 token，实现截断 + 摘要 + 外置记忆。
"""
import json
import os


class ContextManager:
    def __init__(self, max_tokens: int = 4000, token_per_char: float = 0.4):
        self.max_tokens = max_tokens
        self.token_per_char = token_per_char
        self.messages = []
        self.memory_dir = ".memory"
        os.makedirs(self.memory_dir, exist_ok=True)

    def estimate_tokens(self, text: str) -> int:
        return int(len(text) * self.token_per_char)

    def budget(self) -> int:
        return sum(self.estimate_tokens(str(m.get("content", ""))) for m in self.messages)

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if self.budget() > self.max_tokens * 0.8:
            self.compress()

    def _externalize(self, index: int) -> str:
        """把一条 message 外置到文件，返回指针。"""
        path = os.path.join(self.memory_dir, f"msg_{index:04d}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.messages[index], f, ensure_ascii=False)
        return f"[内容已外置到 {path}]"

    def compress(self):
        """保留 system 和最近 2 轮，较早内容摘要或外置。"""
        # 简单策略：把最老的用户/助手消息外置
        for i, m in enumerate(self.messages):
            if m["role"] in ("user", "assistant") and i < len(self.messages) - 4:
                self.messages[i]["content"] = self._externalize(i)


if __name__ == "__main__":
    cm = ContextManager(max_tokens=200)
    for i in range(20):
        cm.add_message("user", f"这是第 {i} 条用户消息，包含一些重复文本。" * 10)
    print(f"当前消息数: {len(cm.messages)}, 估算 token: {cm.budget()}")
