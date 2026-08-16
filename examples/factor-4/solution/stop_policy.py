"""
Factor 4：Knowing When to Stop（参考实现）

Turn termination policy：显式 task_done（需校验）/ 隐式 finish_reason 完成判定，
三类循环检测（重复调用、diminishing returns、相似内容），错误阈值熔断。
参考：nano-agent pkg/agent/turn_policy.go
"""
import difflib

SIMILARITY_THRESHOLD = 0.9


class TurnPolicy:
    def __init__(self, max_repeat: int = 3, max_stale: int = 4, max_errors: int = 3,
                 verifier=None):
        self.max_repeat = max_repeat
        self.max_stale = max_stale
        self.max_errors = max_errors
        self.verifier = verifier or (lambda claim: True)  # 校验"完成"声明，默认放行
        self.recent_calls: list[str] = []
        self.seen_observations: set[str] = set()
        self.stale_steps = 0
        self.last_output = ""
        self.consecutive_errors = 0

    def _check_loop(self, signature: str, observation: str) -> tuple[bool, str]:
        # 重复调用：同一签名连续出现 max_repeat 次
        self.recent_calls.append(signature)
        tail = self.recent_calls[-self.max_repeat:]
        if len(tail) == self.max_repeat and len(set(tail)) == 1:
            return True, f"循环检测：工具调用 {signature} 连续重复 {self.max_repeat} 次"
        # diminishing returns：连续 max_stale 步没有新观测
        if observation in self.seen_observations:
            self.stale_steps += 1
        else:
            self.seen_observations.add(observation)
            self.stale_steps = 0
        if self.stale_steps >= self.max_stale:
            return True, f"diminishing returns：连续 {self.max_stale} 步无新信息"
        # 相似内容循环：相邻输出几乎一样
        similarity = difflib.SequenceMatcher(None, self.last_output, observation).ratio()
        self.last_output = observation
        if similarity >= SIMILARITY_THRESHOLD and observation:
            return True, f"相似内容循环：相邻输出相似度 {similarity:.2f}"
        return False, ""

    def should_stop(self, action: dict) -> tuple[bool, str]:
        """每个 turn 调用一次。action 是模型这一步的决策。返回 (是否停止, 原因)。"""
        if action["type"] == "task_done":
            # 显式完成：校验声明是否属实，不可轻信模型自称"完成了"
            if self.verifier(action.get("claim", "")):
                return True, "任务完成（task_done，已通过校验）"
            return False, "task_done 校验未通过，继续执行"
        if action["type"] == "finish":
            # 隐式完成：模型自行结束且没有 pending 工具调用
            return True, f"隐式完成（finish_reason={action.get('finish_reason')})"
        if action["type"] == "error":
            self.consecutive_errors += 1
            if self.consecutive_errors >= self.max_errors:
                return True, f"错误熔断：连续 {self.consecutive_errors} 次错误"
            return False, ""
        self.consecutive_errors = 0
        return self._check_loop(action["signature"], action.get("observation", ""))


def run_loop(actions: list[dict], policy: TurnPolicy):
    """模拟 Agent Loop：逐步把模型动作喂给 policy，直到 policy 叫停。"""
    for step, action in enumerate(actions):
        stop, reason = policy.should_stop(action)
        print(f"step={step} action={action['type']}" + (f" -> 停止: {reason}" if stop else ""))
        if stop:
            return reason
    return "动作序列耗尽"


if __name__ == "__main__":
    print("== 场景 1：重复调用（签名相同，观测不同） ==")
    calls = [{"type": "tool_call", "signature": "search:{'q': 'x'}",
              "observation": obs} for obs in ["r1", "r2", "r3", "r4", "r5"]]
    run_loop(calls, TurnPolicy())
    print("== 场景 2：错误熔断 ==")
    run_loop([{"type": "error", "message": "boom"} for _ in range(5)], TurnPolicy())
    print("== 场景 3：相似内容循环 ==")
    same = "搜索完成，没有找到相关结果"
    run_loop([{"type": "tool_call", "signature": f"search:{i}", "observation": same}
              for i in range(5)], TurnPolicy())
    print("== 场景 4：task_done 校验 ==")
    policy = TurnPolicy(verifier=lambda claim: "测试通过" in claim)
    run_loop([{"type": "task_done", "claim": "我写完了"}, {"type": "task_done", "claim": "测试通过"}], policy)
