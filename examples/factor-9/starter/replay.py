"""
Factor 9：Reproducible Runs（骨架代码）

目标：给定 trace 和配置，能复现 loop 路径并验证 Harness 行为。
"""

# TODO 1: 实现 save_run(trace, config, path) 保存 trace + config
# TODO 2: 实现 replay(trace_path)：读取 trace，跳过模型调用，按记录推进 loop
# TODO 3: 实现 regression_test(trace_path)：验证 Harness 对某条失败 trace 的拦截/恢复行为


def save_run(trace: list, config: dict, path: str):
    raise NotImplementedError("TODO")


def replay(trace_path: str):
    raise NotImplementedError("TODO")
