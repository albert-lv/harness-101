"""
Factor 3：Context Budgeting（骨架代码）

目标：实现 context 预算管理，防止长任务撑爆窗口。
"""

# TODO 1: 实现一个 ContextManager 类，维护 messages 列表
# TODO 2: 实现截断策略：当总 token 超过阈值时，截断早期工具输出
# TODO 3: 实现摘要策略：当超过阈值时，把早期对话压缩成摘要
# TODO 4: 实现外置记忆：把大块内容存到文件，context 里只留指针


class ContextManager:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.messages = []

    def add_message(self, role: str, content: str):
        raise NotImplementedError("TODO")

    def budget(self):
        """返回当前已用 token 估算。"""
        raise NotImplementedError("TODO")

    def compress(self):
        """当接近阈值时压缩 messages。"""
        raise NotImplementedError("TODO")
