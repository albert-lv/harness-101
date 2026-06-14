# 动手代码示例

本目录按模块提供可运行的骨架代码（`starter/`）与参考实现（`solution/`）。

> **学习建议**：先根据课程讲义自己实现，跑不通或想对比时再来看 `solution/`。

## 目录结构

```text
examples/
├── module-0/           # 环境与第一次 API 调用
├── module-1/           # 手写 Agent Loop
├── module-2/           # 工具设计
├── module-3/           # Context 管理
├── module-4/           # 失败模式与容错
├── module-5/           # 权限与沙箱
├── module-6/           # 可观测性
├── module-7/           # 多 Agent 编排
└── module-8/           # 阅读真实 Harness
```

每个模块目录建议包含：

- `README.md` — 该模块代码的说明与运行方式
- `starter/` — 骨架代码，留有 TODO 供你填补
- `solution/` — 参考实现
- `exercises.md` — 针对代码的额外练习

## 快速开始

```bash
# 进入任意模块
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python starter/first_call.py
```

## 贡献代码示例

1. 保持示例与课程讲义一致。
2. 优先使用标准库 + `anthropic`（或兼容 OpenAI API 的库），避免引入框架。
3. 在 `README.md` 中说明运行所需的环境变量（如 `ANTHROPIC_API_KEY`）。
