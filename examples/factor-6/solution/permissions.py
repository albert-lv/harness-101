"""
Factor 6：Least-Privilege Tooling（参考实现片段）
"""
import os

ALLOWED_TOOLS = {"read_file", "list_dir", "run_command"}
FORBIDDEN_PATHS = ("/etc", "/usr", "/bin", "/sbin", "/sys", "/proc")
WRITE_TOOLS = {"write_file", "delete_file", "run_command"}


def validate_path(path: str) -> str | None:
    if not isinstance(path, str):
        return "path 必须是字符串"
    if any(path.startswith(p) for p in FORBIDDEN_PATHS):
        return f"禁止访问系统路径: {path}"
    return None


def is_tool_allowed(tool_name: str) -> bool:
    return tool_name in ALLOWED_TOOLS


def is_write_operation(tool_name: str) -> bool:
    return tool_name in WRITE_TOOLS


def execute_with_permission(tool_name: str, tool_input: dict, read_only: bool = True):
    if not is_tool_allowed(tool_name):
        return f"[拒绝] 工具 {tool_name} 不在白名单中"
    if read_only and is_write_operation(tool_name):
        return f"[拒绝] 当前为只读模式，禁止调用 {tool_name}"
    if "path" in tool_input:
        err = validate_path(tool_input["path"])
        if err:
            return f"[拒绝] {err}"
    return f"[执行] {tool_name}({tool_input})"


if __name__ == "__main__":
    print(execute_with_permission("read_file", {"path": "./notes.txt"}, read_only=True))
    print(execute_with_permission("write_file", {"path": "./notes.txt"}, read_only=True))
    print(execute_with_permission("read_file", {"path": "/etc/passwd"}, read_only=True))
