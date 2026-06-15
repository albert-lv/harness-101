"""
Factor 11：Config-Driven Behavior（参考实现片段）
"""
import json


DEFAULT_CONFIG = {
    "model": "claude-3-5-sonnet-latest",
    "max_tokens": 1024,
    "system_prompt": "你是一个谨慎的助手。",
    "allowed_tools": ["read_file", "calculator"],
    "read_only": True,
    "max_steps": 10,
}


class ConfigDrivenAgent:
    def __init__(self, config: dict):
        self.config = {**DEFAULT_CONFIG, **config}

    def load_config(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def is_tool_allowed(self, tool_name: str) -> bool:
        return tool_name in self.config["allowed_tools"]

    def can_write(self) -> bool:
        return not self.config.get("read_only", True)

    def summary(self):
        return {
            "model": self.config["model"],
            "read_only": self.config["read_only"],
            "allowed_tools": self.config["allowed_tools"],
        }


if __name__ == "__main__":
    aggressive = ConfigDrivenAgent({"read_only": False, "allowed_tools": ["read_file", "write_file", "calculator"]})
    conservative = ConfigDrivenAgent({"read_only": True})
    print("aggressive:", aggressive.summary())
    print("conservative:", conservative.summary())
