# 动手代码示例

本目录按 **Harness 12-Factor** 组织，每章提供可运行的骨架代码（`starter/`）与参考实现（`solution/`）。

> **学习建议**：先根据课程讲义自己实现，跑不通或想对比时再来看 `solution/`。

## 目录结构

```text
examples/
├── prep/                  # 前置：环境与第一次 API 调用
├── factor-1/              # Single Agent Loop
├── factor-2/              # Explicit Tool Contract
├── factor-3/              # Context Budgeting
├── factor-4/              # Failure-First Design
├── factor-5/              # Graceful Degradation
├── factor-6/              # Least-Privilege Tooling
├── factor-7/              # Human-in-the-Loop Gates
├── factor-8/              # Observable by Default
├── factor-9/              # Reproducible Runs
├── factor-10/             # Composable Agents
├── factor-11/             # Config-Driven Behavior
└── factor-12/             # Continuous Evaluation
```

每个 Factor 目录建议包含：

- `README.md` — 该 Factor 代码的说明与运行方式
- `starter/` — 骨架代码，留有 TODO 供你填补
- `solution/` — 参考实现
- `exercises.md` — 针对代码的额外练习

## 快速开始

```bash
# 进入任意 Factor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python starter/xxx.py
```

## 贡献代码示例

1. 保持示例与课程讲义一致。
2. 优先使用标准库 + `anthropic`（或兼容 OpenAI API 的库），避免引入框架。
3. 在 `README.md` 中说明运行所需的环境变量（如 `ANTHROPIC_API_KEY`）。
