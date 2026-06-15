"""
Factor 11：Config-Driven Behavior（骨架代码）

目标：把模型、prompt、工具列表、安全策略外置到配置。
"""

# TODO 1: 创建 config.yaml，包含 model、max_tokens、system_prompt、tools、permissions
# TODO 2: 实现 load_config(path) 读取配置
# TODO 3: 实现 ConfigDrivenAgent，所有行为从配置初始化
# TODO 4: 支持激进/保守两种配置切换


class ConfigDrivenAgent:
    def __init__(self, config: dict):
        raise NotImplementedError("TODO")
