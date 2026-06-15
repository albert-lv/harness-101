"""
Factor 6：Least-Privilege Tooling（骨架代码）

目标：实现默认最小权限、工具白名单、只读模式、路径黑名单。
"""

# TODO 1: 定义工具白名单：哪些工具在当前上下文中可用
# TODO 2: 实现 read_only 开关：开启时拦截所有写操作
# TODO 3: 实现路径黑名单：禁止访问 /etc、/usr 等系统路径
# TODO 4: 实现权限检查装饰器，给工具函数统一加权限门


def permission_check(tool_name: str, read_only: bool = True):
    raise NotImplementedError("TODO")
