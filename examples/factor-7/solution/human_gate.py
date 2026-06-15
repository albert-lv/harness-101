"""
Factor 7：Human-in-the-Loop Gates（参考实现片段）
"""
import json
import os
import time
import uuid
from enum import Enum


class GateState(str, Enum):
    RUNNING = "running"
    PENDING = "pending"
    RESUMED = "resumed"
    CANCELLED = "cancelled"


class HumanGate:
    def __init__(self, state_file: str = "human_gate_state.json"):
        self.state_file = state_file
        self.state = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"status": GateState.RUNNING, "pending_actions": [], "audit": []}

    def _save(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def request_approval(self, action: dict) -> str:
        action_id = uuid.uuid4().hex[:8]
        pending = {
            "id": action_id,
            "action": action,
            "requested_at": time.time(),
        }
        self.state["pending_actions"].append(pending)
        self.state["status"] = GateState.PENDING
        self._save()
        return action_id

    def approve(self, action_id: str) -> dict:
        return self._resolve(action_id, "approved")

    def reject(self, action_id: str) -> dict:
        return self._resolve(action_id, "rejected")

    def _resolve(self, action_id: str, decision: str) -> dict:
        pending = [a for a in self.state["pending_actions"] if a["id"] == action_id]
        if not pending:
            return {"error": "未找到待确认操作"}
        action = pending[0]
        self.state["pending_actions"].remove(action)
        self.state["audit"].append({
            "id": action_id,
            "action": action["action"],
            "decision": decision,
            "resolved_at": time.time(),
        })
        self.state["status"] = GateState.RESUMED if decision == "approved" else GateState.CANCELLED
        self._save()
        return {"action_id": action_id, "decision": decision}


if __name__ == "__main__":
    gate = HumanGate()
    aid = gate.request_approval({"tool": "write_file", "path": "./important.txt"})
    print(f"操作 {aid} 已挂起，等待确认")
    print(gate.approve(aid))
