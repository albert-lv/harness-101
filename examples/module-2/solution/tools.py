"""
模块 2：工具设计（参考实现）
"""
import os

FORBIDDEN_PREFIXES = ("/etc", "/usr", "/bin", "/sbin", "/sys", "/proc")


def validate_path(path: str) -> str | None:
    if not isinstance(path, str):
        return "path 必须是字符串"
    if any(path.startswith(p) for p in FORBIDDEN_PREFIXES):
        return f"禁止写入系统路径: {path}"
    if os.path.isabs(path) and not path.startswith(os.path.expanduser("~")):
        return f"只允许写入用户目录下的相对路径: {path}"
    return None


def write_file(path: str, content: str) -> str:
    if not isinstance(content, str):
        return "content 必须是字符串"

    error = validate_path(path)
    if error:
        return f"[错误] {error}"

    # 幂等：内容相同则跳过
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            existing = f.read()
        if existing == content:
            return f"[跳过] 文件内容已相同: {path}"

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"[成功] 已写入 {path}，字节数 {len(content.encode('utf-8'))}"


def calculator(expression: str) -> str:
    """计算一个数学表达式并返回结果。表达式只支持基本四则运算。"""
    if not isinstance(expression, str):
        return "[错误] expression 必须是字符串"
    allowed = set("0123456789+-*/(). ")
    if any(c not in allowed for c in expression):
        return "[错误] 表达式包含非法字符"
    try:
        result = eval(expression)  # 本示例仅用于演示，生产环境应使用 safe_eval
        return f"[结果] {expression} = {result}"
    except Exception as e:
        return f"[错误] 计算失败: {e}"
