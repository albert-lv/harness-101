"""
模块 6：可观测性——Trace 与 Events（骨架代码）

目标：给 Agent Loop 增加结构化事件日志。
"""

# TODO 1: 定义 Event 数据类 / TypedDict，包含：
# - event_id, parent_id, type, timestamp, step, content

# TODO 2: 在 Agent Loop 的每个阶段 emit 事件：
# - think: 模型开始思考
# - tool_call: 模型决定调用工具
# - tool_result: 工具返回结果
# - error: 发生错误
# - complete: 任务完成

# TODO 3: 把事件写入 JSONL 文件

# TODO 4: 实现一个简单查看器，按时间线打印事件
