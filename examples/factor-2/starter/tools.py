"""
模块 2：工具设计（骨架代码）

目标：为模块 1 的 Agent 设计健壮的工具接口。
"""

# TODO 1: 写一个带参数校验的 write_file 工具
# 要求：
# - 校验 path 是 str
# - 校验 content 是 str
# - 校验 path 不在黑名单中（如 /etc、/usr）
# - 返回模型能理解的字符串，而不是抛异常


def write_file(path: str, content: str) -> str:
    raise NotImplementedError("TODO")


# TODO 2: 让 write_file 具备幂等性：重复写入相同内容应返回成功但不重复写
# 提示：先读取文件，比较 content


# TODO 3: 写一个模糊 description 的工具，观察模型如何误用

def calculator(expression: str) -> str:
    raise NotImplementedError("TODO")
