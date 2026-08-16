"""
模块 6：可观测性——Trace 与 Events（参考实现片段）
"""
import json
import uuid
import time
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Event:
    event_id: str
    parent_id: Optional[str]
    trace_id: str
    type: str  # think, tool_call, tool_result, error, complete
    step: int
    timestamp: float
    content: dict


class TraceLogger:
    def __init__(self, trace_id: Optional[str] = None, path: Optional[str] = None):
        self.trace_id = trace_id or uuid.uuid4().hex[:12]
        self.path = path or f"trace_{self.trace_id}.jsonl"
        self.events: List[Event] = []

    def emit(self, type: str, step: int, content: dict, parent_id: Optional[str] = None):
        event = Event(
            event_id=uuid.uuid4().hex[:8],
            parent_id=parent_id,
            trace_id=self.trace_id,
            type=type,
            step=step,
            timestamp=time.time(),
            content=content,
        )
        self.events.append(event)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")
        return event.event_id

    def print_timeline(self):
        for e in self.events:
            prefix = f"[{e.type:12}] step={e.step}"
            print(prefix, json.dumps(e.content, ensure_ascii=False)[:120])


# 与 Agent Loop 集成示例（伪代码）
def agent_loop_with_trace(task: str, logger: TraceLogger):
    # ...
    # 模型调用前
    logger.emit("think", step=0, content={"task": task})
    # 模型返回工具调用
    # tool_call_id = logger.emit("tool_call", step=step, content={"name": name, "input": input})
    # 工具返回后
    # logger.emit("tool_result", step=step, content={"output": output}, parent_id=tool_call_id)
    # ...
    pass
