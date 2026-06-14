# 术语表（Glossary）

> 本课程使用的一致术语。贡献者在新增内容时请优先使用本表定义，避免歧义。

## Agent

让大语言模型“做事”的循环：它能调用工具、观察结果、做多步决策，而不只是一问一答。Agent 的核心是 **loop**，不是模型本身。

## Harness / Agent Harness

把裸 LLM API 包装成可靠 Agent 的全部工程代码与运行时：上下文管理、prompt 组装、工具执行、权限沙箱、子 Agent 调度、错误恢复、trace。Claude Code、Cursor、OpenHands 本质上都是 Harness。

## Agent Loop

Agent 的核心状态机：`调模型 → 解析工具调用 → 执行工具 → 结果回填 context → 再调模型`，直到模型决定完成。

## Tool / 工具

Agent 与外部世界交互的唯一接口。每个工具包含 name、description（对模型可见的“prompt”）、参数 schema 和实际执行函数。

## Tool Contract / 工具契约

工具的 name、description、参数 schema、返回值格式、副作用与幂等语义的完整约定。契约写得好不好，直接决定模型调用是否正确。

## Context / Context Window

模型可见的全部输入文本。长度受限于模型的 context window，token 计费也基于此。Harness 必须管理 context 的预算与质量。

## Context Budgeting / Context 预算

把 context 当作有限资源来管理：截断、摘要、外置记忆，在信息损失与成本之间做权衡。

## Tool Call / 工具调用

模型在响应中请求调用某个工具，包含工具名和参数。Harness 负责解析、执行并把结果返回给模型。

## Hallucinated Call / 幻觉调用

模型调用不存在的工具，或编造不存在的参数。Harness 必须拦截并纠正。

## Dead Loop / 死循环

Agent 反复执行同一动作或反复出错，无法向前推进。需要通过最大步数、重复检测、阶段性目标等手段打断。

## Drift / 跑偏

Agent 在多步任务中偏离原始目标。通常用阶段目标、自检、人工介入来拉回。

## Idempotency / 幂等

同一操作执行多次与执行一次效果相同。对有副作用的工具（写文件、改配置）至关重要。

## Allow-List / 白名单

明确列出哪些工具在哪些上下文中可用。最小权限原则的体现：默认拒绝，显式授权。

## Human-in-the-Loop / 人工确认门

对危险或不可逆操作，Harness 暂停执行并等待人类确认，具备可恢复状态。

## Sandbox / 沙箱

把工具执行限制在隔离环境中（受限文件系统、网络隔离、只读模式），降低 Agent 误操作的影响面。

## Trace / 运行轨迹

一次 Agent 运行的完整结构化记录：思考、工具调用、结果、错误、完成。trace 是 Agent 的“黑匣子”。

## Event / 事件

Trace 中的单个结构化记录。常见事件类型：think、tool_call、tool_result、error、complete。

## Orchestrator-Worker / 主-子编排

多 Agent 架构：主 Agent（orchestrator）拆分任务并派发给子 Agent（worker），子 Agent 独立完成后返回结果，主 Agent 汇总。

## 12-Factor Harness

本课程提出的生产级 Harness 设计方法论，共 12 条原则，覆盖 loop、工具、context、容错、权限、可观测性、编排、配置与评估。

## Config-Driven / 配置驱动

模型选择、系统提示、工具列表、安全策略等行为应外置到配置中，而不是硬编码，便于环境切换与 A/B 测试。

## Continuous Evaluation / 持续评估

Harness 的质量不应只看 demo 是否成功，而应持续测量失败率、恢复率、任务完成率、成本与延迟。
